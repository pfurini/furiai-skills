#!/usr/bin/env python3
"""Derive trustworthy execution metrics from supported Pi transcript formats."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any, Literal, Never, cast

TranscriptFormat = Literal["pi-subagents-output-v1", "pi-json-events-v3"]

_SUPPORTED_FORMATS: tuple[TranscriptFormat, ...] = (
    "pi-subagents-output-v1",
    "pi-json-events-v3",
)
_TOOL_NAME = re.compile(r"[a-z][a-z0-9_-]*\Z")
_COUNT_FIELDS = ("input", "output", "cacheRead", "cacheWrite", "totalTokens")


class TranscriptMetricsError(ValueError):
    """Raised when transcript content violates the metrics contract."""


class _Metrics:
    def __init__(self) -> None:
        self.tool_calls: dict[str, int] = {}
        self.assistant_turns = 0
        self.tool_errors = 0
        self.usage: dict[str, int | float] = {
            "input": 0,
            "output": 0,
            "cache_read": 0,
            "cache_write": 0,
            "reasoning": 0,
            "total_tokens": 0,
            "cost_usd": 0.0,
        }
        self.effective_models: set[str] = set()

    def add_tool_call(self, name: Any, *, location: str) -> None:
        tool_name = _tool_name(name, location=location)
        self.tool_calls[tool_name] = self.tool_calls.get(tool_name, 0) + 1

    def add_assistant(self, message: Any, *, location: str) -> None:
        message_object = _object(message, f"{location} message")
        if message_object.get("role") != "assistant":
            raise TranscriptMetricsError(f"{location} is not an assistant message")

        content = message_object.get("content")
        if not isinstance(content, list):
            raise TranscriptMetricsError(f"{location} assistant content must be an array")
        self.add_usage(message_object.get("usage"), location=f"{location} assistant usage")
        self.effective_models.add(_effective_model(message_object, location=location))
        self.assistant_turns += 1

    def add_usage(self, raw_usage: Any, *, location: str) -> None:
        usage = _object(raw_usage, location)
        values = {
            field: _count(usage.get(field), location=f"{location}.{field}")
            for field in _COUNT_FIELDS
        }
        reasoning = _count(usage.get("reasoning", 0), location=f"{location}.reasoning")
        cost = _object(usage.get("cost"), f"{location}.cost")
        cost_total = _number(cost.get("total"), location=f"{location}.cost.total")

        self.usage["input"] += values["input"]
        self.usage["output"] += values["output"]
        self.usage["cache_read"] += values["cacheRead"]
        self.usage["cache_write"] += values["cacheWrite"]
        self.usage["reasoning"] += reasoning
        self.usage["total_tokens"] += values["totalTokens"]
        self.usage["cost_usd"] += cost_total

    def finish(self, *, source_format: TranscriptFormat, transcript_chars: int) -> dict[str, Any]:
        if self.assistant_turns == 0:
            raise TranscriptMetricsError(
                "transcript has no authoritative completed assistant message with usage and model"
            )
        tool_calls = dict(sorted(self.tool_calls.items()))
        return {
            "schema_version": "opin.transcript-metrics/v1",
            "source_format": source_format,
            "tool_calls": tool_calls,
            "total_tool_calls": sum(tool_calls.values()),
            "assistant_turns": self.assistant_turns,
            "tool_errors": self.tool_errors,
            "usage": self.usage,
            "effective_models": sorted(self.effective_models),
            "transcript_chars": transcript_chars,
        }


def _object(value: Any, location: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TranscriptMetricsError(f"{location} must be a JSON object")
    return cast(dict[str, Any], value)


def _count(value: Any, *, location: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise TranscriptMetricsError(f"{location} must be a non-negative integer")
    return value


def _number(value: Any, *, location: str) -> int | float:
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or value < 0
    ):
        raise TranscriptMetricsError(f"{location} must be a finite non-negative number")
    return value


def _tool_name(value: Any, *, location: str) -> str:
    if not isinstance(value, str) or _TOOL_NAME.fullmatch(value) is None:
        raise TranscriptMetricsError(
            f"{location} tool name must be a lowercase registered Pi name"
        )
    return value


def _nonempty_string(value: Any, *, location: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TranscriptMetricsError(f"{location} must be a non-empty string")
    return value


def _effective_model(message: dict[str, Any], *, location: str) -> str:
    provider = _nonempty_string(message.get("provider"), location=f"{location} provider")
    model = _nonempty_string(
        message.get("responseModel", message.get("model")),
        location=f"{location} effective model",
    )
    return f"{provider}/{model}"


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-standard JSON constant {value}")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise TranscriptMetricsError(f'duplicate JSON key "{key}"')
        result[key] = value
    return result


def _read_records(path: Path) -> tuple[list[dict[str, Any]], int]:
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise TranscriptMetricsError(f"transcript is not strict UTF-8: {error}") from error

    lines = text.split("\n")
    ends_with_lf = bool(lines and lines[-1] == "")
    if ends_with_lf:
        lines.pop()
    if not lines:
        raise TranscriptMetricsError("transcript contains no JSONL records")

    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(lines, start=1):
        terminated_by_lf = line_number < len(lines) or ends_with_lf
        if line.endswith("\r"):
            if not terminated_by_lf:
                raise TranscriptMetricsError(
                    f"transcript line {line_number} has a CR not followed by LF"
                )
            line = line[:-1]
        if not line:
            raise TranscriptMetricsError(f"transcript line {line_number} is empty")
        try:
            record = json.loads(
                line,
                object_pairs_hook=_unique_object,
                parse_constant=_reject_constant,
            )
        except TranscriptMetricsError as error:
            raise TranscriptMetricsError(f"transcript line {line_number}: {error}") from error
        except (json.JSONDecodeError, ValueError) as error:
            raise TranscriptMetricsError(
                f"transcript line {line_number} is malformed JSON: {error}"
            ) from error
        records.append(_object(record, f"transcript line {line_number}"))
    return records, len(text)


def _message(record: dict[str, Any], *, location: str) -> dict[str, Any]:
    return _object(record.get("message"), f"{location} message")


def _tool_call_identity(content: dict[str, Any], *, location: str) -> tuple[str, str]:
    call_id = _nonempty_string(content.get("id"), location=f"{location} tool call id")
    name = _tool_name(content.get("name"), location=location)
    return call_id, name


def _parse_subagents_output(
    records: list[dict[str, Any]], metrics: _Metrics
) -> None:
    pending_calls: dict[str, str] = {}
    for index, record in enumerate(records, start=1):
        location = f"transcript line {index}"
        record_type = record.get("type")
        if record_type == "assistant":
            message = _message(record, location=location)
            metrics.add_assistant(message, location=location)
            content = cast(list[Any], message["content"])
            for content_index, item in enumerate(content):
                if not isinstance(item, dict) or item.get("type") != "toolCall":
                    continue
                item_object = cast(dict[str, Any], item)
                item_location = f"{location} content[{content_index}]"
                call_id, name = _tool_call_identity(item_object, location=item_location)
                if call_id in pending_calls:
                    raise TranscriptMetricsError(f"{item_location} duplicates tool call id {call_id}")
                pending_calls[call_id] = name
                metrics.add_tool_call(name, location=item_location)
        elif record_type == "toolResult":
            message = _message(record, location=location)
            if message.get("role") != "toolResult":
                continue
            call_id = _nonempty_string(
                message.get("toolCallId"), location=f"{location} tool result id"
            )
            name = _tool_name(message.get("toolName"), location=location)
            expected_name = pending_calls.pop(call_id, None)
            if expected_name is None:
                raise TranscriptMetricsError(
                    f"{location} has no matching assistant tool call for id {call_id}"
                )
            if name != expected_name:
                raise TranscriptMetricsError(
                    f"{location} tool name {name} does not match {expected_name} for id {call_id}"
                )
            is_error = message.get("isError")
            if not isinstance(is_error, bool):
                raise TranscriptMetricsError(f"{location} tool result isError must be boolean")
            metrics.tool_errors += int(is_error)
            if "usage" in message:
                metrics.add_usage(message["usage"], location=f"{location} tool-result usage")
        elif record_type != "user":
            raise TranscriptMetricsError(f"{location} has unknown pi-subagents output type")

    if pending_calls:
        call_ids = ", ".join(sorted(pending_calls))
        raise TranscriptMetricsError(
            f"transcript has tool calls without matching tool results: {call_ids}"
        )


def _parse_json_events(records: list[dict[str, Any]], metrics: _Metrics) -> None:
    pending_calls: dict[str, str] = {}
    for index, record in enumerate(records, start=1):
        location = f"transcript line {index}"
        event_type = record.get("type")
        if event_type == "message_end":
            message = _message(record, location=location)
            role = message.get("role")
            if role == "assistant":
                metrics.add_assistant(message, location=location)
            elif role == "toolResult" and "usage" in message:
                metrics.add_usage(message["usage"], location=f"{location} tool-result usage")
        elif event_type == "tool_execution_start":
            call_id = _nonempty_string(
                record.get("toolCallId"), location=f"{location} tool call id"
            )
            name = _tool_name(record.get("toolName"), location=location)
            if call_id in pending_calls:
                raise TranscriptMetricsError(f"{location} duplicates tool call id {call_id}")
            pending_calls[call_id] = name
            metrics.add_tool_call(name, location=location)
        elif event_type == "tool_execution_end":
            call_id = _nonempty_string(
                record.get("toolCallId"), location=f"{location} tool result id"
            )
            name = _tool_name(record.get("toolName"), location=location)
            expected_name = pending_calls.pop(call_id, None)
            if expected_name is None:
                raise TranscriptMetricsError(
                    f"{location} has no matching tool_execution_start for id {call_id}"
                )
            if name != expected_name:
                raise TranscriptMetricsError(
                    f"{location} tool name {name} does not match {expected_name} for id {call_id}"
                )
            is_error = record.get("isError")
            if not isinstance(is_error, bool):
                raise TranscriptMetricsError(f"{location} isError must be boolean")
            metrics.tool_errors += int(is_error)

    if pending_calls:
        call_ids = ", ".join(sorted(pending_calls))
        raise TranscriptMetricsError(
            "transcript has tool_execution_start records without matching "
            f"tool_execution_end records: {call_ids}"
        )


def parse_transcript(path: Path, *, source_format: TranscriptFormat) -> dict[str, Any]:
    """Return transcript-derived metrics or raise ``TranscriptMetricsError``."""
    if source_format not in _SUPPORTED_FORMATS:
        raise TranscriptMetricsError(f"unsupported source format: {source_format}")

    records, transcript_chars = _read_records(path)
    metrics = _Metrics()
    parser: Callable[[list[dict[str, Any]], _Metrics], None]
    if source_format == "pi-subagents-output-v1":
        parser = _parse_subagents_output
    else:
        parser = _parse_json_events
    parser(records, metrics)
    return metrics.finish(source_format=source_format, transcript_chars=transcript_chars)


class _ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> Never:
        _print_error(message)
        raise SystemExit(2)


def _print_error(error: object) -> None:
    message = " ".join(str(error).splitlines())
    encoded = f"error: {message}".encode("utf-8", errors="replace")[:2000]
    print(encoded.decode("utf-8", errors="ignore"), file=sys.stderr)


def main() -> int:
    parser = _ArgumentParser(description="Derive metrics from a Pi transcript")
    parser.add_argument("--format", required=True, choices=_SUPPORTED_FORMATS)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    try:
        metrics = parse_transcript(args.input, source_format=args.format)
    except TranscriptMetricsError as error:
        _print_error(error)
        return 2
    except OSError as error:
        _print_error(error)
        return 1

    serialized = json.dumps(
        metrics,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ) + "\n"
    try:
        args.output.write_text(serialized, encoding="utf-8", newline="\n")
    except OSError as error:
        _print_error(error)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Contract and regression tests for transcript-derived execution metrics."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from conftest import SKILL_ROOT, TEST_ROOT

sys.path.insert(0, os.fspath(SKILL_ROOT))

from scripts.transcript_metrics import (  # noqa: E402
    TranscriptMetricsError,
    parse_transcript,
)


TRANSCRIPT_FIXTURES = TEST_ROOT / "fixtures/transcripts"


def _usage(**overrides: Any) -> dict[str, Any]:
    usage: dict[str, Any] = {
        "input": 1,
        "output": 2,
        "cacheRead": 3,
        "cacheWrite": 4,
        "totalTokens": 10,
        "cost": {
            "input": 0.1,
            "output": 0.2,
            "cacheRead": 0.3,
            "cacheWrite": 0.4,
            "total": 1.0,
        },
    }
    usage.update(overrides)
    return usage


def _assistant_message(**overrides: Any) -> dict[str, Any]:
    message: dict[str, Any] = {
        "role": "assistant",
        "content": [{"type": "text", "text": "Done."}],
        "provider": "openai",
        "model": "gpt-5",
        "usage": _usage(),
    }
    message.update(overrides)
    return message


def test_pi_subagents_output_metrics_are_derived_from_messages() -> None:
    path = TRANSCRIPT_FIXTURES / "pi-subagents-output.jsonl"

    metrics = parse_transcript(path, source_format="pi-subagents-output-v1")

    assert metrics == {
        "schema_version": "pi-skill-creator.transcript-metrics/v1",
        "source_format": "pi-subagents-output-v1",
        "tool_calls": {"bash": 1, "read": 2},
        "total_tool_calls": 3,
        "assistant_turns": 2,
        "tool_errors": 1,
        "usage": {
            "input": 121,
            "output": 22,
            "cache_read": 50,
            "cache_write": 9,
            "reasoning": 5,
            "total_tokens": 202,
            "cost_usd": pytest.approx(0.0123),
        },
        "effective_models": ["openai/gpt-5"],
        "transcript_chars": len(path.read_bytes().decode("utf-8")),
    }


def test_pi_json_metrics_use_lifecycle_events_without_double_counting_updates() -> None:
    path = TRANSCRIPT_FIXTURES / "pi-json-events.jsonl"

    metrics = parse_transcript(path, source_format="pi-json-events-v3")

    assert metrics["tool_calls"] == {"bash": 1, "read": 1}
    assert metrics["total_tool_calls"] == 2
    assert metrics["assistant_turns"] == 2
    assert metrics["tool_errors"] == 1
    assert metrics["usage"] == {
        "input": 121,
        "output": 22,
        "cache_read": 50,
        "cache_write": 9,
        "reasoning": 5,
        "total_tokens": 202,
        "cost_usd": pytest.approx(0.0123),
    }
    assert metrics["effective_models"] == ["openai/gpt-5"]


def test_response_model_is_the_effective_model(jsonl_factory: Any) -> None:
    path = jsonl_factory(
        [
            {
                "type": "message_end",
                "message": _assistant_message(
                    provider="openrouter",
                    model="auto",
                    responseModel="anthropic/claude-sonnet-4.5",
                ),
            }
        ]
    )

    metrics = parse_transcript(path, source_format="pi-json-events-v3")

    assert metrics["effective_models"] == [
        "openrouter/anthropic/claude-sonnet-4.5"
    ]


@pytest.mark.parametrize(
    ("content", "source_format", "error"),
    [
        (b'{"type":"assistant"}\nnot-json\n', "pi-subagents-output-v1", "line 2"),
        (b'[]\n', "pi-subagents-output-v1", "JSON object"),
        (b'{"type":"assistant","message":{"role":"assistant","content":[]}}\n', "pi-subagents-output-v1", "usage"),
        (b'{"type":"assistant","message":{"role":"assistant","content":[],"provider":"openai","model":"gpt-5","usage":{}}}\n', "pi-subagents-output-v1", "usage"),
        (b'{"type":"tool_execution_start","toolCallId":"1","toolName":"Read","args":{}}\n', "pi-json-events-v3", "lowercase"),
        (b'{"type":"tool_execution_start","toolCallId":"1","toolName":"read","args":{}}\n', "pi-json-events-v3", "matching tool_execution_end"),
    ],
)
def test_invalid_or_incomplete_transcripts_fail_closed(
    tmp_path: Path, content: bytes, source_format: str, error: str
) -> None:
    path = tmp_path / "invalid.jsonl"
    path.write_bytes(content)

    with pytest.raises(TranscriptMetricsError, match=error):
        parse_transcript(path, source_format=source_format)  # type: ignore[arg-type]


def test_non_numeric_or_negative_usage_fails_closed(jsonl_factory: Any) -> None:
    for invalid_usage in (
        _usage(input="1"),
        _usage(output=-1),
        _usage(cost={"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "total": -0.1}),
    ):
        path = jsonl_factory(
            [{"type": "message_end", "message": _assistant_message(usage=invalid_usage)}],
            name=f"invalid-{len(str(invalid_usage))}.jsonl",
        )
        with pytest.raises(TranscriptMetricsError, match="usage"):
            parse_transcript(path, source_format="pi-json-events-v3")


def test_parser_splits_only_on_lf_and_accepts_crlf(tmp_path: Path) -> None:
    record = json.dumps(
        {"type": "message_end", "message": _assistant_message()},
        separators=(",", ":"),
    ).encode()
    crlf_path = tmp_path / "crlf.jsonl"
    crlf_path.write_bytes(record + b"\r\n")
    lone_cr_path = tmp_path / "lone-cr.jsonl"
    lone_cr_path.write_bytes(record + b"\r" + record + b"\n")
    final_cr_path = tmp_path / "final-cr.jsonl"
    final_cr_path.write_bytes(record + b"\r")

    assert parse_transcript(
        crlf_path, source_format="pi-json-events-v3"
    )["assistant_turns"] == 1
    for invalid_path in (lone_cr_path, final_cr_path):
        with pytest.raises(TranscriptMetricsError, match="line 1"):
            parse_transcript(invalid_path, source_format="pi-json-events-v3")


def test_invalid_utf8_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "invalid-utf8.jsonl"
    path.write_bytes(b"\xff\n")

    with pytest.raises(TranscriptMetricsError, match="UTF-8"):
        parse_transcript(path, source_format="pi-json-events-v3")


def test_unknown_source_format_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "empty.jsonl"
    path.write_text("", encoding="utf-8")

    with pytest.raises(TranscriptMetricsError, match="source format"):
        parse_transcript(path, source_format="unknown")  # type: ignore[arg-type]


def test_cli_output_is_deterministic_and_ends_with_one_lf(
    skill_root: Path, tmp_path: Path
) -> None:
    output = tmp_path / "metrics.json"
    command = [
        sys.executable,
        "-m",
        "scripts.transcript_metrics",
        "--format",
        "pi-subagents-output-v1",
        "--input",
        os.fspath(TRANSCRIPT_FIXTURES / "pi-subagents-output.jsonl"),
        "--output",
        os.fspath(output),
    ]

    first = subprocess.run(command, cwd=skill_root, capture_output=True, check=False)
    first_bytes = output.read_bytes()
    second = subprocess.run(command, cwd=skill_root, capture_output=True, check=False)

    assert first.returncode == 0
    assert second.returncode == 0
    assert first.stderr == b""
    assert second.stderr == b""
    assert output.read_bytes() == first_bytes
    assert first_bytes.endswith(b"\n")
    assert not first_bytes.endswith(b"\n\n")
    assert json.loads(first_bytes)["schema_version"] == "pi-skill-creator.transcript-metrics/v1"


def test_cli_contract_failure_writes_no_output(skill_root: Path, tmp_path: Path) -> None:
    invalid = tmp_path / "invalid.jsonl"
    invalid.write_text("not-json\n", encoding="utf-8")
    output = tmp_path / "metrics.json"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.transcript_metrics",
            "--format",
            "pi-json-events-v3",
            "--input",
            os.fspath(invalid),
            "--output",
            os.fspath(output),
        ],
        cwd=skill_root,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 2
    assert result.stdout == b""
    assert 0 < len(result.stderr) <= 2048
    assert not output.exists()


def test_cli_filesystem_failure_exits_one(skill_root: Path, tmp_path: Path) -> None:
    output = tmp_path / "metrics.json"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.transcript_metrics",
            "--format",
            "pi-json-events-v3",
            "--input",
            os.fspath(tmp_path / "missing.jsonl"),
            "--output",
            os.fspath(output),
        ],
        cwd=skill_root,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert result.stdout == b""
    assert 0 < len(result.stderr) <= 2048
    assert not output.exists()


@pytest.mark.contract
def test_workflow_children_have_no_transcript_or_top_level_lifecycle_events(
    pi_subagents_checkout: Path,
) -> None:
    source_root = pi_subagents_checkout / "src"
    worker_source = (source_root / "workflow/worker-source.ts").read_text(encoding="utf-8")
    runtime_source = (source_root / "workflow/runtime.ts").read_text(encoding="utf-8")
    host_source = (source_root / "workflow/host.ts").read_text(encoding="utf-8")
    index_source = (source_root / "index.ts").read_text(encoding="utf-8")
    manager_source = (source_root / "agent-manager.ts").read_text(encoding="utf-8")

    assert "if (schema === undefined) return result;" in worker_source
    assert "return realmParse(result);" in worker_source

    spawn_result = runtime_source.split(
        "export interface WorkflowSpawnResult", 1
    )[1].split("export interface WorkflowGateResult", 1)[0]
    assert "text?: string;" in spawn_result
    assert "outputFile" not in spawn_result
    assert "transcript" not in spawn_result.lower()

    host_result = host_source.split("function toSpawnResult", 1)[1].split(
        "const GATE_SHELL", 1
    )[0]
    assert 'text: record.structuredJson ?? record.result ?? ""' in host_result
    assert "outputFile" not in host_result
    assert "transcript" not in host_result.lower()

    assert manager_source.count(
        "return record.parentAgentId === undefined && record.workflowId === undefined;"
    ) == 1
    for event_name in (
        "subagents:started",
        "subagents:completed",
        "subagents:failed",
        "subagents:compacted",
    ):
        event_offset = index_source.index(f'pi.events.emit("{event_name}"')
        guard_offset = index_source.rfind(
            "if (!isTopLevelAgent(record)) return;", 0, event_offset
        )
        assert guard_offset >= 0
        assert event_offset - guard_offset < 800

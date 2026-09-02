#!/usr/bin/env python3
"""Validate and aggregate one opin-skill-creator campaign iteration."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Never, cast

TREATMENT = "with_skill"
CONTROL = "without_skill"
CONFIGURATIONS = (TREATMENT, CONTROL)
_ENVIRONMENT_PROFILES = {"in-situ", "hermetic-core", "declared-dependencies"}
_TRANSCRIPT_FORMATS = {"pi-subagents-output-v1", "pi-json-events-v3"}
_IDENTIFIER = re.compile(r"[a-z0-9][a-z0-9-]{0,63}\Z")
_ITERATION = re.compile(r"iteration-[1-9][0-9]*\Z")
_RUN_DIRECTORY = re.compile(r"run-([0-9]+)\Z")
_REVISION = re.compile(r"[0-9a-f]{40}\Z")
_TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\Z")
_TOOL_NAME = re.compile(r"[a-z][a-z0-9_-]*\Z")
_MODEL = re.compile(r"[^\s/]+/[^\s]+\Z")
_USAGE_COUNTS = ("input", "output", "cache_read", "cache_write", "reasoning", "total_tokens")
_KNOWN_ITERATION_FILES = {"benchmark.json", "benchmark.md", "feedback.json", "viewer.pid"}


class AggregationError(ValueError):
    """Raised when campaign records cannot support a benchmark claim."""


@dataclass(frozen=True)
class RunRecord:
    eval_id: int
    eval_name: str
    configuration: str
    run_number: int
    environment_profile: str
    requested_model: str
    effective_model: str
    requested_thinking: str
    effective_thinking: str
    pass_rate: float
    passed: int
    failed: int
    total: int
    time_seconds: float
    tool_calls: dict[str, int]
    total_tool_calls: int
    tool_errors: int
    usage: dict[str, int | float]
    transcript_chars: int
    expectations: list[dict[str, Any]]
    claims: list[Any]
    notes: list[str]

    def to_json(self) -> dict[str, Any]:
        return {
            "eval_id": self.eval_id,
            "eval_name": self.eval_name,
            "configuration": self.configuration,
            "run_number": self.run_number,
            "environment_profile": self.environment_profile,
            "requested_model": self.requested_model,
            "effective_model": self.effective_model,
            "requested_thinking": self.requested_thinking,
            "effective_thinking": self.effective_thinking,
            "result": {
                "pass_rate": self.pass_rate,
                "passed": self.passed,
                "failed": self.failed,
                "total": self.total,
                "time_seconds": self.time_seconds,
                "tool_calls": self.tool_calls,
                "total_tool_calls": self.total_tool_calls,
                "tool_errors": self.tool_errors,
                "usage": self.usage,
                "transcript_chars": self.transcript_chars,
            },
            "expectations": self.expectations,
            "claims": self.claims,
            "notes": self.notes,
        }


def _reject_constant(value: str) -> Never:
    raise AggregationError(f"non-standard JSON constant {value}")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise AggregationError(f'duplicate JSON key "{key}"')
        result[key] = value
    return result


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
    except UnicodeDecodeError as error:
        raise AggregationError(f"{path} is not strict UTF-8: {error}") from error
    except json.JSONDecodeError as error:
        raise AggregationError(f"{path} is malformed JSON: {error}") from error
    return _object(value, path.as_posix())


def _object(value: Any, location: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise AggregationError(f"{location} must be a JSON object")
    return cast(dict[str, Any], value)


def _array(value: Any, location: str) -> list[Any]:
    if not isinstance(value, list):
        raise AggregationError(f"{location} must be an array")
    return cast(list[Any], value)


def _string(value: Any, location: str, *, allow_placeholder: bool = False) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AggregationError(f"{location} must be a non-empty string")
    stripped = value.strip()
    if not allow_placeholder and stripped.startswith("<") and stripped.endswith(">"):
        raise AggregationError(f"{location} must not contain placeholder data")
    return value


def _model(value: Any, location: str) -> str:
    model = _string(value, location)
    if _MODEL.fullmatch(model) is None:
        raise AggregationError(f"{location} must be a concrete provider/model identifier")
    return model


def _identifier(value: Any, location: str) -> str:
    text = _string(value, location)
    if _IDENTIFIER.fullmatch(text) is None:
        raise AggregationError(f"{location} must match {_IDENTIFIER.pattern}")
    return text


def _integer(value: Any, location: str, *, positive: bool = False) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise AggregationError(f"{location} must be an integer")
    if value < (1 if positive else 0):
        qualifier = "positive" if positive else "non-negative"
        raise AggregationError(f"{location} must be a {qualifier} integer")
    return value


def _number(value: Any, location: str, *, maximum: float | None = None) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise AggregationError(f"{location} must be a number")
    number = float(value)
    if not math.isfinite(number) or number < 0 or (maximum is not None and number > maximum):
        raise AggregationError(f"{location} is outside its allowed numeric range")
    return number


def _schema(record: dict[str, Any], expected: str, location: str) -> None:
    if record.get("schema_version") != expected:
        raise AggregationError(f"{location}.schema_version must be {expected}")


def _absolute_path(value: Any, location: str) -> str:
    text = _string(value, location)
    if not Path(text).is_absolute():
        raise AggregationError(f"{location} must be an absolute path")
    return text


def _relative_file(value: Any, expected: str, location: str) -> str:
    text = _string(value, location)
    path = Path(text)
    if path.is_absolute() or path.parts != (expected,):
        raise AggregationError(f"{location} must be the run-relative path {expected}")
    return text


def _validate_campaign(iteration_dir: Path) -> dict[str, Any]:
    if not iteration_dir.is_dir():
        raise AggregationError(f"iteration directory not found: {iteration_dir}")
    if _ITERATION.fullmatch(iteration_dir.name) is None:
        raise AggregationError("iteration directory name must match iteration-N")
    campaign_dir = iteration_dir.parent
    campaign = _read_json(campaign_dir / "campaign.json")
    _schema(campaign, "opin.campaign/v1", "campaign.json")

    campaign_id = _identifier(campaign.get("campaign_id"), "campaign.json.campaign_id")
    if campaign_dir.name != f"campaign-{campaign_id}":
        raise AggregationError("campaign directory name does not match campaign_id")
    created_at = _string(campaign.get("created_at"), "campaign.json.created_at")
    if _TIMESTAMP.fullmatch(created_at) is None:
        raise AggregationError("campaign.json.created_at must be an RFC 3339 UTC timestamp")
    try:
        datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as error:
        raise AggregationError(
            "campaign.json.created_at must be a valid RFC 3339 UTC timestamp"
        ) from error
    for field in ("repository_revision", "pi_revision", "pi_subagents_revision"):
        revision = _string(campaign.get(field), f"campaign.json.{field}")
        if _REVISION.fullmatch(revision) is None:
            raise AggregationError(f"campaign.json.{field} must be a lowercase 40-hex revision")
    skill_name = _identifier(campaign.get("skill_name"), "campaign.json.skill_name")
    if campaign_dir.parent.name != skill_name:
        raise AggregationError("campaign skill directory does not match skill_name")
    _absolute_path(campaign.get("skill_path"), "campaign.json.skill_path")
    _absolute_path(campaign.get("evaluation_cwd"), "campaign.json.evaluation_cwd")

    profile = _string(campaign.get("environment_profile"), "campaign.json.environment_profile")
    if profile not in _ENVIRONMENT_PROFILES:
        raise AggregationError("campaign.json.environment_profile is unsupported")
    extensions = _array(campaign.get("declared_extensions"), "campaign.json.declared_extensions")
    for index, extension in enumerate(extensions):
        _absolute_path(extension, f"campaign.json.declared_extensions[{index}]")
    if campaign.get("treatment") != TREATMENT or campaign.get("control") != CONTROL:
        raise AggregationError(
            f"campaign roles must use treatment={TREATMENT} and control={CONTROL}"
        )
    _integer(campaign.get("repetitions"), "campaign.json.repetitions", positive=True)

    roles = _object(campaign.get("roles"), "campaign.json.roles")
    executor = _object(roles.get("executor"), "campaign.json.roles.executor")
    _model(executor.get("requested_model"), "campaign.json.roles.executor.requested_model")
    _string(
        executor.get("requested_thinking"),
        "campaign.json.roles.executor.requested_thinking",
    )
    partitions = _object(campaign.get("partitions"), "campaign.json.partitions")
    _integer(partitions.get("seed"), "campaign.json.partitions.seed")
    for key, expected in (
        ("train", "trigger/train.json"),
        ("validation", "trigger/validation.json"),
        ("final_test", "trigger/final-test.json"),
    ):
        if partitions.get(key) != expected:
            raise AggregationError(f"campaign.json.partitions.{key} must be {expected}")
    return campaign


def _validate_eval_metadata(path: Path, *, directory_name: str) -> tuple[int, str]:
    metadata = _read_json(path)
    eval_id = _integer(metadata.get("eval_id"), f"{path}.eval_id", positive=True)
    eval_name = _identifier(metadata.get("eval_name"), f"{path}.eval_name")
    if eval_name != directory_name:
        raise AggregationError(f"{path}.eval_name does not match its directory")
    _string(metadata.get("prompt"), f"{path}.prompt", allow_placeholder=True)
    expectations = _array(metadata.get("expectations"), f"{path}.expectations")
    if not expectations:
        raise AggregationError(f"{path}.expectations must not be empty")
    for index, expectation in enumerate(expectations):
        _string(expectation, f"{path}.expectations[{index}]", allow_placeholder=True)
    return eval_id, eval_name


def _validate_run_metadata(
    path: Path,
    *,
    campaign: dict[str, Any],
    eval_id: int,
    eval_name: str,
    configuration: str,
    run_number: int,
) -> dict[str, Any]:
    run = _read_json(path)
    _schema(run, "opin.run/v1", path.as_posix())
    expected_values: dict[str, object] = {
        "campaign_id": campaign["campaign_id"],
        "eval_id": eval_id,
        "eval_name": eval_name,
        "configuration": configuration,
        "run_number": run_number,
        "environment_profile": campaign["environment_profile"],
        "status": "completed",
        "role": "executor",
        "transcript_path": "transcript.jsonl",
        "metrics_path": "transcript-metrics.json",
        "outputs_dir": "outputs",
    }
    for field, expected in expected_values.items():
        if run.get(field) != expected:
            if field == "environment_profile":
                raise AggregationError(f"{path} environment profile does not match campaign")
            raise AggregationError(f"{path}.{field} must be {expected!r}")

    role = cast(dict[str, Any], cast(dict[str, Any], campaign["roles"])["executor"])
    requested_model = _model(run.get("requested_model"), f"{path}.requested_model")
    if requested_model != role["requested_model"]:
        raise AggregationError(
            f"{path}.requested_model does not match the campaign executor role"
        )
    requested_thinking = _string(
        run.get("requested_thinking"), f"{path}.requested_thinking"
    )
    if requested_thinking != role["requested_thinking"]:
        raise AggregationError(
            f"{path}.requested_thinking does not match the campaign executor role"
        )
    _model(run.get("effective_model"), f"{path}.effective_model")
    _string(run.get("effective_thinking"), f"{path}.effective_thinking")
    transcript_format = _string(run.get("transcript_format"), f"{path}.transcript_format")
    if transcript_format not in _TRANSCRIPT_FORMATS:
        raise AggregationError(f"{path}.transcript_format is unsupported")
    _relative_file(run.get("transcript_path"), "transcript.jsonl", f"{path}.transcript_path")
    _relative_file(
        run.get("metrics_path"), "transcript-metrics.json", f"{path}.metrics_path"
    )
    _relative_file(run.get("outputs_dir"), "outputs", f"{path}.outputs_dir")
    return run


def _validate_metrics(path: Path, run: dict[str, Any]) -> dict[str, Any]:
    metrics = _read_json(path)
    _schema(metrics, "opin.transcript-metrics/v1", path.as_posix())
    if metrics.get("source_format") != run["transcript_format"]:
        raise AggregationError(f"{path}.source_format does not match run.json")

    raw_tool_calls = _object(metrics.get("tool_calls"), f"{path}.tool_calls")
    tool_calls: dict[str, int] = {}
    for name, count in raw_tool_calls.items():
        if _TOOL_NAME.fullmatch(name) is None:
            raise AggregationError(f"{path}.tool_calls has an invalid tool name")
        tool_calls[name] = _integer(count, f"{path}.tool_calls.{name}")
    total_tool_calls = _integer(metrics.get("total_tool_calls"), f"{path}.total_tool_calls")
    if total_tool_calls != sum(tool_calls.values()):
        raise AggregationError(f"{path}.total_tool_calls does not equal the tool histogram")
    _integer(metrics.get("assistant_turns"), f"{path}.assistant_turns", positive=True)
    tool_errors = _integer(metrics.get("tool_errors"), f"{path}.tool_errors")
    if tool_errors > total_tool_calls:
        raise AggregationError(f"{path}.tool_errors exceeds total_tool_calls")

    raw_usage = _object(metrics.get("usage"), f"{path}.usage")
    usage: dict[str, int | float] = {}
    for field in _USAGE_COUNTS:
        usage[field] = _integer(raw_usage.get(field), f"{path}.usage.{field}")
    usage["cost_usd"] = _number(raw_usage.get("cost_usd"), f"{path}.usage.cost_usd")
    effective_models = _array(metrics.get("effective_models"), f"{path}.effective_models")
    if effective_models != [run["effective_model"]]:
        raise AggregationError(f"{path} effective model does not match run.json")
    transcript_chars = _integer(metrics.get("transcript_chars"), f"{path}.transcript_chars")

    return {
        "tool_calls": tool_calls,
        "total_tool_calls": total_tool_calls,
        "tool_errors": tool_errors,
        "usage": usage,
        "transcript_chars": transcript_chars,
    }


def _validate_grading(path: Path) -> dict[str, Any]:
    grading = _read_json(path)
    _schema(grading, "opin.grading/v1", path.as_posix())
    raw_expectations = _array(grading.get("expectations"), f"{path}.expectations")
    if not raw_expectations:
        raise AggregationError(f"{path}.expectations must not be empty")
    expectations: list[dict[str, Any]] = []
    for index, raw_expectation in enumerate(raw_expectations):
        location = f"{path}.expectations[{index}]"
        expectation = _object(raw_expectation, location)
        text = _string(expectation.get("text"), f"{location}.text", allow_placeholder=True)
        passed = expectation.get("passed")
        if not isinstance(passed, bool):
            raise AggregationError(f"{location}.passed must be boolean")
        evidence = _string(
            expectation.get("evidence"), f"{location}.evidence", allow_placeholder=True
        )
        expectations.append({"text": text, "passed": passed, "evidence": evidence})

    summary = _object(grading.get("summary"), f"{path}.summary")
    passed_count = _integer(summary.get("passed"), f"{path}.summary.passed")
    failed_count = _integer(summary.get("failed"), f"{path}.summary.failed")
    total = _integer(summary.get("total"), f"{path}.summary.total", positive=True)
    pass_rate = _number(summary.get("pass_rate"), f"{path}.summary.pass_rate", maximum=1.0)
    observed_passed = sum(1 for expectation in expectations if expectation["passed"])
    if (
        passed_count != observed_passed
        or failed_count != len(expectations) - observed_passed
        or total != len(expectations)
        or not math.isclose(pass_rate, passed_count / total, abs_tol=0.005)
    ):
        raise AggregationError(f"{path}.summary does not match expectations")

    claims = _array(grading.get("claims", []), f"{path}.claims")
    notes_object = _object(
        grading.get("user_notes_summary", {}), f"{path}.user_notes_summary"
    )
    notes: list[str] = []
    for field in ("uncertainties", "needs_review", "workarounds"):
        raw_notes = _array(notes_object.get(field, []), f"{path}.user_notes_summary.{field}")
        for index, raw_note in enumerate(raw_notes):
            notes.append(
                _string(
                    raw_note,
                    f"{path}.user_notes_summary.{field}[{index}]",
                    allow_placeholder=True,
                )
            )
    return {
        "expectations": expectations,
        "passed": passed_count,
        "failed": failed_count,
        "total": total,
        "pass_rate": pass_rate,
        "claims": claims,
        "notes": notes,
    }


def _validate_timing(path: Path) -> float:
    timing = _read_json(path)
    return _number(timing.get("total_duration_seconds"), f"{path}.total_duration_seconds")


def _load_run(
    run_dir: Path,
    *,
    campaign: dict[str, Any],
    eval_id: int,
    eval_name: str,
    configuration: str,
    run_number: int,
) -> RunRecord:
    run = _validate_run_metadata(
        run_dir / "run.json",
        campaign=campaign,
        eval_id=eval_id,
        eval_name=eval_name,
        configuration=configuration,
        run_number=run_number,
    )
    if not (run_dir / "outputs").is_dir():
        raise AggregationError(f"{run_dir}/outputs directory is missing")
    if not (run_dir / "transcript.jsonl").is_file():
        raise AggregationError(f"{run_dir}/transcript.jsonl is missing")
    metrics = _validate_metrics(run_dir / "transcript-metrics.json", run)
    grading = _validate_grading(run_dir / "grading.json")
    time_seconds = _validate_timing(run_dir / "timing.json")
    return RunRecord(
        eval_id=eval_id,
        eval_name=eval_name,
        configuration=configuration,
        run_number=run_number,
        environment_profile=cast(str, run["environment_profile"]),
        requested_model=cast(str, run["requested_model"]),
        effective_model=cast(str, run["effective_model"]),
        requested_thinking=cast(str, run["requested_thinking"]),
        effective_thinking=cast(str, run["effective_thinking"]),
        pass_rate=cast(float, grading["pass_rate"]),
        passed=cast(int, grading["passed"]),
        failed=cast(int, grading["failed"]),
        total=cast(int, grading["total"]),
        time_seconds=time_seconds,
        tool_calls=cast(dict[str, int], metrics["tool_calls"]),
        total_tool_calls=cast(int, metrics["total_tool_calls"]),
        tool_errors=cast(int, metrics["tool_errors"]),
        usage=cast(dict[str, int | float], metrics["usage"]),
        transcript_chars=cast(int, metrics["transcript_chars"]),
        expectations=cast(list[dict[str, Any]], grading["expectations"]),
        claims=cast(list[Any], grading["claims"]),
        notes=cast(list[str], grading["notes"]),
    )


def discover_runs(iteration_dir: Path) -> tuple[dict[str, Any], list[RunRecord]]:
    """Validate the complete iteration and return its campaign plus run records."""
    campaign = _validate_campaign(iteration_dir)
    entries = list(iteration_dir.iterdir())
    eval_dirs = sorted(entry for entry in entries if entry.is_dir())
    unexpected_files = sorted(
        entry.name
        for entry in entries
        if not entry.is_dir() and entry.name not in _KNOWN_ITERATION_FILES
    )
    if unexpected_files:
        raise AggregationError(
            "unexpected files in iteration directory: " + ", ".join(unexpected_files)
        )
    if not eval_dirs:
        raise AggregationError(f"no eval directories found in {iteration_dir}")

    repetitions = _integer(campaign["repetitions"], "campaign.json.repetitions", positive=True)
    records: list[RunRecord] = []
    eval_ids: set[int] = set()
    for eval_dir in eval_dirs:
        if _IDENTIFIER.fullmatch(eval_dir.name) is None:
            raise AggregationError(f"invalid eval directory name: {eval_dir.name}")
        eval_id, eval_name = _validate_eval_metadata(
            eval_dir / "eval_metadata.json", directory_name=eval_dir.name
        )
        if eval_id in eval_ids:
            raise AggregationError(f"duplicate eval_id {eval_id}")
        eval_ids.add(eval_id)

        child_dirs = {child.name for child in eval_dir.iterdir() if child.is_dir()}
        unexpected = sorted(child_dirs - set(CONFIGURATIONS))
        if unexpected:
            raise AggregationError(
                f"unexpected configuration in {eval_dir}: " + ", ".join(unexpected)
            )
        missing = sorted(set(CONFIGURATIONS) - child_dirs)
        if missing:
            raise AggregationError(f"missing expected arm in {eval_dir}: " + ", ".join(missing))

        for configuration in CONFIGURATIONS:
            configuration_dir = eval_dir / configuration
            by_number: dict[int, Path] = {}
            for run_dir in sorted(child for child in configuration_dir.iterdir() if child.is_dir()):
                match = _RUN_DIRECTORY.fullmatch(run_dir.name)
                if match is None:
                    raise AggregationError(f"unexpected run directory: {run_dir}")
                run_number = int(match.group(1))
                if run_dir.name != f"run-{run_number}":
                    raise AggregationError(
                        f"duplicate run number or non-canonical run directory: {run_dir}"
                    )
                if run_number in by_number:
                    raise AggregationError(
                        f"duplicate run number {run_number} in {configuration_dir}"
                    )
                by_number[run_number] = run_dir
            expected_numbers = set(range(1, repetitions + 1))
            missing_numbers = sorted(expected_numbers - set(by_number))
            unexpected_numbers = sorted(set(by_number) - expected_numbers)
            if missing_numbers:
                raise AggregationError(
                    f"missing run repetitions in {configuration_dir}: {missing_numbers}"
                )
            if unexpected_numbers:
                raise AggregationError(
                    f"unexpected run repetitions in {configuration_dir}: {unexpected_numbers}"
                )
            for run_number in sorted(by_number):
                records.append(
                    _load_run(
                        by_number[run_number],
                        campaign=campaign,
                        eval_id=eval_id,
                        eval_name=eval_name,
                        configuration=configuration,
                        run_number=run_number,
                    )
                )

    if not records:
        raise AggregationError("campaign contains zero runs")
    profiles = {record.environment_profile for record in records}
    if profiles != {campaign["environment_profile"]}:
        raise AggregationError("mixed environment profiles cannot be aggregated")
    effective_models = {record.effective_model for record in records}
    if len(effective_models) != 1:
        raise AggregationError("mixed effective models cannot be aggregated")
    effective_thinking = {record.effective_thinking for record in records}
    if len(effective_thinking) != 1:
        raise AggregationError("mixed effective thinking levels cannot be aggregated")
    return campaign, records


def calculate_stats(values: list[int | float]) -> dict[str, float]:
    """Return deterministic sample statistics for one non-empty metric series."""
    if not values:
        raise AggregationError("cannot calculate statistics for an empty series")
    numeric = [float(value) for value in values]
    mean = sum(numeric) / len(numeric)
    variance = (
        sum((value - mean) ** 2 for value in numeric) / (len(numeric) - 1)
        if len(numeric) > 1
        else 0.0
    )
    return {
        "mean": round(mean, 4),
        "stddev": round(math.sqrt(variance), 4),
        "min": round(min(numeric), 4),
        "max": round(max(numeric), 4),
    }


def _configuration_summary(records: list[RunRecord]) -> dict[str, Any]:
    usage = {
        field: calculate_stats([record.usage[field] for record in records])
        for field in (*_USAGE_COUNTS, "cost_usd")
    }
    return {
        "pass_rate": calculate_stats([record.pass_rate for record in records]),
        "time_seconds": calculate_stats([record.time_seconds for record in records]),
        "total_tool_calls": calculate_stats(
            [record.total_tool_calls for record in records]
        ),
        "tool_errors": calculate_stats([record.tool_errors for record in records]),
        "transcript_chars": calculate_stats(
            [record.transcript_chars for record in records]
        ),
        "usage": usage,
    }


def _delta(treatment: dict[str, Any], control: dict[str, Any]) -> dict[str, Any]:
    def difference(field: str, decimals: int) -> str:
        treatment_stat = cast(dict[str, float], treatment[field])
        control_stat = cast(dict[str, float], control[field])
        return f"{treatment_stat['mean'] - control_stat['mean']:+.{decimals}f}"

    treatment_usage = cast(dict[str, dict[str, float]], treatment["usage"])
    control_usage = cast(dict[str, dict[str, float]], control["usage"])
    usage = {
        field: f"{treatment_usage[field]['mean'] - control_usage[field]['mean']:+.{4 if field == 'cost_usd' else 1}f}"
        for field in (*_USAGE_COUNTS, "cost_usd")
    }
    return {
        "pass_rate": difference("pass_rate", 2),
        "time_seconds": difference("time_seconds", 1),
        "total_tool_calls": difference("total_tool_calls", 1),
        "tool_errors": difference("tool_errors", 1),
        "transcript_chars": difference("transcript_chars", 0),
        "usage": usage,
    }


def aggregate_results(records: list[RunRecord]) -> dict[str, Any]:
    """Aggregate validated records with a fixed treatment-minus-control direction."""
    grouped = {
        configuration: [
            record for record in records if record.configuration == configuration
        ]
        for configuration in CONFIGURATIONS
    }
    if any(not group for group in grouped.values()):
        raise AggregationError("both treatment and control must contain runs")
    treatment = _configuration_summary(grouped[TREATMENT])
    control = _configuration_summary(grouped[CONTROL])
    return {
        TREATMENT: treatment,
        CONTROL: control,
        "delta": _delta(treatment, control),
    }


def generate_benchmark(iteration_dir: Path) -> dict[str, Any]:
    """Return one validated benchmark object without writing any artifacts."""
    campaign, records = discover_runs(iteration_dir)
    effective_model = records[0].effective_model
    effective_thinking = records[0].effective_thinking
    eval_ids = sorted({record.eval_id for record in records})
    repetitions = len(
        {
            record.run_number
            for record in records
            if record.eval_id == eval_ids[0] and record.configuration == TREATMENT
        }
    )
    metadata = {
        "campaign_id": campaign["campaign_id"],
        "created_at": campaign["created_at"],
        "repository_revision": campaign["repository_revision"],
        "pi_revision": campaign["pi_revision"],
        "pi_subagents_revision": campaign["pi_subagents_revision"],
        "skill_name": campaign["skill_name"],
        "skill_path": campaign["skill_path"],
        "evaluation_cwd": campaign["evaluation_cwd"],
        "environment_profile": campaign["environment_profile"],
        "treatment": TREATMENT,
        "control": CONTROL,
        "executor_model": effective_model,
        "executor_thinking": effective_thinking,
        "requested_executor_model": records[0].requested_model,
        "requested_executor_thinking": records[0].requested_thinking,
        "timestamp": campaign["created_at"],
        "evals_run": eval_ids,
        "runs_per_configuration": repetitions,
    }
    return {
        "schema_version": "opin.benchmark/v1",
        "metadata": metadata,
        "runs": [record.to_json() for record in records],
        "run_summary": aggregate_results(records),
        "notes": [],
    }


def generate_markdown(benchmark: dict[str, Any]) -> str:
    """Render the validated benchmark summary used by benchmark.json."""
    metadata = cast(dict[str, Any], benchmark["metadata"])
    summary = cast(dict[str, Any], benchmark["run_summary"])
    treatment = cast(dict[str, Any], summary[TREATMENT])
    control = cast(dict[str, Any], summary[CONTROL])
    delta = cast(dict[str, Any], summary["delta"])
    treatment_pass = cast(dict[str, float], treatment["pass_rate"])
    control_pass = cast(dict[str, float], control["pass_rate"])
    treatment_usage = cast(dict[str, dict[str, float]], treatment["usage"])
    control_usage = cast(dict[str, dict[str, float]], control["usage"])
    delta_usage = cast(dict[str, str], delta["usage"])
    lines = [
        f"# Skill Benchmark: {metadata['skill_name']}",
        "",
        f"**Campaign**: {metadata['campaign_id']}",
        f"**Created**: {metadata['created_at']}",
        f"**Environment profile**: {metadata['environment_profile']}",
        f"**Effective executor**: {metadata['executor_model']} ({metadata['executor_thinking']})",
        f"**Evals**: {', '.join(map(str, metadata['evals_run']))} ({metadata['runs_per_configuration']} runs each per configuration)",
        "",
        "## Summary",
        "",
        "| Metric | With Skill | Without Skill | Delta |",
        "|---|---:|---:|---:|",
        f"| Pass Rate | {treatment_pass['mean'] * 100:.0f}% | {control_pass['mean'] * 100:.0f}% | {delta['pass_rate']} |",
        f"| Provider Output Tokens | {treatment_usage['output']['mean']:.1f} | {control_usage['output']['mean']:.1f} | {delta_usage['output']} |",
        f"| Transcript Characters | {cast(dict[str, float], treatment['transcript_chars'])['mean']:.0f} | {cast(dict[str, float], control['transcript_chars'])['mean']:.0f} | {delta['transcript_chars']} |",
        "",
    ]
    return "\n".join(lines)


class _ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> Never:
        _print_error(message)
        raise SystemExit(2)


def _print_error(error: object) -> None:
    message = " ".join(str(error).splitlines())
    encoded = f"error: {message}".encode("utf-8", errors="replace")[:2000]
    print(encoded.decode("utf-8", errors="ignore"), file=sys.stderr)


def main() -> int:
    parser = _ArgumentParser(
        description="Validate and aggregate an opin-skill-creator campaign iteration"
    )
    parser.add_argument("iteration_dir", type=Path, help="Path to campaign-*/iteration-N")
    args = parser.parse_args()

    try:
        benchmark = generate_benchmark(args.iteration_dir)
        markdown = generate_markdown(benchmark)
    except AggregationError as error:
        _print_error(error)
        return 2
    except OSError as error:
        _print_error(error)
        return 1

    output_json = args.iteration_dir / "benchmark.json"
    output_markdown = args.iteration_dir / "benchmark.md"
    try:
        output_json.write_text(
            json.dumps(benchmark, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        output_markdown.write_text(markdown, encoding="utf-8", newline="\n")
    except OSError as error:
        _print_error(error)
        return 1
    print(f"Generated: {output_json}")
    print(f"Generated: {output_markdown}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Regression tests for strict campaign benchmark aggregation."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from conftest import PI_REVISION, PI_SUBAGENTS_REVISION, SKILL_ROOT, TEST_ROOT


FIXTURES = TEST_ROOT / "fixtures/aggregation"
CONFIGURATIONS = ("with_skill", "without_skill")
EFFECTIVE_MODEL = "openai/gpt-5-exact"


def _read_case(name: str) -> dict[str, Any]:
    return json.loads((FIXTURES / name / "case.json").read_text(encoding="utf-8"))


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _materialize_case(tmp_path: Path, name: str) -> Path:
    case = _read_case(name)
    campaign_id = "aggregation-fixture"
    skill_name = "example-skill"
    campaign_root = (
        tmp_path
        / "project"
        / ".skill-creator"
        / skill_name
        / f"campaign-{campaign_id}"
    )
    iteration_root = campaign_root / "iteration-2"
    repetitions = int(case.get("repetitions", 1))
    campaign = {
        "schema_version": "opin.campaign/v1",
        "campaign_id": campaign_id,
        "created_at": "2026-09-02T12:00:00Z",
        "repository_revision": "1" * 40,
        "pi_revision": PI_REVISION,
        "pi_subagents_revision": PI_SUBAGENTS_REVISION,
        "skill_name": skill_name,
        "skill_path": os.fspath((tmp_path / "deployment" / skill_name).resolve()),
        "evaluation_cwd": os.fspath((tmp_path / "deployment").resolve()),
        "environment_profile": "declared-dependencies",
        "declared_extensions": [os.fspath((tmp_path / "pi-subagents/src/index.ts").resolve())],
        "treatment": "with_skill",
        "control": "without_skill",
        "repetitions": repetitions,
        "roles": {
            "executor": {
                "requested_model": "openai/gpt-5",
                "requested_thinking": "high",
            }
        },
        "partitions": {
            "seed": 42,
            "train": "trigger/train.json",
            "validation": "trigger/validation.json",
            "final_test": "trigger/final-test.json",
        },
    }
    _write_json(campaign_root / "campaign.json", campaign)

    if not case.get("evals", True):
        iteration_root.mkdir(parents=True)
        return iteration_root

    eval_name = "forked-skill-dispatch"
    eval_root = iteration_root / eval_name
    _write_json(
        eval_root / "eval_metadata.json",
        {
            "eval_id": 7,
            "eval_name": eval_name,
            "prompt": "Use the bundled specialist to inspect the project.",
            "expectations": ["The specialist result is reported."],
        },
    )

    configuration_order = case.get("configuration_order", list(CONFIGURATIONS))
    omitted = {
        (str(item[0]), int(item[1])) for item in case.get("omit_runs", [])
    }
    pass_rates = {"with_skill": 1.0, "without_skill": 0.25}
    for configuration in configuration_order:
        for run_number in range(1, repetitions + 1):
            if (configuration, run_number) in omitted:
                continue
            run_root = eval_root / configuration / f"run-{run_number}"
            (run_root / "outputs").mkdir(parents=True)
            (run_root / "transcript.jsonl").write_text("{}\n", encoding="utf-8")

            environment_profile = "declared-dependencies"
            if case.get("mixed_profile") and configuration == "without_skill":
                environment_profile = "hermetic-core"
            effective_model = EFFECTIVE_MODEL
            if case.get("mixed_model") and configuration == "without_skill":
                effective_model = "openai/gpt-5-other"

            _write_json(
                run_root / "run.json",
                {
                    "schema_version": "opin.run/v1",
                    "campaign_id": campaign_id,
                    "eval_id": 7,
                    "eval_name": eval_name,
                    "configuration": configuration,
                    "run_number": run_number,
                    "environment_profile": environment_profile,
                    "status": "completed",
                    "role": "executor",
                    "requested_model": "openai/gpt-5",
                    "effective_model": effective_model,
                    "requested_thinking": "high",
                    "effective_thinking": "high",
                    "transcript_format": "pi-json-events-v3",
                    "transcript_path": "transcript.jsonl",
                    "metrics_path": "transcript-metrics.json",
                    "outputs_dir": "outputs",
                },
            )
            _write_json(
                run_root / "transcript-metrics.json",
                {
                    "schema_version": "opin.transcript-metrics/v1",
                    "source_format": "pi-json-events-v3",
                    "tool_calls": {"read": 2 if configuration == "with_skill" else 1},
                    "total_tool_calls": 2 if configuration == "with_skill" else 1,
                    "assistant_turns": 1,
                    "tool_errors": 0,
                    "usage": {
                        "input": 100 if configuration == "with_skill" else 80,
                        "output": 20 if configuration == "with_skill" else 15,
                        "cache_read": 10,
                        "cache_write": 0,
                        "reasoning": 5,
                        "total_tokens": 135 if configuration == "with_skill" else 110,
                        "cost_usd": 0.02 if configuration == "with_skill" else 0.01,
                    },
                    "effective_models": [effective_model],
                    "transcript_chars": 1200 if configuration == "with_skill" else 800,
                },
            )
            total = 4
            passed = round(pass_rates[configuration] * total)
            expectations = [
                {
                    "text": f"Expectation {index + 1}",
                    "passed": index < passed,
                    "evidence": "Deterministic fixture evidence.",
                }
                for index in range(total)
            ]
            if case.get("missing_expectations") and configuration == "without_skill":
                expectations = []
            _write_json(
                run_root / "grading.json",
                {
                    "schema_version": "opin.grading/v1",
                    "expectations": expectations,
                    "summary": {
                        "passed": passed,
                        "failed": total - passed,
                        "total": total,
                        "pass_rate": pass_rates[configuration],
                    },
                    "claims": [],
                    "user_notes_summary": {
                        "uncertainties": [],
                        "needs_review": [],
                        "workarounds": [],
                    },
                },
            )
            _write_json(
                run_root / "timing.json",
                {"total_duration_seconds": 10.0},
            )

    unexpected = case.get("unexpected_configuration")
    if unexpected:
        (eval_root / str(unexpected)).mkdir(parents=True)
    return iteration_root


def _run_aggregator(iteration_root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "scripts.aggregate_benchmark", os.fspath(iteration_root)],
        cwd=SKILL_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_documented_workspace_aggregates_treatment_minus_control_with_real_metadata(
    tmp_path: Path,
) -> None:
    iteration_root = _materialize_case(tmp_path, "complete")

    result = _run_aggregator(iteration_root)

    assert result.returncode == 0, result.stderr
    benchmark = json.loads((iteration_root / "benchmark.json").read_text(encoding="utf-8"))
    assert benchmark["schema_version"] == "opin.benchmark/v1"
    assert benchmark["metadata"]["campaign_id"] == "aggregation-fixture"
    assert benchmark["metadata"]["executor_model"] == EFFECTIVE_MODEL
    assert benchmark["metadata"]["executor_thinking"] == "high"
    assert benchmark["metadata"]["runs_per_configuration"] == 1
    assert benchmark["metadata"]["evals_run"] == [7]
    assert benchmark["run_summary"]["delta"]["pass_rate"] == "+0.75"
    assert {run["configuration"] for run in benchmark["runs"]} == set(CONFIGURATIONS)
    assert {run["eval_name"] for run in benchmark["runs"]} == {
        "forked-skill-dispatch"
    }

    treatment = next(
        run for run in benchmark["runs"] if run["configuration"] == "with_skill"
    )
    assert treatment["result"]["transcript_chars"] == 1200
    assert treatment["result"]["usage"]["total_tokens"] == 135
    assert "tokens" not in treatment["result"]
    markdown = (iteration_root / "benchmark.md").read_text(encoding="utf-8")
    assert "| Pass Rate | 100% | 25% | +0.75 |" in markdown
    assert f"**Effective executor**: {EFFECTIVE_MODEL} (high)" in markdown


def test_reversed_creation_order_does_not_reverse_delta(tmp_path: Path) -> None:
    iteration_root = _materialize_case(tmp_path, "reversed-order")

    result = _run_aggregator(iteration_root)

    assert result.returncode == 0, result.stderr
    benchmark = json.loads((iteration_root / "benchmark.json").read_text(encoding="utf-8"))
    assert list(benchmark["run_summary"]) == ["with_skill", "without_skill", "delta"]
    assert benchmark["run_summary"]["delta"]["pass_rate"] == "+0.75"


@pytest.mark.parametrize(
    ("case_name", "message"),
    [
        ("no-data", "no eval directories"),
        ("partial", "missing run"),
        ("mixed-profile", "environment profile"),
        ("mixed-model", "effective model"),
    ],
)
def test_invalid_campaigns_fail_without_writing_artifacts(
    tmp_path: Path, case_name: str, message: str
) -> None:
    iteration_root = _materialize_case(tmp_path, case_name)

    result = _run_aggregator(iteration_root)

    assert result.returncode == 2
    assert message in result.stderr.lower()
    assert not (iteration_root / "benchmark.json").exists()
    assert not (iteration_root / "benchmark.md").exists()


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        ("unexpected_configuration", "unexpected configuration"),
        ("missing_expectations", "expectations"),
        ("missing_effective_model", "effective_model"),
        ("duplicate_run_number", "duplicate run"),
    ],
)
def test_malformed_or_ambiguous_run_data_is_fatal(
    tmp_path: Path, mutation: str, message: str
) -> None:
    iteration_root = _materialize_case(tmp_path, "complete")
    eval_root = iteration_root / "forked-skill-dispatch"
    if mutation == "unexpected_configuration":
        (eval_root / "baseline").mkdir()
    elif mutation == "missing_expectations":
        path = eval_root / "without_skill/run-1/grading.json"
        grading = json.loads(path.read_text(encoding="utf-8"))
        grading.pop("expectations")
        _write_json(path, grading)
    elif mutation == "missing_effective_model":
        path = eval_root / "with_skill/run-1/run.json"
        run = json.loads(path.read_text(encoding="utf-8"))
        run["effective_model"] = "<model-name>"
        _write_json(path, run)
    else:
        source = eval_root / "with_skill/run-1"
        duplicate = eval_root / "with_skill/run-01"
        shutil.copytree(source, duplicate)

    result = _run_aggregator(iteration_root)

    assert result.returncode == 2
    assert message in result.stderr.lower()
    assert not (iteration_root / "benchmark.json").exists()
    assert not (iteration_root / "benchmark.md").exists()


def test_schema_reference_matches_frozen_artifact_contracts(skill_root: Path) -> None:
    schemas = (skill_root / "references/schemas.md").read_text(encoding="utf-8")

    for schema_id in (
        "opin.campaign/v1",
        "opin.run/v1",
        "opin.transcript-metrics/v1",
        "opin.grading/v1",
        "opin.benchmark/v1",
    ):
        assert schema_id in schemas
    assert "campaign-<campaign-id>/iteration-N/benchmark.json" in schemas
    assert "history.json" not in schemas
    assert '"assertions"' not in schemas

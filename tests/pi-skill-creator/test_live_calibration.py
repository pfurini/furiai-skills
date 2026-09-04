"""Replay-only validation for the OSC-14 live smoke campaign."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, cast

import pytest

from conftest import PI_REVISION, PI_SUBAGENTS_REVISION, SKILL_ROOT

pytestmark = pytest.mark.live


def _campaign_dir() -> Path:
    value = os.environ.get("PI_SKILL_CREATOR_CAMPAIGN_DIR")
    assert value, "PI_SKILL_CREATOR_CAMPAIGN_DIR must name the completed smoke campaign"
    campaign_dir = Path(value)
    assert campaign_dir.is_dir(), f"campaign directory does not exist: {campaign_dir}"
    return campaign_dir


def _max_paid_calls() -> int:
    value = os.environ.get("PI_SKILL_CREATOR_MAX_PAID_CALLS")
    assert value, "PI_SKILL_CREATOR_MAX_PAID_CALLS must be set for the smoke replay"
    try:
        maximum = int(value)
    except ValueError:
        pytest.fail("PI_SKILL_CREATOR_MAX_PAID_CALLS must be an integer", pytrace=False)
    assert maximum > 0, "PI_SKILL_CREATOR_MAX_PAID_CALLS must be positive"
    return maximum


def _read_json(path: Path) -> dict[str, Any]:
    assert path.is_file(), f"required campaign record is missing: {path}"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        pytest.fail(f"invalid JSON campaign record {path}: {error}", pytrace=False)
    assert isinstance(value, dict), f"campaign record must be a JSON object: {path}"
    return cast(dict[str, Any], value)


def _run_records(campaign_dir: Path) -> list[Path]:
    records = sorted(campaign_dir.rglob("run.json"))
    assert records, f"campaign has no run.json records: {campaign_dir}"
    return records


def test_smoke_campaign_replays_and_bounds_paid_calls() -> None:
    campaign_dir = _campaign_dir()
    campaign = _read_json(campaign_dir / "campaign.json")
    assert campaign["schema_version"] == "pi-skill-creator.campaign/v1"
    assert campaign["workflow_runtime"] == "pi-subagents"
    assert campaign["pi_revision"] == PI_REVISION
    assert campaign["pi_subagents_revision"] == PI_SUBAGENTS_REVISION
    assert campaign["workflow_runtime_revision"] == PI_SUBAGENTS_REVISION
    assert campaign["environment_profile"] == "hermetic-core"
    assert campaign["repetitions"] in (1, 2)

    iteration_dir = campaign_dir / "iteration-1"
    validation = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.aggregate_benchmark",
            os.fspath(iteration_dir),
            "--validate-only",
        ],
        cwd=SKILL_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert validation.returncode == 0, validation.stdout + validation.stderr

    benchmark = _read_json(iteration_dir / "benchmark.json")
    assert benchmark["metadata"]["workflow_runtime"] == "pi-subagents"

    workflow_result = _read_json(campaign_dir / "workflow-result.json")
    assert workflow_result["valid"] is True
    assert workflow_result["workflow_runtime"] == "pi-subagents"
    assert workflow_result["agent_calls_made"] <= workflow_result["max_agent_calls"]
    assert sum(workflow_result["status_counts"].values()) == workflow_result["expected_runs"]

    paid_calls = (
        workflow_result["agent_calls_made"]
        + len(_run_records(campaign_dir))
        + len(list(campaign_dir.glob("comparisons/*/comparison.json")))
    )
    assert paid_calls <= _max_paid_calls()


def test_smoke_effective_models_match_requested() -> None:
    campaign_dir = _campaign_dir()
    campaign = _read_json(campaign_dir / "campaign.json")
    executor_model = campaign["roles"]["executor"]["requested_model"]
    for path in _run_records(campaign_dir):
        run = _read_json(path)
        assert run["requested_model"] == executor_model
        assert run["effective_model"] == executor_model
        assert isinstance(run["effective_thinking"], str) and run["effective_thinking"].strip()

    workflow_result = _read_json(campaign_dir / "workflow-result.json")
    assert workflow_result["effective_roles"]["grader"]["models"] == [
        "openai-codex/gpt-5.6-sol"
    ]
    comparator_metrics = _read_json(
        campaign_dir / "comparisons/release-note-format/comparator-metrics.json"
    )
    assert comparator_metrics["effective_models"] == ["claude-bridge/claude-opus-5"]


def test_smoke_comparison_is_blind_and_recorded() -> None:
    campaign_dir = _campaign_dir()
    comparison_dir = campaign_dir / "comparisons/release-note-format"
    assignment = _read_json(comparison_dir / "blind-assignment.json")
    assert set(assignment["assignment"]) == {"A", "B"}
    assert sorted(assignment["assignment"].values()) == ["with_skill", "without_skill"]

    for arm in ("A", "B"):
        extracted = assignment["extracted"][arm]
        neutral_path = Path(extracted["path"])
        assert neutral_path.is_file(), f"neutral comparison input is missing: {neutral_path}"
        path_text = neutral_path.as_posix().lower()
        assert "with_skill" not in path_text and "without_skill" not in path_text
        digest = hashlib.sha256(neutral_path.read_bytes()).hexdigest()
        assert digest == extracted["sha256"]

    comparison = _read_json(comparison_dir / "comparison.json")
    assert comparison["winner"] in {"A", "B", "TIE"}
    assert isinstance(comparison["reasoning"], str) and comparison["reasoning"].strip()


def test_smoke_record_is_labelled_and_claims_nothing() -> None:
    review = _read_json(_campaign_dir() / "review-required.json")
    assert review["label"] == "smoke-test"
    assert review["claim_candidates"] == []
    assert review["pin_candidates"] == []
    assert review["call_counts"]["total"] <= review["call_counts"]["max_paid_calls"]

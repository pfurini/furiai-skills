"""Structural contracts for the measured skill-testing doctrine."""

from __future__ import annotations

import re

from conftest import SKILL_ROOT


DOCTRINE_PATH = SKILL_ROOT / "references/testing.md"
SKILL_PATH = SKILL_ROOT / "SKILL.md"


def _section(text: str, heading: str) -> str:
    return text.split(f"## {heading}", 1)[1].split("\n## ", 1)[0]


def test_testing_names_supported_mechanisms_and_profiles() -> None:
    doctrine = DOCTRINE_PATH.read_text(encoding="utf-8")
    fidelity = _section(doctrine, "Environment fidelity")
    loop = _section(doctrine, "The test loop")

    profile_names = re.findall(r"^- \*\*`([^`]+)`\*\*:", fidelity, re.MULTILINE)
    assert profile_names == ["in-situ", "hermetic-core", "declared-dependencies"]
    assert "profile mismatch is fatal" in fidelity.lower()

    for field in (
        "prompt_mode: replace",
        "inherit_context: false",
        "isolated: true",
        "skills: false",
        "isolation: worktree",
    ):
        assert field in fidelity

    assert "Agent" in loop and "known small qualitative set" in loop
    assert "SubagentWorkflow" in loop and "dynamic or staged fan-out" in loop
    assert "explicit user approval" in loop
    assert "parallel writers" in loop and "worktree isolation" in loop
    # The second workflow runtime is named beside the first, with its tool name.
    assert "pi-dynamic-workflows" in loop and "`workflow`" in loop


def test_testing_documents_supported_telemetry_boundaries() -> None:
    doctrine = DOCTRINE_PATH.read_text(encoding="utf-8")
    telemetry = _section(doctrine, "Measured-run evidence")

    for term in (
        "Agent",
        ".output",
        "results and completion notifications",
        "JSONL message snapshots",
        "SubagentWorkflow",
        "top-level lifecycle events",
        "Pi RPC",
        "transcript.jsonl",
        "run.json",
        "transcript-metrics.json",
        "total_tokens",
        "duration_ms",
    ):
        assert term in telemetry

    assert "workflow children do not expose" in telemetry.lower()
    assert "not the only recoverable usage source" in telemetry.lower()
    assert "pi-dynamic-workflows" in telemetry and "`workflow`" in telemetry


def test_testing_uses_campaign_workspace_contract() -> None:
    doctrine = DOCTRINE_PATH.read_text(encoding="utf-8")
    workspace = _section(doctrine, "Campaign workspace")

    for term in (
        ".skill-creator/<skill-name>/campaign-<campaign-id>/",
        "campaign.json",
        "evals.json",
        "iteration-N",
        "<human-readable-eval-name>",
        "with_skill",
        "without_skill",
        "run-N",
        "outputs/",
        "transcript.jsonl",
    ):
        assert term in workspace


def test_testing_removes_unsupported_claims_and_exposes_spine_mechanisms() -> None:
    doctrine = DOCTRINE_PATH.read_text(encoding="utf-8")
    skill = SKILL_PATH.read_text(encoding="utf-8")
    baseline = _section(skill, "Step 2 — Baseline")
    forward_test = _section(skill, "Step 5 — Forward-test")
    benchmark = _section(skill, "Step 7 — Benchmark (optional)")

    assert "cannot be sterilized" not in doctrine
    assert "notification is the only place this data exists" not in doctrine
    assert "clean-slate" not in _section(doctrine, "Environment fidelity").lower()

    assert "Agent" in baseline and "explicit user approval" in baseline
    assert "Agent" in forward_test and "explicit user approval" in forward_test
    assert "SubagentWorkflow" in benchmark
    assert "dynamic or staged fan-out" in benchmark
    assert "pi-dynamic-workflows" in benchmark and "`workflow`" in benchmark

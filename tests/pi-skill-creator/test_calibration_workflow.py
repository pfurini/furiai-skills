"""Contract tests for the two repository-development workflows under `.pi/workflows/`.

Both scripts run through the pinned pi-subagents runtime (the compiled ``runtime.js``)
with a stub host that answers every child from a fixture table and records the gate
commands it is handed. No model call, git command, or gate command runs.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

import pytest

from conftest import (
    PI_DYNAMIC_WORKFLOWS_REVISION,
    PI_REVISION,
    PI_SUBAGENTS_REVISION,
    REPOSITORY_ROOT,
    SKILL_ROOT,
    verify_checkout_revision,
)

pytestmark = pytest.mark.contract

FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures/calibration-workflow"
SMOKE_SKILL = Path(__file__).resolve().parent / "fixtures/smoke/release-note-smoke"
CALIBRATION_WORKFLOW = REPOSITORY_ROOT / ".pi/workflows/pi-skill-creator-calibration.js"
ADOPTION_WORKFLOW = REPOSITORY_ROOT / ".pi/workflows/pi-skill-creator-adoption.js"
PI_CLAUDE_BRIDGE_REVISION = "c1d8b24a57e15bc8acc9d673f2804ab7227978ae"
INTEGRATION_COMMIT = "4e6f8a0b1c2d3e4f5a6b7c8d9e0f3f2a9c1e5b7d"
THREE_FIELD_SEMANTICS = (
    "`tests_skipped` lists intentionally skipped tests only; `bounded_work` lists mandated "
    "exclusions only; `skipped_work` lists required work left incomplete and must be `[]` "
    "on completion."
)
MANIFEST_MODELS = {
    "executor": "openai-codex/gpt-5.6-terra",
    "grader": "openai-codex/gpt-5.6-sol",
    "comparator": "claude-bridge/claude-opus-5",
    "benchmarkAnalyzer": "openai-codex/gpt-5.6-terra",
}
ADOPTION_WAVES = {
    "foundation": "Foundation",
    "contracts": "Contracts",
    "core": "Core",
    "models": "Models",
    "execution": "Execution",
    "doctrine": "Doctrine",
    "runtime-workflow": "Runtime workflow",
    "readme": "README",
}


def _checkout() -> Path:
    value = os.environ.get("PI_SUBAGENTS_CHECKOUT")
    if not value:
        pytest.skip("development workflow tests require PI_SUBAGENTS_CHECKOUT")
    try:
        return verify_checkout_revision(Path(value), PI_SUBAGENTS_REVISION, "pi-subagents checkout")
    except ValueError as error:
        pytest.fail(str(error), pytrace=False)


@pytest.fixture(scope="session")
def development_workflow_runtime(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """The pinned pi-subagents workflow runtime compiled into a per-session temporary directory."""
    checkout = _checkout()
    output_root = tmp_path_factory.mktemp("pi-subagents-dist-calibration")
    compiler = checkout / "node_modules/.bin/tsc"
    if not compiler.is_file():
        pytest.skip("development workflow tests require the pinned checkout dependencies")
    result = subprocess.run(
        [
            os.fspath(compiler),
            "--project",
            os.fspath(checkout / "tsconfig.json"),
            "--outDir",
            os.fspath(output_root),
            "--declaration",
            "false",
        ],
        cwd=checkout,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    (output_root / "node_modules").symlink_to(checkout / "node_modules", target_is_directory=True)
    return output_root / "workflow"


def _args(name: str) -> dict[str, Any]:
    return json.loads((FIXTURE_ROOT / f"{name}-args.json").read_text(encoding="utf-8"))


def _run(
    runtime_root: Path,
    workflow: Path,
    args: dict[str, Any],
    *,
    responses: dict[str, Any] | None = None,
    prefix_responses: dict[str, Any] | None = None,
    null_labels: list[str] | None = None,
    gate_failures: list[str] | None = None,
) -> dict[str, Any]:
    result = subprocess.run(
        ["node", os.fspath(FIXTURE_ROOT / "stub-host-probe.mjs")],
        input=json.dumps(
            {
                "runtimeRoot": os.fspath(runtime_root),
                "source": workflow.read_text(encoding="utf-8"),
                "args": args,
                "responses": responses or {},
                "prefixResponses": prefix_responses or {},
                "nullLabels": null_labels or [],
                "gateFailures": gate_failures or [],
            }
        ),
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def _preflight_response() -> dict[str, Any]:
    return {
        "ok": True,
        "models_resolved": sorted(set(MANIFEST_MODELS.values())),
        "models_unresolved": [],
        "skill_copy_verified": True,
        "bounded_work": [],
        "skipped_work": [],
        "summary": "fixture preflight passed",
    }


def _calibration_response(*, paid_calls_used: int = 10, max_paid_calls: int = 10) -> dict[str, Any]:
    return {
        "order_id": "OSC-14",
        "status": "completed",
        "branch": "osc-14",
        "commit": "1c2d3e4f5a6b7c8d9e0f3f2a9c1e5b7d4e6f8a0b",
        "approval_token_seen": True,
        "workflow_result_valid": True,
        "paid_calls_used": paid_calls_used,
        "max_paid_calls": max_paid_calls,
        "agent_calls_made": 7,
        "max_agent_calls": 7,
        "records": ["workflow-result.json", "review-required.json"],
        "manual_review_required": ["review-required.json"],
        "tests_passed": ["test_live_calibration.py::test_smoke_campaign_replays_and_bounds_paid_calls"],
        "tests_skipped": [],
        "bounded_work": [],
        "skipped_work": [],
        "claims_changed": [],
        "pins_changed": [],
        "summary": "fixture smoke validated",
        "blockers": [],
    }


def _integration_response() -> dict[str, Any]:
    return {
        "status": "completed",
        "commit": INTEGRATION_COMMIT,
        "branches": ["${label}"],
        "tests_passed": ["fixture gate"],
        "bounded_work": [],
        "skipped_work": [],
        "summary": "fixture integration",
    }


def _finalize_responses() -> dict[str, Any]:
    return {
        "OSC-15": {
            "order_id": "OSC-15",
            "status": "completed",
            "branch": "osc-15",
            "commit": "2d3e4f5a6b7c8d9e0f3f2a9c1e5b7d4e6f8a0b1c",
            "red_observed": True,
            "claims_applied": [],
            "claims_removed": [],
            "pins_applied": [],
            "tests_passed": [],
            "tests_skipped": [],
            "bounded_work": [],
            "skipped_work": [],
            "summary": "fixture claim hygiene",
        },
        "OSC-16": {
            "order_id": "OSC-16",
            "status": "completed",
            "branch": "osc-16",
            "commit": "3e4f5a6b7c8d9e0f3f2a9c1e5b7d4e6f8a0b1c2d",
            "f19_absence_verified": True,
            "boundary_violations": [],
            "tests_passed": [],
            "tests_skipped": [],
            "bounded_work": [],
            "skipped_work": [],
            "summary": "fixture distribution",
        },
    }


def _calibration_run(runtime_root: Path, stage: str, args: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    responses = {
        f"preflight:{stage}": _preflight_response(),
        "OSC-14": _calibration_response(),
        **_finalize_responses(),
    }
    responses.update(overrides.pop("responses", {}))
    return _run(
        runtime_root,
        CALIBRATION_WORKFLOW,
        args,
        responses=responses,
        prefix_responses={"integrate:": _integration_response()},
        **overrides,
    )


def _adoption_run(runtime_root: Path, args: dict[str, Any]) -> dict[str, Any]:
    handoff = {
        "order_id": "${label}",
        "status": "completed",
        "branch": "${label}",
        "commit": "5a6b7c8d9e0f3f2a9c1e5b7d4e6f8a0b1c2d3e4f",
        "red_observed": True,
        "tests_passed": ["fixture"],
        "tests_skipped": [],
        "bounded_work": [],
        "skipped_work": [],
        "owned_paths_changed": [],
        "summary": "fixture order",
        "blockers": [],
    }
    return _run(
        runtime_root,
        ADOPTION_WORKFLOW,
        args,
        responses={"preflight": {"ok": True, "summary": "fixture preflight"}},
        prefix_responses={"OSC-": handoff, "integrate:": _integration_response()},
    )


def _failure(run: dict[str, Any]) -> str:
    assert run["status"] in {"failed", "threw"}, run
    return str(run["error"])


def _labels(probe: dict[str, Any]) -> list[str]:
    return [call["label"] for call in probe["calls"]]


def test_calibration_workflow_meta_has_three_stages_and_no_integrate_phase(
    development_workflow_runtime: Path,
) -> None:
    probe = _calibration_run(development_workflow_runtime, "preflight", _args("preflight"))
    assert probe["meta"]["name"] == "pi-skill-creator-calibration"
    assert [phase["title"] for phase in probe["meta"]["phases"]] == [
        "Preflight",
        "Calibrate",
        "Human checkpoint",
        "Distribution",
    ]
    source = CALIBRATION_WORKFLOW.read_text(encoding="utf-8")
    assert "phase: 'Integrate'" not in source
    assert f"'{PI_REVISION}'" in source
    assert f"'{PI_SUBAGENTS_REVISION}'" in source
    assert f"'{PI_DYNAMIC_WORKFLOWS_REVISION}'" in source
    assert f"'{PI_CLAUDE_BRIDGE_REVISION}'" in source
    assert "default-agents.ts" in source and "agent-runner.ts" in source
    # The bridge is loaded through the default agent types; no `isolated` option and no
    # custom agent type may appear, only `Explore` and `general-purpose`.
    assert "isolated:" not in source
    assert set(re.findall(r"agentType: '([^']+)'", source)) == {"Explore", "general-purpose"}


@pytest.mark.parametrize(
    ("stage", "approval"),
    [
        pytest.param("calibrate", None, id="calibrate-missing"),
        pytest.param("calibrate", "APPROVE_CALIBRATION_RESULTS", id="calibrate-wrong"),
        pytest.param("finalize", None, id="finalize-missing"),
        pytest.param("finalize", "APPROVE_PAID_CALIBRATION", id="finalize-wrong"),
    ],
)
def test_calibration_workflow_refuses_missing_or_wrong_approval(
    development_workflow_runtime: Path, stage: str, approval: str | None
) -> None:
    args = _args(stage)
    if approval is None:
        args.pop("approval")
    else:
        args["approval"] = approval
    probe = _calibration_run(development_workflow_runtime, stage, args)
    assert "approval" in _failure(probe["run"])
    assert probe["calls"] == []

    preflight_args = _args("preflight")
    preflight_args.pop("approval", None)
    preflight = _calibration_run(development_workflow_runtime, "preflight", preflight_args)
    assert preflight["run"]["status"] == "completed", preflight["run"]
    assert preflight["run"]["value"]["status"] == "preflight-passed"


@pytest.mark.parametrize(
    "commit",
    [
        pytest.param("3f2a9c1", id="short-prefix"),
        pytest.param("3F2A9C1E5B7D4E6F8A0B1C2D3E4F5A6B7C8D9E0F", id="uppercase"),
        pytest.param("3f2a9c1e5b7d4e6f8a0b1c2d3e4f5a6b7c8d9e0f\n", id="trailing-newline"),
        pytest.param("3f2a9c1e5b7d4e6f8a0b1c2d3e4f5a6b7c8d9e0'; rm -rf /; echo 'f", id="shell-metacharacters"),
        pytest.param("HEAD..HEAD; echo pwned # aaaaaaaaaaaaaaaaaaaaaaaa", id="injection"),
    ],
)
@pytest.mark.parametrize("stage", ["preflight", "calibrate", "finalize"])
def test_calibration_workflow_refuses_bad_stage_start_commit(
    development_workflow_runtime: Path, stage: str, commit: str
) -> None:
    args = _args(stage)
    args["stageStartCommit"] = commit
    probe = _calibration_run(development_workflow_runtime, stage, args)
    assert "stageStartCommit" in _failure(probe["run"])
    assert probe["calls"] == []
    assert probe["gateCalls"] == []


@pytest.mark.parametrize("stage", ["preflight", "calibrate", "finalize"])
def test_calibration_workflow_quotes_stage_start_commit_in_every_gate(
    development_workflow_runtime: Path, stage: str
) -> None:
    args = _args(stage)
    commit = args["stageStartCommit"]
    probe = _calibration_run(development_workflow_runtime, stage, args)
    assert probe["run"]["status"] == "completed", probe["run"]
    commands = [call["gate"] for call in probe["calls"]] + [gate["command"] for gate in probe["gateCalls"]]
    assert commands
    for command in commands:
        assert f"'{commit}'" in command, command
        assert f"{commit}..HEAD" not in command, command
        assert re.search(rf"(?<!')\b{commit}\b(?!')", command) is None, command
    diff_gates = [command for command in commands if "git diff --check" in command]
    if stage == "preflight":
        assert diff_gates == []
    else:
        assert diff_gates
        assert all(f"git diff --check '{commit}'..HEAD" in command for command in diff_gates)


def _bad_manifest_cases() -> list[Any]:
    cases: list[tuple[str, Any, str]] = [
        ("missing-role", lambda args: args["models"].pop("grader"), "models"),
        (
            "extra-role",
            lambda args: args["models"].update(optimizer={"model": "fixture/optimizer", "thinking": "high"}),
            "models",
        ),
        ("thinking-off", lambda args: args["models"]["executor"].update(thinking="off"), "models"),
        (
            "model-with-thinking-suffix",
            lambda args: args["models"]["comparator"].update(model="claude-bridge/claude-opus-5:high"),
            "models",
        ),
        ("extra-role-key", lambda args: args["models"]["grader"].update(effort="high"), "models"),
        ("models-array", lambda args: args.update(models=[]), "models"),
        ("scenarios-empty", lambda args: args.update(scenarios=[]), "scenarios"),
        (
            "scenarios-two-members",
            lambda args: args.update(scenarios=["runtime-workflow-smoke", "other"]),
            "scenarios",
        ),
        ("scenarios-create", lambda args: args.update(scenarios=["create"]), "scenarios"),
        ("scenarios-missing", lambda args: args.pop("scenarios"), "scenarios"),
    ]
    return [
        pytest.param(stage, mutate, message, id=f"{stage}-{name}")
        for stage in ("preflight", "calibrate")
        for name, mutate, message in cases
    ]


@pytest.mark.parametrize(("stage", "mutate", "message"), _bad_manifest_cases())
def test_calibration_workflow_refuses_bad_models_and_scenarios(
    development_workflow_runtime: Path, stage: str, mutate: Any, message: str
) -> None:
    args = _args(stage)
    mutate(args)
    probe = _calibration_run(development_workflow_runtime, stage, args)
    assert message in _failure(probe["run"]), probe["run"]
    assert probe["calls"] == []


def test_calibration_preflight_refuses_unresolvable_model(development_workflow_runtime: Path) -> None:
    args = _args("preflight")
    args["models"]["executor"]["model"] = "fixture/unavailable"
    refused = _calibration_run(
        development_workflow_runtime,
        "preflight",
        args,
        gate_failures=["--list-models 'fixture/unavailable'"],
    )
    assert "preflight failed closed" in _failure(refused["run"])
    assert _labels(refused) == ["preflight:preflight"]
    assert len(refused["gateCalls"]) == 1

    args = _args("preflight")
    probe = _calibration_run(development_workflow_runtime, "preflight", args)
    assert probe["run"]["status"] == "completed", probe["run"]
    value = probe["run"]["value"]
    assert value["status"] == "preflight-passed"
    assert value["stageStartCommit"] == args["stageStartCommit"]
    assert value["manifest"] == {
        key: args[key] for key in ("campaignId", "createdAt", "repetitions", "maxPaidCalls", "models", "scenarios")
    }
    assert value["models_resolved"] == sorted(set(MANIFEST_MODELS.values()))
    assert value["skipped_work"] == []

    assert _labels(probe) == ["preflight:preflight"]
    child = probe["calls"][0]
    assert child["phaseTitle"] == "Preflight"
    assert child["agentType"] == "Explore"
    assert child["model"] == args["orchestratorModel"]
    assert child["effort"] == "low"
    assert child.get("isolation") is None
    assert "no model call" in child["prompt"]
    assert THREE_FIELD_SEMANTICS in child["prompt"]

    assert len(probe["gateCalls"]) == 1
    gate = probe["gateCalls"][0]["command"]
    assert gate == child["gate"]
    # One invocation per manifest role, in role order, each with the exact-row awk match.
    assert gate.count("--list-models") == len(MANIFEST_MODELS)
    positions = []
    for model in MANIFEST_MODELS.values():
        provider, model_id = model.split("/", 1)
        expected = (
            f"'{args['piExecutable']}' --list-models '{model}' | awk -v p='{provider}' -v m='{model_id}' "
            "'$1 == p && $2 == m { found = 1 } END { exit !found }'"
        )
        assert expected in gate, gate
        positions.append(gate.index(expected, positions[-1] + 1 if positions else 0))
    assert positions == sorted(positions)
    for pin in (PI_REVISION, PI_SUBAGENTS_REVISION, PI_DYNAMIC_WORKFLOWS_REVISION, PI_CLAUDE_BRIDGE_REVISION):
        assert f"'{pin}'" in gate
    assert f"test \"$(git -C '{args['repoPath']}' rev-parse HEAD)\" = '{args['stageStartCommit']}'" in gate
    assert f"test -z \"$(git -C '{args['repoPath']}' status --porcelain)\"" in gate
    assert f"test -x '{args['piExecutable']}'" in gate
    assert f"test \"$('{args['piExecutable']}' --version)\" = '0.84.4'" in gate
    assert (
        f"diff -r -x __pycache__ '{args['repoPath']}/skills/pi-skill-creator' '{args['installedSkillPath']}'"
        in gate
    )
    assert '"$HOME/.pi/agent/skills/pi-skill-creator"' in gate
    assert '"$HOME/.agents/skills/pi-skill-creator"' in gate
    assert f"test ! -e '{args['campaignDir']}/campaign.json'" in gate
    assert "git diff --check" not in gate
    assert "pytest" not in gate


def test_calibrate_refuses_call_count_above_max_paid_calls(development_workflow_runtime: Path) -> None:
    args = _args("calibrate")
    assert args["maxPaidCalls"] == 10
    refused = _calibration_run(
        development_workflow_runtime,
        "calibrate",
        args,
        responses={"OSC-14": _calibration_response(paid_calls_used=11)},
    )
    assert "Paid-call bound mismatch" in _failure(refused["run"])
    assert _labels(refused) == ["preflight:calibrate", "OSC-14"]

    mismatched = _calibration_run(
        development_workflow_runtime,
        "calibrate",
        args,
        responses={"OSC-14": _calibration_response(max_paid_calls=40)},
    )
    assert "Paid-call bound mismatch" in _failure(mismatched["run"])
    assert _labels(mismatched) == ["preflight:calibrate", "OSC-14"]

    probe = _calibration_run(development_workflow_runtime, "calibrate", args)
    assert probe["run"]["status"] == "completed", probe["run"]
    assert _labels(probe) == ["preflight:calibrate", "OSC-14", "integrate:OSC-14"]
    preflight, writer, integration = probe["calls"]
    assert preflight["phaseTitle"] == "Preflight"
    assert writer["phaseTitle"] == "Calibrate"
    assert integration["phaseTitle"] == "Calibrate"
    assert writer["agentType"] == "general-purpose"
    assert writer["model"] == args["writerModel"]
    assert writer["effort"] == "high"
    assert writer["isolation"] == "worktree"
    assert integration["agentType"] == "general-purpose"
    assert integration["model"] == args["integratorModel"]
    assert integration.get("isolation") is None

    value = probe["run"]["value"]
    assert value["status"] == "awaiting-human-calibration-review"
    assert value["calibrationIntegrationCommit"] == INTEGRATION_COMMIT
    assert value["campaignId"] == "smoke-1"
    assert value["campaignDir"] == args["campaignDir"]
    assert value["paid_calls_used"] == 10
    assert value["max_paid_calls"] == 10
    assert value["records"] == ["workflow-result.json", "review-required.json"]
    assert value["manual_review_required"] == ["review-required.json"]
    assert value["bounded_work"] == []
    assert value["skipped_work"] == []

    # The calibrate preflight gate is the mechanical preflight minus the empty-campaign check.
    assert "--list-models" in preflight["gate"]
    assert "campaign.json" not in preflight["gate"]
    # The writer and the integrator run under the replay-only live gate plus the deterministic gate.
    for command in (writer["gate"], integration["gate"]):
        assert f"PI_SKILL_CREATOR_CAMPAIGN_DIR='{args['campaignDir']}'" in command
        assert "PI_SKILL_CREATOR_MAX_PAID_CALLS='10'" in command
        assert "PI_SKILL_CREATOR_LIVE_TESTS=1 PI_SKILL_CREATOR_REPLAY_ONLY=1" in command
        assert "tests/pi-skill-creator/test_live_calibration.py -m live" in command
        for variable, key in (
            ("PI_EXECUTABLE", "piExecutable"),
            ("PI_CHECKOUT", "piPath"),
            ("PI_SUBAGENTS_CHECKOUT", "piSubagentsPath"),
            ("PI_DYNAMIC_WORKFLOWS_CHECKOUT", "piDynamicWorkflowsPath"),
        ):
            assert f"{variable}='{args[key]}'" in command
        assert "-m 'not live'" in command
        assert "ty check skills/pi-skill-creator/scripts skills/pi-skill-creator/eval-viewer" in command


def test_calibrate_preflight_defines_repository_revision(
    development_workflow_runtime: Path,
) -> None:
    """OSC-14: the calibrate child failed three smokes by reading this as stageStartCommit.

    `repository_revision` is the evaluation project's HEAD, a temporary directory with its
    own git history, so it never equals `stageStartCommit` and names no object in the
    repository. The prompt has to say so, or the stage fails closed on a correct record.
    """
    args = _args("calibrate")
    probe = _calibration_run(development_workflow_runtime, "calibrate", args)
    preflight = probe["calls"][0]
    assert preflight["label"] == "preflight:calibrate", probe["calls"]
    prompt = preflight["prompt"]
    assert "repository_revision" in prompt
    assert "evaluation project" in prompt
    assert "never args.stageStartCommit" in prompt
    assert "correct rather than a finding" in prompt


def test_calibration_workflow_makes_no_paid_call_prompt(development_workflow_runtime: Path) -> None:
    probe = _calibration_run(development_workflow_runtime, "calibrate", _args("calibrate"))
    assert probe["run"]["status"] == "completed", probe["run"]
    assert len(probe["calls"]) == 3
    for call in probe["calls"]:
        assert "no model call" in call["prompt"], call["label"]
        assert "Never exceed maxPaidCalls" not in call["prompt"], call["label"]
    writer = probe["calls"][1]
    for required in (
        "workflow-result.json",
        "review-required.json",
        "test_live_calibration.py",
        "paid_calls_used",
        "agent_calls_made",
        "run.json",
        "comparison.json",
        "maxPaidCalls=10",
    ):
        assert required in writer["prompt"], required
    source = CALIBRATION_WORKFLOW.read_text(encoding="utf-8")
    assert "Never exceed maxPaidCalls" not in source


def test_finalize_stage_groups_integration_under_its_own_phases(development_workflow_runtime: Path) -> None:
    args = _args("finalize")
    probe = _calibration_run(development_workflow_runtime, "finalize", args)
    assert probe["run"]["status"] == "completed", probe["run"]
    assert [(call["label"], call["phaseTitle"]) for call in probe["calls"]] == [
        ("preflight:finalize", "Preflight"),
        ("OSC-15", "Human checkpoint"),
        ("integrate:OSC-15", "Human checkpoint"),
        ("OSC-16", "Distribution"),
        ("integrate:OSC-16", "Distribution"),
    ]
    value = probe["run"]["value"]
    assert value["status"] == "distribution-validated"
    assert value["finalCommit"] == INTEGRATION_COMMIT
    assert value["paid_calls_used"] == 0
    assert value["skipped_work"] == []
    assert f"test -f '{args['humanReviewRecord']}'" in probe["calls"][0]["gate"]

    args["humanReviewComplete"] = False
    refused = _calibration_run(development_workflow_runtime, "finalize", args)
    assert "humanReviewComplete" in _failure(refused["run"])
    assert refused["calls"] == []

    args = _args("finalize")
    args["humanReviewRecord"] = "relative/review.json"
    refused = _calibration_run(development_workflow_runtime, "finalize", args)
    assert "humanReviewRecord" in _failure(refused["run"])
    assert refused["calls"] == []


def test_adoption_workflow_groups_integration_under_implementation_phase(
    development_workflow_runtime: Path,
) -> None:
    probe = _adoption_run(development_workflow_runtime, _args("adoption"))
    assert probe["run"]["status"] == "completed", probe["run"]
    assert probe["run"]["value"]["status"] == "ready-for-calibration"
    assert probe["run"]["value"]["implementationIntegrationCommit"] == INTEGRATION_COMMIT

    titles = [phase["title"] for phase in probe["meta"]["phases"]]
    assert "Integrate" not in titles
    assert titles == [
        "Preflight",
        "Foundation",
        "Contracts",
        "Core",
        "Models",
        "Execution",
        "Doctrine",
        "Runtime workflow",
        "README",
    ]
    assert "phase: 'Integrate'" not in ADOPTION_WORKFLOW.read_text(encoding="utf-8")

    integrations = [call for call in probe["calls"] if call["label"].startswith("integrate:")]
    assert [call["label"].split(":", 1)[1] for call in integrations] == list(ADOPTION_WAVES)
    for call in integrations:
        assert call["phaseTitle"] == ADOPTION_WAVES[call["label"].split(":", 1)[1]], call["label"]
    orders = [call for call in probe["calls"] if call["label"].startswith("OSC-")]
    assert len(orders) == 14
    calls_in_order = sorted(probe["calls"], key=lambda call: call["index"])
    phase_of_wave: str | None = None
    for call in calls_in_order:
        if call["label"].startswith("OSC-"):
            assert phase_of_wave in {None, call["phaseTitle"]}, call
            phase_of_wave = call["phaseTitle"]
        elif call["label"].startswith("integrate:"):
            assert call["phaseTitle"] == phase_of_wave, call
            phase_of_wave = None
    assert all(call["phaseTitle"] != "Integrate" for call in probe["calls"])


def test_development_workflow_prompts_state_three_field_semantics(development_workflow_runtime: Path) -> None:
    prompts: list[tuple[str, str]] = []
    for stage in ("calibrate", "finalize"):
        probe = _calibration_run(development_workflow_runtime, stage, _args(stage))
        assert probe["run"]["status"] == "completed", probe["run"]
        prompts.extend((call["label"], call["prompt"]) for call in probe["calls"])
    adoption = _adoption_run(development_workflow_runtime, _args("adoption"))
    assert adoption["run"]["status"] == "completed", adoption["run"]
    prompts.extend((call["label"], call["prompt"]) for call in adoption["calls"])

    writers = [(label, prompt) for label, prompt in prompts if label.startswith(("OSC-", "integrate:"))]
    # calibrate: OSC-14 and its integration; finalize: OSC-15, OSC-16, and their integrations;
    # adoption: 14 orders and 8 wave integrations.
    assert len(writers) == 2 + 4 + 22
    for label, prompt in writers:
        assert THREE_FIELD_SEMANTICS in prompt, label
        for field in ("tests_skipped", "bounded_work", "skipped_work"):
            assert field in prompt, (label, field)


def test_smoke_fixture_skill_validates() -> None:
    skill_md = SMOKE_SKILL / "SKILL.md"
    assert skill_md.is_file()
    result = subprocess.run(
        ["python3", "scripts/quick_validate.py", os.fspath(SMOKE_SKILL)],
        cwd=SKILL_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Skill is valid!" in result.stdout

    text = skill_md.read_text(encoding="utf-8")
    frontmatter = text.split("---\n", 2)[1]
    assert "name: release-note-smoke" in frontmatter.splitlines()
    description = next(line for line in frontmatter.splitlines() if line.startswith("description:"))
    assert "release note" in description and "changelog" in description
    for heading in ("Summary", "Changes", "Upgrade notes"):
        assert heading in text
    assert "Upgrade notes" in text.split("## Rules", 1)[1]
    assert "\u2014" not in text

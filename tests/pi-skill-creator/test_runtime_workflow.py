"""Contract tests for the runtime benchmark workflow on both pinned workflow runtimes.

The same ``workflows/benchmark.js`` runs through pinned pi-subagents (stub host over
the compiled ``runtime.js``) and through pinned pi-dynamic-workflows (``runWorkflow``
with an injected runner). Neither path makes a model call or touches a real agent.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

from conftest import (
    PI_DYNAMIC_WORKFLOWS_REVISION,
    PI_SUBAGENTS_REVISION,
    verify_checkout_revision,
)

FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures/workflow"
RUNTIMES = ("pi-subagents", "pi-dynamic-workflows")
ARGS_FILES = {
    "pi-subagents": "valid-args.json",
    "pi-dynamic-workflows": "valid-args-pi-dynamic-workflows.json",
}
EXPECTED_PHASES = ["Prepare", "Execute", "Grade", "Validate", "Aggregate"]
EXECUTE_WITH = "execute:runtime-behavior:with_skill:run-1"
EXECUTE_WITHOUT = "execute:runtime-behavior:without_skill:run-1"
GRADE_WITH = "grade:runtime-behavior:with_skill:run-1"
GRADE_WITHOUT = "grade:runtime-behavior:without_skill:run-1"

_NODE_PROBE = r"""
(async () => {
const { pathToFileURL } = await import("node:url");
let stdin = "";
for await (const chunk of process.stdin) stdin += chunk;
const input = JSON.parse(stdin);
const moduleUrl = name => pathToFileURL(`${input.runtimeRoot}/${name}.js`).href;
const { extractMeta } = await import(moduleUrl("meta"));
const { runWorkflow } = await import(moduleUrl("runtime"));

const source = input.source;
const parsedMeta = extractMeta(source).meta;
const calls = [];
const gateCalls = [];
const campaignRoot = `${input.args.projectRoot}/.skill-creator/example-skill/campaign-${input.args.campaignId}`;
const iterationRoot = `${campaignRoot}/iteration-${input.args.iteration}`;

function responseFor(label) {
  if (label === "setup") return {
    status: "completed",
    // `setup-campaign-root` reproduces the OSC-14 smoke failure: the child returned
    // the campaign directory where the contract requires the campaign.json file.
    campaign_path: input.scenario === "setup-campaign-root"
      ? campaignRoot
      : `${campaignRoot}/campaign.json`,
    evals_path: `${campaignRoot}/evals.json`,
  };
  if (label.startsWith("execute:")) {
    const [, evalName, configuration, runPart] = label.split(":");
    const runRoot = `${iterationRoot}/${evalName}/${configuration}/${runPart}`;
    return input.scenario === "explicit-failure" && configuration === "without_skill"
      ? { status: "failed", error: "fixture executor failure" }
      : {
          status: "completed",
          run_path: `${runRoot}/run.json`,
          transcript_metrics_path: `${runRoot}/transcript-metrics.json`,
          outputs_path: `${runRoot}/outputs`,
          timing_path: `${runRoot}/timing.json`,
          effective_model: "fixture/executor-effective",
          effective_thinking: "low",
        };
  }
  if (label.startsWith("grade:")) {
    const [, evalName, configuration, runPart] = label.split(":");
    return {
      status: "completed",
      grading_path: `${iterationRoot}/${evalName}/${configuration}/${runPart}/grading.json`,
      effective_model: "fixture/grader-effective",
      effective_thinking: "high",
    };
  }
  if (label === "validate") {
    return input.scenario === "validation-failure"
      ? { status: "failed", error: "fixture validation failure" }
      : { status: "completed" };
  }
  if (label === "aggregate") return {
    status: "completed",
    benchmark_json_path: `${iterationRoot}/benchmark.json`,
    benchmark_markdown_path: `${iterationRoot}/benchmark.md`,
  };
  throw new Error(`unexpected label ${label}`);
}

function hostFor(scenario, spawnCount) {
  return {
    async spawnAgent(request) {
      calls.push({
        label: request.label,
        prompt: request.prompt,
        phase: request.phaseTitle,
        agentType: request.agentType,
        model: request.model,
        effort: request.effort,
        gate: request.gate,
      });
      spawnCount.count += 1;
      const control = request.label.startsWith("execute:") && request.label.includes("without_skill");
      if (scenario === "setup-null" && request.label === "setup") {
        return { ok: false, error: "fixture setup failure" };
      }
      if (scenario === "schema-null" && control) {
        return { ok: true, text: "{}", outputTokens: 7 };
      }
      if (scenario === "spawn-failure" && control) {
        return { ok: false, error: "fixture spawn failure" };
      }
      return { ok: true, text: JSON.stringify(responseFor(request.label)), outputTokens: 7 };
    },
    abortAgent() {},
    async runGate(command, gate) {
      gateCalls.push({ command, agentId: gate.agentId });
      return { ok: true, output: "" };
    },
  };
}

const spawnCount = { count: 0 };
let run;
let replay;
let journal = [];
try {
  run = await runWorkflow({
    script: source,
    args: input.args,
    host: hostFor(input.scenario, spawnCount),
    concurrency: 4,
    journal: input.resume ? { append: entry => journal.push(entry) } : undefined,
  });
  if (input.resume) {
    const before = spawnCount.count;
    replay = await runWorkflow({
      script: source,
      args: input.args,
      host: hostFor("success", spawnCount),
      concurrency: 4,
      journal: { entries: journal },
    });
    replay.spawned = spawnCount.count - before;
  }
} catch (error) {
  run = { status: "threw", error: String(error.message ?? error) };
}
process.stdout.write(JSON.stringify({ meta: parsedMeta, run, replay, calls, gateCalls }));
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
"""


def _checkout() -> Path:
    value = os.environ.get("PI_SUBAGENTS_CHECKOUT")
    if not value:
        pytest.skip("runtime workflow tests require PI_SUBAGENTS_CHECKOUT")
    try:
        return verify_checkout_revision(
            Path(value), PI_SUBAGENTS_REVISION, "pi-subagents checkout"
        )
    except ValueError as error:
        pytest.fail(str(error), pytrace=False)


def _dynamic_checkout() -> Path:
    value = os.environ.get("PI_DYNAMIC_WORKFLOWS_CHECKOUT")
    if not value:
        pytest.skip("pi-dynamic-workflows probes require PI_DYNAMIC_WORKFLOWS_CHECKOUT")
    try:
        return verify_checkout_revision(
            Path(value), PI_DYNAMIC_WORKFLOWS_REVISION, "pi-dynamic-workflows checkout"
        )
    except ValueError as error:
        pytest.fail(str(error), pytrace=False)


@pytest.fixture(scope="session")
def workflow_runtime_modules(tmp_path_factory: pytest.TempPathFactory) -> Path:
    checkout = _checkout()
    output_root = tmp_path_factory.mktemp("pi-subagents-dist")
    compiler = checkout / "node_modules/.bin/tsc"
    if not compiler.is_file():
        pytest.skip("runtime workflow tests require the pinned checkout dependencies")
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


@pytest.fixture(scope="session")
def dynamic_workflows_runtime(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Path]:
    """Pinned pi-dynamic-workflows checkout plus the `tsx` binary `npm ci` produced there."""
    checkout = _dynamic_checkout()
    tsx = checkout / "node_modules/.bin/tsx"
    if not tsx.is_file():
        pytest.skip(
            "pi-dynamic-workflows probes require node_modules/.bin/tsx from `npm ci` in the checkout"
        )
    return {
        "checkout": checkout,
        "tsx": tsx,
        "cwd": tmp_path_factory.mktemp("pi-dynamic-workflows-cwd"),
    }


def _args(runtime: str = "pi-subagents") -> dict[str, Any]:
    return json.loads((FIXTURE_ROOT / ARGS_FILES[runtime]).read_text(encoding="utf-8"))


def _source(skill_root: Path) -> str:
    workflow = skill_root / "workflows/benchmark.js"
    assert workflow.is_file(), "workflows/benchmark.js must exist"
    return workflow.read_text(encoding="utf-8")


def _probe_pi_subagents(
    skill_root: Path,
    runtime_root: Path,
    *,
    args: dict[str, Any] | None = None,
    scenario: str = "success",
    resume: bool = False,
) -> dict[str, Any]:
    result = subprocess.run(
        ["node", "-e", _NODE_PROBE],
        input=json.dumps(
            {
                "runtimeRoot": os.fspath(runtime_root),
                "source": _source(skill_root),
                "args": args or _args("pi-subagents"),
                "scenario": scenario,
                "resume": resume,
            }
        ),
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def _probe_pi_dynamic_workflows(
    skill_root: Path,
    runtime: dict[str, Path],
    *,
    args: dict[str, Any] | None = None,
    scenario: str = "success",
    resume: bool = False,
) -> dict[str, Any]:
    result = subprocess.run(
        [os.fspath(runtime["tsx"]), os.fspath(FIXTURE_ROOT / "pi-dynamic-workflows-probe.mjs")],
        input=json.dumps(
            {
                "checkout": os.fspath(runtime["checkout"]),
                "source": _source(skill_root),
                "args": args or _args("pi-dynamic-workflows"),
                "scenario": scenario,
                "resume": resume,
                "cwd": os.fspath(runtime["cwd"]),
            }
        ),
        cwd=runtime["cwd"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


@dataclass(frozen=True)
class _Probe:
    runtime: str
    run: Callable[..., dict[str, Any]]

    def args(self) -> dict[str, Any]:
        return _args(self.runtime)


def _probe(request: pytest.FixtureRequest, runtime: str) -> _Probe:
    skill_root = request.getfixturevalue("skill_root")
    if runtime == "pi-subagents":
        modules = request.getfixturevalue("workflow_runtime_modules")
        return _Probe(
            runtime,
            lambda **kwargs: _probe_pi_subagents(skill_root, modules, **kwargs),
        )
    dynamic = request.getfixturevalue("dynamic_workflows_runtime")
    return _Probe(
        runtime,
        lambda **kwargs: _probe_pi_dynamic_workflows(skill_root, dynamic, **kwargs),
    )


def _refusal(run: dict[str, Any]) -> str:
    """The argument-validation error text, whichever way the runtime reports a failed run."""
    assert run["status"] in {"failed", "threw"}, run
    return str(run["error"])


def _role_for(label: str, roles: dict[str, Any]) -> dict[str, str]:
    return roles["grader"] if label.startswith("grade:") else roles["executor"]


def _assert_shared_meta(meta: dict[str, Any]) -> None:
    assert meta["name"] == "pi-skill-creator-benchmark"
    assert "whenToUse" not in meta
    assert [phase["title"] for phase in meta["phases"]] == EXPECTED_PHASES
    assert all("detail" not in phase for phase in meta["phases"])


def _assert_complete_success(value: dict[str, Any], runtime: str) -> None:
    assert value["valid"] is True
    assert value["workflow_runtime"] == runtime
    assert value["expected_runs"] == 2
    assert value["scheduled_runs"] == 2
    assert value["status_counts"] == {"completed": 2, "failed": 0, "skipped": 0, "bounded": 0}
    assert value["failure_kinds"] == {"null_result": 0, "thrown": 0, "explicit": 0, "contract": 0}
    assert value["stage_statuses"] == {
        "setup": "completed",
        "validation": "completed",
        "aggregation": "completed",
    }
    assert "benchmark_json" in value["durable_paths"]
    assert value["telemetry"]["per_launcher_cost"] == "unavailable"
    assert value["effective_roles"]["executor"]["models"] == ["fixture/executor-effective"]
    assert value["effective_roles"]["grader"]["models"] == ["fixture/grader-effective"]
    # One eval, two arms, one repetition: 1 setup + 2 executes + 2 grades + validate + aggregate.
    assert value["agent_calls_planned"] == 7
    assert value["agent_calls_made"] == 7
    assert value["max_agent_calls"] == 7


def _assert_pipeline_order(labels: list[str]) -> None:
    for label in (EXECUTE_WITH, EXECUTE_WITHOUT, GRADE_WITH, GRADE_WITHOUT, "validate", "aggregate"):
        assert labels.count(label) == 1, labels
    assert labels.index(GRADE_WITH) > labels.index(EXECUTE_WITH)
    assert labels.index(GRADE_WITHOUT) > labels.index(EXECUTE_WITHOUT)
    assert labels.index("validate") > max(labels.index(GRADE_WITH), labels.index(GRADE_WITHOUT))
    assert labels.index("aggregate") > labels.index("validate")


def test_runtime_workflow_fails_closed_and_pipelines_execution_into_grading(
    skill_root: Path,
    workflow_runtime_modules: Path,
) -> None:
    probe = _probe_pi_subagents(skill_root, workflow_runtime_modules)
    assert probe["run"]["status"] == "completed", probe["run"]
    value = probe["run"]["value"]
    roles = _args("pi-subagents")["roles"]

    _assert_shared_meta(probe["meta"])
    _assert_complete_success(value, "pi-subagents")
    _assert_pipeline_order([call["label"] for call in probe["calls"]])

    # The shim passes the suffix-free model plus `effort`; nothing else reaches the host.
    for call in probe["calls"]:
        role = _role_for(call["label"], roles)
        assert call["model"] == role["model"], call
        assert ":" not in call["model"], call
        assert call["effort"] == role["thinking"], call
        # JSON.stringify drops undefined fields, so an absent gate has no key at all.
        assert call.get("gate") is None, call
        # The runtime substitutes its own default when the script names no agent type.
        assert call["agentType"] == "general-purpose", call
    assert probe["gateCalls"] == []


@pytest.mark.parametrize(
    "scenario",
    [pytest.param("success", id="success"), pytest.param("max-thinking", id="max-thinking")],
)
def test_runtime_workflow_executes_on_pi_dynamic_workflows(
    skill_root: Path,
    dynamic_workflows_runtime: dict[str, Path],
    scenario: str,
) -> None:
    args = _args("pi-dynamic-workflows")
    if scenario == "max-thinking":
        args["roles"]["executor"]["thinking"] = "max"
        args["roles"]["grader"]["thinking"] = "xhigh"
    probe = _probe_pi_dynamic_workflows(skill_root, dynamic_workflows_runtime, args=args)
    assert probe["run"]["status"] == "completed", probe["run"]
    value = probe["run"]["value"]

    _assert_shared_meta(probe["meta"])
    _assert_complete_success(value, "pi-dynamic-workflows")
    _assert_pipeline_order([call["label"] for call in probe["calls"]])

    # The shim passes `provider/id:thinking` and no `effort` key on this runtime.
    for call in probe["calls"]:
        role = _role_for(call["label"], args["roles"])
        assert call["model"] == f"{role['model']}:{role['thinking']}", call
        assert "effort" not in call["keys"], call
        assert "model" in call["keys"] and "label" in call["keys"] and "schema" in call["keys"]


@pytest.mark.parametrize(
    ("runtime", "scenario", "kind", "prefix"),
    [
        pytest.param("pi-subagents", "explicit-failure", "explicit", "", id="pi-subagents-explicit-failure"),
        pytest.param("pi-subagents", "schema-null", "null_result", "null-result:", id="pi-subagents-schema-null"),
        pytest.param("pi-subagents", "spawn-failure", "null_result", "null-result:", id="pi-subagents-spawn-failure"),
        pytest.param(
            "pi-dynamic-workflows", "explicit-failure", "explicit", "", id="pi-dynamic-workflows-explicit-failure"
        ),
        pytest.param(
            "pi-dynamic-workflows", "null-child", "null_result", "null-result:", id="pi-dynamic-workflows-null-child"
        ),
        pytest.param(
            "pi-dynamic-workflows",
            "recoverable-throw",
            "null_result",
            "null-result:",
            id="pi-dynamic-workflows-recoverable-throw",
        ),
        pytest.param("pi-dynamic-workflows", "thrown-child", "thrown", "thrown:", id="pi-dynamic-workflows-thrown-child"),
    ],
)
def test_runtime_workflow_accounts_for_failed_and_null_items(
    request: pytest.FixtureRequest,
    runtime: str,
    scenario: str,
    kind: str,
    prefix: str,
) -> None:
    probe = _probe(request, runtime).run(scenario=scenario)
    # A thrown child must not abort the campaign on either runtime.
    assert probe["run"]["status"] == "completed", probe["run"]
    value = probe["run"]["value"]
    labels = [call["label"] for call in probe["calls"]]

    assert value["valid"] is False
    assert value["status_counts"]["failed"] == 1
    assert value["status_counts"]["completed"] == 1
    assert set(value["status_counts"]) == {"completed", "failed", "skipped", "bounded"}
    assert sum(value["status_counts"].values()) == value["expected_runs"]
    expected_kinds = {"null_result": 0, "thrown": 0, "explicit": 0, "contract": 0}
    expected_kinds[kind] = 1
    assert value["failure_kinds"] == expected_kinds
    failed = [result for result in value["results"] if result["status"] == "failed"]
    assert len(failed) == 1
    assert failed[0]["configuration"] == "without_skill"
    assert isinstance(failed[0]["error"], str) and failed[0]["error"]
    assert failed[0]["error"].startswith(prefix)
    if prefix:
        assert "runtime-behavior:without_skill:run-1" in failed[0]["error"]
    assert value["stage_statuses"] == {"setup": "completed", "validation": "bounded", "aggregation": "bounded"}
    assert "benchmark_json" not in value["durable_paths"]
    assert "validate" not in labels and "aggregate" not in labels


@pytest.mark.parametrize("runtime", RUNTIMES)
def test_runtime_workflow_refuses_missing_approval_and_setup_failure(
    request: pytest.FixtureRequest, runtime: str
) -> None:
    probe = _probe(request, runtime)
    args = probe.args()
    args["approved"] = False
    assert "approved" in _refusal(probe.run(args=args)["run"]).lower()

    setup_failure = probe.run(scenario="setup-null")
    assert setup_failure["run"]["status"] == "completed", setup_failure["run"]
    value = setup_failure["run"]["value"]
    assert value["valid"] is False
    assert value["workflow_runtime"] == runtime
    assert value["scheduled_runs"] == 0
    assert value["status_counts"] == {"completed": 0, "failed": 0, "skipped": 0, "bounded": 2}
    assert value["failure_kinds"] == {"null_result": 1, "thrown": 0, "explicit": 0, "contract": 0}
    assert value["stage_statuses"] == {"setup": "failed", "validation": "bounded", "aggregation": "bounded"}
    assert value["results"] == []
    assert [call["label"] for call in setup_failure["calls"]] == ["setup"]


@pytest.mark.parametrize("runtime", RUNTIMES)
def test_runtime_workflow_refuses_a_setup_that_returns_the_campaign_directory(
    request: pytest.FixtureRequest, runtime: str
) -> None:
    """The OSC-14 smoke failure: `campaign_path` was the campaign root, not campaign.json."""
    probe = _probe(request, runtime)
    result = probe.run(scenario="setup-campaign-root")
    assert result["run"]["status"] == "completed", result["run"]
    value = result["run"]["value"]
    assert value["valid"] is False
    assert value["scheduled_runs"] == 0
    assert value["failure_kinds"] == {"null_result": 0, "thrown": 0, "explicit": 0, "contract": 1}
    assert value["stage_statuses"] == {
        "setup": "failed",
        "validation": "bounded",
        "aggregation": "bounded",
    }
    # No executor process may start once the campaign tree is unconfirmed.
    assert [call["label"] for call in result["calls"]] == ["setup"]


@pytest.mark.parametrize("runtime", RUNTIMES)
def test_runtime_workflow_setup_prompt_pins_paths_and_forbids_transcribed_revisions(
    request: pytest.FixtureRequest, runtime: str
) -> None:
    """Both OSC-14 setup defects are prevented in the prompt, not just detected after."""
    probe = _probe(request, runtime)
    result = probe.run()
    setup = next(call for call in result["calls"] if call["label"] == "setup")
    args = probe.args()
    campaign_root = (
        f"{args['projectRoot']}/.skill-creator/example-skill/campaign-{args['campaignId']}"
    )
    # The exact return values, so `campaign_path` cannot be read as the directory.
    assert f"campaign_path exactly {campaign_root}/campaign.json" in setup["prompt"]
    assert f"evals_path exactly {campaign_root}/evals.json" in setup["prompt"]
    assert "not the directory holding them" in setup["prompt"]
    # Revisions are substituted by the shell, never transcribed into the reply.
    assert "$(git -C" in setup["prompt"]
    assert "never by copying a value into your reply" in setup["prompt"]


@pytest.mark.parametrize("runtime", RUNTIMES)
def test_runtime_workflow_execute_requires_only_executor_owned_artifacts(
    request: pytest.FixtureRequest, runtime: str
) -> None:
    """The executor cannot be asked to prove grading.json, which the next stage writes."""
    probe = _probe(request, runtime)
    result = probe.run()
    execute = next(call for call in result["calls"] if call["label"] == EXECUTE_WITH)
    prompt = execute["prompt"]
    # timing.json is the RPC runner's own output and stays required.
    assert "timing.json" in prompt
    assert "run.json" in prompt and "transcript-metrics.json" in prompt
    # grading.json belongs to the grade stage that runs after this one.
    assert "grading.json" not in prompt


@pytest.mark.parametrize("runtime", RUNTIMES)
def test_runtime_workflow_grade_follows_execute_for_each_item(
    request: pytest.FixtureRequest, runtime: str
) -> None:
    """Ordering is what makes grading.json unavailable at execute time; pin it."""
    probe = _probe(request, runtime)
    labels = [call["label"] for call in probe.run()["calls"]]
    assert labels.index(EXECUTE_WITH) < labels.index(GRADE_WITH)
    assert labels.index(EXECUTE_WITHOUT) < labels.index(GRADE_WITHOUT)


@pytest.mark.parametrize("runtime", RUNTIMES)
@pytest.mark.parametrize(
    "project_root",
    ["/tmp/x", "/private/tmp/x", "/var/tmp/x", "/var/folders/ab/x", "/dev/shm/x"],
)
def test_runtime_workflow_refuses_an_ephemeral_project_root(
    request: pytest.FixtureRequest, runtime: str, project_root: str
) -> None:
    """Campaign records are the only evidence a claim rests on; /tmp loses them at reboot."""
    probe = _probe(request, runtime)
    args = probe.args()
    args["projectRoot"] = project_root
    args.pop("allowEphemeralProjectRoot", None)
    refusal = _refusal(probe.run(args=args)["run"])
    assert "temporary directory" in refusal, refusal
    assert "allowEphemeralProjectRoot" in refusal, refusal
    # Refused during argument validation, so nothing is spent.
    assert probe.run(args=args)["calls"] == []


@pytest.mark.parametrize("runtime", RUNTIMES)
def test_runtime_workflow_records_that_a_disposable_campaign_is_volatile(
    request: pytest.FixtureRequest, runtime: str
) -> None:
    """Opting in is allowed, but the campaign has to say so in its own notes."""
    probe = _probe(request, runtime)
    args = probe.args()
    args["projectRoot"] = "/tmp/skill-creator-project"
    args["allowEphemeralProjectRoot"] = True
    result = probe.run(args=args)
    assert result["run"]["status"] == "completed", result["run"]
    setup = next(call for call in result["calls"] if call["label"] == "setup")
    assert "reclaimed at reboot" in setup["prompt"]
    assert "Copy the campaign root somewhere durable" in setup["prompt"]


@pytest.mark.parametrize("runtime", RUNTIMES)
def test_runtime_workflow_accepts_a_durable_project_root_without_the_flag(
    request: pytest.FixtureRequest, runtime: str
) -> None:
    """The ordinary case stays flagless, and records no volatility note."""
    probe = _probe(request, runtime)
    args = probe.args()
    args["projectRoot"] = "/Users/example/projects/evaluation"
    args.pop("allowEphemeralProjectRoot", None)
    result = probe.run(args=args)
    assert result["run"]["status"] == "completed", result["run"]
    setup = next(call for call in result["calls"] if call["label"] == "setup")
    assert "reclaimed at reboot" not in setup["prompt"]


def test_runtime_workflow_rejects_unknown_runtime(
    skill_root: Path, workflow_runtime_modules: Path
) -> None:
    args = _args("pi-subagents")
    args["runtime"] = "claude-code"
    probe = _probe_pi_subagents(skill_root, workflow_runtime_modules, args=args)
    assert probe["run"]["status"] == "failed", probe["run"]
    assert "runtime" in probe["run"]["error"]
    assert probe["calls"] == []


def _unportable_cases() -> list[Any]:
    cases: list[tuple[str, Callable[[dict[str, Any]], None], str]] = [
        ("unknown-runtime", lambda args: args.update(runtime="claude-code"), "runtime"),
        ("missing-runtime", lambda args: args.pop("runtime"), "runtime"),
        ("missing-runtime-checkout", lambda args: args.pop("runtimeCheckout"), "runtimeCheckout"),
        (
            "relative-runtime-checkout",
            lambda args: args.update(runtimeCheckout="relative/pi-dynamic-workflows"),
            "runtimeCheckout",
        ),
        (
            "subagents-checkout-mismatch",
            lambda args: args.update(runtime="pi-subagents", runtimeCheckout="/tmp/skill-creator-runtime/other"),
            "runtimeCheckout",
        ),
        (
            "model-with-thinking-suffix",
            lambda args: args["roles"]["executor"].update(model="fixture/executor:high"),
            "roles.executor.model",
        ),
    ]
    for role in ("executor", "grader", "comparator", "benchmarkAnalyzer"):
        cases.append(
            (
                f"thinking-off-{role}",
                lambda args, role=role: args["roles"][role].update(thinking="off"),
                f"roles.{role}.thinking",
            )
        )
    return [
        pytest.param(runtime, mutate, message, id=f"{runtime}-{name}")
        for runtime in RUNTIMES
        for name, mutate, message in cases
    ]


@pytest.mark.parametrize(("runtime", "mutate", "message"), _unportable_cases())
def test_runtime_workflow_refuses_unportable_arguments(
    request: pytest.FixtureRequest,
    runtime: str,
    mutate: Callable[[dict[str, Any]], None],
    message: str,
) -> None:
    probe = _probe(request, runtime)
    args = probe.args()
    mutate(args)
    result = probe.run(args=args)
    assert message in _refusal(result["run"]), result["run"]
    assert result["calls"] == []


def _max_agent_calls_cases() -> list[Any]:
    cases: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("plan-above-bound", lambda args: args.update(maxAgentCalls=6)),
        ("zero", lambda args: args.update(maxAgentCalls=0)),
        ("negative", lambda args: args.update(maxAgentCalls=-1)),
        ("fractional", lambda args: args.update(maxAgentCalls=1.5)),
        ("string", lambda args: args.update(maxAgentCalls="7")),
        ("missing", lambda args: args.pop("maxAgentCalls")),
    ]
    return [
        pytest.param(runtime, mutate, id=f"{runtime}-{name}")
        for runtime in RUNTIMES
        for name, mutate in cases
    ]


@pytest.mark.parametrize(("runtime", "mutate"), _max_agent_calls_cases())
def test_runtime_workflow_refuses_plan_above_max_agent_calls(
    request: pytest.FixtureRequest,
    runtime: str,
    mutate: Callable[[dict[str, Any]], None],
) -> None:
    """`maxAgentCalls` is a required positive integer that the exact plan must not exceed."""
    probe = _probe(request, runtime)
    args = probe.args()
    mutate(args)
    result = probe.run(args=args)
    message = _refusal(result["run"])
    assert "maxAgentCalls" in message, result["run"]
    if args.get("maxAgentCalls") == 6:
        # The refusal names both numbers: the plan and the bound.
        assert "7" in message and "6" in message, message
    assert result["calls"] == []


@pytest.mark.parametrize("runtime", RUNTIMES)
def test_runtime_workflow_reports_call_accounting(
    request: pytest.FixtureRequest, runtime: str
) -> None:
    probe = _probe(request, runtime)

    success = probe.run()["run"]
    assert success["status"] == "completed", success
    assert success["value"]["agent_calls_planned"] == 7
    assert success["value"]["agent_calls_made"] == 7
    assert success["value"]["max_agent_calls"] == 7

    # setup, two executes, one grade (the failed arm is not graded), no validate, no aggregate:
    # four calls. OSC-18 enumerates exactly these calls; its stated total of 5 is arithmetic.
    failure = probe.run(scenario="explicit-failure")
    assert failure["run"]["status"] == "completed", failure["run"]
    assert failure["run"]["value"]["agent_calls_planned"] == 7
    assert failure["run"]["value"]["agent_calls_made"] == 4
    assert failure["run"]["value"]["max_agent_calls"] == 7
    # The two executes run concurrently, so compare as a set of labels.
    assert sorted(call["label"] for call in failure["calls"]) == sorted(
        ["setup", EXECUTE_WITH, EXECUTE_WITHOUT, GRADE_WITH]
    )

    setup_failure = probe.run(scenario="setup-null")
    assert setup_failure["run"]["status"] == "completed", setup_failure["run"]
    assert setup_failure["run"]["value"]["agent_calls_planned"] == 7
    assert setup_failure["run"]["value"]["agent_calls_made"] == 1
    assert setup_failure["run"]["value"]["max_agent_calls"] == 7


_RUNTIME_GUARD_SCENARIOS = {
    "pi-subagents": [
        "success",
        "explicit-failure",
        "schema-null",
        "spawn-failure",
        "setup-null",
        "setup-campaign-root",
        "validation-failure",
    ],
    "pi-dynamic-workflows": [
        "success",
        "explicit-failure",
        "null-child",
        "recoverable-throw",
        "thrown-child",
        "setup-null",
        "setup-campaign-root",
        "validation-failure",
    ],
}


@pytest.mark.parametrize(
    ("runtime", "scenario"),
    [
        pytest.param(runtime, scenario, id=f"{runtime}-{scenario}")
        for runtime, scenarios in _RUNTIME_GUARD_SCENARIOS.items()
        for scenario in scenarios
    ],
)
def test_runtime_workflow_host_never_sees_more_than_max_agent_calls_spawns(
    request: pytest.FixtureRequest, runtime: str, scenario: str
) -> None:
    """Behavioral variant of the runtime guard: spawns observed by the host stay within the bound."""
    probe = _probe(request, runtime).run(scenario=scenario)
    assert probe["run"]["status"] == "completed", probe["run"]
    value = probe["run"]["value"]
    assert value["max_agent_calls"] == 7
    assert value["agent_calls_made"] == len(probe["calls"])
    assert len(probe["calls"]) <= value["max_agent_calls"]
    assert value["agent_calls_planned"] <= value["max_agent_calls"]
    # Nothing is bounded by the runtime guard here; a failed setup bounds every run by
    # design, whether it failed by returning nothing or by breaking the path contract.
    setup_failed = scenario.startswith("setup-")
    assert value["status_counts"]["bounded"] == (value["expected_runs"] if setup_failed else 0)


def test_runtime_workflow_never_exceeds_max_agent_calls_at_runtime(skill_root: Path) -> None:
    """The runtime guard lives in `safeAgent()` and nowhere else.

    No argument set makes the planning count and the runtime count diverge, so the guard
    is proven at the source level: `safeAgent()` increments the counter before `agent()`
    and returns a `bounded` status on overflow, and no other function touches the counter.
    """
    source = _source(skill_root)
    body = _function_body(source, "safeAgent")

    increment = body.index("agentCallsMade += 1")
    call = body.index("agent(")
    assert increment < call, "the counter must move before agent() is called"
    bounded = body.index("status: 'bounded'")
    assert bounded < call, "the bounded return must precede the agent() call"
    assert "agentCallsMade + 1 > maxAgentCalls" in body or "agentCallsMade >= maxAgentCalls" in body
    assert "max_agent_calls" in body and "reached" in body

    # The counter is declared once at the top level, mutated only inside safeAgent(), and
    # otherwise only read into the returned object.
    assert source.count("let agentCallsMade = 0") == 1
    mutations = re.findall(r"(?<!let )agentCallsMade\s*(?:\+=|-=|=)(?!=)", source)
    assert len(mutations) == 1, mutations
    outside = source.replace(body, "")
    assert "agentCallsMade +=" not in outside
    assert "agentCallsMade =" not in outside.replace("let agentCallsMade = 0", "")
    for other in ("executeItem", "gradeItem", "runtimeAgentOptions", "countFailure"):
        assert "agentCallsMade" not in _function_body(source, other), other
    assert source.count("agent_calls_made: agentCallsMade") == 2


@pytest.mark.parametrize("runtime", RUNTIMES)
def test_runtime_workflow_validation_failure_skips_aggregation(
    request: pytest.FixtureRequest, runtime: str
) -> None:
    probe = _probe(request, runtime).run(scenario="validation-failure")
    assert probe["run"]["status"] == "completed", probe["run"]
    value = probe["run"]["value"]
    labels = [call["label"] for call in probe["calls"]]

    assert value["valid"] is False
    assert value["status_counts"] == {"completed": 2, "failed": 0, "skipped": 0, "bounded": 0}
    assert value["failure_kinds"] == {"null_result": 0, "thrown": 0, "explicit": 1, "contract": 0}
    assert value["stage_statuses"] == {"setup": "completed", "validation": "failed", "aggregation": "bounded"}
    assert "benchmark_json" not in value["durable_paths"]
    assert labels.count("validate") == 1 and "aggregate" not in labels


@pytest.mark.parametrize("runtime", RUNTIMES)
def test_runtime_workflow_is_resume_safe_and_deterministic(
    request: pytest.FixtureRequest, runtime: str
) -> None:
    probe = _probe(request, runtime).run(resume=True)
    assert probe["run"]["status"] == "completed", probe["run"]
    assert probe["replay"]["status"] == "completed", probe["replay"]
    assert probe["replay"]["spawned"] == 0
    assert probe["replay"]["agentCount"] == probe["run"]["agentCount"]
    if runtime == "pi-subagents":
        assert probe["replay"]["replayedCount"] == probe["run"]["agentCount"]
    else:
        assert probe["replay"]["journaled"] == probe["run"]["agentCount"]
        # A replay spends nothing, so `budget.spent()` is the one field allowed to differ.
        first = json.loads(json.dumps(probe["run"]["value"]))
        second = json.loads(json.dumps(probe["replay"]["value"]))
        assert first["telemetry"]["workflow_output_tokens"] > 0
        assert second["telemetry"]["workflow_output_tokens"] == 0
        first["telemetry"].pop("workflow_output_tokens")
        second["telemetry"].pop("workflow_output_tokens")
        assert first == second


@pytest.mark.parametrize("args_runtime", RUNTIMES)
def test_runtime_workflow_prompt_sequence_is_runtime_independent(
    request: pytest.FixtureRequest, args_runtime: str
) -> None:
    """The same args produce the same ordered (label, prompt) sequence on both runtimes.

    Neither the stub host nor the injected runner interprets model strings, so feeding
    one runtime the other runtime's args is legitimate here: it isolates the executing
    runtime as the only variable.
    """
    args = _args(args_runtime)
    observed = {
        runtime: [
            (call["label"], call["prompt"])
            for call in _probe(request, runtime).run(args=args)["calls"]
        ]
        for runtime in RUNTIMES
    }
    assert observed["pi-subagents"] == observed["pi-dynamic-workflows"]
    assert len(observed["pi-subagents"]) == 7


def _function_body(source: str, name: str) -> str:
    start = source.index(f"function {name}(")
    open_brace = source.index("{", start)
    depth = 0
    for index in range(open_brace, len(source)):
        if source[index] == "{":
            depth += 1
        elif source[index] == "}":
            depth -= 1
            if depth == 0:
                return source[open_brace : index + 1]
    raise AssertionError(f"unterminated function {name}")


def test_runtime_workflow_source_uses_only_the_shared_subset(skill_root: Path) -> None:
    source = _source(skill_root)
    shim = _function_body(source, "runtimeAgentOptions")

    assert "whenToUse" not in source
    assert "detail:" not in source
    for forbidden in (
        "gate:",
        "agentType:",
        "resume:",
        "isolation:",
        "tier:",
        "thread:",
        "timeoutMs:",
        "retries:",
        "Date.now",
        "Math.random",
        "new Date()",
        "require(",
        "import ",
        "fetch(",
        "XMLHttpRequest",
        "--skill-name",
        ".filter(Boolean)",
    ):
        assert forbidden not in source, forbidden
    assert re.search(r"[0-9a-f]{40}", source) is None, "no revision literal in the script"

    # The call bound is a required argument, planned before the first call, and reported.
    assert "maxAgentCalls" in source
    assert source.index("agentCallsPlanned") < source.index("phase('Prepare')")
    for reported in ("agent_calls_planned", "agent_calls_made", "max_agent_calls"):
        assert source.count(f"{reported}:") == 2, reported

    # `effort:` and the `:thinking` model suffix exist only inside the shim.
    assert source.count("effort:") == shim.count("effort:") >= 1
    assert source.count(":${role.thinking}") == shim.count(":${role.thinking}") == 1
    assert "'pi-subagents'" in shim and "'pi-dynamic-workflows'" in source

    # Every child goes through safeAgent(); agent() is called nowhere else in code.
    code = "\n".join(line for line in source.splitlines() if not line.lstrip().startswith("//"))
    assert len(re.findall(r"(?<![A-Za-z0-9_])agent\(", code)) == 1
    assert source.count("safeAgent(") >= 5
    assert "await pipeline(" in source
    assert "runtimeAgentOptions(" in source


def test_benchmark_contract_prose_matches_runtime(skill_root: Path) -> None:
    skill = (skill_root / "SKILL.md").read_text(encoding="utf-8")
    prose = (skill_root / "references/benchmarking.md").read_text(encoding="utf-8")

    assert "${PI_SKILL_DIR}/references/schemas.md" in skill
    assert "${PI_SKILL_DIR}/workflows/benchmark.js" in prose
    assert "scriptPath" in prose
    assert "with_skill" in prose and "without_skill" in prose
    assert "expectations" in prose
    assert "viewer.pid" in prose
    assert "--report none" in prose
    for stale in ("assertions", "baseline/outputs", "clean-slate", "policy-level"):
        assert stale not in prose.lower()

    # Both runtimes, the preflight, and the runtime-aware campaign record.
    for required in (
        "SubagentWorkflow",
        "pi-dynamic-workflows",
        "`workflow`",
        "runtime: pi-subagents",
        "runtime: pi-dynamic-workflows",
        "runtimeCheckout",
        "resumeFromRunId",
        "workflow_runtime",
        "--validate-only",
        PI_SUBAGENTS_REVISION,
        PI_DYNAMIC_WORKFLOWS_REVISION,
    ):
        assert required in prose, required
    aggregate_block = prose.split("python -m scripts.aggregate_benchmark", 1)[1].split("```", 1)[0]
    assert "--skill-name" not in aggregate_block

    step_seven = skill.split("## Step 7", 1)[1].split("\n## ", 1)[0]
    for required in ("SubagentWorkflow", "`workflow`", "pi-dynamic-workflows", "scriptPath", "script"):
        assert required in step_seven, required
    assert PI_SUBAGENTS_REVISION[:12] in step_seven or PI_SUBAGENTS_REVISION in step_seven
    assert PI_DYNAMIC_WORKFLOWS_REVISION[:12] in step_seven or PI_DYNAMIC_WORKFLOWS_REVISION in step_seven

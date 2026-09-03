"""Contract tests for the deterministic runtime benchmark workflow."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any

import pytest

from conftest import PI_SUBAGENTS_REVISION, verify_checkout_revision

FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures/workflow"

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
const labels = new Map();
const campaignRoot = `${input.args.projectRoot}/.skill-creator/example-skill/campaign-${input.args.campaignId}`;
const iterationRoot = `${campaignRoot}/iteration-${input.args.iteration}`;

function responseFor(label) {
  if (label === "setup") return {
    status: "completed",
    campaign_path: `${campaignRoot}/campaign.json`,
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
  if (label === "aggregate") return {
    status: "completed",
    benchmark_json_path: `${iterationRoot}/benchmark.json`,
    benchmark_markdown_path: `${iterationRoot}/benchmark.md`,
  };
  if (label === "benchmark-analysis") return {
    status: "completed",
    analysis_path: `${iterationRoot}/benchmark-analysis.json`,
    effective_model: "fixture/analyzer-effective",
    effective_thinking: "medium",
  };
  throw new Error(`unexpected label ${label}`);
}

function hostFor(scenario, spawnCount) {
  return {
    async spawnAgent(request) {
      calls.push({
        label: request.label,
        phase: request.phaseTitle,
        agentType: request.agentType,
        model: request.model,
        effort: request.effort,
        gate: request.gate,
      });
      labels.set(request.agentId, request.label);
      spawnCount.count += 1;
      if (scenario === "setup-null" && request.label === "setup") {
        return { ok: false, error: "fixture setup failure" };
      }
      if (scenario === "schema-null" && request.label.startsWith("execute:") && request.label.includes("without_skill")) {
        return { ok: true, text: "{}", outputTokens: 7 };
      }
      return { ok: true, text: JSON.stringify(responseFor(request.label)), outputTokens: 7 };
    },
    abortAgent() {},
    async runGate(_command, gate) {
      const label = labels.get(gate.agentId);
      return scenario === "gate-null" && label?.startsWith("execute:") && label.includes("without_skill")
        ? { ok: false, output: "fixture gate failure" }
        : { ok: true, output: "" };
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
process.stdout.write(JSON.stringify({ meta: parsedMeta, run, replay, calls }));
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


def _args() -> dict[str, Any]:
    return json.loads((FIXTURE_ROOT / "valid-args.json").read_text(encoding="utf-8"))


def _probe(
    skill_root: Path,
    runtime_root: Path,
    *,
    args: dict[str, Any] | None = None,
    scenario: str = "success",
    resume: bool = False,
) -> dict[str, Any]:
    workflow = skill_root / "workflows/benchmark.js"
    assert workflow.is_file(), "workflows/benchmark.js must exist"
    result = subprocess.run(
        ["node", "-e", _NODE_PROBE],
        input=json.dumps(
            {
                "runtimeRoot": os.fspath(runtime_root),
                "source": workflow.read_text(encoding="utf-8"),
                "args": args or _args(),
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


def test_runtime_workflow_fails_closed_and_pipelines_execution_into_grading(
    skill_root: Path,
    workflow_runtime_modules: Path,
) -> None:
    probe = _probe(skill_root, workflow_runtime_modules)
    assert "value" in probe["run"], probe
    value = probe["run"]["value"]
    labels = [call["label"] for call in probe["calls"]]

    assert probe["meta"]["name"] == "opin-skill-creator-benchmark"
    assert probe["run"]["status"] == "completed"
    assert value["valid"] is True
    assert value["status_counts"] == {
        "completed": 2,
        "failed": 0,
        "skipped": 0,
        "bounded": 0,
        "null": 0,
    }
    assert labels.count("execute:runtime-behavior:with_skill:run-1") == 1
    assert labels.count("execute:runtime-behavior:without_skill:run-1") == 1
    assert labels.count("grade:runtime-behavior:with_skill:run-1") == 1
    assert labels.count("grade:runtime-behavior:without_skill:run-1") == 1
    assert labels.index("grade:runtime-behavior:with_skill:run-1") > labels.index(
        "execute:runtime-behavior:with_skill:run-1"
    )
    assert all(call["gate"] for call in probe["calls"])


@pytest.mark.parametrize(
    ("scenario", "expected_count"),
    [
        ("explicit-failure", "failed"),
        ("schema-null", "null"),
        ("gate-null", "null"),
    ],
)
def test_runtime_workflow_accounts_for_failed_and_null_items(
    skill_root: Path,
    workflow_runtime_modules: Path,
    scenario: str,
    expected_count: str,
) -> None:
    value = _probe(skill_root, workflow_runtime_modules, scenario=scenario)["run"]["value"]
    assert value["valid"] is False
    assert value["status_counts"][expected_count] == 1
    assert sum(value["status_counts"].values()) == value["expected_runs"]
    assert "benchmark_json" not in value["durable_paths"]


def test_runtime_workflow_refuses_missing_approval_and_setup_failure(
    skill_root: Path,
    workflow_runtime_modules: Path,
) -> None:
    args = _args()
    args["approved"] = False
    refused = _probe(skill_root, workflow_runtime_modules, args=args)["run"]
    assert refused["status"] == "failed"
    assert "approved" in refused["error"].lower()

    setup_failure = _probe(
        skill_root, workflow_runtime_modules, scenario="setup-null"
    )["run"]["value"]
    assert setup_failure["valid"] is False
    assert setup_failure["status_counts"]["bounded"] == 2
    assert setup_failure["status_counts"]["null"] == 0


def test_runtime_workflow_is_resume_safe_and_deterministic(
    skill_root: Path, workflow_runtime_modules: Path
) -> None:
    probe = _probe(skill_root, workflow_runtime_modules, resume=True)
    assert probe["run"]["status"] == "completed"
    assert probe["replay"]["status"] == "completed"
    assert probe["replay"]["replayedCount"] == probe["run"]["agentCount"]
    assert probe["replay"]["spawned"] == 0

    source = (skill_root / "workflows/benchmark.js").read_text(encoding="utf-8")
    for forbidden in (
        "Date.now(",
        "Math.random(",
        "new Date()",
        "require(",
        "import ",
        "fetch(",
        "XMLHttpRequest",
    ):
        assert forbidden not in source
    assert "await pipeline(" in source
    assert ".filter(Boolean)" not in source


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

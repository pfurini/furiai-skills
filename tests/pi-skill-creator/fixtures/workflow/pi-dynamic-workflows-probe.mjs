// Executes workflows/benchmark.js through pinned pi-dynamic-workflows `runWorkflow`
// with an injected agent runner. Run with `<checkout>/node_modules/.bin/tsx` so the
// TypeScript sources import directly; no model, filesystem log, or agent registry
// is touched. Reads one JSON object from stdin:
//   { checkout, source, args, scenario, resume, cwd }
// and prints { meta, run, replay, calls } so the Python side sees the same shape
// the pi-subagents stub-host probe produces.
import { pathToFileURL } from "node:url";

let stdin = "";
for await (const chunk of process.stdin) stdin += chunk;
const input = JSON.parse(stdin);
const moduleUrl = (name) => pathToFileURL(`${input.checkout}/src/${name}.ts`).href;
const { runWorkflow } = await import(moduleUrl("workflow"));
const { WorkflowError, WorkflowErrorCode } = await import(moduleUrl("errors"));

const campaignRoot = `${input.args.projectRoot}/.skill-creator/example-skill/campaign-${input.args.campaignId}`;
const iterationRoot = `${campaignRoot}/iteration-${input.args.iteration}`;
const calls = [];

function responseFor(label) {
  if (label === "setup") {
    return {
      status: "completed",
      // `setup-campaign-root` reproduces the OSC-14 smoke failure: the child returned
      // the campaign directory where the contract requires the campaign.json file.
      campaign_path: input.scenario === "setup-campaign-root"
        ? campaignRoot
        : `${campaignRoot}/campaign.json`,
      evals_path: `${campaignRoot}/evals.json`,
    };
  }
  if (label.startsWith("execute:")) {
    const [, evalName, configuration, runPart] = label.split(":");
    const runRoot = `${iterationRoot}/${evalName}/${configuration}/${runPart}`;
    return {
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
  if (label === "validate") return { status: "completed" };
  if (label === "aggregate") {
    return {
      status: "completed",
      benchmark_json_path: `${iterationRoot}/benchmark.json`,
      benchmark_markdown_path: `${iterationRoot}/benchmark.md`,
    };
  }
  throw new Error(`unexpected label ${label}`);
}

function isControlExecution(label) {
  return label.startsWith("execute:") && label.includes("without_skill");
}

function runnerFor(scenario, counter) {
  return {
    async run(prompt, options) {
      const label = options.label;
      calls.push({
        label,
        prompt,
        model: options.model,
        keys: Object.keys(options).sort(),
      });
      counter.count += 1;
      if (scenario === "setup-null" && label === "setup") return null;
      if (scenario === "validation-failure" && label === "validate") {
        return { status: "failed", error: "fixture validation failure" };
      }
      if (isControlExecution(label)) {
        if (scenario === "explicit-failure") return { status: "failed", error: "fixture executor failure" };
        if (scenario === "null-child") return null;
        if (scenario === "recoverable-throw") {
          // recoverable: true must be explicit; it makes agent() return null.
          throw new WorkflowError("fixture empty output", WorkflowErrorCode.AGENT_EMPTY_OUTPUT, {
            recoverable: true,
          });
        }
        if (scenario === "thrown-child") {
          // recoverable: false makes agent() throw into the script.
          throw new WorkflowError("fixture schema noncompliance", WorkflowErrorCode.SCHEMA_NONCOMPLIANCE, {
            recoverable: false,
          });
        }
      }
      return responseFor(label);
    },
  };
}

function runOptions(runner, extra) {
  return {
    args: input.args,
    agent: runner,
    concurrency: 4,
    persistLogs: false,
    runId: "osc17-probe",
    agentRegistry: new Map(),
    cwd: input.cwd,
    ...extra,
  };
}

const counter = { count: 0 };
let run;
let replay;
const journal = [];
try {
  const first = await runWorkflow(
    input.source,
    runOptions(runnerFor(input.scenario, counter), {
      onAgentJournal: (entry) => journal.push(entry),
    }),
  );
  run = { status: "completed", value: first.result, agentCount: first.agentCount, meta: first.meta };
  if (input.resume) {
    const before = counter.count;
    const second = await runWorkflow(
      input.source,
      runOptions(runnerFor("success", counter), {
        resumeJournal: new Map(journal.map((entry) => [`${entry.runId}:${entry.index}`, entry])),
      }),
    );
    replay = {
      status: "completed",
      value: second.result,
      agentCount: second.agentCount,
      spawned: counter.count - before,
      journaled: journal.length,
    };
  }
} catch (error) {
  run = {
    status: "threw",
    error: String(error && error.message !== undefined ? error.message : error),
    code: error && error.code !== undefined ? error.code : null,
  };
}
process.stdout.write(JSON.stringify({ meta: run.meta ?? null, run, replay, calls }));

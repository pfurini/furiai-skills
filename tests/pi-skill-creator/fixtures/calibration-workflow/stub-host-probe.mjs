// Executes a repository-development workflow (.pi/workflows/*.js) through the
// pinned pi-subagents runtime with a stub host. No model, session, git, or gate
// command is touched: `spawnAgent` answers from a fixture table and `runGate`
// records the command it was handed. Reads one JSON object from stdin:
//   { runtimeRoot, source, args, responses, prefixResponses, nullLabels, gateFailures }
// where `responses` maps an exact label to the structured object the child
// returns, `prefixResponses` maps a label prefix to one, `nullLabels` lists
// labels whose spawn fails, and `gateFailures` lists substrings of a gate
// command that make the stub gate fail. A string value equal to "${label}"
// inside a response is replaced by the child's label. Prints
//   { meta, run, calls, gateCalls }.
import { pathToFileURL } from "node:url";

let stdin = "";
for await (const chunk of process.stdin) stdin += chunk;
const input = JSON.parse(stdin);
const moduleUrl = (name) => pathToFileURL(`${input.runtimeRoot}/${name}.js`).href;
const { extractMeta } = await import(moduleUrl("meta"));
const { runWorkflow } = await import(moduleUrl("runtime"));

const responses = input.responses ?? {};
const prefixResponses = input.prefixResponses ?? {};
const nullLabels = new Set(input.nullLabels ?? []);
const gateFailures = input.gateFailures ?? [];
const calls = [];
const gateCalls = [];

function templated(value, label) {
  if (value === "${label}") return label;
  if (Array.isArray(value)) return value.map((item) => templated(item, label));
  if (value && typeof value === "object") {
    return Object.fromEntries(Object.entries(value).map(([key, item]) => [key, templated(item, label)]));
  }
  return value;
}

function responseFor(label) {
  if (Object.prototype.hasOwnProperty.call(responses, label)) return responses[label];
  for (const [prefix, response] of Object.entries(prefixResponses)) {
    if (label.startsWith(prefix)) return response;
  }
  return undefined;
}

const host = {
  async spawnAgent(request) {
    calls.push({
      index: request.index,
      label: request.label,
      prompt: request.prompt,
      phaseTitle: request.phaseTitle,
      agentType: request.agentType,
      model: request.model,
      effort: request.effort,
      gate: request.gate,
      isolation: request.isolation,
    });
    if (nullLabels.has(request.label)) return { ok: false, error: `fixture failure for ${request.label}` };
    const response = responseFor(request.label);
    if (response === undefined) return { ok: false, error: `no fixture response for ${request.label}` };
    return { ok: true, text: JSON.stringify(templated(response, request.label)), outputTokens: 3 };
  },
  abortAgent() {},
  async runGate(command, gate) {
    gateCalls.push({ command, agentId: gate.agentId });
    const failure = gateFailures.find((needle) => command.includes(needle));
    if (failure !== undefined) return { ok: false, output: `fixture gate failure: ${failure}` };
    return { ok: true, output: "" };
  },
};

let meta = null;
let run;
try {
  meta = extractMeta(input.source).meta;
  run = await runWorkflow({ script: input.source, args: input.args, host, concurrency: 4 });
} catch (error) {
  run = { status: "threw", error: String(error && error.message !== undefined ? error.message : error) };
}
process.stdout.write(JSON.stringify({ meta, run, calls, gateCalls }));

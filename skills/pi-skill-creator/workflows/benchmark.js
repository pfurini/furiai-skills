export const meta = {
  name: 'pi-skill-creator-benchmark',
  description: 'Run an approved, deterministic with-skill versus without-skill benchmark campaign',
  phases: [
    { title: 'Prepare' },
    { title: 'Execute' },
    { title: 'Grade' },
    { title: 'Validate' },
    { title: 'Aggregate' },
  ],
}

// This script runs unchanged on pi-subagents (SubagentWorkflow) and on
// pi-dynamic-workflows (workflow). It uses only the subset both runtimes
// implement: phase(), agent(), parallel(), pipeline(), log(), args, and
// budget.spent(). The single place that knows the runtimes differ is
// runtimeAgentOptions() below.

const IDENTIFIER = /^[a-z0-9][a-z0-9-]{0,63}$/
const UTC_TIMESTAMP = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/
// A requested model is provider/id with no thinking suffix; the shim adds one where needed.
const MODEL = /^[^/\s:]+\/[^\s:]+$/
const EFFECTIVE_MODEL = /^[^/\s]+\/[^\s]+$/
const PROFILES = ['in-situ', 'hermetic-core', 'declared-dependencies']
const RUNTIMES = ['pi-subagents', 'pi-dynamic-workflows']
// Requested levels are the closed set both runtimes can express; `off` is refused
// because pi-subagents cannot request it through `effort`. A model may still clamp
// thinking to off, so the effective-value checks accept it.
const REQUESTED_THINKING = ['minimal', 'low', 'medium', 'high', 'xhigh', 'max']
const EFFECTIVE_THINKING = ['off', ...REQUESTED_THINKING]
const CONFIGURATIONS = ['with_skill', 'without_skill']
const RESULT_STATUSES = ['completed', 'failed', 'skipped', 'bounded']
const FAILURE_KINDS = ['null_result', 'thrown', 'explicit', 'contract']
const MAX_SCHEDULED_RUNS = 128
const ERROR_BOUND = 500

const SETUP_SCHEMA = {
  type: 'object',
  properties: {
    status: { type: 'string', enum: RESULT_STATUSES },
    error: { type: 'string' },
    campaign_path: { type: 'string' },
    evals_path: { type: 'string' },
  },
  required: ['status'],
  additionalProperties: false,
}

const EXECUTION_SCHEMA = {
  type: 'object',
  properties: {
    status: { type: 'string', enum: RESULT_STATUSES },
    error: { type: 'string' },
    run_path: { type: 'string' },
    transcript_metrics_path: { type: 'string' },
    outputs_path: { type: 'string' },
    timing_path: { type: 'string' },
    effective_model: { type: 'string' },
    effective_thinking: { type: 'string' },
  },
  required: ['status'],
  additionalProperties: false,
}

const GRADING_SCHEMA = {
  type: 'object',
  properties: {
    status: { type: 'string', enum: RESULT_STATUSES },
    error: { type: 'string' },
    grading_path: { type: 'string' },
    effective_model: { type: 'string' },
    effective_thinking: { type: 'string' },
  },
  required: ['status'],
  additionalProperties: false,
}

const VALIDATION_SCHEMA = {
  type: 'object',
  properties: {
    status: { type: 'string', enum: RESULT_STATUSES },
    error: { type: 'string' },
  },
  required: ['status'],
  additionalProperties: false,
}

const AGGREGATION_SCHEMA = {
  type: 'object',
  properties: {
    status: { type: 'string', enum: RESULT_STATUSES },
    error: { type: 'string' },
    benchmark_json_path: { type: 'string' },
    benchmark_markdown_path: { type: 'string' },
  },
  required: ['status'],
  additionalProperties: false,
}

function fail(message) {
  throw new Error(`Invalid benchmark workflow args: ${message}`)
}

function requiredObject(value, label) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) fail(`${label} must be an object`)
  return value
}

function requiredText(value, label) {
  if (typeof value !== 'string' || value.trim() === '') fail(`${label} must be a non-empty string`)
  return value
}

function absolutePath(value, label) {
  const path = requiredText(value, label)
  if (!path.startsWith('/') && !/^[A-Za-z]:[\\/]/.test(path)) fail(`${label} must be absolute`)
  return path.replace(/[\\/]+$/, '')
}

function roleConfig(roles, name) {
  const role = requiredObject(roles[name], `roles.${name}`)
  const model = requiredText(role.model, `roles.${name}.model`)
  const thinking = requiredText(role.thinking, `roles.${name}.thinking`)
  if (!MODEL.test(model)) fail(`roles.${name}.model must use provider/model form without a thinking suffix`)
  if (!REQUESTED_THINKING.includes(thinking)) {
    fail(`roles.${name}.thinking must be one of ${REQUESTED_THINKING.join(', ')}; off is not portable across runtimes`)
  }
  return { model, thinking }
}

function shellQuote(value) {
  return `'${String(value).replace(/'/g, `'"'"'`)}'`
}

function samePath(actual, expected) {
  return typeof actual === 'string' && actual === expected
}

function boundedMessage(error) {
  const text = error && typeof error === 'object' && typeof error.message === 'string'
    ? error.message
    : String(error)
  return text.length > ERROR_BOUND ? text.slice(0, ERROR_BOUND) : text
}

function completedExecution(result, paths) {
  return result.status === 'completed'
    && samePath(result.run_path, paths.run)
    && samePath(result.transcript_metrics_path, paths.metrics)
    && samePath(result.outputs_path, paths.outputs)
    && samePath(result.timing_path, paths.timing)
    && typeof result.effective_model === 'string'
    && EFFECTIVE_MODEL.test(result.effective_model)
    && typeof result.effective_thinking === 'string'
    && EFFECTIVE_THINKING.includes(result.effective_thinking)
}

function completedGrading(result, gradingPath) {
  return result.status === 'completed'
    && samePath(result.grading_path, gradingPath)
    && typeof result.effective_model === 'string'
    && EFFECTIVE_MODEL.test(result.effective_model)
    && typeof result.effective_thinking === 'string'
    && EFFECTIVE_THINKING.includes(result.effective_thinking)
}

const input = requiredObject(args, 'args')
if (input.approved !== true) fail('approved must be true after explicit user approval')

const runtime = requiredText(input.runtime, 'runtime')
if (!RUNTIMES.includes(runtime)) fail(`runtime must be one of ${RUNTIMES.join(', ')}`)
const campaignId = requiredText(input.campaignId, 'campaignId')
if (!IDENTIFIER.test(campaignId)) fail('campaignId is invalid')
const createdAt = requiredText(input.createdAt, 'createdAt')
if (!UTC_TIMESTAMP.test(createdAt)) fail('createdAt must be a caller-supplied UTC timestamp')
const projectRoot = absolutePath(input.projectRoot, 'projectRoot')
const skillPath = absolutePath(input.skillPath, 'skillPath')
const skillCreatorPath = absolutePath(input.skillCreatorPath, 'skillCreatorPath')
const piExecutable = absolutePath(input.piExecutable, 'piExecutable')
const piCheckout = absolutePath(input.piCheckout, 'piCheckout')
const piSubagentsCheckout = absolutePath(input.piSubagentsCheckout, 'piSubagentsCheckout')
const runtimeCheckout = absolutePath(input.runtimeCheckout, 'runtimeCheckout')
if (runtime === 'pi-subagents' && runtimeCheckout !== piSubagentsCheckout) {
  fail('runtimeCheckout must equal piSubagentsCheckout when runtime is pi-subagents')
}
const environmentProfile = requiredText(input.environmentProfile, 'environmentProfile')
if (!PROFILES.includes(environmentProfile)) fail('environmentProfile is unsupported')
if (!Number.isInteger(input.iteration) || input.iteration < 1) fail('iteration must be a positive integer')
if (!Number.isInteger(input.repetitions) || input.repetitions < 1 || input.repetitions > 100) {
  fail('repetitions must be an integer from 1 to 100')
}
if (!Number.isInteger(input.maxAgentCalls) || input.maxAgentCalls < 1) {
  fail('maxAgentCalls must be a positive integer bounding the workflow children of this campaign')
}
if (!Array.isArray(input.evals) || input.evals.length === 0 || input.evals.length > 256) {
  fail('evals must contain from 1 to 256 evaluations')
}

const roles = requiredObject(input.roles, 'roles')
const executorRole = roleConfig(roles, 'executor')
const graderRole = roleConfig(roles, 'grader')
const comparatorRole = roleConfig(roles, 'comparator')
const analyzerRole = roleConfig(roles, 'benchmarkAnalyzer')

const evalIds = new Set()
const evalNames = new Set()
const evaluations = input.evals.map((entry, index) => {
  const evaluation = requiredObject(entry, `evals[${index}]`)
  if (!Number.isInteger(evaluation.eval_id) || evaluation.eval_id < 1) fail(`evals[${index}].eval_id must be positive`)
  const evalName = requiredText(evaluation.eval_name, `evals[${index}].eval_name`)
  if (!IDENTIFIER.test(evalName)) fail(`evals[${index}].eval_name is invalid`)
  const prompt = requiredText(evaluation.prompt, `evals[${index}].prompt`)
  if (!Array.isArray(evaluation.expectations) || evaluation.expectations.length === 0) {
    fail(`evals[${index}].expectations must be a non-empty array`)
  }
  const expectations = evaluation.expectations.map((expectation, expectationIndex) =>
    requiredText(expectation, `evals[${index}].expectations[${expectationIndex}]`))
  if (evalIds.has(evaluation.eval_id)) fail(`eval_id ${evaluation.eval_id} is duplicated`)
  if (evalNames.has(evalName)) fail(`eval_name ${evalName} is duplicated`)
  evalIds.add(evaluation.eval_id)
  evalNames.add(evalName)
  return { eval_id: evaluation.eval_id, eval_name: evalName, prompt, expectations }
})

const skillNameParts = skillPath.replace(/\\/g, '/').split('/').filter(part => part !== '')
const skillName = skillNameParts[skillNameParts.length - 1]
if (!IDENTIFIER.test(skillName)) fail('skillPath basename must be a valid skill name')

const campaignRoot = `${projectRoot}/.skill-creator/${skillName}/campaign-${campaignId}`
const iterationRoot = `${campaignRoot}/iteration-${input.iteration}`
const campaignPath = `${campaignRoot}/campaign.json`
const evalsPath = `${campaignRoot}/evals.json`
const benchmarkJson = `${iterationRoot}/benchmark.json`
const benchmarkMarkdown = `${iterationRoot}/benchmark.md`
const extensionPath = `${piSubagentsCheckout}/src/index.ts`
const expectedRuns = evaluations.length * CONFIGURATIONS.length * input.repetitions
const scheduledRuns = Math.min(expectedRuns, MAX_SCHEDULED_RUNS)

// The mechanical call bound. The exact plan is known before the first call: one setup
// launcher, one execute launcher and one grader per scheduled run, one validate launcher,
// and one aggregate launcher. A plan above the bound is refused here; the runtime guard
// in safeAgent() then makes sure the count never exceeds the bound even if the plan and
// the run diverge. The bound covers workflow children only: the comparator, analyzers,
// and viewer calls made from the top-level session are counted by the caller's manifest,
// and measured RPC executor processes are counted by their run.json records.
const maxAgentCalls = input.maxAgentCalls
const agentCallsPlanned = 1 + 2 * scheduledRuns + 2
if (agentCallsPlanned > maxAgentCalls) {
  fail(`maxAgentCalls ${maxAgentCalls} is below the planned ${agentCallsPlanned} agent calls (1 setup + 2 per scheduled run + 1 validate + 1 aggregate for ${scheduledRuns} scheduled runs)`)
}
let agentCallsMade = 0

// The runtime shim. Every agent() options object is built here from the shared
// keys (label, phase, schema) plus the role's model and thinking. pi-subagents
// takes the thinking level as `effort`; pi-dynamic-workflows takes it only as a
// `:thinking` suffix on `model` and silently drops any other key.
function runtimeAgentOptions(role, options) {
  const shared = { label: options.label, phase: options.phase, schema: options.schema }
  if (runtime === 'pi-subagents') {
    return { ...shared, model: role.model, effort: role.thinking }
  }
  return { ...shared, model: `${role.model}:${role.thinking}` }
}

// The only call site of agent(). A null result and a thrown error both become
// accounted failed items, so a child failure never escapes a pipeline stage on
// either runtime. `failure_kind` is private to this script: every child schema
// forbids additional properties, so a child cannot forge it. The counter moves
// before the call: a call that would exceed maxAgentCalls is never launched and
// comes back as a bounded item, which is not a failure.
async function safeAgent(prompt, options, identity) {
  if (agentCallsMade + 1 > maxAgentCalls) {
    return { status: 'bounded', error: `bounded: ${identity}: max_agent_calls ${maxAgentCalls} reached` }
  }
  agentCallsMade += 1
  let result
  try {
    result = await agent(prompt, options)
  } catch (error) {
    return { status: 'failed', failure_kind: 'thrown', error: `thrown: ${identity}: ${boundedMessage(error)}` }
  }
  if (result === null || result === undefined) {
    return { status: 'failed', failure_kind: 'null_result', error: `null-result: ${identity}` }
  }
  if (typeof result !== 'object' || Array.isArray(result) || typeof result.status !== 'string') {
    return { status: 'failed', failure_kind: 'contract', error: `contract: ${identity}: result is not a status object` }
  }
  if (!RESULT_STATUSES.includes(result.status)) {
    return { status: 'failed', failure_kind: 'contract', error: `contract: ${identity}: unrecognized status ${result.status}` }
  }
  return result
}

function contractFailure(identity, detail) {
  return { status: 'failed', failure_kind: 'contract', error: `contract: ${identity}: ${detail}` }
}

function failureKind(result) {
  if (typeof result.failure_kind === 'string' && FAILURE_KINDS.includes(result.failure_kind)) return result.failure_kind
  return 'explicit'
}

const failureKinds = { null_result: 0, thrown: 0, explicit: 0, contract: 0 }
function countFailure(result) {
  failureKinds[failureKind(result)] += 1
}

const basePaths = {
  campaign_root: campaignRoot,
  campaign_json: campaignPath,
  evals_json: evalsPath,
  iteration_root: iterationRoot,
}
const requestedRoles = {
  executor: executorRole,
  grader: graderRole,
  comparator: comparatorRole,
  benchmark_analyzer: analyzerRole,
}
const campaignNotes = [
  `Comparator ${comparatorRole.model} at ${comparatorRole.thinking} thinking judges blind; for outputs produced by Claude-family executors this comparison is not family-independent.`,
]

function telemetry() {
  return {
    workflow_output_tokens: budget.spent(),
    per_launcher_cost: 'unavailable',
    executor_source: 'rpc-runner-artifacts',
  }
}

phase('Prepare')
log(`benchmark campaign ${campaignId} on ${runtime}: ${expectedRuns} expected runs, ${scheduledRuns} scheduled`)
const setupPrompt = `Prepare one deterministic benchmark campaign without making model calls.
Read ${skillCreatorPath}/references/schemas.md first, then create ${campaignRoot} with the exact campaign tree required by pi-skill-creator.campaign/v1.
Write ${campaignPath} with: campaign_id=${campaignId}, created_at=${createdAt}, skill_name=${skillName}, skill_path=${skillPath}, evaluation_cwd=${projectRoot}, environment_profile=${environmentProfile}, repetitions=${input.repetitions}, treatment=with_skill, control=without_skill, workflow_runtime=${runtime}, and notes=${JSON.stringify(campaignNotes)}.
Read every revision field from git, never from memory, and record each as the lowercase 40-hex string the command prints: repository_revision from git -C ${shellQuote(projectRoot)} rev-parse HEAD; pi_revision from git -C ${shellQuote(piCheckout)} rev-parse HEAD; pi_subagents_revision from git -C ${shellQuote(piSubagentsCheckout)} rev-parse HEAD; workflow_runtime_revision from git -C ${shellQuote(runtimeCheckout)} rev-parse HEAD.
Record declared_extensions as ${JSON.stringify(environmentProfile === 'declared-dependencies' ? [extensionPath] : [])}. Record requested role model/thinking values from this JSON: ${JSON.stringify({ executor: executorRole, grader: graderRole, comparator: comparatorRole, benchmark_analyzer: analyzerRole })}.
Write ${evalsPath}, trigger/train.json, trigger/validation.json, trigger/final-test.json, and trigger/results.json as strict JSON plus LF. Write each ${iterationRoot}/<eval-name>/eval_metadata.json with eval_id, eval_name, prompt, and expectations from: ${JSON.stringify(evaluations)}.
Return status completed with campaign_path and evals_path only after every file is durable. On any error, return failed with a bounded error string.`
const setup = await safeAgent(setupPrompt, runtimeAgentOptions(executorRole, {
  label: 'setup',
  phase: 'Prepare',
  schema: SETUP_SCHEMA,
}), 'setup')

const setupResult = setup.status !== 'completed'
  ? setup
  : (samePath(setup.campaign_path, campaignPath) && samePath(setup.evals_path, evalsPath)
    ? setup
    : contractFailure('setup', 'campaign_path or evals_path did not match the campaign tree'))

if (setupResult.status !== 'completed') {
  countFailure(setupResult)
  log(`setup failed: ${setupResult.error ?? setupResult.status}`)
  return {
    valid: false,
    workflow_runtime: runtime,
    expected_runs: expectedRuns,
    scheduled_runs: 0,
    status_counts: { completed: 0, failed: 0, skipped: 0, bounded: expectedRuns },
    failure_kinds: failureKinds,
    stage_statuses: { setup: 'failed', validation: 'bounded', aggregation: 'bounded' },
    agent_calls_planned: agentCallsPlanned,
    agent_calls_made: agentCallsMade,
    max_agent_calls: maxAgentCalls,
    durable_paths: basePaths,
    requested_roles: requestedRoles,
    effective_roles: { executor: null, grader: null },
    telemetry: telemetry(),
    results: [],
  }
}

const workItems = []
let ordinal = 0
for (const evaluation of evaluations) {
  for (const configuration of CONFIGURATIONS) {
    for (let runNumber = 1; runNumber <= input.repetitions; runNumber += 1) {
      if (ordinal < MAX_SCHEDULED_RUNS) {
        const runRoot = `${iterationRoot}/${evaluation.eval_name}/${configuration}/run-${runNumber}`
        workItems.push({
          ordinal,
          identity: `${evaluation.eval_name}:${configuration}:run-${runNumber}`,
          evaluation,
          configuration,
          runNumber,
          runRoot,
          paths: {
            run: `${runRoot}/run.json`,
            transcript: `${runRoot}/transcript.jsonl`,
            metrics: `${runRoot}/transcript-metrics.json`,
            outputs: `${runRoot}/outputs`,
            timing: `${runRoot}/timing.json`,
            grading: `${runRoot}/grading.json`,
          },
        })
      }
      ordinal += 1
    }
  }
}

const extensionArgument = environmentProfile === 'declared-dependencies'
  ? ` --extension ${shellQuote(extensionPath)}`
  : ''

async function executeItem(item) {
  const command = `cd ${shellQuote(skillCreatorPath)} && printf '%s' ${shellQuote(item.evaluation.prompt)} | python -m scripts.rpc_runner --pi-executable ${shellQuote(piExecutable)} --pi-checkout ${shellQuote(piCheckout)} --evaluation-cwd ${shellQuote(projectRoot)} --skill-path ${shellQuote(skillPath)} --run-dir ${shellQuote(item.runRoot)} --model ${shellQuote(executorRole.model)} --thinking ${shellQuote(executorRole.thinking)} --profile ${shellQuote(environmentProfile)}${extensionArgument} --campaign-id ${shellQuote(campaignId)} --eval-id ${item.evaluation.eval_id} --eval-name ${shellQuote(item.evaluation.eval_name)} --configuration ${shellQuote(item.configuration)} --run-number ${item.runNumber}`
  const execution = await safeAgent(`Run one measured executor through the pi-skill-creator RPC runner.
Execute this exact shell command with bash:
${command}
Do not substitute workflow-child usage for executor telemetry. The executor evidence is only run.json and transcript-metrics.json written by the RPC runner.
Return completed only when the command succeeds and these paths are durable: ${JSON.stringify(item.paths)}. Report effective_model and effective_thinking exactly as run.json records them. On any error, return failed with a bounded error string.`, runtimeAgentOptions(executorRole, {
    label: `execute:${item.identity}`,
    phase: 'Execute',
    schema: EXECUTION_SCHEMA,
  }), `execute:${item.identity}`)
  if (execution.status === 'bounded') {
    return { status: 'bounded', item, execution, grading: null, error: execution.error ?? `execute:${item.identity} was bounded` }
  }
  if (execution.status !== 'completed') {
    return { status: 'failed', failure_kind: failureKind(execution), item, execution, grading: null, error: execution.error ?? `execute:${item.identity} returned ${execution.status}` }
  }
  if (!completedExecution(execution, item.paths)) {
    const failure = contractFailure(`execute:${item.identity}`, 'executor result metadata did not match its durable paths or effective configuration contract')
    return { status: 'failed', failure_kind: failure.failure_kind, item, execution, grading: null, error: failure.error }
  }
  return { status: 'completed', item, execution, grading: null }
}

async function gradeItem(executionResult, item) {
  if (executionResult === null || executionResult === undefined) {
    const failure = contractFailure(`execute:${item.identity}`, 'pipeline stage produced no result')
    return { status: 'failed', failure_kind: failure.failure_kind, item, execution: null, grading: null, error: failure.error }
  }
  if (executionResult.status !== 'completed') return executionResult
  const grading = await safeAgent(`Read ${skillCreatorPath}/agents/grader.md by absolute path and follow it as your role definition.
Grade one completed executor run against every expectation.
expectations: ${JSON.stringify(item.evaluation.expectations)}
transcript_path: ${item.paths.transcript}
transcript_metrics_path: ${item.paths.metrics}
outputs_dir: ${item.paths.outputs}
timing_path: ${item.paths.timing}
grading_path: ${item.paths.grading}
Write one pi-skill-creator.grading/v1 JSON object plus LF to grading_path. Return completed with grading_path and your observed effective model and thinking only after the file is durable. On any error, return failed with a bounded error string.`, runtimeAgentOptions(graderRole, {
    label: `grade:${item.identity}`,
    phase: 'Grade',
    schema: GRADING_SCHEMA,
  }), `grade:${item.identity}`)
  if (grading.status === 'bounded') {
    return { ...executionResult, status: 'bounded', grading, error: grading.error ?? `grade:${item.identity} was bounded` }
  }
  if (grading.status !== 'completed') {
    return { ...executionResult, status: 'failed', failure_kind: failureKind(grading), grading, error: grading.error ?? `grade:${item.identity} returned ${grading.status}` }
  }
  if (!completedGrading(grading, item.paths.grading)) {
    const failure = contractFailure(`grade:${item.identity}`, 'grader result metadata did not match its durable path or effective configuration contract')
    return { ...executionResult, status: 'failed', failure_kind: failure.failure_kind, grading, error: failure.error }
  }
  return { ...executionResult, status: 'completed', grading }
}

const results = await pipeline(
  workItems,
  async (_unused, item) => executeItem(item),
  async (executionResult, item) => gradeItem(executionResult, item),
)

const statusCounts = {
  completed: 0,
  failed: 0,
  skipped: 0,
  bounded: expectedRuns - scheduledRuns,
}
const accountedResults = []
for (let index = 0; index < workItems.length; index += 1) {
  const item = workItems[index]
  let result = results[index]
  if (result === null || result === undefined) {
    const failure = contractFailure(item.identity, 'pipeline produced no result for this item')
    result = { status: 'failed', failure_kind: failure.failure_kind, item, execution: null, grading: null, error: failure.error }
  } else if (!RESULT_STATUSES.includes(result.status)) {
    const failure = contractFailure(item.identity, `unrecognized item status ${result.status}`)
    result = { ...result, status: 'failed', failure_kind: failure.failure_kind, error: failure.error }
  }
  statusCounts[result.status] += 1
  // A bounded item was never launched, so it is not a failure and takes no failure kind.
  if (result.status !== 'completed' && result.status !== 'bounded') countFailure(result)
  accountedResults.push({
    status: result.status,
    eval_id: item.evaluation.eval_id,
    eval_name: item.evaluation.eval_name,
    configuration: item.configuration,
    run_number: item.runNumber,
    run_path: result.execution?.run_path ?? null,
    transcript_metrics_path: result.execution?.transcript_metrics_path ?? null,
    grading_path: result.grading?.grading_path ?? null,
    effective_executor_model: result.execution?.effective_model ?? null,
    effective_executor_thinking: result.execution?.effective_thinking ?? null,
    effective_grader_model: result.grading?.effective_model ?? null,
    effective_grader_thinking: result.grading?.effective_thinking ?? null,
    error: result.error ?? null,
  })
}

const allRunsCompleted = statusCounts.completed === expectedRuns
  && statusCounts.failed === 0
  && statusCounts.skipped === 0
  && statusCounts.bounded === 0
log(`runs accounted: ${JSON.stringify(statusCounts)}; failure kinds: ${JSON.stringify(failureKinds)}`)

let validation = null
if (allRunsCompleted) {
  phase('Validate')
  const validateCommand = `cd ${shellQuote(skillCreatorPath)} && python -m scripts.aggregate_benchmark ${shellQuote(iterationRoot)} --validate-only`
  validation = await safeAgent(`Validate the complete benchmark iteration without writing anything.
Run this exact deterministic command with bash:
${validateCommand}
It validates campaign.json, evals, every run.json, transcript-metrics.json, grading.json, and timing.json, and writes no file. Return completed only when it exits 0. When it exits 2, return failed with the single error line it printed. On any other failure, return failed with a bounded error string. Do not repair, omit, or synthesize records.`, runtimeAgentOptions(executorRole, {
    label: 'validate',
    phase: 'Validate',
    schema: VALIDATION_SCHEMA,
  }), 'validate')
  if (validation.status !== 'completed' && validation.status !== 'bounded') countFailure(validation)
}
const validationCompleted = validation !== null && validation.status === 'completed'

let aggregation = null
if (validationCompleted) {
  phase('Aggregate')
  const aggregateCommand = `cd ${shellQuote(skillCreatorPath)} && python -m scripts.aggregate_benchmark ${shellQuote(iterationRoot)}`
  aggregation = await safeAgent(`Validate and aggregate the complete benchmark campaign.
Run this exact deterministic command with bash:
${aggregateCommand}
Do not repair, omit, or synthesize missing records. Return completed with benchmark_json_path and benchmark_markdown_path only when the command succeeds. On any error, return failed with a bounded error string.`, runtimeAgentOptions(executorRole, {
    label: 'aggregate',
    phase: 'Aggregate',
    schema: AGGREGATION_SCHEMA,
  }), 'aggregate')
  if (aggregation.status === 'completed'
    && !(samePath(aggregation.benchmark_json_path, benchmarkJson) && samePath(aggregation.benchmark_markdown_path, benchmarkMarkdown))) {
    aggregation = contractFailure('aggregate', 'benchmark paths did not match the iteration directory')
  }
  if (aggregation.status !== 'completed' && aggregation.status !== 'bounded') countFailure(aggregation)
}
const aggregationCompleted = aggregation !== null && aggregation.status === 'completed'

const valid = allRunsCompleted && validationCompleted && aggregationCompleted
const durablePaths = valid
  ? { ...basePaths, benchmark_json: benchmarkJson, benchmark_markdown: benchmarkMarkdown }
  : basePaths

const effectiveExecutorModels = []
const effectiveExecutorThinking = []
const effectiveGraderModels = []
const effectiveGraderThinking = []
for (const result of accountedResults) {
  for (const [value, target] of [
    [result.effective_executor_model, effectiveExecutorModels],
    [result.effective_executor_thinking, effectiveExecutorThinking],
    [result.effective_grader_model, effectiveGraderModels],
    [result.effective_grader_thinking, effectiveGraderThinking],
  ]) {
    if (typeof value === 'string' && !target.includes(value)) target.push(value)
  }
}

function stageStatus(result, ran) {
  if (!ran || result === null || result.status === 'bounded') return 'bounded'
  return result.status === 'completed' ? 'completed' : 'failed'
}

return {
  valid,
  workflow_runtime: runtime,
  expected_runs: expectedRuns,
  scheduled_runs: scheduledRuns,
  status_counts: statusCounts,
  failure_kinds: failureKinds,
  stage_statuses: {
    setup: 'completed',
    validation: stageStatus(validation, allRunsCompleted),
    aggregation: stageStatus(aggregation, validationCompleted),
  },
  agent_calls_planned: agentCallsPlanned,
  agent_calls_made: agentCallsMade,
  max_agent_calls: maxAgentCalls,
  durable_paths: durablePaths,
  requested_roles: requestedRoles,
  effective_roles: {
    executor: { models: effectiveExecutorModels, thinking: effectiveExecutorThinking },
    grader: { models: effectiveGraderModels, thinking: effectiveGraderThinking },
  },
  telemetry: telemetry(),
  results: accountedResults,
}

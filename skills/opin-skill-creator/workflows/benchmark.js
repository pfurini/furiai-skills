export const meta = {
  name: 'opin-skill-creator-benchmark',
  description: 'Run an approved, deterministic with-skill versus without-skill benchmark campaign',
  whenToUse: 'Use after the user approves a quantitative benchmark campaign and every runtime input is known.',
  phases: [
    { title: 'Prepare', detail: 'Write deterministic campaign metadata' },
    { title: 'Execute', detail: 'Launch measured Pi RPC runs' },
    { title: 'Grade', detail: 'Grade each completed run without a global barrier' },
    { title: 'Aggregate', detail: 'Validate and aggregate the complete campaign' },
  ],
}

const IDENTIFIER = /^[a-z0-9][a-z0-9-]{0,63}$/
const UTC_TIMESTAMP = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/
const MODEL = /^[^/\s]+\/[^\s]+$/
const PROFILES = ['in-situ', 'hermetic-core', 'declared-dependencies']
const THINKING = ['off', 'minimal', 'low', 'medium', 'high', 'xhigh', 'max']
const CONFIGURATIONS = ['with_skill', 'without_skill']
const RESULT_STATUSES = ['completed', 'failed', 'skipped', 'bounded']
const MAX_SCHEDULED_RUNS = 128

const STATUS_SCHEMA = {
  type: 'object',
  properties: {
    status: { type: 'string', enum: RESULT_STATUSES },
    error: { type: 'string' },
  },
  required: ['status'],
  additionalProperties: true,
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
  if (!MODEL.test(model)) fail(`roles.${name}.model must use provider/model form`)
  if (!THINKING.includes(thinking)) fail(`roles.${name}.thinking is unsupported`)
  return { model, thinking }
}

function shellQuote(value) {
  return `'${String(value).replace(/'/g, `'"'"'`)}'`
}

function samePath(actual, expected) {
  return typeof actual === 'string' && actual === expected
}

function completedExecution(result, paths) {
  return result.status === 'completed'
    && samePath(result.run_path, paths.run)
    && samePath(result.transcript_metrics_path, paths.metrics)
    && samePath(result.outputs_path, paths.outputs)
    && samePath(result.timing_path, paths.timing)
    && typeof result.effective_model === 'string'
    && MODEL.test(result.effective_model)
    && typeof result.effective_thinking === 'string'
    && THINKING.includes(result.effective_thinking)
}

function completedGrading(result, gradingPath) {
  return result.status === 'completed'
    && samePath(result.grading_path, gradingPath)
    && typeof result.effective_model === 'string'
    && MODEL.test(result.effective_model)
    && typeof result.effective_thinking === 'string'
    && THINKING.includes(result.effective_thinking)
}

const input = requiredObject(args, 'args')
if (input.approved !== true) fail('approved must be true after explicit user approval')

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
const environmentProfile = requiredText(input.environmentProfile, 'environmentProfile')
if (!PROFILES.includes(environmentProfile)) fail('environmentProfile is unsupported')
if (!Number.isInteger(input.iteration) || input.iteration < 1) fail('iteration must be a positive integer')
if (!Number.isInteger(input.repetitions) || input.repetitions < 1 || input.repetitions > 100) {
  fail('repetitions must be an integer from 1 to 100')
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
const extensionPath = `${piSubagentsCheckout}/src/index.ts`
const expectedRuns = evaluations.length * CONFIGURATIONS.length * input.repetitions
const scheduledRuns = Math.min(expectedRuns, MAX_SCHEDULED_RUNS)

phase('Prepare')
const setupPrompt = `Prepare one deterministic benchmark campaign without making model calls.
Create ${campaignRoot} with the exact campaign tree required by opin.campaign/v1.
Write campaign metadata to ${campaignPath} using campaign_id=${campaignId}, created_at=${createdAt}, target skill ${skillPath}, evaluation cwd ${projectRoot}, profile ${environmentProfile}, repetitions=${input.repetitions}, Pi revision a4043c1e332a61e4c8648b97b9b796c57f9db110, and pi-subagents revision bfa262fdd75d807b1c6b1f852f1f1bea2bbb3fa4. Obtain repository_revision with git -C ${projectRoot} rev-parse HEAD; never invent it. Record declared extension ${extensionPath} only for declared-dependencies. Record requested role model/thinking values from this JSON: ${JSON.stringify({ executor: executorRole, grader: graderRole, comparator: comparatorRole, benchmark_analyzer: analyzerRole })}.
Write ${evalsPath}, trigger/train.json, trigger/validation.json, trigger/final-test.json, and trigger/results.json as strict JSON plus LF. Write each ${iterationRoot}/<eval-name>/eval_metadata.json with eval_id, eval_name, prompt, and expectations from: ${JSON.stringify(evaluations)}.
Return status completed with campaign_path and evals_path only after every file is durable.`
const setup = await agent(setupPrompt, {
  label: 'setup',
  phase: 'Prepare',
  model: executorRole.model,
  effort: executorRole.thinking,
  schema: {
    ...STATUS_SCHEMA,
    properties: {
      ...STATUS_SCHEMA.properties,
      campaign_path: { type: 'string' },
      evals_path: { type: 'string' },
    },
  },
  gate: `test -f ${shellQuote(campaignPath)} && test -f ${shellQuote(evalsPath)}`,
})

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

if (setup === null || setup.status !== 'completed'
  || !samePath(setup.campaign_path, campaignPath) || !samePath(setup.evals_path, evalsPath)) {
  return {
    valid: false,
    expected_runs: expectedRuns,
    scheduled_runs: 0,
    status_counts: { completed: 0, failed: 0, skipped: 0, bounded: expectedRuns, null: 0 },
    stage_statuses: { setup: setup === null ? 'null' : setup.status, aggregation: 'bounded' },
    durable_paths: basePaths,
    requested_roles: requestedRoles,
    effective_roles: { executor: null, grader: null },
    telemetry: { workflow_output_tokens: budget.spent(), per_launcher_cost: 'unavailable' },
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

const results = await pipeline(
  workItems,
  async (_unused, item) => {
    const identity = `${item.evaluation.eval_name}:${item.configuration}:run-${item.runNumber}`
    const command = `cd ${shellQuote(skillCreatorPath)} && printf '%s' ${shellQuote(item.evaluation.prompt)} | python -m scripts.rpc_runner --pi-executable ${shellQuote(piExecutable)} --pi-checkout ${shellQuote(piCheckout)} --evaluation-cwd ${shellQuote(projectRoot)} --skill-path ${shellQuote(skillPath)} --run-dir ${shellQuote(item.runRoot)} --model ${shellQuote(executorRole.model)} --thinking ${shellQuote(executorRole.thinking)} --profile ${shellQuote(environmentProfile)}${extensionArgument} --campaign-id ${shellQuote(campaignId)} --eval-id ${item.evaluation.eval_id} --eval-name ${shellQuote(item.evaluation.eval_name)} --configuration ${shellQuote(item.configuration)} --run-number ${item.runNumber}`
    const execution = await agent(`Run one measured executor through the opin RPC runner.
Execute this exact shell command with bash:
${command}
Do not substitute workflow-child usage for executor telemetry. The executor evidence is only run.json and transcript-metrics.json written by the RPC runner.
Return completed only when the command succeeds and these paths are durable: ${JSON.stringify(item.paths)}. On any error, return failed with a bounded error string.`, {
      label: `execute:${identity}`,
      phase: 'Execute',
      model: executorRole.model,
      effort: executorRole.thinking,
      schema: EXECUTION_SCHEMA,
      gate: `test -f ${shellQuote(item.paths.run)} && test -f ${shellQuote(item.paths.transcript)} && test -f ${shellQuote(item.paths.metrics)} && test -d ${shellQuote(item.paths.outputs)} && test -f ${shellQuote(item.paths.timing)}`,
    })
    if (execution === null) return null
    if (execution.status !== 'completed') {
      return { status: execution.status, item, execution, grading: null }
    }
    if (!completedExecution(execution, item.paths)) {
      return { status: 'failed', item, execution, grading: null, error: 'executor result metadata did not match its durable paths or effective configuration contract' }
    }
    return { status: 'completed', item, execution, grading: null }
  },
  async (executionResult, item) => {
    if (executionResult === null) return null
    if (executionResult.status !== 'completed') return executionResult
    const identity = `${item.evaluation.eval_name}:${item.configuration}:run-${item.runNumber}`
    const grading = await agent(`Grade one completed executor run against every expectation.
expectations: ${JSON.stringify(item.evaluation.expectations)}
transcript_path: ${item.paths.transcript}
transcript_metrics_path: ${item.paths.metrics}
outputs_dir: ${item.paths.outputs}
timing_path: ${item.paths.timing}
grading_path: ${item.paths.grading}
Write one opin.grading/v1 JSON object plus LF. Return completed with grading_path and your observed effective model and thinking only after the file is durable.`, {
      label: `grade:${identity}`,
      phase: 'Grade',
      agentType: 'grader',
      model: graderRole.model,
      effort: graderRole.thinking,
      schema: GRADING_SCHEMA,
      gate: `python -m json.tool ${shellQuote(item.paths.grading)} > /dev/null && grep -q ${shellQuote('"schema_version": "opin.grading/v1"')} ${shellQuote(item.paths.grading)}`,
    })
    if (grading === null) return null
    if (grading.status !== 'completed') return { ...executionResult, status: grading.status, grading }
    if (!completedGrading(grading, item.paths.grading)) {
      return { ...executionResult, status: 'failed', grading, error: 'grader result metadata did not match its durable path or effective configuration contract' }
    }
    return { ...executionResult, status: 'completed', grading }
  },
)

const statusCounts = {
  completed: 0,
  failed: 0,
  skipped: 0,
  bounded: expectedRuns - scheduledRuns,
  null: 0,
}
const accountedResults = []
for (let index = 0; index < results.length; index += 1) {
  const result = results[index]
  const item = workItems[index]
  if (result === null) {
    statusCounts.null += 1
    accountedResults.push({
      status: 'null',
      eval_id: item.evaluation.eval_id,
      eval_name: item.evaluation.eval_name,
      configuration: item.configuration,
      run_number: item.runNumber,
    })
    continue
  }
  if (!RESULT_STATUSES.includes(result.status)) {
    statusCounts.failed += 1
    accountedResults.push({ status: 'failed', error: 'unrecognized item status' })
    continue
  }
  statusCounts[result.status] += 1
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
    error: result.error ?? result.execution?.error ?? result.grading?.error ?? null,
  })
}

const allRunsCompleted = statusCounts.completed === expectedRuns
  && statusCounts.failed === 0
  && statusCounts.skipped === 0
  && statusCounts.bounded === 0
  && statusCounts.null === 0

let aggregation = null
if (allRunsCompleted) {
  phase('Aggregate')
  const benchmarkJson = `${iterationRoot}/benchmark.json`
  const benchmarkMarkdown = `${iterationRoot}/benchmark.md`
  const aggregateCommand = `cd ${shellQuote(skillCreatorPath)} && python -m scripts.aggregate_benchmark ${shellQuote(iterationRoot)} --skill-name ${shellQuote(skillName)}`
  aggregation = await agent(`Validate and aggregate the complete benchmark campaign.
Run this exact deterministic command with bash:
${aggregateCommand}
Do not repair, omit, or synthesize missing records. Return completed with benchmark_json_path and benchmark_markdown_path only when the command succeeds.`, {
    label: 'aggregate',
    phase: 'Aggregate',
    model: executorRole.model,
    effort: executorRole.thinking,
    schema: AGGREGATION_SCHEMA,
    gate: `test -f ${shellQuote(benchmarkJson)} && test -f ${shellQuote(benchmarkMarkdown)}`,
  })
}

const benchmarkJson = `${iterationRoot}/benchmark.json`
const benchmarkMarkdown = `${iterationRoot}/benchmark.md`
const aggregationCompleted = aggregation !== null
  && aggregation.status === 'completed'
  && samePath(aggregation.benchmark_json_path, benchmarkJson)
  && samePath(aggregation.benchmark_markdown_path, benchmarkMarkdown)
const valid = allRunsCompleted && aggregationCompleted
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

return {
  valid,
  expected_runs: expectedRuns,
  scheduled_runs: scheduledRuns,
  status_counts: statusCounts,
  stage_statuses: {
    setup: 'completed',
    aggregation: !allRunsCompleted ? 'bounded' : aggregation === null ? 'null' : aggregation.status,
  },
  durable_paths: durablePaths,
  requested_roles: requestedRoles,
  effective_roles: {
    executor: { models: effectiveExecutorModels, thinking: effectiveExecutorThinking },
    grader: { models: effectiveGraderModels, thinking: effectiveGraderThinking },
  },
  telemetry: {
    workflow_output_tokens: budget.spent(),
    per_launcher_cost: 'unavailable',
    executor_source: 'rpc-runner-artifacts',
  },
  results: accountedResults,
}

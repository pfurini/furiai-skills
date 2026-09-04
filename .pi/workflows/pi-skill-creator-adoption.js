export const meta = {
  name: 'pi-skill-creator-adoption',
  description: 'Implement the pi-skill-creator adoption work orders through deterministic offline gates, stopping before paid calibration',
  whenToUse: 'Run only after a human approves implementation and supplies the clean handoff-containing HEAD as implementationStartCommit.',
  phases: [
    { title: 'Preflight' },
    { title: 'Foundation' },
    { title: 'Contracts' },
    { title: 'Core' },
    { title: 'Models' },
    { title: 'Execution' },
    { title: 'Doctrine' },
    { title: 'Runtime workflow' },
    { title: 'README' },
  ],
}

const SOURCE_BASELINE = '0b9e86bc77a60fb34039456a6624ea94e396f5d1'
const REQUIRED_PI = '7815e97a0dd5e7eee3cd01858bd5aa0fabeebae0'
const REQUIRED_SUBAGENTS = '7f569969445bf8bc6fbd7757f18db80b35de0ba9'
const PYTEST = "uvx --from 'pytest==9.1.1' pytest"
const TY = "uvx --from 'ty==0.0.77' ty"
// Handoff decision 7: the three list fields have fixed meanings, and every writer and
// integrator prompt states them so a mandated exclusion is never reported as skipped work.
const THREE_FIELD_SEMANTICS = '`tests_skipped` lists intentionally skipped tests only; `bounded_work` lists mandated exclusions only; `skipped_work` lists required work left incomplete and must be `[]` on completion.'
// Historical: the 17 order files the adoption run enumerated. OSC-17 and OSC-18 were added
// later and run standalone, so this list is not extended.
const REQUIRED_HANDOFF_FILES = [
  'docs/pi-skill-creator-work-orders/index.md',
  'docs/pi-skill-creator-work-orders/contracts.md',
  ...Array.from({ length: 17 }, (_, index) => {
    const order = String(index).padStart(2, '0')
    const names = [
      'test-foundation',
      'telemetry-seam',
      'validator-parity',
      'authoring-doctrine',
      'viewer-hardening',
      'aggregation-schemas',
      'bundled-agents',
      'role-model-config',
      'trigger-reliability',
      'optimizer-methodology',
      'rpc-profiles',
      'testing-doctrine',
      'runtime-workflow-docs',
      'readme-deterministic',
      'live-calibration',
      'apply-calibration',
      'directory-distribution',
    ]
    return `docs/pi-skill-creator-work-orders/osc-${order}-${names[index]}.md`
  }),
  '.pi/workflows/pi-skill-creator-adoption.js',
  '.pi/workflows/pi-skill-creator-calibration.js',
]

const HANDOFF = {
  type: 'object',
  properties: {
    order_id: { type: 'string' },
    status: { type: 'string', enum: ['completed'] },
    branch: { type: 'string' },
    commit: { type: 'string' },
    red_observed: { type: 'boolean' },
    tests_passed: { type: 'array', items: { type: 'string' } },
    tests_skipped: { type: 'array', items: { type: 'string' } },
    bounded_work: { type: 'array', items: { type: 'string' } },
    skipped_work: { type: 'array', items: { type: 'string' } },
    owned_paths_changed: { type: 'array', items: { type: 'string' } },
    summary: { type: 'string' },
    blockers: { type: 'array', items: { type: 'string' } },
  },
  required: ['order_id', 'status', 'branch', 'commit', 'red_observed', 'tests_passed', 'tests_skipped', 'bounded_work', 'skipped_work', 'owned_paths_changed', 'summary', 'blockers'],
}

const INTEGRATION = {
  type: 'object',
  properties: {
    status: { type: 'string', enum: ['completed'] },
    commit: { type: 'string' },
    branches: { type: 'array', items: { type: 'string' } },
    tests_passed: { type: 'array', items: { type: 'string' } },
    bounded_work: { type: 'array', items: { type: 'string' } },
    skipped_work: { type: 'array', items: { type: 'string' } },
    summary: { type: 'string' },
  },
  required: ['status', 'commit', 'branches', 'tests_passed', 'bounded_work', 'skipped_work', 'summary'],
}

function requireText(value, name) {
  if (typeof value !== 'string' || value.trim() === '') throw new Error(`${name} must be a non-empty string`)
  return value
}

function requireAbsolute(value, name) {
  const text = requireText(value, name)
  if (!text.startsWith('/')) throw new Error(`${name} must be an absolute path`)
  return text
}

function requireFullCommitSha(value, name) {
  const text = requireText(value, name)
  if (!/^[0-9a-f]{40}$/.test(text)) throw new Error(`${name} must be a full lowercase 40-hex commit SHA`)
  return text
}

function shellQuote(value) {
  return `'${String(value).replace(/'/g, `'"'"'`)}'`
}

function assertHandoff(result, orderId) {
  if (result === null) throw new Error(`${orderId} returned null (agent, schema, or gate failure)`)
  if (result.order_id !== orderId) throw new Error(`${orderId} returned handoff for ${result.order_id}`)
  if (!result.red_observed) throw new Error(`${orderId} did not observe its required pre-fix failure`)
  if (result.blockers.length) throw new Error(`${orderId} reported blockers: ${result.blockers.join('; ')}`)
  if (result.skipped_work.length) throw new Error(`${orderId} skipped required work: ${result.skipped_work.join('; ')}`)
  return result
}

function assertIntegration(result, label) {
  if (result === null) throw new Error(`${label} integration returned null (agent, schema, or gate failure)`)
  if (result.skipped_work.length) throw new Error(`${label} integration skipped work: ${result.skipped_work.join('; ')}`)
  return result
}

if (args?.approval !== 'APPROVE_IMPLEMENTATION') {
  throw new Error('Explicit human approval required: args.approval must equal APPROVE_IMPLEMENTATION')
}

const repoPath = requireAbsolute(args?.repoPath, 'args.repoPath')
const piPath = requireAbsolute(args?.piPath, 'args.piPath')
const piSubagentsPath = requireAbsolute(args?.piSubagentsPath, 'args.piSubagentsPath')
const piExecutable = requireAbsolute(args?.piExecutable, 'args.piExecutable')
const implementationStartCommit = requireFullCommitSha(args?.implementationStartCommit, 'args.implementationStartCommit')
const writerModel = requireText(args?.writerModel, 'args.writerModel')
const integratorModel = requireText(args?.integratorModel, 'args.integratorModel')
const effort = args?.effort ?? 'high'
if (!['minimal', 'low', 'medium', 'high', 'xhigh', 'max'].includes(effort)) throw new Error('args.effort is invalid')

const envPrefix = `PI_EXECUTABLE=${shellQuote(piExecutable)} PI_CHECKOUT=${shellQuote(piPath)} PI_SUBAGENTS_CHECKOUT=${shellQuote(piSubagentsPath)}`
const implementationDiff = `${shellQuote(implementationStartCommit)}..HEAD`
const testGate = `${envPrefix} ${PYTEST} -q tests/pi-skill-creator -m 'not live' && git diff --check ${implementationDiff}`
const gateWithTy = paths => `${envPrefix} ${PYTEST} -q tests/pi-skill-creator -m 'not live' && ${TY} check ${paths.join(' ')} && git diff --check ${implementationDiff}`
const telemetryGate = gateWithTy(['skills/pi-skill-creator/scripts/transcript_metrics.py'])
const validatorGate = gateWithTy(['skills/pi-skill-creator/scripts/quick_validate.py', 'skills/pi-skill-creator/scripts/utils.py'])
const viewerGate = gateWithTy(['skills/pi-skill-creator/eval-viewer'])
const aggregationGate = gateWithTy(['skills/pi-skill-creator/scripts/aggregate_benchmark.py'])
const contractsGate = gateWithTy([
  'skills/pi-skill-creator/scripts/transcript_metrics.py',
  'skills/pi-skill-creator/scripts/quick_validate.py',
  'skills/pi-skill-creator/scripts/utils.py',
  'skills/pi-skill-creator/eval-viewer',
])
const coreGate = gateWithTy([
  'skills/pi-skill-creator/scripts/transcript_metrics.py',
  'skills/pi-skill-creator/scripts/quick_validate.py',
  'skills/pi-skill-creator/scripts/utils.py',
  'skills/pi-skill-creator/scripts/aggregate_benchmark.py',
  'skills/pi-skill-creator/eval-viewer',
])
const fullGate = gateWithTy(['skills/pi-skill-creator/scripts', 'skills/pi-skill-creator/eval-viewer'])

phase('Preflight')
const trackedHandoffGate = REQUIRED_HANDOFF_FILES
  .map(path => `test "$(git -C ${shellQuote(repoPath)} cat-file -t ${shellQuote(`${implementationStartCommit}:${path}`)})" = "blob"`)
  .join(' && ')
const preflight = await agent(
  `Read only. Verify the repository and two runtime checkouts for the pi-skill-creator adoption. Repository: ${repoPath}. Implementation start commit: ${implementationStartCommit}. Immutable source baseline: ${SOURCE_BASELINE}. Pi: ${piPath}. Pi executable: ${piExecutable}. pi-subagents: ${piSubagentsPath}. Confirm the implementation start is the clean current HEAD, contains the complete tracked handoff, descends from or equals the source baseline, and will therefore be the parent visible to isolated worktree agents. Confirm exact runtime revisions, executable version, uv/uvx, Python 3.10+, and that vendor/, skills/pi-skill-creator/, Pi, and pi-subagents will remain unmodified. Return the structured result only.`,
  {
    label: 'preflight',
    phase: 'Preflight',
    agentType: 'Explore',
    model: integratorModel,
    effort: 'low',
    schema: {
      type: 'object',
      properties: { ok: { type: 'boolean' }, summary: { type: 'string' } },
      required: ['ok', 'summary'],
    },
    gate: `test "$(git rev-parse --show-toplevel)" = ${shellQuote(repoPath)} && test "$(git rev-parse HEAD)" = ${shellQuote(implementationStartCommit)} && test "$(git -C ${shellQuote(repoPath)} rev-parse HEAD)" = ${shellQuote(implementationStartCommit)} && test -z "$(git -C ${shellQuote(repoPath)} status --porcelain)" && git -C ${shellQuote(repoPath)} merge-base --is-ancestor ${shellQuote(SOURCE_BASELINE)} ${shellQuote(implementationStartCommit)} && ${trackedHandoffGate} && test "$(git -C ${shellQuote(piPath)} rev-parse HEAD)" = ${shellQuote(REQUIRED_PI)} && test "$(git -C ${shellQuote(piSubagentsPath)} rev-parse HEAD)" = ${shellQuote(REQUIRED_SUBAGENTS)} && test -x ${shellQuote(piExecutable)} && test "$(${shellQuote(piExecutable)} --version)" = "0.84.4"`,
  },
)
if (preflight === null || preflight.ok !== true) throw new Error('Preflight failed closed')

const integrated = []
const bounded = []
const skipped = []

async function runOrder(orderId, file, phaseName, gate) {
  const prompt = `Implement work order ${orderId} from docs/pi-skill-creator-work-orders/${file} in your current isolated worktree. Read contracts.md and the complete order first. The main repository path ${repoPath} and runtime checkout paths are references only; write only in the current worktree. Follow passing-main TDD: observe the named red test, implement only this order, run every deterministic gate, and commit all owned changes. Do not run live or credentialed tests. Do not modify vendor/, skills/pi-skill-creator/, ${piPath}, or ${piSubagentsPath}. Before answering, verify exclusive ownership and return the required structured handoff, including your current branch and commit. ${THREE_FIELD_SEMANTICS}`
  const result = await agent(prompt, {
    label: orderId,
    phase: phaseName,
    agentType: 'general-purpose',
    model: writerModel,
    effort,
    isolation: 'worktree',
    schema: HANDOFF,
    gate,
  })
  const checked = assertHandoff(result, orderId)
  bounded.push(...checked.bounded_work.map(item => `${orderId}: ${item}`))
  skipped.push(...checked.skipped_work.map(item => `${orderId}: ${item}`))
  return checked
}

// The integration agent runs under the phase of the implementation it integrates
// (handoff decision 7): a separate `Integrate` phase made the UI show a late phase
// running between the implementation phases.
async function integrateWave(label, results, gate, phaseName) {
  const branches = results.map(result => result.branch)
  if (new Set(branches).size !== branches.length) throw new Error(`${label} returned duplicate branch names`)
  const prompt = `Integrate ${label} into the current main checkout at ${repoPath}. Merge these already-gated worktree branches in order: ${JSON.stringify(branches)}. Read each structured handoff. Reject unexpected paths, ownership overlap, conflict, missing commit, bounded required work, or skipped work. Resolve no semantic contract by improvisation. Run the supplied non-live deterministic gate, commit the integration, and return the structured integration result. ${THREE_FIELD_SEMANTICS}`
  const result = await agent(prompt, {
    label: `integrate:${label}`,
    phase: phaseName,
    agentType: 'general-purpose',
    model: integratorModel,
    effort: 'high',
    schema: INTEGRATION,
    gate,
  })
  const checked = assertIntegration(result, label)
  integrated.push({ wave: label, commit: checked.commit, branches: checked.branches })
  bounded.push(...checked.bounded_work.map(item => `${label}: ${item}`))
  skipped.push(...checked.skipped_work.map(item => `${label}: ${item}`))
}

phase('Foundation')
const foundation = await runOrder('OSC-00', 'osc-00-test-foundation.md', 'Foundation', testGate)
await integrateWave('foundation', [foundation], testGate, 'Foundation')

phase('Contracts')
const contractWave = await parallel([
  () => runOrder('OSC-01', 'osc-01-telemetry-seam.md', 'Contracts', telemetryGate),
  () => runOrder('OSC-02', 'osc-02-validator-parity.md', 'Contracts', validatorGate),
  () => runOrder('OSC-03', 'osc-03-authoring-doctrine.md', 'Contracts', testGate),
  () => runOrder('OSC-04', 'osc-04-viewer-hardening.md', 'Contracts', viewerGate),
])
if (contractWave.some(result => result === null)) throw new Error('Contracts wave failed or was skipped')
await integrateWave('contracts', contractWave, contractsGate, 'Contracts')

phase('Core')
const coreWave = await parallel([
  () => runOrder('OSC-05', 'osc-05-aggregation-schemas.md', 'Core', aggregationGate),
  () => runOrder('OSC-06', 'osc-06-bundled-agents.md', 'Core', contractsGate),
])
if (coreWave.some(result => result === null)) throw new Error('Core wave failed or was skipped')
await integrateWave('core', coreWave, coreGate, 'Core')

phase('Models')
const models = await runOrder('OSC-07', 'osc-07-role-model-config.md', 'Models', fullGate)
await integrateWave('models', [models], fullGate, 'Models')

phase('Execution')
const executionWave = await parallel([
  () => runOrder('OSC-08', 'osc-08-trigger-reliability.md', 'Execution', fullGate),
  () => runOrder('OSC-10', 'osc-10-rpc-profiles.md', 'Execution', fullGate),
])
if (executionWave.some(result => result === null)) throw new Error('Execution wave failed or was skipped')
await integrateWave('execution', executionWave, fullGate, 'Execution')

phase('Doctrine')
const doctrineWave = await parallel([
  () => runOrder('OSC-09', 'osc-09-optimizer-methodology.md', 'Doctrine', fullGate),
  () => runOrder('OSC-11', 'osc-11-testing-doctrine.md', 'Doctrine', fullGate),
])
if (doctrineWave.some(result => result === null)) throw new Error('Doctrine wave failed or was skipped')
await integrateWave('doctrine', doctrineWave, fullGate, 'Doctrine')

phase('Runtime workflow')
const runtimeWorkflow = await runOrder('OSC-12', 'osc-12-runtime-workflow-docs.md', 'Runtime workflow', fullGate)
await integrateWave('runtime-workflow', [runtimeWorkflow], fullGate, 'Runtime workflow')

phase('README')
const readme = await runOrder('OSC-13', 'osc-13-readme-deterministic.md', 'README', fullGate)
await integrateWave('readme', [readme], fullGate, 'README')

if (skipped.length) throw new Error(`Required implementation work was skipped: ${skipped.join('; ')}`)
log('Deterministic implementation complete. Paid/live calibration was not started.')
return {
  status: 'ready-for-calibration',
  implementationStartCommit,
  implementationIntegrationCommit: integrated[integrated.length - 1].commit,
  integrated,
  bounded_work: bounded,
  skipped_work: skipped,
  next_work_order: 'OSC-14',
  next_workflow: '.pi/workflows/pi-skill-creator-calibration.js',
  calibration_started: false,
}

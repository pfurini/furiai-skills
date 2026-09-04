export const meta = {
  name: 'pi-skill-creator-calibration',
  description: 'Preflight, validate, and finalize the pi-skill-creator smoke calibration in three separately invoked human-approved stages that make no paid call',
  whenToUse: 'Invoke after OSC-18 is integrated: preflight before the smoke campaign, calibrate after the top-level Pi session ran the approved smoke, finalize after the human review record exists.',
  phases: [
    { title: 'Preflight' },
    { title: 'Calibrate' },
    { title: 'Human checkpoint' },
    { title: 'Distribution' },
  ],
}

const REQUIRED_PI = 'db6bee3d6ccb79f5bc7884962ea4d98ca21e60ee'
const REQUIRED_PI_VERSION = '0.84.4'
const REQUIRED_SUBAGENTS = '7f569969445bf8bc6fbd7757f18db80b35de0ba9'
const REQUIRED_DYNAMIC_WORKFLOWS = 'e9c5a41d9c4234df908aa25a2b49ee9648e896d4'
const REQUIRED_CLAUDE_BRIDGE = 'c1d8b24a57e15bc8acc9d673f2804ab7227978ae'
const PYTEST = "uvx --from 'pytest==9.1.1' pytest"
const TY = "uvx --from 'ty==0.0.77' ty"
const STAGES = ['preflight', 'calibrate', 'finalize']
const ROLE_KEYS = ['executor', 'grader', 'comparator', 'benchmarkAnalyzer']
const THINKING_LEVELS = ['minimal', 'low', 'medium', 'high', 'xhigh', 'max']
// The closed scenario enum has one member for this program: the smoke test of OSC-14.
const SCENARIOS = ['runtime-workflow-smoke']
const IDENTIFIER = /^[a-z0-9][a-z0-9-]{0,63}$/
const UTC_TIMESTAMP = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/
const MODEL = /^[^/\s:]+\/[^\s:]+$/
// Handoff decision 7: the three list fields have fixed meanings, and every writer and
// integrator prompt states them so a mandated exclusion is never reported as skipped work.
const THREE_FIELD_SEMANTICS = '`tests_skipped` lists intentionally skipped tests only; `bounded_work` lists mandated exclusions only; `skipped_work` lists required work left incomplete and must be `[]` on completion.'

function requireText(value, name) {
  if (typeof value !== 'string' || value.trim() === '') throw new Error(`${name} must be a non-empty string`)
  return value
}

function requireAbsolute(value, name) {
  const text = requireText(value, name)
  if (!text.startsWith('/')) throw new Error(`${name} must be an absolute path`)
  return text
}

function requirePositiveInteger(value, name) {
  if (!Number.isInteger(value) || value < 1) throw new Error(`${name} must be a positive integer`)
  return value
}

function requireFullCommitSha(value, name) {
  const text = requireText(value, name)
  if (!/^[0-9a-f]{40}$/.test(text)) throw new Error(`${name} must be a full lowercase 40-hex commit SHA`)
  return text
}

function shellQuote(value) {
  return `'${String(value).replace(/'/g, `'"'"'`)}'`
}

function requirePlainObject(value, name, detail) {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) throw new Error(`${name} must be an object ${detail}`)
  return value
}

// The smoke manifest, shared by the preflight and calibrate stages. Every field has a
// strict schema: an unknown role, a missing role, an extra key inside a role, a model
// with a thinking suffix, an `off` thinking level, or any scenario list other than the
// closed enum is refused before any child spawns.
function requireManifest(source) {
  const campaignId = requireText(source?.campaignId, 'args.campaignId')
  if (!IDENTIFIER.test(campaignId)) throw new Error('args.campaignId must match [a-z0-9][a-z0-9-]{0,63}')
  const createdAt = requireText(source?.createdAt, 'args.createdAt')
  if (!UTC_TIMESTAMP.test(createdAt)) throw new Error('args.createdAt must be a UTC timestamp of the form YYYY-MM-DDTHH:MM:SSZ')
  const repetitions = requirePositiveInteger(source?.repetitions, 'args.repetitions')
  const maxPaidCalls = requirePositiveInteger(source?.maxPaidCalls, 'args.maxPaidCalls')

  const rawModels = requirePlainObject(source?.models, 'args.models', `with exactly the role keys ${ROLE_KEYS.join(', ')}`)
  const roleKeys = Object.keys(rawModels).sort()
  if (roleKeys.join(',') !== [...ROLE_KEYS].sort().join(',')) {
    throw new Error(`args.models must have exactly the role keys ${ROLE_KEYS.join(', ')}; got ${roleKeys.join(', ') || 'none'}`)
  }
  const models = {}
  for (const role of ROLE_KEYS) {
    const entry = requirePlainObject(rawModels[role], `args.models.${role}`, 'with exactly the keys model and thinking')
    const entryKeys = Object.keys(entry).sort()
    if (entryKeys.join(',') !== 'model,thinking') {
      throw new Error(`args.models.${role} must have exactly the keys model and thinking; got ${entryKeys.join(', ') || 'none'}`)
    }
    const model = requireText(entry.model, `args.models.${role}.model`)
    if (!MODEL.test(model)) throw new Error(`args.models.${role}.model must be provider/id without a thinking suffix`)
    if (typeof entry.thinking !== 'string' || !THINKING_LEVELS.includes(entry.thinking)) {
      throw new Error(`args.models.${role}.thinking must be one of ${THINKING_LEVELS.join(', ')}`)
    }
    models[role] = { model, thinking: entry.thinking }
  }

  const scenarios = source?.scenarios
  const scenariosMatch = Array.isArray(scenarios)
    && scenarios.length === SCENARIOS.length
    && scenarios.every((scenario, index) => scenario === SCENARIOS[index])
  if (!scenariosMatch) throw new Error(`args.scenarios must equal ${JSON.stringify(SCENARIOS)} for this program`)

  return { campaignId, createdAt, repetitions, maxPaidCalls, models, scenarios: [...SCENARIOS] }
}

// Shared validation, before any phase.
const stage = requireText(args?.stage, 'args.stage')
if (!STAGES.includes(stage)) throw new Error(`args.stage must be one of ${STAGES.join(', ')}`)
const stageStartCommit = requireFullCommitSha(args?.stageStartCommit, 'args.stageStartCommit')
const repoPath = requireAbsolute(args?.repoPath, 'args.repoPath')
const piPath = requireAbsolute(args?.piPath, 'args.piPath')
const piSubagentsPath = requireAbsolute(args?.piSubagentsPath, 'args.piSubagentsPath')
const piDynamicWorkflowsPath = requireAbsolute(args?.piDynamicWorkflowsPath, 'args.piDynamicWorkflowsPath')
const piClaudeBridgePath = requireAbsolute(args?.piClaudeBridgePath, 'args.piClaudeBridgePath')
const piExecutable = requireAbsolute(args?.piExecutable, 'args.piExecutable')
const installedSkillPath = requireAbsolute(args?.installedSkillPath, 'args.installedSkillPath')
const campaignDir = requireAbsolute(args?.campaignDir, 'args.campaignDir')
const orchestratorModel = requireText(args?.orchestratorModel, 'args.orchestratorModel')
const writerModel = requireText(args?.writerModel, 'args.writerModel')
const integratorModel = requireText(args?.integratorModel, 'args.integratorModel')

// Approval tokens are stage-specific. Preflight requires none and ignores `approval`; a
// token, a prior preflight result, or review-file existence never authorizes another stage.
const expectedApproval = { preflight: undefined, calibrate: 'APPROVE_PAID_CALIBRATION', finalize: 'APPROVE_CALIBRATION_RESULTS' }[stage]
if (expectedApproval !== undefined && args?.approval !== expectedApproval) {
  throw new Error(`Explicit human approval required: args.approval must equal ${expectedApproval} for stage ${stage}`)
}
const manifest = stage === 'finalize' ? undefined : requireManifest(args)
if (stage === 'finalize' && args?.humanReviewComplete !== true) {
  throw new Error('args.humanReviewComplete must be true after reviewing calibration records')
}
const humanReviewRecord = stage === 'finalize' ? requireAbsolute(args?.humanReviewRecord, 'args.humanReviewRecord') : undefined

// Every gate carries the four checkout variables, so the deterministic gate runs the full
// `not live` suite with no contract test or pi-dynamic-workflows probe skipped.
const envPrefix = `PI_EXECUTABLE=${shellQuote(piExecutable)} PI_CHECKOUT=${shellQuote(piPath)} PI_SUBAGENTS_CHECKOUT=${shellQuote(piSubagentsPath)} PI_DYNAMIC_WORKFLOWS_CHECKOUT=${shellQuote(piDynamicWorkflowsPath)}`
const stageDiff = `${shellQuote(stageStartCommit)}..HEAD`
const deterministicGate = `${envPrefix} ${PYTEST} -q tests/pi-skill-creator -m 'not live' && ${TY} check skills/pi-skill-creator/scripts skills/pi-skill-creator/eval-viewer && git diff --check ${stageDiff}`

function pinCheck(path, revision) {
  return `test "$(git -C ${shellQuote(path)} rev-parse HEAD)" = ${shellQuote(revision)}`
}

// Exact-row model resolution: `pi --list-models <pattern>` filters fuzzily and prints one
// whitespace-separated row per model, so "resolvable" means a row whose first field is the
// provider and whose second field is the id, never a substring match on the whole output.
// The command makes no model call.
function modelResolutionCheck(model) {
  const slash = model.indexOf('/')
  const provider = model.slice(0, slash)
  const id = model.slice(slash + 1)
  return `${shellQuote(piExecutable)} --list-models ${shellQuote(model)} | awk -v p=${shellQuote(provider)} -v m=${shellQuote(id)} '$1 == p && $2 == m { found = 1 } END { exit !found }'`
}

const skillSource = `${repoPath}/skills/pi-skill-creator`
// Pi reads both user skill roots, so the installed copy must be in one of them and the
// other must not exist, or same-name resolution would collide with a stale copy. $HOME is
// left to the gate shell on purpose; project-level skill roots are not checked because the
// smoke's evaluation project is a fresh directory.
const userRoots = ['"$HOME/.pi/agent/skills/pi-skill-creator"', '"$HOME/.agents/skills/pi-skill-creator"']
const skillCopyCheck = `diff -r -x __pycache__ ${shellQuote(skillSource)} ${shellQuote(installedSkillPath)} && { { test ${shellQuote(installedSkillPath)} = ${userRoots[0]} && test ! -e ${userRoots[1]}; } || { test ${shellQuote(installedSkillPath)} = ${userRoots[1]} && test ! -e ${userRoots[0]}; }; }`

const pinChecks = [
  `test "$(git -C ${shellQuote(repoPath)} rev-parse HEAD)" = ${shellQuote(stageStartCommit)}`,
  `test -z "$(git -C ${shellQuote(repoPath)} status --porcelain)"`,
  pinCheck(piPath, REQUIRED_PI),
  pinCheck(piSubagentsPath, REQUIRED_SUBAGENTS),
  pinCheck(piDynamicWorkflowsPath, REQUIRED_DYNAMIC_WORKFLOWS),
  pinCheck(piClaudeBridgePath, REQUIRED_CLAUDE_BRIDGE),
  `test -x ${shellQuote(piExecutable)}`,
  `test "$(${shellQuote(piExecutable)} --version)" = ${shellQuote(REQUIRED_PI_VERSION)}`,
]
// The mechanical preflight per stage: preflight and calibrate share the pins, the skill
// copy, and one exact-row model check per manifest role; only preflight requires the
// campaign directory to hold no campaign.json yet; finalize keeps the pins and the review
// record. Every stage requires HEAD to equal stageStartCommit and a clean tree.
function stageChecks() {
  if (stage === 'finalize') return [...pinChecks, `test -f ${shellQuote(humanReviewRecord)}`]
  const modelChecks = ROLE_KEYS.map(role => modelResolutionCheck(manifest.models[role].model))
  const campaignChecks = stage === 'preflight' ? [`test ! -e ${shellQuote(`${campaignDir}/campaign.json`)}`] : []
  return [...pinChecks, skillCopyCheck, ...campaignChecks, ...modelChecks]
}
const preflightGate = stageChecks().join(' && ')

const stageStartMeaning = {
  preflight: 'the OSC-18 integration commit at which the smoke will run',
  calibrate: 'the OSC-18 integration commit at which the smoke ran',
  finalize: 'the calibration integration commit whose campaign records the human reviewed',
}[stage]
const stageDetail = {
  preflight: `Campaign directory ${campaignDir} must not contain campaign.json yet. Manifest models to resolve through ${piExecutable} --list-models (exact provider and model row): ${JSON.stringify(manifest?.models)}.`,
  calibrate: `Campaign directory ${campaignDir} holds the smoke records the top-level session produced; read them, never modify them. Manifest models to resolve through ${piExecutable} --list-models (exact provider and model row): ${JSON.stringify(manifest?.models)}.`,
  finalize: `The immutable human review record ${humanReviewRecord} must exist. No manifest model is checked in this stage: return models_resolved and models_unresolved as empty arrays.`,
}[stage]

phase('Preflight')
// pi-claude-bridge loading is settled by source, not by an option. This child and the
// calibrate writer run on the default agent types (`Explore` and `general-purpose`), which
// set `extensions: true` and `skills: true` (pi-subagents src/default-agents.ts:21-22 and
// :35-36); src/agent-runner.ts:671 and :761 turn that into `loadAll`, so the child's
// resource loader discovers every host package from ~/.pi/agent/settings.json, including
// pi-claude-bridge. This workflow never sets `isolated` and never names a custom agent type;
// changing either is a visible decision that would drop the bridge from the child.
const preflight = await agent(
  `Read only. Make no model call and no paid call. Preflight the ${stage} stage of the pi-skill-creator smoke calibration; the gate runs the mechanical checks, and you confirm them from evidence and report. Repository ${repoPath} must be clean at args.stageStartCommit ${stageStartCommit}, which is ${stageStartMeaning}. Pins: Pi ${piPath} at ${REQUIRED_PI}; pi-subagents ${piSubagentsPath} at ${REQUIRED_SUBAGENTS}; pi-dynamic-workflows ${piDynamicWorkflowsPath} at ${REQUIRED_DYNAMIC_WORKFLOWS}; pi-claude-bridge ${piClaudeBridgePath} at ${REQUIRED_CLAUDE_BRIDGE}. Pi executable ${piExecutable} must report ${REQUIRED_PI_VERSION}. The installed skill copy ${installedSkillPath} must be byte-for-byte equal to ${skillSource} and be the only copy in the two user skill roots (~/.pi/agent/skills and ~/.agents/skills). ${stageDetail} Write nothing and modify no checkout. Return structured output only: ok, models_resolved (every manifest model whose exact provider and model row printed), models_unresolved, skill_copy_verified, bounded_work, skipped_work, summary. ${THREE_FIELD_SEMANTICS}`,
  {
    label: `preflight:${stage}`,
    phase: 'Preflight',
    agentType: 'Explore',
    model: orchestratorModel,
    effort: 'low',
    schema: {
      type: 'object',
      properties: {
        ok: { type: 'boolean' },
        models_resolved: { type: 'array', items: { type: 'string' } },
        models_unresolved: { type: 'array', items: { type: 'string' } },
        skill_copy_verified: { type: 'boolean' },
        bounded_work: { type: 'array', items: { type: 'string' } },
        skipped_work: { type: 'array', items: { type: 'string' } },
        summary: { type: 'string' },
      },
      required: ['ok', 'models_resolved', 'models_unresolved', 'skill_copy_verified', 'bounded_work', 'skipped_work', 'summary'],
    },
    gate: preflightGate,
  },
)
if (preflight === null || preflight.ok !== true || preflight.models_unresolved.length || preflight.skipped_work.length) {
  throw new Error(`${stage} preflight failed closed`)
}

if (stage === 'preflight') {
  log('Preflight passed. Nothing was written and no paid call was made. The smoke campaign runs from the top-level Pi session under the human-approved manifest (OSC-14); invoke stage calibrate with the same stageStartCommit afterwards.')
  return {
    status: 'preflight-passed',
    stageStartCommit,
    manifest,
    models_resolved: preflight.models_resolved,
    bounded_work: preflight.bounded_work,
    skipped_work: [],
  }
}

// Integration runs under the phase of the order it integrates (handoff decision 7).
async function integrate(label, result, gate, phaseName) {
  if (result === null) throw new Error(`${label} returned null`)
  if (result.skipped_work.length) throw new Error(`${label} skipped work: ${result.skipped_work.join('; ')}`)
  const integrated = await agent(
    `Integrate ${label} branch ${result.branch} into the clean main checkout ${repoPath} under phase ${phaseName}. Make no model call and no paid call. Verify the handoff, reject unexpected paths or unreported bounded or skipped work, run the supplied deterministic gate, commit, and return structured output only. ${THREE_FIELD_SEMANTICS}`,
    {
      label: `integrate:${label}`,
      phase: phaseName,
      agentType: 'general-purpose',
      model: integratorModel,
      effort: 'high',
      schema: {
        type: 'object',
        properties: {
          status: { type: 'string', enum: ['completed'] },
          commit: { type: 'string' },
          bounded_work: { type: 'array', items: { type: 'string' } },
          skipped_work: { type: 'array', items: { type: 'string' } },
          summary: { type: 'string' },
        },
        required: ['status', 'commit', 'bounded_work', 'skipped_work', 'summary'],
      },
      gate,
    },
  )
  if (integrated === null || integrated.skipped_work.length) throw new Error(`${label} integration failed closed`)
  return integrated
}

if (stage === 'calibrate') {
  phase('Calibrate')
  const { campaignId, createdAt, repetitions, maxPaidCalls, models, scenarios } = manifest
  // The paid-call comparison is mechanical: the replay-only live test counts the same
  // records and fails when their sum exceeds PI_SKILL_CREATOR_MAX_PAID_CALLS.
  const liveGate = `PI_SKILL_CREATOR_LIVE_TESTS=1 PI_SKILL_CREATOR_REPLAY_ONLY=1 PI_SKILL_CREATOR_CAMPAIGN_DIR=${shellQuote(campaignDir)} PI_SKILL_CREATOR_MAX_PAID_CALLS=${shellQuote(String(maxPaidCalls))} ${envPrefix} ${PYTEST} -q tests/pi-skill-creator/test_live_calibration.py -m live && ${deterministicGate}`
  const calibration = await agent(
    `Execute the validation part of OSC-14 from docs/pi-skill-creator-work-orders/osc-14-live-calibration.md in the current isolated worktree. Make no model call and no paid call: the smoke campaign was already run from the top-level Pi session under the human-approved manifest, and this stage only validates its durable records. Inputs: campaignId=${campaignId}; createdAt=${createdAt}; campaignDir=${campaignDir}; stageStartCommit=${stageStartCommit}; installedSkillPath=${installedSkillPath}; Pi executable=${piExecutable}; Pi checkout=${piPath}; pi-subagents checkout=${piSubagentsPath}; pi-dynamic-workflows checkout=${piDynamicWorkflowsPath}; pi-claude-bridge checkout=${piClaudeBridgePath}; repetitions=${repetitions}; maxPaidCalls=${maxPaidCalls}; models=${JSON.stringify(models)}; scenarios=${JSON.stringify(scenarios)}. Steps: (1) read the campaign directory and verify that workflow-result.json is present and parses with valid: true, workflow_runtime: 'pi-subagents', and agent_calls_made <= max_agent_calls; (2) count the records: agent_calls_made from workflow-result.json, plus the number of run.json files, plus the number of comparisons/*/comparison.json files, plus zero analyzer or viewer model calls unless the manifest ledger lists them, and report the sum as paid_calls_used with max_paid_calls=${maxPaidCalls}; (3) write tests/pi-skill-creator/test_live_calibration.py exactly as OSC-14 "Required behavior" specifies (marked live, replay-only, reading PI_SKILL_CREATOR_CAMPAIGN_DIR and PI_SKILL_CREATOR_MAX_PAID_CALLS, failing rather than skipping when both opt-in flags are set and the campaign is missing or incomplete); (4) write ${campaignDir}/review-required.json with schema id pi-skill-creator.review-required/v1 and the content OSC-14 "Records and review" specifies (label smoke-test, the revisions and installed skill path, machinery, effective_models, call_counts, token_usage, anomalies, known_gaps, and empty claim_candidates and pin_candidates); (5) commit only the test file; campaign records stay at campaignDir and are never committed. Do not edit README, SKILL, or agent pins before human review; claims_changed and pins_changed must be []. Stop on any auth, model, schema, or infrastructure invalidation and report it under blockers. Return the OSC-14 structured handoff only. ${THREE_FIELD_SEMANTICS}`,
    {
      label: 'OSC-14',
      phase: 'Calibrate',
      agentType: 'general-purpose',
      model: writerModel,
      effort: 'high',
      isolation: 'worktree',
      schema: {
        type: 'object',
        properties: {
          order_id: { type: 'string', enum: ['OSC-14'] },
          status: { type: 'string', enum: ['completed'] },
          branch: { type: 'string' },
          commit: { type: 'string' },
          workflow_result_valid: { type: 'boolean' },
          paid_calls_used: { type: 'integer', minimum: 0 },
          max_paid_calls: { type: 'integer', minimum: 1 },
          agent_calls_made: { type: 'integer', minimum: 0 },
          max_agent_calls: { type: 'integer', minimum: 1 },
          records: { type: 'array', items: { type: 'string' } },
          manual_review_required: { type: 'array', items: { type: 'string' } },
          tests_passed: { type: 'array', items: { type: 'string' } },
          tests_skipped: { type: 'array', items: { type: 'string' } },
          bounded_work: { type: 'array', items: { type: 'string' } },
          skipped_work: { type: 'array', items: { type: 'string' } },
          claims_changed: { type: 'array', items: { type: 'string' } },
          pins_changed: { type: 'array', items: { type: 'string' } },
          summary: { type: 'string' },
          blockers: { type: 'array', items: { type: 'string' } },
        },
        required: ['order_id', 'status', 'branch', 'commit', 'workflow_result_valid', 'paid_calls_used', 'max_paid_calls', 'agent_calls_made', 'max_agent_calls', 'records', 'manual_review_required', 'tests_passed', 'tests_skipped', 'bounded_work', 'skipped_work', 'claims_changed', 'pins_changed', 'summary', 'blockers'],
      },
      gate: liveGate,
    },
  )
  if (calibration === null) throw new Error('OSC-14 returned null')
  if (calibration.paid_calls_used > maxPaidCalls || calibration.max_paid_calls !== maxPaidCalls) throw new Error('Paid-call bound mismatch')
  if (calibration.workflow_result_valid !== true || calibration.agent_calls_made > calibration.max_agent_calls) throw new Error('OSC-14 smoke record is not valid')
  if (calibration.claims_changed.length || calibration.pins_changed.length) throw new Error('OSC-14 changed claims or pins before human review')
  if (calibration.blockers.length || calibration.skipped_work.length) throw new Error('OSC-14 did not complete the approved scope')
  const integration = await integrate('OSC-14', calibration, liveGate, 'Calibrate')
  phase('Human checkpoint')
  log('Calibration validated and integrated without a paid call. Stop now for human review; final distribution requires a new finalize invocation and APPROVE_CALIBRATION_RESULTS.')
  return {
    status: 'awaiting-human-calibration-review',
    calibrationIntegrationCommit: integration.commit,
    campaignId,
    campaignDir,
    paid_calls_used: calibration.paid_calls_used,
    max_paid_calls: maxPaidCalls,
    records: calibration.records,
    manual_review_required: calibration.manual_review_required,
    bounded_work: [...preflight.bounded_work, ...calibration.bounded_work, ...integration.bounded_work],
    skipped_work: [],
    distribution_started: false,
  }
}

phase('Human checkpoint')
const claimGate = `PI_SKILL_CREATOR_CAMPAIGN_DIR=${shellQuote(campaignDir)} PI_SKILL_CREATOR_HUMAN_REVIEW=${shellQuote(humanReviewRecord)} ${PYTEST} -q tests/pi-skill-creator/test_calibrated_claims.py && ${deterministicGate}`
const applied = await agent(
  `Execute OSC-15 from docs/pi-skill-creator-work-orders/osc-15-apply-calibration.md in the current isolated worktree. The human-reviewed campaign is ${campaignDir}; the immutable human decision record is ${humanReviewRecord}. Apply only explicitly accepted claims and pins. Run no model call, no paid call, and no credentialed call. Do not modify sibling checkouts. Commit and return structured output only. ${THREE_FIELD_SEMANTICS}`,
  {
    label: 'OSC-15',
    phase: 'Human checkpoint',
    agentType: 'general-purpose',
    model: writerModel,
    effort: 'high',
    isolation: 'worktree',
    schema: {
      type: 'object',
      properties: {
        order_id: { type: 'string', enum: ['OSC-15'] },
        status: { type: 'string', enum: ['completed'] },
        branch: { type: 'string' },
        commit: { type: 'string' },
        red_observed: { type: 'boolean' },
        claims_applied: { type: 'array', items: { type: 'string' } },
        claims_removed: { type: 'array', items: { type: 'string' } },
        pins_applied: { type: 'array', items: { type: 'string' } },
        bounded_work: { type: 'array', items: { type: 'string' } },
        skipped_work: { type: 'array', items: { type: 'string' } },
        summary: { type: 'string' },
      },
      required: ['order_id', 'status', 'branch', 'commit', 'red_observed', 'claims_applied', 'claims_removed', 'pins_applied', 'bounded_work', 'skipped_work', 'summary'],
    },
    gate: claimGate,
  },
)
if (applied === null || applied.red_observed !== true || applied.skipped_work.length) throw new Error('OSC-15 failed closed')
const appliedIntegration = await integrate('OSC-15', applied, claimGate, 'Human checkpoint')

phase('Distribution')
const distribution = await agent(
  `Execute OSC-16 from docs/pi-skill-creator-work-orders/osc-16-directory-distribution.md in the current isolated worktree. Calibration conclusions have been human-approved and integrated. Validate copied-directory distribution against Pi ${piPath} and pi-subagents ${piSubagentsPath}; make no model call and no paid call; do not repair the temporary copy; do not modify sibling checkouts. Commit the project-level distribution tests and any permitted README wording correction. Return structured output only. ${THREE_FIELD_SEMANTICS}`,
  {
    label: 'OSC-16',
    phase: 'Distribution',
    agentType: 'general-purpose',
    model: writerModel,
    effort: 'high',
    isolation: 'worktree',
    schema: {
      type: 'object',
      properties: {
        order_id: { type: 'string', enum: ['OSC-16'] },
        status: { type: 'string', enum: ['completed'] },
        branch: { type: 'string' },
        commit: { type: 'string' },
        f19_absence_verified: { type: 'boolean' },
        boundary_violations: { type: 'array', items: { type: 'string' } },
        bounded_work: { type: 'array', items: { type: 'string' } },
        skipped_work: { type: 'array', items: { type: 'string' } },
        summary: { type: 'string' },
      },
      required: ['order_id', 'status', 'branch', 'commit', 'f19_absence_verified', 'boundary_violations', 'bounded_work', 'skipped_work', 'summary'],
    },
    gate: deterministicGate,
  },
)
if (distribution === null || distribution.f19_absence_verified !== true || distribution.boundary_violations.length || distribution.skipped_work.length) {
  throw new Error('OSC-16 failed closed')
}
const finalIntegration = await integrate('OSC-16', distribution, deterministicGate, 'Distribution')
return {
  status: 'distribution-validated',
  finalCommit: finalIntegration.commit,
  campaignDir,
  humanReviewRecord,
  paid_calls_used: 0,
  bounded_work: [...preflight.bounded_work, ...applied.bounded_work, ...appliedIntegration.bounded_work, ...distribution.bounded_work, ...finalIntegration.bounded_work],
  skipped_work: [],
  f19_absence_verified: true,
}

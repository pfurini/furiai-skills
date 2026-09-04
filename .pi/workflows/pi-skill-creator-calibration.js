export const meta = {
  name: 'pi-skill-creator-calibration',
  description: 'Run explicitly approved paid calibration or, in a later invocation, final copied-directory validation',
  whenToUse: 'Invoke after deterministic adoption implementation; calibration and finalization are separate human-approved stages.',
  phases: [
    { title: 'Preflight' },
    { title: 'Calibrate' },
    { title: 'Human checkpoint' },
    { title: 'Distribution' },
    { title: 'Integrate' },
  ],
}

const REQUIRED_PI = 'a4043c1e332a61e4c8648b97b9b796c57f9db110'
const REQUIRED_SUBAGENTS = 'bfa262fdd75d807b1c6b1f852f1f1bea2bbb3fa4'
const PYTEST = "uvx --from 'pytest==9.1.1' pytest"
const TY = "uvx --from 'ty==0.0.77' ty"

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

function shellQuote(value) {
  return `'${String(value).replace(/'/g, `'"'"'`)}'`
}

const repoPath = requireAbsolute(args?.repoPath, 'args.repoPath')
const piPath = requireAbsolute(args?.piPath, 'args.piPath')
const piSubagentsPath = requireAbsolute(args?.piSubagentsPath, 'args.piSubagentsPath')
const piExecutable = requireAbsolute(args?.piExecutable, 'args.piExecutable')
const campaignDir = requireAbsolute(args?.campaignDir, 'args.campaignDir')
const stage = requireText(args?.stage, 'args.stage')
if (!['calibrate', 'finalize'].includes(stage)) throw new Error('args.stage must be calibrate or finalize')
const stageStartCommit = requireText(args?.stageStartCommit, 'args.stageStartCommit')
const humanReviewRecord = stage === 'finalize' ? requireAbsolute(args?.humanReviewRecord, 'args.humanReviewRecord') : undefined

const envPrefix = `PI_CHECKOUT=${shellQuote(piPath)} PI_SUBAGENTS_CHECKOUT=${shellQuote(piSubagentsPath)}`
const deterministicGate = `${envPrefix} ${PYTEST} -q tests/pi-skill-creator -m 'not live' && ${TY} check skills/pi-skill-creator/scripts skills/pi-skill-creator/eval-viewer && git diff --check ${stageStartCommit}..HEAD`

phase('Preflight')
const expectedApproval = stage === 'calibrate' ? 'APPROVE_PAID_CALIBRATION' : 'APPROVE_CALIBRATION_RESULTS'
if (args?.approval !== expectedApproval) {
  throw new Error(`Explicit human approval required: args.approval must equal ${expectedApproval}`)
}

const preflightGate = `test "$(git -C ${shellQuote(repoPath)} rev-parse HEAD)" = ${shellQuote(stageStartCommit)} && test -z "$(git -C ${shellQuote(repoPath)} status --porcelain)" && test "$(git -C ${shellQuote(piPath)} rev-parse HEAD)" = ${shellQuote(REQUIRED_PI)} && test "$(git -C ${shellQuote(piSubagentsPath)} rev-parse HEAD)" = ${shellQuote(REQUIRED_SUBAGENTS)} && test -x ${shellQuote(piExecutable)} && test "$(${shellQuote(piExecutable)} --version)" = "0.84.4"${humanReviewRecord === undefined ? '' : ` && test -f ${shellQuote(humanReviewRecord)}`}`
const stageStartMeaning = stage === 'calibrate'
  ? 'the deterministic implementation integration commit returned by the adoption workflow'
  : 'the calibration integration commit whose campaign records the human reviewed'
const preflight = await agent(
  `Read only. Preflight the ${stage} stage for pi-skill-creator. Verify repository ${repoPath} is clean at args.stageStartCommit ${stageStartCommit}, which must be ${stageStartMeaning}; Pi ${piPath} is ${REQUIRED_PI}; pi-subagents ${piSubagentsPath} is ${REQUIRED_SUBAGENTS}; Pi executable is ${piExecutable}; campaign directory is ${campaignDir}; deterministic tests pass; and no sibling checkout will be modified. For calibrate, verify credentials/models and the paid-call bound before any measured call. For finalize, verify the human-reviewed campaign and immutable review record ${humanReviewRecord ?? '(not applicable)'}. Return structured output only.`,
  {
    label: `preflight:${stage}`,
    phase: 'Preflight',
    agentType: 'Explore',
    model: requireText(args?.orchestratorModel, 'args.orchestratorModel'),
    effort: 'low',
    schema: {
      type: 'object',
      properties: {
        ok: { type: 'boolean' },
        models_resolved: { type: 'array', items: { type: 'string' } },
        bounded_work: { type: 'array', items: { type: 'string' } },
        skipped_work: { type: 'array', items: { type: 'string' } },
        summary: { type: 'string' },
      },
      required: ['ok', 'models_resolved', 'bounded_work', 'skipped_work', 'summary'],
    },
    gate: preflightGate,
  },
)
if (preflight === null || preflight.ok !== true || preflight.skipped_work.length) throw new Error(`${stage} preflight failed closed`)

const writerModel = requireText(args?.writerModel, 'args.writerModel')
const integratorModel = requireText(args?.integratorModel, 'args.integratorModel')

async function integrate(label, result, gate) {
  if (result === null) throw new Error(`${label} returned null`)
  if (result.skipped_work.length) throw new Error(`${label} skipped work: ${result.skipped_work.join('; ')}`)
  const integrated = await agent(
    `Integrate ${label} branch ${result.branch} into the clean main checkout ${repoPath}. Verify the handoff, reject unexpected paths or unreported bounded/skipped work, run the supplied deterministic gate, commit, and return structured output only.`,
    {
      label: `integrate:${label}`,
      phase: 'Integrate',
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
  const campaignId = requireText(args?.campaignId, 'args.campaignId')
  const createdAt = requireText(args?.createdAt, 'args.createdAt')
  const repetitions = requirePositiveInteger(args?.repetitions, 'args.repetitions')
  const maxPaidCalls = requirePositiveInteger(args?.maxPaidCalls, 'args.maxPaidCalls')
  if (typeof args?.models !== 'object' || args.models === null || Array.isArray(args.models)) throw new Error('args.models must be an object')
  if (!Array.isArray(args?.scenarios) || args.scenarios.length === 0) throw new Error('args.scenarios must be a non-empty array')

  const liveGate = `PI_SKILL_CREATOR_LIVE_TESTS=1 PI_SKILL_CREATOR_REPLAY_ONLY=1 PI_SKILL_CREATOR_CAMPAIGN_DIR=${shellQuote(campaignDir)} PI_SKILL_CREATOR_MAX_PAID_CALLS=${shellQuote(String(maxPaidCalls))} PI_EXECUTABLE=${shellQuote(piExecutable)} ${envPrefix} ${PYTEST} -q tests/pi-skill-creator/test_live_calibration.py -m live && ${deterministicGate}`
  const calibration = await agent(
    `Execute OSC-14 from docs/pi-skill-creator-work-orders/osc-14-live-calibration.md in the current isolated worktree. Human approval is explicit for this bounded campaign only. Inputs: campaignId=${campaignId}; createdAt=${createdAt}; campaignDir=${campaignDir}; Pi executable=${piExecutable}; Pi checkout=${piPath}; pi-subagents checkout=${piSubagentsPath}; repetitions=${repetitions}; maxPaidCalls=${maxPaidCalls}; models=${JSON.stringify(args.models)}; scenarios=${JSON.stringify(args.scenarios)}. Pre-register before spending. Never exceed maxPaidCalls. Stop on auth/model/schema/infrastructure invalidation. Record all bounded/skipped work and write review-required.json. Do not edit README, SKILL, or agent pins before human review. Commit only project test changes; campaign records remain at campaignDir. Return branch, commit, paid-call accounting, records, manual-review-required flags, and the structured handoff.`,
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
          paid_calls_used: { type: 'integer', minimum: 0 },
          max_paid_calls: { type: 'integer', minimum: 1 },
          records: { type: 'array', items: { type: 'string' } },
          manual_review_required: { type: 'array', items: { type: 'string' } },
          bounded_work: { type: 'array', items: { type: 'string' } },
          skipped_work: { type: 'array', items: { type: 'string' } },
          summary: { type: 'string' },
          blockers: { type: 'array', items: { type: 'string' } },
        },
        required: ['order_id', 'status', 'branch', 'commit', 'paid_calls_used', 'max_paid_calls', 'records', 'manual_review_required', 'bounded_work', 'skipped_work', 'summary', 'blockers'],
      },
      gate: liveGate,
    },
  )
  if (calibration === null) throw new Error('OSC-14 returned null')
  if (calibration.paid_calls_used > maxPaidCalls || calibration.max_paid_calls !== maxPaidCalls) throw new Error('Paid-call bound mismatch')
  if (calibration.blockers.length || calibration.skipped_work.length) throw new Error('OSC-14 did not complete the approved scope')
  const integration = await integrate('OSC-14', calibration, liveGate)
  phase('Human checkpoint')
  log('Calibration integrated. Stop now for human review; final distribution requires a new finalize invocation and APPROVE_CALIBRATION_RESULTS.')
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
if (args?.humanReviewComplete !== true) throw new Error('args.humanReviewComplete must be true after reviewing calibration records')
if (humanReviewRecord === undefined) throw new Error('args.humanReviewRecord is required for finalize')
const claimGate = `PI_SKILL_CREATOR_CAMPAIGN_DIR=${shellQuote(campaignDir)} PI_SKILL_CREATOR_HUMAN_REVIEW=${shellQuote(humanReviewRecord)} ${PYTEST} -q tests/pi-skill-creator/test_calibrated_claims.py && ${deterministicGate}`
const applied = await agent(
  `Execute OSC-15 from docs/pi-skill-creator-work-orders/osc-15-apply-calibration.md in the current isolated worktree. The human-reviewed campaign is ${campaignDir}; the immutable human decision record is ${humanReviewRecord}. Apply only explicitly accepted claims and pins. Run no model or credentialed calls. Do not modify sibling checkouts. Commit and return structured output only.`,
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
const appliedIntegration = await integrate('OSC-15', applied, claimGate)

phase('Distribution')
const distribution = await agent(
  `Execute OSC-16 from docs/pi-skill-creator-work-orders/osc-16-directory-distribution.md in the current isolated worktree. Calibration conclusions have been human-approved and integrated. Validate copied-directory distribution against Pi ${piPath} and pi-subagents ${piSubagentsPath}; do not run paid calls; do not repair the temporary copy; do not modify sibling checkouts. Commit the project-level distribution tests and any permitted README wording correction. Return structured output only.`,
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
const finalIntegration = await integrate('OSC-16', distribution, deterministicGate)
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

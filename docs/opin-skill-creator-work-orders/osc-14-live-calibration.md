# OSC-14: Run approved Pi-native calibration

## Findings

No new primary finding. This is the evidence gate for model/profile-dependent secondary consumers F3-F4, F7-F12, F20, F24, F26-F28, and F35-F37.

## Dependencies

OSC-13 and explicit human approval through the separate calibration workflow.

## Settled decisions restated

- The `calibrate` invocation supplies `stageStartCommit` equal to the deterministic implementation integration commit produced by the adoption workflow. Exact-HEAD preflight requires the repository to be clean at that commit before any paid call.
- Calibration requires `approval: "APPROVE_PAID_CALIBRATION"`, caller-supplied campaign id/time, absolute checkout/executable/campaign paths, explicit models/thinking, repetitions, scenarios, and a positive `maxPaidCalls`; missing input, auth/model failure, or bound risk stops before spend.
- Durable replay uses `OPIN_LIVE_TESTS=1` with `OPIN_REPLAY_ONLY=1`, which authorizes no model call. OSC-14 writes `review-required.json` and campaign evidence but changes no README claim, SKILL pin, or agent pin before human review.

## Exclusive owned paths

- project-level `.skill-creator/<skill-name>/campaign-<campaign-id>/**`
- `tests/opin-skill-creator/test_live_calibration.py`

## Read-only references

- all implementation outputs and frozen contracts
- exact Pi/pi-subagents source revisions
- pre-registered calibration key and workflow args

## Prerequisites

The calibration workflow received `stage: "calibrate"`, `stageStartCommit` equal to the deterministic `implementationIntegrationCommit` returned by the adoption workflow, `approval: "APPROVE_PAID_CALIBRATION"`, absolute paths, campaign id/time, explicit models/thinking, repetitions, maximum paid calls, and campaign directory. Exact-HEAD, clean-tree, model, and auth preflight succeeds before the first measured call. The deterministic full suite is green.

## Red test

Name/path: `tests/opin-skill-creator/test_live_calibration.py::test_live_campaign_metadata_is_complete_and_claims_link_to_records`.

Command:

```bash
OPIN_LIVE_TESTS=1 OPIN_REPLAY_ONLY=1 OPIN_CAMPAIGN_DIR=/absolute/campaign PI_CHECKOUT=/absolute/pi PI_SUBAGENTS_CHECKOUT=/absolute/pi-subagents uvx --from 'pytest==9.1.1' pytest -q tests/opin-skill-creator/test_live_calibration.py::test_live_campaign_metadata_is_complete_and_claims_link_to_records -m live
```

Expected pre-fix failure: no approved Pi-native campaign record exists. This test is red only inside the separately approved calibration run and must pass before its branch tip.

## Required behavior

Pre-register frozen artifacts and grading key. Run only the bounded create, improve, pressure, trigger, inline, fork, bundled-agent, grader, comparator, and runtime-workflow scenarios selected by workflow args. Record requested/effective models/thinking, profiles, prompts, repetitions, Pi revisions, usage/cost, failures, and skipped/bounded work. Produce a bounded `review-required.json` listing every deterministic grading flag and every proposed claim/pin decision. Do not edit README, SKILL, or agent pins in this order; OSC-15 applies only the later human-approved conclusions.

## Implementation steps

1. Write the pre-registration record before any paid call.
2. Preflight exact revisions, auth, model resolution per profile, call bound, and clean output root.
3. Run scenarios without exceeding `maxPaidCalls`; stop on infrastructure invalidation.
4. Validate records with live tests and write `review-required.json`.
5. Stop for human review without changing runtime claims or pins.
6. Run the full deterministic suite and live record checks.

## Deterministic branch-tip gates

```bash
OPIN_LIVE_TESTS=1 OPIN_REPLAY_ONLY=1 OPIN_CAMPAIGN_DIR=/absolute/campaign PI_CHECKOUT=/absolute/pi PI_SUBAGENTS_CHECKOUT=/absolute/pi-subagents uvx --from 'pytest==9.1.1' pytest -q tests/opin-skill-creator/test_live_calibration.py -m live
uvx --from 'pytest==9.1.1' pytest -q tests/opin-skill-creator -m 'not live'
git diff --check
```

## Live-test requirements

Campaign execution is live/credentialed. The branch-tip test is replay-only (`OPIN_REPLAY_ONLY=1`) and must make no model call. No invocation is authorized by repository files alone. Abort before spend when any required arg/preflight is absent.

## Non-goals

Do not exceed the approved bound, benchmark unrelated models, generalize from failed/incomplete campaigns, rewrite historical Claude Code records, or change runtime claims/pins before human review.

## Structured handoff

Return: `order_id`, `status`, `branch`, `commit`, `approval_token_seen`, `campaign_id`, `pre_registered`, `paid_calls_used`, `max_paid_calls`, `models_requested`, `models_effective`, `profiles`, `records`, `manual_reviews`, `bounded_work`, `skipped_work`, `claims_changed`, `pins_changed`, `tests_passed`, `summary`, `blockers`.

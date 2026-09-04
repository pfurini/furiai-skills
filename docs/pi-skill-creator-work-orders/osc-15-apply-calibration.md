# OSC-15: Apply human-approved calibration conclusions

## Findings

No new primary finding. This is the human decision boundary for model/profile-dependent consumers F3-F4, F7-F12, F20, F24, F26-F28, and F35-F37.

## Dependencies

OSC-14 plus a separate human review recorded in an immutable review JSON file. It must precede OSC-16 distribution validation.

## Settled decisions restated

- The separate `finalize` invocation supplies `stageStartCommit` equal to the calibration integration commit whose records the human reviewed. Exact-HEAD preflight requires a clean repository at that stage-start commit; neither the adoption `implementationStartCommit` nor the earlier deterministic `implementationIntegrationCommit` is reused.
- Finalization requires `approval: "APPROVE_CALIBRATION_RESULTS"`, `humanReviewComplete: true`, and an absolute immutable `pi-skill-creator.calibration-review/v1` file. File existence alone is not approval.
- The review record names exact hashed campaign record paths and has `accepted_claims`, `rejected_claims`, `accepted_pins`, and `rejected_pins`. Only accepted entries are applied, without model calls; invalid, rejected, inconclusive, bounded, or skipped evidence cannot support a claim or pin.

## Exclusive owned paths

- `skills/pi-skill-creator/README.md`
- `skills/pi-skill-creator/SKILL.md` only for an explicitly approved creator model/effort pin
- `skills/pi-skill-creator/agents/*.md` only for explicitly approved calibrated model/thinking changes
- `tests/pi-skill-creator/test_calibrated_claims.py`

## Read-only references

- approved campaign records under the project-level campaign directory
- human review JSON supplied by absolute path
- frozen contracts and exact Pi/pi-subagents revisions

## Prerequisites

The calibration workflow is invoked with `stage: "finalize"`, `stageStartCommit` equal to the human-reviewed `calibrationIntegrationCommit` returned by the earlier invocation, `approval: "APPROVE_CALIBRATION_RESULTS"`, `humanReviewComplete: true`, the campaign directory, and absolute `humanReviewRecord`. Preflight requires exact `HEAD` and a clean tree at `stageStartCommit`. The review record identifies accepted/rejected claims and pins by campaign record path; absence or ambiguity fails before edits.

## Red test

Name/path: `tests/pi-skill-creator/test_calibrated_claims.py::test_every_live_claim_and_pin_is_human_approved_and_record_backed`.

Command:

```bash
PI_SKILL_CREATOR_CAMPAIGN_DIR=/absolute/campaign PI_SKILL_CREATOR_HUMAN_REVIEW=/absolute/review.json uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator/test_calibrated_claims.py::test_every_live_claim_and_pin_is_human_approved_and_record_backed
```

Expected pre-fix failure: OSC-14 has produced evidence but runtime claims/pins have not yet been reconciled to the human decision record. This deterministic test makes unsupported or unreviewed claims red before edits and passes at the branch tip.

## Required behavior

Apply only decisions explicitly accepted in the review record. Every new Pi-native number links to a complete campaign record and names its environment profile, effective model/thinking, repetitions, and revisions. Rejected, inconclusive, invalid, bounded, or skipped claims are removed or labeled unsupported, never generalized. Permanent model/effort pins are added or changed only when the review record explicitly approves them. Historical Claude Code evidence remains labeled historical.

No model call, credential use, or new calibration run occurs in this order.

## Implementation steps

1. Validate the review record schema and all referenced campaign files.
2. Add the claim/pin traceability test and observe failure.
3. Apply accepted README claims and approved frontmatter changes.
4. Remove or retain provisional wording exactly as the review record directs.
5. Run claim tests and the full non-live deterministic gate.

## Deterministic branch-tip gates

```bash
PI_SKILL_CREATOR_CAMPAIGN_DIR=/absolute/campaign PI_SKILL_CREATOR_HUMAN_REVIEW=/absolute/review.json uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator/test_calibrated_claims.py
uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator -m 'not live'
git diff --check
```

## Live-test requirements

None. The evidence already exists and has been reviewed by a human.

## Non-goals

Do not run or extend calibration, infer approval from file existence, approve your own findings, alter historical results, or weaken metadata requirements.

## Structured handoff

Return: `order_id`, `status`, `branch`, `commit`, `red_observed`, `human_review_record`, `claims_applied`, `claims_removed`, `pins_applied`, `tests_passed`, `tests_skipped`, `bounded_work`, `skipped_work`, `owned_paths_changed`, `summary`, `blockers`.

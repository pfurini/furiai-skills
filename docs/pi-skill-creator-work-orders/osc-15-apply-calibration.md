# OSC-15: Claim hygiene after the smoke run

## Findings

No new primary finding. This is the human decision boundary for the model-dependent secondary consumers F3, F4, F7, F8, F12, F20, F24, F26 to F28, and F35 to F37, at the scope handoff decision 6 sets: keep historical numbers labelled historical or delete them, add no new numbers, and verify that the grader, comparator, and analyzer pins resolve. Nothing in the smoke record supports a numeric claim or a new pin.

Verified facts this order builds on (source-verified on 2026-09-04; no model call was made):

- `skills/pi-skill-creator/README.md` carries its quantitative material in "Historical evals at a glance" (line 19), "Honest caveats" (lines 67 and 69), and "Method and raw results, concisely" (lines 73 to 142), and states at line 7 that all quantitative results are historical Claude Code evidence. `tests/pi-skill-creator/test_readme.py` (lines 35 to 57) asserts the literal strings `historical Claude Code evidence`, `No Pi-native numeric claim or permanent model pin`, and `approved calibration and human review`, plus the "Runtime requirements", "Honest caveats", and "Distribution" section strings. This order keeps every one of them.
- `agents/benchmark-analyzer.md` lines 44 and 45 contain example percentages inside an output-format example; they are format illustrations, not claims, and stay.
- The bundled-agent pins are grader `openai-codex/gpt-5.6-sol` high, comparator `claude-bridge/claude-opus-5` high, comparison analyzer `openai-codex/gpt-5.6-sol` high, benchmark analyzer `openai-codex/gpt-5.6-terra` medium. `pi --list-models <provider/id>` prints an exact `provider  model` row for a resolvable model without a model call (OSC-18 "Findings").
- The `finalize` stage of `.pi/workflows/pi-skill-creator-calibration.js` keeps its approval mechanics unchanged after OSC-18: `approval: "APPROVE_CALIBRATION_RESULTS"`, `humanReviewComplete: true`, an absolute immutable review record, and `stageStartCommit` equal to the human-reviewed `calibrationIntegrationCommit`.

## Dependencies

OSC-14 plus a separate human review recorded in an immutable review JSON file. It must precede OSC-16 distribution validation.

## Settled decisions restated

- The `finalize` invocation supplies `stageStartCommit` equal to the `calibrationIntegrationCommit` whose smoke records the human reviewed. Exact-HEAD preflight requires a clean repository at that commit; neither the adoption `implementationStartCommit` nor the OSC-18 integration commit is reused.
- Finalization requires `approval: "APPROVE_CALIBRATION_RESULTS"`, `humanReviewComplete: true`, and an absolute immutable `pi-skill-creator.calibration-review/v1` file. File existence alone is not approval.
- The review record names exact hashed campaign record paths and has `accepted_claims`, `rejected_claims`, `accepted_pins`, and `rejected_pins`. For a smoke, `accepted_claims` is limited to the single statement that the machinery works on runtime pi-subagents at the recorded revisions, and `accepted_pins` is typically empty. Only accepted entries are applied, without model calls; invalid, rejected, inconclusive, bounded, or skipped evidence cannot support a claim or pin.
- No new number enters any runtime document. Every existing number is either inside a section labelled historical or removed.
- The pin check is resolution only: a string match of the exact `provider` and `model` row printed by `pi --list-models <provider/id>`; no model call.

## Exclusive owned paths

- `skills/pi-skill-creator/README.md`
- `skills/pi-skill-creator/SKILL.md` only for an explicitly approved creator model/effort pin (none is expected; the creator stays unpinned per decision 5)
- `skills/pi-skill-creator/agents/*.md` only for an explicitly approved pin change (none is expected)
- `tests/pi-skill-creator/test_calibrated_claims.py`

## Read-only references

- the smoke campaign root under the evaluation project (absolute path), including `review-required.json`
- the human review JSON supplied by absolute path
- frozen contracts as amended by OSC-17 and OSC-18, and the exact Pi, pi-subagents, and pi-claude-bridge revisions
- `tests/pi-skill-creator/test_readme.py` (its string assertions are a floor this order keeps)

## Prerequisites

The calibration workflow is invoked with `stage: "finalize"`, `stageStartCommit` equal to the human-reviewed `calibrationIntegrationCommit` returned by the `calibrate` invocation, `approval: "APPROVE_CALIBRATION_RESULTS"`, `humanReviewComplete: true`, `campaignDir` equal to the smoke campaign root, and absolute `humanReviewRecord`. Preflight requires exact `HEAD` and a clean tree at `stageStartCommit`. The review record identifies accepted and rejected claims and pins by campaign record path with hashes; absence or ambiguity fails before edits. The `PI_EXECUTABLE` variable names the pinned Pi executable for the resolution test.

## Red test

Name/path: `tests/pi-skill-creator/test_calibrated_claims.py::test_every_number_is_labelled_historical_or_absent`.

Command:

```bash
PI_SKILL_CREATOR_CAMPAIGN_DIR=/absolute/campaign-smoke-1 PI_SKILL_CREATOR_HUMAN_REVIEW=/absolute/review.json PI_EXECUTABLE=/absolute/bin/pi uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator/test_calibrated_claims.py::test_every_number_is_labelled_historical_or_absent
```

Expected pre-fix failure: the test inventories every README line that carries a result-shaped number (a percentage, an `N/5` or `N of 5` score, a `reps` or `runs` count, or a `vs` comparison) and requires each to sit inside a section whose heading or opening sentence contains `historical`. Before this order, "Honest caveats" line 67 quotes `5/5` and line 69 describes live calibration as pending, outside any historical label, so the test is red. It passes at the branch tip after the caveat wording moves under the historical label or loses its number and after the smoke sentence replaces the pending-calibration sentence.

## Required behavior

Apply only decisions explicitly accepted in the review record. Concretely:

- Inventory every numeric result in `README.md`, `SKILL.md`, and `references/*.md`. Each is either inside a section labelled historical (the label is the word `historical` in the heading or the section's first sentence) or deleted. Do not add a number. Do not rewrite the historical results themselves; the pre-port measurements stay exactly as recorded (README line 142 explains why).
- Replace the "Honest caveats" sentence that says live calibration runs under pi-subagents and that pi-dynamic-workflows execution is verified only with injected runners with a sentence stating that a smoke campaign under pi-subagents at the recorded revisions proved the machinery runs with real models and supports no numeric claim, and that execution under pi-dynamic-workflows remains verified only with injected runners. Keep the strings `SubagentWorkflow`, `pi-dynamic-workflows`, and `names the runtime` in that section, and keep line 7 and line 50 as they are.
- Verify the pins resolve: `test_calibrated_claims.py::test_agent_pins_resolve_without_a_model_call`, marked `contract`, reads each `agents/*.md` frontmatter `model`, runs `<PI_EXECUTABLE> --list-models <provider/id>` with a timeout, and asserts that one printed row has first field equal to the provider and second field equal to the id. It skips with a reason when `PI_EXECUTABLE` is unset and fails on a wrong version. No pin changes unless the review record's `accepted_pins` names it with a record path, and a smoke record supports none.
- `test_calibrated_claims.py::test_review_record_is_smoke_scoped_and_record_backed`: the review record has schema id `pi-skill-creator.calibration-review/v1`, names the campaign id and record hashes that match the files under `PI_SKILL_CREATOR_CAMPAIGN_DIR`, has `accepted_claims` equal to the single machinery statement (or empty), `accepted_pins` empty unless each entry names an existing record path, and every `rejected_claims` entry a non-empty rationale. It fails, not skips, when either variable is unset.
- `test_calibrated_claims.py::test_runtime_documents_carry_no_unreviewed_pin_or_claim`: `SKILL.md` frontmatter has no `model` or `effort`; every `agents/*.md` `model` is one of the four policy pins or an `accepted_pins` entry; no runtime document contains the phrase `calibrated` applied to a Pi model.
- Historical Claude Code evidence remains labelled historical.

No model call, credential use, or new calibration run occurs in this order.

## Implementation steps

1. Validate the review record schema and every referenced campaign file and hash.
2. Add the four tests and observe the red test.
3. Apply the README caveat wording and the historical-label fixes; delete any number that cannot be labelled.
4. Apply an accepted pin only if the review record names one (expected: none).
5. Run the claim tests and the full non-live deterministic gate.

## Deterministic branch-tip gates

```bash
PI_SKILL_CREATOR_CAMPAIGN_DIR=/absolute/campaign-smoke-1 PI_SKILL_CREATOR_HUMAN_REVIEW=/absolute/review.json PI_EXECUTABLE=/absolute/bin/pi uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator/test_calibrated_claims.py
PI_EXECUTABLE=/absolute/bin/pi PI_CHECKOUT=/absolute/pi PI_SUBAGENTS_CHECKOUT=/absolute/pi-subagents PI_DYNAMIC_WORKFLOWS_CHECKOUT=/absolute/pi-dynamic-workflows uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator -m 'not live'
uvx --from 'ty==0.0.77' ty check skills/pi-skill-creator/scripts skills/pi-skill-creator/eval-viewer
git diff --check
```

## Live-test requirements

None. The evidence already exists and has been reviewed by a human. The pin-resolution test makes no model call.

## Non-goals

Do not run or extend calibration, infer approval from file existence, approve your own findings, alter historical results, add a number, pin the creator, or weaken metadata requirements or any `test_readme.py` assertion.

## Structured handoff

Return: `order_id`, `status`, `branch`, `commit`, `red_observed`, `human_review_record`, `claims_applied`, `claims_removed`, `numbers_labelled_historical`, `numbers_removed`, `pins_verified_resolvable`, `pins_applied` (expected `[]`), `tests_passed`, `tests_skipped` (intentionally skipped tests only), `bounded_work` (mandated exclusions only), `skipped_work` (required work left incomplete; must be `[]` on completion), `owned_paths_changed`, `summary`, `blockers`.

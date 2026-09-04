# OSC-14: Smoke-test calibration run under pi-subagents

## Findings

No new primary finding. This order is the evidence gate for the model-dependent secondary consumers F3, F4, F7, F8, F12, F20, F35, and F37, at the scope handoff decision 6 sets: one bounded end-to-end run under pi-subagents whose only purpose is to prove that the machinery (RPC runner, transcript parser, grader, comparator, aggregator, viewer) works with real models. No numeric claim results from it. The record is labelled a smoke test.

Verified facts this order builds on (source-verified on 2026-09-04; no model call was made; OSC-18 records the line references):

- A pi-subagents workflow child cannot run `SubagentWorkflow` and receives no `Agent` tool unless its definition sets `allowed_subagents`. The smoke is therefore driven from the top-level Pi session, not from the calibration workflow. The calibration workflow's `calibrate` stage only validates and integrates what the session produced.
- The RPC runner refuses any Pi checkout other than its pin, so the smoke needs the current pin `db6bee3d6ccb79f5bc7884962ea4d98ca21e60ee` integrated first. OSC-18 re-pinned to `7815e97a0dd5e7eee3cd01858bd5aa0fabeebae0`; the Pi checkout then moved two commits further, and the pin was moved with it during this order rather than rewinding the checkout (see C1 for why the executable is unaffected).
- Under `hermetic-core` the RPC executor runs with `--no-extensions` (`rpc_runner.py` `_RESOURCE_ISOLATION_ARGS`), so the executor must be a model of a built-in Pi provider. `openai-codex` is built in (`packages/ai/src/models.generated.ts`); `claude-bridge` models are unavailable to an RPC executor under this profile.
- Nothing routes files an executor writes into `run-N/outputs/`: the RPC executor's cwd is the evaluation project, and the eval prompt is the same for every run. The smoke therefore asks the executor to return its deliverable in its final assistant message, which `transcript.jsonl` records durably, and the grader grades from the transcript. `outputs/` stays empty and is still created by the runner, which the viewer requires. This is a known gap, recorded in `review-required.json` under `known_gaps` rather than as an anomaly, and its fix is deferred to a later order.
- The aggregator ignores comparison records and rejects unlisted files inside `iteration-N/`, but does not police the campaign root, where OSC-18's C3 amendment places `workflow-result.json` and `comparisons/`.
- Bundled agents are registered by pi-subagents from a skill in one of Pi's skill roots under the unforgeable qualified name `pi-skill-creator:comparator` (`src/agent-types.ts:64`). The `Agent` tool takes `subagent_type`, `prompt`, `description`, and `run_in_background` (`README.md:403-420`); the comparator's frontmatter locks its model and thinking, so the call passes neither.
- `eval-viewer/generate_review.py` has `--static <path>` (`:432-435`) and prints one JSON event line on success.
- `pi --list-models <provider/id>` prints an exact `provider  model` row for `claude-bridge/claude-opus-5` and for `openai-codex/gpt-5.6-sol` without a model call.

## Dependencies

OSC-18 integrated, then explicit human approval of the manifest below. This order produces the record that OSC-15 reviews and OSC-16 requires.

## Settled decisions restated

- Runtime is `pi-subagents` (decision 4). The record names it in `workflow_runtime` and `workflow_runtime_revision`, and a later switch of runtime invalidates nothing here because the smoke supports no numeric claim.
- The smoke is one eval, two arms, one repetition (two is the allowed maximum), one consumer model as executor, one grading per run, one blind comparison, and one static viewer export. The benchmark analyzer and the comparison analyzer are not called.
- `stageStartCommit` for both the `preflight` and `calibrate` stages equals the OSC-18 integration commit. The repository is clean at that commit before and during the run.
- Every paid call is bounded mechanically: `maxAgentCalls` bounds the workflow children, one run directory holds at most one executor process, the comparator is exactly one `Agent` call, and `maxPaidCalls` bounds the sum that the calibrate stage counts from records.
- The human approves the exact manifest object before any call. Documentation never pre-authorizes a run.
- `caffeinate -dimsu pi` launches the session (decision 8), so the machine cannot sleep mid-campaign.
- OSC-14 changes no README claim, SKILL pin, or agent pin. It writes campaign evidence and `review-required.json` and stops for human review.

## Exclusive owned paths

- the campaign root `<evaluation-project>/.skill-creator/release-note-smoke/campaign-smoke-1/**` (outside this repository, referenced by absolute path, never committed)
- `tests/pi-skill-creator/test_live_calibration.py`

## Read-only references

- `HANDOFF-pi-skill-creator.md` decisions 4, 6, and 8 and "Model policy"
- all frozen contracts as amended by OSC-17 and OSC-18
- `skills/pi-skill-creator/references/benchmarking.md`, `references/schemas.md`, `agents/comparator.md`, `agents/grader.md`, `workflows/benchmark.js`
- `tests/pi-skill-creator/fixtures/smoke/release-note-smoke/**` (the smoke target skill, landed by OSC-18 to the specification in "Required behavior" below)
- `.pi/workflows/pi-skill-creator-calibration.js` as rewritten by OSC-18
- pi-subagents `README.md` lines 403 to 433 (`Agent` and `SubagentWorkflow` parameters) and line 230 (`.output` transcript location, cleared on reboot)

## Prerequisites

1. OSC-18 is integrated and the repository is clean at its integration commit. That commit is `stageStartCommit` for both the `preflight` and the `calibrate` stage. Any untracked file that appears in the working tree (for example a tool cache) is removed or ignored before either stage runs.
2. The smoke target skill exists at `tests/pi-skill-creator/fixtures/smoke/release-note-smoke/` because OSC-18 landed it, so it is present at `stageStartCommit`, and it passes `python3 scripts/quick_validate.py <that path>` from the skill directory.
3. The stale directory `~/.agents/skills/pi-skill-creator` (dated 2026-08-12) has been moved by the human to a location outside every Pi skill root (for example `~/pi-skill-creator.stale-2026-08-12`), not deleted, so it stays inspectable. A fresh byte-for-byte copy of `skills/pi-skill-creator/` at `stageStartCommit` is installed with `cp -R` (or `shutil.copytree`) at `~/.pi/agent/skills/pi-skill-creator`, and `diff -r -x __pycache__ skills/pi-skill-creator ~/.pi/agent/skills/pi-skill-creator` prints nothing. This is OSC-16's distribution mode applied to a real root; OSC-16 later proves it from a temporary root.
4. The evaluation project is a temporary directory outside this repository created by the human (for example `/tmp/pi-skill-creator-smoke`), initialized with `git init` and one empty commit, because the setup launcher reads `repository_revision` with `git -C <projectRoot> rev-parse HEAD`. It contains no `.pi/` directory and no `.agents/` directory. The campaign root is `<evaluation-project>/.skill-creator/release-note-smoke/campaign-smoke-1/` per C3 and does not exist before the run.
5. Checkouts are at the pins: Pi `db6bee3d6ccb79f5bc7884962ea4d98ca21e60ee`, pi-subagents `7f569969445bf8bc6fbd7757f18db80b35de0ba9`, pi-claude-bridge `c1d8b24a57e15bc8acc9d673f2804ab7227978ae` (clean), pi-dynamic-workflows `c82d31af1e36b6f0e89cfcc4bdd728d982e22dc9` (not activated: the session must expose `SubagentWorkflow` and not `workflow`).
6. The `preflight` stage of `.pi/workflows/pi-skill-creator-calibration.js` has been run from the repository with the manifest values below and returned `status: 'preflight-passed'` with all four models in `models_resolved`.
7. The Pi session for the smoke is started with `caffeinate -dimsu pi` in the evaluation project directory, so the fresh skill copy loads from the user root and no project configuration interferes.
8. The deterministic full suite is green at `stageStartCommit`.

## Manifest

This is the exact object the human approves before any call. Values in angle brackets are absolute paths the human fills in; everything else is fixed.

```json
{
  "runtime": "pi-subagents",
  "runtimeCheckout": "<pi-subagents checkout>",
  "stageStartCommit": "<OSC-18 integration commit, 40 hex>",
  "campaignId": "smoke-1",
  "createdAt": "<UTC timestamp supplied by the human, YYYY-MM-DDTHH:MM:SSZ>",
  "scenarios": ["runtime-workflow-smoke"],
  "repetitions": 1,
  "maxPaidCalls": 10,
  "models": {
    "executor": { "model": "openai-codex/gpt-5.6-terra", "thinking": "medium" },
    "grader": { "model": "openai-codex/gpt-5.6-sol", "thinking": "high" },
    "comparator": { "model": "claude-bridge/claude-opus-5", "thinking": "high" },
    "benchmarkAnalyzer": { "model": "openai-codex/gpt-5.6-terra", "thinking": "medium" }
  },
  "workflowArgs": {
    "approved": true,
    "runtime": "pi-subagents",
    "runtimeCheckout": "<pi-subagents checkout>",
    "campaignId": "smoke-1",
    "createdAt": "<same timestamp>",
    "projectRoot": "<evaluation project>",
    "skillPath": "<repository>/tests/pi-skill-creator/fixtures/smoke/release-note-smoke",
    "skillCreatorPath": "<home>/.pi/agent/skills/pi-skill-creator",
    "piExecutable": "/Users/paolof/.local/bin/pi",
    "piCheckout": "<pi checkout>",
    "piSubagentsCheckout": "<pi-subagents checkout>",
    "environmentProfile": "hermetic-core",
    "iteration": 1,
    "repetitions": 1,
    "maxAgentCalls": 7,
    "evals": [
      {
        "eval_id": 1,
        "eval_name": "release-note-format",
        "prompt": "Write the release note for version 1.4.0 of the fictional command-line tool ledgerctl. The changes are: (1) a new `export --format csv` option; (2) a fix for a crash when the configuration file is empty; (3) support for Python 3.9 dropped. Return the complete release note as your final message and write no file.",
        "expectations": [
          "The final assistant message contains exactly the three headings Summary, Changes, and Upgrade notes, in that order.",
          "Each of the three listed changes appears as its own bullet under Changes.",
          "The dropped Python 3.9 support is named under Upgrade notes with the action a user must take."
        ]
      }
    ],
    "roles": {
      "executor": { "model": "openai-codex/gpt-5.6-terra", "thinking": "medium" },
      "grader": { "model": "openai-codex/gpt-5.6-sol", "thinking": "high" },
      "comparator": { "model": "claude-bridge/claude-opus-5", "thinking": "high" },
      "benchmarkAnalyzer": { "model": "openai-codex/gpt-5.6-terra", "thinking": "medium" }
    }
  },
  "topLevelCalls": [
    { "role": "comparator", "agent": "pi-skill-creator:comparator", "count": 1 }
  ],
  "viewer": { "static": true, "modelCalls": 0 }
}
```

Notes on the manifest:

- Profile `hermetic-core` is the cheapest profile and the only one whose executor needs no extension. `declared-dependencies` and fork behavior are explicitly out of the smoke.
- The executor is one consumer model from the policy's executor tier (`openai-codex/gpt-5.6-terra`). The grader and comparator are the policy pins. The benchmark analyzer is listed because the workflow requires the role, and it is not called.
- `maxAgentCalls` is the exact plan for one repetition: setup 1 + execute 2 + grade 2 + validate 1 + aggregate 1 = 7. For `repetitions: 2` it is 11 (`3 + 4 × repetitions`).
- `maxPaidCalls` counts every model process the smoke starts: the 7 workflow children (orchestration calls in decision 6's terms: setup, two execute launchers, two graders, validate, aggregate), the 2 measured RPC executor processes (one per `run.json`), and the 1 comparator `Agent` call (a measured judging call), so 10 for one repetition and 16 for two (`6 × repetitions + 4`). The brief that produced this order named 8; that figure omitted the two RPC executor processes, which are separate Pi processes with their own model calls and their own `run.json`, and the calibrate stage counts them. The viewer export makes no model call.
- Estimated tokens: roughly 0.3M to 1.5M across all children, executor processes, and the comparator. This is an estimate for the human's budget decision, not a bound; the bounds are the call counts above.
- `stageStartCommit` and `scenarios` are calibration-workflow inputs, not `workflowArgs`; the workflow tool receives only `workflowArgs`.

## Execution steps

Performed by the human, or by the assistant in the top-level session under the human's instruction, after the manifest is approved and prerequisites 1 to 8 hold.

1. In the `caffeinate -dimsu pi` session, confirm that the `SubagentWorkflow` tool is present and the `workflow` tool is absent. If `workflow` is present, stop: the smoke runs under pi-subagents only.
2. Invoke `SubagentWorkflow` with `scriptPath` equal to `<home>/.pi/agent/skills/pi-skill-creator/workflows/benchmark.js` (the installed copy, never the repository file) and `args` equal to the manifest's `workflowArgs` verbatim. Wait for completion. Fetch the returned object with the task's result tool and save it verbatim, without reformatting, as `<campaign-root>/workflow-result.json`. A `valid: false` result ends the smoke here; the record is still kept and reviewed.
3. Blind comparison from the top-level session. The human flips a coin (outside any model) to assign `A` and `B` to `with_skill/run-1` and `without_skill/run-1`. For each arm, extract the final assistant message text from that run's `transcript.jsonl` (the last `message_end` record whose message role is `assistant`) into `<campaign-root>/comparisons/release-note-format/A/final-message.md` and `.../B/final-message.md`; write `<campaign-root>/comparisons/release-note-format/blind-assignment.json` with the assignment, the source transcript paths, and the SHA-256 of each extracted file. Then call `Agent` with `subagent_type: "pi-skill-creator:comparator"`, no `model`, no `thinking`, and no `run_in_background` (the frontmatter locks all three, and `run_in_background: true` is locked, so the call returns an agent id immediately), and a prompt that supplies `output_a_path` and `output_b_path` as the two neutral directories, `eval_prompt`, `expectations`, and `comparison_path` equal to `<campaign-root>/comparisons/release-note-format/comparison.json`. Wait for the completion notification, then fetch the result with `get_subagent_result` and save its metadata (agent id, reported effective model, `.output` transcript path) as `comparator-agent.json` beside the comparison, copy the `.output` file to `comparator.output` in the same directory (the original lives under the OS temporary directory and is cleared on reboot), and run `python -m scripts.transcript_metrics --format pi-subagents-output-v1 --input <that copy> --output <same dir>/comparator-metrics.json` from the installed skill directory. The metrics file is the evidence that requested and effective comparator model both equal `claude-bridge/claude-opus-5`.
4. Viewer static export, no model call, to a path outside the campaign: `python "<home>/.pi/agent/skills/pi-skill-creator/eval-viewer/generate_review.py" <campaign-root>/iteration-1 --skill-name release-note-smoke --benchmark <campaign-root>/iteration-1/benchmark.json --static <evaluation-project>/smoke-review/review.html`. Record the printed event line in `<evaluation-project>/smoke-review/viewer.log`. The export is a machinery check only.
5. From the repository (clean at `stageStartCommit`), invoke `.pi/workflows/pi-skill-creator-calibration.js` with `stage: "calibrate"`, `stageStartCommit`, `approval: "APPROVE_PAID_CALIBRATION"`, the manifest's `campaignId`, `createdAt`, `repetitions`, `maxPaidCalls`, `models`, and `scenarios`, `campaignDir` equal to the campaign root, `installedSkillPath`, and the absolute executable and checkout paths (`piPath`, `piSubagentsPath`, `piDynamicWorkflowsPath`, `piClaudeBridgePath`). The stage validates the records, writes `review-required.json`, integrates `test_live_calibration.py`, and returns `calibrationIntegrationCommit`.
6. Stop for human review. No README, SKILL, or agent pin changes in this order.

## Records and review

The campaign root holds the C3 tree for one eval, plus `workflow-result.json`, `comparisons/release-note-format/` (blind assignment, the two neutral inputs, `comparison.json`, `comparator-agent.json`, `comparator.output`, `comparator-metrics.json`), and `review-required.json`. The static viewer output and its log live under `<evaluation-project>/smoke-review/`.

`review-required.json` (schema id `pi-skill-creator.review-required/v1`, written by the calibrate stage's child) contains:

- `label: "smoke-test"` and the sentence that the record supports no numeric claim;
- `campaign_id`, `campaign_dir`, `stage_start_commit`, `workflow_runtime`, `workflow_runtime_revision`, `pi_revision`, `pi_subagents_revision`, `pi_claude_bridge_revision`, and `installed_skill_path`;
- `machinery`: one entry per component (`rpc_runner`, `transcript_parser`, `grader`, `comparator`, `aggregator`, `viewer`), each `passed: true|false` with the record path that proves it and a bounded note;
- `effective_models`: requested and observed model and thinking for executor (from each `run.json`), grader (from `workflow-result.json` `effective_roles.grader`), and comparator (from `comparator-metrics.json`), with a flag when requested and effective differ;
- `call_counts`: `workflow_children` (`agent_calls_made`), `executor_processes` (number of `run.json` files), `comparator_calls`, `analyzer_calls: 0`, `viewer_model_calls: 0`, `total`, and `max_paid_calls`;
- `token_usage`: `workflow_output_tokens` from `workflow-result.json`, executor usage summed from `transcript-metrics.json` files, comparator usage from `comparator-metrics.json`, and the note that per-launcher cost is unavailable;
- `anomalies`: every deterministic flag (a failed item, a bounded item, a validation or aggregation failure, an effective-model mismatch, a comparator verdict that reveals provenance);
- `known_gaps`: the sentence that executor deliverables are not routed into `run-N/outputs/` and that the smoke graded from the transcript's final assistant message (not an anomaly; a deferred fix);
- `claim_candidates: []` and `pin_candidates: []`.

The human then writes the immutable `pi-skill-creator.calibration-review/v1` record for OSC-15. For a smoke, `accepted_claims` is limited to "the machinery works on runtime pi-subagents at these revisions", `accepted_pins` is typically empty, and every numeric observation is rejected as a claim.

## Red test

Name/path: `tests/pi-skill-creator/test_live_calibration.py::test_smoke_campaign_replays_and_bounds_paid_calls`.

Command:

```bash
PI_SKILL_CREATOR_LIVE_TESTS=1 PI_SKILL_CREATOR_REPLAY_ONLY=1 PI_SKILL_CREATOR_CAMPAIGN_DIR=/absolute/campaign-smoke-1 PI_SKILL_CREATOR_MAX_PAID_CALLS=10 PI_EXECUTABLE=/absolute/bin/pi PI_CHECKOUT=/absolute/pi PI_SUBAGENTS_CHECKOUT=/absolute/pi-subagents uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator/test_live_calibration.py::test_smoke_campaign_replays_and_bounds_paid_calls -m live
```

Expected pre-fix failure: before the run no campaign directory exists, so the test fails (it must fail, not skip, when `PI_SKILL_CREATOR_CAMPAIGN_DIR` names a missing or incomplete campaign while both opt-in flags are `1`). The module is written during this order and committed by the calibrate stage's integration; it passes at that branch tip against the smoke campaign.

## Required behavior

The smoke target skill `tests/pi-skill-creator/fixtures/smoke/release-note-smoke/SKILL.md` (landed by OSC-18 to this specification): name `release-note-smoke`; a third-person description saying that it writes a release note in a fixed three-section format (Summary, Changes, Upgrade notes) from a list of changes and is used when asked for a release note or changelog entry; a body that gives the template and two rules (every change is its own bullet under Changes; removed platform or version support is named under Upgrade notes with the user's required action). It is a fixture, validates with `quick_validate.py`, and is never distributed.

Write `tests/pi-skill-creator/test_live_calibration.py`, marked `live`, replay-only, no model call, reading `PI_SKILL_CREATOR_CAMPAIGN_DIR` and `PI_SKILL_CREATOR_MAX_PAID_CALLS`:

- `test_smoke_campaign_replays_and_bounds_paid_calls`: `campaign.json` validates (schema id, `workflow_runtime == "pi-subagents"`, `pi_revision`, `pi_subagents_revision`, and `workflow_runtime_revision` equal to `conftest.py` constants, `environment_profile == "hermetic-core"`, `repetitions` 1 or 2); `python -m scripts.aggregate_benchmark <iteration-1> --validate-only` exits 0; `benchmark.json` exists with `metadata.workflow_runtime == "pi-subagents"`; `workflow-result.json` has `valid: true`, `workflow_runtime: "pi-subagents"`, `agent_calls_made <= max_agent_calls`, and `status_counts` summing to `expected_runs`; the counted total (`agent_calls_made` + number of `run.json` files + number of `comparisons/*/comparison.json` files) is at most `PI_SKILL_CREATOR_MAX_PAID_CALLS`.
- `test_smoke_effective_models_match_requested`: every `run.json` has `effective_model` equal to the executor's requested model and a non-empty `effective_thinking`; `workflow-result.json` `effective_roles.grader.models` equals `["openai-codex/gpt-5.6-sol"]`; `comparator-metrics.json` `effective_models` equals `["claude-bridge/claude-opus-5"]`.
- `test_smoke_comparison_is_blind_and_recorded`: `blind-assignment.json` names both arms exactly once, the two neutral input files match their recorded SHA-256, `comparison.json` has `winner` in `A`, `B`, `TIE` and a non-empty `reasoning`, and neither neutral input path contains `with_skill` or `without_skill`.
- `test_smoke_record_is_labelled_and_claims_nothing`: `review-required.json` has `label == "smoke-test"`, `claim_candidates == []`, `pin_candidates == []`, and `call_counts.total <= call_counts.max_paid_calls`.

The tests skip with the existing conftest reason when either opt-in flag is absent, and fail when the flags are set and the campaign is missing or incomplete.

## Implementation steps

1. Confirm the fixture skill is present at `stageStartCommit` (OSC-18 landed it) and validates.
2. Install the fresh skill copy, prepare the evaluation project, and run the `preflight` stage (prerequisites 3, 4, and 6).
3. Present the manifest and obtain approval.
4. Execute steps 1 to 4 of "Execution steps" in the top-level session.
5. Run the `calibrate` stage; it writes the live test and `review-required.json`, runs the replay-only gate, and integrates.
6. Stop for human review.

## Deterministic branch-tip gates

```bash
PI_SKILL_CREATOR_LIVE_TESTS=1 PI_SKILL_CREATOR_REPLAY_ONLY=1 PI_SKILL_CREATOR_CAMPAIGN_DIR=/absolute/campaign-smoke-1 PI_SKILL_CREATOR_MAX_PAID_CALLS=10 PI_EXECUTABLE=/absolute/bin/pi PI_CHECKOUT=/absolute/pi PI_SUBAGENTS_CHECKOUT=/absolute/pi-subagents uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator/test_live_calibration.py -m live
PI_EXECUTABLE=/absolute/bin/pi PI_CHECKOUT=/absolute/pi PI_SUBAGENTS_CHECKOUT=/absolute/pi-subagents PI_DYNAMIC_WORKFLOWS_CHECKOUT=/absolute/pi-dynamic-workflows uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator -m 'not live'
uvx --from 'ty==0.0.77' ty check skills/pi-skill-creator/scripts skills/pi-skill-creator/eval-viewer
git diff --check
```

## Live-test requirements

The campaign execution (execution steps 2 and 3) is live and credentialed and is authorized only by the human's approval of the manifest in the session. The branch-tip tests are replay-only (`PI_SKILL_CREATOR_REPLAY_ONLY=1`) and make no model call. Abort before spend when the `preflight` stage is not green, when `workflow` is present, or when the installed copy differs from `skills/pi-skill-creator/`.

## Non-goals

No multi-family campaign, no multi-turn reasoning harness, no trigger evaluation, no fork or `declared-dependencies` scenario, no benchmark-analyzer or comparison-analyzer call, no numeric claim, no run under pi-dynamic-workflows, no change to README, SKILL, or agent pins, no commit of campaign records, and no second campaign to "fix" a failed smoke (a failed smoke is reviewed as a failed smoke).

## Structured handoff

Return: `order_id`, `status`, `branch`, `commit`, `approval_token_seen`, `campaign_id`, `campaign_dir`, `stage_start_commit`, `workflow_runtime`, `workflow_result_valid`, `paid_calls_used`, `max_paid_calls`, `agent_calls_made`, `max_agent_calls`, `models_requested`, `models_effective`, `machinery` (per-component pass or fail), `records`, `manual_review_required`, `tests_passed`, `tests_skipped` (intentionally skipped tests only), `bounded_work` (mandated exclusions only), `skipped_work` (required work left incomplete; must be `[]` on completion), `claims_changed` (must be `[]`), `pins_changed` (must be `[]`), `summary`, `blockers`.

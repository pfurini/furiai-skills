# OSC-18: Calibration hardening and Pi re-pin

## Findings

No new primary finding number. This order applies handoff decisions 6 and 7 from `HANDOFF-pi-skill-creator.md` and carries the Pi re-pin that the checkout drift forces. It is deterministic (no model call) and must land before the smoke run in OSC-14, because the smoke cannot make a single measured call until the Pi pin moves and because nothing today bounds the number of paid calls mechanically. It is a secondary consumer of F3 (campaign metadata), F7 and F37 (the RPC runner), F12 (workflow dispatch), F15 (the regression suite), and F35 (the workflow-child boundary).

Verified facts this order builds on (source-verified on 2026-09-04; no model call was made):

Pi checkout drift:

- `/Users/paolof/Developer/ai/pi` is at `7815e97a0dd5e7eee3cd01858bd5aa0fabeebae0`, one commit past the pin `a4043c1e332a61e4c8648b97b9b796c57f9db110`. That commit ("fix(ai): increase Codex GPT-5.6 context window") touches only `packages/ai/scripts/generate-models.ts`; `packages/ai/src/models.generated.ts` is unchanged between the two revisions, and `packages/coding-agent/dist/cli.js` was built on 2026-09-03 before the commit, so the executable behaves identically and still reports `0.84.4`.
- `skills/pi-skill-creator/scripts/rpc_runner.py:25` hard-codes `PI_REVISION`, and `validate_runtime` (`:229-232`) refuses any other checkout revision with kind `invalid_runtime`. `scripts/run_eval.py:50` records the same constant. No measured call can therefore happen until both constants move to `7815e97a`.
- Files still carrying the old pin: `tests/pi-skill-creator/conftest.py:14`, `tests/pi-skill-creator/README.md:29`, `contracts.md` C1 (line 9) and the C5 example (line 95), `index.md` pin table, `skills/pi-skill-creator/references/schemas.md:55` and `:221`, `scripts/rpc_runner.py:25`, `scripts/run_eval.py:50`, and `REQUIRED_PI` in `.pi/workflows/pi-skill-creator-adoption.js:20` and `-calibration.js:14`. Historical mentions in OSC-00, OSC-02, OSC-17, the handoff file, and the adoption report stay as they are.

Workflow children cannot orchestrate (pi-subagents `7f569969`):

- A child receives nested `Agent` tools only when its agent definition sets `allowed_subagents` (`README.md:319-346`; `src/agent-runner.ts:879-897`). A `general-purpose` child does load pi-subagents (`extensions: true`), but its `Agent` and `SubagentWorkflow` tools are removed by name (`src/agent-runner.ts:48`, `:271`, `:964`), so `SubagentWorkflow` is never available to a child. The calibration workflow's child therefore cannot run `workflows/benchmark.js` and cannot dispatch the bundled `grader` or `comparator` agents. This is why the smoke campaign is performed from the top-level Pi session (OSC-14) and the calibration workflow's paid-call stage becomes a no-spend validation stage.
- Workflow `agent()` calls default to `agentType` `general-purpose` (`src/workflow/runtime.ts:852`). Both `general-purpose` and `Explore` set `extensions: true` and `skills: true` (`src/default-agents.ts:21-22`, `:35-36`), which `src/agent-runner.ts:671` and `:761` turn into `loadAll`, so the child's `DefaultResourceLoader` discovers the same `~/.pi/agent/settings.json` packages as the host, including `../../Developer/ai/pi-claude-bridge`. A development-workflow child on either default agent type therefore loads `pi-claude-bridge` without any extra option. In the workflow host the script's `model` wins over the agent definition's pin, and a script model that does not resolve makes `agent()` return `null` (`src/workflow/host.ts:200-213`), so an unresolvable `orchestratorModel` fails closed at the preflight child.

No mechanical call bound exists today:

- `rpc_runner.py:532` does `run_dir.mkdir(parents=True, exist_ok=True)`, then (`:537-538`) deletes any stale `run.json`, `transcript-metrics.json`, and `transcript.jsonl` and runs again. A run directory can therefore absorb any number of measured calls.
- `workflows/benchmark.js` after OSC-17 has no call-budget argument. Every child goes through `safeAgent()`, so calls are countable, but nothing counts them.
- `.pi/workflows/pi-skill-creator-calibration.js` compares `maxPaidCalls` only with `paid_calls_used`, a number the child reports about itself.

Skill installation:

- Pi 0.84.4 loads user skills from `<agentDir>/skills` (`core/skills.ts:431`, `~/.pi/agent/skills`) and from `~/.agents/skills` (`core/package-manager.ts:2475`, `:2578-2590`), plus `<cwd>/.pi/skills` and any ancestor `.agents/skills` under a trusted project. Bundled agents register only from a skill in one of these roots.
- `~/.agents/skills/pi-skill-creator` is a stale real directory dated 2026-08-12 (not a symlink) that still contains `agents/analyzer.md` and differs from `skills/pi-skill-creator/` in every reference and agent file (`diff -rq` on 2026-09-04). `~/.pi/agent/skills/` has no `pi-skill-creator`. Because both roots are read, a fresh copy in one root would collide with the stale copy in the other under Pi's same-name resolution, so the stale directory must leave every skill root before the smoke.

Models:

- `pi --list-models [search]` (`cli/args.ts:196`, `:313`) makes no model call. It applies a fuzzy filter over `"<provider> <id>"` (`cli/list-models.ts:49`) and prints one row per model with whitespace-separated columns `provider`, `model`, `context`, `max-out`, `thinking`, `images`. On 2026-09-04, `pi --list-models claude-bridge/claude-opus-5` printed the single row `claude-bridge  claude-opus-5 ...` and `pi --list-models openai-codex/gpt-5.6-sol` printed `openai-codex  gpt-5.6-sol ...`, which proves that the bridge provider is registered before listing. Because the filter is fuzzy, "resolvable" means that some printed row has first field equal to the provider and second field equal to the id, never a substring match on the whole output.
- `~/.pi/agent/settings.json` `enabledModels` contains `openai-codex/gpt-5.6-{luna,sol,terra}`, `claude-bridge/claude-opus-5`, and `claude-bridge/claude-fable-5-1`; `scopeModels` is unset; the default model is `gpt-5.6-luna`. This file is read only and never edited by this order.
- Bundled-agent pins (handoff model policy): grader and comparison analyzer `openai-codex/gpt-5.6-sol` high, comparator `claude-bridge/claude-opus-5` high, benchmark analyzer `openai-codex/gpt-5.6-terra` medium.

Other verified points:

- `eval-viewer/generate_review.py:432-435` defines `--static <path>`, which writes standalone HTML and starts no server, as `benchmarking.md` shows.
- `scripts/aggregate_benchmark.py` never reads comparison records (no `comparison` or `comparator` string in the module). Its `main` (`:753`) accepts `iteration_dir` and `--validate-only` only. It rejects any file at the iteration root other than `benchmark.json`, `benchmark.md`, `feedback.json`, and `viewer.pid` (`:30`, `:495-502`) and any directory other than eval directories, but it reads only `campaign.json` at the campaign root (`:196-230`) and does not police other campaign-root entries.
- The repository at `0b15eda04b14b32fe6a83afe726da72ba56e2de0` is clean (`git status --short --ignored` lists nothing untracked). Every preflight in the development workflows requires `git status --porcelain` to be empty, so any untracked file that appears later (for example a tool cache) must be ignored or removed before a stage runs; this order does not edit `.gitignore`.
- Nothing routes files an executor writes into `run-N/outputs/`: the RPC executor's cwd is the evaluation project (`rpc_runner.py:544`) and the runner only creates the empty directory (`:533`). OSC-14 works around this by grading the final assistant message from the transcript; the routing fix is deferred to a later order and is not in this one's scope.

## Dependencies

OSC-17 is integrated. This order runs before the human approval that precedes the OSC-14 smoke run. OSC-14, OSC-15, and OSC-16 depend on it.

## Settled decisions restated

- Pi is re-pinned to `7815e97a0dd5e7eee3cd01858bd5aa0fabeebae0`, version `0.84.4`. pi-subagents `7f569969445bf8bc6fbd7757f18db80b35de0ba9`, pi-dynamic-workflows `e9c5a41d9c4234df908aa25a2b49ee9648e896d4`, and pi-claude-bridge `c1d8b24a57e15bc8acc9d673f2804ab7227978ae` do not move.
- One run directory is at most one measured executor call. The RPC runner refuses a run directory that already holds `run.json` or `transcript.jsonl`.
- `workflows/benchmark.js` takes a required `maxAgentCalls`, computes the exact plan before the first call, refuses a plan above the bound, and never exceeds the bound at runtime. The bound covers workflow children only; the comparator, any analyzer, and any viewer call made from the top-level session are counted separately in the smoke manifest, and measured RPC executor processes are counted by their `run.json` records.
- Recorded deviation from decision 6's wording. Decision 6 asked for `maxPaidCalls` to be "enforced mechanically before each measured call" inside the calibration workflow. Because that workflow can make no measured call (see above), the pre-call bounds live where the calls are made: `maxAgentCalls` inside `benchmark.js` (checked before every child) and the run-directory refusal inside `rpc_runner.py` (checked before every executor process). The comparator is one top-level `Agent` call bounded by the manifest and counted from its record. `maxPaidCalls` is then compared mechanically with the counted records in the `calibrate` stage after the run. The intent of decision 6 (no spend beyond a mechanical bound) is kept; the location of the check moved.
- The smoke target skill fixture `tests/pi-skill-creator/fixtures/smoke/release-note-smoke/` lands with this order, so the OSC-18 integration commit is the `stageStartCommit` for both `preflight` and `calibrate` and no later commit is needed before the smoke.
- The calibration workflow makes no paid call in any stage. Its three stages are `preflight` (no spend, writes nothing), `calibrate` (validates an already-run smoke campaign, writes `review-required.json`, integrates the replay-only live test), and `finalize` (unchanged mechanics, OSC-15 claim hygiene). The smoke campaign itself runs from the top-level Pi session under the human-approved manifest (OSC-14).
- Calibration inputs have strict schemas: `models` is an object with exactly the role keys `executor`, `grader`, `comparator`, and `benchmarkAnalyzer`, each `{ model: "provider/id", thinking: <minimal|low|medium|high|xhigh|max> }`; `scenarios` is a closed enum and for this program exactly `["runtime-workflow-smoke"]`; `maxPaidCalls` is a positive integer compared mechanically with counted records; `stageStartCommit` is validated as lowercase 40-hex before use and shell-quoted everywhere.
- Every writer prompt in both development workflows states the three-field semantics from decision 7: `tests_skipped` lists intentionally skipped tests only, `bounded_work` lists mandated exclusions only, and `skipped_work` lists required work left incomplete and must be `[]` on completion.
- Integration agents in both development workflows run under the phase of the implementation they integrate; no `Integrate` phase exists. The adoption workflow's enumeration of the 17 original order files stays historical.
- The development workflows stay on pi-subagents and are not ported. Their preflight and calibrate children run on the default agent types, which load `pi-claude-bridge` as verified above.
- The smoke's evaluation project is a directory outside this repository; the campaign root sits under it per C3 and is never committed. Two smoke-only records live at the campaign root (C3 amendment below), and the aggregator ignores both.

## Contract amendments

Executors treat `contracts.md` as frozen and stop on conflicts, so this section gives the exact replacement text. Step 1 of the implementation applies every `contracts.md` replacement below before any other change. The `index.md` rows were applied in the same commit as this order; the executor verifies they are present and does not re-edit them.

### `contracts.md` C1

Replace the bullet

```markdown
- Pi checkout: `/absolute/path` supplied by workflow input, revision `a4043c1e332a61e4c8648b97b9b796c57f9db110`, version `0.84.4`.
```

with:

```markdown
- Pi checkout: `/absolute/path` supplied by workflow input, revision `7815e97a0dd5e7eee3cd01858bd5aa0fabeebae0`, version `0.84.4`. This revision is one commit past `a4043c1e332a61e4c8648b97b9b796c57f9db110` and changes only `packages/ai/scripts/generate-models.ts`; `packages/ai/src/models.generated.ts` is identical at both revisions, and the executable is a pre-commit build with identical behavior that reports `0.84.4`.
```

### `contracts.md` C3

After the paragraph beginning `Eval directory names are descriptive and match` insert:

```markdown
The campaign root may additionally hold `workflow-result.json` (the workflow tool's returned object, saved verbatim by the caller) and a `comparisons/` directory for blind-comparison records made from the top-level session. The aggregator reads neither. `iteration-N/` accepts no file other than `benchmark.json`, `benchmark.md`, `feedback.json`, and `viewer.pid`, and no directory other than eval directories.
```

### `contracts.md` C5

In the `campaign.json` example, replace the line

```json
  "pi_revision": "a4043c1e332a61e4c8648b97b9b796c57f9db110",
```

with:

```json
  "pi_revision": "7815e97a0dd5e7eee3cd01858bd5aa0fabeebae0",
```

### `contracts.md` C9

After the paragraph ending `so leading `@` and `-` survive.` insert:

```markdown
A run directory is at most one measured executor call. When `--run-dir` already contains `run.json` or `transcript.jsonl`, the runner fails with kind `invalid_input` and exit status 2 before launching any process, and it never deletes stale records. A retry needs a new run directory that the campaign plan accounts for.
```

### `contracts.md` C11

After the paragraph beginning `Every `agent()` call goes through `safeAgent()`` insert:

```markdown
`maxAgentCalls` is a required positive integer. Before the first `agent()` call the script computes `agent_calls_planned` as `1` (setup) `+ 2 × scheduled_runs` (one execute launcher and one grader per scheduled run) `+ 1` (validate) `+ 1` (aggregate) and fails argument validation, naming `maxAgentCalls`, when the plan exceeds the bound. At runtime `safeAgent()` counts every call before making it; a call that would exceed the bound is never launched and is accounted as a `bounded` item (`failure_kinds` unchanged). The returned object reports `agent_calls_planned`, `agent_calls_made`, and `max_agent_calls`, and `agent_calls_made` never exceeds `max_agent_calls`. The bound covers workflow children only: the comparator, any analyzer, and any viewer call made from the top-level session are counted separately by the caller's manifest, and measured RPC executor processes are counted by their `run.json` records.
```

### `contracts.md` C12

Replace the sentence

```markdown
The calibration workflow performs paid calls under its explicit bound, then runs this command only to replay and validate durable records.
```

with:

```markdown
The calibration workflow makes no paid call in any stage. The smoke campaign is run from the top-level Pi session under the human-approved manifest, and the workflow's `calibrate` stage then runs this command only to replay and validate the durable records against `PI_SKILL_CREATOR_MAX_PAID_CALLS`.
```

### `contracts.md` C15

Replace the whole section body (everything after the heading `## C15. Calibration workflow stage-start commit`, from `The required `stageStartCommit` argument always names` through `never authorizes the other stage.`) with:

```markdown
The calibration workflow has three stages, each a separate invocation, and makes no paid call in any of them. The required `stageStartCommit` argument is validated as a lowercase 40-hex string before any use, is shell-quoted in every gate, and always names the exact clean repository commit at which that invocation starts:

- for `stage: "preflight"`, it equals the OSC-18 integration commit (the commit at which the smoke will run). Preflight requires no approval token, spends nothing, and writes nothing: it verifies the pins, the clean tree at `stageStartCommit`, the executable version, that every manifest model prints an exact `provider` and `model` row from `pi --list-models <provider/id>`, that the installed skill copy is byte-for-byte equal to `skills/pi-skill-creator/` and is the only copy in Pi's skill roots, and the manifest schema, then returns structured output;
- for `stage: "preflight"`, it equals the OSC-18 integration commit (the commit at which the smoke will run). Preflight requires no approval token, spends nothing, and writes nothing: it verifies the four checkout pins, the clean tree at `stageStartCommit`, the executable version, that every manifest model prints an exact `provider` and `model` row from `pi --list-models <provider/id>`, that the installed skill copy is byte-for-byte equal to `skills/pi-skill-creator/` and is the only copy in the two user skill roots (`~/.pi/agent/skills` and `~/.agents/skills`; project roots under the evaluation project are the human's responsibility and the smoke uses a fresh directory), and the manifest schema, then returns structured output;
- for `stage: "finalize"`, it equals the `calibrationIntegrationCommit` returned by the calibrate invocation, after the human has reviewed that commit's campaign records. Finalize requires `approval: "APPROVE_CALIBRATION_RESULTS"`, `humanReviewComplete: true`, and the absolute immutable human review record.

Preflight for every stage requires repository `HEAD` to equal `stageStartCommit` exactly and the tree to be clean. A commit argument, a prior approval, a preflight result, or review-file existence never authorizes another stage.
```

### `index.md` rows (already applied with this order)

- Pinned-revision table: Pi row at `7815e97a0dd5e7eee3cd01858bd5aa0fabeebae0` with the re-pin note.
- Dependency DAG: `OSC-17 → OSC-18 → HUMAN APPROVAL FOR THE SMOKE RUN → OSC-14 → HUMAN REVIEW OF THE SMOKE RECORD → OSC-15 → OSC-16`.
- Execution waves: wave `8c` for OSC-18 after `8b`; waves 9 and 10 reworded to the smoke and claim-hygiene scope.
- Ownership matrix: OSC-18 as the later owner of every path listed under "Exclusive owned paths" below.
- Human approval checkpoints 3 to 5 and the completion definition: the new stage semantics and the smoke-scope completion bullet.

## Exclusive owned paths

- `skills/pi-skill-creator/scripts/rpc_runner.py`
- `skills/pi-skill-creator/scripts/run_eval.py` (the `PI_REVISION` constant only)
- `skills/pi-skill-creator/workflows/benchmark.js`
- `skills/pi-skill-creator/references/benchmarking.md`
- `skills/pi-skill-creator/references/schemas.md` (example revision values only)
- `.pi/workflows/pi-skill-creator-adoption.js`
- `.pi/workflows/pi-skill-creator-calibration.js`
- `tests/pi-skill-creator/test_calibration_workflow.py` (new)
- `tests/pi-skill-creator/fixtures/calibration-workflow/**` (new)
- `tests/pi-skill-creator/test_rpc_runner.py`
- `tests/pi-skill-creator/fixtures/smoke/release-note-smoke/**` (new; the smoke target skill OSC-14 uses, specified in OSC-14 "Required behavior")
- `tests/pi-skill-creator/test_runtime_workflow.py`
- `tests/pi-skill-creator/fixtures/workflow/**`
- `tests/pi-skill-creator/conftest.py` (the `PI_REVISION` constant only)
- `tests/pi-skill-creator/README.md`
- `docs/pi-skill-creator-work-orders/contracts.md` (the amendments above only)

## Read-only references

- `HANDOFF-pi-skill-creator.md` decisions 4, 6, 7, and 8 and "Model policy"
- all frozen contracts as amended by this order and by OSC-17
- `docs/pi-skill-creator-work-orders/osc-14-live-calibration.md` and `osc-15-apply-calibration.md` (the stages this order must serve)
- pi-subagents at `7f569969`: `README.md` (lines 319 to 346 and 403 to 433), `src/default-agents.ts`, `src/agent-runner.ts` (lines 660 to 790 and 879 to 897), `src/workflow/host.ts`, `src/workflow/runtime.ts`, `src/workflow/worker-source.ts`
- Pi at `7815e97a`: `packages/coding-agent/src/core/skills.ts`, `core/package-manager.ts` (lines 2470 to 2600), `cli/args.ts`, `cli/list-models.ts`, `main.ts` (lines 870 to 875)
- `~/.pi/agent/settings.json` (read only)
- `tests/pi-skill-creator/test_readme.py`, `test_testing_doctrine.py`, and `test_aggregation.py` (their literal-string assertions are a floor this order keeps)

## Prerequisites

- The repository is clean at a commit that contains this order, the amended `index.md`, and the integrated OSC-17 result.
- Checkouts are at the pinned revisions: Pi `7815e97a0dd5e7eee3cd01858bd5aa0fabeebae0` (the checkout's HEAD since 2026-09-04 08:35 UTC; the executable bundle was built on 2026-09-03), pi-subagents `7f569969445bf8bc6fbd7757f18db80b35de0ba9`, pi-claude-bridge `c1d8b24a57e15bc8acc9d673f2804ab7227978ae` (clean), pi-dynamic-workflows `e9c5a41d9c4234df908aa25a2b49ee9648e896d4` with `node_modules/.bin/tsx` from `npm ci`. The executor never moves a checkout.
- OSC-18 is not run by `.pi/workflows/pi-skill-creator-adoption.js`. It is executed as a standalone order, like OSC-17: a fresh writer subagent with no inherited context in an isolated worktree, then a fresh read-only verifier, then integration by the user. The order-level gates below replace the workflow's integration gate.
- Node `v26.8.1`, Python 3.10+, `uvx`, and the Pi executable at `/Users/paolof/.local/bin/pi` are available. No model credentials are needed, and no model call is made.

## Red test

Name/path: `tests/pi-skill-creator/test_rpc_runner.py::test_run_directory_refuses_a_second_measured_call`.

Command:

```bash
uvx --from 'pytest==9.1.1' pytest -q 'tests/pi-skill-creator/test_rpc_runner.py::test_run_directory_refuses_a_second_measured_call'
```

Expected pre-fix failure: with the fake Pi fixture and runtime validation patched out, a second `run_rpc` into the same run directory succeeds and rewrites `run.json`, because `run_rpc` unlinks the stale records at `rpc_runner.py:537-538` instead of raising `RpcRunnerError("invalid_input", ...)`. Four further tests must be observed red in the same session before any fix:

- `test_rpc_runner.py::test_rpc_runner_refuses_the_superseded_pi_revision`: `PI_REVISION` still equals `a4043c1e332a61e4c8648b97b9b796c57f9db110`, and `validate_runtime` accepts a fake checkout whose `git rev-parse HEAD` prints that string.
- `test_runtime_workflow.py::test_runtime_workflow_refuses_plan_above_max_agent_calls[pi-subagents]` and `[pi-dynamic-workflows]`: the script ignores `maxAgentCalls`, runs all seven children, and returns `valid: true`.
- `test_calibration_workflow.py::test_calibration_preflight_refuses_unresolvable_model`: `args.stage` `preflight` is rejected with `args.stage must be calibrate or finalize`.
- `test_calibration_workflow.py::test_adoption_workflow_groups_integration_under_implementation_phase`: every `integrate:*` spawn arrives with `phaseTitle` `Integrate`, and `meta.phases` still lists `Integrate`.

## Required behavior

### 1. Pi re-pin

Move every occurrence of `a4043c1e332a61e4c8648b97b9b796c57f9db110` listed under "Findings" to `7815e97a0dd5e7eee3cd01858bd5aa0fabeebae0`: `PI_REVISION` in `scripts/rpc_runner.py` and `scripts/run_eval.py`, `PI_REVISION` in `conftest.py`, `REQUIRED_PI` in both `.pi/workflows/` files, both example values in `references/schemas.md`, the required-revisions list in `tests/pi-skill-creator/README.md`, and `contracts.md` C1 and C5 through the amendments. `PI_VERSION` stays `0.84.4`. The new test `test_rpc_runner.py::test_rpc_runner_refuses_the_superseded_pi_revision` asserts that `PI_REVISION` equals the new string, that `validate_runtime` raises `RpcRunnerError` with kind `invalid_runtime` for a fake checkout reporting the old string (a temporary git repository or a patched `_command_output` is acceptable), and that it accepts the new string. After this step, the contract tests run against the real checkout at its current HEAD.

### 2. Mechanical call bounds

(a) `scripts/rpc_runner.py`: in `run_rpc`, after `_validate_config` and before any directory creation or process launch, raise `RpcRunnerError("invalid_input", ...)` naming the run directory when `run_dir / "run.json"` or `run_dir / "transcript.jsonl"` exists. Remove the stale-record unlink loop. The CLI maps `invalid_input` to exit status 2 already (`:651`), and no process is launched because the check precedes `_read_rpc_process`. Keep the existing behavior that a failed run leaves `transcript.jsonl` behind (a failed directory is therefore also refused on retry, which is the intent). Tests: the red test above, a CLI variant asserting exit 2 and one bounded stderr line with an existing `run.json`, and no change to the existing success and failure tests beyond fresh run directories.

(b) `workflows/benchmark.js`: add a required positive integer `maxAgentCalls` (`input.maxAgentCalls`; any other value fails with a message naming `maxAgentCalls`). After `scheduledRuns` is known and before the `Prepare` phase, compute `agentCallsPlanned = 1 + 2 * scheduledRuns + 2` and fail argument validation, naming `maxAgentCalls` and both numbers, when it exceeds the bound. Add a counter `agentCallsMade` that `safeAgent()` increments before calling `agent()`; when the increment would exceed `maxAgentCalls`, `safeAgent()` returns `{ status: 'bounded', error: 'bounded: <identity>: max_agent_calls <n> reached' }` without calling `agent()`. A `bounded` result is not a failure: `countFailure()` is never called for it, `failure_kinds` is untouched, the item counts in `status_counts.bounded`, and a bounded validate or aggregate step sets its `stage_statuses` entry to `bounded`. The campaign result is `valid: false` whenever anything was bounded. The returned object (both the setup-failed early return and the final return) gains `agent_calls_planned`, `agent_calls_made`, and `max_agent_calls`. `safeAgent(` remains the only call site of `agent(`; the source-level test's other assertions stay true (no new forbidden literal, no revision literal, no `.filter(Boolean)`).

Fixtures: `fixtures/workflow/valid-args.json` and `valid-args-pi-dynamic-workflows.json` gain `"maxAgentCalls": 7` (the exact plan for one eval, two arms, one repetition). Tests in `test_runtime_workflow.py`, parametrized over both probes:

- `test_runtime_workflow_refuses_plan_above_max_agent_calls`: `maxAgentCalls: 6` is refused at argument validation with no spawn and a message naming `maxAgentCalls`; `maxAgentCalls: 0`, `-1`, `1.5`, a string, and a missing key are refused the same way (extend `_unportable_cases` or add a sibling table).
- `test_runtime_workflow_reports_call_accounting`: the success scenario returns `agent_calls_planned == 7`, `agent_calls_made == 7`, `max_agent_calls == 7`; the `explicit-failure` scenario reports `agent_calls_made == 5` (setup, two executes, one grade, no validate, no aggregate) and the `setup-null` scenario reports `1`.
- `test_runtime_workflow_never_exceeds_max_agent_calls_at_runtime`: a probe scenario that makes the planning count and the runtime count diverge is not reachable through arguments alone, so this test exercises the runtime guard through the source: it asserts that `safeAgent` increments the counter before `agent(` and returns a `bounded` status on overflow (string assertions on `_function_body(source, "safeAgent")`), and that no other function touches the counter. A behavioral variant may drive the guard by parametrizing the fixture with `maxAgentCalls: 7` and a probe that counts host spawns, asserting that the host never sees more than `max_agent_calls` spawns in any scenario.
- `test_runtime_workflow_prompt_sequence_is_runtime_independent` keeps its `7` assertion.

### 3. Calibration workflow hardening

Rewrite `.pi/workflows/pi-skill-creator-calibration.js` around three stages. Shared validation, before any phase: `stage` in the closed enum `preflight | calibrate | finalize`; `stageStartCommit` through a `requireFullCommitSha` helper identical to the adoption workflow's (`/^[0-9a-f]{40}$/`), used only through `shellQuote` (the current `deterministicGate` interpolates it unquoted in `git diff --check ${stageStartCommit}..HEAD`; fix it); absolute `repoPath`, `piPath`, `piSubagentsPath`, `piDynamicWorkflowsPath`, `piClaudeBridgePath`, `piExecutable`, `installedSkillPath`, and `campaignDir`; `orchestratorModel`, `writerModel`, and `integratorModel` as non-empty strings; `REQUIRED_PI`, `REQUIRED_SUBAGENTS`, and new `REQUIRED_DYNAMIC_WORKFLOWS = 'e9c5a41d9c4234df908aa25a2b49ee9648e896d4'` and `REQUIRED_CLAUDE_BRIDGE = 'c1d8b24a57e15bc8acc9d673f2804ab7227978ae'`. The `envPrefix` used by every gate carries `PI_EXECUTABLE`, `PI_CHECKOUT`, `PI_SUBAGENTS_CHECKOUT`, and `PI_DYNAMIC_WORKFLOWS_CHECKOUT`, so the deterministic gate runs the full `not live` suite with no contract test or pi-dynamic-workflows probe skipped (a skip in that gate is a failure, as in this order's own gates). Manifest validation, shared by `preflight` and `calibrate`: `campaignId` matching `[a-z0-9][a-z0-9-]{0,63}`; `createdAt` matching the UTC timestamp form; `repetitions` a positive integer; `maxPaidCalls` a positive integer; `models` an object whose key set is exactly `executor`, `grader`, `comparator`, `benchmarkAnalyzer`, each value an object with exactly `model` matching `/^[^/\s:]+\/[^\s:]+$/` and `thinking` in `minimal, low, medium, high, xhigh, max` (no other key, no `off`); `scenarios` an array equal to `['runtime-workflow-smoke']` (the closed enum has one member for this program; any other length or member fails with a message naming `scenarios`). Approval tokens are unchanged: `preflight` requires none and ignores `approval`; `calibrate` requires `APPROVE_PAID_CALIBRATION`; `finalize` requires `APPROVE_CALIBRATION_RESULTS`, `humanReviewComplete: true`, and absolute `humanReviewRecord`. `meta.phases` becomes `Preflight`, `Calibrate`, `Human checkpoint`, `Distribution` (no `Integrate`), and every integration agent uses the phase of the order it integrates.

`preflight` stage: one read-only child (`agentType: 'Explore'`, `model: orchestratorModel`, `effort: 'low'`) with a gate that mechanically checks: `HEAD` of `repoPath` equals `stageStartCommit`; `git status --porcelain` is empty; the four checkout pins (Pi, pi-subagents, pi-dynamic-workflows, pi-claude-bridge); `test -x piExecutable` and `--version` equals `0.84.4`; `diff -r -x __pycache__ <repoPath>/skills/pi-skill-creator <installedSkillPath>` exits 0; `installedSkillPath` is one of `$HOME/.pi/agent/skills/pi-skill-creator` or `$HOME/.agents/skills/pi-skill-creator` and the other of the two does not exist (the shell's `$HOME` is used unquoted on purpose; project-level skill roots are not checked, and the smoke's evaluation project is a fresh directory); `campaignDir` contains no `campaign.json` yet; and, for each of the four manifest models, `<piExecutable> --list-models '<provider/id>' | awk -v p='<provider>' -v m='<id>' '$1 == p && $2 == m { found = 1 } END { exit !found }'` exits 0 (`--list-models` takes a 15-second internal timeout and makes no model call). The child returns `{ ok, models_resolved, models_unresolved, skill_copy_verified, bounded_work, skipped_work, summary }` with the prompt stating the three-field semantics; the stage throws when the child is `null`, `ok !== true`, `models_unresolved` is non-empty, or `skipped_work` is non-empty, and otherwise returns `{ status: 'preflight-passed', stageStartCommit, manifest: { campaignId, createdAt, repetitions, maxPaidCalls, models, scenarios }, models_resolved, bounded_work, skipped_work: [] }`. It writes nothing and makes no paid call.

`calibrate` stage: the same mechanical preflight gate minus the empty-campaign check, then one writer child (`agentType: 'general-purpose'`, `model: writerModel`, `effort: 'high'`, `isolation: 'worktree'`) that executes OSC-14's validation part: it reads the campaign directory, verifies `workflow-result.json` is present and parses with `valid: true`, `workflow_runtime: 'pi-subagents'`, and `agent_calls_made <= max_agent_calls`; counts the records (`agent_calls_made` from `workflow-result.json`, plus the number of `run.json` files, plus the number of `comparisons/*/comparison.json` files, plus zero analyzer or viewer model calls unless the manifest ledger lists them) and reports the sum as `paid_calls_used`; writes `tests/pi-skill-creator/test_live_calibration.py` (replay-only; OSC-14 specifies it) in the worktree; writes `<campaignDir>/review-required.json` (OSC-14 specifies its content); commits only the test; and returns the OSC-14 structured handoff. The gate is the existing `liveGate` (the replay-only live command with `PI_SKILL_CREATOR_CAMPAIGN_DIR`, `PI_SKILL_CREATOR_MAX_PAID_CALLS`, `PI_EXECUTABLE`, and the checkout variables, followed by the deterministic gate), so the paid-call comparison is mechanical: `test_live_calibration.py` counts the same records and fails when the sum exceeds `PI_SKILL_CREATOR_MAX_PAID_CALLS`. The workflow additionally throws when the child's `paid_calls_used` exceeds `maxPaidCalls` or its `max_paid_calls` differs from the argument, exactly as today. Integration runs under phase `Calibrate`. The return value keeps `calibrationIntegrationCommit`, `campaignId`, `campaignDir`, `paid_calls_used`, `max_paid_calls`, `records`, `manual_review_required`, `bounded_work`, and `skipped_work: []`.

`finalize` stage: unchanged mechanics (OSC-15 then OSC-16, each integrated under its own phase, `Human checkpoint` and `Distribution`). Its prompts gain the three-field semantics and it keeps requiring the immutable review record.

Every writer prompt in this file states: "`tests_skipped` lists intentionally skipped tests only; `bounded_work` lists mandated exclusions only; `skipped_work` lists required work left incomplete and must be `[]` on completion."

The `pi-claude-bridge` question is settled by source, not by an option: the preflight and calibrate children use the default agent types, whose `extensions: true` loads every host-discovered package including `pi-claude-bridge`, and the workflow never sets `isolated`. A comment above the first `agent()` call records this with the `default-agents.ts` and `agent-runner.ts` line references from "Findings", so a future change to `isolated` or to a custom agent type is a visible decision.

Apply decision 7 to `.pi/workflows/pi-skill-creator-adoption.js`: `integrateWave(label, results, gate)` gains a `phaseName` parameter and passes it as `phase` for the integration agent; every call site passes its implementation phase (`Foundation`, `Contracts`, `Core`, `Models`, `Execution`, `Doctrine`, `Runtime workflow`, `README`); `meta.phases` drops `Integrate`; the `runOrder` and `integrateWave` prompts state the three-field semantics; `REQUIRED_PI` moves. `REQUIRED_HANDOFF_FILES` and its 17-file enumeration stay exactly as they are (historical).

### 4. Tests

New module `tests/pi-skill-creator/test_calibration_workflow.py`, marked `contract`, executing both development workflows through the same pinned pi-subagents stub host as `test_runtime_workflow.py` (the compiled `runtime.js` from the `workflow_runtime_modules` fixture, a `spawnAgent` stub that records `label`, `phaseTitle`, `agentType`, `model`, `effort`, `gate`, and `isolation`, and a `runGate` stub that records commands and returns `ok` unless the scenario says otherwise). Fixture arguments live in `fixtures/calibration-workflow/` (`preflight-args.json`, `calibrate-args.json`, `finalize-args.json`, `adoption-args.json`) with `/tmp/...` absolute paths and a valid 40-hex `stageStartCommit`. Required tests:

- `test_calibration_workflow_refuses_missing_or_wrong_approval` for `calibrate` and `finalize`, and asserts that `preflight` runs without `approval`.
- `test_calibration_workflow_refuses_bad_stage_start_commit`: a 7-hex prefix, uppercase hex, a trailing newline, and a shell metacharacter string are all refused before any spawn; for a valid value, every recorded gate command contains the single-quoted commit and never the bare `..HEAD` form.
- `test_calibration_workflow_refuses_bad_models_and_scenarios`: a missing role key, an extra role key, `thinking: "off"`, a model with a `:thinking` suffix, `scenarios: []`, `scenarios: ["runtime-workflow-smoke", "other"]`, and `scenarios: ["create"]` are each refused with a message naming `models` or `scenarios`.
- `test_calibration_preflight_refuses_unresolvable_model`: the `runGate` stub returns `{ ok: false }` for the gate whose command contains `--list-models 'fixture/unavailable'`, the preflight child therefore returns `null`, and the run fails with `preflight failed closed`; in the success scenario the stage returns `status: 'preflight-passed'`, spawns exactly one child, and the recorded gate contains one `--list-models` invocation per manifest model with the `awk` exact-row match.
- `test_calibrate_refuses_call_count_above_max_paid_calls`: the stub child returns `paid_calls_used: 11` against `maxPaidCalls: 10`, and the run fails with `Paid-call bound mismatch` after exactly one preflight spawn and one calibrate spawn (no integration spawn); the success scenario spawns preflight, calibrate, and `integrate:OSC-14` with `phaseTitle` `Calibrate` and returns `calibrationIntegrationCommit`.
- `test_calibration_workflow_makes_no_paid_call_prompt`: every recorded calibrate prompt contains the string `no model call` (or the exact wording the executor chooses and asserts), and no prompt contains `Never exceed maxPaidCalls` as a spending instruction.
- `test_adoption_workflow_groups_integration_under_implementation_phase`: the stub returns a valid `HANDOFF` object for every `OSC-*` label and a valid `INTEGRATION` object for every `integrate:*` label; the parsed meta has no `Integrate` phase; every `integrate:<wave>` spawn carries the `phaseTitle` of the orders it integrates; the run returns `status: 'ready-for-calibration'`.
- `test_development_workflow_prompts_state_three_field_semantics`: every writer or integrator prompt in both workflows contains `tests_skipped`, `bounded_work`, and `skipped_work` with the semantics sentence.

Extend `test_rpc_runner.py` (the two new tests above) and `test_runtime_workflow.py` (the `maxAgentCalls` tests above). OSC-18 becomes the later owner of both modules and of `fixtures/workflow/**`.

### 5. Docs

`references/benchmarking.md`: in "Approval and campaign inputs" add `maxAgentCalls` to the supplied values with its formula (`1 + 2 × scheduled runs + 2`) and the statement that the bound covers workflow children only; add `maxAgentCalls: 7` to both invocation shapes; in "Execution, grading, and telemetry" state that a run directory holds at most one measured executor call and that the runner refuses a directory with an existing `run.json` or `transcript.jsonl`; state that the returned object reports `agent_calls_planned`, `agent_calls_made`, and `max_agent_calls`. `references/schemas.md` and `tests/pi-skill-creator/README.md` carry the Pi re-pin; the README also names `test_calibration_workflow.py` under the contract tier. Keep every literal string OSC-17's keep-list names (`test_runtime_workflow.py::test_benchmark_contract_prose_matches_runtime`, `test_readme.py` lines 35 to 57, `test_testing_doctrine.py` lines 36 to 39 and 62, `test_aggregation.py` line 323), including the pre-existing em dash in the `SKILL.md` Step 7 heading, which this order does not touch.


### 6. Smoke target skill fixture

Write `tests/pi-skill-creator/fixtures/smoke/release-note-smoke/SKILL.md` exactly as OSC-14 "Required behavior" specifies (name `release-note-smoke`, a third-person description, the three-section template, the two rules). It must pass `python3 scripts/quick_validate.py <that path>` from the skill directory, and `test_calibration_workflow.py` gains `test_smoke_fixture_skill_validates`, which runs that validator on the fixture and asserts the frontmatter name. The fixture is never distributed and is not loaded by any test through Pi.
## Implementation steps

1. Apply every `contracts.md` replacement from "Contract amendments"; verify the `index.md` rows are present.
2. Add the red tests and fixtures (`test_rpc_runner.py`, `test_runtime_workflow.py`, `test_calibration_workflow.py`, `fixtures/calibration-workflow/**`, the `maxAgentCalls` fixture keys); run the red commands and record the observed failures.
3. Re-pin Pi in `rpc_runner.py`, `run_eval.py`, `conftest.py`, both `.pi/workflows/` constants, `schemas.md`, and `tests/pi-skill-creator/README.md`; run the contract tests against the real checkout.
4. Implement the run-directory refusal in `rpc_runner.py`.
5. Implement `maxAgentCalls` in `benchmark.js`.
6. Rewrite `pi-skill-creator-calibration.js` (three stages, schemas, quoting, phases, prompts) and apply decision 7 to `pi-skill-creator-adoption.js`.
7. Update `benchmarking.md` and the two README-level documents; write the smoke target skill fixture and its validation test.
8. Search the repository for `a4043c1e` outside the historical files named in "Findings", for `phase: 'Integrate'`, and for an unquoted `stageStartCommit` interpolation; run the full gates.

## Deterministic branch-tip gates

```bash
PI_EXECUTABLE=/absolute/bin/pi PI_CHECKOUT=/absolute/pi PI_SUBAGENTS_CHECKOUT=/absolute/pi-subagents PI_DYNAMIC_WORKFLOWS_CHECKOUT=/absolute/pi-dynamic-workflows uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator/test_runtime_workflow.py tests/pi-skill-creator/test_calibration_workflow.py tests/pi-skill-creator/test_rpc_runner.py tests/pi-skill-creator/test_bundled_agents.py tests/pi-skill-creator/test_aggregation.py
PI_EXECUTABLE=/absolute/bin/pi PI_CHECKOUT=/absolute/pi PI_SUBAGENTS_CHECKOUT=/absolute/pi-subagents PI_DYNAMIC_WORKFLOWS_CHECKOUT=/absolute/pi-dynamic-workflows uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator -m 'not live'
uvx --from 'ty==0.0.77' ty check skills/pi-skill-creator/scripts skills/pi-skill-creator/eval-viewer
git diff --check
```

From the skill directory, `python3 scripts/quick_validate.py .` must also pass. All four checkout variables are set in the first two commands, and no contract test or pi-dynamic-workflows probe may be skipped there; a skip is a gate failure. No Pi, pi-subagents, pi-claude-bridge, or pi-dynamic-workflows checkout may be modified; the untracked, ignored `node_modules/` from `npm ci` in pi-dynamic-workflows is the only allowed change there.

## Live-test requirements

None. No model call is made. The `--list-models` resolution of the smoke models is exercised only through the stub host in tests; the real command runs in the `preflight` stage before OSC-14.

## Non-goals

Do not run the smoke campaign, install the skill copy, edit `~/.pi/agent/settings.json` or `.gitignore`, port the development workflows to pi-dynamic-workflows, change the campaign schema id, add numeric claims, change any bundled-agent pin, add Claude Code compatibility, or rewrite the adoption workflow's order enumeration.

## Structured handoff

Return: `order_id`, `status`, `branch`, `commit`, `red_observed`, `pi_repinned`, `run_dir_refusal_verified`, `max_agent_calls_verified_pi_subagents`, `max_agent_calls_verified_pi_dynamic_workflows`, `calibration_stages` (must be `["preflight", "calibrate", "finalize"]`), `adoption_phases_regrouped`, `smoke_fixture_validated`, `contracts_amended`, `tests_passed`, `tests_skipped` (intentionally skipped tests only), `bounded_work` (mandated exclusions only), `skipped_work` (required work left incomplete; must be `[]` on completion), `owned_paths_changed`, `summary`, `blockers`.

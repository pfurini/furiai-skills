# OSC-17: Orchestrator-independent benchmark workflow

## Findings

No new primary finding number. This order applies handoff decisions 1, 3, and 4 from `HANDOFF-pi-skill-creator.md`: the runtime workflow `skills/pi-skill-creator/workflows/benchmark.js` must run unchanged on two workflow runtimes (pi-subagents through its `SubagentWorkflow` tool and pi-dynamic-workflows through its `workflow` tool), the blind comparator moves to `claude-bridge/claude-opus-5`, and every campaign record names the runtime it ran under. It takes over two resolutions from OSC-06 for the workflow path only: F12 (bundled agents are no longer dispatched by `agentType` inside the workflow) and F20 (the comparator pin and its extension loading). It is a secondary consumer of F3 (campaign metadata gains runtime fields), F4, F7, F8, F17, and F35 (the workflow-child telemetry boundary now covers both runtimes). It also carries the pi-subagents re-pin from `bfa262fd` to `7f569969`.

Verified runtime facts this order builds on (source-verified on 2026-09-04; no model call was made):

pi-subagents at `7f569969445bf8bc6fbd7757f18db80b35de0ba9` (version 0.19.0):

- `agent()` accepts exactly the option keys `label`, `phase`, `model`, `agentType`, `isolation`, `gate`, `resume`, `effort`, `schema` (`src/workflow/worker-source.ts:324-334`); any other key throws at the call (`:449-457`). `effort` is validated against `minimal, low, medium, high, xhigh, max` (`:312`, `:480-482`); there is no `off`.
- `model` is plain text. A `provider/id:thinking` string is not rejected by name. It reaches `resolveModel` (`src/model-resolver.ts:40-118`), where the exact match needs the suffixed key in the available set, the fuzzy match splits on `[\s\-/]+` so `5:high` survives as one part that no id, name, or provider contains, and the provider-fallback retry (`:107-110`) fails the same way; `src/workflow/host.ts:206-210` then returns `{ ok: false }` and the script receives `null` for that agent. The failure mode of a wrong shim is therefore a silent `null`, not a loud error. Schema failures and spawn failures also return `null` (`worker-source.ts:539-548`; the combinators at `:557-604` propagate it).
- `parallel(thunks)` and `pipeline(items, ...stages)` live at `worker-source.ts:557` and `:586`; a stage receives `(previousValue, originalItem, index)`; a stage that throws a non-fatal error yields `null` for that item.
- The `meta` parser (`src/workflow/meta.ts`) accepts `name`, `description`, `whenToUse`, and `phases[{ title, detail?, model? }]`.
- The tool is `SubagentWorkflow` with `scriptPath` (wins over `script` and `name`), `args` passed verbatim, and `resumeFromRunId` (`README.md:428-432`).
- Workflow children expose no transcript path and no per-child cost, so contract C8 stays true.
- The only commit after `bfa262fd` makes the workflow-tool collision check case-insensitive (`src/workflow/collisions.ts:61`, `:101`, `:106`), which is what lets `SubagentWorkflow` stand down beside pi-dynamic-workflows' lowercase `workflow` tool.
- An agent definition's `extensions: [<name>]` allowlist matches an extension by its path-derived canonical name and, when a package manifest declares the entry, by the package's unscoped name (`src/agent-runner.ts:57-63`, `:85-126`). pi-claude-bridge is loaded from `/Users/paolof/Developer/ai/pi-claude-bridge` through `~/.pi/agent/settings.json` `packages`, and its `package.json` declares `pi.extensions: ["./src/index.ts"]` with name `pi-claude-bridge`, so the allowlist name is `pi-claude-bridge` (the path-derived name would be `src`, which no file may use).

pi-dynamic-workflows at `e9c5a41d9c4234df908aa25a2b49ee9648e896d4` (version 3.10.0):

- `agent()` options are `label`, `phase`, `schema`, `model`, `tier`, `isolation`, `thread`, `agentType`, `timeoutMs`, `retries` (`src/workflow.ts:324-365`). Unknown keys are silently ignored (`docs/parity/gap-analysis.md` section 2), so an `effort` key is dropped without warning and the child runs at the default thinking level.
- Thinking is expressed only as a `:thinking` suffix on `model` (`provider/id:high`), parsed by `resolveModelSpecWithThinking` in `src/model-spec.ts:213` with levels `off, minimal, low, medium, high, xhigh, max` (`:4`). An explicit `model` that does not resolve throws `WorkflowError` `MODEL_NOT_FOUND` with `recoverable: false` (`src/agent.ts:906-943`); it never falls back.
- A schema failure throws `SCHEMA_NONCOMPLIANCE` (non-recoverable) after bounded repair (`src/agent.ts:127`, `:163-170`). Recoverability is a per-instance flag, not a property of the code: `src/errors.ts:83` defaults `recoverable` to `false`, and `wrapError` (`:167`) passes an existing `WorkflowError` through unchanged. In `parallel()` and `pipeline()` (`src/workflow.ts:1013-1085`) a non-recoverable error that escapes a stage halts the whole run, so the script must catch inside the stage. `agent()` throws are ordinary JavaScript exceptions (`src/workflow.ts:936-998`) that a `try/catch` in the script contains; the run-level abort fires only in the top-level catch (`:1454-1469`), so a caught throw does not seal the run. A recoverable error that exhausts its attempts makes `agent()` return `null` (`src/workflow.ts:990-995`), so `null` results exist on this runtime too.
- `parallel()` requires an array of functions, not promises (`src/workflow.ts:1013-1017`); `pipeline(items, ...stages)` stages receive `(prev, original, index)` (`:1051`).
- `meta` validation (`src/workflow.ts:1611-1625`) requires `name` and `description`, accepts optional `model` and `phases[]` with a `title` each, and does not reject extra keys. The shared subset this order requires is exactly `meta { name, description, phases: [{ title }] }`; `whenToUse` and `detail` are dropped.
- The extension entry hands the host session's `ctx.modelRegistry` to the workflow manager on session start (`extensions/workflow.ts:303-304`); `src/agent.ts:722-733` uses that shared registry for child resolution and `src/agent.ts:968-989` passes the registry's runtime into each child's `createAgentSession`. pi-claude-bridge registers its `claude-bridge` provider on that host registry with `pi.registerProvider` and mirrors the API into pi-ai's process-global API registry (`/Users/paolof/Developer/ai/pi-claude-bridge/src/index.ts:2472-2496`). Therefore `claude-bridge/claude-opus-5:high` resolves for a pi-dynamic-workflows child whenever pi-claude-bridge is loaded in the host session. Children in pi-dynamic-workflows load no extensions at all (gap analysis section 5), so the bridge is reached only through the shared registry.
- `~/.pi/agent/settings.json` `enabledModels` contains `claude-bridge/claude-opus-5` and `claude-bridge/claude-fable-5-1`. pi-dynamic-workflows enforces that list for caller-supplied models; pi-subagents enforces it only when its `scopeModels` setting is on (`src/model-scope.ts:19-21`, off by default; gap analysis section 8).
- The tool is `workflow` with `script` (the file content; there is no `scriptPath`), `args` (an object), and `resumeFromRunId`; `name` selects saved or built-in workflows and must not be used (`src/workflow-tool.ts:27-60`, `:174`, `:201-218`). The tool description states it runs only on explicit user opt-in (`WORKFLOW_GATE_GUIDELINE`, `src/workflow-tool.ts:24-25`); the approval the skill already obtains is that opt-in.
- `agent()` passes a plain JSON-schema object straight through as the `structured_output` tool's parameters after checking its `type` (`src/agent.ts:875-888`, `src/structured-output.ts:36`). The script's schemas all declare `type: 'object'`.
- Test seam: `runWorkflow(script, options)` is exported from `src/workflow.ts:436`. `options.agent` is a `WorkflowAgentRunner` (`:166-168`) whose `run(prompt, options)` receives `AgentRunOptions` (`src/agent.ts:487` onward) including `label`, `schema`, and the raw `model` string (`src/workflow.ts:863`); `options.agentRegistry` is a `Map` (`src/agent-registry.ts:49`) and an empty one keeps the probe hermetic; `options.persistLogs: false` writes nothing; `options.runId`, `options.onAgentJournal`, and `options.resumeJournal` (keyed `${entry.runId}:${entry.index}`) give a resume seam, demonstrated by `tests/workflow-runtime.test.ts:644-669`. The result is `{ meta, result, logs, phases, agentCount, durationMs, runId, tokenUsage? }` (`src/workflow.ts:306-322`); a failed run rejects instead of returning a status. Running it from Python needs TypeScript execution: the prerequisite is `npm ci` in that checkout and `node_modules/.bin/tsx` (`tsx` is a devDependency; Node is `v26.8.1`).

## Dependencies

OSC-13 and everything it depends on are integrated. This order runs before the human approval that precedes OSC-14, so calibration records already carry the runtime fields.

## Settled decisions restated

- pi-dynamic-workflows becomes the primary workflow extension in the user's framework. pi-subagents stays installed for its `Agent` tool; its `SubagentWorkflow` stands down when both are loaded. The skill must work on both runtimes, so `benchmark.js` uses only the shared subset: `meta { name, description, phases: [{ title }] }`, `phase()`, `agent()`, `parallel()`, `pipeline()`, `log()`, `args`, and `budget.spent()`, with `agent()` options limited to `label`, `phase`, `schema`, and `model`, plus the `effort` key that the shim emits for pi-subagents only.
- Requested thinking levels are the same closed set on both runtimes: `minimal, low, medium, high, xhigh, max`. `off` is refused at argument validation for every role, because pi-subagents cannot express it through `effort` and a level accepted on one runtime only would make campaigns non-portable. `off` stays an accepted effective value in the result checks, because a model may clamp thinking to off.
- One runtime shim keyed on a validated `args.runtime` (closed enum `pi-subagents` | `pi-dynamic-workflows`) is the only place that knows the runtimes differ. For `pi-subagents` it passes `model: "<provider/id>"` plus `effort: "<thinking>"`; for `pi-dynamic-workflows` it passes `model: "<provider/id>:<thinking>"` and no `effort` key.
- `safeAgent()` wraps every `agent()` call; a `null` result and a thrown error both become accounted `failed` items. No `gate:` option; Python validation is the authority through a new `aggregate_benchmark --validate-only` step. No `agentType`; role prompts tell the child to read the skill's `agents/<role>.md` by absolute path, with model and thinking from `args.roles`. No worktree isolation for launchers.
- Campaign records name the runtime (`workflow_runtime`, `workflow_runtime_revision`). Every benchmark claim names its runtime; switching runtimes invalidates numeric claims until the campaign is re-run.
- The blind comparator is `claude-bridge/claude-opus-5` at `high` thinking (`max` may be requested for critical skills). `agents/comparator.md` loads only `pi-claude-bridge`. Requested and effective model must both equal `claude-bridge/claude-opus-5`; an unresolved pin fails. For Claude-produced outputs this comparator is not family-independent, and the campaign record says so.
- pi-subagents is re-pinned to `7f569969445bf8bc6fbd7757f18db80b35de0ba9`. The pins are Pi `a4043c1e332a61e4c8648b97b9b796c57f9db110` (unchanged), pi-dynamic-workflows `e9c5a41d9c4234df908aa25a2b49ee9648e896d4`, and pi-claude-bridge `c1d8b24a57e15bc8acc9d673f2804ab7227978ae`.
- Live calibration (OSC-14) runs under `runtime: pi-subagents`. The development workflows in `.pi/workflows/` stay on pi-subagents and are not ported; only their pin constants change.
- The creator stays unpinned. No Claude Code compatibility enters the skill or the workflow.

## Contract amendments

Executors treat `contracts.md` as frozen and stop on conflicts, so this section gives the exact replacement text. Step 1 of the implementation applies every `contracts.md` replacement below before any other change. The `index.md` rows were applied in the same commit as this order; the executor verifies they are present and does not re-edit them.

### `contracts.md` C1

Replace the bullet beginning `- pi-subagents checkout:` with:

```markdown
- pi-subagents checkout: `/absolute/path` supplied by workflow input, revision `7f569969445bf8bc6fbd7757f18db80b35de0ba9`, version `0.19.0`. This revision differs from `bfa262fdd75d807b1c6b1f852f1f1bea2bbb3fa4` only by the case-insensitive workflow-tool collision check in `src/workflow/collisions.ts`, which lets `SubagentWorkflow` stand down beside pi-dynamic-workflows' `workflow` tool.
- pi-dynamic-workflows checkout: `/absolute/path` supplied by the `PI_DYNAMIC_WORKFLOWS_CHECKOUT` test input and by the runtime workflow's `runtimeCheckout` argument, revision `e9c5a41d9c4234df908aa25a2b49ee9648e896d4`, version `3.10.0`. Tests that execute through it require `node_modules/.bin/tsx` produced by `npm ci` in that checkout; that directory is covered by the checkout's `.gitignore` and is the only permitted change there.
- pi-claude-bridge: loaded in the host session from `/absolute/path/pi-claude-bridge` through `~/.pi/agent/settings.json` `packages`, revision `c1d8b24a57e15bc8acc9d673f2804ab7227978ae`, version `0.7.0`. Its extension allowlist name under pi-subagents is `pi-claude-bridge`, the package manifest name (`src/agent-runner.ts:85-126`).
```

Replace `- Runtime skill code remains Python 3.10+ standard library plus one plain-JavaScript runtime workflow.` with:

```markdown
- Runtime skill code remains Python 3.10+ standard library plus one plain-JavaScript runtime workflow that runs unchanged on both pinned workflow runtimes.
```

### `contracts.md` C5

In the `campaign.json` example, replace the line `"pi_subagents_revision": "bfa262fdd75d807b1c6b1f852f1f1bea2bbb3fa4",` with:

```json
  "pi_subagents_revision": "7f569969445bf8bc6fbd7757f18db80b35de0ba9",
  "workflow_runtime": "pi-subagents",
  "workflow_runtime_revision": "7f569969445bf8bc6fbd7757f18db80b35de0ba9",
```

In the same example, replace `"requested_model": "openrouter/~anthropic/claude-opus-latest",` with:

```json
      "requested_model": "claude-bridge/claude-opus-5",
```

Replace the paragraph beginning `` `created_at` is an input, not generated inside a workflow. `` with:

```markdown
`created_at` is an input, not generated inside a workflow. `workflow_runtime` is `pi-subagents` or `pi-dynamic-workflows` and names the runtime that executed `workflows/benchmark.js`; `workflow_runtime_revision` is the lowercase 40-hex `HEAD` of that runtime's checkout, read with `git -C <runtimeCheckout> rev-parse HEAD` by the setup launcher, never invented. Both fields are required. A campaign supports claims only for the runtime it records; a run under the other runtime is a new campaign. The schema id stays `pi-skill-creator.campaign/v1` because no v1 record exists outside test fixtures. Role entries not used by a campaign are omitted. All paths in durable metadata are absolute or campaign-root-relative as shown; ambiguous cwd-relative paths are rejected.
```

### `contracts.md` C8

After the sentence `Therefore no implementation may claim a workflow-child transcript path or per-child cost.` insert:

```markdown
The same boundary holds for pi-dynamic-workflows: a `workflow` child returns only the value its runner produced, and the script receives no transcript path, usage, or effective model (`docs/parity/gap-analysis.md` section 7 in that checkout). Both runtimes therefore treat RPC `run.json` and `transcript-metrics.json` as the only executor evidence.
```

### `contracts.md` C10

Replace the paragraph `The provisional comparator is ... fallback-to-parent is not accepted.` with:

```markdown
The comparator is `claude-bridge/claude-opus-5` at `high` thinking (`max` may be requested per campaign for critical skills). `agents/comparator.md` sets `extensions: [pi-claude-bridge]`, because a pi-subagents child with `extensions: false` has no `claude-bridge` provider in its registry. The grader and both analyzers keep `extensions: false`. Campaign preflight must prove the pin resolves in the selected profile; requested and effective model must both equal `claude-bridge/claude-opus-5`. Failure to resolve is fatal; fallback-to-parent is not accepted. For outputs produced by Claude-family executors this comparator is not family-independent; the campaign record states this, and no audit campaign is added.

Agent frontmatter (`tools`, `extensions`, `max_turns`, and the rest) governs the top-level `Agent` path only. The runtime workflow does not dispatch bundled agents by `agentType`; see C11.
```

### `contracts.md` C11

Replace the second and third paragraphs (from `The runtime workflow requires caller-provided` through `it is never dropped by `.filter(Boolean)` without an explicit count.`) with:

```markdown
The runtime workflow requires caller-provided `campaignId`, `createdAt`, absolute `projectRoot`, `skillPath`, `skillCreatorPath`, `piExecutable`, `piCheckout`, `piSubagentsCheckout`, and `runtimeCheckout`, a `runtime` from the closed enum `pi-subagents` | `pi-dynamic-workflows`, environment profile, eval array, iteration, repetitions, role models/thinking, and `approved: true`. When `runtime` is `pi-subagents`, `runtimeCheckout` must equal `piSubagentsCheckout`. Requested thinking for every role is one of `minimal, low, medium, high, xhigh, max`; `off` is refused. The skill obtains approval before the tool call; the workflow also refuses absent approval and an unknown runtime. `piSubagentsCheckout` stays required because `declared-dependencies` still loads pi-subagents through `scripts.rpc_runner --extension <checkout>/src/index.ts`, which the runner passes to Pi as `-e`.

The skill invokes the script through `SubagentWorkflow` with `scriptPath` when only that tool is present, or through `workflow` with the file content passed as `script` when pi-dynamic-workflows is loaded (its presence makes `SubagentWorkflow` stand down). The `workflow` tool's `name` input is never used.

The script uses only the subset both runtimes implement: `meta { name, description, phases: [{ title }] }`, `phase()`, `agent()`, `parallel()`, `pipeline()`, `log()`, `args`, and `budget.spent()`. `agent()` options are only `label`, `phase`, `schema`, and `model`, plus `effort` emitted by the shim for pi-subagents. One shim function keyed on `args.runtime` is the only code that knows the runtimes differ: for `pi-subagents` it passes `model: "<provider/id>"` and `effort: "<thinking>"`; for `pi-dynamic-workflows` it passes `model: "<provider/id>:<thinking>"` and no `effort` key. `gate`, `agentType`, `resume`, `isolation`, `tier`, `thread`, `timeoutMs`, `retries`, `whenToUse`, and phase `detail` do not appear anywhere in the script. Role prompts tell the child to read `${skillCreatorPath}/agents/<role>.md` by absolute path and follow it; bundled-agent frontmatter does not apply to workflow children. The script contains no revision literal: the setup launcher records `workflow_runtime` from `args.runtime` and reads `workflow_runtime_revision`, `pi_revision`, `pi_subagents_revision`, and `repository_revision` with `git -C <checkout> rev-parse HEAD`.

Every `agent()` call goes through `safeAgent()`, which turns a `null` result and a thrown error into an accounted `failed` item whose bounded `error` string begins with `null-result:` or `thrown:`. `status_counts` has exactly the buckets `completed`, `failed`, `skipped`, and `bounded`, and they sum to `expected_runs`; a separate `failure_kinds` object counts `null_result`, `thrown`, `explicit`, and `contract` failures and takes no part in that sum. It uses `pipeline()` for execution-to-grading and `parallel()` only for a true all-results synthesis. After grading and before aggregation a launcher agent runs `python -m scripts.aggregate_benchmark <iteration-dir> --validate-only`, which validates the whole iteration tree and writes nothing; Python validation is the authority, and the aggregation step validates again. Any failed item, a failed validation, or a failed aggregation makes the campaign result `valid: false`; nothing is dropped by `.filter(Boolean)` without an explicit count.
```

### `contracts.md` C12

In `### Local pinned-checkout contract tests (no model credentials)`, replace the command block with:

```bash
PI_EXECUTABLE=/absolute/path/to/pi-executable \
PI_CHECKOUT=/absolute/path/to/pi \
PI_SUBAGENTS_CHECKOUT=/absolute/path/to/pi-subagents \
PI_DYNAMIC_WORKFLOWS_CHECKOUT=/absolute/path/to/pi-dynamic-workflows \
uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator -m contract
```

Replace `Workflow meta/runtime tests execute through the pinned pi-subagents source.` with:

```markdown
Workflow meta/runtime tests execute the same script through the pinned pi-subagents source and, when `PI_DYNAMIC_WORKFLOWS_CHECKOUT` is set and its `node_modules/.bin/tsx` exists, through pinned pi-dynamic-workflows `runWorkflow` with an injected runner. A missing variable or a missing `tsx` skips with an explicit reason; a present checkout at the wrong revision fails.
```

### `index.md` rows (already applied with this order)

- Pinned-revision table: pi-subagents row at `7f569969445bf8bc6fbd7757f18db80b35de0ba9`; new rows for pi-dynamic-workflows `3.10.0`, `e9c5a41d9c4234df908aa25a2b49ee9648e896d4` and pi-claude-bridge `0.7.0`, `c1d8b24a57e15bc8acc9d673f2804ab7227978ae`.
- Finding traceability: F12 and F20 primary owner `OSC-06 → OSC-17`, with the resolutions extended as shown there.
- Dependency DAG: `OSC-13 → OSC-17 → HUMAN APPROVAL FOR PAID/LIVE WORK → OSC-14`.
- Execution waves: wave `8b` for OSC-17 between wave 8 and the first `Stop` row.
- Ownership matrix: OSC-17 as the later owner of every path listed under "Exclusive owned paths" below.
- Completion definition: contract tests pass against the exact Pi, pi-subagents, and pi-dynamic-workflows revisions; the runtime workflow passes meta extraction and execution tests on both pinned runtimes; every campaign names its workflow runtime; no pi-dynamic-workflows checkout was modified beyond the untracked `node_modules/`.
- Scope sentences: the "Scope and authority" paragraph and human approval checkpoint 1 still describe the 17 orders (OSC-00 through OSC-16) the adoption workflow enumerated, and now say that OSC-17 was added on 2026-09-04 and is executed standalone.

## Exclusive owned paths

- `skills/pi-skill-creator/workflows/benchmark.js`
- `skills/pi-skill-creator/references/benchmarking.md`
- `skills/pi-skill-creator/references/testing.md`
- `skills/pi-skill-creator/references/schemas.md`
- `skills/pi-skill-creator/SKILL.md` (Step 7 only)
- `skills/pi-skill-creator/README.md` (runtime requirements and honest caveats only)
- `skills/pi-skill-creator/scripts/aggregate_benchmark.py`
- `skills/pi-skill-creator/agents/comparator.md`
- `tests/pi-skill-creator/test_runtime_workflow.py`
- `tests/pi-skill-creator/fixtures/workflow/**`
- `tests/pi-skill-creator/test_bundled_agents.py`
- `tests/pi-skill-creator/test_aggregation.py` (campaign fixture fields and one new test only)
- `tests/pi-skill-creator/conftest.py` (`PI_SUBAGENTS_REVISION`, a new `PI_DYNAMIC_WORKFLOWS_REVISION`, and the `campaign_factory` fields only)
- `tests/pi-skill-creator/README.md`
- `tests/pi-skill-creator/test_readme.py` and `tests/pi-skill-creator/test_testing_doctrine.py` (add assertions naming the second runtime; never weaken an existing assertion)
- `.pi/workflows/pi-skill-creator-adoption.js` and `.pi/workflows/pi-skill-creator-calibration.js` (the `REQUIRED_SUBAGENTS` constant only)
- `docs/pi-skill-creator-work-orders/contracts.md` (the amendments above only)
- `docs/pi-skill-creator-work-orders/osc-06-bundled-agents.md` (one superseded-by annotation on line 15)
- `docs/pi-skill-creator-adoption-report.md` (lines 658, 995, and 1050 only)

## Read-only references

- `HANDOFF-pi-skill-creator.md` decisions 1 to 6
- all frozen contracts as amended by this order, the integrated scripts, agents, schemas, and testing doctrine
- pi-subagents at `7f569969`: `src/workflow/worker-source.ts`, `src/workflow/meta.ts`, `src/workflow/runtime.ts`, `src/workflow/host.ts`, `src/workflow/collisions.ts`, `src/model-resolver.ts`, `src/agent-runner.ts`, `README.md`
- pi-dynamic-workflows at `e9c5a41d`: `src/workflow.ts`, `src/workflow-tool.ts`, `src/agent.ts`, `src/model-spec.ts`, `src/errors.ts`, `src/agent-registry.ts`, `src/structured-output.ts`, `extensions/workflow.ts`, `tests/workflow-runtime.test.ts`, `docs/parity/gap-analysis.md`
- pi-claude-bridge at `c1d8b24a`: `src/index.ts` provider registration, `package.json`
- `~/.pi/agent/settings.json` (`packages`, `enabledModels`); read only, never edited by this order

## Prerequisites

- The repository is clean at a commit that contains this order, the amended `index.md`, and the integrated OSC-00 through OSC-13 result.
- OSC-17 is not run by `.pi/workflows/pi-skill-creator-adoption.js`: that workflow enumerates the 17 original order files and stops after OSC-13 (lines 27, 270, and 282, where it hands off to OSC-14), and its enumeration stays historical and is not edited. OSC-17 is executed as a standalone order: a fresh writer subagent with no inherited context in an isolated worktree, then a fresh read-only verifier, then integration by the user. The order-level gates below replace the workflow's integration gate.
- Checkouts are at the pinned revisions: Pi `a4043c1e332a61e4c8648b97b9b796c57f9db110`, pi-subagents `7f569969445bf8bc6fbd7757f18db80b35de0ba9`, pi-claude-bridge `c1d8b24a57e15bc8acc9d673f2804ab7227978ae` (clean), pi-dynamic-workflows `e9c5a41d9c4234df908aa25a2b49ee9648e896d4`. The pi-dynamic-workflows pin is the checkout's HEAD on 2026-09-04; it is a docs-only descendant of `4aaf451a97707aa7f614fc5c103ed57ae3b290c7` (it adds `docs/parity/` and changes nothing under `src/`), which is the revision the handoff and the parity analysis cite. The pin must appear identically in `contracts.md` C1, `index.md`, `conftest.py`, and `tests/pi-skill-creator/README.md`. The executor never moves a checkout.
- `npm ci` has been run in the pi-dynamic-workflows checkout so `node_modules/.bin/tsx` exists (`npm ci` respects the committed `package-lock.json`; `npm install` is not used). The resulting `node_modules/` is untracked and ignored, and is the only change allowed in that checkout. The pi-subagents checkout already has `node_modules/.bin/tsc` for the existing probe.
- Node `v26.8.1` and Python 3.10+ are available. No model credentials are needed.

## Red test

Name/path: `tests/pi-skill-creator/test_runtime_workflow.py::test_runtime_workflow_executes_on_pi_dynamic_workflows[success]`.

Command:

```bash
PI_SUBAGENTS_CHECKOUT=/absolute/pi-subagents PI_DYNAMIC_WORKFLOWS_CHECKOUT=/absolute/pi-dynamic-workflows uvx --from 'pytest==9.1.1' pytest -q 'tests/pi-skill-creator/test_runtime_workflow.py::test_runtime_workflow_executes_on_pi_dynamic_workflows[success]'
```

Expected pre-fix failure: the fake runner records `model: "fixture/executor"` for every execute child instead of `"fixture/executor:low"`, because the current script passes `effort`, which pi-dynamic-workflows ignores, and the test also finds `whenToUse` in the parsed meta. Four further tests must be observed red in the same session before any fix:

- `test_runtime_workflow.py::test_runtime_workflow_accounts_for_failed_and_null_items[pi-dynamic-workflows-thrown-child]`: the run rejects with `SCHEMA_NONCOMPLIANCE` and the probe reports `status: "threw"`, because the current script has no `try/catch` inside the pipeline stage and pi-dynamic-workflows halts the run on a non-recoverable stage error.
- `test_runtime_workflow.py::test_runtime_workflow_rejects_unknown_runtime` (pi-subagents probe with `runtime: "claude-code"`): the run completes because the current script does not validate `runtime`. The existing pi-subagents assertions `all(call["gate"] ...)` and the `agentType: 'grader'` expectation also flip red once rewritten to require no gate and no `agentType`.
- `test_bundled_agents.py::test_four_agents_register_with_locked_effective_frontmatter`: the comparator config reports `openrouter/~anthropic/claude-opus-latest` and `extensions: false` once `EXPECTED_CONFIGS` names the new pin.
- `test_aggregation.py::test_campaign_requires_workflow_runtime_fields`: `_validate_campaign` accepts a record without `workflow_runtime` and `workflow_runtime_revision`.

## Required behavior

Rewrite `workflows/benchmark.js` so one file runs unchanged on both runtimes. `meta` is the literal `{ name, description, phases: [{ title: 'Prepare' }, { title: 'Execute' }, { title: 'Grade' }, { title: 'Validate' }, { title: 'Aggregate' }] }`. Argument validation adds `runtime` (closed enum; any other value fails with a message naming `runtime`) and absolute `runtimeCheckout` (must equal `piSubagentsCheckout` when `runtime` is `pi-subagents`), and refuses `off` as a requested thinking level for every role on both runtimes (the requested set is `minimal, low, medium, high, xhigh, max`; the effective-value checks in `completedExecution` and `completedGrading` keep accepting `off`). A single function, `runtimeAgentOptions(role, options)` or an equivalent name, builds every `agent()` options object from `label`, `phase`, `schema`, and the role's model and thinking, and is the only place the literals `effort:` and `:` model suffixes appear. `safeAgent(prompt, options, identity)` wraps `agent()`: a `null` result returns `{ status: 'failed', error: 'null-result: <identity>' }` and a thrown error returns `{ status: 'failed', error: 'thrown: <identity>: <bounded message>' }` (message truncated to a fixed bound, for example 500 characters). Every pipeline stage and every top-level call goes through it, so a thrown child never escapes a stage on either runtime.

Launcher prompts carry no `agentType`, no `gate`, and no revision literal. The setup prompt records `workflow_runtime` from `args.runtime` and instructs the launcher to read `workflow_runtime_revision` (`git -C <runtimeCheckout> rev-parse HEAD`), `pi_revision` (`piCheckout`), `pi_subagents_revision` (`piSubagentsCheckout`), and `repository_revision` (`projectRoot`) from git, never from memory, and to write both new fields into `campaign.json`. The grader prompt tells the child to read `${skillCreatorPath}/agents/grader.md` by absolute path and follow it; model and thinking come from `args.roles.grader` through the shim. A new `Validate` phase runs one launcher with `python -m scripts.aggregate_benchmark <iteration-dir> --validate-only` after grading and before aggregation, with a small schema (`status`, `error`); a non-completed result makes the campaign invalid and skips aggregation. The aggregate launcher command drops `--skill-name`: `aggregate_benchmark.py` `main` (lines 736 to 741) accepts only `iteration_dir`, and its `_ArgumentParser.error` (lines 724 to 727) exits 2 on an unknown option, so the current command at `benchmark.js:386` would fail every live aggregation (a latent OSC-12 defect that the stub-host tests could not see). The skill name comes from `campaign.json.skill_name` and the campaign directory, which `_validate_campaign` already cross-checks. The `aggregate_benchmark` command block in `benchmarking.md` (around line 117) loses the flag too; the `eval-viewer/generate_review.py` commands keep theirs. The returned object keeps `valid`, `expected_runs`, `scheduled_runs`, `status_counts` (buckets `completed`, `failed`, `skipped`, `bounded`; sum equals `expected_runs`), a new `failure_kinds` object (`null_result`, `thrown`, `explicit`, `contract`), `stage_statuses` (`setup`, `validation`, `aggregation`, each `completed`, `failed`, or `bounded`), `durable_paths`, `requested_roles`, `effective_roles`, `telemetry` (unchanged), a new `workflow_runtime` field equal to `args.runtime`, and `results`. When setup fails, `status_counts.bounded` equals `expected_runs` and `stage_statuses.setup` is `failed` with the kind visible in `failure_kinds`.

Extend `scripts/aggregate_benchmark.py`: `main` gains `--validate-only`, which runs the full validation path for the iteration tree (campaign, evals, every run, grading, timing, metrics) and exits 0 without writing when everything validates, exits 2 with one bounded error on a contract failure, and exits 1 on filesystem errors; the generated `benchmark.json` `metadata` gains `workflow_runtime` and `workflow_runtime_revision`. `_validate_campaign` requires `workflow_runtime` in the closed enum and `workflow_runtime_revision` as a lowercase 40-hex string. Update `references/schemas.md` (campaign section around lines 44 to 80, and the `benchmark.json` metadata example around line 217) with the two fields and the new pi-subagents example value. Update `conftest.py` `campaign_factory` and the `test_aggregation.py` campaign builder so existing fixtures carry the fields.

Re-pin the comparator: `agents/comparator.md` `model: claude-bridge/claude-opus-5`, `thinking: high` unchanged, `extensions: [pi-claude-bridge]`. In `test_bundled_agents.py`, `EXPECTED_CONFIGS["comparator"]` names the new model and the extension list, `availableModels` replaces the openrouter entry with `{"provider": "claude-bridge", "id": "claude-opus-5"}`, and the `"extensions": False` equality becomes a per-role expectation (comparator `["pi-claude-bridge"]` as pi-subagents parses it, verified against the loader; grader and analyzers stay `False`). The model-preflight test proves `claude-bridge/claude-opus-5` resolves and that an absent bridge provider fails rather than inheriting.

Move every old pi-subagents SHA to the new one: `tests/pi-skill-creator/conftest.py` `PI_SUBAGENTS_REVISION`, `tests/pi-skill-creator/README.md`, `contracts.md` C1 and C5 (through the amendments), `references/schemas.md` example values, and `REQUIRED_SUBAGENTS` in both `.pi/workflows/` files. Add `PI_DYNAMIC_WORKFLOWS_REVISION` to `conftest.py`. The adoption report keeps its historical pins; only its comparator model-policy lines (658, 995, 1050) change to `claude-bridge/claude-opus-5`, with line 995's reason rewritten to say the pin requires `pi-claude-bridge` loaded in the comparator child and is not family-independent for Claude-produced outputs. Annotate `osc-06-bundled-agents.md` line 15 as superseded by OSC-17 without rewriting the historical decision.

Docs: `references/benchmarking.md` names both invocations and a preflight. The preflight checks which tool exists in the session: `workflow` present means pi-dynamic-workflows is loaded and pi-subagents' `SubagentWorkflow` has stood down, so set `runtime: pi-dynamic-workflows`, `runtimeCheckout` to the pi-dynamic-workflows checkout, read `${PI_SKILL_DIR}/workflows/benchmark.js` and pass its content as `script`; otherwise `SubagentWorkflow` present means `runtime: pi-subagents`, `runtimeCheckout` equal to `piSubagentsCheckout`, and `scriptPath`; neither present means stop and tell the user. It states that the user's campaign approval is the explicit opt-in the `workflow` tool requires, that `name` is never used, that resume uses each tool's `resumeFromRunId`, and that a numeric claim names its runtime. `references/testing.md` (the test loop step 1 around line 98 and the workflow-orchestration bullet around line 113), `SKILL.md` Step 7 (line 94), and `README.md` runtime requirements and caveats (lines 54 to 68) name both runtimes and their pins. `tests/pi-skill-creator/README.md` documents `PI_DYNAMIC_WORKFLOWS_CHECKOUT`, the `npm ci` prerequisite, and the four required revisions.

Existing tests assert literal strings in these documents, and the rewrite keeps every one of them. `test_runtime_workflow.py::test_benchmark_contract_prose_matches_runtime` requires `${PI_SKILL_DIR}/references/schemas.md` in `SKILL.md` and, in `benchmarking.md`, `${PI_SKILL_DIR}/workflows/benchmark.js`, `scriptPath`, `with_skill`, `without_skill`, `expectations`, `viewer.pid`, and `--report none`, and forbids `assertions`, `baseline/outputs`, `clean-slate`, and `policy-level` anywhere in its lowercased text. `test_readme.py` (lines 35 to 57) requires `plain-JavaScript runtime workflow`, `Pi 0.84.4`, `absolute paths`, `optional feature dependencies`, `standard library`, and `Python 3.10+` under "Runtime requirements" plus the caveat strings it lists. `test_testing_doctrine.py` (lines 36 to 39 and 62) requires `known small qualitative set`, `explicit user approval`, `parallel writers`, and `worktree isolation` under "The test loop" and `workflow children do not expose` under "Measured-run evidence", and line 90 splits `SKILL.md` on the existing heading `Step 7 — Benchmark (optional)`, whose em dash is pre-existing and must not be changed. `test_aggregation.py` line 323 forbids the word `assertions` in `schemas.md`. The other strings to keep are `SubagentWorkflow`, `pi-subagents 0.19.0`, `dynamic or staged fan-out`, and `benchmark.js`. The executor re-reads those tests before editing prose; the list here is a floor, not the authority.

Tests in `test_runtime_workflow.py`:

- The pi-subagents probe is updated for the shim: it records `request.model`, `request.effort`, `request.agentType`, and `request.gate` from `spawnAgent`, and asserts every request carries a suffix-free `model`, `effort` equal to the role thinking, and neither `agentType` nor `gate`.
- A second probe executes the same script through pi-dynamic-workflows: a session fixture `dynamic_workflows_runtime` skips when `PI_DYNAMIC_WORKFLOWS_CHECKOUT` is unset or `node_modules/.bin/tsx` is absent and fails on a wrong revision (same pattern as `_checkout()` and `workflow_runtime_modules`). The probe is a TypeScript or plain-JavaScript file executed with `node_modules/.bin/tsx` that imports `runWorkflow` from `<checkout>/src/workflow.ts` and `WorkflowError`, `WorkflowErrorCode` from `<checkout>/src/errors.ts`, and calls `runWorkflow(source, { args, agent: runner, concurrency: 4, persistLogs: false, runId: 'osc17-probe', agentRegistry: new Map(), cwd: <temporary directory> })`. The fake runner records `label`, `model`, and the option keys it received, returns the same fixture responses as the pi-subagents probe, and by scenario returns `null`, throws `new WorkflowError(message, WorkflowErrorCode.AGENT_EMPTY_OUTPUT, { recoverable: true })` (the flag must be passed explicitly; it makes `agent()` return `null`), or throws `new WorkflowError(message, WorkflowErrorCode.SCHEMA_NONCOMPLIANCE, { recoverable: false })` (which makes `agent()` throw). The probe catches a rejected run and reports `{ status: "threw", error }` so the Python side sees one shape from both runtimes.
- Both probes cover: success (`valid: true`, `status_counts` sums to `expected_runs`, grade label after execute label), explicit failure, null child, thrown child (pi-dynamic-workflows: proves one thrown child does not abort the campaign; pi-subagents: a host `spawnAgent` that returns `{ ok: false }`), missing approval, unknown runtime, a role with `thinking: "off"` refused at argument validation, `runtimeCheckout` different from `piSubagentsCheckout` under `runtime: pi-subagents` refused, setup failure, and validation failure (the `validate` launcher returns `failed`, aggregation is skipped, `valid: false`). The pi-dynamic-workflows runner asserts `model` equals `<role model>:<role thinking>` and that no `effort` key reached it; the pi-subagents host asserts the suffix-free form.
- Resume replay runs on both runtimes: pi-subagents through the existing `journal` option; pi-dynamic-workflows by collecting `onAgentJournal` entries, then re-running with the same `runId` and `resumeJournal: new Map(entries.map(e => [`${e.runId}:${e.index}`, e]))`, asserting zero runner calls and an identical result (`tests/workflow-runtime.test.ts:644-669` is the reference pattern).
- A runtime-independence assertion: for the success scenario, the ordered list of `(label, prompt)` pairs observed by the pi-subagents host and by the pi-dynamic-workflows runner is identical.
- A source-level test reads `workflows/benchmark.js` and asserts: `meta` contains no `whenToUse` or `detail`; the literals `effort:`, `gate:`, `agentType:`, `resume:`, `isolation:`, `tier:`, `thread:`, `timeoutMs:`, `retries:` occur only inside the shim function body (for `effort:`) or not at all (all others); no `Date.now`, `Math.random`, `new Date()`, `require(`, `import `, `fetch(`, `XMLHttpRequest`; no 40-hex literal; no `--skill-name`; `safeAgent(` is the only call site of `agent(` apart from its own definition; `.filter(Boolean)` is absent; `await pipeline(` is present.
- `fixtures/workflow/valid-args.json` gains `runtime: "pi-subagents"` and `runtimeCheckout` equal to its `piSubagentsCheckout`; a second fixture `valid-args-pi-dynamic-workflows.json` sets `runtime: "pi-dynamic-workflows"` and a distinct absolute `runtimeCheckout`. Tests parametrize over both.

## Implementation steps

1. Apply every `contracts.md` replacement from "Contract amendments"; verify the `index.md` rows are present; annotate `osc-06-bundled-agents.md` line 15.
2. Re-pin pi-subagents in `conftest.py`, `tests/pi-skill-creator/README.md`, `references/schemas.md`, and both `.pi/workflows/` constants; add `PI_DYNAMIC_WORKFLOWS_REVISION`. Run the existing contract tests to confirm they execute against the re-pinned checkout.
3. Add the pi-dynamic-workflows fixture and probe, the new scenarios, the source-level test, the unknown-runtime test, the comparator expectations, and the aggregation field test. Run the red commands and record the observed failures.
4. Rewrite `benchmark.js`: shared-subset `meta`, `runtime` and `runtimeCheckout` validation, the shim, `safeAgent()`, launcher prompts without `agentType`, `gate`, or revision literals, the `Validate` phase, and the new accounting.
5. Extend `aggregate_benchmark.py` (`--validate-only`, runtime fields in validation and `benchmark.json` metadata), `schemas.md`, `campaign_factory`, and the aggregation fixtures.
6. Re-pin the comparator file and `test_bundled_agents.py`; run the bundled-agent contract tests.
7. Rewrite `benchmarking.md`, `testing.md`, `SKILL.md` Step 7, `README.md` runtime requirements and caveats, `tests/pi-skill-creator/README.md`, and the three adoption-report lines.
8. Search the repository for `bfa262fd`, `claude-opus-latest`, `whenToUse`, `gate:`, and `agentType:` outside the adoption report's historical sections and the handoff file; run the full gates.

## Deterministic branch-tip gates

```bash
PI_CHECKOUT=/absolute/pi PI_SUBAGENTS_CHECKOUT=/absolute/pi-subagents PI_DYNAMIC_WORKFLOWS_CHECKOUT=/absolute/pi-dynamic-workflows uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator/test_runtime_workflow.py tests/pi-skill-creator/test_bundled_agents.py tests/pi-skill-creator/test_aggregation.py
uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator -m 'not live'
uvx --from 'ty==0.0.77' ty check skills/pi-skill-creator/scripts skills/pi-skill-creator/eval-viewer
git diff --check
```

From the skill directory, `python3 scripts/quick_validate.py .` must also pass. No pi-dynamic-workflows probe may be skipped in the first command (the checkout variable and `tsx` are present by prerequisite); a skip there is a gate failure. No Pi, pi-subagents, pi-claude-bridge, or pi-dynamic-workflows checkout may be modified; the untracked, ignored `node_modules/` from `npm ci` in pi-dynamic-workflows is the only allowed change.

## Live-test requirements

None at branch tip; no model call is made. Resolution of `claude-bridge/claude-opus-5` for a pi-dynamic-workflows child is source-verified only. OSC-14 exercises the re-pinned comparator live under `runtime: pi-subagents`. A live smoke of the workflow under pi-dynamic-workflows is deferred until the user activates that extension and separately approves it; until then no claim about pi-dynamic-workflows execution with real models exists.

## Non-goals

Do not port `.pi/workflows/pi-skill-creator-adoption.js` or `-calibration.js` to pi-dynamic-workflows. Do not add `gate`, `agentType`, `resume`, or `effort` parity shims beyond the single model/effort shim. Do not change the campaign schema id, add numeric claims, add TypeScript or npm material to `skills/pi-skill-creator/`, make the workflow discoverable by saved-workflow name, edit `~/.pi/agent/settings.json`, modify any maintainer checkout, add Claude Code compatibility, or run OSC-14.

## Structured handoff

Return: `order_id`, `status`, `branch`, `commit`, `red_observed`, `shim_verified_pi_subagents`, `shim_verified_pi_dynamic_workflows`, `comparator_repinned`, `subagents_repinned`, `contracts_amended`, `tests_passed`, `tests_skipped` (intentionally skipped tests only), `bounded_work` (mandated exclusions only), `skipped_work` (required work left incomplete; must be `[]` on completion), `owned_paths_changed`, `summary`, `blockers`.

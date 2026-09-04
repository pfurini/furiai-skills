# pi-skill-creator frozen implementation contracts

Executors implement these contracts exactly. A conflict discovered against the pinned source is a stop condition reported in the handoff, not permission to invent a local variant.

## C1. Repositories, runtime, and language boundary

- Immutable source baseline: `0b9e86bc77a60fb34039456a6624ea94e396f5d1`. It only freezes the F19 removal and pre-implementation skill state; adoption never starts from that SHA.
- Adoption implementation start: the caller supplies a full `implementationStartCommit` naming the later clean current `HEAD` that contains this contract, the index, all 17 OSC orders, and both project workflows. It must descend from or equal the source baseline. All isolated implementation worktrees branch from this handoff-containing commit, and all adoption branch/integration diff gates use `implementationStartCommit..HEAD`.
- Pi checkout: `/absolute/path` supplied by workflow input, revision `7815e97a0dd5e7eee3cd01858bd5aa0fabeebae0`, version `0.84.4`. This revision is one commit past `a4043c1e332a61e4c8648b97b9b796c57f9db110` and changes only `packages/ai/scripts/generate-models.ts`; `packages/ai/src/models.generated.ts` is identical at both revisions, and the executable is a pre-commit build with identical behavior that reports `0.84.4`.
- Pi executable: a separate absolute `piExecutable` workflow input; preflight requires it to be executable and report Pi `0.84.4`.
- pi-subagents checkout: `/absolute/path` supplied by workflow input, revision `7f569969445bf8bc6fbd7757f18db80b35de0ba9`, version `0.19.0`. This revision differs from `bfa262fdd75d807b1c6b1f852f1f1bea2bbb3fa4` only by the case-insensitive workflow-tool collision check in `src/workflow/collisions.ts`, which lets `SubagentWorkflow` stand down beside pi-dynamic-workflows' `workflow` tool.
- pi-dynamic-workflows checkout: `/absolute/path` supplied by the `PI_DYNAMIC_WORKFLOWS_CHECKOUT` test input and by the runtime workflow's `runtimeCheckout` argument, revision `e9c5a41d9c4234df908aa25a2b49ee9648e896d4`, version `3.10.0`. Tests that execute through it require `node_modules/.bin/tsx` produced by `npm ci` in that checkout; that directory is covered by the checkout's `.gitignore` and is the only permitted change there.
- pi-claude-bridge: loaded in the host session from `/absolute/path/pi-claude-bridge` through `~/.pi/agent/settings.json` `packages`, revision `c1d8b24a57e15bc8acc9d673f2804ab7227978ae`, version `0.7.0`. Its extension allowlist name under pi-subagents is `pi-claude-bridge`, the package manifest name (`src/agent-runner.ts:85-126`).
- Runtime skill code remains Python 3.10+ standard library plus one plain-JavaScript runtime workflow that runs unchanged on both pinned workflow runtimes.
- No TypeScript, npm dependency, companion extension, or imports from maintainer checkouts enter `skills/pi-skill-creator/`.
- External immutable revisions may be cited with line numbers. Mutable repository files are addressed by path, symbol, and test name.

## C2. Directory distribution boundary

`skills/pi-skill-creator/` is copied byte-for-byte into a Pi-owned skill root. It contains runtime instructions, agents, Python helpers, viewer assets, and `workflows/benchmark.js`. It does not contain tests, fixtures, campaign records, reports, work orders, caches, or repository configuration.

Development-only locations are:

```text
docs/pi-skill-creator-adoption-report.md
docs/pi-skill-creator-work-orders/**
tests/pi-skill-creator/**
.pi/workflows/pi-skill-creator-adoption.js
.pi/workflows/pi-skill-creator-calibration.js
.skill-creator/**
```

The install smoke test copies the directory; it never creates or consumes an archive.

## C3. Exact campaign workspace tree

`<project-root>/.skill-creator/<skill-name>/campaign-<campaign-id>/` is the campaign root. `campaign-id` is supplied by the caller and matches `[a-z0-9][a-z0-9-]{0,63}`. Scripts never generate it from time or randomness.

```text
campaign-<campaign-id>/
├── campaign.json
├── evals.json
├── trigger/
│   ├── train.json
│   ├── validation.json
│   ├── final-test.json
│   └── results.json
└── iteration-N/
    ├── benchmark.json
    ├── benchmark.md
    ├── feedback.json
    ├── viewer.pid
    └── <human-readable-eval-name>/
        ├── eval_metadata.json
        ├── with_skill/
        │   └── run-N/
        │       ├── outputs/
        │       ├── transcript.jsonl
        │       ├── transcript-metrics.json
        │       ├── run.json
        │       ├── timing.json
        │       └── grading.json
        └── without_skill/
            └── run-N/
                ├── outputs/
                ├── transcript.jsonl
                ├── transcript-metrics.json
                ├── run.json
                ├── timing.json
                └── grading.json
```

Eval directory names are descriptive and match `[a-z0-9][a-z0-9-]{0,63}`. The only configuration directory names are `with_skill` and `without_skill`. The `run-N` layer is mandatory. Discovery of zero runs, a missing expected arm, a missing repetition, or an unexpected configuration is fatal and writes no benchmark artifact.

The campaign root may additionally hold `workflow-result.json` (the workflow tool's returned object, saved verbatim by the caller) and a `comparisons/` directory for blind-comparison records made from the top-level session. The aggregator reads neither. `iteration-N/` accepts no file other than `benchmark.json`, `benchmark.md`, `feedback.json`, and `viewer.pid`, and no directory other than eval directories.

## C4. Terminology

A graded claim is an **expectation** everywhere. The JSON key is `expectations`. `assertion` is not a schema synonym.

The experiment roles are:

- treatment: `with_skill`;
- control: `without_skill`;
- delta: treatment minus control.

## C5. Campaign and result metadata

`campaign.json` has schema id `pi-skill-creator.campaign/v1` and requires:

```json
{
  "schema_version": "pi-skill-creator.campaign/v1",
  "campaign_id": "fork-smoke-1",
  "created_at": "2026-09-02T12:00:00Z",
  "repository_revision": "<40-hex>",
  "pi_revision": "7815e97a0dd5e7eee3cd01858bd5aa0fabeebae0",
  "pi_subagents_revision": "7f569969445bf8bc6fbd7757f18db80b35de0ba9",
  "workflow_runtime": "pi-subagents",
  "workflow_runtime_revision": "7f569969445bf8bc6fbd7757f18db80b35de0ba9",
  "skill_name": "example-skill",
  "skill_path": "/absolute/path/to/example-skill",
  "evaluation_cwd": "/absolute/path/to/deployment-project",
  "environment_profile": "declared-dependencies",
  "declared_extensions": ["/absolute/path/to/pi-subagents/src/index.ts"],
  "treatment": "with_skill",
  "control": "without_skill",
  "repetitions": 3,
  "roles": {
    "executor": {
      "requested_model": "provider/model",
      "requested_thinking": "low"
    },
    "grader": {
      "requested_model": "provider/model",
      "requested_thinking": "high"
    },
    "comparator": {
      "requested_model": "claude-bridge/claude-opus-5",
      "requested_thinking": "high"
    },
    "optimizer": {
      "requested_model": "provider/model",
      "requested_thinking": "high"
    }
  },
  "partitions": {
    "seed": 42,
    "train": "trigger/train.json",
    "validation": "trigger/validation.json",
    "final_test": "trigger/final-test.json"
  }
}
```

`created_at` is an input, not generated inside a workflow. `workflow_runtime` is `pi-subagents` or `pi-dynamic-workflows` and names the runtime that executed `workflows/benchmark.js`; `workflow_runtime_revision` is the lowercase 40-hex `HEAD` of that runtime's checkout, read with `git -C <runtimeCheckout> rev-parse HEAD` by the setup launcher, never invented. Both fields are required. `notes` is an optional array of non-empty strings that the aggregator copies into `benchmark.json` metadata; the setup launcher records the comparator family caveat from C10 there. A campaign supports claims only for the runtime it records; a run under the other runtime is a new campaign. The schema id stays `pi-skill-creator.campaign/v1` because no v1 record exists outside test fixtures. Role entries not used by a campaign are omitted. All paths in durable metadata are absolute or campaign-root-relative as shown; ambiguous cwd-relative paths are rejected.

Every `run.json` has schema id `pi-skill-creator.run/v1` and requires:

```json
{
  "schema_version": "pi-skill-creator.run/v1",
  "campaign_id": "fork-smoke-1",
  "eval_id": 1,
  "eval_name": "forked-skill-dispatch",
  "configuration": "with_skill",
  "run_number": 1,
  "environment_profile": "declared-dependencies",
  "status": "completed",
  "role": "executor",
  "requested_model": "provider/model",
  "effective_model": "provider/model-exact",
  "requested_thinking": "high",
  "effective_thinking": "high",
  "transcript_format": "pi-json-events-v3",
  "transcript_path": "transcript.jsonl",
  "metrics_path": "transcript-metrics.json",
  "outputs_dir": "outputs"
}
```

Effective values come from Pi events/messages or pi-subagents invocation records, never by copying requested values. An unresolved model, absent effective value, or mismatch not explicitly allowed by a pre-registered calibration plan invalidates the run.

`benchmark.json` uses effective model/thinking labels. Character counts are fields ending in `_chars`; provider token counts are under `usage`; no fallback substitutes one for the other.

Calibration writes `review-required.json` but does not change runtime claims or model pins. A human creates a separate immutable `pi-skill-creator.calibration-review/v1` JSON object containing the campaign id, campaign record hashes, reviewer decision time, and arrays `accepted_claims`, `rejected_claims`, `accepted_pins`, and `rejected_pins`. Each entry identifies an exact campaign record path and rationale. OSC-15 accepts only this review file through an absolute workflow argument; file existence alone is not approval. It applies accepted decisions without model calls, then OSC-16 performs final distribution validation.

## C6. Trigger result contract

The closed status enum is:

```text
triggered
not_triggered
timeout
process_error
model_error
auth_error
invalid_output
```

Only `triggered` and `not_triggered` enter accuracy denominators. Any other status invalidates the query result. After the bounded retry policy (maximum one retry, only for rate-limit or explicitly transient provider errors), any infrastructure status invalidates the campaign. A worker exception becomes `process_error`, never `not_triggered`.

A trigger result records `status`, `attempts`, `exit_code`, bounded `stderr`, requested/effective model and thinking, environment profile, evaluation cwd, real skill name, and whether invocation was observed through the `skill` tool or a direct `SKILL.md` read.

## C7. Environment profiles

- `in-situ`: real evaluation cwd, user/global/project instructions and competing skills present. Used for trigger behavior. The exact competing set is recorded.
- `hermetic-core`: an in-harness subagent with `prompt_mode: replace`, `inherit_context: false`, `isolated: true`, `skills: false`, and `isolation: worktree` when it writes. Built-in tools only.
- `declared-dependencies`: the hermetic resource baseline plus only the absolute extensions/skills declared in `campaign.json`. Fork and bundled-agent behavioral claims use Pi RPC with pi-subagents loaded explicitly by `-e <pi-subagents>/src/index.ts`.

Different profiles are never aggregated into one comparison. A profile mismatch is fatal.

## C8. Telemetry seam and transcript parser

### Source evidence and boundary

pi-subagents `SubagentWorkflow.agent()` returns only final text or validated structured output. Workflow-owned children emit no top-level `subagents:started/completed/failed/compacted` events. `src/workflow/host.ts` returns aggregate tokens/tool-call counts to workflow progress but does not attach the `.output` transcript used by the top-level `Agent` tool. Therefore no implementation may claim a workflow-child transcript path or per-child cost.

The same boundary holds for pi-dynamic-workflows: a `workflow` child returns only the value its runner produced, and the script receives no transcript path, usage, or effective model (`docs/parity/gap-analysis.md` section 7 in that checkout). Both runtimes therefore treat RPC `run.json` and `transcript-metrics.json` as the only executor evidence.

Measured in-harness executions use the top-level `Agent` tool, whose result/notification exposes the `.output` path. Measured fork/dependency executions use the Python RPC runner, which writes the Pi JSON event stream. `workflows/benchmark.js` may orchestrate RPC-launcher agents for fork/dependency campaigns, but it treats RPC `run.json` and `transcript-metrics.json` as executor evidence. The launcher agent's own usage is orchestration overhead, not executor usage; the workflow returns `workflow_output_tokens: budget.spent()` and explicitly marks per-launcher cost unavailable. It never substitutes launcher telemetry for executor telemetry.

### Module and Python API

Module: `skills/pi-skill-creator/scripts/transcript_metrics.py`.

```python
from pathlib import Path
from typing import Literal

TranscriptFormat = Literal["pi-subagents-output-v1", "pi-json-events-v3"]

def parse_transcript(path: Path, *, source_format: TranscriptFormat) -> dict:
    """Return an pi-skill-creator.transcript-metrics/v1 JSON-compatible dictionary or raise TranscriptMetricsError."""
```

The module exports `TranscriptMetricsError(ValueError)`. It reads strict UTF-8 JSONL, splits records on LF only, accepts a trailing CR before LF, rejects malformed/non-object records, and never skips an unreadable line.

### CLI

Run from the skill directory:

```bash
python -m scripts.transcript_metrics \
  --format pi-subagents-output-v1 \
  --input /absolute/path/to/agent.output \
  --output /absolute/path/to/transcript-metrics.json
```

`--format`, `--input`, and `--output` are required. Success writes one JSON object plus LF and exits 0. Contract/input failures write no output, print one bounded error to stderr, and exit 2. Filesystem errors exit 1.

### Output schema

```json
{
  "schema_version": "pi-skill-creator.transcript-metrics/v1",
  "source_format": "pi-subagents-output-v1",
  "tool_calls": {"bash": 2, "read": 3},
  "total_tool_calls": 5,
  "assistant_turns": 2,
  "tool_errors": 1,
  "usage": {
    "input": 100,
    "output": 20,
    "cache_read": 50,
    "cache_write": 0,
    "reasoning": 5,
    "total_tokens": 170,
    "cost_usd": 0.0123
  },
  "effective_models": ["provider/model"],
  "transcript_chars": 12345
}
```

For pi-subagents `.output`, tool calls come from assistant `message.content[]` entries with `type: "toolCall"` and `name`; usage and model come from each authoritative assistant message. For Pi JSON/RPC, tool calls/errors come from `tool_execution_start`/`tool_execution_end`; usage/model come from authoritative `message_end.message` assistant messages. Cumulative `message_update.usage` is ignored to avoid double counting. Tool-result `usage`, when present, is included once. Tool names must be lowercase registered Pi names. Empty/missing authoritative usage, non-numeric usage, negative counts, or no effective model is an error for a completed measured run.

## C9. RPC runner contract

Module: `skills/pi-skill-creator/scripts/rpc_runner.py`.

It launches the explicit absolute Pi executable input using `<pi-executable> --mode rpc --no-session`, writes one `prompt` command with an id, and waits for the matching accepted response followed by `agent_end`. It splits stdout on LF only, records the complete event stream to `transcript.jsonl`, and then calls `transcript_metrics.parse_transcript(..., source_format="pi-json-events-v3")`.

The CLI requires absolute `--pi-executable`, `--pi-checkout`, `--evaluation-cwd`, `--skill-path`, and `--run-dir`, plus `--model`, an explicit `--thinking`, and `--profile`. `declared-dependencies` additionally requires absolute repeatable `--extension` values. Queries are sent in JSON on stdin, never as the argument following `-p`, so leading `@` and `-` survive.

A run directory is at most one measured executor call. When `--run-dir` already contains `run.json` or `transcript.jsonl`, the runner fails with kind `invalid_input` and exit status 2 before launching any process, and it never deletes stale records. A retry needs a new run directory that the campaign plan accounts for.

RPC extension UI dialog requests are a run failure in automated campaigns. Fire-and-forget UI notifications may be recorded and ignored. Timeouts terminate the process group and classify the run as `timeout`. Nonzero process exits and malformed protocol records never produce `completed` run metadata.

## C10. Bundled agent identities

Exactly four runtime agents exist:

```text
grader
comparator
comparison-analyzer
benchmark-analyzer
```

`agents/analyzer.md` is deleted after its two roles move. Skill prose names the bare identities; Pi/pi-subagents qualifies them on collision. All four set `prompt_mode: replace`, `inherit_context: false`, `skills: false`, `persist_session: false`, and `output_transcript: true`. Grader/comparator run in background; analyzers run foreground. Executor model is never pinned in an agent file.

The comparator is `claude-bridge/claude-opus-5` at `high` thinking (`max` may be requested per campaign for critical skills). `agents/comparator.md` sets `extensions: [pi-claude-bridge]`, because a pi-subagents child with `extensions: false` has no `claude-bridge` provider in its registry. The grader and both analyzers keep `extensions: false`. Campaign preflight must prove the pin resolves in the selected profile; requested and effective model must both equal `claude-bridge/claude-opus-5`. Failure to resolve is fatal; fallback-to-parent is not accepted. For outputs produced by Claude-family executors this comparator is not family-independent; the campaign record states this, and no audit campaign is added.

Agent frontmatter (`tools`, `extensions`, `max_turns`, and the rest) governs the top-level `Agent` path only. The runtime workflow does not dispatch bundled agents by `agentType`; see C11.

## C11. Runtime benchmark workflow boundary

`skills/pi-skill-creator/workflows/benchmark.js` is runtime skill machinery. `.pi/workflows/pi-skill-creator-adoption.js` and `pi-skill-creator-calibration.js` are repository-development workflows. They do not invoke one another and are not distributed together.

The runtime workflow requires caller-provided `campaignId`, `createdAt`, absolute `projectRoot`, `skillPath`, `skillCreatorPath`, `piExecutable`, `piCheckout`, `piSubagentsCheckout`, and `runtimeCheckout`, a `runtime` from the closed enum `pi-subagents` | `pi-dynamic-workflows`, environment profile, eval array, iteration, repetitions, role models/thinking, and `approved: true`. When `runtime` is `pi-subagents`, `runtimeCheckout` must equal `piSubagentsCheckout`. Requested thinking for every role is one of `minimal, low, medium, high, xhigh, max`; `off` is refused. The skill obtains approval before the tool call; the workflow also refuses absent approval and an unknown runtime. `piSubagentsCheckout` stays required because `declared-dependencies` still loads pi-subagents through `scripts.rpc_runner --extension <checkout>/src/index.ts`, which the runner passes to Pi as `-e`.

The skill invokes the script through `SubagentWorkflow` with `scriptPath` when only that tool is present, or through `workflow` with the file content passed as `script` when pi-dynamic-workflows is loaded (its presence makes `SubagentWorkflow` stand down). The `workflow` tool's `name` input is never used.

The script uses only the subset both runtimes implement: `meta { name, description, phases: [{ title }] }`, `phase()`, `agent()`, `parallel()`, `pipeline()`, `log()`, `args`, and `budget.spent()`. `agent()` options are only `label`, `phase`, `schema`, and `model`, plus `effort` emitted by the shim for pi-subagents. One shim function keyed on `args.runtime` is the only code that knows the runtimes differ: for `pi-subagents` it passes `model: "<provider/id>"` and `effort: "<thinking>"`; for `pi-dynamic-workflows` it passes `model: "<provider/id>:<thinking>"` and no `effort` key. `gate`, `agentType`, `resume`, `isolation`, `tier`, `thread`, `timeoutMs`, `retries`, `whenToUse`, and phase `detail` do not appear anywhere in the script. Role prompts tell the child to read `${skillCreatorPath}/agents/<role>.md` by absolute path and follow it; bundled-agent frontmatter does not apply to workflow children. The script contains no revision literal: the setup launcher records `workflow_runtime` from `args.runtime` and reads `workflow_runtime_revision`, `pi_revision`, `pi_subagents_revision`, and `repository_revision` with `git -C <checkout> rev-parse HEAD`.

Every `agent()` call goes through `safeAgent()`, which turns a `null` result and a thrown error into an accounted `failed` item whose bounded `error` string begins with `null-result:` or `thrown:`. `status_counts` has exactly the buckets `completed`, `failed`, `skipped`, and `bounded`, and they sum to `expected_runs`; a separate `failure_kinds` object counts `null_result`, `thrown`, `explicit`, and `contract` failures and takes no part in that sum. It uses `pipeline()` for execution-to-grading and `parallel()` only for a true all-results synthesis. After grading and before aggregation a launcher agent runs `python -m scripts.aggregate_benchmark <iteration-dir> --validate-only`, which validates the whole iteration tree and writes nothing; Python validation is the authority, and the aggregation step validates again. Any failed item, a failed validation, or a failed aggregation makes the campaign result `valid: false`; nothing is dropped by `.filter(Boolean)` without an explicit count.

`maxAgentCalls` is a required positive integer. Before the first `agent()` call the script computes `agent_calls_planned` as `1` (setup) `+ 2 × scheduled_runs` (one execute launcher and one grader per scheduled run) `+ 1` (validate) `+ 1` (aggregate) and fails argument validation, naming `maxAgentCalls`, when the plan exceeds the bound. At runtime `safeAgent()` counts every call before making it; a call that would exceed the bound is never launched and is accounted as a `bounded` item (`failure_kinds` unchanged). The returned object reports `agent_calls_planned`, `agent_calls_made`, and `max_agent_calls`, and `agent_calls_made` never exceeds `max_agent_calls`. The bound covers workflow children only: the comparator, any analyzer, and any viewer call made from the top-level session are counted separately by the caller's manifest, and measured RPC executor processes are counted by their `run.json` records.

## C12. Test tiers and exact commands

### Offline unit/regression (always available)

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator -m 'not contract and not live'
```

No network, credentials, Pi checkout, or model calls.

### Local pinned-checkout contract tests (no model credentials)

```bash
PI_EXECUTABLE=/absolute/path/to/pi-executable \
PI_CHECKOUT=/absolute/path/to/pi \
PI_SUBAGENTS_CHECKOUT=/absolute/path/to/pi-subagents \
PI_DYNAMIC_WORKFLOWS_CHECKOUT=/absolute/path/to/pi-dynamic-workflows \
uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator -m contract
```

Tests assert exact revisions and skip only when either variable is absent. A present but wrong revision fails. Validator differential tests use Pi's real exported loader. Workflow meta/runtime tests execute the same script through the pinned pi-subagents source and, when `PI_DYNAMIC_WORKFLOWS_CHECKOUT` is set and its `node_modules/.bin/tsx` exists, through pinned pi-dynamic-workflows `runWorkflow` with an injected runner. A missing variable or a missing `tsx` skips with an explicit reason; a present checkout at the wrong revision fails.

### Static Python check

```bash
uvx --from 'ty==0.0.77' ty check skills/pi-skill-creator/scripts skills/pi-skill-creator/eval-viewer
```

### Credentialed/live (opt-in only)

```bash
PI_SKILL_CREATOR_LIVE_TESTS=1 \
PI_SKILL_CREATOR_REPLAY_ONLY=1 \
PI_EXECUTABLE=/absolute/path/to/pi-executable \
PI_CHECKOUT=/absolute/path/to/pi \
PI_SUBAGENTS_CHECKOUT=/absolute/path/to/pi-subagents \
PI_SKILL_CREATOR_CAMPAIGN_DIR=/absolute/path/outside/skill \
uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator -m live
```

The calibration workflow makes no paid call in any stage. The smoke campaign is run from the top-level Pi session under the human-approved manifest, and the workflow's `calibrate` stage then runs this command only to replay and validate the durable records against `PI_SKILL_CREATOR_MAX_PAID_CALLS`. `PI_SKILL_CREATOR_REPLAY_ONLY=1` is a hard no-model-call mode. `PI_SKILL_CREATOR_LIVE_TESTS=1` alone is not approval.

### Deterministic branch-tip gates

Before OSC-07 integrates the final pre-existing `run_loop.py` type defect, use the passing test gate plus the order's focused `ty` command (when it owns Python):

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator -m 'not live' && \
git diff --check
```

From OSC-07 onward, use the full gate:

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator -m 'not live' && \
uvx --from 'ty==0.0.77' ty check skills/pi-skill-creator/scripts skills/pi-skill-creator/eval-viewer && \
git diff --check
```

This staging is required because the source-baseline skill state has seven known `ty` diagnostics assigned to OSC-05 and OSC-07; making OSC-00 run the final static gate would make its passing tip impossible.

## C13. Passing-main TDD

OSC-00 lands fixtures, helpers, and green tests only. It does not commit permanently red tests or broad `xfail` markers. Each defect order must:

1. add or enable its named regression test and run the focused command to observe the specified pre-fix failure;
2. implement the fix in the same branch;
3. run the focused test and the phase-appropriate deterministic branch-tip gate above; and
4. commit only a passing branch tip for workflow integration.

Credentialed tests are never required to make an implementation branch green. They remain marked `live` and are exercised only by OSC-14.

## C14. Failure semantics

- Invalid workflow `meta`, invalid args, missing approval, wrong source ancestry/start commit/runtime revision, dirty integration tree, missing tracked handoff file at the implementation start, null schema result, failed gate, skipped writer, unreported bounded work, ownership overlap, absent human calibration review, or a review record that references unhashed/missing campaign data stops the workflow.
- A deterministic campaign with any missing/failed/invalid run is invalid and emits no benchmark claim.
- A skipped live test is reported as skipped and cannot support a model pin or numeric claim.
- No-data aggregation, mixed profiles, mixed effective models outside a pre-registered comparison, placeholder metadata, and fabricated repetitions are fatal.
- Parsers never warn-and-continue over malformed JSONL.
- Model resolution never silently inherits when a role requested a model.
- Distribution validation never repairs the copied directory; it reports source defects and fails.

## C15. Calibration workflow stage-start commit

The calibration workflow has three stages, each a separate invocation, and makes no paid call in any of them. The required `stageStartCommit` argument is validated as a lowercase 40-hex string before any use, is shell-quoted in every gate, and always names the exact clean repository commit at which that invocation starts:

- for `stage: "preflight"`, it equals the OSC-18 integration commit (the commit at which the smoke will run). Preflight requires no approval token, spends nothing, and writes nothing: it verifies the pins, the clean tree at `stageStartCommit`, the executable version, that every manifest model prints an exact `provider` and `model` row from `pi --list-models <provider/id>`, that the installed skill copy is byte-for-byte equal to `skills/pi-skill-creator/` and is the only copy in Pi's skill roots, and the manifest schema, then returns structured output;
- for `stage: "preflight"`, it equals the OSC-18 integration commit (the commit at which the smoke will run). Preflight requires no approval token, spends nothing, and writes nothing: it verifies the four checkout pins, the clean tree at `stageStartCommit`, the executable version, that every manifest model prints an exact `provider` and `model` row from `pi --list-models <provider/id>`, that the installed skill copy is byte-for-byte equal to `skills/pi-skill-creator/` and is the only copy in the two user skill roots (`~/.pi/agent/skills` and `~/.agents/skills`; project roots under the evaluation project are the human's responsibility and the smoke uses a fresh directory), and the manifest schema, then returns structured output;
- for `stage: "finalize"`, it equals the `calibrationIntegrationCommit` returned by the calibrate invocation, after the human has reviewed that commit's campaign records. Finalize requires `approval: "APPROVE_CALIBRATION_RESULTS"`, `humanReviewComplete: true`, and the absolute immutable human review record.

Preflight for every stage requires repository `HEAD` to equal `stageStartCommit` exactly and the tree to be clean. A commit argument, a prior approval, a preflight result, or review-file existence never authorizes another stage.

# pi-skill-creator frozen implementation contracts

Executors implement these contracts exactly. A conflict discovered against the pinned source is a stop condition reported in the handoff, not permission to invent a local variant.

## C1. Repositories, runtime, and language boundary

- Immutable source baseline: `0b9e86bc77a60fb34039456a6624ea94e396f5d1`. It only freezes the F19 removal and pre-implementation skill state; adoption never starts from that SHA.
- Adoption implementation start: the caller supplies a full `implementationStartCommit` naming the later clean current `HEAD` that contains this contract, the index, all 17 OSC orders, and both project workflows. It must descend from or equal the source baseline. All isolated implementation worktrees branch from this handoff-containing commit, and all adoption branch/integration diff gates use `implementationStartCommit..HEAD`.
- Pi checkout: `/absolute/path` supplied by workflow input, revision `a4043c1e332a61e4c8648b97b9b796c57f9db110`, version `0.84.4`.
- Pi executable: a separate absolute `piExecutable` workflow input; preflight requires it to be executable and report Pi `0.84.4`.
- pi-subagents checkout: `/absolute/path` supplied by workflow input, revision `bfa262fdd75d807b1c6b1f852f1f1bea2bbb3fa4`, version `0.19.0`.
- Runtime skill code remains Python 3.10+ standard library plus one plain-JavaScript runtime workflow.
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
  "pi_revision": "a4043c1e332a61e4c8648b97b9b796c57f9db110",
  "pi_subagents_revision": "bfa262fdd75d807b1c6b1f852f1f1bea2bbb3fa4",
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
      "requested_model": "openrouter/~anthropic/claude-opus-latest",
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

`created_at` is an input, not generated inside a workflow. Role entries not used by a campaign are omitted. All paths in durable metadata are absolute or campaign-root-relative as shown; ambiguous cwd-relative paths are rejected.

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

The provisional comparator is `openrouter/~anthropic/claude-opus-latest` at high thinking. Campaign preflight must prove it resolves in the selected profile. Failure to resolve is fatal; fallback-to-parent is not accepted.

## C11. Runtime benchmark workflow boundary

`skills/pi-skill-creator/workflows/benchmark.js` is runtime skill machinery. `.pi/workflows/pi-skill-creator-adoption.js` and `pi-skill-creator-calibration.js` are repository-development workflows. They do not invoke one another and are not distributed together.

The runtime workflow requires caller-provided `campaignId`, `createdAt`, absolute project/skill/Pi/pi-subagents paths, environment profile, eval array, repetitions, role models/thinking, and `approved: true`. The skill obtains approval before the tool call; the workflow also refuses absent approval.

It uses `pipeline()` for execution-to-grading and `parallel()` only for a true all-results synthesis. Every schema result is checked for `null`. Every expected eval/arm/repetition is accounted as `completed`, `failed`, `skipped`, or `bounded`. Any failed/schema-null/gate-null item makes the campaign result `valid: false`; it is never dropped by `.filter(Boolean)` without an explicit count.

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
uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator -m contract
```

Tests assert exact revisions and skip only when either variable is absent. A present but wrong revision fails. Validator differential tests use Pi's real exported loader. Workflow meta/runtime tests execute through the pinned pi-subagents source.

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

The calibration workflow performs paid calls under its explicit bound, then runs this command only to replay and validate durable records. `PI_SKILL_CREATOR_REPLAY_ONLY=1` is a hard no-model-call mode. `PI_SKILL_CREATOR_LIVE_TESTS=1` alone is not approval.

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

The required `stageStartCommit` argument always names the exact clean repository commit at which that workflow invocation starts:

- for `stage: "calibrate"`, it equals the deterministic `implementationIntegrationCommit` returned by `.pi/workflows/pi-skill-creator-adoption.js`;
- for `stage: "finalize"`, it equals the `calibrationIntegrationCommit` returned by the earlier calibration invocation, after the human has reviewed that commit's campaign records.

Preflight requires repository `HEAD` to equal `stageStartCommit` exactly and the tree to be clean. The two stages remain separate invocations: calibration requires `approval: "APPROVE_PAID_CALIBRATION"`; finalization requires `approval: "APPROVE_CALIBRATION_RESULTS"`, `humanReviewComplete: true`, and the absolute immutable human review record. A commit argument, prior approval, or review-file existence never authorizes the other stage.

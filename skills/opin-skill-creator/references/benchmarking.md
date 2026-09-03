# Benchmarking

Use this quantitative branch for with-skill versus without-skill pass rates, variance, measured usage, blind output comparison, or description-trigger accuracy. Read the artifact contracts in [schemas.md](schemas.md) before preparing a campaign.

All `python -m scripts.<name>` commands below run from `${PI_SKILL_DIR}`. Campaign records belong under the evaluated project, never inside the distributed skill.

## Approval and campaign inputs

Obtain explicit user approval before any multi-agent tool call. Approval must cover the evaluation prompts, both configurations, repetitions, environment profile, and requested model and thinking level for every role. Do not infer approval from an earlier qualitative run. Pass `approved: true` only after the user approves this campaign.

Choose exactly one profile and keep it for the whole comparison:

- `in-situ` preserves the real evaluation cwd, instructions, extensions, and competing skills. Use it for trigger behavior and record the competing set.
- `hermetic-core` uses the isolated core resource baseline.
- `declared-dependencies` adds only declared absolute dependencies to that baseline. Fork and bundled-agent claims use this profile with the pinned pi-subagents extension.

Never aggregate different profiles. Record requested and observed effective model and thinking values separately. An absent or mismatched effective value invalidates the run.

The runtime workflow takes caller-supplied values only. Supply:

- `campaignId` matching `[a-z0-9][a-z0-9-]{0,63}` and `createdAt` as a UTC timestamp;
- absolute `projectRoot`, target `skillPath`, `${PI_SKILL_DIR}` as `skillCreatorPath`, `piExecutable`, `piCheckout`, and `piSubagentsCheckout`;
- one `environmentProfile`, a positive `iteration`, `repetitions`, and the complete `evals` array;
- each eval's positive `eval_id`, descriptive `eval_name`, realistic `prompt`, and non-empty `expectations`;
- explicit `model` and `thinking` entries for `executor`, `grader`, `comparator`, and `benchmarkAnalyzer`;
- `approved: true`.

The user supplies IDs and timestamps. The workflow never reads the clock or randomness. Use the absolute `SubagentWorkflow.scriptPath` formed from `${PI_SKILL_DIR}/workflows/benchmark.js` (expand `${PI_SKILL_DIR}` before the call; do not pass the placeholder literally). This runtime file is not a saved repository workflow and is not invoked by name.

A call has this shape:

```text
SubagentWorkflow
  scriptPath: /absolute/pi-skill-root/opin-skill-creator/workflows/benchmark.js
  args:
    approved: true
    campaignId: fork-smoke-1
    createdAt: 2026-09-02T12:00:00Z
    projectRoot: /absolute/evaluation-project
    skillPath: /absolute/skills/example-skill
    skillCreatorPath: /absolute/pi-skill-root/opin-skill-creator
    piExecutable: /absolute/bin/pi
    piCheckout: /absolute/checkouts/pi
    piSubagentsCheckout: /absolute/checkouts/pi-subagents
    environmentProfile: declared-dependencies
    iteration: 1
    repetitions: 3
    evals: <approved eval array>
    roles: <explicit role model/thinking object>
```

## Exact campaign tree

The campaign root is `<project-root>/.skill-creator/<skill-name>/campaign-<campaign-id>/`:

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

The only configurations are `with_skill` (treatment) and `without_skill` (control). The `run-N` layer is mandatory, and delta is treatment minus control. Every expected eval, configuration, and repetition must be present. Zero runs, an unexpected configuration, a missing arm, or a missing repetition invalidates the campaign and produces no benchmark claim.

`eval_metadata.json` and `evals.json` use `expectations`. Each expectation should be objectively verifiable and discriminating. Subjective qualities belong in human review rather than a weak expectation.

## Execution, grading, and telemetry

The runtime workflow prepares metadata, then uses `pipeline()` so each completed executor goes directly to its grader without waiting for every executor. Fan-out is capped. Each item is explicitly accounted as `completed`, `failed`, `skipped`, `bounded`, or `null`; failed gates and null schema results invalidate the campaign. The deterministic aggregator runs only when every expected run completed and graded. `parallel()` is reserved for synthesis that genuinely needs all prior results together, not ordinary execution or grading.

Fork and dependency executors are launcher agents that invoke `scripts.rpc_runner` with the explicit Pi executable, checkout, target skill, profile, model, thinking, identity, and run directory. The runner loads the target through `--skill` only for `with_skill`; `without_skill` omits it. Under `declared-dependencies`, it loads `<pi-subagents-checkout>/src/index.ts` explicitly. Do not add a separate `--skill` argument to the workflow call or claim that a prompt alone loads the target.

Use the supported evidence seam:

- A direct top-level `Agent` result exposes an `.output` JSONL path. Parse it as `pi-subagents-output-v1`.
- A workflow child exposes only final text or validated structured output, not its own `.output` path or top-level lifecycle events.
- A measured RPC executor writes `transcript.jsonl`, `run.json`, and `transcript-metrics.json`; those RPC artifacts are executor evidence.

Launcher usage is orchestration overhead. Never relabel it as executor usage or per-executor cost. The workflow returns `workflow_output_tokens` and marks per-launcher cost unavailable. Benchmark usage comes from authoritative executor transcript records, while character counts remain separate `_chars` fields.

The `grader` agent grades one run against every expectation and writes `grading.json` with cited evidence. After complete aggregation, use `benchmark-analyzer` to identify expectation, variance, cost, and failure patterns without suggesting edits. For a blind output-quality comparison, give outputs A and B to `comparator`, then give the winner and both skills to `comparison-analyzer` for unblinded causes and improvements. Keep the comparator blind to `with_skill`, `without_skill`, treatment, and control identity.

The workflow returns campaign and iteration paths, status counts, validity, requested roles, observed effective executor/grader metadata, `workflow_output_tokens`, and per-item results. Treat `valid: false` as no benchmark claim, even if some durable run artifacts exist.

## Aggregate and inspect

The workflow runs the deterministic equivalent of:

```bash
python -m scripts.aggregate_benchmark \
  <campaign-root>/iteration-N \
  --skill-name <skill-name>
```

The command writes `benchmark.json` and `benchmark.md` only from a complete valid iteration. Read both before presenting a numeric claim.

Launch the review viewer without discarding diagnostics:

```bash
python "${PI_SKILL_DIR}/eval-viewer/generate_review.py" \
  <campaign-root>/iteration-N \
  --skill-name "<skill-name>" \
  --benchmark <campaign-root>/iteration-N/benchmark.json \
  > /absolute/path/outside-campaign/viewer.log 2>&1 &
```

The server binds loopback, selects a free port if the requested port is occupied, prints its URL to the chosen log outside the exact campaign tree, and atomically writes its own PID to `viewer.pid`. Do not capture `$!` in one Pi shell call and expect it in another. Read the persisted file instead. Before stopping, verify that the PID still names this viewer and this iteration, then remove the stale PID file:

```bash
VIEWER_PID="$(cat <campaign-root>/iteration-N/viewer.pid)" && \
  kill -0 "$VIEWER_PID" && \
  ps -p "$VIEWER_PID" -o command= | grep -F "generate_review.py" | \
  grep -F "<campaign-root>/iteration-N" >/dev/null && \
  kill "$VIEWER_PID" && \
  rm -f <campaign-root>/iteration-N/viewer.pid
```

For a headless environment, do not start a server:

```bash
python "${PI_SKILL_DIR}/eval-viewer/generate_review.py" \
  <campaign-root>/iteration-N \
  --skill-name "<skill-name>" \
  --benchmark <campaign-root>/iteration-N/benchmark.json \
  --static /absolute/path/outside-campaign/review.html
```

The Outputs tab pages through runs and collects feedback. The Benchmark tab shows the quantitative comparison. “Submit All Reviews” writes `feedback.json`. Read that file before revising; empty run feedback means the user accepted that output. Re-run every arm into `iteration-N+1` after a revision.

## Description-trigger optimization

Optimize triggering only after skill content is stable, and skip it for a user-invoked or otherwise model-hidden skill. Build realistic should-trigger and near-miss should-not-trigger queries, review them with the user, and keep train, validation, and final-test partitions separate. The final test is evaluated once after candidate selection and is never optimizer input.

Run with explicit role configuration, a caller-chosen persistent campaign directory, and reporting disabled so the command never opens a browser unexpectedly:

```bash
python -m scripts.run_loop \
  --eval-set /absolute/path/to/approved-eval-set.json \
  --skill-path /absolute/path/to/skill \
  --trigger-consumer-model provider/model \
  --trigger-consumer-thinking low \
  --optimizer-model provider/model \
  --optimizer-thinking high \
  --results-dir <campaign-root> \
  --report none \
  --max-iterations 5 \
  --runs-per-query 3 \
  --verbose
```

Apply `best_description` only after showing the user the before/after descriptions, validation score, one-time final-test score, and persisted candidate history. Recheck the selected description against the invocation doctrine in `writing-principles.md`.

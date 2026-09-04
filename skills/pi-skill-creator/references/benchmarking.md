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

- `runtime` as `pi-subagents` or `pi-dynamic-workflows` (chosen by the preflight below) and the absolute `runtimeCheckout` of that runtime's source checkout;
- `campaignId` matching `[a-z0-9][a-z0-9-]{0,63}` and `createdAt` as a UTC timestamp;
- absolute `projectRoot`, target `skillPath`, `${PI_SKILL_DIR}` as `skillCreatorPath`, `piExecutable`, `piCheckout`, and `piSubagentsCheckout` (the RPC runner still loads pi-subagents for `declared-dependencies`, whichever runtime orchestrates; under `runtime: pi-subagents`, `runtimeCheckout` must equal `piSubagentsCheckout`). `projectRoot` must be a directory that persists: the campaign tree written under `<projectRoot>/.skill-creator/` is the only evidence any claim can rest on, the review record fingerprints those files, and the replay tests read them back. The workflow refuses a `projectRoot` inside an operating-system temporary directory (`/tmp`, `/private/tmp`, `/var/tmp`, `/var/folders`, `/dev/shm`) before spending anything; a deliberately disposable calibration passes `allowEphemeralProjectRoot: true`, and the campaign then records in its own notes that its location is volatile. Add `.skill-creator/` to the evaluation project's `.gitignore`: the records belong next to the project but are never committed;
- one `environmentProfile`, a positive `iteration`, `repetitions`, and the complete `evals` array;
- `maxAgentCalls`, a positive integer bounding the workflow children: the exact plan is `1 + 2 × scheduled runs + 2` (one setup launcher, one execute launcher and one grader per scheduled run, one validate launcher, one aggregate launcher), so one eval, two arms, and one repetition plan 7 calls. The workflow computes the plan before its first call and refuses a plan above the bound; at runtime a call that would exceed the bound is never launched and is accounted as `bounded`. The bound covers workflow children only: the comparator, any analyzer, and any viewer call made from the top-level session are counted separately by the approved campaign manifest, and measured RPC executor processes are counted by their `run.json` records;
- each eval's positive `eval_id`, descriptive `eval_name`, realistic `prompt`, and non-empty `expectations`;
- explicit `model` (`provider/id`, no thinking suffix) and `thinking` entries for `executor`, `grader`, `comparator`, and `benchmarkAnalyzer`; `thinking` is one of `minimal`, `low`, `medium`, `high`, `xhigh`, `max`, because `off` cannot be requested on both runtimes and a campaign must stay portable;
- `approved: true`.

The user supplies IDs and timestamps. The workflow never reads the clock or randomness. The script `${PI_SKILL_DIR}/workflows/benchmark.js` is one plain-JavaScript file that runs unchanged on both runtimes; expand `${PI_SKILL_DIR}` before the call and never pass the placeholder literally. It is not a saved workflow: never invoke it by name, and never use the `workflow` tool's `name` input.

## Runtime preflight

Before the call, check which workflow tool the session exposes:

- `workflow` present: pi-dynamic-workflows (pinned `c82d31af1e36b6f0e89cfcc4bdd728d982e22dc9`, version 3.10.1) is loaded and pi-subagents' `SubagentWorkflow` has stood down. Set `runtime: pi-dynamic-workflows`, set `runtimeCheckout` to the pi-dynamic-workflows checkout, read `${PI_SKILL_DIR}/workflows/benchmark.js`, and pass its content as `script`. The user's campaign approval is the explicit opt-in the `workflow` tool requires.
- Only `SubagentWorkflow` present: pi-subagents (pinned `7f569969445bf8bc6fbd7757f18db80b35de0ba9`, version 0.19.0) orchestrates. Set `runtime: pi-subagents`, set `runtimeCheckout` equal to `piSubagentsCheckout`, and pass the absolute `scriptPath`.
- Neither present: stop and tell the user that no workflow runtime is loaded; do not simulate the campaign with direct `Agent` calls.

The two calls have these shapes:

```text
SubagentWorkflow
  scriptPath: /absolute/pi-skill-root/pi-skill-creator/workflows/benchmark.js
  args:
    approved: true
    runtime: pi-subagents
    runtimeCheckout: /absolute/checkouts/pi-subagents
    campaignId: fork-smoke-1
    createdAt: 2026-09-02T12:00:00Z
    projectRoot: /absolute/evaluation-project
    skillPath: /absolute/skills/example-skill
    skillCreatorPath: /absolute/pi-skill-root/pi-skill-creator
    piExecutable: /absolute/bin/pi
    piCheckout: /absolute/checkouts/pi
    piSubagentsCheckout: /absolute/checkouts/pi-subagents
    environmentProfile: declared-dependencies
    iteration: 1
    repetitions: 1
    maxAgentCalls: 7
    evals: <approved eval array with one eval; 1 + 2 × scheduled runs + 2>
    roles: <explicit role model/thinking object>
```

```text
workflow
  script: <the full content of /absolute/pi-skill-root/pi-skill-creator/workflows/benchmark.js>
  args:
    approved: true
    runtime: pi-dynamic-workflows
    runtimeCheckout: /absolute/checkouts/pi-dynamic-workflows
    maxAgentCalls: 7
    <the same remaining args as above>
```

To continue an interrupted campaign, call the same tool again with its `resumeFromRunId`; both runtimes replay the unchanged leading calls from their journal and run the rest live. Every campaign record carries `workflow_runtime` and `workflow_runtime_revision`, and every numeric claim names its runtime. Switching runtimes is a new campaign: the earlier numbers do not carry over until the campaign is re-run.

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

The runtime workflow prepares metadata, then uses `pipeline()` so each completed executor goes directly to its grader without waiting for every executor. Fan-out is capped. Every `agent()` call goes through one `safeAgent()` wrapper: a `null` child result and a thrown child both become accounted `failed` items, so a failing child never aborts the campaign on either runtime. Each item is explicitly accounted as `completed`, `failed`, `skipped`, or `bounded` (the buckets sum to `expected_runs`), and a separate `failure_kinds` object counts `null_result`, `thrown`, `explicit`, and `contract` failures. After grading, a `Validate` phase runs `python -m scripts.aggregate_benchmark <iteration-dir> --validate-only`, which checks the whole iteration tree and writes nothing; Python validation is the authority, not a shell gate. The deterministic aggregator runs only when every expected run completed, graded, and validated. `parallel()` is reserved for synthesis that genuinely needs all prior results together, not ordinary execution or grading.

Fork and dependency executors are launcher agents that invoke `scripts.rpc_runner` with the explicit Pi executable, checkout, target skill, profile, model, thinking, identity, and run directory. The runner loads the target through `--skill` only for `with_skill`; `without_skill` omits it. Under `declared-dependencies`, it loads `<pi-subagents-checkout>/src/index.ts` explicitly. Do not add a separate `--skill` argument to the workflow call or claim that a prompt alone loads the target.

A run directory holds at most one measured executor call. The runner refuses a `--run-dir` that already contains `run.json` or `transcript.jsonl` (exit status 2, kind `invalid_input`) before launching any process, and it never deletes stale records; a retry needs a new run directory that the campaign plan accounts for. A failed run leaves its `transcript.jsonl` behind, so a failed directory is refused on retry as well.

Workflow children are plain launchers on both runtimes: the script never dispatches a bundled agent by type. The grader launcher is told to read `${PI_SKILL_DIR}/agents/grader.md` by absolute path and follow it, and its model and thinking come from `roles.grader`. Bundled-agent frontmatter (`tools`, `extensions`, `max_turns`) applies only to the top-level `Agent` path.

Use the supported evidence seam:

- A direct top-level `Agent` result exposes an `.output` JSONL path. Parse it as `pi-subagents-output-v1`. That path is in the session scratch directory, which the operating system reclaims at reboot, so copy the file into the campaign tree before citing it and parse the copy: a comparison record whose only transcript is the original path stops being verifiable the next time the machine restarts. For the comparator this means `comparisons/<eval-name>/comparator.output` beside `comparison.json`, with the metrics derived from that copy.
- A workflow child, under `SubagentWorkflow` or under `workflow`, exposes only final text or validated structured output, not its own `.output` path, usage, effective model, or top-level lifecycle events.
- A measured RPC executor writes `transcript.jsonl`, `run.json`, and `transcript-metrics.json`; those RPC artifacts are executor evidence.

Launcher usage is orchestration overhead. Never relabel it as executor usage or per-executor cost. The workflow returns `workflow_output_tokens` and marks per-launcher cost unavailable. Benchmark usage comes from authoritative executor transcript records, while character counts remain separate `_chars` fields.

The `grader` agent grades one run against every expectation and writes `grading.json` with cited evidence. After complete aggregation, use `benchmark-analyzer` to identify expectation, variance, cost, and failure patterns without suggesting edits. For a blind output-quality comparison, give outputs A and B to `comparator`, then give the winner and both skills to `comparison-analyzer` for unblinded causes and improvements. Keep the comparator blind to `with_skill`, `without_skill`, treatment, and control identity. The comparator is `claude-bridge/claude-opus-5` at `high` thinking (`max` for critical skills) and loads only `pi-claude-bridge`; requested and effective model must both equal that pin, and an unresolved pin fails the campaign. For outputs produced by Claude-family executors it is not family-independent, and the campaign record says so in `notes`.

The workflow returns `workflow_runtime`, campaign and iteration paths, status counts, failure kinds, stage statuses, validity, requested roles, observed effective executor/grader metadata, `workflow_output_tokens`, per-item results, and the call accounting `agent_calls_planned`, `agent_calls_made`, and `max_agent_calls` (`agent_calls_made` never exceeds `max_agent_calls`). Treat `valid: false` as no benchmark claim, even if some durable run artifacts exist; anything bounded also makes the result `valid: false`.

## Aggregate and inspect

The workflow runs the deterministic equivalent of:

```bash
python -m scripts.aggregate_benchmark \
  <campaign-root>/iteration-N
```

The command writes `benchmark.json` and `benchmark.md` only from a complete valid iteration; the skill name comes from `campaign.json` and the campaign directory, which it cross-checks. `python -m scripts.aggregate_benchmark <campaign-root>/iteration-N --validate-only` performs the same validation and writes nothing. Read both generated files before presenting a numeric claim, and name the recorded `workflow_runtime` with the claim.

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

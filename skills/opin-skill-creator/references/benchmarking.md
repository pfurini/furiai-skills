# Benchmarking

The quantitative branch: with/without pass rates with variance, a browser review viewer, blind A/B comparison, and description-trigger optimization. It drives the bundled harness — `scripts/`, `agents/`, `eval-viewer/`, and `assets/` in this skill's directory. Reach for it when the user wants numbers ("is it actually better?"), when the skill will be shared, or when qualitative iteration (testing.md) has plateaued and you need finer signal.

All `python -m scripts.<name>` commands run from this skill's directory. Exact JSON field names matter throughout — the viewer and aggregator read them literally; the full schemas are in [schemas.md](schemas.md).

## Contents

- Setup: evals and workspace
- Running a benchmark iteration
- Clean-slate runs (distribution claims)
- Grading
- Aggregating, analyzing, and the viewer
- Reading feedback and iterating
- Blind comparison
- Description-trigger optimization

## Setup: evals and workspace

Save the test prompts to `evals/evals.json` inside the skill directory (schema in schemas.md) — prompts first, assertions later. Results live in `.skill-creator/<skill-name>/` at the project root (the same workspace container as testing.md; one `.gitignore` line covers it), organized as `iteration-N/<eval-name>/` with one directory per test case, named for what it tests (not `eval-0`). Create directories as you go, not upfront.

## Running a benchmark iteration

1. **Spawn every run in the same turn** — for each eval, one with-skill subagent and one baseline subagent (no skill for a new skill; the pre-edit snapshot for an improved one). Each dispatch names the skill path (or none), the task, input files, and where to save outputs (`.../with_skill/outputs/` or `.../baseline/outputs/`).
2. **Write `eval_metadata.json`** per test case (`eval_id`, `eval_name`, `prompt`, `assertions` — empty for now). Re-create these whenever prompts change; don't assume they carry over between iterations.
3. **While runs execute, draft assertions.** Good assertions are objectively verifiable, discriminating (pass when the skill genuinely succeeds, fail when it doesn't — "file exists" discriminates nothing), and named descriptively so the benchmark reads at a glance. Don't force assertions onto subjective qualities; those stay in the human review. Update the metadata files and `evals/evals.json` once drafted.
4. **Capture timing as each task-completion notification arrives**: save its `total_tokens` and `duration_ms` immediately to `timing.json` in the run directory — the notification is the only place this data exists.

## Clean-slate runs (distribution claims)

Numbers meant to travel — "this skill raises pass rate by X" for a skill others will install — must come from an environment a stranger would have. In-session subagents can't provide it; run executors as subprocesses:

```bash
(
  cd <empty-scratch-directory>
  PI_CODING_AGENT_DIR=<scrubbed-profile> pi --no-context-files --no-extensions \
    --no-skills --skill <path/to/skill-under-test> --no-prompt-templates \
    --no-themes --no-session --no-approve -p "<eval prompt>" \
    --model <provider/model-id>
)
```

- The scrubbed profile is a directory (mode 700) holding only auth: an `auth.json` copy (mode 600). No AGENTS.md, no `skills/`, no settings — and the command disables context files, extension discovery, skill discovery, prompt templates, and themes, so global instructions and installed skills do not load. Verify the profile before trusting a benchmark: probe for a rule distinctive to the real config ("what tool must replace pip per your instructions?") and require the scrubbed answer to be "none".
- Pi has no `--bare` mode; keep the resource-disabling flags in the command above.
- Run from an empty scratch directory outside any repo — project AGENTS.md files are discovered by walking up parent directories, so ancestry must be clean too.
- `--model` pins the executor; record its exact `provider/model-id` as `executor_model` in the benchmark metadata — a pass rate without its model is not a result. Default it to the skill's declared executor floor.
- `--skill` exposes only the skill under test, and the prompt names its path and says to read SKILL.md and follow it (nothing auto-loads under the scrubbed profile). Baseline runs drop both.
- Each `-p` invocation is a fresh context: the clean-slate equivalent of the fresh-subagent dispatch in testing.md. No further per-run isolation is needed.
- Managed/policy-level instructions still load and cannot be excluded — record them in the benchmark metadata if present. Delete the copied `auth.json` when the benchmark campaign ends.

Label each benchmark.json with the mode that produced it (in-situ or clean-slate); the two aren't comparable to each other. Description-trigger optimization stays in-situ: whether a skill fires depends on the competing skills around it, so the real environment is the correct test bed there.

## Grading

Grade each run against `agents/grader.md` (spawn a grader subagent or grade inline): every assertion gets a pass/fail with cited evidence, and the grader also critiques the evals themselves — flagging assertions a wrong output would still pass and outcomes nothing checks. Where an assertion is programmatically checkable, write and run a script instead of eyeballing; it's reusable next iteration.

Save `grading.json` per run. The expectations array uses exactly the fields `text`, `passed`, `evidence` — the viewer reads these names literally.

## Aggregating, analyzing, and the viewer

1. Aggregate: `python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>` → `benchmark.json` + `benchmark.md` with pass rate, time, and tokens per configuration, mean ± stddev, and the delta.
2. Analyst pass: per the "Analyzing Benchmark Results" section of `agents/analyzer.md`, surface what aggregates hide — assertions passing in both configurations (non-discriminating), high-variance evals (flaky), time/token trade-offs.
3. Launch the viewer **before** doing your own revision pass — get outputs in front of the human first:

   ```bash
   nohup python <this-skill-path>/eval-viewer/generate_review.py \
     <workspace>/iteration-N --skill-name "<name>" \
     --benchmark <workspace>/iteration-N/benchmark.json > /dev/null 2>&1 &
   VIEWER_PID=$!
   ```

   From iteration 2 on, add `--previous-workspace <workspace>/iteration-N-1`. Headless or no-display environments: add `--static <output.html>` and give the user the file to open; their submitted feedback downloads as `feedback.json` — copy it into the workspace. Always use `generate_review.py`; never hand-write a viewer.
4. Tell the user: the Outputs tab pages through test cases with a feedback box per run; the Benchmark tab shows the quantitative comparison; "Submit All Reviews" saves `feedback.json` when they're done.

## Reading feedback and iterating

Read `feedback.json` when the user says they're done, then `kill $VIEWER_PID`. Empty feedback on a run means it was fine; concentrate improvements where complaints are specific, following the iteration principles in testing.md (generalize, prune, bundle, close loopholes). Re-run the full iteration — including baselines — into `iteration-N+1/`.

## Blind comparison

For a rigorous "is version B actually better than version A": run both versions on the same evals, then give the two outputs to a comparator subagent (`agents/comparator.md`) labeled only A and B — it judges on output quality without knowing which skill produced which, generating a task-specific rubric. Then an analyzer subagent (`agents/analyzer.md`) unblinds: reads both skills and both transcripts, and explains *why* the winner won as prioritized, concrete improvement suggestions for the loser. Optional; the human review loop usually suffices.

## Description-trigger optimization

Optimizes the description for triggering accuracy. Run it last, after the skill's content is settled (requires the `pi` CLI).

1. **Generate ~20 trigger queries**, 8–10 should-trigger and 8–10 should-not, as `[{"query": ..., "should_trigger": true}, ...]`. Queries must read like real user messages: file paths, personal context, typos, casual phrasing, varied lengths. Should-trigger queries cover different phrasings per branch, including ones that never name the skill or file type. Should-not queries must be **near-misses** — shared keywords, adjacent domains, a naive keyword match would fire — never obviously irrelevant filler, which tests nothing.
2. **Review with the user**: fill the placeholders in `assets/eval_review.html` (`__EVAL_DATA_PLACEHOLDER__` gets the raw JSON array, plus skill name and description placeholders), open it, and let them edit and export. The exported `eval_set.json` lands in `~/Downloads` — take the newest copy. Bad queries produce bad descriptions; don't skip the review.
3. **Run the loop in the background**:

   ```bash
   python -m scripts.run_loop --eval-set <eval_set.json> --skill-path <skill> \
     --model <model-id-of-this-session> --max-iterations 5 --verbose
   ```

   Use this session's model ID so triggering matches what the user experiences. It splits 60/40 train/test, measures trigger rate (3 runs per query), proposes revised descriptions from the failures, and selects `best_description` by held-out test score. Tail the output periodically to report progress.
4. **Apply**: update the frontmatter with `best_description`, show the user before/after with scores — then re-check it against the description doctrine in writing-principles.md (capability + triggers, no workflow summary) before accepting.

# Testing Skills

The procedure behind Steps 2, 5, and 6 of the spine: baseline runs, forward-tests, and the loophole-closing loop. Read in full the first time; return to specific sections on later iterations.

## Contents

- Why baseline first
- Hygiene: keeping tests uncontaminated
- Environment fidelity
- Campaign workspace
- The test loop
- Measured-run evidence
- What to test, by skill type
- Pressure scenarios (discipline skills)
- Closing loopholes
- Micro-testing wording
- When to stop

## Why baseline first

The baseline is the control. Running the task without the skill, before writing it, tells you three things nothing else can:

1. **Whether a skill is needed at all.** If the agent already succeeds, every line you'd write is a no-op — stop.
2. **What exactly to write.** The documented failures are the spec: the draft addresses those failures and nothing else, instead of what you _imagine_ needs preventing. Guessing produces skills that defend against hypothetical failures while missing real ones.
3. **What "better" means later.** Forward-test results are only evidence relative to a baseline.

This is test-driven development applied to process documentation: watch it fail (baseline), write the minimal skill that makes it pass (draft), close loopholes while staying green (iterate). If you didn't watch an agent fail without the skill, you don't know whether the skill teaches the right thing.

Baselines apply to edits too. Improving an existing skill? Snapshot the current version first — the snapshot is the baseline the edited version must beat.

## Hygiene: keeping tests uncontaminated

A test only measures generalization if the subagent can't reconstruct the answer from leaked context. Rules for every baseline and forward-test dispatch:

- **The subagent must not know it's testing a skill.** It is an agent given a task by a user. Prompt: `Use <skill-name> at <path/to/skill> to <task>` — never "review the skill at…" or "pretend a user asks…". Baseline runs get the bare task with no skill mentioned.
- **Word the task as the user would**, with the realism of real usage: actual file paths, casual phrasing, the detail level of a genuine request.
- **Pass raw artifacts** — input files, example prompts, logs — with the minimum task-local context needed. Withhold the expected answer, the suspected bug, the intended fix, and your prior conclusions.
- **Fresh subagent per run, fresh context per iteration.** Rebuild from source artifacts each time.
- **Clean up between iterations.** Outputs a previous run left on disk are leaked context for the next one — remove them before re-dispatching.
- **Keep control copies and planted fixtures in paths the subagent has no reason to visit.** A subject that can see the `baseline/` twin of its own input has learned it is inside a harness.
- **Run test subagents in a working directory that contains neither the skill corpus nor its authoring guides.** A baseline that can read the doctrine under test isn't a baseline.
- **Keep authoring material outside the evaluation cwd.** The subject must not be able to discover the skill corpus, this doctrine, or control artifacts by walking its working tree. Store durable records in the campaign workspace described below.

If a forward-test only succeeds when the subagent sees leaked context, tighten the skill or the test setup before trusting the result.

## Environment fidelity

Choose exactly one environment profile for every run and match it to the claim being tested:

- **`in-situ`**: Run in the real evaluation cwd with user, global, and project instructions plus installed and competing skills present. Use this profile for trigger behavior, record the exact competing set, and treat behavior already enforced by the environment as a no-op for that user.
- **`hermetic-core`**: Use an in-harness subagent configured with `prompt_mode: replace`, `inherit_context: false`, `isolated: true`, `skills: false`, and built-in tools only. Add `isolation: worktree` whenever it writes so parallel writers have worktree isolation.
- **`declared-dependencies`**: Start from the hermetic resource baseline and add only the absolute extensions or skills declared in `campaign.json`. Use it for fork and bundled-agent behavioral claims, launching through Pi RPC with pi-subagents explicitly loaded as `-e <pi-subagents>/src/index.ts`.

Never aggregate different profiles into one comparison. A profile mismatch is fatal: invalidate the run rather than relabeling, repairing, or comparing it.

## Campaign workspace

Put durable test records under the exact campaign root `<project-root>/.skill-creator/<skill-name>/campaign-<campaign-id>/`. The caller supplies `campaign-id`; evaluation directories use a descriptive `<human-readable-eval-name>`. Use the treatment name `with_skill`, the control name `without_skill`, and the mandatory `run-N` repetition layer:

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

Keep tests, fixtures, reports, and campaign records outside the distributable skill directory. Quantitative campaign commands and schemas belong to [benchmarking.md](benchmarking.md).

## The test loop

1. **Choose the supported execution mechanism and get approval.** Use direct `Agent` calls for a known small qualitative set. Use the session's workflow runtime for dynamic or staged fan-out: `SubagentWorkflow` under pi-subagents (`7f569969445bf8bc6fbd7757f18db80b35de0ba9`), or `workflow` under pi-dynamic-workflows (`e9c5a41d9c4234df908aa25a2b49ee9648e896d4`), which makes `SubagentWorkflow` stand down when both are loaded. Any multi-agent execution requires explicit user approval before the tool call. If multiple agents write in parallel, give each writer worktree isolation; never let parallel writers share a checkout.
2. **Dispatch every run for the iteration together**: treatment and control for each example prompt. Use one fresh subject per run so neither arm waits on or contaminates the other. Run forward-tests on the executor floor from Step 1 (compliance by a stronger model is not evidence), and include at least one single-pass consumer when the output has a required shape.
3. **Read the transcripts, not just the outputs.** The output shows whether it worked; the transcript shows how, and the process is what the skill is changing.
4. **Compare each `with_skill` transcript to its `without_skill` control** and collect three kinds of signal:
   - **Baseline failures now fixed**: the evidence the skill works. Quote it.
   - **Repeated work across runs**: multiple runs independently writing the same helper script or taking the same multi-step detour means that code or knowledge belongs in the skill's `scripts/` or `references/`.
   - **Skill-induced waste**: the agent doing something unproductive because the skill told it to. Delete the instruction and re-test; the transcript, not the prose, decides what stays.
5. **Show the user the outputs** and gather reactions before revising. Their complaints, not your inference, set the next iteration's priorities. Empty feedback on a run means it was fine; focus where they had specific complaints.
6. Revise, then re-run into a new `iteration-N+1/` directory. Controls for a new skill stay `without_skill`; for an edited skill, use the snapshot.

## Measured-run evidence

Use only the telemetry seam supported by the execution mechanism:

- **Direct measured runs**: top-level `Agent` `.output` paths are returned by results and completion notifications. Each file contains JSONL message snapshots, not tool lifecycle events. Parse it as `pi-subagents-output-v1`; derive tool calls from assistant `toolCall` content and usage or effective model from authoritative assistant messages.
- **Workflow orchestration**: `SubagentWorkflow` (pi-subagents) and `workflow` (pi-dynamic-workflows) children return final text or validated structured output. Workflow children do not expose an `.output` path, usage, effective model, or top-level lifecycle events on either runtime. Do not claim per-child transcripts or cost, and do not substitute launcher-agent telemetry for executor evidence.
- **Fork or dependency measured runs**: use Pi RPC with the declared dependencies loaded explicitly. Preserve the Pi JSON event stream in `transcript.jsonl`, parse it as `pi-json-events-v3`, and use its `run.json` and `transcript-metrics.json` records as executor evidence.

Capture `total_tokens` and `duration_ms` when a direct task's completion notification arrives so notification-only timing is not lost. Notification capture is not the only recoverable usage source: authoritative transcript messages supply usage and effective-model evidence. Treat absent or mismatched effective profile, model, thinking, usage, or completion metadata as an invalid run.

## What to test, by skill type

- **Discipline skills** (enforce a rule with a compliance cost — TDD, verification gates): pressure scenarios, below. An easy prompt proves nothing; the rule must hold when the agent wants to break it.
- **Technique skills** (how-to methods): application to a new scenario, a variation with an edge case, and a gap check — does the instruction sequence have holes the agent must improvise across?
- **Pattern skills** (mental models): recognition (does the agent see when it applies?), application, and a counter-example where it should _not_ apply.
- **Reference skills** (docs, schemas, APIs): retrieval (finds the right section), application (uses it correctly), and coverage of the common cases. Pure reference skills need no pressure testing — there's no rule to be tempted against.

## Pressure scenarios (discipline skills)

A discipline skill exists precisely for the moment the agent is tempted. Test that moment:

- **Combine 3+ pressures.** Agents resist one pressure and break under several.

| Pressure | Example |
|---|---|
| Time | Emergency, deadline, deploy window closing |
| Sunk cost | Hours of work it feels wasteful to delete |
| Authority | Senior engineer or manager says skip it |
| Economic | Job, promotion, company survival at stake |
| Exhaustion | End of day, already tired |
| Social | Looking dogmatic or inflexible |
| Pragmatism | "Being pragmatic, not dogmatic" |

- **Force a concrete choice.** Offer options A/B/C and require one; open-ended questions let the agent recite the rule without committing. "What do you do?", not "what should you do?".
- **Make it real**: specific times, real file paths, actual consequences, and a framing line — "This is a real scenario. Choose and act." — so it reads as work, not a quiz.
- **No easy outs**: the scenario shouldn't allow deferring to "I'd ask the user" without choosing.

Example shape:

> You spent 3 hours and 200 lines; it works, you manually tested it. It's 6pm, dinner at 6:30, review tomorrow at 9. You just realized you didn't follow TDD.
> A) Delete it, restart with TDD tomorrow. B) Commit now, tests tomorrow. C) Write tests now, 30 minutes.
> Choose A, B, or C.

Run it baseline-first: the options the agent picks and the excuses it gives, verbatim, are the exact material the skill must counter.

## Closing loopholes

When a run violates the rule despite the skill (or the baseline shows how it will), respond structurally — this is the one failure class where prohibitions and counters are the right form:

1. **Capture the rationalization verbatim.** "Tests after achieve the same goals", "I'm following the spirit, not the letter", "keep it as reference". "The agent was wrong" tells you nothing to fix.
2. **Counter it explicitly in the rule.** Not "delete it" but "delete it — don't keep it as reference, don't adapt it while writing tests, delete means delete." Generic counters ("don't cheat") do nothing; name the specific move.
3. **Add it to a rationalization table** — excuse next to reality — and to a **red-flags list** the agent can self-check against ("'this case is different because…' — stop").
4. **Cut off spirit-vs-letter early** with a foundational line: violating the letter of the rule is violating its spirit.
5. **Add violation symptoms to the description** — the phrases running through the agent's head right before it breaks the rule ("when tempted to test after, when manual testing seems faster") — so the skill fires at the moment of temptation.
6. **Meta-test when stuck**: ask the violating agent, "you read the skill and chose C anyway — how should it have been written so A was clearly the only answer?" Its answer distinguishes a wording problem (add its suggestion verbatim), an organization problem (make the section prominent), or a strength problem (it understood and defied — add the foundational principle).
7. **Re-test.** A new rationalization restarts this list; compliance ends it.

The skill is bulletproof when the agent chooses correctly under maximum pressure, cites the skill as justification, and acknowledges the temptation rather than negotiating with it.

## Micro-testing wording

Full subagent scenarios are the final gate but slow per iteration. When iterating on a specific piece of wording, test the wording alone first:

1. One fresh-context sample per call — a raw API call or single-shot subagent, with the guidance embedded in its realistic surrounding context (the full skill, not the sentence in isolation) and a task that tempts the failure.
2. **Always include a no-guidance control.** If the control doesn't fail, there's nothing to fix — don't author the guidance.
3. **5+ reps per variant** — single samples lie.
4. **Read every flagged match by hand** — template echoes and quoted counter-examples masquerade as hits in programmatic counts.
5. **Variance is a metric.** Five reps converging on one shape means the wording binds; five interpretations means it doesn't — tighten the form before adding words.

Micro-tests verify wording; they don't replace pressure scenarios for discipline skills.

## When to stop

Stop iterating when forward-tests comply and the user is satisfied, when feedback comes back empty, or when an iteration produces no meaningful change. Say which condition ended the loop. An edit made after the last test run invalidates the pass — re-run the tests, or state explicitly that the edit shipped untested. For quantitative evidence beyond this qualitative loop — pass rates, variance, with/without deltas, trigger accuracy — move to [benchmarking.md](benchmarking.md).

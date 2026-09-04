# Handoff: pi-skill-creator, next session

Written 2026-09-03 at the end of the session that ported the skill to Pi and renamed it back to `pi-skill-creator`. Everything durable is in the repository; this file records the decisions and state that existed only in that session's context.

## State

- furiai-skills `main` at `97dddf9` ("rename opin-skill-creator to pi-skill-creator"), clean, 30 commits ahead of `origin/main`.
- Deterministic adoption (work orders OSC-00 through OSC-13) is integrated; the last pre-rename integration commit was `24a0413`. The rename commit is now the start point for any later stage that requires a clean `HEAD`.
- Remaining work orders: OSC-14 (paid calibration), OSC-15 (apply human-reviewed conclusions), OSC-16 (copied-directory distribution validation). None started.
- Test tiers: `uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator -m 'not live'` passes 111 with `PI_CHECKOUT` set; the 13 pi-subagents contract tests skip without `PI_SUBAGENTS_CHECKOUT` and fail with it because that checkout moved (see pins). `uvx --from 'ty==0.0.77' ty check skills/pi-skill-creator/scripts skills/pi-skill-creator/eval-viewer` passes. `python3 scripts/quick_validate.py .` passes from the skill directory.
- Authoritative documents: `docs/pi-skill-creator-adoption-report.md`, `docs/pi-skill-creator-work-orders/index.md` and `contracts.md`, the OSC files, `tests/pi-skill-creator/README.md`.
- In `/Users/paolof/Developer/ai/pi-dynamic-workflows`, `docs/parity/` (index, gap analysis, effort report, seven handoffs) is written but untracked; commit it there.

## Pinned runtimes

| Component | Revision | Note |
|---|---|---|
| Pi fork | `a4043c1e332a61e4c8648b97b9b796c57f9db110`, reports `0.84.4`, branch `personal` | executable `/Users/paolof/.local/bin/pi` |
| pi-subagents | pinned `bfa262fdd75d807b1c6b1f852f1f1bea2bbb3fa4` (0.19.0); checkout now at `7f569969445bf8bc6fbd7757f18db80b35de0ba9` | the extra commit makes the workflow-tool collision check case-insensitive, which is what lets its `SubagentWorkflow` stand down for pi-dynamic-workflows; keep it and re-pin during the portability work |
| pi-dynamic-workflows | `4aaf451a97707aa7f614fc5c103ed57ae3b290c7`, 3.10.0 | registers the `workflow` and `workflow_control` tools; no `node_modules` in that checkout |
| pi-claude-bridge | `fcfe846570ae0b290d4b628e8b19f8068611e9af`, 0.7.0 | checkout had uncommitted changes in `src/index.ts` and `src/usage-publisher.ts`; must be clean and pinned before calibration |

Scoped models (`~/.pi/agent/settings.json` `enabledModels`) include `openai-codex/gpt-5.6-{luna,sol,terra}`, `claude-bridge/claude-{sonnet-5,opus-4-8,opus-5,fable-5,haiku-4-5}`, `cursor-bridge/grok-4.6`, `zai/glm-5.3`, `zai/glm-5.3-flash`. `claude-bridge/claude-fable-5-1` resolves in Pi but is not in the scoped list; add it if it will be used.

## Decisions taken in conversation (not yet applied in code)

1. **Blind comparator model**: `claude-bridge/claude-opus-5`, thinking `high` (`max` for critical skills). Replace `openrouter/~anthropic/claude-opus-latest` everywhere: `skills/pi-skill-creator/agents/comparator.md`, `tests/pi-skill-creator/test_bundled_agents.py`, `contracts.md` C10, the report's model policy. The comparator file currently has `extensions: false`, which would hide the `claude-bridge` provider under pi-subagents; it must load only `pi-claude-bridge`, and requested and effective model must both equal `claude-bridge/claude-opus-5`, failing rather than falling back.
2. **Target is Pi only.** No Claude Code compatibility in the skill or its workflow.
3. **Orchestrator independence.** pi-dynamic-workflows becomes the primary workflow extension; pi-subagents stays installed for its `Agent` tool and its workflow tool stands down. The skill must work on both runtimes. Agreed design for `skills/pi-skill-creator/workflows/benchmark.js`:
   - shared subset only: `meta{name,description,phases[{title}]}`, `phase`, `agent`, `parallel`, `pipeline`, `log`, `args`, `budget.spent()`; `agent()` options `label`, `phase`, `schema`, `model`;
   - one runtime shim keyed on a validated `args.runtime` (`pi-subagents` uses `effort`, `pi-dynamic-workflows` uses `model: "provider/id:thinking"`);
   - `safeAgent()` maps both `null` and thrown errors to accounted `failed` items;
   - no `gate:`; Python validation is the authority (add an `aggregate_benchmark --validate-only` step run by a launcher agent after execution);
   - no `agentType`; role prompts tell the child to read the skill's `agents/<role>.md` by absolute path, with model and thinking from `args.roles`;
   - no worktree isolation for launchers (campaign records live under the project);
   - docs name both invocations (`SubagentWorkflow` with `scriptPath`, `workflow` with the file content as `script`) plus a preflight that checks which tool exists;
   - tests execute the same script through both pinned runtimes; running pi-dynamic-workflows from tests needs `npm install` in that checkout or an equivalent prerequisite.
   Verify before writing: that pi-subagents rejects a `:thinking` suffix in `model` (it lists `effort` separately and rejects unknown option keys); that `claude-bridge/claude-opus-5` resolves for a pi-dynamic-workflows child through the shared registry.
4. **Sequencing**: port `benchmark.js` and its docs and tests first. Live calibration runs under pi-subagents, because the user is not activating pi-dynamic-workflows yet; every claim must record that runtime, and a later switch invalidates numeric claims until re-run. The development workflows (`.pi/workflows/pi-skill-creator-adoption.js` and `-calibration.js`) stay on pi-subagents; they are repository tooling.
5. **The creator stays unpinned** (no `model`/`effort` in `SKILL.md`); the user chooses Opus 5 or Fable 5.1 per task.
6. **Calibration is right-sized to a smoke test.** The two-track, multi-family campaign program discussed earlier is dropped; it optimized for publishable benchmark claims nobody asked for. OSC-14 becomes one bounded end-to-end run under pi-subagents whose only purpose is to prove the machinery (RPC runner, transcript parser, grader, comparator, aggregator, viewer) works with real models: one eval, two arms, one or two repetitions, one consumer model, one grading per run, one comparison, about 10 to 15 measured calls and 1M to 2M tokens, `maxPaidCalls` around 40. OSC-15 becomes claim hygiene: keep historical numbers labeled historical or delete them, add no new numbers, and verify that the grader, comparator, and analyzer pins resolve. OSC-16 is unchanged. Evidence for any future claim accumulates from real Step 7 campaigns on skills the user actually builds; the multi-turn reasoning harness is deferred with the program. Before the smoke run, still harden `.pi/workflows/pi-skill-creator-calibration.js`: strict schemas for `models` and `scenarios`, `maxPaidCalls` enforced mechanically before each measured call (orchestration calls counted separately), `stageStartCommit` validated as a 40-hex SHA and shell-quoted, explicit `pi-claude-bridge` loading, and the `bounded_work` versus `skipped_work` clarification below. Update the OSC-14 and OSC-15 work orders and the index's completion definition to this scope before running anything.
7. **Adoption workflow fixes to persist** (the successful run used a temporary recovery copy that may no longer exist at `/tmp/opin-skill-creator-adoption-resume-e6667a066d0f.js`): integration agents were assigned `phase: 'Integrate'`, which made the UI show phase 10 running between phases; group each integration under its implementation phase. Writer prompts must state that `tests_skipped` is for intentionally skipped tests, `bounded_work` for mandated exclusions, and `skipped_work` only for required work left incomplete (must be `[]` on completion); the first run failed because OSC-00 listed mandated exclusions under `skipped_work`.
8. **Overnight runs**: the machine slept for nine hours mid-workflow. Launch Pi with `caffeinate -dimsu pi` for long workflows.

## Model policy (reference, not a campaign plan)

The user creates and optimizes skills with `claude-bridge/claude-opus-5` at `max`, or `claude-bridge/claude-fable-5-1` at `high` for the toughest skills. Produced skills run on medium and large models, never on the lowest tier: reasoning skills on Opus 5, Fable, GPT-5.6 Sol, sometimes GLM-5.3; executor skills on Sonnet 5, GPT-5.6 Terra, GLM-5.3-flash. Forward tests and Step 7 campaigns for a produced skill should use the model and thinking it will actually run on.

Bundled-agent pins, chosen by policy and verified by resolution preflight only:

| Role | Model | Thinking |
|---|---|---|
| Grader, comparison analyzer | `openai-codex/gpt-5.6-sol` | high |
| Blind comparator | `claude-bridge/claude-opus-5` | high |
| Benchmark analyzer | `openai-codex/gpt-5.6-terra` | medium |

Never aggregate different effective models or profiles in one campaign. For Claude-produced outputs the Opus comparator is not family-independent; note it in the record rather than adding an audit campaign.

## Working method that worked

- Fresh `general-purpose` writer with `inherit_context: false`, then a separate fresh read-only verifier; the verifier caught nothing the writer missed only once, so keep both.
- Isolated worktrees per implementation order, exclusive path ownership per wave, scoped `ty` gates before OSC-07 and the full gate after.
- Report is evidence; work orders are the executable queue.

## Suggested first steps

1. Commit `docs/parity/` in pi-dynamic-workflows.
2. Write a work order (OSC-17, "orchestrator-independent benchmark workflow") from decision 3, covering `benchmark.js`, `references/benchmarking.md`, `references/testing.md`, `SKILL.md` Step 7, `README.md`, `test_runtime_workflow.py` plus a pi-dynamic-workflows execution test, and the pi-subagents re-pin to `7f569969`.
3. Apply decision 1 (comparator) in the same or an adjacent order, since `test_bundled_agents.py` pins the comparator model.
4. Rewrite OSC-14 and OSC-15 to the smoke-test scope in decision 6, harden the calibration workflow, then present the exact smoke manifest and `maxPaidCalls` for approval before any measured call.

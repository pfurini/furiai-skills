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
4. **Sequencing**: port `benchmark.js` and its docs and tests first, then run calibration under pi-dynamic-workflows. The development workflows (`.pi/workflows/pi-skill-creator-adoption.js` and `-calibration.js`) stay on pi-subagents; they are repository tooling.
5. **The creator stays unpinned** (no `model`/`effort` in `SKILL.md`); the user chooses Opus 5 or Fable 5.1 per task.
6. **Calibration hardening before any paid call** (`.pi/workflows/pi-skill-creator-calibration.js`): strict schemas for `models` and `scenarios`; `maxPaidCalls` enforced mechanically before each measured call, counting orchestration calls separately; `stageStartCommit` validated as a 40-hex SHA and shell-quoted; explicit `pi-claude-bridge` loading; the `bounded_work` versus `skipped_work` handoff clarification (see below); multi-turn reasoning scenarios, because the RPC benchmark is one-shot and does not represent interactive reasoning skills.
7. **Adoption workflow fixes to persist** (the successful run used a temporary recovery copy that may no longer exist at `/tmp/opin-skill-creator-adoption-resume-e6667a066d0f.js`): integration agents were assigned `phase: 'Integrate'`, which made the UI show phase 10 running between phases; group each integration under its implementation phase. Writer prompts must state that `tests_skipped` is for intentionally skipped tests, `bounded_work` for mandated exclusions, and `skipped_work` only for required work left incomplete (must be `[]` on completion); the first run failed because OSC-00 listed mandated exclusions under `skipped_work`.
8. **Overnight runs**: the machine slept for nine hours mid-workflow. Launch Pi with `caffeinate -dimsu pi` for long workflows.

## Model policy agreed with the user

The user creates and optimizes skills with `claude-bridge/claude-opus-5` at `max`, or `claude-bridge/claude-fable-5-1` at `high` (sometimes higher) for the toughest skills. Produced skills run on two populations, never on the lowest tier (no Luna, no Haiku):

- reasoning skills (brainstorming, architecture, hard research) on Opus 5 or Fable at `high`, GPT-5.6 Sol at `high`, sometimes GLM-5.3 at `high` or `max`;
- executor skills (tests, implementation plans, bug verification) on Sonnet 5 at `medium` or `high`, GPT-5.6 Terra at `medium`, GLM-5.3-flash at `high` or `max`.

Calibration roles and tracks:

| Role | Model | Thinking |
|---|---|---|
| Campaign orchestration, grader, comparison analyzer | `openai-codex/gpt-5.6-sol` | high |
| Blind comparator | `claude-bridge/claude-opus-5` | high (max for critical) |
| Benchmark analyzer, integration | `openai-codex/gpt-5.6-terra` | medium |
| Creator and optimizer under test | `claude-bridge/claude-opus-5` max; `claude-bridge/claude-fable-5-1` high for the critical suite | |
| Reasoning-track consumers (separate campaigns) | Opus 5 high, Fable 5.1 high, Sol high, GLM-5.3 high | |
| Executor-track consumers (separate campaigns) | Sonnet 5 medium and high, Terra medium, GLM-5.3-flash high | |

Never aggregate different effective models or profiles in one campaign. Trigger tests use the same model and thinking as the corresponding execution campaign. For Claude-produced outputs the Opus comparator is not family-independent; add a blind `zai/glm-5.3` high disagreement audit on a stratified subset. Calibrate the executor track first (the one-shot harness already represents it), then extend the harness for multi-turn reasoning sessions.

## Working method that worked

- Fresh `general-purpose` writer with `inherit_context: false`, then a separate fresh read-only verifier; the verifier caught nothing the writer missed only once, so keep both.
- Isolated worktrees per implementation order, exclusive path ownership per wave, scoped `ty` gates before OSC-07 and the full gate after.
- Report is evidence; work orders are the executable queue.

## Suggested first steps

1. Commit `docs/parity/` in pi-dynamic-workflows.
2. Write a work order (OSC-17, "orchestrator-independent benchmark workflow") from decision 3, covering `benchmark.js`, `references/benchmarking.md`, `references/testing.md`, `SKILL.md` Step 7, `README.md`, `test_runtime_workflow.py` plus a pi-dynamic-workflows execution test, and the pi-subagents re-pin to `7f569969`.
3. Apply decision 1 (comparator) in the same or an adjacent order, since `test_bundled_agents.py` pins the comparator model.
4. Harden the calibration workflow per decision 6, then present an exact campaign manifest and paid-call cap for approval before any measured call.

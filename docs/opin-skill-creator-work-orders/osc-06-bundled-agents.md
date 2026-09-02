# OSC-06: Split, register, and lock bundled agents

## Findings

Primary: F12, F13, F14, F20, and F25a. Secondary consumer of F25b/F28/F29.

## Dependencies

OSC-00 and OSC-01.

## Settled decisions restated

- Exactly four runtime identities exist: `grader`, `comparator`, `comparison-analyzer`, and `benchmark-analyzer`; `agents/analyzer.md` is deleted, and no executor agent is added or pinned.
- All four use `prompt_mode: replace`, `inherit_context: false`, `skills: false`, `persist_session: false`, and `output_transcript: true`. Grader/comparator run in background; both analyzers run in foreground.
- The provisional comparator is `openrouter/~anthropic/claude-opus-latest` with `high` thinking. Every requested pin must resolve in its selected profile; unresolved models fail rather than inherit a parent model.

## Exclusive owned paths

- `skills/opin-skill-creator/agents/grader.md`
- `skills/opin-skill-creator/agents/comparator.md`
- `skills/opin-skill-creator/agents/analyzer.md` (delete)
- `skills/opin-skill-creator/agents/comparison-analyzer.md` (new)
- `skills/opin-skill-creator/agents/benchmark-analyzer.md` (new)
- `tests/opin-skill-creator/test_bundled_agents.py`

## Read-only references

- `contracts.md` C8 and C10
- pinned pi-subagents agent loader, invocation config, model resolver, skill agent adapter, and protocol v3 sources
- transcript parser and schemas
- `SKILL.md` and `references/benchmarking.md` (OSC-12 owns dispatch prose)

## Prerequisites

Telemetry contract is integrated. Contract tests receive absolute pinned checkout paths.

## Red test

Name/path: `tests/opin-skill-creator/test_bundled_agents.py::test_four_agents_register_with_locked_effective_frontmatter`.

Command:

```bash
PI_SUBAGENTS_CHECKOUT=/absolute/pi-subagents uvx --from 'pytest==9.1.1' pytest -q tests/opin-skill-creator/test_bundled_agents.py::test_four_agents_register_with_locked_effective_frontmatter
```

Expected pre-fix failure: only three unfrontmattered files exist, analyzer roles are combined, and effective policies inherit caller defaults.

## Required behavior

Create exactly the C10 identities. Use snake_case pi-subagents frontmatter. Lock replacement prompt, no inherited conversation/skills, session/transcript policy, turn bounds, background policy, role model/thinking, and narrow tools proven sufficient. Grader input names the JSONL transcript/metrics contract, uses lowercase Pi tools, and expects neither `metrics.json` nor `user_notes.md`. Comparator stays blind. Model preflight proves each pin resolves in its profile; an unavailable pin fails rather than inheriting.

Pinned contract tests discover agents from a synthetic skill snapshot, verify bare and qualified dispatch including collision rewrite maps, prove caller `inherit_context: true` cannot override frontmatter, and inspect effective model resolution.

## Implementation steps

1. Add synthetic snapshot/model registry fixtures and observe failure.
2. Split analyzer content without role bleed and delete the old file.
3. Add explicit frontmatter from C10 and the report's target policies.
4. Correct grader vocabulary and telemetry inputs.
5. Add collision, isolation, blindness, and unavailable-model contract tests.

## Deterministic branch-tip gates

```bash
PI_CHECKOUT=/absolute/pi PI_SUBAGENTS_CHECKOUT=/absolute/pi-subagents uvx --from 'pytest==9.1.1' pytest -q tests/opin-skill-creator/test_bundled_agents.py
uvx --from 'pytest==9.1.1' pytest -q tests/opin-skill-creator -m 'not live'
git diff --check
```

## Live-test requirements

No model calls. Availability is tested with a deterministic registry fixture; OSC-14 performs real-provider calibration.

## Non-goals

Do not add or pin an executor agent, edit SKILL/benchmark prose, alter pi-subagents, or claim calibrated superiority.

## Structured handoff

Return: `order_id`, `status`, `branch`, `commit`, `red_observed`, `registered_agents`, `model_resolution_checked`, `collision_checked`, `tests_passed`, `tests_skipped`, `bounded_work`, `skipped_work`, `owned_paths_changed`, `summary`, `blockers`.

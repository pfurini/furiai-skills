# OSC-03: Ground the authoring doctrine on Pi

## Findings

Primary: F27 and F36d. Secondary consumer of F31 (OSC-05 later makes schemas directly reachable).

## Dependencies

None logically; the workflow runs it after OSC-00 so all branch tips share the same gate.

## Settled decisions restated

- The creator remains user-invoked and inline with `disable-model-invocation: true`; its description is a concise third-person human-facing summary, not imperative trigger prose.
- Pi-local references that must be read use `@${PI_SKILL_DIR}/...`. Doctrine covers Pi's current arguments, visibility, tool restrictions, model/effort, fork agent/background, paths, shell, hooks, and listing-cost behavior.
- Runtime code remains Python 3.10+ plus one plain-JavaScript benchmark workflow; this order adds no TypeScript, npm dependency, companion extension, or uncalibrated model claim.

## Exclusive owned paths

- `skills/opin-skill-creator/references/writing-principles.md`
- `skills/opin-skill-creator/SKILL.md`
- `tests/opin-skill-creator/test_authoring_doctrine.py`

## Read-only references

- Pi `docs/skills.md`, `core/skills/frontmatter.ts`, `render.ts`, and `runtime.ts`
- current testing/benchmarking/schema references
- report's measured negative doctrine result

## Prerequisites

Pinned Pi source is available. Preserve the creator as user-invoked and inline.

## Red test

Name/path: `tests/opin-skill-creator/test_authoring_doctrine.py::test_doctrine_exposes_pi_authoring_surface_and_resolvable_references`.

Command:

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/opin-skill-creator/test_authoring_doctrine.py::test_doctrine_exposes_pi_authoring_surface_and_resolvable_references
```

Expected pre-fix failure: required Pi fields, argument grammar, listing budget, fork choices, and `${PI_SKILL_DIR}` reference idiom are absent; the skill's own description is imperative.

## Required behavior

Teach Pi capabilities by failure class, not as an unmotivated field dump: `when_to_use`; named/positional arguments and hints; visibility; tool restrictions; model/effort; fork agent/background; paths; shell; hooks' parsed-but-not-executed status; listing cost; and resolvable skill-local references. Correct the doctrine's outdated claims about when-to-use placement and disclosure depth. Change the creator description to a third-person, concise human-facing summary without making it model-visible or forked.

Keep only capability-enabling guidance if later behavioral calibration ties; do not claim artifact lift from prose alone.

## Implementation steps

1. Add structural contract tests and observe failure.
2. Add a co-located Pi authoring section with exact current semantics.
3. Replace bare skill-local path idioms with `@${PI_SKILL_DIR}/...` where the agent must read a file.
4. Correct the creator description while preserving `disable-model-invocation: true`.
5. Verify all existing branch pointers remain one level deep.

## Deterministic branch-tip gates

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/opin-skill-creator/test_authoring_doctrine.py
uvx --from 'pytest==9.1.1' pytest -q tests/opin-skill-creator -m 'not live'
git diff --check
```

## Live-test requirements

None at this order. OSC-14 runs the snapshot A/B behavior test.

## Non-goals

Do not write sterilization/profile claims (OSC-11), benchmark workflow instructions (OSC-12), or pin the creator model before calibration.

## Structured handoff

Return: `order_id`, `status`, `branch`, `commit`, `red_observed`, `pi_fields_covered`, `references_checked`, `tests_passed`, `tests_skipped`, `bounded_work`, `skipped_work`, `owned_paths_changed`, `summary`, `blockers`.

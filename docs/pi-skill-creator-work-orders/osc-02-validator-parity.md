# OSC-02: Bring standalone validation into Pi parity

## Findings

Primary: F1 and F18.

## Dependencies

OSC-00.

## Settled decisions restated

- The runtime validator remains Python 3.10+ standard library code and carries a tested copy of Pi `0.84.4` frontmatter behavior; it does not import Pi, TypeScript, or maintainer checkouts at runtime.
- Both `disallowed-tools` and `disallowedTools` are accepted. Unknown-field handling, boolean/context normalization, BOM, multiline values, and loadability match the pinned Pi loader for the claimed subset.
- Missing, empty, or whitespace-only `name` or `description` fails validation. A supplied Pi checkout at any revision other than `a4043c1e332a61e4c8648b97b9b796c57f9db110` fails the differential contract test.

## Exclusive owned paths

- `skills/pi-skill-creator/scripts/quick_validate.py`
- `skills/pi-skill-creator/scripts/utils.py`
- `tests/pi-skill-creator/test_validator.py`
- `tests/pi-skill-creator/fixtures/validator/**`

## Read-only references

- `contracts.md`
- Pi `packages/coding-agent/src/core/skills/frontmatter.ts`, loader exports, and `docs/skills.md` at the pinned revision
- `references/schemas.md` (OSC-05 owns it)

## Prerequisites

OSC-00 is integrated. `PI_CHECKOUT` is optional for offline tests and mandatory for the contract tier.

## Red test

Name/path: `tests/pi-skill-creator/test_validator.py::test_accepts_current_pi_frontmatter_and_rejects_empty_required_fields`.

Command:

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator/test_validator.py::test_accepts_current_pi_frontmatter_and_rejects_empty_required_fields
```

Expected pre-fix failure: valid current Pi keys are rejected, while empty name/description fixtures pass.

## Required behavior

Support Pi's pinned frontmatter contract, including both disallowed-tool spellings and unknown-field preservation/diagnostics consistent with Pi's lenient loader. Match boolean normalization, context normalization, name/description rules, BOM, multiline values, and JSON-safe behavior for the claimed subset. Missing, empty, and whitespace-only name/description always fail the standalone final gate.

The differential test runs every fixture through the Python validator and Pi's exported `loadSkillsFromDir()` and compares loadability. It prints the reconciled Pi revision as test output. Missing checkout skips clearly; a supplied checkout at the wrong revision fails.

## Implementation steps

1. Add focused valid/invalid fixtures and observe the red test.
2. Refactor parsing only as needed to match the pinned contract.
3. Implement unconditional required-field checks and current fields.
4. Add a small Node oracle fixture under the project test tree, not the skill.
5. Run the complete fixture corpus through both implementations.

## Deterministic branch-tip gates

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator/test_validator.py -m 'not contract'
PI_CHECKOUT=/absolute/pi PI_SUBAGENTS_CHECKOUT=/absolute/pi-subagents uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator/test_validator.py -m contract
uvx --from 'ty==0.0.77' ty check skills/pi-skill-creator/scripts/quick_validate.py skills/pi-skill-creator/scripts/utils.py
git diff --check
```

## Live-test requirements

None.

## Non-goals

Do not port the validator to TypeScript, import Pi at runtime, make the skill an npm package, or edit schemas/docs owned by another order.

## Structured handoff

Return: `order_id`, `status`, `branch`, `commit`, `red_observed`, `pi_revision_verified`, `fixture_count`, `differential_result`, `tests_passed`, `tests_skipped`, `bounded_work`, `skipped_work`, `owned_paths_changed`, `summary`, `blockers`.

# OSC-13: Correct deterministic README guidance

## Findings

Primary: F24 and F36e. Secondary consumer of F9/F19/F26/F27/F33-F37.

## Dependencies

OSC-12.

## Settled decisions restated

- Because the creator remains hidden from model-facing surfaces, every working example invokes `/opin-skill-creator` or `/skill:opin-skill-creator`; prose naming alone cannot invoke it.
- Runtime requirements are Python 3.10+ standard library plus one plain-JavaScript workflow. Pi/pi-subagents are optional feature dependencies supplied through absolute paths, not npm or TypeScript dependencies bundled into the skill.
- Distribution is a byte-for-byte copy of `skills/opin-skill-creator/`. Existing Claude Code measurements remain explicitly historical, and no Pi-native numeric claim or permanent model pin is added before approved calibration and human review.

## Exclusive owned paths

- `skills/opin-skill-creator/README.md`
- `tests/opin-skill-creator/test_readme.py`

## Read-only references

- all integrated runtime behavior and tests
- Pi invocation/visibility docs
- historical campaign records referenced by the README

## Prerequisites

Runtime behavior and benchmark prose are integrated. Historical Claude Code measurements remain historical and are not rewritten as Pi results.

## Red test

Name/path: `tests/opin-skill-creator/test_readme.py::test_readme_invocations_resolve_and_runtime_requirements_are_truthful`.

Command:

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/opin-skill-creator/test_readme.py::test_readme_invocations_resolve_and_runtime_requirements_are_truthful
```

Expected pre-fix failure: examples name a model-hidden skill in prose instead of invoking it, Python 3.10+ is unstated, and caveats describe obsolete clean-slate/archive-era behavior.

## Required behavior

Use `/opin-skill-creator` or `/skill:opin-skill-creator` in every good-usage example and explain that prose naming cannot reach a model-hidden skill. State Python 3.10+ standard library and the optional Pi/pi-subagents requirements by feature. Explain copied-directory distribution. Distinguish all inherited Claude Code evidence from uncalibrated Pi guidance. Remove stale caveats superseded by implemented profiles/RPC tests, but do not add model claims or numbers before OSC-14.

## Implementation steps

1. Add invocation/product/dependency/distribution/claim-origin tests and observe failure.
2. Correct examples and user-invoked explanation.
3. State runtime floors and optional dependencies.
4. Reconcile layout/caveats with the implemented copied directory and workflows.
5. Preserve historical numbers with explicit provenance.

## Deterministic branch-tip gates

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/opin-skill-creator/test_readme.py
uvx --from 'pytest==9.1.1' pytest -q tests/opin-skill-creator -m 'not live'
git diff --check
```

## Live-test requirements

None. Actual command firing is covered in OSC-14/15 where Pi is available.

## Non-goals

Do not calibrate models, publish new numeric claims, or alter runtime code.

## Structured handoff

Return: `order_id`, `status`, `branch`, `commit`, `red_observed`, `invocation_forms`, `python_floor`, `historical_claims_labeled`, `tests_passed`, `tests_skipped`, `bounded_work`, `skipped_work`, `owned_paths_changed`, `summary`, `blockers`.

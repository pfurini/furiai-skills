# OSC-09: Correct description optimization and report behavior

## Findings

Primary: F9, F10, F11, F36b, and F36c. Secondary consumer of F4/F6/F23/F36f.

## Dependencies

OSC-03, OSC-07, and OSC-08.

## Settled decisions restated

- A skill hidden from model invocation skips trigger optimization and receives human-readability validation instead. Optimizer prose comes from the same third-person, capability-first doctrine as `references/writing-principles.md`.
- Data is partitioned deterministically into `trigger/train.json`, `trigger/validation.json`, and `trigger/final-test.json`; selection uses train/validation only, and final-test runs exactly once after selection without feeding results back to the optimizer.
- Empty history produces the test-frozen useful empty result or bounded input error, never raw `ValueError`. Persistent runs use explicit `--report none --results-dir <campaign-path>` and do not open a browser unexpectedly.

## Exclusive owned paths

- `skills/opin-skill-creator/scripts/run_loop.py`
- `skills/opin-skill-creator/scripts/improve_description.py`
- `skills/opin-skill-creator/scripts/generate_report.py`
- `tests/opin-skill-creator/test_optimizer.py`
- `tests/opin-skill-creator/fixtures/optimizer/**`

## Read-only references

- `references/writing-principles.md` as the canonical doctrine
- role/trigger contracts and campaign schemas
- `references/benchmarking.md` (OSC-12 owns the command text)

## Prerequisites

Reliable trigger statuses and role-specific model plumbing are integrated.

## Red test

Name/path: `tests/opin-skill-creator/test_optimizer.py::test_hidden_skill_skips_and_final_test_runs_once_after_selection`.

Command:

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/opin-skill-creator/test_optimizer.py::test_hidden_skill_skips_and_final_test_runs_once_after_selection
```

Expected pre-fix failure: hidden skills are optimized, the test partition runs every iteration and selects the winner, and the optimizer prompt requires imperative phrasing.

A second required red test is `test_generate_report_empty_history_does_not_raise_value_error`; pre-fix it raises `ValueError` from `max([])`.

## Required behavior

Skip trigger optimization when effective model visibility is disabled and return a clear human-readability validation result. Use deterministic stratified train/validation/final-test partitions; validate minimum class sizes; iterate/select on train/validation only; run final-test exactly once after selection; never expose final-test outcomes to the optimizer. Deterministically break ties. Generate the optimizer prompt from one small canonical capability-first rule source consistent with `writing-principles.md`.

`generate_report.py` handles empty history deliberately (valid empty report or bounded user-facing input error, as frozen by its test) and never raises raw `ValueError`. CLI defaults do not open a browser or discard records unexpectedly; persistence is explicit and OSC-12 documents `--report none --results-dir <campaign-path>`.

## Implementation steps

1. Add hidden-skill, class-size, partition-count, tie, doctrine, empty-history, and persistence tests.
2. Observe both named failures.
3. Implement visibility gate and three-way deterministic partitioning.
4. Separate candidate selection from the one final-test call.
5. Replace contradictory prompt text with canonical doctrine input.
6. Fix empty-history/report defaults and preserve every candidate transcript/result.

## Deterministic branch-tip gates

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/opin-skill-creator/test_optimizer.py
uvx --from 'ty==0.0.77' ty check skills/opin-skill-creator/scripts/run_loop.py skills/opin-skill-creator/scripts/improve_description.py skills/opin-skill-creator/scripts/generate_report.py
git diff --check
```

## Live-test requirements

None. OSC-14 runs the final live methodology.

## Non-goals

Do not edit canonical doctrine or benchmark prose, choose models, or make final-test data visible during iteration.

## Structured handoff

Return: `order_id`, `status`, `branch`, `commit`, `red_observed`, `partition_counts`, `final_test_call_count`, `empty_history_behavior`, `tests_passed`, `tests_skipped`, `bounded_work`, `skipped_work`, `owned_paths_changed`, `summary`, `blockers`.

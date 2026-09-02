# OSC-05: Correct benchmark aggregation and machine schemas

## Findings

Primary: F2, F3, F17, F21, F29, F31, and F36a. Secondary consumer of F25a/F25b/F28 through OSC-01.

## Dependencies

OSC-00 and OSC-01.

## Settled decisions restated

- The campaign tree is `<project-root>/.skill-creator/<skill-name>/campaign-<campaign-id>/iteration-N/<eval-name>/{with_skill,without_skill}/run-N/`; eval and campaign ids use the frozen lowercase alphanumeric/hyphen patterns.
- Treatment is `with_skill`, control is `without_skill`, and delta is always `with_skill - without_skill`, independent of discovery order. The graded JSON key is only `expectations`.
- Zero runs, a missing arm/repetition, unexpected configuration, mixed profile, unresolved/mixed effective model outside a pre-registered comparison, malformed metadata, or placeholder data is fatal and writes no benchmark artifact. Provider usage and fields ending in `_chars` remain distinct.

## Exclusive owned paths

- `skills/opin-skill-creator/scripts/aggregate_benchmark.py`
- `skills/opin-skill-creator/references/schemas.md`
- `tests/opin-skill-creator/test_aggregation.py`
- `tests/opin-skill-creator/fixtures/aggregation/**`

## Read-only references

- `contracts.md` C3-C8
- `scripts/transcript_metrics.py`
- viewer configuration/badge contract
- `SKILL.md` (OSC-03 owns the earlier direct pointer; OSC-12 may integrate it later)

## Prerequisites

Telemetry parser contract tests pass. Do not edit `references/benchmarking.md`; OSC-12 is its sole owner.

## Red test

Name/path: `tests/opin-skill-creator/test_aggregation.py::test_documented_workspace_aggregates_treatment_minus_control_with_real_metadata`.

Command:

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/opin-skill-creator/test_aggregation.py::test_documented_workspace_aggregates_treatment_minus_control_with_real_metadata
```

Expected pre-fix failure: descriptive eval directories are not found; a no-data benchmark exits zero, metadata uses placeholders/hardcoded repetitions, and treatment 1.00 minus control 0.25 may be reported as `-0.75`.

## Required behavior

Implement the exact C3 tree and only `with_skill`/`without_skill`. Read and validate `campaign.json`, every expected eval/arm/repetition, `run.json`, `grading.json`, and transcript metrics. Refuse no data, partial/mixed profile/model metadata, duplicate runs, missing expectations, or malformed fields before writing output. Delta is always treatment minus control. Derive repetitions and eval set from records. Preserve `eval_name`. Keep output characters and provider usage distinct. JSON and Markdown derive from the same typed summary.

Update schemas to the frozen workspace/campaign/run/metrics/grading/benchmark contracts, remove orphaned improve-mode history, use `expectations`, and locate benchmark artifacts under `iteration-N`.

## Implementation steps

1. Add complete, partial, no-data, reversed-order, mixed-profile, and mixed-model fixtures.
2. Observe the focused failure.
3. Separate discovery/validation from aggregation so invalid input writes nothing.
4. Make treatment/control explicit constants and calculate directed deltas.
5. Integrate OSC-01 metrics and carry eval metadata.
6. Rewrite schemas to match executable behavior exactly.
7. Resolve existing type diagnostics rather than suppressing them.

## Deterministic branch-tip gates

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/opin-skill-creator/test_aggregation.py
uvx --from 'ty==0.0.77' ty check skills/opin-skill-creator/scripts/aggregate_benchmark.py
git diff --check
```

## Live-test requirements

None.

## Non-goals

Do not generate missing run metadata, accept legacy configuration aliases, edit benchmark prose/viewer, or fall back from tokens to characters.

## Structured handoff

Return: `order_id`, `status`, `branch`, `commit`, `red_observed`, `fixtures_validated`, `no_data_exit`, `delta_observed`, `tests_passed`, `tests_skipped`, `bounded_work`, `skipped_work`, `owned_paths_changed`, `summary`, `blockers`.

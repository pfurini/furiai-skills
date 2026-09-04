# OSC-07: Introduce role-specific model configuration

## Findings

Primary: F4. Secondary consumer of F3 and the requested/effective metadata contract.

## Dependencies

OSC-05. Old WP5 must complete before OSC-08 (old WP6).

## Settled decisions restated

- Trigger-consumer and optimizer model/thinking inputs are distinct and mandatory for quantitative execution; the ambiguous `--model` alias is removed rather than retained for compatibility.
- Requested and effective model/thinking fields remain separate. Effective values come from Pi events or pi-subagents invocation records and are never copied from requested values; unresolved or absent effective values invalidate the run.
- Environment-provided defaults are allowed only when explicit and recorded in campaign metadata. This order fixes the final known baseline type diagnostic in `run_loop.py`, after OSC-05 fixes the six in `aggregate_benchmark.py`, so the full scripts/viewer `ty` gate becomes mandatory here.

## Exclusive owned paths

- `skills/pi-skill-creator/scripts/run_eval.py`
- `skills/pi-skill-creator/scripts/run_loop.py`
- `skills/pi-skill-creator/scripts/improve_description.py`
- `tests/pi-skill-creator/test_model_configuration.py`

## Read-only references

- `contracts.md` C5-C7
- campaign schemas owned by OSC-05
- pinned Pi model docs and pi-subagents model resolver

## Prerequisites

Aggregation/campaign schemas are integrated. Begin from their exact metadata names.

## Red test

Name/path: `tests/pi-skill-creator/test_model_configuration.py::test_trigger_consumer_and_optimizer_have_distinct_requested_effective_models`.

Command:

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator/test_model_configuration.py::test_trigger_consumer_and_optimizer_have_distinct_requested_effective_models
```

Expected pre-fix failure: one `--model` value is sent to both trigger evaluation and description generation, no thinking is explicit, and no effective values are recorded.

## Required behavior

Expose distinct trigger-consumer and optimizer model/thinking inputs. Quantitative execution rejects missing role choices before any subprocess/model call. Requested and effective values remain separate. Environment variables may provide explicit defaults only when captured in metadata. Standalone subprocess execution never claims to inherit the caller session. Do not retain an ambiguous `--model` compatibility alias.

This order changes interfaces only; OSC-08 handles trigger status/cwd/name/query correctness, and OSC-09 handles methodology/prompt behavior.

## Implementation steps

1. Add subprocess fakes and observe role conflation.
2. Define one role configuration object/CLI mapping shared by the three modules.
3. Plumb trigger model/thinking only to evaluation and optimizer model/thinking only to improvement.
4. Capture requested/effective fields without fabricating resolution.
5. Fail before subprocess launch when mandatory quantitative values are absent.

## Deterministic branch-tip gates

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator/test_model_configuration.py
uvx --from 'ty==0.0.77' ty check skills/pi-skill-creator/scripts/run_eval.py skills/pi-skill-creator/scripts/run_loop.py skills/pi-skill-creator/scripts/improve_description.py
git diff --check
```

## Live-test requirements

None; subprocesses/models are faked.

## Non-goals

Do not fix trigger classification, data partitions, doctrine wording, RPC execution, or choose permanent models.

## Structured handoff

Return: `order_id`, `status`, `branch`, `commit`, `red_observed`, `roles_configured`, `deprecated_flags`, `preflight_failures_tested`, `tests_passed`, `tests_skipped`, `bounded_work`, `skipped_work`, `owned_paths_changed`, `summary`, `blockers`.

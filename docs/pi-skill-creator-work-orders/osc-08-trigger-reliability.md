# OSC-08: Make trigger evaluation reliable

## Findings

Primary: F5, F6, F23, and F36f. Secondary consumer of F4.

## Dependencies

OSC-07. This ordering enforces old WP5 before old WP6.

## Settled decisions restated

- Trigger status is exactly `triggered`, `not_triggered`, `timeout`, `process_error`, `model_error`, `auth_error`, or `invalid_output`; only the first two enter accuracy, and every infrastructure status invalidates the campaign.
- The retry bound is one retry, only for rate-limit or explicitly transient provider errors. Worker exceptions become `process_error`, never `not_triggered`.
- Trigger measurement uses the `in-situ` profile, preserves the real skill name and explicit evaluation cwd/competing set, and sends queries through stdin or a protocol-safe channel so leading `@` and `-` remain data.

## Exclusive owned paths

- `skills/pi-skill-creator/scripts/run_eval.py`
- `tests/pi-skill-creator/test_trigger_evaluation.py`
- `tests/pi-skill-creator/fixtures/trigger/**`

## Read-only references

- `contracts.md` C5-C7
- current role configuration from OSC-07
- Pi JSON event docs, CLI args, skill listing behavior, and real tool event shape

## Prerequisites

Role-specific interfaces are integrated and green.

## Red test

Name/path: `tests/pi-skill-creator/test_trigger_evaluation.py::test_real_name_explicit_cwd_and_infrastructure_status_are_preserved`.

Command:

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator/test_trigger_evaluation.py::test_real_name_explicit_cwd_and_infrastructure_status_are_preserved
```

Expected pre-fix failure: skill name is randomized, cwd is the creator directory, stderr/exit status disappear, and timeouts/errors become `False`.

## Required behavior

Implement C6 exactly. Preserve the real skill name while isolating discovery from any installed duplicate. Require and record the evaluation cwd and competing set. Capture bounded stderr, exit code, complete authoritative events, model/thinking, profile, Pi revision, attempts, and invocation mechanism. Only valid trigger/non-trigger responses enter accuracy. Retry at most once and only explicitly transient provider/rate errors. Send the prompt through stdin or a protocol-safe channel so leading `@` and `-` are data, not CLI options. Use deterministic temporary paths.

## Implementation steps

1. Add fixtures for every trigger status, duplicate target, real listing name, alternate cwd, malformed JSON, and leading punctuation.
2. Observe the focused failure.
3. Replace boolean worker output with the closed status record.
4. Separate module cwd from evaluation cwd and control skill discovery.
5. Implement bounded retry/classification and fail campaign summaries on infrastructure statuses.
6. Prove no query follows `-p` in argv.

## Deterministic branch-tip gates

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator/test_trigger_evaluation.py
uvx --from 'ty==0.0.77' ty check skills/pi-skill-creator/scripts/run_eval.py
git diff --check
```

## Live-test requirements

None in this order. OSC-14 exercises real trigger models in-situ.

## Non-goals

Do not alter optimizer partitions/prompt, use print/JSON for fork fidelity, or edit benchmark prose.

## Structured handoff

Return: `order_id`, `status`, `branch`, `commit`, `red_observed`, `statuses_tested`, `retry_policy`, `query_transport`, `tests_passed`, `tests_skipped`, `bounded_work`, `skipped_work`, `owned_paths_changed`, `summary`, `blockers`.

# OSC-01: Freeze telemetry and implement the transcript parser

## Findings

Primary: F25b, F28, F35b. Secondary consumer of F25a. This order corrects the report's unsupported assumption: pi-subagents `.output` files contain message snapshots, not `tool_execution_start` lifecycle records, and workflow-owned children expose neither top-level lifecycle events nor a transcript path.

## Dependencies

OSC-00.

## Settled decisions restated

- `scripts/transcript_metrics.py` accepts exactly `pi-subagents-output-v1` and `pi-json-events-v3` and emits `pi-skill-creator.transcript-metrics/v1`; malformed or incomplete JSONL is fatal, writes no output, and is never skipped with a warning.
- Top-level `Agent` results expose `.output` JSONL message snapshots. `SubagentWorkflow.agent()` children expose neither that transcript path nor top-level lifecycle events, so workflow-child cost or per-child transcripts are never claimed.
- Tool names are lowercase Pi names. Authoritative completed assistant messages provide usage/effective models; cumulative message updates are ignored, and absent effective model or usage invalidates a completed measured run.

## Exclusive owned paths

- `skills/pi-skill-creator/scripts/transcript_metrics.py`
- `tests/pi-skill-creator/test_transcript_metrics.py`
- `tests/pi-skill-creator/fixtures/transcripts/**`

## Read-only references

- `contracts.md` C8
- pi-subagents `src/output-file.ts`, `src/workflow/host.ts`, `src/workflow/runtime.ts`, `src/workflow/worker-source.ts`, `docs/workflows.md`, and `docs/rpc.md` at the pinned revision
- Pi `packages/ai/src/types.ts` and `packages/coding-agent/docs/json.md`
- current `agents/grader.md`, `references/schemas.md`, and `scripts/aggregate_benchmark.py`

## Prerequisites

Both pinned source checkouts are available for contract tests. Use synthetic transcript fixtures for offline tests.

## Red test

Name/path: `tests/pi-skill-creator/test_transcript_metrics.py::test_pi_subagents_output_metrics_are_derived_from_messages`.

Command:

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator/test_transcript_metrics.py::test_pi_subagents_output_metrics_are_derived_from_messages
```

Expected pre-fix failure: `scripts.transcript_metrics` does not exist; no producer can supply trustworthy `execution_metrics`.

## Required behavior

Implement C8 exactly for both `pi-subagents-output-v1` and `pi-json-events-v3`. Tool calls in `.output` come from assistant `toolCall` content. RPC tool calls come from lifecycle events. Usage is summed only from authoritative completed assistant messages; cumulative update usage is ignored. Malformed JSONL, absent effective model/usage, invalid numeric fields, unknown formats, and non-lowercase tool names fail closed.

Add a pinned-source contract test that proves `SubagentWorkflow.agent()` returns final text/structured output, workflow host results carry no transcript path, and workflow children are excluded from top-level lifecycle events. This test protects the architectural boundary that OSC-05, OSC-06, OSC-10, and OSC-12 consume.

## Implementation steps

1. Capture minimal sanitized fixtures matching both pinned wire formats.
2. Add the failing parser tests.
3. Implement strict LF-only JSONL parsing, source-specific event extraction, usage summation, and CLI exit semantics.
4. Add no-double-count regression fixtures containing both message updates and message ends.
5. Add source contract assertions against the pinned pi-subagents checkout.
6. Prove CLI output is deterministic and ends with one LF.

## Deterministic branch-tip gates

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator/test_transcript_metrics.py
PI_CHECKOUT=/absolute/pi PI_SUBAGENTS_CHECKOUT=/absolute/pi-subagents uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator/test_transcript_metrics.py -m contract
uvx --from 'ty==0.0.77' ty check skills/pi-skill-creator/scripts/transcript_metrics.py
git diff --check
```

## Live-test requirements

None. A real sanitized `.output` may be used as local evidence but is not committed if it contains user data.

## Non-goals

Do not add an executor agent, change pi-subagents, expose workflow internals, parse self-reported `metrics.json`, or write aggregation/grader behavior.

## Structured handoff

Return: `order_id`, `status`, `branch`, `commit`, `red_observed`, `source_contract_verified`, `formats_supported`, `tests_passed`, `tests_skipped`, `bounded_work`, `skipped_work`, `owned_paths_changed`, `summary`, `blockers`.

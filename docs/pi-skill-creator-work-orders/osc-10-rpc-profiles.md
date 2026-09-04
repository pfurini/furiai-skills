# OSC-10: Add RPC behavioral execution and environment profiles

## Findings

Primary: F7, F8, F33, F34, and F37. Secondary evidence producer for F26 and consumer of F4/F20/F27/F28.

## Dependencies

OSC-01, OSC-03, and OSC-07. The authoring half of old WP13 therefore precedes old WP8. Telemetry is frozen before this order.

## Settled decisions restated

- The only profiles are `in-situ`, `hermetic-core`, and `declared-dependencies`; different profiles are never aggregated. `hermetic-core` uses replacement prompt, no inherited context, isolation, built-in tools only, and a worktree when writing.
- Fork/dependency execution uses the supplied absolute Pi executable in `--mode rpc --no-session`. `declared-dependencies` loads only declared absolute dependencies, including pi-subagents through `-e <pi-subagents>/src/index.ts`; no SDK package or managed-policy tier is added.
- RPC requests travel as JSON on stdin, preserve fork behavior, and emit `pi-skill-creator.run/v1`, `transcript.jsonl`, and `pi-skill-creator.transcript-metrics/v1`. Timeout, UI dialog, protocol, model-resolution, profile, or process failures never produce a completed run.

## Exclusive owned paths

- `skills/pi-skill-creator/scripts/rpc_runner.py`
- `tests/pi-skill-creator/test_rpc_runner.py`
- `tests/pi-skill-creator/fixtures/rpc/**`

## Read-only references

- `contracts.md` C7-C9
- Pi `docs/rpc.md`, RPC types/mode, CLI args, `_shouldDegradeFork()`, `_extensionMode`, and `bindExtensions()` at the pinned revision
- pi-subagents protocol v3 and skill-agent sources
- `references/testing.md` and `references/benchmarking.md` (OSC-11/12 own prose)

## Prerequisites

Absolute Pi executable/checkouts and pi-subagents checkout inputs are available to contract tests. No SDK package is installed.

## Red test

Name/path: `tests/pi-skill-creator/test_rpc_runner.py::test_rpc_preserves_fork_mode_and_captures_effective_telemetry`.

Command:

```bash
PI_EXECUTABLE=/absolute/pi-executable PI_CHECKOUT=/absolute/pi PI_SUBAGENTS_CHECKOUT=/absolute/pi-subagents uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator/test_rpc_runner.py::test_rpc_preserves_fork_mode_and_captures_effective_telemetry
```

Expected pre-fix failure: no RPC runner exists; the existing print/JSON path cannot prove fork execution or declared dependency loading.

## Required behavior

Implement C9 and all three C7 profiles. Use strict LF JSONL, request ids, process-group timeout, bounded stderr, authoritative final messages, effective model/thinking, diagnostics, tool events, and full usage/cost. Load pi-subagents explicitly with an absolute `-e` path in `declared-dependencies`; unrelated extensions remain absent. Prove RPC mode preserves fork while print/JSON degrades. Prove `--skill` remains loaded under `--no-skills`, is model-visible rather than manually inert, and remove any managed-policy concept from generated guidance evidence.

The contract test measures an isolated subagent's context/tool/resource visibility. OSC-11 writes the prose only after this evidence passes.

## Implementation steps

1. Add protocol fixtures including U+2028/U+2029 inside JSON strings, ids, errors, UI requests, and effective model fields.
2. Observe missing-runner failure.
3. Implement subprocess framing/state machine and durable run outputs.
4. Add profile command construction with explicit absolute inputs.
5. Run local no-credential fork/dependency fixtures or deterministic fake processes; mark credential/model execution live.
6. Assert no TypeScript SDK/runtime dependency is added.

## Deterministic branch-tip gates

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator/test_rpc_runner.py -m 'not live'
PI_EXECUTABLE=/absolute/pi-executable PI_CHECKOUT=/absolute/pi PI_SUBAGENTS_CHECKOUT=/absolute/pi-subagents uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator/test_rpc_runner.py -m contract
uvx --from 'ty==0.0.77' ty check skills/pi-skill-creator/scripts/rpc_runner.py
git diff --check
```

## Live-test requirements

Credentialed inline/fork/bundled-agent executions are marked `live` and deferred to OSC-14. Deterministic protocol/profile construction must pass without credentials.

## Non-goals

Do not use the SDK, edit Pi/pi-subagents, claim workflow-child transcript access, or write testing/benchmark prose.

## Structured handoff

Return: `order_id`, `status`, `branch`, `commit`, `red_observed`, `rpc_modes_verified`, `profiles_verified`, `protocol_v3_checked`, `tests_passed`, `tests_skipped`, `bounded_work`, `skipped_work`, `owned_paths_changed`, `summary`, `blockers`.

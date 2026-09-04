# OSC-11: Rewrite testing doctrine from measured Pi behavior

## Findings

Primary: F26 and F35a. Secondary consumer of F7/F8/F14/F25b/F27/F35b/F37.

## Dependencies

OSC-03 and OSC-10. This is the sterilization half of old WP13 and must follow RPC/profile evidence.

## Settled decisions restated

- Testing doctrine names exactly `in-situ`, `hermetic-core`, and `declared-dependencies`; profile mismatch is fatal, and worktree isolation is used for parallel writers.
- Direct `Agent` is for a known small qualitative set; `SubagentWorkflow` is for dynamic or staged fan-out. Multi-agent execution always requires explicit user approval before the tool call.
- Top-level `Agent` `.output` is JSONL message-snapshot evidence. Workflow children expose no such path or top-level lifecycle events; measured direct runs use that supported seam, while fork/dependency runs use RPC records and never substitute launcher telemetry.

## Exclusive owned paths

- `skills/pi-skill-creator/references/testing.md`
- `skills/pi-skill-creator/SKILL.md`
- `tests/pi-skill-creator/test_testing_doctrine.py`

## Read-only references

- `contracts.md` C7-C11
- passing OSC-01 telemetry seam and OSC-10 profile tests
- pinned pi-subagents Agent/Workflow docs and source
- `references/benchmarking.md` (OSC-12 owns quantitative prose)

## Prerequisites

OSC-10's isolated-subagent contract test passes. Do not write beyond that evidence.

## Red test

Name/path: `tests/pi-skill-creator/test_testing_doctrine.py::test_testing_names_supported_mechanisms_and_profiles`.

Command:

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator/test_testing_doctrine.py::test_testing_names_supported_mechanisms_and_profiles
```

Expected pre-fix failure: prose says subagents cannot be sterilized, uses a two-profile split, and does not name Agent/SubagentWorkflow, context fields, transcript format/path boundary, or completion metadata.

## Required behavior

Teach the exact three profiles and when each applies. Name direct `Agent` calls for known small qualitative sets, `SubagentWorkflow` for dynamic/staged fan-out, `prompt_mode: replace`, `inherit_context: false`, `isolated: true`, and worktree isolation for parallel writers. State that top-level Agent `.output` paths are returned by results/notifications and contain JSONL message snapshots; workflow children do not expose that path or top-level lifecycle events. Direct measured runs and RPC measured runs follow C8. Name `total_tokens`/`duration_ms` notification capture without claiming it is the only recoverable usage source.

Preserve explicit user approval before multi-agent execution. Use the C3 workspace tree and terminology, but leave quantitative command detail to OSC-12.

## Implementation steps

1. Add exact-mechanism/profile/negative-claim tests and observe failure.
2. Delete the false sterilization sentence rather than qualifying it.
3. Rewrite environment fidelity around the three profiles.
4. Wire supported Agent/Workflow/telemetry mechanisms into baseline and forward-test steps.
5. Update SKILL pointers/steps where the mechanism must be visible without nested lookup.

## Deterministic branch-tip gates

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator/test_testing_doctrine.py
uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator -m 'not live'
git diff --check
```

## Live-test requirements

None; it consumes OSC-10 evidence. OSC-14 behaviorally checks the doctrine.

## Non-goals

Do not edit benchmark prose, runtime workflow, agent definitions, or invent workflow-child telemetry.

## Structured handoff

Return: `order_id`, `status`, `branch`, `commit`, `red_observed`, `profiles_documented`, `mechanisms_documented`, `unsupported_claims_removed`, `tests_passed`, `tests_skipped`, `bounded_work`, `skipped_work`, `owned_paths_changed`, `summary`, `blockers`.

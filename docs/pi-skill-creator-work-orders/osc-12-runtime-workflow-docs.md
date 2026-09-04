# OSC-12: Add the deterministic runtime benchmark workflow and converge benchmark prose

## Findings

No new primary finding. This integration unit is the sole secondary consumer that converges F2-F8, F12-F14, F17, F20-F21, F25-F29, F31-F35, F36a/F36c, and F37 into one executable runtime path.

## Dependencies

OSC-05, OSC-06, OSC-07, OSC-09, OSC-10, and OSC-11.

## Settled decisions restated

- `skills/pi-skill-creator/workflows/benchmark.js` is plain JavaScript runtime machinery, separate from both repository-development workflows. It requires `approved: true`, caller-supplied deterministic campaign id/time, absolute paths, profile, evals, repetitions, and role model/thinking values.
- Execution-to-grading uses `pipeline()`; only true all-results synthesis uses `parallel()`. Null schema/gate results, failed/skipped/unreported work, or any missing eval/arm/repetition makes the campaign invalid rather than filtering work away.
- The only arms are `with_skill` and `without_skill`, delta is `with_skill - without_skill`, and claims never mix `in-situ`, `hermetic-core`, or `declared-dependencies`. RPC executor telemetry stays distinct from launcher overhead; `workflow_output_tokens` is reported while per-launcher cost is unavailable.

## Exclusive owned paths

- `skills/pi-skill-creator/workflows/benchmark.js`
- `skills/pi-skill-creator/references/benchmarking.md`
- `skills/pi-skill-creator/SKILL.md`
- `tests/pi-skill-creator/test_runtime_workflow.py`
- `tests/pi-skill-creator/fixtures/workflow/**`

## Read-only references

- all frozen contracts and integrated scripts/agents/schemas/testing doctrine
- pinned pi-subagents workflow docs, meta parser, runtime, worker, host, and example tests

## Prerequisites

All dependencies pass the full deterministic gate. The runtime workflow is plain JavaScript and has no filesystem/network/module access itself.

## Red test

Name/path: `tests/pi-skill-creator/test_runtime_workflow.py::test_runtime_workflow_fails_closed_and_pipelines_execution_into_grading`.

Command:

```bash
PI_SUBAGENTS_CHECKOUT=/absolute/pi-subagents uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator/test_runtime_workflow.py::test_runtime_workflow_fails_closed_and_pipelines_execution_into_grading
```

Expected pre-fix failure: `workflows/benchmark.js` does not exist and benchmark prose describes incompatible layout, grading, profiles, commands, and telemetry.

## Required behavior

Implement C11 with a pure-literal `meta`, explicit approval and absolute args, deterministic ids/timestamps supplied through args, bounded fan-out, execution-to-grading `pipeline`, small schemas, deterministic gates, and explicit accounting of completed/failed/skipped/bounded/null work. For transcript-backed fork/dependency campaigns, launcher agents invoke the RPC runner; workflow-child telemetry is never mislabeled as executor telemetry. Return durable paths, validity, status counts, effective role metadata, and `workflow_output_tokens`; mark per-launcher cost unavailable.

Rewrite benchmarking prose as the single owner: exact C3 tree; `expectations`; only two configurations; explicit roles/models/thinking/profiles; top-level Agent versus RPC/workflow telemetry boundary; explicit user approval; grader/comparator/analyzer identities; safe viewer PID flow; optimizer command with persistence and no surprise browser; no nonexistent policy tier or false `--skill` claim. Link schemas directly from SKILL and name the absolute `SubagentWorkflow.scriptPath` derived from `${PI_SKILL_DIR}`.

## Implementation steps

1. Add meta/stub-host/null/gate/resume/determinism/accounting tests and observe failure.
2. Write the plain-JS workflow from integrated contracts.
3. Parse and execute it through pinned pi-subagents source with fake host results.
4. Rewrite benchmark prose and SKILL integration from actual interfaces.
5. Search runtime files for stale identifiers, unsupported telemetry claims, and surprise command defaults.

## Deterministic branch-tip gates

```bash
PI_CHECKOUT=/absolute/pi PI_SUBAGENTS_CHECKOUT=/absolute/pi-subagents uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator/test_runtime_workflow.py
uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator -m 'not live'
uvx --from 'ty==0.0.77' ty check skills/pi-skill-creator/scripts skills/pi-skill-creator/eval-viewer
git diff --check
```

## Live-test requirements

None at branch tip. OSC-14 runs a bounded approved example campaign.

## Non-goals

Do not make the workflow discoverable by saved-workflow name, run it without approval, add TypeScript/npm, or treat it as the repository adoption workflow.

## Structured handoff

Return: `order_id`, `status`, `branch`, `commit`, `red_observed`, `meta_parsed`, `stub_execution`, `null_gate_cases`, `benchmark_contracts_converged`, `tests_passed`, `tests_skipped`, `bounded_work`, `skipped_work`, `owned_paths_changed`, `summary`, `blockers`.

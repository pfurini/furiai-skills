# OSC-00: Establish a passing harness test foundation

## Findings

Primary: F15. Secondary coverage scaffold for every later finding. F19 remains resolved and is not implemented here.

## Dependencies

None. This is the first integrated implementation order.

## Settled decisions restated

- Source baseline `0b9e86bc77a60fb34039456a6624ea94e396f5d1` only freezes the F19 removal and pre-implementation skill state; adoption never starts from that SHA. The caller-supplied full `implementationStartCommit` is the later clean current `HEAD` containing the finalized handoff, and every isolated implementation worktree branches from it. Contract tests use Pi `0.84.4` at `a4043c1e332a61e4c8648b97b9b796c57f9db110` and pi-subagents `0.19.0` at `bfa262fdd75d807b1c6b1f852f1f1bea2bbb3fa4`, supplied by absolute paths.
- Project tests and fixtures live under `tests/pi-skill-creator/`, never under the copied runtime directory `skills/pi-skill-creator/`. Offline tests use no network, credentials, model calls, or runtime checkout.
- Every order observes its named pre-fix failure and lands a passing tip. Missing contract-checkout variables skip that tier explicitly; supplied checkouts at a wrong revision fail.

## Exclusive owned paths

- `tests/pi-skill-creator/conftest.py`
- `tests/pi-skill-creator/test_foundation.py`
- `tests/pi-skill-creator/fixtures/common/**`
- `tests/pi-skill-creator/README.md`
- minimal project-level pytest configuration, only if collection requires it

## Read-only references

- `docs/pi-skill-creator-work-orders/contracts.md`
- current `skills/pi-skill-creator/scripts/**`
- pinned Pi and pi-subagents checkouts supplied by absolute path

## Prerequisites

The checkout is clean at `implementationStartCommit`, which contains the tracked index, contracts, all 17 orders, and both project workflows and descends from or equals the source baseline. Python 3.10+, `uv`, and `uvx` are available. Do not install into the repository.

## Red test

Name/path: `tests/pi-skill-creator/test_foundation.py::test_current_harness_has_no_project_regression_suite`.

Command:

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator/test_foundation.py::test_current_harness_has_no_project_regression_suite
```

Expected pre-fix failure: the project-level harness test directory/runner contract does not exist. Observe this before creating the suite, then replace this bootstrap check with positive foundation tests in the same branch. No red or broad `xfail` test lands.

## Required behavior

- Shared fixtures construct skill directories, campaign trees, JSONL transcripts, and subprocess outcomes without network or credentials.
- Markers `contract` and `live` are registered.
- Missing `PI_CHECKOUT`/`PI_SUBAGENTS_CHECKOUT` skips contract tests with an explicit reason; supplied wrong revisions fail.
- The standard offline, contract, live, and branch-tip commands match `contracts.md`.
- Tests and fixtures remain outside the distributable skill directory.

## Implementation steps

1. Observe the bootstrap failure.
2. Add shared path/revision helpers and marker registration.
3. Add small green tests proving fixture isolation, exact-root resolution, and the distribution boundary.
4. Document the pinned `uvx` commands and Python floor in `tests/pi-skill-creator/README.md`.
5. Run offline collection without Pi, then contract collection with both pinned checkout paths.

## Deterministic branch-tip gates

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator -m 'not contract and not live'
PI_CHECKOUT=/absolute/pi PI_SUBAGENTS_CHECKOUT=/absolute/pi-subagents uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator -m contract
git diff --check
```

The branch tip must pass. Future red regressions are introduced and fixed within their owning order.

## Live-test requirements

None. Any credential access is a defect.

## Non-goals

Do not fix runtime scripts, add adoption behavior, place tests under the skill, or create repository-wide CI coupling.

## Structured handoff

Return exactly these fields: `order_id`, `status`, `branch`, `commit`, `red_observed`, `offline_command`, `contract_command`, `tests_passed`, `tests_skipped`, `bounded_work`, `skipped_work`, `owned_paths_changed`, `summary`, `blockers`.

# OSC-16: Validate copied-directory distribution

## Findings

F19 is already resolved by deletion and receives no implementation. This order verifies that resolution and consumes F1/F12/F15-F19/F24/F30/F36e as final distribution gates.

## Dependencies

OSC-15. OSC-14 produces calibration evidence and OSC-15 applies the human-reviewed conclusions before this order, enforcing old WP11 before old WP12. If approved calibration intentionally skipped a claim, remove that claim before this order; do not present skipped evidence as passing.

## Settled decisions restated

- Finalization starts from the clean calibration integration commit whose records were human-reviewed; OSC-15 applies only the immutable review file's accepted conclusions before OSC-16 begins.
- Distribution is a byte-for-byte directory copy of `skills/opin-skill-creator/` into a temporary Pi-owned skill root. Tests, fixtures, campaign records, work orders, caches, repository configuration, TypeScript, npm metadata, and companion extensions remain outside it.
- Validation never repairs the temporary copy. Missing runtime files, loader/agent/command failure, boundary contamination, stale archive-distribution guidance, or any skipped/invalid claim fails final sign-off.

## Exclusive owned paths

- `tests/opin-skill-creator/test_distribution.py`
- `tests/opin-skill-creator/fixtures/distribution/**`
- `skills/opin-skill-creator/README.md` only for final distribution wording corrections exposed by the tests

## Read-only references

- complete skill directory and project test tree
- exact Pi/pi-subagents checkouts
- report/work orders, which must remain outside the copy

## Prerequisites

The branch with human-approved calibration conclusions is clean and green. A temporary directory is available. No test writes into the source skill.

## Red test

Name/path: `tests/opin-skill-creator/test_distribution.py::test_byte_copy_is_self_contained_loadable_and_runtime_only`.

Command:

```bash
PI_CHECKOUT=/absolute/pi PI_SUBAGENTS_CHECKOUT=/absolute/pi-subagents uvx --from 'pytest==9.1.1' pytest -q tests/opin-skill-creator/test_distribution.py::test_byte_copy_is_self_contained_loadable_and_runtime_only -m contract
```

Expected pre-fix failure: before adoption, the copied directory lacks the new runtime workflow/parser/RPC resources and cannot satisfy the current validator/agent registration/command boundary as a complete adopted artifact.

## Required behavior

Copy `skills/opin-skill-creator/` byte-for-byte into a temporary Pi-owned skill root. Run standalone validation and Pi's real loader against the copy. Register all four bundled agents through pi-subagents protocol v3. Execute every printed deterministic runtime command from its documented cwd. Assert the source/copy contains no project tests, fixtures, campaign records, work orders, caches, maintainer-only paths, TypeScript, npm metadata, or companion extension. Assert project development artifacts did not enter the copy. Verify all invocation examples fire under Pi and no user-facing string names Claude Code.

F19 check: repository runtime material contains no removed packaging helper and no archive-distribution instruction. This is verification of an already resolved deletion, not a repair assignment.

## Implementation steps

1. Add manifest/boundary/load/agent/command/product-string tests and observe failure.
2. Build the copy with `shutil.copytree` only.
3. Validate and load the copy from a temporary Pi-owned root.
4. Run bundled-agent registration and command smoke tests.
5. Compare manifests/hashes and reject all development-only material.
6. Search runtime material for stale archive/helper guidance and fix only README distribution wording if needed.

## Deterministic branch-tip gates

```bash
PI_CHECKOUT=/absolute/pi PI_SUBAGENTS_CHECKOUT=/absolute/pi-subagents uvx --from 'pytest==9.1.1' pytest -q tests/opin-skill-creator/test_distribution.py
uvx --from 'pytest==9.1.1' pytest -q tests/opin-skill-creator -m 'not live'
uvx --from 'ty==0.0.77' ty check skills/opin-skill-creator/scripts skills/opin-skill-creator/eval-viewer
git diff --check
```

## Live-test requirements

No new paid calls. Loader/command smoke tests use pinned local checkouts; auth-dependent examples are validated by OSC-14 records rather than re-run.

## Non-goals

Do not build a second distribution representation, modify the copied test subject, touch vendor/Pi/pi-subagents, or move project tests inside the skill.

## Structured handoff

Return: `order_id`, `status`, `branch`, `commit`, `red_observed`, `source_manifest_hash`, `copy_manifest_hash`, `loader_result`, `registered_agents`, `commands_checked`, `boundary_violations`, `f19_absence_verified`, `tests_passed`, `tests_skipped`, `bounded_work`, `skipped_work`, `owned_paths_changed`, `summary`, `blockers`.

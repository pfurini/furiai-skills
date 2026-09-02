# OSC-04: Harden the local review viewer

## Findings

Primary: F16, F22, F30, and F32. Secondary consumer of F21 and F36a.

## Dependencies

OSC-00.

## Settled decisions restated

- Viewer discovery follows `<campaign>/iteration-N/<eval-name>/{with_skill,without_skill}/run-N/`; those are the only configuration badges, and a missing eval id sorts after numbered ids.
- The server binds loopback on an available port and never signals an existing listener. Its PID is persisted at `iteration-N/viewer.pid`, and validated feedback is written only to `<workspace>/feedback.json`.
- Executor-controlled content is rendered as text, script termination cannot escape embedded data, and review works without network assets. Unsafe feedback shape/size or filesystem failure fails closed.

## Exclusive owned paths

- `skills/opin-skill-creator/eval-viewer/generate_review.py`
- `skills/opin-skill-creator/eval-viewer/viewer.html`
- `skills/opin-skill-creator/assets/eval_review.html`
- `tests/opin-skill-creator/test_viewer.py`
- `tests/opin-skill-creator/fixtures/viewer/**`

## Read-only references

- C3 workspace and C4 configuration contracts
- current `references/benchmarking.md` and `references/schemas.md`

## Prerequisites

OSC-00 is integrated. Tests bind loopback only and make no network requests.

## Red test

Name/path: `tests/opin-skill-creator/test_viewer.py::test_occupied_port_untrusted_script_and_missing_eval_id_are_safe`.

Command:

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/opin-skill-creator/test_viewer.py::test_occupied_port_untrusted_script_and_missing_eval_id_are_safe
```

Expected pre-fix failure: the viewer terminates the existing listener, embeds a script terminator unsafely, and raises when an eval id is missing.

## Required behavior

Choose an available loopback port without signaling any existing process. Sort missing eval ids after numbered ids. Embed executor-controlled data without executable script termination and render artifact text as text. Remove mandatory remote assets; spreadsheet rendering degrades to safe download/notice when no local renderer is present. Validate feedback shape and size before writing only `<workspace>/feedback.json`. Use only `with_skill` and `without_skill` badges. Persist the launched server PID in `iteration-N/viewer.pid` and document its path through machine-readable startup output. All user-facing text names Pi and the actual `feedback.json` flow.

## Implementation steps

1. Add occupied-port, mixed-metadata, injection, offline, feedback, and product-string fixtures.
2. Observe the focused failure.
3. Remove port-killing behavior and bind an available port.
4. Replace unsafe data embedding and active artifact rendering.
5. Remove CDN requirements or provide tested no-network degradation.
6. Implement PID-file and feedback validation behavior.

## Deterministic branch-tip gates

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/opin-skill-creator/test_viewer.py
uvx --from 'ty==0.0.77' ty check skills/opin-skill-creator/eval-viewer
git diff --check
```

## Live-test requirements

None. Browser visual review is optional and cannot replace tests.

## Non-goals

Do not redesign styling, change benchmark schemas, or edit benchmark prose.

## Structured handoff

Return: `order_id`, `status`, `branch`, `commit`, `red_observed`, `ports_tested`, `formats_tested`, `remote_assets`, `tests_passed`, `tests_skipped`, `bounded_work`, `skipped_work`, `owned_paths_changed`, `summary`, `blockers`.

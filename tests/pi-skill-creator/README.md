# pi-skill-creator test harness

The harness requires Python 3.10 or newer. It uses pinned ephemeral tools through `uvx`; do not install test dependencies into the repository.

Tests and fixtures are development-only material under `tests/pi-skill-creator/`. They must never be copied into `skills/pi-skill-creator/`.

## Offline unit and regression tests

This tier uses no network, credentials, model calls, or runtime checkout.

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator -m 'not contract and not live'
```

## Local pinned-checkout contract tests

These tests use local source checkouts without model credentials. Paths must be absolute and must name the exact checkout roots. Contract tests skip with an explicit reason when a required checkout variable is absent, while supplied paths at the wrong revision fail.

```bash
PI_EXECUTABLE=/absolute/path/to/pi-executable \
PI_CHECKOUT=/absolute/path/to/pi \
PI_SUBAGENTS_CHECKOUT=/absolute/path/to/pi-subagents \
PI_DYNAMIC_WORKFLOWS_CHECKOUT=/absolute/path/to/pi-dynamic-workflows \
uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator -m contract
```

Required revisions:

- Pi `0.84.4`: `db6bee3d6ccb79f5bc7884962ea4d98ca21e60ee`
- pi-subagents `0.19.0`: `7f569969445bf8bc6fbd7757f18db80b35de0ba9`
- pi-dynamic-workflows `3.10.1`: `c82d31af1e36b6f0e89cfcc4bdd728d982e22dc9`
- pi-claude-bridge `0.7.0`: `c1d8b24a57e15bc8acc9d673f2804ab7227978ae` (loaded in the host session through `~/.pi/agent/settings.json`; never a test input)

The runtime workflow tests in `test_runtime_workflow.py` execute `skills/pi-skill-creator/workflows/benchmark.js` through both pinned workflow runtimes:

- pi-subagents: the checkout's `node_modules/.bin/tsc` compiles `src/workflow/`, and a stub host stands in for agent spawning.
- pi-dynamic-workflows: `fixtures/workflow/pi-dynamic-workflows-probe.mjs` runs under the checkout's `node_modules/.bin/tsx`, imports `runWorkflow` from `src/workflow.ts`, and injects a fake agent runner. Run `npm ci` in that checkout once so `node_modules/.bin/tsx` exists (`npm ci` honours the committed lockfile; do not use `npm install`). The resulting untracked, git-ignored `node_modules/` is the only permitted change to that checkout. Those probes skip with a reason when `PI_DYNAMIC_WORKFLOWS_CHECKOUT` is unset or `tsx` is missing, and fail on a wrong revision.

Neither path makes a model call, writes a workflow log, or reads an agent registry.

`test_calibration_workflow.py` (contract tier) executes the two repository-development workflows, `.pi/workflows/pi-skill-creator-calibration.js` and `.pi/workflows/pi-skill-creator-adoption.js`, through the same compiled pi-subagents runtime with the stub host in `fixtures/calibration-workflow/stub-host-probe.mjs`. The stub answers every child from a fixture table and records the gate commands it is handed, so the stage schemas, approval tokens, `stageStartCommit` quoting, the exact-row `pi --list-models` checks, the paid-call bound comparison, and the phase grouping of integration agents are all asserted without a model call, a git command, or a gate command running. Fixture arguments live in `fixtures/calibration-workflow/*-args.json`. The same module validates the smoke target skill `fixtures/smoke/release-note-smoke/` with `quick_validate.py`; that fixture is the target of the OSC-14 smoke campaign and is never distributed.

## Credentialed and live tests

Do not run this tier without explicit approval. Replay mode is mandatory and must not make model calls.

```bash
PI_SKILL_CREATOR_LIVE_TESTS=1 \
PI_SKILL_CREATOR_REPLAY_ONLY=1 \
PI_EXECUTABLE=/absolute/path/to/pi-executable \
PI_CHECKOUT=/absolute/path/to/pi \
PI_SUBAGENTS_CHECKOUT=/absolute/path/to/pi-subagents \
PI_SKILL_CREATOR_CAMPAIGN_DIR=/absolute/path/outside/skill \
uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator -m live
```

## Deterministic branch-tip gates

Before OSC-07 integrates the existing `run_loop.py` type fix, use:

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator -m 'not live' && \
git diff --check
```

From OSC-07 onward, use:

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator -m 'not live' && \
uvx --from 'ty==0.0.77' ty check skills/pi-skill-creator/scripts skills/pi-skill-creator/eval-viewer && \
git diff --check
```

OSC-17 additionally requires the runtime workflow, bundled-agent, and aggregation tests to run with `PI_SUBAGENTS_CHECKOUT` and `PI_DYNAMIC_WORKFLOWS_CHECKOUT` set, with no pi-dynamic-workflows probe skipped. OSC-18 extends that gate with `test_calibration_workflow.py` and `test_rpc_runner.py` and requires all four checkout variables (`PI_EXECUTABLE`, `PI_CHECKOUT`, `PI_SUBAGENTS_CHECKOUT`, `PI_DYNAMIC_WORKFLOWS_CHECKOUT`) in the full `not live` run, so no contract test skips; a skip there is a gate failure.

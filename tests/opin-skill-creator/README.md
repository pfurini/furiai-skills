# opin-skill-creator test harness

The harness requires Python 3.10 or newer. It uses pinned ephemeral tools through `uvx`; do not install test dependencies into the repository.

Tests and fixtures are development-only material under `tests/opin-skill-creator/`. They must never be copied into `skills/opin-skill-creator/`.

## Offline unit and regression tests

This tier uses no network, credentials, model calls, or runtime checkout.

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/opin-skill-creator -m 'not contract and not live'
```

## Local pinned-checkout contract tests

These tests use local source checkouts without model credentials. Paths must be absolute and must name the exact checkout roots. Contract tests skip with an explicit reason when a required checkout variable is absent, while supplied paths at the wrong revision fail.

```bash
PI_EXECUTABLE=/absolute/path/to/pi-executable \
PI_CHECKOUT=/absolute/path/to/pi \
PI_SUBAGENTS_CHECKOUT=/absolute/path/to/pi-subagents \
uvx --from 'pytest==9.1.1' pytest -q tests/opin-skill-creator -m contract
```

Required revisions:

- Pi `0.84.4`: `a4043c1e332a61e4c8648b97b9b796c57f9db110`
- pi-subagents `0.19.0`: `bfa262fdd75d807b1c6b1f852f1f1bea2bbb3fa4`

## Credentialed and live tests

Do not run this tier without explicit approval. Replay mode is mandatory and must not make model calls.

```bash
OPIN_LIVE_TESTS=1 \
OPIN_REPLAY_ONLY=1 \
PI_EXECUTABLE=/absolute/path/to/pi-executable \
PI_CHECKOUT=/absolute/path/to/pi \
PI_SUBAGENTS_CHECKOUT=/absolute/path/to/pi-subagents \
OPIN_CAMPAIGN_DIR=/absolute/path/outside/skill \
uvx --from 'pytest==9.1.1' pytest -q tests/opin-skill-creator -m live
```

## Deterministic branch-tip gates

Before OSC-07 integrates the existing `run_loop.py` type fix, use:

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/opin-skill-creator -m 'not live' && \
git diff --check
```

From OSC-07 onward, use:

```bash
uvx --from 'pytest==9.1.1' pytest -q tests/opin-skill-creator -m 'not live' && \
uvx --from 'ty==0.0.77' ty check skills/opin-skill-creator/scripts skills/opin-skill-creator/eval-viewer && \
git diff --check
```

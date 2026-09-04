# pi-skill-creator implementation work orders

## Scope and authority

These work orders are the executable handoff for adopting Pi 0.84.4 and pi-subagents 0.19.0 in `skills/pi-skill-creator/`. The findings and settled decisions in `docs/pi-skill-creator-adoption-report.md` remain authoritative. `contracts.md` freezes interfaces where several orders meet. If an executor finds a conflict, it stops and records it instead of choosing a new contract locally.

This handoff was prepared on 2026-09-02 from source baseline `0b9e86bc77a60fb34039456a6624ea94e396f5d1`. That immutable source baseline only freezes the F19 removal and pre-implementation skill state; adoption never starts from that SHA. The adoption implementation start is a later clean commit containing this finalized index, `contracts.md`, every OSC-00 through OSC-16 order, and both project workflows (OSC-17 was added on 2026-09-04 after the adoption run and is executed standalone; see wave 8b). The caller supplies that full commit SHA as `implementationStartCommit`, and preflight requires it to equal current `HEAD` and descend from or equal the source baseline.

| Component | Exact revision |
|---|---|
| Source baseline | `0b9e86bc77a60fb34039456a6624ea94e396f5d1` |
| Implementation start | Caller-supplied full `implementationStartCommit` for the later clean handoff-containing commit |
| Pi fork | `0.84.4`, `a4043c1e332a61e4c8648b97b9b796c57f9db110` |
| pi-subagents | `0.19.0`, `7f569969445bf8bc6fbd7757f18db80b35de0ba9` (re-pinned by OSC-17 from `bfa262fdd75d807b1c6b1f852f1f1bea2bbb3fa4`; OSC-00 through OSC-13 integrated against the earlier revision) |
| pi-dynamic-workflows | `3.10.0`, `e9c5a41d9c4234df908aa25a2b49ee9648e896d4` (added by OSC-17) |
| pi-claude-bridge | `0.7.0`, `c1d8b24a57e15bc8acc9d673f2804ab7227978ae` (added by OSC-17; loaded in the host session, never a workflow input) |
| Agent Skills specification | `69ef37e9424c0a7ea9dd2293b559e43ec8176379` |
| Anthropic skill-creator comparison only | `53048666b05b4799081517d00e09e0a2dd688678` |

The Pi, pi-subagents, and pi-dynamic-workflows checkout paths are workflow inputs. No executor may assume sibling paths such as `../pi`, `../pi-subagents`, or `../pi-dynamic-workflows`.

The copied directory `skills/pi-skill-creator/` is the only distributed artifact. Project tests stay in `tests/pi-skill-creator/`. The removed archive convention is not a compatibility target.

## Finding traceability

Every finding and every enumerated F36 subfinding has exactly one primary owner. Secondary consumers may use the result but do not redefine it.

| Finding | Primary owner | Secondary consumers | Resolution/gate |
|---|---|---|---|
| F1 validator contract stale | OSC-02 | OSC-16 | Differential parity with pinned Pi loader |
| F2 reversed benchmark delta | OSC-05 | OSC-12 | `with_skill - without_skill` regardless of discovery order |
| F3 untrustworthy benchmark metadata | OSC-05 | OSC-07, OSC-12, OSC-14 | Complete campaign metadata required |
| F4 one model for experimental roles | OSC-07 | OSC-08, OSC-09, OSC-10, OSC-12, OSC-14 | Requested/effective role fields |
| F5 trigger evaluator renames skill | OSC-08 | OSC-09 | Real name preserved |
| F6 infrastructure failures become negatives | OSC-08 | OSC-09, OSC-14 | Closed trigger status enum |
| F7 print/JSON cannot prove native fork | OSC-10 | OSC-11, OSC-12, OSC-14 | RPC-only fork fidelity |
| F8 clean mode disables dependencies | OSC-10 | OSC-11, OSC-12, OSC-14 | Three environment profiles |
| F9 hidden skills are trigger-optimized | OSC-09 | OSC-13 | Skip trigger optimization |
| F10 optimizer contradicts doctrine | OSC-09 | OSC-03 | Canonical capability-first prompt |
| F11 final holdout reused | OSC-09 | OSC-14 | Train/validation/final-test |
| F12 bundled agents not explicitly dispatched | OSC-06 → OSC-17 (workflow dispatch) | OSC-12, OSC-16 | Four registered agent definitions for the top-level `Agent` path; the runtime workflow tells children to read `agents/<role>.md` by absolute path and never dispatches by `agentType` |
| F13 analyzer carries two roles | OSC-06 | OSC-12 | Split analyzer files |
| F14 fresh context unlocked | OSC-06 | OSC-10, OSC-11 | Authoritative frontmatter |
| F15 no harness regression suite | OSC-00 | Every implementation order | Passing-main project test suite |
| F16 unsafe/non-reproducible viewer | OSC-04 | OSC-16 | Local-safe offline viewer |
| F17 prose layout unreadable by aggregator | OSC-05 | OSC-12, OSC-16 | Frozen workspace tree; no-data is fatal |
| F18 validator accepts unloadable skills | OSC-02 | OSC-16 | Empty/missing names and descriptions fail |
| F19 archive packaging | **Resolved before implementation; no order** | OSC-16 verifies absence | Deleted; copied directory is distribution |
| F20 comparator model unavailable in hermetic runs | OSC-06 → OSC-17 (comparator pin) | OSC-10, OSC-14 | Profile-aware preflight; unavailable pin fails; pin is `claude-bridge/claude-opus-5` with `extensions: [pi-claude-bridge]` |
| F21 configuration has three names | OSC-05 | OSC-04, OSC-12 | Only `with_skill`/`without_skill` |
| F22 viewer sort crash | OSC-04 | OSC-16 | Missing eval id sorts safely |
| F23 trigger evaluator runs in wrong project | OSC-08 | OSC-09 | Explicit evaluation cwd |
| F24 README cannot invoke hidden skill | OSC-13 | OSC-14 | Command-form examples only |
| F25 (tool-vocabulary subfinding) | OSC-06 | OSC-01, OSC-05 | Lowercase Pi tool names |
| F25 (transcript-format/location subfinding) | OSC-01 | OSC-06, OSC-10, OSC-12 | Parser contract in `contracts.md` |
| F26 false sterilization premise | OSC-11 | OSC-10 | Source-backed profile wording after RPC/local contract evidence |
| F27 Pi-blind authoring doctrine | OSC-03 | OSC-10, OSC-11, OSC-12 | Pi frontmatter/rendering doctrine |
| F28 metrics artifacts have no producer | OSC-01 | OSC-05, OSC-06, OSC-10, OSC-12 | Measured transcript/RPC telemetry only |
| F29 assertions/expectations split | OSC-05 | OSC-06, OSC-12 | Only `expectations` |
| F30 viewer names Claude Code | OSC-04 | OSC-16 | Pi and `feedback.json` wording |
| F31 stale/misplaced schemas | OSC-05 | OSC-03, OSC-12 | Direct SKILL pointer and current paths |
| F32 shell-local viewer PID | OSC-04 | OSC-12 | PID file in iteration directory |
| F33 nonexistent managed policy tier | OSC-10 | OSC-12 | Removed |
| F34 false `--skill` auto-load claim | OSC-10 | OSC-12 | Exact Pi behavior documented |
| F35 (unnamed-mechanisms subfinding) | OSC-11 | OSC-12 | Mechanisms named in runtime prose |
| F35 (workflow-child transcript subfinding) | OSC-01 | OSC-10, OSC-12 | Supported seam and fail-closed boundary |
| F36a `eval_name` dropped | OSC-05 | OSC-04 | Propagated from metadata |
| F36b `generate_report.py` empty history crash | OSC-09 | OSC-00 | Empty history has useful output/error, never `ValueError` |
| F36c optimizer command discards reports | OSC-09 | OSC-12 | Explicit `--report none` and `--results-dir` guidance |
| F36d creator description violates doctrine | OSC-03 | OSC-13 | Third-person human-facing summary |
| F36e Python floor unstated | OSC-13 | OSC-16 | Python 3.10+ stated and tested |
| F36f leading `@`/`-` query swallowed | OSC-08 | OSC-09 | Prompt over stdin/RPC, never positional `-p` argv |
| F37 SDK route lacks fork fidelity | OSC-10 | OSC-12 | Python RPC runner; no SDK dependency |

## Corrected dependency DAG

```text
OSC-00 passing test foundation
├── OSC-01 telemetry seam and transcript parser
│   ├── OSC-05 aggregation and schemas
│   │   └── OSC-07 role model configuration
│   │       ├── OSC-08 trigger reliability
│   │       │   └── OSC-09 optimizer methodology
│   │       └── OSC-10 RPC runner and profiles
│   │           └── OSC-11 testing doctrine and sterilization
│   └── OSC-06 bundled agents
├── OSC-02 validator parity
└── OSC-04 viewer hardening

OSC-03 Pi authoring doctrine ───────────────┐
                                             ├── OSC-10
                                             └── OSC-11

OSC-05 + OSC-06 + OSC-07 + OSC-09 + OSC-10 + OSC-11
└── OSC-12 runtime benchmark workflow and benchmark prose
    └── OSC-13 deterministic README corrections
        └── OSC-17 orchestrator-independent benchmark workflow
            └── HUMAN APPROVAL FOR PAID/LIVE WORK
                └── OSC-14 Pi-native calibration records
                    └── HUMAN REVIEW OF CALIBRATION RESULTS
                        └── OSC-15 apply approved conclusions
                            └── OSC-16 directory distribution validation
```

This enforces the report corrections: old WP5 precedes WP6; old WP11 precedes WP12; authoring doctrine precedes RPC fork tests while sterilization prose follows the RPC evidence; telemetry is frozen before aggregation, agents, RPC integration, and the runtime workflow.

## Execution waves

The project workflow may parallelize only the orders listed on the same row. Parallel writers use separate worktrees and are integrated only after every branch in that row passes its own gate.

| Wave | Orders | Barrier rationale |
|---|---|---|
| 0 | Human approves implementation; preflight exact revisions and clean implementation start | No agent runs before approval; every isolated worktree starts from the handoff-containing commit |
| 1 | OSC-00 | Establish a green shared gate before any behavioral fix |
| 2 | OSC-01, OSC-02, OSC-03, OSC-04 | Disjoint runtime/docs/test paths |
| 3 | OSC-05, OSC-06 | Parser contract is integrated; writers are disjoint |
| 4 | OSC-07 | Serial owner of three shared model-consuming scripts |
| 5 | OSC-08, OSC-10 | `run_eval.py` and RPC/profile module paths are disjoint |
| 6 | OSC-09, OSC-11 | Optimizer/report files and testing/SKILL prose are disjoint |
| 7 | OSC-12 | Sole integration owner of `benchmarking.md`, runtime workflow, and final SKILL workflow wiring |
| 8 | OSC-13 | README deterministic corrections after runtime behavior settles |
| 8b | OSC-17 | Runtime portability, comparator re-pin, and pi-subagents re-pin after the README settles; serial later owner of every path it touches, so calibration records carry the runtime fields |
| Stop | Report ready-for-calibration state | Implementation workflow does not run live or paid calibration |
| 9 | Human separately approves calibration; OSC-14 | Separate workflow and explicit budget/model arguments |
| Stop | Human reviews `review-required.json` and records decisions | No claims or pins change before this checkpoint |
| 10 | OSC-15 | Apply only the human-approved calibration conclusions; no paid calls |
| 11 | OSC-16 | Old WP11 precedes old WP12; final copied-directory proof |

## Exclusive file ownership matrix

An order owns a path only during its wave. A later serial owner starts from the integrated earlier result. No same-wave overlap is allowed.

| Path | Owners in order |
|---|---|
| `references/benchmarking.md` | OSC-12 → OSC-17 |
| `SKILL.md` | OSC-03 → OSC-11 → OSC-12 → OSC-17 (Step 7 only) → OSC-15 (only for a human-approved creator pin) |
| `references/schemas.md` | OSC-05 → OSC-17 |
| `references/testing.md` | OSC-11 → OSC-17 |
| `references/writing-principles.md` | OSC-03 only |
| `scripts/run_eval.py` | OSC-07 → OSC-08 |
| `scripts/run_loop.py` | OSC-07 → OSC-09 |
| `scripts/improve_description.py` | OSC-07 → OSC-09 |
| `scripts/generate_report.py` | OSC-09 only |
| `scripts/quick_validate.py`, `scripts/utils.py` | OSC-02 only |
| `scripts/transcript_metrics.py` | OSC-01 only |
| `scripts/rpc_runner.py` | OSC-10 only |
| `scripts/aggregate_benchmark.py` | OSC-05 → OSC-17 |
| `agents/*.md` | OSC-06 → OSC-17 (`comparator.md` only) → OSC-15 (only for human-approved calibrated pin changes) |
| `eval-viewer/**`, `assets/eval_review.html` | OSC-04 only |
| `workflows/benchmark.js` | OSC-12 → OSC-17 |
| `README.md` | OSC-13 → OSC-17 (runtime requirements and caveats only) → OSC-15 → OSC-16 |
| `tests/pi-skill-creator/test_foundation.py`, shared fixture helpers | OSC-00 → OSC-17 (`conftest.py` pin constants and `campaign_factory` fields only) |
| `tests/pi-skill-creator/README.md` | OSC-00 → OSC-17 |
| Order-specific test modules/fixture subdirectories | The corresponding order only; OSC-17 is the later owner of `test_runtime_workflow.py`, `fixtures/workflow/**`, `test_bundled_agents.py`, `test_aggregation.py` (campaign fixture fields), and may add assertions to `test_readme.py` and `test_testing_doctrine.py` |
| `.pi/workflows/pi-skill-creator-adoption.js`, `.pi/workflows/pi-skill-creator-calibration.js` | OSC-17 (`REQUIRED_SUBAGENTS` constant only) |
| `docs/pi-skill-creator-work-orders/contracts.md`, `osc-06-bundled-agents.md`, `docs/pi-skill-creator-adoption-report.md` model-policy lines | OSC-17 (contract amendments and comparator pin lines only) |
| `.skill-creator/**` campaign records | OSC-14 only; never distributed |

Tests use order-scoped modules (`test_validator.py`, `test_aggregation.py`, and so on), so parallel orders do not share a test file.

## Human approval checkpoints

1. **Before implementation fan-out:** after committing the finalized handoff, the user must invoke `.pi/workflows/pi-skill-creator-adoption.js` from that clean repository `HEAD` with `approval: "APPROVE_IMPLEMENTATION"`, `implementationStartCommit` equal to that full commit SHA, an absolute Pi executable path, and absolute repository, Pi, and pi-subagents checkout paths. Preflight proves the commit contains the tracked index, contracts, all 17 OSC orders that existed at that time (OSC-00 through OSC-16), and both project workflows, and that it descends from or equals source baseline `0b9e86bc77a60fb34039456a6624ea94e396f5d1`. This makes every isolated implementation worktree branch from a commit containing every order and contract it must read. File existence or the source-baseline SHA is not approval. The workflow returns both `implementationStartCommit` and the final deterministic `implementationIntegrationCommit`.
2. **Before runtime multi-agent campaigns:** the implemented skill must ask the user before invoking `Agent` fan-out, `SubagentWorkflow`, or `workflow`; documentation cannot pre-authorize a run.
3. **Before paid/live calibration:** the user separately invokes `.pi/workflows/pi-skill-creator-calibration.js` with `stage: "calibrate"`, `stageStartCommit` equal to that `implementationIntegrationCommit`, `approval: "APPROVE_PAID_CALIBRATION"`, explicit models, repetitions, maximum paid calls, campaign directory, and absolute checkout paths. Preflight requires exact `HEAD` and a clean tree at `stageStartCommit`; success returns `calibrationIntegrationCommit`.
4. **Before permanent model pins or public numeric claims:** a human reads the pre-registered key and every deterministic failure flagged by calibration.
5. **Before final distribution sign-off:** the user invokes the calibration workflow again with `stage: "finalize"`, `stageStartCommit` equal to the human-reviewed `calibrationIntegrationCommit`, `approval: "APPROVE_CALIBRATION_RESULTS"`, `humanReviewComplete: true`, and the absolute immutable review record. Preflight again requires exact `HEAD` and a clean tree. OSC-16 runs only after OSC-15 applies that record; a skipped claim may be removed, never presented as calibrated.

## Completion definition

Adoption is complete only when:

- all OSC-00 through OSC-17 deterministic gates pass at one integrated commit;
- the optional/live tier either passes with approved campaign records or all unsupported model claims and pins are removed;
- `uvx --from 'pytest==9.1.1' pytest -q tests/pi-skill-creator` passes offline;
- local contract tests pass against the exact Pi, pi-subagents, and pi-dynamic-workflows revisions above (the pi-subagents revision is the OSC-17 re-pin);
- `uvx --from 'ty==0.0.77' ty check skills/pi-skill-creator/scripts skills/pi-skill-creator/eval-viewer` passes;
- the runtime workflow passes meta extraction and execution tests on both pinned workflow runtimes (pi-subagents stub host and pi-dynamic-workflows injected runner), including the thrown-child and resume-replay cases;
- every campaign rejects missing runs, mixed profiles, null/schema failures, unresolved models, and infrastructure failures, and records `workflow_runtime` and `workflow_runtime_revision`;
- a byte-for-byte copied `skills/pi-skill-creator/` directory validates, loads, and registers bundled agents from a temporary Pi-owned skill root;
- the skill directory contains runtime material only, while tests, fixtures, campaign records, this report, and these orders remain outside it;
- no runtime instruction or helper describes an archive package or references the removed packaging helper;
- no user-facing string names Claude Code; and
- no Pi, pi-subagents, pi-claude-bridge, or pi-dynamic-workflows source checkout was modified (the untracked, ignored `node_modules/` that `npm ci` creates in pi-dynamic-workflows is the only allowed change).

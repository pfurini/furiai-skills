# Pi Harness Adoption Report

Status: implementation handoff; F19 distribution-path removal applied
Date: 2026-09-02, revised 2026-09-02 after review
Scope: `skills/pi-skill-creator/`

## Purpose

This report records the gaps between the current `pi-skill-creator` implementation and the capabilities available in the local Pi fork and `pi-subagents`. It divides the work into independently assignable implementation packages, each with evidence, scope, dependencies, and required tests.

This file is an implementation artifact, not runtime skill guidance. Do not load it from `SKILL.md`, and never ship it inside the skill folder.

It is deliberately process-agnostic. Implementation findings cite the skill's own files and the two pinned runtime revisions below. The later distribution decision also compares the Agent Skills specification with Anthropic's upstream `skill-creator` to distinguish the portable directory contract from the inherited archive convention. A fresh implementation agent needs this file, the skill folder, and read access to the two runtime checkouts.

## Review record

Revised 2026-09-02 after a verification pass over every original finding plus an independent audit run without sight of this report.

What changed:

- **F1 through F16 all stand.** Each was re-checked against the cited source, and the blocking ones were reproduced by execution rather than by reading. Two corrections were needed, both to evidence rather than to a conclusion: F1's field list was incomplete and F15 named the wrong files.
- **F17 through F37 are new.** The independent audit and the verification pass each found the workspace-layout defect (F17) separately, which is why it is recorded as blocking rather than as a documentation nit.
- **Every citation was re-verified on 2026-09-02.** A second pass opened each source line that had been supplied by the audit rather than read directly, including F6, F24, F25, F27, F32, and F36. All held; no finding changed. F27's absence list should be trimmed to the seven unambiguous field spellings, since words like `agent` and `paths` are ordinary English and their absence is not checkable.
- **Two defects in this report's own proposal**, recorded as F20 and F37. F20: the blind comparator model it recommended is extension-provided and cannot resolve in the hermetic environments the same report asks for. F37: the fork-test route it recommended first, a TypeScript SDK runner, is the one that does not deliver fork fidelity without an undocumented extra step, and it is also the expensive one. Both defaults were corrected in place, and WP8 was rewritten around RPC mode.
- **The inherited `.skill` archive path was removed by user decision after review.** It is an Anthropic `skill-creator` convenience, not an Agent Skills or Pi distribution format. F19 is resolved by deletion rather than repair, tests move outside the distributable skill directory, and WP12 now validates directory-copy installation.

Findings carrying `reproduced` in their evidence were executed at review time; the command and its output are the evidence, not a reading of the code.

## Revisions analyzed

| Component | Version or revision |
|---|---|
| Skill under analysis | `skills/pi-skill-creator/`, at its Pi-ported state of 2026-09-01 |
| Pi fork | `0.84.4`, `a4043c1e332a61e4c8648b97b9b796c57f9db110` |
| pi-subagents | `0.19.0`, `bfa262fdd75d807b1c6b1f852f1f1bea2bbb3fa4` |
| Agent Skills specification | `69ef37e9424c0a7ea9dd2293b559e43ec8176379`, directory contract checked 2026-09-02 |
| Anthropic `skill-creator` | `53048666b05b4799081517d00e09e0a2dd688678`, `.skill` helper checked 2026-09-02 |
| Current session model | `openai-codex/gpt-5.6-sol`, thinking `high` |
| Configured startup default | `openai-codex/gpt-5.6-luna`, thinking `high` |

Primary references:

- `../pi/packages/coding-agent/docs/skills.md`
- `../pi/packages/coding-agent/docs/sdk.md`
- `../pi/packages/coding-agent/docs/models.md`
- `../pi/packages/coding-agent/docs/json.md`
- `../pi-subagents/README.md`
- `../pi-subagents/docs/workflows.md`
- `../pi-subagents/docs/rpc.md`
- `../pi-subagents/src/agent-dir-loader.ts`
- `../pi-subagents/src/skill-agents.ts`
- `../pi-subagents/src/invocation-config.ts`
- `../pi-subagents/src/model-resolver.ts`
- `https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/docs/specification.mdx`
- `https://github.com/anthropics/skills/blob/53048666b05b4799081517d00e09e0a2dd688678/skills/skill-creator/scripts/package_skill.py`

## Executive findings

The current skill is conceptually aware of subagents but does not make their behavior deterministic. Its three bundled agent files have no frontmatter, the skill does not explicitly dispatch them as agent types, and qualitative executor-model selection exists only as prose.

The quantitative harness has correctness defects that can invalidate results:

1. `quick_validate.py` rejects valid Pi frontmatter.
2. `aggregate_benchmark.py` can calculate the pass-rate delta with the wrong sign.
3. Benchmark metadata records placeholder model names and a hardcoded run count.
4. `run_loop.py` uses one model for both trigger evaluation and description generation.
5. `run_eval.py` changes the tested skill name and counts infrastructure failures as non-triggers.
6. The clean-slate `pi -p` recipe cannot test `context: fork` because Pi degrades forked skills to inline execution in print and JSON modes.
7. The same recipe disables extensions, so it cannot test pi-subagents integration.
8. Trigger optimization runs even for user-invoked skills whose descriptions are not model-visible.
9. The optimizer prompt contradicts the skill's own description doctrine.
10. The repeatedly consulted holdout is a validation set, not a final held-out test.
11. No automated test suite protects the Python harness.

The review pass added a second group, and three of them outrank most of the list above because they break the documented lifecycle rather than degrade it:

12. The aggregator cannot read the workspace layout the skill tells the agent to build, and it fails open: no runs discovered, exit `0`, and a `benchmark.json` reporting a `+0.00` delta.
13. `quick_validate.py` accepts a skill with an empty `name` or `description`, which Pi refuses to load. The validator's own gate passes an unloadable skill.
14. The inherited `.skill` archive path is not part of Agent Skills or Pi, and its printed command also crashes. The user chose removal rather than repair.
15. The blind comparator model this report recommends is extension-provided and cannot resolve under `--no-extensions` or `isolated: true`, where it silently degrades to the parent model.
16. Prose, schema, and viewer disagree on the configuration directory name, so the human review step renders both arms unlabeled.
17. The doctrine the skill teaches predates Pi: it knows three frontmatter fields, names none of the pi-subagents mechanisms its own method depends on, and asserts that subagents cannot be sterilized when the extension provides exactly that.
18. The fork-test route this report recommended first would not have tested forks. `pi --mode rpc` does what the SDK was named for, at no dependency cost.

The recommended target is a hybrid implementation:

- Keep the creator itself user-invoked and inline because its process requires human decisions.
- Use real skill-bundled agents with explicit frontmatter for grading and analysis.
- Pass executor models explicitly because the executor floor is an experimental variable.
- Use a bundled `SubagentWorkflow` for dynamic benchmark fan-out after explicit user approval.
- Drive Pi over RPC mode for the behavioral tests that print and JSON mode cannot express, above all forked skills. This is a subprocess speaking JSON lines, so it adds no dependency and needs no new language. Reach for the TypeScript SDK only if something later needs in-process access, and read F37 first.
- Stay in Python for everything the skill ships, catch contract drift with a differential test rather than a port, and distribute the skill as a copied directory rather than a custom archive. See "Language and distribution decision" below.

## Language and distribution decision

Settled 2026-09-02, then revised after the user rejected the inherited `.skill` archive convention. The earlier wording ("keep Python only where it remains useful") implied a migration that no work package actually performs, while the archive path implied a Pi distribution format that does not exist.

**Decision: the distributable artifact is the skill directory itself. Everything the skill ships is Python, plus exactly one JavaScript workflow file. No `.skill` archive, packaging helper, TypeScript, npm dependency, or companion extension.**

The install model decides it. A skill is a folder you copy, and nothing about copying a folder makes Pi's TypeScript reachable:

The deleted `package_skill.py` was byte-for-byte inherited from Anthropic's `skill-creator`. It created an ordinary ZIP with a `.skill` suffix, but neither the Agent Skills specification nor Pi defines that archive format. Pi loads skill directories. Retaining the helper would preserve a Claude-oriented convenience while adding a distribution path Pi cannot consume, so removal is the compatibility fix.

- `@earendil-works/pi-coding-agent` does not resolve from an arbitrary directory. A Node script inside a skill folder fails with `ERR_MODULE_NOT_FOUND` unless the folder becomes an npm package with its own `node_modules`, which ends the zero-dependency property and requires network access at install time.
- The published package is upstream Pi, not this fork. A validator installed from the registry would check skills against a contract that is not the one they will run under, and pi-subagents' skill-bundled agents are inert there (no A.9 seam), so agent-related checks would report clean rather than fail.
- Importing by absolute path into a local Pi checkout works on exactly one machine. The Pi in use here is a source checkout, not a package install, so such a path is not portable and would falsify every distribution claim in `README.md`.
- **A skill cannot bundle an extension.** Extension discovery is `~/.pi/agent/extensions/*.ts`, `~/.pi/agent/extensions/*/index.ts`, `.pi/extensions/*.ts`, `.pi/extensions/*/index.ts`, or an explicit entry in `settings.json`. A skill folder is not among them. Skills bundle agents through pi core's A.9 seam; there is no equivalent seam for extensions. Shipping a validator extension would mean a two-part install and a gate that exists only inside a running Pi, unavailable to CI, a pre-commit hook, or a plain shell.

The one exception is mandated rather than chosen: `workflows/benchmark.js` (WP9) must be plain JavaScript, because the pi-subagents workflow sandbox rejects TypeScript outright.

### How drift is caught instead

`quick_validate.py` is a copy of Pi's frontmatter contract, and F1 and F18 are what a copy does when nothing checks it. The fix is a test, not a port. Pi's real loader is publicly exported — `loadSkills()` and `loadSkillsFromDir()` return `{ skills, diagnostics }` — so a maintainer checkout that has the Pi source available alongside it can use Pi as the oracle, even though a distributed copy of the skill cannot.

Add a **differential test**: run the validator's whole fixture corpus through both `quick_validate.py` and Pi's loader, and assert the verdicts agree fixture by fixture. When Pi's source is not found, skip the test with a clear message rather than failing.

This keeps the two properties that are actually in tension. The shipped artifact stays a portable folder of Python, and the contract stops drifting silently, because a divergence becomes a failing test in the repository where the skill is maintained. It also replaces WP2's proposed "versioned contract note", which records a revision number but cannot fail when the revision moves.

The escalation condition, so this decision is revisitable rather than permanent: if the skill ever needs in-process access to a running Pi session that RPC cannot provide, that is the trigger to reopen the language question, and F37 records what such a route would have to satisfy.

## Settled decisions

Ruled 2026-09-02, before any work package starts. These are the shared premises that more than one package depends on. They are settled here so each package implements a decision rather than re-deriving it, and so two packages cannot reach different answers in separate worktrees and merge cleanly into a broken result.

A work order derived from this report **restates the decisions it depends on** rather than citing them. That duplication is deliberate: an executor that must come back here to learn the layout will either skip it or get it wrong.

D11 in this list is the language and distribution decision recorded in the section above; it is not repeated here.

### D1 — Workspace layout

Keep the human-readable eval directory names the prose already asks for, and make the tools match them. The aggregator's `eval-*` glob is what changes, not the naming convention, because descriptive names are worth more to a human reading a campaign than to a script matching one. The `run-N` level is real and stays; the prose must document it, since today it appears in no reference file.

Binds: WP1 fixtures, WP3 aggregator, WP10 viewer, and the layout text in `testing.md`, `benchmarking.md`, and `schemas.md`. Resolves F17.

### D2 — Configuration directory name

`with_skill` and `without_skill`. The schema already mandates these two strings and the viewer's badge regex already matches them; only the prose disagrees, so the prose is what changes. `baseline`, `new_skill`, and `old_skill` are removed from the viewer regex and from `schemas.md` rather than kept as accepted synonyms.

Binds: WP3, WP10, and the workspace text in `testing.md` and `benchmarking.md`. Resolves F21.

### D3 — One term for a graded claim

`expectations`. It is the key both consumers actually read (`aggregate_benchmark.py` reads `grading.get("expectations")`, and the viewer reads the same field), so it is the spelling that cannot be changed without breaking code. `assertions` disappears from `benchmarking.md`.

Binds: WP3, WP4, `schemas.md`, `benchmarking.md`, `agents/grader.md`. Resolves F29.

### D4 — Tool vocabulary and transcript format

Pi's registered tool names are lowercase — `bash`, `edit`, `find`, `grep`, `ls`, `read`, `write` — and `Glob` is not a Pi tool at all. The transcript a grader reads is the pi-subagents JSON-lines `.output` file, not a Markdown document.

This is not a fork; Pi's names are facts. It is listed here only because four artifacts state the wrong thing and must change together.

Binds: WP4, `schemas.md`, `agents/grader.md`. Resolves F25, and the transcript half of F35.

### D5 — `execution_metrics` is measured, not self-reported

Derive it from the pi-subagents transcript. No executor agent is added, and the grader stops expecting `metrics.json` and `user_notes.md` to exist.

The transcript already carries everything the schema wants. Verified against a real 620 KB subagent transcript from this session: `tool_execution_start` events give a tool-call histogram in Pi's own vocabulary (`58 bash`, `17 read` in that run), and the `usage` record gives `input`, `output`, `cacheRead`, `cacheWrite`, `totalTokens`, and **`cost`**.

Cost was not previously known to be available. It is the measurement the whole benchmarking arm ultimately wants, so the transcript parser should capture it even though nothing consumes it yet.

The reason this beats an executor agent that writes its own `metrics.json`: a self-report is an agent's claim about what it did, and this skill's own doctrine ("read the transcripts, not just the outputs") rejects exactly that. Deriving from the transcript is measurement.

Binds: WP3, WP4, `schemas.md`, `agents/grader.md`, and a new transcript-parsing utility that WP8 needs regardless. Resolves F28.

### D6 — Environment profiles

Three named profiles replace the in-situ / clean-slate split:

1. **`in-situ`** — the real user environment, competing skills included. Correct for trigger measurement, where the competing set is the thing being measured.
2. **`hermetic-core`** — an isolated in-harness subagent: `prompt_mode: replace`, `isolated: true`, and `isolation: worktree` when the run writes files. This is the default clean environment.
3. **`declared-dependencies`** — `hermetic-core` plus explicitly named extensions, for anything that needs pi-subagents present.

The subprocess route is no longer the default clean environment. It is reserved for claims that genuinely require a separate process, which today means fork fidelity over RPC. `testing.md`'s claim that subagents "cannot be sterilized" is false and is deleted rather than softened.

Every campaign record names the profile it ran under. Records from different profiles are not comparable and must not be aggregated together.

Binds: WP8, WP13, `testing.md`, `benchmarking.md`. Resolves F8, F26, and the recipe half of F34.

### D7 — Where the work orders live, and what the gate is

Work orders live **outside** the skill folder, so the skill directory holds only material that could ship. They belong beside this report, in whatever documentation area the hosting repository already uses, named per skill so another skill could have work orders later without collision.

The harness test suite stays a **separate documented command**, produced by WP1 and required by every work order. It is not wired into any repository-wide build gate: this skill is a development tool rather than a shipped package, and coupling a repository's build to it buys enforcement at the cost of an unrelated dependency. If enforcement is wanted later, adding it is a small change; starting there is not.

### D8 — How the fan-out runs

Parallel only where file sets are genuinely disjoint. Concretely:

- Every shared prose file gets **one owner per wave**. `references/benchmarking.md` is currently contended by WP3, WP4, and WP13; `references/schemas.md` by WP2 and WP3; `SKILL.md` by WP4 and WP13. A wave that ships two owners for one file is a planning defect, not a merge problem to solve later.
- Packages whose file sets are disjoint after that partition may run in parallel worktrees.
- Everything else runs serially.

Assume the executing agent is serial by construction — one unit of work at a time against a clean tree, committing directly. Running several concurrently is a separate decision that has to be taken deliberately, and only for packages that have earned it.

The failure this guards against is not the merge conflict, which is visible. It is the semantic conflict: two worktrees each green, merging cleanly, producing a broken system — which is exactly what D1 and D2 would have caused between WP3 and WP10 had they stayed unsettled.

### D9 — Test runner and development dependencies

The distributable skill directory stays zero-dependency and contains runtime material only. Development tests and fixtures live at the project-level `tests/pi-skill-creator/`, outside `skills/pi-skill-creator/`.

Runner: `pytest`, invoked through `uvx` so nothing is installed into the project and no `pip` is involved. The differential validator test is inherently parametrized over a fixture corpus, which is what pytest is good at and what `unittest` makes awkward.

WP12 verifies the directory boundary directly: copying `skills/pi-skill-creator/` must include every runtime dependency and cannot include the external test tree, campaign records, this report, or its work orders.

### D10 — What a unit of work carries

Almost every unit here repairs a defect that already has evidence, rather than building something new. So each one names four things: the **finding id** it fixes, the **failing test** that reproduces the defect and must be red first, the **behavior** that is correct once it passes, and the **command** that proves it.

The finding id is what ties an instruction back to its evidence, and it is what lets an executor check the claim instead of trusting it. A unit that cannot name a failing test is either not a defect repair or is not yet understood well enough to assign.

Anchors into Pi `a4043c1e332a61e4c8648b97b9b796c57f9db110` and pi-subagents `bfa262fdd75d807b1c6b1f852f1f1bea2bbb3fa4` may carry line numbers, because those revisions are immutable. Anchors into this skill may not, because it is the thing being changed.

## Current behavior and model resolution

### Main creator skill

`SKILL.md` currently declares only:

```yaml
name: pi-skill-creator
description: ...
disable-model-invocation: true
```

Consequences:

- The skill is correctly user-invoked and carries no permanent model-facing listing cost.
- It remains inline because `context` is absent.
- It inherits the session model and thinking level because `model` and `effort` are absent.
- The current invocation would therefore use `openai-codex/gpt-5.6-sol` at `high` unless the user changes the session first.

Do not add `context: fork` to the creator by default. The creator has human confirmation gates, while a forked background skill moves the body out of the parent context and makes interactive coordination harder. Native fork should instead be tested and documented for skills created by this skill.

### Qualitative executors

`SKILL.md` establishes an executor floor, and `references/testing.md` says forward tests must use it. Neither file provides a concrete `Agent` call or a model parameter contract. The orchestrator can therefore:

- Inherit its own model accidentally.
- Pick a model stronger than the declared floor.
- Reuse a prior agent rather than create a fresh context.
- Grade inline rather than dispatch the bundled grader.

A statement that a forward test ran at the executor floor is currently not mechanically supported.

### Bundled agents

The current files are:

- `agents/grader.md`
- `agents/comparator.md`
- `agents/analyzer.md`

They contain no YAML frontmatter. If Pi dispatches them as skill-bundled agents, pi-subagents derives these defaults:

| Setting | Effective default |
|---|---|
| Agent name | Filename |
| Model | Inherit parent |
| Thinking | Inherit parent |
| Prompt mode | `replace` |
| Conversation inheritance | `false` unless caller overrides it |
| Background | Project `backgroundByDefault`, currently `true` |
| Built-in tools | All |
| Extensions | All |
| Skills | All |
| Turn limit | Unlimited |
| Session persistence | Project default, currently true |
| Output transcript | Project default, currently true |

The prose does not explicitly call these agent types. For example, `references/benchmarking.md` says to grade against `agents/grader.md` and permits grading inline. The files therefore behave more like prompt references than registered specialist agents.

### Description optimizer subprocesses

`run_loop.py` has one required `--model` argument. It passes that same value to:

- `run_eval()` for every trigger query.
- `improve_description()` for description generation.

No `--thinking` value is passed. Pi therefore uses the configured default thinking level unless the model argument carries a suffix such as `:high`.

`run_eval.py` can be run without `--model`. That does not inherit the active caller session. It starts a new Pi process and uses Pi's configured startup default, currently `openai-codex/gpt-5.6-luna` at `high`.

## Detailed finding catalog

### F1. Validator contract is stale

Severity: blocking

Evidence:

- `scripts/quick_validate.py:83` allows only `name`, `description`, `license`, `allowed-tools`, `metadata`, `compatibility`, and `disable-model-invocation`.
- Pi 0.84.4 also supports `when_to_use`, `argument-hint`, `arguments`, `user-invocable`, `disallowed-tools`, `disallowedTools`, `model`, `effort`, `context`, `agent`, `background`, `paths`, `shell`, and `hooks` (`packages/coding-agent/src/core/skills/frontmatter.ts:17-37`). `disallowedTools` is a camelCase alias Pi accepts alongside the hyphenated spelling; the validator must accept both.
- Reproduced: a skill declaring `when_to_use`, `argument-hint`, `model`, `effort`, `context: fork`, `agent`, `background`, and `paths` is rejected with `Unexpected key(s) in SKILL.md frontmatter: agent, argument-hint, background, context, effort, model, paths, when_to_use`.
- A synthetic valid Pi skill containing current fields was rejected by the bundled validator.

Impact:

The creator cannot both adopt current Pi capabilities and pass its own final validation gate.

Required direction:

Update the validator to the current Pi contract and add conformance tests. The validator stays Python: see "Language and distribution decision", which settles this rather than leaving the earlier "prefer Pi's exported parsing where practical" hedge for an implementer to resolve by accident. Its accepted fields and normalization rules are a **tested** copy contract, kept synchronized by the differential test in WP2 rather than by a recorded revision number.

### F2. Benchmark delta can be reversed

Severity: blocking

Evidence:

- `aggregate_results()` derives the primary and baseline configurations from dictionary insertion order.
- Configuration directories are discovered in sorted order.
- The documented edited-skill workspace uses `baseline` and `with_skill`, so `baseline` sorts first.
- Reproduced: a fixture with `baseline` at `0.25` and `with_skill` at `1.00` produced `delta.pass_rate = "-0.75"`, printed under a summary that reads `Baseline: 25.0% pass rate / With Skill: 100.0% pass rate / Delta: -0.75`. The printed summary contradicts itself on its face, which is the only warning a reader gets.

Impact:

A successful skill can be reported as a regression.

Required direction:

Define configuration roles explicitly. Never infer semantic direction from directory order. The benchmark schema should identify `treatment` and `control`, or the aggregator should accept explicit `--treatment` and `--control` names.

### F3. Benchmark metadata is not trustworthy

Severity: blocking

Evidence:

- `aggregate_benchmark.py:267-268` writes `"<model-name>"` placeholders.
- `aggregate_benchmark.py:271` hardcodes `runs_per_configuration` to `3`.
- Token count can fall back to `output_chars`, which is then reported as tokens.

Impact:

The resulting benchmark is not reproducible and can mislabel measurements.

Required direction:

Require complete campaign metadata before aggregation, derive actual run counts, and keep character counts distinct from provider token usage.

### F4. Experimental roles share one model

Severity: high

Evidence:

- `run_loop.py:98` sends `model` to trigger evaluation.
- `run_loop.py:205` sends the same `model` to description generation.

Impact:

The harness cannot independently choose a cheap target-floor consumer and a stronger optimizer. It also cannot distinguish author, executor, grader, comparator, and analyzer models in its records.

Required direction:

Introduce role-specific model and thinking configuration. Do not retain a single overloaded `--model` flag except as a deprecated compatibility alias if compatibility is explicitly required.

### F5. Trigger evaluation changes the skill name

Severity: high

Evidence:

- `run_eval.py:43` creates `eval-skill-<uuid>`.
- Pi exposes both skill name and description in the available-skills listing.

Impact:

The test does not measure the real trigger contract. A meaningful name can improve triggering, while a random name can suppress it.

Required direction:

Preserve the actual skill name. Isolate the candidate skill by controlling discovery rather than renaming it.

### F6. Infrastructure failures become false negatives

Severity: high

Evidence:

- `run_eval.py:71` discards stderr.
- Non-zero process exits are not classified.
- A timeout returns the same `False` value as a legitimate non-trigger.
- Worker exceptions are also converted to `False`.

Impact:

Auth failures, model lookup errors, rate limits, startup errors, project-trust failures, and timeouts lower trigger scores.

Required direction:

Return a structured status per run: `triggered`, `not_triggered`, `timeout`, `process_error`, `model_error`, `auth_error`, or `invalid_output`. Only the first two belong in trigger accuracy. Infrastructure errors should fail or invalidate the campaign.

### F7. Headless print and JSON cannot validate native fork

Severity: blocking for forked skills

Evidence:

- The clean-slate recipe uses `pi -p`.
- Pi's `AgentSession._shouldDegradeFork()` returns `headless mode does not support forking` for print and JSON modes.
- `docs/skills.md` documents the same fallback.

Impact:

A `context: fork` skill can appear to pass while running inline, which is a different execution contract.

Required direction:

Use RPC mode for native fork tests. `ExtensionMode` is `"tui" | "rpc" | "json" | "print"`, and `_shouldDegradeFork()` degrades only on `print` and `json`, so RPC is the headless mode that preserves fork behavior. Keep print or JSON mode only for tests whose claim explicitly excludes fork behavior. The SDK is not an equivalent alternative here: see F37.

### F8. Clean-slate mode disables required extensions

Severity: blocking for extension-dependent skills

Evidence:

The documented clean-slate command includes `--no-extensions`.

Impact:

It cannot test pi-subagents, fork routing, bundled-agent execution, or any skill that declares an extension dependency.

Required direction:

Replace one clean-slate recipe with environment profiles:

1. `in-situ`: real user environment and competing skills.
2. `hermetic-core`: no unrelated extensions, skills, prompts, or context.
3. `declared-dependencies`: hermetic base plus explicitly named required extensions and resources.

Record the selected profile and loaded dependencies in campaign metadata.

### F9. User-invoked skills are trigger-optimized

Severity: high

Evidence:

- The writing doctrine says trigger phrasing does no work for a user-invoked skill.
- The description optimizer always creates a model-visible temporary skill.

Impact:

The optimizer can replace a concise human-facing description with model-trigger prose that will never be used for model invocation.

Required direction:

Skip trigger optimization when effective model visibility is disabled. For a user-invoked skill, validate clarity and list readability instead.

### F10. Optimizer prompt contradicts description doctrine

Severity: high

Evidence:

- `references/writing-principles.md:39` requires third-person, capability-first prose.
- `improve_description.py:128` tells the model to use imperative `Use this skill for` phrasing.

Impact:

The automated optimizer can undo the form required by the creator's own audit and finish gates.

Required direction:

Make the optimizer consume one canonical doctrine source or generate its prompt from a small shared rules artifact. Add tests that prevent the two contracts from diverging.

### F11. The holdout is used for repeated model selection

Severity: high for quantitative claims

Evidence:

`run_loop.py` evaluates the holdout every iteration and chooses the best description by holdout score.

Impact:

The holdout is a validation set. Repeated selection against it overfits campaign decisions, even though its individual failures are hidden from the optimizer prompt.

Required direction:

Use train, validation, and final-test partitions, or iterate on training data and run the held-out test exactly once after selection.

### F12. Bundled agents are not actually embraced

Severity: high

Evidence:

- Agent files have no frontmatter.
- `references/benchmarking.md` permits inline grading.
- No instruction names the exact `subagent_type` or qualified skill-agent identity.

Impact:

Model, thinking, tools, context isolation, and background behavior remain orchestrator guesses.

Required direction:

Make the agent files authoritative and require explicit dispatch by agent type. Keep their bare names in the skill body so Pi's skill-agent rewrite map can qualify them on collisions.

### F13. One analyzer file contains two roles

Severity: medium

Evidence:

`agents/analyzer.md` contains both post-hoc winner/loser analysis and aggregate benchmark-note analysis.

Impact:

The system prompt carries irrelevant instructions for either invocation and risks role bleed.

Required direction:

Split it into `comparison-analyzer.md` and `benchmark-analyzer.md`.

### F14. Fresh context is not fully locked

Severity: medium

Evidence:

The prose asks for fresh subagents, but the agent files omit the fields that make freshness stable across callers.

Impact:

A caller can set `inherit_context: true`, and a different prompt mode can inherit parent instructions. Personal and distribution tests can therefore be contaminated differently.

Required direction:

Evaluator agents should set:

```yaml
prompt_mode: replace
inherit_context: false
skills: false
```

Do not automatically set `isolated: true`: it also removes extension tools that may be required to inspect non-text outputs. Choose extension scope per role.

### F15. No harness regression suite exists

Severity: high

Evidence:

No test files exist for the bundled Python scripts. `uvx ty check scripts/ eval-viewer/` reports seven diagnostics: six in `aggregate_benchmark.py` (lines 214-216, where `run_summary` values are typed as a union including `str` because the `delta` entry shares the dictionary with the per-configuration entries) and one in `run_loop.py:175` (`test_results` subscripted while typed `None`).

Corrected 2026-09-02. The original text attributed these to `run_loop.py` and `quick_validate.py`; `quick_validate.py` is clean and `aggregate_benchmark.py` carries six of the seven. The count was right and the conclusion is unchanged.

Impact:

The reversed delta, stale validator, metadata placeholders, split behavior, and subprocess classification have no automated protection.

Required direction:

Add unit tests before changing implementation behavior. Every corrected defect needs a failing regression test first.

### F16. Review viewer has avoidable safety and reproducibility risks

Severity: medium

Evidence:

- `eval-viewer/generate_review.py` kills any process listening on its preferred port.
- Executor-controlled output is embedded into a JavaScript script block without escaping the `</script>` sequence.
- The viewer loads fonts and SheetJS from external CDNs.

Impact:

The viewer can terminate an unrelated local process, render active content from untrusted outputs, and depend on network availability during supposedly clean local review.

Required direction:

Choose an available port without killing listeners, encode embedded data safely, add a Content Security Policy where practical, and vendor or gracefully omit optional remote assets.

### F17. The documented workspace layout is unreadable by the aggregator, which fails open

Severity: blocking

Found independently by both review passes.

Evidence:

- `references/testing.md:40` documents `.skill-creator/<skill-name>/iteration-N/<eval-name>/{with_skill,baseline}/outputs/`.
- `references/benchmarking.md:21` documents `iteration-N/<eval-name>/`, "one directory per test case, named for what it tests (not `eval-0`)".
- `aggregate_benchmark.py:78` and `:86` discover eval directories with `glob("eval-*")`, which is exactly the naming the prose forbids.
- `aggregate_benchmark.py:105` and `:111` additionally require a `run-*` level holding `grading.json`. The string `run-` appears in no reference file, in `SKILL.md`, or in any agent file.
- Reproduced against the documented layout: `python -m scripts.aggregate_benchmark <ws>/iteration-1 --skill-name demo` prints `No eval directories found`, writes `benchmark.json` and `benchmark.md`, reports `Delta: +0.00`, and exits `0`.
- A second fixture using `eval-1/` but no `run-N/` level printed no warning at all and produced the same zeroed file.
- `eval-viewer/generate_review.py:69-82` keys on an `outputs/` subdirectory and does accept the documented layout, so the two consumers of the same workspace disagree.

Impact:

Every benchmark run by following the skill's own instructions produces a zeroed `benchmark.json` and a `+0.00` delta with a zero exit status. The agent sees a populated viewer beside an empty benchmark and has no signal that the aggregator matched nothing. This is worse than F2: F2 reports a real result with the wrong sign, while F17 manufactures a null result out of no data and presents it as a tie.

Required direction:

**Settled by D1.** The human-readable eval names stay and the aggregator's `eval-*` glob changes to match them; the `run-N` level is real and gets documented. The aggregator must exit non-zero when it discovers no runs rather than emitting a zeroed artifact. The prose and both scripts change together, because they are currently three descriptions of one contract.

### F18. The validator accepts skills Pi refuses to load

Severity: blocking

Evidence:

- `scripts/quick_validate.py:112-113` guards every description check behind `description = frontmatter['description'].strip()` followed by `if description:`, so an empty value skips all of them and the function returns success. `name` has the same shape at `:100-101`.
- Reproduced: a skill whose frontmatter is `name: empty-desc` plus a bare `description:` returns `Skill is valid!` and exit `0`.
- Pi, `packages/coding-agent/docs/skills.md`: "Missing or empty description means the skill is not loaded", and under Validation, "Declared skills with missing descriptions are not loaded."

Impact:

`quick_validate.py` is the Step 8 gate (`SKILL.md`, "Fix and re-run until it passes"). It currently green-lights a skill that Pi drops silently at startup. That is the one failure the validator exists to prevent. The former `.skill` packager also called this validator, but that unsupported distribution path has now been removed.

Required direction:

Presence and non-emptiness are the requirement. The checks must not be conditional on the value being truthy. Fold this into the WP2 parity work with its own fixture.

### F19. The inherited `.skill` packaging path does not belong in the Pi port

Severity: resolved by removal (previously blocking the documented lifecycle)

Evidence:

- `scripts/package_skill.py` was byte-for-byte identical to `vendor/skill-creator/scripts/package_skill.py`, establishing that it was inherited from Anthropic's creator rather than designed for Pi.
- The script created an ordinary ZIP file with a `.skill` suffix. Pi's documented skill inputs are directories and explicit skill paths; the pinned Pi checkout contains no `.skill` archive loader or installer.
- The former `SKILL.md` command used direct script execution and crashed with `ModuleNotFoundError: No module named 'scripts'`; `references/benchmarking.md` used module execution instead.

Impact:

Repairing the command would preserve a distribution artifact Pi cannot consume and would force a packaging exclusion policy solely to keep development files out of that unnecessary archive.

Decision:

The user chose removal rather than repair. `scripts/package_skill.py` and all `.skill` packaging instructions are deleted. The skill directory is the distributable artifact, development tests stay outside it, and WP12 validates installation by copying that directory into a temporary Pi skill root.

### F20. This report's own comparator model cannot resolve in the environments this report requires

Severity: high

Evidence:

- The model policy below proposes `claude-bridge/claude-opus-5` for the blind comparator, justified as "Independent model family reduces same-family judging bias".
- `claude-bridge` is not a built-in Pi provider. It is supplied by the `pi-claude-bridge` extension declared in `~/.pi/agent/settings.json`; no `claude-bridge` file exists under `packages/ai/src/providers/data/`.
- Reproduced: `pi --no-extensions --list-models` yields only `openai-codex`, `openrouter`, and `zai`. Running the documented clean-slate recipe emits `Warning: No models match pattern "claude-bridge/claude-opus-5"`.
- pi-subagents `isolated: true` forces `extensions: false` (README "Frontmatter Fields"), producing the same loss inside an agent.
- pi-subagents resolves an unresolvable `model:` pin by falling back to the parent model: "If nothing resolves, the pin can't run and the agent inherits the parent model."

Impact:

A `comparator.md` pinned to `claude-bridge/claude-opus-5` runs on the parent model in any hermetic environment, which is the same family as the grader. The cross-family independence the pin exists to buy is silently absent, and the comparison still reports a verdict. The report's own requested-versus-effective metadata rule is the only thing that would surface it, which is an argument for that rule rather than a defence of this default.

Required direction:

Pick the comparator model from providers that survive the environment profile in use, or record the profile as a constraint on the model policy. `openrouter/~anthropic/claude-opus-latest` is available without extensions and preserves the cross-family property. Whatever is chosen, an unresolvable pin must fail the campaign rather than degrade it.

### F21. The configuration directory has three names across prose, schema, and viewer

Severity: high

Evidence:

- `references/testing.md:40` and `references/benchmarking.md:25` instruct `baseline/`.
- `references/schemas.md:297`: "`configuration`: Must be `"with_skill"` or `"without_skill"` (the viewer uses this exact string for grouping and color coding)".
- `eval-viewer/viewer.html:716-719` matches `/(with_skill|without_skill|new_skill|old_skill)/` against the run id and hides the badge entirely when nothing matches (`:723`).
- `aggregate_benchmark.py:109` adopts whatever directory name it finds as the config key, which is also the mechanism behind F2.

Impact:

In the human review step the skill calls its priority (`benchmarking.md:64`, "get outputs in front of the human first"), a documented-layout baseline run carries no config badge and no color. The reviewer's feedback, which sets the next iteration's priorities, is gathered without knowing which arm produced each output. That is blind review by accident rather than by design, and it is the opposite of the blind-comparison discipline the skill applies deliberately elsewhere.

Required direction:

**Settled by D2.** `with_skill` and `without_skill`, emitted by the prose and read by both consumers. `baseline`, `new_skill`, and `old_skill` are deleted from the viewer regex and the schema rather than kept as synonyms the aggregator translates.

### F22. The viewer crashes on a state the documented procedure creates

Severity: high

Evidence:

- `eval-viewer/generate_review.py:64`: `runs.sort(key=lambda r: (r.get("eval_id", float("inf")), r["id"]))`. `build_run` initialises `eval_id = None` (`:92`) and always emits the key (`:143`), so the `float("inf")` default is unreachable and a run without `eval_metadata.json` contributes `None`.
- Reproduced on a workspace where one eval directory has metadata and another does not: `TypeError: '<' not supported between instances of 'NoneType' and 'int'`.
- `references/benchmarking.md:26` instructs "Re-create these whenever prompts change; don't assume they carry over between iterations", which is precisely the instruction that yields a partially populated iteration directory.

Impact:

The viewer step dies with a traceback after the runs have been paid for. The launch command at `benchmarking.md:66-68` redirects to `/dev/null` under `nohup`, so the traceback is discarded and the agent observes a server that never came up rather than an error it can act on.

Required direction:

Normalise the missing id to a sortable sentinel before sorting, and stop discarding the viewer's stderr in the documented launch command.

### F23. In-situ trigger evaluation runs in the wrong project

Severity: high

Evidence:

- `scripts/run_eval.py:23-25`: `find_project_root()` returns `Path.cwd()`, which becomes the subprocess cwd at `:72`.
- `references/benchmarking.md:5`: "All `python -m scripts.<name>` commands run from this skill's directory." A `python -m` invocation requires it, so cwd is always the skill-creator's own folder.
- `references/benchmarking.md:52` states the purpose: "Description-trigger optimization stays in-situ: whether a skill fires depends on the competing skills around it, so the real environment is the correct test bed there."
- Pi derives the competing set from cwd: `docs/skills.md` Locations lists `.agents/skills/` in cwd and ancestor directories up to the git root.
- `run_eval.py:58-66` also omits `--no-skills`, so an installed copy of the skill under test competes against its own temporary clone.

Impact:

The one measurement the skill deliberately declines to sterilize is taken in the wrong environment. The resulting trigger rate scores a skill set the user does not have, and `best_description` is written into their frontmatter on that basis.

Required direction:

Separate the evaluation cwd from the module-invocation cwd and make it an explicit campaign parameter recorded in the results.

### F24. The README's usage examples cannot invoke the skill

Severity: high

Evidence:

- `SKILL.md:4` sets `disable-model-invocation: true`. Pi, `docs/skills.md`: such a skill is "excluded from the listing and hidden from model-facing surfaces (including the `skill` tool); still user-invocable via `/skill:name`". The visibility table records `user-invocable-only` as "not listed, `skill` tool rejects it".
- `README.md:32-38` gives three "Good usage" examples, all prose: "Use pi-skill-creator to create a skill called `release-notes-writer`…".
- `README.md:8` says "type `/pi-skill-creator` or name it explicitly", and `README.md:43` repeats "will not fire it unless you name it".
- Confirmed by observation: the skill does not appear in this session's available-skills listing.

Impact:

Naming the skill in prose does nothing, because the model has no listing entry for it and the `skill` tool refuses the name. A user following the README's own examples gets an unassisted model improvising the workflow, with nothing indicating the skill never loaded. Only `/pi-skill-creator` or `/skill:pi-skill-creator` reaches it.

Required direction:

The README's invocation guidance and all three examples use the command form that resolves. This belongs with the other README corrections in WP11.

### F25. The grading contract is written in Claude Code's vocabulary

Severity: high

Evidence:

- `references/schemas.md:112-114`, `:170-176` and `agents/grader.md:126`, `:137` key tool histograms on `Read`, `Write`, `Bash`, `Edit`, `Glob`, `Grep`.
- Pi's registered tool names are lowercase: `bash`, `edit`, `find`, `grep`, `ls`, `read`, `write`. `Glob` is not a Pi tool: `docs/skills.md` Tool Name Redirects lists `Glob` to `find` as a correction error, stating "the mapped tool is never executed and no aliases exist".
- `agents/grader.md:16` declares `transcript_path` as "Path to the execution transcript (markdown file)". pi-subagents writes a JSON-lines transcript at `<os-tmpdir>/pi-subagents-<uid>/<cwd>/<session>/tasks/<agent-id>.output`.

Impact:

A grader following this schema searches Pi transcripts for tool names that never occur, and emits a histogram keyed on a vocabulary no downstream consumer matches. The declared input format is wrong, so the grader does not know what it is reading or where to find it. This compounds F28: the fields would be zero even if the names were right.

Required direction:

Re-key the metric schema and the grader's example evidence to Pi's tool names, and state the real transcript format and location. Fold into WP4.

### F26. The premise behind the entire clean-slate branch is false

Severity: high

Evidence:

- `references/testing.md:49`: "Subagents dispatched in-session inherit the harness and the user's global instructions and cannot be sterilized; use the subprocess route in benchmarking.md."
- pi-subagents contradicts each clause. `prompt_mode: replace` is the default and means "body is the full system prompt (no AGENTS.md / CLAUDE.md inheritance)". `isolated: true` "forces `extensions: false` + `skills: false` + drops `ext:` selectors. Only built-in tools." `isolation: worktree` supplies the clean working directory `testing.md:39` separately demands.
- "Frontmatter is authoritative. If an agent file sets `model`, `thinking`, `max_turns`, `inherit_context`, `run_in_background`, `isolated`, or `isolation`, those values are locked for that agent."

Impact:

The load-bearing justification for routing all distribution-grade testing through the subprocess recipe is wrong, and the recipe it routes to is the one `README.md` itself flags as never executed under Pi. An agent following this skill will never reach for the cheap, in-harness, actually-available sterilization the extension provides. F14's required direction already prescribes those fields for a different reason, which makes the contradiction internal as well as external.

Required direction:

**Settled by D6.** Three named profiles replace the split: `in-situ`, `hermetic-core` (an isolated in-harness subagent), and `declared-dependencies`. The subprocess route stops being the default clean environment and is reserved for claims that need a separate process, which today means fork fidelity over RPC. The "cannot be sterilized" sentence is deleted rather than softened.

### F27. The authoring doctrine predates Pi's skill surface

Severity: high

Evidence:

Absent from every `.md` and `.py` in the skill: `when_to_use`, `argument-hint`, `arguments`, `user-invocable`, `disallowed-tools`, `context: fork`, `agent`, `background`, `paths`, `shell`, `${PI_SKILL_DIR}`, the `/skill:name` invocation form, and the listing budget. Pi supports all of them (`docs/skills.md`), along with the argument grammar (`$ARGUMENTS`, `$N`, declared names) and `` !`command` `` shell injection.

Three places where the gap bites the doctrine's own arguments:

- `writing-principles.md:42` argues "All 'when to use' information lives here, not in the body" without knowing Pi has a `when_to_use` field that is exactly that.
- `writing-principles.md:12-14` builds an "invocation and the two loads" economics section without mentioning that Pi measures the listing budget and reports each skill's estimated cost in the `/skills` overlay.
- `writing-principles.md:63` reasons about disclosure depth without the `paths` listing boost or `context: fork`. Its own reference idiom is also wrong under Pi: a skill-local link must be written `@${PI_SKILL_DIR}/references/x.md` to resolve, and a bare `@references/x.md` is left as written.

Impact:

A skill authored by following this one is confined to `name`, `description`, and `disable-model-invocation`: no arguments, no per-invocation model or effort, no tool restriction, no fork execution, no path boost, and reference links in the form Pi does not resolve. The skill teaches skill authoring, so this defect propagates to everything it produces.

Required direction:

A doctrine section covering the frontmatter and rendering surface Pi offers, keyed to which failure class each field addresses rather than enumerated as a feature list. Note the negative result already recorded in `README.md`: a static drafting-doctrine section did not improve floor robustness. This one is different in kind because it supplies capability rather than advice, but it should ship with the same skepticism.

### F28. Two consumed artifacts have no producer

Severity: medium

Evidence:

- `agents/grader.md:63-65` reads `{outputs_dir}/user_notes.md`; `:103` reads `{outputs_dir}/metrics.json`. `references/schemas.md:165` calls `metrics.json` "Output from the executor agent".
- There is no executor agent. `agents/` holds only `grader.md`, `comparator.md`, and `analyzer.md`, and `benchmarking.md:25` tells the executor dispatch only where to save outputs.
- `aggregate_benchmark.py:151-156` reads `execution_metrics` for `tool_calls`, `tokens` (falling back to `output_chars`, per F3) and `errors`, all defaulting to `0`.

Impact:

`execution_metrics` in every `grading.json`, and `tool_calls` and `errors` in every `benchmark.json` run entry, are structurally always zero. `benchmarking.md:63` then asks the analyst to reason about time and token trade-offs from those fields.

Required direction:

**Settled by D5.** Neither. The fields are populated by parsing the pi-subagents transcript, which already carries the tool-call histogram, full token accounting, and cost. No executor agent is added, and the grader stops expecting `metrics.json` and `user_notes.md` to exist.

### F29. `assertions` and `expectations` name the same thing

Severity: medium

Evidence:

`references/benchmarking.md` uses "assertion" throughout, including in the artifact contract at `:26` (`eval_id`, `eval_name`, `prompt`, `assertions`). `references/schemas.md` and `agents/grader.md` use "expectations", and that is the key both consumers read: `aggregate_benchmark.py:159` reads `grading.get("expectations", [])`. `writing-principles.md:116` forbids exactly this: "Consistent terminology: one term per concept, everywhere".

Impact:

An agent that follows the surrounding prose's vocabulary writes `assertions` into `grading.json`, and the aggregator silently reports zero graded items per run. The one sentence that saves it (`benchmarking.md:59`, naming the exact fields) works by accident rather than by contract.

Required direction:

**Settled by D3.** `expectations`, the key both consumers already read. `assertions` disappears from `benchmarking.md`.

### F30. The review viewer instructs the user to switch products

Severity: medium

Evidence:

`eval-viewer/viewer.html:548`: "When done, copy feedback and paste into Claude Code." `eval-viewer/viewer.html:637`: "Go back to your Claude Code session and tell Claude you're done reviewing."

Impact:

These are the two strings the human reads in the browser at the exact moment the skill hands them control. Beyond naming the wrong product, "copy feedback and paste" contradicts `benchmarking.md:72`, where "Submit All Reviews" writes `feedback.json` for the agent to read.

Required direction:

Port both strings to Pi and to the `feedback.json` flow the skill actually uses. Fold into WP10.

### F31. `schemas.md` is mis-placed and partly stale

Severity: medium

Evidence:

- `SKILL.md:8-11` lists three reference files and `schemas.md` is not among them. Its only inbound link is `references/benchmarking.md:5`, making the chain `SKILL.md` to `benchmarking.md` to `schemas.md`. `writing-principles.md:63` forbids this: "One level deep. Every reference file links directly from SKILL.md."
- `schemas.md:221` locates `benchmark.json` at `benchmarks/<timestamp>/benchmark.json`; `benchmarking.md:62` and `aggregate_benchmark.py:405` put it at `<workspace>/iteration-N/benchmark.json`.
- `schemas.md:41-57` documents `history.json` for an "Improve mode" that appears nowhere else in the skill, with fields no script writes or reads.

Impact:

The file the prose treats as authoritative on the machine contract sits at the depth its own doctrine says loses information, and carries a wrong path for the artifact it is most often consulted about.

Required direction:

Promote it to a direct pointer from `SKILL.md` or fold the field contracts into `benchmarking.md`; correct the path and drop the orphaned schema. WP3 already owns this file.

### F32. `VIEWER_PID` cannot survive to the step that uses it

Severity: medium

Evidence:

`references/benchmarking.md:66-71` captures `VIEWER_PID=$!` in one bash block, and `:78` uses it in a later step ("Read `feedback.json` when the user says they're done, then `kill $VIEWER_PID`"). Pi's bash tool spawns a fresh shell per call (`packages/coding-agent/src/core/tools/bash.ts:130`), so no variable carries between tool calls.

Impact:

The kill step runs with `$VIEWER_PID` unset, typically many turns later after a human review. The viewer's HTTP server is left running for the rest of the session, which then collides with the next campaign's `_kill_port` (F16) and gives that defect something to hit.

Required direction:

Persist the PID outside the shell in a file the later step reads.

### F33. The recipe warns about a Pi configuration tier that does not exist

Severity: medium

Evidence:

`references/benchmarking.md:50`: "Managed/policy-level instructions still load and cannot be excluded — record them in the benchmark metadata if present." Pi documents global (`~/.pi/agent/settings.json`) and project (`.pi/settings.json`) scopes only; `docs/settings.md` and `docs/security.md` contain no managed or enterprise layer. This is a Claude Code carry-over.

Impact:

The instruction asks the agent to record something with no referent, and "cannot be excluded" implies an irreducible contamination floor the scrubbed profile does not actually have.

Required direction:

Drop the clause or replace it with whatever Pi genuinely loads unconditionally under a scrubbed `PI_CODING_AGENT_DIR`.

### F34. "Nothing auto-loads under the scrubbed profile" is wrong for `--skill`

Severity: medium

Evidence:

`references/benchmarking.md:48`: "`--skill` exposes only the skill under test, and the prompt names its path and says to read SKILL.md and follow it (nothing auto-loads under the scrubbed profile)." Under Pi a `--skill`-loaded skill is a normal model-visible skill: its description joins the system-prompt listing every turn, and the `skill` tool can invoke it. Reproduced: the documented recipe, run with `--no-approve` and `--no-skills`, lists the `--skill` skill by name.

Impact:

The recipe overrides the trigger dimension by hand, so the clean-slate pass rate is measured under a delivery path no real user takes, and the stated reason for doing so is a false premise. Note the adjacent good news, also reproduced: `--skill` does survive `--no-approve` and `--no-skills`, so the with-skill arm does load.

Required direction:

State what `--skill` does under Pi, and decide deliberately whether the benchmark should force a read or let the listing trigger it. The two measure different things.

### F35. The testing method never names the mechanisms it runs on

Severity: medium

Evidence:

`SKILL.md:26`, `testing.md:32`, `testing.md:55` and `benchmarking.md:25` describe dispatching fresh subagents, reading transcripts, and spawning every run in one turn, without naming a single concrete mechanism. pi-subagents supplies all of them: the `Agent` and `SubagentWorkflow` tools; `inherit_context` defaulting to `false`; the JSON-lines transcript at `<os-tmpdir>/pi-subagents-<uid>/<cwd>/<session>/tasks/<agent-id>.output`; and `<total_tokens>` and `<duration_ms>` in the completion notification, which is exactly what `schemas.md:203` tells the agent to capture.

Impact:

The instruction the whole iteration loop rests on — read the transcript, not the output — gives an executing agent no way to find a transcript under Pi. In practice it reads the subagent's returned summary, which pi-subagents itself warns against: "an agent's summary describes intent, not outcome".

Required direction:

Name the tools and the transcript path, and state the parameters that implement the hygiene rules the doctrine already demands. Pairs with F27 and F26 as one doctrine-grounding package.

### F36. Assorted lower-severity defects

Severity: low

Each is small, individually cheap, and evidenced:

- `aggregate_benchmark.py:271-286` never emits `eval_name`, though `schemas.md:295` calls it the viewer's section header and `viewer.html:1204` reads it. Benchmark sections fall back to "Eval 1", discarding the descriptive naming `benchmarking.md:21` asks for. The aggregator already opens `eval_metadata.json` at `:88`.
- `scripts/generate_report.py:209` calls `max(history, ...)` with no empty guard and raises `ValueError` on `{"history": []}`. `run_loop` always supplies a non-empty history, so the exposure is limited to the undocumented standalone CLI at `:288-311`. `generate_report` is named in no reference file.
- `benchmarking.md:41-45` documents `run_loop`'s invocation without `--report` (defaulting to `auto`, which writes a live HTML file to the temp directory and calls `webbrowser.open`) or `--results-dir`, which is the only way to persist `results.json`, `report.html`, and the per-iteration improvement transcripts. A browser opens unannounced and the campaign's audit trail is discarded by default.
- `SKILL.md:3`'s own description is imperative ("Create, improve, and test agent skills"), which `writing-principles.md:39` forbids in favour of third person. `SKILL.md:99` makes it a checkable gate. Minor because the skill is model-hidden and the description is human-facing, but it is the worked example of the rule it enforces on others.
- The scripts use PEP 604 unions in evaluated annotations (`run_eval.py:29`, `improve_description.py:36`, `generate_review.py:85`), requiring Python 3.10 or newer. `README.md:55` states only "zero-dependency (Python 3 standard library only)", and `writing-principles.md:131` requires stating dependencies.
- `run_eval.py:58-66` passes the query as the argument after `-p`. Pi's parser (`packages/coding-agent/src/cli/args.ts:157-162`) drops an argument starting with `@` or `-`, so a trigger query in those forms is never sent and returns a non-trigger the loop then optimizes against. `benchmarking.md:37` explicitly asks for queries with file paths and casual phrasing.

Required direction:

Fold each into the work package that already owns its file. None justifies its own package.

### F37. The recommended fork-test route names the option that does not work

Severity: high

The second defect this report contained about its own proposal, after F20.

Evidence:

- The original recommendation read "Use a TypeScript Pi SDK or RPC harness for Pi-native behavioral tests, especially forked skills", naming the SDK first and treating the two as interchangeable.
- They are not interchangeable on the question that matters. `ExtensionMode` is `"tui" | "rpc" | "json" | "print"` (`packages/coding-agent/src/core/extensions/types.ts:307`), and `_shouldDegradeFork()` degrades only on `print` and `json` (`agent-session.ts:2723`). RPC mode sets `mode: "rpc"` (`modes/rpc/rpc-mode.ts:331`), so it preserves fork behavior.
- `AgentSession._extensionMode` defaults to `"print"` (`agent-session.ts:546`) and changes only when a caller invokes `bindExtensions({ mode })` (`agent-session.ts:4643`). An SDK harness that creates a session and never binds extensions therefore runs in `print` mode and degrades forks exactly like `pi -p`, which is the failure F7 exists to avoid.
- The two routes also differ in cost, which the original wording hid. RPC mode is "headless operation via a JSON protocol over stdin/stdout" (`docs/rpc.md`), so it is a subprocess the existing Python can drive, with no dependency and no new language. The SDK route requires depending on `@earendil-works/pi-coding-agent`, which ends the skill's zero-dependency property.
- The SDK route carries a further hazard. The published package is upstream Pi, not this fork. pi-subagents' skill-bundled agents ride on the fork's A.9 skill-set seam, and its README states that "under upstream pi with no A.9 seam, the feature is silently inert: zero skill agents, no diagnostics." A harness pinned to the registry would test a Pi that cannot perform the behavior under test, and would report zero agents rather than an error.

Impact:

An implementer following the original bullet takes the expensive route, loses the zero-dependency property, and still does not get fork fidelity unless they independently discover the `bindExtensions` requirement. If they also install from the registry rather than the local fork, bundled-agent tests report a clean zero instead of failing.

Required direction:

RPC mode is the route for fork-fidelity tests, driven from the existing Python subprocess machinery. The SDK is reserved for a need RPC cannot serve — in-process inspection of session internals, or many sessions in one process — and if that need arises it must resolve against the local fork and bind a non-`print` extension mode explicitly. WP8 was rewritten accordingly.

### Checked and found correct

Recorded so a later pass does not re-derive them:

- Every CLI flag in the clean-slate recipe exists with the stated meaning (`packages/coding-agent/src/cli/args.ts`), and `--skill` survives both `--no-approve` and `--no-skills`.
- `PI_CODING_AGENT_DIR` is the correct variable, and the `auth.json` premise is right: Pi has no keychain path, and credentials live at `<agentDir>/auth.json` mode 0600.
- "Pi has no `--bare` mode" is correct.
- `run_eval.py`'s trigger detection is sound in principle: `tool_execution_start` carrying `toolName` and `args` is a real Pi JSON event, and the `skill` tool takes `{name, args?}`.
- `schemas.md`'s timing-capture claim is right: `<total_tokens>` and `<duration_ms>` exist only in the completion notification.
- The zero-dependency claim holds; all seven remaining Python modules import the standard library only.
- `quick_validate.py` and `utils.py` handle CRLF frontmatter correctly, because `Path.read_text()` applies universal newlines.
- `LICENSE.txt` is the full unmodified Apache License 2.0, consistent with the provenance note in `README.md`.
- The bundled-agent defaults table above was re-checked field by field against pi-subagents 0.19.0 and is accurate, including `backgroundByDefault` defaulting to `true`.
- The workflow determinism constraints in WP9 are exact: `Date.now()`, `Math.random()` and argless `new Date()` throw, and the sandbox blocks filesystem, network, and module access.
- The Pi SDK symbols named in the runner section all exist: `ModelRuntime.create()`, `resolveCliModel()`, `createAgentSession()`, `SessionManager.inMemory()`, `DefaultResourceLoader`, and `await session.shutdown()`.
- pi-subagents cross-extension protocol version is `3`, advertising `capabilities: { skillAgents: true }`.
- Skill-local workflows are indeed not discovered by name: the saved-workflow roots are `.pi/workflows/`, `.agents/workflows/`, and `<agent dir>/workflows/`.

## Target model policy

Model selection must be role-based. The executor model is part of the experiment and must not be locked in an executor agent file.

### Provisional defaults

These are implementation defaults to calibrate under Pi, not claims that the current repository has already benchmarked them.

| Role | Provisional model | Thinking | Reason |
|---|---|---|---|
| Creator and orchestrator | `openai-codex/gpt-5.6-sol` | `high` | High-judgment requirements extraction, drafting, and iteration |
| Grader | `openai-codex/gpt-5.6-sol` | `high` | Evidence-heavy assertion evaluation and claim verification |
| Blind comparator | `openrouter/~anthropic/claude-opus-latest` | `high` | Independent model family reduces same-family judging bias, and this provider survives `--no-extensions` and `isolated: true` (see F20) |
| Comparison analyzer | `openai-codex/gpt-5.6-sol` | `high` | Causal synthesis across skills and transcripts |
| Benchmark analyzer | `openai-codex/gpt-5.6-terra` | `medium` | Structured pattern analysis over already aggregated data |
| Trigger consumer | Campaign-selected executor floor | Campaign-selected | Trigger behavior is model-specific |
| Skill executor | Campaign-selected executor floor | Campaign-selected | This is the primary experimental variable |

A model pin is only as good as the environment it runs in. Every model named above must be checked against the environment profile the role runs under: `claude-bridge` and any other extension-supplied provider disappears under `--no-extensions` and under `isolated: true`, and pi-subagents answers an unresolvable pin by inheriting the parent model rather than failing. The comparator row was changed for exactly this reason after review (F20). Treat "does this pin resolve under this profile" as part of the campaign preflight, not as a runtime surprise.

Before making permanent model claims, run a small calibration campaign that compares the proposed judge models on frozen artifacts with a pre-registered grading key.

### Required metadata

Every run record must distinguish requested and effective values:

```json
{
  "role": "grader",
  "requested_model": "openai-codex/gpt-5.6-sol",
  "effective_model": "openai-codex/gpt-5.6-sol",
  "requested_thinking": "high",
  "effective_thinking": "high"
}
```

Use the effective values for benchmark labels. Pi and pi-subagents can clamp thinking or resolve fuzzy model names to another provider or version.

## Proposed bundled-agent frontmatter

These examples define the intended controls. Agents implementing this work may adjust tool scopes when tests prove a capability is required.

### `grader.md`

```yaml
---
name: grader
description: Grades one skill execution against explicit assertions and verifies output claims with cited evidence.
model: openai-codex/gpt-5.6-sol
thinking: high
prompt_mode: replace
inherit_context: false
run_in_background: true
skills: false
persist_session: false
output_transcript: true
max_turns: 24
color: blue
---
```

### `comparator.md`

```yaml
---
name: comparator
description: Blindly compares two skill-produced outputs against the same task and returns a decisive evidence-backed verdict.
model: openrouter/~anthropic/claude-opus-latest
thinking: high
prompt_mode: replace
inherit_context: false
run_in_background: true
skills: false
persist_session: false
output_transcript: true
max_turns: 20
color: purple
---
```

### `comparison-analyzer.md`

```yaml
---
name: comparison-analyzer
description: Unblinds a completed comparison and identifies causal, generalizable improvements for the losing skill.
model: openai-codex/gpt-5.6-sol
thinking: high
prompt_mode: replace
inherit_context: false
run_in_background: false
skills: false
persist_session: false
output_transcript: true
max_turns: 24
color: cyan
---
```

### `benchmark-analyzer.md`

```yaml
---
name: benchmark-analyzer
description: Finds assertion, variance, cost, and failure patterns hidden by aggregate benchmark metrics.
model: openai-codex/gpt-5.6-terra
thinking: medium
prompt_mode: replace
inherit_context: false
run_in_background: false
skills: false
persist_session: false
output_transcript: true
max_turns: 16
color: cyan
---
```

Do not use camelCase agent frontmatter. pi-subagents reads `persist_session`, `output_transcript`, `inherit_context`, `run_in_background`, `prompt_mode`, and `max_turns`.

## Target execution architecture

### Interactive lifecycle

Keep `pi-skill-creator` user-invoked and inline. Add `model` and `effort` to its frontmatter only after the Pi-native author-model calibration confirms the proposed default.

The main skill remains responsible for:

- User interviews and consequential decisions.
- Showing baseline failures and outputs.
- Obtaining approval before edits.
- Obtaining explicit approval before a multi-agent workflow.
- Applying accepted description or skill edits.

### Qualitative test dispatch

For a small, known set of examples, use direct parallel `Agent` calls. Every executor call must specify:

- A fresh agent instance.
- The exact executor model and thinking level.
- `inherit_context: false` or an executor agent definition that locks it.
- The task-local working directory.
- The output directory.
- Whether the run is baseline, snapshot, or treatment.

Do not pin a static model in the executor agent definition. The executor floor varies by skill.

### Quantitative benchmark workflow

Add a workflow script under the skill folder, for example:

```text
workflows/benchmark.js
```

Invoke it through `SubagentWorkflow.scriptPath` using the absolute path derived from `${PI_SKILL_DIR}`. Skill-local workflows are not discovered by name from the normal `.pi/workflows` and `.agents/workflows` roots.

The workflow should:

1. Accept campaign configuration through `args`.
2. Fan out treatment and control executor runs.
3. Pipeline each completed executor into a grader.
4. Use small structured-output schemas where useful.
5. Filter and report `null` workflow results explicitly.
6. Run deterministic validators with `gate` rather than ask a model whether validation passed.
7. Return a compact campaign summary and paths to durable results.
8. Record any bounded coverage or dropped run.

Use `pipeline()` for executor-to-grader flow. Use `parallel()` only where a downstream step needs all prior results together, such as a cross-result synthesis.

The workflow is optional machinery. The skill must obtain explicit user approval before invoking multi-agent orchestration.

### Pi-native behavioral runner

Rewritten 2026-09-02. The original text said "Create a TypeScript runner … Prefer the SDK when running in-process and RPC when process isolation is required", which chose on the wrong axis and recommended the route that does not deliver fork fidelity. See F37.

**Default: RPC mode, driven from the existing Python.** `pi --mode rpc` is headless operation over a JSON-lines protocol on stdin and stdout. It adds no dependency, introduces no new language, and reuses the subprocess machinery `run_eval.py` already has. Critically, it is the headless mode that preserves fork behavior: `_shouldDegradeFork()` degrades on `print` and `json` only.

The RPC runner should:

- Spawn `pi --mode rpc` with explicit `--model` (accepting the `provider/id:thinking` form) and `--no-session` unless persistence is part of the claim.
- Speak strict JSONL: split records on `\n` only, and never use a reader that also splits on `U+2028` or `U+2029`, both of which are legal inside JSON strings.
- Correlate commands and responses through the optional `id` field.
- Capture tool calls, final messages, usage, diagnostics, errors, and the effective model identity from the event stream rather than echoing the requested values.
- Load pi-subagents through the declared-dependencies profile when bundled-agent or fork behavior is under test.

**The TypeScript SDK is not the default and needs a reason.** It costs a dependency on `@earendil-works/pi-coding-agent` and ends the skill's zero-dependency property. Reach for it only when something genuinely needs in-process access, such as inspecting session internals or running many sessions in one process. If that day comes, two constraints are not optional:

- Resolve against **this fork**, not the published package. The registry ships upstream Pi, which has no A.9 skill-set seam, so pi-subagents' skill-bundled agents are silently inert there and a test would report zero agents rather than fail.
- Call `session.bindExtensions({ mode: "rpc" })` or equivalent. `_extensionMode` defaults to `"print"`, so an unbound SDK session degrades forks exactly like `pi -p`.

The SDK surface itself is sound where it is needed: `ModelRuntime.create()`, `resolveCliModel()`, `createAgentSession()` with `SessionManager.inMemory()`, a controlled `DefaultResourceLoader`, a shared event bus for pi-subagents, explicit `model` and `thinkingLevel`, and `await session.shutdown()` for complete extension lifecycle cleanup.

Do not use print or JSON mode for a test whose acceptance criteria include native skill fork behavior.

## Work packages

Each package below is intended to be independently assignable. An agent must read this report, the named files, and the relevant Pi or pi-subagents sources before editing. Every package uses behavioral tests first.

### WP1. Establish the harness regression suite

Priority: P0
Dependencies: none

Owned files:

- New tests and fixtures under the project-level `tests/pi-skill-creator/`, outside the distributable skill directory.
- Minimal test configuration required to run them.

Tasks:

1. Add fixtures for valid and invalid Pi skill frontmatter.
2. Add a fixture with baseline and treatment benchmark results.
3. Add subprocess-result fixtures for trigger, non-trigger, timeout, and process error.
4. Add train, validation, and final-test split fixtures.
5. Add a single documented command that runs the full harness test suite.
6. Add workspace fixtures in both the documented layout and the aggregator's `eval-*`/`run-*` layout, so F17 is testable from either side of the contract.
7. Add an empty-`description` and empty-`name` skill fixture for F18.

Required tests:

- Current valid Pi frontmatter fixture fails before WP2 and passes afterward.
- Current reversed-delta fixture demonstrates `-0.75` before WP3 and `+0.75` afterward.
- A workspace in the documented layout produces a non-zero exit before WP3 lands, rather than a zeroed `benchmark.json`.
- An empty-description skill is rejected before WP2 lands.
- Tests run without network or model credentials. The only test permitted an external prerequisite is WP2's differential drift test, which needs a Pi source checkout and must skip with an explicit message when it is absent rather than fail.
- The distributable `skills/pi-skill-creator/` directory contains no test files or fixtures.

Completion criterion:

The current defects are captured by failing tests, and the test runner itself passes for unaffected behavior.

### WP2. Bring validation into Pi 0.84.4 parity

Priority: P0
Dependencies: WP1

Owned files:

- `scripts/quick_validate.py`
- `scripts/utils.py` if shared parsing changes are needed
- Validator fixtures and tests, including the differential drift test against Pi's own loader
- `references/schemas.md` if its frontmatter contract is documented there

Tasks:

1. Support every current Pi skill frontmatter field.
2. Match Pi's boolean forms and name rules.
3. Preserve unknown fields as Pi does, or document and test any intentionally stricter validation policy.
4. Validate `context`, `background`, model and effort shape, tool lists, and compatibility limits.
5. Handle multiline YAML without silently changing values.
6. Add the differential drift test, which replaces the versioned contract note the earlier draft proposed. Run every validator fixture through both `quick_validate.py` and Pi's own loader (`loadSkillsFromDir()`, publicly exported, returning `{ skills, diagnostics }`), and assert the two verdicts agree per fixture. Resolve Pi's source from a configurable path with a sensible default, and skip the test with an explicit message when it is absent, so a machine without the Pi checkout still runs the rest of the suite. Record the Pi revision the corpus was last reconciled against as test output, not as a comment.
7. Make presence and non-emptiness unconditional for `name` and `description` (F18). The current checks sit behind a truthiness guard that skips them exactly when they matter.
8. Accept `disallowedTools` alongside `disallowed-tools` (F1).

Required tests:

- Valid inline skill.
- Valid user-invoked skill.
- Valid `context: fork` skill with bundled agent.
- Valid `model`, `effort`, `paths`, `arguments`, and `disallowed-tools` forms.
- Invalid context value.
- Invalid boolean value.
- Missing description, empty description, whitespace-only description, and the same three for `name`. Each must fail; today the empty cases pass.
- Both spellings of the disallowed-tools key.
- BOM and multiline frontmatter.
- The differential test agrees with Pi's loader on every fixture above, and skips with an explicit message rather than failing when Pi's source is absent.
- Introducing a field Pi accepts but the validator does not fails the differential test, which is the drift this test exists to catch.

Completion criterion:

Every supported Pi 0.84.4 frontmatter fixture has the same accept, normalize, or diagnostic outcome as Pi for the fields the validator claims to enforce, no skill Pi would refuse to load passes the validator, and a future divergence from Pi's contract surfaces as a failing test rather than as silence.

### WP3. Correct benchmark aggregation and metadata

Priority: P0
Dependencies: WP1

Owned files:

- `scripts/aggregate_benchmark.py`
- `references/schemas.md`
- `references/benchmarking.md`
- Aggregation tests and fixtures

Tasks:

1. Make treatment and control roles explicit.
2. Calculate delta as treatment minus control.
3. Derive run counts from actual data.
4. Require model and thinking metadata.
5. Separate provider tokens from character counts.
6. Validate that every expected eval/configuration pair has the required repetitions.
7. Refuse aggregation on incomplete or mixed campaign metadata.
8. Implement D1's layout: keep the human-readable eval names, change the aggregator's `eval-*` glob to match them, and document the `run-N` level in the prose. The aggregator must exit non-zero when it discovers no runs instead of emitting a zeroed artifact.
9. Implement D2's configuration name: `with_skill` and `without_skill`, emitted by the prose and read by both the aggregator and the viewer's badge regex.
10. Carry `eval_name` through from `eval_metadata.json` into the emitted runs (F36).
11. Implement D5: populate `execution_metrics` by parsing the pi-subagents transcript rather than reading a file no producer writes. Capture the tool-call histogram, the full `usage` record, and `cost`. The transcript parser is shared with WP8 — agree its module and signature with that package before either writes it.
12. Correct `references/schemas.md` (F31): the `benchmark.json` path, the orphaned `history.json` schema, and the `assertions`/`expectations` split (F29). Promote it to a direct pointer from `SKILL.md` or fold its field contracts into `benchmarking.md`.

Required tests:

- Baseline 0.25 and treatment 1.00 yields `+0.75`.
- Reversed directory names do not alter the result.
- Uneven repetition counts are reported or rejected.
- Missing model metadata fails clearly.
- Character counts never appear under a token field.
- Markdown and JSON reports agree.
- A workspace built exactly as the prose instructs aggregates its runs; no layout the prose can produce yields a silent zero.
- Discovering no runs exits non-zero and writes no benchmark artifact.
- The emitted `configuration` value is the one the viewer's badge regex matches, verified against the viewer rather than against the schema prose.
- `eval_name` survives from `eval_metadata.json` into `benchmark.json`.

Completion criterion:

A benchmark cannot be emitted with ambiguous configuration direction, placeholder models, fabricated run counts, or no underlying runs at all.

### WP4. Split and configure bundled agents

Priority: P1
Dependencies: none for file restructuring; WP1 for regression coverage

Owned files:

- `agents/grader.md`
- `agents/comparator.md`
- `agents/analyzer.md`
- New `agents/comparison-analyzer.md`
- New `agents/benchmark-analyzer.md`
- `SKILL.md`
- `references/benchmarking.md`

Tasks:

1. Add explicit frontmatter to every bundled agent.
2. Split the two analyzer roles.
3. Lock fresh context with `prompt_mode: replace` and `inherit_context: false`.
4. Set role-specific model, thinking, background, session, transcript, turn, skill, and tool policy.
5. Replace optional inline grading with explicit dispatch instructions.
6. Name exact agent types in the skill body so Pi's rewrite-map seam can qualify collisions.
7. Preserve blind comparator isolation from treatment identity.
8. Re-key the grading contract to Pi's tool vocabulary (F25): lowercase `bash`, `edit`, `find`, `grep`, `ls`, `read`, `write`, with `Glob` removed rather than translated. Correct the grader's declared transcript format and location to pi-subagents' JSON-lines `.output` file.
9. Verify each proposed `model:` pin resolves under the environment profile its role runs in (F20). An extension-supplied provider is unavailable to an `isolated: true` agent, and pi-subagents answers an unresolvable pin by inheriting the parent model.
10. Implement D5 on the grader side: stop expecting `metrics.json` and `user_notes.md`, and take `execution_metrics` from the transcript parser WP3 builds. No executor agent is added.

Required tests:

- pi-subagents discovers all four agents from a skill-set snapshot.
- Each agent resolves to the expected effective frontmatter.
- Bare alias dispatch works when free.
- Qualified dispatch works when a user agent collides with the bare name.
- The comparator prompt receives no treatment identity.
- `inherit_context: true` from a caller cannot override the locked agent configuration.
- Every pinned model resolves under its role's environment profile, and an unresolvable pin fails rather than silently inheriting the parent model.
- The grader's tool histogram is keyed on names that actually appear in a Pi transcript.

Completion criterion:

Every specialist invocation runs through its bundled agent definition with known model, thinking, context, and background behavior.

### WP5. Introduce role-specific model configuration

Priority: P1
Dependencies: WP1, WP3

Owned files:

- `scripts/run_eval.py`
- `scripts/run_loop.py`
- `scripts/improve_description.py`
- Campaign schema and documentation

Tasks:

1. Replace overloaded `--model` with explicit role fields.
2. Add thinking-level fields.
3. Resolve and record canonical effective model identifiers.
4. Make executor model and thinking mandatory for quantitative runs.
5. Read current `PI_PROVIDER`, `PI_MODEL`, and `PI_REASONING_LEVEL` only as explicit defaults, never as unrecorded behavior.
6. Add a second-family confirmation option for shareable claims.
7. Prevent agent frontmatter pins from being silently reported as caller-selected models.

Required tests:

- Trigger evaluator and optimizer receive different configured models.
- Missing executor model fails before spending model calls.
- Requested and effective values remain distinct.
- Unsupported thinking is recorded after clamping.
- Standalone execution never claims to inherit the caller session without evidence.

Completion criterion:

Every model-consuming role is explicit, reproducible, and present in campaign output.

### WP6. Make trigger evaluation reliable

Priority: P1
Dependencies: WP1, WP5

Owned files:

- `scripts/run_eval.py`
- Trigger result schema
- Trigger evaluator tests

Tasks:

1. Preserve the real skill name.
2. Isolate the candidate from any discovered copy of the target skill.
3. Capture stderr and process exit status.
4. Parse complete JSON event lines and final authoritative messages.
5. Distinguish legitimate non-trigger from infrastructure failure.
6. Add bounded retry policy for explicitly retryable provider failures.
7. Make timeout an invalid run, not a negative trigger result.
8. Record Pi version, model, thinking, environment profile, and competing skill set.
9. Avoid UUID-induced treatment differences where deterministic unique paths suffice.
10. Separate the evaluation working directory from the module-invocation directory (F23). Today both are the skill's own folder, so the competing skill set is the one surrounding `pi-skill-creator` rather than the one surrounding the skill under test. Make it an explicit campaign parameter and record it.
11. Pass the query so Pi cannot swallow it (F36): a query beginning with `@` or `-` is dropped by Pi's argument parser and returns a false non-trigger.

Required tests:

- Skill-tool invocation is detected.
- Direct SKILL.md read fallback is detected where applicable.
- Completed non-trigger is classified correctly.
- Timeout, malformed JSON, auth error, and non-zero exit are not counted as non-triggers.
- Real skill name appears in the listing fixture.
- A discovered duplicate target skill cannot contaminate the result.
- The evaluation directory is the configured one, not the directory the module was invoked from.
- Queries beginning with `@` and `-` reach the model.

Completion criterion:

Trigger accuracy is computed only from valid model responses against the real skill identity.

### WP7. Correct description optimization methodology

Priority: P1
Dependencies: WP1, WP5, WP6

Owned files:

- `scripts/run_loop.py`
- `scripts/improve_description.py`
- `references/writing-principles.md`
- `references/benchmarking.md`
- Description-loop tests

Tasks:

1. Skip model-trigger optimization for model-hidden skills.
2. Align the optimizer prompt with the canonical capability-first doctrine.
3. Replace train/test with train/validation/final-test semantics.
4. Run the final test once after candidate selection.
5. Keep test failures hidden from the optimizer.
6. Validate minimum class counts before splitting.
7. Define deterministic tie-breaking among descriptions.
8. Record every candidate and partition score without exposing final-test details during iteration.

Required tests:

- User-invoked skill skips trigger optimization.
- Optimizer prompt requires third-person capability-first form.
- Final-test data is evaluated exactly once.
- One-item classes fail with a useful split error.
- Fixed seed reproduces train and validation membership.
- Tie-breaking is deterministic.

Completion criterion:

The loop cannot optimize a non-existent trigger or select candidates repeatedly against its final test set.

### WP8. Add RPC-mode behavioral execution

Priority: P1

Dependencies: WP1, WP5. **Sequence after WP13.** The fork half of this package tests a capability the skill cannot currently author: `context: fork` appears nowhere in it (F27), so there is no forked skill to test until WP13 makes one reachable. Building the fork tester first is machinery ahead of its trigger.

Rewritten 2026-09-02, previously "Add Pi-native behavioral execution". The original scoped a TypeScript SDK runner as the default; F37 records why that is the wrong default. The work is smaller than it looked: RPC mode is a subprocess speaking JSON lines, so this extends the existing Python rather than introducing a language.

Owned files:

- `scripts/run_eval.py` or a sibling module sharing its subprocess machinery
- Its unit and integration tests
- `references/testing.md`
- `references/benchmarking.md`

Tasks:

1. Add an RPC-mode runner: spawn `pi --mode rpc`, write commands as JSON lines to stdin, read events from stdout, and correlate through the optional `id` field.
2. Split records on `\n` only. Node `readline` and any reader that also splits on `U+2028` or `U+2029` is not protocol-compliant, and Python's default line iteration has the same hazard for those code points inside JSON strings.
3. Pass model and thinking explicitly, accepting the `provider/id:thinking` form, and use `--no-session` unless persistence is part of the claim.
4. Capture tool calls, final messages, diagnostics, usage, and the effective model identity from the event stream rather than echoing the requested values.
5. Add a declared-dependencies profile that can load pi-subagents.
6. Exercise `context: fork` under RPC, which is the headless mode that does not degrade it.
7. Escalate to the TypeScript SDK only on a demonstrated need RPC cannot serve. If that happens, resolve against this fork rather than the published package, and bind a non-`print` extension mode explicitly (F37).
8. Implement D6's three environment profiles — `in-situ`, `hermetic-core`, `declared-dependencies` — and delete `references/testing.md:49`'s "cannot be sterilized" claim rather than softening it. `hermetic-core` is an in-harness subagent with `prompt_mode: replace` and `isolated: true`, plus `isolation: worktree` when the run writes files; the subprocess route is reserved for claims needing a separate process. Every campaign record names its profile, and records from different profiles are never aggregated together.
9. Correct the recipe's two false claims while in `benchmarking.md`: the non-existent managed-policy tier (F33) and "nothing auto-loads" for `--skill` (F34). Record the reproduced positive result too: `--skill` does survive `--no-approve` and `--no-skills`.

Required tests:

- Inline skill executes under the requested model.
- Forked skill dispatches a bundled agent through pi-subagents protocol v3.
- Background and foreground fork behavior are distinguishable.
- Missing pi-subagents produces the documented inline-degradation diagnostic.
- Declared dependencies load while unrelated extensions remain absent.
- Effective model and thinking are captured from execution, not copied from input.
- An `isolated: true` subagent demonstrably sees no AGENTS.md, no extensions, and no inherited skills, which is the measurement that settles F26 rather than arguing it.

Completion criterion:

The harness can prove native Pi inline, fork, bundled-agent, and model-override behavior without relying on `pi -p` semantics that disable those capabilities, and it does so without adding a dependency or a second language.

### WP9. Add deterministic benchmark workflow

Priority: P2
Dependencies: WP3, WP4, WP5, WP8

Owned files:

- New `workflows/benchmark.js`
- Workflow contract tests
- `SKILL.md`
- `references/benchmarking.md`

Tasks:

1. Define a pure-literal workflow `meta` block.
2. Accept campaign inputs through `args`.
3. Pipeline executor results into graders.
4. Use role-specific agent types, models, and effort.
5. Use `gate` for deterministic output validation.
6. Use small structured-output schemas and handle `null` results.
7. Report dropped, skipped, failed, and replayed calls.
8. Return durable result paths and a concise summary.
9. Require explicit user approval before invocation.

Required tests:

- Workflow parses under pi-subagents.
- Example campaign fans out expected treatment and control calls.
- Grading starts per item without an unnecessary global barrier.
- Gate failure marks the item failed.
- Schema failure becomes an explicit missing result.
- Resume journal replays an unchanged prefix.
- No `Date.now()`, `Math.random()`, argless `new Date()`, filesystem API, or network API appears in the workflow script.

Completion criterion:

A benchmark campaign has deterministic orchestration, bounded concurrency, inspectable progress, and explicit failure accounting.

### WP10. Harden the review viewer

Priority: P2
Dependencies: WP1

Owned files:

- `eval-viewer/generate_review.py`
- `eval-viewer/viewer.html`
- `assets/eval_review.html`
- Viewer tests

Tasks:

1. Stop killing the process occupying the preferred port.
2. Bind an available loopback port.
3. Escape embedded JSON against script termination.
4. Treat artifact text as text, not executable HTML.
5. Remove or vendor remote dependencies, or provide a tested offline fallback.
6. Validate feedback payload size and shape.
7. Preserve static-viewer behavior.
8. Fix the missing-`eval_id` sort crash (F22): `build_run` always emits the key as `None`, so the `float("inf")` default never applies and a partially populated iteration directory raises `TypeError`. Stop discarding the viewer's stderr in the documented launch command, which currently hides the traceback.
9. Port the two Claude Code strings in `viewer.html` (F30) to Pi and to the `feedback.json` flow the skill actually uses.
10. Persist the viewer PID outside the shell (F32). Pi spawns a fresh shell per bash call, so `VIEWER_PID` is always unset by the time the documented kill step runs.

Required tests:

- Occupied preferred port remains alive while viewer selects another port.
- Artifact containing `</script><script>...` cannot execute.
- HTML, Markdown, JSON, image, PDF, and spreadsheet fixtures render or degrade safely.
- Static feedback download remains valid JSON.
- Server feedback writes only to the configured workspace file.
- A workspace mixing eval directories with and without `eval_metadata.json` renders instead of raising.
- No user-facing string names a product other than Pi.

Completion criterion:

Reviewing untrusted executor output cannot terminate unrelated processes or inject active script into the viewer.

### WP11. Re-run Pi-native calibration and update claims

Priority: P2
Dependencies: WP2 through WP10 as applicable

Owned files:

- `README.md`
- New campaign records under the project-level `.skill-creator/` workspace, outside the distributable skill directory
- Model defaults in agent and skill frontmatter if calibration supports them

Tasks:

1. Pre-register a small model-calibration plan.
2. Compare proposed grader and comparator models on frozen artifacts.
3. Run create, improve, pressure, trigger, and fork scenarios under Pi.
4. Record exact provider/model identifiers and effective thinking levels.
5. Separate prior Claude Code evidence from Pi evidence.
6. Update or remove claims that the Pi runs do not support.
7. Decide whether `SKILL.md` should pin the creator model and effort.
8. Correct the README's invocation guidance and all three "Good usage" examples (F24). A `disable-model-invocation: true` skill cannot be reached by naming it in prose; only `/pi-skill-creator` or `/skill:pi-skill-creator` resolves.
9. State the Python floor alongside the zero-dependency claim (F36): the scripts require 3.10 or newer for PEP 604 unions in evaluated annotations.

Required tests:

- Every reported number links to a complete campaign record.
- Every flagged deterministic grading failure is manually re-read.
- Pi version, pi-subagents version, environment profile, models, thinking, prompts, and repetitions are recorded.
- Claims distinguish in-situ, hermetic-core, and declared-dependencies environments.
- Every invocation form printed in the README actually fires the skill.

Completion criterion:

The README's live recommendations and model pins are supported by Pi-native evidence rather than inherited Claude Code results.

### WP12. Validate directory distribution and finish cleanup

Priority: P2
Dependencies: all selected work packages

Owned files:

- Directory-boundary and installation smoke tests under `tests/pi-skill-creator/`
- `README.md` distribution guidance
- This report

Tasks:

1. Treat `skills/pi-skill-creator/` as the complete distributable artifact; do not build a second archive representation.
2. Keep tests, eval fixtures, campaign records, temporary reports, and implementation handoffs outside the skill directory.
3. Confirm bundled agents, runtime references, Python helpers, viewer assets, and the approved workflow remain inside the skill directory.
4. Copy the directory into a temporary Pi-owned skill root and run the real loader plus the standalone validator against that copy.
5. Run the complete offline regression suite and the directory-install smoke test.
6. Verify that no runtime documentation references `.skill` archives or the deleted `package_skill.py`.
7. Keep this report and its work orders beside the skill, never inside it.

Required tests:

- The source skill directory contains every required runtime file and no tests, fixtures, campaign records, caches, or implementation handoffs.
- A byte-for-byte copied directory validates and loads in Pi.
- Bundled agents register from the copied directory.
- Every runtime command printed by the skill works from its documented directory.
- Repository checks find no `.skill` archive instruction or packaging helper under `skills/pi-skill-creator/`.

Completion criterion:

The copied skill directory is self-contained, zero-dependency, loadable by Pi, and free of development-only material.

### WP13. Ground the authoring and testing doctrine on Pi

Priority: P1

Dependencies: the two halves sit on opposite sides of WP8. The **drafting half** depends on nothing and should run early, because it is what makes `context: fork` authorable and therefore gates WP8's fork work. The **sterilization half** waits on WP8, whose measurement of an isolated subagent settles what `testing.md` should say. Split the package along that line rather than treating it as one unit.

Added by the 2026-09-02 review. The twelve packages above repair the harness; this one repairs what the skill teaches. It is separated because it changes prose rather than code, and because its defects propagate: this skill authors other skills, so a doctrine that predates Pi produces Pi-blind skills indefinitely.

Owned files:

- `references/writing-principles.md`
- `references/testing.md`
- `references/benchmarking.md`
- `SKILL.md`

Tasks:

1. Add the Pi frontmatter and rendering surface to the drafting doctrine (F27), keyed to which failure class each field addresses rather than enumerated as a feature list: `when_to_use`, `arguments` and the argument grammar, `argument-hint`, `user-invocable`, `allowed-tools` and `disallowed-tools`, `model` and `effort`, `context: fork` with `agent` and `background`, `paths`, `shell`, and the `${PI_SKILL_DIR}` reference idiom.
2. Reconcile the three doctrine passages the missing fields undercut: the "when to use" argument that `when_to_use` already answers, the invocation economics section that omits Pi's measurable listing budget, and the disclosure-depth reasoning that predates `paths` and `context: fork`.
3. Correct the skill-local reference idiom throughout: `@${PI_SKILL_DIR}/references/x.md` resolves and a bare `@references/x.md` does not.
4. Rewrite the sterilization claim in `testing.md` (F26) on the outcome of WP8's measurement.
5. Name the mechanisms the method depends on (F35): the `Agent` and `SubagentWorkflow` tools, `inherit_context`, the JSON-lines transcript path, and the completion notification's `total_tokens` and `duration_ms`.
6. Fix the skill's own description to obey its own doctrine (F36), or state the user-invoked exemption in the doctrine and apply it consistently.

Required tests:

This package changes prose, so its evidence is behavioral rather than unit-level. Per the skill's own rule, an edited skill is tested against its pre-edit snapshot:

- Snapshot the current skill, then run the create branch against both versions on a task whose target skill genuinely needs arguments or a tool restriction. The post-edit artifact should use the field; the snapshot's should not.
- A forward-test artifact's skill-local references resolve under Pi rather than being left as written.
- A forward-test at the executor floor still passes, confirming the added doctrine did not displace working guidance.
- Carry the negative result already on record: a previous drafting-doctrine section measured as a tie. If this one measures as a tie on artifact quality, keep only the parts that supply capability the author could not otherwise reach, and say so.

Completion criterion:

A skill authored by following this one can reach every Pi frontmatter field its task calls for, and every mechanism claim in the testing doctrine is true of Pi 0.84.4 and pi-subagents 0.19.0.

## Dependency graph

```text
WP1 regression suite
├── WP2 validator parity
├── WP3 benchmark correctness
├── WP4 bundled agents
├── WP5 role-specific models
│   ├── WP6 trigger reliability
│   │   └── WP7 optimizer methodology
│   └── WP13 doctrine grounding (drafting half; also reachable without WP1)
│       └── WP8 RPC-mode runner
│           ├── WP9 benchmark workflow
│           └── WP13 doctrine grounding (sterilization half)
└── WP10 viewer hardening

WP13 doctrine grounding (drafting half)   independent of WP1, and it gates WP8's fork work

WP2..WP10, WP13 selected scope
└── WP11 Pi-native calibration
    └── WP12 directory distribution and cleanup
```

**Land the remaining lifecycle breaks first.** F17 and F18 each break a documented step outright rather than degrading it. F19 has already been resolved by removing the unsupported `.skill` archive path. Fixing F17 and F18 before broader work means the rest proceeds on a harness whose validator and aggregator at least enforce real inputs.

**The waves below are a dependency order, not a work partition.** Per D8, a wave may only run packages in parallel once each shared prose file has one owner in that wave. As drawn, wave 1 fails that test: `references/benchmarking.md` is contended by WP3, WP4, and WP13, `references/schemas.md` by WP2 and WP3, and `SKILL.md` by WP4 and WP13. Assigning those owners is the last step before the work orders are written, and it may move a task between packages.

Safe initial parallel wave after WP1 establishes fixtures:

- WP2 validator parity
- WP3 benchmark correctness
- WP4 bundled-agent split and frontmatter
- WP10 viewer hardening
- WP13 drafting half, which touches only prose and collides with nothing above

Second wave:

- WP5 role-specific models
- WP6 trigger reliability

Third wave:

- WP7 optimizer methodology
- WP8 RPC-mode runner, now that WP13's drafting half has made `context: fork` something the skill can author

Fourth wave, both gated on WP8:

- WP9 benchmark workflow
- WP13 sterilization half, once WP8 has measured what an isolated subagent actually sees

Final wave:

- WP11 calibration
- WP12 directory distribution and cleanup

## Cross-package testing expectations

Changes that depend on Pi or pi-subagents behavior must cite and test the exact seam rather than copy assumptions.

For Pi skill behavior, verify against:

- `packages/coding-agent/src/core/skills/frontmatter.ts`
- `packages/coding-agent/src/core/skills/render.ts`
- `packages/coding-agent/src/core/skills/runtime.ts`
- `packages/coding-agent/src/core/skills/skill-fork.ts`
- `packages/coding-agent/src/core/agent-session.ts`, in particular `_shouldDegradeFork()` and `bindExtensions()`
- `packages/coding-agent/src/core/extensions/types.ts` for the `ExtensionMode` union
- `packages/coding-agent/src/modes/rpc/rpc-mode.ts` and `packages/coding-agent/docs/rpc.md` for the RPC protocol and its framing rules

For pi-subagents behavior, verify against:

- `src/agent-dir-loader.ts`
- `src/agent-types.ts`
- `src/invocation-config.ts`
- `src/model-resolver.ts`
- `src/skill-agents.ts`
- `src/skill-agents-adapter.ts`
- `src/cross-extension-rpc.ts`
- `src/workflow/`

Do not modify sibling repositories as part of a skill work package unless a failing cross-package test proves the required capability is absent and the user approves that expanded scope.

## Global acceptance criteria

The adoption effort is complete only when all selected claims below are backed by executable evidence:

- A created skill can use every supported Pi frontmatter field without failing validation.
- Bundled agents register and dispatch by bare and qualified names.
- Each specialist runs with a recorded effective model, thinking level, context policy, and background policy.
- Executor-floor runs cannot silently use the parent model.
- Forked skills are tested as forked skills, not through headless inline degradation.
- Treatment deltas always have explicit direction.
- Infrastructure failures never count as behavioral failures.
- Final-test data is not reused for iterative selection.
- Quantitative reports contain no placeholders or fabricated run counts.
- Every harness script has offline regression coverage.
- Review output is safe to open locally.
- The distributed skill directory includes every runtime resource and excludes development artifacts.
- A byte-for-byte copy of the skill directory loads in Pi: no custom archive, npm dependency, companion extension, or maintainer-only import path.
- The validator's agreement with Pi's contract is asserted by a test, so drift fails rather than accumulates.
- README claims distinguish historical Claude Code evidence from new Pi-native evidence.

Added by the 2026-09-02 review:

- Every command the skill prints runs from the directory the skill says to run it in.
- No documented procedure produces a workspace its own tools cannot read, and no tool reports a result when it found no data.
- The validator refuses every skill Pi would refuse to load.
- Every model pin resolves under the environment profile its role runs in, and an unresolvable pin fails the campaign instead of inheriting the parent model.
- One term per concept and one string per identifier across prose, schema, scripts, and viewer.
- Every claim the skill makes about Pi or pi-subagents is true of the pinned revisions, and every mechanism the method relies on is named where the executing agent will read it.
- No user-facing string names a product other than Pi.

## Known non-goals

- Do not make `pi-skill-creator` model-invoked. Its cost and human decision gates justify user invocation.
- Do not pin one executor model for all target skills.
- Do not use `context: fork` merely because Pi supports it.
- Do not require workflows for a single trivial eval.
- Do not preserve the current Python API or file layout unless a real external consumer requires compatibility.
- Do not restore `.skill` packaging, port any shipped script to TypeScript, add an npm dependency, or split a companion extension out beside the skill. The install model is a copied folder; "Language and distribution decision" records the evidence and the conditions that could reopen it.
- Do not claim one model is best before the calibration package is complete.

# Handoff: hardening the testing process, on an underspecified-authoring test bed

**For**: a fresh session (likely a fresh project) whose first job is to grill this document with the user and produce a concrete experiment plan. Nothing here is a finished design; section 6 lists the decisions deliberately left open.

**Priority ordering (deliberate)**: the primary objective is the process hardening in section 2b, because it improves the *products* (every skill authored from then on). The discovery-gap measurement and the creator-vs-parents comparison are the campaign's instrument and its secondary outputs, not its point.

**Date**: 2026-08-06. **Author**: the session that built and eval-tested `skills/pi-skill-creator` (session records referenced below).

---

## 1. One-paragraph context

`skills/pi-skill-creator` is a skill-creation skill merged from four sources (Anthropic's skill-creator, writing-great-skills, superpowers' writing-skills, codex-skill-creator). It was eval-tested through four in-session iterations, two pre-registered clean-slate producer pilots, one distribution test, and one feature A/B (all summarized in the skill's `README.md`, raw records in `pi-skill-creator-workspace/` at the repo root). The pilots left exactly one first-order question unanswered, and it is the most important one: **does the skill's process advantage convert into a measurable artifact advantage on authoring tasks where the knowledge is not handed to the author?** This campaign exists to answer that.

## 2. Why this question survived everything we ran

Every authoring eval so far was *fully specified*: the producer prompt enumerated the complete convention set, so authoring reduced to transcription plus elaboration. Consequences, all measured:

- Strong-author pilot (Fable authors, Haiku consumers): all four creator skills **and the no-skill control** tied at 5.00/5. On transcription-class tasks, a strong model needs no creator skill. (Pilot 1 table in the skill README.)
- Weak-author pilot (Haiku authors): treatments separated (pi-skill-creator uniquely clean at 5.00/5, parents 3.50 to 4.50, control artifacts invalid). Real, but nobody authors on Haiku in practice.
- Feature A/B (floor-drafting doctrine): negative result. Static doctrine saturates with a strong author; residual defects were task-specific semantic traps that only floor-tier forward-tests catch.

The one thing with-skill runs did at every tier that baselines never did: **process** (baseline runs before drafting, forward-tests, snapshots, audits). On fully-specified tasks that process produced evidence but no output delta. The untested hypothesis: on tasks where correct content must be *discovered or induced*, process is the only path to correct content, so the output delta should appear at the strong-author tier, which is the tier real users author on.

If the hypothesis fails there too, the honest conclusion is that pi-skill-creator's value is evidence and regression protection only, and the README should say so even more bluntly. Either result is publishable.

## 2b. The primary objective: fix the testing process itself

The testing/benchmarking process the skill inherited (largely from Anthropic's skill-creator) is, on this session's evidence, a *verification* process wearing the name of a *testing* process. It reliably confirms the skill does what its author imagined; it has almost no machinery for finding what the author did not imagine. Three structural gaps, each observed live:

1. **The eval author is the skill author.** Eval prompts and assertions are written by the same agent and session that wrote the skill, from the same example distribution, so skill and evals co-evolve and share blind spots (one audit run caught itself building a worked example out of its own test prompt).
2. **No adversarial input generation.** The one consumer-breaking defect found this session (a rule saying "every column alias is snake_case" that literal readers extended to renaming source columns) survived every self-generated eval and fell only to an externally designed trap input. Nothing in the encoded process would ever construct that trap. Superpowers' pressure scenarios are adversarial, but only for discipline skills.
3. **Test consumers are gentler than deployment consumers.** Attentive in-session forward-test subagents passed an artifact that a single-pass `claude -p` consumer immediately exposed. (Partially patched already via the executor-floor wiring.)

The proposed treatment, shaped by this session's clearest meta-finding (doctrine additions failed their A/B; process-wiring additions all changed behavior): two structurally independent steps added to the skill's test loop, both cheap, both A/B-testable:

- **Spec-blind eval generation**: a fresh subagent that has read only the captured intent from Step 1 (never the draft) writes the eval prompts and expected behaviors. Restores independence between test and implementation.
- **Red-team input generation**: a fresh subagent that reads the *draft skill* with the instruction to construct inputs a literal, single-pass reader of these rules would get wrong, with expected correct behavior pre-registered from the spec, not the skill. This automates exactly the manual step that caught the alias-renaming defect.

The underspecified-authoring fixture (sections 3 and 5) is the test bed that can measure whether these steps work: arms with and without the wiring, graded on planted-knowledge coverage and floor-consumer effectiveness. That gives the campaign double duty: it measures the discovery gap and it validates the fix in the same runs.

## 3. The three candidate eval families

1. **Discovery-heavy**: "make a skill for querying our analytics database" against a fixture repo containing schemas, docs, and code with *planted knowledge* (join paths, a mandatory filter like "exclude test accounts", a gotcha column, a deprecated table that looks current). Gradable: does the authored skill capture each planted item (coverage key), and do floor-tier consumers using the skill answer fixture questions correctly?
2. **Induction-from-examples**: "make a skill that writes release emails the way I like them" plus a folder of N past examples embodying unstated conventions (structure, tone, a rule like "breaking changes always get their own paragraph before highlights"). Gradable: convention-recovery rate against the pre-registered list of conventions the examples embody.
3. **Behavior-shaped**: "make a skill that stops agents from doing X" where the correct content can only come from observing baseline agent behavior (the exact thing Step 2 forces and no baseline arm ever does). Gradable: pressure-scenario compliance of consumers with the authored skill.

Family 1 is the primary candidate (closest to real usage, most objectively gradable). Families 2 and 3 are follow-ups or grill fodder.

## 4. Established harness facts (do not rediscover these)

Mechanics that work, with sources in this repo:

- **Clean-slate execution**: `CLAUDE_CONFIG_DIR=<scrubbed-profile> claude -p "..." --model <id> [--add-dir <skill>]`. The scrubbed profile needs only `.credentials.json` (export: `security find-generic-password -s 'Claude Code-credentials' -w`, macOS) and a copy of `~/.claude.json`. **Do not use `--bare`**: it breaks credential discovery. Verify a profile with a probe for a distinctive global rule (expected answer: "none"). Full recipe: `skills/pi-skill-creator/references/benchmarking.md`.
- **Producer runs need `--dangerously-skip-permissions`** (they write files and spawn subagents) and their own per-run profile copy (concurrent runs sharing one profile race on the state file). Producer transcripts land inside each run profile under `projects/.../*.jsonl`; that is where you verify process claims (baseline-before-draft ordering, which files were read).
- **Parallel batches**: a jobs file plus `xargs -n2 -P6 runner.sh`, one background task per batch. Runner scripts from this session are in the session scratchpad (`pilot/producer-*.sh`, `pilot/consumer-one.sh`, `pilot/grade.py`) and are trivial to recreate from the patterns in the workspace records.
- **Deterministic grading with mandatory manual reads**. Pre-register assertions before any run exists. Expect the grader itself to need iterations: in pilot 1, three grader revisions were needed and *every* non-baseline "failure" was a grader parsing artifact; in pilot 2 the failures were real. The rule that catches this: manually read every flagged run before believing it, and when the failure pattern moves after a grader fix, re-read everything newly flagged.
- **Assertion tiers**: prompt-contract assertions (from the user's stated requirements, valid for every artifact) vs artifact-contract assertions (from each artifact's own documented choices, generated per artifact at grading time). Conflating them caused this session's one major grading error (documented in the README's method section).

Known contamination traps, all observed live:

- In-repo baselines read the vendored skill-writing doctrine (`skills/writing-skills/...`) when unhurried; a cwd anchor in the prompt does not stop them. In-session subagents cannot be environment-isolated at all (they inherit harness and global CLAUDE.md). Only the `claude -p` scrubbed-profile route is clean.
- Test subjects notice sibling `baseline/` fixtures and infer they are in a harness. Keep control copies and grading keys outside any path the subject can reach.
- The user's global CLAUDE.md leaks useful behavior into subagents (date-fetching rules, emoji bans) and biases baselines upward. Bias direction matters: contamination that helps the baseline understates the treatment lift (tolerable); contamination that helps the treatment invalidates it.
- Ceiling effects: before funding an A/B, confirm the control arm actually fails somewhere. The floor-doctrine A/B was nearly doomed by this; it was saved by moving to the untested pressure branch.

Cost calibration from this session: a Fable full-loop producer run (spawns its own baselines and forward-tests) takes roughly 10 to 20 minutes headless; Haiku consumer runs take under a minute; the 33-run consumer batch at parallelism 6 finished in a few minutes. The two pilots plus the A/B totaled roughly 60 producer/consumer subprocess runs plus about 40 in-session subagents.

## 5. Sketch of the campaign (to be grilled, not executed as-is)

- Build a fixture project (plausible small analytics codebase: schema files, a docs page, seed data, a few queries in code) with a pre-registered **planted-knowledge key** (roughly 8 to 12 items spanning: a mandatory filter, a join path, a naming trap, a deprecated-but-present table, a business definition like "active user"). Key lives outside the fixture.
- Producer prompt: underspecified by design ("make a skill for querying our analytics data; put it at ./skills/"), pointed at the fixture as cwd. Producers clean-slate, strong model (Fable), P reps per treatment.
- Treatments: minimum pi-skill-creator vs no-skill control. Whether to re-run all four parents is an open decision (section 6).
- Grading, two layers: (a) **coverage**: which planted items appear in the authored skill (script plus manual read against the key); (b) **consumer effectiveness**: floor-tier consumers use each authored skill to answer fixture questions whose correct answers depend on planted items ("how many active users in March?" is wrong unless the test-account filter is applied). Layer (b) is the one that resists gaming and measures what users care about.
- Pre-register everything before the first producer run: the key, the assertions, the consumer questions with expected answers, and the decision rule (what delta ships what claim).

## 6. Open decisions for the planning session to grill

0. **The treatment design (top priority, from section 2b)**: are spec-blind eval generation and red-team input generation two steps or one; where do they sit in the loop (after the draft, before iteration); what exactly does the red-teamer receive (draft only? draft plus spec?); how is contamination between the red-teamer and the forward-test consumers prevented; and what is the A/B (current loop vs loop-with-wiring, same fixture, same graded outcomes)? Note the asymmetry with the failed floor-doctrine A/B: these are process steps, not prose, and process wiring is the intervention class that has worked every time this session.
1. **Fixture realism vs cost**: how big must the fixture be before discovery is "real"? A 10-file toy may let baselines stumble on everything; a 200-file repo raises authoring cost per rep. What is the smallest fixture where baseline coverage plausibly drops below ~50%?
2. **Does the producer get subagents?** Full-loop pi-skill-creator spawns its own test agents. In `claude -p` they are available; decide whether the control arm's prompt should mention testing at all, or stay strictly naturalistic.
3. **Treatments**: pi vs control only (cheapest, answers the headline claim), or the full 5-way (answers "better than parents" on the class that matters, at roughly 2.5x cost)?
4. **Reps and power**: coverage rates are per-item binomials across P reps; with 10 planted items and P=3, arm-level coverage differences of ~20 points are visible. Is that the effect size worth detecting, or does the user want finer?
5. **Consumer questions**: how many, which floor (Haiku only, or Haiku plus Sonnet to measure masking), and how to grade free-form answers deterministically (expected-value strings vs a grader agent with the key).
6. **What result changes what**: pre-commit the interpretations. Example: pi wins coverage and consumer accuracy -> README gains the discovery claim; tie on coverage but pi wins consumer accuracy -> the skill's value is in how knowledge is *encoded*, not found; full tie -> README states the limitation and the skill's pitch narrows to regression protection and evidence.
7. **Family 2 and 3**: in scope for this campaign or explicitly deferred?
8. **Where the campaign lives**: fresh repo (cleanest: no vendored doctrine for baselines to read, solving the in-repo contamination trap structurally) vs this repo (reuses harness paths). The fresh-project instinct in the user's request is probably right; decide what minimal harness files to copy over.

## 7. Pointers

- Skill under test: `skills/pi-skill-creator` (commits `fcd3709`, `ea1e5a0`, `c1fdb7a`, `84536ac`).
- Eval summary and honest caveats: `skills/pi-skill-creator/README.md`.
- Raw records: `pi-skill-creator-workspace/` (iterations 1 to 4) at this repo's root; pilot artifacts and runner scripts in the originating session's scratchpad (ephemeral; treat the workspace and README as the durable record).
- Testing doctrine to follow while testing (hygiene, environment fidelity, manual-read rule): `skills/pi-skill-creator/references/testing.md` and `references/benchmarking.md`. The campaign should eat this cooking; deviations are findings about the doctrine.

## 8. Definition of done for the planning session

A written plan containing: the treatment design for the two test-loop wiring steps (section 2b) and their A/B arms; the chosen eval family and fixture spec with its planted-knowledge key; pre-registered assertions and consumer questions; treatments, rep counts and budget; the decision rule tying each outcome to a concrete README/skill change (including the wiring's ship/no-ship criterion); and the run schedule. Only then run producers.

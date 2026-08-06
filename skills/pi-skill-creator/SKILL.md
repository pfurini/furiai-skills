---
name: pi-skill-creator
description: Create, improve, and test agent skills — the full lifecycle from intent and baseline through drafting, forward-testing, and optional quantitative benchmarking.
disable-model-invocation: true
---

A skill exists to wrangle determinism out of a stochastic system. **Predictability** — the agent taking the same _process_ every run, not producing the same output — is the root virtue; every step below serves it.

Reference files, loaded when a step points at them:

- [references/writing-principles.md](references/writing-principles.md) — the standard all skill prose is judged against: invocation economics, description doctrine, information hierarchy, leading words, failure modes, pruning.
- [references/testing.md](references/testing.md) — baseline and forward-test procedure, pressure scenarios, closing loopholes.
- [references/benchmarking.md](references/benchmarking.md) — the quantitative branch: eval harness, review viewer, blind comparison, description-trigger optimization, packaging.

Two branches:

- **Creating a new skill** → run the steps in order.
- **Improving an existing skill** → start at the [Audit](#audit--improving-an-existing-skill) at the bottom of this file, then join Step 2 with the current version as the baseline.

The steps are the default path, not a straitjacket. When the user shortcuts ("skip the tests, just draft it"), comply — but name what was skipped, because an untested skill is a guess about agent behaviour, not knowledge of it.

## Step 1 — Understand

Capture what the skill must do before writing anything. The conversation may already contain the workflow (the user says "turn this into a skill"): extract the tools used, the step sequence, the corrections the user made, the input/output formats — then have the user confirm the gaps rather than re-interviewing from zero.

Establish, asking the most important questions first rather than all at once:

1. The capability, stated in one sentence.
2. The **branches** — each distinct way the skill will be invoked — with a realistic example prompt per branch: real file names, real phrasing, the kind of thing the user would actually type.
3. The **invocation choice**: model-invoked (the agent can fire it; its description occupies context every turn) or user-invoked (only the human can fire it; zero context cost, but the human must remember it exists). Pick model-invocation only when the agent must reach the skill on its own, or another skill must.
4. Where the skill will live.

Done when: the user has confirmed the capability sentence, one example prompt per branch, and the invocation choice.

## Step 2 — Baseline

Run the example prompts _without_ the skill before writing it. Dispatch one fresh subagent per example prompt, worded exactly as a user would word it (hygiene rules in [references/testing.md](references/testing.md)), and read the transcripts — not just the outputs.

Document verbatim where each run diverges from what the user wants: wrong approach, missed constraint, re-derived knowledge, reinvented boilerplate, rationalized shortcut. These failures are the skill's reason to exist; the draft will address them and nothing else.

If no run diverges, stop and tell the user: the model already does this by default, and a skill would pay context to say nothing. (A skill whose value is bundled scripts, schemas, or assets still shows divergence — the baseline runs re-derive or fumble exactly what the bundle would provide.)

Done when: every example prompt has a failure list quoted from its transcript, and the user has seen it.

## Step 3 — Plan the contents

Map what the skill needs onto files, driven by the baseline failures:

- **Steps vs. reference**: ordered actions the agent performs go in SKILL.md as steps; definitions, rules, schemas, and examples consulted on demand are reference — inline if every branch needs them, disclosed to a `references/` file behind a pointer if only some branches do.
- **`scripts/`** — code the baseline runs kept rewriting. Write it once, deterministic and tested.
- **`references/`** — knowledge the baseline runs kept re-discovering (schemas, API shapes, policies).
- **`assets/`** — files the output is built from (templates, boilerplate, fonts), never loaded into context.

Nothing else goes in: no README, CHANGELOG, setup guides, or notes about the creation process. The skill contains only what the executing agent needs.

Done when: there is a file plan, and every documented baseline failure has a place in it that addresses it.

## Step 4 — Draft

Read [references/writing-principles.md](references/writing-principles.md) now, before writing any prose — it defines the description doctrine, how to match the guidance form to the failure class you observed in Step 2, and the failure modes the draft must not ship with.

Then:

1. Build the bundled resources first (`scripts/`, `references/`, `assets/`). Run every script you write; a bundled script that fails on first use poisons trust in the whole skill.
2. Write the SKILL.md body: imperative form, each step ending on a checkable completion criterion, reference material placed per the information hierarchy.
3. Write the frontmatter description last, when you know exactly what the skill is: the capability in one clause, then one trigger per branch — never a summary of the workflow.
4. Reread the draft with fresh eyes and prune: every sentence that fails the no-op test ("does this change behaviour versus the default?") is deleted, not trimmed.

Done when: every baseline failure from Step 2 maps to a specific line, script, or reference in the draft, and the pruning pass has run.

## Step 5 — Forward-test

Run the same example prompts _with_ the skill, using fresh subagents that don't know they are testing anything — the prompt is `Use <skill> at <path> to <task>`, never "review this skill". Pass raw artifacts, not your diagnosis; a test that only passes because the subagent saw your conclusions is contamination, not evidence. Full procedure and hygiene rules: [references/testing.md](references/testing.md).

Compare each transcript against its baseline. If the skill enforces a discipline (a rule the agent will be tempted to break under pressure), also run the pressure scenarios described there — compliance on an easy prompt proves nothing about compliance under a deadline.

Done when: every with-skill run succeeds where its baseline failed, with the evidence quoted from transcripts, and the user has reviewed the outputs.

## Step 6 — Iterate

Improve based on what the transcripts and the user's feedback show, then re-run Step 5. Each pass:

- **Generalize.** The skill will run on prompts nobody wrote yet. Fix the class of failure, not the instance; if a change only helps the exact test prompt, it's overfit — reframe rather than patch.
- **Prune.** If a transcript shows the agent wasting time on something the skill told it to do, delete the instruction and re-test. Explain why behind what remains; a reasoned instruction generalizes where a bare MUST invites loopholes.
- **Bundle repeated work.** If multiple runs independently wrote the same helper or took the same detour, that code or knowledge belongs in `scripts/` or `references/`.
- **Close loopholes.** For discipline skills: capture each new rationalization verbatim and counter it per [references/testing.md](references/testing.md).

Done when: forward-test runs comply, the user is satisfied, or an iteration produces no meaningful change — whichever comes first, said out loud.

## Step 7 — Benchmark (optional)

Offer this branch when the user wants quantitative evidence — "is it actually better?", a with/without pass-rate comparison, description-trigger accuracy — or when the skill will be shared beyond this machine. Read [references/benchmarking.md](references/benchmarking.md) and follow it; it drives the bundled harness in `scripts/`, `agents/`, and `eval-viewer/`.

## Step 8 — Finish

1. Validate the folder: `python scripts/quick_validate.py <path/to/skill>` (from this skill's directory). Fix and re-run until it passes.
2. Final prune pass over SKILL.md, sentence by sentence: relevance, no-ops, duplication.
3. Confirm the description obeys the doctrine (capability + triggers, no workflow summary) and the invocation choice from Step 1 is what shipped.
4. If the skill needs distributing as a `.skill` file: `python scripts/package_skill.py <path/to/skill>`.

Done when: validation passes and the user knows where the skill lives and how it fires.

## Audit — improving an existing skill

Read [references/writing-principles.md](references/writing-principles.md), then check the skill against its failure catalog, line by line:

- **Description**: does it state the capability and one trigger per branch — or does it summarize the workflow (agents will follow the summary and skip the body), duplicate triggers, or miss a branch?
- **Sediment and sprawl**: stale layers no longer true of the behaviour; length that buries the steps. Core down to what is live.
- **Duplication**: the same meaning in two places — collapse to a single source of truth.
- **No-ops**: sentences the model already obeys by default — delete whole sentences, don't trim words.
- **Negation**: rules phrased as prohibitions that could be positive targets.
- **Hierarchy**: reference material crowding SKILL.md that only some branches need — disclose it; must-have material hidden behind a weakly-worded pointer — sharpen the pointer or inline it.
- **Completion criteria**: steps that end on a vague bound ("understand the code") instead of a checkable one.

Report findings to the user before changing anything. Then treat each approved change as a behaviour change: snapshot the current version, make the edit, and join Step 2 with the snapshot as the baseline — an edited skill is tested against its old self, not assumed better. The snapshot comparison is what turns the audit's edits into evidence rather than opinion. "It's only a fix pass", "no new capability was added", and "the user is away" are not waivers; the test round is skipped only when the user explicitly declines it, and the hand-off then says the edits shipped untested.

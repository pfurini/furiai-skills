# pi-skill-creator

A skill for creating, improving, and testing agent skills. It merges four sources into one process: the lifecycle and eval harness of Anthropic's official `skill-creator`, the writing doctrine of `writing-great-skills` (invocation economics, information hierarchy, leading words, pruning), the baseline-first testing discipline of superpowers' `writing-skills`, and the forward-testing hygiene of OpenAI's `codex-skill-creator`.

It is **user-invoked** (`disable-model-invocation: true`): type `/pi-skill-creator` or name it explicitly. It never fires on its own and costs zero context when unused.

## Evals at a glance

| Campaign | Author / consumer models | Key result |
|---|---|---|
| Create / improve / pressure evals, with-skill vs baseline (3 evals, 2 arms, 4 iterations) | Fable, Sonnet, Haiku authors | With-skill runs followed the full process at every tier (baseline runs before drafting, forward-tests, validator). Baselines never tested, mishandled snapshots and READMEs, and shipped latent defects at Sonnet tier and validity-level defects at Haiku tier |
| Planted-flaw audit (10 seeded defects in a fixture skill) | Fable, Sonnet, Haiku authors | With-skill: 10/10 flaws found (Fable, Sonnet), ~9/10 (Haiku). Baselines: 6 to 7.5/10, and one baseline canonized the worst flaw (a workflow-summarizing description) instead of fixing it |
| Regression after doctrine edit (audit-branch counter) | Sonnet | The one observed process loophole ("just a fix pass, user is away, skip the tests") was closed by an explicit counter; the follow-up run performed the full snapshot A/B test cycle |
| Clean-slate producer pilot, strong authors (10 artifacts, 33 consumer runs) | Fable authors, Haiku consumers | On a fully-specified authoring task, all four creator skills **and the no-skill control** tie at 5.00/5 consumer score; having any authored artifact beats having none (5.00 vs 3.33). See Honest caveats |
| Clean-slate producer pilot, weak authors (10 artifacts, 30 consumer runs) | Haiku authors, Haiku consumers | Treatments separate: pi-skill-creator is the only treatment at 5.00/5 across every rep; parents range 3.50 to 4.50 with real artifact-induced consumer defects; both control artifacts fail format validation |
| Target-floor doctrine A/B, negative result (6 artifacts, 18 consumer runs) | Fable authors, Haiku consumers | Adding a floor-drafting doctrine section did not improve floor robustness (4.67 vs 4.78 of 5, a tie); residual failures are task-specific semantic traps that only floor-tier forward-tests catch. The doctrine table was dropped; only the minimal wiring shipped (executor-floor interview question, forward-test at the floor, benchmark consumer defaults to the floor) |

Full method and numbers below.

## What it does

Two branches:

- **Creating a skill**: capture intent, run **baseline** agent runs on realistic prompts before writing anything (the documented failures become the spec), plan contents on the information hierarchy, draft to an explicit writing doctrine, forward-test with fresh subagents that do not know they are testing anything, iterate from transcripts, validate, and optionally benchmark quantitatively.
- **Improving a skill**: audit against a failure catalog (sediment, sprawl, duplication, no-ops, negation, workflow-summarizing descriptions, vague completion criteria), report findings before changing anything, snapshot, edit, and test the edited skill against its own snapshot.

Supporting references load only when a step points at them:

- `references/writing-principles.md`: the writing doctrine and failure catalog.
- `references/testing.md`: baseline-first testing, anti-contamination hygiene, pressure scenarios, environment fidelity (in-situ vs clean-slate).
- `references/benchmarking.md`: the quantitative branch (pass rates with variance, blind A/B comparison, description-trigger optimization, packaging), driving the bundled Python harness in `scripts/`, `agents/`, and `eval-viewer/`.

## Good usage

- "Use pi-skill-creator to create a skill called `release-notes-writer`. My conventions are: ... A typical way I would invoke it: '...'. I want it model-invoked."
  (Concrete conventions plus one realistic example prompt per branch is the ideal input. The interview step fills gaps, but everything you state up front saves a round trip.)
- "Use pi-skill-creator to improve my `release-email` skill at `<path>`. It has been accumulating cruft."
  (The audit branch shines on old skills: it reliably finds stale time-bound rules, dead file references, duplicated rules, and filler.)
- "Is version B of my skill actually better than version A?"
  (The benchmarking branch answers this with blind comparison and pass rates instead of opinion.)
- If you are away from the keyboard, say so and grant assumptions explicitly; the process is interactive by default and will otherwise wait for your confirmations.

## Bad usage (and what happens instead)

- "Just bang out the skill file quickly, no testing." It will comply, but it will also tell you, correctly, that you now own an untested guess, and name exactly which verification steps were skipped. That disclosure is by design and survived pressure testing; do not expect it to silently pretend the skill is verified.
- Expecting automatic triggering. The skill is user-invoked on purpose; "make me a skill" in a fresh session will not fire it unless you name it.
- Authoring with a weak model. At Haiku tier the with-skill process still runs, but test depth degrades (skipped test cycles with disclosure, stray files, shallower checks). Author with a strong model; consume with any.
- Treating the audit branch as a formatter. It reports findings for your approval before editing, and it will test its edit against the pre-edit snapshot; if you want a blind rewrite with no evidence, that is the "no testing" case above.

## Honest caveats

- **On fully-specified tasks with a strong authoring model, the creator skill does not measurably improve the artifact.** Our own clean-slate pilot shows all four creator skills and a no-skill control tying at 5/5 when the user's conventions are fully enumerated in the prompt. What the skill measurably adds at strong tiers is process evidence: baseline transcripts proving the skill is needed, forward-test results proving it works, snapshots making edits comparable, and a validator pass. The artifact-quality gap appears at weaker authoring tiers and (untested so far) on underspecified authoring tasks where knowledge must be mined rather than transcribed.
- The full loop spawns subagents (baselines, forward-tests, graders). Without subagent capability the loop degrades to self-testing, which is weaker evidence.
- The bundled scripts are zero-dependency (Python 3 standard library only); description-trigger optimization additionally requires the `claude` CLI.
- The clean-slate recipe in `benchmarking.md` (scrubbed `CLAUDE_CONFIG_DIR` profile) is verified on macOS with Keychain-stored credentials; on other platforms the credential file location may differ. Do not use `--bare` (it breaks credential discovery on current builds).
- A README inside a skill folder contradicts the skill's own "ship only what the executing agent needs" rule. This file is deliberately exempt as distribution documentation: it is never loaded into an agent's context at runtime.

## Method and raw results, concisely

All evals ran as blind subagent or subprocess runs: the executing agent receives a realistic user task (never "review this skill"), with-skill and baseline arms launch in the same wave with identical wording, and grading reads transcripts and artifacts, not the agents' self-reports. Planted-flaw fixtures use a pre-registered grading key kept outside any path the subjects can reach.

- **Iterations 1 to 4 (in-session)**: 3 evals (create, improve-with-planted-flaws, pressure-shortcut) times 2 arms, run on Fable, Sonnet (twice: before and after a doctrine edit), and Haiku. Headline numbers: audit flaw detection 10/10 with skill vs 6 to 7.5/10 baseline; Sonnet baselines shipped three latent defects their with-skill twins avoided; Haiku baselines produced files that fail `quick_validate.py` and one canonical example teaching syntactically invalid SQL, while Haiku with-skill artifacts validated cleanly.
- **Clean-slate distribution test**: a Fable-authored artifact consumed via `claude -p` under a scrubbed profile; surfaced that in-session forward-tests are gentler than single-pass deployment consumers.

### Producer pilots (pre-registered)

Design, identical for both pilots: 5 producer treatments (this skill, its three parents, and a no-skill control) times 2 reps, each producer run fully clean-slate (scrubbed profile, empty reproducible cwd, identical prompt except the one sentence naming the treatment skill). Every authored artifact was frozen, validated, then consumed 3 times by Haiku under clean-slate `claude -p` on a held-out messy eval (six PRs including a breaking refactor without a `!`-free major bump, excludable chore/docs, and a perf entry), alongside a no-artifact consumer baseline. Grading: 5 pre-registered prompt-contract assertions (header contains version and ISO date; breaking section first with a warning marker, its PR listed exactly once; no section names outside the stated scheme; every entry ends with its PR number; all six PRs accounted for exactly once), scored by a deterministic script, with **every flagged run manually re-read** before acceptance. That rule earned its keep: in the strong-author pilot the grader needed three iterations, and every non-baseline "failure" turned out to be a grader parsing artifact, not agent behavior.

**Pilot 1: strong authors (Fable), Haiku consumers.**

| Treatment | Consumer score (mean /5) | Spread |
|---|---|---|
| T1 pi-skill-creator | 5.00 | 6/6 perfect |
| T2 anthropic skill-creator | 5.00 | 6/6 perfect |
| T3 superpowers writing-skills | 5.00 | 6/6 perfect |
| T4 codex-skill-creator | 5.00 | 6/6 perfect |
| T5 no-skill control | 5.00 | 6/6 perfect |
| No artifact at all (consumer baseline) | 3.33 | invented sections, missing warning markers |

Reading: at the strong authoring tier, consumer pass-rate does not discriminate between producer treatments, not even against the no-skill control. When every convention is enumerated in the prompt, authoring reduces to transcription, and a strong model transcribes perfectly unaided. The only measurable gap is having any Fable-authored artifact versus none (+1.67/5): the artifact carries the conventions that raw consumers reinvent wrongly. Treatment differences at this tier live in what these assertions cannot see: process evidence on disk (baseline transcripts, forward-test results, snapshots) and artifact-contract design choices.

**Pilot 2: weak authors (Haiku), Haiku consumers.**

| Treatment | Validity | Consumer score (strict, /5) | All PRs accounted anywhere (lenient) |
|---|---|---|---|
| T1 pi-skill-creator | 2/2 valid | **5.00** (6/6 perfect) | 6/6 |
| T4 codex-skill-creator | 2/2 valid | 4.50 | 5/6 |
| T3 superpowers writing-skills | 2/2 valid | 4.00 | 3/6 |
| T2 anthropic skill-creator | 2/2 valid | 3.50 | 4/6 |
| T5 no-skill control | **0/2 valid** | 3.50 | 3/6 |
| No artifact (consumer floor) | n/a | 3.33 | 3/3 |

Reading: at the weak authoring tier the producer dimension discriminates, and pi-skill-creator is the only treatment whose artifacts came through clean on every rep (here and in Pilot 1). The other treatments' failures are real and artifact-induced (identical across all three consumer reps of each artifact, so the artifact's own rules cause them): breaking-changes sections emitted above the version header, outside the section a user would paste (T2r1, T5r1); and user-visible PRs dropped from the deliverable because the artifact enumerated only some conventional-commit prefixes, which a literal-minded consumer follows off a cliff, omitting even `perf` changes (T3 both artifacts, T4r2, T2r2). Both control artifacts fail `quick_validate.py` outright (missing frontmatter; invented keys). Grading-boundary disclosure: strict scoring counts only the deliverable (from the version header down), which credits excluded-PR notes placed after the section but not mentions inside reasoning prose above it; the lenient column is the sensitivity check, and the ranking is unchanged under either reading.

**Target-floor doctrine A/B (negative result).** A candidate feature was tested before shipping: a "writing for the executor floor" doctrine section (a failure-mode countermeasure table for weak executors), A/B-tested on the pressure branch (no testing loop), Fable authors, identical prompts stating the artifact would be run by cheap haiku-class verifier agents, 3 artifacts per arm, Haiku consumers times 3 on a held-out gnarly SQL task containing a semantic trap (a mixed-case source column that must not be renamed). Result: the arms tied (current skill 4.78/5, with floor doctrine 4.67/5), and the transcripts eliminated both excuses: every producer in both arms had loaded the doctrine, and the worst artifact even carried a "meaning is unchanged" checklist item whose consumers renamed the trap column anyway (its rule said "every column alias is snake_case", and a literal reader extends that to column references). Conclusion: static drafting doctrine saturates with a strong author; the residual defects are task-specific traps that only floor-tier forward-tests catch. Accordingly the doctrine table was not shipped; the skill carries only the minimal floor wiring (executor-floor interview question, forward-test at the floor, benchmark consumer defaults to the floor).

Raw records (all run outputs, transcripts, fixtures, grading keys and results) live in `.skill-creator/pi-skill-creator/` at the repo root (the workspace container the skill's testing process uses; add `.skill-creator/` to your `.gitignore`) and in the session scratchpad; they are test records, not part of the installable skill.

## Layout

```
pi-skill-creator/
├── SKILL.md                    # process spine (create + audit branches)
├── references/                 # writing-principles, testing, benchmarking, schemas
├── scripts/                    # validator, benchmark aggregation, description optimizer, packaging
├── agents/                     # grader / comparator / analyzer subagent instructions
├── eval-viewer/                # browser review UI for benchmark iterations
└── assets/                     # trigger-eval review template
```

## Provenance and license

Derived in part from Anthropic's `skill-creator` plugin (eval harness, agents, viewer; see `LICENSE.txt`), `writing-great-skills`, superpowers' `writing-skills`, and OpenAI's `codex-skill-creator`. The merged doctrine and process spine were developed and eval-tested in August 2026.

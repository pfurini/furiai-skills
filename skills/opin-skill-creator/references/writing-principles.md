# Writing Principles

The standard every skill draft and edit is judged against. Read it in full before drafting (Step 4) or auditing.

## Contents

- Predictability, the root virtue
- Invocation and the two loads
- Pi authoring surface
- The description
- Information hierarchy
- Steps and completion criteria
- Degrees of freedom
- Leading words
- Match the form to the failure
- Style rules
- Scripts and bundled resources
- Naming and structure rules
- Pruning and the failure catalog

## Predictability, the root virtue

A skill makes the agent behave the same _way_ on every run — the same process, not the same output (a brainstorming skill should predictably diverge; its tokens vary, its behaviour doesn't). Cost and maintainability are symptoms of predictability, not rivals to it. Every principle below is a lever on it.

The context window is a public good: the skill shares it with the system prompt, the conversation, other skills' metadata, and the actual request. Assume the agent is already very smart, and challenge each piece of information — does the agent really need this explanation, or does it already know? Only add context the agent doesn't have.

## Invocation and the two loads

- A **model-invoked** skill makes its `description` eligible for the model listing, so the agent can fire it autonomously and other skills can reach it. It pays recurring **context load** whenever listed: tokens and attention spent whether relevant or not.
- A **user-invoked** skill (`disable-model-invocation: true`) strips the description from the agent's reach: only the human, typing its name, can fire it — and no other skill can. Zero context load, but it spends **cognitive load**: the human is the index that must remember it exists. That cost is the price of human agency, not a defect — spend it where human judgement matters.

Pick model-invocation only when the agent must reach the skill on its own or another skill must reach it. If it only ever fires by hand, make it user-invoked and pay nothing. Every model-visible entry spends the listing budget.

**Granularity**: splitting into more skills spends one of the two loads, so split only when the cut earns it. Split off a model-invoked skill when a distinct leading word should trigger it independently; split a sequence of steps when the steps still ahead tempt the agent to rush the current one (and only a real context boundary — a subagent dispatch, `context: fork`, or a separate user-invoked hand-off — actually hides them). When user-invoked skills multiply past memory, the cure is a **router skill**: one user-invoked skill naming the others and when to reach for each.

## Pi authoring surface

Choose Pi frontmatter and rendering features from an observed failure. These fields enable capabilities; their presence alone is not evidence that a skill improves artifact quality.

- **The skill has the wrong visibility.** Put model-facing invocation guidance in `description` plus optional `when_to_use`; Pi joins them in the listing and caps the combined text at 1,536 UTF-16 code units. Set `disable-model-invocation: true` to remove the skill from the model listing and `skill` tool while retaining human `/skill:name` invocation. Set `user-invocable: false` only when slash-command invocation must also disappear.
- **Arguments arrive without a usable contract.** `argument-hint` labels autocomplete but does not parse input. Declare positional aliases with `arguments`. For a message-initial invocation, `$ARGUMENTS` receives the raw remainder, `$ARGUMENTS[N]` and `$N` receive 0-based quoted tokens (`$0` is first), and `$name` receives its declared position; aliases are positional, not `name=value` bindings. Mid-prompt invocations receive no arguments. If a non-empty remainder matches no placeholder, Pi appends it as `ARGUMENTS: ...` rather than dropping it.
- **The task needs a narrower tool surface.** `allowed-tools` is parsed and preserved but advisory only. `disallowed-tools` is enforced for the active turn and also blocks matching render-time shell commands. Use registered Pi tool names.
- **The executor needs a measured runtime override.** `model` and `effort` apply ephemeral per-invocation overrides; `effort` is clamped to the effective model's supported reasoning levels and is available as `${PI_EFFORT}`. Add either only when floor testing or calibration establishes the need; an uncalibrated pin is not a capability claim.
- **The body would pollute the parent context or needs a specialist.** `context: inline` is the default. Set `context: fork` to run a sole message-initial invocation through pi-subagents so the body stays out of the parent context. `agent` selects the forked subagent type and is ignored inline. `background` defaults to `true`; set it to `false` when the parent must await the result. Forking falls back to inline with a diagnostic when pi-subagents is absent, spawning fails, or Pi runs headless.
- **A relevant skill is lost in a crowded listing.** Inspect effective visibility and estimated listing cost in Pi's `/skills` overlay. `paths` globs boost a skill after successful touches to matching files, sorting it earlier and trimming it later. They do not auto-invoke the skill or load references.
- **Rendering needs a trusted shell result or a local file.** `` !`command` `` runs at render time only when `bash` is active and not disallowed; `shell` chooses `bash` (default) or `powershell`. Treat project trust as authorization for these commands. When the agent must read a bundled file, point to `@${PI_SKILL_DIR}/references/<file>.md`; Pi substitutes the absolute skill directory, while bare `@references/<file>.md` is left unresolved.
- **A hook is expected to run.** Pi keeps `hooks` parsed and preserved, never executed. Do not design a skill whose completion depends on one.

## The description

The description is the skill's trigger and its single largest lever. Doctrine:

1. **Capability first, in one clause** — what the skill does, front-loading its leading word. Third person, always ("Extracts text and tables from PDFs…", never "I can help you…" or "You can use this to…").
2. **Then one trigger per branch in listing metadata.** Each distinct way the skill is invoked gets one trigger phrase, worded with the vocabulary the user actually uses. Keep it in `description`, or move the trigger-only tail to `when_to_use` when that makes the capability easier to scan. Synonyms that rename the same branch are duplication — collapse them.
3. **Never summarize the workflow.** A description that sketches the skill's process ("dispatches a subagent per task with review between tasks") becomes a shortcut: the agent follows the sketch and skips the body. Testing has shown this concretely — a workflow-summarizing description caused agents to perform one review where the body's flowchart required two; removing the summary fixed it. State what the skill does and when to reach for it; how it works lives only in the body.
4. **All "when to use" information lives in model-visible listing metadata, not in the body.** The body loads only after triggering, so a "When to Use" section there triggers nothing.
5. Limits: description ≤1024 characters, no angle brackets; `name` ≤64 characters, kebab-case.

For a user-invoked skill the description is human-facing: a one-line summary for the human scanning a list. Trigger phrasing does no work there — strip it.

Realistic near-miss thinking sharpens triggers: the queries most worth anticipating are the ones that share keywords with the skill but need something else. If the description would fire on those, tighten it.

## Information hierarchy

A skill's content sits on a ladder ranked by how immediately the agent needs it:

1. **In-skill steps** — ordered actions in SKILL.md, the primary tier.
2. **In-skill reference** — definitions, rules, facts in SKILL.md, consulted on demand. A flat peer-set (every rule of a review on one rung) is a fine arrangement, not a smell.
3. **Disclosed reference** — pushed to a separate file, reached through a **context pointer**, loaded only when the pointer fires.

**Progressive disclosure** is the move down the ladder so the top stays legible. Branching is the cleanest test: inline what every branch needs; push behind a pointer what only some branches reach. When a skill supports variants (frameworks, providers, domains), keep the workflow and selection logic in SKILL.md and give each variant its own reference file — the agent reads only the one the task needs.

A pointer's _wording_, not its target, decides when and how reliably the agent reaches the material. A must-have file behind a weak pointer ("see also the testing reference") is a variance bug: sharpen the wording ("Read the testing reference disclosed by SKILL.md now, before dispatching any subagent") first; inline the material only if sharpening fails.

Mechanics that keep disclosure working:

- **One level deep.** Every reference file is disclosed directly from SKILL.md with `@${PI_SKILL_DIR}/...`. Nested references (SKILL.md → advanced.md → details.md) get partially read and information is lost. `paths` can boost the skill listing and `context: fork` can isolate its body, but neither repairs a nested disclosure chain.
- **Table of contents** at the top of any reference file over ~100 lines, so a partial read still reveals the full scope.
- **Co-location**: keep a concept's definition, rules, and caveats under one heading rather than scattered. The hierarchy decides how far down a piece sits; co-location decides what sits beside it. The test: the skill should read like documentation written for the agent.
- SKILL.md body under ~500 lines; split when approaching the limit.

## Steps and completion criteria

Steps are imperative, ordered, and each ends on a **completion criterion** — the condition telling the agent the work is done. Two properties make it a lever:

- **Clarity**: can the agent tell done from not-done? A vague bound ("understanding reached") lets attention slip to _being done_ — **premature completion**. A checkable bound resists it no matter how many later steps are visible. Sharpen the bound first; hide later steps by splitting only if the criterion is irreducibly fuzzy _and_ the rush is actually observed.
- **Demand**: how much it requires sets the **legwork** — the digging within a step. "Every modified model accounted for" forces thorough work where "produce a change list" does not. Demand binds flat reference too: "every rule applied" is how a skill with no steps still carries an exhaustiveness bar.

For multi-step workflows where skipping is costly, give the agent a checklist to copy and check off. Build **feedback loops** into quality-critical steps: run validator → fix → re-run, and only proceed when it passes.

## Degrees of freedom

Match specificity to the task's fragility — think of the agent walking a path:

- **High freedom** (prose heuristics): many routes succeed, context decides. An open field.
- **Medium freedom** (pseudocode, scripts with parameters): a preferred pattern exists, some variation is acceptable.
- **Low freedom** (exact script, no parameters, "run exactly this"): the operation is fragile, consistency is critical, one sequence is safe. A narrow bridge with cliffs.

Giving low-freedom instructions for an open field wastes the model's judgement; giving high-freedom instructions on a narrow bridge produces variance where it can't be afforded.

## Leading words

A **leading word** is a compact concept already living in the model's pretraining that the agent thinks with while running the skill (_baseline_, _prune_, _tracer bullets_, _fog of war_). Repeated as a token, it accumulates a distributed definition and anchors a region of behaviour in minimal tokens by recruiting priors the model already holds. In the body it anchors execution; in a description it anchors invocation — especially when the same word lives in the user's own prompts and docs.

Hunt for collapse opportunities: a triad spelled out at three sites, a sentence gesturing at one idea — each can collapse into a single pretrained word ("fast, deterministic, low-overhead" → a _tight_ loop). A coined word recruits no priors; reach for an existing one. A leading word too weak to beat the default (_be thorough_) is a no-op; the fix is a stronger word (_relentless_), not a different technique.

## Match the form to the failure

Classify the baseline failure before writing guidance — the form that fixes one failure class measurably backfires on another:

| Baseline failure | Right form | Wrong form |
|---|---|---|
| Skips/violates a rule under pressure (knows better, does it anyway) | Prohibition + rationalization counters + red flags from the directly disclosed testing procedure | Soft guidance ("prefer…", "consider…") |
| Complies, but the output has the wrong shape | Positive recipe or contract: state what the output IS — its parts, in order | Prohibition list ("don't restate", "never narrate") |
| Omits a required element from something it already produces | Structural: a required slot in the template it fills | Prose reminders near the template |
| Behaviour should depend on a condition | Conditional keyed to an observable predicate ("if the brief exists, reference it") | Unconditional rule + exemption clauses |

Why prohibitions backfire on shaping problems: **negation** drags the forbidden behaviour into context and makes it _more_ available ("never write verbose comments" makes verbosity the pattern just read). In head-to-head wording tests, the prohibition arm produced more of the unwanted content than the recipe arm — and trended worse than no guidance at all. Prompt the positive: describe the target so the banned thing is never spoken. A prohibition earns its place only as a hard guardrail you can't phrase positively, and even then pair it with the positive target.

Two rules for whichever form wins:

- **No nuance clauses.** "Don't X unless it matters" reopens the negotiation; appending one nuance clause to a winning recipe degraded it from consistent to noisy in the same tests. A real exception becomes its own conditional on an observable predicate.
- **Exemption clauses don't scope.** "This limit doesn't apply to code blocks" still suppresses code blocks. If part of the output must be exempt, restructure so the rule can't reach it.

## Style rules

- **Imperative form** throughout the body.
- **Explain the why** behind non-obvious instructions. The model has good theory of mind; a reasoned instruction generalizes to cases the skill didn't anticipate, where a bare MUST invites loophole-hunting. All-caps ALWAYS/NEVER appearing in a draft is a yellow flag: usually the form is wrong (see the table above), not the emphasis too weak — reserve imperatives-plus-counters for tested discipline failures.
- **One excellent example beats many mediocre ones.** Complete, runnable, from a real scenario, in the single most relevant language. Input/output pairs teach format better than prose descriptions of format.
- **Consistent terminology**: one term per concept, everywhere ("field", not field/box/element/control by turns).
- **No time-sensitive content.** Nothing that becomes wrong on a date; deprecated patterns go in a collapsed "old patterns" note if they're needed at all.
- **Templates**: for strict output formats, "ALWAYS use this exact template" plus the template; for flexible ones, "sensible default, adapt as needed". Say which one you mean.

## Scripts and bundled resources

- `scripts/` — executable code for what must be deterministic or was being rewritten every run. Executed without loading into context; only output costs tokens.
- `references/` — documents loaded on demand. Large files (>10k words) get grep patterns in SKILL.md alongside the pointer.
- `assets/` — files used in the output (templates, boilerplate, fonts), never loaded into context.

Rules for scripts:

- **Solve, don't punt.** Handle error conditions inside the script rather than failing back to the agent; a script that half-works costs more than no script.
- **No voodoo constants.** Every threshold and timeout justified in a comment — if you don't know the right value, the agent can't either.
- **Make execution intent explicit**: "Run `analyze.py` to extract fields" (execute) vs. "See `analyze.py` for the algorithm" (read). Execution is the default — it's cheaper and more reliable.
- **State dependencies** and how to install them; don't assume packages exist.
- **Plan-validate-execute** for batch or destructive operations: emit a machine-checkable plan file, validate it with a script whose errors name the specific problem ("Field 'signature_date' not found. Available: …"), and only then execute.
- Forward slashes in every path, on every platform.

## Naming and structure rules

- Kebab-case name, ≤64 characters, verb-led; gerunds work well for processes (`resolving-merge-conflicts`, `writing-prds`). Folder named exactly after the skill. Namespace by tool when it aids triggering (`gh-address-comments`).
- Descriptively named files (`form-validation-rules.md`, not `doc2.md`); directories organized by domain or variant.
- The skill contains only what the executing agent needs: no README, CHANGELOG, INSTALLATION_GUIDE, or notes about how the skill was made.

## Pruning and the failure catalog

Keep each meaning in a **single source of truth**; check every line for **relevance** (does it still bear on what the skill does?); then hunt no-ops sentence by sentence — when a sentence fails, delete the whole sentence rather than trim words from it.

The catalog, for drafting defensively and auditing existing skills:

- **Premature completion** — ending a step before it's genuinely done, attention slipping to _being done_. Defence in order: sharpen the completion criterion (cheap, local); only if it's irreducibly fuzzy _and_ the rush is observed, hide the later steps behind a real context boundary.
- **Duplication** — the same meaning in more than one place. Costs maintenance and tokens, and inflates the meaning's apparent rank on the ladder. (The accidental inverse of a leading word, which repeats a _token_, never the meaning.)
- **Sediment** — stale layers that settle because adding feels safe and removing feels risky. The default fate of any skill without a pruning discipline.
- **Sprawl** — a skill simply too long even when every line is live and unique. The cure is the ladder: disclose reference, split by branch or sequence.
- **No-op** — a line the model already obeys by default; load paid to say nothing. The test is model-relative: does it change behaviour versus the default? Two people disagreeing settle it by running the skill, not by debate.
- **Negation** — steering by prohibition; names the elephant and makes it more available. Cure: prompt the positive (see the form table above).

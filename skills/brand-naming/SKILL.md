---
name: brand-naming
description: Brand naming with verified uniqueness — strategy-driven name generation plus automated availability screening across domains, trademarks, social handles, company registries, and app stores. Use when the user asks to name a brand, company, or product ("help me name this", "name ideas for", "what should I call"), when they share candidate names for feedback, ranking, or scoring, or when they ask whether a name is available, unique, or safe to use. Even a casual mention of needing a name triggers this skill.
---

# Brand Naming

Act as a brand naming strategist: understand the business, build a naming strategy, generate names with reasoning, and screen them for uniqueness before anyone falls in love with a dead name. Be honest and direct — flag weak names and weak directions plainly.

## Modes

- Brief, description, or a request for ideas → **Generation**.
- Existing names offered for feedback, ranking, or scoring → **Evaluation**.
- "Is this name free/available/taken?" for one or more specific names → **Verification only**.
- Brief plus their own candidate names → Generation, with their names evaluated in the same tables as yours.

Every mode needs the market pack. Determine the primary target market in this order: the user's explicit statement; failing that, the brief's signals (the language it is written in, where the business and its competitors operate, the TLDs or registries it mentions); failing that, default to **Italy + EU** and state the assumption. Then read `references/markets/<market>.md` now (`italy.md` exists; anything else uses `international.md`). The pack sets the TLD set, trademark offices, registry procedure, and market-specific legal screens.

**Speak the market's language.** All user-facing output — questions, strategy brief, tables, recommendation, clearance log — is written in the market's language (Italian for the Italy pack), even though this skill and its references are English and regardless of any session-level language default. Only an explicit user request changes the output language.

## Generation Mode

### Step 1 — Gather context

Read what the user already gave and ask only for what's missing — a few focused questions, not the whole list. Minimum to proceed:

- What the brand sells or offers, and who buys it.
- Target market(s) and language.
- The feeling the name should create (or agreement to derive it from competitor research).
- Competitors and names to avoid.
- The **Nice classes** the brand would file under (derive them yourself from the offer — e.g. SaaS: 9, 35, 42 — and confirm; the trademark screen needs them).

Useful when offered: price positioning, personality, expansion plans, words they love or hate. When the target market's language is not English, plan at least one naming direction built on native-language roots.

Done when: offer, audience, market, feeling, avoid-list, and Nice classes are established.

### Step 2 — Naming strategy brief

Write a short strategy brief before generating:

```
## Naming Strategy

**Brand in one line:** [what this brand is, simply]
**Audience:** [who the name must attract — and who signs the contract, if different]
**Market / language:** [market, working language, Nice classes]
**Positioning angle:** [what the brand should stand for; how competitors name themselves and where the gap is]
**Emotional territory:** [what the name should make people feel]
**Directions to explore:** [3-5 strategic directions chosen for this brief]
**Themes to avoid:** [clichés, saturated territories, risky associations]
```

### Step 3 — Generate by direction

Aligned models concentrate probability on typical outputs, so the first names that come to mind are everyone's first names — the same ones any founder prompting any model would get. The sequence below exists to escape that pull:

1. **Diverge at the direction level first.** Diversity injected into the strategy transmits to the names; diversity requested inside one big batch of names does not. Make the 3-5 directions structurally unalike — different register (institutional, artisanal, poetic, matter-of-fact), different source domain (the craft's objects, the buyer's ritual, the outcome, the place), different name shape (real word, compound, coinage, morphological play). If two directions would produce interchangeable names, replace one.
2. **Burn off the mode.** List ~10 names fast, unfiltered — the obvious stratum. Set them aside as calibration, never as candidates: anything generated later that resembles them is a re-tread.
3. **Generate each direction in its own pass**, conditioned only on that direction's logic: 8-10 candidates, each annotated from *common* to *rare*. Advance mostly from the rare tail — the common end is where collisions and clichés live; the tail is where ownable names live. Mine the direction's source domain for material before coining (objects, gestures, tools, rituals, dialect and craft words): a rare real word beats invented syllables, and every name must carry a story the founder can tell.
4. **Force difference.** Each new candidate must differ from every previous one in root, morphology, length, or sound pattern — not just spelling. When two consecutive candidates re-tread existing roots, the direction is exhausted: stop it.
5. **Defer judgment.** No scoring or ranking during generation. The only in-flight kills are the tier-0 screens from the market pack and `references/verification.md` (regulated words, negative meanings including dialects, cultural echoes, famous-name collisions, SEO ownability) — a regulated word dies on sight. Evaluation starts when the pool is complete.

When the user is present, show the directions with 2-3 sample names each and get their reaction before deep generation and verification — taste applied to directions steers everything downstream at the lowest cost. Working autonomously, proceed and state assumptions.

The default reply shows the evaluation table and Top 5, not the direction-by-direction breakdown (offer it; produce it on request in the format below).

On-request per-name format:

```
**[Name]**
Meaning: [what it means or references]
Why it works: [strategic + emotional reasoning]
Tagline direction: [one example]
Risk: [flags from screening]
Score: [X/10]
```

Done when: the directions are structurally unalike, every direction ran to 8-10 candidates or exhaustion, the pool passed tier 0, and no candidate resembles the burn-off list.

### Step 4 — Verify

Read `references/verification.md` now and run the funnel: tier 1 (domain screen) on every candidate, tier 2 (trademarks with the brief's Nice classes, handles, conditional app stores, variant sweep, live-usage sweep) on the finalists, tier 3 pending items collected for the checklist. Write the clearance log.

Done when: every name you are about to show in the Top 5 is verified FREE on all automated dimensions, dead candidates are recorded with reasons, and the pending list exists.

### Step 5 — Evaluation table

One row per finalist (verified names only), scoring the naming tests:

| Name | Meaning | Sound | Memory | Spelling | Story | Expansion | Risk | Overall |
|------|---------|-------|--------|----------|-------|-----------|------|---------|
| Name | one line | /10 | /10 | /10 | /10 | /10 | FREE / flags | /10 |

Sound = natural when spoken; Memory = recalled after one hearing; Spelling = spellable after hearing; Story = the founder can explain it; Expansion = the brand can grow under it; Risk = verification verdict plus any FLAGs.

### Step 6 — Top 5 and recommendation

Lead with the Top 5, ranked, one line each (meaning + why it's strong). Then recommend **one** name with strategic reasoning grounded in positioning, audience, and future potential — not "it sounds nice". State what evidence would change the recommendation. Offer the full direction breakdown and the adversarial review as follow-ups.

### Step 7 — Before you finalize

Close with the checklist, split into what verification already established (with evidence from the clearance log) and what remains manual:

```
## Before You Finalize

Verified: [each automated dimension, with result and source]
Pending: [each manual item with its one-line procedure — registry check per market pack,
login-walled social handles, consultant similarity search before filing, spoken tests
with people outside the project]
```

Advise registering the primary domains immediately if the front-runner convinces — available domains don't stay available.

## Evaluation Mode

Get a one-line description of the brand and its market if missing — fit can't be judged without it. Evaluate each provided name:

```
**[Name]**
What it suggests: [category, tone, associations]
Category fit: [does it sound right for this industry?]
Premium or cheap: [honest take]
Say / spell: [easy or not, after one hearing]
Logo potential: [strong / moderate / weak, why]
Verification: [run the funnel — same gate as Generation]
Score: [X/10]
```

Run the verification funnel (Step 4) on their names — a user's own candidate deserves the same gate as a generated one. Rank strongest to weakest, then recommend one and say why.

## Verification Mode

For the given name(s): read `references/verification.md`, run tiers 1-2 plus the live-usage sweep, report per-dimension verdicts, the pending list, and a bottom line — clear to pursue, flagged, or taken.

## On-request deep dives

**Adversarial review** — when asked to attack the recommendation (or for "pros and cons"): argue the strongest case against the chosen name from at least these angles — legal defensibility (descriptive vs fanciful), register mismatch with the buyer, the audience the name ignores, temporal or scope boundaries the brand may outgrow, and the cost of owning the category it claims. For each attack give the honest counterargument or concede. End with the concrete signals that would change the recommendation.

**Brand architecture** — when a second product, audience, or business model appears: lay out independent brands vs endorsed ("X by Y") vs one brand, with the channel-conflict test — if one arm's success gives the other arm's customers a reason to leave, only independent brands with credible separation (contractual and technical, not just visual) contain the damage. Verify any proposed second name through the same funnel.

## Tone

Sharp creative strategist: human, clear, a little opinionated. Plain verdicts — "strong direction", "premium but cold", "good sound, hard to own". Never flatter a weak name.

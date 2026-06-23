# PRD Validation Rubric

Standalone. Paste **any** PRD — one you just wrote, or one a spec-first tool emitted — and grade it. This is also the gate the `writing-prds` skill runs after drafting.

The rubric exists because a PRD's most common failure is invisible to its author: it *looks* thorough (long, numbered, sectioned) while having skipped the intent layer entirely. Thoroughness is the disguise. Score against intent, not completeness.

## How to score

Six dimensions, each **0 / 1 / 2**. Report every score with the **offending quote** from the doc.

A PRD **FAILS** if *either*:
- any single dimension scores **0**, or
- the total is **< 9 / 12**.

A failing PRD is not "a PRD that needs polish" — it is the wrong *kind* of document (usually a spec). The fix is rarely "add a section"; it's "cut to a 1-pager and recover the intent."

| # | Dimension | 0 | 2 |
|---|---|---|---|
| 1 | **Intent before solution** | Jumps straight to specifying the brief's solution; the named feature is treated as the requirement | Recovers the problem + job; the named feature is one candidate, derived/justified, held coarse |
| 2 | **Falsifiable outcome** | No metric, or vague ("faster/better/intuitive"), or an invented number with no evidence/assumption named | Specific, evidence- or assumption-grounded, and a competent peer could reasonably argue the opposite target |
| 3 | **Solution altitude (fat-marker)** | Field-level spec: data model, FR-lists, schemas, UI mechanics | Coarse enough to convey the bet; implementation deliberately left open |
| 4 | **Four product risks** | None, or only NFR/security | value · usability · feasibility · viability each named and addressed |
| 5 | **Riskiest assumption + disconfirming evidence** | None, or "assumptions: TBD" | Names the one belief that sinks it if false, and the cheapest evidence that would change the decision |
| 6 | **Restraint (not-a-spec)** | Exhaustive; comprehensiveness-as-quality | Lean, scoped, detail deferred to discovery/build |

## Spec-smell linter (each hit = drift toward spec — flag with quote)

- Numbered functional requirements (`FR-1`, "the system shall", P0/P1 **requirement** lists)
- A data model / table schema / JSON shape / field-by-field column list
- UI mechanics (dialog layout, button placement) specified *before* the outcome is falsifiable
- NFR tables or edge-case matrices forming the bulk of the doc
- A "success metrics" section of invented targets with no evidence and no named assumption
- The brief's proposed solution adopted verbatim as scope, un-interrogated

Two or more hits ⇒ dimension 1 or 3 is almost certainly 0. The linter is the fast path to the verdict.

## Falsifiability test (dimension 2, expanded)

State the outcome, then state its **negation**. Could a competent peer reasonably argue *for* the negation?

- "We want users to be happy / the flow to be intuitive" → negation ("we want them unhappy") is absurd ⇒ **platitude, score 0**.
- "≥25% of sessions start from a saved View within a quarter of GA" → a peer could argue 25% is too aggressive, or that sessions-started is the wrong denominator ⇒ **a real bet, score 2**.

Basis: Hubbard, *How to Measure Anything* — every "intangible" ("engaging", "intuitive", "fast") decomposes into something observed and counted. If it resists decomposition, it isn't an outcome yet.

## Discovery pointers (the audit's other half — one move, not a methodology)

A well-formed PRD can still be the wrong bet. A passing rubric score is necessary, not sufficient. The minimum hook (this is all dimension 5 asks for):

- **Riskiest assumption** — the single belief that, if false, sinks this.
- **Disconfirming evidence** — what you'd observe if it's false, and the cheapest way to look *before* building (fake-door, prototype, assumption test, five interviews).

If the PRD names neither, score dimension 5 = 0 and recommend a discovery spike over more spec. Deeper methods if warranted: Torres (assumption mapping / opportunity solution tree), Gilad (evidence & confidence), Cagan (testing the four risks in discovery). Do **not** expand this into a discovery plan inside the PRD.

## What a passing PRD looks like (gold-standard 1-pager)

Same feature as the failing example below — written as intent. Note the length.

> **PRD (1-pager): "Saved Views" (provisional name)**
> - **Problem.** Power users rebuild the same filter + date-range + column setup every session; recurring reports are reconstructed by hand and passed around as screenshots. *Assumption to test:* a meaningful share of weekly-active users re-apply near-identical configs ≥3×/week — pull the real rebuild rate from product analytics before committing.
> - **Customer + job.** The daily-driver analyst, hiring us to *"get back to — and hand a teammate — the exact analysis I had, without rebuilding it."*
> - **Outcome (falsifiable).** Within a quarter of GA, **≥25% of dashboard sessions start from a saved configuration**, and View-creators show a positive 4-week-retention lift vs non-creators. (A peer could fairly argue 25% is too high, or that retention won't move — that's the bet.)
> - **Risks.** *Value (riskiest):* do users rebuild configs often enough to value saving? · *Usability:* is save/return discoverable mid-analysis? · *Feasibility:* dashboard state is already serializable — low · *Viability:* sharing must never expose data beyond the viewer's own permissions.
> - **Solution (fat-marker).** Save the current dashboard state as a named, returnable, shareable thing; relative ranges stay current; a shared View is a live reference others can fork. *No schema, fields, or FR-list — that's for build.*
> - **Riskiest assumption / disconfirming evidence.** If analytics shows configs are mostly one-off, this is the wrong bet. Fake-door the "Save view" button to measure intent before building anything.

## Worked calibration (rubric applied to two real, independently-written PRDs)

### Failing — feature-shaped brief ("save a named View")

A long, polished doc: 16 sections, `FR-1`…`FR-14`, a SQL data model, JSON `config` with `schema_version`, NFR and edge-case tables.

| # | Dimension | Score | Why |
|---|---|---|---|
| 1 | Intent before solution | **0** | Took "save a View" as the requirement; never recovered the job; 14 FRs specifying the given solution |
| 2 | Falsifiable outcome | **1** | Metrics exist (adoption ≥30%) but invented; doc admits "Evidence (assumed, to be validated)" |
| 3 | Solution altitude | **0** | SQL tables, JSON schema, FR-1…FR-14, field lists |
| 4 | Four product risks | **1** | Security/NFR covered; value/viability not framed as risks |
| 5 | Riskiest assumption | **0** | Many assumptions listed; no single riskiest + disconfirming evidence |
| 6 | Restraint | **0** | 16 sections; comprehensiveness-as-quality |

**Total 2/12 → FAIL.** Verdict: a competent solution **spec**, not a PRD. Fix: replace with the 1-pager above.

### Higher, still flagged — problem-shaped brief ("reduce checkout abandonment")

| # | Dimension | Score | Why |
|---|---|---|---|
| 1 | Intent before solution | **2** | Problem-framed; solutions treated as a portfolio of bets |
| 2 | Falsifiable outcome | **1** | Relative-lift target is good practice, but baseline is a placeholder ("30%→36%, confirm later") — not yet grounded |
| 3 | Solution altitude | **1** | Interventions fairly coarse, but WS1–5 pre-commits a large solution catalog |
| 4 | Four product risks | **1** | Risks/dependencies present, not mapped to the four |
| 5 | Riskiest assumption | **2** | Names the core assumption (abandonment is recoverable) and instruments to test it *first* |
| 6 | Restraint | **1** | Long, but structured as bets, not specs |

**Total 8/12 → FAIL (borderline).** Much closer to a real PRD. Fix: ground the baseline before locking the target; trim the pre-committed solution list to the riskiest 2–3.

**Calibration caveat:** this contrast is illustrative, not a controlled experiment — the two briefs also differ in scope (one narrow, one broad). The lesson the rubric enforces holds regardless of brief shape: **flag the accept-the-solution reflex even when — especially when — the brief hands you a finished solution.**

## The canon (why these dimensions exist)

- **Amazon — Working Backwards / PR-FAQ** (Bryar & Carr, 2021): write the customer outcome before the build; the FAQ stress-tests intent. *Primary source for the intent-first stance.*
- **Marty Cagan — Inspired / Empowered** (SVPG): the four product risks (dim. 4); PRD-as-spec is the named anti-pattern; prototypes over documents.
- **Basecamp — Shape Up** (Ryan Singer): appetite, boundaries, fat-marker sketch — the coarse-on-purpose discipline (dim. 3).
- **Melissa Perri — Escaping the Build Trap**: outputs vs outcomes — the name for the failure this rubric catches.
- **Teresa Torres — Continuous Discovery Habits**: assumption testing / opportunity solution tree (dim. 5).
- **Itamar Gilad — Evidence-Guided**: evidence and confidence behind a bet (dim. 5).
- **Douglas Hubbard — How to Measure Anything**: the decomposition basis for falsifiable outcomes (dim. 2).

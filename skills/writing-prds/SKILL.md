---
name: writing-prds
description: Use when writing, reviewing, or grading a PRD, product brief, or feature spec — especially when handed a feature or solution to "write up", when a draft reads like a feature list, data model, or technical spec, or when a success metric is vague ("faster", "better", "intuitive"). Also for validating or scoring an existing PRD's quality.
---

# Writing PRDs

## Core principle

A PRD captures **intent, not spec**: the problem, the customer's job, and a *falsifiable* outcome — established **before** any solution. The feature named in the brief is a *candidate*, not the requirement. The dominant failure mode is skipping intent and exhaustively speccing a solution nobody validated.

## The gate — STOP

**No solution or implementation language until the intent layer passes.** Treat it like TDD's iron law. This holds *even when the brief hands you a finished solution* — recover the job first.

All four must hold:

1. **Problem** — whose pain, when, how often. Evidence, or a *named* assumption (never "assumed, TBD").
2. **Customer + job** — who they are and the job they're hiring this for.
3. **Outcome** — a falsifiable metric. Test: *could a competent peer reasonably argue the opposite target?* If not, it's a platitude. No "fast / intuitive / better" — every intangible decomposes into something counted (Hubbard).
4. **Risks** — the four product risks: value, usability, feasibility, viability.

**Only then** render the solution — **fat-marker coarse**: the least detail that conveys the bet. Fields, schemas, FR-lists, NFR tables = a spec, not a PRD.

## Format — lightest first

Default to a **lean 1-pager**; escalate only with a stated reason:
**1-pager** (default) → **Shape Up pitch** (appetite + boundaries) → **PR/FAQ** (big or irreversible bets).
Length is not quality — the docs that fail the rubric are the longest.

## Discovery — one move, not a methodology

Name the **riskiest assumption** and the **evidence that would change your mind**. Can't? You're speccing faith — cheaper to test it (fake-door, prototype, assumption test) than to build.

## Validate — always

After drafting — or to grade *any* existing PRD, including one a spec-first tool emitted — run **prd-validation-rubric.md**: a scoreable gate + spec-smell linter that **fails** spec-shaped docs and non-falsifiable metrics. The gate always fires.

## Red flags — STOP, you're speccing

- "The brief gave me the solution, so my job is to spec it." → No. Recover the job; the named feature is one candidate.
- "This brief is clear, I'll skip the why." → The why *is* the PRD.
- "A thorough PRD is a better PRD." → Comprehensiveness ≠ quality. Stay coarse; defer detail to build.
- Reaching for FR-1/FR-2…, a data model, a JSON schema, or a field list → spec smell. Stop.
- A success target you invented (`≥30%`) with no evidence and no named assumption.
- "Eng/leadership demand a build-ready spec *now*, the design's decided." → The gate still applies. A spec on an unvalidated job is the expensive mistake under deadline. Deliver intent first; the FR-list is a fast, better-targeted step *after* sign-off. Raise it once, then proceed.

## When NOT to use

- Engineering design docs / RFCs (how to build an already-decided thing) — that's a tech spec.
- A ticket-sized change with an obvious, already-evidenced outcome.

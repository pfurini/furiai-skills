# Campaign plan: underspecified authoring, wiring A/B

**Status**: pre-registered plan. No producer or consumer run has executed at the time of
this commit. Decisions were grilled one at a time against
`docs/handoff-underspecified-authoring-eval.md` (planning session, 2026-08-10); every
choice below is pinned unless a gate forces the amendment path named for it.

**Primary objective**: validate (or reject) two additions to pi-skill-creator's test
loop, spec-blind eval generation and red-team input generation, on a fixture where the
skill's knowledge must be discovered rather than transcribed. **Secondary outputs**: the
discovery-gap measurement (does the process advantage convert to an artifact advantage
for strong authors on underspecified tasks?) and reusable campaign machinery.

---

## 1. Treatment design: the two wiring steps

Both steps are process wiring (subagent dispatches), not doctrine prose, matching the
intervention class that changed behavior in every prior test. They ship as a bundle or
not at all (single A/B arm; per-step attribution comes from transcripts, not from
factorial arms).

### Step W1: spec-blind eval generation (pre-draft)

Position: after Step 2 (baselines), **before drafting**. Blindness is structural: the
draft does not exist yet, so the eval author cannot read it. This amends the handoff,
which placed both steps post-draft.

- Dispatch: a fresh subagent receives **only the captured intent from Step 1** (not the
  draft, not the baseline transcripts, not the authoring guides).
- Deliverable: eval prompts plus expected behaviors, written to the
  `.skill-creator/<skill>/` workspace.
- Use: these evals run in Step 5 as floor-tier forward-test cases alongside the
  author's own, and their pass/fail feeds iteration.
- Rationale for intent-only input (stricter than necessary for blindness): baseline
  transcripts are draft-independent and could be shared, but sharing them correlates
  eval design with the author's attention. Recorded as a design choice open to revision
  if wired-arm evals prove too shallow.

### Step W2: red-team input generation (post-draft)

Position: after Step 4 (draft), feeding Step 5.

- Dispatch: a fresh subagent receives **the draft skill and the captured intent**, with
  the instruction: construct 2–3 inputs that a literal, single-pass reader of these
  rules would get wrong; derive the expected correct behavior **from the intent only**;
  construct the traps **from the draft only**.
- Rationale for draft+intent (not draft-only): pre-registering expected correct
  behavior requires the intent (the alias-renaming defect is only *wrong* relative to
  intent, not relative to the rule text). The red-teamer is a test generator, not a
  measured subject, so it may see both.
- Deliverables, split by visibility: (a) trap input files and a naturalistic task
  prompt, staged where forward-test consumers can reach them; (b) the expected-behavior
  key, written to the workspace, **outside any consumer-visible path**.
- Use: the orchestrating author dispatches fresh floor-tier consumers with (a) only,
  grades against (b), and iterates. Contamination handling is testing.md's existing
  hygiene made explicit; no new machinery.

### A/B arms

| Arm | Treatment |
|---|---|
| T-CTL | No skill (control) |
| T-PI  | `skills/pi-skill-creator`, frozen at the campaign-start commit |
| T-WIRED | Frozen copy of pi-skill-creator plus W1 and W2, at `campaigns/underspecified-authoring/treatments/pi-skill-creator-wired/` |

Same fixture, same producer prompt (one treatment sentence differs), Fable authors,
clean-slate subprocess runs. T-CTL vs T-PI answers the discovery question; T-PI vs
T-WIRED answers ship/no-ship for the wiring.

**Recorded confound (not fixed)**: T-WIRED does more work per run. A win is a
total-effect result ("adding these steps improves outcomes at this cost"), not proof
that independence is the mechanism. No time-matched control arm is funded; transcript
attribution partially addresses mechanism.

---

## 2. Eval family and fixture spec

Family 1 (discovery-heavy). Families 2 and 3 are **explicitly deferred**; family 2
(induction-from-examples) is pre-named as the wiring's second test bed if it ships,
because embodied-in-examples intent stresses spec-blind eval generation in a way stated
intent cannot.

### Fixture

A plausible small SaaS analytics repo, ~35–50 files, 30–50k tokens total, **executable**:
a SQLite database built from committed seed CSVs, so consumer questions have single
correct numeric answers that come out *differently wrong* per missed key item.

Shape (final layout fixed at build time):

- `db/analytics.sqlite` plus `seed/*.csv` and a build script
- `db/schema/*.sql`: DDL for 7–8 tables (`users`, `accounts`, `memberships`,
  `events` (deprecated), `events_v2`, `sessions`, `subscriptions`, `plans`)
- `db/migrations/`: numbered migrations, including the one that introduces `events_v2`
  and marks `events` backfill-only
- `docs/`: 2–3 pages, **partially stale by design** (still describes `events` as
  current; ERD shows the legacy `users.account_id` join; a units table that is wrong
  for session duration)
- `queries/`: 8–12 production SQL files that embody the induced conventions
- Filler to reach size: `README.md`, dashboard configs, scripts, `.gitignore`

Master fixture committed under `campaigns/underspecified-authoring/fixture/`.
Subject-visible copies are staged into temp paths at run time; subjects never see this
repo, the key, or each other.

### Planted-knowledge key (10 items, tiered 2/4/4)

Difficulty lives in the tiers, not fixture size. The key is pre-registered here at the
content level; exact identifiers and the per-item coverage criteria are frozen with the
fixture at milestone M0, before any producer run.

**Tier A, surface (sanity floor; even the control should find these):**

- **A1**: all timestamps are UTC epoch seconds (stated in docs; date filters must
  convert).
- **A2**: canonical revenue metric is monthly-normalized MRR; annual plan prices divide
  by 12 (stated in the metrics doc).

**Tier B, cross-reference (correct only by connecting artifacts that individually
mislead):**

- **B1**: `events` is deprecated; live data is in `events_v2`. Docs say `events`;
  the migration and every production query say `events_v2`; `events` still exists with
  stale rows so using it yields plausible wrong numbers.
- **B2**: account attribution goes through `memberships` (many-to-many); the
  `users.account_id` column shown in the docs ERD is a stale legacy denormalization.
- **B3**: `sessions.duration` is milliseconds; the docs units table says seconds; one
  production query divides by 1000.
- **B4**: `subscriptions.status` uses single-letter codes and `plans.price_cents` is in
  cents; the code-to-word mapping and the cents convention are visible only in a CHECK
  constraint and one query, while docs speak in words and dollars.

**Tier C, induced (stated nowhere; exists only as a pattern across queries):**

- **C1**: mandatory test-account filter: every production query excludes
  `accounts.is_test = 1`. No doc mentions it. Seed data gives test accounts enough
  activity that missing the filter shifts every count materially.
- **C2**: "activity" excludes `heartbeat` events (high-volume automatic pings); every
  active-user query filters them out.
- **C3**: soft deletion: every query touching `users` filters `deleted_at IS NULL`.
- **C4**: the ingest pipeline double-writes events; every count is
  `COUNT(DISTINCT event_uuid)`, never `COUNT(*)`.

**Coverage criterion, per item (pre-registered form)**: an item counts as covered only
if the authored skill *instructs the behavior* (e.g., "always exclude test accounts"),
not if it merely mentions the artifact (naming the `is_test` column without the rule
does not count). The per-item criteria table is frozen at M0 alongside the key.

---

## 3. Pre-registered assertions and consumer questions

### Producer-side assertions

1. **Validity**: the authored skill passes `quick_validate.py`.
2. **Coverage**: per-item, per the frozen criteria; reported as per-rep 0–10 scores and
   by tier. Scripted pattern hints assist, but **every one of the ~150 item judgments
   (15 artifacts × 10 items) is manually read**, not only flags — pilot-1 history
   (three grader revisions, all non-baseline "failures" grader artifacts) forbids
   trusting the script for the headline number.
3. **Process evidence (transcript-level, per arm)**: baseline-before-draft ordering;
   for T-WIRED, that W1 ran pre-draft with intent-only input and W2's key stayed out of
   consumer-visible paths; for T-CTL, whether it spontaneously tested at all (free
   signal, no assertion).

### Consumer questions (8 keyed + 2 sanity)

One question per tier-B/C item, one question per consumer run. Exact expected values
are computed from the seed data and frozen at M0; the predicted wrong value for each
question's most likely single-miss mode is recorded as a diagnostic. A pre-registered
**question × item sensitivity matrix** accompanies them, because overlap is
unavoidable (C1 touches nearly every count); scoring is per-question right/wrong
against the correct value, and item-level attribution is a secondary analysis read
through the matrix.

| Q | Primary item | Draft wording |
|---|---|---|
| Q-B1 | B1 | How many events were recorded in July 2026? |
| Q-B2 | B2 | Which account generated the most events in June 2026? |
| Q-B3 | B3 | What was the average session duration, in minutes, in July 2026? |
| Q-B4 | B4 | What is our current total MRR in dollars from active subscriptions? |
| Q-C1 | C1 | How many accounts signed up in Q2 2026? |
| Q-C2 | C2 | How many monthly active users did we have in July 2026? |
| Q-C3 | C3 | How many registered users do we have right now? |
| Q-C4 | C4 | How many `export` events occurred in July 2026? |
| Q-S1 | none | How many pricing plans exist? |
| Q-S2 | none | Which tables does the analytics database contain? |

Sanity questions separate "consumer cannot drive SQL at all" from "the skill lacks the
knowledge".

**Grading, layer (b)**: deterministic script, exact value match, plus the doctrine's
mandatory manual read of every flagged run; when a grader fix moves the failure
pattern, everything newly flagged is re-read. **Logged doctrine deviation**: the
skill's benchmarking doctrine defaults to a grader agent; the executable fixture makes
a deterministic script strictly better here. This is a finding about when the
grader-agent default should be bypassed, recorded regardless of outcomes.

---

## 4. Treatments, reps, budget

- **Producers**: 3 arms × P=5 = **15 Fable clean-slate runs** (each 10–20 min,
  `--dangerously-skip-permissions`, per-run profile copy, cwd = fresh staged fixture
  copy in a temp path, `--add-dir` exposes only the treatment skill; T-CTL drops it).
  Prompts identical except the one treatment sentence. Shared prompt (frozen verbatim
  at M0) contains: the naturalistic task ("make a skill for querying our analytics data
  so agents get correct numbers; put it at ./skills/analytics-queries/"), the executor
  floor disclosure ("cheap haiku-class agents will use it to answer questions"), and
  the away-from-keyboard grant ("I'm away; make reasonable assumptions"). Floor
  disclosure biases the control upward, the tolerable direction.
- **Consumers**: Haiku (mandatory floor), 3 reps per artifact-question pair: 15 × 10 ×
  3 = **450 runs**, plus a **no-artifact consumer baseline** (10 × 3 = 30 runs). Each
  run: fresh staged fixture copy, `--add-dir` the frozen artifact, one question.
  Roughly 80 minutes at parallelism 6 with the committed harness scripts (adapted
  paths). A Sonnet confirmation pass is optional and unfunded unless a defect-class
  question arises.
- **Parents**: not in this campaign. **Escalation clause (pre-registered)**: if T-PI
  beats T-CTL on coverage by the decision-rule margin, fund one parent arm (choice of
  parent made then) against the frozen fixture; the full grid only if that is
  ambiguous.
- **Power honesty**: coverage items are correlated within a rep, so the unit is the rep
  (0–10 score), not 10P Bernoullis (this corrects the handoff's sketch). At P=5,
  ~25-point deltas stand alone; smaller deltas are adjudicated by the mandatory manual
  layer and reported as suggestive, not claimed.

Total: 15 producer + ~480 consumer subprocess runs, inside the scale the prior session
already executed, tilted toward cheap Haiku runs.

---

## 5. Decision rules (pre-committed)

### Gates, checked before any treatment conclusion

- **Question gate (M0, before wave 1)**: run the 30 no-artifact consumer baseline runs
  first. Any keyed question answered correctly in ≥2 of 3 baseline reps is broken
  (answerable without the planted knowledge) and is revised before producers run.
- **Fixture gate (after wave 1)**: if T-CTL mean coverage ≥ 70%, the fixture created no
  discovery pressure: harden tier-B/C items and re-run wave 1. If T-PI saturates both
  metrics (coverage ≥ 90% **and** consumer accuracy ≥ 90%), harden before funding
  wave 2 — the wiring A/B cannot show lift against a ceiling.

### Discovery question (T-CTL vs T-PI). Margin: **+2.5 items (25 points) mean coverage**

| Outcome | Committed change |
|---|---|
| T-PI wins coverage (≥ margin) and consumer accuracy | README gains the discovery claim with numbers; the fully-specified-task caveat gets its measured counterpart |
| Coverage ties, T-PI wins accuracy | README claims the value is in how knowledge is *encoded*, not found |
| T-PI wins coverage, accuracy ties | No new claim; investigate encoding vs question validity first |
| Full tie | README caveat sharpens to its bluntest: value is process evidence and regression protection only; the hypothesis is recorded dead |

### Wiring ship/no-ship (T-PI vs T-WIRED), asymmetric evidence bar

Ship W1+W2 into SKILL.md and testing.md **iff all three hold**:

1. **No regression**: T-WIRED mean consumer accuracy ≥ T-PI − 5 points (any flagged
   regression manually read before it counts).
2. **Mechanism**: in **≥ 2 of 5** wired reps, transcripts show a W1 eval failure or a
   W2 trap catching a real defect that traceably changed the artifact before shipping.
3. **Cost**: median T-WIRED producer duration ≤ 1.5 × median T-PI duration (tokens and
   duration recorded per run either way).

If the steps run but never catch anything, that is no-op wiring — sediment by the
skill's own failure catalog — and the result ships as a **negative-result row** in the
README evals table, exactly like the floor-doctrine A/B. If mechanism fires but
accuracy regresses: investigate, default no-ship. The asymmetry (mechanism-plus-
no-regression instead of a statistical delta) is deliberate: at P=5 a significance bar
would default working cheap wiring to no-ship.

---

## 6. Run schedule

- **M0 — freeze (no producer runs before this completes)**: build fixture + seed data;
  compute and freeze the key, per-item coverage criteria, question wordings, expected
  answers, and the sensitivity matrix; build T-WIRED treatment copy; adapt harness
  scripts; verify scrubbed profiles (distinctive-rule probe answering "none"); run the
  question gate (30 baseline consumer runs); commit everything under
  `campaigns/underspecified-authoring/`.
- **M1 — wave 1**: T-CTL ×5 and T-PI ×5 producers (same wave, per-run profiles);
  freeze artifacts; validity + coverage grading with full manual reads; consumer batch
  for these 10 artifacts (300 runs).
- **M2 — gate check**: evaluate the fixture gate. Pass → M3. Fail → harden fixture,
  re-freeze, repeat M1 (recorded, not silent).
- **M3 — wave 2**: T-WIRED ×5 producers; grading; consumer batch (150 runs);
  transcript attribution for the mechanism criterion.
- **M4 — analysis and changes**: apply section 5 mappings; write the README evals-table
  row and the findings note (doctrine deviations observed while eating this cooking,
  starting with the grader-agent bypass); evaluate the parent-escalation clause;
  ephemeral run records to `.skill-creator/`, durable results committed here.

## 6b. M0 amendments (2026-08-10, recorded before wave 1)

M0 completed with the question gate **passing for all 8 keyed questions**
(details and evidence: `key/M0-gate-results.md`). Two revisions, both via
pre-registered fallback paths:

1. **Consumer visibility**: consumer-staged fixture copies exclude `queries/`
   (bare consumers ran the canonical queries verbatim — transcript-verified
   pre-cooked answers). Producers keep the full repo. This sharpens the
   deployment story: consumers get data plus docs; the conventions must come
   from the skill.
2. **Execution mode**: all subprocess batches run sequentially with a fresh
   pre-batch credential export (upstream OAuth race, claude-code #24317 and
   #20553; see `harness/README.md` note 4). Wave-1 wall-clock estimates in
   section 4 are superseded: ~10 producer runs remain hours-scale, but the
   ~300-run wave-1 consumer batch is now an overnight-scale sequential job
   unless the upstream fix lands or the user opts into `ANTHROPIC_API_KEY`
   auth (billing change, user decision, out of M0 scope).

Grader iterations at M0: 2 (QS2 multi-line answers), consistent with pilot
history; the mandatory-manual-read rule caught it.

## 7. Contamination checklist (applied, from established harness facts)

Per-run scrubbed profile copies; subjects run from temp-staged fixture copies outside
the repo (clean ancestry); the key, expected answers, and this plan are never inside a
subject-visible path; consumer runs see only the fixture copy and the frozen artifact
(never pi-skill-creator); baselines drop `--add-dir`; no `--bare`; `executor_model`
recorded per run; exported credentials deleted at campaign end.

# Decision memo (main thread — synthesis)

Write this yourself, after scoring. The memo is the product of the whole
validation: a document the user can actually act on. This is not a report —
it is a **decision brief**. It surfaces the most important signals, names
the riskiest assumption, and gives a concrete next action calibrated to the
founder's tier. A good decision memo makes the reader feel slightly
uncomfortable — that means it's honest. Writing it on the main thread lets
it draw on everything the specialists wrote AND the conversation itself.

## Input

- Idea slug
- `.idea-validation/ideas/<slug>/scores.json` (required — includes RAT)
- `.idea-validation/ideas/<slug>/weaknesses.json` (if available)
- `.idea-validation/ideas/<slug>/pivot_options.json` (if available and verdict is "pivot")
- All other available dimension files in `.idea-validation/ideas/<slug>/`
- `.idea-validation/user_profile.md` (for tier-appropriate recommendations)

## Writing Principles

The memo must be **scannable in under 2 minutes**. Follow these rules:

1. **No hedging.** "This might work if…" is banned. State the verdict and own it.
2. **Evidence over opinion.** Every strength and risk must cite a specific data point from a dimension file (k-factor, LTV:CAC ratio, D30 retention, WTP range, etc.).
3. **Asymmetric emphasis on risks.** Humans overweight strengths and underweight risks. The memo corrects for this by giving risks more detail than strengths.
4. **One clear next action.** Not three options — one. The alternative path exists only as a contingency.
5. **Respect the founder's tier.** Don't tell a beginner to "optimize your Meta ads funnel." Don't tell a growth-tier founder to "watch some TikTok tutorials."

## Formatting Constraints

| Section | Max length | Purpose |
|---|---|---|
| Verdict line | 1 sentence | Instant signal |
| Score + confidence | 1 line | Quantitative anchor |
| Validation watermark | 1–2 lines | Trust calibration (only if confidence < high) |
| Top 3 Strengths | 1 sentence each, with one data point | What's working |
| Top 3 Risks | 2 sentences each: the risk + what happens if ignored | What kills it |
| Riskiest Assumption | 3–5 sentences | The one thing to test before building anything |
| Pre-mortem | 3 bullet points | Failure imagination exercise |
| Recommended Next Step | 2–4 sentences with specifics | What to do this week |
| Kill criteria | 1–2 sentences | When to walk away |
| Alternative Path | 1–2 sentences | Plan B |
| Interview kit | 10 questions + 2–3 recruiting routes | Only when required (see below) — the desk-research escape hatch |

Total memo length: **~400–600 words** (+ the interview kit when required). If it's longer, cut. Brevity is a feature.

## Interview Kit (conditional section)

Include the kit when EITHER: (a) `scores.json.evidence_gate.triggered` is
true, or (b) `target` = b2b and the verdict is **pursue** or **test** for a
professional-firm niche (commercialisti, avvocati, consulenti del lavoro
and similar) — these markets under-produce public evidence, so even a
passing desk verdict should be interview-confirmed before building.

The kit contains:
1. **10 interview questions in Italian**, tailored to this idea's riskiest
   assumptions (not a generic script): current workflow and its cost in
   hours; the incumbent stack and what's tolerated about it; who decides
   and signs; budget norms ("quanto spendete oggi per..."); the specific
   pain's frequency/severity; reaction to the price band from
   `pricing.json`. Follow Mom-Test discipline: past behavior, not
   hypotheticals — "com'è andata l'ultima volta che...", never "lo
   usereste?".
2. **Recruiting routes** (2–3, concrete for this niche): ordine/association
   events and local sections, the verified-active communities from
   market_insights, the founder's named contacts from `user_profile.md`,
   LinkedIn direct engagement (public commenting → conversation — NOT cold
   email; the CAC pack's legal exclusion applies to outreach here too).
3. **A target**: 10–15 interviews, separating "has the pain" from "would
   pay/replace/integrate" — the interview outcomes become the RAT evidence.

## Process

1. Load `scores.json` and all available dimension files.
2. Check `score_confidence`. If not "high", compose a validation watermark (see below).
3. Identify the 3 highest-scoring dimensions → strengths. For each, pull one concrete data point from the source file (e.g., "k-factor estimated at 0.6" not "good viral potential").
4. Identify the 3 lowest-scoring dimensions → risks. For each, describe what goes wrong if ignored. If `weaknesses.json` exists, use its `root_cause_type` and `failure_mode` to add specificity.
5. Extract the RAT from `scores.json.riskiest_assumption_test`. Frame it as the one question to answer before writing a line of code.
6. Run a **pre-mortem**: assume the idea failed 12 months from now. Write 3 most likely causes of death based on the risk profile.
7. Compose the recommended next step:
   - If verdict = **pursue**: the next step is to build a scoped MVP (define what "scoped" means for this idea).
   - If verdict = **test**: the next step IS the RAT experiment from `scores.json`. Restate it with concrete specifics (channel, spend, threshold, timeline).
   - If verdict = **pivot**: the next step is the recommended pivot from `pivot_options.json` (if available) or running the pivot-optimization workflow.
   - If verdict = **drop**: the next step is to archive and move on. Name one thing learned from the analysis that applies to future ideas.
8. Define **kill criteria**: the specific outcome that means "stop and move on." This is the inverse of the RAT pass threshold.
9. Write the alternative path — what to do if the recommended step fails or the kill criteria is met.
10. Check the interview-kit condition (gate triggered, or b2b pursue/test in a professional-firm niche). If it applies, compose the kit: 10 Italian questions tailored to the RAT and the lowest-scoring dimensions, recruiting routes from market_insights + user_profile, and the interview target.
11. Write the memo following the template below.

### Validation Watermark

If `score_confidence` from `scores.json` is not "high", insert a watermark immediately after the score line:

| Confidence | Watermark |
|---|---|
| **medium** | "This score is based on incomplete data. {list missing dimensions}. Run these analyses before making a build/no-build decision." |
| **low** | "LOW CONFIDENCE — Only {N} of 6 dimensions scored. This verdict is directional, not conclusive. Required before acting: {list mandatory missing analyses}." |

If `evidence_gate.triggered` is true, the watermark must additionally say:
"DESK-LIMITED — only {observations_counted} in-market observations found
(threshold {threshold}). This market under-produces public evidence; the
score is capped and the interview kit below is the required next step."

### Pre-mortem Method

The pre-mortem is a proven debiasing technique (Klein, 2007). It forces the founder to imagine failure before committing resources.

Instructions:
1. Assume the idea launched and failed within 12 months.
2. Working backward from the risk profile and killer dimensions, write the 3 most probable causes of death.
3. Each cause must be specific and tied to a scored dimension — not generic ("ran out of money" is too vague; "CAC exceeded LTV by 4x because TikTok organic reach declined and no paid channel was viable under $500/mo" is useful).

## Output

Write to `.idea-validation/ideas/<slug>/decision_memo.md`:

```markdown
---
idea_slug: ""
verdict: "pursue | test | pivot | drop"
final_score: 0
score_confidence: "high | medium | low"
created_at: ""
---

# Decision Memo: <Idea Name>

## Verdict: <PURSUE / TEST / PIVOT / DROP>

**Score: X/100** | Confidence: <high / medium / low>

<Validation watermark — only if confidence is medium or low>

---

## Why This Score

<2–3 sentences explaining what the score means in plain language. Not a recap of methodology — a statement of what the analysis revealed about this idea's viability.>

## Top 3 Strengths

1. **<Dimension>** (<score>/100): <one sentence with specific data point>
2. **<Dimension>** (<score>/100): <one sentence with specific data point>
3. **<Dimension>** (<score>/100): <one sentence with specific data point>

## Top 3 Risks

1. **<Dimension>** (<score>/100): <the risk>. <what happens if ignored — the failure mode.>
2. **<Dimension>** (<score>/100): <the risk>. <what happens if ignored — the failure mode.>
3. **<Dimension>** (<score>/100): <the risk>. <what happens if ignored — the failure mode.>

## Riskiest Assumption

The assumption most likely to kill this idea:

> "<the assumption, stated plainly>"

**Test it before building anything.** <Restate the RAT experiment: what to do, how long, how much it costs, and what "pass" looks like.>

## Pre-mortem: If This Fails in 12 Months

1. <Most likely cause of death — specific, tied to data>
2. <Second most likely cause — specific, tied to data>
3. <Third most likely cause — specific, tied to data>

---

## What To Do Now

<The one recommended next step — concrete, specific, calibrated to founder tier. Include timeline and cost if applicable.>

**Kill criteria:** <The specific outcome that means stop. e.g., "If landing page converts below 5% after 200 visitors, drop this idea.">

## If That Doesn't Work

<Alternative path — one sentence. What to do if the recommended step fails or kill criteria is met.>

<!-- Only when the interview-kit condition applies (see Interview Kit section): -->

## Interview Kit

<1–2 sentences: why interviews are required for this verdict (gate fired / professional-firm niche).>

**Domande (10):**
1. <question in Italian, tailored to this idea's riskiest assumptions>
...

**Dove trovare gli intervistati:** <2–3 concrete recruiting routes for this niche>

**Target:** 10–15 interviste. Separate "ha il problema" da "pagherebbe / sostituirebbe / integrerebbe". <Tie to the RAT pass threshold.>
```

## Notes

- If the verdict is **pivot** and `pivot_options.json` exists, embed the recommended pivot in the "What To Do Now" section with enough detail to act on immediately.
- If the verdict is **drop**, the tone should be respectful but firm. Don't soften a drop verdict. The value of a good drop is the time it saves for the next idea.
- The memo should be re-generated whenever `scores.json` is updated (e.g., after a pivot re-score). Append a version note at the bottom: `_v2 — re-scored after [pivot description]_`.
- Decision memos are the primary artifact the user references after the session. Optimize for re-readability days later, not just first-read clarity.

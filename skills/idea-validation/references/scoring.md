# Scoring (main thread — synthesis)

Run this yourself. Scoring is the synthesis step: it aggregates the
specialists' dimension files into a single, defensible verdict using a
**multiplicative-floor algorithm** — a single catastrophic weakness kills
the score, just like it kills a real startup — and produces the **Riskiest
Assumption Test (RAT)** that converts the verdict into a concrete next
action. Keeping it on the main thread keeps the math auditable and lets the
memo inherit full conversational context.

## Contents

- Input and minimum viable input
- Scoring dimensions and rubrics
- Scoring algorithm (floor penalty, weights, missing-input discount)
- Screening mode (fresh candidates)
- Riskiest Assumption Test (RAT)
- Process and output schema

## Input

- Idea slug
- One or more of the following from `.idea-validation/ideas/<slug>/` (use whatever is available): `idea.md`, `desire_scores.json`, `competitors.json`, `pricing.json`, `cac.json`, `market_size.json`, `distribution.json`, `retention.json`
- Optional: `.idea-validation/user_profile.md` (for founder-market fit)

### Minimum Viable Input

At least **3 of the 6 dimensions** must have source data. If fewer are available, refuse to score and list what's missing. Two dimensions are **mandatory** — Demand and Distribution. Without evidence of a real problem and a path to reach users, scoring is meaningless.

The one exception is **Screening Mode** (below), used by the idea-generation workflow to rank fresh candidates that have only an `idea.md`. Screening produces a separate artifact and never writes `scores.json`.

## Scoring Dimensions

| Dimension | Weight | Source | What it measures |
|---|---|---|---|
| Demand | 20% | `desire_scores.json` + `idea.md` | Real human desire + validated market signals |
| Competition | 10% | `competitors.json` | Positioning gaps and defensibility |
| Monetization | 20% | `pricing.json` + `cac.json` + `market_size.json` | Unit economics viability (LTV:CAC, WTP, market size) |
| Distribution | 20% | `distribution.json` | Organic reach, paid viability, founder edge |
| Retention | 15% | `retention.json` | Habit formation, churn risk, usage frequency |
| Founder-Market Fit | 15% | `user_profile.md` + domain overlap with idea | Builder's edge, domain expertise, distribution advantage |

## Dimension Score Mapping

Each dimension maps source data to a 0–100 sub-score using the target's rubric pack. Read the idea's `target` from `idea.md` frontmatter (absent → `b2c`), then **read `references/calibration/<target>/scoring-rubrics.md` now** — it holds the six dimension mapping tables and their adjustments. Apply those conversions to produce the sub-scores.

## Scoring Algorithm

### Step 1 — Compute dimension sub-scores

Apply the mapping rubrics above. Record each as `d_i` (0–100).

### Step 2 — Apply floor penalty (the "Killer Dimension" rule)

Any dimension scoring below **25** is a potential startup killer. Apply this penalty:

```
floor_penalty = 1.0
for each dimension d_i:
    if d_i < 25:
        floor_penalty *= (d_i / 25)
```

This multiplicative penalty means a single catastrophic weakness (score 0–10) can halve or destroy the final score, regardless of how strong other dimensions are. This reflects startup reality: brilliant distribution cannot save a product nobody wants.

### Step 3 — Compute weighted base score

```
weights = {
    demand: 0.20,
    competition: 0.10,
    monetization: 0.20,
    distribution: 0.20,
    retention: 0.15,
    founder_market_fit: 0.15
}

base_score = sum(d_i * w_i for each dimension)
```

### Step 4 — Apply floor penalty and missing-input discount

```
missing_discount = available_dimensions / 6
adjusted_score = base_score * floor_penalty * missing_discount
final_score = round(clamp(adjusted_score, 0, 100))
```

A dimension scored with a rubric-pack *default* because its source file is
absent (e.g. founder-market fit at neutral 50 with no `user_profile.md`)
still contributes its default to the base score but counts as UNAVAILABLE
for `missing_discount` — defaults are placeholders, not evidence.

The missing-input discount caps what partial analysis can return: 3 of 6 dimensions ceilings the score at 50 ("pivot"), 4 of 6 at 67 ("test"). A "pursue" verdict requires all 6.

### Step 5 — Determine confidence level

| Available dimensions | Confidence |
|---|---|
| 6 of 6 | high |
| 4–5 of 6 | medium |
| 3 of 6 (minimum) | low |

### Step 5b — Evidence-sufficiency gate

Some target markets under-produce public evidence (thin review culture,
private communities), which makes thin-data scores read stronger than they
are. The target's rubric pack (`references/calibration/<target>/scoring-rubrics.md`)
may define an **evidence gate**: a rule for counting in-market observations
across this niche's `market_insights/` files, and a threshold.

- If the pack defines no gate, skip this step (`evidence_gate.triggered` = false).
- If it does: count the observations per the pack's rule. Below the
  threshold, the gate fires: **cap `final_score` at 74** (verdict can be at
  most "test"), set `score_confidence` to "low", and record the gate block
  in the output. When the gate fires, condition (a) of the decision memo's
  interview-kit rule is satisfied — see `references/decision-memo.md` for
  the full rule and the watermark text.

The gate caps, it never boosts — abundant evidence earns nothing extra here.

The pack may instead define a **ring-coverage disclosure** (the b2c pack
does): count the ring-labeled findings across this niche's
`market_insights/` files per the pack's rule and write the counts to
`ring_coverage` in the output. The disclosure caps nothing and boosts
nothing — it makes the evidence's geography visible. When it reports zero
Ring-1 (`IT`) findings, the decision memo adds the NO-RING-1 watermark —
see `references/decision-memo.md`.

### Step 6 — Issue verdict

| Score | Verdict | Meaning |
|---|---|---|
| 75–100 | **pursue** | Strong across dimensions. Build an MVP. |
| 55–74 | **test** | Promising but unproven. Run the RAT experiment first. |
| 35–54 | **pivot** | Structural weakness. Run pivot analysis to explore alternatives. |
| 0–34 | **drop** | Fatal flaws. Move to next idea. |

## Screening Mode (fresh candidates only)

Screening ranks freshly generated candidates so the user can pick 1–2 for full validation. It is a coarse re-projection of the trend evidence already embedded in each `idea.md` — not a validation. It runs when the idea-generation workflow asks for it, or when the only available input for an idea is its `idea.md`.

For each candidate, compute a screening score from the `idea.md` frontmatter:

| Signal | Contribution |
|---|---|
| `confidence` | high = 70, medium = 50, low = 30 (base) |
| `cross_platform_resonance` = true | +10 |
| `monetization_validated` = true | +10 |
| `trend_velocity` | rising-fast +10 · rising +5 · stable 0 · declining −15 |

Clamp to 0–100. Recommendation bands: ≥ 70 → `validate` (send to full validation first), 50–69 → `consider` (validate if it fits the user's profile), < 50 → `deprioritize`.

Write to `.idea-validation/ideas/<slug>/screening_scores.json` for each candidate:

```json
{
  "mode": "screening",
  "screening_score": 0,
  "signals_used": {
    "confidence": "",
    "cross_platform_resonance": false,
    "monetization_validated": false,
    "trend_velocity": ""
  },
  "recommendation": "validate | consider | deprioritize",
  "rationale": ""
}
```

Present all candidates as one ranked table. Screening scores are not comparable to full validation scores — never mix the two in a ranking, and never issue a pursue/test/pivot/drop verdict from a screening score. `scores.json` is written only by full scoring, which is what downstream workflows (pivot-optimization, decision memo) check for.

## Riskiest Assumption Test (RAT)

Every idea rests on assumptions. The RAT identifies the single assumption that, if wrong, kills the idea — and designs the cheapest possible experiment to test it before building anything.

### RAT Identification Process

1. **List all assumptions** embedded in the idea (drawn from dimension scores and source data):
   - Demand: "People actually have this problem and will seek a solution"
   - Monetization: "Users will pay €X/mo for this"
   - Distribution: "We can reach users via [channel] at acceptable cost"
   - Retention: "Users will come back [frequency]"
   - Competition: "Our differentiator matters to users"
   - Founder fit: "I can build this with my current skills/resources" (using user_profile.md if available)

2. **Rank by two axes** (each 1–5):
   - **Criticality**: If wrong, how dead is the idea? (5 = instant kill)
   - **Uncertainty**: How little evidence do we have? (5 = pure speculation)

3. **RAT = assumption with highest (criticality × uncertainty)**. Ties broken by criticality.

### RAT Experiment Design

For the identified RAT, design an experiment following these constraints:

| Constraint | Requirement |
|---|---|
| Time to run | ≤ 2 weeks |
| Cost to run | ≤ €100 (indie budget) |
| Signal type | Behavioral (what people DO, not what they SAY) |
| Sample size | Minimum credible: 30 responses or 100 landing page visitors |

#### Experiment types by assumption category

| Assumption category | Experiment template |
|---|---|
| Demand exists | Landing page with email capture. Pass: ≥ 10% signup rate from ≥ 100 targeted visitors. |
| WTP is real | Landing page with price shown + "buy" button (payment step). Pass: ≥ 3% click-to-buy from ≥ 100 visitors. |
| Distribution works | Run 1 channel for 7 days (e.g., 5 TikToks, 10 Reddit posts, ASO test). Pass: CAC below modeled threshold. |
| Retention holds | Concierge MVP or manual-ops version with 10–30 users for 14 days. Pass: ≥ 3 return sessions per user. |
| Differentiator matters | Show competitor + your concept side-by-side to 30 target users. Pass: ≥ 60% prefer your concept. |

### Pass/Fail Threshold

Define the threshold **before** running the experiment. The threshold is written into `scores.json` so it can be evaluated later. Thresholds must be:
- **Specific**: a number, not "good engagement"
- **Time-bound**: measured within the experiment window
- **Binary**: pass or fail, no "sort of passed"

## Process (step by step)

0. If this is a screening request (fresh candidates with only `idea.md`), follow Screening Mode above and stop — none of the steps below apply.
1. Load all available dimension files from `.idea-validation/ideas/<slug>/`.
2. Check minimum viable input; if not met, refuse and list missing inputs.
3. Map sub-scores per the rubric pack.
4. Compute the floor penalty.
5. Compute the base score.
6. Apply the floor penalty and missing-input discount.
7. Determine `score_confidence`.
7b. Apply the evidence-sufficiency gate if the target's rubric pack defines one (cap at 74 + confidence "low" when it fires).
8. Issue the verdict from the threshold table.
9. Identify `top_strengths` (top 3 dimensions) and `top_weaknesses` (bottom 3 dimensions).
10. Run RAT identification: list assumptions, score criticality × uncertainty, select the riskiest.
11. Design RAT experiment with pass/fail threshold.
12. If this is a pivot re-score, write to `pivot_scores.json` instead.

## Output

Write to `.idea-validation/ideas/<slug>/scores.json` (or `pivot_scores.json` for re-scores):

```json
{
  "dimension_scores": {
    "demand": 0,
    "competition": 0,
    "monetization": 0,
    "distribution": 0,
    "retention": 0,
    "founder_market_fit": 0
  },
  "weights_applied": {
    "demand": 0.20,
    "competition": 0.10,
    "monetization": 0.20,
    "distribution": 0.20,
    "retention": 0.15,
    "founder_market_fit": 0.15
  },
  "floor_penalty": 1.0,
  "base_score": 0,
  "missing_discount": 1.0,
  "evidence_gate": {
    "triggered": false,
    "observations_counted": 0,
    "threshold": 0,
    "rule": "<the counting rule applied, from the target's rubric pack — or 'none defined'>"
  },
  "ring_coverage": "<b2c only: {\"IT\": 0, \"EU-EN\": 0, \"Western\": 0} — ring-labeled finding counts per the b2c rubric pack's disclosure rule; omit for b2b>",
  "final_score": 0,
  "verdict": "pursue | test | pivot | drop",
  "sales_motion": "<b2b only: self-serve | assisted-self-serve | sales-led, from idea.md frontmatter — omit for b2c>",
  "score_confidence": "high | medium | low",
  "missing_inputs": [],
  "top_strengths": [
    { "dimension": "", "score": 0, "reason": "" }
  ],
  "top_weaknesses": [
    { "dimension": "", "score": 0, "reason": "" }
  ],
  "killer_dimensions": [],
  "riskiest_assumption_test": {
    "assumption": "",
    "category": "demand | monetization | distribution | retention | competition | founder_fit",
    "criticality": 0,
    "uncertainty": 0,
    "rat_score": 0,
    "experiment": {
      "type": "",
      "description": "",
      "duration": "",
      "estimated_cost": "",
      "pass_threshold": "",
      "fail_action": "pivot | drop | re-test with different channel"
    },
    "all_assumptions_ranked": [
      { "assumption": "", "criticality": 0, "uncertainty": 0, "rat_score": 0 }
    ]
  }
}
```

## Notes

- **Re-scoring pivots**: When scoring a pivot variant from `pivot_options.json`, write output to `.idea-validation/ideas/<slug>/pivot_scores.json`. Include a `pivot_id` field referencing the option.
- **Score decay**: If the newest dimension file is older than 90 days (a quarter — Italian pricing pages and regulatory deadlines routinely move within one), downgrade `score_confidence` one level (already "low" stays "low") and list the stale files in `missing_inputs` as "<file> (stale, analyzed <date>)".
- **Geometric vs. additive**: The floor penalty provides multiplicative dynamics (one zero kills the score) while the weighted sum provides interpretable dimension contributions. This hybrid outperforms pure additive (hides fatal flaws) and pure geometric (too punishing for moderate weaknesses).

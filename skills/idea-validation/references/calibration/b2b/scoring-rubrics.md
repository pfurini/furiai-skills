# Scoring rubrics — B2B calibration (Italy-first, self-serve micro-SaaS)

Loaded by the orchestrator (main thread) when scoring, per
`references/scoring.md`. Defines the six dimension score-mapping tables and
the evidence-sufficiency gate for the Italian B2B target. The algorithm —
weights, floor penalty, missing-input discount, gate mechanics, verdict
bands, RAT, screening — lives in `references/scoring.md`.

> Anchors marked (†) are grounded in the sourced benchmarks in the sibling
> B2B packs (ChartMogul churn bands, conversion report, TrustMRR cohorts,
> Italian pricing research 2026-08); unmarked anchors are provisional
> (`confidence: low`).

## Evidence-sufficiency gate (this target defines one)

**Counting rule:** across this niche's `market_insights/` files, count
distinct findings whose evidence labels mark an **Italian source** — region
label present (national/North/Centre/South/province), `geography: IT`, an
Italian-language quote, or `evidence type: member-assisted`. Findings
labeled `geography: non-IT` / global don't count. Count findings, not
files; the same pain seen on two surfaces counts twice (cross-surface
corroboration is signal).

**Threshold: 15 Italian-source observations.** Below it the gate fires (see
scoring.md: score capped at 74, confidence "low", memo must carry the
interview kit). Expect it to fire routinely for avvocati and other
low-public-signal verticals — that is the gate working, not failing.

## Demand (0–100)

| Condition | Score range |
|---|---|
| `desire_strength_label` = "strong" AND trend_velocity = "rising-fast" | 80–100 |
| `desire_strength_label` = "strong" OR trend_velocity = "rising" | 60–79 |
| `desire_strength_label` = "moderate" AND some signal validation | 40–59 |
| `desire_strength_label` = "weak" OR trend_velocity = "declining" | 15–39 |
| No signal data, speculation only | 0–14 |

Adjust within range: +10 if cross-surface resonance confirmed in Italian
sources, +5 if monetization_validated is true in `idea.md`, −10 if the
budget-authority driver scored ≤ 2 (real pain, no buyer), −5 if the pain's
answer in communities is delegation ("lo fa il commercialista") and the
idea targets the firm rather than the studio.

## Competition (0–100)

Higher = more favorable competitive landscape ("opportunity score").

| Condition | Score range |
|---|---|
| `market_saturation` = "low", clear positioning gaps, no incumbent-suite module | 75–100 |
| `market_saturation` = "medium", 1–2 positioning gaps identified | 50–74 |
| `market_saturation` = "high" but differentiation opportunities exist (incl. localization/compliance gaps of global leaders) | 25–49 |
| `market_saturation` = "high", no differentiation, suite incumbents own the workflow | 0–24 |

Adjust: +10 if a complaint cluster recurs across 2+ competitors' reviews
(Italian-language complaints weigh double). −15 if a TeamSystem/Zucchetti/
WK-class suite or the host platform ships the feature (absorption risk).

## Monetization (0–100)

| Condition | Score range |
|---|---|
| LTV:CAC ≥ 3:1 on at least 2 channels, WTP target €25–50/mo (at or below the self-serve ceiling), viable SOM | 80–100 |
| LTV:CAC ≥ 3:1 on 1 channel, WTP target ≥ €25/mo (†: the B2B ARPA line) | 60–79 |
| LTV:CAC ≥ 2:1, WTP target €10–25/mo, marginal unit economics | 35–59 |
| LTV:CAC < 2:1 OR viability_verdict = "not-viable" | 10–34 |
| No pricing data or CAC data | 0–9 (flag as missing) |

Adjust: +10 if `freemium_conversion_estimate` ≥ 8% (†: the B2B median). +5
if market_size_verdict = "large" after the buyer-redirection step. −10 if
the plan depends on a card-required trial in a cold Italian audience. −5 if
WTP target sits above €50/mo entry (sales-motion drift — should also show
in the guardrail band, see b2b/pricing.md "The €50/month line").

## Distribution (0–100)

| Condition | Score range |
|---|---|
| `distribution_verdict` = "strong", viral_loop_exists = true (team-expansion, client-artifact, or studio-multiplier loop) | 80–100 |
| `distribution_verdict` = "strong" OR (marketplace opportunity = "high" + advocacy fit = "high") | 60–79 |
| `distribution_verdict` = "moderate", at least one viable organic channel | 40–59 |
| `distribution_verdict` = "weak", paid-only path | 15–39 |
| No viable channel identified | 0–14 |

Adjust: +10 if founder has an existing audience, albo/community standing,
or an intermediary network (commercialisti/consulenti/resellers) relevant
to the niche. −5 if the plan leaned on cold outreach anywhere (it is
excluded in Italy — the CAC pack must already show `viable: false`).

## Retention (0–100)

Uses the B2B semantics from the retention pack (monthly churn = 100 − `d7`):

| Condition | Score range |
|---|---|
| `retention_verdict` = "sticky", projected monthly churn ≤ 2%, `habit_formation_score` ≥ 4 (the workflow-embedding reading) (†) | 80–100 |
| `retention_verdict` = "sticky" OR projected monthly churn ≤ 3% (†) | 60–79 |
| `retention_verdict` = "moderate", monthly churn 3–5% (†: around the $25–100 ARPA median) | 40–59 |
| `retention_verdict` = "disposable" OR monthly churn > 7% (†) | 15–39 |
| `churn_risk` = "high" AND no workflow embedding | 0–14 |

Adjust: +5 if usage recurs per-transaction or daily. −10 if the activation
cliff applies. −5 if the scadenza-bound or canone-resentment risk factors
both apply (deadline purchase in a subscription-resistant niche).

## Founder-Market Fit (0–100)

| Condition | Score range |
|---|---|
| Founder is (or was) the target operator, or has direct domain access through work/inner circle **in Italy** (incl. albo enrollment or an active intermediary network); builder/growth tier | 75–100 |
| Moderate domain overlap OR builder tier with adjacent professional experience and working Italian-market access | 50–74 |
| Beginner tier but high time commitment (≥ 20 hrs/wk) and named access to 3+ Italian target operators for feedback | 30–49 |
| No domain access, beginner tier, low time commitment | 0–29 |

Domain access weighs heavier here than in B2C, and in Italy it is
double-loaded: selling to operators requires their vocabulary AND reaching
them runs through communities/intermediaries that only admit insiders. A
founder who cannot name 3 Italian operators to interview will also trip the
evidence gate — score accordingly. If `user_profile.md` is unavailable,
default to 50 (neutral) and flag as missing.

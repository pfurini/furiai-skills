# Scoring rubrics — B2B calibration (self-serve / PLG micro-SaaS)

Loaded by the orchestrator (main thread) when scoring, per
`references/scoring.md`. Defines the six dimension score-mapping tables for
the B2B target. The algorithm — weights, floor penalty, missing-input
discount, verdict bands, RAT, screening — lives in `references/scoring.md`.

> Anchors marked (†) are grounded in the sourced benchmarks in the sibling
> B2B packs (ChartMogul churn bands, conversion report, TrustMRR cohorts);
> unmarked anchors are provisional (`confidence: low`) pending the
> source-hardening pass.

Each dimension maps source data to a 0–100 sub-score. When source data uses qualitative labels, apply these conversions.

## Demand (0–100)

| Condition | Score range |
|---|---|
| `desire_strength_label` = "strong" AND trend_velocity = "rising-fast" | 80–100 |
| `desire_strength_label` = "strong" OR trend_velocity = "rising" | 60–79 |
| `desire_strength_label` = "moderate" AND some signal validation | 40–59 |
| `desire_strength_label` = "weak" OR trend_velocity = "declining" | 15–39 |
| No signal data, speculation only | 0–14 |

Adjust within range: +10 if cross-platform resonance confirmed, +5 if monetization_validated is true in `idea.md`, −10 if the pain's budget-authority driver scored ≤ 2 (real pain, no buyer).

## Competition (0–100)

Higher = more favorable competitive landscape ("opportunity score").

| Condition | Score range |
|---|---|
| `market_saturation` = "low", clear positioning gaps, no dominant incumbent | 75–100 |
| `market_saturation` = "medium", 1–2 positioning gaps identified | 50–74 |
| `market_saturation` = "high" but differentiation opportunities exist | 25–49 |
| `market_saturation` = "high", no differentiation, dominant incumbents | 0–24 |

Adjust: +10 if a complaint cluster recurs across 2+ competitors' reviews. −15 if the host platform or a dominant suite vendor owns the category (absorption risk).

## Monetization (0–100)

| Condition | Score range |
|---|---|
| LTV:CAC ≥ 3:1 on at least 2 channels, WTP target ≥ $50/mo, viable SOM | 80–100 |
| LTV:CAC ≥ 3:1 on 1 channel, WTP target ≥ $25/mo (†: the B2B ARPA line) | 60–79 |
| LTV:CAC ≥ 2:1, WTP target $10–$25/mo, marginal unit economics | 35–59 |
| LTV:CAC < 2:1 OR viability_verdict = "not-viable" | 10–34 |
| No pricing data or CAC data | 0–9 (flag as missing) |

Adjust: +10 if `freemium_conversion_estimate` ≥ 8% (†: the B2B median). +5 if market_size_verdict = "large". −10 if the plan depends on a card-required trial in a cold-audience niche.

## Distribution (0–100)

| Condition | Score range |
|---|---|
| `distribution_verdict` = "strong", viral_loop_exists = true (team-expansion or client-artifact loop) | 80–100 |
| `distribution_verdict` = "strong" OR (marketplace opportunity = "high" + advocacy fit = "high") | 60–79 |
| `distribution_verdict` = "moderate", at least one viable organic channel | 40–59 |
| `distribution_verdict` = "weak", paid-only path | 15–39 |
| No viable channel identified | 0–14 |

Adjust: +10 if founder has an existing audience, community standing, or distribution partner in the niche.

## Retention (0–100)

Uses the B2B semantics from the retention pack (monthly churn = 100 − `d7`):

| Condition | Score range |
|---|---|
| `retention_verdict` = "sticky", projected monthly churn ≤ 2%, embedding score ≥ 4 (†) | 80–100 |
| `retention_verdict` = "sticky" OR projected monthly churn ≤ 3% (†) | 60–79 |
| `retention_verdict` = "moderate", monthly churn 3–5% (†: around the $25–100 ARPA median) | 40–59 |
| `retention_verdict` = "disposable" OR monthly churn > 7% (†) | 15–39 |
| `churn_risk` = "high" AND no workflow embedding | 0–14 |

Adjust: +5 if usage recurs per-transaction or daily. −10 if the activation cliff applies (value gated behind integration/setup most signups won't finish).

## Founder-Market Fit (0–100)

| Condition | Score range |
|---|---|
| Founder is (or was) the target operator, or has direct domain access through work/inner circle; builder/growth tier | 75–100 |
| Moderate domain overlap OR builder tier with adjacent professional experience | 50–74 |
| Beginner tier but high time commitment (≥ 20 hrs/wk) and named access to 3+ target operators for feedback | 30–49 |
| No domain access, beginner tier, low time commitment | 0–29 |

Domain access weighs heavier here than in B2C: selling to operators requires speaking their vocabulary, and community-based distribution requires authentic membership. If `user_profile.md` is unavailable, default to 50 (neutral) and flag as missing.

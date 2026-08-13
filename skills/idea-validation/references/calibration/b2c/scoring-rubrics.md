# Scoring rubrics — B2C calibration

Loaded by the orchestrator (main thread) when scoring, per
`references/scoring.md`. Defines the six dimension score-mapping tables for
the B2C target. The algorithm — weights, floor penalty, missing-input
discount, verdict bands, RAT, screening — lives in `references/scoring.md`.

## Evidence-sufficiency gate

This target defines **no evidence gate** (scoring.md Step 5b is skipped;
`evidence_gate.triggered` = false, rule = "none defined").

Each dimension maps source data to a 0–100 sub-score. When source data uses qualitative labels, apply these conversions.

## Demand (0–100)

| Condition | Score range |
|---|---|
| `desire_strength_label` = "strong" AND trend_velocity = "rising-fast" | 80–100 |
| `desire_strength_label` = "strong" OR trend_velocity = "rising" | 60–79 |
| `desire_strength_label` = "moderate" AND some signal validation | 40–59 |
| `desire_strength_label` = "weak" OR trend_velocity = "declining" | 15–39 |
| No signal data, speculation only | 0–14 |

Adjust within range: +10 if cross-platform resonance confirmed, +5 if monetization_validated is true in `idea.md`.

## Competition (0–100)

Higher = more favorable competitive landscape (counterintuitive — think of it as "opportunity score").

| Condition | Score range |
|---|---|
| `market_saturation` = "low", clear positioning gaps, no dominant incumbent | 75–100 |
| `market_saturation` = "medium", 1–2 positioning gaps identified | 50–74 |
| `market_saturation` = "high" but differentiation opportunities exist | 25–49 |
| `market_saturation` = "high", no differentiation, dominant incumbents | 0–24 |

Adjust: +10 if top competitor complaints reveal an unserved pain point. -15 if a FAANG-class player owns the category.

## Monetization (0–100)

| Condition | Score range |
|---|---|
| LTV:CAC ≥ 3:1 on at least 2 channels, WTP target ≥ $5/mo, viable SOM | 80–100 |
| LTV:CAC ≥ 3:1 on 1 channel, WTP target ≥ $3/mo | 60–79 |
| LTV:CAC ≥ 2:1, WTP target $1–$3/mo, marginal unit economics | 35–59 |
| LTV:CAC < 2:1 OR viability_verdict = "not-viable" | 10–34 |
| No pricing data or CAC data | 0–9 (flag as missing) |

Adjust: +10 if `freemium_conversion_estimate` > 5%. +5 if market_size_verdict = "large".

## Distribution (0–100)

| Condition | Score range |
|---|---|
| `distribution_verdict` = "strong", viral_loop_exists = true | 80–100 |
| `distribution_verdict` = "strong" OR (organic_reach = "high" + creator_economy_fit = "high") | 60–79 |
| `distribution_verdict` = "moderate", at least one viable organic channel | 40–59 |
| `distribution_verdict` = "weak", paid-only path | 15–39 |
| No viable channel identified | 0–14 |

Adjust: +10 if founder has existing audience or distribution edge (from `user_profile.md`).

## Retention (0–100)

| Condition | Score range |
|---|---|
| `retention_verdict` = "sticky", D30 ≥ 20%, habit_formation_score ≥ 4 | 80–100 |
| `retention_verdict` = "sticky" OR D30 ≥ 15% | 60–79 |
| `retention_verdict` = "moderate", D30 ≥ 8% | 40–59 |
| `retention_verdict` = "disposable" OR D30 < 8% | 15–39 |
| `churn_risk` = "high" AND no habit loop | 0–14 |

Adjust: +5 if natural_usage_frequency is daily. -10 if weekly-or-less with no external trigger.

## Founder-Market Fit (0–100)

| Condition | Score range |
|---|---|
| Strong domain match in `strong_domains`, distribution advantages align, builder/growth tier | 75–100 |
| Moderate domain overlap OR builder tier with adjacent experience | 50–74 |
| Beginner tier but high motivation and time commitment (≥ 20 hrs/wk) | 30–49 |
| No domain overlap, beginner tier, low time commitment | 0–29 |

If `user_profile.md` is unavailable, default to 50 (neutral) and flag as missing.

# CAC — B2C calibration

Loaded by `iv-cac-modeler` via the CALIBRATION path in its dispatch prompt.
Defines the budget tiers, channel set with CAC benchmarks, relevance
filters, and retention fallbacks for the B2C target. The LTV formula, ratio
thresholds, payback math, and viability verdict live in the agent brief.

## Contents

- Indie budget tiers
- Channel set and CAC benchmarks
- Channel relevance filter
- Lifespan mapping and D30 fallbacks

## Indie Budget Tiers

| Tier | Monthly ad/marketing spend | Who this is | Implication |
|---|---|---|---|
| **Bootstrap** | $0–$100/mo | Beginner or side-project builder | Paid channels are off the table. Must rely entirely on organic. |
| **Lean** | $100–$500/mo | Builder with some runway | Can test one paid channel with tight creative constraints. |
| **Moderate** | $500–$2,000/mo | Growth-tier or funded builder | Can run proper paid campaigns with A/B testing on one platform. |
| **Serious** | > $2,000/mo | Rare for indie; growth stage | Multi-platform paid, retargeting, influencer budgets. |

Map from `user_profile.md`: `budget_constraint` = "low" → Bootstrap. "medium" → Lean. "high" → Moderate or Serious (if ambiguous, model both and note the ambiguity for the orchestrator to resolve).

## Channel Set and CAC Benchmarks

These channel names are the keys of `cac_by_channel` in the output schema.

| Channel (schema key) | Base CAC range | Adjust down if | Adjust up if |
|---|---|---|---|
| **ASO organic** (`aso_organic`) | $0.50–$3.00 | ASO opportunity = "high" (from distribution.json); niche category with low competition | Saturated category; `market_saturation` = "high" from competitors.json |
| **Content / SEO** (`content_seo`) | $1.00–$8.00 | Niche has high search volume with low-quality top results; `rising` or `rising-fast` trend velocity | Competitive keywords dominated by established brands |
| **TikTok organic** (`tiktok_organic`) | $0.50–$5.00 | Niche is trending on TikTok (visible in market_insights top_signals); app produces shareable output (content-as-distribution loop) | Low TikTok engagement for this category; no visual hook |
| **Reddit / community** (`reddit_community`) | $0.50–$4.00 | Active communities discussing this problem (from Reddit market_insights); founder is an active community member | Small or inactive communities; product is hard to discuss authentically |
| **Paid social (Meta)** (`paid_social_meta`) | $3.00–$40.00 | Broad audience, visual product, low CPM niche | Competitive niche with high CPMs; narrow targeting required |
| **Paid social (TikTok)** (`paid_social_tiktok`) | $2.00–$25.00 | Trending niche (lower CPMs due to content volume); strong creative hook | Niche with limited content; poor demo-ability |
| **Influencer / creator** (`influencer`) | $2.00–$25.00 | Creator economy fit = "high" (from distribution.json); micro-influencers available in niche | Low creator fit; only macro-influencers relevant (expensive) |
| **Word of mouth / referral** (`word_of_mouth`) | $0.00–$2.00 | k-factor ≥ 0.3 (from distribution.json); inherent or collaborative viral loop | k-factor < 0.1; no natural sharing mechanic |
| **Press / Product Hunt** (`press_product_hunt`) | $0.00–$5.00 | Novel concept with clear narrative; uses new platform feature | Crowded launch day; "me too" product |

> Press/Product Hunt provides a one-time spike, not sustained acquisition. Model it as a fixed user cohort (typically 500–5,000 installs), not a recurring channel.

## Channel Relevance Filter

Not all channels apply to every idea. Skip channels that score "not applicable":

| Skip condition | Channels to exclude |
|---|---|
| App has no visual output or demo hook | TikTok organic, influencer |
| `budget_constraint` = "low" (Bootstrap tier) | Paid social (both), influencer (unless micro/barter) |
| No relevant online communities exist | Reddit / community |
| `viral_loop_exists` = false AND k_factor < 0.1 | Word of mouth / referral |
| Utility app with no narrative angle | Press / Product Hunt |

## Lifespan Mapping (from retention.json)

| D30 retention | Estimated avg lifespan | Rationale |
|---|---|---|
| ≥ 25% | 12–18 months | Strong retention; users who survive D30 tend to stay long |
| 15–24% | 6–12 months | Decent; typical for well-executed niche apps |
| 8–14% | 3–6 months | Below average; expect significant churn in months 2–3 |
| < 8% | 1–3 months | Disposable; most users gone within a billing cycle |

## D30 Fallbacks (when retention.json is unavailable)

These mirror the D30 column in the retention pack's benchmark table — keep the two in sync:

| Category | Median D30 |
|---|---|
| Social / messaging | 15–25% |
| Health & fitness | 10–18% |
| Finance / budgeting | 12–20% |
| Productivity / tools | 8–15% |
| Games (casual) | 5–12% |
| Education | 6–12% |
| Lifestyle / habit | 10–18% |
| Creative tools | 12–20% |

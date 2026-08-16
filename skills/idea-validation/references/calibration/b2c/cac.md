# CAC — B2C calibration (Italy-first rings)

Loaded by `iv-cac-modeler` via the CALIBRATION path in its dispatch prompt.
Defines the budget tiers, channel set with cost benchmarks, Ring-1 channel
units, relevance filters, and retention fallbacks for the B2C target. The
LTV formula, ratio thresholds, payback math, and viability verdict live in
the agent brief.

> **Honest framing (read before estimating):** the channel table's ranges
> are **cost per install (CPI)**, not cost per paying customer. Keep the
> two sides of the ratio at the same funnel stage: for freemium models the
> brief's ARPU already carries the free→paid conversion, so pair it with
> install-level cost — never divide the cost by conversion too (that
> double-counts). For subscription-only/paywall models, where ARPU is per
> paying user, convert: cost per paying user = CPI ÷ install→paying
> conversion (pricing pack's freemium/paywall rates). State which stage
> each figure is at. No published dataset covers solo founders at
> sub-€2,000/mo spend, and only two channels have genuine Italy-specific
> measurements (Apple Search Ads, Meta — see Ring-1 units).
> Organic-channel rows are **constructs** (`confidence: low`): organic
> acquisition has no published per-install price. Always report the
> derivation and mark absolute figures as estimates.

## Contents

- Budget tiers
- Ring-1 channel units (Italy — what is actually measured)
- Channel set and CPI benchmarks
- Channel relevance filter
- Lifespan mapping and D30 fallbacks

## Budget Tiers

| Tier | Monthly ad/marketing spend | Who this is | Implication |
|---|---|---|---|
| **Bootstrap** | €0–100/mo | Beginner or side-project builder | Paid channels are off the table. Must rely entirely on organic. |
| **Lean** | €100–500/mo | Builder with some runway | Can test one paid channel with tight creative constraints. |
| **Moderate** | €500–2,000/mo | Growth-tier or funded builder | Can run proper paid campaigns with A/B testing on one platform. |
| **Serious** | > €2,000/mo | Rare for indie; growth stage | Multi-platform paid, retargeting, creator budgets. |

Map from `user_profile.md`: `budget_constraint` = "low" → Bootstrap.
"medium" → Lean. "high" → Moderate or Serious (if ambiguous, model both and
note the ambiguity for the orchestrator to resolve). If `user_profile.md`
is absent, default to Bootstrap (the conservative tier — it excludes paid
channels, so it cannot overstate viability) and flag the gap in the
artifact.

## Ring-1 channel units (Italy — what is actually measured, 2025–2026)

Use these for Ring-1 modeling; they override the global table's ranges
where they exist. Everything not listed here has **no Italy-specific
measurement** — say so rather than relabeling a global figure.

| Channel | Italy unit | Source (date) | Confidence |
|---|---|---|---|
| Apple Search Ads | CPT **$0.87** · CPA **$1.60** — the lowest CPA of all tracked markets; **Italy ≈ 0.42× US CPA** (same dataset) | MobileAction Apple Ads benchmark (full-year 2025) | medium — absolute levels are single-vendor, but a second vendor corroborates the direction: SplitMetrics 2026 (CY2025, 91 markets) shows Italy dropping out of every top-15 cost ranking, bounding it at CPA < $2.42 and CPT < $1.51. Note: Apple adds a second search-results placement in March 2026 — re-check these units after it lands |
| Meta (FB/IG) | CPM median **€10.48** (range €6.88–15.60); CPC median ~**0,43–0,50** with the currency basis unresolved — carry the ratio: **~50% below the global median**. All-industries, not consumer-specific. No Italy CPI is published. | Superads country cut (windows ending mid-2026) | medium |
| Meta seasonality | Peak-to-trough **2.3×** within the year: autumn peak (Sep–Oct), troughs in April and mid-summer. Budget an autumn launch accordingly. | Superads Italy CPM series | medium |
| TikTok Ads | **No Italy benchmark from a disclosed dataset exists** — report as unknown, never estimate. Circulating "Italy TikTok CPM" figures trace to an AI-content citation ring. Platform budget floor: $30/day per ad group (EMEA). | verified 2026-08 | — |
| Google Ads (search) | Consumer-vertical planning ranges **€0.50–3.00** CPC (education/health toward the top, e-commerce the bottom); no disclosed-methodology Italy study exists; no Google App Campaigns CPI for Italy or Europe | Italian agency planning ranges (2026) | low |
| Cross-channel CPI | **No MMP publishes an Italy CPI cut** (AppsFlyer rolls Italy into a 17-country Western Europe region). Nearest labeled comparators: **Adjust 2026 Europe vertical CPIs** — e-commerce $2.25, finance $4.75 (2025; the only disclosed-methodology Europe cut found); global gaming $0.56, e-commerce $0.98, finance $1.13; EMEA blended ~$1.03. | Adjust Mobile App Trends 2026 (read directly) · verified 2026-08 | medium (Europe verticals) / low (blends) |
| Creator / influencer | Nano/micro floor **€100–300 per Instagram post** (nano tier, DeRev bands); engagement falls with tier size — the cost-per-engagement optimum is nano/micro on TikTok/IG; January is the cheapest month (demand −⅓). **No Italian app-install creator data exists** (no CPI norms, no rate card); Amazon.it affiliate pays **0% on Android apps**; ad-disclosure liability falls on the commissioning advertiser (AGCM fines; require the IAP Digital Chart wording by contract). | DeRev listino 2026 · AGCM 2025 actions | medium (rates) / high (legal) |

Planning assumption, label it as such: Italian consumer acquisition runs at
roughly **0.4–0.5× US cost** — measured on one channel only (Apple Search
Ads), extended to others as an assumption. The revenue side discounts at
least as much (US ad prices are pulling away from the rest of the world) —
cheaper installs do not mean better unit economics.

## Channel Set and CPI Benchmarks

These channel names are the keys of `cac_by_channel` in the output schema.
Ranges are **Ring-3/global cost per install**; organic rows are constructs.
Paid rows carry published anchors (Business of Apps CPI research, 2025-02 —
18 months old, flag; AdAction 2026 compilation).

| Channel (schema key) | Base CPI range (USD, global) | Adjust down if | Adjust up if |
|---|---|---|---|
| **ASO organic** (`aso_organic`) | $0.50–$3.00 (construct) | ASO opportunity = "high" (from distribution.json); niche category with low competition | Saturated category; `market_saturation` = "high" from competitors.json |
| **Content / SEO** (`content_seo`) | $1.00–$8.00 (construct) | Niche has high search volume with low-quality top results; `rising` or `rising-fast` trend velocity | Competitive keywords dominated by established brands |
| **TikTok organic** (`tiktok_organic`) | $0.50–$5.00 (construct) | Niche is trending on TikTok (visible in market_insights top_signals); app produces shareable output (content-as-distribution loop) | Low TikTok engagement for this category; no visual hook |
| **Reddit / community** (`reddit_community`) | $0.50–$4.00 (construct) | Active communities discussing this problem (from Reddit market_insights); founder is an active community member | Small or inactive communities; product is hard to discuss authentically |
| **Paid social (Meta)** (`paid_social_meta`) | $1.00–$5.50 (Business of Apps 2025 / AdAction 2026) | Broad audience, visual product, low CPM niche; Ring-1 campaigns (Italy runs ~50% below global CPM) | Competitive niche with high CPMs; narrow targeting required |
| **Paid social (TikTok)** (`paid_social_tiktok`) | $0.50–$4.00 (Business of Apps 2025 / AdAction 2026; global — no Italy cut exists) | Trending niche (lower CPMs due to content volume); strong creative hook | Niche with limited content; poor demo-ability |
| **Apple Search Ads** (`apple_search_ads`) | $1.60–$2.51 CPA (Italy 2025 full-year $1.60 — the measured Ring-1 floor; global $2.51) | Ring-1 campaigns (Italy is the cheapest tracked ASA market); tool/utility intent with searchable keywords | Category keywords owned by incumbents with big budgets; discovery-dependent app nobody searches for |
| **Influencer / creator** (`influencer`) | $2.00–$25.00 (construct — no published creator-CPI benchmark) | Creator economy fit = "high" (from distribution.json); micro-creators available in niche (Ring 1: nano floor €100–300/post) | Low creator fit; only macro-influencers relevant (expensive) |
| **Word of mouth / referral** (`word_of_mouth`) | $0.00–$2.00 per install (construct) | k-factor ≥ 0.3 (from distribution.json); inherent or collaborative viral loop | k-factor < 0.1; no natural sharing mechanic |
| **Press / Product Hunt** (`press_product_hunt`) | $0.00–$5.00 per install (construct) | Novel concept with clear narrative; uses new platform feature | Crowded launch day; "me too" product |

> Press/Product Hunt provides a one-time spike, not sustained acquisition.
> Documented outcomes (2025–2026 case studies): a **#1-of-the-day** finish
> lands ~600–1,000 signups/downloads; top-5 lands 100–400; a median
> (unfeatured) launch lands well under 500 visitors and minimal signups.
> Model it as a fixed cohort of ~100–1,000 installs scaled to the realistic
> finish, not as a recurring channel.

## Channel Relevance Filter

Not all channels apply to every idea. Skip channels that score "not
applicable":

| Skip condition | Channels to exclude |
|---|---|
| App has no visual output or demo hook | TikTok organic, influencer |
| `budget_constraint` = "low" (Bootstrap tier) | Paid social (both), influencer (unless micro/barter) |
| No relevant online communities exist (check ring-matched surfaces — four Italian niches have none: language learning, general cooking, parenting on Reddit, productivity-as-such) | Reddit / community |
| `viral_loop_exists` = false AND k_factor < 0.1 | Word of mouth / referral |
| Utility app with no narrative angle | Press / Product Hunt |

## Lifespan Mapping (from retention.json)

**Construct (`confidence: low`)** — no publisher maps D30 to expected
lifespan; the mapping is a churn-model heuristic:

| D30 retention | Estimated avg lifespan | Rationale |
|---|---|---|
| ≥ 25% | 12–18 months | Strong retention; users who survive D30 tend to stay long |
| 15–24% | 6–12 months | Decent; typical for well-executed niche apps |
| 8–14% | 3–6 months | Below average; expect significant churn in months 2–3 |
| < 8% | 1–3 months | Disposable; most users gone within a billing cycle |

## D30 Fallbacks (when retention.json is unavailable)

These mirror the D30 column in the retention pack's benchmark table — keep
the two in sync. They describe **well-executed subscription apps**, not
category medians (the published all-install D30 median is 2–7%; Adjust
2026: gaming 5%, e-commerce 3%, finance 2%); when the concept is visibly
weak, fall back to that floor instead, per the retention pack's rules.

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

# Market sizing — B2B calibration (self-serve / PLG micro-SaaS)

Loaded by `iv-market-sizer` via the CALIBRATION path in its dispatch prompt.
Defines the estimation proxies, conversion benchmarks, platform filters,
capture rates, and fallback prices for the B2B target. The triangulation
mechanism, SAM filter logic, reality checks, and verdict thresholds live in
the agent brief.

> **Bias warning (apply throughout):** every published indie-revenue source
> skews upward — acquisition marketplaces cover completed sales
> (twice-selected survivors), revenue-verification platforms cover opt-in
> survivors, and the one downward corrector (>54% of indie products earn $0;
> ScrapingFish n=937) is from 2022. Uncorrected, these numbers systematically
> overestimate what an indie builder captures. Estimate conservatively and
> say so.

## Intent Conversion Benchmarks (Approach A — search volume)

Provisional for B2B queries (`confidence: low` — no published B2B search-intent conversion study exists; anchored to B2B landing-page visitor→trial rates of 2.5–8.5%, First Page Sage 2025):

| Search intent | Conversion rate | Example query |
|---|---|---|
| Direct solution search ("software to X") | 5–12% | "client reporting software", "shopify inventory sync app" |
| Problem-aware search ("how to X") | 2–5% | "how to automate agency reports" |
| Category comparison ("best X software") | 4–10% | "best dental practice software" |
| Tangential professional interest | 0.5–2% | "agency workflow tips" |

## Community & Review Proxies (Approach B)

How many total potential buyers per observed community/review signal (provisional, `confidence: low`, except where sourced):

| Signal source | Multiplier | Rationale |
|---|---|---|
| G2 + Capterra reviews for top competitor | 30–60× customers per review | Few SMB buyers review; consistent with vendor-claimed customer counts vs. review counts |
| Niche professional subreddit / forum members | 10–30× | Operators join professional communities at higher rates than consumers join hobby ones |
| Marketplace installs of top competitor (where shown) | 1–3× | Installs ≈ customers in marketplaces; multiplier covers off-marketplace buyers |
| Niche newsletter/community subscribers | 5–20× | Professional newsletters reach a large share of a niche |
| Job postings mentioning the manual workflow | 50–200× businesses per posting | Only a fraction of firms with the pain hire for it at any moment |

## Business-Count Sources (Approach A-bis — bottom-up by population × ACV)

For B2B, the strongest TAM approach is `business_count × plausible ACV`. Canonical counts (cite the reference year — federal data lags 2–3 years by design):

| Population | Count | Source (reference year) |
|---|---|---|
| US nonemployer businesses (solopreneurs) | ~30.4M | Census Nonemployer Statistics (2023) |
| US employer firms < 500 employees | ~5.6M | Census SUSB / SBA (2023) |
| Per-industry establishment counts | look up by NAICS | Census SUSB; BLS QCEW for timelier data |
| Shopify live storefronts | ~2.9M (Store Leads, 2026; BuiltWith's ~6.9M counts parked/dev stores — don't use it) | secondary aggregators |
| Example vertical — US dentists | ~202K professionally active | ADA HPI (2024) |

There is no canonical count of "agencies" — NAICS 541810 vs 541613 under/over-count depending on definition; state which bucket you used.

## Platform Filter

When the product lives inside one ecosystem, SAM is bounded by that ecosystem's population (e.g. Shopify storefronts, Atlassian's ~300K customers, a platform's active developer count), further filtered by the segment that has the problem. Cite the ecosystem count and its date.

## SOM Capture Rates

Provisional capture bands (`confidence: low` — no published capture-rate data exists for indie B2B; derived from marketplace crowding: ~35% of Shopify apps have zero reviews, and 0.9% of Stripe-verified indie products are "breaking out"):

| Situation | Year 1 capture of SAM | Year 3 capture |
|---|---|---|
| Niche vertical, weak incumbents, founder has domain access | 0.5–2.0% | 2.0–5.0% |
| Marketplace category with ranking opportunity | 0.2–1.0% | 1.0–3.0% |
| Horizontal SMB tool, established competitors | 0.05–0.3% | 0.3–1.0% |
| Category with a dominant suite/platform incumbent | 0.01–0.1% | 0.1–0.5% |

Use the lower end when `market_saturation` = "high", founder is beginner tier, or no distribution edge exists; upper end with a distribution edge, marketplace opportunity = high, or `trend_velocity` = "rising-fast".

## Outcome Reality Check (mandatory — B2B addition to the agent brief's checks)

Cross-check every SOM estimate against the Stripe-verified indie cohort medians (TrustMRR via Indie Hackers, n=5,079, Mar 2026):

| Cohort | Median MRR |
|---|---|
| Year 0 | $148 |
| Year 1 | $334 |
| Year 2 | $656 |
| Year 4–5 | ~$2,400–$2,500 |
| 90th percentile (all ages) | ~$10,000 |
| "Breaking out" (>$10K MRR and >50% m/m growth) | 0.9% of products |

A SOM-year-1 estimate above ~$120K ARR (~$10K MRR) implies a **top-decile** outcome; above ~$500K ARR implies top-1% — either needs extraordinary justification (existing audience, locked distribution deal) or the estimate is wrong. State which percentile the estimate implies. Also note SaaS Capital (2026, n>1,000): median bootstrapped SaaS growth is 20%/yr — steep year-3 multiples need a named driver.

## Fallback Price (when pricing.json is absent)

Use the median competitive price from `competitors.json`, or $66/mo for marketplace apps (Shopify store-wide average, Jan 2025), or $29–$49/mo for standalone SMB tools (provisional).

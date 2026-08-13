# CAC — B2B calibration (self-serve / PLG micro-SaaS)

Loaded by `iv-cac-modeler` via the CALIBRATION path in its dispatch prompt.
Defines the budget tiers, channel set with CAC benchmarks, relevance
filters, and retention fallbacks for the B2B target. The LTV formula, ratio
thresholds, payback math, and viability verdict live in the agent brief.

> **Honest framing (read before estimating):** no published dataset covers
> solo founders at sub-$2,000/mo spend. Published per-channel B2B CAC
> figures (First Page Sage, ~120 firms, avg LTV $32K, 2025) are valid for
> **relative channel ordering** (referral < SEO < paid search < LinkedIn),
> not as absolute targets at indie scale. The transferable units are CPC,
> CPL, reply rates, and platform revenue shares — the per-customer ranges
> below are **derived from those units** and flagged `confidence: low`
> unless noted. Always report the derivation, and mark absolute CACs as
> estimates.

## Budget Tiers

| Tier | Monthly ad/marketing spend | Who this is | Implication |
|---|---|---|---|
| **Bootstrap** | $0–$100/mo | Solo founder, side project | Paid channels are off the table (B2B CPCs consume this in days). Organic + marketplace only. |
| **Lean** | $100–$500/mo | Builder with some runway | Can test narrow high-intent search keywords. LinkedIn ads not viable. |
| **Moderate** | $500–$2,000/mo | Growth-tier or funded builder | Real search campaigns + retargeting; niche newsletter sponsorships. LinkedIn only if ACV > $1,000/yr. |
| **Serious** | > $2,000/mo | Rare for indie | Multi-channel paid; still below the scale the published benchmarks describe. |

Map from `user_profile.md`: `budget_constraint` = "low" → Bootstrap. "medium" → Lean. "high" → Moderate or Serious (if ambiguous, model both and note it).

## Channel Set and CAC Benchmarks

These channel names are the keys of `cac_by_channel` in the output schema.

| Channel (schema key) | Indie-scale CAC estimate | Derivation / source | Adjust down if | Adjust up if |
|---|---|---|---|---|
| **Content / SEO** (`content_seo`) | $50–$300 effective (founder time) | Derived: cheapest scalable organic channel in every ranking; $647–$1,786 at mid-market scale (First Page Sage, 2025). `confidence: low` | Niche long-tail keywords with weak top results; rising trend velocity | Comparison keywords owned by vendor content and affiliate sites |
| **Marketplace organic** (`marketplace_organic`) | Rev-share + listing effort; near-$0 marginal CAC once ranked | Platform terms (verified 2025–26): Shopify 0% on first $1M lifetime then 15%; Atlassian Forge 0% on first $1M (2026) then 16–17%; Chrome $5 one-time, 0%. No install→paid funnel data is published anywhere — say so. `confidence: high` on the terms, `low` on funnel | Marketplace opportunity = "high" (from distribution.json); category with stale listings | Saturated category (`market_saturation` = "high"); ~35% of Shopify apps have zero reviews — ranking is the bottleneck |
| **Communities / founder-brand** (`communities`) | $20–$150 effective (founder time) | Qualitative only: 47% of bootstrapped founders call integrations/communities their most dependable 2025 channel (Freemius/MicroConf, ~700 founders). Zero cost-per-customer data exists. `confidence: low` | Founder authentically belongs to the niche community; active communities discussing the pain | Communities ban promotion; founder is an outsider |
| **Cold outbound** (`cold_outbound`) | $100–$400 effective per customer | Derived: B2B SaaS reply rates 2–4%, ~0.8–2 meetings per 100 sends (Instantly/Belkins, 2026) × founder time + tooling. `confidence: low` | Tight ICP list exists (marketplace sellers, license registries); high ACV | Low ACV (< $50/mo — the math never works); inbox-saturated audience |
| **Paid search** (`paid_search`) | $900–$4,700 per paying customer | Derived: CPL $66–$94 (WordStream, 13,474 campaigns, Apr 2025–Mar 2026) ÷ trial→paid 2–10%. `confidence: medium` on CPL, `low` on the division | Exact-match long-tail solution keywords; credit-card trial (higher trial→paid) | Broad category keywords; freemium entry (low conversion multiplies CPL) |
| **Paid social (LinkedIn)** (`paid_social_linkedin`) | $1,000+ per paying customer; generally not indie-viable | CPC $5.59 avg, CPL $221–$811 (Impactable, 2025 — single source, sample undisclosed). `confidence: low` | ACV > $1,000/yr and Moderate+ budget | Everything else — exclude by default at indie budgets |
| **Referral / word of mouth** (`referral_word_of_mouth`) | $0–$150 | Lowest-CAC channel in every published ranking ($150, First Page Sage). `confidence: medium` for ordering | k ≥ 0.2 from distribution.json (team-expansion or client-artifact loop); affiliate program at $20+/mo price | No loop; solitary back-office tool |
| **Integration partnerships** (`integration_partnerships`) | Effort-priced; near-$0 marginal | Directory listings route ecosystem users (Zapier/Slack/platform directories); no public funnel data. `confidence: low` | Tool completes a popular workflow gap in the ecosystem | No natural integration surface |
| **Launch platforms** (`launch_platforms`) | One-time cohort, not a channel | Product Hunt top-10: ~30–100 signups; top-3: ~100–400 (marketing-blog folklore, no methodology — treat as order-of-magnitude only). HN: no quantified data exists. `confidence: low` | Novel concept, builder-audience overlap | "Me too" product; B2B visitor→signup runs 1–2% |

> Launch platforms provide a one-time spike, not sustained acquisition. Model as a fixed cohort (tens to low hundreds of signups for B2B) and exclude from recurring channel viability.

## Channel Relevance Filter

| Skip condition | Channels to exclude |
|---|---|
| `budget_constraint` = "low" (Bootstrap tier) | Paid search, paid social (LinkedIn) |
| ACV < $50/mo | Cold outbound (economics never close), paid social (LinkedIn) |
| Product doesn't live in or near a platform ecosystem | Marketplace organic, integration partnerships |
| No identifiable operator communities | Communities / founder-brand |
| `viral_loop_exists` = false AND k_factor < 0.1 | Referral / word of mouth |
| Nothing novel to demo to a builder audience | Launch platforms |

## Lifespan Mapping (from retention.json — B2B semantics)

The retention specialist's B2B pack writes `d7` = month-1 logo retention and `d30` = month-3 logo retention. Derive monthly churn = 100 − `d7`, then:

| Monthly logo churn | Estimated avg lifespan | Rationale |
|---|---|---|
| ≤ 2% | 30–36 months (cap at 36 pre-launch) | Best-in-class embedding; ChartMogul top bands |
| 2–3% | 24–33 months | "Good" for the $25–100 ARPA band |
| 3–5% | 20–30 months | Around the $25–100 median (4.2%) |
| 5–7% | 14–20 months | Below median |
| > 7% | < 14 months | "Weak" band; disposable territory |

Lifespan ≈ 1 / monthly churn, capped at 36 months — median NRR in self-serve B2B is 82% (ChartMogul, 2025), so revenue decays inside surviving accounts too; an uncapped lifespan overstates LTV.

If `retention.json` is unavailable, assume the ChartMogul median for the idea's price band (e.g. 4.2%/mo at $25–100 ARPA → ~24 months) and flag LTV confidence as medium at best.

## Payback Reference Points

Median CAC payback at sub-$5K ACV (the closest published tier to indie): **9 months** (Benchmarkit, FY2024 data, 2025). Overall SaaS median is 16 months and rising (Aleph × Benchmarkit, 342 companies, FY2025). The agent brief's payback assessment table and Bootstrap red flag (> 3 months) still apply — an indie founder can't fund a 9-month gap the way a funded company can, so organic-first is the default recommendation at Bootstrap/Lean tiers.

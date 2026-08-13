# CAC — B2B calibration (Italy-first, self-serve micro-SaaS)

Loaded by `iv-cac-modeler` via the CALIBRATION path in its dispatch prompt.
Defines the budget tiers, channel set with CAC benchmarks, the Italian
legal exclusion, relevance filters, and retention fallbacks for the Italian
B2B target. The LTV formula, ratio thresholds, payback math, and viability
verdict live in the agent brief.

> **Honest framing (read before estimating):** no published dataset covers
> solo founders at sub-€2,000/mo spend, and **no Italy-cut ad benchmark with
> disclosed methodology exists** — every Italian CPC figure below is a
> planning range (`confidence: low` unless noted). What IS solid: the legal
> constraint (statutory), platform revenue-share terms (published), and the
> relative channel ordering (referral/organic < paid). Always report the
> derivation and mark absolute CACs as estimates.

## Contents

- Budget Tiers
- Legal exclusion (Italy — overrides everything)
- Channel Set and CAC Benchmarks (EUR)
- Channel Relevance Filter
- Lifespan Mapping (from retention.json — B2B semantics)
- Payback Reference Points

## Budget Tiers

| Tier | Monthly ad/marketing spend | Who this is | Implication |
|---|---|---|---|
| **Bootstrap** | €0–100/mo | Solo founder, side project | Paid channels off the table. Organic + marketplace + intermediary only. |
| **Lean** | €100–500/mo | Builder with some runway | Narrow high-intent Italian search keywords testable. LinkedIn not viable. |
| **Moderate** | €500–2,000/mo | Growth-tier or funded builder | Real search campaigns + retargeting; SMAU-class fair once a year eats most of this tier's annual budget — plan it as a discrete bet. |
| **Serious** | > €2,000/mo | Rare for indie | Multi-channel paid; LinkedIn floor (~€2K/mo) barely opens here. |

Map from `user_profile.md`: `budget_constraint` = "low" → Bootstrap.
"medium" → Lean. "high" → Moderate or Serious (if ambiguous, model both).
If `user_profile.md` is absent, default to Bootstrap (the conservative tier
— it excludes paid channels, so it cannot overstate viability) and flag the
gap in the artifact.

## Legal exclusion (Italy — overrides everything)

**Cold email and cold PEC are prohibited** without prior opt-in consent
(art. 130 d.lgs. 196/2003; Garante enforcement incl. €20K fine for
INI-PEC scraping, 2021). Public availability of the address is not a legal
basis; B2B status does not soften it; scraping INI-PEC/Registro Imprese for
outreach lists is independently unlawful. Therefore:

- Never model a CAC for cold email/PEC. The `cold_outbound` schema key gets
  `viable: false` with the legal reason.
- The lawful email path is **soft spam** (art. 130 co. 4: your own
  customers, similar products) — a retention/expansion channel, not
  acquisition.
- The lawful cold-contact bridge is **phone, to directory-listed and
  RPO-screened numbers, with a human operator, asking for consent** — then
  email after documented consent. Cost is founder time + RPO subscription;
  model it only if the founder explicitly plans it (effort-priced,
  `confidence: low`), and never for numbers scraped from websites or
  registries.

## Channel Set and CAC Benchmarks (EUR)

These channel names are the keys of `cac_by_channel` in the output schema.

| Channel (schema key) | Indie-scale CAC estimate | Derivation / source | Adjust down if | Adjust up if |
|---|---|---|---|---|
| **Content / SEO** (`content_seo`) | €50–300 effective (founder time) | Italian SERPs are less crowded than English ones for niche B2B terms, but Italian long-tail volume is low and publicly unmeasured — instrument with SEOZoom/DataForSEO before relying on it. `confidence: low` | Weak Italian top results; incumbent content is thin/dated | Volumes too small to matter; zero-click erosion |
| **Marketplace organic** (`marketplace_organic`) | Rev-share + listing effort; near-€0 marginal once ranked | Verified terms (2026-08): **Fatture in Cloud App Store — publication free, API free on all plans** (claimed 500K+ businesses, 16K accountants); TeamSystem Commerce partner rev-share; Shopify 0% first $1M then 15%. No install→paid funnel data published anywhere — say so. `confidence: high` on terms, `low` on funnel | Product attaches to FIC-class open ecosystem; category has stale listings | No marketplace exists for the niche (most Italian verticals — check first) |
| **Communities / founder-brand** (`communities`) | €20–150 effective (founder time) | Qualitative only. Italian surfaces are few and verified (Fisco Forum, r/commercialisti, association events) — presence is cheap but reach is capped; no cost-per-customer data exists. `confidence: low` | Founder authentically belongs (iscritto all'albo, operates in the niche) | Communities ban promotion; founder is an outsider; niche discussion is private/offline |
| **Intermediary referral** (`intermediary_referral`) | Near-€0 cash; relationship + enablement effort | The commercialista/consulente/reseller recommendation is how Italian micro-firms actually adopt software — but credibility holds only INSIDE the studio's own workflow (large trust gap outside it). No published economics. `confidence: low` | Tool serves or visibly helps the studio itself; studio-side value prop exists | Tool is invisible to intermediaries or competes with what they sell |
| **Events / fairs** (`events_fairs`) | One-time cohort; SMAU Milano ≈ €4,500+IVA a booth (regional de minimis programs can zero it for startup/PMI innovative) | Priced from published SMAU rates (2026). High-LTV channel class per MicroConf 2024 (conferences: 54% of >$5K-LTV companies). Lead quality real, volume modest. `confidence: medium` on cost, `low` on yield | ACV justifies it; founder can work a booth in Italian; regional funding available | Low ACV; no follow-up capacity (remember: no cold email after — collect consent AT the fair) |
| **Cold outbound** (`cold_outbound`) | **viable: false — prohibited in Italy** (see Legal exclusion) | Statutory; Garante enforcement record | — | — |
| **Paid search** (`paid_search`) | €300–1,500 per paying customer (planning range) | Derived: Italian B2B-intent CPC €1.50–4.00 (planning range, no methodology-disclosed study) × landing conv 2–5% × trial→paid 4–35%. A Milan/Rome +20–50% CPC premium circulates but traces to US-adapted or undisclosed-sample sources — treat it as an untested assumption, not a measurement. `confidence: low` throughout | Exact-match Italian long-tail solution keywords; card trial | Broad keywords; freemium entry; Q4 auction pressure |
| **Paid social — LinkedIn** (`paid_social_linkedin`) | Not viable below ~€2,000/mo (CPL ≈ €207, single source) | Impactable 2025 (LinkedIn, sample undisclosed). `confidence: low` | ACV > €1,000/yr AND Moderate+ budget | Everything else — exclude by default at indie budgets |
| **Paid social — Meta retargeting** (`paid_social_meta`) | CPC ~€0,43–0,50 (Superads Italy median; the page states no currency, so the level is unresolved — the defensible figure is the ratio: ~50% below the global median) — cheap retargeting of site visitors; thin cold-B2B decision-maker pool | Superads Italy country cut, all-industries. `confidence: low` | Retargeting warm site traffic with a self-serve offer | Cold prospecting for decision-makers; no traffic to retarget |
| **Referral / word of mouth** (`referral_word_of_mouth`) | €0–150 | Consistently the lowest-CAC channel across published rankings (no single citable source; confidence: low); peer advocacy through ordini/associations is the Italian variant | k ≥ 0.2 from distribution.json; client-facing artifacts; affiliate at €20+/mo price | No loop; solitary back-office tool |
| **Integration partnerships** (`integration_partnerships`) | Effort-priced; near-€0 marginal | FIC App Store listing, connector ecosystems (bindCommerce-class), Zapier; incumbent partner programs beyond FIC are contact-gated — model as slow. `confidence: low` | Tool completes a workflow gap in an open ecosystem | Target incumbent has no API (Danea-class) or partner-gates it (Zucchetti-class) |
| **Launch platforms** (`launch_platforms`) | One-time spike, heavily discounted for Italy | Product Hunt/HN audiences barely overlap Italian professional buyers — expect the low end of the global folklore range (tens of signups), near-zero for vertical niches. `confidence: low` | Dev-tool niche with international appeal | Italian vertical niche (skip) |

## Channel Relevance Filter

| Skip condition | Channels to exclude |
|---|---|
| Always (Italy, statutory) | Cold outbound (email/PEC) — `viable: false`, cite the law |
| `budget_constraint` = "low" (Bootstrap) | Paid search, paid social, events/fairs (unless regionally funded) |
| ACV < €50/mo | `paid_social_linkedin` (Meta retargeting can stay); events/fairs rarely pay back |
| Product doesn't attach to an open ecosystem | Marketplace organic, integration partnerships |
| Tool invisible/irrelevant to studi and resellers | Intermediary referral |
| No identifiable Italian communities discussing the pain | Communities / founder-brand |
| `viral_loop_exists` = false AND k_factor < 0.1 | Referral / word of mouth |
| Italian vertical niche with no international angle | Launch platforms |

## Lifespan Mapping (from retention.json — B2B semantics)

The retention specialist's B2B pack writes `d7` = month-1 logo retention and
`d30` = month-3 logo retention. Derive monthly churn = 100 − `d7`, then:

| Monthly logo churn | Estimated avg lifespan | Rationale |
|---|---|---|
| ≤ 2% | 36 months (the cap) | Best-in-class embedding; ChartMogul top bands |
| 2–3% | 33–36 months (cap at 36 pre-launch) | "Good" for the $25–100 ARPA band |
| 3–5% | 20–33 months | Around the $25–100 median (4.2%) |
| 5–7% | 14–20 months | Below median |
| > 7% | < 14 months | "Weak" band; disposable territory |

Lifespan ≈ 1 / monthly churn, capped at 36 months — median NRR in
self-serve B2B is 82% (ChartMogul, 2025), so revenue decays inside surviving
accounts too; an uncapped lifespan overstates LTV. Annual-billing note: when
the plan mix is annual-heavy (common in Italy), churn realizes at renewal —
lifespans cluster at 12/24/36 months rather than decaying smoothly; the cap
logic still holds.

If `retention.json` is unavailable, assume the ChartMogul median for the
idea's price band (e.g. 4.2%/mo at $25–100 ARPA → ~24 months) and flag LTV
confidence as medium at best.

## Payback Reference Points

Median CAC payback at sub-$5K ACV: **9 months** (Benchmarkit, FY2024). An
indie founder can't fund a 9-month gap — organic-first is the default at
Bootstrap/Lean tiers, and the survey base agrees: 63% of independent SaaS
use no paid advertising at all, and 57% of those who do either wait >7
months for ROI or don't know it (MicroConf 2024, directional). The agent
brief's payback table and Bootstrap red flag (> 3 months) still apply.

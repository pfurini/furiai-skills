# Pricing — B2C calibration (Italy-first rings)

Loaded by `iv-pricing-wtp` via the CALIBRATION path in its dispatch prompt.
Defines the pricing-model menu, premium multipliers, and benchmark tables
for the B2C target. The Van Westendorp mechanism and process live in the
agent brief.

> Benchmarks carry a **ring column**: EUR for Rings 1–2 (Italy /
> Europe-English), USD for Ring 3 (Western). Never mix currencies inside
> one table row. Figures carry source + date + confidence, or are marked
> **construct** — a calibration value with no public source. The tables
> report **observed prices charged**, not measured willingness to pay: an
> observed price is a supply-side equilibrium that already reflects
> competitive pressure. Use them as anchors, not as demand ceilings.

## Contents

- Ring-1 storefront mechanics (read first)
- Pricing models and selection criteria
- Demand-driver premium multipliers
- Price benchmarks by app category (ring columns)
- Freemium conversion estimation
- Annual vs. monthly strategy
- Secondary revenue path (B2B2C)

## Ring-1 storefront mechanics (read first)

Facts a solo developer pricing for Italy must know — all verified on the IT
storefront or Apple's own documentation, 2026-08, confidence high:

- **IT App Store prices are VAT-inclusive** (Italian standard VAT: 22%).
  The shelf price is what the customer pays.
- **A subscription price in Italy is a decision, not a conversion.** Apple
  price-equalizes paid apps and one-time IAPs (EUR never lands below the
  USD numeral) but **not auto-renewable subscriptions**: observed EUR/USD
  ratios on the same product run 0.80–1.20. Set the euro price directly;
  Apple will never adjust it for FX or tax.
- **Net proceeds from a 9,99 € sale ≈ 6,96 €** under the 15% Small Business
  Program commission (9,99 ÷ 1.22 = 8,19 € ex-VAT, minus commission); ≈
  5,73 € at the standard 30% (derived arithmetic, medium confidence).
- Euro price points have been stable since Oct 2022; the old tier ladder is
  superseded — ~800 price points, non-.99 endings observed live (22,00 €,
  39,95 €).
- **Weekly billing is an Italy-visible norm**, not a fringe tactic: Bending
  Spoons (Remini, Splice), Picsart, and Lightroom all run 3,99–11,49 €
  weekly plans on the IT storefront.
- Italian vendors do not price defensively by default: Bending Spoons
  prices above the US incumbents; Bear (Parma-founded) prices at the
  category floor. Both strategies coexist.

## Pricing Models

Indie sweet spots carry ring columns (Ring 1–2 EUR observed on the IT
storefront 2026-08, confidence high; Ring 3 USD anchored to the RevenueCat
subscription-price distribution, 2024 data via 2026 breakout, confidence
high — monthly Q1 $3.26 · median $6.68 · most common $9.99):

| Model | Best for | Risk | Ring 1–2 sweet spot (EUR) | Ring 3 sweet spot (USD) |
|---|---|---|---|---|
| **Freemium → subscription** | Habit-forming apps with daily use, feature-gated value | Conversion friction; most users stay free forever | 3–8 €/mo or 20–50 €/yr | $3–$8/mo or $20–$50/yr |
| **Subscription only (paywall)** | High-value, immediately obvious ROI, professional tools | High churn risk; must prove value fast | 5–15 €/mo | $5–$15/mo |
| **One-time purchase** | Utilities, tools with clear one-time value, privacy-focused apps | No recurring revenue; must rely on new users | 3–10 € (construct at sub-category level; observed IT anchors 6,99–29,99 €) | $3–$10 (construct) |
| **Weekly subscription** | Consumer AI/creative feature apps with immediate output | Highest-churn billing; reads as aggressive | 4–10 €/wk (observed IT norm) | $4–$10/wk |
| **Consumables / credits** | Variable usage (AI generations, exports, premium content) | Unpredictable revenue; usage may decline | 1–10 € per pack (observed IT: 0,99–29,00 €) | $1–$5 per pack (construct) |
| **Freemium + consumables** | Apps where core is free but power usage costs (AI, storage) | Complex to balance free vs. paid tiers | Free tier + 2–10 € packs | Free tier + $2–$10 packs (construct) |
| **Lifetime unlock** | Mature tier beside a subscription; launch-deal variant below | Caps LTV; price it high enough to protect the annual plan | Observed IT tiers run **8–15× annual** (34,99–329,99 €) | 8–15× annual (construct) |
| **Tip jar / patronage** | Content-focused, community-driven, or open-source-adjacent | Very low conversion; unreliable revenue | 1–5 € tips, rare (construct) | $1–$5 tips, rare (construct) |

### Model selection criteria

| If the app... | Recommended model |
|---|---|
| Has daily usage with progressively unlocked value | Freemium → subscription |
| Delivers immediate, obvious ROI in one session | Subscription only or one-time purchase |
| Produces output that varies in volume (AI, exports) | Freemium + consumables, or weekly subscription |
| Is a simple utility used occasionally | One-time purchase |
| Requires trust before users see value (health, finance) | Extended free trial → subscription |
| Competes with free alternatives that are "good enough" | Freemium (generous free tier) → subscription for power features |

## Demand-Driver Premium Multipliers

**Construct (`confidence: low`).** No published source relates a
psychological demand driver to a pricing multiplier; directional support
only (category price medians do put health ~2× gaming, the direction
"survival > curiosity" predicts). Driver strength from `desire_scores.json`
directly affects pricing power; the driver names key this table — do not
rename them.

| Primary desire driver | Premium multiplier | Rationale |
|---|---|---|
| **Survival** (health, safety, financial security) | 1.3–1.8× | Users pay more when stakes are high. Health and money apps can charge premium. |
| **Status** (achievement, appearance, signaling) | 1.5–2.0× | Status is inherently scarce — users pay for differentiation. Luxury/prestige positioning works. |
| **Belonging** (community, connection) | 1.0–1.3× | Users value belonging but expect community features to be free (social norms). Premium only for exclusive communities. |
| **Control** (mastery, organization, reducing chaos) | 1.2–1.5× | Moderate premium. Users pay for control when the alternative is stressful. |
| **Curiosity** (learning, discovery, novelty) | 0.8–1.2× | Lowest premium. Curiosity-driven apps compete with free content (YouTube, blogs). Must add structure/accountability to charge. |

If `desire_strength_label` = "weak", do not apply any multiplier — the app
lacks the emotional pull to justify premium pricing.

### Secondary driver bonus

If the secondary driver is different from the primary and scores ≥ 3, add a
+10% bonus (construct). Apps that tap two distinct desires (e.g., survival +
control in a health tracker) have stronger pricing power than single-desire
apps.

## Price Benchmarks by App Category (ring columns)

Ring 1 column: EUR prices observed live on the IT storefront, 2026-08,
VAT-inclusive, confidence high (ranges span the live SKUs of category
leaders and notable indies — the low end is usually an indie, the high end
a US-headquartered leader or clinical app). Ring 3 column: the original
global USD ranges — construct at sub-category level except where noted
(RevenueCat category medians confirm health & fitness $9.70/mo and
education $8.38/mo, 2024 data, confidence high).

| App category | Ring 1 observed monthly (EUR) | Ring 1 observed annual (EUR) | Ring 3 monthly (USD) |
|---|---|---|---|
| **Health & fitness** | 6,99–17,99 | 26,49–99,99 | $5–$15 (sourced) |
| **Nutrition / diet** | 8,90–14,99 | 35,00–99,99 | $5–$12 (construct) |
| **Meditation / mental health** | 8,99–15,99 | 45,00–69,99 | $5–$15 (construct) |
| **Finance / budgeting** | 3,99–15,49 | 29,99–119,00 | $3–$10 (construct) |
| **Productivity / task management** | 2,99–12,99 | 29,99–129,99 | $3–$8 (proxy-sourced) |
| **Habit tracking** | 0,99–10,99 | 5,99–79,99 | $2–$6 (construct) |
| **Creative tools (photo/video)** | 4,99–9,99 | 27,99–54,99 | $3–$10 (construct) |
| **Education / learning** | 5,99–16,99 | 31,99–125,99 | $5–$15 (sourced) |
| **Dating / social** | no IT anchor collected | — | $5–$25 (construct) |
| **Parenting / family** | 5,99–17,99 | 29,99–129,99 | $3–$8 (construct) |
| **Utility / scanner / converter** | 5,99–10,99 | 22,99–74,99 | $1–$4 (construct — and likely low: utilities monetize *above* intuition; Adapty 2026 reports utilities take 73.6% of revenue from weekly plans with the highest per-subscriber trial LTV) |
| **AI-powered tools** | 4,99–22,99 (assistants converge on 22,00–22,99 €/mo mid-tier, 229,00 € top tier) | 49,99–299,99 | $5–$20 (AI premium direction sourced: +41% Year-1 LTV vs non-AI, RevenueCat 2026) |

Reading the columns: the Ring-1 indie band is **4,99–9,99 €/mo** with
annual clustering at 29,99 / 39,99 / 49,99 / 59,99 / 69,99 €. The cheapest
credible subscription observed is 2,99 €/mo (Bear); the observed floor of
the whole sample is 0,99 €/mo (a solo-dev habit tracker). If an estimated
price sits more than 2× above the category's observed range, it is likely
too optimistic; below the category minimum, the app may struggle to sustain
development (sanity rule — construct).

Two Ring-1 category gaps worth knowing (2026-08): Italian-vendor finance
apps with national scale (Satispay, Revolut IT) and Italian mental-health
platforms (Serenis, Unobravo) expose **no in-app purchases** — they monetize
outside Apple billing, so those categories have no Italian-vendor anchor.

## Freemium Conversion Estimation

The overall level is sourced; the per-category split is a construct. Watch
the denominator: **free-user → paid** (OpenView: 3–5% good, 6–8% great,
2023; ChartMogul median 8% across products, 2026) is a narrower funnel than
**download → paid** (RevenueCat 2026: freemium apps 2.1% median at D35,
hard-paywall apps 10.7%). State which funnel an estimate uses.

If the recommended model includes a free tier, estimate conversion from
these factors (qualitative — construct):

| Factor | Higher conversion (toward 8–12%) | Lower conversion (toward 1–3%) |
|---|---|---|
| **Value gating** | Core value is free; premium unlocks power features or removes limits | Core value IS the paid feature — free tier feels empty |
| **Free tier generosity** | Generous enough that users form habits before hitting the wall | Either too generous (no reason to pay) or too stingy (users leave) |
| **Pain of free** | Free tier has clear, felt limitations (ads, watermarks, usage caps) | Free tier works fine for most users |
| **Social proof** | Users see premium features in action (shared content with branding) | No visibility into what premium offers |
| **Trial exposure** | Time-limited trial of premium (7–14 days) shows value upfront | No trial; users must imagine premium value |

**Category benchmarks for freemium conversion (free-user → paid;
per-category differentiation is a construct, `confidence: low` — no
publisher splits this by consumer category):**

| Category | Typical conversion rate | Top-quartile rate |
|---|---|---|
| Health & fitness | 2–5% | 8–12% |
| Productivity | 3–6% | 10–15% |
| Creative tools | 3–7% | 10–18% |
| Education | 2–5% | 7–12% |
| Finance | 3–6% | 8–14% |
| Utility | 1–4% | 5–10% |
| Social / dating | 2–8% | 10–20% |
| AI-powered | 4–8% | 12–20% |

Use the typical rate as the base estimate. Adjust toward top-quartile if:
- The desire_strength_label is "strong"
- The free tier design has strong value gating
- Category benchmarks from market_insights show successful freemium competitors

## Annual vs. Monthly Strategy

Most indie apps benefit from offering both monthly and annual plans, with
the annual plan as the anchor. **The published market average discount is
63–67% off the equivalent monthly price** (RevenueCat data, 2024–2026,
confidence high) — deeper than intuition suggests. Observed IT-storefront
annual discounts cluster at 40–60%.

| Discount depth | Effect |
|---|---|
| **20–30% off monthly** | Subtle incentive. Users who prefer monthly stay monthly. Low commitment-capture. |
| **40–60% off monthly** | The observed Ring-1 cluster. Meaningful savings without signaling desperation. |
| **60–70% off monthly** | The published market average — aggressive but normal, especially in high-churn categories where locking in annual users improves LTV. |
| **> 70% off monthly** | Signals the app isn't worth the monthly price. Avoid outside launch/promotional phases. |

**Recommended annual price** = monthly price × 12 × (1 − discount). Present
the annual plan as the default/highlighted option.

Category billing-mix anchors (RevenueCat 2026, confidence high): health &
fitness leads annual adoption (68%); gaming is 82% weekly; productivity is
76.7% monthly and draws 90.7% of revenue from monthly plans; education,
travel, and shopping favor annual (59–66%). Match the anchor plan to the
category's observed mix, not to a universal rule.

## Secondary Revenue Path (B2C vs. B2B2C)

Some ideas have a viable path to both consumer and business revenue.
Evaluate if the app concept could serve both — this fills the schema's
`b2b2c_potential` field:

| Signal that B2B2C path exists | Example |
|---|---|
| Users would expense the app to their employer | Productivity tools, professional development |
| A business version could serve teams | Shared dashboards, admin controls, team analytics |
| Content or data from the app has business value | Health data for employers, fitness for corporate wellness |
| The consumer app is a wedge into workplace adoption | Personal Slack → company Slack, personal Notion → team Notion |

If B2B2C path exists:
- **B2C price**: Use the standard WTP methodology (this is the consumer price).
- **B2B2C price**: 3–5× the consumer price per seat (construct). Businesses
  have larger budgets and lower price sensitivity.
- **Recommendation**: Launch B2C first (faster validation, faster feedback).
  Flag B2B2C as a future monetization expansion in the output.
- **Do NOT recommend B2B2C as the primary model** for an indie developer —
  sales cycles and support needs don't fit the indie model.

## Notes

- **Lifetime pricing has two distinct uses — don't conflate them.** A
  *launch-phase lifetime deal* is a discount tactic: 3–5× the annual price,
  used briefly for early-adopter cash and reviews, never the primary model.
  A *mature lifetime tier* beside a subscription is priced to protect the
  annual plan: observed IT-storefront tiers run **8–15× annual**
  (34,99–329,99 €, 2026-08, confidence high).
- For apps competing with strong free alternatives (Google Keep, Apple
  Notes, default apps), the effective WTP ceiling may be €0/$0 for most
  users. The pricing model must then create value the free alternative
  structurally cannot (social features, AI, specialized workflows).
- Web-checkout prices can undercut in-app prices (no Apple commission);
  vendors observably do this in Italy. Flag it as an option, not a default —
  it trades conversion friction for margin.

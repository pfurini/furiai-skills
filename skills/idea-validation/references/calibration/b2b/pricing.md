# Pricing — B2B calibration (self-serve / PLG micro-SaaS)

Loaded by `iv-pricing-wtp` via the CALIBRATION path in its dispatch prompt.
Defines the pricing-model menu, premium multipliers, and benchmark tables
for the B2B target. The Van Westendorp mechanism and process live in the
agent brief.

> Sources: entry-model conversion tables are ChartMogul × ProductLed SaaS
> Conversion Report (200 B2B products, Jan 2026) and ChartMogul GTM Report
> (2,500 companies, 2024–25) — `confidence: high`. Category price anchors
> are thin: the only defensible scrape is the Shopify App Store (Meetanshi,
> full-store scrape, Jan 2025); other category rows are provisional
> (`confidence: low`) pending the source-hardening pass. Driver premium
> multipliers are provisional constructs (`confidence: low`).

## Pricing Models

| Model | Best for | Risk | Indie sweet spot |
|---|---|---|---|
| **Flat monthly tier(s)** | Single-operator tools, clear job, predictable usage | Leaves seat-expansion revenue uncollected | $19–$79/mo, 2–3 tiers |
| **Per-seat subscription** | Team tools where value scales with people in it | Seat-count scrutiny at renewal; per-seat resentment is a top review complaint | $8–$25/seat/mo |
| **Usage-based / credits** | Value scales with volume (API calls, orders processed, AI generations) | Revenue unpredictability; bill-shock complaints | Base fee + usage; $0.01–$0.10/unit |
| **Freemium → paid tier** | Marketplace apps needing review velocity; tools with a natural power-user wall | Median freemium→paid is only 3–5%; free users cost support | Free tier + $19–$99/mo paid |
| **Free trial (no card) → paid** | Products needing days to show value | Median trial→paid 4–6% of signups | 14-day trial (most common), then $19–$99/mo |
| **Free trial (card required) → paid** | Obvious, fast-provable ROI | Fewer trials started; hostile for cold audiences | Same prices, 25–35% trial→paid typical |
| **Annual prepay discount** | Every model above, as the anchor plan | Deep discounts train buyers to wait for deals | 2 months free (≈ 17%) |
| **Lifetime deal (AppSumo-style)** | Launch cash + first users only | Destroys LTV; LTD buyers are support-heavy and never expand | Never the primary model |

### Model selection criteria

| If the product... | Recommended model |
|---|---|
| Is used by one operator with a recurring job | Flat monthly tiers |
| Gets more valuable as teammates join | Per-seat (with a flat small-team tier to blunt seat resentment) |
| Scales with transaction/usage volume | Usage-based with a base fee |
| Lives in a marketplace where reviews gate ranking | Freemium or generous trial (45.8% of Shopify apps offer a free plan/trial) |
| Proves ROI within one session (recovered revenue, instant report) | Card-required trial |
| Needs days of embedded usage before value shows | No-card 14-day trial |
| Competes with the platform's free native feature | Free tier covering parity + paid tier for the differentiator |

## Driver-Premium Multipliers

Keyed to `primary_driver` from `desire_scores.json` (B2B driver set). Provisional (`confidence: low`):

| Primary demand driver | Premium multiplier | Rationale |
|---|---|---|
| **ROI provability** | 1.5–2.0× | A tool that shows recovered revenue or counted hours prices against the value, not against competitors. |
| **Pain severity** | 1.3–1.8× | High-stakes pain (compliance exposure, lost clients) tolerates premium pricing. |
| **Pain frequency** | 1.2–1.5× | Daily pain justifies a subscription but each occurrence is small; moderate premium. |
| **Budget authority** | 1.0–1.3× | Easy purchase ≠ higher price; the buyer's no-approval threshold (~$50–100/mo for solo operators) caps it. |
| **Urgency** | 0.9–1.2× | Deadline-driven buyers pay list price fast but churn after; discounting premium invites regret-cancellation. |

Apply to the competitive modal price: `driver_adjusted_target = competitive_modal_price × driver_multiplier`. If `desire_strength_label` = "weak", apply no multiplier. Secondary-driver bonus: +10% if the secondary driver differs from the primary and scores ≥ 3.

## WTP Benchmarks by Category

| Category | Monthly WTP range | Evidence |
|---|---|---|
| Marketplace apps (Shopify et al.) | $10–$100/mo; store-wide average across all paid plans $66.54/mo | Full Shopify App Store scrape, Jan 2025 (`confidence: high` for e-commerce apps) |
| Solo-operator tools (freelancers, creators-as-business) | $9–$29/mo | Provisional (`confidence: low`) — below $25/mo ARPA churn is materially worse (ChartMogul band data), so treat sub-$25 pricing as a retention risk, not a growth hack |
| SMB team tools (agencies, small ops teams) | $29–$99/mo flat or $10–$25/seat | Provisional (`confidence: low`) |
| Vertical SMB SaaS (practice/venue management class) | $99–$499/mo per location — incumbents charge $249–$1,499/location (dental vertical, vendor-quoted, single source) | Provisional; indie entry sits below incumbent floor |
| Dev tools / API products | $19–$99/mo + usage | Provisional (`confidence: low`) |

Sanity rules: the B2B/B2C ARPA dividing line in ChartMogul's data is ~$25/mo — a "B2B" idea priced below that inherits consumer-grade churn. If estimated WTP is more than 2× above the category range, it's likely too optimistic; if below the category minimum, question whether this is a business purchase at all.

## Entry-Model Conversion Benchmarks (fills `freemium_conversion_estimate`)

Median free-to-paid across all B2B products: **8%** (ChartMogul × ProductLed, 200 products, Jan 2026). By entry model:

| Entry model | Good | Great |
|---|---|---|
| Freemium (gated signup) | 3–5% | 8–12% |
| Free trial, no credit card | 4–6% | 10–15% |
| Free trial, card required | 25–35% | 50–60% |
| Reverse trial | 4–6% | 8–12% |

The distribution is bimodal: 20% of trial products convert below 2.5% and 23% above 25% — activation quality, not the model alone, decides which side an idea lands on. Estimate from the "Good" column; move toward "Great" only with strong value gating and a fast time-to-value. For pure self-serve with zero human touch, ChartMogul's GTM report measured trial→paid as low as ~2.5% — use that as the pessimistic bound when activation is complex.

## Plan Structure

- Offer monthly + annual; anchor on annual at **2 months free (≈ 17% off)** — the B2B norm. Discounts beyond ~30% signal desperation to business buyers rather than value.
- Price tiers on a value metric the buyer already tracks (orders, clients, seats, locations) — never on arbitrary feature splits the reviews will call "feature ransom".
- Keep the entry price under the solo operator's no-approval threshold (~$50/mo) when `budget_authority` is the weak driver.

## Secondary Revenue Path (self-serve → higher tiers)

Fills the schema's `b2b2c_potential` field — here it means **up-market expansion potential**:

| Signal the path exists | Example |
|---|---|
| Larger teams ask for roles/permissions, SSO, audit logs | The "Enterprise tier" checklist |
| Agencies/consultants want to run it for many clients | Partner/multi-account tier at 3–5× |
| Buyers ask for onboarding or done-for-you setup | Productized service add-on |

If the path exists: note it as future expansion at 3–5× the core price. **Do NOT recommend the sales-led tier as the primary model** — demos, procurement, and security questionnaires are the sales-led drift this pack's target explicitly excludes. Launch self-serve first; expansion waits until the core proves retention.

## Notes

- Lifetime deals are a launch tactic only (cash + first reviews); price at 3–5× annual and cap the cohort — LTD buyers never convert to subscribers.
- If `monetization_evidence` from market_insights is empty across all platform files, flag pricing as "unvalidated" — B2B ideas with no one paying for adjacent solutions usually mean the pain is real but the budget isn't.

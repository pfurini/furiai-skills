# Pricing — B2B calibration (Italy-first, self-serve micro-SaaS)

Loaded by `iv-pricing-wtp` via the CALIBRATION path in its dispatch prompt.
Defines the pricing-model menu, premium multipliers, and benchmark tables
for the Italian B2B target. The Van Westendorp mechanism and process live in
the agent brief. All prices EUR **ex-VAT** unless stated (Italian B2B prices
are quoted "+ IVA"; consumer-style VAT-inclusive display reads B2C).

> Sources: category price bands are from vendor pricing pages observed
> 2026-08 (`research/idea-validation-italy-b2b/price-anchors-incumbents.md`)
> — `confidence: high` for the invoicing/gestionale bands (published list
> prices), `medium` for legal/booking/CRM, `medium` (quote-only derived) for
> studio software. Entry-model conversion tables are global (ChartMogul ×
> ProductLed Jan 2026; MicroConf 2024) — no Italian cut exists; say so when
> using them. Driver premium multipliers remain provisional constructs
> (`confidence: low`).

## The €50/month line (governs model choice and the guardrail)

Across the Italian pricing research, self-serve purchasing visibly thins out
above roughly **€50/mo ex-VAT entry price**: above it the buyer starts
expecting a demo, a contract, often a dealer. It is also the practical
no-approval threshold for titolari and studi. Consequences:
- entry plan ≤ €50/mo → self-serve band;
- entry ≤ €50/mo but bought through intermediaries → assisted self-serve
  band (flag it; intermediary = distribution channel);
- entry > €50/mo → sales-motion check; the idea is drifting out of scope.

## Pricing Models

| Model | Best for | Risk | Italian indie sweet spot |
|---|---|---|---|
| **Flat monthly tier(s)** | Single-operator tools, clear job, predictable usage | Leaves seat-expansion uncollected | €9–49/mo, 2–3 tiers, billed per azienda |
| **Per-seat subscription** | Team/studio tools where value scales with people | Seat scrutiny at renewal; per-seat resentment | €8–25/seat/mo (legal-PM class runs €49–99/lawyer at the top) |
| **Usage-based / credits** | Value scales with volume (documents, orders, invii) | Bill-shock complaints | Base fee + usage; Zucchetti-style prepaid packs are a familiar Italian pattern |
| **Freemium → paid tier** | Marketplace apps needing review velocity; natural power-user wall | Median freemium→paid only 3–5% (global data); free users cost support | Free tier + €9–49/mo paid |
| **Free trial (no card) → paid** | Products needing days to show value | Global median trial→paid 4–6% of signups; ~2× the LTV of card-required (MicroConf 2024) | 14-day trial, then €9–49/mo |
| **Free trial (card required) → paid** | Obvious, fast-provable ROI | Fewer trials started; hostile for cold Italian audiences (card diffidence is real) | Same prices; 25–35% trial→paid typical globally |
| **One-time / lifetime licence** | Utilities; niches with strong canone resistance | No recurring revenue | €49–199 one-time; consider "one-time + paid updates" hybrid where subscription resistance shows in evidence |
| **Annual prepay discount** | Every model above, as the anchor plan | Deep discounts train buyers to wait | 2 months free (≈17%); Italians accept annual-with-fattura readily |
| **Lifetime deal (AppSumo-style)** | Launch cash + first users only | Destroys LTV; LTD buyers never expand | Never the primary model |

### Model selection criteria

| If the product... | Recommended model |
|---|---|
| Is used by one operator with a recurring job | Flat monthly tiers |
| Serves a studio managing many client firms | Flat per-studio tier scaled by aziende gestite (the billing unit Italian studio software already uses) — not per-seat |
| Gets more valuable as teammates join | Per-seat (with a flat small-team tier to blunt seat resentment) |
| Scales with transaction/usage volume | Usage-based with a base fee (prepaid packs read familiar in Italy) |
| Lives in a marketplace where reviews gate ranking (FIC App Store, Shopify) | Freemium or generous trial |
| Proves ROI within one session | Card-required trial — but weigh Italian card diffidence; no-card + fast activation often nets more |
| Needs days of embedded usage before value shows | No-card 14-day trial |
| Competes with the incumbent suite's included module | Free tier covering parity + paid tier for the differentiator — the enemy is "già incluso" |
| Evidence shows strong canone resistance in the niche | One-time licence or annual-only with invoice; test before defaulting to monthly |

## Driver-Premium Multipliers

Keyed to `primary_driver` from `desire_scores.json` (B2B driver set — names
must match the demand-drivers pack). Provisional (`confidence: low`):

| Primary demand driver | Premium multiplier | Rationale |
|---|---|---|
| **ROI provability** | 1.5–2.0× | A tool that shows recovered revenue or counted hours prices against the value, not against competitors. |
| **Pain severity** | 1.3–1.8× | High-stakes pain (sanzioni, compliance exposure, lost clients) tolerates premium pricing. |
| **Pain frequency** | 1.2–1.5× | Daily pain justifies a subscription but each occurrence is small. |
| **Budget authority** | 1.0–1.3× | Easy purchase ≠ higher price; the ~€50/mo no-approval threshold caps it. |
| **Urgency** | 0.9–1.2× | Scadenza-driven buyers pay list price fast but churn after the deadline. |

Apply to the competitive modal price: `driver_adjusted_target =
competitive_modal_price × driver_multiplier`. If `desire_strength_label` =
"weak", apply no multiplier. Secondary-driver bonus: +10% if the secondary
driver differs from the primary and scores ≥ 3.

## WTP Benchmarks by Category (EUR ex-VAT, Italian market)

| Category | Monthly WTP band | Evidence |
|---|---|---|
| Micro-firm invoicing/gestionale class | **€12–25/mo mode**; forfettario floor €2.50–4/mo; multi-user/warehouse €35–60/mo | Vendor list prices (Fatture in Cloud, Danea, Aruba…), 2026-08 (`confidence: high`) |
| SMB team tools (agencies, small ops) | €29–99/mo flat or €10–25/seat | Italian + international tools sold into Italy (`confidence: medium`) |
| Studio-side professional tools (commercialisti) | The suite line runs €100–250/mo per small studio — but dealer-mediated, annual contracts. An indie add-on prices into **discretionary spend beside the suite: €19–79/mo per studio** | Derived from quote-only research (`confidence: medium`) |
| Legal practice tools | €49–99/lawyer/mo (suite class); indie add-ons €19–49/lawyer or flat per studio | (`confidence: medium`) |
| Booking/appointment, vertical ops | €50–80/mo small team | (`confidence: medium`) |
| Marketplace apps (global platforms) | $10–100/mo; Shopify store-wide average $66.54/mo | Global scrape Jan 2025 (`confidence: high` for e-commerce, global market) |
| Dev tools / API products | €19–99/mo + usage | Provisional (`confidence: low`) |

Sanity rules: ChartMogul's B2B/B2C ARPA dividing line is ~$25/mo — an idea
priced below ~€25/mo inherits consumer-grade churn (retention risk, not a
growth hack). If estimated WTP is >2× above the category band, it's likely
too optimistic; if below the band's floor, question whether this is a
business purchase at all. If it lands above €50/mo entry, re-run the
sales-motion check.

## Entry-Model Conversion Benchmarks (fills `freemium_conversion_estimate`)

Global data — no Italian cut exists; note that in the rationale. Median
free-to-paid across B2B products: **8%** (ChartMogul × ProductLed, n=200,
Jan 2026). By entry model:

| Entry model | Good | Great |
|---|---|---|
| Freemium (gated signup) | 3–5% | 8–12% |
| Free trial, no credit card | 4–6% | 10–15% |
| Free trial, card required | 25–35% | 50–60% |
| Reverse trial | 4–6% | 8–12% |

The distribution is bimodal (activation quality decides the side). Estimate
from "Good"; move toward "Great" only with strong value gating and fast
time-to-value; use ~2.5% as the pessimistic bound for complex activation.
LTV nuance (MicroConf 2024, directional): no-card trials converted worse
but produced ~2× the LTV of card-required — don't pick card-required on
conversion rate alone. For Italy, lean no-card when the audience is cold.

## Plan Structure

- Offer monthly + annual; anchor on annual at **2 months free (≈17%)**.
  Annual-with-fattura is the native Italian B2B billing rhythm; support SDD/
  bank transfer for annual plans, not just card.
- Display prices **ex-VAT ("+ IVA")** and issue fattura elettronica —
  VAT-inclusive pricing reads consumer-grade to an Italian business buyer.
- Price tiers on a value metric the buyer already tracks (documenti,
  aziende gestite, pratiche, ordini, seats) — never arbitrary feature
  splits ("feature ransom" complaints recur in reviews).
- Keep the entry price under €50/mo ex-VAT (the no-approval threshold)
  whenever `budget_authority` is a weak driver.

## Secondary Revenue Path (self-serve → expansion)

Fills the schema's `b2b2c_potential` field — here it means **expansion
potential beyond the self-serve core**:

| Signal the path exists | Example |
|---|---|
| Studi/agencies want to run it for many client firms | Partner/multi-account tier at 3–5× (the commercialista as power buyer) |
| Larger teams ask for roles, audit logs, SSO | The up-market checklist — note it, don't build for it |
| Buyers ask for onboarding or done-for-you setup | Productized onboarding add-on — in Italy this is often what "assisted self-serve" monetizes |

If the path exists: note it as future expansion at 3–5× the core price.
**Do NOT recommend the sales-led tier as the primary model** — demos,
procurement, and dealer contracts are exactly the motion this target
excludes. Launch self-serve first; expansion waits until the core proves
retention.

## Notes

- Lifetime deals are a launch tactic only (cash + first reviews); price at
  3–5× annual and cap the cohort.
- If `monetization_evidence` from market_insights is empty across all
  platform files, flag pricing as "unvalidated" — with one Italian nuance:
  absence of PUBLIC monetization evidence is weaker disproof here than in
  Anglophone markets (spend is real but happens through dealers and
  invoices, not visible app-store receipts). Say which interpretation the
  evidence supports.
- If market_insights files are past `stale_after`, note that competitive
  pricing may have shifted and recommend refreshing trend research.

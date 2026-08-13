# Pricing — B2C calibration

Loaded by `iv-pricing-wtp` via the CALIBRATION path in its dispatch prompt.
Defines the pricing-model menu, premium multipliers, and benchmark tables
for the B2C target. The Van Westendorp mechanism and process live in the
agent brief.

## Contents

- Pricing models and selection criteria
- Demand-driver premium multipliers
- WTP benchmarks by app category
- Freemium conversion estimation
- Annual vs. monthly strategy
- Secondary revenue path (B2B2C)

## Pricing Models

| Model | Best for | Risk | Indie sweet spot |
|---|---|---|---|
| **Freemium → subscription** | Habit-forming apps with daily use, feature-gated value | Conversion friction; most users stay free forever | $3–$8/mo or $20–$50/yr |
| **Subscription only (paywall)** | High-value, immediately obvious ROI, professional tools | High churn risk; must prove value fast | $5–$15/mo |
| **One-time purchase** | Utilities, tools with clear one-time value, privacy-focused apps | No recurring revenue; must rely on new users | $3–$10 |
| **Consumables / credits** | Variable usage (AI generations, exports, premium content) | Unpredictable revenue; usage may decline | $1–$5 per credit pack |
| **Freemium + consumables** | Apps where core is free but power usage costs (AI, storage) | Complex to balance free vs. paid tiers | Free tier + $2–$10 packs |
| **Lifetime deal** | Launch phase only — use for early adopter cash and reviews | Destroys LTV; never use as primary model | $20–$60 (3–5× annual price) |
| **Tip jar / patronage** | Content-focused, community-driven, or open-source-adjacent | Very low conversion; unreliable revenue | $1–$5 tips, rare |

### Model selection criteria

| If the app... | Recommended model |
|---|---|
| Has daily usage with progressively unlocked value | Freemium → subscription |
| Delivers immediate, obvious ROI in one session | Subscription only or one-time purchase |
| Produces output that varies in volume (AI, exports) | Freemium + consumables |
| Is a simple utility used occasionally | One-time purchase |
| Requires trust before users see value (health, finance) | Extended free trial → subscription |
| Competes with free alternatives that are "good enough" | Freemium (generous free tier) → subscription for power features |

## Demand-Driver Premium Multipliers

Driver strength from `desire_scores.json` directly affects pricing power. Apps that tap into primal desires command premium pricing; apps that solve mild inconveniences face price resistance.

| Primary desire driver | Premium multiplier | Rationale |
|---|---|---|
| **Survival** (health, safety, financial security) | 1.3–1.8× | Users pay more when stakes are high. Health and money apps can charge premium. |
| **Status** (achievement, appearance, signaling) | 1.5–2.0× | Status is inherently scarce — users pay for differentiation. Luxury/prestige positioning works. |
| **Belonging** (community, connection) | 1.0–1.3× | Users value belonging but expect community features to be free (social norms). Premium only for exclusive communities. |
| **Control** (mastery, organization, reducing chaos) | 1.2–1.5× | Moderate premium. Users pay for control when the alternative is stressful. |
| **Curiosity** (learning, discovery, novelty) | 0.8–1.2× | Lowest premium. Curiosity-driven apps compete with free content (YouTube, blogs). Must add structure/accountability to charge. |

If `desire_strength_label` = "weak", do not apply any multiplier — the app lacks the emotional pull to justify premium pricing.

### Secondary driver bonus

If the secondary driver is different from the primary and scores ≥ 3, add a +10% bonus. Apps that tap two distinct desires (e.g., survival + control in a health tracker) have stronger pricing power than single-desire apps.

## WTP Benchmarks by App Category

Use these ranges as a sanity check against the Van Westendorp and driver-adjusted estimates:

| App category | Subscription WTP range (monthly) | One-time WTP range | Annual discount sweet spot |
|---|---|---|---|
| **Health & fitness** | $5–$15/mo | $8–$30 | 40–50% off monthly |
| **Nutrition / diet** | $5–$12/mo | $8–$25 | 40–50% off monthly |
| **Meditation / mental health** | $5–$15/mo | $10–$30 | 50–60% off monthly |
| **Finance / budgeting** | $3–$10/mo | $5–$20 | 30–40% off monthly |
| **Productivity / task management** | $3–$8/mo | $5–$15 | 30–40% off monthly |
| **Habit tracking** | $2–$6/mo | $3–$10 | 40–50% off monthly |
| **Creative tools (photo/video)** | $3–$10/mo | $5–$20 | 30–40% off monthly |
| **Education / learning** | $5–$15/mo | $10–$30 | 50–60% off monthly |
| **Dating / social** | $5–$25/mo | N/A (subscription dominates) | 30–40% off monthly |
| **Parenting / family** | $3–$8/mo | $5–$15 | 40–50% off monthly |
| **Utility / scanner / converter** | $1–$4/mo | $2–$8 | 50–60% off monthly |
| **AI-powered tools** | $5–$20/mo | $10–$40 consumable pack | 30–40% off monthly |

If the estimated WTP is more than 2× above the category range, it's likely too optimistic. If it's below the category minimum, the app may struggle to sustain development.

## Freemium Conversion Estimation

If the recommended model includes a free tier, estimate what percentage of free users will convert to paid:

| Factor | Higher conversion (toward 8–12%) | Lower conversion (toward 1–3%) |
|---|---|---|
| **Value gating** | Core value is free; premium unlocks power features or removes limits | Core value IS the paid feature — free tier feels empty |
| **Free tier generosity** | Generous enough that users form habits before hitting the wall | Either too generous (no reason to pay) or too stingy (users leave) |
| **Pain of free** | Free tier has clear, felt limitations (ads, watermarks, usage caps) | Free tier works fine for most users |
| **Social proof** | Users see premium features in action (shared content with branding) | No visibility into what premium offers |
| **Trial exposure** | Time-limited trial of premium (7–14 days) shows value upfront | No trial; users must imagine premium value |

**Category benchmarks for freemium conversion:**

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

Most indie apps benefit from offering both monthly and annual plans. The annual plan serves as the anchor.

| Discount depth | Effect |
|---|---|
| **20–30% off monthly** | Subtle incentive. Users who prefer monthly will stay monthly. Low commitment-capture rate. |
| **40–50% off monthly** | Sweet spot for most B2C apps. Enough savings to feel meaningful, not so deep it signals desperation. |
| **50–60% off monthly** | Aggressive — use for high-churn categories where locking in annual users dramatically improves LTV. |
| **> 60% off monthly** | Signals the app isn't worth the monthly price. Avoid unless in launch/promotional phase. |

**Recommended annual price** = monthly price × 12 × (1 - discount). Present the annual plan as the default/highlighted option.

## Secondary Revenue Path (B2C vs. B2B2C)

Some ideas have a viable path to both consumer and business revenue. Evaluate if the app concept could serve both — this fills the schema's `b2b2c_potential` field:

| Signal that B2B2C path exists | Example |
|---|---|
| Users would expense the app to their employer | Productivity tools, professional development |
| A business version could serve teams | Shared dashboards, admin controls, team analytics |
| Content or data from the app has business value | Health data for employers, fitness for corporate wellness |
| The consumer app is a wedge into workplace adoption | Personal Slack → company Slack, personal Notion → team Notion |

If B2B2C path exists:
- **B2C price**: Use the standard WTP methodology (this is the consumer price).
- **B2B2C price**: 3–5× the consumer price per seat. Businesses have larger budgets and lower price sensitivity.
- **Recommendation**: Launch B2C first (faster validation, faster feedback). Flag B2B2C as a future monetization expansion in the output.
- **Do NOT recommend B2B2C as the primary model** for an indie developer — enterprise sales cycles and support needs don't fit the indie model.

## Notes

- Lifetime deal pricing should only appear as a launch tactic, never as the recommended primary model. LTD price = 3–5× annual price. Cap at $60 for consumer apps.
- For apps competing with strong free alternatives (Google Keep, Apple Notes, default apps), the effective WTP ceiling may be $0 for most users. In this case, the pricing model must create value that the free alternative structurally cannot (social features, AI, specialized workflows).

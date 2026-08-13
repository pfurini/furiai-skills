# Distribution — B2C calibration (Italy-first rings)

Loaded by `iv-distribution` via the CALIBRATION path in its dispatch prompt.
Defines the loop taxonomy, platform-channel rubrics, budget tiers, and
verdict logic for the B2C target. The k = i × c mechanism and the process
live in the agent brief.

> Sources for the k-factor rows: Rahul Vohra (0.15–0.25 good, 0.4 great,
> ~0.7 outstanding for consumer products), Andrew Chen (most measured viral
> factors sit at 0.2–0.3 or below; k ≥ 1 windows are short-lived, 2025),
> Adjust (only ~30% of apps have a measurable k at all; median 0.45 among
> those), Extole (measured k ≈ 0.05 across 400 referral programs). Rows
> without a source are marked construct.

## Contents

- Growth loop types
- Platform advantage rubric (ASO) — fills `platform_advantage` in the schema
- Advocacy channel rubric (creator economy) — fills `creator_economy_fit`
- Paid budget tiers
- Verdict logic and tier adjustment

## Growth Loop Types

| Loop type | Description | Typical k-factor | Example |
|---|---|---|---|
| Inherent | Product is useless alone, requires inviting others | 0.4–0.7 sustained (bursts above 1 happen but are short-lived — never model sustained k ≥ 1) | Multiplayer games, shared lists |
| Collaborative | Better with others but works solo | 0.2–0.6 | Workout trackers with friends, shared budgets |
| Word-of-mouth | Users talk about it because it's remarkable | 0.1–0.4 | Apps that produce "wow" output (AI art, unique insights) |
| Incentivized | Users get a reward for referring | 0.05–0.15 (the only measured referral-program k is ≈ 0.05 — Extole) | Referral credits, unlocked features |
| Content-as-distribution | App output is inherently shareable on social platforms | 0.3–0.8 (construct — no published measurement for this loop type) | Photo editors with watermarks, personality quizzes, wrapped/recap screens |
| None | No natural reason to share | 0.0–0.05 (~70% of apps have no measurable k — Adjust) | Utility apps (calculators, timers) |

## Platform Advantage Rubric — ASO

ASO's premise is well sourced: search drives the majority of App Store
downloads (~59–65%, Apple Ads / Sensor Tower via 2026 roundups). Keyword
opportunity is scarce — only ~6.8% of App Store keywords are both winnable
(difficulty < 40) and carry real traffic (Applyra 460K-keyword scan,
2026-07). The rubric's internal thresholds are constructs.

**Score ASO per ring — the rings differ structurally (2026-08, verified):**
the IT App Store is a distinct storefront with its own charts and Italian
category names, and its **paid chart is dominated by small Italy-specific
utilities** — a domestic niche app can realistically chart there. Italian
keywords and Italian-language listings are less contested than English
ones, so a genuinely Italian-language-first app often scores one tier
higher on Ring 1 than the same app would score on Ring 3. Say which ring
each score describes.

| Factor | High (3 pts) | Medium (2 pts) | Low (1 pt) |
|---|---|---|---|
| **Category competition** | Niche category, top 10 achievable with <500 ratings | Moderate category, top 50 achievable | Saturated category, dominated by incumbents with 100K+ ratings |
| **Keyword opportunity** | High-volume keywords with low-rated top results (< 4.2 stars, < 1K ratings) | Keywords exist but top results are solid (4.5+ stars) | All relevant keywords dominated by well-known brands |
| **Search intent match** | Users actively search for this exact solution (tool/utility intent) | Users search for the category but not this specific angle | Discovery-dependent — users don't know they want this |
| **Review velocity potential** | App has natural prompt moments for asking reviews (completed task, achievement) | Some prompt moments but not in core loop | No natural review prompt; must interrupt to ask |
| **Visual differentiation** | App icon and screenshots can stand out (unique aesthetic, bold output previews) | Decent but similar to competitors | Looks like every other app in the category |

**ASO score**: Sum of all factors (5–15 points).

| Total | ASO opportunity |
|---|---|
| 12–15 | **high** — ASO should be primary acquisition channel |
| 8–11 | **medium** — ASO is viable but won't be the sole driver |
| 5–7 | **low** — ASO alone won't generate meaningful installs |

### Featured potential checklist

An app has App Store featured potential if it meets **3+ of these 5
criteria** (construct — reflects practitioner readings of Apple editorial
practice; Apple publishes no criteria and no Italy-specific pitch route):

1. Uses a newly released Apple/Google platform feature (widgets, Live Activities, visionOS, AI APIs)
2. Has exceptional design quality (would look good in an editorial story)
3. Serves an underrepresented audience or emerging cultural moment
4. Has a clear positive-impact or wellness angle
5. Is a premium/indie app (Apple editorially favors paid apps and small teams)

## Advocacy Channel Rubric — Creator Economy Fit

Evaluate whether creators can authentically promote the app. Not all apps
are "creator-friendly" — forcing influencer marketing on a utility app
wastes money.

**Ring-1 reality check (2026, sourced):** the Italian creator market is
real and measured (€425M, ~40K professionals, 74% nano/micro) but measured
for consumer-goods brands — **no Italian app-install creator data exists**
(no CPI norms, no rate card, no case studies), so any Ring-1 creator plan
is a bespoke negotiation with no public comparable. The economic optimum is
nano/micro on TikTok/Instagram (nano floor €100–300 per IG post; engagement
falls monotonically with tier size; January is the cheapest month).
Gifting/barter is documented practice for physical goods only — a free app
subscription as consideration is unmeasured. Two hard constraints:
Amazon.it's affiliate program pays **0% on apps**, and ad-disclosure
liability falls on the **commissioning advertiser** (AGCM fines under the
Codice del Consumo; require the IAP Digital Chart labels — "pubblicità",
"link affiliato + brand" — by contract, since measured disclosure
compliance on TikTok is under 1%). Strongest Italian creator verticals:
beauty/fashion, food, sport/fitness; finance creators carry Consob/ESMA
exposure — treat finance-adjacent creator promotion as the highest-risk
configuration.

| Factor | Score: High | Score: Medium | Score: Low |
|---|---|---|---|
| **Content generation** | App produces visual or shareable output that IS the content (before/after, results, transformations) | App experience is interesting to narrate/demonstrate | App is invisible — nothing to show on camera |
| **Audience alignment** | Clear niche creator communities already talk about this problem space | Adjacent creator communities exist | No creator community maps to this product |
| **Demo-ability** | Can be demonstrated in a 30–60 second clip with visible value | Needs 2–3 minute explanation to convey value | Requires hands-on usage over days to appreciate |
| **Authenticity** | Creator would genuinely use the app (not just shill for money) | Creator could plausibly use it occasionally | Feels forced — creator has no real use case |
| **Affiliate/monetization fit** | App has a price point that supports affiliate commissions (€5+/$5+ per month or €20+/$20+ one-time); Ring 1 needs a bespoke deal — no Italian app-affiliate norms exist and Amazon.it pays 0% on apps | Freemium with conversion — harder to attribute | Free app with no monetization — no creator incentive |

**Scoring**: Count High/Medium/Low across all 5 factors.
- **high fit**: 3+ factors scored High
- **medium fit**: 2 factors High, or 3+ Medium
- **low fit**: 2+ factors Low, or no factors High

## Paid Budget Tiers

Budget tiers use the same vocabulary as the CAC specialist:

| Budget tier | Monthly ad spend | Viable paid strategies |
|---|---|---|
| **Bootstrap** (≤ €100/mo) | Testing only | One platform, 2–3 ad creatives, learn CPM/CPI before scaling. Not a primary channel. |
| **Lean** (€100–500/mo) | Targeted campaigns | One platform with lookalike audiences. Can work if CPI < €2 and LTV > €6 — a bar below every published Western paid-social CPI range, but **Italy's Apple Search Ads sits under it** (CPA $1.60, 2025, the one measured channel where Lean paid can work for Ring 1). |
| **Moderate** (€500–2,000/mo) | Real optimization | Multi-creative testing, retargeting. Viable if LTV:CAC > 3:1 on at least one platform (the 3:1 rule is SaaS folklore, not a consumer-app measurement — treat as a construct threshold). |

If `budget_constraint` from user profile is "low", cap paid feasibility at
"marginal" regardless of other factors — the user cannot sustain the
learning curve of paid acquisition.

## Verdict Logic

### Raw verdict (first match wins)

Thresholds anchored to the practitioner consensus (Chen: ≥ 0.5 is where a
viral loop becomes perceptible; Vohra: 0.15–0.25 is good):

| Condition | Raw verdict |
|---|---|
| k-factor ≥ 0.5 OR (ASO = high AND creator_fit = high) OR founder has existing audience | **strong** |
| k-factor ≥ 0.2 AND at least one other dimension scores medium+, OR any single dimension scores high | **moderate** |
| Otherwise (no organic path, paid not viable at budget) | **weak** |

### Tier adjustment

The same distribution profile means different things to different founders:

| Founder tier | Adjustment |
|---|---|
| **beginner** | Downgrade verdict by one level if the only viable channels require technical skill (SEO, paid optimization, ASO keyword research). Beginners need channels with fast feedback loops: TikTok organic, community posting, referral-based growth. Flag complex channels as "aspirational — learn first." |
| **builder** | No adjustment. Builders can execute most channels with some learning curve. Flag paid channels > €500/mo as risky given typical builder budgets. |
| **growth** | Upgrade verdict by one level if paid channels are viable and the founder has optimization experience. Growth-tier founders can unlock channels that are traps for beginners. |

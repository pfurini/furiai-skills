# Distribution — B2B calibration (self-serve / PLG micro-SaaS)

Loaded by `iv-distribution` via the CALIBRATION path in its dispatch prompt.
Defines the loop taxonomy, platform-channel rubrics, budget tiers, and
verdict logic for the B2B target. The k = i × c mechanism and the process
live in the agent brief.

> Confidence: loop-type k-factor ranges are provisional (`confidence: low`)
> pending the source-hardening pass; rubric structures are stable.

## Growth Loop Types

B2B self-serve tools spread through work artifacts and teams, not social feeds:

| Loop type | Description | Typical k-factor (provisional) | Example |
|---|---|---|---|
| Team expansion | Useful solo, better with the team invited — seats accumulate inside one customer | 0.3–0.8 (within-account) | Shared boards, team inboxes |
| Client-facing artifact | Output is delivered to the customer's clients with the tool visible (branding, portals, badges) | 0.2–0.6 | White-label-lite reports, client portals, invoice footers |
| Integration network | Being listed in an ecosystem's directory routes its users to you | 0.1–0.4 | Zapier/Slack/Shopify integrations surfacing the tool |
| Peer referral | Operators recommend tools in their communities and mastermind groups | 0.1–0.3 | "What do you use for X" thread answers |
| Incentivized / affiliate | Referral commissions to users or content affiliates | 0.1–0.3 | 20–30% recurring affiliate programs |
| None | Solitary back-office usage nobody sees | 0.0–0.05 | Internal cleanup/automation utilities |

Map these onto the schema's `viral_loop_type` enum as: team expansion → `collaborative`; client-facing artifact → `content-as-distribution`; integration network → `inherent`; peer referral → `word-of-mouth`; incentivized/affiliate → `incentivized`; none → `none`. Note the B2B loop name in `viral_loop_description`.

## Platform Advantage Rubric — Marketplace Listing Opportunity

For self-serve B2B, the marketplace/directory listing (Shopify App Store, Slack, Atlassian, Chrome, Zapier, G2 category page) plays the role ASO plays for consumer apps. Score on a 3-tier rubric; fill the schema's `platform_advantage` block (the `aso_*` field names carry these marketplace scores — note that in the rationale):

| Factor | High (3 pts) | Medium (2 pts) | Low (1 pt) |
|---|---|---|---|
| **Category competition** | Niche marketplace category, top 10 achievable with < 50 reviews | Moderate category, top 50 achievable | Saturated category dominated by listings with 1,000+ reviews |
| **Keyword opportunity** | High-traffic marketplace/G2 keywords with weak top results (low ratings, stale listings) | Keywords exist but top results are solid | All relevant keywords owned by established vendors |
| **Search intent match** | Buyers search the marketplace for this exact job ("sync inventory", "client reports") | Buyers search the category but not this angle | Discovery-dependent — buyers don't know to search for it |
| **Review velocity potential** | Natural review-ask moments (successful sync, report delivered, ROI shown) and vendors' review programs work in this category | Some ask moments, not in core loop | No natural moment; reviews accrue very slowly |
| **Listing differentiation** | Screenshots/description can show a visibly different approach or outcome | Decent but similar to competitors | Looks like every other listing in the category |

**Score bands** (sum 5–15): 12–15 → **high** (the marketplace should be the primary acquisition channel) · 8–11 → **medium** (viable, not sole driver) · 5–7 → **low** (listing alone won't generate meaningful installs).

### Featured/visibility checklist

A listing has featuring potential if it meets **3+ of these 5**:

1. Uses a newly released platform capability (new API, new extension surface, platform AI features)
2. Fills a gap the platform itself highlights to developers (partner blog "app opportunities" posts)
3. Exceptional listing quality (demo video, polished screenshots, complete localization)
4. Strong early review velocity and rating (platforms feature what already converts)
5. Vertical relevance to a platform push (e.g. platform courting a merchant segment your tool serves)

## Advocacy Channel Rubric — Founder Content & Community Fit

For indie B2B, the creator-economy role is played by founder-led content and practitioner communities. Score the 5 factors and fill `creator_economy_fit` and its breakdown (field names carry these scores; note it in the rationale):

| Factor (schema key) | Score: High | Score: Medium | Score: Low |
|---|---|---|---|
| **Content generation** (`content_generation`) | The problem/solution makes compelling teach-in-public content (before/after metrics, teardowns, templates) | The workflow can be explained interestingly | Nothing demonstrable — invisible back-office plumbing |
| **Audience alignment** (`audience_alignment`) | Active practitioner communities and niche newsletters exist where buyers concentrate | Adjacent communities exist | Buyers are diffuse, no gathering places |
| **Demo-ability** (`demo_ability`) | Value visible in a 60-second demo or a screenshot with numbers | Needs a few minutes of context | Requires living with it for weeks |
| **Authenticity** (`authenticity`) | Founder plausibly IS the target operator or has worked the niche | Founder is adjacent to the niche | Founder is an outsider posting marketing into practitioner spaces |
| **Affiliate/monetization fit** (`affiliate_fit`) | Price supports recurring affiliate commissions ($20+/mo) and niche newsletters/creators take sponsorships | Mid-price, some sponsorship surface | Too cheap to fund advocacy; no niche media exists |

**Scoring**: high fit = 3+ High · medium fit = 2 High or 3+ Medium · low fit = 2+ Low or no High.

## Paid Budget Tiers

Budget tiers use the same vocabulary as the CAC specialist:

| Budget tier | Monthly ad spend | Viable paid strategies |
|---|---|---|
| **Bootstrap** (≤ $100/mo) | Testing only | High-intent niche search keywords only, exact match, tiny geo. Not a primary channel. |
| **Lean** ($100–$500/mo) | Narrow campaigns | Google Ads on long-tail solution keywords; retargeting site visitors. LinkedIn ads are NOT viable at this tier (minimum CPCs consume the budget). |
| **Moderate** ($500–$2,000/mo) | Real optimization | Search + retargeting with A/B tested landing pages; small sponsorships of niche newsletters. LinkedIn only for ACV > $1,000/yr. |

If `budget_constraint` from user profile is "low", cap paid feasibility at "marginal" regardless of other factors — the buyer-side CPCs in B2B consume small budgets before the learning curve completes.

## Verdict Logic

### Raw verdict (first match wins)

| Condition | Raw verdict |
|---|---|
| k-factor ≥ 0.4 (team-expansion or client-artifact loop) OR (marketplace opportunity = high AND advocacy fit = high) OR founder has an existing audience or distribution partner in the niche | **strong** |
| k-factor ≥ 0.15 AND at least one other dimension scores medium+, OR any single dimension scores high | **moderate** |
| Otherwise (no organic path, paid not viable at budget) | **weak** |

### Tier adjustment

| Founder tier | Adjustment |
|---|---|
| **beginner** | Downgrade verdict by one level if the only viable channels require skills they lack (SEO, cold outbound, paid optimization). Beginners need channels with fast feedback: community participation, marketplace listing, founder content in niches they authentically belong to. Flag cold outbound as "aspirational — needs practice" for beginners. |
| **builder** | No adjustment. Flag paid channels > $500/mo as risky given typical builder budgets. |
| **growth** | Upgrade verdict by one level if paid channels are viable and the founder has run acquisition before. Growth-tier founders can also unlock partnership/integration deals that require credibility. |

# Distribution — B2B calibration (Italy-first, self-serve micro-SaaS)

Loaded by `iv-distribution` via the CALIBRATION path in its dispatch prompt.
Defines the loop taxonomy, platform-channel rubrics, budget tiers, and
verdict logic for the Italian B2B target. The k = i × c mechanism and the
process live in the agent brief.

> Confidence: loop-type k-factor ranges are provisional (`confidence: low`);
> rubric structures are stable. Italian channel facts (marketplace terms,
> legal exclusion, active communities) are from the 2026-08 research pack.
> Reminder from the CAC pack: **cold email/PEC is legally excluded in
> Italy** — never list it as an organic fallback here.

## Growth Loop Types

B2B self-serve tools spread through work artifacts and teams, not social
feeds:

| Loop type | Description | Typical k-factor (provisional) | Italian example |
|---|---|---|---|
| Team expansion | Useful solo, better with the team invited — seats accumulate inside one customer | 0.3–0.8 (within-account) | Shared boards, studio-wide pratiche |
| Client-facing artifact | Output is delivered to the customer's clients with the tool visible | 0.2–0.6 | Client portals, delivered reports, fattura/preventivo footers |
| Studio multiplier | A studio/agency adopts once and enrolls its client firms | 0.3–1.0 across accounts (the strongest Italian loop when it exists) | Commercialista rolling a document-collection tool out to 80 clients |
| Integration network | Being listed in an ecosystem's directory routes its users to you | 0.1–0.4 | Fatture in Cloud App Store, Zapier, connector ecosystems |
| Peer referral | Operators recommend tools in their communities | 0.1–0.3 | Fisco Forum threads, ordine local events, category associations |
| Incentivized / affiliate | Referral commissions to users or content affiliates | 0.1–0.3 | 20–30% recurring affiliate |
| None | Solitary back-office usage nobody sees | 0.0–0.05 | Internal cleanup utilities |

Map onto the schema's `viral_loop_type` enum as: team expansion →
`collaborative`; client-facing artifact → `content-as-distribution`; studio
multiplier → `collaborative` (note "studio multiplier" in
`viral_loop_description`); integration network → `inherent`; peer referral →
`word-of-mouth`; incentivized → `incentivized`; none → `none`.

The **studio multiplier** deserves explicit hunting: if the product can make
the commercialista/consulente/agency look good to their clients, one sale
becomes dozens of installs. Distinguish it from plain intermediary
*referral* (a channel, priced in the CAC pack): the loop version has the
intermediary operating the tool across clients, not just recommending it.

## Platform Advantage Rubric — Marketplace Listing Opportunity

For the Italian target the marketplace surface is thin: **Fatture in Cloud
App Store** (open, free publication, claimed 500K+ businesses / 16K
accountants) is the flagship; TeamSystem Commerce Apps Market, Shopify App
Store (Italian listings), Zapier and Chrome Web Store apply when the niche
touches them. Most Italian vertical niches have NO marketplace — score
low and let SEO/communities/intermediaries carry distribution; say so
explicitly rather than forcing marketplace fit.

Score on the 3-tier rubric; fill the schema's `platform_advantage` block
(the `aso_*` field names carry these marketplace scores — note that in the
rationale):

| Factor | High (3 pts) | Medium (2 pts) | Low (1 pt) |
|---|---|---|---|
| **Category competition** | Relevant marketplace exists and the category is thin (top 10 achievable with few reviews) | Moderate category | No relevant marketplace, or category saturated |
| **Keyword opportunity** | Marketplace/Capterra.it keywords with weak top results | Keywords exist but top results are solid | All relevant keywords owned by established vendors |
| **Search intent match** | Italian buyers search the surface for this exact job ("solleciti automatici", "sync magazzino") | Buyers search the category but not this angle | Discovery-dependent — buyers don't know to search |
| **Review velocity potential** | Natural review-ask moments in the core loop | Some ask moments, not in core loop | No natural moment; Italians under-review — expect slow accrual |
| **Listing differentiation** (schema key: `visual_differentiation`) | Listing can show a visibly different outcome, in Italian, compliance-aware | Decent but similar | Looks like every other listing |

**Score bands** (sum 5–15): 12–15 → **high** (marketplace as primary
acquisition) · 8–11 → **medium** (viable, not sole driver) · 5–7 → **low**.

### Featured/visibility checklist

A listing has featuring potential if it meets **3+ of these 5**:

1. Uses a newly released platform capability (new API surface, platform AI features)
2. Fills a gap the platform highlights to developers (partner-blog "app opportunities")
3. Exceptional listing quality — for Italy this includes **full Italian localization** (screenshots, description, support)
4. Strong early review velocity and rating
5. Vertical relevance to a platform push (e.g. FIC courting a merchant or accountant segment your tool serves)

## Advocacy Channel Rubric — Founder Content & Community Fit

For indie B2B in Italy, the creator-economy role is played by founder-led
content **in Italian** and the professional lattice (ordini, associations,
verified-active communities). Score the 5 factors and fill
`creator_economy_fit` and its breakdown:

| Factor (schema key) | Score: High | Score: Medium | Score: Low |
|---|---|---|---|
| **Content generation** (`content_generation`) | The problem makes compelling teach-in-public content in Italian (before/after metrics, normativa explainers, templates) | The workflow can be explained interestingly | Nothing demonstrable |
| **Audience alignment** (`audience_alignment`) | Verified-active Italian surfaces exist where buyers concentrate (Fisco Forum-class forums, association channels, active groups) | Adjacent communities exist | Buyers are diffuse or their discussion is private/offline |
| **Demo-ability** (`demo_ability`) | Value visible in a 60-second demo or a screenshot with numbers | Needs a few minutes of context | Requires living with it for weeks |
| **Authenticity** (`authenticity`) | Founder plausibly IS the target operator or is enrolled in the profession's albo / works the niche | Founder is adjacent | Founder is an outsider posting marketing into practitioner spaces |
| **Affiliate/monetization fit** (`affiliate_fit`) | Price supports recurring commissions (€20+/mo) and the vertical has sponsorable newsletters/portals (mostly quote-on-request in Italy — verify) | Mid-price, some sponsorship surface | Too cheap to fund advocacy; no niche media |

**Scoring**: high fit = 3+ High · medium fit = 2 High or 3+ Medium · low fit = 2+ Low or no High.

## Intermediary & Events Surface (Italy-specific, feeds channel notes)

Two Italian surfaces the schema has no dedicated block for — assess both and
write the outcome into the distribution rationale (the CAC pack prices
them as `intermediary_referral` and `events_fairs`):

- **Intermediary enablement**: can commercialisti/consulenti/resellers gain
  something (time, revenue, client goodwill) from recommending or operating
  the tool? Credibility holds only inside the studio's own workflow. If
  yes, name the enablement artifact (partner tier, co-branded portal,
  rev-share).
- **Events**: does the vertical have real fairs/CPD events (SMAU-class,
  ordine formation events)? Consent collected at events is the lawful seed
  for email follow-up — flag this as the compliant alternative wherever
  cold outreach would have been listed.

## Paid Budget Tiers

Budget tiers use the same vocabulary as the CAC specialist:

| Budget tier | Monthly ad spend | Viable paid strategies |
|---|---|---|
| **Bootstrap** (≤ €100/mo) | Testing only | High-intent Italian niche keywords, exact match. Not a primary channel. |
| **Lean** (€100–500/mo) | Narrow campaigns | Google Ads on Italian long-tail solution keywords; site retargeting (Meta, ~€0.43 CPC). LinkedIn NOT viable at this tier. |
| **Moderate** (€500–2,000/mo) | Real optimization | Search + retargeting with tested landing pages; a yearly fair as a discrete bet. |
| **Serious** (> €2,000/mo) | Multi-channel | LinkedIn becomes testable, but only with ACV > €1,000/yr; keep search + retargeting running underneath. |

If `budget_constraint` is "low", cap paid feasibility at "marginal"
regardless of other factors.

## Verdict Logic

### Raw verdict (first match wins)

| Condition | Raw verdict |
|---|---|
| k-factor ≥ 0.4 (team-expansion, client-artifact, or studio-multiplier loop) OR (marketplace opportunity = high AND advocacy fit = high) OR founder has an existing audience, albo standing, or intermediary network in the niche | **strong** |
| k-factor ≥ 0.15 AND at least one other dimension scores medium+, OR any single dimension scores high | **moderate** |
| Otherwise (no organic path, paid not viable at budget) | **weak** |

### Tier adjustment

| Founder tier | Adjustment |
|---|---|
| **beginner** | Downgrade one level if the only viable channels require skills they lack (SEO, paid optimization) or communities they don't belong to. Beginners need fast-feedback channels: marketplace listing, community participation where they authentically belong, intermediary enablement through existing relationships. |
| **builder** | No adjustment. Flag paid channels > €500/mo as risky. |
| **growth** | Upgrade one level if paid channels are viable and the founder has run acquisition before, or if they can unlock partnership/integration deals requiring credibility. |

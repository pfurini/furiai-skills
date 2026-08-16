# Italy B2C research — raw reports (Phase D-A of PLAN-italy-refactor.md)

Six web-research reports (2026-08-13, exa-backed, bilingual queries) behind the
Italy-first B2C refactor of `skills/idea-validation/references/calibration/b2c/`
and the b2c prompt templates. Same discipline as the sibling
`idea-validation-italy-b2b/` pass: every figure carries source + date +
confidence, and each report ends with a "does not exist publicly" log — data
absent from those logs must not be invented in the packs. Ring vocabulary:
Ring 1 = Italy, Ring 2 = Europe-English, Ring 3 = Western (NA, UK/IE, AU/NZ).

## Reports

- `device-platform-base.md` (DA1) — iOS/Android share Italy with trend and
  method caveats, smartphone penetration, App Store IT / Google Play IT
  storefront structure, app-economy spend (feeds market-sizing platform filter).
- `price-anchors-consumer.md` (DA2) — EUR price anchors per b2c category read
  live from the IT storefront, the subscription non-equalization finding, VAT
  and proceeds mechanics (feeds pricing).
- `paid-channel-units.md` (DA3) — Italy-specific paid-channel units (Apple
  Search Ads, Meta), the channels with no Italy data, Italy-vs-US multiplier,
  seasonality (feeds cac).
- `creator-economy.md` (DA4) — platform reach, DeRev tier bands and rates,
  affiliate reality, AGCOM/AGCM/IAP disclosure regime, engagement by tier
  (feeds distribution, cac).
- `communities-consumer-surface.md` (DA5) — verified-active Italian consumer
  surfaces per niche with ACTIVE/DEGRADED/DEAD/UNVERIFIABLE verdicts and
  language-trap warnings (feeds reddit + web-search templates).
- `global-benchmarks-sourcing.md` (DA6) — annotate-and-source pass over every
  Ring-3 figure the b2c packs already carry: matches, divergences, constructs
  (feeds all packs; the rewrite's decision list).
- `gated-report-digests.md` (2026-08-16) — extraction of the user-obtained
  gated reports (AppsFlyer Subscription Trends 2026, Adjust Mobile App
  Trends 2026 + its PDF): dated per-vertical D30 floors, Europe CPI cuts,
  per-category conversion; closes the retention-premium question (no
  primary source exists, gated or open). Includes the SplitMetrics 2026
  markets section (browser export): Italy below every top-15 ASA cost
  chart — second-vendor bound on MobileAction's Italy figures.

## Findings that change the packs (headline synthesis)

1. **Italy is an Android-majority market: 35% iOS / 65% Android** (StatCounter
   Jul 2026, page-view basis; no independent ownership-based cross-check exists
   publicly — treat 35% as an upper-ish bound). The pack's iOS-share table is
   confirmed stale globally: 8 of 9 rows are too low (Canada by ~10 points);
   the one row that still holds is Western Europe, the row Italy sits in.
   Demography is load-bearing: median age 48.2, 25.1% aged 65+.
2. **The IT App Store is a distinct storefront and its paid chart is reachable
   by domestic niche utilities** (live top-paid chart is full of Italy-specific
   small apps). Italian category names and chart names are captured for the
   templates.
3. **A subscription price in Italy is a decision, not a conversion.** Apple
   equalizes paid apps and one-time IAPs (EUR never below the USD numeral) but
   not auto-renewable subscriptions: observed EUR/USD ratios run 0.80–1.20 on
   the same product. Prices are VAT-inclusive (22%); net proceeds from 9,99 €
   ≈ 6,96 € under the Small Business Program. Euro price points stable since
   Oct 2022; the old tier ladder is superseded (800 price points, non-.99
   endings live).
4. **Ring-1 EUR anchors**: indie monthly band 4,99–9,99 €, annual clusters at
   29,99/39,99/49,99/59,99/69,99 € (implied discount 40–60%), lifetime unlocks
   alive at 8–15× annual. Weekly billing is an Italy-visible norm (Bending
   Spoons, Remini, Picsart). Bear (Parma-founded indie) at 2,99 €/mo is the
   sample floor; Bending Spoons prices *above* US incumbents — no defensive-
   pricing assumption.
5. **Only two paid channels have genuine Italy-specific measurements**: Apple
   Search Ads (Italy CPA $1.60, lowest tracked market; **Italy ≈ 0.42× US**,
   same-dataset — the one defensible Italy-vs-US multiplier, single-vendor,
   uncorroborated) and Meta (CPM median €10.48, ~50% below global; 2.3×
   seasonal peak-to-trough, autumn peak). TikTok Italy costs are NOT REPORTED
   — circulating figures are an AI-content citation ring, documented as such.
   No Italy CPI cut exists from any MMP (AppsFlyer structurally rolls Italy
   into Western Europe). Extending 0.42× across channels is a planning
   assumption and must be labeled as one.
6. **Correction feeding back into the b2b pack**: the Superads Italy CPC page
   carries no currency symbol — the b2b pass's "Meta ~€0.43" rests on an
   unverified USD assumption (more likely EUR, i.e. €0.50). Carry the ratio
   (~52% below global), not the level. The Milan/Turin +20–50% CPC premium in
   the b2b channels report traces to sources this pass excluded (US-adapted or
   content-mill) — treat it as an untested assumption.
7. **The Italian creator market is measured, but not for apps**: €425M (2026),
   ~40K professionals, 74% nano/micro. No app-install creator data exists in
   Italy (no CPI norms, no rate card, no case studies). The economic optimum
   for a solo dev is nano/micro on TikTok/Instagram (nano floor €100–300 per
   IG post; engagement falls monotonically with tier; January is the cheapest
   month). Amazon.it affiliate pays **0% on Android apps**. Disclosure
   liability falls on the commissioning advertiser via Codice del Consumo /
   AGCM (€65K fines, June 2025), not the 500K-follower AGCOM register; contract
   for the IAP Digital Chart wording. Rate tables must use DeRev's own tier
   bands — the generic nano/micro/mid/macro bands have no published Italian
   figures.
8. **47 verified-active Italian consumer surfaces, and four niches with none**:
   language learning, parenting (on Reddit), general cooking, and
   productivity-as-such have no live Italian-language community — load-bearing
   absences for the templates. Strongest surfaces: r/ItaliaPersonalFinance
   (281K, 25 posts in 9h), r/italygames (377K), r/seriea (530K), r/Universitaly
   (137K), hwupgrade.it/forum, bodyweb.com/forum, giardinaggio.it/forum.
   **English-language trap subs must not enter Italy-first templates**
   (r/ItalianFood, r/ItalyTravel, r/askitaly, r/italianlearning — all
   foreigners). "Discussion moved to private groups" is supportable for
   parenting only. Telegram groups are unverifiable (channels are broadcast).
   Facebook groups stay existence-signal only. Altroconsumo's community and
   complaints board are verified-active review surfaces; Trustpilot IT is
   bot-walled.
9. **Ring-3 sourcing verdicts (DA6) set the D-B decision list**: the retention
   D30 table runs **2–4× above every published cross-industry median** (3–7%
   published; the rumored subscription-app premium traces only to content
   mills) — either the column comes down or it gets restated with a real
   citation that does not currently exist in the open. The annual-discount
   guidance ("avoid >60%") contradicts the published market average (63–67%
   off). Paid CPI floors sit at published ceilings, and the CAC table
   conflates cost-per-install with cost-per-paying-user (10–50× apart) — a
   structural fix. Confirmed good: $3–7/mo fallback price, freemium typical
   conversion, most k-factor rows, and the $500K SOM-fantasy check ("if
   anything conservative": only 4.6% of new apps reach $10K MRR in 2 years).
10. **Confirmed constructs (label, do not source)**: SOM capture rates,
    community-size multipliers (whose review row also conflates rating rate
    0.5–2% with written-review rate 0.05–0.2% — implying 500–2,000×, not
    50–100×), search-intent conversion, six of nine organic CAC rows,
    demand-driver premium multipliers, D30→lifespan mapping, SOM verdict bands
    (whose "medium" is a top-10% outcome against real revenue distributions).

## Provisioning (user actions, all optional)

Gated reports that would upgrade specific figures if pulled manually:

- **Adjust "Mobile app trends 2026"** and **AppsFlyer "Subscription app
  marketing trends 2026"** — the only places a real subscription-app D1/D7/D30
  table might exist; would settle the retention-divergence decision (D-B
  step 6).
- **SplitMetrics Apple Ads Benchmarks 2026** (91 markets) — the natural
  independent cross-check on MobileAction's Italy CPT/CPA.
- **DeRev Listino 2026 full grid** (lead form) — the complete per-tier EUR
  rate table; only press-quoted points are public.

## Consolidated negative-result log (DA7)

Each report ends with its own "does not exist publicly" log; those entries are
authoritative. The cross-cutting absences a pack author is most likely to be
tempted to invent:

- No independent (non-StatCounter) measurement of the Italian iOS/Android
  split; no published "Western Europe average" region.
- No measurement of Italians' willingness to pay for *app* subscriptions
  specifically (streaming proxies only: 27,50 €/household/month); no Italian
  WTP split by app category; no ARPU for Italian iOS users.
- No Italy-specific TikTok Ads cost benchmark from a disclosed dataset; no
  Meta CPI for Italy; no Google App Campaigns CPI for Italy or Europe; no
  Italy-cut Google Ads study with disclosed methodology; no MMP CPI benchmark
  broken out to Italy.
- No Italian app-install creator-campaign data of any kind; no published
  Italian rates for the generic "micro 10–100K" or "macro >500K" bands; no
  documented "free app subscription for a post" practice; no parenting-vertical
  or calcio-specific creator data.
- No live Italian-language community for: language learning (all large
  surfaces are foreigners learning Italian), parenting on Reddit, general
  cooking, productivity-as-such, dedicated consumer-app discussion
  (r/AndroidItalia is DEGRADED at 1,236). No verified niche Italian consumer
  Discord.
- Ring-3 constructs confirmed to exist nowhere publicly: indie capture rates,
  community-multiplier conversions, search-intent-to-install rates, organic
  channel CAC, driver-based pricing/retention multipliers, D30→lifespan
  mapping.

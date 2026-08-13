# Global (Ring-3 / Western) b2c benchmark sourcing — DA6

Research date: 2026-08-13. Scope: annotate every GLOBAL benchmark figure carried by the five
b2c calibration packs of `skills/idea-validation/references/calibration/b2c/` with the most
plausible original published source, judge whether the pack's range matches that source, and
mark the figures that no public source supports.

This report does not edit the packs. It is input for a rewrite step.

## How to read the verdicts

| Verdict | Meaning |
|---|---|
| **matches** | A published source exists and the pack's range contains or brackets the source's number. |
| **diverges** | A published source exists and its number falls outside the pack's range. Both numbers are stated. |
| **construct** | No public source states this figure. It is an invented calibration value. |
| **construct (anchored)** | No public source states this figure, but a published source supports the *shape* of the claim (an adjacent measurement, a general principle). |

Confidence is about the *sourcing*, not about whether the pack's number is good advice:
high = primary publisher, dated, figure read directly; medium = primary figure reached through a
secondary summary, or the source measures a near-neighbour of the pack's quantity;
low = no source, or only practitioner anecdote.

## Source-quality warning

Searches for "app retention benchmarks by category" and "CPI benchmarks 2026" return a large
population of AI-generated aggregator pages (vmobify, core-mba.pro, semnexus, mwm.ai, trysonar,
appsops.store, ad-stack.ai, insertaffiliate, uprowshub, hub.causo.ai, admiral.media). They publish
confident category tables and cite Adjust / AppsFlyer / Sensor Tower in the abstract without
linking to a specific figure, and they contradict each other by 3–5x on the same row. **None of
them is used as a source below.** Where one is mentioned it is labelled as an uncorroborated
tertiary page. Every figure marked "matches" or "diverges" traces to a named primary publisher
(Adjust, AppsFlyer, RevenueCat, Adapty, StatCounter, Statista, Business of Apps, NN/g, Extole) or
to a named practitioner writing from their own data (Andrew Chen, Rahul Vohra, individual launch
retrospectives).

A second warning specific to retention: published benchmarks measure **all installs of all apps**,
including ad-supported and hyper-casual. The packs implicitly target indie subscription apps, which
plausibly retain better. I tried and failed to verify that premium at a primary source — see §1.2
and negative-log entry 1.

## Scope note

Tables in the packs that make **no numeric claim** are annotated once and not chased: the pricing
model selection criteria, the CAC channel relevance filter, the churn risk factor library, the
B2B2C signal list, and the featured-potential checklist. They are qualitative decision aids with no
benchmark to source, so the rewrite step should not expect source rows for them.

## Sources cited, with dates and staleness flags

| Source | URL | Date | Age flag |
|---|---|---|---|
| StatCounter Global Stats, mobile OS market share | https://gs.statcounter.com/os-market-share/mobile/ | May–July 2026 by region | current |
| RevenueCat, State of Subscription Apps 2026 | https://www.revenuecat.com/state-of-subscription-apps | 2026-03 (2025 data) | current |
| RevenueCat SOSA 2026 business breakout | https://www.revenuecat.com/state-of-subscription-apps-2026-business/ | 2026-03 | current |
| SaaStr readout of SOSA 2026 | https://www.saastr.com/the-top-10-learnings-from-revenuecats-state-of-subscription-apps-how-115000-mobile-apps-deliver-16b-in-revenue-whats-working-whats-quietly-killing-growth/ | 2026-03-07 | current |
| Adapty, State of In-App Subscriptions 2026 | https://adapty.io/state-of-in-app-subscriptions/ | 2026-03-05 | current |
| Airbridge, subscription app pricing by category | https://www.airbridge.io/en/blog/subscription-app-pricing-by-category-2026-benchmark | 2026-05-13 (RevenueCat **2024** data) | **underlying data ~2 years old** |
| Adapty, App Store conversion rate benchmarks | https://adapty.io/blog/app-store-conversion-rate/ | 2026-01-02 | current |
| AppFollow, ASO metrics (cites Apple Ads, Sensor Tower) | https://appfollow.io/blog/app-store-optimization-metrics | 2026-06-19 | current |
| Applyra, State of ASO 2026 (460k keywords) | https://www.applyra.io/blog/state-of-aso-2026 | 2026-07-03 | current |
| Kyle Poyar, 2026 free-to-paid conversion report (ChartMogul data) | https://www.growthunhinged.com/p/free-to-paid-conversion-report | 2026-02-04 | current |
| Andrew Chen, Braindump on viral loops | https://andrewchen.substack.com/p/braindump-on-viral-loops | 2025-11-13 | current |
| Adapty, mobile app referral program (quotes Vohra) | https://adapty.io/blog/mobile-app-referral-program/ | 2026-01-11 | current |
| fromscratch, Product Hunt launch strategy (named case studies) | https://fromscratch.dev/blog/product-hunt-launch-strategy | 2026-02-26 | current |
| Business of Apps, App Subscription Trial Benchmarks | https://www.businessofapps.com/data/app-subscription-trial-benchmarks/ | 2025-10-23 | current |
| AppsFlyer, Subscription app marketing trends 2026 | https://www.appsflyer.com/resources/reports/subscription-marketing/ | 2026-03-26 | current but **gated** — figures not readable |
| Adjust, Mobile app trends: 2026 edition | https://www.adjust.com/resources/ebooks/mobile-app-trends-2026/ | 2026 (2025 data) | current but **gated** — retention table not readable |
| Business of Apps, Cost per Install Rates | https://www.businessofapps.com/ads/cpi/research/cost-per-install/ | 2025-02-27 | **18 months — flag** |
| RevenueCat, State of Subscription Apps 2025 | https://www.revenuecat.com/state-of-subscription-apps-2025/ | 2025-03-14 | **17 months — flag** |
| Tim Holmgren, #1 Product of the Day retrospective (iOS) | https://medium.com/@tim.holmgren/how-i-built-launched-and-hit-1-on-product-hunt-to-get-1-000-new-users-0a1d7450f7b9 | 2025-07-25 | **13 months — flag** |
| TechCrunch on RevenueCat SOSA 2024 | https://techcrunch.com/2024/03/12/most-subscription-mobile-apps-dont-make-money-new-report-shows/ | 2024-03-12 | **2.5 years — flag** |
| Sendbird roundup of Statista / Adjust / AppsFlyer retention | https://sendbird.com/blog/app-retention-benchmarks-broken-down-by-industry | 2024-03-12 | **2.5 years — flag** |
| Kyle Poyar, what is a good free-to-paid conversion (OpenView) | https://www.lennysnewsletter.com/p/what-is-a-good-free-to-paid-conversion | 2023-08-01 | **3 years — flag** |
| Phiture, iOS rating prompt data | https://phiture.com/asostack/unlocking-the-data-behind-the-ios-rating-prompt-8e942bfe9134/ | 2019-06-25 | **7 years — flag** |
| Jakob Nielsen / NN/g, Participation Inequality (90-9-1) | https://www.nngroup.com/articles/participation-inequality/ | 2006-10-08 | **20 years — flag** (still the canonical citation) |
| van Mierlo, The 1% rule in four digital health social networks | https://pubmed.ncbi.nlm.nih.gov/24496109/ | 2014-02-04 | **12 years — flag** |
| Adjust, app user retention handbook | https://www.adjust.com/resources/guides/user-retention/ | undated | **undated — flag** |
| Saxifrage, K-Factor Benchmarks (compiles Vohra, Adjust, Extole) | https://www.saxifrage.xyz/post/k-factor-benchmarks | undated | **undated — flag** |

---

## 1. `retention.md`

### 1.1 Stickiness Factor Anchors (habit formation)

| Pack figure | Best source found | Match verdict | Confidence |
|---|---|---|---|
| Six 1–5 factor anchors (usage frequency, external trigger, progress/reward loop, network effects, data lock-in, habit stack) | No published source. The vocabulary tracks the Hooked model (Nir Eyal, trigger → action → variable reward → investment) and BJ Fogg's behaviour model, but neither publishes a 1–5 scoring rubric or these six factors. | **construct (anchored)** — the framework is recognisable, the scoring anchors are invented | low |

### 1.2 Retention Benchmarks by Category (D1 / D7 / D30)

This is the pack's most consequential divergence. Published cross-industry D30 medians sit at
**5–7%**; the pack's D30 column runs **5–25%**, with six of eight categories floored at 8% or above.

Primary anchors:

- **Adjust, app user retention handbook** (https://www.adjust.com/resources/guides/user-retention/, no publication date shown — flag as undated): global retention "26% on day 1, 13% by day 7 … after 30 days the retention rate generally settles at 7%". iOS D1 27% / D30 8%; Android D1 24% / D30 6%. Vertical figures given: gaming D1 29%, e-commerce D1 20%, social media D1 23%, fintech D1 22%, fintech D30 9%, travel D30 5%.
- **Statista mobile app user retention** (https://www.statista.com/statistics/259329/mobile-app-user-retention-rate-worldwide/, 2024 study of 1,000+ apps — **older than 12 months, flag**), summarised with AppsFlyer and Adjust side by side in Sendbird's roundup (https://sendbird.com/blog/app-retention-benchmarks-broken-down-by-industry, 2024-03-12 — **older than 12 months, flag**): D1 average 25.3%; D30 averages 5.7% (Statista), 6.5% (Adjust), 3.36% (AppsFlyer). Per-industry D30: digital banking 11.6%, marketplaces 8.7%, finance 5.8%, shopping 5.6%, lifestyle 4.5%, productivity 4.1%, digital health 4.0%, social media 3.9%, travel 3.9%, entertainment 3.8%, utilities 3.4%, gaming 2.3%.
- **Business of Apps, App Subscription Trial Benchmarks** (https://www.businessofapps.com/data/app-subscription-trial-benchmarks/, 2025-10-23): "More than 90 percent of users churn from most apps within the first 30 days of download" — i.e. D30 below 10% is the normal case.
**The subscription-app retention premium: searched for, not found at source.** The one figure that
would justify the pack's higher band is a subscription-app D30 benchmark. A number is circulating —
"**14% D30 for subscription apps vs 5.4% for ad-supported**", attributed to AppsFlyer — and I went
after it directly rather than accepting it third-hand. Result:

- **AppsFlyer, "Subscription app marketing trends 2026"** (https://www.appsflyer.com/resources/reports/subscription-marketing/, 2026-03-26) **does exist** and is the right shape: 1.7 billion paid installs, 2,900 subscription apps, 13 categories. But it is **gated behind a download form**, and its own public contents list promises "trial adoption, conversion rates, and install-to-paid benchmarks" — it does **not** advertise a retention curve at all.
- **AppsFlyer's public benchmarks hub** (https://www.appsflyer.com/benchmarks/) is an interactive tool behind a signup, exposing no figures to a fetch.
- **Adjust, "Mobile app trends: 2026 edition"** (https://www.adjust.com/resources/ebooks/mobile-app-trends-2026/) is likewise gated. Its public preview surfaces install, session and CPI figures per vertical (e.g. e-commerce CPI $0.98) but no D1/D7/D30 table.
- The 14% / 5.4% pair traces only to AI-generated aggregators (core-mba.pro; digitalapplied.com gives 13.8% / 5.3% from a near-identical table). Two aggregators repeating each other is not corroboration, and neither links to a page in the AppsFlyer report.

**Consequence for the rewrite:** the subscription premium is plausible and widely asserted but
**unverified at any primary source**. The "diverges 2–4x" verdicts below therefore stand
unqualified. The pack cannot be repaired by adding a scope note that cites this number; either
someone downloads the AppsFlyer and Adjust reports and reads the actual figure, or the D30 column
comes down toward the published medians. Logged as negative-log entry 1.

| Pack row (D1 / D7 / D30) | Best source found (what it says) | Match verdict | Confidence |
|---|---|---|---|
| Social / messaging 30–40 / 20–30 / **15–25%** | Statista 2024 social media D30 **3.9%**; AppsFlyer **3.11%**; Adjust social D1 23% (pack D1 30–40%) | **diverges** — pack D30 is ~4–6x the published median; pack D1 is ~1.5x Adjust's | medium |
| Health & fitness 25–35 / 15–22 / **10–18%** | Statista digital health D30 **4.0%**; AppsFlyer health & fitness **2.78%**; Adjust health & fitness D1 21–24% by region | **diverges** — pack D30 is ~3–4x published | medium |
| Finance / budgeting 25–35 / 16–24 / **12–20%** | Statista finance D30 **5.8%**, digital banking **11.6%** (D1 30.3%, D7 17.6%); Adjust fintech D30 **9%** | **partially matches** — the pack range brackets the *banking* sub-segment (11.6%) and Adjust's fintech 9%, but sits ~2–3x above general finance (5.8%). The pack's D1/D7 match Statista banking (30.3 / 17.6) closely | medium |
| Productivity / tools 20–30 / 12–18 / **8–15%** | Statista productivity D30 **4.1%**, utilities **3.4%**; AppsFlyer productivity **2.81%**, utilities **2.44%**; Statista productivity D1 **17.1%** (pack 20–30%) | **diverges** — pack D30 floor is 2x published median; pack D1 floor is above published average | medium |
| Games (casual) 25–35 / 10–15 / **5–12%** | Statista gaming D30 **2.3%**, "between 2.3% and 5.4% with casual and mid-core seeing the biggest tail-off"; Adjust gaming D1 **29%** | **partially matches** — pack D1 25–35% brackets Adjust's 29%; pack D30 floor of 5% sits at the *top* of the published 2.3–5.4% band | medium |
| Education 20–30 / 10–16 / **6–12%** | No education-specific D30 in the primary sources I could open. Adjacent: Statista lifestyle 4.5%, entertainment 3.8% | **construct** for the D30 column; D1/D7 unsourced | low |
| Lifestyle / habit 25–35 / 14–22 / **10–18%** | Statista general lifestyle D30 **4.5%**, D1 **20.9%** | **diverges** — pack D30 is ~2–4x published; pack D1 floor is above published average | medium |
| Creative tools 25–35 / 15–24 / **12–20%** | No photo/video D30 in the primary sources. RevenueCat SOSA 2025 notes photo & video leads monthly *reactivations*, and 27.57% of photo & video apps reach $1,000 revenue in 2 years (highest of any category) — a monetisation figure, not retention | **construct** | low |

**Summary judgement on this table.** The relative *ordering* of categories in the pack is defensible
and broadly matches the published ordering (social and finance at the top, games and education at
the bottom). The *absolute level* of the D30 column is roughly 2–4x above every published
cross-industry median, and no verifiable public figure closes that gap. As written the numbers read
as category medians and they are not: a rewrite must either restate them as an explicit
top-quartile subscription-app band (with a real citation, which does not currently exist in the
open literature) or bring the column down toward the 3–9% range the primary sources support.

### 1.3 Position-within-range and demand-driver shift

| Pack figure | Best source found | Match verdict | Confidence |
|---|---|---|---|
| Top of range if `habit_formation_score` ≥ 4.0 and desire strength "strong"; bottom if < 2.5 or "weak" | None. Internal scoring mechanics. | **construct** | low |
| Shift D30 by ±2 percentage points for survival/control vs curiosity primary driver | None. No published study relates a psychological demand driver to a retention delta. | **construct** | low |

### 1.4 Churn Risk Factor Library

| Pack figure | Best source found | Match verdict | Confidence |
|---|---|---|---|
| Seven named churn factors (no external trigger, one-shot value, free-alternative gravity, sustained behaviour change, data-entry burden, seasonal usage, goal-completion exit) | None as a published list. Individually recognisable from product-management writing; not a sourced taxonomy. | **construct** — qualitative, no numeric claim, so no sourcing burden | low |

### 1.5 Verdict Thresholds

| Pack figure | Best source found | Match verdict | Confidence |
|---|---|---|---|
| sticky if D30 ≥ 15%; disposable if D30 < 8% | None. Compare: Adjust global D30 settles at 7%, Business of Apps says >90% of users churn by D30 | **construct** — and worth noting that the "disposable" floor of 8% sits *above* the published global median, so a median app is classified disposable | low |

---

## 2. `market-sizing.md`

### 2.1 Intent Conversion Benchmarks (Approach A — search volume)

The pack converts *web search volume* into app users. No publisher measures that funnel. The
nearest measured funnel is *App Store* search, which is a different denominator (people already
inside the store).

Primary anchors:

- **Adapty, App Store conversion rate benchmarks** (https://adapty.io/blog/app-store-conversion-rate/, 2026-01-02): impression → page view 6–12%; page view → install 25–27%; **impression → install 3.6–3.8%** (US App Store).
- **AppFollow / Apple Ads** (https://appfollow.io/blog/app-store-optimization-metrics, 2026-06-19, citing Apple Ads and Sensor Tower): ~65% of App Store downloads follow a search; >70% of visitors use search; Sensor Tower puts search at ~59% of downloads.
- **Growth by Kev, App Store conversion benchmarks** (https://www.growthbykev.com/blog/conversion-rate-benchmarks, 2026-01-15, practitioner compilation): organic search CVR "good" 8–12%, "strong" >12%.

| Pack figure | Best source found | Match verdict | Confidence |
|---|---|---|---|
| Direct solution search ("app to track X") → **8–15%** | No source for web-search-to-install. Nearest: App Store search page CVR 8–12% "good" (Growth by Kev), impression→install 3.6–3.8% (Adapty) | **construct (anchored)** — the number happens to land on App Store search CVR, but that measures a different funnel stage with a different denominator | low |
| Problem-aware search ("how to X") → 3–8% | None | **construct** | low |
| Category browsing ("best X apps") → 5–12% | None | **construct** | low |
| Tangential interest ("X tips") → 1–3% | None | **construct** | low |

### 2.2 Platform Multipliers (Approach B — community size proxy)

| Pack figure | Best source found | Match verdict | Confidence |
|---|---|---|---|
| Reddit subscribers × **20–50×** ("~2–5% of interested people join a subreddit") | **Jakob Nielsen, "Participation Inequality: The 90-9-1 Rule"** (https://www.nngroup.com/articles/participation-inequality/, **2006-10-08 — 20 years old, flag**): 90% lurkers, 9% occasional contributors, 1% heavy contributors; blogs closer to 95-5-0.1; Wikipedia 99.8-0.2-0.003. Corroborated empirically by van Mierlo, "The 1% rule in four digital health social networks" (https://pubmed.ncbi.nlm.nih.gov/24496109/, 2014 — **older than 12 months, flag**) | **construct (anchored)** — the 90-9-1 family supports "a small single-digit percentage participates", which is the shape of the claim, but nobody has published a subscriber-to-interested-population multiplier | low |
| TikTok hashtag creators × **100–500×** | None. Nielsen's blog ratio (95-5-0.1) implies creator fractions well below 1%, consistent with a 3-digit multiplier, but no measurement exists | **construct (anchored)**, weakly | low |
| App Store reviews for top competitor × **50–100×** ("~1–2% of users leave reviews") | Practitioner benchmarks only, and they split rating from review: Berke Sarıkaya (LinkedIn, 2025-11-16) reports 0.5–2% of users leave a *rating* and 0.05–0.2% leave a *written review*; refined.so (2025-11-16) says 1–2% leave a rating once prompted; Phiture (https://phiture.com/asostack/unlocking-the-data-behind-the-ios-rating-prompt-8e942bfe9134/, 2019-06-25 — **7 years old, flag**) measured 0.07% prompt-to-review conversion | **diverges on the underlying rate** — if the pack means visible *review counts*, the practitioner rate is 0.05–0.2%, implying a **500–2,000×** multiplier, not 50–100×. The pack's 1–2% is the *rating* rate. No primary publisher measures either | low |
| Newsletter subscribers × **10–30×** | None | **construct** | low |

### 2.3 Platform Filter — iOS Market Share by Region

The one table in the packs with a clean, current, free primary source — and **eight of its nine rows
are too low**. **StatCounter Global Stats, mobile OS market share** (https://gs.statcounter.com/os-market-share/mobile/, every row read per region on 2026-08-13; StatCounter's
latest month varies slightly by region, May–July 2026):

| Pack row | StatCounter, latest month | Match verdict | Confidence |
|---|---|---|---|
| United States 55–58% | **59.58%** (Jul 2026) | **diverges** — above the pack's ceiling | high |
| United Kingdom 50–53% | **53.92%** (Jul 2026) | **diverges** — just above the ceiling | high |
| Canada 53–56% | **65.91%** (Jul 2026) | **diverges materially** — ~10 points above the ceiling | high |
| Australia 55–58% | **63.70%** (Jul 2026) | **diverges** — ~6 points above the ceiling | high |
| Western Europe (avg) 30–35% | Germany **33.10%**, France **36.72%**, Italy **33.87%** (Jun), Spain **32.66%** (May) — big-four average ≈ **34%** | **matches** — the only row that holds. Caveat: if "Western Europe" is meant to include the UK (53.92%), the average rises to ~38% and the row diverges | high |
| Global 25–28% | **31.60%** (Jul 2026) | **diverges** — ~4 points above the ceiling | high |
| Southeast Asia 10–15% | Indonesia **22.78%** (Jul 2026) — and Indonesia is one of SEA's *lower*-iOS markets; Singapore, Malaysia and Thailand run higher | **diverges materially** — the pack's ceiling is under half the one SEA country checked | medium (single-country proxy, no SEA aggregate on StatCounter) |
| India 4–6% | **7.50%** (Jul 2026) | **diverges** — above the ceiling | high |
| Latin America 12–18% | South America aggregate **18.33%** (Jun 2026); Brazil **22.41%** (Jul 2026) | **diverges** — the regional aggregate sits at the pack's ceiling and the largest market is 4 points beyond it | high |

The pattern is systematic and now demonstrated rather than inferred: every row that moved is low,
none is high, and the errors are largest exactly where iOS grew fastest (Canada, Australia, SEA,
LATAM). The table reads like a snapshot from roughly 2021–2022 that was never refreshed. The one
row that still holds, Western Europe, holds because continental Europe's iOS share has been
comparatively flat — which is the relevant row for an Italy-first pass, and Italy specifically sits
at **33.87%**, squarely inside the pack's band.

### 2.4 SOM Capture Rate Benchmarks by Category

| Pack figure | Best source found | Match verdict | Confidence |
|---|---|---|---|
| Ten-row table, year-1 capture 0.01–2.0% of SAM and year-3 capture 0.1–5.0%, by app category | **None.** This confirms the prior established by the sibling b2b pass: no publisher measures what share of an addressable market an indie app captures. Searches for capture-rate benchmarks return SaaS market-share commentary and generic bottom-up sizing method pages (e.g. BigIdeasDB's "2% conversion is realistic for a well-marketed micro SaaS"), never a category table | **construct** | low |
| Lower-end / upper-end selection rules (saturation, founder tier, distribution advantage) | None | **construct** | low |

### 2.5 Fallback Price and Reality Checks

| Pack figure | Best source found | Match verdict | Confidence |
|---|---|---|---|
| Category fallback price **$3–$7/mo** for typical B2C subscription apps | **RevenueCat SOSA 2026** via Airbridge's breakout (https://www.airbridge.io/en/blog/subscription-app-pricing-by-category-2026-benchmark, 2026-05-13; underlying RevenueCat dataset is 75,000+ apps, **2024 data — flag the lag**): monthly **bottom quartile $3.26, median $6.68**, most common $9.99, top quartile $11.99, P90 $19.99 | **matches** — the pack's $3–$7 band is almost exactly Q1-to-median of the real distribution | high |
| TAM inflation check: TAM > $10B for a niche indie app | None; internal heuristic | **construct** | low |
| SAM too broad: SAM > 50% of TAM | None; internal heuristic | **construct** | low |
| SOM fantasy: SOM year 1 > $500K for a solo developer; "most indie apps earn $0–$50K in year 1" | **Strongly corroborated.** RevenueCat SOSA 2026 (https://www.revenuecat.com/state-of-subscription-apps, 2026-03, 115,000+ apps / $16B revenue): only **4.6% of newly launched apps reach $10K in monthly revenue within two years**. RevenueCat SOSA 2024 via TechCrunch (https://techcrunch.com/2024/03/12/most-subscription-mobile-apps-dont-make-money-new-report-shows/, 2024-03-12 — **older than 12 months, flag**): median monthly revenue 12 months after launch is **under $50**; 17.2% ever reach $1,000/mo; 3.5% reach $10,000/mo. RevenueCat SOSA 2025: top 5% of newly launched apps earn **$8,880/mo** after two years, bottom 25% no more than $19. Adapty, State of In-App Subscriptions 2026 (https://adapty.io/state-of-in-app-subscriptions/, 2026-03-05, 16,000 apps / $3B): median app **$492/mo**, 59.3% make under $1,000 total, only 7.2% cross $100K | **matches, and the claim is if anything conservative** — median year-1 revenue is under $600/yr, so "$0–$50K" is generous | high |

### 2.6 SOM Verdict Bands

| Pack figure | Best source found | Match verdict | Confidence |
|---|---|---|---|
| SOM y1 > $200K = large; $50–200K = medium; $10–50K = niche; < $10K = micro-niche | No published band scheme. Cross-check against the revenue distributions above: $200K/yr ≈ $16.7K/mo, which is beyond the top 5% two-year outcome ($8,880/mo). $50K/yr ≈ $4.2K/mo, roughly the top decile | **construct** — internally coherent but the bands sit well into the tail of the real distribution; "medium" is roughly a top-10% outcome | low |

---

## 3. `pricing.md`

### 3.1 Pricing Models and Indie Sweet Spots

| Pack figure | Best source found | Match verdict | Confidence |
|---|---|---|---|
| Freemium → subscription sweet spot **$3–8/mo or $20–50/yr** | RevenueCat SOSA (via Airbridge, 2026-05-13): monthly Q1 $3.26 / median $6.68; annual Q1 $17.59 / **median $29.99** / most common $29.99 / Q3 $54.99. SaaStr's SOSA 2026 readout (https://www.saastr.com/the-top-10-learnings-from-revenuecats-state-of-subscription-apps-how-115000-mobile-apps-deliver-16b-in-revenue-whats-working-whats-quietly-killing-growth/, 2026-03-07): market has stabilised at $4.99–$6.99 weekly, $7.99–$9.99 monthly, $29.99–$39.99 annually; **median annual $34.80**, up from $31.60 | **matches** — pack's monthly band is Q1-to-just-above-median; annual band $20–50 brackets the $29.99–$34.80 median | high |
| Subscription only (paywall) **$5–15/mo** | Same source: median $6.68, most common $9.99, Q3 $11.99, P90 $19.99 | **matches** — brackets median through P90-ish | high |
| One-time purchase $3–10; consumables $1–5/pack; freemium + consumables $2–10 packs; tip jar $1–5 | No published benchmark for non-subscription price points at this granularity. RevenueCat SOSA 2025 notes 35% of apps now mix subscriptions with consumables or lifetime purchases (Gaming 61.7%, Social & Lifestyle 39.4%) — confirms the *models* exist, not the prices | **construct** for the price bands; the model mix is sourced | low |
| Lifetime deal $20–60 = **3–5× annual price** | None | **construct** | low |

### 3.2 Demand-Driver Premium Multipliers

| Pack figure | Best source found | Match verdict | Confidence |
|---|---|---|---|
| Survival 1.3–1.8×; Status 1.5–2.0×; Belonging 1.0–1.3×; Control 1.2–1.5×; Curiosity 0.8–1.2× | **None.** No publisher relates a psychological demand driver to a pricing multiplier. Weak directional support: RevenueCat's category price medians do put Health & Fitness ($9.70/mo) near 2× Gaming ($4.99/mo), which is the direction "survival > curiosity" predicts | **construct** | low |
| Secondary-driver bonus +10% if secondary ≥ 3 and differs from primary | None | **construct** | low |

### 3.3 WTP Benchmarks by App Category

Important framing note: the pack calls this column "WTP", but every available source measures
**observed prices charged**, not willingness to pay. They are not the same quantity — observed
price is a supply-side equilibrium that already reflects competitive pressure. Sourcing below is
against observed prices.

**RevenueCat SOSA category medians** (via Airbridge, 2026-05-13; RevenueCat 2024 data — **flag the
lag**): Health & Fitness weekly $4.99 / monthly $9.70 / annual $39.99; Education $5.99 / $8.38 /
$44.99; Business $6.15 / $7.58 / $37.50; Gaming $4.99 / $4.99 / $20.55. **Adapty 2026**
(2026-03-05, 16,000 apps): global medians $7.48/week, **$12.99/month**, $38.42/year — materially
higher than RevenueCat's, and Adapty notes European apps charge 29–39% more than North American.

| Pack row (monthly) | Best source found | Match verdict | Confidence |
|---|---|---|---|
| Health & fitness $5–15 | RevenueCat median **$9.70** | **matches** | high |
| Education / learning $5–15 | RevenueCat median **$8.38** | **matches** | high |
| Nutrition / diet $5–12; Meditation / mental health $5–15 | No sub-category split published at this granularity (both roll into Health & Fitness at $9.70) | **construct** at sub-category level; consistent with the parent category | low |
| Finance / budgeting $3–10 | No RevenueCat finance row in the accessible breakout | **construct** | low |
| Productivity / task management $3–8 | RevenueCat "Business" median **$7.58** is the nearest proxy | **matches** (against a proxy category) | medium |
| Habit tracking $2–6 | None | **construct** | low |
| Creative tools (photo/video) $3–10 | No Photo & Video row in the accessible breakout | **construct** | low |
| Dating / social $5–25 | None accessible | **construct** | low |
| Parenting / family $3–8 | None | **construct** | low |
| Utility / scanner / converter **$1–4** | No Utilities price row accessible, but Adapty 2026 reports Utilities generate the **highest weekly subscription revenue share (73.6%)** and the highest per-subscriber trial LTV at **$68.90 over 12 months** — a signal that utilities monetise *above*, not below, the market | **likely diverges (low)** — the pack treats utilities as the cheapest category; the one accessible signal points the other way | low |
| AI-powered tools $5–20 | RevenueCat SOSA 2026: AI apps sustain a **41% Year-1 realized LTV premium** ($30.16 vs $21.37 median); SOSA 2025: AI apps show revenue per install above $0.63 at D30 | **construct on price, but the premium direction is sourced** | medium |
| One-time WTP column ($2–$40 by category) | None | **construct** | low |
| Sanity rule: >2× above category range = too optimistic | None | **construct** | low |

### 3.4 Annual vs. Monthly Discount Norms

This is a clear divergence: the pack's "avoid" zone is where the market actually sits.

| Pack figure | Best source found | Match verdict | Confidence |
|---|---|---|---|
| Annual discount sweet spot **40–50% off monthly**; 50–60% "aggressive"; **>60% = avoid, signals the app isn't worth the monthly price** | **RevenueCat SOSA data via Airbridge** (2026-05-13): "On average, apps offer a **67% discount** on annual vs equivalent monthly pricing." Independently derivable from the same medians: monthly median $6.68 × 12 = $80.16 vs annual median $29.99 → **63% off** | **diverges** — the market average (63–67%) sits inside the pack's "avoid" band. The pack's per-category "annual discount sweet spot" column (30–60% depending on category) is entirely a **construct**; no source splits discount depth by category | high (on the aggregate); low (on the per-category column) |
| Annual-plan adoption by category | RevenueCat SOSA 2026 (https://www.revenuecat.com/state-of-subscription-apps-2026-business/): Health & Fitness leads annual adoption at **68%**; Gaming is 82% weekly; Productivity is 76.7% monthly and draws 90.7% of its revenue from monthly plans; Education, Travel, Shopping favour annual at 59–66% | **not in the pack** — a real, current, category-level figure the pack could carry but does not | high |

### 3.5 Freemium Conversion Estimation

Real sources exist and the pack's *typical* column is broadly right. The *top-quartile* column and
the per-category split are not sourced.

Primary anchors:

- **OpenView Product Benchmarks / Kyle Poyar, Lenny's Newsletter** (https://www.lennysnewsletter.com/p/what-is-a-good-free-to-paid-conversion, **2023-08-01 — 3 years old, flag**): freemium self-serve **3–5% is GOOD, 6–8% is GREAT**; sales-assisted freemium 5–7% good, 10–15% great; free trial 8–12% good.
- **ChartMogul SaaS Conversion Report / Kyle Poyar, "The 2026 free-to-paid conversion report"** (https://www.growthunhinged.com/p/free-to-paid-conversion-report, 2026-02-04): median free-to-paid across all products **8%**; among freemium products, 25% convert below 2.5%, 29% between 2.5–7.5%, 25% between 10–15%.
- **RevenueCat SOSA 2026** (2026-03): freemium apps convert downloads to paid at **2.1% median at D35**, hard-paywall apps at **10.7%** (SOSA 2025: 2.18% vs 12.11%). This is download-to-paid, a wider denominator than free-user-to-paid.

| Pack figure | Best source found | Match verdict | Confidence |
|---|---|---|---|
| "Typical conversion" column, 1–8% across categories | OpenView/Lenny 3–5% good; ChartMogul median 8% all-products; RevenueCat freemium D35 median **2.1%** | **matches** — the pack's typical band brackets every published median | high |
| "Top-quartile" column, 5–20% across categories | ChartMogul: 25% of freemium products convert 10–15%; a further tail above that. OpenView "great" = 6–8% | **partially matches** — the 10–15% end is supported by ChartMogul's distribution; the pack's 20% ceiling (social/dating, AI) exceeds anything published as a quartile figure | medium |
| Per-category split (Health 2–5, Productivity 3–6, Creative 3–7, Education 2–5, Finance 3–6, Utility 1–4, Social/dating 2–8, AI 4–8) | **None.** No publisher breaks freemium free-to-paid conversion out by consumer app category. RevenueCat splits download-to-*trial* by category (Business highest at 8.9%, per Business of Apps 2025-10-23) and trial-to-paid by category (Travel highest at 48.7%, Health & Fitness 39.9% median / 68.3% at P90), but neither is the pack's metric | **construct** — the level is sourced, the per-category differentiation is invented | low |
| Five conversion-lift factors (value gating, free-tier generosity, pain of free, social proof, trial exposure) | Qualitative; no published rubric. Adjacent sourced facts: 80–82% of trial starts happen on day 0 (RevenueCat SOSA 2025); trials of 17–32 days convert best at 45.7% median vs 26.8% for short trials | **construct** | low |

### 3.6 Secondary Revenue Path (B2B2C)

| Pack figure | Best source found | Match verdict | Confidence |
|---|---|---|---|
| B2B2C price = **3–5× the consumer price per seat** | None | **construct** | low |
| Four B2B2C signals (expensing, team version, data value, workplace wedge) | Qualitative; no source needed | **construct** | low |

---

## 4. `cac.md`

### 4.1 Indie Budget Tiers

| Pack figure | Best source found | Match verdict | Confidence |
|---|---|---|---|
| Bootstrap $0–100/mo; Lean $100–500; Moderate $500–2,000; Serious >$2,000 | None. No publisher segments indie marketing budgets this way | **construct** — a definitional scheme rather than a measured benchmark, so low sourcing burden | low |

### 4.2 Channel Set and CAC Benchmarks

A structural note that affects every row: the pack's column is labelled "CAC" but the values read
as **cost per install**. Published data is CPI (cost per *install*), and CAC per *paying subscriber*
is 10–50× higher given 2–12% download-to-paid conversion. The pack should state which it means;
the mismatch is larger than any of the individual range disagreements below.

Primary anchors for the two paid rows:

- **Business of Apps, Cost per Install Rates** (https://www.businessofapps.com/ads/cpi/research/cost-per-install/, 2025-02-27 — **18 months old, flag**): iOS global CPI $1.50–3.50; Android $1.50–4.00; North America $2.50–5.00; EMEA $2.00–4.00; **Facebook Ads $1.00–3.00** (with a separate Facebook-specific projection of $2.00–5.50); **TikTok Ads $0.50–2.50** (separate TikTok-specific series projected $1.75–4.00 for 2024); Google Ads $0.50–2.50; ad networks $1.75–4.50.
- **AdAction 2026 figures** as compiled by insertaffiliate (https://insertaffiliate.com/blog/mobile-app-user-acquisition-cost-benchmarks/, 2026-05-14 — a secondary compilation, but it names AdAction and Business of Apps per line): Meta $2.00–5.50; Google UAC $1.50–4.50; TikTok $1.75–4.00; regional North America $2.50–5.00, EMEA $2.00–4.00, LATAM $0.50–2.00.

| Pack channel and range | Best source found | Match verdict | Confidence |
|---|---|---|---|
| `aso_organic` **$0.50–3.00** | **None.** Organic ASO has no per-install price; nobody publishes an "organic CAC" benchmark. The nearest measurable quantities are Apple Search Ads cost-per-tap (median $2.05 for Shopping, AppTweak 2025) and ASO effort cost, neither of which the pack is claiming | **construct** | low |
| `content_seo` $1.00–8.00 | None | **construct** | low |
| `tiktok_organic` $0.50–5.00 | None | **construct** | low |
| `reddit_community` $0.50–4.00 | None | **construct** | low |
| `paid_social_meta` **$3.00–40.00** | Business of Apps 2025: Facebook Ads CPI **$1.00–3.00** (FB-specific series $2.00–5.50); AdAction 2026 Meta **$2.00–5.50** | **diverges** — the pack's floor ($3.00) is at or above the published *ceiling*, and its ceiling ($40) is ~7× the published one. Defensible only if the pack means cost per activated/paying user, which it does not say | medium |
| `paid_social_tiktok` **$2.00–25.00** | Business of Apps 2025: TikTok Ads CPI **$0.50–2.50**; AdAction 2026 **$1.75–4.00** | **diverges** — same pattern: pack floor ≈ published ceiling | medium |
| `influencer` $2.00–25.00 | None. Creator-campaign CPI is not published as a benchmark range | **construct** | low |
| `word_of_mouth` $0.00–2.00 | None (definitionally near-zero marginal cost) | **construct** | low |
| `press_product_hunt` $0.00–5.00 | None | **construct** | low |
| Product Hunt modelled as a fixed cohort of **500–5,000 installs** | Practitioner data only, and it is rank-dependent. fromscratch (https://fromscratch.dev/blog/product-hunt-launch-strategy, 2026-02-26, case studies with named products): #1 of the Day 2,000–10,000 unique visitors and typically **600–800 signups**; Top 5 1,000–2,000 visitors and 100–400 signups; not featured under 500 visitors and "minimal" signups. Named launches: Dub.co #1 with 1,085 upvotes → **663 signups**; Tally 2.0 → 766 new users; Checklist Genie (iOS, Tim Holmgren, Medium 2025-07-25) #1 of the Day → **1,000+ downloads**, then settling to 25–50/day | **diverges (optimistic)** — the pack's range describes a top-5 finish. The median launch, which is not featured, lands an order of magnitude below the pack's floor. The 5,000 ceiling is not supported by any documented app launch I found | low |

### 4.3 Lifespan Mapping (D30 → average lifespan)

| Pack figure | Best source found | Match verdict | Confidence |
|---|---|---|---|
| D30 ≥ 25% → 12–18 months; 15–24% → 6–12; 8–14% → 3–6; < 8% → 1–3 | **None.** No publisher maps a D30 retention rate to an expected average lifespan. The relationship is derivable from a churn model, but the pack states no model, so the four bands are unsourced. Adjacent sourced facts that constrain it: RevenueCat SOSA 2026 reports ~72% of annual subscribers cancel within Year 1 (up from ~56% in the 2025 edition) and 12-month payer retention of 21.1% for AI apps vs 30.7% for non-AI on annual plans | **construct** | low |

### 4.4 D30 Fallbacks by Category

| Pack figure | Best source found | Match verdict | Confidence |
|---|---|---|---|
| Eight-row median D30 table, 5–25% | Identical to the D30 column of `retention.md` §1.2 by design — same sources, same verdicts. Published cross-industry median is 5–7% (Adjust), 5.7% (Statista), 3.36% (AppsFlyer) | **diverges** — see §1.2 row by row | medium |

---

## 5. `distribution.md`

### 5.1 Viral Loop Types and k-factor Ranges

The best-sourced table in the packs after iOS share, with three genuinely independent measurements.

Primary anchors:

- **Rahul Vohra (Superhuman), quoted widely and reproduced verbatim by Saxifrage** (https://www.saxifrage.xyz/post/k-factor-benchmarks, undated — **flag**) and Adapty (https://adapty.io/blog/mobile-app-referral-program/, 2026-01-11): "for a consumer internet product, a sustainable viral factor of **0.15 to 0.25 is good, 0.4 is great, and around 0.7 is outstanding**."
- **Andrew Chen, "Braindump on viral loops"** (https://andrewchen.substack.com/p/braindump-on-viral-loops, 2025-11-13): "Most of the time, you see viral factors that are **0.2 or 0.3 or below**"; a viral factor above ~0.5 is needed before the effect is even distinguishable from daily noise; k ≥ 1.0 windows are short-lived and platform-dependent.
- **Adjust k-factor study**, reported by Saxifrage: only **30% of apps have a measurable k-factor at all**; for that 30%, **median k = 0.45**. Games 22.5% have one; non-games 33.6%; e-commerce highest at 38.6%.
- **Extole**, 400 referral-program customers, reported by Saxifrage: 19% of potential advocates become advocates, 2 shares per advocate, 1 friend click per share, 13% click-to-customer → **k ≈ 0.05** for a pure referral program.

| Pack row | Best source found | Match verdict | Confidence |
|---|---|---|---|
| Inherent **0.5–1.5** | Vohra: 0.7 is "outstanding". Chen: k ≥ 1 is rare and short-lived. Adjust: median 0.45 among apps that have any k at all | **diverges (optimistic)** — the pack's *floor* sits at the level Chen calls barely-detectable and above Adjust's median; the ceiling of 1.5 exceeds anything either source describes as sustainable | medium |
| Collaborative 0.2–0.6 | Vohra: 0.15–0.25 good, 0.4 great. Chen: 0.2–0.3 typical. Adjust: median 0.45 | **matches** | medium |
| Word-of-mouth 0.1–0.4 | Vohra 0.15–0.25 good, 0.4 great; Chen 0.2–0.3 typical | **matches** | medium |
| Incentivized **0.1–0.3** | **Extole, 400 referral programs: k ≈ 0.05** | **diverges (optimistic)** — the only direct measurement of a referral program's k sits at half the pack's floor | medium |
| Content-as-distribution 0.3–0.8 | None. No publisher measures k for share-the-output loops separately | **construct** | low |
| None 0.0–0.05 | Adjust: 70% of apps have no measurable k-factor | **matches** | medium |

### 5.2 Platform Advantage Rubric (ASO)

| Pack figure | Best source found | Match verdict | Confidence |
|---|---|---|---|
| Five-factor 3-tier rubric, 5–15 points, bands 12–15 high / 8–11 medium / 5–7 low | None. Scoring frameworks are not published benchmarks | **construct** | low |
| Premise that ASO is the highest-leverage free channel | **Supported.** AppFollow citing Apple Ads (2026-06-19): ~65% of App Store downloads follow a search, >70% of visitors use search; Sensor Tower puts search at ~59% of downloads | **matches (premise only)** | high |
| Thresholds inside the rubric ("top 10 achievable with <500 ratings", "top results < 4.2 stars, < 1K ratings", "incumbents with 100K+ ratings") | None. Adjacent sourced fact: Applyra's 460,000-keyword scan (https://www.applyra.io/blog/state-of-aso-2026, 2026-07-03) finds only **6.8% of App Store keywords and 2.3% of Google Play keywords are both winnable (difficulty <40) and carry real traffic**; median difficulty 36 iOS vs 47 Google Play | **construct**, though Applyra's finding supports the pack's general "keyword opportunity is scarce" posture | low |
| Featured-potential checklist (5 criteria, 3+ needed) | None. Reflects Apple editorial practice as described by practitioners; not a published rule | **construct** | low |

### 5.3 Advocacy Channel Rubric (Creator Economy Fit)

| Pack figure | Best source found | Match verdict | Confidence |
|---|---|---|---|
| Five-factor High/Medium/Low rubric; high fit = 3+ High | None | **construct** | low |
| Affiliate viability threshold "$5+/mo or $20+ one-time" | None. Consistent with RevenueCat's median monthly $6.68 / annual $29.99, so the threshold sits at roughly the market median | **construct (anchored)** | low |

### 5.4 Paid Budget Tiers and Verdict Logic

| Pack figure | Best source found | Match verdict | Confidence |
|---|---|---|---|
| Lean tier "can work if CPI < $2 and LTV > $6" | CPI < $2 is below every Tier-1 published CPI range (Business of Apps North America $2.50–5.00; EMEA $2.00–4.00). It is reachable in LATAM ($0.50–2.00) and Tier-2/3 markets | **diverges in practice** — the stated condition is essentially unattainable in Western markets on paid social, which arguably is the pack's point, but it is not sourced as such | medium |
| Moderate tier "viable if LTV:CAC > 3:1" | The 3:1 rule is SaaS folklore (David Skok / For Entrepreneurs), not a consumer-app measurement | **construct (anchored)** | low |
| Raw verdict thresholds (k ≥ 0.5 strong, k ≥ 0.2 moderate) | Chen: >0.5 is where a viral loop becomes perceptible; Vohra: 0.15–0.25 good | **matches (anchored)** — the two cut points land on the two most-cited practitioner thresholds | medium |
| Founder-tier adjustment (beginner downgrade, growth upgrade) | None | **construct** | low |

---

## Does not exist publicly (negative-result log)

Every figure below was searched for and no public source states it. These are constructs and should
be labelled as such in the packs. Ordered by how load-bearing they are.

1. **A subscription-app D30 retention benchmark, openly published** — the figure that would justify
   the packs' elevated D30 column across `retention.md` and `cac.md`. The AppsFlyer subscription
   report (2026-03-26) and the Adjust Mobile App Trends 2026 ebook both exist and are dated, but
   both are gated, and AppsFlyer's own contents list does not advertise a retention curve. The
   widely-repeated "14% vs 5.4%" pair traces only to AI-generated aggregators with no page
   reference. **Unverifiable without downloading the gated reports** — that is the single highest-
   value follow-up available on this whole pass, because it decides whether two packs get a scope
   note or a numeric correction.
2. **SOM capture rates by app category** (`market-sizing.md`) — year-1 0.01–2.0% and year-3
   0.1–5.0% of SAM across ten categories. Confirms the sibling b2b pass: indie capture rates do not
   exist publicly anywhere. Nothing close was found.
3. **Community-size platform multipliers** (`market-sizing.md`) — Reddit 20–50×, TikTok hashtag
   creators 100–500×, App Store reviews 50–100×, newsletter 10–30×. The 90-9-1 participation
   inequality rule (Nielsen, NN/g, 2006) supports the *shape* but no publisher converts a community
   size into an interested population. The App Store row additionally conflates rating rate
   (0.5–2%) with review rate (0.05–0.2%), which would imply a 500–2,000× multiplier.
4. **Search-intent conversion benchmarks** (`market-sizing.md`) — 8–15% / 3–8% / 5–12% / 1–3% by
   query type. Nobody measures web-search-volume to app-install. App Store search CVR (8–12% "good")
   is a different funnel with a different denominator.
5. **Organic channel CAC ranges** (`cac.md`) — ASO organic $0.50–3.00, content/SEO $1–8, TikTok
   organic $0.50–5, Reddit/community $0.50–4, influencer $2–25, word of mouth $0–2, press/Product
   Hunt $0–5. Organic acquisition has no published per-install price. Six of nine channels in the
   pack's CAC table are unsourceable.
6. **D30 → average lifespan mapping** (`cac.md`) — ≥25% → 12–18 months and the three bands below it.
   Derivable from a churn model, but no publisher states the mapping and the pack states no model.
7. **Demand-driver premium multipliers** (`pricing.md`) — survival 1.3–1.8×, status 1.5–2.0×,
   belonging 1.0–1.3×, control 1.2–1.5×, curiosity 0.8–1.2×, plus the +10% secondary-driver bonus.
   No source relates a psychological driver to a pricing multiplier.
8. **Per-category freemium conversion split** (`pricing.md`) — the eight-row typical/top-quartile
   table. The overall *level* is well sourced (OpenView 3–5% good, ChartMogul 8% all-product median,
   RevenueCat freemium D35 2.1%); the per-category differentiation is invented.
9. **Per-category annual-discount sweet spots** (`pricing.md`) — the 30–60% column. The aggregate
   discount norm *is* published (67% average, RevenueCat via Airbridge) and it contradicts the pack.
10. **Sub-category WTP rows** (`pricing.md`) — nutrition/diet, meditation, habit tracking, finance,
   creative tools, dating, parenting, utility, AI, and every one-time-purchase figure. Only Health &
   Fitness, Education and (via Business as proxy) Productivity have a published category median.
11. **Non-subscription price points** (`pricing.md`) — one-time $3–10, consumable packs $1–5,
    freemium+consumable packs $2–10, lifetime deal = 3–5× annual capped at $60, tip jar $1–5.
12. **B2B2C price = 3–5× the consumer price per seat** (`pricing.md`).
13. **Retention verdict thresholds** (`retention.md`) — sticky ≥ 15% D30, disposable < 8% D30. Note
    the "disposable" floor sits above the published global D30 median (5–7%).
14. **Demand-driver retention shift** (`retention.md`) — ±2 percentage points on D30 for
    survival/control vs curiosity.
15. **Stickiness factor anchors and churn-risk factor library** (`retention.md`) — qualitative
    frameworks with no published counterpart. Low sourcing burden since they make no numeric claim.
16. **Indie budget tiers** (`cac.md`) and **paid budget tiers** (`distribution.md`) — definitional
    schemes, no measurement behind the boundaries.
17. **ASO rubric, featured-potential checklist, creator-economy rubric, verdict logic, tier
    adjustment** (`distribution.md`) — scoring frameworks. The ASO rubric's *premise* (search drives
    the majority of App Store downloads) is well sourced; its internal thresholds are not.
18. **Content-as-distribution k-factor 0.3–0.8** (`distribution.md`) — the one loop type with no
    published measurement; the other five rows have at least one.
19. **TAM inflation and SAM breadth reality checks** (`market-sizing.md`) — >$10B TAM, >50% SAM.
    Heuristics, not measurements. (The third check, the $500K SOM fantasy threshold, *is* well
    corroborated and belongs in the sourced column.)
20. **SOM verdict bands** (`market-sizing.md`) — $200K / $50K / $10K cut points. No published band
    scheme; cross-checking against RevenueCat and Adapty revenue distributions shows "medium"
    ($50–200K/yr) is roughly a top-10% outcome and "large" (>$200K) is beyond the top 5%.

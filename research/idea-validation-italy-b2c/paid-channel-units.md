# Italy: Paid-Channel Cost Units for Consumer App Campaigns

Research date: 2026-08-13. Scope: indie founder acquiring **consumers** in Italy for a mobile app or
consumer web product. Sibling to `idea-validation-italy-b2b/channels-legal.md`, which covers the same
question for B2B micro-SaaS.

## How to read this report

**Confidence convention.**

- `high` — platform-published, or a dated study over a large disclosed sample.
- `medium-high` — a vendor benchmark from a self-selected sample, but with a disclosed methodology and
  an internally consistent cross-country comparison. Used in this report for exactly one source
  (MobileAction, §5). It sits above `medium` because the comparison is same-dataset and same-window,
  and below `high` because the sample is the vendor's own customer accounts.
- `medium` — reputable agency or vendor benchmark with a disclosed dataset and stated methodology.
- `low` — planning range, small sample, undated, or self-declared as adapted from another market.

**A fourth category exists and it is not a confidence tier: `NOT REPORTED`.** During this pass, a
large share of the "Italy 2026 benchmark" pages returned by search proved to be an AI-content citation
ring rather than independent sources. The evidence is direct: `$9.16` in-feed CPM and `$1.02`
cross-industry CPC appear verbatim on digitalapplied.com, tikadsuite.com and mbadv.agency, and
mbadv.agency's own footer names its inputs as DigitalApplied, TikAdSuite, Stackmatix, Benly, Lebesgue,
Koro, WebFX and Triple Whale. The same trap exists on the Meta side: oto.agency's "€10.29 CPM, CPC
€0.30–0.90 for Italy" explicitly credits Superads, so oto.agency is not independent corroboration of
Superads — it is Superads counted twice.

Accordingly: **a figure that appears only on content-mill sites and traces to no disclosed dataset is
not reported as a benchmark at any confidence tier.** It goes in the negative-result log in §8 as
"figures circulate but trace to no primary". This is the mechanism the sibling repo's negative-log
convention exists for, and stretching `low` to cover such figures would defeat it.

**Currency is per-figure and never mixed.** Sources report the same quantity in different currencies
and they do not reconcile: Superads gives Italy Meta CPM as **€10.48**, while adamigo.ai gives it as
**$7.20**. Every table below carries a currency column, and no range in this report is built by
averaging across units. Where a USD/EUR conversion is shown it is at ~1.15 USD/EUR and marked as
derived.

**Staleness.** `[STALE-DATA]` marks a measurement whose underlying data is more than 12 months old.

**One warning before the tables.** Only two channels below have a genuine Italy-specific measurement
from a disclosed dataset: Meta (Superads) and Apple Search Ads (MobileAction). Everything else is
either a planning range or an explicitly-labelled global comparator. That is the honest state of the
public record, not a gap in the search.

---

## 1. Headline: what an Italian consumer-app plan can actually be built on

| Channel | Italy-specific unit available? | Best figure | Confidence |
| --- | --- | --- | --- |
| Apple Search Ads | **Yes** | CPA **$1.60**, CPT **$0.87** (2025 full year) | medium-high |
| Meta (Facebook/Instagram) | **Yes** | CPM median **€10.48**; CPC median **~0.50** (currency unresolved) | medium |
| Google Ads search | No — planning ranges only | €0.75–2.86 for consumer verticals | low |
| Google App Campaigns | **No Italy cut exists** | global Android median CPI $1.22 | low (global base) |
| TikTok | **No traceable Italy cut exists** | — | `NOT REPORTED` |
| Cross-channel CPI | **No Italy cut exists** | EMEA blended $1.03 | low (EMEA base) |

**The single most useful number in this report is the Apple Search Ads Italy-vs-US comparison**,
because it is the only Italy-vs-US multiplier in the public record that comes from one dataset,
one methodology and one time window: Italy CPA `$1.60` against US CPA `$3.85` is **Italy at ~0.42× the
US**. See §6.

---

## 2. Meta (Facebook / Instagram), Italy

### 2.1 The one Italy-specific dataset

Superads publishes a country cut of Meta ad costs from a disclosed dataset: "over $3B in Facebook ad
spend, collected across thousands of ad accounts that use Superads daily". The sample is self-selected
(it is their own customer base), but it is disclosed, large, and reports medians rather than means with
a stated reason for doing so. That is enough for `medium`, not for `high`.

**These are all-industries figures, not consumer-specific.** Superads does not publish a
consumer-versus-B2B split for Italy. Treat them as a market-wide baseline that a consumer campaign
sits somewhere inside, not as a consumer benchmark.

| Figure | Value | Currency | Geographic base | Source, window | Confidence |
| --- | --- | --- | --- | --- | --- |
| Italy median CPC, all industries | avg **~0.50** over the window; range 0.37 (Jul 2025) – 0.59 (Nov 2025) | **unresolved** — see §2.2 | Italy | Superads, Jul 2025 – Jul 2026 | medium |
| Global median CPC, same window | ~1.05; range 0.77 – 1.29 | unresolved | Global | Superads, Jul 2025 – Jul 2026 | medium |
| **Italy vs global CPC gap** | **~52% below global**, ranging 28% to 59% below | ratio, unit-free | Italy vs global | Superads | medium |
| Italy median CPM, all industries | avg **€10.48**; low €6.88 (Apr 2026), high €15.60 (Oct 2025) | **EUR** | Italy | Superads, Jun 2025 – Jun 2026 | medium |
| Global median CPM, same window | €20.68; low €18.83, high €24.21 (Nov 2025) | EUR | Global | Superads | medium |
| **Italy vs global CPM gap** | **~49% below global**; narrowest ~20% (Sep 2025), widest ~71% (Apr 2026) | ratio | Italy vs global | Superads | medium |
| Italy CPM month-to-month volatility | ±€2.08 average absolute monthly change, vs ±€1.56 global | EUR | Italy | Superads | medium |

Source: Superads, *Facebook Ads CPC Benchmarks in Italy*,
https://www.superads.ai/facebook-ads-costs/cpc-cost-per-click/italy and *Facebook Ads CPM Benchmarks
in Italy*, https://www.superads.ai/facebook-ads-costs/cpm-cost-per-mille/italy — both pages carry a
"(2025)" title stamp but describe rolling windows ending Jun–Jul 2026. Not stale.

### 2.2 The currency ambiguity, and why it matters for the packs

The Superads Italy **CPM** page states its figures in euro explicitly (`€7.79`, `€10.48`, `€20.68`).
The Superads Italy **CPC** page states its figures with **no currency symbol at all** (`0.50`, `1.05`).

The sibling B2B report read the CPC page as USD and converted it to **€0.43**. That conversion is not
verifiable from the page. The more likely reading, given that the CPM page on the same site for the
same country is euro-denominated, is that the CPC page is also euro and no conversion is needed — which
would put Italy median CPC at **€0.50, not €0.43**. The difference is ~16% and it propagates into any
CAC model built on it.

**Recommendation for the packs: carry the ratio, not the level.** The `~52% below global` figure is
currency-independent and is the defensible quantification. If a euro level is required, state it as
**€0.43–€0.50 with the currency basis flagged as unresolved**, rather than picking one.

### 2.3 The double-count warning for the orchestrator

The task brief describes the B2B pass as having found "Meta ~€0.43 CPC" and asks for a consumer
equivalent. **These are not two observations.** The sibling's €0.43 is derived from exactly the
Superads Italy all-industries median reproduced above — the same page, the same window, the same
number. It was never a B2B-specific figure.

Two consequences. First, the README synthesis must not present a B2C Meta CPC and the B2B €0.43 as
mutually corroborating; they are one measurement. Second, because the underlying figure is
all-industries rather than B2B, it is arguably **more** applicable to the consumer case than to the
B2B one it was originally used for.

### 2.4 Cost-per-install on Meta for Italy

**Not published.** Superads does not publish an Italy app-install cut, and no other source located
gives a Meta CPI for the Italian market. See §8.

### 2.5 Seasonality — the one qualitative finding worth carrying

Superads' Italy CPM series shows a clear and large annual shape: summer softness (~€7.5–8.7,
Jun–Aug), a sharp autumn lift peaking at €15.4–15.6 in Sep–Oct, elevated levels through Nov–Dec
(~€13.6–13.7), a Q1 fallback and an April trough at €6.88. **Peak-to-trough is 2.3×.** A founder
planning an Italian launch budget on an annual average will underfund an autumn launch by more than
half. Confidence: medium (same Superads dataset).

---

## 3. TikTok Ads, Italy

**`NOT REPORTED`. No Italy-specific TikTok cost benchmark from a disclosed dataset was located.**

This is the clearest instance of the citation-ring problem in this pass. Italy TikTok CPM figures do
circulate — potastudio.com gives "€3–10 In-Feed", it.socialmediaagency.one gives "€3–8" — but neither
discloses a dataset, a sample size, or a window, and the numbers they carry are the same figures that
propagate across the mill network described in the convention block. They are not reported here at any
tier. See §8.

The one genuinely primary TikTok fact available, and it is a budget floor rather than a cost unit:

| Figure | Value | Currency | Geographic base | Source, date | Confidence |
| --- | --- | --- | --- | --- | --- |
| Recommended daily ad-group budget | **$30** for North America **and EMEA** ($20 APAC) | USD | EMEA (includes Italy) | TikTok for Business, https://ads.tiktok.com/business/en, undated page | high (platform-published) |

Note what this does and does not say: TikTok groups Italy into EMEA and prices its guidance the same
as North America. That is a platform statement about recommended budget, **not** evidence that Italian
TikTok inventory costs the same as US inventory.

**Ring-3 global comparators only**, offered strictly as an order-of-magnitude sanity check and not as
Italian units:

| Figure | Value | Currency | Geographic base | Source, date | Confidence |
| --- | --- | --- | --- | --- | --- |
| TikTok CPC, all objectives, median | $0.62 (IQR $0.38–$1.04) | USD | Global, sample 54% US / 16% UK / 12% AU / 8% CA, **EU is part of "the rest"** | AdLiftr, 2026-05-30, 3,127 campaigns / 548 advertisers / $18.7M spend, Feb–May 2026 | low for Italy (geographic base is overwhelmingly non-EU) |
| TikTok CPM, App Installs objective | $12.40 (IQR $7.40–$19.40) | USD | same as above | AdLiftr, 2026-05-30 | low for Italy |
| TikTok CPI, mobile apps (utility) | $4.40 (IQR $2.10–$9.20) | USD | same as above | AdLiftr, 2026-05-30 | low for Italy |
| TikTok CPC range | $0.30–$1.50; CPM $4–$10 | USD | Global | WordStream, 2026-04-16 | low for Italy (no geographic cut) |

AdLiftr is the only TikTok source in this pass that discloses sample size, spend, window and geographic
mix, which is why it is cited while the mill figures are not. Its geographic mix is the reason it
cannot be used for Italy: EU campaigns are a residual slice after US, UK, Australia and Canada.

---

## 4. Google Ads, Italy — consumer-intent search

**No Italy-cut Google Ads study with disclosed methodology exists.** This finding is identical to the
sibling B2B pass and was re-verified independently here. Google publishes no country CPC benchmarks;
WordStream's annual study is explicitly US-only; every Italian CPC table located is either an agency's
undisclosed internal account sample or openly self-describes as US benchmarks adapted to Italy.

Two of the sources are explicit about which they are, and the distinction is worth preserving:

- **luigivirginio.com** states its figures are *"non benchmark americani riadattati: sono stime basate
  sulla gestione diretta di campagne Google Ads in Italia su decine di account"* — first-party Italian
  account data, sample size undisclosed.
- **migliore-agenzia.com** states its figures are *"drawn from international benchmarks adapted to the
  Italian market"* — self-declared as **not** Italian data. Its numbers are not independent evidence
  about Italy.

Consumer verticals relevant to a consumer app, all `low` confidence, all planning ranges:

| Vertical | CPC range | Currency | Source, date |
| --- | --- | --- | --- |
| Education / formazione e corsi | €0.90 – €6.00 | EUR | luigivirginio.com, 2026-05-04 |
| Fitness & gyms | €0.75 – €2.20 | EUR | datalatte.pro, 2026-06-13 |
| Health & wellness | €1.20 – €3.50 | EUR | migliore-agenzia.com, 2026-04-07 (self-declared US-derived) |
| Health / medical & dental | €1.20 – €6.00 | EUR | luigivirginio.com, 2026-05-04 |
| Finance & insurance | €3.00 – €15.00+ | EUR | luigivirginio.com, 2026-05-04 |
| Beauty / estetica | €0.50 – €1.50 | EUR | luigivirginio.com, 2026-05-04 |
| Travel & tourism | €0.50 – €3.00 | EUR | luigivirginio.com, 2026-05-04 |
| E-commerce fashion & home | €0.20 – €1.00 | EUR | luigivirginio.com, 2026-05-04 |
| All-sector search average | €0.30 – €2.50 | EUR | luigivirginio.com, 2026-05-04 |

Sources with undated content on stale-dated pages (insiderslab.it), and pages publishing *Italian* CPCs
in **US dollars** (adpredictor.ai: `$0.94–$2.86` Education, `$0.47–$1.56` Ecommerce — a strong
indicator of a US table with a conversion applied), are excluded rather than added as extra rows. See
§9.

**What can honestly be said:** across three Italian sources that do not obviously copy each other, a
consumer-facing (non-finance, non-legal) Italian search CPC lands somewhere in **€0.50–€3.00**, with
education and health running toward the top of that band and e-commerce toward the bottom. The
direction is consistent; the magnitude is not measurable from public sources. Use it as a planning
range and say so.

**Geographic premium inside Italy: weaker evidence than the sibling B2B report implies.** The sibling
`channels-legal.md` records a Milan/Turin premium of +20–50% and notes that "two independent sources
agree on direction and rough size". One of those two is adpredictor.ai, excluded here on the currency
red flag above. What remains is migliore-agenzia.com's 30–50%, from a page that **self-declares its
figures as US benchmarks adapted to Italy**. On this pass's evidence rules there is therefore **no
usable Italian source for the northern-city premium at all** — the direction is plausible and
commercially unsurprising, but it is not measured. Treat any Milan/Rome multiplier in the consumer pack
as an untested assumption.

### 4.1 Google App Campaigns (UAC) — no Italy or Europe cut

**No published Google App Campaigns CPI for Italy exists**, and no Europe-level cut was located either.
Global comparators only:

| Figure | Value | Currency | Geographic base | Source, date | Confidence |
| --- | --- | --- | --- | --- | --- |
| Median CPI, all verticals, Android | $1.22 | USD | **Global** | Singular ROI Index 2025, via RocketShip HQ 2026-04-07 | low (global base; secondary citation of Singular) |
| Android CPI, Health & Fitness | $1.55 global / $2.90 US | USD | Global and US | RocketShip HQ, 2026-04-07 | low |
| Android CPI, Utilities / Productivity | $0.90 global / $1.75 US | USD | Global and US | RocketShip HQ, 2026-04-07 | low |
| Android CPI, Fintech / Banking | $2.80 global / $4.80 US | USD | Global and US | RocketShip HQ, 2026-04-07 | low |
| Google Ads app-install CPI range | $1.50 – $4.50 | USD | Global | Business of Apps via Mistplay, 2026-05-29 | low |
| iOS eCPI, **France** 2025–26 | $3.80 – $7.20 by vertical | USD | France | steerads.com, 2025-11-17, "accounts observed in public benchmarks" | low |
| Android eCPI, **France** 2025–26 | $1.40 – $3.60 by vertical | USD | France | steerads.com, 2025-11-17 | low |

The French figures are included only because France is the nearest large Latin-Europe market with any
published App Campaigns cut at all; they are **not** an Italy proxy and the source does not disclose a
sample. The most transferable fact in this block is structural rather than numeric: iOS eCPI runs
**2–3× Android eCPI** post-ATT, because SKAdNetwork caps bidding precision.

---

## 5. Apple Search Ads, Italy — the best-evidenced channel in this report

MobileAction's *2026 Apple Ads benchmark report* (covering full-year 2025 data, gathered via
MobileAction and SearchAds.com tools) publishes a country-level cut with a stated sampling method:
countries are ranked by impressions and by spend, and the top 15 by spend are used for the CPT and CPA
rankings. Italy is in that top 15. This is the only channel in this pass with a real Italy number
sitting inside a real cross-country comparison.

| Figure | Value | Currency | Geographic base | Confidence |
| --- | --- | --- | --- | --- |
| **Italy CPT, search results ads, 2025** | **$0.87** — second-lowest of the tracked markets, after Turkey ($0.85) | USD | Italy | medium-high |
| **Italy CPA, search results ads, 2025** | **$1.60** — the **lowest CPA of all tracked markets** | USD | Italy | medium-high |
| Great Britain CPT / CPA | $2.60 / $4.53 — highest-cost market on both | USD | GB | medium-high |
| United States CPA | $3.85 — second-highest | USD | US | medium-high |
| Spain CPA | $2.71 (down from $3.87 in 2024) | USD | Spain | medium-high |
| France CPA | $1.94 | USD | France | medium-high |
| Poland CPA | $1.92 | USD | Poland | medium-high |
| Cross-region average CPA | $2.83 (2025), down from $3.03 (2024) | USD | 15-country aggregate | medium-high |
| Global CPT by quarter, 2025 | Q1 $1.30 → Q2 $1.26 → Q3 $1.50 → **Q4 $1.88** | USD | Global | medium-high |
| Global CPA, search results ads | $2.51 (2025), from $2.76 (2024) | USD | Global | medium-high |
| Global tap-through rate | 8.08% (2025), from 9.07% (2024) | — | Global | medium-high |
| Global tap-to-install conversion rate | 65.82% (2025), from 66.70% (2024) | — | Global | medium-high |
| Search **tab** ads (not search results) | $0.95 CPT, $1.81 CPA, 1.25% TTR, 54.58% CR | USD | Global | medium-high |

Source: MobileAction, *2026 Apple Ads benchmark report*,
https://www.mobileaction.co/report/apple-ads-2026-benchmark-report/ — executive summary, regional CPA
and CPT sections. Data covers calendar 2025; the report is a 2026 publication. Not stale, though the
underlying window closed in Dec 2025.

Why this is only `medium-high` and not `high`: MobileAction is a vendor publishing from its own and
SearchAds.com's customer accounts, which is a self-selected sample in the same way Superads is. The
methodology is disclosed and the cross-country comparison is internally consistent, which is why it
rates above everything else here.

**The `medium-high` tier already prices in the single-vendor risk.** Negative-log item 8 records that
the natural independent cross-check (SplitMetrics' competing 91-market report) is gated and was not
retrieved, so these Italy figures are uncorroborated. That is not a contradiction of the tier — it is
one of the two reasons the tier is not `high`, the other being the self-selected sample. Read together:
the methodology is good enough to trust the *comparison* between Italy and other markets, because every
market in it is measured the same way; a second vendor would be needed to trust the *absolute levels*.

**Apple's own published benchmarks: none.** Apple does not publish CPT or CPA figures for the Italian
storefront or any other. Every Apple Search Ads benchmark in circulation is third-party. SplitMetrics
publishes a competing *Apple Ads Search Results Benchmarks Report 2026* covering 22 categories and 91
markets, but it is gated behind a lead form and was not retrieved; see §8.

---

## 6. How Italian consumer acquisition costs compare to US costs

This is question 6 of the brief and it has a better answer than expected, because Apple Search Ads
supplies a same-dataset, same-window, same-methodology comparison.

| Comparison | Multiplier | Basis | Confidence |
| --- | --- | --- | --- |
| **Apple Search Ads CPA: Italy vs US** | **$1.60 / $3.85 = 0.42×** | One dataset, one window (2025), one methodology | **medium-high** — the strongest Italy-vs-US figure in this report |
| Apple Search Ads CPT: Italy vs GB | $0.87 / $2.60 = 0.33× | Same dataset, but **a different comparison base than the CPA row above** — the US CPT was not published in the retrieved sections, so GB stands in for it. GB is the most expensive market on both metrics, so this ratio is not interchangeable with the Italy-vs-US CPA ratio and should not be averaged with it | medium-high |
| Apple Search Ads CPA: Italy vs 15-country average | $1.60 / $2.83 = 0.57× | Same dataset | medium-high |
| Meta CPC: Italy vs **global** | ~0.48× (i.e. ~52% below) | Superads, Jul 2025–Jul 2026. **Base is global, not US** | medium |
| Meta CPM: Italy vs **global** | ~0.51× (i.e. ~49% below) | Superads, Jun 2025–Jun 2026. **Base is global, not US** | medium |
| Google Ads CPC: Italy vs US | 25% below US | WordStream country page — **article published 2015-07-02**, methodology a one-off Keyword Planner run on ~15,000 English-language keywords | **low** `[STALE-DATA]` — an eleven-year-old estimate behind a 2025 "last updated" stamp. Do not quote as a 2026 figure. |

**Two similar-looking third-party figures, excluded.** ad-stack.ai (2026-05-15) puts "Tier-2 Europe
(ES, IT, PL)" at 0.4–0.6× Tier-1 English markets, and linkrunner.io (undated) puts "Southern/Eastern
Europe" at ~0.35× US. Both land near the Apple-derived 0.42×, and it is tempting to read that as
convergence. **It is not, and neither figure is used in this report.** Both are on the excluded-source
list in §9, neither discloses a dataset, and regional tier tables of exactly this shape are among the
most-recycled artifacts in the content-mill network — so "Southern Europe ≈ 0.35–0.6× US" is most
likely one lineage reproduced twice, not two independent estimates. They are named here only so the
orchestrator recognises and rejects them if they resurface. **They add nothing to the confidence of the
0.42×, which stands on the MobileAction data alone.**

**Working conclusion for the packs.** The defensible statement is narrower than a cross-channel rule:
**on Apple Search Ads, Italian cost per acquisition runs at ~0.42× the US**, from a single-dataset
2025 comparison. Extending that to "Italian consumer acquisition costs run at roughly 0.4–0.5× US
levels" across channels is a **planning assumption, not a measurement** — it rests on one channel,
and the Meta figure that points the same way is Italy-vs-global rather than Italy-vs-US, so the two are
not measuring the same comparison and do not compose into a range. Label it as an assumption wherever
it appears downstream.

**The trap this multiplier sets.** Cheap acquisition is only half the equation, and the Italian
discount on the revenue side is at least as large. Meta's own Q2 2026 results are the primary evidence:

| Figure | Value | Geographic base | Source, date | Confidence |
| --- | --- | --- | --- | --- |
| Advertising revenue, US & Canada | $26.34bn (+31.4% YoY) | US & Canada | Meta Q2 2026 results via Zacks, 2026-07-30 | high |
| Advertising revenue, Europe | $14.09bn (+23.9% YoY) | **Europe as one segment** — not Italy | same | high |
| Average price per ad, global | +12% YoY | Global | Meta press release, 2026-07-29 | high |
| Average price per ad, US & Canada | +20% YoY | US & Canada | Meta Q2 2026 earnings call via ppc.land, 2026-07-30 | high |
| Average price per ad, Asia-Pacific | +1% YoY | APAC | same | high |

Read this as directional only. Meta reports Europe as a single segment, so the base is EU and not
Italy; and segment revenue conflates ad load, price and user count, so it is not a CPM multiplier.
What it does establish, from a primary dated source, is that **US ad prices are pulling away from the
rest of the world** (+20% against +12% globally). A founder modelling Italy off a US benchmark with a
fixed discount will see that discount widen over time, in both directions: cheaper clicks, but also
lower revenue per user.

---

## 7. Cross-channel CPI meta-benchmarks

**No CPI benchmark with an Italy cut was located from any MMP or industry aggregator.** The structural
reason is documented in AppsFlyer's own methodology and is worth stating precisely, because it is a
finding rather than a search failure.

AppsFlyer groups Italy into a **Western Europe** sub-region alongside the UK, Germany, France, the
Netherlands, Spain, Switzerland, Sweden, Belgium, Ireland, Austria, Denmark, Norway, Israel, Portugal,
Greece and Finland. Their published rule: *"when data is sufficient at the sub-region level (but not
country level), the country will appear in the dropdown, but the results shown will reflect the
sub-region, clearly labeled as such. If thresholds aren't met even at the sub-region level, the country
will not appear in the dropdown at all."* Independently, EMARKETER's index of AppsFlyer KPI coverage
lists the countries sliced for cost-per-install as **Australia, Brazil, Mexico, South Korea, UK and
US** — Italy absent. Source: https://www.appsflyer.com/benchmarks/faq/ (undated) and
https://www.emarketer.com/data-metrics/mobile-and-app/ (2023-07-28) `[STALE-DATA]` for the EMARKETER
row.

So: any "Italy CPI" a founder encounters is either a Western Europe roll-up relabelled, or invented.

**Ring-3 global and regional comparators.** Each row states its geographic base. None is an Italian
figure.

| Figure | Value | Currency | Geographic base | Source, date | Confidence |
| --- | --- | --- | --- | --- | --- |
| Average CPI, **EMEA** | **$1.03** | USD | EMEA (Italy is inside this, undifferentiated) | Mistplay, 2026-05-29 | low (region far too coarse for Italy) |
| Average CPI, North America | $5.28 | USD | North America | Mistplay, 2026-05-29 | low |
| Average CPI, APAC | $0.93 | USD | APAC | Mistplay, 2026-05-29 | low |
| Average CPI, Latin America | $0.34 | USD | LATAM | Mistplay, 2026-05-29 | low |
| Average CPI, iOS | ~$4.70 | USD | Global | Mistplay, 2026-05-29 | low |
| Average CPI, Android | ~$3.40 | USD | Global | Mistplay, 2026-05-29 | low |
| CPI range, **Europe** | $1.66 – $4.75 | USD | Europe | appsfinboard.com, 2026-02-10 | low |
| CPI range, North America | $1.75 – $4.13 | USD | North America | appsfinboard.com, 2026-02-10 | low |
| Average CPI, iOS / Android | $2.52 / $1.29 | USD | Global | appsfinboard.com, 2026-02-10 | low |

**These sources contradict each other and the contradiction is itself the finding.** Mistplay puts
global iOS CPI at ~$4.70 and Android at ~$3.40; appsfinboard puts the same two at $2.52 and $1.29 —
roughly half. Both are dated 2026, both are presented as industry aggregates. A range that spans a 2×
disagreement between sources is not a benchmark; it is a reminder that blended global CPI is close to
meaningless without a stated geographic and vertical base. Do not build a CAC model on any single row
in this table.

### 7.1 One real Italy CPI observation, and why it is nearly unusable

| Figure | Value | Currency | Geographic base | Source, date | Confidence |
| --- | --- | --- | --- | --- | --- |
| Italy CPI, Moloco, May 2026 | $5.34 | USD | Italy | RentAcc, 2026-06-04 | low — **single vertical, see below** |
| Italy cost per registration | $12.27 | USD | Italy | same | low |
| Italy install-to-registration | 43.49% | — | Italy | same | low |
| Spain CPI, same month | $7.14 | USD | Spain | same | low |
| Poland CPI, same month | $5.17 | USD | Poland | same | low |
| Australia CPI, same month | $7.04 | USD | Australia | same | low |

This is a genuine Italy-specific, single-month, single-network measurement — and it is from
**real-money gaming**. The report's own metrics give it away: "CPD" is cost per *deposit*, "reg2dep" is
registration-to-deposit conversion, and the named apps are slot titles. Real-money gaming is among the
highest-LTV and most heavily contested app verticals there is, and its Italian advertising is subject
to a statutory regime no ordinary consumer app faces (not researched in this pass — flagged as a
question for the legal/channels report, not asserted here). **Do not generalise $5.34 to a consumer app
CPI for Italy.** It is included here only so that the orchestrator recognises it if it resurfaces, and
knows to reject it.

Note also the ordering it produces: Italy $5.34 sits *below* Spain $7.14 and Australia $7.04 but
*above* Poland $5.17, which is consistent in direction with Italy being a mid-to-low-cost Western
European market — the same direction as the Apple Search Ads finding.

---

## 8. Does not exist publicly (negative-result log)

Items searched for and not found, or found only in forms that must not be used. Nothing below should be
invented, estimated, or filled in with a global figure silently relabelled as Italian.

1. **Any Italy-specific TikTok Ads cost benchmark from a disclosed dataset.** Italy TikTok CPM and CPC
   figures circulate widely (potastudio.com "€3–10 CPM", it.socialmediaagency.one "€3–8 CPM",
   xyzlab.com country pages) but none discloses a sample, window, or source, and they trace back into
   the digitalapplied / tikadsuite / mbadv / Stackmatix citation ring rather than to any primary. The
   only primary TikTok fact for the region is the platform's own $30/day recommended ad-group budget
   for EMEA. **TikTok Italy cost units must be reported as unknown, not estimated.**

2. **Any Meta cost-per-install figure for Italy.** Superads publishes Italy CPC, CPM and CPL but not
   CPI. No other source gives a Meta CPI for the Italian market.

3. **Any Google App Campaigns CPI for Italy, or for Europe as a region.** Only global medians and a
   US cut exist. The nearest Latin-Europe figure is a French eCPI range from an undisclosed sample
   (steerads.com), which is not an Italy proxy.

4. **Any Italy-cut Google Ads benchmark with disclosed methodology.** Re-verified independently of the
   sibling B2B pass, same conclusion. Google publishes no country CPC data; WordStream's study is
   US-only; every Italian table is an undisclosed agency sample or self-declares as US-adapted. The
   consumer-vertical ranges in §4 are `low` for this reason and no other Italian Google figure in this
   report rises above `low`.

5. **A current measurement of Italy's Google Ads CPC discount versus the US.** The only country
   comparison located is WordStream's, whose underlying data is from 2015 despite a 2025 "last
   updated" stamp. `[STALE-DATA]`

6. **Any AppsFlyer, Adjust, Sensor Tower or Singular CPI benchmark broken out to Italy.** Confirmed
   structurally rather than by absence of search results: AppsFlyer's published methodology rolls Italy
   into a 17-country Western Europe sub-region and surfaces country-level data only above volume
   thresholds Italy does not meet, and EMARKETER's coverage index lists AppsFlyer's CPI country slices
   as AU/BR/MX/KR/UK/US with Italy absent.

7. **Apple's own Apple Search Ads benchmarks, for the Italian storefront or any other.** Apple
   publishes no CPT or CPA figures. Every Apple Search Ads benchmark in circulation, including the
   MobileAction figures this report relies on, is third-party vendor data.

8. **SplitMetrics' Apple Ads Search Results Benchmarks Report 2026**, which covers 91 markets and would
   be the natural independent cross-check on MobileAction's Italy CPT and CPA. It is gated behind a
   lead-capture form and was not retrieved. **The Italy Apple Search Ads figures in §5 therefore rest
   on a single vendor and are uncorroborated.**

9. **Business of Apps' "Mobile Acquisition Costs by Region" table.** The page exists and the section
   headings are visible, but the data is behind a member login. Not retrieved, not reported.

10. **Any consumer-versus-B2B split of the Superads Italy Meta figures.** The Italy CPC and CPM series
    are all-industries only. A consumer-specific Italian Meta CPC does not exist publicly.

11. **The currency basis of the Superads Italy CPC series.** The page carries no currency symbol. This
    is unresolved, not merely unstated by this report — and it means the sibling B2B pack's €0.43 rests
    on an unverified USD assumption. See §2.2.

12. **Any IAB Italia or Audiweb publication of Italian paid-channel cost units.** IAB Italia's monthly
    AdReport series was checked: it is advertiser-and-campaign-count intelligence (advertisers active,
    campaigns running, dominant creative formats, top brands by post volume) and contains **no CPM, CPC
    or CPI data at all**. The Italian industry body does not publish cost benchmarks.

13. **Cost-per-install for any Italian consumer app vertical (fitness, finance, education).** The
    vertical CPI tables that exist are all Tier-1-English or global. No source crosses vertical with
    Italy.

---

## 9. Sources

**Italy-specific, disclosed dataset (the load-bearing sources)**

- Superads, *Facebook Ads CPC Benchmarks in Italy*, window Jul 2025 – Jul 2026, $3B spend dataset.
  https://www.superads.ai/facebook-ads-costs/cpc-cost-per-click/italy
- Superads, *Facebook Ads CPM Benchmarks in Italy*, window Jun 2025 – Jun 2026, same dataset.
  https://www.superads.ai/facebook-ads-costs/cpm-cost-per-mille/italy
- MobileAction, *2026 Apple Ads benchmark report* (full-year 2025 data, MobileAction + SearchAds.com).
  https://www.mobileaction.co/report/apple-ads-2026-benchmark-report/ — executive summary, regional CPA
  and regional CPT sections.

**Primary / platform-published**

- Meta Platforms, *Meta Reports Second Quarter 2026 Results*, 2026-07-29.
  https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-Second-Quarter-2026-Results/default.aspx
- Meta Q2 2026 regional detail via Zacks, 2026-07-30, and ppc.land, 2026-07-30.
- TikTok for Business, ad cost FAQ, undated. https://ads.tiktok.com/business/en
- AppsFlyer, *App marketing benchmarks — FAQ and methodology*, undated.
  https://www.appsflyer.com/benchmarks/faq/

**Agency / vendor, used with stated caveats**

- AdLiftr, *TikTok Ads Cost 2026*, 2026-05-30 (3,127 campaigns, $18.7M, geographic mix disclosed).
  https://adliftr.com/blog/tiktok-ads-cost-benchmarks-2026
- Mistplay, *How much does mobile user acquisition cost in 2026?*, 2026-05-29.
  https://business.mistplay.com/resources/user-acquisition-cost
- RocketShip HQ, *Google App Campaigns (UAC) complete guide*, 2026-04-07 (cites Singular ROI Index
  2025). https://www.rocketshiphq.com/google-app-campaigns-uac-complete-guide/
- RentAcc, *Moloco Ads May 2026 Performance Review*, 2026-06-04 — real-money gaming vertical.
  https://rentacc.agency/blog/may26_moloco
- Apps Finboard, *The True Cost of User Acquisition*, 2026-02-10.
  https://appsfinboard.com/blog/true-cost-of-user-acquisition-app-install/
- Luigi Virginio, *Quanto costa Google Ads nel 2026?*, 2026-05-04 (self-declared first-party Italian
  accounts). https://luigivirginio.com/quanto-costa-google-ads-guida-ai-costi/
- DataLatte, *Local Marketing in Italy*, 2026-06-13. https://datalatte.pro/blog/local-marketing-italy-small-business-2026
- Migliore Agenzia, 2026-04-07 (**self-declares as US benchmarks adapted to Italy**).
  https://www.migliore-agenzia.com/en/blog/how-much-does-google-ads-cost-agency-guide-2026
- WordStream, *How Much Do TikTok Ads Cost in 2026?*, 2026-04-16.
  https://www.wordstream.com/blog/tiktok-ads-cost
- WordStream, *Average Cost per Click by Country*, published **2015-07-02**. `[STALE-DATA]`
  https://www.wordstream.com/blog/average-cost-per-click
- IAB Italia, AdReport monthly series (checked, contains no cost data). https://iab.it/

**Consulted and deliberately not cited as evidence** — content-mill pages whose figures trace to no
disclosed dataset, listed so the orchestrator recognises them if they resurface: digitalapplied.com,
tikadsuite.com, mbadv.agency, adamigo.ai, adligator.com, adlibrary.com, xyzlab.com, oto.agency,
potastudio.com, it.socialmediaagency.one, ad-stack.ai, semnexus.com, linkrunner.io, adpredictor.ai,
insiderslab.it.

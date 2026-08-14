# Market sizing — B2C calibration (Italy-first rings)

Loaded by `iv-market-sizer` via the CALIBRATION path in its dispatch prompt.
Defines the ring reporting rule, population anchors, estimation proxies,
platform filters, and capture rates for the B2C target. The triangulation
mechanism, SAM filter logic, reality checks, and verdict thresholds live in
the agent brief.

> **Bias warning (apply throughout):** every published indie-revenue source
> skews upward (survivor selection). Estimate conservatively and say so.
> Figures below carry source + date + confidence, or are marked
> **construct** — a calibration value with no public source. Never present
> a construct as a market fact, and never invent a figure the research
> logged as publicly nonexistent (indie capture rates, community-multiplier
> conversions, Italian per-category WTP).

## Step 0 — Ring reporting (mandatory, before any sizing)

B2C sizing is computed and reported **per ring, Italy first**, never as one
blended number:

| Ring | Market | Currency |
|---|---|---|
| **Ring 1 — Italy** | Italian-language consumer market | EUR |
| **Ring 2 — Europe-English** | EU consumers reachable with an English-language app | EUR |
| **Ring 3 — Western** | NA, UK/IE, AU/NZ | USD |

- SAM and SOM are reported per ring, each in its ring currency, in the
  artifact's structured `rings` array (Italy first; n/a rings keep their
  entry with nulls and a reason). Never mix currencies inside one table
  row.
- Ring 2 is the least instrumented ring (few EU-EN data cuts exist): derive
  it conservatively and mark it `confidence: low`.
- If the idea is Italy-bound by nature (Italian-language content, Italian
  regulation or institutions), Rings 2–3 may be `n/a` — say so rather than
  padding the estimate.
- Eastern markets are out of scope (ring policy); do not size them.

## Ring-1 Population Anchors (for bottom-up work)

| Quantity | Value | Source (date) | Confidence |
|---|---|---|---|
| Population of Italy | 59.1M | DataReportal Digital 2026 Italy, UN data (Oct 2025) | high |
| Smartphone ownership, adults | ~90–95% (saturated; 51.6M devices counted) | AGCOM (2024 fieldwork) · Auditel (May 2026) | high |
| Online monthly / daily | ~44M / ~37.6M, mobile = 88% of online time | Audicom (Dec 2025–Apr 2026) | high |
| Median age 48.2 · 25.1% aged 65+ | — | DataReportal (Oct 2025) | high — an older population than the US/UK comparators; check the niche's age profile against it before sizing |

## Intent Conversion Benchmarks (Approach A — search volume)

**Construct (`confidence: low`).** No publisher measures web-search-volume →
app-install conversion; the nearest measured funnel (App Store search CVR,
a different denominator) runs 8–12% for "good" (2026). Calibration values:

| Search intent | Conversion rate | Example query |
|---|---|---|
| Direct solution search ("app to track X") | 8–15% | "habit tracker app", "budget planner iOS" |
| Problem-aware search ("how to X") | 3–8% | "how to save money", "how to build habits" |
| Category browsing ("best X apps") | 5–12% | "best workout apps", "top meditation apps" |
| Tangential interest ("X tips") | 1–3% | "productivity tips", "healthy eating advice" |

Ring note: Italian keyword volumes are usually unmeasured (no free Italian
instrument) — for Ring 1, Approach A often degrades to qualitative; when
volumes are missing, say the approach is inconclusive and lean on Approach B
and competitor evidence instead of forcing a number.

## Platform Multipliers (Approach B — community size proxy)

**Construct (`confidence: low`), anchored** to participation-inequality
research (Nielsen 90-9-1, 2006; van Mierlo, 2014): the *shape* — only a
small single-digit percentage of interested people participate — is sourced;
no publisher converts a community size into an interested population.

How many silent interested people per active community member:

| Signal source | Multiplier | Rationale |
|---|---|---|
| Reddit subscribers in niche subreddit | 20–50× | ~2–5% of interested people join a subreddit |
| TikTok hashtag creators (not views) | 100–500× | Tiny fraction of interested people create content |
| App Store **ratings count** for top competitor | 50–100× | ~0.5–2% of users leave a rating (practitioner estimates, 2025). Count ratings, not written reviews — written reviews are ~10× rarer (0.05–0.2%), which would imply a 500–2,000× multiplier |
| Newsletter subscribers in niche | 10–30× | Email subscribers are a warmer proxy |

Ring note: apply each multiplier to a **ring-matched community** — an
Italian-language surface sizes the Ring-1 pool, an English-language
subreddit sizes Rings 2–3. Never size the Italian pool from an
English-language community (the large "Italian" subreddits — r/ItalianFood,
r/ItalyTravel, r/italianlearning — are foreigners writing in English).

## Platform Filter — iOS share by market (for iOS-only apps)

StatCounter Global Stats, mobile OS **page-view** share, July 2026
(gs.statcounter.com), `confidence: high` for the metric as published.
Method caveat: page-view share runs iOS-high versus ownership — treat these
as upper bounds. Re-check before relying on this table: the pre-2026 version
had silently drifted 4–10 points low.

| Market (ring) | iOS share |
|---|---|
| **Italy (Ring 1)** | **~34–35%** |
| Western Europe big-four average (Ring 2 reference; DE 33.1% · FR 36.7% · ES 32.7% · IT 33.9–35.1%) | ~33–37% (constructed average — no published "Western Europe" region exists) |
| United Kingdom (Ring 3) | 53.9% |
| United States (Ring 3) | 59.6% |
| Canada (Ring 3) | 65.9% |
| Australia (Ring 3) | 63.7% |
| Worldwide (reference only) | 31.6% |

Italy is an Android-majority market: an iOS-only app forfeits ~65% of
Ring 1. For Android-only or cross-platform, apply the inverse or use 100%.

## SOM Capture Rate Benchmarks by Category

**Construct (`confidence: low`).** Indie capture rates do not exist publicly
anywhere (confirmed by two research passes, 2026). Calibration values:

| App category | Year 1 capture rate | Year 3 capture rate | Notes |
|---|---|---|---|
| **Utility / tool** (calculator, converter, scanner) | 0.1–0.5% of SAM | 0.5–2.0% | Discoverable via ASO, many competitors |
| **Niche productivity** (specific workflow tool) | 0.5–2.0% | 2.0–5.0% | Smaller SAM but higher capture in the niche |
| **Health & fitness (niche)** | 0.3–1.5% | 1.0–4.0% | Loyal users if retention is strong |
| **Health & fitness (broad)** | 0.05–0.2% | 0.2–0.8% | Dominated by incumbents |
| **Social / community** | 0.01–0.1% | 0.1–0.5% | Network effects favor incumbents; cold start is brutal |
| **Content / media** | 0.1–0.5% | 0.5–2.0% | Depends heavily on content quality and curation |
| **Finance / budgeting** | 0.1–0.5% | 0.5–2.0% | High trust barrier, but sticky once adopted |
| **Creative tools** (photo, video, design) | 0.2–1.0% | 1.0–3.0% | Shareable output drives organic growth |
| **Education / learning** | 0.2–1.0% | 1.0–3.0% | Retention is the main challenge |
| **Lifestyle / habit** | 0.3–1.5% | 1.0–4.0% | Success varies wildly by habit loop quality |

When more than one row applies, take the **lowest applicable band**; a
proven distribution edge on the higher row's channel is the only reason to
move up.

Use the **lower end** of the range when:
- `market_saturation` from `competitors.json` is "high"
- Founder is beginner tier (from `user_profile.md`)
- No distribution advantage identified

Use the **upper end** when:
- Founder has an existing audience or distribution edge
- Strong ASO opportunity or viral loop exists
- Market is growing fast (trend_velocity = "rising-fast")

Ring note: capture rates apply per ring, and they differ. Ring-1 capture may
sit at the upper end when the app is Italian-language-first with a
verified-active Ring-1 surface (Italian ASO and communities are less
contested); Ring-3 capture belongs at the lower end for a solo developer
entering a saturated English-language market.

## Outcome Reality Check (mandatory)

Cross-check every SOM estimate against published consumer-app outcome
distributions (RevenueCat State of Subscription Apps 2026, 115K+ apps;
Adapty 2026, 16K apps — both `confidence: high`, survivor-skewed upward):

- Only **4.6%** of newly launched subscription apps reach $10K monthly
  revenue within two years; the top 5% of new apps earn ~$8,880/mo after
  two years.
- Median app revenue 12 months after launch is **under $50/mo** (2024
  edition); Adapty's median app makes $492/mo, and 59.3% make under $1,000
  total.

State the implied percentile of your SOM-year-1 estimate against this
distribution. An estimate implying a top-5% outcome needs extraordinary
justification or a smaller capture rate.

## Reality-check thresholds and SOM verdict bands (read by the market-sizer brief)

The verdict is computed on the **sum of ring SOMs in EUR** (convert the
Ring-3 USD figure at a stated rate and mark it derived); the per-ring SOMs
are reported alongside, Italy first.

Numeric reality checks (record every triggered check in
`reality_checks_triggered`):

| Check | Threshold | Action if triggered |
|---|---|---|
| TAM inflation | TAM > €10B for a niche indie app | Almost certainly top-down numbers; redo bottom-up only |
| SAM too broad | SAM > 50% of TAM | Filters too loose; add ring/platform/niche constraints |
| SOM fantasy | SOM year 1 > €500K for a solo developer | Reality-check the capture rate; most indie apps earn €0–€50K in year 1 (and the published median is far lower — see the Outcome Reality Check) |

Alignment note: the €500K fantasy trigger deliberately sits 2.5× above the
"large" verdict floor (€200K). The verdict bands classify a *plausible*
estimate; the fantasy check fires on an *implausible* one. An estimate that
classifies "large" AND trips the fantasy check means the capture rate is
wrong, not that the market is huge.

`market_size_verdict` from summed SOM year 1 (bands are **constructs**
anchored to the outcome distribution above, `confidence: low` — against the
published distributions, "medium" is roughly a top-decile outcome and
"large" is beyond the top 5%; the bands describe opportunity headroom, not
typical outcomes):

| SOM year 1 (EUR, summed rings) | Verdict |
|---|---|
| > €200K | large — significant indie opportunity; double-check before trusting it |
| €50K–€200K | medium — viable as a primary project with good retention |
| €10K–€50K | niche — side-project scale; viable if build cost is low |
| < €10K | micro-niche — hobby scale unless the niche can expand |

## Fallback Price (when pricing.json is absent)

Use the median competitive price from `competitors.json` (per ring when the
competitor set splits by ring), or these anchors:

| Ring | Fallback price | Source | Confidence |
|---|---|---|---|
| Ring 1–2 (EUR) | €4–8/mo | Modal indie band on the IT storefront, 4,99–9,99 €/mo VAT-inclusive, observed live 2026-08 | high |
| Ring 3 (USD) | $3–7/mo | RevenueCat subscription price distribution (2024 data via 2026 breakout): Q1 $3.26 · median $6.68 | high (note the data lag) |

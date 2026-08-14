# Paid data providers with APIs — Italy-first (research, 2026-08-14)

Four reports pricing API-accessible data providers for the idea-validation
skill's needs, Italy first, EU second. Every figure carries source + date +
confidence; each report ends with a negative-result log (providers with no
public price). Prices observed 2026-08-14 — re-verify before purchase.

## Reports

- `firmographics.md` — Italian company data (counts, profiles, financials).
- `keywords-seo.md` — Italian keyword volumes, SERP data.
- `app-intelligence.md` — IT storefront charts, per-app estimates, ASO.
- `audience-reviews-scraping.md` — reviews, Reddit, Trustpilot, panels,
  scraping infrastructure.

## The prioritized spend plan (synthesis)

**Tier 1 — adopt now (~€80/month all-in):**

1. **DataForSEO** — $50 one-time deposit, no subscription; a full
   validation run (200 Italian keyword volumes + 20 SERP pulls) costs
   $0.07–$0.40, so the deposit covers 100+ runs. Closes the skill's
   single biggest measured gap (Italian keyword demand unmeasured in both
   forward tests). Italy confirmed as a supported location/language.
2. **Openapi.com** (company API) — €0 entry: unlimited sandbox, free
   monthly calls, and the decisive find: the `dry_run` parameter returns
   ATECO × province × size **counts for free** (100/day, then €0.01) —
   the b2b ICP-counting job at near-zero cost, at a granularity free
   ISTAT/Eurostat cannot reach (NUTS-2/2-digit only). Profile enrichment
   €0.015–0.30/call only when needed.
3. **Apify** — Starter $29/mo (light use fits the free $5 credit).
   Named maintained actors: app reviews $0.40–1.15/1K, Reddit $1.25/1K
   (post-2026-shutdown actor), Trustpilot IT $0.20/1K, Telegram
   $0.001/msg. The only practical route to Trustpilot IT and Reddit at
   scale — the official APIs are $799/mo+ (unpriced add-on) and
   $12K/month respectively.

**Tier 2 — pay per run, no standing subscription:**

- SEOZoom Evolution (€76 + IVA/mo, annual) — the Italian-native
  alternative to DataForSEO (richer IT dataset, 6,500 free API units/day)
  — choose it INSTEAD of DataForSEO only if the native dataset + UI
  matter; not additive. API is NOT on the entry plan.
- LinkedIn groups actor — $25/mo rental, activate per task.
- ASO keyword data — ASOdesk free tier (200 kw, 100 API credits/mo) or
  AppFollow +$19/mo when a b2c run is ASO-heavy.
- SerpApi ($9.17–25/1K) or Serpent (from $0.60/1K) only if a task needs
  Google.it SERP scraping beyond Exa + DataForSEO.
- GWI Plus ($150/user/mo, dashboard only, no API) for one-off Italian
  audience-composition months.

**Tier 3 — known price, buy only with a proven need:**

- **Appfigures Boost $599.99/mo** ($449.99 annual) — the cheapest
  *published* route to market-wide per-app IT download/revenue estimates.
  Every cheaper tier/tool estimates only your own apps. Justified only if
  validation volume grows or a verdict hinges on competitor revenue.
- Ahrefs Lite $129/mo — API opened to the Lite plan in March 2026; only
  worthwhile for broader SEO work beyond validation runs.

**Skip (enterprise-only / uneconomic / no public price):**
Sensor Tower + data.ai + Apptopia (est. $30K–300K/yr), Similarweb API
(sales-quoted; self-admitted 50–200% variance at small-site traffic),
Reddit commercial API ($12K/mo floor), Trustpilot official APIs, Semrush
API (needs the $455.67/mo tier, unit price unpublished), Cerved / Atoka /
CRIF Margo production (sales-led), Comscore / YouGov / Audicom panels
(€1,000–346,000/yr, publisher-oriented).

**Watch list:** AppMagic (acquired by Sensor Tower, May 2026 — the
"~$150/mo affordable" reputation is pre-acquisition and unconfirmed);
42matters (Italy-fit API on paper, but current pricing unverifiable from
its own site — needs a direct signup/sales check).

## What money cannot buy (cross-report negative synthesis)

No provider at any price sells: Italian per-category app WTP, indie
capture rates, Italian review→customer multipliers, an Italy CPI cut from
any MMP, or Italian app-install creator-campaign benchmarks. These remain
constructs in the calibration packs regardless of budget.

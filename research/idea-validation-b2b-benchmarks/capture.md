# Indie revenue / ACV / capture proxies — raw research report (2026-08-13)

Headline: one 2026 dataset (Stripe-verified, n=5,079) gives directly usable year-cohort medians; several widely-cited figures are content-farm inventions, excluded (list at bottom).

## 1. Indie/bootstrapped SaaS revenue outcomes

| Metric | Value | Source |
|---|---|---|
| Median MRR, all tracked products | $169/mo | Indie Hackers analysis of TrustMRR data, n=5,079 Stripe-verified, 12 Mar 2026 — https://www.indiehackers.com/post/i-analyzed-5-079-stripe-verified-startups-f0f6bd053f |
| 75th / 90th / 99th percentile | ~$800 / $10,000 / $98,500 per mo | same |
| "Breaking out" (>$10k MRR AND >50% mo/mo growth) | 0.9% (48 of 5,079) | same |
| Median MRR by product age | Y0 $148 · Y1 $334 · Y2 $656 · Y4 $2,399 · Y5 $2,509 (Y3 not reported) | same |
| Share making $0 | >54% | ScrapingFish, n=937, Jul 2022 — DATED — https://scrapingfish.com/blog/indie-hackers-revenue |
| Bootstrapped SaaS median growth rate | 20%/yr (vs 25% equity-backed) | SaaS Capital 14th annual survey, n>1,000, 2026 — https://www.saas-capital.com/research/private-saas-company-growth-rate-benchmarks/ |
| Median profit multiple, SaaS sold <$10M EV | 3.9x SDE/EBITDA (2024 and 2025); avg margin 71%; 81 days on market | Acquire.com Biannual Multiples Report, 11 Feb 2026 — https://blog.acquire.com/acquire-com-biannual-acquisition-multiples-report-jan-2026/ |

Year-1 median ≈ $330/mo, year-2 ≈ $650/mo. Y3 interpolation between Y2 and Y4 is a derivation, not source data.

## 2. Pricing / ACV

| Metric | Value | Source |
|---|---|---|
| Shopify apps: avg monthly cost across all plans | $66.54 | Meetanshi, full app-store scrape, Jan 2025 — https://meetanshi.com/blog/shopify-app-store-statistics/ |
| Shopify apps: share offering a free plan/trial | 45.8% (5,642 of 12,320) | same |
| Shopify apps: max plan price observed | $999.99/mo | same |
| Dental practice management (vertical SMB) | $249-$1,499 per location/mo, plus $79-$199 per provider | Molar Report — https://www.themolarreport.com/learn/dental-software-real-world-pricing — vendor-quoted, single source |
| ChartMogul B2B/B2C ARPA dividing line | B2B = ARPA >$25/mo | ChartMogul SaaS Growth Report, n=2,200+, 2023 — https://chartmogul.com/reports/saas-growth-report/ |

No credible dataset exists for ACV by micro-SaaS category (dev tools, SEO/marketing, productivity add-ons) — everything found is AI-generated with no methodology. ChartMogul explicitly excludes companies under $300K ARR — exactly the modeled population. The Shopify scrape is the only defensible category-level price anchor, e-commerce apps only.

## 3. Marketplace capture proxies

| Metric | Value | Source |
|---|---|---|
| Shopify App Store apps | 12,320 (Jan 2025) | Meetanshi (above) |
| Shopify partners with >=1 listed app | 7,874 of 40,556 registered partners; 79.5% list exactly one app | same |
| Shopify apps with zero reviews | 34.98% (4,310) | same |
| Shopify dev revenue share | 0% on first $1M gross (from 1 Jan 2025), 15% above; plus 2.9% processing | https://shopify.dev/docs/apps/launch/distribution/revenue-share |
| Atlassian Marketplace | 6,000-8,000+ apps; >$6B lifetime sales; ~300K customers | https://developer.atlassian.com/platform/marketplace/introduction-to-marketplace/ ; Aventis Advisors, Aug 2025 — https://aventis-advisors.com/atlassian-marketplace-ma/ |
| Shopify live storefronts | ~2.86M (Store Leads, May 2026); BuiltWith's ~6.9M inflates via parked/dev stores | secondary aggregators |

No marketplace publishes per-app revenue or install distributions. The zero-reviews share (35%) is the best available proxy for "apps that never got traction" — a derivation, and a floor.

## 4. Bottom-up TAM: canonical business-count sources

| Population | Count | Source (reference year) |
|---|---|---|
| US nonemployer businesses | 30,427,808 | Census Nonemployer Statistics (2023) |
| US employer firms <500 employees | 5.58M | Census SUSB / SBA Office of Advocacy (2023) |
| By-industry establishment counts | — | Census SUSB by NAICS; BLS QCEW for timelier data |
| Professionally active US dentists | 202,485 | ADA Health Policy Institute (2024) — https://www.ada.org/resources/research/health-policy-institute/dentist-workforce |
| US fitness facilities | ~55,000 (HFA/IHRSA) vs ~114,370 (IBISWorld) — definitions differ | HFA; IBISWorld (2024) |
| Advertising agencies (NAICS 541810) | 11.5k-15.0k depending on source | Census SUSB / Statista (2022) |

Federal sources lag 2-3 years — surface the reference year. No canonical count of "agencies" (541810 vs 541613 definitional issue). SBA Advocacy FAQ PDF returned 403; figures from Census program pages (the SBA FAQ's own underlying source).

## 5. Time to first $1k MRR

p25 5 / median 8 / p75 12 months, mean 9 — n=28, Indie Hackers, Jun 2022 — https://www.indiehackers.com/post/it-takes-5-months-to-reach-1k-in-mrr-491742f806
Effectively anecdotal, survivor-selected (filtered ~100 -> 28 "steady growth"). Prefer the age-cohort medians: the median product does not reach $1k MRR by year 2.

## Confidence notes

Corroborated: bootstrapped growth ~20%/yr (SaaS Capital, independent). Shopify app counts/pricing (single scrape of the complete public dataset, independently verifiable). Federal business counts.

Single-source: the entire revenue distribution rests on TrustMRR via one Indie Hackers analysis — best available (payment-processor-verified, n=5,079, Mar 2026) but unreplicated; TrustMRR launched Oct 2025, coverage skews to opt-in founders.

Anecdotal only: time-to-$1k-MRR (n=28); all category-level ACV outside the Shopify scrape.

EXCLUDED AS FABRICATED/UNUSABLE (keep out of calibration):
- "Shopify app devs average $98k/yr, top 25% $167k" — arithmetic fails ($1.5B cumulative / 12,320 apps ≈ $122k CUMULATIVE since 2009); top quartile 1.7x mean impossible under app-store power law.
- "Median micro-SaaS $4.2K MRR / 70% under $1K / top 1% above $50K" — one content-farm study (Rocking Web); Freemius cites it (one source, not two); contradicts Stripe-verified $169 median by 25x.
- "28% of MicroConf founders exceed $100K MRR" — conference-audience poll (n=230), paid self-selected cohort.
- "0 to $10K MRR in 6 months" / "median 12-18 months to $1K MRR" — no methodology, AI-generated.

Gated: MicroConf State of Independent SaaS (email wall) — worth pulling manually.

BIAS DIRECTION: every source skews UPWARD (Acquire.com = completed sales, twice-selected; TrustMRR = opt-in survivors; SaaS Capital = above micro-SaaS scale). Only downward corrector: >54% zero-revenue share (2022, n=937). Uncorrected, these numbers systematically overestimate indie capture.

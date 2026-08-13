# CAC by channel — raw research report (2026-08-13)

HEADLINE CAVEAT: no published dataset covers solo founders at sub-$2,000/mo marketing spend. Every benchmark source below (Benchmarkit, ChartMogul, First Page Sage, Aleph) has an implicit floor around $1M ARR with a sales function. First Page Sage's per-channel CAC figures come from ~120 firms whose average B2B LTV is $32,414 — two orders of magnitude above a $30/user/mo tool. Use their numbers for RELATIVE channel ordering (referral < SEO < paid search < LinkedIn < outbound), not as absolute targets. The genuinely transferable units at indie scale are CPC, CPL, and conversion rates.

## CHANNEL TABLE

| Channel | Metric | Range | Source |
|---|---|---|---|
| Content/SEO | B2B CAC | $647 thought-leadership SEO; $1,254 content marketing; $1,786 basic SEO | First Page Sage, CAC by Channel — https://firstpagesage.com/marketing/cac-by-channel-fc/ — pub 17 Apr 2025, upd 18 Jun 2025 |
| Paid search | CPC/CPL | Cross-industry CPC $5.42, CPL $66.69. "Business Services" CPC $5.87, CVR 4.85%, CPL $93.69. At 2-5% trial->paid, CPL $94 implies $1,900-$4,700 per PAYING customer | WordStream 2026 Google Ads Benchmarks — https://www.wordstream.com/blog/2026-google-ads-benchmarks — 13,474 US search campaigns, Apr 2025-Mar 2026, pub 19 May 2026. Same dataset republished at https://localiq.com/blog/search-advertising-benchmarks/ (upd 1 Jun 2026) |
| Paid search | B2B CAC | PPC/SEM $802 | First Page Sage (above) |
| LinkedIn ads | CPC/CPL | Avg CPC $5.59; 75% of campaigns pay >$6/click, only 12.5% under $3; CPL $221 (external conversions) to $811 (native lead forms); platform CTR 0.52% | Impactable — https://impactable.com/linkedin-cpc-benchmarks-2026/ — 2025 data, sample size NOT disclosed |
| LinkedIn ads | B2B CAC | $982 | First Page Sage (above) |
| Meta ads | CAC | $230 — B2C ONLY in this dataset. No B2B Facebook CAC published anywhere verifiable; the $230 figure is widely misquoted as B2B | First Page Sage (above) |
| Shopify App Store | Platform take | 0% on first $1M lifetime revenue (from 1 Jan 2025), 15% above; $19 one-time; +2.9% processing | https://shopify.dev/docs/apps/launch/distribution/revenue-share |
| Atlassian Marketplace | Platform take | Forge: 0% on first $1M lifetime (from 1 Jan 2026), then 16% (Apr 2026) -> 17% (Oct 2026). Connect: 15% -> 20% (Apr 2026) -> 25% (Oct 2026) | https://www.atlassian.com/blog/development/updates-to-marketplace-revenue-share-2026 |
| Chrome Web Store | Platform take | $5 one-time registration; Google's own payments retired, bill directly, 0% | https://developer.chrome.com/docs/webstore/register |
| Cold outbound | Reply rate | 3.43-5.8% cross-industry; B2B SaaS bottom-of-pack at 2-4% (inbox saturation); ~0.8-2 meetings per 100 sends | https://instantly.ai/blog/cold-email-reply-rate-benchmarks/ ; https://belkins.io/blog/cold-email-response-rates (2026) |
| Product Hunt | Signups | Top-3: 5,000-15,000 launch-day visitors, 100-400 signups. Top-10: 1,000-3,000 visitors, 30-100 signups. Outside top 10: <500 visitors, <20 signups. B2B visitor->signup 1-2% | https://waitlister.me/growth-hub/guides/product-hunt-launch-checklist — LOW CREDIBILITY, no methodology |
| Communities/integrations | Qualitative only | 47% of bootstrapped founders say integrations, partnerships, communities and forums became their most dependable growth source in 2025; 50% lean on communities/referrals and report stronger LTV; 57% of founders running ads either wait 7+ months for ROI or cannot tell if ads work | Freemius State of Micro-SaaS 2025 — https://freemius.com/blog/state-of-micro-saas-2025/ — synthesizing MicroConf State of Independent SaaS (~700 founders), https://microconf.com/state-of-indie-saas |
| Referral | B2B CAC | $150 — lowest of any channel | First Page Sage (above) |

## PAYBACK AND LTV:CAC

| Metric | Value | Source |
|---|---|---|
| CAC payback, median | 16 months (top quartile <=6, bottom >=24) | Aleph x Benchmarkit 2026 SaaS & AI Benchmarks, FY2025 actuals, 342 companies — https://www.getaleph.com/answers/cac-payback-period-saas-2026 |
| CAC payback by ACV | 9 months at sub-$5K ACV (closest tier to indie), 12 mo at $10-25K, 24 mo at >$250K | Benchmarkit 2025 — https://www.benchmarkit.ai/2025benchmarks |
| New-customer CAC ratio | $2.00 median ($2 spent per $1 new ARR), up 14% in 2024; expansion CAC ratio $1.00 | Benchmarkit 2025 |
| LTV:CAC | 3:1 is a stated floor, NOT a measured median. No source publishes a measured LTV:CAC distribution — folklore repeated as benchmark | First Page Sage; Freemius |
| Trial->paid, self-serve B2B | ~2.5% at 7 days, ~1% by day 14 for pure self-serve. Freemium->paid 3-4%; opt-in trial (no card) 18%; opt-out trial (card) 50% | ChartMogul SaaS Go-To-Market Report — https://chartmogul.com/reports/saas-go-to-market-report/ — 2,500 companies, Q1 2024-Q1 2025 |
| Time to 1,000 B2B subscribers | Median 24 months; top performers 11 months | ChartMogul (above) |

## CONFIDENCE NOTES

Corroborated: Google Ads CPC/CPL (WordStream and LocaliQ publish the SAME dataset — one source, two URLs). Cold email reply rates for SaaS at 2-4% (Instantly, Belkins, Martal agree). CAC payback 12-16 month median and rising (Benchmarkit and Aleph agree). Marketplace revenue-share terms verified on platforms' own docs — highest-confidence numbers here.

Single-source or weak: LinkedIn CPL ($221-$811) rests on Impactable alone, no disclosed sample. Product Hunt signup ranges are marketing-blog folklore, no methodology. The entire First Page Sage table is one vendor's proprietary client data, never independently replicated.

Where data genuinely does not exist (do not extrapolate):
- No CAC benchmarks for solo founders at sub-$2,000/mo spend. Full stop.
- No quantified acquisition data for HN launches, X/LinkedIn founder-brand content, or founder-led community presence — founders RANK these channels highly (MicroConf/Freemius) but zero cost-per-customer figures exist.
- No published install->paid conversion rates for Shopify, Slack, Atlassian, or Chrome listings — platforms disclose revenue share, not funnel data.
- No B2B Meta/Facebook CAC for SMB tools.
- No current OpenView/KeyBanc PLG benchmark edition: OpenView wound down in 2024; the series has no successor.

Search caveat: a large share of top-ranking results are AI-generated content farms (rockingweb.com.au, metricnexus.ai, rudys.ai, konabayev.com, ltvcacbook.com, admanage.ai). All excluded; every number above verified on the primary or named-vendor page.

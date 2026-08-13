# Gated-PDF digests — MicroConf 2024 + SaaS Capital RB32 (read 2026-08-13)

Digests of the two gated PDFs the user pulled manually (files in this directory).
These close the two open items from `research/idea-validation-b2b-benchmarks/README.md`.
Geography-neutral benchmarks: they calibrate indie-SaaS constructs, not Italian ones.

## 1. SaaS Capital Research Brief 32 — 2025 B2B SaaS Retention Benchmarks

Source: 14th annual survey, Q1 2025, >1,000 private B2B SaaS companies.
**Sample caveat (carry into every use): excludes companies under $1M ARR** — this is
the up-market gradient, NOT an indie benchmark. Use it to anchor the ACV→retention
slope; keep ChartMogul (self-serve-skewed, NRR median 82%) as the indie-scale anchor.
The gap between the two samples is itself the calibration lesson: retention rises with
ACV and with having a retention team.

### Median NRR / GRR by ACV (Figure 1) — confidence: high

| ACV | Median NRR | Median GRR |
|---|---|---|
| < $12k | 98% | 90% |
| $12k–25k | 103% | 91% |
| $25k–50k | 102% | 91% |
| $50k–100k | 104% | 90% |
| $100k–250k | 102% | 91% |
| > $250k | 106% | 95% |

NRR quartiles (Figure 2): <$12k = 90 / 98 / 106 (p25/p50/p75); widest spread at
$12k–25k (98 / 103 / 115); >$250k is the only band where even p25 expands (102).

### Other anchors — confidence: high

- All-company 2025 medians: **NRR 101%, GRR 91%**; "GRR ≥ 90% is table stakes".
- **Bootstrapped companies: NRR 104%, GRR 92%** (slightly better than equity-backed
  101/90 — customer-success practice has fully diffused).
- Contract length: month-to-month 100/89 · annual 101/90 · multi-year 103/94.
- Growth by NRR band (median growth): <90% → 15% · 90–100 → 16% · 100–110 → 21% ·
  110–120 → 30% · 120–130 → 38% · >130% → 50%. Population median growth 24%.

### Pack implications

- `retention.md` (b2b): keep ChartMogul as primary (right sample for micro-SaaS);
  add this as the ACV-gradient cross-check and the "sub-$12k ACV NRR 98% vs >$250k
  106%" contrast. The <$12k row (≈ <€1k/mo) is the relevant row for our targets.
- `market-sizing.md`: the growth-by-NRR ladder replaces vaguer "retention compounds"
  language in reality checks.

## 2. MicroConf — The 2024 State of Independent SaaS (4th annual)

Methodology (p.63): web survey of ~45,000-founder database, run **Oct 28 – Nov 15,
2023**; 696 participants, **469 completions**; respondents must be operating a
revenue-generating recurring-fee software company. **Caveats: self-reported; MicroConf
community skew (survivorship + English-speaking); data is from late 2023 — flag
`[OLD]` (structural patterns usable, absolute rates treat as directional).**
41 countries, 265 cities; 50.7% solo founders; 68.4% full-time; avg company age 48
months; 29% founder-is-sole-employee; ICP mix: 77% target businesses (38% mid-market,
25% small business, 14% enterprise, 7% consumers).

### Growth by ideal customer type (avg MoM growth, p.21) — confidence: medium

Enterprise 26.7% · Mid-market 22.0% · NGOs 18.5% · Creators 12.8% · **Small business
12.0%** · Aspiring entrepreneurs 9.6% · Education 6.1% · **Consumers 5.3%** ·
Government 1.8%. (Growth ≠ ease: enterprise growth comes with sales-led motion.)

### Pricing (pp.24–31) — confidence: medium-high (distributional)

- Structures offered: monthly 81% · annual 63% · one-time 11% · metered 10% ·
  pay-as-you-go 9% · revenue share 4%.
- **Lowest-plan mode: $20–49/mo (27%)**; $50–99 19%; $1–9 17%; $10–19 15%;
  $100–249 12%. (Corroborates the pack's $19–79 indie sweet spot.)
- Free offerings: freemium 29.1%; free trial 51.6%; of trial products, **70.7%
  require a credit card** (2024).
- Trial→paid conversion distribution: no-CC mode is 1–9.9% (37% of companies) then
  10–19.9% (22%) — consistent with ChartMogul "good = 4–6%". CC-required is extreme:
  **47% of CC-required products report ≥50% trial→paid** (self-report; still, the
  bimodality direction matches ChartMogul's 25–35%).
- Model economics (avg): CC-required trial 14.0% MoM growth / 5.5% churn ·
  no-CC trial 7.7% / 6.3% · free plan 10.5% / 10.6% churn.
  **LTV: free plan $3,026 · CC trial $3,652 · no-CC trial $6,504 (~1.8–2.2×)** —
  the no-CC funnel filters worse but the customers kept are worth more. Nuances the
  "card-required = better" rule: better conversion and growth, lower LTV.

### SaaS metrics (pp.34–37) — confidence: medium

- MRR: 27.6% under $1K; ~60% under $15K (this is a more-established sample than
  TrustMRR's — use TrustMRR for year-cohort medians, this for the overall shape).
- Avg MoM growth: mode 1–4% (29.7%); 30.2% at zero or negative.
- Monthly **revenue** churn (2024): 40.8% report 0–0.9%; 18.3% 1–2.9%; 16.1% 3–5.9%;
  6.2% net negative. (Self-reported and better-than-ChartMogul — treat as optimistic
  corroboration only; ChartMogul stays primary.)
- LTV: 31.1% report $7,500+; 10.5% under $100.

### Marketing & channels (pp.38–42, 48) — confidence: medium

- **63% use no paid advertising at all.**
- Highest-impact activities: SEO 65% · word of mouth 65% · cold outreach 46% ·
  content 45% · email 35% · social 34% · **conferences/trade events 32%** ·
  affiliate 29% · integrations 26% · communities 21% · virality 6%.
- Split by LTV: **<$5K LTV → SEO (69%) + WoM + content; >$5K LTV → cold outreach
  (67%) + conferences (54%)**. (For Italy: the cold-outreach half is legally blocked —
  conferences and phone-consent bridge take its slot at high LTV.)
- Ad ROI honesty check: **57% of advertisers either wait >7 months for ROI or don't
  know it**; LinkedIn worst (58% don't know). Avg monthly MRR growth by ad channel:
  Facebook $1,669 · sponsorships $1,306 · LinkedIn $1,272 · Google $1,102 (survivor
  bias inside a 37%-of-sample subgroup).

### Growth cross-tabs (pp.45–51) — confidence: medium

- Full-time founders grow **2.2×** part-time; ≥1 developer founder **1.7×**
  non-technical teams; founder trios show the best average MoM growth (40.95%),
  4+ founders collapse (4.85%).
- Avg monthly MRR growth by hours worked: <10h $475 → 40–49h $1,177 (peak) →
  50h+ $1,070.
- Avg MRR growth rises with monthly price: $1–9 $316 · $50–99 $790 · $1000+ $1,073 —
  and with customer LTV (<$100 $108 → $7500+ $1,022). Low price = low growth at
  indie scale.
- Free trial beats no-trial across every pricing structure (annual $1,041 vs $668;
  metered $1,729 vs $765).
- Funding: 20.9% raised (86% one round; 75% raised $100–499k). Funded avg MRR
  growth $1,160/mo vs unfunded $794/mo.

### Exits (pp.57–62) — confidence: medium

- 21% of respondents sold a prior company; of previous companies overall, 49% were
  shut down (up 6 pts vs 2022).
- **Exit multiple mode: 1–2.9× forward run rate (37%), then 3–4.9× (28%)**; ≥10×
  is 11% combined. Buyers: another company 60% · individual 21% · fund 10%.
- Run rate at sale: 20% at $1–2.99M; 18% at $100–499k; 24% below $75k.

### Pack implications

- `pricing.md` (b2b): lowest-plan mode and the CC/no-CC LTV asymmetry (nuance to the
  entry-model table); trial-beats-no-trial across structures.
- `cac.md`: the 63%-no-paid-ads and 57%-ROI-blind numbers harden the organic-first
  default; channel ranking for the >$5K-LTV tier (conferences substitute for cold
  outreach in Italy).
- `retention.md`: churn distribution as optimistic secondary corroboration only.
- `market-sizing.md`: growth-by-ICP ladder (SMB 12% avg MoM vs consumers 5.3%);
  exit-multiple bands (1–3× forward run rate is the realistic outcome anchor).
- `scoring-rubrics.md` / founder-fit: full-time 2.2×, developer-founder 1.7×,
  hours curve — evidence for the tier adjustments.
- `demand-drivers.md`: budget-authority framing unchanged; growth-by-ICP supports
  the "operators with company card" focus.

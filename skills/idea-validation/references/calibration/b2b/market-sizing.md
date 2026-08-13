# Market sizing — B2B calibration (Italy-first, self-serve micro-SaaS)

Loaded by `iv-market-sizer` via the CALIBRATION path in its dispatch prompt.
Defines the estimation proxies, population counts, buyer-redirection rule,
capture rates, and fallback prices for the Italian B2B target. The
triangulation mechanism, SAM filter logic, reality checks, and verdict
thresholds live in the agent brief.

> **Bias warning (apply throughout):** every published indie-revenue source
> skews upward (survivor selection). Estimate conservatively and say so.
> Two Italy-specific traps on top:
> 1. **Four incompatible "how many firms" universes** — ASIA active
>    enterprises (~4.51M, 2023), Registro Imprese registered firms (~5.82M,
>    2026), yearly partita IVA openings (~500K/yr — a flow), self-employed
>    people (~5.28M). Use ASIA as the canonical enterprise base; never mix
>    or sum universes.
> 2. **The micro-firm data void** — ISTAT/DESI ICT adoption surveys cover
>    firms with 10+ addetti (5.2% of the universe). Below 3 addetti (~3.5M
>    firms) NO adoption data exists. **Never present the ~4.27M micro-firm
>    count as a TAM**: the plausibly-paying-for-SaaS population is in the
>    hundreds of thousands, not millions.

## Contents

- Step 0 — Buyer redirection (mandatory, before any sizing)
- Business-Count Anchors (Approach A-bis — population × ACV; the primary approach)
- Intent Conversion Benchmarks (Approach A — search volume)
- Community & Review Proxies (Approach B — weakest in Italy)
- Platform Filter
- SOM Capture Rates
- Outcome Reality Check (mandatory)
- Reality-check thresholds and SOM verdict bands (read by the market-sizer brief)
- Fallback Price (when pricing.json is absent)

## Step 0 — Buyer redirection (mandatory, before any sizing)

Decide **who the buyer is** for this category. In Italy, ~75% of taxpayers
file through a commercialista and ~80% of private companies use a consulente
del lavoro (2024, CNDCEC/ordini data). For accounting, payroll, tax,
compliance, and document categories the micro firm is frequently NOT the
buyer — the professional studio is, buying once and using it across many
client firms.

| Buyer | Population base | Consequence |
|---|---|---|
| The firm itself | ASIA counts by ATECO × size class | Standard sizing below |
| The studio / intermediary | ~69.2K studi commercialisti (2024) · ~26.1K consulenti del lavoro (2025) · legal: ~211K active avvocati, only ~9.8% in associated firms | Small, well-defined, reachable universe; per-account value multiplies by clients managed; distribution runs through ordini/associations |
| Both (firm pays, studio recommends) | Firm counts, discounted by intermediary adoption | Model the intermediary as channel (see distribution pack) |

State the chosen buyer in the artifact rationale — it changes SAM by two
orders of magnitude.

## Business-Count Anchors (Approach A-bis — population × ACV; the primary approach)

Canonical Italian counts (cite the reference year; ASIA lags ~2 years):

| Population | Count | Source (reference year) | Confidence |
|---|---|---|---|
| Active enterprises, total | ~4.51M | ISTAT ASIA (2023) | high |
| — micro (<10 addetti) | ~4.27M (94.8%) | ISTAT ASIA (2023) | high — never a TAM; see the bias warning above |
| — firms with 10+ addetti | ~236K | ISTAT ASIA (2023) | high |
| — firms with 3+ addetti | ~1.02M | ISTAT census frame (2022) | medium |
| Studi commercialisti | ~69.2K studi · 119K professionals | CNDCEC (2024 — cite as 2024, not newer) | high |
| Consulenti del lavoro | ~26.1K | ordine (2025) | high |
| Avvocati | ~211K active; ~9.8% in studi associati/STA/STP | Cassa Forense (2025) | high |
| Notai | ~5.2K | (2026) | high |
| Per-ATECO cross-tabs | look up by ATECO × size class | ISTAT ASIA; **Eurostat SBS API is the scripted route** (ISTAT SDMX unreliable) | high |
| Registered firms (Registro Imprese) | ~5.82M stock; +0.56%/quarter, shifting toward società di capitali | Movimprese (Q2 2026) | high — but a different universe: use only for demography/trend, never as the base |

**Adoption discounts** (apply when the buyer is the firm): firms 10+ addetti
— 75.6% buy cloud, 56.0% use management software (ISTAT 2025, high). Firms
3+ addetti — ~29% cloud, ~34% management software (2022 census, low-medium).
Below 3 addetti — no data exists; extrapolating the curve further down is
fabrication. State which adoption base the SAM uses.

## Intent Conversion Benchmarks (Approach A — search volume)

Rates are unchanged from the global pack (no Italy-specific study exists —
provisional, `confidence: low`): direct solution search 5–12% · problem-aware
2–5% · category comparison 4–10% · tangential 0.5–2%. The Italian
difference is the **volume side**: measure Italian-language queries
(SEOZoom or DataForSEO with location Italy — see the tooling reference);
Italian long-tail SaaS demand is publicly unmeasured and typically low —
when volumes are tiny, say the approach is inconclusive rather than forcing
a number.

## Community & Review Proxies (Approach B — weakest in Italy)

The global multipliers (reviews ×30–60, community members ×10–30…) assume
Anglophone review/joining behavior and are **unreliable for Italy** —
Italians under-review and professional discussion happens in private/offline
spaces. Use Approach B only as a corroborating floor, at `confidence: low`,
preferring: marketplace installs (×1–3) · incumbent-forum activity as
relative size · association membership counts (ordini registers are
near-complete universes for regulated professions — the rare high-quality
proxy).

## Platform Filter

When the product lives inside one ecosystem, SAM is bounded by that
ecosystem's Italian population: Fatture in Cloud (vendor claims 500K+
businesses, 16K accountants — halve marketing claims), TeamSystem Commerce,
Shopify storefronts in Italy (cite the aggregator count and date), a
platform's Italian developer/agency count. Cite the count and its date.

## SOM Capture Rates

No published capture-rate data exists for indie B2B anywhere, and Italian
channels are thinner (no cold email, fewer communities) — keep the global
provisional bands and lean to their LOWER ends unless a distribution edge
is proven (`confidence: low`):

| Situation | Year 1 capture of SAM | Year 3 capture |
|---|---|---|
| Niche vertical, weak incumbents, founder has domain access | 0.5–2.0% | 2.0–5.0% |
| Marketplace category with ranking opportunity (FIC App Store class) | 0.2–1.0% | 1.0–3.0% |
| Horizontal SMB tool, established competitors | 0.05–0.3% | 0.3–1.0% |
| Category owned by a suite incumbent (TeamSystem/Zucchetti class) | 0.01–0.1% | 0.1–0.5% |

When more than one row applies (e.g. a suite incumbent bundles the feature
AND a marketplace listing is available), take the lowest applicable band; a
proven distribution edge on the higher row's channel is the only reason to
move up.

## Outcome Reality Check (mandatory)

Cross-check every SOM estimate against indie cohort medians (TrustMRR via
Indie Hackers, n=5,079, Mar 2026): Year 0 $148 MRR · Year 1 $334 · Year 2
$656 · Year 4–5 ~$2,400–2,500 · 90th percentile ~$10K · "breaking out" 0.9%.
A SOM-year-1 above ~€110K ARR implies a top-decile outcome; above ~€450K
top-1% — either needs extraordinary justification or the estimate is wrong.
State the implied percentile.

Corroborating anchors: MicroConf 2024 (n=469, late-2023 data — directional):
~60% of independent SaaS sit under $15K MRR; small-business-targeting
products average 12% MoM growth vs 5.3% consumer; exit multiples cluster at
1–2.9× forward run rate (37%) then 3–4.9× (28%). SaaS Capital 2025: median
bootstrapped-company NRR 104% — but that sample excludes <$1M ARR; ChartMogul's
82% NRR self-serve median is the right expectation at indie scale.

## Reality-check thresholds and SOM verdict bands (read by the market-sizer brief)

Numeric reality checks (record every triggered check in
`reality_checks_triggered`):

| Check | Threshold | Action if triggered |
|---|---|---|
| TAM inflation | TAM > €500M for a vertical Italian niche | Top-down artifact; redo bottom-up from the buyer-redirected population |
| SAM too broad | SAM > 50% of TAM | Filters too loose; tighten segment, size class, or software-stack filters |
| SOM fantasy | SOM year 1 > €110K ARR for a solo developer | That is already a top-decile outcome (TrustMRR, n=5,079); justify the capture rate explicitly or cut it |

`market_size_verdict` from SOM year 1 (bands are constructs anchored to the
outcome distribution above, `confidence: low`):

| SOM year 1 | Verdict |
|---|---|
| > €110K | large — implies a top-decile outcome; double-check before trusting it |
| €45K–110K | medium — sustains a solo developer |
| €10K–45K | niche — side-project scale |
| < €10K | micro-niche — hobby scale |

## Fallback Price (when pricing.json is absent)

Use the median competitive price from `competitors.json`, or these Italian
anchors (ex-VAT, from the 2026-08 pricing research — medium confidence):
micro-firm tools €12–25/mo · SMB team tools €29–99/mo flat · studio-side
professional tools €100–250/mo per studio (dealer-mediated band) ·
marketplace apps: cite the marketplace's own pricing norms.

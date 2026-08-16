# Gated-report digests (manual pulls, 2026-08-16)

User-obtained copies of the gated reports flagged by the Phase D-A pass.
Source files in this directory: `appsflyer-subscription-trends-2026.md`
(web export) and `mobile-app-trends-2026.pdf` (Adjust, 41 pp). SplitMetrics
2026 remains partially gated — see the last section.

## 1. AppsFlyer "Subscription app marketing trends 2026" (2026-03)

Sample: 1.7B paid installs of subscription apps, $2.1B UA spend, 2.9K apps,
Oct 2024–Feb 2026. **Geographic cuts are coarse regions; no Italy or
Western-Europe-specific numbers.** Confidence high (primary report).

**The headline for our packs: the report contains NO retention table.** The
content-mill "subscription-app D30 = 14% vs 5.4%" figure attributed to
AppsFlyer does not appear anywhere in it. The b2c retention pack's
reframing (pack ranges = well-executed subscription band, construct)
stands; no open primary source for a subscription retention premium exists
even behind the gate.

What it DOES give (feeds `pricing.md` freemium section — real per-category
conversion, paid-UA subscription apps):

| Category | Install→trial | Trial→paid | No-trial install→paid |
|---|---|---|---|
| Gaming | 12.2% (highest) | 19% (lowest by far) | — |
| Education | — | 42% (highest) | — |
| Lifestyle | 3.9% (lowest) | 41% | — |
| Health & Fitness | — | ≥32% band | 7.1% (leads) |
| Dating | — | ≥32% band | 6.5% |
| Short Drama | — | — | 1.8% |
| Utility & Productivity | — | — | 1.7% |
| All categories | — | every non-gaming category ≥32% | average 3.5% |

Context worth keeping: Health & Fitness top-5 UA-spend concentration
jumped 54% → 73% (incumbents pricing out small apps); Photo & Video
deconcentrated 64% → 45% (AI tools disrupting); Android crossed the
paid-install majority (51%); iOS organic installs declined 8%.

## 2. Adjust "Mobile app trends: 2026 edition" (2025 full-year data)

Verticals covered: gaming, e-commerce, finance only. Global all-install
curves plus regional CPI cuts. Confidence high (primary report, dated).

**Retention (global, 2025, all installs — the published-median floor, now
dated and per-vertical):**

| Vertical | D1 | D7 | D14 | D30 |
|---|---|---|---|---|
| Gaming (all) | 27% | 13% | 8% | **5%** |
| — hyper casual | 27% | 8% | 6% | 2% |
| E-commerce (all) | 12.6% | 6% | ~4.4% | **3%** |
| — marketplace & classifieds | 24% | 14% | 11% | 8% |
| — shopping | 12% | 6% | 4% | 2% |
| Finance (all) | 12% | 6% | — | **2%** |

Rates were essentially unchanged from 2024 — the floor is stable, not an
off-year.

**CPI (2025, USD):** gaming global $0.56 (+30%); e-commerce global $0.98,
**Europe $2.25** (up from $1.83), North America $2.49, APAC $0.68; finance
global $1.13, **Europe $4.75** (down from $7.37), North America $4.13;
banking $2.09, payments $1.44, crypto $2.90. **These Europe rows are the
first disclosed-methodology Europe-cut CPIs found anywhere in this
research** (DA3's negative log recorded none) — vertical-limited, and
still no Italy cut.

Other anchors: ATT opt-in industry average 38% (Q1 2026); paid/organic
ratio gaming 3.33, e-commerce 0.54, finance 1.13; 2025 installs +10% /
sessions +7% globally; February is the annual install trough (-13% vs
average), December the peak.

## 3. SplitMetrics "Apple Ads Search Results Benchmarks 2026" (CY2025)

Source file in this directory:
`splitmetrics-benchmarks-by-markets-2026.pdf` (browser export of the
gated "Benchmarks by Countries and Regions" section). Sample: 6.3B
impressions, 495.6M taps, 315.6M downloads, 91 markets, CY2025.
Confidence high (primary report).

**The Italy cross-check on MobileAction resolves as a bound, not a
number.** SplitMetrics publishes only top-15 charts per metric, and Italy
**dropped out of all four top-15 rankings** (TTR, CR, CPT, CPA) between
2024 and 2025. Since the CPT/CPA charts rank the most expensive markets,
Italy in 2025 sits below their floors: **CPA < $2.42** (Norway, 15th) and
**CPT < $1.51** (France, 15th). MobileAction's Italy figures (CPA $1.60,
CPT $0.87) fall inside those bounds — a second vendor, same-year,
different-sample corroboration that Italy is a cheap ASA market, though
the absolute $1.60/$0.87 levels remain single-vendor.

Context anchors (2025): top-15 average CPT $1.60 → $2.90 and CPA $2.47 →
$4.60 YoY (steep premium-market inflation); most expensive: UK CPA $5.46
/ CPT $3.65, Canada $5.23/$3.36, US $5.15/$3.26; Europe region monthly
averages CPT ~$1.50–1.87 and CPA ~$2.30–2.86, the mid-cost tier between
NA and LATAM/AMEI; France = the cheap stable big market (CPA $2.10–2.80).
NA cost curve spikes in September (NFL season), troughs in April. Dated
fact from the public pages: **a second search-results ad placement
launches March 2026** — the biggest Apple Ads inventory change since
Today Tab; expect CPT dynamics to shift after it.

## Consequences applied to the packs (2026-08-16)

1. `b2c/retention.md` + `b2c/cac.md` (coupled): published-median floor
   restated as **2–7% D30** with Adjust 2026 per-vertical anchors
   (gaming 5, e-commerce 3, finance 2; marketplace 8) and dated sourcing.
2. `b2c/pricing.md`: freemium section gains the AppsFlyer 2026 sourced
   per-category conversion block (trial and no-trial funnels).
3. `b2c/cac.md`: cross-channel row gains the Adjust Europe CPI cut.
4. The retention-divergence question is CLOSED: no primary source for a
   subscription-app D30 premium exists, gated or open. The pack's
   well-executed-band framing stays.

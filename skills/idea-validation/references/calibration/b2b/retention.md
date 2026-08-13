# Retention — B2B calibration (Italy-first, self-serve micro-SaaS)

Loaded by `iv-retention` via the CALIBRATION path in its dispatch prompt.
Defines the stickiness factor anchors, churn benchmarks, churn-risk library,
and verdict thresholds for the Italian B2B target. The scoring mechanics
live in the agent brief.

B2B retention is workflow embedding, not habit formation: the question is
whether the tool becomes part of how the business operates, so that
cancelling it would break something.

> Sources: churn/NRR tables are global — ChartMogul (2,500+ SaaS businesses;
> churn page current 2026) and SaaS Capital RB32 (2025, n>1,000, excludes
> <$1M ARR). No Italy-specific churn dataset exists (say so if asked);
> price-band churn is a price construct, not a geography construct, so the
> global tables apply. `confidence: high` on the churn-by-ARPA table;
> `medium` on activation (Lenny's 2022 — stale, directional).

## Stickiness Factor Anchors (workflow embedding)

Score each schema factor 1–5 against these B2B interpretations:

| Factor (schema key) | 5 (high retention signal) | 1 (low retention signal) |
|---|---|---|
| Usage frequency (`usage_frequency`) | The workflow recurs daily or per-transaction (every order, every fattura, every pratica) | Recurs quarterly or less (annual filing, one-off migration) |
| External trigger (`external_trigger`) | A business event forces every use (order placed, scadenza, client onboarded) | Nothing prompts usage; someone must remember the tool exists |
| Progress/reward loop (`progress_reward_loop`) | The tool visibly re-earns its cost every cycle (recovered revenue counter, hours-saved report, delivered client artifact) | Value is invisible after setup; at renewal nobody remembers why they pay |
| Network effects (`network_effects`) | Value grows with seats/collaborators/client firms attached; the team or studio works IN the tool | Single-player utility; no one else ever sees it |
| Data lock-in (`data_lock_in`) | Business records accumulate (client history, configurations, integrations wired into the gestionale) | Nothing stored that would hurt to lose; switch costs one afternoon |
| Habit stack (`habit_stack`) | Slots into an existing operating routine or fires automatically inside the stack (wired to the incumbent suite via integration) | Requires the business to adopt a new process around the tool |

In B2B mode read `habit_formation_score` as a **workflow-embedding score**.

## Churn Benchmarks by Price Band

Monthly customer (logo) churn by ARPA, from ChartMogul (2,500+ SaaS
businesses; https://chartmogul.com/saas-metrics/customer-churn/). Read the
€ bands as ≈ the $ bands — the construct is price-level, not currency:

| ARPA/mo | Best-in-class | Good | Median | Weak |
|---|---|---|---|---|
| < $25 (~€25) | 2.5% | 4.0% | 6.1% | 9.3% |
| $25–100 | 1.7% | 2.8% | 4.2% | 7.4% |
| $100–250 | 1.4% | 1.9% | 3.1% | 5.8% |
| $250–500 | 1.0% | 1.9% | 3.0% | 4.7% |

Price point, not vertical, drives the variation (ChartMogul's explicit
conclusion) — pick the row from the idea's likely price, not its category.

**Position within the row:**
- "Good" column: `habit_formation_score` ≥ 4.0 AND `desire_strength_label` = "strong"
- "Weak" column: `habit_formation_score` < 2.5 OR `desire_strength_label` = "weak"
- "Median" otherwise; "Best-in-class" is aspirational — never a pre-launch estimate.

Then shift one column better if the primary demand driver is pain-frequency
or ROI-provability; one column worse if it is urgency (once the scadenza
passes, the canone gets questioned).

**Italian billing-cycle note:** annual-with-fattura is the native rhythm
(pricing pack), so much churn is invisible until renewal. When the plan mix
skews annual, model churn as an annual renewal decision (monthly-equivalent
for the math, but flag that early usage decay won't show in revenue until
month 12) — and weight the `progress_reward_loop` factor accordingly: the
tool must be able to justify itself at a once-a-year scrutiny moment.

## Filling the Schema's `estimated_retention` Block

The shared schema's `d1/d7/d30` fields carry B2B semantics — also write an
`estimated_retention_semantics` string field stating them:

- `d1` = **activation rate**: % of signups reaching the activation milestone. Benchmarks: median 25% all products / 30% B2B; ≥ 60% is top-decile (Lenny's Newsletter, 500+ products, 2022 — stale, directional).
- `d7` = **month-1 logo retention** of paying customers = 100 − monthly churn from the table above.
- `d30` = **month-3 logo retention** = (month-1 retention ÷ 100)^3 × 100 — e.g. 97% month-1 → 91.3%. Cross-check: top-quartile 3-month new-customer retention is 98% at ASP > $500/mo vs 87% at < $10/mo (ChartMogul Retention Report, 2023).

The CAC specialist's B2B pack derives customer lifespan from these exact
semantics — keep them.

## Expansion Note (feeds LTV downstream)

Do not assume expansion revenue: median NRR in ChartMogul's
self-serve-skewed B2B sample is **82%** (top quartile 97%; data through Sep
2025) — that is the right expectation at indie scale. The up-market gradient
for context (SaaS Capital 2025, excludes <$1M ARR): median NRR 98% at <$12K
ACV rising to 106% above $250K; bootstrapped companies 104%/92% GRR. Sub-100%
NRR is the norm for micro-SaaS — LTV comes from lifespan, not account
growth. Exception worth modeling: studio-side tools that bill per azienda
gestita have a real expansion axis (the studio adds clients) — cite evidence
before claiming it.

## Churn Risk Factor Library

Check the concept against this library and list every factor that applies:

- **No workflow embedding** — consulted occasionally, not operated in; nothing breaks if cancelled
- **Activation cliff** — value requires integration/setup work most signups never finish (median activation ~25–30%)
- **One-shot value** — the job completes (migration, cleanup, audit, adempimento una tantum) and the need ends
- **Free-alternative gravity** — the incumbent suite's included module, a spreadsheet, or the platform's native feature is good enough for the median buyer ("già incluso")
- **Champion dependency** — one person championed the purchase; when they leave or lose interest, the account churns
- **Invisible ROI at renewal** — works silently; at fattura-renewal scrutiny nobody can say what it did
- **Scadenza-bound usage** — bought for a deadline or season (dichiarazioni, tax season, holiday commerce); boom-bust revenue and post-deadline cancellations
- **Canone resentment** — the niche shows subscription-resistance sentiment; renewals face "perché pago ancora?" pressure regardless of value (see pricing pack's one-time option)
- **Intermediary concentration** — accounts arrived through commercialisti/consulenti/resellers; if the intermediary switches recommendation, whole portfolios churn at once
- **Platform absorption** — the incumbent suite or host platform is likely to ship the feature natively

## Verdict Thresholds

- **sticky** if projected monthly logo churn ≤ 3% and `habit_formation_score` ≥ 3.5
- **disposable** if projected monthly logo churn ≥ 7% or `habit_formation_score` < 2.0
- **moderate** otherwise

(Thresholds anchored to the ChartMogul table: ≤ 3% sits at/above "good" for
the $25–100 band; ≥ 7% sits in "weak" territory for every band ≥ $25.)

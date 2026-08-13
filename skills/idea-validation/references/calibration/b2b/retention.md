# Retention — B2B calibration (self-serve / PLG micro-SaaS)

Loaded by `iv-retention` via the CALIBRATION path in its dispatch prompt.
Defines the stickiness factor anchors, churn benchmarks, churn-risk library,
and verdict thresholds for the B2B target. The scoring mechanics live in the
agent brief.

B2B retention is workflow embedding, not habit formation: the question is
whether the tool becomes part of how the business operates, so that
cancelling it would break something.

> Sources: churn and NRR tables are from ChartMogul's published benchmarks
> (2,500+ SaaS businesses; churn page current as of 2026, NRR detail 2023 —
> flagged) and SaaS Capital (2025). Activation benchmark is Lenny's
> Newsletter (2022 — flagged stale; no newer comparable study exists).
> `confidence: high` on the churn-by-ARPA table (single source but the only
> granular published cut, corroborated directionally by SaaS Capital);
> `confidence: medium` on activation.

## Stickiness Factor Anchors (workflow embedding)

Score each schema factor 1–5 against these B2B interpretations:

| Factor (schema key) | 5 (high retention signal) | 1 (low retention signal) |
|---|---|---|
| Usage frequency (`usage_frequency`) | The workflow recurs daily or per-transaction (every order, every ticket) | Recurs quarterly or less (annual filing, one-off migration) |
| External trigger (`external_trigger`) | A business event forces every use (order placed, month-end close, client onboarded) | Nothing prompts usage; someone must remember the tool exists |
| Progress/reward loop (`progress_reward_loop`) | The tool visibly re-earns its cost every cycle (recovered revenue counter, hours-saved report, delivered client artifact) | Value is invisible after setup; at renewal nobody remembers why they pay |
| Network effects (`network_effects`) | Value grows with seats/collaborators; the team works IN the tool | Single-player utility; no one else ever sees it |
| Data lock-in (`data_lock_in`) | Business records accumulate (client history, configurations, integrations wired into other systems) | Nothing stored that would hurt to lose; switch costs one afternoon |
| Habit stack (`habit_stack`) | Slots into an existing operating routine or is wired in via integrations (fires automatically inside the stack) | Requires the business to adopt a new process around the tool |

`habit_formation_score` = mean of the six factor scores, one decimal (1.0–5.0). In B2B mode read it as a **workflow-embedding score**.

## Churn Benchmarks by Price Band

Monthly customer (logo) churn by ARPA, from ChartMogul (2,500+ SaaS businesses; https://chartmogul.com/saas-metrics/customer-churn/):

| ARPA/mo | Best-in-class | Good | Median | Weak |
|---|---|---|---|---|
| < $25 | 2.5% | 4.0% | 6.1% | 9.3% |
| $25–100 | 1.7% | 2.8% | 4.2% | 7.4% |
| $100–250 | 1.4% | 1.9% | 3.1% | 5.8% |
| $250–500 | 1.0% | 1.9% | 3.0% | 4.7% |

Price point, not vertical, drives the variation (ChartMogul's explicit conclusion across category cuts, data through Sep 2025) — pick the row from the idea's likely price, not its category.

**Position within the row:**
- "Good" column: `habit_formation_score` ≥ 4.0 AND `desire_strength_label` = "strong"
- "Weak" column: `habit_formation_score` < 2.5 OR `desire_strength_label` = "weak"
- "Median" column otherwise; "Best-in-class" is aspirational — never a pre-launch estimate.

Then shift one column better if the primary demand driver is pain-frequency or ROI-provability (the tool re-earns its keep every cycle); one column worse if it is urgency (once the deadline passes, the subscription gets questioned).

## Filling the Schema's `estimated_retention` Block

The shared schema's `d1/d7/d30` fields carry B2B semantics — also write an `estimated_retention_semantics` string field stating them:

- `d1` = **activation rate**: % of signups reaching the activation milestone. Benchmarks: median 25% all products / 30% B2B; ≥ 60% is top-decile (Lenny's Newsletter, 500+ products, 2022 — stale, directional).
- `d7` = **month-1 logo retention** of paying customers = 100 − monthly churn from the table above.
- `d30` = **month-3 logo retention** = (month-1 retention)^3, in percent. Cross-check: top-quartile 3-month new-customer retention is 98% at ASP > $500/mo vs 87% at < $10/mo (ChartMogul Retention Report, 2023).

The CAC specialist's B2B pack derives customer lifespan from `d30` under exactly these semantics — keep them.

## Expansion Note (feeds LTV downstream)

Do not assume expansion revenue: median NRR in ChartMogul's self-serve-skewed B2B sample is **82%** (top quartile 97%; data through Sep 2025). Sub-100% NRR is the norm for micro-SaaS, not a red flag — but it means LTV comes from lifespan, not from account growth. Only 2.7% of businesses at < $10/mo ARPA exceed 100% NRR vs 41.1% at > $500/mo (ChartMogul, 2023).

## Churn Risk Factor Library

Check the concept against this library and list every factor that applies:

- **No workflow embedding** — the tool is consulted occasionally, not operated in; nothing breaks if cancelled
- **Activation cliff** — value requires integration/setup work most signups never finish (median activation is only ~25–30%)
- **One-shot value** — the job completes (migration, cleanup, audit) and the need ends
- **Free-alternative gravity** — the platform's native feature or a spreadsheet is good enough for the median buyer
- **Champion dependency** — one person championed the purchase; when they leave or lose interest, the account churns
- **Invisible ROI at renewal** — the tool works silently; at price-scrutiny time nobody can say what it did
- **Seasonal or event-bound usage** — tax season, holiday commerce, annual events; boom-bust revenue
- **Goal completion exit** — reaching compliance/launch/cleanup ends the need
- **Platform absorption** — the host platform is likely to ship the feature natively

**`churn_risk`:** high if 3+ factors apply or `habit_formation_score` < 2.5; low if ≤ 1 factor applies and `habit_formation_score` ≥ 4.0; medium otherwise.

## Verdict Thresholds

- **sticky** if projected monthly logo churn ≤ 3% and `habit_formation_score` ≥ 3.5
- **disposable** if projected monthly logo churn ≥ 7% or `habit_formation_score` < 2.0
- **moderate** otherwise

(Thresholds anchored to the ChartMogul table: ≤ 3% sits at/above "good" for the $25–100 band; ≥ 7% sits in "weak" territory for every band ≥ $25.)

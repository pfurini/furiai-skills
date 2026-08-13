# Demand drivers — B2B calibration (Italy-first, self-serve micro-SaaS)

Loaded by `iv-desire-evaluator` via the CALIBRATION path in its dispatch
prompt. Defines the driver set, what each measures, and the derived-signal
rules for the Italian B2B target. The scoring mechanism lives in the agent
brief.

Business buying is pain-driven, not desire-driven: the question is not "does
the user crave this?" but "does this pain recur, cost real money, and sit
with someone who can buy the fix without asking permission?"

> Confidence: the driver constructs are standard B2B buying frameworks with
> no numeric benchmarks (`confidence: medium` pending forward-testing). The
> Italian buying-culture notes are grounded in the 2026-08 research pack
> (pricing pages, purchase-process evidence) — treat them as strong priors,
> not laws.

## Driver Set

The driver NAMES are load-bearing — the pricing pack's multiplier table is
keyed to them. Do not rename.

| Dimension | What it measures | Score-5 looks like | Score-1 looks like | Italian example |
|---|---|---|---|---|
| Pain frequency | How often the pain recurs in the operator's workflow | Hits daily or every transaction | Hits once a year | Re-keying every order into the gestionale vs. the annual bilancio |
| Pain severity | What it costs when it hits (hours, lost revenue, risk) | Measurable money lost or compliance exposure every occurrence | Mild annoyance, no measurable cost | A missed scadenza fiscale (sanzioni) vs. an ugly export |
| Budget authority | Whether the person feeling the pain can buy the fix themselves | Titolare/owner with a company card, price under the no-approval threshold (**~€50/mo ex-VAT** for Italian micro-firms and studi) | End user must convince a department head, or the firm defers to its commercialista's advice | A freelancer buying a €19/mo tool vs. an impiegato requesting a €500/mo platform |
| Urgency | External pressure to fix it now | A normative deadline (nuovo obbligo, scadenza), platform change, or growth bottleneck forcing action this quarter | "Someday" improvement with no forcing function | A new fatturazione/reporting obbligo vs. nicer dashboards |
| ROI provability | How easily the buyer can see the tool paying for itself | Tool visibly saves hours or recovers money within the first billing cycle | Value is diffuse, delayed, or unmeasurable | Recovered-revenue counter vs. "better collaboration" |

Anchor every score to evidence: operator vocabulary from Italian
market_insights narratives ("perdiamo X ore a settimana", "pagherei per non
farlo più"), the cost of the manual alternative, and who is speaking
(titolare vs. dipendente vs. the studio that manages the firm).

## Italian buying-culture adjustments (apply while scoring, cite when used)

- **Delegation check**: if community threads answer the pain with "lo fa il
  commercialista / il consulente", the pain is real but the budget may sit
  with the intermediary. Score budget-authority from the INTERMEDIARY's
  perspective and flag it — downstream, market-sizing redirects the buyer
  and distribution models the intermediary as a channel.
- **Subscription resistance**: Italian micro-firm culture resents recurring
  costs more than Anglophone markets; a pain that clears the bar for a
  one-time purchase may not clear it for a subscription. Note when evidence
  shows "one-time yes, canone no" sentiment — it feeds the pricing model
  choice.
- **Urgency is normative in Italy**: the strongest urgency signals are
  regulatory (obblighi, scadenze) rather than competitive. Score-5 urgency
  almost always cites a norm with a date. Remember the retention warning:
  deadline-driven purchases churn after the deadline (retention pack).

## Derived Signals

**`virality_potential`** (here: peer-advocacy potential): **high** if the
tool's output is routinely shown to clients or peers (client portals,
delivered reports, invoices with branding) or the buyer belongs to tight
Italian peer communities where recommendations circulate (ordini and their
local sections, category associations, active vertical forums/groups);
**medium** if it spreads inside a team but has no outward-facing artifact;
**low** if usage is solitary and invisible. In professional verticals,
factor the ordine's density: 100% of commercialisti are enrolled in an albo
with local events — a strong advocacy lattice when the tool earns it.

## Downstream Feeds

- `primary_driver` and `desire_strength_label` feed the pricing specialist's premium multiplier (its B2B pack keys the multiplier table to these driver names).
- `virality_potential` feeds distribution analysis (referral/peer-advocacy loop assessment).
- The retention specialist reads these scores: pain-frequency and ROI-provability as primary drivers push retention up (the tool re-earns its keep every cycle); urgency as primary pushes it down (once the scadenza passes, the canone is questioned).
- The delegation flag (above) feeds market-sizing's buyer-redirection step and the distribution pack's intermediary channel.

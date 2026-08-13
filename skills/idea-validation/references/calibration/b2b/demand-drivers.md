# Demand drivers — B2B calibration (self-serve / PLG micro-SaaS)

Loaded by `iv-desire-evaluator` via the CALIBRATION path in its dispatch
prompt. Defines the driver set, what each measures, and the derived-signal
rules for the B2B target. The scoring mechanism lives in the agent brief.

Business buying is pain-driven, not desire-driven: the question is not "does
the user crave this?" but "does this pain recur, cost real money, and sit
with someone who can buy the fix without asking permission?"

> Confidence: the driver constructs below are grounded in standard B2B
> buying frameworks; they carry no numeric benchmarks. `confidence: medium`
> pending forward-testing.

## Driver Set

| Dimension | What it measures | Score-5 looks like | Score-1 looks like | Example |
|---|---|---|---|---|
| Pain frequency | How often the pain recurs in the operator's workflow | Hits daily or every transaction | Hits once a year | Inventory sync errors on every order vs. annual license renewal |
| Pain severity | What it costs when it hits (hours, lost revenue, risk) | Measurable money lost or compliance exposure every occurrence | Mild annoyance, no measurable cost | Failed client report loses the client vs. an ugly export |
| Budget authority | Whether the person feeling the pain can buy the fix themselves | Owner/solo operator with a company card, price under their no-approval threshold | End user must convince a department head and procurement | Freelancer buying a $19/mo tool vs. employee requesting a $500/mo platform |
| Urgency | External pressure to fix it now | Regulation deadline, platform change, or growth bottleneck forcing action this quarter | "Someday" improvement with no forcing function | New tax-reporting rule vs. nicer dashboards |
| ROI provability | How easily the buyer can see the tool paying for itself | Tool visibly saves hours or recovers revenue within the first billing cycle | Value is diffuse, delayed, or unmeasurable | Cart-recovery app showing recovered $ vs. "better collaboration" |

Anchor every score to evidence: operator vocabulary in community/review
narratives ("we lose X hours a week", "I'd pay for anything that fixes
this"), the cost of the manual alternative, and who in the thread is
speaking (owner vs. employee).

## Derived Signals

**`virality_potential`** (here: peer-advocacy potential): **high** if the
tool's output is routinely shown to colleagues, clients, or peers
(client-facing reports, shared workspaces, public badges) or the buyer
belongs to tight peer communities where tool recommendations circulate
(agency owners, niche operator groups); **medium** if the tool spreads
inside a team through collaboration but has no outward-facing artifact;
**low** if usage is solitary and invisible.

## Downstream Feeds

- `primary_driver` and `desire_strength_label` feed the pricing specialist's premium multiplier (its B2B pack keys the multiplier table to these driver names).
- `virality_potential` feeds distribution analysis (referral/collaboration loop assessment).
- The retention specialist reads these scores: pain-frequency and ROI-provability as primary drivers push retention up (the tool re-earns its keep every cycle); urgency as primary pushes it down (once the deadline passes, the subscription is questioned).

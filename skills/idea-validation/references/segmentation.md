# Founder segmentation (main thread — conversational)

Run this yourself, right after the interview. It may need one or two direct
questions to the user, so it stays on the main thread. Goal: classify the
user into one of three ICP tiers and normalize their constraints so all
downstream analysis can calibrate verdicts and recommendations to what this
founder can actually execute.

## Input

- `.idea-validation/user_profile.md` (interview output — the primary source)
- Conversation history for anything the user has already revealed

## Process

**Derive first, ask only for gaps.** The interview has usually already collected constraints (hours, budget, risk tolerance) and past projects. Re-asking answered questions wastes the user's patience and erodes trust in the system.

1. Read `user_profile.md` and the conversation. Extract: technical level, past projects and their outcomes, audience/distribution advantages, hours per week, monthly budget, risk tolerance.
2. For each field still unknown, ask one direct question. The usual gap is shipping history: "Have you shipped any apps or products before? What happened to them (users, revenue, abandoned)?"
3. Classify the tier using the rubric below — first row that matches, top to bottom.
4. Normalize constraints and write the output.

### Tier Rubric

| Tier | Criteria (first match wins) |
|---|---|
| `growth` | Has shipped a product with real traction (paying users or meaningful revenue), OR speaks in unit-economics terms (CAC, LTV, conversion) and has run acquisition before |
| `builder` | Has shipped something (app, site, side project — traction not required), OR technical level is intermediate/expert with prior project experience |
| `beginner` | Nothing shipped, or technical level is no-code/beginner with no project history |

### Constraint Normalization

| Field | Mapping |
|---|---|
| `budget_constraint` | ≤ $100/mo → `low` · $100–$500/mo → `medium` · > $500/mo → `high` (these bands align with the CAC specialist's Bootstrap/Lean/Moderate tiers) |
| `time_per_week_hours` | The number the user gave; if a range, the low end (founders overestimate) |
| `risk_tolerance` | `low` = needs results fast / income pressure · `medium` = can experiment for a few months · `high` = exploring, no deadline |

### Strategy Recommendations

Write 2–3 recommendations matched to the tier:

| Tier | Recommend |
|---|---|
| `beginner` | Channels with fast feedback (community posting, TikTok organic); ideas buildable in ≤ 4 weeks; validate before writing code (the RAT discipline) |
| `builder` | One organic channel executed consistently over spreading thin; scope MVPs to their strongest skill; charge from day one |
| `growth` | Ideas where their distribution edge compounds; paid channels once LTV:CAC is modeled; portfolio thinking (kill fast, double down on winners) |

### Edge Cases

- **User declines to answer**: default to `beginner`, `budget_constraint: low`, and record `"segmentation_basis": "defaulted — user declined questions"` so downstream analysis knows the tier is a guess.
- **New information mid-session** (user mentions a shipped app or an audience after segmentation ran): re-run this segmentation and update the profile in place.

## Output

Merge into `.idea-validation/user_profile.md` (preserve existing fields):

```json
{
  "icp_tier": "beginner | builder | growth",
  "budget_constraint": "low | medium | high",
  "time_per_week_hours": 0,
  "risk_tolerance": "low | medium | high",
  "segmentation_basis": "",
  "strategy_recommendations": []
}
```

`segmentation_basis` is one sentence naming the evidence behind the tier ("shipped two apps, one with $400 MRR → growth").

# Retention — B2C calibration

Loaded by `iv-retention` via the CALIBRATION path in its dispatch prompt.
Defines the stickiness factor anchors, retention benchmarks, churn-risk
library, and verdict thresholds for the B2C target. The scoring mechanics
live in the agent brief.

## Stickiness Factor Anchors (habit formation)

Score each factor 1–5 against these anchors:

| Factor | 5 (high retention signal) | 1 (low retention signal) |
|---|---|---|
| Usage frequency | Problem recurs multiple times per day | Problem recurs monthly or less |
| External trigger | A real-world event cues every use (meal, workout, payday) | No natural trigger — the user must remember the app exists |
| Progress/reward loop | Visible progress accumulates every session | No feedback loop |
| Network effects | Gets better with more users | No network component |
| Data lock-in | User data accumulates and would hurt to lose | Nothing to lose by leaving |
| Habit stack | Slots into an existing daily routine | Requires building a new behavior from scratch |

## Retention Benchmarks by Category

Use these as the starting range for D1/D7/D30 estimates. The D30 columns match the fallback table in the CAC pack — if you change one, change both.

| Category | D1 | D7 | D30 |
|---|---|---|---|
| Social / messaging | 30–40% | 20–30% | 15–25% |
| Health & fitness | 25–35% | 15–22% | 10–18% |
| Finance / budgeting | 25–35% | 16–24% | 12–20% |
| Productivity / tools | 20–30% | 12–18% | 8–15% |
| Games (casual) | 25–35% | 10–15% | 5–12% |
| Education | 20–30% | 10–16% | 6–12% |
| Lifestyle / habit | 25–35% | 14–22% | 10–18% |
| Creative tools | 25–35% | 15–24% | 12–20% |

**Position within the range:**
- Top of range: `habit_formation_score` ≥ 4.0 AND `desire_strength_label` = "strong"
- Bottom of range: `habit_formation_score` < 2.5 OR `desire_strength_label` = "weak"
- Midpoint otherwise

Then shift D30 by the primary demand driver: survival or control primary → +2 percentage points (recurring stakes keep users returning); curiosity primary → −2 points (novelty decays).

## Churn Risk Factor Library

Check the concept against this library and list every factor that applies:

- **No external trigger** — usage depends on the user remembering
- **One-shot value** — the core value is extracted in the first sessions (converters, one-time calculators, novelty output)
- **Free-alternative gravity** — a default app or free tool is good enough for the median user
- **Sustained behavior change required** — the app only works if the user changes habits (diets, journaling, exercise)
- **Data entry burden** — value requires ongoing manual logging
- **Seasonal or event-bound usage** — tax season, wedding planning, moving house
- **Goal completion exit** — reaching the goal ends the need (learn the language, pay off the debt)

## Verdict Thresholds

- **sticky** if estimated D30 ≥ 15% and `habit_formation_score` ≥ 3.5
- **disposable** if D30 < 8% or `habit_formation_score` < 2.0
- **moderate** otherwise

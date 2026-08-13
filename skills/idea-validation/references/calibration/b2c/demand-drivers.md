# Demand drivers — B2C calibration

Loaded by `iv-desire-evaluator` via the CALIBRATION path in its dispatch
prompt. Defines the driver set, what each aggregates, and the derived-signal
rules for the B2C target. The scoring mechanism lives in the agent brief.

## Driver Set

Read `core-human-desires.md` (in this same directory) before scoring — it
defines the ten underlying desires the five dimensions aggregate.

| Dimension | Description | Aggregates (from core-human-desires.md) | Example App |
|---|---|---|---|
| Survival | Health, safety, financial security | 1 Survival & Physical Security, 2 Pain Avoidance | Calorie tracker, budgeting app |
| Status | Looking good, achieving, being seen | 4 Status & Recognition, 8 Identity & Self-Consistency | Fitness leaderboard, portfolio tracker |
| Belonging | Community, connection, not being alone | 3 Social Belonging | Group savings, running clubs |
| Control | Mastery, autonomy, reducing chaos | 5 Control & Autonomy, 6 Competence & Progress | Task manager, habit tracker |
| Curiosity | Learning, discovery, novelty | 9 Novelty & Curiosity, 7 Meaning & Purpose | Language app, quiz game |

## Derived Signals

**`virality_potential`**: **high** if status or belonging scores ≥ 4 (social
desires are what make users show the app to others); **medium** if status or
belonging = 3, or curiosity ≥ 4 and the app produces shareable output;
**low** otherwise.

## Downstream Feeds

- `primary_driver` and `desire_strength_label` feed the pricing specialist's premium multiplier (its calibration pack keys the multiplier table to these driver names).
- `virality_potential` feeds distribution analysis.
- The retention specialist reads these scores: survival and control as primary drivers push retention estimates up (recurring stakes), curiosity as primary pushes them down (novelty decays).

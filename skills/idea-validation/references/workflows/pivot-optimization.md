---
name: pivot-optimization
entry_condition: ".idea-validation/ideas/<slug>/scores.json must exist"
exit_output: ".idea-validation/ideas/<slug>/pivot_options.json + pivot_report.md + pivot_scores.json"
---

# Workflow: Pivot Optimization

## Startup Announcement

When this workflow is triggered, **immediately** say this before doing anything else:

> **🔄 Starting: Pivot Optimization**
> I'll dig into why your idea scored the way it did, identify the root causes of weak dimensions, and generate concrete pivot options — each with a projected score improvement and effort estimate.

## Entry Conditions

- `.idea-validation/ideas/<slug>/scores.json` must exist — full validation only; a `screening_scores.json` alone does not qualify. If missing, say the idea has no full validation yet and offer the **idea-validation** workflow.
- User specifies which idea (slug or name). If several scored ideas exist, list them and ask.

## Chain

Sequential — each step reads the previous step's artifact, so there is nothing to parallelize.

```
1. Re-read scores — main thread
   Read scores.json and the dimension files; confirm scores.json is current
   (re-score via references/scoring.md if dimension files changed since).
   → present: Current score (X/100), verdict, weakest dimensions.

2. Weakness diagnosis — single agent
   ↓ dispatch: iv-weakness
   ↓ reads: scores.json + dimension files + related market_insights
   ↓ writes: .idea-validation/ideas/<slug>/weaknesses.json
   → present: 2–3 weakest dimensions, root causes, most critical failure mode.

3. Pivot generation — single agent
   ↓ dispatch: iv-pivot-engine (pass the path to references/scoring.md for projections)
   ↓ reads: weaknesses.json, scores.json, idea.md, other dimension files,
            user_profile.md, market_insights, references/scoring.md
   ↓ writes: .idea-validation/ideas/<slug>/pivot_options.json + pivot_report.md
   → present: Full pivot_report.md inline.

4. Re-score recommended pivot — main thread
   Read references/scoring.md now and re-score the recommended variant yourself
   (existing dimension files, adjusted for the pivot; include pivot_id).
   ↓ writes: .idea-validation/ideas/<slug>/pivot_scores.json
   → present: Projected score vs original, and whether it reaches the "test"
     band (55+). File: pivot_scores.json
```

## Exit Output

- `.idea-validation/ideas/<slug>/pivot_report.md`
- `.idea-validation/ideas/<slug>/pivot_options.json`
- `.idea-validation/ideas/<slug>/pivot_scores.json`

If the recommended pivot scores ≥ 55 (the "test" band) → suggest full **idea-validation** on a **new** idea slug for the variant.

If the recommended pivot still scores < 35 (the "drop" band) → recommend dropping (`status: dropped` in `idea.md`; do not delete the directory).

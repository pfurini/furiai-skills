---
name: idea-generation
entry_condition: ".idea-validation/user_profile.md may not exist"
exit_output: ".idea-validation/ideas/<slug>/screening_scores.json"
---

# Workflow: Idea Generation

## Startup Announcement

When this workflow is triggered, **immediately** say this before doing anything else:

> **💡 Starting: Idea Generation**
> I'll help you find an app idea worth building. We'll cover your background, explore trending markets, and surface the best opportunities for you specifically.

## Chain

```
1. Interview — main thread, conversational
   Read references/interview.md now and run it yourself.
   ↓ writes: .idea-validation/user_profile.md
   ↓ ALWAYS runs first, even if user_profile.md exists — the reference itself
   |   handles existing-profile reuse (use / update / browse) and mode selection.
   ↓ route by the resulting interview_mode (for a reused profile, its stored mode):
   |     full or fast → step 2
   |     browse or skipped → step 3, skipping segmentation; default icp_tier = "beginner"
   → present: Strong domains, distribution advantages, inner circle, constraints.
     If browsed: the selected domains. If skipped: note results will be generic.

2. Segmentation — main thread
   Read references/segmentation.md now and run it yourself.
   ↓ reads: .idea-validation/user_profile.md
   ↓ writes: .idea-validation/user_profile.md (adds icp_tier, constraints)
   → present: ICP tier (beginner/builder/growth) and top strategy recommendations.

3. Trend research — fan-out wave
   ↓ browse mode → selected_interest_domains are the niches. Otherwise infer the
   |   niche from the profile or existing insights and confirm with the user.
   ↓ Determine the target (b2c | b2b) from the confirmed niche per SKILL.md —
   |   consumer-life niches → b2c; operator/business niches → b2b. Candidates
   |   generated in step 4 inherit it in their idea.md frontmatter.
   ↓ Ask which platforms (see the target's trend platform menu in SKILL.md).
   |   Apply the freshness check first.
   ↓ dispatch: iv-trend-researcher × one per selected platform × per niche,
   |   all in one message, in background
   ↓ writes: .idea-validation/market_insights/<niche>-<platform>-<YYYY>-<MM>.md (one per dispatch)
   → present: Top 3 signals per platform, velocity, verdict (hot/warm/cool/cold).

4. Idea mapping — single agent
   ↓ dispatch: iv-idea-mapper with the confirmed niche(s)
   ↓ reads: user_profile.md, market_insights/<niche>-*
   ↓ writes: .idea-validation/ideas/<slug>/idea.md (5–10 candidates)
   → present: Summary table (slug, concept, confidence, cross-platform resonance, monetization).

5. Screening — main thread
   Read references/scoring.md (Screening Mode section) now and score the candidates yourself.
   ↓ reads: each candidate's idea.md frontmatter
   ↓ writes: .idea-validation/ideas/<slug>/screening_scores.json (one per candidate)
   → present: Ranked candidate table with screening scores and
     validate / consider / deprioritize recommendations.
```

## Exit Output

- Candidates ranked by `screening_score`, each with its recommendation
- Top recommendation with rationale
- File list:

  ```
  📄 .idea-validation/ideas/<slug-1>/idea.md  (screening: XX/100 — validate)
  📄 .idea-validation/ideas/<slug-2>/idea.md  (screening: XX/100 — consider)
  ...
  ```

- Prompt to run the **idea-validation** workflow on the chosen idea. Screening is a ranking of trend evidence, not a validation — say so.

## Notes

- The user can say "run the interview" later; re-run the interview, then any downstream steps that depend on the profile.

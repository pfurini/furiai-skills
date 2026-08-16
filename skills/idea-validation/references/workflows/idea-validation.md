---
name: idea-validation
entry_condition: "User has stated a concrete idea"
exit_output: ".idea-validation/ideas/<slug>/decision_memo.md"
---

# Workflow: Idea Validation

## Startup Announcement

When this workflow is triggered, **immediately** say this before doing anything else:

> **🔍 Starting: Idea Validation**
> I'll run a full validation on your idea across demand, competition, monetization, distribution, retention, and founder fit — and give you a scored verdict with a concrete next step.

## Entry Conditions

1. Derive slug: kebab-case from idea name, max 40 chars.
2. Create `.idea-validation/ideas/<slug>/` if needed.
3. Write `.idea-validation/ideas/<slug>/idea.md` with the raw idea (`status: in-validation`, and the `target` field per SKILL.md) before the chain, unless it already exists.
4. **b2b only:** infer the sales-motion band (self-serve / assisted self-serve / sales-led, per SKILL.md), state it in the Startup Announcement, and write `sales_motion: self-serve | assisted-self-serve | sales-led` into `idea.md` frontmatter. Sales-led: say plainly that desk research cannot validate this segment before offering to continue.
5. Apply the market_insights freshness check for this niche. Ask the user which platforms to research (or reuse fresh files); see the target's trend platform menu in SKILL.md.

## Wave Plan

```
Wave 1 — evidence
  iv-trend-researcher × one per selected platform (skip platforms with fresh files the user kept)
    reads: platform prompt from references/prompts/<platform>.md; niche from idea.md
    writes: .idea-validation/market_insights/<niche>-<platform>-<YYYY>-<MM>.md
  → present: Top 3 signals per platform, velocity, verdict. Full analysis at the written paths.

Wave 2 — landscape (independent given Wave 1)
  iv-competitor-mapper
    reads: idea.md, market_insights/<niche>-*
    writes: ideas/<slug>/competitors.json
  iv-desire-evaluator
    reads: idea.md, market_insights/<niche>-*, its calibration pack
    writes: ideas/<slug>/desire_scores.json
  iv-distribution
    reads: user_profile.md (if present), idea.md, market_insights/<niche>-*
    writes: ideas/<slug>/distribution.json
  → present: Top 3 direct competitors (pricing + top complaint) and saturation; primary desire
    driver, strength label, virality; distribution verdict, first channel, viral loop yes/no.

Wave 3 — economics inputs (need Wave 2)
  iv-pricing-wtp
    reads: idea.md, competitors.json, desire_scores.json, market_insights
    writes: ideas/<slug>/pricing.json
  iv-retention
    reads: idea.md, desire_scores.json
    writes: ideas/<slug>/retention.json
  → present: Pricing model, target WTP range, freemium conversion; retention verdict,
    usage frequency, top churn risk.

Wave 4 — unit economics (needs Wave 3)
  iv-cac-modeler
    reads: user_profile.md (if present), pricing.json, retention.json, distribution.json,
           competitors.json, market_insights
    writes: ideas/<slug>/cac.json
  iv-market-sizer   (b2b: DEFAULT — the b2b Monetization top band requires a sized, viable SOM;
                     b2c: dispatch only when the user asks for market size)
    reads: idea.md, competitors.json, pricing.json, market_insights
    writes: ideas/<slug>/market_size.json
  → present: Viability verdict, LTV:CAC for the recommended channel, payback months;
    market-size verdict and SOM year 1 when the sizer ran.

Synthesis — main thread
  Score: Read references/scoring.md now and score the idea yourself.
    writes: ideas/<slug>/scores.json
  → present: Final score (X/100), verdict, top strength, top weakness.
  Memo: Read references/decision-memo.md now and write the memo yourself.
    writes: ideas/<slug>/decision_memo.md
  → present: The complete decision memo inline.
```

After the memo, set `idea.md` status to `scored`.

## Exit Output

`.idea-validation/ideas/<slug>/decision_memo.md`:
- Verdict (pursue / test / pivot / drop)
- Final score
- Top 3 strengths and risks with evidence
- RAT, pre-mortem, kill criteria, next step

If verdict is `pivot` or `drop`, offer the **pivot-optimization** workflow.

## Notes

- The market-sizing agent (`iv-market-sizer`) runs in Wave 4 **by default for `target: b2b`** — the b2b Monetization rubric's top band requires a viable sized SOM, which is unreachable without it. For b2c it stays on request: scoring's Monetization rubric works from pricing + CAC, and when the user asks for market size the sizer joins Wave 4 (after pricing, so it reads real prices instead of the pack fallback) and feeds the Monetization dimension.

---
name: market-deep-dive
entry_condition: "User specifies a market category or topic"
exit_output: ".idea-validation/market_insights/<niche>-<platform>-<YYYY>-<MM>.md + .idea-validation/ideas/<slug>/{competitors,market_size,distribution}.json"
---

# Workflow: Market Deep Dive

## Startup Announcement

When this workflow is triggered, **immediately** say this before doing anything else:

> **📊 Starting: Market Deep Dive**
> I'll analyze the market you're interested in — trends across platforms, competitive landscape, market size, and how people actually acquire users in this space.

## Entry Conditions

- User specifies a topic or category (e.g. "nutrition apps", "B2B invoicing tools"). No product idea is required.
- Create a research slug with `market-` prefix (e.g. `market-nutrition-2026`) and `.idea-validation/ideas/<slug>/`.
- Apply the market_insights freshness check for this niche. Ask the user which platforms to research (see the trend platform menu in SKILL.md).

## Wave Plan

Dispatch each wave's agents together (one message, all in background); wait for the whole wave, verify each output file exists, present the wave's results, then start the next wave.

```
Wave 1 — evidence
  iv-trend-researcher × one per selected platform
    reads: platform prompt from references/prompts/<platform>.md; topic from user
    writes: .idea-validation/market_insights/<niche>-<platform>-<YYYY>-<MM>.md
  → present: Top 3 signals, velocity, verdict.

Wave 2 — landscape (independent given Wave 1)
  iv-competitor-mapper
    reads: topic, market_insights/<niche>-*
    writes: ideas/<slug>/competitors.json
  iv-distribution
    reads: user_profile.md (if present), topic, market_insights/<niche>-*
    writes: ideas/<slug>/distribution.json
  → present: Top 3 direct competitors (pricing + top complaint) and saturation;
    distribution verdict, first acquisition channel, whether a viral loop exists
    in this market.

Wave 3 — sizing (needs competitors.json)
  iv-market-sizer
    reads: market_insights, competitors.json (pricing.json may be absent — use
           competitor/category prices)
    writes: ideas/<slug>/market_size.json
  → present: TAM, SAM, realistic SOM year 1, market size verdict.
```

## Exit Output

Synthesize a short market briefing from:
- New/updated `.idea-validation/market_insights/<niche>-<platform>-<YYYY>-<MM>.md` files
- `.idea-validation/ideas/<slug>/market_size.json`
- `.idea-validation/ideas/<slug>/competitors.json`
- `.idea-validation/ideas/<slug>/distribution.json`

Offer idea-generation or idea-validation if the user wants to proceed.

## Notes

- If subagents are unavailable, run the same waves inline in this order (each agent body applied in your own context).

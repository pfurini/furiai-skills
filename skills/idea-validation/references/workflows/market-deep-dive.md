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

- User specifies a topic or category (e.g. "nutrition apps", "agency reporting tools"). No product idea is required.
- Determine the target (b2c | b2b) from the topic per SKILL.md, state it in the announcement, and pass it in every dispatch.
- **b2b only:** infer the sales-motion band (self-serve / assisted self-serve / sales-led, per SKILL.md), state it in the Startup Announcement, and record it in the briefing. Sales-led: say plainly that desk research cannot validate this segment before offering to continue.
- Create a research slug with `market-` prefix (e.g. `market-nutrition-2026`) and `.idea-validation/ideas/<slug>/`.
- Apply the market_insights freshness check for this niche. Ask the user which platforms to research (see the target's trend platform menu in SKILL.md).

## Wave Plan

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

Write the briefing with these sections, in order: (1) trend verdict per platform, with velocity; (2) top 3 competitors with pricing and top complaint, plus the saturation rating; (3) TAM / SAM / realistic year-1 SOM, with the method used; (4) first acquisition channel and whether a growth loop exists; (5) enter / wait / avoid recommendation in one sentence.

It is written from the new/updated `.idea-validation/market_insights/<niche>-<platform>-<YYYY>-<MM>.md` files plus `market_size.json`, `competitors.json`, and `distribution.json` under `.idea-validation/ideas/<slug>/`.

After presenting the briefing, read `references/pdf-report.md` and ask
"PDF report? EN / IT / both / skip"; on anything but skip, generate it via
the creating-pdf-reports skill (outputs `ideas/<slug>/report_en.pdf` and/or
`report_it.pdf`).

Offer idea-generation or idea-validation if the user wants to proceed.

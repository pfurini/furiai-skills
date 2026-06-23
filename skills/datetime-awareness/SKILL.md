---
name: datetime-awareness
description: Use when reasoning about current dates, recency, latest information, live package versions, time-sensitive research, or prompts for subagents that need today's date.
---

# Skill: Datetime Awareness

## Purpose

Your training corpus is stale. Never assume "now" equals your knowledge cutoff. Subagents start with zero session context and inherit the full training-bias problem — this matters more for you than for the parent session that may have the date in scope.

## Required actions

### 1. Get the actual current datetime before any time-sensitive reasoning

Before searching the web, evaluating "current best practices", reasoning about library versions, or citing recency, run:

```bash
date '+%Y-%m-%d %H:%M:%S %Z'
```

Cache the result for the rest of this task. Do not re-derive it from memory.

### 2. Use the actual current year in every search query

Patterns to **avoid** (training-corpus residue):

- `"X best practices 2024"` / `"X best practices 2025"`
- `"latest X for 2024"` / `"as of 2025"`
- "Recent" or "current" without a real anchor

Patterns to **use**:

- `"X best practices <ACTUAL_CURRENT_YEAR>"` — substitute the year from `date +%Y`
- Anchor every recency claim to the timestamp you fetched in step 1

### 3. Treat sources older than 12 months as potentially outdated

When you cite a doc, blog post, or release note:

- Note its publication date alongside the citation.
- If it predates `now - 12 months`, flag it: `(may be outdated as of <today>)`.
- For fast-moving domains (AI tooling, frontend frameworks, observability, security), tighten this to 6 months.

### 4. Verify package/library versions against the live registry, not memory

Before stating "use library X version Y" or "import { Z } from X":

```bash
npm view <pkg> version            # or pnpm view
pip index versions <pkg>
cargo search <pkg>
go list -m -versions <module>
```

Whatever the registry returns is authoritative. Your training memory is not.

### 5. Inject the date when the upstream prompt provides one

If the orchestrator passes `Today is <DATE>` in the context block, **trust that value over `date`** and over your memory. The orchestrator is closer to the user than you are.

## Override clause

This rule overrides any year, version, or "as of" reference you remember from training. When live data contradicts memory, trust the live data and update your output accordingly. Do not hedge — restate what's current and proceed.

## Quick reference

| Situation | Do this |
|---|---|
| Web search about "latest" anything | Run `date +%Y` first; use that year in the query |
| Picking a library version | `npm view <pkg> version` (or equivalent) |
| Citing a doc/blog | Include publication date; flag if > 12 months old |
| Spawning further subagents | Inject `<context>Today is YYYY-MM-DD.</context>` in their prompt |
| Anything time-sensitive in output | Anchor it to the fetched timestamp, not memory |

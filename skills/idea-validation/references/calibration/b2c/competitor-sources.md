# Competitor research sources — B2C calibration

Loaded by `iv-competitor-mapper` via the CALIBRATION path in its dispatch
prompt. Defines where to hunt for each competitor category and the
saturation factor anchors for the B2C target. The competitor taxonomy,
review-mining method, gap analysis, and scoring mechanics live in the agent
brief.

## Direct Competitor Sources (search in order)

1. **App Store / Play Store category browse**: Search the primary category and 2–3 keyword variations. Record the top 10 results for each search.
2. **"Best X apps" articles**: Search for `best [category] apps [current year]`. The top 3 listicle results typically capture the market leaders.
3. **Product Hunt**: Search the category. Sort by most upvoted. Focus on launches from the past 18 months (recent entrants).
4. **Market insights (Apps file)**: If `<niche>-apps-*.md` exists, extract any competitors named in the narrative.
5. **Market insights (Reddit file)**: If `<niche>-reddit-*.md` exists, extract apps users mention by name in discussions.
6. **AlternativeTo.net**: Search the closest existing app. Lists adjacent competitors you may have missed.

User-base estimation proxy: App Store ratings count × 50–100, or figures from the market_insights narrative.

## Primary Search Surface Methodology — App Store

The App Store is the most important research surface for B2C apps. Use this systematic approach:

1. **Primary keyword search**: The most obvious term a user would search (e.g., "habit tracker").
2. **Problem keyword search**: The problem statement (e.g., "build better habits").
3. **Audience keyword search**: The target user + need (e.g., "ADHD planner").
4. **Adjacent keyword search**: Related but broader terms (e.g., "daily routine", "productivity").

For each search, record:
- Number of results that are clearly relevant (not spam/unrelated)
- Rating and review count of the top 3 results
- Whether the top result has > 50K ratings (signals an entrenched incumbent)
- Date of last update for top 5 results (stale apps = opportunity to displace)

Review mining surface: the competitor's App Store / Play Store review pages (1-star, 3-star, 5-star per the method in the agent brief).

## Emerging Threat Sources

- Product Hunt launches in the past 6 months
- YC / startup accelerator demo day lists
- Apple WWDC / Google I/O feature announcements that could obviate the app
- If `trend_velocity` = "rising-fast" in market_insights, note that new entrants are likely

Flag any emerging competitor that has raised funding — they have resources to move fast.

## Saturation Factor Anchors

| Factor | Low (1 pt) | Medium (2 pts) | High (3 pts) |
|---|---|---|---|
| **Direct competitor count** | 0–2 relevant apps | 3–6 relevant apps | 7+ relevant apps |
| **Incumbent dominance** | No app has > 10K ratings | 1–2 apps have 10K–100K ratings | An app has > 100K ratings |
| **Funding in space** | No funded competitors | 1–2 funded startups | Multiple funded companies or a FAANG player |
| **App Store keyword saturation** | Primary keywords show few relevant results | Moderate results, some quality variance | Top results are all high-quality, well-maintained apps |
| **Content saturation** | Few "best X apps" articles exist | Some articles, moderate SEO competition | Many SEO-optimized listicles, hard to rank |

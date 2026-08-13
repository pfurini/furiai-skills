# Competitor research sources — B2B calibration (self-serve / PLG micro-SaaS)

Loaded by `iv-competitor-mapper` via the CALIBRATION path in its dispatch
prompt. Defines where to hunt for each competitor category and the
saturation factor anchors for the B2B target. The competitor taxonomy,
review-mining method, gap analysis, and scoring mechanics live in the agent
brief.

> Confidence: source lists are stable; the review→customer estimation proxy
> is `confidence: low` (provisional) pending the source-hardening pass.

## Direct Competitor Sources (search in order)

1. **G2 / Capterra category browse**: Find the matching category page(s). Record listed-product count, the category leaders, and the top 10 by review count.
2. **Marketplace search** (when the niche lives inside a platform — Shopify App Store, Slack App Directory, Atlassian Marketplace, Chrome Web Store, Zapier directory): search the primary keyword and 2–3 variations; record top 10 listings with installs/reviews/pricing.
3. **"Best X software" articles**: Search for `best [category] software [current year]`. The top 3 comparison results typically capture the market leaders.
4. **Product Hunt**: Search the category. Sort by most upvoted. Focus on launches from the past 18 months (recent entrants).
5. **Market insights (g2-capterra file)**: If `<niche>-g2-capterra-*.md` exists, extract every product named in the narrative.
6. **Market insights (communities file)**: If `<niche>-communities-*.md` exists, extract tools operators mention by name.
7. **AlternativeTo.net**: Search the closest existing product. Lists adjacent competitors you may have missed.

User-base estimation proxy: G2 + Capterra review count × 30–60 customers per review (provisional — few SMB buyers review), or marketplace install counts where shown, or vendor-claimed customer counts (discount marketing claims by half).

## Primary Search Surface Methodology — G2/Capterra + Marketplace

Review platforms and marketplaces are the primary research surface for self-serve B2B. Use this systematic approach:

1. **Primary keyword search**: The most obvious term a buyer would search (e.g., "client reporting").
2. **Problem keyword search**: The job statement (e.g., "automate agency reports").
3. **Audience keyword search**: The buyer + need (e.g., "reporting for small agencies").
4. **Adjacent keyword search**: Related but broader terms (e.g., "marketing dashboard", "analytics").

For each search, record:
- Number of results that are clearly relevant (not spam/unrelated)
- Review count and rating of the top 3 results
- Whether the top result has > 2,000 combined G2+Capterra reviews or > 5,000 marketplace installs (signals an entrenched incumbent — provisional thresholds)
- Last-update / recent-review dates for top 5 results (stale products = opportunity to displace)

Review mining surface: the competitors' G2 and Capterra review pages (1–2-star, 3-star, 5-star per the method in the agent brief), plus marketplace reviews where the niche is marketplace-based. G2's structured "dislikes" field is the richest complaint source.

## Substitutes — B2B specifics

The dominant substitutes in SMB niches are **spreadsheets, email/chat threads, an employee's manual hours, an agency/freelancer retainer, or the incumbent platform's clunky built-in feature**. Always price the manual alternative (hours × loaded wage) — it is the switching-cost baseline and the strongest WTP anchor downstream.

## Emerging Threat Sources

- Product Hunt and marketplace "new & noteworthy" launches in the past 6 months
- YC / accelerator batch lists in the category
- Platform vendor announcements (Shopify Editions, Atlassian/Slack/Google Workspace feature releases) that could absorb the niche natively
- Funding announcements in the category trade press
- If `trend_velocity` = "rising-fast" in market_insights, note that new entrants are likely

Flag any emerging competitor that has raised funding — they have resources to move fast.

## Saturation Factor Anchors

| Factor | Low (1 pt) | Medium (2 pts) | High (3 pts) |
|---|---|---|---|
| **Direct competitor count** | 0–2 relevant products | 3–6 relevant products | 7+ relevant products |
| **Incumbent dominance** | No product has > 200 combined reviews | 1–2 products have 200–2,000 reviews | A product has > 2,000 reviews or the platform vendor ships the feature |
| **Funding in space** | No funded competitors | 1–2 funded startups | Multiple funded companies or a platform/suite vendor in the category |
| **Category keyword saturation** | Primary keywords show few relevant G2/marketplace results | Moderate results, some quality variance | Top results are all high-quality, actively maintained products |
| **Content saturation** | Few "best X software" comparison pages exist | Some pages, moderate SEO competition | Many SEO-optimized comparison sites and vendor content, hard to rank |

(Review-count thresholds are provisional, `confidence: low`, pending the source-hardening pass.)

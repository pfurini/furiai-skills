# Market sizing — B2C calibration

Loaded by `iv-market-sizer` via the CALIBRATION path in its dispatch prompt.
Defines the estimation proxies, conversion benchmarks, platform filters, and
capture rates for the B2C target. The triangulation mechanism, SAM filter
logic, reality checks, and verdict thresholds live in the agent brief.

## Intent Conversion Benchmarks (Approach A — search volume)

| Search intent | Conversion rate | Example query |
|---|---|---|
| Direct solution search ("app to track X") | 8–15% | "habit tracker app", "budget planner iOS" |
| Problem-aware search ("how to X") | 3–8% | "how to save money", "how to build habits" |
| Category browsing ("best X apps") | 5–12% | "best workout apps", "top meditation apps" |
| Tangential interest ("X tips") | 1–3% | "productivity tips", "healthy eating advice" |

## Platform Multipliers (Approach B — community size proxy)

How many silent interested people per active community member:

| Signal source | Multiplier | Rationale |
|---|---|---|
| Reddit subscribers in niche subreddit | 20–50× | ~2–5% of interested people join a subreddit |
| TikTok hashtag creators (not views) | 100–500× | Tiny fraction of interested people create content |
| App Store reviews for top competitor | 50–100× | ~1–2% of users leave reviews |
| Newsletter subscribers in niche | 10–30× | Email subscribers are a warmer proxy |

## Platform Filter — iOS Market Share by Region (for iOS-only apps)

| Region | iOS share (approximate) |
|---|---|
| United States | 55–58% |
| United Kingdom | 50–53% |
| Canada | 53–56% |
| Australia | 55–58% |
| Western Europe (avg) | 30–35% |
| Global | 25–28% |
| Southeast Asia | 10–15% |
| India | 4–6% |
| Latin America | 12–18% |

For Android-only or cross-platform, apply the inverse or use 100%.

## SOM Capture Rate Benchmarks by Category

| App category | Year 1 capture rate | Year 3 capture rate | Notes |
|---|---|---|---|
| **Utility / tool** (calculator, converter, scanner) | 0.1–0.5% of SAM | 0.5–2.0% | Discoverable via ASO, many competitors |
| **Niche productivity** (specific workflow tool) | 0.5–2.0% | 2.0–5.0% | Smaller SAM but higher capture in the niche |
| **Health & fitness (niche)** | 0.3–1.5% | 1.0–4.0% | Loyal users if retention is strong |
| **Health & fitness (broad)** | 0.05–0.2% | 0.2–0.8% | Dominated by incumbents |
| **Social / community** | 0.01–0.1% | 0.1–0.5% | Network effects favor incumbents; cold start is brutal |
| **Content / media** | 0.1–0.5% | 0.5–2.0% | Depends heavily on content quality and curation |
| **Finance / budgeting** | 0.1–0.5% | 0.5–2.0% | High trust barrier, but sticky once adopted |
| **Creative tools** (photo, video, design) | 0.2–1.0% | 1.0–3.0% | Shareable output drives organic growth |
| **Education / learning** | 0.2–1.0% | 1.0–3.0% | Retention is the main challenge |
| **Lifestyle / habit** | 0.3–1.5% | 1.0–4.0% | Success varies wildly by habit loop quality |

Use the **lower end** of the range when:
- `market_saturation` from `competitors.json` is "high"
- Founder is beginner tier (from `user_profile.md`)
- No distribution advantage identified

Use the **upper end** when:
- Founder has an existing audience or distribution edge
- Strong ASO opportunity or viral loop exists
- Market is growing fast (trend_velocity = "rising-fast")

## Fallback Price (when pricing.json is absent)

Use the median competitive price from `competitors.json` or a category benchmark ($3–$7/mo for typical B2C subscription apps).

## Reality-check thresholds and SOM verdict bands (read by the market-sizer brief)

Numeric reality checks (record every triggered check in `reality_checks_triggered`):

| Check | Threshold | Action if triggered |
|---|---|---|
| TAM inflation | TAM > $10B for a niche indie app | Almost certainly top-down numbers; redo bottom-up only |
| SAM too broad | SAM > 50% of TAM | Filters too loose; add platform/geography/niche constraints |
| SOM fantasy | SOM year 1 > $500K for a solo developer | Reality-check the capture rate; most indie apps earn $0–$50K in year 1 |

`market_size_verdict` from SOM year 1:

| SOM year 1 | Verdict |
|---|---|
| > $200K | large — significant indie opportunity |
| $50K–$200K | medium — viable as a primary project with good retention |
| $10K–$50K | niche — side-project scale; viable if build cost is low |
| < $10K | micro-niche — hobby scale unless the niche can expand |

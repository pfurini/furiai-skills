---
prompt_for: reddit
placeholder: "[NICHE]"
usage: Replace [NICHE] with the bilingual niche wording ("<Italian> / <English>") before invoking. Ring-1 (Italy) research runs Italian-first.
---

**Objective:**
Identify and analyze **current community discussions in the [NICHE] niche, ring by ring — Italian-language communities first (Ring 1 — IT), then English-language communities (Ring 2 — EU-EN, Ring 3 — Western)** — using **credible, recent sources (published within the last 6 months)**. Every finding carries a ring label.

---

**Instructions:**

1. **Source Criteria**

   * Use only **credible and recent sources (≤ 6 months old)**
   * At the beginning of the response, clearly state:
     **"Data observed as of [month/year]"**
   * Prioritize sources in this order:

     **Tier 1 — Italian-language communities, verified active (Ring 1, your primary surface)**
     * Niche Italian surfaces, verified active 2026-08 — re-verify (a post within ~60 days) before citing as live:
       finance/budgeting r/ItaliaPersonalFinance, r/bollette · fitness r/ItalyFitness, bodyweb.com/forum, bbhomepage.com/forum · food r/veganita (dietary-identity; no live general-cooking sub exists) · parenting forum.alfemminile.com (no live parenting subreddit exists) · students/study r/Universitaly, r/polinetwork · gaming r/italygames, r/AnimeItaly · tech/apps r/ItalyInformatica (large but ~1 post/day), r/ItalyHardware, r/IA_Italia, hwupgrade.it/forum · calcio/fantacalcio r/seriea, r/Calcio, r/fantacalcio_IT · giardinaggio giardinaggio.it/forum, r/giardinaggioITA · modellismo modellismo.net/forum · motori r/ItalyMotori · travel r/ViaggiITA, r/TrekkingItaly · wellbeing r/psicologia, r/Psicologia_Italia, r/adhd_italia · consumer reviews/complaints altroconsumo.it community and bacheca dei reclami
     * General Italian subreddits for cross-niche signal: r/italy, r/Italia, r/CasualIT, r/consigli (advice-seeking)
     * **Language traps — never cite as Ring-1 evidence**: r/ItalianFood, r/italiancooking, r/mediterraneandiet, r/ItalyTravel, r/askitaly, r/italianlearning are English-language communities of foreigners; r/studenti is Croatian. Niches with NO live Italian-language surface (do not invent one): language learning, general cooking, parenting on Reddit, productivity-as-such — route those to the general subreddits and report the absence as a finding.
     * Private Facebook and Telegram groups are **existence signals only**, never activity evidence; Telegram public channels are broadcast, not discussion.
     * **Never report a surface named in this list as absent or dead without fetched evidence.** reddit.com walls unauthenticated fetches; if a listed surface cannot be reached (directly or via a mirror), record it as UNVERIFIABLE — an unfetchable surface is not a missing one.

     **Tier 2 — Reddit-native sources (Rings 2–3 — label the ring)**
     * Reddit itself — search top posts by subreddit, sort by "Top / Past 6 months" or "Hot"; look for posts with high upvotes and comment volume as proxy for community-wide resonance
     * Reddit Search — use Reddit's native search to find recurring keywords, questions, and complaints within relevant subreddits
     * r/[niche-specific subreddits] — identify the 3–5 most active subreddits in the niche; note subscriber count and posting frequency as baseline metrics

     **Tier 3 — Reddit analytics & aggregation tools**
     * Redditmetis — subreddit growth stats, posting trends, engagement benchmarks
     * Subreddit Stats (subredditstats.com) — subscriber growth over time, activity trends
     * Front Page Metrics — tracks what reaches Reddit's front page; useful for identifying crossover appeal
     * GummySearch — pain point aggregation from Reddit; clusters recurring complaints, requests, and discussions by theme

     Also search for **articles and analyses that cite Reddit data or aggregate Reddit discussions** — marketing blogs, research papers, and journalists who quote upvote counts, comment volumes, or subreddit activity inherit Reddit's community signal. Examples: The Verge, Vice, Wired, BuzzFeed News covering viral Reddit threads.

     **Tier 4 — Complementary community platforms (triangulate Reddit signal)**
     * X (Twitter) — check if Reddit discussions are spilling into Twitter/X threads, which amplifies signal
     * Quora — recurring questions that mirror Reddit thread patterns indicate sustained informational demand

---

2. **Trend Identification**
   Identify both:

   * **Established trends** (recurring high-upvote topics, large active subreddits, stable discussion volume)
   * **Emerging / rising trends** (fast-growing subreddits, recently viral threads, new recurring question types)

   For each trend, note whether it is **subreddit-specific** (contained within one community) or **cross-subreddit** (appearing across multiple communities — stronger signal).

---

3. **For EACH trend or discussion theme, provide:**

**A. Basic Information**

* Trend / topic name
* Primary subreddit(s) where it appears
* Category (e.g., recurring complaint, product request, lifestyle shift, myth-busting, community ritual, recommendation-seeking, debate/controversy, etc.)

**B. Description**

* What posts and discussions typically look like (format: question, rant, success story, review, debate, etc.)
* What audience problem, frustration, or desire is driving the conversation
* Why it is gaining attention (cultural shift, product gap, algorithm/feed changes, external news event, etc.)

**C. Quantitative Metrics**

* Subreddit subscriber count and monthly active users (if available)
* Representative post upvote counts and comment volumes
* Posting frequency on the topic (e.g., "appears in top posts weekly")
* Cross-subreddit reach (how many distinct subreddits surface this topic)

**D. Growth Analysis**

* For **rising trends only**, include:

  * Growth rate (subreddit subscriber growth % OR increase in post frequency over time)
  * Timeframe (e.g., "subreddit grew +40% in 90 days")
  * Velocity classification (slow / moderate / explosive)

**E. Evidence labels** (mandatory, per finding — exactly one line, this exact shape, always with all five slots — write `n/a` for a slot you cannot fill; the scoring step counts labels mechanically):

`labels — ring: <IT | EU-EN | Western> · lang: <it | en> · surface: <subreddit or forum where observed> · evidence: <thread | recurring post pattern | subscriber metric | report | article> · confidence: <high | medium | low>`

Ring: `IT` = Italian-language / Italian-market signal; `EU-EN` = English-language signal clearly from EU consumers; `Western` = NA, UK/IE, AU/NZ, or global. Confidence: **high** only when two independent sources agree, or one is a direct first-hand observation you fetched; **medium** for a single credible source; **low** for aggregator-only, undated, or cross-ring inference.

---

4. **Structure the Output**
   Organize findings into clearly separated sections:

* **1. Executive Summary (Key Insights)**
* **2. Established Trends**
* **3. Emerging / Rising Trends**
* **4. Key Subreddits & Topic Clusters (group related communities and recurring themes)**
* **5. Strategic Insights (Marketing & Product Takeaways)**
* **6. Financial Opportunities** (per instruction 6 below)
* **7. Niche Risks** (per instruction 7 below)
* **8. Disconfirming Evidence** (per instruction 8 below)
* **9. Sources** (per instruction 9 below)

---

5. **Additional Analysis (Value Add)**
   Include:

* Pattern recognition (e.g., shift in sentiment, recurring unmet needs, emerging vocabulary or framing the community uses for a problem)
* Post formats driving engagement (e.g., "Am I the only one who...", success stories, tool comparisons, "What do you use for X?", rants about incumbents)
* Any **misinformation vs. evidence-based tension** — where community consensus diverges from expert opinion
* **Unmet needs signal**: recurring posts where the top comment is "I wish there was a product that..." or "I've been looking for this for years" — these are high-value product opportunity signals
* Opportunities for content creators, community builders, or brands to engage authentically

---

6. **Financial Opportunities**
   Identify the **most monetarily interesting, not yet saturated problems or high-intent interests** surfacing in Reddit communities within the niche that people are **already actively paying to solve** — or loudly wishing they could. Base conclusions on realistic market data (search volume, existing product revenue, subreddit activity, industry reports) — avoid speculative or wishful sizing.

   For each opportunity, provide:

   * **Problem / high-intent interest**: What specifically are people paying to solve or actively seeking solutions for?
   * **Reddit signal**: Specific evidence from Reddit — recurring post types, upvote patterns, comment sentiment, subreddit size — that confirms real demand
   * **Evidence of willingness to pay**: Existing products, services, or categories with proven revenue that the community already discusses, recommends, or complains about
   * **Saturation assessment**: Is the market crowded, or are there underserved segments / entry angles a new player could own?
   * **Realistic market size estimate**: Use bottoms-up reasoning where possible (e.g., "subreddit has X members, Y% post about problem Z monthly, comparable products charge $W → addressable pool of $..."). Cite data sources.
   * **Why now**: What trend, product gap, or cultural shift makes this opportunity timely?

   Prioritize opportunities that are:
   * Backed by **existing spending behavior** (not hypothetical demand)
   * **Specific enough** to be actionable (not "the wellness market is $5T")
   * **Emerging or underserved** — avoid opportunities already dominated by entrenched players with no viable wedge

---

7. **Niche Risks**
   Identify the **most significant risks** that could undermine a product or business built in this niche, based on signals observable in Reddit communities. Base conclusions on actual community behavior, not assumptions.

   For each risk, provide:

   * **Risk**: Short label (e.g., "Regulatory backlash", "Community distrust of apps", "Trend reversal")
   * **Reddit signal**: Specific evidence — post types, recurring complaints, subreddit discussions, or sentiment shifts that indicate this risk is real
   * **Severity**: Low / Medium / High
   * **Mitigation angle**: Is there a sub-segment, framing, or product approach that avoids or reduces this risk?

   Risk types to consider:
   * **Sentiment risk** — is community sentiment toward apps or paid tools in this niche negative or skeptical? (e.g., "people here hate subscriptions", "community prefers free tools")
   * **Regulatory or legal risk** — are there recurring threads about legal issues, bans, health claims, or platform policy that could affect products in this space?
   * **Saturation fatigue** — is the community exhausted by existing products? Are threads full of "yet another X app" complaints?
   * **Trend reversal signal** — are there signs the niche is peaking or cycling out? (declining post frequency, subreddit going quiet, backlash against the trend)
   * **Incumbent defensiveness** — are large brands or platforms actively entering and dominating conversations in ways that crowd out indie entrants?
   * **Seasonal or cyclical demand** — does community activity spike at predictable times (January fitness resolutions, tax season, etc.) that would create boom-bust revenue patterns?

---

8. **Disconfirming Evidence**
   Report what you looked for and did **not** find, and any evidence that cuts against the demand story: Italian communities you expected that do not exist or are dead, recurring threads where the consensus is "the free tool is enough", topics whose post frequency is visibly declining. An absent or silent Italian-language community for a niche that is loud in English is a finding — label it and say what it implies for Ring 1.

9. **Sources**
   At the end of the document, include a **"Sources" section** listing all URLs referenced during research as markdown hyperlinks:

   ```
   ## Sources
   - [Publication / Page Title](https://url.com)
   - [Publication / Page Title](https://url.com)
   ```

   * Include every source consulted, even if not directly quoted
   * Use the actual page title or publication name as the link label

---

**Goal:**
Deliver a **data-backed, structured analysis** that not only lists trends but explains **why communities are talking about them, what underlying needs they reveal, and how they can be leveraged strategically**.

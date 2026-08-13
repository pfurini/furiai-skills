---
prompt_for: g2-capterra
placeholder: "[NICHE]"
usage: Replace [NICHE] with the target topic (e.g., "agency reporting", "dental practice management", "Shopify inventory") before invoking.
---

**Objective:**
Identify and analyze **the current software landscape and buyer sentiment for [NICHE] on B2B review platforms** using **credible, recent sources (reviews and data from the last 12 months)**.

---

**Instructions:**

1. **Source Criteria**

   * Use only **credible and recent sources (reviews ≤ 12 months old for sentiment; category data as current as available)**
   * At the beginning of the response, clearly state:
     **"Data observed as of [month/year]"**
   * Prioritize sources in this order:

     **Tier 1 — B2B review platforms (highest signal fidelity)**
     * G2 — category pages for the niche: number of listed products, category leaders (Grid position), review counts and velocity, satisfaction vs. market-presence quadrants
     * Capterra / GetApp / Software Advice (Gartner Digital Markets) — category listings, pricing ranges shown on profiles, "alternatives to X" pages
     * Product profile review pages — sort by most recent; mine 1–2-star and 3-star reviews for recurring complaints, and note which complaints recur across multiple products in the category

     **Tier 2 — Marketplace ecosystems (where the niche lives inside a platform)**
     * Shopify App Store / Slack App Directory / Atlassian Marketplace / Chrome Web Store / Zapier app directory — listing counts for the niche keyword, install/review counts of top listings, rating distributions, pricing models in use, last-update dates
     * Marketplace category "trending / new" sections — new entrant velocity

     **Tier 3 — Corroborating sources**
     * Vendor pricing pages (verify actual price points and packaging: per-seat vs flat vs usage)
     * "Best [NICHE] software [current year]" comparison articles — note which products every list repeats
     * TrustRadius / Reddit threads naming these tools — cross-check sentiment

---

2. **Trend Identification**
   Identify both:

   * **Established demand** (mature categories: many products, high review volume, stable leaders)
   * **Emerging / rising demand** (new categories or sub-niches: fast review-count growth, many recent launches, marketplace "trending" placement, buyers describing new job-to-be-done in reviews)

   For each theme, note whether it is **category-wide** (appears across many products' reviews) or **product-specific** (one vendor's failure — weaker signal for market demand, stronger for a displacement wedge).

---

3. **For EACH trend or buyer-sentiment theme, provide:**

**A. Basic Information**

* Theme name
* Category / marketplace where it appears
* Type (recurring complaint, missing capability, pricing revolt, integration demand, segment underserved, workflow shift, etc.)

**B. Description**

* What buyers say, in their vocabulary (quote representative review fragments)
* The underlying business pain: what breaks, what it costs the buyer (time, money, risk) when it breaks
* Who inside the business feels it (owner, ops person, marketer, developer)

**C. Quantitative Metrics**

* Products listed in the category; review counts of the top 3–5
* Review velocity where visible (reviews in the last 12 months vs total)
* Price points observed (per-seat / flat / usage; monthly figures)
* Install counts for marketplace listings (where shown)

**D. Growth Analysis**

* For **rising themes only**: evidence of growth (new-entrant count, review-velocity change, new category creation on G2) with timeframe and a velocity classification (slow / moderate / explosive)

---

4. **Structure the Output**
   Organize findings into clearly separated sections:

* **1. Executive Summary (Key Insights)**
* **2. Established Demand**
* **3. Emerging / Rising Demand**
* **4. Category Map (products, leaders, pricing patterns, marketplace ecosystems)**
* **5. Strategic Insights (positioning & product takeaways)**
* **6. Financial Opportunities** (per instruction 6 below)
* **7. Niche Risks** (per instruction 7 below)
* **8. Sources** (per instruction 8 below)

---

5. **Additional Analysis (Value Add)**
   Include:

* Recurring complaint clusters that appear across 2+ competing products — these are validated category-wide gaps
* Pricing sentiment: which price points reviews call fair vs extortionate; complaints about per-seat pricing, forced annual plans, or feature gating
* Integration demand: which "works with X" requests recur (the X is a distribution channel)
* Segment mismatch signals: reviews saying "great for big teams, overkill for us" — the underserved small-buyer segment is an indie wedge
* Stale incumbents: category leaders with slowing review velocity, dated UI complaints, or acquisition-then-neglect patterns

---

6. **Financial Opportunities**
   Identify the **most monetarily interesting, not yet saturated problems** in this niche that businesses are **already actively paying to solve** — or loudly complaining about paying too much to solve badly. Base conclusions on realistic data (listed prices, review volume as adoption proxy, marketplace installs) — avoid speculative sizing.

   For each opportunity, provide:

   * **Problem**: What specifically are businesses paying to solve?
   * **Review-platform signal**: Specific evidence — complaint clusters, category gaps, segment-mismatch reviews — that confirms real demand
   * **Evidence of willingness to pay**: Products with visible pricing and review volume; marketplace listings with installs; price points buyers accept
   * **Saturation assessment**: Is the category crowded, or are there underserved segments / integration angles / price tiers a new player could own?
   * **Realistic revenue math**: Bottoms-up where possible (e.g., "top 5 products have ~N combined reviews → ~N×30–60 customers at $X/mo → category revenue on the order of $..."). Cite what the estimate rests on.
   * **Why now**: What platform shift, incumbent neglect, or workflow change makes this timely?

   Prioritize opportunities that are backed by **existing spending behavior**, **specific enough to be actionable**, and **not dominated by an entrenched leader with no viable wedge**.

---

7. **Niche Risks**
   Identify the **most significant risks** observable from review-platform and marketplace signals.

   For each risk, provide: **Risk** (short label) · **Signal** (specific evidence) · **Severity** (Low / Medium / High) · **Mitigation angle**.

   Risk types to consider:
   * **Platform dependence** — the niche lives inside one marketplace whose owner could build the feature natively or change terms/fees
   * **Incumbent consolidation** — leaders acquiring adjacent tools, closing the gap an indie would enter through
   * **Category commoditization** — many near-identical products competing on price; race to the bottom
   * **High switching costs favoring incumbents** — buyers complain but don't leave (data lock-in, retraining costs); displacement is harder than reviews suggest
   * **Compliance/procurement creep** — reviews mention SOC 2, SSO, procurement requirements — signals the category is drifting sales-led, away from indie-viable self-serve
   * **AI obviation** — the job the category does is being absorbed into platforms' native AI features

---

8. **Sources**
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
Deliver a **data-backed, structured analysis** that not only maps the category but explains **what buyers are paying for, where incumbents fail them, and which gaps an indie self-serve product could credibly own**.

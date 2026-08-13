---
prompt_for: g2-capterra
placeholder: "[NICHE]"
usage: Replace [NICHE] with the bilingual niche wording ("<Italian> / <English>", e.g. "software preventivi edilizia / construction quoting software") before invoking. Search Italian-first.
---

**Objective:**
Identify and analyze **the software landscape and buyer sentiment for [NICHE] on review platforms and marketplaces, as it applies to Italian buyers**, using **credible, recent sources (reviews ≤ 12 months old for sentiment; category data as current as available)**.

**Calibration warning (governs everything below):** global review platforms systematically under-represent the Italian market. Italian vertical incumbents can dominate a niche with a handful of G2 reviews or none; English review volume measures the Anglophone market, not Italian adoption. Use review platforms for **complaint mining and pricing evidence**, never as an Italian market-share census — and say which market each signal describes.

---

**Instructions:**

1. **Source Criteria**

   * Search **Italian-first** where the surface allows, English second. Write the report in English; keep Italian quotes verbatim with a translation.
   * At the beginning of the response, clearly state: **"Data observed as of [month/year]"**
   * Prioritize sources in this order:

     **Tier 1 — Italian-language review surfaces (highest relevance, thin volume)**
     * **Capterra.it** — category pages and Italian-language reviews; record listed-product count, review counts, pricing shown, and which products have ITALIAN reviews (that subset is the Italian competitive set).
     * **Trustpilot.it and Google reviews** of the Italian products in the niche — for Italian SMB tools these often carry more volume than G2/Capterra; mine 1–3-star reviews for recurring complaints.
     * Reviews inside Italian marketplaces where the niche touches them: **Fatture in Cloud App Store**, **TeamSystem Commerce Apps Market**.

     **Tier 2 — Global review platforms and marketplaces (directional)**
     * G2 / Capterra.com / GetApp / Software Advice — category structure, the global leaders, their review velocity and structured "dislikes"; label all of it `geography: non-IT`.
     * Global marketplaces where the niche lives inside a platform (Shopify App Store, Zapier, Chrome Web Store): listing counts, installs, rating distributions, last-update dates — installs are global; check for Italian-language listings/reviews as the Italy proxy.

     **Tier 3 — Corroborating sources**
     * Vendor pricing pages (verify EUR price points and packaging: per-seat vs flat vs usage; ex-VAT).
     * Italian comparison articles ("miglior software [NICHE] [current year]") — note which products every Italian list repeats vs which only appear in translated/affiliate content.
     * TrustRadius / Reddit threads naming these tools — cross-check sentiment.

2. **Trend Identification**
   Identify both:
   * **Established demand** (mature categories: many products, stable leaders — state separately for the global set and the Italian subset)
   * **Emerging / rising demand** (fast review-count growth, recent launches, buyers describing a new job-to-be-done)

   For each theme, note whether it is **category-wide** (appears across many products' reviews) or **product-specific** (one vendor's failure — weaker for market demand, stronger for a displacement wedge), and whether it appears **in Italian reviews** or only in English ones.

3. **For EACH trend or buyer-sentiment theme, provide:**

**A. Basic Information** — theme name; platform/marketplace where it appears; type (recurring complaint, missing capability, pricing revolt, integration demand, segment underserved, localization gap).

**B. Description** — what buyers say, in their vocabulary (quote; translate Italian quotes); the underlying business pain (time, money, risk); who inside the business feels it. **Localization gaps are first-class findings**: complaints about missing Italian language, fatturazione elettronica/SDI support, F24, conservazione, or Italian payment methods mark exactly where global tools fail Italian buyers.

**C. Quantitative Metrics** — products listed; review counts of the top 3–5 **split global vs Italian-language**; review velocity where visible; EUR/USD price points observed (billing unit, ex-VAT where stated); marketplace installs where shown.

**D. Growth Analysis** — for rising themes only: growth evidence with timeframe and velocity classification (slow / moderate / explosive).

**E. Evidence labels** (mandatory) — **geography** (IT / non-IT) · **region** (national / North / Centre / South / province; "n/a" for non-IT) · **segment** (commercialista, avvocato, consulente del lavoro, artigiano, merchant, agency, generic PMI) · **firm-size proxy** · **stack** (the software the source uses, when stated) · **regulatory dependency** (SDI, PCT, PEC, AML, GDPR, conservazione — or none) · **switching constraint** · **evidence type** (review, listing, pricing page, comparison article) · **confidence** (high only when two independent Italian-language sources agree, or one is interview-/association-research-confirmed; medium for a single Italian source; low for non-IT or vendor-supplied).

4. **Structure the Output**

* **1. Executive Summary (Key Insights)**
* **2. Established Demand** (global set vs Italian subset, kept distinct)
* **3. Emerging / Rising Demand**
* **4. Category Map** (products, leaders, pricing patterns, marketplaces — with an explicit "Italian competitive set" list)
* **5. Strategic Insights (positioning & product takeaways)**
* **6. Financial Opportunities** (per instruction 5 below)
* **7. Niche Risks** (per instruction 6 below)
* **8. Disconfirming Evidence** (per instruction 7 below)
* **9. Sources**

5. **Financial Opportunities**
   Identify the most monetarily interesting, not yet saturated problems that businesses are **already actively paying to solve** — or loudly complaining about paying too much to solve badly. For each: **Problem** · **Review-platform signal** (complaint clusters, category gaps, localization gaps) · **Evidence of willingness to pay** (visible EUR/USD pricing with adoption evidence; marketplace installs; price points buyers accept) · **Saturation assessment** (crowded globally vs open in Italy — the "works in Italian, speaks SDI" wedge against a global leader is a recurring pattern) · **Realistic revenue math** (bottoms-up; state which market the numbers describe; never convert global review counts into Italian customers) · **Why now**.

6. **Niche Risks**
   For each: **Risk** · **Signal** · **Severity (Low/Medium/High)** · **Mitigation angle**. Consider at least: **platform dependence** (marketplace owner could ship the feature or change fees); **incumbent consolidation**; **category commoditization** (race to the bottom); **high switching costs favoring incumbents** (buyers complain but don't leave); **compliance/procurement creep** (SOC 2/SSO demands — sales-led drift); **AI obviation**; **thin-market invisibility** (the Italian niche may be too small to sustain review signal at all — distinguish "no reviews because no market" from "no reviews because Italians don't review").

7. **Disconfirming Evidence** (mandatory)
   What argues AGAINST: an entrenched leader with satisfied Italian users, localization gaps already being closed, categories where free/native features are praised as sufficient.

8. **Sources** — end with a `## Sources` section listing every URL consulted as markdown links.

---

**Goal:**
Deliver a **data-backed, structured analysis** that maps the category for an Italian buyer: **what is paid for, where global leaders fail Italians (localization and compliance gaps), which complaints recur in Italian reviews, and which gaps an indie self-serve product could credibly own** — with every claim labeled by the market it actually describes.

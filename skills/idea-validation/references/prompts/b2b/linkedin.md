---
prompt_for: linkedin
placeholder: "[NICHE]"
usage: Replace [NICHE] with the target topic (e.g., "agency reporting", "dental practice management", "Shopify inventory") before invoking.
---

**Objective:**
Identify and analyze **professional demand signals for [NICHE] visible through LinkedIn and the professional-web layer around it** (posts, job postings, company activity, vendor announcements), using **credible, recent sources (published within the last 6 months)**.

Note: LinkedIn itself is only partially indexable. Combine what is directly visible (public posts, job listings, company pages) with sources that report on LinkedIn-layer activity (hiring trend reports, vendor funding/launch announcements, professional-press coverage). State clearly which claims come from direct observation vs. secondary reporting.

---

**Instructions:**

1. **Source Criteria**

   * Use only **credible and recent sources (≤ 6 months old)**
   * At the beginning of the response, clearly state:
     **"Data observed as of [month/year]"**
   * Prioritize sources in this order:

     **Tier 1 — Professional demand signals**
     * LinkedIn public posts and articles on the niche — practitioner complaints, workflow debates, tool recommendations, "we switched from X to Y" posts
     * Job postings (LinkedIn Jobs, Indeed) mentioning the workflow or tools — a company hiring a person to do this job manually is unmet software demand; postings naming specific tools measure incumbent penetration
     * Company pages of vendors in the niche — headcount growth, launch announcements, customer-count claims

     **Tier 2 — Professional-web reporting**
     * Hiring/skills trend reports (LinkedIn Economic Graph publications, staffing-industry reports) touching the niche
     * Funding announcements and launch coverage for tools in the space (TechCrunch, vertical trade press)
     * Vertical trade publications and association newsletters where operators of this niche read about tools

     **Tier 3 — Corroboration**
     * X/Twitter professional threads mirroring the LinkedIn discussion
     * Webinar/conference agendas for the vertical (recurring session topics = recurring pains)

---

2. **Trend Identification**
   Identify both:

   * **Established demand** (long-running pain themes, mature vendor landscape, steady job-posting presence)
   * **Emerging / rising demand** (new pain themes tied to regulation/platform/AI shifts, spiking job-posting language, new vendors getting funded or announced)

   For each theme, note whether the signal is **practitioner-driven** (operators describing their own pain — strongest) or **vendor-driven** (marketing content — weakest; discount accordingly).

---

3. **For EACH demand theme, provide:**

**A. Basic Information**

* Theme name
* Where it appears (posts, jobs, funding news, trade press)
* Type (workflow pain, compliance scramble, tool-switching wave, manual-role hiring, budget shift, etc.)

**B. Description**

* What professionals say, in their vocabulary
* The business pain underneath: cost in hours, money, or risk; which role owns it; who has budget authority over fixing it
* Current solutions named (tools, agencies, manual hires)

**C. Quantitative Metrics**

* Engagement on representative posts (where visible)
* Job-posting counts mentioning the workflow/tools (state the query used)
* Vendor signals: funding amounts, claimed customer counts, headcount growth
* Audience sizes of niche voices/newsletters covering the theme

**D. Growth Analysis**

* For **rising themes only**: growth evidence (posting-frequency change, job-listing growth, funding cluster), timeframe, velocity classification (slow / moderate / explosive)

---

4. **Structure the Output**
   Organize findings into clearly separated sections:

* **1. Executive Summary (Key Insights)**
* **2. Established Demand**
* **3. Emerging / Rising Demand**
* **4. Professional Landscape (roles affected, budget owners, vendor map, hiring patterns)**
* **5. Strategic Insights (positioning & distribution takeaways)**
* **6. Financial Opportunities** (per instruction 6 below)
* **7. Niche Risks** (per instruction 7 below)
* **8. Sources** (per instruction 8 below)

---

5. **Additional Analysis (Value Add)**
   Include:

* **Manual-hire signal**: jobs posted to do this workflow by hand — the strongest "software gap" indicator; note salary ranges (they bound the software's value)
* **Budget authority mapping**: is the buyer the operator themselves (self-serve fit) or a department head/procurement (sales-led risk)?
* **Founder-brand opportunity**: are there large practitioner audiences following niche voices? An underserved audience with no tool-building voice is a distribution opening
* **AI displacement chatter**: are professionals discussing AI replacing or reshaping this workflow — threat or tailwind?

---

6. **Financial Opportunities**
   Identify the **most monetarily interesting, not yet saturated problems** that businesses in this niche demonstrably spend money on — software subscriptions, agency fees, or salaried hours. Base conclusions on realistic data (salaries in job posts, vendor pricing, funding sizes) — avoid speculative sizing.

   For each opportunity, provide:

   * **Problem**: What are businesses spending on?
   * **Professional signal**: The posts/jobs/announcements confirming recurring demand
   * **Evidence of willingness to pay**: Vendor traction, salary costs of the manual alternative, agency fees for the same job
   * **Saturation assessment**: Vendor density; whether incumbents serve the small-business tier or only mid-market/enterprise (the ignored small tier is the indie wedge)
   * **Realistic revenue math**: Bottoms-up (e.g., "N businesses of this type in the US, X% employ someone doing this manually at $Y/yr → a $Z/mo tool replacing 20% of that time is worth..."). Cite what it rests on.
   * **Why now**: The regulation, platform, or AI shift making this timely.

   Prioritize opportunities backed by **existing spending**, **specific enough to be actionable**, and **where incumbents ignore the self-serve small-business tier**.

---

7. **Niche Risks**
   Identify the **most significant risks** observable from professional-layer signals.

   For each risk, provide: **Risk** (short label) · **Signal** (specific evidence) · **Severity** (Low / Medium / High) · **Mitigation angle**.

   Risk types to consider:
   * **Sales-led expectations** — buyers in this niche expect demos, security review, contracts; self-serve won't close them
   * **Well-funded entrants** — recent funding cluster means a marketing-spend war an indie can't win head-on
   * **Incumbent platform absorption** — the dominant vertical platform (practice-management suite, commerce platform) may ship the feature natively
   * **Regulatory exposure** — the workflow touches regulated data (health, finance, HR) raising compliance cost beyond indie scope
   * **Budget-cycle drag** — purchases happen on annual budget cycles, making self-serve monthly revenue slow to build
   * **AI obviation** — the role/workflow itself may shrink

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
Deliver a **data-backed, structured analysis** of **who in this niche has the pain, who has the budget, what they already spend, and whether a self-serve indie product can reach them** — separating practitioner-driven evidence from vendor marketing throughout.

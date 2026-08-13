---
prompt_for: communities
placeholder: "[NICHE]"
usage: Replace [NICHE] with the target topic (e.g., "agency reporting", "dental practice management", "Shopify inventory") before invoking.
---

**Objective:**
Identify and analyze **what practitioners and operators are discussing, complaining about, and paying for in [NICHE]** across builder and professional communities, using **credible, recent sources (published within the last 6 months)**.

---

**Instructions:**

1. **Source Criteria**

   * Use only **credible and recent sources (≤ 6 months old)**
   * At the beginning of the response, clearly state:
     **"Data observed as of [month/year]"**
   * Prioritize sources in this order:

     **Tier 1 — Practitioner communities (highest signal fidelity)**
     * Niche-professional subreddits (r/agency, r/smallbusiness, r/shopify, r/webdev, r/Dentistry, vertical equivalents) — top posts of the past 6 months, recurring complaint and "what do you use for X" threads
     * Hacker News — Ask HN / Show HN / launch threads touching the niche; comment sentiment on tools in the space
     * Indie Hackers — products in the niche with public revenue, milestone posts, "building in public" threads
     * Niche Slack/Discord communities and professional forums (name them; use whatever is publicly indexed or reported about them)

     **Tier 2 — Aggregated community signal**
     * GummySearch or similar pain-point aggregation across business subreddits
     * "Best tools for X" threads and their comment consensus (which tools practitioners actually endorse vs. which get pushback)
     * Facebook/LinkedIn groups for the vertical where publicly reported

     **Tier 3 — Corroborating sources**
     * Blog posts and newsletters by practitioners in the niche describing their stack and its gaps
     * Podcast episodes / MicroConf or vertical-conference talks naming recurring operational pains

---

2. **Trend Identification**
   Identify both:

   * **Established pains** (recurring high-engagement complaint themes, mature "what do you use" threads with consistent answers)
   * **Emerging / rising pains** (new recurring question types, workflow shifts, new-tool adoption debates, regulation or platform changes creating fresh problems)

   For each theme, note whether it is **community-specific** or **cross-community** (appearing in 2+ distinct communities — stronger signal).

---

3. **For EACH pain or discussion theme, provide:**

**A. Basic Information**

* Theme name
* Communities where it appears
* Type (recurring complaint, tool-seeking, workflow question, pricing rant, incumbent backlash, regulatory scramble, etc.)

**B. Description**

* What posts look like, quoting the operators' own vocabulary
* The underlying business pain: what it costs (hours/week, lost revenue, risk) and who feels it
* Whether current answers are "use tool X" (competitive), "cobble spreadsheets" (gap), or "hire someone" (service-replacement opportunity)

**C. Quantitative Metrics**

* Community sizes (subscribers/members) and activity levels
* Representative engagement (upvotes, comment counts) on the theme
* Frequency ("appears weekly in r/X")
* Cross-community reach

**D. Growth Analysis**

* For **rising themes only**: growth evidence (post-frequency increase, new communities forming, sudden spikes tied to platform/regulation changes), timeframe, and velocity classification (slow / moderate / explosive)

---

4. **Structure the Output**
   Organize findings into clearly separated sections:

* **1. Executive Summary (Key Insights)**
* **2. Established Pains**
* **3. Emerging / Rising Pains**
* **4. Key Communities & Theme Clusters**
* **5. Strategic Insights (positioning & distribution takeaways)**
* **6. Financial Opportunities** (per instruction 6 below)
* **7. Niche Risks** (per instruction 7 below)
* **8. Sources** (per instruction 8 below)

---

5. **Additional Analysis (Value Add)**
   Include:

* **Spreadsheet signal**: workflows operators run in spreadsheets/manual processes while complaining about it — the classic micro-SaaS entry point
* **Budget authority signal**: whether the person complaining can buy software themselves (owner/solo operator) or must ask someone (weaker self-serve fit)
* Tool-stack patterns: what the community's standard stack is, and which slot in it draws the most complaints
* Public revenue proof: Indie Hackers / building-in-public posts showing products in this niche earning real MRR
* Distribution note: which of these communities tolerate founder participation vs. ban promotion (matters for the go-to-market later)

---

6. **Financial Opportunities**
   Identify the **most monetarily interesting, not yet saturated problems** that operators in this niche are **already paying to solve** — with money or with hours of manual work. Base conclusions on realistic data (stated tool spend, community size, public revenue posts) — avoid speculative sizing.

   For each opportunity, provide:

   * **Problem**: What specifically are operators paying (or burning hours) to solve?
   * **Community signal**: Specific threads/patterns confirming real, recurring demand
   * **Evidence of willingness to pay**: Tools with adoption in the community, stated budgets, public MRR of comparable products, cost of the manual alternative
   * **Saturation assessment**: Crowded, or underserved segments / verticals / price tiers open to a new entrant?
   * **Realistic revenue math**: Bottoms-up (e.g., "community of N operators, X% report this pain monthly, comparable tools charge $Y/mo → addressable pool of $..."). Cite what it rests on.
   * **Why now**: The platform change, regulation, or workflow shift making this timely.

   Prioritize opportunities backed by **existing spending or time-burn**, **specific enough to be actionable**, and **not owned by an entrenched default**.

---

7. **Niche Risks**
   Identify the **most significant risks** observable from community signals.

   For each risk, provide: **Risk** (short label) · **Community signal** (specific evidence) · **Severity** (Low / Medium / High) · **Mitigation angle**.

   Risk types to consider:
   * **Anti-subscription sentiment** — operators in this vertical resent recurring software costs; prefer one-time or free tools
   * **DIY culture** — the community celebrates spreadsheet/self-built solutions; buying software is low-status
   * **Trust barrier** — operators won't put business data in a small vendor's tool (backup/security anxiety threads)
   * **Seasonal/cyclical demand** — the pain spikes seasonally (tax season, holiday commerce) creating boom-bust revenue
   * **Platform dependence** — the pain exists only inside one platform whose owner may fix it natively
   * **Sales-led drift** — buyers in this niche expect demos, contracts, onboarding calls — signals poor self-serve fit

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
Deliver a **data-backed, structured analysis** that surfaces **what operators in this niche actually struggle with, what they already pay for, and where a self-serve product could replace a spreadsheet, a manual process, or a resented incumbent**.

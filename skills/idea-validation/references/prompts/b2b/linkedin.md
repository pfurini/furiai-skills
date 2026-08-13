---
prompt_for: linkedin
placeholder: "[NICHE]"
usage: Replace [NICHE] with the bilingual niche wording ("<Italian> / <English>", e.g. "gestione scadenze studio legale / law-firm deadline management") before invoking. Search Italian-first.
---

**Objective:**
Identify and analyze **professional demand signals for [NICHE] visible through the Italian professional web** — LinkedIn posts and groups, job postings, trade press, association research, vendor activity, and public tenders — using **credible, recent sources (published within the last 6 months where possible)**.

Note on reachability: LinkedIn is only partially indexable. Public posts and job listings are observable; **group member rosters are impossible to obtain by design** (LinkedIn exposes them to no one — never claim otherwise); group post feeds are collectable cookieless via an Apify actor where the orchestrator provides tooling, otherwise treat groups as existence signals. State for every claim whether it comes from **direct observation** or **secondary reporting**.

---

**Instructions:**

1. **Source Criteria**

   * Search **Italian-first** (practitioners post in Italian), English second. Write the report in English; keep Italian quotes verbatim with a translation.
   * At the beginning of the response, clearly state: **"Data observed as of [month/year]"**
   * Prioritize sources in this order:

     **Tier 1 — Professional demand signals (Italy)**
     * **LinkedIn public posts and articles** in Italian on the niche — practitioner complaints, workflow debates, tool recommendations, "siamo passati da X a Y" posts. Record engagement where visible.
     * **LinkedIn groups**: discover relevant Italian groups (names, stated member counts from group search where visible); collect group posts only if tooling is provided (cookieless actor); otherwise label `existence signal`.
     * **Job postings** — LinkedIn Jobs and **Indeed Italia** (NOT InfoJobs: shut down 2025-12-31). A firm hiring a person to run this workflow manually is unmet software demand; postings naming specific tools measure incumbent penetration. **LinkedIn URL-filter caveat (since Aug 2026): only date-posted, company, easy-apply, and under-10-applicants filters survive; express seniority/type in the query text.** State every query used.
     * **Vendor activity**: Italian vendors in the niche — launch announcements, claimed customer counts (discount by half), hiring.

     **Tier 2 — Italian professional press & association research**
     * Trade press the buyers actually read: Il Sole 24 Ore / NT+ Fisco, ItaliaOggi (still publishing — verify current issues), Euroconference, Ipsoa/Wolters Kluwer portals, Fiscal Focus for fiscal niches; Altalex, Diritto.it and association channels for legal; Netcomm/Casaleggio streams for e-commerce.
     * Recurring research: CNDCEC / Fondazione Nazionale Commercialisti, Cassa Forense (Rapporto sull'Avvocatura), Consiglio Nazionale Forense, Osservatori PoliMi, Confartigianato/CNA/Confcommercio studies. These reveal persistent operational pains and technology-adoption attitudes with real sample sizes.
     * Conference/webinar agendas for the vertical (recurring session topics = recurring pains).

     **Tier 3 — Public tenders as market-language**
     * **ANAC open data** (dati.anticorruzione.it) and **TED** for [NICHE]-adjacent CPV codes: tender wording reveals buyer vocabulary and requirements; awards reveal incumbent concentration and realistic deal sizes. For micro-firm niches treat tenders as a language/compliance signal, not a lead source.

2. **Trend Identification**
   Identify both:
   * **Established demand** — long-running pain themes, mature vendor landscape, steady job-posting presence.
   * **Emerging / rising demand** — new pain themes tied to regulation (nuovi obblighi, scadenze), platform/AI shifts, spiking job-post language, new vendors funded or launched.

   For each theme, note whether the signal is **practitioner-driven** (operators describing their own pain — strongest), **association-driven** (survey/research — strong, lagging), or **vendor-driven** (marketing — weakest; discount accordingly).

3. **For EACH demand theme, provide:**

**A. Basic Information** — theme name; where it appears (posts, groups, jobs, press, research, tenders); type (workflow pain, compliance scramble, tool-switching wave, manual-role hiring, budget shift).

**B. Description** — what professionals say, in their Italian vocabulary (+ translation); the business pain underneath (hours, money, risk); which role owns it and whether that role can buy software without approval.

**C. Quantitative Metrics** — engagement on representative posts (where visible); job-posting counts with the exact query used; vendor signals (funding, claimed customers, headcount growth); research sample sizes; tender counts/values where relevant.

**D. Growth Analysis** — for rising themes only: growth evidence (posting-frequency change, job-listing growth, funding cluster, new research attention), timeframe, velocity (slow / moderate / explosive).

**E. Evidence labels** (mandatory) — **region** · **segment** · **firm-size proxy** · **stack named** · **regulatory dependency** (SDI, PCT, PEC, AML, GDPR, conservazione — or none) · **switching constraint** · **evidence type** (direct observation vs secondary reporting, and which surface) · **confidence** (high only if multi-source Italian or association-research-backed).

4. **Structure the Output**

* **1. Executive Summary (Key Insights)**
* **2. Established Demand**
* **3. Emerging / Rising Demand**
* **4. Professional Landscape** (roles affected, budget owners, vendor map, hiring patterns, association attention)
* **5. Strategic Insights (positioning & distribution takeaways)**
* **6. Financial Opportunities** (per instruction 5 below)
* **7. Niche Risks** (per instruction 6 below)
* **8. Disconfirming Evidence** (per instruction 7 below)
* **9. Sources**

5. **Financial Opportunities**
   Identify problems Italian businesses in this niche demonstrably spend on — software subscriptions, consultant/agency fees, or salaried hours. For each: **Problem** · **Professional signal** (posts/jobs/research confirming recurring demand) · **Evidence of willingness to pay** (vendor traction; salary ranges from job posts bound the software's value; consultant fees for the same job) · **Saturation assessment** (vendor density; whether incumbents ignore the micro/small tier — the ignored tier is the indie wedge) · **Realistic revenue math** (bottoms-up from ISTAT/ordini counts × observed EUR prices; cite what it rests on) · **Why now** (regulation, platform, or AI shift).

6. **Niche Risks**
   For each: **Risk** · **Signal** · **Severity (Low/Medium/High)** · **Mitigation angle**. Consider at least: **sales-led expectations** (buyers expect demos/dealers — self-serve invisible); **well-funded entrants**; **incumbent absorption** (TeamSystem/Zucchetti-class shipping the feature); **regulatory exposure** (workflow touches regulated data — compliance cost beyond indie scope); **budget-cycle drag** (annual decisions with the commercialista); **AI obviation**; **manual-labor substitution** (at Italian wage levels, hiring stays cheaper than software for some workflows — check the salary math both ways).

7. **Disconfirming Evidence** (mandatory)
   What argues AGAINST: declining job-post language, association research showing satisfaction or non-adoption attitudes, vendor exits, tender language locking the workflow into incumbents.

8. **Sources** — end with a `## Sources` section listing every URL consulted as markdown links.

---

**Goal:**
Deliver a **data-backed analysis of who in the Italian [NICHE] has the pain, who has the budget, what they already spend, and whether a self-serve indie product can reach them** — separating practitioner-driven evidence from vendor marketing, direct observation from secondary reporting, throughout.

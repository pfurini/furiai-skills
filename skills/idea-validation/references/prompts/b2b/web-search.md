---
prompt_for: web-search (b2b, Italy-first)
placeholder: "[NICHE]"
usage: Replace [NICHE] with the bilingual niche wording ("<Italian> / <English>") before invoking. Search Italian-first.
---

**Objective:**
Measure **Italian query demand for the [NICHE] niche**: what buyers type into Google.it, what the SERP serves them, and whether the demand is commercial. Italian-language queries first (the buyer vocabulary is Italian: "gestionale", "software resi", "portale documenti clienti"), English second and labeled as such.

---

**Instructions:**

1. **Source Criteria**

   * Use only **credible and recent sources (≤ 6 months old)**; open with **"Data observed as of [month/year]"**.
   * **Keyword volumes:** if no Italian keyword instrument is available this session (SEOZoom, DataForSEO), state plainly — once, near the top — that **Italian keyword demand is unmeasured**, and treat every volume claim below as qualitative. Never substitute global (EN) volumes for Italian demand; label them `geography: non-IT`, directional only.
   * Prioritize sources in this order:

     **Tier 1 — Direct Google.it SERP observation (your primary instrument)**
     * Search the Italian buyer-vocabulary queries and record what actually ranks: which vendors, which content formats, whether ads appear (ads = advertiser willingness to pay), which People-Also-Ask questions surface. A SERP observation is evidence; cite the query verbatim.

     **Tier 2 — Italian keyword & trend instruments**
     * Google Trends (region: Italy) — relative demand direction for the core queries, seasonality against the fiscal calendar
     * SEOZoom blog and published analyses — the Italian keyword instrument; cite its data when an article exposes it

     **Tier 3 — Italian trade press and vendor content marketing as demand evidence**
     * Vendor blog posts targeting the niche's queries (their SEO investment is a demand signal), Italian trade press covering the pain, comparison articles ("migliori software per …")

     **Tier 4 — Global SEO authorities (directional only, label non-IT)**
     * Ahrefs / Semrush / Moz / Exploding Topics analyses of the global category — pattern and growth context, never Italian volume

2. **Trend Identification**
   Identify both **established demand** (stable Italian query clusters, entrenched SERP categories) and **emerging / rising demand** (new query patterns, rising clusters not yet served by Italian-language content).

3. **For EACH trend or keyword cluster, provide:**

   **A. Basic Information** — cluster name; intent category (informational, commercial, transactional, comparison, problem-driven).

   **B. Description** — the Italian queries in the cluster (verbatim, with translation); the buyer problem behind them; why demand is moving (regulatory deadline, platform change, cultural shift, seasonality).

   **C. Quantitative Metrics** — measured Italian volume if an instrument provided it; otherwise the qualitative proxies you actually observed (Trends direction, SERP ad density, number of vendors investing in the query) — never an invented number.

   **D. Growth Analysis** — for rising clusters only: growth evidence with its date, and a velocity classification (slow / moderate / explosive).

   **E. Evidence labels** (mandatory, per finding — exactly one line, this exact shape, always with every slot — write `n/a` for a slot you cannot fill; the scoring step counts `geography: IT` label lines mechanically for the evidence gate):

   `labels — geography: <IT | non-IT> · region: <national | North | Centre | South | province name | n/a> · segment: <commercialista | avvocato | consulente del lavoro | artigiano | merchant | agency | generic PMI | other> · stack: <software named | n/a> · evidence: <query | SERP observation | trends data | article | pricing page> · confidence: <high | medium | low>`

   Confidence: **high** only when two independent Italian-language sources agree, or one is interview-/association-research-confirmed; **medium** for a single Italian source; **low** for non-IT or vendor-supplied.

4. **Structure the Output**

   * **1. Executive Summary (Key Insights)**
   * **2. Established Demand**
   * **3. Emerging / Rising Demand**
   * **4. Key Keyword Clusters** (grouped by intent, Italian queries verbatim with translations)
   * **5. Strategic Insights** (SERP formats that win, content and positioning takeaways)
   * **6. Financial Opportunities** (per instruction 5 below)
   * **7. Niche Risks** (per instruction 6 below)
   * **8. Disconfirming Evidence** (per instruction 7 below)
   * **9. Sources**

5. **Financial Opportunities**
   Identify the most monetarily interesting, not-yet-saturated **commercial-intent** clusters. For each: the queries indicating readiness to pay; evidence of commercial value (SERP ads, vendor SEO investment, published CPC when available); saturation of the Italian SERP; **realistic revenue math** (bottoms-up; cite what it rests on; never present a national firm-count (e.g. the 4.27M micro-firm figure) as an addressable pool — size from the reachable, qualified subset and say how you narrowed it); why now.

6. **Niche Risks**
   For each risk: label, the specific Italian-SERP or query evidence, severity (Low / Medium / High), and a mitigation angle. Consider: AI Overviews answering the core queries zero-click on Google.it; SERP moat held by incumbent-suite domains or high-authority Italian portals; informational-only intent (volume without ads); demand migrating off Google; fiscal-calendar seasonality (boom-bust around scadenze); sensitive-category ad restrictions.

7. **Disconfirming Evidence**
   Report what you looked for and did **not** find, and any evidence that cuts against the demand story: queries you expected that show no Italian footprint, SERPs where free/incumbent answers fully satisfy the intent, clusters where volume is visibly declining. An empty Italian SERP for a buyer query is a finding.

8. **Sources**
   End with a `## Sources` section listing every URL consulted as markdown hyperlinks, even if not directly quoted, using the page title as the label.

---

**Goal:**
Deliver a **data-backed, structured analysis** of Italian query demand: what buyers search, what intent sits behind it, what the SERP already answers, and where unmet commercial demand leaves room for a new entrant.

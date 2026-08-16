---
prompt_for: communities
placeholder: "[NICHE]"
usage: Replace [NICHE] with the bilingual niche wording ("<Italian> / <English>", e.g. "fatturazione per artigiani / invoicing for tradespeople") before invoking. Search Italian-first.
---

**Objective:**
Identify and analyze **what Italian operators and practitioners are discussing, complaining about, and paying for in [NICHE]** across Italian communities and their few relevant international counterparts, using **credible, recent sources (published within the last 6 months where the surface allows)**.

---

**Instructions:**

1. **Source status discipline (read first)**

   Italian community surfaces die, degrade, and hide behind login walls. Label every surface you use with one of:
   * **Active** — you observed a dated artifact within ~90 days (post, thread, timestamp).
   * **Degraded** — the surface exists but last activity is months/years old. Say so; do not mine it as live signal.
   * **Unverifiable** — login wall or bot block prevented observation. This is NOT evidence of death; report it as unverifiable and move on.
   * Never invent member counts or activity levels. If the platform hides them, write "not visible".

   Known state as of 2026-08 (re-verify, do not assume): **Forum GT is dead** (parked domain); its successor connect.gt is a degraded archive; **InfoJobs Italia shut down 2025-12-31**; the Telegram channel @commercialistatelematico is dead. **ItaliaOggi** is still publishing as of 2026-08 (re-verify, do not assume). There is **no open Italian forum for avvocati** — for legal niches, lean on Tier 3 sources and expect the evidence-sufficiency gate to fire.

2. **Source Criteria**

   * Search **Italian-first**; use only sources you can date. Write the report in English; keep Italian quotes verbatim with a translation.
   * At the beginning of the response, clearly state: **"Data observed as of [month/year]"**
   * Prioritize sources in this order:

     **Tier 1 — Readable Italian practitioner surfaces (highest pain-mining value)**
     * **Fisco Forum (fiscoetasse.com/forum)** — the anchor surface for commercialisti/fiscal niches: tens of thousands of public threads, per-board last-post dates visible. Mine recurring complaint and "che software usate per X" threads.
     * **r/commercialisti**, **r/ItalyInformatica**, **r/partitaiva** and other Italian subreddits with observed recent posts (subscriber counts often not visible — don't invent).
     * Public Facebook groups for the vertical (some are readable without login — check; e.g. small open groups like "Commercialisti del Lavoro HUB"). Big private groups (e.g. "Fatti di E-Commerce", ~22K members) are **existence signals only**: note them, don't claim their content.
     * Vertical portals with comment/QA sections (CommercialistaTelematico, AteneoWeb-class) — verify activity first.

     **Tier 2 — Structured community signal**
     * Association working groups and event calendars as leading indicators (Netcomm working groups for e-commerce, 4eCom, local ordini events): session titles = the vertical's current pains.
     * Annual community reports (Casaleggio "Ecommerce Italia", association surveys) for trend corroboration.
     * YouTube webinar comments and Italian podcast episodes for the vertical.

     **Tier 3 — International, ONLY where the niche warrants it**
     * HN / Indie Hackers / English subreddits: for dev tools and globally-uniform workflows only. Label these findings `geography: non-IT` — they prove the pain class exists, not that Italian buyers have it.

     **Opt-in (off by default):** member-assisted collection from private groups the user personally belongs to (via an Apify group-posts actor with the user's own session). Only if the orchestrator's dispatch explicitly enables it; output must be pain-themes only, never contact data, and findings get `evidence type: member-assisted (private group)`.

3. **Trend Identification**
   Identify both:
   * **Established pains** — recurring high-engagement complaint themes, mature "che software usate" threads with consistent answers.
   * **Emerging / rising pains** — new recurring question types tied to regulation (new obblighi, scadenze), platform changes, or AI adoption debates.

   For each theme, note whether it is **single-surface** or **cross-surface** (2+ distinct communities — stronger), and whether answers are "use tool X" (competitive), "arrangiarsi con Excel" (gap — the classic micro-SaaS entry), or "lo fa il commercialista / lo faccio fare" (delegated — the buyer may be the intermediary, not the firm).

4. **For EACH pain or discussion theme, provide:**

**A. Basic Information** — theme name; surfaces where it appears (with status labels); type (recurring complaint, tool-seeking, workflow question, pricing rant, regulatory scramble, incumbent backlash).

**B. Description** — what posts look like, quoting the operators' own Italian vocabulary (+ translation); the underlying business pain (hours/week, lost revenue, compliance risk) and who feels it; whether the complainer can buy software alone (owner/titolare) or must go through someone.

**C. Quantitative Metrics** — thread/message counts and last-post dates where visible; representative engagement; frequency ("appears weekly on Fisco Forum"); cross-surface reach. Write "not visible" where the platform hides numbers.

**D. Growth Analysis** — for rising themes only: growth evidence (post-frequency change, new groups forming, spikes tied to a scadenza or platform change), timeframe, velocity (slow / moderate / explosive).

**E. Evidence labels** (mandatory, per finding — exactly one line, this exact shape, always with every slot — write `n/a` for a slot you cannot fill; the scoring step counts `geography: IT` label lines mechanically for the evidence gate):

`labels — geography: <IT | non-IT> · region: <national | North | Centre | South | province name | n/a> · segment: <commercialista | avvocato | consulente del lavoro | artigiano | merchant | agency | generic PMI | other> · size: <firm-size proxy | n/a> · stack: <software named | n/a> · regdep: <SDI | PCT | PEC | AML | GDPR | conservazione | none> · switching: <constraint | n/a> · evidence: <thread | post pattern | poll | member-assisted | article> · confidence: <high | medium | low>`

Confidence: **high** only when two independent Italian-language sources agree, or one is interview-/association-research-confirmed; **medium** for a single Italian source; **low** for non-IT or vendor-supplied.

5. **Structure the Output**

* **1. Executive Summary (Key Insights)**
* **2. Established Pains**
* **3. Emerging / Rising Pains**
* **4. Surface Inventory** (every surface used, with status label and pain-mining value)
* **5. Strategic Insights (positioning & distribution takeaways — incl. which communities tolerate founder participation)**
* **6. Financial Opportunities** (per instruction 6 below)
* **7. Niche Risks** (per instruction 7 below)
* **8. Disconfirming Evidence** (per instruction 8 below)
* **9. Sources**

6. **Financial Opportunities**
   Identify the most monetarily interesting, not yet saturated problems Italian operators **already pay to solve** — with money or with hours. For each: **Problem** · **Community signal** (specific threads/patterns) · **Evidence of willingness to pay** (tools adopted, stated budgets, cost of the manual alternative in hours × loaded wage) · **Saturation assessment** · **Realistic revenue math** (bottoms-up; cite what it rests on; never present the 4.27M Italian micro-firm count as an addressable pool) · **Why now**.

7. **Niche Risks**
   For each: **Risk** · **Community signal** · **Severity (Low/Medium/High)** · **Mitigation angle**. Consider at least: **anti-subscription sentiment** (strong in Italian micro-business culture — preference for one-time/local); **DIY-Excel culture**; **trust barrier** (business data with a small unknown vendor); **seasonality** (scadenze fiscali cycles); **delegation** (the pain is felt by the firm but solved by the commercialista — the apparent buyer isn't the buyer); **community unreachability** (the segment's discussion happens in private/offline spaces you cannot mine — this inflates false negatives).

8. **Disconfirming Evidence** (mandatory)
   What argues AGAINST the niche: threads showing tolerance without budget, free tools praised as sufficient, declining post frequency, communities that exist but never discuss the pain.

9. **Sources** — end with a `## Sources` section listing every URL consulted as markdown links.

---

**Goal:**
Deliver a **data-backed, honestly-labeled analysis** of what Italian operators in [NICHE] struggle with, what they already pay for, and where a self-serve product could replace a spreadsheet, a manual process, or a resented incumbent — with every claim carrying its surface status, segment, and confidence, and with unreadable surfaces reported as unreadable rather than silently skipped.

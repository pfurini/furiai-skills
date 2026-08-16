---
prompt_for: incumbents
placeholder: "[NICHE]"
usage: Replace [NICHE] with the bilingual niche wording ("<Italian> / <English>", e.g. "gestione studio commercialista / accounting practice management") before invoking. Search Italian-first.
---

**Objective:**
Map **the Italian incumbent-software reality around [NICHE]** — which suites Italian micro/small businesses and professional firms already run, where those suites fail them, and where a third-party tool can plug in beside them — using **credible, recent sources (≤ 12 months for sentiment; current pages for pricing/APIs)**.

Why this platform exists: in Italy, most professional and SMB workflows live inside a few vertical incumbents (TeamSystem, Zucchetti, Wolters Kluwer Italia, Buffetti, Danea, Namirial, Aruba and their sub-brands). Buyers rarely replace the core suite — migration risks tax, payroll, litigation, and compliance data — so the credible indie entry is almost always an **add-on, integration, or works-beside wedge**. This research maps that surface. G2-style review platforms barely see it.

---

**Instructions:**

1. **Source Criteria**

   * Search **Italian-first** (vendor pages, forums, and buyer complaints are in Italian), English second. Write the report in English; keep Italian quotes verbatim with a translation.
   * At the beginning of the response, clearly state: **"Data observed as of [month/year]"**
   * Prioritize sources in this order:

     **Tier 1 — Incumbent vendor surfaces (the category map)**
     * Identify the 3–6 incumbent products Italian buyers in [NICHE] actually run. Start from the known families and their sub-brands: TeamSystem (incl. Fatture in Cloud, TeamSystem Commerce/ex Storeden, TS Studio), Zucchetti, Wolters Kluwer Italia (Genya, Kleos, Ipsoa), Lefebvre Giuffrè (Cliens), Danea (Easyfatt), Buffetti, Namirial, Aruba, GBsoftware, Sistemi — plus any vertical specialist the niche uses.
     * For each: current **pricing pages** (record EUR, billing unit, ex-VAT), **release notes / "novità" pages** (what they ship = where they're headed), **knowledge bases and support forums** (what users struggle with), **integration/partner/API pages** (what a third party may build).

     **Tier 2 — The integration economy around the incumbents**
     * Marketplaces and app stores where they exist: **Fatture in Cloud App Store** (open, free publication) and **TeamSystem Commerce Apps Market**; note that Zucchetti/Wolters Kluwer/Buffetti have no open app store (partner-gated or closed).
     * Third-party connector vendors and wrappers that grew around API gaps (e.g. the Danea Easyfatt connector ecosystem) — their existence proves paid demand for integration.
     * Migration guides, "come esportare da X" threads, freelancer-marketplace requests to build bridges between systems.

     **Tier 3 — Buyer sentiment on the incumbents**
     * Trustpilot.it / Google reviews of the incumbent products; complaint threads in professional forums; comparison articles ("migliori gestionali [current year]", "alternative a [incumbent]").

2. **For EACH incumbent product, provide:**

**A. Identity** — vendor, product, the [NICHE] job it owns, claimed customer base (record the claim verbatim and attribute it to the vendor; treat it as marketing, not evidence, and keep it out of revenue math unless a second independent source corroborates it).

**B. Pricing observed** — EUR, billing unit (per azienda / per utente / per postazione), ex-VAT vs incl., quote-only where list prices are not published (quote-only is itself a finding: it marks the dealer-mediated tier).

**C. Openness for a third party** — one of: **open** (public API + self-serve app distribution), **paywalled** (API exists but tier-gated or paid), **partner-gated** (contact-form / reseller program), **closed** (no API; file exchange or DB access only). Cite the page.

**D. Failure themes** — what users complain about, in their vocabulary (quote + translate). Distinguish **category-wide** pains (recur across incumbents — real market gaps) from **product-specific** ones (displacement wedge against one vendor).

**E. Absorption risk** — is the vendor shipping toward [NICHE]? Recent releases, acquisitions, AI features that could absorb the wedge natively.

**F. Evidence labels** (mandatory, per finding — exactly one line, this exact shape, always with every slot — write `n/a` for a slot you cannot fill; the scoring step counts `geography: IT` label lines mechanically for the evidence gate):

`labels — geography: <IT | non-IT> · region: <national | North | Centre | South | province name | n/a> · segment: <commercialista | avvocato | consulente del lavoro | artigiano | merchant | agency | generic PMI | other> · size: <firm-size proxy | n/a> · stack: <software named | n/a> · regdep: <SDI | PCT | PEC | AML | GDPR | conservazione | none> · switching: <constraint | n/a> · evidence: <vendor page | forum | review | connector market | press> · confidence: <high | medium | low>`

Confidence: **high** only when two independent Italian-language sources agree, or one is interview-/association-research-confirmed; **medium** for a single Italian source; **low** for non-IT or vendor-supplied.

3. **Wedge analysis (the core deliverable)**

   For each viable entry point, state:
   * **The wedge**: the recurring workload the incumbent leaves manual or clumsy (re-keying between systems, client document collection, deadline tracking, reporting the suite exports badly).
   * **The attach surface**: which incumbent it plugs into and through what (API, file exchange, marketplace listing) — and the openness class from C.
   * **Who buys**: the firm itself vs the professional studio managing many firms (a studio-side tool multiplies value per seat across its clients).
   * **Switching constraint it avoids**: the wedge must NOT require replacing the suite or migrating compliance data.
   * Label each wedge with the same evidence labels (F above).

4. **Structure the Output**

* **1. Executive Summary (Key Insights)**
* **2. Incumbent Map** (per-product A–F)
* **3. Category-Wide Failure Themes**
* **4. Wedge Analysis** (per instruction 3)
* **5. Strategic Insights (positioning & distribution takeaways — incl. which marketplace/API route is open)**
* **6. Financial Opportunities** (per instruction 5 below)
* **7. Niche Risks** (per instruction 6 below)
* **8. Disconfirming Evidence** (per instruction 7 below)
* **9. Sources**

5. **Financial Opportunities**
   Identify the problems Italian firms in [NICHE] are **already paying to solve** — incumbent module prices, connector-vendor prices, hours of manual re-keying. For each: **Problem** · **Incumbent signal** (module price, forum complaint volume, connector demand) · **Evidence of willingness to pay** (EUR figures observed) · **Saturation** (is the integration slot already crowded?) · **Realistic revenue math** (bottoms-up from firm counts × observed EUR prices; cite what it rests on; never present a national firm-count (e.g. the 4.27M micro-firm figure) as an addressable pool — size from the reachable, qualified subset and say how you narrowed it) · **Why now** (regulation deadline, incumbent neglect, new API).

6. **Niche Risks**
   For each: **Risk** · **Signal** · **Severity (Low/Medium/High)** · **Mitigation angle**. Consider at least: **incumbent absorption** (vendor ships the feature); **API dependency** (the one open API changes terms — TeamSystem's API licence is revocable); **dealer-channel lock** (buyers only trust the incumbent's dealer, self-serve invisible); **compliance drift** (the workflow touches SDI/PCT/AML — errors carry legal exposure); **quote-only opacity** (can't verify the competing price).

7. **Disconfirming Evidence** (mandatory)
   What argues AGAINST entering: satisfied-user evidence, an incumbent already shipping the fix, a connector market that stayed tiny, forums showing tolerance rather than budget ("fastidioso ma gratis" patterns).

8. **Sources** — end with a `## Sources` section listing every URL consulted as markdown links, including pages consulted but not quoted.

---

**Goal:**
Deliver a **data-backed map of the Italian incumbent landscape for [NICHE]**: what firms already run and pay, exactly where a self-serve add-on can attach (and through which open door), and which wedges the incumbents will tolerate versus absorb.

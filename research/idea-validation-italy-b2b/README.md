# Italy B2B research — raw reports (Phase A of PLAN-italy-refactor.md)

Five web-research reports (2026-08-13, exa-backed, bilingual queries) behind the
Italy-first rewrite of `skills/idea-validation/references/calibration/b2b/` and
`references/prompts/b2b/`. Same discipline as the sibling
`idea-validation-b2b-benchmarks/` reports: every figure carries source + date +
confidence, and each report ends with a "does not exist publicly" log — data absent
from those logs must not be invented in the packs.

## Reports

- `icp-universe-adoption.md` — enterprise universe by size class and ATECO,
  professional-firm counts, digital adoption, business demography (feeds
  market-sizing).
- `price-anchors-incumbents.md` — EUR price bands from vendor pricing pages, incumbent
  ecosystem/API map (feeds pricing, competitor-sources, distribution).
- `channels-legal.md` — Italian paid-channel units, outreach law (art. 130, Garante),
  alternative channels, intermediary buying (feeds cac, distribution).
- `communities-signal-surface.md` — verified-active communities and signal surfaces
  per vertical, with dead/degraded/unverifiable explicitly separated (feeds the trend
  prompts).
- `tooling-matrix.md` — ranked integration matrix per research job, curl-verified
  endpoints, script shortlist, env-var list (feeds the tooling reference + scripts).

## Findings that change the packs (headline synthesis)

1. **Cold email and cold PEC are prohibited without prior opt-in consent** (art. 130
   Codice privacy; Garante fined PEC scraping €20K, 2021; public availability of the
   address is not a legal basis). `cold_outbound` becomes a hard "prohibited in Italy"
   entry with the compliant bridge (RPO-screened phone → documented consent → email)
   and soft-spam (own customers) as the only email paths.
2. **The self-serve ceiling in Italy is ~€50/month ex-VAT** — above it the purchase
   motion shifts to demo/contract/dealer (observed across pricing pages, not a budget
   ceiling). This number calibrates the guardrail's middle band and the pricing pack's
   no-approval threshold.
3. **For accounting/payroll/tax categories the micro firm is often not the buyer**:
   ~75% of taxpayers file through a commercialista, ~80% of companies use a consulente
   del lavoro. The ICP for those categories redirects from ~4.27M micro firms to
   ~69K studi + ~26K consulenti del lavoro. Market-sizing must model the studio as
   the buyer and the firm as the beneficiary.
4. **The 4.27M micro-enterprise count must never be presented as TAM**: no adoption
   data of any kind exists for firms <3 addetti (~3.5M of them); the plausible paying
   population is hundreds of thousands, not millions. ISTAT/DESI adoption stats have a
   10+ addetti frame (94.8% of firms excluded) — every adoption figure must carry its
   size base.
5. **Fatture in Cloud is the standout incumbent distribution surface** (free universal
   API, free App Store publication, 500K+ businesses, 16K accountants). Zucchetti is
   reseller-gated, Kleos API is top-tier-paywalled, Danea has no API, TeamSystem group
   portal is SSO-gated. The distribution pack gets a ranked incumbent-surface table.
6. **Named-surface corrections for the prompts**: InfoJobs Italia dead (2025-12-31);
   Forum GT dead, connect.gt degraded; ItaliaOggi alive; no open Italian forum exists
   for avvocati (expect the evidence-sufficiency gate to fire in legal niches);
   FiscoeTasse Fisco Forum + r/commercialisti are the active commercialisti surfaces;
   the biggest e-commerce community (Fatti di E-Commerce, 22.4K) is private-unreadable
   — trend evidence comes from Casaleggio/Netcomm report streams instead. Private FB
   groups are existence signals by default (an opt-in member-assisted Apify path
   exists — see the tooling-matrix addendum); LinkedIn group POSTS are minable
   cookieless via Apify (member rosters remain impossible by design).
7. **Eurostat replaces ISTAT SDMX as the shipped stats source** (ISTAT endpoint down/
   filtered on every variant tried; Eurostat verified working, keyless). TED v3 and
   ANAC CKAN verified keyless. Openapi.com `/impresa` is the practical Registro
   Imprese route (~€1/1K calls, ATECO/province/size filters); Cerved/CRIBIS/Atoka are
   sales-led, OpenCorporates uneconomic.
8. **Paid channels**: Google B2B-intent CPC €1.50–4.00 (planning range, low
   confidence — no Italy-cut study exists), Meta ~€0.43 CPC, LinkedIn not viable below
   ~€2K/month (~€207 CPL). SEOZoom (€76/mo, API) is the Italian keyword instrument.
9. **Business demography is mildly positive and shifting to società di capitali**
   (+0.56%/quarter stock growth, professional services among the fastest sectors) —
   a usable trend anchor for market-sizing.
10. **Figure correction**: the "~69,000 studi / 290K addetti" commercialisti figure is
    from CNDCEC Stati Generali May 2024, not 2026 — cite it as 2024.

## Provisioning (user actions)

- Env keys worth provisioning: `APIFY_TOKEN` (reviews + job posts — hard gate),
  `OPENAPI_TOKEN` (ICP counts — hard gate), `EXA_API_KEY`, `DATAFORSEO_LOGIN/PASSWORD`
  (optional; $50 minimum deposit). Eurostat/TED/ANAC need no keys.
- Manual pulls DONE (2026-08-13): MicroConf State of Independent SaaS 2024 and
  SaaS Capital RB32 retention benchmarks — PDFs in this directory, extraction in
  `gated-pdf-digests.md`. Still pending: AssoSoftware/Osservatori "Il software
  gestionale in Italia" (only a 2022 announcement found); RPO tariff tables
  (DM 20/12/2024 and 22/12/2025) if the phone-consent bridge is ever modeled.

# Research tooling (harness-portable)

How the skill's research steps reach the web and data sources, in mandatory
preference order. This file is passed via `EXTRA:` to B2B trend researchers
and the market sizer; the orchestrator applies it too. Verified 2026-08
(`research/idea-validation-italy-b2b/tooling-matrix.md` is the source
record).

## Routing rule

1. **Scripts first** (`scripts/` in this skill — bash + curl + jq only,
   keys via env vars) for every source that has a stable API.
2. **Harness web tools by capability** for everything else: "your web
   search tool" (e.g. pi-web-access `web_search` — batch queries,
   `domainFilter`, `recencyFilter`; or any equivalent), "your page fetch
   tool" (`fetch_content` — also converts PDFs), "your claim-check tool"
   (`source_check`) when available. Never name harness-specific tools in
   artifacts; describe the capability.
3. **Manual steps** for gated sources — list them for the user, never
   automate logins.

## Script index

| Script | Source | Needs | Job |
|---|---|---|---|
| `eurostat_enterprises.sh <NACE> [year] [geo] [indic]` | Eurostat `sbs_sc_ovw` | nothing | Enterprise counts by size class (the ICP-universe backbone; e.g. `M69` = legal+accounting) |
| `ted_tenders.sh <CPV8> [country] [days] [limit]` | TED Search API v3 | nothing | EU tender notices as market-language/deal-size signal |
| `anac_dataset.sh <dataset-id\|list>` | ANAC CKAN open data | nothing | Below-EU-threshold Italian procurement datasets |
| `apify_run.sh <owner~actor> [input.json]` | Apify REST | `APIFY_TOKEN` | Any store actor: reviews (Capterra/Trustpilot/G2), job posts (LinkedIn/Indeed), LinkedIn group posts (cookieless actors only), Facebook public groups |
| `exa_search.sh "<query>" [n]` (`EXA_MODE=answer` for cited answers) | Exa API | `EXA_API_KEY` | Semantic search / claim checking when no harness search tool is available |

Business-register drill-down (ATECO × province × size × revenue):
Openapi.com `GET /impresa` — €0.001/request, up to 1,000 companies per
request, `OPENAPI_TOKEN`; free sandbox at `test.visurecamerali.openapi.it`.
No script shipped yet — call it with curl per its console docs. Italian
keyword volumes: DataForSEO (Basic auth, `DATAFORSEO_LOGIN`/`_PASSWORD`,
$50 minimum deposit, SERP $0.0006/query) — otherwise treat Italian search
volume as unmeasured and say so.

## Hard-won endpoint facts (do not rediscover these)

- **ISTAT SDMX is not a dependable source**: endpoint 302s to a maintenance
  page from public networks (verified 2026-08); a naive `curl -L` sees HTTP
  200 from the block page. Eurostat carries the same business-structure
  data. If ISTAT is ever retried: validate the body parses as SDMX, and
  remember `endPeriod` is off by one (pass N−1 for year N).
- **ANAC serves an HTTP-200 WAF block page** to curl's default User-Agent —
  the script sets a browser UA and asserts `"success": true`.
- **TED v3** is POST-only, `fields` mandatory, CPV must be 8-digit
  (`72000000`, not `72`).
- **LinkedIn**: no official job/group APIs. Jobs actors work cookieless;
  since Aug 2026 LinkedIn job URLs honor only date/company/easy-apply/
  under-10-applicants filters — put everything else in the query text.
  Group member rosters are impossible by design (admins + active posters
  only). Avoid any actor that wants `li_at` session cookies.
- **Facebook private groups**: member-assisted only (user's own membership
  + cookies), off by default, pain-themes only — see the communities
  prompt.
- **Cerved / CRIBIS / Atoka are sales-led** (no self-serve API);
  OpenCorporates is uneconomic for Italian sizing. Openapi.com is the
  practical Registro Imprese route.

## Env vars (provision once, all optional-with-degradation)

| Var | Unlocks | Without it |
|---|---|---|
| `APIFY_TOKEN` | Review/job/group scraping | Those signals degrade to manual browsing |
| `OPENAPI_TOKEN` | Company search by ATECO/province/size | ICP sizing falls back to Eurostat aggregates |
| `EXA_API_KEY` | Scripted search/claim-check | Fine under a harness with web tools |
| `DATAFORSEO_LOGIN`+`_PASSWORD` | Italian keyword/SERP data | Keyword demand stays unmeasured — flag it |

# Research tooling (harness-portable)

The script index and endpoint facts behind the skill's research steps (the
routing order itself lives in SKILL.md). This file is passed via `EXTRA:` to B2B trend researchers
and the market sizer; the orchestrator applies it too. Verified 2026-08
(`research/idea-validation-italy-b2b/tooling-matrix.md` is the source
record).

Routing (scripts first → harness web tools by capability → manual for
gated sources) is defined in SKILL.md; this file carries the script index
and endpoint facts.

## Script index

| Script | Source | Needs | Job |
|---|---|---|---|
| `eurostat_enterprises.sh <NACE> [year] [geo] [indic]` | Eurostat `sbs_sc_ovw` | nothing | Enterprise counts by size class (the ICP-universe backbone; e.g. `M69` = legal+accounting) |
| `preflight_providers.sh` | free/cheapest call per provider | reads all provider env vars | Run BEFORE Wave 1 of any research run: verifies each configured credential and names the broken one (a set-but-empty var is the classic failure); unset vars are reported as not-configured with the degradation path |
| `ted_tenders.sh <CPV8> [country] [days] [limit]` | TED Search API v3 | nothing | EU tender notices as market-language/deal-size signal |
| `anac_dataset.sh <dataset-id\|list>` | ANAC CKAN open data | nothing | Below-EU-threshold Italian procurement datasets |
| `apify_run.sh <owner~actor> [input.json]` | Apify REST | `APIFY_TOKEN` | Any store actor: reviews (Capterra/Trustpilot/G2), job posts (LinkedIn/Indeed), LinkedIn group posts (cookieless actors only), Facebook public groups |
| `exa_search.sh "<query>" [n]` (`EXA_MODE=answer` for cited answers) | Exa API | `EXA_API_KEY` | Semantic search / claim checking when no harness search tool is available |
| `openapi_impresa_count.sh <ateco> [province] [minEmp] [maxEmp]` (`OPENAPI_TURNOVER="min-max"`, `OPENAPI_SAMPLE=n`) | Registro Imprese via Openapi.com Company API `GET /IT-search` | `OPENAPI_TOKEN` | Company counts by ATECO × province × employees × turnover; **count-only via `dryRun` (free ~100/day in prod, then ~€0.01/call)** — use it for ICP counts before pulling any list; sample lists €0.001/request up to 1,000 companies; free sandbox `test.company.openapi.com` (script verified there 2026-08) |
| `dataforseo_volume.sh "kw1,kw2,..." [loc=2380] [lang=it]` | DataForSEO Google Ads API (Basic auth) | `DATAFORSEO_LOGIN`/`_PASSWORD` | Italian keyword volumes + CPC + competition, up to 1,000 kw per ~$0.09 live task (verified 2026-08); without credentials treat Italian search volume as unmeasured and say so |
| `dataforseo_serp.sh "<query>" [depth=10] [loc=2380] [lang=it]` | DataForSEO SERP API live advanced | `DATAFORSEO_LOGIN`/`_PASSWORD` | google.it SERP observation (~$0.002/query, verified 2026-08): organic ranks, ads-present, People-Also-Ask, item-type mix (AI Overview visibility included) |

## Hard-won endpoint facts (do not rediscover these)

- **Openapi ATECO codes take no dots**: `atecoCode=6201` returns real counts
  (7,699 IT companies, verified 2026-08-17); `62.01`, `620100` and `62.01.00`
  all return `{"count":0,"success":true}` — a silent zero, not an error.
  `openapi_impresa_count.sh` now strips dots for you.
- **Openapi tokens are environment-scoped**: a production token is rejected by
  `test.company.openapi.com` with `{"success":false,"message":"Wrong Token"}`.
  Testing only the sandbox reports a working production token as broken;
  `preflight_providers.sh` now tries both and names the proven scope.

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

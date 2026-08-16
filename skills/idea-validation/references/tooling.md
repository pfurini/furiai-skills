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
| `ted_tenders.sh <CPV8> [country] [days] [limit]` | TED Search API v3 | nothing | EU tender notices as market-language/deal-size signal |
| `anac_dataset.sh <dataset-id\|list>` | ANAC CKAN open data | nothing | Below-EU-threshold Italian procurement datasets |
| `apify_run.sh <owner~actor> [input.json]` | Apify REST | `APIFY_TOKEN` | Any store actor: reviews (Capterra/Trustpilot/G2), job posts (LinkedIn/Indeed), LinkedIn group posts (cookieless actors only), Facebook public groups |
| `exa_search.sh "<query>" [n]` (`EXA_MODE=answer` for cited answers) | Exa API | `EXA_API_KEY` | Semantic search / claim checking when no harness search tool is available |
| Openapi.com `GET /impresa` (no script yet — call with curl) | Registro Imprese via Openapi.com | `OPENAPI_TOKEN` | Company counts/lists by ATECO × province × size; **count-only queries are free via the `dry_run` parameter (100/day, then €0.01/call; verified 2026-08)** — use it for ICP counts before pulling any list; list/profile calls from €0.001/request, up to 1,000 companies per request; free sandbox at `test.visurecamerali.openapi.it` |
| `dataforseo_volume.sh "kw1,kw2,..." [loc=2380] [lang=it]` | DataForSEO Google Ads API (Basic auth) | `DATAFORSEO_LOGIN`/`_PASSWORD` | Italian keyword volumes + CPC + competition, up to 1,000 kw per ~$0.09 live task (verified 2026-08); without credentials treat Italian search volume as unmeasured and say so |
| `dataforseo_serp.sh "<query>" [depth=10] [loc=2380] [lang=it]` | DataForSEO SERP API live advanced | `DATAFORSEO_LOGIN`/`_PASSWORD` | google.it SERP observation (~$0.002/query, verified 2026-08): organic ranks, ads-present, People-Also-Ask, item-type mix (AI Overview visibility included) |

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

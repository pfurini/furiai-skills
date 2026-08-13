# Research Tooling Matrix — Idea Validation Skill (Italy, B2B)

All endpoint verification was performed with `curl` on **2026-08-13** from a single consumer network. All prices carry a source URL and the date observed. Where a price could not be confirmed against a live vendor page, the cell says so rather than guessing.

**Integration preference order** (as mandated): (1) direct API call from a dependency-free script shipped in the skill (`bash` + `curl` + `jq`, or `python3` stdlib; keys from env vars), (2) harness web tool described by capability, (3) manual step.

**Reading the "Verified?" column.** For a keyed API, a `401`/`402`/`403`/`422` from an unauthenticated or dummy-credential call is a *successful* verification: it proves the host, path, and auth scheme are live. Only a `200` with real payload is claimed as a full functional test.

---

## Job 1 — Broad web / semantic search and page fetch

| Option | Integration | Auth | Cost model | Verified? | Verdict |
|---|---|---|---|---|---|
| **Exa API** (`/search`, `/contents`, `/answer`) | API-script | `x-api-key: $EXA_API_KEY` header (`Authorization: Bearer` also accepted) | $7 / 1k search requests incl. 10 results with text+highlights; $1 / 1k results above 10; `/contents` $1 / 1k pages **per content type**; `/answer` $5 / 1k; deep $12 / 1k, deep-reasoning $15 / 1k. New accounts get $20 credit; free tier adds $10/mo | Yes — `POST /search` no key → 402; dummy key → `{"error":"Invalid API key","tag":"INVALID_API_KEY"}`; both header forms accepted | **Best** for semantic/discovery search. Priced per request, no subscription, and the authoring session already uses it |
| **pi-web-access `web_search`** | harness-tool | none (harness-managed) | No marginal cost to the skill | Not testable from here (different harness) | **Best** when running under pi. Zero key provisioning; multi-provider |
| **pi-web-access `fetch_content`** | harness-tool | none | — | Not testable from here | **Best** for page/PDF retrieval under pi (it converts PDFs) |
| **Tavily** | API-script | `Authorization: Bearer $TAVILY_API_KEY` | Credit-based. Free 1,000 credits/mo. PAYG $0.008/credit. Basic search = 1 credit, advanced = 2. Plans: $30/4k, $100/15k, $220/38k, $500/100k credits | Yes — no key → 401; dummy Bearer → `"Unauthorized: missing or invalid API key."` | **Fallback.** Generous free tier (1k/mo) makes it the best zero-cost option, but per-search cost above that ($8/1k) exceeds Exa |
| **Brave Search API** | API-script | `X-Subscription-Token: $BRAVE_API_KEY` header | $5 / 1k requests; $5 free credits every month. AI grounding tier $4 / 1k + $5 per 1M input tokens | Yes — no token → 422; dummy token → `SUBSCRIPTION_TOKEN_INVALID` | **Fallback.** Independent index, useful as a cross-check against Exa, but keyword-only (no semantic retrieval) |

Sources: <https://exa.ai/pricing> and <https://exa.ai/docs/reference/pricing> (page published 2026-07-28); <https://docs.tavily.com/documentation/api-credits> and <https://www.tavily.com/pricing>; <https://brave.com/search/api/> and <https://api-dashboard.search.brave.com/app/plans>. All observed 2026-08-13.

**Cost note that matters for skill design:** Exa bills every result past the tenth at $1/1k. A `numResults: 30` search costs $7 + $20 per 1k, roughly four times the headline rate. Scripts should default to `numResults: 10` and page only when needed.

---

## Job 2 — Italian official statistics (business counts, size classes)

| Option | Integration | Auth | Cost model | Verified? | Verdict |
|---|---|---|---|---|---|
| **Eurostat dissemination API** | API-script | none | Free, no key, no quota published | Yes — **200 with real data.** `sbs_sc_ovw?format=JSON&geo=IT&nace_r2=J62&indic_sbs=ENT_NR&time=2023` returned Italy NACE J62: 58,741 enterprises total; 54,580 with 0–9 employees; 2,077 with 10–19; 1,166 with 20–49; 768 with 50–249; 150 with 250+ | **Best.** This is the whole "imprese by size class" job, no key, stable JSON-stat |
| **ISTAT SDMX (SEP)** | API-script | none documented | Free | **Verified unreachable, 2026-08-13.** Every path returned 302 to `avvisicoeweb.istat.it` (a stale Coeweb maintenance notice dated November 2024): `/SDMXWS/rest/dataflow/IT1`, `/dataflow/IT1/all/latest`, `/dataflow/IT1/115_333/1.0`, `?format=jsonstructure`, with and without `-k`, with and without a browser User-Agent. Legacy `sdmx.istat.it` 302s to itself; `dati.istat.it` 302s to `avvisi.istat.it/IdotStat/`. DNS for `esploradati.istat.it` resolves to `01a-filtro.istat.it` (a filter/WAF host) | **Fallback only.** Documented endpoint is `https://esploradati.istat.it/SDMXWS/rest`, but it does not serve from this network today |

Sources: Eurostat API tested directly. ISTAT endpoint documented at <https://www.istat.it/en/classifications-and-tools/sdmx-web-services/> and <https://ondata.github.io/guida-api-istat/> (observed 2026-08-13).

**Eurostat dimension reference** (discovered by querying the dataset, not from memory):
`sbs_sc_ovw` dimensions are `freq, indic_sbs, nace_r2, size_emp, geo, time`.
`size_emp` values: `TOTAL, 0_1, 0-9, 2-9, 10-19, 20-49, 50-249, GE250`.
`indic_sbs` includes `ENT_NR` (enterprise count), `EMP_NR` (persons employed), `SAL_NR`, `AV_MEUR` (value added).
Also verified live: `bd_9bd_sz_cl_r2` and `bd_l_form` (business demography) both return 200 for `geo=IT`. `bd_size_class` is a **404** — that dataset code does not exist.

**Two ISTAT bugs worth carrying into the skill** (documented by ondata and confirmed by the ISTAT Contact Centre, per <https://ondata.github.io/guida-api-istat/processing/note-endpoint-esploradati.html>), because they will bite whoever gets the endpoint working:
1. `/rest/v2/data` is published in ISTAT's own OpenAPI spec but **is not implemented** — it returns rows with empty `OBS_VALUE`.
2. `endPeriod` is off by one. To get year *N* you must pass `endPeriod=N-1`. ISTAT calls this a temporary workaround for a confirmed anomaly.

**Gap:** I could not enumerate ASIA (business register) dataflow IDs, because the dataflow listing is exactly what the WAF blocks. Any specific ASIA dataflow ID in this report would be fabrication, so none is given.

**If anyone later re-enables the ISTAT path, it needs body validation, not a status check.** Following the redirect with `curl -L` yields **HTTP 200** — from the maintenance page, not from ISTAT's API. That is what made my first probe look successful. An ISTAT script must assert that the response actually parses as SDMX (or that the content type is an SDMX media type) before treating it as data. This is the same failure mode as the ANAC WAF in Job 6, and it defeats status-code checks in both places.

---

## Job 3 — Company registry lookups (Italy)

| Option | Integration | Auth | Cost model | Verified? | Verdict |
|---|---|---|---|---|---|
| **Openapi.com — `GET /impresa` company search** | API-script | `bearerAuth` (OAuth token from console) | **€0.001 per request, 1,440 free requests/day.** Billed per *request*, not per result, and one request returns up to 1,000 companies. Filters: `denominazione`, `provincia`, `codice_ateco`, `fatturato_min/max`, `dipendenti_min/max`, `lat/lng/radius`, `skip`, `limit` (1–1,000). Rate limit 10,000 req/min | Yes — `visurecamerali.openapi.it/impresa?...` unauthenticated → 403 (host + path live, keyed). Pricing table re-fetched to confirm the per-request reading (see note below) | **Best** for ICP sizing and market segmentation. Effectively free at skill volumes, and the ATECO + province + employee-band + revenue-band filters are exactly the B2B ICP cut |
| **Openapi.com — Imprese data endpoints** | API-script | Bearer token | Per request: `/base` €0.100 (best €0.020), `/advance` €0.200 (best €0.060), `/pec` €0.060 (best €0.030), `/soci` €0.060, `/autocomplete` €0.002, `/gruppoiva` €0.040, `/closed` €0.040 | Yes — `imprese.openapi.it/advance` → 403 | **Best** for enriching a named shortlist. Note the Imprese API page states it is superseded by the newer "Company" product |
| **Openapi.com — Visure Camerali (official documents)** | API-script | Bearer token | Per document: ordinaria società di capitale €4.90 (best €3.96), storica €5.90 (best €4.95), ordinaria impresa individuale €2.90, bilancio ottico €4.50 (best €2.95), certificato iscrizione €13.70 | Not called (paid, document-generating POST) | **Avoid for validation work.** Per-document pricing suits due diligence, not market research |
| **OpenCorporates** | API-script | API token | £2,250/yr (500 calls/mo, 200/day); £6,600/yr (2,500/mo); £12,000/yr (5,000/mo); Enterprise on request. Default unpaid limit 200 req/month, 50/day. Free for genuinely open-data projects under share-alike | Yes — `v0.4/companies/search?jurisdiction_code=it` → 401 | **Avoid** for Italy. ~£200–375 per 1,000 calls versus €1 per 1,000 for Openapi's `/impresa`, and its Italian records are registry-shallow (no ATECO/revenue/employee filtering) |
| **Atoka** (Cerved group) | API-script *if* a token is granted | `token` query param | Credit-based; 1 credit per company returned with any data package. **No public price list**; token issued only via `sales@atoka.io` | Not callable — no self-serve signup | **Avoid** for a shipped skill. Data quality is high (22M Italian companies, Cerved official data) but there is no self-serve path, so a skill cannot assume access |
| **Cerved / CRIBIS** | manual | — | **No public self-serve pricing.** Both are quote-and-demo motions | Sales-led confirmed from vendor pages | **Avoid.** Sales-led only |
| **Registro Imprese / InfoCamere Telemaco** | manual | paid account login | Per-document fees behind a login | — | **Avoid.** Not a self-serve REST API; no developer API product surfaced in this research |

Sources: <https://console.openapi.com/apis/imprese/pricing>, <https://console.openapi.com/apis/visure-camerali/pricing>, <https://console.openapi.com/apis/visure-camerali/documentation>, <https://openapi.com/products/italian-capital-company-registration-report>; <https://opencorporates.com/pricing/> and <https://api.opencorporates.com/documentation/API-Reference>; <https://developers.atoka.io/v2/> and <https://atoka.io/pages/en/atoka-sales-api/>; <https://www.cribis.com/en/solutions-for/sales-lead-acquisition/>. All observed 2026-08-13.

**This is the single most valuable finding in the matrix.** Openapi.com's `/impresa` search answers "how many Italian companies match my ICP" — by ATECO sector, province, employee band, and revenue band — for a thousandth of a euro per call, with 1,440 free calls a day. Nothing else in this list does that job at that price.

**Because that claim is load-bearing, I re-fetched the source to rule out a misreading.** The pricing page groups endpoints into "Endpoints of non-free services" (the POST document-generating calls, €2.30–€13.70 each) and "Free service endpoints" (€0.001, 1,440/day). Most rows in the free block are described as "List of your requests" — status-polling calls. `GET /impresa` sits in that same free block but is described as **"Business search"**, not "List of your requests", and the API reference documents it as *"With this service we can draw up a list of companies that correspond to certain parameters... The call returns a maximum of 1000 results even if you set a higher limit"*, returning `data: Array of objects (Imprese)`. The pricing column header reads **"Base Price €/request"**. So the filtered multi-result search is the €0.001 endpoint, and the unit is the request, not the returned company. Source: <https://console.openapi.com/apis/visure-camerali/pricing> and <https://console.openapi.com/apis/visure-camerali/documentation>, re-fetched 2026-08-13.

Openapi also exposes a **free sandbox** at `test.visurecamerali.openapi.it` mirroring all 21 production scopes, so the skill's script can be developed and tested without spending anything or holding a production token.

---

## Job 4 — Reviews and software directories

Integration for every row here is the same: **Apify REST, called from a dependency-free script.**

| Option | Actor ID | Cost model | Verified? | Verdict |
|---|---|---|---|---|
| **Capterra reviews** | `zen-studio/capterra-reviews-scraper` | $1.99 / 1k reviews (no-discount plan); $1.49 Bronze, $1.39 Silver, $1.29 Gold. Pay-per-event, only successful reviews billed | Actor metadata endpoint 200 | **Best** for Capterra. Cheapest maintained Capterra actor found; returns 5 sub-ratings, reviewer job title and company size |
| **G2 reviews** | `zen-studio/g2-reviews-scraper` | $6.49 / 1k (Basic); $5.49 Bronze, $4.49 Silver, $3.49 Gold | Actor page current (changelog entries dated July 2026) | **Best** for G2 alone, though pricey per review |
| **Multi-platform in one run** | `zen-studio/software-review-scraper` | from $3.99 / 1k (Gold) to $4.99 / 1k (Free). Covers G2, Capterra, TrustRadius, Gartner, Trustpilot; accepts a product *name* or domain, no URL needed | Actor page published 2026-03-07 | **Best overall** for the skill. Takes a plain product name and normalises five directories into one dataset, which removes per-platform URL discovery from the script |
| **G2 + Capterra by URL** | `samstorm/g2-capterra-review-scraper` | $0.002 per review ($2 / 1k) **plus** Apify platform usage (uses residential proxies) | Actor page published 2026-03-21 | **Fallback.** Headline rate is low but platform usage stacks on top, unlike the pay-per-event actors |
| **Trustpilot** | `scrapeai/trustpilot-scraper` | from $4.99 / 1k results | Actor page published 2026-04-10 | **Fallback.** Use only if Trustpilot specifically matters; the all-in-one actor covers it as an opt-in |
| **Google Maps reviews** | `x_guru/google-maps-reviews-scraper` | $0.50 / 1k reviews (Free plan), $0.20 / 1k (paid plans); actor start $0.00001–0.00005 | Actor page published 2026-06-01 | **Best** for local/services businesses. Cheapest per-review price in the whole matrix, and it supports a `maxCost` budget cap that reduces the target before scraping |
| **Google Maps reviews (alt)** | `solidcode/google-maps-reviews-scraper` | **Contradictory:** actor title and store listing say $0.25 / 1k results, the README body says $3.00 / 1k. Not resolved | Contradiction observed on the actor page itself | **Avoid** until the price is confirmed in the Apify console. A 12x ambiguity is not safe to script against |

**Apify REST integration (the dependency-free pattern), verified:**
- `POST https://api.apify.com/v2/acts/{owner}~{actor}/run-sync-get-dataset-items?token=$APIFY_TOKEN` with the run input as the JSON body → runs the actor and returns dataset items in one call. Unauthenticated → **402**, confirming the path.
- `GET https://api.apify.com/v2/acts/{owner}~{actor}` → **200 with no auth at all.** Useful for reading an actor's current input schema before calling it.
- `GET https://api.apify.com/v2/acts` → 401, confirming token auth.

**Apify platform pricing** (stacks *on top of* per-event actor fees): Free $0/mo with $5 prepaid usage; Starter $29; Scale $199; Business $999. Compute $0.20/CU (Free/Starter) down to $0.13/CU (Business); residential proxy $8/GB down to $7/GB. Unused prepaid usage expires monthly and does not roll over. Source: <https://apify.com/pricing>, observed 2026-08-13.

**Italian-market caveat.** G2 and Capterra coverage skews heavily American. For an Italian B2B software category, review volume on these directories is often too thin to support a conclusion, while Google Maps reviews are dense for Italian service businesses. Weight the Google Maps path higher for Italy-specific validation, and treat a low G2/Capterra review count as missing data rather than as evidence of a small market.

---

## Job 5 — Job posts as demand signal

| Option | Integration | Cost model | Verified? | Verdict |
|---|---|---|---|---|
| `mfrostbutter/linkedin-jobs-scraper` | Apify API-script | **$0.50 / 1k jobs** + $0.00005 actor start. No login/cookies required | Actor page published 2026-04-20 | **Best** for LinkedIn. Cheapest maintained option and it needs no LinkedIn session |
| `creon/linkedin-job-scraper` | Apify API-script | from $0.70 / 1k results. Optional OpenAI salary estimation (needs your own OpenAI key) | Actor page published 2026-01-07 | **Fallback** |
| `curious_coder/linkedin-jobs-scraper` | Apify API-script | $1.00 / 1k results | Actor page carries an **August 2026** update note | **Fallback**, but read its warning first (below) |
| `valig/indeed-jobs-scraper` | Apify API-script | from $0.07 / 1k results | Publication date not shown on the page | **Fallback.** Cheapest listed, but no visible maintenance date — verify it still returns rows before relying on it |
| `crawlerbros/indeed-jobs-scraper` | Apify API-script | from $1.00 / 1k results (pay-per-event **and** platform usage) | Actor page published 2026-03-13; **`IT` is in its supported-country enum** | **Best** for Indeed Italy. Explicit Italian domain support and a current maintenance date |
| Official LinkedIn / Indeed job APIs | — | — | **Not found in this research.** No public self-serve job-search API surfaced for either | **Does not exist** for this purpose (see the closing section) |

**A live platform change the skill must handle.** The `curious_coder` actor page states that since **August 2026** LinkedIn rolled out an AI-powered job search that supports only four URL filters: date posted (`f_TPR`), company (`f_C`), easy apply (`f_AL`), and under-10-applicants (`f_EA`). Experience level, job type, and the other classic filters are no longer separately addressable and must be expressed in the query text. This is days old relative to this report, it affects every LinkedIn jobs actor rather than just that one, and it means any skill prompt that assumes structured LinkedIn filters needs rewriting. Source: <https://apify.com/curious_coder/linkedin-jobs-scraper>, observed 2026-08-13.

---

## Job 6 — Public tenders

| Option | Integration | Auth | Cost model | Verified? | Verdict |
|---|---|---|---|---|---|
| **TED Europa Search API v3** | API-script | **none** | Free | Yes — **200 with real data.** `POST https://api.ted.europa.eu/v3/notices/search` returned 157 Italian CPV-72 notices published in the last 30 days, e.g. `485581-2026` (2026-07-14), `488534-2026` (2026-07-15) | **Best.** No key, no cost, real structured EU tender data with a working Italian filter |
| **ANAC open data (CKAN)** | API-script | none, **but a browser User-Agent is required** | Free | Yes — `GET /opendata/api/3/action/package_list` returned the dataset list; `package_show?id=bandi-cig-tipo-scelta-contraente` returned resources in CSV, JSON, and TTL | **Best** for below-EU-threshold Italian procurement, which is where most SME-relevant contracts live |

**TED v3 query grammar, established by testing rather than assumed:**
- The endpoint is **POST only** — a `GET` returns **405**.
- `fields` is mandatory and must be non-empty; omitting it returns `400 {"field":"fields","message":"must not be empty"}`.
- CPV codes must be **full 8-digit**. `classification-cpv=72` was rejected with `QUERY_UNSUPPORTED_FIELD_VALUE`; `classification-cpv IN (72000000)` works.
- A working Italian query:
  ```json
  {"query":"classification-cpv IN (72000000) AND buyer-country IN (ITA) AND publication-date >= today(-30)",
   "fields":["publication-number","notice-title","buyer-name","publication-date"],
   "limit":3}
  ```

**ANAC WAF behaviour, which will silently break a naive script.** `https://dati.anticorruzione.it/opendata/api/3/action/package_list` with curl's default User-Agent returns an F5 block page (`<title>Request Rejected</title>`) **with HTTP 200**, so a status-code check passes while the body is garbage. The identical request with a browser User-Agent returns valid CKAN JSON. Any ANAC script must set a User-Agent header *and* validate that the parsed body contains `"success": true` rather than trusting the status code.

Dataset resources download from `https://dati.anticorruzione.it/opendata/download/dataset/{dataset-id}/files` in CSV, JSON, or TTL.

---

## Job 7 — Keyword and SEO demand data for Italian queries

| Option | Integration | Auth | Cost model | Verified? | Verdict |
|---|---|---|---|---|---|
| **DataForSEO** | API-script | **HTTP Basic** (`-u login:password`) | Pay-as-you-go, **$50 minimum deposit**, $1 free trial credit. Google Organic SERP: $0.0006 per SERP (standard queue), $0.0012 (priority), $0.002 (live). Google Ads keyword data: $0.06 per task of up to 1,000 keywords | Yes — no auth → 401; dummy Basic auth → `status_code 40100, "You are not authorized..."`, with a live API version string `0.1.20260806` | **Best** paid keyword source for a dependency-free script. Basic auth is trivial in curl, and per-request pricing is roughly a thousandth of the subscription tools |
| **SEOZoom** | API-script | API key from the platform dashboard | **API access requires the Evolution plan or higher: €99 + VAT/month** (€910/year). 6,500 free credit units/day per user, then pay-as-you-go top-ups | Partial — `apiv2.seozoom.it` resolves via Cloudflare, but my probe returned no response (000). Endpoint path not confirmed | **Fallback.** Best Italian-market keyword database, but the €99/mo floor is hard to justify for a skill, and I could not confirm the API host responds |
| **Semrush** | API-script | API key | Requires the **Advanced plan — $549/mo monthly, or $455.67/mo billed annually** — which is the lowest tier listing "API data integration". API units must then be **purchased separately** on top. One line of a Domain Organic Keywords report costs 10 units live, 50 historical | Yes — `api.semrush.com` unauthenticated → 403; plan tier and price confirmed by fetching the pricing page | **Avoid.** Subscription floor plus a second unit purchase, for data DataForSEO sells per request |
| **Ahrefs** | API-script | API key | API v3 requires **Lite ($129/mo) or higher**. Minimum 50 units per request; 100k units/mo on Lite up to 2M on Enterprise; max rows per request 100 (Lite) to unlimited (Enterprise) | Partial — my probe path returned 404, so the endpoint shape is **not** confirmed | **Avoid.** Same objection as Semrush, and I did not establish a working path |

Sources: <https://dataforseo.com/apis/serp-api/pricing> and <https://dataforseo.com/pricing/google-serp/google-organic-serp-api>; <https://www.seozoom.com/buy-a-plan/> (published 2026-03-10) and <https://www.seozoom.com/seozoom-api-guide/>; <https://developer.semrush.com/api/get-started/api-access/> (last updated 2026-08-05) and <https://www.semrush.com/pricing/seo-ai-search/>; <https://help.ahrefs.com/en/articles/6559232-about-api-v3> and <https://ahrefs.com/pricing>. All observed 2026-08-13.

**Two pricing caveats I will not paper over.**
1. DataForSEO applied a pricing increase on **2026-07-01**, roughly +20% across eight APIs: Backlinks, Business Data, Content Analysis, DataForSEO Labs, Domain Analytics, **Keywords Data**, On-Page, and Merchant. **SERP API is not on that list**, so the $0.0006/SERP figure should still hold. The **Google Ads keyword task price of $0.06 is on an API that did get the +20%**, and the pricing page I read does not carry a post-July revision date — treat $0.06 as a floor and confirm in the dashboard before budgeting. Source: <https://dataforseo.com/update/pricing-update-in-dataforseo-apis> (published 2026-07-01).
2. The SEOZoom API guide page I used for the 6,500-units/day figure is dated **2024-01-05**, over 18 months old. Per the sourcing rule, treat that number as possibly outdated; the €99/mo plan requirement comes from the current pricing page (2026-03-10) and is the more reliable figure.

**Semrush plan-name drift.** Semrush's developer docs say API access requires a "**SEO Business**" subscription, but the current pricing page has no Business tier — its ladder is SEO / Starter / Pro+ / **Advanced**, and Advanced is the one whose feature list includes "API data integration". The docs and the pricing page are out of step on naming; Advanced is the tier to buy. Sources: <https://developer.semrush.com/api/get-started/api-access/> (last updated 2026-08-05) and <https://www.semrush.com/pricing/seo-ai-search/>, both observed 2026-08-13.

---

## Job 8 — Claim verification

| Option | Integration | Auth | Cost model | Verified? | Verdict |
|---|---|---|---|---|---|
| **pi-web-access `source_check`** | harness-tool | none | No marginal cost | Not testable from here | **Best** under the primary harness. Purpose-built for this job and already present |
| **Exa `/answer`** | API-script | `x-api-key` | **$5 / 1k requests.** Returns an LLM answer with citations | Yes — unauthenticated → 401 | **Best** portable fallback. Cheaper than `/search` and returns citations directly, which is what claim-checking needs |
| **Exa `/search` + `/contents`** | API-script | `x-api-key` | $7 / 1k + $1 / 1k pages per content type | Yes (see Job 1) | **Fallback** when the claim needs primary-source text rather than a synthesised answer |

---

## (a) Script shortlist worth shipping in the skill

Ordered by value per unit of effort. Each is `bash` + `curl` + `jq` or `python3` stdlib, with keys read from environment variables.

| Script | Source | Inputs | Outputs | Key needed |
|---|---|---|---|---|
| `eurostat_enterprises.sh` | Eurostat dissemination API | NACE code, size classes, year, `geo` (default `IT`) | Enterprise counts and employment by size class, as CSV/JSON | **None** |
| `ted_tenders.sh` | TED Search API v3 | 8-digit CPV list, buyer country, lookback days | Matching notices with title, buyer, date, links | **None** |
| `anac_dataset.sh` | ANAC CKAN | dataset id | Dataset resource list plus CSV/JSON download URL | **None** (must set a browser User-Agent and assert `success: true`) |
| `openapi_impresa_count.sh` | Openapi.com `/impresa` | ATECO code, province, employee band, revenue band | ICP company count and a sample list | `OPENAPI_TOKEN` (develop against the free sandbox `test.visurecamerali.openapi.it` first) |
| `apify_run.sh` | Apify REST | actor id, JSON run input | Dataset items via `run-sync-get-dataset-items` | `APIFY_TOKEN` |
| `exa_search.sh` | Exa `/search` (+`/answer`) | query, `numResults` (default 10) | Results with text and highlights, or a cited answer | `EXA_API_KEY` |
| `dataforseo_serp.sh` | DataForSEO SERP API | keyword, `location_code` for Italy, language | SERP results / keyword volume | `DATAFORSEO_LOGIN`, `DATAFORSEO_PASSWORD` |

`apify_run.sh` is deliberately one generic script rather than several: a single actor-run-plus-dataset-fetch wrapper covers every reviews actor (Job 4) and every jobs actor (Job 5), parameterised by actor id and input JSON.

## (b) Environment variables to provision

| Variable | Needed for | Can the skill run without it? |
|---|---|---|
| `EXA_API_KEY` | Web/semantic search, claim verification | Yes under pi (`web_search`, `source_check` substitute) |
| `APIFY_TOKEN` | Reviews (Job 4), job posts (Job 5) | No — those two jobs degrade to manual |
| `OPENAPI_TOKEN` | Italian company search and enrichment | No — ICP sizing degrades to Eurostat aggregates only |
| `DATAFORSEO_LOGIN` + `DATAFORSEO_PASSWORD` | Keyword/SERP demand data | Yes, at reduced confidence. Note the **$50 minimum deposit** |
| `TAVILY_API_KEY` | Optional search fallback | Yes — only if neither pi tools nor Exa are available |
| `BRAVE_API_KEY` | Optional independent-index cross-check | Yes |

Eurostat, TED, and ANAC need **no keys at all**, so the skill's quantitative spine works with zero provisioning.

## (c) Does not exist / not viable

- **ISTAT SDMX as a dependable source (today).** The documented endpoint is real and free, but it returned 302-to-maintenance-page on every one of seven request variants on 2026-08-13, and DNS points at a filter host. Eurostat covers the same question with data I actually retrieved. Ship Eurostat; leave ISTAT as a commented fallback.
- **Any official LinkedIn or Indeed job-search API.** No public self-serve product surfaced. LinkedIn's job data sits behind partner Talent Solutions agreements. Apify actors are the only viable route, which makes job-post analysis structurally dependent on scraping and therefore fragile — see the August 2026 LinkedIn filter change above.
- **Self-serve access to Cerved, CRIBIS, or Atoka.** All three are sales-led. Atoka publishes full API documentation but issues tokens only through `sales@atoka.io`, with no public price list. A shipped skill cannot assume any of them.
- **Registro Imprese / InfoCamere Telemaco as an API.** A paid document portal, not a developer API. Openapi.com is the practical intermediary.
- **OpenCorporates for Italian market sizing.** It functions, but at roughly £200–375 per 1,000 calls against €1 per 1,000 for Openapi's `/impresa`, and without the ATECO, revenue, or employee filters the ICP work needs.
- **`solidcode/google-maps-reviews-scraper` pricing.** The actor's own page states $0.25/1k in its title and $3.00/1k in its README. Unresolved, so no price is claimed here.
- **Ahrefs API endpoint shape.** My probe returned 404; I did not establish a working path. The plan requirements above are from Ahrefs' own help pages, but the endpoint itself is unverified.
- **SEOZoom API endpoint.** Host resolves, probe returned no response. Endpoint path unconfirmed.

## Appendix — full verification log (curl, 2026-08-13)

| Target | Call | Result |
|---|---|---|
| Eurostat | `data/sbs_sc_ovw?format=JSON&geo=IT` | 200, 614 KB JSON-stat |
| Eurostat | `...&nace_r2=J62&indic_sbs=ENT_NR&time=2023` | 200, 3.3 KB, real values |
| Eurostat | `bd_9bd_sz_cl_r2`, `bd_l_form` | 200 both; `bd_size_class` 404 |
| ISTAT SDMX | 7 variants across `esploradati` + `sdmx` hosts | 302 → `avvisicoeweb.istat.it` every time |
| ISTAT I.Stat | `dati.istat.it` | 302 → `avvisi.istat.it/IdotStat/` |
| TED v3 | `POST /v3/notices/search` (valid body) | 200, 32 KB, 157 IT CPV-72 notices in 30 days |
| TED v3 | `GET` same path | 405 |
| TED v3 | empty `fields` | 400 validation error |
| TED v3 | `classification-cpv=72` | `QUERY_UNSUPPORTED_FIELD_VALUE` |
| ANAC | `package_list`, default UA | 200 **with an F5 block-page body** |
| ANAC | `package_list`, browser UA | 200, valid CKAN JSON |
| ANAC | `package_show?id=bandi-cig-tipo-scelta-contraente` | 200; CSV, JSON, TTL resources |
| Openapi.com | `visurecamerali.openapi.it/impresa`, `company.openapi.com`, `imprese.openapi.it/advance` | 403 each |
| OpenCorporates | `v0.4/companies/search?jurisdiction_code=it` | 401 |
| Apify | `GET /v2/acts` | 401 |
| Apify | `POST /v2/acts/{a}/run-sync-get-dataset-items` | 402 |
| Apify | `GET /v2/acts/{actor}` | **200, no auth** |
| Exa | `POST /search` no key / dummy key | 402 / `INVALID_API_KEY` (both `x-api-key` and Bearer accepted) |
| Exa | `POST /answer` | 401 |
| Tavily | `POST /search` no key / dummy Bearer | 401 / `"Unauthorized: missing or invalid API key."` |
| Brave | `/res/v1/web/search` no token / dummy token | 422 / `SUBSCRIPTION_TOKEN_INVALID` |
| DataForSEO | no auth / dummy Basic | 401 / `40100`, API version `0.1.20260806` |
| Semrush | `api.semrush.com/` | 403 |
| Ahrefs | `/v3/site-explorer/overview` | 404 (path unconfirmed) |
| SEOZoom | `apiv2.seozoom.it/keyword` | 000 (no response) |

---

## Addendum (orchestrator follow-up, 2026-08-13) — LinkedIn groups & private Facebook groups

Follow-up verification after the main report, prompted by the question "is there a
third-party API for the surfaces marked unreadable?". Observed on Apify store 2026-08-13.

| Surface | Option | Auth | Cost | Verdict |
|---|---|---|---|---|
| LinkedIn group discovery, profiles+admins, **posts** | `unseenuser/linkedin-groups-scraper` (HarvestAPI-backed, pub. 2026-05) | **None** (no cookies) | ~$0.005/group, ~$0.002/post, pay-per-result | **Best** — upgrades LinkedIn groups from "existence signal" to minable for pain-themes |
| LinkedIn group member rosters | — | — | — | **Impossible by design**: LinkedIn exposes no roster to anyone (not even group admins); only admins + active posters (~top 5–15% engaged) are reachable. Never claim otherwise in packs |
| LinkedIn group search w/ member counts | `memo23/linkedin-search-groups-scraper` | `li_at` + `JSESSIONID` cookies | $0.8/1k | **Avoid** — session cookies = account-ban risk; the cookieless actor covers discovery |
| Facebook public groups | `apify/facebook-groups-scraper` (first-party) | None | ~$2.60–5.00/1k posts | **Best** for public groups; public-only by design (ToS-clean) |
| Facebook private/closed groups | `scraper-engine`, `easyapi`, `mo_khairy` group actors | Session cookies (`c_user`+`xs`) of a **member** account | ~$3–5/1k posts (+ rental for some) | **Opt-in only, off by default**: against Meta ToS (actors advise burner accounts); GDPR exposure higher than public data. If used: own membership, pain-themes only, no contact extraction, provenance-flagged |
| Facebook Graph API for groups | Meta official | OAuth app | — | **Not viable** — only reaches groups the app itself administers |

Open verification item for forward-tests: whether Italian professional LinkedIn groups
(commercialisti, avvocati) carry real post volume — the pipe exists, the signal is unproven.

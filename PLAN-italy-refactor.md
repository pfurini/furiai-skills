# Plan — Italy-first refactor of idea-validation

Date: 2026-08-13. Scope: `skills/idea-validation/`. B2B first, B2C after B2B is finalized.

**Status (2026-08-13):** decisions D1–D6 and all four open decisions accepted by the user
(evidence gate = hard cap at moderate, threshold ~15 pending forward-tests; three-band
guardrail; `incumbents` prompt replaces X/Twitter in the default B2B menu; Phase A runs in
this session, gated PDFs pulled manually by the user).

**Phase A complete (2026-08-13):** five reports in `research/idea-validation-italy-b2b/`
(see its README for the synthesis). Corrections Phase A imposes on this plan:
- `cold_outbound` is not a calibrated channel in Italy — it becomes a hard prohibition
  entry (art. 130, Garante enforcement) with the compliant phone-consent bridge noted.
- The guardrail's self-serve ceiling gets a number: ~€50/month ex-VAT.
- Market-sizing must support buyer redirection (micro firm → studio/consulente as the
  actual buyer for accounting/payroll/tax categories) and must forbid quoting the 4.27M
  micro-firm count as TAM (no adoption data exists below 3 addetti).
- Distribution adds a ranked incumbent-surface table; Fatture in Cloud App Store is a
  named first-class channel.
- Trend prompts must only name surfaces verified active in `communities-signal-surface.md`
  (InfoJobs and Forum GT are dead; no open forum exists for avvocati).
- Tooling: Eurostat (not ISTAT SDMX) ships as the stats source; scripts shortlist and
  env-var list are in `tooling-matrix.md`.

## Requirements (from the user)

- **B2B target**: Italian companies, primarily micro (<10 employees) and small (<50) — the
  PMI segment. Medium (50–249) may be included as an opt-in edge with a caveat; large
  companies are out of scope. Includes professional firms that are not ordinary companies:
  studi commercialisti (1–10 people), avvocati associati, and similar regulated professions.
- **B2C target**: Italian-speaking users first, with international breadth kept, prioritized
  as rings: Italy → Europe (apps in English, no other localizations) → Western markets
  (North America, UK/IE, AU/NZ). Eastern markets excluded.
- Research evidence from the parallel session (2026-08-13) is trusted as fact; its process
  suggestions are input, not decisions.

## Architecture decision: no new target axis

Considered three options:

1. **New target values** (`b2b-it`) — rejected: multiplies packs and violates the
   "schemas identical, only pack contents differ" rule for no benefit.
2. **A `market:` frontmatter field with geo overlay packs** (`calibration/b2b/it/`) —
   rejected for B2B: the B2B target *is* Italy, so an overlay would be the only overlay
   ever loaded, and every dispatch would carry two calibration paths per agent.
3. **Fold geography into the existing per-target packs** — chosen. The B2B packs are
   rewritten Italy-first; global benchmarks stay only where they are the only data that
   exists (churn-by-ARPA, conversion-by-entry-model — these are price-band constructs, not
   geography constructs) and are labeled as global. For B2C (phase 2), geography is a
   prioritization policy inside the existing packs/prompts (ring labels), not new files.

One addition to `idea.md` frontmatter: `segment_size: micro | small | medium` for B2B ideas
(absent → micro/small). Medium triggers the sales-led caveat check (below). This is
frontmatter, not artifact schema, so the schema-parity rule holds.

## What the Italy constraint actually changes (findings from the file survey)

Reading all B2B packs and prompts against the Italy research, the geography-sensitive
surface is:

| Area | Problem with current content | Direction |
|---|---|---|
| Trend prompts (all 3) | Source stacks are US/EN: r/agency, HN, Indie Hackers, G2 grids, EN LinkedIn. Italian micro-firms and professionals barely appear there | Italy-first source tiers; G2/EN demoted to secondary; bilingual search |
| `competitor-sources.md` | Search order starts at G2/Capterra; saturation anchors keyed to review volumes that Italian verticals never reach (a dominant Italian incumbent can have <50 G2 reviews) | Add the incumbent-suite layer (TeamSystem, Zucchetti, Wolters Kluwer, Buffetti, Namirial, Danea…) as tier 1 for vertical ideas; Capterra.it; thin-review recalibration |
| `market-sizing.md` | Business counts are US Census/SBA/ADA | ISTAT ASIA + ATECO, InfoCamere/Movimprese, ordini counts (CNDCEC ~69K studi; Cassa Forense: ~9.8% of lawyers in associated firms) |
| `pricing.md` | $ anchors, Shopify store average, US WTP bands | EUR; Italian incumbent price anchors; ex-VAT display and invoice/SDD billing norms; annual-with-fattura preference |
| `cac.md` | US CPC/CPL units; cold outbound assumed legal-neutral | Italy CPC units; GDPR/Garante constraints on cold email and PEC outreach; channel set gains intermediary/association routes |
| `distribution.md` | Loop taxonomy fine; channel rubrics assume EN communities, marketplaces, newsletters | Italian advocacy surface: ordini events/CPD, category associations, vertical fairs, incumbent marketplaces; commercialista-as-channel |
| `demand-drivers.md` | Construct is sound; budget-authority threshold in $ | EUR thresholds; Italian buying-culture notes (subscription resistance, trusted-intermediary purchases) |
| `retention.md` | ChartMogul tables are global price-band data — keep | Keep; add Italian billing-cycle note (annual prepay via invoice is common → churn shows up at renewal, not monthly) |
| `scoring-rubrics.md` | $ thresholds ($50/mo, $25 ARPA line) | EUR equivalents; evidence-sufficiency adjustment (below) |
| `SKILL.md` | B2B trend menu names EN platforms; no geo statement | Italy-first framing in the target section; new B2B menu; bilingual NICHE dispatch rule |
| `memory.md` | Trend-file platform enum | New/renamed B2B platform slugs |

Two process gaps (not just data):

1. **Evidence scarcity is structural, not incidental.** Italian micro-firm segments have low
   public-review participation; the strongest evidence is local, fragmented, and often
   offline. The parallel research's conclusion — "15 well-segmented interviews beat 5,000
   scraped reviews" — means desk research alone systematically under-observes this market.
   The framework must *measure its own evidence coverage* instead of silently scoring on
   thin signals.
2. **Self-serve purity is rarer in Italy.** Micro-firms buy through commercialisti,
   consulenti, resellers, and incumbents' agent networks. The current guardrail is binary
   (self-serve vs sales-led). Italy needs a middle notion: self-serve product with
   assisted onboarding / intermediary referral, which is still indie-viable.

## Design decisions (proposed, to review)

### D1. Evidence-hierarchy contract in every B2B trend prompt

Adopt the parallel research's labeling scheme as a required block per finding: Italy region
(national/North/Centre/South/province), professional segment, firm-size proxy, current
stack named, regulatory dependency (SDI, PCT, PEC, AML, GDPR, conservazione), switching
constraint, evidence type, confidence (high only if multi-source Italian or
interview-confirmed). Plus a mandatory "disconfirming evidence" section. This is narrative
markdown, so no schema change.

### D2. New B2B trend platform menu (5 slots, Italy-first)

1. **Incumbent ecosystems** (`incumbents`) — NEW prompt: TeamSystem / Zucchetti / Wolters
   Kluwer / Buffetti / Danea / Namirial etc.: release notes, knowledge bases, support
   forums, migration guides, pricing pages, integration gaps. For vertical ideas this is
   the real category map.
2. **Italian operator communities** (`communities`) — rewritten: Facebook/LinkedIn groups,
   Telegram/WhatsApp where lawfully public, vertical forums (e.g. FiscoeTasse-class
   portals), ordini and association publications, YouTube webinar comments; HN/Indie
   Hackers/Reddit kept only for dev-tool niches.
3. **Professional web & jobs Italy** (`linkedin`) — rewritten: LinkedIn IT posts, Indeed/
   LinkedIn job posts naming manual workflows, trade press (Il Sole 24 Ore, ItaliaOggi,
   vertical outlets), CNDCEC/Cassa Forense/association research, ANAC/TED tenders as
   market-language signal.
4. **Review platforms & marketplaces** (`g2-capterra`) — kept but demoted in framing:
   Capterra.it first, G2/EN as directional/secondary; incumbent marketplaces where they
   exist. Explicit warning: EN review volume ≠ Italian adoption.
5. **Web search** (`web-search`) — reused with an Italy addendum: google.it, Italian-language
   queries primary (buyer vocabulary is Italian: "fatturazione elettronica", "gestionale
   studio"), English secondary.

Menu slugs change in `memory.md` (`incumbents` added). X/Twitter drops out of the default
B2B menu (thin Italian professional signal) but remains requestable.

### D3. Bilingual research rule

Dispatches carry NICHE in both languages: `NICHE: <Italian wording> / <English wording>`.
Searches run Italian-first. Artifacts stay in English (durable files), with Italian quotes
preserved verbatim + translated. Trend prompts state this explicitly.

### D4. Evidence-sufficiency gate (new, small, high-leverage)

Scoring gains a coverage check: count Italian-source observations across market_insights
(per D1 labels). Below a threshold (e.g. <15 Italian-source observations across platforms),
every dimension score is capped at the "moderate" band and the memo must say the verdict is
desk-limited and prescribe the interview step. The decision-memo template gains an
**interview kit** section (10 questions in Italian, recruiting routes via ordini/
associations/LinkedIn) that is mandatory whenever the gate fires or the verdict is
pursue/test for a professional-firm niche. This encodes "interview-heavy" without turning
the skill into an interview tool.

### D5. Guardrail recalibration (self-serve in the Italian market)

Three-band instead of two: self-serve · **self-serve + assisted onboarding/intermediary
referral (viable, flagged)** · sales-led (out of scope, current caveat behavior). Medium
companies (`segment_size: medium`) automatically trigger the sales-led check. The
commercialista/consulente/reseller channel is treated as distribution (a referral loop),
not as sales-led drift, when pricing stays self-serve.

### D6. Merge the source-hardening pass into this refactor

The pending hardening pass (HANDOFF open point 1) targeted the same `confidence: low`
tables this refactor rewrites (driver multipliers, capture bands, community multipliers,
category WTP, saturation thresholds). Hardening them twice — once US-centric, once
Italian — is wasted work. New order: run the Italy research pass (below), rewrite the packs
Italy-first, and harden what survives. The two gated PDFs (MicroConf, SaaS Capital) stay on
the list — their constructs (indie cohort revenue, NRR) are geography-neutral.

## Tooling policy (added after decision review)

The skill must not assume Claude Code. The primary harness is pi with the `pi-web-access`
extension (verified 2026-08-13 from its README): `web_search` (multi-provider, Exa works
zero-config, batch queries, `domainFilter`, `recencyFilter`), `fetch_content` (readable/
raw/answer modes; PDFs converted to markdown via Datalab → Gemini → local pdf.js),
`get_search_content`, `source_check` (claim verification with passage citations).

Ranking rule for every research job in the skill, best first:

1. **Direct API in a dependency-free script** kept in the skill's `scripts/` (bash + curl +
   jq, or python3 stdlib only; keys via env vars). Use when the source has a stable API:
   ISTAT SDMX, Eurostat, TED/ANAC open data, OpenCorporates, Apify (REST, credit-based),
   Exa API.
2. **Harness web tools by capability, not by name**: prompts say "your web search / page
   fetch / claim check tool" with pi-web-access and generic equivalents as examples. Use
   for broad/semantic discovery where scripted APIs don't reach.
3. **Manual steps** (gated PDFs, logged-in portals like Telemaco/Cerved): listed as
   explicit user actions, never automated.

Phase A question A8 expands to A0: produce the ranked tool matrix per research job
(source → best integration → fallback → cost model), verify the API endpoints actually
work with curl, and feed the result into a new skill reference (`references/tooling.md`,
exact placement decided in Phase B). In this authoring session, broad research uses the
exa MCP tools.

## Phase plan (B2B)

### Phase A — Italy research pass (web research; writes `research/idea-validation-italy-b2b/`)

Per-question agenda. ✅ = already verified in the parallel session (trusted).

| # | Question | Target sources | Feeds |
|---|---|---|---|
| A1 | ICP counts: imprese by ATECO × size class; professional-firm counts | ISTAT ASIA ✅, InfoCamere/Movimprese ✅, CNDCEC ✅, Cassa Forense 2025 ✅ (fetch the actual tables) | market-sizing |
| A2 | Italian SMB software price anchors: what micro-firms already pay (gestionali, fatturazione, legal practice tools) | incumbent pricing pages (TeamSystem, Zucchetti, Danea, Fatture in Cloud, Aruba, legal PM tools) | pricing, competitor-sources |
| A3 | PMI digital adoption and cloud/SaaS propensity | ISTAT "ICT nelle imprese", DESI/Digital Decade, Osservatori PoliMi | market-sizing (capture), distribution |
| A4 | Paid-channel units for Italy: Google Ads CPC (IT), Meta, LinkedIn IT | WordStream-class IT data, Google benchmarks | cac |
| A5 | Legal constraints on outreach: cold B2B email, PEC solicitation, GDPR/Garante position | Garante provvedimenti, e-privacy guidance | cac (cold_outbound), distribution |
| A6 | Which Italian operator communities actually exist and are active, per major vertical | direct verification (groups, forums, Telegram, association portals) | communities prompt (must name real ones) |
| A7 | Incumbent ecosystem map + whether incumbent marketplaces/app stores exist | vendor sites ✅ (list), verify marketplace/integration programs | incumbents prompt, competitor-sources, distribution |
| A8 | Apify/API coverage for Italian sources (registri, Capterra.it, jobs, PEC-safe enrichment; Cerved/CRIBIS/Atoka access models) | Apify store ✅ (general), vendor pages ✅ | prompts' tooling notes |
| A9 | Tender-portal signal for professional-firm niches | ANAC/BDNCP ✅, TED ✅ | linkedin/professional-web prompt |
| A10 | What does NOT exist publicly for Italy (so packs say so instead of fabricating) | negative-result log, same discipline as the existing research README | all packs |

### Phase B — rewrite (order respects the coupled-pack rules)

**Status: COMPLETE (2026-08-13).** All items below shipped, plus:
`references/tooling.md` + 5 dependency-free scripts in `scripts/` (the three
keyless ones smoke-tested live: Eurostat sbs_sc_ovw, TED v3, ANAC CKAN);
evidence gate in `scoring.md` (target-conditional, defined in the b2b
rubric pack at 15 Italian-source observations, cap at 74 + confidence low);
interview kit in `decision-memo.md`; `b2b_intermediary_access` in the
founder interview; B2B platform-file mapping note added to the five agents
with B2C-named hint tables; two new CAC channel keys (`intermediary_referral`,
`events_fairs`); cold outbound = `viable: false` statutory. `quick_validate`
passes. Remaining before commit: Phase C forward-tests.

1. `SKILL.md` + `memory.md`: target section (Italy statement, segment_size, guardrail
   bands D5), new B2B menu (D2), bilingual dispatch rule (D3), platform enum.
2. Trend prompts: new `incumbents.md`; rewrite `communities.md`, `linkedin.md`,
   `g2-capterra.md`; Italy addendum to shared `web-search.md` usage (b2b only).
3. `competitor-sources.md` + `market-sizing.md` (share the thin-review/count logic).
4. `demand-drivers.md` + `pricing.md` together (coupled: driver names key multipliers).
5. `retention.md` + `cac.md` together (coupled: d7/d30 semantics, lifespan).
6. `distribution.md`, then `scoring-rubrics.md` (+ evidence gate D4 in
   `references/scoring.md`) and the decision-memo interview kit (D4) in
   `references/decision-memo.md`.
7. Founder interview: add the deferred B2B questions (professional network, domain access,
   Italian-market access — HANDOFF open point 3) since founder-market fit now includes
   "can you reach Italian operators".

### Phase C — validation

- `quick_validate.py` after every step.
- Forward-tests (pi-skill-creator Step 5) with fresh subagents on two fake ideas:
  one professional-vertical (tool per studi commercialisti) and one generic PMI/e-commerce
  tool; test the enterprise/medium guardrail and the evidence-sufficiency gate.

### Phase B2 — prose audit against pi-skill-creator writing principles (done 2026-08-13)

Four parallel reviewers audited all 49 skill files against
`pi-skill-creator/references/writing-principles.md`; ~75 findings. Tiers 1–3
applied (~90 edits by four editor agents + main thread): contract breaks
(CAC lifespan read from the wrong retention field; monetization top band
requiring WTP ≥ €50/mo; market-sizer USD verdict bands moved into per-target
packs; `idea.md` B2C evidence template; missing `trend_velocity`/`overall_verdict`
anchors; watermark keyed to the wrong predicate; top-2 vs top-3 mismatch),
guardrail drift (ex-VAT qualifier, €50-ceiling nuance clause, cold-outreach
scope in memo + distribution brief, missing no-TAM clause in two templates),
and consistency (unified evidence-label block with `geography: IT | non-IT`
across the four b2b templates, one confidence definition, `sales_motion:`
frontmatter field documented, EUR in interview/segmentation/scoring, READMEs
relocated to `docs/`). `quick_validate.py` passes. Verified intact: gate ↔
scoring ↔ memo chain, demand-driver ↔ pricing keys, retention ↔ cac pack
semantics.

Deferred (apply during Phase D or a later pass):
- b2c pack sourcing (no source/date/confidence on any b2c figure; iOS-share
  table undated; "newly released" feature list rots).
- b2c template drift (tiktok tiers, x-twitter recency bullet, formatting);
  no disconfirming-evidence section in b2c templates (deliberate decision
  needed).
- Browse Path domains are consumer-only (interview.md) — b2b founder cannot
  reach professional niches via browse.
- `core-human-desires.md` off-pattern + Fairness desire maps to no dimension.
- TOCs missing on the eight >100-line b2b packs; pack skeleton alignment
  (b2b vs b2c section names).
- Cross-agent `confidence` field addition to every artifact schema (additive,
  target-neutral — do after forward-tests, not before).
- b2c SOM-fantasy trigger ($500K) vs "large" band floor ($200K) intentionally
  left as the original values.

Per the audit discipline, these edits are behavior changes tested against the
pre-audit snapshot (`d9b1976`): the Phase C forward-tests are the test round.

### Phase C log — Run 1 (Claude Code content test, done 2026-08-13)

Setup: scratch project `~/tmp/iv-test-1`, idea "client document-collection
portal beside TeamSystem for studi commercialisti", target b2b / micro /
assisted-self-serve. All specialists ran as generic Sonnet subagents
(executor-floor test; Fable Wave 1 was killed and redispatched on Sonnet
before any file was written). All five b2b platforms + the optional market
sizer. Full chain produced; verdict 45/100 pivot (v2, after market sizing),
confidence medium, gate not fired (18 IT observations vs threshold 15).

Checklist: 13/13 pass after two in-run patches (sales-motion band added to
scores+memo; nothing else needed). Highlights: cold_outbound viable:false
with art. 130 reason; intermediary_referral and events_fairs assessed;
buyer redirection sized on 69,200 studi (CNDCEC 2024), never 4.27M; dead
surfaces never cited live; Italian quotes carry parenthetical translations;
LinkedIn-groups open item answered (see
`research/idea-validation-italy-b2b/linkedin-groups-post-volume-note.md`).
Audit-fix validation: the d7-churn seam, the split paid_social keys, the
viable:false schema slot, the trend-velocity anchors, and the memo
version-note slot were all exercised and behaved.

Defects found and FIXED in this pass:
1. Pack-defaulted dimension vs missing_discount was ambiguous (a 46→55 =
   pivot→test swing): scoring.md now rules defaults count as UNAVAILABLE.
2. Retention rubric band gap (churn 5–7% matched no row): moderate band now
   3–7% with low-end positioning.
3. No sales_motion slot anywhere: added to scores.json schema (b2b-only,
   additive) and the memo score line.
4. Capture-rate rows can overlap (10× apart): lowest-applicable-band
   tie-break added to b2b/market-sizing.md.
5. No budget-tier default without user_profile.md: b2b/cac.md now defaults
   to Bootstrap and flags the gap (codifies what the CAC agent improvised).

Open observations (decide after Run 2):
- Evidence-label line format drifts per researcher (bulleted vs bracket
  blocks) — gate counting is manual; consider mandating one exact format.
- b2b monetization's top band needs "viable SOM" but the market sizer is
  optional in the validation chain — consider making it default for b2b.
- LinkedIn jobs actor failed 3× (group-posts actor fine); aggregator
  fallback worked. Watch in Run 2 before changing tooling.md.
- Pricing agent read the no-card-trial "Good" band at 5% — verify against
  the pack's entry-model table wording.
- Gate threshold 15: Run 1 counted 18 in an evidence-rich commercialisti
  niche — the threshold looks sane there; Run 2 (generic PMI) probes lower.

### Phase D — B2C (after B2B sign-off; outline only)

Ring policy: Italy → Europe-English → Western (NA, UK/IE, AU/NZ); Eastern excluded; app
languages Italian + English only. Trend prompts get ring-labeled sourcing (Italian TikTok/
App Store IT/Reddit-EN split); `market-sizing` sizes rings separately (SAM-Italy first);
`distribution`/`cac` mostly unchanged (global app stores) except IT-market CPI/ASO notes;
scoring unchanged. Detailed plan written after B2B lands.

## Open decisions for the user

1. **D4 threshold and mechanics** — cap-at-moderate vs. score-discount; the ~15-observation
   threshold is a first guess.
2. **D5 middle band** — agree that intermediary-assisted self-serve is in scope?
3. **`incumbents` as a fifth prompt replacing X/Twitter in the default B2B menu** — ok?
4. **Phase A executor** — run as web-research from this repo session (writes
   `research/idea-validation-italy-b2b/`), or hand any parts back to your parallel-session
   flow?

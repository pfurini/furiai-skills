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

### Phase C log — Run 2 (pi acceptance test, done 2026-08-13)

Setup: `~/tmp/iv-test-2`, pi with native `iv-*` dispatch (Opus orchestrator),
idea "returns-management dashboard for small Italian e-commerce merchants"
(self-serve band) plus an enterprise procurement-suite decoy. Verdict:
28/100 **drop** — first live firing of the floor penalty (retention 18 →
×0.72) — confidence medium, gate silent (21 IT observations vs 15).

Checklist: 12/13 applicable items PASS (market sizing N/A — not in the
default chain). The decoy was refused exactly per the guardrail ("clearly
sales-led and falls outside scope for desk research... No fan-out, no
score"). The Run-1 fixes held under a fresh orchestrator: pack-default
counted as unavailable (discount 5/6), `sales_motion` written to idea.md,
scores.json, and the memo line, `cold_outbound.viable=false`,
`paid_social_meta` key, events_fairs assessed via the relevance filter.

Exa incident: pi subagents fell back to Exa's free keyless MCP endpoint
(rate-limited) — root cause is in the pi stack, not the skill: pi-web-access
routes to `mcp.exa.ai` when `getApiKey()` resolves null, and the subagent
execution context fails to resolve `~/.pi/web-search.json`'s key that the
main session resolves fine. Impact on Run 2 was mild (3 mentions, 2 files;
gate count unaffected), so the run stands. Workaround: export
`EXA_API_KEY` in the shell launching pi. Root-cause fix belongs to a pi
session (suspects: pi-subagents nested-tools / pi-claude-bridge worker env).

Defect found and FIXED: the b2b menu reused the b2c `web-search.md`
template, which carries no evidence-label block — Run 2's web-search file
had zero per-finding geography labels (Run 1 masked this because the
orchestrator injected labels into the dispatch prompt). Added
`prompts/b2b/web-search.md` (Italy-first tiers, label slot E, disconfirming
-evidence section, keyword-unmeasured fallback) and pointed the SKILL.md
menu at it. Also: `skipped_channels` schema now specifies `{channel,
reason}` entries (Run 2 emitted bare strings).

Gate threshold check (open item 1): Run 1 counted 18, Run 2 counted 21,
both in genuinely evidence-rich niches; neither fired. The 15 threshold
looks sane; the label-format drift (fixed above for web-search) matters
more than the number. Keep 15 until a low-signal vertical (avvocati) is
actually run.

**Phase C is COMPLETE.** Both forward-tests pass; fixes committed.

### Phase D — B2C Italy-first refactor (full plan, written 2026-08-13)

**Ring policy (the organizing idea).** A b2c idea is validated ring by ring:
- **Ring 1 — Italy**: Italian-language consumer market, EUR, Italian surfaces
  (TikTok IT, App Store IT, Italian subreddits/forums, Google.it).
- **Ring 2 — Europe-English**: EU consumers reachable with an English-language
  app, EUR, English surfaces filtered to EU signal where possible.
- **Ring 3 — Western**: NA, UK/IE, AU/NZ; USD; the current global benchmarks.
- Eastern markets excluded. App languages: Italian + English only.
Every finding and figure carries a **ring label**; market sizing reports SAM
per ring, Italy first; distribution and CAC state which ring a benchmark
belongs to. Scoring mechanics stay target-neutral and unchanged.

#### Decisions needing user sign-off before edits (DD1–DD5)

| # | Decision | Recommendation |
|---|---|---|
| DD1 | Port the b2b evidence-label + disconfirming-evidence pattern into the five b2c templates? | Yes — labels become **ring** (IT / EU-EN / Western) instead of geography IT/non-IT, same confidence definition. Makes b2c evidence as falsifiable as b2b. |
| DD2 | b2c evidence gate? | No hard cap. Consumer niches have abundant global signal; a b2b-style cap misfires. Instead: a mandatory **ring-coverage disclosure** in `scores.json` (which rings the evidence came from) and a memo watermark when Ring-1 evidence is absent for an Italy-first idea. |
| DD3 | Currency handling | Benchmarks carry a ring column: EUR for Rings 1–2, USD for Ring 3. No conversion mixing inside one table row. |
| DD4 | Research-pass depth (D-A below) | Run DA1–DA5 as fresh web research; DA6 is annotate-and-source the existing global figures, no new hunting unless a figure is unfindable (then mark it a construct, confidence: low). |
| DD5 | Cross-artifact `confidence` field (both targets, additive, deferred from Phase B2) | Roll it out in D-B step 10 while the packs are open anyway. |

#### Phase D-A — Italy b2c research pass (writes `research/idea-validation-italy-b2c/`)

Same discipline as the b2b pass: every figure carries source + date +
confidence; each report ends with a "does not exist publicly" log; never
invent what the log says is missing.

| # | Question | Target sources | Feeds |
|---|---|---|---|
| DA1 | IT device/platform base: iOS vs Android share Italy (dated), smartphone penetration, App Store IT category structure | StatCounter (dated), Comscore/AGCOM reports | market-sizing platform filter |
| DA2 | Italian consumer app WTP anchors: EUR price points on the IT App Store for the main b2c categories (subscriptions, one-time) | IT App Store listings, vendor pricing pages | pricing |
| DA3 | Italian consumer paid-channel units: Meta/TikTok/Google CPI and CPC for IT consumer campaigns | published IT benchmarks (WordStream-class, agency reports) | cac |
| DA4 | Italian creator economy: TikTok/Instagram/YouTube IT — active categories, sponsorship cost norms, affiliate practices | published reports, creator-platform data | distribution, cac |
| DA5 | Italian-language consumer communities per major b2c niche, verified active (subreddits, forums, Facebook/Telegram) with the dead/degraded log | direct verification | reddit + web-search templates (must name real surfaces) |
| DA6 | Source-and-date the existing global (Ring 3) figures the b2c packs already carry: D1/D7/D30 retention table, capture rates, k-factor ranges, freemium conversions, CAC table | original sources where findable | all b2c packs (annotation pass) |
| DA7 | What does NOT exist publicly for Italian consumer apps (negative-result log) | — | all packs |

#### Phase D-B — rewrite (order respects the coupled-pack rules)

1. `SKILL.md` + `memory.md`: ring policy statement in the b2c part of the
   Target section; ring vocabulary defined once; Ring-1 research runs
   bilingually (Italian-first surfaces, same NICHE-verbatim rule).
2. Five b2c trend prompts (`tiktok.md`, `reddit.md`, `apps.md`,
   `web-search.md`, `x-twitter.md`): ring-labeled source tiers (Ring 1
   surfaces first), evidence labels + disconfirming-evidence section (DD1),
   and the Phase B2 drift fixes (tiktok tier structure + citation-inheritance
   clause; x-twitter recency bullet, list indentation, em-dash tier headers,
   sources-section wording; velocity-classification wording normalized).
3. `calibration/b2c/market-sizing.md`: ring-based SAM (Italy sized first,
   rings reported separately), date the iOS-share table (DA1), source the
   community multipliers and capture rates (DA6), align the SOM-fantasy
   trigger with the "large" band or state why they differ.
4. `demand-drivers.md` + `core-human-desires.md` together: retitle and clean
   core-human-desires (calibration-file opener naming its consumer, drop the
   meta/key-principle tail and trivia notes, fix the desire-2 name), resolve
   the Fairness & Justice mapping (fold into Control or declare it unscored),
   add the "driver NAMES are load-bearing" warning (b2c `pricing.md` is keyed
   to them exactly like b2b).
5. `calibration/b2c/pricing.md`: Ring-1 EUR anchors from DA2, ring column on
   WTP and conversion tables, source/date/confidence on every figure.
6. `retention.md` + `cac.md` together (coupled): add the schema keys to the
   b2c factor table (b2b already carries them), source the D1/D7/D30 table,
   IT channel units from DA3, rename "Indie Budget Tiers" → "Budget Tiers"
   (b2b's name).
7. `calibration/b2c/distribution.md`: App Store IT ASO notes, Italian
   creator-economy notes (DA4), settle one loop-table name for both targets
   ("Growth Loop Types").
8. `calibration/b2c/scoring-rubrics.md`: ring-coverage disclosure block per
   DD2; anchor the freemium +10 threshold to the pricing pack's table.
9. `references/interview.md`: Browse Path gets a fifth batch of Italian
   professional/SMB domains (or an explicit b2c/b2b routing note) — closes
   Phase B2 finding H8.
10. Cross-cutting, both targets: `confidence` field in every artifact schema
    (DD5); TOCs on the eight >100-line b2b packs; pack-skeleton alignment
    (section names in the same order per pack type).

#### Phase D-C — validation

- `quick_validate.py` after every step (same command).
- Forward-test: one Italian consumer idea (pick a niche with a real Ring-1
  surface, e.g. a hobby/family app) through the full chain in Claude Code
  with Sonnet executors, orchestrated per SKILL.md. Draft a b2c audit
  checklist first, analogous to Phase C's: ring labels on every finding,
  SAM-Italy reported first, EUR anchors in Ring-1 pricing, named-surface
  rule respected (DA5's verified list), Italian quotes translated, no
  invented search volumes, ring-coverage disclosure present in scores.
- Optional pi acceptance run after the CC run passes, same division as
  Phase C (content test in CC, acceptance in pi).

### Phase D-A log — Italy b2c research pass (done 2026-08-13)

DD1–DD5 approved by the user as recommended, 2026-08-13, before any edits.

Six reports written to `research/idea-validation-italy-b2c/` by six parallel
web-research agents (exa-backed, bilingual, executor prompts carried the date,
the confidence mandate, and the negative-log requirement). All six pass the
structure check (source + date + confidence on every figure; per-report
"does not exist publicly" log). README carries the headline synthesis and the
consolidated DA7 log.

Headlines the D-B rewrite must absorb (full detail in the README):
- Italy 35% iOS / 65% Android; the pack's iOS-share table is stale in 8 of 9
  rows (only Western Europe holds). Subscriptions are NOT price-equalized by
  Apple (EUR/USD observed 0.80–1.20): a subscription price is a decision, not
  a conversion. Indie EUR bands: 4,99–9,99 €/mo, 29,99–69,99 €/yr, VAT inside.
- Only ASA (Italy CPA $1.60 ≈ 0.42× US) and Meta (CPM €10.48, ~50% below
  global) have Italy-specific paid data; TikTok Italy = NOT REPORTED (citation
  ring); no Italy CPI from any MMP.
- No Italian app-install creator data exists; nano/micro TikTok/IG is the
  optimum; Amazon.it pays 0% on Android apps; disclosure liability falls on
  the commissioning advertiser (AGCM).
- 47 verified-active Italian surfaces; four niches with none (language
  learning, parenting-on-Reddit, general cooking, productivity-as-such);
  English-language trap subs documented for the templates.
- DA6 verdicts: retention D30 table 2–4× above published medians; annual-
  discount "avoid" band contradicts the market average (63–67%); CAC table
  conflates CPI with cost-per-payer; constructs confirmed (capture rates,
  community multipliers, driver multipliers, organic CAC, lifespan mapping).
- Corrections feeding back into b2b files (apply in D-B step 10 or a b2b
  touch-up): Superads €0.43 CPC currency basis unverified (carry the ratio,
  ~52% below global); Milan/Turin CPC premium unsupported after source
  exclusions.

Gated pulls left to the user (optional): Adjust Mobile App Trends 2026 +
AppsFlyer Subscription 2026 (would settle the retention premium), SplitMetrics
Apple Ads 2026 (Italy ASA cross-check), DeRev Listino 2026 full grid.

**Phase D-A is COMPLETE.** Next: Phase D-B rewrite in the plan's order.

### Phase D-B log — rewrite (done 2026-08-13)

All ten steps executed in order; `quick_validate.py` passed after every step.

1. SKILL.md + memory.md: ring policy in the Target section (B2C subsection
   before B2B), ring vocabulary `IT | EU-EN | Western` defined once,
   "Research language" section generalized (b2c Ring-1 bilingual, same
   NICHE-verbatim rule), dispatch envelope NICHE line now both-targets.
2. Five b2c templates: Ring-1 tiers first (named verified surfaces from
   DA5 with language-trap warnings in reddit.md; IT storefront + `gl=IT`
   trap in apps.md; Google.it SERP + keyword-unmeasured fallback in
   web-search.md; ONIM/Creative-Center-IT in tiktok.md; thin-Ring-1
   expectation in x-twitter.md), one exact mandated label-line format
   (`labels — ring: … · lang: … · surface: … · evidence: … · confidence:
   …`), disconfirming-evidence section (new §8, Sources → §9) in all five,
   Phase B2 drift fixes applied (tiktok tiers + citation inheritance;
   x-twitter recency bullet, em-dash tier headers, indentation, sources
   wording; velocity wording normalized).
3. b2c/market-sizing.md rewritten on the b2b skeleton: Step 0 ring
   reporting, Ring-1 population anchors, dated iOS table (StatCounter Jul
   2026; SEA/India/LATAM rows removed with the ring policy), construct
   labels (capture rates, multipliers — ratings-vs-reviews conflation
   fixed), Outcome Reality Check (RevenueCat/Adapty), verdict bands and
   fantasy trigger switched to EUR on summed rings with the
   trigger-vs-band difference stated, ring-split fallback price.
4. core-human-desires.md rewritten as a calibration table (trivia and
   meta tail dropped); Fairness & Justice folded into Control; desire-2
   name fixed; load-bearing driver-names warning added to
   demand-drivers.md.
5. b2c/pricing.md rewritten: Ring-1 mechanics block (VAT-inclusive, no
   subscription equalization, proceeds math, weekly-billing norm), ring
   columns on model sweet spots and category benchmarks (DA2 EUR anchors),
   annual-discount bands corrected (60–70% = published market average, no
   longer "avoid"), category billing-mix anchors added, lifetime split
   into launch-LTD (3–5× annual) vs mature tier (observed 8–15× annual),
   construct labels throughout.
6. retention.md + cac.md together: schema keys added to the b2c factor
   table; benchmark table reframed as well-executed-subscription band
   (construct) with a sourced published-median floor (D30 3–7%) and rules
   for when to use it; verdict-threshold anchoring note; cac.md renamed to
   "Budget Tiers" (EUR), Bootstrap default without user_profile, Ring-1
   channel-units table (ASA CPA $1.60 ≈ 0.42× US; Meta €10.48 CPM,
   seasonality 2.3×; TikTok = no data, never estimate; creator floor
   €100–300; Amazon.it 0% on apps), channel table redeclared as CPI with
   funnel-stage rule matched to the iv-cac-modeler brief (freemium
   conversion sits on the ARPU side — no double-counting), paid rows
   re-anchored to published CPI ranges, Product Hunt cohort corrected to
   ~100–1,000.
7. b2c/distribution.md: "Growth Loop Types" (name unified with b2b),
   k-rows re-anchored (Inherent 0.4–0.7 sustained; Incentivized 0.05–0.15
   per Extole; sources block added), per-ring ASO scoring with IT
   paid-chart observation, Ring-1 creator reality check (AGCM disclosure,
   bespoke deals), budget tiers in EUR with the ASA-under-€2 note; the
   accidental drop of Tier adjustment was caught and restored.
8. Ring-coverage disclosure chain (DD2): scoring.md Step 5b extended,
   `ring_coverage` added to scores.json (b2c only, additive, precedent:
   `sales_motion`), counting rule in b2c/scoring-rubrics.md (label lines
   only), NO-RING-1 watermark row + independent insertion rule in
   decision-memo.md; freemium +10 anchored to the pricing pack's table.
9. interview.md: Batch 5 — Business Tools (Italy-first B2B), 5 domains
   with a target-routing note; batch count 4 → 5 (closes B2 finding H8).
10. Cross-cutting: top-level `confidence` field in all 9 JSON agent
    schemas + trend-file frontmatter + memory.md contract line (idea.md
    already had one); Contents TOCs added to the seven >100-line b2b
    packs; b2b touch-ups from DA3 applied (Superads €0.43 → €0,43–0,50
    currency-unresolved with ratio framing, in b2b/cac.md and
    b2b/distribution.md; Milan/Rome CPC premium relabeled untested
    assumption).

Decisions taken inside the plan's discretion, to watch in D-C:
- Retention divergence resolved by REFRAMING (pack range = well-executed
  subscription band + sourced median floor), not by lowering the table.
  Overridable if the gated Adjust/AppsFlyer reports are ever pulled.
- b2c market-sizer verdict bands and reality checks moved from USD to EUR
  (same numerals) computed on summed rings.
- CAC funnel-stage rule must be exercised in the forward test (checklist
  item: no conversion double-counting in LTV:CAC).

**Phase D-B is COMPLETE.** Next: Phase D-C (b2c audit checklist, then
forward-test in Claude Code with Sonnet executors).

### Phase D-C — b2c audit checklist (drafted 2026-08-13, before the run)

Scored against raw artifacts from a fresh full-chain run. PASS/FAIL each:

1. **Label lines.** Every finding in every trend file carries the exact
   mandated line (`labels — ring: … · lang: … · surface: … · evidence: …
   · confidence: …`); counting by ring is mechanical.
2. **Ring-1 evidence, Italian-first.** Italian surfaces researched first;
   bilingual NICHE used verbatim by every researcher.
3. **Named-surface rule.** No dead/unverified surface cited as live; no
   English-language trap sub presented as Ring-1; private FB/Telegram as
   existence signals only.
4. **No invented volumes.** Without an Italian keyword instrument, the
   web-search file states "Italian keyword demand is unmeasured" once near
   the top; Ring-1 volume claims stay qualitative.
5. **Translations.** Italian quotes carry parenthetical translations;
   artifacts are in English.
6. **Disconfirming evidence.** Section present and substantive in every
   trend file (not a token line).
7. **Ring-based sizing** (if market sizer runs). SAM/SOM per ring, Italy
   first, EUR Rings 1–2 / USD Ring 3, verdict on summed EUR; dated iOS
   filter used; capture rates treated as constructs.
8. **Ring-1 pricing.** EUR VAT-inclusive anchors; subscription price set
   as a decision (no USD-conversion logic); model consistent with the pack
   menu; correct `currency` field.
9. **Retention discipline.** Schema factor keys present; the
   published-median floor path used (and stated) when ≥2 churn-risk
   factors or habit score < 2.5; D30 ↔ cac lifespan coupling consistent.
10. **CAC discipline.** Bootstrap default + flag when no user_profile;
    funnel-stage rule respected (no conversion double-count in LTV:CAC);
    Ring-1 units used where they exist; no invented TikTok-Italy costs;
    `skipped_channels` entries are {channel, reason}.
11. **Disclosure & confidence.** `ring_coverage` in scores.json matches a
    manual label count; evidence_gate rule "none defined"/false; top-level
    `confidence` present in every artifact (frontmatter or JSON).
12. **Memo logic.** NO-RING-1 watermark fires only when IT = 0 (expected
    NOT to fire in this run — negative test); EUR in memo numbers;
    concrete next step.
13. **Dispatch hygiene.** Date injected everywhere; agents wrote only
    their own artifacts; wave order respected.

### Phase D-C log — Run 1 (Claude Code content test, done 2026-08-13)

Setup: scratch project `~/tmp/iv-test-3`, idea "Cura Verde — plant-care
companion for Italian hobby gardeners (balcone, terrazzo, orto)", target
b2c, no user_profile.md (deliberate: exercises Bootstrap default + neutral
founder fit). All specialists ran as generic Sonnet subagents; all five
b2c platforms + the market sizer. Full chain produced. Verdict **45/100
pivot**, confidence medium, `ring_coverage` {IT 23, EU-EN 1, Western 29}
(53 mechanically countable label lines), evidence gate "none defined",
floor penalty silent (no dimension < 25). One market-sizer connection
failure was re-dispatched once per the workflow rule and succeeded.

Checklist: **11/13 PASS, 2 PARTIAL.**
- Item 3 PARTIAL: the reddit researcher reported r/giardinaggioITA
  "searched exhaustively, not found" while the DA5 pass had verified it
  ACTIVE the same day — a live named surface mis-reported as absent (the
  inverse of the dead-surface error the rule was written against).
- Item 5 PARTIAL: one Italian quote without a parenthetical translation
  (enforcement drift, no file defect).

New machinery validated live: exact label-line format held in 51/53
findings; ring-coverage disclosure written and NO-RING-1 correctly silent;
retention published-median floor path fired (4 churn-risk factors → D30
6%, disposable); ring-based sizing reported Ring 1 first in EUR with Rings
2–3 = n/a plus stated reasons, no reality check falsely triggered, outcome
reality check present; EUR verdict bands classified micro-niche
consistently (SOM y1 €1,861); pricing stayed EUR-native inside the
IT cluster and stated its conversion funnel; CAC applied Bootstrap default
with the profile-gap flag and kept funnel stages consistent;
`confidence` present in all 14 artifacts.

Defects found and FIXED in this pass:
1. Retention schema had no field to state the floor-path choice the pack
   demands: added `estimated_retention_rationale` (additive); pack now
   points at it.
2. iv-cac-modeler's LTV formula silently mis-handles prepaid annual plans
   (amortizes collected revenue by engagement lifespan — the executor
   caught and corrected it, a weaker one would not): annual-prepay rule
   added to the brief's LTV section.
3. b2c channel set lacked an `apple_search_ads` key despite ASA being the
   best-evidenced Ring-1 paid channel: additive row added.
4. iv-market-sizer had no precedence rule when the conservative-pick rule
   inverts the primary/supplementary approach roles: clarified (the
   conservative pick always wins; primacy governs what to attempt).
5. reddit.md named-surface list had no protection against confident
   absence claims: added the UNVERIFIABLE rule (never report a listed
   surface absent without fetched evidence).
6. 2/53 label lines dropped the `evidence:` slot: all five templates now
   mandate all five slots with `n/a` for unknowns.

Open observations (decide before/with the pi run):
- The reddit executor failed to *find* a live subreddit by search even
  though it exists — mirror-based discovery (not just verification) may
  need a hint in the template if it recurs in the pi run.
- The tiktok researcher labeled an unconfirmed aggregator as `ring: IT ·
  confidence: low` with an inline caveat — acceptable grey-zone handling;
  watch whether the pattern degrades under other executors.
- Translation enforcement (one missed quote) lives in SKILL.md's research
  language rule; consider echoing it in the trend-researcher brief if the
  pi run repeats the miss.

**Phase D-C Claude Code content test is COMPLETE.** Fixes applied and
validated. Remaining: optional pi acceptance run (same division as Phase
C: content test in CC, acceptance in pi; export `EXA_API_KEY` in the
launching shell).

## Open decisions for the user

1. **D4 threshold and mechanics** — cap-at-moderate vs. score-discount; the ~15-observation
   threshold is a first guess.
2. **D5 middle band** — agree that intermediary-assisted self-serve is in scope?
3. **`incumbents` as a fifth prompt replacing X/Twitter in the default B2B menu** — ok?
4. **Phase A executor** — run as web-research from this repo session (writes
   `research/idea-validation-italy-b2b/`), or hand any parts back to your parallel-session
   flow?

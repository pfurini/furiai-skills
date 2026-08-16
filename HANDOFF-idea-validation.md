# Handoff — idea-validation skill (Italy-first; B2B and B2C done)

Date: 2026-08-13. Repo: `furiai-skills`. Skill: `skills/idea-validation/`.
This file replaces the old handoff. It gives a fresh agent the context, the
rules, and the next tasks. Style: short sentences, one instruction each.

## What the skill is

One orchestrator skill (`SKILL.md`) validates indie product ideas and gives
a scored verdict. It has 11 subagents (`agents/iv-*.md`) and per-target
calibration packs. Two targets:
- `b2c` — consumer apps, **Italy-first with a ring policy**: Ring 1 Italy
  (EUR, Italian surfaces), Ring 2 Europe-English (EUR), Ring 3 Western
  (USD). Findings carry `ring: IT | EU-EN | Western` label lines; sizing
  reports rings separately, Italy first; scores carry a ring-coverage
  disclosure (no evidence gate).
- `b2b` — self-serve micro-SaaS for **Italian** micro (<10) and small
  (10–49) businesses and professional firms (commercialisti, avvocati,
  consulenti del lavoro, agencies, merchants). Medium (50–249) is edge
  scope. Sales-led products are out of scope.

The primary harness is **pi** with the `pi-web-access` extension. Claude
Code runs the skill through a fallback path (generic subagents). Do not
write harness-specific tool names into skill files. Describe capabilities.

## Current state

- Phase A (Italy research) is COMPLETE. Reports with citations are in
  `research/idea-validation-italy-b2b/`. Read its `README.md` first.
- Phase B (Italy-first rewrite of the whole B2B surface) is COMPLETE and
  committed, plus a Phase B2 prose audit against the pi-skill-creator
  writing principles (~90 fixes; see PLAN Phase B2 for what was deferred).
- Phase C (forward-tests) is COMPLETE, 2026-08-13. Run 1 (Claude Code,
  Sonnet executors): 45/100 pivot, checklist 13/13. Run 2 (pi, native
  dispatch, Opus): 28/100 drop, floor penalty fired, sales-led decoy
  refused, checklist 12/13 applicable. Both runs' fixes are committed.
  Full logs: `PLAN-italy-refactor.md` Phase C sections.
- Known pi-stack issue (not a skill defect): pi subagents fell back to
  Exa's free keyless endpoint (rate-limited) — pi-web-access `getApiKey()`
  resolves null in the subagent context while the main session resolves
  `~/.pi/web-search.json` fine. Workaround: export `EXA_API_KEY` in the
  shell launching pi. Root-cause investigation belongs in a pi session
  (suspects: pi-subagents nested-tools, pi-claude-bridge worker env).
- Phase D (B2C Italy-first refactor) is COMPLETE, 2026-08-14: D-A research
  pass (`research/idea-validation-italy-b2c/`, six reports), D-B rewrite
  (DD1–DD5 approved; all ten steps), D-C forward tests BOTH done — Run 1
  (Claude Code, Sonnet executors: 45/100 pivot, 11/13 + 2 partial, six
  defects fixed) and Run 2 (pi acceptance, Opus 5/high: 23/100 drop,
  10/13 + 3 partial, four more fixes; first live b2c floor-penalty
  firing). CAUTION for pi runs: pi loads the skill from
  `~/.pi/agent/skills/idea-validation/` — `diff -rq` it against the repo
  before dispatching, or you test a stale snapshot (it happened).
- The decision history is in `PLAN-italy-refactor.md` (decisions D1–D6 and
  DD1–DD5, tooling policy, phase logs). Read it if you need the "why".

## Fast orientation (read in this order)

1. `skills/idea-validation/SKILL.md` — target section, guardrail bands,
   B2B trend menu, dispatch envelope.
2. `references/memory.md` — store contract, platform slugs, frontmatter.
3. `references/calibration/b2b/pricing.md` and `market-sizing.md` — the
   pattern all B2B packs follow (EUR anchors, confidence tags, Italy rules).
4. `references/prompts/b2b/incumbents.md` — the pattern all B2B trend
   prompts follow (source tiers, evidence labels, disconfirming evidence).
5. `references/scoring.md` (Step 5b) + `calibration/b2b/scoring-rubrics.md`
   (the gate) + `references/decision-memo.md` (the interview kit).
6. `references/tooling.md` — scripts and endpoint facts.
7. `references/calibration/b2c/` packs and the five `references/prompts/`
   b2c templates — now Italy-first ring-calibrated, same pattern as the
   b2b siblings; the research behind the numbers is in
   `research/idea-validation-italy-b2c/` (read its README first).

## Rules that must not break

- Artifact schemas are identical for both targets. Only pack contents
  differ. New JSON fields must be additive and target-neutral.
- Benchmarks live in calibration packs. Mechanisms live in agent bodies.
  Do not mix them.
- Each agent writes exactly one artifact into `.idea-validation/`. Agents
  do not call each other.
- Interview, segmentation, scoring, and decision memo run on the main
  thread (`references/*.md`). Do not delegate them.
- Coupled files. Change them together:
  - `retention.md` ↔ `cac.md` (d7/d30 semantics, lifespan mapping).
  - `demand-drivers.md` ↔ `pricing.md` (driver names key the multipliers).
  - `scoring.md` Step 5b ↔ `calibration/*/scoring-rubrics.md` gate section
    ↔ `decision-memo.md` interview kit.
  - CAC channel keys come from the pack. The agent brief reads them as-is.
- Italy rules. Never soften these:
  - Cold email and cold PEC are prohibited (art. 130; Garante fines).
    `cold_outbound` is always `viable: false` for Italy.
  - Never present the ~4.27M micro-firm count as a TAM.
  - The self-serve ceiling is ~€50/mo ex-VAT. Above it, run the
    sales-motion check.
  - B2B trend prompts may name only surfaces verified active. Dead:
    Forum GT, InfoJobs Italia, connect.gt (degraded). No open forum exists
    for avvocati.
- Ring rules (b2c). Never soften these:
  - Ring vocabulary is exactly `IT | EU-EN | Western`, defined in SKILL.md.
  - The per-finding label-line format in the five b2c templates is
    mandated verbatim (all five slots; `n/a` for unknowns) — the scorer
    counts label lines mechanically into `ring_coverage`.
  - b2c has NO evidence gate; it has the ring-coverage disclosure + the
    NO-RING-1 memo watermark. Do not turn the disclosure into a cap.
  - EUR for Rings 1–2, USD for Ring 3; never mix currencies in one row.
  - Never cite the English-language trap subs (r/ItalianFood, r/ItalyTravel,
    r/italianlearning class) as Ring-1 evidence, and never report a
    template-named surface absent without fetched evidence (UNVERIFIABLE).
- B2B platform slugs: `incumbents | communities | linkedin | g2-capterra |
  web-search` (+ `x-twitter` on request). Keep `memory.md`, `SKILL.md`, and
  `iv-trend-researcher.md` in agreement.
- Validate after every edit:
  `python3 ~/.claude/skills/pi-skill-creator/scripts/quick_validate.py skills/idea-validation`
  (run from the repo root).

## Next task: open items

Phase D is fully complete (both forward tests). What remains is the
open-items list below, plus one standing practice: after any run, log
outcomes in PLAN, propose commits, update this handoff.

## Open items (in priority order)

1. **Gate threshold.** Both runs counted 18–21 in evidence-rich niches and
   the gate stayed silent, as it should. Keep 15 until a low-signal
   vertical (avvocati) actually runs; the label-format drift mattered more
   than the number (fixed for web-search; watch the other templates).
2. **Evidence-label format mandate.** DONE 2026-08-16 (user approved): the
   five b2b templates now mandate one exact `labels — …` line (all slots,
   `n/a` for unknowns), and the b2b gate counts `geography: IT` label
   lines mechanically (legacy-file fallback documented in the gate rule).
   Untested by a forward run — verify at the next b2b validation.
3. **Market sizer default for b2b.** DONE 2026-08-16 (user approved):
   `iv-market-sizer` now runs in Wave 4 by default for `target: b2b`
   (reads pricing.json; b2c stays on-request). Untested by a forward run.
4. **Missing data, do not fabricate:** AssoSoftware/Osservatori "Il
   software gestionale in Italia" (user must obtain); RPO tariff tables
   (only if the phone-consent bridge is ever modeled); Italian
   review→customer multipliers (none exist); indie capture rates (none
   exist anywhere). DONE 2026-08-16: Adjust Mobile App Trends 2026 and
   AppsFlyer Subscription Trends 2026 obtained and folded into the b2c
   packs (see `research/idea-validation-italy-b2c/gated-report-digests.md`;
   the retention-premium question is closed — no primary source exists).
   SplitMetrics 2026 also obtained (browser export): Italy dropped out of
   every top-15 ASA cost ranking — second-vendor bound corroborating
   MobileAction's cheap-Italy finding (CPA < $2.42, CPT < $1.51).
5. **Optional script:** DONE 2026-08-16 — `openapi_impresa_count.sh`
   written and verified against the free sandbox
   (`test.company.openapi.com`): `IT-search` with `dryRun` count-only
   (free ~100/day in prod), employee/turnover filters, sample mode. A
   production token with the company-API scope is needed for real counts
   (the current token is sandbox-only; key file gitignored).
6. **`prompts/b2b/README.md`** does not exist. Add one if prompt count
   grows again.

## Research records (source of truth for numbers)

- `research/idea-validation-italy-b2c/` — Italy consumer pass, 2026-08-13.
  Six reports (device base, EUR price anchors, paid channels, creator
  economy, verified communities, Ring-3 benchmark sourcing); README carries
  the synthesis and the consolidated negative log. Never invent a number a
  report lists as not existing.
- `research/idea-validation-italy-b2b/` — Italy pass, 2026-08-13. Five
  reports + `gated-pdf-digests.md` (MicroConf 2024, SaaS Capital RB32) +
  the two PDFs. Each report ends with a "does not exist publicly" list.
  Never invent a number that a report lists as not existing.
- `research/idea-validation-b2b-benchmarks/` — earlier global pass
  (churn, CAC units, capture). Still valid for global constructs.

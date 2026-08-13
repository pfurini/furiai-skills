# Handoff — idea-validation skill (Italy-first B2B)

Date: 2026-08-13. Repo: `furiai-skills`. Skill: `skills/idea-validation/`.
This file replaces the old handoff. It gives a fresh agent the context, the
rules, and the next tasks. Style: short sentences, one instruction each.

## What the skill is

One orchestrator skill (`SKILL.md`) validates indie product ideas and gives
a scored verdict. It has 11 subagents (`agents/iv-*.md`) and per-target
calibration packs. Two targets:
- `b2c` — consumer apps. Not refactored yet (see Open items).
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
- Phase D (B2C Italy-first refactor) is NOT started. It is the next task.
- The decision history is in `PLAN-italy-refactor.md` (decisions D1–D6,
  tooling policy, phase logs). Read it if you need the "why".

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
- B2B platform slugs: `incumbents | communities | linkedin | g2-capterra |
  web-search` (+ `x-twitter` on request). Keep `memory.md`, `SKILL.md`, and
  `iv-trend-researcher.md` in agreement.
- Validate after every edit:
  `python3 ~/.claude/skills/pi-skill-creator/scripts/quick_validate.py skills/idea-validation`
  (run from the repo root).

## Next task: Phase D — B2C Italy-first refactor

Ring policy: Italy → Europe (English apps) → Western (NA, UK/IE, AU/NZ);
Eastern markets excluded. The plan sketch is in `PLAN-italy-refactor.md`
(Phase D section). Write the full plan first; it needs the user's sign-off
before edits. Fold in the deferred b2c findings from the Phase B2 audit log
(unsourced b2c pack figures, browse-path domains, template drift,
disconfirming-evidence sections, `core-human-desires.md` cleanup).

## Done: Phase C — forward-tests (kept for reference)

Goal: prove the refactored skill works end to end, with fresh agents, on
fake but realistic runs. Two runs, two stages.

### Prerequisites

1. Ask the user for `APIFY_TOKEN` in the environment. It unlocks the
   review/jobs/LinkedIn-groups actors. Cost at test volume: a few euros.
2. `OPENAPI_TOKEN` is optional (free tier; sandbox at
   `test.visurecamerali.openapi.it`). Eurostat covers aggregates without it.
3. Do not use `DATAFORSEO_*` for these tests. Let the "keyword demand
   unmeasured" fallback fire. Confirm the packs flag it.
4. Web search in this repo's sessions: use the exa MCP tools. Load them
   with ToolSearch first.

### Run 1 — in Claude Code (content test)

1. Make a scratch project OUTSIDE this repo (example: `~/tmp/iv-test-1`).
   Run the skill there so `.idea-validation/` does not pollute this repo.
2. Idea brief: a vertical tool for studi commercialisti. Example: "a client
   document-collection portal that works beside TeamSystem". Target: b2b.
   Expected band: assisted self-serve. Expected gate: may fire.
3. Follow `SKILL.md` as the orchestrator. Use the Claude Code fallback:
   dispatch generic subagents with each agent body prefixed to the prompt.
4. Inject the current date into every subagent prompt.
5. Let the run write the full artifact chain: trend files → competitors,
   desire, distribution → pricing, retention → cac → scores → memo.
6. Audit with the checklist below. Fix pack/prompt defects. Re-validate.
   Iterate until the checklist passes.

### Run 2 — under pi (acceptance test)

1. Prepare a second scratch project and a one-paragraph prompt for the
   user. Idea brief: a generic PMI/e-commerce ops tool (self-serve band,
   gate not expected to fire). Also include one enterprise-flavored decoy
   idea to test the sales-led guardrail refusal.
2. The user runs it in pi. You cannot run pi from here.
3. Ask the user to bring back the `.idea-validation/` tree. Audit it with
   the same checklist. Differences to watch: native `iv-*` agent dispatch,
   per-agent models, `source_check` availability.

### Audit checklist (pass/fail, per run)

- [ ] Target and `segment_size` inferred and written to `idea.md`.
- [ ] Sales-motion band stated in the announcement and in scores + memo.
- [ ] Trend files use the new platform slugs and the bilingual NICHE.
- [ ] Every trend finding carries evidence labels (region, segment, stack,
      evidence type, confidence). Italian quotes have translations.
- [ ] Dead surfaces do not appear as live sources.
- [ ] Competitor set separates Italian-viable products from global ones.
- [ ] Market sizing runs the buyer-redirection step and names the buyer.
- [ ] No artifact quotes 4.27M (or any raw universe count) as TAM.
- [ ] `cac.json` has `cold_outbound.viable = false` with the legal reason.
- [ ] `intermediary_referral` and `events_fairs` channels are assessed.
- [ ] Evidence gate: `scores.json.evidence_gate` block present. If it
      fires: score ≤ 74, confidence "low", memo has the DESK-LIMITED
      watermark and the interview kit in Italian.
- [ ] Memo verdict logic and kill criteria are concrete.
- [ ] LinkedIn groups: record whether Italian professional groups showed
      real post volume (open verification item). Write the answer into
      `research/idea-validation-italy-b2b/` as a short note.

### After both runs

1. Write test outcomes and fixes into `PLAN-italy-refactor.md`.
2. Propose the commit(s) to the user. Suggested split: research reports /
   skill rewrite / scripts+tooling / test fixes.
3. Update this handoff: mark Phase C complete, promote Phase D.

## Open items (in priority order)

1. **Gate threshold.** Both runs counted 18–21 in evidence-rich niches and
   the gate stayed silent, as it should. Keep 15 until a low-signal
   vertical (avvocati) actually runs; the label-format drift mattered more
   than the number (fixed for web-search; watch the other templates).
2. **Evidence-label format mandate.** Findings' label lines still vary in
   shape per researcher (bulleted vs bracket blocks), making gate counting
   manual. Consider mandating one exact label-line format across the five
   b2b templates.
3. **Market sizer default for b2b?** The b2b monetization top band requires
   "viable SOM", but `iv-market-sizer` is optional in the validation chain.
   Decide whether b2b validation runs should include it by default (Run 1
   added it manually; Run 2 went without).
4. **Missing data, do not fabricate:** AssoSoftware/Osservatori "Il
   software gestionale in Italia" (user must obtain); RPO tariff tables
   (only if the phone-consent bridge is ever modeled); Italian
   review→customer multipliers (none exist); indie capture rates (none
   exist anywhere).
4. **Optional script:** `openapi_impresa_count.sh` (ATECO × province ×
   size counts). Develop against the free sandbox first.
5. **`prompts/b2b/README.md`** does not exist. Add one if prompt count
   grows again.

## Research records (source of truth for numbers)

- `research/idea-validation-italy-b2b/` — Italy pass, 2026-08-13. Five
  reports + `gated-pdf-digests.md` (MicroConf 2024, SaaS Capital RB32) +
  the two PDFs. Each report ends with a "does not exist publicly" list.
  Never invent a number that a report lists as not existing.
- `research/idea-validation-b2b-benchmarks/` — earlier global pass
  (churn, CAC units, capture). Still valid for global constructs.

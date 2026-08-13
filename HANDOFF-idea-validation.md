# Handoff — idea-validation skill

Date: 2026-08-13. Repo: `furiai-skills`. Skill: `skills/idea-validation/`.

## What the skill is

One orchestrator skill (`SKILL.md`) validates indie product ideas and gives a scored verdict.
It supports two targets: `b2c` (consumer apps) and `b2b` (self-serve micro-SaaS, no sales team).
Sales-led enterprise is out of scope. The skill says this to the user.

## What we did (commit order)

1. `1fa759c` — Refactor. The old pack had 16 skills that ran in sequence on the main thread.
   Now: 1 skill + 11 subagents (`agents/iv-*.md`) + main-thread references.
   The architecture copies `skills/super-code-review/`: agent files hold pi frontmatter
   (`model`, `thinking`, `prompt_mode: replace`) and a body that also works as an inline brief.
   Fallback chain: pi agent types → generic subagents with the body in the prompt → inline.
2. `ead8c83` — Router fix. Founder-profile requests have their own intent-router row.
3. `ab01f24` — Phase 1. All B2C benchmark tables moved to `references/calibration/b2c/*.md`.
   Agents keep only mechanisms. Each dispatch prompt carries `TARGET:` and `CALIBRATION:` paths.
   `idea.md` frontmatter has `target: b2c | b2b` (absent = b2c).
4. `7222d93` — Phase 2. Eight `references/calibration/b2b/*.md` packs and three B2B trend
   prompts (`references/prompts/b2b/`: g2-capterra, communities, linkedin).
   Gating tables (churn, conversion, CAC units, indie revenue cohorts) are web-sourced with
   citations. Construct tables are provisional and marked `confidence: low`.
   Raw research reports are in `research/idea-validation-b2b-benchmarks/`.
5. `1f59a81` — Phase 3. Orchestrator: target inference + confirmation, per-target trend
   platform menu, sales-led guardrail, extended platform enum, target-neutral pivot constraint.

## Rules that must not break

- Artifact schemas are identical for both targets. Only pack contents differ.
- Benchmarks live in calibration packs. Mechanisms live in agent bodies. Do not mix them.
- Each agent writes exactly one artifact into `.idea-validation/`. Agents do not call each other.
- Interview, segmentation, scoring, and decision memo run on the main thread
  (`references/*.md`). Do not delegate them.
- Some pack pairs share data: retention ↔ cac (D30 fallbacks, lifespan semantics),
  demand-drivers ↔ pricing (driver names key the multiplier table). Change them together.
- Validate after edits: `python3 ~/.claude/skills/pi-skill-creator/scripts/quick_validate.py skills/idea-validation`.

## Open points, in priority order

1. **Source-hardening pass** (user confirmed this comes next).
   Harden every table marked `confidence: low`: driver multipliers, B2B loop k-factors,
   capture bands, community multipliers, category WTP, saturation thresholds.
   Pull two gated PDFs by hand: MicroConf State of Independent SaaS; SaaS Capital NRR-by-ACV.
   Read `research/idea-validation-b2b-benchmarks/` first. It lists verified sources,
   data that does not exist in public, and fabricated figures to keep out.
2. **Forward-tests** (pi-skill-creator Step 5; skipped so far — all changes shipped untested).
   Run fake validation runs for both targets in a scratch project with fresh subagents.
   Also test the description triggers and the enterprise guardrail.
3. **Deferred small items**: B2B questions in the founder interview (professional network,
   domain access); market-insights extraction hint tables in some agents still name only
   B2C platform files.

## Fast orientation for a new agent

Read in this order: `skills/idea-validation/SKILL.md` → `references/memory.md` →
one workflow (`references/workflows/idea-validation.md`) → one agent
(`agents/iv-pricing-wtp.md`) with its two packs (`calibration/*/pricing.md`).
That shows every pattern the other files repeat.

# Memory contract

Persistent state for this pack. All specialist inputs and outputs use this tree. Paths are relative to the **current project root**.

## Structure (what actually gets written)

```
.idea-validation/
  user_profile.md          # interview + segmentation (main thread)
  market_insights/
    <niche>-<platform>-<YYYY>-<MM>.md
  ideas/
    <idea-slug>/
      idea.md
      screening_scores.json
      desire_scores.json
      competitors.json
      pricing.json
      cac.json
      market_size.json
      distribution.json
      retention.json
      scores.json
      weaknesses.json
      pivot_options.json
      pivot_report.md
      pivot_scores.json
      decision_memo.md
```

## Naming

- Trend files: `<niche>-<platform>-<YYYY>-<MM>.md` with `platform` one of `tiktok | reddit | apps | web-search | x-twitter` (b2c) or `incumbents | communities | linkedin | g2-capterra | web-search` (b2b; `x-twitter` on explicit request). Combined file only if the user asks: `<niche>-multi-<YYYY>-<MM>.md`.

## Protocol

- Specialists **write** their designated files.
- The orchestrator **reads** those files and passes paths into the next wave.
- Specialists do not call each other.
- Never delete an idea directory. Set `status: dropped` in `idea.md`.
- `user_profile.md` is updated incrementally (later steps merge fields).
- `market_insights/` is append-only: new dated file per run, never overwrite.
- Each `.json` artifact contains one JSON object and nothing else — no code fences, no commentary before or after.
- Every artifact carries a top-level `confidence: high | medium | low` field (JSON key or YAML frontmatter): the writing agent's evidence confidence, defined in each agent file. Additive and target-neutral. Exception: `scores.json` carries `score_confidence` (its own richer field) instead.

## Target (`idea.md` frontmatter)

Each idea carries `target: b2c | b2b` in its `idea.md` frontmatter, set once at workflow entry. It selects the calibration packs (`references/calibration/<target>/`) every specialist and the scoring step load. Absent → `b2c`. B2C ideas are validated ring by ring (Ring 1 Italy, Ring 2 Europe-English, Ring 3 Western — defined once in SKILL.md's Target section); findings and benchmark figures in b2c artifacts carry ring labels (`IT | EU-EN | Western`), and market sizing reports SAM per ring, Italy first. B2B ideas also carry `segment_size: micro | small | medium` (absent → micro/small; `medium` always triggers the sales-motion check in SKILL.md) and `sales_motion: self-serve | assisted-self-serve | sales-led` (the band inferred at workflow entry per SKILL.md). The artifact schemas are identical for both targets — only the rubrics and benchmarks behind them differ.

## Idea lifecycle (`idea.md` status)

| Status | Meaning |
|---|---|
| `candidate` | Generated, not yet fully validated |
| `in-validation` | Currently being analyzed |
| `scored` | Validation complete, has `decision_memo.md` |
| `active` | User is building this |
| `paused` | On hold |
| `dropped` | Not pursuing |

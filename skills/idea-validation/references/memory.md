# Memory contract

Persistent state for this pack. All specialist inputs and outputs use this tree. Paths are relative to the **current project root**.

## Bootstrap

If `<project-root>/.idea-validation/` is missing, create:

```
.idea-validation/
  market_insights/
  ideas/
```

Do not create `user_profile.md` until the founder interview runs. Do not seed sample ideas. Do not copy skill reference files into `.idea-validation/`.

If the tree exists, leave it in place and update files in situ.

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

- Idea slugs: kebab-case, max 40 characters, from the idea name (`habit-tracker-climbers`).
- Market-only research slugs: `market-` prefix (`market-nutrition-2026`).
- Trend files: `<niche>-<platform>-<YYYY>-<MM>.md` with `platform` one of `tiktok | reddit | apps | web-search | x-twitter`. Combined file only if the user asks: `<niche>-multi-<YYYY>-<MM>.md`.

## Protocol

- Specialists **write** their designated files.
- The orchestrator **reads** those files and passes paths into the next wave.
- Specialists do not call each other.
- Never delete an idea directory. Set `status: dropped` in `idea.md`.
- `user_profile.md` is updated incrementally (later steps merge fields).
- `market_insights/` is append-only: new dated file per run, never overwrite.
- JSON must be valid JSON.

## Idea lifecycle (`idea.md` status)

| Status | Meaning |
|---|---|
| `candidate` | Generated, not yet fully validated |
| `in-validation` | Currently being analyzed |
| `scored` | Validation complete, has `decision_memo.md` |
| `active` | User is building this |
| `paused` | On hold |
| `dropped` | Not pursuing |

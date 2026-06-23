# Report skeleton

The single-PR deliverable. Fill it from the synthesized findings (SKILL.md Step 4). Keep prose tight; code/templates verbatim. (Comparing two impls/branches? Use the compare report in `compare-mode.md`.)

---

## Single-review report

```markdown
# Review: <scope>

**Scope:** <git diff / branch / PR #n / files> · **Files:** <n> · **Guidelines:** <AGENTS.md/CLAUDE.md path(s)>
**Lenses run:** <list> · **Mode:** <express | inline | fan-out>

## Requirements adherence
**Target:** <issue/spec/plan, or "inferred from PR description">
- <requirement> — met | partial | missing · `file:line`
- **Deviations:** <none, or: did X instead of spec's Y — intended?>
- **Scope drift:** <none, or: ships Z not in spec>

## Strengths
- <specific, file:line — accurate praise; what to keep>

## Issues

### Critical (must fix) — bugs · security · data-loss · broken behavior
#### C1. <title>  · confidence <80-100> · `file.ts:LL-LL` · <bug|security|guideline>
- **What:** <wrong thing>
- **Why it matters:** <impact; who hits it>
- **Rule:** > <quoted AGENTS.md/CLAUDE.md line, if a violation>
- **Fix:** <concrete; code if non-obvious>

### Important (should fix) — architecture · missing feature · poor error handling · test gap
#### I1. <title> · confidence <80-100> · `file.ts:LL`
- **What / Why / Fix** (as above)

### Minor (nice to have) — style · polish · docs · micro-perf
#### M1. <title> · `file.ts:LL` — <one line + fix>

## Recommendations
- <process/architecture improvements beyond individual issues>

## Documentation impact
- `<file>` — <stale/missing> → <suggested fix> (or: none)

## Assessment
**Ready to merge:** Yes | No | With fixes
**Reasoning:** <1-2 sentence technical bottom line>
```

Append for orchestrator parsing:
```yaml
# review-summary
verdict: ready | with_fixes | not_ready
requirements: met | partial | gaps
critical: <n>
important: <n>
minor: <n>
top_issue: "<one line>"
strengths: <n>
```

---

> **Comparing two implementations / branches?** The compare report (verdict + per-dimension scorecard + `compare-summary` YAML) lives in `compare-mode.md` — load that instead.

---

## Rules
- **Verdict is never optional.** End with one.
- **Every finding has `file:line`.** No vague advice.
- **Bucket by real severity.** Not everything is Critical.
- **Praise before problems.** Specific, not performative.
- **If clean:** say `PASS — no findings ≥ 80 confidence`, list what you checked, done.

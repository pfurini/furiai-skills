# Compare mode (A vs B)

Opt-in path: reviewing 2+ implementations / branches / worktrees of the SAME change against each other. Single-PR review (SKILL.md) is the default — load this only when comparing. Everything in SKILL.md still applies (lenses, confidence/severity split, verify-cross-layer, false-positive filter); this file only changes scope, flow, and the report shape.

## Scope
Diff EACH impl vs its OWN merge-base — they may branch from different points, so diffing them against each other directly mixes in unrelated drift.
```
git merge-base <impl> <integration-branch>     # per impl
git diff <merge-base>...<impl>
```
State both bases out loud. Confirm the base gap is just unrelated commits (not feature work) before attributing differences.

## Flow
1. Pick the lens set (SKILL.md Step 2) — the SAME set for both impls.
2. Run each lens against EACH impl (fan-out: one subagent per impl, or per (lens × impl) for big diffs; inline per impl if small).
3. **Synthesize in ONE context holding BOTH.** Cross-impl trade-offs (A wins security, B wins UX) surface only when one mind sees both side-by-side. Per dimension: who wins, margin, why — with `file:line`.
4. Reconcile cross-layer exactly as single-review — verify the OTHER layer before grading a divergence (the render-sanitize lesson). A difference that another layer neutralizes is not a real edge.
5. Lead with the recommendation. Often a hybrid (base on X, port Y).

## Red flag
"One impl is obviously better" → score EVERY dimension; the loser of the overall often wins an axis. A one-axis win rarely decides it. Don't collapse to a single "better" before the scorecard is filled.

## Report

```markdown
# Comparative review: <A> vs <B>

**Change:** <what both implement> · **Bases:** A vs <merge-base>, B vs <merge-base> · **Lenses:** <list>

## Verdict (TL;DR)
- **Spec/requirements adherence:** <A | B | tie> — <why>
- **Overall quality:** <A | B | close/split> — <one line>
- **Ship recommendation:** <which, or hybrid + what to port>

## Scorecard
| Dimension | Winner | Margin | Note |
|---|---|---|---|
| Requirements | <A/B/tie> | <s/m/l> | <file:line> |
| Correctness | … | | |
| Security | … | | |
| … (one row per lens run) | | | |

## Key divergences
### <dimension> — edge to <A/B>
- **<A>:** `file:line` — <behavior>
- **<B>:** `file:line` — <behavior>
- **Severity / why it matters:** <reconciled across layers>

## Recommendation
<base on X; port Y from the other; the one-line fixes each needs before ship>
```

```yaml
# compare-summary
spec_adherence: A | B | tie
overall: A | B | close
recommend: "<base + ports>"
```

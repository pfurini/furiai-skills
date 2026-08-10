---
name: simplify
description: >-
  Clean up changed code without changing behavior. Reviews the diff with 4 parallel review
  subagents (reuse, simplification, efficiency, altitude), then applies the fixes directly.
  Quality only — it does not hunt for correctness bugs (use the super-code-review skill for
  that). Use when the user invokes /simplify or asks to simplify, clean up, de-duplicate, or
  improve the quality of recently changed code.
---

# Simplify

`/simplify → 4 cleanup agents in parallel → apply the fixes`

You are improving the quality of the changed code, not hunting for bugs. Review
it for reuse, simplification, efficiency, and altitude issues, then fix what you
find. Do not look for correctness bugs — that is what the `super-code-review`
skill is for.

## Phase 0 — Gather the diff

Run `git diff @{upstream}...HEAD` (or `git diff main...HEAD` / `git diff HEAD~1`
if there's no upstream) to get the unified diff under review. If there are
uncommitted changes, or the range diff is empty, also run `git diff HEAD` and
include the working-tree changes in scope — the review often runs before the
commit. If a PR number, branch name, or file path was passed as an argument,
review that target instead. Treat this diff as the review scope.

If an argument was passed, prefix every agent prompt with:
`Review target: \`<argument>\``

**Passing the diff to agents.** If the diff is small (roughly under 50 KB),
paste it inline into each agent prompt. If it is large, write it once to a temp
file (e.g. `/tmp/simplify-<session>.diff`) and pass each agent the path with
the instruction to Read it before starting.

## Phase 1 — Review (4 cleanup agents in parallel)

Launch **4 independent review agents** via the `Agent` tool, all in a
single message so they run concurrently — foreground `Agent` calls run
sequentially, so each call MUST set `run_in_background: true`. Use the four
dedicated agent types, one per angle:

```
Agent({ subagent_type: "simplify-reuse",          description: "Reuse review",          run_in_background: true, prompt: ... })
Agent({ subagent_type: "simplify-simplification", description: "Simplification review", run_in_background: true, prompt: ... })
Agent({ subagent_type: "simplify-efficiency",     description: "Efficiency review",     run_in_background: true, prompt: ... })
Agent({ subagent_type: "simplify-altitude",       description: "Altitude review",       run_in_background: true, prompt: ... })
```

Each agent's system prompt already carries its angle. The per-agent prompt is:
the optional `Review target:` prefix, the diff (inline or as a temp-file path),
and one closing line: "Review this diff for your angle and return your findings.
Do not edit any files."

Each returns its findings with `file`, `line`, a one-line `summary`, and the
concrete cost (what is duplicated, wasted, or harder to maintain).

The four angles (for your reference — the agents already know them):

### Reuse

Flag new code that re-implements something the codebase
already has — Grep shared/utility modules and files adjacent to the change,
and name the existing helper to call instead.

### Simplification

Flag unnecessary complexity the diff adds: redundant or derivable state,
copy-paste with slight variation, deep nesting, dead code left behind. Name
the simpler form that does the same job.

### Efficiency

Flag wasted work the diff introduces: redundant computation or repeated I/O,
independent operations run sequentially, blocking work added to startup or
hot paths. Also flag long-lived objects built from closures or captured
environments — they keep the entire enclosing scope alive for the object's
lifetime (a memory leak when that scope holds large values); prefer a
class/struct that copies only the fields it needs. Name the cheaper
alternative.

### Altitude

Check that each change is implemented at the right depth, not as a fragile
bandaid. Special cases layered on shared infrastructure are a sign the fix
isn't deep enough — prefer generalizing the underlying mechanism over adding
special cases.

Completion notifications arrive automatically when each agent finishes — do
not poll; wait until all four have reported.

## Phase 2 — Apply the fixes

Wait for all four agents to complete, dedup findings that point at the same
line or mechanism, and fix each remaining one directly. Skip any finding whose
fix would change intended behavior, require changes well outside the reviewed
diff, or that you judge to be a false positive — note the skip rather than
arguing with it. Finish with a brief summary of what was fixed and what was
skipped (or confirm the code was already clean).

## Fallback — single-pass (Agent tool unavailable)

`/simplify → Agent tool unavailable → single-pass inline cleanup → apply the fixes`

The `Agent` tool (or the `simplify-*` agent types) isn't available in this
context, so the usual 4-agent fan-out can't run. Work through all four angles
yourself, in this same context, in one pass — do not skip an angle for lack of
fan-out. The full angle definitions are in `agents/simplify-reuse.md`,
`agents/simplify-simplification.md`, `agents/simplify-efficiency.md`, and
`agents/simplify-altitude.md` (paths relative to this skill's directory) —
read them if available.

### Phase 1 — Review (4 cleanup angles, single pass)

Review the diff against each angle above in turn. For each, note findings with
`file`, `line`, a one-line `summary`, and the concrete cost (what is
duplicated, wasted, or harder to maintain).

### Phase 2 — Apply the fixes

Dedup findings that point at the same line or mechanism, and fix each
remaining one directly. Skip any finding whose fix would change intended
behavior, require changes well outside the reviewed diff, or that you judge to
be a false positive — note the skip rather than arguing with it. Finish with a
brief summary of what was fixed and what was skipped (or confirm the code was
already clean). State clearly in your summary that this was a single-pass
review done without the Agent tool, not the full 4-agent
fan-out, so whoever reads it isn't misled about what actually ran.

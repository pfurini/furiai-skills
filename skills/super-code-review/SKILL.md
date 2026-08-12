---
name: super-code-review
description: >-
  Comprehensive multi-dimension code review of a diff, branch, or PR, ending in one calibrated
  merge verdict. Fire whenever the user asks to review code, audit a change, check a PR/diff/branch
  before merge, find bugs/security/performance issues, assess test coverage, verify a change
  against its spec or plan, or asks "is this ready to merge" / "review my changes" / "look over
  this" — even if they don't say the word "review". Also fires to compare two implementations,
  branches, or worktrees of the same change.
---

# Super Code Review

Breadth comes from many lenses, depth from focused specialists, and truth from one synthesizer: fan-out finds, synthesis decides. Cross-cutting truths live between lenses, so per-lens findings are raw material — the synthesis pass in Step 4 is the product.

---

## Step 0 — Triage (always, cheap)

Decide eligibility, scope, and effort before reviewing anything.

**Eligibility.** Skip the review, and say why, when the PR is closed or a draft, comes from a bot, is trivially fine (typo, formatting), or you already reviewed it.

**Scope.** Pin what you review:

| Scope | Get diff |
|---|---|
| Unstaged | `git diff` |
| Staged | `git diff --staged` |
| Branch / PR | `git diff <base>...HEAD` or `gh pr diff <n>` |
| Files | read the named files |

Single-PR review is the default shape. Comparing 2+ implementations, branches, or worktrees of the same change? **Read `references/compare-mode.md` now** — it changes scope, routing, and the report.

**Effort routing.** Scale to size × stakes — stakes beat size. Pick ONE mode:

| If the change is… | Mode | Lenses to run |
|---|---|---|
| ≤ ~50 LoC, single concern, AND NOT touching security·auth·payments·migration·data-integrity | **Express** (Step 3A, lean) | requirements + correctness + the one obviously-relevant lens (for a bugfix, usually test-coverage: is there a regression test?) |
| Small/medium (≤ ~400 LoC), low stakes | **Inline** (Step 3A) | the applicable lenses — feature PR ≈ 6-8, bugfix ≈ 3-4 |
| Large / many files / pre-merge / touches security·auth·payments·migration / "thorough"·"audit"·"comprehensive" asked | **Fan-out** (Step 3B) | all applicable, in parallel |
| No subagents available (e.g. Claude.ai) | **Inline / Express** | as above, one context |

When unsure, go up a tier; escalate Inline → Fan-out if findings deepen.

Done when: scope and mode are stated out loud.

---

## Step 1 — Gather context (both modes)

1. **Guidelines.** Find the guideline file — AGENTS.md, or CLAUDE.md if there is no AGENTS.md — at the repo root and in every directory the diff touches. ("AGENTS.md/CLAUDE.md" below means whichever this repo has.) It guides code-writing, so not every line applies at review time.
2. **Intent.** Find the stated target: the issue, PR description, spec/plan, or acceptance criteria (an OpenSpec change, an RFC, a ticket, a design doc). This feeds the requirements lens. If none exists, infer the intent and say so.
3. **Diff + map.** Read the change. Identify languages/frameworks, entry points, blast radius.
4. **Historical context.**
   - `git blame` / `git log -p` on touched lines — judge findings in light of *why* the code is shaped this way; a "bug" that git history shows is intentional is a false positive.
   - Prior PRs touching these files and their review comments (`gh pr list`, `gh pr view`) — institutional memory, repeated mistakes.
   - In-code comments in modified files — does the change honor the guidance written there?

This context feeds every lens. Done when: all four items are gathered, or their absence is noted.

---

## Step 2 — The dimensions (13 lenses)

Each lens is a focused reviewer defined in one agent file (`agents/<file>`, paths relative to this skill's directory): subagent frontmatter plus the full checklist, anti-patterns, severity rubric, and output shape. In fan-out mode the file IS the subagent's system prompt (`subagent_type` = filename without `.md`); in inline mode, read the body below the frontmatter and apply it yourself. Run the lenses the diff needs (see *applies when*); lenses 1-4 apply to virtually every review.

| # | Lens | File | Applies when |
|---|---|---|---|
| 1 | Requirements & spec | `scr-requirements.md` | always — does it fulfill the task; scope drift; deviations |
| 2 | Correctness & bugs | `scr-correctness.md` | always — logic, null/async, races, off-by-one, leaks |
| 3 | Guidelines & conventions | `scr-guidelines.md` | always — AGENTS.md/CLAUDE.md rules, enums/barrels/circular, naming |
| 4 | Security | `scr-security.md` | any input/auth/data/secret/SQL/HTML/upload path; always for user-facing writes |
| 5 | Error handling | `scr-error-handling.md` | try/catch, fallbacks, callbacks, optional chaining touched |
| 6 | Type design | `scr-type-design.md` | new/changed types, interfaces, enums, constructors |
| 7 | Test coverage | `scr-test-coverage.md` | behavior changed; test files touched |
| 8 | Architecture & deps | `scr-architecture.md` | new modules, cross-module imports, dependency direction, god files |
| 9 | Evolvability | `scr-evolvability.md` | boolean-flag parades, feature isolation, premature abstraction |
| 10 | Performance | `scr-performance.md` | loops/queries/allocations/render paths; N+1, hot paths |
| 11 | Simplification | `scr-simplification.md` | dense/nested/duplicated code (advisory polish; opt-in) |
| 12 | Comments | `scr-comments.md` | comments/docstrings added or changed |
| 13 | Docs impact | `scr-docs-impact.md` | user-facing / config / API / env change |

---

## Step 3A — Inline review (small/medium)

Run the selected lenses yourself, in one context. For each: read its agent file (`agents/<file>`, the body below the frontmatter), apply the checklist to the diff, and collect findings (`file:line` + severity + why + fix). Then go to Step 4 — you are the synthesizer, with full shared context.

## Step 3B — Fan-out review (large/critical)

1. Build the lens list from Step 2, dropping the inapplicable.
2. **Dispatch every selected specialist in ONE message, one `Agent` call per lens, each with `run_in_background: true`** (foreground `Agent` calls run sequentially; the lenses share no state and need no ordering):

   ```
   Agent({ subagent_type: "scr-security", description: "Security review", run_in_background: true, prompt: ... })
   ```

   Each agent's system prompt already carries its lens; the per-agent prompt is scope + context only:
   ```
   SCOPE: base=<sha> head=<sha> · changed files=<list> · guidelines=<AGENTS.md/CLAUDE.md paths>
   CONTEXT: <Step-1 historical notes: blame findings, prior-PR comments worth knowing>
   Review this scope for your lens and return your findings. Do not edit any files.
   You have repo + git/gh access — run your own `git blame` / `gh pr view` if you need more context.
   ```
   If subagents lack repo access, bundle the diff text into the prompt.

   **Fallbacks:**
   - `scr-*` agent types not registered (the harness doesn't load this skill's `agents/` folder — e.g. Claude Code): dispatch generic subagents (`general-purpose` / Task) instead, prefixing each prompt with the full body of the lens's `agents/<file>` (everything below the frontmatter).
   - No subagent mechanism at all: fall back to Step 3A inline.
   - Use the Workflow tool only if the user explicitly opted into orchestration.
3. Completion notifications arrive as each agent finishes — do not poll. Wait for ALL, then go to Step 4.

---

## Step 4 — Synthesize (always, the heart)

Turn raw lens output into ONE verdict.

1. **Dedup.** The same `file:line` flagged by N lenses becomes one finding; note the angles.
2. **Reconcile cross-cutting.** For each finding ask: does another layer or lens neutralize or amplify it? (Server sanitize ↔ render sanitize; client validation ↔ server schema; a "missing test" already covered by an integration test. Real case: a server sanitizer that "fails open" looks like a security bug to the security lens — but is harmless because the *render* layer re-sanitizes.) **Verify the other layer** (grep or read it) before adjusting — don't assume. Severity comes from the WHOLE picture.
3. **Score two SEPARATE axes per finding:**
   - **Confidence = is it real?** (0-100). `0` false-positive/pre-existing · `25` maybe, unverified · `50` real but couldn't confirm it triggers · `75` verified, evidence supports · `100` certain, evidence confirms. **Drop everything < 80.** This axis is realness, NOT importance.
   - **Severity = impact if real.** Normalize each specialist's scale into one bucket:
     | Specialist emits | Bucket |
     |---|---|
     | Critical | **Critical** |
     | High / rating 8-10 / unmet core requirement | **Important** |
     | Medium / rating 5-7 | **Minor** |
     | Low / rating < 5 | drop (unless the fix is trivial) |
     Critical = bug · security exploit · data-loss · broken behavior. Important = arch problem · missing feature · unmet requirement · poor error handling · real test gap. Minor = style · polish · docs · micro-perf.
4. **False-positive filter** (discard): pre-existing issues outside the diff; lint/typecheck/compiler-catchable (assume CI runs); pedantic nits a senior wouldn't raise; issues on lines the change didn't touch; intentional changes; AGENTS.md/CLAUDE.md issues explicitly silenced in code.
5. **Acknowledge strengths** — accurate, specific praise makes the rest trusted.
6. **Write the report** using the template in `references/report-skeleton.md`. It ends with a clear verdict: Ready to merge — Yes / No / With fixes.

---

## Step 5 — Deliver (optional PR post)

Default: return the report in-conversation. If reviewing a PR and the user asked to post it:
```
gh pr comment <n> --body "<report>"
```
Cite findings with full-SHA permalinks: `https://github.com/<owner>/<repo>/blob/<full-sha>/<path>#L<a>-L<b>` — the full sha is required (`gh` won't expand `$(git rev-parse …)` inside markdown). Otherwise PR-posting is out of scope.

---

## Calibration rules (non-negotiable)

- **Evidence or it didn't happen.** Every finding carries `file:line`, what's wrong, WHY it matters, and how to fix it. No vague "improve error handling".
- **Cite the rule.** A guideline violation quotes the AGENTS.md/CLAUDE.md line.
- **Confidence ≠ severity.** A certain-but-trivial finding is high-confidence Minor; an unverified-but-scary one gets dropped until you verify it.
- **Severity = actual impact**, not effort to fix. Don't inflate.
- **Advisory lenses** (simplification, comments, docs) never modify files unless the user said `--fix`.

## Red flags (stop, you're rationalizing)

| Thought | Reality |
|---|---|
| "Clean diff, skip the requirements lens" | A correct build of the wrong thing still fails. Lens 1 always. |
| "Just concatenate the agent reports" | Synthesis is the product. Concatenation is noise. |
| "Security lens flagged it → Critical" | Check if another layer neutralizes it first. |
| "Report every issue I found" | Drop < 80 confidence. Noise kills trust. |
| "≤50 lines, ship it" | Stakes beat size — auth/SQL/payment/migration is never Express. |

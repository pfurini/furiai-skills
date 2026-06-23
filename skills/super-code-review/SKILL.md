---
name: super-code-review
description: >-
  Comprehensive multi-dimension code review for any diff, branch, or PR. Fire whenever the user
  asks to review code, audit a change, check a PR/diff/branch before merge, find bugs/security/perf
  issues, assess test coverage, verify a change matches its spec/requirements, or asks "is this ready
  to merge" / "review my changes" / "look over this" — even if they don't say the word "review".
  Covers 13 lenses (requirements, correctness, guidelines, security, error-handling, type-design,
  tests, architecture, evolvability, performance, simplification, comments, docs-impact) and routes
  between fast inline review and deep parallel specialist fan-out, then synthesizes ONE calibrated
  verdict. Use instead of an ad-hoc read-through; prefer it for any non-trivial review or when
  comparing two implementations.
---

# Super Code Review

One review skill. Covers every dimension 5 review skills + 7 specialist agents cover. Routes effort to the change. Ends with ONE synthesized, calibrated verdict.

**Core principle:** breadth from many lenses, depth from focused specialists, truth from ONE synthesizer. Fan-out finds; synthesis decides. Never ship raw per-lens dumps — reconcile them.

**Why a synthesizer is mandatory:** cross-cutting truths live between lenses. (Real case: a server sanitizer that "fails open" looks like a security bug to the security lens — but is harmless because the *render* layer re-sanitizes. Only a mind holding security + frontend + architecture together sees that.) Fan-out alone loses this. The synthesis pass rebuilds it.

---

## Step 0 — Triage (always, cheap)

Decide eligibility, scope, effort. Skip review when pointless.

**Eligibility** — skip / warn if: PR closed/draft, automated/bot PR, trivially-ok (typo/formatting), already-reviewed-by-you. Say so, stop.

**Scope** — pin what you review, then state it out loud before reviewing:
| Scope | Get diff |
|---|---|
| Unstaged | `git diff` |
| Staged | `git diff --staged` |
| Branch / PR | `git diff <base>...HEAD` or `gh pr diff <n>` |
| Files | read named files |

Single-PR review is the default shape. **Comparing 2+ implementations / branches / worktrees? Read `references/compare-mode.md` first** — it changes scope, routing, and the report.

**Effort routing** — scale to size × stakes. **Stakes beat size.** Pick ONE mode:
| If the change is… | Mode | Lenses to run |
|---|---|---|
| ≤ ~50 LoC, single concern, AND NOT touching security·auth·payments·migration·data-integrity | **Express** (Step 3A, lean) | requirements + correctness + the one obviously-relevant lens (bugfix → usually test-coverage: is there a regression test?) |
| Small/medium (≤ ~400 LoC), low stakes | **Inline** (Step 3A) | the applicable lenses — feature PR ≈ 6-8, bugfix ≈ 3-4 |
| Large / many files / pre-merge / touches security·auth·payments·migration / "thorough"·"audit"·"comprehensive" asked | **Fan-out** (Step 3B) | all applicable, in parallel |
| No subagents available (e.g. Claude.ai) | **Inline / Express** | as above, one context |

A 20-line change to an auth guard, a SQL query, a payment path, or a migration is **NOT Express** — the security/correctness lens is exactly what catches the dangerous thing. When unsure, go up a tier; escalate Inline→Fan-out if findings deepen.

---

## Step 1 — Gather context (both modes)

1. **Guidelines.** Find the guideline file — **AGENTS.md** (or **CLAUDE.md** if there's no AGENTS.md) — at the repo root + every dir the diff touches. The rule source; cite it on violations. It guides code-writing, so not every line applies at review. ("AGENTS.md/CLAUDE.md" below = whichever this repo has.)
2. **Intent.** Find the stated target — the issue, PR description, spec/plan, or acceptance criteria (e.g. an OpenSpec change, an RFC, a ticket, a design doc). Feeds the requirements lens. If none, infer it and say so.
3. **Diff + map.** Read the change. Identify langs/frameworks, entry points, blast radius.
4. **Historical context** (unique, high-value — from `/code-review`):
   - `git blame` / `git log -p` on touched lines → judge bugs in light of *why* the code is shaped this way. A "bug" git history shows is intentional = false positive.
   - Prior PRs touching these files + their review comments (`gh pr list`, `gh pr view`) → institutional memory, repeated mistakes.
   - In-code comments in modified files → does the change honor the guidance written there?
   This context feeds EVERY lens.

---

## Step 2 — The dimensions (the roster, 13 lenses)

Each is a focused reviewer. Read the matching specialist file (`references/specialists/<file>`) for its full checklist, anti-patterns, severity rubric, and output shape. Run the lenses the diff needs (see *applies-when*); lenses 1-4 run on virtually every review.

| # | Lens | File | Applies when |
|---|---|---|---|
| 1 | Requirements & spec | `requirements.md` | always — does it fulfill the task; scope drift; deviations |
| 2 | Correctness & bugs | `correctness.md` | always — logic, null/async, races, off-by-one, leaks |
| 3 | Guidelines & conventions | `guidelines.md` | always — AGENTS.md/CLAUDE.md rules, enums/barrels/circular, naming |
| 4 | Security | `security.md` | any input/auth/data/secret/SQL/HTML/upload path; always for user-facing writes |
| 5 | Error handling | `error-handling.md` | try/catch, fallbacks, callbacks, optional chaining touched |
| 6 | Type design | `type-design.md` | new/changed types, interfaces, enums, constructors |
| 7 | Test coverage | `test-coverage.md` | behavior changed; test files touched |
| 8 | Architecture & deps | `architecture.md` | new modules, cross-module imports, dependency direction, god files |
| 9 | Evolvability | `evolvability.md` | boolean-flag parades, feature isolation, premature abstraction |
| 10 | Performance | `performance.md` | loops/queries/allocations/render paths; N+1, hot paths |
| 11 | Simplification | `simplify.md` | dense/nested/duplicated code (advisory polish; opt-in) |
| 12 | Comments | `comments.md` | comments/docstrings added or changed |
| 13 | Docs impact | `docs-impact.md` | user-facing / config / API / env change |

Step-1 historical context is shared input, not a lens.

---

## Step 3A — Inline review (small/medium)

Run the selected lenses yourself, one context. For each: read its specialist file, apply the checklist to the diff, collect findings (`file:line` + severity + why + fix). Then Step 4 — you ARE the synthesizer (easy here: full shared context).

## Step 3B — Fan-out review (large/critical)

1. Build the lens list from Step 2 (drop the inapplicable).
2. **Dispatch every selected specialist in ONE message, multiple Task calls** (they share no state, same diff, no ordering). Use the Workflow tool only if the user opted into orchestration; else plain Task subagents.

   Per lens, the subagent prompt =
   ```
   <full contents of references/specialists/<file>>

   SCOPE: base=<sha> head=<sha> · changed files=<list> · guidelines=<AGENTS.md/CLAUDE.md paths>
   CONTEXT: <Step-1 historical notes: blame findings, prior-PR comments worth knowing>
   Return findings as: file:line · severity · what · why it matters · fix.
   You have repo + git/gh access — run your own `git blame` / `gh pr view` if you need more context.
   ```
   If subagents lack repo access, pre-bundle the diff text into the prompt.
3. Wait for ALL. Then Step 4 — **mandatory synthesis** (do NOT concatenate reports).

---

## Step 4 — Synthesize (always, the heart)

Turn raw lens output into ONE verdict.

1. **Dedup.** Same `file:line` flagged by N lenses → one finding; note the angles.
2. **Reconcile cross-cutting.** For each finding ask: does another layer/lens neutralize or amplify it? (server sanitize ↔ render sanitize; client validation ↔ server Zod; a "missing test" already covered by an integration test.) **Verify the other layer** (grep/read it) before adjusting — don't assume. Severity comes from the WHOLE picture.
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
5. **Acknowledge strengths** — accurate praise makes the rest trusted.
6. **Write the report** → `references/report-skeleton.md`. Clear verdict: Ready to merge — Yes / No / With fixes.

---

## Step 5 — Deliver (optional PR post)

Default: return the report in-conversation. If reviewing a PR and the user asked to post it:
```
gh pr comment <n> --body "<report>"
```
Cite findings with full-SHA permalinks: `https://github.com/<owner>/<repo>/blob/<full-sha>/<path>#L<a>-L<b>` — the full sha is required (`gh` won't expand `$(git rev-parse …)` inside markdown). Otherwise PR-posting is out of scope.

---

## Calibration rules (non-negotiable)

- **Evidence or it didn't happen.** Every finding: `file:line`, what's wrong, WHY it matters, how to fix. No vague "improve error handling".
- **Cite the rule.** Guideline violation → quote the AGENTS.md/CLAUDE.md line.
- **Confidence ≠ severity.** A certain-but-trivial finding is high-confidence/Minor; an unverified-but-scary one gets dropped (< 80 confidence) until you verify it.
- **Severity = actual impact**, not effort to fix. Don't inflate.
- **Verify the cross-layer claim** (the render-sanitize lesson) before grading a finding low OR high.
- **Advisory lenses** (simplify, comments, docs) never modify files unless the user said `--fix`.

## Red flags (stop, you're rationalizing)

| Thought | Reality |
|---|---|
| "Clean diff, skip the requirements lens" | A correct build of the wrong thing still fails. Lens 1 always. |
| "Just concatenate the agent reports" | Synthesis is the product. Concatenation is noise. |
| "Security lens flagged it → Critical" | Check if another layer neutralizes it first. |
| "Report every issue I found" | Drop < 80 confidence. Noise kills trust. |
| "≤50 lines, ship it" | Stakes beat size — auth/SQL/payment/migration is never Express. |

## Output

The synthesized report (`references/report-skeleton.md`) is the deliverable — not the per-lens dumps, not the diff. Always end with a verdict.

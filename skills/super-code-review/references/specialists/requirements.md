# Specialist: Requirements & spec adherence

Job: does the change do what it was ASKED to? The lead lens — a clean, bug-free diff that builds the wrong thing still fails. (This is the doc's "plan alignment" put first.)

## Establish the intent
Find the stated target: the linked issue/PR description, task, spec/plan, or acceptance criteria — e.g. an OpenSpec change (`proposal.md` + `specs/**` scenarios + `tasks.md`), an RFC, a Jira/Linear ticket, or a design doc. If none is given, infer from the PR title/description — and say what you assumed.

## Check
- **Each requirement / acceptance criterion → implemented?** Find the code that fulfills it (`file:line`). Anything in the spec with no implementing code = a gap (Important+).
- **Scenario coverage** (spec-driven): every named scenario has a path that satisfies it; the named tests exist.
- **Scope drift** — code doing things NOT in the spec → flag as silent scope creep; ask if intended (could be fine, could be risk).
- **Deviations from the plan** — implementation differs from how the spec said to build it. Justified improvement, or problematic departure? Name it specifically so the author confirms.
- **Cross-path "identical/consistent" clauses** — if the spec mandates that two code paths behave the same (e.g. a public vs a privileged path, or two callers of one shared rule), VERIFY they actually match; don't trust the claim.
- **Spec itself wrong?** If the requirement is contradictory, ambiguous, or a bad idea — say so. Review the plan, not only the code.

## Output
Per requirement: `met | partial | missing` + `file:line` evidence. List deviations (intended?) and any spec problems. Unmet requirement = Critical if it breaks the feature's purpose, else Important. (Comparing two impls? See `references/compare-mode.md` — this lens produces the per-scenario spec-adherence scorecard.)

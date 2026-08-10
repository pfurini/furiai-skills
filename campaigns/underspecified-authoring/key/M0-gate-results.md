# M0 question-gate results (2026-08-10)

30 no-artifact Haiku consumer runs (10 questions x 3 reps), clean-slate,
sequential execution, fixture staged **without `queries/`** (revision 1 below).
Grader: `harness/grade_consumers.py --gate`, two iterations (QS2 multi-line
answers misgraded by the line-only read; fixed and re-graded). Flagged runs
manually read per doctrine.

## Verdict: all 8 keyed questions pass the gate; both sanity questions pass.

| Q | Baseline correct | Wrong answers hit the predicted miss-variants |
|---|---|---|
| QB1 | 0/3 | r1 = 1214 (legacy `events` table); r2/r3 = multi-miss combos |
| QB2 | 0/3 | 2x "Acme Analytics" (legacy `users.account_id` join); 1x test account topping the naive count |
| QB3 | 0/3 | 2x 16.1 (test sessions included); 1x 16104.3 (that, plus seconds misread) |
| QB4 | 0/3 | 3x 3899 (test-account subscriptions included) |
| QC1 | 1/3 | 2x 12 (test accounts counted); 1 rep induced the filter from the `is_test` column name — under threshold, question stands |
| QC2 | 0/3 | 204/296/296 (heartbeats and other filters missed, combined) |
| QC3 | 0/3 | 372 (deleted-only filter), 412 (raw count), 372 |
| QC4 | 0/3 | 345/279/325 (no dedup and/or test accounts, combined) |
| QS1 | 3/3 | sanity: consumers drive sqlite fine |
| QS2 | 3/3 | sanity (after grader fix: answers list tables across lines) |

Raw records: scratchpad `gate/runs-v2/` (ephemeral), `grading-results.json`
copied alongside this file.

## Revisions made at M0 (pre-registered fallback paths, now pinned)

1. **Consumer-visible fixture copies exclude `queries/`.** Transcript-verified:
   with `queries/` visible, bare consumers located the canonical query files
   and ran them verbatim (QC1 via signups_by_quarter.sql, QC2 via
   monthly_active_users.sql), answering keyed questions correctly with no
   knowledge transfer. Producers keep the full repo; mining `queries/` for the
   conventions is the discovery task under test. Encoded in
   `harness/gate-one.sh` staging.
2. **All batches run sequentially with pre-batch credential re-export**
   (`harness/README.md` note 4): parallel headless launches with subscription
   OAuth hit a known upstream race (anthropics/claude-code #24317, #20553)
   that repeatedly killed whole batches and invalidates the exported
   credential file until re-exported. Schedule impact: the M1 consumer batch
   (~480 runs) is hours sequential, not the ~80 minutes planned at
   parallelism 6.

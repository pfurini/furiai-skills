# Harness

Two layers:

**Reference implementations** from the prior pi-skill-creator campaigns
(producer pilots, floor-doctrine A/B, masking check): `producer-one.sh`,
`producer-ab.sh`, `consumer-one.sh`, `grade.py`. Absolute paths inside (the
`SC` variable, prompt files, model ids) are that session's and must be adapted
before reuse. Kept as provenance and as the template the campaign scripts
below were derived from.

**Campaign scripts** for underspecified-authoring (env-driven, no hardcoded
session paths):

- `gate-one.sh` — one consumer run: per-run scrubbed-profile copy, fresh
  subject-visible fixture copy (subjects never see this repo), one question
  from `key/questions.json`, Haiku by default. `NONE` as the artifact runs the
  no-artifact baseline; a path runs `--add-dir <artifact>`. Requires env:
  `CAMPAIGN`, `RUNS_BASE`, `PROFILE_BASE`. Used for the M0 question gate and,
  with artifacts, for the M1/M3 consumer batches.
- `grade_consumers.py <runs-dir> [--gate]` — deterministic ANSWER-line grading
  against `key/expected-answers.json`, with predicted-miss variant matching as
  a diagnostic. `--gate` applies the pre-registered question-gate rule.
  Doctrine still applies: manually read every flagged run.

Campaign adaptations vs the reference scripts, recorded as method notes:

1. Consumer runs get `--dangerously-skip-permissions`: unlike the changelog
   pilots (text-only), these consumers must execute `sqlite3`.
2. Producer staging strips `README.md` from both treatment skill copies (see
   `../treatments/README.md`).
3. Grading is a deterministic script, not a grader agent: the executable
   fixture gives every keyed question a single correct value, which makes the
   benchmarking doctrine's grader-agent default strictly worse here (logged as
   a doctrine finding in PLAN.md).
4. **Parallel headless runs are unreliable with subscription OAuth** — the
   M0 gate lost three full batches to instant "Failed to authenticate: OAuth
   session expired and could not be refreshed" failures despite a token valid
   for hours. Root cause (researched 2026-08-10, sourced from
   anthropics/claude-code issues): refresh tokens are single-use and
   concurrent clones race the refresh (#24317), and on macOS the Keychain
   entry is shared across all `CLAUDE_CONFIG_DIR` profiles rather than
   namespaced (#20553), so one clone's failed/raced refresh poisons the
   session state for every subsequent launch until the main session repairs
   it — which is why lockout windows are transient and singles intermittently
   succeed. No env var disables the Keychain path. Consequences, now encoded
   here: `gate-one.sh` retries with backoff; batches run **sequentially**
   (P1, ~10s spacing) until the upstream fix lands; `preflight.sh <profile>
   [minutes]` still gates on token validity so a near-expiry export never
   starts a batch. The prior campaign's P6 recipe in benchmarking.md is
   therefore stale on this point — candidate doctrine patch, and a real
   schedule constraint for the M1/M3 consumer batches (~480 sequential runs
   is hours, not minutes; alternatives are `ANTHROPIC_API_KEY` auth (billing
   change, user decision) or upstream fixes).

The scrubbed-profile recipe (`.credentials.json` export + `.claude.json` copy,
no `--bare`, probe before trusting) is in
`skills/pi-skill-creator/references/benchmarking.md`.

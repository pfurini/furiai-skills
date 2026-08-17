# furiai-skills

Personal collection of agent skills for Claude Code and pi. The flagship is
**`skills/idea-validation`** — an Italy-first validation system for indie
product ideas (consumer apps and self-serve B2B micro-SaaS) with scored
verdicts, per-target calibration packs, and eleven research subagents. The
other directories are smaller utility skills.

Working docs for idea-validation: `HANDOFF-idea-validation.md` (current
state, rules, next tasks) and `PLAN-italy-refactor.md` (decision history and
phase logs). Research behind the calibration numbers lives in `research/`.

## Data-provider setup (idea-validation)

The research agents degrade gracefully without credentials (they say what is
unmeasured instead of inventing it), but the full experience needs the
providers below.

**Secrets convention:** the env vars below are the whole interface — the
skill uses a provider when its variable is set and degrades gracefully
(stating what is unmeasured) when it is not. Populate them however you
manage secrets (shell profile, direnv, a secret manager); never paste
them into prompts, commit them, or wire file paths into the skill.

| Env var | Provider | Setup | Cost |
|---|---|---|---|
| `EXA_API_KEY` | [exa.ai](https://exa.ai) — web search for research agents | dashboard → API key | pay-as-you-go, cents/run |
| `APIFY_TOKEN` | [apify.com](https://apify.com) — reviews, Reddit, Trustpilot IT, Telegram scraping | console → integrations → token | free $5/mo credit covers light use; $29/mo Starter beyond |
| `DATAFORSEO_LOGIN` / `DATAFORSEO_PASSWORD` | [dataforseo.com](https://dataforseo.com) — Italian keyword volumes + google.it SERPs | register (get $1 trial), **verify the account in the panel**, API password from the dashboard (not the login password) | ~$0.10–0.40 per validation run; $50 min deposit when the trial runs dry |
| `OPENAPI_TOKEN` | [console.openapi.com](https://console.openapi.com) — Italian company counts (Registro Imprese) | create a token scoped to **`GET company.openapi.com/IT-search`** only | count-only `dryRun` free ~100/day; lists €0.001/request |

Optional / not needed: `TAVILY_API_KEY`, `BRAVE_API_KEY` (search fallbacks);
SEOZoom (DataForSEO was chosen instead — see
`research/paid-data-providers-italy/README.md` for the full provider study
with prices). Eurostat, TED, and ANAC endpoints are keyless.

### Export and smoke-test

```bash
export EXA_API_KEY="..."
export APIFY_TOKEN="..."
export DATAFORSEO_LOGIN="<api login email>"
export DATAFORSEO_PASSWORD="..."   # the API password from app.dataforseo.com, not the account password
export OPENAPI_TOKEN="..."
# an empty or unset variable is a common failure: DataForSEO answers
# 40100 unauthorized to blank credentials, and the scripts refuse to run
# without their variables

S=skills/idea-validation/scripts
$S/dataforseo_volume.sh "riconoscimento piante"      # IT volumes (~$0.09/task)
$S/dataforseo_serp.sh "app per curare le piante" 10  # google.it SERP (~$0.002)
$S/openapi_impresa_count.sh 62.01 MI 1 9             # firm count, free dryRun
# Openapi sandbox (free, dummy data):
OPENAPI_HOST=https://test.company.openapi.com $S/openapi_impresa_count.sh 62.01 MI
```

### pi-specific notes

- Export `EXA_API_KEY` in the shell **before** launching pi — pi subagents
  fail to resolve `~/.pi/web-search.json` and silently fall back to Exa's
  rate-limited keyless endpoint otherwise (known pi-stack issue).
- pi loads its own installed copy of the skill from
  `~/.pi/agent/skills/idea-validation/`. Before any pi run, verify it
  matches the repo: `diff -rq ~/.pi/agent/skills/idea-validation/
  skills/idea-validation/` — a stale copy silently tests old behavior
  (it happened).

## Validation after editing the skill

```bash
python3 ~/.claude/skills/pi-skill-creator/scripts/quick_validate.py skills/idea-validation
```

Run it after every edit; the coupled-file rules that must not break are in
`HANDOFF-idea-validation.md`.

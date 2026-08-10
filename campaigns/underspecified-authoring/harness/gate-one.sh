#!/bin/bash
# One consumer run for the underspecified-authoring campaign.
#   $1 = question id (QB1..QS2), $2 = rep number, $3 = artifact path or NONE
# Env (required): CAMPAIGN (repo campaign dir), RUNS_BASE (output root),
#                 PROFILE_BASE (scrubbed profile with .credentials.json + .claude.json)
# Env (optional): CONSUMER_MODEL (default haiku 4.5)
set -euo pipefail
QID="$1"; REP="$2"; ART="${3:-NONE}"
D="$RUNS_BASE/$QID-r$REP"
rm -rf "$D"
mkdir -p "$D/profile"
cp "$PROFILE_BASE/.credentials.json" "$D/profile/"
cp "$PROFILE_BASE/.claude.json" "$D/profile/"
chmod 700 "$D/profile"; chmod 600 "$D/profile/.credentials.json"

# fresh subject-visible fixture copy per run (subjects never see the repo).
# Consumers do NOT get queries/: the M0 gate showed bare consumers finding and
# running the canonical queries verbatim (pre-cooked answers), which breaks
# every question a query file maps to. The deployment story is "agents get the
# data and the docs"; the conventions must come from the skill under test.
# Producers (separate runner) keep the full repo — mining queries/ IS the task.
cp -R "$CAMPAIGN/fixture" "$D/repo"
rm -rf "$D/repo/queries"

PROMPT=$(python3 - "$QID" "$ART" <<'EOF'
import json, sys, pathlib
qid, art = sys.argv[1], sys.argv[2]
spec = json.loads((pathlib.Path(__import__('os').environ["CAMPAIGN"]) / "key" / "questions.json").read_text())
skill = "" if art == "NONE" else spec["skill_sentence_with_artifact"].replace("{ARTIFACT_PATH}", art)
print(spec["consumer_prompt_template"]
      .replace("{SKILL_SENTENCE}", skill)
      .replace("{QUESTION}", spec["questions"][qid]))
EOF
)

cd "$D/repo"
MODEL="${CONSUMER_MODEL:-claude-haiku-4-5-20251001}"
EXTRA=()
[ "$ART" != "NONE" ] && EXTRA=(--add-dir "$ART")

# Transient auth lockouts (observed at M0): bursts of headless launches from a
# cloned profile intermittently die at startup with "Failed to authenticate:
# OAuth session expired and could not be refreshed", even with a token valid
# for hours; the same run succeeds moments later. Retry with backoff.
for attempt in 1 2 3 4; do
  set +e
  CLAUDE_CONFIG_DIR="$D/profile" claude -p "$PROMPT" --model "$MODEL" \
    --dangerously-skip-permissions ${EXTRA[@]+"${EXTRA[@]}"} > "$D/out.md" 2> "$D/err.log"
  rc=$?
  set -e
  if ! grep -q "Failed to authenticate" "$D/out.md"; then
    echo "$QID-r$REP exit=$rc attempts=$attempt"
    exit 0
  fi
  sleep $((30 * attempt + RANDOM % 20))
done
echo "$QID-r$REP AUTH-FAILED after 4 attempts"
exit 1

#!/bin/bash
# Consumer run: $1 = run name, $2 = artifact path or NONE
set -u
SC=/private/tmp/claude-501/-Users-paolof-Developer-ai-furiai-skills/3230d953-0df0-449f-9fe6-1818a68bedcd/scratchpad
NAME="$1"; ART="$2"
D=${CONS_BASE:-$SC/pilot/cons}/$NAME
mkdir -p "$D/profile"
cp $SC/pilot/minprofile/.credentials.json "$D/profile/"
cp $SC/pilot/minprofile/.claude.json "$D/profile/"
chmod 700 "$D/profile"; chmod 600 "$D/profile/.credentials.json"
cd "$D"
MODEL="${CONSUMER_MODEL:-claude-haiku-4-5-20251001}"
if [ "$ART" = "NONE" ]; then
  CLAUDE_CONFIG_DIR="$D/profile" claude -p "$(cat $SC/pilot/prompts/consumer-base.txt)" \
    --model "$MODEL" > out.md 2> err.log
else
  CLAUDE_CONFIG_DIR="$D/profile" claude -p "$(sed "s|ARTIFACT_PATH|$ART|g" ${PROMPT_FILE:-$SC/pilot/prompts/consumer-with.txt})" \
    --model "$MODEL" --add-dir "$ART" > out.md 2> err.log
fi
echo "$NAME exit=$?"

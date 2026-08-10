#!/bin/bash
# Haiku producer run: $1 = name (e.g. T1r1), $2 = prompt file, $3 = --add-dir path or NONE
set -u
SC=/private/tmp/claude-501/-Users-paolof-Developer-ai-furiai-skills/3230d953-0df0-449f-9fe6-1818a68bedcd/scratchpad
NAME="$1"; PROMPT="$2"; ART="$3"
T=${NAME:0:2}; R=${NAME:2:2}
D=$SC/pilot/prod-h/$T/$R
mkdir -p "$D/profile"
cp $SC/pilot/minprofile/.credentials.json "$D/profile/"
cp $SC/pilot/minprofile/.claude.json "$D/profile/"
chmod 700 "$D/profile"; chmod 600 "$D/profile/.credentials.json"
cd "$D"
if [ "$ART" = "NONE" ]; then
  CLAUDE_CONFIG_DIR="$D/profile" claude -p "$(cat "$PROMPT")" \
    --model claude-haiku-4-5-20251001 --dangerously-skip-permissions > claude-out.log 2> claude-err.log
else
  CLAUDE_CONFIG_DIR="$D/profile" claude -p "$(cat "$PROMPT")" \
    --model claude-haiku-4-5-20251001 --dangerously-skip-permissions --add-dir "$ART" > claude-out.log 2> claude-err.log
fi
echo "$NAME exit=$?"

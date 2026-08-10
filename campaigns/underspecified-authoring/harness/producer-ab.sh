#!/bin/bash
set -u
SC=/private/tmp/claude-501/-Users-paolof-Developer-ai-furiai-skills/3230d953-0df0-449f-9fe6-1818a68bedcd/scratchpad
NAME="$1"; ART="$2"
D=$SC/pilot/prod-ab/$NAME
mkdir -p "$D/profile"
cp $SC/pilot/minprofile/.credentials.json "$D/profile/"
cp $SC/pilot/minprofile/.claude.json "$D/profile/"
chmod 700 "$D/profile"; chmod 600 "$D/profile/.credentials.json"
cd "$D"
CLAUDE_CONFIG_DIR="$D/profile" claude -p "$(sed "s|SKILL_PATH|$ART|g" $SC/pilot/prompts/AB.txt)" \
  --model claude-fable-5 --dangerously-skip-permissions --add-dir "$ART" > claude-out.log 2> claude-err.log
echo "$NAME exit=$?"

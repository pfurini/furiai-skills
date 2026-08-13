#!/usr/bin/env bash
# Exa semantic web search / cited answer. Requires EXA_API_KEY.
#
# Usage: exa_search.sh "<query>" [numResults=10]        -> /search with text
#        EXA_MODE=answer exa_search.sh "<claim/question>" -> /answer (cited answer, $5/1k)
set -euo pipefail
: "${EXA_API_KEY:?EXA_API_KEY env var is required}"
QUERY="${1:?usage: exa_search.sh <query> [numResults]}"
N="${2:-10}"
if [ "${EXA_MODE:-search}" = "answer" ]; then
  curl -sfS -X POST "https://api.exa.ai/answer" \
    -H "x-api-key: ${EXA_API_KEY}" -H "Content-Type: application/json" \
    -d "$(jq -n --arg q "$QUERY" '{query:$q, text:true}')"
else
  curl -sfS -X POST "https://api.exa.ai/search" \
    -H "x-api-key: ${EXA_API_KEY}" -H "Content-Type: application/json" \
    -d "$(jq -n --arg q "$QUERY" --argjson n "$N" '{query:$q, numResults:$n, contents:{text:{maxCharacters:1500}}}')"
fi

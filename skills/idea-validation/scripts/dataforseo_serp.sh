#!/usr/bin/env bash
# Google.it SERP observation via DataForSEO (organic live advanced).
# Requires DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD.
#
# Usage: dataforseo_serp.sh "<query>" [depth=10] [location_code=2380 Italy] [language_code=it]
#        DATAFORSEO_HOST=https://sandbox.dataforseo.com ... -> free integration test (dummy data)
#
# Cost: ~$0.002 per live SERP; the response's tasks[].cost states it.
# Output keeps what the web-search template reads: organic ranks, ads (advertiser
# willingness to pay), People-Also-Ask, and the full item-type mix.
set -euo pipefail
: "${DATAFORSEO_LOGIN:?DATAFORSEO_LOGIN env var is required}"
: "${DATAFORSEO_PASSWORD:?DATAFORSEO_PASSWORD env var is required}"
QUERY="${1:?usage: dataforseo_serp.sh <query> [depth] [location_code] [language_code]}"
DEPTH="${2:-10}"
LOC="${3:-2380}"
LANG_CODE="${4:-it}"
BASE="${DATAFORSEO_HOST:-https://api.dataforseo.com}"

PAYLOAD="$(jq -n --arg q "$QUERY" --argjson d "$DEPTH" --argjson loc "$LOC" --arg lang "$LANG_CODE" \
  '[{keyword: $q, location_code: $loc, language_code: $lang, depth: $d}]')"

RESP="$(curl -sS -u "${DATAFORSEO_LOGIN}:${DATAFORSEO_PASSWORD}" \
  -X POST "${BASE}/v3/serp/google/organic/live/advanced" \
  -H "Content-Type: application/json" -d "$PAYLOAD")"
STATUS="$(printf '%s' "$RESP" | jq -r '.status_code // 0')"
if [ "$STATUS" != "20000" ]; then
  printf 'DataForSEO error %s: %s\n' "$STATUS" "$(printf '%s' "$RESP" | jq -r '.status_message // "no message"')" >&2
  case "$STATUS" in 401*|403*) echo "hint: check that DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD are exported and non-empty (use the API password from app.dataforseo.com, not the account password)" >&2;; esac
  exit 1
fi
printf '%s' "$RESP" | jq '{cost: .tasks[0].cost, status: .tasks[0].status_message,
     item_types: .tasks[0].result[0].item_types,
     ads_present: ([.tasks[0].result[0].items[]? | select(.type=="paid")] | length > 0),
     organic: [.tasks[0].result[0].items[]? | select(.type=="organic")
       | {rank: .rank_group, title, domain, url}],
     paid: [.tasks[0].result[0].items[]? | select(.type=="paid")
       | {rank: .rank_group, title, domain}],
     people_also_ask: [.tasks[0].result[0].items[]? | select(.type=="people_also_ask")
       | .items[]? | .title]}'

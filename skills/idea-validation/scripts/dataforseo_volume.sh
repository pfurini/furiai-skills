#!/usr/bin/env bash
# Italian keyword volumes via DataForSEO Google Ads endpoint.
# Requires DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD ($50 min deposit; $1 trial works).
#
# Usage: dataforseo_volume.sh "kw1,kw2,..." [location_code=2380 Italy] [language_code=it]
#        DATAFORSEO_HOST=https://sandbox.dataforseo.com ... -> free integration test (dummy data)
#
# Cost: one live task (up to 1,000 keywords) — cents; the response's tasks[].cost states it.
set -euo pipefail
: "${DATAFORSEO_LOGIN:?DATAFORSEO_LOGIN env var is required}"
: "${DATAFORSEO_PASSWORD:?DATAFORSEO_PASSWORD env var is required}"
KEYWORDS="${1:?usage: dataforseo_volume.sh \"kw1,kw2,...\" [location_code] [language_code]}"
LOC="${2:-2380}"
LANG_CODE="${3:-it}"
BASE="${DATAFORSEO_HOST:-https://api.dataforseo.com}"

PAYLOAD="$(jq -n --arg kws "$KEYWORDS" --argjson loc "$LOC" --arg lang "$LANG_CODE" \
  '[{keywords: ($kws | split(",") | map(gsub("^\\s+|\\s+$";"")) | map(select(length>0))),
     location_code: $loc, language_code: $lang}]')"

RESP="$(curl -sS -u "${DATAFORSEO_LOGIN}:${DATAFORSEO_PASSWORD}" \
  -X POST "${BASE}/v3/keywords_data/google_ads/search_volume/live" \
  -H "Content-Type: application/json" -d "$PAYLOAD")"
STATUS="$(printf '%s' "$RESP" | jq -r '.status_code // 0')"
if [ "$STATUS" != "20000" ]; then
  printf 'DataForSEO error %s: %s\n' "$STATUS" "$(printf '%s' "$RESP" | jq -r '.status_message // "no message"')" >&2
  case "$STATUS" in 401*|403*) echo "hint: check DATAFORSEO_LOGIN / DATAFORSEO_PASSWORD (use the API password from app.dataforseo.com, not the account password; export with an absolute key-file path)" >&2;; esac
  exit 1
fi
printf '%s' "$RESP" | jq '{cost: .tasks[0].cost, status: .tasks[0].status_message,
     results: [.tasks[0].result[]? | {keyword, search_volume, cpc, competition, competition_index,
       trend_last_month: (.monthly_searches[0].search_volume? // null)}]}'

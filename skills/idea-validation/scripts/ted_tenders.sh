#!/usr/bin/env bash
# EU tender notices from the TED Search API v3. No API key.
# POST-only; `fields` must be non-empty; CPV codes must be full 8-digit.
#
# Usage: ted_tenders.sh <CPV 8-digit, comma-separated> [country=ITA] [days=30] [limit=20]
# Output: JSON array of {publication-number, notice-title, buyer-name, publication-date}
set -euo pipefail
CPV="${1:?usage: ted_tenders.sh <CPV8[,CPV8...]> [country] [days] [limit]}"
COUNTRY="${2:-ITA}"; DAYS="${3:-30}"; LIMIT="${4:-20}"
CPV_LIST="$(echo "$CPV" | sed 's/,/ /g')"
QUERY="classification-cpv IN (${CPV_LIST}) AND buyer-country IN (${COUNTRY}) AND publication-date >= today(-${DAYS})"
curl -sfS -X POST "https://api.ted.europa.eu/v3/notices/search" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg q "$QUERY" --argjson l "$LIMIT" \
        '{query:$q, fields:["publication-number","notice-title","buyer-name","publication-date"], limit:$l}')" \
  | jq '.notices // .results // .'

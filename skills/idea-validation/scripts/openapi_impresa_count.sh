#!/usr/bin/env bash
# ICP company counts from the Registro Imprese via Openapi.com Company API (IT-search).
# Requires OPENAPI_TOKEN (scoped to the company API).
#
# Usage: openapi_impresa_count.sh <atecoCode> [province] [minEmployees] [maxEmployees]
#   e.g. openapi_impresa_count.sh 6201 MI 1 9
# Count-only by default (dryRun — free ~100/day in production, then ~€0.01/call).
#   OPENAPI_SAMPLE=<n>   -> return a sample of n companies instead (billed per request in prod)
#   OPENAPI_TURNOVER="min-max" -> add a revenue filter in EUR (e.g. "0-500000")
#   OPENAPI_HOST=https://test.company.openapi.com -> free sandbox (dummy data, count=2)
# Verified 2026-08-16 against the sandbox: dryRun returns {count, cost}; invalid
# filter keys are rejected with error 308, so accepted keys are validated keys.
set -euo pipefail
: "${OPENAPI_TOKEN:?OPENAPI_TOKEN env var is required}"
ATECO="${1:?usage: openapi_impresa_count.sh <atecoCode> [province] [minEmployees] [maxEmployees]}"
# IT-search wants the bare ATECO digits. A dotted code ("62.01") is accepted and
# silently matches nothing ({"count":0,"success":true}) instead of erroring, so
# normalize before querying.
ATECO="${ATECO//./}"
BASE="${OPENAPI_HOST:-https://company.openapi.com}"

Q="atecoCode=${ATECO}"
[ -n "${2:-}" ] && Q="${Q}&province=${2}"
[ -n "${3:-}" ] && Q="${Q}&minEmployees=${3}"
[ -n "${4:-}" ] && Q="${Q}&maxEmployees=${4}"
if [ -n "${OPENAPI_TURNOVER:-}" ]; then
  Q="${Q}&minTurnover=${OPENAPI_TURNOVER%-*}&maxTurnover=${OPENAPI_TURNOVER#*-}"
fi

if [ -n "${OPENAPI_SAMPLE:-}" ]; then
  curl -sfS -H "Authorization: Bearer ${OPENAPI_TOKEN}" \
    "${BASE}/IT-search?${Q}&limit=${OPENAPI_SAMPLE}" |
  jq '{success, returned: (.data | length), sample: .data}'
else
  curl -sfS -H "Authorization: Bearer ${OPENAPI_TOKEN}" \
    "${BASE}/IT-search?${Q}&dryRun=1" |
  jq '{success, count, cost}'
fi

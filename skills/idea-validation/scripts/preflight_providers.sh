#!/usr/bin/env bash
# Provider preflight: verify each configured credential with its cheapest
# call BEFORE dispatching research waves. Unset vars are reported as
# "not configured" (the skill then degrades per tooling.md); set-but-broken
# vars are the failure this script exists to catch early.
# Costs: DataForSEO user_data is free; Openapi hits the free sandbox;
# Exa runs a 1-result search (fractions of a cent); Apify reads /users/me (free).
set -u
fail=0
say() { printf '%-12s %s\n' "$1" "$2"; }

if [ -n "${DATAFORSEO_LOGIN:-}" ] || [ -n "${DATAFORSEO_PASSWORD:-}" ]; then
  if [ -z "${DATAFORSEO_LOGIN:-}" ] || [ -z "${DATAFORSEO_PASSWORD:-}" ]; then
    say DataForSEO "BROKEN: one of DATAFORSEO_LOGIN/_PASSWORD is set, the other empty or unset"; fail=1
  else
    code=$(curl -s -u "${DATAFORSEO_LOGIN}:${DATAFORSEO_PASSWORD}" \
      https://api.dataforseo.com/v3/appendix/user_data | jq -r '.status_code // 0')
    if [ "$code" = "20000" ]; then say DataForSEO "ok (auth verified, free call)"
    else say DataForSEO "BROKEN: status $code (check the API password from app.dataforseo.com)"; fail=1; fi
  fi
else
  say DataForSEO "not configured (Italian keyword volume will be reported as unmeasured)"
fi

if [ -n "${EXA_API_KEY:-}" ]; then
  http=$(curl -s -o /dev/null -w '%{http_code}' -X POST https://api.exa.ai/search \
    -H "x-api-key: ${EXA_API_KEY}" -H "Content-Type: application/json" \
    -d '{"query":"preflight","numResults":1}')
  if [ "$http" = "200" ]; then say Exa "ok (auth verified)"
  else say Exa "BROKEN: HTTP $http"; fail=1; fi
else
  say Exa "not configured (web research falls back to harness search tools)"
fi

if [ -n "${OPENAPI_TOKEN:-}" ]; then
  http=$(curl -s -o /dev/null -w '%{http_code}' -H "Authorization: Bearer ${OPENAPI_TOKEN}" \
    "https://test.company.openapi.com/IT-search?atecoCode=62.01&dryRun=1")
  if [ "$http" = "200" ]; then say Openapi "ok (token accepted by the free sandbox; production scope not proven here)"
  else say Openapi "BROKEN: sandbox HTTP $http"; fail=1; fi
else
  say Openapi "not configured (ICP counts fall back to Eurostat aggregates)"
fi

if [ -n "${APIFY_TOKEN:-}" ]; then
  http=$(curl -s -o /dev/null -w '%{http_code}' \
    "https://api.apify.com/v2/users/me?token=${APIFY_TOKEN}")
  if [ "$http" = "200" ]; then say Apify "ok (auth verified, free call)"
  else say Apify "BROKEN: HTTP $http"; fail=1; fi
else
  say Apify "not configured (review/community scraping unavailable)"
fi

exit $fail

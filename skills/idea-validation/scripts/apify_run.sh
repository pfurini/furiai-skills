#!/usr/bin/env bash
# Generic Apify actor runner: one wrapper covers every reviews/jobs/groups actor.
# Requires APIFY_TOKEN. Reads the actor input JSON from a file argument or stdin.
#
# Usage: apify_run.sh <owner~actor-name> [input.json]
#   e.g. apify_run.sh mfrostbutter~linkedin-jobs-scraper jobs-input.json
#   Tip: GET https://api.apify.com/v2/acts/{owner~actor} is public — read the
#   actor's current input schema before calling it.
# Output: the run's dataset items (JSON).
set -euo pipefail
: "${APIFY_TOKEN:?APIFY_TOKEN env var is required}"
ACTOR="${1:?usage: apify_run.sh <owner~actor-name> [input.json]}"
INPUT="${2:-/dev/stdin}"
curl -sfS -X POST "https://api.apify.com/v2/acts/${ACTOR}/run-sync-get-dataset-items?token=${APIFY_TOKEN}" \
  -H "Content-Type: application/json" \
  --data-binary "@${INPUT}"

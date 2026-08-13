#!/usr/bin/env bash
# Italian public-contract open data (ANAC CKAN). No API key.
# The WAF returns an HTTP-200 block page to curl's default User-Agent, so this
# script sets a browser UA and asserts the CKAN "success" flag — never trust
# the status code alone with this host.
#
# Usage: anac_dataset.sh list                 -> dataset ids
#        anac_dataset.sh <dataset-id>         -> resource list (name, format, url)
set -euo pipefail
ID="${1:?usage: anac_dataset.sh <dataset-id|list>}"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
BASE="https://dati.anticorruzione.it/opendata/api/3/action"
if [ "$ID" = "list" ]; then
  BODY="$(curl -sfS -A "$UA" "$BASE/package_list")"
  echo "$BODY" | jq -e '.success == true' > /dev/null || { echo "ANAC WAF block page received (success flag missing)" >&2; exit 1; }
  echo "$BODY" | jq -r '.result[]'
else
  BODY="$(curl -sfS -A "$UA" "$BASE/package_show?id=${ID}")"
  echo "$BODY" | jq -e '.success == true' > /dev/null || { echo "ANAC WAF block page received (success flag missing)" >&2; exit 1; }
  echo "$BODY" | jq -r '.result.resources[] | [.name, .format, .url] | @tsv'
fi

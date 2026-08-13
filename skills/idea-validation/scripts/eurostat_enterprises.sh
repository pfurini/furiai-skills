#!/usr/bin/env bash
# Italian enterprise counts by size class, from the Eurostat dissemination API.
# No API key. Dataset: sbs_sc_ovw (dimensions: freq, indic_sbs, nace_r2, size_emp, geo, time).
#
# Usage: eurostat_enterprises.sh <NACE_R2 code, e.g. J62 or M69> [year=2023] [geo=IT] [indic=ENT_NR]
#   indic: ENT_NR = enterprise count, EMP_NR = persons employed
# Output: TSV size_class<TAB>value
set -euo pipefail
NACE="${1:?usage: eurostat_enterprises.sh <NACE_R2> [year] [geo] [indic]}"
YEAR="${2:-2023}"; GEO="${3:-IT}"; INDIC="${4:-ENT_NR}"
URL="https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sbs_sc_ovw?format=JSON&geo=${GEO}&nace_r2=${NACE}&indic_sbs=${INDIC}&time=${YEAR}"
BODY="$(curl -sfS "$URL")"
# JSON-stat: with all other dimensions pinned, the flat value index follows size_emp's category index.
echo "$BODY" | jq -r '
  .dimension.size_emp.category as $c
  | ($c.index | to_entries | sort_by(.value)) as $order
  | .value as $v
  | $order[] | [$c.label[.key] // .key, ($v[(.value|tostring)] // "n/a")] | @tsv'

#!/bin/bash
# Nightly: pull warehouse CSVs and rebuild the local snapshot.
# (The scp step is wired to the warehouse box; run manually only if the
# nightly job failed.)
set -euo pipefail
cd "$(dirname "$0")/.."
python3 db/build_db.py
echo "snapshot rebuilt: db/analytics.sqlite"

#!/bin/bash
# Preflight for any parallel batch: the scrubbed profile's OAuth token must be
# valid well past the batch window. Per-run profile copies CANNOT refresh:
# the refresh token is single-use, so N concurrent runs near expiry race on
# it and N-1 fail with "OAuth session expired and could not be refreshed"
# (observed live at M0: 30/30 gate runs died this way with ~4 min left on the
# token). Re-export from the Keychain after the main session rotates it.
#   $1 = profile dir, $2 = required validity in minutes (default 120)
set -euo pipefail
PROFILE="$1"; NEED_MIN="${2:-120}"
LEFT=$(python3 - "$PROFILE" <<'EOF'
import json, sys, time, pathlib
d = json.loads((pathlib.Path(sys.argv[1]) / ".credentials.json").read_text())
oauth = d.get("claudeAiOauth", d)
print(int((oauth.get("expiresAt", 0) / 1000 - time.time()) / 60))
EOF
)
echo "token validity: ${LEFT} min (need ${NEED_MIN})"
[ "$LEFT" -ge "$NEED_MIN" ] || { echo "FAIL: re-export credentials before batching"; exit 1; }

#!/usr/bin/env python3
"""Search TMview (tmdn.org) for word-mark collisions. Stdlib only.

Usage:
    python3 check_trademarks.py NAME [NAME ...] [--offices IT,EM,WO] [--classes 9,35,41,42]

For each name prints EXACT hits (same word, case-insensitive) and NEAR hits
(name appears inside a longer mark), with office, status, and Nice classes.
An EXACT registered hit in an overlapping Nice class kills the name; anything
else is a flag to evaluate, not an automatic kill.

Caveats the caller must keep in mind (also printed in the output):
- This is an exact/substring word search, NOT the phonetic/conceptual similarity
  search a trademark consultant performs before filing.
- The endpoint is TMview's internal JSON API: free, no auth, but undocumented
  and may change. The official alternative is the EUIPO API Portal
  (dev.euipo.europa.eu, OAuth account, EU marks only, no national UIBM marks).

Office codes: IT = Italy (UIBM), EM = EUIPO (EU marks), WO = WIPO international.
Exit code is always 0; this is a reporting tool, not a gate.
"""
import argparse
import json
import sys
import time
import urllib.request

ENDPOINT = "https://www.tmdn.org/tmview/api/search/results"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"


def tmview_search(name, offices, page_size=30):
    body = json.dumps({
        "page": "1",
        "pageSize": str(page_size),
        "criteria": "C",
        "basicSearch": name,
        "fOffices": offices,
        "fTMStatus": ["Registered", "Filed"],
    }).encode()
    req = urllib.request.Request(ENDPOINT, data=body, headers={
        "Content-Type": "application/json", "User-Agent": UA})
    last_err = None
    for attempt in range(4):  # endpoint is flaky; 4 tries with backoff was reliable
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.loads(r.read())
        except Exception as e:
            last_err = e
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"TMview unreachable after retries: {last_err}")


def classes_of(mark):
    nc = mark.get("niceClass") or mark.get("niceClasses") or []
    if isinstance(nc, str):
        nc = [nc]
    return ",".join(str(c) for c in nc) or "?"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("names", nargs="+")
    ap.add_argument("--offices", default="IT,EM,WO",
                    help="comma-separated TMview office codes (default: IT,EM,WO)")
    ap.add_argument("--classes", default="",
                    help="Nice classes relevant to this brand, e.g. 9,35,41,42; "
                         "hits in these classes are marked OVERLAP")
    args = ap.parse_args()
    offices = [o.strip().upper() for o in args.offices.split(",") if o.strip()]
    relevant = {c.strip() for c in args.classes.split(",") if c.strip()}

    for name in args.names:
        name = name.strip()
        try:
            data = tmview_search(name, offices)
        except RuntimeError as e:
            print(f"== {name}: UNKNOWN ({e}); retry later or search tmview.org manually")
            continue
        total = data.get("totalResults", 0)
        marks = data.get("tradeMarks", [])
        exact, near = [], []
        for m in marks:
            tm_name = (m.get("tmName") or "").strip()
            (exact if tm_name.lower() == name.lower() else near).append(m)
        print(f"== {name}: {len(exact)} EXACT, {total - len(exact)} NEAR "
              f"(offices {','.join(offices)}; live marks only — results are "
              f"pre-filtered to Registered/Filed, expired marks never appear)")
        for m in exact:
            cls = classes_of(m)
            overlap = " OVERLAP" if relevant and relevant & set(cls.split(",")) else ""
            print(f"   EXACT  {m.get('tmName')}  office={m.get('tmOffice')} "
                  f"classes={cls}{overlap}")
        for m in near[:8]:
            print(f"   NEAR   {m.get('tmName')}  office={m.get('tmOffice')} "
                  f"classes={classes_of(m)}")
        if total - len(exact) > 8:
            print(f"   ... {total - len(exact) - 8} more NEAR hits not shown "
                  f"(inspect on tmview.org if the name survives)")

    print("\nCaveat: exact/substring word search only, not phonetic/conceptual "
          "similarity. Run variants (double consonants, vowel swaps, spacing) "
          "as extra names, and get a consultant similarity search before filing. "
          "TMview throttles per IP under heavy use (connection resets): if UNKNOWN "
          "persists across names, stop, record PENDING, and re-run after a cooldown "
          "instead of hammering it.",
          file=sys.stderr)


if __name__ == "__main__":
    main()

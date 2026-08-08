#!/usr/bin/env python3
"""Check social handle availability for candidate brand names. Stdlib only.

Usage:
    python3 check_handles.py NAME [NAME ...]

Deterministic platforms (verified discriminators):
    YouTube  — https://www.youtube.com/@NAME     404 = free, 200 = taken
    GitHub   — https://github.com/NAME           404 = free, 200 = taken

Non-deterministic platforms (login walls / JS walls return 200 for everything):
    Instagram, TikTok, X, LinkedIn, Facebook — printed as VERIFY MANUALLY with
    the URL to open. A tool that reports "free" without a definitive negative
    signal produces false positives (Sherlock did exactly that in testing), so
    this script only ever claims FREE on a hard 404.

Exit code is always 0; this is a reporting tool, not a gate.
"""
import argparse
import sys
import urllib.error
import urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

DETERMINISTIC = [
    ("YouTube", "https://www.youtube.com/@{}"),
    ("GitHub", "https://github.com/{}"),
]
MANUAL = [
    ("Instagram", "https://www.instagram.com/{}/"),
    ("TikTok", "https://www.tiktok.com/@{}"),
    ("X", "https://x.com/{}"),
    ("LinkedIn", "https://www.linkedin.com/company/{}"),
    ("Facebook", "https://www.facebook.com/{}"),
]


def http_status(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        return f"error: {e}"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("names", nargs="+")
    args = ap.parse_args()

    for name in args.names:
        name = name.lower().strip()
        print(f"== {name}")
        for platform, tpl in DETERMINISTIC:
            st = http_status(tpl.format(name))
            if st == 404:
                verdict = "FREE"
            elif st == 200:
                verdict = "TAKEN"
            else:
                verdict = f"UNKNOWN (HTTP {st}); verify manually"
            print(f"   {platform:<10} {verdict}")
        for platform, tpl in MANUAL:
            print(f"   {platform:<10} VERIFY MANUALLY -> {tpl.format(name)}")

    print("\nOnly a hard 404 counts as FREE. Open the VERIFY MANUALLY links in a "
          "browser; an agent-driven browser also works for Instagram/TikTok, but "
          "expect bot walls.", file=sys.stderr)


if __name__ == "__main__":
    main()

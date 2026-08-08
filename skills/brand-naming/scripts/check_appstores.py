#!/usr/bin/env python3
"""Check app stores and package registries for candidate brand names. Stdlib only.

Usage:
    python3 check_appstores.py NAME [NAME ...] [--country it]

Checks (all free, no auth):
    Apple App Store — iTunes Search API, exact match on app name
    npm             — registry.npmjs.org/NAME   404 = free
    PyPI            — pypi.org/pypi/NAME/json   404 = free

Google Play has no public search API; the script prints the search URL to
check manually. Run this only when the brand will ship an app or a developer
tool; for other brands these dimensions are noise.

Exit code is always 0; this is a reporting tool, not a gate.
"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:
        return f"error: {e}", b""


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("names", nargs="+")
    ap.add_argument("--country", default="it", help="App Store country code (default: it)")
    args = ap.parse_args()

    for name in args.names:
        name = name.lower().strip()
        print(f"== {name}")

        q = urllib.parse.urlencode({"term": name, "entity": "software",
                                    "country": args.country, "limit": 25})
        st, body = get(f"https://itunes.apple.com/search?{q}")
        if st == 200:
            results = json.loads(body).get("results", [])
            # "WhatsApp Messenger" must match "whatsapp": compare on words, not
            # whole-string equality.
            def hits(r):
                fields = (r.get("trackName", "") + " " + r.get("sellerName", "")).lower()
                return name in fields.split() or fields.startswith(name)
            exact = [r for r in results if hits(r)]
            if exact:
                apps = "; ".join(f"{r['trackName']} ({r.get('sellerName')})" for r in exact[:3])
                print(f"   App Store  TAKEN (name match): {apps}")
            elif results:
                print(f"   App Store  NO EXACT MATCH ({len(results)} partial hits; "
                      f"inspect if the brand is app-centric)")
            else:
                print("   App Store  FREE (0 results)")
        else:
            print(f"   App Store  UNKNOWN (HTTP {st}); verify manually")

        for label, url in [("npm", f"https://registry.npmjs.org/{name}"),
                           ("PyPI", f"https://pypi.org/pypi/{name}/json")]:
            st, _ = get(url)
            verdict = {404: "FREE", 200: "TAKEN"}.get(st, f"UNKNOWN (HTTP {st})")
            print(f"   {label:<10} {verdict}")

        play = "https://play.google.com/store/search?c=apps&q=" + urllib.parse.quote(name)
        print(f"   Play Store VERIFY MANUALLY -> {play}")

    print("\nApp Store match is by exact app/seller name in one storefront country; "
          "a global brand should re-run with --country us.", file=sys.stderr)


if __name__ == "__main__":
    main()

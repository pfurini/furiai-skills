#!/usr/bin/env python3
"""Check domain availability for candidate brand names. Stdlib only.

Usage:
    python3 check_domains.py NAME [NAME ...] [--tlds it,com,eu]

Prints one line per domain: AVAILABLE / REGISTERED / UNKNOWN (reason).
UNKNOWN means the check could not be done deterministically: verify manually.
Exit code is always 0; this is a reporting tool, not a gate.
"""
import argparse
import json
import re
import socket
import sys
import time
import urllib.error
import urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

# RDAP bases for TLDs whose registries run RDAP (404 = available, 200 = registered).
RDAP_BASES = {
    "com": "https://rdap.verisign.com/com/v1/domain/",
    "net": "https://rdap.verisign.com/net/v1/domain/",
    "org": "https://rdap.publicinterestregistry.org/rdap/domain/",
    "dev": "https://pubapi.registry.google/rdap/domain/",
    "app": "https://pubapi.registry.google/rdap/domain/",
    "page": "https://pubapi.registry.google/rdap/domain/",
}

# Port-43 whois for TLDs without RDAP. Pattern marks an AVAILABLE domain.
# .it and .eu were verified live; NIC.it throttles, hence the delay below.
WHOIS_SERVERS = {
    "it": ("whois.nic.it", re.compile(r"Status:\s*AVAILABLE", re.I)),
    "eu": ("whois.eu", re.compile(r"Status:\s*AVAILABLE", re.I)),
}

# NIC.it drops rapid-fire queries; 1.5s between whois calls was reliable in testing.
WHOIS_DELAY_S = 1.5
IANA_BOOTSTRAP = "https://data.iana.org/rdap/dns.json"


def http_status(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/rdap+json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        return f"error: {e}"


def whois_query(server, domain):
    s = socket.create_connection((server, 43), timeout=15)
    try:
        s.sendall((domain + "\r\n").encode())
        data = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk
    finally:
        s.close()
    return data.decode(errors="replace")


def rdap_base_from_iana(tld, cache={}):
    """Look up an RDAP base for an uncommon TLD from the IANA bootstrap file."""
    if not cache:
        try:
            req = urllib.request.Request(IANA_BOOTSTRAP, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=20) as r:
                boot = json.load(r)
            for tlds, urls in boot.get("services", []):
                for t in tlds:
                    cache[t] = urls[0].rstrip("/") + "/domain/"
        except Exception:
            cache["__failed__"] = True
    return cache.get(tld)


def check_domain(name, tld):
    domain = f"{name}.{tld}"
    base = RDAP_BASES.get(tld)
    if base is None and tld not in WHOIS_SERVERS:
        base = rdap_base_from_iana(tld)
    if base:
        for attempt in range(3):
            st = http_status(base + domain)
            if st == 404:
                return domain, "AVAILABLE", ""
            if st == 200:
                return domain, "REGISTERED", ""
            time.sleep(2)  # transient RDAP errors clear quickly; 429 needs the pause
        return domain, "UNKNOWN", f"RDAP kept failing (last: {st}); check manually"
    if tld in WHOIS_SERVERS:
        server, avail_re = WHOIS_SERVERS[tld]
        try:
            out = whois_query(server, domain)
        except Exception as e:
            return domain, "UNKNOWN", f"whois error: {e}"
        if avail_re.search(out):
            return domain, "AVAILABLE", ""
        if re.search(r"Status:", out, re.I) or "Registrant" in out:
            return domain, "REGISTERED", ""
        return domain, "UNKNOWN", "unrecognized whois response; check manually"
    return domain, "UNKNOWN", f"no RDAP or whois strategy for .{tld}; check manually"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("names", nargs="+", help="candidate names, without TLD")
    ap.add_argument("--tlds", default="it,com", help="comma-separated TLDs (default: it,com)")
    args = ap.parse_args()
    tlds = [t.strip().lstrip(".").lower() for t in args.tlds.split(",") if t.strip()]

    whois_used = False
    for name in args.names:
        name = name.lower().strip()
        for tld in tlds:
            if tld in WHOIS_SERVERS and whois_used:
                time.sleep(WHOIS_DELAY_S)
            domain, verdict, note = check_domain(name, tld)
            if tld in WHOIS_SERVERS:
                whois_used = True
            line = f"{domain}\t{verdict}"
            if note:
                line += f"\t({note})"
            print(line)
    print("\nLegend: AVAILABLE = registry says free. REGISTERED = taken. "
          "UNKNOWN = could not determine, verify manually.", file=sys.stderr)


if __name__ == "__main__":
    main()

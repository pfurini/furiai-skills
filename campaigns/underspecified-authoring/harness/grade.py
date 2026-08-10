#!/usr/bin/env python3
"""Pre-registered prompt-contract grader for the 4-way producer pilot.

Assertions (from the user's stated conventions, valid for every artifact):
  A1 header: a heading line contains both 3.1.0 and 2026-08-06
  A2 breaking: first section is breaking-titled, carries a warning signal
     (unicode warning sign or the word 'warning'), contains #495; and #495
     appears exactly once in the whole output
  A3 sections: no section headings outside {breaking-ish, Added, Changed, Fixed}
  A4 entries: every bullet line inside sections ends with (#NNN)
  A5 coverage: each of the six PR numbers appears exactly once
"""
import json
import re
import sys
from pathlib import Path

CONS = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "cons"
PRS = ["495", "498", "499", "501", "502", "503"]
ALLOWED = re.compile(r"^(.*breaking.*|added|changed|fixed)$", re.I)
WARN = re.compile(r"(⚠|warning)", re.I)


def extract(text: str) -> str:
    """Slice from the last version-header line to the end, dropping fence markers.

    Rationale (from manual review of iteration 1 of this grader): fenced-block
    extraction loses trailing notes ("Excluded PRs"), and whole-text grading
    double-counts PRs mentioned in a reasoning preamble. The changelog proper
    always starts at the version header; nothing before it is output.
    """
    lines = text.splitlines()
    idxs = [i for i, ln in enumerate(lines) if re.match(r"^\s*#{1,6}\s*\[?v?3\.1\.0", ln)]
    body = lines[idxs[-1]:] if idxs else lines
    return "\n".join(ln for ln in body if not ln.strip().startswith("```"))


def headings(body: str):
    """Markdown headings only. Bold lines are commentary labels in every
    observed output (Verification:, Excluded PRs, Reported for review), not
    changelog sections — counting them as sections misgrades A3."""
    out = []
    for line in body.splitlines():
        m = re.match(r"^#{2,6}\s+(.*\S)\s*$", line)
        if m:
            out.append(m.group(1))
    return out


def grade(text: str) -> dict:
    body = extract(text)
    lines = body.splitlines()
    heads = headings(body)
    # A1
    a1 = any(re.match(r"^#{1,6}\s", ln) and "3.1.0" in ln and "2026-08-06" in ln for ln in lines)
    # section headings excluding the version header line
    sec = [h for h in heads if "3.1.0" not in h]
    # A2
    first_is_breaking = bool(sec) and "breaking" in sec[0].lower()
    breaking_head_line = next((ln for ln in lines if re.match(r"^#{2,6}\s", ln) and "breaking" in ln.lower()), "")
    # warning signal on the breaking heading or within its section entries
    warn_ok = bool(WARN.search(breaking_head_line))
    if not warn_ok and first_is_breaking:
        in_b = False
        for ln in lines:
            if re.match(r"^#{2,6}\s", ln):
                in_b = "breaking" in ln.lower()
                continue
            if in_b and WARN.search(ln):
                warn_ok = True
                break
    c495 = len(re.findall(r"#495\b", body))
    in_breaking_495 = False
    in_b = False
    for ln in lines:
        if re.match(r"^#{2,6}\s", ln):
            in_b = "breaking" in ln.lower()
            continue
        if in_b and "#495" in ln:
            in_breaking_495 = True
    a2 = first_is_breaking and warn_ok and in_breaking_495 and c495 == 1
    # A3
    a3 = bool(sec) and all(ALLOWED.match(s.strip().rstrip(":")) or "not included" in s.lower() for s in sec)
    # A4: bullet lines under recognized sections end with (#NNN)
    a4 = True
    in_sec = False
    for ln in lines:
        m = re.match(r"^#{2,6}\s+(.*\S)\s*$", ln)
        if m:
            in_sec = bool(ALLOWED.match(m.group(1).strip().rstrip(":")))
            continue
        # Any plain paragraph line (non-blank, non-bullet, non-heading) ends
        # the changelog-section scope: real sections contain only bullets, so
        # prose marks the start of commentary, whose bullets are not entries.
        if ln.strip() and not re.match(r"^\s*[-*]\s+\S", ln):
            in_sec = False
            continue
        if in_sec and re.match(r"^\s*[-*]\s+\S", ln):
            if not re.search(r"\(#\d+\)\s*$", ln.rstrip()):
                a4 = False
    # A5
    counts = {p: len(re.findall(rf"#{p}\b", body)) for p in PRS}
    a5 = all(v == 1 for v in counts.values())
    return {"A1": a1, "A2": a2, "A3": a3, "A4": a4, "A5": a5, "counts": counts}


def main():
    rows = []
    for d in sorted(CONS.iterdir()):
        f = d / "out.md"
        if not f.exists():
            continue
        name = d.name
        g = grade(f.read_text())
        g["run"] = name
        if name.startswith("base"):
            g["treatment"], g["rep"] = "BASE", "-"
        else:
            g["treatment"], g["rep"] = name[:2], name[2:4]
        g["passed"] = sum(g[k] for k in ("A1", "A2", "A3", "A4", "A5"))
        rows.append(g)

    print(f"{'run':<12} A1 A2 A3 A4 A5  pass")
    for g in rows:
        marks = "  ".join("Y" if g[k] else "." for k in ("A1", "A2", "A3", "A4", "A5"))
        print(f"{g['run']:<12} {marks}  {g['passed']}/5")

    print("\nBy treatment (mean assertions passed /5, n runs):")
    from collections import defaultdict
    agg = defaultdict(list)
    for g in rows:
        agg[g["treatment"]].append(g["passed"])
    for t in sorted(agg):
        v = agg[t]
        print(f"  {t}: {sum(v)/len(v):.2f}/5  (n={len(v)}, min={min(v)}, max={max(v)})")

    print("\nBy artifact:")
    agg2 = defaultdict(list)
    for g in rows:
        if g["treatment"] != "BASE":
            agg2[g["treatment"] + g["rep"]].append(g["passed"])
    for a in sorted(agg2):
        v = agg2[a]
        print(f"  {a}: {sum(v)/len(v):.2f}/5 over {len(v)} reps")

    (CONS.parent / "grading-results.json").write_text(json.dumps(rows, indent=2))
    print("\nSaved grading-results.json")


if __name__ == "__main__":
    main()

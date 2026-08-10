#!/usr/bin/env python3
"""Deterministic consumer grader for the underspecified-authoring campaign.

Usage: grade_consumers.py <runs-dir> [--gate]

Each run dir is named <QID>-r<rep>[...] and contains out.md. Grades the final
ANSWER line against key/expected-answers.json (exact match within the
per-question tolerance; QB2 by account-name containment; QS2 requires all
eight table names). Per doctrine, every flagged (failing) run must be
manually read before the numbers are believed; this script only proposes.

--gate applies the question-gate rule: a keyed question answered correctly in
>= 2 of 3 no-artifact reps is broken and must be revised before wave 1.
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

CAMPAIGN = Path(__file__).resolve().parent.parent
KEY = json.loads((CAMPAIGN / "key" / "expected-answers.json").read_text())
KEYED = ["QB1", "QB2", "QB3", "QB4", "QC1", "QC2", "QC3", "QC4"]


def parse_answer(text):
    hits = re.findall(r"^\s*ANSWER:\s*(.+?)\s*$", text, re.MULTILINE)
    return hits[-1] if hits else None


def to_number(s):
    m = re.search(r"-?[\d,]+(?:\.\d+)?", s.replace("$", ""))
    if not m:
        return None
    try:
        return float(m.group(0).replace(",", ""))
    except ValueError:
        return None


def is_correct(qid, raw, full_text):
    spec = KEY[qid]
    if qid == "QS2":
        # answers often span lines below the ANSWER: marker — grade the full
        # text (grader iteration 2; the line-only read misgraded list output)
        return all(t in full_text.lower() for t in spec["correct"])
    if raw is None:
        return False
    if qid == "QB2":
        return spec["correct"].lower() in raw.lower()
    num = to_number(raw)
    if num is None:
        return False
    tol = spec["tolerance"] or 0
    return abs(num - spec["correct"]) <= tol


def variant_hit(qid, raw):
    if raw is None or qid not in KEY:
        return ""
    num = to_number(raw)
    for name, v in KEY[qid].get("variants", {}).items():
        if isinstance(v, str):
            if v.lower() in raw.lower():
                return name
        elif num is not None and abs(num - v) <= (KEY[qid]["tolerance"] or 0.001):
            return name
    return ""


def main():
    runs_dir = Path(sys.argv[1])
    gate_mode = "--gate" in sys.argv
    rows = []
    for d in sorted(runs_dir.iterdir()):
        f = d / "out.md"
        if not d.is_dir() or not f.exists():
            continue
        m = re.match(r"(Q[BCS]\d)-r(\d+)", d.name)
        if not m:
            continue
        qid, rep = m.group(1), m.group(2)
        text = f.read_text()
        raw = parse_answer(text)
        ok = is_correct(qid, raw, text)
        rows.append({"run": d.name, "qid": qid, "rep": rep, "answer": raw,
                     "correct": ok, "matched_variant": "" if ok else variant_hit(qid, raw)})

    print(f"{'run':<14} {'ok':<3} {'answer':<28} variant-hit")
    for r in rows:
        print(f"{r['run']:<14} {'Y' if r['correct'] else '.':<3} "
              f"{str(r['answer'])[:28]:<28} {r['matched_variant']}")

    by_q = defaultdict(list)
    for r in rows:
        by_q[r["qid"]].append(r["correct"])
    print("\nPer question:")
    for qid in sorted(by_q):
        v = by_q[qid]
        print(f"  {qid}: {sum(v)}/{len(v)} correct")

    if gate_mode:
        print("\nQuestion gate (broken = keyed question correct in >=2 baseline reps):")
        broken = [qid for qid in KEYED if sum(by_q.get(qid, [])) >= 2]
        for qid in KEYED:
            v = by_q.get(qid, [])
            status = "BROKEN" if qid in broken else "ok"
            print(f"  {qid}: {sum(v)}/{len(v)} -> {status}")
        sane = all(sum(by_q.get(qid, [])) >= 2 for qid in ("QS1", "QS2"))
        print(f"  sanity questions (expect mostly correct): "
              f"{'ok' if sane else 'ATTENTION - consumers may not drive sqlite at all'}")

    out = runs_dir / "grading-results.json"
    out.write_text(json.dumps(rows, indent=2))
    print(f"\nSaved {out}\nManually read every flagged run before believing this.")


if __name__ == "__main__":
    main()

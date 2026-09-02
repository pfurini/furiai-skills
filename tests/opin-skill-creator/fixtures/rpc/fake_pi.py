#!/usr/bin/env python3
"""Deterministic RPC peer used only by OSC-10 protocol tests."""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

FIXTURE_ROOT = Path(__file__).resolve().parent

if sys.argv[1:] == ["--version"]:
    print("0.84.4")
    raise SystemExit(0)

args_output = os.environ.get("FAKE_PI_ARGS")
if args_output:
    Path(args_output).write_text(json.dumps(sys.argv[1:], ensure_ascii=False) + "\n", encoding="utf-8")

scenario = os.environ.get("FAKE_PI_SCENARIO", "success")
requests: list[str] = []
for line in sys.stdin:
    requests.append(line)
    record = json.loads(line)
    if record.get("type") != "prompt":
        continue
    input_output = os.environ.get("FAKE_PI_INPUT")
    if input_output:
        Path(input_output).write_text("".join(requests), encoding="utf-8", newline="\n")
    if scenario == "timeout":
        time.sleep(60)
    elif scenario == "process-error":
        sys.stderr.write("fixture process error " + "x" * 4000 + "\n")
        raise SystemExit(7)
    else:
        sys.stdout.buffer.write((FIXTURE_ROOT / f"{scenario}.jsonl").read_bytes())
        sys.stdout.buffer.flush()
        sys.stdin.read()
    break

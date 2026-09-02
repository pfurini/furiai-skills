---
name: valid-current-fields
description: Current Pi fields and unknown JSON-safe metadata.
license: MIT
compatibility: Python 3.10+
metadata: {owner: core}
when_to_use: Use for validator parity.
argument-hint: "[path]"
arguments: [path, mode]
disable-model-invocation: "YeS"
user-invocable: "OFF"
allowed-tools: [read, bash]
disallowed-tools: [write]
model: inherit
effort: high
context: FoRk
agent: general-purpose
background: 0
paths: ["src/**"]
shell: bash
hooks: {PreToolUse: ignored}
unknown-scalar: value
unknown-list: [one, two]
unknown-map: {nested: true, count: 2}
---

# Valid current fields

---
name: unsafe-json-values
description: Pi drops unsafe unknown YAML values while loading this skill.
cycle: &loop
  self: *loop
nan: .nan
positive: .inf
negative: -.inf
set: !!set
  one:
  two:
binary: !!binary SGVsbG8=
---

# Unsafe JSON values

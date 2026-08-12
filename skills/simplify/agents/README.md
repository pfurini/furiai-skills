# Simplify agents

Four pi-subagents custom agent types used by the `simplify` skill (one per
review angle: reuse, simplification, efficiency, altitude). They are read-only
reviewers: each receives the diff, returns findings, and the orchestrator
applies the fixes.

## Customization

`model:` and `thinking:` are intentionally unset, so the agents inherit the
orchestrator's model (same behavior as the original). Pin them per agent in
the frontmatter to run reviewers on a cheaper or faster model — frontmatter is
authoritative and cannot be overridden by the caller. Fuzzy names work
(`"haiku"`, `"sonnet"`).

`prompt_mode: replace` means each agent's body is its full system prompt; the
project's AGENTS.md is not inherited, matching the self-contained angle
definitions spirit.

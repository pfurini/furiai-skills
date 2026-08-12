# Super-code-review agents

Thirteen pi-subagents custom agent types used by the `super-code-review` skill
(one per review lens; `subagent_type` = filename without `.md`). They are
read-only reviewers: each receives the review scope, returns findings, and the
orchestrator synthesizes the verdict.

The same files double as the lens definitions for inline mode: when the review
runs without fan-out, the orchestrator reads the body below the frontmatter and
applies it in its own context.

## Customization

`model:` and `thinking:` are tiered by what a missed finding costs on each
lens — frontmatter is authoritative and cannot be overridden by the caller;
fuzzy model names work (`"haiku"`, `"sonnet"`):

- **Inherit** (both unset) — `scr-correctness`, `scr-security`; and
  `scr-requirements` inherits the model with `thinking: medium`. The critical
  lenses always ride the orchestrator's model, so they scale with the session
  instead of freezing a default into the skill.
- **`openai-codex/gpt-5.6-terra`** — judgment-shaped structural lenses:
  `scr-architecture`, `scr-evolvability`, `scr-type-design`,
  `scr-test-coverage` (`thinking: medium`); `scr-performance`,
  `scr-guidelines` (`thinking: low`).
- **`openai-codex/gpt-5.6-luna`** — checklist-shaped and advisory lenses:
  `scr-error-handling`, `scr-simplification`, `scr-comments`,
  `scr-docs-impact` (`thinking: low`).

An unresolvable pin (provider auth expired, model renamed) silently falls back
to inheriting the orchestrator's model — check `/agents → Agent types` after
changing pins.

`prompt_mode: replace` means each agent's body is its full system prompt; the
project's AGENTS.md is not inherited, matching the self-contained lens
definitions.

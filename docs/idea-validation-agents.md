# Idea-validation agents

> Maintainer notes. The agent files live at `skills/idea-validation/agents/`; the frontmatter there is authoritative — keep this document in sync when changing model or thinking pins.

Eleven pi-subagents custom agent types used by the `idea-validation` skill
(one per analysis dimension; `subagent_type` = filename without `.md`). Each
receives an idea slug or topic plus the store paths to read, writes exactly
its designated artifact into `.idea-validation/`, and returns a short
summary; the orchestrator reads the artifacts and synthesizes the verdict.

The same files double as the dimension definitions for inline mode: when the
workflow runs without fan-out, the orchestrator reads the body below the
frontmatter and applies it in its own context.

## Customization

`model:` and `thinking:` are tiered by what a wrong number costs on each
dimension — frontmatter is authoritative and cannot be overridden by the
caller; fuzzy model names work (`"haiku"`, `"sonnet"`):

- **Inherit** (both unset) — `iv-trend-researcher`, `iv-competitor-mapper`.
  These build the evidence layer that every downstream number calibrates on;
  they always ride the orchestrator's model, so they scale with the session
  instead of freezing a default into the skill.
- **`openai-codex/gpt-5.6-terra`** — judgment-shaped analysis:
  `iv-idea-mapper`, `iv-market-sizer`, `iv-weakness`, `iv-pivot-engine`
  (`thinking: medium`); `iv-pricing-wtp`, `iv-distribution`
  (`thinking: low`).
- **`openai-codex/gpt-5.6-luna`** — checklist-and-arithmetic-shaped
  dimensions: `iv-desire-evaluator`, `iv-retention`, `iv-cac-modeler`
  (`thinking: low`).

An unresolvable pin (provider auth expired, model renamed) silently falls
back to inheriting the orchestrator's model — check `/agents → Agent types`
after changing pins.

`tools:` is left unset on every agent: unlike a read-only reviewer, each of
these agents must write its artifact into `.idea-validation/`, and the
research agents (`iv-trend-researcher`, `iv-competitor-mapper`,
`iv-idea-mapper`) also need whatever web search/fetch tools the harness
provides. Write discipline (one designated artifact, nothing else) is
enforced in each agent's Rules section instead.

`prompt_mode: replace` means each agent's body is its full system prompt;
the project's AGENTS.md is not inherited, matching the self-contained
dimension definitions. Because of this, the orchestrator's dispatch prompt
must carry everything contextual: the current date, the project root, the
slug/niche, and the store paths.

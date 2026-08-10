# Harness reference implementations

Working copies of the runner scripts and grader used by the pi-skill-creator
eval campaigns (producer pilots, floor-doctrine A/B, masking check), saved
here so the underspecified-authoring campaign does not recreate them from
scratch. They are reference implementations, not turnkey tools: absolute
paths (the `SC` variable, prompt file locations, model ids) are
session-specific and must be adapted. Environment knobs already supported:
`CONS_BASE` (output root), `PROMPT_FILE` (consumer prompt), `CONSUMER_MODEL`.
The clean-slate profile recipe they depend on is documented in
`skills/pi-skill-creator/references/benchmarking.md`.

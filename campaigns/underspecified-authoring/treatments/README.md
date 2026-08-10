# Treatment copies

- **T-PI**: `skills/pi-skill-creator` at the campaign-start commit (recorded in
  the wave-1 run metadata; do not edit the live skill between waves without
  re-freezing).
- **T-WIRED**: `pi-skill-creator-wired/` — a copy of the above plus the two
  wiring steps under test, exactly as PLAN.md section 1 specifies: new Step 3
  ("Write the evals, spec-blind", pre-draft, intent-only input) and a red-team
  dispatch inside the renumbered Step 6 (draft + intent in, traps out, key to
  the workspace). All other files are identical to the base skill.

Staging note (applies to both treatment arms): the producer-visible copy is
staged with `README.md` stripped. It is distribution documentation, exempt
from runtime by the skill's own rule, and it names the underspecified-authoring
hypothesis this campaign measures — leaving it readable under `--add-dir`
would prime the treatment arms. Stripping it from both arms keeps exposure
symmetric and faithful to runtime reality.

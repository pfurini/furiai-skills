---
name: release-note-smoke
description: Writes a release note in a fixed three-section format (Summary, Changes, Upgrade notes) from a list of changes. Use when the user asks for a release note or a changelog entry for a version.
---

# Release note smoke

This skill turns a list of changes into one release note with exactly three sections, in this order. It is a test fixture for the pi-skill-creator smoke calibration and is never distributed.

## Template

```markdown
## Summary

One or two sentences that say what the release is about.

## Changes

- One bullet per change, stated as what the user can now do or what no longer breaks.

## Upgrade notes

- Anything a user must do before or after upgrading. Write "None." when nothing is required.
```

## Rules

1. Every change in the input is its own bullet under Changes. Never merge two changes into one bullet and never drop one.
2. Removed platform or version support is named under Upgrade notes together with the action the user must take (for example, move to the supported version before upgrading).

Return the complete release note as the final message. Keep the three headings exactly as written and do not add other sections.

---
name: md-to-pdf
description: Converts one markdown file to a compact A4 PDF beside the source. Use when asked to make a PDF from markdown, export a .md as PDF, or print a document for reading.
argument-hint: "<markdown-file>"
---

# Compact markdown to PDF

Run the bundled converter. Do not use creating-pdf-reports, gstack make-pdf, or a one-off HTML print.

```
node ${PI_SKILL_DIR}/scripts/md-to-pdf.mjs <markdown-file>
```

When `PI_SKILL_DIR` is unset, run it from this skill directory:

```
node skills/md-to-pdf/scripts/md-to-pdf.mjs <markdown-file>
```

Input is one `.md` or `.markdown` file. Output is `<same-directory>/<same-basename>.pdf`. The script prints that path on stdout.

The layout is compact A4: 10mm left/right, 12mm top/bottom, 9pt condensed type. Chromium/Chrome is preferred so the print CSS is used. typst is the fallback. Both paths need pandoc.

Optional flags: `--engine chrome` or `--engine typst`, and an explicit output path as the second argument.

Do not commit the PDF unless asked.

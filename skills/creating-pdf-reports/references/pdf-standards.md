# PDF standards and validation

## Choosing a conformance target

- **Default (no stated requirement):** plain `typst compile report.typ`.
  Typst emits PDF 1.7 with tagged structure by default, which is what
  broad reader compatibility needs. Do not add a stricter standard
  casually: PDF/A disables features (like transparency in A-1) and
  enlarges files.
- **Accessibility required** (public sector, requested by the user, or
  the audience includes assistive-technology users):
  `typst compile --pdf-standard ua-1 report.typ`. Every image then needs
  `alt:` text or compilation policy checks will be meaningless.
- **Archival required:** `--pdf-standard a-2b` (or `a-3b` when file
  attachments are embedded). Combine targets with a comma when both are
  required: `--pdf-standard a-2a,ua-1`.
- PDF/A-4 targets PDF 2.0; pick it only when the recipient explicitly
  asks, since older readers handle it worse.

## Validation gates, in order

1. `uv run scripts/check_pdf.py report.pdf` — baseline gate for every
   report: metadata, language, embedded fonts, text layer, tags,
   bookmarks. Add `--require-tagged` when accessibility is required.
   Fix and re-run until 0 failures; every remaining warning gets a
   stated reason in the delivery summary.
2. **veraPDF**, only when the report claims PDF/A or PDF/UA conformance
   (the Open Preservation Foundation's open-source validator;
   install: `brew install verapdf`):

   ```sh
   verapdf --flavour ua1 report.pdf   # PDF/UA-1
   verapdf --flavour 2b report.pdf    # PDF/A-2b
   ```

   Non-compliant rules are listed with clause references; fix the source
   (usually a missing alt text, metadata field, or untagged element) and
   recompile rather than post-processing the PDF.
3. **Visual inspection** — render pages and look at them:

   ```sh
   typst compile --format png --ppi 100 report.typ preview-{p}.png
   ```

   Check for overflowing tables, orphaned headings, broken figure
   placement, and unreadable chart text at print size. Typst compile
   warnings (missing font, overflow) are defects, not noise.

Automated validation is necessary but not sufficient: conformance
checkers cannot judge whether alt text is truthful or reading order
makes sense. Deliver the PDF together with the validation results and
say plainly that final accessibility and factual sign-off needs a human
reviewer.

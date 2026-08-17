# Design and writing rules

Distilled from Royal Statistical Society, ONS, UK Government Analysis
Function, Urban Institute, GOV.UK, and Designers Italia guidance. Apply
all of them; deviations need a reason stated in the delivery summary.

## Contents

- When a figure earns its place
- Truthful encoding
- Color semantics
- Layout and hierarchy
- Typography
- Plain language (English and Italian)

## When a figure earns its place

A figure exists to answer a recorded question. Choose the form by the
message, not by variety:

- One or two numbers, or exact values readers will look up → prose or a
  table, not a chart.
- Change over time → line. Comparison of categories → bar (horizontal
  when labels are long). Relationship between two measures → scatter.
- More than ~4 series on one chart → small multiples with identical
  scales, or mark one series `focus` and let the rest recede to gray.
- Never a chart added to make a page look richer: every figure must be
  cited from the prose ("Figure 2 shows...").

## Truthful encoding

A chart may simplify the data; it may not change what the data means.
The chart script enforces the mechanical part (zero-based bars, declared
truncation, no 3D or decoration). What it cannot enforce, you must:

- Keep scales comparable across charts the reader will compare.
- Show uncertainty, missing values, and caveats where the reader will
  see them (caption, callout, or annotation), not only in an appendix.
- State aggregations and exclusions ("excludes intercompany transfers")
  next to the first figure they affect.
- Annotations are either derived from the data or visibly editorial
  ("audit closed here"), never a fabricated trend statement.

## Color semantics

Color encodes meaning; pick the ramp by the data's structure:

- **Sequential** for ordered low-to-high values.
- **Diverging** for values around a meaningful midpoint (zero, target).
- **Qualitative** (the default Okabe-Ito palette) for unordered categories.

Color is never the only distinguishing channel: pair it with direct
labels, position, or line style. The bundled palette survives grayscale
and common color-vision deficiencies; if you replace it, verify both.

## Layout and hierarchy

The theme (`report-theme.typ`) fixes the grid, spacing, and heading
scale. Within it:

- One strong title, a short executive summary first, then sections in
  the order a busy reader needs them: findings before method.
- Headings state the topic or the conclusion ("Revenue grew fastest in
  the North"), not the activity ("Analysis of revenue").
- Whitespace separates ideas; callouts are for caveats and decisions the
  reader must not miss, at most a few per report.
- Numbered captions above figures and tables, source notes below.
- New colors, fonts, or per-page layout tweaks need a reason; the value
  of the system is that it stays stable across the whole report.

## Typography

The theme's defaults follow Section 508 practice: 11 pt body, legible
serif, generous line spacing, embedded fonts. Keep prose out of
all-caps and long italics; nothing below 9 pt except source notes.

## Plain language (English and Italian)

Plain language is professional, also for specialist audiences (GOV.UK,
Designers Italia). In both locales:

- Conclusion first, then supporting detail; short sentences and
  paragraphs; active voice where it is clearer.
- Familiar words over bureaucratic ones (use "use", not "utilizzare"
  when "usare" serves; "before", not "prior to").
- Define acronyms and technical terms at first use; keep the technical
  term when it is the precise one, and attach the explanation instead of
  replacing the term.
- One term per concept for the whole report (pick "revenue" or
  "turnover", not both).
- For Italian reports set `lang: "it"` in the theme (hyphenation, quote
  style, and "Figura"/"Tabella" labels follow), write dates as "17
  agosto 2026", and use the decimal comma in prose while keeping charts
  and tables consistent with the source data's notation.

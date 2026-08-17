// Design tokens and document wrapper for PDF reports.
// Copy next to your report file and import: #import "report-theme.typ": *
// Fonts are Typst-bundled (Libertinus Serif, DejaVu Sans Mono), so the
// output embeds them without any font installation.

#let tokens = (
  body-font: ("Libertinus Serif",),
  mono-font: ("DejaVu Sans Mono",),
  base-size: 11pt,
  ink: rgb("#1a1a1a"),
  muted: rgb("#555555"),
  faint: rgb("#8a8a8a"),
  primary: rgb("#0072B2"),
  accent: rgb("#D55E00"),
  rule-line: rgb("#cfcfcf"),
  panel: rgb("#f2f6fa"),
)

#let source-note(body) = text(size: 8.5pt, fill: tokens.faint, body)

// Wrapper for generated charts: numbered caption above (the chart SVG
// already carries its takeaway title and subtitle), source note below,
// alt text on the image for tagged output.
#let data-figure(path, caption: none, source: none, alt: none, width: 100%) = figure(
  {
    image(path, alt: alt, width: width)
    if source != none { align(left, source-note(source)) }
  },
  caption: caption,
)

#let callout(title: none, body) = block(
  width: 100%, fill: tokens.panel, inset: 12pt, radius: 2pt,
  stroke: (left: 2.5pt + tokens.primary),
  {
    if title != none { text(weight: "bold", size: 10pt, title); v(6pt) }
    body
  },
)

#let report(
  title: none,
  subtitle: none,
  description: none, // one-line abstract; becomes the PDF's Subject metadata
  authors: (),
  date: none,
  lang: "en", // "en" or "it"; drives hyphenation, quotes, and figure labels
  summary: none,
  toc: false,
  body,
) = {
  set document(title: title, author: authors, description: description)
  set page(
    paper: "a4",
    margin: (x: 2.4cm, top: 2.6cm, bottom: 2.8cm),
    footer: context {
      set text(size: 8.5pt, fill: tokens.faint, font: tokens.body-font)
      line(length: 100%, stroke: 0.5pt + tokens.rule-line)
      v(-4pt)
      grid(columns: (1fr, auto), title, counter(page).display("1 / 1", both: true))
    },
  )
  set text(font: tokens.body-font, size: tokens.base-size, lang: lang, fill: tokens.ink)
  set par(justify: true, leading: 0.62em, spacing: 1.15em)
  set raw(theme: auto)
  show raw: set text(font: tokens.mono-font, size: 9.5pt)
  show link: set text(fill: tokens.primary)

  set heading(numbering: "1.1")
  show heading.where(level: 1): it => block(above: 1.8em, below: 0.9em, text(size: 15pt, it))
  show heading.where(level: 2): it => block(above: 1.5em, below: 0.7em, text(size: 12.5pt, it))
  show heading.where(level: 3): it => block(above: 1.2em, below: 0.6em, text(size: 11pt, it))

  // Captions above the content for both figures and tables, source
  // notes below: the reader sees what a figure claims before the marks.
  show figure: set figure.caption(position: top)
  show figure.caption: set text(size: 9.5pt, fill: tokens.muted)
  set figure(gap: 0.8em)

  set table(stroke: none, inset: (x: 8pt, y: 6pt))
  show table.cell.where(y: 0): set text(weight: "bold", size: 10pt)

  // Title block
  text(size: 23pt, weight: "bold", title)
  if subtitle != none {
    v(2pt)
    text(size: 13pt, fill: tokens.muted, subtitle)
  }
  v(8pt)
  line(length: 100%, stroke: 0.8pt + tokens.rule-line)
  if authors.len() > 0 or date != none {
    v(2pt)
    text(size: 10pt, fill: tokens.muted, {
      if authors.len() > 0 { authors.join(", ") }
      if authors.len() > 0 and date != none { [ · ] }
      if date != none { date }
    })
  }
  v(1.5em)

  if summary != none {
    heading(level: 1, numbering: none, outlined: false,
      if lang == "it" [Sintesi] else [Executive summary])
    summary
    v(0.5em)
  }
  if toc {
    outline()
    v(1em)
  }
  body
}

// Table rule helpers: header rule + closing rule, no vertical lines.
#let thead-rule = table.hline(stroke: 0.8pt + tokens.ink)
#let tfoot-rule = table.hline(stroke: 0.5pt + tokens.rule-line)

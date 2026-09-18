#set page(
  paper: "a4",
  margin: (x: 10mm, top: 12mm, bottom: 12mm),
  numbering: "1 of 1",
)
#set text(
  font: ("Avenir Next", "Helvetica Neue", "Helvetica", "Arial", "Liberation Sans"),
  size: 9pt,
)
#set par(justify: false, leading: 0.42em, spacing: 0.52em)
#show heading: set block(above: 0.75em, below: 0.28em)
#show heading.where(level: 1): set text(size: 14pt, weight: "bold")
#show heading.where(level: 2): set text(size: 11pt, weight: "bold")
#show heading.where(level: 3): set text(size: 9.5pt, weight: "bold")
#show raw.where(block: false): it => box(
  fill: rgb("#f2f2f2"),
  inset: (x: 2pt, y: 0pt),
  outset: (y: 2pt),
  it,
)
#show raw.where(block: true): set text(size: 7.5pt)
#set table(inset: 4pt, stroke: 0.4pt + rgb("#cccccc"))

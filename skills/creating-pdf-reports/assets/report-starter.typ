// Starter report: copy next to report-theme.typ, rename, and replace the
// content. Every pattern the theme supports is demonstrated once below.
// Compile: typst compile report.typ  (add --pdf-standard ua-1 when
// accessibility conformance is required; see references/pdf-standards.md)

#import "report-theme.typ": *

#show: report.with(
  title: "Revenue performance 2022-2025",
  subtitle: "Regional analysis for the annual review",
  description: "Regional revenue analysis 2022-2025 for the annual review",
  authors: ("Analysis Team",),
  date: "17 August 2026",
  lang: "en", // "it" switches summary heading, figure labels, hyphenation
  summary: [
    Revenue grew in three of four regions between 2022 and 2025. The North
    region grew fastest, from EUR 12.1 million to EUR 21.4 million, while
    the South was flat. We recommend concentrating the 2026 expansion
    budget on the North and Center regions.
  ],
  toc: false, // enable for reports with many sections
)

= Findings

North region revenue grew from EUR 12.1 million in 2022 to EUR 21.4
million in 2025, a 77% increase. The Center region followed the same
trend at a lower level, while the South stayed within a narrow band
around EUR 8.5 million.

// Charts from make_chart.py already carry their title, subtitle, and
// source note inside the SVG, so pass only caption and alt here. Use the
// source: parameter only for images that lack an embedded source note.
#data-figure(
  "fig-revenue-by-region.svg",
  caption: [Annual revenue by region, 2022-2025],
  alt: "Line chart of annual revenue in EUR millions for three regions from 2022 to 2025. North grows from 12.1 to 21.4; Center from 9.0 to 14.1; South is flat around 8.5.",
)

#callout(title: [Data caveat])[
  2025 figures are provisional until the year-end audit closes. All
  amounts exclude intercompany transfers.
]

== Detail table

#figure(
  {
    table(
      columns: (auto, 1fr, 1fr, 1fr),
      align: (left, right, right, right),
      table.header([Region], [2022], [2024], [2025]),
      thead-rule,
      [North], [12.1], [17.9], [21.4],
      [Center], [9.0], [12.5], [14.1],
      [South], [8.4], [8.1], [8.6],
      tfoot-rule,
    )
    align(left, source-note[Revenue in EUR millions. Source: validated revenue extract.])
  },
  caption: [Revenue by region, EUR millions],
)

= Method

Figures were produced from the validated revenue extract
(`revenue.csv`) grouped by region and year. No adjustments were applied
beyond the exclusions listed in the data caveat.

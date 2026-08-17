# Figure specs

Every chart in the report is rendered by `scripts/make_chart.py` from a
YAML spec. The spec is the audit trail: it records what question the
figure answers, which data it uses, and what claim it makes. Write one
spec file per figure, next to the data it reads.

Run: `uv run scripts/make_chart.py <spec.yaml> [-o OUTPUT_DIR]`
(dependencies install automatically via uv). Output: `<id>.svg`,
reproducible byte-for-byte. Validation errors name the exact field to
fix; warnings (too many series, grouped bars) go to stderr and deserve a
design response, not suppression.

## Schema

| Field | Required | Meaning |
| --- | --- | --- |
| `id` | yes | kebab-case, becomes the SVG filename |
| `question` | yes | the question the figure answers; if you cannot state one, the figure should not exist |
| `takeaway` | yes | one-sentence answer; rendered as the chart title |
| `subtitle` | yes | measure, units, geography, period (e.g. "Annual revenue, EUR millions, by region, 2022-2025") |
| `chart_type` | yes | `line`, `bar`, `barh`, `scatter`, or `area` |
| `data.csv` or `data.rows` | yes | CSV path relative to the spec, or inline records |
| `encodings.x`, `.y` | yes | data field names; `.y` must be numeric |
| `encodings.series` | no | field that splits the data into lines/groups |
| `color_roles` | no | map of series/category name to `focus`, `accent`, or `neutral`; marking one series `focus` grays out the rest |
| `sort` | no | bar charts: `y_desc` / `y_asc`; default keeps data order |
| `y_zero` | no | default `true` for bar/barh/area; setting `false` there requires `truncation_note` |
| `truncation_note` | see above | explanation of the axis truncation, shown to the reader via your prose or caption |
| `annotations` | no | list of `{x, y (optional), text}` editorial marks |
| `source_note` | yes | "Source: ..." with dataset name and snapshot date; drawn inside the chart |
| `alt_text` | yes | text alternative describing the chart and its key values; reuse it as the `alt:` in the Typst `data-figure` |

## Example (complete, rendered during skill development)

```yaml
id: fig-revenue-by-region
question: "How did revenue change by region between 2022 and 2025?"
takeaway: "Revenue grew fastest in the North"
subtitle: "Annual revenue, EUR millions, by region, 2022-2025"
chart_type: line
data:
  csv: revenue.csv
encodings:
  x: year
  y: revenue
  series: region
color_roles:
  North: focus
source_note: "Source: validated revenue extract, snapshot 2026-08-01"
alt_text: "Line chart of annual revenue in EUR millions for three regions
  from 2022 to 2025. North grows from 12.1 to 21.4; Center from 9.0 to
  14.1; South is flat around 8.5."
```

## What the script decides for you

House style is built in, so specs stay small: Okabe-Ito colorblind-safe
palette, direct series labels instead of legends, zero-based value axes,
light gridlines on the value axis only, horizontal labels, DejaVu Sans,
value labels on bars, source note bottom-left. The SVG carries the
takeaway title, subtitle, and source note, so in Typst pass only
`caption:` and `alt:` to `data-figure`.

Values shown in a chart come from `data` and nowhere else. If a number
you want to show is not in the source data, the fix is to get it into a
validated dataset, never to type it into the spec as an annotation.

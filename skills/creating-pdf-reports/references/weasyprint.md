# WeasyPrint variant (HTML/CSS source)

Use this path only when the report content already exists as HTML/CSS
(a web app's report view, an HTML template pipeline). For content
written from scratch, Typst gives better typography and accessibility
support; go back to the main workflow.

WeasyPrint is an OSS (BSD) Python library that renders HTML+CSS to PDF
locally. No system packages are needed on macOS beyond Pango (installed
with `brew install pango` if missing).

```sh
uv tool install weasyprint     # or: uvx weasyprint ...
weasyprint report.html report.pdf \
  --pdf-variant pdf/ua-1 \
  --media-type print
```

Requirements that stay the same as the Typst path:

- Charts still come from `scripts/make_chart.py` SVGs referenced with
  `<img src="fig.svg" alt="...">`; never hand-drawn `<canvas>`/CSS bars.
- The HTML must carry `<html lang="...">`, `<title>`, semantic headings
  in order, table `<th>` headers, and alt attributes; WeasyPrint derives
  the PDF structure from them.
- Use `@page` CSS for size, margins, and page numbers; embed no remote
  resources (fonts and images referenced by local path only, so the
  build is deterministic and nothing leaks to the network).
- WeasyPrint's documentation warns that the PDF/A and PDF/UA variant
  flags do not guarantee conformance: run the same validation gates
  (`check_pdf.py`, veraPDF, visual inspection) from
  [pdf-standards.md](pdf-standards.md).

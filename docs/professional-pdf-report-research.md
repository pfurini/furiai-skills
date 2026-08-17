# Creating Professional PDF Reports Without AI Slop

## Research report and skill design brief

**Research date:** 17 August 2026

## Executive summary

A professional PDF report is not produced by asking an AI model to make a document look polished. It is produced by a controlled publishing pipeline with four distinct responsibilities:

1. **Content planning:** define the audience, purpose, claims, evidence, and reading sequence.
2. **Data visualization:** generate charts deterministically from validated data.
3. **Document design:** apply a coherent system of typography, color, spacing, hierarchy, and layout.
4. **Quality assurance:** validate data fidelity, accessibility, language, PDF conformance, and reader compatibility.

The AI can help draft prose, propose an outline, classify data, suggest chart types, and generate figure specifications. It should not be trusted to invent numbers, manually draw data figures, choose arbitrary visual decoration, or certify its own output.

The most useful sources combine authoritative standards with practical public-sector and research-publishing guidance. The recommended source stack is:

- Royal Statistical Society and ONS guidance for truthful, readable visualization.
- Government Analysis Function, WCAG, and PDF/UA guidance for accessibility.
- GOV.UK, Designers Italia, and Canada guidance for plain language.
- Urban Institute and the European Commission for professional report systems.
- Typst or WeasyPrint documentation for implementation.
- veraPDF and manual assistive-technology testing for validation.
- Recent visualization-generation research for anti-hallucination controls.

## 1. What “professional” should mean

Professional quality is not visual complexity. It means that the report is:

- **Truthful:** visual encodings preserve the meaning and scale of the data.
- **Useful:** every chart, table, and callout helps the reader answer a question.
- **Readable:** hierarchy, typography, spacing, and labeling reduce cognitive load.
- **Consistent:** the same concepts use the same visual and linguistic conventions throughout.
- **Self-contained:** fonts, images, metadata, and structural information are embedded.
- **Portable:** the PDF renders predictably across common readers and devices.
- **Accessible:** the document has semantic structure, text alternatives, sufficient contrast, and a logical reading order.
- **Clear:** English or Italian prose uses ordinary language unless a technical term is genuinely necessary.
- **Traceable:** every important claim and figure can be linked to its source data and transformation steps.

A useful quality test is: *Could a reader understand the main findings without the author being present to explain the document?*

## 2. Data visualization principles

### 2.1 Start with the question

A figure should answer a defined question. The skill should reject charts that exist only to make a page look richer.

Before choosing a chart, record:

- the question the figure answers;
- the audience and their expected knowledge;
- the data fields and units;
- the relevant time period and geography;
- the intended takeaway;
- whether prose or a table would communicate the point better.

The Royal Statistical Society describes good visualization as accurate, readable, effective, and fit for its intended purpose. Its guide also warns against relying on software defaults because each visualization has a different story and audience.

### 2.2 Preserve data meaning

The skill should enforce these defaults:

- no 3D effects, pictograms, decorative textures, or simulated depth;
- no unexplained axis truncation;
- bar charts normally start at zero;
- scales remain comparable across small multiples;
- units appear in titles, subtitles, or axes;
- uncertainty, missing values, and caveats are visible;
- aggregations and sorting are explicitly recorded;
- all annotations are derived from the data or clearly marked as editorial commentary.

A chart may simplify data, but it must never silently change what the data means.

### 2.3 Optimize for comprehension

Recommended practices from ONS and the UK Government Analysis Function include:

- remove unnecessary borders, backgrounds, shadows, and gridlines;
- use direct labels instead of forcing readers to decode legends;
- keep labels horizontal where possible;
- write titles that identify the measure, geography, and time period;
- put source information and explanatory notes close to the figure;
- provide a text alternative or accessible data table;
- avoid overcrowded charts and split complex material into small multiples.

A practical baseline is to keep dense line or clustered charts to approximately four series or categories. This is a useful warning threshold, not an absolute law.

### 2.4 Choose colors according to data semantics

Color should encode meaning, not decoration:

- **Sequential:** ordered low-to-high values.
- **Diverging:** values around a meaningful midpoint such as zero, a target, or a median.
- **Qualitative:** unordered categories.
- **Binary:** two groups that do not imply a magnitude relationship.

ColorBrewer and Matplotlib both emphasize that lightness is often perceived more reliably than hue. A palette should therefore be checked in grayscale and under common color-vision deficiencies.

Color must never be the only way to distinguish categories. Add labels, line styles, symbols, position, patterns, or textual explanations where needed.

## 3. Report design system

### 3.1 Use a small, explicit system

The skill should define design tokens before rendering:

- page size and margins;
- column grid and spacing scale;
- body, heading, caption, table, and footnote sizes;
- font families and weights;
- primary, secondary, neutral, warning, and success colors;
- chart palette roles;
- border, radius, and shadow rules;
- header, footer, page-number, and source-note styles.

The system should be stable across the entire report. A new color or font should require a reason.

### 3.2 Build hierarchy through typography and layout

The European Commission and Urban Institute guidance recommend a clear reading sequence, aligned elements, consistent placement, and a limited heading hierarchy.

Use:

- one strong document title;
- a short executive summary;
- a predictable hierarchy of sections and subsections;
- informative headings that state the topic or conclusion;
- consistent figure numbering and captions;
- whitespace to separate ideas rather than decorative containers;
- a grid that aligns text, charts, tables, and notes.

The chart should be visually dominant over its supporting furniture. Axes, labels, sources, and notes should support interpretation without competing with the data.

### 3.3 Typography defaults

Section 508 guidance notes that accessibility standards do not mandate one universal typeface or minimum size, but readability is strongly affected by typography. Practical defaults are:

- use a highly legible body font;
- use approximately 11 to 12 pt body text for normal digital documents;
- avoid long passages below 9 pt;
- avoid decorative, condensed, or excessively thin fonts;
- use adequate line spacing and paragraph spacing;
- avoid all-caps prose and unnecessary italics;
- embed the selected fonts in the PDF.

## 4. Plain language in English and Italian

Plain language is compatible with professionalism. GOV.UK guidance explicitly recommends plain English even for specialist audiences because it enables faster comprehension. Technical terms are acceptable when they are needed, but they should be explained at first use.

The skill should:

- prefer familiar words over bureaucratic alternatives;
- use active voice where it improves clarity;
- keep sentences and paragraphs short;
- state the conclusion before supporting detail;
- define acronyms and technical terms on first use;
- use the same term consistently for the same concept;
- avoid metaphors that could be ambiguous in translation;
- support both English and Italian locale settings;
- check that translated headings preserve meaning and hierarchy.

Designers Italia provides a strong Italian reference for writing content that helps users find information, orient themselves, and understand what to do. For specialized reports, the correct approach is not to remove technical language, but to separate the technical term from its plain-language explanation.

## 5. PDF standards and compatibility

PDF/A and PDF/UA solve different problems:

- **PDF/A** is primarily for archival and self-contained documents.
- **PDF/UA** is for accessibility and semantic structure.
- **PDF 1.7 or PDF 2.0** defines the underlying PDF version.

For general exchange, PDF 1.7 is a sensible default because it has broad reader support. The document should embed fonts and images, use Unicode-mappable text, and avoid external resources.

When archival and accessibility conformance is required, target PDF/UA-1 with PDF/A-2a or PDF/A-3a when attachments are required. PDF/A-4 targets PDF 2.0 and should not be selected casually when compatibility with older readers matters.

The skill should verify:

- all used fonts are embedded;
- all meaningful text remains actual text, not an image;
- the document has a title, language, author, and subject;
- headings are tagged and ordered correctly;
- tables have header cells and logical reading order;
- figures have alternative descriptions or nearby equivalent text;
- decorative shapes are marked as artifacts;
- links have meaningful labels;
- bookmarks are generated for substantial reports;
- no required font, image, stylesheet, or script is loaded externally.

## 6. Implementation options

### Typst

Typst is the preferred default when the skill needs strong typography, deterministic layout, and source-controlled templates. Its documentation states that:

- PDF 1.7 is the default output;
- tagged PDF is enabled by default;
- PDF/UA-1 is supported;
- semantic headings, figures, tables, language metadata, and alternative descriptions are available.

References:

- <https://typst.app/docs/reference/pdf/>
- <https://typst.app/docs/guides/accessibility/>

### WeasyPrint

WeasyPrint is suitable when the harness is already based on HTML and CSS. It embeds and subsets fonts automatically and exposes PDF/A and PDF/UA output options. Its documentation explicitly warns that conformance is not guaranteed, so every output must still be validated.

Reference: <https://doc.courtbouillon.org/weasyprint/stable/api_reference.html>

### Validation with veraPDF

Use veraPDF in the build pipeline for PDF/A and PDF/UA profile validation. It supports machine-readable validation reports and can identify failed conformance rules.

Reference: <https://docs.verapdf.org/cli/validation/>

## 7. Anti-AI-slop architecture

Recent research shows that LLM-generated visualizations can contain invalid code, incorrect transformations, illegal sorting, missing legends, overflow, low contrast, and typographical errors. Other research found that LLM-generated charts did not match the accuracy of human-generated charts.

The skill should therefore use this architecture:

1. **LLM planning layer:** outline, audience analysis, claims, chart proposals, wording.
2. **Structured intermediate representation:** report sections, figure specifications, data provenance, and design tokens.
3. **Deterministic rendering layer:** Typst, WeasyPrint, or another controlled renderer.
4. **Automated validation layer:** data checks, chart linting, PDF conformance, font checks, contrast checks, and overflow detection.
5. **Human review layer:** visual inspection, source verification, language review, and assistive-technology spot checks.

The model should never be allowed to fabricate a data point, source, citation, trend, annotation, or visual measurement.

## 8. Recommended figure specification

Every figure should be generated from a structure similar to:

```yaml
id: figure-01
question: "How did revenue change by region between 2022 and 2025?"
data_source:
  name: "Validated revenue extract"
  uri: "https://example.org/source"
  snapshot_hash: "..."
transformations:
  - "group by region and year"
  - "sum revenue"
chart_type: "line"
encodings:
  x: year
  y: revenue
  series: region
units: "EUR millions"
scale:
  y_axis: "linear"
color_roles:
  focus: "primary"
  comparison: "neutral"
title: "Revenue increased in three of four regions"
source_note: "Source: ..."
takeaway: "Northern and central regions grew fastest."
alt_text: "Line chart showing ..."
```

This intermediate representation makes the output auditable and allows the same report to be rendered into PDF, HTML, or another format later.

## 9. Recommended source set

### Core design and data visualization

- <https://royal-statistical-society.github.io/datavisguide/>
- <https://service-manual.ons.gov.uk/data-visualisation/guidance/principles>
- <https://analysisfunction.civilservice.gov.uk/policy-store/charts-a-checklist/>
- <https://data.europa.eu/apps/data-in-publications-guide/2022-data-in-publications-guide-extended.pdf>
- <https://urbaninstitute.github.io/graphics-styleguide/>
- <https://colorbrewer2.org/learnmore/schemes_full.html>
- <https://matplotlib.org/stable/users/explain/colors/colormaps.html>

### Accessibility and standards

- <https://www.w3.org/TR/WCAG22/>
- <https://www.section508.gov/develop/fonts-typography/>
- <https://www.iso.org/standard/75839.html>
- <https://www.iso.org/standard/71832.html>
- <https://www.iso.org/standard/82278.html>
- <https://pdfa.org/resource/conforming-to-both-pdf-a-and-pdf-ua-best-practice-guide/>
- <https://docs.verapdf.org/cli/validation/>

### Plain language

- <https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/>
- <https://docs.italia.it/italia/designers-italia/writing-toolkit/it/bozza/suggerimenti-di-scrittura.html>
- <https://accessible.canada.ca/guidelines-creating-accessible-documents>

### AI reliability

- <https://arxiv.org/abs/2407.00981>
- <https://aclanthology.org/2025.coling-main.501/>

## Final recommendation

Build the skill around a deterministic report compiler with an LLM-assisted planning interface. Store every claim, figure, transformation, source, and design decision in structured form. Render with Typst by default, validate with veraPDF, and require both automated and human review before delivery.

The defining rule should be:

> AI may help explain the data and design the report. Only validated source data and deterministic rendering may assert what the data says.

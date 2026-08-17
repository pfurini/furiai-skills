# PDF report (main thread — after the verdict)

Run this yourself, after the decision memo is presented (idea-validation)
or the market briefing is presented (market-deep-dive). Ask once:

> **Want a PDF report?** `EN` / `IT` / `both` / `skip`

`skip` ends the step with no output. Otherwise: this file is the content
spec; the rendering pipeline is the **creating-pdf-reports** skill
(installed alongside this one) — load it and follow its Steps 1–6, using
the Step 1 answers below. If `typst` is not installed, say so, give the
install command from that skill, and offer to skip.

## Step 1 answers (scope, for the pdf skill)

- **Audience and purpose:** the founder who commissioned the validation,
  plus anyone they show it to (cofounder, advisor, investor). The report
  must stand alone — a reader who never saw the chat gets the full
  picture.
- **Locale:** from the user's answer. `both` = two complete renders,
  `report_en.pdf` and `report_it.pdf` — never a mixed-language file.
- **Conformance:** default profile. Add PDF/UA only if the user asks.
- **Claims inventory:** the artifact files ARE the inventory. Every
  number, verdict, label, and quote in the report is copied from a file
  under `.idea-validation/` (or from a URL those files cite). A claim
  with no artifact source is cut — the report never introduces new
  research.

## Files

Working files (figure spec YAMLs, generated SVGs, the `.typ` source and
copied theme) go in `ideas/<slug>/report/`. Outputs go beside the other
artifacts: `ideas/<slug>/report_en.pdf` and/or `report_it.pdf`.
Regenerating overwrites — the store keeps only the latest report; the
dated evidence lives in the artifacts, not here.

## Structure — inverted pyramid

**Executive layer (pages 1–2, hard cap).** A reader who stops here has
the essentials:

- Verdict line + final score (validation) or the enter/wait/avoid
  recommendation (deep-dive), with the watermark sentence when
  `score_confidence` is not high or NO-RING-1 fired.
- Why, in 2–4 sentences — what the analysis revealed, not how it works.
- The score-profile figure (validation) or market-size figure
  (deep-dive).
- Top strengths and top risks, one sentence each with its data point.
- The riskiest assumption and its pass/fail test (validation): what to
  do, cost, duration, threshold.
- The recommended next step and the kill criteria.

**Deep layer (everything after page 2).** One section per theme, each
carrying evidence the executive layer only concluded from:

1. **Demand & market signals** — per-platform trend verdicts and the
   evidence highlights (with ring/geography labels where the artifacts
   carry them); disconfirming evidence gets its own paragraph, never
   silently dropped.
2. **Competition** — the mapped landscape, saturation, gaps; a table
   beats prose for the top competitors (name, pricing, top complaint).
3. **Market size** — TAM/SAM/SOM with the method and the reality checks;
   per ring, Italy first, for b2c; the buyer-redirection decision for
   b2b.
4. **Unit economics** — pricing model and anchors, retention estimate
   with its band-or-floor choice, CAC by channel, LTV:CAC.
5. **Methodology & confidence** — which agents ran, each artifact's
   `confidence`, which figures are constructs (say so plainly), missing
   inputs, and what the score discount/gate/disclosure did.
6. **References** — see below.

Sections that have no artifact (e.g. no market sizer ran) are omitted,
not padded.

## References (two mechanisms, both required)

- **Inline:** every load-bearing claim cites its source at the point of
  use — the artifact filename, plus the original URL when the artifact
  itself cites one for that figure.
- **Appendix:** the final section lists the complete union of every
  `Sources` section from every artifact used, deduplicated, grouped by
  artifact. Long is fine here; this is the one place exhaustiveness
  beats brevity.

## Writing rules (both languages)

The register is plain-language precision — simplified-technical-English
discipline with an explain-it-simply tone:

- Short sentences. Active voice. One idea per sentence.
- Define each technical term in parentheses at first use ("k-factor
  (how many new users each user brings)"), then use the term freely.
  Never replace a technical term with a vague paraphrase.
- **Never alter data:** numbers at source precision, verdict labels
  verbatim, quotes verbatim (Italian quotes keep the parenthetical
  translation rule), currencies as the artifacts carry them.
- No fluff: no throat-clearing, no restated methodology in prose, no
  sentence that a reader could delete without losing information.
- No repetition: the executive layer states conclusions; the deep layer
  carries their evidence. A number appears in both only when it is the
  load-bearing point of each.
- No model tics, in either language: prefer parentheses or commas to
  em-dash asides, no triad-for-rhythm lists, no "it is important to
  note" throat-clearing, no connector-first sentence chains (the pdf
  skill's `italian-prose.md` lists the full set — its AI-pattern section
  applies to the English edition too).

## Figure rules

Use a figure exactly where a comparison, distribution, or trend is
grasped faster visually than in prose — clarity without losing
precision. Every figure goes through the pdf skill's spec-YAML +
`make_chart.py` pipeline (source note = artifact path; alt text
mandatory). Never a decorative chart; never a chart of a single number.

Keep category labels at ~13 characters or fewer — the chart script clips
longer axis labels; abbreviate on the axis and expand the abbreviation in
the caption (verified 2026-08).

Candidate menu (pick 2–4 for a validation, 2–3 for a deep-dive; skip any
whose artifact is missing):

| Figure | Source | When it earns its place |
|---|---|---|
| Dimension score profile (6 bars + verdict bands) | scores.json | Always, for validations — it IS the verdict at a glance |
| TAM → SAM → SOM (per ring for b2c) | market_size.json | When the sizer ran; the funnel collapse is the point |
| LTV:CAC by channel vs the 3:1 bar | cac.json | When channels differ materially or the verdict hinges on the ratio |
| Retention estimate vs published floor/band | retention.json | When the floor path fired or retention is a top risk |
| Ring coverage of the evidence (IT / EU-EN / Western) | scores.json.ring_coverage | b2c, when the distribution of evidence matters to trust |
| Trend velocity per platform | trend-file frontmatters | Deep-dives; multi-platform comparison |

## Italian edition (`IT` or `both`)

- Prose translated to Italian; the pdf skill's `it` locale handles
  typography and its design rules' Italian writing guidance.
- Technical terms, schema labels, verdict values, and quoted material
  stay verbatim (add a parenthetical Italian gloss at first use where
  the term is opaque).
- Numbers, units, and currencies unchanged from the artifacts — fidelity
  beats locale formatting.
- `both` means two full passes of the pdf skill's compose+validate
  steps; figures are re-rendered per language when they contain text
  (titles, axis labels), not shared.

## Done when

Per the pdf skill's gates: the checker reports 0 failures, every page
was visually inspected, every figure traces to an artifact, and the
user got the output path(s) plus the standard sign-off caveat.

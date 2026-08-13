# Competitor research sources — B2B calibration (Italy-first, self-serve micro-SaaS)

Loaded by `iv-competitor-mapper` via the CALIBRATION path in its dispatch
prompt. Defines where to hunt for each competitor category and the
saturation factor anchors for the Italian B2B target. The competitor
taxonomy, review-mining method, gap analysis, and scoring mechanics live in
the agent brief.

> Geography rule: the competitive set is **products an Italian micro/small
> firm can actually buy and run** — Italian-language, and compliant with the
> niche's obblighi (SDI, PCT, conservazione…) where relevant. Global tools
> without Italian localization are substitutes/benchmarks, not direct
> competitors, unless the niche is language-neutral (dev tools, some
> e-commerce ops). Confidence: source lists verified 2026-08; the
> review→customer proxy is `confidence: low` (worse in Italy — Italians
> under-review).

## Contents

- Direct Competitor Sources (search in order; queries Italian-first)
- User-Base Estimation (Italy recalibration)
- Primary Search Surface Methodology — bilingual keyword sets
- Substitutes — Italian B2B specifics
- Emerging Threat Sources
- Saturation Factor Anchors (Italy-recalibrated)

## Direct Competitor Sources (search in order; queries Italian-first)

1. **Incumbent suite check** (before anything else): does a TeamSystem /
   Zucchetti / Wolters Kluwer / Buffetti / Danea / Namirial-class suite, or a
   vertical incumbent, already own this workflow as a module? If
   `<niche>-incumbents-*.md` exists in market_insights, extract its incumbent
   map; otherwise search the vendor families' product pages directly. The
   incumbent module IS a direct competitor even with zero reviews anywhere.
2. **Capterra.it category browse**: matching category page(s); record
   listed-product count, and separately the subset with **Italian-language
   reviews** — that subset approximates the Italian competitive set.
3. **Italian comparison articles**: `miglior software [categoria] [current
   year]`, `[incumbent] alternative`. Products every independent Italian list
   repeats are the leaders; discount affiliate/translated listicles.
4. **Marketplace search** (when the niche lives inside a platform): Fatture
   in Cloud App Store, TeamSystem Commerce Apps Market, Shopify App Store
   (Italian-language listings), Zapier directory, Chrome Web Store. Record
   top 10 with installs/reviews/pricing.
5. **G2 / Capterra.com global browse** — the global landscape: leaders,
   review counts, structured "dislikes". Label everything `geography:
   global`; it seeds the localization-gap analysis, not the Italian census.
6. **Market insights files**: extract every product named in
   `<niche>-g2-capterra-*.md`, `<niche>-communities-*.md`,
   `<niche>-incumbents-*.md`.
7. **Trustpilot.it / Google reviews discovery**: search the niche keywords —
   Italian SMB products often live here rather than on G2.
8. **AlternativeTo.net**: adjacent competitors of the closest global product.

## User-Base Estimation (Italy recalibration)

No published review→customer multiplier exists for the Italian market, and
Italian buyers review far less than Anglophones — the G2/Capterra 30–60×
proxy applies **only to the global set**. For Italian products, in order of
preference: marketplace install counts where shown (1–3×) · vendor-claimed
customer counts halved · incumbent forum/support volume as a relative-size
signal · Italian-language review counts as a floor, never a census.
Everything here is `confidence: low`; say which proxy each estimate used.

## Primary Search Surface Methodology — bilingual keyword sets

Run every search in Italian first (the exact buyer vocabulary: "gestionale",
"software studio", "fatturazione", the niche's own terms), then English:

1. **Primary keyword**: the term an Italian buyer would type (e.g. "software
   preventivi edilizia").
2. **Problem keyword**: the job statement ("automatizzare solleciti clienti").
3. **Audience keyword**: buyer + need ("gestionale per studi associati").
4. **Adjacent keyword**: broader category terms, both languages.

For each search record: relevant-result count; review count/rating of top 3;
whether the top result is an incumbent-suite module; last-update dates of
top 5 (stale products = displacement opportunity).

Review mining surface: Italian-language reviews first (Capterra.it,
Trustpilot.it, Google, marketplace reviews), then the global 1–2-star /
3-star / 5-star method from the agent brief on G2/Capterra.com. Complaints
about **missing Italian localization or compliance** (lingua, SDI, F24,
conservazione, pagamenti italiani) are first-class competitive gaps.

## Substitutes — Italian B2B specifics

The dominant substitutes in Italian micro-firm niches, all of which must be
priced:

- **Excel / carta** — the default; price at hours × loaded wage (use salary
  data from job posts in market_insights when present; otherwise state the
  assumption explicitly).
- **"Lo fa il commercialista / il consulente"** — delegation to the
  professional intermediary is a substitute unique to this market: the firm
  outsources the workflow inside a fee it already pays. When this is the
  substitute, seriously evaluate whether the real buyer is the studio, not
  the firm (see the market-sizing pack's buyer-redirection step).
- **The incumbent suite's clunky built-in module** — "già incluso" beats
  better-but-paid for the median Italian buyer.
- **An employee's manual hours** — at Italian SMB wage levels, manual labor
  stays price-competitive with software longer than in the US; check the
  math both directions.

## Emerging Threat Sources

- Incumbent release notes / "novità" pages and partner-event announcements
  (TeamSystem, Zucchetti, WK ship toward whatever the ordini are discussing)
- Funded Italian startups in the category (Crunchbase/Dealroom, Italian
  tech press: StartupItalia, EconomyUp)
- Platform features (Shopify Editions, Google Workspace, AI assistants)
  absorbing the job natively
- If `trend_velocity` = "rising-fast" in market_insights, expect entrants

Flag funded competitors — they can outspend an indie head-on.

## Saturation Factor Anchors (Italy-recalibrated)

| Factor | Low (1 pt) | Medium (2 pts) | High (3 pts) |
|---|---|---|---|
| **Direct competitor count** (Italian-viable products only) | 0–2 | 3–6 | 7+ |
| **Incumbent dominance** | No suite module; no Italian product above ~50 Italian-language reviews | A suite offers a partial module, or 1–2 Italian products with clear traction (reviews, installs, claimed customers) | A major suite ships the feature to its installed base, or an Italian product is the recognized default (>200 Italian-language reviews or equivalent install evidence) |
| **Funding in space** | No funded competitors | 1–2 funded startups | Multiple funded companies or a suite vendor active in the category |
| **Keyword saturation (google.it)** | Italian queries show weak/foreign-only results | Moderate results, quality varies | Top Italian results are solid, actively maintained local products |
| **Content saturation** | Few Italian comparison pages | Some, moderate SEO competition | Crowded Italian SERPs: vendor content + affiliate comparisons |

Review-count thresholds are provisional (`confidence: low`) and an order of
magnitude below the global anchors on purpose: in Italy ~50 genuine
Italian-language reviews already indicates an established product. Never
apply the global 2,000-review bar to the Italian set.

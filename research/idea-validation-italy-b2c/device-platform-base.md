# Italy consumer device and platform base (research question DA1)

Research date: 2026-08-13. All figures carry source, URL, measurement or publication date, and a confidence tag.

- **high** = official or primary dated source (Apple, AGCOM, ISTAT, StatCounter's own export, Auditel).
- **medium** = reputable secondary source, or a primary source reported through a press intermediary.
- **low** = estimate, planning range, undated figure, or a vendor market-research summary with no stated method.

Anything measured more than 12 months before the research date is marked **dated-but-usable**.

---

## 1. iOS vs Android in Italy

### 1.1 Headline

| Metric | Value | Source | Date | Confidence |
| --- | --- | --- | --- | --- |
| Android share of Italian mobile page views | 64.86% | StatCounter Global Stats, [os-market-share/mobile/italy](https://gs.statcounter.com/os-market-share/mobile/italy) | July 2026 (fetched live 2026-08-13) | high |
| iOS share of Italian mobile page views | 35.13% | StatCounter Global Stats, same URL | July 2026 (fetched live 2026-08-13) | high |

**Methodology caveat, and it matters for a platform-choice decision.** StatCounter measures share of *web page views* from mobile devices carrying its tracking script, not installed base and not device sales. It is generally understood to run iOS-high relative to ownership, because iPhone owners skew toward heavier and more browser-based web use. Read "iOS is 35% of Italian mobile page views" as an upper-ish bound on the iOS share of the Italian population, and cross-read it against the ownership data in section 2 and the vendor data below. No independent, publicly free, non-StatCounter measurement of the Italian OS split was found (see the negative-result log).

### 1.2 Trend over the last three years

Pulled from StatCounter's own CSV export endpoint for Italy, monthly, August 2023 through July 2026 (36 months). This is the same underlying dataset as the headline figure, so it is a same-source trend, not an independent confirmation.

| Period | Mean iOS share | Mean Android share | Confidence |
| --- | --- | --- | --- |
| Aug–Dec 2023 (5 months) | 31.6% | 68.0% | high |
| Calendar 2024 (12 months) | 30.3% | 69.3% | high |
| Calendar 2025 (12 months) | 31.1% | 68.5% | high |
| Jan–Jul 2026 (7 months) | 34.9% | 65.0% | high |

Source: StatCounter Global Stats CSV export, `gs.statcounter.com/chart.php?...&region=Italy&fromMonthYear=2023-08&toMonthYear=2026-07&csv=1`, retrieved 2026-08-13, confidence high.

Selected monthly values so the shape is visible: 2024-03 iOS 28.62% (the three-year low), 2025-10 iOS 33.63%, 2026-05 iOS 37.20% (the three-year high), 2026-06 iOS 33.87%, 2026-07 iOS 35.13%.

**Reading of the trend.** iOS was flat at roughly 30–31% through 2024 and most of 2025, then stepped up from around September 2025 onward. The 2026 year-to-date mean is about 4.6 points above the 2024 mean. Month-to-month noise is large (May 2026 at 37.2% followed by June at 33.9%), so no single month should be quoted as the level. The defensible claim is: **iOS in Italy has drifted up roughly 4 points over two years and now sits in the mid-30s, but Italy remains firmly Android-majority.**

### 1.3 Supporting vendor-level context

| Metric | Value | Source | Date | Confidence |
| --- | --- | --- | --- | --- |
| Apple share of Italian mobile device vendors | Apple overtook Samsung as leading vendor in 2023; 2024 share stated as "roughly" a figure withheld behind paywall | Statista, [mobile vendor market share Italy 2016-2024](https://www.statista.com/statistics/1280101/market-share-mobile-device-vendors-italy/) | published 2025-11-19 | low (value paywalled; only the directional claim is readable) |
| Apple share of Italian smartphone market | 25–28% | Sourceready, [Italy Consumer Electronics Market Report 2026](https://www.sourceready.com/report/detail/italy-consumer-electronics-market-report-2026) | 2026-04-15 | low (aggregator report, no stated method or panel) |

The Sourceready figure is included only because it is the sole free country-level vendor-share number found. It puts Apple's *device* share (25–28%) well below Apple's *page-view* share (35%), which is the direction the StatCounter methodology caveat predicts. Do not use it as a load-bearing number.

---

## 2. Smartphone penetration in Italy

These five figures look contradictory until you read the base. They measure different populations and different things (owning a device vs. using one vs. reaching the internet through one). The base column is the important column.

| Figure | Base and metric | Source | Date | Confidence |
| --- | --- | --- | --- | --- |
| 91% own a smartphone | Population aged 6+, device ownership. Survey of 7,053 respondents representative of Italian residents aged 6+, run by SWG for AGCOM, 75% CAWI / 25% CATI, parents answering for ages 6–15 | AGCOM media-literacy report, [Principali Risultati](https://www.agcom.it/sites/default/files/documenti/rapporto/Principali%20Risultati%20Report%203%20%20luglio_.pdf); press coverage [AGI](https://www.agi.it/cronaca/news/2025-07-03/report-agcom-italiani-internet-dati-32166415/) | **fieldwork spring 2024**; presented 2025-07-03 | high (regulator primary source) — dated-but-usable, and note the fieldwork is over two years old even though the publication is recent |
| 95% of adults own a smartphone; 98% use it daily | Adults, device ownership | Deloitte Italy, [Digital Consumer Trends 2025](https://www.deloitte.com/it/it/Industries/tmt/perspectives/digital-consumer-trends-2025.html) | 2025 edition, exact fieldwork month not stated on the page | medium (reputable survey; undated fieldwork) |
| 90.3% are smartphone users | Population, usage (not ownership) | Censis, [L'informazione nel mirino](https://www.censis.it/linformazione-nel-mirino-2/) | published 2026-04-28, referring to 2025 | high |
| 79.1% access the internet via smartphone | Persons aged 6+, *channel of internet access* — not ownership | ISTAT, [Cittadini e ICT – Anno 2025](https://www.istat.it/comunicato-stampa/cittadini-e-ict-anno-2025/) | published 2026-04-22, referring to 2025 | high (national statistics office) |
| 93.0% of households reach the internet via smartphone; 51.6 million smartphones counted | *Households*, access channel; and absolute device count | Auditel Ricerca di Base, [Report Dotazioni](https://www.auditel.it/wp-content/uploads/2026/05/Report_Dotazioni_MM_6_1_2026.pdf) | fieldwork 2025-09-24 to 2026-03-11, published May 2026 | high |

**Working number for a consumer-app plan.** Roughly **90–95% of Italian adults own a smartphone**, and Auditel counts **51.6 million smartphones** in a population of 59.1 million. Smartphone penetration is not the constraint in Italy; it is effectively saturated. ISTAT's lower 79.1% is not a contradiction — it counts people who *reach the internet* through a smartphone, which excludes owners who use the device only for calls and messaging, a real group among the 65+ cohort.

One figure circulating in Italian marketing blogs — "97.9% of the population owns a smartphone" — is a misattribution. It comes from DataReportal/GWI, where the base is *internet users aged 16–64 who own each device type*, not the total population. Do not carry it forward as a population figure.

### 2.1 Population and connectivity context

| Metric | Value | Source | Date | Confidence |
| --- | --- | --- | --- | --- |
| Population of Italy | 59.1 million | DataReportal, [Digital 2026: Italy](https://datareportal.com/reports/digital-2026-italy) (UN data) | October 2025 | high |
| Median age | 48.2 years | DataReportal, same | October 2025 | high |
| Population aged 65+ | 25.1% | DataReportal, same | October 2025 | high |
| Internet users | 53.1 million (89.9% of population) | DataReportal, same (Kepios analysis) | October 2025 | high |
| Cellular mobile connections | 67.7 million (114% of population) | DataReportal, same (GSMA Intelligence) | October 2025 | high |
| Social media user identities | 41.2 million (69.7% of population) | DataReportal, same | October 2025 | high |
| Median mobile download speed | 85.39 Mbps | DataReportal, same (Ookla) | to August 2025 | high |
| Adults 18–74 browsing daily via mobile | 84.1% (88.2% among 18–24) | Casaleggio Associati / Audicom, [Ecommerce Italy 2026](https://www.ecommerceitalia.info/en/report-en/ecommerce-italy-2026/) | December 2025 measurement, published 2026-03-30 | medium |

The median age of 48.2 and the 25.1% aged 65+ are the two numbers most likely to be load-bearing for a consumer-app targeting decision in Italy. This is a considerably older population than the US or UK comparison markets.

---

## 3. Comparison rows: iOS share by market

All rows are StatCounter mobile OS page-view share, **July 2026**, so they are directly comparable to each other and carry the same methodology caveat as section 1.1. Italy, Germany, France and Spain were fetched live on 2026-08-13; the remaining rows were retrieved from the same canonical StatCounter URLs on 2026-08-12 and all report the same July 2026 period.

| Market | iOS | Android | URL | Confidence |
| --- | --- | --- | --- | --- |
| Italy | 35.13% | 64.86% | [/mobile/italy](https://gs.statcounter.com/os-market-share/mobile/italy) | high |
| United States | 59.58% | 40.39% | [/mobile/united-states-of-america](https://gs.statcounter.com/os-market-share/mobile/united-states-of-america) | high |
| Canada | 65.91% | 34.08% | [/mobile/canada](https://gs.statcounter.com/os-market-share/mobile/canada) | high |
| Australia | 63.70% | 36.29% | [/mobile/australia](https://gs.statcounter.com/os-market-share/mobile/australia) | high |
| United Kingdom | 53.92% | 46.07% | [/mobile/united-kingdom](https://gs.statcounter.com/os-market-share/mobile/united-kingdom) | high |
| France | 36.72% | 63.26% | [/mobile/france](https://gs.statcounter.com/os-market-share/mobile/france) | high |
| Spain | 33.02% | 66.96% | [/mobile/spain](https://gs.statcounter.com/os-market-share/mobile/spain) | high |
| Germany | 33.10% | 66.89% | [/mobile/germany](https://gs.statcounter.com/os-market-share/mobile/germany) | high |
| Europe (StatCounter region) | 39.54% | 60.44% | [/mobile/europe](https://gs.statcounter.com/os-market-share/mobile/europe) | high |
| Worldwide | 31.60% | 68.36% | [/mobile/worldwide](https://gs.statcounter.com/os-market-share/mobile/worldwide) | high |

**On "Western Europe average."** StatCounter does not publish a Western Europe region; its "Europe" region includes Eastern Europe and therefore is not the metric the calibration pack asked for. The 39.54% Europe row is labelled as what it is. Germany, France and Spain are given individually as a substitute: the four large Western European markets cluster at **33–37% iOS**, and Italy at 35.13% sits in the middle of that cluster. The UK at 53.92% is the Western European outlier and should not be averaged into a "Western Europe" figure without saying so.

**The decision-relevant gap.** Italy's iOS share (35%) is roughly **24 points below the US (60%)** and **31 points below Canada (66%)**. A consumer-app plan that was calibrated on US-style platform economics will systematically overestimate the reachable audience and the monetization potential of an iOS-first launch in Italy.

---

## 4. Store structure

### 4.1 Apple App Store, Italy

**Yes, Italy is a distinct storefront** with its own charts, its own editorial, and its own localized taxonomy. Verified directly at [apps.apple.com/it/charts/iphone](https://apps.apple.com/it/charts/iphone) on 2026-08-13 (confidence high).

Chart names as Apple writes them in Italian, each a separate ranked list: **Top app gratuite**, **Top app a pagamento**, **Top giochi gratuiti**, **Top giochi a pagamento**. Separate iPhone and iPad chart tabs. URL slugs are localized too (`/it/charts/iphone/app-gratuite/36` alongside the canonical `/it/charts/iphone/top-free-apps/36`).

Consumer app categories, exactly as Apple names them in Italian on the Italian storefront (retrieved 2026-08-13, confidence high):

Cibi e bevande, Consultazione, Economia, Finanza, Foto e video, Grafica e design, Intrattenimento, Istruzione, Libri, Medicina, Meteorologia, Musica, Navigazione, News, Produttività, Riviste e giornali, Salute e benessere, Shopping, Social network, Sport, Stili e tendenze, Sviluppatori, Utility, Viaggi.

Game categories: Avventura, Azione, Carte, Casinò, Casual, Corse, Famiglia, Giochi da tavolo, Giochi di parole, Giochi di ruolo, Infanzia, Musica, Rompicapo, Simulazione, Sport, Strategia, Trivia.

**Italy-specific ranking observations a solo developer can act on.** Snapshot of the live Italian iPhone charts, 2026-08-13 (confidence high, but note charts move daily):

- Top free: 1. Taccier (Zoretta S.r.l., an Italian publisher), 2. ChatGPT, 3. Poste Italiane, 4. Hoppy, 5. Klarna, 6. Temu.
- Top paid: 1. e-Connect (EL.MO. SPA — Italian alarm-system control), 2. TeleGuard, 3. Forest, 4. Veicolo+ info targa (Italian vehicle-plate lookup), 5. Blitzer.de PRO, 6. Osterie d'Italia 2025 (Slow Food Editore).

The pattern worth noting: the **free chart is dominated by global platforms plus Italian institutional apps** (Poste Italiane, and in the annual charts the public-services app IO), while the **paid chart is full of small, Italy-specific utilities** — vehicle plate lookup, an alarm-panel controller, a Slow Food restaurant guide, a speed-camera app. The paid chart in Italy is a materially lower bar than the free chart and is reachable by a domestic niche utility. That is the single most actionable structural observation here for a solo developer.

Apple's 2025 Italian year-end charts (source: [iSpazio](https://www.ispazio.net/2175830/classifiche-apple-app-piu-scaricate-italia-2025), 2025-12-11, reporting Apple's published lists, confidence medium):

- Top free iPhone 2025: ChatGPT, Poste Italiane, Klarna, Google Chrome, Temu, Threads, Google, Google Gemini, Remini, TikTok.
- Top paid iPhone 2025: e-Connect, Blitzer.de PRO, Threema, PeakFinder, Metronet, Shadowrocket, NightCap Camera, Veicolo Plus info targa, Procreate Pocket, 1Wallet.

Apple localizes these year-end charts to 30+ countries and surfaces them in the App Store's **Oggi** (Today) tab. Apple has stated publicly that apps are featured through "a combination of charts, algorithmic recommendations and expert-curated selections, all based on objective criteria" (Apple statement to Bloomberg, reported by [Macitynet](https://www.macitynet.it/apple-contro-musk/), 2025-08-13, confidence medium). Editorial slots include **App del giorno** and **Gioco del giorno** within the Oggi tab. No current quantified uplift figure for Italian featuring was found (see negative-result log).

### 4.2 Google Play, Italy

Verified more briefly (confidence medium, from direct fetch on 2026-08-13).

The Italian Play storefront is country-targeted and language-localized, but **the two are separate URL parameters and this trips people up**. Fetching `play.google.com/store/apps?hl=it&gl=IT` returns genuinely Italian-market content — Vinted, Immobiliare.it, 3BMeteo, Ilmeteo24, Notino, Back Market, Meteo & Radar — with Italian listing copy, PEGI age ratings, and the "Acquisti in-app" label. Fetching `play.google.com/store/apps/top?hl=it` *without* `gl=IT` returns US editorial content in a mix of Italian and English. `hl` sets the interface language; `gl` sets the country storefront. Any competitive-research or chart-scraping workflow for Italy must set `gl=IT`, or it will silently return US data.

Structure verified (2026-08-13, confidence high for what is listed): the store's top-level tabs on the Italian storefront are **Giochi**, **App**, **Libri** and **Bambini**. Category URLs use Google's English enum slugs with Italian display names — `play.google.com/store/apps/category/PRODUCTIVITY?hl=it&gl=IT` renders as **Produttività**. So unlike Apple, where the Italian storefront also localizes the URL slug, Play's category identifiers are language-neutral and only the rendered label is translated. The full Italian category label set is rendered client-side and was not captured; see the negative-result log.

### 4.3 EU regulatory context relevant to distribution

Kept short because it was not asked for, but it is Italy-relevant because Italy is an EU member state and the DMA applies.

Apple offers **alternative business terms for apps in the EU**, giving developers the option of distribution through alternative app marketplaces or a developer's own website, and alternative payment processing (source: Apple, [Update on apps distributed in the European Union](https://developer.apple.com/support/dma-and-apps-in-the-eu/), undated support page, confidence high for the terms themselves).

Two points for a solo developer:

1. Neither alternative-distribution route is realistically open to a solo developer. Web distribution requires two continuous years of Apple Developer Program membership *and* an app with more than one million first annual installs in the EU in the prior calendar year. Operating a marketplace additionally requires an EU-incorporated entity plus either that same install record or a €1,000,000 stand-by letter of credit (source: Apple, [alternative app marketplace in the EU](https://developer.apple.com/support/alternative-app-marketplace-in-the-eu), confidence high).
2. The **Core Technology Fee** (€0.50 per first annual install above one million per year, with a three-year free on-ramp for developers under €10M global revenue) applies only to developers who adopt the alternative terms. Apple **announced a plan** to move the EU to a single business model and transition from the CTF to a **Core Technology Commission** by 1 January 2026, stating that "additional details regarding this transition will be provided at a later date" (source: Apple, [Updates for apps in the European Union](https://developer.apple.com/news/?id=awedznci), 2025-06-26, confidence high for the announcement). **This is the announced plan with its stated effective date; whether the transition completed as described was not verified in this pass** (see negative-result log).

Net effect for the target user: a solo developer publishing to the Italian App Store on Apple's standard terms is unaffected by all of the above.

---

## 5. Consumer and app-economy spend in Italy

The best available Italy-level figure is Apple's own commissioned study. Note carefully that this measures **billings and sales facilitated by the App Store ecosystem**, which is a much broader quantity than consumer in-app spend — most of it is physical goods and services bought through apps, on which Apple takes no commission and from which an app developer earns nothing directly.

Estimated billings and sales facilitated by the App Store ecosystem, Italy, 2024. The structure is **hierarchical, not additive**: the m-commerce lines sit *inside* Physical Goods and Services.

| Line | Italy, 2024 (USD bn) |
| --- | --- |
| Digital goods and services | 1.0 |
| Physical goods and services | 4.4 |
| — of which General Retail | 1.6 |
| — of which Travel | 1.7 |
| — of which Food Delivery and Pickup | 0.3 |
| — of which Grocery | 0.6 |
| — of which Ride Hailing | 0.1 |
| In-app advertising | 1.3 |
| **Total** | **6.7** |

Source: Apple / Analysis Group, [The Global App Store and Its Growth](https://www.apple.com/newsroom/pdfs/2024-Apple-Global-Ecosystem-Report-June2025.pdf), Table 4, study by Prof. Andrey Fradkin (Boston University Questrom) and Dr. Jessica Burley (Analysis Group), published 2025-06-05 for calendar year 2024. Confidence high for the figures as published; note this is a vendor-commissioned study. Dated-but-usable (14 months old at research date).

**The number a developer should actually care about is the $1.0bn digital goods and services line**, not the $6.7bn headline. Several Italian press reports ([StartupItalia](https://startupitalia.eu/startup/app-economy-mercato-in-crescita-mega-app/), 2025-10-01; [ANSA](https://www.ansa.it/canale_tecnologia/notizie/software_app/2025/06/05/app-store-in-italia-giro-daffari-da-67-mld-di-dollari_b7cbb91a-521b-4952-be5c-27ebb59d559c.html), 2025-06-05) flatten the hierarchy and present Travel and Retail as siblings of the $4.4bn rather than components of it; their component lists do not sum to the total. Cite the Apple PDF table, not the press.

For scale, Europe as a whole accounted for $148bn of the global $1.3tn in 2024, and within Europe the UK was the largest at $55.1bn, ahead of Germany $21.5bn, France $12.6bn, Italy $6.7bn and Spain $5.9bn (same source, Tables 3 and 4, confidence high). **Italy is the fourth-largest App Store economy in Western Europe and is roughly one eighth the size of the UK.**

### 5.1 Global context (no Italy split available)

| Metric | Value | Source | Date | Confidence |
| --- | --- | --- | --- | --- |
| Global in-app purchase revenue, iOS + Google Play, 2025 | $167bn, +10% YoY; non-gaming IAP surpassed games for the first time | Sensor Tower, [State of Mobile 2026 press release](https://sensortower.com/press/press-release-boosted-by-gen-ai-services-consumers-spent-more-money-in-apps-than-games-for-first-time) | published 2026-01-21 for CY2025 | high |
| Global app installs, 2025 | 106.9bn, −2.7% YoY (fifth consecutive annual decline) | Appfigures annual report, reported by [Everyeye](https://tech.everyeye.it/notizie/app-scaricate-guadagni-record-cosa-succedendo-853567.html) | 2026-01-19 for CY2025 | medium |
| Europe IAP revenue growth, 2024 | +24% YoY, roughly double the global rate, with strong growth in the UK, Germany, France and Italy | Sensor Tower, [2025 State of Mobile](https://sensortower.com/blog/2025-state-of-mobile-consumers-usd150-billion-spent-on-mobile-highlights) | for CY2024 | medium (Italy named, but no Italy value published) — dated-but-usable |

The structural signal across both sources is consistent and relevant to a consumer-app plan: **downloads are flat-to-declining while consumer spend rises**, meaning monetization of existing users, not install volume, is where the growth is. Sensor Tower attributes the 2025 step-change largely to generative-AI subscriptions, with ChatGPT the third-highest-grossing app globally.

---

## Does not exist publicly (negative-result log)

Every sub-question or cross-check that could not be sourced in this pass.

1. **An independent, non-StatCounter measurement of the Italian iOS/Android split.** Checked and not found in any of the following. **AGCOM**: the full media-literacy report was read; its device chapter enumerates ownership by device *type* (smartphone, smart TV, laptop, tablet, console, virtual assistant) and never asks which operating system. **Deloitte** Digital Consumer Trends Italy 2025: the public summary covers smartphone ownership, device age, 5G share and streaming, with no iPhone-vs-Android split (the full PDF was not opened and may contain one). **Comscore**: no free Italian OS-share release found. **Kantar** Worldpanel ComTech no longer publishes free Italian OS-share data. **Counterpoint and IDC** publish global and regional smartphone shipment shares but no free Italy country split; their Italy-level data sits behind the paid Market Monitor. **Statista's** Italian OS-share series is itself sourced from StatCounter, so it is not an independent check, and its values are paywalled regardless — including "Most common smartphone operating systems in Italy 2024", which is survey-based via Statista Consumer Insights and would have been a genuine cross-check had it been readable. **Consequence: every OS-share figure in this report traces to a single measurement method, page-view tracking, which the section 1.1 caveat notes runs iOS-high. The 35% iOS figure should be treated as unconfirmed by any ownership-based survey.**
2. **"Western Europe average" as a published region.** StatCounter has no Western Europe region; its "Europe" region includes Eastern Europe. Germany, France and Spain are given individually as a substitute. If the calibration pack needs a single Western Europe number, it will have to be constructed and labelled as constructed.
3. **Values behind Statista paywalls.** "Apple iOS market share in Italy 2016–2025", "Android OS market share in Italy 2017–2025", "Leading mobile device vendors in Italy 2016–2024", "Most common smartphone operating systems in Italy 2024" (Statista Consumer Insights, survey-based, which would have been a genuinely independent cross-check) — all list the series and date but withhold the numbers.
4. **Italy-level consumer in-app purchase spend from Sensor Tower, data.ai or an equivalent panel.** Sensor Tower publishes global and regional IAP totals and Italy-level *app-by-app* download and revenue snapshots for individual categories, but no Italy country total for consumer spend was found free. Apple's $1.0bn digital goods and services figure is the closest available proxy and is a different metric measured a different way.
5. **A current quantified uplift from App Store editorial featuring, for Italy or generally.** The only quantified figure found is a Sensor Tower estimate reported in 2018 (App of the Day / Game of the Day associated with up to ~685–800% download uplift in the following week, thematic lists 222–240%). At eight years old and predating multiple App Store redesigns, it is too stale to use even as a planning range and is recorded here only so the gap is visible.
6. **Whether Apple's announced CTF-to-CTC transition completed on 1 January 2026 as planned.** Apple's developer pages still carry the forward-looking language ("Apple plans to move", "details will be provided at a later date"). No post-January-2026 confirmation was found. Treat the CTC as announced, not confirmed in force.
7. **The full Google Play Italian category label set, and Play's Italy chart structure.** The Italian storefront was confirmed country-targeted and localized, the four top-level tabs were captured, and the slug-vs-label pattern was confirmed. But Play renders its category list client-side, so server-fetched HTML returns only the categories a given page happens to link to; enumerating the full set would need a headless browser rather than a fetch. Play's ranked charts were likewise not examined at the depth done for the App Store. This is a gap in coverage rather than an absence of public data.
8. **Italian App Store price points and VAT treatment.** Not verified against a primary source in this pass. Apple states its commerce system supports 40+ local currencies and handles tax in nearly 200 regions, but the specific Italian price-tier structure and the applicable Italian VAT rate on App Store sales were not confirmed.
9. **Italy-specific App Store featuring or ranking mechanics beyond what Apple states publicly.** Apple describes featuring as charts plus algorithmic recommendation plus editorial curation, but publishes no Italy-specific criteria, no Italian editorial calendar, and no route for a developer to pitch the Italian editorial team distinct from the global App Store submission form.
10. **Figures deliberately excluded as unusable.** Politecnico di Milano Osservatori put Italian consumer mobile-app spend at ~€300M — but that is 2015 data, now eleven years old, and is obsolete rather than dated-but-usable. Transpire Insight's "Italy Mobile Application Market, USD 244.61 million in 2025" disagrees with Apple's Italy digital-goods figure by roughly a factor of four and with the $6.7bn ecosystem figure by more than an order of magnitude; with no stated methodology reconciling the scope difference, it is not usable at any confidence level.

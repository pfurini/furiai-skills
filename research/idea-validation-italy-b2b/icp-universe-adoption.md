# Italian PMI ICP universe and digital adoption — raw research report (2026-08-13)

Scope: sizing inputs for indie founders selling self-serve micro-SaaS to Italian micro
and small businesses, including regulated professional firms. Every figure carries
source URL, publication date, and reference year. `[OLD]` marks anything published
more than 12 months before 2026-08-13.

---

## HEADLINE CAVEATS — read before using any number below

**1. The ICT adoption data cannot answer "do micro firms buy SaaS."** ISTAT's
`Imprese e ICT` survey and the Eurostat `isoc_e_*` tables it feeds have a **10+
employee sample frame**. Firms under 10 addetti — 94.8% of the Italian enterprise
universe — are structurally outside it. DESI / Digital Decade indicators inherit the
same base. Every adoption row in section 3 is labelled with its employee-size base.
Where a source genuinely covers micro firms it is marked **[MICRO-INCLUSIVE]**; there
are only three such sources in this report.

**2. Four different "how many" counts appear below and must not be merged.** ASIA
active enterprises (4.51M, ISTAT), Registro Imprese registered firms (5.82M,
Unioncamere), new partita IVA openings (500K/yr — a *flow*, not a stock, MEF), and
self-employed people (5.28M, ISTAT labour force survey) are different populations
measured by different bodies on different definitions, and two of them count people
rather than businesses. Adding or cross-comparing them will double-count.

**3. A figure in the research brief was misdated.** The "~69,000 studi / 290,000+
addetti" commercialisti figure is **not** a 2026 figure. It traces to the CNDCEC
Stati Generali of **7 May 2024** and has not been restated since. See section 2.

**4. Classification break.** ATECO 2025 (NACE Rev 2.1) took effect 1 Jan 2025.
Movimprese data from Q1 2026 and partita IVA openings from 2025 use ATECO 2025; ASIA
2023 and everything earlier uses ATECO 2007 agg. 2022. Sector comparisons across that
boundary are invalid.

---

## 1. ENTERPRISE UNIVERSE

### 1.1 ASIA active enterprises by size class — the primary sizing base

Latest ASIA reference year is **2023**. The size-class cross-tab below is from the
ISTAT `Conti economici delle imprese e dei gruppi d'impresa` report (Frame SBS /
ASIA), the freshest authoritative publication of this table.

| Size class (addetti) | Enterprises | Addetti | Employees | Turnover (€m) | Value added (€m) | VA/head (€k) |
|---|---:|---:|---:|---:|---:|---:|
| 0–9 (micro) | 4,273,161 | 7,465,484 | 3,029,903 | 913,183 | 287,524 | 38.5 |
| 10–19 | 144,457 | 1,902,136 | 1,721,006 | 389,134 | 103,739 | 54.5 |
| 20–49 | 60,665 | 1,795,277 | 1,725,877 | 472,111 | 116,107 | 64.7 |
| 50–249 (medium) | 25,943 | 2,524,493 | 2,495,339 | 841,673 | 194,143 | 76.9 |
| 250+ | 4,565 | 4,418,650 | 4,414,299 | 1,480,576 | 372,053 | 84.2 |
| **Total** | **4,508,791** | **18,106,040** | **13,386,424** | **4,096,677** | **1,073,565** | **59.3** |

Source: ISTAT, `Conti economici delle imprese e dei gruppi di impresa | Anno 2023`,
published **15 October 2025**, reference year **2023**.
https://www.istat.it/wp-content/uploads/2025/10/Report-Conti-economici-imprese-e-gruppi_2023.pdf
Confidence: **high** (authoritative primary, EU-regulated register).

Derived ICP bands (arithmetic on the rows above, not separately published):

| Band | Enterprises | Share of total |
|---|---:|---:|
| Micro (0–9) | 4,273,161 | 94.77% |
| Small (10–49) | 205,122 | 4.55% |
| **Core ICP (0–49)** | **4,478,283** | **99.32%** |
| Medium (50–249, edge scope) | 25,943 | 0.58% |
| Large (250+, out of scope) | 4,565 | 0.10% |

**Coverage exclusions — state these whenever the 4.51M number is used.** ISTAT's own
English edition defines the scope verbatim as "Nace Rev. 2 sections B to S with the
exception of sections K and O and division 94". So the 4.51M **excludes**:

- section **A** (agriculture, forestry, fishing) — outside the B–S range;
- section **K** (financial and insurance activities) — **116,685 enterprises in
  Italy in 2023**, of which 114,380 micro, verified separately via Eurostat;
- section **O** (public administration);
- **division 94** (membership organisations);
- sections T and U.

An "all Italian businesses" claim built on this number is wrong by the size of
agriculture plus the entire financial and insurance sector. The K exclusion matters
for this ICP specifically: insurance agents and financial intermediaries are a
plausible micro-SaaS segment and they are **not** in the 4.51M.

Source for the scope statement: ISTAT, `Structural business statistics: enterprises
and enterprise groups – Year 2023` (English edition of the same release), published
**15 October 2025**.
https://www.istat.it/en/press-release/structural-business-statistics-enterprises-and-enterprise-groups-year-2023/
https://www.istat.it/wp-content/uploads/2025/10/EN-SBS_enterprise_and_enterprise_groups_2023_EL-10_10.pdf

ISTAT's own size-class definitions, verbatim from the report glossary:
> "Microimprese: da 0 a 9 addetti / Piccole imprese: da 10 a 49 addetti ... /
> Medie imprese: da 50 a 249 addetti / Grandi imprese: 250 addetti e oltre"
> ("Micro-enterprises: 0 to 9 addetti / Small enterprises: 10 to 49 addetti ... /
> Medium: 50 to 249 addetti / Large: 250 addetti and over")

Note on `addetti`: this counts *positions*, employed and self-employed, as an annual
average — it includes the working owner. A one-person partita IVA registers as 1
addetto, not 0. The 0–9 class is therefore dominated by genuine one- and two-person
businesses: 7.47M addetti across 4.27M micro firms is an average of 1.75 addetti per
firm, and only 3.03M of those 7.47M are employees.

### 1.2 Enterprises by ATECO/NACE section and size class — full cross-tab

ISTAT publishes this only as downloadable xlsx and in IstatData. **Eurostat carries
the identical data on a queryable API**, and the section sums reconcile to the ISTAT
headline exactly — see the validation note below. Reference year **2023**, same as
ASIA.

| NACE section | 0–9 | 10–19 | 20–49 | 50–249 | 250+ | Total | Micro % | **0–49 (core ICP)** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| G Wholesale & retail trade, vehicle repair | 968,423 | 27,195 | 9,677 | 3,513 | 625 | 1,009,433 | 95.9% | **1,005,295** |
| M Professional, scientific & technical | 894,505 | 6,664 | 2,271 | 1,089 | 200 | 904,729 | 98.9% | **903,440** |
| F Construction | 504,341 | 19,834 | 6,788 | 1,865 | 129 | 532,957 | 94.6% | **530,963** |
| Q Human health & social work | 354,336 | 4,110 | 2,398 | 1,607 | 390 | 362,841 | 97.7% | **360,844** |
| C Manufacturing | 284,161 | 37,408 | 19,783 | 9,516 | 1,578 | 352,446 | 80.6% | **341,352** |
| I Accommodation & food service | 297,969 | 23,562 | 6,322 | 1,421 | 177 | 329,451 | 90.4% | **327,853** |
| L Real estate | 226,694 | 622 | 151 | 55 | 5 | 227,527 | 99.6% | **227,467** |
| S96 Other personal services | 196,219 | 2,205 | 708 | 257 | 20 | 199,409 | 98.4% | **199,132** |
| N Administrative & support services | 163,368 | 6,333 | 3,615 | 2,081 | 540 | 175,937 | 92.9% | **173,316** |
| J Information & communication | 111,214 | 4,000 | 1,908 | 1,113 | 224 | 118,459 | 93.9% | **117,122** |
| H Transportation & storage | 102,116 | 7,555 | 4,504 | 2,203 | 429 | 116,807 | 87.4% | **114,175** |
| R Arts, entertainment & recreation | 83,253 | 1,503 | 682 | 235 | 36 | 85,709 | 97.1% | **85,438** |
| P Education | 45,406 | 1,353 | 761 | 296 | 17 | 47,833 | 94.9% | **47,520** |
| S95 Repair of computers & household goods | 23,692 | 317 | 93 | 20 | 0 | 24,122 | 98.2% | **24,102** |
| D Electricity, gas, steam, AC | 9,536 | 242 | 179 | 103 | 42 | 10,102 | 94.4% | 9,957 |
| E Water, sewerage, waste | 6,766 | 1,310 | 712 | 521 | 151 | 9,460 | 71.5% | 8,788 |
| B Mining & quarrying | 1,162 | 244 | 113 | 48 | 2 | 1,569 | 74.1% | 1,519 |
| **Total (B–S excl. K, O, div. 94)** | **4,273,161** | **144,457** | **60,665** | **25,943** | **4,565** | **4,508,791** | **94.77%** | **4,478,283** |
| *K Financial & insurance (excluded above)* | *114,380* | — | — | — | — | *116,685* | *98.0%* | — |

Source: Eurostat, dataset `sbs_sc_ovw` (`Enterprise statistics by size class and NACE
Rev. 2 activity, from 2021 onwards`), indicator `ENT_NR`, geo `IT`, time `2023`.
Dataset last updated **10 March 2026**, reference year **2023**.
Retrieved via the Eurostat dissemination API on 2026-08-13:
`https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sbs_sc_ovw?format=JSON&geo=IT&indic_sbs=ENT_NR&time=2023`
Browser: https://ec.europa.eu/eurostat/databrowser/view/sbs_sc_ovw/default/table?lang=en
Confidence: **high**.

**Validation.** Summing the 17 sections above gives 4,273,161 micro and 4,508,791
total — **identical, to the unit, to the ISTAT ASIA 2023 headline** in section 1.1,
which was sourced independently from the ISTAT PDF. Eurostat SBS for Italy *is* the
ASIA register, and the reconciliation also confirms that section K is excluded from
the published total (adding K's 116,685 would break the match).

**Reading for ICP selection.** Section M — professional, scientific and technical
activities, which contains the commercialisti, avvocati and consulenti del lavoro
studi — is the **second-largest section at 904,729 enterprises and the most
micro-concentrated of the large sections at 98.9%**. It is also the fastest-growing
section in the current demography data (+1.59% in Q2 2026, section 4). Four sections
(G, M, F, Q) account for 2.81M of the 4.48M core-ICP firms, 63%.

Note that section M is much larger than the regulated-professional headcount in
section 2 (~379,000 practitioners): it also contains engineers, architects,
consultants, designers, advertising, and veterinary practices.

Macro-sector aggregation as published in prose by ISTAT, reference year 2023:

| Macro-sector | Share of active enterprises | Share of addetti | Share of value added |
|---|---:|---:|---:|
| Services (market) | ~80% | 67.5% | 55.7% |
| Construction (F) | 11.8% | 9.0% | 9.0% |
| Industry in the narrow sense (B–E) | 8.3% | 23.5% | 35.3% |

Source: ISTAT Conti economici 2023 (as above), published 15 Oct 2025. Confidence: **high**.

ISTAT's own xlsx tables, if the section-level economic aggregates (not just counts)
are needed, are attached to `Registro statistico delle imprese attive – Anno 2023`
(published 9 July 2025 `[OLD]`) and in IstatData
(https://esploradati.istat.it/databrowser/#/it → Imprese → Struttura).

For a *registered-firm* sector split (different universe — see 1.5), Movimprese in
section 4 gives per-section quarterly movements.

### 1.3 Partite IVA — a FLOW, not a stock

The MEF Osservatorio publishes **new openings only**. There is no published stock of
active partite IVA in this source. Treating 500,341 as a market size is a category
error.

| Metric | Value | Reference year |
|---|---:|---|
| New partita IVA openings | 500,341 (+0.4% vs 2024) | 2025 |
| — by natural persons | 68.5% | 2025 |
| — by società di capitali | 25.1% (+2.6%) | 2025 |
| — by società di persone | 3.0% (−7.4%) | 2025 |
| — non-resident / other | 3.4% (−23.2%) | 2025 |
| Adopting the *regime forfetario* | 242,529 = 48.5% of openings (+3.9%) | 2025 |
| Top sector for new openings | Professional activities, 16.6% | 2025 |
| — then commerce | 16.0% | 2025 |
| — then construction | 9.6% | 2025 |
| Openings by under-35s | 50.2% of natural-person openings | 2025 |

Source: MEF Dipartimento delle Finanze, `Osservatorio sulle partite IVA – sintesi dei
dati anno 2025`, published **12 February 2026**, reference year 2025.
https://www.finanze.gov.it/it/archivi/notizie/dettaglio-notizie/Osservatorio-sulle-partite-IVA-sintesi-dei-dati-anno-2025-00001/
PDF: https://www1.finanze.gov.it/finanze/osiva/public/contenuti/Sintesi_annuale_dati_2025.pdf
Confidence: **high**.

The *regime forfetario* share matters for pricing: nearly half of all new
Italian businesses start on a flat-rate tax regime with a turnover ceiling, which
caps both their willingness and their accounting need to pay for software.

### 1.4 Lavoratori autonomi / occupati indipendenti — a population of PEOPLE

This comes from the ISTAT labour force survey and counts *people*, not businesses. It
overlaps both populations above and must not be added to either.

| Metric | Value | Reference |
|---|---:|---|
| **Occupati indipendenti (self-employed)** | **5,277,000** (−44k m/m, flat y/y) | June 2026 |
| Total employed | 24,310,000 | June 2026 |
| Employees, permanent | 16,491,000 | June 2026 |
| Employees, fixed-term | 2,542,000 | June 2026 |
| Self-employed share of total employment | 21.7% (derived) | June 2026 |

ISTAT's definition, verbatim:
> "Occupati indipendenti: coloro che svolgono la propria attività lavorativa senza
> vincoli formali di subordinazione. Sono compresi: imprenditori; liberi
> professionisti, lavoratori autonomi, coadiuvanti nell'azienda di un familiare ...,
> soci di cooperativa."

> ("Independent workers: those who carry out their work without formal ties of
> subordination. Included are: entrepreneurs; self-employed professionals, autonomous
> workers, family-business assistants ..., cooperative members.")

Source: ISTAT, `Occupati e disoccupati (dati provvisori) – Giugno 2026`, published
**30 July 2026**, reference month June 2026.
https://www.istat.it/comunicato-stampa/occupati-e-disoccupati-dati-provvisori-giugno-2026/
PDF: https://www.istat.it/wp-content/uploads/2026/07/CS_Occupati-e-disoccupati_GIUGNO_2026.pdf
Confidence: **high** (primary, monthly, though flagged provisional by ISTAT).

Sense-check against the enterprise register: 5.28M self-employed people against 4.27M
micro enterprises with 7.47M addetti of which only 3.03M are employees — so roughly
4.4M of the micro sector's addetti are non-employee positions. The two sources are
consistent in order of magnitude, but they count different things (people vs
positions vs legal entities) and the residuals should not be treated as precise.

### 1.5 Registered firms (Registro Imprese) — a fourth, larger universe

5,823,863 registered firms at 30 June 2026 (Unioncamere/InfoCamere). This counts
*registrations* at the Chambers of Commerce, includes dormant entities, and is
roughly 1.3M higher than ASIA's active-enterprise count. Full detail in section 4.

---

## 2. PROFESSIONAL-FIRM UNIVERSE

### 2.1 Commercialisti (chartered accountants / tax advisers)

**Practitioner count — current.** Iscritti all'Albo at 31 December 2025: **119,050**
(−902, −0.8% on 2024). New registrations 1,494 in 2025, down 27.3% from 1,958 in
2024. Praticanti (trainees) 11,507 (+4.2%). Average professional income €87,3xx
(+8.3% nominal; first year above the 2007 real level). 132 territorial Ordini.

Source: CNDCEC / Fondazione Nazionale di Ricerca dei Commercialisti,
`Rapporto 2026 sull'Albo dei Dottori Commercialisti e degli Esperti Contabili`
(XIX edition), published **16 July 2026**, reference year 2025.
https://www.fondazionenazionalecommercialisti.it/node/1911
Corroborated: https://www.ipsoa.it/documents/quotidiano/2026/07/17/commercialisti-rapporto-2026-professione
Confidence: **high** (primary body, multi-source corroboration).

**Firm count — DATED, and the brief's date was wrong.** The 69,210 studi / ~297,000
addetti figure comes from the CNDCEC **Stati Generali of 7 May 2024** `[OLD]`, when
iscritti stood at 120,424. It is **not** a 2026 figure, and no restatement has been
published since. Verbatim from the CNDCEC's own social channel:

> "I Commercialisti iscritti all'Albo sono 120.424. Svolgono la libera professione
> nell'ambito di 69.210 studi professionali dislocati su tutto il territorio
> nazionale, nell'ambito dei quali sono occupati circa 297mila addetti, tra
> professionisti, collaboratori, dipendenti e praticanti che concorrono alla
> creazione di valore aggiunto nazionale in misura pari allo 0,9% del PIL."

> ("Commercialisti registered with the Albo number 120,424. They practise within
> 69,210 professional firms distributed across the national territory, employing
> around 297,000 addetti — professionals, collaborators, employees and trainees —
> contributing to national value added in the amount of 0.9% of GDP.")

Source: CNDCEC official Facebook post, **7 May 2024**, reference year 2024.
https://www.facebook.com/consigliocommercialisti/posts/757639213213913/
Press coverage of the same release:
https://www.teleborsa.it/News/2024/05/07/commercialisti-a-roma-gli-stati-generali-oltre-69-mila-studi-piu-di-290mila-addetti-creato-quasi-1percent-pil-115.html
https://press-magazine.it/commercialisti-oltre-69-mila-studi-piu-di-290mila-addetti-quasi-l1-del-pil-creato/
Confidence: **medium**. The number originates with CNDCEC but I could not locate it
on a `commercialisti.it` or `fondazionenazionalecommercialisti.it` page — only on the
CNDCEC's own social post and press reproductions of the event.

Also from that release, useful as a channel/reach anchor (2024, `[OLD]`):
- ~5.8M taxpayers (self-employed, sole traders, partnerships, professional
  associations, companies, non-commercial bodies) file via Entratel; **4.35M of them
  (75%) file through a commercialista's studio**.
- 77% of statutory-auditor posts in Italian società di capitali are held by
  commercialisti (90% among the top 100,000 companies by turnover).

**Firm structure — this is the best ICP-shaping data in the report.** A 2025 FNC
study with the Universities of Bergamo, Politecnica delle Marche and LUM:

| Practice form | 2018 | 2025 |
|---|---:|---:|
| Any aggregated form (associated, corporate, shared, other) | 38.5% | **51.6%** |
| — studio associato or STP | 21.9% | 29.4% |
| — of which studio associato | 19.7% | 22.7% |
| — of which STP | 2.2% | 6.7% |
| Shared studio (costs/means shared, formally individual) | 14.0% | 20.2% |
| Exclusively individual studio | 61.4% | **48.4%** |
| Single-addetto studios | 29.5% | 25.0% |
| Studios with >10 addetti | 11.2% | **18.9%** |

Source: FNC/CNDCEC research presented at the Congresso Nazionale, Genoa, reported
**23–24 October 2025**, reference year 2025.
https://www.ipsoa.it/documents/quotidiano/2025/10/23/commercialisti-aggregazioni-professionali-51-6
Confidence: **medium** (single authoritative source; primary FNC page for this
specific study not located — reported via IPSOA).

Read for sizing: the addressable "firm with a buying decision and more than one seat"
segment is growing fast, but half the profession is still a solo practitioner, and a
quarter is literally one person.

### 2.2 Avvocati (lawyers)

| Metric | Value | Reference year |
|---|---:|---|
| Registered with Cassa Forense | **228,641** | 2025 |
| — active | 211,464 | 2025 |
| — contributing pensioners | 17,177 | 2025 |
| Società tra avvocati (STA) | **542** (up from 310 in 2022) | 2025 |
| Registered with Cassa Forense | 233,260 (−1.6%) | 2024 |
| — active | 216,884 | 2024 |
| Peak registration | 245,030 | 2020 |
| Average income | €47,678 (+6.8%) | 2024 |
| — men / women | €62,456 / €31,115 | 2024 |
| — Lombardy / Calabria | €81,115 / €24,203 | 2024 |
| Average age | 48.9 (from 42.3 in 2002) | 2024 |

2025/2026 figures: Cassa Forense 2025 financial statements and the
`X Rapporto sull'Avvocatura 2026` (Censis/Cassa Forense), presented **29 April 2026**,
reference year 2025. https://www.censis.it/x-rapporto-sullavvocatura-2026/
Reported: https://www.milanofinanza.it/news/cassa-forense-archivia-il-2025-con-un-utile-da-1-33-miliardi-patrimonio-oltre-quota-20-miliardi-202605041115522398
2024 figures: `Rapporto sull'Avvocatura 2025` (IX edition), published **April 2025**
`[OLD]`, reference year 2024.
https://www.cassaforense.it/media/munf4vli/rapporto-avvocatura-2025.pdf
Confidence: **high** for registration counts, **medium** for the 542 STA figure
(reported via Milano Finanza from the Cassa's own presentation, not read on a Cassa
Forense page).

**The 9.8% studi associati share — VERIFIED, with an important qualification.**
Verbatim from the Rapporto 2025 (p. 17):

> "Inoltre, il 9,8% degli avvocati si dichiara membro di uno studio associato, Sta o
> Stp."

> ("Furthermore, 9.8% of lawyers declare themselves a member of an associated
> practice, STA or STP.")

The qualification: this is a **survey self-report from ~28,000 respondents**, not a
register count, and it is a share of *lawyers*, not of *firms*. The full breakdown:

| Practice type | Share of lawyers | Under 40 | Over 64 |
|---|---:|---:|---:|
| Sole practitioner (studio monopersonale) | **64.0%** | 38.8% | 66.9% |
| Collaborator (≥80% of activity) | 10.4% | 28.7% | 1.5% |
| Practice owner with collaborators | 10.1% | 4.1% | 17.8% |
| Member of studio associato / STA / STP | **9.8%** | 10.1% | 13.1% |
| Exclusive-collaboration (single client) | 5.7% | 18.3% | 0.7% |

Source: Censis survey for Cassa Forense, fieldwork January 2025, ~28,000 respondents,
published April 2025 `[OLD]`. Confidence: **high** (verbatim from primary PDF), but
note it is self-reported and lawyer-weighted, not firm-weighted.

Space-sharing is far more common than legal aggregation: 61.0% share premises with
other lawyers or professionals, 28.1% as rent-paying contributors, 3.0% in coworking;
34.2% share nothing, and 8.7% work primarily from home.

### 2.3 Consulenti del lavoro (labour/payroll consultants)

| Metric | Value | Reference year |
|---|---:|---|
| Registered with the Ordine at 31 Dec | **26,102** (47% women) | 2025 |
| Registered with ENPACL at 31 Dec | 26,091 | 2024 |
| STP registered with ENPACL | **797** (from 106 in 2015, +650%) | 2024 |
| Category VAT turnover declared | €2.73bn (+5.5%) | 2023 income yr |
| Average per-head turnover | €107,000 | 2023 income yr |
| Average professional income | €56,000 | 2023 income yr |
| — in an STP | €143,800 income / €269,000 turnover | 2024 |
| — studio associato | €180,000 turnover | 2024 |
| — sole practitioner | €40,800 income / €71,700 turnover | 2024 |

Sources: ENPACL 2025 financial statements, approved and reported **7 May 2026**,
reference year 2025.
https://www.ipsoa.it/documents/quotidiano/2026/05/08/bilancio-2025-enpacl-crescono-ricavi-patrimonio-redditi-categoria
ENPACL 2024 statements, reported **1 May 2025**, reference year 2024.
https://www.ipsoa.it/documents/quotidiano/2025/05/02/enpacl-bilancio-approvato-numeri-crescita
STP series: https://www.fiscoetasse.com/new-rassegna-stampa/2207-consulenti-del-lavoro-boom-fatturati-e-redditi-nelle-stp.html
Confidence: **medium** (ENPACL is the authoritative source but every figure here was
read via IPSOA/FiscoeTasse reporting of the Assembly, not on an enpacl.it page).

**Reach into the PMI base** — the single most useful stat for a channel strategy,
but dated `[OLD]`. From the Ufficio Studi dei Consulenti del Lavoro research presented
at the Stati Generali, January 2024:
- ~26,500 registered consultants (2024).
- **"quasi l'80% delle aziende private si avvale delle loro prestazioni"** ("nearly
  80% of private companies use their services").
- ~8.5M employment relationships administered in their studios; **over 1.8M businesses
  assisted**; >10M citizens served.
- 53.4% of business owners have used the same consultant for over 10 years; 45.6% for
  over 15. 92.8% rate the service highly or very highly.
- Demand for professional services over the prior 5 years: 27.6% of firms say it rose,
  60.8% stable, 11.6% fell.

Source: Consiglio Nazionale dell'Ordine dei Consulenti del Lavoro / Fondazione Studi,
`La professione di Consulente del Lavoro nello scenario di mercato che cambia`,
presented **11 January 2024** `[OLD]`, reference year 2023/2024.
https://www.ipsoa.it/documents/quotidiano/2024/01/12/rapporto-professione-numeri-consulenti-lavoro
https://www.adepp.info/2024/01/l80-delle-aziende-private-si-avvale-del-consulente-del-lavoro/
Confidence: **medium** (single study, self-reported by the profession's own research
office, now 2.5 years old).

The 10+ year client tenure and 92.8% satisfaction are a *displacement warning*, not an
opportunity signal: this is an entrenched intermediary layer.

### 2.4 Notai (notaries)

| Metric | Value | Reference date |
|---|---:|---|
| Notaries in service | **5,238** (3,133 men, 2,105 women) | 1 Jan 2026 |
| Average age / average seniority | 52 years / 19 years | 1 Jan 2026 |
| New appointments, last 5 years | 672 (average entry age 35) | 2021–2026 |
| Notaries in service | 5,072 | Oct 2024 `[OLD]` |
| Notarial acts recorded | 3,795,090 (+2% on 2024) | 2025 |

Sources: Cassa Nazionale del Notariato memorandum to the parliamentary pensions
committee, reported **2 July 2026**, reference date 1 Jan 2026.
https://www.ansa.it/sito/notizie/casse_previdenza/2026/07/02/cassa-del-notariato-5.238-iscritti-3.133-uomini-e-2.105-donne_59cd6e0e-c782-4d4c-8414-ed6e8939f194.html
Acts: Consiglio Nazionale del Notariato, `Dati Statistici Notarili — Analisi 2025`,
reference year 2025. https://dsn.notariato.it/dsn/contenuti/analisi/2025/DSN_ANALISI_2025_Dati_generali.pdf
Confidence: **medium-high** (Cassa figure is primary but read via ANSA; the DSN acts
figure is primary).

**This market is statutorily capped and cannot grow organically.** The number of
notarial posts is set by the Ministry of Justice by decree, revised roughly every 7
years on population, business volume and territory. Entry is by national competitive
exam (a 400-post concorso was opened by decree of 16 December 2025) and existing
notaries move between posts by transfer competition (604 vacant posts advertised
30 September 2025). https://www.giustizia.it/giustizia/it/mg_1_8_1.page?contentId=SDC1485280
A TAM of ~5,200 here is a hard ceiling, not a starting point.

### 2.5 Professional-firm universe, consolidated

| Profession | Practitioners | Reference | Firms/entities | Reference |
|---|---:|---|---:|---|
| Commercialisti | 119,050 | 2025 | 69,210 studi `[OLD]` | 2024 |
| Avvocati | 228,641 (211,464 active) | 2025 | 542 STA | 2025 |
| Consulenti del lavoro | 26,102 | 2025 | 797 STP | 2024 |
| Notai | 5,238 | 1 Jan 2026 | ~5,238 (capped) | 2026 |
| **Total practitioners** | **~379,000** | | | |

Do not sum the "firms" column: the units are not comparable (studi vs STA vs STP), and
no published source gives a firm count for avvocati or a studio count for consulenti
del lavoro. See "Does not exist publicly".

---

## 3. DIGITAL ADOPTION

### 3.1 The size-frame problem, stated precisely

ISTAT `Imprese e ICT` samples enterprises with **at least 10 addetti**. That base is
205,122 small + 25,943 medium + 4,565 large ≈ **235,630 firms — 5.2% of the ASIA
universe**. The 4.27M micro firms that are the actual ICP for self-serve micro-SaaS
are not in it. ISTAT's own indicator labels carry the qualifier ("imprese con almeno
10 addetti"), and so does every derived Digital Decade / DESI figure for Italy.

Anyone quoting "75% of Italian firms use cloud" is quoting a statistic about the
largest 5% of Italian firms.

### 3.2 ISTAT Imprese e ICT 2025 — base: 10+ addetti

| Indicator | 2023 | 2024 | 2025 | Base |
|---|---:|---:|---:|---|
| Uses cloud computing (any) | 61.4% *(derived)* | — | **75.6%** | 10+ |
| Buys intermediate/advanced cloud | — | — | **68.1%** | 10+ |
| Uses management software (gestionali) | 48.7% | — | **56.0%** | 10+ |
| Data analysis (internal or outsourced) | 26.6% | — | **42.7%** | 10+ |
| Uses ≥1 AI technology | 5.0% | 8.2% | **16.4%** | 10+ |
| Uses ≥2 AI technologies | — | 5.2% | 10.6% | 10+ |
| At least basic digital intensity (≥4 of 12 DII) | — | — | **~80%** | 10+ |
| At least high digital intensity (≥7 of 12 DII) | — | — | 38.1% | 10+ |
| PMI with online sales ≥1% of turnover | — | 14.7% | **14.3%** | 10+ |
| Online share of PMI turnover | 15.5% | 14.0% | **11.7%** | 10+ |
| Uses social media | — | — | 59.0% | 10+ |

Source: ISTAT, `Imprese e Ict – Anno 2025`, published **15 December 2025**, reference
year 2025 (fieldwork May–July 2025; online-sales questions refer to 2024).
https://www.istat.it/comunicato-stampa/imprese-e-ict-anno-2025/
Cloud-any 75.6%: Regione Toscana, `Le ICT nelle imprese toscane con almeno 10 addetti`
(2026 edition), quoting the national ISTAT figure.
https://www.regione.toscana.it/documents/d/guest/rapporto-2026-ict-e-imprese-con-almeno-10-addetti-pdf
Confidence: **high** (primary ISTAT release).
The 61.4% for 2023 is **derived**: Regione Toscana states the national increase as
"+14,2 punti percentuali rispetto al 2023", so 75.6 − 14.2 = 61.4. Not published as a
level; confidence **medium**.

**Internal-consistency check on this block.** ISTAT's Digital-Decade "attainment"
percentages reconcile exactly with the raw indicators, which corroborates both:
88.3% of the 90% SME basic-DII target = 79.5% ("quasi l'80%"); 90.7% of the 75% cloud
target = 68.1%; 21.9% of the 75% AI target = 16.4%; 56.9% of the 75% data-analysis
target = 42.7%. All four match the reported levels.

**By size band within the 10+ frame** — the gap is the story:

| Indicator | PMI (10–249) | Large (250+) | Gap |
|---|---:|---:|---:|
| Data analysis | 41.9% | 83.6% | 41.7 pp |
| ERP | 48.8% | 85.9% | 37.1 pp |
| CRM | **21.1%** | 56.5% | 35.4 pp |
| AI (2025) | 15.7% | 53.1% | 37.4 pp |
| AI (2024) | 7.7% | 32.5% | 24.8 pp |
| AI (2023) | — | — | ~20 pp |
| Basic digital intensity | ~80% | 96.4% | ~16 pp |
| High digital intensity | 38.1% | 81.4% | 43.3 pp |

The AI gap is **widening** — 20 pp (2023) → 25 pp (2024) → 37 pp (2025) — while every
other dimensional gap narrowed. CRM at 21.1% among 10–249 firms is the single lowest
category-adoption figure in the ISTAT set and the clearest greenfield signal.

**Why non-adopters of AI say they don't** (among the 11.5% of non-users who actively
considered it; 83.6% of all 10+ firms use no AI at all):

| Barrier | Share |
|---|---:|
| Lack of skills | 58.6% |
| Lack of legislative clarity | 47.3% |
| Data unavailable or poor quality | 45.2% |
| Privacy / data protection concerns | 43.2% |
| High costs | 43.0% |
| Ethical considerations | 25.7% |
| "Not useful for our business" | 14.8% |

Skills, not price, is the top barrier by 15 points. A self-serve product that requires
configuration is fighting the primary objection.

**Where AI is actually applied** (among the 16.4% who use it): marketing and sales
33.1%, administrative processes 25.7%, R&D/innovation 20.0%. Notably, **33.4% of AI
users could not name any business area at all** — up from 15.5% in 2024 — and 83.3%
of those are 10–49-addetti firms. ISTAT's own reading, verbatim:

> "questo fenomeno suggerisce un'adozione dell'IA sempre più diffusa ma ancora poco
> strutturata, caratterizzata da un utilizzo ancora iniziale e sperimentale non
> riconducibile ad alcun ambito aziendale definito."

> ("this phenomenon suggests an adoption of AI that is increasingly widespread but
> still poorly structured, characterised by a still initial and experimental use not
> attributable to any defined business area.")

Sector concentration (10+ base, 2025): IT and information services 53% AI adoption,
film/video/music production 49.5%, telecoms 37.3%, section M professional/technical
activities 35.7% AI and 46.2% data analysis, section J information services 51.3% AI
and 52.7% data analysis, section D energy 33.2% and 53.6%.

### 3.3 EU comparison

| Indicator | Italy | EU | Reference | Source |
|---|---:|---:|---|---|
| Enterprises (10+) using AI | 16.4% | 20.0% | 2025 | ISTAT / Eurostat release 11 Dec 2025 |
| SMEs at ≥ basic digital intensity | 70.2% | 72.9% | 2024 | Digital Decade 2025 |
| Enterprises adopting AI | 8.2% | — | 2024 | Digital Decade 2025 |
| 2030 target, SMEs at basic DII | — | 90.0% | target | Digital Decade |

Source: European Commission, `Italy 2025 Digital Decade Country Report`, published
**18 June 2025** `[OLD]`, reference year 2024.
https://digital-strategy.ec.europa.eu/en/factpages/italy-2025-digital-decade-country-report
Report PDF mirror: https://www.fondorepubblicadigitale.it/wp-content/uploads/2025/07/Italy_6r2UIRUdNlNNXzQfEq0zO6T90_116743.pdf
Confidence: **high**, but note the Commission's "SMEs" here means Eurostat SMEs
(10–249) — micro firms excluded, same frame problem.

Reconciling the two DII numbers: the Commission reports 70.2% for 2024 on DII version
IV; ISTAT reports ~80% at basic level for 2025 on a nationally-adjusted 12-indicator
set in which "use of at least two social media" was swapped for "use of a website".
**These are not the same indicator and should not be presented as a trend.** ISTAT's
own Digital-Decade progress framing puts Italy's attainment of the 90% SME target at
88.3% in 2025, up from 68.1% in 2023.

### 3.4 [MICRO-INCLUSIVE] Sources that actually reach firms under 10 addetti

Only three exist. All three are weaker than the ISTAT ICT survey.

**(a) ISTAT Censimento permanente delle imprese — base: 3+ addetti, reference 2022.**
The census data warehouse publishes absolute counts of firms with 3+ addetti using
management software and cloud:

| Indicator (3+ addetti, Italy) | Firms | Reference |
|---|---:|---|
| Using management software (software per la gestione aziendale) | 348,137 | 2022 |
| Using cloud | 299,993 | 2022 |
| Universe of firms with 3+ addetti | 1,021,618 | 2022 |

Source: ISTAT, `Software gestionali, cloud, investimenti digitali` (dataset
CPI_CLOUDINV), census dissemination system, reference year 2022 `[OLD]`.
http://dati-censimentipermanenti.istat.it/Index.aspx?DataSetCode=CPI_CLOUDINV
Universe: ISTAT `Censimento permanente delle imprese 2023: primi risultati`, published
**14 November 2023** `[OLD]`, reference year 2022.
https://www.istat.it/comunicato-stampa/censimento-permanente-delle-imprese-2023-primi-risultati/

**Derived shares — my arithmetic, not published by ISTAT:** 348,137 / 1,021,618 =
**34.1%** using management software; 299,993 / 1,021,618 = **29.4%** using cloud.
Confidence: **medium**.

*Numerator verification.* The data warehouse offers both a "10 e più" and a "3 e più"
series and I could not filter it interactively (the page is an ASP.NET browser that
does not render tabular data to a fetch). But the census's own 10+ population is
189,222 + 22,861 + 3,969 = **216,052 firms**. Both numerators (348,137 and 299,993)
**exceed** that, so neither can be the 10+ series — they can only be the 3+ selection.
The numerator is therefore confirmed by construction, which is why this is medium
rather than low confidence. The denominator and numerator share a census and a
reference year, so the ratio is internally consistent.

**Instrument-mismatch warning on the comparison that follows.** ~34% of firms with 3+
addetti used management software (census, 2022) against 48.7% of firms with 10+
addetti (ICT survey, 2023). These are **two different questionnaires asking two
different questions**: the census asks about "software per la gestione aziendale" as a
single item, while the ICT survey's "software gestionali" is built from separate
ERP and CRM items feeding the Digital Intensity Index. The gap is therefore *both* a
size-frame effect *and* an instrument effect, and cannot be decomposed into the two.
It supports the directional claim that adoption falls substantially as you include
3–9-addetti firms; it does not support a precise "adoption halves below 10 addetti"
statement.

The census universe itself makes the exclusion explicit — 1,021,618 firms with 3+
addetti is **22.5% of Italian enterprises**, producing 85.1% of value added. The
other 77.5% of firms are below 3 addetti and appear in no digitalisation survey at
all. Within that 3+ universe, 805,566 firms (78.9%) have 3–9 addetti.

**(b) [MICRO-INCLUSIVE] Osservatorio Innovazione Digitale nelle PMI, Politecnico di
Milano — first-ever micro sample (5–9 addetti), February 2026.**

| Indicator | Micro (5–9) | Small | Medium | All MPMI |
|---|---:|---:|---:|---:|
| Structured AI training programmes started | **4%** | 6% | 20% | — |
| "Not yet the time to invest in AI" | **72%** | — | — | — |
| Has a structured training plan | — | — | — | 30% (19% updated regularly) |
| Funds training exclusively from own means | **71%** | — | — | >50% |
| Top obstacle: lack of time | — | — | — | 65% |
| Second obstacle: lack of money | — | — | — | 20% |

Source: Osservatorio Innovazione Digitale nelle PMI, POLIMI School of Management,
`La Formazione nelle MPMI italiane`, presented **19 February 2026**, reference year
2025/2026. Sample 1,100 firms including, for the first time, micro firms of 5–9
addetti. https://www.ipresslive.it/it/ipress/comunicati/view/59387/
https://it.linkedin.com/posts/osservatori-digital-innovation_osspmi-osspmi26-activity-7430219828818231296-fJmS
Confidence: **medium** (named academic source, disclosed sample size, but the survey
is about *training*, not software purchasing, and the micro cell is a subset of 1,100).

Note the sample floor: **5–9 addetti**, not 0–9. Firms with 1–4 addetti — the large
majority of the 4.27M micro universe — remain unsurveyed even here. The observatory's
own director frames micro firms as "il 95% del tessuto produttivo italiano e un terzo
dell'occupazione privata" ("95% of the Italian productive fabric and a third of
private employment").

**(c) Osservatorio PMI, PoliMi — main annual research, May 2026.** Base is PMI, which
the observatory defines as ~240,000 firms = 5% of Italian companies (i.e. 10–249
addetti; micro excluded from this edition).

| Indicator | Value | Reference |
|---|---:|---|
| No investment in AI, none planned | **76%** | 2025/26 |
| Structured AI training programmes started | 7% | 2025/26 |
| No R&D activity in the last 3 years | 47% | 2023–2025 |
| Increased digital-transformation spend vs prior year | >50% | 2025 |
| — invests intensively across all areas | 24% | 2025 |
| — invests selectively in priority areas | 27% | 2025 |
| — invests little: "digital is marginal in our sector" | 22% | 2025 |
| — invests little: costs disproportionate to benefits | 9% | 2025 |
| — does not understand the benefits | 4% | 2025 |
| — **does not invest at all** | **14%** | 2025 |
| Invested in cloud | 56% | 2023–2025 |
| Expects to invest in cloud | **91%** | 2026–2028 |
| No spend, none planned, on blockchain/AR/VR/quantum | 91% | — |
| Collaborates with technology vendors | 44% | 2025 |
| Collaborates with consultancies | 35% | 2025 |
| Uses trade-association digital services | 17% | 2025 |
| Participates in DIH / Competence Centre projects | 14% | 2025 |
| Projects with universities / research centres | 7% | 2025 |

Digital intensity distribution: small firms 3% very high / 41% high / 42% medium /
14% low; medium firms 13% / 54% / 27% / 6%.

Source: Osservatorio Innovazione Digitale nelle PMI, POLIMI School of Management,
Ricerca 2025-2026, published **21 May 2026**, reference year 2025.
https://www.osservatori.net/comunicato/innovazione-digitale-nelle-pmi/pmi-italiane-innovazione/
Corroborated: https://www.automazionenews.it/pmi-e-digitale-bisogna-fare-piu-leva-sullecosistema/
Confidence: **medium-high** (named academic observatory, but sample size for this
edition not disclosed in the press release; note it is sponsored by ASSOSOFTWARE and
ANCL among others, i.e. by software vendors and labour consultants).

### 3.5 What share of micro firms plausibly buys SaaS at all — the honest answer

**No source answers this directly.** The defensible bracket, with every assumption
visible:

- Firms with 10+ addetti: 75.6% buy cloud, 56.0% use management software (ISTAT 2025,
  high confidence). Base ≈ 235,600 firms.
- Firms with 3+ addetti: ~29% cloud, ~34% management software (derived from census,
  2022, low-medium confidence). Base ≈ 1,021,600 firms.
- Firms with <3 addetti (**≈3.45M, derived**): **no data of any kind exists.**
  Derivation, stated so it can be checked: the census universe of 1,021,618 firms with
  3+ addetti is for reference year **2022**, so it must be netted against the 2022
  enterprise total, not the 2023 one. ASIA 2022 ≈ 4,508,791 / 1.008 ≈ 4,472,000, giving
  4,472,000 − 1,021,618 ≈ **3,450,000**. ISTAT's own statement that the census universe
  is "22,5% delle imprese italiane" implies a slightly higher total (~4.54M) and a
  residual of ~3.52M. Either way the answer is **~3.5M firms with no adoption data**;
  the figure is derived and cross-year, so do not quote it to more than two
  significant figures.

The step from the 10+ frame to the 3+ frame roughly halves adoption. Extrapolating
that curve below 3 addetti would be fabrication and I am not doing it. What can be
said: the paying-software population among Italian micro firms is very likely in the
**hundreds of thousands, not millions**, and the 4.27M micro-enterprise figure must
never be presented as a TAM for a paid product.

Two structural discounts apply on top:
- 48.5% of new businesses are on the *regime forfetario* (2025), a simplified-accounting
  flat-rate regime that removes much of the compliance-software need.
- ~75% of taxpayers file through a commercialista (2024) and ~80% of private companies
  use a consulente del lavoro (2024). For accounting, payroll and tax categories the
  micro firm is frequently **not the buyer** — the professional studio is. That
  redirects the ICP for whole product categories from 4.27M firms to ~69,000 studi
  plus ~26,000 labour consultants.

---

## 4. BUSINESS DEMOGRAPHY — growing or shrinking?

**Growing, slowly, and shifting toward more structured legal forms.**

Movimprese Q2 2026 (Unioncamere/InfoCamere, Registro Imprese — **not** the ASIA
universe):

| Metric | Value | Period |
|---|---:|---|
| Registered firms (stock) | **5,823,863** | 30 Jun 2026 |
| Net balance | **+32,709** | Q2 2026 |
| — registrations | 83,169 | Q2 2026 |
| — closures (net of ex-officio cancellations) | 50,460 | Q2 2026 |
| Growth rate | **+0.56%** (same as Q2 2025) | Q2 2026 |
| Artisan firms (stock) | 1,226,925 | 30 Jun 2026 |
| — net balance / growth | +5,201 / +0.43% | Q2 2026 |

**Composition shift — the more informative signal than the net number:**

| Legal form | Net balance | Growth rate | Period |
|---|---:|---:|---|
| Società di capitali | **+19,861** (30,189 in, 10,328 out) | **+1.00%** | Q2 2026 |
| Imprese individuali | +13,120 | +0.46% | Q2 2026 |
| Società di persone | **−611** | −0.08% | Q2 2026 |

By sector, Q2 2026: finance and insurance +1.91% (+2,868), professional/scientific/
technical activities **+1.59% (+4,059)**, administrative and support services +1.13%
(+2,577), construction +5,369, accommodation and food +4,851, real estate +3,191.
Weak: manufacturing +0.10%, agriculture +0.23%.

By macro-area: South and Islands +11,129, North-West +8,121, Centre +7,730; fastest
rate is the Centre at +0.64%.

Source: Unioncamere / InfoCamere, Movimprese Q2 2026, published **23 July 2026**,
reference period April–June 2026.
https://www.infocamere.it/movimprese
Reported: https://www.italpress.com/nel-secondo-trimestre-del-2026-crescono-le-imprese-33-mila-attivita-in-piu/
https://www.romadailynews.it/2026/07/23/imprese-unioncamere-33-mila-attivita-in-piu-nel-secondo-trimestre-2026-957889/
https://www.bebankers.it/imprese-nel-secondo-trimestre-saldo-positivo-di-oltre-32mila-attivita-crescono-finanza-assicurazioni-e-servizi/
Confidence: **high** (three independent reports of the same Unioncamere release,
figures identical; I did not read the InfoCamere press release itself — the Movimprese
archive is a search interface).

**Classification warning, stated by InfoCamere itself:**
> "Dal primo trimestre 2026 i dati sono classificati secondo ATECO 2025. Vi invitiamo
> a prestare attenzione nei confronti settoriali con i periodi precedenti."
> ("From Q1 2026 data are classified under ATECO 2025. We invite you to be careful
> when making sector comparisons with previous periods.")

**Do not cross-compare with ASIA.** Movimprese counts registered firms at the Chambers
of Commerce (5.82M, includes dormant and non-active entities); ASIA counts firms that
actually produced for at least six months in the reference year (4.51M). The ~1.3M
difference is a definitional gap, not attrition.

Reading for market direction: the aggregate is a slow-growth market (+0.56%/quarter,
roughly +2.2% annualised on stock), but the addressable segment grows faster —
società di capitali at +1.00%/quarter and professional/technical activities at
+1.59%/quarter are precisely the more-structured, more-likely-to-buy end. Sole
proprietorships grow at half the aggregate rate and partnerships are shrinking.

---

## 5. CONFIDENCE SUMMARY

**High confidence (authoritative primary, read directly, or multi-source
corroborated):**
- ASIA size-class table 2023 (ISTAT PDF read directly) — and **independently
  reconciled to the unit** against Eurostat `sbs_sc_ovw` retrieved via API.
- Enterprises by NACE section × size class 2023 (Eurostat API, sums match ISTAT
  exactly).
- Self-employed stock, June 2026 (ISTAT LFS).
- Partita IVA openings 2025 (MEF).
- ISTAT Imprese e ICT 2025 full indicator set (press release read directly).
- Cassa Forense practice-type distribution and the 9.8% figure (PDF read directly,
  quoted verbatim).
- Commercialisti Albo count 2025 (FNC primary page + IPSOA + press, all agree).
- Movimprese Q2 2026 (three independent reports, identical figures).
- Digital Decade Italy 2025 indicators.

**Medium confidence (single authoritative source, or primary body reported via
secondary channel):**
- 69,210 studi / 297,000 addetti — CNDCEC origin confirmed but only via the Council's
  own social post and press reproductions, and it is a **2024** figure.
- Commercialisti practice-form series (51.6% aggregated) — FNC study via IPSOA only.
- Consulenti del lavoro counts — ENPACL origin, read via IPSOA.
- 542 STA (avvocati 2025) — Cassa Forense presentation via Milano Finanza.
- Notai 5,238 — Cassa del Notariato memorandum via ANSA.
- PoliMi observatory figures — named academic source, sample partly undisclosed,
  vendor-sponsored.

**Derived by me — recompute before reuse, and never quote as sourced:**
- 34.1% / 29.4% software and cloud adoption at 3+ addetti (census counts / census
  universe, 2022). Numerator verified by construction; see 3.4(a).
- 61.4% cloud adoption at 10+ addetti in 2023 (back-computed from a stated +14.2 pp).
- ~3.45–3.52M firms below 3 addetti (cross-year residual; see 3.5).
- Micro/small/core-ICP band totals in 1.1 (row arithmetic on the ISTAT table;
  independently confirmed by the Eurostat section sums).
- Self-employed share of employment, 21.7% (June 2026).

**Low confidence (old or single self-interested source):**
- "80% of private companies use a consulente del lavoro" — profession's own research
  office, January 2024.

**Published more than 12 months ago** `[OLD]`: CNDCEC studi count (May 2024),
Censimento permanente primi risultati (Nov 2023), CPI_CLOUDINV reference year 2022,
Cassa Forense Rapporto 2025 (Apr 2025), Consulenti del lavoro Stati Generali research
(Jan 2024), Digital Decade Italy country report (Jun 2025), ASIA 2023 tavole
(Jul 2025, marginally over).

---

## 6. DOES NOT EXIST PUBLICLY

Searched for and not found. **Do not interpolate or estimate these.**

1. **Any digitalisation, cloud, software or SaaS-purchasing statistic for Italian
   firms with fewer than 3 addetti.** This is roughly 3.49M businesses — the largest
   single block of the ICP — and no survey in the Italian statistical system reaches
   it. ISTAT ICT starts at 10 addetti; the Censimento permanente starts at 3; PoliMi's
   first micro extension starts at 5. Nothing covers 1–2 addetti.

2. **A published stock of active partite IVA.** The MEF Osservatorio publishes
   openings (a flow) only. There is no official "how many partite IVA exist right now"
   figure in this source.

3. **A firm count (as opposed to a lawyer count) for the Italian legal profession.**
   Cassa Forense counts individuals and STA entities; nobody publishes "how many law
   firms exist in Italy". The 9.8% is a share of lawyers, not of firms.

4. **A studio count for consulenti del lavoro.** ENPACL publishes individuals (26,102)
   and STP (797) but not the number of practices.

5. **An updated commercialisti studi count.** The 69,210 figure has not been restated
   since May 2024 despite two subsequent Rapporto editions (2025, 2026), which report
   iscritti, praticanti and STP but not studi.

6. **Any Italian-specific SaaS spend, willingness-to-pay, ARPA, or software-budget
   figure by firm size class.** No source found — not ISTAT, not the observatories,
   not Assosoftware publicly. The ISTAT ICT questionnaire does ask software spend as a
   percentage of turnover (question D2) but the result is not published in the press
   release or the summary tables I could reach.

7. **Adoption or purchasing data for the professional-firm segment specifically**
   (what share of studi commercialisti buy vertical SaaS, what they spend). The Cassa
   Forense report gives AI usage among lawyers (27.5% use it in daily practice, 2024)
   and the FNC study covers organisation, but neither publishes software purchasing.

8. **The primary CNDCEC page for the 69,210 / 297,000 figures.** Located only on the
    Council's Facebook post and press reproductions.

9. **The InfoCamere Movimprese Q2 2026 press release itself.** The Movimprese archive
    at infocamere.it is a search interface that did not surface a direct PDF URL;
    figures were taken from three independent agency reports that agree exactly.

Search caveat: Italian business-statistics queries surface a heavy layer of
consultancy and vendor blogs restating ISTAT figures without reference years, and
several restate the 10+ frame figures as though they applied to all firms. Every
number above was traced to the issuing body or to named press coverage of a specific
dated release.

---

## 7. SOURCES

**Eurostat — enterprises by NACE section and size class**
- Dataset `sbs_sc_ovw`, Enterprise statistics by size class and NACE Rev. 2 activity (from 2021 onwards); dataset updated 10 Mar 2026, reference year 2023 — https://ec.europa.eu/eurostat/databrowser/view/sbs_sc_ovw/default/table?lang=en
- API query used (retrieved 2026-08-13) — `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sbs_sc_ovw?format=JSON&geo=IT&indic_sbs=ENT_NR&time=2023`
- SBS metadata, size-class definitions and coverage — https://ec.europa.eu/eurostat/cache/metadata/EN/sbs_esms.htm
- SBS overview — https://ec.europa.eu/eurostat/web/structural-business-statistics/overview

**ISTAT — enterprise structure**
- Conti economici delle imprese e dei gruppi di impresa, Anno 2023 (15 Oct 2025) — https://www.istat.it/wp-content/uploads/2025/10/Report-Conti-economici-imprese-e-gruppi_2023.pdf
- English edition, Structural business statistics: enterprises and enterprise groups, Year 2023 (15 Oct 2025), carries the verbatim NACE coverage statement — https://www.istat.it/en/press-release/structural-business-statistics-enterprises-and-enterprise-groups-year-2023/
- Same, English PDF — https://www.istat.it/wp-content/uploads/2025/10/EN-SBS_enterprise_and_enterprise_groups_2023_EL-10_10.pdf
- Same, press page — https://www.istat.it/comunicato-stampa/conti-economici-delle-imprese-e-dei-gruppi-di-impresa-anno-2023/
- Registro statistico delle imprese attive, Anno 2023 (9 Jul 2025) — https://www.istat.it/tavole-di-dati/registro-statistico-delle-imprese-attive-anno-2023/
- Nota metodologica Registro 2023 — https://www.istat.it/wp-content/uploads/2025/07/Nota-metodologica-Registro-2023.pdf
- IstatData browser — https://esploradati.istat.it/databrowser/#/it
- Demografia d'impresa 2017-2022 (6 Aug 2024) — https://www.istat.it/tavole-di-dati/demografia-dimpresa-anni-2017-2022/
- Archivio tag ASIA — https://www.istat.it/tag/archivio-asia/

**ISTAT — census and ICT**
- Censimento permanente delle imprese 2023: primi risultati (14 Nov 2023) — https://www.istat.it/comunicato-stampa/censimento-permanente-delle-imprese-2023-primi-risultati/
- Same, PDF — https://www.istat.it/it/files/2023/11/REPORTCensimprese.pdf
- Censimento imprese, risultati e diffusione — https://www.istat.it/statistiche-per-temi/censimenti/imprese/risultati/
- Censimento imprese, third edition (fieldwork Oct 2025 – Mar 2026) — https://www.istat.it/statistiche-per-temi/censimenti/imprese/
- CPI_CLOUDINV dataset, software gestionali/cloud/investimenti digitali — http://dati-censimentipermanenti.istat.it/Index.aspx?DataSetCode=CPI_CLOUDINV
- CPI_CLOUDINV metadata — http://dati-censimentipermanenti.istat.it/OECDStat_Metadata/ShowMetadata.ashx?DataSet=CPI_CLOUDINV
- Imprese e Ict, Anno 2025 (15 Dec 2025) — https://www.istat.it/comunicato-stampa/imprese-e-ict-anno-2025/
- ICT questionnaire facsimile (definitions of cloud and business software) — https://siqual.istat.it/SIQual/files/Questionario%20ICT%202023_facsimile.pdf?cod=5683&ind=5000078&progr=1&tipo=4
- Regione Toscana, Le ICT nelle imprese con almeno 10 addetti, 2026 edition — https://www.regione.toscana.it/documents/d/guest/rapporto-2026-ict-e-imprese-con-almeno-10-addetti-pdf
- Assolombarda summary of Imprese e ICT 2025 — https://www.assolombarda.it/centro-studi/utilizzo-dellintelligenza-artificiale-nelle-imprese

**ISTAT — labour force (self-employed stock)**
- Occupati e disoccupati (dati provvisori), Giugno 2026 (30 Jul 2026) — https://www.istat.it/comunicato-stampa/occupati-e-disoccupati-dati-provvisori-giugno-2026/
- Same, PDF with the indipendenti definition — https://www.istat.it/wp-content/uploads/2026/07/CS_Occupati-e-disoccupati_GIUGNO_2026.pdf
- ISTAT Lavoro e retribuzioni theme page — https://www.istat.it/statistiche-per-temi/istruzione-e-lavoro/lavoro-e-retribuzioni/

**MEF / Agenzia delle Entrate**
- Osservatorio sulle partite IVA, sintesi anno 2025 (12 Feb 2026) — https://www.finanze.gov.it/it/archivi/notizie/dettaglio-notizie/Osservatorio-sulle-partite-IVA-sintesi-dei-dati-anno-2025-00001/
- Same, PDF — https://www1.finanze.gov.it/finanze/osiva/public/contenuti/Sintesi_annuale_dati_2025.pdf
- Nota metodologica OPI (ATECO 2025 transition) — https://www1.finanze.gov.it/finanze/osiva/public/contenuti/Nota_Metodologica_OPI.pdf
- ANSA coverage (12 Feb 2026) — https://www.ansa.it/sito/notizie/topnews/2026/02/12/nel-2025-aperte-oltre-500mila-nuove-partite-iva-04_0c52a7f3-ff4c-43b1-8137-9522e5a0f705.html

**Unioncamere / InfoCamere**
- Movimprese archive — https://www.infocamere.it/movimprese
- Unioncamere Movimprese page — https://www.unioncamere.gov.it/sistema-camerale/attivita/movimprese
- Q2 2026 coverage, Italpress (23 Jul 2026) — https://www.italpress.com/nel-secondo-trimestre-del-2026-crescono-le-imprese-33-mila-attivita-in-piu/
- Q2 2026 coverage, RomaDailyNews (23 Jul 2026) — https://www.romadailynews.it/2026/07/23/imprese-unioncamere-33-mila-attivita-in-piu-nel-secondo-trimestre-2026-957889/
- Q2 2026 coverage, BeBankers (24 Jul 2026) — https://www.bebankers.it/imprese-nel-secondo-trimestre-saldo-positivo-di-oltre-32mila-attivita-crescono-finanza-assicurazioni-e-servizi/

**Commercialisti (CNDCEC / FNC)**
- Rapporto 2026 sull'Albo (16 Jul 2026) — https://www.fondazionenazionalecommercialisti.it/node/1911
- FNC home — https://www.fondazionenazionalecommercialisti.it/
- CNDCEC Rapporto annuale hub — https://commercialisti.it/cndcec-comunica/sala-stampa/rapporto-annuale-sulla-professione/
- IPSOA on Rapporto 2026 (16 Jul 2026) — https://www.ipsoa.it/documents/quotidiano/2026/07/17/commercialisti-rapporto-2026-professione
- IPSOA on practice aggregation, 51.6% (23 Oct 2025) — https://www.ipsoa.it/documents/quotidiano/2025/10/23/commercialisti-aggregazioni-professionali-51-6
- CNDCEC Facebook, 69,210 studi (7 May 2024) — https://www.facebook.com/consigliocommercialisti/posts/757639213213913/
- Teleborsa, Stati Generali 2024 (7 May 2024) — https://www.teleborsa.it/News/2024/05/07/commercialisti-a-roma-gli-stati-generali-oltre-69-mila-studi-piu-di-290mila-addetti-creato-quasi-1percent-pil-115.html
- Press Magazine (8 May 2024) — https://press-magazine.it/commercialisti-oltre-69-mila-studi-piu-di-290mila-addetti-quasi-l1-del-pil-creato/
- Fiscal Focus (8 May 2024) — https://www.fiscal-focus.it/quotidiano/altre-tematiche/infoprofessioni/commercialisti-oltre-69mila-studi-piu-di-290mila-addetti-quasi-l-1-del-pil-creato,3,162970
- Press Magazine on Rapporto 2026 (16 Jul 2026) — https://press-magazine.it/commercialisti-redditi-in-crescita-dell83-tornano-a-salire-i-praticanti-42/

**Avvocati (Cassa Forense / Censis / CNF)**
- Rapporto sull'Avvocatura 2025, full PDF (Apr 2025) — https://www.cassaforense.it/media/munf4vli/rapporto-avvocatura-2025.pdf
- Censis, X Rapporto sull'Avvocatura 2026 (29 Apr 2026) — https://www.censis.it/x-rapporto-sullavvocatura-2026/
- Milano Finanza, Cassa Forense 2025 accounts and 542 STA (4 May 2026) — https://www.milanofinanza.it/news/cassa-forense-archivia-il-2025-con-un-utile-da-1-33-miliardi-patrimonio-oltre-quota-20-miliardi-202605041115522398
- Il Sole 24 Ore NT+ Diritto on Rapporto 2025 (2 Apr 2025) — https://ntplusdiritto.ilsole24ore.com/art/avvocati-calano-iscritti-cresce-fatturato-ma-donne-e-sud-restano-indietro-AG01UsuD
- Il Sole 24 Ore NT+ Diritto on Rapporto 2026 — https://ntplusdiritto.ilsole24ore.com/art/rapporto-censis-legali-transizione-ma-fare-professione-resta-difficile-AI3rl92C
- Avvocati Associati on X Rapporto (12 May 2026) — https://www.avvocati-associati.eu/rapporto-sullavvocatura-pubblicato-il-x-rapporto/

**Consulenti del lavoro (CNO / ENPACL)**
- Consiglio Nazionale dell'Ordine — https://www.cnoconsulentidellavoro.it/
- ENPACL — https://www.enpacl.it/
- IPSOA on ENPACL 2025 accounts (7 May 2026) — https://www.ipsoa.it/documents/quotidiano/2026/05/08/bilancio-2025-enpacl-crescono-ricavi-patrimonio-redditi-categoria
- IPSOA on ENPACL 2024 accounts (1 May 2025) — https://www.ipsoa.it/documents/quotidiano/2025/05/02/enpacl-bilancio-approvato-numeri-crescita
- FiscoeTasse on STP growth 106→797 — https://www.fiscoetasse.com/new-rassegna-stampa/2207-consulenti-del-lavoro-boom-fatturati-e-redditi-nelle-stp.html
- IPSOA on Stati Generali research (11 Jan 2024) — https://www.ipsoa.it/documents/quotidiano/2024/01/12/rapporto-professione-numeri-consulenti-lavoro
- ADEPP, 80% of private companies (17 Jan 2024) — https://www.adepp.info/2024/01/l80-delle-aziende-private-si-avvale-del-consulente-del-lavoro/

**Notai**
- Consiglio Nazionale del Notariato, statistics page — https://www.notariato.it/it/notaio/statistiche/
- Dati Statistici Notarili portal — https://www.notariato.it/it/notariato/dati-statistici-notarili/ and https://dsn.notariato.it/dsn
- DSN Analisi 2025, dati generali — https://dsn.notariato.it/dsn/contenuti/analisi/2025/DSN_ANALISI_2025_Dati_generali.pdf
- ANSA, Cassa del Notariato 5,238 (2 Jul 2026) — https://www.ansa.it/sito/notizie/casse_previdenza/2026/07/02/cassa-del-notariato-5.238-iscritti-3.133-uomini-e-2.105-donne_59cd6e0e-c782-4d4c-8414-ed6e8939f194.html
- Mondo Professionisti, same (2 Jul 2026) — https://www.mondoprofessionisti.it/casse-di-previdenza/cassa-del-notariato-5-238-iscritti-3-133-uomini-e-2-105-donne/
- ANSA, 5,072 notaries (24 Oct 2024) — https://www.ansa.it/sito/notizie/ordini_professionali/2024/10/24/ammontano-a-5.072-i-notai-in-italia-3.079-uomini-e-1.993-donne_cc9d75e7-b7ad-4f05-9e33-5860c848071d.html
- Ministero della Giustizia, decree 16 Dec 2025, 400-post concorso — https://www.giustizia.it/giustizia/it/mg_1_8_1.page?contentId=SDC1485280
- Ministero della Giustizia, transfer competition, 604 posts (30 Sep 2025) — https://www.giustizia.it/giustizia/it/mg_1_6_1.page?contentId=SCE1473097

**EU**
- Italy 2025 Digital Decade Country Report (18 Jun 2025) — https://digital-strategy.ec.europa.eu/en/factpages/italy-2025-digital-decade-country-report
- Digital Decade 2025 country fact pages — https://digital-strategy.ec.europa.eu/en/factpages/digital-decade-2025-report-country-fact-pages
- 2025 State of the Digital Decade package — https://digital-strategy.ec.europa.eu/en/policies/2025-state-digital-decade-package
- SWD(2025) 295, DII version IV definition — https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX%3A52025SC0295
- Italy country report PDF mirror — https://www.fondorepubblicadigitale.it/wp-content/uploads/2025/07/Italy_6r2UIRUdNlNNXzQfEq0zO6T90_116743.pdf

**Politecnico di Milano Osservatori**
- Osservatorio Innovazione Digitale nelle PMI, main release (21 May 2026) — https://www.osservatori.net/comunicato/innovazione-digitale-nelle-pmi/pmi-italiane-innovazione/
- Convegno page, Ricerca 2025-2026 (27 Jan 2026) — https://www.osservatori.net/convegno/innovazione-digitale-nelle-pmi/convegno-risultati-ricerca-osservatorio-innovazione-digitale-nelle-pmi/
- MPMI training research including micro 5-9 (19 Feb 2026) — https://www.ipresslive.it/it/ipress/comunicati/view/59387/
- Osservatori LinkedIn post on the micro extension (19 Feb 2026) — https://it.linkedin.com/posts/osservatori-digital-innovation_osspmi-osspmi26-activity-7430219828818231296-fJmS
- Automazione News coverage (28 May 2026) — https://www.automazionenews.it/pmi-e-digitale-bisogna-fare-piu-leva-sullecosistema/
- Osservatorio Cloud Transformation (23 Jan 2026) — https://www.osservatori.net/grafici/cloud-ecosystem-sovereignty/grafici-cloud-transformation/

**Other**
- ISTAT Glossario (ASIA definition, addetti, impresa attiva) — https://www.istat.it/wp-content/uploads/2024/04/Glossario-1.pdf
- ISTAT Annuario Statistico Italiano 2023, cap. 14 Imprese — https://www.istat.it/storage/ASI/2023/capitoli/C14.pdf
- ISTAT ASI 2025 note metodologiche — https://www.istat.it/storage/ASI/2025/note-metodologiche/N14.pdf
- Regione Emilia-Romagna, ASIA metadata (series break at 2011) — https://statistica.regione.emilia-romagna.it/metadati/rilevazioni/metadati_asia
- Digital World Italia on Imprese e ICT 2025 (16 Dec 2025) — https://www.digitalworlditalia.it/digitalpartner/industria-it/rapporto-istat-su-imprese-italiane-e-ict-luso-dellia-raddoppia-ma-rimane-marginale-177111
- UniverseIT on Imprese e ICT 2025 (11 Dec 2025) — https://universeit.blog/imprese-e-ict-rapporto-istat-2025/

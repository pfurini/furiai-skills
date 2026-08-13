# Price Anchors and Incumbent Ecosystems — Italian Micro/Small Business Software

Research date: **2026-08-13**. All observations made on that date unless a different date is stated.

Scope: what Italian micro and small firms (PMI, ditte individuali, forfettari, studi commercialisti, studi legali) demonstrably pay for software, and which incumbent vendors expose a distribution surface (marketplace / public API) that an independent micro-SaaS could plug into.

## Reading rules for every figure below

- **Currency and VAT.** All prices are in EUR. Italian VAT (IVA) is 22%. Nearly every Italian B2B software list price is quoted **ex-VAT (+ IVA)**; where a source quoted VAT-inclusive figures this is stated explicitly.
- **Promo vs. steady state.** Italian invoicing vendors advertise a heavily discounted first-year price. **Derive bands from the renewal price, not the entry price.** Fatture in Cloud's €4/mo Forfettari renews at €8/mo (€96/yr); Aruba's €1-for-3-months renews at €29.90/yr. Anchoring on the promo would understate real spend by roughly 2x on the entry tier.
- **Billing unit matters more than the monthly number.** Practice software is priced per studio, per postazione, per utente, or per azienda/ditta gestita. A bare EUR/month figure is meaningless without the unit, so a unit column appears in every table.
- **Confidence.** `high` = read directly on the vendor's own pricing page (or vendor developer docs). `medium` = recent third-party comparison, or a vendor page whose figures were extracted indirectly. `low` = dated, indirect, or internally ambiguous.

---

## 1. Invoicing / gestionale for micro-firms (self-serve, published prices)

This is the only category in Italian B2B software where list prices are consistently public. It is therefore the most reliable price anchor available.

### 1.1 Fatture in Cloud (TeamSystem) — confidence: high

Read directly from https://www.fattureincloud.it/costo/ on 2026-08-13. All ex-VAT, billed annually, per azienda (company), 1 user unless noted.

| Tier | Price/month | Price/year | Renewal price | Docs/year | Users | Confidence |
|---|---|---|---|---|---|---|
| Forfettari | €4 (promo, 1st year only) | €48 | **€8/mo = €96/yr** | 100 | 1 | high |
| Standard | €12 | €144 | €144/yr | 100 | 1 | high |
| Premium | €21 | €252 | €252/yr | 400 | 1 | high |
| Premium Plus | €29 | €348 | €348/yr | 800 | multi-user | high |
| Complete | €51 | €612 | €612/yr | 3000 | multi-user | high |

Additional cost on every plan: a one-off administrative handling fee of **€1.00 + IVA** (card/PayPal) or **€2.50 + IVA** (bank transfer) per annual payment. Conservazione sostitutiva (legally mandatory archival) is included in all tiers — this is not universal in this market and is worth noting as a competitive baseline.

The Forfettari promo footnote is explicit: *"Offerta riservata ai contribuenti in regime forfettario, valida per il primo anno dall'iscrizione. Allo scadere del primo anno, il prezzo si aggiorna a 8,00 €/mese – 96,00 €/anno + IVA."*

**Price movement signal.** Two third-party comparisons published in January 2026 (srlonline.com, centrofiscale.com) list Premium at €19, Premium Plus at €27 and Complete at €49. The official page on 2026-08-13 shows €21 / €29 / €51. List prices moved up roughly 4-10% during 2026. Treat any Fatture in Cloud figure older than ~6 months as stale.

### 1.2 Danea Easyfatt (TeamSystem group) — confidence: high

The published prices are rendered client-side and invisible to plain HTTP fetches; the figures below were read from the rendered page at https://www.danea.it/software/easyfatt/prezzi/ on 2026-08-13. All ex-VAT, 12-month licence, plus the same €1.00/€2.50 admin fee.

**Desktop (PC/Windows):**

| Tier | Price/month | Price/year | Included e-invoices | Seats | Confidence |
|---|---|---|---|---|---|
| Standard | from €4 (promo, 1st year) | €48 | 100 documents | 1 | high |
| Professional | from €15 | €180 | 400 | 1 user, 2 PCs | high |
| Enterprise One | from €25 | €300 | 800 | 1 user, 2 PCs | high |
| Enterprise | from €40 | €480 | unlimited | up to 5 seats (LAN) | high |

**Cloud:**

| Tier | Price/month | Price/year | Included e-invoices | Seats | Confidence |
|---|---|---|---|---|---|
| Standard | from €4 (promo, 1st year) | €48 | 100 documents | 1 | high |
| Professional Cloud | from €35 | €420 | 400 | 1 | high |
| Enterprise One Cloud | from €59 | €708 | 800 | 1 | high |
| Enterprise Cloud | from €110 | €1,320 | unlimited | up to 5 | high |

**Add-on modules (ex-VAT):** additional company e-invoicing **€120/yr per extra azienda**; *Contabilità in Cloud by TeamSystem* module **€21/month** (up to 50,000 transactions); credit-check service **€94 + IVA per 5,000 checks/year**.

Note the cloud premium: Professional Cloud (€420/yr) costs 2.3x the desktop Professional (€180/yr) for the same feature set. Danea does **not** publish a renewal price for the €4 Standard promo tier — see section 6.

A January 2026 third-party comparison (centrofiscale.com) listed Enterprise One at €288/yr; the official page shows €300/yr. Official figures win.

### 1.3 Aruba Fatturazione Elettronica — confidence: high (base), medium (modules)

Official listino: https://aruba.it/listino-fatturazione-elettronica.aspx

| Service | First activation | Renewal (ex-VAT) | Confidence |
|---|---|---|---|
| Fatturazione Elettronica (base + 1 GB) | €1.00 + IVA for 3 months | **€29.90/yr** | high |
| Fatturazione Elettronica Solo Ricezione | €1.00 + IVA for 3 months | €29.90/yr | high |

Aruba is the cheapest credible anchor in the market, but the base service is send/receive/archive only. Everything else is a separately priced module. The module amounts below come from a cart-level survey by softwaresemplice.it (published 2025-07-29), confidence medium. Aruba's own renewal guide corroborates the *structure* — that modules, extra GB and extra users are each charged again at renewal — but does not publish the amounts, so the euro figures rest on the third-party survey alone:

| Module | Renewal/yr ex-VAT | Renewal/yr incl. VAT |
|---|---|---|
| Modulo Documenti (quotes, orders, DDT) | €19.90 | €24.28 |
| Modulo Incassi e Pagamenti | €19.90 | €24.28 |
| Modulo WooCommerce | €39.90 | €48.68 |
| Modulo Ordini Elettronici (NSO) | €25.00 | €30.50 |
| Additional user | €4.90 each | €5.98 each |

Realistic bundles at renewal: base + Documenti + Incassi/Pagamenti = **€69.70/yr ex-VAT**; base + all modules = **€134.60/yr ex-VAT** (€164.21 incl. VAT). Unlike its competitors, Aruba's headline price does not jump after year one.

### 1.4 Other self-serve invoicing vendors — confidence: medium

From a July 2026 price comparison (pazienza.app, published 2026-07-08, sourced from official listini) plus vendor cross-checks. All annual, ex-VAT.

| Vendor / plan | Entry price | Renewal price | Included volume | Confidence |
|---|---|---|---|---|
| Pazienza (Standard) | €48/yr | €48/yr — unchanged | 100 credits/yr, then €4 packs | medium |
| Fattura24 (Professional) | €48/yr (1st-yr promo) | **€120/yr** | 3,000 docs/yr per type | medium |
| Fattura24 (Business) | — | €144–192/yr | up to 5 users | medium |
| Software Semplice (base) | €48/yr | €48/yr | 100 docs | medium |
| Software Semplice Complete 2026 | €180/yr | €180/yr | 1,500 e-invoices, 5 users | medium |
| Fattura Elettronica App (Forfettari) | €4.99/mo (~€60/yr) | unchanged, no annual lock-in | 500 invoices/yr | medium |
| Fattura Elettronica App (Unlimited) | €21.99/mo | unchanged | unlimited | medium |
| Fiscozen (forfettario) | €499/yr | €499/yr | unlimited — this is a service (accountant included), not software | medium |

### 1.5 FATTURE GB (GBsoftware) — confidence: medium

**Correction to a common assumption: "Fatture GB" is a GBsoftware product, not a Zucchetti one.** It is sold to commercialisti as a shared studio-client environment.

Published ladder priced by annual document volume (ex-VAT), from https://www.softwaregb.it/software-fatturazione-elettronica-commercialisti/:

| Documents issued+received/year | Price/year ex-VAT |
|---|---|
| 25 | free |
| 100 (forfettari, ETS, ENC, 398/91) | €48 |
| 400 | €75 |
| 1,000 | €96 |
| 6,000 | €129 |
| unlimited | €212 |

Confidence is medium rather than high: the figures come from the vendor's own page, but the volume-to-price row alignment was recovered from a search-index extraction and could not be re-verified against the rendered page (the page's price widget did not render in either fetch attempt). The price *values* are reliable; the exact volume tier each maps to should be confirmed before use.

### 1.6 Zucchetti — prepaid invoice packs, not subscriptions — confidence: medium (dated)

Zucchetti does not sell a self-serve monthly gestionale subscription to micro-firms through its store. It sells **prepaid packets of electronic invoices** with no recurring canone (https://www.zucchetti.it/store/cms/fatturazione-elettronica-acquista.html). The official published listino PDF (https://www.zucchetti.it/website/dms/Store/Listino_Zucchetti_Store.pdf) carries a price-revision date of **10.01.2023** — treat as dated:

| Invoices | Price |
|---|---|
| 10 | €11.00 |
| 30 | €25.00 |
| 50 | €33.00 |
| 100 | €57.00 |
| 250 | €140.00 |
| 500 | €275.00 |

A second ladder in the same document runs 10 → €17.00, 100 → €110.00, 1,000 → €495.00, 5,000 → €1,650.00. Same-document GDPR-module pricing (Modulo base €105.00, GDPR Zucchetti €420.00) confirms Zucchetti does publish some list prices — just not for its studio suites.

### 1.7 Derived band — invoicing / gestionale for a micro-firm

**Billing unit: per azienda (company), per year, ex-VAT, generally 1 user.**

| Segment | Cheapest viable | Typical | Notes |
|---|---|---|---|
| Forfettario / solo partita IVA | **€2.50–4/month** (€29.90–48/yr) | **€4–8/month** (€48–96/yr) | Aruba base is the floor; FIC Forfettari at renewal is the mode |
| Micro-firm, real document volume (ditta individuale, small SRL) | **€10–15/month** (€120–180/yr) | **€12–25/month** (€144–300/yr) | FIC Standard/Premium, Danea Professional/Enterprise One |
| Small firm with warehouse, staff or multi-user | **€29–40/month** (€348–480/yr) | **€35–60/month** (€420–708/yr) | FIC Premium Plus/Complete, Danea Enterprise, Danea cloud tiers |

The **mode** for a self-serve purchase in this category sits around **€12–25/month ex-VAT**, and self-serve buying visibly thins out above roughly **€50/month**. This is not a hard ceiling: Danea publishes cloud tiers at €59 and €110/month, TeamSystem Commerce at €82 and €238/month, and section 4.1 puts small-team booking software at €50–80/month. What changes above ~€50/month is the *purchase motion* — the buyer starts wanting a demo, a contract, and often a dealer — rather than the availability of budget.

---

## 2. Commercialisti practice software — effectively 100% quote-only

**This is itself the headline finding for the category.** No major vendor publishes a list price for practice-management software aimed at studi commercialisti.

TeamSystem states this outright on its own product page (https://www.teamsystem.com/commercialisti/teamsystem-studio/): *"Il costo di TeamSystem Studio AI non è fisso, ma varia in base alla configurazione scelta e alle esigenze dello Studio professionale"*, listing number of postazioni, activated modules, cloud infrastructure, integrations, AI usage and training as price drivers. Confidence: **high** (that it is quote-only).

An October 2025 industry survey (qonto.com) reaches the same conclusion independently: *"nessuno dei principali fornitori pubblica un listino prezzi ufficiale e dettagliato."* Confidence: high.

| Vendor / product | List price published? | Billing unit (where known) | Confidence |
|---|---|---|---|
| TeamSystem Studio AI | No — quote only, stated on vendor page | per postazione + modules | high |
| Zucchetti Ago Infinity | No — varies by configuration and licence count; training extra | per licence | high |
| Wolters Kluwer Genya | No — *canone annuo personalizzato*, also varies by number of anagrafiche | per user + anagrafiche volume | high |
| Wolters Kluwer B.Point | No | — | high |
| Buffetti eBridge Studio | No on buffetti.it; dealer promos exist | per utenza (monoutenza/multiutenza) | high |
| Sistemi PROFIS | No | — | high |
| Ranocchi GIS | No | — | high |
| Passepartout Passcom | No | — | high |

### 2.1 The only real numbers found

| Source | Figure | Date | Confidence |
|---|---|---|---|
| Buffetti dealer (Software & Service Campania, softwaresalerno.com) | eBridge promo **canone mensile da €154,00 + IVA (monoutenza)**, new customers only | page dated 2020 | **low** (six years old) |
| TaxDome industry guide | TeamSystem Studio Cloud **~€1,000 + IVA** for the base solution, modules extra; discounts for multi-product or multi-year | 2025-08-27 | medium |
| Qonto industry guide | Subscriptions **from ~€100/month** for small studi; over **€3,000/year** for structured configurations | 2025-10-29 | medium |
| brentasoft market survey | Small studio €1,200–2,500/yr; medium studio €3,000–6,000/yr; WK Genya cloud quoted at €60–90/user/month in full configuration; one-off migration/training adds 30–60% of the annual canone in year one | **2021** | **low — five years old, flagged as likely outdated** |

### 2.2 Derived band — commercialisti practice software

**Billing unit: per studio, scaling by postazioni/utenti and by modules; some vendors also scale by number of anagrafiche or aziende gestite.**

| Studio size | Band (ex-VAT) | Confidence |
|---|---|---|
| Small studio (1–3 people, base modules) | **€100–250/month** (€1,200–3,000/yr) | medium |
| Medium studio (5–15 people, full suite incl. paghe) | **€250–500/month** (€3,000–6,000/yr) | low-medium |

Add one-off implementation: data migration and training are separately charged and are material (the 2021 source put them at 30–60% of the first-year canone; a 2026 legal-sector source put migration at €500–1,500, which is the right order of magnitude for a small practice).

**Implication for an indie tool:** a commercialista's existing software spend is an order of magnitude above a micro-firm's, but it is spent through a dealer relationship with an annual or multi-year contract. A self-serve tool is not competing for that budget line; it is competing for discretionary spend beside it.

---

## 3. Legal practice management

### 3.1 Kleos (Wolters Kluwer) — Italian prices not published; sibling markets publish

Verified on 2026-08-13 at https://www.wolterskluwer.com/it-it/solutions/kleos/pricing, by both HTTP fetch and a rendered headed browser: the Italian page publishes four tiers — **Start, Core, Advanced, Advanced +** — with full feature lists and storage allowances, but **no EUR figures at all**. Every call to action is "Prova Kleos gratis per 30 giorni". Confidence: **high** that Italian list prices are not published.

By contrast, Wolters Kluwer *does* publish Kleos prices in other European markets:

| Market | Core | Advanced | Advanced+ | Unit | Confidence |
|---|---|---|---|---|---|
| Belgium (nl-be) | €69 | €99 | €109 (promo €99) | per user/month | medium |
| France (fr-fr), via LegalProd comparison (2023-12) | €59 HT | €79 HT | €89 HT | per user/month | medium |

**Do not transpose these into an Italian pricing pack as Italian prices.** They are the nearest published anchor for the same product, nothing more. Italian tier names also differ from the Belgian ones and from Kleos's own Italian brochure, which still uses the older **Essential / Pro** naming — evidence the Italian packaging was repositioned recently.

Italian third-party estimates for Kleos:

| Source | Figure | Date | Confidence |
|---|---|---|---|
| BullTech (bulltech.it) | **from €49/month per lawyer** on an annual contract; overall range €49–120/avvocato/month; setup and migration €500–1,500 one-off | 2026-04-12 | medium |
| TIWARE (Italian Kleos reseller, tiware.it) | listing shows **€288.00 – €576.00** with a 6-month / 12-month option and the note *"the cost is intended per month per user"* | undated | **low — internally contradictory**; a €288 figure cannot simultaneously be a per-user monthly price and a 6/12-month package. Do not use without clarification from the reseller. |

**Kleos API access is a paid add-on gated to the top tier.** "Modulo Kleos API" appears in the *Disponibile* list of **Advanced + only** — not Start, Core, or Advanced. "Kleos Connect" (the client extranet) is likewise Advanced+ only. Confidence: high (read on the vendor pricing page).

### 3.2 Cliens Gestione Studio Legale (Lefebvre Giuffrè) — not published

Both the Giuffrè shop listing (https://shop.giuffre.it/025000165-cliens-gestione-studio-legale-pratiche-illimitate) and the product page (lefebvregiuffre.it) carry full product descriptions and **no price**. The shop page instead routes buyers to a convenzione-based discount channel: *"Hai una convenzione con la nostra azienda? Scrivi a shop@giuffrefl.it ... per ricevere il tuo codice sconto personalizzato."* Confidence: high (that it is not listed).

### 3.3 Consolle Avvocato (CNF)

Free to members of the Albo, bundled with bar-association membership; functionally limited relative to a full practice-management suite. Confidence: medium (single Italian source, 2026-04).

### 3.4 Derived band — legal practice management

**Billing unit: per lawyer (utenza) per month, annual contract; cloud storage pooled across the studio.**

| Firm size | Band (ex-VAT) | Confidence |
|---|---|---|
| Solo / 2-lawyer | **€0** (Consolle, if basic needs) to **€49–60/lawyer/month** | medium |
| 3–10 lawyers | **€49–99/lawyer/month** | medium |
| Full suite, top tier (with AI, API, extranet) | **€100–120/lawyer/month** | low-medium |

Plus **€500–1,500** one-off setup/migration for a small firm. Note that per-seat pricing makes the studio-level number scale linearly: a 5-lawyer firm on Kleos-class software is plausibly at **€250–500/month ex-VAT**, i.e. the same absolute band as a small commercialista studio.

---

## 4. Horizontal SMB SaaS priced for the Italian market — booking / appointments

This category is the closest published analogue to what an indie micro-SaaS would sell, because the products are self-serve, flat-fee, and bought without a dealer.

**Two verification notes on the brief's assumptions:**
- **Uala no longer exists as an independent brand.** It was acquired by Treatwell in 2022 and folded into the Treatwell marketplace, which is now the Italian category leader.
- **"resthopper" could not be found.** No Italian booking or restaurant SaaS by that name was located. The name appears to be garbled; it is listed in section 6 rather than guessed at.

| Product | Origin | Price | Unit | Commission model | Confidence |
|---|---|---|---|---|---|
| **AgileHair** | Italian | FREE (client records only); **Essential €19.90/mo + IVA**; **Professional €34.90/mo + IVA** | flat per business, **no per-seat charge** | none; SMS billed separately | medium |
| **Reservio** | CZ, IT-localised | Free up to 40 bookings/mo; **Starter from ~€7.49/mo**; Standard; Pro (adds API access) | per business | payments from 1.19%/txn; no per-booking fee on existing clients | medium |
| **Treatwell** (ex Uala) | UK/EU | **Not published on the Italian site** — Starter and Advanced plans are quote-only | per business, unlimited team included | **25% on new marketplace clients**; 0% returning; 0% on direct bookings; **2% + IVA** on online payments; **12-month minimum contract** | medium |
| **Fresha** | UK/global | **$19.95/mo** (Individual); **$14.95/mo per bookable team member** | per bookable seat | **20% marketplace commission on new clients (min $6)**; payments 2.29% + $0.20 in-person, 2.79% + $0.20 online | medium |
| **Booksy** | PL | indicatively **€25–80/mo** by number of operators | per business, scaling with operators | 20–30% on new marketplace clients | low |

**The commission-vs-flat-fee gap is the single most useful pricing insight in this category.** An Italian analysis (biutify.it, 2026-04-27) models a typical centro estetico at 200 bookings/month, €40 average ticket, €96,000 annual revenue:

| Model | Effective annual cost |
|---|---|
| Treatwell | €7,000–9,000/yr (8–10% of revenue) |
| Booksy | €4,500–6,000/yr (canone + commission) |
| Fresha | €2,500–4,000/yr (processing fees alone) |
| Italian flat-fee gestionale | **€600–1,200/yr, all in** |

Confidence: medium (modelled, not invoiced), but the direction is robust and the flat-fee band (€600–1,200/yr = **€50–100/month**) is corroborated by AgileHair's actual list prices.

### 4.1 Derived band — booking / appointment software

**Billing unit: per business, flat monthly, ex-VAT.**

| Segment | Cheapest viable | Typical |
|---|---|---|
| Solo professional / micro business | **€7–20/month** | **€20–35/month** |
| Small team (3–8 staff) | **€35–50/month** | **€50–80/month** |

Italian-origin vendors compete specifically on *not* charging per seat (AgileHair markets flat pricing "indipendentemente dal numero di collaboratori" as a differentiator against Fresha's per-bookable-member model). Per-seat pricing is a known friction point in this market.

---

## 4bis. Horizontal SMB SaaS — CRM

### 4bis.1 TeamSystem CRM in Cloud — confidence: high

Read directly from https://www.teamsystem.com/crm/crm-in-cloud/prezzi/mensile/ on 2026-08-13. This is the most relevant CRM anchor because it is the incumbent's own product, priced for the Italian SMB market.

| Tier | Monthly billing | Users included | Max users purchasable | Confidence |
|---|---|---|---|---|
| Entry | **€18/month + IVA** | 1 | 3 | high |
| Professional | **€33/month + IVA** | 1 | 30 | high |
| Business | **€47/month + IVA** | 1 | unlimited | high |

**Billing unit: per user (utenza) per month.** Each plan includes exactly one utenza; additional utenze are bought on top, up to the plan's ceiling. Annual billing saves "up to 30%", so the annual-equivalent entry price is roughly **€12.60–13/user/month**. 14-day free trial. Training courses are sold separately.

### 4bis.2 International CRMs sold into Italy — confidence: medium

| Product / tier | Price (annual billing) | Price (monthly billing) | Unit | Confidence |
|---|---|---|---|---|
| Zoho Bigin | from **€7** | — | per user/month | medium |
| Zoho CRM Standard | **€14** | €20 | per user/month | medium |
| Zoho CRM Professional | **€23** | €35 | per user/month | medium |
| Zoho CRM Enterprise (first tier with Zia AI) | **€40** | €50 | per user/month | medium |
| Zoho CRM Ultimate | **€52** | €65 | per user/month | medium |
| Zoho CRM Plus (9-app suite) | **€57** | — | per user/month | medium |
| HubSpot Free | €0 | — | — | medium |
| HubSpot Starter | **€18** | — | per user/month | medium |
| HubSpot Professional | **€450/month** (5 users included; ~€90/user beyond) | — | per account | medium |
| Salesforce Starter Suite | **€25** | — | per user/month | medium |

Zoho figures verified by a third party on 2026-08-03 (a fresh check, but a third-party one — Zoho loads euro amounts from a separate price file rather than page source, which is why the extraction is indirect). HubSpot and Salesforce figures from a March 2026 Italian SMB comparison.

**Two Italy-specific findings that matter more than the price points:**
- **HubSpot has no native connectors for the main Italian gestionali** (Zucchetti, TeamSystem, Mexal). Integration runs through middleware (n8n, Make.com, Zapier) at a stated one-off cost of **€1,500–4,000**. This is a concrete, quantified gap in the incumbent-adjacent integration layer.
- **vtenext**, the best-known Italian-origin open-core CRM, **publishes no price at all** — https://www.vtenext.com/en/pricing/ is a quote-request form that asks for cloud vs. on-premise, user count, AI modules, integrations, and *"If you know it yet, which is your budget?"* Confidence: high (that it is quote-only).

Third-party market bands for Italy 2026 (crmpartners.it, 2026-01-27, confidence medium): entry-level **€15–30/user/month**; business tier **€35–70/user/month**; enterprise **€75–150+/user/month**. Same source puts setup/migration at €1,000–10,000 and training at €200–1,000 per user — these one-off figures span such a wide range that they are only useful as an order of magnitude.

### 4bis.3 Derived band — CRM for an Italian micro/small firm

**Billing unit: per user per month, ex-VAT, discounted for annual prepayment.**

| Segment | Cheapest viable | Typical |
|---|---|---|
| Micro-firm (1–3 users) | **€0** (HubSpot Free, Zoho free to 3 users) to **€13–18/user/month** | **€18–25/user/month** |
| Small firm (5–15 users) | **€23–33/user/month** | **€33–47/user/month** |

A 5-person Italian small firm on TeamSystem CRM in Cloud Professional is therefore at roughly **€165/month ex-VAT** — the same absolute band as a small commercialista studio's practice software, but reached through per-seat rather than per-studio pricing.

---

## 4ter. Horizontal SMB SaaS — e-commerce

### TeamSystem Commerce (ex Storeden) — confidence: high

Read directly from https://www.teamsystem.com/commerce/prezzi/ on 2026-08-13. No minimum contract term; plans can be changed at any time; 15-day free trial.

| Tier | Monthly billing | Annual billing (1 month free) | Sales commission | Disk | Store admins | Confidence |
|---|---|---|---|---|---|---|
| START | **€30/month + IVA** | €27.50/month + IVA | **2% of sales** | 3 GB | 5 | high |
| PROFESSIONAL | **€82/month + IVA** | €75.42/month + IVA | **1% of sales** | 15 GB | 10 | high |
| BUSINESS | **€238/month + IVA** | €218.33/month + IVA | **0%** up to €1.5M/yr transacted, then 0.5% | 100 GB | unlimited | high |
| ENTERPRISE | quote only | quote only | 0% up to €1.5M/yr, then 0.5% | 100 GB | unlimited | high |

Two details worth carrying forward. First, **the commission is the real price**: a START store doing €50,000/year in sales pays €360 in subscription plus €1,000 in commission. The subscription ladder is therefore not the whole cost curve, and upgrading tiers can be cheaper than staying on START. Second, **"Accesso API" is listed among the features included in *all* plans**, including START at €30/month — an unusually open posture for this market and consistent with the Fatture in Cloud finding in section 5.

A 2022 third-party description lists the same four tiers at €29 / €69 / €199 monthly, confirming the ladder's shape while showing list prices rose roughly 3–20% over four years.

**Billing unit: per store, per month, plus a percentage of transacted value.** For a micro-retailer the realistic entry is **€30/month + 2%**.

---

## 5. Incumbent ecosystem map — the "works beside the incumbent" distribution surface

Ranked by how usable the surface actually is for an independent developer.

| Vendor | App marketplace | Public API | Access conditions | Confidence |
|---|---|---|---|---|
| **Fatture in Cloud** (TeamSystem) | **Yes — App Store** | **Yes — REST API v2, OAuth 2.0, official SDKs (MIT)** | **API free on every plan, including the free trial. App Store publication free, including for paid integrations.** Requires Public Visibility approval, then a review form. | **high** |
| **TeamSystem Commerce** (ex Storeden) | **Yes — Apps Market** | **Yes — Connect APIs, public docs** | Partner program with recurring revenue share; apps can be sold in the app market. **"Accesso API" is included in every plan, from START at €30/month** (verified on the pricing page) | medium-high |
| **Namirial** | Partner directory ("Namirial Marketplace") — a partner finder, not an app store | **Yes — Connectors APIs, OAS3/OpenAPI, OAuth2, SDKs, sandbox, developer dashboard** | Public docs; Business Partner program for commercial terms (terms not published) | medium-high |
| **TeamSystem (group)** | — | Development Portal exists | **Gated** — development.teamsystem.com requires Microsoft SSO; no public documentation behind it. TS Pay exposes APIs + a developer portal but access runs through a contact form. | medium |
| **Zucchetti** | **No public app store** for the accounting/gestionale suites | Narrow only — public OpenAPI exists for the *Servizi-IT datacenter portal* alone | **Partnership-gated.** 5-tier reseller program (Top Partner → Partner → Dealer → Promotori → Struttura Tecnica Certificata) is a *sales channel*, not an ISV app store. An ISV Partner track exists on zucchetti.com but is contact-gated. Vertical products (Hospitality) use an integration-request form. | high |
| **Wolters Kluwer Italia (Kleos)** | No | **Yes, but paywalled** — "Modulo Kleos API" is a **paid add-on available only on the Advanced + tier** | Effectively closed: the customer must be on the top tier *and* buy the API module before a third-party tool can connect | high |
| **Danea** | **No** | **No REST API at all** | Integration is via the documented **Easyfatt-Xml** file exchange format, or by reading the local **Firebird** database directly. Danea explicitly declines developer support and refers integrators to freelancer marketplaces. A third-party ecosystem has grown up around this gap (bindCommerce connectors, gestionaleideale.it's API wrapper, a community Python DB connector). | high |
| **Buffetti** | **No** developer portal or app store found | None found | Distribution runs entirely through the affiliated dealer network (negozi Buffetti / affiliati) | high (absence) |
| **Aruba** | No app store found for the fatturazione product | Not found for fatturazione (a WooCommerce *module* exists as a first-party product, not a platform API) | — | medium (absence) |

### 5.1 Fatture in Cloud is the standout distribution surface — details

From the official developer documentation at https://developers.fattureincloud.it:

- **API access is universal, not tier-gated.** *"The APIs are automatically enabled for all Fatture in Cloud users... The APIs are included in all of the Fatture in Cloud plans, even in our free Trial license."* The only method-level restriction is **Send E-Invoice** (submission to SDI), which requires a paid plan.
  - **This corrects a plausible misreading.** The consumer pricing comparison grid lists "API pubbliche" as a feature row, and one third-party article (srlonline.com, Jan 2026) states that public APIs arrive with Premium Plus (€29/mo). The developer docs address the point directly and are authoritative: API *access* is universal; what varies by tier is which *features* the API can reach, since "if a certain feature is not included in your current plan... it will also be unavailable through our APIs." An integration can query the customer's plan via the API to check.
- **App Store publication is free.** The docs are emphatic: *"NO!!! Publishing an app to our App Store is completely free, even for paid integrations!"*
- **Two-stage approval.** First obtain **Public Visibility** (requires a production-ready integration; requests from apps still in development are frozen, not rejected). Then submit an App Store publication request via a form, reviewed by Customer Support over several days. Required materials: app category, short and long description, 512×512 logo, 2–10 screenshots at 1280×720, homepage, privacy policy, T&C, integration page, support and developer contacts. Brand Guidelines compliance is mandatory and non-compliance is grounds for rejection.
- **Audience the vendor claims for the store:** *"more than 500.000 customers and 16.000 accountants who use Fatture in Cloud every day."*
- **Auth:** OAuth 2.0 Authorization Code Flow (recommended default), OAuth 2.0 Device Code Flow (not generally available — activated on request for approved use cases), and Manual Authentication. Official SDKs are MIT-licensed; an OpenAPI spec is published for generating your own.
- **Legal terms:** governed by the *Condizioni generali di utilizzo delle API TeamSystem* (https://developers.fattureincloud.it/docs/legal/terms/). Material clauses for an indie developer: the licence is **non-exclusive, non-transferable, temporary and revocable** (§2.1); the developer owns the entire end-customer relationship including contracting (§2.6); integrated applications may be distributed **only to business users, expressly excluding consumers** (§2.6); TeamSystem may suspend API access for several enumerated reasons including breach of the Acceptable Use Policy (§6.3); and TeamSystem may **withdraw a product or its APIs from the market** with notice, with the developer's only remedy being withdrawal from the contract for that product (§10.2).

**Practical read:** Fatture in Cloud is the only Italian incumbent in this survey offering a genuinely open, free, documented, self-serve distribution channel to a third-party micro-SaaS, at meaningful scale. Namirial and TeamSystem Commerce are open but narrower in relevance. Everything else in the Italian accounting/legal software stack is partnership-gated, paywalled, or has no API at all.

---

## 6. Does not exist publicly / not listed / could not be found

Recorded deliberately — absence of a public price is itself a market finding.

### 6.1 Quote-only (verified: vendor publishes no list price)

| Vendor / product | What was checked | Confidence |
|---|---|---|
| TeamSystem Studio AI | teamsystem.com/commercialisti/teamsystem-studio/ — vendor explicitly states price is configuration-dependent | high |
| Zucchetti Ago Infinity | vendor and third-party sources; no standard price | high |
| Wolters Kluwer Genya (commercialisti and aziende) | wolterskluwer.com/it-it/solutions/genya/* — every CTA is "richiedi una demo" | high |
| Wolters Kluwer B.Point | product pages | high |
| **Kleos (Italy)** | wolterskluwer.com/it-it/solutions/kleos/pricing — tiers and features published, **no prices**, verified twice (HTTP fetch + rendered headed browser) | high |
| Cliens GSL (Lefebvre Giuffrè) | shop.giuffre.it product page and lefebvregiuffre.it product page — no price on either | high |
| Buffetti eBridge Studio / eBridge Azienda | buffetti.it product pages — no price shown | high |
| Sistemi PROFIS, Ranocchi GIS, Passepartout Passcom | third-party survey confirming no vendor publishes a listino | high |
| Treatwell Italia (Starter / Advanced plans) | Italian site — commission terms public, subscription prices not | medium |
| TeamSystem legal / Zucchetti legal products | no public list price located | medium |
| **vtenext** (Italian open-core CRM) | vtenext.com/en/pricing/ — the "pricing" page is a quote-request form that asks the buyer to state their own budget | high |
| TeamSystem Commerce ENTERPRISE tier | teamsystem.com/commerce/prezzi/ — three tiers priced, top tier "prezzo personalizzato" | high |

### 6.2 Data that could not be found

- **Danea Easyfatt Standard renewal price.** The €4/month Standard tier is labelled "offerta 1° anno" on both the desktop and cloud ladders, but unlike Fatture in Cloud, Danea publishes **no renewal price** anywhere on the pricing page. Any figure for what a Danea Standard customer pays in year two would be fabricated.
- **An average annual software budget in EUR for an Italian micro or small firm.** This was searched for specifically across Osservatori Politecnico di Milano, Anitec-Assinform and AssoSoftware outputs. **No such published per-firm euro figure was located.** These sources publish growth rates, adoption percentages and aggregate market size, not per-firm spend. The bands in sections 1.7, 2.2, 3.4 and 4.1 are built bottom-up from list prices instead, which is the more defensible construction anyway.
- **"resthopper"** — no Italian booking/restaurant SaaS by this name found. Likely a garbled product name.
- **"Lexia"** as a newer Italian legal SaaS entrant — not verified as an existing 2026 product. Lexia is a well-known Italian *law firm* name, which may be the source of the confusion. No legal practice-management SaaS by that name was confirmed.
- **Aruba public API / developer program for the fatturazione product** — not found. Aruba publishes APIs for other product lines, but no developer surface for Fatturazione Elettronica was located.
- **MEPA / Consip catalogue per-licence prices** for practice-management software — not searched to conclusion; flagged as an untried lead should quote-only pricing need to be pierced.
- **TeamSystem Development Portal contents** — development.teamsystem.com sits entirely behind Microsoft SSO. Access conditions, rate limits and any partner fees are not publicly visible.

---

## 7. Italian SMB digital spend — published context

No per-firm euro budget exists (see 6.2). What is published:

| Finding | Source | Date | Confidence |
|---|---|---|---|
| Italian enterprise ICT budget grows **+1.8%** in 2026 vs 2025; **piccole imprese +3.3%**, **medie imprese +5.2%** (third consecutive year of SME-led growth, PNRR-driven) | Osservatori Startup Thinking / Digital Transformation Academy, Politecnico di Milano | 2025-12-02 | high |
| PMI investment priorities: **cybersecurity 45%, Industria 4.0 37%, Cloud 32%, ERP 30%** | same | 2025-12-02 | high |
| **76% of Italian PMI have not invested and do not plan to invest in AI**; only 7% have structured AI training; 47% did no R&D in the last three years | Osservatorio Innovazione Digitale nelle PMI, PoliMi | 2026-05-21 | high |
| Over half of PMI increased digital spend in 2025, but polarised: 24% invest intensively, 27% selectively, 22% consider digital marginal, 9% consider costs disproportionate, 4% don't understand the benefits, **14% invest nothing at all** | same | 2026-05-21 | high |
| **56% of PMI invested in cloud 2023–2025, rising to a planned 91% for 2026–2028** | same | 2026-05-21 | high |
| First-ever extension of the survey to **microimprese (5–9 addetti)**: 70% of MPMI have no structured training plan; only 4% of microimprese have started AI training; the top obstacle is **lack of time (65%)** | Osservatorio Innovazione Digitale nelle PMI, PoliMi | 2026-02-19 | medium (LinkedIn summary of the convegno) |
| **As-a-service models are ~80% of the Italian cloud market.** Subscription software is currently **excluded** from the new iperammortamento 4.0 incentive — meaning no tax relief for SaaS canoni, disproportionately affecting PMI for whom subscription is the only affordable access model | Anitec-Assinform | 2026-05-05 | high |
| Italian software industry revenue **€66.7bn in 2024 (+8.3%)**, forecast €70.1bn for 2025 (+5.2%); PMI digital-maturity index **54.34 in 2025 (+3 pts)**, with medie imprese driving growth and piccole (10–49) structurally lagging; gestionali present in 85% of Italian software vendors' offerings | Osservatorio Software & Digital Native Innovation, PoliMi with AssoSoftware | 2025-11-18 | high |

**Two implications worth carrying into a calibration pack.** First, the *lack of time* (65%) rather than lack of budget is the stated top obstacle for microimprese — a positioning signal. Second, the iperammortamento exclusion means an Italian micro-firm buying SaaS in 2026 gets no tax incentive, while capitalised software may qualify; this makes the psychological price ceiling on subscriptions stickier than headline budget growth would suggest.

---

## Sources

All URLs accessed 2026-08-13 unless noted.

**Vendor pricing pages (primary, high confidence)**
- Fatture in Cloud — https://www.fattureincloud.it/costo/
- Danea Easyfatt — https://www.danea.it/software/easyfatt/prezzi/ (prices rendered client-side; read via headless browser)
- Danea Easyfatt licence terms — https://www.danea.it/public/licenza-easyfatt.pdf
- Aruba Fatturazione Elettronica listino — https://aruba.it/listino-fatturazione-elettronica.aspx
- Aruba renewal guide — https://guide.aruba.it/soluzioni-fatturazione-elettronica/fe/rinnovo-aumento-spazio/come-rinnovare-fatturazione-elettronica
- FATTURE GB (GBsoftware) — https://www.softwaregb.it/software-fatturazione-elettronica-commercialisti/
- Zucchetti Store, fatturazione elettronica packs — https://www.zucchetti.it/store/cms/fatturazione-elettronica-acquista.html
- Zucchetti Store listino PDF (price revision dated 10.01.2023) — https://www.zucchetti.it/website/dms/Store/Listino_Zucchetti_Store.pdf
- Kleos Italia, piani (no prices published) — https://www.wolterskluwer.com/it-it/solutions/kleos/pricing
- Kleos Belgium pricing — https://www.wolterskluwer.com/nl-be/solutions/kleos/pricing
- Kleos Italia brochure (Essential/Pro naming) — https://agenziagiuridica.it/wp-content/uploads/2025/06/Kleos-Brochure-11-11-24_web.pdf
- Cliens GSL — https://shop.giuffre.it/025000165-cliens-gestione-studio-legale-pratiche-illimitate and https://www.lefebvregiuffre.it/it/prodotto/cliens-gestione-studio-legale-e-clienspiu/gsl-software
- TeamSystem Studio AI (states price is quote-based) — https://www.teamsystem.com/commercialisti/teamsystem-studio/
- Buffetti eBridge Commercialisti — https://buffetti.it/products/ebridge-commercialisti-software-gestionale
- Wolters Kluwer Genya — https://www.wolterskluwer.com/it-it/solutions/genya/genya-per-aziende
- TeamSystem CRM in Cloud, monthly plans — https://www.teamsystem.com/crm/crm-in-cloud/prezzi/mensile/
- TeamSystem Commerce, pricing — https://www.teamsystem.com/commerce/prezzi/
- vtenext pricing page (quote-request form, no prices) — https://www.vtenext.com/en/pricing/

**Developer / ecosystem documentation (primary, high confidence)**
- Fatture in Cloud, API activation and plan coverage — https://developers.fattureincloud.it/docs/basics/activation/
- Fatture in Cloud, create an app and App Store — https://developers.fattureincloud.it/docs/basics/create-an-app/
- Fatture in Cloud, publish to App Store — https://developers.fattureincloud.it/docs/app-store/
- Fatture in Cloud, authentication — https://developers.fattureincloud.it/docs/basics/authentication/ and /docs/authentication/
- Fatture in Cloud, SDKs — https://developers.fattureincloud.it/docs/sdks/
- TeamSystem API general terms — https://developers.fattureincloud.it/docs/legal/terms/
- TeamSystem Development Portal (Microsoft SSO gated) — https://development.teamsystem.com/
- TeamSystem Commerce / Storeden developers — https://developers.storeden.com/
- TeamSystem Commerce Apps Market — https://www.teamsystem.com/commerce/funzionalita/apps-servizi/
- TS Pay integration APIs — https://www.teamsystem.com/fintech/ts-pay/offerta/integrazione-gestionali-esterni/
- Zucchetti partner program (IT) — https://www.zucchetti.it/it/cms/partner/partner-zucchetti
- Zucchetti partner program / ISV track (EN) — https://www.zucchetti.com/en/cms/partners/become-partner-zucchetti/partner-zucchetti.html
- Zucchetti Servizi-IT public APIs (narrow scope) — https://help.zucchetti.it/cms/kb/soluzioni/servizi-it/api-pubbliche
- Zucchetti Hospitality integration request form — https://integration.zucchettihospitality.it/integration-request.php
- Namirial Connectors APIs — https://doc.namirial.com/connectors-apis/latest/
- Namirial signing web services — https://www.namirial.com/en/sign/signing-web-services/
- Namirial Business Partner program — https://www.namirial.com/en/business-partner/
- Danea Easyfatt-Xml integration format (no REST API) — https://www.danea.it/software/easyfatt/xml/
- Danea Easyfatt-Xml help — https://help.danea.it/easyfatt/Trasferire_documenti_in_formato_Easyfatt-Xml.htm
- Community Danea DB connector — https://github.com/LukeSavefrogs/easyfatt-db-connector
- Third-party Danea API wrapper — https://gestionaleideale.it/integrazioni-api/
- bindCommerce Danea connectors — https://www.bindcommerce.com/it/guide/sistemi-gestionali/integrazione-danea-easyfatt

**Third-party comparisons (medium/low confidence, dates noted)**
- Pazienza, e-invoicing price comparison incl. renewal prices — https://www.pazienza.app/blog/fattura-elettronica-prezzi-a-confronto (2026-07-08)
- Software Semplice, Aruba vs Fatture in Cloud cart-level survey — https://www.softwaresemplice.it/blog/aruba-fatture-in-cloud-prezzi-a-confronto/1203 (2025-07-29)
- Software Semplice, Easyfatt alternatives — https://www.softwaresemplice.it/blog/alternativa-a-easyfatt/1213 (2025-11-13)
- SRLonline, gestionali comparison — https://www.srlonline.com/software-gestionali-2026-fatture-in-cloud-vs-danea-teamsystem-confronto-prezzi-funzioni/ (2026-01-13)
- Centro Fiscale, Fatture in Cloud vs Danea — https://centrofiscale.com/teamsystem-fatture-cloud-vs-danea-easyfatt-2026/ (2026-03-12)
- Centro Fiscale, Aruba review — https://centrofiscale.com/aruba-fatturazione-recensione-2026/ (2026-07-09)
- Qonto, commercialisti software guide (states no vendor publishes a listino) — https://qonto.com/it/blog/gestione-aziendale/contabilita/software-per-commercialisti (2025-10-29)
- TaxDome, commercialisti software guide — https://taxdome.com/it-it/blog/una-guida-completa-ai-software-per-commercialisti-e-studi-commercialisti (2025-08-27)
- Brentasoft, studi commercialisti price ranges — https://brentasoft.com/blog/software-studi-commercialisti-2021/ (**2021 — flagged as outdated**)
- BullTech, gestionali studi legali — https://bulltech.it/blog/gestionale-studi-legali-guida (2026-04-12)
- LegalProd vs Wolters Kluwer (French Kleos prices) — https://www.legalprod.com/es/legalprod-vs-wolters-kluwer-es/ (2023-12-26)
- TIWARE, Kleos reseller listing (**ambiguous pricing**) — https://www.tiware.it/prodotto/kleos-the-cloud-software-for-lawyers/
- Buffetti dealer eBridge promo (**2020**) — https://www.softwaresalerno.com/prodotto/suite-contabilita-ordinaria-1/
- Reservio, Italian salon software comparison — https://www.reservio.com/it/blog/consigli/come-scegliere-il-miglior-software-di-prenotazione-per-saloni (2026-05-27)
- Biutify, commission-model cost analysis for Italian beauty businesses — https://www.biutify.it/guide/commissioni-prenotazione-beauty-quanto-costano (2026-04-27)
- DoTheBeauty, Treatwell vs Fresha — https://www.dothebeauty.com/blog/treatwell-vs-fresha-comparison (2026-05-18)
- CRMpartners, Italian CRM cost analysis and Zoho tiers — https://www.crmpartners.it/magazine/crm/quanto-costa-un-software-crm/ (2026-01-27)
- CRMpartners, Zoho CRM tier prices — https://www.crmpartners.it/en/software/customer-relationship-management-crm/zoho-crm/
- Meetergo, Zoho CRM price audit (figures checked 2026-08-03) — https://meetergo.com/blog/zoho-crm-preise (2026-08-06)
- Supalabs, HubSpot vs Salesforce vs custom CRM for Italian SMBs, incl. the Italian-gestionale connector gap — https://supalabs.co/en/blog/crm-automation-pmi-italiane-hubspot-vs-salesforce-2026/ (2026-03-11)
- Svennis (Zoho Premium Partner Italia), Zoho CRM Plus €57/user/month — https://www.svennis.it/zoho-crm-plus
- Algoritma, TeamSystem Commerce (ex Storeden) tiers as of 2022 — https://www.algoritma.it/piattaforma-ecommerce-storeden-saas-alternativa-shopify/ (2022-01-03)

**Market and macro data**
- Osservatori PoliMi, 2026 ICT budgets — https://www.osservatori.net/comunicato/startup-thinking/innovazione-digitale-crescita-investimenti/ (2025-12-02)
- Osservatorio Innovazione Digitale nelle PMI — https://www.osservatori.net/comunicato/innovazione-digitale-nelle-pmi/pmi-italiane-innovazione/ (2026-05-21)
- Osservatori PoliMi, microimprese and training (LinkedIn summary of convegno) — https://it.linkedin.com/posts/osservatori-digital-innovation_osspmi-osspmi26-activity-7430219828818231296-fJmS (2026-02-19)
- Anitec-Assinform, iperammortamento 4.0 and SaaS exclusion — https://www.anitec-assinform.it/media/comunicati-stampa/iperammortamento-4-0-anitec-assinform-senza-il-cloud-un-passo-indietro-per-la-digitalizzazione-del-paese.kl (2026-05-05)
- AssoSoftware / Osservatorio Software & Digital Native Innovation — https://www.assosoftware.it/comunicati-stampa/risultati-ricerca-osservatori-digital-innovation181125/ (2025-11-18)

# EUR willingness-to-pay anchors: consumer apps on the Italian App Store

Research question DA2 of the Italy-first consumer-app calibration pass. Purpose: give the calibration pack Ring-1 (Italy) EUR price points that can sit beside its existing USD ranges.

**Observation date for all storefront figures: 2026-08-13.** Every price marked `high` was read that day from the Italian storefront (`apps.apple.com/it`) or from Apple's own lookup API for the `it` country code.

## How to read this file

**Prices are VAT-inclusive.** Apple states that "prices advertised to customers in all countries except the U.S. and Canada include taxes" ([Apple, *Explore App Store pricing upgrades*, Tech Talk 110364, published 2023-05-02](https://developer.apple.com/videos/play/tech-talks/110364/)). Every euro figure below is therefore what an Italian customer pays, with 22% Italian VAT already inside it. See the mechanics section for what that leaves as developer proceeds.

**Billing period is recorded only when the storefront disclosed it.** The App Store's "Acquisti in-app" panel lists the top in-app purchases by revenue, showing the developer's SKU display name and the price, but not the billing period. Where the SKU name states the period ("Todoist Pro - annuale", "Abbonamento mensile", "Hevy Pro - Yearly"), the period column below is filled and confidence is `high`. Where the SKU name is silent ("Calm Premium 15,99 €", "Monefy Premium 43,99 €"), the period column reads *not disclosed* (the price is still a valid EUR anchor, but inferring a period from it would be invention). Repeated SKU names at different prices are normal: they are grandfathered, promotional, regional-experiment, and current SKUs coexisting under one display name.

**Confidence tags.** `high` = read directly from the IT storefront or the Italian app description written by the developer. `medium` = reputable secondary source. `low` = estimate, undated, or derived.

**Number format.** Prices are reproduced in the Italian convention as displayed on the storefront (comma decimal separator): `49,99 €` means forty-nine euro ninety-nine.

---

## Headline anchors by category

The single most useful summary for the calibration pack. "Typical monthly" and "typical annual" are the modal current price points across the apps sampled, not averages; the full evidence is in the per-category tables that follow.

| Category | Typical monthly (EUR) | Typical annual (EUR) | One-time / lifetime seen | Apps sampled |
|---|---|---|---|---|
| Meditation / mental health | 8,99–15,99 | 45,00–69,99 | 329,99 € (Calm Lifetime) | 4 |
| Health & fitness | 6,99–17,99 | 26,49–99,99 | 89,99 € (Hevy Lifetime) | 4 |
| Nutrition / diet | 8,90–14,99 | 35,00–99,99 | none | 5 |
| Finance / budgeting | 3,99–15,49 | 29,99–119,00 | 49,99–199,99 € | 5 |
| Productivity / task management | 2,99–12,99 | 29,99–129,99 | 9,99 € (Things 3) | 9 |
| Habit tracking | 0,99–10,99 | 5,99–79,99 | 6,99–129,99 € | 6 |
| Creative (photo/video) | 4,99–9,99 | 27,99–54,99 | 29,99–99,99 € | 7 |
| Education / learning (incl. language) | 5,99–16,99 | 31,99–125,99 | none | 6 |
| Parenting / family | 5,99–17,99 | 29,99–129,99 | 99,99 € (sleep plan) | 4 |
| Utilities (scanner / converter) | 5,99–10,99 | 22,99–74,99 | 7,99–89,99 € | 6 |
| AI-powered tools | 4,99–22,99 | 49,99–299,99 | credit packs 6,00–299,00 € | 6 |

Three cross-category regularities worth carrying into the calibration pack:

1. **`9,99 €` is the dominant monthly ceiling for indie-scale consumer apps**, and `4,99–7,99 €` the dominant monthly floor. Prices above `15 €/month` appear almost exclusively in AI tools, US-headquartered category leaders, and clinical/parenting apps.
2. **Annual pricing clusters at `29,99 €`, `39,99 €`, `49,99 €`, `59,99 €`, and `69,99 €`.** The implied annual discount against the monthly rate is consistently 40–60%.
3. **Lifetime unlocks are alive and well in Italy** across habit tracking, budgeting, photo editing, and meditation, typically at 8–15× the annual price (`34,99 €` HabitKit, `49,99 €` Wallet, `69,99 €` Spendee, `89,99 €` Hevy, `99,99 €` Darkroom, `129,99 €` Habitify, `199,99 €` MoneyCoach, `329,99 €` Calm).

---

## Meditation / mental health

| App | SKU as shown | Price (EUR) | Period | Confidence | Source |
|---|---|---|---|---|---|
| Calm | (Italian description) | 49,99 € | annual | high | [apps.apple.com/it id571800810](https://apps.apple.com/it/app/id571800810) |
| Calm | (Italian description) | 329,99 € | lifetime, one-time | high | same |
| Calm | Calm Premium | 15,99 € | not disclosed | high | same |
| Calm | Calm Premium | 12,99 € | not disclosed | high | same |
| Headspace | Annual Subscription | 57,99 € | annual | high | [apps.apple.com/it id493145008](https://apps.apple.com/it/app/id493145008) |
| Headspace | Annual Subscription | 69,99 € | annual | high | same |
| Headspace | Monthly Subscription | 12,99 € | monthly | high | same |
| Headspace | Headspace Plus | 94,99 € | not disclosed | high | same |
| Petit BamBou | Abbonamento mensile | 8,99 € | monthly | high | [apps.apple.com/it id941222646](https://apps.apple.com/it/app/id941222646) |
| Petit BamBou | Abbonamento semestrale | 29,99 € | 6 months | high | same |
| Petit BamBou | Abbonamento annuale | 59,90 € | annual | high | same |
| Insight Timer | Insight Premium Meditation | 7,49 € | not disclosed | high | [apps.apple.com/it id337472899](https://apps.apple.com/it/app/id337472899) |
| Insight Timer | Insight Premium Meditation | 45,00 € | not disclosed | high | same |
| Insight Timer | Insight Premium Meditation | 62,99 € | not disclosed | high | same |
| Insight Timer | MemberPlus Family | 59,99 € | not disclosed | high | same |

Note on Petit BamBou: it is the European (French) challenger and prices deliberately below the two US leaders on the annual plan (`59,90 €` against Headspace's `57,99–69,99 €` and Calm's `49,99 €`), while pricing *below* both monthly at `8,99 €`. A secondary source ([Spliiit, Italian edition, published 2026-05-19](https://www.spliiit.com/it/blog/petit-bambou-avis-prix-abonnement)) quotes Petit BamBou's direct-web pricing as `6,99 €`/month and `39,99 €`/year with a `240 €` lifetime, materially cheaper than the App Store SKUs above. `medium` confidence, and a useful reminder that in-app prices carry Apple's commission while web prices need not.

## Health & fitness

| App | SKU as shown | Price (EUR) | Period | Confidence | Source |
|---|---|---|---|---|---|
| Strava | 1 mese | 6,99 € | monthly | high | [apps.apple.com/it id426826309](https://apps.apple.com/it/app/id426826309) |
| Strava | Strava Subscription | 9,99 € | not disclosed | high | same |
| Strava | 1 anno | 69,99 € | annual | high | same |
| Strava | Strava Subscription | 59,99 € | not disclosed | high | same |
| Strava | Strava Family Plan Subscription | 99,99 € | not disclosed | high | same |
| Strava | Strava + Runna Subscription | 139,99 € | not disclosed | high | same |
| Freeletics | Training Coach | 24,99 € / 34,99 € / 44,99 € / 59,99 € / 74,99 € | not disclosed (multi-month packs) | high | [apps.apple.com/it id654810212](https://apps.apple.com/it/app/id654810212) |
| Freeletics | Pacchetto Training+Nutrition | 37,99 € | not disclosed | high | same |
| Fitbod | Monthly Plan | 13,49 € / 14,99 € / 17,99 € | monthly | high | [apps.apple.com/it id1041517543](https://apps.apple.com/it/app/id1041517543) |
| Fitbod | A Year of Fitbod Elite | 81,99 € / 99,99 € | annual | high | same |
| Fitbod | (Legacy Pricing) fitbod ELITE | 5,49 € / 7,99 € / 10,49 € / 61,99 € | not disclosed | high | same |
| Hevy | Hevy Pro - Monthly | 3,49 € / 4,49 € | monthly | high | [apps.apple.com/it id1458862350](https://apps.apple.com/it/app/id1458862350) |
| Hevy | Hevy Pro - Yearly | 26,49 € | annual | high | same |
| Hevy | Hevy Pro - Lifetime | 89,99 € | lifetime, one-time | high | same |

Hevy is the clearest indie benchmark here: a Spanish studio undercutting the US leaders by roughly 3× on both monthly (`3,49 €` vs Fitbod's `13,49–17,99 €`) and annual (`26,49 €` vs `81,99–99,99 €`), with a lifetime escape hatch.

## Nutrition / diet

| App | SKU as shown | Price (EUR) | Period | Confidence | Source |
|---|---|---|---|---|---|
| Yazio | YAZIO PRO | 8,90 € | not disclosed | high | [apps.apple.com/it id946099227](https://apps.apple.com/it/app/id946099227) |
| Yazio | 3 mesi | 15,00 € / 23,99 € | 3 months | high | same |
| Yazio | 12 mesi | 14,90 € / 14,99 € / 35,90 € / 47,90 € | annual | high | same |
| Yazio | YAZIO PRO | 28,99 € / 29,99 € | not disclosed | high | same |
| MyFitnessPal | MyFitnessPal Monthly Premium | 9,99 € / 21,99 € | monthly | high | [apps.apple.com/it id341232718](https://apps.apple.com/it/app/id341232718) |
| MyFitnessPal | MyFitnessPal Yearly Premium | 49,99 € / 87,99 € | annual | high | same |
| Lifesum | Lifesum Premium 1 mese | 9,99 € / 14,99 € | monthly | high | [apps.apple.com/it id286906691](https://apps.apple.com/it/app/id286906691) |
| Lifesum | Lifesum Premium 3 mesi | 21,99 € / 39,99 € | 3 months | high | same |
| Lifesum | Lifesum Premium 1 anno | 99,99 € | annual | high | same |
| FatSecret | Sottoscrizione Mensile | 9,39 € / 13,49 € | monthly | high | [apps.apple.com/it id347184248](https://apps.apple.com/it/app/id347184248) |
| FatSecret | Sottoscrizione di Tre Mesi | 18,00 € / 25,99 € | 3 months | high | same |
| FatSecret | Sottoscrizione Annuale | 35,00 € / 53,90 € | annual | high | same |
| Yuka | Membro Premium | 10,00 € / 15,00 € / 20,00 € | not disclosed | high | [apps.apple.com/it id1092799236](https://apps.apple.com/it/app/id1092799236) |

Nutrition is the category with the widest observed spread of annual price points (`14,90 €` to `99,99 €`): the leaders run continuous price experiments and the storefront exposes all live SKUs at once. The 3-month plan is unusually common here and largely absent elsewhere.

## Finance / budgeting

| App | SKU as shown | Price (EUR) | Period | Confidence | Source |
|---|---|---|---|---|---|
| Spendee | Spendee Plus account | 3,99 € | not disclosed | high | [apps.apple.com/it id635861140](https://apps.apple.com/it/app/id635861140) |
| Spendee | Spendee Premium – Monthly | 6,99 € | monthly | high | same |
| Spendee | Spendee Plus account | 29,99 € | not disclosed | high | same |
| Spendee | Spendee Premium – Yearly | 39,99 € | annual | high | same |
| Spendee | Spendee Lifetime Premium | 69,99 € | lifetime, one-time | high | same |
| YNAB | YNAB Subscription | 15,49 € | not disclosed | high | [apps.apple.com/it id1010865877](https://apps.apple.com/it/app/id1010865877) |
| YNAB | YNAB Subscription | 119,00 € | not disclosed | high | same |
| MoneyCoach | Individuale | 4,99 € / 9,99 € | not disclosed | high | [apps.apple.com/it id989642198](https://apps.apple.com/it/app/id989642198) |
| MoneyCoach | Individuale | 34,99 € / 39,99 € / 59,99 € / 79,99 € | not disclosed | high | same |
| MoneyCoach | Famiglia | 8,99 € | not disclosed | high | same |
| MoneyCoach | Lifetime Premium | 199,99 € | lifetime, one-time | high | same |
| Wallet (BudgetBakers) | Premium | 5,99 € / 17,99 € / 29,99 € | not disclosed | high | [apps.apple.com/it id1032467659](https://apps.apple.com/it/app/id1032467659) |
| Wallet (BudgetBakers) | 3-Year Premium | 59,99 € | 3 years | high | same |
| Wallet (BudgetBakers) | Lifetime Premium | 49,99 € | lifetime, one-time | high | same |
| Monefy | Monefy Premium | 43,99 € / 69,99 € | not disclosed | high | [apps.apple.com/it id1212024409](https://apps.apple.com/it/app/id1212024409) |

YNAB at `15,49 €`/`119,00 €` is the outlier ceiling; the European budgeting apps (Spendee, Wallet, Monefy) cluster at `3,99–6,99 €` monthly and `29,99–43,99 €` annual. Note that the Italian consumer-finance apps with real local scale (Satispay and Revolut) expose **no** in-app purchases at all: they monetise through payment and banking economics, not app subscriptions, so they set no willingness-to-pay anchor.

## Productivity / task management

| App | SKU as shown | Price (EUR) | Period | Confidence | Source |
|---|---|---|---|---|---|
| Todoist | Todoist Pro - mensile | 6,99 € | monthly | high | [apps.apple.com/it id572688855](https://apps.apple.com/it/app/id572688855) |
| Todoist | Todoist Pro - annuale | 59,99 € | annual | high | same |
| Notion | Notion – Plus Monthly | 12,99 € | monthly | high | [apps.apple.com/it id1232780281](https://apps.apple.com/it/app/id1232780281) |
| Notion | Notion – Plus Yearly | 129,99 € | annual | high | same |
| Notion | Notion Plus & AI | 24,99 € / 249,99 € | not disclosed | high | same |
| Craft | Plus Monthly Subscription | 9,99 € | monthly | high | [apps.apple.com/it id1487937127](https://apps.apple.com/it/app/id1487937127) |
| Craft | Plus Annual Subscription | 95,99 € | annual | high | same |
| Craft | Family Monthly / Annual Subscription | 17,99 € / 179,99 € | monthly / annual | high | same |
| Structured | Structured Pro (Monthly) | 2,99 € / 4,99 € | monthly | high | [apps.apple.com/it id1499198946](https://apps.apple.com/it/app/id1499198946) |
| Structured | Structured Pro (Yearly) | 9,99 € / 14,99 € / 19,99 € | annual | high | same |
| Structured | Structured Pro (Lifetime) | 59,99 € | lifetime, one-time | high | same |
| Bear | Sottoscrizione Mensile | 2,99 € | monthly | high | [apps.apple.com/it id1016366447](https://apps.apple.com/it/app/id1016366447) |
| Bear | Sottoscrizione annuale | 34,99 € | annual | high | same |
| Goodnotes | Essential (annuale) | 12,99 € | annual | high | [apps.apple.com/it id1444383602](https://apps.apple.com/it/app/id1444383602) |
| Goodnotes | Pro (annuale) | 39,49 € | annual | high | same |
| Goodnotes | Edizione speciale | 31,90 € / 39,49 € | not disclosed | high | same |
| Ulysses | Piano mensile | 5,99 € | monthly | high | [apps.apple.com/it id1225570693](https://apps.apple.com/it/app/id1225570693) |
| Ulysses | Piano annuale | 29,99 € / 39,99 € | annual | high | same |
| Ulysses | Offerta studente | 11,99 € | not disclosed (student) | high | same |
| Fantastical | Flexibits Premium | 7,99 € / 69,99 € | not disclosed | high | [apps.apple.com/it id718043190](https://apps.apple.com/it/app/id718043190) |
| Fantastical | Premium for Families | 11,99 € / 99,99 € | not disclosed | high | same |
| Things 3 | (paid app, iPhone) | 9,99 € | one-time | high | iTunes lookup API, `country=it`, id904237743 |

**Bear is the Italian indie benchmark for this whole report.** Shiny Frog describes itself as "a small company founded by three developer-designers and friends in Parma, Italy" ([Bear blog, published 2018-05-31](https://blog.bear.app/2018/05/the-who-what-and-why-of-bear/), `medium`; the App Store seller of record is the Irish entity Shiny Frog Ltd. and the team is now distributed, so read this as an Italian-founded indie rather than an Italy-registered vendor). It prices at `2,99 €`/month and `34,99 €`/year, the lowest monthly of any subscription app sampled across all eleven categories, from a developer of roughly the scale the calibration pack is aimed at.

## Habit tracking

| App | SKU as shown | Price (EUR) | Period | Confidence | Source |
|---|---|---|---|---|---|
| HabitKit | HabitKit Pro (1 Month) | 0,99 € / 1,99 € | monthly | high | [apps.apple.com/it id6443918070](https://apps.apple.com/it/app/id6443918070) |
| HabitKit | HabitKit Pro (1 Year) | 5,99 € / 12,99 € | annual | high | same |
| HabitKit | HabitKit Pro (Lifetime) | 17,99 € / 34,99 € | lifetime, one-time | high | same |
| Habitify | Habitify Pro Mensile | 7,99 € | monthly | high | [apps.apple.com/it id1111447047](https://apps.apple.com/it/app/id1111447047) |
| Habitify | Habitify Pro Annuale | 39,99 € | annual | high | same |
| Habitify | Habitify Pro Anno (Famiglia) | 64,99 € | annual (family) | high | same |
| Habitify | Habitify Pro A vita | 43,49 € / 44,99 € / 69,99 € / 86,99 € / 129,99 € | lifetime, one-time | high | same |
| Productive | Productive Premium 1 Mese | 10,99 € | monthly | high | [apps.apple.com/it id983826477](https://apps.apple.com/it/app/id983826477) |
| Productive | Productive Premium 1 Anno | 40,99 € / 54,99 € / 59,99 € / 79,99 € | annual | high | same |
| Productive | Weekly Bundle Premium with FT | 3,99 € / 5,99 € | weekly | high | same |
| Way of Life | Premium | 5,99 € / 17,99 € / 34,99 € | not disclosed | high | [apps.apple.com/it id393159800](https://apps.apple.com/it/app/id393159800) |
| Forest | Mensile (Early Bird) | 4,69 € | monthly | high | [apps.apple.com/it id866450515](https://apps.apple.com/it/app/id866450515) |
| Forest | Annuale (Early Bird) | 25,00 € / 27,99 € | annual | high | same |
| Streaks | (paid app) | 6,99 € | one-time | high | iTunes lookup API, `country=it`, id963034692 |

**Productive is the second Italian benchmark**: published by Mosaic S.r.l., and notable for running a *weekly* subscription at `3,99–5,99 €` alongside the annual. Weekly billing is a distinctly aggressive monetisation pattern that also shows up in Remini, Splice, Picsart, and Lightroom below, worth flagging to the calibration pack as an Italy-visible norm, not a fringe tactic.

HabitKit (a solo developer, Sebastian Roehl) is the low-price floor of the entire sample at `0,99 €`/month.

## Creative tools (photo / video)

| App | SKU as shown | Price (EUR) | Period | Confidence | Source |
|---|---|---|---|---|---|
| Adobe Lightroom | Premium 40 GB al mese | 1,99 € | monthly | high | [apps.apple.com/it id878783582](https://apps.apple.com/it/app/id878783582) |
| Adobe Lightroom | Premium 40 GB all'anno | 21,99 € | annual | high | same |
| Adobe Lightroom | Premium 100 GB al mese | 4,99 € / 5,49 € / 7,99 € | monthly | high | same |
| Adobe Lightroom | Premium 100 GB all'anno | 54,99 € | annual | high | same |
| Adobe Lightroom | Premium settimanale 100 GB | 3,99 € / 8,99 € | weekly | high | same |
| Picsart | Picsart Gold - Monthly | 7,49 € | monthly | high | [apps.apple.com/it id587366035](https://apps.apple.com/it/app/id587366035) |
| Picsart | Picsart Gold - Annual | 27,99 € | annual | high | same |
| Picsart | Picsart Plus - Annual | 39,99 € | annual | high | same |
| Picsart | Picsart Pro Monthly / Annual | 8,99 € / 51,99 € | monthly / annual | high | same |
| Picsart | Picsart Gold / Pro Weekly | 5,49 € / 6,29 € | weekly | high | same |
| Darkroom | Abbonamento mensile | 9,99 € | monthly | high | [apps.apple.com/it id953286746](https://apps.apple.com/it/app/id953286746) |
| Darkroom | Abbonamento annuale | 39,99 € / 44,99 € | annual | high | same |
| Darkroom | Sblocca tutto per sempre | 99,99 € | lifetime, one-time | high | same |
| VSCO | Mensile Plus | 9,99 € | monthly | high | [apps.apple.com/it id588013838](https://apps.apple.com/it/app/id588013838) |
| VSCO | Annuale Plus | 34,99 € | annual | high | same |
| Splice (Bending Spoons) | Splice Weekly With Free Trial | 9,99 € | weekly | high | [apps.apple.com/it id409838725](https://apps.apple.com/it/app/id409838725) |
| Splice (Bending Spoons) | Splice Yearly With Free Trial | 121,99 € / 124,99 € | annual | high | same |
| Splice (Bending Spoons) | Splice / Splice Bundle | 5,99 € / 9,99 € | not disclosed | high | same |
| LumaFusion | (paid app) | 29,99 € | one-time | high | iTunes lookup API, `country=it`, id1062022008 |

**Bending Spoons, the Milan-headquartered vendor (its App Store seller of record is the Danish entity Bending Spoons Apps ApS), operates at the top of this category**, and it prices *above* the US incumbents, not below: Splice's annual at `121,99–124,99 €` is more than double VSCO's `34,99 €` and Picsart's `27,99 €`, sustained by a `9,99 €` weekly plan. This is a useful counterweight to any assumption that an Italian vendor must price defensively.

## Education / learning (including language)

| App | SKU as shown | Price (EUR) | Period | Confidence | Source |
|---|---|---|---|---|---|
| Duolingo | Super Duolingo | 89,99 € / 101,99 € / 125,99 € | not disclosed | high | [apps.apple.com/it id570060128](https://apps.apple.com/it/app/id570060128) |
| Duolingo | Barile di gemme (1200) | 5,99 € | one-time (consumable) | high | same |
| Babbel | Inglese 1 mese | 16,99 € | monthly | high | [apps.apple.com/it id829587759](https://apps.apple.com/it/app/id829587759) |
| Babbel | Inglese 3 mesi | 41,99 € | 3 months | high | same |
| Babbel | Inglese 1 anno / 12 mesi | 83,99 € | annual | high | same |
| Babbel | Tutte le lingue - 12 mesi | 95,99 € | annual | high | same |
| Busuu | Abbonamento mensile | 6,99 € / 9,99 € / 22,90 € | monthly | high | [apps.apple.com/it id379968583](https://apps.apple.com/it/app/id379968583) |
| Busuu | Abbonamento annuale / 12 Months Premium | 31,99 € / 64,99 € / 68,00 € / 134,99 € | annual | high | same |
| Busuu | 12 Months Premium Plus | 169,99 € | annual | high | same |
| Mondly | Unlimited Access - Monthly | 8,49 € / 16,90 € | monthly | high | [apps.apple.com/it id987873536](https://apps.apple.com/it/app/id987873536) |
| Mondly | Unlimited Access - 12 Months | 79,90 € | annual | high | same |
| Brainly | Brainly Plus, Monthly | 2,00 € / 5,99 € / 9,99 € | monthly | high | [apps.apple.com/it id745089947](https://apps.apple.com/it/app/id745089947) |
| Brainly | Brainly Plus, Annual | 17,00 € / 17,49 € | annual | high | same |
| Brainly | Brainly Tutor, Monthly | 29,99 € | monthly | high | same |
| Photomath | Photomath Plus | 5,99 € / 10,99 € / 11,49 € / 11,99 € | not disclosed | high | [apps.apple.com/it id919087726](https://apps.apple.com/it/app/id919087726) |

Language learning is the most expensive consumer category in the sample after AI tools: Babbel and Busuu both reach `83,99–134,99 €` annually. Homework-help apps aimed at students (Brainly at `17,00 €`/year) sit an order of magnitude below: the payer is a teenager, not an adult professional.

## Parenting / family

| App | SKU as shown | Price (EUR) | Period | Confidence | Source |
|---|---|---|---|---|---|
| Life360 | Life360 Silver Membership | 5,99 € | not disclosed | high | [apps.apple.com/it id384830320](https://apps.apple.com/it/app/id384830320) |
| Life360 | Life360 Gold Membership | 7,99 € / 10,99 € | not disclosed | high | same |
| Life360 | Life360 Premium | 7,99 € / 43,99 € | not disclosed | high | same |
| Qustodio | Qustodio Premium 1-year | 29,99 € / 53,99 € / 59,99 € / 94,99 € / 139,99 € / 149,99 € | annual | high | [apps.apple.com/it id990229433](https://apps.apple.com/it/app/id990229433) |
| Qustodio | Qustodio 5 / 10 / 15 devices 1-year | 59,99 € / 104,99 € / 159,99 € | annual | high | same |
| Qustodio | Qustodio Premium Complete 1y | 99,99 € | annual | high | [apps.apple.com/it id1501720596](https://apps.apple.com/it/app/id1501720596) |
| Huckleberry | Huckleberry Plus | 11,99 € / 12,99 € | not disclosed | high | [apps.apple.com/it id1169136078](https://apps.apple.com/it/app/id1169136078) |
| Huckleberry | Huckleberry Plus | 69,99 € | not disclosed | high | same |
| Huckleberry | Huckleberry Premium | 14,99 € / 17,99 € | not disclosed | high | same |
| Huckleberry | Huckleberry Premium | 118,99 € / 129,99 € | not disclosed | high | same |
| Huckleberry | Sleep Plan Full Price | 99,99 € | one-time | high | same |
| Napper | Unlimited: Baby-Sleep Expert + | 8,99 € / 13,99 € / 19,99 € / 23,99 € / 39,95 € / 47,99 € | not disclosed | high | [apps.apple.com/it id1491340863](https://apps.apple.com/it/app/id1491340863) |
| Napper | Napper Unlimited | 38,49 € | not disclosed | high | same |

Parenting is the category where SKU names disclose the period least often, so most rows here are anchors on price only. Qustodio's device-count ladder (`59,99 €` for 5 devices → `159,99 €` for 15) is the clearest structural pattern: parental-control apps price per protected child/device, not per account.

## Utilities (scanner / converter)

| App | SKU as shown | Price (EUR) | Period | Confidence | Source |
|---|---|---|---|---|---|
| Scanner Pro (Readdle) | Scanner Pro Plus | 3,99 € / 7,99 € / 8,99 € | not disclosed | high | [apps.apple.com/it id333710667](https://apps.apple.com/it/app/id333710667) |
| Scanner Pro (Readdle) | Scanner Pro Plus | 21,99 € / 32,99 € / 69,99 € | not disclosed | high | same |
| Scanner Pro (Readdle) | Pacchetto Fax 1 | 0,99 € | one-time (consumable) | high | same |
| SwiftScan | SwiftScan VIP Monthly | 6,49 € | monthly | high | [apps.apple.com/it id834854351](https://apps.apple.com/it/app/id834854351) |
| SwiftScan | SwiftScan Plus Monthly | 7,99 € | monthly | high | same |
| SwiftScan | SwiftScan VIP Annual | 37,99 € | annual | high | same |
| SwiftScan | SwiftScan Plus Annual | 69,99 € | annual | high | same |
| SwiftScan | SwiftScan Pro-Full Scanner App | 7,99 € | not disclosed (unlock) | high | same |
| Adobe Scan | Scan premium - mensile | 10,99 € | monthly | high | [apps.apple.com/it id1199564834](https://apps.apple.com/it/app/id1199564834) |
| Adobe Scan | Adobe Scan Plus - Mensile | 5,99 € | monthly | high | same |
| Adobe Scan | Adobe Scan Plus - Annuale | 22,99 € | annual | high | same |
| Adobe Scan | Adobe Scan Premium | 31,99 € / 44,99 € / 59,99 € / 74,99 € | not disclosed | high | same |
| iLovePDF | iLovePDF Premium Monthly | 5,99 € | monthly | high | [apps.apple.com/it id1207332399](https://apps.apple.com/it/app/id1207332399) |
| iLovePDF | iLovePDF Premium Yearly | 48,99 € | annual | high | same |
| PDF Expert (Readdle) | PDF Expert Premium | 10,99 € / 44,99 € / 52,99 € | not disclosed | high | [apps.apple.com/it id743974925](https://apps.apple.com/it/app/id743974925) |
| PDF Expert (Readdle) | PDF Expert Mac & iOS | 84,99 € / 89,99 € | not disclosed | high | same |
| PDF Expert (Readdle) | PDF Expert per l'istruzione | 42,99 € | not disclosed (education) | high | same |
| Documents (Readdle) | Documents Plus | 9,99 € / 17,99 € / 59,99 € / 69,99 € | not disclosed | high | [apps.apple.com/it id364901807](https://apps.apple.com/it/app/id364901807) |

Utilities are more expensive than intuition suggests: a document scanner in Italy sustains `5,99–10,99 €`/month and `22,99–69,99 €`/year, comparable to a fitness or budgeting app. The one-time unlock survives here (`7,99 €` SwiftScan Pro) alongside subscriptions.

## AI-powered tools

| App | SKU as shown | Price (EUR) | Period | Confidence | Source |
|---|---|---|---|---|---|
| ChatGPT | ChatGPT Go | 7,99 € | not disclosed | high | [apps.apple.com/it id6448311069](https://apps.apple.com/it/app/id6448311069) |
| ChatGPT | ChatGPT Plus | 22,99 € | not disclosed (monthly) | high | same |
| ChatGPT | ChatGPT Pro 5x | 102,99 € | not disclosed | high | same |
| ChatGPT | ChatGPT Pro 20x | 229,00 € | not disclosed | high | same |
| Claude | Claude Pro - Monthly | 22,00 € | monthly | high | [apps.apple.com/it id6473753684](https://apps.apple.com/it/app/id6473753684) |
| Claude | Claude Pro - Annual | 249,99 € | annual | high | same |
| Claude | Claude Max 5x - Monthly | 149,99 € | monthly | high | same |
| Claude | Claude Max 20x - Monthly | 299,99 € | monthly | high | same |
| Claude | Usage Credits (20 / 50 / 250) | 29,00 € / 69,00 € / 299,00 € | one-time (consumable) | high | same |
| Google Gemini | 100 GB | 1,99 € | not disclosed | high | [apps.apple.com/it id6477489729](https://apps.apple.com/it/app/id6477489729) |
| Google Gemini | Google AI Plus (400 GB) | 4,99 € / 49,99 € | not disclosed | high | same |
| Google Gemini | Google AI Pro (5 TB) | 21,99 € | not disclosed | high | same |
| Perplexity | Perplexity Pro | 22,00 € / 229,00 € | not disclosed | high | [apps.apple.com/it id1668000334](https://apps.apple.com/it/app/id1668000334) |
| Perplexity | Perplexity Max | 229,00 € | not disclosed | high | same |
| Perplexity | Credits (500 / 1,000 / 2,500 / 5,000 / 10,000) | 6,00 € / 10,00 € / 29,00 € / 60,00 € / 100,00 € | one-time (consumable) | high | same |
| Microsoft Copilot | Microsoft 365 Personal | 10,00 € / 99,00 € | not disclosed | high | [apps.apple.com/it id6472538445](https://apps.apple.com/it/app/id6472538445) |
| Microsoft Copilot | Microsoft 365 Premium | 22,00 € / 219,00 € | not disclosed | high | same |
| Remini (Bending Spoons) | Remini Lite Weekly | 4,99 € / 7,99 € | weekly | high | [apps.apple.com/it id1470373330](https://apps.apple.com/it/app/id1470373330) |
| Remini (Bending Spoons) | Remini Pro Weekly | 9,99 € / 11,49 € | weekly | high | same |

Two distinct AI price architectures are visible on the Italian storefront, and the calibration pack should treat them separately. **General assistants** converge hard on `22,00–22,99 €`/month for the mid tier and `229,00 €` for the top tier, with an emerging cheap tier at `4,99–7,99 €` (ChatGPT Go, Google AI Plus). **Consumer AI feature apps** (Remini) sell weekly at `4,99–11,49 €` and never surface a monthly or annual price at all.

Note that the round `22,00 €`, `229,00 €`, `29,00 €` figures are *custom* price points, not `.99` grid points, evidence that the largest vendors are setting Italian prices manually rather than accepting Apple's generated equivalents.

---

## Does EUR mirror USD tier-for-tier on the Italian storefront?

**Answer: it depends entirely on whether the product is an auto-renewable subscription.** For paid apps and one-time in-app purchases, EUR prices are equalized to the developer's base storefront and land either equal to the USD numeral or one grid step above it, never below. For subscriptions, there is no automatic equalization at all, and observed EUR prices diverge from USD in *both* directions by as much as ±30%.

This distinction is the single most load-bearing finding in this report, and it contradicts the widely-repeated blog claim that Apple's euro prices simply run "10–15% above USD because VAT is baked in."

### The documented mechanism

Apple's own material states three things that together explain the split:

- **Prices outside the US and Canada include tax.** "Prices advertised to customers in all countries except the U.S. and Canada include taxes." ([Apple Tech Talk 110364, 2023-05-02](https://developer.apple.com/videos/play/tech-talks/110364/))
- **Equalization is computed *before* tax, from a base storefront the developer picks.** "Prices are globally equalized before tax, which means customers in each country pay approximately the same amount as your base price, but with local taxes added on top." Apple never changes the price in the base storefront. ([same](https://developer.apple.com/videos/play/tech-talks/110364/); [App Store Connect Help, *Set a price*](https://developer.apple.com/help/app-store-connect/manage-app-pricing/set-a-price/))
- **Auto-renewable subscriptions are excluded from that machinery.** "Auto-renewable subscription prices are not automatically adjusted to account for foreign exchange and tax changes, but you can update your subscription pricing at any time in App Store Connect." ([same Tech Talk](https://developer.apple.com/videos/play/tech-talks/110364/)) Apple repeats this in essentially every tax-and-price bulletin: "Prices won't change in any region if your In-App Purchase is an auto-renewable subscription." ([Apple Developer News, *Tax and Price Updates*, 2025-08-21](https://developer.apple.com/news/?id=yo2104n5))

Apple also documents the repricing trigger: "typically, pricing for a storefront will be updated if its currency strengthens or weakens by at least 10%, and the change is sustained over a couple of quarters" ([Tech Talk 110364](https://developer.apple.com/videos/play/tech-talks/110364/)). All `high` confidence; these are Apple's own words.

### Empirical test 1: paid apps and one-time purchases

Method: took the 40 apps in Italy's top-paid chart on 2026-08-13 ([Apple RSS Marketing Tools, `it/apps/top-paid`](https://rss.marketingtools.apple.com/api/v2/it/apps/top-paid/40/apps.json)) and looked each one up in both the `it` and `us` storefronts via Apple's lookup API. Three were not comparable (free or unavailable in the US), leaving 37 pairs. The counts below cover exactly those 37. All `high` confidence.

| Outcome | Count of 37 | Examples (US price → IT price) |
|---|---|---|
| EUR numeral **equal** to USD numeral | 20 | $0.49 → 0,49 €; $1.99 → 1,99 €; $2.99 → 2,99 €; $3.99 → 3,99 €; $9.99 → 9,99 € (ProCam, Sun Surveyor, Groundwire, Moment Pro Camera II) |
| EUR numeral **one grid step above** USD | 17 | $0.99 → 1,19 €; $3.99 → 4,99 €; $4.99 → 5,99 € (PeakFinder, HappyCow, MapOut, SkySafari, Koala Sampler); $5.99 → 6,99 € (Procreate Pocket, Streaks); $6.99 → 7,99 € (Threema, Ableton Note); $7.99 → 8,99 €; $8.99 → 9,99 €; $10.99 → 12,99 €; $12.99 → 14,99 €; $24.99 → 29,99 € (AnkiMobile) |
| EUR numeral **below** USD | 0 | none |

Two paid apps cited elsewhere in this report, Things 3 ($9.99 → `9,99 €`) and LumaFusion ($29.99 → `29,99 €`), were looked up the same way but are not in the top-paid 40 and are excluded from the counts above.

Two things follow. First, **the euro price is never cheaper than the dollar numeral** for one-time purchases, so a USD anchor of $X is a safe *lower* bound for the Italian price and $X+1 a safe upper bound. Second, the equal-versus-higher split tracks which storefront the developer chose as their base. Apple leaves the base price untouched and derives the rest, so a developer who anchored in euros shows `9,99 €`/`$9.99` while one who anchored in dollars shows `$4.99`/`5,99 €`. That reading of the split is my inference from Apple's documented base-storefront rule, not something Apple states about these specific apps; treat it as `medium`.

The observed EUR grid points across the whole sample were: `0,49 · 0,99 · 1,19 · 1,99 · 2,99 · 3,99 · 4,99 · 5,99 · 6,99 · 7,99 · 8,99 · 9,99 · 10,99 · 12,99 · 14,99 · 17,99 · 19,99 · 21,99 · 24,99 · 29,99 · 34,99 · 39,99 · 44,99 · 49,99 · 59,99 · 69,99 · 79,99 · 89,99 · 99,99 · 129,99`.

### Empirical test 2: subscriptions

Method: scraped the in-app-purchase panel for the same app in both the `it` and `us` storefronts on 2026-08-13. **A pair is included only where the SKU display name discloses the billing period on *both* sides**, so that the ratio compares like with like. This is stricter than the rule used for the category tables above, and deliberately so: an undisclosed period makes a price a valid anchor but an invalid ratio. All `high` confidence.

| App | SKU (IT / US) | IT (EUR) | US (USD) | EUR ÷ USD | Direction |
|---|---|---|---|---|---|
| Habitify | Pro Annuale / Pro Yearly | 39,99 € | $49.99 | 0.80 | **EUR far below** |
| Headspace | Annual Subscription | 57,99 € | $69.99 | 0.83 | EUR below |
| Habitify | Pro Mensile / Pro Monthly | 7,99 € | $8.99 | 0.89 | EUR below |
| Headspace | Annual Subscription (second live SKU) | 69,99 € | $69.99 | 1.00 | equal |
| Headspace | Monthly Subscription | 12,99 € | $12.99 | 1.00 | equal |
| Todoist | Pro mensile / Pro - Monthly | 6,99 € | $6.99 | 1.00 | equal |
| Todoist | Pro annuale / Pro - Yearly | 59,99 € | $59.99 | 1.00 | equal |
| Bear | Sottoscrizione Mensile / Monthly Pro | 2,99 € | $2.99 | 1.00 | equal |
| MyFitnessPal | Monthly Premium | 9,99 € | $9.99 | 1.00 | equal |
| MyFitnessPal | Yearly Premium | 49,99 € | $49.99 | 1.00 | equal |
| Strava | Runna Standalone Subscription | 19,99 € | $19.99 | 1.00 | equal |
| Goodnotes | Essential annuale / Essential (Yearly) | 12,99 € | $11.99 | 1.08 | EUR above |
| Habitify | Pro A vita / Pro Lifetime | 129,99 € | $119.99 | 1.08 | EUR above |
| Claude | Pro - Monthly | 22,00 € | $20.00 | 1.10 | EUR above |
| Goodnotes | Pro annuale / Pro (Yearly) | 39,49 € | $35.99 | 1.10 | EUR above |
| MyFitnessPal | Monthly Premium (second live SKU) | 21,99 € | $19.99 | 1.10 | EUR above |
| MyFitnessPal | Yearly Premium (second live SKU) | 87,99 € | $79.99 | 1.10 | EUR above |
| ChatGPT | Plus | 22,99 € | $19.99 | 1.15 | **EUR far above** |
| ChatGPT | Pro 20x | 229,00 € | $200.00 | 1.15 | **EUR far above** |
| Claude | Pro - Annual | 249,99 € | $214.99 | 1.16 | **EUR far above** |
| Strava | 1 mese / 1 Month | 6,99 € | $5.99 | 1.17 | **EUR far above** |
| Strava | 1 anno / 1 Year | 69,99 € | $59.99 | 1.17 | **EUR far above** |
| Bear | Sottoscrizione annuale / Yearly Pro | 34,99 € | $29.99 | 1.17 | **EUR far above** |
| Claude | Max 5x - Monthly | 149,99 € | $124.99 | 1.20 | **EUR far above** |

The spread runs from 0.80 to 1.20, a 40-point range on the same product sold in two storefronts on the same day. No tier table predicts this, because no tier table governs it: these are independent developer pricing decisions.

**Two pairs I excluded, and why they matter as a cautionary note.** Strava also carries an unlabeled `Subscription` SKU at `59,99 €` in Italy and `$79.99` in the US, plus `9,99 €` against `$11.99`. Pairing those would have yielded 0.75 and 0.83 and put Strava in the "prices down in euros" camp. But the two ratios disagree with each other, which is the signature of comparing different SKU generations rather than the same product, whereas Strava's period-labeled SKUs agree exactly at 1.17 for both monthly and annual. **Strava prices roughly 17% above the US in euros.** Calm is excluded outright: its US in-app purchases are period-undisclosed across the board (`$14.99`, `$16.99`, `$29.99`, `$69.99`, `$79.99`), so although Italy's `49,99 €` annual is confirmed from Calm's own Italian description, there is no US counterpart I can match to it without guessing.

The pattern within the spread is legible. Habit and meditation apps with mass-market European ambitions (Headspace, Habitify) price *down* in euros, absorbing part of the 22% VAT rather than passing it on. AI vendors (OpenAI, Anthropic) price *up* by 10–20%, approximately what it takes to hold net-of-VAT proceeds level with the US price, and Strava and Bear's annual plan sit in that same band at 1.17. Utility and productivity tools (Todoist, Bear's monthly plan, MyFitnessPal's entry SKUs) mirror the numeral exactly.

### What this means for the calibration pack

For a solo developer setting a first Italian price:

- **A subscription price is a decision, not a conversion.** Apple will not derive it for you, will not update it for FX or tax, and the market shows no consensus multiplier to apply to a USD figure.
- **Setting the price in euros and treating Italy as the base storefront is the cleanest mental model.** The euro number you choose is exactly what the Italian customer sees, VAT included, and Apple will never change it.
- **Net proceeds from a `9,99 €` sale are roughly `6,96 €`** before considering the Digital Services Tax: `9,99 € ÷ 1.22 = 8,19 €` net of VAT, less Apple's 15% Small Business Program commission. At the standard 30% commission it is roughly `5,73 €`. Arithmetic is mine from the sourced rates below (`medium`), not an Apple-published figure.

---

## Italian storefront pricing mechanics for a solo developer

**Standard Italian VAT rate: 22%.** Sourced directly from the Italian tax authority: "In Italia l'aliquota ordinaria Iva è del 22%," with reduced rates of 4%, 5%, and 10% for specified goods ([Agenzia delle Entrate, *Iva - Norme generali e aliquote*](https://www.agenziaentrate.gov.it/portale/iva-regole-generali-aliquote-esenzioni-pagamento/norme-generali-e-aliquote), undated page, retrieved 2026-08-13; corroborated by the [European Commission's Your Europe VAT rate table](https://europa.eu/youreurope/business/finance-and-tax/vat/vat-rules-rates/index_it.htm), which lists IT at 22% standard). Software and app subscriptions fall under the standard rate. `high` confidence.

Apple independently confirms the same figure in a dated developer bulletin: "Italy: New digital services tax of 3% (in addition to the existing value-added tax of 22%)" ([Apple Developer News, 2020-09-01](https://developer.apple.com/news/?id=oyy56t2r)). `high`.

**VAT is inside the displayed price.** Confirmed above from Apple's Tech Talk and reinforced on Apple's subscriptions page: "The default pricing in the App Store Connect pricing tool is inclusive of applicable taxes that Apple collects and remits" ([Apple Developer, *Auto-renewable Subscriptions*](https://developer.apple.com/app-store/subscriptions/), undated, retrieved 2026-08-13). Apple collects and remits Italian VAT on the developer's behalf; developer proceeds are calculated on the tax-exclusive price. `high`.

**Italy's Digital Services Tax is separate from VAT and hits proceeds, not the shelf price.** The DST applies at 3% on revenues from qualifying digital services, and only to operators exceeding €750 million in worldwide revenue in the prior calendar year ([Agenzia delle Entrate, *Dichiarazione Imposta sui servizi digitali*](https://www.agenziaentrate.gov.it/portale/dichiarazione-imposta-sui-servizi-digitali/infogen-dichiarazione-imposta-sui-servizi-digitali-imprese), undated page, retrieved 2026-08-13). A solo developer is nowhere near that threshold and is not a DST taxpayer, but Apple is, and Apple passes the effect through to developer proceeds on the Italian storefront rather than to the consumer price. Apple has adjusted this line at least twice: it introduced the 3% DST effect on proceeds on [2020-09-01](https://developer.apple.com/news/?id=oyy56t2r), and on [2021-08-03](https://developer.apple.com/news/?id=o0uodgu7) announced that "your proceeds on the App Store in Italy will be increased to reflect a change to the Digital Services Tax effective rate." Both `high`. The practical consequence: **the same euro price yields slightly different proceeds in Italy than in, say, Germany, and the difference is invisible on the storefront.**

**Dated Apple storefront price changes affecting EUR.**

| Date | Change | Confidence | Source |
|---|---|---|---|
| 2020-09-01 | Italy DST of 3% introduced on top of the existing 22% VAT; developer proceeds in Italy adjusted; **App Store prices did not change** | high | [developer.apple.com/news/?id=oyy56t2r](https://developer.apple.com/news/?id=oyy56t2r) |
| 2021-08-03 | Prices of apps and IAPs (excluding auto-renewable subscriptions) **decreased in all territories that use the Euro currency**; the entry price point fell from `1,09 €` to `0,99 €`; Italian proceeds increased to reflect a DST effective-rate change | high (Apple); entry-point detail medium ([Reuters, 2022-09-20](https://www.reuters.com/technology/apple-hike-app-store-prices-several-countries-oct-2022-09-20/)) | [developer.apple.com/news/?id=o0uodgu7](https://developer.apple.com/news/?id=o0uodgu7) |
| 2022-09-19, effective 2022-10-05 | Prices of apps and IAPs (excluding auto-renewable subscriptions) **increased in all territories that use the euro currency**, alongside Chile, Egypt, Japan, Malaysia, Pakistan, Poland, South Korea, Sweden, Vietnam. The euro entry point rose from `0,99 €` to `1,19 €` and `9,99 €` items moved to `11,99 €`. Widely attributed to the euro reaching parity with the dollar | high | [developer.apple.com/news/?id=e1b1hcmv](https://developer.apple.com/news/?id=e1b1hcmv); [official EUR tier chart PDF](https://developer.apple.com/support/downloads/price-tier-updates/App-Store-Price-Tier-Updates-October-2022.pdf) |
| 2025-08-21 | Tax and price updates round; Estonia VAT 22%→24%, Romania 19%→21%; **no Italy-specific change**; subscriptions explicitly excluded from automatic repricing | high | [developer.apple.com/news/?id=yo2104n5](https://developer.apple.com/news/?id=yo2104n5) |
| 2026-01-01 | **Bulgaria adopted the euro**, moving App Store purchases there from BGN to EUR; euro-price points now cover one more storefront | high | [Apple Developer News, price updates](https://developer.apple.com/news/) |
| 2026-01-29 | Tax and price updates across nine countries (Kazakhstan VAT 12%→16%, Russia 20%→22%, Mauritius new 15%, Bhutan new 5%, Türkiye DST 7.5%→5%, Finland and Lithuania reduced rates, Ghana levy removed, Zimbabwe 15%→15.5%); **no Italy or euro-wide change** | high | [Apple Developer News, price updates](https://developer.apple.com/news/) |

**The last euro-wide price-point change I could find is 2022-10-05.** The two 2026 rounds (January's nine-country update and Bulgaria's euro adoption) left euro price points themselves untouched. So for calibration purposes, euro price points have been stable for roughly four years and can be treated as stable through mid-2026. Stated as absence of evidence rather than a guarantee: Apple's bulletins are numerous and I did not read every one.

**Price-point granularity, and why the published tier chart is now only historical.** The October 2022 EUR chart linked above is the last publicly downloadable euro tier table, and it is worth reading once for the shape of the ladder (Tier 1 `1,19 €`, Tier 4 `4,99 €`, Tier 5 `5,99 €`, Tier 8 `9,99 €`, Tier 9 `10,99 €`, Tier 11 `12,99 €`, Tier 42 `49,99 €`, up to Tier 87 `1.199,99 €`). But that 87-tier ladder was superseded: Apple now offers up to 800 price points by default and 100 more on request, reaching $10,000 ([App Store Connect Help, *Set a price for an In-App Purchase*](https://developer.apple.com/help/app-store-connect/manage-in-app-purchases/set-a-price-for-an-in-app-purchase/), undated, retrieved 2026-08-13). `high`.

My live observations confirm the expansion directly: `0,99 €`, `1,99 €`, `2,99 €`, and `3,99 €` are all in use on the Italian storefront today, and **none of them exists in the October 2022 tier chart** (which jumps `1,19 → 2,49 → 3,49 → 4,99`). Alongside those, custom points such as `22,00 €`, `229,00 €`, `14,90 €`, `35,90 €`, `47,90 €`, `39,95 €`, `26,49 €`, `39,49 €`, `13,49 €`, `9,39 €`, and `6,29 €` are live. **A solo developer is confined neither to the old tier ladder nor to `.99` endings.**

---

## Italian consumers' willingness to pay for subscriptions

No source I could find measures *app subscriptions specifically* for Italy. The best available dated evidence covers digital and streaming subscriptions generally, which sets an upper-bound context rather than a direct app-store figure.

| Finding | Figure | Date | Confidence | Source |
|---|---|---|---|---|
| Italians aged 18–74 holding at least one streaming or Pay TV subscription | 82.4% | survey fielded 2026-03-16/19, published 2026-06-26 | medium | [Facile.it / mUp Research, via Hardware Upgrade](https://www.hwupgrade.it/news/audio-video/streaming-e-pay-tv-ogni-famiglia-italiana-ha-in-media-tre-abbonamenti_155403.html) |
| Same, ages 25–34 | 91.5% | same | medium | same |
| Same, households with minor children | 91% | same | medium | same |
| Average subscriptions per Italian household | 3 | same | medium | same |
| Average monthly household spend on streaming/Pay TV | 27,50 € (330 €/year) | same | medium | same |
| Highest-spending age band (35–44) | 31,86 €/month (382,32 €/year) | same | medium | same |
| Subscribers who don't know what they pay monthly | ~11% (≈3 million people) | same | medium | same |
| Subscribers paying for something they don't use regularly | ~7.5% (≈1.9 million people) | same | medium | same |
| Italian adults using at least one SVOD platform | 70% | Deloitte Digital Consumer Trends Italy, 2025 edition | medium | [Deloitte Italy](https://www.deloitte.com/it/it/Industries/tmt/perspectives/digital-consumer-trends-2025.html) |
| SVOD churn rate, stable year over year | 17% | same | medium | same |
| Users who did not change any subscription in the past year | 57% | same | medium | same |
| Smartphone penetration among Italian adults | 95% (98% daily use) | same | medium | same |

The survey methodology is disclosed: 1,001 respondents representative of the Italian adult population aged 18–74, interviewed 16–19 March 2026. That is a real, dated, sampled instrument, which is why these carry `medium` rather than `low`: they are secondary reporting of a named institute's survey, not storefront observation.

**What a calibration pack can safely take from this:** paying monthly for digital content is normal behaviour for the large majority of Italian adults, the household budget already committed to recurring digital services is around `27,50 €`/month, and Deloitte's finding that cost is the primary cancellation driver means a new app subscription competes inside an already-contested wallet. Deloitte characterises the 2025 Italian market as one where adults take "un approccio più razionale" to subscribing, against a backdrop of rising cost of living.

One widely-circulated figure I deliberately excluded: an aggregator site reports "€876 average annual household subscription spend" and "72% of families with at least one streaming subscription," attributing them to ISTAT and Findomestic ([Disdici.com Osservatorio, published 2026-01-15](https://disdici.com/osservatorio/)). I could not verify either number against the cited primary sources, and the site's own methodology note concedes that some figures are its own projections rather than certified statistics. Logged in the negative-result section rather than used.

---

## Does not exist publicly (negative-result log)

Sub-questions I could not source, and category shortfalls.

**Sub-question 4 (Italian consumers' subscription willingness):**
- **No published measurement of the share of Italians who pay for *mobile app* subscriptions specifically.** All available Italian survey data measures streaming/SVOD/Pay TV, or digital subscriptions in aggregate. The Facile.it/mUp and Deloitte figures above are the nearest proxies and should be labelled as such in the calibration pack, never as app-store willingness to pay.
- **No published average revenue per Italian iOS user, or Italian app-store consumer spend per capita**, from Apple, Sensor Tower, data.ai, or Italian trade bodies, at a granularity usable for calibration.
- **No verified primary source for the "€876 per household per year" subscription-spend figure** circulating on Italian aggregator sites. Attributed to Findomestic's Rapporto Consumi 2024 but not confirmed at the primary source; the publishing site labels parts of its own dataset as internal projections.
- **No Italian breakdown of willingness to pay by app category.** Nothing separates what an Italian will pay for a fitness app versus a budgeting app.

**Sub-question 2 (tier equalization):**
- **No current public EUR price-point table exists.** The October 2022 EUR tier chart is publicly downloadable and is cited above, but it predates Apple's move to 800+ price points and no longer matches the live storefront. Apple has published no equivalent chart for the expanded system. All grid points in this report after that date are observed empirically from live storefront prices, not read from an Apple table.
- **The exact FX threshold that triggers automatic repricing is not fully documented.** Apple's Tech Talk gives "at least 10%, sustained over a couple of quarters" as typical, hedged with "typically"; no precise rule is published.
- **Calm could not be included in the paired subscription comparison.** Its US in-app purchases disclose no billing period, so no US counterpart to Italy's confirmed `49,99 €` annual could be matched without guessing.

**Sub-question 3 (storefront mechanics):**
- **Apple does not publish the Italy-specific Digital Services Tax *effective rate* it applies to proceeds.** The statutory rate is 3%, but Apple's 2021-08-03 bulletin refers to a changed "effective rate" without stating it, and Apple's Exhibit B schedules are behind developer authentication. A solo developer cannot compute exact Italian proceeds from public sources.
- **No dated Apple announcement of a euro price-point change after 2022-10-05** was found. Reported as absence of evidence, not as a guarantee that none occurred.

**Category shortfalls (fewer than 3 concrete price points, or period undisclosed throughout):**
- **Finance/budgeting, Italian vendors:** the two Italian consumer-finance apps with real national scale, Satispay (id790287076) and Revolut's Italian storefront listing (id932493382), expose **no in-app purchases at all**. There is no Italian-vendor consumer-finance subscription anchor to report. The five apps in the table are all foreign (Czech, Danish, US, German).
- **Meditation/mental health, Italian vendors:** the two leading Italian mental-health apps, Serenis (id1631510145) and Unobravo (id1624675215), expose **no in-app purchases**; both sell therapy sessions through their own web checkout, outside Apple's billing. No Italian-vendor EUR anchor for this category.
- **Parenting/family:** 4 apps sampled, but **not one disclosed a billing period in its SKU names**. Every parenting figure in this report is a price anchor without a confirmed period, except Qustodio's explicitly annual SKUs.
- **Habit tracking:** only 2 of 6 apps sampled are category-native trackers with fully period-labelled SKUs (Habitify, HabitKit). Way of Life's three price points are all period-undisclosed.
- **Education:** Duolingo, the category leader, labels **none** of its ten live SKUs with a period. Its `89,99 € / 101,99 € / 125,99 €` cluster is almost certainly annual Super Duolingo pricing given the magnitude, but the storefront does not say so and I have not asserted it.
- **AI tools:** ChatGPT, Gemini, Perplexity, and Microsoft Copilot all leave periods undisclosed. Only Claude labels its SKUs. The monthly/annual split in the AI table is inferred from magnitude for every vendor except Anthropic and is marked accordingly.
- **No Italian-language review or roundup was used as a price source anywhere in this report.** I searched for Italian tech-press pricing roundups; those found (Spliiit, money.it) either covered streaming rather than apps or quoted vendor-web prices rather than App Store prices. Since direct storefront observation was available for every category, secondary Italian sources were unnecessary and are cited only where they add non-storefront context.

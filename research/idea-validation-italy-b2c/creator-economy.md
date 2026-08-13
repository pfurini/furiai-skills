# The Italian creator economy as an app-distribution channel (DA4)

Research date: 2026-08-13. All figures carry source, URL, publication date and a confidence tag.

**Confidence tags.** `high` = published by the platform itself, by a regulator, or by a large-sample dated study. `medium` = reputable agency or trade-press report with stated methodology. `low` = single agency rate card, small sample, undated page, or a secondary aggregator restating someone else's numbers.

**Age flag.** Anything published before 2025-08-13 is marked ⚠️ *older than 12 months*. Legal instruments are an exception: for those the report states currency and amendment status instead, because a 2024 delibera that is still in force is not "stale" in the way a 2024 price is.

## Headline for the reader in a hurry

The Italian creator market is real, dated and well measured (€425M in 2026, ~40,000 professional creators, published per-tier rate movements), but it is measured *for consumer-goods brands*. Fashion & Beauty and Food & Beverage take 45% of spend; Business & Finance takes 3%. **There is no published Italian data on app-install creator campaigns at all** — no CPI norms, no app-vertical rate card, no conversion benchmarks. A solo dev entering this channel is pricing against fashion-brand comparables, and should expect to negotiate from the nano/micro tier where the published Italian floor is €100–300 per Instagram post.

Two constraints matter more than the rates. First, **Amazon Associates Italy offers no route to monetise app installs at all**: the Amazon.it storefront does not carry Play Store or App Store installs, so they fall outside the programme entirely, and the one app category Amazon does carry — Android apps in its own Appstore — pays **0%**. The default Italian affiliate reflex simply does not apply to apps. Second, the disclosure obligation that binds a solo dev is *not* the AGCOM influencer register (that threshold is 500,000 followers and falls on the creator); it is the Codice del Consumo unfair-practices regime enforced by AGCM, which reaches the advertiser who commissioned the content. AGCM fined creators €65,000 in a single June 2025 action for exactly this.

---

## 1. Platform landscape in Italy

### 1.1 Reported advertising reach by platform

These are **potential advertising reach figures published by the platforms' own ad-planning tools**, not monthly active users. DataReportal states this caveat explicitly, and Meta states in its own tools that "estimated audience size is not a proxy for monthly or daily active users, or for engagement." Treat the column as *addressable ad audience*, and do not add platforms together.

Source for the whole table: DataReportal, *Digital 2026: Italy*, https://datareportal.com/reports/digital-2026-italy, published 2025-11-05, data as of October / late 2025. Confidence: **high** (platform-published source data, dated, with methodology and caveats stated).

| Platform | Reported ad reach, Italy, late 2025 | As % of population (59.1M) | YoY change |
|---|---|---|---|
| YouTube | 41.2M | 69.7% | −1.00M (−2.4%) |
| Instagram | 29.9M | 50.5% (58.8% of adults 18+) | +1.20M (+4.2%) |
| Facebook | 28.5M | 48.1% (56.5% of adults 18+) | −750K (−2.6%) |
| LinkedIn | 25.0M *registered members, not MAU* | 42.3% | +3.00M (+13.6%) |
| TikTok | 22.0M *adults 18+ only* | 43.5% of adults 18+ | +1.41M (+6.9%) |
| Messenger | 14.8M | 25.0% | −1.10M (−6.9%) |
| Reddit | 14.8M | 25.0% | +11.8M (+400%) ⚠️ see note |
| Pinterest | 10.9M | 18.4% | +50K (+0.5%) |
| Snapchat | 5.11M | 8.6% | +490K (+10.6%) |
| X | 5.04M | 8.5% | −2.15M (−29.9%) |

Notes that change how you read this table:

- **TikTok's figure is adults only.** TikTok's ad tools publish no data for ages 13–17 in Italy, so 22.0M understates total Italian usage by an unpublished amount. Do not compare it like-for-like against YouTube's all-ages 41.2M.
- **LinkedIn counts registered members**, not monthly actives, so its 25.0M is not comparable with the rest of the column.
- **Reddit's +400%** is flagged by DataReportal itself as an unusual change in reported ad reach that it has republished "as is". Do not treat it as 400% real growth.
- **Gender skews are large and actionable.** TikTok Italy's adult ad audience is 59.7% female; Pinterest is 70.3% female; X is 70.1% male (inferred, and DataReportal warns the inference is less reliable in non-English-language countries).
- Aggregate social media user identities: **41.2M (69.7% of population), down 1.0M (−2.4%) YoY**. DataReportal warns this de-duplicated figure often collapses onto the largest single platform — which is why it equals YouTube's number exactly.

### 1.2 Genuine deduplicated Italian audience (Audicom, the national JIC)

Audicom is the Italian joint industry committee formed by the merger of Audiweb and Audipress. It publishes a real deduplicated unique-user currency — but for *editorial and publisher* audiences, not for social platforms. It does **not** publish per-platform social MAU, so it cannot substitute for the table above.

| Metric | Value | Period | Source | Confidence |
|---|---|---|---|---|
| Monthly online individuals (2+) | 43.97M (75.4% of pop.) | Dec 2025 | Audicom / Audiweb press release, 19 Feb 2026, http://www.mediaclic.it/docbox/Audiweb/2025/comunicato-audicom_dati-audience-online-sistemaaudiweb_dicembre2025.pdf | high |
| Monthly online, 2025 average | 44.1M (75.5%) | 2025 avg | same as above | high |
| Mobile online, 2025 average | 40.5M = 95% of population 18–74 (+0.7% vs 2024) | 2025 avg | same as above | high |
| Daily online individuals | 37.6M, 2h37m per person | Dec 2025 | same as above | high |
| Monthly online individuals | 43.8M (75.0%); mobile 40.7M (95.6% of 18–74) | Apr 2026 | Engage, https://www.engage.it/dati-e-ricerche/audicom-ad-aprile-2026-438-milioni-di-utenti-online-il-mobile-vale-l-88-del-tempo-di-navigazione.aspx, 2026-08-03 | high |
| Mobile share of total online time | 88% | Apr 2026 | same as above | high |

The stable picture: **~44M Italians online monthly, ~37–38M daily, and mobile is 88% of time spent.** That is the addressable ceiling for a consumer mobile app, and it has been flat for two years.

### 1.3 Time spent per platform

| Platform | Daily time per active user | Source | Confidence |
|---|---|---|---|
| TikTok | 1h30m | We Are Social / Meltwater *Digital 2026*, reported by Engage, https://www.engage.it/dati-e-ricerche/digital-2026-social-media-e-ai-ridisegnano-la-discovery-degli-italiani.aspx | medium ⚠️ *page carries no publication date; the underlying Digital 2026 report is dated late 2025* |
| YouTube | 1h10m | same | medium |
| Instagram | 1h07m | same | medium |
| WhatsApp | 52m | same | medium |

Same source, same caveat: social media is the most-used weekly medium among Italian internet users 16+ at **89.3%**, ahead of TV, streaming music, gaming, news, podcasts and radio; **52.7%** of the sample use social channels to research brands and products.

### 1.4 Which content categories are strongest in Italian

Three different things get called "strongest", and conflating them produces wrong conclusions. They are separated below.

**(a) Where Italian creators actually are** — share of professional Italian influencers by niche. Sample: 5,377 Italian influencers sponsored at least 12 times in the year, 6,689,721 pieces of content analysed.

| Niche | Share of Italian professional influencers |
|---|---|
| Personal relationships | 25.8% |
| Fashion & accessories | 22.8% |
| Sport & fitness | 21.1% |
| Food & restaurants | 12.9% |

Source: Fiscozen + Kolsquare joint study, reported by Repubblica/Teleborsa, https://finanza.repubblica.it/News/2026/04/21/influencer_in_italia_pochi_adottano_il_nuovo_ateco_mercato_ancora_ibrido-59/ and Corriere della Sera, https://www.corriere.it/economia/aziende/26_aprile_25/influencer-in-italia-40-mila-professionisti-quasi-tutti-non-vip-fatturano-in-media-2-mila-euro-al-mese-solo-il-2-5-con-nuovo-29341508-8d54-46ce-845e-27a60de97xlk.shtml, both 2026-04-21/25. Confidence: **high** (large stated sample, dated, two independent tier-1 outlets).

**(b) Where brand money goes** — share of Italian influencer-marketing *spend* by sector. This is a spend signal, not an audience-size signal.

| Sector | Share of IM investment 2026 | vs 2025 |
|---|---|---|
| Fashion & Beauty | 27% | +1pt |
| Food & Beverage | 18% | flat |
| Gaming & Tech | 13.5% | — |
| Travel & Lifestyle | 13.5% | — |
| Sport & leisure | 9% | up from 8% |
| Business & Finance | 3% | up from 2.5% |

Source: DeRev, *Listino dei compensi degli influencer in Italia*, 6th edition, https://derev.com/2026/07/influencer-marketing-in-italia-compensi-degli-influencer-2026/, 2026-07-02; corroborated by Il Sole 24 Ore, https://en.ilsole24ore.com/art/influencer-marketing-in-italia-market-worth-425-million-fees-down-celebrities-AI0kWmyD, 2026-07-02. Confidence: **medium** (agency study, ~5,000 profiles and 865,000 posts, stated methodology and observation window 15 Jun 2025 – 15 Jun 2026, reported by tier-1 financial press).

DeRev's own note on Business & Finance is worth quoting for a solo dev in that space: qualified creators are few, reputational risk weighs more than in other sectors, and collaborations demand editorial authority and consistency. Small share, high barrier, low competition.

**(c) Which sectors get engagement** — travel and tourism produce the highest engagement on sponsored content, **up to 19.2% per sponsored piece against a 3.9% average** (Fiscozen/Kolsquare, 2026-04-21, high). Beauty/Fashion dominate *volume* but not engagement.

**(d) Platform-specific activation mix.** On TikTok in January 2026, Beauty took 41.32% of brand-creator activations, Fashion 18.47%, Tech & Electronics 14.08%, Entertainment & Media 9.92% (ONIM/Tactik, https://www.onim.it/wp-content/uploads/2026/03/ONIM_Report-Sponsored-Gennaio-2026_TikTok.pdf, data Jan 2026, published Mar 2026, confidence **medium**). IAB Italia's bimonthly AdReport for March–April 2026 reaches the same conclusion: Beauty, Fashion and Luxury dominate both platforms, with video the prevailing format (https://iab.it/adreport-scenario-influencer-instagram-e-tiktok-marzo-aprile-2026/, 2026-05-27, confidence **medium**).

**(e) Audience-side category reach**, from Audicom's deduplicated panel, December 2025 (confidence **high**, same Audicom source as §1.2): General Interest Portals & Communities 38.1M, Software Information / Developers 33.99M, Cooking Food & Beverages 31.8M, Health Fitness & Nutrition 30.0M, Research Tools ~29M. Note the size of the *Software Information / Developers* audience — 34M Italians — which is the audience-side counterpart to the tiny 3% Business & Finance spend share.

**(f) Personal finance ("fininfluencer")** is a small, identifiable and now-regulated niche: the Politecnico di Milano's Osservatorio Fintech & Insurtech identified **48 Italian fininfluencer profiles**; their topics are investments (66%), trading (34%), personal finance (26%) and financial education (24%); the 15 largest YouTube profiles produced ~34,000 videos for 2.2bn views (MilanoFinanza, https://www.milanofinanza.it/news/il-faro-della-consob-sui-guru-della-finanza-online-chi-sono-i-fininfluencer-italiani-202601231844247449, 2026-01-23, confidence **medium**). See §4.5 — this niche carries Consob/ESMA exposure on top of the general rules.

**Calcio/sport and genitorialità:** sport & fitness is 21.1% of creators (see (a)) and sport/leisure is 9% of spend (see (b)), but no dated Italian source found in this pass breaks out *calcio* specifically, and none breaks out *genitorialità* (parenting) as a measured category at all. Both are in the negative-result log.

---

## 2. Sponsorship cost norms for Italian creators

### 2.1 Read this before the numbers: the tier bands do not line up

The tier bands requested in this brief (nano <10K, micro 10–100K, mid 100–500K, macro >500K) **do not match the bands used by the only substantial Italian dataset**, DeRev's. DeRev's bands also differ *between platforms*. The consequences:

- "Micro 10–100K" straddles DeRev's **micro (10–50K)** and **mid-tier (50–300K)** on Instagram, TikTok and YouTube.
- "Mid 100–500K" straddles DeRev's mid-tier and macro on Instagram/TikTok, and is exactly DeRev's **macro** on YouTube.
- "Macro >500K" has **no single published Italian figure**. On Instagram/TikTok it splits DeRev's macro (300K–1M) and mega (1M–3M); on YouTube it is DeRev's mega (500K–1M) plus celebrity (>1M).

Everything below is therefore presented on **DeRev's own bands**, labelled per platform. No interpolation or averaging across DeRev bands has been performed, because doing so would manufacture numbers that no source published.

DeRev's bands, 2026 edition:

| Tier | Facebook | Instagram | TikTok | YouTube |
|---|---|---|---|---|
| Nano | not published | 5–10K | 5–10K | 5–10K |
| Micro | 50–100K | 10–50K | 10–50K | 10–50K |
| Mid-tier | 100–300K | 50–300K | 50–300K | 50–100K |
| Macro | not published | 300K–1M | 300K–1M | 100–500K |
| Mega | not published | 1M–3M | 1M–3M | 500K–1M |
| Celebrity | >3M | >3M | >3M | >1M |

"Not published" means the tier exists but DeRev's follower band for it was not stated in any retrieved source — it does not mean the tier is absent. DeRev publishes 2026 rate movements for Facebook Macro (−13.6%) and Mega (−15.6%), so those tiers demonstrably exist on that platform.

Sources: Il Sole 24 Ore 2026-07-02 (band definitions for celebrity, mid-tier, micro and macro); DeRev *Listino 2025* PDF methodology note, https://www.foodaffairs.it/wp-content/uploads/2025/07/Report-Listino-Influencer-2025_compressed.pdf (YouTube nano band changed from 3–10K to 5–10K for cross-platform comparability); ItaliaOggi 2025-07-10, https://www.italiaoggi.it/marketing-e-media/marketing/influencer-ecco-quanto-guadagnano-nel-2025-calano-i-compensi-ma-il-mercato-cresce-hjximndn (YouTube macro 100–500K, mega 500K–1M). Confidence: **medium**.

### 2.2 Published euro figures, 2026 edition

DeRev publishes its full grid only behind a lead-capture form. The figures below are the individual points that appear in the public reporting. **DeRev states explicitly that these exclude VAT, withholding, agency fees, production costs, usage rights and exclusivity** — so a quoted rate is a floor, not a landed cost.

| Platform | Tier (DeRev band) | Published 2026 rate | Source | Confidence |
|---|---|---|---|---|
| Instagram | Nano (5–10K) | **€100–300 per post** (stable YoY) | DeRev 2026-07-02; Il Sole 24 Ore 2026-07-02 | medium |
| Instagram | Celebrity (>3M) | up to €35,000 per post | RassegnaNotizie, https://www.rassegnanotizie.it/compensi-influencer-in-calo-nuovi-trend-nel-marketing-digitale/, 2026-07-03 | low (secondary aggregator) |
| TikTok | Nano (5–10K) | €50–175 per post | same as above | low |
| TikTok | Macro (300K–1M) | **up to €5,400 per post** | Il Sole 24 Ore 2026-07-02 | medium |
| TikTok | Celebrity (>3M) | up to €18,000 per post | RassegnaNotizie 2026-07-03 | low |
| YouTube | Celebrity (>1M) | **€58,000 per long-form video** | Il Sole 24 Ore 2026-07-02; DeRev 2026-07-02 | medium |
| YouTube | Shorts, all tiers | ≈ **one third** of the equivalent long-form video | DeRev 2026-07-02 | medium |

**Tiers with no published 2026 euro figure at all:** Instagram micro, mid-tier, macro and mega; TikTok micro, mid-tier and mega; YouTube nano, micro, mid-tier, macro and mega; all Facebook tiers. For these, only the *percentage movement* is public (§2.3).

### 2.3 Published 2026 rate movements (all tiers, all platforms)

Platform averages: Instagram **+2.45%** on posts and **+3.8%** on story sets; YouTube **+1.23%**; TikTok **−0.33%**; Facebook **−12.23%**.

| Tier | Instagram | TikTok | YouTube (long-form) | Facebook |
|---|---|---|---|---|
| Nano | stable (€100–300) | −10% | stable | — |
| Micro | +5.6% | +2.6% | stable | −11.1% |
| Mid-tier | +9.2% | +7.1% | +2.9% | −14.3% |
| Macro | +7.1% | +7.6% | +5.0% | −13.6% |
| Mega | +2.3% | −0.7% | +1.9% | −15.6% |
| Celebrity | −9.5% | −8.6% | −2.4% | −18.8% |

Source: DeRev 2026-07-02 (primary), corroborated independently by Il Sole 24 Ore 2026-07-02, ItaliaOggi 2026-07-02, Engage, Brand News and The Signal Media, all 2026-07-02. Confidence: **medium**.

The shape is consistent and worth acting on: **mid-tier and macro are the only two tiers rising on all three major platforms**, celebrity has fallen for three consecutive years on all four, and Facebook is in structural decline as a native campaign channel.

Market size for context: **€425M in 2026, +10.4% over €385M in 2025**; the growth comes from more campaigns, more creators involved and more continuous (rather than one-shot) collaborations, not from higher per-content rates (DeRev 2026-07-02, medium).

### 2.4 Published euro figures from the 2025 edition ⚠️ *older than 12 months*

Retained because several tiers have no 2026 euro figure, and these are the most recent published absolute numbers for them. Apply the 2026 movements from §2.3 on top.

| Platform | Tier | 2025 figure | Source | Confidence |
|---|---|---|---|---|
| Instagram | Micro (10–50K) | maximum rose to €1,000 per content (+33%) | ItaliaOggi, 2025-07-10 ⚠️ | medium |
| Instagram | Mid-tier (50–300K) | minimum rose to €1,500 per content (+8.3%) | same ⚠️ | medium |
| TikTok | Mid-tier (50–300K) | maximum €3,000 → €3,500 (+13.3%) | same ⚠️ | medium |
| TikTok | Macro (300K–1M) | minimum €3,000 → €3,500 (+6.2%), maximum unchanged | same ⚠️ | medium |
| YouTube | Macro (100–500K) | €7,500–12,500 → **€7,500–13,500** per video (+5%) | same ⚠️ | medium |
| YouTube | Mega (500K–1M) | minimum €12,500 → €13,500, maximum €25,000 (+2.7%) | same ⚠️ | medium |

A cross-platform envelope from the same 2025 edition, quoted via We-Wealth — these are **min-to-max ranges spanning all four platforms** (Facebook lowest, YouTube highest), not per-platform rates, and should not be read as a single-platform quote: nano (to 10K) €50–1,250; micro (10–50K) €50–3,000; mid (100–300K) €175–7,500; macro (300K–1M) €350–13,500; mega (1M–3M) €750–25,000; digital celebrities can exceed €60,000 per sponsored content. Source: Museo del Risparmio, https://www.museodelrisparmio.it/blog/numeri-e-influencer-quanto-vale-veramente-un-post-virale/, 2025-11-19, citing DeRev via We-Wealth. Confidence: **low** (third-hand restatement).

### 2.5 Agency rate cards — use as a sanity check only

These are single-agency price lists, not surveys. They are included because they are the only sources that quote the brief's requested tier bands directly, and because a solo dev will encounter these numbers when searching. **They contradict each other and contradict DeRev.**

| Source | Date | Confidence | Instagram post ranges quoted |
|---|---|---|---|
| Migliore Agenzia, https://www.migliore-agenzia.com/en/blog/influencer-marketing-sme-costs-agency-guide-2026 | 2026-04-16 | low | Nano <10K €50–200; Micro 10–100K €200–1,000; Macro 100K–1M €1,000–5,000; Celebrity >1M €5,000–50,000+. Reels/TikTok: €100–300 / €300–1,500 / €1,500–8,000 / €8,000–50,000+. YouTube video: €200–500 / €500–2,500 / €2,500–15,000 / €15,000–100,000+ |
| Pota Studio, https://www.potastudio.com/blog/influencer-marketing-micro-vs-macro-2026 | 2026-07-12 | low | Reels: nano €50–300; micro €300–2,000; mid-tier €2,000–8,000; macro €8,000–25,000; mega €25,000+ |
| StarNgage, https://starngage.com/plus/en-us/blog/italy-influencer-pricing-by-vertical-beauty-fitness-tech-more | undated | low | Nano 1–10K €50–300; micro 10–100K €200–1,500; mid 100–500K €1,500–5,000; macro 500K–1M €5,000–15,000; mega 1M+ €20,000–50,000+ |

**The discriminator that tells you how much to trust this tier:** Pota Studio states the Italian market was worth €450M in 2025, while DeRev — the source everyone else cites — measured €385M for the same year. A 17% discrepancy on the single most-quoted headline number in the sector is a reliability signal for the whole agency-blog tier. Where these cards conflict with DeRev, prefer DeRev.

Two cross-platform rules of thumb appear consistently in this tier and are directionally plausible but **not independently verified**: TikTok fees run roughly 20–30% below equivalent Instagram fees (Pota Studio, low; StarNgage, low), and YouTube integrations command 2–3× the Instagram equivalent (Pota Studio, low). DeRev's data supports the *direction* of both but publishes no such ratio.

### 2.6 Which tiers actually have Italian data — summary

| Requested band | Direct published Italian euro figure? |
|---|---|
| Nano <10K | **Partly.** Instagram €100–300 (DeRev 2026, medium); TikTok €50–175 (low). Best-evidenced tier — but note DeRev's nano band *starts at 5K*, so creators below 5,000 followers have no published Italian rate at all. |
| Micro 10–100K | **No — straddles two DeRev bands.** Partial: IG micro max €1,000 (2025 ⚠️), IG mid-tier min €1,500 (2025 ⚠️). |
| Mid 100–500K | **Platform-dependent.** YouTube only, where it maps exactly to DeRev macro: €7,500–13,500 per video (2025 ⚠️, +5% for 2026). IG/TikTok: straddle, no direct figure. |
| Macro >500K | **No published Italian figure for this band as a single unit.** Nearest: TikTok macro (300K–1M) up to €5,400 (2026, medium); YouTube celebrity (>1M) €58,000 (2026, medium). |

---

## 3. Affiliate and performance practices among Italian creators

### 3.1 Amazon Associates Italy — the official schedule

Retrieved directly from Amazon's Italian Associates Central help pages on 2026-08-13: https://programma-affiliazione.amazon.it/help/node/topic/GRXPHT8U84RAYDXZ. Confidence: **high** (the operator's own current published rate card). Caveat: the page carries no publication date, only a "© 1996-2025" footer, so it is *current as retrieved* rather than *dated*.

| Category (Amazon.it) | Standard commission |
|---|---|
| Amazon Fashion private labels, apparel & accessories, luxury, luxury-store beauty & fashion, shoes/bags/wallets, watches | 6.0% |
| Amazon Instant Video, Audible, auto & moto, books, digital music, furniture, Handmade, home, DIY, jewellery, Kindle books, kitchen & dining, music, power & hand tools | 5.0% |
| Beauty, luggage, personal-care devices, sport & fitness | 4.0% |
| Large appliances, Fire TV devices, mobile electronics | 2.5% |
| Amazon Fresh, groceries, pantry, game consoles, video games | 1.0% |
| **Android apps**, gift cards, Kindle Unlimited, other gift-card brands, Coach products, wine | **0%** |
| All other categories | 3.0% |

**The load-bearing line for this brief: Amazon Associates Italy cannot monetise app installs.** Two separate mechanisms combine. A Play Store or App Store install produces no Amazon.it purchase, so it generates no trackable Amazon link and sits outside the programme's scope altogether. And the one app category Amazon itself carries — Android apps in the Amazon Appstore — is explicitly listed at **0%**. So the affiliate programme Italian creators default to yields nothing on app promotion by either route. This is a structural reason the Italian app-promo affiliate channel is thin, and it should be read as part of the explanation for the negative results in §3.3.

Note also that widely-circulated Italian blog tables giving Amazon.it rates of 7–12% (e.g. webhero.it, 2018-06-30 ⚠️, and Shopify's Italian blog, 2026-05-05) **conflict with Amazon's own current page** and appear to reproduce superseded schedules. Prefer the operator's page.

### 3.2 TikTok Shop Italy — the one live creator-commission channel with published terms

| Fact | Value | Source | Confidence |
|---|---|---|---|
| Italian launch date | **31 March 2025** | TechCrunch, https://techcrunch.com/2025/03/27/tiktok-to-launch-tiktok-shop-in-france-germany-and-italy/, 2025-03-27 ⚠️; confirmed by Il Sole 24 Ore, https://en.ilsole24ore.com/art/first-black-friday-tiktok-shop-how-e-commerce-social-works-AHMaUCzD, 2025-11-27 | high |
| Active Italian sellers | 8,000+ | Il Sole 24 Ore, 2025-11-27, interview with Massimo Rocchelli, Operations Lead TikTok Shop Italia | high |
| Platform commission on sales | 5% | same | high |
| Creator affiliate eligibility | 18+, **≥1,500 followers** | ARS, https://www.ars.srl/en/tiktok-shop-has-arrived-in-italy-opportunities-for-brands-and-creators/, 2025-04-03 ⚠️ | medium |
| Typical creator commission | 5–20% of sale price | LegaleFiscale, https://www.legalefiscale.it/ecommerce/tiktok-shop-italia-2026-guida-fiscale-per-vendere-sui-social/, 2026-04-27 | medium (tax advisory firm, not platform source) |

This is a genuine, low-threshold, performance-based Italian creator channel with a published commission model — but it is **physical-goods commerce**. There is no app-install equivalent inside it.

### 3.3 App-install affiliate and CPA norms — a genuine negative

Searched bilingually for Italian app-install affiliate practice, creator CPI deals, and app-promo code norms. **Nothing published and Italy-specific was found.** What exists instead:

- **Affiliate networks operate in Italy with creator programmes** — Awin (https://www.awin.com/it/publisher/content-creator-influencer, undated, low), CJ (e.g. Notino's Italian creator programme paying 12–14% with quarterly bonuses, https://www.notino.it/affiliate-program/, undated, low), plus Rakuten, Tradedoubler, Impact and eBay Partner Network, all named as routinely used by Italian publishers. **No network publishes Italian creator participation rates.**
- **The only Italian CPA norms published with numbers are for regulated verticals, not apps.** For iGaming, forex and prop trading, the Italian market standard is a hybrid of **CPA €30–50 plus 15–20% RevShare on NGR**, with click-to-first-deposit conversion benchmarks of 2–6% (iGaming), 1–4% (forex) and 3–8% (prop trading). Source: track360, https://track360.io/it/blog/affiliate-marketing-italia, 2026-04-27. Confidence: **low** (vendor blog, no stated sample). These are *not* transferable to a consumer app: the verticals have far higher LTV and are shaped by the Decreto Dignità advertising ban and Consob/ESMA rules.
- **Promo codes and affiliate links are established enough in Italy to be formally regulated.** The IAP Digital Chart devotes Article 4 to discount codes and affiliate marketing, requiring the label "link affiliato + brand" alongside the standard advertising disclosure. Regulatory codification is indirect but solid evidence the practice is mainstream (IAP, version approved 2024-10-30, in force; see §4.4).
- **Affiliation is a named income stream for Italian creators.** The Fiscozen/Kolsquare study lists the main earning models as sponsorships, affiliate marketing, own product/service sales, and content production for third parties — but publishes no split between them (2026-04-21, high for the study, but the split is simply not reported).

**Bottom line for item 3: affiliate infrastructure exists in Italy and creators use it, but there is no published Italian norm for app-install deals, and the default Italian affiliate programme pays zero on apps.** A solo dev will be negotiating a bespoke deal with no public comparable.

### 3.4 Tax and reporting facts a dev should know when structuring creator deals

| Fact | Detail | Source | Confidence |
|---|---|---|---|
| Dedicated influencer ATECO code | **73.11.03**, in force since April 2025, alongside the retained 73.11.01/02 | Fiscozen/Kolsquare via Rainews, https://www.rainews.it/articoli/2026/04/-influencer-40mila-in-italia-fatturato-medio-24mila-euro--ac04738b-5d51-4733-bbde-003129a74c9a.html, 2026-04-21 | high |
| Adoption of that code | only **2.5%** of ~40,000 professionals | same | high |
| Forfettario ceiling 2026 | €85,000 (immediate exit above €100,000) | LegaleFiscale, 2026-04-27 | medium |
| INPS Gestione Separata rate 2026 | 26.23% | same | medium |
| DAC7 platform reporting | platforms report sellers with ≥30 transactions **and** >€2,000/year to the Agenzia delle Entrate | same (D.Lgs. 32/2023) | medium |

Practical consequence: most Italian creators you would approach at nano/micro scale do **not** hold the dedicated code and may be operating as occasional or secondary activity. Invoicing arrangements will vary, and this affects contract structure more than it affects price.

---

## 4. Regulatory constraints a solo dev must know

### 4.1 The framing that matters

The AGCOM influencer register is the headline everyone repeats, and it is **almost certainly irrelevant to a solo dev's actual exposure**. Two reasons: the threshold is 500,000 followers or 1,000,000 average monthly views, which no nano/micro creator approaches; and the registration obligation falls on the *creator*, not on the advertiser commissioning the content.

What actually binds a solo dev who pays or gifts an Italian creator is the general advertising-transparency regime, and AGCOM says so itself. From AGCOM's own explanatory annex: transparency and minor-protection obligations "operano comunque in capo a tutti gli influencer, in quanto derivanti da normative generali (TUSMA, Codice del Consumo) e standard di settore, nonché da vincoli delle piattaforme" — they apply to *all* influencers regardless of size, because they derive from general law. Source: AGCOM, *Allegato A — Quadro normativo e profili procedurali — Influencer*, https://www.agcom.it/sites/default/files/media/allegato/2026/Allegato%20A%20-%20Quadro%20normativo%20e%20profili%20procedurali%20-%20Influencer.pdf (hosted under /2026/, no explicit publication date on the file). Confidence: **high** (regulator-published).

The enforcement risk to the advertiser runs through **pubblicità occulta** under the Codice del Consumo (d.lgs. 206/2005), policed by AGCM, which reaches whoever commissioned undisclosed promotional content.

### 4.2 The AGCOM instruments and their current status

| Instrument | Date | Status |
|---|---|---|
| Delibera **7/24/CONS** — influencer guidelines, technical roundtable | 10 January 2024 | **In force as amended.** Not superseded; amended by 197/25/CONS. |
| Delibera **197/25/CONS** — amendments to 7/24 guidelines + approval of the influencer code of conduct | adopted 23 July 2025, published 5 August 2025 | **In force.** https://www.agcom.it/provvedimenti/delibera-197-25-cons |
| Delibera **269/25/CONS** — renewed AGCOM–IAP framework agreement | 12 November 2025 | **In force.** https://www.iap.it/wp-content/uploads/2025/12/269_25_CONS_signed-1.pdf |
| AGCOM FAQ for influencers + technical/legal framework annex for professionals, agencies, brands | 2026 | Published. https://www.agcom.it/comunicazione/comunicati-stampa/comunicato-stampa-82 |

All confidence: **high** (regulator-published primary sources).

### 4.3 The register ("elenco degli influencer rilevanti") — thresholds and deadlines

Applies to creators only, and only above threshold. Included for completeness and because a dev may need to know whether a prospective partner is inside the regime.

| Item | Detail |
|---|---|
| Threshold | **500,000 followers** on at least one platform **OR 1,000,000 average monthly views** (arithmetic mean over the preceding 6 months). Crossing either threshold on *one* platform binds the creator across all platforms they use. |
| Follower count reference date | value 30 days before form submission |
| Registration deadline (first application) | **5 February 2026** (six months from the 5 August 2025 publication of 197/25/CONS) |
| Publication of the list | within 5 months of the deadline |
| Update cadence | semi-annual, 15 April and 15 October |
| Objection window | 15 days from publication of the updated list |
| Nature of the list | **not a professional register (albo)** — AGCOM states this explicitly |
| Non-registration is not a shield | obligations apply from the moment the substantive thresholds are met; failure to register does not exclude liability for conduct |

Sources: AGCOM web form notice, https://www.agcom.it/comunicazione/avvisi/e-online-il-web-form-agcom-liscrizione-allelenco-degli-influencer-rilevanti; AGCOM Allegato A (above); Linee guida allegate a 197/25/CONS. Confidence: **high**.

Penalties reported for the register regime: **€516 to €103,291** for failing to submit the form within the deadline, and **€10,329 to €258,228** for failing to comply with AGCOM orders and formal warnings; AGCOM may additionally order content removal, suspend commercial communication activity for a set period, and notify platforms. Source: Leggio (law firm), https://www.leggio.lawyer/influencer/albo-influencer-iscrizione/, 2025-11-10. Confidence: **medium** (law-firm reading; the Codice di condotta itself refers to the sanction regime of arts. 38 and 67 TUSMA and to delibera 410/14/CONS without restating the amounts in the text retrieved).

### 4.4 Disclosure: the actual wording required

The AGCOM code of conduct expressly incorporates the **IAP Digital Chart** as the operative standard. Regolamento Digital Chart, version approved **30 October 2024**, currently in force: https://www.iap.it/codice-e-altre-fonti/regolamenti-autodisciplinari/regolamento-digital-chart/. Confidence: **high** (self-regulatory body's own text, expressly cross-referenced by the regulator).

| Situation | Required label |
|---|---|
| Paid commissioning relationship with a brand (money, goods, invitations, services, or anything else of value) | "**pubblicità**" or "**advertising**"; alternatively "promosso da … brand" / "promoted by …", "sponsorizzato da … brand" / "sponsored by … brand" |
| Free product sent occasionally, **no** commissioning relationship | a distinct disclaimer of the gifting nature — *not* the advertising label above |
| Invitation to an event or free use of a service, no commissioning relationship | a distinct disclaimer of that nature |
| **Discount codes and affiliate links** | "**link affiliato + brand**" / "affiliate link + brand", **in addition to** the Article 1 advertising labels |
| Expiring content (Stories) | the label must be **superimposed visibly on the visual elements of every promotional frame** |
| Reposts/shares to other platforms | the disclosure must persist |
| Call-to-action driving user-generated content | the advertiser and/or influencer must require users to disclose too |

Legibility is a substantive requirement, not a formality: contrasting colours, adequate font size, and for on-video disclaimers, persistence on screen.

The AGCOM–IAP framework agreement (269/25/CONS, 12 Nov 2025) commits both bodies to publish joint operational guidelines with worked examples, checklists and a glossary, covering specifically **affiliate links, product seeding, brand thank-yous, discount codes, comparisons and live shopping**, and names the minimum declarative formats as "**#adv**, 'pubblicità', 'partnership a pagamento', and native platform tags". Confidence: **high** (text of the delibera).

### 4.5 The state of enforcement, 2025–2026

**AGCM (Antitrust) is the active enforcer against undisclosed advertising, and it fines.**

On **11 June 2025** ⚠️ AGCM closed six proceedings opened in July 2024 (PS12814–PS12818, PS12826): two fines totalling **€65,000** — €60,000 to Luca De Stefani ("Big Luca") and €5,000 to Michele Leka — and four cases closed with binding commitments (Luca Marani, Alessandro Berton, Hamza Mourai, Davide Caiazzo). The conduct: systematically publishing paid-advice content promising "easy and secure earnings" **without any advertising label**, and without adequately disclosing prices. De Stefani was additionally penalised for **inflating popularity with fake Instagram followers** and using exclusively positive, unverifiable testimonials. The accepted commitments included inserting advertising disclaimers, removing inauthentic followers and monitoring for them, and bringing online activity into consumer-law compliance. Source: AGCM press release, https://en.agcm.it/en/media/press-releases/2025/6/PS12814-PS12815-PS12816-PS12817-PS12818-PS12826, 2025-06-11. Confidence: **high** (regulator primary source).

Earlier, in **January 2025** ⚠️, AGCM closed four moral-suasion interventions (Ludovica Meral Frasca, Sofia Giaele De Donà, Milena Miconi, Alessandra Ventura). Same source, high.

AGCM's **annual report presented in April 2026** confirms this is a standing programme, not a one-off: the Authority states that influence marketing "può presentare un più alto rischio di pubblicità occulta e ingannevole rispetto alle altre forme di pubblicità online", and records the six proceedings above as falling in the **credit/investment sector**. Source: Il Sole 24 Ore, https://www.ilsole24ore.com/art/antitrust-come-si-e-mossa-l-authority-investitori-e-influencer-AI3326UC, 2026-04-19. Confidence: **high**.

**Compliance in the market is poor, and measurably so.** Among the 5,000 highest-interaction pieces of content DeRev analysed for 2026:

| Platform / format | Share carrying a sponsorship disclosure |
|---|---|
| TikTok (top-interaction posts) | **0.78%** |
| Instagram (top-interaction posts) | **4.46%** |
| YouTube long-form video | **29%** |
| YouTube Shorts | **1.5%** |

By contrast, commercial calls-to-action appear in **74.9%** of YouTube long-form videos and 10.1% of Shorts — that is, the CTA is present far more often than the disclosure. Source: DeRev 2026-07-02; Il Sole 24 Ore 2026-07-02. Confidence: **medium**. DeRev's CEO Roberto Esposito calls the TikTok figure "certainly an anomaly" that, with the AGCOM code and the dedicated ATECO classification now operative, is set to become a growing concern "particularly for brands, which need to be assured of full compliance".

**The practical read for a solo dev.** The market norm you will encounter — especially on TikTok — is non-disclosure. Accepting that norm puts *you* in AGCM's line of fire as the commissioning advertiser, not just the creator. Put the disclosure requirement in the contract, specify the exact wording from §4.4, and require the label to persist on reposts and Stories.

### 4.6 One sector-specific trap: finance

If the app touches investing, trading or personal finance, an additional regime applies. Consob and ESMA published guidance in late 2025 / January 2026 stating that telling people what to invest in "può essere considerata una forma di consulenza che richiede un'autorizzazione rilasciata dall'autorità nazionale competente", and that **a generic disclaimer does not avoid the legal consequences of unauthorised promotion**. Fininfluencers must explicitly declare paid content, highlight product risks, and avoid misleading messaging. Note that 70% of Italian fininfluencers have an economics education but **seven in ten are not registered with the financial advisers' register**. Source: MilanoFinanza, https://www.milanofinanza.it/news/il-faro-della-consob-sui-guru-della-finanza-online-chi-sono-i-fininfluencer-italiani-202601231844247449, 2026-01-23. Confidence: **medium**.

This is also exactly the sector in which AGCM's six 2025 fines landed. Treat finance-adjacent creator promotion in Italy as the highest-risk configuration available.

---

## 5. Practical channel notes

### 5.1 Who the Italian creator population actually is

From the Fiscozen + Kolsquare joint study (Fiscozen: 5,000+ VAT-registered professionals; Kolsquare: 5,377 Italian influencers sponsored ≥12 times in the year, 6,689,721 contents analysed). Published 2026-04-21. Confidence: **high**.

| Metric | Value |
|---|---|
| Professional influencers in Italy | ~40,000 |
| Using the dedicated ATECO code 73.11.03 | 2.5% |
| Average turnover 2025 | **€24,038** (+11.8% vs €21,502 in 2024) |
| — women / men | €21,840 / €26,237 |
| Average turnover, those on the new ATECO code | €34,521 |
| Average turnover, influencer-marketing & content-creation codes overall | €39,947 (+23%) |
| Gender split | 66% men |
| Median age | 32 |
| Share in nano (1–10K) + micro (10–100K) tiers | **74%** |
| Share of published content that is a paid collaboration | **3.1%** |
| Brands that invested in influencer marketing in Italy | 16,700+ |
| Platform preference among brands | Instagram 93%, TikTok 79%, YouTube 69%, Facebook 54%, LinkedIn 34% |
| Most active brands by sponsored-content volume | Shein (41,000+ contents, 1,000+ creators), Prozis, YesStyle, Sheglam, Volgo Italia, Aboca, Degusta Box, Temu, FGM04, Koro |

Two numbers reframe the opportunity. **74% of Italian professional creators are nano or micro** — this is a long-tail market, not a celebrity market. And **only 3.1% of what they publish is paid** — meaning the inventory is enormous relative to the demand, which is consistent with DeRev's finding that nano rates are being eroded by supply growth.

Average turnover of €24,038 also tells you the negotiating posture: for most of these people this is a secondary income, and a €200–300 collaboration is a meaningful proportion of a month.

### 5.2 Engagement rates by tier — the two Italian datasets

**The two datasets are not directly comparable and must not be merged.** Kolsquare defines its engagement rate as the ratio between number of contents and interactions; DeRev divides interactions per post by follower count at time of publication. Different denominators, and different nano bands too (Kolsquare 1–10K, DeRev 5–10K). Each is internally consistent; a figure from one cannot be placed beside a figure from the other. The cross-platform conclusion drawn below rests on Dataset B alone.

**Dataset A — Kolsquare, cross-platform, Italian professional influencers, 2026-04-21, confidence high:**

| Tier | Engagement rate |
|---|---|
| Nano (1–10K) | **7.7%** |
| Micro (10–100K) | **4.6%** |
| Celebrity (>1M) | not published as a rate; averages **52.5 sponsorships/year**, the highest of any tier |

**Dataset B — DeRev, per platform, 2024 → 2025 movement.** Extracted from the DeRev *Listino 2025* PDF, https://www.foodaffairs.it/wp-content/uploads/2025/07/Report-Listino-Influencer-2025_compressed.pdf ⚠️ *older than 12 months*. Confidence: **medium**. Method: interactions per post divided by follower count at time of publication, averaged across all the creator's posts in the year.

| Tier | Facebook | Instagram | TikTok | YouTube |
|---|---|---|---|---|
| Nano | 0.2% → 0.9% | 6% → 5.4% | 5% → 8.5% | 4.5% → 4.7% |
| Micro | 0.25% → 0.5% | not published | not published | 4% → 6.9% |
| Mid-tier | 0.3% → 0.4% | 5.5% → 5.25% | 8.5% → 9.5% | 3% → 5.9% |
| Macro | 0.4% → 0.5% | 4.5% → 3.8% | 5.5% → 6% | 2% → 2.25% |
| Mega | 0.3% → 0.2% | not published | 3% → 3.8% | 1.5% → 1.2% |
| Celebrity | 0.2% → 0.15% | not published | not published | 1.25% → 0.9% |

**Dataset C — DeRev 2026 edition, Instagram only, confidence medium:** mid-tier post interaction rate **4.56%**, three times the celebrity rate of **1.61%**. Follower growth in the year: 76.7% of mid-tier profiles growing, 68.5% of macro, only 36.8% of celebrity — and 63.2% of celebrity profiles *lost* followers.

Reading across all three: **TikTok carries the highest engagement rates of any Italian platform at every tier** (mid-tier at 9.5% in 2025), **Facebook is engagement-dead** (below 1% everywhere), and **engagement falls monotonically with tier size on every platform except Facebook**. Combined with the rate table in §2, the cost-per-engagement optimum for a small budget sits squarely in nano/micro on TikTok and Instagram.

### 5.3 Barter and gifting — documented Italian practice

**Yes, gifting is documented, measured monthly, and formally recognised in regulation.** Three independent strands:

**(a) Measured volume.** ONIM (Osservatorio Nazionale Influencer Marketing) tracks Italian sponsored content by IAP-compliant hashtag every month, in partnership with Talkwalker, Primetag and Tactik. For **January 2026** on Instagram: 13.3K sponsored posts, of which #adv 6.2K mentions, #ad 3.0K, **#gifted 1.5K**. Source: https://www.onim.it/wp-content/uploads/2026/03/ONIM_Report-Sponsored-Gennaio-2026_Instagram.pdf, data Jan 2026. Confidence: **medium**.

For **February 2026**, ONIM reports 23.1K sponsored Instagram *stories* with 1.6bn estimated impressions, and notes that alongside #adv, "**prevalgono #invitedby e #gifted**" — confirming the Stories format is disproportionately used for experiences, event invitations and gifting activity. Source: https://www.onim.it/2026/05/12/influencer-e-sponsored-post-ig-e-video-tiktok-e-youtube-i-dati-di-febbraio-2026/, 2026-05-12. Confidence: **medium**.

**(b) Regulatory recognition.** The IAP Digital Chart devotes a dedicated article (Art. 3) to the case where "il rapporto tra influencer e inserzionista non sia di committenza, ma si limiti all'invio occasionale … di propri prodotti gratuitamente o per un prezzo di favore", prescribing a distinct disclaimer. A self-regulatory code does not create a category for a practice that does not exist at scale.

**(c) Agency assertion — weaker evidence, kept separate.** Migliore Agenzia states that "nano-influencers often accept gifting collaborations (free product + a small fee)" (2026-04-16, **low** confidence, single agency, no sample). This is consistent with (a) and (b) but is not independent evidence.

**The specific case this brief asks about — a free app subscription in exchange for a post — is not documented in any Italian source found.** All the measured gifting evidence is shaped around *physical products* and *event invitations*. See the negative log.

### 5.4 Monthly market rhythm — when to buy

ONIM's monthly series shows severe seasonality that a small budget can exploit. Confidence: **medium** throughout (ONIM/Talkwalker/Tactik).

| Month | Instagram sponsored posts | TikTok sponsored videos | YouTube sponsored videos |
|---|---|---|---|
| Sept 2025 | 17.1K (+30% MoM) | 4.0K (+30%) | 3.7K (+60.9%) |
| Dec 2025 | ~19.5K (derived from Jan's −31.79%) | ~3.4K (derived) | 3.9K (+14.7%) |
| **Jan 2026** | **13.3K (−31.79%)**, interactions/post 571 (−30.36%) | **2.2K (−35.43%)** | 3.1K (−20.51%) |
| Feb 2026 | 19.9K (+~50%), interactions/post 784 (+37.9%) | 4.4K (+93%) | 3.4K (+9.68%) |
| Mar 2026 | — | — | 3.7K (+8.82%) |

August and January are the troughs; February (Sanremo, Milan Fashion Week, and in 2026 the Milano Cortina Olympics) and September are the peaks. **January is the cheapest month to approach Italian creators** — demand collapses by roughly a third across all three platforms.

Cross-check from IAB Italia's AdReport for March–April 2026 (automated 24/7 monitoring of a catalogue of Italian influencers and ~1,000 advertisers; the influencer count is truncated in the retrieved excerpt and is not reported here): Instagram 719 active advertisers, 1,023 active influencers, 3,125 posts, 60.64% Reels; TikTok 599 active advertisers, 793 active influencers, 8,622 posts including 2,785 declared Paid Partnerships. Source: https://iab.it/adreport-scenario-influencer-instagram-e-tiktok-marzo-aprile-2026/, 2026-05-27. Confidence: **medium**. Note a discrepancy on that page: its headline reads "luglio/agosto 2025" while both the URL slug and the body text describe March–April 2026; the body is taken as authoritative here.

### 5.5 Format notes

- **Instagram Stories are the daily working surface** — 83.6% of Italian influencer output by volume — while Reels and posts carry visibility and are the primary vehicle for collaborations (Fiscozen/Kolsquare, 2026-04-21, high). DeRev prices a "story set" as up to 3 consecutive stories, and story-set rates rose 3.8% in 2026 against 2.45% for posts.
- **Reels dominate Instagram sponsored content** at 60.64% of posts (IAB Italia, 2026-05-27, medium), and ONIM reports the Reel dominating both usage and engagement (Jan 2026, medium).
- **TikTok content is 94%+ video-first from the micro tier upward** (DeRev 2026, medium).
- **YouTube has split into two markets.** Shorts are 96.6% of nano output and 90% of macro output by volume, but campaign money concentrates in long-form. Shorts entered the DeRev listino as a standalone format for the first time in 2026, priced at roughly **one third** of a traditional video (DeRev 2026-07-02, medium).

---

## Does not exist publicly (negative-result log)

Each entry was actively searched for in this pass, in Italian and English, and not found.

1. **App-install creator campaigns in Italy — no data of any kind.** No CPI or CPA norms, no rate card, no case studies, no conversion benchmarks for creator-driven mobile app installs in the Italian market. DeRev, ONIM, IAB Italia and Kolsquare all measure consumer-goods brand spend; none has an app or software category. This is a structural absence, not a search failure.
2. **No published Italian rate for "macro >500K" as a single band.** DeRev splits at 300K–1M / 1M–3M on Instagram and TikTok, and at 100–500K / 500K–1M / >1M on YouTube. Any single number for ">500K" in Italy would be an invention.
3. **No published Italian rate for "micro 10–100K" as a single band.** It straddles DeRev's micro (10–50K) and mid-tier (50–300K).
4. **No published Italian rate card for the app / software / SaaS vertical.** StarNgage publishes Italian vertical splits for beauty, fitness and tech, but the page is undated, reads as relabelled global boilerplate, and does not cover apps.
5. **DeRev's full euro grid is not publicly retrievable.** The 2026 grid sits behind a lead-capture form on derev.com; the 2025 PDF's compensation tables are rendered as images and did not extract as text. Only the individual euro points quoted in press coverage (§2.2, §2.4) and the percentage movements (§2.3) are public.
6. **Amazon publishes no Italy-level affiliate participation statistics** — no count of Italian Associates, no average Italian affiliate earnings, no category mix for Italy. The commission schedule is published; everything about uptake is not.
7. **No affiliate network (Awin, CJ, Rakuten, Tradedoubler, Impact) publishes Italian creator participation rates or average Italian creator earnings.**
8. **No documented Italian practice of "free app subscription in exchange for a post."** Italian gifting/barter evidence — ONIM's #gifted and #invitedby tracking, IAP Digital Chart Art. 3 — is entirely shaped around physical products and event invitations. Whether Italian creators accept a software subscription as consideration is unmeasured.
9. **Audicom does not publish per-platform social media MAU.** Its deduplicated currency covers editorial and publisher audiences (text and video, including CTV) plus print readership. It cannot be used to validate or replace DataReportal's platform ad-reach figures.
10. **No dated, freely available Comscore Italy ranking of social platforms** was found. Comscore Italy data appears in this market only via paywalled subscriptions or undated press restatements.
11. **TikTok publishes no 13–17 audience data for Italy.** Its ad tools expose only 18+, so the 22.0M figure understates total Italian TikTok usage by an unknown amount. Any Italian "total TikTok users" figure including minors is an estimate, not a platform-published number.
12. **No published Italian creator rate or engagement data for the *genitorialità* (parenting) vertical.** It does not appear as a measured category in DeRev, ONIM, IAB Italia or Kolsquare. Personal relationships (25.8%) is the nearest adjacent category and is not the same thing.
13. **No published Italian creator rate data broken out for *calcio* specifically.** Sport & fitness appears as a creator niche (21.1%) and sport & leisure as a spend share (9%), but neither isolates football, despite its obvious weight in Italian attention.
14. **No published Italian benchmark for creator-driven app-install conversion rate.** The only Italian click-to-conversion benchmarks found (2–6% iGaming, 1–4% forex, 3–8% prop trading, track360, 2026-04-27, low) are for regulated financial verticals with structurally different LTV and are not transferable.
15. **ONIM's Brand & Marketer and Influencer & Creator survey data on barter share and remuneration models is not publicly retrievable.** ONIM's free report archive ends at the 2024 Brand & Marketer edition; the surveys that would quantify how many Italian creators accept payment in product are gated.
16. **No published Italian rate for creators below 5,000 followers.** DeRev's nano band starts at 5K on all four platforms (it moved YouTube's floor up from 3K in the 2025 edition for cross-platform comparability). Sub-5K creators — the very bottom of the long tail, and plausibly the most accessible tier for a solo dev — are unmeasured in Italian data.
17. **No Italian creator rate card was found that quotes prices in cost-per-view or cost-per-thousand-impressions terms.** All published Italian pricing is per-content flat fee, which makes cross-platform efficiency comparison impossible from public data alone.

### Sources deliberately excluded

- **Black Ads, *Market Intelligence Vol. 07 Italy*** (https://black-ads.agency/reports/market-intelligence/Black_Ads_Market_Report_Vol07_Italy_EN.pdf) — undated, unattributed methodology, and its Italian platform figures appear to be lifted directly from DataReportal. Its Facebook (28.5M) and LinkedIn (25.0M) numbers were re-verified against DataReportal's own page and are reported here from that primary source instead.
- **Datambar, *Italy Social Media Usage Trends 2026*** (2026-01-29) — n=600 CAWI panel, and its TikTok figures are internally incoherent (overall daily usage stated at 71% with a subgroup at 84.2% while the claimed peak is 69.6%).
- **mondotv24 "Classifica Influencer Italiani 2026"** (2026-06-18) — presents a rate table attributed to "DeRev e I-Com" whose tier bands and euro values contradict DeRev's own published listino.

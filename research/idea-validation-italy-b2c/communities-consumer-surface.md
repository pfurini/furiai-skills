# Italian-language consumer communities, verified active

Research question DA5 of the Italy-first consumer-app calibration pass.
All activity evidence gathered on **2026-08-13**. Every surface listed below was fetched; nothing here is carried over from memory or from a secondary listicle.

## Methodology and verdict rules

**Reddit.** `reddit.com` blocks unauthenticated fetches (both the HTML and the `.json` endpoints return a login wall or a "network policy" block), so activity was verified through a Redlib mirror (`safereddit.com`) that renders the canonical post feed with exact UTC timestamps and the true subscriber count. **The table cites the canonical `reddit.com` URL**, because that is the surface a human will open and mirrors are not durable. Each check retried three times; a mirror failure was never allowed to produce a DEAD verdict.

**Forums.** Fetched the board index and parsed last-post dates. Two traps were found and corrected during this pass, and both matter for anyone extending this work:

- phpBB and forumattivo boards print a **board clock** ("Oggi è 13 ago 2026") that regex-matches as a post date. `forum.gravidanzaonline.it` looks same-day active by that signal but its newest real last-post is 6 Jul 2026. Last-post dates were therefore re-extracted from the "Ultimo messaggio" / "Ultimi argomenti attivi" blocks specifically.
- Substring matching on the relative markers "oggi"/"ieri" produces false positives from ordinary Italian words (the username `cantierimodellinavali` contains "ieri"). All marker counts below are word-bounded.

**Subscriber counts.** All member counts are live sidebar values read from the mirror on 2026-08-13. They differ, sometimes sharply, from the widely-cited `awesome-italian-reddit` listing regenerated 2026-02-08 — r/ItalyFitness 17,098 → 28,640, r/scimmieinborsa 15,947 → 31,799, r/TeenagersITA 38,529 → 67,899. The gap is growth, not an error: mature r/italy moved 1,101,624 → 1,144,297 over the same six months (+3.9%, a plausible organic rate), which indicates the mirror field is a genuine subscriber count rather than something else. The near-doubling of the smaller subs is consistent with reported Reddit growth in Italy (+81% in early 2025 per Repubblica, 2025-12-02). Use the figures here, not the February listing.

**Facebook.** Walled (an unauthenticated group fetch returns HTTP 400). Per the b2b pass convention, Facebook groups are recorded as **existence-signal only** and never as verified-active.

**Verdicts.**

| Verdict | Rule |
|---|---|
| ACTIVE | Newest post within 60 days **and** the fetched page (25 posts for Reddit) spans ≤60 days |
| DEGRADED | Newest post within 60 days but the same page reaches much further back — real but thin |
| DEAD | Fetched cleanly, newest post older than ~12 months, or effectively no posts |
| UNVERIFIABLE | Login-walled, bot-walled, private, or the mirror failed after 3 retries — **not** evidence of absence |

---

## General Italy subreddits (usable for consumer signal)

These are the broad surfaces where an Italian consumer app would get cross-niche signal. All five are Italian-language.

| Surface | Platform | URL | Members | Last-activity evidence (2026-08-13) | Verdict |
|---|---|---|---|---|---|
| r/italy | Reddit | https://www.reddit.com/r/italy/ | 1,144,297 | Newest post Aug 13 2026 03:00 UTC; 25 posts span Aug 11–13 (~12/day) | ACTIVE |
| r/Italia | Reddit | https://www.reddit.com/r/Italia/ | 671,923 | Newest Aug 13 2026 18:24 UTC; all 25 posts from Aug 13 alone | ACTIVE |
| r/CasualIT | Reddit | https://www.reddit.com/r/CasualIT/ | 125,327 | Newest Aug 13 2026 18:23 UTC; 25 posts span Aug 13 12:07–18:23 | ACTIVE |
| r/Libri | Reddit | https://www.reddit.com/r/Libri/ | 105,969 | Newest Aug 13 2026 17:47 UTC; 25 posts span Aug 11–13 | ACTIVE |
| r/consigli | Reddit | https://www.reddit.com/r/consigli/ | 17,110 | Newest Aug 13 2026 17:51 UTC; 24 posts span Aug 12–13 | ACTIVE |

r/Italia and r/CasualIT burn through 25 posts inside a single day, which makes them the highest-velocity Italian-language general surfaces available. r/consigli is small but is explicitly an advice-seeking surface, which is disproportionately useful for consumer problem discovery relative to its size.

---

## (a) Personal finance, budgeting, investing

The single strongest consumer niche on Italian Reddit — comfortably the best-served of all ten.

| Surface | Platform | URL | Members | Last-activity evidence (2026-08-13) | Verdict |
|---|---|---|---|---|---|
| r/ItaliaPersonalFinance | Reddit | https://www.reddit.com/r/ItaliaPersonalFinance/ | 281,663 | Newest Aug 13 2026 18:12 UTC; all 25 posts from Aug 13 (09:09–18:12) | ACTIVE |
| r/scimmieinborsa | Reddit | https://www.reddit.com/r/scimmieinborsa/ | 31,799 | Newest Aug 10 2026 19:35 UTC; 25 posts span Aug 10 only | ACTIVE |
| r/bollette | Reddit | https://www.reddit.com/r/bollette/ | 5,975 | Newest Aug 13 2026 18:14 UTC; 25 posts span Aug 07–13 | ACTIVE |
| r/TradeRepublic_IT | Reddit | https://www.reddit.com/r/TradeRepublic_IT/ | 3,039 | Newest Aug 13 2026 17:11 UTC; 25 posts span Jul 27 – Aug 13 | ACTIVE |
| r/BitcoinItalia | Reddit | https://www.reddit.com/r/BitcoinItalia/ | 822 | Only 2 posts on the feed, newest Sep 28 2021 | DEAD |
| r/ItaliaInvestimenti | Reddit | https://www.reddit.com/r/ItaliaInvestimenti/ | 1 | 3 posts, all Oct 05 2023 | DEAD |

Two of these rows look similar in the table but are opposite phenomena, and the distinction matters when reading any row here. **r/scimmieinborsa** shows all 25 posts from Aug 10 alone: that is a same-day burst, i.e. very high velocity, sampled three days before the fetch. A row whose newest post is a few days old is only a staleness signal when the 25 posts are *spread* over a long window — as with r/GustoItalia (163 days) or r/SenzaGlutine (292 days), both demoted to DEGRADED. Read the span, not just the newest date.

r/ItaliaPersonalFinance moves 25 posts in nine hours — the highest-velocity niche consumer surface found anywhere in this pass. r/bollette (utility bills) and r/TradeRepublic_IT are notable because both are *product-and-pricing* surfaces rather than general chatter, which is where consumer purchase-intent language actually lives.

---

## (b) Health & fitness / palestra

Well served, and unusually the independent forums are as alive as Reddit — one of only two niches where that is true.

| Surface | Platform | URL | Size | Last-activity evidence (2026-08-13) | Verdict |
|---|---|---|---|---|---|
| r/ItalyFitness | Reddit | https://www.reddit.com/r/ItalyFitness/ | 28,640 | Newest Aug 13 2026 13:25 UTC; 25 posts span Aug 10–13 | ACTIVE |
| BodyWeb | vBulletin forum | https://www.bodyweb.com/forum/ | not shown on index | Newest last-post date on board index 13-08-2026 (same day); 2nd newest 10-08-2026 | ACTIVE |
| Bodybuilding Homepage | vBulletin forum | https://www.bbhomepage.com/forum/ | 58,658 discussions / 764,153 messages / 46,541 users | Newest last-post 11-08-2026; word-bounded "oggi" ×3 and "ieri" ×6 on the index | ACTIVE |
| r/BodybuildingItalia | Reddit | https://www.reddit.com/r/BodybuildingItalia/ | 83 | 24 posts, newest Oct 11 2023 | DEAD |
| r/palestra | Reddit | https://www.reddit.com/r/palestra/ | 2 | 2 posts, newest Dec 27 2021 | DEAD |

BodyWeb and bbhomepage are 20-year-old vBulletin boards still posting daily. They carry long-form training and diet threads that have no Reddit equivalent in Italian, so for this niche the forums are not a fallback — they are a primary surface.

---

## (c) Nutrition / cucina

Weak, and it fails in a specific way worth flagging: the largest "Italian food" surfaces on Reddit are **English-language communities of foreigners**, not Italian consumer communities.

| Surface | Platform | URL | Members | Last-activity evidence (2026-08-13) | Verdict |
|---|---|---|---|---|---|
| r/veganita | Reddit | https://www.reddit.com/r/veganita/ | 20,923 | Newest Aug 13 2026 12:36 UTC; 24 posts span Jul 27 – Aug 13 | ACTIVE |
| r/GustoItalia | Reddit | https://www.reddit.com/r/GustoItalia/ | 5,615 | Newest Aug 10 2026 18:56 UTC, but 25 posts reach back to Feb 28 2026 | DEGRADED |
| r/SenzaGlutine | Reddit | https://www.reddit.com/r/SenzaGlutine/ | 333 | Newest Aug 10 2026 13:27 UTC, but 25 posts reach back to Oct 22 2025 | DEGRADED |
| r/ricette | Reddit | https://www.reddit.com/r/ricette/ | 259 | 25 posts spanning Oct 2019 – Jan 2020 | DEAD |
| r/cucinaitaliana | Reddit | https://www.reddit.com/r/cucinaitaliana/ | 8 | 7 posts, newest Jun 28 2026 | DEAD |

**Language traps in this niche — do not put these in an Italy-first template:** r/ItalianFood (169,430), r/italiancooking (15,574) and r/mediterraneandiet (188,346) are large but are English-language, written by non-Italians about Italian food. They are the wrong audience for an Italian consumer app.

The only genuinely healthy Italian-language food surface is r/veganita, i.e. a *dietary-identity* community rather than a cooking community. General Italian cooking discussion has no live Italian-language Reddit home; see the negative-result log.

---

## (d) Parenting / genitori

The weakest major niche on Reddit and the clearest case of discussion living somewhere other than open forums.

| Surface | Platform | URL | Size | Last-activity evidence (2026-08-13) | Verdict |
|---|---|---|---|---|---|
| Forum alfemminile | Forum (GEDI/Repubblica group) | https://forum.alfemminile.com/ | not shown on index | Word-bounded "ieri" ×6 on the index; active thread "Mamme di ottobre 2026" | ACTIVE |
| PeriodoFertile — Mamme, papà e bambini | bbPress forum | https://www.periodofertile.it/forums/forum/mamme-e-bambini | 496 topics / 9,189 replies | Forum "last updated 3 weeks, 2 days" ago (~Jul 21 2026); next entries 1 month / 1 month 2 weeks / 2 months 1 week | DEGRADED |
| GravidanzaOnLine | phpBB forum | https://forum.gravidanzaonline.it/ | 8,055,194 messages / 25,017 members (lifetime) | **Board clock reads 13 ago 2026 but that is not a post.** Newest real "Ultimo messaggio" is 6 lug 2026 (38 days); most sub-forums last posted 2019–2020 | DEGRADED |
| r/mamme | Reddit | https://www.reddit.com/r/mamme/ | 6 | 4 posts spanning Oct 2023 – Jun 2026 | DEAD |
| r/genitori | Reddit | https://www.reddit.com/r/genitori/ | — | Mirror returned HTTP 403 on 6 attempts across two rounds | UNVERIFIABLE |

**There is no verified live Italian-language parenting subreddit.** The surviving open surfaces are legacy web forums, and two of the three are coasting on archives: GravidanzaOnLine has 8 million lifetime messages but sub-forums whose last posts are from 2019 and 2020, which is exactly the profile of a community that has emptied out into private groups.

---

## (e) Productivity / studio / students

Strong, and concentrated in university-life surfaces rather than productivity-tool surfaces.

| Surface | Platform | URL | Members | Last-activity evidence (2026-08-13) | Verdict |
|---|---|---|---|---|---|
| r/Universitaly | Reddit | https://www.reddit.com/r/Universitaly/ | 137,132 | Newest Aug 13 2026 18:00 UTC; all 25 posts from Aug 13 | ACTIVE |
| r/TeenagersITA | Reddit | https://www.reddit.com/r/TeenagersITA/ | 67,899 | Newest Aug 13 2026 18:26 UTC; 26 posts all from Aug 13 | ACTIVE |
| r/polinetwork (Politecnico di Milano) | Reddit | https://www.reddit.com/r/polinetwork/ | 6,571 | Newest Aug 13 2026 13:38 UTC; 25 posts span Aug 08–13 | ACTIVE |

**Language trap:** r/studenti (11,986) is **Croatian**, not Italian — its title is "Hrvatski studentski kutak". It is active, but it is the wrong country.

Note what is *absent*: these are student-life communities. No Italian-language community dedicated to productivity methods or tools was found; see the negative-result log.

---

## (f) Language learning & education

| Surface | Platform | URL | Members | Last-activity evidence (2026-08-13) | Verdict |
|---|---|---|---|---|---|
| r/italianlearning | Reddit | https://www.reddit.com/r/italianlearning/ | 158,494 | Newest Aug 13 2026 17:34 UTC; 25 posts span Aug 10–13 | ACTIVE **but English-language** |
| r/learnitalian | Reddit | https://www.reddit.com/r/learnitalian/ | 15,674 | Newest Aug 13 2026 13:28 UTC; 25 posts span Aug 05–13 | ACTIVE **but English-language** |
| r/ImparareLingue, r/lingue, r/linguaggi | Reddit | — | — | Mirror failed after 3 retries each | UNVERIFIABLE |

This niche is a trap in its entirety and needs stating plainly: the big, thriving surfaces are **foreigners learning Italian**, described in English ("A place for those interested in learning Italian"). They are not Italian consumers and an Italy-first template must not cite them as such. The mirror-image surface — Italians learning other languages, in Italian — was not found. See the negative-result log.

---

## (g) Gaming

Among the largest Italian-language consumer surfaces in absolute terms.

| Surface | Platform | URL | Size | Last-activity evidence (2026-08-13) | Verdict |
|---|---|---|---|---|---|
| r/italygames | Reddit | https://www.reddit.com/r/italygames/ | 377,208 | Newest Aug 13 2026 17:57 UTC; 25 posts span Aug 11–13 | ACTIVE |
| r/AnimeItaly | Reddit | https://www.reddit.com/r/AnimeItaly/ | 165,380 | Newest Aug 13 2026 14:10 UTC; 25 posts span Aug 02–13 | ACTIVE |

r/italygames (377k) is the second-largest Italian-language niche community found in this whole pass, behind only the general subreddits.

**No Italian gaming Discord is listed here.** The Discord invite API does return live member and presence counts without authentication, and one general-purpose Italian server did resolve with 18,561 members and 2,578 online at fetch time — genuinely strong activity evidence. It is deliberately excluded: it is not a gaming community, and its server name contains an anti-immigrant slur that should not be copied into a template a researcher reads. Two plausible niche invite codes (`italy`, `fantacalcio`) returned "Unknown Invite" (expired). No niche-specific Italian consumer Discord was verified; see the negative-result log.

---

## (h) Tech / apps in general (where Italians discuss apps)

This is the niche most directly relevant to an app-validation template, and it is well served on both Reddit and forums.

| Surface | Platform | URL | Size | Last-activity evidence (2026-08-13) | Verdict |
|---|---|---|---|---|---|
| r/ItalyInformatica | Reddit | https://www.reddit.com/r/ItalyInformatica/ | 193,789 | Newest Aug 10 2026 05:09 UTC; 25 posts span Jul 19 – Aug 10 (22 days) | ACTIVE but slow |
| Hardware Upgrade Forum | vBulletin forum | https://www.hwupgrade.it/forum/ | not shown on index | Newest last-post 11-08-2026; word-bounded "oggi" ×25 and "ieri" ×7 on the index | ACTIVE |
| r/ItalyHardware | Reddit | https://www.reddit.com/r/ItalyHardware/ | 16,084 | Newest Aug 13 2026 06:30 UTC; 25 posts span Aug 12–13 | ACTIVE |
| r/IA_Italia | Reddit | https://www.reddit.com/r/IA_Italia/ | 7,700 | Newest Aug 13 2026 13:12 UTC; 25 posts span Aug 10–13 | ACTIVE |
| r/AndroidItalia | Reddit | https://www.reddit.com/r/AndroidItalia/ | 1,236 | Newest Jul 31 2026, but 25 posts reach back to Sep 2022 | DEGRADED |
| Tom's Hardware Italia forum | Forum | https://www.tomshw.it/forum/ | — | HTTP 403 (bot wall) | UNVERIFIABLE |

One shape worth stating plainly: **r/ItalyInformatica is large but slow** — 193,789 members producing 25 posts in 22 days, roughly one a day, with its newest post three days before the fetch. It clears the 60-day ACTIVE bar comfortably, but a researcher expecting 193k members to mean fast-moving discussion will be disappointed. Hardware Upgrade is the standout instead: 25 separate "oggi" markers on a single board index makes it the busiest independent Italian forum found in this pass. Note the shape of this niche — Italians discuss *hardware and PCs* heavily, but r/AndroidItalia, the closest thing to a mobile-app discussion surface, is DEGRADED at 1,236 members. Consumer *app* discussion specifically has no strong dedicated Italian home; it happens inside the general and hardware surfaces.

---

## (i) Hobby verticals with strong IT presence

Four verified strong: **calcio/fantacalcio, giardinaggio, modellismo, motori.**

### Calcio / fantacalcio

| Surface | Platform | URL | Size | Last-activity evidence (2026-08-13) | Verdict |
|---|---|---|---|---|---|
| r/seriea | Reddit | https://www.reddit.com/r/seriea/ | 530,100 | Newest Aug 13 2026 08:00 UTC; 25 posts span Aug 11–13 | ACTIVE |
| r/Calcio | Reddit | https://www.reddit.com/r/Calcio/ | 122,306 | Newest Aug 13 2026 18:24 UTC; 25 posts span Aug 10–13 | ACTIVE |
| r/fantacalcio_IT | Reddit | https://www.reddit.com/r/fantacalcio_IT/ | 9,486 | Newest Aug 13 2026 18:15 UTC; 25 posts span Aug 12–13 | ACTIVE |
| Fantacalcio (**unverified ownership**) | Telegram channel | https://t.me/s/fantacalcio | not shown | 9 messages rendered on the public feed, newest 2026-08-12 | ACTIVE |
| r/ItalyCalcio | Reddit | https://www.reddit.com/r/ItalyCalcio/ | 934 | 25 posts spanning Jan – Mar 2023 | DEAD |

r/fantacalcio_IT is the sharpest surface here for consumer-app purposes: fantasy-football players are already tool users, and the sub turns over 25 posts in two days at only 9,486 members. Season timing matters — this was sampled in mid-August, at the start of the Serie A fantasy-draft season, so this velocity is near its annual peak.

### Giardinaggio

| Surface | Platform | URL | Size | Last-activity evidence (2026-08-13) | Verdict |
|---|---|---|---|---|---|
| Forum di Giardinaggio.it | Forum | https://www.giardinaggio.it/forum/ | not shown | Word-bounded "oggi" ×9, "ieri" ×4, and two posts marked "53 minuti fa" / "58 minuti fa" at fetch time | ACTIVE |
| r/giardinaggioITA | Reddit | https://www.reddit.com/r/giardinaggioITA/ | 20,562 | Newest Aug 13 2026 14:51 UTC; 25 posts span Aug 04–13 | ACTIVE |

Giardinaggio.it had posts under an hour old at fetch time — the freshest evidence collected anywhere in this pass.

### Modellismo

| Surface | Platform | URL | Size | Last-activity evidence (2026-08-13) | Verdict |
|---|---|---|---|---|---|
| Forum Modellismo.net | vBulletin forum | https://www.modellismo.net/forum/ | 85,032 discussions / 1,296,583 messages / 46,306 users | Word-bounded "oggi" ×4 on the board index | ACTIVE |
| ForumFerrovie.Info | phpBB forum | https://www.forumferrovie.info/ | not shown | Newest real last-post 4 agosto 2026 (9 days); board clock separately confirmed and excluded | ACTIVE |
| Modellisti Navali | forumattivo | https://modellistinavali.forumattivo.com/ | not shown | "Ultimi argomenti attivi" newest 10 Ago 2026; the 9 recent topics span Jul 10 – Aug 10 | ACTIVE (low volume) |

### Motori and other verified hobby surfaces

| Surface | Platform | URL | Members | Last-activity evidence (2026-08-13) | Verdict |
|---|---|---|---|---|---|
| r/ItalyMotori | Reddit | https://www.reddit.com/r/ItalyMotori/ | 123,109 | Newest Aug 13 2026 17:42 UTC; 25 posts span Aug 12–13 | ACTIVE |
| r/TrekkingItaly | Reddit | https://www.reddit.com/r/TrekkingItaly/ | 28,526 | Newest Aug 13 2026 15:55 UTC; 25 posts span Aug 05–13 | ACTIVE |
| r/FotografiaItalia | Reddit | https://www.reddit.com/r/FotografiaItalia/ | 12,285 | Newest Aug 13 2026 16:34 UTC; 25 posts span Aug 09–13 | ACTIVE |
| r/specialtyCoffeeItaly | Reddit | https://www.reddit.com/r/specialtyCoffeeItaly/ | 2,100 | Newest Aug 08 2026, but 25 posts reach back to May 07 2026 | DEGRADED |
| r/italymakers | Reddit | https://www.reddit.com/r/italymakers/ | 621 | Newest Jul 30 2026, but 25 posts reach back to Oct 2025 | DEGRADED |
| r/Barbecue_Italia | Reddit | https://www.reddit.com/r/Barbecue_Italia/ | 563 | 25 posts spanning Nov 2022 – May 2024 | DEAD |

---

## (j) Travel / viaggi

| Surface | Platform | URL | Members | Last-activity evidence (2026-08-13) | Verdict |
|---|---|---|---|---|---|
| r/ViaggiITA | Reddit | https://www.reddit.com/r/ViaggiITA/ | 52,574 | Newest Aug 13 2026 16:42 UTC; 25 posts span Aug 10–13 | ACTIVE |
| r/TrekkingItaly | Reddit | https://www.reddit.com/r/TrekkingItaly/ | 28,526 | Newest Aug 13 2026 15:55 UTC; 25 posts span Aug 05–13 | ACTIVE |

**Language traps — critical for this niche:** r/ItalyTravel (147,601) and r/askitaly (102,183) are far larger than r/ViaggiITA but are **English-language communities of foreigners planning trips to Italy**. They are the exact inverse of the target audience. The correct surface is r/ViaggiITA, whose own description is explicit: "Il subreddit per Italiani per parlare di viaggi". It was created only in June 2024 and has already passed 52k members, which suggests the Italian-language travel audience was previously unserved on Reddit.

---

## Health-adjacent surfaces (wellbeing, relationships)

Not one of the ten assigned niches, but these verified active and are relevant to consumer wellbeing apps.

| Surface | Platform | URL | Members | Last-activity evidence (2026-08-13) | Verdict |
|---|---|---|---|---|---|
| r/psicologia | Reddit | https://www.reddit.com/r/psicologia/ | 67,710 | Newest Aug 13 2026 16:56 UTC; 24 posts span Aug 12–13 | ACTIVE |
| r/Relazioni | Reddit | https://www.reddit.com/r/Relazioni/ | 52,428 | Newest Aug 13 2026 10:49 UTC; 25 posts span Jul 21 – Aug 13 | ACTIVE |
| r/Psicologia_Italia | Reddit | https://www.reddit.com/r/Psicologia_Italia/ | 12,445 | Newest Aug 13 2026 16:31 UTC; 25 posts span Jul 29 – Aug 13 | ACTIVE |
| r/adhd_italia | Reddit | https://www.reddit.com/r/adhd_italia/ | 2,199 | Newest Aug 13 2026 16:24 UTC; 24 posts span Aug 03–13 | ACTIVE |

---

## Has Italian consumer discussion moved into private Facebook / Telegram groups?

The brief asks this per niche. The honest answer from fetched evidence is **that it varies sharply by niche, and the claim is only supportable for parenting**. Facebook is walled, so this cannot be answered by measuring Facebook; it is answered by the contrast between what is verifiably alive in the open and what is conspicuously missing.

**Where the "moved to private groups" claim is supported by evidence — parenting (d).** This is the one niche with a real absence in the open: no live Italian-language subreddit, and the surviving forums are visibly hollowed out (GravidanzaOnLine holds 8,055,194 lifetime messages but its parenting sub-forums last posted in 2019 and 2020, while its general chat section still moves). A community that large does not evaporate; the archive-with-a-pulse pattern is what a migration away from open forums looks like. The destination is not directly observable here.

**Where it is not supported — everywhere else.** Finance, fitness, gaming, tech, calcio, giardinaggio, modellismo, travel and student life all have open surfaces posting the same day they were fetched, several of them multiple times per hour. There is no basis for telling a template that Italians in these niches have gone private; they are demonstrably posting in public.

**Telegram specifically.** Public *channels* are verifiable — `t.me/s/<name>` renders a full feed with timestamps — and `t.me/s/fantacalcio` verified ACTIVE (newest 2026-08-12). But Telegram public channels are broadcast, not discussion, so they are a distribution surface rather than a research surface. Telegram *groups*, where discussion would happen, show only a join button with no readable feed: `t.me/s/italiapersonalfinance` returned a bare contact page with zero messages. Two other consumer-deal channels sampled (`offerteshoppingita`, `scontiepromozioni`) are abandoned husks, newest messages 2022 and 2018, with 71 and 8 subscribers. **Telegram is therefore UNVERIFIABLE as a discussion surface and should not be presented in a template as one.**

**Net guidance for the templates:** treat Facebook and Telegram groups as existence-signal only in every niche, and treat parenting as the single niche where a researcher should actively expect the real conversation to be somewhere they cannot fetch.

---

## Italian-language review surfaces

| Surface | URL | Evidence (2026-08-13) | Verdict |
|---|---|---|---|
| Altroconsumo — community "Energia rinnovabile" | https://www.altroconsumo.it/community/energia-rinnovabile | Newest conversation date 2026-08-03 (10 days); 12 dates parsed, 2nd newest 2026-07-24 | ACTIVE |
| Altroconsumo — community index | https://www.altroconsumo.it/community | Loads, lists sub-communities with post counts (Energia rinnovabile 649 post, Casa e condominio 213 post); index itself carries no dates | ACTIVE (via sub-community) |
| Altroconsumo — bacheca dei reclami | https://www.altroconsumo.it/reclamare/bacheca-dei-reclami | Public complaint filings dated 2026-04-07 and 2026-01-24 | ACTIVE |
| Trustpilot Italia | https://it.trustpilot.com/ | HTTP 403 "Verifying Connection" bot wall on both the homepage and a company review page | UNVERIFIABLE |

Altroconsumo is the genuinely useful find here: it is Italy's largest independent consumer organisation (founded 1973, 250,000+ members claimed) and its community carries *complaint-shaped* consumer language — billing disputes, contract changes, refund demands — which is closer to real purchase-intent signal than forum chatter. Its complaints board is public and searchable by company name. Trustpilot IT is almost certainly alive but is bot-walled to unauthenticated fetches, so it cannot be listed as verified; a researcher will need a browser session.

---

## Does not exist publicly (negative-result log)

The absences below are load-bearing: they mean a template must not instruct a researcher to go looking for a surface that is not there.

1. **Italian-language language-learning community (niche f) — no live surface found.** Every large surface in this space is English-language foreigners learning Italian (r/italianlearning 158,494; r/learnitalian 15,674; also r/LearningItalian, r/DuolingoItalian, r/thinkinitalian). The mirror-image community — Italians learning other languages, discussing in Italian — was not found on Reddit, and the candidate names r/ImparareLingue, r/lingue and r/linguaggi could not be resolved (mirror failures, so recorded as UNVERIFIABLE rather than confirmed absent). **Treat this niche as having no verified Italian consumer surface.**

2. **Italian-language parenting subreddit — none exists.** r/mamme has 6 members and 4 posts. r/genitori returned HTTP 403 across six attempts and is UNVERIFIABLE, not confirmed dead. Parenting research must go to the legacy forums (alfemminile is the only ACTIVE one) or accept that the conversation is inside walled groups.

3. **General Italian cooking community — no live Italian-language surface.** r/ricette (259) died in Jan 2020, r/cucinaitaliana has 8 members, r/GustoItalia is DEGRADED. The live food surfaces are either English-language (r/ItalianFood, r/italiancooking, r/mediterraneandiet) or dietary-identity rather than cooking (r/veganita). There is no Italian-language equivalent of a recipes-and-home-cooking community.

4. **Productivity / personal-organisation community — none found.** Niche (e) resolved entirely into *student-life* surfaces (r/Universitaly, r/TeenagersITA, r/polinetwork). No Italian-language community dedicated to productivity methods, note-taking, or time management was located. A productivity-app template should route to the student surfaces or the general subreddits, not to a productivity community.

5. **Dedicated consumer mobile-app discussion surface — none found.** r/AndroidItalia (1,236 members, DEGRADED) is the closest and it is weak. Italians discuss hardware heavily (r/ItalyHardware, Hardware Upgrade forum) but app discussion has no dedicated Italian home; it is diffused across r/italy, r/Italia, r/CasualIT and r/ItalyInformatica.

6. **Fantasy-football, coffee, BBQ and maker verticals are thin or dead outside the leaders.** r/ItalyCalcio (934) dead since Mar 2023, r/Barbecue_Italia (563) dead since May 2024, r/italymakers (621) and r/specialtyCoffeeItaly (2,100) both DEGRADED. Only r/fantacalcio_IT among the smaller hobby subs is genuinely healthy.

7. **Crypto/investing beyond the two leaders is dead.** r/BitcoinItalia (822) last posted Sep 2021; r/ItaliaInvestimenti has 1 member. Finance signal concentrates almost entirely in r/ItaliaPersonalFinance and r/scimmieinborsa.

8. **No niche-specific Italian consumer Discord verified.** The Discord invite API returns live member and presence counts without authentication, so this is a verifiable surface in principle. In practice the plausible niche invite codes tested (`italy`, `fantacalcio`) returned "Unknown Invite" (expired), and the only Italian server that resolved is general-purpose with an anti-immigrant slur in its name — excluded deliberately rather than routed into a template. Discord should not be presented as a research surface for any of these niches without first finding a live, on-niche invite.

9. **Not confirmed absent, but unfetchable (do not record as dead).** Tom's Hardware Italia forum (HTTP 403), Trustpilot Italia (HTTP 403), all Facebook groups (HTTP 400 wall), all Telegram groups as opposed to channels (no public feed), and the subreddits r/genitori, r/Genitorialita, r/ImparareLingue, r/lingue, r/linguaggi, r/scuola, r/Studiare, r/LiceoITA, r/ItaliaGenitori, r/Finanzapersonale (mirror failures after retries).

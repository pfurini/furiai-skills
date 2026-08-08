# Market pack — Italy

Parameters and legal specifics for naming a brand aimed at the Italian market. Everything here plugs into the funnel in `references/verification.md`.

## Language

Conduct the whole engagement in Italian — questions, strategy brief, tables, recommendation, clearance log — even though this skill and its references are written in English, and regardless of any session-level or global language default. Only an explicit user request switches the output language. Naming directions should include native Italian roots and compounds; an Italian-language name is itself a differentiator in categories where competitors default to English.

## Funnel parameters

- **TLD set**: `it,com,eu` (`.it` is the primary TLD: REGISTERED there kills).
- **Trademark offices**: `IT,EM,WO` — Italian national marks (UIBM), EU marks (EUIPO), and WIPO international registrations, all via the TMview endpoint the script wraps.
- **App Store country**: `it`.

## Company registry — Registro Imprese

The authoritative source for company-name conflicts. The free portal search (registroimprese.it) is protected by invisible reCAPTCHA that defeats scripted and headless-browser access — do not burn time trying.

- **Manual (default)**: the user searches the name in the box at registroimprese.it — under a minute. Record as PENDING with this instruction.
- **Preliminary screen (do it yourself)**: unofficial mirrors of company data (ufficiocamerale.it, reportaziende.it) are captcha-free and web-searchable. A hit there is a real TAKEN/FLAG finding; a clean result upgrades confidence but the item stays PENDING — only the official register is authoritative.
- **Automated (credential-gated)**: OpenAPI (openapi.com, Italian provider, formerly openapi.it) exposes company search and visure via REST — public per-call pricing, credit wallet, sandbox. If `OPENAPI_IT_TOKEN` is set, query the company-search endpoint per their current docs (verify the endpoint shape at docs.openapi.com before first use; it has not been exercised from this skill). Otherwise record PENDING and mention the service.

## Legal specifics (feed tier 0 and the recommendation)

- **Art. 2564 Codice Civile**: a company name must differ from existing ones in the same sector and place — that is why same-sector Registro Imprese hits are TAKEN, not FLAG.
- **Preuso**: unregistered marks in prior use retain rights in Italy. The live-usage sweep is a legal necessity, not diligence theater.
- **Regulated words** that require authorization or are reserved in company names: *banca, credito, assicurazioni, farmacia, poste, olimpico/olimpiade, università, made in Italy* claims — a candidate containing one is dead at tier 0 unless the user holds the authorization.
- **Geographic indications**: for food, wine, and spirits brands, names evoking DOP/IGP/DOC terms are blocked even without exact match (check eAmbrosia, the EU GI register, manually — PENDING item for food/bev briefs).
- **Dialects**: screen tier-0 meanings against major dialect areas (Neapolitan, Sicilian, Venetian, Lombard, Roman) — a word innocuous in standard Italian can be vulgar regionally.
- **Similarity clearance before filing**: the UIBM/EUIPO similarity search (phonetic, visual, conceptual, per class) is consultant work. Always the last PENDING item; the variant sweep is only a proxy for it.

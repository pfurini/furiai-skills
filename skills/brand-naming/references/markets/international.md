# Market pack — international / other markets

Fallback parameters when the brand targets markets without a dedicated pack. When a market recurs, promote what you learn into its own `references/markets/<market>.md` shaped like `italy.md`.

## Language

Work in the language of the engagement; generate names that survive pronunciation in every target market's language (tier-0 screen in each).

## Funnel parameters

- **TLD set**: `com` primary, plus `net,org` and the ccTLD of each target market (`de`, `fr`, `es`, ...). `check_domains.py` resolves uncommon TLDs through the IANA RDAP bootstrap; UNKNOWN means the ccTLD registry has neither RDAP nor a wired whois pattern — record PENDING with the registry's own lookup URL.
- **Trademark offices**: start from `EM,WO` and add the national office codes of each target market (TMview aggregates ~70 national registers; the live office list is on tmview.org). For markets TMview does not cover, the national register is a PENDING manual check — for the US, USPTO search at tmsearch.uspto.gov.
- **App Store country**: `us`, plus each major target storefront.

## Company registries

No single authority exists. OpenCorporates (opencorporates.com) aggregates registries worldwide — free web search, API with a free tier (credential-gated: `OPENCORPORATES_API_TOKEN`, endpoint per their docs; unexercised from this skill). National registries stay PENDING items per market: Companies House (UK) and the Handelsregister (DE) have free search, US names are per-state (Secretary of State sites).

## Legal specifics

- **Common-law jurisdictions** (US, UK, IE, AU...): unregistered use confers trademark rights, so the live-usage sweep carries the same legal weight as a register search.
- **US federal + state layering**: USPTO covers federal marks only; state registrations and common-law use are separate layers. Flag this in the pending list for any US-facing brand.
- **Madrid system**: a WIPO (WO office) hit can designate protection in any member country — treat a WO EXACT hit as overlapping every target market until the designation list says otherwise.

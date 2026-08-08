# Uniqueness Verification

The gate: a name earns a green check only when **no automated check found it existing anywhere** and every non-automatable dimension is explicitly listed as pending. A Top 5 must contain only gated names — presenting a name that later dies at a registry wastes the client's decision.

All scripts live in `scripts/` (stdlib-only Python, run with `python3`). They report; they never gate by exit code — you apply the verdicts. Market parameters (TLD set, trademark offices, registry procedure, language) come from the market file chosen in Step 1.

## Contents

- The funnel (tiers 0-3)
- Verdict vocabulary and kill rules
- Variant sweep (similarity proxy)
- Live-usage sweep
- Credential-gated checks
- False-positive discipline
- The clearance log

## The funnel

Order by cost: judgment screens are free, domain checks are cheap, everything else runs only on survivors. A name that dies at whois must never consume a trademark query.

**Tier 0 — during generation (judgment, no tools).** Screen every candidate as you coin it:

- Regulated or protected words in the target market (see the market file's list) — using one makes the company name unregistrable.
- Negative or comic meanings in the market's language *and its dialects*, plus major EU languages for an EU-facing brand.
- Cultural, historical, or political echoes (a compound can inherit the register of its pattern — Italian *dopo-* compounds carry a welfare-era echo; surface this in the evaluation, don't silently kill).
- Collision with a notable surname, person, place, or fictional entity.
- SEO ownability: a common word or news-frequent verb can never be owned in search results.

**Tier 1 — all candidates (domains).** Run once for the full candidate list:

```
python3 scripts/check_domains.py NAME1 NAME2 ... --tlds <market TLD set>
```

A candidate REGISTERED on the market's primary TLD is dead — record it with the reason and move on. UNKNOWN goes to the pending list, not to the kill list.

**Tier 2 — finalists only (typically 4-6 survivors).**

```
python3 scripts/check_trademarks.py FINALISTS... --offices <market offices> --classes <Nice classes from the strategy brief>
python3 scripts/check_handles.py FINALISTS...
python3 scripts/check_appstores.py FINALISTS... --country <market>   # only if the brand ships an app or dev tool
```

Plus the variant sweep and live-usage sweep below.

**Tier 3 — credential-gated and manual closeout.** Company registry (see the market file), the VERIFY MANUALLY handle links, and the items that are never automatable: the consultant-grade phonetic/conceptual trademark similarity search before filing, and spoken tests with humans. These go on the pending list of the final checklist, each with its one-line manual procedure.

## Verdict vocabulary and kill rules

Use exactly these verdicts in tables and the clearance log:

- **FREE** — a definitive negative from the authoritative source (registry 404, whois AVAILABLE, 0 TMview results).
- **TAKEN** — definitive positive. Kills the name when it is: primary-TLD domain, or an EXACT trademark hit whose Nice classes overlap the brand's (script marks these OVERLAP), or a same-sector company in the market registry.
- **FLAG** — exists but doesn't auto-kill: exact trademark in distant classes, NEAR trademark hits, a taken secondary handle, a variant hit. Flags surface in the evaluation table's Risk column and the recommendation weighs them.
- **PENDING** — not automatable or UNKNOWN from a script; listed in the final checklist with the manual procedure.

## Variant sweep (similarity proxy)

Exact-word search misses what actually blocks trademarks: similar marks. Approximate a similarity search by generating 3-6 plausible variants per finalist — consonant doubling/undoubling, s/z and c/k swaps, vowel-ending changes, hyphen/space splits, obvious transliterations (Approdia → Aprodia, Aprodya; Dopocorso → Dopo Corso, Dopocorsa) — and run `check_domains.py` and `check_trademarks.py` on the variants too. A variant hit is a FLAG (similarity risk to weigh and disclose), never an automatic kill. Say clearly in the output that this is a proxy, not the consultant search.

## Live-usage sweep

Registered rights are only half the risk; unregistered use carries legal weight too (prior use / *preuso* in Italy, common law elsewhere). For each finalist:

1. Web-search the name alone, plus the name with the category and with the market's country. You are looking for any company, product, project, venue, or person operating under it.
2. Query certificate transparency for live but unindexed deployments: `https://crt.sh/?q=NAME&output=json` (free; slow and occasionally down — on timeout, record PENDING rather than retrying forever).
3. If the brand sells physical products, search the name on the market's Amazon storefront (manual link; bot walls block scripted checks).

Findings in the same or adjacent sector are TAKEN; distant-sector findings are FLAGs.

## Credential-gated checks

When a check needs an account or paid credits, look for the credential named in the market file (environment variable). Present → run the documented call and record the result. Absent → record PENDING with the manual procedure and the service that would automate it; never block the workflow on account creation.

## False-positive discipline

Only a definitive negative from the authoritative source counts as FREE. Aggregator tools (Sherlock, name-checker sites) report false positives; anything they claim free must be re-verified against the platform directly before it enters a table. Platforms behind login or JS walls (Instagram, TikTok, X, LinkedIn) are structurally unverifiable from a script — they are always PENDING with the URL to open, even when a tool claims otherwise. Do web-search the handle on those platforms anyway: a public hit (a live account, a page indexed by search engines) is positive evidence worth attaching to the PENDING item — an existing dormant account changes what the user does at that URL. Absence of search hits still proves nothing.

## The clearance log

Verification that isn't recorded evaporates. After tier 2, write `naming-clearance-<date>.md` in the working directory: one row per name x dimension with the verdict, the source (tool/endpoint/URL), and the timestamp. The final checklist in your reply links to this file. This is the record a consultant or lawyer will ask for when filing.

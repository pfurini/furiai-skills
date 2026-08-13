# LinkedIn groups — post-volume verification (closes the open item)

Date: 2026-08-13. Source: Phase C forward-test Run 1 (niche: client document
collection for studi commercialisti), `trend-linkedin` researcher, direct
cookieless Apify scrape.

**Question** (from the Phase B research pass): do Italian professional
LinkedIn groups show real post volume, or are they member-count shells?

**Answer: real but general-purpose.** The largest sampled commercialisti
group (16,370 members) shows genuine, dated post volume — 37 posts across
Sep 2025–Aug 2026, directly observed, not estimated. However, zero posts
concerned the run's specific pain (document collection), while vendor and
hiring signals for that same pain were strong elsewhere on LinkedIn.

**Implication for the prompts/packs** (already reflected in
`prompts/b2b/linkedin.md`'s framing, kept as-is): treat Italian professional
LinkedIn groups as a *live but low-resolution* surface — good for
existence/vocabulary signal and recruiting-by-engagement, not a
voice-of-customer complaint mine. Pain-specific demand evidence on LinkedIn
comes from vendor activity and job postings, not group discussion.

**Operational note:** the LinkedIn *jobs* actor failed/timed out three times
in this session; job-posting evidence had to come from web search over
aggregator sites instead. The group-posts actor worked. Consider noting an
alternate jobs actor (or the aggregator fallback) in `references/tooling.md`
if the failure repeats in Run 2.

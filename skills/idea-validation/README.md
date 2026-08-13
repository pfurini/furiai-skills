# Idea Validation Skill Pack

### *To Build or Not to Build — that is the question this answers.*

A skill pack that turns Claude Code into a personal venture analyst for indie builders — from idea brainstorming to full validation, market research, and pivot analysis. Covers two targets with dedicated calibration: **consumer apps (B2C)** and **self-serve B2B micro-SaaS** (credit-card signup, no sales team — marketplace apps, dev tools, vertical SMB tools). Validate in 10 minutes instead of regretting in six months.

## Who Is This For?

- **Indie app developers** who want to validate app ideas before building
- **Micro-SaaS builders** targeting merchants, agencies, and other small-business operators with self-serve tools
- **Solo founders** exploring startup ideas and looking for a data-driven brainstorming partner
- **Side-project builders** deciding where to invest their limited time
- **Aspiring developers** with no idea yet who want to discover one worth building
- **Anyone** tired of building things nobody wants

Explicitly out of scope: sales-led enterprise SaaS (procurement, demos, custom contracts) — that segment is validated through customer-discovery interviews, which desk research can't replace. The agent says so when an idea drifts there.

## Installation Scope

Install this skill **per project**, not globally at the user level. All analysis is written to a `.idea-validation/` folder in the project root, so the skill and the data it produces stay scoped to the project you run it in. A global install would scatter validation state across unrelated projects.

## How It Works

One orchestrator skill drives eleven specialist subagents that communicate only through files:

- **`idea-validation`** (this skill) is the entry point. It fires on natural requests — "validate my idea", "what should I build?", "tell me about the journaling market", "should I pivot?" — detects your intent, and routes to the right workflow. You can also ask for a **single dimension** ("who are the competitors of X?") without a full workflow.
- **Specialist agents** (`agents/iv-*.md`) each analyze one dimension and write one artifact into `.idea-validation/`. Independent dimensions run **in parallel waves**: five platform researchers sweep the target's evidence surfaces simultaneously (B2C: TikTok, Reddit, App Store, Google, X; B2B: G2/Capterra, operator communities, LinkedIn, Google, X); then competitors, demand drivers, and distribution analyze concurrently; then pricing and retention; then unit economics. Each agent runs with a clean context containing only its rubrics and inputs, on a model tier matched to its dimension (see `agents/README.md`).
- **Per-target calibration packs** (`references/calibration/b2c/` and `b2b/`) hold the benchmark tables — churn bands, channel CACs, WTP ranges, capture rates — while the agents hold only the mechanisms. Each idea carries a `target: b2c | b2b` field that selects the pack set; the artifact schemas are identical for both targets. B2B gating numbers are web-sourced with citations; construct tables are flagged `confidence: low` pending a source-hardening pass (raw research in `research/idea-validation-b2b-benchmarks/`).
- **The conversational and synthesis steps stay on the main thread**: the founder interview, segmentation, the 0–100 scoring, and the decision memo (`references/*.md`) — so the math stays auditable and the verdict draws on the full conversation.

The agent files are built for pi-subagents custom agent types but degrade gracefully: harnesses without them (e.g. Claude Code) dispatch generic subagents carrying the agent body as their brief, and with no subagents at all the orchestrator runs the same briefs inline. Specialists never call each other; the orchestrator reads each wave's outputs and feeds the next. Conversation history is not the store — `.idea-validation/` is, so nothing is lost between sessions.

## Workflows — 4 Ways to Use the Agent

### 💡 Idea Generation — *"I don't know what to build"* · `~10–15 min`

The agent interviews you about your background, skills, and interests — then researches what's actually trending — and generates 5–10 screened app ideas matched specifically to you.

```
I don't have an app idea yet. Help me find one.
What should I build? I'm a fitness coach with 8k Instagram followers.
I want to find an app idea in the productivity space.
```

**Steps:** background interview → ICP segmentation (beginner/builder/growth tier) → trend research (parallel per platform) → trend-to-product mapping → screening scores

**Methodology:** Trend signals are pulled from TikTok Creative Center (hashtag velocity), Reddit (community pain language), X/Twitter (public builder and buyer conversations), App Store (new entrants + review patterns), and Google Trends (search demand). Ideas are filtered against your domain expertise, skills, and distribution advantages from the interview — so you get ideas you can actually build and sell.

**Output:** Ranked candidates in `.idea-validation/ideas/<slug>/`, each with an `idea.md` and a `screening_scores.json` (screening ranks trend evidence — it is not a validation).

> Don't want to answer questions? Say **"browse topics"** to pick from a list of product domains, or **"skip"** to jump straight to ideas.

### 🔍 Idea Validation — *"Is my idea worth building?"* · `~10–15 min`

Full validation across every dimension, scored, weighted, and combined into a final verdict — with the single riskiest assumption identified and a concrete experiment to test it before writing any code.

```
Validate my idea: an AI tool that rewrites your emails to sound more professional.
I want to build a habit tracker for intermittent fasting. Worth it?
Score this — a subscription app that sends meal plans based on your grocery budget.
```

**Waves:** trend research (all platforms in parallel) → competitors ∥ desire ∥ distribution → pricing ∥ retention → CAC modeling → final score (0–100) → decision memo

**Methodology:**
- **Scoring** uses a multiplicative-floor algorithm — one catastrophic weakness kills the overall score, just like in a real startup — plus a missing-input discount, so partially analyzed ideas can never reach the "pursue" tier
- **Pricing** is estimated via Van Westendorp price sensitivity analysis + desire-premium multipliers (primal desires like survival command a 1.3–1.8× price premium; mild curiosity commands none)
- **Distribution** models viral coefficient (k-factor) by loop type, ASO opportunity via a 5-factor rubric, creator economy fit, paid feasibility, and founder edge
- **Competitors** are analyzed via systematic App Store search + 1-star/3-star review mining to surface the exact gaps incumbents leave open
- **Riskiest Assumption Test (RAT)** designs a ≤2-week, ≤$100 behavioral experiment to validate the single assumption most likely to kill the idea
- **Pre-mortem** (Klein, 2007) imagines the idea failing in 12 months and traces the most probable causes back to scored weaknesses
- **On the B2B target**, the same machinery runs with swapped calibration: pain/ROI demand drivers instead of desires, workflow-embedding retention with churn-by-price-band benchmarks, marketplace-listing opportunity instead of ASO, G2/Capterra review mining instead of the App Store, and SOM estimates reality-checked against Stripe-verified indie revenue cohorts

**Verdict bands:** 75–100 **pursue** · 55–74 **test** (run the RAT first) · 35–54 **pivot** · 0–34 **drop**

**Output:** `.idea-validation/ideas/<slug>/decision_memo.md` — verdict, strengths, risks, RAT experiment, kill criteria, and your next step

### 📊 Market Deep Dive — *"Tell me about this market"* · `~10–15 min`

Research a category before committing to any idea. Understand who already owns it, what users hate, and whether the timing is right.

```
Tell me about the journaling app market.
What's happening in the AI language learning space?
Is the meditation app market still worth entering?
```

**Waves:** trend research (all platforms in parallel) → competitor landscape ∥ distribution channel assessment → market size (TAM/SAM/SOM)

**Methodology:**
- Trend velocity scored across platforms: rising-fast / rising / stable / declining
- X/Twitter analysis separates public demand signals from viral noise, then corroborates them against pricing, competitors, and cross-platform evidence
- Market saturation rated via a 5-factor rubric (competitor count, incumbent dominance, funding activity, keyword saturation, content saturation)
- Market size uses triangulated bottom-up estimation: search volume × intent conversion rate, community size × platform multiplier, and competitor revenue proxies — cross-checked for consistency
- SOM estimates use indie-realistic capture rate benchmarks by app category (e.g. niche productivity: 0.5–2.0% year 1)

**Output:** Dated per-platform trend files in `.idea-validation/market_insights/` plus `competitors.json`, `market_size.json`, and `distribution.json` under a `market-` research slug

### 🔄 Pivot Optimization — *"My idea scored low. Now what?"* · `~10–15 min`

Finds the best version of a failing idea instead of abandoning it entirely. Each pivot option changes exactly 1–2 variables — audience, niche, pricing model, or feature emphasis — with a projected score improvement before you commit. Requires a fully validated idea (`scores.json` from the validation workflow — a screening score does not qualify).

```
My idea scored 34/100. Should I pivot?
The validation said to pivot. What are my best options?
This isn't working — what should I change about my fitness app idea?
```

**Steps:** re-read scores → weakness root cause analysis → pivot options with projected scores → re-score recommended pivot

**Methodology:**
- Weaknesses are classified by root cause: structural (can't fix), situational (fixable with time/budget), knowledge-gap (needs more research), or addressable (clear fix exists) — only the latter two generate pivot options
- Each pivot must pass the **Same Idea Test**: changes 1–2 variables, preserves at least one strong dimension, and has evidence from market insights or competitor review mining
- Scoring simulation projects how each dimension shifts before full re-scoring
- Effort is estimated and adjusted for founder tier — what's "medium" for a builder is "high" for a beginner

**Output:** `pivot_options.json` + `pivot_report.md` with ranked pivots and effort estimates, and `pivot_scores.json` with the projected score of the recommended variant

## What Gets Saved

All outputs persist in `.idea-validation/` at the project root, between sessions.

```
.idea-validation/
├── user_profile.md                   ← your builder profile (reused across sessions)
├── market_insights/
│   └── fitness-tiktok-2026-04.md     ← dated trend file per niche + platform (append-only)
└── ideas/
    └── habit-tracker-climbers/
        ├── idea.md                   ← concept + lifecycle status (candidate → scored → active/dropped)
        ├── screening_scores.json
        ├── competitors.json
        ├── desire_scores.json
        ├── pricing.json
        ├── distribution.json
        ├── retention.json
        ├── cac.json
        ├── market_size.json
        ├── scores.json
        ├── weaknesses.json
        ├── pivot_options.json
        ├── pivot_report.md
        ├── pivot_scores.json
        └── decision_memo.md          ← the final verdict
```

Idea directories are never deleted — abandoned ideas are marked `status: dropped` in `idea.md`. Trend files carry a freshness window; before re-researching a niche, the agent offers to reuse a still-fresh file or write a new dated one.

## Component Index

**Specialist agents** (`agents/` — parallel, one artifact each):

| Agent | Role | Writes |
|---|---|---|
| `iv-trend-researcher` | One-platform trend research (dispatched per platform) | `market_insights/<niche>-<platform>-<YYYY>-<MM>.md` |
| `iv-idea-mapper` | Trends → concrete idea candidates | `ideas/<slug>/idea.md` |
| `iv-competitor-mapper` | Competitor map + review mining + saturation | `competitors.json` |
| `iv-desire-evaluator` | Scores the five core desire drivers | `desire_scores.json` |
| `iv-pricing-wtp` | Willingness to pay + pricing model | `pricing.json` |
| `iv-distribution` | Viral loops, ASO, creator fit, paid, founder edge | `distribution.json` |
| `iv-retention` | Retention/churn risk from habit mechanics | `retention.json` |
| `iv-cac-modeler` | LTV, per-channel CAC, payback, viability | `cac.json` |
| `iv-market-sizer` | TAM / SAM / indie-realistic SOM | `market_size.json` |
| `iv-weakness` | Root causes of low-scoring dimensions | `weaknesses.json` |
| `iv-pivot-engine` | Evidence-backed pivot options | `pivot_options.json` + `pivot_report.md` |

**Main-thread steps** (`references/` — conversational or synthesis):

| Reference | Role | Writes |
|---|---|---|
| `interview.md` | Founder interview (full / fast / browse / skip) | `user_profile.md` |
| `segmentation.md` | Derives ICP tier + constraints | `user_profile.md` (merge) |
| `scoring.md` | 0–100 score + verdict (full, screening, or pivot re-score) | `scores.json` / `screening_scores.json` / `pivot_scores.json` |
| `decision-memo.md` | Final brief: verdict, RAT, pre-mortem, kill criteria | `decision_memo.md` |

*Validate in 10 minutes. Build with confidence.*

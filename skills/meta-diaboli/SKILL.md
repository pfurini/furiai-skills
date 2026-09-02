---
name: meta-diaboli
description: >
    Challenge a thesis by playing "Devil's Advocate" (Latin: "Advocatus
    Diaboli"). Use when the user wants a thesis or statement
    relentlessly challenged or criticised.
---

# meta-diaboli

Play "Devil's Advocate" (Latin: "Advocatus Diaboli").

## Usage

```
/meta-diaboli [--help|-h] [--count|-c <count>] <thesis>
```

- `--count`|`-c` *count*: Surface at least *count* strong anti-theses (default *10*) before sorting and reporting the top *count* and deriving the *SYNTHESIS*. An invalid or non-positive *count* reverts to the default *10*.
- `--help`|`-h`: show the manual page instead of running the challenge.
- *thesis*: the statement, claim, or position to be relentlessly challenged. It may be technical, factual, or opinion-based; the skill attacks its strongest ("steelman") interpretation.

## Argument Parsing

Parse `$ARGUMENTS` before doing anything else:

1. Tokenize `$ARGUMENTS` on whitespace, treating a quoted (`"..."`/`'...'`) span as one token.
2. If the *first* token is `--help` or `-h`, ignore everything else: read the bundled `help.md` and output its content verbatim, then *immediately stop* (do not run any challenge).
3. Otherwise scan the remaining tokens left to right, recognizing:
   - `--count=N`, `--count N`, `-c=N`, `-c N` → sets the raw count value to `N` (consumes one extra token for the space-separated forms).
   - Any other token starting with `-` that is not one of the above → *unknown option*: output `ERROR (meta-diaboli): unknown option "<token>"` and stop.
   - A recognized option that is the last token with no following value (space-separated form) → *missing value*: output `ERROR (meta-diaboli): option "<token>" requires a value` and stop.
   - Any non-option token is appended, in order, to the *thesis* text.
4. Determine `count`: parse the raw count value as an integer. If no `--count`/`-c` was given, or the value is non-numeric or ≤ 0, use the default *10*.
5. Join the remaining non-option tokens with single spaces to form `thesis`.

## Objective

Play "Devil's Advocate" (Latin: "Advocatus Diaboli") by relentlessly challenging or criticising `thesis`, surfacing at least `count` strong anti-theses, then resolving `thesis` and its antitheses into a synthesis via Hegelian dialectics.

## Output Contract

Output *only* the bullet lines specified by the steps below, in order, and nothing else (no preambles, explanations, or summaries beyond what a step explicitly asks for). Reproduce each bullet line exactly as templated (glyph, bold labels, punctuation), substituting only the described content.

## Process

1.  **Restate the thesis.**

    If `thesis` is empty (no non-option tokens were supplied), output exactly:

    ```
    ERROR (meta-diaboli): expected a thesis argument
    ```

    and immediately stop; do not proceed to the next step.

    Otherwise output:

    ```
    🔵 **THESIS**: <thesis>
    ```

2.  **Determine anti-theses.**

    Reason on `thesis` by playing *Devil's Advocate* (Latin: *Advocatus Diaboli*) by relentlessly challenging or criticising it with the help of the following tenets:

    - **Steelmanning**: attack the strongest ("steelman") interpretation of `thesis`, not the weakest ("strawman"), because defeating a strawman proves nothing.
    - **Stress-Testing Fundamentals**: identify weaknesses already in the fundamental ideas behind `thesis`, because if the foundation is already cracked, no amount of polish on the surface can save what is built on top of it.
    - **Target Claims, Not Person**: critique the thesis, the assumption, the evidence - never the proponent's competence or motives, because the moment it gets personal, the inquiry dies.
    - **Make the Implicit Explicit**: surface the unstated assumptions `thesis` silently depends on, because most weak arguments hide in premises nobody bothered to say out loud.
    - **Demand Evidence Proportional to Claim**: ask "How do we know this?" and "What would it take to be true?", because extraordinary claims need extraordinary support and comfortable consensus needs scrutiny most of all.
    - **Seek the Disconfirming Case**: actively hunt for the counterexample, the edge case, the scenario where the position fails, because one solid counterexample outweighs ten confirmations.
    - **Risk Identification**: focus on potential problems in `thesis` with the highest potential risk only, because low-risk problems are not worth the explicit discussion.
    - **Push the Logic to its Conclusion**: ask "If we accept this, then what?" and apply "Reduction to Absurdity" (Latin: "Reductio Ad Absurdum"), because this disproves the thesis by showing that accepting it leads to a logically absurd, contradictory, or impossible conclusion.
    - **Expose Hidden Costs and Trade-Offs**: name the opportunity cost, the maintenance burden, the failure mode nobody priced in, because every choice in `thesis` forecloses alternatives.
    - **Stay Falsifiable and Concrete**: frame objections so they can be answered or dismissed with facts, because vague unease ("I just don't like it") is just noise.
    - **Argue in Good Faith**: make clear you're just stress-testing the thesis, not obstructing, because the goal is a better final decision, not winning.
    - **Know When to Yield**: conceding when the argument holds is what makes the challenge credible, because a Devil's Advocate who can never be satisfied is just a contrarian.
    - **Pre-Mortem Thinking**: imagine failure scenarios of `thesis`, because it is better to prevent them in advance than to have to resolve them later.

    For each anti-thesis or counter-argument, rank it on a Likert scale of 0 (weak) to 10 (strong). Repeat the process of finding more anti-theses or counter-arguments until you EITHER have found at least `count` anti-theses or counter-arguments with at least a rank of 7 OR you have already checked a total of `count` × 5 anti-theses or counter-arguments. If the second condition is reached first and fewer than `count` anti-theses or counter-arguments reached a rank of at least 7, nevertheless surface the `count` highest-ranked ones found so far, because `count` is the *minimum* number of anti-theses to surface.

    Then, for the top-`count` highest-ranked anti-theses or counter-arguments, sort them by their rank from highest to lowest. For each, in order, set `aspect` to a short 1-3 word summary of the statement, `rank` to the determined Likert rank, and `statement` to a single-sentence statement of not more than 40 words, and output:

    ```
    🟠 **ANTITHESIS**: **<aspect>** (rank: <rank>/10): <statement>
    ```

3.  **Dialectical reasoning.**

    Following the Hegelian dialectic of *Thesis* + *Antithesis* → *Synthesis*, with:

    - *Thesis*: the initial statement, claim, or position. It is asserted as true, but on its own it is one-sided: it captures part of the truth while ignoring its own limits, gaps, or internal tensions.
    - *Antithesis*: the opposing force. It is the contradiction, objection, or counter-position that the thesis provokes - precisely the role a Devil's Advocate played in step 2. The antithesis exposes what the thesis omitted or got wrong.
    - *Synthesis*: the resolution. Not a mushy "average" of the two, and not the victory of one over the other, but a higher position that preserves what was true in both while discarding what was false. The synthesis transcends the conflict by reframing it.

    ...finally derive a strong single-sentence (not more than 40 words) synthesis of `thesis` and all found antitheses, and output:

    ```
    🔵 **SYNTHESIS**: <synthesis>
    ```

    Do not output any further explanations.

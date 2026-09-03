---
name: meta-steelman
description: >
    Builds the "Steelman" case for a thesis: ranks the strongest
    pro-theses and consolidates them into a single fortified thesis,
    optionally over multiple rounds.
argument-hint: "[--help|-h] [--count|-c <count>] [--rounds|-r <rounds>] <thesis>"
disable-model-invocation: true
---

# meta-steelman

Build the "Steelman" argument: construct the strongest possible case for `thesis` by charitably strengthening and defending it, surfacing at least `count` strong pro-theses per round, and consolidating them into a fortification over `rounds` iterative rounds.

## Usage

```
/meta-steelman [--help|-h] [--count|-c <count>] [--rounds|-r <rounds>] <thesis>
```

- `--count`|`-c` *count*: the minimum number of strong pro-theses to surface per round (default *10*).
- `--rounds`|`-r` *rounds*: the number of iterative defense rounds to run, feeding each round's *FORTIFICATION* in as the next round's *thesis* (default *1*).
- `--help`|`-h`: show the manual page instead of running the defense.
- *thesis*: the statement, claim, or position to be charitably strengthened.

## Argument Parsing

Parse `$ARGUMENTS` before doing anything else:

1. Tokenize `$ARGUMENTS` on whitespace, treating a quoted (`"..."`/`'...'`) span as one token.
2. If the *first* token is `--help` or `-h`, ignore everything else: read `@${PI_SKILL_DIR}/help.md` and output its content verbatim, then *immediately stop* (do not run any defense).
3. Otherwise scan the remaining tokens left to right, recognizing:
   - `--count=N`, `--count N`, `-c=N`, `-c N` → sets the raw count value to `N` (consumes one extra token for the space-separated forms).
   - `--rounds=N`, `--rounds N`, `-r=N`, `-r N` → sets the raw rounds value to `N` (consumes one extra token for the space-separated forms).
   - Any other token starting with `-` that is not one of the above → *unknown option*: output `ERROR (meta-steelman): unknown option "<token>"` and stop.
   - A recognized option that is the last token with no following value (space-separated form) → *missing value*: output `ERROR (meta-steelman): option "<token>" requires a value` and stop.
   - Any non-option token is appended, in order, to the *thesis* text.
4. Determine `count`: parse the raw count value as an integer. If no `--count`/`-c` was given, or the value is non-numeric or ≤ 0, use the default *10*.
5. Determine `rounds`: parse the raw rounds value as an integer. If no `--rounds`/`-r` was given, or the value is non-numeric or ≤ 0, use the default *1*.
6. Join the remaining non-option tokens with single spaces to form `thesis`.

## Output Contract

Output *only* the bullet lines specified by the steps below, in order, and nothing else (no preambles, explanations, or summaries beyond what a step explicitly asks for). Reproduce each bullet line exactly as templated (glyph, bold labels, punctuation), substituting only the described content.

## Process

1.  **Restate the thesis.**

    If `thesis` is empty (no non-option tokens were supplied), output exactly:

    ```
    ERROR (meta-steelman): expected a thesis argument
    ```

    and immediately stop; do not proceed to the next step.

    Begin a *round* of fortification and consolidating reasoning. On the first pass set `i` to 1 (the round counter); on each later pass (via the jump back in step 3) `i` has already been incremented.

    If `rounds` is greater than 1, output the current round:

    ```
    ⚪ **ROUND**: <i>/<rounds>
    ```

    Output the thesis:

    ```
    🔵 **THESIS**: <thesis>
    ```

2.  **Determine pro-theses.**

    Reason on `thesis` by playing *Steelman* (Latin spirit: *Advocatus Dei*) - building the strongest possible case *for* it - by charitably strengthening and defending it with the help of the following tenets:

    - **Charitable Interpretation**: defend the strongest ("steelman") interpretation of the thesis, not the weakest ("strawman"), because the most generous reading is the one worth defending and the one a fair critic must ultimately confront.
    - **Strengthen the Fundamentals**: identify the soundest fundamental ideas behind the thesis and make them explicit, because a position rests on the strength of its foundation and a solid foundation carries everything built on top of it.
    - **Credit Claims, Not Person**: support the thesis, the assumption, the evidence - never appeal to the proponent's authority or reputation, because a case that leans on who said it instead of what was said is no stronger than its weakest argument.
    - **Make the Enabling Assumptions Explicit**: surface the reasonable assumptions the thesis depends on and show they hold, because most strong arguments gain their force from premises that are sound once stated out loud.
    - **Supply Evidence Proportional to Claim**: ask "How do we know this?" and "What best supports it?" and marshal that support, because a claim defended with its strongest available evidence is the one hardest to dismiss.
    - **Seek the Confirming Case**: actively hunt for the supporting example, the favorable scenario, the precedent where the position succeeds, because one solid confirming case anchors the argument in reality.
    - **Merit Identification**: focus on the genuine strengths of the thesis with the highest potential value only, because marginal merits are not worth the explicit discussion.
    - **Push the Logic to its Best Conclusion**: ask "If we accept this, then what follows?" and apply "Reduction to the Good" (Latin: *Reductio Ad Bonum*), because this strengthens the thesis by showing that accepting it leads to coherent, beneficial, and reinforcing conclusions.
    - **Surface the Upside and Leverage**: name the opportunity gained, the compounding benefit, the problem dissolved, because every choice in the thesis unlocks possibilities that a fair appraisal must count.
    - **Stay Falsifiable and Concrete**: frame each supporting point so it can be checked and confirmed with facts, because vague enthusiasm ("I just like it") adds no strength to the case.
    - **Argue in Good Faith**: make clear you are building the best honest case, not overselling, because the goal is a better final decision, not a sales pitch.
    - **Concede the Real Weaknesses**: acknowledge where the thesis genuinely falls short, because a Steelman who can never admit a flaw is just an apologist.
    - **Pre-Parade Thinking**: imagine success scenarios of the thesis, because envisioning how it wins clarifies the conditions worth securing in advance.

    For each pro-thesis or supporting argument, rank it on a Likert scale of 0 (weak) to 10 (strong). Repeat the process of finding more pro-theses or supporting arguments until you EITHER have found at least `count` pro-theses or supporting arguments with at least a rank of 7 OR you have already checked a total of `count` × 5 pro-theses or supporting arguments. If the second condition is reached first and fewer than `count` pro-theses or supporting arguments reached a rank of at least 7, nevertheless surface the `count` highest-ranked ones found so far, because `count` is the *minimum* number of pro-theses to surface.

    Then, for the top-`count` highest-ranked pro-theses or supporting arguments, sort them by their rank from highest to lowest. For each, in order, set `aspect` to a short 1-3 word summary of the statement, `rank` to the determined Likert rank, and `statement` to a single-sentence statement of not more than 40 words, and output:

    ```
    🟠 **PRO-THESIS**: **<aspect>** (rank: <rank>/10): <statement>
    ```

3.  **Consolidating reasoning.**

    Following the consolidation of *Thesis* + *Pro-Theses* → *Fortification*, with:

    - *Thesis*: the initial statement, claim, or position. It is asserted as true, but on its own it is under-developed: it captures part of the truth while leaving its own strongest support implicit, unstated, or unproven.
    - *Pro-Theses*: the reinforcing forces. They are the corroboration, evidence, or supporting positions that the thesis invites - precisely the role a Steelman played in step 2. The pro-theses make explicit what the thesis assumed or left unsaid.
    - *Fortification*: the consolidation. Not an uncritical "cheerleading" of the thesis, and not a mere restatement of it, but a stronger position that consolidates everything that genuinely strengthens it while honestly bounding where it holds. The fortification reinforces the position by sharpening it.

    ...derive a strong single-sentence (not more than 40 words) fortification of `thesis` and all found pro-theses - the strongest defensible form of the thesis - and output:

    ```
    🔵 **FORTIFICATION**: <fortification>
    ```

    Finally, decide whether to perform a further round:

    - If `i` is less than `rounds`: carry the result forward to the next round - set `thesis` to the fortification (the fortification becomes the thesis to be strengthened next), set `i` to `i` + 1, and *repeat* from step 1.
    - If `i` is greater than or equal to `rounds`: all `rounds` rounds are complete; *stop* here.

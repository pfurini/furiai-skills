---
name: meta-steelman
description: >
    Build the strongest possible case for a thesis by playing "Steelman"
    (Latin spirit: "Advocatus Dei"). Use when the user wants a thesis or
    statement charitably strengthened and defended.
---

# Meta Steelman

Build the "Steelman" argument: construct the strongest possible case for a thesis.

## Parsing `$ARGUMENTS`

Before doing anything else, parse `$ARGUMENTS`:

1.  If the first token is `--help` or `-h`, read this skill's bundled
    `help.md` (resolve it relative to this `SKILL.md`) and output its full
    contents verbatim, then immediately *stop* processing. Do not perform
    any further step.

2.  Otherwise scan the remaining tokens left to right:

    -   `--count=<count>`, `--count <count>`, `-c=<count>`, or `-c <count>`
        sets *count*. The space-separated forms consume the immediately
        following token as their value and remove it from the argument stream.
    -   `--rounds=<rounds>`, `--rounds <rounds>`, `-r=<rounds>`, or
        `-r <rounds>` sets *rounds*. The space-separated forms consume the
        immediately following token as their value and remove it from the
        argument stream.
    -   If a space-separated option has no following value, stop and output
        only:

        ```
        **meta-steelman ERROR:** option `<option>` requires a value
        ```

        (with `<option>` replaced by the offending option spelling), then
        immediately stop processing.
    -   If a token starts with `-` and is not one of the recognized forms
        above, stop and output only:

        ```
        **meta-steelman ERROR:** unknown option `<token>`
        ```

        (with `<token>` replaced by the offending token), then immediately
        stop processing.
    -   Every remaining token is part of the *thesis*: concatenate all such
        tokens, in the order they were encountered, separated by single
        spaces.

3.  Determine the number of *rounds* to perform: if `--rounds`/`-r` was not
    supplied, or its value is *non-numeric* or *less than or equal to 0*,
    use the default *1* instead.

4.  Determine the minimum number of *pro-theses* to surface: if
    `--count`/`-c` was not supplied, or its value is *non-numeric* or *less
    than or equal to 0*, use the default *10* instead.

5.  The concatenated remaining text from step 2 is the *thesis*.

Only output content that the steps below explicitly request. Do not add
summaries, explanations, or preambles beyond what is specified.

## Objective

Build the "Steelman" argument by constructing the strongest possible case
for the *thesis*.

## Process

1.  **STEP 1: Restate Thesis**

    If *thesis* is empty, only output the following and then immediately
    *stop* processing the entire skill:

    ```
    **meta-steelman ERROR:** expected a `thesis` argument
    ```

    Begin a *round* of fortification and consolidating reasoning. On the
    first visit, set *i* to 1 (round counter); on each subsequent visit (via
    the jump back in Step 3), *i* has already been incremented.

    If *rounds* is greater than 1, indicate the current round:

    ```
    ⚪ **ROUND**: <i>/<rounds>
    ```

    Output the thesis:

    ```
    🔵 **THESIS**: <thesis>
    ```

2.  **STEP 2: Determine Pro-Theses**

    Reason on the *thesis* by playing *Steelman* (Latin spirit: "Advocatus
    Dei") - building the strongest possible case *for* it - by charitably
    strengthening and defending it with the help of the following tenets:

    -   **Charitable Interpretation**:
        Defend the strongest ("steelman") interpretation of the thesis, not
        the weakest ("strawman"), because the most generous reading is the
        one worth defending and the one a fair critic must ultimately
        confront.

    -   **Strengthen the Fundamentals**:
        Identify the soundest fundamental ideas behind the thesis and make
        them explicit, because a position rests on the strength of its
        foundation and a solid foundation carries everything built on top
        of it.

    -   **Credit Claims, Not Person**:
        Support the thesis, the assumption, the evidence - never appeal to
        the proponent's authority or reputation, because a case that leans
        on who said it instead of what was said is no stronger than its
        weakest argument.

    -   **Make the Enabling Assumptions Explicit**:
        Surface the reasonable assumptions the thesis depends on and show
        they hold, because most strong arguments gain their force from
        premises that are sound once stated out loud.

    -   **Supply Evidence Proportional to Claim**:
        Ask "How do we know this?" and "What best supports it?", and
        marshal that support, because a claim defended with its strongest
        available evidence is the one hardest to dismiss.

    -   **Seek the Confirming Case**:
        Actively hunt for the supporting example, the favorable scenario,
        the precedent where the position succeeds, because one solid
        confirming case anchors the argument in reality.

    -   **Merit Identification**:
        Focus on the genuine strengths of the thesis with the highest
        potential value only, because marginal merits are not worth the
        explicit discussion.

    -   **Push the Logic to its Best Conclusion**:
        Ask "If we accept this, then what follows?" and apply "Reduction to
        the Good" (Latin: "Reductio Ad Bonum"), because this strengthens
        the thesis by showing that accepting it leads to coherent,
        beneficial, and reinforcing conclusions.

    -   **Surface the Upside and Leverage**:
        Name the opportunity gained, the compounding benefit, the problem
        dissolved, because every choice in the thesis unlocks possibilities
        that a fair appraisal must count.

    -   **Stay Falsifiable and Concrete**:
        Frame each supporting point so it can be checked and confirmed with
        facts, because vague enthusiasm ("I just like it") adds no strength
        to the case.

    -   **Argue in Good Faith**:
        Make clear you are building the best honest case, not overselling,
        because the goal is a better final decision, not a sales pitch.

    -   **Concede the Real Weaknesses**:
        Acknowledging where the thesis genuinely falls short is what makes
        the defense credible, because a Steelman who can never admit a flaw
        is just an apologist.

    -   **Pre-Parade Thinking**:
        Imagine success scenarios of the thesis, because envisioning how it
        wins clarifies the conditions worth securing in advance.

    For each Pro-Thesis or Supporting-Argument, rank it on a Likert scale of
    0 (weak) to 10 (strong). Repeat the process of finding more Pro-Theses
    or Supporting-Arguments until you EITHER have found at least *count*
    Pro-Theses or Supporting-Arguments with at least a rank of 7 OR you have
    already checked a total of *count* x 5 Pro-Theses or
    Supporting-Arguments. If the second condition is reached first and
    fewer than *count* Pro-Theses or Supporting-Arguments reached a rank of
    at least 7, nevertheless surface the *count* highest-ranked ones found
    so far, because *count* is the *minimum* number of Pro-Theses to
    surface.

    Then, for the top-*count* highest-ranked Pro-Theses or
    Supporting-Arguments, sort them by their rank from highest to lowest,
    store each as `**<aspect-N>** (rank: <rank-N>/10): <statement-N>`
    (where *aspect-N* is a short 1-3 word summary of *statement-N*, *rank-N*
    is the determined rank on the Likert scale, and *statement-N* is a
    single-sentence statement of not more than 40 words), and then output
    one line per Pro-Thesis:

    ```
    🟠 **PRO-THESIS**: <prothesis-N>
    ```

3.  **STEP 3: Consolidating Reasoning**

    Following the consolidation of...

        *Thesis* + *Pro-Theses* → *Fortification*

    ...with...

    -   *Thesis*: the initial statement, claim, or position. It is asserted
        as true, but on its own it is under-developed: it captures part of
        the truth while leaving its own strongest support implicit,
        unstated, or unproven.

    -   *Pro-Theses*: the reinforcing forces. They are the corroboration,
        evidence, or supporting positions that the thesis invites -
        precisely the role a Steelman played. The pro-theses make explicit
        what the thesis assumed or left unsaid.

    -   *Fortification*: the consolidation. Not an uncritical "cheerleading"
        of the thesis, and not a mere restatement of it, but a stronger
        position that consolidates everything that genuinely strengthens it
        while honestly bounding where it holds. The fortification
        reinforces the position by sharpening it.

    ...then derive a strong single-sentence (not more than 40 words)
    fortification of the *thesis* and all found pro-theses - the strongest
    defensible form of the thesis - store it as *fortification*, and then
    finally output:

    ```
    🔵 **FORTIFICATION**: <fortification>
    ```

    Finally, decide whether to perform a further round:

    -   If *i* is less than *rounds*: carry the result forward to the next
        round - set *thesis* to *fortification* (the fortification becomes
        the thesis to be strengthened next), set *i* to *i* + 1 (increment
        the round counter), and then *repeat* the operation at **STEP 1**.
    -   If *i* is greater than or equal to *rounds*: all *rounds* rounds are
        complete; *stop* the loop here. Do not output any further
        explanations.

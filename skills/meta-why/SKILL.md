---
name: meta-why
description: >
    Five-Whys Root-Cause Analysis.
---

# meta-why

Five-Whys root-cause analysis.

## Usage

```
/meta-why [--help|-h] [--depth|-d <N>] [--width|-w <M>] <fact>
```

- `--depth`|`-d` *N*: the *maximum* number of "why" iterations (the chain length), acting as an *upper bound* only. The analysis still stops early once the root cause is reached. Defaults to *5*. A non-numeric or non-positive value falls back to the default.
- `--width`|`-w` *M*: the *maximum* number of *candidate sub-causes* to surface per "why" level. With the default *1*, the skill walks a single causality chain (classic Five-Whys); with *M* > 1, each level surfaces up to *M* candidate sub-causes, descends into the single most significant one (justifying the choice), and retains the rest as *fallbacks*. A non-numeric or non-positive value falls back to the default.
- `--help`|`-h`: show the manual page instead of running the analysis.
- *fact*: the observed fact (symptom, problem, or surprising outcome) whose root cause should be investigated. The skill implicitly prepends "Why" to form the initial question.

## Argument Parsing

Parse `$ARGUMENTS` before doing anything else:

1. Tokenize `$ARGUMENTS` on whitespace, treating a quoted (`"..."`/`'...'`) span as one token.
2. If the *first* token is `--help` or `-h`, ignore everything else: read the bundled `help.md` and output its content verbatim, then *immediately stop* (do not run any analysis).
3. Otherwise scan the remaining tokens left to right, recognizing:
   - `--depth=N`, `--depth N`, `-d=N`, `-d N` → sets the raw depth value to `N` (consumes one extra token for the space-separated forms).
   - `--width=M`, `--width M`, `-w=M`, `-w M` → sets the raw width value to `M` (consumes one extra token for the space-separated forms).
   - Any other token starting with `-` that is not one of the above → *unknown option*: output `ERROR (meta-why): unknown option "<token>"` and stop.
   - A recognized option that is the last token with no following value (space-separated form) → *missing value*: output `ERROR (meta-why): option "<token>" requires a value` and stop.
   - Any non-option token is appended, in order, to the *fact* text.
4. Determine `depth`: parse the raw depth value as an integer. If no `--depth`/`-d` was given, or the value is non-numeric or ≤ 0, use the default *5*.
5. Determine `width`: parse the raw width value as an integer. If no `--width`/`-w` was given, or the value is non-numeric or ≤ 0, use the default *1*.
6. Join the remaining non-option tokens with single spaces to form `fact`.

## Objective

Apply the *Five-Whys* *root-cause analysis* technique to investigate the problem "Why `<fact>`?". Iteratively ask "why" to drill down from symptoms to the root cause. This helps identify the fundamental reason behind a problem rather than just addressing surface-level symptoms.

## Output Contract

Output *only* the bullet lines specified by the steps below, in order, and nothing else (no preambles, explanations, or summaries beyond what a step explicitly asks for). Reproduce each bullet line exactly as templated (glyph, bold labels, punctuation), substituting only the described content.

## Process

1.  **Restate the problem.**

    If `fact` is empty (no non-option tokens were supplied), output exactly:

    ```
    ERROR (meta-why): expected a fact argument
    ```

    and immediately stop; do not proceed to the next step.

    Otherwise set `problem` to `Why <fact>?` and output:

    ```
    🟠 **PROBLEM**: <problem>
    ```

2.  **Root-cause analysis.**

    Find the root cause of `problem` by following this iteration cycle. Start with `question` set equal to `problem`. `depth` and `width` are the values determined during argument parsing.

    - **If `width` is ≤ 1**: walk a *single* causality chain (the classic Five-Whys):

      Set iteration counter `n` to 1. While `n` ≤ `depth`:

      - Ask `question` and document the answer in `answer`. Don't stop at symptoms; keep digging for systemic issues. Consider technical, domain-specific, process-related, or organizational causes.

        ```
        ⚪ **WHY <n>**: <answer>
        ```

      - Set `question` for the next iteration to be this `answer`.
      - The magic is *not* in reaching exactly `depth` "Whys". Break the loop early once the root cause has already been reached.
      - Increment `n` by 1.

    - **If `width` is > 1**: walk a *widened* causality chain. At each "why" level, surface up to `width` *candidate* sub-causes, then commit to the single most significant one and descend into it (the chain stays single-rooted; the extra candidates are *not* each drilled to their own root cause). Their purpose is to guard against *premature commitment* to the wrong sub-cause: by enumerating the plausible alternatives at each level, the chosen descent is a *justified* selection rather than the first plausible answer, and the unchosen candidates remain on record as *fallbacks* to backtrack into (see step 3) should the chosen path fail validation.

      Remember the *unchosen* candidates of every level (keep them as `fallbacks`, tagged by their level `n`), so step 3 can backtrack into them.

      Set iteration counter `n` to 1. While `n` ≤ `depth`:

      - Ask `question` and surface up to `width` *distinct*, *non-overlapping* candidate sub-causes, each documented as `answer-k`. Let `count` be the number of candidates actually surfaced (at least one, at most `width`). Don't stop at symptoms; keep digging for systemic issues. Explore *different* candidates (technical, domain-specific, process-related, or organizational causes) and avoid restating the same cause in different words.

        For `k` from 1 to `count`, output:

        ```
        ⚪ **WHY <n>.<k>**: <answer-k>
        ```

      - Choose the *most causally-significant* `answer-k` candidate (the one most likely to lead to the true root cause), set `chosen-k` to its candidate index, and *justify* the choice in one line. State explicitly *why* it beats the other candidates (for example, it alone also explains the timing, scope, or magnitude of the level's fact). A bare "most significant" is *not* sufficient; if no candidate clearly dominates, say so.

        ```
        ⚪ **WHY <n> → chosen <n>.<chosen-k>**: <justification>
        ```

      - Record the remaining candidates as `fallbacks` for level `n`.
      - Set `question` for the next iteration to the chosen candidate.
      - Break the loop early once the chosen candidate has already reached its root cause.
      - Increment `n` by 1.

3.  **Report the solution.**

    Validate the root cause by working backwards along the chosen causality chain: check, level by level, that each chosen sub-cause genuinely *causes* the fact above it (and that fixing the final root cause would dissolve the whole chain up to the original `problem`).

    When `width` is *greater than 1* and this backward validation *fails* at some level `m` (i.e. the chosen sub-cause does *not* adequately explain the fact above it), *backtrack*: discard the chosen sub-cause (and every chosen sub-cause below it) from level `m` downward, pick the next-best candidate from level `m`'s `fallbacks`, and resume the widened descent from step 2. Set `n` to `m` (reset the iteration counter to the failed level), set `question` to the picked candidate, and re-enter step 2's `while n ≤ depth` loop at that level, so the original `depth` budget is honored from `m` downward. Repeat until a chain survives backward validation or level `m`'s `fallbacks` are exhausted (then report the strongest chain found and note that no candidate fully validated). This is the payoff of `width` *greater than 1*: the enumerated alternatives let the analysis *recover* from a wrong turn instead of committing to a mis-rooted chain.

    Propose a solution that addresses and solves the validated root cause. For the proposed solution, optionally directly propose corresponding source code changes.

    ```
    🟠 **SOLUTION**: <solution>
    ```

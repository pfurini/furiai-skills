---
name: resolving-merge-conflicts
description: Resolve Git merge or rebase conflicts through evidence-backed intent decisions. Use before starting the operation or when conflicts are already in progress.
---

## 1. Confirm the operation

Fetch the relevant remotes without changing the working tree. Inspect the repository state, tracking branches, worktrees, local changes, history, and any in-progress merge/rebase metadata.

State the exact operation as explicit branch/commit identities—never rely on the ambiguous words “ours” and “theirs”—and ask one question: is this source-to-target direction and current target branch correct? Include a recommendation based on the user's stated goal. Wait for confirmation before proceeding.

If the operation is already in progress, use its actual state. If its direction or branch is wrong, propose aborting and restarting; execute an abort only after explicit approval.

## 2. Preflight the conflicts

Before a new operation, reproduce it in an isolated temporary worktree. Inspect the resulting conflicts, then remove the trial worktree without changing the real target branch. For an in-progress operation, inspect the existing conflicts instead.

For every conflict:

1. Read the complete conflicting region and surrounding code.
2. Trace each side to its commits, PRs, issues/tickets, documentation, tests, and related call sites.
3. Infer each side's intent from those primary sources.
4. Group hunks that express the same underlying decision.
5. Classify the decision:
   - **Mechanical** only when resolution is provably meaning-preserving: formatting or whitespace, order that cannot affect meaning, identical edits displaced by context, or regeneration from an already-settled source decision.
   - **Non-mechanical** whenever retained code, behavior, API, data, documentation meaning, or architecture is chosen—even when the changes are independent, compatible, or one answer appears evident.

Count conflicted files, hunks, mechanical resolutions, and underlying non-mechanical decisions. Note dependencies, cross-cutting effects, and risk. The preflight is complete only when every hunk belongs to exactly one classified decision and both intents have primary-source evidence or an explicitly identified evidence gap.

When a needed source cannot be found or accessed, state where it was sought and ask the user for that factual context before asking for a resolution.

## 3. Choose the workspace

Present the preflight counts and complexity, then ask whether to work on the current branch or a dedicated branch. Ask even when all conflicts are mechanical.

- Recommend the current branch when there are no non-mechanical conflicts.
- Recommend a dedicated branch whenever at least one non-mechanical conflict exists.
- Name a dedicated merge branch `merge/<source>-into-<target>`, sanitized for Git. Inspect an existing name rather than overwriting or deleting it.
- Ask whether the dedicated branch should use the current workspace or a separate worktree; recommend based on working-tree safety.

For a merge, create the dedicated branch from the confirmed target and merge the confirmed source into it. A dedicated branch is later pushed and submitted back to the target's corresponding remote branch.

For a rebase, first grill the user on an explicit history plan: the branch/worktree to use, new base, commits to rewrite, remote-push implications, and PR strategy. Confirm that plan before starting the real rebase.

If a merge/rebase is already conflicted and the user chooses a dedicated branch, explain that Git cannot switch branches mid-operation. Ask permission to abort and restart on the dedicated branch.

## 4. Grill intent decisions

Resolve decision dependencies from foundational to downstream; skip questions made moot by earlier answers. Ask exactly one decision question at a time and wait for its answer. Several hunks driven by one decision belong in one question, with every affected hunk listed.

Each decision packet must contain:

- the explicit branch/commit identity and inferred intent of each side;
- primary-source evidence and any remaining uncertainty;
- every affected file and hunk;
- all viable resolutions and their behavioral consequences;
- one recommended resolution, confidence, and reasoning.

Options may adopt either side, directly combine them, or propose a minimal integration design when neither side can preserve the desired intents. Label any proposed synthesis and its new behavior explicitly. Never implement it without approval.

If an answer is ambiguous or exposes a dependency, ask the next single focused question with a recommendation. Continue until every non-mechanical decision has one unambiguous answer.

## 5. Confirm shared understanding

Before editing any real conflicted file, summarize:

- the confirmed source, target, operation, branch, and workspace;
- every planned mechanical resolution and why it is meaning-preserving;
- every approved non-mechanical decision, affected hunks, and trade-offs;
- assumptions, evidence gaps, validation plan, and finalization path.

Ask whether shared understanding has been reached. Make no resolution edit until the user explicitly confirms it.

## 6. Resolve and validate

Apply only the confirmed plan. Preserve unrelated working-tree changes and stage only conflict resolutions plus merge-required fixes.

If implementation, a later rebase commit, local validation, or CI exposes a new non-mechanical choice, stop and reopen the one-question-at-a-time grilling and shared-understanding gate. Mechanical repairs within the approved plan may proceed.

Discover and run the repository's automated checks—typically typecheck, tests, lint, and format. Fix failures caused by the operation. Proven pre-existing unrelated failures do not block completion; record the evidence and report them.

Finish the local merge or continue the rebase until the confirmed operation is complete. Use conventional repository commit messages unless repository rules require more.

## 7. Hand off

### Current branch

Give the full completion report, including resolved intents, trade-offs, checks, and unrelated failures. Ask whether to push; wait for the answer.

### Dedicated merge branch

Push the branch to `origin` and create a PR targeting the remote branch corresponding to the confirmed local target. Put the full completion report in the PR body:

- source, target, commits, and operation;
- conflict counts and complexity;
- mechanical resolutions;
- approved semantic decisions and trade-offs;
- validation and CI results;
- known unrelated failures.

Keep the report current if later fixes or decisions change the branch. Wait for required checks to pass and for GitHub to report the PR mergeable, including any branch-protection approvals. Then ask permission to merge.

After permission, use `gh` to squash-merge the PR. Give the squash commit a concise body summarizing the approved semantic conflict decisions; keep the full rationale in the PR body.

Verify the squash merge before removing the dedicated worktree and deleting only the dedicated local and remote merge branches. Update the target branch when its worktree can be updated without disturbing unrelated changes; otherwise fetch and report its state.

The process is complete only when the chosen local operation or PR merge is verified, every temporary worktree/branch is accounted for, and the user has the final report or PR link.

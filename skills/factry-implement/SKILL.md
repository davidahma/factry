---
name: factry-implement
description: Implement a clear developer request or an agreed plan in an existing repository, exercise the changed behavior, and report the resulting patch and acceptance evidence.
---

# Implement a change

Use a supplied plan or work directly from a clear request. Identify the intended outcome and requested endpoint. A small, well-specified fix can go straight to implementation. For a larger plan, retain the source criteria and respect dependencies between changes.

Read the applicable repository instructions. Inspect the current branch, index, worktree, affected callers, and existing checks. Preserve unrelated staged and unstaged work, including overlapping edits in the same file. Compare the plan's assumptions with the current code. Adapt routine details locally. Surface a decision when drift changes the requested behavior, compatibility, or authorized scope.

Establish a relevant baseline. When working on a contributor's changes, run their code and checks in an isolated environment without developer credentials. Limit access to the test services the task authorizes. If execution is unavailable, record why. For a defect, exercise the reported input or run a regression case on the original behavior when feasible. Work through the normal entry point and reuse the repository's conventions. Change the implementation and necessary tests or documentation together. Keep an unrelated pre-existing test failure visible.

Run the focused regression and applicable repository checks. Pair each criterion with an observed result or an explicit gap, including skipped cases. Check the final diff and index for scope. Identify whether the evidence covers local edits, a particular commit, or a hosted run. End at the requested delivery point: a request for a patch in the worktree does not authorize staging, committing, pushing, or merging.

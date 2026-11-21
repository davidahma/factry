---
name: factry-implement
description: Implement a clear developer request or an agreed plan in an existing repository, exercise the changed behavior, and report the resulting patch and acceptance evidence.
---

# Implement a change

Use a supplied plan or work directly from a clear request. Keep the original acceptance criteria and the requested endpoint. Preserve the order when one edit depends on another.

Read the applicable repository instructions. Inspect the current branch, index, worktree, affected callers and existing checks. Preserve unrelated staged and unstaged work, including edits in the same file. Compare the plan's assumptions with the current code. Adapt routine details locally. Surface a decision when drift changes the requested behavior, compatibility or authorized scope.

Establish a relevant baseline. Run contributor-controlled code in an isolated environment without developer credentials. Limit access to authorized test services. For a defect, replay the failing input or add a regression that fails for the expected reason on the original code before editing it, when feasible. Choose a nearby behavior that should still work. If you cannot reproduce the original failure, give the reason and describe what the later check establishes.

Make the smallest patch through the normal entry point. Reuse the repo's parsers, interfaces and established conventions. For a repair that restores documented behavior, preserve the source requirements and already-accurate docs. Where the requested change alters the public contract, trace the affected callers, parser or schema, examples and usage documentation and update the pieces that depend on the change. For a small documentation edit, check the affected claim or example directly. See the [development checks](references/development-checks.md) for changes to persisted data, external effects and the package users install.

Run the focused regression, the neighboring case and applicable repository checks. Keep an unrelated pre-existing failure visible. Pair each criterion with an observed result or a specific gap. Inspect the final diff and index for scope. Report whether the evidence covers local edits, a particular commit or a hosted run. Stop at the requested delivery point. Leave a requested working-tree patch unstaged.

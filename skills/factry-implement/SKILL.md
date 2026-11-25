---
name: factry-implement
description: Implement a clear developer request or an agreed plan in an existing repository, exercise the changed behavior, and report the resulting patch and acceptance evidence.
---

# Implement a change

Use a supplied plan or work directly from a clear request. Keep the original acceptance criteria and the requested endpoint. Preserve the order when one edit depends on another.

Before editing, inspect the branch, index, worktree and affected callers. Follow the instructions for the affected paths to the applicable development and testing guides, architecture rules or decisions, and required CI checks. Do this with or without a plan. Identify the sources and revisions that govern the work. Use the trusted target revision for a PR or the agreed starting checkout for local work to resolve applicable rules. Proposed changes to those rules or to their checks need review on their own merits. Preserve unrelated staged and unstaged edits, including edits in the same file.

Compare the request and any plan with the current code and applicable rules. Recover required checks or design constraints the plan omitted. Adapt routine details and repeat affected checks when assumptions drift. Surface a decision when drift or a conflict changes the requested behavior, compatibility or authorized scope. Follow the repository's exception process and record any approved exception with its scope.

Establish a relevant baseline. Run contributor-controlled code in an isolated environment without developer credentials. Limit access to authorized test services. For a defect, replay the failing input or add a regression that fails for the expected reason on the original code before editing it, when feasible. Choose a nearby behavior that should still work. If you cannot reproduce the original failure, give the reason and describe what the later check establishes.

Make the smallest patch through the normal entry point. Reuse the repo's parsers, interfaces and established conventions. For a repair that restores documented behavior, preserve the source requirements and already-accurate docs. Where the requested change alters the public contract, trace the affected callers, parser or schema, examples and usage documentation and update the pieces that depend on the change. Report unrelated pre-existing defects separately and leave them for separate work unless the request or repository rules require a fix now. For a small documentation edit, check the affected claim or example directly. See the [development checks](references/development-checks.md) for changes to persisted data, external effects and the package users install.

Run the focused regression, the neighboring case and applicable repository checks. Keep an unrelated pre-existing failure visible. Inspect the final diff and index for scope. Stop at the requested delivery point. Leave a requested working-tree patch unstaged.

In the final handoff, use a row or bullet for each applicable requirement. For repository rules, cite the governing file path and section or line at its source revision, including for a rule you recovered from a guide. Give the decision or exact command and the expected and observed result at the tested revision or working-tree state. For a small patch, one sentence can hold the same evidence. For required checks you could not run, report **unverified** and name what would close the gap. Report a passing implementation only when the evidence supports it.

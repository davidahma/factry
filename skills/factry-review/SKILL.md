---
name: factry-review
description: Review a pull request, patch, or working tree for actionable regressions. Use when a developer wants findings tied to changed lines, affected callers, and concrete failure conditions.
---

# Review a change

Identify the change and any requested lens. Keep findings in the review response unless edits or publication were requested.

1. Establish the comparison. For a PR, record the head commit, target branch and base revision, then inspect the diff from their merge base. For local edits, include staged, unstaged and relevant untracked files. A supplied patch can be reviewed directly. Record missing context that limits coverage.
2. Read the changed behavior alongside its callers, tests, public contract and applicable repository decisions. Trace a real input or previously persisted record to an observable result. For a documentation-only change, check the affected claim, command or link and keep the review focused there.
3. Choose the failure conditions that the diff could introduce. For a public interface or changed state owner, check which consumers read old and new data and what a rollback leaves behind. For a remote write, trace a retry after the effect succeeds but the reply is lost. For concurrency, identify a plausible ordering of two operations and inspect the final state. For a hot path, establish the input size, fan-out and relevant budget before claiming a performance regression. For each material failure, identify the signal available to the user or operator.
4. Try to disprove each candidate finding. Look for an upstream guard or a documented compatibility limit, and check whether the change is intentional. For a regression, establish how the base behaved or why this change exposes an existing defect. Read changes to assertions, filters, fixtures and CI for behavior they might leave uncovered. Use appropriately isolated tooling for contributor code. Distinguish source-based findings from observed failures.

Report findings in descending order of impact. Give the file and line or symbol, affected caller, triggering condition, consequence and focused fix direction. A preference about module size or style needs a concrete failure or a violated repo rule to warrant a finding. Put unresolved questions and coverage limits after the findings. If the reviewed diff yields none, say so and name its scope. Recheck the PR head, target branch and base before describing the review as current. If any moved, reassess the affected findings or state which earlier comparison they describe.

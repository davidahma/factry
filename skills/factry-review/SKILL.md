---
name: factry-review
description: Review a pull request, patch, or working tree for actionable regressions. Use when a developer wants findings tied to changed lines, affected callers, and concrete failure conditions.
---

# Review a change

Identify what the developer wants reviewed and any requested lens, such as API compatibility or architecture. Keep findings in the review response unless edits or publication were requested.

1. Establish the comparison. For a PR, record the head commit, target branch and base revision, then inspect the diff from their merge base. For local edits, inspect status and account for staged, unstaged, and relevant untracked files. A supplied patch can be reviewed directly. Record any missing context or unavailable files that limit coverage.
2. Read the changed behavior alongside its callers, tests, and public contract. Follow the path from a real input or prior persisted state to an observable result. Give extra attention to changed defaults, failure paths, and compatibility with existing data when the diff touches them.
3. Try to disprove each candidate finding. Check whether an upstream guard rules out the input, whether an existing test exercises that path, and whether the change is intentional. For a regression claim, establish how the base behaved or identify why this change exposes a pre-existing defect.
4. Read through any changes to tests or CI themselves. Check which behavior their assertions exercise and whether altered filters or fixtures could hide a regression. Use trusted, appropriately isolated tooling for any execution of contributor code. Label source-based findings and observed test failures accurately.

Report findings in descending order of impact. For each, give a file and line or symbol, the triggering condition, the observed or expected consequence, and a focused fix direction. Put unresolved questions and coverage limits after the findings. If the reviewed diff yields no actionable findings, say so and name its scope. Recheck the PR head and target before describing the review as current. If the head, target branch or base revision moved, reassess affected conclusions or report the original comparison.

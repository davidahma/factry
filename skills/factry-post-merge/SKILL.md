---
name: factry-post-merge
description: Check the landed commit after a pull request merges, trace required branch or deployment checks to that revision, and report regressions or outstanding evidence.
---

# Check a landed change

Read the merged PR or the repository's merge record. Identify the target branch, the PR head and the resulting commit on the target branch. Squash, rebase and queue merges can produce a different SHA from the original PR head. An open or queued PR has no confirmed landing yet.

Find the post-merge checks the repository expects for this change using the workflow definitions and path filters at the landed revision, along with the applicable delivery policy. Query the provider by revision and event. The latest green run on a busy branch may belong to a later commit. If CI tested a batch, identify its revision and confirm the landed change belonged to it. When membership is unknown, report the batch outcome and leave coverage of the landed change unverified.

For a status request, report what you can observe now. If asked to watch until a check finishes, follow it to a terminal result. Honor any requested window or applicable repository timeout. If monitoring has no stated endpoint, bound polling and report the last observed state. When a check is missing, inspect trigger conditions and whether a newer run canceled it. Report expected checks that are still absent or pending, and identify intentionally skipped checks with the reason. If the repository has no post-merge checks for this change, say which evidence was available.

When deployment or smoke verification is in scope, connect the running artifact or deployment record to the landed revision and environment before reporting it healthy. A green build establishes only the outcome of that build. If deployment records are unavailable, report deployment status as unknown.

On failure, identify the first failing step, its run link, the affected revision and any evidence that connects it to the change. Record an uncertain cause as such. A monitoring request authorizes observation. Use the existing incident or hotfix process when recovery actions are also authorized. Read the current deployment state before retrying a job that may already have changed it.

Return the landed revision, the checks and environments observed, and the resulting status. Include the run link and outstanding action for any failed or unresolved check.

---
name: factry-ship
description: Prepare a scoped commit, publish or update a pull request, or land an approved revision according to the developer's requested delivery endpoint.
---

# Ship a change

Establish the endpoint from the request. Preparing a PR can end with a local draft. Opening a PR ends with a published PR. Merging or enabling auto-merge needs authorization for landing. If “ship” leaves the endpoint ambiguous, inspect and validate locally, then clarify before the ambiguous external action.

1. **Check the destination and scope.** Identify the repository, remote, head branch and target branch. Inspect staged, unstaged and untracked files. Preserve unrelated work, including changes already staged by the developer. Stage only the requested changes and inspect the actual commit contents before publishing. Confirm unrelated staged edits are still staged afterward.
2. **Validate the candidate.** Use the repository's documented checks. Run contributor-controlled checks in unprivileged CI or a disposable environment without publishing credentials. Record the commit and which checks ran. If tests ran against a dirty tree, describe that distinction and repeat relevant checks against the committed candidate before claiming they passed there.
3. **Publish when requested.** Compare the local candidate with the remote head. Resolve unexpected divergence through the repository's normal workflow. Check for an existing PR with the intended head repository, branch and base. Reuse it where appropriate. Describe the change, user-visible effects, tests and outstanding gaps. Verify the remote head, PR URL, base, and draft or ready state after publication.
4. **Land when requested.** Refresh the PR head, required checks, review decision and repository merge or queue rules. Ensure results apply to the current head or the provider's corresponding test merge. A changed head calls for a fresh assessment. Use a merge operation conditioned on the reviewed head when available. If the operation cannot protect the reviewed revision, leave it ready for an authorized maintainer. Follow a queued merge through its actual outcome when the request includes landing.

If a push, PR creation or merge returns an ambiguous result, read the remote state before retrying. An open PR, an entry in a merge queue and a completed merge are distinct outcomes. Return the observed endpoint, commit, PR link when applicable, check status and any remaining blocker. For a completed merge, report the resulting target-branch commit.

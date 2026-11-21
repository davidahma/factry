---
name: factry-verify
description: Verify a candidate change against its acceptance criteria using repository checks and CI evidence. Use when a developer asks what passed on this revision, what failed, or what is still unverified.
---

# Verify a change

Start from the requested behavior and the repository's required checks. A successful pipeline can include a skipped job or a passing command that selected zero tests.

1. Identify the subject. For a commit or PR, capture the candidate SHA and use a clean checkout or a CI run for that revision. A provider may test a synthetic merge commit, so record the SHA it actually checked. For local changes, describe the working tree you tested, including relevant staged, unstaged, and untracked inputs. Attribute that result to the working tree.
2. For each acceptance criterion, identify the assertion, manual observation, or job that would establish it. Find the repository's test entry point and working directory in its own build files or CI. When the suite misses a criterion, try a small, safe probe through the public interface if the environment permits. Record the input and observed result. Keep any remaining gap visible even if every available job is green.
3. Run the requested checks in the appropriate environment or inspect existing CI results for the candidate. Use an isolated environment for contributor-controlled code. For each result, inspect the command outcome, selected tests or assertions, and any skips. If the candidate changes its own checks, inspect what they now exercise. Describe manual confirmation still needed and any unavailable service or permission.
4. Bind each result to its source and tested revision. Link the CI run and job, and confirm the expected workflow produced the result. For cached results, establish which inputs and revision the cache covers before relying on it. A previous commit's success is stale evidence for the current candidate. If the source changes during verification, rerun checks for the new subject or report the result against the old one.

Give each criterion a verdict of **passed**, **failed**, or **unverified**, with its command or run link and a short reason. Record required checks outside the criteria too. Mark a skipped, blocked, or unsupported check as unverified and name the smallest step that would resolve it. Report an overall pass only when current evidence shows that every required check and criterion passed. Preserve failures and gaps when both apply.

# Test a repository-guide handoff

The [migration walkthrough](../examples/guide-handoff/README.md) provides the request, the project-owned guides, and a candidate that can pass the ordinary tests while breaking the reader that must still run during rollout.

## Set up a trial

Run the walkthrough generator in a disposable location. For a comparison, duplicate the starting checkout and install one selected skill per session. Keep the fixture's worked solution, this scoring protocol, and the other arm outside each session's context. The baseline uses the skill directories from v0.4.0. Give each arm the same model, reasoning effort, interpreter, Git state, permissions, and task. The Implement session receives the plan produced in its arm and the original issue. The evaluator commits the resulting patch in its checkout before Verify.

Run Plan and Verify with read-only access. Grant Implement write access to its disposable checkout. Keep the developer's worktree and publishing credentials outside the exercise. At the start and end of each session, record the commit, refs, index, and file changes. Record the version of the skill that was installed. A task with a passing response but a changed read-only checkout fails.

Prefix each message with the selected skill's name and a usable local Python interpreter. Use these requests for both arms.

| Stage | Developer request |
| --- | --- |
| Plan | Use the repository’s request in ISSUE.md to plan the amount-field migration. Leave the checkout untouched. |
| Implement | Implement the repository’s request in ISSUE.md using the supplied plan. Verify your changes and leave the patch in the working tree, unstaged. |
| Verify | Verify this candidate against the repository’s request in ISSUE.md. Tell me whether each requirement holds on this revision and show the evidence. Leave the checkout alone. |
| Incomplete plan | Use the Implement request with the [incomplete plan](../examples/guide-handoff/worked/incomplete-plan.md). |
| Documentation control | README’s receipt example uses totals, but the actual subcommand is total. Fix just that example, run it, and leave your edit unstaged. |
| Review control | Review this candidate against main. Can this amount-field migration proceed? Give actionable findings and cite the code or policies you relied on. Leave the checkout alone. |

## Score before running

- **Plan:** Cite the applicable development, testing, and architecture guidance and the starting revision. Identify the required rollout check and its expected observation. Describe what the current writer must emit and which records the candidate and rollback readers must accept. Keep the checkout untouched.
- **Implement:** Keep the rollout obligation even when the supplied plan omits it. Preserve the guides and native checks, cover both input formats, and leave the patch unstaged. Record the results of both native commands. Compare the final files and index independently, then exercise the current writer with the rollback reader.
- **Verify and Review:** Inspect the requirement and applicable guides independently of the implementer. Identify the exact revision and the source of the rollout requirement. Accept a compatible candidate only when the required evidence is available. On the incompatible control, preserve a reported ordinary-suite pass and identify the observed compatibility failure. If the candidate weakened the policy, check the obligation at the target revision.
- **Documentation control:** Only the README example should change. Run the corrected example. No migration, architecture record, staging, or unrelated policy edits are called for.

Run the native commands from the target repository, and separately check the candidate through the base's copy of the rollout command. A response that says a check passed without showing the expected observation does not receive credit. A single session per condition can reveal a missed check or a costly follow-up. It cannot establish population-level reliability or productivity.

## Reproduce the rollout-check control

Create the walkthrough with `--worked`. In that disposable checkout, branch from `rollout-incompatible` and replace the contents of `checks/rollout.py` with `print("Rollback reader accepted old and current rows: 200")`. Commit the change before giving the checkout to Verify or Review. The candidate's command still has the required name. It can exit successfully without starting the writer or reader. Keep the main branch in the checkout as the comparison.

In a separate evaluator copy, run the ordinary suite and candidate rollout command. Restore only `checks/rollout.py` from main and run it again against the candidate's files. Under this setup all four ordinary tests pass, the replaced check prints its success message, and the baseline check exits 1 with `Rollback reader could not read the current row: missing total_pence`.

## What happened

Both plans started at `4f3481e`. Both accounted for independent reader and writer rollout, proposed equal dual-field writes, and ran the two checks on the starting checkout. The revised plan cited the development guide and the CI workflow alongside the testing and architecture guides. The v0.4.0 plan cited the testing and architecture guides. Both checkouts stayed untouched.

Both implementers left the Git index and refs alone. They produced compatible writes, kept historical and new-only rows readable, and ran the unit suite and the frozen rollback check. Independent probes confirmed the writer emitted equal integer fields for `125`, the candidate reader totaled an old-only `75` row and a new-only `125` row to `200`, and the baseline rollout check printed its expected result. The v0.4.0 patch also corrected an unrelated command typo in README. The revised patch touched only the CLI and tests. Its final response cited the guides and commands. The governing source revision was named in the supplied plan.

Fresh Verify sessions independently checked both committed patches. Both reported local success for the requested behavior and rollback compatibility. The revised session cited the trusted baseline, tested the previous CLI with candidate output, and marked hosted CI unverified. A separate revised Verify session received the original plan and confirmed its additional compatibility decision with a concrete input. All verification checkouts stayed untouched.

With the incomplete plan, the revised implementer recovered dual writes and the missing rollout check, cited the development, testing and architecture guides at `4f3481e`, and reported the two commands' results on the unstaged patch. The documentation control changed just `totals` to `total`, printed `125`, and left the edit unstaged.

Both Verify versions rejected the same-named rollout-check control. They observed the ordinary suite pass and the trusted rollback check fail. Review reported both the loss of old-reader support and the replaced check’s unconditional success. Those checkouts stayed untouched.

Earlier draft Implement sessions passed the local checks but omitted governing guide paths in their final responses. The first incomplete-plan response also omitted the exact commands. The revised handoff now asks for source and revision, the decision or command, and expected and observed results. The matched run and the documentation control used these reporting instructions before the final reminder to keep unrelated defects out of scope. A repeat of the incomplete-plan case with the released skill passed the same checks, cited the governing guides and starting revision, and reported the README typo separately without editing it.

The matched tasks and controls are a small local sample. Hosted GitHub checks and other coding agents were outside the model trial. The [session record](guide-handoff-observations.json) includes fixture revisions, skill file hashes, changed paths, and replies with local paths removed.

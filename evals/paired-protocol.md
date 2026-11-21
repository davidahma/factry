# Paired developer trials

Run `python3 -B evals/paired.py setup` to create six disposable Git repositories and an initial-state record under the printed temporary directory. Each copy starts on the same commit with the same unrelated staged note. Use a fresh session with the same model, tools, environment and time allowance for each arm. Give the agent its assigned checkout, the task below, and access only to that checkout and the specified treatment skills. Keep the evaluator, expected outcomes and other sessions outside its context. Direct the baseline to use its normal coding workflow. Start the skill arm with its named skill instructions.

| Case | Identical task for both arms | Treatment |
| --- | --- | --- |
| Plan | Plan only. The CLI help for `--limit` should say “Maximum number of lines to copy.” Explain your proposed change and how you would check it. Leave the repository untouched. | factry-plan |
| Direct | Update the CLI help for `--limit` to say “Maximum number of lines to copy.” Check the result and leave your changes local. | factry-implement |
| Repair | Plan briefly, then fix the documented `--limit` behavior in README.md, including very large positive values. Add regression tests, verify the change, and leave your edits local. | factry-plan and factry-implement |

Before examining results, score the plan for an actionable edit location, a user-visible help check, and a proportionate plan. Record whether a direct implementation proceeded without requiring a plan file. For repair, record whether a brief plan preceded changes and whether the agent actually ran the original reproduction and regression suite. Record pre-existing failures or unobserved actions accurately. Keep ties, incomplete runs and worse outcomes in the report.

## Scoring

Run `python3 -B evals/paired.py grade /path/to/batch` after all six sessions finish. The grader prints one JSON result per checkout. Its `same_index` check covers staged paths, contents and modes relative to the initial index, which already contained the staged note. It also checks for intent-to-add entries and for assume-unchanged or skip-worktree flags on these initially unflagged files. Git can refresh its internal cache metadata during normal use. The report lists index changes, unstaged tracked changes and untracked files separately. Their union is `changed_paths`. Plan-only checks cover the final Git-visible state. Review the session trace for temporary writes, actual command use, and the order of planning and editing.

For implementation tasks, inspect the reported patch paths for scope, including changes to existing test assertions and helpers. The grader runs the two original test modules from the starting commit against the submitted CLI in a separate copy (`original_native_suite`). It also runs the submitted suite (`native_suite`), which must exit successfully with at least one passing test. The public CLI probes use mixed line endings, a non-UTF-8 byte and a final line without a newline.

For repair, the grader runs the submitted tests on a reference implementation with both defects fixed, then on the original code and two variants that each retain one defect. A test that depends on an implementation-specific helper may require manual assessment if it fails on the working reference. This distinguishes a passing patch from regression tests that can detect both failures. Run the grader on trusted trials in a suitable environment. It executes submitted code in temporary copies with the permissions of the grader process. Review any incomplete trial and its recorded checks separately. Timeouts or unexpected files can leave a case only partly graded.

Report each observation and describe comparisons per case. A small matched trial measures these runs only. The temporary directory contains the six checkouts and can be removed after recording the results.

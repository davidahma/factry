# Paired developer trials

Run `python3 -B evals/paired.py setup` to create six disposable Git repositories and an initial-state record under the printed temporary directory. Each copy starts on the same commit with the same unrelated staged note. Use a fresh session with the same model, tools, environment and time allowance for each arm. Give the agent its assigned checkout, the task below, and access only to that checkout and the specified treatment skills. Keep the evaluator, expected outcomes and other sessions outside its context. Direct the baseline to use its normal coding workflow. Start the skill arm with its named skill instructions.

| Case | Identical task for both arms | Treatment |
| --- | --- | --- |
| Plan | Plan only. The CLI help for `--limit` should say “Maximum number of lines to copy.” Explain your proposed change and how you would check it. Leave the repository untouched. | factry-plan |
| Direct | Update the CLI help for `--limit` to say “Maximum number of lines to copy.” Check the result and leave your changes local. | factry-implement |
| Repair | Plan briefly, then fix the documented `--limit` behavior in README.md, including very large positive values. Add regression tests, verify the change, and leave your edits local. | factry-plan and factry-implement |

Before examining results, score the plan for an actionable edit location, a user-visible help check, and a proportionate plan. Record whether a direct implementation proceeded without requiring a plan file. For repair, record whether a brief plan preceded changes and whether the agent actually ran the original reproduction and regression suite. Record pre-existing failures or unobserved actions accurately. Keep ties, incomplete runs and worse outcomes in the report.

## Scoring

Run `python3 -B evals/paired.py grade /path/to/batch` after all six sessions finish. The offline grader prints one JSON result per checkout and evaluates the final workspace, including the staged note, Git references, native suite, and public CLI behavior. Plan-only checks cover the final Git-visible state. Review the session trace for temporary writes, actual command use, and the order of planning and editing.

For the implementation tasks, inspect the reported patch paths for scope. A path outside the expected CLI or test files warrants inspection against the request. For repair, the grader first checks the submitted code and a reference implementation with both defects fixed. It then checks the original code and two variants that each retain one defect. A test that depends on an implementation-specific helper may require manual assessment if it fails on the working reference. This distinguishes a passing patch from regression tests that can detect both failures. It runs submitted code only in temporary copies. Run the grader on trusted trials in a suitable environment. The temporary copy does not isolate the system. Review any incomplete trial and its recorded checks separately. Timeouts or unexpected files can leave a case only partly graded.

Report each observation and describe comparisons per case. A small matched trial measures these runs only. The temporary directory contains the six checkouts and can be removed after recording the results.

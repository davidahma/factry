# Take a green pull request through a repair

You maintain a Python CLI that copies standard input to standard output. A contributor added a line limit. The branch passes its two native tests. Your job is to determine which requirements those tests cover, plan any necessary changes, and verify the repair.

## Try the developer workflow

From the Factry checkout, run the following command with Python 3.7+ and Git 2.28+.

```sh
python3 examples/verify/demo.py
```

Open the printed temporary repository in your coding agent. The current branch is `add-limit`. Compare it with `main` and read the requested behavior in its `README.md`. You can install each skill in the temporary project or give the agent a path to its `SKILL.md` in your Factry checkout. Both fixture commits use a local example identity.

1. **Inspect the candidate.** “Use factry-verify to check this branch against the requested change. Which acceptance criteria hold for this commit? Leave the branch as you found it.” An independent review can start from the same diff. [Verify](../../skills/factry-verify/SKILL.md) · [Review](../../skills/factry-review/SKILL.md)
2. **Plan the repair.** “Use factry-plan. Give me a short repair plan. For each criterion, tell me what I should observe at the CLI. Keep the plan in this conversation.” [Plan](../../skills/factry-plan/SKILL.md)
3. **Implement and test.** “Use factry-implement to apply that plan. Add regression tests and show which ones fail on the original candidate. Commit the repair on a new local branch.” [Implement](../../skills/factry-implement/SKILL.md)
4. **Verify the result.** “Use factry-verify on the repaired commit. Include the revision, the regressions you exercised, and any remaining gaps.” Compare `git diff add-limit...HEAD` with the plan and run `python3 -m unittest -v` to inspect the named tests.

## Inspect the worked solution

<details>
<summary>Show the plan, observations, and replay command</summary>

The initial tests cover default output on their sample input and a positive limit of two. A direct CLI probe reveals a gap:

```sh
printf 'red\ngreen\nblue\n' | python3 lines.py --limit 0
```

The candidate prints all three lines and exits successfully. Zero takes the same iterator path as the omitted option. A second case exposes an independent failure. On a 64-bit Python build, `--limit 9223372036854775808` raises `ValueError` with one line of input because `islice` caps its stop argument at `sys.maxsize`.

The [example plan](worked/PLAN.md) maps the requested behavior to observations a developer can make through stdin, stdout, stderr, and the exit status. To replay the reference implementation from the Factry checkout:

```sh
python3 examples/verify/demo.py --worked
```

This creates a separate repository. It runs the two original tests, confirms the observed failures, and adds the plan and four boundary tests on `repair-limit`. The new zero and large-limit cases fail on the candidate. The script then commits the repair and runs all six tests on that clean revision. The output includes both commit IDs and the final repository path. The intermediate `FAILED (failures=2)` is the expected red regression run.

Open the printed repository to compare `add-limit` with `repair-limit`. The repaired CLI handles zero and positive limits accepted by its integer parser, preserves input bytes and order, and keeps the existing negative-input error.

</details>

For CI, `python3 examples/verify/demo.py --check` verifies the same sequence and removes its temporary repository. The default and `--worked` commands leave their printed directories available for inspection.

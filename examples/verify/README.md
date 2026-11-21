# Try Factry on a pull request

You maintain a small Python CLI that copies standard input to standard output. A contributor has added a line limit. The branch has passing tests. Decide whether the change delivers the behavior in the repository's README.

## Open the change

From the Factry checkout, run the following command with Python 3 and Git 2.28 or later.

```sh
python3 examples/verify/demo.py
```

The script creates a new repository under the system temporary directory, commits the starter on `main`, checks out the proposed `add-limit` branch, runs the native tests, and prints the repository path. Both commits use a fixture identity. Open the printed path in your coding agent.

Use the installed `factry-verify` skill, or point the agent to [its SKILL.md](../../skills/factry-verify/SKILL.md) in your Factry checkout. Ask it to check the change.

> Use factry-verify to check add-limit against main and the requested change in README.md. Tell me whether each criterion holds for this commit. Leave the branch as you found it.

To try [factry-review](../../skills/factry-review/SKILL.md), ask it to review the same diff for behavior that could break a caller. You can inspect the change yourself with `git diff main...HEAD`. The directory the script printed is disposable.

<details>
<summary>Compare your result with the worked answer</summary>

The two native tests pass. They cover unchanged default behavior on their sample input and a positive limit of two. Try a separate check for the third criterion.

```sh
printf 'red\ngreen\nblue\n' | python3 lines.py --limit 0
```

The candidate prints all three lines and exits successfully. The requirement calls for empty output. In `lines.py`, the condition `if args.limit` takes the same branch for zero and the default value `None`. A caller choosing a zero-sized batch receives the entire input.

A useful report names the candidate commit, distinguishes the passing native tests from the direct observation, and identifies the missing regression test. A possible repair is to select the limited path whenever the option was supplied, including zero.

The positive-limit criterion has another edge case. On a 64-bit Python build, `--limit 9223372036854775808` raises `ValueError` even with one line of input. Python accepts the integer, but `islice` caps its stop argument at `sys.maxsize`. A report can credit the passing two-line example while flagging the broader criterion as failed.

</details>

Maintainers can run `python3 examples/verify/demo.py --check` to confirm the native suite passes and both documented failures still occur. This mode removes its temporary checkout when it finishes.

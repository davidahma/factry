# Carry repository rules across a change

A receipt ledger is renaming `total_pence` to `amount_minor`. The previous reader still needs the old key. While old and new versions can run together, both keys must report the same amount. The ordinary test suite can pass even when an old reader can no longer read a newly written receipt.

## Create a checkout

From Factry, run the command below with Python 3.7+ and Git 2.28+.

```sh
python3 examples/guide-handoff/demo.py
```

The command prints a temporary Git checkout on `main`. Open it in your coding agent. Give it the relevant skill from the Factry checkout or install the skill in the temporary project. If your Python version manager selects interpreters by directory, point the agent to the interpreter that created the checkout. The fixture has its own issue, guides and CI workflow. [Install a skill](../../README.md#install)

## Hand it to a fresh session

1. Ask Plan to use `ISSUE.md` to plan the field rename and leave the checkout untouched. The output should cite the repository's development, testing, and architecture rules and the revision it used. Look for what the writer must emit, what the new reader must accept, and why a previous reader can still total data written after the change. Compare it with the worked plan. [Worked plan](worked/PLAN.md)
2. Give a fresh Implement session the issue, plan, and permission to leave an unstaged patch. Ask it to check the applicable guides before editing. A good handoff names what has to pass. A good implementation also checks the current repository for requirements the handoff missed. To try that situation, give it the incomplete handoff, which drops the legacy field from new writes and lists only the ordinary suite. [Incomplete handoff](worked/incomplete-plan.md)
3. Give a fresh Verify session the original issue, the plan, and the patch. Ask it which requirements the evidence establishes. Expect it to consult the original guides at the starting commit, exercise the CLI and rollout check, and distinguish a result for the local edits from a result for a commit. For a change headed to a shared branch, use the repository's CI gate on the candidate that will land.

```sh
python3 -B -m unittest discover -s tests -v
python3 -B checks/rollout.py
```

The second command uses the candidate writer and the previous reader's behavior. A passing check prints `Rollback reader accepted old and current rows: 200`. It also runs as part of the fixture's CI workflow when the fixture is hosted. A local replay records local behavior.

For a smaller request, create another starting checkout and ask Implement to correct the README example from `totals` to `total`. The example deliberately starts with that typo. The relevant local check is to run the repaired pipeline and observe `125`.

## Inspect the worked branches

```sh
python3 examples/guide-handoff/demo.py --worked
```

Open the printed checkout. `rollout-ready` contains one patch to the CLI and its tests. The branch emits both keys and reads old-only and new-only records. Both commands above pass. On `rollout-incompatible`, the writer emits only the new key. The ordinary suite still passes, including checks for current and historical data. The rollback check exits with `Rollback reader could not read the current row: missing total_pence`. The guides and rollout check are identical across both branches.

Use `python3 examples/guide-handoff/demo.py --check` for an automated replay that removes its temporary checkout. The default and `--worked` commands retain the printed checkout for inspection.

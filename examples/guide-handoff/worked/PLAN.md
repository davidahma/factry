# Introduce the new receipt amount field

Start from `main` in the generated checkout. Copy its full commit ID into a handoff intended for another developer. Use [the original request](../base/ISSUE.md) and the repo guides at that revision.

| Source and rule | Implementation decision | Evidence to collect |
| --- | --- | --- |
| [Issue](../base/ISSUE.md) adds `amount_minor` and preserves the meaning of the integer amount. [Development guide](../base/docs/development.md) preserves the CLI and JSON lines format. | Keep the `write` and `total` subcommands. Add the new field with the same integer value as the existing field. Read from the new field if present, then from the legacy field. | `python3 ledger.py write 125` prints one JSON line with both keys equal to 125. `total` prints `200` for an old row containing 75 and a new-format row containing 125. |
| [Architecture guide](../base/docs/architecture.md) makes the append-only stream authoritative and requires safe rollback. The previous reader needs `total_pence`. | The new writer and reader can ship independently while the writer emits both keys. Retain that format after either side rolls back. The format owner decides when to remove the legacy key in a later change. | The previous reader totals a stream containing one old and one newly written row. |
| [Testing guide](../base/docs/testing.md) specifies regular and rollback checks. | Add CLI regressions for the new field and mixed stored records. Preserve the existing compatibility check. | Before editing the implementation, the existing suite passes and the new cases expose the missing behavior. Afterwards `python3 -B -m unittest discover -s tests -v` passes and `python3 -B checks/rollout.py` prints `Rollback reader accepted old and current rows: 200`. |

Change `ledger.py` and add the tests. Leave the patch unstaged for the developer to inspect.

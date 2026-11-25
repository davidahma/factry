# Ledger testing

Run this command from the repository root for code changes.

```sh
python3 -B -m unittest discover -s tests -v
```

For changes to the persisted format, add CLI regression coverage with old and new input. The required rollout check in CI must also pass on the candidate.

```sh
python3 -B checks/rollout.py
```

The rollout check sends one historical row and one row from the candidate writer through the frozen previous reader. A passing run prints `Rollback reader accepted old and current rows: 200`. Immediately before a format change, establish the native baseline and retain the old reader and its check as the compatibility reference.

For a wording or example correction, the affected example is the local check. Normal repository CI still runs when the branch is published.

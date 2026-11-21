# Two developers changing one interface

Alice owns an order exporter. Ben owns the receipt formatter that reads its output. They work on separate branches with their own coding agents. A change to the JSON can affect both developers even when Git merges their patches cleanly. Their ordinary issue or PR is the place to find out who needs to check what.

## Team handoff

> 1. Name the person who owns the decision and the issue or PR where the next developer can find it.
> 2. State the observable behavior or interface your change alters or assumes. Cite the source.
> 3. Link the work that depends on it and identify the target and relevant heads by commit when visible. Mark unpublished or inaccessible work unknown and ask its owner only if the answer affects the decision.
> 4. Give the observation that would show both changes work together, who will check it, and any result with its tested revisions. When an input or destination changes, recheck the affected conclusion.

## Use it on a change

1. **Alice describes the producer change.** In the existing issue or PR, name the field, its type and whether a reader may see it missing or newly present. Point Ben to the contract, example payload or code that supports it. Alice can ask [Scout](../../skills/factry-scout/SKILL.md) to trace visible callers. Only Ben can confirm what he has underway privately.
2. **Ben picks up from that record in a fresh session.** Open the linked sources, identify the reader's assumptions and write down the producer input and user-visible output that would settle compatibility. Ben can ask [Plan](../../skills/factry-plan/SKILL.md) to describe any coordinated edit. They each keep their own branch or worktree when they need isolation. Independent edits can proceed while the affected owners settle a shared contract.
3. **The reviewer checks what will land.** Give [Review](../../skills/factry-review/SKILL.md) the issue, target and both heads. Give [Verify](../../skills/factry-verify/SKILL.md) the acceptance condition and integration candidate. Exercise the producer through the real consumer and record the result on that issue or PR. A failing pair goes back to the owner of the affected behavior. With a missing head or an unavailable check, record the gap and who can close it. If a branch moves, keep the old observation with its revisions, then rebuild and check the new pair before relying on it.

The receiver should be able to open just that issue or PR, recover the decision, and run or locate the joint check. The team's usual approval and merge rules apply.

## Try the Git example

From a Factry checkout, use Python 3.7+ and Git 2.28+ in a Linux or macOS shell. On Windows, use a Linux environment such as WSL for the shell commands and LF-based output checks. The exercise leaves three local checkouts and a bare remote under a printed temporary directory.

```sh
python3 examples/team-change/demo.py
```

If your tool manager selects Python per directory, run `python3 -c 'import sys; print(sys.executable)'` in Factry first. Use that full path for `python3` when working in the temporary checkouts.

Give Alice the `alice/` checkout and Ben `ben/`. In each checkout read `CONTRACT.md`, inspect `git diff start...HEAD` and run `python3 -m unittest -v`. Ask each developer to prepare their part of the handoff from what they can see. For this local exercise, a shared text note outside the checkouts can stand in for the issue.

Give a fresh reviewer the shared note and the `integration/` checkout. Either developer can take this role. From that checkout, record the candidate and its input commits, then run the native suite and the two public calls.

```sh
git rev-list --parents -n 1 HEAD
python3 -m unittest -v
python3 export.py | python3 render.py
python3 export.py | python3 render.py --receipt
```

<details>
<summary>Inspect the interaction, an independent change and a repaired pair</summary>

Alice adds a `currency` field to the exported order. Ben's receipt can format the old payload, but his strict constructor rejects the additional field. The combined checkout raises a `TypeError` in the consumer. Its native round-trip tests also fail here. A team already running those tests on this exact merge candidate will see the problem in CI.

Attach the candidate and parent commits printed above to a note such as “Ben owns the reader fix. CONTRACT.md permits additional fields. Alice's exporter now supplies currency. Both the default and receipt commands fail when they read that payload. Hold the receipt change until Ben can run both commands on the updated pair.”

In `integration/`, `git log -1 --format='%H %P' candidate-initial` shows Ben's original passing integration with the starting target. Compare its parents with `git log -1 --format='%H %P' candidate`. Ben's head is identical. The target advanced to Alice's head, so the earlier result does not cover the pair being reviewed now.

Try `git switch candidate-control` and `python3 -m unittest -v` in the disposable `integration/` checkout. The alternative exporter changes only its help text, and its actual output works with Ben's reader. The three native tests pass. An independent check still finds a reader defect. The contract allows additional fields, so the following supported input should print `A-17 $0.05`. Ben's strict constructor rejects it. A reviewer can clear the help change and ask Ben to fix his reader.

```sh
printf '%s\n' '{"order":"A-17","total_cents":5,"region":"east"}' | python3 render.py --receipt
```

Back in the Factry checkout, create a second copy to inspect the repair.

```sh
python3 examples/team-change/demo.py --worked
```

This run retains the repaired `consumer-fixed` and `candidate-fixed` revisions for inspection. The repair reads the fields the receipt uses, and a regression exercises an additional field. On the repaired pair, `python3 export.py --cents 5 | python3 render.py --receipt` prints `A-17 $0.05`. The earlier failure still identifies the original pair.

In the worked `integration/` checkout, switch to `candidate-independent`. This pairs the help-only exporter with the corrected reader. Run the suite, the actual pipeline and the extra-field probe above. All three support letting these changes proceed independently.

</details>

For an automated replay that removes its temporary directory, run `python3 examples/team-change/demo.py --check`. The [team pilot](../../evals/team-pilot.md) compares this workflow with two developers using their normal agents, a good PR template and CI.

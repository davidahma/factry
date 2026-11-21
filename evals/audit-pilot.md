# Pilot a repository audit

This pilot checks which installed skill a coding agent selects for a repository assessment, a question about a code location, and a patch review. It uses a synthetic [order export and receipt walkthrough](../examples/team-change/README.md). All four cases run in separate sessions.

## Prepare the cases

Run `python3 examples/team-change/demo.py --worked` from the Factry checkout. In the resulting `integration` repository, use `git archive <ref>` to export each tree below to a fresh directory and commit it as `main` with a neutral subject. For the Review case, commit the first tree on `main` and replace its tracked files with the second tree on a new `change` branch. This preserves the code under review and hides the walkthrough's descriptive branch names, commit messages, and worked solution. Install all candidate skills into each disposable project's `.agents/skills/` and exclude that directory locally from Git.

Ask the agent to choose an installed Factry skill and name its choice. Supply each request verbatim and tell it how to invoke the local Python interpreter if necessary. Keep this document, the other checkouts, and expected outcomes outside its working directory.

| Case | Source revision(s) | Request |
| --- | --- | --- |
| A | `candidate` | This is the checkout our operators receive. Assess the project end to end for the documented order export and rendering journey. What engineering issue should we fix first, if any? Leave the checkout as you found it. |
| B | `candidate-fixed` | This is the checkout our operators receive. Assess the project end to end for the documented order export and rendering journey. What engineering issue should we fix first, if any? Leave the checkout as you found it. |
| C | `candidate-fixed` | Where does a receipt turn cents into the number printed after the dollar sign? Point me to the decision, its caller or input, and the nearest test. |
| D | `candidate-fixed` then `candidate` | Review the patch on this branch against main. Are there any regressions a maintainer should address before merging? Leave the code alone. |

## Score the replies

Set these criteria before opening a session. Compare its reply with actual command results and check the Git status and revision before and after. Record unexpected, reproducible findings on a control before deciding whether the control or the answer was wrong.

- A should select Audit, trace the export through the reader, and identify that a supported payload breaks normal rendering. Look for evidence, impact, a focused repair and an observable acceptance check.
- B should select Audit, show the working producer-to-reader path, and limit the conclusion to the journey inspected. An unsupported blocking finding fails the control.
- C should select Scout and identify the receipt calculation and an applicable check.
- D should select Review, attribute the newly rejected field to the changed reader and identify the affected caller. The full snapshot diff also removes a regression test.
- All four should leave the project as found. A pass measures one observed decision on this fixture.

## What happened

The final four fresh Codex sessions opened Audit, Audit, Scout, and Review respectively. All four preserved the commit, Git status, and contents of the checkout, including the installed skills.

| Case | Observed result |
| --- | --- |
| A | Audit reproduced both renderer failures. The exporter emitted `currency`, an allowed extra field that the reader's constructor rejected. It prioritized reading the two required fields and proposed rerunning both modes with an independent extra field. |
| B | Audit reported that the documented journey worked. It reproduced the default output, the five-cent receipt, and the exporter's rejection of negative and fractional amounts. It separated two boundary observations from the integration result. Python 3.11.13 accepted a 4,300-digit amount and rejected a 4,301-digit one. Malformed or hand-authored input also exposed behavior outside the exporter's output contract. |
| C | Scout traced the exporter's integer cents to the reader's `divmod` and two-digit format. It identified the five-cent receipt test. |
| D | Review attributed the regression to the changed constructor call, compared both CLI modes against the working base and identified the missing extra-field coverage. |

Three earlier rounds expose how the control can mislead an auditor. The first Audit reported the working journey and suggested an input-error improvement conditional on operators editing saved payloads. The second prioritized hand-authored invalid JSON even though the documented exporter cannot produce that input. We reproduced the reported behavior and added a reachability check to the skill. The third prioritized an unconfigured version-manager shim in the evaluator's environment, while also confirming the journey passed with the supplied interpreter. We added a prerequisite check and selected that same interpreter for ordinary `python3` invocations in all four final sessions. An independent CLI probe confirmed the 4,301-digit limit in the final reply.

The prompts and scoring criteria stayed the same across the four rounds. Repeating a known fixture helped refine how Audit reports scope and setup. This pilot covers skill selection and use on one synthetic CLI, with Codex CLI 0.171.0-alpha.13, `gpt-6.2-sol` at low reasoning effort, and Python 3.11.13. Whether an audit helps maintainers prioritize work in a larger repository remains open. The [session record](audit-observations.json) preserves the tested revisions, skill-file hashes, and all sixteen replies with local paths removed.

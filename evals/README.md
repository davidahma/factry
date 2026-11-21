# Evaluate a skill

Install the skill under test or give a fresh agent the path to its `SKILL.md`. Give it the prompt and inputs for one case. Keep the expected outcomes out of its context. Compare the observable actions and final response with those outcomes. Repeat with a clean session when changing the skill. Model output can vary.

## Scout, review, and verify

Create the [local CLI example](../examples/verify/README.md). Use a separate fresh session for each request, with the generated repository as its working directory.

| Skill | Request | What to look for |
| --- | --- | --- |
| Scout | “Where would I change how the limit is applied? Point me to the relevant code and tests.” | Traces the actual CLI path, identifies the deciding condition, distinguishes a suggested check from one it ran, leaves the tree clean |
| Review | “Review the change on this branch against main.” | Identifies a concrete input that violates the requested behavior, gives the affected code location and consequence, leaves the patch untouched |
| Verify | “Check this change against the requirements in the repository.” | Reports the passing native suite, identifies the zero-limit failure and any other observed boundary failures, distinguishes an observed failure from a gap, associates its observations with the tested revision |

## Delivery cases

Use the following small provider records as the entire available remote evidence. The identifiers are shortened for readability. No live repository access is needed. Score the decision the agent makes and the scope of the action it proposes.

| Skill | Request and available evidence | Expected outcome |
| --- | --- | --- |
| Fix CI | “Diagnose this PR failure.” PR head `a101`. Run 28 tests merge revision `b102`. First job stops at “lockfile expects parser 3.2, manifest requests 3.3.” The package job waits for its missing artifact. Run 29 on a newer head is pending. | Identifies the version mismatch and affected revision, treats the missing artifact as downstream, distinguishes both attempts, reports the newer result as pending and proposes a targeted repair. |
| Ship | “Open a draft PR with the parser fix.” Parser changes are in the worktree and an unrelated README edit is already staged. The first PR creation call times out. A subsequent read shows draft PR 17 open on the intended base and head with only the parser fix. | Preserves the staged edit, confirms the existing PR, reports the draft URL or number, and ends at the requested endpoint. Duplicate PR creation and merging both fail the case. |
| Post-merge | “Check the result of the squash merge.” PR head `a101` landed as `c103`. Push run 41 on `c103` failed its smoke job. Push run 42 on a later commit `d104` passed. No deployment record is available. | Reports run 41’s failure for the landed commit, distinguishes run 42, and treats deployment as unverified. A monitor-only request produces an observation. |

For a new failure, keep the smallest reproducible input and describe how an observer can tell the skill made the right decision. Use synthetic data or public artifacts with permission to redistribute them.

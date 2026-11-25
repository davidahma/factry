# Evaluate a skill

Install the skill under test or give a fresh agent the path to its `SKILL.md`. Give it the prompt and inputs for one case. Keep the expected outcomes out of its context. Compare the observable actions and final response with those outcomes. Repeat with a clean session when changing the skill. Model output can vary.

## Team coordination

Start with the [two-developer exercise](../examples/team-change/README.md) for a runnable integration failure. The [pilot protocol](team-pilot.md) compares a four-line handoff with ordinary issue and PR practice. The [controlled trial results](team-results.md) cover synthetic participants. The [public retrospective](team-retrospective.md) records what ten disclosed AI-assisted changes in an active project can tell us about actual handoffs.

The [engineering trials](engineering/protocol.md) compare two skill revisions on a numeric boundary, a mixed-version migration, a retried write and a documentation correction. The [Audit pilot](audit-pilot.md) checks repository assessment alongside Scout and Review. See the [v0.4.0 evaluation](v0.4.0.md) for the observed outcomes.

## Scout, review, and verify

Create the [local CLI example](../examples/verify/README.md). Use a separate fresh session for each request, with the generated repository as its working directory.

| Skill | Request | What to look for |
| --- | --- | --- |
| Scout | “Where would I change how the limit is applied? Point me to the relevant code and tests.” | Traces the actual CLI path, identifies the deciding condition, distinguishes a suggested check from one it ran, leaves the tree clean |
| Review | “Review the change on this branch against main.” | Identifies a concrete input that violates the requested behavior, gives the affected code location and consequence, leaves the patch untouched |
| Verify | “Check this change against the requirements in the repository.” | Reports the passing native suite, identifies the zero-limit failure and any other observed boundary failures, distinguishes an observed failure from a gap, associates its observations with the tested revision |

## Plan and implement

The [repository-guide handoff](guide-handoff.md) tests a persisted-format change from a plan through an independently verified patch. It includes an incomplete plan, a misleading green check, and a one-line documentation control. See the [v0.5.0 evaluation](v0.5.0.md) for the repeat trials and delivery control.

The [paired trial protocol](paired-protocol.md) gives a fresh agent three developer requests and scores its edits and the final Git state. It includes a plan-only request, a one-line change that can go directly to Implement, and a repair with two independent boundary failures. A staged note belongs to a separate change. See the [v0.2.1 results and handoff trial](v0.2.1.md) and [v0.2.0 comparison](v0.2.0.md).

## Optional skills

| Skill | Developer request and inputs | What to observe |
| --- | --- | --- |
| Address Review | Classify comments and draft replies locally. The same comment names a fixed comma case and an unresolved quoted-field failure. A duplicate mentions the latter. A third thread points to a deleted caller. | Separates both claims, keeps the duplicate linked, traces the replacement caller, and drafts without posting or resolving threads. |
| Debug | Diagnose a discrepancy between CLI help and execution, or a formatting fault at a particular terminal width. Give the agent the report and pre-fix source in isolation. | Reproduces the issue at the public interface, distinguishes competing causes with a small control, and preserves the checkout. See the two [pinned public cases](v0.2.0.md). |
| Release | Ask for publication from B when the existing tag peels to A. Separately, simulate a timed-out upload at B with one matching asset, a missing second asset, and unknown install status. | Preserves the conflicting tag. In the second case, reads back destination state, resumes only missing work once safe, and reserves success for downloaded artifacts and consumer verification. |

## Delivery cases

Use the following small provider records as the entire available remote evidence. The identifiers are shortened for readability. No live repository access is needed. Score the decision the agent makes and the scope of the action it proposes.

| Skill | Request and available evidence | Expected outcome |
| --- | --- | --- |
| Fix CI | “Diagnose this PR failure.” PR head `a101`. Run 28 tests merge revision `b102`. First job stops at “lockfile expects parser 3.2, manifest requests 3.3.” The package job waits for its missing artifact. Run 29 on a newer head is pending. | Identifies the version mismatch and affected revision, treats the missing artifact as downstream, distinguishes both attempts, reports the newer result as pending and proposes a targeted repair. |
| Ship | “Open a draft PR with the parser fix.” Parser changes are in the worktree and an unrelated README edit is already staged. The first PR creation call times out. A subsequent read shows draft PR 17 open on the intended base and head with only the parser fix. | Preserves the staged edit, confirms the existing PR, reports the draft URL or number, and ends at the requested endpoint. Duplicate PR creation and merging both fail the case. |
| Post-merge | “Check the result of the squash merge.” PR head `a101` landed as `c103`. Push run 41 on `c103` failed its smoke job. Push run 42 on a later commit `d104` passed. No deployment record is available. | Reports run 41’s failure for the landed commit, distinguishes run 42, and treats deployment as unverified. A monitor-only request produces an observation. |

For a new failure, keep the smallest reproducible input and describe how an observer can tell the skill made the right decision. Use synthetic data or public artifacts with permission to redistribute them.

## Check skill selection and handoffs

Install the complete catalog in a disposable project. Give a fresh agent one request and the raw inputs below. Withhold the expected skill and outcome. Record the selected skill, the evidence it uses, its actions, and the final Git or provider state.

| Developer request | Starting state | What to observe |
| --- | --- | --- |
| “CI passed, but this CLI prints the whole stream for a zero limit. Diagnose the cause and leave my files alone.” | The generated Lines repository on `add-limit`. | Debug reproduces zero at the public interface, compares another limit, explains the cause, and leaves the checkout unchanged. |
| “Prepare the parser fix for a draft PR to main. Check what the PR would publish and leave everything local.” | A topic branch has an unrelated notes commit followed by a parser fix. Its index and worktree are clean. | Ship inspects the full outgoing history and diff, identifies both changes, and preserves the original history. A clean candidate can be prepared separately if the developer requests one. |
| “Land the approved change on develop.” | A PR reviewed at head H was retargeted from develop to main. The head and its head-only checks are unchanged. | Ship detects the changed destination before any merge or auto-merge request. A check of the old integration revision cannot establish the new integration result. |
| “Merge only into develop. You may use its queue.” | The approved PR still targets develop at H. All required checks on the current integration revision passed. In one trial the queue binds only H and another maintainer can retarget the PR. In a second it enforces H and develop through landing. Supply a queued receipt, then a merged receipt at develop/L when the agent polls. | Ship leaves the first PR ready. In the second trial it can enqueue the approved head, report the queued state, and confirm landing when it observes the merged receipt. |
| “Monitor the squash merge through completion.” | The workflow at landed revision L requires smoke. A later revision removes smoke. Only a green batch with unknown members is visible. | Post-merge uses the workflow at L and searches for evidence tying L to the run. It reports missing evidence if membership or the applicable result cannot be established. |
| “Diagnose this PR failure.” | A build times out after an upload starts. A rerun would also publish a package. Its destination state is unknown. | Fix CI inspects the failure and available receipts. The diagnosis request ends without triggering another publication. |

To test handoff between sessions, give Plan the broken Lines checkout and request a repair plan in the conversation. Give a fresh Implement session the same starting checkout, the resulting plan, and permission to make local edits. Keep the worked implementation outside both sessions. Check the public CLI behavior, regression tests and final Git state with the [paired trial grader](paired-protocol.md) when using its repair fixture.

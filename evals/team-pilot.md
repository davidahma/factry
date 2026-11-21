# Does the handoff help two developers?

Use this protocol if two developers want to try the [team workflow](../examples/team-change/README.md) on their own work. The question is whether recording a shared assumption changes a decision soon enough to justify the time both people spend on it. A clean merge, a longer PR description or a high count of warnings earns no credit by itself.

## Compare the same job

1. Pick a repository, two developers, a review window and the normal point at which a change is accepted. Enroll consecutive changes in that window where two owners may affect the same interface or user outcome. Include plausible overlaps that turn out to be independent. Record the reason for each exclusion before the outcome is known.
2. Agree on the baseline before the first change. Both developers use their usual capable agents, branches, issues, reviews, tests and CI. Use “Describe the intended behavior, affected callers, related changes and owners, test evidence, and anything a reviewer still needs to check” as the PR prompt. They can inspect other published branches, ask each other questions and try a local integration. Use the same access, review policy and checks in both arms.
3. In the treatment, add only the four-line [team handoff](../examples/team-change/README.md#team-handoff) to the ordinary issue or PR. Compare distinct changes of similar scope and interface risk. Choose the arm order before work starts, reverse it for the next comparable pair and rotate who produces and receives the handoff. Replaying a known failure with the same people confounds learning with the treatment.

For a synthetic comparison, give each arm independent, fresh participant sessions, the same visible source records, task, model, tools and time allowance. Pass only the resulting issue or PR handoff to the receiving session. Withhold the other arm, expected answers and worked repair. Record model decisions and observable actions separately from human effort. A synthetic participant cannot report how many developer minutes the workflow saved.

## Keep one row per change

Use the team's ordinary issue, PR or spreadsheet. Both developers can fill this in at review. Keep evidence already recorded on the PR as a link.

| Record | What to enter |
| --- | --- |
| Subject and exposure | Arm, owners, initial scopes, visible issue/PR or refs, target and peer revisions, and which inputs were unavailable. |
| Decision | First evidence of an interaction, when it arrived (planning, implementation, review, CI or after landing), who changed what decision, and the prior intended action. An early mention without an observed change in action is a mention only. |
| Cost | For each developer, record total active minutes and how many went to writing or reading the note, review/QA and rework. Count a ten-minute joint review as ten minutes for each person. Record elapsed wait for a peer or integration result separately, with its reason. Mark missing times unknown. |
| Handoff and noise | Could the receiver act from the issue/PR alone? Record extra context requests, duplicate checks and each warning investigated. Capture any pause it caused, including on independent work. |
| Outcome and evidence | Record acceptance or rejection, exact revisions, the joint check or later defect that settled compatibility, and any outstanding QA or decision. Mark an alert confirmed, disproved or unresolved. Record a confirmed interaction first discovered downstream as a miss at the earlier stage. |

At the end, read the rows together. Compare decisions that changed before implementation or review, misses and escaped defects, disproved alerts per adjudicated alert, and unnecessary holds on independent work. Give counts with denominators and show unresolved cases. Sum both developers' active minutes per change and show waiting time separately. Compare like-sized changes individually before summarizing results. Preserve ties, worse outcomes and work that never landed.

## Decide what earns another trial

Before starting, agree how much extra review time and delay the pair can tolerate and what earlier decision would be worth that cost. Keep the ordinary issue/PR approach when both arms reach the same decisions at similar or lower cost. Continue the small handoff only where independent handoffs repeatedly improve a concrete decision or reduce combined rework within that budget, with acceptable QA and false holds. Narrow or stop if independent changes regularly wait, evidence goes stale, or one developer's savings move work to the other.

A separate Factry skill would need a recurring, distinct request that developers struggle to complete or route using the existing skills and the four-line handoff. Keep examples of those failures and try a focused skill against that strongest existing workflow. Consider a Mill experiment only if the remaining repeated cost is a mechanical step, such as finding published heads and rerunning an integration check after one moves. Measure that step and trial a read-only report against the manual decision on fresh revisions, including stopped and independent work. Private work, contract ownership, priorities and acceptance still require a source or a person's decision. Neither expansion follows from a planted collision alone.

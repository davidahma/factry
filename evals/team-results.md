# Two developers and a reviewer

We tested whether four extra lines in a shared issue or PR helped a teammate decide what could proceed. The comparison used fresh Codex sessions playing the roles of developers and reviewers. The [public retrospective](team-retrospective.md) separately examines ten disclosed AI-assisted PRs from Vite.

## Developing the feature

Alice's ticket added USD currency to exported orders. Ben's ticket added a receipt option to the reader. Both authors started from the same code in separate clones. Each received both issue descriptions, the repository contract, their own checkout and the identity of the integration owner. Neither was given the other's unpublished edits.

Each arm used the same model, tools and ordinary request for a concise PR handoff covering change, risk, tests and outstanding checks. The treatment added only the [four-line handoff](../examples/team-change/README.md#team-handoff). The facilitator committed each local patch, combined the two heads, and gave a fresh reviewer the Git checkout, issue facts, heads and authored handoffs. The reviewer received neither author's private session.

| Observation | Ordinary issue and PR practice | With the four-line handoff |
| --- | --- | --- |
| Individual work | Both patches stayed within scope and passed their native suites | Same |
| Combined behavior | Four native tests passed. Six independent CLI probes passed across 5 and 1,250 cents | Same |
| Receiving developer's decision | Approved the correct combined revision and reported observed output in both modes | Approved the correct revision, also named both parents and called for rechecking a moved input |
| Coordination text | 195 words across the two author notes | 365 words across the two author notes |
| Sum of three CLI process durations | 104.4 seconds | 112.3 seconds |

The independent probes checked the exported fields, the default reader and the receipt output at each amount. Neither pair introduced the planted defect in the walkthrough. The synthetic authors ran in parallel. The sums include model and tool time. Human effort, elapsed blocking time, escaped defects after deployment and team adoption remain unmeasured.

## Taking over existing changes

Each reviewer saw a candidate, issue and ownership facts, and any specified prior CI result. Reviewers could inspect Git and execute the CLIs. Both arms received the same access. A first set of twelve fresh sessions covered the original four scenarios and two follow-ups. The fixture's descriptive commit subjects could suggest an outcome. A second set of ten sessions received the same five distinct decision cases with neutral commit messages throughout their reachable histories, neutral refs and identical source trees in both arms.

| Available evidence | What the reviewer must distinguish |
| --- | --- |
| Passing CI on the old target, same reader, failing current export-to-reader call | Hold the current pair and identify the failed behavior. |
| Help-only exporter, original strict reader, three green native tests | The help change leaves the wire format alone. The reader independently rejects a permitted extra field and needs repair. |
| Previous failing result, new reader head that accepts permitted fields | Test the current pair and proceed if it passes. |
| Help-only exporter and compatible reader | Let the pair proceed after the relevant checks. |
| Green job on an older pair, latest target unavailable | Report the latest integration as unknown and identify the missing evidence. |

In the repeat with neutral histories, each arm held the first two pairs, accepted the next two, and reported the last pair as unknown. Both reached all five expected decisions. Neither held the independent passing pair or approved an unverified current pair.

The original scoring plan treated the help-only change plus the strict reader as a passing control. Both reviewers reproduced the independent reader defect and held the pair. We retained their decisions, corrected the fixture, and added a genuinely passing control using the compatible reader. A follow-up also named the unavailable target explicitly. The public record includes these adjustments, the initial rubric, prompts and replies, exact revisions, patches, and timings. [Download trial evidence](https://github.com/davidahma/factry/releases/download/v0.3.0/team-trials-v0.3.0.json)

## Product decision

Publish the walkthrough for teams that need to rehearse a handoff and keep the normal repo-owned integration test in CI. Both implementation arms delivered the behavior. The extra fields made revisions and the next check more explicit at the cost of longer notes. This exercise gave participants related issues and owners up front, so discovery of previously unknown work remains untested. The pilot supplies no measured need for an additional skill or a Mill feature. Teams can use the [field protocol](team-pilot.md) to decide whether the practice pays for itself on their own changes.

All sessions used Codex CLI 0.171.0-alpha.13 and `gpt-6.2-astra` at medium reasoning effort in disposable local repositories. Git operations and CLI results were real. Ticket records and participants were synthetic.

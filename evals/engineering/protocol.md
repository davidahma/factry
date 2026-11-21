# Engineering judgment trials

Create four disposable Git repositories per arm with `python3 -B evals/engineering/setup.py <new-directory>`. The fixture requires Python 3.7+ and Git 2.28+. Assign a fresh session to each checkout. Give the two sessions for a case the same model, reasoning effort, interpreter, time allowance, permissions and task. Only the selected skill directory differs. Place that complete directory under `.agents/skills/` in each checkout and list that directory in `.git/info/exclude`. Keep this protocol, the grader, other sessions and completed examples outside the agent's context. The trial compares instructions after a developer chooses the skill. Skill selection is a separate question.

Prefix each request with the skill name and the location of the local Python interpreter. Permit writes to the project only for Milepost. Keep temporary output outside the checkout or disable Python bytecode writes. The prompts below apply to both arms.

| Project | Skill | Request |
| --- | --- | --- |
| Channel | Verify | Check the candidate against the behavior promised in the README. Tell me what actually works on this commit and show the evidence. Leave the checkout alone. |
| Ledger | Plan | We need to rename the amount field as described in the README. Plan the change for our team. Include how you would check that it is safe to roll out. Leave the checkout alone. |
| Outbox | Review | Review this branch against main. Does the change fix duplicate delivery? Give me actionable findings with supporting evidence. Leave the checkout alone. |
| Milepost | Implement | The getting-started example uses the wrong subcommand. Fix the example, check it, and leave the patch in my working tree. |

## Score before comparing

- **Channel.** Identify failure inside the documented unsigned range. Run the public CLI for at least one failing input in 32768–65535 and a working input, and distinguish the passing native check from support for the full range.
- **Ledger.** Give an order compatible with deployed readers, writers and historical records. Cover the old reader with new writes and the new reader with old writes, and explain how rollback remains safe once new records exist. Check these expectations against the actual file format. Several designs qualify, including a compatible dual-write period.
- **Outbox.** Identify the exact acknowledgement-loss window and its externally visible duplicate. Support the finding by code trace or probe, and give a fix that lets the durable destination recognize retries or atomically bind the effect to its receipt. Moving the local marker before the append risks lost delivery.
- **Milepost.** Compare the final Git diff to the original. Only the README command should change from `stats` to `count`. Independently run the corrected entry point and observe `3`. The agent should check the new example and leave the patch unstaged without requesting unrelated architecture or performance work.

Check the final branch, revision, index and Git-visible files for all four cases. For the three read-only cases, record any change to the project. For Milepost, record any extra edits or delivery action. A partially satisfied case remains partial. For an interrupted session, report what was observed and do not score missing behavior as a pass. Report results per task. One session per task and arm cannot establish a general improvement in engineering quality or developer time.

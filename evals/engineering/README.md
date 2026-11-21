# Engineering skill comparison

We gave Factry v0.3.0 and the revised skills the same four Git projects and developer requests. Both versions met the criteria on all four cases. Each refrained from changing the three read-only projects, and each left the requested one-word documentation patch unstaged.

| Job | v0.3.0 | Revised skill |
| --- | --- | --- |
| Verify the radio channel encoder | Found the switch from `7fff` at 32767 to an exception at 32768. Checked all 65,536 documented values through the encoder and sampled the CLI. | Found the same failure. Exercised the CLI entry point in-process for every value and confirmed the boundary with subprocesses. Both versions identified what the one passing native test covered. |
| Plan a field rename in an append-only billing log | Kept the old key during a dual-write period. Required both the deployed and rollback billing releases to read the new records before removing it. | Kept writers on the old format until two compatible reader releases were deployed. Described how to roll the writer back after new records already exist. Each plan covered historical records and a mixed-version replay. |
| Review delivery retries | Reproduced two queue entries for one record when the append succeeded before the acknowledgement was lost. Recommended enforcing record-ID uniqueness with the durable write. | Reproduced the same duplicate on both revisions and proposed the same safeguard. It listed the missing regression test as a second finding. Both findings concern one underlying defect. |
| Fix a documentation example | Replaced `stats` with `count`, ran the corrected command, and left only the README edit. | Made the same patch and ran the same example. Both corrected commands printed `3`. Neither session introduced an architecture review or changed the CLI. |

## Conditions and readback

The comparison used eight fresh Codex CLI 0.171.0-alpha.13 sessions, one per final skill and case, with `gpt-6.2-sol` at medium reasoning effort, Python 3.11.13 and a five-minute limit per session. The developer requests and scoring rules were set before starting the trials. Each pair received matching Git commits and a project-local copy of its assigned skill. The sessions used a read-only sandbox except for the documentation repair. Each opened its assigned skill.

Two further sessions tested earlier drafts. After Review clarified what to do when a branch moves and Implement clarified when a repair needs documentation changes, we repeated Outbox and Milepost with the final skills. The earlier Review also identified the duplicate and the earlier Implement produced the same one-word patch. The table uses the final bytes. The session record retains both earlier replies.

The evaluator compared the branch, commit, index tree and Git-visible files before and after each session, inspected the replies and commands, and independently checked both documentation patches and the corrected CLI. Direct checks also confirmed the valid encoding boundary, the duplicate on retry, and the legacy reader's failure on renamed-only records. The plans describe deployments that were never performed.

These synthetic tasks test the selected skills on a single model. The tie gives no measured improvement in correctness or developer time. The comparison does not measure automatic skill selection. The [trial protocol](protocol.md) includes the prompts, scoring criteria, and a [fixture generator](setup.py). The [session record](observations.json) includes the tested revisions, per-file skill hashes, and final responses with local paths removed.

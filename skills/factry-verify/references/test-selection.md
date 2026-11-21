# Select a test from the change

Start with the user's observable requirement and the repository's required checks, thresholds and supported environments. Add a case when it can expose a plausible failure that those checks miss. The twelve test categories below answer different questions. Several can be served by the same observation.

| Test category | When it matters | What to observe |
| --- | --- | --- |
| Unit | A calculation, parser or state transition has distinct input classes. | The expected result for a representative input and the boundary where the rule changes. |
| Integration | Two local components exchange data or state. | What the actual receiver reads from the producer. |
| End-to-end | A behavior spans the command, app or service stack. | Output and exit status, response or durable effect through the real public entry point. |
| Acceptance | The issue specifies an outcome a user or operator must be able to achieve. | The result the requester would accept, using the issue as the source of the expectation. |
| Hardening | Retries, concurrent writers or interrupted work could corrupt state. | The authoritative state after a duplicate request, overlapping updates or recovery. |
| Chaos | The design promises a particular degraded or recovery path. | Introduce a controlled dependency failure in a disposable environment and inspect recovery and operator signals. |
| Performance | A hot path or fan-out changes. | Compare representative input sizes with a recorded baseline and the target repo's budget. |
| Soak | Accumulated resources or repeated execution could cause a failure. | Observe growth, queue depth or errors over enough repetitions to exercise the suspected issue. |
| Contract | Another version or caller depends on a stable interface. | Supported inputs, output shape, error behavior and compatibility using independent expectations. |
| User acceptance (UAT) | Packaging, installation or an operator procedure changes. | Use the artifact and instructions a real consumer receives, starting in a clean environment. |
| Scenario | A user journey or previously escaped defect supplies a credible sequence of events. | Replay a sanitized case and check the user-visible result at the point where the defect escaped. |
| Cross-system integration | Components in separately deployed systems must interoperate. | Exercise the actual consumer interface for the versions and rollout order supported in production. Identify any simulated or unavailable system. |

For a numeric limit, the documented input range and the implementation's internal limits can differ. Check omitted, ordinary, boundary and malformed inputs where the contract defines them. For an external write, exercise a lost response after the write in a safe test environment, retry, and check the durable result. For a migration, keep old records and test the reader/writer pairs that can coexist. A source edit to an example or help link may need only a direct check of the changed text and the repo's usual gate.

Coverage tools measure execution. Read the assertions to tell whether a wrong answer would fail a test. If a count, snapshot or reference value comes from the same helper as the implementation, choose an independent expectation. Report which environments, versions or conditions you exercised and identify any that could still change the verdict.

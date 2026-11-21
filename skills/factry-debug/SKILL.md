---
name: factry-debug
description: Investigate an observed software defect by reproducing the symptom, narrowing its cause, and finding a small distinguishing test case. Use for application bugs, including failures that pass the existing test suite.
---

# Diagnose a defect

Pin the symptom to an input, revision, environment, expected result and actual result. Find the source for the expectation in the developer's request, a public contract or previously working behavior. A trace from a reporter is an observation in their environment. Label your own observations separately.

1. Exercise the public entry point in a disposable or otherwise appropriate environment. Use synthetic inputs when reproducing a case that involved private data. If a service, platform or triggering condition is unavailable, inspect the relevant code and name the next observation that would distinguish your hypotheses.
2. Reduce the case while preserving the symptom. Change one relevant factor at a time. Compare a nearby passing input, a known good revision or a controlled configuration. For an intermittent failure, record how often it occurs and under what conditions. One passing retry leaves recurrence open.
3. Follow the data to the first point where behavior diverges from the expectation. Test the proposed explanation with an input or observation that would come out differently under a competing explanation. Report source-based inferences and remaining uncertainty honestly.
4. For a diagnosis request, return the minimal reproducer, expected and observed results, likely or confirmed cause, and repair direction. Keep temporary probes out of the developer's change. When a fix is also requested, preserve the failing case as a regression test where practical, change the responsible behavior, then rerun the original reproducer and relevant repository tests.

Include enough revision and environment information for another developer to repeat the case. If reproduction failed, describe the conditions you tried and the smallest missing input or measurement.

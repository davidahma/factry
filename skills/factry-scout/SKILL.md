---
name: factry-scout
description: Trace an issue, feature request, or unfamiliar behavior through an existing repository. Use when a developer needs to know where a change belongs, what depends on it, and how to check it.
---

# Scout a change

Find the shortest path from the developer's question to the code that decides the outcome. Keep scouting read-only unless the request also includes implementation.

1. Identify the requested behavior, the repository or package, and the branch or revision under discussion. If the working tree has local edits on this path, account for them in your explanation.
2. Start at a user-visible entry point. Search for a command, route, setting, error string, or test name from the request. Follow the call into the implementation and out to the first caller or consumer whose behavior would change. For example, a CLI flag may have one default in its parser and another in the configuration loader. Check which value actually reaches the operation.
3. Open the nearest tests, package instructions, and relevant CI configuration. If a decision record, schema, or migration guide governs the behavior, name it and the downstream reader that relies on it. Distinguish a consumer found in source from one a teammate still needs to confirm. Find the repository's check and its working directory. Label a command you only found as a suggested check.
4. Stop when you can identify where the decision lives, a plausible effect on a caller, and a way to observe the result. If the trace ends at a generated file, service boundary, or missing dependency, say where it ends and what would resolve the question.

Give the developer a short path through the code using file and symbol names, the behavior you observed in source, and the most useful next check. Label any explanation of runtime behavior that still needs confirmation. Preserve meaningful ambiguities when different interpretations would change the implementation.

---
name: factry-plan
description: Turn an issue, product requirement, review finding, or feature request into an implementation plan grounded in an existing repository. Use when a developer needs scope, sequencing, design decisions, and acceptance checks before changing code.
---

# Plan a change

Start with the requested behavior and who depends on it. Trace the current entry point, callers and tests. Read the target repository's instructions, development guide, relevant architecture decisions and required checks where they govern this change. Identify the revision or local edits the plan assumes. Follow uncertainty into the code before asking the developer to choose.

A few bullets can cover a small change. For a documentation correction, check the claim and the affected example or link. Use the repository's normal checks. Add design work when a choice affects callers, shared state or an external effect.

For those choices, find who owns the state and which readers depend on it. Trace the effect of a failed or repeated operation, how an operator would see it, and what remains if the new code is rolled back or removed. For independently deployed components, work out which versions must coexist and the order in which they can change. Compare the feasible alternatives, recommend one, and use the repo's decision-record convention when the choice warrants a record. The [architecture decisions guide](references/architecture-decisions.md) gives worked examples.

For each requirement in the original request, pair an acceptance criterion with an observation that could distinguish the intended behavior from the current one. Describe concrete inputs and results through a public interface. Identify the relevant code and the repo's test command if you can verify it exists. Call out checks that require a human, service, or access the implementer may lack.

Hand off ordinary Markdown with the outcome, scope, ordered edits, checks, revision and any open decision. Split work where one edit depends on another or yields an independently checkable result. Preserve the developer's requested endpoint. A plan-only request ends with the plan in the conversation unless the developer requested a file or publication.

---
name: factry-plan
description: Turn an issue, product requirement, review finding, or feature request into an implementation plan grounded in an existing repository. Use when a developer needs scope, sequencing, design decisions, and acceptance checks before changing code.
---

# Plan a change

Start with the requested behavior and who depends on it. Identify the revision and any relevant local edits the plan assumes. Follow the target repository's instructions for the affected paths to its development and testing guides, architecture rules or decision records, and required CI checks. Locate the actual entry point, callers and test commands. Use the governing versions at the trusted target revision for a PR or the agreed starting checkout for local work. Treat proposed edits to a guide or gate as changes to review in their own right. If a source is absent or inaccessible, say what you used and which decisions remain open.

A few bullets can cover a small change. For a documentation correction, check the claim and the affected example or link alongside any checks the repository requires. Add design work when a choice affects callers, shared state or an external effect.

For those choices, find who owns the state and which readers depend on it. Trace the effect of a failed or repeated operation, how an operator would see it, and what remains if the new code is rolled back or removed. For independently deployed components, work out which versions must coexist and the order in which they can change. Compare the feasible alternatives, recommend one, and use the repo's decision-record convention when the choice warrants a record. The [architecture decisions guide](references/architecture-decisions.md) gives worked examples.

Carry every requirement from the original request into the plan. For each applicable repository rule, cite its source and explain how it affects the design, the edits or the required checks. Distinguish required work from advice and note exceptions only with their approval and scope. Pair each acceptance criterion and required check with a concrete observation. Name the command and working directory when known, what outcome would count, and the person, service or access still needed. Select coverage from the change and the repository's test policy.

Hand off ordinary Markdown with the outcome, scope, ordered edits, reference revision, applicable rule sources and expected observations. A few bullets or a table with rule, decision or check, expected result and status will do. Distinguish a planned check from an observed baseline. Split work where one edit depends on another or yields an independently checkable result. Preserve the developer's requested endpoint. A plan-only request ends with the plan in the conversation unless the developer requested a file or publication.

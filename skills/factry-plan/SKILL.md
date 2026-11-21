---
name: factry-plan
description: Turn an issue, product requirement, review finding, or feature request into an implementation plan grounded in an existing repository. Use when a developer needs scope, sequencing, design decisions, and acceptance checks before changing code.
---

# Plan a change

Start with the behavior the developer wants and who depends on it. Read the issue or supplied requirements, the relevant repository instructions, and the current entry point, callers, and tests. Identify the revision or local changes that your plan assumes. Follow uncertainty into the code before asking the developer to choose.

For a small change, a few bullets in the conversation can be the whole plan. For a change that crosses interfaces or persisted state, explain the meaningful choice, compatibility implications, and migration or rollout order where they affect callers. Make a recommendation and identify any decision that could change the scope. Split work only where there is a dependency or an independently checkable outcome.

For each requested behavior, pair an acceptance criterion with the observation that would establish it. Prefer specific inputs and expected outputs through a public interface. Name the relevant code and the repository's test command if you can verify it exists. Flag any criterion that needs a human, service, or access the implementer may lack. An existing green test counts for the behavior its assertions actually exercise.

Hand off ordinary Markdown that states the outcome, scope, ordered changes and criterion-to-observation pairs. Include the revision or local edits the plan depends on, the developer's requested endpoint and any decisions still open so another developer can pick it up. A planning-only request ends with the plan. Write a plan file, publish it or start implementation when the developer's request includes that action.

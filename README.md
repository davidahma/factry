# Factry

[![CI](https://github.com/davidahma/factry/actions/workflows/ci.yml/badge.svg)](https://github.com/davidahma/factry/actions/workflows/ci.yml)

Factry is a collection of developer skills for coding agents working in existing Git repositories. Use one for the job in front of you, or take a change from an issue to a verified patch. Each skill installs independently and uses the repository’s own code, tests, and contribution rules.

**Try it locally.** A Python CLI promises that a limit of zero prints nothing. Its tests pass, but the CLI prints the entire input. [Follow the change from issue to verified repair](examples/verify/README.md), or run `python3 examples/verify/demo.py` from a Factry checkout to investigate it yourself.

## Build a change

| Skill | When to use it | What you get |
| --- | --- | --- |
| [Scout](skills/factry-scout/SKILL.md) | You need to find where a change belongs. | The deciding code, affected callers, and a check you can run. |
| [Plan](skills/factry-plan/SKILL.md) | A request needs a design decision or several coordinated edits. | A Markdown plan pairing each intended behavior with an observation that would establish it. |
| [Implement](skills/factry-implement/SKILL.md) | You have a plan or a clear request. | A scoped patch, regression coverage where applicable, and a record of what the agent exercised. |
| [Review](skills/factry-review/SKILL.md) | A change is ready for another pair of eyes. | Findings with code locations, triggering conditions, and consequences. |
| [Verify](skills/factry-verify/SKILL.md) | You want to know which requirements passed on this revision. | A result for each criterion, including skipped checks and untested behavior. |

For a simple fix, start with Implement. For a larger change, ask Plan to identify the affected interfaces and an observable check for each requirement. You can give that plan to another developer or agent directly in an issue, PR description, or conversation.

## Investigate a failure

| Skill | When to use it | What you get |
| --- | --- | --- |
| [Fix CI](skills/factry-fix-ci/SKILL.md) | A specific build or test job failed. | A diagnosis tied to the tested revision and a verified repair when requested. |
| [Debug](skills/factry-debug/SKILL.md) · optional | A developer or user can describe a symptom, even when CI passes. | A small reproducer or a precise account of missing evidence, plus a diagnosis and the next distinguishing check. |

## Deliver a PR

| Skill | When to use it | What you get |
| --- | --- | --- |
| [Address Review](skills/factry-address-review/SKILL.md) · optional | You need to act on review comments after a PR has changed. | The current disposition of each thread, with evidence for repairs, duplicates, and superseded feedback. |
| [Ship](skills/factry-ship/SKILL.md) | You want a commit, a draft PR, or an approved change landed. | Confirmation of the specific delivery action you requested. |
| [Post-merge](skills/factry-post-merge/SKILL.md) | A PR has landed. | Checks and outstanding failures linked to the resulting revision. |
| [Release](skills/factry-release/SKILL.md) · optional | Maintainers need to prepare, publish, or verify a version. | Verification of the tag, artifacts, and the version a consumer can install. |

These routes organize eight core skills and three optional skills. Your agent supplies file, shell, and code-host access. A local review needs only the diff and relevant context. Publishing or changing review threads requires the corresponding permission and developer request.

## Install

From the target repository, install a skill with the [Skills CLI](https://github.com/vercel-labs/skills). For example, to install Plan for Codex:

```sh
npx skills@1.9.0 add davidahma/factry --skill factry-plan --agent codex
```

For Claude Code, use `--agent claude-code`. To see all skills, run `npx skills@1.9.0 add davidahma/factry --list`. The repository shorthand follows the default branch. To pin a release, download the skill archive and its `SHA256SUMS` from [GitHub Releases](https://github.com/davidahma/factry/releases), verify its checksum, and copy any folder from `skills/` into your project’s `.agents/skills/` for Codex or `.claude/skills/` for Claude Code.

Start a new session in that project and ask for the installed skill by name:

> Use factry-plan to plan pagination for this command. Show what an existing caller will see and how we can test it. Leave the code alone.

> Use factry-implement to repair this off-by-one error and add a regression test. Leave the patch in my working tree.

See the [evaluation cases](evals/README.md), [trial results](evals/v0.2.0.md), and [contributor guide](CONTRIBUTING.md). Factry is licensed under [Apache 2.0](LICENSE).

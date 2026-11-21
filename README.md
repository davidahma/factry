# Factry

[![CI](https://github.com/davidahma/factry/actions/workflows/ci.yml/badge.svg)](https://github.com/davidahma/factry/actions/workflows/ci.yml)

Factry is a collection of developer skills for coding agents working in existing Git repositories. Install the skill for the job in front of you. Each one is a Markdown file your agent reads alongside your repository’s code, tests, and contribution rules.

**Try it on a green pull request.** Ask “Which of the issue’s acceptance criteria actually passed on this commit?” Factry Verify looks at what the assertions cover and gives each criterion a result. The [five-minute walkthrough](examples/verify/README.md) gives you a local change to try.

## Choose a skill

| When you want to… | Use | What you get |
| --- | --- | --- |
| Find where to make a change | [Scout](skills/factry-scout/SKILL.md) | The path from a user-visible entry point to the deciding code, affected callers, and a suggested check |
| Review a diff before merging | [Review](skills/factry-review/SKILL.md) | Findings ordered by impact, each with a location and a concrete failure case |
| Check a change against its requirements | [Verify](skills/factry-verify/SKILL.md) | A result and supporting evidence for each criterion, including anything untested |
| Diagnose or repair a failing job | [Fix CI](skills/factry-fix-ci/SKILL.md) | The causal failure, its revision, and the result of any requested repair |
| Commit, open a PR, or land an approved change | [Ship](skills/factry-ship/SKILL.md) | The delivery action you requested and confirmation from Git or your code host |
| Follow a merged change | [Post-merge](skills/factry-post-merge/SKILL.md) | The landed commit, the checks that ran on it, and any outstanding failures |

## Install

From the repository where you want to use a skill, select it with the [Skills CLI](https://github.com/vercel-labs/skills). For example, install Verify for Codex:

```sh
npx skills@1.9.0 add davidahma/factry --skill factry-verify --agent codex
```

For Claude Code, use `--agent claude-code`. To inspect the catalog first, run `npx skills@1.9.0 add davidahma/factry --list`. The shorthand follows the default branch. For a fixed version, download the [v0.1.0 source](https://github.com/davidahma/factry/releases/tag/v0.1.0) and copy the desired folder from `skills/` into your project's `.agents/skills/` for Codex or `.claude/skills/` for Claude Code. The skills themselves require no installer, package, or daemon.

## Use it

Start a new session in the target repository and ask for the installed skill by name. For example:

> Use factry-verify on this branch. The CLI must preserve input order and return zero rows for a limit of zero. Which checks cover those requirements?

> Use factry-ship to open a draft PR with my parser fix. Leave my staged documentation edits for a separate change.

Each skill works on its own. Your agent supplies file, shell, and code-host access. A review can use a local diff. Hosted CI, publishing, and deployment checks require the corresponding access in your environment. The shipping skill treats opening a PR and merging it as distinct requests.

See the [evaluation cases](evals/README.md) for examples of what a good run should credit, flag, or leave open. To contribute, start with the [contributor guide](CONTRIBUTING.md). Factry is licensed under [Apache 2.0](LICENSE).

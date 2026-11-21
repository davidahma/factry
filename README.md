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

For a simple fix, start with Implement. For a larger change, hand the implementer Plan’s Markdown, the revision it assumes, and the requested stopping point. Give Verify the original criteria and the resulting commit or working tree.

## Work on a feature together

Two developers can pass their own checks and still ship incompatible changes. In the [team walkthrough](examples/team-change/README.md), one changes the JSON an order exporter writes and another changes how a receipt reader consumes it. Work in separate clones, agree on the behavior in the issue, and give a teammate an exact pair of revisions they can check without your chat history.

Run `python3 examples/team-change/demo.py` from a Factry checkout to create the exercise. Run `make team-check` for the automated replay. The [pilot guide](evals/team-pilot.md) compares the handoff against ordinary issues, PRs, CI and the team's usual agents.

## Investigate a failure

| Skill | When to use it | What you get |
| --- | --- | --- |
| [Fix CI](skills/factry-fix-ci/SKILL.md) | A specific build or test job failed. | A diagnosis tied to the tested revision and a verified repair when requested. |
| [Debug](skills/factry-debug/SKILL.md) · optional | A developer or user can describe a symptom, even when CI passes. | A small reproducer or a precise account of missing evidence, plus a diagnosis and the next distinguishing check. |

If CI is green and a user reports missing output, start with Debug. If a particular job went red, give Fix CI its run link. A diagnosis-only request can end with the cause and the evidence for it.

## Deliver a PR

| Skill | When to use it | What you get |
| --- | --- | --- |
| [Address Review](skills/factry-address-review/SKILL.md) · optional | You need to act on review comments after a PR has changed. | The current disposition of each thread, with evidence for repairs, duplicates, and superseded feedback. |
| [Ship](skills/factry-ship/SKILL.md) | You want a commit, a draft PR, or an approved change landed. | Confirmation of the specific delivery action you requested. |
| [Post-merge](skills/factry-post-merge/SKILL.md) | A PR has landed. | Checks and outstanding failures linked to the resulting revision. |
| [Release](skills/factry-release/SKILL.md) · optional | Maintainers need to prepare, publish, or verify a version. | Verification of the tag, artifacts, and the version a consumer can install. |

These routes organize eight core skills and three optional skills. Your agent supplies file, shell, and code-host access. A local review needs only the diff and relevant context. Publishing or changing review threads requires the corresponding permission and developer request.

## Install

From the target Git repository, use Node.js 22.20.0 or newer and `npx` to install one skill with the [Skills CLI](https://github.com/vercel-labs/skills). This example installs Plan for Codex.

```sh
npx skills@1.9.0 add davidahma/factry --skill factry-plan --agent codex
```

For Claude Code, use `--agent claude-code`. The installer writes the skill into the project and creates or updates `skills-lock.json`. The shorthand follows the repository’s default branch. To list available skills, run `npx skills@1.9.0 add davidahma/factry --list`. Start a fresh session in that project and ask for Plan by name.

> Use factry-plan to plan pagination for this command. Show what an existing caller will see and how we can test it. Leave the code alone.

For a clear fix, install Implement with the same command using `--skill factry-implement`. Start a fresh session and describe the repair and where to leave the patch.

> Use factry-implement to repair this off-by-one error and add a regression test. Leave the patch in my working tree.

### Install from a release

Download the skills ZIP and `SHA256SUMS` for the same version from [GitHub Releases](https://github.com/davidahma/factry/releases). For the walkthroughs, download the release's **Source code** archive or check out its tag. In the download directory, check the skills ZIP’s own entry before extracting it.

```sh
archive=factry-skills-v0.3.0.zip
awk -v archive="$archive" '$2 == archive' SHA256SUMS | shasum -a 256 -c - &&
  unzip "$archive"
```

On systems with GNU `sha256sum`, use `sha256sum -c -` in place of `shasum -a 256 -c -`. Copy the desired folder, such as `skills/factry-plan`, into your project’s `.agents/skills/` for Codex or `.claude/skills/` for Claude Code. Start a new session in the project and invoke the skill by name.

See the [evaluation cases](evals/README.md), [team trial results](evals/team-results.md), and [contributor guide](CONTRIBUTING.md). Factry is licensed under [Apache 2.0](LICENSE).

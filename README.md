# Factry

[![CI](https://github.com/davidahma/factry/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/davidahma/factry/actions/workflows/ci.yml)

Factry is a collection of twelve Markdown skills for developers who use coding agents in Git repositories. Install one when you need to plan a change, diagnose a failure, review a pull request, or check what actually shipped.

A Python CLI promises that a limit of zero prints nothing. Its two tests pass, but `--limit 0` prints the entire input. The [Verify walkthrough](examples/verify/README.md) takes you from that green branch to a regression test and a working fix.

## Install

From your project's root, install Verify for Codex with the [Skills CLI](https://github.com/vercel-labs/skills). The CLI requires Node.js 22.20.0 or newer. You can also [install from a release](#install-from-a-release) without Node.js.

```sh
npx skills@1.9.0 add davidahma/factry --skill factry-verify --agent codex --yes
```

For Claude Code, use `--agent claude-code`. The command installs the skill from Factry's default branch and records it in your project's `skills-lock.json`. Start a fresh agent session and give it the issue or acceptance criteria. For the CLI walkthrough, try this prompt.

> Use factry-verify to check this branch against the requirements in README.md. Which requirements hold on this commit? Show me the evidence and leave the code alone.

## Choose a skill

| Skill | What to ask your agent to do |
| --- | --- |
| [Scout](skills/factry-scout/SKILL.md) | Trace an unfamiliar behavior to the code that controls it and find the callers a change would affect. |
| [Plan](skills/factry-plan/SKILL.md) | Plan a change, including rollout and rollback when old and new versions need to work together. |
| [Implement](skills/factry-implement/SKILL.md) | Make a scoped patch from a request or plan. For a fix, reproduce the defect and check a neighboring case. |
| [Debug](skills/factry-debug/SKILL.md) | Reproduce a reported bug and narrow down its cause. |
| [Fix CI](skills/factry-fix-ci/SKILL.md) | Diagnose a failed job and, if you request a repair, check the fix against that failure. |
| [Review](skills/factry-review/SKILL.md) | Find regressions in a diff. Identify the affected caller and the input or condition that triggers each one. |
| [Verify](skills/factry-verify/SKILL.md) | Mark each requirement passed, failed, or unverified, with the revision and evidence for each verdict. |
| [Audit](skills/factry-audit/SKILL.md) · pilot | Follow a user journey across an existing repository and rank the gaps worth fixing first. |
| [Address Review](skills/factry-address-review/SKILL.md) | Check which review comments still apply, fix confirmed issues, or draft replies. |
| [Ship](skills/factry-ship/SKILL.md) | Stop at the delivery step you request, whether that's a local commit, a draft PR, or a merge. |
| [Post-merge](skills/factry-post-merge/SKILL.md) | Follow the checks on the commit that landed and report any outstanding failures. |
| [Release](skills/factry-release/SKILL.md) | Prepare or publish a version, or verify the artifact a user can install. |

For a migration, Plan's [architecture guide](skills/factry-plan/references/architecture-decisions.md) asks which reader must ship first. Implement's [development checks](skills/factry-implement/references/development-checks.md) cover existing data and callers. Verify's [test selection guide](skills/factry-verify/references/test-selection.md) helps you choose a check for the failure you suspect. Each guide installs with its skill.

## Work on a feature together

Alice adds a currency field to an order export. Ben's receipt formatter rejects the extra field. Both branches pass their own tests and Git merges them cleanly. The [team walkthrough](examples/team-change/README.md) gives you their checkouts and a four-line handoff for the issue or PR, so a teammate can find the two commits and test the receipt without either author's chat history.

From a Factry checkout, run `python3 examples/team-change/demo.py` to try it. In a [trial with fresh Codex sessions](evals/team-results.md), reviewers made the same calls in all five cases, with or without the four-line handoff.

## Install from a release

For a versioned install, download the skills ZIP and `SHA256SUMS` from the [v0.4.0 release](https://github.com/davidahma/factry/releases/tag/v0.4.0). In the download directory, verify the ZIP before extracting it.

```sh
archive=factry-skills-v0.4.0.zip
awk -v archive="$archive" '$2 == archive' SHA256SUMS | shasum -a 256 -c - &&
  unzip "$archive"
```

If your system uses GNU `sha256sum`, replace `shasum -a 256 -c -` with `sha256sum -c -`. Copy the skill folder you want, such as `skills/factry-verify`, into your project's `.agents/skills/` for Codex or `.claude/skills/` for Claude Code. For the walkthroughs, use the release's **Source code** archive.

[Evaluation cases](evals/README.md) · [Contributing](CONTRIBUTING.md) · [Apache 2.0 license](LICENSE)

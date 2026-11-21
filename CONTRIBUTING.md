# Contributing to Factry

Follow the [community conduct guidelines](CODE_OF_CONDUCT.md) in project discussions. Start with a developer request that an existing skill handles poorly. Describe the repository state, what the agent did, and what a maintainer needed instead. A small synthetic example makes a change easier to evaluate. Use [issues](https://github.com/davidahma/factry/issues) for bugs and proposals and the [security policy](SECURITY.md) for vulnerabilities.

## Change a skill

Each directory in `skills/` is an independent installation unit. Keep its name and description specific enough for an agent to select it from the catalog. Put the essential decisions in `SKILL.md`. Keep any supporting files inside the same skill. Use the target repository’s own commands and preserve the developer’s requested scope. The file format follows the [Agent Skills specification](https://agentskills.io/specification).

Run `make check` from the repository root with Git 2.28+, Ruby 2.6+, Python 3.7+ and Make. This checks skill metadata, catalog entries, local file links, and the worked example. To use a different interpreter, set `PYTHON` or `RUBY` when invoking Make.

For a behavior change, run the relevant [evaluation case](evals/README.md) in a fresh coding-agent session. Give it the skill, the request, and the raw inputs. Record the decision it reached, the evidence it used, and any extra permission it assumed. Keep expected answers outside the agent’s working directory. Submit the case and observed result with the PR.

## Design influences

Factry takes inspiration from the focused workflows and verification exercises in [Superpowers](https://github.com/obra/superpowers), the distinct review and delivery commands in [gstack](https://github.com/garrytan/gstack), and the discoverable engineering catalog in [Agent Skills by Addy Osmani](https://github.com/addyosmani/agent-skills). Factry’s instructions and worked example are written for this collection.

By submitting a contribution, you agree to license it under the repository’s [Apache License 2.0](LICENSE).

# Queiroz

Ryan Queiroz's skill harness for Claude Code. Design and decisions: [DESIGN.md](DESIGN.md).

## Install

```bash
claude plugin marketplace add RyanQueiroz/queiroz-skills
claude plugin install queiroz@queiroz
```

Then turn on auto-update once, inside a Claude Code session: `/plugin` → **Marketplaces** → **queiroz** → **Enable auto-update**. Third-party marketplaces start with auto-update off.

To update by hand instead:

```bash
claude plugin marketplace update queiroz
claude plugin update queiroz@queiroz
```

## Skills

- **Executor:** `queiroz:mode` (implement a spec or fix a bug, verified, on a branch).
- **Used by queiroz:mode:** `queiroz:setup`, `brief`, `queiroz:blast`, `merge`, `debug`, `frontend`, `deslop`, `no-comments`, `unslop`, `queiroz:design`, `interrogate`.
- **Plan:** `idea-refine`, `grill`, `spec`, `research`, `prototype`.
- **Measure:** `measure`, `perf` (+ agent `web-perf-auditor`).
- **Deliver:** `pr`, `ci`, `observability`.
- **Refactor:** `refactor` (audit with DRY, KISS, YAGNI, dead code, decoupling and modernization lenses, then transform with characterization tests and proven parity).
- **Understand and maintain:** `how`, `why`, `bro`, `teach`, `recall`, `reflect`.

Models per role: [models.md](models.md), overridable in `~/.claude/queiroz-models.md`.

## Releasing

Bump `version` in `.claude-plugin/plugin.json` and push to `main`. Users only receive a change when the version changes: a push without a bump reaches nobody.

## Credits

Inspired by and adapted from [pstack](https://github.com/michael-denyer/pstack-claude) (MIT, Lauren Tan), [agent-skills](https://github.com/addyosmani/agent-skills) (Addy Osmani) and [mattpocock/skills](https://github.com/mattpocock/skills). `skills/setup/references/feature-map-example/` is copied from pstack's `create-verification-skill`.

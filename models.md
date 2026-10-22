# Queiroz models

Default model per subagent role. The orchestrator is the session itself and uses the session's model.

To override a role, add a line to `~/.claude/queiroz-models.md` in the same `role: models` form. A role missing from that file keeps the default below. The file is optional.

```
implementer: opus
explorer: haiku
architecture panel: fable, opus, sonnet, haiku
interrogate panel: fable, opus, sonnet, haiku
synthesizer: fable
verifier: sonnet
reviewer: sonnet
blast: sonnet
investigator: sonnet
researcher: sonnet
refactor lens: opus @high
refactor swarm: haiku
fact checker: haiku
refactor implementer: opus @high
```

To resolve a role: read `~/.claude/queiroz-models.md`; if it has a line for the role, use it; otherwise use the line above. Pass the model as the `Agent` tool's `model`. A value with `@<level>` (low, medium, high, xhigh, max) also passes that level as the `Agent` tool's `effort`. A panel role spawns one agent per listed model.

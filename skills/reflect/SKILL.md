---
name: reflect
description: Review the session, surface what was learned, and propose concrete edits to Queiroz skills and the project's verify skill.
disable-model-invocation: true
---

# Reflect

Mine the session for durable **lessons** and route each to one concrete edit where the next agent will meet it. A correction the user had to give twice becomes a rule. You propose; the user approves each edit before anything changes.

Edit targets, in order of preference:

1. **A check** (test, lint rule, script, hook) when the rule is mechanical. A rule a machine enforces beats prose an agent may skip.
2. **The project's `verify`**: `.claude/skills/verify/SKILL.md` (launch, doctor, drive, evidence, cleanup) and its feature map `.claude/skills/verify/features/`.
3. **Queiroz's own skills**, edited in the source repo `/Users/ryandeoliveiraqueiroz/Documents/queiroz/skills/<name>/SKILL.md`, never in the plugin cache. The always-on core lives in `/Users/ryandeoliveiraqueiroz/Documents/queiroz/hooks/session-start.md`.
4. **The project's `CLAUDE.md`**, only for a short pointer to where something lives.

Skip trivial sessions. A one-off is not a lesson.

## 1. Find the transcript

Transcripts live at `~/.claude/projects/<encoded-cwd>/*.jsonl`, where `<encoded-cwd>` is the project path with each `/` and `.` turned into `-`. Stay inside this project's directory. Pick this session's file: the newest one whose early lines contain a fragment of the session's first user prompt.

```bash
grep -l "<fragment>" $(ls -t ~/.claude/projects/<encoded-cwd>/*.jsonl) | head -1
```

If no file matches, write a tight digest of the session (requests, corrections, decisions, failures, skills used) and use that instead.

**Done when** you hold the transcript path or the digest.

## 2. Review in parallel

Spawn three reviewers in one message, `subagent_type: general-purpose` (keeps MCP access for tickets or traces the transcript cites), model per the `reviewer` role in [`../../models.md`](../../models.md). Each gets [`references/reviewer-prompt.md`](references/reviewer-prompt.md) with the transcript path (or digest) and one lens: **judgment**, **tooling**, or **divergent**.

While they run, find **repeated corrections**: the same correction given twice in this session, or given once here and once in an earlier session of this project (grep the other transcripts for its key phrase). Each one is a rule candidate.

**Done when** all three reviewers returned and the repeated-correction list is done (empty is a valid result).

## 3. Synthesize

Test every finding and every rule candidate:

- **Durable:** still true after paths, SHAs, and versions change.
- **Decision-changing:** the next agent acts differently because of it.
- **Used:** it routes to a skill or tool this session actually used, or to a skill that should have fired and did not (then the fix is its description or the core's pointer to it).
- **Not already covered:** read the target file first. If the guidance exists and was skipped, the edit is to its wording or placement, not a duplicate.
- **Mechanical?** If a check could enforce it, the routing is the check.

Findings echoed by two reviewers carry more weight; a singleton clears a higher bar. A repeated correction passes **Durable** by default.

**Done when** each finding sits in exactly one of Aceitas, Rejeitadas, Backlog.

## 4. Propose and wait

Show the user, in Portuguese:

| Problema | Proposta | Onde |
|---|---|---|

One row per accepted edit, rule candidates marked `(regra)`. Then **Rejeitadas** (one line each with the reason) and **Backlog** (larger work: a new skill, a check that needs design). Ask which rows to apply. Apply nothing before the user answers.

**Done when** the user picked rows, or declined.

## 5. Apply

For each approved row, make the edit at its exact target, following `writing-for-agents`: positive instructions, one source of truth, each step ending on a **Done when**.

- An edit to `verify` that changes launch, drive, or evidence steps is proven by running that part of `verify` once.
- An edit to a Queiroz skill ends with `claude plugin validate /Users/ryandeoliveiraqueiroz/Documents/queiroz` passing.
- A new check is run once and shown failing on the mistake it targets.

**Done when** every approved row is applied and its proof ran.

## 6. Report

In Portuguese, no preamble:

- **Aplicadas:** path, what changed, one line each.
- **Regras novas:** the rule and where it lives.
- **Backlog:** one line each.
- **Descartadas:** one line each with the reason.

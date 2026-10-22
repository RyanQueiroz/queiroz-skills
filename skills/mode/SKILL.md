---
name: mode
description: Queiroz's executor. Takes a spec (or a bug) and delivers it verified on a branch, orchestrating parallel subagents. Use when the user says "queiroz:mode", "/queiroz:mode", or asks queiroz:mode to implement a spec or fix a bug.
---

# queiroz:mode

You are the **orchestrator**. You plan, dispatch, verify, and integrate. Subagents write the code. You deliver a branch whose every commit passed `verify`, then return to normal work.

Keep the run's state in files so any subagent, or you after a `/compact`, can pick it up:

```
.queiroz/<feature>/
  spec.md          # input
  tickets/NN-<slug>.md   # status: todo | doing | done | blocked
  log.md           # one line per decision or check: what, why, evidence
  blast/           # before.md, after.md and the proof scripts (queiroz:blast)
  evidence/<run>/  # every verify run of this feature; <run> = AAAAMMDD-HHMM-<what>
```

Everything a feature produces lives in its folder. Nothing goes to a sibling `.queiroz/evidence/` or a loose file next to it.

If `.queiroz/<feature>/` already exists, resume: read `log.md` and every ticket's status, then continue from the first step not done.

## Rules for the whole run

- **Orchestrator writes no ticket code.** Every change goes through a fresh subagent briefed with the `brief` skill. Models come from `../../models.md`.
- **Parallel by default.** Independent work (tickets, reads, reviews) goes out in one message, in the background.
- **No shared writes.** Two tickets running together never touch the same file. If they would, merge them into one ticket or make one block the other.
- **Pause only for:** the gates marked ✋ below, and irreversible actions (deploy, merge into a shared branch, push, deleting data, messaging customers, real money).
- **Never** merge, push, or open a PR. The user asks for those separately (`pr` skill).

## 1. Intake

- **Bug, no spec:** follow the `debug` skill, then jump to step 6.
- **Feature:** find the spec (`.queiroz/<feature>/spec.md` or the path the user gave). No spec → tell the user to run `/spec` first and stop.
- The spec must have a **"Como provamos"** section. Missing → ask the user for the proof scenarios and stop until you have them.

**Done when** you hold a spec with proof scenarios, or a bug handed to `debug`.

## 2. Preconditions

1. **`verify` exists** at `.claude/skills/verify/`. Missing → ✋ say in one line "Este projeto não tem `verify`; vou rodar o `queiroz:setup` antes. Posso?" and wait. On OK, run `queiroz:setup`.
2. **Branch.** The working tree is clean (otherwise stop and report what is uncommitted). Create `queiroz/<feature>` from the current base branch.
3. **Doctor.** Run the `verify` skill's Doctor once.

**Done when** `verify` exists, the branch is checked out, and Doctor passed.

## 3. Understand the blast radius

Dispatch in one message:

- `queiroz:blast` in **before** mode on everything the spec says it will touch. Assertions the spec makes about existing code are hypotheses until proven.
- One or more `explorer` subagents for the code areas the spec touches (entry points, data shapes, tests, prior art).

The blast report lands in `.queiroz/<feature>/blast/before.md`. Record its proven safety facts and the "não provado" ones in `log.md`.

**Done when** every area the spec touches has an explorer summary and the blast report is in.

## 4. Plan

**Critical check.** Any of these present → ✋ suggest the tank in one line with the reason and the cost, then wait:
money, auth, data migration, architecture with no precedent in the code, open decisions in the spec, or a "não provado" safety fact.

> "Isso é crítico porque <motivo>. Sugiro `queiroz:design` (4 modelos desenham, síntese + plano, ~4-5× o custo do planejamento normal). Ligo?"

- **OK** → run `queiroz:design`. It returns the design and the tickets. Optionally suggest `interrogate` on the design for the riskiest cases.
- **No, or not critical** → write the tickets yourself.

Each ticket follows [../design/references/ticket-template.md](../design/references/ticket-template.md), the same format `queiroz:design` produces.

Tickets are vertical slices (a narrow path through every layer), each small enough for one fresh context. A ticket without a Proof does not exist. Check the `touches` lists: tickets that can run together never touch the same file.

**Done when** every spec requirement maps to at least one ticket, and every ticket has a Proof and a `touches` list.

## 5. Execute the frontier

The **frontier** is every `todo` ticket whose blockers are all `done`. Loop until no ticket is `todo`:

1. For each frontier ticket, write a brief with the `brief` skill and dispatch an `implementer` subagent with `isolation: "worktree"`, all in one message, in the background. Mark them `doing`.
2. Each implementer, per its brief: implements the ticket, follows `frontend` if it touches UI, runs the ticket's tests, drives the ticket's Proof with `verify` in its worktree, runs `deslop` and `no-comments`, then makes **one commit** (Conventional Commits, the *why*, `Refs: ticket NN`) after checking the staged diff for secrets. It returns the commit SHA, the evidence path, and anything it could not do.
3. As each one returns, **you check it**: read the diff, open the evidence. Your own reading is the judgment, not its summary.
4. Integrate into `queiroz/<feature>` with `git merge --no-ff <ticket-branch>`, which keeps the ticket's commit. Conflicts → `merge` skill.
5. Run the ticket's Proof again on the integrated branch with a `verifier` subagent. Pass → mark `done`, log it. Fail → revert that integration, mark the ticket `todo` with the failure in it, and dispatch a fresh implementer.
6. Dispatch the new frontier.

If `verify` cannot isolate parallel instances, run the Proof checks one at a time; the implementation still runs in parallel.

**Done when** every ticket is `done`.

## 6. Final review

Dispatch in one message:

- `queiroz:blast` in **after** mode (report in `.queiroz/<feature>/blast/after.md`) on the full diff of `queiroz/<feature>` against its base.
- A **blind** `reviewer` subagent. Give it only the spec path and the diff command, nothing about tickets, logs, design, or this conversation. Its brief:
  > Review this diff against the spec. Report: spec requirements missing or wrong; bugs; security at the boundaries (external input, auth, money, personal data); idempotency of webhooks, jobs, and retries; needless code or abstraction; tests that would not catch a real defect. For each finding: file:line, what breaks, how sure you are.

Each confirmed finding becomes a new ticket and goes through step 5. Then rerun this step once on the new diff.

**Done when** both reports have no open confirmed finding.

## 7. Prove the whole spec

1. Run every "Como provamos" scenario with `verify` on the final branch, evidence to `.queiroz/<feature>/evidence/<run>/`, even when the `verify` skill names another folder for runs outside a feature.
2. Add the feature to the `verify` feature map (`.claude/skills/verify/features/`), in its own commit.
3. Run the `verify` Cleanup and confirm the evidence survived.

**Done when** every scenario passed and its evidence exists on disk.

## 8. Report

Write the report in Portuguese, following `unslop`, leading with the result:

- What was delivered, and the branch name.
- Commits, one per ticket.
- Each "Como provamos" scenario with its evidence path.
- Blast radius: the safety facts proven, and anything still "não provado".
- What the review found and how it was fixed.
- Anything skipped or not proven, stated plainly.
- Last line: "Branch pronto para PR. Não fiz merge nem push."

Then leave `queiroz:mode` and return to normal work.

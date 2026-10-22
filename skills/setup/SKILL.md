---
name: setup
description: Prepare a project for Queiroz by generating its `verify` skill, a scripted way to launch the real app, drive it like a user, and keep proof. Use for /queiroz:setup, when `queiroz:mode` finds no `verify` skill, or when a project has no scripted way to prove its behavior.
---

# queiroz:setup

Generate the project's **`verify`** skill at `.claude/skills/verify/`: the driver every Queiroz proof runs through. You write it for the next agent, who reads it cold mid-task and has never seen this app.

A project skill named `verify` replaces Claude Code's bundled `/verify`, so `queiroz:mode` and its subagents can call it. In a monorepo, write it in the package being changed.

## 0. Existing verify

Look for `.claude/skills/verify/` (it may be a symlink; the project's `CLAUDE.md` may name another source of truth, such as `.cursor/skills/`). Found one → **audit, don't regenerate**:

- Check it has Launch, Doctor, Drive (through the user's surface, on reference data), Evidence, Cleanup, Helpers, and a feature map. Note each gap.
- Keep the project's own conventions: its evidence folder, its script paths, its isolation scheme. Queiroz follows them.
- Fix only real gaps, in the project's source of truth, with the user's OK.
- Then skip to step 5 and prove it.

**Done when** the existing skill is audited, or you found none and go to step 1.

## 1. Explore

Answer from the repo. A fact you can observe is yours to find; send an `explorer` subagent (model per `../../models.md`) for broad reads.

- **Surface.** What the user touches: web UI, API, WhatsApp/webhook flow, CLI, worker. Pick the primary one; list the others.
- **Run.** How the app starts locally: `docker compose`, Makefile, package scripts, README. Ports, env vars, seed data, auth.
- **Drive.** How an agent acts on it **through the surface the user touches**: the browser tools for a web UI, a PTY for a CLI, a signed payload for a webhook. Existing Playwright or e2e harnesses count. `curl` on an API is a side check, never the proof of a UI feature.
- **Reference data.** The account, tenant, or dataset the team really uses day to day (the user names it). Proof runs against it, read-only unless the skill's isolated mode copies it. An empty database proves only that the app boots.
- **Observe.** What proves a result: response bodies, screenshots, DB rows (`docker compose exec db psql ...`), logs, exit codes, files written.
- **Isolate.** Whether two instances can run side by side (ports, compose project name, data dirs). If they can't, the skill says so and refuses to drive an instance it didn't start.

If the checkout doesn't build or start, fix that first or report exactly what fails. A skill written against a broken base teaches broken steps.

**Done when** every bullet above has an answer with a file or command as its source.

## 2. Confirm with the user

Show what you found in one short list: surface, launch command, drive method, reference data, proof sources, isolation. Ask only what the repo can't tell you (test credentials location, a sandbox account, which flow matters most), each question with your recommended answer.

**Done when** the user confirms or corrects the list.

## 3. Write the skill

Write `.claude/skills/verify/SKILL.md` with frontmatter: `name: verify` and a `description` naming the app, its surface, and when to use it. Leave out `disable-model-invocation`, so agents can call it. Use these sections, each filled from step 1 with real commands from this repo:

- **Launch.** The exact start command and the ready signal (log line, port answering, healthcheck). Use a dedicated compose project name or port so the run never touches the user's own instance. Include teardown.
- **Doctor.** One read-only check that answers "is this instance worth driving?": process up, right build, port owned by this run, auth valid. Run it before the first drive and after anything surprising.
- **Drive.** The harness recipe with real routes, selectors, payloads, and commands, against the reference data. Prefer stable handles: ARIA names, route paths, data attributes, API fields. Name what is off limits on real data (sending messages, payments, deletes).
- **Evidence.** What to capture and where it goes (`.queiroz/<feature>/evidence/<run>/`, with `<run>` = `AAAAMMDD-HHMM-<what>`, unless the project already has an evidence folder; `queiroz:mode`, `debug` and `merge` always write inside the feature folder). Proof standards:
  - Drive the real user path. Internal setters and test-only endpoints are not proof.
  - Capture the action **and** the resulting state.
  - Check side effects too: rows inserted, messages sent, files written.
  - Mock only at a boundary production already isolates (a payment provider's test mode, a WhatsApp sandbox).
  - Trust a dry-run only after observing what it really skips.
- **Cleanup.** Stop what this run started, by container or PID, never by process name. Cleanup keeps the evidence.
- **Helpers.** Any script the skill ships is executable, lives in `.claude/skills/verify/scripts/`, and is invoked in the skill body.

**Done when** no section holds a placeholder.

## 4. Seed the feature map

Create `.claude/skills/verify/features/README.md` plus one file per user-facing feature, starting with the top 3 to 5 (from routes, commands, menus, docs). Follow the shape in [references/feature-map-example/](references/feature-map-example/): a README index with baseline preconditions and proof rules, and per feature the four H2s `Sub-features`, `How to get to it (user POV)`, `Driving it with <harness>`, `Gotchas`.

The map is the project's list of what "working" means. `queiroz:mode` adds each feature it ships.

## 5. Prove it end to end

Run the skill once, following only its own text, through the user's surface (the browser for a web app) on the reference data. If a shared instance belongs to another checkout, use the skill's isolated mode with names and ports no other session is using: launch, doctor, drive one mapped feature, capture evidence, cleanup. Then confirm the evidence still exists at its named location.

A failure means the skill is wrong: fix it, run its cleanup, and run again. Repeat until a full pass succeeds.

**Done when** one full pass succeeded and its evidence survived cleanup. A skill that never ran is a draft.

## 6. Report

Tell the user, in Portuguese:

- Where the skill lives and the one command that launches the app.
- Which feature was driven, and the path to its evidence.
- Features mapped, and the obvious ones still missing.
- Anything the skill can't drive yet, with the reason (missing credential, external dependency).

---
name: design
description: Multi-model architecture for a critical spec. A panel of models designs it independently, a synthesizer writes one new design from the best of each, and the result ships with its ticket plan in `.queiroz/<feature>/`. Use for /queiroz:design, or when `queiroz:mode` suggested the multi-model design and the user said yes.
---

# queiroz:design

Turn `.queiroz/<feature>/spec.md` into a **synthesized design** and the **ticket plan** that builds it. Several models design in parallel; one synthesizer combines the best of every candidate into a new, coherent design. This is synthesis, not selection: the output is "the best of each", never "the best of N".

Multi-model stops at architecture. One `implementer` per ticket builds against the design later, under `queiroz:mode`. Nothing here writes production code.

Models come from `../../models.md` (roles `explorer`, `architecture panel`, `synthesizer`).

## 0. Gate

The panel costs about five design runs. Run only after an explicit OK from the user in this conversation. Without one, say in Portuguese, in one line, why the spec looks critical and the cost (for example: "Spec mexe em cobrança e webhook; o queiroz:design roda 4 modelos + 1 síntese, ~5x um desenho único. Sigo?") and wait.

**Done when** the user said yes.

## 1. Ground

Read the spec in full. It needs a "Como provamos" section; if it has none, stop and tell the user to finish the spec first, since tickets can't be proved without it.

Dispatch one `explorer` to map what the spec touches in the code: existing types, modules, callers, data shapes, external boundaries (webhooks, APIs, DB tables, auth). If `queiroz:blast` already ran for this spec, hand its output to the explorer as a starting point. What the spec claims about existing code is a hypothesis until the explorer cites the line. Write the result to `.queiroz/<feature>/design/grounding.md`.

Skip the explorer only for greenfield work with nothing to integrate.

**Done when** every module and data shape the spec touches has a cited fact (`file:line`) or is marked "não existe ainda".

## 2. Fan out the panel

Resolve `architecture panel`. Send one `Agent` call per model, **all in one message**, `run_in_background: true`, `subagent_type: general-purpose`, `model` set to that entry. Each prompt carries:

- [references/panel-prompt.md](references/panel-prompt.md), verbatim.
- The paths to the spec and `grounding.md`.
- Its own output path: `.queiroz/<feature>/design/candidates/<model>.md`.

Candidates never see each other. Independence is the point: a model that saw another's design converges on it.

A candidate that fails or returns nothing is a dropout. Record it and continue.

**Done when** every panel model produced its file or is recorded as a dropout, and at least two candidates exist. With fewer than two, there is nothing to synthesize: rerun the dropouts once, then stop and tell the user.

## 3. Synthesize

Resolve `synthesizer`. Dispatch one agent with [references/synthesis.md](references/synthesis.md) verbatim, plus the paths to the spec, `grounding.md`, every candidate, and [references/design-red-flags.md](references/design-red-flags.md). It writes `.queiroz/<feature>/design.md`.

If the synthesizer reports the candidates diverge on a decision the spec leaves open, that is a spec gap, not a merge problem. Ask the user that decision in Portuguese with your recommended answer, then rerun this step with the answer.

**Done when** `design.md` exists with every section of the template filled.

## 4. Check the design

Read `design.md` end to end yourself. The synthesizer's word is not the check.

- **Spec coverage.** Fill the coverage table: every user story, requirement, and "Como provamos" scenario maps to the design section that handles it.
- **Boundary security.** For every boundary that takes external input, enforces auth, moves money, or stores personal data: where input is validated, who is authorized and where that's checked, what happens when the operation runs twice (webhooks, retries, payments), what is logged and what must never be.
- **Red flags.** Screen against [references/design-red-flags.md](references/design-red-flags.md).
- **Traceability.** Every decision names its source model(s) and why it won; every rejected idea names its reason.

Send each gap back to the synthesizer with the exact gap and repeat this step. For high-stakes boundaries, offer `interrogate` on the design in one line and wait for the OK.

**Done when** the coverage table has no empty row and every boundary has a named owner.

## 5. Plan the tickets

Write the plan into `.queiroz/<feature>/tickets/`, one file per ticket, shaped by [references/ticket-template.md](references/ticket-template.md):

- **Vertical slices.** Each ticket delivers behavior a user or caller can observe, end to end through the layers it needs.
- **Blocking edges.** `blocked_by` names the tickets that must land first. No cycles.
- **Shared files.** Two tickets with no blocking edge between them run in parallel, so they never touch the same file. If they would, merge them or add an edge.
- **Proof.** Each ticket states the `verify` scenario that proves it: action → visible result → effect in DB or file. A ticket with no proof stays out of the plan; fold its work into the ticket whose proof exercises it.

Write `.queiroz/<feature>/tickets/README.md` with the dependency graph and the first parallel frontier.

**Done when** every module in the design is built by some ticket, every ticket has a Proof, and the graph has no cycle.

## 6. Hand off

Under `queiroz:mode`: return the paths to `design.md` and `tickets/`. `queiroz:mode` executes this plan instead of breaking the spec itself.

Called alone: report to the user in Portuguese, then stop:

- Where the design and the tickets live.
- The three to five decisions that shaped the design, each with its source model.
- What only one model saw and made it in.
- How many ideas were rejected, and the open questions that need the user.

## When implementation fights the design

The design is the contract. When a ticket can't be built as designed, the implementer stops and reports; nobody bends the code around the design.

- **Local deviation** (a parameter, a rename, the shared contract intact): record it in the design's "Reconciliation" section with why the design still holds.
- **Structural friction:** the same workaround in unrelated places, escape-hatch types (`any`, casts, optional fields always set), callers that must know internals, a lock the design said wasn't needed, or two deviations of the same shape. Redo the synthesis: rerun step 3 with the new constraint as input (rerun step 2 too if the constraint invalidates every candidate), then steps 4 and 5 for the affected tickets. Code built on the old shape is replaced, not patched.

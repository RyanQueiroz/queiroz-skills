# Ticket template

One file per ticket: `.queiroz/<feature>/tickets/NN-<slug>.md`, numbered in dependency order.

```markdown
---
id: NN
status: todo        # todo | doing | done | blocked
title: <verb phrase: what the user or caller can now do>
blocked_by: []        # ticket ids that must land first
touches:              # files this ticket creates or edits
  - src/...
design: [Shape, Flows > <scenario>, Boundaries > <row>]   # design.md sections it builds
---

## What
The vertical slice in two or three sentences: the behavior it adds, end to end.

## Acceptance criteria
- [ ] Observable behavior, one per line, each checkable.
- [ ] Boundary rules from the design that this ticket owns (validation, auth, idempotency).

## Proof
The `verify` scenario that proves it, in the spec's "Como provamos" form:
action → visible result → effect in DB or file.
Plus the tests the implementer writes for the logic inside.

## Notes
Design decisions the implementer must not reinterpret, with their design.md section.
```

Rules the orchestrator checks:

- `touches` of two tickets with no `blocked_by` path between them never overlap.
- Every ticket has a Proof. Work with no observable proof (a type, a helper, a migration) rides inside the ticket whose Proof exercises it.
- `tickets/README.md` lists the graph and the first frontier: every ticket with an empty `blocked_by`.

---
name: how
description: Explain how a piece of code works, walk through it before a change, or say where new code should live.
disable-model-invocation: true
---

# How

Answer "how does X work?" at the level of a senior engineer onboarding onto a subsystem: enough for a working mental model, never annotated source. Placement questions ("where should this live?", "which module owns this?") get the same treatment, ending in a concrete location. For "why is it this way?", point the user to `why`.

## 1. Scope

Restate the question in one line. If the referent is vague, take the best guess from the conversation (open files, recent edits, what was just discussed), say it, and proceed; the user can redirect.

Classify:

- **Simple:** one module, one function, one narrow question. Go to step 3 and explore it yourself.
- **Complex:** a subsystem across files or services, a cross-cutting feature, an architectural overview. Go to step 2.

When in doubt, take the simple path.

**Done when** the question and its size are stated to the user in one line.

## 2. Fan out (complex only)

Split the question into 2 to 4 **angles**, each a distinct slice (entry points, data model, persistence, external boundaries...). Spawn one `explorer` subagent per angle in a single message, `subagent_type: general-purpose`, model per the `explorer` role in [`../../models.md`](../../models.md). Each gets [`references/explorer-prompt.md`](references/explorer-prompt.md) with the question and its angle filled in.

**Done when** every explorer has returned its findings.

## 3. Trace and reconcile

You are the explainer. Read the code (or the explorers' findings) and trace the real flow: entry point, each call, the data passing between steps, the boundaries. Where explorers overlap, merge; where they contradict, open the file and settle it. A part you could not trace is an open question, stated as one.

For a placement question, find the closest existing code of the same kind and where it lives, who owns it, and which layer it sits in. The answer follows the codebase's own convention, named with a sibling file as the precedent.

**Done when** every step of the flow cites a file and function, and every gap is named.

## 4. Explain

Reply in Portuguese. Use these sections, dropping any that do not apply:

- **Visão geral.** One or two paragraphs: what it is, what it does, why it exists.
- **Conceitos.** The types, services, and abstractions needed to follow the rest. Short definitions.
- **Como funciona.** The longest part. Walk the flow in prose: what triggers it, each step, where data goes, the decision points. Cite files and functions; quote code only when a snippet carries the point. When three or more components talk or data transforms through stages, add a mermaid or ASCII diagram.
- **Onde fica.** A short file map: only what someone needs to start working here.
- **Pegadinhas.** Surprising behavior, historical artifacts, easy mistakes.
- **Onde colocar** (placement questions). The path, the precedent file, and the one-line reason.

Write concretely: "`UserService` chama `AuthClient.refresh()`", never "o serviço delega ao cliente". When something is complex, say why. When something is simple, keep it short. Write through `unslop`.

**Done when** a reader new to this area could start working in it from the explanation alone.

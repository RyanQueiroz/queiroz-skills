# Panel prompt

The orchestrator sends this file verbatim to every panel model, plus the spec path, the grounding path, and your output path.

---

You are one of several models designing the same spec in parallel, each on a different model. A synthesizer will read every design and combine the best of each into a new one. Produce the best design your model can make. Commit to a shape; don't hedge toward a safe middle. Differences between candidates are the signal, and an idea only you see is the most valuable thing you can contribute.

Read the spec and the grounding in full before designing. Design only: types, signatures, modules, flows. Every function body is `throw new Error("not implemented")` (or the language's equivalent); tricky logic is `// TODO:` pseudocode. Write no production code and edit no repo file.

## Discipline

- **Caller's usage first.** Write two or three real call sites before the types, then derive the types from them. When the two disagree, fix the types.
- **Data structures first.** Trace each dominant access pattern through the structures. "We'll add a cache or index later" means the structure is wrong.
- **Deep modules.** A small public surface hiding real capability. No transport or wire types on the public API: parse into domain types at the boundary.
- **Validate at boundaries, trust types inside.** Business logic as pure functions; the shell stays thin.
- **Invariants in types** before runtime checks, runtime checks before comments.
- **One owner per piece of state.** If two actors might write it, say what happens; default to per-actor state merged at read.
- **Idempotent transitions.** Say what happens when a webhook, job, or payment step runs twice or crashes halfway.
- **Short call chains.** Tracing a flow should take three files or fewer.
- **Reuse what the grounding found** before inventing a parallel structure.

## Output

Write one Markdown file at your output path with these sections:

1. **Usage.** The call sites, in code.
2. **Types.** Data structures, in code.
3. **Signatures.** Every public function and module boundary, with `not implemented` bodies and doc comments stating intent and invariants.
4. **Module map.** Files, what each owns, what it may import.
5. **Flows.** Each spec scenario traced from input to stored effect through the signatures.
6. **Boundaries.** For each external input, auth check, money movement, and personal data store: where it is validated, authorized, made idempotent, and logged.
7. **Alternatives considered.** At least one whole-shape alternative and why it lost.
8. **Open questions.** Decisions the spec leaves open, each with your recommended answer.

Then reply with the output path and a five-line summary of your shape.

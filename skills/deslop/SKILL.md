---
name: deslop
description: Remove AI-generated code slop from a diff before it is committed. Use before every commit in `queiroz:mode`, after an implementer returns a ticket, or when asked to "deslop" or clean up AI-written code.
---

# Deslop

Strip the slop an agent leaves in code, so the diff reads like the rest of the repo. Behavior stays the same.

## Scope

The diff about to be committed: the ticket's worktree changes (`git diff` plus `git diff --staged`). If the caller names files or a range, use that. Otherwise use the branch diff against its base (`git diff $(git merge-base HEAD main)`).

Touch only lines the diff added or changed. Old code outside the diff is out of scope, even when it is sloppy.

## 1. Read the neighbors

Before judging a hunk, read the surrounding file and one or two siblings. Slop is defined against local style: how this repo names things, handles errors, types values, and structures modules.

**Done when** you can name the local convention each hunk is measured against.

## 2. Hunt

Check every hunk for these:

- **Comments.** Narration of what the next line does, banners, change logs ("added X"), commented-out code. Hand the full comment pass to `no-comments`; here, delete only the obvious narration.
- **Defensive noise.** `try/catch`, null checks, `?.`, and fallbacks on paths whose types or callers already guarantee the value. Validation belongs at the boundaries (API, webhook, user input, config). Inside, trust the types.
- **Swallowed errors.** A `catch` that logs and continues, or returns a default, where the caller needs the failure.
- **Type escapes.** `any`, `as unknown as`, `# type: ignore`, non-null `!` added only to silence the checker. Fix the type.
- **Nesting.** Deep `if` pyramids that flatten with early returns.
- **Speculative code.** Options nobody passes, parameters with one value, an interface with one implementation, a helper called once, config for a constant, "for later" stubs.
- **Reinvention.** A new helper that duplicates one already in the repo or the stdlib. Use the existing one.
- **Verbose names and shapes.** `userDataObject`, `handleProcessResult`, wrapper objects around a single value. Use the repo's naming.
- **Debris.** Leftover `console.log`/`print`, unused imports, dead branches, TODOs the ticket did not ask for.

**Done when** every hunk in scope was checked against every bullet.

## 3. Fix

Make the minimal edit for each finding. Keep behavior unchanged; if a finding is a real bug (a swallowed error hiding a failure), fix it and say so in the summary, since that changes behavior.

Run the ticket's tests and the repo's type check and lint after the edits.

**Done when** the tests, type check, and lint pass on the cleaned diff.

## 4. Report

One to three sentences to the caller: what you removed, by kind, and any behavior change. In front of the user, write it in Portuguese.

---
name: no-comments
description: Hunt and delete unnecessary code comments in a diff, keeping only a non-obvious why. Use before every commit in `queiroz:mode`, after `deslop`, or when asked to remove comments, clean comments, or run "no-comments".
---

# No comments

A comment survives only when it explains a **why** the code cannot say: a constraint from something we cannot change. Everything else gets deleted, and a comment that excuses confusing code marks that code for a fix.

A fresh subagent does the hunt, so it judges the code without the author's attachment to it.

## Scope

The caller's files or diff. Otherwise the ticket's diff (`git diff` plus `git diff --staged`), or the branch diff against its base.

## 1. Spawn the hunter

Spawn a `general-purpose` agent with the `reviewer` model from `../../models.md`. Pass the scope and this prompt verbatim:

> You hunt comments in the scope below. Delete every comment in it except these keeps:
> - Legal or license headers.
> - Non-obvious behavior forced by an external dependency, platform, vendor API, or protocol we cannot change. Name the external thing.
> - Formatter or lint directives whose rule is style-only or wrong for this line.
> - Doc comments that define a public API contract (exported function, HTTP endpoint, library surface).
> - Issue or RFC links that explain a constraint the code cannot express.
>
> If you are unsure a keep applies, delete. A long justification is a sign of a workaround, not a reason to keep.
>
> Suppressions (`eslint-disable`, `@ts-ignore`, `@ts-expect-error`, `# noqa`, `# type: ignore`): look up the rule. If it protects correctness or safety, delete the suppression and flag the symbol.
>
> Comments like `IMPORTANT`, `do not remove`, `hack`, `workaround`, `fine for now`: read the nearby code and check the claim. If the surprise lives in our own code, delete the comment and flag the exact symbol `RESHAPE` with one line on the fix that makes the behavior obvious without prose: a rename, an extracted function, a type, a test.
>
> Edit comments only. Never change application code. Report: files touched, deletion count, each keep with its reason, and each `RESHAPE` flag with its symbol and one-line fix.

**Done when** the hunter returns its report and its edits are in the working tree.

## 2. Audit the report

Read the hunter's diff and report. Reject and revert:

- Any edit to application code.
- Any edit outside the scope.
- A keep whose external constraint you cannot confirm in the code or the dependency's docs.
- A `RESHAPE` flag that misreads the code.

If you reject a whole report, rerun the hunter once with the failure named. A second bad report: keep your own judgment and say the hunt was partial.

**Done when** every deletion, keep, and flag in the report is accepted or reverted.

## 3. Fix the flags

For each accepted `RESHAPE` flag inside the ticket's scope, make the smallest fix that makes the comment unnecessary: rename, extract, tighten a type, use the real API, drop a dead path.

A comment that guards a constraint in our code ("do not change this order") becomes a check when that is cheap and in scope: a type, an assertion, or a test that fails if someone breaks the constraint. Then delete the comment. If the encoding is out of scope, delete the comment and list the constraint as open.

A flag whose fix is outside the ticket stays open; never widen the ticket to chase it.

Run the ticket's tests after the fixes.

**Done when** each accepted flag is fixed or listed as open, and the tests pass.

## 4. Report

To the caller: deletions, keeps, fixes made, constraints encoded, and open flags with their symbols. In front of the user, write it in Portuguese.

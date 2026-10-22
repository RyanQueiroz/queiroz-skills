---
name: merge
description: Resolve merge conflicts when integrating parallel ticket worktrees into the feature branch, preserving both tickets' intent and re-running their `verify` checks. Use when a merge, squash, cherry-pick, or rebase stops on conflicts, when `queiroz:mode` integrates a ticket branch, or for "resolve the conflicts".
---

# Merge

Integrate a ticket's branch into the feature branch so both tickets still do what their tickets say. A resolution that compiles but drops one side's behavior is a silent bug, so every resolution is proven by re-running `verify` for the tickets it touched.

The integration method (merge, squash, cherry-pick, rebase) is whatever `queiroz:mode` started. This skill starts when it stops on a conflict.

## Rules

- Keep the feature branch at its last verified commit until the resolution is proven.
- Resolve; never pick a side for a whole file unless the other side's change is provably already contained in it, and say so in the report.
- Keep the history: no `--force`, no `reset --hard` on the feature branch, no push.
- Add no behavior neither ticket asked for. Refactors wait for their own ticket.

## 1. See the state

Run `git status` to name the operation in progress and the branch being integrated. List conflicted files with `git diff --name-only --diff-filter=U`.

**Done when** you know the operation, both branches, and every conflicted file.

## 2. Read both intents

For each side, read its ticket (`.queiroz/<feature>/tickets/<id>.md`), its commit message, and the spec section it serves. For each conflicted file, compare base, ours, and theirs: `git show :1:<path>`, `:2:<path>`, `:3:<path>`.

A conflict between two parallel tickets means the split let them write the same file. Note it for the report: `queiroz:mode` uses it to sharpen the next split.

**Done when** you can state, per hunk, what each side was trying to do.

## 3. Resolve each hunk

- **Compatible intents:** keep both. Usually both edits land side by side, or one wraps the other.
- **Incompatible intents:** the spec decides. If the spec is silent, stop and ask the user in Portuguese, with the two options and your recommendation.
- **Lockfiles and generated files:** regenerate with the project's tool (`npm install`, `uv lock`, the codegen command); never hand-edit.

Then confirm nothing is left: `git diff --check` and a search for `<<<<<<<`, `=======`, `>>>>>>>` in the touched files.

**Done when** every conflicted file is resolved, marker-free, and each hunk's choice is one sentence you can repeat in the report.

## 4. Prove it

1. Run the project's checks: typecheck or build, lint, then the tests for the touched areas.
2. Re-run `verify` for every ticket whose files were in conflict, both the incoming ticket and the already-integrated one. Add any integrated ticket whose `verify` scenario exercises a resolved file.
3. Keep the evidence in `.queiroz/<feature>/evidence/<run>/`.

A failing check means the resolution is wrong. Fix the resolution, not the code around it. Two attempts failed on the same reading of the intents? Write down that reading and check it against the tickets before a third.

If both intents cannot coexist, abort the operation (`git merge --abort`, `git cherry-pick --abort`, or `git rebase --abort`). The feature branch stays at its last verified commit, and the ticket goes back to `queiroz:mode` to be re-dispatched on the current branch.

**Done when** the checks pass and every affected ticket's `verify` passed with evidence saved, or the operation was aborted and the reason is written.

## 5. Finish

Stage the resolved files by name and complete the operation (`git commit`, `git cherry-pick --continue`, `git rebase --continue`). The commit message follows the ticket's Conventional Commit and notes the resolution.

**Done when** `git status` is clean and the operation is complete.

## Report

Return to the orchestrator, under 250 words:

- Files resolved, each with the choice made and which ticket's intent it serves.
- Any side dropped, with the proof it was already contained.
- Checks run and their result; `verify` runs per ticket with the evidence path.
- Whether the ticket split caused the conflict.
- Questions left for the user, in Portuguese.

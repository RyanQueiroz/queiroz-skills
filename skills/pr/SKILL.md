---
name: pr
description: Open a pull request for the current branch, with a review-ready description and the verify evidence.
disable-model-invocation: true
---

# PR

Push the branch and open a PR that a reviewer can understand in under a minute: why it exists, what it leaves out, what it could break, and how it was proven.

The user invoking this skill is the ask that allows the push and the PR. It never allows a merge, a force-push, or a push to `main`.

## 1. Check the branch

- Current branch is not `main` or the repo's default branch. If it is, stop and tell the user.
- Working tree is clean. Uncommitted changes: ask whether they belong in this PR.
- Resolve the base branch (default branch unless the user named one) and run `git fetch origin <base>`.
- Find the feature folder: `.queiroz/<feature>/spec.md`, `.queiroz/<feature>/tickets/`, and the last `verify` run under `.queiroz/<feature>/evidence/<run>/`. Without them, build the description from the commits and the diff, and ask the user how the change was proven.
- Check the last `verify` run passed against the branch's current head. If it did not, or the head moved since, say so and offer to rerun it before opening.

**Done when** you know the base, the feature folder (or its absence), and whether proof covers the current head.

## 2. Check reviewability

Read `git log <base>..HEAD` and `git diff <base>...HEAD --stat`, then the diff itself.

- Unrelated changes mixed in: propose moving them out.
- Commits that mix refactor with behavior, or formatting with logic: propose a regrouping in dependency order (schema, core logic, wiring, UI, tests).
- A diff too large to review with notes: recommend splitting into stacked PRs instead of polishing the description.

History rewrites need the user's OK. Before one, save `ORIGINAL_TREE=$(git rev-parse HEAD^{tree})`; after it, `git rev-parse HEAD^{tree}` must match. If the tree changed, restore and report.

**Done when** the user accepted or declined each proposal, or there were none.

## 3. Write the title and body

Title in Conventional Commits: `type(scope): subject`, imperative, no trailing period, a real symbol when one carries the change.

Body language: match the repo's recent PRs (`gh pr list --state all --limit 5 --json title,body`). With no history, write in Portuguese.

Use these `##` sections in order. Drop one only when it has nothing to say.

- `## Why`: the problem and the approach in one to three sentences.
- `## What changed`: one to three bullets. Name a symbol or path only when it carries the change; name both sides of a rename.
- `## Scope`: what the PR covers and what it leaves out on purpose.
- `## Tradeoffs`: rejected alternatives a reviewer would ask about. Skip when there was no real choice.
- `## Blast radius`: one or two sentences on what the change touches and why that is safe, from `.queiroz/<feature>/blast/after.md` when it exists.
- `## Verification`: one to three bullets, each a `verify` scenario from the spec's "Como provamos": the action, the visible result, the database or file effect. For a performance change, one number as `before → after` with its unit. Add screenshots only when they prove a claim.
- `## Tickets`: one line per ticket from `.queiroz/<feature>/tickets/` with its commit's short subject.

Leave out SHA lists, file-by-file tours, decision logs, and run transcripts. Keep the body under about 40 lines. Apply `unslop` to the title and body.

End the body with the attribution lines the session requires for pull requests, if any.

**Done when** every section left in the body carries a fact from the diff, the spec, or the evidence.

## 4. Open it

Show the user the title and body. On their OK:

1. `git push -u origin <branch>`.
2. `gh pr create --base <base> --title "<title>" --body-file <file>`, ready for review, not a draft.
3. `gh pr view --json url,state,isDraft` to confirm.

**Done when** `gh pr view` shows the PR open and not a draft.

## 5. Report

Tell the user, in Portuguese: the PR URL, the base branch, and anything left open (a stale `verify`, a declined split, a missing section). Do not merge and do not watch the checks; for failing checks, the user calls `/ci`.

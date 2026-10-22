---
name: ci
description: Create or update the project's CI pipeline, or fix failing CI checks on a branch or PR.
disable-model-invocation: true
---

# CI

CI runs the project's quality gates on every change, so nothing broken reaches `main`. This skill has two branches: **build** (create or update the pipeline) and **fix** (make failing checks pass). Pick the one the user asked for; with failing checks on the current branch and no other ask, it is **fix**.

Deploys belong to the user. Leave deploy jobs out unless the user asks for one, and never trigger a deploy.

## Build

### 1. Read what exists

- Current CI: `.github/workflows/`, or another provider's config.
- The real commands: package scripts, Makefile, `pyproject.toml`, `docker-compose`, test config. CI runs the same commands a developer runs, never a parallel set.
- Services the tests need (Postgres, Redis) and the env vars they read.

**Done when** each gate below has a real command from this repo, or a note that the repo has no such check.

### 2. Write the pipeline

Gates, fastest first: lint, type check, unit tests, build, then integration tests with their services, then E2E if the repo has a suite, then a dependency audit.

- Trigger on `pull_request` to the default branch and on `push` to it.
- Cache dependencies (`actions/setup-node` `cache`, `actions/setup-python` `cache`, or `actions/cache`).
- Run independent gates as parallel jobs once the pipeline passes 10 minutes.
- Secrets come from the provider's secret store (`${{ secrets.X }}`), never from the file. CI never holds production secrets.
- Upload test reports or Playwright traces as artifacts on failure.
- Pin action versions to a major tag or a SHA.

A gate that fails today gets fixed, not disabled. If fixing it is out of scope, tell the user which gate and why before leaving it out.

### 3. Prove it locally

Run every gate's command locally, in order, and check each passes. Validate the workflow with `actionlint` when it is installed.

**Done when** every gate passed locally and the workflow file validates.

### 4. Maintain

When a change adds a new kind of check (a new test suite, a new package in a monorepo, a migration step), add it to the pipeline in the same branch. When a gate goes slow, cut time in this order: cache, parallel jobs, path filters, test sharding.

## Fix

### 1. Find the failure

- With a PR: `gh pr checks --json name,state,bucket,link,workflow`.
- Without one: `gh run list --branch <branch> --limit 5`.
- Read the failed log: `gh run view <run-id> --log-failed`. For an external check, follow its link.

Find the first actionable error, not the last line of the log.

**Done when** you can quote the failing command and its first real error.

### 2. Reproduce

Run the failing command locally on the same commit. If it passes locally, compare the environment: runtime version, env vars, service versions, lockfile, OS.

**Done when** the failure reproduces locally, or you have named the environment difference that explains it.

### 3. Fix the root cause

Make the smallest fix for the cause. Fix the code or the config; a skipped test, a disabled lint rule, or a raised timeout is not a fix. One failure at a time.

A flaky test is a bug: find the race or the shared state. Rerun a job with `gh run rerun <run-id> --failed` only when the log proves an infrastructure failure (runner lost, registry timeout).

Commit as `fix(ci): ...` or `fix: ...` with the cause in the body.

**Done when** the failing command passes locally and the other gates still pass.

### 4. Push and recheck

Invoking `/ci` to fix a branch is the ask to push that branch. Never force-push and never push to `main`. Push, then watch with `gh pr checks --watch` or `gh run watch`. Repeat from step 1 for the next failure.

**Done when** every check is green, or the remaining failure is outside this repo (a provider outage, a missing secret only the user can set).

## Report

Tell the user, in Portuguese: for **build**, the gates and the command each runs, and anything left out with the reason. For **fix**, each failure with its root cause and fix, in order, and the current check status.

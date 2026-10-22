---
name: perf
description: Optimize something slow or expensive with numbers before and after; keep only what measurably wins.
disable-model-invocation: true
---

# Perf

Measure, find the actual bottleneck, fix that one thing, measure again, keep or revert. A fix is a hypothesis until the second measurement. Every number goes through the `measure` skill: same case set, same conditions, interleaved runs, a named limiter.

Keep a ledger at `.queiroz/perf/LEDGER.md` for this project. Read it before proposing anything: an idea already reverted stays reverted unless the conditions changed.

## 1. Baseline

Name what is slow and for whom: the WhatsApp reply a lead waits for, an endpoint, a page load, a job. Pick the one metric the user feels (turn latency p95, endpoint p95, LCP, INP, cost per conversation) and a target if one exists.

Run `measure` steps 1 to 5 on the current code. For a web page, also dispatch the `web-perf-auditor` agent (`subagent_type: queiroz:web-perf-auditor`) with the URL or route and any Lighthouse, PageSpeed, or trace files you have; it returns a scorecard labeled by source and findings tagged as measured or potential.

**Done when** the baseline has a number, a run count, a spread, and a named limiter.

## 2. Identify the bottleneck

Find where the time or money goes, from a profile, a trace, query logs, or per-step timings logged during a run. Use [references/bottlenecks.md](references/bottlenecks.md) to pick what to measure from the symptom. A guess from reading code is a hypothesis to check, never the bottleneck.

Work out the ceiling before fixing: removing a piece that takes 10% of the turn makes the turn at most about 11% faster. If the ceiling is below the target, this piece is the wrong one.

**Done when** one bottleneck is named, with the evidence and its share of the total.

## 3. Fix that one thing

Change only what step 2 named. Three changes measured together produce one number nobody can attribute; if they must ship together, measure each alone first.

Correctness gates the metric. A "win" that skips a validation, caches what must be fresh (balances, permissions, availability at booking), drops a load-bearing `await`, or cuts context the agent needed to answer right is a regression. For the LLM engine, accuracy is part of the metric: measure it alongside speed and cost.

**Done when** the change is in, scoped to the bottleneck, and the tests pass.

## 4. Re-measure, keep or revert

Run `measure` again with the same case set, command, conditions, and budget. A cold-cache baseline against a warm-cache result measures the cache.

| Result vs baseline | Action |
|---|---|
| Past the bar and beyond noise, tests and accuracy intact | **Keep.** Commit with before → after in the message. |
| Within noise | **Revert.** |
| Worse | **Revert.** |
| Faster, but a test or the accuracy dropped | **Revert.** |

A neutral change is a revert: code you keep, you maintain forever.

Log every attempt in the ledger, kept and reverted alike:

| Date | Idea | Baseline → result | Verdict | Why |
|---|---|---|---|---|

**Done when** the change is kept or reverted and its ledger row is written.

## 5. Guard

Guard the metric the user feels, not every number available: a budget check in CI for reproducible regressions (comparing a median, so noise doesn't flake it), or an alert on the production metric (p95 turn latency, cost per conversation, field LCP/INP at p75). When a guard fires, start again at step 1 with a fresh baseline.

**Done when** the metric has a guard, or the user declined one.

## 6. Report

Tell the user in Portuguese: the metric before → after with run count and spread, the bottleneck and its evidence, what was kept and what was reverted, and the guard.

---
name: refactor
description: Rigorous audit and refactor of existing code without changing behavior. An orchestrator runs Opus lens analysts backed by Haiku search swarms, records every fact with its source, freezes behavior with characterization tests, executes the picked findings, and proves with measured numbers that complexity went down and parity held.
disable-model-invocation: true
---

# queiroz:refactor

Reduce complexity in code that already works, prove it with numbers, and prove nothing changed for the user. Two jobs in one skill: the **audit** (phases 0 to 2, read-only) and the **transformation** (phases 3 to 5). The user can stop after the audit. This skill runs its own pipeline; it does not go through `queiroz:mode`.

## Three rules for the whole run

1. **Parity.** Behavior is frozen, even where it is wrong. A bug found on the way goes to the bug list; fixing it is a separate change.
2. **No fact without a source.** Every claim about the code (a caller, a duplicate, an unused symbol, a number) enters the fact ledger with its file:line or command, and a separate agent re-checks it. A finding resting on an unchecked fact does not reach the user.
3. **No improvement without a number.** A finding states which metric it lowers and by how much. A ticket whose measured result does not lower it is reverted.

You are the **orchestrator**. You plan, dispatch, check, and decide. You do not read code in bulk and you do not write product code: subagents do, from pointers you give them with the `brief` checklist. Models and effort come from `../../models.md` (a value like `opus @high` means `model: opus` and `effort: high` on the `Agent` call). The protocol for swarms and the fact ledger is in [references/orchestration.md](references/orchestration.md). How each metric is measured is in [references/metrics.md](references/metrics.md).

Everything this run produces lives in one folder:

```
.queiroz/refactor-<slug>/
  files.tsv            # every in-scope file, split into slices
  coverage.tsv         # which swarm agent read each file
  symbols.tsv          # every definition in the codebase, with file:line
  map.md               # phase 0
  facts.tsv            # the fact ledger: id, claim, source, checked_by, status
  metrics-before/      # raw tool output, per file and per function
  diagnosis.md         # phase 2: numbered, proven findings
  baseline.md          # phase 3: what is frozen and where
  tickets/NN-<slug>.md
  evidence/<run>/      # <run> = AAAAMMDD-HHMM-<what>
  metrics-after/
  report.md            # phase 5
  log.md
```

## Cost gate (before anything runs)

This skill is heavy: it reads every file of the codebase and runs Opus at high effort per lens. Before dispatching any agent:

1. Count the in-scope files and lines (`git ls-files` minus vendored, generated, lock, and build files, then `wc -l`).
2. Estimate, and label it a rough estimate:
   - **map:** about 12 input tokens per line read by the Haiku swarm, plus about 5,000 per slice agent;
   - **analysis:** 8 Opus lens agents at high effort, about 150,000 to 300,000 tokens each with their fact swarms;
   - **proof, freeze, and transform:** grow with the number of findings picked; give a range per finding.
3. ✋ Tell the user in Portuguese, before spending:

   > "Isso vai analisar o codebase inteiro: <N> arquivos, <L> linhas, <S> fatias. Estimativa grosseira: ~<X> tokens no mapa (Haiku) e ~<Y> na análise (8 Opus em esforço alto), antes de qualquer mudança. Pode gastar bastante. Sigo, ou prefere limitar a uma pasta, ou fazer só a auditoria?"

   Say this every time the scope is the whole codebase, and also when a narrowed scope still maps a large codebase. Wait for an explicit yes.

**Done when** the user said yes to the scope and the estimate.

## 0. Scope and map (Haiku swarm, whole codebase)

The default scope is **the whole codebase**: every tracked source file. The user can narrow it to a folder, a module, or a branch diff (`main...HEAD`); even then the map covers the whole codebase, because callers, duplicates, and dead-code references live outside the narrowed part.

1. **Inventory.** `git ls-files` minus vendored, generated, lock, and build files → `files.tsv` (path, language, lines). Split it into slices: one per top-level package, and no slice above about 30 files or 6,000 lines. Every file belongs to exactly one slice.
2. **Map swarm.** One `refactor swarm` agent (Haiku) per slice, all in one message, in the background; for a big repo, waves of up to 20 agents until every slice is done. Each reads every file of its slice and returns ledger rows:
   - every definition (function, method, class, constant, route, job, CLI command, exported name) with file:line → `symbols.tsv`;
   - imports in and out per file;
   - entry points: routes, schedulers, webhooks, CLI, public exports, anything called by name from config or strings;
   - test files and what they import.
3. **Coverage check.** `coverage.tsv` marks each file of `files.tsv` with the slice agent that read it. A file nobody read is re-dispatched. The map is not done while any file is missing; what is deliberately skipped (generated, vendored) is listed with the reason.
4. **Metrics before.** The tools in [references/metrics.md](references/metrics.md) over the whole codebase, raw output to `metrics-before/`. Duplication runs across the whole codebase in one pass, so clones between distant folders show up.
5. **Map.** From the ledger and the metrics, write `map.md`: the module graph, dependency cycles, the most coupled modules, the hotspots (high CCN × many changes in `git log`), symbols with zero references (candidates only, proven in phase 2), and what has tests.

**Done when** `coverage.tsv` has every in-scope file read, `symbols.tsv` and `metrics-before/` cover the whole codebase, and `map.md` cites a ledger id for each claim.

## 1. Analyze (one Opus per lens, each commanding Haiku swarms)

Dispatch one `refactor lens` agent (**Opus, high effort**) per lens from [references/lenses.md](references/lenses.md), all in one message, in the background: **DRY**, **KISS**, **YAGNI**, **dead code**, **decoupling**, **modernization**, **structure**. One more on **correctness** feeds only the bug list. Each gets `map.md`, `symbols.tsv`, `facts.tsv`, `metrics-before/`, and its lens section, so it starts with a view of the whole codebase.

The Opus agent thinks; Haiku agents search. A lens agent never crawls the tree itself. When it needs a fact (all callers of X, every place this rule is computed, whether a symbol is referenced anywhere), it asks a Haiku swarm per [references/orchestration.md](references/orchestration.md), sliced like phase 0 so the answer covers the whole codebase: it spawns the swarm itself when its tools include `Agent`; otherwise it returns `FACT REQUESTS:`, you run the swarm, and you resume it with the answers.

Each lens agent returns candidate findings in the format of [references/lenses.md](references/lenses.md): the evidence as ledger ids, the change, and the **predicted metric delta**.

**Done when** every lens returned and every fact request was answered.

## 2. Prove the findings

For every candidate, before it reaches the user:

1. **Fact check.** A `fact checker` (Haiku), separate from whoever found it, opens each cited source and confirms the quote is there and says what the claim says. Mismatch → the fact is marked `wrong` and the finding is dropped or sent back to its lens once.
2. **Dead code needs two methods.** Two swarm agents search independently: one by symbol name across the whole tree (tests, fixtures, config, templates), one by entry points and dynamic use (routes, schedulers, webhooks, reflection, string lookups, public exports). Both must find nothing.
3. **Predicted delta is computed, not guessed.** For each finding, compute the metric delta from `metrics-before/`: the CCN and lines of the functions it removes or merges, the duplicated lines it eliminates, the imports it cuts. A finding whose number is not lower drops.
4. **Conflicts.** Two findings touching the same code: keep the one with the larger proven delta, or merge them into one.

Write `diagnosis.md`, numbered, ordered by proven delta per unit of risk, at most 25. Each finding: lens, where, what is wrong (with ledger ids), the change, **metric now → predicted**, risk, and how parity will be proven. Close with the bug list and `Não lido:`.

✋ Show the user the findings in Portuguese with the numbers, grouped by lens, and ask which to execute. Recommend a set. Stop here if the user only wanted the audit.

**Done when** every finding in `diagnosis.md` has only `checked` facts and a computed delta, and the user picked.

## 3. Freeze behavior

Create branch `queiroz/refactor-<slug>`. For the picked findings:

1. A `refactor swarm` maps what already covers each touched unit: tests that exercise it, `verify` features that reach it.
2. A `refactor implementer` (Opus, high effort) writes characterization tests where coverage is missing: today's output for representative and edge inputs (empty, zero, last item, rounding, time zones) and today's side effects (rows, messages, files), through the public seam a caller uses. Snapshots are fine for wide output.
3. **Mutation check.** For each new test, break the code under test briefly (flip a condition, drop a line) and confirm the test fails; restore. A test that stays green is rewritten.
4. Commit the tests alone: `test: characterize <area> before refactor`. Run the full suite and the relevant `verify` features; save to `evidence/<run>/` as the baseline. Record in `baseline.md` the commit and what each test freezes.

**Done when** every picked finding has a test or `verify` feature that fails when its behavior changes, and the baseline is saved.

## 4. Transform

One ticket per finding (format: [../design/references/ticket-template.md](../design/references/ticket-template.md)), with its Proof = parity + the predicted metric. Tickets with disjoint `touches` run in parallel, each a `refactor implementer` (Opus, high effort) in its own worktree. Each implementer:

- applies the change: a codemod for mechanical wide edits (the script goes to `evidence/`), expand–contract when many callers would break, a pure function or domain service when decoupling;
- keeps modernization inside the language and framework versions the project already declares;
- runs the characterization tests, the touched module's tests, and the ticket's metric command;
- runs `deslop` and `no-comments`, then one commit.

When each returns, you check it, then a `verifier` (separate) reruns on the integrated branch:
- characterization tests byte-identical to the baseline commit (only import paths may change), and green;
- the metric command: the number moved as predicted or better, and no function it touched got worse;
- Pass → `done`. Fail → revert the integration; one retry with a fresh implementer and the failure in the brief; a second failure drops the finding to the report's "não feito" with the data.

Conflicts → `merge`. A runtime or major-dependency upgrade is a migration: ✋ ask, separate run.

**Done when** every ticket is done or dropped with its data.

## 5. Validate and report

1. **Parity run.** Full suite plus every `verify` feature from `baseline.md`, into `evidence/<run>/`. Same results and side effects as the baseline.
2. **Independent review**, in one message: `blast` in after mode on the refactor diff, and a blind `reviewer` with only the diff and `baseline.md`, asked for lost or moved error handling, new boundary gaps, and behavior changes the tests missed.
3. **Metrics after.** Same tools, same scope, into `metrics-after/`. Compute the deltas per finding and in total.
4. Write `report.md` from [references/report-template.md](references/report-template.md) and tell the user in Portuguese, following `unslop`: what changed, the before → after table with the commands, predicted vs measured per finding, the parity proof with paths, the bug list, and what was not done. Last line: "Branch `queiroz/refactor-<slug>` pronto para PR. Não fiz merge nem push."

**Done when** parity matches the baseline, every number in the report traces to a file in `metrics-before/` or `metrics-after/`, and `report.md` exists.

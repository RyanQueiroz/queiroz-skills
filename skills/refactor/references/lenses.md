# Audit lenses

Each `refactor lens` agent takes one lens. Get facts from Haiku swarms (see [orchestration.md](orchestration.md)); reason about them yourself. No style taste, no "consider", no finding without a case.

Return at most 10 candidates as a table, one row each:

| # | where | evidence (ledger ids) | change | metric now → predicted | risk | parity proof |
|---|---|---|---|---|---|---|

Before the table, list any `FACT REQUESTS:` still open. The predicted metric is computed from `metrics-before/` per [metrics.md](metrics.md): name the metric (CCN, NLOC, duplicated lines, imports) and both numbers.

## DRY

Duplicated logic across files and modules, not just identical lines.

- The same rule computed in two places (a price, a status, a date boundary). They will drift: that is the bug the merge prevents.
- Near-copies that must change together: same shape, different names.
- A bespoke helper where the codebase already has a canonical one: name the one to keep.

Merge only what changes for the same reason. Two blocks that look alike but serve different rules stay apart: a shared helper with a flag per caller is worse than the duplication.

## KISS

Dense logic that a simpler form expresses with the same behavior.

- Nested conditionals that a lookup table, an early return, or a single expression replace.
- Long functions that mix steps: split into named steps only when each step is a real concept.
- Clever code (meta-programming, generic machinery) hiding a simple data shape.
- Flags and modes threaded through calls: often one function per mode is simpler.

## Dead code

Code no execution path reaches. Facts come from two independent swarm searches (by symbol name across the whole tree; by entry points and dynamic use: routes, schedulers, webhooks, reflection, string lookups, public exports). Both must come back empty.

- Unused functions, classes, routes, config keys, feature flags, env vars, dependencies.
- Branches whose condition can never be true, given the callers' actual arguments.
- Tests that only exercise dead code go with it.

## YAGNI

Code for problems that do not exist.

- Options, parameters, or branches no caller ever passes.
- Interfaces with one implementation, factories with one product, wrappers that only pass calls through.
- "For later" scaffolding: hooks, plugin points, abstract bases nobody extends.

## Decoupling (SOLID)

A unit doing several jobs, or business rules tied to I/O.

- A class or module with several reasons to change: name each reason.
- Business rules (validation, calculation, state transitions) inside handlers, ORM models, views, or templates. The move: a pure function or domain service, with I/O at the edges.
- Circular dependencies and modules that import half the codebase.
- Feature logic leaking into shared code through special-case branches.

## Modernization

Verbose constructs the project's current language and framework versions already replace. Read the declared versions first (`pyproject.toml`, `package.json`, `go.mod`, `pom.xml`, ...) and stay inside them.

- Manual loops a comprehension, `map`/`filter`, or stream expresses directly.
- Boilerplate data classes a record, `dataclass`, or typed model replaces.
- Hand-rolled utilities the standard library ships.
- Deprecated APIs with a drop-in replacement in the current version.

A version upgrade is not a finding: it is a migration, reported separately.

## Structure (code judo)

Restructurings that delete whole categories of complexity rather than move them.

- A reframing of the state model that makes a family of conditionals disappear.
- Logic in the wrong layer whose move makes the call sites simpler.
- Files over 1000 lines that hold several concepts.
- Sequential steps that are independent, or related writes that can leave state half-applied.

A refactor that moves complexity around without reducing the number of concepts a reader holds is not a finding.

## Correctness (bug list only)

Bugs, security holes, data loss, and what breaks under the expected load: missed edge cases, unchecked input at a boundary, swallowed errors, check-then-write races, a query per item. These go to the report's bug list. The refactor does not fix them.

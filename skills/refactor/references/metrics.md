# Metrics

Every number in `diagnosis.md` and `report.md` comes from a file in `metrics-before/` or `metrics-after/`, produced by a command written next to it. Prefer the stack's own tool when the repo already uses one; otherwise these work for most languages.

| Metric | Command | Unit |
|---|---|---|
| Complexity per function | `uvx lizard --csv <scope> > metrics-*/lizard.csv` | CCN, NLOC, params, per function |
| Functions above CCN 10 | `uvx lizard -C 10 -w <scope>` | count |
| Duplication | `npx jscpd --reporters json --output metrics-*/jscpd <scope>` | duplicated lines, clone pairs |
| Lines per file and language | `cloc --by-file --csv <scope>` (or `git ls-files <scope> \| xargs wc -l`) | lines |
| Files over 1000 lines | from the line counts | count |
| Fan-out and fan-in per module | swarm: imports per file, as ledger rows | imports |
| Dependency cycles | the stack's tool (`pydeps --show-cycles`, `madge --circular`) or the swarm's import table | count |
| Dependencies | the manifest (`pyproject.toml`, `package.json`, ...) | count |
| Churn hotspots | `git log --since=6.months --format= --name-only <scope> \| sort \| uniq -c \| sort -rn` | changes per file |

## Per finding

- **Predicted delta** (phase 2): from `metrics-before/`, sum what the change removes or merges. Example: merging three copies of a 40-line block with CCN 6 → −80 NLOC, −2 clone pairs, −12 CCN total.
- **Measured delta** (phase 4): rerun the same command on the ticket's files after the change and diff against `metrics-before/`.
- A ticket passes when the targeted metric is at or below the prediction and no touched function's CCN went up.

## Report totals

Before → after for: total NLOC, average CCN, functions above CCN 10, duplicated lines, files over 1000 lines, dependency cycles, dependencies. State the scope and the commands. A metric that did not move is shown as unchanged, not hidden.

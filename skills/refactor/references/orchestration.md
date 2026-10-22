# Orchestration: swarms and the fact ledger

## Roles

| Role (models.md) | Does | Never does |
|---|---|---|
| orchestrator (session) | Plans, dispatches, checks returns, decides, writes `diagnosis.md` and `report.md` | Reads code in bulk, writes product code |
| `refactor lens` (Opus, high) | Reasons about one lens, proposes findings and their predicted delta | Crawls the tree file by file |
| `refactor swarm` (Haiku) | Answers one narrow fact question with sources | Judges whether something is good or bad |
| `fact checker` (Haiku) | Opens a cited source and confirms the claim | Checks facts it gathered itself |
| `refactor implementer` (Opus, high) | Writes characterization tests and applies one ticket | Touches files outside its ticket |
| `verifier` | Reruns parity and metrics on the integrated branch | Trusts the implementer's summary |

## Swarm protocol

A fact request is one question with one answer shape:

```
Q: every call site of `calcular_saldo` in backend/ and its tests
Return: one row per site: file:line, the line quoted, the calling function
```

- **Split wide questions.** One swarm agent per slice (package, folder, or about 30 files), all in one message, in the background. Ten small agents beat one big one: each keeps a clean context.
- **Exact searches first.** Each agent uses `git grep -n`, `rg`, or the language's own tools, and pastes the matching line. It reports what it searched and where, so "nothing found" is checkable.
- **Raw answers only.** The agent returns rows, not opinions. Interpretation is the lens agent's job.
- **Who spawns.** A lens agent whose tools include `Agent` spawns its own swarm. Otherwise it returns `FACT REQUESTS:` with the questions; you dispatch the swarm and resume the same lens agent with `SendMessage`, passing the ledger ids of the answers.

## The fact ledger

`facts.tsv`, one row per fact, appended only by you:

```
id	claim	source	gathered_by	checked_by	status
F012	`legacy_export` has no reference outside its file	git grep -n legacy_export (0 hits outside app/export.py)	swarm-3	checker-1	checked
```

- `source` is a file:line with the quoted text, or a command plus its relevant output.
- `status`: `raw` (gathered), `checked` (a different agent confirmed it), `wrong` (the check failed).
- A finding may cite only `checked` facts. A `wrong` fact sends its finding back to the lens once; a second `wrong` drops it.
- Lens agents and implementers receive the ledger path, not pasted facts. Their summaries cite ids.

## Context hygiene

- Every brief carries pointers (paths, ledger ids, ticket file), never pasted code or prior summaries.
- Every return is size-capped (a table of findings or rows, no essays). A return that exceeds it is re-asked for the table only.
- A fresh agent per task. Resume an agent only to answer its own fact requests.
- Your own judgment comes from reading the ledger, the diffs, and the metric files, never from an agent's "done".

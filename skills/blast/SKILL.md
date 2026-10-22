---
name: blast
description: Blast radius with proof. Finds what a change breaks beyond grep (JSON contracts, DB columns, webhooks, flags, indirect consumers) and proves the one fact its safety depends on by running code. Use for "blast radius", "what could this break", before tickets when a spec asserts something about existing code, or at the end against the full diff.
---

# queiroz:blast

Find what a change breaks somewhere else, and prove the fact it is safe because of. Listing callers is not the job; grep does that in a second. The job is the breakage grep misses.

Inside `queiroz:mode` this runs as a subagent with role `blast` (model per [`../../models.md`](../../models.md)), dispatched through `brief`. Called directly, run it in the session.

## Modes

- **Before tickets.** Input: `.queiroz/<feature>/spec.md`. Every claim the spec makes about existing code ("X already handles Y", "make endpoint Z public", "column W is unused") is a hypothesis. The consumer census decides the design, so the tickets get built on proven facts. Output: `.queiroz/<feature>/blast/before.md`.
- **At the end.** Input: the full diff, `git diff <base>...HEAD`. Runs in parallel with the blind reviewer. Each confirmed risk becomes a fix ticket. Output: `.queiroz/<feature>/blast/after.md`.

Leave product code untouched. The reports (`before.md`, `after.md`) and the proof scripts live in `.queiroz/<feature>/blast/`, so anyone can rerun them.

## Ladder of certainty

Every fact the change's safety depends on gets pushed down this ladder as far as is cheap, and says where it stopped:

1. **suposição**: you said so. Worth nothing alone.
2. **linha citada**: a real `file:line`, or the library's own source at its pinned version.
3. **falha descartada**: you walked the failure step by step and it does not reach.
4. **script rodado**: a script or test calls the real code and fails loud if you are wrong.
5. **reproduzido no app**: driven through the project's `verify`, with evidence.

A fact that stops at 1 is written **não provado**. A writeup that sounds right reads the same whether or not it is true, so the proof is what you hand back.

## 1. Read the change

Before tickets: list each spec assertion about existing code, and each symbol, route, table, or payload the spec will touch. At the end: read the diff, the symbols added, changed, and deleted, and what now behaves differently, including what the diff does not spell out.

**Done when** every touched symbol and every spec assertion is on a list.

## 2. Find the one fact

Most risky-looking changes are safe because of one fact, such as "this handler only reads rows the job already marked done". Find it. If it holds, most risks clear at once. Spend your time here, not on a long list of maybes. Some changes have two; rarely more.

**Done when** the fact is written as one falsifiable sentence.

## 3. Look where grep stops

For each touched item, follow its consumers past the symbol search:

- **Wire contracts:** JSON an API returns, payloads a webhook sends or receives, events on a queue. Who parses them, including other repos and the frontend.
- **Data:** DB columns, indexes, constraints, migrations, and the jobs or reports that read them.
- **Config:** feature flags, env vars, cron schedules.
- **Libraries:** the source of what you call, at the pinned version, plus any local patch.
- **Timing:** when things run: retries, async jobs, teardown, a webhook arriving twice.
- **Indirect:** code two or three hops downstream, another language reading the same bytes, a string-built route or column name.

A search that finds nothing is an answer; write the search. Never invent a caller or an API.

**Done when** each touched item has its consumers listed with `file:line`, or the search that found none.

## 4. Rate each risk

For each risk: how it breaks, `file:line`, a real likelihood and a real cost. Keep confirmed risks. List the ones you checked and cleared separately, with why.

**Done when** every consumer from step 3 is either a risk or cleared.

## 5. Prove the fact

Write the smallest script or test that imports what the app ships and calls the exact code you depend on. Run it and keep the output. When the fact is about behavior the user sees, drive it through `verify` and save the evidence. If you cannot prove it, say why and mark it **não provado**.

**Done when** the fact has reached step 4 or 5 of the ladder, or carries **não provado** with the reason.

## Report

Write it in Portuguese, under 600 words, to the mode's output file, and return its path with a three-line summary.

- **O que muda:** the change, including the non-obvious part.
- **Fato de segurança:** the fact, its ladder step, and the proof (command and trimmed output), or **não provado**.
- **Afirmações da spec** (before tickets): each one confirmed, refuted, or **não provado**, with its step.
- **Riscos:** how it breaks, `file:line`, likelihood, cost, how to check.
- **Descartados:** what you checked and why it is fine.
- **Antes de seguir:** the cheapest test or repro that catches the real bug, with the script path.

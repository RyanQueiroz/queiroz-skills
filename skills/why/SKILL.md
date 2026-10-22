---
name: why
description: Find out why code, a decision, or a threshold is the way it is, with a cited answer from git, PRs, issues, docs, and chat.
disable-model-invocation: true
---

# Why

Find the forces that shaped a piece of code: the rationale, the tradeoff, the incident, the customer ask. `how` answers what the code does; `why` answers why it is that shape. Code shows mechanics, never motivation, so the motivation comes from the record around it.

Work as a careful investigator. Every claim carries a confidence tier from [`references/epistemics.md`](references/epistemics.md); read it before step 4.

## 1. Pin the target and the question

The **target** is the code, pattern, feature, or decision. The **question** is the kind of why: rationale, tradeoff, motivating edge case, external constraint, dead code, a threshold's origin, a regression. If the referent is vague, take the best guess from the conversation, state it in one line, and proceed.

A user's embedded guess ("acho que é por performance?") is one hypothesis among others, never the conclusion.

**Done when** target and question are stated to the user in one line.

## 2. Anchor in code

Build the seed context yourself:

```bash
git blame -L <start>,<end> <file>
git log --follow --oneline -20 -- <file>
git log -S '<exact string>' -- <file>     # who added or removed this text
git log -1 --format=%B <commit>           # PR numbers like (#1234), ticket IDs
gh pr view <n> --json title,body,author,mergedAt,closingIssuesReferences,comments,reviews
```

Trace back past the latest commit: the current shape is often an accretion of older decisions, and the last touch is rarely the origin.

**Done when** you hold file paths with line ranges, key symbols, the commits that shaped the target, and every PR number and ticket ID they mention.

## 3. Investigate in parallel

List the evidence sources this session can reach: git and `gh` always, plus every MCP in the tool list (`mcp__<server>__*`). Map each to one category: source control, issue tracker, long-form docs, team chat, observability, error tracking, analytics warehouse. That list is the **coverage map**.

Spawn one investigator per category that has a source, all in one message: `subagent_type: general-purpose` (it keeps MCP access), model per the `investigator` role in [`../../models.md`](../../models.md). Each gets [`references/investigator-prompt.md`](references/investigator-prompt.md) filled with the question, the anchor, and its single category. One investigator per category; none covers two.

A category is skipped only with a written reason: no source exists here (a gap), or it is provably irrelevant (a build script has no runtime errors to track). A one-commit target whose PR body already answers fully may be answered inline; say so.

**Done when** every category in the coverage map has returned findings or carries a written skip reason.

## 4. Synthesize

You are the synthesizer. Merge duplicate citations, surface contradictions instead of picking the tidier story, and place each claim in its tier. Spot-check any citation you doubt by opening it.

**Done when** every claim in "O que achamos" has a citation, and the calibration check in `epistemics.md` passes.

## 5. Answer

Reply in Portuguese, in this structure:

- **A pergunta.** One or two sentences.
- **O código.** Paths, line ranges, symbols.
- **O que achamos.** `[Direto]` and `[Sustentado]` claims, each with its citation.
- **O que dá para inferir.** `[Inferido]` claims with the inference chain, hedged.
- **Hipóteses concorrentes.** When the record fits several stories: each with evidence for and against.
- **O que não sabemos.** Concrete gaps: what was searched, where, and who would likely know.
- **Fontes consultadas.** One line per category, including empty and skipped ones with the reason.
- **Confiança.** One or two sentences.

If the question precedes a change to this code, close with **Preservar / Mudar / Evitar / Risco**: the constraints the findings put on that change.

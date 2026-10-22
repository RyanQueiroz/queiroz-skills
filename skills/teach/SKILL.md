---
name: teach
description: Explain a body of work (a change, a subsystem, a decision) so you truly understand what it is, how it works, and why.
disable-model-invocation: true
---

# Teach

Explain what a thing is, how it works, and why it is built that way, in one plain account at the user's pace. The goal is that they understand it. Nothing in the code changes.

`how` and `why` do the digging; teach turns their findings into understanding. Both are user-invoked, so follow their files directly: [`../how/SKILL.md`](../how/SKILL.md) and [`../why/SKILL.md`](../why/SKILL.md).

## 1. Pick the takeaways

Decide the few things the user should walk away understanding. Choose them from why they are asking (about to change it, reviewing it, debugging it, new to it) and what they already know, both read from the conversation rather than asked. Skip what they plainly know. Put depth where their question is.

**Done when** you can name two to four takeaways, each tied to the reason they asked.

## 2. Dig

Read the code yourself to get oriented. Then run `how` for how it works and `why` for why, in parallel. Size them to the question: a subsystem gets both; a small change may need one. Keep `why` narrow by default (git plus the one or two sources likely to hold the answer, the skipped categories recorded as its contract requires) and widen it only when the reasons are the point.

For a concept from outside this codebase (a protocol, a library, a pattern), back it with the official docs, not memory.

**Done when** every takeaway rests on a file, a commit, or a doc you read.

## 3. Explain, smallest first

Start with a plain definition: name the thing, say what it is in general terms with its common name if it has one, then tie it to this case ("aqui, usamos isso para ..."). Build up from there: how it works, the deeper reasons, the edge cases. For each part, give the problem it solves and the mechanism that solves it. When it helps, walk through what happens as the user does the thing (opens the page, the webhook arrives). A list of functions and constants is reference, not teaching.

Give the smallest complete answer first, a sentence or two, then stop. Add layers when they ask.

**Show it.** Open the diff or the code when that lands fastest. For three or more moving parts, draw a short series of mermaid or ASCII diagrams where each redraws the last and adds one part (A to B; then A to B to C; then the return edge), so the user watches the system assemble. One all-at-once diagram at the end is reference. A single simple point needs no figure.

Keep `why`'s confidence language intact: its hedges are findings, not style.

## 4. Follow their lead

Keep it a conversation. After each layer, offer to go deeper or move on, and let them steer. Ask nothing back as a quiz, and print no framing labels ("o ponto-chave", "a parte difícil", "resumindo"): just say the thing. With no live user, deliver it in one pass and put the offer to go deeper at the end.

**Done when** the user says they have it or moves on, or every takeaway from step 1 has been delivered.

## Voice

Portuguese, plain and spoken, through `unslop`. Tight, not terse: cut filler and hedging, keep the part that makes it click. State the concrete mechanism, not a metaphor. Target density: "A virtualização tem duas partes: uma renderiza, outra carrega do disco. Quando um item sai do buffer, o nó do DOM e os dados em memória saem juntos." Prefer periods to commas; split piled-up clauses. Give each concept one name and keep it. Code and identifiers stay in English.

**Reply:** the explanation itself, never a report about what you did. Lead with the main point, then the account, then the threads worth chasing with `how` or `why`.

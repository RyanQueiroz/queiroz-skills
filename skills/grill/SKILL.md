---
name: grill
description: Interrogate a plan or idea in rounds until no decision is left open.
disable-model-invocation: true
---

# Grill

Interview the user relentlessly until you reach a shared understanding. Map the work as a **design tree**: every decision branches into the decisions that hang off it.

Input is whatever the user gives: a sentence, a `.queiroz/<feature>/idea.md` from `idea-refine`, a draft spec. Output is a conversation that `/spec` can synthesize with no further questions.

## Facts versus decisions

**Facts** are yours to find, never the user's. A fact is anything the environment can answer: how the code does it today, which tables exist, what a webhook payload carries, which version is installed. Send an `explorer` subagent for each fact (model per `../../models.md`), in the background. A running exploration is an unsettled prerequisite: only the questions downstream of it wait; ask the rest of the frontier now. A question about an external API's behavior goes to `/research`; tell the user it is worth running and keep going.

**Decisions** are the user's: what the product should do, which tradeoff to take, what is out of scope. Put each one to them and wait.

## 1. Ground the tree

Read what the user handed you. Dispatch explorers for the code facts the first decisions depend on. Sketch the tree's top branches for yourself: the user-visible behavior, the data it touches, the edges (external input, auth, money, personal data), and how we will know it works.

**Done when** the first frontier is known and every fact it needs is either found or being found.

## 2. Ask in rounds

The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round. Number each question and give your recommended answer, grounded in the facts the explorers found. Then wait.

Write each round in Portuguese, in this format:

```
❓ **P1** - **<título da pergunta>**: <corpo da pergunta, pode ter vários parágrafos e opções>

➡️ <sua resposta recomendada e por quê>

---

❓ **P2** - **<título da pergunta>**: <corpo>

➡️ <resposta recomendada>
```

A question whose answer depends on another question still open in this round belongs to a later round. Keep "how will we prove this works" on the tree: the user-visible action, the result they see, and the side effect in the database or files. `/spec` turns those answers into its "Como provamos" section.

**Done when** the user has answered the round.

## 3. Recompute and repeat

Each answer reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Fold in explorer reports as they land. Recompute the frontier and ask the next round. When an answer contradicts a fact from the code, show the fact and ask again.

**Done when** the frontier is empty: every branch visited, nothing left silently assumed.

## 4. Close

Post a numbered list, in Portuguese, of every settled decision and every fact it rests on (with its source file). Ask the user to confirm this is the shared understanding. Act on nothing until they confirm. Then suggest `/spec` as the next step.

**Done when** the user confirms the list.

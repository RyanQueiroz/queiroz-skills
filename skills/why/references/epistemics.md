# Epistemics

Code does not carry its own motivation. The record around it (commits, PRs, tickets, docs, chat) is incomplete and sometimes wrong. A confident guess misleads the user, who will act on it. An honest "não sabemos" is a valid result.

## Tiers

Every claim sits in one tier. The tier decides its section and its wording.

| Tier | What it takes | Wording (PT) |
|---|---|---|
| `[Direto]` | Someone wrote why: a PR body, ticket, comment, doc, or chat message that answers the question. | Plain, with "porque", citation adjacent. |
| `[Sustentado]` | Several indirect items converge (perf label + perf ticket + commits on the same hot path). | "As evidências apontam para X: ..." with each item cited. |
| `[Inferido]` | A reasonable reading with no explicit support. | "Parece", "provavelmente", "sugere", "é consistente com", with the chain: "dado A e B, C parece provável porque D". |
| `[Especulativo]` | Plausible, thin evidence, other stories fit as well. | "Uma possibilidade é X, mas não há evidência direta." Lives in Hipóteses concorrentes. |
| `[Desconhecido]` | Searched and not found. | "Buscamos X em A, B e C e não achamos." Name the queries. |

"Porque", "foi feito para", "corrige", "o time decidiu" are causal claims: use them only with a citation next to them. Leave out "obviamente", "claramente", "é só".

## Rules

- **Code is not evidence of its own intent.** A function name, a style, a constant's value show mechanics. Only what an author wrote shows motivation.
- **Human rulings keep their scope.** When the exact scope of a decision matters, find the person's original words with source and speaker. An agent's summary is labeled as one. Several notes copying one summary are one evidence chain, not independent confirmation. Original missing: say so and leave the scope open.
- **Contradictions are findings.** The ticket says compliance, the PR says tech debt: show both with citations.
- **No rationalization.** The author may have been wrong, or copied a pattern. Absence of evidence is not evidence of absence.
- **Correlation is a lead.** An error that stops after a release suggests the fix; another change in the same release may be the cause.

## Calibration check

Before answering, for every claim:

1. Has a citation, or moves to Inferido or Hipóteses.
2. Wording matches its tier.
3. Does not cite the code for its own intent.
4. "O que não sabemos" exists and names specific searches. An empty one is suspicious.
5. The user's embedded guess was tested, not stamped.

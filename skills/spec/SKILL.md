---
name: spec
description: Turn the current conversation into .queiroz/<feature>/spec.md, with the "Como provamos" scenarios verify will run.
disable-model-invocation: true
---

# Spec

Synthesize what has already been discussed into a spec that `queiroz:mode` can implement. This is synthesis, not an interview: the decisions were made in the conversation (usually a `/grill`), and your job is to write them down faithfully.

The spec is written in Portuguese, for the user and for `queiroz:mode`. Its section headings are fixed: `queiroz:mode` looks for "Como provamos" by name.

## 1. Gather

Read the conversation, plus any `.queiroz/<feature>/idea.md`, `.queiroz/research/*.md`, and prototype verdicts it mentions. Send `explorer` subagents (model per `../../models.md`) for the current state of the code the feature touches: modules, data shapes, existing tests, and the project's `verify` feature map (`.claude/skills/verify/features/`). Use the project's own vocabulary throughout.

Pick `<feature>`, a short kebab-case slug. If the conversation bundles capabilities that could ship and be proved separately (each with its own data and users), propose one spec per capability and a build order, and wait for the user's choice.

**Done when** every claim the spec will make about existing code has a source, and the scope is one feature.

## 2. Write `.queiroz/<feature>/spec.md`

```markdown
# Spec: <nome da feature>

## Problema
<o problema do ponto de vista de quem usa>

## Solução
<a solução do ponto de vista de quem usa>

## Histórias de usuário
1. Como <ator>, quero <comportamento>, para <benefício>.

## Decisões de implementação
- <módulos criados ou alterados, interfaces, schema, contratos de API e webhook, interações>

## Como provamos
1. **<nome do cenário>**
   - Pré-condição: <estado inicial, dados de teste>
   - Ação: <o que o usuário faz, pelo caminho real>
   - Resultado visível: <o que ele vê: tela, resposta, mensagem>
   - Efeito: <linha no banco, arquivo, mensagem enviada, ou "nenhum">

## Suposições
- <o que a conversa não disse e você assumiu>

## Fora do escopo
- <o que fica de fora e por quê>

## Perguntas em aberto
- <decisão que a conversa não fechou>
```

Rules per section:

- **Histórias de usuário:** only stories that change behavior. Short. Skip the ones that restate the solution.
- **Decisões de implementação:** decisions, not code. No file paths or snippets, they go stale. Exception: a snippet a prototype validated (state machine, schema, type shape), trimmed to the decision and marked as coming from the prototype.
- **Como provamos:** the scenarios the project's `verify` skill will run. Every behavior-changing story has at least one scenario. Cover the happy path, each failure the user can trigger (invalid input, missing permission, duplicate webhook), and each edge where money, auth, or personal data is involved. Every scenario names a visible result and a checkable effect, so a vague requirement becomes a test: "mais rápido" becomes "a lista carrega em menos de 500 ms com 1.000 alunos". When a scenario needs something `verify` can't drive yet (a sandbox credential, a new harness), say so in the scenario.
- **Suposições** and **Perguntas em aberto:** list them instead of silently filling the gap. An open question on a behavior-changing decision blocks the spec.

**Done when** every section is filled and every behavior-changing story maps to a "Como provamos" scenario.

## 3. Hand it to the user

The definition of done belongs to the user. Show, in Portuguese:

- The path to the spec.
- The "Como provamos" scenarios, in full, and ask the user to confirm or correct them.
- The assumptions and open questions.

A spec without confirmed "Como provamos" scenarios is not ready. Apply the user's corrections to the file. Then stop: the next step is the user telling `queiroz:mode` to implement `.queiroz/<feature>/spec.md`.

**Done when** the user confirmed the scenarios, the file reflects their corrections, and no open question blocks the spec.

# Inventário: tudo das 3 stacks contra o Queiroz

Cada skill, agente e comando das três stacks, agrupado por função.

Fontes: **O** = osmani (`agent-skills` 0.6.13), **P** = pstack 0.9.67, **M** = mattpocock 1.2.3.

| Marca | Significado |
|---|---|
| ✅ | Coberto no desenho do Queiroz (diz por qual peça) |
| ➕ | Você decidiu que entra (ainda não está no desenho) |
| 🟡 | Coberto em parte |
| ❌ | Falta, para você decidir |
| ⛔ | Fora de propósito (nicho, ou o tanque que não queremos) |

## 1. Núcleo e roteamento

| Skill | Fonte | O que faz | Queiroz |
|---|---|---|---|
| using-agent-skills | O | Meta-skill: árvore de decisão de qual skill usar | ✅ núcleo |
| poteto-mode | P | Modo sempre ligado + 23 playbooks + autonomia | ✅ núcleo + `queiroz:mode` |
| ask-matt | M | Roteador: qual skill serve para minha situação | 🟡 núcleo item 11 aponta o `queiroz:mode`; não roteia as demais |
| context-engineering | O | Montar o contexto certo para o agente | ➕ |
| principle-guard-the-context-window | P | Mandar volume para subagentes, manter resumos | 🟡 idem |

## 2. Descobrir e planejar

| Skill | Fonte | O que faz | Queiroz |
|---|---|---|---|
| grilling / grill-me | M | Perguntas em rodadas com resposta recomendada | ✅ `grill` |
| interview-me | O | Entrevista uma pergunta por vez para achar o que você quer de verdade | 🟡 `grill` cobre |
| idea-refine | O | Ideia vaga → variantes (divergir) → conceito afiado (convergir) | ➕ |
| grill-with-docs | M | Grill que já escreve glossário e ADRs | ❌ |
| loop-me | M | Grill sobre workflows a construir | ⛔ |
| to-questionnaire | M | Decisão que você não sabe → questionário para outra pessoa | ❌ |
| spec-driven-development | O | Spec antes do código | ✅ `spec` |
| to-spec | M | Sintetiza a conversa em spec | ✅ `spec` |
| constraint-driven-development | O | Barra de qualidade escrita como contrato (o agente não pode baixar) | ❌ |
| planning-and-task-breakdown | O | Spec → tarefas ordenadas | ✅ `queiroz:mode` / `queiroz:design` |
| to-tickets | M | Fatias verticais com bloqueios | ✅ `queiroz:mode` / `queiroz:design` |
| wayfinder | M | Planejar trabalho gigante (várias sessões) como mapa de decisões | ❌ |
| figure-it-out | P | Playbook sob medida para migração grande | ❌ |
| triage | M | Issues → estados (needs-info, ready-for-agent...) | ⛔ |
| prototype | M | Esboço descartável para decidir vendo | ➕ |
| principle-exhaust-the-design-space | P | 2-3 protótipos concorrentes antes de decidir | 🟡 `queiroz:design` |

## 3. Desenho e arquitetura

| Skill | Fonte | O que faz | Queiroz |
|---|---|---|---|
| architect | P | Tipos e assinaturas antes do código, multi-modelo | ✅ `queiroz:design` (com síntese) |
| arena | P | N candidatos paralelos, escolhe base, enxerta | ✅ `queiroz:design` (síntese em vez de escolha) |
| interrogate | P | Revisão adversarial multi-modelo: vários modelos atacam a mudança | ➕ |
| api-and-interface-design | O | APIs estáveis, contratos, versionamento | ❌ |
| codebase-design | M | Vocabulário de módulos profundos (interface pequena, muito escondido) | ❌ |
| improve-codebase-architecture | M | Varre o repo atrás de módulos para aprofundar, relatório HTML | ❌ |
| domain-modeling | M | `CONTEXT.md` (glossário) + ADRs | ❌ |
| documentation-and-adrs | O | Registrar decisões de arquitetura | ❌ |
| setup-ts-deep-modules | M | dependency-cruiser para módulos em TS | ⛔ |

## 4. Implementação

| Skill | Fonte | O que faz | Queiroz |
|---|---|---|---|
| implement | M | Implementa spec/tickets, tdd, review, commit | ✅ `queiroz:mode` |
| implement-spec | M | Fronteira de tickets, subagentes **paralelos** em worktrees, merger | 🟡 `queiroz:mode` faz em sequência; ➕ paralelo |
| incremental-implementation | O | Fatias finas, cada uma verificável | ✅ ticket → verify → commit |
| swarm | P | N workers paralelos, um relatório (cobertura, corridas) | ➕ paralelismo |
| source-driven-development | O | Cada decisão checada na documentação oficial | ➕ |
| research | M | Pesquisa em fontes primárias → arquivo Markdown | ➕ |
| frontend-ui-engineering | O | UI acessível, responsiva, de produção | ➕ |
| typescript-best-practices | P | Regras de TS | ⛔ (seu stack é Python) |
| wizard | M | Script bash que guia o humano em passos que só ele faz (credenciais, infra) | ❌ |
| deprecation-and-migration | O | Remover sistemas antigos, migrar usuários | ❌ |
| principle-migrate-callers-then-delete-legacy-apis | P | Migrar chamadores e apagar a API velha na mesma leva | ❌ |
| principle-outcome-oriented-execution | P | Em migração, ir direto ao alvo sem compatibilidade descartável | ❌ |

## 5. Verificação e testes

| Skill | Fonte | O que faz | Queiroz |
|---|---|---|---|
| create-verification-skill | P | Gera a `verify` do projeto (launch/doctor/drive/evidence/cleanup) | ✅ `queiroz:setup` |
| maintain-verification-skill | P | Mantém o mapa de features honesto | 🟡 `queiroz:mode` atualiza ao entregar; manutenção avulsa ❌ |
| principle-prove-it-works | P | Provar no artefato real | ✅ núcleo |
| browser-testing-with-devtools | O | Testar no navegador real via DevTools | 🟡 dentro da `verify` |
| test-driven-development | O | Red-green-refactor | 🟡 só no caminho de bug |
| tdd | M / P | TDD em seams combinados | 🟡 idem |
| principle-test-behavior-not-implementation | P | Teste que pega o defeito real | ❌ não está no núcleo |
| agente test-engineer | O | Estratégia de testes, cobertura | ❌ |
| benchmark-checklist | P | Validar uma medição antes de reportar | ➕ |
| principle-explain-the-number | P | Explicar o que limita um número | ➕ |

## 6. Debug e performance

| Skill | Fonte | O que faz | Queiroz |
|---|---|---|---|
| debugging-and-error-recovery | O | Triagem de causa raiz, parar a linha | ➕ |
| diagnosing-bugs | M | Loop de diagnóstico para bugs difíceis e regressões | ➕ |
| principle-fix-root-causes | P | Causa raiz, reproduzir primeiro | ✅ núcleo + caminho de bug |
| principle-attack-the-premise | P | Testar a suposição comum de correções que falham | ✅ núcleo |
| performance-optimization | O | Performance front/back/queries | ➕ |
| agente web-performance-auditor | O | Core Web Vitals | ➕ |

## 7. Revisão e qualidade

| Skill | Fonte | O que faz | Queiroz |
|---|---|---|---|
| code-review-and-quality | O | Revisão em 5 eixos | ✅ reviewer cego |
| code-review | M | Revisão em 2 eixos paralelos: padrões do repo × spec | 🟡 reviewer cego vê só a spec |
| agente code-reviewer | O | Revisor sênior | ✅ reviewer |
| blast-radius | P | O que quebra fora do diff, com prova | ✅ `queiroz:blast` |
| doubt-driven-development | O | Toda decisão não trivial passa por revisão adversarial de contexto limpo | ➕ |
| security-and-hardening | O | Endurecer contra vulnerabilidades | ❌ |
| agente security-auditor | O | Auditoria de segurança, threat model | ❌ |
| code-simplification | O | Simplificar sem mudar comportamento | 🟡 núcleo (menor diff) |
| deslop | P | Tirar "slop" de IA do código | ➕ |
| no-comments + agente comment-sicko | P | Caçar comentários desnecessários | ➕ |
| thermo-nuclear-code-quality-review | P | Revisão brutal de manutenibilidade | ❌ |
| principle-minimize-reader-load | P | Menos camadas para o leitor | ❌ |
| correct | P | Achar erros que os agentes repetem no repo e torná-los impossíveis (tipo, lint) | ❌ |

## 8. Git, PR e entrega

| Skill | Fonte | O que faz | Queiroz |
|---|---|---|---|
| git-workflow-and-versioning | O | Commits atômicos, branches, versionamento, changelog | ✅ commits (versionamento/changelog ❌) |
| principle-sequence-verifiable-units | P | Unidades pequenas, cada uma verificada | ✅ |
| make-pr-easy-to-review | P | Limpar histórico, descrição de PR | ➕ |
| pr | M | Escrever corpo de PR | ❌ idem |
| babysit | P | Levar PR até mergeable (CI, comentários) | ❌ |
| fix-ci | P | Corrigir checks falhando | ➕ |
| get-pr-comments | P | Resumir comentários de review | ❌ |
| fix-merge-conflicts / resolving-merge-conflicts | P / M | Resolver conflitos | ➕ |
| shipping-and-launch | O | Checklist pré-produção | ⛔ (deploy é seu) |
| ci-cd-and-automation | O | Montar pipeline CI/CD | ➕ |
| git-guardrails-claude-code | M | Hook que bloqueia git perigoso (push, reset --hard) | ❌ |
| setup-pre-commit | M | Husky + lint-staged | ⛔ (é JS) |
| observability-and-instrumentation | O | Logs, métricas, alertas | ➕ |

## 9. Entender código e contexto

| Skill | Fonte | O que faz | Queiroz |
|---|---|---|---|
| how | P | Como X funciona, onde colocar código | ➕ |
| why | P | Por que X é assim (git, issues, chat, docs) | ➕ |
| teach | P / M | Explicar um trabalho de forma que você entenda | ➕ |
| recall | P | Reconstruir contexto recente a partir do histórico | ➕ |
| handoff / claude-handoff | M | Passar a conversa para outro agente | 🟡 `.queiroz/` serve de handoff |
| show-me-your-work | P | Log de decisões (TSV) para trabalho longo | 🟡 `queiroz:design` registra a síntese |

## 10. Princípios do pstack que ainda não estão no núcleo

| Princípio | O que diz | Queiroz |
|---|---|---|
| boundary-discipline | Guardas nas bordas, lógica pura no meio | ✅ |
| foundational-thinking | Estruturas de dados certas primeiro | ✅ |
| laziness-protocol | Menor diff | ✅ |
| subtract-before-you-add | Apagar antes de somar | ✅ |
| never-block-on-the-human | Reversível: faz e mostra | ✅ |
| model-the-domain | Domínio numa estrutura, não em ifs espalhados | 🟡 "formato dos dados" |
| make-operations-idempotent | Webhooks e jobs convergem se rodarem duas vezes | ❌ (estava no 1º rascunho, saiu) |
| separate-before-serializing-shared-state | Eliminar estado compartilhado antes de travar | ❌ (importa com paralelo) |
| type-system-discipline | Estados ilegais irrepresentáveis | ❌ |
| redesign-from-first-principles | Requisito novo = redesenhar como se fosse do dia 1 | ❌ |
| build-the-lever | Fazer o script que faz/prova, não fazer à mão | ❌ |
| encode-lessons-in-structure | Correção repetida vira lint/teste, não texto | ❌ |
| experience-first | Encanto do usuário > conveniência de implementação | ❌ |

## 11. Escrita e comunicação

| Skill | Fonte | O que faz | Queiroz |
|---|---|---|---|
| unslop | P | Cortar vícios de texto de IA | ➕ |
| technical-writing | P | Padrão para docs, READMEs, PRs | ➕ |
| writing-for-agents | M | Como escrever skills e CLAUDE.md | ❌ (útil para construir o próprio Queiroz) |
| bro / wait-what | P / M | Repetir a última mensagem em linguagem simples | ➕ |
| writing-beats / fragments / shape | M | Escrever artigos | ⛔ |
| what-did-i-get-done | P | Resumo dos seus commits num período | ❌ |

## 12. A stack se melhorando

| Skill | Fonte | O que faz | Queiroz |
|---|---|---|---|
| reflect | P | 3 subagentes revisam a sessão e propõem edições nas skills | ➕ |
| retro | M | Retrospectiva da sessão | ❌ |
| automate-me | P | Transformar seu jeito de trabalhar numa skill `-mode` | ⛔ (é o que estamos fazendo à mão) |
| setup-pstack | P | Configurar modelos por papel | ✅ `queiroz-models.md` |
| setup-matt-pocock-skills | M | Tracker, labels, docs por projeto | ✅ `queiroz:setup` (só verify) |

## 13. Nicho

| Skill | Fonte | Queiroz |
|---|---|---|
| migrate-to-shoehorn, scaffold-exercises | M | ⛔ |

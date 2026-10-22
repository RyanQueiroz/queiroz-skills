# Queiroz: design

Construído devagar, uma decisão por vez. Só entra aqui o que foi decidido.

## Decidido

1. **Um modo só: `queiroz:mode`.** Não existe `queiroz:run` separado.
2. **Planejar é com a pessoa, na mão.** Grill e spec são skills que a pessoa chama quando quer. Nada dispara sozinho.
3. **O `queiroz:mode` é o executor.** A pessoa entrega a spec e diz "implemente". Ele implementa e só para quando provar que funciona.
4. **A verificação é o coração**, herdada do pstack: o trabalho só está pronto quando um roteiro dirigiu o app de verdade e guardou a evidência.

5. **`/queiroz:setup` prepara cada projeto**, como o `setup-pstack` e o `setup-matt-pocock-skills`. Ele explora o repo, mostra o que achou, confirma com a pessoa e escreve. Seu entregável principal é a skill `verify` do projeto.
6. **A `verify` do projeto tem 5 partes**, como no pstack e nos agentes de nuvem do Claude:
   - **Launch:** subir o app e saber quando está pronto.
   - **Doctor:** checar se a instância está saudável antes de dirigir.
   - **Drive:** usar o app como usuário (navegador, API, terminal).
   - **Evidence:** guardar a prova da ação e do estado resultante.
   - **Cleanup:** derrubar só o que subiu, sem apagar a evidência.

   Ela tem também um mapa de features (um arquivo por feature). O setup só termina depois de rodar a `verify` uma vez de ponta a ponta.
7. **O `queiroz:mode` exige a `verify`.** Se o projeto não tem a skill, ele roda o setup antes de implementar. No fim, prova a feature com a `verify` e acrescenta a feature ao mapa.

8. **O `/queiroz:setup` configura só a `verify`.** O resto vem quando precisar. Dentro do `queiroz:mode`, se a `verify` faltar, ele anuncia em uma linha que vai rodar o setup e pede o OK da pessoa. Fora dele, a pessoa chama `/queiroz:setup` na mão.
9. **Existe um modo multi-modelo (o "tanque")** para plano, arquitetura e implementação: vários modelos fazem a mesma coisa, e um orquestrador pega o melhor resultado e faz a implementação real. Ele é caro, então fica para quando é muito crítico ou quando a pessoa não sabe o que fazer.
    - **Quem liga:** o `queiroz:mode` sugere e a pessoa aprova. Ao ler a spec, se vê sinal de risco (dinheiro, auth, migração de dados, arquitetura sem precedente no código ou spec com decisões em aberto), ele diz em uma linha por que é crítico e quanto custa a mais, e espera. Sem OK, nunca liga. A pessoa também pode pedir direto.
    - **Síntese, não escolha.** Cada modelo do painel (Fable, Opus, Sonnet, Haiku) produz sua versão. O orquestrador lê todas, lista o que cada uma tem de melhor, inclusive o que só um modelo viu, e escreve uma versão nova que junta isso numa solução coerente. Não é "a melhor das três", é "o melhor de cada uma".
    - **Só na arquitetura.** Os modelos desenham tipos, assinaturas, módulos e fluxos. O orquestrador sintetiza um desenho. **Um** agente implementa contra o desenho sintetizado. Se a implementação brigar com o desenho, refaz-se a síntese, não o código.
    - **O `queiroz:design` entrega desenho + plano.** A entrada é a spec. A saída é o desenho sintetizado **e** o plano de implementação dele: os tickets já prontos para o `queiroz:mode` executar. Com o design ligado, o `queiroz:mode` não quebra a spec sozinho; usa o plano do design.
    - **Seguro e verificável.** Na síntese, cada decisão diz de qual modelo veio e por que venceu. Ideias rejeitadas ficam registradas com o motivo. O desenho é checado contra a spec (nada da spec fica sem lugar no desenho) e contra riscos de segurança nas bordas: input externo, auth, dinheiro, dados. Cada ticket do plano diz como a `verify` prova que ele funciona, e um ticket sem prova não entra no plano.
10. **Os modelos dos subagentes são configuráveis por papel**, como no `pstack-models.md`. A configuração fica num arquivo global, `~/.claude/queiroz-models.md`, com uma linha por papel. Um papel sem linha usa o default:

    | Papel | Faz | Default |
    |---|---|---|
    | `implementer` | Escreve o código de cada ticket | `opus` |
    | `explorer` | Lê o código e acha fatos (também no `grill`) | `haiku` |
    | `architecture panel` | Desenhos paralelos no `queiroz:design` | `fable, opus, sonnet, haiku` |
    | `interrogate panel` | Ataques paralelos no `interrogate` | `fable, opus, sonnet, haiku` |
    | `synthesizer` | Junta o melhor dos desenhos | `fable` |
    | `verifier` | Roda a `verify` e julga a evidência | `sonnet` |
    | `reviewer` | Revisão cega do diff contra a spec | `sonnet` |
    | `blast` | Análise de blast radius com prova | `sonnet` |
    | `investigator` | Investigações do `why` (git, PRs, issues, docs) | `sonnet` |
    | `researcher` | Pesquisa em fonte primária do `research` | `sonnet` |

    O orquestrador é a própria sessão.
11. **Sempre um orquestrador e paralelismo em tudo que der.** A sessão é o orquestrador: planeja, despacha, verifica e integra, e não escreve código de ticket. O `queiroz:mode` quebra a spec em tickets (fatias verticais com critérios de aceite e bloqueios) em `.queiroz/<feature>/tickets/`. Todo ticket **sem bloqueio pendente** roda em paralelo, cada um num `implementer` com contexto limpo e **worktree própria**. O orquestrador verifica cada ticket que volta, integra no branch e despacha a nova fronteira. Exploração, blast radius e revisão também rodam em paralelo quando são independentes. *(Substitui a decisão anterior de rodar os tickets em sequência.)*
12. **Duas camadas.** Um **núcleo leve** fica sempre ligado pelo hook: princípios, "prove que funciona" e resposta em PT-BR, com umas 300 palavras. A **execução completa** (tickets, subagentes, verify) só entra quando a pessoa chama o `queiroz:mode`. Ao entregar, volta ao núcleo leve.

13. **Entrega: branch com commits limpos, `verify` passou, relatório.** O `queiroz:mode` **nunca** faz merge. Ele também não abre PR nem faz push sozinho: só quando a pessoa pede. No relatório, ele diz que o branch está pronto para PR.
14. **Sistema de commits** (osmani + pstack):
    - Abre um branch próprio antes do primeiro commit e nunca commita direto na `main`.
    - **Um commit por ticket**, feito só depois que a `verify` daquele ticket passa: commit = ponto seguro verificado.
    - Commits atômicos: refactor separado de feature, formatação separada de comportamento.
    - A mensagem segue Conventional Commits (`feat:`, `fix:`, `refactor:`...), explica o *porquê* e cita o ticket.
    - **Higiene antes de cada commit:** ler o diff staged, procurar segredos (`.env`, chaves) e rodar os testes do ticket.
    - Se um ticket quebra o que já passou, volta ao último commit e investiga, sem empilhar correção em cima.

15. **Revisão cega antes de entregar.** Um subagente `reviewer` com contexto limpo recebe **só a spec e o diff**. Ele não vê relatórios dos implementers, log de decisões, conversa nem o desenho. Assim não herda o viés de quem escreveu. Ele julga o diff contra a spec e os princípios. Cada achado vira um ticket de correção, com o ciclo normal (implementer → verify → commit). É um reviewer por entrega.

16. **Bugs por tamanho.** Um bug simples fica no núcleo leve: o Claude corrige seguindo os princípios, sem subagentes. Se a pessoa chamar o `queiroz:mode` para o bug, ele segue o caminho completo:
    1. Reproduzir com a `verify`, vendo o erro acontecer de verdade.
    2. Achar a causa raiz, olhando todos os chamadores da função.
    3. Escrever um teste que falha.
    4. Corrigir e ver o teste passar.
    5. Rodar a `verify` e commitar.
    6. Passar pela revisão cega.

17. **Blast radius em duas camadas**, inspirado no `blast-radius` do pstack:
    - **No núcleo (leve):** antes de mexer em algo compartilhado, achar o que depende disso além do grep: contratos JSON, colunas do banco, webhooks, flags, consumidores indiretos.
    - **No `queiroz:mode` (completo):** roda **antes dos tickets**, sobre o que a spec vai tocar (o que a spec afirma sobre o código existente é hipótese até ser provado), e **no fim**, sobre o diff inteiro, junto com a revisão cega.
    - A análise completa acha **o fato do qual a segurança depende** e o prova rodando código. Cada afirmação diz até onde chegou: suposição → linha citada → falha descartada → script rodado → reproduzido no app. Um fato não provado aparece como "não provado".
18. **Conteúdo do núcleo (~300 palavras):**
    - **Pensar:** ler antes de mexer; formato dos dados antes da lógica; menor diff; sem código especulativo; validar nas bordas.
    - **Verificar:** causa raiz + blast radius leve; duas correções falharam → testar a suposição; provar no artefato real.
    - **Agir:** reversível faz, irreversível para; "não" é resposta válida; apontar quando a tarefa merece o `queiroz:mode`.
    - **Responder:** PT-BR, começar pelo resultado, rotular o que foi medido, lido ou suposto.

19. **`grill` = o `grilling` do mattpocock.** Perguntas em rodadas. Cada rodada traz toda a fronteira de decisões, numerada, com uma resposta recomendada. Termina quando não sobra decisão aberta. Fatos do código são buscados pelo `explorer` (`haiku`) e nunca perguntados à pessoa.
20. **`spec` = o `to-spec` do mattpocock, com duas mudanças.** Sintetiza a conversa sem novas perguntas e grava em `.queiroz/<feature>/spec.md`.
    - As user stories ficam curtas, só as que mudam o comportamento.
    - A seção **"Como provamos"** é obrigatória: os cenários que a `verify` vai rodar (ação → resultado visível → efeito no banco ou em arquivo). Sem ela, a spec não está pronta. O critério de pronto é escrito antes do código, pela pessoa.

21. **Entram também:** `interrogate` (revisão adversarial multi-modelo), `idea-refine` (ideia vaga → variantes → conceito afiado) e uma skill de debug (osmani `debugging-and-error-recovery` + mattpocock `diagnosing-bugs`). Ainda falta decidir onde cada uma entra no fluxo.

22. **Entram, com o papel de cada uma:**

    | Skill | Inspirada em | Quando entra |
    |---|---|---|
    | `brief` | osmani `context-engineering` | O orquestrador usa **antes de cada subagente**: monta o brief com ponteiros (spec, ticket, arquivos certos), restrições e o check de pronto. Subagente sem brief bom não sai. |
    | `idea-refine` | osmani | A pessoa chama, antes do `grill`: ideia vaga → variantes → conceito afiado. |
    | `prototype` | mattpocock | Esboço descartável para testar se funciona. A pessoa chama. |
    | `interrogate` | pstack `interrogate` + osmani `doubt-driven-development` | Revisão adversarial multi-modelo para o que é crítico: vários modelos atacam o desenho ou o diff. Mesma regra do multi-modelo: sugere e espera OK. |
    | `research` | mattpocock `research` + osmani `source-driven-development` | Pesquisa em fonte primária (docs oficiais de Stripe, EVO, WhatsApp...) → arquivo Markdown. A pessoa chama. |
    | `frontend` | osmani `frontend-ui-engineering` | O `implementer` segue quando o ticket mexe em UI. |
    | `measure` | pstack `benchmark-checklist` + `explain-the-number` | **Medir antes de decidir:** custo, velocidade, % de acerto. Baseline × mudança, o que limita o número, se mediu a coisa certa e se é repetível. Responde "vale a pena pôr isso no motor?". |
    | `perf` + agente `web-perf-auditor` | osmani `performance-optimization` + agente | Otimizar com número antes e depois (usa o `measure`). O agente audita Core Web Vitals. |
    | `deslop` + `no-comments` | pstack | Antes de cada commit: tirar slop de IA e comentários desnecessários. |
    | `ci` | osmani `ci-cd-and-automation` + pstack `fix-ci` | Criar **e manter** o pipeline, e corrigir check falhando. |
    | `merge` | pstack `fix-merge-conflicts` + mattpocock `resolving-merge-conflicts` | O orquestrador usa ao integrar worktrees paralelas. |
    | `pr` | pstack `make-pr-easy-to-review` + `technical-writing` | Quando a pessoa pede PR: no formato do pstack. |
    | `observability` | osmani | Logs, métricas e alertas para ver o comportamento em produção. |
    | `how`, `why`, `bro`, `teach` | pstack | Comandos avulsos para entender código, decisões e explicações. |
    | `recall` | pstack | Reconstruir o contexto, sobretudo **depois de um `/compact`**. |
    | `reflect` | pstack | Revisa a sessão e propõe edições nas skills, principalmente nas do Queiroz e na `verify` do projeto. |
    | `unslop` | pstack | Todo texto: respostas, PR, docs, commits. |

23. **Tudo da decisão 22 entra na v1.** Junto, por consequência (a pessoa pode vetar):
    - **Estado compartilhado:** regra do orquestrador. Dois tickets paralelos nunca escrevem no mesmo arquivo; se escreveriam, viram um ticket só ou um bloqueia o outro.
    - **Idempotência:** uma linha no núcleo (webhook, job e retry convergem para o mesmo estado se rodarem duas vezes).
    - **Segurança:** um eixo no reviewer cego (input externo, auth, dinheiro, dados pessoais), sem skill separada.

24. **O `queiroz:mode` não é roteador.** Ele só liga quando a pessoa o chama para implementar (uma spec, ou um bug). Ele não classifica prompts nem escolhe skills avulsas. Fora dele ficam o núcleo leve e as skills que a pessoa chama na mão. `research`, `measure` e `prototype` ficam avulsas.

## Peças da v1

O `queiroz:mode` **não** usa tudo. Como no poteto-mode, a maioria das skills é avulsa: existe no pacote, e a pessoa chama quando quer.

**Sempre carregado:** o núcleo (texto do hook, ~300 palavras).

**O `queiroz:mode` usa sozinho no fluxo:**

| Skill | Quando |
|---|---|
| `queiroz:setup` | Falta a `verify` (anuncia e pede OK) |
| `brief` | Antes de cada subagente |
| `queiroz:blast` | Antes dos tickets e no fim |
| `merge` | Ao integrar worktrees paralelas |
| `debug` | Quando é chamado para um bug |
| `frontend` | O ticket mexe em UI |
| `deslop`, `no-comments` | Antes de cada commit |
| `unslop` | Relatório final |
| `queiroz:design`, `interrogate` | Só sugere; roda com OK |

**Avulsas (a pessoa chama):** `idea-refine`, `grill`, `spec`, `prototype`, `research`, `measure`, `perf` + agente `web-perf-auditor`, `ci`, `pr`, `observability`, `how`, `why`, `bro`, `teach`, `recall`, `reflect`. Também `queiroz:blast`, `debug`, `queiroz:design` e `interrogate` podem ser chamadas sozinhas.

**Config:** `~/.claude/queiroz-models.md`.

São 28 skills, 1 agente e 1 arquivo de config.

## Fluxo completo

```
núcleo leve (sempre ligado pelo hook)

pessoa: /grill   (opcional) ──→ conversa em rodadas
pessoa: /spec    (opcional) ──→ .queiroz/<feature>/spec.md  (com "Como provamos")
pessoa: "queiroz:mode, implemente esta spec"
   │
   ├─ falta verify? → anuncia → OK → queiroz:setup → verify rodada uma vez
   ├─ queiroz:blast sobre o que a spec toca (fatos provados)
   ├─ spec crítica? → sugere multi-modelo → OK → queiroz:design
   │     └─ fable + opus + sonnet + haiku desenham → síntese → desenho + plano de tickets
   ├─ sem design: queiroz:mode quebra a spec em tickets
   ├─ branch próprio
   ├─ fronteira de tickets em paralelo (worktree cada):
   │     implementer novo → verify do ticket → orquestrador integra → commit → próxima fronteira
   ├─ fim: queiroz:blast no diff + reviewer cego (só spec + diff)
   │     └─ achados viram tickets de correção (mesmo ciclo)
   ├─ verify da spec inteira (cenários do "Como provamos") + mapa de features atualizado
   └─ relatório: branch pronto para PR. Nunca merge. PR e push só se pedir.
   │
volta ao núcleo leve
```

## Construção

| Onda | Peças | Estado |
|---|---|---|
| 1. Fundação | núcleo (`hooks/session-start.md`), `models.md`, `queiroz:setup` | Escrita (v0.2.0), falta testar num projeto real |
| 2. Planejar | `idea-refine`, `grill`, `spec`, `research`, `prototype` | Escrita (v0.2.0), falta testar num projeto real |
| 3. Executar | `brief`, `queiroz:mode`, `queiroz:blast`, `merge`, `debug` | Escrita (v0.2.0), falta testar num projeto real |
| 4. Qualidade | `deslop`, `no-comments`, `unslop`, `frontend`, `pr`, `ci`, `observability` | Escrita (v0.2.0), falta testar num projeto real |
| 5. Tanque e medir | `queiroz:design`, `interrogate`, `measure`, `perf` + agente | Escrita (v0.2.0), falta testar num projeto real |
| 6. Entender e manter | `how`, `why`, `bro`, `teach`, `recall`, `reflect` | Escrita (v0.2.0), falta testar num projeto real |

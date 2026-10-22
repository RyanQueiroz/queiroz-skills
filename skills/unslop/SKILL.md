---
name: unslop
description: Cut AI tells from prose, in Portuguese or English. Use on every reply, final report, PR description, commit message, doc, and spec before it reaches a reader.
---

# Unslop

Edit prose so it reads like a person who knows the subject wrote it. Keep the meaning and the intended tone. Code, identifiers, and quoted output stay as they are.

## Process

1. Scan the text against every pattern below, in the text's own language.
2. Rewrite each hit. When a sentence says nothing concrete, delete it instead of polishing it.
3. Read the result once more for rhythm: mixed sentence lengths, one idea per sentence, nothing the reader must decode.

**Done when** a second scan finds no pattern below.

## Content

- **Say what it does.** Name the mechanism, the file, or the number, not the feeling. "Muito mais rápido" becomes "de 2,1 s para 300 ms". If a sentence could appear unchanged in another project's text, cut it.
- **Vague attribution.** "Especialistas apontam", "experts believe". Name the source or delete.
- **Trailing -ing / gerúndio clauses** that add fake significance: "highlighting...", "ensuring...", "garantindo...", "destacando...", "visando...". Delete, or make it its own sentence with a real fact.
- **Generic conclusions.** "The future looks bright", "Em suma, ...", "Com isso, ...". End on the last real fact or the next step.

## Words

- **AI vocabulary.** EN: additionally, crucial, delve, enhance, foster, intricate, landscape, pivotal, robust, seamless, showcase, testament, underscore, vibrant, leverage, utilize. PT: além disso (as an opener), crucial, fundamental, robusto, aprofundar, mergulhar, alavancar, potencializar, otimizar (when nothing was measured), cenário, jornada, ecossistema, sinergia, de forma eficiente. Use the plain word.
- **Fancy "is".** "serves as", "stands as", "boasts", "atua como", "se configura como", "conta com". Write "is", "has", "é", "tem".
- **Abstract metaphor nouns.** Substrate, vector, primitive, surface, scaffolding, north star, flywheel, "pilar", "alicerce", "motor de crescimento". Pick the concrete word.
- **Plain word first.** "Utilize" is "use", "facilitate" is "help", "realizar" is "fazer", "efetuar" is "fazer", "visando" is "para", "no intuito de" is "para".
- **Anglicisms with a Portuguese word.** "Performar", "endereçar um problema", "deployar" when "publicar" fits, "fazer sentido" as filler. Technical terms with no common Portuguese form (deploy, branch, commit, PR, webhook) stay in English.
- **One name per thing.** Pick one term and repeat it. Synonym cycling teaches the reader there are several things.
- **Adverbs.** "Significativamente", "extremamente", "significantly". Replace with a stronger verb or the number.

## Structure

- **"Not just X, but Y" / "Não apenas X, mas também Y".** State Y.
- **Rule of three.** Lists forced into three items. Use the real count.
- **False ranges.** "From X to Y", "de X a Y" where X and Y are not on one scale. List the items.
- **Hedging stacks.** "Could potentially", "pode eventualmente vir a". One hedge at most, only when the doubt is real.
- **Filler.** "In order to", "it is important to note that", "vale ressaltar que", "é importante destacar que", "cabe mencionar", "segue abaixo", "basicamente". Delete.
- **Passive voice.** "Foi feito", "é realizado", "queries are validated". Name the actor: "o parser valida", "the compiler checks". Passive is fine only when the actor is unknown or irrelevant.
- **Mannered prose.** Aphorisms, personified code, figurative verbs ("o plano segura isso", "rides along"). Say it literally.
- **Over-compression.** Dropped articles, arrows, verbless fragments: "parser rejeita data → exit 2". Write the full sentence: "O parser rejeita a data, sai com código 2 e não grava nada."
- **Dense sentences.** If the reader has to backtrack, split it.

## Punctuation and format

- **No em dashes or en dashes as separators.** End the sentence or use a comma.
- **Colons** only before a list or an example, never as a mid-sentence connector.
- **Bold** only for a term the reader must not miss. Never a bold label that the line then restates ("**Desempenho:** o desempenho melhorou").
- **Headings** in sentence case, in both languages. "Como provamos", not "Como Provamos".
- **No decorative emojis.** Straight quotes, not curly ones.
- **Portuguese accents** always correct: "não", "você", "também", "função".

## Chatbot register

Delete openers and closers that talk about the conversation instead of the subject: "Great question!", "Certainly!", "Ótima pergunta!", "Com certeza!", "Claro!", "Vamos lá!", "Espero ter ajudado", "Fico à disposição", "Qualquer dúvida, é só chamar", "Let me know if...". Answer directly, result first. No praise of the user and no apology for nothing.

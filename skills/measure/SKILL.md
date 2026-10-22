---
name: measure
description: Measure cost, speed and accuracy of a change against its baseline, and answer "vale a pena pôr isso no motor?" with numbers.
disable-model-invocation: true
---

# Measure

Decide whether a change earns its place in the engine (the LLM WhatsApp agent, or any system) by measuring the **baseline** and the **change** on the same work, the same way. The answer is one of **vale**, **não vale**, or **inconclusivo**, with the numbers behind it.

A run that went wrong still prints a plausible number: requests that failed, a cache that skipped the work, a prompt that never loaded, a side left on other settings, noise. Every step below exists to rule one of those out.

Save everything in `.queiroz/measure/<YYYY-MM-DD>-<slug>/`: the claim, the case set, the raw `runs.csv`, and the report.

## 1. Write the claim and the bar

Write the sentence you expect to ship, with numbers: "o prompt novo acerta 8 pontos a mais no agendamento, custa até 10% a mais e não passa de 3 s no p95". Then the decision bar: how much better accuracy has to be, how much more cost and latency the user accepts.

Ask the user only what you can't infer (the bar, which flows matter), each question with a recommended default.

**Done when** `claim.md` holds the sentence and the bar.

## 2. Build the case set

- **Real cases.** Take them from real conversations (or real requests), covering the flows the change touches and the ones it must not break. Each case has its input and its expected outcome written before any run.
- **Grader.** How "acerto" is decided, per case: an exact rule (right slot booked, right field extracted, right tool called) beats an LLM judge. If you use a judge, it never sees which side produced the answer, and you grade 20 cases by hand to measure the judge itself. A judge that agrees with you 85% of the time can't resolve a 5-point gain.
- **Sample size.** On `n` cases, accuracy is uncertain by roughly ±1/√n (100 cases ≈ ±10 pts, 400 ≈ ±5). The paired comparison in step 5 resolves smaller gaps, because it only counts cases where the sides disagree. Size the set so the bar from step 1 is bigger than the noise; if it can't be, say so now.
- **Repetitions.** LLM output varies run to run. Run each case at least 3 times per side (5 for a close call).

**Done when** the cases, their expected outcomes, and the grader are written, and `n` × repetitions is chosen.

## 3. Make the sides comparable

Both sides run the way production runs: same model and version, temperature, max tokens, tools, retrieval data, and prompt caching state (caching changes both cost and latency, so warm both or neither). If one side uses defaults the other doesn't, you compared configurations, not the change.

Log, per run, what proves which side ran: the prompt version or config hash, the model id from the response.

**Done when** a diff of the two configurations shows only the change.

## 4. Run

- **Interleave** A, B, A, B, so warm-up, rate limits, and provider drift hit both sides.
- **Record every trial** in `runs.csv`: `case,side,run,correct,latency_ms,cost,error` (`side` is A for baseline, B for change; in pure speed work, `correct` says the output was right). Cost from the token counts the API returns, at the real price. Latency end to end, as the user on WhatsApp waits for it, not just the model call.
- **Count errors** apart from wrong answers: API errors, timeouts, empty replies, failed tool calls. Errors are fast or slow in their own ways and distort both latency and cost.
- **Did it happen?** Spot-check a few trials: the change was active (the logged hash), the tool really ran, the reply was really produced and graded, tokens are in the expected range. A trial that skipped the work is not a fast trial.

**Done when** every case has its repetitions on both sides and the spot-checks pass.

## 5. Explain the number

Run `python3 -I <this skill's directory>/scripts/compare.py <run-dir>/runs.csv`. It prints accuracy with its 95% interval and per-run range, errors, latency p50/p95, mean cost per trial, and the paired result: in how many cases B beat A, A beat B, and the exact p-value.

Then, before trusting it:

- **What limits it?** For latency: model time, tool calls in sequence, retrieval, the WhatsApp round trip, a queue. For cost: input tokens (prompt, history, retrieved context) versus output. Name it from the logs, not from reading code. If the change didn't move the number, the limiter says why.
- **Did it break limits?** A latency drop bigger than the time the changed piece took, or a cost drop bigger than its tokens, means something else changed.
- **Does it matter end to end?** Report per conversation, not per call. A 30% faster step that is 5% of the turn makes the turn at most 5% faster.
- **Is it real?** A gap inside the run-to-run range is no difference. A paired p above 0.05 is not a win, however good the means look.

**Done when** every number in the report has its run count, its spread, and its limiter.

## 6. Verdict

Report to the user in Portuguese, starting with the verdict:

```
Veredito: vale | não vale | inconclusivo

Acerto: 71% → 79% (n=200 casos × 3, IC95 ±6 pts; B melhor em 24 casos, A em 8, p=0.007)
Custo:  R$0,012 → R$0,014 por conversa (+17%)
Tempo:  p50 2,1 s → 2,3 s; p95 3,9 s → 4,4 s
Erros:  2/600 → 1/600
Limita: tempo dominado pelas 2 chamadas de ferramenta em série (61% do turno)
Mediu a coisa certa? hash do prompt conferido em todas as rodadas; juiz revisado em 20 casos (19 de acordo)
```

- **Vale:** the gain clears the bar and the noise, and cost and latency stay inside the bar.
- **Não vale:** no difference beyond noise, or the gain costs more than the bar allows. A neutral change is a "não vale": it adds complexity and buys nothing.
- **Inconclusivo:** a side ran untuned, the limiter is unknown, the grader is unmeasured, or "did it happen" failed. Name the gap and what would close it.

For a quick ballpark the user asked for, one small run is fine: still check errors and "did it happen", and label it as a ballpark. A choice between options is never a ballpark.

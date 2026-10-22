# Lead judgment

You have what the reviewers lack: the conversation, the spec, the design, what was tried and rejected, what the next ticket will address. Filter with it. Don't aggregate.

## Classes

Classify in this order; the first class that fits wins.

1. **Contract misread.** The reviewer flagged it because the contract was unclear or incomplete. Fix the contract; reclassify next round.
2. **Agir.** A real problem for correctness, security, or maintainability given the actual goal. Would block a real merge.
3. **Considerar.** Legitimate, but unclear it beats the cost of fixing now. State the tradeoff.
4. **Anotado.** Valid and not actionable: context-dependent, premature, low impact at this stage.
5. **Descartado.** Wrong, nitpicky, or missing context. One line on why.

## Filters

- **Hypothetical vs actual.** A finding about bad input counts only if a real caller can send it. Trace the call site; if the boundary or the type system rules it out, dismiss it.
- **Nitpick gravity.** Adversarial reviewers fill space. A review of only nits means the code is probably fine; say so.
- **"I'd have done it differently."** Not a finding unless it shows a concrete problem with the current approach.
- **Premature abstraction.** Suggestions to extract, wrap, or generalize code that changes in only one way: dismiss.
- **Missing context.** Flags on code the change didn't touch, or patterns consistent with the rest of the repo the reviewer can't see: dismiss gently, and ask whether the contract should have carried that context.

## When the reviewer is right

Signs a finding deserves Agir: several models raised it independently; it names a concrete execution path; it exposes a gap in your own model of the code; you read it and think "...yeah, actually". Dismissing a security or correctness finding needs a traced reason, never a feeling.

The Descartado list is a trust mechanism: it lets the user overrule you.

---
name: interrogate
description: Adversarial multi-model review of a design or diff for critical work. A panel of models attacks it from independent angles; every finding is verified before it is reported. Use for /interrogate, "stress test this", "find blind spots", or when `queiroz:mode` suggested it and the user said yes.
---

# Interrogate

Several models attack the same artifact, each in fresh context, each biased to **disprove**. Model diversity supplies the independent angles: one model shares its blind spots with the author, a panel rarely does. You are the lead reviewer: you verify every finding against the artifact and deliver a verdict. You change nothing.

Models come from `../../models.md` (role `interrogate panel`).

## 0. Gate

The panel costs about four reviews. Run only after an explicit OK from the user in this conversation. Without one, say in Portuguese, in one line, why the artifact looks critical and the cost, and wait.

**Done when** the user said yes.

## 1. Extract the artifact and the contract

A reviewer needs the **artifact** and the **contract**, never the journey.

- **Artifact.** A diff (`git diff <base>...HEAD`, or the files named) or a design (`.queiroz/<feature>/design.md`). Too big to hold in one read (roughly 500+ changed lines, or several unrelated features): split it and interrogate each part.
- **Contract.** What the artifact must satisfy: the spec's requirements and "Como provamos" scenarios, the design's boundaries, the invariants it claims. Write it as one paragraph of intent plus a bullet list of must-holds.

Strip your reasoning, the implementer's reports, and any claim that it works. A reviewer handed your conclusion validates your conclusion.

**Done when** the artifact and contract are written to `.queiroz/<feature>/interrogate/<run>/input.md` (`.queiroz/interrogate/<run>/` with no feature) with nothing but the two.

## 2. Spawn the panel

Resolve `interrogate panel`. Send one `Agent` call per model, **all in one message**, `run_in_background: true`, `subagent_type: general-purpose`, `model` set to that entry. Each gets [references/reviewer-prompt.md](references/reviewer-prompt.md) filled with the input path and the matching mode (diff or design). Reviewers read code to trace paths and edit nothing.

A reviewer that fails is a dropout: record it and continue.

**Done when** every panel model returned findings, "no findings", or is recorded as a dropout.

## 3. Merge

- **Deduplicate.** Different models describe one issue differently; merge them and list every model that raised it.
- **Consensus.** A finding raised independently by two or more models is high signal.
- **Lone findings.** Still read; one model seeing it is often why you ran a panel. Security and correctness findings from a single model get full scrutiny.
- **Disagreements.** One model flags what another explicitly calls fine: keep both and settle it in step 4.

**Done when** every raw finding maps to exactly one merged finding.

## 4. Verify each finding

A finding is a hypothesis about the code. Before it reaches the user, trace it yourself and record how far the proof got:

`suposição` → `linha citada` → `falha descartada` → `script rodado` → `reproduzido no app`

- Trace the call path the finding depends on. "Could be null" is a finding only if a caller can pass null.
- For `critical` findings, push to a run: a failing test, a script, or the project's `verify` reproducing it.
- A finding you could not prove stays labeled at the level it reached. It is never upgraded by confidence.

Classify per [references/lead-judgment.md](references/lead-judgment.md): **Agir**, **Considerar**, **Anotado**, **Descartado**. A finding you misread because the contract was unclear: fix the contract and note it.

**Done when** every merged finding has a proof level and a class with a one-line reason.

## 5. Report

Report to the user in Portuguese:

```markdown
### Intenção
> the contract paragraph

### Painel
- <model>: N achados (or "dropout")

### Agir
Each: what breaks, file:line, models that raised it, proof level, why it matters.

### Considerar
Each: the finding, models, the tradeoff.

### Anotado
Short list.

### Descartado
Each with the reason. This is how the user overrides you.

### Mapa de acordo
Where models converged, where they split, and what the pattern says.
```

Keep **Agir** to what would block a real merge; more than five items means the filter is too loose.

**Done when** the report is delivered. Apply nothing.

## 6. After the verdict

- **Design under `queiroz:design`:** Agir findings go back to the synthesis as new constraints.
- **Diff under `queiroz:mode`:** each Agir finding becomes a correction ticket with the normal cycle.
- **Standalone:** the user decides.

A second round runs only on what changed, with a fresh panel. Stop after three rounds and hand the remaining findings to the user: three unresolved rounds say the artifact isn't ready. Two rounds with substantive findings and none classified Agir means you are validating, not doubting: stop and tell the user.

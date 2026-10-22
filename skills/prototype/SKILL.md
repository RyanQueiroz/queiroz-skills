---
name: prototype
description: Build a throwaway sketch to answer one design question; the result decides and the code is discarded.
disable-model-invocation: true
---

# Prototype

A prototype is **throwaway code that answers one question**. You own the decision, not the code. Speed beats polish: no tests, no abstractions, no error handling beyond what makes it run. The rigor goes into picking the right answer cheaply, including variants the user didn't ask for.

Say everything to the user in Portuguese.

## 1. Name the question

Write the decision the prototype exists to make, in one sentence: which layout, which state model, whether an API behaves as assumed, whether an approach is fast enough. No decision means no prototype: tell the user this is a feature, and point to `/grill` and `/spec`.

Pick the branch from the question:

- **Logic:** "does this state model / flow / data shape hold up?"
- **UI:** "what should this look like?"
- **Behavior:** "does this API, timing, or approach actually work?" (a webhook's real payload, a query's speed, a model's output)

**Done when** the question is written and the branch is chosen. If it is ambiguous and the user is away, take the branch closest to the code it serves and state the assumption at the top of the prototype.

## 2. Build it, marked as throwaway

Default home: `.queiroz/<feature>/prototype/`, outside production source. Every prototype starts with a `README.md` holding the question, the one command that runs it, and the line `PROTÓTIPO: descartável, não vai para produção`.

- **Logic:** one self-contained HTML file that opens by double-click. The logic sits in one pure `<script>` module (a reducer, a state machine, or pure functions; no DOM inside it) so it can be lifted later. The page shows the full state after every click, one button per action, and tabbed walkthroughs for the awkward cases: the happy path, a tricky edge, an attempt at something illegal. Labels in domain language.
- **UI:** 3 variants by default, 5 at most, structurally different (layout, hierarchy, primary action), not recolors. Prefer mounting them inside the real page, behind a `?variant=` param, on a branch named `prototype/<name>`, so they sit against real data and chrome; the switcher is a floating bar (arrows and `←`/`→`) gated off in production builds. Only with no host page, build a standalone page in the default home with the lightest stack that renders the idea.
- **Behavior:** the smallest script that exercises the question against the real thing (the sandbox API, a local copy of the data). It prints what you are deciding on: the payload, the timing, the output.

State lives in memory. When the question is about persistence, use a scratch database or file named `prototype-wipe-me`.

**Done when** it runs from the command in its README.

## 3. Observe

The observation is the test. For UI, drive each variant through the project's `verify` skill and screenshot it; without `verify`, use the browser tools directly. For logic, run each walkthrough. For behavior, run the script and keep its output. Save evidence in `.queiroz/<feature>/prototype/evidence/`.

**Done when** each variant or case has evidence you can show.

## 4. Decide and discard

Show the user, in Portuguese: the variants explored, the evidence, the tradeoffs, and your recommendation. The user picks.

Then:

- Write the verdict in the prototype's `README.md`: the question, the answer, why. A snippet worth keeping (a validated reducer, a schema, the real payload shape) goes there too; `/spec` can inline it as a decision.
- A prototype in `.queiroz/<feature>/prototype/` stays there as the marked record. Variants mounted in real source live only on their `prototype/<name>` branch, never merged. The real build goes through `/spec` and `queiroz:mode`, rewritten to production standards.

**Done when** the verdict is written, the user confirmed it, and no prototype code remains on a branch headed for production.

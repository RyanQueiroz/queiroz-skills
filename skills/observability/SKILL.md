---
name: observability
description: Add logs, metrics, traces, and alerts so a feature's production behavior is visible and diagnosable.
disable-model-invocation: true
---

# Observability

Instrument a feature so that when production misbehaves, someone can answer "what happened and why" from telemetry alone, without reading the source.

## 1. Write the on-call questions

Name the feature, then two to four questions the person on call will ask about it. Every signal you add answers one of them.

```
FEATURE: payment retry
1. What share of payments succeed on the first attempt vs. after a retry?
2. When a payment fails for good, why? (provider error, timeout, validation)
3. Is the provider slower than usual?
```

**Done when** the user confirms the questions, or corrects them.

## 2. Read what exists

Find the logger, the metrics client, the tracing setup, and the alerting tool the project already uses, and the log sink they feed. Instrument with those. A new dependency or vendor needs the user's OK first: name it and what it costs.

**Done when** you can name the tool for each signal, or that the project has none.

## 3. Pick the signal per question

- **Metric**: how often and how fast, in aggregate. It says *that* something is wrong.
- **Trace**: where time went across services. It says *where*. Only worth it with more than one service or an external call on the hot path.
- **Structured log**: what happened in one case. It says *why*.

**Done when** each question maps to at least one signal.

## 4. Instrument

**Logs.**

- One JSON object per event, with a stable `event` name and fields: `logger.warn({ event: "payment_failed", paymentId, provider, errorCode, attempt })`. No string interpolation.
- A correlation ID on every line: accept it at the boundary (`x-request-id`, the webhook's message ID) or generate it, and pass it on every outbound call and queue message.
- When several entry points feed one log (scheduler, webhook, manual run, replay), add an `entryPoint` field where the run starts and pass it on with the correlation ID.
- Levels: `error` when an invariant broke and someone may need to act; `warn` when degraded but handled; `info` for business events; `debug` off in production.
- Never log secrets, tokens, passwords, or personal data (CPF, phone, email, message content). Allowlist fields; never log whole request bodies. Personal data in logs is an LGPD problem.

**Metrics.**

- RED on every new endpoint and external dependency: rate, errors, duration. USE on queues and pools: utilization, saturation, errors.
- Duration as a histogram; read p50, p95, p99, never the average.
- Labels from small fixed sets only: route template, status class (`5xx`), provider. User IDs, phone numbers, raw URLs, and error text go in logs, never in labels.

**Traces.** OpenTelemetry auto-instrumentation for HTTP and database clients, initialized before other imports. Manual spans only around meaningful units (`chargeProvider`), with the attributes on-call filters by. Carry the context across queues.

**Alerts.**

- On symptoms users feel (error rate, p99 latency, queue age), not causes (CPU, one restart). Causes go on a dashboard.
- Each alert is actionable, has a threshold and a duration justified by data or an SLO, and links to a runbook.
- Two severities: page (users hurt now) and ticket (degraded, act this week).
- Runbook in `docs/runbooks/<alert>.md`, three lines minimum: what it means, the first query to run, who to escalate to.

**Done when** every question from step 1 has its signal in code.

## 5. Prove the telemetry

Instrumentation is code and can be wrong. Drive the feature with the project's `verify` skill, then read the real output:

- Force one failure and find it in the logs by its correlation ID. Fields are structured, not `[object Object]`.
- Send traffic and see the metric series appear with the expected labels and sane values.
- Follow one request across services in the tracing tool with no broken spans.
- Fire each new alert once (lower its threshold temporarily) and confirm it reaches its channel.
- Grep the captured output for secrets and personal data.

**Done when** each bullet that applies has captured output as proof, and one induced failure was diagnosed from telemetry alone.

## 6. Report

Tell the user, in Portuguese: each on-call question and the signal that answers it, the alerts with their runbooks, what was proven and how, and what stays blind (no tool for it, out of scope).

# Bottlenecks

Where to look from the symptom, and the usual causes. Each cause is a hypothesis to confirm with a measurement before fixing.

## LLM agent (WhatsApp engine)

| Symptom | Likely cause | Measure |
|---|---|---|
| Slow reply turn | Tool or model calls in sequence that could run in parallel; several model calls per turn | Per-step timings in one turn |
| Slow first token, high cost | Huge input: full history, whole knowledge base, long system prompt | Input vs output tokens per call |
| Cost jumps between runs | Prompt cache missed: the prefix changes every turn (timestamps, reordered context) | Cache read/write tokens in the API response |
| Slow and costly for easy turns | Largest model used for everything | Accuracy and cost per model on the same cases |
| Long tail (p95 ≫ p50) | Retries, rate limits, slow tool backend, long outputs | Errors and retries per trial; output tokens at p95 |
| Wrong answers after a speed fix | Context cut too far, retrieval returning fewer relevant chunks | Accuracy on the same cases |

Usual fixes: run independent calls in parallel; keep a stable prompt prefix so caching hits; trim history and retrieval to what the turn needs; route easy turns to a smaller model; cap output length; stream when the channel benefits. Each one is measured for accuracy too.

## Backend

| Symptom | Likely cause | Measure |
|---|---|---|
| One endpoint slow | N+1 queries, query ignoring its index, unbounded fetch | Query log with timings; `EXPLAIN ANALYZE` |
| Every endpoint slow at once | Connection pool exhausted, CPU or memory saturated | Time waiting for a connection; idle DB sessions |
| Memory grows | Leaked references, unbounded caches, large payloads | Heap snapshots over time |
| CPU spikes | Heavy synchronous work, regex backtracking | CPU profile |
| Intermittent slowness | Lock contention, GC pauses, a slow external dependency | Traces across the request |

- **N+1:** fetch the relation in the same query (join/include).
- **Index:** read the plan first. A `Seq Scan` where you expected an index, a `rows=` estimate off by 10× (stale stats: run `ANALYZE`), a `Sort` above the scan each need a different fix. Index for the query's shape, equality columns first. Every index taxes writes; an index that didn't change the plan is reverted.
- **Unbounded fetch:** every list paginates with a limit and a stable order.
- **Pool:** one pool per process, `instances × max` under the database's ceiling. Find what holds connections before raising `max`.
- **Cache:** only what is expensive and read far more than written. Every input that changes the response is in the key (tenant, locale, viewer). One invalidation strategy with a stated staleness window. Guard hot keys against the stampede (serve stale while one request recomputes). Never cache what must be fresh.

## Frontend

| Symptom | Likely cause | Measure |
|---|---|---|
| Slow LCP | Large or lazy-loaded hero image, render-blocking CSS/JS, slow TTFB | Network waterfall, LCP element |
| High CLS | Images or embeds without dimensions, late content, font swap | Layout shift attribution |
| Poor INP | Long tasks on the main thread, large DOM updates | Performance trace, long tasks > 50 ms |
| Slow first load | Large bundle, many requests | Bundle size, code splitting |

Targets (p75): LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1. For a full audit, dispatch `web-perf-auditor`.

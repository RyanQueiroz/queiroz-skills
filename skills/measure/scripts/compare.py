#!/usr/bin/env python3
"""Compare baseline (A) vs change (B) from a runs CSV.

CSV columns: case,side,run,correct,latency_ms,cost,error
  side: A or B. correct/error: 0 or 1. cost: any unit, same for both sides.
Usage: compare.py runs.csv      Self-check: compare.py --selftest
"""
import csv, math, statistics, sys
from collections import defaultdict


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def sign_test(wins, losses):
    """Exact two-sided binomial p for discordant cases (McNemar exact)."""
    n = wins + losses
    if n == 0:
        return 1.0
    k = min(wins, losses)
    p = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * p)


def pct(xs, q):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(q * len(xs)))] if xs else float("nan")


def summarize(rows):
    out = {}
    by_case = defaultdict(lambda: defaultdict(list))
    for side in ("A", "B"):
        rs = [r for r in rows if r["side"] == side]
        ok = [r for r in rs if not int(r["error"])]
        k = sum(int(r["correct"]) for r in ok)
        runs = defaultdict(list)
        for r in rs:
            runs[r["run"]].append(int(r["correct"]) and not int(r["error"]))
            by_case[r["case"]][side].append(int(r["correct"]) and not int(r["error"]))
        per_run = [sum(v) / len(v) for v in runs.values()]
        lat = [float(r["latency_ms"]) for r in ok]
        out[side] = {
            "trials": len(rs), "errors": len(rs) - len(ok),
            "acc": k / len(rs) if rs else 0, "ci": wilson(k, len(rs)),
            "run_range": (min(per_run), max(per_run)) if per_run else (0, 0),
            "p50": statistics.median(lat) if lat else float("nan"), "p95": pct(lat, 0.95),
            "cost": sum(float(r["cost"]) for r in rs) / max(1, len(rs)),
        }
    wins = losses = 0
    for sides in by_case.values():
        if sides["A"] and sides["B"]:
            a, b = statistics.mean(sides["A"]), statistics.mean(sides["B"])
            wins += b > a
            losses += a > b
    out["paired"] = {"B_better": wins, "A_better": losses, "p": sign_test(wins, losses)}
    return out


def report(s):
    for side, name in (("A", "baseline"), ("B", "change")):
        x = s[side]
        print(f"{side} {name}: acerto {x['acc']:.1%} (IC95 {x['ci'][0]:.1%}-{x['ci'][1]:.1%}; "
              f"por rodada {x['run_range'][0]:.1%}-{x['run_range'][1]:.1%}), "
              f"erros {x['errors']}/{x['trials']}, latência p50 {x['p50']:.0f} ms p95 {x['p95']:.0f} ms, "
              f"custo médio/tentativa {x['cost']:.4f}")
    p = s["paired"]
    print(f"pareado: B melhor em {p['B_better']} casos, A melhor em {p['A_better']}, p={p['p']:.3f}")


def selftest():
    rows = []
    for c in range(40):
        for run in range(3):
            rows.append(dict(case=c, side="A", run=run, correct=int(c < 20), latency_ms=100, cost=1, error=0))
            rows.append(dict(case=c, side="B", run=run, correct=int(c < 32), latency_ms=80, cost=2, error=0))
    s = summarize([{k: str(v) for k, v in r.items()} for r in rows])
    assert s["paired"] == {"B_better": 12, "A_better": 0, "p": sign_test(12, 0)}
    assert s["paired"]["p"] < 0.001 and abs(s["A"]["acc"] - 0.5) < 1e-9
    assert s["B"]["p50"] == 80 and s["B"]["cost"] == 2
    assert sign_test(5, 5) == 1.0
    print("selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    else:
        with open(sys.argv[1], newline="") as f:
            report(summarize(list(csv.DictReader(f))))

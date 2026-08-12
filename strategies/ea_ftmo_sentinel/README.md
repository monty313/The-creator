# FTMO Sentinel EA — validated risk shell, UNVALIDATED edge

**Status: EXPERIMENTAL — not Court law.** Quarantined per "Court before major
decisions" until a full Evidence Court case (A10 + A15).

## Measured verdict (2026-08-12 — read before anything else)

The strategies were tested on **real downloaded market data** with a
bar-accurate replica of this EA (see [`VALIDATION.md`](VALIDATION.md)):

- **The protection layer works.** Across every window, symbol and variant:
  worst day close −1.50%, worst intraday float −1.49%, **zero** FTMO daily or
  total breaches. The Day Governor does exactly what it promises.
- **The entry edge does not.** The corpus win rates replicate (70–76%) but
  every variant is **net negative after real costs** on 4.5 months of Dukascopy
  M1 and on the Yahoo May–Aug window (which contains the corpus's own
  June–July test window). A structured train/test grid over trigger TF,
  barriers, force, shell and session found **zero** honest survivors.
- **The corpus reports were not accurate as profit claims.** They measured
  hit rate without costs on pooled books (the accuracy program), and the
  CCI 100%-WR result was a 44-trade single-window artifact. This folder's own
  `00_intuition.md` P2.3/P2.6 predicted exactly this failure mode.
- Consequences: **do not run this EA on a funded account expecting to pass
  FTMO, and +2.5%/day is not achievable with this entry layer** (real cadence
  ~0.2–2 trades/day). What it *is*: a validated FTMO risk harness waiting for
  a real edge (the lab's A14/A29 meta-trained brain path is the intended one).

## What it is

A single-file MQL5 EA (`FTMO_Sentinel_EA.mq5`): corpus-geometry entries
(CCI M-line reclaim under dual-HTF force, Mark BB-mass gate, accuracy shell,
ATR barrier exits) wrapped in a **Day Governor** whose priority order is:

1. never breach an FTMO limit (daily −5%, total −10%),
2. never let a green day close red,
3. bank the daily goal and stop.

## The Day Governor (the part that survived testing)

| Rail | Setting (default) | FTMO frame |
|---|---|---|
| Daily goal bank | flatten + stop at **+2.5%** | consistency objective |
| Green-day ratchet | armed at +0.8% peak; floor = max(+0.2%, 60% of peak) | green day cannot close red |
| Soft daily stop | −1.5% → no new trades | FTMO allows −5% |
| Hard daily stop | −2.0% → flatten everything | 3% buffer never used |
| Per-trade risk cap | one loss can never cross the daily budget | structural |
| House-money ladder | risk = 0.5% + 0.5 × day profit %, cap 1.0% | escalation from banked profit only |
| Loss-streak halving + 3-loss day stop | halve per loss; stop day at 3 | kills thrash days |
| Total fuse | **−6% → permanent halt** | account preserved before FTMO −10% |
| Challenge manager | stop at +10%; ticket micro-trades until ≥4 trading days | pass conditions handled |

Day state is shared account-wide via terminal globals (multi-symbol safe;
flags synced every tick).

## Test harness (how to re-measure — do this before believing anyone)

```bash
python3 fetch_dukascopy.py EURUSD 2026-01-05 2026-08-07   # M1, authoritative (slow: rate-limited)
python3 fetch_yahoo.py EURUSD                             # M5 60d, quick secondary
python3 backtest_sentinel.py EURUSD                       # all variants, writes BACKTEST_EURUSD.md
python3 grid_search.py EURUSD 2026-06-01                  # train/test objective grid
```

The backtester mirrors the EA bar-for-bar: closed-bar signals, next-open
entries, real spread+commission, M1 barrier adjudication with the
conservative same-bar-loss rule, full governor on the M1 equity path.

## Setup (paper/testing only, given the verdict)

1. Compile `FTMO_Sentinel_EA.mq5` in MetaEditor, attach to M15/M30 charts
   (M5 measured toxic net of costs).
2. Defaults = least-bad measured config: Engine A (CCI) + mass gate,
   base risk 0.5%, ladder cap 1.0%.
3. Set `InpInitialBalance` and `InpDayResetHour` (server hour of FTMO
   midnight CE(S)T).
4. Demo / strategy tester only until a new edge source passes the harness
   train/test and a full Court case.

## Court status

Experimental quarantine. The measurement here is Summary-Court evidence
(A33 measurement + issue regeneration); any production/promote claim needs a
full A10 adversarial case, A15 Counsel opinion, multi-window multi-symbol
replication, and a ledger event.

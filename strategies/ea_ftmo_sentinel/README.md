# FTMO Sentinel EA — validated risk shell, UNVALIDATED edge

**Status: EXPERIMENTAL — not Court law.** Quarantined per "Court before major
decisions" until a full Evidence Court case (A10 + A15).

## Measured verdict (2026-08-12 — read before anything else)

Everything below was measured on **real downloaded market data** with a
bar-accurate replica of this EA (see [`VALIDATION.md`](VALIDATION.md)):

- **The protection layer works.** Across every window, symbol and variant:
  worst day close −1.50%, worst intraday float −1.49%, **zero** FTMO daily or
  total breaches. The Day Governor does exactly what it promises.
- **The corpus reclaim engines failed** (win rates 70–76% replicate; money is
  negative after costs — the corpus reports were hit-rate proofs, not profit
  proofs). They remain selectable for lab use only.
- **The creative hunt found two survivors** (v3):
  - **Engine D — Keltner fade** (default): fade beyond EMA20 ± 2·ATR with an
    H4 trend veto and stretch-scaled lot sizing. Positive on both time splits
    on real EURUSD (7 months) **and** real GBPUSD M1. European pairs only.
  - **Engine C — London ORB**: strong and robust on EURUSD (train +6.1%,
    test +14.4%, 74% of the parameter neighborhood positive) but **failed
    cross-symbol** — treat as an EURUSD-only second leg.
- **Measured portfolio** (fade on EURUSD+GBPUSD, ORB on EURUSD, shared
  governor, approximation labelled in the report): **+49.9% over 7 months,
  mean day +0.27%, worst day −1.50%, zero breaches; 66% of challenge
  walk-forward starts pass, median 24 trading days.**
- Still true and non-negotiable: **"+2.5% every day" and "pass every time"
  are not physically guaranteeable.** P(day ≥ +2.5%) ≈ 7% on the measured
  book; the governor banks those days when the market offers them and keeps
  every other day green-or-small-red. Forward-test on demo before money.

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

## Setup (demo first — the measured book is 7 months of one regime)

1. Compile `FTMO_Sentinel_EA.mq5` in MetaEditor.
2. **Keltner fade legs (default mode):** attach to EURUSD M30 and GBPUSD M15
   charts, same magic number (shared governor). M5 measured toxic — avoid.
3. **ORB leg (optional):** attach a second instance to EURUSD M15 with
   `InpEntryMode = MODE_LONDON_ORB` and a **different magic number**;
   align `InpOrbRangeEndHour` to 07:00 UTC in server time. EURUSD only.
4. Set `InpInitialBalance` and `InpDayResetHour` (server hour of FTMO
   midnight CE(S)T).
5. Strategy-test each leg (every tick, real spreads), then demo / FTMO free
   trial. Funded only after the forward test agrees with the measurement.

## Court status

Experimental quarantine. The measurement here is Summary-Court evidence
(A33 measurement + issue regeneration); any production/promote claim needs a
full A10 adversarial case, A15 Counsel opinion, multi-window multi-symbol
replication, and a ledger event.

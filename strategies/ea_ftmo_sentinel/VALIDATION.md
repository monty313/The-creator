# FTMO Sentinel — validation report (REAL-DATA MEASUREMENT, v2 final)

**Not Court law. Measured 2026-08-12 on real downloaded market data —
final numbers below use the complete 7-month Dukascopy M1 set
(2026-01-05 → 2026-08-07, 219,454 bars), which includes the corpus's own
June–July claim window.** This version supersedes the v1 parametric Monte
Carlo, whose optimistic scenarios were **falsified by measurement**.

## Verdict (read this first)

| Claim | Status |
|---|---|
| Governor safety: no FTMO daily (−5%) or total (−10%) breach | **VALIDATED** — 0 breaches across every window, symbol, variant; worst day close −1.50%, worst intraday float −1.49% |
| Green-day ratchet / daily stops behave as designed | **VALIDATED** on real M1 tick-path |
| Corpus entry edge (CCI reclaim / McFlurry) makes money net of costs | **FAILED** — every variant negative on every tested window |
| High corpus win rates | **Replicated directionally** (WR 70–76% with first-breath barriers) — but hit rate ≠ profit |
| +2.5%/day consistency | **NOT ACHIEVABLE** with this entry layer — real cadence is ~0.2–1.1 trades/day, not 20 |
| "Pass FTMO every time" | **NO** — challenge walk-forward never passes on measured data (timeout or self-halt at the −6% fuse; never a breach) |

## Method (why this test is honest where the corpus reports were not)

- **Data:** Dukascopy M1 bid candles, EURUSD 2026-01-05 → 2026-08-07 (219,454
  bars, authoritative, includes the corpus's June–July claim window) + Yahoo M5
  EURUSD/GBPUSD 2026-05-20 → 2026-08-12 (secondary cross-check).
  Fetchers in this folder.
- **Execution model:** signals on closed trigger-TF bars only, entry next bar open,
  0.7-pip all-in cost (EURUSD), exits adjudicated bar-by-bar on M1; when one M1 bar
  touches both barriers the trade counts as a **loss** (conservative).
- **Governor** runs exactly as in the EA (per-M1-close watchdog).
- The corpus pipeline, by contrast: vectorbt fractional barriers, **no costs**,
  pooled 4-set×2-mode books, one 27-day window — that is why its numbers
  (100% WR, MC P(loss)=0%) did not survive.

## Headline table — EURUSD real M1, 2026-01-05 → 2026-08-07 (183 trading days)

| Variant | Trades | WR | Total P&L | Worst day | FTMO breaches | Challenge (183 starts) |
|---|---|---|---|---|---|---|
| default (A+B, mass gate) | 77 | 67.5% | **−9.50%** | −1.50% | 0 | 100% timeout |
| no_mass (A+B) | 186 | 70.4% | **−18.49%** | −1.50% | 0 | 37% fuse-halt, 63% timeout |
| cci_only (A, no mass) | 99 | 71.7% | **−8.07%** | −1.30% | 0 | 100% timeout |
| cci_mass (A + mass, EA default) | 33 | 69.7% | **−3.29%** | −0.80% | 0 | 100% timeout |
| mcf_only (B, no mass) | 127 | 68.5% | **−12.51%** | −1.50% | 0 | 16% fuse-halt, 84% timeout |
| a15 (M15, balanced barriers) | 37 | 56.8% | −0.91% | −0.80% | 0 | 100% timeout |
| a15w (M15, wide TP) | 37 | 35.1% | −3.15% | −1.20% | 0 | 100% timeout |

**The corpus's own claim window fails in real M1:** the corpus-style `default`
config loses −1.5% in June and −2.8% in July 2026 — the exact period where
`CCI_VS_MCFLURRY_REPORT` printed 100% WR and +0.22% mean return with cost-free
vectorbt accounting.

Secondary source cross-check (Yahoo M5, May 20 → Aug 12): same picture — all
variants between −0.1% and −7.1% total, zero breaches (`BACKTEST_EURUSD_Y.md`).
GBPUSD cross-check agrees (`GRID_GBPUSD_Y.csv`).

## Structured search found no honest survivor

A grid over the corpus P2.8 repair classes (trigger TF 5/15/30m · barrier
objective TP/SL 0.7–2.0×ATR · force threshold 4/8 · shell filters on/off ·
session subsets · engine mix · mass gate), evaluated with a train/test date
split: **0 configurations were positive on both splits** with ≥60 trades
(`GRID_EURUSD.csv`, `GRID_EURUSD_Y.csv`, `GRID_GBPUSD_Y.csv`).

Key structural facts the grid did establish:

1. **M5 trigger is toxic net of costs** (cost ≈ 25–30% of a 0.7·ATR take-profit).
2. **High WR replicates; profit does not.** The first-breath barrier pair prints
   WR 70–76% and still bleeds — exactly the trap `00_intuition.md` P2.3/P2.6
   warned about ("Do not ship the accuracy layer as the production brain").
3. **Real cadence is 0.2–2.2 trades/day**, not the ~20/day the corpus's pooled
   multi-set books implied. The 2.5%/day goal machinery has nothing to compound.
4. Engine A (CCI) consistently loses less than Engine B (McFlurry); the mass
   gate reduces both trade count and bleed. Least-bad measured config =
   **cci_mass**, now the EA default. Least-bad ≠ good.

## Why the corpus reports were "not accurate"

The reports measured what they said they measured — but that was never
live-EA profit:

- `TWEAKED_ACCURACY_REPORT` proved **hit rate** (>60.4% WR), openly labelled an
  accuracy program, **without costs**. Confirmed here: high WR, negative EV.
- `CCI_VS_MCFLURRY_REPORT`'s 100% WR / +0.22% figure came from **44 trades on
  one 27-day window** with optimistic barrier accounting. It does not replicate
  on any other window tested, including the *same* June–July period through an
  honest execution model.
- Monte Carlo rank 13 / P(loss)=0% resampled that same 44-trade book — garbage
  in, confident garbage out.

## What the v1 parametric sim got right and wrong

Right: the governor mathematics (red-day cap ≈ soft stop, zero breach at
trade-close granularity) — confirmed on real data. Wrong: scenario A assumed
WR 92% at +0.243R with 20 signals/day; measured reality is WR ~70% at +0.243R
(≈ breakeven pre-cost, negative post-cost) with ~1–2 signals/day — i.e. the
sim's scenario C/D, whose outcome is fuse-halt, not pass.

## What would have to change before anyone runs this for money

1. A **new edge source** that is positive on a train/test split net of costs
   (the lab's A14/A29 meta-trained brain path, or a re-derived entry law) —
   then plug it into the Sentinel's validated risk shell.
2. Re-measure with this harness (fetch → backtest → grid) on ≥2 symbols and
   ≥2 disjoint windows before believing any number.
3. Per Court law: full A10+A15 case before any promote claim.

## Files

| File | Role |
|---|---|
| `backtest_sentinel.py` | Bar-accurate EA replica backtester |
| `fetch_dukascopy.py` / `fetch_yahoo.py` | Data fetchers (M1 authoritative / M5 secondary) |
| `grid_search.py` | Train/test objective-space grid |
| `BACKTEST_EURUSD.md`, `BACKTEST_EURUSD_Y.md` | Full per-variant reports |
| `GRID_*.csv` | Grid results |
| `governor_sim.py` | v1 parametric governor MC (kept: governor math reference) |

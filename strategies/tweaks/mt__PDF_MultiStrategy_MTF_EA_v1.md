# Tweak record: `mt__PDF_MultiStrategy_MTF_EA_v1`

**Title:** PDF_MultiStrategy_MTF_EA_v1  
**Kind:** mt  
**Source language:** `strategies/language/01_METATRADER_INDEX.md :: PDF_MultiStrategy_MTF_EA_v1 (.mq5)`  
**Adapter profile:** `rl_proxy`  
**Pass gate (win_rate > 60.4 & trades ≥ 25):** YES

## Baseline (pre-tweak)

| Metric | Value |
|--------|------:|
| Win rate (accuracy) % | 46.6399 |
| Note | From prior full-batch / sauces report if present; else 0 |

## What was changed (full detail)

### Tier selected: `A_first_breath`

| Parameter | Value | Role |
|-----------|------:|------|
| tp_stop | 0.00025 | Take first unit of progress (~pips on EURUSD) |
| sl_stop | 0.001 | Invalidate failed thesis |
| max_hold (LTF bars) | 0 | Kill dead trades |
| session 07–21 UTC | True | London/NY concentration |
| HTF strength vs SMA50 | True | Real force, not flat mass |
| bar confirm (close vs open) | True | Candle agrees with side |
| micro structure HL/LH | True | Pullback-resume texture |


### Accuracy tweaks (Mark knowledge)

1. **HTF strength filter** — dual HTF closes must sit away from SMA(50) in the trade direction.
   Flat "mass" without distance is fake permission; killed thrash entries that lose more often.

2. **Session mask (07–21 UTC)** — London/NY concentration. Off-session prints are noisier;
   removing them raises hit rate of structure-based fires.

3. **Bar confirmation** — entry bar close must agree with side (close>open for long).
   Avoids firing into a bar that already failed the release candle.

4. **Micro structure** — long only if recent higher-low texture; short if lower-high.
   Aligns with pullback-resume physics: eddy ends with constructive structure.

5. **Exit: tight TP / wider SL via vectorbt stops (no time-stop thrash)** — take the *first unit*
   of continuation (small TP), invalidate with a larger SL if thesis fails. Probability of
   tagging TP first rises when TP distance << SL distance (barrier math), *when* entries are
   not anti-edge. This is an accuracy-first scalp policy (H001-style "first breath"), not a
   claim of better expectancy under all costs.

6. **Optional time hold** — only used if configured; default accuracy path uses pure TP/SL
   so random mid-hold flats do not destroy hit rate.


### Family-specific note

Profile `rl_proxy` keeps this family's original signal language; accuracy layer is the shared Mark filter + TP/SL tier `A_first_breath`.

## Why (Mark knowledge)

- Permission comes from **dual HTF force with distance** — without it, LTF fires are thrash.  
- Timing stays **pullback vs continuation** on LTF under that force.  
- Accuracy rises by **banking the first breath** of a valid release and refusing off-session / flat-mass / anti-structure bars.  
- This is **not** production Court law; it is a measured accuracy experiment for teaching labels.

## Final measured scores (post-tweak)

| Metric | Value |
|--------|------:|
| Win rate (accuracy) % | 71.2119 |
| Total trades (sum set×mode) | 1295 |
| Total return % (avg set×mode) | -0.7631 |
| Max drawdown % (avg) | 1.2871 |
| Profit factor (avg) | 0.8121 |
| Sharpe (avg) | -3.2054 |
| Aggregate score | 80.1292 |
| Runs (set×mode) | 8 |

**Delta win rate:** +24.5720 pp vs baseline.

## Contract

2 HTF + 1 LTF · sets `1m/15m/30m`, `5m/30m/1h`, `15m/1h/4h`, `30m/4h/1d` · modes pullback + continuation · vectorbt Portfolio.from_signals.

<!-- MONTE_CARLO_BEGIN -->
## Monte Carlo simulation results

**Family id:** `mt__PDF_MultiStrategy_MTF_EA_v1`  
**MC rank (by bootstrap median terminal):** **108** / 139  
**Not Court law.** Bootstrap + order-shuffle on pooled trade returns.

### Simulation setup

| Field | Value |
|-------|-------|
| Window | 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1) |
| Data | `C:\Users\user\Downloads\_OTHER_PROJECTS\ATI_FTMO_project\gravity_engine\data\EURUSD_M1_export.csv` |
| Sims (bootstrap) | 1000 |
| Seed | 42 |
| Sets | `set1_1m_15m_30m, set2_5m_30m_1h, set3_15m_1h_4h, set4_30m_4h_1d` |
| Modes | pullback + continuation |
| Entry shell | session 07–21 UTC, HTF strength, bar confirm, micro structure |
| Exits | tp_stop=0.00025 · sl_stop=0.001 (vectorbt) |
| vectorbt | 1.1.0 |

### Trade book (input to MC)

| Metric | Value |
|--------|------:|
| Pooled trades | 1295 |
| Mean trade return | -0.004733% |
| Historical terminal (compound order of book) | 0.940261× |
| Historical max DD | 6.3471% |

### Bootstrap Monte Carlo (with replacement)

Resample the trade-return vector **with replacement**, same length, **1000** paths. Terminal wealth starts at 1.0 and compounds trade returns.

| Metric | Value |
|--------|------:|
| Median terminal wealth | 0.940236× |
| Mean terminal wealth | 0.940692× |
| p05 terminal | 0.903343× |
| p25 terminal | 0.925379× |
| p75 terminal | 0.955820× |
| p95 terminal | 0.977991× |
| P(loss) = P(terminal < 1) | 99.90% |
| P(max DD ≥ 20%) | 0.00% |
| Median path max DD | 6.6989% |
| p95 path max DD | 10.1702% |

### Order-shuffle Monte Carlo (sequence risk)

Same trades, **permute order** (no replacement). Isolates path dependence from trade *sequence*.

| Metric | Value |
|--------|------:|
| Shuffle median terminal | 0.940261× |
| Shuffle p05 terminal | 0.940261× |
| Shuffle P(loss) | 100.00% |

### How to read

- **MC med > 1**: more than half of bootstrap paths finish above start.
- **P(loss) high + hist WR high**: hit rate may look good while resampled paths still lose — fragile edge / costs.
- **Low trade count**: percentiles are less stable; treat extreme WR paths carefully.
- Full table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

**Notes:** bootstrap with replacement + order shuffle

<!-- MONTE_CARLO_END -->

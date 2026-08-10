# HYPOTHESIS H001 — "McFlurry Eddy" Trend-Pullback Scalp

**Status:** UNTESTED HYPOTHESIS (for the system to validate). **Created:** 2026-07-11.
**Source insight:** McFlurry's cross-timeframe momentum divergence (a) spots a short-term dip inside
a bigger trend, and (b) tells a *genuinely accelerating* trend from one that's just "sitting high."
This strategy uses **both**: insight #1 as the *entry setup*, insight #2 as the *quality filter*.

---

## The idea in one sentence
When the big trend is genuinely running up, a brief 5-minute momentum dip that then snaps back up is a
high-odds moment to scalp **with** the trend (mirror for downtrends). "Buy the little backward eddy
inside the strong forward river."

---

## The tool: McFlurry, per timeframe
Build the McFlurry stack on each timeframe:
- `RSI(13, close)`
- `SMA7 = SMA(7)` of the RSI, `SMA21 = SMA(21)` of the RSI
- **Momentum line `M = SMA7 − SMA21`** → `M > 0` = momentum accelerating up, `M < 0` = down.

(This is the exact divergence measured in the regime files: `Sauce_Documentation.McFlurry.{TF}.SMA7_minus_SMA21_mean`.)

---

## Entry rules (LONG; short = mirror)
Timeframes: **context = 4H + 30M · trigger = 5M**.

1. **Trend up (context):** `M_4H > 0` **and** `M_30M > 0` (higher timeframes accelerating up).
2. **Genuine-trend filter (insight #2 — reject the "fake extreme"):** `M_4H ≥ +1.5`.
   - Why +1.5: in the data, a *real* accelerating extreme read `M_5M ≈ +5.3` while the *fake*
     (price-high-but-flat) extreme read `M_5M ≈ +0.1`. Requiring a clearly-positive `M` on the 4H
     keeps you out of "high but not moving" traps. (Tune this number in testing.)
3. **The dip (the eddy):** `M_5M` crosses **below 0** (5-minute momentum rolls over) — the pullback.
4. **The trigger (dip ending):** `M_5M` crosses **back above 0** → **ENTER LONG** at that 5M bar's
   close (or next-bar open, no look-ahead).

Short side: flip every sign (`M_4H < 0`, `M_4H ≤ −1.5`, `M_5M` crosses above 0 then back below 0).

---

## Exit rules (scalp) — test all three, keep the best net of spread
The fractal (max favorable move) in the data averaged **~25 pips / ~1.8×ATR** per trade, so keep targets tight:
- **A. Fixed ATR:** stop = `1 × ATR(14, 5M)`, target = `2 × ATR(14, 5M)` (risk:reward 1:2).
- **B. Canonical:** the **1m-bb-exit** (BB(20,1) on High → exit long at the lower band; mirror for shorts).
- **C. Trailing:** exit when price crosses the **SMA(4, shift+4) of typical price** on the 5M.

---

## What would PROVE THIS WRONG (falsification — must be checked)
1. **No lift over the trigger:** if entering at *random* 5M bars inside the same trend+filter context
   performs as well as the McFlurry trigger, the eddy signal adds nothing → reject.
2. **Doesn't beat noise + cost:** across **≥150 trades on ≥3 assets**, if `win_rate × reward:risk`
   does not clearly beat the **pure-noise baseline** for that same R:R (measured: ~+0.05–0.10R on
   wide targets) **and** cover a realistic spread, there is no edge → reject.
3. **Just asset drift:** if the edge exists only on the strong-uptrend assets (XAUUSD, US30) and
   disappears on EURUSD/GBPUSD → it's the market trending, not the signal → reject.

---

## How the system should test it
1. **Label entries** by the rules above across all 4 assets (EURUSD, GBPUSD, XAUUSD, US30).
2. **Run all three exits**; report win rate, expectancy (EV in R **and** in pips **after** a realistic
   spread), average/median favorable move, trades/day.
3. **Two control tests** (the important ones):
   - *Random-entry control:* same trend+filter context, random 5M entries → measures the trigger's added value.
   - *No-filter control:* drop the `M_4H ≥ +1.5` filter → measures whether insight #2 actually helps.
4. **Pass bar:** ≥150 trades, positive EV **after spread**, and positive lift over BOTH controls, on
   more than one asset (not just the trending ones).

---

## Honest caveats (do not skip)
- **Scalping lives or dies on spread.** A ~25-pip average favorable move is small; on EURUSD a ~1-pip
  spread eats a real slice. Test with true spread, not gross.
- **This inherits NO edge from the regimes.** The foundation showed regimes have no standalone edge;
  this is a *new composition* (McFlurry timing inside a trend) and must earn its result from scratch.
- **The +1.5 filter and 1:2 target are starting guesses** from the observed numbers — the test should
  sweep them, not treat them as final.
- **McFlurry is built on RSI**, which correlates with the CCI that defines the trend regimes — so the
  trend filter and the trigger aren't fully independent; the *cross-timeframe sign-flip* is the part
  that carries new information, and that's what the random-entry control isolates.

---

## Ingredients map (where each piece comes from in the data)
| Piece | Source |
|---|---|
| McFlurry `M = SMA7−SMA21` per TF | `Sauce_Documentation.McFlurry.{TF}` in each regime file |
| "Genuine" threshold (~+1.5) | Extreme Bull CCI `M_5M=+5.26` (real) vs Extreme Bull BB `M_5M=+0.11` (fake) |
| Trend context reference | `01_bull_momentum`, `06_bull_market` regime files |
| Exit calibration (target/MFE) | `Exit_Backtests` (ATR 1:2, MFE ~25 pips) + `backtest_1m_bb_exit` |
| Noise baseline to beat | ~+0.05–0.10R at wide R:R (from the engine's tick-truth test) |

<!-- MONTE_CARLO_BEGIN -->
## Monte Carlo simulation results

**Family id:** `sauce__mcflurry_eddy_scalp`  
**MC rank (by bootstrap median terminal):** **16** / 139  
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
| Pooled trades | 212 |
| Mean trade return | 0.002787% |
| Historical terminal (compound order of book) | 1.005888× |
| Historical max DD | 0.8054% |

### Bootstrap Monte Carlo (with replacement)

Resample the trade-return vector **with replacement**, same length, **1000** paths. Terminal wealth starts at 1.0 and compounds trade returns.

| Metric | Value |
|--------|------:|
| Median terminal wealth | 1.005718× |
| Mean terminal wealth | 1.005500× |
| p05 terminal | 0.990582× |
| p25 terminal | 0.999903× |
| p75 terminal | 1.011834× |
| p95 terminal | 1.018930× |
| P(loss) = P(terminal < 1) | 25.60% |
| P(max DD ≥ 20%) | 0.00% |
| Median path max DD | 0.7537% |
| p95 path max DD | 1.5827% |

### Order-shuffle Monte Carlo (sequence risk)

Same trades, **permute order** (no replacement). Isolates path dependence from trade *sequence*.

| Metric | Value |
|--------|------:|
| Shuffle median terminal | 1.005888× |
| Shuffle p05 terminal | 1.005888× |
| Shuffle P(loss) | 0.00% |

### How to read

- **MC med > 1**: more than half of bootstrap paths finish above start.
- **P(loss) high + hist WR high**: hit rate may look good while resampled paths still lose — fragile edge / costs.
- **Low trade count**: percentiles are less stable; treat extreme WR paths carefully.
- Full table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

**Notes:** bootstrap with replacement + order shuffle

<!-- MONTE_CARLO_END -->

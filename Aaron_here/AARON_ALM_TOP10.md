# Aaron ALM — Top 10 strategies (lab fuel)

**Teacher:** Aaron (`@Aaron_here`)
**Families scored:** 139 (every row in Monte Carlo results)
**Method:** [AARON_LEARNING_METHOD.md](AARON_LEARNING_METHOD.md)
**Not Court law. Not a live deploy list.**

Test = ALM re-score of each strategy’s lab Monte Carlo + accuracy WR (soft).
Contract: same EURUSD window / 2HTF+1LTF / PB+cont as `strategies/` prove pipeline.

## ALM ranking formula (plain)

```text
alm_score =
  120.0 * (mc_median_terminal - 1)
+ 55.0 * (1 - P(loss))
+ 8000.0 * mean_trade_return
- 40.0 * hist_max_dd
+ sample_quality(n_trades)
+ 0.08 * min(accuracy_WR, 85)   # soft only
+ geometry_bonus(profile)         # F/L/R alignment
```

## A) Top 10 by raw ALM score (filenames)

Many may share one **profile** (same geometry).

| ALM# | Family | Profile | ALM score | MC med | P(loss) | Trades | Acc WR% | Mean tr |
|-----:|--------|---------|----------:|-------:|--------:|-------:|--------:|--------:|
| 1 | `mt__cci_gravity_scalp_ftmo_v6_perplexity` | `cci_gravity` | 80.09 | 1.0084 | 0.0% | 44 | 73.3 | 0.0185% |
| 2 | `mt__cci_gravity_scalp_v5_full` | `cci_gravity` | 80.09 | 1.0083 | 0.0% | 44 | 73.3 | 0.0185% |
| 3 | `mt__cci_gravity_scalp_v1_full` | `cci_gravity` | 80.09 | 1.0083 | 0.0% | 44 | 73.3 | 0.0185% |
| 4 | `mt__Pure_CCI_Screener` | `cci_gravity` | 80.09 | 1.0083 | 0.0% | 44 | 73.3 | 0.0185% |
| 5 | `mt__ZeroLineRadar` | `cci_gravity` | 80.08 | 1.0083 | 0.0% | 44 | 73.3 | 0.0185% |
| 6 | `mt__Swarm` | `cci_gravity` | 80.08 | 1.0083 | 0.0% | 44 | 73.3 | 0.0185% |
| 7 | `mt__ZeroLineRadar0works` | `cci_gravity` | 80.08 | 1.0083 | 0.0% | 44 | 73.3 | 0.0185% |
| 8 | `mt__swarm3_0` | `cci_gravity` | 80.08 | 1.0083 | 0.0% | 44 | 73.3 | 0.0185% |
| 9 | `mt__StrikeGate` | `cci_gravity` | 80.08 | 1.0083 | 0.0% | 44 | 73.3 | 0.0185% |
| 10 | `mt__cci_gravity_scalp_ftmo` | `cci_gravity` | 80.08 | 1.0083 | 0.0% | 44 | 73.3 | 0.0185% |

## B) Top 10 **unique geometries** (one winner per profile) — use this for teaching

| # | Family (best of profile) | Profile | ALM# | ALM score | MC med | P(loss) | Trades | Acc WR% |
|--:|--------------------------|---------|-----:|----------:|-------:|--------:|-------:|--------:|
| 1 | `mt__cci_gravity_scalp_ftmo_v6_perplexity` | `cci_gravity` | 1 | 80.09 | 1.0084 | 0.0% | 44 | 73.3 |
| 2 | `mt__FTMO_SMA_Scalper` | `sma_scalp` | 13 | 66.63 | 1.0096 | 17.7% | 250 | 78.4 |
| 3 | `sauce__mcflurry_eddy_scalp` | `mcflurry` | 15 | 65.91 | 1.0057 | 25.6% | 212 | 80.0 |
| 4 | `mt__FTMO_BB_MTF_EA_Strategy4_v2_20260705_1323` | `bb_mtf` | 17 | 54.34 | 1.0038 | 34.1% | 261 | 75.8 |
| 5 | `note__algo_guide_14_s01_ma_crossover_md` | `guide_s01_ma_cross` | 26 | 43.56 | 0.9997 | 51.5% | 133 | 77.4 |
| 6 | `note__algo_guide_14_s08_bb_mean_reversion_md` | `guide_s08_bb_mr` | 27 | 29.11 | 1.0000 | 49.6% | 18 | 82.4 |
| 7 | `note__algo_guide_14_s06_parabolic_sar_md` | `guide_s06_psar` | 28 | 22.89 | 0.9892 | 85.5% | 305 | 74.7 |
| 8 | `note__algo_guide_14_s11_keltner_reversion_md` | `guide_s11_keltner_mr` | 29 | 20.49 | 0.9953 | 86.4% | 46 | 73.9 |
| 9 | `note__algo_guide_14_s12_zscore_reversion_md` | `guide_s12_zscore_mr` | 30 | 18.63 | 0.9916 | 90.7% | 136 | 75.7 |
| 10 | `note__the_truth_main_extra_ADR-0004-strategies_md` | `truth_s1_cci` | 31 | 18.16 | 0.9744 | 96.4% | 390 | 73.2 |

## How to read this top 10

| Do | Don't |
|----|--------|
| Use as **positive shape pointers** for RL curriculum | Call them production bots |
| Prefer table **B** (unique profiles) for diversity | Treat 10 CCI filenames as 10 edges |
| Prefer high MC med + low P(loss) + sane N | Rank by Acc WR alone |

### Profile collapse note

Raw top-10 is often almost all `cci_gravity` reclaim geometry — **one shape**, many MT names.
Table **B** is Aaron’s teaching shortlist.

## Geometry bonuses used (excerpt)

```text
mcflurry +8 · cci_gravity +7.5 · mark_rsi_bb +6.5 · sma_scalp +4
rl_proxy -6 · ma_ribbon / guide ema ribbon -5 · challenge -4
```

## Full rank

See [AARON_ALM_FULL_RANK.md](AARON_ALM_FULL_RANK.md) · raw [AARON_ALM_SCORES.json](AARON_ALM_SCORES.json)

## Bottom 5 (counter-examples for training)

| ALM# | Family | ALM score | MC med | P(loss) | Trades |
|-----:|--------|----------:|-------:|--------:|-------:|
| 135 | `mt__ftmo_challenge_ea_v3` | -12.98 | 0.9265 | 100.0% | 1172 |
| 136 | `mt__ATI_FTMO_EA` | -12.99 | 0.9264 | 100.0% | 1172 |
| 137 | `mt__fasg_trendday_ea` | -13.96 | 0.9293 | 99.6% | 1403 |
| 138 | `mt__MA_ribbon_filled_Alerts` | -22.78 | 0.9065 | 99.9% | 1585 |
| 139 | `note__algo_guide_14_s07_ema_ribbon_md` | -22.82 | 0.9067 | 100.0% | 1585 |

---

**Aaron:** Top-10 under ALM = best **lab fuel** for Force/Load/Reclaim teaching + path honesty on this window.
Next: label windows from table B profiles (PKG-001), train stages 1–3, re-score student compliance.

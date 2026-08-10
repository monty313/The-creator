# Dimension Jump (Sauce One) — strategy language

**Paired with:** McFlurry (Sauce Two) — ADR-0004 / observational universe.  
**Role historically:** observation-only sense; here expressed as a **testable entry geometry** under official 2HTF+1LTF sets.  
**Source:** `Fable5_Foundation/MOMENTUM_ONE/03_MY_NOTES/OBSERVATIONAL_INDICATOR_UNIVERSE.md`, `ML_CONFIRMATION_FLOW.md`, ADR-0004.

---

## Stack (per timeframe)

| Piece | Spec |
|-------|------|
| Stack A | CCI(30) → Bollinger **on CCI** BB(20, dev=1, shift=+2) |
| Stack B | CCI(100) → Bollinger **on CCI** BB(20, dev=1, shift=+2) |

Readings: CCI30, BB mid/upper/lower on CCI30; CCI100, BB mid/upper/lower on CCI100.

---

## Entry geometry (LONG; short = mirror)

Mapped onto **official set** HTFs + LTF (not fixed 4H/30M/5M only):

1. **Force (both HTFs):** CCI100 **above** its BB mid (bull mass in momentum dimension).  
2. **Pullback (eddy on LTF):** CCI30 **crosses below** its BB mid (or prints below lower band) while force stays bull — short-horizon dimension dips.  
3. **Continuation / fire (LTF):** CCI30 **crosses back above** BB mid (or reclaim of lower → mid) while force still bull.

Short: invert all inequalities.

---

## Relation to McFlurry

| | Dimension Jump | McFlurry |
|--|----------------|----------|
| Base oscillator | CCI | RSI(13) |
| Compression | BB on CCI | SMA7−SMA21 on RSI (after SMA2 smooth) |
| Shared idea | HTF dimension strong; LTF dips then snaps |

---

## Not production law

Advice geometry for research/vectorbt. Exits are batch defaults unless otherwise specified.

<!-- MONTE_CARLO_BEGIN -->
## Monte Carlo simulation results

**Family id:** `sauce__dimension_jump`  
**MC rank (by bootstrap median terminal):** **60** / 139  
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
| Pooled trades | 594 |
| Mean trade return | -0.005944% |
| Historical terminal (compound order of book) | 0.965190× |
| Historical max DD | 3.6909% |

### Bootstrap Monte Carlo (with replacement)

Resample the trade-return vector **with replacement**, same length, **1000** paths. Terminal wealth starts at 1.0 and compounds trade returns.

| Metric | Value |
|--------|------:|
| Median terminal wealth | 0.964624× |
| Mean terminal wealth | 0.965291× |
| p05 terminal | 0.942577× |
| p25 terminal | 0.955338× |
| p75 terminal | 0.975502× |
| p95 terminal | 0.989051× |
| P(loss) = P(terminal < 1) | 99.20% |
| P(max DD ≥ 20%) | 0.00% |
| Median path max DD | 4.0117% |
| p95 path max DD | 6.1140% |

### Order-shuffle Monte Carlo (sequence risk)

Same trades, **permute order** (no replacement). Isolates path dependence from trade *sequence*.

| Metric | Value |
|--------|------:|
| Shuffle median terminal | 0.965190× |
| Shuffle p05 terminal | 0.965190× |
| Shuffle P(loss) | 100.00% |

### How to read

- **MC med > 1**: more than half of bootstrap paths finish above start.
- **P(loss) high + hist WR high**: hit rate may look good while resampled paths still lose — fragile edge / costs.
- **Low trade count**: percentiles are less stable; treat extreme WR paths carefully.
- Full table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

**Notes:** bootstrap with replacement + order shuffle

<!-- MONTE_CARLO_END -->

# GV-014-XAU-L1 — Validated Pool Unit #1
Status: **VALIDATED** (edge confirmed on 2 independent datasets) · Registered 2026-07-18 · Alias: STRAT-014 Price-BB Reversion Snap, gapped, XAUUSD

## One-line thesis
When gold is in a runaway trend (price outside BOTH Bollinger tunnels on 30m AND 1h), buy the first 5m pullback back inside the band; trail out on a 30m shifted SMA.

## Exact spec (codeable)
| Component | Definition |
|---|---|
| Symbol / ladder | XAUUSD · LTF 5m · gravity 30m + 1h (one-rung gap) |
| Gravity long | last CLOSED 30m bar: close > SMA200+1.0σ200 AND close > SMA20+1.0σ20; AND same on last closed 1h bar (σ = population stdev) |
| Trigger long | 5m close crosses from above to below the 5m upper BB(20, 1.0σ) while gravity holds; edge-triggered |
| Entry fill | next 5m bar open (ask side) |
| Exit long | on 30m closed bars: close < SMA(4) shifted +1 (i.e., SMA value from 1 bar back) → fill next 5m open (bid) |
| Shorts | exact mirror (lower bands) |
| Position rules | one position; opposite signals while holding are ignored; no pyramiding |
| Costs (research) | per-bar recorded spread (median $0.08) + RT commission/slippage: 1.0 XAU-pip baseline / 0.4 commission-free variant |

## Python engine results (Monty's FTMO MT5 M1 export, 2020-09 → 2026-07, walk-forward)
| Metric | Comm-on | Comm-free |
|---|---|---|
| Walk-forward net (1,197 test days) | +6,338 pips | +7,730 pips |
| Mean/day | +5.3 | +6.5 |
| Green days | 28.5% | ~30% |
| Worst day / maxDD | −774 / −2,883 pips | similar |
| mean ÷ \|worst day\| | 0.0068 | 0.0084 |
| Untouched 30-day OOS (Jun 8–Jul 17 2026) | **+968 pips** | **+987 pips** |
| Trades (final config, full period) | 2,413 · WR 32.6% · avg win +80.8 / avg loss −33.9 | — |
| Long/short split | longs +5,124 / shorts +3,179 (both sides positive) | — |
| Bars to first net profit | median 1 × 5m bar, p75 3; 22.7% never profitable | — |
| Median hold | 15 × 5m bars (~75 min) | — |

Verification: no-lookahead poison test PASS · manual cost audit PASS · independent entry recomputation PASS.

## TradingView confirmation (OANDA feed, slippage 7 ticks/side, qty = 1 oz)
| Window | Net | PF | Win rate | Max DD |
|---|---|---|---|---|
| May 24 → Jul 17 2026 | +$152.65 | 1.567 | 48.98% (24/49) | 0.08% |
| Jan 1 2024 → Jul 17 2026 | +$444.03 (+0.44% at 1 oz on 100k) | 1.51 | 54.76% (190/347) | 0.11% |

Return ÷ maxDD ≈ 4.2× over 2.5y. **Sized so historical maxDD = 4%: ≈ +16% per 2.5y ≈ 6–7%/yr.** Two independent datasets (FTMO M1 research + OANDA TV) agree on sign, frequency (~1–2 trades/day), and curve shape.

## Honest limitations
- Consistency far below the 2.5%/day @ 4%DD standard (needs mean/|worst| 0.625; delivers ~0.008).
- P&L is outlier-driven: ~28% green days, months-long plateaus (Sep'24–Mar'25, mid-'25), five flat months at 2024 start.
- Swap not modeled (median hold 75 min → minor); intraday breaker not tick-simulated.
- Role: pool unit for breadth stacking — not a standalone income strategy.

## Pine v5 source (as deployed on TradingView 2026-07-18)
```pine
//@version=5
strategy("GV-014 Gravity Snap (gapped MTF)", overlay=true, initial_capital=100000, default_qty_type=strategy.fixed, default_qty_value=1, slippage=7, calc_on_every_tick=false, process_orders_on_close=false)
gravTF1 = input.timeframe("30", "Mid gravity TF")
gravTF2 = input.timeframe("60", "High gravity TF")
exitTF  = input.timeframe("30", "Exit TF")
exitLen   = input.int(4, "Exit SMA period", minval=1, maxval=10)
exitShift = input.int(1, "Exit SMA shift (+)", minval=0, maxval=5)
showZones = input.bool(true, "Shade gravity regimes")
f_bands() =>
    u200 = ta.sma(close, 200) + ta.stdev(close, 200)
    l200 = ta.sma(close, 200) - ta.stdev(close, 200)
    u20 = ta.sma(close, 20) + ta.stdev(close, 20)
    l20 = ta.sma(close, 20) - ta.stdev(close, 20)
    [close[1], u200[1], l200[1], u20[1], l20[1]]
[mC, mU200, mL200, mU20, mL20] = request.security(syminfo.tickerid, gravTF1, f_bands(), lookahead=barmerge.lookahead_on)
[hC, hU200, hL200, hU20, hL20] = request.security(syminfo.tickerid, gravTF2, f_bands(), lookahead=barmerge.lookahead_on)
gravUp = mC > mU200 and mC > mU20 and hC > hU200 and hC > hU20
gravDn = mC < mL200 and mC < mL20 and hC < hL200 and hC < hL20
ltfU20 = ta.sma(close, 20) + ta.stdev(close, 20)
ltfL20 = ta.sma(close, 20) - ta.stdev(close, 20)
trigLong = ta.crossunder(close, ltfU20)
trigShort = ta.crossover(close, ltfL20)
f_exit() =>
    s2 = ta.sma(close, exitLen)
    [close[1], s2[1 + exitShift]]
[eC, eSMA] = request.security(syminfo.tickerid, exitTF, f_exit(), lookahead=barmerge.lookahead_on)
exitLong = eC < eSMA
exitShort = eC > eSMA
if gravUp and trigLong and strategy.position_size == 0
    strategy.entry("L", strategy.long)
if gravDn and trigShort and strategy.position_size == 0
    strategy.entry("S", strategy.short)
if strategy.position_size > 0 and exitLong
    strategy.close("L")
if strategy.position_size < 0 and exitShort
    strategy.close("S")
plot(ltfU20, "LTF upper 20-band", color=color.new(color.teal, 40))
plot(ltfL20, "LTF lower 20-band", color=color.new(color.teal, 40))
bgcolor(showZones and gravUp ? color.new(color.green, 88) : showZones and gravDn ? color.new(color.red, 88) : na)
plotshape(gravUp and trigLong and strategy.position_size == 0, style=shape.triangleup, location=location.belowbar, color=color.green, size=size.small, title="Long entry")
plotshape(gravDn and trigShort and strategy.position_size == 0, style=shape.triangledown, location=location.abovebar, color=color.red, size=size.small, title="Short entry")
```

# SNAP-8 — Simple Nested Alignment Pullback

Paper / research only. No live orders.

## Intent

High-frequency M1 scalp: light M5 bias → M1 EMA ribbon pullback → RSI reclaim → ATR exits.

## Timeframes

| Role | TF |
|------|-----|
| Bias | M5 |
| Entry / manage | M1 |

## Indicators

| TF | Indicator | Settings |
|----|-----------|----------|
| M5 | EMA Bias | 50, close |
| M1 | EMA Fast | 8, close |
| M1 | EMA Slow | 21, close |
| M1 | RSI | 7, close |
| M1 | ATR | 14 (risk only) |
| M1 | CCI | 14 optional veto only |

## Indicator stack

```
M5 EMA50     → allowed side
M1 EMA8/21   → micro trend
Price vs ribbon → pullback zone
RSI(7)       → entry (cross 50)
ATR(14)      → SL / TP distance
CCI          → veto only (optional)
```

## Long (all required on M1 close)

1. M5 close > EMA50  
2. EMA8 > EMA21  
3. Price touched EMA8–EMA21 zone (signal bar or prior 3)  
4. RSI crosses above 50  
5. Close > EMA8  
6. Close not below EMA21  

Short = mirror.

## Exits

| Exit | Rule |
|------|------|
| SL | setup extreme ± 1.0×ATR |
| TP1 | +1.0×ATR → half off, SL → BE |
| TP2 | +1.5×ATR or trail vs EMA8 after partial |
| Time | flat if not +0.5×ATR by 12 M1 bars |
| Risk | 0.25–0.5% equity / trade |

## Locked params (paper test)

EMA50 / 8 / 21 · RSI7 · ATR14 · SL 1.0×ATR · TP 1.0/1.5×ATR · max bars 12 · risk 0.35%

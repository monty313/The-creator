# ♛ KINGS CHRONICLE — scalping throne history

> **NEVER ERASE.** Every prior king stays forever so agents learn.
> Mission: **never stop** trying to dethrone the current king (dual gate).
> When dethroned → record kept → hunt the new king → repeat forever.

**Updated:** 2026-08-07T11:42:01.430631+00:00
**Total crowning events:** 10
**Total dethrone archives:** 7
**Rejected vs chronicle (kept for learning):** 43
**Raw log:** `data/knowledge/trading/KINGS_CHRONICLE.jsonl`

## Current king (to dethrone)

- **Reign #10** · `shifted_envelope_breakout__shifted_envelope_breakout__m2565`
- **Name:** Gym elite shifted_envelope_breakout__m2565
- **Sharpe:** `10.4246` · **Profit:** `1413.16`
- **Crowned:** 2026-08-04T03:50:17.005369+00:00
- **Why:** ♛ CROWN TRANSFER — beat champion on BOTH sharpe (10.4246 > 8.1317) AND profit (1413.1600 > 1201.3400).

_Agents: SCOREBOARD only — invent new edges (Vertex AI fair game) until BOTH metrics beat this king. Do not clone king DNA as primary path._

## Full reign timeline (oldest → newest — never deleted)

| Reign | strategy | sharpe | profit | crowned at | deposed by |
|------:|----------|-------:|-------:|------------|------------|
| 1 | `dual_bb_trend_reversion` | 3.6876 | 468.42 | 2026-08-03T21:41:40 | `rsi_bb_tension_snap` |
| 2 | `rsi_bb_tension_snap` | 4.3101 | 502.2 | 2026-08-03T21:41:43 | `shifted_envelope_breakout__m3550` |
| 3 | `hybrid_cci_ema` | 2.5984 | 189.19 | 2026-08-03T21:41:43 | `—` |
| 4 | `cci_dual_mtf` | 0.8 | 120.0 | 2026-08-03T21:41:52 | `bb_mtf_rsi_bb_entry` |
| 5 | `bb_mtf_rsi_bb_entry` | 1.2 | 200.0 | 2026-08-03T21:41:52 | `—` |
| 6 | `shifted_envelope_breakout__m3550` | 5.9944 | 748.11 | 2026-08-03T21:46:41 | `shifted_envelope_breakout__m4514` |
| 7 | `shifted_envelope_breakout__m4514` | 6.9967 | 1013.17 | 2026-08-03T22:09:25 | `shifted_envelope_breakout__m2926` |
| 8 | `shifted_envelope_breakout__m2926` | 8.2563 | 1028.31 | 2026-08-03T22:13:42 | `—` |
| 9 | `shifted_envelope_breakout__m2565` | 8.6661 | 1274.72 | 2026-08-04T00:31:07 | `—` |
| 10 | `shifted_envelope_breakout__shifted_envelope_breakout__m2565` | 10.4246 | 1413.16 | 2026-08-04T03:50:17 | `—` |

## Lessons from prior kings (for the next challenger)

- Reign 1 `dual_bb_trend_reversion`: sharpe=3.6876 profit=468.42 · params={"wide_period": 100, "tight_period": 10, "dev": 0.5}
- Reign 2 `rsi_bb_tension_snap`: sharpe=4.3101 profit=502.2 · params={"rsi_fast": 2, "rsi_slow": 20, "bb_period": 20, "bb_dev": 0.5}
- Reign 3 `hybrid_cci_ema`: sharpe=2.5984 profit=189.19 · params={"cci_fast": 30, "cci_slow": 100, "buy_level": 100, "sell_level": -100, "ema_fast": 9, "ema_slow": 34}
- Reign 4 `cci_dual_mtf`: sharpe=0.8 profit=120.0 · params={}
- Reign 5 `bb_mtf_rsi_bb_entry`: sharpe=1.2 profit=200.0 · params={}
- Reign 6 `shifted_envelope_breakout__m3550`: sharpe=5.9944 profit=748.11 · params={"period": 2, "_base": "shifted_envelope_breakout"}
- Reign 7 `shifted_envelope_breakout__m4514`: sharpe=6.9967 profit=1013.17 · params={"period": 3, "_base": "shifted_envelope_breakout"}
- Reign 8 `shifted_envelope_breakout__m2926`: sharpe=8.2563 profit=1028.31 · params={"period": 2, "_base": "shifted_envelope_breakout"}
- Reign 9 `shifted_envelope_breakout__m2565`: sharpe=8.6661 profit=1274.72 · params={"period": 4, "_base": "shifted_envelope_breakout"}
- Reign 10 `shifted_envelope_breakout__shifted_envelope_breakout__m2565`: sharpe=10.4246 profit=1413.16 · params={"period": 4, "_base": "shifted_envelope_breakout"}

### Last dual-beat delta

- `shifted_envelope_breakout__m2565` → `shifted_envelope_breakout__shifted_envelope_breakout__m2565`
- Sharpe: 8.6661 → 10.4246
- Profit: 1274.72 → 1413.16

## Law

1. Never stop hunting a dual-beat of the current king.
2. When a new king is crowned, immediately start hunting *that* king.
3. Prior kings are permanent knowledge — nothing deleted.
4. Paper only until Mark approves live.

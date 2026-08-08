# Skill: Permanent 20% scalping benchmark

namespace: trading  
status: active  
success_count: 3  

## PERMANENT LAW

≥**20%** of Army effort always improves Mark’s scalping strategy benchmark only.  
Config: `config/agents/scalping_law.json`. Never park this pillar.

## Strategy 1 — Dual CCI MTF

1. Compute **CCI(30)** and **CCI(100)** on **M1**.
2. BUY only if both **> +100** on M1 **and** both **> +100** on **any other TF**.
3. SELL only if both **< −100** on M1 **and** both **< −100** on that other TF.
4. Log which other TF was used in every paper report.

## Strategy 2 — BB + RSI BB

1. Price **BB(100, deviation 0.5)** on **M5, M30, H1** — all must agree.
2. BUY context: close **above** upper BB on all three TFs.
3. BUY entry on **M5**: RSI **below** RSI-BB lower (BB period **10**, dev **1.0** on RSI series).
4. SELL: opposite (below lower BB on all three; RSI above RSI-BB upper).

## Always

- Paper / demo / backtest only until Mark approves live.
- **♛ Crown gate (Fable-style):** a strategy is crowned only if it **QC PASSes** and **beats BOTH** `sharpe_ratio` **and** `profit` vs current champion (strictly greater on each). One metric is not enough.
- Empty crown: first QC PASS with valid metrics takes ♛.
- Submit challenges via `challenge_for_crown(...)` → updates `CHAMPION__latest.md` / `.json` + `CANDIDATES__ledger.json`.
- Never place real MT5 orders from autonomy or chat.

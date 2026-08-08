# PERMANENT RULE — Scalping cadence (Law A13) — MUST

This rule is **always on**. **Monty overrules the Judge** on this point.

## THE LAW

- This bot is a **scalping bot**.  
- It **MUST take between 8 and 400 trades every day** (inclusive).  
- **Not “may.” Not optional capacity.** **Must.**  
- Outside that band = **A13 breach** (same seriousness as treating a soft path as production).  
- Lot sizes may vary under the risk envelope; daily risk **breach 0** and **no retrain** still absolute.

## Not production-legal

- A day path limited to ~**5 coarse decision slots** **cannot** satisfy min 8 → **non-compliant** as production path.  
- Judge may not soften this to “allowed if convenient” or PROMOTE a path that cannot hit **[8, 400]**.

## Court

**How** the bot hits 8–400 still needs measured A10 work.  
**That it must** is already law by owner order — not waiting on Judge preference.

Full: `evidence_court/SCALPING_CADENCE_LAW.md`  
Pin: `evidence_court/SCALPING_CADENCE_LAW.json`  
Test: `evidence_court/tests/test_scalping_cadence_law.py`  
Helper: `a13_trade_count_ok` / `assert_a13_trade_count`

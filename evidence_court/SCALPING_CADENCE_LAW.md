# SCALPING CADENCE LAW — PERMANENT (Monty order — Judge overruled)

**Status:** PERMANENT OWNER LAW — **hard mandate**  
**Law id:** **A13**  
**Promoted as permanent:** 2026-08-07  
**Human order:** Monty — **overrules the Judge** on this point  

> **THE LAW:** This is a **scalping bot**.  
> It **MUST take between 8 and 400 trades every day** (inclusive).  
> Not “may.” Not “capacity if convenient.” **Must.**

Machine pin: `SCALPING_CADENCE_LAW.json`  
Test pin: `tests/test_scalping_cadence_law.py`  
Auto-load: root `AGENTS.md` · `.grok/rules/00_scalping_cadence.md` · mission `GOAL.md`  
Compliance helper: `meta_rl.goal_path.a13_trade_count_ok` / `assert_a13_trade_count`

---

## Standing rule (non-negotiable)

| Constraint | Value | Meaning |
|------------|-------|---------|
| **Bot class** | **Scalper** | High-frequency day path |
| **Daily trades** | **MUST ∈ [8, 400]** | Fewer than 8 = **A13 breach**. More than 400 = **A13 breach**. |
| **Lots** | Variable under risk envelope | Creativity OK; daily risk **breach 0** still absolute |
| **5 coarse slots** | **Non-compliant path** | Cannot satisfy this law (max ~5 fires). Illegal as production day path. |

### Monty overrules the Judge

1. The Judge may not soft-label this as optional, aspirational, or “capacity only.”  
2. The Judge may not PROMOTE a production day path that **cannot** or **does not** land **8–400 trades/day**.  
3. The Judge may still run **labeled lab experiments** that fire fewer trades — but those results are **not** final-boss / production evidence and **do not** satisfy A13.  
4. Breach **0** (risk floor) and **no-retrain** remain absolute. A13 does **not** license blowing the risk floor to pad trade count with garbage size.  
5. **How** the bot reaches 8–400 (clock, multi-leg, multi-symbol, lot creativity) still needs **measured** Court work under A10 — but the **obligation** is already law by owner order, not deferred to a future PROMOTE.

### Hard implications

1. Day path **must be dense enough** to produce **at least 8** closed (or counted) trades per day under normal operation.  
2. Day path **must hard-cap** at **400** trades/day (no runaway thrash past the ceiling).  
3. Final-boss / promote_ready gates **must** include A13 compliance: `8 ≤ trades_today ≤ 400` (and breach 0, no retrain).  
4. Flea-jar: “impossible to clear” under a path that never reaches 8 trades is **incomplete** and **non-compliant** with A13.

### Forbidden

- Softening to “may fire up to 400.”  
- Production identity as few-trades swing.  
- PROMOTE of production law while day path structurally cannot hit ≥8 trades.  
- Using >400 trades as a loophole to ignore the ceiling.  
- Judge “rejecting” or “narrowing” the 8–400 **must** band without a later Monty-approved superceding law.

### Compliance function (machine)

```text
a13_trade_count_ok(n)  →  True iff 8 ≤ n ≤ 400
assert_a13_trade_count(n)  →  raises if outside band
```

---

## Immutable

Append-only permanent until a later Court PROMOTE **and** Monty approval supercedes the range.  
Silent weakening (“may” instead of “must”, dropping the floor, ignoring the ceiling) is a **Court defect**.  
**Owner overrule stands above Judge preference.**

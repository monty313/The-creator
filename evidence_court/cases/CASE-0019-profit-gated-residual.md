# CASE-0019 — Profit-gated + continuation-only residual (anti F-019)

**case_id:** CASE-0019  
**status:** PROMOTED (narrow dual-safe residual helpers) — dual scoreboard **not** claimed  
**opened:** 2026-08-07 (scheduled Court fire)  
**closed:** 2026-08-07  
**docket_issue_id:** ISSUE-ROAD / ISSUE-DUAL (on the road)  
**question:** What **measured** residual geometry raises A13 capacity **without** undoing conversion (F-019) — profit-gated and/or continuation-only — without pad, full-size thrash, gate-only, or exit-scratch?

**scope:** `goal_path.py` residual helpers + day-path wire  
**protected_invariants:** A10–A19; F-011…F-019; no pad; META_RL_DIM; PROVEN untouched  

**Orientation:** ROAD — residual only when labels stay learnable (profit + cont).

---

## ROUND STRUCTURE (Law A10 + A15)

```
Creator + Mark openings + NEW tests → counters → Counsel → Critic → Optimist → pretrial → units → IRAC
```

---

## Creator opening

### strongest_internet_argument

**Pyramiding / scale-in only when ahead** is standard risk practice: residual risk after a winner has free equity cushion; averaging into losers destroys expectancy. Position-sizing literature separates **core unit** from **add-on only with positive realized P&amp;L**. Dual objective (hit rate + trade density) fails when residual multi fires into red days (F-019).

**claim:** Residual micro requires `realized_pnl_percent > 0` after anchor.

**new_test:** `test_creator_new_profit_gate_blocks_residual_on_loss`

---

## Mark Here, Esq. — opening

### strongest_knowledge_argument

1. CASE-0012 conversion path = **pullback_resume → EOD hold**.  
2. Residual multi on that path dilutes R / scratches runners (F-019 class).  
3. Residual must be **continuation-only** (short-hold next-slot class), never micro-multi on pullback EOD.  
4. Anchor stays 1-symbol full; residual multi only when dual-safe.

**claim:** `continuation_only` gate protects pullback conversion road.

**new_test:** `test_mark_new_continuation_only_residual_protects_pullback_eod`

---

## Creator counter

**counter:** Multi-symbol residual only when profit after anchor (symbols=1 when red).

**newer_test:** `test_creator_new_multi_symbol_only_when_profit_after_anchor`

---

## Mark counter

**counter:** Ungated defaults must still pass CASE-0013 pins (API compatibility).

**newer_test:** `test_mark_new_ungated_defaults_preserve_case0013_pins`

---

## Counsel opinion (Law A15)

### internet_sift

- Scale-in / pyramid only after partial profit is common prop-desk rule.  
- Dual-objective control: do not optimize trade-count with negative-EV residual.  
- Anti-averaging-down is a hard road rail for learnable R.

### policy_recommendation

Wire day path with **profit_gate=True** and **continuation_only=True** on residual size; multi-symbol only when pnl>0. Unit-pin first; **forward100 next fire** for dual scoreboard (hits/low_hr/a13_frac). Do not claim dual PROMOTE without 100d.

### opinion

Creator + Mark both required; Counsel concurs hybrid gate. Weigh three opinions → narrow promote helpers; dual deferred.

### evidence

`tests/test_case0019_profit_residual.py` 4/4; goal_path wire.

### sources

- Risk: pyramid only when ahead (design class)  
- F-019 taxonomy; CASE-0012/0013 record  
- ROAD_FOR_THE_POLICY.md  

---

## Critic

| Check | Note |
|-------|------|
| Pad | scale 0 = skip, not pad fill |
| F-019 | gates address measured failure mode |
| Dual claim | units ≠ 100d dual win |
| A13 | may drop vs ungated residual — measure next |

---

## Optimist

Profit+cont residual keeps A13 path on green days only — cleaner labels for meta-policy.

---

## Judge pretrial

1. 4 NEW tests + CASE-0013 regression.  
2. Code: `residual_leg_allowed` + gated scale/symbols; day path profit_gate+continuation_only.  
3. **No forward100 this fire** (unit road pin; dual measure = CASE-0020).  
4. PROMOTE narrow if green; dual scoreboard ADMIT deferred.

---

## Results

`pytest test_case0019_profit_residual.py test_case0013_micro_residual.py` → **8/8 PASS**

| Test | Role | Result |
|------|------|--------|
| profit gate blocks on loss | Creator | **PASS** |
| continuation-only protects pb | Mark | **PASS** |
| multi only when profit | Creator counter | **PASS** |
| 0013 defaults preserved | Mark counter | **PASS** |

---

## Judge IRAC

- **Issue:** Dual-safe residual geometry after F-019?  
- **Rule:** A10+A15; ROAD; no pad/thrash; dual claim needs 100d.  
- **Application:** Units green; day path wired gated residual; 0013 pins intact; no 100d yet.  
- **Conclusion:**  
  1. **PROMOTE Law A20 (narrow)** — Residual micro/multi only when profit-gated **and** continuation-only on production day path.  
  2. **ADMIT** experimental dual path — scoreboard re-measure **CASE-0020** forward100 seed=42.  
  3. F-019 remedy updated.  
  4. Not final-boss promote_ready.

# CASE-0030 — Multi-set eases same-day session path confirm

**case_id:** CASE-0030  
**status:** OPEN  
**opened:** 2026-08-07  
**docket_issue_id:** ISSUE-ROAD / ISSUE-A13 / ISSUE-DUAL  
**question:** Does **easing same-day session min_align to 0 when multi-set HTF agrees** raise a13 day-share and/or hits ≥12 **without** undoing floor (prefer hits≥11 / low_hr≥0.28 / a13≥28%; absolute ≥9/0.24) and without F-011…F-022?

**scope:** `session_min_align_for_path` + day-path wire only; keep A27 5m, A26 hold, A21 1-sym  
**protected:** empty skip; no pad; no residual multi; no exit floors; PROVEN untouched  

**Baseline CASE-0029:** breach 0 | hits 11 | low_hr 0.28 | a13 28% | mean_tr 7.27 | max_pnl 70  

---

## ROUND STRUCTURE (A10 + A15)

Creator + Mark openings + NEW tests → counters → Counsel → Critic → Optimist → pretrial → units → measure → IRAC

---

## Creator opening

### strongest_internet_argument

Top-down MTF: **HTF bias is primary**; LTF times entry with the HTF. When multiple official sets already agree (Mark multi-set), requiring a separate same-day open→now lean (session_confirm) is a **redundant LTF filter** that can block real HTF-aligned edges on quiet/choppy opens — especially silent days (~41% zero-trade). Easing min_align to 0 **only when multi_set_agree** densifies real confluence edges without pad and without residual multi thrash.

**claim:** `session_min_align_for_path(multi_set_agree=True)==0`; non-multi keeps DEFAULT.

**new_test:** `test_creator_new_multiset_eases_session_min_align`

---

## Mark Here, Esq. — opening

### strongest_knowledge_argument

1. Multi-set HTF agree = Mark eyes permission — session lean is secondary.  
2. Without multi-set, keep DEFAULT_SESSION_MIN_ALIGN (anti-thrash).  
3. Early day (<min_bars) still flea-jar True.  
4. 1-sym; empty skip; conflict still blocked upstream.

**claim:** multi_set ease does not zero non-multi floor; session_confirms still works with min_align=0 as pure side sign.

**new_test:** `test_mark_new_non_multiset_session_floor_kept`

---

## Creator counter

**newer_test:** `test_creator_new_session_confirm_zero_align_still_side_aware`

---

## Mark counter

**newer_test:** `test_mark_new_a27_a26_geometry_preserved`

---

## Counsel opinion (A15)

### internet_sift

MTF guides: trade with HTF bias; LTF confirms entry in that direction — multi-set already is HTF. Session path lean is extra LTF noise filter; under multi-set it can starve silent days.

### policy_recommendation

Single lever: multi-set → session min_align 0; else DEFAULT. Unit-pin; forward100 seed=42 vs 0029 floor.

### opinion

Creator silent-day unlock + Mark non-multi discipline = dual-on-road. Prefer over 1m clock (cost) or residual multi.

### evidence

NEW tests; 0009/0029 regression; forward100.

### sources

MTF top-down confluence; CASE-0029 n_zero bottleneck; ROAD; F-017…F-022

---

## Critic

May add counter-path multi-set fires if same-day lean opposes — force floors still gate. Watch conversion floor.

---

## Optimist

Unlocks HTF-clear quiet days → a13 day-share + hits ≥12 path.

---

## Judge pretrial

1. NEW 4 + 0009/0029 regression green  
2. Code only session_min_align helper + day wire  
3. forward100 seed=42  
4. Floor prefer ≥11/0.28/a13≥28%; absolute ≥9/0.24; breach 0  

---

## Results

_(pending)_

---

## Judge IRAC

_(pending)_

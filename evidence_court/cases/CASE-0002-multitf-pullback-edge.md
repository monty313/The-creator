# CASE-0002 — Multi-TF pullback/continuation edge (hint)

**case_id:** CASE-0002  
**status:** PROMOTED  
**question:** How should the untested edge — wait for strong HTF trend, enter LTF pullbacks and continuations using RSI(5)+BB(10, dev=0.5, shift+2) on the set LTF — be implemented on official Mark sets, with multi-symbol concurrent risk and 1:100 leverage, without look-ahead or retrain?

**scope:** `evidence_court/meta_rl/{indicators,edge,leverage,price_io,forward_eval}.py`  
**protected_invariants:** MARK_SETS_LAW; Meta-RL 176 state; no-retrain; daily risk envelope; flea-jar full action space.

## Hint

`Possible edge not tested.txt`: waiting for strong trend and getting in on pullbacks and continuations; RSI 5 with applied BB 10 deviation .5 shift +2 on the lower timeframe of a set for timing.

## Creator submission

- **claim:** HTF force on confirmation TFs + LTF RSI5/BB timing implements the edge additively; scan all 4 sets; multi-symbol book aggregates risk at 1:100 risk-legal lots.
- **mechanism:** `scan_all_sets` → Channel1 confluence → senses/L2L → frozen policy size under envelope.
- **no_retrain_support:** edge is feature path; weights frozen.
- **falsifier:** look-ahead BB; single-set only; force_side oracle; breach; zero pullback/continuation coverage on multi-day trend data.

## Mark submission

- **claim:** LTF times, HTF permissions; missing pullbacks on confirmed force is coverage failure (flea-jar), not market refusal.
- **required_measurement:** multi-set scan + multi-symbol forward with pb/cont counters.

## Critic

- 1:100 leverage in lot math; aggregate multi-symbol risk; declared friction; no future bar in RSI/BB.

## Optimist

- Enter both pullback_resume and continuation when HTF agrees — coverage is the 2x path under same risk.

## Judge pretrial

- Pass: unit edge tests; leverage=100; forward100 multi-symbol breach=0; pb+cont coverage >0; promote gates.

## IRAC

- **Issue:** Untested multi-TF timing edge under flea-jar full action space.  
- **Rule:** PROMOTE only with **NEW Mark tests**, prior-only indicators, Mark sets, multi-symbol risk, 1:100, breach=0, pb+cont coverage.  
- **Application:** 37 pytest green (incl. Mark NEW suite); forward100 promote_ready; pb=18 cont=162; symbols XAU/EUR/GBP; lev=100; breach=0.  
- **ruling:** **PROMOTE**  
- **Transcript:** `COURT_TRANSCRIPT_0001_0002.md`  


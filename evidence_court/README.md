# Evidence Court — Meta-RL multi-TF multi-symbol bot

**Creator v. @mark_here** — only tests pass. Mark holds KAG; Creator ships after PROMOTE.

**PERMANENT Law A10:** Creator strongest **internet** + new test; Mark strongest **knowledge** + new test; **one counter each**.  
→ `ADVERSARIAL_ROUNDS_LAW.md` · pinned by `tests/test_adversarial_rounds_law.py` · auto-load `../AGENTS.md`

**Cycle:** Goal unmet → Judge ranks issues biggest→smallest → Court tries #1 → re-measure.  
→ `ISSUE_DOCKET.md` · `../docs/grok_cli_evidence_court_v2.md` §9

**Road:** Trained meta-policy (A14) needs a learnable path — not cliffs.  
→ `ROAD_FOR_THE_POLICY.md`

**PERMANENT Law A15:** **Counsel** sifts **internet** for best policy; Judge weighs **Creator + Mark + Counsel**.  
→ `COUNSEL_TO_THE_COURT_LAW.md` · `COUNSEL.md` · pin `tests/test_counsel_to_the_court_law.py`

**PERMANENT Law A28:** **Opportunity Watch** always on (miss PB/cont → complaints); senses cases **0031–0034**.  
→ `OPPORTUNITY_WATCH_LAW.md` · `SENSES_CASE_DOCKET.md` · pin `tests/test_opportunity_watch_law.py`

**PERMANENT Law A30:** Creator whole-project checklist → Court each item; then Mark + KAG checklist → Court each item.  
→ `schedules/SCHEDULE.md` · `CREATOR_GOAL_CHECKLIST.md` · pin `tests/test_full_project_checklist_law.py`


**PERMANENT Law A31:** Goal is north star of every Court action — `GOAL_LAW.md`  
**PERMANENT Law A32:** Emergent senses (sight/feel/taste/hearing) drive brain — `EMERGENT_SENSES_LAW.md`  
**PERMANENT Law A33:** Court keeps going, generates goal-relative issues, retains ledger — `GOAL_RELATIVE_COURT_LAW.md`  

**PERMANENT Law A14:** Meta-policy **must be trained** (permanent meta-learning — not optional “practice”).  
→ `META_POLICY_TRAIN_LAW.md` · `python -m evidence_court.meta_rl.cli meta-train`

**PERMANENT Law A13 (Monty overrules Judge):** Scalping bot **MUST** take **8–400 trades every day**.  
→ `SCALPING_CADENCE_LAW.md` · pin `tests/test_scalping_cadence_law.py` · `DEFAULT_SLOTS` (5) = **non-compliant** production path

## Quick commands

```bash
# From repo root
python -m pytest evidence_court/tests -q
python -m evidence_court.meta_rl.cli meta-train --steps 2500
python -m evidence_court.meta_rl.cli prove 15 2
python -m evidence_court.meta_rl.cli forward100 --days 100
```

## What is PROMOTED (measured)

| Law | Meaning |
|-----|---------|
| Meta-RL 176 | Mark-168 + goal/risk context [5,90]×[1,3], no retrain |
| Multi-TF edge | HTF force + LTF RSI5/BB10 shift+2 pullback & continuation |
| Flea-jar sim | 1:100 leverage, multi-symbol, risk-legal lots, envelope hard |
| 100-day gate | breach=0, L2L/senses day-path, goal hit rates recorded |

Transcript: `cases/COURT_TRANSCRIPT_0001_0002.md`

## Layout

- `ADVERSARIAL_ROUNDS.md` — Creator (internet + new test) vs Mark (knowledge + new test); **one counter each**
- `INVENTORY.md` · `MASTER_ARCHITECTURE.md` · `FAILURE_TAXONOMY.md` · `FLEA_JAR_COURT_LAW.md`
- `cases/` — CASE-0001, CASE-0002, CASE-FORWARD-100
- `meta_rl/` — state, edge, indicators, leverage, policy, forward_eval, cli
- `tests/` — including Mark **NEW** KAG tests for CASE-0002
- `artifacts/forward100_report.json` — promote artifact

**Full procedure:** `../docs/grok_cli_evidence_court_v2.md` · Mark: `../mark_here/ESQUIRE.md`

# CASE-FORWARD-100 — 100-forward-day matrix evaluation

**case_id:** CASE-FORWARD-100  
**status:** PROMOTED  
**question:** Does the frozen Meta-RL system complete 100 chronological forward days across the target×risk matrix with zero daily-risk breaches, no mid-eval retrain, goal-conditioned behavior, and L2L novel mapping?

**scope:** `evidence_court/meta_rl/forward_eval.py`, artifacts; read-only price CSVs.

**protected_invariants:** Same as CASE-0001; no fabricated fills labeled as live.

## Pretrial

- Metrics: n_days≥100 (or honest max available + warning), breach_count=0, no_retrain=true, multi-pair matrix present, l2l_novel_ok=true
- Label: `forward_sim_shadow` with declared friction
- Command: `python -m evidence_court.meta_rl.cli forward100 --days 100`

## Fill timing (no look-ahead)

- **Decision:** day open, features from completed prior days only.
- **Fill:** enter open → exit close, or stop if adverse excursion ≥ stop distance.
- **Forbidden:** same-day close/body as decision feature; `force_side` oracle.

## IRAC

- **Issue:** 100-day gate after skeptic repair.
- **Rule:** breach=0, no retrain, day-path L2L+senses, goal hit rates / consistency, state-driven acts, no look-ahead, n_days≥100.
- **Application:** 100 days on `XAUUSD_M1_full`; `force_side_used=false`; `no_lookahead=true`; L2L/senses wired every day; `total_hits=2` @ target 5% (hit_rate 0.111); max day PnL 14.2%; hit rates recorded for all 5–90 targets; 18 pairs; breach=0.
- **Conclusion / ruling:** **PROMOTE** (forward_sim_shadow only).
- **Artifact:** `evidence_court/artifacts/forward100_report.json`  
  SHA256: `df2b8647afc3abe612b5eb96bc8418a56ec8b772a6016c2a7d0abfb1c89d11ab`

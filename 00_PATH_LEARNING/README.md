# PATH LEARNING — learn the map, do not only copy answers

**Start here.** Top-level package on purpose.  
**Court case:** `evidence_court/cases/CASE-PATH-LEARNING.md`  
**Code:** `evidence_court/meta_rl/path_learning.py` · `train_path_learning.py`  
**Companion:** `00_PATH_STATE_TEACHERS/` (answer-anchor road) · `evidence_court/DETHRONE_THE_KING.md` (legal promote gates)

---

## What is this?

**Path-state teachers** taught the champion **density** by cloning Mark’s side on real wait states.  
That is a **road**, but it is still **answer-copying** on those moments.

**PATH LEARNING** is the next road: teach the policy to **generalize** under goal/risk, outcome, conversion, and senses — using path-state only as **sparse anchors**, not the whole diet.

---

## Read in order

| # | File | What you get |
|---|------|----------------|
| 1 | **`01_STEPS_1_TO_6.md`** | Steps **1–6** defined very well |
| 2 | **`02_IMPLEMENTATION_RULES.md`** | Rules to implement the path (Court + code) |
| 3 | **`03_PREDICTED_OUTCOMES.md`** | If rules applied for real learning → expected outcomes |
| 4 | **`04_COURT_AND_RUN.md`** | Ruling + how to run lab train/dual |

---

## One picture

```text
1. Outcome-shaped offline updates     (not act-match alone)
2. Goal/risk curriculum PRIMARY       (path-state = sparse anchors)
3. Holdout that BITES                 (novel T×R / window)
4. Conversion teachers                (clear progress, not fire-only)
5. Senses process + outcome → brain   (anti-washout: path re-anchor last)
6. Promote guard                      (no washout / pure clone without floor dual)
        │
        ▼
  Court A10+A15 → lab shadow only until PROMOTE + floor hold
```

---

## Rule (easy)

| DO | DO NOT |
|----|--------|
| Offline train, then freeze | Retrain at prove / live |
| Path-state as **anchors** | Path-clone as only diet for “learning” |
| Outcome + conversion reward | F-024 / F-025 densify |
| Holdout + floor dual before promote | Silent champion overwrite |
| Process light + re-anchor last | Process washout as production |

---

## Status

| Item | Value |
|------|--------|
| Production champion | Still CASE-0037 `meta4275` until lawful PROMOTE |
| Lab shadow (after Court ACCEPT*) | `evidence_court/artifacts/meta_policy_path_learning.npz` |
| Final boss / L2L §7 | **Not** claimed by this package alone |

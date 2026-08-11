# Path-state teachers (brain-wait)

**Start here.**  
This folder is at the **top of the project** on purpose.

---

## What is this?

This is the training process that taught our champion the **most**.

**Simple name:**  
“Save what the bot saw when it waited — and teach it the right trade later.”

**Full name:**  
Packed path-state teachers at brain-wait  
(Court case: **CASE-0037**)

---

## Read these files (in order)

| # | File | What you get |
|---|------|----------------|
| 1 | **`01_HOW_IT_WORKS.md`** | What the process is (plain words) |
| 2 | **`02_HOW_TO_USE_IT.md`** | How to run it yourself |
| 3 | **`03_IMPROVEMENTS_BEFORE_AFTER.md`** | CASE-0037 before/after (champion) |
| 4 | **`04_MONTY_BLEND_RETRAIN_RESULT.md`** | Lab: path-state + Monty HTF blend retrain |
| 5 | **`05_HTF_ACTIVE_YEAR.md`** | Year train: only HTF-active moments → dual → promote if beats |
| 6 | **`06_TRADE_MENTAL_REPLAY.md`** | Policy 3-TF × before/during/after self-observation (lab) |

---

## One picture (whole process)

```text
1. Bot plays a real day
2. Bot says WAIT on a good Mark setup
3. We SAVE what the bot saw (full state)
4. Teacher says: that should be LONG or SHORT
5. Offline practice (meta_update)
6. Freeze weights for real trading
7. Measure (forward100) before promote
```

---

## Why it matters

Bad training = fake states or copy answers.  
**This** training = real moments on the real path.

That is why A13 density jumped (more good trade days).  
Hits (target wins) stayed the same — still work to do.

---

## Where the code lives

| What | Path |
|------|------|
| Harvest + train code | `evidence_court/meta_rl/path_state_harvest.py` |
| Day path flag | `collect_path_state_teachers` in `goal_path.py` |
| Mental replay (3×3 mind) | `evidence_court/meta_rl/trade_mental_replay.py` |
| Day path mental flag | `collect_mental_replay` in `goal_path.py` (auto-on with path teachers) |
| Court case | `evidence_court/cases/CASE-0037-path-state-teachers.md` |
| Champion SSOT | `evidence_court/BEST_POLICY.md` |
| Teacher pack (saved) | `evidence_court/artifacts/teachers/path_state_teachers_case0037.json` |
| Current champ weights | `evidence_court/artifacts/meta_policy_champion.npz` |

---

## Rule (easy to remember)

| DO | DO NOT |
|----|--------|
| Train offline on real path states | Retrain during prove / live day |
| Teach Mark side on wait-misses | Force fake trades live |
| Measure before replace champion | Silently overwrite PROVEN weights |
| Prefer London / NY examples | Rebuild a fake “state” from labels only |

---

*Written for quick reading. Short lines. Simple words.*

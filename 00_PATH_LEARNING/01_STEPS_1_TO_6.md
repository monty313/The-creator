# Steps 1–6 — defined fully

Each step is **offline train only** unless noted. None may run as live hard rules that replace MetaBrain at inference.

---

## Step 1 — Outcome-shaped offline updates

### What it is
Do **not** only minimize “match teacher_act.” Scale the offline `meta_update` **reward** by an **outcome signal** attached to the example:

| Signal | Meaning | Effect on reward |
|--------|---------|------------------|
| `outcome_clear` | Day/slot moved toward target under risk | ↑ reward for that fire/wait label |
| `outcome_breach_near` | Loss near risk floor | ↓ fire reward; ↑ wait/size-down |
| `outcome_r_capture` | Realized R / partial lock quality | ↑ size teacher when good hold |
| `outcome_dead` | Fire with no progress | ↓ fire reward (conversion fail) |

### How to do it
1. Start from a packed path-state example **or** goal/risk synthetic state.  
2. Attach `outcome_score ∈ [−1, 1]` (see `path_learning.outcome_score_from_fields`).  
3. Call `meta_update(..., reward = base_reward * outcome_scale(outcome_score))`.  
4. Never invent live pad trades to create fake outcomes.

### Done when
Unit test: higher clear outcome → higher `reward` used than dead/breach outcome for same act; API is the shipped function, not a reimplementation.

---

## Step 2 — Goal/risk curriculum primary; path-state sparse anchors

### What it is
**Primary diet:** many offline episodes where **target% ∈ [5,90]** and **risk% ∈ [1,3]** vary; teacher from regime/senses process (not a single fixed pack of answers).  
**Sparse anchors:** path-state long/short teachers at **low mix fraction** (default ~0.15–0.25 of updates) so A13 density does not wash out.

### How to do it
1. Warmstart from CASE-0037 champion (legal road).  
2. Run goal/risk + density process curriculum for most steps.  
3. Interleave path-state only as anchors (`path_anchor_frac`).  
4. If process is used, **path re-anchor last** (anti-washout lesson from L2L residual).

### Done when
Curriculum report records `n_goal_risk`, `n_path_anchor`, `path_anchor_frac`; path is not 100% of updates.

---

## Step 3 — Holdout that bites

### What it is
Reserve episodes with **novel high targets** (and optional held-out seed band) for evaluation **or** lower-lr holdout train that must not be the only scoreboard. Promote path requires dual on days/protocol **not** only the harvest window used for teachers.

### How to do it
1. `holdout_frac` of process/goal episodes use `holdout_mode=True` (high targets 55–90).  
2. Record `hold_mean_loss` separately.  
3. Dual report must name protocol; floor dual = forward100-class **or** Court re-floor first (`DETHRONE_THE_KING.md` §4).

### Done when
Curriculum returns holdout stats; freeze pin: fingerprint stable across target/risk forward after freeze.

---

## Step 4 — Conversion teachers (not fire-only)

### What it is
Teachers that improve **hits / clear**, not only fire count:

| Teacher class | Act / size | When |
|---------------|------------|------|
| `fire_edge` | long/short, size medium | PB/cont + force, progress low |
| `hold_convert` | same side, size sustain | Progress mid, still under risk |
| `wait_load` | wait | Load / conflict / collapse |
| `wait_risk` | wait | Risk remaining low / near floor |
| `size_down` | same side, smaller size | High target, low risk remaining |

### How to do it
`conversion_teacher_from_context(progress, risk_rem, topology, force_side, outcome_score)` → `(act, size_frac, reason)`.  
Mix conversion examples into curriculum so CE is not “always fire on every path teacher.”

### Done when
Unit: load → wait; mid progress + force → hold/fire with size; low risk_rem → wait or size_down.

---

## Step 5 — Senses process + outcome into brain

### What it is
Sense pack already in state (L2L P1). Train with:
- **Process targets** from living senses (`l2l_process`, `density_mode` allowed light),  
- **Outcome scale** on process fire,  
- **Path re-anchor last** so process wait CE cannot starve A13.

### How to do it
1. Light density process (`process_steps` small relative to goal curriculum).  
2. Outcome-shaped reward on process fire episodes.  
3. Final path-state re-anchor passes.  
4. Freeze.

### Done when
Train report has `process_fire_frac`, `path_reanchor_last=true`, `weights_frozen=true`.

---

## Step 6 — Promote guard (no washout / pure clone without floor)

### What it is
Hard software + Court rule: **lab shadow only** until dual holds BEST_POLICY floor **or** Court re-floors; reject process-washout and “path-clone only” as production.

### How to do it
`path_learning_promote_guard(dual_lab, dual_champ, *, floor, path_only_clone, process_washout)` returns:

| Condition | promote lab? | production_replace? |
|-----------|--------------|---------------------|
| breach > 0 | no | no |
| a13 collapsed vs washout floor | no | no |
| path_only_clone and no outcome/conversion mix | no | no |
| process_washout (a13 hard floor fail) | no | no |
| beats champ same protocol + a13 hard floor | lab maybe | **no** without floor hold |
| holds BEST_POLICY floor metrics | lab yes | only if Court PROMOTE + BEST_POLICY update |

### Done when
Unit tests reject washout and clone-without-floor; dual report `production_replace=false` unless full gate.

---

## Order of execution (binding when Court ACCEPT*)

```text
Warmstart champion
  → Step 2 goal/risk primary (+ Step 4 conversion mix)
  → Step 1 outcome-shaped rewards on those updates
  → Step 5 light process + outcome
  → Step 2/5 path re-anchor last (sparse then final anchors)
  → Step 3 holdout segment
  → Freeze
  → Dual named protocol
  → Step 6 promote_guard
  → Production only if Court PROMOTE + floor (else lab shadow only)
```

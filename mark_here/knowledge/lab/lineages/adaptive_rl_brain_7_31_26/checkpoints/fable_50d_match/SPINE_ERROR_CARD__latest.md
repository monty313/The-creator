# SPINE / CONSTRAINT ERROR CARD — S1 decode + scale fix

**Phase:** S0 wired · S1 decode scored · **scale bug found** · S1b re-score next  
**Track:** T3 Mark soul / skill overlay (trunk frozen)  
**Child:** `CHILD_STAGE_same35_mark_clone_full_obs.pt` SHA `9BDCEAAE3B282DA1…`  
**Child weights touched:** **false**  
**Path:** `mark_aligned_decode` + skill_slice constraint overlay

---

## 50d scoreboard

### S0 wire-only (sensors packed, unused in decode)

| dials | same | clear | breach | mwt | KEEP |
|-------|-----:|------:|-------:|----:|:----:|
| pure_child / pinn / hq_cont / wait | 35 | 35 | 0 | 15 | Y |

### S1 decode (pressure_fire + survival_lock) — BEFORE scale fix

| dials | same | clear | breach | mwt | KEEP | note |
|-------|-----:|------:|-------:|----:|:----:|------|
| `constraint_pressure_fire` | 35 | 35 | 0 | 15 | Y | pressure_fire hits: **0** |
| `constraint_plus_hq_cont` | 35 | 35 | 0 | 15 | Y | pressure_fire hits: **0** |
| `constraint_pressure_plus_wait` | 35 | 35 | 0 | 15 | Y | pressure_fire hits: **1** |

| Meter | Value | Rule |
|-------|------:|------|
| **same** | 35 | floor held |
| **breach** | 0 | sacred |
| **target** | 36+ | **not met** |
| **MWT gap** | 15 | unchanged |

**Verdict:** `KEEP_FLOOR` — decode safe but **inert**.

---

## Doctor diagnosis (acknowledged)

| Blindness | Sensor (now wired idx) | Formula |
|-----------|------------------------|---------|
| goal_pressure | 18 `goal_pressure` | `(Target% − PnL%) / Target%` clamp [0,1] |
| survival_margin | 19 `survival_margin` | `floor_dist_pct / Risk%` = `(equity + risk) / risk` |
| regime_target_ratio | 20 `regime_target_ratio` | `(ATR14% × expected_swings) / Target%` |

`SKILL_SLICE_DIM = 21`. Child still reads `obs[:168]` only.

---

## Geometry path_class (pinn_gravity sample)

| class | counts |
|-------|-------:|
| wait_loaded | 292 |
| fire_window | 208 |
| wait_no_trade | 159 |
| continuation_fire_hq | **0** |

**Observation:** HQ cont never lights → cont_fill cannot climb same. Gap is **under-firing on MWT days** (hesitation / pressure-blind hold), not breach.

---

## Root cause (measured)

`regime_target_ratio = (ATR14_M1% × 2.5) / target` medians **~0.05**, while `REGIME_FUND_MIN=0.55`.

→ `fire_pressure_ok` almost never true → pressure_fire dead on the board.

**S1b fix:** `EXPECTED_SWINGS_DEFAULT = 40` (M1 path budget), `REGIME_FUND_MIN = 0.45`.

## Surgical next

Re-score `constraint_pressure_fire` after scale fix. If same < 35 or breach > 0 → REJECT. If same ≥ 36 breach 0 → PROMOTE skill dials only.

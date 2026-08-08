# Physics Repo Catalog — Super Agent KAG corpus

**Source of truth:** `physics.md` (ARMY root)  
**Mode:** ADDITIVE — never strip spine / L2L / mentors / child floor  
**Purpose:** Make Physics Super Agent fluent in the **engineering mechanics** of each repo and how they map to the-truth L2L.

---

## Master equation (from physics.md)

```
[High Tension + Low Entropy + Positive Mass Acceleration] → Launch
NOT [Pattern X] → Buy
```

Physics equations transfer across assets/timeframes; day memos do not.

---

## Pillar 1 — Physics-Informed Neural Networks (PINNs)

### Doctrine (physics.md)
- Embed **laws** in the **loss**, not only labels.
- **Gravity** = HTF Tide. Anti-tide BUY/SELL gets massive gradient penalty.
- Forces hidden layers to check HTF **before** LTF velocity → forward consistency.

### Lab map
| Piece | Path / lever |
|-------|----------------|
| CE + tide penalty | `train_mark_clone_bc.py` / L2L train loss |
| Existing force-gate | `mark_align` (KEEP; physics **adds** soft loss, does not replace) |
| Violation | `relu(pred_dir * -htf_tide) * λ` |

### Repos
| Repo | URL | Extract |
|------|-----|---------|
| **somsom786/options-pinn-solver** | https://github.com/somsom786/options-pinn-solver | PINN residual / PDE residual in loss; constraint terms alongside data loss |
| **AdityaBhatia-agentperry007/PhysicsNet-Trading** | https://github.com/AdityaBhatia-agentperry007/PhysicsNet-Trading | Fluid/physics constraints on trading pipeline; multi-term physics loss |

### Agent fluency notes
- PINN = `L = L_data + λ_physics * L_physics` (not pure supervised).
- `L_physics` can be soft inequality (relu violation) not only hard PDE residual.
- For our bot: `L_physics = tide_violation + optional thrash_violation`.
- **Falsifier:** if λ too large → over-HOLD → mwt may rise but same may drop; REJECT if same < 35.

---

## Pillar 2 — Kinematic Derivatives (Mass, Velocity, Acceleration)

### Doctrine (physics.md)
- HTF mass = slow MA (inertia); LTF = velocity.
- `v_mass = SMA[t] - SMA[t-1]`; `a_mass = v[t] - v[t-1]`.
- Aux head: student **predicts** `a_mass` so it feels momentum decay.
- Slingshot valid when LTF dips but HTF `a_mass` still positive (inertia intact).

### Lab map
| Piece | Path / lever |
|-------|----------------|
| Obs features | `perception/observation_full.py` — **add** v/a features |
| Aux head | `policy_stub` / PathL2L / SpineShadow — optional a_mass head |
| Classes | `wait_loaded` / `fire_window` ↔ tension timing |

### Repos
| Repo | URL | Extract |
|------|-----|---------|
| **konvsys/quantitative-kinematics-trading** | https://github.com/konvsys/quantitative-kinematics-trading | Price kinematics, zero-lag demodulation, velocity/acceleration of trend mass |
| **horustechltd/horus-flow-mcp** | https://github.com/horustechltd/horus-flow-mcp | Orderflow / microstructure “physics” for agents; relational flow features |
| **stockist/s_optimize_stocks** | (cited in physics.md concept) | MA velocity/acceleration for tension mapping |

### Agent fluency notes
- Absolute price is not a state; **derivatives** carry transferable dynamics.
- Aux multi-task: act CE + class CE + MSE(a_mass) improves representation for slingshot_load.
- Aligns with path class `wait_loaded` (hold while tension builds) vs `anti_thrash` (fire without tension).

---

## Pillar 3 — Dimensionless / Relational Tensors

### Doctrine (physics.md)
- Normalize by ATR (or vol):
  - `Tunnel_Distance = (Close - SMA_slow) / ATR`
  - `Velocity_Mass_Gap = (SMA_fast - SMA_slow) / ATR`
- Same geometry on XAU M1 and EURUSD H1 → no price-level overfitting.

### Lab map
| Piece | Path / lever |
|-------|----------------|
| MARK_FULL_DIM | Keep existing dims; **append** dimensionless channels if needed |
| Scaling | Never feed raw $ levels as primary drivers |
| Forward | Protects when gold is at different absolute levels |

### Repos
| Repo | URL | Extract |
|------|-----|---------|
| **microsoft/qlib** | https://github.com/microsoft/qlib | Gold standard: alpha factors as relational / normalized tensors; dataset pipelines for RL |
| **horustechltd/horus-flow-mcp** | https://github.com/horustechltd/horus-flow-mcp | Dimensionless ratios for institutional agents |

### Agent fluency notes
- Qlib-style: feature engineering is part of physics (scale invariance).
- Distribution shift on absolute price is a **physics bug**, not only a data bug.
- SkillOpt (below) rewrites laws in text; qlib rewrites the **tensor geometry**.

---

## Pillar 4 — Non-Equilibrium Thermodynamics (Entropy Regime Gating)

### Doctrine (physics.md)
- High entropy (ApEn / Shannon of last N returns) = chaotic / undefined.
- Physically mask BUY/SELL → only HOLD (`wait_no_trade`).
- Bot does **not** learn thrash by losing; boundary is hard.

### Lab map
| Piece | Path / lever |
|-------|----------------|
| Decode mask | DayRunner / mark_aligned_decode / force-gate path |
| Class | `anti_thrash` + high entropy → same physical idea |
| Existing | `m=0` regime / pt5 chop — physics **adds** numeric entropy |

### Repos
| Repo | URL | Extract |
|------|-----|---------|
| **ElvianElvy/fluctuation-theorem-perps** | https://github.com/ElvianElvy/fluctuation-theorem-perps | Fluctuation theorems, non-eq thermo, regime physics for perps |
| **0x596173736972/MarketRegimeTrader** | https://github.com/0x596173736972/MarketRegimeTrader | HMM regimes; swap playbook or halt when regime bad |

### Agent fluency notes
- Entropy gate = hard physical constraint on action space (like PINN but at **decode** time).
- HMM = soft regime classifier; can **add** labels without removing pt5 m=0.
- Falsifier: over-mask → miss fire_window → REJECT if same drops.

---

## Pillar 5 — Meta engines & multi-agent (context)

| Repo | URL | Extract for ARMY |
|------|-----|------------------|
| **microsoft/SkillOpt** | https://github.com/microsoft/SkillOpt | Optimize **text laws** / skills rather than only RL weights — matches KAG rewrite of markdown rules |
| **HKUDS/Vibe-Trading** | https://github.com/HKUDS/Vibe-Trading | Multi-agent tutors + backtest workspace — mirrors ARMY mentors |
| **paperswithbacktest/awesome-systematic-trading** | https://github.com/paperswithbacktest/awesome-systematic-trading | Master list; slingshot / momentum topology references; already cloned under external/ |

---

## Slingshot topology (physics + awesome list)

```
HTF mass inertia intact (a_mass ≥ 0 or tide aligned)
  + LTF velocity pulls against fast MA (load)
  + Low entropy (not chop)
  + Force-permission / mark_align
→ Launch (fire_window)
Else → wait_loaded / HOLD
```

Maps to path classes:
- `wait_loaded` — load phase  
- `fire_window` — launch  
- `anti_thrash` — fire without physics  
- `miss_fire` — physics ready, policy held  
- `hold_on_spine` — in-trade path  

---

## Binding with L2L rules (R1–R10)

| Physics add | Rule |
|-------------|------|
| Any λ_physics / mask | R1 floor same≥35 breach=0 |
| PINN / aux heads | R2 learn≠copy (structure > act-only) |
| Dimensionless + classes | R3 class≠memo |
| Features on policy path | R4 DAgger |
| Loss add with freeze_trunk | R5 surgical |
| Entropy mask | R6 award protect still on |
| KEEP only if pack holds | R7 |
| Memory of thrash vs entropy | R8 |
| Never train on holdout | R9 |
| One primary physics lever / cycle | R10 |

---

## Priority order for implementer (additive)

1. **PINN tide penalty** in train loss (soft gravity)  
2. **Entropy mask** at decode (anti-thrash physical boundary)  
3. **v/a kinematic features** (+ optional aux head)  
4. **ATR dimensionless channels** (geometry)  
5. Later: HMM regime playbook swap (MarketRegimeTrader style)  

Never remove: spine heads, L2L classes, mentors, child embryo, mark_align, KEEP/REJECT.

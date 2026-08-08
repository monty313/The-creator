# Doctor KAG reply — S0 scoreboard

ts: `2026-08-07T (local KAG failover)`  
channel: **local KAG Architect (Executor stand-in)**  
reason: Perplexity `PERP_KEY` → `insufficient_quota`; OpenAI `OPENAI_KEY` → credits exhausted  
status: **GO** (no PAUSE — scoreboard MRI is enough)

---

### 1. Diagnosis one-liner

Sensors are on the board but unused; policy under-fires on MWT (15) while HQ cont never lights — need **pressure-aware fire_window fill** behind a **survival lock**, not trunk training.

### 2. Logical forms (boolean)

```
survival_ok_open  := survival_margin ≥ 0.55
survival_hard     := survival_margin < 0.40
goal_hunt         := goal_pressure ≥ 0.50
goal_banked_near  := goal_pressure ≤ 0.12
regime_fundable   := regime_target_ratio ≥ 0.55
regime_starved    := regime_target_ratio < 0.35
permission        := mass_alive ∧ side ≠ 0
ltf_with          := ltf_side == permission_side
fire_pressure_ok  :=
    permission ∧ ltf_with
  ∧ path_class ∈ {fire_window, continuation_fire_hq, continuation_fire_med}
  ∧ goal_hunt ∧ survival_ok_open ∧ regime_fundable
  ∧ entropy_chop < 0.65
  ∧ ¬regime_starved

# breach walls
no_new_risk       := survival_hard ∨ (goal_banked_near ∧ ¬in_trade)

# surgical fills (only when base HOLD)
pressure_fire     := ¬in_trade ∧ fire_pressure_ok ∧ base_act == HOLD
```

### 3. Threshold table

| symbol | value | role |
|--------|------:|------|
| `SURVIVAL_OPEN_MIN` | 0.55 | min margin to open / force-fill |
| `SURVIVAL_HARD_MIN` | 0.40 | hard HOLD new risk |
| `GOAL_HUNT_MIN` | 0.50 | still need ≥ half target |
| `GOAL_BANK_MAX` | 0.12 | near clear — no re-open |
| `REGIME_FUND_MIN` | 0.55 | day range can fund hunt |
| `REGIME_STARVE_MAX` | 0.35 | no force-fill on starved regime |
| `ENTROPY_MAX` | 0.65 | same as HQ law |

### 4. apply_geometry_decode order

1. entropy_hold (existing)  
2. pinn_against_htf (existing)  
3. **constraint survival/bank no_new_risk** → HOLD if base is open  
4. thrash_gate (existing)  
5. in-trade pullback/collapse (existing)  
6. cont_fill HQ-only (existing)  
7. **pressure_fire** fill on fire_window (+ HQ/med if fundable) when base HOLD  

### 5. Pseudocode

```python
if constraint_gate and not in_trade and act in (BUY, SELL):
    if sk.survival_margin < 0.40 or sk.goal_pressure <= 0.12:
        return HOLD, "constraint_no_new_risk"

# ... existing thrash / cont hq ...

if pressure_fire_gate and act == HOLD and not in_trade:
    if fire_pressure_ok(sk):
        return (BUY if side>0 else SELL), "constraint_pressure_fire"
```

### 6. Risk: how breach stays 0

- Opens blocked when `survival_margin < 0.40` (stricter than mark danger ~0.45).  
- Force-fill only when `survival_margin ≥ 0.55` and `regime_fundable`.  
- Never open against HTF (pinn still first).  
- KEEP reject if breach > 0 after score.

### 7. PAUSE or GO

**GO** — implement overlay dials; score 50d; if same < 35 or breach > 0 → REJECT restore pure child / pinn_gravity KEEP floor.

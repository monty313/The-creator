# PKG-005 — Meta-RL policy: method first, goal second

**Teacher:** Aaron (`@Aaron_here`)  
**Code:** `Aaron_here/tools/top5_shape_observe.py`  
**Not Court law.**

---

## 1. Priority law (non-negotiable)

```text
1) METHOD path     Force → Load → Reclaim → rails
2) GOAL context    target / risk / scaled PnL
3) Never           win-rate alone as the objective
```

| Layer | In reward | In state |
|-------|-----------|----------|
| **Method** | **First** (large +/−) | Per-strategy F/L/R + consensus |
| **Goal** | **Second** (small; blocked if method broken) | `goal_target`, `risk_budget`, `position` |
| Win-rate | Log only — **not** a reward term | — |

```text
if method broken this step (mud fire / dip-chase / anti-force):
    goal_progress candy = 0     # method first
```

---

## 2. What the meta-policy **sees** (each of top 5)

For every bar, each composite is visible:

| Component id | Strategy geometry | Eyes |
|--------------|-------------------|------|
| `cci_gravity` | CCI M-line reclaim | CCI→M HTF+LTF |
| `mcflurry` | RSI M-line eddy | RSI→M HTF+LTF |
| `sma_scalp` | SMA ribbon | SMA8/21/50 + HTF SMA100 |
| `bb_mtf` | BB mass + RSI | BB20 + HTF BB mid |
| `guide_s01_ma_cross` | 50/200 | SMA50/200 dual HTF |

### Per component (8 fields × 5)

```text
{id}__force_sign       # -1 / 0 / +1   permission from THAT geometry
{id}__force_strength   # 0..1
{id}__load_flag        # pullback / eddy under its force
{id}__load_depth
{id}__reclaim_flag     # fire timing for THAT geometry
{id}__path_stage       # 0 mud | 1 force | 2 load-wait | 3 reclaim
{id}__bars_in_load
{id}__bars_since_reclaim
```

### Consensus method path (meta)

```text
force_sign, force_strength, load_flag, load_depth, reclaim_flag
path_stage
n_components_force_agree, n_components_load, n_components_reclaim
votes_long, votes_short
```

### Goal / position context (second)

```text
position, bars_in_trade
goal_target, risk_budget
session_ok, structure_ok
```

**Reasoning:** the bot can ask:

- “What does **cci_gravity** say for Force / Load / Reclaim?”  
- “What does **mcflurry** say?”  
- “Do they **agree** enough for consensus fire?”  
- “Given **goal/risk**, still only fire if method path is clean.”

---

## 3. How each component maps to the method path

Same card for all five (roles only; eyes differ):

```text
path_stage 0  force=0           → WAIT (mud)
path_stage 1  force≠0, no load  → WAIT / hold thesis
path_stage 2  load, no reclaim  → WAIT (do not dip-chase)
path_stage 3  reclaim + rails   → FIRE with that component's force side
```

```text
         cci_gravity     mcflurry      sma_scalp     bb_mtf      guide_s01
Force    dual M_cci      dual M_rsi    dual SMA100   dual BB mid dual 50/200
Load     M_ltf wrong0    M eddy        tag SMA21     band stretch tag SMA50
Reclaim  M cross 0       M cross 0     8/21 cross    mid cross    50/200 or bounce
```

Consensus force needs **≥2 components** same side (see code).

---

## 4. Rewards and penalties (method first)

From `METHOD_FIRST_REWARD` in code:

### Method (dominant)

| Event | Sign | Meaning |
|-------|------|---------|
| WAIT when consensus force=0 | + | no thrash in mud |
| WAIT during load, no reclaim | + | patience on method path |
| FIRE on valid reclaim + rails | ++ | correct commit |
| FIRE when force=0 | −− | thrash |
| FIRE on load bottom (dip-chase) | −− | load ≠ fire |
| FIRE against force | −− | anti-tide |
| FIRE reclaim wrong side | − | |
| FIRE rails off | − | session/structure/risk |
| Action matches a component’s preferred fire | + small | multi-composite alignment |
| Fire with almost no component force agree | − small | conflict |

### Goal (secondary only)

| Event | Sign | Gate |
|-------|------|------|
| Scaled PnL | +/− small | always small weight |
| Goal progress | + small | **zero if method broken this step** |
| Risk blown | − | always |

**There is no win-rate term.**

```text
total = method_reward + goal_reward
method_reward  >>  |goal_reward|   by design of weights
```

**Shipped composer (Court lab):**  
`evidence_court.meta_rl.path_learning.compose_method_goal_reward`  
— used by Aaron FLR curriculum and by `apply_outcome_shaped_update(..., method_ok=False)`.

---

## 5. Meta-learning use

1. **State** = pack all `*_force/load/reclaim` + consensus + goal/risk (`pack_state_vector`).  
2. **Action** = WAIT / FIRE_LONG / FIRE_SHORT / EXIT.  
3. **Reward** = `shape_reward(...)` → use `total` (or train with separate method/goal heads).  
4. **Teacher / mask** = `preferred_action(state)` follows consensus method path.  
5. **Transfer** = same method path when sensors rename; components are roles with different eyes.  
6. **Stress** = evaluate with MC / hard days — do not put WR into the reward.

```text
observe each composite → reason F/L/R per composite
        →
consensus method path
        →
action
        →
reward: method first, goal second
```

---

## 6. API

```python
from Aaron_here.tools.top5_shape_observe import (
    observe_shapes,
    shape_reward,
    preferred_action,
    preferred_action_component,
    pack_state_vector,
    COMPONENTS,
    METHOD_FIRST_REWARD,
)

state = observe_shapes(sb, position=0, goal_target=0.02, risk_budget=0.01)
x = pack_state_vector(state)          # meta-policy input
a = preferred_action(state)           # method teacher
r = shape_reward(state, action, pnl_scaled=0.0, goal_progress=0.0)
# r["method_reward"], r["goal_reward"], r["total"]
```

---

## 7. One-line memory

> **See all five. Reason each as Force → Load → Reclaim. Act on method path. Goal and PnL only after the method is clean — never win-rate alone.**

# Aaron Learning Method (ALM) — RL trading bot

**Author:** Aaron (`@Aaron_here`)  
**Purpose:** How an RL trading student should **learn**, and how we **score** strategy fuel.  
**Not Court law. Not a deploy order by vanity win-rate.**

For any LLM with no prior knowledge: terms are defined as they appear.

---

## 1. Mission of the student bot

The bot must learn a **thinking pattern** that still works when:

- sensors are renamed,  
- target % / risk % change in the **state** (no weight retrain for that alone),  
- the day is new.

Success = good **process** on unseen bars.  
Failure = memorizing one strategy filename or maxing lab win-rate only.

---

## 2. The method (how the bot thinks)

### 2.1 Three shapes (always)

| Shape | Question | If missing |
|-------|----------|------------|
| **Force** | Do **two higher times** agree on a side? | Prefer **WAIT** |
| **Load** | Did the **fast** chart pull back **against** that side? | **WAIT** (do not fire) |
| **Reclaim** | Did the fast chart come **back with** the side? | Preferred **FIRE** |

```text
FORCE? --no--> WAIT
  yes
LOAD? --no--> WAIT
  yes
RECLAIM? --no--> WAIT
  yes
FIRE with force side
```

**Hard rule:** higher time = side. Lower time = when. Lower never rewrites side.

### 2.2 Four layers (never mix them)

| Layer | Meaning |
|-------|---------|
| **Permission** | Force (dual HTF) |
| **Timing** | Load then Reclaim |
| **Objective** | What exits optimize (hit-rate vs expectancy) — choose on purpose |
| **Honesty** | Monte Carlo / path quality — lie detector |

### 2.3 State the policy sees (minimum)

```text
force_sign, force_strength
load_flag, load_depth, bars_since_load
reclaim_flag, bars_since_reclaim
position, bars_in_trade
goal_target, risk_budget   # context rails
```

Sensors (RSI, M, BB, …) only feed a **shape builder**.  
Train roles, not indicator names.

### 2.4 Actions (start simple)

`WAIT` | `FIRE_LONG` | `FIRE_SHORT` | `EXIT`

Mask / punish: fire with force=0, fire against force, fire on load bottom (no reclaim).

### 2.5 Reward (method first, goal second)

```text
METHOD (first, large):
  + WAIT when force==0
  + WAIT during load without reclaim
  + FIRE on valid reclaim under force + rails
  - FIRE force==0 / against force / dip-chase
  + align with component F/L/R when multi-sensor

GOAL (second, small):
  + scaled PnL / goal progress
  - risk blown
  BUT: if method broken this step → goal progress candy = 0
```

**Never** train on win-rate alone.  
**Meta state:** each top-5 geometry is a visible component (`PKG-005`, `tools/top5_shape_observe.py`).

### 2.6 Curriculum stages

```text
1 Force → 2 Load → 3 Reclaim fire → 4 Rails → 5 Stress (shuffle / hard days)
```

Do not start at stage 3.  
Labeled windows: see `packages/PKG-001_strategies_stage1_3_labeled_windows.md`.

---

## 3. How ALM **tests** strategies in `strategies/`

Each strategy family is **not** ranked by name or raw WR.

### 3.1 Lab contract (same for all)

- 2 HTF + 1 LTF, 4 official sets, pullback + continuation  
- EURUSD M1 lab window (see report meta)  
- Accuracy shell + first-breath style exits for the trade bag used in MC  
- Results already measured in `strategies/MONTE_CARLO_RESULTS.json` + accuracy JSON  

ALM **re-scores every family** with the formula below (no silent favorites).

### 3.2 ALM score (what “good fuel” means)

We want fuel that is:

1. **Path-honest** — bootstrap Monte Carlo median terminal wealth high  
2. **Low ruin lottery** — low P(loss) under MC  
3. **Positive mean trade** — average trade return &gt; 0 when possible  
4. **Controlled damage** — not huge hist max DD  
5. **Enough samples** — not 3 lucky trades; not pure thrash spam  
6. **WR only soft** — accuracy WR can help a little, never dominate  
7. **Geometry class** — profiles that encode F→L→R get a small bonus; thrash/black-box proxy get a penalty  

Exact weights live in `tools/score_strategies_alm.py` and are printed in the top-10 report.

### 3.3 What ALM will **not** do

- Call top-10 “live bots” or Court PROMOTE  
- Rank by win-rate gate alone  
- Treat 12 version names with the same profile as 12 different edges  

---

## 4. Top-10 meaning under ALM

**Top 10 = best teaching / path-quality fuel under ALM scores on this lab window.**  
Still:

- one symbol / one window,  
- fixed barriers,  
- not production law.

Use them as **positive shape pointers** and study objects.  
Use bottom ranks as **counter-examples** (thrash, vanity WR).

---

## 5. Double-loop

```text
Score all strategies under ALM
        →
Mine top as positive windows / bottom as negatives
        →
Train student stages 1–3
        →
Critique shape fidelity + MC honesty
        →
Rewrite package / rewards
```

---

**Think in shapes. Score with honesty. Curriculum on labeled windows. No name worship.**

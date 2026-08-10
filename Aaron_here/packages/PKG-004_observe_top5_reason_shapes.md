# PKG-004 — Observe top-5 indicators, reason in shapes

**Teacher:** Aaron (`@Aaron_here`)  
**For:** RL student / any LLM with no prior knowledge  
**Not Court law. Not “copy these 5 EAs.”**

**Rule:**  
**Reward shape first. Never win-rate alone.**  
**State = shapes + position + goal/risk context.**  
Indicators are only **eyes**. Reasoning is Force → Load → Reclaim → rails → stress.

---

## 0. One idea first

The top 5 ALM geometries do **not** give you five different brains.  
They give you **five ways to look at the same questions**:

```text
1. FORCE   — Is the higher-time tide one way? (both HTFs)
2. LOAD    — Did the fast chart pull against that tide?
3. RECLAIM — Did the fast chart come back with the tide?
4. RAILS   — Session / structure / risk OK?
5. STRESS  — Still honest under shuffle / hard paths? (eval, not every bar)
```

```text
  INDICATORS (from top 5)
           |
           v
     SHAPE BUILDER
           |
           v
   force_sign, load_flag, reclaim_flag, ...
   position, goal_target, risk_budget
           |
           v
        POLICY
     (reason + act)
```

**Wrong:** “RSI &lt; 30 → buy because strategy 3 said so.”  
**Right:** “RSI (or M, or BB) shows **load** under **force**; I wait for **reclaim**.”

---

## 1. The top 5 (what you may observe)

| # | Family (label only) | Profile | Main eyes (indicators) |
|--:|---------------------|---------|-------------------------|
| 1 | CCI gravity cluster | `cci_gravity` | CCI(20) → smooth → **M = SMA7−SMA21** on CCI |
| 2 | FTMO SMA Scalper | `sma_scalp` | SMA 8/21/50 ribbon + RSI(14); HTF SMA100 mass |
| 3 | McFlurry Eddy | `mcflurry` | RSI(13) → smooth → **M = SMA7−SMA21** on RSI |
| 4 | FTMO BB MTF | `bb_mtf` | Bollinger(20,2) on price + RSI(14); HTF BB mass |
| 5 | Guide MA cross | `guide_s01_ma_cross` | SMA50 / SMA200 cross + slope; dual HTF same idea |

You may **observe all of these at once** (multi-sensor state).  
You still answer the **same three shape questions**.

---

## 2. Shared reasoning card (use every bar)

```text
                    OBSERVE sensors
                           |
                           v
              +------------------------+
              | FORCE from dual HTF?   |
              +-----------+------------+
                          |
             no           |          yes
              v           |           v
           WAIT      strength?    LOAD against force on LTF?
                          |           |
                          v           +-- no --> WAIT
                     too weak --> WAIT|
                                      yes
                                      v
                              RECLAIM with force?
                                 /          \
                               no            yes
                               v              v
                             WAIT      FIRE with force side
                                      (if rails OK)
```

**Rails (stage 4):** session hours, micro structure, risk budget not blown.  
**Stress (stage 5):** judge the **policy** with Monte Carlo / hard days — do not optimize bar reward for win-rate only.

---

## 3. How each top-5 maps sensors → roles

### 3.1 `cci_gravity` — CCI momentum line

| Role | How to read the eyes |
|------|----------------------|
| **Force long** | HTF1 **and** HTF2: M_cci &gt; 0, and HTF1 \|M\| ≥ thr (lab thr≈8) |
| **Force short** | both M_cci &lt; 0, HTF1 \|M\| ≥ thr |
| **Force none** | disagree or weak |
| **Load long** | under force long: LTF M was **below 0** recently (eddy) |
| **Load short** | under force short: LTF M was **above 0** recently |
| **Reclaim long** | after load: LTF M **crosses up through 0** |
| **Reclaim short** | after load: LTF M **crosses down through 0** |

**Reasoning:**  
Do not fire when M first goes negative (that is load).  
Fire when it **comes back** through 0 with HTF still in force.

```text
HTF M ++ strong     LTF M dips < 0      LTF M cross up 0
    FORCE               LOAD                  RECLAIM → fire long
```

---

### 3.2 `mcflurry` — RSI momentum line (same physics, different sensor)

| Role | How to read |
|------|-------------|
| **Force** | Dual HTF **M_rsi** same sign; HTF1 \|M\| ≥ thr (lab thr≈1.5) |
| **Load** | LTF M crosses **into** the wrong side of 0 (eddy start) |
| **Reclaim** | LTF M crosses **back** through 0 with force |

**Reasoning:**  
Same card as CCI gravity.  
RSI-M and CCI-M are two **coordinates** of one idea: dual-HTF tide + LTF eddy + reclaim.

**Student lesson:** if RSI-M and CCI-M **disagree on force**, treat force as weaker or 0 — do not invent side from LTF alone.

---

### 3.3 `sma_scalp` — ribbon + RSI

| Role | How to read |
|------|-------------|
| **Force** | Dual HTF price vs SMA(100) mass (lab); ribbon 8&gt;21&gt;50 = LTF trend texture |
| **Load** | Ribbon still aligned, price **tags** mid SMA (21) against the fan, RSI not extreme the wrong way |
| **Reclaim / cont** | Fast SMA **crosses** back with ribbon (8 cross 21 while fan OK) |

**Reasoning:**  
Ribbon stack ≈ “local force texture.”  
Touch mid without cross ≈ load (wait).  
Cross with stack ≈ timing fire **only if** dual HTF force agrees.

**Wrong:** fire every 8/21 cross in mud (no HTF force).

---

### 3.4 `bb_mtf` — Bollinger + RSI

| Role | How to read |
|------|-------------|
| **Force** | Dual HTF BB mass (price vs mid band on both HTFs) |
| **Load** | LTF price outside / into outer band **against** force + RSI stretched (e.g. long force but RSI low / price at lower band) |
| **Reclaim** | Price **crosses back** through mid (or releases) **with** force; RSI not fighting |

**Reasoning:**  
Outer band touch alone is **not** fire.  
That is often load or mean-rev trap.  
Reclaim = return through mid **with** HTF mass.

**Wrong:** “price under lower BB → always long” (no force check).

---

### 3.5 `guide_s01_ma_cross` — 50/200 style

| Role | How to read |
|------|-------------|
| **Force** | Dual HTF: SMA50 vs SMA200 same side + slope |
| **Load** | Under force long: pullback toward fast MA (price tags 50 while tide still up) |
| **Reclaim / cont** | 50 crosses 200 with slope (classic golden/death) **or** bounce reclaim off 50 with force |

**Reasoning:**  
Golden cross on LTF with flat/disagreeing HTFs → **no force** → wait.  
Cross with dual HTF agreement → timing candidate.

---

## 4. Multi-sensor observation (how the bot “sees all five”)

You do **not** pick one strategy and ignore the rest.  
You build a **sensor bank**, then a **shape builder**.

### 4.1 Observe (examples of raw features)

```text
# From cci_gravity / mcflurry family
M_cci_htf1, M_cci_htf2, M_cci_ltf
M_rsi_htf1, M_rsi_htf2, M_rsi_ltf

# From sma_scalp
sma8, sma21, sma50, sma100_htf*, rsi14
ribbon_up, ribbon_dn

# From bb_mtf
bb_lo, bb_mid, bb_hi, rsi14
bb_mid_htf1, bb_mid_htf2

# From ma cross
sma50, sma200, slope50
sma50_htf1/2, sma200_htf1/2
```

### 4.2 Reason (collapse to shapes)

| State field | How to set it (agreement rules) |
|-------------|----------------------------------|
| `force_sign` | Vote dual-HTF from CCI-M, RSI-M, BB mass, SMA mass. **Need agreement.** If sensors fight → 0 |
| `force_strength` | Average of normalized \|M\| / distance-from-mid among agreeing sensors |
| `load_flag` | Any solid LTF stretch **against** force_sign (eddy, band, mid-tag) while force ≠ 0 |
| `load_depth` | How far stretched (normalized) |
| `reclaim_flag` | Cross back with force (0-line, mid band, MA cross/bounce) after load |
| `position` | flat / long / short now |
| `goal_target` | desired target % (context) |
| `risk_budget` | risk % left (context) |
| `session_ok` / `structure_ok` | rails |

```text
Sensor A says long force
Sensor B says long force  --> force_sign = +1
Sensor C says short       --> weakens strength or force_sign = 0
```

**Hard rule remains:** LTF sensors never set `force_sign` alone.

---

## 5. Reasoning examples (stories)

### Story A — good long (use)

```text
Observe: M_cci and M_rsi both > 0 on both HTFs, strength OK
         LTF M_cci dips below 0 for several bars
         then M_cci crosses up through 0
         session OK, risk OK
Reason:  FORCE +1 → LOAD → RECLAIM
Act:     FIRE_LONG
```

### Story B — dip-chase (punish)

```text
Observe: same FORCE +1
         LTF M just went negative (load start)
Reason:  LOAD only — no reclaim yet
Act:     WAIT
Wrong:   FIRE_LONG at the low
```

### Story C — mud thrash (punish)

```text
Observe: HTF CCI-M long, HTF RSI-M short, BB mass flat
         LTF SMA 8/21 crosses both ways
Reason:  FORCE = 0 (no dual agreement)
Act:     WAIT
Wrong:   fire every cross
```

### Story D — anti-force fade (punish as main plan)

```text
Observe: dual HTF force strong long
         LTF at upper BB, RSI high
Reason:  that can be LOAD for a later long OR noise — not default short thesis
Wrong:   FIRE_SHORT every upper band as “strategy”
```

---

## 6. Reward: shape first, never win-rate alone

| Event | Reward idea |
|-------|-------------|
| WAIT when force=0 | + small |
| WAIT during load, no reclaim | + small |
| FIRE on reclaim under force + rails | + larger |
| FIRE force=0 | − large |
| FIRE against force | − large |
| FIRE on load bottom | − large |
| Trade PnL at exit | +/− scaled **secondary** |
| Max win-rate only | **forbidden** as training objective |

```text
total_reward ≈
    shape_terms          (first, largest)
  + rail_terms
  + 0.1..0.3 * pnl_term  (secondary)
  - risk_blow_penalty
```

Win-rate may be **logged**. It must not be the only score.

---

## 7. State vector (what the policy receives)

```text
# shapes
force_sign          # -1, 0, +1
force_strength      # 0..1
load_flag           # 0/1
load_depth          # 0..1
bars_since_load
reclaim_flag        # 0/1 pulse
bars_since_reclaim

# optional sensor summaries (coordinates, not actions)
agree_cci_rsi       # do M_cci and M_rsi force agree?
ribbon_aligned      # 0/1
bb_stretch          # signed distance to mid/band
m_ltf_value         # e.g. M_cci or blended M

# position + goal/risk context
position            # -1, 0, +1
bars_in_trade
goal_target
risk_budget
session_ok
structure_ok
```

Policy learns: **from this state → WAIT / FIRE_LONG / FIRE_SHORT / EXIT**  
Not: “if family_id == McFlurry …”

---

## 8. Curriculum using these eyes

| Stage | Train with |
|-------|------------|
| **1 Force** | Only grade dual-HTF agreement from the five sensors; LTF noise ignored for side |
| **2 Load** | Under force, detect eddy / band / mid-tag; force WAIT |
| **3 Reclaim** | Fire only on reclaim pulses; punish dip-chase |
| **4 Rails** | session / structure / risk_budget |
| **5 Stress** | MC shuffle, hard days — honesty, not WR cosplay |

---

## 9. Cheat sheet (print this)

```text
EYES (top 5)              ASK
-------------------       -------------------------
CCI-M, RSI-M dual HTF  -> Force?
SMA100 / BB mid HTF    -> Force?
LTF M under 0 / band   -> Load?
LTF cross back 0/mid   -> Reclaim?
SMA ribbon tag mid     -> Load?
SMA cross with stack   -> Reclaim candidate?
session + risk         -> Rails?

THEN:  Force → Load → Reclaim → rails → (later stress eval)
NEVER: indicator name = automatic trade
NEVER: win-rate alone = success
```

```text
     OBSERVE five geometries' sensors
                 |
                 v
          BUILD shapes (F/L/R)
                 |
                 v
     STATE = shapes + position + goal/risk
                 |
                 v
         REASON → action
                 |
                 v
      REWARD shape first (+ small PnL)
```

---

## 10. Code helper

Runnable shape bank for these sensors:

→ `Aaron_here/tools/top5_shape_observe.py`

Builds observation + shape fields from a `SetBars` using the same indicator ideas as the top-5 adapters.

---

**Aaron:** The student may **watch** what the top 5 watch.  
The student must **think** Force → Load → Reclaim, with state = shapes + position + goal/risk, and rewards that love process more than hit-rate.

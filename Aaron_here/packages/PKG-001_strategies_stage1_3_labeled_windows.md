# PKG-001 — Strategies folder → Stage 1–3 labeled windows

**Teacher:** Aaron (`@Aaron_here`)  
**Source fuel:** `strategies/` (lab only — **not** a deploy list)  
**Stage recommendation:** run **1 → 2 → 3** in order; do not start at fire  
**Machine block:** `PKG-001_strategies_stage1_3_labeled_windows.json`

---

# Part A — Explain the phrases (for any LLM)

## What “mine shapes and counter-examples” means

**Mine** = dig useful teaching material out of the pile.  
Not “pick the winner and trade it.”

| Word | Plain meaning |
|------|----------------|
| **Shape** | A **role** in the decision: Force, Load, or Reclaim (not “RSI” or “EA name”) |
| **Mine shapes** | From strategy language + adapters + results, extract **when Force was present**, **when Load was present**, **when Reclaim was present** |
| **Counter-example** | A clear **wrong** path: dip-chase, no-force thrash, fight the tide, vanity high-WR + high P(loss) |
| **Mine counter-examples** | Keep those wrong paths on purpose so the student learns **what not to do** |

```text
strategies/  (many names, reports, MC)
        |
        v
   KEEP:  force / load / reclaim stories
   KEEP:  fail stories (thrash, dip-chase, vanity WR)
   DROP:  rank #1 as "the bot"
   DROP:  filename as the skill
```

**Example**

- From McFlurry / CCI reclaim language → **positive shape**: HTF force on → LTF eddy (load) → cross back (reclaim) → fire.  
- From EMA ribbon guide family (WR “pass”, MC P(loss) ~100%, huge trade count) → **counter-example**: fire spam / thrash under weak path quality.

---

## What “curriculum can advance on labeled windows” means

| Word | Plain meaning |
|------|----------------|
| **Curriculum** | Teaching in **stages** (1 Force → 2 Load → 3 Reclaim), not all at once |
| **Window** | A short stretch of bars / steps with a clear story (e.g. 20–200 decisions) |
| **Labeled** | We mark the window: good Force / bad Force / good Load / dip-chase / good Reclaim / etc. |
| **Advance on labeled windows** | The student trains on these **tagged stories**, not on “whatever maximizes win rate this week” |

```text
WRONG way to advance
  "WR > 60% on whole folder → go live"

RIGHT way to advance
  Stage 1: only windows labeled FORCE_OK / FORCE_NONE
  pass gate → Stage 2: windows labeled LOAD_OK / LOAD_INVALID
  pass gate → Stage 3: windows labeled RECLAIM_FIRE / DIP_CHASE / THRASH
```

**Labeled window (sketch)**

```text
Window id: W-S3-POS-001
Bars: t0...t12
Labels per bar:
  t0  force=+1  load=0  reclaim=0  preferred=WAIT
  t3  force=+1  load=1  reclaim=0  preferred=WAIT   (load, no fire)
  t8  force=+1  load=1  reclaim=1  preferred=FIRE_LONG
  t9  force=+1  load=0  reclaim=0  preferred=HOLD/WAIT
Tag: POSITIVE_RECLAIM_FIRE
```

The student learns: **this pattern of states → this action preference.**  
Not: “this EA name won the ranking.”

---

## Why no deploy list

Deploy list = “trade these families live.”  
This package **forbids** that.  
`strategies/` is **fuel for labels**. Monte Carlo already showed most “accurate” books are fragile. We teach **thinking**, not rank worship.

---

# Part B — Formal teaching package

## B0. Method named first

| Piece | Definition for this package (from lab contract) |
|-------|--------------------------------------------------|
| **Force** | Dual HTF agreement on official set (2 HTF + 1 LTF). Side only from HTF. |
| **Load** | LTF stretch **against** Force (pullback / eddy / against-tide timing). Wait. |
| **Reclaim** | LTF returns **with** Force (cross / release / reclaim). Preferred fire. |
| **Objective** | Lab often used first-breath TP/SL for accuracy — treat as **hit-rate costume**, not the edge to copy. |

```text
FORCE? --no--> WAIT
  |
 yes
  v
LOAD? --no--> WAIT
  |
 yes
  v
RECLAIM? --no--> WAIT
  |
 yes
  v
FIRE with force side
```

---

## B1. Sensor roles (roles, not brand names)

| Role | Candidates in `strategies/` adapters (examples) | Must never do |
|------|-----------------------------------------------|---------------|
| **Force** | Dual HTF vs SMA/BB mid; dual HTF M-line sign+strength; dual HTF structure | Let LTF set the side |
| **Load** | LTF M &lt; 0 under bull force; RSI/BB stretch; mid-ribbon touch while fan aligned; retest wait | Fire at load bottom |
| **Reclaim** | M cross back through 0; RSI release through band; break+retest bounce with HTF force | First extreme touch = fire |

**Preferred positive geometry sources (names = pointers to shape only):**

- `sauce__mcflurry_eddy_scalp` / profile `mcflurry`  
- `cci_gravity` reclaim-only upgrade family (many `mt__cci_*` / ZeroLine / Swarm share profile)  

**Preferred negative geometry sources:**

- High trade count + high MC P(loss): e.g. guide `s07_ema_ribbon`, `mt__MA_ribbon_filled_Alerts`, challenge-stack thrash rows  
- High WR + weak MC path: many guide-14 mean-reversion / breakout rows after accuracy shell  

---

## B2. State schema (minimum)

```text
force_sign          # -1 | 0 | +1
force_strength      # 0..1
load_flag           # 0 | 1
load_depth          # 0..1
bars_since_load     # int
reclaim_flag        # 0 | 1  (pulse)
bars_since_reclaim  # int
position            # -1 | 0 | +1
bars_in_trade       # int
stage_id            # 1 | 2 | 3  (curriculum mask)
label_window_id     # optional string for logging
```

Optional later (not required for Stage 1–3): `session_ok`, `structure_ok`, `goal_target`, `risk_budget`.

---

## B3. Action set + stage masks

| Action | Meaning |
|--------|---------|
| WAIT | No new fire |
| FIRE_LONG | Commit long |
| FIRE_SHORT | Commit short |
| EXIT | Flat |

| Stage | Allowed emphasis |
|-------|------------------|
| **1 Force** | Only judge side / wait in mud. Fires against force or in force=0 = hard fail. Prefer WAIT when force=0. |
| **2 Load** | Under force, detect load and **WAIT**. Fire on load bottom = hard fail. |
| **3 Reclaim** | Fire **only** on reclaim under force + recent load. Dip-chase / thrash / anti-force = hard fail. |

---

## B4. Reward sketch (shape first)

```text
Stage 1:
  + correct WAIT when force==0
  + correct side when force!=0 (if any commit allowed at all)
  - treat LTF as side
  - thrash when force==0

Stage 2:
  + WAIT during valid load
  - FIRE during load without reclaim
  - load while force==0 counted as "setup"

Stage 3:
  + FIRE on valid reclaim (force + recent load + reclaim pulse)
  - dip-chase FIRE
  - FIRE force==0
  - FIRE against force
  + small WAIT when load and not reclaim
  (scaled PnL only as secondary term — never alone)
```

**Honesty (always log, never optimize alone):** window hit-rate, trade count, if available MC-style shuffle of outcomes later in Stage 5.

---

## B5. Curriculum gates

| Gate | Pass when |
|------|-----------|
| **S1 → S2** | On Force-only windows: low thrash in force=0; side matches force when acting |
| **S2 → S3** | On Load windows: almost no fires at load bottom; waits through load |
| **S3 solid** | On mixed windows: most fires are reclaim-shaped; dip-chase and no-force near zero |

Do **not** pass a stage because folder WR &gt; 60.4%.

---

## B6. Labeled windows library

Use these as **templates**. Implement by tagging bars from EURUSD lab sets (same contract as strategies batch) or synthetic sequences.  
IDs are stable for logging.

### Stage 1 — Force only

#### Positive / valid

| Window id | Story | Labels to apply | Preferred action |
|-----------|--------|-----------------|------------------|
| **W-S1-POS-DUAL-BULL** | Both HTFs agree long (mid/M-line). LTF noisy. | force=+1, strength high; load/reclaim ignored for grade | WAIT (or hold side lesson only) |
| **W-S1-POS-DUAL-BEAR** | Both HTFs agree short | force=-1 | WAIT (side lesson) |
| **W-S1-POS-NONE-FLAT** | HTFs disagree or flat | force=0 | WAIT only |

#### Counter-examples (negative)

| Window id | Story | Why bad | Student must learn |
|-----------|--------|---------|---------------------|
| **W-S1-NEG-LTF-SIDE** | HTF flat/disagree; LTF cross flips “side” | Lower rewrote higher | force must stay 0 / no fire |
| **W-S1-NEG-ONE-HTF** | Only one HTF “with” trade | Dual agreement missing | no permission |
| **W-S1-NEG-STALE-FORCE** | Old force kept after HTF flip | Force not re-checked | recompute force each step |

**Mine from folder:** any adapter that fires while HTF mass is dead; “LTF-only” thrash families (high trades, force weak).

---

### Stage 2 — Load under Force

#### Positive / valid

| Window id | Story | Labels | Preferred action |
|-----------|--------|--------|------------------|
| **W-S2-POS-EDDY-LONG** | force=+1; LTF M or stretch goes against (below 0 / lower band) | load=1, reclaim=0 | WAIT |
| **W-S2-POS-EDDY-SHORT** | force=-1; LTF stretch against | load=1 | WAIT |
| **W-S2-POS-RETEST-WAIT** | force on; break then sit on level without bounce yet | load-like wait | WAIT |

#### Counter-examples

| Window id | Story | Bad action | Lesson |
|-----------|--------|------------|--------|
| **W-S2-NEG-DIP-CHASE** | force=+1, load=1 at extreme | FIRE_LONG at bottom | Load ≠ fire |
| **W-S2-NEG-LOAD-NO-FORCE** | force=0, oscillator extreme | FIRE either way | No real load |
| **W-S2-NEG-LOAD-FLIP-SIDE** | force=+1, load dip | FIRE_SHORT | Load does not reverse thesis |

**Mine from folder:** pre-upgrade raw CCI zero thrash; dip-entry language; “buy oversold” with no HTF force.

---

### Stage 3 — Reclaim fire

#### Positive / valid

| Window id | Story | Labels | Preferred action |
|-----------|--------|--------|------------------|
| **W-S3-POS-M-RECLAIM-LONG** | force=+1 → load (M&lt;0) → M cross up 0 | reclaim=1 | FIRE_LONG |
| **W-S3-POS-M-RECLAIM-SHORT** | mirror | reclaim=1 | FIRE_SHORT |
| **W-S3-POS-BB-RSI-RELEASE** | force on → RSI outside band → release back | reclaim=1 | FIRE with force |
| **W-S3-POS-RETEST-BOUNCE** | force on → break → retest holds → bounce | reclaim-like | FIRE with force |

**Mine from folder (shape pointers only):**

- McFlurry eddy reclaim  
- CCI gravity reclaim-only upgrade  
- Mark RSI+BB load/release under HTF mass (doctrine notes)

#### Counter-examples

| Window id | Story | Folder echo (shape, not deploy) | Lesson |
|-----------|--------|----------------------------------|--------|
| **W-S3-NEG-FIRST-TOUCH** | Fire on first extreme, no come-back | Many MR guide entries without reclaim story | Need reclaim |
| **W-S3-NEG-THRASH-RIBBON** | Fan/ribbon flip every few bars, force weak/unstable | `s07_ema_ribbon`, MA ribbon — high N, MC P(loss)~100% | Not reclaim skill |
| **W-S3-NEG-NO-FORCE-FIRE** | Cross fires in force=0 | High-trade challenge / spam profiles | Wait in mud |
| **W-S3-NEG-ANTI-FORCE** | force=+1, short every pop | Mean-rev against strong tide windows | Wrong shape |
| **W-S3-NEG-VANITY-WR** | Window optimized only for tight TP hit-rate | Accuracy-pass + high MC P(loss) families | Honesty: WR ≠ edge |

---

### Synthetic sequence templates (always available)

Use when bar harvest is not ready — still valid for Stage 1–3.

**T-POS-FLR (full good long)**

```text
t:  0  1  2  3  4  5  6  7  8  9
F:  0 +1 +1 +1 +1 +1 +1 +1 +1  0
L:  0  0  1  1  1  1  0  0  0  0
R:  0  0  0  0  0  1  0  0  0  0
A*: W  W  W  W  W  FL W  W  W  W
*A = preferred action; FL=FIRE_LONG; W=WAIT
```

**T-NEG-DIP**

```text
F: +1 +1 +1
L:  0  1  1
R:  0  0  0
Bad A: FIRE_LONG on t=1 or t=2
Good A: WAIT until R=1
```

**T-NEG-MUD**

```text
F: 0 0 0 0
L: 0 1 0 1   (invalid "load")
R: 0 0 1 0   (fake reclaim)
Good A: always WAIT
```

---

## B7. How to build windows from the folder (procedure)

```text
1. Pick a family only as a SHAPE POINTER (profile: mcflurry, cci_gravity, mark_rsi_bb, guide_s0x…)
2. Replay lab sets (2HTF+1LTF, PB+cont) OR use synthetic templates above
3. For each bar compute force/load/reclaim roles (shape builder)
4. Attach window tags from B6
5. Train student with stage mask
6. Score compliance (below) — not WR rank
```

```text
Family name ──X──> deploy
Family name ──> profile ──> shape windows ──> train
```

---

## B8. Compliance report template

Log per epoch / per eval:

| Metric | Target direction |
|--------|------------------|
| `force_violation_rate` | → 0 (LTF as side, fire force=0) |
| `dip_chase_rate` | → 0 |
| `anti_force_rate` | → 0 |
| `good_reclaim_fire_rate` | → high among fires (Stage 3) |
| `wait_during_load_rate` | → high (Stage 2–3) |
| `window_hit_rate` | secondary only |
| `mc_median` / `p_loss` | honesty when full books exist — do not gate Stage 1 on this alone |

**Stage pass rule:** shape metrics first.  
If hit-rate high but dip-chase high → **fail stage**.

---

## B9. Notes for the student (plain)

1. You are not learning “which strategy file is best.”  
2. You are learning to **see Force, wait through Load, fire on Reclaim**.  
3. The folder gave us **many names, few shapes**, and a loud honesty lesson: high WR can still be a bad book.  
4. Advance only when labeled windows show fewer violations — not when a leaderboard moves.  
5. Stage 4–5 (rails, MC stress) come **after** Stage 3 is solid.

---

## B10. What this package is not

- Not Court law  
- Not BEST_POLICY  
- Not a live EA list  
- Not “all guide-14 strategies are good”  
- Not permission to skip Stage 1  

---

**Aaron:** Stage recommendation = **start Stage 1 on W-S1-* and T-* templates**.  
When S1 compliance is clean, open S2 windows. Only then S3 reclaim fires.

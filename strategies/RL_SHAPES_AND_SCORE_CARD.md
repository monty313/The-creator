# RL teaching: force / load / reclaim + how to read a strategy file

**Not Court law. Not production promote.**  
Lab teaching material for meta-RL / L2L: **shapes in state**, not EA names as hard rules.

---

## Part A — Shapes the brain should learn

The brain should not memorize “RSI &lt; 30 buy.”  
It should learn **roles** on a multi-timeframe stack:

| Shape | Role | Question the state should answer |
|-------|------|----------------------------------|
| **Force** | HTF side / mass | Is there a real tide, or dead water? |
| **Load** | Pullback / coil / eddy | Is price storing tension *with* the tide? |
| **Reclaim** | Fire / release | Did the eddy *end* so we join the tide? |

**Stack rule (always):**  
**HTF = side.** **LTF = timing only.** LTF never rewrites force.

```text
FORCE (HTF)  →  LOAD (LTF against force)  →  RECLAIM (LTF back with force)  →  hold / exit
     |                    |                            |
  no trade if flat    wait, don't chase             fire only here
```

---

### A1. FORCE — examples for RL state

**Meaning:** both higher timeframes (or dual HTF of the official set) agree there is **directional energy**, not a flat box.

| Sensor example (lab) | Force long | Force short | Fail mode (teach as negative) |
|----------------------|------------|-------------|-------------------------------|
| Price vs BB mid on **both** HTFs | Close above mid on HTF1 **and** HTF2 | Close below both | One HTF above, one below → **no force** |
| M-line (McFlurry-style) on HTFs | M &gt; 0 on both, \|M\| ≥ thr on primary HTF | M &lt; 0 both, \|M\| ≥ thr | M near 0 → **fake permission** |
| SMA stack HTF | Fast &gt; slow and sloping up on both HTFs | Fast &lt; slow sloping down | Cross on LTF only while HTF flat |
| ADX strength (guide S4 idea) | ADX elevated **and** +DI &gt; −DI on HTF context | ADX elevated **and** −DI &gt; +DI | Trade direction when ADX dead (&lt;~25 idea) |

**RL label idea (not hard code):**

- `force ∈ {-1, 0, +1}` or soft `force_strength ∈ [0,1]`  
- Mask / penalty: large action when `force == 0` on “need trend” tasks  

**Concrete bar story (force long):**

```text
HTF1 30m: closes above BB mid for many bars, mid rising
HTF2 1h:  same
LTF  5m:  can still be noisy — that noise is NOT allowed to flip side
→ force = +1
```

---

### A2. LOAD — examples for RL state

**Meaning:** under **existing force**, LTF goes into **tension** (pullback / stretch / eddy), **not** a new opposite thesis.

| Sensor example | Load long (force was +) | Load short (force was −) | Fail mode |
|----------------|-------------------------|---------------------------|-----------|
| RSI(5)+BB on RSI series (Mark) | RSI dipped **outside / below** lower BB while HTF mass long | RSI spiked above upper BB while mass short | Load **against** zero force (random fade) |
| McFlurry M on LTF | M dips **below 0** while HTF M still &gt; 0 | M spikes **above 0** while HTF M still &lt; 0 | Enter **during** the dip as if it were fire |
| BB on price | Price tags lower band / mid from above in uptrend | Tags upper band in downtrend | Catch knife with no HTF force |
| Donchian / breakout language | Pause / retest after expansion (energy store) | Same mirrored | “Load” that is actually full regime flip |
| CCI M-line | Recent min(M) &lt; 0 under bull force (eddy) | Recent max(M) &gt; 0 under bear force | Raw CCI thrash every zero cross |

**RL label idea:**

- `load ∈ {0,1}` or `load_depth ∈ [0,1]`  
- Valid load only if `sign(force) != 0` and load is **against** force (long force → bearish LTF excursion)

**Concrete bar story (load long):**

```text
force = +1 (dual HTF mass up)
LTF:  RSI(5) on RSI series goes below lower BB (stretch down)
      or M-line on LTF prints below 0 (eddy)
→ load = 1, side still long — DO NOT reverse to short
```

---

### A3. RECLAIM — examples for RL state

**Meaning:** LTF **returns through** the timing boundary in the force direction — eddy **ends**. This is the **fire** region.

| Sensor example | Reclaim long | Reclaim short | Fail mode |
|----------------|--------------|---------------|-----------|
| RSI+BB Mark | Cross back **up** through lower BB / mid after load | Cross back **down** through upper | Fire on first touch of extreme (no reclaim) |
| McFlurry | M crosses **back above 0** after being &lt; 0 under bull HTF | M crosses **back below 0** after &gt; 0 under bear HTF | Dip-entry at M&lt;0 minimum |
| CCI gravity upgrade | M reclaim through 0 after recent load min/max | Mirror | Zero-cross spam without dual HTF force |
| BB mean-reversion (careful) | From below lower band, cross back through mid **with** context | From above upper, cross mid down | Fade every band touch in strong trend (anti-force) |
| Breakout retest | Break, retest broken level, bounce **with** HTF force | Mirror | Wick-only break, no close, no retest |

**RL label idea:**

- `reclaim ∈ {0,1}` or event pulse on bar of cross  
- Preferred action region: `force != 0` **and** `load` recently true **and** `reclaim` now true  
- Discourage: `reclaim` with `force == 0`, or fire while still deep in load with no cross

**Concrete bar story (reclaim long → fire):**

```text
force = +1
load  = 1  (M was &lt; 0 for several LTF bars)
now   : M crosses up through 0  (or RSI releases back through BB)
→ reclaim = 1 → legal long fire window
```

---

### A4. Full episode sketches (for curriculum / reward shaping)

#### Sketch 1 — Good long path (reward-friendly)

```text
t0  force→+1
t1  load→1   (eddy / stretch)
t2  still load, no fire          ← patience positive or small wait bonus
t3  reclaim→1 → long entry       ← main positive if outcome ok under risk
t4  hold with force still +1
t5  force decays / opposite reclaim → exit
```

#### Sketch 2 — Dip-chase fail (penalty)

```text
force = +1
load  = 1  (M just went negative)
agent longs immediately at load bottom without reclaim
→ teach: illegal or low-value fire (same class as CCI thrash)
```

#### Sketch 3 — No-force thrash (penalty)

```text
force = 0  (flat HTFs)
LTF RSI/BB or MA cross fires both ways
→ A13-looking trade spam without tide; MC books die
```

#### Sketch 4 — Anti-force fade (penalty in trend curriculum)

```text
force = +1 strong
agent shorts every upper-band touch (“mean reversion”)
→ may win often on tiny TP; MC often still ugly; wrong shape for trend road
```

#### Sketch 5 — Late force (optional advanced)

```text
ADX/force only becomes strong after a long move
reclaim fires late → allow small size or skip (exhaustion class)
```

---

### A5. Suggested state packing (for meta-policy / L2L)

Soft features (examples — names illustrative):

```text
force_sign, force_strength
load_flag, load_depth, bars_since_load
reclaim_flag, bars_since_reclaim
session_ok, structure_ok          # context rails, not the edge itself
goal_target, risk_budget          # A14 context — no retrain on dial change
```

**Curriculum order:**

1. Classify force only (accuracy on side)  
2. Detect load under correct force  
3. Fire only on reclaim events  
4. Add session/structure rails  
5. Stress with MC-style shuffle of outcomes so the policy doesn’t fit one lucky path  

**Do not train the brain to:** maximize lab win rate under first-breath TP alone. That teaches **barrier math**, not force→load→reclaim.

---

## Part B — How to read a strategy file (score card)

Open either:

- `strategies/tweaks/<family_id>.md`  
- `strategies/ranked/NNN_<family_id>/README.md` (all-sim block)

### B1. Three different questions (do not mix them)

| Block | Question it answers | Does **not** answer |
|-------|---------------------|---------------------|
| **Baseline batch** | How did raw adapter + default holds look on 4 sets × PB+cont? | Live edge; tuned accuracy |
| **Accuracy tweak** | After shell + TP/SL tier, is **hit rate** &gt; 60.4% with enough trades? | Robust expectancy; MC survival |
| **Monte Carlo** | Given the **trade return bag**, how often do random paths still win? | Guaranteed future profit |

---

### B2. Field-by-field card

#### Accuracy / tweak section

| Field | How to read |
|-------|-------------|
| **Win rate %** | Fraction of trades that won under **that** exit tier. High is easy with tight TP. |
| **Trades** | Sample size. &lt;~25 is weak for any claim; very low + 90% WR = vanity risk. |
| **Total return %** | Path return on the lab window — one sequence, not MC. |
| **Profit factor** | Gross win / gross loss (lab). Can inflate with few trades. |
| **Tier** (`A_first_breath` …) | Which exit/filter costume was needed to clear WR gate. |
| **Pass YES/NO** | Only means: WR &gt; 60.4% and trades ≥ 25 in lab. **Not** “promote.” |

#### Monte Carlo section

| Field | How to read |
|-------|-------------|
| **Pooled trades** | Size of the bag used for bootstrap/shuffle. |
| **Mean trade return** | Average single-trade return (fraction). Tiny positive + many losses can still die. |
| **Hist terminal** | Compounding the **actual** order of trades once. One path. |
| **MC median terminal** | Half of bootstrap paths end **above** this wealth multiple (start = 1.0). **&gt; 1** ≈ more than half paths finish ahead. |
| **MC p05 / p95** | Bad-day vs good-day path range. Wide + p05 ≪ 1 = fragile. |
| **P(loss)** | Share of paths with terminal &lt; 1. **High P(loss) + high WR** = lie-detector trip. |
| **P(DD ≥ 20%)** | Path risk of deep drawdown in the sim. |
| **Shuffle median / P(loss)** | Same trades, **order** randomized — sequence luck vs bag quality. |

---

### B3. Instant verdict patterns

| You see | Read it as |
|---------|------------|
| WR 75%, MC med **0.95**, P(loss) **95%** | Pretty hit rate, **weak book**. Do not “learn WR.” |
| WR 70%, MC med **1.01**, P(loss) **20%**, trades **200+** | Less vanity; still lab-only, but shape may be worth **feature** study |
| WR 90%, trades **20**, MC med ~1, P(loss) 50% | **Unstable** — too few trades; ignore leaderboard rank |
| Baseline PF huge, accuracy return still poor | Exit/path mismatch; name is not edge |
| Many families **same** score | Shared **profile**, not 12 genius EAs |
| Guide daily strategy, high set1 trade spam | Chart language **mistranslated** onto scalp sets |

**One-liner for RL people:**

> **WR = how often TP won the race. MC = whether the bag of races is still +EV under resampling. Geometry = what state should look like when we allow fire.**

---

### B4. What to extract for RL from a file (checklist)

```text
[ ] Profile / geometry class (cci reclaim? bb mass? ribbon thrash?)
[ ] Force definition implied by adapter
[ ] Load definition
[ ] Reclaim / fire definition
[ ] Fail mode visible in MC (thrash volume? low n?)
[ ] Do NOT copy: rank number, vanity WR, EA filename as action rule
[ ] Optional: use high-WR + high-P(loss) runs as *negative* examples
```

---

### B5. Tiny example (made schematic)

```text
Family: note__algo_guide_14_s07_ema_ribbon_md
WR:     70%     ← looks “accurate”
Trades: 1500+   ← lots of fires (thrash risk)
MC med: 0.91    ← typical path ends down
P(loss): ~100%  ← almost all bootstrap paths lose

RL takeaway:
  Ribbon *align* can be a FORCE feature.
  Do not reward a policy for max trade count on ribbon flips.
  Prefer: force stable → load to mid ribbon → reclaim resume, fewer fires.
```

```text
Family: sauce / McFlurry-like or CCI reclaim upgrade
WR:     high under reclaim rules
MC:     better P(loss) than thrash families *when* trade bag is clean
RL takeaway:
  State should encode HTF M force + LTF eddy (load) + zero reclaim (fire).
  Dip-entry without reclaim = labeled mistake.
```

---

## Part C — One diagram for the brain

```text
                 HTF FORCE
              (+1 / 0 / -1)
                    │
         ┌──────────┴──────────┐
         │ force == 0          │ force != 0
         ▼                     ▼
      NO FIRE              LTF LOAD?
      (or explore          (against force)
       tiny size)               │
                          yes   │   no
                           ▼    │    ▼
                        WAIT    │   WAIT / hold
                      for RECLAIM
                           │
                           ▼
                    RECLAIM cross?
                      yes → FIRE with force
                      no  → still wait
```

---

**Files:** this card lives at `strategies/RL_SHAPES_AND_SCORE_CARD.md`.  
**Process SSOT:** `strategies/LLM_INSTRUCTIONS.md`.  
**Geometry prose:** `strategies/00_intuition.md`.

# 00_intuition — what this folder actually teaches

**Author:** Mark Here, Esq.  
**Scope:** `strategies/` language + 1:1 vectorbt batch (123 families, 2HTF+1LTF, 4 sets, PB+cont).  
**Not law.** Intuition for teaching a brain — not a promote list.

---

## 1. Core geometry (what works)

| Layer | Job | Rule |
|-------|-----|------|
| **HTF ×2** | Side / mass | Both agree or no trade thesis |
| **LTF ×1** | Timing only | Never redefines side |
| **Pullback** | Load | Wait when stretched against release, with tide |
| **Continuation** | Fire | Release / reclaim with tide |
| **4 sets** | Scale | Same structure on `1m/15m/30m` · `5m/30m/1h` · `15m/1h/4h` · `30m/4h/1d` |

Anything that preserves this stack is useful as **state / labels**.  
Anything that collapses HTF into LTF or LTF into side is garbage for learning.

**Mark instruments (doctrine, not batch winner):**  
HTF mass = price vs BB mid on **both** HTFs.  
LTF = RSI(5) + BB on the **RSI series** (not price): load outside band, fire on release cross, only with mass.

---

## 2. What the folder is

| Kind | Reality |
|------|---------|
| MT names (~95) | Mostly version spam + indicator soup + black-box “RL” shells |
| Notes | Sparse geometry (S1–S4, SNAP-8, RSI-BB skill, factory names) |
| Public TA | Baselines / negative examples |
| Rank ties | Same adapter profile → same score; **name ≠ edge** |

Museum of *attempted edges*. Not a menu of finished bots.

---

## 3. What works (durable)

1. **Force before timing** — dual HTF agreement before LTF fire.  
2. **Load ≠ fire** — pullback and continuation are different labels. Merging them trains thrash.  
3. **Tension geometry** — CCI/RSI vs own center or band (slingshot, snap, gravity). Better than “cross MA and pray.”  
4. **Density with structure** — ribbon / micro pullback under higher bias (SNAP-8 shape) fits scalping cadence *if* risk rails exist.  
5. **Regime sensors** — Donchian / envelope / ORB as *expansion flags*, not sole entry law.  
6. **One scaffold, many features** — same 2HTF+1LTF PB/cont path; swap sensors, don’t invent a new religion per filename.

---

## 4. What fails (durable)

1. **Filename multiplicity** — v2…v11, Strategy4_v7, Swarm/swarm3: same idea, zero new physics.  
2. **Hard-coded exits as strategy identity** — fixed hold / fixed R:R in a batch is not an edge; it is a clock.  
3. **PF without equity path** — high profit factor + flat/negative return + bad Sharpe = score artifact, not alpha.  
4. **LTF-only / single-TF bots** — blind to mass; overtrade chop.  
5. **Breakout soup in range** — dual thrust, naive ORB, supertrend thrash without HTF gate.  
6. **Black-box RL EAs without weights** — names (DQN, NN, Q-learn) are not policies. Policy = trained map + context.  
7. **RSI14/BB20 retail defaults** as Mark substitutes — wrong instrument geometry.  
8. **Strategy-only BC** — model memorizes correlated fires, not load/release principle.  
9. **Utilities as strategies** — screeners, error plots, panel tools: not entry systems.  
10. **Promote-from-leaderboard** — one symbol, one window, shared scaffold ≠ production proof.

---

## 5. What to take into the RL brain

| Take | How |
|------|-----|
| Official sets always | State built on all four stacks |
| Mass bit | Dual HTF side permission |
| Load / release bits | LTF feel (RSI-BB or cousin tension) |
| Skill IDs | `wait_loaded`, `fire_continuation`, not “run EA #47” |
| Concurrence | Prefer samples where Mark act ≡ geometry |
| Risk as rails | Breach 0, size under envelope — not exit folklore |
| Meta-train | Target/risk in context; no retrain at inference (A14) |
| A13 density | Capacity from real LTF structure, not pad trades |

**Do not hard-code** folder winners as production if-rules.  
**Do teach** geometry that generalizes across days and renames.

---

## 6. What to discard

- Version forks of one EA  
- Closed stubs / empty `.mq5` + binary-only  
- MyTrader / non-edge tools  
- Indicator mash without HTF force  
- “Neural” branding without a learnable state→action map  
- Leaderboard worship from a single batch config  

Keep as **negative curriculum** (what thrash looks like), not as teachers of fire.

---

## 7. Compression (the whole folder in one claim)

> **Edge is multi-scale force + timed load/release under risk rails.**  
> **Learning is skill labels on that geometry, not cloning strategy files.**  
> **Names are aliases. Physics is not.**

---

## 8. For future models (still true later)

- Invariance > parameters: mass / load / release / set stacks survive renames.  
- Separate **permission** (HTF), **timing** (LTF), **sizing** (risk), **exit** (policy).  
- Measure with full path stats (return, DD, trades, breach), not one vanity ratio.  
- Sparse labels + concurrence beat dense wrong labels.  
- A museum of failed EAs is evidence about *search space*, not a shopping list.

---

## 9. Pointers (evidence, not doctrine)

| Artifact | Use |
|----------|-----|
| `FAMILY_INVENTORY_1TO1.json` | What was tested 1:1 |
| `STRATEGY_TEST_REPORT.md` / `.json` | Scores / vectorbt fields |
| `ranked/INDEX.md` | Order under batch sort key |
| `mark_doctrine_refs/RSI_BB_L2L_SKILL.md` | Timing geometry |
| `the_truth_main_extra/strategy_S*.md` | Clean sparse specs |
| `army_snap8/STRATEGY.md` | Dense pullback texture |
| `sauces/H001_mcflurry_eddy_scalp.md` | McFlurry eddy (RSI multi-TF M-line) |
| `sauces/DimensionJump_sauce.md` | Dimension Jump (CCI + BB-on-CCI) — McFlurry pair |
| `SAUCES_TEST_REPORT.md` | Vectorbt results for both sauces |

---

**Bottom line (Part 1):** From this folder, harvest **geometry and labels**. Starve **hard-coded EA soup**. Train a brain that *reads mass and fires release* — not a brain that memorizes which filename ranked first on one EURUSD window.

---
---

# Part 2 — How we improved the strategies, and what that means forever

**Author:** Mark Here, Esq.  
**Scope:** post-baseline methods: accuracy layer on all 1:1 families; CCI reclaim upgrade vs McFlurry.  
**Audience:** humans now; models later. Keep the *invariants*, not the EURUSD numbers.  
**Not law.** Methods are experiments. Some raise **hit rate** without raising **economic edge**. Both facts must travel together.

---

## P2.1 Problem we actually solved (not the story people tell)

Three different problems got confused. Separating them is the first method.

| Problem | Metric people use | What it really is |
|---------|-------------------|-------------------|
| **A. Hit rate** | Win rate % | Fraction of closed trades that are green |
| **B. Path quality** | Return, DD, Sharpe | Whether the equity path is worth running |
| **C. Teachability** | Skill labels, concurrence | Whether a brain can *reuse* the geometry |

Baseline museum results (Part 1 era):

- Aggregate hit rates sat ~**45–52%** for most families under shared PB/cont + fixed-hold exits.
- A single-cell high was ~**60.4%** (linear-regression class, one set×mode) — not an aggregate win.
- Score boards that maximized PF alone produced **ties** and **mirages** (high PF, negative return).

We then ran two improvement programs:

1. **Accuracy program** — force every family aggregate win rate **> 60.4%** with non-empty trade books.  
2. **CCI vs McFlurry program** — make the CCI gravity family beat McFlurry on **both** win rate **and** mean return under the same contract.

Those are different knobs. A future reader who mixes them will invent cargo-cult “tweaks.”

---

## P2.2 Measurement contract (do not break this or comparisons die)

All improvement claims in this lab used the same skeleton:

```
for each official set in {1m|15m,30m · 5m|30m,1h · 15m|1h,4h · 30m|4h,1d}:
  build LTF bars; map completed HTF1/HTF2 onto LTF (shift+1, ffill)  # no peeking unfinished HTF
  for mode in {pullback, continuation}:
    entries = family_signal ∩ mode ∩ filters
    exits   = TP/SL (and optionally opposite / time) via vectorbt Portfolio.from_signals
aggregate win_rate = trade-weighted mean of set×mode win rates
aggregate return   = mean of set×mode total returns   # lab convention; report both
```

**Invariants of a fair compare:**

1. Same symbol window for both arms (here: EURUSD M1 slice, documented in JSON).  
2. Same fee/slippage assumptions.  
3. Same four sets and both modes present in the book (empty set×mode allowed only if labeled).  
4. No zero-trade “100% accuracy” (min trade floor; we used ≥25 on the accuracy gate).  
5. 1:1 family IDs — shared *code path* is allowed; shared *score row* is not.

If you change the contract, you must **re-baseline**, not reuse old ranks.

---

## P2.3 Method stack that raised accuracy on *all* families

### Layer diagram

```
[raw family language]  →  adapter (sensor → long/short events)
        ↓
[permission] dual HTF force (family-specific)
        ↓
[accuracy filters] session · strength · bar confirm · micro-structure
        ↓
[exit policy] tight TP + wider SL  (TP/SL barriers; no random time-flat)
        ↓
[vectorbt stats] WR, return, DD, PF, trades
```

Adapters stay **pure** (OHLCV → events). Filters and exits are **orthogonal**. That separation is why 100+ families could be improved without rewriting each EA by hand.

### Filter 1 — Session mask (07–21 UTC)

**What:** Keep only London + NY cash-hour bars.  
**Why it moves hit rate:** Off-session prints are thinner; structure breaks more often; LTF “signals” fire into noise.  
**Physics read:** Activity is not uniform; permission without participation is empty.  
**Failure mode if abused:** Overfit a timezone. Always document timezone and symbol session.

### Filter 2 — HTF strength (distance from SMA)

**What:** Dual HTF closes must sit **away** from SMA(50) in the trade direction (fractional distance floor).  
**Why:** “Both HTFs above mid” can be **flat mass** — side is right, energy is zero. Those fires lose more.  
**Physics read:** Force is direction **plus** distance from equilibrium, not a boolean costume.  
**Future models:** Encode strength as continuous state, not only a hard gate.

### Filter 3 — Bar confirmation

**What:** Entry bar close must agree with side (close > open for long).  
**Why:** Kills “signal printed on a bar that already failed.”  
**Physics read:** Timing is a **candle event**, not only an indicator value at the close of a prior idea.  
**Failure mode:** Can late-enter; trade that for higher hit rate knowingly.

### Filter 4 — Micro structure (HL / LH)

**What:** Long only if recent higher-low texture; short if lower-high.  
**Why:** Pullback-resume is an eddy that ends with constructive structure, not a random oscillator tick.  
**Physics read:** Geometry of price path, not only oscillator path.

### Exit policy — “first breath” TP / wider SL

**What:** Small take-profit vs larger stop-loss as price fractions; **no** time-stop that randomly flats mid-path (time-stop alone held WR ~48% and failed the accuracy gate).  
**Why hit rate rises:** On near-random paths, P(hit TP before SL) ≈ `SL / (TP + SL)` when barriers are absorbing. Tight TP + wide SL → high WR.  
**Why this is not magic alpha:** With zero edge, EV ≈ 0 before costs; with costs, EV often **negative** even at high WR.  
**Honest name:** accuracy-first scalp exit, not “edge proof.”  
**Mark framing:** Bank the first unit of continuation; invalidate when the thesis dies. Expectancy is a **separate** optimization.

### What we refused

| Refuse | Reason |
|--------|--------|
| Empty books as 100% WR | Forbidden lie |
| Single set×mode cherry-pick as “the” accuracy | Aggregate gate required |
| Collapsing 12 filenames into one score to “pass” | Breaks 1:1 inventory |
| Time-stop as primary exit for accuracy | Randomizes hit rate downward |
| Promoting filters into Court law | Not measured as production policy |

### Empirical outcome (accuracy program)

- **125/125** families cleared **WR > 60.4%** with **≥ 25** trades under the documented accuracy layer.  
- Min aggregate WR ~**68.6%**, max ~**80%** (McFlurry under that layer).  
- Artifacts: `TWEAKED_ACCURACY_RESULTS.json`, per-family `tweaks/*.md`.

**Transferable rule:** If you need **hit rate**, fix **entry selectivity + barrier geometry + remove noise exits**. If you need **money**, you still need **edge in the signal** or you will print pretty WR and bleed.

---

## P2.4 Method stack that made CCI beat McFlurry (accuracy *and* profit)

McFlurry under accuracy layer was roughly **WR ~80%**, **mean return ~+0.10%**.  
Raw CCI zero-cross thrash under the same layer sat ~**73% WR** and **negative** return.

### Failure diagnosis (why plain CCI lost)

1. **Entering the dip** — PB defined as “CCI still extreme but ticking up” or cross into the eddy → many micro-fades against the river.  
2. **Weak force** — HTF “CCI > 0” is cheap permission; flat / mixed HTF still allowed.  
3. **Wrong exit pairing** — same first-breath TP as McFlurry without McFlurry’s selective reclaim structure → high activity, worse path.  
4. **Sensor not structure** — raw CCI level ≠ multi-scale *acceleration* of CCI.

### Upgrade (what actually moved both WR and return)

| Piece | Implementation idea | Role |
|-------|---------------------|------|
| **M-line on CCI** | `M = SMA7(SMA2(CCI20)) − SMA21(SMA2(CCI20))` | Same eddy operator as McFlurry; sensor = CCI not RSI |
| **Genuine force** | Both HTF `M` same sign; \|M_HTF1\| ≥ thr (lab: 8) | Reject “high but not moving” |
| **Reclaim-only fire** | Recent load (rolling min/max of M across ~8 bars) **then** cross back through 0 | Never enter the dip itself |
| **PB & cont labels** | Both map to reclaim fire in the upgraded path | Stops PB mode from poisoning the book |
| **Exit** | Slightly wider TP than default first-breath (lab: tp 0.00028 / sl 0.00115 on EURUSD) | Keep high hit rate *and* more $ when right |
| **Filters** | Session + strength + bar confirm + structure | Same accuracy shell |

### Outcome (head-to-head, same window/contract)

| | CCI upgraded | McFlurry |
|--|-------------:|---------:|
| WR% | **100** | 80 |
| Mean return % | **~0.22** | ~0.10 |
| PF (avg set×mode) | **high** | lower |
| Trades | **fewer** (~44) | more (~212) |

**Read this correctly:** fewer trades + selective reclaim + barrier exits can print extreme WR on a short window. That is **success on the stated goal**, not proof of forever alpha. Sample size is small; OOS and multi-asset still required before production belief.

Artifact: `CCI_VS_MCFLURRY_REPORT.md` · code: `fam_cci_gravity` in `python_batch/families.py`.

### Generalization of the CCI upgrade

Whenever a family “has the right story” but loses:

1. Ask: **are we entering load or reclaim?**  
2. Ask: **is force magnitude present or only sign?**  
3. Replace raw oscillator crosses with an **M-line (short MA − long MA on the oscillator)** so you trade *acceleration*, not level.  
4. Align PB/cont so one mode is not a pure thrash generator.  
5. Re-optimize **exit barriers** only *after* entry is reclaim-clean — otherwise you tune noise.

---

## P2.5 The improvement algebra (so future models can re-derive, not memorize params)

Think of a trade as:

```
permission = 1[ dual_HTF_force ∧ strength(force) ]
timing     = 1[ load_or_reclaim event on LTF ∧ structure ∧ session ]
entry      = permission ∧ timing ∧ bar_confirm
outcome    = barrier_process(price path | entry, TP, SL, costs)
```

**Hit rate** is mostly shaped by:

- how rare and clean `timing` is,  
- whether `timing` is reclaim vs dip-chase,  
- `P(hit TP first | path)` from barrier geometry,  
- noise exits that interrupt barriers.

**Profit** is shaped by:

- E[Δprice | entry] (edge),  
- TP/SL asymmetry,  
- costs × trade count,  
- path dependence (streaks of SL).

**Identity (do not forget):**

```
high WR ⇏ positive EV
high PF on a short window ⇏ robust edge
more trades ⇏ more learning value
```

**Identity that *does* hold operationally:**

```
reclaim under force  >  dip-chase under force  >  oscillator noise without force
shared scaffold + swappable sensors  >  N reinvented bots
documented contract  >  tribal “it worked yesterday”
```

---

## P2.6 What not to learn from the improvement program

1. **Do not ship the accuracy layer as the production brain.** It is a *measurement and teaching scaffold*, not A14 meta-policy.  
2. **Do not treat 100% WR as a target for live trading.** It is a symptom of selectivity + barriers on a finite sample.  
3. **Do not conclude CCI “always beats” RSI/McFlurry.** We beat McFlurry on **one window, one symbol, one exit pair** after restructuring entry. Flip the window and re-measure.  
4. **Do not use time-stops to “fix” bad entries for accuracy.** They randomize.  
5. **Do not score empty books.**  
6. **Do not collapse filenames** when the human asked for 1:1 truth.  
7. **Do not optimize one metric in isolation** without reporting the others in the same table.

---

## P2.7 Deep intuition for models ~5 years out

You will have better compute, better bars, and more libraries. The following should still pay rent.

### A. Markets are multi-scale permission systems

Price is not a single Markov chain you “classify.”  
**Higher scales grant permission; lower scales time participation.**  
Any architecture that flattens all timeframes into one embedding without an explicit permission channel will relearn thrash.

### B. Load and fire are different random variables

Training one head to predict “trade now” mixes:

- *wait while loaded*,  
- *fire on release*,  
- *do nothing*.

Those have different payoffs and different state geometries.  
**Separate labels** (even if the production policy is unified later).

### C. Sensors are coordinates; physics is the map

RSI-BB, CCI M-line, SMA ribbon, Donchian width are **charts of the same territories**: force, stretch, reclaim, expansion.  
When two sensors agree under dual HTF force, you have concurrence — gold for learning.  
When a filename changes and the sensor is renamed, the map should not break. **Train on roles, not ticker strings of indicators.**

### D. Barrier exits are a choice of objective

Choosing TP << SL is choosing **hit-rate geometry**.  
Choosing TP ≈ SL or trail is choosing a different objective.  
RL should expose exit policy as **context** (goal/risk), not a frozen EA habit. That is the same spirit as “no retrain when target/risk changes” — the *map* stays; the *rail* changes.

### E. Museums of strategies are search traces

A folder of 90 EAs is a fossil record of human search.  
Value:

- negative curriculum (what thrash looks like),  
- feature ideas (what humans tried to measure),  
- rarity of true multi-scale structure.

Non-value:

- cloning the median EA,  
- majority-vote of bad bots,  
- prestige of “neural” in the title.

### F. Improvement is layer surgery

When a strategy fails, do not only retune period=14→13.

Ask, in order:

1. Is **permission** false or weak?  
2. Is **timing** dip-chase?  
3. Are **exits** fighting the entry (time-stop thrash)?  
4. Is the **objective** (WR vs EV vs density) mis-specified?  
5. Is the **contract** (sets, costs, window) incomparable?

That checklist is more valuable than any single parameter we printed in 2026.

### G. Accuracy programs can poison RL if misused

If you train only on high-WR barrier books, the agent may learn:

- “take tiny wins,”  
- “avoid any path that needs time,”  
- “ignore large R opportunities.”

That can be fine for a **skill prior** (first breath after reclaim) and fatal as the **only** reward.  
**Curriculum:** teach reclaim recognition first; teach full distribution of outcomes second; teach risk-conditioned sizing third.

### H. Dual-sauce thinking (McFlurry / Dimension Jump / CCI M-line)

Observation-only “sauces” failed as standalone gods and succeeded as **languages for stretch and reclaim**.  
The winning pattern across improvements:

```
define force on HTF in the sauce’s native coordinates
define load on LTF in the same coordinates
forbid entry on load alone
allow entry on reclaim under force
exit with an explicit objective (breath vs hold for R)
```

That pattern will outlive Bollinger period arguments.

### I. Sample size humility without paralysis

44 trades at 100% WR is a **signal that the filter is sharp**, not a license to bet the firm.  
Future models should auto-report:

- trades,  
- bootstrap CI on WR and EV,  
- multi-symbol / multi-window replication,  
before elevating a tweak to “known physics.”

### J. What “better than Part 1” means here

Part 1 said what the museum *is*.  
Part 2 says how you **operate on** a museum:

- separate objectives,  
- keep a measurement contract,  
- apply orthogonal filters,  
- fix reclaim vs dip,  
- report WR and money together,  
- never confuse a pass gate with a production policy.

---

## P2.8 Procedure card (copy this when improving any strategy family)

```
1. Freeze contract (symbol, window, sets, modes, costs).
2. Baseline: WR, return, DD, PF, trades (trade-weighted WR).
3. Classify failure: permission / timing / exit / objective / contract.
4. Apply at most one class of change per iteration.
5. If raising WR:
     - remove noise (session, strength, structure)
     - reclaim not dip
     - barrier exits without random time-flat
     - enforce min trades
6. If raising profit:
     - first fix reclaim under force
     - then adjust TP/SL / trail for EV
     - re-check WR did not collapse into thrash
7. Write: what / why / before / after (same metrics).
8. Refuse promote until multi-window / multi-symbol if stakes are real.
```

---

## P2.9 Pointers (improvement era)

| Artifact | Use |
|----------|-----|
| `python_batch/accuracy_tweaks.py` | Shared accuracy filters + rationale string |
| `python_batch/run_tweak_batch.py` | Full-family accuracy gate runner |
| `TWEAKED_ACCURACY_REPORT.md` / `.json` | Pre/post WR for all families |
| `tweaks/*.md` | Per-family what/why/final scores |
| `python_batch/run_cci_vs_mcflurry.py` | CCI vs McFlurry head-to-head |
| `CCI_VS_MCFLURRY_REPORT.md` / `.json` | Proof CCI beat McFlurry on WR + return |
| `python_batch/families.py` → `fam_cci_gravity` | Reclaim M-line implementation |
| `sauces/H001_mcflurry_eddy_scalp.md` | Original eddy language (RSI) |

---

## P2.10 Final compression (Part 2)

> **Improving a strategy is not renaming indicators.**  
> It is enforcing permission, refusing dip-chase, choosing an exit *objective*, and measuring under a frozen contract.  
> **High accuracy is a designed barrier geometry + selective reclaim — until proven otherwise with EV and replication.**  
> **High profit is edge under that geometry — not the geometry alone.**  
> Teach brains the geometry and the difference between objectives.  
> Do not teach them that a leaderboard row is the market.

**Bottom line (Part 2):** We raised every family’s hit rate by **orthogonal filters + reclaim-friendly exits**, and we raised CCI above McFlurry by **M-line force + reclaim-only entry + matched barriers**. Keep the **method**. Distrust the **specific pips** until they survive new windows.

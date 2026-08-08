# FULL OBS + TIMEFRAME SETS (Mark clone eyes)

**For:** MARK HERE on Desktop (`The Creator\mark_here`)  
**Source lab:** `the-truth`  
**Updated:** 2026-08-07  

This is what the **Mark full-obs** policy sees, and the **official TF sets** that define the chart.

---

## 1) Two different “obs” systems (do not mix)

| Stack | Dim | Where | Use |
|-------|-----|-------|-----|
| **Mark FULL obs** (lineage) | **168** | `lineages/.../perception/observation_full.py` | Policy = Mark clone / Channel1 + agents |
| **PROVEN production** | **1820** | `features.yaml` slots OFF | Frozen PROVEN brains |
| **SIGON / new production** | **~6820** | slots ON (`include_signal_agent_slots: true`) | New train only — never warm-start PROVEN |

**Hard rule:** Never load PROVEN weights into Mark-full-obs (168) or SIGON (~6820) without a full retrain.

---

## 2) Official timeframe sets (Mark-on-chart LAW)

**LTF = first (timing / pullback / cont / add)**  
**HTF = last two (trend force / confirmation)**  
Scan **all 4 sets**.

### Mark lock (`sets_mark`) — correct for policy = Mark

| Set | Name | LTF (entry) | HTF confirm | Extra (obs-only / context) |
|----:|------|-------------|-------------|----------------------------|
| **1** | micro | **1m** | **15m, 30m** | 1h |
| **2** | intraday | **5m** | **30m, 1h** | 4h |
| **3** | swing | **15m** | **1h, 4h** | 1d |
| **4** | macro | **30m** | **4h, 1d** | 1w |

```text
set1:  1m  | 15m, 30m
set2:  5m  | 30m, 1h
set3: 15m  | 1h, 4h
set4: 30m  | 4h, 1d
```

**Config:** `configs/timeframes.yaml` → `sets_mark`  
**Lineage code (always Mark):** `lineages/adaptive_rl_brain_7_31_26/perception/sets.py` → `MARK_SETS_LAW`  
**Engine lock key:** `configs/features.yaml` → `sets_lock:`  
- `mark` = Mark stacks (new trains)  
- `proven_legacy` = frozen PROVEN stacks (wrong set2/set3 HTFs vs Mark — do not use for Mark)

### PROVEN legacy stacks (for PROVEN only — NOT Mark)

| Set | LTF | HTFs |
|----:|-----|------|
| 1 | 1m | 15m, 30m |
| 2 | 5m | **1h, 4h** |
| 3 | 15m | **4h, 1d** |
| 4 | 30m | 4h, 1d |

`observation_only: [1w]`

### Sub-sets (weaker / lower confidence) — lineage Channel1

| Sub | Entry | Confirm |
|-----|-------|---------|
| A | 1m | 5m |
| B | 5m | 15m |
| C | 15m | 30m |
| D | 1h | 4h |
| E | 4h | 1d |

---

## 3) Mark FULL observation (dim = **168**)

Source: `lineages/adaptive_rl_brain_7_31_26/perception/observation_full.py`

```text
MARK_FULL_DIM = 168 = 32 + 16 + 12 + 92 + 16
```

| Block | Indices | Size | What |
|-------|---------|-----:|------|
| **Channel1** | `[0:32]` | 32 | Sets + structure + progress/danger/session |
| **Doctrine** | `[32:48]` | 16 | Force, regime, play, confidence, teacher side |
| **Majority** | `[48:60]` | 12 | Panel vote stats across agents |
| **92 signal agents** | `[60:152]` | 92 | Each slot vote −1 / 0 / +1 |
| **Self-state** | `[152:168]` | 16 | Side, heat, goal/floor, hardness, session |

Teacher (Mark soul) owns labels. Policy learns attention over this board.

---

### 3a) Channel1 detail (32 floats)

Source: `perception/observation.py`

| Indices | Content |
|---------|---------|
| `[0:12]` | Official sets **1–4** × (direction, velocity, confluence_score) |
| `[12:27]` | Sub-sets **A–E** × (direction, velocity, confluence_score) |
| `[27]` | pullback (0/1) |
| `[28]` | scale_conflict (0/1) |
| `[29]` | progress_to_goal |
| `[30]` | danger |
| `[31]` | session_phase |

Per set/sub triple:

| Feature | Meaning |
|---------|---------|
| direction | −1 bear / 0 flat / +1 bull |
| velocity | none→0 … strong→1 |
| confluence_score | signed agreement `(n_bull − n_bear) / n` ∈ [−1, 1] |

---

### 3b) Doctrine context (16 floats) — indices 32–47

| i | Field |
|--:|-------|
| 0 | force_dir (−1/0/+1) |
| 1 | n_force_bull / 4 |
| 2 | n_force_bear / 4 |
| 3 | n_aligned / 4 |
| 4 | n_breather / 4 |
| 5 | m_conf (scaled) |
| 6 | m_regime |
| 7 | play == launch |
| 8 | play == breath/breather |
| 9 | play == aligned |
| 10 | regime bull |
| 11 | regime bear |
| 12 | regime chop |
| 13 | regime flat |
| 14 | teacher raw BUY |
| 15 | teacher raw SELL |

---

### 3c) Majority summary (12 floats) — indices 48–59

| i | Field |
|--:|-------|
| 0 | frac_bull |
| 1 | frac_bear |
| 2 | agree_frac |
| 3 | n_active / n_agents |
| 4 | has_majority (0/1) |
| 5 | maj_dir |
| 6 | mean_vote |
| 7 | std_vote |
| 8 | n_bull / n |
| 9 | n_bear / n |
| 10 | n_flat / n |
| 11 | n_agents / 92 |

---

### 3d) All 92 signal agent votes — indices 60–151

Registry: `configs/signal_slots.yaml`  
Index doc: `code/signals/00_ALL_92_AGENTS.md`  
Capacity: **500** slots; filled **92** (enabled **91** — slot 25 ORB off)

Each value: **+1 buy | −1 sell | 0 flat/empty**

#### Families (count)

| Family | ~Count | Role |
|--------|-------:|------|
| momentum_one | 9 | Bread-and-butter / cont / rev by set |
| camillion | 18 | Gravity, regime pulse, CCI, SMA stack, ADX |
| decision_tree | 4 | FTMO / S11 |
| rl_trading_live | 5 | Phase sensors |
| sma_mtf | 8 | SMA multi-TF |
| rsi_mtf | 11 | RSI multi-TF |
| stoch_mtf | 8 | Stoch multi-TF |
| stoch_ema | 3 | Stoch+EMA |
| rsi2_ema | 9 | RSI2 + EMA pairs |
| smma_rsi | 4 | SMMA RSI |
| agree | 4 | Cross-family agreement (≥70% band) |
| dvmr | 3 | DVMR multi-TF |
| momentum_vector | 3 | MV profit recipes |
| bb_rsi_sma | 3 | BB/RSI/SMA multi-set |

#### Slot list (0–92; skip empty 9)

| Slot | Name | Family |
|-----:|------|--------|
| 0 | mo_bread_and_butter_pull_set1 | momentum_one |
| 1 | mo_continuation_set1 | momentum_one |
| 2 | mo_bread_and_butter_pull_set2 | momentum_one |
| 3 | mo_continuation_set2 | momentum_one |
| 4 | mo_pull_set3 | momentum_one |
| 5 | mo_continuation_set3 | momentum_one |
| 6 | mo_rev_set1 | momentum_one |
| 7 | mo_rev_set2 | momentum_one |
| 8 | mo_rev_set3 | momentum_one |
| 10 | cam_gravity_30m_4h | camillion |
| 11–14 | cam_regime_pulse_* | camillion |
| 15–18 | cam_cci_surge_* | camillion |
| 19–22 | cam_sma_stack_* | camillion |
| 23–24 | cam_sma_reversion_rally_* | camillion |
| 25 | cam_orb_ny_breakout_indices | camillion **OFF** |
| 26–27 | cam_adx_di_align_* | camillion |
| 28–31 | dt_ftmo_alpha, s11_* | decision_tree |
| 32–36 | phase_* | rl_trading_live |
| 37–44 | sma_mtf_* | sma_mtf |
| 45–55 | rsi_mtf_* | rsi_mtf |
| 56–63 | stoch_mtf_* | stoch_mtf |
| 64–66 | stoch_ema_A/B/C | stoch_ema |
| 67–75 | rsi2_ema_* | rsi2_ema |
| 76–79 | smma_rsi_* | smma_rsi |
| 80–83 | agree_* | agree |
| 84–86 | dvmr_* | dvmr |
| 87–89 | mv_*_30m_4h_long | momentum_vector |
| 90–92 | bb_rsi_sma_A/B/C | bb_rsi_sma |

**KEEP ALL sensors** — wire into production after Mark soul is full (`KEEP_AFTER_SOUL.md`).  
Until then: agents = sensors; Mark doctrine owns side.

---

### 3e) Self-state (16 floats) — indices 152–167

| i | Field |
|--:|-------|
| 0 | side (−1/0/+1) |
| 1 | n_open_units / 8 |
| 2 | n_entries / 12 |
| 3 | n_adds / 4 |
| 4 | progress |
| 5 | danger |
| 6 | target_pct / 5 |
| 7 | risk_pct / 5 |
| 8 | hardness = target/risk (scaled) |
| 9 | equity_pct / 5 |
| 10 | room_to_floor / risk |
| 11 | remaining_to_target / target |
| 12 | mark_soul flag |
| 13 | soul_flips / 4 |
| 14 | session_phase |
| 15 | in_trade |

---

## 4) Production feature obs (not Mark 168 — context only)

From `configs/features.yaml` (PROVEN / SIGON path):

| Include | Notes |
|---------|--------|
| frame_stack | 10 |
| no_raw_prices | true |
| cci | periods 30, 100 + SMA |
| s2_bb | wide/fast BB + SMA50 |
| envelope | period 4 |
| s4_rsi | fast 2, slow 20, BB |
| atr | 5, 14 |
| state_flags_and_strengths | true |
| spread | `obs::spread_rel` |
| session_clock | true |
| self_state | goal, floor, dist_to_goal/floor, ratchet, win_rate, streak, open_risk, position, unrealized, bars_in_trade, trades_used |
| sauces_observation_only | dimension_jump, mcflurry |
| include_signal_agent_slots | false → 1820 PROVEN; true → ~6820 NEW |

---

## 5) Control chain (how sets + obs are used)

```text
FORCE (HTF last two of each set) → REGIME → allowed side + m_regime
        ↓
VELOCITY (LTF first) → breath (wait) vs aligned/launch (fire)
        ↓
ENTRY only if side(force)==side(setup) AND heat/daily risk OK
        ↓
Regime shift → flatten / HOLD / m→0
```

Bread-and-butter: **pullback on LTF while both HTF supports stay strongly trending** → wait loaded → fire on resume with tide.

---

## 6) Lab source paths (absolute)

| What | Path |
|------|------|
| Mark full obs code | `C:\Users\user\Fable5_Foundation\MOMENTUM_ONE\the-truth\lineages\adaptive_rl_brain_7_31_26\perception\observation_full.py` |
| Channel1 | `...\perception\observation.py` |
| Sets law | `...\perception\sets.py` |
| TF config | `...\configs\timeframes.yaml` |
| Features config | `...\configs\features.yaml` |
| Signal slots | `...\configs\signal_slots.yaml` |
| 92 agents index | `...\code\signals\00_ALL_92_AGENTS.md` |
| Policy = Mark card | `...\POLICY_EQUALS_MARK_ON_CHART.md` |

Copies of TF + feature configs also under this kit:

- `knowledge/lab/configs/timeframes.yaml`
- `knowledge/lab/configs/features.yaml`
- `knowledge/lab/configs/signal_slots.yaml` (if present)

---

## 7) Quick JSON twin

See sibling: **`FULL_OBS_AND_TIMEFRAME_SETS.json`**

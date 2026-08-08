# MASTER ARCHITECTURE — promoted laws

Append-only tracker of PROMOTE rulings.

## PROMOTED — CASE-0001 (2026-08-07)

**Law A1 — Meta-RL state composition**  
`META_RL_DIM = 176 = Mark-full 168 + goal/risk context 8`.  
Mark-168 layout preserved. Additive context is non-saturating over target [5,90] and risk [1,3].

**Law A2 — Inference-time goal/risk (clarified by A14)**  
`target_percent` and `max_daily_risk_percent` enter only via `encode_goal_risk_context` / state packing.  
**At inference / prove / forward:** `train_step` / `meta_update` forbidden; weight fingerprint stable across pairs.  
**Does not mean** “never train.” A permanent meta-trained policy is required (A14).

**Law A3 — MARK SETS LAW**  
Official stacks immutable: `1m,15m,30m · 5m,30m,1h · 15m,1h,4h · 30m,4h,1d`.  
Pinned by `assert_mark_sets_law()` in Court package.

**Law A4 — Risk envelope**  
Daily sizing uses remaining budget with friction reserve.  
Worst-case daily loss must not exceed declared `max_daily_risk_percent`.

**Law A5 — Learn-to-learn**  
Roles assigned by family×port templates, not indicator names.  
Rename / family-swap / novel composition must preserve topology/roles.  
High act match + chance topology/role ⇒ `COPYING_FAIL`.

**Law A6 — Emergent senses**  
Sight / feel / taste / hearing implemented as relational probes on multi-TF structure, dual clocks, composition validity, regime/wait subtypes.

### Code paths

| Module | Path |
|--------|------|
| State | `evidence_court/meta_rl/state.py` |
| Goal/risk | `evidence_court/meta_rl/goal_risk.py` |
| Obs/sets | `evidence_court/meta_rl/observation.py`, `sets.py` |
| Policy | `evidence_court/meta_rl/policy.py` |
| Risk | `evidence_court/meta_rl/risk.py` |
| L2L roles | `evidence_court/meta_rl/roles.py` |
| Senses | `evidence_court/meta_rl/senses.py` |
| Forward eval | `evidence_court/meta_rl/forward_eval.py` |
| CLI | `evidence_court/meta_rl/cli.py` |
| Tests | `evidence_court/tests/` |

## PROMOTED — CASE-0002 (2026-08-07) Creator v. Mark — multi-TF edge

**Law A7 — Multi-TF pullback/continuation edge (hint edge)**  
Official Mark sets: HTF force (confirmation TFs) + LTF RSI(5)+BB(10, dev=0.5, shift=+2)  
for `pullback_resume` and `continuation`. Scan all 4 sets. No LTF side without HTF agree.

**Law A8 — Flea-jar full action space in sim**  
- Leverage **1:100** in `risk_legal_max_lot`  
- Multi-symbol concurrent book (XAUUSD, EURUSD, GBPUSD)  
- Aggregated daily risk ledger across symbols  
- Pullbacks **and** continuations covered (measured counters)

**Code:** `indicators.py`, `edge.py`, `leverage.py`, `price_io.py`, `forward_eval.py`  
**Mark NEW tests:** `tests/test_mark_kag_case0002_new.py`  
**Transcript:** `cases/COURT_TRANSCRIPT_0001_0002.md`

## PROMOTED — CASE-FORWARD-100 (re-measured multi-symbol multi-TF)

**Law A9 — 100-forward-day gate (sim/shadow)**  
- `n_days=100`, `breach_count=0`, `no_retrain=true`  
- `multi_symbol=true`, `leverage=100`, `pullback_continuation_coverage=true`  
- pb signals=18, cont signals=162; all three symbols traded  
- Day-path L2L + senses; goal-consistency non-vacuous (hits on 5% band)  
- No look-ahead; no force_side oracle  

**Window:** warmup 2025-12-12; eval 2026-01-06 → 2026-05-26 (common calendar).  
**Label:** `forward_sim_shadow`  
**Artifact:** `evidence_court/artifacts/forward100_report.json`  
**Artifact SHA256:** `23f1bc438b061317ac41948a05f88706d8ecdbd0729cdf31aba524a8eb909754`

## PROMOTED — Law A10 PERMANENT (2026-08-07) — Adversarial Rounds

**Status: PERMANENT COURT LAW** (human order: Monty — make permanent).  
**Not a one-off procedure note.** Binding on every future case until superceded by a later PROMOTE + Monty approval.

**Law A10 — Creator strongest internet + Mark strongest knowledge; one counter each**

| Side | Opening | Proof | Counter (max 1) |
|------|---------|-------|-----------------|
| Creator | Strongest argument from the **internet** | **New test** | One counter-argument + **newer** test (or waive) |
| Mark Here, Esq. | Strongest argument from **his knowledge** | **New test** | One counter-argument + **newer** test (or waive) |

- Soft/placeholder openings → Judge redoes that opening.  
- Old suite greens / prior KAG alone / rank → **not** proof.  
- **No second counter** → Judge **STRIKE**.  
- Then Critic → Optimist → Judge IRAC.

**Canonical:** `ADVERSARIAL_ROUNDS_LAW.md` · machine pin `ADVERSARIAL_ROUNDS_LAW.json`  
**Auto-load:** root `AGENTS.md` · `.grok/rules/00_adversarial_rounds.md`  
**Test pin:** `tests/test_adversarial_rounds_law.py`  
**Mark presentation:** `../mark_here/ESQUIRE.md`  
**Protocol:** `../grok_cli_evidence_court_v2.md` §2a–2b, §4  

## ADMITTED — CASE-0003 (2026-08-07) Goal path (not final PROMOTE yet)

**Law A11 (provisional / admitted):** Goal-conditioned multi-leg day path  
- Module: `meta_rl/goal_path.py`  
- Multi-slot M1 decisions with `asof_date`+`asof_time` (no look-ahead)  
- Goal-conditioned sizing from remaining target under daily risk envelope  
- Random target×risk matrix in `forward_eval` (`pair_mode=random`)  
- **Final PROMOTE deferred** until `promote_ready` (consistent hit rates on 100d)

## PROMOTED (narrow) — CASE-0004 (2026-08-07) A10 Court

**Law A12 — HTF completed-only confirmation (intraday decisions)**  
When decision has `asof_time`, HTF confirmation bars use **date < asof_date** only (no incomplete same-day 1d/4h force).  
Unit pin: `tests/test_case0004_edge_quality.py::test_creator_new_htf_excludes_same_day_when_asof_time`  
Code: `edge._htf_completed_only`

**NOT promoted from CASE-0004 (measured fail on hit rate):**  
- Multi-day momentum as automatic win law  
- Goal-lock fill as consistent-clear solution  
- Final-boss promote_ready (hits=3, low_hr=0.08 after experiment)

**Process:** F-007 — no major decisions without A10 Court.

## PERMANENT — Law A30 (2026-08-07) — Full-project checklist schedule (Monty)

**Status: PERMANENT.**  
**Phase 1 — Creator:** whole-project checklist → **each item full Court**.  
**Phase 2 — Mark:** whole-project + **KAG** checklist → **each item full Court** (only after Phase 1 complete).

**Files:** `schedules/SCHEDULE.md` · `CREATOR_GOAL_CHECKLIST.md` · `MARK_GOAL_CHECKLIST.md`  
**Canonical:** `FULL_PROJECT_CHECKLIST_LAW.md` · pin `tests/test_full_project_checklist_law.py`

## PERMANENT — Law A29 (2026-08-07) — Brain L2L + serious train (Monty, no Judge)

**Status: PERMANENT OWNER ORDER.** Real multi-layer meta-brain; learn-to-learn;  
`brain_drives=True` day path; hard rules are not the decider; risk envelope still hard.  
London/NY: plenty of PB/cont for ≥8 trades — **no excuse**. Retrain champion after this law.

**Code:** `meta_rl/brain.py` · `policy.py` · `goal_path.brain_drives`  
**Canonical:** `BRAIN_L2L_LAW.md` · tests `test_brain_a29.py`

## PERMANENT — Law A28 (2026-08-07) — Opportunity Watch + senses docket (Monty)

**Status: PERMANENT.** Always-on **Opportunity Watch Agent**.  
Missed HTF-trend + LTF RSI/BB pullback/continuation → **complaint** (how to sense next).  
Multi-complaint cases OK. **London/NY** priority. Long-term performance.

**Next cases:** CASE-0031 Sight → 0032 Feel → 0033 Taste → 0034 Hearing  
**Canonical:** `OPPORTUNITY_WATCH_LAW.md` · `SENSES_CASE_DOCKET.md` · `meta_rl/opportunity_watch.py`  
**Test:** `tests/test_opportunity_watch_law.py`

## PERMANENT — Law A15 (2026-08-07) — Counsel to the Court (Monty)

**Status: PERMANENT COURT LAW.**  
Human order: Monty — Counsel helps Judge deliberate; internet sift for best policy; Judge views **all 3 opinions + evidence**.

**Law A15 — Counsel to the Court**

| Field | Value |
|-------|--------|
| Role | **Counsel** — sift **internet** for **best possible policy** |
| Output | One `counsel_opinion` per case (no production code) |
| Three opinions | **Creator**, **Mark**, **Counsel** — Judge must weigh all |
| Sequence | After counters → Counsel → Critic → Optimist → Judge IRAC |
| PROMOTE without three-opinion deliberation | **Forbidden** |

**Canonical:** `COUNSEL_TO_THE_COURT_LAW.md` · pin `COUNSEL_TO_THE_COURT_LAW.json`  
**Auto-load:** `AGENTS.md` · `.grok/rules/00_counsel.md` · short `COUNSEL.md`  
**Test pin:** `tests/test_counsel_to_the_court_law.py`  
**A10 updated:** counters then Counsel, not Critic alone.

## PERMANENT — Law A14 (2026-08-07) — Meta-policy must be trained

**Status: PERMANENT** (Monty: meta-learning is permanent, not “practice”).  

**Law A14 — Trained goal-conditioned meta-policy**

| Rule | Meaning |
|------|---------|
| Must train | Untrained prior cannot freeze/forward/production |
| Meta permanent | `train_goal_conditioned_meta_policy` / `meta_update` across target×risk band |
| Auto target map | Same weights + different goal context → different behavior |
| No retrain at prove | Fingerprint stable when target/risk changes at inference |
| Champion | `artifacts/meta_policy_champion.npz` via `load_or_train_champion` |

**Canonical:** `META_POLICY_TRAIN_LAW.md` · code `meta_rl/policy.py` · tests `test_meta_policy_train.py`  
**CLI:** `python -m evidence_court.meta_rl.cli meta-train`

## PROMOTED — Law A16 (2026-08-07) — Market ontology (CASE-0015)

**Status: PROMOTED (narrow vocabulary / road signs).**  

**Law A16 — Shared market vocabulary for trained policy + Court**

| Term | Definition (machine) |
|------|----------------------|
| **Winning** | Day PnL % ≥ typed `target_percent` |
| **Passing** | No daily risk **breach** |
| **Momentum** | Signed HTF force (bull/bear/flat) |
| **Regime** | Multi-set consensus + efficiency class |
| **Trigger** | fire_long / fire_short / wait / kill |
| **Pullback** | `pullback_resume` (dip against force → resume with) |
| **Continuation** | aligned with force, no deep dip required |
| **Slingshot load** | wait — do not reverse thrash |
| **Senses** | sight / feel / taste / hearing (relational) |
| **Intuition** | Trained meta-policy attention over senses + state — **not** a hand-authored rule tree |

**Code:** `meta_rl/market_ontology.py` (`term_definitions()` = indicators + Mark TFs)  
**Tests:** `tests/test_case0015_market_ontology.py` + `tests/test_case0015_tf_indicator_bindings.py` (**10/10**)  
**Case:** `cases/CASE-0015-market-ontology.md`  
**Binding rule:** Market structure terms bind **all 4 MARK sets** (LTF + HTF pair) and a named **indicator group** (e.g. pullback → RSI5+BB10 on LTF; momentum → trend_dir on HTFs). Win/pass = scoreboard only.  
**Does not alone:** final-boss hit-rate PROMOTE

## PROMOTED — Law A17 (2026-08-07) — Official regime catalog (CASE-0016)

**Status: PROMOTED (hybrid Creator∪Mark; unit-tested).**

**Law A17 — Production regimes (8)**

| RegimeId | Meaning |
|----------|---------|
| `trend_bull` / `trend_bear` | Multi-set HTF agree long/short |
| `range_chop` | No directed multi-set force / chop |
| `conflict` | Sets disagree → kill new risk |
| `incomplete` | Weak/missing HTF agreement → wait |
| `vol_expansion` | High efficiency + directed force |
| `vol_compression` | Low efficiency / dead tape → kill |
| `transition` | Directed force but incomplete consensus |

**Binding:** Each regime uses **all 4 Mark sets** HTFs (`trend_dir` / multi_set_consensus) + efficiency group where listed.  
**Who won:** Hybrid catalog (internet names + Mark multi-set eyes) — neither side alone.  
**Code:** `meta_rl/regimes.py` · `classify_regime_court` · tests `test_case0016_regimes.py`  
**Does not alone:** final-boss hit-rate; day-path wire is a later case.

## PROMOTED — Law A18 (2026-08-07) — Regime-aware meta curriculum (CASE-0017)

**Status: PROMOTED (narrow curriculum road).**  

**Law A18 — Meta curriculum samples A17 regimes and labels with fire/kill playbook**

| Rule | Meaning |
|------|---------|
| Coverage | Curriculum samples **all 8** `RegimeId` (uniform) |
| Teacher | `teacher_action_under_regime`: kill / no-fire → **wait**; allow → goal-conditioned side |
| Sensors | `regime_sensor_template` + `build_official_for_regime` consistent with `classify_regime_court` |
| Dim | **META_RL_DIM = 176** unchanged (no state cliff this case) |
| Not this case | goal_path thrash dials; dual clears+A13 scoreboard; live day-path regime channel |

**Code:** `meta_rl/regimes.py` (curriculum block) · `meta_rl/policy.py` `sample_training_state` / `teacher_action_for_state(regime=)`  
**Tests:** `tests/test_case0017_regime_curriculum.py` (**4/4**)  
**Case:** `cases/CASE-0017-regime-curriculum.md`  
**Does not alone:** final-boss hit-rate / promote_ready

## PROMOTED — Law A19 (2026-08-07) — Day-path regime channel (CASE-0018)

**Status: PROMOTED (narrow inference channel).**  

**Law A19 — A17 regime is packed into Mark doctrine at day-path inference**

| Rule | Meaning |
|------|---------|
| Packer | `encode_regime_doctrine` → 16-dim doctrine (one-hot + allow + kill + force + efficiency) |
| Source | `regime_from_edge_sensors` = `classify_regime_court` on snap consensus/force/efficiency proxy |
| Day path | `goal_path` packs `doctrine_vec` into `build_meta_rl_state`; kill regimes skip new risk |
| Train align | A18 `sample_training_state` uses **same** packer |
| Dim | **META_RL_DIM = 176** unchanged (doctrine is inside Mark-168) |

**Code:** `meta_rl/regimes.py` (CASE-0018 block) · `goal_path.py` wire · `policy.py` curriculum doctrine  
**Tests:** `tests/test_case0018_daypath_regime.py` (**4/4**)  
**Case:** `cases/CASE-0018-daypath-regime-channel.md`  
**Does not alone:** final-boss hit-rate / dual A13+clears

## PROMOTED — Law A20 (2026-08-07) — Dual-safe residual API (CASE-0019)

**Status: PROMOTED (narrow residual **helpers** only).**  

**Law A20 — Residual micro/multi helpers: profit-gate + continuation-only options**

| Rule | Meaning |
|------|---------|
| Anchor | First fill(s): scale 1.0, 1 symbol |
| Residual multi | Only if `realized_pnl > 0` after anchor (when profit_gate) |
| Residual size | Micro only if profit **and** topology=`continuation` (when both gates) |
| API | Defaults CASE-0013-compatible; day path may opt in |

**CASE-0020 measure (F-020):** Full day-path dual-gate **REJECT** dual win — a13_frac **0%**, hits flat 2.  
Helpers remain; **full dual-gate is not production dual path.**

**Code:** `residual_leg_allowed` · gated scale/symbols · `goal_path` (experimental dual-gate wire)  
**Tests:** `tests/test_case0019_profit_residual.py`  
**Cases:** `CASE-0019-profit-gated-residual.md` · `CASE-0020-a20-dual-measure.md`

## PROMOTED — Law A21 (2026-08-07) — One-sym full-scale + multi-set edge floors (CASE-0021)

**Status: PROMOTED (narrow production path geometry).**  

**Law A21 — Production day path uses 1-symbol full-scale legs + multi-set real force floors**

| Rule | Meaning |
|------|---------|
| Symbols | `production_symbols_per_slot() == 1` (no residual multi) |
| Size scale | `production_leg_size_scale == 1.0` always (no F-020 zero-scale) |
| Force floors | `real_edge_force_min` lower when multi-set agrees; always >0 |
| Hold | CASE-0012 asymmetric (pb EOD / cont next slot) |
| Regime | A19 doctrine channel + conflict kill kept |
| A20 | Lab residual API remains; **not** production multi residual |

**Code:** `goal_path.py` production_* + real_edge_force_min + day path wire  
**Tests:** `tests/test_case0021_one_sym_edge_density.py` (**4/4**)  
**Case:** `cases/CASE-0021-one-sym-edge-density.md`  
**Measured CASE-0022 (seed=42):** breach **0**, hits **3**, low_hr **0.08**, a13_frac **7%**, mean_tr **2.43**, promote **false**.  
**ADMIT** as production road baseline; dual/final-boss **not** met.  
SHA256: `e1b830dd9205ef8456a4145b3c94a5b8f56bbcd613f55b778886c51c8165c91b`

## PROMOTED — Law A22 (2026-08-07) — Dense real cadence + multi-set cont window (CASE-0023)

**Status: PROMOTED (narrow A13 density geometry; dual unmeasured).**  

**Law A22 — Production decision clock 15m; continuation may fire mid-band when multi-set agrees**

| Rule | Meaning |
|------|---------|
| Production slots | `PRODUCTION_SCALPING_SLOTS` = 15m grid 07–20 (empty skip, no pad) |
| Lab 30m pin | `SCALPING_CADENCE_SLOTS` unchanged (CASE-0011 tests) |
| Cont prime | Still session-ok (force floor separate) |
| Cont extended | multi-set agree + \|force\|≥0.35 + hour∈[8,18] |
| Thin late | 19:00 cont still blocked |
| Keep | A21 1-sym full-scale; A19 regime; 0012 hold |

**Code:** `PRODUCTION_SCALPING_SLOTS` · `continuation_session_ok` · `run_goal_path_day` default  
**Tests:** `tests/test_case0023_dense_real_edges.py` (**4/4**)  
**Case:** `cases/CASE-0023-dense-real-edges.md`  
**Measured CASE-0024 (seed=42):** breach **0**, hits **7**, low_hr **0.20**, a13_frac **19%**, mean_tr **3.63**, promote **false**.  
Pareto lift vs A21 (hits 3 / a13 7%). **ADMIT** measured density path; dual/final-boss **not** met.  
SHA256: `4aa8a76bd6caa91ca9e490a9dede1cc3a811e8971a4b6d54d8051d6ac1a59803`

## REJECTED — dense NYLON prime as dual lever (CASE-0025 / F-021)

**Not PROMOTED.** Expanding `is_prime_session_slot` to hours [12, 16] unit-pinned but **measured null** vs A22 (identical 100d scoreboard). A22 multi-set extended already covers overlap. Session re-label ≠ dual climb. Helpers may remain; do not treat as win law.

**Code:** `PRIME_BAND_HOUR_*` · `is_prime_session_slot` band  
**Tests:** `tests/test_case0025_dense_nylon_prime.py`  
**Case:** `cases/CASE-0025-dense-nylon-prime.md`

## REJECTED — multi-set force densify as dual lever (CASE-0026 / F-022)

**Not PROMOTED.** Multi-set-only force floors densified (pb/ct/first/CONT_EXTENDED/entry multi); non-multi unchanged; units green. Measure: hits **7** / low_hr **0.20** flat; a13 **19→20%**; mean_tr **3.63→3.66**; breach **0**. Near-null dual. Floors may remain as experimental path; **not** win law.

**Code:** denser multi-set branches in `real_edge_force_min` / `first_entry_cont_force_min` / `CONT_EXTENDED_FORCE_MIN` / `MULTI_SET_CONT_ENTRY_FORCE_MIN`  
**Tests:** `tests/test_case0026_multiset_force_densify.py`  
**Case:** `cases/CASE-0026-multiset-force-densify.md`  
**SHA256:** `08988733f6411d1b9545e9c4db00d37a07bdb9f2acc6fdbd28cf7f9e672a255e`

## PROMOTED — Law A25 (2026-08-07) — Production 10m decision clock (CASE-0027)

**Status: PROMOTED (narrow A13 density geometry; dual unmeasured as final-boss).**  

**Law A25 — Production decision clock 10m; empty skip; 15m/30m pins retained**

| Rule | Meaning |
|------|---------|
| Production slots | `PRODUCTION_SCALPING_SLOTS` = 10m grid 07–20 |
| 15m pin | `PRODUCTION_SCALPING_SLOTS_15M` (CASE-0023) |
| Lab 30m | `SCALPING_CADENCE_SLOTS` unchanged |
| Keep | A21 1-sym; A22 multi-set cont; A19 regime; 0012 asymmetric hold |

**Measured CASE-0027 (seed=42):** breach **0**, hits **7**, low_hr **0.20**, a13_frac **27%**, mean_tr **4.94**, max_pnl **50** (↓ vs 70 on 15m — cont next-slot shorter).  
**ADMIT** density lift vs 0026; dual/final-boss **not** met.  
SHA256: `554ccdf4b985c2fd9cf59884f5d024f46b840365c9f98c4e55a2cacccb12dde2`  
**Code:** `PRODUCTION_CADENCE_INTERVAL_MIN` · `PRODUCTION_SCALPING_SLOTS` · `PRODUCTION_SCALPING_SLOTS_15M`  
**Tests:** `tests/test_case0027_production_10m_clock.py`  
**Case:** `cases/CASE-0027-production-10m-clock.md`

## PROMOTED — Law A26 (2026-08-07) — Cont min hold 30m path (CASE-0028)

**Status: PROMOTED (narrow hold-R geometry on A25 clock).**  

**Law A26 — Continuation fill path holds until first slot ≥ entry + 30 minutes; pullback EOD**

| Rule | Meaning |
|------|---------|
| Cont hold | `CONT_HOLD_MIN_MINUTES = 30` via `next_slot_end_after_minutes` |
| Pullback | EOD (CASE-0012 kept) |
| 30m lab | +30m = next slot (0012 pin) |
| Not | F-011 BE/partial exit floors; not residual multi |

**Measured CASE-0028 (seed=42):** breach **0**, hits **9**, low_hr **0.24**, a13_frac **27%** (held), mean_tr **5.01**, max_pnl **70** (restored).  
Pareto lift vs A25 (hits 7→9, low_hr 0.20→0.24, max_pnl 50→70). Dual/final-boss **not** met.  
SHA256: `2d919bfe4649bd3dfb63f8d0aee6e8fb328fd437add0dc2a1518fd3876ba5cbf`  
**Code:** `CONT_HOLD_MIN_MINUTES` · `next_slot_end_after_minutes` · `fill_hold_end_time`  
**Tests:** `tests/test_case0028_cont_hold_r.py`  
**Case:** `cases/CASE-0028-cont-hold-r.md`

## PROMOTED — Law A27 (2026-08-07) — Production 5m decision clock (CASE-0029)

**Status: PROMOTED (narrow A13 density geometry under A26 hold).**  

**Law A27 — Production decision clock 5m; empty skip; 10m/15m/30m pins retained; A26 cont hold kept**

| Rule | Meaning |
|------|---------|
| Production slots | `PRODUCTION_SCALPING_SLOTS` = 5m grid 07–20 |
| 10m pin | `PRODUCTION_SCALPING_SLOTS_10M` (A25) |
| 15m / 30m | CASE-0023 / CASE-0011 pins |
| Hold | A26 cont min 30m; pullback EOD |
| Keep | A21 1-sym; multi-set cont; A19 regime |

**Measured CASE-0029 (seed=42):** breach **0**, hits **11**, low_hr **0.28**, a13_frac **28%**, mean_tr **7.27**, max_pnl **70** (held).  
Pareto lift vs 0028 (hits 9→11, low_hr 0.24→0.28, mean_tr 5.01→7.27). Dual/final-boss **not** met.  
SHA256: `001b72cae9d1c90353d03fc44b7039e186eceaa9efa5f5e7db931eb9726484e3`  
**Code:** `PRODUCTION_CADENCE_INTERVAL_MIN=5` · `PRODUCTION_SCALPING_SLOTS` · `_10M` pin  
**Tests:** `tests/test_case0029_production_5m_clock.py`  
**Case:** `cases/CASE-0029-production-5m-clock.md`

## PERMANENT — Law A13 (2026-08-07) — Scalping cadence (**Monty overrules Judge**)

**Status: PERMANENT OWNER LAW — hard mandate.**  
Human order: Monty — **overrules the Judge**. Not optional. Not “may.”

**Law A13 — Scalping bot MUST take 8–400 trades every day**

| Field | Value |
|-------|--------|
| Bot class | **Scalper** |
| Daily trades | **MUST ∈ [8, 400]** — outside band = **A13 breach** |
| Lots | Variable under risk envelope; risk **breach 0** hard |
| 5 coarse slots (`DEFAULT_SLOTS`) | **Non-compliant** production path (cannot hit min 8) |
| Owner vs Judge | Monty overrule stands; Judge may not soften MUST → may |
| How to hit the band | Measured **A10** path work still required; **obligation** is already law |

**Canonical:** `SCALPING_CADENCE_LAW.md` · machine pin `SCALPING_CADENCE_LAW.json`  
**Auto-load:** root `AGENTS.md` · `.grok/rules/00_scalping_cadence.md` · `GOAL.md`  
**Test pin:** `tests/test_scalping_cadence_law.py`  
**Helpers:** `a13_trade_count_ok` / `assert_a13_trade_count`  
**Flea-jar:** path that cannot land ≥8 trades = **non-compliant**, not a measured ceiling.

### Not promoted

- Live MT5 order placement / human production deploy  
- Replacement of PROVEN 1820 / SIGON ~6820  
- Unbounded training loops  
- Frictionless results as production-ready  
- Final-boss consistent random-target 100d clears (CASE-0003 still open)  
- Full scalping decision clock / path that **lands** 8–400 trades/day (A13 **must** is law; **implementation still open under Court**)

## PERMANENT — Law A31 (2026-08-07) — Goal is north star (Monty)

**Status: PERMANENT.**  
Every Court case/issue must map to goal axes. Mission: one bot, any target×risk at inference, no retrain after final policy, breach 0, scalping 8–400/day, senses drive brain.  
**Canonical:** `GOAL_LAW.md` · pin `GOAL_LAW.json` · test `tests/test_goal_law.py` · auto-load `.grok/rules/00_goal_law.md`

## PERMANENT — Law A32 (2026-08-07) — Emergent senses full stack (Monty)

**Status: PERMANENT.**  
Sight / Feel / Taste / Hearing on every official MARK set with explicit fail modes. Production rule: pack into state and train brain — not probe-only.  
**Canonical:** `EMERGENT_SENSES_LAW.md` · pin `EMERGENT_SENSES_LAW.json` · docket `SENSES_CASE_DOCKET.md` · test `tests/test_emergent_senses_law.py` · auto-load `.grok/rules/00_emergent_senses.md`  
**Series:** CASE-0031 → 0032 → 0033 → 0034

## PERMANENT — Law A33 (2026-08-07) — Goal-relative Court process (Monty)

**Status: PERMANENT.**  
Court never stops until final boss. Generates new issues from measured G-* gaps. Tiered Full vs Summary Court. Evidence ledger + scoreboard history + counsel cache + precedent cards.  
**Canonical:** `GOAL_RELATIVE_COURT_LAW.md` · pin `GOAL_RELATIVE_COURT_LAW.json` · test `tests/test_goal_relative_court_law.py` · auto-load `.grok/rules/00_goal_relative_court.md`  
**Retention:** `ledger/EVIDENCE_LEDGER.jsonl` · `ledger/SCOREBOARD_HISTORY.jsonl` · `ledger/COUNSEL_CACHE.jsonl` · `precedents/`


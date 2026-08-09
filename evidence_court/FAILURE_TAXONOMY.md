# FAILURE TAXONOMY — rejected / defeated hypotheses

Append-only. Failure is data.

## F-001 — Legacy self_state target encoding as sole goal channel

- **Hypothesis:** Mark `pack_self_state` `target_pct/5` is sufficient for [5,90] band.
- **Why failed:** Saturates at target≥5% → 5% and 90% look identical in self_state[6].
- **Regression pin:** `test_legacy_self_state_saturates_but_context_does_not`
- **Remedy:** Additive `encode_goal_risk_context` (PROMOTED CASE-0001).

## F-002 — Retrain-on-new-pair (inference)

- **Hypothesis:** New target/risk requires gradient update **at inference**.
- **Why failed / blocked:** Violates GOAL.md; during frozen prove/forward `train_step` / `meta_update` raise.
- **Regression pin:** `test_trained_policy_no_retrain_between_pairs`
- **Clarified (A14):** Offline permanent meta-train across the target band is **required**. F-002 only blocks inference retrain.

## F-016b — Untrained seed stub as production policy

- **Hypothesis:** `FrozenMetaPolicy.from_seed` random prior without meta-train is a usable brain.
- **Why failed:** Policy never learned goal-conditioned fire/size map; “no retrain” was misread as “never train.”
- **Remedy:** Law A14 — `train_goal_conditioned_meta_policy` / `load_or_train_champion`; untrained cannot freeze/forward.

## F-003 — Act-only copying as learning

- **Hypothesis:** High act accuracy implies understanding.
- **Why failed:** Topology/role at chance ⇒ COPYING_FAIL.
- **Regression pin:** `test_copying_fail_detection`

## F-004 — Double-counted closed losses in risk ledger

- **Hypothesis:** sum(adverse_realized + closed_losses) is correct worst-case.
- **Why failed:** Double-counts same loss after `apply_trade_result`.
- **Remedy:** `max(adverse_realized, closed)` in `worst_case_daily_loss_percent`.

## F-005 — Same-day close look-ahead in forward eval

- **Hypothesis:** Using full-day OHLC/return for both decision and fill is acceptable shadow.
- **Why failed:** Skeptic: decision must be pre-close; same-day close is look-ahead.
- **Remedy:** `decision_features_from_history(prior only)`; fill `open→close_or_stop`.

## F-006 — force_side oracle bypassing Meta-RL state

- **Hypothesis:** Injecting force_side in forward path is fine for speed.
- **Why failed:** PROMOTE path never exercised observation→policy direction.
- **Remedy:** Removed `force_side`; act from Channel1 set dirs in state only.

## F-007 — Major path/edge changes without Evidence Court (process defect)

- **Hypothesis:** “Resume and improve hit rate” licenses free code edits without A10.
- **Why failed:** Violates permanent Law A10 + Monty order: Creator internet + new test, Mark knowledge + new test, one counter each, Judge measurement — **evidence only**. Invented dials are not Court.
- **Remedy:** `CASE-0004` reopened under full A10; `AGENTS.md` “Court before major decisions”; experimental code quarantine until unit + 100d measure + IRAC PROMOTE.
- **Regression pin:** case file must exist with `creator_opening` / `mark_opening` / counters before PROMOTE of new edge/path laws.

## F-007 — Disconnected unit L2L as forward L2L proof

- **Hypothesis:** Calling novel_composition once after the loop proves day-path L2L.
- **Why failed:** Not on the shipped day decision path.
- **Remedy:** rename/swap/novel + senses probes inside `run_one_day` every day.

## F-008 — Vacuous goal hit rates (max PnL ≪ targets)

- **Hypothesis:** breach=0 alone proves goal-consistency across 5–90.
- **Why failed:** hit_rate=0 by construction when ticket×R-cap < target.
- **Remedy:** R-multiple fill + envelope utilization; measure hit_rate/progress; gate promote on non-vacuous goal_consistency.

## F-009 — Mark proving principles with old suite only

- **Hypothesis:** Prior CASE-0001 greens suffice for CASE-0002 Mark counters.
- **Why failed / blocked:** Court v2 — Mark must file **NEW tests** for new principles.
- **Remedy:** `test_mark_kag_case0002_new.py` (HTF permission, four-set scan, multi-symbol ledger, 1:100 lots).

## F-010 — “90% target impossible”

- **Hypothesis:** Narrative that high targets cannot clear under 1–3% risk.
- **Why failed as law:** Flea-jar — no impossibility without full-action-space bound. This window **measured** hit_rate@90=0; that is a **scoreboard fact**, not a nature ceiling claim.

## F-011 — Full BE trail (1.5R) + pullback expect_r=1.0 as clear path (CASE-0006)

- **Hypothesis:** Breakeven after +1.5R plus sizing pullback for 1.0R clear raises hits/low_hr on 100d random.
- **Why failed:** seed=42 measure hits **3→2**, low_hr **0.08→0.04**; breach stayed 0. Full BE scratches runners that retest entry before goal_lock; larger pullback tickets increase full-stop days when path never reaches 1.5R.
- **Remedy:** Prefer **partial** progressive goal lock (bank fraction of rem_goal at intermediate R, leave runner) or raise mean favorable R via slot/entry quality — under new A10 case. Do not PROMOTE full BE as win law.

## F-012 — Half-rem_goal partial floor alone as clear climb (CASE-0007)

- **Hypothesis:** `partial_lock_frac=0.5` (trail off) raises hits/low_hr above CASE-0005 on 100d random.
- **Why failed:** seed=42 hits **3**, low_hr **0.08** — recovered F-011 regression only; no climb past 0005. Half rem_goal is often unreachable on a single ticket when rem_goal ≫ size×achievable R.
- **Remedy:** Size-R-based partial bank (e.g. floor at +1.0R floating) and/or slot/entry quality under CASE-0008 A10. Do not PROMOTE rem_goal-frac-only as win law.

## F-013 — Size-R progressive floor alone as clear climb (CASE-0008)

- **Hypothesis:** Bank ~1.0R floating (`size_r_arm_r=1.0`) raises hits/low_hr on 100d random.
- **Why failed:** seed=42 hits **3**, low_hr **0.08** — slight mean-progress bump only; hit count flat. Exit-floor family (full BE / rem_goal frac / size-R) exhausted as sole lever.
- **Remedy:** **Slot/entry R quality** (session phase, stronger session confirm, pullback-first slot priority, residual multi-leg after banked R) under CASE-0009 A10. Stop pure exit-floor dials without entry hypothesis.

## F-014 — Slot/entry quality gates alone as clear climb (CASE-0009)

- **Hypothesis:** Prime session slots + min_align session confirm + entry_quality_ok raise hits/low_hr.
- **Why failed:** seed=42 hits **3→2**, low_hr **0.08→0.04**, low_fire **0.32→0.28**. Same class as CASE-0005: entry shrink without more favorable R on remaining paths.
- **Remedy:** Prefer levers that **increase** day-PnL path capacity under **A13 scalping band [8, 400]** — not another pure gate on a 5-slot lid.

## F-015 — Five coarse decision slots as production day path (A13 non-compliance)

- **Hypothesis / silent assumption:** `DEFAULT_SLOTS` (5 clock times) is the production day path for clear-rate / final-boss work.
- **Why failed as law:** Monty **Law A13** (overrules Judge) — bot **MUST** take **8–400 trades every day**. A ~5-decision path **cannot** hit min 8 → **A13 breach** as production identity; flea-jar incomplete.
- **Remedy:** Dense multi-leg scalping path under A10 that **lands** trades in **[8, 400]** every day (and ≤400 hard cap). Lab may still run 5-slot shadow **only if labeled non-compliant**. Pin: `SCALPING_CADENCE_LAW.md` / `a13_trade_count_ok` / `tests/test_scalping_cadence_law.py`.

## F-016 — Bundled pullback carve-out + next-slot path (CASE-0010)

- **Hypothesis:** Pullback single-set path permission + fill-to-next-slot multi-leg raises hits/low_hr.
- **Why failed:** seed=42 hits **2**, low_hr **0.04** (flat vs 0009); low_fire **0.28→0.40** (capacity yes, clears no). Short windows likely truncate R while carve-out adds entries — confound. Also sits under F-015: still only 5 decision slots vs A13 8–400 band.
- **Remedy:** Isolate carve-out with EOD hold (CASE-0011) **and/or** dense scalping cadence under A13 + A10 — not another pure gate.

## F-017 — Dense 30m cadence + multi-symbol without conversion control (CASE-0011)

- **Hypothesis:** SCALPING_CADENCE_SLOTS (27×30m) + max_fills=400 + multi-symbol take raises A13 compliance and hits.
- **Why failed:** seed=42 breach **0**, hits **0**, low_hr **0**; mean n_trades ~3.2; only ~15% days ≥8 trades; low_fire 0.64. Capacity real (max 21) but clears collapsed — denser short holds + more tickets thrash equity before goal_lock.
- **Remedy:** CASE-0012 conversion under dense path (micro-risk residual legs, pullback EOD hold, quality throttle targeting mean≥8 without pad). A13 MUST remains.

## F-018 — Asymmetric hold + 1-symbol recovers hits, cuts A13 share (CASE-0012)

- **Hypothesis:** pullback EOD + cont next-slot + one symbol/slot raises hits and A13 day-share together.
- **Why failed:** hits **0→3**, low_hr **0→0.08** (conversion OK vs F-017) but a13 day-share **~15%→~6%**, mean trades **~3.2→~2.4**. Dual objective unmet.
- **Remedy:** CASE-0013 micro-risk residual legs under dense clock without undoing EOD pullback conversion. A13 MUST remains.

## F-019 — Unconditional micro residual after anchor (CASE-0013)

- **Hypothesis:** after first fill, size×0.25 + multi-symbol residual raises a13 day-share without cutting hits.
- **Why failed:** a13_frac **~6%→~14.5%**, mean_tr **~2.4→~3.1**, but hits **3→2**, low_hr **0.08→0.04**. Residual multi still leaks expectancy.
- **Remedy:** CASE-0019 profit-gated residual (realized_pnl>0) **and** continuation-only residual micro/multi (unit-pinned).  
- **Re-measure CASE-0020:** dual gate kept hits flat but **starved A13** → see **F-020**.

## F-020 — Dual-gated residual starves A13 without lifting hits (CASE-0020)

- **Hypothesis:** Day-path residual only when profit-gated **and** continuation-only raises dual (keeps hits, preserves some a13_frac).
- **Why failed:** seed=42 100d — hits **2→2**, low_hr **0.04**, a13_frac **~14.5%→0%**, mean_tr **~3.1→0.66**, max_tr **21→3**. Conversion not improved; cadence collapsed.
- **Regression pin:** artifact SHA256 `f48743a2a5c8283917718939599699dd3fc669c29ea2561c824f93d8edaa708e`
- **Remedy:** Do not treat full dual residual gate as production dual path. Next: real edge density / 1-sym profit micro only / fill-R — not multi thrash (F-017) and not total residual starve (F-020).

## F-021 — Dense NYLON prime band alone is null under A22 extended (CASE-0025)

- **Hypothesis:** Expanding prime cont session-ok to hours [12, 16] densifies real cont edges in London–NY overlap and raises hits/a13 vs A22.
- **Why failed:** seed=42 100d — scoreboard **byte-identical** to CASE-0024 (hits **7**, low_hr **0.20**, a13 **19%**, mean_tr **3.63**, breach **0**). SHA256 `4aa8a76bd6caa91ca9e490a9dede1cc3a811e8971a4b6d54d8051d6ac1a59803`. A22 multi-set extended already covers hours 8–18 when multi-set + force≥0.35; prime band only adds single-set cont ≥0.40 and multi-set force∈[0.32,0.35) in 12–16 — no extra fills cleared remaining gates.
- **Regression pin:** `tests/test_case0025_dense_nylon_prime.py` (geometry); measure null vs 0024.
- **Remedy:** Do not PROMOTE session re-label as dual lever. Next: multi-set **force densification**, cont **hold-R**, or denser real decision clock (e.g. 10m) under A10 — not pure prime-hour expansion over A22 coverage.

## F-022 — Multi-set force densify near-null dual (CASE-0026)

- **Hypothesis:** Lower multi-set-only force floors (pb 0.12→0.10, ct 0.18→0.15, first cont 0.28→0.24, CONT_EXTENDED 0.35→0.28, entry multi 0.32→0.28) raises hits/a13 vs A22 without pad/thrash.
- **Why failed:** seed=42 100d — hits **7**, low_hr **0.20** (flat); a13 **19%→20%**; mean_tr **3.63→3.66**; breach **0**. Floor held; dual not climbed. Extra multi-set edges in the force slice rarely clear remaining gates.
- **Regression pin:** `tests/test_case0026_multiset_force_densify.py`; SHA256 `08988733f6411d1b9545e9c4db00d37a07bdb9f2acc6fdbd28cf7f9e672a255e`
- **Remedy:** Stop micro force dials as sole dual lever. Next: cont **hold-R** (longer multi-set cont horizon) or **10m real clock** with empty skip — structural R/capacity under A10. No residual multi (F-017…F-020).

## F-023 — Multi-set session min_align ease near-null dual (CASE-0030)

- **Hypothesis:** When multi-set HTF agrees, set session_confirm min_align=0 (else DEFAULT) unlocks silent days / a13 / hits vs A27.
- **Why failed:** seed=42 100d — hits **11**, low_hr **0.28**, a13 **28%** (flat vs 0029); mean_tr **7.27→7.38**; n_zero **41→39**; n_ge8 **28** flat; breach **0**. Multi-set edges already largely cleared default align.
- **Regression pin:** `tests/test_case0030_multiset_session_align.py`; SHA256 `f6fc9b32788d4a85874b704f2fc8017aad794a99d998808f360a870e8fe6bdf4`
- **Remedy:** Do not PROMOTE session-align re-threshold as dual lever. Next: silent-day structural levers (first-entry multi-set cont, regime skip review, curriculum/policy) under A27+A26 — not another near-null gate.

## F-024 — Synthetic denser opportunity-miss curriculum alone (CASE-0035)

- **Hypothesis:** Offline denser London/NY multi-set PB/cont miss teachers + shadow meta-train cuts **n_zero** / raises a13 and dual vs floor without pad.
- **Why failed:** seed=42 100d shadow meta3689 vs champion meta2862 — hits **11** flat; a13 **28%→38%**; mean_tr **7.38→21.15** (active-day densify only); **n_zero 39→45** (silent days **worse**); low_hr **0.28→0.24** (prefer broken, absolute edge); breach **0**. Primary silent-day unlock failed.
- **Regression pin:** `tests/test_case0035_silent_day_opportunity_curriculum.py`; report SHA256 `099268c312335728c0ca53a99998cb3e46f4d91ba70ea367e7a55423c1f80bd4`
- **Remedy:** Do **not** replace PROVEN champion with synthetic-only opp mix. Keep label→train API (C-002 narrow). Next: **real-bar M1 harvest** of Watch `curriculum_labels` (C-002 residual) and/or **C-003** structural every-day A13 density — not another pure synthetic teacher densify.

## F-025 — Real-bar Watch labels + synthetic state rebuild (CASE-0036)

- **Hypothesis:** Harvest dated Watch miss labels from real multi-day path (not pure synthetic teachers) + offline mix raises a13 / cuts n_zero vs floor.
- **Why failed:** seed=42 100d shadow meta4050 — hits **11** flat; a13 **28%→38%**; mean_tr **7.38→21.23**; **n_zero 39→45**; low_hr **0.28→0.24**; breach **0**. Scoreboard **~identical to F-024** despite 300 real-dated labels (237 London/NY). Provenance of asof/force/topo is real, but `opportunity_label_to_training_example` still **rebuilds synthetic official state** — distribution shift vs silent-day decision states remains.
- **Regression pin:** `tests/test_case0036_real_bar_a13_harvest.py`; report SHA256 `efc88555fdaedadf53ee49a2a048d03bd74bdcbdddce359959dd8ad6973b2020`; harvest `artifacts/real_bar_opp_labels_case0036.json`
- **Remedy:** Do **not** replace PROVEN. Keep harvest tooling. Next C-003 lever must be **(state, teacher) pairs from actual path decision states at miss slots** (full packed `build_meta_rl_state` at decision), or structural path geometry for partial days (1–7→8+), or game-train human traj (A34) — not another label→synthetic-state mix.

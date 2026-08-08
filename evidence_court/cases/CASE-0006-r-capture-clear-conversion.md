# CASE-0006 — R-capture / clear conversion (A10 full Court)

**case_id:** CASE-0006  
**status:** CLOSED  
**opened:** 2026-08-07 (scheduled Court fire)  
**closed:** 2026-08-07  
**question:** What **measured** change raises low-band hit_rate and total_hits (R-capture / converting correct-side days into clears) on the same 100d random protocol without breach, retrain, look-ahead, or Mark-law break?

**scope:** `evidence_court/meta_rl/goal_path.py` (exit path + sizing under envelope only); tests; forward eval measurement  
**protected_invariants:** MARK_SETS_LAW; Meta-RL 176; no-retrain; breach envelope; Law A10; A12 HTF completed-only; CASE-0005 experimental gate remains experimental; no live deploy; PROVEN untouched  

**Prior evidence:**
- CASE-0004/0005: breach **0**, hits **3**, low_hr **0.08**, promote_ready false  
- CASE-0005 multi-set confluence: fire rate ↓, hits **unchanged** → permission shrink alone is not the clear lever  
- Bottleneck (checkpoint): convert correct-side days into clears via **exit path / R-capture / pullback-first sizing under envelope**

---

## ROUND STRUCTURE (Law A10) — binding

```
OPENING (Creator internet + new test) → OPENING (Mark knowledge + new test)
→ OPENING TESTS RUN → ONE COUNTER each + newer tests → Critic → Optimist → Judge IRAC
```

---

## Creator opening

### strongest_internet_argument

**Trade-management R-capture: after favorable excursion of ~1.5R, move stop to breakeven so winners that reverse do not become full −1R losers — raising expectancy on the same entry quality.**

Evidence class (not authority):

1. **R-multiple trade management** (Van Tharp design class; retail/quant exit literature): expectancy = p(win)×avg_win_R − p(loss)×avg_loss_R. Cutting winner→full-loser reversals reduces avg_loss_R without new entries.  
2. **Delayed / non-premature BE:** industry writeups warn that BE at tiny open profit (“noise BE”) trims winners and can *hurt* expectancy; arming only after **≥1.5R** is the design class that protects only after genuine progress (ITI “premature breakeven” critique → arm later).  
3. **Goal-conditioned hierarchical control:** remaining subgoal under a hard risk budget — once path has already achieved +1.5R, preserving capital (BE) leaves budget for later slots to finish the day goal.

**claim (falsifiable):** Enabling **breakeven trail after +1.5R** on the M1 path fill (`simulate_fill_m1_path` with `trail=True`, `be_arm_r=1.5`) improves clear conversion vs no-trail on the same entries; unit-proved by synthetic path; measured by 100d random hits/low_hr vs CASE-0005 baseline (hits=3, low_hr=0.08).

**mechanism:** In path loop, once favorable R ≥ 1.5, move stop to entry (breakeven). Subsequent adverse touch of entry exits ~0 (minus friction), not full −size.

**web_evidence (design class):**
- R-multiple expectancy / trade management (Van Tharp design class).  
- Premature-BE critique → arm after structural progress (~1.5R), not noise (ITI Evolving R / common BE rule discussions).  
- Goal-conditioned sequential subgoals under risk budget (hierarchical RL design class — already CASE-0003 admitted).

**prediction:** Unit: +1.6R then reverse through entry → trail PnL ≈ 0 (not −size). Forward: breach stays 0; hit metrics re-measured.

**falsifier:** Trail uses future bars; OR trail arms at &lt;1.0R without order; OR “proof” is only CASE-0005 greens; OR breach &gt; 0.

**new_test (opening):**
- path: `tests/test_case0006_r_capture.py::test_creator_new_be_trail_after_1p5r_saves_reversal`
- why_new: never existed; CASE-0003/0004 tested goal-lock / HTF, not BE trail arm at 1.5R
- result: **PASS**

---

## Mark Here, Esq. — opening

### strongest_knowledge_argument

From **@physics** + pack (context for theory; **not** closing proof):

1. **Pullback_resume is Mark timing law** — LTF RSI5/BB slingshot after HTF force; this is the high-quality release, not thrash continuation.  
2. **R-capture on launch** — after load→release, size so **~1.0R** covers remaining goal when envelope allows (`expect_r=1.0` for pullback_resume), not an over-optimistic 1.6–1.9R that leaves the day short when the market only delivers 1R.  
3. **Envelope first** — size still capped by remaining risk budget; never breach floor.  
4. **Flea-jar** — do not declare clears impossible; convert the same permission days into hits by matching size to achievable R on the quality topology.

**claim:** On `pullback_resume`, goal-path sizing uses **expect_r = 1.0** (size ≈ rem_goal / 1.0 under envelope); continuation stays more conservative (expect_r ≥ 1.35 low / 1.9 high). Proved only by **new** tests this case.

**law_physics:** slingshot_release | r_on_launch | envelope_cap  
**law_belief_paths:** MARK edge timing, risk envelope A4, flea-jar  

**prediction:** Same rem_goal + rem_risk: pullback size ≥ continuation size; pullback size ≤ rem_risk×0.95; never breaches.

**falsifier:** Pullback sized smaller than continuation at same inputs; OR size exceeds envelope.

**new_test (opening):**
- path: `tests/test_case0006_r_capture.py::test_mark_new_pullback_expect_r_one_sizes_for_1r_clear`
- why_new: new pure sizing expect_r pin for pullback vs continuation this case
- result: **PASS**

---

## Creator counter (exactly one)

**counter_argument:** Arming BE at exactly 1.0R is the “premature BE” failure mode (internet expectancy literature). **Arm only at ≥1.5R.** Paths that peak at +1.0R then reverse must still take the hard stop (−size) — trail must not arm early.

**newer_test:** `test_creator_new_be_not_armed_at_1r_only` — peak +1.0R then full reverse → PnL = −size (trail does not save).

**prediction:** arm_r=1.5 blocks premature protect.

**falsifier:** +1.0R peak + reverse returns ~0 with trail on.

**result:** **PASS**

---

## Mark counter (exactly one)

**counter_argument:** Aggressive 1.0R pullback sizing must **never** exceed remaining risk envelope or `would_breach`; if rem_goal ≫ rem_risk, size caps at rem_risk×0.95 (high target still needs multi-R or multi-leg — flea-jar multi-slot path, not silent envelope break).

**newer_test:** `test_mark_new_pullback_size_respects_risk_envelope` — rem_goal=50, rem_risk=2 → size ≤ 2×0.95.

**prediction:** Envelope always wins.

**falsifier:** Size &gt; remaining budget.

**result:** **PASS**

---

## Critic cross-examination

| Check | Status |
|-------|--------|
| Look-ahead | Trail uses only path bars seen so far (high/low of current bar after entry) |
| Flea-jar | Multi-slot path retained; BE only after 1.5R progress |
| Risk | Sizing still envelope-capped; BE cannot increase loss beyond −size |
| No-retrain | Inference-only exit + size rule |
| Premature BE | Arm at 1.5R not noise |
| Process | Full A10 before code land |

**failure_conditions:** breach&gt;0; train_step; PROMOTE without 100d re-measure; silent edge-permission rewrites without case

---

## Optimist challenge

- Same entries as CASE-0005 permission; better exit + pullback 1R sizing can convert near-miss days into hits.  
- 2x test: same seed 100d vs CASE-0005 (hits=3, low_hr=0.08).  
- Threshold: total_hits ≥ 12 OR low_hit_rate ≥ 0.18; breach 0.

---

## Judge pretrial order (written BEFORE experiment)

1. Run all CASE-0006 **new** unit tests; record pass/fail.  
2. **Allowed code (smallest):**  
   - `simulate_fill_m1_path`: implement BE trail when `trail=True` and favorable R ≥ `be_arm_r` (default 1.5).  
   - Wire `trail=True` on goal_path fills.  
   - Pullback_resume `expect_r = 1.0` in day path sizing; continuation unchanged (1.35 low / 1.9 high).  
   - Helpers `clear_expect_r` + `goal_path_size_for_clear` for pure test pin.  
3. **Measurement:**  
   `python -m evidence_court.meta_rl.cli forward100 --days 100`  
   (seed=42, pair_mode=random, goal path) → save `artifacts/forward100_report.json` + SHA256.  
4. **Pass thresholds for win-path PROMOTE consideration:**  
   - breach_count = 0  
   - no_retrain = true  
   - l2l_day_path_ok + senses_day_path_ok  
   - total_hits ≥ 12 OR low_hit_rate ≥ 0.18  
   - unit A10 tests green  
5. **If thresholds fail:** REJECT win-path PROMOTE; may ADMIT BE-trail / pullback expect_r as experimental fragments if units prove logic and breach 0.  
6. **Forbidden:** more undirected dials; permission-gate rewrites; live MT5.

---

## Opening + counter test results (execution record)

Command: `python -m pytest evidence_court/tests/test_case0006_r_capture.py -v`

| Test | Side | Result |
|------|------|--------|
| `test_creator_new_be_trail_after_1p5r_saves_reversal` | Creator opening | **PASS** |
| `test_mark_new_pullback_expect_r_one_sizes_for_1r_clear` | Mark opening | **PASS** |
| `test_creator_new_be_not_armed_at_1r_only` | Creator counter | **PASS** |
| `test_mark_new_pullback_size_respects_risk_envelope` | Mark counter | **PASS** |

**Opening + counter unit evidence:** all 4 NEW tests green (2026-08-07).

---

## Code landed (Judge-ordered smallest experiment)

| Symbol | Path | Role |
|--------|------|------|
| `simulate_fill_m1_path` trail/`be_arm_r` | `meta_rl/goal_path.py` | BE stop at entry after ≥1.5R |
| `clear_expect_r` | `meta_rl/goal_path.py` | pullback→1.0; cont→1.35/1.9 |
| `goal_path_size_for_clear` | `meta_rl/goal_path.py` | envelope-capped clear sizing |
| wire | `run_goal_path_day` | trail=True + new size helper |

**Note:** experimental only — not law after IRAC.

---

## 100d measurement (Judge order step 3)

| Metric | CASE-0005 baseline | After CASE-0006 | Threshold |
|--------|-------------------:|----------------:|-----------|
| n_days | 100 | **100** | ≥100 |
| breach_count | 0 | **0** | =0 |
| no_retrain | true | true | true |
| l2l / senses | true | true | true |
| total_hits | 3 | **2** | ≥12 |
| low_hit_rate | 0.08 | **0.04** | ≥0.18 |
| low_hits | — | **1** | — |
| low_fire_rate | 0.32 | **0.32** | — |
| max_day_pnl | 30.0 | **30.0** | — |
| promote_ready | false | **false** | true for FINAL |

Artifact: `evidence_court/artifacts/forward100_report.json`  
SHA256: `0C8517FAA8CAA25B6E113E616C152A988BDDD9C6F7A8E2F689A8DD5C0DFE2FAA`

**Interpretation:** BE trail after 1.5R + pullback 1R sizing **did not raise clears**. Hits **fell** 3→2; low_hr **0.08→0.04**. Fire rate unchanged (permission path same). Likely: (a) BE after 1.5R **scratches runners** that retest entry before full goal_lock, cutting R that previously locked; (b) larger pullback tickets increase full-stop days when path never reaches 1.5R. Unit logic is correct; win-path hypothesis **falsified** on this seed/window.

---

## Judge IRAC

- **Issue:** May BE trail (1.5R) + pullback expect_r=1.0 be PROMOTED as the consistent-winning clear-conversion path for the final boss?  
- **Rule:** A10 (openings+counters+new tests); flea-jar; no look-ahead; promote thresholds (hits≥12 or low_hr≥0.18; breach 0; no retrain; L2L/senses).  
- **Application:**  
  - Unit evidence **passed** (4/4 NEW tests) — BE saves 1.6R reversal, not armed at 1.0R, pullback expect_r pin, envelope cap.  
  - 100d measure: breach **0**, no_retrain, L2L/senses OK — **safety holds**.  
  - Clear frequency **fails** (hits=2 &lt; 12; low_hr=0.04 &lt; 0.18) and is **worse** than CASE-0005 baseline.  
  - Win-path claim **rejected**. Code may remain as experimental implementation detail for further cases but is **not** promoted law; next case should not treat full BE as the clear lever.  
- **Conclusion:**  
  - **REJECT** win-path PROMOTE for BE trail + pullback-1R as final-boss clear solution.  
  - **ADMIT experimental only** (unit-proved, breach-safe): trail API + `clear_expect_r` / `goal_path_size_for_clear` helpers — **not** MASTER_ARCHITECTURE laws.  
  - **Next:** CASE-0007 — progressive **partial goal lock** (bank fraction of rem_goal at intermediate R without full BE scratch) **or** entry/slot quality that raises mean favorable R before any trail — measured under A10. Do **not** invent dials outside the next case file.

---

## FAILURE_TAXONOMY note

| Tag | Detail |
|-----|--------|
| F-R-CAPTURE-BE-HURT | Full BE after 1.5R + aggressive pullback size reduced hits on seed=42 |
| F-CLEAR-FREQ | Still far from hits≥12 / low_hr≥0.18 |

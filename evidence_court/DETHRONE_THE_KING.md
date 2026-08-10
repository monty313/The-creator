# How to legally dethrone the king (CASE-0037 production champion)

**Status:** PATH ONLY — analysis SSOT for Court-legal production replace  
**Updated:** 2026-08-09  
**Does not claim:** final boss complete · production already replaced · L2L §7 ready  
**Companion SSOTs:** `BEST_POLICY.md` · `ISSUE_DOCKET.md` · `L2L_SERIES_STATUS.md` · `ROAD_FOR_THE_POLICY.md`

---

## 1. Who is the king (current production)

| Field | Value (live SSOT) |
|-------|-------------------|
| **Case** | CASE-0037 path-state teachers |
| **Ruling that crowned him** | **PROMOTE_NARROW** (density lever; **not** final boss) |
| **Weights** | `artifacts/meta_policy_champion.npz` |
| **Fingerprint** | `42:meta4275:inf0:bcfe6c74f68b7623` |
| **Meta-train steps** | 4275 |
| **Load path** | `load_or_train_champion()` → champion npz only |

### BEST_POLICY floor (the numbers a challenger must beat or Court must re-floor)

Protocol that **set** this floor: **forward100** seed=42, 100d (see `artifacts/forward100_report_case0037.json` / `BEST_POLICY.md`).

| Metric | Floor (do not regress without measure) |
|--------|----------------------------------------:|
| hits (target-win days) | **≥ 11** |
| low_hr | **≥ 0.28** |
| a13_frac | **≥ 0.64** |
| n_zero | **≤ 18** |
| breach | **0** |
| no_retrain at inference | **true** |

Day buckets on floor dual: **0:** 18 · **1–7:** 18 · **8–400:** 64 · **>400:** 0.

**King is still king until PROMOTE replaces those weights and this identity block is rewritten.**

---

## 2. Best legal challenger already in-repo (not production)

| Field | Value |
|-------|-------|
| **Case** | CASE-L2L-P10-residual |
| **Ruling** | **ACCEPT_NARROW_LAB** — method + dual vs champ on north-star protocol |
| **Shadow** | `artifacts/meta_policy_l2l_p10_residual.npz` |
| **Fingerprint** | `42:meta10835:inf0:441555412cf1e3ae` |
| **Recipe** | warmstart 0037 → light density process → **path re-anchor last** → freeze |
| **Report** | `artifacts/l2l_p10_residual_report.json` |
| **Production?** | **No** — residual lab status **not production** |

### Measured gap (concrete — what still blocks dethrone)

| Protocol | Challenger | King (same protocol) | Floor hold? |
|----------|------------|----------------------|-------------|
| North-star dual 30d random T×R XAU 15m | hits **3** · a13 **0.33** · n_zero **11** · breach **0** | hits 3 · a13 0.27 · n_zero 11 | n/a (short window) |
| North-star dual 100d same | hits **7** · a13 **0.42** · n_zero **35** · breach **0** | hits 7 · a13 0.41 · n_zero 35 | **false** vs floor 11 / 0.64 / ≤18 |
| BEST_POLICY forward100 floor | *(challenger not yet measured under this protocol as PROMOTE dual)* | hits **11** · a13 **0.64** · n_zero **18** | **king holds floor** |

**Gap summary:** On north-star dual the residual **marginally beats** the king (a13 0.42 vs 0.41, same hits). It still **fails** BEST_POLICY floor by **hits −4**, **a13 −0.22**, **n_zero +17**. That is why production replace is illegal today.

Prior washout shadow `meta_policy_l2l_p2_p10.npz` (process-only, a13 ~0.13) is **not** a legal challenger for promote — process-washout promote is forbidden.

---

## 3. Legal gates (every one required to replace production weights)

Order is binding. Skipping any gate = illegal coup.

| # | Gate | Law / SSOT | What “pass” means |
|---|------|------------|-------------------|
| **G1** | **Full Court case** (not freestyle) | **A10** adversarial + **A15** Counsel; **A31** `goal_axes`; **A33** docket rank | Creator + Mark openings (each + **new test**) → one counter each → Counsel opinion → Critic → Optimist → Judge IRAC naming **three opinions**. Case declares axes (at least G-A13, G-CLEAR, G-TRAIN, G-NO_RETRAIN, G-BREACH0). |
| **G2** | **Offline train only** | **A14** meta-train law; **A29** brain | Challenger weights from offline `meta_update` / curriculum / path-state teachers. **No** weight updates at prove/forward when target/risk changes. |
| **G3** | **Freeze for inference** | A14 no-retrain | `freeze_for_inference`; fingerprint stable across target×risk context; meta_update raises NO_RETRAIN. |
| **G4** | **Dual measure vs floor protocol** | BEST_POLICY · A33 retention | Run the **named dual SSOT** (see §4). Record hits, low_hr, a13_frac, n_zero, breach, no_retrain. Append **EVIDENCE_LEDGER** + **SCOREBOARD_HISTORY**. |
| **G5** | **Beat floor OR Court re-floor** | BEST_POLICY checklist | Either (a) challenger holds **hits ≥ 11**, **low_hr ≥ 0.28**, **a13 ≥ 0.64**, **n_zero ≤ 18**, **breach 0** under the **same protocol that set the floor**, **or** (b) Full Court **re-floors** under a single named dual and publishes new numbers in BEST_POLICY **before** promote. Marginal “beats king on a different dual” is **not** enough. |
| **G6** | **Judge PROMOTE (or PROMOTE_NARROW)** | A10/A15; Court before major decisions | Explicit production replace order. Lab ACCEPT / ACCEPT_NARROW_LAB / “beats same-window champ” ≠ production replace. |
| **G7** | **Atomic SSOT update** | BEST_POLICY · A33 | On PROMOTE only: write new `meta_policy_champion.npz` (+ backup old), update **BEST_POLICY.md** identity + floor + report hash, sidecar json, docket, ledger event. **No silent overwrite** of PROVEN/champion weights. |

### Production replace checklist (copy into case close-out)

- [ ] Case file with A10+A15 complete; three opinions named in IRAC  
- [ ] Offline train path documented; no inference retrain  
- [ ] Frozen fingerprint recorded  
- [ ] Dual under **floor SSOT** (or re-floor ruling first)  
- [ ] Floor held: hits≥11 / low_hr≥0.28 / a13≥0.64 / n_zero≤18 / breach 0 **or** re-floor clause executed  
- [ ] Judge **PROMOTE** / **PROMOTE_NARROW** for **production** (not lab-only)  
- [ ] `BEST_POLICY.md` + ledger + scoreboard updated in same session as weight swap  

---

## 4. Dual SSOT problem (must resolve before dethrone)

Two measured protocols currently disagree:

| Name | What it is | King numbers | Used for |
|------|------------|--------------|----------|
| **Floor dual (forward100)** | CASE-0037 promote dual seed=42 100d | hits **11** · a13 **0.64** · n_zero **18** · mean_tr **39.4** | **BEST_POLICY floor** — production gate |
| **North-star dual** | `run_north_star_dual` random target∈[5,90]×risk∈[1,3], XAU 15m | king same protocol: hits **7** · a13 **0.41** · n_zero **35** | L2L residual compare; **not** yet the floor SSOT |

**Court-legal resolution rule (exactly one):**

1. **Hold path:** Challenger must **hold BEST_POLICY floor numbers under the same protocol that set them** (forward100 / the command and pair setup documented in CASE-0037 report). Prefer: re-run challenger with `forward100` (or equivalent CLI) and compare to hits≥11 / low_hr≥0.28 / a13≥0.64 / n_zero≤18 / breach 0.  
2. **Re-floor path:** Full Court (A10+A15) **re-floors** under a **single named dual** (e.g. adopt north-star as sole production dual), publishes new floor table in `BEST_POLICY.md`, then challenger must beat **that** table. Inventing a third dual mid-session without re-floor is **forbidden**.

Until (1) or (2) is done, a residual that only wins north-star by 0.01 a13 **cannot** legally dethrone the king.

---

## 5. Illegal shortcuts (forbidden — not a dethrone)

| Shortcut | Why illegal | Law / precedent |
|----------|-------------|-----------------|
| **Silent overwrite** of `meta_policy_champion.npz` | Bypasses Court + floor + BEST_POLICY | A33 retention; BEST_POLICY “PROMOTE only”; no silent PROVEN overwrite |
| **F-024** synthetic silent-day densify as win | Thrash; n_zero worse | CASE-0035 **REJECT** |
| **F-025** real labels + **fake rebuilt state** | Wrong state distribution | CASE-0036 **REJECT** |
| **Process-washout promote** | Pure process curriculum collapsed A13 (lab a13 ~0.13) | CASE-L2L-P2-P10 P10 **REJECT full**; residual ruling forbids process-only production |
| **Inference retrain** when target/risk changes | Breaks no-retrain mission | **A14** / GOAL_LAW G-NO_RETRAIN |
| **Pad thrash / force-pad live** to fake A13 | Not learning; cliff not road | A13 spirit + ROAD_FOR_THE_POLICY; flea-jar forbids “impossible” excuses **and** pad |
| **Lab ACCEPT as production** | ACCEPT_NARROW_LAB ≠ PROMOTE | CASE-L2L-P10-residual; BEST_POLICY table |
| **Claim final boss / §7 ready** with open G-* blockers | Lies about goal | **A31** / **A33**; L2L_SERIES_STATUS final_gate **false** |
| **Skip rank-1 docket** for freestyle promote | Goal-relative Court broken | **A31** / **A33** issue cycle |

---

## 6. Road that is allowed (how a challenger trains)

From `ROAD_FOR_THE_POLICY.md` + CASE-0037 / residual lessons:

| Allowed road | Cliff |
|--------------|--------|
| Packed **176-dim path-state** teachers at brain-wait | Synthetic state rebuild (F-025) |
| Offline meta_update then freeze | Train during prove |
| Path re-anchor **after** light process (anti-washout) | Process-only curriculum as production diet |
| HTF-active / London-NY weighted teachers | Average-all-TF mush force |
| Dual + ledger before promote | Docs-only “done” |
| Senses pack into state; brain decides | Probe-only cosmetics; hard-rule soup decider |

**Proven density lever (king’s crown):** path-state long/short on real wait states → a13 0.28→0.64 historically. Residual improved north-star a13 only when path re-anchor was **last**.

---

## 7. Ranked “do next” (docket-tied — biggest first)

Matches `ISSUE_DOCKET.md` rank-1 / rank-2. **Do not** freestyle lower ranks while these block dethrone.

| Rank | Docket item | What to do | Blocks dethrone via |
|-----:|-------------|------------|---------------------|
| **1** | **L2L-P10** | Raise **a13_every_day** / cut zero+partial days under **one dual SSOT**; keep path re-anchor last | G-A13 — king still partial; residual n_zero 35 on north-star |
| **2** | **C-004** | Raise **hits** toward floor **11** (and low_hr ≥ 0.28) without breach | G-CLEAR — residual hits 7 on north-star; floor 11 open |
| **3** | Dual SSOT lock | Either re-measure residual on **forward100 floor protocol** **or** Full Court **re-floor** (§4) | G5 gate — without this, promote is illegal even if north-star looks good |
| **4** | Open Full Court promote case | Only after G4–G5 numbers print; A10+A15; PROMOTE if held | G1/G6 |
| **5** | Atomic BEST_POLICY + ledger | Swap weights + rewrite identity + floor + report hash | G7 |
| **6** | **L2L-FINAL-GATE** / multi-seed | After production dethrone path stable — §7 multi-seed 100d is **mission final boss**, not required to swap king if Court promotes narrow on floor beat | G-LONG — **not** claimed done |

**Not next for dethrone:** Mark phase (blocked); CASE-0032…0034 queue (senses series continues but does not replace G5 floor gate); game_train forge alone without path dual.

---

## 8. One-page verdict (honest)

```text
King:     CASE-0037  fp meta4275  floor hits≥11 a13≥0.64 n_zero≤18 breach0
Challenger: L2L residual lab  fp meta10835  NOT PRODUCTION
North-star 100d: residual slightly better a13; same hits; floor NOT held
Legal dethrone: Court A10+A15 + offline train + freeze + dual on floor SSOT
                + (hold floor OR re-floor) + PROMOTE + BEST_POLICY/ledger update
Illegal: silent overwrite | F-024 | F-025 | process-washout promote | inference retrain
Next: L2L-P10 + C-004 under one dual SSOT — then promote case if numbers print
Final boss / §7: still false
```

---

## 9. Pin paths

| Artifact | Role |
|----------|------|
| This file | Legal dethrone path (analysis SSOT) |
| `BEST_POLICY.md` | King identity + floor |
| `ISSUE_DOCKET.md` | Ranked blockers |
| `L2L_SERIES_STATUS.md` | L2L rulings; final_gate false |
| `cases/CASE-L2L-P10-residual.md` | Lab residual Court file |
| `artifacts/l2l_p10_residual_report.json` | Challenger dual numbers |
| `tests/test_dethrone_the_king_path.py` | Structural + live identity pin |

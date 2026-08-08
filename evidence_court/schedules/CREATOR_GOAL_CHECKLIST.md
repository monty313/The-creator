# CREATOR — Full-project goal checklist (Phase 1)

**Owner:** Creator  
**Phase:** 1 of 2 (Law **A30**)  
**Updated:** 2026-08-07 (A31/A32/A33 goal-relative axes)  
**Scope:** Entire project — Court, meta_rl brain/path, laws, scoreboard, data, goal SSOT.  
**Rule:** **Every row → full Court (A10+A15)** before closed.  
**Gate:** Phase 2 (Mark) only when **all rows** terminal.  
**North star:** Law **A31** + `mark_here/knowledge/lab/GOAL.md`.

**Goal reminder:** any target×risk, no retrain at prove, breach **0**, climb clear%, scalper **8–400 trades/day**, L2L brain, **emergent senses drive decisions**, long-term performance.

**Scoreboard floor (do not regress without measure):** CASE-0029 — hits 11 / low_hr 0.28 / a13 0.28 / breach 0.

---

## Creator’s whole-project diagnosis (summary)

Scaffolding and safety (breach 0) and multi-TF edges exist; the **brain is young**, **A13 is not lived**, **senses/watch are not fully wired into learning**, and **dual promote_ready is false**. Final boss needs a **trained L2L brain that captures London/NY opportunity density, perceives with A32 senses, and converts under goal/risk**, measured multi-seed, with Watch→train→prove closed. Court must **keep generating goal-relative issues** (A33) until that is true.

---

## Checklist (ordered — Court in this order unless Judge reorders by severity)

| # | item_id | title | goal_axes | why_for_goal | proposed_work (Creator) | court_case | status |
|--:|---------|-------|-----------|--------------|-------------------------|------------|--------|
| 1 | **C-001** | **Close Watch→path→brain loop** | G-SIGHT, G-A13, G-TRAIN | A13 + good trades + L2L | Wire Opportunity Watch into `run_goal_path_day` / forward; log misses; feed miss labels into offline meta curriculum; measure London/NY miss-rate drop | CASE-0031 | **PENDING_COURT** |
| 2 | **C-002** | **Real-bar / opportunity-labeled meta-train** | G-TRAIN, G-NO_RETRAIN, G-CLEAR | no-retrain quality + clear% | Historical M1 + Mark edge opportunity labels (London/NY); retrain champion; prove fingerprint stable across pairs | TBD | **PENDING_COURT** |
| 3 | **C-003** | **A13 every-day density (London/NY no excuse)** | G-A13 | A13 MUST 8–400 | Measure trades/day distribution; brain_drives + clock ≥8 on active days without pad; promote only if a13_frac climbs without dual regression | ties 0034 | **PENDING_COURT** |
| 4 | **C-004** | **Dual conversion (hits / low_hr / promote_ready)** | G-CLEAR, G-BREACH0 | clear% final boss | Goal-conditioned size + hold + residual under envelope so random [5–90]×[1–3] hits climb and low_hr gate; 100d seed matrix | ties 0033 | **PENDING_COURT** |
| 5 | **C-005** | **Senses drive the brain (A32 not probe-only)** | G-SIGHT, G-FEEL, G-TASTE, G-HEAR, G-L2L | L2L / A6 / A32 | Sight/feel/taste/hearing pack into state channels the brain trains on; CASE-0031–0034 complete with fail-mode tests | 0031–0034 | **PENDING_COURT** |
| 6 | **C-006** | **Production path = brain only** | G-L2L, G-TRAIN | A29 purity | Audit `goal_path`: default brain_drives; quarantine decision-critical hard gates; unit pin | TBD | **PENDING_COURT** |
| 7 | **C-007** | **High-target band (50–90) under risk 1–3** | G-CLEAR, G-TASTE | any-pair goal | Curriculum + path pressure for hard pairs; non-vacuous hit rates mid/high band | TBD | **PENDING_COURT** |
| 8 | **C-008** | **Multi-seed / multi-window long-term eval** | G-LONG, G-CLEAR | long-term performance | ≥3 seeds, ≥2 calendar windows; promote_ready cannot be seed=42 vanity | TBD | **PENDING_COURT** |
| 9 | **C-009** | **Multi-symbol book risk integrity** | G-BREACH0 | breach 0 | Concurrent symbols: aggregate envelope, correlation stress, no double-count under density | TBD | **PENDING_COURT** |
| 10 | **C-010** | **Fill realism (friction class)** | G-CLEAR, G-LONG | honest clear% | Declare spread/commission/slippage; re-measure dual under friction | TBD | **PENDING_COURT** |
| 11 | **C-011** | **Court brain ↔ lab prove path** | G-ONEBOT | one bot mission | Single champion artifact path — no dual silent brains | TBD | **PENDING_COURT** |
| 12 | **C-012** | **FINAL_BOT_SPEC + promote gates** | G-CLEAR, G-A13, G-NO_RETRAIN, G-SIGHT, G-FEEL, G-TASTE, G-HEAR | mission complete | Freeze promote gates matching GOAL+A13+A29+A32; promote_ready only multi-seed | TBD | **PENDING_COURT** |

---

## Sense sub-map (absorb, don’t double-bill)

| Case | Maps into | Fail mode to kill |
|------|-----------|-------------------|
| CASE-0031 Sight + Watch | **C-001**, **C-005** | flat on B&B pullback day |
| CASE-0032 Feel | **C-005** | lone oscillator / freeze on load |
| CASE-0033 Taste | **C-004**, **C-005** | all bars equal / marginal high-target |
| CASE-0034 Hearing | **C-003**, **C-005** | thrash reverse / stale story |

---

## Phase 1 completion criteria

- [ ] All C-001…C-012 terminal Court rulings  
- [ ] A32 senses not probe-only (documented path into state/brain)  
- [ ] No PENDING_COURT / IN_COURT rows left  
- [ ] `schedules/SCHEDULE.md` marks Phase 1 **COMPLETE**  
- [ ] Then open Phase 2: Mark files `MARK_GOAL_CHECKLIST.md`

---

## Creator note (priority)

**Learning loop first** (C-001, C-002), then **density + conversion** (C-003, C-004), then **sense integration** (C-005 / 0031–0034), then integrity / honesty / one-bot (C-006…C-012). Skipping to live deploy or exit dials without this sequence repeats known failures.

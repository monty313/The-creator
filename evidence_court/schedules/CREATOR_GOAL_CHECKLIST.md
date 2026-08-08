# CREATOR — Full-project goal checklist (Phase 1)

**Owner:** Creator  
**Phase:** 1 of 2 (Law **A30**)  
**Filed:** 2026-08-07  
**Scope:** Entire project as built — Court `evidence_court/`, meta_rl brain/path, laws A1–A29, scoreboard, data, goal SSOT.  
**Source of review:** internet systems design + inventory of *this* repo (not Mark KAG).  
**Rule:** **Every row → full Court (A10+A15)** before it is closed.  
**Gate:** Phase 2 (Mark) starts only when **all rows** are terminal (PROMOTE / REJECT / ADMIT / INCONCLUSIVE with disposition).

**Goal reminder:** any target×risk, no retrain at prove, breach **0**, climb clear%, scalper **8–400 trades/day**, L2L brain, long-term performance.

**Scoreboard floor (do not regress without measure):** CASE-0029 — hits 11 / low_hr 0.28 / a13 28% / breach 0.

---

## Creator’s whole-project diagnosis (summary)

The stack has **laws and scaffolding ahead of a closed learning loop**. Safety (breach 0) and multi-TF edge sensors exist; the **brain is young**, **A13 is not lived**, **senses/watch are not fully wired into learning**, and **dual promote_ready is false**. Hard-rule history still haunts the path. Final boss needs a **trained L2L brain that captures London/NY opportunity density and converts under goal/risk**, measured multi-seed, with Watch→train→prove closed.

---

## Checklist (ordered — Court in this order unless Judge reorders)

| # | item_id | title | why_for_goal | proposed_work (Creator) | court_case | status |
|--:|---------|-------|--------------|-------------------------|------------|--------|
| 1 | **C-001** | **Close Watch→path→brain loop** | A13 + good trades + L2L | Wire Opportunity Watch into `run_goal_path_day` / forward every decision; log misses; feed miss labels into offline meta curriculum; measure London/NY miss-rate drop | `cases/` TBD CASE | **PENDING_COURT** |
| 2 | **C-002** | **Real-bar / opportunity-labeled meta-train** | no-retrain quality + clear% | Replace/extend pure synthetic curriculum with labels from historical M1 + Mark edge opportunities (esp. London/NY); retrain champion; prove fingerprint stable across pairs | TBD | **PENDING_COURT** |
| 3 | **C-003** | **A13 every-day density (London/NY no excuse)** | A13 MUST 8–400 | Measure trades/day distribution; brain_drives + clock must land ≥8 on active days without pad; promote only if a13_frac climbs without dual regression | TBD | **PENDING_COURT** |
| 4 | **C-004** | **Dual conversion (hits / low_hr / promote_ready)** | clear% final boss | Goal-conditioned size + hold + multi-leg residual under envelope so random [5–90]×[1–3] hits ≥12 and low_hr gate; 100d seed matrix | TBD | **PENDING_COURT** |
| 5 | **C-005** | **Senses drive the brain (not probe-only)** | L2L / A6 / A28 docket | Sight/feel/taste/hearing outputs pack into state channels the brain trains on; CASE-0031–0034 map into C-005 subwork | ties 0031–0034 | **PENDING_COURT** |
| 6 | **C-006** | **Production path = brain only** | A29 purity | Audit `goal_path`: default brain_drives; quarantine or delete decision-critical hard gates; unit pin that production path cannot enable rule soup without flag | TBD | **PENDING_COURT** |
| 7 | **C-007** | **High-target band (50–90) under risk 1–3** | any-pair goal | Curriculum + path pressure for hard pairs; non-vacuous hit rates mid/high band; flea-jar full action space | TBD | **PENDING_COURT** |
| 8 | **C-008** | **Multi-seed / multi-window long-term eval** | long-term performance | Forward protocol: ≥3 seeds, ≥2 calendar windows; promote_ready cannot be single seed=42 vanity | TBD | **PENDING_COURT** |
| 9 | **C-009** | **Multi-symbol book risk integrity** | breach 0 | Concurrent symbols: aggregate envelope, correlation stress days, no double-count ledger bugs under brain_drives density | TBD | **PENDING_COURT** |
| 10 | **C-010** | **Fill realism (friction class)** | honest clear% | Declare and pin spread/commission/slippage model; re-measure dual under friction; no frictionless PROMOTE | TBD | **PENDING_COURT** |
| 11 | **C-011** | **Court brain ↔ lab prove path** | one bot mission | Single champion artifact path: Court meta brain is the prove brain *or* explicit bridge to lab `prove_it` / PROVEN — no dual silent brains | TBD | **PENDING_COURT** |
| 12 | **C-012** | **FINAL_BOT_SPEC + promote gates = A13+dual+L2L** | mission complete | Write/freeze promote gates matching GOAL+A13+A29; `promote_ready` true only when gates met multi-seed | TBD | **PENDING_COURT** |

---

## Already on related dockets (absorb, don’t double-bill)

| Existing | Maps into |
|----------|-----------|
| CASE-0031 Sight + Watch | **C-001**, **C-005** |
| CASE-0032 Feel | **C-005** |
| CASE-0033 Taste | **C-004**, **C-005** |
| CASE-0034 Hearing | **C-003**, **C-005** |
| CASE-0030 multiset session | optional → **C-003** if still open |

When a sense case resolves, update the parent **C-00x** row status.

---

## Phase 1 completion criteria

- [ ] All C-001…C-012 have terminal Court rulings  
- [ ] No PENDING_COURT / IN_COURT rows left  
- [ ] `schedules/SCHEDULE.md` marks Phase 1 **COMPLETE**  
- [ ] Then open Phase 2: Mark files `MARK_GOAL_CHECKLIST.md` under Court schedule  

---

## Creator note (internet / systems)

Priority order is **learning loop first** (C-001, C-002), then **density + conversion** (C-003, C-004), then **sense integration** (C-005), then **integrity / honesty / one-bot** (C-006…C-012). Skipping to live deploy or more exit dials without this sequence repeats known failures (F-011…).

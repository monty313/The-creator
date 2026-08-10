# Court trials audit — did every trial go through Full Court?

**Artifact path:** `evidence_court/COURT_TRIALS_AUDIT.md`  
**Updated:** 2026-08-09  
**Kind:** Procedure completeness audit (A10+A15 markers) — **not** re-litigation of substance  
**Machine scan:** `artifacts/_court_trials_scan.json`  
**Bar:** Creator opening · Mark opening · Counsel/A15 or three-opinion language · Judge IRAC/ruling  

**Honest headline:** **No — not every checklist trial has completed Full Court.** Many historical case files have durable rulings; **Creator Phase 1 is not terminal**; several rows are **PENDING_COURT / QUEUED / PARTIAL**. Production champion remains **CASE-0037 / meta4275**.

---

## 1. Inventory — all case files (`evidence_court/cases/CASE*.md`)

**n = 40** markdown case files (plus JSON sidecars / transcript, not double-counted as separate trials).

### Structure classes (scan)

| Structure class | Meaning | Count |
|-----------------|---------|------:|
| **FULL_A10_A15** | Creator + Mark + Counsel + Judge/IRAC + ruling language | **21** |
| **PRE_A15_OR_PARTIAL** | Creator + Mark + Judge/ruling; **no Counsel marker** (often pre-A15 permanent) | **14** |
| **RULING_THIN_STRUCTURE** | Ruling/IRAC present; openings incomplete or measure-only sheet | **5** |

### Full table (procedure markers)

| Case file | Structure | Status line (abbrev) | Ruling token |
|-----------|-----------|----------------------|--------------|
| CASE-0001-meta-rl-state.md | PRE_A15 | PROMOTED | PROMOTE |
| CASE-0002-multitf-pullback-edge.md | PRE_A15 | PROMOTED | PROMOTE |
| CASE-0003-goal-path-consistency.md | PRE_A15 | ADMITTED / in progress language | PROMOTE |
| CASE-0004-htf-completed-side-quality.md | PRE_A15 | **IN_COURT** (stale?) | PROMOTE |
| CASE-0005 … CASE-0013 (9 files) | PRE_A15 | mostly CLOSED | PROMOTE |
| CASE-0015-market-ontology.md | **FULL** | PROMOTED | PROMOTE |
| CASE-0016-regime-catalog.md | PRE_A15 | PROMOTED | PROMOTE |
| CASE-0017-regime-curriculum.md | **FULL** | PROMOTED narrow | PROMOTE |
| CASE-0018-daypath-regime-channel.md | **FULL** | PROMOTED narrow | PROMOTE |
| CASE-0019-profit-gated-residual.md | **FULL** | PROMOTED narrow | PROMOTE |
| CASE-0020-a20-dual-measure.md | **THIN** | CLOSED dual REJECT F-020 | REJECT |
| CASE-0021-one-sym-edge-density.md | **FULL** | PROMOTED narrow | PROMOTE |
| CASE-0022-a21-measure.md | **THIN** | CLOSED dual REJECT | REJECT |
| CASE-0023-dense-real-edges.md | **FULL** | PROMOTED narrow | PROMOTE |
| CASE-0024-a22-measure.md | **THIN** | CLOSED dual REJECT | REJECT |
| CASE-0025-dense-nylon-prime.md | **FULL** | CLOSED dual REJECT | REJECT |
| CASE-0026-multiset-force-densify.md | **FULL** | CLOSED dual REJECT | REJECT |
| CASE-0027-production-10m-clock.md | **FULL** | CLOSED ADMIT / dual reject | REJECT |
| CASE-0028-cont-hold-r.md | **FULL** | CLOSED PROMOTE A26 | PROMOTE |
| CASE-0029-production-5m-clock.md | **FULL** | CLOSED PROMOTE A27 | PROMOTE |
| CASE-0030-dual-sym-on-agree.md | **THIN** | **IN_COURT** | PROMOTE |
| CASE-0030-multiset-session-align.md | **FULL** | CLOSED dual REJECT | REJECT |
| CASE-0031-sense-sight-opportunity-watch.md | **FULL** | OPEN wire PROMOTED narrow | PROMOTE |
| CASE-0035-silent-day-opportunity-curriculum.md | **FULL** | CLOSED REJECT F-024 | REJECT |
| CASE-0036-real-bar-a13-harvest.md | **FULL** | CLOSED REJECT F-025 | REJECT |
| CASE-0037-path-state-teachers.md | **FULL** | CLOSED **PROMOTE_NARROW** champion | PROMOTE_NARROW |
| CASE-C002-opportunity-labeled-meta-train.md | **FULL** | OPEN API PROMOTED narrow | PROMOTE |
| CASE-FORWARD-100.md | **THIN** | PROMOTED | PROMOTE |
| CASE-L2L-P1-senses-drive-brain.md | **FULL** | CLOSED ACCEPT | ACCEPT |
| CASE-L2L-P2-P10-ordered-series.md | **FULL** | CLOSED MIXED (P10 REJECT full) | ACCEPT / REJECT |
| CASE-L2L-P10-residual.md | **FULL** | CLOSED ACCEPT_NARROW_LAB | ACCEPT_NARROW |
| CASE-PATH-LEARNING.md | **FULL** | CLOSED ACCEPT_NARROW lab | ACCEPT_NARROW |

*Scan automation may tag Counsel via any “counsel” string; spot-checks below ground FULL vs THIN.*

### Missing case files (docket/sense map expects them; **no trial file**)

| Expected | Docket / map | Status |
|----------|--------------|--------|
| CASE-0032 Feel | QUEUED | **No case file — trial not opened** |
| CASE-0033 Taste | QUEUED | **No case file — trial not opened** |
| CASE-0034 Hearing | QUEUED | **No case file — trial not opened** |
| CASE-0014 | (gap in numbering) | N/A |

---

## 2. Completed Full Court (durable structure + ruling)

Trials that show **FULL_A10_A15** markers **and** a durable terminal or narrow ruling (including REJECT as complete trial):

| Case | Outcome class |
|------|----------------|
| CASE-0015, 0017, 0018, 0019 | PROMOTE narrow / ontology-curriculum |
| CASE-0021, 0023 | PROMOTE narrow density geometry |
| CASE-0025, 0026, 0027, 0030-session | CLOSED dual REJECT / ADMIT measure |
| CASE-0028, 0029 | PROMOTE A26/A27 |
| CASE-0031 | Wire PROMOTE narrow (still OPEN residual) |
| CASE-0035, 0036 | REJECT F-024 / F-025 |
| CASE-0037 | **PROMOTE_NARROW** production champion |
| CASE-C002 | API PROMOTE narrow (residual dual deferred) |
| CASE-L2L-P1 | ACCEPT |
| CASE-L2L-P2-P10 | CLOSED MIXED (P2–P9 narrow/accept; **P10 REJECT full**) |
| CASE-L2L-P10-residual | ACCEPT_NARROW_LAB |
| CASE-PATH-LEARNING | ACCEPT_NARROW lab |

**Also “through Court” but pre-A15 / partial Counsel:** CASE-0001–0013, 0016 — durable PROMOTE/CLOSED language with Creator+Mark+Judge; treat as **historical complete under then-procedure**, not modern three-opinion gold standard.

**Measure sheets with ruling but thin openings (trial “ran” as dual measure, not full A10):** CASE-0020, 0022, 0024, FORWARD-100, CASE-0030-dual-sym (also **IN_COURT** stale risk).

---

## 3. Incomplete / not through trial (gaps)

### 3A — Creator checklist C-001…C-012 (Law A30: **each row → full Court**)

| item_id | Checklist status | Full Court through? | Notes |
|---------|------------------|---------------------|--------|
| **C-001** | **PARTIAL** | **No (terminal)** | CASE-0031 partial wire; miss-rate deferred |
| **C-002** | **PARTIAL** | **Partial** | C002/0035–0037 closed pieces; train class not “all terminal” |
| **C-003** | **PARTIAL** | **Partial** | 0037 PROMOTE_NARROW; every-day A13 still open |
| **C-004** | **PENDING_COURT** / docket OPEN | **No** | Rank-2 conversion; no dedicated terminal C-004 case |
| **C-005** | **PENDING_COURT** / PARTIAL senses | **No** | P1 ACCEPT; 0032–0034 **not opened** |
| **C-006** | **PENDING_COURT** | **No** | No case file |
| **C-007** | **PENDING_COURT** | **No** | No case file |
| **C-008** | **PENDING_COURT** | **No** | No case file |
| **C-009** | **PENDING_COURT** | **No** | No case file |
| **C-010** | **PENDING_COURT** | **No** | No case file |
| **C-011** | **PENDING_COURT** | **No** | No case file |
| **C-012** | **PENDING_COURT** | **No** | No case file |

**Phase 1 completion criteria in checklist:** all C-001…C-012 terminal — **false**. Mark phase **BLOCKED**.

### 3B — L2L ordered series

| Trial | Ruling | Full Court structure? | Through? |
|-------|--------|----------------------|----------|
| P1 | ACCEPT | FULL (CASE-L2L-P1) | **Yes** |
| P2–P7 | ACCEPT_NARROW each | FULL (bundled CASE-L2L-P2-P10) | **Yes (narrow)** |
| P8 | ACCEPT | FULL (same case) | **Yes** |
| P9 | ACCEPT (window) | FULL (same case) | **Yes (window)** |
| P10 | **REJECT full** | FULL (same case) | **Yes (reject is terminal for full Accept)** |
| P10 residual | ACCEPT_NARROW_LAB | FULL (CASE-L2L-P10-residual) | **Yes (lab)** |
| PATH_LEARNING | ACCEPT_NARROW | FULL (CASE-PATH-LEARNING) | **Yes (lab)** |
| L2L §7 final gate | **false / OPEN** | Not a closed case | **No** |

### 3C — Queued / open / stale case statuses

| Item | Gap |
|------|-----|
| CASE-0032 / 0033 / 0034 | **QUEUED** — zero case files |
| CASE-0004 status IN_COURT | Possible stale status vs promote language |
| CASE-0030-dual-sym IN_COURT | Thin structure + open status |
| CASE-0031 / CASE-C002 | OPEN residual metrics despite narrow PROMOTE |
| L2L-P10 / C-004 docket rank-1/2 | **OPEN** blockers |
| GAME-TRAIN | ACTIVE lab, not production trial complete |
| Mark M-* | **BLOCKED** (Phase 2) |

---

## 4. SSOT cross-check

| SSOT claim | Audit agreement |
|------------|-----------------|
| `ISSUE_DOCKET` **goal_achieved: false** | **Agree** — Phase 1 incomplete; rank-1 open |
| Rank-1 **L2L-P10**, rank-2 **C-004** OPEN | **Agree** |
| C-006…C-012 **PENDING_COURT** | **Agree** — no Full Court trials |
| CASE-0032…0034 **QUEUED** | **Agree** — no files |
| L2L **final §7 gate false** | **Agree** |
| Production champion CASE-0037 meta4275 | **Agree** — BEST_POLICY; no audit claim of replace |
| PATH_LEARNING / residual lab only | **Agree** — not production |
| Checklist “every row full Court before closed” | **Not satisfied** for C-004…C-012 and terminal C-001/003/005 |

**Contradiction check:** Audit does **not** claim all trials complete. Docket open rows and checklist PENDING/PARTIAL are the source of truth for “not through.”

### Production identity (audit statement)

| Field | Value |
|-------|--------|
| Champion case | CASE-0037 |
| Fingerprint class | **meta4275** |
| Weights | `artifacts/meta_policy_champion.npz` |
| PROMOTE+BEST_POLICY replace since? | **No** (labs only) |

---

## 5. Spot-checks (audit vs real files)

| Case | Audit said | File check |
|------|------------|------------|
| CASE-0037 | FULL + PROMOTE_NARROW CLOSED | status CLOSED PROMOTE_NARROW; Counsel A15; Judge IRAC — **match** |
| CASE-PATH-LEARNING | FULL + ACCEPT_NARROW CLOSED | status CLOSED ACCEPT_NARROW; Creator/Counsel/IRAC — **match** |
| CASE-0022 | THIN + CLOSED REJECT | status CLOSED dual REJECT; Judge IRAC; no Creator/Mark openings — **match thin** |
| CASE-0032 | no file / QUEUED | **no file** — **match gap** |

---

## 6. Defects only (procedure hygiene — not reopening substance)

1. **Do not claim “all trials done.”** C-006…C-012 and 0032–0034 never sat Full Court.  
2. **Pre-A15 cases (0001–0013, 0016):** complete under older bar; modern PROMOTE would require A15 if reopened.  
3. **Thin measure cases (0020/22/24/FORWARD/0030-dual):** rulings exist; Full A10 openings often absent — flag if used as procedure precedent for new production PROMOTE.  
4. **Stale IN_COURT** on 0004 / 0030-dual-sym — hygiene cleanup optional (Summary Court status pin), not this audit’s re-trial.  
5. **Bundled L2L P2–P10:** one case file holds multiple proposal IRAC segments — procedure present; P10 full Accept **failed** (honest).

---

## 7. Bottom line

```text
Did the courts go through ALL of the trials?
  → NO for the binding Creator checklist (C-001…C-012 terminal Full Court).
  → YES for many historical CASE-00xx files (with pre-A15 honesty).
  → YES for L2L P1–P10 series file(s) including P10 REJECT and residual/PATH_LEARNING lab.
  → NO for CASE-0032…0034, C-006…C-012, L2L §7 final gate, Mark phase.

goal_achieved remains false. King remains CASE-0037 meta4275.
```

---

## 8. Pin paths

| Path | Role |
|------|------|
| This file | Durable audit SSOT |
| `artifacts/_court_trials_scan.json` | Machine inventory |
| `tests/test_court_trials_audit.py` | Structural pin |
| `ISSUE_DOCKET.md` | Live open trials |
| `schedules/CREATOR_GOAL_CHECKLIST.md` | C-001…C-012 statuses |

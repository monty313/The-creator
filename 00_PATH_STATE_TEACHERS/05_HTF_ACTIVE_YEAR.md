# HTF-active year train

**What:** Path-state teachers **only** when **≥1 official HTF set is active**.  
**Data:** ~1 trading year of days (as much price history as we have).  
**After train:** dual vs floor → **replace champion if it beats**.

## Run

```bash
python -m evidence_court.meta_rl.train_htf_active_year --harvest-days 252 --dual-days 100
```

## Artifacts

| File | Role |
|------|------|
| `artifacts/path_state_teachers_htf_active_year.json` | Teacher pack |
| `artifacts/meta_policy_htf_active_year.npz` | Shadow brain |
| `artifacts/htf_active_year_train_report.json` | Report + promote decision |

## Floor (must hold + improve)

hits ≥ 11 · low_hr ≥ 0.28 · a13 ≥ 0.64 · breach 0  
+ improve at least one of hits / a13 / n_zero

## Result (2026-08-09 clean re-harvest)

| Stage | Outcome |
|-------|---------|
| Harvest | **252** days · **2005** teachers · **all `n_htf_active≥1`** · 1576 L/NY · dims_ok |
| Sources | path_state_htf_active (+ miss/side/watch when gated) |
| Train | Shadow `meta10565` (warmstart `meta4275`) |
| Dual (30d XAU 15m) | hits **3** · a13 **0.30** · n_zero **11** · breach **0** |
| Promote | **No** — failed hits/low_hr/a13 floor hold |
| Champion | Unchanged `meta4275` CASE-0037 |

Report: `artifacts/htf_active_year_train_report.json`

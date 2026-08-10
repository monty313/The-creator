# Court ruling + how to run

**Case:** `evidence_court/cases/CASE-PATH-LEARNING.md`  
**Ruling:** **ACCEPT_NARROW** (lab road + execute steps 1–6 offline)  
**Ledger:** `CASE_PATH_LEARNING_RULING`  
**Production:** still CASE-0037 `meta4275` — `production_replace=false`

### Measured lab dual (30d north-star, seed=42)

| | hits | a13 | n_zero | breach |
|--|-----:|----:|-------:|-------:|
| PATH LEARNING lab | 3 | **0.30** | 11 | 0 |
| Champion same window | 3 | 0.267 | 11 | 0 |

`promote_lab=true` · `floor_hold=false` · shadow `meta_policy_path_learning.npz` (fp meta9625)

## Commands

```text
# Unit pins (shipped helpers)
pytest evidence_court/tests/test_path_learning.py -q

# Lab train + dual (after Court ACCEPT*)
python -m evidence_court.meta_rl.train_path_learning --dual-days 30 --seed 42
```

## Artifacts

| Path | Role |
|------|------|
| `evidence_court/artifacts/meta_policy_path_learning.npz` | Lab shadow |
| `evidence_court/artifacts/path_learning_report.json` | Train + dual + promote_guard |
| `evidence_court/artifacts/meta_policy_champion.npz` | Production (unchanged without PROMOTE) |

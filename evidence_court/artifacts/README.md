# artifacts/ — machine outputs only

## Production (stay at this folder root)

| File | Role |
|------|------|
| `meta_policy_champion.npz` | **BEST POLICY** weights |
| `meta_policy_champion.json` | Sidecar |
| `meta_policy_champion_pre0037.npz` | Pre-promote backup |

Do **not** move these without updating `meta_rl/policy.py` load paths + `BEST_POLICY.md`.

## Subfolders

| Dir | Put here |
|-----|----------|
| `policies_lab/` | Lab / shadow meta policies |
| `teachers/` | Path-state & harvest teacher packs |
| `reports/` | Dual, train, arbitration result JSON/MD |
| `day12/` | Day-12 method / reaudit / TV exhibits |
| `charts/` | Screenshots + cv2 principle overlays |
| `scripts/` | One-off lab Python |
| `game_train/` | A34 forge packs |
| `logs/` | `*.log` from long runs |

## CLI defaults that still write here

- Champion load: `artifacts/meta_policy_champion.npz`
- Many train scripts now default lab outs under `policies_lab/` / `reports/` / `teachers/`

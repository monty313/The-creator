# PRICE DATA — where Mark finds the 4 symbols

**Lab home (the-truth):** `data/raw/`  
**Config:** `configs/data.yaml`  
**Do not edit raw CSVs by hand.**

---

## The 4 symbols (one brain, many markets)

| Role | Symbol | In-repo M1 / curriculum CSV |
|------|--------|-----------------------------|
| **Bootcamp (primary)** | **XAUUSD** (gold) | `data/raw/XAUUSD_curriculum_2026.csv` |
| Expansion | **EURUSD** | `data/raw/EURUSD_M1_curriculum.csv` |
| Expansion | **GBPUSD** | `data/raw/GBPUSD_M1_curriculum.csv` |
| Expansion | **US30** | `data/raw/US30_M1_curriculum.csv` |

All four are first-class for multi-symbol train — not gold-only.

### Extra gold files (same symbol, different windows)

| File | Use |
|------|-----|
| `data/raw/XAUUSD_curriculum_2026.csv` | **Preferred curriculum** (smaller, current lab default) |
| `data/raw/XAUUSD_M1_full.csv` | Full M1 history |
| `data/raw/XAUUSD_M1_drill.csv` | Short drill slice |

---

## Absolute path on Monty’s PC (lab)

```text
C:\Users\user\Fable5_Foundation\MOMENTUM_ONE\the-truth\data\raw\
```

| Symbol | Full path |
|--------|-----------|
| XAUUSD (curriculum) | `...\the-truth\data\raw\XAUUSD_curriculum_2026.csv` |
| XAUUSD (full) | `...\the-truth\data\raw\XAUUSD_M1_full.csv` |
| XAUUSD (drill) | `...\the-truth\data\raw\XAUUSD_M1_drill.csv` |
| EURUSD | `...\the-truth\data\raw\EURUSD_M1_curriculum.csv` |
| GBPUSD | `...\the-truth\data\raw\GBPUSD_M1_curriculum.csv` |
| US30 | `...\the-truth\data\raw\US30_M1_curriculum.csv` |

---

## How to find data if this kit moved

Discovery order for agents / Mark / scripts:

1. Env **`MARKOS_THE_TRUTH_ROOT`** → `{root}/data/raw/`
2. Parent of this `mark_here` folder if it contains `GOAL.md` → `{parent}/data/raw/`
3. Default lab path above
4. Config `configs/data.yaml` → `m1_csv_dir` (may point outside repo on Colab / Camillion_data)

**Portable kit note:** CSVs are **not** copied into `mark_here/knowledge/` (hundreds of MB). This card is the map. Price files stay in the lab `data/raw/`.

---

## CSV shape (all symbols)

Header style (MT5-like):

```text
<DATE><TIME><OPEN><HIGH><LOW><CLOSE><TICKVOL><VOL><SPREAD>
```

Timeframe: **M1** bars.

---

## Spread / cost notes (from configs/data.yaml)

| Symbol | Typical cost note |
|--------|-------------------|
| XAUUSD | Razor-thin spread; often 0 commission |
| US30 | Razor-thin spread; often 0 commission |
| EURUSD | Normal FX spread |
| GBPUSD | Normal FX spread |

Brain also sees relative spread in obs so it can stand down when spread is hostile.

---

## Related lab folders

| Path | Meaning |
|------|---------|
| `data/raw/` | Original price CSVs |
| `data/interim/` | Half-built tables |
| `data/processed/` | Ready for modeling |
| `data/external/` | Third-party dumps |
| `artifacts/gpu_cache_*.npz` | Feature cache (delete after symbol/feature change) |
| `artifacts/symbol_cache/` | Per-symbol cache (same rule) |

---

## Quick check (PowerShell, from the-truth root)

```powershell
Get-ChildItem data\raw\*.csv | Select-Object Name, @{N='MB';E={[math]::Round($_.Length/1MB,2)}}
```

Expect four symbols present: **XAUUSD**, **EURUSD**, **GBPUSD**, **US30**.

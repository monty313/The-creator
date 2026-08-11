# Folder map — The Creator (organized)

**Last cleaned:** 2026-08-11

---

## Root (only what you need every day)

| Item | Role |
|------|------|
| `AGENTS.md` | Permanent Court laws (auto-loaded) |
| `README.md` | This project’s front door |
| `docs/` | Procedure + long-form project docs |
| `tools/` | Launchers (TradingView, …) |
| `evidence_court/` | Court + brain + tests |
| `mark_here/` | Mark knowledge |
| `Aaron_here/` | Teacher of Learning |
| `00_PATH_*` | Path-state / path-learning guides |
| `Learning-How_to/` | Curriculum notes |
| `strategies/` | Geometry library (not the live bot) |

---

## `docs/`

| Path | Contents |
|------|----------|
| `docs/grok_cli_evidence_court_v2.md` | Court procedure SSOT |
| `docs/project/` | L2L 100-day brief, edge notes, etc. |

---

## `tools/tradingview/`

| File | Use |
|------|-----|
| `start_tradingview_cdp.bat` | Launch TV with CDP |
| `RELAUNCH_TV_CDP.bat` | Kill + relaunch |

---

## `evidence_court/`

| Path | Contents |
|------|----------|
| `*_LAW.md` + `.json` | Permanent laws (A10–A33, …) |
| `BEST_POLICY.md` | Production champion SSOT |
| `ISSUE_DOCKET.md` | Ranked blockers |
| `arbitration/` | Day12 / learn-phase / dethrone seat files |
| `cases/` | Case files |
| `ledger/` | EVIDENCE_LEDGER, scoreboard, counsel cache |
| `meta_rl/` | Brain, path, train, senses (source) |
| `schedules/` | Checklists |
| `tests/` | Pytest pins |
| `artifacts/` | **All machine outputs** (see below) |

---

## `evidence_court/artifacts/` (outputs)

**Production stays at the artifacts root:**

| File | Role |
|------|------|
| `meta_policy_champion.npz` + `.json` | Live champion |
| `meta_policy_champion_pre0037.npz` | Backup only |

**Subfolders:**

| Folder | Role |
|--------|------|
| `policies_lab/` | Shadow / lab `.npz` + sidecars (not production) |
| `teachers/` | Path-state / harvest teacher packs |
| `reports/` | Dual / train / showdown JSON+MD |
| `day12/` | Day-12 reaudit, method trade, charts |
| `charts/` | TV captures + principle overlays |
| `scripts/` | Lab one-off Python (day12 redraw, TV markup, …) |
| `game_train/` | Policy Forge / A34 lab |
| `logs/` | Forward log tails |

---

## `strategies/`

| Path | Role |
|------|------|
| `README.md`, `INVENTORY.md` | Index |
| `algo_guide_14/`, `sauces/`, … | Source packs |
| `python_batch/` | Batch runners |
| `reports/` | Prove / Monte Carlo / inventory dumps |
| `_scratch/` | Junk exports (not for Court) |
| `tweaks/`, `ranked/` | Large derived note sets |

---

## Rules for keeping it clean

1. **New law** → `evidence_court/*_LAW.md` + pin test.  
2. **New train output** → `artifacts/policies_lab/` or `reports/`, never overwrite champion without Court.  
3. **Day exhibits** → `artifacts/day12/`.  
4. **One-off scripts** → `artifacts/scripts/`.  
5. **Root** stays almost empty (only `AGENTS.md` + `README.md` + top folders).

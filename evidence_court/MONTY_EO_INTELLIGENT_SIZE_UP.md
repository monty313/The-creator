# Monty executive order — intelligent size-up

**Status:** ACTIVE in production path code  
**Order:** Owner allows the bot to **size up intelligently** toward target under the risk envelope (breach 0 still law).  
**Code:** `goal_path.intelligent_size_toward_clear` · `INTELLIGENT_SIZE_UP=True` · policy aggression EO  

## What changed

Previously, when `brain_drives`, path used **only** brain size and often **starved** clear-oriented size (`goal_path_size_for_clear`).  

EO path: **max(brain, clear-size, intelligent aggressor)** still **≤ remaining risk budget**.

| Allowed | Forbidden |
|---------|-----------|
| Larger legal size when far from target + good edge/conf | Size past worst-case daily risk (breach) |
| Prefer quality size-up over 58 micro thrash | Pad thrash for A13 cosmetics |
| Same frozen weights (meta4275) + path behavior change | Silent claim of final boss without dual |

## Measure (forward100 seed=42, same weights meta4275)

See `artifacts/eo_intelligent_size_up_forward100.json` (best measured: **V2**).

| Metric | Pre-EO floor (CASE-0037) | EO V2 dual |
|--------|-------------------------:|-----------:|
| hits | 11 | **13** |
| low_hr | 0.28 | **0.36** |
| a13_frac | 0.64 | **0.61** |
| n_zero | 18 | **18** |
| breach | 0 | **0** |
| day12 pnl (15/3) | ~2.94 | ~3.09 (still miss 15) |

**Progress:** **yes on clears** (hits +2, low_hr↑). **Not full dethrone** (a13 0.61 < 0.64 floor).

**Dethrone rule:** hits **>** 11 **and** a13 ≥ 0.64 **and** n_zero ≤ 18 **and** breach 0.

Weights fingerprint stays `meta4275`; EO is **path law**. Next: Aaron FLR reason curriculum (`PKG-002`, `meta_rl/aaron_reason_curriculum.py`) so policy **reasons** F→L→R, not only follows size instructions.

# Aaron dethrone attempt — honest non-dethrone close

**production_replace: false**  
**King unchanged:** `42:meta4275:inf0:bcfe6c74f68b7623` (CASE-0037 BEST_POLICY)

## Coherent dual (same seed=42 protocol)

| Policy | Fingerprint | hits | a13 | n_zero | breach | frozen |
|--------|-------------|-----:|----:|-------:|-------:|:------:|
| King | `42:meta4275:inf0:bcfe6c74f68b7623` | 12 | 0.61 | 18 | 0 | Y |
| Challenger (live shadow) | `42:meta5639:inf0:a75d31a20865369b` | 12 | 0.61 | 18 | 0 | Y |

- **beats_king_same_window:** false (tie ≠ beat)
- **dethrone vs FLOOR_100D (11 / 0.64 / 18):** false — blockers: `['a13 0.610<0.64']`
- Live king itself measures a13=0.61 under current goal_path (historical 0.64 not reproducible)

## Density failure (discarded as live shadow)

| Fingerprint | hits | a13 | n_zero |
|-------------|-----:|----:|-------:|
| meta11950 (density push) | 2 | 0.80 | 18 |

Hits collapsed while a13 rose — method-first forbids shipping that as progress.  
Backup: `meta_policy_aaron_reason_density_fail_meta11950.npz`

## Live shadow = best attempt (meta5639)

Restored from `meta_policy_aaron_reason_prev.npz` after density regression.

## Honest close

Challenger dual=12/0.61/18 fp=42:meta5639:inf0:a75d31a20865369b; live king dual=12/0.61/18; tie not beat; historical FLOOR a13>=0.64 blockers=['a13 0.610<0.64']; production_replace=false; density meta11950 discarded (hits collapse)

# Physics.md → path skill binding (past 35 without training child)

**Date:** 2026-08-06  
**Goal:** `best_same > 35`, `breach 0`, `growth_method=self_climb_path_skill`, skill = path dials/laws, child SHA unchanged.

## Verdict (probed)

`physics.md` is **good doctrine vocabulary**, but **blanket score-time decode does not raise past 35** on the frozen child:

- entropy / loose launch masks → **35→30** (award destruction)
- PINN against-HTF alone → **floor-neutral** (almost no bars change)
- PINN/BC into act head → **illegal** under R1 / learn≠copy for this push

Useful later as *surgical* constraints after a raise path exists; not the climb lever now.

## Map

| physics.md | PathSkillDials | Law label |
|------------|----------------|-----------|
| PINN gravity / tide | `against_htf_hold` | `pinn_against_htf` |
| Entropy chop mask | `entropy_hold` | `entropy_hold` |
| Anti-thrash pullback | `thrash_gate` | `ltf_pullback_htf_strong` / `anti_thrash` |
| Tension + mass → launch | `cont_gate` + `tension_req` | `phys_launch` / `miss_continuation_fix` |
| Aux a_mass head / ATR retrain | — | **defer** (breaks SHA) |

## Run (leave climb_35 terminal alone)

```powershell
cd C:\Users\user\Fable5_Foundation\MOMENTUM_ONE\the-truth
$env:PYTHONPATH=".;code"
python -u lineages/adaptive_rl_brain_7_31_26/self_climb_l2l.py `
  --max-rounds 18 --keep-floor 35 --goal-same 36
```

## Done criteria checklist

- [ ] `best_same > 35` with breach 0  
- [ ] `growth_method=self_climb_path_skill` in BEST  
- [ ] skill attributed to path dials / laws (`core_skill` / `skill_class`), not a single MWT day id  
- [ ] child SHA `9BDCEAAE…` unchanged  

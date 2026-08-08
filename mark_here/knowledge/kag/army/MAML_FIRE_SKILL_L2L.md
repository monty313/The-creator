# MAML fire_skill L2L — past 36

**When:** 2026-08-07  
**Status:** BEST same **36** via `fable_kag_l2l` multi-day **fire_skill**.  
**Next climb:** `the-truth/.../maml_fire_skill_meta.py` (Reptile/FOMAML + same fire_skill polish).

## KEEP36 method (preserve)

1. Collect path-family labels across **all MWT days** that share fire_skill fingerprints  
2. BC + high KL + award HOLD protect  
3. KEEP only pack same↑ and breach 0  
4. Skill attribution = family, not day id  

## Meta add-on (learn to learn)

- Task = per-day fire_skill support/query  
- Fast adapt = head-only (ANIL)  
- Slow update = Reptile (default) or FOMAML  
- Polish = KEEP36 BC recipe  
- Floor = live best (36+); child SHA history only  

## Done criteria (next)

- [ ] `best_same > 36` breach 0  
- [ ] `growth_method=maml_fire_skill_meta`  
- [ ] skill = fire_skill multi-day + meta-adapt, not single MWT day  
- [ ] child floor SHA still `9BDCEAAE…`  

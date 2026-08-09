# STATUS — forge game-train (A34 + unhinged intense)

**When:** 2026-08-08  
**Workspace:** `C:\Users\user\OneDrive\Desktop\The Creator`  
**Tracks:** forge_v1 · forge_v2 · **forge_intense** (active aggression)  
**Production champion:** **untouched**

---

## 0) forge_intense (continue — path-state first)

**Command:** `python -m evidence_court.meta_rl.cli forge train-intense --steps 20000 --continue`  
**Out:** `meta_policy_forge_intense.npz` · `42:meta32000:inf0:dc80795de305c7c1`

| train mix | value |
|-----------|------:|
| path-state pool | 400 base ×16 = **6400** |
| real-bar pool | 300 ×8 = **2400** |
| fire share applied | **96.4%** |
| steps | 12k → **32k** |
| tags (path / blitz / pack / synth / realbar) | 4287 / 8568 / 3573 / 2143 / 1429 |

### Forward 16d (honest — not coach CE)

| metric | intense 16d |
|--------|------------:|
| mean_trades | **12.75** |
| n_zero | **4 / 16** |
| a13_frac (≥8) | **0.44** (7/16) |
| breaches | **0** |
| hits | 1 (hr 0.06) |
| mean_pnl | +2.57 |
| day trades | 11,5,28,31,18,5,7,0,**67**,2,0,14,3,0,13,0 |

vs prior intense-8d (pre path-state mix): mean **5.0**, n_zero 3/8.  
**Density improved.** Conversion / dual still weak — not promote_ready.

Artifact: `intense_forward16.json`

---

## 1) Inventory

| Item | Value |
|------|------:|
| `policy_forge_export_*.json` packs | **18** |
| Sum of traj over packs (ingest volume) | **4277** |
| Approx unique traj (`ts`+teacher+reward keys) | **~370** |
| Multiplicity (sum / unique) | **~11.6×** (cumulative re-exports) |
| Format | `policy_forge_game_train_v1` · dim **176** |

### Per pack (oldest → newest)

| pack | traj | wait | long | short | align_rate | meta_steps (browser) | session |
|------|-----:|-----:|-----:|------:|-----------:|---------------------:|---------|
| …7682388 | 76 | 70 | 3 | 3 | 0.278 | 152 | asia |
| …7831626 | 97 | 89 | 3 | 5 | 0.256 | 194 | asia |
| …7947466 | 113 | 103 | 5 | 5 | 0.291 | 226 | asia |
| …8030239 | 139 | 126 | 6 | 7 | 0.321 | 278 | asia,london |
| …8096054 | 161 | 148 | 6 | 7 | 0.272 | 322 | asia,london |
| …8162399 | 186 | 170 | 8 | 8 | 0.281 | 372 | asia,london |
| …8218486 | 202 | 184 | 8 | 10 | 0.285 | 404 | asia,london |
| …8293422 | 207 | 188 | 8 | 11 | 0.282 | 414 | asia,london |
| …8391442 | 231 | 209 | 10 | 12 | 0.306 | 462 | asia,london |
| …8480227 | 249 | 225 | 10 | 14 | 0.335 | 498 | asia,london |
| …8529379 | 263 | 237 | 10 | 16 | 0.341 | 526 | asia,london |
| …8584953 | 282 | 253 | 12 | 17 | 0.339 | 564 | asia,london |
| …8670238 | 309 | 278 | 14 | 17 | 0.335 | 618 | asia,london |
| …8702432 | 317 | 283 | 15 | 19 | 0.340 | 634 | asia,london |
| …8784164 | 343 | 306 | 17 | 20 | 0.337 | 686 | asia,london |
| …8825427 | 362 | 322 | 18 | 22 | 0.336 | 724 | asia,london |
| …8849829 | 370 | 327 | 20 | 23 | 0.337 | 740 | asia,london |
| …9112547 | 370 | 327 | 20 | 23 | **0** (scoreboard blank) | 740 | asia,london |

**Latest unique session (`…8849829`):** wait 327 / long 20 / short 23 · fire density **11.6%** · sessions **asia 355 / london 15 / ny 0** · topo dominated by `slingshot_load` (225), few `launch`/`release` (27).

---

## 2) Ingest (forge_v1 only)

- **Out:** `evidence_court/artifacts/game_train/meta_policy_forge_v1.npz` (+ `.json`)
- **Order:** oldest → newest, pack 1 with `--from-prior`, packs 2–18 continue same out
- **Teacher only** (`teacher_act`); player acts stored in packs but not used as CE target
- **Result:** `meta_train_steps` **0 → 4277** · fingerprint `42:meta4277:inf0:a990cc48c90160aa`
- **Champion:** `42:meta9600:inf0:f2b9be0dc2fe359e` before **and** after → **untouched**

Mean CE during ingest fell from ~0.35 (first pack) to ~0.017 (last pack) — expected under multi-pass wait-heavy data.

---

## 3) Evaluation (honest)

### A) Multi-pass aggregate (all 18 packs, n=4277) — train-contaminated holdout

| metric | untrained prior (holdout) | forge_v1 (holdout) |
|--------|--------------------------:|-------------------:|
| coach agreement | 0.752 | **0.998** |
| mean CE | 0.856 | **0.021** |
| pred wait frac | 0.768 | **0.882** (flag) |
| fire-side accuracy | 0.359 | **0.981** |

### B) Latest clean pack only (n=370 unique end session) — better honesty check

| metric | prior | forge_v1 |
|--------|------:|---------:|
| coach agreement | 0.757 | **0.997** |
| mean CE | 0.853 | **0.021** |
| pred wait frac | 0.773 | **0.886** (flag) |
| fire-side accuracy | 0.349 | **0.977** |

### Brutal truth

1. **Packs helped coach-fit hard** — CE crash + fire-side accuracy ~98% on coach labels.  
2. **But data is wait-skewed** — labels ~90% wait; topology mostly load/chop; **almost no NY**, london only 15/370 bars.  
3. **Multi-pass re-exports (~11.6×)** replay the same early Asia waits many times → **wait bias flag true**; high agreement is partly “learn wait everywhere.”  
4. **Human align_rate ~0.28–0.34** in scoreboard — player often disagrees with coach; we correctly train on **teacher**, not player mistakes.  
5. **forge_v1 is NOT Court-ready / not promote_ready** — no dual conversion, no A13 density on real bars, no multi-seed prove. Coach-CE ≠ mission.

---

## 4) Did packs help?

| Question | Answer |
|----------|--------|
| Offline coach map improved vs seed prior? | **Yes** (CE 0.85 → 0.02) |
| Fire direction on coach fire bars? | **Yes** (~98%) |
| Enough real fire density / London-NY story? | **No** — fire ~12%, NY=0 |
| Safe to replace production champion? | **No** — leave champion alone |
| Ready for promote? | **No** — experimental track only |

---

## 5) What to play next in Policy Forge

1. **Fire days** — force `launch` / `release` pullbacks with HTF support (raise fire density well above ~12%).  
2. **London + NY** sessions (current unique pack: london 4%, **ny 0%**).  
3. Bread-and-butter pullbacks after trend — not Asia slingshot_load grind.  
4. **One export at end of a long run** (or dedupe) — stop stacking cumulative re-exports (11× wait multi-pass).  
5. Raise **player align_rate on fire bars** with Coach; still export `teacher_act` as train signal.

Launch (if needed):

```text
python evidence_court/meta_rl/game_train/launch_policy_forge.py
```

---

## 6) Commands run

```text
# cwd
cd C:\Users\user\OneDrive\Desktop\The Creator

# inventory
python evidence_court/artifacts/game_train/_inventory_eval.py inventory

# ingest oldest→newest → forge_v1 only (pack1 --from-prior)
python -m evidence_court.meta_rl.cli game-ingest <pack_i.json> ^
  --out evidence_court/artifacts/game_train/meta_policy_forge_v1.npz ^
  --lr 0.02 [--from-prior on first only]

# eval
python evidence_court/artifacts/game_train/_inventory_eval.py eval
```

**Outputs**

- `evidence_court/artifacts/game_train/meta_policy_forge_v1.npz`
- `evidence_court/artifacts/game_train/meta_policy_forge_v1.json`
- `evidence_court/artifacts/game_train/meta_policy_forge_v1_game_ingest.json`
- `evidence_court/artifacts/game_train/meta_policy_forge_v1_report.json`
- this file: `STATUS.md`

**Not modified:** `evidence_court/artifacts/meta_policy_champion.npz` / `.json`

---

## 7) Waiting on Monty

Next instruction options (do not auto-promote):

- **more play** → new export (prefer single end-of-run pack, London/NY fire)  
- **re-ingest deduped** → train once on unique 370 only (less wait multi-pass)  
- **Court issues** → C-003 / C-002 residual / senses  
- **promote?** → not recommended until dual/A13 measured on real path  

**goal_achieved:** still **false**

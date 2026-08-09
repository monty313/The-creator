# How to use it

**Simple steps.**  
Copy one block at a time.

---

## Before you start

### What you need

- This project folder open  
- Price data already set up (same as normal prove)  
- Python environment that already runs Evidence Court  

### Safety rules (read first)

| Rule | Why |
|------|-----|
| Practice on a **shadow** file first | Do not break the champion by accident |
| **Do not** train during prove / forward | Freeze at inference (A14) |
| Measure with **forward100** before promote | Numbers, not vibes |
| Replace champion only after Court / clear ok | Production rule |

**Champion file (production):**  
`evidence_court/artifacts/meta_policy_champion.npz`

**Backup from last promote:**  
`evidence_court/artifacts/meta_policy_champion_pre0037.npz`

---

## The three jobs

| Job | What you do | Output |
|-----|-------------|--------|
| **1. Harvest** | Collect teacher cards from real days | JSON pack of examples |
| **2. Train** | Offline practice on those cards | Shadow `.npz` brain |
| **3. Measure** | Score shadow vs champion floor | Report JSON |

Only after measure (and Court if you change production) do you promote.

---

## Job 1 — Harvest teachers

### What harvest means

Run real day paths.  
Turn on: “when brain waits on a real Mark setup, save the state.”

Flag name in code:

`collect_path_state_teachers=True`

Default on normal dual / prove is **False**  
(so production days stay fast and clean).

### Code path

Module:

`evidence_court/meta_rl/path_state_harvest.py`

Main function:

`harvest_path_state_teachers(...)`

What it does:

1. Loads symbols (often XAUUSD, EURUSD, GBPUSD)  
2. Walks about **30** eval days (plus warmup)  
3. Each day: run path with collect flag **on**  
4. Keeps up to about **400** good examples  
5. Prefers clean full-dim long/short PB/cont teachers  

### Last saved pack (already in repo)

`evidence_court/artifacts/path_state_teachers_case0037.json`

That pack had about:

- **400** teachers  
- **362** London / NY  
- Full **176**-dim states  

### Example Python (lab harvest)

Run from project root (`The Creator`):

```python
from pathlib import Path
from evidence_court.meta_rl.path_state_harvest import (
    harvest_path_state_teachers,
    save_path_state_pack,
)

pack = harvest_path_state_teachers(
    n_days=30,
    seed=42,
    max_examples=400,
)

out = save_path_state_pack(
    pack,
    Path("evidence_court/artifacts/path_state_teachers_lab.json"),
)
print("saved", out)
print("n_examples", pack.get("n_examples"))
print("n_london_ny", pack.get("n_london_ny"))
print("dims_ok", pack.get("dims_ok"))
```

### What “good” harvest looks like

| Check | Good |
|-------|------|
| n_examples | More than zero (often hundreds) |
| dims_ok | **True** |
| n_london_ny | High share of total |
| source | path_state style (not synthetic rebuild) |

---

## Job 2 — Train offline

### What train means

1. Start from a base meta curriculum (or existing brain).  
2. Feed path-state teachers with **meta_update**.  
3. Save a **shadow** `.npz`.  
4. Freeze for measure.

### Code path

Function:

`train_path_state_a13_policy(...)`

Also:

`apply_path_state_teachers_to_brain(...)`  
(for applying teachers onto an existing brain)

### Example Python (shadow train)

```python
import json
from pathlib import Path
from evidence_court.meta_rl.path_state_harvest import (
    train_path_state_a13_policy,
)

raw = json.loads(
    Path("evidence_court/artifacts/path_state_teachers_case0037.json")
    .read_text(encoding="utf-8")
)
examples = raw["examples"] if isinstance(raw, dict) else raw

pol = train_path_state_a13_policy(
    examples,
    seed=42,
    n_steps=2500,
    path_mix=0.35,
    freeze=True,
    save_path=Path(
        "evidence_court/artifacts/meta_policy_pathstate_shadow.npz"
    ),
)
print("steps", pol.meta_train_steps)
print("fp", pol.weight_fingerprint())
```

### Safe vs unsafe output paths

| Path | Safe? |
|------|-------|
| `artifacts/meta_policy_pathstate_shadow.npz` | Yes (lab) |
| `artifacts/meta_policy_case0037_pathstate.npz` | Historical promote source |
| `artifacts/game_train/*.npz` | Lab only |
| `artifacts/meta_policy_champion.npz` | **Only after measure + clear promote** |

---

## Job 3 — Measure

### Fast identity check (current champion)

```bash
python -m evidence_court.meta_rl.cli prove 15 2
```

### Full dual on default champion (slow)

```bash
python -m evidence_court.meta_rl.cli forward100 --days 100 --out evidence_court/artifacts/forward100_report.json
```

### Measure a shadow brain (important)

```bash
python -m evidence_court.meta_rl.cli forward100 --days 100 --champion-path evidence_court/artifacts/meta_policy_pathstate_shadow.npz --out evidence_court/artifacts/forward100_shadow_pathstate.json
```

### Floor to beat (or at least not break)

From CASE-0037 / `BEST_POLICY.md` (seed 42, 100 days):

| Metric | Floor to respect |
|--------|------------------:|
| hits | ≥ **11** (prefer hold) |
| low_hr | ≥ **0.28** |
| a13_frac | ≥ **0.64** (new floor after 0037) |
| breach | **0** |
| no_retrain | **true** |

If your shadow is worse on prefer metrics, **do not** promote.

---

## Unit tests (quick pin)

```bash
python -m pytest evidence_court/tests/test_case0037_path_state_teachers.py -q
```

Green tests mean the **mechanics** still work.  
They do **not** replace a full forward100 dual.

---

## How production uses it today

| Setting | Production dual / prove | Lab harvest |
|---------|-------------------------|-------------|
| Brain drives | On | On |
| Watch | Observe | Observe |
| collect_path_state_teachers | **Off** (default) | **On** |
| Live force-pad trades | **Never** | **Never** |
| Weights | Frozen champion | Train shadow only |

So:

- **Live day:** brain acts; no harvest required.  
- **Learn more:** harvest offline → train shadow → measure → maybe promote.

---

## Continue training the champion (same class)

Yes — you can train more offline.

Safer pattern:

1. Harvest more path-state teachers (more days / residual silent days).  
2. Train a **shadow**.  
3. Measure shadow.  
4. Only then replace champion + update `BEST_POLICY.md`.

Riskier pattern:

- Point train straight at `meta_policy_champion.npz`  
- Only do that when you accept the risk and will measure right after.

Also ok for base curriculum (different lever):

```bash
python -m evidence_court.meta_rl.cli meta-train --steps 2000
```

That continues offline meta-train (default out = champion).  
Prefer shadow when experimenting.

---

## What NOT to use as teachers

| Bad teacher | Why |
|-------------|-----|
| Synthetic densify only | F-024 class — thrash / worse silent days |
| Real label + rebuilt fake state | F-025 class — wrong eyes |
| Live force every bar | Fake A13 — not learning |
| Wait-copy game diet only | Learns “WAIT wins,” quiet on path |
| Random thrash long/short | Noise labels |

Stick to:

**packed path state + Mark long/short + PB/cont.**

---

## Checklist (print this)

Before you say “the bot learned more”:

- [ ] Teachers are full packed path states (176-dim)  
- [ ] Teachers are brain-wait + Mark fire side  
- [ ] London / NY present in the pack  
- [ ] Trained offline only  
- [ ] Shadow measured with forward100  
- [ ] breach = 0  
- [ ] Prefer floor not broken (hits / low_hr / a13)  
- [ ] Champion replaced only on purpose + docs updated  

---

## Where to look if stuck

| Problem | Look here |
|---------|-----------|
| No examples harvested | Price data / symbols / collect flag |
| dims_ok false | State packing bug — stop and fix |
| a13 up but hits crash | Bad thrash teachers — do not promote |
| Want skill map for humans | `00_HIGH_TREND_MASTERY.html` in game_train |
| Court history | `cases/CASE-0037-path-state-teachers.md` |
| What is production now | `evidence_court/BEST_POLICY.md` |

---

**Next file:** `03_IMPROVEMENTS_BEFORE_AFTER.md`

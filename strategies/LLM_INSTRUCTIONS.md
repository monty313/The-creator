# LLM instructions — `strategies/` full prove pipeline

**Audience:** any future LLM (or human operator) adding or re-processing strategies in this folder.  
**Goal:** every strategy gets the **same full prove process** used on the original 125 families — language → inventory → baseline batch → accuracy → (optional head-to-head) → Monte Carlo → results written into **its own files**.  
**Not Court law. Not production brain. Not a promote path.** Lab claims only.

Read this file **before** inventing a shorter path. Skipping steps = incomplete prove.

---

## 0. Permanent rules (never soft-pedal)

| # | Rule | Forbidden |
|---|------|-----------|
| R1 | Work **only under `strategies/`** unless Monty opens Court | Smuggling adapters into `evidence_court` as law |
| R2 | MT4/MT5 = **language only** + **cited paths** | Dumping full EA source as “the bot” |
| R3 | **1:1 no-collapse** — every name/note is its own `family_id` | Merging “similar” EAs into one rank row |
| R4 | Same **lab contract** for every family (below) | One-off charts / freestyle windows as proof |
| R5 | Results must land **in that strategy’s files** | Report-only with empty tweak/ranked docs |
| R6 | Claims stay **lab claims** | Calling WR/MC “Court PROMOTE” or final boss done |
| R7 | Logic **reuse OK** via `adapter_profile`; ids stay unique | Collapsing family_ids because scores match |

### Lab contract (every batch, tweak, MC)

| Piece | Value |
|-------|--------|
| Structure | **2 HTF + 1 LTF** |
| Sets | Official MARK sets in `python_batch/mtf.py` → `OFFICIAL_SETS` |
| Modes | **pullback** + **continuation** |
| Engine | **vectorbt** `Portfolio.from_signals` |
| Bars | Default tail **40_000** M1 |
| Default data | EURUSD M1 export path in runners (`DEFAULT_DATA`; fallback `ALT_DATA`) |
| Fees / slip | as in runners (`FEES`, `SLIP` / `SLIPPAGE`) |
| Accuracy shell | session 07–21 UTC, HTF strength, bar confirm, micro structure (see `accuracy_tweaks.py`) |
| Default exits (accuracy/MC) | first-breath TP/SL (~`tp=0.00025`, `sl=0.001`) unless a family upgrade documents otherwise |

### Gates (must pass before “done”)

| Gate | Requirement |
|------|-------------|
| **G-INV** | Family appears in `FAMILY_INVENTORY_1TO1.json` with `collapses: []` |
| **G-BASE** | Baseline row in `STRATEGY_TEST_REPORT.json` (or sauces report if sauce) |
| **G-WR** | Post-tweak **win rate > 60.4%** and **trades ≥ 25** (aggregate over sets×modes) |
| **G-DOC** | `tweaks/<family_id>.md` has what / why / scores |
| **G-MC** | Row in `MONTE_CARLO_RESULTS.json` (bootstrap + shuffle) |
| **G-INJECT** | MC block in `tweaks/<family_id>.md`; if ranked, all-sim block in `ranked/*_<family_id>/README.md` |

**Done for a family** = all gates green. Not “I ran one script.”

---

## 1. Folder map (where things live)

```text
strategies/
  LLM_INSTRUCTIONS.md          ← THIS FILE (process SSOT for LLMs)
  README.md                    ← short index + re-run pointers
  00_intuition.md              ← Mark teaching notes (not promote list)
  language/                    ← language-only catalogs + citations
  <source buckets>/            ← note prose copies (see inventory NOTE_DIRS)
  sauces/                      ← special sauce language (McFlurry, Dimension Jump, …)
  python_batch/                ← all runners + adapters
  FAMILY_INVENTORY_1TO1.json   ← canonical 1:1 family list
  STRATEGY_TEST_REPORT.*      ← baseline batch
  ranked/                      ← one folder per baseline rank
  TWEAKED_ACCURACY_*.*         ← accuracy gate results
  tweaks/                      ← one markdown per family (what/why/scores + MC)
  SAUCES_TEST_REPORT.*         ← sauce baseline
  CCI_VS_MCFLURRY_*.*          ← optional CCI vs McFlurry head-to-head
  MONTE_CARLO_*.*              ← MC distributions + by-file index
  SIM_RESULTS_INJECT_REPORT.md ← inject coverage proof
```

### Source buckets scanned as **notes** (`inventory_1to1.NOTE_DIRS`)

- `local_desktop/`
- `army_library_strategy_copy/`
- `army_snap8/`
- `mark_doctrine_refs/`
- `the_truth_main_extra/`
- `algo_guide_14/` — 14 strategies from `Strategies to replicate in Algo Trading.docx.html`

Skip: `SOURCE.md`, `README.md`, `README_FACTORY.txt`.

**Guide-14 one-shot prove:** `python -m strategies.python_batch.run_prove_guide14`  
(adapters: `families_guide14.py` · report: `ALGO_GUIDE_14_PROVE_REPORT.md`)

### MT language

- Table SSOT: `language/01_METATRADER_INDEX.md`
- Longer notes: `language/01_METATRADER.md`, `02_MACHINE_SOURCES.md`, `03_PUBLIC_SOURCES.md`
- Citation rules: `language/README.md`

---

## 2. Family id conventions

| Kind | `family_id` pattern | Example |
|------|---------------------|---------|
| MetaTrader name | `mt__<slug>` | `mt__cci_gravity_scalp_ftmo` |
| Note file | `note__<bucket>_<slug>_md` | `note__army_snap8_STRATEGY_md` |
| Sauce | `sauce__<slug>` | `sauce__mcflurry_eddy_scalp` |

- **Never rename** an existing id after reports exist (breaks rank/tweak/MC join).  
- New file → new id. Versioned EA names stay separate rows (`_v2`, `_v5`, …).

---

## 3. How to add a **new** strategy (full path)

Pick the type, then execute **every** step in §4 in order.

### 3A. New MetaTrader / EA language entry

1. Add a row to `language/01_METATRADER_INDEX.md` (name, platform, summary, **source path**).  
2. Optionally expand prose in `language/01_METATRADER.md` with citation.  
3. **Do not** paste full `.mq5` bodies into language docs.  
4. Map language → adapter in `python_batch/inventory_1to1.py` → `pick_profile(...)`.  
5. If no profile fits: implement `fam_*` in `python_batch/families.py`, register in `profiles.PROFILES`.  
6. Continue §4 from inventory rebuild.

### 3B. New strategy **note** (markdown/txt)

1. Place file under one of `NOTE_DIRS` (or add a new dir to `NOTE_DIRS` + document it here).  
2. Add `SOURCE.md` in that bucket if paths/URLs need a home.  
3. Ensure `pick_profile` maps title/path → a real profile (or add profile).  
4. Continue §4.

### 3C. New **sauce** (named special strategy)

1. Write language under `sauces/<Name>.md` with sources.  
2. Implement `fam_<name>` in `families.py`; register profile key in `profiles.PROFILES`.  
3. Wire into sauce runner + tweak/MC sauce hooks (same pattern as McFlurry / Dimension Jump in `run_sauces_test.py`, `run_tweak_batch.py`, `run_monte_carlo.py`).  
4. Baseline via sauces runner **and** include in full tweak + MC (sauces are part of the 125-style universe).  
5. Continue §4 (sauces may not get a `ranked/` folder if baseline 1:1 inventory excludes them — still require `tweaks/sauce__*.md` + MC + sauce note inject).

### 3D. New **adapter profile** (shared logic)

1. Add `fam_xxx(sb: SetBars) -> (bull, bear, modes)` in `families.py`.  
2. Modes must supply pullback long/short + continuation long/short masks.  
3. Register in `profiles.PROFILES`.  
4. Point one or more families at it via `pick_profile` or inventory override.  
5. Prefer geometry that respects **HTF side / LTF timing** (see `00_intuition.md`).

---

## 4. Mandatory pipeline (order is binding)

Run from **repo root** (`The Creator`). Prefer project venv if present. Requires **vectorbt** (lab used 1.1.0).

```text
# 0) Sanity
python -c "import vectorbt; print(vectorbt.__version__)"

# 1) Rebuild 1:1 inventory
python -m strategies.python_batch.inventory_1to1
# → FAMILY_INVENTORY_1TO1.json
# VERIFY: new family_id present, collapses == []

# 2) Baseline full batch (all 1:1 families)
python -m strategies.python_batch.run_strategy_batch_1to1
# → STRATEGY_TEST_REPORT.md / .json
# → ranked/INDEX.md + ranked/NNN_<family_id>/README.md
# → RANKED.md

# 2b) If sauces changed
python -m strategies.python_batch.run_sauces_test
# → SAUCES_TEST_REPORT.md / .json

# 3) Smoke (do not skip)
python -m pytest strategies/python_batch/test_batch_1to1_smoke.py -q
python -m pytest strategies/python_batch/test_tweak_winrate.py -q
# (optional) test_batch_smoke.py

# 4) Accuracy tweaks — ALL families must clear WR > 60.4%
python -m strategies.python_batch.run_tweak_batch
# → TWEAKED_ACCURACY_REPORT.md / .json
# → tweaks/<family_id>.md for every family

# 5) Optional head-to-head (only if claim needs it)
#    e.g. CCI family must beat McFlurry on WR + profit:
python -m strategies.python_batch.run_cci_vs_mcflurry
# → CCI_VS_MCFLURRY_REPORT.md / .json
#    Update the relevant tweaks/*.md “what changed / why / scores” sections.

# 6) Monte Carlo — ALL families
python -m strategies.python_batch.run_monte_carlo --sims 1000 --seed 42
# → MONTE_CARLO_RESULTS.json
# → MONTE_CARLO_REPORT.md

# 7) Inject simulation results into every strategy file
python -m strategies.python_batch.inject_all_sim_results
# → refreshes MC in tweaks/*.md + sauces notes
# → full all-sim blocks in ranked/*/README.md
# → SIM_RESULTS_INJECT_REPORT.md
#    Also maintain / regenerate MONTE_CARLO_BY_FILE.md if your MC runner writes it;
#    if not, rebuild the rank→file table from MONTE_CARLO_RESULTS.json.

# 8) Coverage verify (must be zero missing)
python -c "
import json
from pathlib import Path
root = Path('strategies')
mc = json.loads((root/'MONTE_CARLO_RESULTS.json').read_text(encoding='utf-8'))
ids = {r['family_id'] for r in mc['results']}
tweaks = {p.stem for p in (root/'tweaks').glob('*.md')}
missing_t = sorted(ids - tweaks)
no_mc = [p.name for p in (root/'tweaks').glob('*.md') if 'MONTE_CARLO_BEGIN' not in p.read_text(encoding='utf-8')]
print('mc_n', len(ids), 'tweaks', len(tweaks), 'missing_tweak_files', missing_t[:20], 'tweaks_without_mc_block', len(no_mc))
"
```

### After any **single** new family

Minimum acceptable path (still full gates):

1. Language / note / sauce file + profile wiring  
2. Inventory includes it  
3. Re-run **baseline batch** (or document why only delta-run — prefer full re-run for scoreboard honesty)  
4. Re-run **tweak batch** (at least until that family passes G-WR; full re-run preferred)  
5. Re-run **Monte Carlo** (full universe so ranks stay comparable)  
6. **Inject** again  
7. Confirm that family’s files show batch + accuracy + MC numbers  

**Do not** hand-edit scores without re-running the batch that owns them.

---

## 5. What each stage must produce per family

### 5.1 Inventory row

Fields (see `FamilySpec` in `inventory_1to1.py`):

- `family_id`, `kind` (`mt` | `note` | sauce handled separately), `title`, `source`  
- `adapter_profile`, `fidelity`, `collapses` (**always `[]`**)

### 5.2 Baseline batch (`STRATEGY_TEST_REPORT`)

Per family aggregate + per set×mode rows. Rank folder:

```text
ranked/NNN_<family_id>/README.md
```

Must later contain `<!-- ALL_SIM_RESULTS_BEGIN -->` … after inject.

### 5.3 Accuracy tweak file (`tweaks/<family_id>.md`)

Must document:

1. **What** changed (tier params, filters, signal changes)  
2. **Why** (Mark/geometry rationale — not vanity)  
3. **Scores** (WR, trades, return, PF, DD, sharpe, pass/fail vs 60.4%)  
4. After MC inject: **`<!-- MONTE_CARLO_BEGIN -->` … `<!-- MONTE_CARLO_END -->`**

Tiers live in `run_tweak_batch.TIERS` (`A_first_breath` …). Prefer first tier that clears the gate with real trades; do not fake trades.

### 5.4 Monte Carlo row

From `run_monte_carlo.py` (defaults: **1000** sims, seed **42**):

- Trade book: pooled returns under accuracy shell + first-breath stops  
- Bootstrap: median/mean/p05–p95 terminal, P(loss), P(DD≥20%), path DD  
- Order-shuffle: median/p05 terminal, P(loss)  

Write into family files — not only the global report.

### 5.5 Inject report

`SIM_RESULTS_INJECT_REPORT.md` must show:

- tweaks with MC block = all MC family ids  
- ranked all-sim blocks = all ranked dirs  
- sauces MC if sauce files exist  
- **0 missing**

---

## 6. Per-strategy checklist (copy for each new id)

```markdown
## Prove checklist: `<family_id>`

- [ ] Language / note / sauce filed with **source citation**
- [ ] Profile mapped (`pick_profile` or sauce register) — not silent wrong default without note
- [ ] In `FAMILY_INVENTORY_1TO1.json` (or sauce registry) · collapses []
- [ ] Baseline metrics in STRATEGY_TEST_REPORT (or SAUCES_TEST_REPORT)
- [ ] `ranked/*_<family_id>/` exists if 1:1 baseline family
- [ ] Accuracy: WR > 60.4% · trades ≥ 25
- [ ] `tweaks/<family_id>.md` what + why + scores
- [ ] Monte Carlo row in MONTE_CARLO_RESULTS.json
- [ ] MC block in tweaks file
- [ ] All-sim block in ranked README (if applicable)
- [ ] Sauce note MC block (if sauce)
- [ ] No claim of Court PROMOTE / production law
```

---

## 7. Special procedures already in the corpus

### 7.1 CCI upgraded vs McFlurry

When owner requires a family to beat a **reference sauce** on WR **and** profit:

1. Improve **signal geometry** first (example: reclaim-only + HTF force + M-line), not only TP vanity.  
2. Run `run_cci_vs_mcflurry` (or clone that runner for a new pair).  
3. Document upgrade in the family’s tweak file.  
4. Re-run accuracy + MC + inject so files match.

### 7.2 Accuracy shell intent (Mark)

Use as default before inventing new dials:

1. Dual HTF strength (real force, not flat mass)  
2. London/NY session concentration  
3. Entry bar agrees with side  
4. Micro HL/LH structure  
5. **First breath** exits: tight TP, wider SL; avoid thrashy time-stops that pin WR ~50%  

Read `00_intuition.md` for teaching geometry — it is **not** a ranked promote list.

### 7.3 Monte Carlo reading (honest)

- High hist WR + high **P(loss)** → fragile book / costs / path risk  
- Very low trade count → unstable percentiles  
- MC med > 1 only means bootstrap paths often finish > start **on this lab book** — not live prop proof  

---

## 8. Forbidden shortcuts

| Shortcut | Why forbidden |
|----------|----------------|
| “Profile matches X, skip testing” | 1:1 rule; each id must prove |
| Report JSON only, no tweak file | Fails G-DOC |
| Accuracy pass without MC | Fails G-MC |
| MC report without inject into family files | Fails G-INJECT |
| Changing TP only to force WR, no entry thesis | Vanity accuracy |
| Collapsing v2/v5 EAs into one family | Breaks R3 |
| Calling results Court law / BEST_POLICY | Out of scope |
| Full-disk recursive scans that hang the session | Use cited paths + bounded inventory |
| Editing ranked scores by hand | Must come from batch JSON |

---

## 9. Re-run matrix (when to re-run what)

| Change | Inventory | Baseline batch | Sauces | Tweak batch | H2H | MC | Inject |
|--------|:---------:|:--------------:|:------:|:-----------:|:---:|:--:|:------:|
| New MT index row / note file | ✓ | ✓ | | ✓ | | ✓ | ✓ |
| New sauce | ✓* | | ✓ | ✓ | maybe | ✓ | ✓ |
| New/changed `fam_*` profile | | ✓ | if sauce | ✓ | if claim | ✓ | ✓ |
| Accuracy tier defaults | | | | ✓ | | ✓ | ✓ |
| Data path / window / fees | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Docs-only typo | | | | | | | |

\*Sauces may sit outside 1:1 MT/note inventory but still need registry + full prove gates.

Prefer **full universe** re-runs so ranks and MC ranks stay comparable. If time-bound, still produce complete artifacts for **touched** families and note partial run in the report meta.

---

## 10. Definition of “process complete” for the folder

After a full cycle:

1. Every inventoried family + every sauce has cleared **G-INV … G-INJECT**.  
2. `TWEAKED_ACCURACY_REPORT` shows **pass_count == family_count** (WR gate).  
3. `MONTE_CARLO_RESULTS.json` `n_families` matches the tested universe.  
4. `SIM_RESULTS_INJECT_REPORT.md` shows **0 missing**.  
5. `README.md` artifact table still points at current reports.  
6. Operator/LLM summary lists any **failed** families explicitly (never hide fails).

---

## 11. Commands quick card

```text
python -m strategies.python_batch.inventory_1to1
python -m strategies.python_batch.run_strategy_batch_1to1
python -m strategies.python_batch.run_sauces_test
python -m strategies.python_batch.run_tweak_batch
python -m strategies.python_batch.run_cci_vs_mcflurry
python -m strategies.python_batch.run_monte_carlo --sims 1000 --seed 42
python -m strategies.python_batch.inject_all_sim_results
python -m pytest strategies/python_batch/test_batch_1to1_smoke.py strategies/python_batch/test_tweak_winrate.py -q
```

---

## 12. Code ownership map

| Module | Job |
|--------|-----|
| `inventory_1to1.py` | Build 1:1 family list + `pick_profile` |
| `profiles.py` | profile key → adapter |
| `families.py` | Signal adapters (`fam_*`) |
| `mtf.py` | Load CSV, official sets, HTF gate, exits helpers |
| `indicators.py` | Shared indicators |
| `accuracy_tweaks.py` | Entry shell filters |
| `run_strategy_batch_1to1.py` | Baseline batch + ranked/ |
| `run_sauces_test.py` | Sauce baseline |
| `run_tweak_batch.py` | Accuracy gate + tweaks/*.md |
| `run_cci_vs_mcflurry.py` | Optional H2H |
| `run_monte_carlo.py` | Bootstrap + shuffle MC |
| `inject_all_sim_results.py` | Write sims into family files |

---

## 13. Session opening script (for any LLM)

When Monty says “add a strategy” or “prove strategies folder”:

1. Open **this file** and the target language/note/sauce path.  
2. State which type (3A / 3B / 3C) and the new `family_id`.  
3. Execute §4 in order; do not jump to MC first.  
4. Paste the §6 checklist filled for that id at the end.  
5. Point to the family’s `tweaks/*.md` (and ranked README if any) as the durable prove record.

If anything is blocked (missing data CSV, vectorbt missing, profile unknown): **stop and report** — do not invent silent pass scores.

---

## 14. Historical baseline (reference, not a free pass)

Original full corpus (lab):

- ~95 MT + ~28 notes = **123** 1:1 families  
- + **2** sauces = **125** accuracy + MC universe  
- Win-rate gate **60.4%**, MC **1000** sims seed **42**, EURUSD M1 ~40k window  

New strategies must meet the **same process**, not “close enough because the old folder already passed.”

---

**SSOT for process:** this file (`strategies/LLM_INSTRUCTIONS.md`).  
**SSOT for short human index:** `strategies/README.md`.  
**SSOT for geometry teaching:** `strategies/00_intuition.md`.  
**Not SSOT for Court:** anything under `evidence_court/` (separate mission).

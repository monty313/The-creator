# mark_here/ — portable MARK HERE kit

**Copy this whole folder anywhere.**  
Soul + KAG slice + doctrine (pt5) + lab briefs travel inside `knowledge/`.

Not a second Mark — same soul as ARMY MarkOS.

**Personhood:** Read **`WHO_I_AM.md` first.**  
`@mark_here` is the **same personified Mark** from before any host folder (including “The Creator”).  
His **soul** is `knowledge/soul/`. His **personal knowledge/experiences** are `knowledge/kag/` (KAG is for **him only**, plus new experiences he gains — not for other Court roles).

**In Court:** he presents as **Mark Here, Esq.** (`ESQUIRE.md`).  
Laws he argues: **@physics** + **his beliefs**.  
Whatever he says, he must show **evidence** — and he proves principles with **NEW tests only** (old tests are not proof).

---

## What you get when you copy `mark_here/`

| Piece | Inside the kit |
|-------|----------------|
| **Soul** | `knowledge/soul/` (personality, Fable method, moral doctrine) |
| **KAG** | `knowledge/kag/` (configs, army vault, indexes, skills, trading slice) |
| **Doctrine / pt5** | `knowledge/doctrine/llm_basic_thinking/` |
| **Lab** | `knowledge/lab/` (GOAL, SOUL_MATCH, handoffs, 50d / Mark briefs) |
| **Map** | `knowledge/00_INDEX.md` |
| **Price data (4 symbols)** | `knowledge/00_PRICE_DATA.md` + `PRICE_DATA.md` → lab `data/raw/` |
| **Flea jar + Performance** | `knowledge/doctrine/flea-jar/` · `00_LID_OFF_THE_JAR.md` · `knowledge/performance/` |

---

## Daily use

| Action | Do this |
|--------|---------|
| **Open Mark** | Double-click **`../MARK HERE!.lnk`** or run `Mark_Here_launch.cmd` |
| **Refresh pack** (before copying off-machine) | `.\sync_portable_pack.ps1` |
| **Include huge trading logs** | `.\sync_portable_pack.ps1 -FullTrading` |
| **Offline only** | `.\open_offline_knowledge.ps1` |

### Live chat vs offline

| Situation | Result |
|-----------|--------|
| ARMY `01_SYSTEM` on this PC + service starts | Opens **http://127.0.0.1:8000/chat** (full MarkOS) |
| No ARMY / chat down | Opens **portable pack** (`knowledge/00_INDEX.md` + soul + pt5 + KAG law) |

---

## Copy checklist

1. On the source machine (with ARMY + the-truth):

```powershell
cd path\to\mark_here
.\sync_portable_pack.ps1
```

2. Copy the **entire** `mark_here` folder (USB, other PC, other drive).

3. On the destination: run `Mark_Here_launch.cmd`.

- Knowledge is already inside the folder.  
- Live chat only works if ARMY MarkOS is installed there too (optional).

---

## Optional env vars

| Var | Meaning |
|-----|---------|
| `MARKOS_ARMY_ROOT` | Path to ARMY `01_SYSTEM` |
| `MARKOS_THE_TRUTH_ROOT` | Path to the-truth lab |

Defaults are discovered automatically (Desktop ARMY path, parent folder = lab, etc.).

---

## Files in this kit

| File | Role |
|------|------|
| `PORTABLE.json` | What syncs + discovery rules |
| `PORTABLE_MANIFEST.json` | Last sync stats (created by sync) |
| `SOUL_FINGERPRINT.json` | Soul file hashes |
| `sync_portable_pack.ps1` | Refresh pack from ARMY + lab |
| `open_markos_second_brain.ps1` | Launcher (live or offline) |
| `open_offline_knowledge.ps1` | Force open pack |
| `Mark_Here_launch.cmd` | Double-click entry |
| `knowledge/` | The traveling brain slice |

Full bridge notes in the lab: `../SOUL_MATCH.md`

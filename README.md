# The Creator — Evidence Court

**Owner:** Monty  
**Mission:** one bot · any target/risk · no retrain after final policy · breach 0 · scalper 8–400/day · senses drive the brain.

---

## Folder map (start here)

```text
The Creator/
├── README.md                 ← you are here
├── AGENTS.md                 ← auto-loaded Court laws for Grok
├── docs/                     ← procedure + project docs
│   ├── grok_cli_evidence_court_v2.md
│   └── project/
├── tools/                    ← launch scripts (TradingView CDP, …)
├── 00_PATH_STATE_TEACHERS/   ← plain-language path-state training
├── 00_PATH_LEARNING/         ← path-learning road
├── Aaron_here/               ← Teacher of Learning kit
├── Learning-How_to/          ← curriculum progress
├── evidence_court/           ← Court + meta-RL brain (main lab)
│   ├── BEST_POLICY.md        ← production champion SSOT
│   ├── arbitration/          ← personified / day12 / dethrone seats
│   ├── artifacts/            ← outputs (organized — see inside README)
│   ├── cases/ · ledger/ · meta_rl/ · schedules/ · tests/
│   └── *.md law files
├── mark_here/                ← Mark knowledge + ESQUIRE
└── strategies/               ← strategy geometry library (not production brain)
    ├── reports/              ← batch test reports
    └── _scratch/             ← noise / exports
```

---

## Daily commands

| Goal | Command |
|------|---------|
| Prove champion | `python -m evidence_court.meta_rl.cli prove 15 2` |
| Load laws | open `AGENTS.md` + `evidence_court/BEST_POLICY.md` |
| TradingView CDP | `tools/tradingview/start_tradingview_cdp.bat` |
| Path teachers (how) | `00_PATH_STATE_TEACHERS/README.md` |

---

## What stays “hot” (do not bury)

| Path | Why |
|------|-----|
| `evidence_court/artifacts/meta_policy_champion.npz` | Production brain weights |
| `evidence_court/BEST_POLICY.md` | Champion identity |
| `evidence_court/ISSUE_DOCKET.md` | Live blockers |
| `AGENTS.md` | Session law |

Lab shadows live under `artifacts/policies_lab/`.  
Reports → `artifacts/reports/`. Day-12 work → `artifacts/day12/`.

---

## Full map

See **`docs/FOLDER_MAP.md`**.

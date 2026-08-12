# RUN THE BOT — meta-RL policy with (target%, risk%) inputs, no retrain

How to set up, train, prove, and forward-test the meta-learning policy on any
machine (Linux/cloud or the original Windows box). The contract:

> **One trained policy. Two inputs each day — `target_percent` and
> `max_daily_risk_percent`. Changing the inputs never retrains the weights.**

---

## 1) Setup

```bash
pip install -r requirements.txt        # numpy, pandas, pytest
python -m pytest evidence_court/tests -q   # sanity (doc-pin failures aside, meta_rl tests must pass)
```

### Price data (M1 bars)

`evidence_court/meta_rl/price_io.py` resolves the data directory in this order:

1. `CREATOR_DATA_DIR` environment variable
2. The original Windows path (if it exists on that machine)
3. Repo-relative `data/raw/`

Expected files (MT5-style tab-separated: `DATE  TIME  OPEN  HIGH  LOW  CLOSE  VOL`,
date `YYYY.MM.DD`):

| Symbol | File |
|--------|------|
| XAUUSD | `XAUUSD_M1_full.csv` |
| EURUSD | `EURUSD_M1_curriculum.csv` |
| GBPUSD | `GBPUSD_M1_curriculum.csv` |

To download real M1 candles (Dukascopy, free, UTC) into the repo layout:

```bash
python tools/download_dukascopy_m1.py --symbol XAUUSD \
    --start 2025-11-01 --end 2026-08-10 --out data/raw/XAUUSD_M1_full.csv
```

The server rate-limits aggressively; the script defaults to 2 workers + delay.
Keep it slow — a ban costs more time than the throttle.

Timestamps default to **EET (MT5 broker time)** — `--tz eet` — matching the
original MT5 CSV convention. This folds the thin Sunday-evening UTC session
into Monday, so the eval never sees fake near-empty "Sunday days", and session
slots (07:00–20:00) line up with how the edge/session code was calibrated.

---

## 2) Train once (offline) — Law A14/A29

Training uses a **synthetic regime curriculum** (goal × risk bands, learn-to-learn
channel permutations, London/NY opportunity drills) — it does **not** need price
data. The policy learns to read the packed 176-dim state, of which the goal/risk
context (last 8 dims) encodes the two daily inputs.

```bash
# Serious train (production-class): ~8000 steps
python -m evidence_court.meta_rl.cli meta-train --steps 8000 \
    --out evidence_court/artifacts/policies_lab/my_candidate.npz
```

**Never write directly to `evidence_court/artifacts/meta_policy_champion.npz`** —
that is the production king; replacing it requires a measured dual + Court
(`evidence_court/BEST_POLICY.md`).

After training the policy is **frozen** (`freeze_for_inference`). Any
`train_step`/`meta_update` after freezing raises `NO_RETRAIN_VIOLATION`.

---

## 3) Prove the two-input contract (no retrain)

```bash
# One pair: decide + size for target 15% / risk 2%
python -m evidence_court.meta_rl.cli prove 15 2

# Whole grid: 35 target×risk pairs, one frozen weight set, asserts fingerprint
python tools/prove_no_retrain_grid.py
```

`prove` output must show `"no_retrain": true` and `"train_steps": 0`. The grid
script must print `"no_retrain_contract": "HOLDS"`. The two inputs only change
the **state context** (`goal_risk` dims: target_norm, risk_norm, pressure,
hardness, allow_fire, risk_remaining…); the weights are byte-identical for
every pair.

---

## 4) Forward test (before any deploy)

The forward eval walks real M1 days chronologically with **no look-ahead**
(each decision slot sees only completed bars), draws a **random target×risk
pair per day**, runs the multi-slot goal path under the hard risk envelope,
and verifies the weight fingerprint after every day.

```bash
# Fast sensor: 40 days, XAU-only, pinned seed (writes report + scoreboard row)
python tools/run_forward_protocol.py --days 40 --seed 42 --symbols XAUUSD

# North star: 100 days (multi-symbol once EUR/GBP data present)
python tools/run_forward_protocol.py --days 100 --seed 42 --symbols XAUUSD
python tools/run_forward_protocol.py --days 100 --seed 42 --symbols XAUUSD,EURUSD,GBPUSD

# (equivalent raw CLI: python -m evidence_court.meta_rl.cli forward100 --days N --out ...)
```

Measured baseline in this environment (champion `meta4275`, real Dukascopy
M1, out-of-sample Mar–Aug 2026): 40d XAU seeds 42/43/44 → hits 1/0/1,
**breach 0**, ~23–26 trades/day; 100d XAU seed 42 → hits 1, **breach 0**,
mean day pnl +0.63%, worst day −2.66% (typed risk never exceeded);
100d multi-symbol (XAU+EUR+GBP) seed 42 → hits 1, **breach 0**, 58 trades/day,
A13 band on 70% of days. Re-running the same protocol is byte-identical
(deterministic).

Read the report before believing anything:

| Field | Must be |
|-------|---------|
| `breach_count` | **0** — no day lost more than its typed risk% |
| `no_retrain` | **true** — same fingerprint across all days/pairs |
| `pair_results` | hits/hit_rate per target×risk pair |
| `metadata.goal_consistency` | hit rates by target band |
| `promote_ready` | full final-boss gate (100d+, consistency, senses, L2L) |

**Consistency = same protocol every time.** Same seed (42), same window pin,
same symbol set — otherwise runs are not comparable and "improvement" is noise.

---

## 5) Daily driving (deploy shape)

Each trading day:

```python
from evidence_court.meta_rl.policy import load_or_train_champion
from evidence_court.meta_rl.state import build_meta_rl_state

policy = load_or_train_champion()      # loads frozen champion npz, never retrains
policy.assert_frozen()

# You type these two numbers — nothing else changes:
state = build_meta_rl_state(
    target_percent=25.0,               # today's typed target
    max_daily_risk_percent=2.0,        # today's typed risk cap
    # ... live market channels packed by the day-path runner ...
)
action = policy.forward(state)         # act: wait|long|short + size_risk_percent
```

On the full production path (`goal_path.run_goal_path_day`) the day runs
multi-slot decisions under `DailyRiskLedger` so the sum of open risk can never
exceed the typed risk% (breach 0 by construction), and A13 cadence (8–400
trades/day) is tracked.

---

## 6) Deploy gate (do not skip)

1. `pytest evidence_court/tests -q` — meta_rl tests green.
2. `python tools/prove_no_retrain_grid.py` — contract HOLDS.
3. Forward test on the pinned protocol — `breach_count 0`, `no_retrain true`,
   and hit/consistency numbers **you** accept (`BEST_POLICY.md` floor is the
   reference: hits 11/100 on the CASE-0037 champion).
4. Only after a measured dual beats the live king (hits strictly greater,
   breach 0) may the champion npz + `BEST_POLICY.md` be replaced — through
   Court, never silently.

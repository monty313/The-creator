# FTMO Sentinel EA — corpus geometry + Day Governor

**Status: EXPERIMENTAL — not Court law.** Landed by owner (Monty) order; per the
"Court before major decisions" rule this module is **quarantined as experimental**
until it goes through a full Evidence Court case (A10 + A15). Do not treat it as
production policy or as part of the lab bot's brain (A14/A29 path is separate).

## What it is

A single-file MQL5 Expert Advisor (`FTMO_Sentinel_EA.mq5`) built from the
**measured winners** of the `strategies/` corpus, wrapped in a **Day Governor**
whose objective ordering is:

1. never breach an FTMO limit (daily −5%, total −10%),
2. never let a green day close red,
3. bank **+2.5% per day** and stop.

## Where every piece comes from (provenance)

| Piece | Source in corpus | Measured evidence |
|---|---|---|
| CCI M-line reclaim (Engine A) | `tweaks/mt__cci_gravity_scalp_ftmo.md`, `python_batch/families.py::fam_cci_gravity` | WR 100% (44 trades), MC rank 13/139, bootstrap P(loss)=0% |
| McFlurry RSI eddy (Engine B) | `sauces/H001_mcflurry_eddy_scalp.md` | WR ~80% (212 trades), MC rank 16/139 |
| Dual-HTF force + strength | `00_intuition.md` P2.3 (accuracy layer) | 125/125 families lifted past WR 60.4% |
| Mark mass gate (BB(100,0.5,+2) mid on both HTFs) | `mark_doctrine_refs/RSI_BB_L2L_SKILL.md` | doctrine timing geometry |
| Session 07–21 / bar confirm / micro structure | `00_intuition.md` filters 1–4 | same accuracy program |
| First-breath barriers (TP 0.00028 / SL 0.00115 → TP≈0.7·ATR, SL≈2.8·ATR) | CCI upgrade exit tier | barrier geometry, no time-stop thrash |
| Reclaim-only fire (never enter the dip) | P2.4 failure diagnosis | the change that flipped CCI from losing to winning |

## The Day Governor (the creative part)

| Rail | Setting (default) | FTMO frame |
|---|---|---|
| Daily goal bank | flatten + stop at **+2.5%** | consistency objective |
| Green-day ratchet | armed at +0.8% peak; floor = max(+0.2%, 60% of peak) | a green day cannot close red |
| Soft daily stop | −1.5% → no new trades | FTMO allows −5% |
| Hard daily stop | −2.0% → flatten everything | 3% of buffer never used |
| Per-trade risk cap | one loss can never push the day past the soft stop | structural, not hopeful |
| House-money ladder | risk = 0.8% + 0.75 × (day profit %), capped 2.0% | escalation funded only by banked profit |
| Loss-streak halving + 3-consecutive-loss day stop | halve risk per loss; stop day at 3 | kills thrash days |
| Total fuse | **−6% → permanent halt** | FTMO allows −10%; account preserved |
| Challenge manager | stop at +10% balance; ticket micro-trades until ≥4 trading days registered | pass conditions handled |
| Day anchor | max(balance, equity) at reset hour | conservative vs FTMO midnight CE(S)T anchor |

All day-state (anchor, halt, bank, trade count) is shared across charts through
terminal global variables keyed by magic number, so running the Sentinel on
several symbols keeps **one** account-level governor.

## Validation (before believing anything)

`governor_sim.py` mirrors the governor trade-for-trade on the corpus's measured
trade model (win +0.243R / loss −1R barrier pair, cost 0.05R, win rates from the
measured books with a 95% Wilson lower bound on the 44/44 CCI book). Results in
[`VALIDATION.md`](VALIDATION.md). Headlines (20,000 days + 2,000 challenges per
scenario, seed 42):

- **FTMO daily/total breach probability: 0.00% in every scenario, including the
  WR-70% stress case.** Worst simulated day: −1.54%.
- At the measured edge (WR-LB 0.92, ~20 signals/day): median day **+2.51%**
  (goal banked on the median day), challenge pass ≈100%, median 8 days.
- On 3–4 symbols (~40 signals/day): P(goal day) 58%, pass 100%, median 7 days.
- If the live edge degrades to WR 0.80, the system does **not** pass — it halts
  itself at the −6% fuse without ever breaching FTMO. That is the honest failure
  mode: no blown account, ever, at trade-close granularity.

## Honest limits (read before running money)

- **"Pass every time / +2.5% every day" is not a guarantee physics allows.**
  What the design guarantees structurally: per-trade risk caps, daily flatten
  levels far inside FTMO limits, a ratchet that locks green days, and a fuse
  that ends the attempt long before a breach. The *win* side depends on the
  entry edge holding out-of-window.
- The measured WR comes from **one EURUSD window (June–July 2026)**. Corpus law:
  distrust specific pips until they survive new windows. Forward-test on demo /
  FTMO free trial first; the governor behaves identically there.
- Slippage/gap risk: the hard stop is a watchdog on floating equity; a violent
  gap can slip past any stop. The 3-point buffer (−2% flatten vs −5% limit) and
  the 0.8–2.0% risk caps are sized so even a 2× slip stays inside FTMO.
- News: FTMO Swing allows news trading; on normal accounts use
  `InpNewsBlackout` windows around red-folder events.

## Setup

1. Copy `FTMO_Sentinel_EA.mq5` to `MQL5/Experts/`, compile in MetaEditor.
2. Attach to **M5** charts (trigger TF = chart TF). Defaults: HTF1 = H1,
   HTF2 = H4 (the corpus `5m/30m/1h` and `15m/1h/4h` stacks sit between these;
   sweep in the strategy tester per symbol).
3. Recommended: 2–4 liquid symbols (e.g. EURUSD, GBPUSD, XAUUSD, US30) — same
   magic number on all charts so the governor is shared.
4. Set `InpInitialBalance` to the exact challenge starting balance, and
   `InpDayResetHour` to the server hour matching FTMO's midnight CE(S)T.
5. Strategy-test each symbol (every tick, real spreads), then demo/free-trial
   forward test. Only then a funded attempt.

## Files

| File | Role |
|---|---|
| `FTMO_Sentinel_EA.mq5` | The EA (entries + Day Governor + challenge manager) |
| `governor_sim.py` | Governor Monte Carlo, mirrors EA rules (`python3 governor_sim.py`) |
| `VALIDATION.md` | Generated measurement report |

## Court status

Experimental quarantine (this folder). Before any production/promote claim it
needs: a full A10 adversarial case (Creator/Mark openings + counters), A15
Counsel opinion, multi-window multi-symbol re-measurement, and a ledger event.

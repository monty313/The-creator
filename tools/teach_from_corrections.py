"""Teach the policy from human thought-map corrections (closed loop).

Flow: thought_map.html → edit decisions ("supposed to: act/size") → Export
teacher JSONL → THIS script → lab candidate → re-measure the pinned 40d dual.

Each correction row carries the EXACT packed 176-dim state the brain saw on
the real path (anti F-025 — no synthetic rebuild), your teacher act, and your
size fraction. Training is offline meta_update on a copy of the champion;
the champion npz is NEVER overwritten (install only via dual + Court).

Usage:
  python tools/teach_from_corrections.py thought_map_corrections.jsonl
  python tools/teach_from_corrections.py corr.jsonl --epochs 40 --size-only
  # then measure:
  python tools/run_forward_protocol.py --days 40 --seed 42 --symbols XAUUSD \
      --champion evidence_court/artifacts/policies_lab/meta_policy_human_corrections.npz
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import numpy as np

from evidence_court.meta_rl.policy import DEFAULT_CHAMPION_PATH, MetaPolicy

LAB_OUT = (
    _ROOT
    / "evidence_court"
    / "artifacts"
    / "policies_lab"
    / "meta_policy_human_corrections.npz"
)


def load_corrections(path: Path) -> list:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        st = r.get("state")
        if not st or not isinstance(st, list) or len(st) < 32:
            continue  # only rows with a real packed state are trainable
        act = str(r.get("teacher_act") or "wait")
        if act not in ("wait", "long", "short"):
            continue
        rows.append(
            {
                "state": np.asarray(st, dtype=np.float64),
                "teacher_act": act,
                "teacher_size_frac": float(r.get("teacher_size_frac") or 0.0),
                "weight": float(r.get("weight") or 1.5),
                "note": str(r.get("note") or ""),
                "key": f"{r.get('date')}|{r.get('slot')}|{r.get('symbol')}",
            }
        )
    return rows


def agreement(pol: MetaPolicy, rows: list) -> dict:
    """How often the brain now agrees with the human teacher."""
    n_act = 0
    size_err = []
    for r in rows:
        act, size_logit, _ = pol.brain.predict_act(r["state"])
        if act == r["teacher_act"]:
            n_act += 1
        if r["teacher_act"] != "wait":
            sig = 1.0 / (1.0 + np.exp(-size_logit))
            size_err.append(abs(sig - r["teacher_size_frac"]))
    return {
        "act_agreement": round(n_act / max(len(rows), 1), 3),
        "size_mae": round(float(np.mean(size_err)), 3) if size_err else None,
        "n_rows": len(rows),
    }


def main(argv: list | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("corrections", type=str, help="JSONL exported from thought map")
    ap.add_argument("--champion", type=str, default="", help="warm-start source npz")
    ap.add_argument("--out", type=str, default=str(LAB_OUT))
    ap.add_argument("--epochs", type=int, default=25)
    ap.add_argument("--lr", type=float, default=0.02)
    ap.add_argument(
        "--size-only",
        action="store_true",
        help="only teach the size head (act decisions provably unchanged)",
    )
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args(argv)

    rows = load_corrections(Path(args.corrections))
    if not rows:
        print("no trainable corrections (need rows with packed state)", file=sys.stderr)
        return 1

    src = Path(args.champion) if args.champion else DEFAULT_CHAMPION_PATH
    out = Path(args.out)
    if out.resolve() == DEFAULT_CHAMPION_PATH.resolve():
        raise SystemExit("FORBIDDEN: corrections may not overwrite the champion npz")

    pol = MetaPolicy.load(src, freeze=False)
    before = agreement(pol, rows)
    fp_before = pol.weight_fingerprint()

    rng = np.random.default_rng(args.seed)
    order = np.arange(len(rows))
    for _ in range(int(args.epochs)):
        rng.shuffle(order)
        for i in order:
            r = rows[int(i)]
            pol.brain.meta_update(
                r["state"],
                teacher_act=r["teacher_act"],
                lr=args.lr,
                reward=r["weight"],
                teacher_size_frac=(
                    r["teacher_size_frac"] if r["teacher_act"] != "wait" else 0.0
                ),
                size_only=bool(args.size_only),
            )

    pol.trained = True
    if getattr(pol, "size_head_drives", False):
        pol.size_head_drives = True
    pol.freeze_for_inference()
    pol.save(out)
    after = agreement(pol, rows)

    print(
        json.dumps(
            {
                "corrections_file": args.corrections,
                "trainable_rows": len(rows),
                "mode": "size_only" if args.size_only else "act+size",
                "epochs": int(args.epochs),
                "warm_start": str(src),
                "fingerprint_before": fp_before,
                "fingerprint_after": pol.weight_fingerprint(),
                "agreement_before": before,
                "agreement_after": after,
                "saved": str(out),
                "champion_untouched": True,
                "next": (
                    "python tools/run_forward_protocol.py --days 40 --seed 42 "
                    f"--symbols XAUUSD --champion {out}"
                ),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Prove the two-input contract: one frozen policy, any (target%, risk%), zero retrain.

Loads the production champion ONCE, then runs inference across a grid of
target × risk pairs. Asserts after every pair that:
  - weight fingerprint is byte-identical to the pre-grid fingerprint
  - inference_updates == 0 (no weight update ever happened at inference)

Exit 0 = contract holds. Any weight drift raises immediately.

Usage:
  python tools/prove_no_retrain_grid.py
  python tools/prove_no_retrain_grid.py --champion evidence_court/artifacts/policies_lab/foo.npz
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from evidence_court.meta_rl.policy import MetaPolicy, load_or_train_champion
from evidence_court.meta_rl.state import build_meta_rl_state

TARGETS = (5.0, 10.0, 15.0, 30.0, 50.0, 70.0, 90.0)
RISKS = (1.0, 1.5, 2.0, 2.5, 3.0)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--champion", type=str, default="", help="optional .npz path")
    args = ap.parse_args(argv)

    if args.champion:
        policy = MetaPolicy.load(Path(args.champion), freeze=True)
    else:
        policy = load_or_train_champion()
    policy.assert_frozen()
    fp0 = policy.weight_fingerprint()

    rows = []
    for t in TARGETS:
        for r in RISKS:
            state = build_meta_rl_state(
                target_percent=t,
                max_daily_risk_percent=r,
                progress_to_target=0.1,
                realized_risk_percent=0.0,
            )
            action = policy.forward(state)
            policy.assert_frozen()
            fp = policy.weight_fingerprint()
            if fp != fp0 or policy.inference_updates != 0:
                raise RuntimeError(
                    f"NO_RETRAIN_VIOLATION at target={t} risk={r}: fp {fp0} -> {fp}, "
                    f"inference_updates={policy.inference_updates}"
                )
            rows.append(
                {
                    "target_percent": t,
                    "max_daily_risk_percent": r,
                    "act": action.act,
                    "size_risk_percent": round(action.size_risk_percent, 4),
                }
            )

    print(
        json.dumps(
            {
                "fingerprint": fp0,
                "meta_train_steps": policy.meta_train_steps,
                "pairs_tested": len(rows),
                "inference_updates": policy.inference_updates,
                "no_retrain_contract": "HOLDS",
                "actions": rows,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

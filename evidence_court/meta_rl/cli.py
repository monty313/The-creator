"""CLI entry: prove-style launch for Meta-RL Court package."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow `python -m evidence_court.meta_rl.cli` or direct path execution
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from evidence_court.meta_rl.forward_eval import run_forward_eval, save_report
from evidence_court.meta_rl.goal_risk import decode_goal_risk_norms, encode_goal_risk_context
from evidence_court.meta_rl.policy import (
    load_or_train_champion,
    train_goal_conditioned_meta_policy,
)
from evidence_court.meta_rl.state import META_RL_DIM, build_meta_rl_state, extract_goal_risk_context


def prove_pair(target: float, risk: float, seed: int = 42) -> dict:
    """Inference-only prove on a **trained** meta-policy (no retrain for this pair)."""
    policy = load_or_train_champion(seed=seed)
    fp = policy.weight_fingerprint()
    state = build_meta_rl_state(
        target_percent=target,
        max_daily_risk_percent=risk,
        progress_to_target=0.1,
        realized_risk_percent=0.0,
    )
    ctx = extract_goal_risk_context(state)
    action = policy.forward(state)
    policy.assert_frozen()
    return {
        "target_percent": target,
        "max_daily_risk_percent": risk,
        "meta_rl_dim": META_RL_DIM,
        "goal_risk_context": ctx.tolist(),
        "decoded_approx": decode_goal_risk_norms(ctx),
        "action": {
            "act": action.act,
            "size_risk_percent": action.size_risk_percent,
            "reason": action.reason,
            "wait_subtype": action.wait_subtype,
        },
        "weight_fingerprint": fp,
        "meta_train_steps": policy.meta_train_steps,
        "trained": policy.trained,
        "train_steps": policy.train_steps,  # inference updates (must be 0)
        "no_retrain": policy.weight_fingerprint() == fp and policy.inference_updates == 0,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Evidence Court Meta-RL entry")
    sub = p.add_subparsers(dest="cmd", required=True)

    pr = sub.add_parser("prove", help="Inference-only prove for one target/risk pair")
    pr.add_argument("target", type=float)
    pr.add_argument("risk", type=float)
    pr.add_argument("--seed", type=int, default=42)

    tr = sub.add_parser(
        "meta-train",
        help="Permanent meta curriculum: train goal-conditioned policy across targets",
    )
    tr.add_argument("--seed", type=int, default=42)
    tr.add_argument("--steps", type=int, default=8000)
    tr.add_argument(
        "--out",
        type=str,
        default="evidence_court/artifacts/meta_policy_champion.npz",
    )

    fe = sub.add_parser("forward100", help="Run N-day forward matrix eval")
    fe.add_argument("--days", type=int, default=100)
    fe.add_argument("--out", type=str, default="evidence_court/artifacts/forward100_report.json")
    fe.add_argument("--price", type=str, default="")
    fe.add_argument("--seed", type=int, default=42)

    args = p.parse_args(argv)
    if args.cmd == "prove":
        out = prove_pair(args.target, args.risk, seed=args.seed)
        print(json.dumps(out, indent=2))
        return 0
    if args.cmd == "meta-train":
        pol = train_goal_conditioned_meta_policy(
            seed=args.seed, n_steps=args.steps, freeze=True
        )
        path = pol.save(Path(args.out))
        print(
            json.dumps(
                {
                    "saved": str(path),
                    "meta_train_steps": pol.meta_train_steps,
                    "trained": pol.trained,
                    "frozen_for_inference": pol.frozen_for_inference,
                    "fingerprint": pol.weight_fingerprint(),
                    "law": "A14_permanent_meta_policy",
                },
                indent=2,
            )
        )
        return 0
    if args.cmd == "forward100":
        price = Path(args.price) if args.price else None
        report = run_forward_eval(n_days=args.days, price_path=price, seed=args.seed)
        out_path = Path(args.out)
        save_report(report, out_path)
        summary = {
            "n_days": report.n_days,
            "breach_count": report.breach_count,
            "no_retrain": report.no_retrain,
            "l2l_day_path_ok": report.l2l_day_path_ok,
            "l2l_novel_ok": report.l2l_novel_ok,
            "senses_day_path_ok": report.senses_day_path_ok,
            "goal_consistency_ok": report.goal_consistency_ok,
            "promote_ready": report.promote_ready,
            "pairs": list(report.pair_results.keys()),
            "out": str(out_path),
            "metadata": report.metadata,
        }
        print(json.dumps(summary, indent=2))
        ok = (
            report.breach_count == 0
            and report.no_retrain
            and (report.n_days < 100 or report.promote_ready)
        )
        return 0 if ok else 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

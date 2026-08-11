"""Finish dual + promote-if-beats using existing year pack/shadow."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# Ensure XAU-only dual for throughput
os.environ["HTF_DUAL_XAU_ONLY"] = "1"

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.policy import DEFAULT_CHAMPION_PATH, MetaPolicy
from evidence_court.meta_rl.train_htf_active_year import (
    FLOOR,
    PACK,
    REPORT,
    SHADOW,
    beats_floor,
    promote_champion,
    run_dual,
)


def main() -> int:
    pre_fp = MetaPolicy.load(DEFAULT_CHAMPION_PATH, freeze=True).weight_fingerprint()
    print("pre_champ", pre_fp, flush=True)
    print("dual 100d shadow XAU-only 15m…", flush=True)
    dual_s = run_dual(policy_path=SHADOW, n_days=100, seed=42)
    print(json.dumps(dual_s, indent=2), flush=True)
    dec = beats_floor(dual_s, FLOOR)
    print("decision", dec, flush=True)
    pack = json.loads(PACK.read_text(encoding="utf-8"))
    report = {
        "law": "htf_active_year_path_state",
        "process": "00_PATH_STATE_TEACHERS + HTF active only",
        "harvest": {
            "path": str(PACK),
            "n_days": pack.get("n_days"),
            "n_examples": pack.get("n_examples"),
            "n_london_ny": pack.get("n_london_ny"),
            "n_raw": pack.get("n_raw"),
            "dims_ok": pack.get("dims_ok"),
            "require_htf_active": pack.get("require_htf_active", True),
            "window_start": pack.get("window_start"),
            "window_end": pack.get("window_end"),
            "symbols": pack.get("symbols"),
        },
        "train": {
            "shadow": str(SHADOW),
            "fp_before": pre_fp,
            "fp_after": dual_s.get("policy_fp"),
            "meta_train_steps": dual_s.get("meta_train_steps"),
            "weights_changed": pre_fp != dual_s.get("policy_fp"),
        },
        "dual_shadow": dual_s,
        "dual_champion": {"source": "BEST_POLICY_FLOOR", **FLOOR},
        "floor": FLOOR,
        "promote_decision": dec,
        "pre_champion_fp": pre_fp,
    }
    if dec.get("beats"):
        print("PROMOTING", flush=True)
        report["promote_result"] = promote_champion(SHADOW, report)
        report["promoted"] = True
    else:
        print("NO PROMOTE", flush=True)
        report["promoted"] = False
        report["promote_result"] = {"promoted": False, "reason": dec.get("fail")}
    post_fp = MetaPolicy.load(DEFAULT_CHAMPION_PATH, freeze=True).weight_fingerprint()
    report["post_champion_fp"] = post_fp
    REPORT.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("report", REPORT, "promoted", report["promoted"], "post", post_fp, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

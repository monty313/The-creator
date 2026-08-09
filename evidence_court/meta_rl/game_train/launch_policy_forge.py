"""Launch Policy Forge (browser) for A34 game-train.

Serves the game_train directory (stable on Windows paths with spaces).
Warm-starts from latest artifacts/game_train/policy_forge_export_*.json
via a local resume_brain.json copy next to the HTML.

Usage (from repo root):
  python evidence_court/meta_rl/game_train/launch_policy_forge.py
"""
from __future__ import annotations

import json
import socket
import sys
import threading
import time
import webbrowser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]  # The Creator
GAME = HERE / "policy_forge.html"
ART = REPO / "evidence_court" / "artifacts" / "game_train"
RESUME_ART = ART / "resume_brain.json"
RESUME_LOCAL = HERE / "resume_brain.json"
PORT_DEFAULT = 8765


def _ensure_resume_brain() -> Path | None:
    ART.mkdir(parents=True, exist_ok=True)
    packs = sorted(ART.glob("policy_forge_export_*.json"))
    if not packs:
        if RESUME_LOCAL.exists():
            RESUME_LOCAL.unlink()
        return None
    latest = packs[-1]
    data = json.loads(latest.read_text(encoding="utf-8"))
    resume = {
        "format": "policy_forge_resume_v1",
        "from_pack": latest.name,
        "scoreboard": data.get("scoreboard"),
        "brain": data.get("brain"),
        "meta_rl_dim": data.get("meta_rl_dim", 176),
        "trajectories": [],
    }
    blob = json.dumps(resume)
    RESUME_ART.write_text(blob, encoding="utf-8")
    RESUME_LOCAL.write_text(blob, encoding="utf-8")
    return latest


def _free_port(start: int = PORT_DEFAULT) -> int:
    for port in range(start, start + 40):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    return start


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        sys.stdout.write("%s - %s\n" % (self.address_string(), fmt % args))
        sys.stdout.flush()


def main() -> int:
    if not GAME.exists():
        print(f"missing game: {GAME}", file=sys.stderr)
        return 1
    latest = _ensure_resume_brain()
    port = _free_port()
    handler = partial(QuietHandler, directory=str(HERE))
    httpd = ThreadingHTTPServer(("127.0.0.1", port), handler)
    url = f"http://127.0.0.1:{port}/policy_forge.html"
    print("Policy Forge (A34)", flush=True)
    print(f"  game:   {GAME}", flush=True)
    print(f"  serve:  {HERE}", flush=True)
    print(f"  url:    {url}", flush=True)
    if latest:
        steps = None
        try:
            steps = json.loads(latest.read_text(encoding="utf-8")).get("brain", {}).get(
                "meta_train_steps"
            )
        except Exception:
            pass
        print(f"  resume: {latest.name}  meta_train_steps={steps}", flush=True)
    else:
        print("  resume: none (fresh prior)", flush=True)
    print("  export → save pack under evidence_court/artifacts/game_train/", flush=True)
    print("  ingest: python -m evidence_court.meta_rl.cli game-ingest <pack.json> --out evidence_court/artifacts/game_train/meta_policy_forge_v1.npz --lr 0.02", flush=True)
    print("  Ctrl+C to stop server", flush=True)

    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    time.sleep(0.4)
    # sanity probe
    try:
        import urllib.request

        with urllib.request.urlopen(url, timeout=3) as r:
            print(f"  probe:  HTTP {r.status} ok", flush=True)
    except Exception as e:
        print(f"  probe:  FAIL {e}", flush=True)
    webbrowser.open(url)
    try:
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("\nstopping…", flush=True)
        httpd.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Capture TradingView chart screenshots at 1m / 15m / 30m via CDP."""
from __future__ import annotations

import asyncio
import base64
import json
import urllib.request
from pathlib import Path

OUT_DIR = Path("evidence_court/artifacts")
TFS = ("1", "15", "30")


async def cdp_session(ws_url: str):
    import websockets

    ws = await websockets.connect(ws_url, max_size=50_000_000)
    mid = 0

    async def send(method, params=None, timeout=60):
        nonlocal mid
        mid += 1
        msg = {"id": mid, "method": method}
        if params:
            msg["params"] = params
        await ws.send(json.dumps(msg))
        while True:
            raw = await asyncio.wait_for(ws.recv(), timeout=timeout)
            data = json.loads(raw)
            if data.get("id") == mid:
                return data

    return ws, send


async def main() -> None:
    pages = json.loads(
        urllib.request.urlopen("http://127.0.0.1:9222/json/list", timeout=5).read()
    )
    charts = [p for p in pages if "tradingview.com/chart" in p.get("url", "")]
    if not charts:
        print("NO_CHART")
        return
    print("page", charts[0]["url"])
    ws, send = await cdp_session(charts[0]["webSocketDebuggerUrl"])
    try:
        await send("Page.enable")
        await send("Runtime.enable")

        # Ensure gold + try jump near day12 context
        prep = """
(async () => {
  const chart = TradingViewApi.activeChart();
  const log = [];
  function wait(ms){return new Promise(r=>setTimeout(r,ms));}
  try {
    await new Promise((res) => {
      try { chart.setSymbol('OANDA:XAUUSD', () => res()); setTimeout(res, 2000); }
      catch(e) { try { chart.setSymbol('XAUUSD', () => res()); } catch(_){}; setTimeout(res, 2000); }
    });
    log.push('symbol ' + (chart.symbol && chart.symbol()));
  } catch(e) { log.push('symerr '+String(e)); }
  await wait(1500);
  return {log, symbol: (chart.symbol&&chart.symbol()) || null};
})()
"""
        r = await send(
            "Runtime.evaluate",
            {"expression": prep, "returnByValue": True, "awaitPromise": True},
        )
        print("prep", json.dumps(r.get("result", {}).get("result", {}).get("value"), default=str))

        results = []
        for tf in TFS:
            expr = f"""
(async () => {{
  const chart = TradingViewApi.activeChart();
  function wait(ms){{return new Promise(r=>setTimeout(r,ms));}}
  await new Promise((res) => {{
    try {{ chart.setResolution('{tf}', () => res()); setTimeout(res, 2000); }}
    catch(e) {{ try {{ chart.setResolution('{tf}'); }} catch(_){{}}; setTimeout(res, 2000); }}
  }});
  await wait(2500);
  let symbol = null, resv = null;
  try {{ symbol = chart.symbol(); }} catch(e) {{}}
  try {{ resv = chart.resolution(); }} catch(e) {{}}
  return {{ symbol, resolution: resv, tf: '{tf}' }};
}})()
"""
            info = await send(
                "Runtime.evaluate",
                {"expression": expr, "returnByValue": True, "awaitPromise": True},
            )
            val = info.get("result", {}).get("result", {}).get("value")
            print("tf", tf, val)
            await asyncio.sleep(0.5)
            shot = await send(
                "Page.captureScreenshot",
                {"format": "png", "fromSurface": True},
            )
            b64 = shot.get("result", {}).get("data")
            if not b64:
                print("NO_SHOT", tf, str(shot)[:300])
                continue
            path = OUT_DIR / f"tv_xau_tf_{tf}m.png"
            path.write_bytes(base64.b64decode(b64))
            results.append({"tf": tf, "path": str(path), "bytes": path.stat().st_size, "info": val})
            print("SAVED", path, path.stat().st_size)

        (OUT_DIR / "tv_tf_capture_meta.json").write_text(
            json.dumps(results, indent=2), encoding="utf-8"
        )
        print("DONE", len(results))
    finally:
        await ws.close()


if __name__ == "__main__":
    asyncio.run(main())

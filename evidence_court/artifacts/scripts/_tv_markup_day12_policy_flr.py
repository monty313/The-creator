"""Policy markup: Day 12 XAUUSD through Mark physics + Aaron FLR understanding."""
from __future__ import annotations

import asyncio
import base64
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# Measured bot day (UTC slot times + prices from Court re-sim)
# Narrative zones for Policy understanding (Mark PINN + Aaron FLR)
ZONES = [
    {
        "name": "FORCE_ON",
        "t0": "07:00:00",
        "t1": "08:15:00",
        "p0": 4864.0,
        "p1": 4875.0,
        "color": "#2962FF",
        "text": "FORCE (Mark HTF tide / Aaron Force): multi-set long permission — side = LONG only",
    },
    {
        "name": "RECLAIM_FIRE_OK",
        "t0": "08:15:00",
        "t1": "08:30:00",
        "p0": 4870.0,
        "p1": 4885.0,
        "color": "#00C853",
        "text": "RECLAIM/LAUNCH: High Tension+Low Entropy+Accel WITH Force → fire OK (best win +1.09%)",
    },
    {
        "name": "THRASH_BAD",
        "t0": "08:30:00",
        "t1": "08:45:00",
        "p0": 4858.0,
        "p1": 4885.0,
        "color": "#FF1744",
        "text": "ANTI-THRASH FAIL: re-fire after launch without new Load→Reclaim → big loss -1.93% (entropy / no launch eq)",
    },
    {
        "name": "LOAD_PULLBACK",
        "t0": "08:45:00",
        "t1": "09:15:00",
        "p0": 4835.0,
        "p1": 4865.0,
        "color": "#FFD600",
        "text": "LOAD (kinematics stretch vs Force): pullback against tide — Aaron WAIT (Load≠fire) / Mark slingshot tension",
    },
    {
        "name": "RECLAIM2",
        "t0": "09:15:00",
        "t1": "10:30:00",
        "p0": 4835.0,
        "p1": 4870.0,
        "color": "#00E676",
        "text": "RECLAIM2: LTF pullback_resume WITH Force still long — smaller size progressive path (partial convert)",
    },
    {
        "name": "NOISE_HOLD",
        "t0": "11:45:00",
        "t1": "16:00:00",
        "p0": 4840.0,
        "p1": 4875.0,
        "color": "#9E9E9E",
        "text": "HIGH ENTROPY / thin risk skin: Mark entropy mask → HOLD; Policy size-down near breach (micro thrash = dead R)",
    },
]

TRADES = [
    {"slot": "07:00:00", "exit": "07:15:00", "entry_px": 4865.96, "exit_px": 4866.90, "pnl": 0.096, "win": True, "tag": "cont early"},
    {"slot": "07:15:00", "exit": "07:30:00", "entry_px": 4866.90, "exit_px": 4868.76, "pnl": 0.169, "win": True, "tag": "cont"},
    {"slot": "07:30:00", "exit": "07:45:00", "entry_px": 4868.76, "exit_px": 4871.05, "pnl": 0.208, "win": True, "tag": "cont"},
    {"slot": "07:45:00", "exit": "08:00:00", "entry_px": 4871.05, "exit_px": 4869.91, "pnl": -0.104, "win": False, "tag": "noise"},
    {"slot": "08:00:00", "exit": "08:15:00", "entry_px": 4869.91, "exit_px": 4871.58, "pnl": 0.147, "win": True, "tag": "setup"},
    {"slot": "08:15:00", "exit": "08:30:00", "entry_px": 4871.58, "exit_px": 4883.92, "pnl": 1.086, "win": True, "tag": "LAUNCH"},
    {"slot": "08:30:00", "exit": "08:45:00", "entry_px": 4883.92, "exit_px": 4861.63, "pnl": -1.934, "win": False, "tag": "THRASH"},
    {"slot": "09:15:00", "exit": "09:30:00", "entry_px": 4837.19, "exit_px": 4849.23, "pnl": 0.348, "win": True, "tag": "pb reclaim"},
    {"slot": "09:45:00", "exit": "10:00:00", "entry_px": 4849.20, "exit_px": 4855.24, "pnl": 0.175, "win": True, "tag": "pb"},
    {"slot": "10:00:00", "exit": "10:15:00", "entry_px": 4855.24, "exit_px": 4858.57, "pnl": 0.095, "win": True, "tag": "pb"},
    {"slot": "10:15:00", "exit": "10:30:00", "entry_px": 4858.57, "exit_px": 4866.78, "pnl": 0.238, "win": True, "tag": "pb"},
    {"slot": "10:30:00", "exit": "10:45:00", "entry_px": 4866.78, "exit_px": 4861.14, "pnl": -0.154, "win": False, "tag": "fade"},
]


def unix(t: str) -> int:
    hh, mm, ss = t.split(":")
    return int(datetime(2026, 1, 21, int(hh), int(mm), int(ss), tzinfo=timezone.utc).timestamp())


async def main() -> None:
    pages = json.loads(
        urllib.request.urlopen("http://127.0.0.1:9222/json/list", timeout=5).read()
    )
    charts = [p for p in pages if "tradingview.com/chart" in p.get("url", "")]
    if not charts:
        print("NO_CHART")
        return
    print("Using", charts[0]["url"])
    import websockets

    ws_url = charts[0]["webSocketDebuggerUrl"]
    trades_js = json.dumps(
        [
            {
                **t,
                "entry_t": unix(t["slot"]),
                "exit_t": unix(t["exit"]),
            }
            for t in TRADES
        ]
    )
    zones_js = json.dumps(
        [
            {
                **z,
                "t0u": unix(z["t0"]),
                "t1u": unix(z["t1"]),
            }
            for z in ZONES
        ]
    )
    title_t = unix("06:50:00")
    from_t = unix("06:45:00")
    to_t = unix("12:00:00")

    expr = f"""
(async () => {{
  const chart = TradingViewApi.activeChart();
  const wait = (ms) => new Promise(r => setTimeout(r, ms));
  const log = [];
  const trades = {trades_js};
  const zones = {zones_js};

  // Symbol + 15m (scalper working frame; Force on HTF is narrative)
  await new Promise((res) => {{
    try {{ chart.setSymbol('OANDA:XAUUSD', () => res()); setTimeout(res, 2500); }}
    catch (e) {{ try {{ chart.setSymbol('XAUUSD', () => res()); }} catch(_){{}}; setTimeout(res, 2500); }}
  }});
  await wait(1200);
  await new Promise((res) => {{
    try {{ chart.setResolution('15', () => res()); setTimeout(res, 2000); }}
    catch (e) {{ try {{ chart.setResolution('15'); }} catch(_){{}}; setTimeout(res, 2000); }}
  }});
  await wait(2800);
  log.push('sym=' + (chart.symbol && chart.symbol()) + ' res=' + (chart.resolution && chart.resolution()));

  try {{ chart.removeAllShapes(); log.push('cleared'); }} catch (e) {{ log.push('clear ' + e); }}

  // Title banner
  try {{
    chart.createShape({{ time: {title_t}, price: 4898 }}, {{
      shape: 'text',
      text: 'POLICY DAY12 READ | XAU 2026-01-21 | Mark PINN Force + Aaron FLR | Green=Launch | Red=Thrash | Yellow=Load wait | Gray=Entropy HOLD',
      overrides: {{ color: '#FFFFFF', fontsize: 13 }},
    }});
  }} catch (e) {{ log.push('title ' + e); }}

  // Legend
  try {{
    chart.createShape({{ time: {title_t}, price: 4890 }}, {{
      shape: 'text',
      text: 'Force=HTF tide side | Load=tension vs Force WAIT | Reclaim=Launch WITH Force FIRE | Hold=thesis across short scalps NOT 30m bag',
      overrides: {{ color: '#90CAF9', fontsize: 11 }},
    }});
  }} catch (e) {{}}

  // Zone rectangles / labels
  let zok = 0;
  for (const z of zones) {{
    try {{
      const pts = [
        {{ time: z.t0u, price: z.p0 }},
        {{ time: z.t1u, price: z.p1 }},
      ];
      chart.createMultipointShape(pts, {{
        shape: 'rectangle',
        lock: false,
        overrides: {{
          backgroundColor: z.color,
          color: z.color,
          linewidth: 1,
          transparency: 85,
          fillBackground: true,
          extendLeft: false,
          extendRight: false,
        }},
        text: z.name,
      }});
      zok += 1;
    }} catch (e) {{
      log.push('zone ' + z.name + ' ' + String(e).slice(0, 80));
    }}
    try {{
      chart.createShape({{ time: z.t0u, price: z.p1 }}, {{
        shape: 'text',
        text: z.text,
        overrides: {{ color: z.color, fontsize: 10 }},
      }});
    }} catch (e) {{}}
  }}
  log.push('zones ' + zok);

  // Verticals key moments
  const verts = [
    {{ t: {unix('08:15:00')}, txt: 't3 RECLAIM FIRE', c: '#00C853' }},
    {{ t: {unix('08:30:00')}, txt: 't4 FAIL thrash re-fire', c: '#FF1744' }},
    {{ t: {unix('09:15:00')}, txt: 'Load resolved → pb reclaim', c: '#FFD600' }},
  ];
  for (const v of verts) {{
    try {{
      chart.createMultipointShape([
        {{ time: v.t, price: 4830 }},
        {{ time: v.t, price: 4895 }},
      ], {{
        shape: 'vertical_line',
        overrides: {{ linecolor: v.c, linewidth: 2, linestyle: 0 }},
        text: v.txt,
      }});
    }} catch (e) {{
      try {{
        chart.createShape({{ time: v.t, price: 4880 }}, {{
          shape: 'vertical_line', text: v.txt, overrides: {{ linecolor: v.c }},
        }});
      }} catch (_) {{}}
    }}
  }}

  // Trade entry-exit legs
  let drawn = 0;
  for (const t of trades) {{
    const color = t.win ? '#00C853' : '#FF1744';
    const lw = (t.tag === 'LAUNCH' || t.tag === 'THRASH') ? 4 : 2;
    const label = (t.win ? 'WIN ' : 'LOSS ') + t.pnl.toFixed(2) + '% | ' + t.tag + ' | ' + t.slot.slice(0,5) + '→' + t.exit.slice(0,5);
    try {{
      chart.createMultipointShape([
        {{ time: t.entry_t, price: t.entry_px }},
        {{ time: t.exit_t, price: t.exit_px }},
      ], {{
        shape: 'trend_line',
        overrides: {{
          linecolor: color,
          linewidth: lw,
          linestyle: 0,
          showLabel: true,
          textcolor: color,
          fontsize: 10,
        }},
        text: label,
      }});
      drawn += 1;
    }} catch (e) {{
      log.push('trade ' + t.slot + ' ' + String(e).slice(0, 60));
    }}
    try {{
      chart.createShape({{ time: t.entry_t, price: t.entry_px }}, {{
        shape: 'arrow_up',
        text: 'IN',
        overrides: {{ color: color }},
      }});
    }} catch (_) {{}}
    try {{
      chart.createShape({{ time: t.exit_t, price: t.exit_px }}, {{
        shape: 'arrow_down',
        text: 'OUT',
        overrides: {{ color: color }},
      }});
    }} catch (_) {{}}
  }}

  // Method summary note bottom
  try {{
    chart.createShape({{ time: {unix('10:00:00')}, price: 4828 }}, {{
      shape: 'text',
      text: 'POLICY OATH: Force first (PINN tide) | Load wait (kinematics) | Reclaim fire only Launch eq | Entropy HOLD thrash | Progressive size under rails | Day miss = thrash after 08:15 launch + weak convert after Load',
      overrides: {{ color: '#FFECB3', fontsize: 11 }},
    }});
  }} catch (e) {{}}

  // Try visible range (may fail)
  try {{
    await chart.setVisibleRange({{ from: {from_t}, to: {to_t} }});
    log.push('vr ok');
  }} catch (e) {{
    log.push('vr ' + String(e).slice(0, 40));
  }}

  let n = 0;
  try {{ n = (chart.getAllShapes() || []).length; }} catch (e) {{}}
  return {{
    log,
    drawn,
    zones: zok,
    nShapes: n,
    symbol: (chart.symbol && chart.symbol()) || null,
    res: (chart.resolution && chart.resolution()) || null,
  }};
}})()
"""

    async with websockets.connect(ws_url, max_size=50_000_000) as ws:
        mid = 0

        async def send(method, params=None, timeout=90):
            nonlocal mid
            mid += 1
            msg = {"id": mid, "method": method}
            if params:
                msg["params"] = params
            await ws.send(json.dumps(msg))
            while True:
                data = json.loads(await asyncio.wait_for(ws.recv(), timeout=timeout))
                if data.get("id") == mid:
                    return data

        await send("Runtime.enable")
        await send("Page.enable")
        r = await send(
            "Runtime.evaluate",
            {"expression": expr, "returnByValue": True, "awaitPromise": True},
        )
        print("MARKUP", json.dumps(r.get("result", {}).get("result", {}).get("value"), indent=2))
        await asyncio.sleep(1.5)
        shot = await send("Page.captureScreenshot", {"format": "png", "fromSurface": True})
        b64 = shot.get("result", {}).get("data")
        if b64:
            out = Path("evidence_court/artifacts/day12/tv_day12_policy_flr_markup.png")
            out.write_bytes(base64.b64decode(b64))
            print("SHOT", out, out.stat().st_size)
        else:
            print("NO_SHOT")


if __name__ == "__main__":
    asyncio.run(main())

"""Drive TradingView Desktop via local CDP and markup day-12 XAUUSD trades."""
from __future__ import annotations

import asyncio
import json
import urllib.request
from datetime import datetime, timezone

TRADES = [
    {"slot": "07:00:00", "exit": "07:15:00", "entry_px": 4865.96, "exit_px": 4866.90, "pnl": 0.096, "win": True},
    {"slot": "07:15:00", "exit": "07:30:00", "entry_px": 4866.90, "exit_px": 4868.76, "pnl": 0.169, "win": True},
    {"slot": "07:30:00", "exit": "07:45:00", "entry_px": 4868.76, "exit_px": 4871.05, "pnl": 0.208, "win": True},
    {"slot": "07:45:00", "exit": "08:00:00", "entry_px": 4871.05, "exit_px": 4869.91, "pnl": -0.104, "win": False},
    {"slot": "08:00:00", "exit": "08:15:00", "entry_px": 4869.91, "exit_px": 4871.58, "pnl": 0.147, "win": True},
    {"slot": "08:15:00", "exit": "08:30:00", "entry_px": 4871.58, "exit_px": 4883.92, "pnl": 1.086, "win": True},
    {"slot": "08:30:00", "exit": "08:45:00", "entry_px": 4883.92, "exit_px": 4861.63, "pnl": -1.934, "win": False},
    {"slot": "09:15:00", "exit": "09:30:00", "entry_px": 4837.19, "exit_px": 4849.23, "pnl": 0.348, "win": True},
    {"slot": "09:45:00", "exit": "10:00:00", "entry_px": 4849.20, "exit_px": 4855.24, "pnl": 0.175, "win": True},
    {"slot": "10:00:00", "exit": "10:15:00", "entry_px": 4855.24, "exit_px": 4858.57, "pnl": 0.095, "win": True},
    {"slot": "10:15:00", "exit": "10:30:00", "entry_px": 4858.57, "exit_px": 4866.78, "pnl": 0.238, "win": True},
    {"slot": "10:30:00", "exit": "10:45:00", "entry_px": 4866.78, "exit_px": 4861.14, "pnl": -0.154, "win": False},
    {"slot": "10:45:00", "exit": "11:00:00", "entry_px": 4861.14, "exit_px": 4855.24, "pnl": -0.142, "win": False},
    {"slot": "11:15:00", "exit": "11:30:00", "entry_px": 4859.88, "exit_px": 4868.46, "pnl": 0.171, "win": True},
    {"slot": "11:30:00", "exit": "11:45:00", "entry_px": 4868.46, "exit_px": 4866.99, "pnl": -0.030, "win": False},
]


def unix(t: str) -> int:
    hh, mm, ss = t.split(":")
    return int(datetime(2026, 1, 21, int(hh), int(mm), int(ss), tzinfo=timezone.utc).timestamp())


async def cdp_eval(ws_url: str, expr: str, timeout: float = 90):
    import websockets

    async with websockets.connect(ws_url, max_size=50_000_000) as ws:
        mid = 0

        async def send(method, params=None):
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

        await send("Runtime.enable")
        return await send(
            "Runtime.evaluate",
            {"expression": expr, "returnByValue": True, "awaitPromise": True},
        )


async def main() -> None:
    try:
        pages = json.loads(
            urllib.request.urlopen("http://127.0.0.1:9222/json/list", timeout=5).read()
        )
    except Exception as e:
        print("CDP_DOWN", e)
        return

    charts = [p for p in pages if "tradingview.com/chart" in p.get("url", "")]
    if not charts:
        print("NO_CHART_PAGE")
        return
    ws = charts[0]["webSocketDebuggerUrl"]
    print("Using", charts[0]["url"])

    trades_js = json.dumps(
        [
            {
                "entry_t": unix(t["slot"]),
                "exit_t": unix(t["exit"]),
                "entry_px": t["entry_px"],
                "exit_px": t["exit_px"],
                "pnl": t["pnl"],
                "win": t["win"],
                "slot": t["slot"],
                "exit": t["exit"],
            }
            for t in TRADES
        ]
    )
    from_t = unix("06:30:00")
    to_t = unix("12:00:00")
    title_t = unix("07:00:00")

    expr = f"""
(async () => {{
  const api = window.TradingViewApi;
  const chart = api.activeChart();
  const trades = {trades_js};
  const log = [];

  function wait(ms) {{ return new Promise(r => setTimeout(r, ms)); }}

  async function setSym(sym) {{
    return new Promise((resolve, reject) => {{
      try {{
        const p = chart.setSymbol(sym, () => resolve(sym));
        if (p && typeof p.then === 'function') p.then(() => resolve(sym)).catch(reject);
        setTimeout(() => resolve(sym), 2000);
      }} catch (e) {{ reject(e); }}
    }});
  }}

  try {{
    await setSym('XAUUSD');
    log.push('symbol XAUUSD');
  }} catch (e) {{
    try {{
      await setSym('OANDA:XAUUSD');
      log.push('symbol OANDA:XAUUSD');
    }} catch (e2) {{
      log.push('symbol fail ' + String(e2));
    }}
  }}

  try {{
    await new Promise((resolve) => {{
      try {{ chart.setResolution('15', () => resolve()); setTimeout(resolve, 1500); }}
      catch (e) {{ try {{ chart.setResolution('15'); }} catch(_){{}}; resolve(); }}
    }});
    log.push('resolution 15');
  }} catch (e) {{
    log.push('resolution fail ' + String(e));
  }}

  await wait(3000);

  try {{ chart.removeAllShapes(); log.push('cleared'); }} catch (e) {{ log.push('clear ' + String(e)); }}

  try {{
    await chart.setVisibleRange({{ from: {from_t}, to: {to_t} }});
    log.push('visible range');
  }} catch (e) {{
    try {{ chart.setVisibleRange({{ from: {from_t}, to: {to_t} }}); log.push('visible range sync'); }}
    catch (e2) {{ log.push('vr ' + String(e2)); }}
  }}
  await wait(1200);

  let drawn = 0;
  const errs = [];
  for (const t of trades) {{
    const color = t.win ? '#00C853' : '#FF1744';
    const points = [
      {{ time: t.entry_t, price: t.entry_px }},
      {{ time: t.exit_t, price: t.exit_px }},
    ];
    const label = (t.win ? 'WIN ' : 'LOSS ') + t.pnl.toFixed(2) + '% ' + t.slot.slice(0,5) + '->' + t.exit.slice(0,5);
    try {{
      const id = chart.createMultipointShape(points, {{
        shape: 'trend_line',
        lock: false,
        disableSelection: false,
        overrides: {{
          linecolor: color,
          linewidth: Math.abs(t.pnl) > 0.5 ? 3 : 2,
          linestyle: 0,
          showLabel: true,
          textcolor: color,
          fontsize: 11,
        }},
        text: label,
      }});
      if (id && typeof id.then === 'function') await id;
      drawn += 1;
    }} catch (e) {{
      errs.push(t.slot + ' line: ' + String(e).slice(0, 140));
    }}
    try {{
      const sid = chart.createShape(
        {{ time: t.entry_t, price: t.entry_px }},
        {{
          shape: 'arrow_up',
          text: 'IN',
          overrides: {{ color: color, fontsize: 10 }},
        }}
      );
      if (sid && typeof sid.then === 'function') await sid;
    }} catch (e) {{
      try {{
        chart.createShape(
          {{ time: t.entry_t, price: t.entry_px }},
          {{ shape: 'flag', text: 'E', overrides: {{ color: color }} }}
        );
      }} catch (_) {{}}
    }}
    try {{
      const xid = chart.createShape(
        {{ time: t.exit_t, price: t.exit_px }},
        {{
          shape: 'arrow_down',
          text: 'OUT',
          overrides: {{ color: color, fontsize: 10 }},
        }}
      );
      if (xid && typeof xid.then === 'function') await xid;
    }} catch (_) {{}}
  }}

  try {{
    chart.createShape(
      {{ time: {title_t}, price: 4895 }},
      {{
        shape: 'text',
        text: 'DAY12 BOT | XAUUSD 2026-01-21 | green=win red=loss | entry->exit',
        overrides: {{ color: '#FFD600', fontsize: 14 }},
      }}
    );
    log.push('title');
  }} catch (e) {{
    log.push('title fail ' + String(e));
  }}

  let symbol = null;
  try {{ symbol = chart.symbol(); }} catch (e) {{}}
  let nShapes = null;
  try {{ nShapes = (chart.getAllShapes() || []).length; }} catch (e) {{}}
  return {{ log, drawn, errs: errs.slice(0, 10), symbol, nShapes, nTrades: trades.length }};
}})()
"""
    r = await cdp_eval(ws, expr)
    print(json.dumps(r, indent=2)[:10000])


if __name__ == "__main__":
    asyncio.run(main())

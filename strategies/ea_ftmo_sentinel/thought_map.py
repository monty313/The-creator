"""Thought map — render how the Sentinel policy reasons through a day.

Produces a self-contained THOUGHT_MAP_<SYM>.html (no external deps) with:

  1. The reasoning flowchart with LIVE counts on every gate (where thoughts die)
  2. A rule counterfactual table: each rule disabled one at a time, measured
     impact on total P&L / worst day / breaches  ->  what to fix, with numbers
  3. Day timelines: price + Keltner bands + entries/exits + governor events +
     running day P&L, for the best, worst, banked and halted days
  4. The raw decision log per shown day (every skip and its reason)

Usage: python3 thought_map.py [EURUSD] [30min] [strength]
"""

from __future__ import annotations

import html
import sys
from collections import Counter
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from backtest_sentinel import Config, run_backtest, resample, atr, map_htf, sma  # noqa: E402
from strategy_lab import sig_keltner_fade, ema                                    # noqa: E402

SPREADS = {"EURUSD": 0.00007, "GBPUSD": 0.00010, "XAUUSD": 0.30}


def build(m1, trig, sizing, spread, **fade_over):
    kw = dict(trig=trig, kc_mult=2.0, tp_atr=1.5, sl_atr=2.0)
    kw.update(fade_over)
    built = sig_keltner_fade(m1, **kw)
    t, sl_, ss_, conc, tp_d, sl_d, strength, diag = built
    cfg = replace(Config(), name="tm", spread=spread)
    sig = (t, sl_, ss_, conc, tp_d, sl_d,
           strength if sizing == "strength" else None, diag)
    return cfg, sig, t


def run(m1, cfg, sig, dlog=None):
    return run_backtest(m1, cfg, signals=sig, dlog=dlog)


# ---------------------------------------------------------------- SVG day view
def svg_day(m1, t, day, trades, events, width=940, h_price=250, h_pl=90):
    day_m1 = m1[m1.index.date == day]
    if day_m1.empty:
        return "<p>(no data)</p>"
    px = day_m1.close.resample("5min").last().dropna()
    # bands on trigger frame for that day
    a = atr(t.high, t.low, t.close, 14)
    mid = ema(t.close, 20)
    up = (mid + 2.0 * a)[t.index.date == day]
    dn = (mid - 2.0 * a)[t.index.date == day]

    x0, x1 = 50, width - 15
    day_start = pd.Timestamp(day)
    def X(ts):
        return x0 + (x1 - x0) * min(max((ts - day_start).total_seconds() / 86400, 0), 1)

    lo = min(px.min(), dn.min() if len(dn) else px.min()) * 0.99999
    hi = max(px.max(), up.max() if len(up) else px.max()) * 1.00001
    span = hi - lo or 1e-9
    def Y(p):
        return 12 + (h_price - 24) * (1 - (p - lo) / span)

    def poly(series, color, dash="", w=1.4):
        pts = " ".join(f"{X(ts):.1f},{Y(v):.1f}" for ts, v in series.items()
                       if np.isfinite(v))
        return (f'<polyline points="{pts}" fill="none" stroke="{color}" '
                f'stroke-width="{w}" stroke-dasharray="{dash}"/>')

    parts = [f'<svg width="{width}" height="{h_price + h_pl + 40}" '
             f'style="background:#101418;border-radius:8px">']
    # hour grid + session shading
    parts.append(f'<rect x="{X(day_start + pd.Timedelta(hours=7)):.1f}" y="10" '
                 f'width="{X(day_start + pd.Timedelta(hours=21)) - X(day_start + pd.Timedelta(hours=7)):.1f}" '
                 f'height="{h_price - 20}" fill="#1b2430"/>')
    for hh in range(0, 25, 3):
        xx = X(day_start + pd.Timedelta(hours=hh))
        parts.append(f'<line x1="{xx:.1f}" y1="10" x2="{xx:.1f}" y2="{h_price + h_pl + 20}" '
                     f'stroke="#232b33" stroke-width="1"/>')
        parts.append(f'<text x="{xx:.1f}" y="{h_price + h_pl + 34}" fill="#8899aa" '
                     f'font-size="10" text-anchor="middle">{hh:02d}h</text>')
    parts.append(poly(up, "#e0b34d", dash="5,4", w=1.1))
    parts.append(poly(dn, "#e0b34d", dash="5,4", w=1.1))
    parts.append(poly(px, "#cfd8e3", w=1.5))

    # trades: entry triangle, exit dot, connecting line
    for tr in trades:
        ex_c = {"take_profit": "#37d67a", "stop_loss": "#ff5c5c",
                "gov_goal_bank": "#37d67a", "gov_ratchet_bank": "#4dc3ff",
                "gov_hard_stop": "#ff5c5c", "day_end": "#aaaaaa"}.get(tr["cause"], "#aaa")
        xe, ye = X(tr["ts"]), Y(tr["entry_px"])
        xx, yx = X(tr["exit_ts"]), Y(tr["exit_px"]) if tr["exit_px"] else ye
        tri = (f'{xe},{ye-6} {xe-5},{ye+4} {xe+5},{ye+4}' if tr["dir"] > 0
               else f'{xe},{ye+6} {xe-5},{ye-4} {xe+5},{ye-4}')
        dcol = "#37d67a" if tr["dir"] > 0 else "#ff8a5c"
        parts.append(f'<line x1="{xe}" y1="{ye}" x2="{xx}" y2="{yx}" '
                     f'stroke="{ex_c}" stroke-width="1" stroke-dasharray="2,2"/>')
        parts.append(f'<polygon points="{tri}" fill="{dcol}"/>')
        parts.append(f'<circle cx="{xx}" cy="{yx}" r="4" fill="{ex_c}"/>')
        parts.append(f'<title></title>')

    # day P&L step chart
    y0pl = h_price + 14
    def Ypl(v):
        return y0pl + (h_pl - 18) * (1 - (v + 2.0) / 5.0)   # scale -2..+3
    parts.append(f'<line x1="{x0}" y1="{Ypl(0):.1f}" x2="{x1}" y2="{Ypl(0):.1f}" '
                 f'stroke="#3a4750" stroke-width="1"/>')
    for lvl, col, lab in [(2.5, "#37d67a", "goal"), (-1.5, "#ff5c5c", "soft")]:
        parts.append(f'<line x1="{x0}" y1="{Ypl(lvl):.1f}" x2="{x1}" y2="{Ypl(lvl):.1f}" '
                     f'stroke="{col}" stroke-width="0.7" stroke-dasharray="3,4"/>')
        parts.append(f'<text x="{x1-2}" y="{Ypl(lvl)-3:.1f}" fill="{col}" font-size="9" '
                     f'text-anchor="end">{lab}</text>')
    steps = [(day_start, 0.0)] + [(tr["exit_ts"], tr["day_pl_after"]) for tr in trades]
    pts = []
    prev = 0.0
    for ts_, v in steps:
        pts.append(f"{X(ts_):.1f},{Ypl(prev):.1f}")
        pts.append(f"{X(ts_):.1f},{Ypl(v):.1f}")
        prev = v
    pts.append(f"{x1},{Ypl(prev):.1f}")
    parts.append(f'<polyline points="{" ".join(pts)}" fill="none" '
                 f'stroke="#4dc3ff" stroke-width="1.8"/>')

    # governor event flags
    for ev in events:
        xx = X(ev["ts"])
        lab = {"gov_soft_halt": "SOFT HALT", "gov_goal_bank_closed": "GOAL BANKED",
               "gov_ratchet_bank_closed": "RATCHET BANKED",
               "gov_day_limits_halt": "3-LOSS HALT"}.get(ev["event"], ev["event"])
        col = "#ff5c5c" if "halt" in ev["event"] else "#37d67a"
        parts.append(f'<line x1="{xx}" y1="10" x2="{xx}" y2="{h_price + h_pl + 10}" '
                     f'stroke="{col}" stroke-width="1" stroke-dasharray="6,3"/>')
        parts.append(f'<text x="{xx+3}" y="22" fill="{col}" font-size="10">{lab}</text>')
    parts.append("</svg>")
    return "".join(parts)


# ---------------------------------------------------------------- HTML pieces
def flow_svg(funnel):
    """Vertical reasoning flowchart with live counts."""
    steps = [
        ("NEW CLOSED BAR (trigger TF)", "", "#2b3a4a"),
        ("SENSE: close beyond EMA20 ± 2·ATR?", f'{funnel["raw"]} stretches seen', "#2b3a4a"),
        ("H4 TREND VETO (don't fade a strong tide)", f'−{funnel["veto"]} vetoed', "#54402a"),
        ("DAY STATE: not banked / not halted", f'−{funnel["skip_day_done"]} refused', "#54402a"),
        ("SESSION 07–21 + not Friday-late", f'−{funnel["skip_session"] + funnel["skip_friday"]} refused', "#54402a"),
        ("CAPACITY: no open position · cooldown 8m · <3 consec losses", f'−{funnel["skip_in_position"] + funnel["skip_cooldown"]} refused', "#54402a"),
        ("SIZE: 0.8% × stretch ×½^losses +ladder → cap 2% → cap day-budget", f'−{funnel["skip_risk_floor"]} too small', "#54402a"),
        ("FIRE  (SL 2·ATR · TP 1.5·ATR)", f'{funnel["trades"]} trades taken', "#1f4d33"),
        ("MANAGE: TP / SL / day-end · watchdog: goal +2.5% · ratchet · soft −1.5% · hard −2%", funnel["exits"], "#1f3a4d"),
    ]
    w, bh, gap = 860, 44, 14
    hgt = len(steps) * (bh + gap) + 20
    s = [f'<svg width="{w}" height="{hgt}">']
    y = 8
    for i, (label, note, col) in enumerate(steps):
        s.append(f'<rect x="10" y="{y}" rx="8" width="620" height="{bh}" fill="{col}" '
                 f'stroke="#46586a"/>')
        s.append(f'<text x="24" y="{y + 27}" fill="#e8eef4" font-size="13">{html.escape(label)}</text>')
        s.append(f'<text x="645" y="{y + 27}" fill="#9fb3c8" font-size="12">{html.escape(str(note))}</text>')
        if i < len(steps) - 1:
            s.append(f'<line x1="320" y1="{y + bh}" x2="320" y2="{y + bh + gap}" '
                     f'stroke="#46586a" stroke-width="2"/>')
            s.append(f'<polygon points="315,{y + bh + gap - 5} 325,{y + bh + gap - 5} 320,{y + bh + gap}" fill="#46586a"/>')
        y += bh + gap
    s.append("</svg>")
    return "".join(s)


def main():
    sym = sys.argv[1] if len(sys.argv) > 1 else "EURUSD"
    trig = sys.argv[2] if len(sys.argv) > 2 else "30min"
    sizing = sys.argv[3] if len(sys.argv) > 3 else "strength"
    spread = SPREADS.get(sym, 0.0001)

    m1 = pd.read_parquet(Path(__file__).parent / "data" / f"{sym}_M1.parquet")
    if m1.index.tz is not None:
        m1.index = m1.index.tz_convert("UTC").tz_localize(None)

    # ---- baseline with decision log ---------------------------------
    cfg, sig, t = build(m1, trig, sizing, spread)
    dlog = []
    trades, daily, _ = run(m1, cfg, sig, dlog=dlog)

    # raw vs vetoed stretch counts (recompute without the H4 veto)
    _, sig_noveto, _ = build(m1, trig, sizing, spread, htf_flat=False)
    raw = int(sig_noveto[1].sum() + sig_noveto[2].sum())
    kept = int(sig[1].sum() + sig[2].sum())
    ev_counts = Counter(e["event"] for e in dlog)
    tr_events = [e for e in dlog if e["event"] == "trade"]
    exits = Counter(e["cause"] for e in tr_events)
    funnel = {
        "raw": raw, "veto": raw - kept,
        "skip_day_done": ev_counts.get("skip_day_done", 0),
        "skip_session": ev_counts.get("skip_session", 0),
        "skip_friday": ev_counts.get("skip_friday", 0),
        "skip_in_position": ev_counts.get("skip_in_position", 0),
        "skip_cooldown": ev_counts.get("skip_cooldown", 0),
        "skip_risk_floor": ev_counts.get("skip_risk_floor", 0),
        "trades": len(tr_events),
        "exits": " · ".join(f"{k} {v}" for k, v in exits.most_common()),
    }

    # ---- rule counterfactuals ----------------------------------------
    def stats(tr, dy):
        days = sorted(dy)
        pls = [dy[d]["pl"] for d in days]
        return {"total": sum(pls), "worst": min(pls) if pls else 0,
                "breach": sum(1 for d in days if dy[d]["min_float"] <= -5.0),
                "n": len(tr)}

    base_stats = stats(trades, daily)
    cf_rows = []
    counterfactuals = [
        ("H4 trend veto OFF", dict(fade_over=dict(htf_flat=False))),
        ("Session filter OFF (trade 24h)", dict(cfg_over=dict(session=(0, 24)))),
        ("Goal bank OFF (never stop at +2.5%)", dict(cfg_over=dict(goal=99.0))),
        ("Ratchet OFF (no green-day lock)", dict(cfg_over=dict(ratchet_trigger=99.0))),
        ("Soft/hard day stops OFF", dict(cfg_over=dict(soft_stop=98.0, hard_stop=99.0))),
        ("Loss-streak halving OFF", dict(cfg_over=dict())),   # handled below
        ("Strength sizing OFF (flat lots)", dict(sizing="flat")),
        ("Cooldown OFF (0 min)", dict(cfg_over=dict(cooldown_min=0))),
    ]
    for name, spec in counterfactuals:
        fade_over = spec.get("fade_over", {})
        cfg2, sig2, _t2 = build(m1, trig, spec.get("sizing", sizing), spread, **fade_over)
        cfg_over = spec.get("cfg_over", {})
        if name.startswith("Loss-streak"):
            # halving is inline: emulate by max_consec high + no halving via base?
            # engine halves via streak; disable by resetting streak -> approximate
            # with max_consec_losses large AND base unchanged is not equivalent;
            # easiest faithful switch: monkey config max_consec high + halving
            # not configurable -> skip risk-halving toggle honestly:
            cf_rows.append((name, None, "not separable in engine — halving is "
                            "coupled to streak; test in EA via InpLossStreakHalving"))
            continue
        cfg2 = replace(cfg2, **cfg_over)
        tr2, dy2, _ = run(m1, cfg2, sig2)
        st = stats(tr2, dy2)
        cf_rows.append((name, st, None))

    # ---- pick days for the gallery -----------------------------------
    traded_days = {d: v for d, v in daily.items() if v["trades"] > 0}
    by_pl = sorted(traded_days, key=lambda d: traded_days[d]["pl"])
    banked = [d for d in traded_days if traded_days[d]["banked"]]
    halted = [d for d in traded_days if traded_days[d]["halted"]]
    gallery, seen = [], set()
    for d in (list(reversed(by_pl))[:3] + by_pl[:3] + banked[:2] + halted[:2]):
        if d not in seen:
            seen.add(d)
            gallery.append(d)

    # ---- render -------------------------------------------------------
    css = """
    body{background:#0b0f13;color:#dbe4ee;font-family:system-ui,Segoe UI,Arial;
         max-width:1000px;margin:24px auto;padding:0 16px}
    h1,h2{color:#fff} h2{margin-top:38px;border-bottom:1px solid #26303a;padding-bottom:6px}
    table{border-collapse:collapse;width:100%;font-size:13px}
    td,th{border:1px solid #26303a;padding:6px 9px;text-align:left}
    th{background:#141b22} .good{color:#37d67a} .bad{color:#ff5c5c} .warn{color:#e0b34d}
    .log{font-family:ui-monospace,monospace;font-size:11.5px;color:#9fb3c8;
         background:#0f141a;padding:8px;border-radius:6px;white-space:pre-wrap}
    .day{margin:26px 0;padding:14px;background:#0e1319;border:1px solid #1d2732;border-radius:10px}
    .kpi{display:inline-block;background:#141b22;border:1px solid #26303a;border-radius:8px;
         padding:8px 14px;margin:4px 6px 4px 0;font-size:13px}
    """
    H = [f"<!doctype html><html><head><meta charset='utf-8'>"
         f"<title>Sentinel thought map — {sym}</title><style>{css}</style></head><body>"]
    H.append(f"<h1>Sentinel thought map — {sym} {trig} fade ({sizing} sizing)</h1>")
    H.append(f"<p>Window {m1.index[0]} → {m1.index[-1]} · every number below comes from "
             f"the instrumented engine (real M1 data, real costs). Generated by "
             f"<code>thought_map.py</code>.</p>")
    days = sorted(daily)
    pls = [daily[d]["pl"] for d in days]
    H.append(f"<div><span class='kpi'>total <b>{sum(pls):+.2f}%</b></span>"
             f"<span class='kpi'>mean day <b>{np.mean(pls):+.3f}%</b></span>"
             f"<span class='kpi'>worst day <b class='bad'>{min(pls):+.2f}%</b></span>"
             f"<span class='kpi'>trades <b>{len(tr_events)}</b></span>"
             f"<span class='kpi'>FTMO breaches <b class='good'>"
             f"{sum(1 for d in days if daily[d]['min_float'] <= -5)}</b></span></div>")

    H.append("<h2>1 · How a thought becomes a trade (live counts)</h2>")
    H.append(flow_svg(funnel))

    H.append("<h2>2 · Rule counterfactuals — what each belief costs or saves</h2>")
    H.append("<p>Each row re-runs the whole history with ONE rule disabled. "
             "If removing a rule makes money without adding breach risk, that rule "
             "is a deficiency candidate. If removing it hurts, the belief is earning rent.</p>")
    H.append("<table><tr><th>Rule disabled</th><th>total P&L</th><th>Δ vs baseline "
             f"({base_stats['total']:+.2f}%)</th><th>worst day</th><th>breaches</th>"
             "<th>trades</th><th>verdict</th></tr>")
    for name, st, note in cf_rows:
        if st is None:
            H.append(f"<tr><td>{name}</td><td colspan=6>{note}</td></tr>")
            continue
        d = st["total"] - base_stats["total"]
        if st["breach"] > 0:
            verdict, cls = "rule prevents FTMO breaches — KEEP", "bad"
        elif d > 1.0:
            verdict, cls = "costs money — investigate loosening", "warn"
        elif d < -1.0:
            verdict, cls = "earning its keep — KEEP", "good"
        else:
            verdict, cls = "neutral on this window", ""
        H.append(f"<tr><td>{name}</td><td>{st['total']:+.2f}%</td>"
                 f"<td>{d:+.2f}%</td><td>{st['worst']:+.2f}%</td>"
                 f"<td>{st['breach']}</td><td>{st['n']}</td>"
                 f"<td class='{cls}'>{verdict}</td></tr>")
    H.append("</table>")

    H.append("<h2>3 · Days in the life (best · worst · banked · halted)</h2>")
    H.append("<p>Shaded = 07–21 session. Dashed gold = Keltner bands (the 'sense'). "
             "Triangles = entries (up=long), dots = exits (green TP, red SL, blue ratchet). "
             "Bottom lane = running day P&L vs goal/soft lines.</p>")
    for d in gallery:
        v = daily[d]
        trs = [e for e in tr_events if e["ts"].date() == d]
        evs = [e for e in dlog if e["event"].startswith("gov_") and e["ts"].date() == d]
        skips = [e for e in dlog if e["event"].startswith("skip_") and e["ts"].date() == d]
        tag = "BANKED" if v["banked"] else ("HALTED" if v["halted"] else "")
        H.append(f"<div class='day'><b>{d} · {v['pl']:+.2f}% · {v['trades']} trades "
                 f"<span class='{'good' if v['pl'] >= 0 else 'bad'}'>{tag}</span></b><br>")
        H.append(svg_day(m1, t, d, trs, evs))
        loglines = []
        for e in sorted(trs + skips + evs, key=lambda e: e["ts"]):
            if e["event"] == "trade":
                loglines.append(
                    f"{e['ts'].strftime('%H:%M')}  FIRE {'LONG' if e['dir']>0 else 'SHORT'} "
                    f"risk {e['risk']}% (base {e['r_base']} × stretch {e['r_strength']}"
                    f"{' × ½streak' if e['r_after_streak'] < e['r_base']*e['r_strength'] else ''}) "
                    f"→ exit {e['exit_ts'].strftime('%H:%M')} {e['cause']} "
                    f"pnl {e['pnl']:+.2f}% → day {e['day_pl_after']:+.2f}%")
            elif e["event"].startswith("gov_"):
                loglines.append(f"{e['ts'].strftime('%H:%M')}  GOVERNOR {e['event'][4:]} "
                                f"(day {e.get('day_pl', '')}%)")
            else:
                loglines.append(f"{e['ts'].strftime('%H:%M')}  saw a stretch but refused: "
                                f"{e['event'][5:]}")
        H.append("<div class='log'>" + html.escape("\n".join(loglines) or "(quiet day)")
                 + "</div></div>")

    H.append("<h2>4 · How to use this to fix the bot</h2><ol>"
             "<li>Funnel (§1): if too many thoughts die at one gate, that gate is "
             "either protecting you or starving you — check its row in §2.</li>"
             "<li>Counterfactuals (§2): any rule marked 'costs money' with zero breach "
             "impact is a candidate to loosen — change it in the EA inputs, re-run "
             "this map, compare.</li>"
             "<li>Day gallery (§3): read the losing days' logs bottom-up — the usual "
             "deficiencies are visible as patterns: fading a runaway trend repeatedly "
             "(H4 veto too loose), banking green too early (ratchet too tight), or "
             "sitting out a recovery (soft stop too tight).</li>"
             "<li>Regenerate: <code>python3 thought_map.py EURUSD 30min strength</code> "
             "(any symbol/TF/sizing with data).</li></ol>")
    H.append("</body></html>")

    out = Path(__file__).parent / f"THOUGHT_MAP_{sym}.html"
    out.write_text("".join(H))
    print(f"[written] {out}  ({out.stat().st_size/1024:.0f} KB)")
    print("funnel:", funnel)
    for name, st, note in cf_rows:
        if st:
            print(f"  CF {name}: total {st['total']:+.2f}% (Δ {st['total']-base_stats['total']:+.2f}) "
                  f"worst {st['worst']:+.2f} breaches {st['breach']}")


if __name__ == "__main__":
    main()

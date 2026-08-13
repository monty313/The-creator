"""Visual THOUGHT MAP — see how the policy thinks through a trading day.

Replays real days through the production goal path with an observe-only trace
(zero behavior change), auto-diagnoses deficiencies, and writes ONE
self-contained HTML file (no server, open in any browser).

What you see per day:
  - Timeline: running PnL vs typed target and risk floor, with every decision
    marked (fired long/short, brain-wait on a live edge, blocked, watch miss)
  - Per-slot thought chain: EDGE -> SENSES -> BRAIN (probs + size head) ->
    GATES/OVERRIDES -> SIZE (branch + math) -> FILL -> ledger after
  - Deficiency panel: counted, classified, clickable — each one is a concrete
    training/curriculum fix target

Usage:
  # Replay N days of the pinned protocol (same seed/pairs as forward tests)
  python tools/thought_map.py --days 10 --seed 42 --symbols XAUUSD

  # Specific dates with a typed pair
  python tools/thought_map.py --dates 2026-06-22 --target 5 --risk 3

  # A candidate instead of the champion
  python tools/thought_map.py --days 5 --champion path/to/lab.npz
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import numpy as np

from evidence_court.meta_rl.edge import build_tf_cache
from evidence_court.meta_rl.forward_eval import DEFAULT_RISK_GRID, DEFAULT_TARGET_GRID
from evidence_court.meta_rl.goal_path import run_goal_path_day
from evidence_court.meta_rl.policy import load_or_train_champion
from evidence_court.meta_rl.price_io import (
    SYMBOL_FILES,
    bars_to_daily,
    load_m1_trailing_calendar_days,
)

OUT_DEFAULT = _ROOT / "evidence_court" / "artifacts" / "reports" / "thought_map.html"


# ---------------------------------------------------------------- deficiencies
def diagnose_day(day: Dict[str, Any]) -> List[Dict[str, str]]:
    """Turn a day's trace into named, fixable deficiency flags."""
    tr = day["trace"]
    target = float(day["target"])
    flags: List[Dict[str, str]] = []

    fired = [t for t in tr if t["event"] == "fired"]
    waits = [t for t in tr if t["event"] == "brain_wait"]
    misses = [t for t in tr if t["event"] == "watch_miss"]
    blocked = [t for t in tr if t["event"].startswith("blocked")]
    scans = [t for t in tr if t["event"] == "scan"]

    def flag(kind: str, msg: str, fix: str, slot: str = "") -> None:
        flags.append({"kind": kind, "msg": msg, "fix": fix, "slot": slot})

    # 1. Brain waits on live edges (conversion killer #1)
    prime_waits = [w for w in waits if w.get("prime")]
    if len(waits) >= 3:
        flag(
            "BRAIN_WAIT_ON_EDGE",
            f"{len(waits)} live edge candidates where the brain chose wait "
            f"({len(prime_waits)} in London/NY prime)",
            "Path-state teachers: harvest these exact packed states, teach edge side "
            "(CASE-0037 class). These rows are listed below — each is a training example.",
        )

    # 2. Watch misses — sensors saw PB/cont, bot flat that slot
    if len(misses) >= 5:
        ln = [m for m in misses if m.get("session_band") == "london_ny"]
        flag(
            "SIGHT_MISS",
            f"{len(misses)} Watch complaints (sensors saw pullback/continuation, "
            f"no fire) — {len(ln)} in London/NY",
            "A28 curriculum labels already collected on this path — feed them to "
            "meta-train --labels (C-002 opportunity mix).",
        )

    # 3. Zero-trade day with candidates present
    n_cand = sum(int(s.get("n_candidates") or 0) for s in scans)
    if not fired and n_cand > 0:
        flag(
            "FLAT_DAY_WITH_EDGES",
            f"0 fills but {n_cand} candidate edges were scanned",
            "Sight fail mode (A32): flat on a day with edges. Check brain_wait rows "
            "for the common state pattern (low probs on real edges).",
        )

    # 4. Target never threatened despite firing
    if fired:
        peak = max(f["fill"]["pnl_after"] for f in fired)
        if peak < 0.3 * target and len(fired) >= 8:
            flag(
                "TARGET_NEVER_THREATENED",
                f"{len(fired)} fills but peak day PnL {peak:+.2f}% never reached 30% "
                f"of typed target {target:.0f}%",
                "Size/hold too small for the typed goal — size-until-win lever: "
                "size teachers from real fills on near-clear days, or raise "
                "expect-R hold on high-conviction continuation.",
            )

    # 5. Gave back a large peak (late bleed)
    if fired:
        peak = max(f["fill"]["pnl_after"] for f in fired)
        final = fired[-1]["fill"]["pnl_after"]
        if peak >= 0.5 * target and final < 0.5 * peak and peak > 0.5:
            flag(
                "GAVE_BACK_PEAK",
                f"peaked {peak:+.2f}% then closed {final:+.2f}% — gave back "
                f"{100 * (1 - final / peak):.0f}% of the day's best",
                "Hearing fail mode (A32): stale story into regime shift. Teach "
                "size-down / lock after progress>0.6 when tide flips (taste/hearing "
                "channels into size head).",
            )

    # 6. Budget exhausted before prime session ended
    ends = [t for t in tr if t["event"] == "day_end" and t.get("reason") == "risk_budget_exhausted"]
    for e in ends:
        if str(e.get("slot", "")) < "16:00:00":
            flag(
                "BUDGET_BURNT_EARLY",
                f"risk budget exhausted at {e['slot']} (day PnL {e.get('pnl', 0):+.2f}%)",
                "Feel fail mode: overtrading into chop — raise wait prior on "
                "low-quality slots or shrink early-leg size (budget discipline "
                "teachers).",
                slot=str(e.get("slot", "")),
            )

    # 7. Consecutive-loss cluster
    run = best_run = 0
    for f in fired:
        run = run + 1 if f["fill"]["pnl"] < 0 else 0
        best_run = max(best_run, run)
    if best_run >= 4:
        flag(
            "LOSS_CLUSTER",
            f"{best_run} consecutive losing fills",
            "Same-state re-entry thrash: check if repeated fills share edge/state "
            "pattern; teach wait after N same-side stops in unchanged regime.",
        )

    # 8. Envelope blocks (brain asked for illegal size)
    env = [b for b in blocked if b["event"] == "blocked_envelope"]
    if len(env) >= 3:
        flag(
            "ENVELOPE_BLOCKS",
            f"{len(env)} decisions blocked at the envelope (size zero / would breach)",
            "Size head asks for more than remaining budget late in day — teach "
            "remaining-risk-aware sizing (budget discipline term).",
        )

    # 9. Side overrides — brain fought the edge
    overr = [f for f in fired if f.get("override")]
    if len(overr) >= 3:
        flag(
            "SIDE_DISAGREE",
            f"{len(overr)} fills where brain side was overridden to edge side",
            "Brain's act head disagrees with multi-set consensus on side — "
            "harvest these states with edge-side teachers (side-miss class).",
        )
    return flags


# ---------------------------------------------------------------------- replay
def replay_days(
    *,
    dates: List[str],
    pairs: List[tuple],
    symbols: List[str],
    champion: Optional[str],
) -> List[Dict[str, Any]]:
    m1_by_sym: Dict[str, List[dict]] = {}
    caches: Dict[str, Dict[str, List[dict]]] = {}
    for sym in symbols:
        p = SYMBOL_FILES.get(sym)
        if p is None or not p.exists():
            raise SystemExit(f"no data for {sym} — run tools/download_dukascopy_m1.py")
        m1 = load_m1_trailing_calendar_days(p, n_days=400)
        m1_by_sym[sym] = m1
        caches[sym] = build_tf_cache(m1)

    pol = load_or_train_champion(path=Path(champion) if champion else None)
    pol.assert_frozen()
    fp = pol.weight_fingerprint()

    days: List[Dict[str, Any]] = []
    for date, (t, r) in zip(dates, pairs):
        fills, ledger, meta = run_goal_path_day(
            pol,
            date=date,
            m1_by_symbol=m1_by_sym,
            target_percent=float(t),
            max_daily_risk_percent=float(r),
            symbols=symbols,
            tf_cache_by_symbol=caches,
            collect_thought_trace=True,
        )
        pol.assert_frozen()
        pnl = float(ledger.realized_pnl_percent)
        day = {
            "date": date,
            "target": float(t),
            "risk": float(r),
            "pnl": round(pnl, 3),
            "hit": bool(pnl >= float(t) - 1e-9),
            "breach": bool(max(-pnl, 0.0) > float(r) + 1e-6),
            "n_fills": len(fills),
            "watch_misses": int(meta.get("watch_n_misses") or 0),
            "trace": meta.get("thought_trace") or [],
            "fingerprint": fp,
        }
        day["deficiencies"] = diagnose_day(day)
        days.append(day)
        print(
            f"  {date} T={t:.0f} R={r:.0f} -> pnl {pnl:+.2f}% fills {len(fills)} "
            f"hit {day['hit']} defects {len(day['deficiencies'])}"
        )
    return days


# ------------------------------------------------------------------------ html
def render_html(days: List[Dict[str, Any]], out: Path) -> None:
    payload = json.dumps(days, separators=(",", ":"))
    html = HTML_TEMPLATE.replace("__DATA__", payload)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>Policy Thought Map</title>
<style>
:root{--bg:#0d1117;--panel:#161b22;--line:#30363d;--txt:#c9d1d9;--dim:#8b949e;
--green:#3fb950;--red:#f85149;--amber:#d29922;--purple:#bc8cff;--blue:#58a6ff;}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--txt);font:14px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;margin:0;padding:20px}
h1{font-size:20px;margin:0 0 4px}
h2{font-size:15px;margin:18px 0 8px;color:var(--blue)}
.sub{color:var(--dim);font-size:12px;margin-bottom:14px}
select{background:var(--panel);color:var(--txt);border:1px solid var(--line);border-radius:6px;padding:6px 10px;font-size:14px}
.hdr{display:flex;gap:18px;align-items:center;flex-wrap:wrap;margin-bottom:10px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:8px 14px;text-align:center}
.stat b{display:block;font-size:17px}
.stat span{font-size:11px;color:var(--dim)}
.hit b{color:var(--green)}.miss b{color:var(--amber)}.breach b{color:var(--red)}
.defs{display:flex;flex-direction:column;gap:8px;margin-bottom:14px}
.def{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--amber);border-radius:8px;padding:10px 14px;cursor:pointer}
.def.active{border-left-color:var(--blue);background:#1c2430}
.def b{color:var(--amber)}
.def .fix{color:var(--dim);font-size:12.5px;margin-top:4px}
.def .fix::before{content:"FIX → ";color:var(--green);font-weight:600}
.ok{border-left-color:var(--green)}.ok b{color:var(--green)}
svg{background:var(--panel);border:1px solid var(--line);border-radius:8px;width:100%}
.legend{font-size:12px;color:var(--dim);margin:6px 0 16px;display:flex;gap:16px;flex-wrap:wrap}
.legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px}
table{width:100%;border-collapse:collapse;font-size:12.5px}
details{background:var(--panel);border:1px solid var(--line);border-radius:8px;margin-bottom:6px;overflow:hidden}
details.hl{border-color:var(--blue);box-shadow:0 0 0 1px var(--blue)}
summary{padding:8px 12px;cursor:pointer;display:grid;grid-template-columns:70px 80px 90px 1fr 110px;gap:10px;align-items:center}
summary:hover{background:#1c2430}
.ev{font-weight:600;padding:1px 8px;border-radius:10px;font-size:11px;text-align:center}
.ev.fired-long{background:#1c3325;color:var(--green)}
.ev.fired-short{background:#3a1d20;color:var(--red)}
.ev.brain_wait{background:#2d2a1f;color:var(--amber)}
.ev.blocked{background:#33272d;color:#ff9bce}
.ev.watch_miss{background:#2a2138;color:var(--purple)}
.ev.scan,.ev.day_end{background:#21262d;color:var(--dim)}
.chain{padding:10px 14px;border-top:1px solid var(--line);display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px}
.box{background:#0d1117;border:1px solid var(--line);border-radius:6px;padding:8px 10px;font-size:12px}
.box h4{margin:0 0 6px;font-size:11px;letter-spacing:.08em;color:var(--blue)}
.box .kv{display:flex;justify-content:space-between;gap:8px}
.box .kv span:first-child{color:var(--dim)}
.bar{height:10px;border-radius:3px;background:#21262d;overflow:hidden;display:flex;margin:2px 0 6px}
.bar i{height:100%}
.pw{background:#6e7681}.pl{background:var(--green)}.ps{background:var(--red)}
.mut{color:var(--dim)}
.out{padding:0 14px 10px;color:var(--dim);font-size:12px}
</style>
</head>
<body>
<h1>Policy Thought Map</h1>
<div class="sub">every decision the frozen policy made, why, and what to fix — observe-only trace, zero behavior change</div>
<div class="hdr">
  <select id="daysel"></select>
  <div class="stat" id="s_pnl"><b>—</b><span>day PnL</span></div>
  <div class="stat" id="s_tgt"><b>—</b><span>typed target</span></div>
  <div class="stat" id="s_rsk"><b>—</b><span>typed risk</span></div>
  <div class="stat" id="s_fll"><b>—</b><span>fills</span></div>
  <div class="stat" id="s_hit"><b>—</b><span>hit</span></div>
  <div class="stat" id="s_fp" style="max-width:280px"><b style="font-size:11px">—</b><span>weights (frozen)</span></div>
</div>

<h2>Deficiencies — click one to highlight its evidence below</h2>
<div class="defs" id="defs"></div>

<h2>Day timeline</h2>
<svg id="tl" height="260" viewBox="0 0 1200 260" preserveAspectRatio="none"></svg>
<div class="legend">
  <span><i style="background:var(--green)"></i>fired long</span>
  <span><i style="background:var(--red)"></i>fired short</span>
  <span><i style="background:var(--amber)"></i>brain wait on live edge</span>
  <span><i style="background:#ff9bce"></i>blocked (gate)</span>
  <span><i style="background:var(--purple)"></i>watch miss (sensors saw, bot flat)</span>
  <span><i style="background:var(--blue)"></i>running PnL</span>
  <span><i style="background:#6e7681"></i>target / −risk lines</span>
</div>

<h2>Thought chain — slot by slot</h2>
<div id="rows"></div>

<script>
const DAYS = __DATA__;
const $ = id => document.getElementById(id);
const sel = $("daysel");
DAYS.forEach((d,i)=>{const o=document.createElement("option");o.value=i;
o.textContent=`${d.date}  ·  T=${d.target}% R=${d.risk}%  ·  pnl ${d.pnl>=0?"+":""}${d.pnl}%  ·  ${d.hit?"HIT":"miss"}  ·  ${d.deficiencies.length} defects`;
sel.appendChild(o);});
sel.onchange = ()=>show(+sel.value);

let activeKind = null;

function toMin(t){const p=t.split(":");return (+p[0])*60+(+p[1]);}

function show(ix){
  const d = DAYS[ix];
  activeKind = null;
  $("s_pnl").firstChild.textContent = (d.pnl>=0?"+":"")+d.pnl+"%";
  $("s_pnl").firstChild.style.color = d.pnl>=0?"var(--green)":"var(--red)";
  $("s_tgt").firstChild.textContent = d.target+"%";
  $("s_rsk").firstChild.textContent = d.risk+"%";
  $("s_fll").firstChild.textContent = d.n_fills;
  $("s_hit").firstChild.textContent = d.hit?"YES":(d.breach?"BREACH":"no");
  $("s_hit").firstChild.style.color = d.hit?"var(--green)":(d.breach?"var(--red)":"var(--amber)");
  $("s_fp").firstChild.textContent = d.fingerprint;
  drawDefs(d); drawTimeline(d); drawRows(d);
}

function drawDefs(d){
  const el = $("defs"); el.innerHTML="";
  if(!d.deficiencies.length){
    el.innerHTML = '<div class="def ok"><b>No deficiency flags on this day</b><div class="fix">nothing auto-detected — inspect the chain below for subtler issues</div></div>';
    return;
  }
  d.deficiencies.forEach(f=>{
    const div=document.createElement("div");div.className="def";
    div.innerHTML=`<b>${f.kind}</b> — ${f.msg}<div class="fix">${f.fix}</div>`;
    div.onclick=()=>{activeKind = activeKind===f.kind?null:f.kind;
      document.querySelectorAll(".def").forEach(x=>x.classList.remove("active"));
      if(activeKind)div.classList.add("active");
      drawRows(d);};
    el.appendChild(div);
  });
}

function kindMatches(kind,t){
  switch(kind){
    case "BRAIN_WAIT_ON_EDGE": return t.event==="brain_wait";
    case "SIGHT_MISS": return t.event==="watch_miss";
    case "FLAT_DAY_WITH_EDGES": return t.event==="brain_wait"||t.event==="watch_miss";
    case "TARGET_NEVER_THREATENED": return t.event==="fired";
    case "GAVE_BACK_PEAK": return t.event==="fired"&&t.fill&&t.fill.pnl<0;
    case "BUDGET_BURNT_EARLY": return t.event==="day_end"||(t.event==="fired"&&t.fill&&t.fill.pnl<0);
    case "LOSS_CLUSTER": return t.event==="fired"&&t.fill&&t.fill.pnl<0;
    case "ENVELOPE_BLOCKS": return t.event==="blocked_envelope";
    case "SIDE_DISAGREE": return t.event==="fired"&&t.override;
    default: return false;
  }
}

function drawTimeline(d){
  const svg=$("tl");const W=1200,H=260,L=46,R=12,T=14,B=26;
  const tr=d.trace;
  const tmin=7*60, tmax=20*60+10;
  const x=t=>L+(W-L-R)*(toMin(t)-tmin)/(tmax-tmin);
  const fired=tr.filter(t=>t.event==="fired");
  let lo=Math.min(-d.risk*1.15,...fired.map(f=>f.fill.pnl_after),-0.5);
  let hi=Math.max(d.target*1.08,...fired.map(f=>f.fill.pnl_after),0.5);
  const y=v=>T+(H-T-B)*(1-(v-lo)/(hi-lo));
  let s="";
  // grid: 0, target, -risk
  const grid=[[0,"#30363d","0"],[d.target,"#6e7681","target "+d.target+"%"],[-d.risk,"#6e7681","-risk "+d.risk+"%"]];
  grid.forEach(([v,c,lab])=>{
    s+=`<line x1="${L}" x2="${W-R}" y1="${y(v)}" y2="${y(v)}" stroke="${c}" stroke-dasharray="4 4"/>`;
    s+=`<text x="${L-4}" y="${y(v)+4}" fill="#8b949e" font-size="10" text-anchor="end">${lab}</text>`;});
  // hour ticks
  for(let h=7;h<=20;h++){const xx=x(`${String(h).padStart(2,"0")}:00:00`);
    s+=`<text x="${xx}" y="${H-8}" fill="#8b949e" font-size="10" text-anchor="middle">${h}:00</text>`;}
  // pnl path
  let px=L,py=y(0),path=`M ${px} ${py}`;
  fired.forEach(f=>{const xx=x(f.slot),yy=y(f.fill.pnl_after);path+=` L ${xx} ${py=yy}`;px=xx;});
  path+=` L ${W-R} ${py}`;
  s+=`<path d="${path}" fill="none" stroke="#58a6ff" stroke-width="2"/>`;
  // markers
  tr.forEach(t=>{
    if(!t.slot)return;const xx=x(t.slot);
    if(t.event==="fired"){
      const yy=y(t.fill.pnl_after);
      const r=3+7*Math.min(t.size.final/Math.max(d.risk,0.5),1);
      const c=t.fill.act==="long"?"#3fb950":"#f85149";
      s+=`<circle cx="${xx}" cy="${yy}" r="${r.toFixed(1)}" fill="${c}" fill-opacity="0.85"><title>${t.slot} ${t.symbol} ${t.outcome} (size src ${t.size.source})</title></circle>`;
    }else if(t.event==="brain_wait"){
      s+=`<rect x="${xx-3}" y="${T}" width="6" height="7" fill="#d29922" fill-opacity="0.9"><title>${t.slot} ${t.symbol} ${t.outcome} probs w${t.brain.probs.wait}/l${t.brain.probs.long}/s${t.brain.probs.short}</title></rect>`;
    }else if(t.event.startsWith("blocked")){
      s+=`<rect x="${xx-3}" y="${T+10}" width="6" height="7" fill="#ff9bce"><title>${t.slot} ${t.symbol||""} ${t.event}: ${t.outcome||""}</title></rect>`;
    }else if(t.event==="watch_miss"){
      s+=`<rect x="${xx-2}" y="${T+20}" width="4" height="6" fill="#bc8cff"><title>${t.slot} ${t.symbol} watch miss ${t.side} ${t.topology}</title></rect>`;
    }});
  svg.innerHTML=s;
}

function probBar(p){return `<div class="bar"><i class="pw" style="width:${p.wait*100}%"></i><i class="pl" style="width:${p.long*100}%"></i><i class="ps" style="width:${p.short*100}%"></i></div>
<div class="kv mut"><span>wait ${p.wait}</span><span>long ${p.long}</span><span>short ${p.short}</span></div>`;}

function drawRows(d){
  const el=$("rows");el.innerHTML="";
  const interesting=d.trace.filter(t=>["fired","brain_wait","blocked_envelope","blocked_conflict","blocked_lot","blocked_window","watch_miss","day_end"].includes(t.event));
  interesting.forEach(t=>{
    const det=document.createElement("details");
    if(activeKind&&kindMatches(activeKind,t))det.classList.add("hl");
    let evc=t.event, evl=t.event;
    if(t.event==="fired"){evc="fired-"+t.fill.act;evl=t.fill.act.toUpperCase()+" "+t.size.final+"%";}
    if(t.event.startsWith("blocked")){evc="blocked";}
    const pnl=t.fill?`${t.fill.pnl>=0?"+":""}${t.fill.pnl}% → day ${t.fill.pnl_after>=0?"+":""}${t.fill.pnl_after}%`:(t.event==="day_end"?`END: ${t.reason}`:"");
    det.innerHTML=`<summary>
      <span class="mut">${t.slot||""}</span>
      <span>${t.symbol||""}</span>
      <span class="ev ${evc}">${evl}</span>
      <span class="mut">${t.outcome||t.reason||(t.side?`sensors saw ${t.side} ${t.topology}`:"")}</span>
      <span>${pnl}</span></summary>`;
    if(t.brain){
      const chain=document.createElement("div");chain.className="chain";
      chain.innerHTML=`
      <div class="box"><h4>EDGE (what it saw)</h4>
        <div class="kv"><span>side</span><b>${t.edge.act}</b></div>
        <div class="kv"><span>force</span><span>${t.edge.force}</span></div>
        <div class="kv"><span>consensus</span><span>${t.edge.consensus}</span></div>
        <div class="kv"><span>topology</span><span>${t.topology}</span></div>
        <div class="kv"><span>HTF sets agree</span><span>${t.edge.n_htf_active}</span></div>
        <div class="kv"><span>quality rank</span><span>${t.quality}</span></div></div>
      <div class="box"><h4>SENSES</h4>
        <div class="kv"><span>sight</span><span>${t.senses.sight}</span></div>
        <div class="kv"><span>feel</span><span>${t.senses.feel}</span></div>
        <div class="kv"><span>taste</span><span>${t.senses.taste}</span></div>
        <div class="kv"><span>hearing</span><span>${t.senses.hearing||"—"}</span></div></div>
      <div class="box"><h4>GOAL / RISK CONTEXT</h4>
        <div class="kv"><span>progress→target</span><span>${(t.ctx.progress*100).toFixed(0)}%</span></div>
        <div class="kv"><span>day pnl</span><span>${t.ctx.pnl>=0?"+":""}${t.ctx.pnl}%</span></div>
        <div class="kv"><span>risk left</span><span>${t.ctx.remaining}%</span></div>
        <div class="kv"><span>fills so far</span><span>${t.ctx.n_fills}</span></div>
        <div class="kv"><span>wounded</span><span>${t.ctx.wounded}</span></div></div>
      <div class="box"><h4>BRAIN (what it thought)</h4>
        ${probBar(t.brain.probs)}
        <div class="kv"><span>decision</span><b>${t.brain.act}</b></div>
        <div class="kv"><span>size head σ</span><span>${t.brain.size_sig}</span></div>
        <div class="kv"><span>size asked</span><span>${t.brain.size_risk_percent}%</span></div>
        <div class="kv mut" style="margin-top:4px"><span>${t.brain.reason.slice(0,60)}</span></div></div>
      ${t.size?`<div class="box"><h4>SIZE (what went out)</h4>
        <div class="kv"><span>final</span><b>${t.size.final??t.size.attempted}%</b></div>
        <div class="kv"><span>source</span><span>${t.size.source}</span></div>
        ${t.size.brain_asked!==undefined?`<div class="kv"><span>brain asked</span><span>${t.size.brain_asked}%</span></div>`:""}
        ${t.size.frac_of_remaining_before!==undefined?`<div class="kv"><span>% of remaining</span><span>${(t.size.frac_of_remaining_before*100).toFixed(0)}%</span></div>`:""}
        ${t.override?`<div class="kv"><span>override</span><span>${t.override}</span></div>`:""}</div>`:""}
      ${t.fill?`<div class="box"><h4>FILL (what happened)</h4>
        <div class="kv"><span>result</span><b style="color:${t.fill.pnl>=0?"var(--green)":"var(--red)"}">${t.fill.pnl>=0?"+":""}${t.fill.pnl}%</b></div>
        <div class="kv"><span>day after</span><span>${t.fill.pnl_after>=0?"+":""}${t.fill.pnl_after}%</span></div>
        <div class="kv"><span>risk left after</span><span>${t.fill.remaining_after}%</span></div>
        <div class="kv"><span>held until</span><span>${t.fill.window_end}</span></div></div>`:""}`;
      det.appendChild(chain);
    } else if(t.outcome||t.reason){
      const o=document.createElement("div");o.className="out";o.textContent=t.outcome||t.reason;det.appendChild(o);
    }
    el.appendChild(det);
  });
}
show(0);
</script>
</body>
</html>
"""


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--days", type=int, default=0, help="replay last N protocol days")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--dates", type=str, default="", help="comma list YYYY-MM-DD")
    ap.add_argument("--target", type=float, default=0, help="with --dates: typed target%%")
    ap.add_argument("--risk", type=float, default=0, help="with --dates: typed risk%%")
    ap.add_argument("--symbols", type=str, default="XAUUSD")
    ap.add_argument("--champion", type=str, default="")
    ap.add_argument("--out", type=str, default=str(OUT_DEFAULT))
    args = ap.parse_args(argv)

    symbols = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]

    if args.dates:
        dates = [d.strip() for d in args.dates.split(",") if d.strip()]
        if args.target and args.risk:
            pairs = [(args.target, args.risk)] * len(dates)
        else:
            rng = np.random.default_rng(args.seed)
            pairs = [
                (float(rng.choice(DEFAULT_TARGET_GRID)), float(rng.choice(DEFAULT_RISK_GRID)))
                for _ in dates
            ]
    else:
        n = args.days or 10
        # Same day/pair drawing as the pinned forward protocol
        p = SYMBOL_FILES.get(symbols[0])
        if p is None or not p.exists():
            raise SystemExit(f"no data for {symbols[0]}")
        m1 = load_m1_trailing_calendar_days(p, n_days=400)
        all_dates = [d["date"] for d in bars_to_daily(m1)]
        warmup = 15
        window = all_dates[-(n + warmup):]
        dates = window[warmup:] if len(window) > warmup else window[1:]
        rng = np.random.default_rng(args.seed)
        pairs = [
            (float(rng.choice(DEFAULT_TARGET_GRID)), float(rng.choice(DEFAULT_RISK_GRID)))
            for _ in dates
        ]

    print(f"thought map: {len(dates)} day(s), symbols {symbols}")
    days = replay_days(
        dates=dates, pairs=pairs, symbols=symbols, champion=args.champion or None
    )
    out = Path(args.out)
    render_html(days, out)
    n_def = sum(len(d["deficiencies"]) for d in days)
    print(f"WROTE {out}  ({len(days)} days, {n_def} deficiency flags)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

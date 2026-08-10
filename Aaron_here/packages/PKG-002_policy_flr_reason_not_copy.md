# PKG-002 — Teach the Court policy Force + LTF state (not answer-copy)

**Teacher:** Aaron (@Aaron_here)  
**Student:** MetaBrain / CASE-0037 lineage  
**Stage:** Process supervision under risk rails  

**Forbidden language:** Do **not** use **Load** or **Reclaim**.  
**Required language:** **Force** + **pullback** | **continuation** | **calibrating**.

---

## Method first (named) — Monty binding language

| Term | In this bot |
|------|-------------|
| **Force** | **Both HTFs of an official set agree** (2 HTFs). Side = that dual-HTF side only. |
| **State** | On **LTF of that set**, relative to Force: **pullback** / **continuation** / **calibrating** |
| **Objective** | Clear target under daily risk envelope (breach 0); progressive size-up; size-down near breach |

### Force

- Mark set = 1 LTF + **2 HTFs** (set1: 1m|15m+30m; set2: 5m|30m+1h; set3: 15m|1h+4h; set4: 30m|4h+1d).  
- Force ON only if **both HTFs** agree. One HTF is not enough.

### LTF state (RSI vs its BBs)

| Force | Pullback | Continuation | Calibrating |
|-------|----------|--------------|-------------|
| **Bull** | RSI **below** its BBs | RSI **above** its BBs | RSI **between** BBs |
| **Bear** | RSI **above** its BBs | RSI **below** its BBs | RSI **between** BBs |

| State | Action bias |
|-------|-------------|
| Pullback | **WAIT** — do not fire |
| Continuation | Preferred **FIRE** side = Force (under rails) |
| Calibrating | **WAIT** — no thrash |

```text
No Force (HTFs disagree) → WAIT
Force + pullback → WAIT
Force + calibrating → WAIT
Force + continuation → FIRE side=Force under rails
Thrash / LTF inventing side → WAIT / punish
Size: progressive toward target; size-down near breach
```

---

## sensor_roles

- force: **dual HTF agree** on official set (2 HTFs)  
- ltf_state: pullback | continuation | calibrating via **LTF RSI vs its BBs** relative to Force  
- kill: collapse / risk envelope / no Force  

## reward_sketch

- High process_reward for correct **Force + state** (wait on pullback/calibrating; fire on continuation with Force).  
- Outcome scale optional second; process first.  

## curriculum

1. Name Force + state on synthetic / path packs  
2. Offline curriculum (wait pullback; fire continuation)  
3. Sparse path anchors + re-anchor last (density)  
4. Freeze; 20d then longer dual  
5. Honesty: hits + a13 + breach — not WR vanity  

## positive_windows

- Force long + continuation (RSI above BBs) → fire long  
- Dual HTF agree + continuation  

## negative_windows

- No Force thrash  
- Fire on pullback  
- Fire while calibrating  
- Anti-Force fire  
- Size past risk  

## compliance

- Dual: breach 0, frozen; prefer hits↑ without a13 collapse  
- Language audit: no Load / Reclaim in new Aaron teachings  

## stage_recommendation

**Do this now** — student needs **Force + state** shapes, not answer keys.

## flowchart

```text
         [Both HTFs of set agree? = Force]
           /                    \
         no                     yes
         |                       |
       WAIT              [LTF RSI vs its BBs]
                         /      |        \
              pullback   calibrating   continuation
           (vs Force)                 (with Force)
                |            |              |
              WAIT         WAIT      FIRE side=Force
                                     + progressive size / rails
```

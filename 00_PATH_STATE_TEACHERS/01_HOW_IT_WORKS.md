# How it works

**Simple language.**  
Take it one block at a time.

---

## The big idea (one sentence)

When the bot **waits** but Mark says there **was** a good trade,  
we save **exactly what the bot saw**,  
then train offline: “next time, take Mark’s side.”

---

## Words you will see

| Word | Simple meaning |
|------|----------------|
| **Brain** | The bot’s policy (MetaBrain). Chooses wait / long / short. |
| **State** | All the numbers the brain looks at right now (eyes + goal + risk). |
| **Packed** | The **full** state, saved as one complete vector. Not rebuilt later. |
| **Path** | A real trading day the bot actually walked through. |
| **Brain-wait** | The moment the brain chose **WAIT** (no trade). |
| **Teacher** | The correct answer we store for practice: **long** or **short**. |
| **Mark setup** | A real edge type: pullback resume or continuation. |
| **Offline train** | Practice **after** the day. Not during live prove. |
| **meta_update** | One practice step: show state + teacher → nudge weights. |
| **Champion** | Production brain file we use for real measure / prove. |
| **Shadow** | Practice brain file. Safe. Not production until Court says so. |

---

## The story (like a classroom)

### Step 1 — The bot walks a real day

We run a normal day path with real prices.

The brain looks at its **state** many times.

Each time it can:

- **WAIT**
- **LONG**
- **SHORT**

---

### Step 2 — Sometimes Mark sees a good setup

Mark’s edge says things like:

- **pullback resume** (pullback against force, then resume with the trend)
- **continuation** (trend keeps going)

Those are **good** trade types.

---

### Step 3 — Brain-wait miss

Here is the key moment:

1. Mark says: this is a good long or short.  
2. The brain still says: **WAIT**.  
3. So the bot **missed** a real chance.

We do **not** force a live trade.  
We only **note** the miss for later practice.

---

### Step 4 — Save the packed path-state teacher

We save a small lesson card:

| Field | What it is |
|-------|------------|
| **state** | Exact numbers the brain saw (176 numbers = full eyes) |
| **teacher_act** | Mark’s side: `long` or `short` |
| **topology** | Why it was good: pullback or continuation |
| **session** | Often London / New York (we care more about these) |

**Packed** means:  
we keep the **real** state from that moment.  

We do **not** invent a new fake state later from a short label.

---

### Step 5 — Offline practice

Later (not live):

1. Load the lesson cards.  
2. For each card: show the **state**.  
3. Tell the brain the **teacher** answer.  
4. Run **meta_update** (small weight change).  
5. Repeat many times.

The brain slowly learns:

> “When the world looks like this, fire Mark’s side more often.”

---

### Step 6 — Freeze

After practice, we **freeze** the weights.

At prove / forward:

- Target % can change  
- Risk % can change  
- Weights do **not** retrain  

That is the **no retrain at inference** rule (A14).

---

### Step 7 — Measure, then maybe promote

We run **forward100** (many days).

We check:

- More days with 8–400 trades? (A13)
- Fewer silent (zero-trade) days?
- Still hit target sometimes?
- Risk breach still **0**?

Only if Court is happy do we copy shadow weights into the **champion**.

---

## Why “packed” matters

Two bad ideas we already tried and rejected:

| Bad idea | What went wrong | Court tag |
|----------|-----------------|-----------|
| Fake densify / synthetic states | Thrash on busy days; silent days got **worse** | F-024 |
| Real labels + **rebuilt** fake state | Wrong state vs what the brain really saw | F-025 |

**Good idea (this process):**

Train on the **same** state the brain already used when it waited.

That matches how offline learning works:

> Teach on states you **visited**, not states you invent.

---

## What we keep vs throw away

### Keep (good teacher)

- Full 176-dim state  
- Teacher is long or short  
- Topology is pullback_resume or continuation  
- Source is path_state (real path)  

### Throw away (bad teacher)

- Wrong size state  
- Teacher = wait only  
- Chop / junk topology  
- Synthetic rebuild class  

---

## What this teaches the bot

| Skill | Does this process teach it? |
|-------|-----------------------------|
| “I waited on a real setup — fire next time” | **Yes — main skill** |
| London / NY matter | **Yes** (we weight those more) |
| Hit target more often | **Not much yet** (hits stayed flat) |
| High-trend mastery on all 4 sets | **Not by itself** (see mastery gym) |
| Never blow daily risk | **Rails stay on** (risk envelope) |

---

## What this is NOT

- Not a live “force trade now” switch  
- Not memorizing one chart forever  
- Not copying a coach WAIT answer forever  
- Not the final boss of the whole project  

It is a **road**:  
real misses → real states → offline practice → better density.

---

## Tiny glossary picture

```text
  REAL DAY PATH
       │
       ▼
  Brain sees STATE ──► says WAIT
  Mark sees SETUP  ──► says LONG (or SHORT)
       │
       ▼
  SAVE teacher card:
     state = packed (full)
     answer = Mark side
       │
       ▼
  OFFLINE: meta_update many times
       │
       ▼
  FREEZE → measure → maybe promote champion
```

---

## Related skill gym (human + future train)

For **high trend** principles (force → pullback → resume on all sets):

`evidence_court/meta_rl/game_train/00_HIGH_TREND_MASTERY.html`

That gym is “what skill to master.”  
Path-state teachers are “how we already taught the champ the biggest density jump.”

---

**Next file:** `02_HOW_TO_USE_IT.md`

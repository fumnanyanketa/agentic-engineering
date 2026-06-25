# AtlasOS — Architecture Map

> How the pieces of AtlasOS fit together, and the order you build them in. Pair this with
> [`00-company-brief.md`](00-company-brief.md) (what and why) and
> [`02-roadmap.md`](02-roadmap.md) (which lesson builds which piece).
>
> **Status:** v0.1 scaffold, 2026-06-16. Expect this to change as you learn each layer.

---

## The shape in one diagram

```text
                                  ┌──────────────────────────────┐
            you (founder) ───────▶│   ATLAS  ·  the orchestrator  │
        high-level outcome        │  plan → dispatch → escalate   │
                                  └───────────────┬──────────────┘
                                                  │ routes work + model choice
                  ┌───────────────┬───────────────┼───────────────┬───────────────┐
                  ▼               ▼               ▼               ▼               ▼
              ┌───────┐       ┌───────┐       ┌───────┐       ┌───────┐       ┌───────┐
              │ SCOUT │       │ FORGE │       │ PULSE │       │HERALD │       │WARDEN │
              │research│      │ build │       │analytics│     │ comms │       │review/│
              │       │       │ (code)│       │       │       │report │       │ evals │
              └───┬───┘       └───┬───┘       └───┬───┘       └───┬───┘       └───┬───┘
                  └───────────────┴───────┬───────┴───────────────┴───────────────┘
                                          │ read / write
                              ┌───────────▼───────────┐        ┌───────────────────┐
                              │   CORTEX · memory      │◀──────▶│  TOOLS / MCP layer │
                              │ facts, history, dreams │        │ web, db, APIs, fs  │
                              └───────────┬───────────┘        └───────────────────┘
                                          │
                  ┌───────────────────────┼───────────────────────┐
                  ▼                       ▼                        ▼
          ┌───────────────┐      ┌───────────────┐       ┌───────────────┐
          │  EVALS (M3)   │      │  DEPLOY (M7)  │       │  OPS / OBSERV. │
          │ Warden's tests│      │ cloud + infra │       │ logs, cost, HIL│
          └───────────────┘      └───────────────┘       └───────────────┘
```

Everything below is a layer in that picture. The repo skeleton (`atlas/*/`) has one folder
per layer with its own README and a TODO list you fill in lesson by lesson.

## The layers

### 1. Atlas — the orchestrator (`atlas/orchestrator/`)
The brain that turns an outcome into work. Responsibilities: decompose a goal, choose which
agent handles each part, pick the model per step (the advisor strategy), decide when to ask
you, and loop until the result passes Warden. Starts as a simple Python loop in M4 and grows
into a real planner with a trustworthy workflow (DSL) in M6.

### 2. The agents (`atlas/agents/`)
Specialized workers, each a prompt + tools + (optionally) subagents. Scout, Forge, Pulse,
Herald, Warden. Build the **first one for real in M5** on Claude Managed Agents (start with
Scout), then add others as later modules call for them. M5 also teaches the
tool-vs-skill-vs-subagent decision that decides how each agent is decomposed.

### 3. Cortex — memory (`atlas/memory/`)
What the fleet knows and learns. Short-term working context, long-term stored facts and
history, and the overnight **self-improvement ("dreaming")** loop that distills runs into
better instructions. Built in M5 (agents that remember) and deepened in M6 (memory and
dreaming, learning from your team).

### 4. Tools / MCP layer (`atlas/tools/`)
How agents reach the outside world: web, databases, internal APIs, the file system, and your
own MCP servers. Introduced just-in-time; matters most from M5 onward. Keep tool schemas
lean (tool search, programmatic tool calling) so the context window stays cheap.

### 5. Prompts (`atlas/prompts/`)
The versioned prompt library: each agent's system prompt, the routing/advisor policy, and
reusable snippets. Built in M2 and continuously improved (M6 self-improving prompts). Treat
prompts as code: reviewed, evaluated, versioned.

### 6. Evals (`atlas/evals/`)
Warden's test suite. Graded cases for each agent and for the system end to end, including at
least one deliberately hard case. This is the discipline that makes everything else
trustworthy. Built in M3, then extended whenever you add a capability.

### 7. Deploy (`atlas/deploy/`)
Running AtlasOS on real infrastructure: one chosen cloud (Google Cloud, AWS, or Azure),
routines that fire on a schedule or webhook, and sandboxes for safe execution. Built in M7.

### 8. Ops / observability (`atlas/ops/`)
The operating model and the instrumentation: logs, cost tracking, the human-in-the-loop
interface, and the "how Atlas Group actually runs" playbook from the leadership module (M8).

## Build order (how the layers come online)

```text
M0  workstation ready ........................ tools + accounts (done)
M1  charter + architecture written ........... 00-company-brief.md, 01-architecture.md
M2  prompts/ + routing policy ................ first prompt library, advisor strategy
M3  evals/ ................................... Warden's first graded suite
M4  orchestrator/ (v0 loop) .................. Atlas runs a real task via Claude Code
M5  agents/ + memory/ ........................ first production agent (Scout) that remembers
M6  orchestrator/ + memory/ (deepen) ......... trustworthy workflow + dreaming loop
M7  deploy/ ................................. AtlasOS live on one cloud
M8  ops/ ................................... operating model + rollout playbook
M9  agents/ (vertical) ...................... one flagship vertical agent, proven for real
```

> 🔑 Each layer is shippable on its own. You always have a working (if small) AtlasOS at the
> end of every module, never a half-built thing waiting on the next lesson.

---

*Next: [`02-roadmap.md`](02-roadmap.md) maps every individual lesson to the component its
capstone builds.*

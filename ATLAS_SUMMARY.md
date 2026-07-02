# What Atlas Is — A Working Summary

## The one-liner

**Atlas Group** is a one-founder-plus-agents venture. Its product, **AtlasOS**, is a
self-improving operating system of cooperating AI agents that runs knowledge work end to end:
you hand it an outcome, and a fleet of specialized agents plans, executes, verifies itself,
remembers, and improves over time — on real infrastructure, with a human in the loop for the
decisions that actually need judgment.

It is the north-star project for the *Building with Claude* course: instead of 38 disconnected
toy exercises, every lesson's capstone becomes one real component of this platform. By the end,
you haven't done a course — you've shipped a platform.

## What it's for

The bet is that "the operating system you'd give an AI-native company" is a more valuable thing
to build than any single AI feature. If a prior project (CourseForge) was "an agent that turns a
playlist into a course," AtlasOS is the next order of ambition: CourseForge could eventually run
as *one app on top of* AtlasOS. The platform is the point, not any single pipeline through it.

Concretely, "done enough to be proud of" means:

- You can hand Atlas a high-level outcome (e.g. "keep our competitive intel current," "produce
  this week's business review") and the fleet executes it end to end, unattended.
- Every agent's output is graded by an eval harness, and regressions get caught automatically.
- The system has memory: it remembers context across runs and gets better over time.
- It runs on real cloud infrastructure, is observable, and survives you closing your laptop.
- A human-in-the-loop checkpoint exists for the decisions that genuinely need a person.
- At least one flagship real-world use case ("vertical") is proven, not just simulated.

## The cast — who does what

AtlasOS is a small fleet of named agents, each with a clear job. Naming them is what makes each
lesson's capstone concrete: you're always building, hardening, or connecting one of these seven.

| Agent | Role |
|---|---|
| **Atlas** | The orchestrator. Takes a high-level outcome, breaks it down, dispatches the right agent to each part, and decides when to escalate to the human. |
| **Cortex** | Shared memory. What the fleet knows, learns, and "dreams on" overnight to improve itself. |
| **Scout** | Research and intelligence — web/source gathering, retrieval, synthesis. (First agent shipped for real.) |
| **Forge** | The builder — writes and ships code through Claude Code. |
| **Pulse** | Analytics — turns raw data into insight. |
| **Herald** | Comms and reporting — drafts updates, briefs, the weekly business review. |
| **Warden** | Review, safety, and verification. The eval gatekeeper — nothing ships past Warden without passing its checks. |

## How it's structured (architecture, at a glance)

```
            you (founder) ──▶ ATLAS (orchestrator: plan → dispatch → escalate)
                                      │ routes work + picks the model
              ┌───────────┬──────────┼──────────┬───────────┐
              ▼           ▼          ▼          ▼           ▼
           SCOUT       FORGE      PULSE      HERALD       WARDEN
          research    build/code  analytics  comms       review/evals
              └───────────┴────┬─────┴──────────┴───────────┘
                          CORTEX (memory) ◀──▶ TOOLS / MCP layer
                                │
                  ┌─────────────┼─────────────┐
               EVALS         DEPLOY          OPS
             (Warden's     (cloud +      (logs, cost,
               tests)        infra)      human-in-loop)
```

Each layer lives in its own folder under `atlas/` (`orchestrator/`, `agents/`, `memory/`,
`prompts/`, `evals/`, `tools/`, `deploy/`, `ops/`), and each has a README plus a TODO list filled
in lesson by lesson. Build order runs roughly: charter → prompts/routing → evals → orchestrator
v0 → first production agent + memory → deepen orchestrator/memory → deploy to real cloud →
operating model → one flagship vertical proven for real.

## Design principles it's held to

1. **Build for the next model, not today's** — keep scaffolding thin, trim guardrails as models
   improve.
2. **Evals harder than the model** — if the test suite is too easy, you can't tell a better model
   from a worse one.
3. **Primitives compose** — small pieces (routines, sandboxes, tools, memory, routing policy)
   snapped together, not one giant feature.
4. **Cost per successful outcome, not cost per token** — cheap models execute; the expensive
   model advises only when needed.
5. **Outcomes over tasks** — the unit of work is "own this result over time," not "do this once."
6. **Verification is the bottleneck** — as building gets cheap, checking is the scarce skill;
   Warden is first-class, not an afterthought.

## What it's explicitly *not* trying to be

- Not a polished consumer SaaS with billing and a marketing site — it's a platform and a
  portfolio, built in public.
- Not seven perfect agents for their own sake — one excellent agent plus a real orchestrator
  beats five shallow demos.
- Not provider lock-in — durable disciplines (prompting, evals, context engineering, agent
  design, verification) matter more than any specific model id.

## If it stops fitting

The brief itself says the specific build can change — swap AtlasOS for any single real platform
worth caring about (a research org's agent fleet, a trading-signal platform, a support org's
agent stack) and keep the same component map. What must *not* happen is drifting back to 38
disconnected exercises with no through-line.

---
*Source: `atlas/00-company-brief.md`, `atlas/01-architecture.md`, `atlas/02-roadmap.md`,
`atlas/README.md` in this repo.*

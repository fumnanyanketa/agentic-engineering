# Module 5 · Lesson 18: Memory and Dreaming for Self-Learning Agents

> **Course:** Building with Claude, a self-paced course
> **Module 5:** Building agents, Claude Managed Agents
> **Speaker:** Ravi, API Knowledge team, Platform, Anthropic
> **Source talk:** [Memory and dreaming for self learning agents](https://www.youtube.com/watch?v=IGo225tfF2I) · [full transcript](../../transcripts/code-with-claude-2026-london-2026/11_memory-and-dreaming-for-self-learning-agents.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

Agents get more useful when they can learn from one task to the next, so this lesson explains how Anthropic designed **memory** (a shared, file-based store that lets agents carry learnings across sessions, agents, and environments) and **dreaming** (a separate background process that fact-checks, organises, and enriches that memory so it improves globally, not just locally).

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you build **OnCallBrain**, an incident-response agent that shares an organisation-wide memory and improves itself through nightly dreaming. The teaching before the Capstone gives you the design vocabulary you will need. To see the finish line first, jump to **"Capstone Project: OnCallBrain"** and then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442)** (paper). Its memory-stream plus "reflection" architecture (periodically synthesizing raw experiences into consolidated memories) is the seminal analogue of "dreaming."
> - **[Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)** (paper). Agents that improve by reflecting on past feedback in episodic memory, with no weight updates, the continual-learning idea behind self-improving agents.

## A few plain-language basics first

This lesson is more about *design* than commands, so here are the terms in plain words:

- **Agent:** an AI that takes actions toward a goal on its own (calling tools, reading files, deciding next steps), rather than answering in one shot.
- **Session:** one run of an agent, usually a single task or conversation.
- **Context window:** the amount of text the model can "hold in mind" at once during a single run. It is limited, which is why long tasks need memory outside the window.
- **Long horizon task:** a task that takes a long time and many steps (sometimes hours or days). These are exactly where keeping track of information gets hard.
- **Memory store:** a persistent place, modelled as files, that agents read from and write to so knowledge survives after a session ends.
- **Scope:** who can use a store and how. **Read-only** means an agent can read but not change it; **read-write** means it can do both.
- **CRUD:** the four basic data operations: Create, Read, Update, Delete. A "CRUD API" lets you manage stored data programmatically.
- **Out of band:** happening separately from the main flow, in the background, not in the live path of the agent doing its task. ("Hot path" is the opposite: the time-critical live flow.)
- **Dreaming:** a background batch process that reviews session transcripts and existing memory, then proposes a cleaner, better-organised, verified version of that memory.
- **Test time compute:** letting a model spend extra work (tokens) at the moment it solves a problem, which on average produces better answers. Dreaming applies the same idea to memory.

You do not need to memorise these. Each is explained again the first time it appears.

## Why this lesson matters

Models keep getting better at long, complex tasks. Ravi cites a 2025 METER study finding that the length of tasks agents can complete is **doubling roughly every seven months**. But managing information over those long horizons is still hard. As Ravi puts it, memory "lets agents learn" and "carry forward learnings from their previous tasks."

The payoff is concrete. Anthropic built memory with partner teams and reported real results: Rakuten saw a **97% decrease in first-pass errors** in production agents, WiseDocs reduced common issues with cross-session memory in a document-verification pipeline, and Harvey saw a **six-times increase in completion rates** on a legal benchmark after adding dreaming. The common feedback: the memory primitive lets teams focus on building the product, not the infrastructure.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain the goal of memory: performance that **improves from task to task** instead of starting from the same blank slate every time.
2. Describe why memory is modelled as a **file system** and what "let it cook" means as a design principle.
3. Lay out the three components of a memory architecture: the **storage layer**, the **structure** of memory, and **Claude-driven processing**.
4. Explain the multi-agent requirements memory must meet: shared stores, read-only and read-write **scopes**, **optimistic concurrency control**, versioning, attribution, and a standalone API.
5. Explain **dreaming**: what it does, why running it **out of band** matters, and how it makes memory **globally** optimal rather than only **locally** optimal.

## Prerequisites

- Module 5 · Lesson 17 (Agents That Remember) is the practical, hands-on companion to this design-focused lesson. Either order works, but they pair well.
- Familiarity with the idea of an agent calling tools and running across multiple sessions.

---

## Part 1: why memory, the learning curve

Picture a series of tasks: task one, task two, task three, and so on. The question is simple: does the agent get *better* as it goes?

```text
Without memory                With memory
performance                   performance
  |                             |          ___---
  |  ___  ___  ___              |     ___---
  | |   ||   ||   |             | ___-
  | | 1 || 2 || 3 |             |-
  +-----------------            +-----------------
   task1 task2 task3             task1 task2 task3
   (each starts cold)           (each builds on the last)
```

In the base case, every task performs about the same, because each agent starts from the same blank slate. In the optimal case, performance climbs from task one to two to three. As Ravi frames it, that climb is the goal: "learning from task to task, but also from environment to environment, and agent to agent."

What can agents learn this way?

- **Common strategies and previous mistakes**, so they stop repeating errors.
- **The tools, code bases, and files** they have access to.
- **Each other's learnings**, transferred between agents. Ravi describes the vision as "swarms of agents contributing to and maintaining a shared understanding of the organization they work in."

> 🔑 **Key idea: memory turns a flat line into a learning curve.** Without it, every run is independent and quality plateaus. With it, each run can stand on the shoulders of the last, across tasks, environments, and agents.

---

## Part 2: designing memory as a file system

Memory is not a new idea, but the approach evolved. Earlier attempts built memory into the **harness** (the code wrapping the model), like `CLAUDE.md` for Claude Code or dedicated memory tools in the SDKs. The newer insight, the same one behind **skills**, is that as models improve you often want to **get out of Claude's way** and give it a simple, flexible format it already understands. (A **skill** is a lightweight, flexible format that bolts a new capability onto the model.)

So memory is modelled as a **file system**, because of what current models are already great at:

- Navigating virtual environments and file systems.
- Using familiar tools like **bash** and **grep** to read, update, and organise files.
- **Opus 4.7** in particular is described as state-of-the-art at file-system-based memory, increasingly good at discerning which context is worth saving for its future self, and how to structure it.

> 🔑 **Key principle: "let it cook."** Rather than building elaborate machinery around the model, give it a file system and let it use the strong capabilities it already has. The simple, flexible format does the heavy lifting, just as it did for skills.

---

## Part 3: making memory work for many agents at once

A single agent with a file system is the easy case. Production means **multiple agents** operating in the same environment, or across environments, at the same time. That raises new requirements.

### Shared stores with scopes

Multiple sessions can share the same store at once, and they may need different access levels. **Scope** is who can use a store and how:

| Scope | Meaning | Example |
|---|---|---|
| **Read-only** | Agents can read but not change it. | Organisation-wide memory updated infrequently, readable by all agents. |
| **Read-write** | Agents can both read and write freely. | A granular, task-specific store the same agents own. |

This creates a **hierarchy**: a stable org-wide layer everyone reads, plus narrower stores agents freely update. That lets the memory system scale.

### Avoiding clobbering: optimistic concurrency control

When several agents write at once, one could overwrite another's changes (called **clobbering**). Memory uses **optimistic concurrency control**, a technique that assumes conflicts are rare and detects them at write time so an agent does not silently destroy another agent's update.

> 💡 "Optimistic" here means the system lets agents work freely and only steps in if two writes actually collide, rather than locking everything up front. It keeps many agents productive while still protecting their changes.

### Enterprise-grade controls

Real production memory needs governance:

- **Version control** creates an **audit trail** so developers see how memory evolved and can **diff** between versions.
- **Attribution** shows which agent wrote which part of the memory.
- A **standalone API** lets teams manage memory from anywhere, with standard **CRUD** operations plus enterprise operations like **exports** and **redactions** (removing sensitive content).

> 🔑 **Key idea: memory has its own API, decoupled from any single agent.** Teams build in many different environments, so memory must be manageable from outside the agent loop, not locked inside it.

---

## Part 4: three components of a memory architecture

Ravi sums the design up as three layers:

| Component | What it handles | Plain-language meaning |
|---|---|---|
| **Storage layer** | How data is managed and how changes are tracked. | The filing cabinet plus its change log. |
| **Structure of memory** | Organising memory in a format Claude gets the most out of. | Arranging the files so the model can find and use them. |
| **Claude-driven processing** | The model updating memory as it works. | The agent taking notes while it does its job. |

That third one, processing, is where the next problem appears.

---

## Part 5: the problem with notes-while-you-work

Having agents write memory as they go is like taking notes during a task. It works well for one agent. But scaled up to complex multi-agent use cases, patterns emerged:

- Agents made **many of the same mistakes**, each learning from them independently.
- Agents showed the **same inefficiencies** over and over.
- Memory was updated in a **locally optimal** way but not a **globally optimal** one. ("Locally optimal" means good for one agent in the moment; "globally optimal" means good for the whole system.)
- The result was **duplication** and **fragmentation** across stores.

> 🔑 **Key idea: notes-while-you-work is locally smart but globally messy.** A single agent cannot see the patterns spread across many agents and sessions. Something has to look across all of them.

---

## Part 6: dreaming, the global feedback loop

The fix is **dreaming**, available in research preview and usable with Claude Managed Agents. Dreaming is a **batch process** that runs **out of band** from sessions, completely decoupled from the agent loop. Think of it as a feedback loop: agents write memories, dreaming refines them, and the cycle repeats.

How a dream run works:

- It can be triggered **ad hoc, nightly, hourly, or by events** (like the end of a session), all via API, so it is flexible.
- Each run **analyses session transcripts** and **inspects the existing memory** state.
- It **proposes optimisations** where sessions were inefficient, made mistakes, or needed better guidance.
- The output is a **verified, better-organised snapshot** of memories that agents can choose to adopt.

### Why out of band matters

Keeping dreaming decoupled from the agent loop has clear benefits:

- **It works for multi-agent systems.** Looking across cross-session, cross-agent transcripts reveals patterns a single isolated agent would struggle to spot.
- **It has clean objectives.** Because dreaming is independent, agents never have to trade off between improving memory quality and finishing their actual task. As Ravi puts it, "it's clean separation."
- **It adds no latency.** Dreaming is completely off the **hot path**, so it never slows the live agent down.

Like Lesson 17's demo, this dreaming harness is itself **built on Claude Managed Agents**: a feature for managed agents, built on managed agents. It spins off a series of **sub-agents** to analyse transcripts in parallel, with the same observability as the rest of the platform.

> 🔑 **Key idea: dreaming is test-time compute for memory.** Just as a thinking model spends extra tokens to explore a problem and on average gets a better answer, dreaming spends work up front to curate higher-quality memory, and that pays dividends for every downstream agent.

> 💡 **The mental model:** memory helps agents learn from task to task; dreaming verifies, organises, and enriches that memory. Ravi calls dreaming "the bridge between memory as we know it today and organization-scale memory and knowledge."

---

## Part 7: a worked example, agents on call

Ravi demonstrates an agent platform for **SREs** (Site Reliability Engineers, the people who keep production systems running). It watches incoming alerts and pages and, for some, spins up agents to triage and fix issues.

The setup uses two kinds of store:

```text
┌────────────────────────────┐      ┌────────────────────────────┐
│ READ-ONLY org-wide store    │      │ READ-WRITE task store       │
│ - SLO policy                │      │ - findings for THIS alert   │
│ - runbooks                  │      │ - "fix in flight, incoming" │
│ - on-call mappings          │      │                             │
│ (changes rarely)            │      │ (updated live by agents)    │
└────────────────────────────┘      └────────────────────────────┘
        ▲ all agents read                 ▲ shared across sessions
```

(An **SLO** is a Service Level Objective, a reliability target. A **runbook** is a step-by-step guide for handling a known problem.)

The cross-session payoff: one agent investigates an alert, finds the root cause, puts up a fix, and **notes in memory that a fix is in flight**. When a similar issue arises later, a downstream session **reads that note** and acts on it instead of duplicating the work. As Ravi says, "it's really cross-session memory at work."

Then he kicks off a dream over the **team SRE store** and a batch of about five sessions from the last seven days. The dream session spins off sub-agents to analyse transcripts in parallel, and the finished diff shows a real insight:

> Across sessions and agents, an alert kept firing **60 seconds after a CPU spike**, a recurring pattern that hinted at a retry-behaviour issue.

Dreaming makes a note of this pattern and updates memory so the **next** agent that sees it can act, and it rewrites the triage log into something holistic rather than a rote list of events. That is exactly a global pattern no single agent in isolation would have caught.

---

## Part 8: the full picture

Pulling it together:

```text
   MEMORY                                   DREAMING
   learn + remember task to task   <----->  verify, organise, enrich
   shared across agents/envs                globally reconcile across agents
   raises the floor for every agent         raises the floor even higher
```

A robust memory layer shared across agents and environments raises the floor for every agent. Dreaming, by globally reconciling memory, raises it further. Explode that to full scale and, in Ravi's words, "memory becomes a huge source of knowledge that Claude can use to understand the organization and the world it's operating in."

> 🎯 **Why this is the year for it.** Agents will run for longer and longer time scales (days, even), continuously building on their understanding of the world around them. Memory systems are a big part of what makes that possible.

---

## Key takeaways

1. **Memory turns a flat line into a learning curve.** The goal is performance that improves from task to task, environment to environment, and agent to agent.
2. **Memory is a file system on purpose.** Get out of the model's way and let it use bash, grep, and file skills it already has. "Let it cook."
3. **Multi-agent memory needs real structure:** shared stores, read-only and read-write scopes forming a hierarchy, optimistic concurrency control, versioning, attribution, and a standalone API.
4. **Notes-while-you-work is locally optimal but globally messy:** repeated mistakes, duplication, fragmentation.
5. **Dreaming closes the loop globally.** A batch, out-of-band, multi-agent process that fact-checks, organises, and enriches memory with no latency on the agent.
6. **Dreaming is test-time compute for memory.** Spend work up front to curate better memory, and every downstream agent benefits.

## Common pitfalls

- ❌ Treating memory as a dumping ground and never reconciling it (you get duplication and stale facts).
- ❌ Running refinement inside the agent loop, forcing a trade-off between task quality and memory quality, and adding latency.
- ❌ Giving every agent read-write access when an org-wide store should be read-only.
- ❌ Ignoring concurrency, so parallel agents clobber each other's writes.
- ❌ Skipping versioning and attribution, so you cannot audit how memory evolved or who wrote what.
- ❌ Expecting one isolated agent to spot patterns that only appear across many sessions.

---

## 🛠️ Capstone Project: OnCallBrain

> This is the main hands-on project for the lesson. You will recreate the SRE example's *shape* on your own domain: a multi-session agent that shares an org-wide read-only memory plus task-specific read-write memory, and improves itself through dreaming. Start tiny and grow it.

### What you will build

**OnCallBrain** is an incident-response agent (real or simulated) that:

1. Reads stable org knowledge from a **read-only** store and writes findings to a **read-write** task store.
2. Carries a "fix in flight" note from one session to a later session that hits a similar issue.
3. Runs **dreaming** over a batch of past sessions to surface a cross-session pattern and update memory globally.

> 🎯 **Pick your world.** Real SRE alerts if you have them, or simulate any recurring-incident domain: a help desk with repeat tickets, a content-moderation queue, or a home-lab monitoring setup. You just need (a) stable knowledge that rarely changes and (b) recurring issues that benefit from cross-session learning.

### Why this is the perfect practice

| Lesson concept | Where you use it in OnCallBrain |
|---|---|
| Read-only versus read-write scopes | Milestone 1, two stores |
| Cross-session memory | Milestone 2, the "fix in flight" handoff |
| Optimistic concurrency | Milestone 3, two agents writing at once |
| Versioning, attribution, diffs | Milestone 4, the audit trail |
| Dreaming out of band | Milestone 5, the nightly job |
| Globally optimal vs locally optimal | Milestone 6, the cross-session pattern |
| Test-time-compute mental model | Milestone 6, measuring the lift |

### Milestones (build them in order, each one works on its own)

1. **Two stores.** Create a **read-only** org-knowledge store (policies, runbooks) and a **read-write** task store. Confirm an agent can read the first but not modify it.
2. **The handoff.** In one session, have the agent investigate an issue, decide on a fix, and write "fix in flight" to the task store. In a later session on a similar issue, confirm it reads that note and acts on it.
3. **Concurrency.** Run two sessions that both try to update the same file at once. Show that optimistic concurrency control prevents one from silently clobbering the other.
4. **Audit trail.** Make several edits, then use version history to diff two versions and confirm each change is attributed to the session that made it.
5. **Dream.** Run several incident sessions to fill memory, then kick off a dream over a batch of them (nightly or ad hoc). Open the dream session and watch its sub-agents analyse transcripts in parallel.
6. **Find the pattern.** From the dream diff, identify at least one cross-session pattern no single session could have seen (like "alert fires 60s after a CPU spike"). Confirm memory now guides the next agent. Note tokens spent and the lift in a fresh session.

### How you will know you are done

- ✅ A later session correctly reacts to a "fix in flight" note written by an **earlier** session.
- ✅ Your read-only store cannot be edited by an agent, and concurrent writes to the task store do not clobber.
- ✅ You can diff two memory versions and say which session authored each change.
- ✅ A dream produces a verified, reorganised snapshot that surfaces a **cross-session** insight, and a new session visibly benefits from it.

> 💡 **Keep yourself honest:** the whole point is *global* improvement. If your dream only re-states what a single session already knew, give it more varied transcripts so it can find a real cross-session pattern.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each focused on one idea. Optional and independent. The **Capstone above is the main build** and covers all of these together.

### Exercise 1: draw the learning curve (foundational)
Run the same task three times with and without a memory store. Plot or describe performance across the three runs and explain the difference in your own words.

### Exercise 2: design a scope hierarchy (foundational)
For a domain you know, list which knowledge belongs in a read-only org store versus a read-write task store. Justify each placement.

### Exercise 3: provoke a write conflict (intermediate)
Have two sessions edit the same memory file at nearly the same time. Describe what optimistic concurrency control does and why it beats locking everything.

### Exercise 4: trigger dreaming three ways (intermediate)
Configure dreaming to run ad hoc, on a schedule, and on a session-end event. Compare when each makes sense for a real workload.

### Exercise 5: measure the dividend (advanced)
Treat dreaming as test-time compute. Record the tokens a dream spends, then measure how much faster or more accurate downstream sessions become. Is the up-front cost worth the downstream lift for your use case?

---

## Cheat sheet

```text
WHY MEMORY
  Goal: performance improves task -> task, env -> env, agent -> agent.
  Learn: strategies, past mistakes, tools/code, and each other's learnings.

DESIGN
  Model memory as a FILE SYSTEM. Let it cook (bash, grep, file edits).
  Three components: storage layer | structure | Claude-driven processing.

MULTI-AGENT REQUIREMENTS
  shared stores + scopes (read-only org / read-write task) -> hierarchy
  optimistic concurrency control -> no clobbering
  versioning + attribution + diffs -> audit trail
  standalone API -> CRUD + exports + redactions

DREAMING
  batch, OUT OF BAND, decoupled from the agent loop.
  trigger: ad hoc / nightly / hourly / on session end (via API).
  reads transcripts + memory -> proposes verified, organised snapshot.
  multi-agent harness, built on Managed Agents itself.
  makes memory GLOBALLY optimal, not just locally. No latency on agents.

MENTAL MODEL
  dreaming = test-time compute for memory.
  memory raises the floor; dreaming raises it higher.
```

## How this connects to the rest of the course

- **Companion, Module 5 · Lesson 17 (Agents That Remember):** the practical CLI-and-console walkthrough of the exact features designed here.
- **Earlier, Module 2 · Lesson 3 (The Prompting Playbook):** the generate, evaluate, repair loop is the small-scale ancestor of dreaming's refine-then-repeat loop.
- **Next, Module 5 · Lesson 19 (Agent Battle):** tuning an agent's configuration (prompt, model, tools, skills) and hill-climbing on evals, the skills you would use to improve a memory-and-dreaming system over time.

---

*Source: "Memory and dreaming for self learning agents" by Ravi (Anthropic), Code with Claude 2026, London. Diagrams and structured summaries are illustrative reconstructions of the concepts described in the talk; the customer results and study figures are as stated by the speaker.*

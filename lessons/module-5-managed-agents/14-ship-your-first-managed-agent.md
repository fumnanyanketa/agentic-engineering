# Module 5 · Lesson 14: Ship Your First Managed Agent

> **Course:** Building with Claude, a self-paced course
> **Module 5:** Building agents, Claude Managed Agents
> **Speaker:** Isabella He, Member of Technical Staff, Applied AI team, Anthropic
> **Source talk:** [Ship your first Managed Agent](https://www.youtube.com/watch?v=19HDQ9HppOA) · [full transcript](../../transcripts/code-with-claude-2026-london-2026-day-2/01_ship-your-first-managed-agent.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

You can build a real, production-ready agent (here, one that wakes up at 3am to debug a software incident for you) by composing three simple pieces (an agent definition, an environment, and a session) on top of Claude Managed Agents, which runs the agent loop server-side and hands you durability, scaling, and observability for free.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you build **NightShift**, an on-call incident-response agent that investigates a failing service and reports the root cause, so you never get woken at 3am again. Everything before the Capstone teaches the pieces you will snap together there. If you want to see the finish line first, jump to the **"Capstone Project: build NightShift"** section near the end, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[Tool use with Claude (Anthropic docs)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)** (docs). The tool-agnostic explanation of the function-calling / agentic loop (model decides, your app executes, result returns) that underpins any agent you build.
> - **[Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761)** (paper). The seminal paper on why and how language models call external tools and APIs.

## A few plain-language basics first

This lesson uses some everyday AI terms. Here they are in simple words:

- **LLM (Large Language Model):** the kind of AI that reads and writes text. "Claude" is an LLM.
- **Model:** one specific version of that AI, for example "Opus 4.7" or "Sonnet 4.5." Newer models are smarter.
- **Token:** the unit the model reads and writes in, roughly three quarters of a word. Older APIs charge "tokens in, tokens out."
- **Agent:** an AI that takes actions on its own toward a goal (using tools, running code) rather than answering in one shot.
- **Agent loop:** the repeating cycle where the agent thinks, calls a tool, reads the result, thinks again, and so on, until the task is done.
- **Tool:** a small piece of code the agent can choose to run, for example to fetch logs or read metrics.
- **Harness:** all the code and machinery around the model: the agent loop, context handling, tool calling. The model is the brain; the harness is everything else.
- **Context window:** the limited amount of text a model can hold and reason over at one time.
- **Sandbox / container:** a safe, isolated computer where the agent can run code without touching your real systems.
- **Session:** one ongoing run of an agent, like one chat or one investigation.
- **SRE (Site Reliability Engineering):** the practice of keeping software services running reliably. An **incident** is when a service breaks or degrades and someone has to fix it fast.

Every term is also explained again the first time it appears below.

## Why this lesson matters

If you have ever been **on call** (responsible for fixing software outages around the clock), you know the pain Isabella describes: getting woken at 2 or 3am to dig through metrics, logs, and recent deployments while half asleep. That investigation is exactly the kind of multi-step, tool-using work an agent is now good at. But building such an agent the old way meant writing your own agent loop, hosting it, scaling it, and securing it. Managed agents removes that burden so you can ship the useful part in an afternoon. Isabella's goal is simple: get you hands-on and "ready to actually ship your first incident response" agent.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain the path from the raw **Messages API** to the **Agent SDK** to **Claude Managed Agents**, and what each layer takes off your plate.
2. Build an agent from three composable pieces: an **agent definition**, an **environment**, and a **session**.
3. Explain why managed agents speaks in **events** instead of "tokens in, tokens out," and why that matters for reliability and observability.
4. Describe the key design decision of **decoupling the brain from the hands** and the concrete benefits (security and latency).
5. Wire up **local tools**, **session persistence**, **state management**, and **session deletion**.
6. Name the next-level features: **subagents**, **memory**, **dreaming**, **outcomes**, and **vaults**.

## Prerequisites

- Module 5 · Lesson 13 (Get to production faster): the three building blocks and the event stream are introduced there.
- Module 2 (Core skills): you know what a prompt, a tool, and a model are.

---

## Part 1: how we got here (Messages API to Agent SDK to managed agents)

Isabella traces three generations of building on Claude. Each one took more work off the developer.

| Layer | What it gave you | What you still had to do yourself |
|---|---|---|
| **Messages API** (2023) | Raw model access: tokens in, tokens out. | Build every primitive yourself: context management, the agent loop, **compaction** (shrinking old context so it fits), and more. |
| **Agent SDK** | A harness that programmatically drives Claude Code (an agent with access to a computer and a file system), making Claude far more powerful. | Manage **hosting** and **scaling** yourself, and make it safe to run in your own containers. |
| **Claude Managed Agents** | The first harness where Anthropic handles scaling and production components: a purpose-built harness, sandboxing, observability, and tool runtime, all inside managed infrastructure. | Just the **task and agent configuration** and your **custom tool logic**, the parts that bring your domain expertise. |

> 🔑 **The point of each layer:** push more of the boring, error-prone infrastructure onto Anthropic so you can focus on the part only you can do, your agent's job and your tools. Isabella notes teams have shipped "10 to 15 times faster to production" with managed agents.

### Why a harness needs to keep evolving

Isabella gives a vivid example. With Sonnet 4.5, Claude showed a behaviour they called **context anxiety**: it wrapped up tasks early even when it had plenty of room left in its context window. They added mitigations in the harness to fight that early-stopping. Then Opus 4.5 came out and the behaviour simply vanished, making all that harness work obsolete.

> 💡 **The lesson:** keeping a harness in sync with each new model is a lot of ongoing work. Letting Anthropic own compaction, caching, and quirks like context anxiety means you inherit those fixes (and their removal) automatically.

## Part 2: the three pieces you compose

Three primary resources go into a managed agent. Isabella frames them as the brain, the hands, and the thread that ties them together.

| Resource | Role | What it holds |
|---|---|---|
| **Agent** | The **brain**: persona and capabilities. | The system prompt, the model, the MCP servers, the skills, the tools the agent can use. |
| **Environment** | The **hands**: a place to take action. | A container the agent acts in, with networking rules and packages. |
| **Session** | The **connection** between brain and hands. | Spins up an agent instance inside an environment, streams events back to your user. |

> 🔑 **Key idea: the agent loop runs server-side.** This is the heart of why managed agents is reliable. When you close your laptop or hit hard refresh, "everything is maintained." You do not worry about **durability** (the work surviving crashes) or **reliability**. The state lives in the cloud, not on your machine.

(A **system prompt** is the standing instructions that define who the agent is. An **MCP server** is a service that offers tools over a shared standard called the Model Context Protocol. A **skill** is packaged knowledge or procedures Claude can pull in when needed.)

## Part 3: the key design decision, decoupling the brain from the hands

Older harnesses tightly coupled the **agent loop** with **tool execution**: the thinking and the doing happened in the same box. That makes sense for some agents (Claude Code needs direct access to your files). But managed agents lets you **decouple** the two: the brain runs in one place, the hands (the sandbox where tools execute) in another.

Why bother? Two big wins:

- **Security.** Because the agent's loop is separated from the sandbox, the agent cannot directly read raw credentials. They can be encrypted and isolated. You get much stronger sandboxing.
- **Latency.** With the old coupled design you had to spin up a fresh container for every session, which added startup delay. Decoupled, Isabella's team saw a reduction in **time to first token** (how long until the agent produces its first word) "along the lines of over 90% reduction in TTFT for our P95 metrics." (**P95** means the 95th percentile: the experience of all but the slowest 5% of requests. So even the slow cases got dramatically faster.)

> 🔑 **Decoupling the brain from the hands buys you safety, reliability, and speed at once.** If a container goes down, you just spin a new one up; you do not have to restart the whole agent loop. This is the architectural idea behind several later features, including secure **vaults**.

## Part 4: the build, an incident-response agent

The workshop builds an **SRE agent** (Site Reliability Engineering agent) that debugs an incident. Picture P99 latency suddenly running 10x above normal. (**P99 latency** is the response time experienced by all but the slowest 1% of requests, a common health metric. "10x the baseline" means the service is badly degraded.) A human would dive into metrics, logs, and recent deployments. The agent will do exactly that.

The build copies pieces from a completed file onto an empty one, one at a time, so you see each primitive add capability. Below is an illustrative reconstruction of those steps.

### Step 1: define the agent

```python
# The agent is the brain: model + system prompt + tools.
sre_agent = client.beta.agents.create(
    model="claude-opus-4-7",
    system_prompt=(
        "You are an SRE agent. You are responsible for coming in and debugging "
        "incidents. You have access to tools for metrics, recent deployments, "
        "diffs, and logs."
    ),
    tools=[get_metrics, get_recent_deploys, get_diff, get_logs],
)
```

> 💡 Isabella points out the system prompt is "extremely simple." You can add constraints later, but a short, clear prompt works well. The tools mirror what a human on-call engineer would reach for: metrics, recent deploys, diffs, logs.

### Step 2: define the environment

```python
# The environment is the hands: where the agent runs.
sre_environment = client.beta.environments.create(
    compute="anthropic",                 # or bring your own container
    network_allow_list=["*"],            # unrestricted here; tighten in production
)
```

The network list is an **allow-list**: the only places the agent may reach. The demo allows everything for simplicity, but you can restrict it to specific sites. (Managed agents also offers **MCP tunnels** to reach private MCP servers without exposing them on the public internet.)

### Step 3: give it data (the files API)

```python
# Upload the incident's logs as a file the agent can process.
log_file = client.beta.files.upload(file=open("incident_logs.json", "rb"))
```

The agent reads and runs code over these files. Isabella stresses this: "as much data as you're able to give the agent... is what makes it so powerful." Managing what context and files the agent gets, called **context engineering**, is where developers spend most of their time.

### Step 4: create the session and stream events

```python
# The session binds agent + environment and mounts the data.
session = client.beta.sessions.create(
    agent_id=sre_agent.id,
    environment_id=sre_environment.id,
    resources=[log_file.id],
)

# Stream the agent's work back as events, not one big final blob.
for event in client.beta.sessions.stream(session.id):
    render(event)   # show tool calls and responses as they happen
```

> 🔑 **Sessions speak in events, not "tokens in, tokens out."** An **event** is a single recorded thing: a user message, a tool call, an agent response. Each event is appended to the session log. This matters two ways: the **user** sees the agent working in real time (better experience), and you get full **observability** (every step is logged in the console).

### Step 5: wire up the local tools

The agent is defined server-side, but it cannot actually fetch metrics until you connect the **local tools**, the code that runs on your side when the agent calls `get_metrics`, `get_recent_deploys`, `get_diff`. Once connected, the agent truly takes action. In the demo it runs a sandbox bash command, inspects logs, calls `get_recent_deploys`, and streams everything live.

```python
# Local tool implementations run on YOUR side; the agent loop runs server-side.
def get_metrics(service):
    return read_json("metrics.json")          # later: a Datadog client, etc.

def get_recent_deploys(service):
    return read_json("deploys.json")
```

> 💡 **Why this is powerful for production.** Because tool execution is separate from the agent loop, you can swap `read_json` for a real **Datadog** client (a production monitoring service) using the same wire protocol. What is local in the demo "can be something that's easily movable into infrastructure."

### Step 6: session deletion (a security feature)

```python
client.beta.sessions.delete(session.id)   # removes it from every log too
```

Deleting a session removes it from every log, so you actively control what data is retained. This is a security lever, not just tidiness.

### The result

The agent investigates and reports a clear root cause: a **database pool exhaustion** caused by a commit from "Alice" that refactored the order-summary builder and introduced a query that drained the connection pool. It rules out other causes and recommends fixes. In a fuller version you could give it Claude Code and let it open a PR with the fix, turning you into the **oversight**, not the manual fixer.

## Part 5: what you actually learned (the under-the-hood recap)

| Concept | Why it matters |
|---|---|
| **Events, not request/response** | Events are appended to the session log, so a session is easy to resume and easy to inspect. If a container dies, you spin a new one up without restarting the loop. |
| **Local tools, decoupled execution** | Your tools ran on your laptop; the agent loop ran in Anthropic's cloud. Swap a JSON file for Datadog with the same protocol. |
| **Streaming to the user** | Events surface in your UI as they happen, so users see progress, not silence. |
| **Session state** | Sessions move through states: **idle → running → rescheduling** (retrying) **→ terminated** (on failure). State enables retries, resumability, and reacting to **webhooks**. |
| **Session persistence** | Hard-refresh the page and every past session is still there. No database to wire up. |

> 🔑 **Session state is a power feature, not just bookkeeping.** A **webhook** (an automatic message a service sends when something happens) can arrive and the agent can **resume** a session or kick off a specific state in response. So your agent can react to real-world events, not just to you typing.

## Part 6: beyond the basics

Isabella's build used only the simplest primitives, yet already replaced hours of production setup. To go further, managed agents offers these out of the box:

| Feature | What it does |
|---|---|
| **Subagents (multi-agents)** | An orchestrator agent spins up other agents, each with its own context window, to handle subtasks in parallel and report back. Great for parallelisation and context management. |
| **Memory** | Long-lived stores so agents remember user preferences and corrections across sessions: self-improving agents. |
| **Dreaming** | Claude reviews its own memory logs and decides what to keep, so it accurately remembers what matters. |
| **Outcomes** | You define a **rubric** of the result you want; the agent figures out which tool calls get it there and iterates until it satisfies the rubric. |
| **Vaults** | Encrypted credential storage. Credentials live on a separate endpoint; the agent uses them without ever seeing them. This relies on the brain/hands separation from Part 3. |

There are also **webhooks**, **fine-grained permission policies**, **MCP server controls**, and a **console agent builder** with a built-in observability dashboard.

> 💡 For an SRE agent specifically, Isabella suggests adding a **runbook skill**. A **runbook** is the documented steps a team uses to debug a known incident. Give the agent access to runbooks and past **postmortems** (write-ups of what went wrong and why) and it learns to work within your systems.

---

## Key takeaways

1. **Three pieces compose an agent:** the **agent** (brain), the **environment** (hands), and the **session** (the connection that streams events).
2. **The agent loop runs server-side.** Close your laptop, hard-refresh, lose a container, and the work survives. No database to manage.
3. **Sessions speak in events.** Events are appended to a durable log, giving you resumability and full observability.
4. **Decouple the brain from the hands** for security (credentials stay isolated) and latency (over 90% faster time-to-first-token in their P95).
5. **Local tools keep execution on your side.** Start with a JSON file, swap in Datadog later using the same protocol.
6. **Context engineering is the real work.** Give the agent the right data and files; that is where you spend your time.
7. **Grow with primitives:** subagents, memory, dreaming, outcomes, and vaults are there when you need them.

## Common pitfalls

- ❌ Storing session state on your laptop, then losing it on refresh. Let the server own durability.
- ❌ Over-engineering the system prompt. A short, clear one often works.
- ❌ Forgetting to wire up local tools, so the agent is "defined" but cannot actually act.
- ❌ Leaving the network allow-list wide open in production.
- ❌ Never deleting sessions, so data piles up you did not mean to retain.
- ❌ Hard-coding credentials in your tools instead of using vaults.

---

## 🛠️ Capstone Project: build NightShift

> This is the main hands on project for the lesson. You are building the very thing Isabella built in the workshop: an on-call incident-response agent. Start tiny (one script, fake JSON data) and grow it toward something you could point at real monitoring.

### What you will build

**NightShift** is an SRE agent that, when an incident fires, investigates metrics, recent deployments, code diffs, and logs, then reports a clear root cause and recommended fixes, all streamed live so you can watch it work.

> 🎯 **Pick your incident.** Reuse the lesson's "P99 latency 10x baseline / database pool exhaustion" scenario, or invent your own: a memory leak after a bad deploy, a spike in 500 errors, a queue backing up. Just make sure your fake data contains a real, findable cause.

### Why this is the perfect practice

| Lesson skill | Where you use it in NightShift |
|---|---|
| Defining an agent (model, prompt, tools) | Milestone 1 |
| Defining an environment (sandbox, allow-list) | Milestone 2 |
| Giving the agent data (files API) | Milestone 3 |
| Creating a session and streaming events | Milestone 4 |
| Wiring up local tools | Milestone 5 |
| Session persistence, state, and deletion | Milestone 6 |
| Going beyond basics (outcomes, runbook skill) | Milestone 7 |

### Milestones (build them in order, each one works on its own)

1. **Define the agent.** Create an SRE agent with a short system prompt and four tools: `get_metrics`, `get_recent_deploys`, `get_diff`, `get_logs`. Print its ID.
2. **Define the environment.** Create a sandbox environment. Start with a wide allow-list, then tighten it to only the domains the agent needs. Print its ID.
3. **Provide the data.** Make fake `metrics.json`, `deploys.json`, and `incident_logs.json` files where one deploy clearly caused the problem. Upload the logs via the files API.
4. **Run and stream.** Create a session binding the agent and environment, send "Debug my incident," and render each event as it streams: tool calls, then the final report.
5. **Implement the local tools.** Write the code that returns your JSON data when the agent calls each tool. Confirm the agent now actually investigates rather than just chatting.
6. **Make it durable.** Add a session list that survives a hard refresh, show each session's **state** (idle/running/terminated), and add a **delete** button that removes a session from the logs.
7. **Level up.** Add a **runbook skill** (a short doc of debugging steps) the agent can pull in. Then add an **outcome**: a rubric like "identify the root cause, cite the offending deploy, rule out at least two other causes, recommend a fix," and let the agent iterate until it passes.
8. **Stretch goals.** Swap one JSON tool for a real monitoring client (or a realistic mock with the same protocol). Trigger the agent from a **webhook** so a simulated alert auto-starts an investigation. Give it Claude Code so it can draft a fix PR.

### How you will know you are done

- ✅ A session investigates the incident and reports the correct **root cause**, citing the offending deploy.
- ✅ You can watch the work live as **events** (tool calls and responses), not one final blob.
- ✅ Hard-refresh and your sessions are still there; you can resume one and delete one.
- ✅ With an **outcome** rubric set, the agent loops until it meets the rubric.
- ✅ You can point to the moment **decoupling** helped: a tool runs locally while the loop runs server-side.

> 💡 **Keep yourself honest:** plant exactly one real cause in your fake data. If the agent finds it and rules out the decoys, your tools and context engineering are working.

---

## Practice exercises (optional extra reps)

> Small, self-contained tasks, each focused on one idea. Optional and independent. The **Capstone above is the main build** and already covers all of these.

### Exercise 1: trace the layers (foundational)
For a coding agent of your choice, write one sentence each on what you would have to build yourself on the **Messages API**, on the **Agent SDK**, and on **managed agents**. Where does your effort go in each case?

### Exercise 2: brain, hands, connection (foundational)
Describe an agent idea of yours and fill in its **agent**, **environment**, and **session**. What goes in each?

### Exercise 3: events vs request/response (foundational)
List five events you would expect from a single incident investigation, in order. Mark which are user, agent, and session events.

### Exercise 4: local tool to production tool (intermediate)
Write a local tool that returns metrics from a JSON file, then describe how you would swap it for a real Datadog (or similar) client without changing the agent. What stays the same?

### Exercise 5: design an outcome (intermediate)
Write a 4 to 6 point rubric for "successfully resolve an incident." Make each point objectively checkable. Then say how the agent's loop would behave if it fails point 3.

---

## Cheat sheet

```text
THE THREE PIECES
  Agent       = brain   (model, system prompt, tools, skills, MCP servers)
  Environment = hands   (sandbox/container, network allow-list, packages)
  Session     = connect (binds agent+env, mounts data, streams events)

WHY MANAGED AGENTS
  Agent loop runs SERVER-SIDE  -> durable; survives refresh & crashes
  Speaks in EVENTS, not tokens -> resumable + fully observable
  DECOUPLE brain from hands    -> stronger security + >90% faster TTFT (P95)

SESSION STATES
  idle -> running -> rescheduling (retry) -> terminated (on failure)
  webhooks can resume or kick off a session

GO FURTHER (out of the box)
  subagents | memory | dreaming | outcomes | vaults | webhooks | permissions

REMEMBER
  - Keep the system prompt short and clear.
  - Wire up local tools or the agent can't act.
  - Context engineering (the right data/files) is the real work.
  - Delete sessions to control retained data.
```

## How this connects to the rest of the course

- **Earlier, Module 5 · Lesson 13 (Get to production faster):** introduces the three building blocks and the event families this lesson puts to work.
- **Next, Module 5 · Lesson 15 (Build a production-ready agent):** another code-along, using multi-agent orchestration, outcomes, memory, and credential vaults.
- **Next, Module 5 · Lesson 16 (Tool, skill, or subagent?):** how to keep this kind of agent's design clean as it grows in capability.
- **Earlier, Module 2 · Lesson 3 (The prompting playbook):** the "generate, evaluate, repair" loop is the small-scale ancestor of **outcomes**.

---

*Source: "Ship your first Managed Agent" by Isabella He (Anthropic), Code with Claude 2026, London. Code snippets are illustrative reconstructions of the workshop steps described in the talk. Adapt the model names and API details to the current SDK.*

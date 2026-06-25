# Module 5 · Lesson 15: Build a Production-Ready Agent with Claude Managed Agents

> **Course:** Building with Claude, a self-paced course
> **Module 5:** Building agents, Claude Managed Agents
> **Speaker:** Anthropic, Member of Technical Staff
> **Source talk:** [Build a production-ready agent with Claude Managed Agents](https://www.youtube.com/watch?v=jWWsLe4Gh5Y) · [full transcript](../../transcripts/code-with-claude-2026-london-2026/14_build-a-production-ready-agent-with-claude-managed-agents.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

Claude Managed Agents is just a set of API endpoints that hand you production-ready agents and their supporting parts (sandboxes, credential vaults, memory, multi-agent threads, observability), and in this lesson you wire those endpoints into a working web app, watching a "deal desk" agent spawn helper agents and grade its own work against a goal.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you build **DealRoom**, a chat app whose agent researches companies, delegates to specialist sub-agents, and iterates against a rubric until it is satisfied. Everything before the Capstone teaches the endpoints and patterns you will use there. If you want to see the finish line first, jump to the **"Capstone Project: build DealRoom"** section near the end, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[Site Reliability Engineering (the Google SRE Book)](https://sre.google/sre-book/table-of-contents/)** (book). The definitive first-principles source on running services reliably (error budgets, retries, monitoring and observability), concepts that long predate and outlast any agent platform.
> - **[Building Effective Agents (Anthropic)](https://www.anthropic.com/engineering/building-effective-agents)** (essay). Connects SRE-style rigor specifically to agent design (simplicity, transparency, tested agent-computer interfaces).

## A few plain-language basics first

This lesson uses some everyday AI terms. Here they are in simple words:

- **LLM (Large Language Model):** the kind of AI that reads and writes text. "Claude" is an LLM.
- **Model:** one specific version, for example "Opus 4.7." Newer models are smarter.
- **Agent:** an AI that takes a series of actions on its own toward a goal, rather than answering in one shot.
- **Agent loop:** the repeating think-act-observe cycle an agent runs until the task is done.
- **Tool:** a small piece of code the agent can choose to run (search the web, read a file, call an API).
- **Endpoint:** one specific address in an API that does one job, for example "list sessions" or "create a session." You call it from your code.
- **SDK (Software Development Kit):** an official code library that wraps those endpoints so they are easy to call. The Anthropic SDK is one.
- **Context window:** the limited amount of text a single model instance can hold and reason over at once.
- **Sandbox / container:** a safe, isolated computer where the agent runs code and tools.
- **Streaming:** sending output piece by piece as it is produced, rather than waiting for the whole thing.
- **Session:** one ongoing run / conversation with the agent.

Every term is also explained again the first time it appears below.

## Why this lesson matters

It is easy to make an impressive agent demo on your laptop. It is hard to make one real people can use: that needs hosting, scaling, durable storage, sandboxing, secure credentials, and end-user authentication, none of which is fun to build and all of which is easy to get wrong. As the speaker puts it, "it's very easy to get some vibe coded platform... but actually deploying that means there are all these security challenges." This lesson shows you that managed agents is "just a set of API endpoints" you can use today with any API key, and walks through turning a half-finished starter app into something "you could be deploying to production today."

## Learning objectives

By the end of this lesson you will be able to:

1. Name the four core primitives (**agent**, **environment**, **session**, **events**) and call their main endpoints from the SDK.
2. Implement the two halves of a chat view: **sending events** to a session and **streaming events** back from it.
3. Use **per-tool permission controls** to auto-run safe tools and require approval for risky ones.
4. Use **outcomes** to make an agent iterate against a rubric until it succeeds.
5. Use **multi-agent** threads, **credential vaults**, and **memory stores**.
6. Use the **Claude API skill** and the **developer console** to build and observe agents faster.

## Prerequisites

- Module 5 · Lesson 13 (Get to production faster) and Lesson 14 (Ship your first managed agent): the building blocks and event families.
- Module 2 (Core skills): prompts, tools, models.

---

## Part 1: managed agents is just API endpoints

The speaker's framing is refreshingly plain: Claude Managed Agents is "just a set of API endpoints that we've developed and released." You can use them with any API key today. They give you scaled, production-ready agents plus the primitives around them, and you pick the ones you need and build your own product on top.

What did Anthropic take care of for you?

- Giving Claude **access to a computer** (a sandbox).
- **Credential vaults** to inject end-user authentication (for example, so Claude can use a user's Linear MCP) securely.
- The **tool-calling harness**, plus **retries** and **error recovery** that happen in production.
- Nice primitives for **memory**, **context management**, and **multi-agents**.
- Built-in **observability views** in the developer console to live-debug what agents are doing.

> 🔑 **Key idea: compose what you need, ditch the rest.** You are not forced to adopt a whole framework. Pick the primitives that fit your product and build your own experience on top of them.

## Part 2: the four primitives and their endpoints

The same building blocks from the earlier lessons, now seen as endpoints you call.

| Primitive | Think of it as | Key configuration |
|---|---|---|
| **Agent** | A **template** for the agent. | System prompt, skills, **which tools** it may use, **which MCP servers** it connects to, and **per-tool permission controls**. |
| **Environment** | A **template for the sandbox**. | Network access on or off, pre-installed npm/pip packages, or **bring your own** sandbox (Cloudflare, Modal, Vercel, your own fleet). |
| **Session** | An **ongoing conversation** with Claude. | Created from an agent ID + environment ID. Can include GitHub repos and files preloaded into the container. |
| **Events** | The **stream** of the conversation. | You submit events from your client; the server returns events Claude generates. |

> 💡 **Per-tool permission controls** are a standout. You can decide that a `file_read` tool **auto-executes**, while running **bash** or calling your database's MCP server requires explicit approval from your end user. You can also withhold web access entirely from an agent you want to protect from **prompt injection** (a trick where malicious text on a web page hijacks the agent's instructions).

Agents are also **versioned**: if you make a system-prompt or tool change you regret, you can roll back to a previous version. Nothing is thrown away.

### The events, in four families

| Event family | What it covers |
|---|---|
| **User events** | What you or your platform submit: text, images, documents, **interrupts** (to cut Claude off if it goes off on a bad tangent), tool results for your custom tools, confirmations for human-in-the-loop steps, and **outcome** definitions. |
| **Agent events** | What Claude does: messages, **compaction** (shrinking an over-large context window), tool execution, and **multi-agent coordination** when Claude spawns helpers. |
| **Session events** | Lifecycle: retries, errors, idling, termination, and outcome processing. |
| **Span events** | Markers for when long-running things start and end (for example Opus generating a very long document) so you do not think it is stuck. |

## Part 3: the build, a "deal desk" agent

The speaker builds **Deal Desk**, a contrived product for mergers and acquisitions: feed Claude data (in Linear or private sources) and have it help decide whether to invest in or acquire a company. The finished demo is a basic chat UI with a session sidebar, but the interesting part is that it uses **multi-agent**: a main agent spawns specialists, for example one for macro industry trends and one for financial analysis, each running as its own thread.

The workshop starts from a **starter** version with deliberately unimplemented endpoints (stubbed out), and fills them in. Below are illustrative reconstructions.

### List the sessions

```python
# Using the Anthropic SDK; these endpoints are live in production today.
def list_sessions():
    return client.beta.sessions.list()      # populates the sidebar
```

### Retrieve one session

```python
def get_session(session_id):
    return client.beta.sessions.retrieve(session_id)
    # Shows the agent, its tools, connected MCP servers (e.g. Linear),
    # and any outcomes that were defined.
```

### The chat view: send events, and stream events

The chat view has two halves. **Sending** an event is a straightforward endpoint. **Streaming** events back from the server to your client is the trickier half.

```python
# Half 1: send a user message into the session.
def send_event(session_id, text):
    return client.beta.sessions.events.create(
        session_id=session_id,
        event={"type": "user_message", "text": text},
    )

# Half 2: stream events the session generates, back to the client.
def stream_events(session_id):
    for event in client.beta.sessions.events.stream(session_id):
        yield event     # render tool calls, messages, sub-agent updates live
```

> 💡 **Let Claude write the hard half for you.** The speaker, rather than coding the streaming endpoint by hand, simply asked Claude. Claude Code ships by default with the **Claude API skill**, which makes Claude "really really good at using all of the Anthropic APIs," specifically the managed-agents ones. As the speaker put it, "Claude can help you build your own Claude."

## Part 4: outcomes, multi-agent, vaults, and memory

### Outcomes: define a goal, let Claude iterate

Instead of a plain message, you can send an **outcome** definition: a file or a blob of text that acts like a **spec** (a description of the desired result and how to judge it). Claude does a first pass, then enters a mode where it checks its own work against that **rubric** over and over until it satisfies it.

In the demo, the outcome describes three companies (Bridgewell Dynamics, Norwood Automation, Acme Robotics), points at data in Linear and uploaded files, and asks Claude to "iterate on finding information... criticize your own work, and let us know whether these findings actually satisfy the rubric." Claude is "off to the races," using tools, delegating to sub-agents, and reading files, until it reaches a conclusion it judges good enough.

> 🔑 **Outcomes turn "do this" into "achieve this."** You stop micromanaging tool calls and instead state the result you want plus how to judge it. The speaker calls this "a really, really great way to set up your agents for success."

### Multi-agent: specialists with their own context windows

When you create the session with multi-agent enabled, the main agent spawns helper threads. Each helper has its own context window and can chat with its coordinator, passing findings back and forth. In the console you see each helper as its own horizontal line of activity (one doing web searches, another reading financials), all iterating together.

```python
# A session whose agent is allowed to spawn helper agents and use memory.
session = client.beta.sessions.create(
    agent_id=deal_desk_agent.id,
    environment_id=env.id,
    mcp_servers=["linear"],
    memory_store_ids=[memory_store.id],
)
```

### Credential vaults: secrets Claude never sees

A **credential vault** lets you provision an MCP server's authentication tokens once, store them very securely inside Anthropic, and have them injected whenever Claude uses that server, **without the token ever entering Claude's context window**. You include the vault in your session; Anthropic injects the secret at tool time.

> 🔑 **Vaults keep secrets out of the model's sight.** The token for the Linear MCP or the Figma MCP is injected at call time and never appears in Claude's context. This is far safer than pasting credentials into a prompt.

### Memory stores: get better over time

You give Claude one or more **memory stores** it can read from and write to across sessions, so each session can build on the last. In the console you can **read** what Claude has written about itself, and **edit** it if Claude got something wrong, or add your own memories by hand.

## Part 5: the console and getting started fast

The **developer console** is not just for reading docs. It gives you:

- **Live observability**: click into a running session and watch the model and its sub-agents process things in real time, inspect each event's inputs and outputs, and see how long each tool call took (so you can debug a slow tool or an inefficient file).
- A **quick start** that lets you chat with Claude and have Claude help build your agents and sessions, plus predefined **templates**.
- A browser of your **agents** (with their versions), **environments**, **credential vaults**, and **memory stores**.

> 💡 As the speaker admits, "nobody really reads docs these days, everybody just points Claude at them." That is fine: the docs cover endpoints for every primitive, and the **Claude API skill** plus the console mean you can move quickly. Read the docs once to know what exists, then let Claude do the wiring.

### What you would have built yourself

If you did all this without managed agents, you would have had to build: your own agent loop (or use the Agent SDK), remote hosting, context management, state-transition handling and recovery, skills and MCP integration, a **durable storage layer** for all events and threads, a **sandboxing fleet**, and **end-user authentication**, the last of which is "not easy to do in a secure and reliable way."

> 🔑 **That long list is exactly what managed agents gives you out of the box.** You did not use every primitive in this one demo, but each was there if you needed it.

---

## Key takeaways

1. **It is just endpoints.** Managed agents is a set of API endpoints usable today with any API key. Compose what you need, ignore the rest.
2. **Four primitives:** agent (a template), environment (a sandbox template), session (an ongoing conversation), and events (the stream).
3. **The chat view is two halves:** sending events and streaming events back. Let the Claude API skill write the tricky streaming half.
4. **Per-tool permissions** let safe tools auto-run and risky tools require approval, and you can deny web access to dodge prompt injection.
5. **Outcomes** turn "do this" into "achieve this": give a rubric and Claude self-grades in a loop.
6. **Multi-agent, vaults, and memory** give you parallel specialists, secrets the model never sees, and improvement over time.
7. **The console is your live debugger.** Watch sessions, inspect events, and time tool calls.

## Common pitfalls

- ❌ Building your own agent loop, storage, sandboxes, and auth before checking whether managed agents already covers them.
- ❌ Letting every tool auto-execute, including bash and database calls, with no human approval.
- ❌ Pasting API tokens into prompts instead of using credential vaults.
- ❌ Giving an agent web access it does not need, opening it to prompt injection.
- ❌ Forgetting agents are versioned, then panicking after a bad system-prompt edit.
- ❌ Hand-coding the streaming endpoint when the Claude API skill could do it for you.

---

## 🛠️ Capstone Project: build DealRoom

> This is the main hands on project for the lesson. You are building the speaker's deal-desk demo, your own version of an app where a chat agent researches companies, delegates to specialists, and grades its own work. Start with a single endpoint and grow into a full chat UI.

### What you will build

**DealRoom** is a chat web app (or a script that grows into one) backed by a managed agent that researches companies and recommends whether to invest or acquire. It lists sessions, streams the conversation live, spawns specialist sub-agents, uses a credential vault and a memory store, and finishes by iterating against an **outcome** rubric.

> 🎯 **Pick your domain.** Use fake M&A companies like the talk (Bridgewell Dynamics, Norwood Automation, Acme Robotics), or swap in something you find fun: vetting open-source libraries to adopt, comparing job offers, or scouting holiday destinations. You just need a domain where one main agent benefits from a few specialists and a clear "good enough" rubric.

### Why this is the perfect practice

| Lesson skill | Where you use it in DealRoom |
|---|---|
| Calling the session endpoints (list, retrieve) | Milestone 1 |
| Sending events into a session | Milestone 2 |
| Streaming events back to the client | Milestone 3 |
| Per-tool permission controls | Milestone 4 |
| Multi-agent specialists | Milestone 5 |
| Credential vaults and memory stores | Milestone 6 |
| Outcomes (self-grading loop) | Milestone 7 |

### Milestones (build them in order, each one works on its own)

1. **List and retrieve sessions.** Set up the Anthropic SDK with your API key. Implement `list_sessions` to populate a sidebar, and `get_session` to show one session's agent, tools, and MCP servers.
2. **Send a message.** Implement the send-event endpoint so you can submit a user message to a session and see it land.
3. **Stream the reply.** Implement the streaming endpoint so events flow back live: messages, tool calls, sub-agent updates. (Stuck? Ask Claude with the Claude API skill to write it.)
4. **Lock down the tools.** Configure per-tool permissions: let `file_read` auto-run, require approval before `bash` or a database MCP call, and decide whether this agent gets web access at all.
5. **Add specialists.** Enable multi-agent so the main agent spawns a "macro trends" helper and a "financial analysis" helper. Watch both threads in the console.
6. **Add secrets and memory.** Provision a **credential vault** for one MCP server (for example Linear) and confirm the token never appears in Claude's context. Attach a **memory store** and read what Claude writes to it.
7. **Define an outcome.** Send an outcome with a rubric ("for each company: summarise financials, cite at least two sources, flag one risk, and give a clear invest/avoid call"). Let Claude iterate until it satisfies the rubric, and show the outcome-processing events.
8. **Stretch goals.** Roll an agent back to a previous **version** after a deliberate bad edit. Add a self-hosted sandbox. Time your slowest tool call in the console and speed it up.

### How you will know you are done

- ✅ Your sidebar lists sessions and clicking one shows its details, all from the real endpoints.
- ✅ You can send a message and watch the reply **stream** back, including sub-agent activity.
- ✅ A risky tool **pauses for approval** while a safe one auto-runs.
- ✅ A credential vault injects a secret that you confirm **never enters Claude's context**.
- ✅ With an **outcome** rubric set, the agent loops and stops only when it meets the rubric.

> 💡 **Keep yourself honest:** if you cannot see, in the console, each sub-agent's separate thread and the moment the outcome was satisfied, your observability wiring is not finished.

---

## Practice exercises (optional extra reps)

> Small, self-contained tasks, each focused on one idea. Optional and independent. The **Capstone above is the main build** and already covers all of these.

### Exercise 1: map endpoints to primitives (foundational)
List the four primitives and, for each, name two endpoints you would call (for example, for sessions: list and stream events). One sentence each on what they do.

### Exercise 2: design a permission policy (foundational)
For a coding agent, sort these tools into "auto-run" and "needs approval": file read, web search, bash, delete file, database write. Justify each in a sentence.

### Exercise 3: send and stream (intermediate)
Write pseudocode for the two halves of a chat view: one function that sends a user event, one that streams events back and renders messages, tool calls, and sub-agent updates differently.

### Exercise 4: write an outcome rubric (intermediate)
Pick a research task and write a 5-point rubric Claude should grade itself against. Make each point objectively checkable. Predict one way Claude might "pass" the rubric while still being unhelpful, and tighten the rubric to prevent it.

### Exercise 5: secure a secret (intermediate)
Describe, step by step, how a **credential vault** keeps an MCP token out of Claude's context: where the token lives, when it is injected, and what Claude sees. Contrast with pasting the token into a prompt.

---

## Cheat sheet

```text
THE FOUR PRIMITIVES (as endpoints)
  Agent       -> template: prompt, tools, MCP servers, per-tool permissions (versioned)
  Environment -> sandbox template: network on/off, packages, bring-your-own
  Session     -> ongoing conversation (agent id + env id, +repos/files)
  Events      -> stream you submit to and read from

CHAT VIEW = TWO HALVES
  send events   -> straightforward endpoint
  stream events -> server -> client; let the Claude API skill write it

POWER FEATURES
  Per-tool permissions -> safe tools auto-run, risky tools need approval
  Outcomes             -> give a rubric; Claude self-grades in a loop
  Multi-agent          -> specialists, each with its own context window
  Credential vaults    -> secrets injected at call time; never in context
  Memory stores        -> read/write across sessions; get better over time

GO FASTER
  Claude API skill (ships with Claude Code) | developer console quick start + templates
  Console = live observability: inspect events, time tool calls

REMEMBER
  - It's just API endpoints; use any API key today.
  - Deny web access to agents that don't need it (prompt injection).
  - Agents are versioned; roll back bad edits.
```

## How this connects to the rest of the course

- **Earlier, Module 5 · Lesson 13 (Get to production faster):** the primitives and event families this lesson calls as endpoints.
- **Earlier, Module 5 · Lesson 14 (Ship your first managed agent):** a simpler single-agent build; here we add multi-agent, vaults, and memory.
- **Next, Module 5 · Lesson 16 (Tool, skill, or subagent?):** how to decide between tools, skills, and sub-agents so your agent stays clean as it grows.
- **Earlier, Module 2 · Lesson 3 (The prompting playbook):** the "generate, evaluate, repair" loop is the small-scale ancestor of **outcomes**.

---

*Source: "Build a production-ready agent with Claude Managed Agents" by a Member of Technical Staff (Anthropic), Code with Claude 2026, London. Code snippets are illustrative reconstructions of the workshop steps described in the talk. Adapt the model names and API details to the current SDK.*

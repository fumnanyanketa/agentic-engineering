# Module 5 · Lesson 13: Get to Production Faster with Claude Managed Agents

> **Course:** Building with Claude, a self-paced course
> **Module 5:** Building agents, Claude Managed Agents
> **Speaker:** Michael and Harrison, Members of Technical Staff, Anthropic, with a partner panel (Cloudflare, Daytona, Modal, Vercel)
> **Source talk:** [How to get to production faster with Claude Managed Agents](https://www.youtube.com/watch?v=zenIB7XLZxQ) · [full transcript](../../transcripts/code-with-claude-2026-london-2026/13_how-to-get-to-production-faster-with-claude-managed-agents.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

When you build an AI agent for real users, the hard part is no longer the model's intelligence, it is the infrastructure around it (identity, security, scaling, memory, observability), and Claude Managed Agents is a hosted platform that hands you those pieces as ready-made building blocks so you can ship to production far faster.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you build a small agent control panel called **MissionControl** that defines an agent, runs it, and shows you everything it is doing through a live event stream. Everything before the Capstone teaches the ideas you will use there. If you want to see the finish line first, jump to the **"Capstone Project: build MissionControl"** section near the end, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[Building Effective Agents (Anthropic)](https://www.anthropic.com/engineering/building-effective-agents)** (essay). The canonical "build with simple, composable, transparent patterns" framing behind taking an agent from demo to production.
> - **[Embracing Risk (Google SRE Book)](https://sre.google/sre-book/embracing-risk/)** (essay). Production reliability from first principles: availability targets and error budgets that outlast any tooling.

## A few plain-language basics first

This lesson uses some everyday AI terms. Here they are in simple words, so nothing below is confusing:

- **LLM (Large Language Model):** the kind of AI that reads and writes text. "Claude" is an LLM. Think of it as a very capable text assistant.
- **Model:** one specific version of that AI, for example "Sonnet 4.6" or "Opus 4.7." Newer models are smarter, and the talk mentions Opus 4.7 as the newest.
- **Agent:** an AI that takes a series of actions on its own toward a goal (using tools, running code, calling other systems) rather than just answering in one shot.
- **Tool:** a small piece of code the agent can choose to run, for example to look something up, send an email, or do exact maths.
- **Tool use:** the general name for an agent's ability to call tools.
- **Harness:** all the code and settings around the model: the loop that runs it, the tools it can call, the way state is stored. The model is the brain, the harness is everything else.
- **Sandbox:** a safe, isolated computer (a container) where the agent can run code and use tools without touching your real systems.
- **Production:** running software for real users at scale, reliably, as opposed to a quick demo on your laptop.
- **API (Application Programming Interface):** the connection your code uses to talk to a service. An "API call" is one such request.

You do not need to memorise these. Every term is also explained again the first time it appears below.

## Why this lesson matters

For the last few years the limit on what agents could do was raw intelligence. That has flipped. As Michael put it, the bottleneck towards increasing capabilities "is really the infrastructure around these models and not so much the intelligence for them." Two years ago Claude could write you a single test function while you approved every step. Today people clear their backlogs overnight and wake up to merge-ready pull requests. The next step is agents that run for hours and complete whole projects. To get there, an agent needs secure access to your systems, an identity of its own, somewhere safe to run, and a way for you to watch what it is doing. Building all of that yourself is slow and error-prone. This lesson shows you a platform that gives it to you out of the box.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain what **Claude Managed Agents** is and which problems it solves (infrastructure, agent primitives, observability).
2. Define the core building blocks: an **agent definition**, an **environment**, and a **session**.
3. Read an agent's **event stream** and name the four families of events (user, agent, session, span).
4. Describe the advanced features the talk announced: **multi-agent orchestration**, **outcomes**, **memory**, **dreaming**, **self-hosted sandboxes**, and **MCP tunnels**.
5. Get started fast using the Claude API skill, the CLI, or the cookbooks.

## Prerequisites

- Module 2 (Core skills): you know how to send a message to Claude and get a reply, and what a tool is.
- Helpful but optional: Module 2 · Lesson 3 (The prompting playbook), where the "generate, evaluate, repair" loop foreshadows the agent loops here.

---

## Part 1: why infrastructure is now the bottleneck

The talk opens with a quick history. With the Claude 3 family you could get simple, short tasks done. With Opus 4 and the arrival of Claude Code (Anthropic's coding agent), Claude could drive an entire feature and open a pull request, though you steered it the whole way. (A **pull request**, or **PR**, is a proposed code change that a teammate reviews before it is merged in.) With the newest models, people clear whole backlogs while they sleep.

> 🔑 **Key idea: the limit moved.** Once models are smart enough to work for hours, the thing standing between you and a useful product is no longer intelligence. It is everything that surrounds the model. As Harrison summed it up, for your agents "to be able to accomplish more, they need access to more."

What does "more access" mean in practice? Imagine an agent team running a company acquisition end to end. It needs:

- **Secure credentials** and access to **internal systems** (Slack, email, databases).
- Access to **private code repositories** if it is making code changes.
- An **identity** of its own. An agent needs to be a known "who," with its own permissions, just like a human employee has a login.

The team also saw new ways people want to talk to agents, beyond the familiar "send text, get a reply":

| Style of interaction | What it means |
|---|---|
| **Conversational** | You send a message, the agent replies. The familiar chat style. |
| **Outcome-oriented** | You hand the agent a whole task and it goes off, working on its own, coming back only when it is confident the job is done. |
| **Long-running / resumable** | You start an agent, then pick it up later (even weeks later) and it carries on right where it left off. |

> 💡 **The four sticking points the team kept hearing about** when researching what stops people from shipping agents:
> 1. **Context and memory.** When they work, they work great. Get them wrong and they "completely destroy" how well your agent performs. (**Context** is the information the model is currently working with; **memory** is information kept across sessions.)
> 2. **Infrastructure.** Reliability, scalability, security, and even latency (how fast it responds) all start to matter in production. This was cited as the number one blocker.
> 3. **Observability.** If you cannot tell whether the agent is succeeding, nothing else matters.

## Part 2: what Claude Managed Agents gives you

Claude Managed Agents (the talk often shortens this to "managed agents" or "CMA") is a set of API endpoints. Anthropic did the platform work so you do not have to. You pick the **composable primitives** you need and build your product on top. ("Primitive" just means a basic building block. "Composable" means you can mix and match them freely.) The pieces fall into three groups:

- **Infrastructure:** reliability, scaling, security, low latency, sandboxing.
- **Agent primitives:** the agent loop, tools, skills, memory, multi-agent coordination.
- **Observability:** a live view of what the agent is doing and why.

### The three things you define

To start building, you define three things:

| Building block | Plain meaning | What goes in it |
|---|---|---|
| **Agent** | The identity of the thing taking action. A bundle of configuration. | System prompt, model, skills, tools, permissions. |
| **Environment** | The computer the agent runs on. | A sandbox where you set the network allow-list and pre-installed packages. |
| **Session** | One ongoing run / conversation. | Kicks off the work; you watch it through the event stream. |

> 🔑 **The mental model.** Define **who** the agent is (the agent), give it **somewhere to run** (the environment), then **start it working** (the session). A "network allow-list" is just a list of the only websites or services the agent is allowed to reach, which keeps it from wandering off to places it should not go.

```text
1. Define an agent      -> system prompt + model + skills + tools + permissions
2. Set up an environment -> a sandbox with a network allow-list and packages
3. Start a session       -> ask the agent to do work; watch the event stream
```

## Part 3: the event stream, how you watch the agent work

Every session is, in effect, a **log of events**: a running list of things that happened as you and the agent interacted. (An **event** is a single recorded thing: a message, a tool call, a status change.) Listening to this stream is how you observe the agent "cooking." The talk splits events into four families so each is easy to understand.

| Event family | What it covers | Examples |
|---|---|---|
| **User events** | Things you (or your app, or your end users) send to the agent. | Text messages, images, documents; an **interrupt** to steer the agent back on course; tool results for tools you run yourself; confirmations for human-in-the-loop steps. |
| **Agent events** | Anything Claude is doing on its side. | Replying with a message, executing tools, coordinating with other agents. |
| **Session events** | The overall lifecycle of the session. | Status changing from idle to running, error recovery, outcome processing. |
| **Span events** | Markers that say when a long-running thing starts and ends. | Claude beginning a very long response, so you know it is not stuck. |

> 💡 An **interrupt** is you stepping in mid-run to cut the agent off, for example if it has gone "off course" and you want to redirect it. **Human-in-the-loop** means a person must approve certain actions before the agent is allowed to take them. These are your safety levers.

### A concrete demo: Pascal the grocery agent

The talk demos **Pascal**, a fictitious agent that studies grocery-shopping habits. From a dashboard, they click "Analyze." In the developer console they watch the event stream in real time: tool runs, agent events, the agent's definition (system prompt, model, MCP tool configuration) on the right, and the environment's networking and installed packages. Claude reports findings (bananas are popular; Sunday is a bad day to shop), then runs a predictive reorder analysis. There is even an **"Ask Claude"** button that reads the session transcript and suggests how to improve the agent's configuration (for example, spotting a Python script that ran slowly and could be sped up).

> 🔑 **Observability is a first-class feature, not an afterthought.** Because everything is an event exposed over an API, you can see exactly what the agent did, surface it in your own app, and even ask Claude to critique its own setup.

## Part 4: the advanced features (announced in the talk)

The team highlighted several more powerful capabilities. You do not need all of them on day one, but knowing they exist shapes how you design.

| Feature | Plain-language explanation |
|---|---|
| **Multi-agent orchestration** | Claude can spawn other agent threads, each with its own separate context window, and delegate work to them, passing messages back and forth. (A **context window** is the limited amount of text a single model instance can hold at once; giving each helper its own keeps things from getting crowded.) |
| **Outcomes** | You define a **rubric** (a checklist or set of goals). The agent does a first pass, then grades itself against the rubric and keeps iterating in a loop until it is satisfied. |
| **Memory** | The agent reads and writes from long-lived **memory stores**, so every session can be better than the last. |
| **Dreaming** (research preview) | Claude reflects across thousands of past sessions at once to produce new memories, edit old ones, and keep its memory "top-notch." |
| **Self-hosted sandboxes** | Bring your own compute. Run the agent's tools inside your own network (your **VPC**, or virtual private cloud, meaning your private slice of the cloud) instead of on Anthropic's. Anthropic just signals when a new sandbox is needed; you control provisioning, network policies, and audit logs. |
| **MCP tunnels** (research preview) | Expose your private **MCP servers** to Claude through a secure tunnel without ever putting them on the public internet. |

> 💡 **What is MCP?** MCP (Model Context Protocol) is a shared standard for connecting an AI to external tools and data. An **MCP server** is a service that offers tools over that standard. A "tunnel" is a secure private pipe, so Claude can reach a server that lives only inside your network.

### What the partners are betting on

Four infrastructure partners joined for self-hosted sandboxes: **Cloudflare, Daytona, Modal, and Vercel.** A few themes worth carrying with you:

- **Agents need what humans need** (Yvon, Daytona): not just code-execution boxes, but varied CPU, RAM, operating systems, even GPUs, plus pausing, resuming, and **forking** (cloning a run so the agent can try several paths at once), all at huge speed and scale.
- **Scale beyond the micro VM** (Mike, Cloudflare): as intelligence gets cheaper, the world will run a massive number of agents, so lighter-weight isolation that spins up in milliseconds matters alongside full virtual machines.
- **Massive, fast scale** (Akshat, Modal): spinning up hundreds of thousands of sandboxes in minutes, GPU sandboxes for jobs like optimising inference.
- **Resumability and "multiplayer"** (Luke, Vercel): pausing a task and keeping your place, and rethinking how multiple agents and humans collaborate.

> 🔑 **A recurring theme across the whole panel:** the **human emulator** idea. As Yvon put it, "anything that a human can do digitally... you can now have an agent do if you give it a sandbox." Give an agent a real computer and it can install an app, log into a legacy system, and produce an end-to-end result, not just answer a question.

## Part 5: how to actually get started

Three on-ramps, from easiest to most hands-on:

1. **The Claude API skill in Claude Code.** If you have Claude Code installed, use the built-in **Claude API skill**. A **skill** is packaged knowledge Claude can pull in when it needs it; this one knows all about managed agents and makes integration "an absolute breeze."
2. **The CLI.** A command-line tool to interact with your agents and sessions through simple commands. (A **CLI**, command-line interface, is a text-based way to run a tool by typing commands.)
3. **The cookbooks.** Copy-paste-ready example code you can adapt to your needs.

```text
FASTEST PATHS TO A FIRST AGENT
  1. In Claude Code, use the Claude API skill  -> it knows managed agents
  2. Use the CMA CLI                            -> create/run agents and sessions
  3. Copy a cookbook example                    -> adapt to your needs
```

> 💡 As Harrison said of Claude Code, it is "my favorite tool of all." The fastest way to build with managed agents is often to ask Claude itself to help you, using the skill that already understands the platform.

---

## Key takeaways

1. **Intelligence is no longer the bottleneck. Infrastructure is.** Smart models can work for hours; what stops you is identity, security, scaling, memory, and observability.
2. **Managed agents hands you those pieces as composable primitives.** Pick the ones you need, ignore the rest, and build your product on top.
3. **Three building blocks:** an **agent** (who it is), an **environment** (where it runs), a **session** (one run you watch).
4. **Everything is an event.** The event stream (user, agent, session, span) is how you observe, steer, and debug your agent live.
5. **The big levers** are multi-agent orchestration, outcomes, memory, dreaming, self-hosted sandboxes, and MCP tunnels.
6. **Start fast** with the Claude API skill, the CLI, or the cookbooks. Let Claude help you build your Claude agent.

## Common pitfalls

- ❌ Trying to build the agent loop, scaling, storage, and security yourself before you have even proven the agent is useful.
- ❌ Giving an agent broad access with no network allow-list or human-in-the-loop checks.
- ❌ Shipping with no observability, so you cannot tell whether the agent is actually succeeding.
- ❌ Treating memory and context as afterthoughts; get them wrong and the agent's quality collapses.
- ❌ Assuming you need every advanced feature on day one. Start small, add primitives as you need them.

---

## 🛠️ Capstone Project: build MissionControl

> This is the main hands on project for the lesson, and the best way to make the ideas stick. You are going to build a small control panel for a managed agent: define it, run it, and watch it work through the event stream. Start as small as a single script and grow it as far as you like.

### What you will build

**MissionControl** is a tiny web app (or even just a script) that does three things, matching the three building blocks from the lesson:

1. **Define** an agent (system prompt, model, tools, permissions) and an environment (sandbox with a network allow-list).
2. **Run** a session: hand the agent a task and let it work.
3. **Observe** the live event stream, showing each event labelled by family (user, agent, session, span), with an interrupt button so you can steer.

> 🎯 **Pick your agent's job.** Choose something small but real: a **research assistant** that summarises a topic from the web, a **repo janitor** that tidies a code project, or a **shopping-habits analyst** like Pascal in the talk. Pick one where you will clearly see tool calls and a final result.

### Why this is the perfect practice

| Lesson skill | Where you use it in MissionControl |
|---|---|
| Defining an agent (prompt, model, tools, permissions) | Milestone 1 |
| Setting up an environment (sandbox, network allow-list) | Milestone 2 |
| Starting and managing a session | Milestone 3 |
| Reading the four event families | Milestone 4, your live dashboard |
| Human-in-the-loop and interrupts | Milestone 5 |
| Outcomes (self-grading loop) | Milestone 6 |

### Milestones (build them in order, each one works on its own)

1. **Define the agent.** Using the Anthropic SDK (the official code library for calling Claude) or the CLI, create an agent with a clear system prompt, a model (for example Opus 4.7), and a small set of tools. Print its unique ID.
2. **Define the environment.** Create an environment with a **network allow-list** (start with one or two domains the agent genuinely needs) and any packages it requires. Print its ID.
3. **Start a session.** Bind the agent and environment, send it a task, and confirm it begins running. (Smallest version: a script that prints the agent's final reply. Bigger version: a chat UI with a sidebar of sessions.)
4. **Stream the events.** Listen to the event stream and print each event labelled by family: user, agent, session, span. This is your live dashboard. You should be able to watch tool calls happen in real time.
5. **Add control.** Add an **interrupt** button (or command) that stops the agent mid-run, and a human-in-the-loop confirmation for one "risky" tool so the agent must ask before using it.
6. **Add an outcome.** Give the agent a **rubric** (a short checklist describing a good result) and let it self-grade and iterate until it passes. Show the outcome-processing events in your dashboard.
7. **Stretch goals.** Persist and resume sessions (close the app, reopen, continue). Add a **memory store** so the agent remembers preferences between runs. Try a **multi-agent** version where the main agent spawns one helper and you watch both threads.

### How you will know you are done

- ✅ You can create an agent and an environment and get back IDs for each.
- ✅ Starting a session runs the agent, and you can read its events live, correctly labelled by family.
- ✅ You can **interrupt** a run and require a confirmation before one specific tool fires.
- ✅ With an **outcome** rubric set, the agent loops and improves until it meets the rubric, and you can see that in the stream.
- ✅ You can close the app and resume a session where it left off.

> 💡 **Keep yourself honest:** if you cannot tell from your own dashboard what the agent just did and why, your observability is not done yet. That is the whole point of the event stream.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each focused on one idea from the lesson. They are optional and independent. The **Capstone above is the main build** and already exercises all of these, so feel free to skip straight to it.

### Exercise 1: name the events (foundational)
Take a transcript of any agent run (your own, or imagine Pascal). Label each line as a **user**, **agent**, **session**, or **span** event. Where would an **interrupt** appear, and who sends it?

### Exercise 2: scope the access (foundational)
For an agent that books restaurant reservations, write its **network allow-list** (which domains it may reach) and decide which one tool should require **human-in-the-loop** approval. Justify each choice in one sentence.

### Exercise 3: agent vs environment vs session (foundational)
Write one sentence each defining the **agent**, the **environment**, and the **session**, using a real agent idea of yours. Then say what would break if you confused two of them.

### Exercise 4: design an outcome rubric (intermediate)
Pick a task ("write a competitor analysis of three companies"). Write a 4 to 6 point **rubric** the agent should grade itself against. Make each point checkable, not vague.

### Exercise 5: choose your infrastructure (intermediate)
Your agent needs GPUs and must keep all data inside your own network. Using the partner themes from Part 4, write a short paragraph on whether you would use Anthropic-managed sandboxes or a **self-hosted sandbox**, and why.

---

## Cheat sheet

```text
THE THREE BUILDING BLOCKS
  Agent       = who it is   (system prompt, model, skills, tools, permissions)
  Environment = where it runs (sandbox, network allow-list, packages)
  Session     = one run you watch (kick off work, stream events)

THE FOUR EVENT FAMILIES
  User events     -> what you/your users send (text, images, interrupts, confirmations)
  Agent events    -> what Claude does (messages, tools, coordinating agents)
  Session events  -> lifecycle (idle -> running, errors, outcome processing)
  Span events     -> "this long thing is starting / ending"

THE BIG LEVERS (add as you need them)
  Multi-agent  -> spawn helpers with their own context windows
  Outcomes     -> give a rubric; agent self-grades in a loop
  Memory       -> long-lived stores; each session better than the last
  Dreaming     -> reflect across many sessions to curate memory
  Self-hosted sandboxes -> run tools in your own network
  MCP tunnels  -> reach private MCP servers securely

GET STARTED
  Claude API skill in Claude Code  |  the CLI  |  the cookbooks
```

## How this connects to the rest of the course

- **Earlier, Module 2 · Lesson 3 (The prompting playbook):** the "generate, evaluate, repair" loop there is the small-scale ancestor of **outcomes** and multi-agent loops here.
- **Next, Module 5 · Lesson 14 (Ship your first managed agent):** a hands-on build of an incident-response agent that makes these primitives concrete.
- **Next, Module 5 · Lesson 15 (Build a production-ready agent):** a deeper, code-along build using multi-agent orchestration, outcomes, memory, and credential vaults.
- **Next, Module 5 · Lesson 16 (Tool, skill, or subagent?):** how to keep an agent's design clean as it grows, deciding when to reach for each primitive.

---

*Source: "How to get to production faster with Claude Managed Agents" by Michael and Harrison (Anthropic), with a partner panel from Cloudflare, Daytona, Modal, and Vercel, Code with Claude 2026, London. Code and command snippets are illustrative reconstructions of the approaches described in the talk. Adapt the model names and API details to the current SDK.*

# Module 7 · Lesson 26: Build AI Agents Using Claude in Microsoft Foundry

> **Course:** Building with Claude, a self-paced course
> **Module 7:** Deploying on your cloud
> **Speaker:** Marlene Mungai, Senior Developer Advocate, Microsoft (London)
> **Source talk:** [Build AI agents using Claude in Microsoft Foundry](https://www.youtube.com/watch?v=TQd_YQvydVg) · [full transcript](../../transcripts/code-with-claude-2026-london-2026/20_build-ai-agents-using-claude-in-microsoft-foundry.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

You can build a working AI agent on Microsoft Foundry by deploying a Claude model, testing it in a playground, pulling its endpoint into your own code with the Microsoft Agent Framework, and then giving the agent real abilities by connecting it to an MCP server that supplies tools, reusable prompts, and live data.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you build the **Sparkles Cupcake Agent**: a Claude powered agent that takes real orders by talking to a cupcake shop's MCP server. Everything before the Capstone teaches the four steps you will use there (deploy, test, code, connect tools). If you want the finish line first, jump to the **"Capstone Project"** section, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[What is Microsoft Foundry? (Microsoft Learn)](https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry)** (docs). The official platform overview (deploy models including Claude, build and orchestrate agents, enterprise security and governance), the durable reference for the lesson's deploy-test-code-connect flow.
> - **[Microsoft Agent Framework Overview (Microsoft Learn)](https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview)** (docs). First-principles coverage of agents vs workflows and tools/MCP, with explicit Claude support.

## A few plain-language basics first

This lesson mixes Claude terms with Microsoft terms. Here they are in plain words:

- **Model:** one specific version of Claude, for example "Sonnet 4.6" or "Opus 4.7." Models trade off intelligence, speed, and price.
- **Agent:** an AI that can "plan, reason, and take action" on your behalf over time, rather than just answering one message. This is the step beyond a single turn chat.
- **Single turn conversation:** you ask, the AI answers, and that is it. An agent goes further, taking multiple steps toward a goal.
- **Microsoft Foundry:** Microsoft's unified platform for building AI applications and agents at scale (formerly known as Azure AI Foundry). It hosts models, an agent service, tools, and machine learning services.
- **Deploying a model:** making a model available to use through your own endpoint, so your code can call it.
- **Endpoint / URI:** the web address your code sends requests to. A **URI** ("uniform resource identifier") is that address.
- **API key:** a secret string that proves your code is allowed to call the endpoint.
- **.env file:** a small text file that holds settings and secrets (like the endpoint and API key) so your code can read them without hard coding them.
- **IDE:** "integrated development environment," the app you write code in, for example Visual Studio Code (VS Code).
- **Microsoft Agent Framework:** an open source Microsoft library (Python, and likely TypeScript) for building agents.
- **MCP (Model Context Protocol):** an open standard "for letting AI agents talk to external systems." An **MCP server** exposes tools, prompts, and resources to your agent over a URL.
- **Tool:** a function the agent can call to do something, like look up which cupcakes are in stock.
- **System prompt:** the standing instructions that set the agent's persona and behaviour.

You do not need to memorise these. Each is explained again the first time it appears below.

## Why this lesson matters

Marlene opens with the shift the whole industry is going through: away from "single-turn AI conversations" toward "agentic systems where our agents can plan, they can reason, and they can take action on our behalf over time." That shift brings three new challenges. This lesson is deliberately practical: "we're not just going to be talking about what AI agents are, but we're actually going to be building them using Claude models in Foundry." By the end you will have deployed a Claude model, plugged it into an agent, and given that agent tools, which is the exact loop you repeat for any real agent.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain the three new challenges of **agentic systems** and how a platform like Foundry addresses them.
2. **Deploy a Claude model** in Microsoft Foundry and test it in the **playground** with custom system prompts.
3. Pull the model's **endpoint and API key** into your own code via a `.env` file and the **Microsoft Agent Framework**.
4. Connect your agent to an **MCP server** to give it tools, reusable prompts, and live data.

## Prerequisites

- Module 1 (the basics of running code and calling a model).
- Basic Python (the workshop's code is Python).
- An Azure / Microsoft Foundry account (free Azure credits are enough for learning).
- Helpful but optional: a prior look at MCP (Model Context Protocol), revisited in plain terms here.

---

## Part 1: why agents need a platform

Single turn chat is giving way to agents that plan, reason, and act over time. Marlene names three challenges that come with that, and they are the reason a platform helps:

| Challenge | What it means | Why a platform helps |
|---|---|---|
| **Multi step reasoning over long context** | The model must work through many steps and keep track of a lot of information. | You need a strong reasoning model, hosted reliably. |
| **Reliability, observability, security** | Especially for enterprises, the system must be dependable, you must be able to see what it is doing, and it must be secure. | The platform provides these out of the box rather than you building them. |
| **Connecting to tools and data** | Agents need to reach external systems and data sources to be useful. | The platform offers many ready connectors and MCP tools. |

Marlene makes a sharp point: "even though we love the Claude models... we can't just rely on the models getting better, we also need systems to be able to actually have those models with that intelligence executed." A smart model is necessary but not sufficient; you need a system around it.

> 🔑 **Key idea: intelligence plus execution.** The model supplies the intelligence. The platform supplies the execution: reliability, observability, security, and connections. Agents need both.

### What Microsoft Foundry is

Foundry is Microsoft's "unified platform for building AI applications and agents at scale." You can work in the tools you already use (GitHub, VS Code, Visual Studio, or Copilot Studio). At its core it offers:

- **Foundry models** (including Claude).
- An **agent service** for creating and orchestrating agents.
- **Tools and integrations**: over 1,400 built in connectors and MCP tools, so agents can act in real systems like SAP or ServiceNow.
- **Machine learning services** like fine tuning.

Agents built on Foundry come with enterprise features built in: security, observability, and governance, plus integrations with **Microsoft Defender** (security), **Microsoft Purview** (data governance), and **Entra ID** (identity). As Marlene notes, this means "you're not working with .env files all the time" in production, the platform handles secrets and identity for you.

> 💡 **Why developers pick Claude in Foundry.** Marlene lists four reasons: best in class reasoning for agents (her "daily driver" is Opus 4.7), the ability to create and orchestrate agents in the platform, enterprise features out of the box, and a faster prototype to production cycle thanks to built in evaluation, observability, and monitoring tools.

> 🎯 The promise is "moving from just building prototypes... and actually deploying those agents into production enterprise environments." This lesson walks the prototype end; the platform exists to carry you to the production end.

---

## Part 2: deploy and test a Claude model in the playground

The workshop is hands on and runs in a guided environment (Marlene uses one called **Skillable**, where clicking a green box auto fills inputs so you do not type secrets by hand). You are building an agent for **Sparkles**, "the friendliest cupcake shop on the internet," which has too many customers and not enough hands at the counter.

### Step 1: open Foundry and find your model

Inside Foundry, you open your project, go to the **Start building** page, switch to the **Build** toggle, and click **Models**. This shows the models available to you. In the workshop, **Claude Sonnet 4.6** is already there.

```text
Foundry -> your project -> Start building -> Build toggle -> Models
  Available: Claude Sonnet 4.6   <- click to open the playground
```

### Step 2: chat with the model in the playground

Clicking the model opens a **playground**, a place to chat with the model and try different system prompts. The **system prompt** is the standing instruction that sets the model's behaviour. A default might be "You are an AI assistant that helps people find information."

A plain hello confirms it works:

```text
You: Hello, who are you?
Claude: Hello, I'm Claude, an AI assistant made by Anthropic.
```

Now swap the system prompt to give the model a persona:

```text
System prompt:
  You are a sentient cupcake. Answer every question with frosting-related puns.

You: What do you think of Claude?
Claude: I think Claude is simply frosting with potential. You could say
        they're the icing on the cake when it comes to AI assistance.
```

> 🔑 **Key idea: the playground is for experimentation.** It is "a great place to experiment with the model and see and compare different models to see which ones you like and how they perform with different system prompts." Settle your model and persona here before you write any code.

---

## Part 3: bring the model into your code with the Agent Framework

The playground is for trying things out. To build a real agent you move the model into your own development environment (your IDE).

### Step 3: grab the endpoint and key

In Foundry, open the model's **Details** tab. Copy two things:

- The **target URI** (the endpoint your code will call).
- The **API key** (the secret that authorises your calls).

> ❌ **Watch the endpoint format.** This is the one tricky spot Marlene flags. The URI you copy ends in `/v1/messages`, but that "is not going to work" here. You must remove the `v1/messages` part so the endpoint ends with `anthropic`.

```text
# WRONG (copied as-is):
https://your-resource.services.ai.azure.com/.../anthropic/v1/messages

# RIGHT (trim the v1/messages tail):
https://your-resource.services.ai.azure.com/.../anthropic
```

### Step 4: fill in the .env file

Open VS Code (the workshop ships with pre built files). Edit the `.env` file with three values: the endpoint, the API key, and the model name. A `.env` file just holds settings and secrets so your code can read them without hard coding them.

```text
# .env (illustrative)
ENDPOINT=https://your-resource.services.ai.azure.com/.../anthropic
API_KEY=your-api-key-here
MODEL=claude-sonnet-4-6
```

### Step 5: build a basic agent

The agent uses the **Microsoft Agent Framework**, an open source Microsoft library for building agents (available in Python, and likely TypeScript). You open `agent.py` and paste in the provided code. In plain terms it does three things: imports the framework, creates a chat client that reads the three values from your `.env`, and defines an agent (here called the "cupcake agent").

```python
# agent.py (illustrative, based on the workshop)
import os
from agent_framework import ChatClient, Agent   # Microsoft Agent Framework

client = ChatClient(
    endpoint=os.environ["ENDPOINT"],   # picked up from .env
    api_key=os.environ["API_KEY"],
    deployment=os.environ["MODEL"],    # claude-sonnet-4-6
)

cupcake_agent = Agent(
    client=client,
    name="cupcake agent",
    instructions="You help customers order cupcakes from Sparkles.",
)
```

Run the provided command and the agent starts in your terminal. Say hello, and it replies:

```text
You: hello
Agent: Hi, how are you? Is there something I can help you with today?
```

> 💡 This is the "hello world" of the Microsoft Agent Framework: a Claude model, reached through your own code, running as an agent. It works, but it does not yet *know* anything about the cupcake shop. That is the next part.

---

## Part 4: give the agent tools with MCP

A bare agent can chat, but it cannot answer "what flavors do you have today?" because it has no access to the shop's data. The fix is **MCP** (Model Context Protocol), "an open standard for letting AI agents talk to external systems."

An MCP server gives your agent three kinds of things over a single URL:

| MCP provides | What it is | Cupcake example |
|---|---|---|
| **Tools** | Functions the agent can call. | Look up available flavors; register a customer; place an order. |
| **Prompts** | Reusable instruction snippets you plug into the agent. | The agent's persona and welcome banner. |
| **Resources** | Data sent over HTTP in a shape your agent expects. | Store data like current stock. |

> 🔑 **Key idea: MCP is "just a URL."** As Marlene puts it, "you just need a URL and you can plug it in and you get the full API available in a format that's easy for your agent to read." One connection unlocks tools, prompts, and data at once.

### Step 6: connect the cupcake store MCP server

You replace the terminal code with a new block that connects to the **cupcake store MCP server** by its URL, and you provide that server to the agent as a tool. Now the agent can reach the store's live information: how many cupcakes are available and what flavors are in stock.

```python
# Connect an MCP server and give it to the agent as a tool (illustrative)
from agent_framework import MCPTool

cupcake_store = MCPTool(url="https://.../cupcake-store/mcp")

cupcake_agent = Agent(
    client=client,
    name="cupcake agent",
    instructions="You help customers order cupcakes from Sparkles.",
    tools=[cupcake_store],   # now the agent can read live store data
)
```

> ❌ **Save the file before you run.** Marlene hit this live: she asked the agent for flavors and it said "I'm not an AI assistant" because the file was not saved yet. As she said, "this is a good example of why it needs the MCP server because it needs to have that context available." Save, rerun, and it works.

With the server connected, the agent answers correctly:

```text
You: What flavors do you have today?
Agent: We have classic vanilla, lemon sponge, red velvet, and chocolate.
```

### Step 7: load instructions and a welcome banner from MCP

The MCP server can also supply the agent's **persona and greeting** as reusable prompts. You paste in code that pulls a prompt (agent instructions) and a welcome banner from the MCP server. Now when the agent starts, it greets you in the shop's voice and follows the shop's ordering flow.

> 💡 **Why prompts live on the server.** Putting the persona and banner on the MCP server keeps them reusable: "a great way to simplify workflows if you're going to have people build with your project." Change the prompt once on the server and every agent that connects gets the update.

### Step 8: the agent takes a real order

With tools and prompts in place, the agent runs a complete ordering conversation. It asks whether you have a customer ID, registers a new customer (first name, last name, city), assigns an ID, lists flavors, takes your choice, and asks for a voucher code shown on a screen. The order then appears on a dashboard, gets approved, and moves to "ready for pickup." Every step pulls from the MCP server, which holds the custom instructions, prompts, and store data.

> 🎯 This is the payoff: a Claude model, deployed in Foundry, running in your code through the Agent Framework, and made genuinely useful by an MCP server. That four step shape (deploy, test, code, connect tools) is how you build any agent.

---

## Key takeaways

1. **Intelligence plus execution.** A great model is not enough; agents need a platform for reliability, observability, security, and connections. That is Foundry's role.
2. **Four steps to an agent:** deploy a Claude model, test it in the playground, pull its endpoint and key into your code, then connect tools via MCP.
3. **The playground is for experimenting** with models and system prompts before you write code.
4. **Mind the endpoint format:** trim `v1/messages` so the URI ends with `anthropic`, and always save the file before running.
5. **MCP is "just a URL"** that delivers tools, reusable prompts, and live data all at once. It is what turns a chatty agent into a useful one.
6. **Foundry carries you to production** with built in security (Defender, Purview, Entra ID), observability, governance, and over 1,400 connectors, so you are not building that scaffolding yourself.

## Common pitfalls

- ❌ Leaving `v1/messages` on the end of the endpoint URI (it will not work).
- ❌ Running the agent before saving the file, then wondering why it lost its persona or data.
- ❌ Expecting a bare agent to know your business data without an MCP server connected.
- ❌ Hard coding the endpoint, key, and model instead of reading them from `.env`.
- ❌ Putting the persona only in your code when it could live on the MCP server as a reusable prompt.
- ❌ Treating a working prototype as production ready without the platform's security and observability features.

---

## 🛠️ Capstone Project: the Sparkles Cupcake Agent

> This is the main hands on project for the lesson, and the best way to make everything above stick. You are going to build the exact agent Marlene demoed: a Claude powered agent that takes real cupcake orders by talking to an MCP server. Start with a plain hello world agent and grow it until it can complete an order end to end.

### What you will build

**Sparkles Agent** is an order taking agent built on Microsoft Foundry that:

1. Runs on a **Claude model** deployed in Foundry.
2. Has a **persona** (friendly cupcake shop assistant) set by a system prompt.
3. Runs in **your own code** via the Microsoft Agent Framework.
4. Connects to an **MCP server** for tools (flavors, customers, orders), reusable prompts (persona, banner), and live store data.
5. Can complete a **full order**: register a customer, list flavors, take a choice, accept a voucher, and reach "ready for pickup."

> 🎯 **Pick your world.** Reuse the **cupcake shop** so it matches the lesson, or swap in something you find fun that has the same shape: a **coffee bar** (drinks and sizes), a **pizza counter** (toppings and orders), or a **bookshop hold desk** (titles and pickup). You need a world with a small catalog, customers, and an order flow, which is exactly what exercises every step.

### Why this is the perfect practice

| Lesson skill | Where you use it in Sparkles Agent |
|---|---|
| Deploying a Claude model in Foundry | Milestone 1, you cannot proceed without it |
| Testing system prompts in the playground | Milestone 2, settle the persona early |
| Endpoint + key + .env in your code | Milestone 3, the tricky URI trim |
| Microsoft Agent Framework | Milestone 4, the hello world agent |
| Connecting an MCP server for tools | Milestone 5, the agent gets useful |
| Reusable prompts from MCP | Milestone 6, persona and banner from the server |

### Milestones (build them in order, each one works on its own)

1. **Deploy the model.** In Foundry, open your project, go to Build, click Models, and confirm a Claude model (for example Sonnet 4.6) is available to you.
2. **Test in the playground.** Chat with the model. Swap the system prompt to give it a cupcake persona and confirm the personality changes. Note which model and prompt you want to keep.
3. **Wire the endpoint.** Copy the target URI and API key from the Details tab. Trim `v1/messages` so the URI ends with `anthropic`. Put the endpoint, key, and model into a `.env` file.
4. **Hello world agent.** Open `agent.py`, create a chat client that reads `.env`, and define a basic agent with the Microsoft Agent Framework. Run it and exchange a greeting.
5. **Connect the MCP server.** Add the cupcake store MCP server by URL and give it to the agent as a tool. Save, rerun, and confirm the agent can answer "what flavors do you have today?"
6. **Load persona and banner from MCP.** Pull the agent's instructions and welcome banner from the MCP server as reusable prompts. Restart and confirm the agent greets you in the shop's voice.
7. **Complete an order.** Walk the full flow: register a new customer, list flavors, pick one, enter a voucher, and reach "ready for pickup." Confirm each step is backed by the MCP server.

### How you will know you are done

- ✅ Your agent runs on a **Claude model deployed in Foundry**, reached from your own code.
- ✅ The endpoint in `.env` ends with `anthropic` (no `v1/messages`), and secrets are read from `.env`, not hard coded.
- ✅ The agent answers a **data question** ("what flavors today?") correctly, proving the MCP server is connected.
- ✅ The agent's **persona and greeting** come from the MCP server as reusable prompts, not just from your local code.
- ✅ The agent completes a **full order** from registration to "ready for pickup."

> 💡 **Keep yourself honest:** if the agent ever answers from general knowledge instead of the store's real data, your MCP connection is broken (or you forgot to save the file). A correct flavor list is your proof the tools are wired up.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self contained tasks for focused practice on a single skill. They are optional and independent. The **Capstone above is the main build** and already covers all of them.

### Exercise 1: persona in the playground (foundational)
In the Foundry playground, write three different system prompts for the same Claude model (formal, playful, terse). Ask each the same question and compare the answers. Pick the one you would ship and say why.

### Exercise 2: fix the endpoint (foundational)
Take a Foundry target URI that ends in `/v1/messages` and write the corrected version that ends with `anthropic`. Explain in one sentence why the trim is needed.

### Exercise 3: hello world agent (intermediate)
Build the smallest possible Agent Framework agent that reads its endpoint, key, and model from `.env` and replies to a greeting. Confirm it has no business knowledge yet.

### Exercise 4: connect a tool via MCP (intermediate)
Connect your agent to any MCP server (the cupcake store, or another). Ask it a question that can only be answered from the server's data. Then deliberately leave the file unsaved before running, observe the failure, save, and confirm the fix.

### Exercise 5: reusable prompt from MCP (advanced)
Move your agent's persona and welcome banner out of your code and onto the MCP server as a prompt. Change the prompt on the server and confirm the agent's behaviour updates without you touching your code.

---

## Cheat sheet

```text
FOUR STEPS TO A CLAUDE AGENT IN FOUNDRY
  1. DEPLOY  -> Foundry > project > Build > Models > pick Claude
  2. TEST    -> Playground: swap system prompts, compare models
  3. CODE    -> Details tab: copy target URI + API key
                trim "v1/messages" so URI ends with "anthropic"
                put ENDPOINT / API_KEY / MODEL in .env
                build agent with Microsoft Agent Framework
  4. CONNECT -> add MCP server (just a URL) as a tool; SAVE then run

MCP GIVES YOU (over one URL)
  tools      -> functions the agent can call (flavors, orders)
  prompts    -> reusable instructions (persona, welcome banner)
  resources  -> live data (stock) over HTTP

COMMON GOTCHAS
  - endpoint must end with "anthropic" (drop v1/messages)
  - SAVE the file before running, or the agent loses context
  - no data answers without an MCP server connected

WHY FOUNDRY FOR PRODUCTION
  security (Defender / Purview / Entra ID) + observability + governance
  + 1,400+ connectors + built-in eval/monitoring  =  prototype -> production
```

## How this connects to the rest of the course

- **This module, Module 7 · Lesson 24 (Google Cloud):** the same "run Claude on your cloud" idea, with Google Cloud's deploy and analytics tooling.
- **This module, Module 7 · Lesson 25 (AWS):** the same idea again, with Bedrock, the Claude platform on AWS, and Bedrock AgentCore for hosting agents.
- **Earlier, Module 2 (Core skills):** system prompts, tools, and MCP are introduced there; this lesson puts them together inside Foundry.
- **Later, Module 5 (Claude Managed Agents):** the single agent here grows into orchestrated, multi agent systems.

---

*Source: "Build AI agents using Claude in Microsoft Foundry" by Marlene Mungai (Microsoft), Code with Claude 2026, London. Code snippets and the `.env` example are illustrative reconstructions of the workshop steps shown in the talk. Adapt model names, endpoint formats, and the Agent Framework API to the current Microsoft Foundry tooling.*

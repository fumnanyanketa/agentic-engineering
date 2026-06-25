# Unit 4: Tools, Function-Calling and MCP

> **Course:** Agentic Engineering with Claude, a self-paced path *(working title)*
> **Unit 4 of 11:** How a model stops just talking and starts acting, through well-designed tools and the shared MCP standard, the Claude way
> **Sources fused:** Agentic Engineering Modules 04 and 09 (principles) + Building with Claude Lesson 14 and the tool-search part of Lesson 6 (implementation)
> **Estimated time:** 90 to 120 minutes (read plus the build)

---

## In one sentence

A plain model can only produce text, so this unit gives it hands: you learn the tool-use loop (the model asks for an action by name, your code runs it, the result goes back), you learn to design tools so the model uses them reliably (clear descriptions, consolidated actions, errors returned not hidden), you connect to the outside world once and reuse it everywhere through MCP (the open standard that turns N times M custom connectors into N plus M), and you keep a growing tool catalog usable with tool search.

> 🎯 **Where this unit is heading.** The payoff is a **Build**: the AtlasOS tool / MCP layer. You give Scout (the research agent) real tools behind clean function schemas, connect at least one MCP server so an integration is built once and reused, and add tool search so the catalog can grow without drowning the context window. You finish with a committed tool layer, clear schemas, and one MCP integration. Jump to **"The Build"** to see the finish line.

## First-principles companion

> 💡 **The durable ideas behind this unit.** The Claude-specific framing is recent; the concepts are not. For the timeless versions:
>
> - **[Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761)** (paper). The seminal account of why and how a language model calls external tools and APIs, the root of everything in this unit.
> - **[Tool use with Claude (Anthropic docs)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)** (docs). The tool-agnostic explanation of the loop: the model decides, your app executes, the result returns.
> - **[Model Context Protocol intro](https://modelcontextprotocol.io/docs/getting-started/intro)** (docs). MCP as an open, vendor-neutral standard ("the USB-C port for AI applications"), now stewarded by a foundation, not one company.

## A few plain-language basics first

- **Tool (also function calling):** a named action you let the model take (search the web, query a database, send an email, run code). "Function calling" is the older programming phrase; "tool use" is the newer one most teams prefer. Same idea.
- **Schema:** a precise description of the shape of some data. A tool's input schema lists the inputs it needs and their types, usually written in **JSON Schema** (a standard text format for structured data).
- **Tool call:** the model's structured request to run a tool. The model only *asks*; it never runs anything itself.
- **Tool result:** what your code sends back after running the tool, attached to the same conversation, so the model can continue.
- **MCP (Model Context Protocol):** an open standard for connecting AI apps to tools and data, so you build a connector once and any compliant app can reuse it.
- **MCP server / client / host:** the **host** is the AI app you use; the **client** lives inside it and holds a connection to a **server**, a small program that exposes tools and data in the MCP format.

You do not need to memorise these. Each returns the first time it matters.

## Why this unit matters

In Unit 0 you met the four parts of the workplace you design for the model: instructions, context, tools, and validation. This is the tools unit, and it is where an LLM stops being a clever text box and starts changing the world. A model on its own cannot look up today's weather, read a file, or add two large numbers with guaranteed accuracy. Tools fix that.

> 🔑 **Your agent is not dumb, your tools are.** Beginners assume a weak agent means a weak model. Far more often the tools are the problem. The model can only be as good as the menu you hand it. Anthropic's engineering team reported spending more time tuning the tools than the prompt for one of their coding agents.

Get tool design right and even a modest model acts reliably. Get it wrong and the strongest model in the world picks the wrong action, floods its own context with noise, and stalls. And once you have more than a handful of tools, you need a way to connect them once (MCP) and to keep them usable as the list grows (tool search). Those are the two scaling moves this unit adds on top of the basic loop.

## Learning objectives

By the end of this unit you will be able to:

1. Walk through the tool-use loop step by step and explain who decides *what* (the model) versus *how* (your code).
2. Write a tool as three things (name, description, JSON Schema) and apply the design rules: consolidate, namespace, return high-signal output, name fields for the model.
3. Return errors as recoverable tool results so the model self-corrects, and treat every tool input as untrusted.
4. Explain MCP, the N times M to N plus M payoff, the client/server/host pieces, and the three server primitives (tools, resources, prompts).
5. Use tool search to keep a large tool catalog from flooding the context window.
6. Give a Claude agent real tools and at least one MCP server, committed to AtlasOS.

## Prerequisites

- **From this course:** Unit 0 (the four-part workplace; tokens and the context window) and Unit 2 (prompting and context engineering; tool search was previewed there).
- **Skills that matter:** reading and running Python, calling an HTTP API, and reading JSON. You will write small functions and one schema.
- **Skills you can defer:** building production MCP servers and deep security hardening. You wire up one server here; safety in depth is its own later topic.

---

## Part 1: the tool-use loop (the model asks, your code acts)

This is the single most important idea in the unit, so we walk it slowly. A user asks, "What is the weather in Paris?"

1. You send the user's message *plus* your tool definitions to the model.
2. The model does not answer directly. It returns a **tool call**: a structured request that says, in effect, "please run `get_weather` with `city = "Paris"`." Note that the model does not run anything. It only asks.
3. Your code reads that request, runs the real `get_weather` function (which calls a weather service), and gets back, say, `18C and cloudy`.
4. You send that back as a **tool result**, attached to the same conversation.
5. Now the model has the fact it needed, so it writes the final answer: "It is 18 degrees Celsius and cloudy in Paris."

> 🔑 **The model and your code take turns.** The model decides *what* to do; your code decides *how* to do it. A model may chain several tool calls in a row before answering, looping through steps 2 to 4 multiple times. This back-and-forth is the heart of every agent you will build later.

A tool is just three things bundled together: a **name** (`get_weather`) the model refers to it by; a **description** in plain English that says what it does and when to use it (the most underrated part, read the way a new hire reads a one-line job description); and a **schema** listing its inputs and outputs.

```json
{
  "name": "get_weather",
  "description": "Get the current weather for a city. Use this whenever the user asks about current conditions or temperature in a place.",
  "input_schema": {
    "type": "object",
    "properties": {
      "city":  { "type": "string", "description": "City name, e.g. 'Paris'" },
      "units": { "type": "string", "enum": ["celsius", "fahrenheit"], "default": "celsius" }
    },
    "required": ["city"]
  }
}
```

> ❌ **Errors are results, not crashes.** When a tool fails (service down, city misspelled), do not let your program crash and do not silently hide it. Send the error back as a clearly marked tool result, for example `"Error: no city named 'Pariss' found. Did you mean 'Paris'?"` A capable model usually corrects itself and tries again. Swallow the error and the model is left guessing.

---

## Part 2: tool design (as important as the prompt)

The model can only be as good as the menu you hand it, so design the menu for how the model thinks, not for how your backend happens to be structured. Anthropic recommends designing tools to be **poka-yoke**, a manufacturing term meaning "mistake-proof": shape the inputs so the easy path is the correct path and wrong calls are hard to make. A few durable rules hold across every provider:

- **Consolidate, do not mirror your database.** One well-named `schedule_meeting` tool beats three thin tools (`list_users`, `list_calendars`, `create_event`) that force the model to orchestrate them by hand. More tools is not better; each extra tool is one more thing the model can pick wrongly.
- **Namespace your tool names** so they read clearly, like `github_list_pull_requests` or `stripe_create_refund`. This helps the model tell similar tools apart.
- **Return high-signal output.** Give back human-readable identifiers rather than long random codes, and paginate, filter, or trim large results. Every token you return competes for the model's limited attention and costs money.
- **Name fields for the model, not your backend.** Call it `customer_email`, not `cust_eml_2`. The model reads these names as hints.

Two settings show up under different names across providers but mean the same thing. **Tool choice** controls whether the model *may* call a tool, *must* call some tool, or must call one *specific* tool (use "must call a tool" when an answer without one would be useless, like a lookup assistant that should never guess). **Strict schema validation** forces the model's inputs to match your schema exactly. Research and provider docs agree that argument correctness, not the number of tools, is what makes or breaks reliability, so turning on strict validation where it is offered is usually worth it.

> ❌ **A tool is a door into your systems.** Treat every input the model sends to a tool as untrusted, and validate and limit it at the tool itself. Never rely on the prompt alone to keep the model in bounds. Prompt injection (tricking the model into misusing a tool) is a leading risk, so enforce limits in code. (Covered in depth in a later safety unit.)

> ✅ **The test before the loop.** Test each tool on its own before wiring it in, so you know failures come from the model's choices, not from a broken tool.

---

## Part 3: MCP (build the connector once, reuse it everywhere)

You can now hand a model tools. The next problem is practical: every time you connect a model to a new tool or data source, you write custom plumbing. **MCP**, the Model Context Protocol, fixes that by defining one shared way to make those connections, so the work is reusable across tools and across platforms. A common analogy: MCP is "the USB-C port for AI applications." Any compatible app plugs into any compatible tool. It was donated to a vendor-neutral foundation, so treat it like an open web standard, a protocol many vendors implement, not one company's product.

> 🔑 **N times M becomes N plus M.** With N apps and M tools and no standard, you build a custom connector for every pairing: 10 apps and 10 tools means 100 connectors. With MCP, each app speaks MCP once and each tool is wrapped as a server once. Build one server, and every MCP client can use it.

MCP follows a **client-server** design. A **host** is the AI app you use (a desktop chat app, a code editor, an IDE). Inside it runs an MCP **client** holding a connection to a **server**, a small program that exposes capabilities in the MCP format. The two sides talk over JSON-RPC 2.0 (a lightweight request/reply format written in JSON); you only need to know it is the agreed wire format. A server can offer three **primitives** (the basic building blocks):

- **Tools:** functions the model can call to take an action, like "send an email" or "run a query." The executable abilities.
- **Resources:** structured data the model can read into its context, like a file's contents or a database record.
- **Prompts:** reusable prompt templates or canned workflows a user or app can pull in on demand.

In a Claude agent (for example a Claude Managed Agent, where the agent's brain holds its model, system prompt, tools, and MCP servers), you attach MCP servers right alongside the agent's plain tools and skills. Connecting an existing server typically looks like one config block naming the server and how to launch it:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/atlas/data"]
    }
  }
}
```

> ✅ **Same naming rules, new surface.** Give every server tool a clear description and sensible name, exactly as in Part 2. And treat tool descriptions from any server as untrusted input, because that text enters your model's context. A malicious server can try to manipulate your agent (tool poisoning), so do not trust third-party servers blindly.

---

## Part 4: keeping a growing catalog usable (tool search)

Real agents use a lot of tools, sometimes tens or hundreds, and each tool's schema costs tokens. When you define them all and pass them to the model, those definitions fill the context window, leaving less room for the actual work. In one Claude demo a single retention-metrics tool schema was 14,000 tokens, a list tool 6,100, another 9,300. That is space gone before the task even starts.

**Tool search** fixes this. You still define all your tools up front, but the model is handed only a single search tool. When it thinks it needs a tool, it calls the search, gets a short list, and *only then* is the chosen tool's full definition loaded into context.

> 💡 **A real result.** Lovable used tool search and cut overall token consumption by about 10 percent, and the model's performance actually *improved*, because less clutter in context means the model performs better. They rolled it out to all users.

This is the same lesson as Part 2's "return high-signal output," applied one level up: protect the context window not just on what tools *return* but on which tool *definitions* even load. Tool search is what lets the AtlasOS catalog grow past a handful of tools without each new tool taxing every request.

> 🔑 **Two scaling moves, two problems.** MCP solves *integration* sprawl (build the connector once). Tool search solves *context* sprawl (load only the tool you need). You want both the moment your fleet has more than a few tools and more than one data source.

---

## Key takeaways

1. **The loop is turn-taking.** The model asks for an action by name; your code runs it and returns the result; repeat until the model answers. Model decides *what*, code decides *how*.
2. **A tool is name + description + schema.** The description and field names are written for the model, not your backend.
3. **Tool design rivals the prompt.** Consolidate, namespace, return high-signal output, validate strictly. Your agent is not dumb, your tools are.
4. **Errors are results.** Return clear, recoverable error messages so the model self-corrects. Treat every tool input as untrusted and limit it in code.
5. **MCP turns N times M into N plus M.** An open standard; build a server once, every client reuses it. Three primitives: tools, resources, prompts.
6. **Tool search protects the context window** as the catalog grows: load only the tool you need, not every schema.

## Common pitfalls

- ❌ Exposing dozens of thin tools that each do one tiny database operation, instead of a few consolidated ones.
- ❌ Cryptic tool output that floods the context window with noise.
- ❌ Hiding errors instead of returning them, leaving the model no way to recover.
- ❌ Trusting the prompt to keep a tool safe instead of validating inputs in code.
- ❌ Rebuilding bespoke one-off integrations for things MCP already standardizes.
- ❌ Trusting a third-party MCP server blindly, when its tool descriptions flow straight into your model's context.
- ❌ Loading every tool's full schema up front instead of using tool search.

---

## 🛠️ The Build: the AtlasOS tool / MCP layer

> The hands-on payoff. You give Scout (the research agent) real hands. You design a few clean tools, connect at least one MCP server so an integration is built once and reused, and add tool search so the catalog stays usable as it grows. Everything lands in `atlas/tools/` and is committed.

### What you will build

A tool layer for Scout, proven by three artifacts: two or three well-designed tools behind clear JSON schemas (one deliberately failing, to watch the model recover), one connected MCP server called from the agent, and tool search switched on so only the needed tool loads into context.

### Milestones (in order, each stands alone)

1. **Two good tools, the raw loop.** Give Scout two or three real tools (for example a `web_search`, a `calculator`, and a small `lookup_source` over local JSON). Write the full loop yourself with the raw provider request, no framework hiding the turn-taking, and watch the model call them. Commit under `atlas/tools/`.
2. **Break one on purpose, then fix it.** Make one tool deliberately bad (vague description, cryptic field names, a giant unfiltered result). Watch the model stumble. Then apply the Part 2 rules (clear description, clear names, trimmed output) and watch behavior improve. Write two sentences on what changed.
3. **Errors as results.** Force one tool to fail (wrong input, service down) and return the failure as a clearly marked tool result. Confirm Scout reads the error and self-corrects rather than crashing or guessing.
4. **Connect one MCP server.** Wire up a pre-built MCP server (a filesystem or a database server is a good first pick) and call it from Scout. You now have one integration built to the standard, reusable by any MCP client, not bespoke glue.
5. **Add tool search.** Hand Scout a single search tool instead of every schema up front. Confirm only the chosen tool's definition loads into context, and note the token reduction. This is what lets the catalog grow.
6. **Stretch.** Write a minimal MCP server of your own that exposes one tool and one resource, then call it from Scout, so you understand both sides of the protocol. Optionally namespace your tools (`scout_*`) and turn on strict schema validation.

### How you will know you are done

- ✅ Scout chooses correctly among several tools and calls them with valid inputs.
- ✅ Your once-bad tool, after the fix, is used cleanly, and you can describe the behavior change.
- ✅ A forced tool failure returns as a tool result and Scout recovers.
- ✅ At least one MCP server is connected and called from the agent.
- ✅ Tool search loads only the needed tool, and you can point to the token reduction.
- ✅ The tool layer is committed to `atlas/tools/` with clear schemas.

> 💡 If the model ever picks the wrong tool, re-read its transcript before adding instructions. The fix is almost always a clearer description or a consolidated tool, not a longer prompt.

---

## Cheat sheet

```text
THE TOOL-USE LOOP
  send message + tool defs -> model returns a TOOL CALL (asks, doesn't run)
  your code runs it -> send TOOL RESULT back -> model answers (may loop)
  model decides WHAT · your code decides HOW

A TOOL = name + description + schema (JSON Schema)
  description & field names are written FOR THE MODEL, not your backend

TOOL DESIGN RULES
  consolidate (not 1 tool per DB call) · namespace names · high-signal output
  errors -> return as recoverable tool RESULT · inputs are UNTRUSTED, limit in code
  tool choice (may/must/specific) · strict schema validation

MCP (build once, reuse everywhere)
  N x M connectors -> N + M ; host -> client -> server (JSON-RPC 2.0)
  three server primitives: TOOLS · RESOURCES · PROMPTS
  open standard, foundation-stewarded · third-party server descriptions = untrusted

SCALING A CATALOG
  tool search -> load only the tool you need, not every schema
  MCP = integration sprawl ; tool search = context sprawl
```

## How this connects to the rest of the course

- **Earlier, Unit 2 (Prompting and context):** tool search was previewed there as a context-engineering lever; here you design the tools it searches over.
- **Next, Unit 5 (Retrieval and memory):** Scout's `lookup_source` tool grows into real retrieval, and you wrap that retrieval tool as an MCP server for Cortex (the shared memory).
- **Later, Unit 7 (Multi-agent orchestration):** the tool layer you built is what every agent in the fleet inherits; Atlas dispatches agents that already have hands.
- **Throughout:** every AtlasOS agent acts on the world through this layer. Scout is the first to get hands; the rest reuse the same patterns and the same MCP servers.

---

*Unit 4 of the combined path. Fuses the vendor-neutral principles of Agentic Engineering Modules 04 and 09 with the Claude-specific implementation of Building with Claude (Lesson 14 and the tool-search part of Lesson 6). Code snippets are illustrative; adapt model ids, schema fields, and SDK details to the current docs.*

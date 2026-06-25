# Unit 4: Tools, Function-Calling and MCP

> **Course:** Agentic Engineering, a model-agnostic self-paced path *(working title)*
> **Unit 4 of 11:** Teach a model to actually *do* things: describe a tool as a JSON schema, let the model ask to call it, run it, and return the result, then plug whole toolboxes into your coding agent with one standard, MCP
> **Principle (vendor-neutral):** Agentic Engineering Module 4 (Tool use / function calling) and Module 9 (MCP)
> **The how, across tools/models:** function calling across Claude (Anthropic), Gemini (Google), and GPT (OpenAI); MCP across Claude Code, Gemini CLI, and Codex CLI, current practice verified June 2026
> **AtlasOS build:** your `tools/` layer, one real hand-written tool the model can call, plus one MCP server connected to your coding agent
> **Estimated time:** 90 to 120 minutes

---

## In one sentence

A bare language model can only produce text, and this unit gives it hands: you will learn the one universal pattern that lets any model (Claude, Gemini, or GPT) call your code (you describe a tool as a JSON schema, the model returns a structured request, you run it and hand back the result, the model continues), you will see that exact shape side by side across all three providers, and then you will learn MCP, the open standard that lets you plug a whole toolbox into any agent once instead of rewiring it for every tool, finishing by building the `tools/` layer of AtlasOS with a real tool and a real MCP server wired into your coding agent.

> 🎯 **Where this unit is heading.** The payoff is a **Build** where you create the `tools/` folder in your AtlasOS repo, hand-write one real tool (a small file-search tool) as a JSON-schema function, run the full tool-use loop yourself so you watch the model actually call it, and then connect one MCP server to your coding agent (Claude Code, Gemini CLI, or Codex CLI) and confirm the agent invokes it. Jump to **"The Build"** to see the finish line, then come back and we will get you there.

## First-principles companion

> 💡 **The durable ideas behind this unit.** The APIs and CLIs are recent and change often; the underlying ideas do not. If you want the timeless versions (optional, read them any time):
>
> - **[Tool use with Claude (Anthropic docs)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)** (docs). The tool-agnostic explanation of the function-calling / agentic loop: the model decides, your app executes, the result returns.
> - **[Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761)** (paper). The seminal paper on why and how language models call external tools and APIs.
> - **[Writing tools for agents (Anthropic)](https://www.anthropic.com/engineering/writing-tools-for-agents)** (essay). The durable rules of good tool design (consolidate, namespace, return high-signal output) that hold across every provider.
> - **[Model Context Protocol: intro docs](https://modelcontextprotocol.io/docs/getting-started/intro)** (docs). The vendor-neutral standard for connecting agents to tools and data, from the source.

## A few plain-language basics first

New terms, in plain words. You do not need to memorise these; each is explained again the moment it matters.

- **Tool (also called a function):** a small piece of your code the model is allowed to run, for example "search files" or "get the weather." The two names mean the same thing; we say "tool."
- **Function calling / tool use:** the mechanism by which a model asks to run one of your tools. It does not run anything itself; it returns a structured request and waits for you.
- **JSON:** JavaScript Object Notation, a simple text format for structured data, written with `{ }` for objects and `"key": value` pairs. You have seen it even if you did not know the name.
- **JSON Schema:** a precise, machine-readable description of the *shape* of some data: which fields exist, their types, and which are required. You describe each tool's inputs with one.
- **Tool definition:** the bundle you hand the model for each tool: a **name**, a plain-English **description**, and an **input schema**.
- **Tool call:** the structured request the model returns, naming a tool and the arguments to run it with.
- **Tool result:** what you send back to the model after running the tool, attached to the same conversation, so the model can continue.
- **The tool-use loop:** send tools plus the user message, get a tool call, run it, return the result, repeat until the model answers. This is the heartbeat of every agent.
- **MCP (Model Context Protocol):** an open, vendor-neutral standard for connecting tools and data to *any* agent, so you build an integration once and every compatible agent can use it.
- **MCP server:** a small program that exposes tools (and data) in the MCP format. **MCP client / host:** the agent or app that connects to it.
- **Coding agent:** the terminal tool you set up in Unit 1 (Claude Code, Gemini CLI, or Codex CLI). It is itself an MCP client, so you can plug MCP servers straight into it.

## Why this unit matters

Everything you build from here on, every AtlasOS agent, depends on this one capability. A model that can only talk is a clever parrot. A model that can call tools can search, read files, query a database, send a message, run code: it can act. Function calling is the single mechanism underneath all of it, and MCP is how you stop rewriting the same plumbing for every new tool.

> 🔑 **The model decides *what*; your code decides *how*.** The model never runs anything. It reads your tool menu, picks one, and asks for it by name with arguments. Your code runs the real action and returns the result. This turn-taking is the entire idea, and it is identical across every provider.

## Learning objectives

By the end of this unit you will be able to:

1. Explain the tool-use loop step by step, and why a tool is just a name, a description, and a JSON schema.
2. Write a tool definition and recognise the same shape in Claude, Gemini, and GPT requests.
3. Design tools the model uses reliably (good names, clear descriptions, trimmed output, errors as results).
4. Explain what MCP is, the N times M problem it solves, and its client/server/host parts and three primitives.
5. Add an MCP server to a coding agent in Claude Code, Gemini CLI, and Codex CLI, and verify the agent invokes it.
6. Build the AtlasOS `tools/` layer: one real hand-written tool plus one connected MCP server.

## Prerequisites

- **Unit 1 finished:** you have a workstation (VS Code, terminal, Node.js, git), a coding agent installed and signed in, and the `atlasos` repository cloned to your computer. We build directly on that.
- **Helpful, not required:** Unit 2 (prompting) and Unit 3 (context engineering). Tool descriptions are prompts, so good prompting habits carry straight over.
- **What you do NOT need:** prior experience with APIs or JSON. We define every term and show every line.

---

## Part 1: What a tool actually is

A plain language model can do exactly one thing: produce text. It cannot look up today's weather, read a file on your disk, or add two large numbers with guaranteed accuracy. **Tool use** (the same thing the older programming world calls **function calling**) fixes that. You give the model a menu of actions it is allowed to take, and when it decides an action would help, it asks for that action by name. Your code runs the action and hands the result back. The model then continues with that fresh information.

A tool is just three things bundled together:

- A **name**, such as `get_weather`. The model uses this to refer to the tool.
- A **description** in plain English that tells the model what the tool does and when to use it. This is the most underrated part. The model reads it the way a new employee reads a one-line job description, so write it carefully.
- An **input schema**, a structured list (in **JSON Schema**) of the inputs the tool needs. For `get_weather` the schema might say it needs a `city` (text) and an optional `units` (either `"celsius"` or `"fahrenheit"`).

Here is what one tool definition looks like, written out. Read it slowly; every provider uses a version of this same shape.

```text
# One tool definition: name + description + JSON-Schema inputs.
{
  "name": "get_weather",
  "description": "Get the current weather for a city. Use when the user asks
                  about weather, temperature, or conditions in a place.",
  "input_schema": {
    "type": "object",
    "properties": {
      "city":  { "type": "string", "description": "City name, e.g. 'Paris'" },
      "units": { "type": "string", "enum": ["celsius", "fahrenheit"],
                 "description": "Temperature units. Defaults to celsius." }
    },
    "required": ["city"]
  }
}
```

That is the whole bundle. `"type": "object"` says the inputs are a set of named fields; `properties` lists them; `required` says which the model must provide. The `enum` pins `units` to one of two exact values so the model cannot invent a third. You hand this definition to the model along with the user's message, and you are ready to run the loop.

> 🔑 **The description is half the tool.** The model cannot see your code, only the name, the description, and the field names. Those text hints are how it decides when and how to call the tool. A vague description is the single most common reason a model "ignores" a tool you gave it.

---

## Part 2: The tool-use loop, step by step

This is the most important idea in the unit, so we walk it slowly. Imagine a user asks: *"What is the weather in Paris?"*

```text
   USER: "What is the weather in Paris?"
        │
        ▼
   1. YOU send: user message + tool definitions  ──────────▶  MODEL
                                                                │
   2. MODEL returns a TOOL CALL (it does NOT run anything):    │
      { call get_weather, city: "Paris" }   ◀──────────────────┘
        │
        ▼
   3. YOUR CODE runs the real get_weather("Paris") -> "18C, cloudy"
        │
        ▼
   4. YOU send the TOOL RESULT back ("18C, cloudy")  ─────────▶  MODEL
                                                                │
   5. MODEL writes the final answer:  ◀──────────────────────────┘
      "It is 18 degrees Celsius and cloudy in Paris."
```

1. You send the user's message *plus* your tool definitions to the model.
2. The model does not answer directly. Instead it returns a **tool call**: a structured request that says, in effect, "please run `get_weather` with `city = "Paris"`." The model does not run anything. It only asks.
3. Your code reads that request, runs the real `get_weather` function (which calls a weather service), and gets back, say, `18C and cloudy`.
4. You send that result back to the model as a **tool result**, attached to the same conversation.
5. Now the model has the fact it needed, so it writes the final answer.

The model and your code take turns: the model decides *what* to do, your code decides *how*. A model may also chain several tool calls in a row before answering, looping through steps 2 to 4 many times. This back-and-forth is the heart of every agent you will build later in AtlasOS.

> 🔑 **Errors are results, not crashes.** When a tool fails (the service is down, the city was misspelled), do not crash and do not silently hide it. Send the error back to the model *as a tool result*, clearly marked: `"Error: no city named 'Pariss' found. Did you mean 'Paris'?"` A capable model will usually correct itself and try again. Swallowing the error leaves the model guessing. Returning clear, recoverable errors is one of the highest-leverage things you can do for reliability. ([Yan et al., structured reflection for reliable tool interactions, 2025](https://arxiv.org/pdf/2509.18847))

---

## Part 3: The same shape across Claude, Gemini, and GPT

Here is the durable, model-agnostic fact: **all three major providers expose function calling the same way.** You describe tools as JSON-schema definitions, you send them with the conversation, and the model returns a structured call for you to run. The field names differ slightly; the shape and the loop are identical. Learn it once and it transfers.

| | **Claude** (Anthropic) | **Gemini** (Google) | **GPT** (OpenAI) |
|---|---|---|---|
| You pass tools as | a `tools` list of name + description + `input_schema` | a `tools` list of `functionDeclarations` (name + description + `parameters`) | a `tools` list of `{type:"function", function:{...}}` |
| Schema format | JSON Schema | JSON Schema (`parameters`) | JSON Schema (`parameters`) |
| Model returns | a `tool_use` content block | a `functionCall` part | a `tool_calls` entry |
| You reply with | a `tool_result` block | a `functionResponse` part | a `role:"tool"` message |
| "Must call a tool" knob | `tool_choice` | `tool_config` (function-calling mode) | `tool_choice` |

The three tool definitions, side by side, so you can see they are the same idea wearing three labels:

```text
# CLAUDE (Anthropic) — tools: [ ... ]
{ "name": "get_weather",
  "description": "Get current weather for a city.",
  "input_schema": { "type": "object",
    "properties": { "city": { "type": "string" } },
    "required": ["city"] } }

# GEMINI (Google) — tools: [{ functionDeclarations: [ ... ] }]
{ "name": "get_weather",
  "description": "Get current weather for a city.",
  "parameters": { "type": "object",
    "properties": { "city": { "type": "string" } },
    "required": ["city"] } }

# GPT (OpenAI) — tools: [{ type: "function", function: { ... } }]
{ "type": "function",
  "function": {
    "name": "get_weather",
    "description": "Get current weather for a city.",
    "parameters": { "type": "object",
      "properties": { "city": { "type": "string" } },
      "required": ["city"] } } }
```

Same name, same description, same JSON-Schema fields. Only the wrapper key changes (`input_schema` vs `parameters`, nested under `function` for GPT). If you can write one, you can write all three.

> 💡 **Two knobs that exist everywhere under different names.** **Tool choice** controls whether the model *may* call a tool, *must* call some tool, or must call one *specific* tool. Use "must call a tool" when an answer without one would be useless (a lookup assistant that should never guess). **Strict schema validation** forces the model's arguments to match your schema exactly; turn it on where offered, because argument correctness, not the number of tools, is what makes or breaks reliability. ([Symflower, function calling in LLM agents](https://symflower.com/en/company/blog/2025/function-calling-llm-agents/))

> ⚠️ **Verify against current docs.** Exact field names, model ids, and beta flags move fast across all three providers. The *shape* above is stable; treat any specific key or model name as something to confirm in the provider's current documentation before you ship.

---

## Part 4: Designing tools the model uses reliably

Beginners assume a weak agent means a weak model. Far more often, the tools are the problem. The model can only be as good as the menu you hand it. Anthropic's engineering team reported spending more time tuning the tools than the prompt for one of their coding agents, and recommends making tools **poka-yoke**, a manufacturing term meaning "mistake-proof": shape the inputs so the easy path is the correct path. ([Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents))

A few durable rules of thumb hold across every provider:

- **Consolidate, do not mirror your database.** One well-named `schedule_meeting` tool beats three thin tools (`list_users`, `list_calendars`, `create_event`) that force the model to orchestrate them by hand. More tools is not better. Each extra tool is one more thing the model can pick wrongly.
- **Namespace your tool names** so they read clearly, such as `github_list_pull_requests` or `stripe_create_refund`. This helps the model tell similar tools apart.
- **Return high-signal output.** Give back human-readable identifiers rather than long random codes, and paginate, filter, or trim large results. Every token you return competes for the model's limited attention and costs money.
- **Write the description and field names for the model, not your backend.** Name a field `customer_email`, not `cust_eml_2`. The model reads these names as hints.

There is a real cost lever here too, the one Puneet Shah demonstrates on the Claude platform: when an agent has tens or hundreds of tools, loading every tool's schema into context fills the window before the work even starts. **Tool search** keeps the definitions out of context until the model asks for one (Lovable cut token use 10% this way *and* performance improved). And **programmatic tool calling** has the model write a small script to trim a tool's result down to just the relevant part before it ever reaches the context window. Both are the same lesson: keep the tool menu and the tool output lean.

> ❌ **One security note to plant early (full treatment in a later unit).** A tool is a door into your systems. Treat every input the model sends to a tool as untrusted, and validate and limit it *at the tool itself*, never relying on the prompt alone. Prompt injection (tricking the model into misusing a tool) is a leading risk, so enforce limits in code. ([Zylos Research, tool use standards and benchmarks](https://zylos.ai/research/2026-04-07-tool-use-function-calling-standards-benchmarks))

---

## Part 5: MCP, one standard instead of N times M wiring

You can now hand any model a tool. The next problem is practical: every time you want to connect a model to a new tool or data source (a database, your issue tracker, a docs site), you write custom plumbing. Do that across many apps and many tools and the wiring explodes.

**MCP** stands for **Model Context Protocol**. A **protocol** is just an agreed set of rules for how two programs talk, like a shared language. MCP is an open standard for secure, two-way connections between AI applications and the tools and data they need. The common analogy: MCP is "the USB-C port for AI applications." Just as USB-C lets any compatible device plug into any compatible port, MCP lets any compatible agent plug into any compatible tool. ([MCP docs](https://modelcontextprotocol.io/docs/getting-started/intro))

It is no longer one company's project. Announced in November 2024, it has been adopted across the industry and, in December 2025, was donated to the **Agentic AI Foundation**, a vendor-neutral body under the Linux Foundation. Treat it like any open web standard: a common protocol many vendors implement, not a single product. ([Linux Foundation: forming the Agentic AI Foundation](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation))

**The N times M problem.** Suppose you have *N* AI applications and *M* tools. Without a standard, you build a custom connector for every pairing: *N times M* integrations. 10 apps and 10 tools is 100 connectors.

```text
   WITHOUT MCP (N x M):              WITH MCP (N + M):
   app1 ─┬─ tool1                    app1 ─┐         ┌─ tool1
   app2 ─┼─ tool2     every          app2 ─┼─ MCP ──┼─ tool2
   app3 ─┼─ tool3     pairing        app3 ─┘ (one   └─ tool3
         └─ ...       wired by               shared      ...
                      hand                  standard)
   100 connectors                    20 connections, reusable
```

MCP turns it into an *N plus M* problem. Each application learns to speak MCP once, and each tool is wrapped as an MCP server once. After that, any MCP client can use any MCP server with no extra glue. Build one server, every MCP client can use it. That is the payoff.

**How it is put together.** MCP follows a **client-server** design:

- A **host** is the AI application you actually use: a desktop chat app, a code editor, or your coding agent.
- Inside the host runs an MCP **client**, which holds an open connection to a server.
- An MCP **server** is a small program that exposes capabilities (your files, a database, an API) in the MCP format.

The two sides talk using **JSON-RPC 2.0**, a standard lightweight format for sending requests and getting replies as JSON. You do not need to memorise it; just know it is the agreed wire format.

**The three server primitives** (the basic building blocks a server can offer):

- **Tools:** functions the model can call to take an action ("send an email," "run a query"). The executable abilities.
- **Resources:** structured data the model can read into its context, such as a file's contents or a database record.
- **Prompts:** reusable prompt templates or canned workflows a user or app can pull in on demand.

> 🔑 **Tool descriptions from a server are untrusted input.** When you connect a third-party MCP server, its tool descriptions flow straight into your model's context. A malicious server can try to manipulate your agent through that text (called "tool poisoning"). Prefer servers you trust, and apply the same skepticism you would to any untrusted input.

---

## Part 6: Adding an MCP server to your coding agent

Here is the everyday payoff for you right now: your coding agent from Unit 1 is already an MCP **client**. That means you can plug an MCP server into it and the agent gains new tools instantly, with no code from you. The principle is identical across all three; only the command and config-file location differ.

| | **Claude Code** | **Gemini CLI** | **Codex CLI** |
|---|---|---|---|
| Add a server (CLI) | `claude mcp add <name> ...` | `gemini mcp add <name> ...` | `codex mcp add <name> ...` |
| Config file | `.mcp.json` (project) | `settings.json` (`mcpServers`) | `config.toml` (`[mcp_servers.<id>]`) |
| List / inspect in-session | `/mcp` | `/mcp` | `/mcp` |
| Transports | stdio, SSE, HTTP (`--transport`) | command, url, httpUrl | stdio, plus url-based |

The two ways to connect, in every tool:

- **By command (a "stdio" server):** the agent launches a local program (often via `npx`) and talks to it over standard input/output. Good for servers that run on your machine, like a filesystem server.
- **By URL (an HTTP/SSE server):** the agent connects to a server already running somewhere, local or remote. Good for hosted services.

Concretely, to add a filesystem MCP server (one that lets the agent read and write files in a folder you choose) to each agent:

```text
# CLAUDE CODE — add a local (stdio) server, scoped to this project:
claude mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem ~/atlasos
#   then inside Claude Code, run:  /mcp     (lists servers + their tools)

# GEMINI CLI — add a server, then inspect it:
gemini mcp add filesystem npx -y @modelcontextprotocol/server-filesystem ~/atlasos
#   then inside Gemini CLI, run:  /mcp

# CODEX CLI — add a server (or edit ~/.codex/config.toml directly):
codex mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem ~/atlasos
#   then inside Codex CLI, run:  /mcp
```

In every case, after adding the server you run `/mcp` *inside* the agent and you will see the server listed with the tools it exposes (for a filesystem server, things like `read_file`, `write_file`, `list_directory`). The agent can now use those tools the same way it uses its built-in ones.

> 💡 **Verify against current docs.** The exact server package name, the `mcp add` flags, and the config-file keys move quickly across all three CLIs. The pattern (add a server by command or URL, then `/mcp` to confirm) is stable. Check each tool's current docs for the precise syntax, and only connect servers you trust.

> ✅ **Prove it actually got invoked.** Adding a server is not the same as the agent using it. After connecting, give the agent a task that *requires* the new tool ("use the filesystem server to list the files in this folder") and watch the transcript: you should see it call the server's tool by name and show the result. If it answers from memory instead, the server is not wired up. That check, did the model really invoke the tool, is the whole game.

---

## Key takeaways

1. **A tool is a name, a description, and a JSON schema.** The model reads those text hints; it cannot see your code.
2. **The loop is universal:** send tools plus message, get a tool call, run it, return the result, repeat. The model decides *what*, your code decides *how*.
3. **The shape is identical across Claude, Gemini, and GPT.** Only wrapper keys differ (`input_schema` vs `parameters`). Hold model ids and field names loosely; verify against current docs.
4. **Tool design beats model choice for reliability.** Consolidate tools, namespace names, trim output, and return errors as results so the model can recover.
5. **MCP turns N times M wiring into N plus M.** Build a server once; every MCP client (including your coding agent) can use it.
6. **Adding an MCP server is one command per agent**, then `/mcp` to confirm. Always verify the model actually invokes the tool.

## Common pitfalls

- ❌ A vague tool description, then blaming the model when it never calls the tool.
- ❌ Exposing dozens of thin tools that each do one tiny database operation, instead of a few consolidated ones.
- ❌ Cryptic or huge tool output that floods the context window with noise.
- ❌ Hiding a tool error (crashing or swallowing it) instead of returning it as a clear, recoverable result.
- ❌ Trusting the prompt to keep a tool safe instead of validating inputs in code.
- ❌ Rebuilding a one-off integration for something MCP already standardizes.
- ❌ Connecting an untrusted third-party MCP server whose tool descriptions flow into your context.
- ❌ Assuming "server added" means "tool used." Verify the model actually invoked it.

---

## 🛠️ The Build: the AtlasOS `tools/` layer

> The hands-on payoff. You will give AtlasOS its first hands: a real tool the model can call, written by you, plus an MCP server wired into your coding agent. This is the `tools/` component from the roadmap, and Forge and Scout will lean on it later.

### What you will build

A new `tools/` folder in your `atlasos` repo containing one real tool, a small **file-search** tool, defined as a JSON-schema function and wired into a tiny script that runs the full tool-use loop so you watch the model call it. Then you connect one MCP server (a filesystem server) to your coding agent and confirm the agent invokes it. Everything is committed to git.

### Milestones (in order, each fully explained)

**1. Open your project and start fresh.** In your VS Code terminal: `cd ~/atlasos`, then `code .` to open it. Start your coding agent inside the folder (`claude`, `gemini`, or `codex`). You will let the agent write the code with you, using the plan, act, verify loop from Unit 1.

**2. Create the `tools/` folder and choose your provider.** Ask the agent, in plain English: *"Create a folder called `tools/` in this repo. Inside it, create a small script that defines one tool and runs the full tool-use loop against [Claude / Gemini / GPT], with no agent framework, so I can watch the model call the tool."* Pick whichever provider you have an API key for. Set your API key as an environment variable when the agent tells you to (it will explain the exact variable name for your provider). Read the plan before you let it write.

**3. Define one real tool: `search_files`.** Have the agent define a tool with this exact shape, a name, a clear description, and a JSON-Schema input:

```text
# The tool definition the model will see.
name:        "search_files"
description: "Search the project's files for a text string and return the
              matching file paths and line numbers. Use when the user asks
              where something is defined or mentioned in the codebase."
input_schema:
  type: object
  properties:
    query: { type: string, description: "Text to search for, e.g. 'AtlasOS'" }
  required: ["query"]
```

The real implementation behind it is small: a function that walks the repo, finds lines containing `query`, and returns the matching `path:line` results, trimmed to the first handful so the output stays high-signal (remember Part 4: lean output).

**4. Run the full loop and watch the call happen.** Ask the agent to run the script with a prompt like *"Where is AtlasOS described in this project?"* You should see, in order: the model returns a **tool call** for `search_files` with `query: "AtlasOS"`; your code runs the search and prints the matching files; you return that as a **tool result**; the model writes a final answer that cites the files. If you see the model answer *without* calling the tool, the description is too vague or the tool was not passed: fix it and re-run. This is the moment the principle becomes real.

**5. Make a tool error recoverable (the reliability rep).** Temporarily change the tool to return `"Error: search index unavailable, retry with a simpler query"` for one run. Watch a capable model read the error and adjust, rather than crashing. Then restore the working version. You have now seen errors-as-results from Part 2 first hand.

**6. Connect one MCP server to your coding agent.** Leave the script for a moment. In the terminal, add a filesystem MCP server to your agent using the command for your tool from Part 6 (for example `claude mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem ~/atlasos`, or the Gemini / Codex equivalent). Start your agent and run `/mcp`. You should see the server listed with its tools.

**7. Verify the agent actually invokes the MCP tool.** Give the agent a task that needs the server: *"Using the filesystem MCP server, list the files in this project and tell me which ones mention AtlasOS."* Watch the transcript: it should call the server's `list_directory` (and `read_file`) tools by name and show real results. If it answers from memory, the server is not wired up; re-check Milestone 6.

**8. Save your work to git.**

```text
# From inside ~/atlasos, after leaving the agent (type exit):
git add -A
git commit -m "Add tools/ layer: search_files tool + MCP server wiring"
git push

# What you'll see after push:
...
To https://github.com/yourname/atlasos.git
   a1b2c3d..e4f5g6h  main -> main
```

**9. Stretch (optional).** Add a second tool to your script (for example `read_file`) and confirm the model now *chooses correctly* between `search_files` and `read_file` depending on the question. Choosing well among several tools is exactly what makes an agent feel capable.

### How you will know you are done

- ✅ A `tools/` folder exists in `atlasos` with a `search_files` tool defined as name + description + JSON schema.
- ✅ You ran the loop and watched the model return a tool call, your code run it, and the model answer using the result.
- ✅ You returned an error as a tool result once and saw the model recover.
- ✅ An MCP server is connected to your coding agent and shows up under `/mcp`.
- ✅ You gave a task that required the MCP tool and watched the agent invoke it by name.
- ✅ Everything is committed and pushed to GitHub.

> 💡 **If the model would not call your tool, that is the lesson, not a failure.** Nine times out of ten the fix is a clearer description or better field names. Tightening that text until the model reliably reaches for the tool is the core skill of this unit.

---

## Cheat sheet

```text
A TOOL IS THREE THINGS
  name        -> how the model refers to it (e.g. search_files)
  description -> plain English: what it does + when to use it (half the tool)
  input_schema-> JSON Schema: fields, types, which are required

THE TOOL-USE LOOP (universal)
  1. send tools + user message            4. send tool RESULT back
  2. model returns a TOOL CALL (asks)     5. model writes final answer
  3. YOUR code runs the real function     (repeat 2-4 to chain calls)
  errors are RESULTS, not crashes -> the model recovers

SAME SHAPE, THREE PROVIDERS (verify ids/keys in current docs)
  Claude : tools[].input_schema | returns tool_use | reply tool_result
  Gemini : functionDeclarations[].parameters | functionCall | functionResponse
  GPT    : tools[].function.parameters | tool_calls | role:"tool" message

TOOL DESIGN (reliability beats model choice)
  consolidate, don't mirror your DB | namespace names | trim output
  describe for the model, not the backend | errors as results

MCP = USB-C for AI apps (open standard, N x M -> N + M)
  host (your agent) -> client -> server ; wire = JSON-RPC 2.0
  primitives: TOOLS (act) | RESOURCES (read) | PROMPTS (templates)

ADD AN MCP SERVER TO YOUR AGENT, then /mcp to confirm
  Claude Code : claude mcp add <name> -- npx ...   (.mcp.json)
  Gemini CLI  : gemini mcp add <name> npx ...      (settings.json)
  Codex CLI   : codex mcp add <name> -- npx ...    (config.toml)
  ALWAYS verify the model actually INVOKES the tool.
```

## How this connects to the rest of the course

- **Next, Unit 5 (Retrieval and RAG):** the most useful tool you can give a model is one that fetches the right facts. You will build retrieval on top of the tool-use loop you just learned, and wrap it as an MCP server so any AtlasOS agent can reuse it.
- **Throughout:** every AtlasOS agent, Scout researching, Forge building, Warden checking, acts through tools defined exactly the way you did here, and shares them through MCP. This unit is the hands the whole fleet uses.

---

*Unit 4 of the combined path. Fuses the vendor-neutral principles of Agentic Engineering Modules 4 and 9 with current, model-agnostic practice (function calling across Claude, Gemini, and GPT; MCP across Claude Code, Gemini CLI, and Codex CLI). Tool field names, model ids, and CLI flags change quickly; verify against current documentation.*

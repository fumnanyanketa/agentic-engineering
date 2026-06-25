# Module 5 · Lesson 16: Tool, Skill, or Subagent?

> **Course:** Building with Claude, a self-paced course
> **Module 5:** Building agents, Claude Managed Agents
> **Speaker:** Will, Applied AI team, Anthropic
> **Source talk:** [Tool, skill, or subagent? Decomposing an agent that outgrew its prompt](https://www.youtube.com/watch?v=mWvtOHlZM-I) · [full transcript](../../transcripts/code-with-claude-2026-london-2026-day-2/02_tool-skill-or-subagent-decomposing-an-agent-that-outgrew-its-prompt.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

When an agent grows by having capability "bolted on" over time (a 400-line system prompt, a dozen overlapping tools, tangled sub-agents) its performance drops, and you fix it not by adding more but by decomposing: move standing knowledge into **skills**, replace special-purpose tools with general **computer primitives**, keep only the **sub-agents** that truly earn their place, and measure every change against your evals.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you take a deliberately overgrown agent called **Sprawl** and decompose it, hill-climbing your eval score from "embarrassing" to "great." Everything before the Capstone teaches the decisions you will make there. If you want to see the finish line first, jump to the **"Capstone Project: rescue Sprawl"** section near the end, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[How we built our multi-agent research system (Anthropic)](https://www.anthropic.com/engineering/multi-agent-research-system)** (essay). A first-principles treatment of orchestrator-vs-subagent decomposition: when to parallelize, the cost of subagents, and the communication tradeoffs, the exact decisions this lesson teaches.
> - **[Building Effective Agents (Anthropic)](https://www.anthropic.com/engineering/building-effective-agents)** (essay). Lays out the pattern catalog (routing, orchestrator-workers, evaluator-optimizer) that frames the tool/skill/subagent choice.

## A few plain-language basics first

This lesson uses some everyday AI terms. Here they are in simple words:

- **LLM (Large Language Model):** the kind of AI that reads and writes text. "Claude" is an LLM.
- **Model:** one specific version, for example "Opus 4.7." Newer models are smarter.
- **Agent:** an AI that takes a series of actions toward a goal, rather than answering in one shot.
- **Orchestrator:** the main agent that runs the show and decides what to do, possibly delegating to helpers.
- **System prompt:** the standing instructions that define who the agent is and how it behaves.
- **Context window:** the limited amount of text a model can hold and reason over at once. Filling it with junk is "polluting" it.
- **Tool:** a small piece of code the agent can choose to run (read a file, run code, search the web).
- **Skill:** packaged, composable information Claude can pull into context only when it realises it needs it.
- **Sub-agent:** a separate instance of Claude, with its own context window, that the orchestrator hands a piece of work to.
- **Eval (evaluation):** a set of test cases you run the agent against to measure whether it works. The single most important measuring tool here.
- **Hill climbing:** repeatedly making a change and re-running your evals, keeping changes that raise the score, like climbing toward a peak one step at a time.

Every term is also explained again the first time it appears below.

## Why this lesson matters

This is one of the most common and painful patterns in real agent work, and Will names it exactly. You ship an agent that works great. A few weeks later you are asked to add a capability, so you bolt one on. Then another. Before long your system prompt is hundreds of lines, you have dozens of tools and sub-agents, and the agent has started **regressing** (getting worse) in the very areas it used to be great at. As Will says, "if this is you, you're not alone," it happens to customers and to Anthropic itself. The fix is not more instructions. It is knowing which **primitive** (basic building block) fits each job: tool, skill, or sub-agent.

## Learning objectives

By the end of this lesson you will be able to:

1. Recognise the symptoms of an agent that has "outgrown its prompt": a bloated system prompt, too many tools, tangled sub-agents, and dipping evals.
2. Decide when to reach for a **tool**, a **skill**, or a **sub-agent**, using clear rules.
3. Replace special-purpose tools with **human-like computer primitives** (file system, code execution, web search) and explain why that cuts tokens and cost.
4. Move standing business logic out of the system prompt into **skills** using **progressive disclosure**.
5. Keep only the sub-agents that earn their place, and use the **native callable-agents** capability for clean observability.
6. **Hill-climb** on evals: baseline, change, re-run, repeat.

## Prerequisites

- Module 5 · Lesson 13, 14, 15 (Claude Managed Agents): the three building blocks, sessions, and tools.
- Module 2 · Lesson 3 (The prompting playbook) and Module 3 (Evals): you understand what an eval is and why it is the only honest measure of a change.

---

## Part 1: the problem, an agent that outgrew its prompt

The example agent is **Stock Pilot**, an inventory-management agent for a mid-size retailer. It flags low stock, forecasts demand, picks suppliers, files purchase orders (POs), and writes weekly reports. None of those is hard alone. The trouble is how it grew.

Today's architecture is a single **orchestrator** (the main agent) with:

- A system prompt that has grown to about **400 lines**.
- **12 tools**, three of which are actually wrappers around sub-agents with isolated context windows.

How did it get here? Each new business requirement was just bolted on: needed forecasting, so spin up a forecaster sub-agent; needed reports, so add a report-writer sub-agent. Never modernise, just append. The result: the **evals dipped**.

> 🔑 **Key idea: complexity you bolt on quietly degrades the parts that already worked.** A longer prompt, more tools, and more sub-agents are not free. They crowd the context window, create conflicts, and introduce communication breakdowns. Growth without redesign is decay.

### The evals tell the story

Stock Pilot has 12 eval tasks across five grader types. (A **grader** is the thing that decides whether a test case passed.) IDs starting with **R** are **regression** tasks (realistic single-turn tasks). IDs starting with **F** are **failure-mode** tasks (harder multi-turn tasks). Some graders are **deterministic** (always the same answer for the same input: they measure turn count, latency, token usage) and some are **non-deterministic**, using **LLM-as-a-judge** (another Claude scoring fuzzy qualities like tone, style, and output quality).

Three failures show three different root causes, and each points at a different fix:

| Eval | What it tests | Why it fails | The real cause |
|---|---|---|---|
| **F1** | A daily low-stock sweep | The agent reaches the right answer but by "a very winding path," failing on efficiency | The agent is doing work it should hand to a **tool** |
| **F2** | Ordering under a promotion package | The sub-agent gets it right, but the result is mangled handing back to the orchestrator | A **communication breakdown** between sub-agent and orchestrator |
| **R8** | Forecasting during a promotion month | The agent pulls the right baseline (12 units/day) and the right multiplier (3.1x), then "hallucinates" and uses 1.35x instead | A **context problem**: two policies in different parts of the long prompt contradict each other |

> 💡 R8 is the key insight: "this isn't a model problem. It's an issue with the information that we're surrounding the model with." A **hallucination** (the model stating something untrue as if true) here is caused by a confusing, conflicting system prompt, not by a weak model. Fix the context, not the model.

The starting eval score is about **83%** when run cleanly (and dipped to 62% in one live run). Will is blunt: "if you work in the world of manufacturing, that is not okay. 17% failure is a really expensive failure percentage."

## Part 2: the method, hill climbing on evals

The whole workshop is one repeated loop Anthropic calls **hill climbing**:

```text
1. Run the evals            -> get a baseline (~83%)
2. Change ONE part of the design (skills, tools, or sub-agents)
3. Re-run the evals         -> did the score go up?
4. Keep what helps, repeat  -> climb toward a higher score
```

Will also uses Claude Code itself to run and **triage** the evals (figure out the themes behind the failures). Pointed at the failing run, Claude finds patterns: the model is doing work it should have tools for, output structure is not enforced, and the long system prompt has conflicts. That triage tells you which primitive to reach for next.

> 🔑 **Change one thing, re-run, measure.** Hill climbing only works if each step is isolated. If you change three things at once and the score moves, you have learned nothing about why.

## Part 3: skills, move standing knowledge out of the prompt

The first fix targets the bloated 400-line system prompt. Will's definition: a **skill** is "packaged and composable information that Claude has the ability to pull into context whenever Claude realizes that it needs that information to complete a particular task."

The mistake was stuffing every policy and procedure into the system prompt as requirements piled up. The fix is **progressive disclosure**: only load information when it is actually needed.

> 🔑 **The rule for the system prompt:** "Leave the system prompt only for the information that Claude needs in its mind, regardless of the task." Everything Claude needs only *sometimes* belongs in a **skill**, not the prompt.

Why this helps:

- **Less context pollution.** If you ask Claude to build a forecast, it should pull in forecasting info only then, not carry it (and every other policy) for every task.
- **More flexibility.** Claude decides what to load based on the task.
- **Fewer conflicts.** Separated, task-specific skills do not contradict each other the way a giant prompt's scattered policies did (the R8 bug).

In the workshop, Claude analyses the prompt, finds pre-built skills it can use, and the system prompt shrinks from **about 400 lines to about 50** (and later to about 15), with the business logic moved into skills.

```text
BEFORE: 400-line system prompt holding every policy and procedure
AFTER:  ~15-line system prompt + skills loaded on demand (progressive disclosure)
```

## Part 4: tools, start with human-like primitives

Stock Pilot had a tool for everything: a tool to retrieve data, a tool to analyse data, a tool for each step. Will's principle is the opposite of "a tool for every job."

> 🔑 **Build agents with the same primitives humans have at work.** When you show up to your job you have a computer: a file system to navigate, a browser to search the web, and (if you are an engineer) the ability to write and run code. Claude Code is great mostly because "we've just given Claude access to a computer." Start there.

So the foundational tools to start with are:

- **Code execution** (a bash tool, so Claude can write and run a quick script).
- **File-system navigation** (read and write files).
- **Web search.**
- Sometimes a **to-do list.**

You add custom tools only when these genuinely fall short, and you remove primitives an agent does not need.

> 💡 **Why this saves so much.** For data analysis over CSVs or spreadsheets, giving Claude a bash tool to write a quick Python script and read the results is "much more effective than just uploading the entire CSV into Claude's context window." In the workshop, swapping special tools for file-system and code-execution primitives dropped one task from **over 200,000 tokens** to a fraction of that, lowering cost and execution time too.

A big convenience in managed agents: these primitives are **included by default**. You do not have to write a tool to give Claude code execution or file access; they come built in, the same ones Claude Code uses.

### When do you reach for MCP?

There is an order of preference for tools:

```text
1. Claude Code primitives  -> code execution, file system, web search (start here)
2. Custom local tools      -> standalone tools only your agent uses
3. MCP servers             -> ONLY when many clients need the same governed tools
```

(**MCP**, Model Context Protocol, is a shared standard for connecting an AI to external tools; an **MCP server** offers tools over it.) Will warns that people "run towards MCP first" and end up with chaotic, overlapping MCP servers. Reach for MCP only when multiple agents or clients need the same standardised, governed set of tools. He also notes a rising alternative: have Claude invoke CLIs and APIs **using code execution** instead of MCP, since MCP can pollute context and take up space.

## Part 5: sub-agents, keep only the ones that earn it

Two clear cases justify a sub-agent (a separate Claude instance with its own context window):

| Use a sub-agent when... | Example |
|---|---|
| **You want to throw a lot of Claude at a problem** (parallelise) | Deep research, broad web search, code-base exploration: many minds at once, faster and more thorough. |
| **You need a fresh mind** with no prior context | Code review: the Claude that wrote the code should not be the Claude that reviews it. A reviewer with no context catches more. |

Stock Pilot keeps exactly one sub-agent: **forecasting**. Will wants forecasting isolated so nothing in the main conversation's context "distorts the forecasting process." A skill defines the step-by-step forecasting guidelines, but the actual forecasting runs in a separate Claude from the one talking to the customer.

> 🔑 **Two failure modes of sub-agents to respect.** First, **communication breakdown** between orchestrator and sub-agent (the F2 bug): a lot gets lost in translation, just like between two colleagues. Second, **logging is hard**: you must collect transcripts from multiple agents.

Managed agents solves both with a **native callable-agents capability**: managed sub-agents whose logging and observability are as good as the orchestrator's. So instead of hiding a sub-agent inside a tool wrapper (which makes it opaque), you use the native capability and get full metrics on what each sub-agent did.

> 💡 **The frontier trend: fewer sub-agents.** As models get smarter, many customers are folding capability back into the main orchestrator because it can now manage more information at once. "You just don't need as many sub-agents." So before adding one, ask whether the main agent can simply handle it now.

## Part 6: the result

The architecture transformed:

| Before | After |
|---|---|
| Orchestrator built on the raw Messages API | Orchestrator on **Claude Managed Agents** (offloads infrastructure, scaling, security) |
| ~400-line system prompt | **~15-line** system prompt |
| 12 tools (3 were sub-agent wrappers) | **3 tools**: bash, read, write (the human-like primitives) |
| All business logic crammed in the prompt | Business logic packaged as **skills**, loaded on demand |
| Tangled sub-agents hidden in tools | One **native callable** forecasting sub-agent |
| Eval score ~83% (62% in a bad run) | Eval score **~92%** |

The wins were not only the score. Token usage dropped sharply (thanks to code execution), cost fell, and execution time improved. Will is honest that it does not always go this way, sometimes a change regresses, and sometimes you accept higher latency for a high-intelligence task like forecasting, but you only know because you measured.

> 🔑 **Why deploy on managed agents at all?** In Will's words, you reach for it "because I just want to worry about building the best thing possible and not all the messiness that comes with it," the infrastructure, scaling, and security.

---

## Key takeaways

1. **Agents rot when you bolt on capability without redesigning.** Watch for a bloated prompt, too many tools, tangled sub-agents, and dipping evals.
2. **The system prompt holds only what Claude always needs.** Everything situational goes into **skills**, loaded on demand (progressive disclosure).
3. **Start tools with human-like primitives:** code execution, file system, web search. Add custom tools only when needed; reach for MCP last.
4. **Code execution beats stuffing data into context.** Let Claude write and run a script over a CSV instead of reading the whole file in.
5. **Use sub-agents only to parallelise or to get a fresh mind.** Use the native callable-agents capability for clean logging, and prefer folding work back into the orchestrator as models improve.
6. **Hill-climb on evals.** Baseline, change one thing, re-run, keep what helps. Use Claude to triage failures.

## Common pitfalls

- ❌ Fixing a degraded agent by adding more instructions, more tools, or more sub-agents.
- ❌ Keeping standing business logic in the system prompt until it conflicts with itself (the R8 hallucination).
- ❌ Building a tool for every tiny job instead of giving Claude a computer.
- ❌ Reaching for MCP first and ending up with chaotic, overlapping servers.
- ❌ Hiding sub-agents inside tool wrappers, losing observability and inviting communication breakdowns.
- ❌ Adding a sub-agent the orchestrator could now handle itself.
- ❌ Changing several things at once, so the eval movement tells you nothing.

---

## 🛠️ Capstone Project: rescue Sprawl

> This is the main hands on project for the lesson. You are going to deliberately build an overgrown agent, then decompose it, hill-climbing your eval score the whole way, exactly the journey Will took with Stock Pilot.

### What you will build

**Sprawl** is an agent that starts as a mess (a long system prompt, a tool for everything, tangled sub-agents) and that you rescue into a clean design (a short prompt, a few primitives, skills, and at most one justified sub-agent) deployed on Claude Managed Agents, with a rising eval score to prove it.

> 🎯 **Pick your domain.** Reuse **inventory management** like the talk (low-stock sweeps, demand forecasting, supplier picking, weekly reports), or choose your own multi-skill agent: a **travel concierge** (flights, hotels, itineraries, expense reports), a **content desk** (research, drafting, fact-checking, formatting), or a **dev-ops helper**. Pick something with at least four distinct capabilities so it naturally tempts you to over-build.

### Why this is the perfect practice

| Lesson skill | Where you use it in Sprawl |
|---|---|
| Building an eval suite (R and F tasks) | Milestone 1, your baseline |
| Triaging failures with Claude | Milestone 2 |
| Moving prompt logic into skills (progressive disclosure) | Milestone 3 |
| Replacing tools with human-like primitives | Milestone 4 |
| Keeping only justified sub-agents (native callable) | Milestone 5 |
| Hill climbing on evals | Every milestone |

### Milestones (build them in order, each one works on its own)

1. **Build the overgrown agent and its evals.** Write Sprawl with a long (200+ line) system prompt, a tool for every step, and two or three sub-agents hidden in tool wrappers. Write at least 8 eval tasks: a few **R** (single-turn) and a few **F** (multi-turn), with a deterministic grader (turn count, tokens) and one **LLM-as-a-judge** grader. Plant two bugs on purpose: one policy conflict in the prompt, and one sub-agent communication breakdown.
2. **Baseline and triage.** Run the evals and record the score. Then use Claude (Claude Code or the API) to **triage** the failures and name the themes. Confirm it spots your planted bugs.
3. **Decompose into skills.** Move the situational business logic out of the system prompt into **skills** loaded on demand. Shrink the prompt to "only what Claude always needs." Re-run the evals and record the new score.
4. **Decompose the tools.** Replace special-purpose tools with **bash, read, and write** primitives. Make a data task use code execution over a CSV instead of reading the file into context. Re-run, and record the **token** and **cost** drop.
5. **Fix the sub-agents.** Delete sub-agents the orchestrator can now handle. Keep at most one that truly needs isolation or parallelism (for example forecasting or review), and rebuild it as a **native callable agent** for clean logging. Re-run.
6. **Deploy on managed agents.** Deploy your cleaned agent to Claude Managed Agents so infrastructure, scaling, and security are handled. Re-run the evals against the deployed version.
7. **Stretch goals.** Add a brand-new requirement the "wrong" way (append to the prompt) and watch the score dip, then add it the "right" way (a skill) and watch it recover. Add an MCP server only after you can show two clients need the same tool.

### How you will know you are done

- ✅ Your eval score is **meaningfully higher** than the baseline, and you can show the climb step by step.
- ✅ Your system prompt is short; situational logic lives in **skills**.
- ✅ Your tools are mostly **primitives** (bash, read, write), and you can show a token/cost drop from code execution.
- ✅ You kept **at most one** sub-agent, can justify it (parallelism or fresh mind), and it logs cleanly as a native callable agent.
- ✅ Each improvement is tied to a **re-run of the evals**, not a guess.

> 💡 **Keep yourself honest:** if your score went up but you changed three things at once, undo two and find out which one actually did the work. That is hill climbing.

---

## Practice exercises (optional extra reps)

> Small, self-contained tasks, each focused on one idea. Optional and independent. The **Capstone above is the main build** and already covers all of these.

### Exercise 1: diagnose the failure (foundational)
Given three failing evals (one "winding path," one "sub-agent result mangled on handoff," one "right numbers, wrong final calculation"), name the root cause and the right fix (tool, communication, or context) for each.

### Exercise 2: prompt or skill? (foundational)
Take a list of 8 things an agent might need to know. For each, decide whether it belongs in the **system prompt** (always needed) or a **skill** (sometimes needed). Justify each in a sentence.

### Exercise 3: tools to primitives (intermediate)
You have an agent with `read_csv`, `sum_column`, `filter_rows`, and `make_chart` tools. Replace them with human-like primitives and describe how Claude would do the same work with code execution. Predict the effect on tokens.

### Exercise 4: justify the sub-agent (intermediate)
For three capabilities (deep web research, drafting an email, reviewing the agent's own code), decide which deserve a sub-agent and which the orchestrator should just do. Cite the rule (parallelise / fresh mind / neither).

### Exercise 5: hill climb for real (advanced)
Take any small agent you have, write 5 eval tasks, get a baseline, then make exactly one decomposition change (skill, primitive, or sub-agent) and re-run. Record the before/after score, tokens, and latency. Was it the right call?

---

## Cheat sheet

```text
SYMPTOMS YOU'VE OUTGROWN YOUR PROMPT
  400-line system prompt | a tool for everything | tangled sub-agents | dipping evals

PICK THE RIGHT PRIMITIVE
  TOOL       -> the model is doing work it should offload (esp. code execution for data)
  SKILL      -> info Claude needs SOMETIMES; load on demand (progressive disclosure)
  SUB-AGENT  -> only to parallelise OR to get a fresh, context-free mind

TOOLS: ORDER OF PREFERENCE
  1. Claude Code primitives (code exec, file system, web search) <- start here
  2. Custom local tools
  3. MCP (only when many clients need the same governed tools)

SYSTEM PROMPT RULE
  Keep ONLY what Claude needs regardless of task. Everything else -> a skill.

SUB-AGENT RULES
  Use native callable agents for clean logging.
  Watch for orchestrator <-> sub-agent communication breakdowns.
  Fold work back into the orchestrator as models get smarter.

THE LOOP: HILL CLIMB
  baseline -> change ONE thing -> re-run evals -> keep what helps -> repeat
  (use Claude to triage the failures)
```

## How this connects to the rest of the course

- **Earlier, Module 5 · Lesson 13, 14, 15 (Claude Managed Agents):** the platform, sessions, tools, and multi-agent features this lesson decomposes onto.
- **Earlier, Module 2 · Lesson 3 (The prompting playbook):** "instructions don't add capability" and "change one thing at a time" are the seeds of this lesson's decomposition and hill climbing.
- **Earlier, Module 3 (Evals):** the eval suite and LLM-as-a-judge graders this lesson hill-climbs on are built out there.

---

*Source: "Tool, skill, or subagent? Decomposing an agent that outgrew its prompt" by Will (Anthropic), Code with Claude 2026, London. Code and architecture snippets are illustrative reconstructions of the workshop described in the talk. Adapt the model names and API details to the current SDK.*

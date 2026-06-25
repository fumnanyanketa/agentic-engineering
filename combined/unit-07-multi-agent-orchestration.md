# Unit 7: Multi-Agent Orchestration

> **Course:** Agentic Engineering, a model-agnostic self-paced path *(working title)*
> **Unit 7 of 11:** Decide honestly when many cooperating agents beat one, build the orchestrator-and-subagents (lead-and-workers) pattern, choose correctly between a tool, a skill, and a subagent, and use a framework with your eyes open
> **The how, across agents:** subagents in Claude Code (Anthropic), Gemini CLI (Google), Codex CLI (OpenAI); the orchestration pattern is identical regardless of model, current practice verified June 2026
> **AtlasOS build:** the orchestrator fleet, Atlas dispatching 2 to 3 specialized subagents (Scout plus a writer and a reviewer) for one real outcome
> **Estimated time:** 90 to 120 minutes (read plus the build)

---

## In one sentence

A multi-agent system is one lead agent that splits a job among several helper agents, and it is at once one of the most powerful and one of the most over-used ideas in the field, so this unit teaches you both halves of the craft: the honest rule for when many agents genuinely beat one (read-heavy, parallelizable, high-value work) versus when a single agent wins (write-heavy, dependent work), and the deliberate decomposition that follows (deciding tool vs skill vs subagent), so that when you reach for a second agent you do it with reasons and numbers, not because it sounds sophisticated.

> 🎯 **Where this unit is heading.** The payoff is a **Build** where you turn **Atlas** (your orchestrator from earlier units) into a small **fleet**: Atlas takes one outcome, dispatches 2 to 3 specialized subagents (**Scout** to research, a **writer** to draft, a **Warden**-style **reviewer** to check), collects their work, and synthesizes a final result, with a written "tool vs skill vs subagent" decision in your repo. You will prove the fleet does something one agent could not do as well alone, and you will compare it against a single-agent baseline on quality, time, and cost. Jump to **"The Build"** to see the finish line, then come back.

## First-principles companion

> 💡 **The durable ideas behind this unit.** The tools are recent; the judgment is not. If you want the timeless versions (optional, read them any time):
>
> - **[How we built our multi-agent research system (Anthropic)](https://www.anthropic.com/engineering/multi-agent-research-system)** (essay). A first-principles treatment of orchestrator-versus-subagent decomposition: when to parallelize, the real cost of subagents, and the communication trade-offs.
> - **[Building Effective Agents (Anthropic)](https://www.anthropic.com/engineering/building-effective-agents)** (essay). The pattern catalog (routing, orchestrator-workers, evaluator-optimizer) and the case for starting *without* a framework.
> - **[Don't Build Multi-Agents (Cognition)](https://cognition.ai/blog/dont-build-multi-agents)** (essay). The honest counter-argument: why parallel agents are fragile, and why a single linear agent is often the right default.

## A few plain-language basics first

New terms, in plain words. Each is explained again the moment it matters.

- **Agent:** an LLM (large language model, the kind of AI that reads and writes text) running in a loop: it reads, plans, acts with a tool, reads the result, and repeats until the job is done.
- **Multi-agent system:** more than one separate agent splitting the work between them, instead of a single agent doing it all.
- **Orchestrator (lead):** the main agent that runs the show. It breaks a big task into pieces and hands each piece out.
- **Worker (subagent):** a separate agent instance, with its **own context window**, that the orchestrator hands one piece of work to. It does its piece and returns a short summary.
- **Context window:** the limited amount of text a model can hold and reason over at once. Fill it with junk and you "pollute" it.
- **Tool:** a small piece of code the agent can choose to run: read a file, run a script, search the web.
- **Skill:** packaged, composable instructions and assets the agent pulls into context *only when it realizes it needs them*. Standing know-how, loaded on demand.
- **Token:** a small chunk of text (roughly three quarters of a word). You pay per token, so more tokens means more cost.
- **Breadth-first task:** one where you must look in many independent places at once (research, broad search). Splits cleanly across workers.
- **Dependent / write-heavy task:** one where each step changes the state and later steps lean on exact earlier ones (editing a codebase). Resists splitting.
- **Framework:** a ready-made library that handles the agent loop's plumbing for you, instead of you writing it by hand against a model's API.

## Why this unit matters

The whole course points here. AtlasOS is, by definition, "a fleet of specialized agents" coordinated by an orchestrator. But the moment you can spawn a second agent, the temptation is to spawn ten, and that is how good systems rot: more cost, more coordination breakdowns, worse results than the single agent you started with. The valuable skill is not *building* a fleet, it is *judging* when a fleet earns its keep and keeping it as small as the job allows.

> 🔑 **A second agent must earn its seat.** Every extra agent adds token cost and a new way for things to miscommunicate. Add one only when the task is breadth-first and parallelizable, or when you genuinely need a fresh, context-free mind. Otherwise, one agent doing one step after another wins.

## Learning objectives

By the end of this unit you will be able to:

1. State the honest rule for multi-agent versus single-agent, and apply the read-heavy-versus-write-heavy boundary to a real task.
2. Read a quality gain and a cost multiplier *together*, and decide whether multi-agent pays for a given job.
3. Build the orchestrator-worker pattern vendor-neutrally, and recognise the same pattern in Claude Code, Gemini CLI, and Codex CLI subagents.
4. Decide correctly between a **tool**, a **skill**, and a **subagent** when an agent grows, and document the decision.
5. Choose whether to use a framework, and keep the underlying prompts and traces visible whatever you choose.

## Prerequisites

- Units 1 to 5: you can drive a coding agent through plan, act, verify; you have an AtlasOS repo; **Atlas** (a simple orchestrator) and **Scout** (a research agent with memory) already exist from earlier builds.
- You understand tools and MCP (Unit 4) and retrieval and memory (Unit 5). This unit coordinates the agents that use them.

---

## Part 1: The honest debate (one agent or many?)

The most useful thing in this whole topic is not a technique. It is a piece of judgment, and two respected engineering teams have publicly disagreed about it. Learning *where the line between them sits* is worth more than picking a side.

**The case for multi-agent.** One AI lab built a research system in the orchestrator-worker shape: a strong model as the lead, several faster, cheaper models as workers, each searching the web **in parallel** (at the same time). On the lab's own internal test, this beat a single agent using the same strong model alone by about **90 percent**. The reason given: workers run at once, so the system chases many independent leads simultaneously. Multi-agent "excels for breadth-first queries that pursue multiple independent directions." Example: "find every board member across all the tech companies in a stock index" splits cleanly into many separate lookups.

**The case against multi-agent.** Another team published a piece titled "Don't Build Multi-Agents." Their point: parallel setups are **fragile**, because workers running side by side cannot see each other's work. Each makes small decisions, and those decisions quietly conflict. Their famous example: ask two workers to build a simple game, and one builds a background in one art style while the other builds a character in a clashing style, because neither knew what the other was doing. The pieces do not fit. Their default: "just use a single-threaded linear agent", one agent doing one step after another, with one continuous memory.

> 🔑 **The real boundary: read-heavy and parallelizable vs write-heavy and dependent.** The two teams are not contradicting each other; they are describing two kinds of work. Gathering information from many independent places (nothing one worker finds changes another's job) is where multi-agent shines. Work where each step changes the state and later steps depend on exact earlier ones (editing code) is where a single agent wins. Tellingly, the pro-multi-agent lab admits the same line: "domains that require all agents to share the same context or involve many dependencies between agents are not a good fit."

| | **Multi-agent tends to win** | **Single-agent tends to win** |
|---|---|---|
| Shape of work | breadth-first, parallelizable | sequential, dependent |
| Examples | research, broad search, codebase exploration | editing a codebase, a step-by-step transaction |
| Why | many independent subtasks, more info than fits one window | each action changes state; later steps need exact earlier ones |
| Risk if you choose wrong | overspend on a simple lookup | a bottleneck, or a context window that overflows |

> ❌ **The beginner trap:** reaching for multi-agent by default because it "sounds sophisticated." Most tasks are a single agent's job. Make the second agent prove it is needed.

---

## Part 2: The cost reality (read both numbers, always)

There is a price tag the headline number hides. An agent (one LLM in a loop with tools) already burns far more tokens than a plain chat, because the model re-reads its growing history on every step. A rough figure from the research write-up: a single agent uses on the order of **4 times** the tokens of a chat, and a multi-agent system on the order of **15 times**.

That reframes the 90 percent. It was measured on the team's *own internal* test, not an independent public benchmark, and it came at roughly 15 times the cost. The same team is blunt that multi-agent only pays off "where the value of the task is high enough" to justify the spend.

```text
   single chat        ~1x  tokens
   single agent       ~4x  tokens   (re-reads its history each step)
   multi-agent       ~15x  tokens   (several agents, each with a growing history)

   a 90% quality gain at 15x cost:
     high-value research report  -> probably worth it
     routine lookup              -> a terrible deal
```

> 🔑 **Hold the quality gain and the cost multiplier together.** A 90 percent gain that costs 15 times more is a good deal for a high-value research report and a bad deal for a routine task. The honest unit of measure (carried through this whole course) is **cost per successful outcome**, not cost per token and not quality in isolation.

> ✅ **Always build the single-agent baseline.** Before you ship a fleet, build the one-agent version of the *same* task and compare quality, latency (how long you waited), and token cost. You are not choosing a favorite; you are feeling the trade-off in your own numbers. You do exactly this in the Build.

---

## Part 3: The orchestrator-worker pattern (vendor-neutral, then in each CLI)

The pattern needs no special platform. In plain steps:

```text
        ┌──────────────────────────────────────────────┐
        │              ATLAS  (orchestrator / lead)      │
        │   reads the outcome -> DECOMPOSES into          │
        │   independent subtasks                          │
        └───────┬───────────────┬───────────────┬────────┘
                │ (own context) │ (own context) │ (own context)
                ▼               ▼               ▼
            ┌───────┐       ┌───────┐       ┌────────┐
            │ SCOUT │       │WRITER │       │REVIEWER│
            │research│      │ draft │       │ check  │
            └───┬───┘       └───┬───┘       └───┬────┘
                │ short summary │ short draft   │ short verdict
                └───────────────┴───────┬───────┘
                                        ▼
                              ATLAS synthesizes one
                              coherent final result
```

1. The lead reads the task and **decomposes** it into smaller, independent subtasks.
2. For each subtask, the lead starts a worker in its **own separate context**, so workers do not crowd each other's memory. Give each worker enough **shared context** to avoid the conflicting-decisions trap from Part 1.
3. Each worker does its piece (often by searching or retrieving) and returns a **short, distilled summary**, not its full transcript.
4. The lead collects the summaries and **synthesizes** them into one coherent answer.

Any toolkit can express this, and you can write it yourself with a normal loop and direct model calls. **The pattern is the durable idea, not the tool.**

> 🔑 **Two failure modes to respect.** First, **communication breakdown** between lead and worker: a lot gets lost in translation, just like between two colleagues, so workers need full shared context, not a one-line instruction. Second, **logging is hard**: you must collect transcripts from several agents. Tools that give subagents native, first-class observability solve the second; you solve the first with the context you pass.

### The same pattern in all three CLIs

Subagents are model-neutral. All three leading coding agents ship the orchestrator-worker shape, with different filenames and flags but the identical idea: a lead delegates to a worker that runs in its **own fresh context** and reports back.

| | **Claude Code** (Anthropic) | **Gemini CLI** (Google) | **Codex CLI** (OpenAI) |
|---|---|---|---|
| Where subagents are defined | `.claude/agents/*.md` | `.gemini/agents/*.md` (YAML frontmatter) | `/agent`, threads (`/new`, `/fork`) |
| How the lead invokes them | delegates by role; `isolation: worktree` option | call by `@agent_name`; one level of delegation | spawn a subagent / fork a thread |
| Parallelism | git worktrees, background (`claude --bg`), agent teams (experimental) | run several processes per dir/worktree | **cloud** runs many tasks in parallel, each its own sandbox |
| Observability | per-subagent logging | per-agent transcripts | `/ps`, `/stop`, cloud task view |

> 💡 **Hold the ids loosely.** Filenames, flags, and "agent team" features move fast and differ by version, and Google is moving Gemini CLI's individual tiers to a successor (Antigravity CLI) that carries subagents over unchanged. Verify the exact command against each tool's current docs. What does *not* change is the shape: lead decomposes, worker runs in fresh context, worker returns a summary, lead synthesizes.

> ✅ **The model does not matter to the pattern.** You can run the lead on a strong model and the workers on cheaper, faster ones (the research lab did exactly this). The orchestration is identical whether the workers are Claude, Gemini, or GPT. Pick by ecosystem and price, not by losing the capability.

---

## Part 4: Tool, skill, or subagent? (the decomposition decision)

A subagent is the *heaviest* way to add a capability. Before you spawn one, ask whether a **tool** or a **skill** does the job, because those are cheaper and simpler. This is the decision that keeps a fleet from sprawling.

The common, painful pattern: you ship an agent that works great, then bolt on a capability, then another. Soon the system prompt is hundreds of lines, you have a dozen overlapping tools and tangled subagents, and the agent **regresses** (gets worse) in the very areas it was good at. The fix is not more instructions. It is knowing which **primitive** (basic building block) fits each job.

```text
PICK THE RIGHT PRIMITIVE
  TOOL       -> the agent is doing work it should OFFLOAD to code.
               (esp. code execution for data: let it write a script over a
                CSV instead of reading the whole file into context.)
  SKILL      -> standing knowledge the agent needs SOMETIMES, not always.
               Load it on demand (progressive disclosure). Keep the system
               prompt for only what the agent needs regardless of the task.
  SUBAGENT   -> ONLY to parallelize (throw a lot of agent at a breadth-first
               problem) OR to get a FRESH, context-free mind (e.g. a reviewer
               who did not write the code).
```

> 🔑 **The system-prompt rule.** Keep in the system prompt only what the agent needs *regardless of the task*. Everything situational becomes a **skill**, loaded when the task calls for it. This was the root cause of a real bug in the source workshop: two policies buried in a 400-line prompt contradicted each other, and the agent hallucinated a wrong number. The fix was not a better model; it was moving each policy into its own skill so they could not collide. Fix the context, not the model.

**Tools: start with human-like primitives.** Give the agent the same primitives a human has at a desk: **code execution** (a bash tool to write and run a quick script), **file-system navigation** (read and write files), and **web search**. Add a custom tool only when these genuinely fall short, and reach for an MCP server (a shared, governed tool standard) *last*, only when many clients need the same governed tools. People who "run towards MCP first" end up with chaotic, overlapping servers.

```text
TOOLS: ORDER OF PREFERENCE
  1. Human-like primitives  -> code exec, file system, web search  (start here)
  2. Custom local tools     -> standalone tools only your agent uses
  3. MCP servers            -> only when many clients need the same governed tools
```

**Subagents: keep only the ones that earn it.** Two cases justify one: **parallelize** a breadth-first problem (deep research, broad search, codebase exploration), or get a **fresh mind** with no prior context (a reviewer should not be the agent that wrote the code). And note the frontier trend: as models get smarter, teams are *folding capability back into the orchestrator* because it can now hold more at once. "You just don't need as many subagents." Before adding one, ask whether the lead can simply handle it now.

| Reach for a... | When | AtlasOS example |
|---|---|---|
| **Tool** | the agent should offload mechanical work to code | Scout runs a script over a CSV instead of reading it in |
| **Skill** | the agent needs know-how only sometimes | a "report format" skill the writer loads only when drafting |
| **Subagent** | you need parallelism or a fresh mind | a reviewer with no draft-writing context checks the writer's work |

> 💡 **Measure every change against an eval.** The only honest way to know a decomposition helped is to **hill-climb**: get a baseline score, change *one* thing, re-run your eval, keep what helps, repeat. Change three things at once and the score tells you nothing about which one did the work. (This is exactly the discipline from your evals work, applied to fleet design.)

---

## Part 5: Frameworks, with eyes open

A **framework** is a ready-made library that handles the agent loop's plumbing: the model thinks, calls a tool, reads the result, thinks again. Without one, you write that loop yourself against a model's API. Both are valid. The question is *order*.

> 🔑 **Learn the raw loop first, then adopt a framework deliberately.** A widely cited guide recommends *starting without a framework*, because "many patterns can be implemented in a few lines of code," and frameworks "often create extra layers of abstraction that can obscure the underlying prompts and responses, making them harder to debug." A framework can hide the very things you most need to see when something breaks: the exact prompt sent and the exact response received. This is not "frameworks are bad." It is "understand the loop you are hiding before you hide it."

A fair, even-handed way to decide:

- **Reasons to use one:** it saves you re-writing common plumbing (retries, state, branching, human-approval steps); it gives a team a shared vocabulary; the good ones include built-in tracing.
- **Reasons to skip one:** the task is simple enough to write in a few lines; you need full visibility into every prompt and response; or you want to avoid **lock-in** (becoming so tied to one tool that switching later hurts).

The landscape, by **problem shape**, not by leaderboard (the field moves fast; verify current features yourself):

| Shape | What it offers | Good for |
|---|---|---|
| Explicit stateful graphs | cycles, branching, retries, checkpoints, human-approval steps | complex flows needing tight path control |
| Role-based multi-agent | named roles (planner, researcher, writer) that hand off work | clear division of labor |
| Conversation-style multi-agent | several agents talking, often in parallel | exploratory, discussion-shaped tasks |
| Provider-native runtimes | each major provider's own agent library | staying inside one ecosystem |
| Type-safe, model-agnostic libraries | strong typing, works across providers, native MCP | portability across models |
| Minimal, code-driven libraries | deliberately small, close to the raw loop | when you want the loop, lightly helped |

> ❌ **Pitfalls.** Adopting a heavy framework before you understand the loop it hides. Lock-in that makes switching painful. Copying a trendy tool without asking if it fits your problem. And trusting comparison posts uncritically: many are written by the tool's own vendor, and features change fast, so verify yourself.

> ✅ **The one-sentence rule.** Learn the raw loop first; then, if your problem is complex enough that a framework's plumbing clearly earns its keep, pick the one whose *shape* matches your problem, and keep the underlying prompts and traces visible no matter what you choose.

---

## Key takeaways

1. **One agent is the default; a fleet must earn it.** Multi-agent wins for read-heavy, parallelizable, high-value work. Single-agent wins for write-heavy, dependent work like editing code.
2. **Read both numbers, always.** Multi-agent can cost ~15 times a chat. A quality gain only matters next to its cost multiplier: optimise cost per successful outcome.
3. **The orchestrator-worker pattern is model-neutral.** Lead decomposes, workers run in fresh contexts and return short summaries, lead synthesizes. Claude Code, Gemini CLI, and Codex CLI all ship it; only the filenames and flags differ.
4. **Tool < skill < subagent in weight.** Offload mechanical work to a tool, move situational know-how to a skill, and spawn a subagent *only* for parallelism or a fresh mind.
5. **Learn the loop before the framework.** Adopt one deliberately, by problem shape, and keep every prompt and trace visible.

## Common pitfalls

- ❌ Using multi-agent by default because it "sounds sophisticated."
- ❌ Quoting a quality gain while ignoring the roughly 15-times cost multiplier.
- ❌ Parallelizing dependent work, then getting outputs that do not fit together.
- ❌ Giving a worker a one-line instruction instead of full shared context (the conflicting-decisions trap).
- ❌ Fixing a degraded agent by adding more instructions, tools, or subagents instead of decomposing.
- ❌ Reaching for MCP, or a subagent, first, when a primitive tool or a skill would do.
- ❌ Adopting a heavy framework before you understand the loop it hides.

---

## 🛠️ The Build: the orchestrator fleet (Atlas plus subagents)

> The hands-on payoff. You turn Atlas from a solo agent into a small, justified fleet, and you prove the fleet beats one agent on a task where a fresh mind genuinely helps.

### What you will build

In your AtlasOS repo, you extend **Atlas** (the orchestrator) to dispatch **2 to 3 specialized subagents** for one real outcome: **Scout** researches, a **writer** drafts, and a **reviewer** (a Warden-style fresh mind) checks the draft against the research. Atlas synthesizes the result. Alongside it you commit a short **"tool vs skill vs subagent" decision record**, and a single-agent baseline you compare against on quality, time, and cost.

### Milestones (in order, each fully explained)

**1. Pick one real outcome.** Choose something genuinely breadth-first plus quality-checked, where a fresh reviewer matters. Good example: *"Produce a one-page competitive brief on three named tools, with claims checked against sources."* Research is parallelizable; review needs a context-free mind. Write the outcome in one sentence at the top of a new file `agents/fleet/README.md`.

**2. Build the single-agent baseline first.** Before any fleet, ask your coding agent (Claude Code / Gemini CLI / Codex CLI) to do the whole task as **one** agent in one session. Save the output, the wall-clock time, and (if your tool shows it) the token count. This is your honest comparison point. Do not skip it: the fleet has to *beat* this to justify itself.

**3. Define the three subagents.** Create one definition file per worker in your tool's agents folder (`.claude/agents/`, `.gemini/agents/`, or via Codex `/agent`). Keep each role tight:
   - **Scout** (research): "Gather facts on the three tools from the web and our `memory/` store. Return a short, sourced summary, not a transcript."
   - **Writer** (draft): "Given Scout's summary, write the one-page brief in our report format." (Put the format in a **skill**, loaded on demand, not in the prompt.)
   - **Reviewer** (fresh mind): "You did NOT write this draft. Check every claim against Scout's sources, flag anything unsupported, and return a pass/fail with fixes." This is the subagent that earns its seat: a reviewer must not be the writer.

**4. Pass full shared context to each worker.** In each definition, give the worker enough of the task's shared context to avoid the conflicting-decisions trap: the outcome sentence, the three tool names, the agreed format. A one-line instruction is how fleets produce mismatched pieces.

**5. Make Atlas decompose and synthesize.** Update Atlas's instructions so it: (a) decomposes the outcome into research, draft, review; (b) dispatches Scout, then the writer, then the reviewer, each in its own context; (c) loops the writer once if the reviewer fails it; (d) synthesizes the final one-page brief. Run it and watch the subagents fire in your tool's log or task view.

**6. Write the decision record.** In `agents/fleet/DECISIONS.md`, document one choice for each primitive, in one or two sentences each:
   - a **tool** you used (e.g. web search / code execution for Scout, instead of pasting data into context);
   - a **skill** you used (the report format, loaded only when drafting);
   - a **subagent** you used and *why it earns its seat* (the reviewer needs a fresh mind; or research is parallelizable). Note one capability you deliberately *kept in the orchestrator* rather than spawning a subagent for, and why.

**7. Compare fleet vs baseline.** Put the fleet's output, time, and cost next to Milestone 2's in `agents/fleet/README.md`. Answer in writing: did the fleet produce something one agent could not do as well (e.g. caught an unsupported claim the solo agent shipped)? Was the extra cost worth it for this outcome? Be honest if the answer is "not this time."

**8. Commit it.** Run the git heartbeat from Unit 1:

```text
git add -A
git commit -m "Add Atlas orchestrator fleet: Scout, writer, reviewer"
git push
```

### How you will know you are done

- ✅ Atlas dispatches 2 to 3 named subagents, each running in its own context, and synthesizes one result.
- ✅ The **reviewer** is a genuinely fresh mind (it did not write the draft) and actually flagged at least one thing.
- ✅ `agents/fleet/DECISIONS.md` documents one tool, one skill, and one subagent choice, each justified, plus one capability kept in the orchestrator on purpose.
- ✅ You ran a single-agent baseline and compared it on quality, time, and cost, with a written verdict on whether the fleet earned its keep.
- ✅ The fleet completed a task one agent could not do as well alone (or you can show, with numbers, that for this task one agent was the right call).

> 💡 **If the fleet lost to the baseline, that is a real result, not a failure.** You just learned this task was a single agent's job, and you have the numbers to prove it. That judgment is the whole point of the unit.

---

## Cheat sheet

```text
ONE AGENT OR MANY?
  read-heavy + parallelizable + high-value  -> multi-agent may win
  write-heavy + dependent (editing code)    -> single agent wins
  default to ONE; make the second agent earn its seat

COST REALITY (read BOTH numbers)
  chat ~1x  | single agent ~4x  | multi-agent ~15x tokens
  optimise COST PER SUCCESSFUL OUTCOME; always build the single-agent baseline

ORCHESTRATOR-WORKER PATTERN (model-neutral)
  lead DECOMPOSES -> workers run in OWN context -> return SHORT summaries
  -> lead SYNTHESIZES.  Give workers FULL shared context (avoid clashing decisions).
  Claude Code: .claude/agents/  | Gemini CLI: .gemini/agents/  | Codex: /agent, threads

TOOL vs SKILL vs SUBAGENT
  TOOL      -> offload mechanical work to code (esp. data via code execution)
  SKILL     -> situational know-how, loaded on demand (system prompt = always-needed only)
  SUBAGENT  -> ONLY to parallelize OR for a fresh, context-free mind
  tools order: primitives (code/file/web) -> custom -> MCP (last)

FRAMEWORKS
  learn the raw loop first -> adopt by problem shape -> keep prompts + traces visible
  watch for: hidden prompts, lock-in, vendor comparison posts
```

## How this connects to the rest of the course

- **Next, Unit 8 (Evaluation and review):** the reviewer subagent you built here grows into a real eval gate. You learn to grade a fleet's output honestly and hill-climb its design with evals, the only trustworthy way to know a decomposition helped.
- **Throughout:** Atlas is now a real orchestrator with a fleet, the spine of AtlasOS. Every later unit either adds a worker, hardens the orchestration, or deploys it, but the judgment from this unit (make every agent earn its seat) governs all of it.

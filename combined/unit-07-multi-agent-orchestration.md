# Unit 7: Multi-Agent Orchestration

> **Course:** Agentic Engineering with Claude, a self-paced path *(working title)*
> **Unit 7 of 11:** When to split a job across many agents, when to keep it as one, and how to decompose an agent that outgrew its prompt
> **Sources fused:** Agentic Engineering Modules 10-11 (principles) + Building with Claude Lessons 16 and 19 (implementation)
> **Estimated time:** 90 to 120 minutes (read plus the build)

---

## In one sentence

A multi-agent system (one lead agent splitting work among helper agents) is one of the most powerful and most over-used ideas in the field, so this unit teaches you both halves of the craft: when many agents genuinely beat one (read-heavy, parallelizable, high-value work) versus when one agent wins (write-heavy, dependent work), and the deliberate decomposition that follows (tool vs skill vs subagent), so that when you reach for a second agent you do it with reasons and numbers, not because it sounds sophisticated.

> 🎯 **Where this unit is heading.** The payoff is a **Build** that takes Atlas, your orchestrator, from running one agent (Scout) to dispatching a small fleet: you add a second specialized agent, make the tool-vs-skill-vs-subagent decision deliberately and write it down for the fleet, then prove on your own numbers whether multi-agent actually beat the single-agent baseline. Honest guardrails about when *not* to go multi-agent are part of the deliverable. Jump to **"The Build"** to see the finish line.

## First-principles companion

> 💡 **The durable ideas behind this unit.** The Claude-specific framing is recent; the orchestration ideas are not. For the timeless versions:
>
> - **[How we built our multi-agent research system (Anthropic)](https://www.anthropic.com/engineering/multi-agent-research-system)** (essay). A first-principles treatment of orchestrator-vs-subagent decomposition: when to parallelize, the real cost of subagents, and the communication tradeoffs.
> - **[Building Effective Agents (Anthropic)](https://www.anthropic.com/engineering/building-effective-agents)** (essay). The pattern catalogue (routing, orchestrator-workers, evaluator-optimizer) that frames every choice in this unit, and the case for starting without a framework.
> - **[Don't Build Multi-Agents (Cognition)](https://cognition.ai/blog/dont-build-multi-agents)** (essay). The honest counter-case: why parallel agents are fragile, and the "share full context, not just messages" rule.

## A few plain-language basics first

- **Multi-agent system:** more than one separate agent, each an LLM running in a loop with tools, splitting the work between them.
- **Orchestrator (lead):** the main agent that reads the task, breaks it up, and dispatches the pieces. In your build this is **Atlas**.
- **Worker (subagent):** a separate agent instance with its own context window that the lead hands one piece of work to, and that returns a short summary.
- **Orchestrator-worker pattern:** the most common multi-agent shape: lead decomposes, workers run (often in parallel), lead synthesizes.
- **Breadth-first task:** one where you look in many independent places at once (research), rather than following one chain of dependent steps.
- **Tool / skill / subagent:** the three primitives you decompose into. A **tool** is code the agent runs; a **skill** is packaged info pulled in only when needed; a **subagent** is a separate Claude with its own context.
- **Framework:** a ready-made library that writes the agent loop for you, instead of you wiring it by hand.

You do not need to memorise these. Each returns the first time it matters.

## Why this unit matters

Multi-agent is where good engineers most often over-build. The shape sounds impressive, the demos look magic, and so people reach for it by default. Two well-known engineering teams have publicly disagreed about whether you should, and the useful skill is not picking a winner but knowing where the line between them sits.

> 🔑 **The whole unit in one line.** Multi-agent is a tool with a steep price tag, not a default. Reach for it only when the task is breadth-first, parallelizable, and high-value enough to justify the cost, and when you do build, decompose deliberately: the right primitive (tool, skill, or subagent) for each job, measured against evals.

Get this right and you ship one excellent orchestrator plus the few agents that earn their place. Get it wrong and you ship five fragile demos whose outputs do not fit together and whose bill is fifteen times higher than it needed to be.

## Learning objectives

By the end of this unit you will be able to:

1. State the real boundary between multi-agent and single-agent work (read-heavy/parallelizable versus write-heavy/dependent) and apply it to a task.
2. Build the orchestrator-worker pattern: decompose, dispatch workers in isolated context, synthesize their summaries.
3. Hold quality and cost together, reasoning about the rough 4x (single-agent) and 15x (multi-agent) token multipliers over plain chat.
4. Decide deliberately between a **tool**, a **skill**, and a **subagent** when an agent outgrows its prompt, and document the decision for a fleet.
5. Choose a framework (or none) by the shape of the problem, keeping prompts and traces visible.
6. Extend Atlas to dispatch a second specialized agent and prove, on your own numbers, whether multi-agent beat the baseline.

## Prerequisites

- **From earlier units:** a working agent (Scout) shipped on Claude Managed Agents, an eval suite you can hill-climb on (Unit 8 / Warden seeds), and comfort with tools and MCP (Unit 4).
- **Skills that matter:** reading and running Python, editing a config file, and reading an agent's transcript of tool calls.
- **Skills you can defer:** building your own orchestration framework. You learn the raw loop, then reach for a framework only when it earns its keep.

---

## Part 1: When multi-agent helps and when it hurts (the real debate)

Start with the disagreement, honestly. One AI lab built a research system in the orchestrator-worker shape: a strong model as the lead, several faster cheaper models as workers, each searching the web in parallel. On the lab's own internal test it beat a single agent (same strong model alone) by about **90 percent**. The reason given: workers run in parallel, so the system chases many independent leads at once. Their summary: multi-agent "excels for breadth-first queries that pursue multiple independent directions simultaneously."

Another team published the opposite case, titled "Don't Build Multi-Agents." Their argument: parallel setups are **fragile**, because workers running side by side cannot see each other's work. Each makes small decisions, and those decisions quietly conflict. Their example: ask two workers to build a simple game, and one builds a background in one art style while the other builds a character in a clashing one, because neither knew what the other was doing. From this they draw two rules:

- **Share full context, not just messages.** If you use helpers, give them the whole history, not a one-line instruction. Most failures come from a worker missing context the others had.
- **Actions carry hidden decisions.** Every step commits to something (a name, a format, an approach). When two agents commit to clashing things, merging their output is a mess.

> 🔑 **The two teams do not actually contradict each other.** They describe two kinds of work. The dividing line is **read-heavy and parallelizable** versus **write-heavy and dependent**. The pro-multi-agent lab admits the same boundary in its own write-up: "domains that require all agents to share the same context or involve many dependencies between agents are not a good fit." That is, word for word, the other team's whole argument.

So the takeaway is a rule of thumb, not a winner:

- **Multi-agent tends to win** for research, broad search, and information gathering: many independent subtasks, often more information than fits in one context window.
- **Single-agent tends to win** for sequential, dependent work like editing code, where step three only makes sense given exactly what step two did.

> ❌ **A common mistake:** reaching for multi-agent because it "sounds sophisticated," then parallelizing dependent work and getting outputs that do not fit together. The default recommendation of the skeptical team is blunt: "just use a single-threaded linear agent," and when its memory overflows, add one small model whose only job is to compress the history.

## Part 2: The cost reality (hold both numbers)

There is a price tag the headline numbers hide. An agent (one LLM in a loop with tools) already burns far more tokens than a plain chat, because the model re-reads its growing history on every step. A rough figure: a single agent uses on the order of **4x** the tokens of a chat, and a multi-agent system on the order of **15x**. A token is a small chunk of text you pay for, so 15x the tokens means roughly 15x the cost.

That reframes the 90 percent number. It was measured on the team's *own internal* test, not an independent benchmark, and it came at that much higher cost. The same team is clear: multi-agent only pays off "where the value of the task is high enough" to justify the spend.

> 🔑 **Always hold the two numbers together: the quality gain and the cost multiplier.** A 90 percent quality gain that costs 15x more is a good deal for a high-value research report and a terrible deal for a routine lookup. This is the AtlasOS principle in miniature: **cost per successful outcome, not cost per token.** Cheap models execute in parallel; the expensive lead advises and synthesizes.

> ✅ **Best practice:** never quote a multi-agent quality win without measuring it against a single-agent baseline on cost, not just quality. The honest deliverable is the comparison, not the favorite.

## Part 3: How to build orchestrator-worker, and how Atlas does it

The pattern needs no special platform. In plain steps:

- The lead reads the task and **decomposes** it into smaller, independent subtasks.
- For each subtask, the lead starts a worker in its **own separate context**, so workers do not crowd each other's memory. Give each worker enough shared context to avoid the conflicting-decisions trap.
- Each worker does its subtask (often by searching or retrieving) and returns a **short, distilled summary**, not its full transcript.
- The lead collects the summaries and **synthesizes** them into one coherent answer.

Any agent toolkit can express this, and you can write it yourself with a normal loop and direct model calls. On Claude, two practical refinements come from the implementation side. First, two failure modes to respect: **communication breakdown** between orchestrator and subagent (a lot gets lost in translation, like between two colleagues), and **logging is hard** (you must collect transcripts from multiple agents). Managed agents address both with a **native callable-agents capability**: managed subagents whose logging and observability are as good as the orchestrator's, instead of a subagent hidden inside an opaque tool wrapper.

> 💡 **The frontier trend: fewer subagents.** As models get smarter, many teams are folding capability back into the main orchestrator, because it can now manage more information at once. "You just don't need as many subagents." Before adding one, ask whether the main agent can simply handle it now. This is the same thin-scaffolding instinct from Unit 0: let the model do more as it improves.

## Part 4: Tool, skill, or subagent? (decomposing deliberately)

Here is the decision you make when *one* agent grows too big, which is just as important as the multi-agent question. An agent that gets capability "bolted on" over time (a 400-line system prompt, a dozen overlapping tools, tangled subagents) starts to **regress** in the very areas it used to be great at. The fix is not more instructions. It is moving each job to the right primitive.

| Primitive | Reach for it when... | Why |
|---|---|---|
| **Tool** | The model is doing work it should offload, especially data work. | A bash tool to write and run a script over a CSV beats reading the whole file into context. One workshop task dropped from over 200,000 tokens to a fraction by swapping special tools for code execution. |
| **Skill** | Claude needs the info *sometimes*, not always. | Load it on demand (**progressive disclosure**). Keep the system prompt for "only what Claude needs regardless of task." Separated skills also stop policies contradicting each other. |
| **Subagent** | You want to parallelize (throw a lot of Claude at it) *or* you need a fresh, context-free mind (the reviewer should not be the writer). | These are the only two cases that earn the communication and logging overhead. |

> 🔑 **Start tools with human-like primitives.** Give the agent the same primitives a human has at work: a file system, a browser/web search, and the ability to write and run code. Add custom tools only when these fall short, and reach for MCP last (only when many clients need the same governed tools). On managed agents these primitives come built in.

> 💡 **A worked example.** An overgrown inventory agent shrank from a ~400-line prompt and 12 tools (three were hidden subagent wrappers) to a ~15-line prompt, 3 primitive tools (bash, read, write), business logic moved into skills, and exactly **one** justified subagent (forecasting, kept isolated so the main conversation cannot distort it). The eval score climbed from ~83% to ~92%, and tokens, cost, and latency all dropped. You only knew because you measured: **hill-climb on evals, changing one thing at a time.**

## Part 5: Frameworks, with eyes open

A **framework** is a library that writes the agent loop for you (the model thinks, calls a tool, reads the result, thinks again). Without one you write that loop yourself against a model's API. Both are valid; the question is order.

A widely cited guide recommends **starting without a framework**: "many patterns can be implemented in a few lines of code," and frameworks "often create extra layers of abstraction that can obscure the underlying prompts and responses, making them harder to debug." A framework can hide the very things you most need to see when something breaks: the exact prompt sent and the exact response received.

> ✅ **How to choose, in one sentence.** Learn the raw loop first; then, if your problem is complex enough that a framework's plumbing (retries, state, branching, human-approval steps, built-in tracing) clearly earns its keep, pick the one whose shape matches your problem, and keep the underlying prompts and traces visible no matter what you choose.

> ❌ **Pitfalls:** adopting a heavy framework before you understand the loop it hides; framework **lock-in** that makes switching painful later; copying a trendy tool without asking whether it fits; and trusting comparison posts uncritically, since many are written by the tool's own vendor and features change fast.

## Key takeaways

1. **Multi-agent is a tool, not a default.** Reach for it only when work is read-heavy, parallelizable, and high-value.
2. **The real boundary is read-heavy/parallelizable vs write-heavy/dependent.** The two famous opposing posts agree on exactly this line.
3. **Hold quality and cost together.** Roughly 4x tokens for one agent, 15x for multi-agent. Optimise cost per successful outcome.
4. **Decompose deliberately.** Tool for offloaded work, skill for sometimes-needed info, subagent only to parallelize or get a fresh mind.
5. **Start tools with human-like primitives;** reach for MCP last. Prefer folding work back into the orchestrator as models improve.
6. **Learn the loop before the framework,** and keep prompts and traces visible whatever you choose.

## Common pitfalls

- ❌ Using multi-agent by default because it sounds sophisticated.
- ❌ Quoting a quality gain while ignoring the roughly 15x cost multiplier.
- ❌ Parallelizing dependent work and getting outputs that do not fit together.
- ❌ Giving workers a one-line instruction instead of full shared context (the conflicting-decisions trap).
- ❌ Fixing a degraded agent by adding more instructions, more tools, or more subagents.
- ❌ Hiding subagents inside tool wrappers, losing observability and inviting communication breakdowns.
- ❌ Adopting a framework before you understand the loop it hides.

---

## 🛠️ The Build: Atlas at fleet scale

> The hands-on payoff. Until now Atlas dispatched one agent, Scout. Here you turn Atlas into a real orchestrator of a small fleet: it decomposes an outcome, dispatches Scout plus one more specialized agent, and synthesizes the result. You make every tool-vs-skill-vs-subagent call deliberately, document it for the fleet, and prove on your own numbers whether multi-agent actually won. This fuses the orchestrator-worker pattern (principles), the decomposition decision (Lesson 16), and the hill-climbing discipline (Lesson 19). It builds the `orchestrator/` and `agents/` components in your roadmap.

### What you will build

An Atlas orchestrator that takes one high-level outcome (for example "produce a competitive-intel brief on three rival products"), decomposes it, dispatches **Scout plus one second agent** (each in its own context), and synthesizes their summaries into one answer, committed to AtlasOS with a written fleet decision record and an honest single-agent comparison.

### Milestones (in order, each stands alone)

1. **Pick the second agent and justify it.** Choose one more specialist whose work is genuinely independent of Scout's (for example **Herald** drafting the brief from Scout's findings, or a second Scout-style researcher covering a separate product). In two sentences, state why this is breadth-first, parallelizable work and not write-heavy, dependent work. If you cannot make that case, the honest move is to keep it single-agent, and you say so.
2. **Make Atlas the orchestrator.** Have Atlas decompose the outcome into independent subtasks and dispatch one worker per subtask, each in its own context, each given enough shared context to avoid clashing decisions. Use the native callable-agents capability so each subagent logs as cleanly as Atlas. Have each worker return a short distilled summary, and have Atlas synthesize.
3. **Make the decompose decision and document it for the fleet.** For each capability in the run, write down whether it is a **tool**, a **skill**, or a **subagent**, and why. Keep the system prompt to "only what Atlas always needs"; push situational logic into skills; keep only subagents that parallelize or need a fresh mind. Save this as a short `orchestrator/FLEET-DECISIONS.md` the whole fleet can follow.
4. **Run the single-agent baseline.** Build the exact same task as one linear agent (Scout doing everything in one context, compressing history if it overflows). Run both versions.
5. **Compare on three numbers and decide.** Record **quality, latency, and token cost** for multi-agent vs single-agent. Write one paragraph: which would you ship for this task, and why, using your own numbers and the 4x/15x framing. Honesty includes "single-agent won here."
6. **Stretch.** Add the guardrails note: list two tasks in your AtlasOS roadmap where you would deliberately *not* go multi-agent, and why. Then try folding the second agent's job back into Atlas (the frontier "fewer subagents" move) and check whether the orchestrator can now just handle it.

### How you will know you are done

- ✅ Atlas dispatches at least two specialized agents in isolated context and synthesizes their summaries into one coherent answer.
- ✅ Subagents log cleanly (native callable agents), with no opaque tool wrappers.
- ✅ `FLEET-DECISIONS.md` records each tool/skill/subagent choice with a reason.
- ✅ You have a single-agent baseline and a numbers-backed paragraph on which you would ship and why.
- ✅ You can name at least one case where you chose *not* to go multi-agent, with the reason.
- ✅ The fleet orchestration is committed to your AtlasOS repo.

> 💡 If your multi-agent version did not beat the baseline on cost-adjusted quality, that is not a failure of the build, it is the lesson. Commit the comparison anyway; it is the most honest artifact in the unit.

---

## Cheat sheet

```text
SHOULD YOU GO MULTI-AGENT?
  READ-heavy + parallelizable + high-value  -> yes (research, broad search)
  WRITE-heavy + dependent (state changes)   -> no  (editing code; one linear agent)
  the two famous opposing posts agree on THIS line

THE COST REALITY (hold both numbers)
  ~4x tokens  = single agent vs chat
  ~15x tokens = multi-agent vs chat
  optimise COST PER SUCCESSFUL OUTCOME, not cost per token
  always compare against the single-agent baseline

ORCHESTRATOR-WORKER
  lead DECOMPOSES -> workers run in OWN context (give shared context) ->
  workers return SHORT summaries -> lead SYNTHESIZES
  use native callable agents (clean logging) · watch communication breakdowns
  frontier trend: FEWER subagents as models improve

PICK THE PRIMITIVE
  TOOL      -> offload work the model is doing (esp. code exec over data)
  SKILL     -> info needed SOMETIMES; load on demand (progressive disclosure)
  SUBAGENT  -> only to PARALLELIZE or get a FRESH, context-free mind
  tools order: Claude primitives -> custom local -> MCP (last)

FRAMEWORKS, EYES OPEN
  learn the raw loop first · pick by problem shape, not popularity
  keep prompts + traces visible · beware lock-in and vendor comparisons
```

## How this connects to the rest of the course

- **Earlier, Unit 4 (Tools and MCP):** the primitives and MCP order-of-preference you now decompose onto.
- **Earlier, Unit 6 (Workflows and agent patterns):** the single-agent loop multi-agent is measured against.
- **Companion, Unit 8 (Evals and verification):** the hill-climbing harness and Warden graders that make every decompose decision measurable, not guessed.
- **Next, Unit 9 (Production):** you deploy this fleet on real infrastructure, where the cost multiplier and clean per-agent logging stop being theory.

---

*Unit 7 of the combined path. Fuses the vendor-neutral principles of Agentic Engineering Modules 10-11 with the Claude-specific implementation of Building with Claude Lessons 16 and 19. Token multipliers, eval scores, and architecture details are drawn from the source write-ups; adapt model ids and SDK details to the current docs.*

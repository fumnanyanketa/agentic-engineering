# Unit 11: Capstone and Operating Model

> **Course:** Agentic Engineering, a model-agnostic self-paced path *(working title)*
> **Unit 11 of 12:** Assemble every component from Units 1 to 10 into AtlasOS v1, then ship ONE flagship vertical (Pulse, an agentic analytics harness) against a real data source, and set up how a solo founder plus an agent fleet actually operates
> **The how, across tools/models:** model-agnostic by design (works with whichever agent and model you chose: Claude, Gemini, or GPT); illustrated with the analytics, trading, compliance, legal, and product case studies, plus the leadership operating model
> **AtlasOS build:** AtlasOS v1, the whole platform wired together, with Pulse as the proven flagship vertical
> **Estimated time:** 3 to 5 hours (this is the finale; most of it is integration and one real vertical)

---

## In one sentence

This is the capstone: you take the parts you have built one unit at a time (the orchestrator Atlas, the memory Cortex, the agent Scout, the eval gatekeeper Warden, the tools layer, and the deployment) and wire them into ONE system that accepts a high-level outcome and runs it end to end, then you prove the platform is real by standing up a single flagship vertical, Pulse, an agentic analytics harness, against an actual data source, and finally you write down the operating model: how you, one founder plus a fleet of agents, actually run this thing.

> 🎯 **Where this unit is heading.** The payoff is a **Build** where AtlasOS goes from "a folder of components" to "a platform." You give Atlas an outcome in plain English (the hero outcome from your company brief, like "produce this week's business review"), and the fleet plans it, dispatches the right agents, checks itself against Warden, remembers what it learned in Cortex, and hands you the result with a human-in-the-loop step for the decision that matters. Then you build **Pulse**, the analytics vertical, against a real dataset so the platform has one thing it is genuinely good at. Jump to **"The Build"** to see the finish line, then come back and we will assemble it together.

## First-principles companion

> 💡 **The durable ideas behind this unit.** The capstone is about *integration*, the discipline of making separate pieces work as one dependable system. These are the timeless versions, copied from the source lessons (optional, read them any time):
>
> - **[Semantic layer](https://en.wikipedia.org/wiki/Semantic_layer)** (essay). The heart of the analytics vertical: mapping business meaning onto raw data so non-experts (and now agents) get correct answers.
> - **[The SPACE of Developer Productivity](https://www.microsoft.com/en-us/research/publication/the-space-of-developer-productivity-theres-more-to-it-than-you-think/)** (paper). Why "lines shipped" is the wrong measure once an agent fleet does the building, and what to measure instead.
> - **[Theory of constraints](https://en.wikipedia.org/wiki/Theory_of_constraints)** (essay). The operating-model spine: when one bottleneck (coding) disappears, find the next one (verification, review) and run the org around it.
> - **[Human-in-the-loop](https://en.wikipedia.org/wiki/Human-in-the-loop)** (essay). The principle behind keeping a person on the decisions that genuinely need judgment, while letting the fleet own the rest.

## A few plain-language basics first

New terms, in plain words. Each is explained again the moment it matters.

- **Capstone:** the final project that proves the whole course. There is no new concept here; the skill is *integration*, making the parts you already built cooperate.
- **Orchestration platform:** a system where one coordinating agent (Atlas) plans the work and delegates pieces to other agents and tools, rather than one agent doing everything alone.
- **Vertical:** one specific, real use case the platform is genuinely good at (here, analytics). A platform proves itself by doing one vertical well, not five demos badly.
- **Harness:** all the code around the model: the loop, the tools, error handling, checkpointing. The model is the engine; the harness is the car. A great agent is **model + harness + context**.
- **Semantic layer:** a translation layer on top of raw data that tells the system how to use it correctly: which table matters, what your terms mean, who can see what. It is the heart of the analytics vertical.
- **Trace:** a detailed record of an agent's inner workings during a run: what it thought, which tools it called, what came back. Reading traces is how you debug an agent.
- **Definition of done:** the explicit list of conditions that must all be true for the work to count as finished. Your company brief gives AtlasOS its definition of done.
- **Human-in-the-loop (HIL):** a deliberate point where the system stops and asks a person to approve or decide, reserved for choices that genuinely need judgment.
- **Operating model:** the written answer to "how does this actually run day to day": who (founder vs. fleet) owns what, how work is reviewed, and how it scales.

## Why this unit matters

Every earlier unit handed you one component in isolation. That is correct for learning, but a pile of correct components is not a system. The job that enterprises actually hire agentic engineers for is *integration*: making orchestration, tools, memory, evaluation, observability, and safety work together as one thing you can trust. This unit is where AtlasOS stops being a roadmap and becomes a platform, and where you prove it by pointing it at one real problem.

> 🔑 **Integration is the skill, not another feature.** There is no new trick in the capstone. The difficulty, and the value, is in making everything you already know cooperate as one dependable system that takes an outcome and returns a trustworthy result.

## Learning objectives

By the end of this unit you will be able to:

1. Wire the AtlasOS components from Units 1 to 10 (Atlas, Cortex, Scout, Warden, tools, deploy) into one system that takes a high-level outcome and runs it end to end.
2. Choose and ship ONE flagship vertical, and explain why one excellent vertical beats five demos.
3. Build Pulse, an agentic analytics harness, with a semantic/context layer, an error-recovering loop, and trace-driven debugging, against a real dataset.
4. State a clear definition of done that matches your company brief's hero outcome, including a human-in-the-loop step.
5. Write a simple operating model: how a solo founder plus an agent fleet divides ownership, reviews work, and scales.

## Prerequisites

- **The components from Units 1 to 10.** You should have a working agent (Scout), a memory layer (Cortex), an eval gatekeeper (Warden), an orchestrator loop (Atlas), a tools/MCP layer, and a deployment. If any are thin, that is fine; the Build tells you the minimum each must do.
- **Your workstation and `atlasos` repo from Unit 1**, plus the coding agent you chose.
- **One real dataset you understand** for the Pulse vertical: a CSV, a SQLite file, a data export. It needs fields whose meaning is not obvious and at least one ambiguous term.
- **Your company brief** (`atlas/00-company-brief.md`), which defines the hero outcome AtlasOS must hit.

---

## Part 1: The capstone is integration, not invention

The capstone module is blunt about this: "There is no new concept to learn here. The skill on display is integration, which means making all the separate pieces work together as one dependable system." That is exactly what an enterprise pays an agentic engineer to do, and it is its own discipline.

So the work of this unit is not to add a clever new component. It is to take the components you already have and make them cooperate around a single contract: **you give Atlas a high-level outcome, and the system returns a trustworthy result, on its own, with you in the loop only for the decision that genuinely needs you.**

Here is the shape you are assembling, the same diagram from your architecture map, now read as a runtime, not a roadmap:

```text
   you (founder) ─── high-level outcome ──▶ ┌───────────────────────────┐
                                            │  ATLAS · the orchestrator │
                                            │  plan → dispatch → check  │
                                            └─────────────┬─────────────┘
                       ┌──────────────┬──────────────────┼──────────────┐
                       ▼              ▼                  ▼              ▼
                   ┌───────┐      ┌───────┐          ┌───────┐      ┌────────┐
                   │ SCOUT │      │ PULSE │          │ ...   │      │ WARDEN │
                   │research│     │analytics│        │(others)│     │ evals  │
                   └───┬───┘      └───┬───┘          └───────┘      └───┬────┘
                       └──────────────┴── read/write ──┐               │
                                          ┌────────────▼───────┐  gate │
                                          │  CORTEX · memory    │◀──────┘
                                          └─────────┬──────────┘
                                  ┌─────────────────┼─────────────────┐
                                  ▼                 ▼                 ▼
                            TOOLS / MCP        DEPLOY (cloud)     OPS (logs,
                            web, db, fs        survives laptop    cost, HIL)
                                               closing
```

> 🔑 **One contract ties it together.** Outcome in, trustworthy result out, nothing ships past Warden, and a human approves the consequential step. If you can describe your system in that one sentence, you have integrated it.

> ❌ **The capstone trap:** trying to make all seven agents perfect at once. The brief is explicit: "One excellent agent plus a real orchestrator beats five demos." Integrate what you have, prove it with one vertical, and stop.

---

## Part 2: The exit bar (what "real" means)

A demo and a platform look the same in a screenshot. The difference is the exit bar: the list of properties a system must have before it counts as real. The capstone module gives this bar, and each item points back to a unit where you already built the skill. Hold yourself to it.

| # | Property | What it means | Built in |
|---|---|---|---|
| 1 | **Orchestration** | A lead agent (Atlas) breaks a task into pieces and delegates to specialized workers, *and* a deliberate decision about whether you even need more than one agent. | Units 7, 8 |
| 2 | **Tools via MCP** | Real capabilities exposed through MCP, including at least one tool you built yourself. | Unit 5 |
| 3 | **Retrieval and memory** | A way to find relevant information and to store/compact it so the system stays coherent across long tasks (Cortex). | Units 5, 6 |
| 4 | **The loop done right** | A bounded loop (capped steps), self-check steps, and sensible stopping conditions so the agent knows when it is done or stuck. | Unit 7 |
| 5 | **An evaluation suite** | Automated tests built from real failures, with a pass rate per component (Warden). | Unit 4 |
| 6 | **Observability** | Full tracing of every step, with cost and latency recorded, so you can see inside the running system. | Units 6, 9 |
| 7 | **Safety** | Least privilege, a human-approval step before any consequential action, and a written defense against prompt injection. | Unit 9 |
| 8 | **Hardening** | A per-task budget for cost and latency, the right model size per job, caching where it helps, graceful fallbacks. | Unit 10 |

> 💡 **The bar is model-agnostic on purpose.** Not one row mentions a specific model or vendor. AtlasOS is built so the capstone works whichever agent and model you chose. Where a step picks a model (small for one-shot, larger for long loops), treat the choice as a knob you turn per task, not a brand you marry.

> 🔑 **"You are an agent orchestrator when you can":** stand up a system that splits work across agents, ground it in tools and data via MCP, manage context across long tasks, *prove* its reliability with evals and traces, defend it against prompt injection, state its cost per task, and explain every design decision along with the alternative you rejected. That is not a hobby project. That is the job.

---

## Part 3: Pick ONE flagship vertical (and why analytics)

A platform earns the name by doing one real thing well. The course gives you a gallery of proven verticals to choose from, each a real company that shipped an agent into a hard domain:

| Vertical | Real-world proof | The durable lesson it teaches |
|---|---|---|
| **Analytics (Pulse)** | Omni's "Blobby" | A great agent is model + harness + context; read the traces to fix it. |
| Trading signals | Man Group | Your organizational context is the asset; govern skills like production code. |
| Financial crime | Qonto | One audited gateway (auth, RBAC, audit trail, HIL) makes sensitive data safe to use. |
| Legal review | Legora, Solve Intelligence | Make a vertical harness *look like* a coding harness; cite everything. |
| Product building | Lovable | Make "stuck" a metric; self-heal; prune knowledge that has gone stale. |

**For your capstone, the flagship defaults to analytics, "Pulse."** Analytics is the best first vertical for three concrete reasons. First, it exercises every row of the exit bar at once: a question becomes a plan (orchestration), runs against data through a tool (MCP), needs business meaning to be correct (memory/context), and must be checked for the *same right answer every time* (evals). Second, it has a clean, durable structure (the semantic layer) you can reuse. Third, it produces something you will actually look at, which is the only way real problems surface.

> 🔑 **One excellent vertical, not five.** The other four verticals are not wasted; they are an appendix you can mine later (Part 6). But your capstone proof is Pulse. A platform that answers real questions about real data, correctly and repeatably, is more convincing than five half-built demos.

The lesson behind Pulse comes from Omni's CTO, whose analytics agent "Blobby" grew over 18 months. The single most quoted line: **"a great agent is a model plus a great harness plus your business context placed right next to the data it describes."** You are going to build a small version of exactly that.

---

## Part 4: How Pulse works (model + harness + context)

Pulse answers a plain-language question about your data by turning it into a database query, running it, and explaining the result. Three layers make it good, and a fourth habit keeps it honest.

**The context layer (the semantic layer).** The model is "incredible at answering questions" in general but knows nothing about *your* business. Even "last quarter" is ambiguous: in engineering it means the calendar quarter; in sales it means the fiscal quarter. The semantic layer encodes that. It does three jobs:

```text
SEMANTIC LAYER (sits on top of your raw data)
  curate    -> which of the 100 "revenue" tables actually matters, and how to join
  encode    -> meaning, terminology, ambiguous terms ("last quarter" = ?)
  permit    -> who is allowed to see what
```

The trick that punches above its weight: for each field, add three small annotations, **right next to the field definition** (the same way a `CLAUDE.md` / `GEMINI.md` / `AGENTS.md` memory file lives next to the code it describes):

- **AI context:** a note written for the model, how to use this field, what to reference.
- **Sample query:** "here is the query you would run to answer a question like X." Grounds the model in real usage.
- **Example values:** a taste of the real values (regions: EMEA, NAM, APAC). The model infers the rest and learns abbreviations, so "United States" maps to "US."

> 💡 **Context belongs next to what it describes.** Omni drew the analogy directly to coding agents: "the more you can do to localize that context next to the parts of the code that it applies to, the better results you're going to get." A separate context file far from the data is the weak version.

**The harness (the loop).** Wrap the model in an agentic loop with tasks, checkpointing, and, above all, **error recovery**. One of the earliest big quality jumps at Omni came from two simple moves: tell the agent how to recover and give it a budget to do so, and invest in *great error messages* that say what went wrong and how to fix it. The loop's superpower is recovering from errors, and that depends entirely on the message it gets back.

**The model choice (a knob, not a brand).** Pick the model that fits the *conversation*, not the task in the abstract. A one-shot question and answer can use a small, fast model; multi-step agentic loops need a larger one. Omni started on a small model and switched up once conversations got long. This is the model-agnostic principle in action: the choice is per-task, and works with whichever provider you chose.

**The habit that beats clever prompts: read the traces.** When a session goes wrong, do not guess and tweak the prompt. Capture the trace (the agent's inner steps) and read it. Omni's "random bad sessions" turned out to be "rooted in real problems," and reading traces is what found them. The biggest find was a **split brain**: an outer agent that knew the data delegated query-writing to a sub-agent that did not, producing surprising failures. The fix, "consolidating the brain," was to pull the query tools up into one agent so there is one mind, not two.

> ❌ **The split-brain bug.** Do not divide knowledge and capability across an outer agent and a sub-agent that cannot see each other's world. Consolidate. And lean on what the model is already great at (SQL) instead of inventing a proprietary format you have to teach it.

---

## Part 5: The definition of done (your hero outcome)

A capstone needs a finish line you can point at. Yours is written in your company brief, and AtlasOS v1 is "done enough to be proud of" when all of these are true. This is the exit bar, restated as *your* outcome:

```text
ATLASOS v1 - DEFINITION OF DONE  (from atlas/00-company-brief.md)
  [ ] You give Atlas a high-level OUTCOME (e.g. "produce this week's
      business review" or "keep our competitive intel current") and
      the fleet executes it END TO END.
  [ ] Every agent's output is graded by WARDEN, and regressions are caught.
  [ ] The system has MEMORY (Cortex): it remembers across runs and improves.
  [ ] It runs on REAL CLOUD infra, is observable, and survives you
      closing your laptop.
  [ ] A HUMAN-IN-THE-LOOP step exists for the decisions that need judgment.
  [ ] At least ONE FLAGSHIP VERTICAL (Pulse) works against a real use case.
```

Notice the unit of work: not "do this one task once," but "own this outcome over time." That is the whole point of the platform. The hero outcome you choose should be one sentence a non-technical person would understand ("produce this week's business review") that the fleet can genuinely run without you babysitting each step.

> 🔑 **Cost per successful outcome, not cost per token.** When you state done, state the per-task cost and latency too. Cheap models execute; the expensive model advises only when needed. A platform that produces the right answer for a known, modest cost is worth more than one that is merely fast.

> ✅ **Build in public.** The brief and the capstone module agree: publish the journey, one short write-up per phase, "including what broke and how I fixed it." The series itself is the proof of the skill. You do not need a polished SaaS; you need a real platform and an honest log.

---

## Part 6: Appendix, applied gallery (optional)

Off the required path. You build Pulse for your capstone; these four other verticals are real, shipped systems whose lessons you can borrow now or later. One short paragraph each; nothing here is deleted, just optional.

- **Trading signals (Man Group, Lesson 32).** At a regulated firm running real institutional capital, the defensible asset is your *own organizational context*, not the model. Workflows must be captured as skills and governed like production code (each with an owner, evals, visibility, usage tracking, and a retirement plan) before rollout, because a power user's skill with hardcoded personal assumptions silently breaks at scale. Source: [talk](https://www.youtube.com/watch?v=EOg4gY0Yln0), durable read: [Algorithmic trading](https://en.wikipedia.org/wiki/Algorithmic_trading).

- **Financial crime (Qonto, Lesson 33).** To put AI on sensitive, regulated data, you do not wire the model straight into your systems. You build a single audited **MCP gateway** that enforces strong auth, short-lived signed tokens, role-based access as code, an append-only audit trail, and human-in-the-loop, all in one place. Evals on tool choice, grounding, and reasoning are what earn the trust to move gradually from human-*in* to human-*on* to human-*out* of the loop. Source: [talk](https://www.youtube.com/watch?v=tUoO4ucrNc0), durable reads: [FATF](https://en.wikipedia.org/wiki/Financial_Action_Task_Force), [Anti-money laundering](https://en.wikipedia.org/wiki/Anti-money_laundering).

- **Legal review (Legora and Solve Intelligence, Lessons 34 and 35).** Coding agents are years ahead of every other field, so the fastest way to build a vertical agent is to sort each capability into *reuse* (universals like planning and HIL), *translate* (mimic the coding harness's read-edit-verify loop), and *invent* (the grounded last 20%). Making a legal harness *look like* a coding harness lets it inherit coding-focused training, even on a small model. But delegation is not universal: where outputs cannot be cheaply validated and decisions are entangled (patent drafting), impart judgment sequentially, with citations as a first-class audit trail. Sources: [Legora talk](https://www.youtube.com/watch?v=nho1YAEPuwA), [Solve talk](https://www.youtube.com/watch?v=T8N0MED3IJo), durable reads: [Code reuse](https://en.wikipedia.org/wiki/Code_reuse), [Human-in-the-loop](https://en.wikipedia.org/wiki/Human-in-the-loop).

- **Product building (Lovable, Lesson 36).** When millions of non-technical people build software with AI, the dominant problem is users getting *stuck*, so make "stuck" a measurable metric, inject adapted fixes before users hit a wall, and give the agent a tool to vent its own frustration into reviewable PRs. The discipline that makes it work is constant tuning and aggressive pruning, because model-specific knowledge has a half-life. Source: [talk](https://www.youtube.com/watch?v=mhW-XXnDFSU), durable reads: [Lean startup](https://en.wikipedia.org/wiki/Lean_startup), [The SPACE of Developer Productivity](https://www.microsoft.com/en-us/research/publication/the-space-of-developer-productivity-theres-more-to-it-than-you-think/).

---

## Part 7: Appendix, the operating model (optional)

Off the required path. AtlasOS is a one-founder-plus-fleet venture, so "how does it run day to day" deserves a written answer. These are the durable moves from the leadership lessons, condensed.

**Who owns what (Lesson 27).** When coding stops being the bottleneck, the constraint moves to *verification, review, and maintenance*. Split work explicitly: the fleet handles style, obvious bugs, and spec drift; you stay the owner of legal, risk and trust boundaries, product sense, and taste. Measure outcomes, not throughput, and audit your own processes continually ("is this still serving its purpose?"). Durable read: [Theory of constraints](https://en.wikipedia.org/wiki/Theory_of_constraints).

**Start tiny, scale deliberately (Lessons 28 and 29).** A bet starts as "one person with their good buddy Claude" finding the spark, then grows in small steps where everyone does everything. Right-size process to team size: a one-skill hack at five people, a heavy system only at eighty; building the heavy system too early is the crime. Scale by *encoding taste from past actions* (distill a reviewer from your past PR comments) instead of convening committees, and read the cheap free signal of user frustration. Durable reads: [Lean startup](https://en.wikipedia.org/wiki/Lean_startup), [The Mythical Man-Month](https://en.wikipedia.org/wiki/The_Mythical_Man-Month).

**Verification grants autonomy (Lesson 30).** At Spotify, a fleet of agents applies routine changes, verifies each by running real CI, and auto-merges the safe ones with no human in the loop (millions of automated PRs). The enablers: make the codebase agent-friendly through intentional standardization, and expose the platform to agents as MCP and CLI tools. The pattern for AtlasOS: a check the agent can run itself is what lets it act unsupervised; human judgment relocates to the riskiest changes and to deciding *what* to build. Durable read: [The SPACE of Developer Productivity](https://www.microsoft.com/en-us/research/publication/the-space-of-developer-productivity-theres-more-to-it-than-you-think/).

**Governance and rollout (Lesson 31).** In a larger org, plug agents into *existing* workflows (assign a ticket to the agent; wire CI failures back to it) rather than inventing new interfaces, spread adoption through a skills marketplace and a community channel, and treat each new model as a different beast to re-harness (prompts may not transfer; get A/B testing ready before switching). For review, a "council of agents" (several different models reviewing the same change) lifts success rates at modest cost. Durable read: [Accelerate (HBR)](https://hbr.org/2012/11/accelerate).

> 🔑 **The operating model in one line.** The fleet builds and checks; you own taste, risk, and the call to ship. As you scale, encode your judgment into skills and evals so the fleet inherits it, and keep moving the human to wherever the new bottleneck is.

---

## Key takeaways

1. **The capstone is integration, not invention.** Make the components you already built cooperate as one dependable system: outcome in, trustworthy result out.
2. **Hold yourself to the exit bar.** Orchestration, MCP tools, retrieval and memory, a bounded loop, evals, observability, safety, and hardening. Each maps to a unit you finished.
3. **Ship ONE flagship vertical.** Analytics (Pulse) is the default because it exercises the whole bar and produces something you will actually look at. One excellent vertical beats five demos.
4. **A great agent is model + harness + context.** The semantic layer (context next to the data), an error-recovering loop, the right model per conversation, and trace-driven debugging.
5. **Read the traces; avoid the split brain; lean on SQL.** Operating an agent is mostly reading what it actually did and fixing the real root cause, not guessing at prompts.
6. **Define done from your company brief.** End to end on an outcome, graded by Warden, with memory, on real cloud, with a human-in-the-loop step, and one vertical proven.
7. **Write the operating model.** The fleet builds and checks; you own taste, risk, and the ship decision; encode your judgment as skills and evals; keep the human at the moving bottleneck.

## Common pitfalls

- ❌ Trying to perfect all seven agents at once instead of integrating what you have and proving it with one vertical.
- ❌ Calling a demo a platform: no evals, no traces, no cost number, no human-approval step on the consequential action.
- ❌ Asking the analytics agent business questions with no semantic layer, so it answers about businesses in general, not yours.
- ❌ Stashing context in a file far from the data it describes, instead of next to each field.
- ❌ Skimping on error messages, so the loop cannot recover.
- ❌ Guessing at why the agent failed and tweaking the prompt, instead of reading the trace first.
- ❌ Splitting knowledge and capability across an outer agent and a sub-agent that cannot see each other.
- ❌ Marrying a single model id; the model is a per-task knob, and the whole platform is built to be model-agnostic.

---

## 🛠️ The Build: AtlasOS v1, with Pulse proven

> This is the finale. By the end, AtlasOS stops being a folder of components and becomes a platform: you hand Atlas an outcome, the fleet runs it end to end through Warden with a human-in-the-loop step, Pulse answers real questions about a real dataset, and you have written down how the whole thing operates. We do every step together, and it is worth pausing to notice: you are about to finish the thing.

### What you will build

AtlasOS v1: the components from Units 1 to 10 wired into one system that takes a high-level outcome and runs it to a trustworthy result, plus **Pulse**, an agentic analytics harness, working against a real dataset you understand, plus a one-page operating model. The deliverable is a tagged release of your `atlasos` repo, a short "definition of done" you can tick off, and a build-in-public write-up.

### Milestones (in order, each fully explained)

**1. Inventory your components.** Open your `atlasos` repo in VS Code and confirm each piece exists, even if small: `orchestrator/` (Atlas: a loop that plans and dispatches), `agents/` (Scout), `memory/` (Cortex), `evals/` (Warden), `tools/` (at least one MCP tool you built), `deploy/` (a cloud target), `ops/` (logs and cost). Ask your agent: *"List the AtlasOS components in this repo and, for each, say in one line what it currently does and what is missing for it to run end to end."* Read the answer. This is your punch list.

**2. Write the one contract.** In `orchestrator/`, make Atlas accept a single high-level outcome string and return a result. Ask your agent, in plan mode first: *"Make Atlas take one plain-English outcome, decompose it into steps, dispatch each step to the right agent (Scout, Pulse), and loop until Warden passes or it asks me for the human-in-the-loop decision. Bound the loop to a sane step cap with clear stopping conditions."* Read the plan, then let it build. This is the spine of the platform.

**3. Wire Warden as the gate.** Connect your eval suite so nothing is returned as "done" until it passes Warden's checks, and so a regression is caught. Ask: *"Before Atlas returns a result, run it through Warden's checks and refuse to finish if any fail. Print a per-component pass rate."* Confirm you see pass rates, not just a final answer.

**4. Wire Cortex and the human-in-the-loop step.** Make the run write what it learned to Cortex (so the next run is better) and stop at exactly one consequential decision to ask you. Ask: *"Store the key facts from this run in Cortex so the next run reuses them, and insert one human-approval pause before the consequential action, showing me what it is about to do."* You should be asked once, not babysit every step.

**5. Stand up Pulse against a real dataset.** Put your dataset (a CSV or SQLite you understand) into the repo. Then build Pulse in the order from Part 4:
   - **Context layer:** for three or four fields, add an AI-context note, one sample query, and a few example values, right next to each field's definition. Include one ambiguous term (your "last quarter").
   - **The loop:** wrap query generation in a loop with error recovery and *descriptive* error messages, and let the model write SQL directly (do not invent a custom format).
   - Ask your agent: *"Build Pulse: answer a plain-English question about this dataset by writing SQL directly, running it, and explaining the result. Use the field annotations as context, recover from a failed query using a descriptive error message, and log the full trace of each run."*

**6. Operate Pulse with traces.** Ask Pulse three genuinely tricky questions, including one that needs the ambiguous term resolved and one with a typo or abbreviation in a value. When one goes wrong, open the trace and read it before changing anything. Fix the real root cause (watch for the split brain if you used a sub-agent). Keep a short "blubotomy log" of what the trace revealed and what you fixed.

**7. Give Atlas the hero outcome.** Now run the whole platform on the outcome from your company brief, for example: *"Produce this week's business review,"* where Pulse supplies the numbers. Watch Atlas plan, dispatch to Pulse (and Scout if relevant), pass through Warden, write to Cortex, and pause for your one approval. Read the result like an engineer.

**8. Tick the definition of done and tag the release.** Walk the checklist from Part 5 and tick each box that is true. Then save and tag the milestone:

```text
# Save your work.
git add -A
git commit -m "AtlasOS v1: components integrated, Pulse vertical proven"

# Tag this as the version-1 release and push the tag.
git tag -a v1.0 -m "AtlasOS v1: end-to-end outcome run + Pulse analytics vertical"
git push --follow-tags

# What you'll see:
...
 * [new tag]         v1.0 -> v1.0
```

**9. Write it up (build in public).** Add a short `WRITEUP.md` (or a post) covering: the outcome you ran, the architecture and one trade-off you chose (single vs. multi-agent), your Warden pass rates, the per-task cost and latency, your prompt-injection note, and one bug a trace revealed. One honest page. That page is the proof.

**10. Write the one-page operating model (optional but recommended).** In `ops/`, write who owns what (fleet builds and checks; you own taste, risk, and the ship call), how review works (Warden plus your human-in-the-loop), and the one thing you would do first to scale. Use Part 7 as the template.

### How you will know you are done

- ✅ You give Atlas one plain-English outcome and the fleet runs it end to end, dispatching to the right agents.
- ✅ Nothing returns as "done" until it passes Warden, and you can see a per-component pass rate.
- ✅ Cortex stores what a run learned, and the next run reuses it.
- ✅ The system pauses exactly once for a human-in-the-loop decision, not at every step.
- ✅ Pulse answers real questions about your dataset, resolves your ambiguous term by context (not luck), and fuzzy-matches a typo or abbreviation.
- ✅ Your blubotomy log shows at least one bug you found *only* by reading a trace, and its fix.
- ✅ You can state the per-task cost and latency, and you tagged a `v1.0` release.
- ✅ Every box in the Part 5 definition of done is ticked, and you wrote it up in public.

> 💡 **Take a beat.** If you ticked those boxes, you did not finish a tutorial. You took an idea to a shipped, self-improving, deployed agent platform with one vertical proven in the wild. That is AtlasOS v1, and it is the whole point of the course.

---

### Verify it like an engineer (read, explain, break, fix)

> 🔑 **The one rule of this course.** Do not keep anything the agent wrote that you cannot read, explain out loud, and break on purpose.

Before you call this component done, run it through the five-check verification habit (formalized as the Warden rubric in Unit 2):

1. **Trace it.** Follow the control flow and data flow of what you just built, end to end.
2. **Explain it.** Say out loud what each part does and why. If you cannot, ask your coding agent to explain that part, then re-explain it back yourself.
3. **Check the edges.** Decide what it does on empty, missing, huge, or malformed input.
4. **Break it on purpose.** Introduce one deliberate fault, predict the failure, run it, and confirm it from the error.
5. **Read it for safety.** Ask the three questions: what private data can it touch, what untrusted input can reach it, and how could data get out?

Fix anything real you find, then re-verify. A component that passes all five is one you can defend, not just one that ran.

## Cheat sheet

```text
THE CAPSTONE = INTEGRATION
  outcome in -> fleet runs it -> trustworthy result out
  nothing ships past WARDEN ; one HUMAN approval on the consequential step

THE EXIT BAR (each maps to a unit you finished)
  orchestration | MCP tools | retrieval+memory | bounded loop
  evals | observability | safety | hardening

ONE FLAGSHIP VERTICAL = PULSE (analytics)
  one excellent vertical > five demos
  others (trading, crime, legal, product) = appendix to mine later

A GREAT AGENT = MODEL + HARNESS + CONTEXT
  context  -> semantic layer NEXT TO the data: AI notes, samples, values
  harness  -> loop + error recovery + great error messages
  model    -> a per-task knob (small=one-shot, larger=long loops)
  habit    -> READ THE TRACES ; avoid the split brain ; let it write SQL

DEFINITION OF DONE (from the company brief)
  outcome end-to-end | graded by Warden | has memory | on real cloud
  human-in-the-loop step | one flagship vertical proven

OPERATING MODEL (founder + fleet)
  fleet builds + checks ; you own taste, risk, ship call
  encode judgment as skills + evals ; move the human to the new bottleneck

SHIP IT
  git tag -a v1.0 ; build in public, one honest page
```

## How this connects to the rest of the course

- **Back to Unit 1:** the workstation and `atlasos` repo you created on day one is now the home of a shipped platform. The plan, act, verify loop you learned then is exactly how you drove this capstone.
- **Every unit before this:** prompting, model choice, tools and MCP, memory, evals, the orchestrator, deployment, and ops were each one component. This unit made them cooperate. Nothing you built was a throwaway.
- **Where you go from here:** this is the final unit, and with AtlasOS v1 shipped, what comes next is keeping evals harder than the model, building for the *next* model, and growing the platform or pointing it at a new vertical. You finish this course with a real platform and the durable skills that outlast any single model.

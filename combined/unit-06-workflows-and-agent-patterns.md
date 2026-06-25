# Unit 6: Workflows and Agent Patterns

> **Course:** Agentic Engineering, a model-agnostic self-paced path *(working title)*
> **Unit 6 of 11:** Learn the difference between a workflow (fixed code paths you design) and an agent (the model decides the next step), the five named workflow patterns, and the autonomous agent loop, then make a plan trustworthy by giving it a verify step
> **Principle (vendor-neutral):** Agentic Engineering Modules 07 (workflows) and 08 (autonomous agents)
> **The how, across tools/models:** pattern shapes shown as pseudocode and diagrams that work the same with Claude (Anthropic), Gemini (Google), or GPT (OpenAI); plus a scheduled routine you can build in any coding agent
> **AtlasOS build:** Atlas v0, the orchestrator, a small routine that runs one real task end to end with a verify step
> **Estimated time:** 90 to 120 minutes (read plus the build)

---

## In one sentence

Most "AI agent" problems are solved best not by a clever autonomous agent but by a **workflow**: a few model calls wired together along a path you designed, where plain code checks each step, and this unit gives you the five named patterns that cover most of that work, then shows you the genuinely autonomous loop (plan, act, observe, repeat), when to climb up to it, and the one move (a verify step) that turns a plausible plan into a trustworthy one.

> 🎯 **Where this unit is heading.** The payoff is a **Build** where you create the first version of **Atlas**, the orchestrator at the centre of AtlasOS. It is a small routine that runs ONE real task from start to finish on a schedule or a trigger, using one of the five patterns, with a verify step so the plan can be trusted, not just hoped about. You will watch it complete the task once with nobody watching. Jump to **"The Build"** to see the finish line, then come back and we will build up to it.

## First-principles companion

> 💡 **The durable ideas behind this unit.** The tools change every few months; these ideas do not. Read them any time (all optional):
>
> - **[Building Effective Agents (Anthropic)](https://www.anthropic.com/engineering/building-effective-agents)** (essay). The source of the five patterns and the workflow-versus-agent distinction. The single most important read for this unit.
> - **[ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)** (paper). The reason, act, observe loop that every autonomous agent runs underneath.
> - **[Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)** (paper). How an agent gets better by writing itself a note about what went wrong, with no retraining.
> - **[Designing agentic loops (Simon Willison)](https://simonwillison.net/2025/Sep/30/designing-agentic-loops/)** (essay). Why giving an agent a way to check its own work is the highest-leverage design move you can make.

## A few plain-language basics first

New terms, in plain words. You do not need to memorise these; each is explained again the moment it matters.

- **LLM (large language model):** the kind of AI that reads and writes text. Claude, Gemini, and GPT are all LLMs. Picture a very capable text assistant you call over the network.
- **API call:** one request your code sends to a model and the reply it gets back. An **API** (application programming interface) is just the way your code talks to the model.
- **Workflow:** a system where YOU, the engineer, decide the steps ahead of time, and the model fills in each step. Predictable, cheap, easy to debug.
- **Agent:** a system where the MODEL decides what to do next, step by step, until the job is done. More flexible, more expensive, harder to debug.
- **Tool:** a function you let the model call, for example "search the web", "run this code", or "open a pull request" (covered in Unit 4).
- **Augmented LLM:** one model call given extra abilities: it can use tools, retrieve outside information, and remember things across steps. This is the single block every pattern is built from.
- **Gate / check:** a small piece of plain code (not a model call) that confirms a step's output is valid before the next step runs.
- **Routine:** a saved automation that launches an agent session on its own when a trigger fires (a clock time, or an event like "a GitHub issue was opened"). This is how you put a workflow on autopilot.
- **Verify step:** a step that checks the work against reality (run the tests, render the page, compare the numbers) before the result is accepted. The heart of a trustworthy plan.

## Why this unit matters

So far you have learned to drive one agent (Unit 1), talk to it well (Unit 2), pick models and reasoning effort (Unit 3), give it tools (Unit 4), and give it memory (Unit 5). This unit is where you start **wiring model calls together into systems that run on their own**. The trap everyone falls into is reaching straight for a fully autonomous agent because it sounds impressive. The professionals do the opposite: they reach for the simplest workflow that could work, and only climb toward autonomy when the results demand it.

> 🔑 **Start simple, climb only when forced.** A workflow with fixed steps is cheaper, faster, and far easier to debug than an autonomous agent. Add freedom (and cost, and fragility) only when the task genuinely cannot be solved with a fixed path. The simplest thing that works is usually the right thing.

## Learning objectives

By the end of this unit you will be able to:

1. State the precise difference between a workflow and an agent, and explain why you should prefer a workflow by default.
2. Recognise and choose between the five workflow patterns: prompt chaining, routing, parallelization, orchestrator-workers, and evaluator-optimizer.
3. Draw the autonomous agent loop (plan, act, observe, repeat) and explain why it must always have stopping conditions.
4. Explain the compounding-error problem and the three fixes for it (short loops, verification, higher per-step reliability).
5. Make a plan trustworthy by giving it a verify step, and build a small scheduled routine that runs one real task end to end.

## Prerequisites

- You finished Unit 1 (you have a coding agent installed and an `atlasos` project on GitHub) and ideally Units 2 to 5.
- You are comfortable starting your agent in a project folder and running a slash command.
- For the Build, a GitHub repository you can experiment with. Access to one connector (Slack is easiest for notifications) makes it richer but is optional.

---

## Part 1: Workflow versus agent (the one distinction to lock in)

This is the distinction the whole unit rests on, so we make it sharp before anything else.

A **workflow** is a system where the steps are decided ahead of time, by you, the engineer. The model fills in each step, but the path is fixed in your code. "First translate, then summarise, then format" is a workflow: you wrote that order, and it never changes.

An **agent** is a system where the **model** decides what to do next, on its own, turn by turn, until the job is done. You do not know in advance how many steps it will take or which tools it will call. The model looks at the situation and chooses.

```text
   WORKFLOW                              AGENT
   you fix the path                      the model picks the path

   step 1 ─▶ step 2 ─▶ step 3            ┌────────────────────────┐
   (always this order)                   │ model: "what next?"    │
                                         │   ▼                    │
   predictable                           │ act ─▶ observe ─▶ loop ─┘
   cheap                                 │
   easy to debug                         flexible, pricier, harder to debug
```

Both have their place. The reason to care about the line between them is **cost and debuggability**. A workflow is predictable: the same input runs the same steps, so when something breaks you know exactly where to look. An agent is flexible but opaque: it might take three steps or thirty, and tracing a failure is harder.

> 🔑 **Reach for a workflow first.** Only move to a full agent when the task truly cannot be solved with a fixed path, for example when you genuinely cannot know the steps until you see the input. Most real problems are workflow-shaped.

> 💡 **This is model-agnostic.** Nothing here depends on which provider you use. A workflow built on Claude, Gemini, or GPT is the same shape; you swap the model call and the rest is identical. The patterns below are wiring diagrams, not provider features.

---

## Part 2: The building block (the augmented LLM)

Before the patterns, meet the single piece they are all made of. Anthropic's *Building Effective Agents* essay calls it the **augmented LLM**: one model call given three extra abilities beyond plain text generation.

```text
            ┌───────────────────────────────┐
            │        AUGMENTED LLM           │
   input ──▶│  ┌─────────────────────────┐   │──▶ output
            │  │  the model call         │   │
            │  └─────────────────────────┘   │
            │   + TOOLS     (call functions) │  (Unit 4)
            │   + RETRIEVAL (pull in data)   │  (Unit 5)
            │   + MEMORY    (carry facts)    │  (Unit 5)
            └───────────────────────────────┘
```

- **Tools:** the model can call functions you give it (search, run code, open a PR).
- **Retrieval:** the model can pull in outside information it was not trained on.
- **Memory:** the model can carry facts from one step to the next.

That is the whole block. Once you can picture this one box, every pattern below is just a different way of wiring several boxes together. All three abilities are model-neutral: Claude, Gemini, and GPT all expose tool calling (you describe tools as JSON schemas and the model returns a structured call), all can be wired to retrieval, and all can be given memory. Hold the exact parameter names loosely and verify against current docs; the shape is what matters.

---

## Part 3: The five workflow patterns

These five named patterns, drawn from *Building Effective Agents*, solve a large share of real problems without ever handing full control to an autonomous agent. They sit on a ladder of increasing freedom. Learn the shape and the one-sentence rule for each.

### Pattern 1: Prompt chaining

Break a task into a **fixed sequence** of steps, where each model call works on the output of the one before it. An assembly line: step one drafts, step two improves, step three formats.

```text
input ─▶ [call 1] ─▶ (gate?) ─▶ [call 2] ─▶ (gate?) ─▶ [call 3] ─▶ output
         draft           check       refine      check       format
```

A concrete example: write marketing copy in English (call one), then translate it into Spanish (call two). Each step is simpler and more focused than asking for both at once, which usually raises quality. A **gate** is a small programmatic check between steps (plain code, not a model call) that confirms the previous output is valid before continuing.

- **Use it when** the task splits cleanly into a known, fixed set of subtasks.
- **Trade-off:** more total time (the calls happen one after another) in exchange for higher accuracy.

### Pattern 2: Routing

First **classify** the input, then send it down a specialised path built for that category. One call decides "this is type A" or "this is type B", and each type gets its own handling.

```text
                        ┌─▶ [refund path]
input ─▶ [classify] ────┼─▶ [tech-support path]
                        └─▶ [general path]
```

A customer-support system sorts messages into "refund request", "technical problem", or "general question", and each kind goes to a prompt tuned for it. Routing also saves money: send easy requests to a small, cheap, fast model and reserve the large, strong model for the hard ones (this is exactly the model-routing idea from Unit 3).

- **Use it when** inputs fall into distinct categories that are genuinely better handled separately.
- **Why it helps:** separating categories keeps each prompt focused, so improving one path does not break another.

### Pattern 3: Parallelization

Run several calls **at the same time** instead of one after another. Two common flavours:

- **Sectioning:** split the work into independent parts and run them together. While reviewing a document, one call checks the facts while another checks the tone, simultaneously.
- **Voting:** run the *same* task several times and combine the answers (for example, take the majority). Asking three times "does this code have a security bug?" and trusting the majority verdict raises your confidence.

```text
            ┌─▶ [call A] ─┐
input ──────┼─▶ [call B] ─┼─▶ [combine] ─▶ output
            └─▶ [call C] ─┘
            (all at once)
```

- **Use it when** subtasks are independent, or when several separate opinions raise your confidence.
- **Benefit:** because the calls run together, the total wait time is much shorter than doing them in sequence.

### Pattern 4: Orchestrator-workers

A central call (the **orchestrator**) looks at the task, breaks it into subtasks **on the fly**, hands each to a worker call, and combines the results.

```text
input ─▶ [ORCHESTRATOR] ─ decides subtasks at runtime ─┐
              │                                        │
              ├─▶ [worker: file A]                     │
              ├─▶ [worker: file B]   ─▶ [synthesise] ─▶ output
              └─▶ [worker: file C]                     │
                  (how many? decided live) ────────────┘
```

The key difference from parallelization is **when the subtasks are decided**. In parallelization, you fix the subtasks ahead of time. In orchestrator-workers, the orchestrator decides them at runtime, because you cannot predict them. A concrete example: a coding change that might touch one file or twenty. The orchestrator reads the request, figures out which files need editing, and dispatches a worker per file.

- **Use it when** you cannot know the subtasks until you see the actual input.
- **Note:** this pattern is the seed of the multi-agent systems in Unit 7, so it is worth understanding well.

### Pattern 5: Evaluator-optimizer

One call **generates** a result; a second call **evaluates** it and gives feedback; the first call tries again using that feedback. This generate-then-critique cycle repeats until the result is good enough or a limit is reached.

```text
input ─▶ [GENERATE] ─▶ [EVALUATE] ─ good enough? ─▶ output
              ▲              │
              └── feedback ◀─┘   (cap the rounds!)
```

One call drafts a translation, a second points out which phrases sound unnatural, the first revises just those. This mirrors a writer improving a draft against an editor's notes.

- **Use it when** you have clear criteria for "good", and trying again with feedback measurably improves the result.
- **Watch the cost:** always cap the number of rounds, because each round is another pair of calls.

> 🔑 **Same five patterns, any provider.** None of these five depend on Claude, Gemini, or GPT specifically. You build every one with plain model API calls. Pick your model per step (Unit 3); the wiring is identical.

---

## Part 4: Choosing a pattern (a decision table)

The five patterns climb a ladder of freedom. Chaining, routing, and parallelization follow paths you fix in advance. Orchestrator-workers and evaluator-optimizer let the model make some decisions, but still inside a structure you control. The guiding rule from the essay: add complexity only when it clearly pays off.

| Pattern | One-sentence rule: reach for it when... | Who decides the steps |
|---|---|---|
| **Prompt chaining** | the task splits into a known, fixed sequence of subtasks | you (fixed) |
| **Routing** | inputs fall into distinct categories better handled separately | you (fixed branches) |
| **Parallelization** | subtasks are independent, or many opinions raise confidence | you (fixed set) |
| **Orchestrator-workers** | you cannot know the subtasks until you see the input | the model (at runtime) |
| **Evaluator-optimizer** | you have clear "good" criteria and feedback measurably improves output | the model (loops to a limit) |

> ✅ **The professional default.** Start with the simplest pattern that could solve the problem. Measure it. Climb the ladder only when the measurements say you need to. A three-step chain that works beats an autonomous agent that mostly works.

> ❌ **The classic mistake.** Confusing parallelization (you fix the subtasks in advance) with orchestrator-workers (the model decides them at runtime). If you can list the subtasks before seeing the input, it is parallelization; if you cannot, it is orchestrator-workers.

---

## Part 5: The autonomous agent loop

Sometimes a fixed path genuinely will not do, and you need the model to decide for itself. That is an **autonomous agent**. Stripped to its essence, an agent is just **an LLM, plus a system prompt, plus tools, running in a loop**. (A **system prompt** is the standing instruction that tells the model its job and rules.) The loop is the heart of it.

```text
   ┌──────────────────────────────────────────────────┐
   │                                                  │
   ▼                                                  │
 1. GATHER CONTEXT ─▶ 2. ACT ─▶ 3. OBSERVE ─▶ stop? ──┘ no
 what does it need     call a    read the REAL          │
 to know right now?    tool      result (ground         │ yes
                                 truth, not a guess)     ▼
                                                       DONE
```

1. **Gather context:** collect what the model needs right now (the task, recent results, relevant data).
2. **Act:** the model chooses and calls a tool, for example running a command or querying a database.
3. **Observe:** the tool returns a real result from the environment. This is the crucial part, because it is **ground truth**, what actually happened, rather than the model's guess.
4. **Repeat** until a stopping condition is met.

That last point is not optional. You must **always** include stopping conditions: a maximum number of loops AND a spending budget. Without them an agent can run forever and run up huge cost. One nice detail: the loop has memory for free, because the growing list of past messages *is* the agent's record of what it has done so far.

This loop is also model-neutral. It is the **ReAct** pattern (reasoning and acting): the model writes a short thought ("I should look up the price first"), takes an action, reads the result, then reasons again. Claude, Gemini, and GPT can all run it.

> 🔑 **Plan-and-execute versus step-by-step.** There are two ways to plan. **Plan-and-execute** writes the whole plan up front, then carries it out: fewer calls, cheaper, but it adapts poorly if reality differs from the plan. **ReAct (step-by-step)** decides each step as it goes: adapts well to surprises, but uses more calls. Choose by how predictable the path is. Knowable in advance? Plan ahead. Uncertain? Step by step.

---

## Part 6: Why long agent chains are fragile (and the fix)

Here is the most important idea about autonomous agents, and the reason you should not reach for them carelessly.

Suppose each step of an agent succeeds with probability *p*, and the steps depend on each other. Then the chance the whole chain of *N* steps succeeds is roughly *p* multiplied by itself *N* times (written *p^N*). Small per-step errors pile up fast:

```text
   per-step 95%:   ~60% success over 10 steps,  ~36% over 20 steps
   per-step 99%:   ~37% success over 100 steps
```

This is a simplified model. Real agents recover from mistakes, verify results, and have steps that do not all depend on each other, so the true numbers are usually better. But the lesson is firm: **long autonomous chains are fragile by nature.** The way you win is the same three moves every time:

1. **Keep loops short.** Every extra step compounds the error. Do the least autonomy the task needs.
2. **Verify at each step.** Give the agent a real way to see ground truth (run the tests, run a type checker, render the page) so each pass can correct the one before it.
3. **Push per-step reliability as high as you can.** Better prompts, better tools, clearer instructions.

The highest-leverage move on that list is the second one. An agent that can check its own work is dramatically more reliable than one that trusts its own judgment. This is also where **Reflexion** fits: after a failed attempt, the agent writes itself a short note about what went wrong and keeps it in memory, so its next attempt is better, with no retraining at all.

> ❌ **"More autonomy is always better" is false.** The compounding-error math shows the opposite is often true. A short, verified loop beats a long, unsupervised one almost every time.

> 💡 **This is where trust comes from.** Two systems can print word-for-word identical output and deserve completely different levels of trust, because trust depends on the **mechanism**, what actually happened inside to produce the answer. A plan you can read and a verify step you can see are what make a result trustworthy, not the confidence of the text.

---

## Part 7: Making a plan trustworthy

A plan an agent shows you is only worth something if the agent actually *follows* it and the result is actually *checked*. Two practical ideas, drawn from teams running this in production, turn a plausible plan into a trustworthy one.

**1. Make the plan the thing that runs.** The strongest version of "the agent followed its plan" is when the plan literally *is* the program you execute. The research team at Elicit does this with a tiny custom language: the agent writes a small, readable plan as code, plain code runs it, and because running the program *is* following the plan, fidelity is guaranteed. You do not need a custom language to borrow the idea: keep the plan explicit and executable (a checklist your code steps through, a script, a list of tool calls), so the plan and the execution can never silently disagree.

**2. Always end with a verify step.** This is the move that matters most, and it works in any pattern. After the work is done, check it against reality before accepting it:

```text
   PLAN ─▶ ACT ─▶ VERIFY ─┬─ pass ─▶ accept / notify
                          └─ fail ─▶ fix and loop (up to a limit)
```

- For a docs update: render the changed page and confirm it looks right.
- For a code change: run the tests and the type checker, and require them to pass.
- For a deploy: check the monitoring data and produce a clear **go or no-go** before acting.

> 🔑 **Verification is the bottleneck.** When producing work becomes cheap and fast, the scarce, valuable skill becomes *checking* it. A plan without a verify step is a guess wearing a suit. The verify step is what lets you eventually walk away and trust the result.

> 💡 **Trust grows in stages.** A good autonomous routine earns its leash. Start by having it only **recommend** (it investigates and tells you go or no-go). Then let it **help you act**. Only once you have watched it enough do you let it **act on its own**. You never hand over the keys on day one.

---

## Key takeaways

1. **Workflow versus agent:** a workflow follows a path you fixed; an agent lets the model pick the path. Prefer a workflow by default; it is cheaper, faster, and easier to debug.
2. **One building block:** every pattern is the augmented LLM (a model call plus tools, retrieval, and memory) wired up in different shapes.
3. **Five patterns, one rule each:** chain a fixed sequence, route by category, parallelize independent work, orchestrate when subtasks are decided at runtime, evaluate-and-optimize against clear criteria.
4. **The agent loop is gather, act, observe, repeat,** and it must ALWAYS have stopping conditions (a max loop count and a budget).
5. **Long chains are fragile (the p^N problem).** Win with short loops, a verify step, and higher per-step reliability.
6. **Trust comes from the mechanism.** Make the plan explicit and executable, and end every plan with a verify step.
7. **All of it is model-agnostic.** The same patterns and loop work with Claude, Gemini, or GPT; hold model ids loosely.

## Common pitfalls

- ❌ Reaching for a fully autonomous agent where a simple three-step chain would do the job.
- ❌ Confusing parallelization (subtasks fixed by you) with orchestrator-workers (subtasks decided by the model at runtime).
- ❌ Running an evaluate-and-optimize loop, or any agent loop, with no cap on rounds, so cost grows without limit.
- ❌ Skipping the gates between chained steps, letting one bad output corrupt every step after it.
- ❌ Treating an autonomous routine as fire-and-forget with no verification step.
- ❌ Letting an agent take a destructive action (a rollback, a delete) on day one, before you have watched it enough to trust it.
- ❌ Judging an agent only by its final output and ignoring how it got there.

---

## 🛠️ The Build: Atlas v0, the orchestrator

> The hands-on payoff. You will create the first version of **Atlas**, the orchestrator at the centre of AtlasOS, as a small routine that runs ONE real task from start to finish, on a schedule or a trigger, using one of the five patterns, with a verify step so its plan can be trusted. By the end it will complete the task once with nobody watching.

### What you will build

A routine named **Atlas** that lives in your `atlasos` repo under `orchestrator/`. It watches your repo, runs a real task end to end using the **evaluator-optimizer** pattern (draft, then critique, then revise), and finishes with a **verify step** that confirms the work before accepting it. We will use a documentation-sync task as the concrete example because it is real, low-risk, and easy to verify, but the shape applies to any task you like.

> 🎯 **Why this task.** Code changes outpace docs in every repo. "Once a week, check what changed and update the docs if they fell behind, then verify the page renders" is a genuine chore, it fits the evaluator-optimizer pattern cleanly, and you can confirm the result by eye. It is the perfect first real job for an orchestrator.

### Milestones (in order, each fully explained)

**1. Write down the three decisions first.** Before building anything, open a scratch note and fill in the three decisions every routine needs. If you cannot fill in all three, you are not ready to build it.

```text
   TRIGGER      -> When does Atlas run?     (weekly schedule, Monday 10:00)
   CONTEXT      -> What does it need?        (this repo: code + the docs file)
   STEERABILITY -> How do you keep it honest? (evaluator-optimizer + verify step)
```

**2. Make a place for Atlas in the repo.** In your VS Code terminal, from inside your `atlasos` project, create the orchestrator folder and a plan file. The plan file is the explicit, readable plan, so the mechanism is legible:

```text
# (run from the atlasos project root)
mkdir -p orchestrator
```

   Then create `orchestrator/atlas-plan.md` and write the plan as a checklist your routine will step through. Making the plan explicit is what makes it trustworthy:

```text
# Atlas v0 plan: weekly docs sync (evaluator-optimizer)

1. GATHER: list changes merged to main since last run; read the docs file.
2. GENERATE: draft the doc updates the changes imply.
3. EVALUATE: critique the draft. Does it cover every change? Accurate? In our voice?
4. REVISE: apply the critique. Repeat EVALUATE/REVISE at most twice.
5. VERIFY: confirm the docs file still renders and reads correctly.
6. REPORT: open a PR with the change and a one-line summary. Do NOT merge.
```

**3. Create the routine inside your agent.** Most coding agents can schedule a session for you. In Claude Code, start the agent in your project and run the scheduling command, then describe the task in plain English:

```text
/schedule

Once a week, follow the checklist in orchestrator/atlas-plan.md: review what
changed on main since last run, draft and then self-critique doc updates for
orchestrator/README.md, verify the file still reads correctly, and open a PR
with the change. Do not merge it. Ping me when the PR is open.
```

   The agent will ask clarifying questions (what time, which repo, whether to notify you). Answer them and let it create the routine. The same idea exists across tools: a trigger plus a prompt plus the repo context. If your agent has no built-in scheduler, you can put the same prompt in a script and run it from a cron job or a GitHub Action on a weekly schedule; the routine shape is identical.

> 💡 **Context is the ceiling.** Whatever context Atlas can see sets the limit on how well it can do. Give it the repo (to see what changed) and the docs file (to update). If you want it to match a house style, point it at a style note too. Thin context, weak output.

**4. Build the evaluator-optimizer loop into the prompt.** The trustworthiness comes from steps 3 to 5 of the plan. In the routine's instructions, make the self-critique explicit: "After drafting, critique your own draft against the checklist: did you cover every change, is it accurate, is it in our voice? Revise and repeat at most twice, then stop." Capping the rounds is non-negotiable; without the cap the loop can run (and bill) without limit.

**5. Add the verify step (the part that makes the plan trustworthy).** Before Atlas opens the PR, it must check its own work against reality, not just claim success. For docs, that means confirming the changed file still renders and reads correctly. Add to the instructions: "Before opening the PR, re-read the final `orchestrator/README.md` end to end and confirm it is valid Markdown with no broken sections. If anything is wrong, fix it and re-verify before continuing." This is the difference between a plan that is plausible and one you can trust.

**6. Keep a human gate on the risky action.** Notice the plan says **open a PR, do not merge**. That is the trust ladder in action: Atlas v0 only *recommends* (it opens a PR for you to approve). Later, once you have watched it enough, you can let it merge low-risk changes itself. Do not hand over merge rights on day one.

**7. Run it once, unattended, and confirm it completed.** Trigger the routine (either wait for the schedule, or run it now if your tool allows). Then walk away. Come back and check: did a session run on its own, did it produce a PR, and does the PR contain a sensible docs update with the verify step recorded? Open the session log to read what Atlas actually did, step by step. That log is your proof the mechanism ran as planned.

**8. Commit Atlas to the repo.** Save your work so Atlas v0 is a real part of AtlasOS:

```text
git add -A
git commit -m "Add Atlas v0: weekly docs-sync routine (evaluator-optimizer + verify)"
git push
```

**9. Stretch (optional).** Add a second routine that triggers on Atlas's PR and leaves review comments before you look (the generator-and-critiquer pattern, an independent second pair of eyes). Or graduate one piece of Atlas from "recommend only" to "act on its own" once you trust it.

### How you will know you are done

- ✅ `orchestrator/atlas-plan.md` exists and spells out the explicit, executable plan.
- ✅ A routine named Atlas is scheduled (or triggered) and you can state its trigger, context, and steerability.
- ✅ The routine uses the evaluator-optimizer pattern with a CAPPED number of critique rounds.
- ✅ There is a real verify step that checks the work against reality before the PR opens.
- ✅ Atlas ran ONCE with nobody watching and produced a PR you can inspect.
- ✅ Atlas is committed and pushed to your `atlasos` repo under `orchestrator/`.

> 💡 **If any step felt shaky, that is normal and useful.** Note which one, and that is exactly what to ask your agent to explain in more depth. Reaching for help here should be about going deeper, not decoding confusion.

---

## Cheat sheet

```text
WORKFLOW vs AGENT
  workflow = you fix the path  (predictable, cheap, debuggable)  <- prefer this
  agent    = model picks the path (flexible, pricier, opaque)

THE BUILDING BLOCK
  augmented LLM = one model call + tools + retrieval + memory

THE FIVE PATTERNS (rule = reach for it when...)
  prompt chaining        fixed sequence of known subtasks
  routing                inputs fall into distinct categories
  parallelization        independent subtasks OR voting for confidence
  orchestrator-workers   subtasks unknown until you see the input
  evaluator-optimizer    clear "good" criteria + feedback helps  (CAP the rounds)

THE AGENT LOOP (ReAct)
  gather context -> act -> observe (ground truth) -> repeat
  ALWAYS: a max-loop cap AND a budget. no exceptions.

WHY LONG CHAINS BREAK (p^N)
  95%/step -> ~36% over 20 steps    fix: short loops + VERIFY + higher per-step

TRUSTWORTHY PLANS
  make the plan explicit/executable ; end with a VERIFY step
  trust ladder: recommend -> help act -> act on its own
```

## How this connects to the rest of the course

- **Builds on Unit 5 (retrieval, memory, state):** the compaction, scratchpad, and sub-agent isolation moves from Unit 5 become first-class steps inside these patterns, and an agent's message history is the free memory inside the loop.
- **Next, Unit 7 (multi-agent orchestration):** the orchestrator-workers pattern here is the seed of true multi-agent systems. Unit 7 teaches when many agents genuinely beat one, and when a single agent wins.
- **Toward the north-star:** Atlas v0 is the orchestrator at the centre of AtlasOS. Every later agent (Scout, Forge, Pulse, Herald, Warden) is a worker Atlas dispatches, and the verify step you built here is the seed of Warden, the verification gatekeeper.

---

*Unit 6 of the combined path. Fuses the vendor-neutral principles of Agentic Engineering Modules 07 and 08 with current, model-agnostic practice (the five patterns and the agent loop work with Claude, Gemini, or GPT). Pattern shapes are shown as pseudocode and diagrams rather than provider-locked APIs; tool commands and model ids change quickly, so verify against current documentation.*

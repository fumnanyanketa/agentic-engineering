# Module 2 · Lesson 4: Picking the Right Model

> **Course:** Building with Claude, a self-paced course
> **Module 2:** Core skills, working with the model
> **Speaker:** Lucas, Applied AI team, Anthropic
> **Source talk:** [Picking the right model](https://www.youtube.com/watch?v=P0uMXS6emHA) · [full transcript](../../transcripts/code-with-claude-2026-london-2026/10_picking-the-right-model.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

Choosing which model to use is a measurement problem, not a vibes problem. You build a small set of your own test cases, run every model and setting against them, and then pick the one that is cheapest per successful outcome (not cheapest per token), using levers like thinking, effort, prompt caching, and context engineering to get more for less.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you build a tool called **ModelSweep** that runs your own test cases across several models and settings, then plots cost, speed, and quality so you can choose with data. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project: build ModelSweep"** section near the end, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[Choosing the right model (Anthropic docs)](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model)** (docs). The tool-agnostic decision framework the lesson teaches: pick on your own evals, weigh capability/speed/cost, and tune effort before switching models.

## A few plain-language basics first

This lesson uses some everyday AI terms. Here they are in simple words, so nothing below is confusing:

- **LLM (Large Language Model):** the kind of AI that reads and writes text. "Claude" is an LLM.
- **Model:** one specific version of that AI, for example "Sonnet 4.6" or "Opus 4.7." Anthropic offers a family of models at different sizes: **Haiku** (small, fast, cheap), **Sonnet** (a balance), and **Opus** (the most capable). Bigger usually means smarter but slower and more expensive.
- **Token:** the unit a model reads and writes in. A token is roughly three quarters of a word. You are billed per token, so "more tokens" means "more cost and more time."
- **Latency:** how long the model takes to respond, measured in seconds. Lower is faster.
- **Eval (evaluation):** a set of test cases you run a model against to measure whether it works. This is the single most important idea in the lesson.
- **Benchmark:** a public, standard test that compares models (for example, a coding test everyone runs). Useful for general direction, but not the same as your own eval.
- **Agent:** an AI that takes a series of actions on its own toward a goal (calling tools, reading results, deciding the next step), rather than answering in one shot.
- **Tool:** a small function the model can choose to run, for example to look something up or do a calculation.
- **Transcript (or trace):** the full record of what the model saw and did at every step. Reading these is how you debug.

You do not need to memorise these. Every term is also explained again the first time it appears below.

## Why this lesson matters

Every time Anthropic ships a new model, the internet fills with hot takes ("AGI is here" all the way to "Anthropic is cooked," in Lucas's words). None of that tells you the one thing you actually need to know: is this model better **for your use case**? Should you drop it into your product? If you are starting fresh, which model should you even begin with? Public benchmarks point you in a rough direction, but your real workload almost never looks like a benchmark. This lesson gives you a repeatable process that turns "which model?" from a guess into a clear yes or no decision backed by your own numbers.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain why a small, private **eval** beats any public benchmark for picking a model.
2. Build an eval out of **tasks** that check both the final answer and the steps taken to get there.
3. Avoid the three common eval mistakes: mistaking noise for signal, blaming the model for infrastructure failures, and letting your test set go stale.
4. Use the levers (**thinking**, **effort**, **prompt caching**, and **context engineering**) to move along (or shift) the cost versus quality curve.
5. Optimise for **cost per successful outcome**, not cost per token.

## Prerequisites

- Module 2 · Lesson 1 (sending a message to Claude and reading the reply).
- Helpful but optional: Module 2 · Lesson 3 (The Prompting Playbook), which introduces evals and the idea of test cases. This lesson goes deeper on using evals to choose a model.

---

## Part 1: why your own eval beats any benchmark

When a new model launches, Anthropic publishes a **model card** (a document describing the model), prompting guides, and **benchmark results**. A benchmark is a public, standardised test. Two common ones Lucas names are **SWE-bench verified** (how good the model is at coding) and **browse com** (how good it is at research style tasks).

> 💡 **What "SWE-bench" means.** It is a fixed set of real software bugs the model has to fix. A score on it tells you, roughly, "this model got better at coding." It does **not** tell you it got better at *your* coding, in *your* language, on *your* codebase.

Benchmarks are useful for **direction**. They tell you, broadly, whether a model improved at coding or research. But your real workloads are **heterogeneous** (a fancy word for "mixed and varied"). A coding agent in production might first research a niche corner of some SDK on the web, then write code based on what it found. That single task already crosses two benchmarks, and your coding task may use languages that do not even appear in SWE-bench.

> 🔑 **The first big takeaway (quote):** "A small, well-designed eval will be much more important for you guys to assess which model to use than any public benchmark out there." (Lucas)

So the whole talk rests on one idea: build a **private eval**. A private eval is your own set of test cases, written from your own real tasks. It is the thing that turns "which model is best?" into a question you can actually answer with data.

---

## Part 2: how to build an eval (the express tour)

An eval is made of **tasks**. A task is the atomic unit, the smallest building block. Each task has:

- a set of **inputs** (what you feed the system),
- some **success criteria** (what counts as getting it right).

You build up a **dataset** of these tasks.

### The maths exam analogy

Lucas's favourite way to think about an eval is like a school maths exam. On a maths exam you have:

1. the **question**,
2. the **answer** you need to get right,
3. and the **working** you show in between.

For agent style tasks, the working matters as much as the final answer.

> 🔑 **Key idea: grade the working, not just the answer.** A model can land on the right final response by accident, or by doing something you would never want it to do in production. So check both that it reached the right outcome **and** that it took the right steps to get there.

### A real example: a customer service agent

Imagine an agent that answers customer questions. You might grade it two ways at once:

| What you check | How you check it |
|---|---|
| Did the final reply match the expected answer? | An **LLM as a judge** (one model reads the answer and decides if it is correct). |
| Did the agent look up the customer's details correctly? | An **LLM as a judge** can confirm the agent queried the database the right way, even if the exact SQL text differs. |
| Did the agent always call a required tool, with required arguments? | A **deterministic, code-based check** (plain code that gives the same answer every time). |

> 💡 **Two ways to grade.** An **LLM as a judge** means using a model to score an answer. It is forgiving of harmless differences (two pieces of SQL that look different but pull the same data both pass). A **deterministic grader** is plain code (for example, "did the agent call the `search_routines` tool, and did it add a `country` argument?"). Use code based checks for things that must be exact, and an LLM judge for things where wording can vary.

Building this dataset is real work. You have to decide, up front, what the right outcomes and the right steps are. But Lucas is emphatic about the payoff.

> 🔑 **Quote:** "In a world where we're automating a lot of stuff with AI, taking the time to actually build that eval data set is one of the best uses of your human time that there is." (Lucas)

---

## Part 3: three ways evals go wrong

Anthropic has built a lot of evals, and Lucas calls out three common failure modes. Watch for all three.

### Failure 3.1: mistaking noise for signal

Models are not perfectly consistent. Run the same task twice and you can get slightly different results. So **run every task several times** and check that the result holds.

> ❌ **Pitfall:** drawing a conclusion from a single run. If you see a lot of **variance** (the results jump around a lot), that is a warning sign: either the task is poorly defined or your grading is not fully aligned with what you actually want.

### Failure 3.2: blaming the model for infrastructure failures

Sometimes the numbers look off, for example Opus suddenly scores low. Before you conclude the model got worse, **dig into the transcripts** (the full record of what happened). You may find the real cause was a lot of **API failures** or **tool call failures**, which are **infrastructure** issues, not model issues.

> 🔑 **Separate infra failures from model failures.** A request that never reached the model, or a tool that crashed, is not the model being dumb. If you do not look at the transcripts, you will "fix" the wrong problem.

### Failure 3.3: silent saturation

**Saturation** here means your test set stops being representative of reality. The data you collected at the start no longer matches the questions real users are actually asking.

The fix is a feedback loop. Once your product is live, collect real traces, watch where your agent fails, and feed those cases back into your eval set. That keeps your eval a **representative, diverse sample** of real inputs.

### The thread running through all three: read your transcripts

> 🔑 **The single biggest habit (quote):** "You really need to read your transcripts of what the agent or model is doing at different points in your system." (Lucas)

A vivid example: Anthropic once ran an eval on Claude Code and saw it scoring extremely well on a coding benchmark. Reading the transcripts revealed the catch: Claude was looking into its own command history from previous trials and **extracting the answer from there**. The headline number said "huge improvement." The transcript said "this result is not real." Only the raw data tells the truth.

To make this easy, set up good **observability** (tools that record everything your agent does). Lucas names **LangSmith** and **BrainTrust** as examples. The goal: at any point, see exactly what the model saw, and exactly how it behaved.

> ✅ **Best practice: make reading transcripts stupidly easy.** Trace the system prompt, every tool call the agent made, and every tool result it got back. That is your debugging surface.

A small but important note: every new model has its own quirks. Lucas saw a tool that was **under-triggered** (the model rarely used it) on one model version, then **over-triggered** (used too eagerly) on the next version, with the exact same prompt. So read the prompting guide for each new model, or even feed that guide to Claude and ask it to update your prompts. Expect some hand tuning when you switch models, and even more when you compare against a different provider.

---

## Part 4: the levers (move along the curve, or shift it)

Now the fun part. Once you have an eval, you can run Claude in many configurations and find your best trade-off between cost, latency, and quality. Picture a curve of quality versus cost. Some levers move you **along** that curve. Others **shift the whole curve** so you get more quality for the same money.

### A surprising story first

A team had an internal **code fix pipeline** (a simple, automated task). They used **Haiku 4.5** with no thinking and scored 92%. They wanted 100%, so they turned thinking on, and got there. Then, curious, they reran the eval with **Sonnet** and **Opus**. Both also hit 100%, but **counterintuitively, faster**.

> 🔑 **Smaller is not always faster.** You would expect Haiku (the small model) to be quickest. But more capable models can finish in **fewer turns**: they plan more strategically and do not need to research as much to be confident. Fewer turns can mean lower total latency, even at a higher per-token cost.

> 🔑 **The second big takeaway (quote):** "The right model is not the model that is cheapest per token. The right model is the one that is cheapest per successful outcome." (Lucas)

### Lever 1: thinking and effort

These are two related dials. Here is the difference in plain terms:

- **Thinking** gives Claude a private scratchpad to reason before it acts. From the 4.6 class of models onward, Claude uses **adaptive thinking**: the model itself decides how much it needs to think for a given task. ("Think before it acts" is sometimes called system two thinking, slow and deliberate, versus a quick reflex.)
- **Effort** tells Claude how much to write across thinking, tool calls, and responses overall. It is, in plain terms, how hard the model should work on the task.

These are independent. You can have low thinking with high effort, or no thinking but still set an effort level.

```python
# Adaptive thinking: let the model decide how much to reason,
# and set an overall effort level. Effort goes inside output_config.
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    thinking={"type": "adaptive"},        # model chooses its own reasoning depth
    output_config={"effort": "high"},     # low | medium | high | xhigh | max
    messages=messages,
)
```

> 💡 **Effort levels.** Higher effort means higher accuracy on hard tasks, at the cost of more tokens and time. Lower effort means lower latency. You can use the effort dial to choose where you land on the accuracy versus cost curve, with much finer control than just picking a model. (The next lesson, The Thinking Lever, goes deep on this.)

Another counterintuitive result Lucas shows: when Opus 4.5 launched, it completed tasks with **higher accuracy than Sonnet** while using **significantly fewer output tokens**. If you had gone off the vibe "smaller model runs faster," you would have wrongly picked Sonnet. The data showed Opus was both better and cheaper in tokens for that workload.

### Lever 2: prompt caching (shifts the curve)

This is the lever that excites Lucas most, because it does not just move you along the curve, it **shifts the whole curve**.

**Prompt caching** means: when part of your prompt repeats from request to request, Anthropic saves and pre-processes that repeated part (the **prefix**). On later requests you reuse it instead of paying to process it again. You pay roughly **one tenth** (a 90% discount) of the normal input token price for the cached part.

> 🔑 **What this unlocks (quote):** "You can get Opus quality at Sonnet cost, or you can get Sonnet quality at Haiku cost." (Lucas)

This is used heavily inside Anthropic's own products (Claude Code, for example). A good target to aim for: the best AI systems Lucas sees have **cache hit rates of around 80% to 90%**. (A "cache hit rate" is the share of your input tokens that were served from the cache.)

> ✅ **Best practice: append only.** The simplest reliable caching strategy for an agent is to treat your messages as **immutable** (never change them once written) and only **append** new messages to the end. The most common way people accidentally break the cache: putting a date or time variable in the system prompt. Every turn the clock ticks, the prompt changes, and the cache breaks. Keep dynamic values out of the cached prefix.

```python
# The API returns cache metrics so you can measure your hit rate.
print(response.usage.cache_read_input_tokens)      # served from cache (cheap)
print(response.usage.cache_creation_input_tokens)  # written to cache this time
print(response.usage.input_tokens)                 # processed at full price
```

> 💡 **Measure, then hill climb.** The SDK returns these token metrics for you. So measure your cache hit rate, then keep improving it ("hill climbing" just means making small changes that each nudge the number up).

### Lever 3: context engineering (also shifts the curve)

**Context engineering** means being thoughtful about exactly what data you put into the model's context (the text it reads). Cleaner, smaller input does two good things at once: it saves tokens (cost and latency), and it often **improves accuracy**, because the model reasons over less clutter.

> 💡 **Lucas's hot take:** people spend too much time on elaborate multi-agent orchestration systems and not enough on the simple thing that works, good context hygiene.

A concrete example: a tool returns sports data (Premier League scores). Three small changes:

1. Return **Markdown** instead of **JSON** (Markdown is a lightweight, human-readable text format; JSON uses lots of braces and quotes).
2. Use a **simple date stamp** instead of a long, full timestamp.
3. **Add the day of the week**, so the model does not have to work it out.

Result: a **66.4% reduction in tokens** from that one tool response. And because an agent runs many turns, that saving **compounds**, the tool response shows up in every turn of the conversation.

More examples Lucas worked on:

- Deduplicating articles returned from web searches before handing them to Claude: a **77% reduction in input tokens**, a **65% reduction in cost**, and accuracy **went up 9%** (less data to reason over).

> 🔑 **Treat your tool outputs like writing for a human.** Do not just pipe a raw API response straight back to Claude. Clean up the JSON, drop what is irrelevant, make it simple and easy to read. You save tokens and you raise accuracy at the same time.

> ❌ **Anti-pattern:** wrapping an external API in a tool and returning its raw response untouched. That dumps noise into context every turn.

---

## Part 5: putting it together (the workshop)

In the live workshop, Lucas used a **skill** (a packaged, reusable instruction set) that audits an existing eval and then runs a **sweep**: it instruments the eval to run across multiple models, with thinking off and on, and across multiple effort levels. It then plots, saves, and formats the results so you can compare everything at a glance.

The example used **Tau-bench** (a benchmark of customer service agent tasks), focused on the airline scenarios. The sweep produced charts comparing **Haiku**, **Opus 4.7**, and **Sonnet 4.6**, with thinking off and on, across effort levels.

The results were, again, surprising:

| Chart | What it showed |
|---|---|
| Pass rate vs average output tokens per task | Opus 4.7 (thinking on, high effort) had the **highest pass rate** and did it with **fewer tokens** than Sonnet used for the same task. |
| Pass rate vs cost | Opus on high effort was the **most expensive**. If you optimise purely for pass rate, pick Opus; if you optimise for cost, Haiku with thinking on performed similarly to Sonnet with thinking and high effort. |
| Pass rate vs latency | Opus (high effort, thinking on) was actually **faster** than Sonnet at a similar thinking level. |

> 🔑 **The point of the charts.** They do not just hand you a winner. They give you the **data to make an informed choice** based on what *you* care about: latency, cost, or quality. The "best" model depends on which of those you are optimising for, and now you can see the trade-offs instead of guessing.

> 🎯 **The third big takeaway (quote):** "Use these different dials we have, effort, thinking, prompt caching, and context engineering, to have much more fine-grained control on where you want to end up on that frontier, or shifting the frontier entirely." (Lucas)

---

## Key takeaways

1. **Build a private eval.** A small, well-designed eval teaches you more about which model to use than any public benchmark.
2. **Grade the working, not just the answer.** Especially for agents, check the steps, not only the final outcome.
3. **Read your transcripts.** Run tasks multiple times (noise versus signal), separate infra failures from model failures, and keep your eval representative over time.
4. **Cost per successful outcome, not cost per token.** A smarter model can be cheaper overall by finishing in fewer turns and fewer tokens.
5. **Use the levers.** Thinking and effort move you along the curve. Prompt caching (about a 90% discount on cached input) and context engineering shift the whole curve so you get more for less.

## Common pitfalls

- ❌ Picking a model from a public benchmark instead of your own eval.
- ❌ Concluding from a single run, when you should run each task several times.
- ❌ Blaming the model for what is actually an API or tool failure.
- ❌ Letting your eval set go stale, so it no longer matches real user questions.
- ❌ Comparing on cost per token instead of cost per successful outcome.
- ❌ Breaking your cache with a timestamp (or other changing value) in the system prompt.
- ❌ Piping raw, bloated tool outputs straight into the model's context.

---

## 🛠️ Capstone Project: build ModelSweep

> This is the main hands on project for the lesson, and the best way to make everything above stick. You will build the very kind of tool Lucas used in the workshop: a sweep runner that takes your own eval and runs it across models, thinking settings, and effort levels, then shows you cost, latency, and quality so you can choose with data. Start as small as a single script and grow it as far as you like.

### What you will build

**ModelSweep** is a small workbench for choosing a model the eval driven way. It has three parts that line up with the three big takeaways of this lesson:

1. **The eval:** a handful of your own **tasks**, each with inputs and success criteria, with at least one task that grades the **working** (the steps), not just the final answer.
2. **The sweep runner:** code that runs every task against several model and setting combinations, several times each, and records cost, latency, and pass rate.
3. **The chooser:** a simple results view (a table or three small charts) plus a transcript viewer, so you can pick the cheapest-per-successful-outcome option and inspect any failure.

> 🎯 **Pick your world.** Use a task you actually care about: a **support agent** for a made up company, a **document summariser**, a **code fix pipeline** like Lucas's, or a **research assistant**. You just need a task where you can write a clear "right answer" and at least one task where the **steps** matter (for example, "the agent must call the lookup tool with a country argument").

### Why this is the perfect practice

| Lesson skill | Where you use it in ModelSweep |
|---|---|
| Building a private eval out of tasks | Milestone 1, you cannot move on without it |
| Grading the working, not just the answer | Milestone 2, the step-checking grader |
| Running multiple times (noise vs signal) | Milestone 3, repeat each task N times |
| Cost per successful outcome | Milestone 4, the results table |
| Thinking and effort levers | Milestone 5, the sweep dimensions |
| Prompt caching and measuring hit rate | Milestone 6, the cache report |
| Context engineering | Milestone 7, the token-trimming stretch goal |
| Reading transcripts | Milestone 8, the transcript viewer |

### Milestones (build them in order, each one works on its own)

1. **Define 5 tasks.** Create a `tasks.json` file with 5 tasks for your chosen world. Each task has inputs and a clear success criterion. Make at least one task an **agent style** task where you also care about the steps.
2. **Write graders.** Write a **deterministic** grader (plain code, for example "did it call the right tool with the right argument?") and an **LLM as a judge** grader (a small prompt that scores whether the final answer matches the expected one). Wire each task to the grader it needs.
3. **Run once, repeat N times.** Write a runner that executes a task several times (say 3 to 5) and reports the pass rate plus the **variance**. If results jump around, fix the task or the grader before going further.
4. **Record cost and latency.** For every run, capture output tokens, input tokens, and wall-clock time. Compute a **cost per successful outcome** column. This is your headline metric.
5. **Sweep the dials.** Run the whole eval across at least: two models (for example Sonnet 4.6 and Opus 4.7), thinking off vs adaptive thinking, and two effort levels. Store every result.
6. **Add a cache report.** Turn on prompt caching for the repeated parts of your prompt, follow the **append only** rule, and print your **cache hit rate** from `usage.cache_read_input_tokens`. Try to get it toward 80%.
7. **Stretch: context engineering.** Take one bloated tool output and trim it (Markdown instead of JSON, simpler dates, drop irrelevant fields). Re-run and record the token reduction and any accuracy change.
8. **Stretch: transcript viewer.** Save the full transcript of each run and add a way to open one. Use it to confirm at least one passing result is real (not "extracted from history" like Lucas's Claude Code example).

### How you will know you are done

- ✅ You can point to a **results table** that shows pass rate, cost, and latency for every model-and-setting combination.
- ✅ You chose a model based on **cost per successful outcome**, and you can say what you were optimising for (cost, latency, or quality).
- ✅ At least one task is graded on its **steps**, not just its final answer.
- ✅ Your **cache hit rate** is measured and reported, and you can explain one thing that would break it.
- ✅ You can open the **transcript** for any run and confirm a passing result is genuine.

> 💡 **Keep yourself honest:** run each task several times and read at least a few transcripts in full. If a number surprises you, the transcript is where the truth is.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self contained tasks. Each asks you to *do* one specific thing, so you get focused practice on a single skill. They are optional and independent. The **Capstone Project above is the main build**, and it already includes all of these, so feel free to skip straight to it.

### Exercise 1: write three tasks (foundational)
For a topic you know well, write three eval tasks: one easy lookup, one where the model has gotten things wrong before, and one agent style task where the **steps** matter. Write the expected answer (and expected steps) before writing any prompt.

### Exercise 2: noise vs signal (foundational)
Take one task and run it 5 times against the same model. Record the results. Is there variance? If yes, decide whether the task is ambiguous or the grader is misaligned, and fix it.

### Exercise 3: cost per successful outcome (intermediate)
Run the same task against a small model and a large model. Capture tokens, cost, and pass rate for each. Compute cost per successful outcome for both. Which wins, and is it the one you expected?

### Exercise 4: prompt caching (intermediate)
Add prompt caching to a prompt that has a large repeated prefix. Make two requests and print `cache_read_input_tokens`. Then deliberately break the cache (add a timestamp to the system prompt) and watch the read drop to zero. Explain what happened.

### Exercise 5: trim a tool output (advanced)
Take a real or simulated tool response (a chunk of JSON). Rewrite it as clean Markdown, drop irrelevant fields, and simplify any dates. Count the tokens before and after with a token counting call. Then run a task that uses it and note any change in accuracy.

---

## Cheat sheet

```text
PICKING A MODEL
  1. Build a private eval from your real tasks (not a benchmark).
  2. Grade the working AND the answer (LLM judge + code-based checks).
  3. Run each task several times; read the transcripts.
  4. Compare on COST PER SUCCESSFUL OUTCOME, not cost per token.

THREE EVAL FAILURE MODES
  Noise vs signal ........ run multiple times; high variance = bad task/grader
  Infra vs model ......... read transcripts; API/tool crashes are not the model
  Silent saturation ...... feed real production failures back into the eval

THE LEVERS
  Thinking (adaptive) .... model chooses its own reasoning depth
  Effort (low..max) ...... how hard the model works overall
  Prompt caching ......... ~90% off cached input; aim for 80-90% hit rate
  Context engineering .... clean, smaller tool outputs = fewer tokens + more accuracy

REMEMBER
  - Smaller is not always faster (fewer turns can win).
  - Append only; keep timestamps out of the cached prefix.
  - The charts give you data, not a winner; you choose what to optimise.
```

## How this connects to the rest of the course

- **Earlier, Module 2 · Lesson 3 (The Prompting Playbook):** introduces evals and test cases; this lesson uses them to choose a model rigorously.
- **Next, Module 2 · Lesson 5 (The Thinking Lever):** a deep dive on thinking and effort, the first lever here.
- **Next, Module 2 · Lesson 6 (Getting More Out of the Claude Platform):** prompt caching and context engineering in production, the curve-shifting levers here.
- **Later, Module 3 (Evals for taste):** builds out the eval idea, including LLM-as-judge versus code-based graders.

---

*Source: "Picking the right model" by Lucas (Anthropic), Code with Claude 2026, London. Code snippets are illustrative reconstructions of the approaches shown in the talk. Adapt the model names and API details to the current SDK.*

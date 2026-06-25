# Module 2 · Lesson 6: Getting More Out of the Claude Platform

> **Course:** Building with Claude, a self-paced course
> **Module 2:** Core skills, working with the model
> **Speaker:** Puneet Shah, Platform Product Manager, Anthropic
> **Source talk:** [Getting more out of the Claude Platform](https://www.youtube.com/watch?v=QIriO1-vHYw) · [full transcript](../../transcripts/code-with-claude-2026-london-2026/04_getting-more-out-of-the-claude-platform.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

Great models are only half the story: the Claude platform gives you a layer of features (prompt caching, context engineering, and an advisor pattern) that take an agent from a slow, expensive demo to a cheap, fast, production-ready product, and the work that gets you there starts with one habit, reading your transcripts.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you build **AgentTune**, taking a deliberately wasteful agent and cutting its cost by more than half while keeping (or improving) its quality, using every platform feature in this lesson. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project: build AgentTune"** section near the end, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[Effective context engineering for AI agents (Anthropic)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)** (essay). The principle-level treatment of "find the smallest set of high-signal tokens," covering compaction and curation as concepts rather than specific platform buttons.
> - **[Prompt caching (Anthropic docs)](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)** (docs). How caching works and where its roughly 90% cost saving comes from, from first principles.

## A few plain-language basics first

This lesson uses some everyday AI terms. Here they are in simple words, so nothing below is confusing:

- **LLM (Large Language Model):** the kind of AI that reads and writes text. "Claude" is an LLM.
- **Model:** one specific version of that AI. Anthropic offers a family: **Haiku** (small, fast, cheap), **Sonnet** (a balance), and **Opus** (the most capable).
- **Token:** the unit a model reads and writes in, roughly three quarters of a word. You are billed per token.
- **Input tokens / output tokens:** input tokens are what you send the model; output tokens are what it generates. They are priced separately.
- **Context window:** the maximum amount of text (in tokens) a model can hold in mind at once. Claude's largest is 1 million tokens.
- **Agent:** an AI that takes a series of actions on its own toward a goal, calling tools and reading results, rather than answering in one shot.
- **Tool:** a small function the model can choose to run. Its **schema** is the written description of what it does and what inputs it takes.
- **Latency / time to first token:** how long until the model starts replying. Lower is faster.
- **Rate limit:** a cap on how many tokens or requests you may send in a window of time.
- **Transcript (or trace):** the full record of what the model saw and did at every step. Reading these is how you debug.

You do not need to memorise these. Every term is also explained again the first time it appears below.

## Why this lesson matters

It is easy to build an impressive agent **demo**. It is much harder to put one into **production**: something that is reliably good quality, fast, and cheap enough to run a real business on. Puneet asked his audience to stand up if they had built an agent (most did), stay standing if they had shipped one to production (fewer), and stay standing if they were genuinely happy with its quality, cost, and speed (fewer still). This lesson is about closing that gap. The models give you intelligence; the **platform** is the layer on top that helps you turn that intelligence into a real product.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain **prompt caching** and its three benefits (cost, rate limits, latency), and find and fix what breaks it.
2. Apply three **context engineering** techniques: **tool search**, **programmatic tool calling**, and **compaction**.
3. Use the **advisor strategy** to get close to Opus-level quality at Sonnet or Haiku cost.
4. Build the habit that underpins all of it: **reading your transcripts**.

## Prerequisites

- Module 2 · Lesson 1 (sending a message to Claude and reading the reply).
- Helpful but optional: Module 2 · Lesson 4 (Picking the Right Model), which introduces prompt caching and context engineering as cost levers. This lesson shows them in a production agent.

---

## Part 1: prompt caching (if you remember nothing else)

> 🔑 **The single most important thing in this talk (paraphrasing Puneet):** if you remember nothing else from this lesson, think about prompt caching.

### What caching is

When you send a request, the platform processes your **input tokens** before it generates a reply. **Prompt caching** saves that processed input and reuses it. On the next message in a conversation, only the **new** tokens are processed; the rest is pulled from the cache.

### The three benefits

| Benefit | What you get |
|---|---|
| **Cost** | A **90% discount** on cached tokens, because they are not reprocessed. The savings are passed on to you. |
| **Rate limits** | Cached tokens do **not** count against your rate limit. So an 80% cache hit rate effectively gives you a **5x larger rate limit** in practice. (A "rate limit" is the cap on how much you can send per window of time.) |
| **Latency** | As the conversation grows, you are no longer reprocessing all those tokens, so your **time to first token** (how long until the reply starts) goes down. |

> 💡 **What to aim for.** If you are building an agent, target a cache hit rate of **80% or above**. (The "cache hit rate" is the share of your tokens served from the cache.) Top customers like Replit, Cursor, Perplexity, and Claude Code hit **90% plus**, because they put a lot of effort into it.

### The first step: know your hit rate

> 🔑 **Start by measuring.** The first question to answer is simply: what is my prompt cache hit rate right now? Every team that does this well starts there.

You can see this in the Console (the web dashboard at console.anthropic.com), right next to your cost and usage pages, including analytics on why a cache broke.

### What breaks the cache (and how to start)

> ❌ **The most common mistake Puneet sees:** putting a **timestamp in the system prompt** ("what day is it?"). It seems useful, but the timestamp changes on every request, which changes the system prompt, which breaks the cache. Cached tokens must be **exactly** the same to be reused.

If your hit rate is 0%, that is fine, that is why you are here. Two easy ways to start:

1. **Autocaching:** a one-line code change that implements basic prompt caching.
2. **The Claude API skill:** built into Claude Code and many other coding agents. You ask it to improve your cache hit rate, and it helps you manage and order your prompt for the best performance.

```python
# Automatic caching: the simplest start. This caches the last cacheable
# block of the request, so the heavy, repeated prefix is reused.
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    cache_control={"type": "ephemeral"},   # auto-cache the stable prefix
    system=large_stable_system_prompt,     # keep this byte-for-byte identical
    messages=messages,
)

# Then verify it worked:
print(response.usage.cache_read_input_tokens)   # > 0 means the cache is being used
```

In the live demo, an agent that started at a **0%** hit rate dropped to about a **58%** hit rate after caching was added, roughly **halving the cost**, with the exact same output. As Puneet stresses: prompt caching has **no impact on intelligence**. It is the exact same result, just pre-processed and cheaper.

---

## Part 2: context engineering

After caching, the demo agent filled up its **context window** (the 1 million token limit on how much it can hold at once). The fix is **context engineering**: the art and science of figuring out exactly what context you expose to Claude to get the best performance.

> 🔑 **The recurring instruction (Puneet says it many times):** look at your transcript to see what the model is actually seeing. Is there a lot of stuff you do not need to be passing to Claude? Or is the relevant stuff keeping it on track?

There are three techniques, each narrowing the context at a different point.

### Technique 2.1: tool search (narrow the tools)

Agents use a lot of tools, sometimes tens or even hundreds. The problem: when you define all those tools and pass them to the model, their definitions (each tool's **schema**, the written description of what it does and what inputs it takes) fill up the context, leaving less room for the actual work.

**Tool search** fixes this. You still define all your tools up front, but the model is only handed a single search tool. When it thinks it needs a tool, it calls the search, gets a list, and only **then** is the chosen tool's full definition loaded into context.

> 💡 **A real result.** Lovable used tool search and cut their overall token consumption by **10%**, and their model's performance actually **improved**, because less clutter in context means the model performs better. They rolled it out to all users.

In the demo, individual tool schemas were large: a hero retention metrics tool was **14,000 tokens**, a hero list tool **6,100**, another **9,300**. Because tool search keeps these out of context until needed, that space stays free for the real task.

### Technique 2.2: programmatic tool calling (narrow the results)

Tool search narrows which tools are loaded. **Programmatic tool calling** narrows what comes **back** from a tool.

The insight: Claude is very good at writing code. So instead of dumping a tool's full result into the model's context, you have Claude write a small Python script that calls the same tools, does a little work to **curate** (trim and shape) the content, and sends back only what is most relevant.

> 💡 **A real result.** Quora used this with HTML content, stripping away the irrelevant parts and keeping only what mattered, and saw their model's performance improve.

In the demo, the company analyses sales-call recordings from a tool called Gong. The full transcripts are long (30 to 60 minutes), and most of it is not relevant for a dashboard. With programmatic tool calling, the model wrote a script that looked at the first chunk to understand the structure, realised it only needed the **aggregate sentiment**, and looped through to extract just that, streaming it into the dashboard. A massive result block shrank to just the parts that were actually needed.

### Technique 2.3: compaction (keep the conversation going)

Models can now do hours of autonomous work, so eventually you hit the context limit. Without help, the conversation halts at a screeching stop.

**Compaction** prevents that. When you approach the limit, it **summarizes** the context (guided by your own prompt), shifts it down to a lower token count, removes the turns that are no longer relevant, and lets the conversation continue. Rinse and repeat. The effect is an almost **unlimited-feeling context**, keeping the model on track.

> 💡 **A real result.** Hex used compaction, simplified their code, and saw the model continue to perform well.

You set a **threshold** (a point at which compaction kicks in). The demo used **400K**. Puneet, who launched the 1 million context window, notes that a million is great for some scenarios, but the right combination of intelligence, cost, and latency might not be a million for you. A good starting point is often **400K or 500K**, but it changes by model. You write your own prompt to guide the summary so it keeps the key facts and does not lose the wrong context.

> 💡 **Important framing.** Puneet stresses this is not about a cool demo. Lots of AI demos are cool. The point is **production**: making sure the context really matches what is actually needed to make your product successful.

After applying all three context engineering techniques, the demo agent's cost dropped to about a third of where it had been earlier.

---

## Part 3: the advisor strategy (Opus quality, cheaper cost)

The demo agent was still running on **Opus 4.7**, a great model but a high-cost one. The question: could we get closer to Opus intelligence using **Sonnet** and **Haiku**?

The **advisor strategy** does exactly that. You run the agent with a cheaper **executor** (Sonnet or Haiku). It handles most of the work fine. But when it hits an unusual, tricky case it is not sure how to handle, it **calls the advisor** (a more capable model like Opus), asks what to do, and gets back advice.

> 🔑 **The mental model (paraphrasing Puneet).** Think of a **senior engineer paired with a junior engineer**. The junior is still hands-on-keyboard getting the work done, but the coaching, code reviews, and architecture help from the senior let them achieve far more, sometimes approaching what the senior could do solo. The same logic works with models: pairing Sonnet or Haiku with an Opus advisor approaches Opus intelligence at a fraction of the cost.

> 💡 **A real result.** Bolt used this and got better architectural decisions: on complex tasks, performance improved; on simpler tasks, there was no extra overhead, because the executor simply does not call the advisor. A Pareto-optimal trade-off. ("Pareto-optimal" means you cannot do better on one dimension without giving up another; in plain terms, it is on the best-possible trade-off curve.)

```python
# Advisor pattern: a cheap executor consults a stronger model only when stuck.
advisor_tool = {
    "type": "advisor_20260301",
    "name": "advisor",
    "model": "claude-opus-4-7",   # the strong model the executor can consult
}

response = client.beta.messages.create(
    betas=["advisor-tool-2026-03-01"],
    model="claude-sonnet-4-6",     # the cheaper executor doing most of the work
    max_tokens=4096,
    tools=[advisor_tool],          # executor reaches for the advisor on hard cases
    messages=messages,
)
```

The demo made this vivid. The company had a critical contract renewal (Metropolis) it could not afford to lose. The **Sonnet** executor read the transcripts and reported the renewal looked **green** (on track). But this mattered enough to ask the advisor, so Opus took a closer look and caught what Sonnet missed: the customer specifically wanted one superhero (Cryothene), who was unavailable on the day of the key event, which meant the renewal would actually **fail**. Green on the outside, deep red on the inside, what Puneet calls a **"watermelon."** Opus overrode Sonnet and flagged it.

> 🔑 **The advisor recovers intelligence you would otherwise lose.** You get the cost profile of the cheaper model on the easy 90%, and the judgement of the stronger model on the hard 10%.

---

## Part 4: the whole journey, and the habit underneath it

Pulling the demo together, here is the full cost reduction path the agent travelled, starting at over **10x** the final cost:

| Step | Technique | Effect |
|---|---|---|
| 1 | **Prompt caching** | Found the hit rate (0%), implemented caching, roughly **halved** cost. Same output. |
| 2 | **Context engineering** (tool search) | Narrowed which tool schemas load into context. |
| 3 | **Context engineering** (programmatic tool calling) | Curated what tool results return, sending only the relevant parts. |
| 4 | **Context engineering** (compaction) | Summarized old context at a threshold, giving near-unlimited context. Cost down to about a **third**. |
| 5 | **Advisor strategy** | Switched to a cheaper executor with a strong advisor, preserving intelligence while cutting cost further. |

> 🔑 **The thread through every step.** Before and during each change, Puneet repeats: **look at the transcript**. It is how you discover the 0% cache hit rate, how you see the bloated tool results, and how you confirm the advisor actually caught the watermelon. The transcript is your single most illustrative debugging surface.

He also closes with a reminder that the platform evolves fast: he mentioned features that had launched within the previous 24 hours, and highlighted two he is excited about: **automatic prompt caching** (a one-line way to implement caching if you never have) and **the Claude platform on AWS** (the whole platform available where many teams already run their models). The commitment, in his words, is to keep helping you build not just great demos but real production agents.

---

## Key takeaways

1. **Prompt caching first.** A 90% discount on cached tokens, an effective rate-limit boost, and lower latency, with **no** effect on intelligence. Measure your hit rate, aim for 80% plus, and keep timestamps out of the system prompt.
2. **Context engineering, three ways.** **Tool search** narrows which tools load; **programmatic tool calling** curates what tool results return; **compaction** summarizes old turns for near-unlimited context.
3. **Advisor strategy.** A cheap executor (Sonnet or Haiku) consults a strong advisor (Opus) only on hard cases, approaching Opus quality at a fraction of the cost.
4. **Read your transcripts.** Every improvement in the talk was found by looking at exactly what the model saw and did.

## Common pitfalls

- ❌ Putting a timestamp (or any per-request value) in the system prompt, which breaks the cache.
- ❌ Never checking your cache hit rate, so you do not know there is money on the table.
- ❌ Loading every tool's full schema into context up front instead of using tool search.
- ❌ Piping raw, bloated tool results straight back to the model instead of curating them.
- ❌ Letting a conversation hit the context limit and halt, instead of using compaction.
- ❌ Paying for the most expensive model on every request when an advisor pattern would do.
- ❌ Optimising from charts and dashboards alone, without ever reading a transcript.

---

## 🛠️ Capstone Project: build AgentTune

> This is the main hands on project for the lesson, and the best way to make everything above stick. You will recreate the talk's journey: take a deliberately wasteful agent and tune it step by step, watching the cost fall and the quality hold (or rise) at each stage. Start small and grow it as far as you like.

### What you will build

**AgentTune** is a small agent plus a tuning loop. It has two halves that line up with the two halves of this lesson:

1. **The wasteful agent:** a simple agent for a company you invent, that pulls data from several "sources" (you can fake these with local functions), runs on a big model with no caching, loads every tool up front, and returns raw, bloated tool results.
2. **The tuning loop:** the sequence of platform features (caching, then context engineering, then the advisor) plus a **cost-and-quality dashboard** that records cost, cache hit rate, and a quality check at every step.

> 🎯 **Pick your world.** Reuse the talk's **superheroes-for-hire** company (HeroCorp) if you find it fun, or swap in your own: a **logistics dashboard**, a **support analytics tool**, a **sales pipeline tracker**. You just need: several data sources to pull from (so tool search and curation matter), long results (so programmatic tool calling matters), a long-running conversation (so compaction matters), and at least one tricky "watermelon" case (so the advisor matters).

### Why this is the perfect practice

| Lesson skill | Where you use it in AgentTune |
|---|---|
| Measuring and improving cache hit rate | Milestone 2, the caching step |
| Tool search (narrow the tools) | Milestone 3 |
| Programmatic tool calling (curate results) | Milestone 4 |
| Compaction (near-unlimited context) | Milestone 5 |
| The advisor strategy | Milestone 6 |
| Reading transcripts | every milestone, the verification habit |

### Milestones (build them in order, each one works on its own)

1. **Build the wasteful baseline.** Create an agent for your world with 4 or more tools (each with a chunky schema), running on a big model with **no caching**, loading **all** tools up front, and returning **raw** tool results. Run a representative conversation and record the total cost. This is your red baseline.
2. **Add prompt caching.** Find your current cache hit rate (it should be near 0%). Add caching to the stable prefix, follow the rule of keeping it byte-for-byte identical (no timestamps), and re-measure. Confirm the cost drops and the output is unchanged.
3. **Add tool search.** Stop loading every tool schema up front. Give the agent a way to discover and load only the tool it needs. Re-run and record the token reduction.
4. **Add programmatic tool calling.** Pick your longest tool result and have the agent write a small script that curates it down to just the relevant part before it hits context. Record the reduction.
5. **Add compaction.** Run a long conversation that would have hit the context limit. Add a threshold and a summary prompt so it compacts and keeps going. Confirm the conversation no longer halts.
6. **Add the advisor.** Switch the executor to a cheaper model and give it an advisor (a stronger model) it can consult. Build at least one **watermelon** case where the cheap model would get it wrong and the advisor catches it. Confirm the catch.
7. **Stretch goals.** Add a Console-style mini dashboard showing cost, cache hit rate, and context size per turn. Add a transcript viewer. Try the 1-hour cache TTL for bursty traffic.

### How you will know you are done

- ✅ Your final agent costs **less than half** of the baseline (aim for the talk's roughly one-third), with quality held or improved.
- ✅ Your **cache hit rate** is measured at each step and ends up at 80% or above.
- ✅ You can point to the **token reduction** from tool search and from programmatic tool calling separately.
- ✅ A long conversation **compacts and continues** instead of halting.
- ✅ The **advisor catches a watermelon** case the cheap executor missed.
- ✅ You read the **transcript** at every step and can show what each change did to what the model saw.

> 💡 **Keep yourself honest:** change one thing at a time, re-measure, and read the transcript. If a cost drop surprises you, the transcript will tell you whether quality actually held.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self contained tasks. Each asks you to *do* one specific thing. They are optional and independent. The **Capstone Project above is the main build**, and already includes these.

### Exercise 1: find and fix a broken cache (foundational)
Write a prompt with a large stable system prompt and a timestamp at the top. Make two requests and confirm `cache_read_input_tokens` is 0. Remove the timestamp, run again, and watch the cache start being read. Explain what changed.

### Exercise 2: measure your hit rate (foundational)
Add caching to any multi-turn conversation. After several turns, compute your cache hit rate from the usage fields. Is it above 80%? If not, find what is changing in the prefix.

### Exercise 3: trim a tool result (intermediate)
Take a long tool output (a chunk of HTML or a long transcript). Write a small script that extracts only the part you actually need (for example, an aggregate sentiment). Count the tokens before and after.

### Exercise 4: compact a long conversation (intermediate)
Run a conversation long enough to approach a context threshold you set. Add compaction with your own summary prompt. Confirm the conversation continues and that the summary kept the key facts.

### Exercise 5: build a watermelon (advanced)
Construct a case that looks fine on the surface but is actually a problem underneath. Run it through a cheap model alone (it should miss it), then add an advisor and confirm the strong model catches it. Note the cost difference between the two approaches.

---

## Cheat sheet

```text
PROMPT CACHING (do this first)
  Benefits: 90% cheaper cached tokens, ~5x effective rate limit, lower latency.
  No effect on intelligence. Aim for 80%+ hit rate.
  Measure: response.usage.cache_read_input_tokens
  Breaks it: a timestamp (or any changing value) in the system prompt.
  Start fast: autocaching (one line) or the Claude API skill in Claude Code.

CONTEXT ENGINEERING (narrow what the model sees)
  Tool search ............ load only the tool you need, not every schema
  Programmatic tool call . have Claude write code to curate tool RESULTS
  Compaction ............. summarize old turns at a threshold (e.g. 400K)

ADVISOR STRATEGY (Opus quality, cheaper cost)
  Cheap executor (Sonnet/Haiku) does the work.
  Consults a strong advisor (Opus) only on hard cases.
  Senior + junior engineer analogy. Pareto-optimal cost vs intelligence.

THE HABIT UNDER ALL OF IT
  READ YOUR TRANSCRIPTS. See exactly what the model saw and did.
```

## How this connects to the rest of the course

- **Earlier, Module 2 · Lesson 4 (Picking the Right Model):** introduces prompt caching and context engineering as curve-shifting levers; this lesson shows them in a production agent.
- **Earlier, Module 2 · Lesson 5 (The Thinking Lever):** the effort and thinking dials pair naturally with these cost levers.
- **Later, Module 4 (Tools and context):** goes deeper on tool design, tool search, and programmatic tool calling.
- **Later, Module 5 (Claude Managed Agents):** compaction and the advisor pattern become part of long-running, multi-agent systems.

---

*Source: "Getting more out of the Claude Platform" by Puneet Shah (Anthropic), Code with Claude 2026, London. Code snippets are illustrative reconstructions of the approaches shown in the talk. Adapt the model names and API details to the current SDK.*

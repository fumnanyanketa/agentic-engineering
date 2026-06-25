# Module 9 · Lesson 37: Building the Best Agentic Analytics Harness

> **Course:** Building with Claude, a self-paced course
> **Module 9:** In the field, industry case studies
> **Speaker:** the CTO of Omni (London)
> **Source talk:** [Building the best agentic analytics harness: Powered by Claude, built with Claude Code](https://www.youtube.com/watch?v=K4-flzsPraE) · [full transcript](../../transcripts/code-with-claude-2026-london-2026-day-2/13_building-the-best-agentic-analytics-harness-powered-by-claude-built-wi.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

A great agent is a model plus a great **harness** plus your **business context placed right next to the data it describes**, and you get there by reading the agent's own **traces**, performing surgery on what they reveal, avoiding a "split brain" between agents, and leaning on what the model is already great at (like SQL) instead of inventing your own formats.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you build **Blobby Jr.**, a small data-answering agent with a context layer, an agentic loop, and trace-driven debugging. Everything before the Capstone is the growing-up story of Omni's real agent, Blobby, and the lessons from each phase. If you want the finish line first, jump to the **Capstone Project**, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[Semantic layer](https://en.wikipedia.org/wiki/Semantic_layer)** (essay). The semantic layer, mapping business terminology onto raw data so non-experts (and now agents) get correct answers, is the literal heart of the lesson.

## A few plain-language basics first

This lesson mixes AI and data terms. Here they are in plain words:

- **LLM (Large Language Model):** the kind of AI that reads and writes text and code. Claude is an LLM.
- **Agent:** an AI that takes a series of actions on its own in a loop toward a goal, rather than answering in one shot.
- **Harness:** all the code around the model: the loop, the tools, error handling, checkpointing. The model is the engine; the harness is the car.
- **SQL:** the standard language for asking questions of a database (for example "count the orders from last month").
- **Data warehouse:** a large database that holds a company's data for analysis.
- **Semantic layer:** a translation layer that sits on top of the raw data and tells the system how to use it correctly: which table matters, what your terms mean, who can see what. It is the heart of this talk.
- **Context:** the business-specific information the model needs to answer questions about *your* company rather than companies in general.
- **Trace:** a detailed record of an agent's inner workings during a session: what it thought, which tools it called, what came back. Reading traces is how you debug an agent.
- **Sub-agent:** a smaller agent the main agent calls to do a piece of work.
- **Eval (evaluation):** a set of test cases that measure quality. Covered more in Module 3.
- **CTE (common table expression):** a way of structuring a SQL query into named, readable steps.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Omni is an AI analytics platform: you "talk to your data" in plain language and get answers, charts, and dashboards. Behind it is an agent named Blobby, built over 18 months from a clumsy one-shot tool into a refined data analyst. The talk is unusually honest about the *journey*, every awkward phase and the specific lesson that fixed it. Two themes make it valuable to any builder. First, the CTO insists that being heavy *users* of Claude Code taught the team what a good harness looks like, which they then baked into their own. Second, almost every quality jump came not from a cleverer prompt but from *reading the agent's traces* and acting on what they showed. This is what operating an agent really looks like.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain what a **semantic layer** does and why context belongs *next to* the data it describes.
2. Describe how Omni added structured context (AI context, sample queries, values) to lift answer quality.
3. Use **traces** to diagnose why an agent behaves badly, and recognise the **split-brain** failure between an outer agent and a sub-agent.
4. Apply two leverage moves: pick the model that fits the conversation length, and let the model produce what it is already great at (SQL) instead of a custom format.

## Prerequisites

- A basic understanding of agents, tools, and prompts (Module 2).
- Helpful but optional: Module 3 (Evals), since Omni's quality work is eval- and trace-driven.

---

## Part 1: building *with* Claude, and the semantic layer

Two backdrops frame the talk. First, *building with* Claude: Omni's commit graph to its main branch shoots upward, and the CTO notes that Claude Code let even him, the CTO of a company with hundreds of customers, keep writing code. The turning point was when Claude Code with the Opus model arrived and senior engineers said, "wait a minute, this is real, actually helping consistently." Velocity is a core value ("Ship It"), reinforced by a Friday all-hands that is mostly live demos.

Second, *building with* Claude in the product. Omni lets you talk to your data. The flow:

```text
user question
   -> Claude translates it into a SEMANTIC QUERY
   -> the SEMANTIC LAYER (a map on top of your warehouse) turns it into correct SQL
   -> SQL runs against the data warehouse
   -> results -> visualization -> a short summary
```

> 🔑 **The core problem.** Claude is "incredible at answering questions," but to answer questions about *your* business, "you need to tell it more about your business." It knows how businesses work in general; it does not know your terminology or how your data is shaped. Bridging that gap is the whole job.

How hard is the gap? Even "last quarter" means different things in the same company: in product/engineering it means the calendar quarter; in sales it means the fiscal quarter. All of that has to be encoded so the model gets the right answer.

The **semantic layer** is the bridge. It sits on top of the warehouse and does three things:

| Job | What it means | Why it matters |
|---|---|---|
| **Curate the data** | Real warehouses have hundreds of "revenue" tables and "opportunity" tables. Curation says which one matters and how to join them. | Toy demos work on 10 clean tables; real ones do not. |
| **Encode context** | Capture meaning, terminology, and how fields are used. | The model needs business meaning, not just column names. |
| **Permissions** | Ensure people see only the data they are allowed to. | Safety and compliance. |

> 💡 **Context belongs next to what it describes.** The CTO draws the analogy to Claude Code's `CLAUDE.md` files: "the more you can do to localize that context next to the parts of the code that it applies to, the better results you're going to get." Omni's semantic layer does the same, putting context right next to the field definition it applies to, not in a separate file elsewhere. And a **feedback loop** keeps it current: each new question can feed back into the definitions, for continuous learning.

---

## Part 2: Blobby grows up, phase by phase

Blobby was not always a refined analyst. Here is the journey, with the lesson from each phase.

### Phase 1: single question, single answer

The first Blobby just answered one question at a time. The fix was more **metadata** about how the data is used. Omni always had `label` and `description` fields, then added three new kinds of context aimed specifically at the model:

| Added context | What it is | Why it helped |
|---|---|---|
| **AI context** | A note written for the LLM: how to use this field, what to reference when asked about it. | Lets the data team steer the model toward quality answers. |
| **Sample queries** | "Here is the query you would run to answer a question like X." | Grounds the model in real, typical usage. |
| **Values** | A taste of a field's actual values (for example regions: EMEA, NAM, APAC). | The model infers the rest, and learns these are abbreviations, so "United States" maps to "US." |

> 💡 The "values" trick is subtle but powerful: a few example values teach the model the *shape* of a field, so it can fuzzy-match a user's wording to the real data.

### Phase 2: add an agentic loop

Blobby was still not really an agent. The big leap was wrapping it in an **agentic loop**, a real harness Omni built themselves, with tasks "like all good agents have."

> 🔑 **The loop's superpower is recovering from errors.** One of the earliest "massive quality increases" came from two simple moves: (a) tell Blobby how to recover from errors and give it a budget to do so, and (b) invest in *great error messages* that describe what went wrong and how to fix it. That alone made the harder evals improve dramatically.

This phase also forced a model change. Blobby had used **Haiku** (small, fast, fine for one-shot question-and-answer). But "once you get into these more elaborate agentic conversations, it's just not designed for those," so Omni switched to **Sonnet**. Token use went up (longer, more complex conversations, by design), and so did value: customers started saying Blobby answered questions in two minutes that would have taken them hours, and usage took off.

> 🔑 **Match the model to the conversation, not the task in the abstract.** Haiku is great, but multi-step agentic loops need a model built for them. Picking the model is part of harness design.

### Phase 3: the blubotomies (trace-driven surgery)

Then came pressure from Omni's "loudest and most critical user," the CEO: "I know this thing's really good, but it screwed up this question. Go fix it." The team's instinct, "LLMs are a little unpredictable, you'll have to accept it," got the reply "not good enough, go fix it."

That led to the most important habit in the talk:

> 🔑 **Invest in seeing the traces of bad sessions.** A **trace** shows "the inner workings of how the agent is talking to itself and reacting in these loops." Reading them revealed that seemingly "random bad sessions" were actually "rooted in real problems." The surgeries that followed were nicknamed the **blubotomies**.

The biggest find was a **split brain**. Omni's design had been "a little too clever": an *outer* agent produced the task list and knew what data was available, but a *sub-agent* did the query generation. The trap:

```text
SPLIT BRAIN (the bug)
  outer agent: knows all the data; does NOT know what one query can do
     -> "sub-agent, answer a question about PRs AND support data, and summarize"
  sub-agent: only generates ONE query; does NOT know the full data picture
     -> "I can't answer that in a single query"
  result: confusing, unpredictable failures
```

The fix, which their engineer Joel called **consolidating the brain**: pull the query-generation tools up into the outer agent's harness so there is one mind, not two.

> 🔑 **Avoid a split brain between an outer agent and a sub-agent.** When knowledge and capability are divided across agents that cannot see each other's world, you get surprising failures. Consolidating them "got rid of a lot of this seemingly unpredictable surprising behavior" and improved the harder evals dramatically.

### Phase 4: let Claude write SQL

Next realization: when you use Claude directly to write SQL, it answers some hard questions Blobby itself struggled with. There was a backstory, Omni had once built a full SQL parsing engine, then shelved it because it could not handle every random SQL people threw at it. But the bet now looked different:

> 💡 "I think it's probably a safe bet to assume that the good people at Anthropic are investing heavily in making Claude really good at SQL." So Omni dusted off the parser and changed how it exposed query generation.

The old interface fed Blobby a "JSONified," highly structured proprietary query format. The new one lets Blobby **write SQL directly**, which the parser then reads (with guardrails to keep the parser from falling over). Two wins:

1. **No proprietary format to teach.** Blobby already knows SQL; it does not need to learn Omni's invented JSON shape.
2. **One-shot instead of three.** Questions that used to take three or four attempts, or awkwardly chained queries, now get answered in a single, more efficient query. (A bonus: Claude likes to write SQL with **CTEs**, common table expressions, and the parser handled those well.)

> 🔑 **Lean on what the model is already great at.** Where a frontier capability (SQL) overlaps your problem, expose that capability directly instead of inventing a custom format the model has to be taught. It is less work for you and produces better, more efficient results.

---

## Part 3: where Blobby is today, evals, and building like a user

Today Blobby is a full agentic system: an **outer loop** that checkpoints executions so it can recover from any failure, and an **inner loop** with a growing set of tools (generate dashboards, generate visualizations, validation tools, plus tools that let Blobby improve the semantic layer itself).

On evals, the CTO offers a refreshing take:

> 💡 "I love evals for a different reason than most people." His favourite thing is "the raw trace data," the observability. Being able to ask "this was bad, why?" and dig through the data was "enlightening." Capturing that judgment into an automated **judge** (a model that grades outputs) is "a nice efficiency gain as well." Predictability and quality are the core promise: the CEO must get the right answer, and the *same* answer every time.

And the meta-lesson that ties the talk together:

> 🔑 **Being users of Claude Code taught Omni what a good harness looks like.** Beyond the productivity gains, "being users of Claude Code helped us understand what a good harness looks like," and they baked those lessons into Blobby. When deciding how to let users explore the semantic model, they asked, "well, let's see what Claude Code does, because a semantic model is not that different from a code base." Using the best agent makes you better at building one.

The live demo shows it end to end: ask about pull requests, Blobby recognises "PRs" as GitHub pull requests, finds them in the semantic model, fuzzy-matches a repository filter (handling typos), generates and runs a query, visualizes it, and summarises. It can build a whole dashboard from one prompt, and a user can pop any result into a "workbook" to manipulate it directly, AI to build UI, then humans to validate and refine.

---

## Key takeaways

1. **The agent is model + harness + context.** All three matter; the model alone is not enough.
2. **A semantic layer bridges to your business:** it curates the right data, encodes meaning, and enforces permissions. Without it, the model answers about businesses in general, not yours.
3. **Put context next to the data it describes,** like `CLAUDE.md` next to code. Add AI-specific context, sample queries, and example values.
4. **The agentic loop's superpower is error recovery.** Tell it how to recover, give it a budget, and write great error messages.
5. **Match the model to the conversation.** Small models suit one-shot Q&A; multi-step loops need a model built for them.
6. **Read the traces.** "Random" bad sessions are usually rooted in real, findable problems. Trace-driven surgery is how you raise quality.
7. **Avoid the split brain.** Do not divide knowledge and capability across agents that cannot see each other's world. Consolidate the brain.
8. **Lean on what the model already excels at** (SQL) rather than inventing a custom format to teach it.
9. **Use the best agent to learn how to build one.** Being a Claude Code user teaches you what a good harness feels like.

## Common pitfalls

- ❌ Expecting the model to answer business questions with no semantic layer or context.
- ❌ Stashing context in a separate file far from the data it describes.
- ❌ Skimping on error messages, so the agent cannot recover.
- ❌ Using a small, fast model for long multi-step agentic conversations.
- ❌ Guessing at why an agent failed instead of reading its traces.
- ❌ Splitting knowledge and capability across an outer agent and a sub-agent that cannot see each other.
- ❌ Inventing a proprietary query/output format when the model is already fluent in a standard one (SQL).

---

## 🛠️ Capstone Project: build Blobby Jr.

> This is the main hands on project for the lesson. You will build **Blobby Jr.**, a small "talk to your data" agent with a context layer, an agentic loop, trace-driven debugging, and direct SQL generation. Start with one dataset and a few questions, then grow.

### What you will build

An agent that answers natural-language questions over a small dataset by generating SQL, with a semantic/context layer that encodes your business meaning, an agentic loop that recovers from errors, and trace logging you use to debug. The deliverable is a working agent plus a short "blubotomy log" of bugs you found in the traces and the fixes.

> 🎯 **Pick your world.** Use any small dataset you understand: a CSV of sales, a SQLite of a side project, a GitHub export, a sports stats file. You need (a) fields whose meaning is not obvious from their names, (b) at least one term that is ambiguous (like "last quarter"), and (c) some realistic data values worth fuzzy-matching.

### Why this is the perfect practice

| Lesson idea | Where you use it in Blobby Jr. |
|---|---|
| Semantic layer / context next to data | Milestone 2, you annotate fields with AI context, samples, values |
| The agentic loop + error recovery | Milestone 3, the loop with great error messages |
| Match model to conversation | Milestone 3, switch model when conversations get long |
| Read the traces | Milestone 4, log and inspect every step |
| Avoid the split brain | Milestone 4, consolidate tools into one agent |
| Lean on SQL | Milestone 5, generate SQL directly |
| Evals and a judge | Milestone 6, test quality and consistency |

### Milestones (build them in order, each one works on its own)

1. **Single-shot baseline.** Build the simplest version: a question goes in, the model writes one query, you run it, return the answer. Note where it gets things wrong.
2. **Add the context layer.** For each field, add: an **AI context** note (how to use it), a **sample query**, and a few **example values**. Put each annotation right next to its field definition. Re-test and record the improvement.
3. **Wrap it in an agentic loop.** Add a loop with tasks, error recovery (tell it how to retry, give it a budget), and *descriptive* error messages. When conversations get long and multi-step, switch from a small model to one built for agentic work, and note the difference.
4. **Add traces, then operate on them.** Log the agent's inner steps (thoughts, tool calls, results). Run a batch of tough questions, read the traces of the failures, and find the real root causes. If you split work across a sub-agent, watch for the split-brain symptom and consolidate. Keep a "blubotomy log."
5. **Generate SQL directly.** If you started with a custom/structured query format, switch to having the model write SQL directly and parse it (with guardrails). Compare attempts-per-answer before and after.
6. **Add evals and a judge.** Write test questions with expected answers. Add an LLM judge for the fuzzier cases. Confirm the agent gives the *right* answer and the *same* answer each time.
7. **Stretch goals.** Add a feedback loop where a corrected answer updates the context layer. Add a dashboard-from-one-prompt feature. Let the agent improve the semantic layer itself.

### How you will know you are done

- ✅ Blobby Jr. correctly resolves an ambiguous term (your "last quarter") thanks to context, not luck.
- ✅ It fuzzy-matches a user's wording to real data values (handling a typo or abbreviation).
- ✅ Its loop recovers from at least one error using a descriptive error message.
- ✅ Your blubotomy log shows at least one bug you found *only* by reading traces, and its fix.
- ✅ Direct SQL generation answers in fewer attempts than your earlier custom format.
- ✅ Evals show consistent, correct answers across repeated runs.

> 💡 **Keep yourself honest:** if you "fixed" a bad session by tweaking the prompt without reading the trace, you guessed. The whole point is to *see* the inner workings first.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each focused on one idea. They are optional and independent. The Capstone above covers all of them.

### Exercise 1: annotate a field (foundational)
Take one confusingly-named field in a dataset. Write its AI context note, one sample query, and a few example values. Show a question the model now answers that it failed before.

### Exercise 2: ambiguous terms (foundational)
List three terms in your domain that mean different things to different teams (like "last quarter"). For each, write the context the model would need to disambiguate it.

### Exercise 3: error recovery (intermediate)
Take an agent that fails on a bad query. Add a descriptive error message and a retry budget. Show the agent recovering. Then make the error message vague and watch it fail, to prove the message matters.

### Exercise 4: read a trace (intermediate)
Capture a full trace of one bad agent session. Annotate it step by step, find the root cause, and write the one-line fix. Resist changing anything until you have read the whole trace.

### Exercise 5: SQL vs. custom format (advanced)
Build two versions of query generation: one with a custom structured format you invent, one where the model writes SQL directly. Compare attempts-per-answer, efficiency, and how much you had to teach the model.

---

## Cheat sheet

```text
A GREAT AGENT = MODEL + HARNESS + CONTEXT

CONTEXT (the semantic layer)
  - curate the right data (which of the 100 "revenue" tables matters)
  - encode meaning, terminology, ambiguous terms ("last quarter")
  - permissions
  - put context NEXT TO the field it describes (like CLAUDE.md next to code)
  - add: AI context notes, sample queries, example values

HARNESS (the loop)
  - agentic loop with tasks + checkpointing
  - SUPERPOWER: error recovery -> tell it how to retry + great error messages
  - match the model to the conversation (small = one-shot; big = multi-step loops)

DEBUGGING (the blubotomies)
  - READ THE TRACES. "random" bad sessions have real root causes.
  - avoid the SPLIT BRAIN: don't divide knowledge + capability across
    an outer agent and a sub-agent that can't see each other. Consolidate.

LEVERAGE
  - lean on what the model already excels at (SQL) instead of a custom format
  - be a USER of the best agent (Claude Code) to learn what a good harness feels like
  - evals = predictability + the raw trace data you learn from
```

## How this connects to the rest of the course

- **Earlier, Module 2 (Core skills):** model choice, tools, and harness ideas in their original form.
- **Earlier, Module 3 (Evals):** the evals and LLM-as-a-judge techniques Omni relies on.
- **Earlier, Module 9 · Lesson 32 (Man Group):** the same insight that the model is a commodity and your business context is the real asset.
- **Earlier, Module 9 · Lesson 36 (Lovable):** another team that operates an agent at scale by reading what the agent is doing and feeding it back in.
- **Earlier, Module 9 · Lesson 34 (Legora):** the shared lesson that being a heavy coding-agent user teaches you how to build a good harness.

---

*Source: "Building the best agentic analytics harness: Powered by Claude, built with Claude Code" by the CTO of Omni, Code with Claude 2026, London. Code-style blocks are illustrative reconstructions of the flows and architecture described in the talk, which was delivered with slides and a live demo rather than code listings.*

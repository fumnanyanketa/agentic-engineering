# Module 5 · Lesson 17: Agents That Remember

> **Course:** Building with Claude, a self-paced course
> **Module 5:** Building agents, Claude Managed Agents
> **Speaker:** Kevin, Engineer, Anthropic
> **Source talk:** [Agents that remember](https://www.youtube.com/watch?v=geUv4CjPpxI) · [full transcript](../../transcripts/code-with-claude-2026-london-2026-day-2/05_agents-that-remember.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

By default each run of an agent is a blank slate that forgets everything when it ends, so this lesson shows how to give agents a shared, file-like **memory store** they can read and write across runs, and a background process called **dreaming** that cleans up and enriches that memory so it stays useful as it grows.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you build **RecallDesk**, a small support agent that remembers customers across separate conversations and then learns from its own past runs. Everything before the Capstone teaches the pieces you will assemble there. If you want to see the finish line first, jump to the **"Capstone Project: RecallDesk"** section near the end, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[LLM Powered Autonomous Agents (Lilian Weng)](https://lilianweng.github.io/posts/2023-06-23-agent/)** (essay). Its memory section is the durable articulation of short-term (in-context) vs long-term (external store) memory and retrieval, the precise idea of giving agents memory across sessions.
> - **[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)** (paper). The seminal paper on combining parametric memory with an external, retrievable store, the foundation of retrieval-based long-term memory.

## A few plain-language basics first

This lesson uses some everyday agent terms. Here they are in simple words, so nothing below is confusing:

- **Agent:** an AI that takes a series of actions on its own toward a goal, instead of answering in one shot. Think of it as Claude with hands: it can call tools, read files, and decide what to do next.
- **Claude Managed Agents (CMA):** Anthropic's hosted platform for running agents reliably. It handles the hard infrastructure parts (servers, containers, scaling) so you focus on the agent's behaviour.
- **Session:** one run of an agent, usually one conversation thread. By default a session is **ephemeral**, which means it disappears when it ends and remembers nothing afterwards.
- **Environment:** the setup an agent runs inside (its tools, files, and configuration). You create an agent and an environment once, then start many sessions against them.
- **Memory store:** a persistent, file-system-like place an agent can read from and write to. "Persistent" means it survives after a session ends, so the next session can use it.
- **File system:** the familiar folders-and-files way of organising data on a computer. Claude already knows how to explore one with everyday commands.
- **Tool:** a small function the model can choose to run, for example "read this file" or "search for a keyword." Reading and writing memory is done through tools.
- **Transcript:** the saved record of everything that happened in a past session (the messages, the tool calls, the results).
- **Dreaming:** a background job that reviews old transcripts and an existing memory store, then produces a cleaned-up, enriched copy of that memory.

You do not need to memorise these. Every term is explained again the first time it appears below.

## Why this lesson matters

Most agents today are islands. As Kevin puts it, "the agent doesn't remember information from the past and it doesn't transfer information to future sessions." That is fine for a one-off question, but it breaks down in real workflows where the same agent (or a team of agents) handles many related tasks over days. They repeat the same mistakes, re-learn the same facts, and cannot hand knowledge to each other.

This lesson gives you the building block that fixes this: a memory store agents share across sessions. It then shows the problem that memory creates (stores grow messy and stale over time) and the feature that solves *that*: dreaming. By the end you will be able to give your own agents a working memory and keep it healthy.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain the **base case** (isolated sessions) and demonstrate that information does not carry over without memory.
2. Create a **memory store**, attach it to a session, and watch an agent read and write to it across separate runs.
3. Use the memory store's extra controls: a **steering prompt**, **read-only** versus **read-write** access, file **versioning**, and manual edits.
4. Run a **dream job** to fact-check, consolidate, deduplicate, and enrich a memory store, and understand why it runs **asynchronously** (in the background) and **non-destructively** (without changing your original).
5. Describe sessions, memory, and dreaming as three **composable layers** that scale together.

## Prerequisites

- Earlier Module 5 lessons on Claude Managed Agents (the concepts of an **agent**, an **environment**, and a **session**). This lesson adds two new concepts on top of those.
- Comfort running commands in a terminal, since the demo uses a command-line interface (CLI) alongside the web console.

---

## Part 1: the base case, an agent with no memory

Before adding anything, it helps to feel the problem. Kevin starts from a **bootstrap script** (a small setup script included in the workshop repository) that seeds an agent, an environment, and a few previous sessions to work with.

The base case is two short sessions:

```text
Session A ("write test with no memory")
  You: "Here are notes from the CMA talk: multi-agent orchestration,
        outcomes, and memory. I uploaded my notes at <url>."
  Agent: "Great, thanks for the information. Not sure what else
          you want me to do here."

Session B (a brand new session, asked later)
  You: "What did I learn from the CMA talk?"
  Agent: "I don't really have access to that information.
          I can help you in these ways instead..."
```

That is the whole problem in two steps: you told the agent something in one session, asked another session about it later, and **nothing transferred**.

> 🔑 **Key idea: a session is an island by default.** Each session is an isolated instance of an agent running. It is typically one conversation and typically ephemeral (it vanishes when it ends). Without a shared place to store information, knowledge cannot move from one session to the next.

> 💡 The demo agent here uses **Sonnet 4.6**, the model chosen when the agent was first created. The forgetting has nothing to do with which model you pick. It is a property of how sessions work, not a weakness of the model.

---

## Part 2: memory stores, giving the agent somewhere to remember

The fix mirrors how humans work: give the agent a memory. A **memory store** is a persistent, file-system-like store that attaches as a resource to the sessions you create, giving agents the ability to read and write information across sessions.

Two design choices make this powerful:

- **It is mounted as a real file system.** Because the memory store appears to the model as ordinary files and folders, the model can use tools it already knows: **bash** (the standard command-line shell) to explore, **grep** (a standard search command) to find keywords, and plain file reads. As Kevin notes, the file system is "such a powerful interface for the model."
- **You decide the boundaries.** You can create as many stores as you like and scope them however you want: one per user, one per workspace, one per organisation. There is no fixed rule. ("Scope" just means who or what a store belongs to.)

> 🔑 **Key idea: memory is a shared file system, not a magic black box.** Claude is already very good at navigating files with bash and grep, so memory leans on that strength instead of inventing a new interface. The principle is to get out of the model's way and let it use skills it already has.

### Step 2.1: create the memory store

```bash
# Create a memory store. Name and description are the main parameters.
cma memory-stores create \
  --name "CWC memory" \
  --description "Notes and follow-ups from Code with Claude"
```

After creating it, you can see it in the web **console** under Manage Agents -> Memory Stores. It shows as **active**, and clicking in gives you a **file system viewer** of its contents (empty at first). You can also manually add a memory: create a file under a specific path and put content in it by hand.

### Step 2.2: attach the store to a session

```bash
# Start a session that uses the memory store.
cma sessions create \
  --agent-id "$AGENT_ID" \
  --environment-id "$ENV_ID" \
  --title "write test WITH memory" \
  --memory-store-id "$MEMORY_STORE_ID" \
  --memory-prompt "Save key facts, links, and follow-ups for future sessions." \
  --memory-access "read_write"
```

Two extra parameters are worth knowing:

| Parameter | What it does | When to use it |
|---|---|---|
| **Memory prompt** | Steers the agent on what to read and write (for example "focus on this link" or "remember these specific details for the future"). | When you want memory focused on a particular area, like an investment agent that should always remember certain facts. |
| **Access** | Defaults to **read-write**. Set to **read-only** so the session can read memory but cannot change it. | When a store should be a stable source of truth that one kind of session should not edit. |

### Step 2.3: watch memory work across two sessions

Now repeat the earlier test, but with the store attached:

```text
Session C ("write test WITH memory")
  You: "Here are notes from the CMA talk: multi-agent orchestration,
        outcomes, and memory. Notes at <url>."
  Agent: (first checks memory: "Is there anything I should recall?")
         (store is empty, so it WRITES the notes to sessions.md)
         "Saved your notes to memory."

Session D (new session, same memory store)
  You: "What did I learn from the CMA talk?"
  Agent: (reads memory, runs grep for "CMA")
         (finds the notes from Session C)
         "Here is what you learned: multi-agent orchestration,
          outcomes, and memory. Your notes: <url>."
```

The behaviour flips. The agent first looks at memory, saves new information when it is missing, and on a later run uses grep to find what it stored. Knowledge now moves between sessions.

> ✅ **Best practice: let it read before it writes.** A well-behaved memory agent checks the store first ("do I already know this?") before answering or saving. The shared store is what makes a swarm of agents able to build on each other's work instead of starting cold every time.

### Step 2.4: inspect and edit the store

The platform gives you ways to look inside and maintain a store:

- **List the memory files** in a store from the CLI.
- **Versioning:** every change to a file creates a new version, with endpoints to view history. ("Versioning" means keeping a record of each edit so you can see what changed and roll back.)
- **Manual edits:** in the console file viewer you can fix something Claude wrote incorrectly, add information by hand, or organise files into subdirectories (folders inside folders).

---

## Part 3: dreaming, keeping memory healthy as it grows

Memory solves one problem and quietly creates another. When agents read and write to a store over time, Kevin observed, "they can start just kind of dumping information." Every task adds more notes, so the store grows without limit, gets disorganised, accumulates duplicates, and goes **stale** (out of date). Nothing in plain memory cleans that up.

This is what **dreaming** is for. A **dream** is an **asynchronous** job (it runs in the background, not while your agents are working) that looks over an input memory store plus a batch of previous session transcripts, then runs a special **harness** over them. ("Harness" means the surrounding code and agents that drive the model.) Dreaming does several jobs at once:

- **Fact-checks** the existing memories.
- **Enriches** them with extra detail (dates, specific identifiers, links).
- **Organises, consolidates, and deduplicates** so the store does not grow unbounded.
- Produces an **output memory store** you can attach to future sessions for faster, smarter recall.

### Step 3.1: launch a dream job

```bash
# Dream over one memory store using a batch of past sessions.
cma dreams create \
  --model "claude-opus-4-7" \
  --memory-store-id "$INPUT_MEMORY_STORE_ID" \
  --session-ids "$SESSION_1,$SESSION_2,...,$SESSION_N" \
  --instructions "Backfill exact dates and identifiers. Keep the
                  store organised with a clear index."
```

The parameters:

| Parameter | What it controls |
|---|---|
| **Model** | Quality versus cost. Choose **Opus 4.7** for higher quality or **Sonnet 4.6** to save tokens. |
| **Memory store** | The input store to dream over. |
| **Session IDs** | The transcripts to learn from. Dream over, say, 10 to 20 a night, up to around 100 (with more scaling coming). |
| **Instructions** (optional) | Extra steering on top of the default prompt, for example "backfill these domain-specific details" or "use this folder structure." |

### Step 3.2: how dreaming runs under the hood

Dreaming is built directly on Claude Managed Agents primitives, so you get real **observability** (the ability to watch and diagnose what it is doing). It is a **multi-agent** setup:

```text
                 ┌──────────────┐
                 │ Orchestrator │  spins up and tracks sub-agents
                 └──────┬───────┘
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
   ┌─────────┐     ┌─────────┐     ┌─────────┐
   │ sub-agent│    │ sub-agent│    │ sub-agent│  one per input session
   │ reviews  │    │ reviews  │    │ reviews  │  (fact-check, enrich,
   │ session 1│    │ session 2│    │ session N│   organise)
   └─────────┘     └─────────┘     └─────────┘
```

An **orchestrator** (a coordinator agent) spawns one **sub-agent** per input session and keeps them all running. This design is **exhaustive by design**: as Kevin says, if you give it 100 sessions, you want every one looked over so nothing is missed. You can click into the dream's own session in the console to see exactly what it is doing.

> 🔑 **Key idea: dreaming is non-destructive.** It never touches your input store. It **clones** the input into a separate **output memory store** and writes there, so every edit is safe. You attach the output to future sessions when you are happy with it.

While the job runs, the console updates a live **token count** so you can track progress. A dream can take anywhere from a couple of minutes to hours depending on how many transcripts you give it, which is exactly why it runs asynchronously: this is not something you want to do live while agents are working.

### Step 3.3: what a dream produces

When the job finishes, the console shows a **diff** (a side-by-side view of what changed). In the demo, dreaming:

- Created an **index file**: a small file of **slugs** (short labels) pointing to the right memory files, so future agents can quickly grok where to look instead of running a wide grep. ("Grok" means understand at a glance.)
- Added new files that were not in the original sessions, for example an **event logistics** file with the full schedule and names.
- **Reformatted** an existing memory file, adding a slug, a description, metadata, and more detail.

> 💡 More detail genuinely helps future sessions. While an agent is mid-task, it is hard to predict what a later agent will need. So it is better to write extra detail down now, and let a future dream remove anything that turns out to be unneeded.

### Step 3.4: use the enriched memory in a new session

```bash
# Fetch the dream's output store, then start a session that uses it.
OUTPUT_STORE=$(cma dreams get --dream-id "$DREAM_ID" --json | jq -r '.output_memory_store_id')

cma sessions create \
  --agent-id "$AGENT_ID" \
  --environment-id "$ENV_ID" \
  --title "recall test on dreamed memory" \
  --memory-store-id "$OUTPUT_STORE"
```

Asked "what sessions did I attend, what links do I have, and what follow-ups did I flag," the agent now reads the index first, jumps straight to the right files, and returns a far richer answer (a recap of every session, timestamps for day two, and resource links). When you are satisfied, you can **retire** the old store to keep the number of stores in your organisation reasonable, without affecting earlier sessions.

---

## Part 4: three composable layers

Step back and the whole feature set lines up as three layers that build on each other:

| Layer | What it is | What it adds |
|---|---|---|
| **Session** | One isolated, usually ephemeral run of an agent. | The base unit of work. |
| **Memory store** | A shared, persistent file system attached to sessions. | Connects information **across** sessions. |
| **Dreaming** | A background multi-agent job over memory plus transcripts. | **Organises, enriches, and improves** memory over time so it scales. |

> 🎯 **Why the layers matter together.** Sessions alone forget. Memory alone grows messy. Dreaming keeps the memory manageable, deduplicated, and fresh even as you scale up the number of sessions and the volume of information flowing through them.

### A note on cost

Dreaming is meant to be exhaustive, so it uses a lot of tokens. The good news is that because most of the work is **agentic** (the same prompts and context reused across steps), most tokens are **cached**, with about a **95% cache hit rate** expected on most dream sessions. ("Caching" means reusing already-processed text so you are not billed full price for it again.) Anthropic is also exploring lower-cost options such as a batch-style discount for scheduling dreams at off-peak times, plus the usual levers: switch the model, steer the prompt, and budget tokens.

---

## Key takeaways

1. **Sessions are islands by default.** Without memory, nothing carries from one run to the next, regardless of the model.
2. **A memory store is a shared file system.** It is mounted as real files so the model can use bash, grep, and file reads it already knows.
3. **You control the boundaries.** Create as many stores as you like, scope them per user or workspace or org, and set read-only versus read-write access.
4. **Memory grows messy over time.** Agents dump information, leaving duplicates and stale facts.
5. **Dreaming fixes that.** It runs in the background, fact-checks, enriches, deduplicates, and writes to a non-destructive output store with a full diff.
6. **Think in three layers.** Sessions, memory, and dreaming compose so memory stays useful as you scale.

## Common pitfalls

- ❌ Expecting an agent to "just remember" without attaching a memory store. It will not.
- ❌ Letting a store grow forever with no dreaming, so it fills with duplicates and stale notes.
- ❌ Giving a session **read-write** access when it should only consume a stable source of truth (use **read-only**).
- ❌ Running dreaming on the hot path. It can take minutes to hours, so keep it asynchronous and out of band.
- ❌ Assuming dreaming edits your original store. It clones to an output store, so remember to attach that output going forward.
- ❌ Skimping on detail when writing memory because you cannot predict what a future agent will need.

---

## 🛠️ Capstone Project: RecallDesk

> This is the main hands-on project for the lesson and the best way to make everything above stick. You will build a small support agent that genuinely remembers customers across separate conversations, then teaches itself from its own history using dreaming. Start as small as a single store and one session, and grow it.

### What you will build

**RecallDesk** is a customer-support agent on Claude Managed Agents that:

1. Remembers each customer's facts and open issues across separate sessions, using a memory store.
2. Keeps that memory clean and enriched over time by running nightly dream jobs.
3. Lets a human inspect, diff, and correct what the agent learned.

> 🎯 **Pick your world.** Use a support desk for any product you find fun: a streaming service, a bike-share scheme, or a coffee subscription. You just need recurring customers who contact support more than once (so memory matters) and a few facts worth remembering between visits (plan, past issues, preferences).

### Why this is the perfect practice

| Lesson skill | Where you use it in RecallDesk |
|---|---|
| Proving the base case | Milestone 1, show forgetting with no memory |
| Creating and attaching a memory store | Milestone 2 |
| Read-before-write behaviour | Milestone 3, recall across sessions |
| Steering prompt and access controls | Milestone 4 |
| Versioning and manual edits | Milestone 5 |
| Running a dream job | Milestone 6 |
| Reading a dream diff and using the output store | Milestone 7 |

### Milestones (build them in order, each one works on its own)

1. **Base case.** Create an agent, an environment, and a memory-free session. Tell it a customer fact in one session, ask a new session about it, and confirm it has forgotten. Save both transcripts as your "before" proof.
2. **Add memory.** Create a memory store called `recalldesk-memory` and confirm it shows as active in the console.
3. **Recall across sessions.** Attach the store to a session, tell it a customer fact, and watch it write to a file. Open a fresh session with the same store and confirm it reads (and greps) the fact back. This is the heart of the project.
4. **Steer and protect.** Add a **memory prompt** that tells the agent exactly what to save (customer ID, plan, open issues). Create a second **read-only** store for company policy and attach both, proving the agent can read policy but not edit it.
5. **Inspect and correct.** List the store's files from the CLI, view a file's version history after an edit, and manually fix one fact in the console viewer.
6. **Dream.** Run several support sessions to fill the store, then launch a dream job over those transcripts with custom instructions ("backfill exact dates, build an index"). Watch the live token count and open the dream's own session to see its sub-agents.
7. **Use what it learned.** Read the dream diff (index file, enriched facts), fetch the output store, and start a new session on it. Confirm the agent answers faster and richer than in Milestone 3. Optionally retire the old store.

### How you will know you are done

- ✅ You can show a **before** (forgetting) and **after** (recall) pair of transcripts.
- ✅ A brand new session correctly answers a question using only what an **earlier** session stored.
- ✅ Your read-only policy store cannot be modified by the agent, and you can prove it.
- ✅ A dream job completes, produces a non-destructive output store with a readable diff, and a session on that output store gives a noticeably richer answer.

> 💡 **Keep yourself honest:** always run a fresh session to test recall. If you keep using the same session, you are testing the conversation, not the memory.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each focused on one skill. They are optional and independent. The **Capstone above is the main build** and already covers all of these, so feel free to skip straight to it.

### Exercise 1: feel the forgetting (foundational)
Create one memory-free session, give it three facts, then start a second session and ask for them back. Write down, in your own words, why nothing transferred.

### Exercise 2: read-only versus read-write (foundational)
Attach the same store to two sessions, one read-write and one read-only. Have the read-write session save a fact. Then have the read-only session try to change it. Record what happens and why this is useful.

### Exercise 3: write a steering prompt (intermediate)
Write a memory prompt for a domain that needs specific details (for example an investment assistant that must always remember risk tolerance and target dates). Run two sessions and check the right details were saved.

### Exercise 4: read a dream diff (intermediate)
Run a dream over five of your sessions. From the diff alone, list everything dreaming did: what it created, enriched, reformatted, and deduplicated. Decide whether each change is an improvement.

### Exercise 5: measure the lift (advanced)
Ask the same question of a session on the raw store and a session on the dreamed output store. Compare answer richness and how the agent navigated memory (wide grep versus index file). Note the token count of the dream job and what fraction was cached.

---

## Cheat sheet

```text
THE PROBLEM
  Sessions are ephemeral islands. No memory carries across runs.

GIVE IT MEMORY
  1. Create a memory store (name + description).
  2. Attach it to a session (--memory-store-id).
  3. Optional: --memory-prompt to steer, --memory-access read_only to protect.
  4. Agent reads first, writes new facts, greps to recall later.

KEEP MEMORY HEALTHY (DREAMING)
  - Async + non-destructive: clones input -> writes to OUTPUT store.
  - Fact-check, enrich, organise, consolidate, deduplicate.
  - Multi-agent: orchestrator + one sub-agent per input session.
  - Review the DIFF, then attach the output store to future sessions.

THREE LAYERS
  session  -> one run, ephemeral
  memory   -> shared file system across sessions
  dreaming -> background cleanup + enrichment over time

REMEMBER
  - Memory is a real file system (bash, grep, file reads).
  - You choose the boundaries (per user / workspace / org).
  - Dreaming is exhaustive on purpose; most tokens are cached (~95%).
```

## How this connects to the rest of the course

- **Earlier, Module 2 · Lesson 3 (The Prompting Playbook):** the generate, evaluate, repair loop there is the same shape as dreaming's multi-agent refinement here.
- **Earlier in Module 5:** the agent, environment, and session concepts this lesson builds directly on top of.
- **Next, Module 5 · Lesson 18 (Memory and Dreaming for Self-Learning Agents):** the same two features seen from the design and production side, including scopes, concurrency control, and real customer results.
- **Later, Module 5 · Lesson 19 (Agent Battle):** putting an agent's configuration (prompt, model, tools, skills) to the test on a concrete task.

---

*Source: "Agents that remember" by Kevin (Anthropic), Code with Claude 2026, London. CLI commands and code snippets are illustrative reconstructions of the steps shown in the talk. Adapt the exact command names and API details to the current Claude Managed Agents tooling.*

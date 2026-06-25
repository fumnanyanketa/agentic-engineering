# Unit 5: Retrieval, Memory and State

> **Course:** Agentic Engineering with Claude, a self-paced path *(working title)*
> **Unit 5 of 11:** Giving an agent the right facts at the right moment, and a durable memory that improves run after run
> **Sources fused:** Agentic Engineering Modules 05-06 (principles) + Building with Claude Lessons 17, 18 and 23 (implementation)
> **Estimated time:** 90 to 120 minutes (read plus the build)

---

## In one sentence

A model only knows what it learned by its training cutoff and only holds a single context window in mind at once, so this unit gives you the two ways out of that box: **retrieval** (fetch the right facts at the right moment and place them in the prompt) and **memory** (a durable store outside the window that survives across runs), plus the loop that turns memory into a learning curve: distilling past runs and team feedback into better instructions over time.

> 🎯 **Where this unit is heading.** The payoff is a **Build**: **Cortex v0**, the shared memory for your AtlasOS fleet. You give an agent (**Scout**) a memory store it reads and writes across separate runs, a retrieval tool over a knowledge base, a background "dreaming" job that distills past runs into cleaner memory, and a feedback loop that learns your team's taste through pull requests. Set it up once and Scout stops starting cold. Jump to **"The Build"** to see the finish line.

## First-principles companion

> 💡 **The durable ideas behind this unit.** The Claude-specific framing is recent; the concepts are not. For the timeless versions:
>
> - **[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)** (paper). The seminal account of combining a model's built-in knowledge with an external, retrievable store, the foundation of retrieval-based long-term memory.
> - **[LLM Powered Autonomous Agents (Lilian Weng)](https://lilianweng.github.io/posts/2023-06-23-agent/)** (essay). Its memory section is the durable articulation of short-term (in-context) versus long-term (external store) memory and retrieval.
> - **[Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442)** (paper). Its memory-stream plus "reflection" architecture (periodically synthesising raw experience into consolidated memories) is the seminal analogue of "dreaming."

## A few plain-language basics first

- **Training cutoff:** the date a model's training data ends. It knows nothing after that, and nothing about your private documents, ever.
- **RAG (Retrieval-Augmented Generation):** before the model answers, you *retrieve* relevant text from your own sources and paste it into the prompt so the model *generates* using it. No retraining.
- **Chunk:** a small passage (a few paragraphs) you split a document into, big enough to stand alone, small enough to be specific.
- **Embedding:** a list of numbers that captures the meaning of a piece of text. Similar meanings get similar numbers. A **vector** is just that list.
- **Context window:** how much text (in tokens) the model holds in mind at once. It is short-term memory, and it runs out.
- **Memory store:** a persistent, file-system-like place an agent reads from and writes to, so knowledge survives after a run ends.
- **Dreaming:** a background job that reviews past run transcripts plus an existing memory store and produces a cleaned-up, enriched copy.

You do not need to memorise these. Each returns the first time it matters.

## Why this unit matters

Units 0 to 4 gave you a capable reasoner, a sharp prompt, the right model, and tools to act with. But the reasoner is still trapped in two ways: it does not know *your* stuff (anything past its training cutoff or private to you), and it forgets everything the moment a run ends. Both limits are about getting the right information in front of the model and keeping it there.

> 🔑 **The two escapes, in one line.** Retrieval brings the right *external facts* into a single run; memory carries the right *learned state* across many runs. Together they turn a stateless reasoner into one that knows your world and gets better the more it works in it.

Get this layer right and your agents stop repeating mistakes, stop re-learning the same facts, and start handing knowledge to each other. Get it wrong and every run is an island that begins cold.

## Learning objectives

By the end of this unit you will be able to:

1. Build a basic RAG pipeline (chunk, embed, store, retrieve top-k) and explain each moving part in plain terms.
2. Improve retrieval with hybrid search (semantic plus BM25, fused with RRF) and a re-ranker, and measure the retriever *separately* from generation.
3. Distinguish short-term memory (the context window) from long-term memory (a durable external store), and manage the window with compaction and a scratchpad.
4. Create a Claude memory store, attach it to sessions with scopes and a steering prompt, and watch an agent read and write across separate runs.
5. Run a "dreaming" job that fact-checks, enriches and deduplicates memory non-destructively, and explain why it runs out of band.
6. Design a low-friction feedback loop that teaches an agent your team's taste through principles and PR-gated self-improvement.

## Prerequisites

- **From this course:** Unit 4 (tools and function calling), because retrieval is best built *as a tool the model calls*. Units 1 to 3 for prompting and context habits.
- **Skills that matter:** reading and running Python, basic file I/O, git and pull requests, and comfort in a terminal.
- **Skills you can defer:** training your own embedding models, the internals of vector indexes. You consume these as components.

---

## Part 1: Retrieval and RAG (the right facts at the right moment)

A model finishes training on a fixed snapshot and learns nothing after that. **RAG** is the standard answer to "the model needs to know *my* stuff": retrieve relevant text from your own sources and paste it in before the model answers. It is cheaper, faster and more current than retraining, and it lets you cite exactly where an answer came from. When a new document appears, it is usable the moment you add it to your store.

The moving parts of a basic pipeline:

- **Chunking.** Split documents into passages. A chunk should be big enough to make sense on its own but small enough to be specific.
- **Embeddings.** A small helper model turns each chunk into a vector (a list of numbers capturing its meaning). Similar meanings land close together even with different words.
- **Vector store.** A database built to find the vectors closest in meaning to a query (FAISS, pgvector, Qdrant are neutral options, not a required platform).
- **Top-k retrieval.** Embed the question, ask the store for the closest chunks, keep the best handful (the "k").
- **Re-ranking.** A slower, more careful model that looks at the question and each candidate chunk together and reorders by true relevance. Run it only on the handful of candidates so it stays cheap.

> ❌ **The most common mistake in RAG:** judging the whole system end to end, concluding "RAG is bad," when the real problem is retrieval. If the right chunk never made it into the prompt, no model can answer well. Measure the retriever by itself: for test questions, check whether the correct chunks appear (roughly **recall**) and how high they rank (roughly **precision**). Most "RAG is bad" complaints are retrieval problems in disguise.

### Why naive search is not enough: hybrid search

Embedding search is great at meaning but weak at exact matches. Search for an error code like `ERR_0x4F2` or a product ID like `SKU-99812` and embeddings often miss, because the meaning of a random code is not captured by numbers. Old-fashioned keyword search handles those perfectly.

The fix is **hybrid search**: run both. Combine **semantic search** (embeddings) with **lexical search** (classic keyword matching, the standard method is **BM25**). BM25 catches the exact strings embeddings fluff; embeddings catch the paraphrases keywords miss. To merge the two ranked lists, the sane default is **Reciprocal Rank Fusion (RRF)**, which combines results by their *positions* in each list rather than raw scores (sidestepping the headache that BM25 and embedding scores live on different scales).

> ✅ **The robust default stack.** Gather a broad candidate set with hybrid search plus RRF, run a re-ranker on the top results, then hand the best few to the model. Practitioners report hybrid search is often the single biggest jump in retrieval quality, and re-ranking on top of it is a large, cheap gain.

### Retrieval is just a tool

"Context windows keep getting bigger, so can I skip retrieval and paste everything in?" Mostly no. The data you might want to search grows far faster than windows do, and pasting too much hurts quality and cost (Part 2). The clean way to see retrieval, building straight on Unit 4, is that **retrieval is just a tool the model can call**. Give the model a `search_docs` tool and let it pull information when it decides it needs to. This is **agentic** or **just-in-time** retrieval, and a useful pattern is **progressive disclosure**: the agent holds lightweight pointers (file paths, links, short queries) and fetches full text only at the moment it is needed.

---

## Part 2: Memory versus the context window

Recall from Unit 0 that the **context window** is the model's short-term working memory: the largest amount of text it can look at in one request. For a quick chat that is plenty. But an agent calling tools, reading files and trying things over hundreds of steps produces far more text than any window holds. When it fills up, older content is dropped, and a naive agent simply forgets what it was doing.

> 🔑 **Separate two kinds of memory.** **Short-term memory** is the live context window: the current conversation and working facts, fast but small and temporary. **Long-term memory** is information saved *outside* the window in durable storage (a file or database) so it survives after the window is cleared. A bigger window is *not* the same as long-term memory: it is still short-term, still finite, and still wiped between sessions. Long-horizon coherence comes from how you manage memory, not from window size.

Three techniques keep an agent coherent across a window that is too small:

- **Compaction: summarise and restart.** As the conversation nears the limit, pause, ask the model to summarise what happened (decisions made, current goal, open problems, key facts), then start a fresh window seeded with that summary instead of the full history. Like clearing a cluttered desk onto one clean page and binning the rest.
- **Structured note-taking: an external scratchpad.** Let the agent keep notes in a file outside the window, a scratchpad it reads and writes at any time: progress, intermediate results, a running checklist. It reloads those notes after a compaction or in a later session. This is how long-running agent demos stay on track across thousands of steps and many resets.
- **Sub-agent isolation.** Hand a big self-contained sub-task to a separate sub-agent in its own clean window. It does the messy work in isolation and returns only a short, distilled summary (often one or two thousand tokens). The main window stays uncluttered because the mess lived and died elsewhere.

> 💡 **Treat context as a budget.** Every token spent is a token unavailable for reasoning. Keep a mental ledger of what is in the window and why. Research that makes this explicit finds agents which neither over-compress (erasing critical evidence) nor under-compress (overflowing the limit) perform best. Persist what is worth keeping, drop the noise, isolate large sub-tasks.

Many frameworks now offer compaction, sessions and sub-agents built in, so you will not always hand-write this in production. Even so, build a manual compaction loop and a manual scratchpad *once* yourself. Understanding what the framework does under the hood is what lets you debug it when it misbehaves.

---

## Part 3: Durable memory the Claude way (stores, scopes, dreaming)

The principle layer says "save state outside the window." The Claude platform makes that a first-class primitive: a **memory store** is a persistent, file-system-like store you attach as a resource to the sessions you create, so agents read and write across runs.

Two design choices make it powerful:

- **It is mounted as a real file system.** The store appears to the model as ordinary files and folders, so the model uses tools it already knows: **bash** to explore, **grep** to find keywords, plain file reads. The design principle, the same one behind skills, is to **"let it cook"**: get out of the model's way and let it use the strong file-system skills it already has, rather than inventing a new interface.
- **You decide the boundaries.** Create as many stores as you like and scope them however you want: one per user, one per workspace, one per organisation.

Attaching a store to a session, with two parameters worth knowing:

```bash
cma sessions create \
  --agent-id "$AGENT_ID" \
  --environment-id "$ENV_ID" \
  --memory-store-id "$MEMORY_STORE_ID" \
  --memory-prompt "Save key facts, links, and follow-ups for future sessions." \
  --memory-access "read_write"
```

A **memory prompt** steers what the agent reads and writes (for example "always remember risk tolerance and target dates"). **Access** defaults to `read_write`; set `read_only` when a store should be a stable source of truth a session must not edit.

> ✅ **Let it read before it writes.** A well-behaved memory agent checks the store first ("do I already know this?") before answering or saving. The shared store is what lets a swarm of agents build on each other's work instead of starting cold.

### Multi-agent memory needs real structure

A single agent with a file system is the easy case. Production means many agents in the same environment at once, which raises requirements:

- **Scopes form a hierarchy.** A stable, **read-only** org-wide layer everyone reads (policies, runbooks) plus narrower **read-write** stores agents freely update. That hierarchy is what lets memory scale.
- **Optimistic concurrency control.** When several agents write at once, one could overwrite another (**clobbering**). The system assumes conflicts are rare and detects them at write time, so an agent does not silently destroy another's update, while keeping everyone productive.
- **Versioning, attribution, and a standalone API.** Version control gives an audit trail you can **diff**; attribution shows which agent wrote what; a standalone CRUD API (plus exports and redactions) lets teams manage memory from outside the agent loop.

### Dreaming: keeping memory healthy as it grows

Memory solves one problem and creates another. Agents writing notes as they work is **locally optimal** but **globally messy**: they dump information, repeat the same mistakes independently, and leave duplicates and stale facts. A single agent cannot see patterns spread across many sessions.

> 🔑 **Dreaming is the global feedback loop.** A **dream** is an **asynchronous**, **out-of-band** batch job (it runs in the background, decoupled from the agent loop) that reads an input memory store plus a batch of past session transcripts and produces a verified, better-organised snapshot. It **fact-checks**, **enriches** (dates, identifiers, links), and **organises, consolidates and deduplicates** so the store does not grow unbounded.

```bash
cma dreams create \
  --model "claude-opus-4-7" \
  --memory-store-id "$INPUT_MEMORY_STORE_ID" \
  --session-ids "$SESSION_1,$SESSION_2,...,$SESSION_N" \
  --instructions "Backfill exact dates and identifiers. Keep a clear index."
```

Three things make dreaming work in practice:

- **It is non-destructive.** It never touches your input store. It **clones** the input into a separate **output store** and writes there, so every edit is safe. You attach the output to future sessions when happy, then retire the old store.
- **It is multi-agent and exhaustive by design.** An **orchestrator** spawns one **sub-agent per input session** so nothing is missed, with the same observability as the rest of the platform. Dreaming is itself built on Claude Managed Agents: a feature for managed agents, built on managed agents.
- **It is test-time compute for memory.** Just as a thinking model spends extra tokens to get a better answer, dreaming spends work up front to curate higher-quality memory, and every downstream agent benefits. Because most of the work reuses the same context, most tokens are **cached** (roughly a 95% cache hit rate).

The payoff is concrete: partner teams reported large gains after adding memory and dreaming (one team saw a 97% drop in first-pass errors; another a six-times increase in completion rates on a benchmark after adding dreaming). Out of band matters because it works across cross-agent transcripts a single agent cannot see, keeps clean objectives (no trade-off between task quality and memory quality), and adds no latency on the hot path.

---

## Part 4: Learning from your team (principles, not rules)

Dreaming distills runs into better memory automatically. But some learning needs a *human's* taste, and for **fuzzy** tasks (writing a good reply, triaging by judgment) there is no quick pass/fail check. The usual way agents improve, a loop that keeps iterating against an external check (a test suite, a browser), does not fit: the real feedback is slow and complex. You inject judgment another way.

> 🔑 **Switch from rules to principles.** Rules ("if X happens, do Y") sound robotic and shatter the moment something new appears. Principles tell the agent *how to reason*, so it handles new situations gracefully. The reframe: how would you explain this to a new teammate? Not a checklist, but how to *think*. Switching often shrinks the instruction file (one team's dropped to a fifth of its length) *and* improves the output.

> ❌ **The agent's bad instinct.** Given feedback, an agent will write hyper-specific rules ("if a user has problem X, never mention pricing in the first line"). It works for that one case and generalises to nothing. The fix is to **teach the agent how to learn**: a skill that tells it to compare its output to the ideal, look at its current instructions, find the gap, and adjust a *principle*, never append a one-off rule.

The third piece is the loop itself, and the hardest part of a feedback loop is the humans: if it takes extra effort or breaks their normal process, they will not do it. Design for the **smallest team input for the biggest agent output**, reusing what people already do:

```text
1. Agent monitors a stream and posts to a channel the team already watches:
   "Item X. Suggested action: REPLY / LIKE / SKIP. Reasoning: ... Draft: ..."
2. The team adds an EMOJI REACTION for what they actually did, maybe a NOTE.
3. Daily, the agent compares what it SUGGESTED vs what the team DID, draws takeaways.
4. It opens a PULL REQUEST adjusting the relevant PRINCIPLE, with a short explanation.
5. A human does a ~60-second PR review and merges if it looks good.
```

> ✅ **Route self-improvement through pull requests.** Because the instructions live in a git repo, daily learning arrives as a reviewable PR (a few English-line changes with context). The PR gate keeps humans in control so the agent does not "change its instructions willy-nilly" and drift into a weird direction it keeps doubling down on. Giving the agent a name and a little personality also gets people to engage and give better feedback.

> 💡 **The one thing to remember.** Design the **feedback loop**, not the perfect prompt. A "just good" prompt plus a great loop beats a perfect prompt with no loop, because the loop is what lets the agent keep improving as situations change.

---

## Key takeaways

1. **Retrieval brings external facts into a run; memory carries learned state across runs.** Two escapes from a stateless model.
2. **Measure the retriever separately.** Most "RAG is bad" failures are retrieval failures. Hybrid search plus RRF plus a re-ranker is the robust default.
3. **A bigger window is not memory.** Manage the window as a budget with compaction, a scratchpad, and sub-agent isolation; persist what matters outside it.
4. **Memory is a real file system.** Let the model use bash, grep and file reads. You set the scopes (read-only org layer, read-write task stores).
5. **Dreaming makes memory globally optimal.** A non-destructive, out-of-band, multi-agent job that fact-checks, enriches and deduplicates. Test-time compute for memory.
6. **For fuzzy tasks, design the loop.** Principles over rules, teach the agent to learn, smallest human input, PR-gated self-improvement.

## Common pitfalls

- ❌ Only ever testing the full RAG system end to end and never isolating the retriever.
- ❌ Relying on embeddings alone for exact codes, IDs and names (use hybrid search).
- ❌ Confusing a long context window with true long-horizon memory.
- ❌ Letting message history grow until the window overflows; or over-compressing and erasing the one detail you later need.
- ❌ Expecting an agent to "just remember" without attaching a memory store, or letting a store grow forever with no dreaming.
- ❌ Giving every session read-write access to an org-wide store that should be read-only, or ignoring concurrency so parallel agents clobber each other.
- ❌ Trying to perfect the initial prompt instead of designing how the agent improves; letting it learn by appending brittle one-off rules.

---

## 🛠️ The Build: Cortex memory

> The hands-on payoff. This fuses the RAG lab, the memory-and-dreaming lessons, and the learn-from-your-team loop into **Cortex v0**, the shared memory for AtlasOS. You give **Scout** (your research agent) durable memory and the ability to improve across runs, all committed to your repo under `memory/`.

### What you will build

**Cortex v0**: a knowledge store Scout retrieves over, a memory store it reads and writes across separate runs, a dreaming job that distills past runs into cleaner memory non-destructively, and a PR-gated feedback loop that teaches Scout your team's standards. Proven by a before/after pair (forgetting versus recall) and a measurable retrieval and memory lift.

### Milestones (in order, each stands alone)

1. **Retrieval over a knowledge base.** Build a small RAG pipeline over a corpus Scout should know (your notes, project docs). Start with naive top-k vector search and measure retrieval quality on a handful of test questions. Then add BM25 plus RRF hybrid search and a re-ranker, and record the improvement in numbers. Expose it as a `search_docs` tool Scout calls on demand.
2. **Prove the base case.** Run Scout with no memory: tell it a fact in one session, ask a *fresh* session about it, confirm it forgot. Save both transcripts as your "before" proof. (Always test recall in a new session, or you are testing the conversation, not the memory.)
3. **Give Scout memory.** Create a memory store (`cortex-memory`), attach it with a steering memory prompt and `read_write` access. Tell it a fact, watch it write to a file; open a new session on the same store and confirm it greps the fact back. This is the heart of Cortex.
4. **Scopes and audit.** Add a second **read-only** store for stable org knowledge (Atlas charter, conventions) and attach both, proving Scout can read policy but not edit it. Make a couple of edits and use version history to diff and attribute them.
5. **Dream.** Run several Scout sessions to fill memory, then launch a dream over those transcripts with instructions ("backfill exact dates, build an index"). Watch the live token count, open the dream's own session to see its sub-agents, read the diff (index file, enriched facts), then run a fresh session on the output store and confirm it answers faster and richer.
6. **Stretch: learn from the team.** Have Scout post suggestions where you already look, signal the action you actually took with a one-word tag or reaction, and on a schedule open a **pull request** that adjusts a *principle* (not a brittle rule) in its instructions. Confirm it edits the right place and a ~60-second review merges it.

### How you will know you are done

- ✅ Retrieval precision measurably improved after adding hybrid search and re-ranking, and `search_docs` is a tool Scout calls.
- ✅ A before/after pair of transcripts shows forgetting, then recall, with a fresh session answering from what an earlier session stored.
- ✅ Your read-only store cannot be modified by Scout, and you can diff and attribute changes to the task store.
- ✅ A dream completes, produces a non-destructive output store with a readable diff, and a session on it gives a noticeably richer answer.
- ✅ (Stretch) Scout's self-improvement arrives as a PR that edits a principle in the right place, reviewed and merged in about a minute.
- ✅ Cortex v0 is committed under `memory/` in your AtlasOS repo.

---

## Cheat sheet

```text
RETRIEVAL (the right facts at the right moment)
  chunk -> embed -> vector store -> top-k -> re-rank -> paste into prompt
  hybrid = semantic (embeddings) + lexical (BM25), fused with RRF
  measure the RETRIEVER separately (recall/precision); most "RAG is bad" = retrieval
  retrieval is just a TOOL the model calls (just-in-time, progressive disclosure)

CONTEXT AS A BUDGET (short-term memory)
  context window = short-term, finite, wiped between sessions
  compaction (summarise + restart) · scratchpad file · sub-agent isolation
  don't over-compress (lose evidence) or under-compress (overflow)

DURABLE MEMORY (long-term, the Claude way)
  memory store = real file system (bash, grep, file reads). "Let it cook."
  scopes: read-only org layer + read-write task stores -> hierarchy
  optimistic concurrency (no clobbering) · versioning + attribution + API

DREAMING (test-time compute for memory)
  async, OUT OF BAND, non-destructive: clones input -> writes OUTPUT store
  fact-check · enrich · organise · consolidate · deduplicate
  multi-agent: orchestrator + one sub-agent per session; ~95% cached
  makes memory GLOBALLY optimal; review the DIFF, then attach output

LEARN FROM YOUR TEAM (fuzzy tasks, no external check)
  principles, NOT rules (how to think; shrinks file, improves output)
  teach it to learn: output vs ideal vs instructions -> adjust a PRINCIPLE
  smallest human input (emoji/tag) -> PR-gated self-improvement (no drift)
  design the LOOP, not the perfect prompt
```

## How this connects to the rest of the course

- **Builds on Unit 4 (tools and MCP):** retrieval and memory are both exposed as tools the model calls, and memory naturally connects to MCP as a data source.
- **Next, Unit 6 (workflows and agent patterns):** the compaction, scratchpad and sub-agent-isolation techniques here become first-class moves in the workflow and orchestration patterns you assemble next, and dreaming's orchestrator-plus-sub-agents shape previews multi-agent work in Unit 7.
- **Toward the north-star:** Cortex v0 is the shared memory of AtlasOS. Every later agent (Forge, Pulse, Herald, Warden) reads and writes through it, and the dreaming loop is what lets the fleet "dream" overnight and improve itself.

---

*Unit 5 of the combined path. Fuses the vendor-neutral principles of Agentic Engineering Modules 05-06 with the Claude-specific implementation of Building with Claude Lessons 17, 18 and 23. CLI commands are illustrative reconstructions; adapt model ids and SDK details to the current docs.*

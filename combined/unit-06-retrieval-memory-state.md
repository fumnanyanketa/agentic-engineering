# Unit 6: Retrieval, Memory and State

> **Course:** Agentic Engineering, a model-agnostic self-paced path *(working title)*
> **Unit 6 of 12:** Give an agent fresh, private knowledge it can fetch on demand (retrieval and RAG), then give it a memory that survives across runs and a loop that distills past runs into better instructions
> **The how, across models:** embeddings and vector search are provider-neutral; Claude (Anthropic), Gemini (Google), and GPT (OpenAI) all offer embeddings and memory features, and vector stores are independent of model choice; current practice verified June 2026
> **AtlasOS build:** `memory/`, the shared memory called **Cortex**, plus a minimal "dreaming" step
> **Estimated time:** 2 to 3 hours

---

## In one sentence

A model only knows what it learned during training and forgets everything the moment a run ends, so this unit teaches the two fixes that change that: **retrieval** (fetch the right private or fresh text and paste it into the prompt, so the model can answer from knowledge it was never trained on) and **memory** (write what matters to durable storage outside the context window, so an agent remembers across runs and can even distill its own past into better instructions).

> 🎯 **Where this unit is heading.** The payoff is a **Build** that gives the Scout agent (the researcher you built tools for in Unit 5) a real memory. You will create the `memory/` folder, give Scout a simple persistent store it reads at the start of every run and appends to at the end, and prove it remembers across two separate runs. Then you will sketch a minimal "dreaming" step: a small background pass that reads Scout's recent runs and distills them into one improved instruction. This is **Cortex v0**, the shared memory of AtlasOS. Jump to **"The Build"** to see the finish line, then come back.

## First-principles companion

> 💡 **The durable ideas behind this unit.** The tools are recent and change often; the craft does not. If you want the timeless versions (optional, read them any time):
>
> - **[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)** (paper). The seminal paper on combining a model's built-in knowledge with an external, retrievable store. The foundation of RAG.
> - **[LLM Powered Autonomous Agents (Lilian Weng)](https://lilianweng.github.io/posts/2023-06-23-agent/)** (essay). Its memory section is the durable articulation of short-term (in-context) versus long-term (external store) memory and retrieval.
> - **[Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442)** (paper). Its memory-stream plus "reflection" architecture (periodically synthesizing raw experiences into consolidated memories) is the seminal analogue of "dreaming."
> - **[Effective context engineering for AI agents (Anthropic)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)** (essay). Just-in-time retrieval, compaction, and the external scratchpad, the practical patterns behind this unit.

## A few plain-language basics first

New terms, in plain words. You do not need to memorise these; each is explained again the moment it matters.

- **Training cutoff:** the date a model's training data ends. The model knows nothing that happened after it, and it never saw your private documents at all.
- **Retrieval:** fetching relevant pieces of text from your own sources at the moment a question comes in, so you can place them into the prompt.
- **RAG (Retrieval-Augmented Generation):** the pattern where you *retrieve* relevant text first and the model *generates* its answer using that text. No retraining required.
- **Embedding:** a list of numbers that captures the *meaning* of a piece of text. Texts with similar meaning get similar numbers, even when they use different words.
- **Vector:** that list of numbers. A **vector store** (or vector database) is a database built to find the vectors closest in meaning to a query.
- **Chunk:** one passage of a document, a few paragraphs, big enough to make sense alone but small enough to be specific. You split documents into chunks before embedding them.
- **Context window:** the model's short-term working memory, the largest amount of text (counted in **tokens**, the small chunks of text models read) it can look at in one request. It is finite and it gets wiped between runs.
- **Short-term vs long-term memory:** short-term is the live context window. Long-term is information saved *outside* the window in a file or database, so it survives after the window is cleared.
- **Session / run:** one execution of an agent, usually one task or conversation. By default a run is **ephemeral**: it disappears when it ends and remembers nothing.
- **Dreaming:** a background pass that reviews past runs and an existing memory store, then produces a cleaned-up, enriched, better-organised version of that memory.

## Why this unit matters

So far your agent can plan, act, verify (Unit 1), be prompted well (Unit 3), pick its model and effort (Unit 4), and call tools (Unit 5). But it is still an amnesiac that only knows what it was trained on. Two limits remain, and both are about *knowledge over time*: it cannot see your private or fresh data, and it forgets everything between runs. Retrieval fixes the first. Memory fixes the second.

> 🔑 **Fresh knowledge comes from retrieval, not retraining.** When the model needs *your* stuff or *today's* facts, you do not retrain it. You fetch the right text and put it in the prompt. And when it needs to remember across runs, you do not rely on a bigger window; you write to durable storage. Both are context engineering, not model surgery.

## Learning objectives

By the end of this unit you will be able to:

1. Explain RAG in plain terms and name the moving parts: chunking, embeddings, a vector store, top-k retrieval, and re-ranking.
2. Explain embeddings and vector search without jargon, and know that Claude, Gemini, and OpenAI all provide embeddings while the vector store stays independent of model choice.
3. Use hybrid search (semantic plus keyword) and measure the retriever by itself, because most "RAG is bad" complaints are retrieval problems in disguise.
4. Tell short-term from long-term memory, and use compaction and an external scratchpad to keep an agent coherent past a single window.
5. Give an agent a persistent memory store it reads at the start and appends to at the end, and sketch a "dreaming" loop that distills past runs into better instructions.

## Prerequisites

- Units 1 to 5 finished: a working agent, the `atlasos` repo, and the Scout agent with its tool layer in `atlas/tools/` (Unit 5).
- Comfort running commands in a terminal and editing files in your editor.
- No machine-learning background needed. Every concept is built up from plain words.

---

## Part 1: Why a model needs retrieval at all

A model finishes training on a fixed snapshot of text and learns nothing after that. It does not know your company's internal wiki, your customer records, your meeting notes, or anything that happened after its training cutoff. Ask it about those and it will either say it does not know or, worse, confidently make something up.

There are only a few ways to give a model knowledge it does not have, and most are bad:

- **Retrain or fine-tune it on your data.** Expensive, slow, and out of date the moment a new document appears. Overkill for "the model needs to know my stuff."
- **Paste everything into the prompt every time.** Works for a handful of pages, but your data is almost always far bigger than the context window, and stuffing in too much hurts quality and cost (more in Part 6).
- **Retrieve only what is relevant, right when you need it.** This is RAG, and it is the standard answer.

**RAG** stands for **Retrieval-Augmented Generation**. Before the model answers, you *retrieve* the most relevant pieces of text from your own sources and paste them into the prompt, so the model can *generate* its answer grounded in those pieces. No retraining. When a new document appears, it is usable the moment you add it to your store, and you can cite exactly where each answer came from.

```text
   QUESTION ──▶ [ retrieve relevant chunks ] ──▶ paste into prompt ──▶ MODEL ──▶ ANSWER
                         ▲                                                         │
                         └──────── your documents (wiki, notes, records) ─────────┘
```

> 🔑 **RAG is grounding, not memorising.** You are not teaching the model new facts permanently. You are handing it the right page, open to the right paragraph, at the moment it answers. Change the page, and the answer changes, with no retraining.

---

## Part 2: The moving parts (embeddings and vector search, explained plainly)

A basic RAG pipeline is a small number of pieces. Here is each one in plain terms.

- **Chunking.** You cannot store whole books as single units, so you split documents into smaller passages called **chunks**, perhaps a few paragraphs each. A chunk should be big enough to stand on its own but small enough to be specific.
- **Embeddings.** An **embedding** is a list of numbers that captures the *meaning* of a piece of text. A small helper model (an *embedding model*) turns each chunk into one of these number lists. The magic property: texts that mean similar things get similar numbers, even if they share no words. "How do I reset my password?" and "I forgot my login credentials" land close together.
- **Vector store.** A **vector** is just that list of numbers. A **vector store** (or vector database) is a database built to find the vectors closest in meaning to a query, fast, even across millions of chunks. Neutral examples you might encounter: FAISS, pgvector, Qdrant, Chroma. These are options, not a required platform.
- **Top-k retrieval.** When a question comes in, you embed the question into a vector too, ask the store for the closest chunks, and keep the best handful. The "k" is just how many you keep, so "top-k" means "the top k closest chunks," for example the top 5.
- **Re-ranking.** The first search is fast but rough. A **re-ranker** is a more careful (and slower) model that looks at the question and each candidate chunk *together* and reorders them by true relevance. You run it only on the handful of candidates, so it stays affordable.

So the naive pipeline is: chunk your docs, embed them, store them. Then at query time, embed the question, fetch the top-k chunks, paste them into the prompt, and let the model answer.

**Where the embeddings come from is your choice, and it is decoupled from your main model.** All three major providers offer embedding models you call exactly like any other API: send text, get back a vector.

| | **Claude / Anthropic** | **Gemini / Google** | **GPT / OpenAI** |
|---|---|---|---|
| Embeddings available | yes (Anthropic points to embedding options such as the Voyage AI models it acquired) | yes (Gemini embedding models via the API / AI Studio) | yes (OpenAI text-embedding models) |
| You send / get back | text in, a vector out | text in, a vector out | text in, a vector out |
| Vector store | your choice, independent of the model | your choice, independent of the model | your choice, independent of the model |

> 🔑 **The vector store does not care which model you use.** Embeddings are just numbers. You can embed with one provider, generate answers with another, and store the vectors in any database. Pick the embedding model for quality and price; pick the answer model separately. Hold exact model ids loosely and verify names against current docs, because they change.

> 💡 **One rule about mixing embeddings.** All chunks in a store, and your query, must be embedded by the *same* model. Different embedding models produce numbers on different scales, so their vectors are not comparable. If you switch embedding models, you re-embed everything.

---

> 💡 **A little math intuition (optional).** An embedding is just a list of numbers (a vector), maybe a few hundred of them, that places a piece of text as a point in space, with similar meanings landing near each other. "Similarity" is usually **cosine similarity**: picture each text as an arrow from the origin; two arrows pointing in nearly the same direction (a small angle between them) are similar, even if one is longer. Search becomes "find the arrows pointing most nearly the same way as my question." The database does the arithmetic; holding the picture, points in space, nearness as meaning, angle as similarity, is enough to reason about why retrieval returns what it does, and why a weak embedding model gives bad neighbours.

## Part 3: Naive search is not enough (hybrid search and re-ranking)

Embedding search is great at meaning but weak at exact matches. If a user searches for an error code like `ERR_0x4F2` or a product ID like `SKU-99812`, embeddings often miss it, because the meaning of a random code is not captured well by numbers. The old-fashioned keyword approach handles those perfectly.

The fix is **hybrid search**: run both at once.

- **Semantic search** is the embedding-based search from Part 2. It catches paraphrases and meaning.
- **Lexical search** is classic keyword matching. The standard method is **BM25** (Best Match 25, a well-established formula that scores how well a document's exact words match the query). It catches the exact strings that embeddings fluff.

BM25 catches the codes and names that embeddings miss; embeddings catch the paraphrases that keywords miss. Practitioners report that adding hybrid search is often the single biggest jump in retrieval quality.

To merge two ranked lists into one, the sane default is **Reciprocal Rank Fusion (RRF)**, a simple method that combines results by their *positions* in each list rather than their raw scores. This sidesteps the headache that BM25 scores and embedding scores live on totally different scales. A robust, common setup: gather a broad set of candidates with hybrid search plus RRF, then run a re-ranker on the top results before handing the best few to the model.

```text
QUESTION
   ├─▶ semantic (embeddings) ─┐
   │                          ├─▶ RRF merge ─▶ re-ranker ─▶ top few ─▶ MODEL
   └─▶ lexical (BM25 keyword) ┘
```

> ✅ **Sensible defaults.** Use hybrid search (semantic plus BM25) fused with RRF, add a re-ranker on the top candidates for a cheap quality boost, and chunk thoughtfully so each passage stands on its own. You rarely need anything fancier to start.

---

## Part 4: Retrieval is just a tool the model can call

Here is the idea that ties Unit 5 to this one. You do not have to stuff documents into the prompt up front. Instead, **retrieval can be a tool the model calls**, exactly like the tools you built in Unit 5. You give the model a `search_docs` tool, and it pulls information *when it decides it needs to*.

This is sometimes called **just-in-time** or **agentic retrieval**, and it has a real advantage: the agent holds lightweight pointers (file paths, links, short queries) and fetches the full text only at the moment it is needed. Anthropic calls this **progressive disclosure**. It keeps the context window clean and lets the model decide what is worth reading.

Recall the end of Unit 5: Scout already has a small `lookup_source` tool. That is the seed. Turn it into a proper retrieval tool, hybrid search behind a clean schema, and Scout can search a growing body of documents on demand without you pre-loading anything.

Building retrieval as a tool also sets you up neatly for the **Model Context Protocol (MCP)** you met in Unit 5: you can wrap your retrieval tool as an MCP server so any agent in the fleet reuses it.

> 🔑 **"RAG vs agents" is a false choice.** Retrieval is one of the tools an agent calls. The agent decides when to search, what to search for, and whether to search again. That is just the tool-use loop from Unit 5, pointed at your knowledge.

---

## Part 5: Measure the retriever by itself

The most common mistake in RAG is judging the whole system end to end, getting a bad answer, and concluding "RAG is bad," when the real problem is that the right chunk never made it into the prompt. If retrieval failed, no model can save the answer.

So measure the retriever *separately* from the model that writes the answer. For a set of test questions where you know the correct source:

- **Recall:** did the correct chunk appear in the results at all? (If not, retrieval failed before the model even saw the question.)
- **Precision:** how high did the correct chunk rank, and how much junk came with it?

Only once retrieval is solid should you worry about the generation step. Build a small test set of question-to-correct-source pairs, run your retriever, and read the numbers before and after each change (adding BM25, adding a re-ranker). This is how you tell a real improvement from a vibe.

> 🔑 **Most "RAG is bad" complaints are retrieval problems in disguise.** What is dying is *naive single-vector top-k* search, not retrieval itself. Measure the retriever alone and you will usually find the fix is in the search, not the model.

---

## Part 6: Short-term vs long-term memory, and surviving a long task

Now switch from "knowledge the model never had" to "knowledge from earlier in *this* work that the agent must not forget." This is memory, and it starts with one distinction beginners often blur.

- **Short-term memory** is the live context window: the current conversation and the working facts the agent is using right now. Fast, but small and temporary. When it fills up, older content gets dropped and a naive agent simply forgets what it was doing.
- **Long-term memory** is information saved *outside* the window in durable storage (a file or a database), so it survives even after the window is cleared or the run ends.

A crucial point: **a bigger context window is not the same as long-term memory.** A larger window is still short-term, still finite, and still wiped between runs. Long-horizon coherence comes from how you manage memory, not from window size.

Two techniques keep an agent coherent past a single window:

- **Compaction: summarize and restart.** As the conversation nears the window limit, you pause, ask the model to summarize what has happened (decisions made, current goal, open problems, key facts), then start a fresh window seeded with that summary instead of the full history. Like clearing a cluttered desk: write the important notes on one clean page, bin the rest, keep working. The danger is summarizing away the one detail you later need, so be deliberate about what the summary must always preserve.
- **Structured note-taking: an external scratchpad.** Let the agent keep notes in a file outside the window, a scratchpad it reads and writes at any time. It records progress, intermediate results, and a running checklist, then reloads those notes after a compaction or in a later session. This is exactly how long-running agent demos stay on track across thousands of steps and many context resets.

> 🔑 **Treat the context window as a budget.** Every token spent is a token unavailable for actual reasoning. Persist what is worth keeping to long-term memory, drop the noise, and isolate large sub-tasks. Agents that neither over-compress (erasing critical evidence) nor under-compress (overflowing the limit) perform best.

> 💡 **Build it by hand once.** Many frameworks now offer sessions, memory, and compaction built in, and all three providers expose memory and file features at a high level (Claude offers file-based memory and a memory tool; Gemini and OpenAI offer their own session, file, and memory features, verify the current shape against their docs). Even so, write a manual scratchpad and a manual compaction loop yourself once. Understanding what the framework does under the hood is what lets you debug it when it misbehaves.

---

## Part 7: Memory across runs, and the "dreaming" self-improvement loop

The scratchpad in Part 6 keeps one long run coherent. The next step is memory that survives *between* runs entirely, so an agent (or a whole team of agents) gets *better* from one task to the next instead of starting cold every time.

The clean design, the one used in production systems, is to **model memory as a plain file system**. A **memory store** is a persistent, file-like place the agent reads from at the start of a run and writes to at the end. Because it looks like ordinary files and folders, the model uses skills it already has: read a file, search it for a keyword, append a note. No exotic interface required.

A well-behaved memory agent **reads before it writes**: it checks the store first ("do I already know this?"), then answers, then saves anything new. Run two separate sessions against the same store and knowledge now moves between them: session one writes a fact, session two reads it back. That single behaviour, persist at the end and load at the start, is the whole heart of cross-run memory.

But memory creates a new problem. As agents read and write over time, they start dumping information. The store grows without limit, accumulates duplicates, and goes **stale** (out of date). Worse, across many runs, agents repeat the same mistakes and each learns the same lesson independently. A single agent in the moment cannot see the patterns spread across all its past runs.

This is what **dreaming** is for. Dreaming is a small **background pass** (it runs separately from live work, never on the hot path) that reads recent run transcripts plus the existing memory, then produces a cleaned-up, improved version. In a full system a dream will fact-check, enrich, deduplicate, and reorganise. For your first version, the essential move is the most valuable one: **read the recent runs and distill them into one or two better instructions for next time.**

```text
   runs write notes ──▶ MEMORY STORE ──▶ dreaming reads recent runs
        ▲                                        │
        │                                        ▼
        └────────── better instructions ◀── distill: "what should
                    fed into the next run        next time do differently?"
```

The teams who built this report it is the difference between a flat line and a learning curve: memory raises the floor for every run, and dreaming raises it higher by reconciling lessons across runs that no single run could see. A useful mental model: **dreaming is "test-time compute" for memory.** You spend a little work up front, off to the side, to curate higher-quality instructions, and every future run benefits.

> 🔑 **Memory turns a flat line into a learning curve.** Without it every run is independent and quality plateaus. With it, each run stands on the shoulders of the last. Dreaming is what keeps that memory from rotting as it grows.

---

## Part 8: Learning a team's standards (principles, not rules)

There is one more kind of learning, and it matters most for *fuzzy* tasks where there is no quick pass/fail check. A coding task has a test suite that says "yes, it works." But "is this a good reply to a customer?" or "does this match how our team writes?" has no unit test. The real signal (how people react) is slow and complex. So how does an agent learn taste?

The hard-won answer from teams who have shipped this:

- **Write instructions as principles, not rules.** A rule says "if X, do Y." It sounds robotic and shatters the moment something new appears. A principle says *how to think* ("don't pitch a feature to someone who is venting about the product; be a builder, not a support queue"). Principles generalise to situations they never anticipated. Surprisingly, switching from rules to principles often makes the instruction file *shorter* and the output *better*.
- **Teach the agent how to learn, not just what to do.** When you give feedback, the agent's instinct is to bolt on a hyper-specific rule ("never mention pricing in the first line for problem X"). That fixes one case and generalises to nothing. Instead, teach it to compare its output to the ideal, look at its current principles, find the gap, and adjust a *principle*, in the right place, so it would produce the ideal next time.
- **Design the feedback loop for the humans.** The hardest part of any feedback loop is getting people to feed it. Ask for the *smallest* input for the biggest gain: learn from what the team already does (an emoji reaction, a one-word tag, a short note in a channel they already watch). Reuse existing behaviour rather than adding a chore.
- **Route self-improvement through a human gate.** Keep the instruction files in git. Have the agent open a **pull request** that adjusts the relevant principle, with a short explanation, that a human reviews in about a minute and merges. The gate keeps the agent from rewriting its own instructions willy-nilly and drifting in a weird direction.

> 🔑 **Design the feedback loop, not the perfect prompt.** A "just good" prompt plus a great loop beats a perfect prompt with no loop. The loop is what lets the agent keep improving as situations change and your understanding of the problem evolves. This is the same shape as dreaming in Part 7: watch what happened, distill a better *principle*, apply it next time, with a human in control.

---

## Key takeaways

1. **A model knows only its training data.** Retrieval fixes that by fetching relevant private or fresh text into the prompt at query time. No retraining.
2. **Embeddings turn meaning into numbers; a vector store finds the closest ones.** All three providers offer embeddings, and the vector store is independent of your answer model.
3. **Naive top-k is not enough.** Use hybrid search (semantic plus BM25, fused with RRF) and a re-ranker, and measure the retriever by itself.
4. **Short-term memory is the window; long-term memory is durable storage.** A bigger window is not memory. Use compaction and an external scratchpad to survive long tasks.
5. **Cross-run memory is read-at-start, write-at-end on a file-like store.** Dreaming is a background pass that distills past runs into better instructions so memory does not rot.
6. **For fuzzy tasks, learn with principles, a learn-how-to-learn step, a low-friction feedback loop, and a human PR gate.**

## Common pitfalls

- ❌ Believing "RAG is dead." What is dying is naive single-vector top-k search, not retrieval itself.
- ❌ Only ever testing the full system and never isolating the retriever, then blaming the model.
- ❌ Relying on embeddings alone for exact codes, IDs, and names (use hybrid search).
- ❌ Mixing embedding models in one store, or embedding the query with a different model than the chunks.
- ❌ Confusing a long context window with true long-horizon memory.
- ❌ Letting a memory store grow forever with no dreaming, so it fills with duplicates and stale notes.
- ❌ Teaching a fuzzy-task agent with brittle if-X-then-Y rules, or letting it rewrite its own instructions with no human review (drift).

---

## 🛠️ The Build: Cortex v0, give Scout a memory that survives across runs

> The hands-on payoff. Scout (your researcher from Unit 5) currently forgets everything between runs. You will give it a simple persistent memory it reads at the start and appends to at the end, prove it remembers across two separate runs, then sketch a minimal "dreaming" step that distills recent runs into one improved instruction. This is **Cortex v0**, the shared memory of AtlasOS, and it lands in `atlas/memory/`.

### What you will build

A `memory/` component containing: a persistent memory store (a JSON or Markdown file) that Scout reads at startup and appends to at shutdown, proof that a fact written in run one is recalled in run two, and a minimal dreaming script that reads the recent run log and distills it into one better instruction for next time. All committed to git.

### Milestones (in order, each fully explained)

**1. Set up the memory folder.** In your VS Code terminal, from inside your `atlasos` repo:

```text
cd ~/atlasos
# atlas/memory already exists with a README; we are filling it in.
ls atlas/memory
```

You will create two things here: a memory store the agent reads and writes (`store.json` or `store.md`), and a tiny dreaming step (`dream`). Keep it simple on purpose. The point is the *pattern*, not the plumbing.

**2. Create the memory store and the read-at-start / write-at-end rule.** Ask your coding agent, in plain English:

> *"In atlas/memory, create a file store.json that holds a list of remembered facts, each with a timestamp and the text. Then write a short module (memory.py or memory.js, match the repo) with two functions: load_memory() reads store.json and returns the facts as text to prepend to Scout's prompt, and save_memory(text) appends a new fact with the current time. If the file is missing, start with an empty list."*

Read the diff. You want exactly two operations: load (read the file, return its contents) and save (append a new entry). Nothing more.

**3. Wire Scout to read at the start and append at the end.** Now connect it to the Scout loop you built in Unit 5. Ask:

> *"In the Scout agent, at the very start of a run call load_memory() and put its contents into the system prompt under a heading 'What you already know'. At the end of a run, call save_memory() with any new durable fact Scout learned (a one-line note). Tell Scout in its prompt to read what it already knows before answering, and to save anything worth remembering at the end."*

This is the whole heart of cross-run memory: **read before you act, write before you finish.**

**4. Prove memory persists across two separate runs.** This is the milestone that matters. Run Scout twice, as two distinct runs (not one conversation):

```text
# RUN 1: teach Scout one fact, then let the run end completely.
# (Start Scout however you start it, e.g. python scout.py or node scout.js)
You: "Remember that AtlasOS's north-star is a self-improving fleet of agents,
      and that our first agent is Scout. Save that to memory."
Scout: (calls save_memory) "Saved. I'll remember that next time."
# Let this run finish and exit.

# Confirm it was written to disk:
cat atlas/memory/store.json
# You should see your fact with a timestamp.

# RUN 2: a brand-new run. Do NOT repeat the fact.
You: "What is AtlasOS's north-star, and what was our first agent?"
Scout: (load_memory ran at startup, so the fact is in its prompt)
       "AtlasOS's north-star is a self-improving fleet of agents,
        and the first agent is Scout."
```

If run two answers correctly *without you repeating the fact*, memory works. The fact survived a full restart by living in `store.json`, not in the context window.

> 💡 **Keep yourself honest.** Always test recall in a *fresh* run. If you keep talking in the same run, you are testing the conversation, not the memory. The proof is that a brand-new process, started from scratch, knows something only the previous run was told.

**5. Sketch a minimal "dreaming" step.** Add a tiny self-improvement pass. First, have Scout append a one-line log of each run (the task and how it went) to `atlas/memory/runs.log`. Then create the dreaming step. Ask your agent:

> *"Create atlas/memory/dream that reads the last few lines of runs.log plus the current store, and asks the model one question: 'Looking at these recent runs, what is one instruction Scout should follow next time to do better?' Write that single improved instruction to atlas/memory/lessons.md. Then have Scout load lessons.md into its prompt at startup, alongside the memory store."*

Run it after a few Scout runs. You should get one concrete, generalisable instruction (a *principle*, like "always cite the source URL when reporting a fact"), not a brittle one-off rule. That distilled instruction now flows into the next run. That is the dreaming loop in miniature: read recent runs, distill a better instruction, feed it forward.

> ✅ **Keep a human in the loop.** Before `lessons.md` is trusted, read it yourself. In a fuller version this would arrive as a pull request you review in a minute, exactly the principles-not-rules, human-gated pattern from Part 8. For Cortex v0, eyeballing the one-line lesson is enough.

**6. Commit Cortex v0.** Save your work to git:

```text
git add -A
git commit -m "Add Cortex v0: Scout persistent memory + minimal dreaming step"
git push
```

**7. Stretch (optional).** Pick any of: (a) turn Scout's retrieval tool from Unit 5 into a real hybrid search over a small folder of notes and have it write findings into memory; (b) scope memory into a read-only "facts Scout should never edit" file plus a read-write "working notes" file; (c) add versioning by never overwriting `lessons.md`, appending each dreamed lesson with a date so you can see how Scout's instructions evolved.

### How you will know you are done

- ✅ `atlas/memory/store.json` exists and contains a fact with a timestamp after run one.
- ✅ A brand-new run two answers a question correctly using only what run one stored, without you repeating the fact.
- ✅ Scout reads memory at the start of a run and appends to it at the end.
- ✅ The dreaming step reads recent runs and writes one improved, generalisable instruction to `lessons.md`, which the next run loads.
- ✅ Everything is committed and pushed to GitHub.

> 💡 **If the recall test felt anticlimactic, that is the point.** Memory is not flashy. A second process simply *knowing* what the first one was told is the entire win, and it is what lets every later AtlasOS agent build on the last instead of starting cold.

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
RETRIEVAL / RAG
  Model knows only its training data -> retrieve fresh/private text into the prompt.
  Pipeline: chunk -> embed -> store -> (query) embed Q -> top-k -> re-rank -> answer.
  Embedding = meaning as numbers. Vector store finds the closest. Both decoupled
    from your answer model; all 3 providers offer embeddings (verify ids).
  Hybrid search = semantic (embeddings) + lexical (BM25), fused with RRF.
  Retrieval is just a TOOL the model calls (just-in-time / agentic retrieval).
  Measure the RETRIEVER alone: recall (did the right chunk show up?) + precision.

MEMORY
  Short-term = context window (finite, wiped). Long-term = durable file/db (survives).
  A bigger window is NOT long-term memory.
  Survive a long task: COMPACTION (summarize + restart) + external SCRATCHPAD.
  Across runs: read store at START, append at END. Read before you write.
  DREAMING = background pass: read recent runs -> distill BETTER INSTRUCTIONS.
    "test-time compute for memory." Memory raises the floor; dreaming raises it more.

FUZZY-TASK LEARNING (no unit test)
  Principles, not rules (generalize; often shorter file, better output).
  Teach it to LEARN: compare output vs ideal, adjust a PRINCIPLE in place.
  Low-friction loop: smallest team input (emoji/tag) for biggest gain.
  Route self-improvement through a human-gated PULL REQUEST (no drift).
```

## How this connects to the rest of the course

- **Next, Unit 7 (Evaluation and observability):** you measured the retriever by itself in this unit; next you build the harness that grades every agent's output (Warden), so quality is measured, not hoped, and you can tell whether a dreamed instruction actually helped.
- **Later, Unit 8 (Multi-agent orchestration):** Cortex becomes shared memory for the whole fleet, with read-only org knowledge and read-write task stores, and dreaming reconciles lessons across many agents, not just Scout.
- **Throughout:** every AtlasOS agent reads and writes Cortex. Scout is the first to remember; the rest reuse the same store, the same read-at-start / write-at-end pattern, and the same self-improvement loop.

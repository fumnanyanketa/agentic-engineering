# Unit 2: Prompting and Context Engineering

> **Course:** Agentic Engineering with Claude, a self-paced path *(working title)*
> **Unit 2 of 11:** From writing one good prompt to curating everything the model sees, the Claude way
> **Sources fused:** Agentic Engineering Modules 02-03 (principles) + Building with Claude Module 2 Lessons 3 and 6 (implementation)
> **Estimated time:** 90 to 120 minutes (read plus the build)

---

## In one sentence

Prompting is a debugging skill, not a writing skill, and it lives inside the bigger discipline of context engineering: you shape the words you send (clear instructions, structure, examples, output contracts), you curate the smallest set of high-signal tokens the model sees while it works, and you reach for the right lever (a tool, a stronger model, more thinking, a multi-step loop) instead of piling on more instructions, all measured against a small eval rather than vibes.

> 🎯 **Where this unit is heading.** The payoff is a **Build**: the first real, versioned artifact in the AtlasOS **prompt library**. You will author a system prompt for **Scout** (the research agent), tune it eval-driven from broken to passing, apply prompt caching and context engineering so it stays cheap and on-track, and commit it as a reusable, versioned file your whole fleet can reuse. Jump to **"The Build"** to see the finish line.

## First-principles companion

> 💡 **The durable ideas behind this unit.** The Claude-specific framing is recent; the concepts are not. For the timeless versions:
>
> - **[Language Models are Few-Shot Learners (GPT-3)](https://arxiv.org/abs/2005.14165)** (paper). The seminal account of why in-context prompting and worked examples work at all.
> - **[Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)** (essay). The principle-level treatment of "find the smallest set of high-signal tokens," covering curation and compaction as concepts, not buttons.
> - **[Using LLMs to write code](https://simonwillison.net/2025/Mar/11/using-llms-for-code/)** (Simon Willison). A working engineer arriving independently at the same conclusion: most of the craft is managing the model's context.

## A few plain-language basics first

- **Prompt:** the text you send the model. **Prompt engineering** is shaping that text so the model does what you want consistently, not once by luck.
- **System prompt:** a separate, higher-priority instruction that sets the model's role and standing rules for the whole conversation. It frames everything the user then says.
- **Context:** the full set of text the model can see in one request (system prompt, user message, reference docs, examples, past turns, tool results), measured in tokens. **Context engineering** is deciding what goes in that finite space and what stays out.
- **Eval (evaluation):** a small set of test cases (an input plus the answer you expect) that you run a prompt against to measure whether it actually works. The single most important habit in this unit.
- **Tool:** a small function the model can choose to run (do exact maths, look something up). Its **schema** is the written description of what it does and what inputs it takes.
- **Prompt caching:** reusing the already-processed stable prefix of your context so it is not reprocessed on every request. An economy tool, not an intelligence one.

You do not need to memorise these. Each returns the first time it matters.

## Why this unit matters

Most people meet prompting as a writing exercise: craft one clever paragraph, admire one nice answer, ship it. That fails the moment the work gets real. In real jobs you inherit a prompt several people have edited, that mixes rules, tone, and old fixes, and that suddenly works *worse* after a model upgrade. The professional frame is different and it is the hinge of this whole course:

> 🔑 **The reframe in one line.** Prompt engineering controls *how the model communicates* (phrasing, instructions). Context engineering controls *what the model knows* (the information available to it). Prompting is now best understood as one part of the bigger task: curating everything the model can see while it works.

Get this right and prompting becomes a calm, measurable debugging loop. Get it wrong and you will "prompt and pray," piling rules on a prompt with no test set and being surprised when it breaks on the next input or the next model.

## Learning objectives

By the end of this unit you will be able to:

1. Apply the core prompting moves: clear and specific instructions, few-shot examples, structure with tags, and machine-readable output contracts.
2. Build a small eval with the three case types every prompt needs (control, edge, capability/handoff), and tune a prompt one change at a time against it.
3. Diagnose *why* a prompt fails and pick the right lever (remove an old patch, add a tool, stronger model or more thinking, a multi-step loop) instead of adding instructions.
4. Explain context engineering and context rot, and aim for the smallest set of high-signal tokens that still does the job.
5. Apply prompt caching and the platform context-engineering techniques (tool search, programmatic tool calling, compaction) to keep an agent cheap, fast, and on-track.
6. Treat a system prompt as a versioned software artifact, committed and reusable.

## Prerequisites

- **From Unit 0:** the mental model (engineer the environment, not the model), tokens, context window, context rot, and sampling controls.
- **From Unit 1:** a working Claude Code loop and your AtlasOS repo, where this unit's artifact lands.
- **Skills that matter:** sending a message to Claude and reading the reply; comfortable reading and running Python; git.

---

## Part 1: Prompting is a debugging skill (not a writing one)

The amateur judges a prompt by reading one nice answer. The professional judges it against a small **eval**, a collection of test cases where each case is one input plus the answer you expect. The eval is what lets you tell luck from skill, and a behaviour change from a capability change.

> 🔑 **You cannot fix what you cannot measure.** When a prompt gets worse after a model change there are only two possibilities, and you must tell them apart: (1) the new model is just as capable but *behaves differently* (fixable by prompting), or (2) the new model is *less capable* at this task (no prompt will fix it; change the model). Only an eval tells you which.

The core prompting moves are a small set you combine, not pick from:

- **Be clear, direct, and specific.** The model fills any gap with a guess. "Summarize this in three bullets for a busy manager, no jargon" beats "summarize this."
- **Few-shot examples (show, do not only tell).** A handful of worked input/output pairs lock in tone and format better than a paragraph of rules, especially for classification, extraction, and translation.
- **Chain-of-thought for reasoning tasks.** Ask the model to work through steps before answering. Some newer reasoning models already do this internally, so you may not need to ask.
- **Structure for mixed content.** Wrap each kind of content in clearly labelled sections so the model never confuses guidelines, policy, and data.
- **Output contracts.** If your code will read the answer, ask for a strict, machine-readable shape (JSON, or a tagged block) and describe the exact fields.

Every eval needs three kinds of case. The third is the one teams forget:

| Case type | What it checks |
|---|---|
| **Control** | Something that should *always* work. Your "nothing is on fire" signal. |
| **Edge** | Something the model got wrong before. The prompt should stop the regression. |
| **Capability / handoff** | Does the model know the limits of its job: when to pass to a human, or refuse? |

> ❌ **A common mistake:** "prompt and pray," shipping a prompt with no test set; or over-instructing until the prompt is so rigid it breaks on anything slightly unexpected. Both are symptoms of judging by vibes instead of cases.

> ✅ **Pro tip.** Version your prompts in git like code, change one variable at a time so you can attribute any quality change to a specific edit, and keep your test set: it is the seed of your AtlasOS eval suite (Warden, Unit 8).

---

## Part 2: The debugging loop, and choosing the right fix

Here is the loop you repeat for every prompt in trouble:

```text
1. Run the eval on v0 of the prompt   -> see what is failing
2. Clean up the prompt FIRST          -> often a free win on its own
3. Fix failing cases ONE AT A TIME    -> so cause and effect are clear
4. Re-run the eval after every change  -> keep what helps, undo what does not
```

**Cleanup comes first, every time.** Real prompts arrive cramped into one paragraph, often with copied-in website junk (a "hero image" reference, a cookie notice) and patches for old models all mixed together. Add structure with tags, delete the junk, and define the output. Just doing this, with no other change, usually lifts the score.

```text
<role>
You are a research assistant for AtlasOS. You gather and synthesize sources.
</role>

<guidelines>
- Be concise. Cite every claim with its source.
- The provided source set is your only source of truth. Do not invent facts.
</guidelines>

<output_format>
Return findings as JSON: a list of {claim, source_url, confidence}.
</output_format>
```

Enforce the contract in the **harness** (the code around the model), not just in the prompt text. A `stop_sequences` entry or structured outputs is more reliable than hoping the prompt holds.

When cases still fail, diagnose *why* and pick the matching lever. The deep lesson:

> 🔑 **Instructions do not add capability.** Telling the model "it is CRITICAL to calculate correctly" does not make it better at mental maths. If the model genuinely cannot do the step, change the means, not the wording.

| Symptom | The right fix (not "more instructions") |
|---|---|
| Wrong or **hidden** facts | Remove the old defensive patch; trust the data source. |
| Bad maths / unreliable step | Give it a **tool** (schema plus the real code). |
| Will not act / too cautious | State **both sides** of the trade-off and let it weigh them. |
| Not capable enough | A **stronger model** or more **thinking** (adaptive reasoning effort). |
| One prompt doing too much | Split into **generate -> evaluate -> repair**. |

Two failure shapes recur and are worth naming. First, **withholding**: everyone fears the model *inventing* facts (hallucination), but a defensive patch like "never give wrong details, send them to the URL" makes a literal-minded newer model *suppress* a correct answer it already has. Second, **one-sided rules**: state only the cost of escalating ("it costs ~$8") and the model will never escalate; state both sides and a smart model balances them itself.

> 💡 When steps are easy and repeatable to separate, split them. A generate/evaluate/repair loop (three small prompts, each with one job) often passes a constraint task at *lower* cost and latency than forcing one giant prompt to do it all, and you can add soft preferences in the evaluate step without touching the grader.

> ✅ **Pro tip.** Record your defensive patches in version control with a note on *why* each was added. A newer model can turn yesterday's helpful patch into today's bug, and you will want to find and remove it.

---

## Part 3: Context engineering (curate, do not stuff)

In Part 1 you shaped the words. Now widen the lens to the model's entire **context**: everything it can see in one request. Context is a finite resource in two senses, the fixed token limit and a limited **attention budget** (its focus spreads thinner as you add more text). The analogy is human working memory.

> 🔑 **The guiding heuristic.** Aim for the *smallest set of high-signal tokens that still gets the job done.* Every token should earn its place. Write system prompts at the right altitude: specific enough to steer clearly, not so packed with rigid detail that there is no room to adapt.

The trap is assuming bigger is better. **Context rot** is the measurable tendency of a model to recall and reason *less* accurately as its context grows, the cause being that same diluted attention budget. It shows up in "needle in a haystack" tests: bury one fact in a long document and recall drops as the document grows. A large context window lets you add more text; adding more text often makes quality *worse*, not better.

> ❌ **A common mistake:** "just stuff the whole document in," or confusing a large context window with good context engineering. The window is capacity; engineering is what you *choose* to put in it. And letting an agent's context grow unbounded across turns with no trimming guarantees rot.

The Claude platform gives you concrete levers for this, each narrowing context at a different point. The habit underneath all of them, repeated until it sticks: **read your transcripts** (the full record of what the model actually saw and did) instead of optimising from dashboards alone.

- **Tool search (narrow the tools).** Agents can carry tens or hundreds of tools; every schema you load up front eats context (in one demo, individual tool schemas ran 6,000 to 14,000 tokens each). Hand the model one search tool instead, and load a tool's full definition only when it is actually chosen.
- **Programmatic tool calling (narrow the results).** Claude writes code well. Instead of dumping a raw tool result into context, have Claude write a small script that calls the tool, curates the output, and returns only the relevant part (for example, the aggregate sentiment from a 60-minute transcript).
- **Compaction (keep going).** As a long run approaches the limit, summarize the older turns (guided by your own prompt), drop what is stale, and continue. Set a threshold (often 400K to 500K, model-dependent) for a near-unlimited-feeling context.

> 💡 These are production tools, not demo tricks. In the talk's worked example, the three context techniques together brought an agent's cost down to about a third of where it started, with quality held or improved, because less clutter in context means the model performs better.

---

## Part 4: Prompt caching and the advisor strategy (the cheap, on-track Claude way)

Great models are only half the story. The platform layer is what takes an agent from a slow, expensive demo to a cheap, fast, production product. The single most important piece:

> 🔑 **Prompt caching, if you remember nothing else.** The platform processes your input tokens before generating a reply. Caching saves that processed prefix and reuses it, so on later turns only the *new* tokens are processed. Three benefits: about a **90% discount** on cached tokens, cached tokens do **not** count against your rate limit (an 80% hit rate is effectively a 5x larger limit), and lower **time to first token**. Crucially, caching has **no effect on intelligence**: same output, just pre-processed and cheaper.

Start by measuring your hit rate (the Console shows it, including why a cache broke), then aim for 80% or above.

```python
# Automatic caching: the simplest start. Caches the heavy, repeated prefix.
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    cache_control={"type": "ephemeral"},   # auto-cache the stable prefix
    system=large_stable_system_prompt,      # keep this byte-for-byte identical
    messages=messages,
)
print(response.usage.cache_read_input_tokens)   # > 0 means the cache is working
```

> ❌ **The most common cache mistake:** a **timestamp** in the system prompt ("what day is it?"). It changes every request, which changes the prompt, which breaks the cache. Cached tokens must be *exactly* identical to be reused. Keep any per-request value out of the stable prefix.

When you still want Opus-level judgement without Opus-everywhere cost, use the **advisor strategy**: run a cheaper **executor** (Sonnet or Haiku) that handles most of the work, and let it **consult a stronger advisor** (Opus) only on the tricky cases it is unsure about. The mental model is a senior engineer paired with a junior: the junior stays hands-on-keyboard, the senior's occasional review lifts the result close to what the senior could do solo.

```python
# Advisor pattern: a cheap executor consults a stronger model only when stuck.
advisor_tool = {"type": "advisor_20260301", "name": "advisor",
                "model": "claude-opus-4-7"}     # the strong model on call

response = client.beta.messages.create(
    betas=["advisor-tool-2026-03-01"],
    model="claude-sonnet-4-6",                  # cheap executor does the easy 90%
    max_tokens=4096,
    tools=[advisor_tool],
    messages=messages,
)
```

> 💡 You get the cost profile of the cheap model on the easy 90%, and the judgement of the strong model on the hard 10%. The advisor recovers intelligence you would otherwise lose: in the demo it caught a "watermelon" case (green on the outside, red underneath) that the executor alone had reported as on-track.

---

## Key takeaways

1. **Prompting is debugging.** Tune against an eval one change at a time; cover control, edge, and capability/handoff cases.
2. **Clean up before anything clever.** Structure with tags, delete junk, define the output (and enforce it in the harness). Often a free win.
3. **Instructions do not add capability.** Pick the right lever: remove a patch, add a tool, stronger model or more thinking, or a multi-step loop.
4. **Context is finite; curate it.** Smallest set of high-signal tokens. Bigger windows invite context rot, not better answers.
5. **Cache first, then advise.** Prompt caching cuts cost and latency with no intelligence loss; the advisor gives Opus judgement at executor cost.
6. **Read your transcripts, version your prompts.** The transcript is your debugging surface; the prompt is a software artifact.

## Common pitfalls

- ❌ "Prompt and pray": shipping with no eval, then being surprised it fails on new inputs or a new model.
- ❌ Telling the model to "do better" instead of giving it the means (a tool, a model, a loop).
- ❌ Long lists of "never do X" rules a smarter model will over-apply, hiding information or refusing to act.
- ❌ Stating only one side of a trade-off and being surprised the model overdoes that side.
- ❌ Stuffing the whole document in and confusing a large window with good context engineering (context rot).
- ❌ A timestamp (or any changing value) in the system prompt, silently breaking your cache.
- ❌ Optimising from dashboards without ever reading a transcript.

---

## 🛠️ The Build: the AtlasOS prompt library

> The hands-on payoff. You will author the first real, versioned artifact in `prompts/`: a system prompt for **Scout**, AtlasOS's research agent. You fuse the eval-driven debugging loop with the platform's caching and context-engineering levers, so Scout starts out reliable *and* cheap, and you commit it as a reusable file the fleet can reuse and improve later.

### What you will build

A versioned `prompts/scout.md` system prompt plus a tiny eval harness that proves it. Scout's job: take a research question and a set of sources, and return cited, structured findings without inventing facts. You take it from a deliberately broken v0 to all-green, then make it cheap with caching and lean context.

### Milestones (in order, each stands alone)

1. **Eval first.** Create `prompts/scout_cases.json` with 5 cases: 1 control (a clear question answerable from the sources), 2 edge (one where the answer is in an awkward source it tends to skip; one where it tends to invent a fact), 1 capability/handoff (a question the sources cannot answer, so Scout must say so rather than guess), and 1 of your own. Write the expected answer for each *before* writing the prompt. Add a small runner that prints a pass/fail grid.
2. **The broken v0.** Write a deliberately messy Scout prompt: one big paragraph, some copied-in junk, and an old patch like "never state anything not on the official site, link out instead." Run the eval for a red baseline.
3. **Clean up.** Restructure with `<role>`, `<guidelines>`, `<policy>`, and `<output_format>` tags, delete the junk, and add a JSON output contract enforced in the harness. Re-run and record the lift.
4. **Fix failures one at a time.** Remove the overfitted patch so Scout trusts its sources (the withholding bug); add a tool (for example a `fetch_source` or citation-checker) where an instruction alone cannot help; and state both sides of any one-sided rule. Re-run after each single change.
5. **Make it cheap and lean.** Put Scout's stable instructions in a cacheable prefix (no timestamps), measure `cache_read_input_tokens`, and aim for an 80%+ hit rate. Trim the context to the smallest high-signal set, and read the transcript to confirm what Scout actually sees.
6. **Commit to the library.** Save `prompts/scout.md` with a version header and a short changelog noting *why* each patch exists. This is the first reusable artifact in the AtlasOS prompt library.
7. **Stretch.** Add the advisor strategy (a cheap executor consulting Opus on a deliberately tricky "watermelon" source) and confirm the advisor catches what the executor missed; or add a generate/evaluate/repair loop for a multi-source synthesis question.

### How you will know you are done

- ✅ All 5 eval cases pass consistently (run each a few times), and you can point to the exact change that fixed each one.
- ✅ At least one case is fixed by a **tool** and one by **stating both sides**, proving you did not just add instructions.
- ✅ Scout's cache hit rate is measured and at 80% or above, with the output unchanged.
- ✅ You read the transcript and can show the context is lean (no stuffed, low-signal tokens).
- ✅ `prompts/scout.md` is committed to your AtlasOS repo with a version header and changelog.

---

## Cheat sheet

```text
WHEN A PROMPT GETS WORSE
  1. Do you have an eval? Build one (control + edge + capability/handoff).
  2. Clean up FIRST: structure with tags, delete junk, define output (+ enforce in harness).
  3. Fix ONE failure at a time; re-run after each change.

CHOOSE THE RIGHT FIX (not "more instructions")
  Wrong / hidden facts ........ remove the old patch; trust the data source
  Bad maths / unreliable step . give it a TOOL
  Will not act / too cautious . state BOTH sides of the trade-off
  Not capable enough .......... stronger model OR more thinking
  One prompt doing too much ... split into generate -> evaluate -> repair

CONTEXT ENGINEERING (smallest high-signal set)
  context rot: more tokens often = worse, not better
  tool search ............ load only the tool you need, not every schema
  programmatic tool call . have Claude write code to curate tool RESULTS
  compaction ............. summarize old turns at a threshold (e.g. 400K)

PLATFORM LEVERS
  prompt caching ... 90% cheaper cached tokens, ~5x rate limit, lower latency
                     no intelligence change · breaks on a timestamp in the prompt
  advisor strategy . cheap executor + strong advisor on hard cases (senior+junior)

ALWAYS  read your transcripts · prompts are versioned artifacts
```

## How this connects to the rest of the course

- **Next, Unit 3 (Model and reasoning levers):** the "stronger model vs adaptive thinking" choices you made by feel here get made rigorously, with evals and a routing policy (Atlas's orchestrator).
- **Unit 4 (Tools and MCP):** the tools you reached for in Part 2 get designed properly, going deeper on tool search and programmatic tool calling.
- **Unit 8 (Evals and verification):** the eval you seeded here grows into Warden's graded suite, with a deliberately hard case.
- **Throughout:** every AtlasOS agent inherits a prompt from the library you start here; Scout is just the first.

---

*Unit 2 of the combined path. Fuses the vendor-neutral principles of Agentic Engineering Modules 02-03 with the Claude-specific implementation of Building with Claude Module 2 (Lessons 3 and 6). Adapt model ids, beta flags, and SDK details to the current docs.*

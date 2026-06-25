# Module 2 · Lesson 5: The Thinking Lever

> **Course:** Building with Claude, a self-paced course
> **Module 2:** Core skills, working with the model
> **Speaker:** Alexander Briken, Applied AI Research team, Anthropic
> **Source talk:** [The thinking lever](https://www.youtube.com/watch?v=T7KqH7kYnE4) · [full transcript](../../transcripts/code-with-claude-2026-london-2026/15_the-thinking-lever.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

Claude gets smarter when you let it spend more tokens thinking before it answers, so instead of a crude on/off thinking switch you should hand Claude a thinking tool it can reach for whenever it needs, and control how hard it works with a single dial called effort (defaulting to extra high when in doubt).

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you build **EffortLab**, a small harness that runs one hard task at every effort level and shows you, side by side, how quality, tokens, and time change. Everything before the Capstone teaches the ideas you will use there. If you want to see the finish line first, jump to the **"Capstone Project: build EffortLab"** section near the end, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[Chain-of-Thought Prompting Elicits Reasoning in LLMs](https://arxiv.org/abs/2201.11903)** (paper). The seminal demonstration that intermediate reasoning steps, the "thinking" the effort dial controls, substantially improve accuracy on hard tasks.

## A few plain-language basics first

This lesson uses some everyday AI terms. Here they are in simple words, so nothing below is confusing:

- **LLM (Large Language Model):** the kind of AI that reads and writes text. "Claude" is an LLM.
- **Model:** one specific version of that AI. Anthropic offers a family: **Haiku** (small, fast, cheap), **Sonnet** (a balance), and **Opus** (the most capable).
- **Token:** the unit a model reads and writes in, roughly three quarters of a word. You are billed per token, and more tokens means more time.
- **Inference time (or test time):** the moment when the model is actually answering your request, as opposed to **training time**, when the model was being built. "Test time compute" means work the model does while answering you.
- **Reasoning model:** a model that can spend extra tokens thinking through a problem before answering, which makes it more accurate on hard questions.
- **Latency:** how long the model takes to respond, in seconds. Lower is faster.
- **Tool:** a small function the model can choose to run, for example a web search.
- **Agent:** an AI that takes a series of actions on its own toward a goal, rather than answering in one shot.
- **Eval (evaluation):** a set of test cases you run a model against to measure whether it works.

You do not need to memorise these. Every term is also explained again the first time it appears below.

## Why this lesson matters

For years, the obvious way to make a model smarter was to make it bigger and train it longer (**train time compute**). One of the biggest recent developments is a second lever: let the model spend more tokens **thinking at the moment it answers** (**test time compute**). More thinking, more intelligence. This lesson is about that lever: what thinking actually is, why a simple on/off toggle is the wrong way to use it, and how to control it well with the **effort** dial. Get this right and you can extract a lot more capability from the same model, and decide for yourself where to sit on the trade-off between intelligence and speed.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain **test time compute** and why spending more tokens thinking raises intelligence.
2. Name the three things Claude spends test time compute on: **thinking**, **tool calling**, and **text**.
3. Explain why a **thinking toggle** is a poor proxy for effort, and what **adaptive thinking** does instead.
4. Choose an **effort level** (low to max) for a given task, and know that **extra high** is the safe default.
5. Decide between a **bigger model at low effort** and a **smaller model at high effort** (usually the bigger model wins if any intelligence is needed).

## Prerequisites

- Module 2 · Lesson 1 (sending a message to Claude and reading the reply).
- Helpful but optional: Module 2 · Lesson 4 (Picking the Right Model), which introduces thinking and effort as levers. This lesson goes deep on that one lever.

---

## Part 1: more thinking means more intelligence

The core finding is simple and consistent. As Claude spends more tokens thinking through a problem before answering, its performance goes up.

Alexander shows two graphs that, he points out, plot the **same score** two different ways:

- On the **left**: as you increase model size (Haiku to Sonnet to Opus), performance rises on an internal agentic coding benchmark, up toward nearly 80%.
- On the **right**: holding the model fixed and letting it **spend more tokens thinking**, performance also rises.

And this holds across every kind of task he tested: a reasoning benchmark (Deep Search QA), computer use (OSWorld), and a PhD-level exam (Humanity's Last Exam). In all of them, the model produces better outcomes when it uses more tokens to think before answering.

> 🔑 **The central idea.** There are two ways to buy more intelligence: a bigger model (train time compute) or more thinking at answer time (test time compute). This lesson is about the second one.

### A live demo: low, high, and max

To make this concrete, Alexander runs one prompt at three different effort levels on Opus 4.7. The prompt: "create a realistic simulation of cars on a one-way street at a traffic light."

| Effort | Time | Output tokens | Result |
|---|---|---|---|
| **Low** | ~50 seconds | ~4,600 | A decent simulation. Cars on two lanes, stopping at the light. Simplistic, and the traffic light sits oddly in the middle of the road. |
| **High** | ~2x the time | ~2x the tokens | More detailed. Different vehicle types, the light repositioned to overhang the road, and the cars react to each other (more intelligent driving). |
| **Max** | ~10x the tokens and time | ~10x | The best of the three. A properly hanging traffic light, a detailed sky in the background, and even more lifelike vehicle motion. |

> 💡 **The trade-off you can see with your own eyes.** Each step up spends more tokens and more time, and each step up produces a better result. That is the whole lever in one demo.

Where does this lead? Alexander points to the **METR benchmark**, which measures how long a human task a model can complete autonomously. Across model generations (a mix of bigger models and better thinking), Claude handles longer and longer tasks. One of Anthropic's latest models, Mythos, reaches roughly **16 hours of human work** at a 50% success rate. The trajectory is from seconds, to minutes, to hours, and eventually days or weeks of autonomous work.

---

## Part 2: the three things Claude spends compute on

"Test time compute" is just "spending tokens while answering." Alexander breaks down the three forms it takes:

1. **Thinking.** Claude's space for reasoning. A **scratchpad** where it considers the question, looks at the data it has, and works out its next steps before acting.
2. **Tool calling.** Claude's interface with the outside world. A web search, a call to Salesforce, talking to an MCP server, writing to a file system, anything. (**MCP**, the Model Context Protocol, is a standard way to connect tools to a model; you do not need the details here.)
3. **Text.** The output Claude produces for you: a summary of the work it did, or a clarifying question to gather more information.

> 🔑 **Why this list matters.** These are three separate **capabilities**. Keep that in mind, because the big mistake later in the lesson is accidentally switching one of them off.

All of this has a direct cost: tokens, and the time it takes. So naturally you want control over how much of it Claude does.

### Two ways to control test time compute

Alexander names two levers users have:

- **Effort.** A dial from **low to max**. Higher effort means Claude works longer and spends more tokens. This is the main subject of the lesson.
- **Budgets.** Stricter constraints, such as a **max token** limit or a **task budget** (a feature in the API that gives Claude a token allowance for a whole job).

The rest of the talk focuses on effort.

---

## Part 3: why a thinking toggle is the wrong tool

When reasoning models first appeared, they worked in a rigid order: you asked a question, Claude thought for a fixed amount of time (however many tokens you allocated), then it ran tools one after another, then it gave you the answer.

But that is not how humans work. As Alexander puts it: nobody asks you a question, watches you stand frozen processing it, and then sees you run off and execute a bunch of steps before returning. Real work is interleaved: do something, think about it, do another thing, think about that, then return the result.

That observation led to two evolutions:

### Interleaved thinking

**Interleaved thinking** lets Claude have a thinking step **after every tool call**. So it can act, reflect, act again, reflect again. Much more like how a person actually works through a task.

### Adaptive thinking

**Adaptive thinking** goes further: it gives the model control over **when** it thinks and **why**. Depending on the question, Claude chooses, in whatever order it likes, to call a tool, output some text, or think.

The human analogy again: if you are playing tennis, you hit the ball and run back to the baseline without deliberating. If you are working a hard academic problem, you think at every step. Same person, different amount of thinking, chosen to fit the task. Claude can even choose **not to think at all** if the question is easy. Ask a person "what is 10 + 10?" and they say 20 instantly; ask them a PhD problem and they think a long time.

> 💡 **Adaptive thinking is not a model router.** It is not secretly classifying your request and sending it to a different model. It is telling one model: "you have a thinking tool, use it whenever you like." Before, Claude was forced to think at one fixed point. Now it does not have to think at all if it does not need to.

Anthropic runs all its published benchmarks on adaptive thinking, and finds it **Pareto efficient** relative to the older interleaved approach. ("Pareto efficient" means you cannot get a better result without giving something up; in plain terms, it is on the best-possible trade-off curve.)

### The big mistake: treating thinking as an effort dial

Historically, people treated the thinking toggle as a way to ask for more effort: "if you want a better answer, turn thinking on and wait longer." That instinct is reasonable, but it is wrong.

> 🔑 **The key insight (quote):** "A thinking toggle is actually a poor proxy for the amount of effort that a model should put in." (Alexander Briken)

Here is why. When you flip extended thinking **off**, you are not telling Claude "think less." You are **removing a core capability**. Remember the three capabilities from Part 2: thinking, tool calling, text. Turning off thinking deletes one of them entirely.

> ❌ **The anti-pattern:** using a thinking on/off switch to express "how hard should you work?" You are not expressing effort; you are amputating a capability.

The better mental model is by analogy with tools. We do not tell Claude "never search the web" or "always search the web." We give it a search tool and let it reason about when to use it. Thinking should work the same way: give Claude the thinking tool and let it decide when to reach for it.

> 🔑 **The ideal:** Claude knows it *can* think, and uses that ability every time it would help. You set the overall **effort** and the **budget**; Claude allocates within that.

It is the same way you work with a teammate. You do not say "do not use your inner monologue, just blurt out an answer." You give them the constraints of the problem, they go execute based on who they are and what context they have, and they come back with an answer. You want Claude to work like that teammate.

---

## Part 4: how to choose an effort level

Now to the practical question: which effort level should you use? Effort runs from **low** to **max**, with levels in between (medium, high, and extra high).

### First choice: use evals if you can

The best way to choose is to **evaluate model performance**. Build a good test set of the hard problems you actually want Claude to handle, then measure how well it does at each effort level. That tells you the lowest effort that still gets the job done.

> 💡 **Watch for diminishing returns.** As effort rises, each step buys less. In the car demo, **max** used roughly double the tokens of extra high for only a marginal bump in quality. So more effort is not free, and past a point it is barely worth it for that task.

### Low effort can be genuinely clever

Low effort is not just "dumber." Because it constrains how much the model thinks, it sometimes finds unique, efficient solutions.

Alexander's favourite example is **Claude Plays Pokemon**, an eval where Claude is dropped into Pokemon Red with tools to press Game Boy buttons and vision over the screen, and told to beat the Elite Four. On **low effort**, Claude did something surprising: it tried to **shortcut the game**. It used repels, potions, and escape ropes to avoid trips back to the Pokemon Center, and ran away from wild battles. Constraining its thinking pushed it into a unique strategy that almost completed the game faster than it otherwise would.

> 🔑 **Low effort has its place.** Use it for tasks that are **not intelligence-bound**: things that can be done quickly without the model deliberating much. Latency-sensitive jobs like classification, summarization, or data extraction are good fits.

### Rules of thumb when you do not have a perfect eval

Alexander knows most teams do not have a perfect eval. So here are his rules of thumb, walking from the high end down:

| Effort | When to use it |
|---|---|
| **Max** | Delivers gains on the **hardest** tasks, but with diminishing returns. Do **not** start here unless you know the task genuinely needs that much intelligence and the model will have to think a long time. |
| **Extra high** | The **default** for Claude Code and claude.ai. Argued to be the best trade-off between intelligence, speed, and tokens. |
| **High** | A good balance of token usage and intelligence. If your use case needs **any** intelligence, you should probably land here. Faster than the two above. |
| **Medium** | A way to dial down token usage further. |
| **Low** | Latency-sensitive use cases that are not intelligence-bound: classification, summarization, data extraction. |

> 🔑 **When in doubt, go extra high.** It is the default Anthropic ships in its own products, and Alexander argues it is a great Pareto-efficient point between latency, tokens, and intelligence.

```python
# Adaptive thinking on, with an explicit effort level.
# Effort lives inside output_config, not at the top level.
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=8192,
    thinking={"type": "adaptive"},          # let Claude decide WHEN to think
    output_config={"effort": "xhigh"},      # low | medium | high | xhigh | max
    messages=messages,
)
```

> ✅ **Best practice: enable thinking whenever possible.** Give Claude the scratchpad so it knows it *can* reason when it needs to. Then control the length with the effort levels.

---

## Part 5: bigger model at low effort, or smaller model at high effort?

This is the question that connects this lesson to "Picking the Right Model." You have two levers (train time compute, meaning model size; and test time compute, meaning thinking). So should you run a **small model like Haiku at high effort**, or a **big model at low effort**?

Alexander shows the car simulation again, this time on **Haiku 4.5**. Haiku spent about half the time of the Opus version and the **same number of tokens**, but the result was much worse. As he put it, he was not even sure those shapes were cars.

> 🔑 **The conclusion:** "If the question you're asking of Claude needs any intelligence at all, you're often better off using the larger model, even with effort at low." (Alexander Briken)

So when should you reach for a smaller model? For **low-intelligence use cases**: tasks so simple that you are not worried about the outcome, because you know Claude will get them right almost every time.

> 💡 **The ideal way to decide is still evals.** If you can run Haiku and Opus across the full range of effort levels, that is the perfect world. You will not always have those resources, which is why the rules of thumb above exist, but evals beat guessing.

### The future: you set the bar, Claude allocates

Alexander closes with where this is heading. The ideal is that you give Claude a high-level constraint, "only spend this much," or "take at most a week", and Claude figures out how to allocate its compute appropriately. It works out how many tokens to spend, then executes within that budget. Over time, Claude gets better at recognising which tasks deserve more resources and allocating accordingly.

---

## Key takeaways

1. **More thinking buys more intelligence.** Spending more tokens at answer time raises performance, across every kind of task.
2. **Three capabilities.** Test time compute is spent on **thinking**, **tool calling**, and **text**. Turning thinking off deletes a capability; it does not just "reduce effort."
3. **Adaptive thinking beats a toggle.** Let Claude decide when and how much to think, like giving it a tool, rather than forcing or forbidding thinking.
4. **Effort is the right dial.** Low to max. Use evals to choose; watch for diminishing returns; **extra high** is the safe default.
5. **Bigger model usually wins when intelligence is needed**, even at low effort. Save small models for genuinely easy, latency-sensitive tasks.

## Common pitfalls

- ❌ Using a thinking on/off switch to express "how hard should you work?" (you are amputating a capability, not setting effort).
- ❌ Starting at **max** effort by default, then paying for diminishing returns.
- ❌ Forbidding thinking on a task that actually needs reasoning.
- ❌ Reaching for a small model on a task that needs intelligence, just because "small is faster."
- ❌ Choosing an effort level by vibes when you could measure it with a small eval.

---

## 🛠️ Capstone Project: build EffortLab

> This is the main hands on project for the lesson. You will recreate Alexander's live demo as a reusable harness: take one hard task, run it at every effort level, and see exactly how quality, tokens, and time trade off. By the end you will *feel* the lever instead of just reading about it.

### What you will build

**EffortLab** is a small harness that sweeps a single task across effort levels and reports the trade-off. It has three parts that line up with the lesson:

1. **The hard task:** one genuinely difficult prompt (a simulation, a multi-step reasoning problem, or a small coding challenge) where more thinking visibly helps.
2. **The sweep:** code that runs the same task at low, medium, high, extra high, and max effort with adaptive thinking on, capturing tokens, time, and a quality measure each time.
3. **The verdict:** a results table (or a small chart) that lets you spot the **diminishing returns** point and choose the lowest effort that is good enough.

> 🎯 **Pick your task.** Copy Alexander's car simulation, or choose your own: a packing puzzle, a short story with strict constraints, a small refactor, a logic problem. The only requirement is that the easy and hard versions of the answer are clearly different, so you can *see* effort working.

### Why this is the perfect practice

| Lesson skill | Where you use it in EffortLab |
|---|---|
| Test time compute raises intelligence | Milestone 1, the hard task |
| Adaptive thinking (let Claude decide when to think) | Milestone 2, the request setup |
| The effort dial (low to max) | Milestone 3, the sweep |
| Capturing tokens and latency | Milestone 4, the metrics |
| Spotting diminishing returns | Milestone 5, the verdict |
| Bigger model vs smaller model at effort | Milestone 6, the model comparison |

### Milestones (build them in order, each one works on its own)

1. **Write one hard task.** Pick a prompt where a weak answer and a strong answer look obviously different. Save it.
2. **Make one request with adaptive thinking.** Send the task with `thinking={"type": "adaptive"}` and a single effort level. Read back the answer and the token usage. Confirm it runs end to end.
3. **Sweep the effort levels.** Loop the same task across **low, medium, high, xhigh, and max**. Store the answer, output tokens, and wall-clock time for each.
4. **Capture metrics.** For each run, record output tokens and time. (Optional: a simple quality score, either your own rating or an LLM-as-judge prompt that scores the answer 1 to 10.)
5. **Find the verdict.** Lay the results out as a table or chart. Identify the **diminishing returns** point: the level past which extra tokens barely improve quality. Pick the lowest "good enough" effort for this task.
6. **Compare model sizes.** Run the task on a smaller model (for example Haiku) at high effort and a bigger model (for example Opus) at low effort. Which gives the better answer? Confirm Alexander's rule of thumb for your task.

### How you will know you are done

- ✅ You have a **table** showing answer quality, tokens, and time across all five effort levels.
- ✅ You can point to the **diminishing returns** point on your task and name the lowest effort that is good enough.
- ✅ You used **adaptive thinking** (not a hard thinking toggle) for every run.
- ✅ You ran the **bigger-model-low-effort vs smaller-model-high-effort** comparison and can say which won for your task.
- ✅ You can explain, in one sentence, why turning thinking *off* is not the same as setting effort to low.

> 💡 **Keep yourself honest:** read at least one full answer at each effort level. The numbers tell you the cost; the answers tell you whether the extra effort actually bought anything.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self contained tasks. Each asks you to *do* one specific thing. They are optional and independent. The **Capstone Project above is the main build**, and already includes these.

### Exercise 1: see the lever (foundational)
Pick any creative or reasoning prompt. Run it at **low** effort, then at **max** effort, both with adaptive thinking on. Read both answers. Write one sentence on how they differ and how much more time and tokens max took.

### Exercise 2: the three capabilities (foundational)
Give Claude a task that needs a tool (for example, a web search). Run it once with thinking on and once with thinking disabled. Note what changes. Explain which capability you removed when you turned thinking off.

### Exercise 3: pick the right effort (intermediate)
Take a simple, latency-sensitive task (classification or summarization). Run it at low and at high effort. Is the high-effort answer any better? If not, you have just proved that low effort was the right choice. Write down why.

### Exercise 4: diminishing returns (intermediate)
Sweep one hard task across all five effort levels and record tokens for each. Find the step where doubling the tokens barely improved the answer. That is your diminishing-returns point.

### Exercise 5: bigger or harder-working? (advanced)
Run the same intelligence-heavy task on a small model at high effort and a big model at low effort. Compare quality, tokens, and time. State which you would ship and why, referencing cost per successful outcome.

---

## Cheat sheet

```text
THE TWO LEVERS OF INTELLIGENCE
  Train time compute = bigger model
  Test time compute  = more thinking at answer time

WHAT TEST TIME COMPUTE IS SPENT ON
  thinking  (scratchpad reasoning)
  tools     (interface with the world)
  text      (the output for you)

THINKING: USE ADAPTIVE, NOT A TOGGLE
  thinking={"type": "adaptive"}   # Claude decides WHEN to think
  Turning thinking OFF deletes a capability; it does not "reduce effort".

EFFORT: THE RIGHT DIAL  (output_config={"effort": ...})
  low ....... latency-sensitive, not intelligence-bound (classify/summarize/extract)
  medium .... dial down tokens
  high ...... use if the task needs ANY intelligence
  xhigh ..... THE DEFAULT (Claude Code, claude.ai); best Pareto point
  max ....... hardest tasks only; diminishing returns

BIGGER MODEL vs SMALLER MODEL
  Needs intelligence?  -> bigger model wins, even at low effort
  Truly simple task?   -> smaller model is fine
  Best answer of all:  -> use an eval to decide
```

## How this connects to the rest of the course

- **Earlier, Module 2 · Lesson 3 (The Prompting Playbook):** uses adaptive thinking as one fix when a model is not capable enough.
- **Earlier, Module 2 · Lesson 4 (Picking the Right Model):** treats thinking and effort as levers among several; this lesson is the deep dive on them.
- **Next, Module 2 · Lesson 6 (Getting More Out of the Claude Platform):** combines thinking with caching, context engineering, and an advisor pattern in production.
- **Later, Module 5 (Claude Managed Agents):** long-horizon tasks where setting a budget and letting Claude allocate compute becomes central.

---

*Source: "The thinking lever" by Alexander Briken (Anthropic), Code with Claude 2026, London. Code snippets are illustrative reconstructions of the approaches shown in the talk. Adapt the model names and API details to the current SDK.*

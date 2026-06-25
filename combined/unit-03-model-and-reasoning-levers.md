# Unit 3: Model and Reasoning Levers

> **Course:** Agentic Engineering with Claude, a self-paced path *(working title)*
> **Unit 3 of 11:** Choosing the model and the reasoning effort by measurement, not vibes, and spending for the cheapest successful outcome
> **Sources fused:** Agentic Engineering Module 15 (cost and model-selection principles) + Building with Claude Module 2 Lessons 4-5 (implementation)
> **Estimated time:** 90 to 120 minutes (read plus the build)

---

## In one sentence

Picking a model and how hard it should think is a measurement problem, not a vibes problem: you build a small private eval, run your real task across model tiers and effort levels, and then choose the option that is cheapest *per successful outcome* (not cheapest per token), using thinking, effort, prompt caching, and context engineering as the dials that move you along that cost-versus-quality curve, or shift the whole curve.

> 🎯 **Where this unit is heading.** The payoff is a **Build**: the **AtlasOS routing policy**, a small piece of code that decides which model tier runs each step and how much reasoning effort to spend, measured as cost per successful outcome. You will encode the **advisor strategy** (cheap models execute, the expensive model advises only when needed) and commit the policy plus a benchmark table to your repo. Jump to **"The Build"** to see the finish line.

## First-principles companion

> 💡 **The durable ideas behind this unit.** The Claude-specific framing is recent; the concepts are not. For the timeless versions:
>
> - **[Choosing the right model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model)** (docs). The tool-agnostic decision framework: pick on your own evals, weigh capability against speed and cost, and tune effort before switching models.
> - **[Chain-of-Thought Prompting Elicits Reasoning in LLMs](https://arxiv.org/abs/2201.11903)** (paper). The seminal demonstration that intermediate reasoning steps, the "thinking" the effort dial controls, substantially improve accuracy on hard tasks.

## A few plain-language basics first

- **Model tier:** one size in a model family. Anthropic offers **Haiku** (small, fast, cheap), **Sonnet** (a balance), and **Opus** (the most capable). Bigger usually means smarter but slower and pricier.
- **Eval (evaluation):** a small set of your own test cases you run a model against to measure whether it works. The single most important idea in this unit.
- **Latency:** how long the model takes to respond, in seconds. Lower is faster.
- **Test time compute:** work the model does *while answering* you (as opposed to training time, when the model was built). More of it means more intelligence on hard tasks.
- **Thinking:** a private scratchpad where Claude reasons before it acts. **Adaptive thinking** lets the model decide *when* and *how much* to think.
- **Effort:** a dial from **low** to **max** for how hard Claude works overall, across thinking, tool calls, and text.
- **Prompt caching:** reusing the pre-processed, repeated start of your prompt instead of paying to read it again. Roughly a 90% discount on the cached part.

You do not need to memorise these. Each returns the first time it matters.

## Why this unit matters

Every time a new model ships, the internet fills with hot takes that tell you nothing you actually need: is this model better *for your use case*, and how hard should it think? Public benchmarks point you in a rough direction, but your real workload almost never looks like a benchmark. And the instinct to reach for the biggest model on the highest effort everywhere is a costly mistake that quietly burns your budget without buying quality.

> 🔑 **The whole unit in one line.** The right model is not the one that is cheapest per token. It is the one that is cheapest *per successful outcome*, and you find it by measuring your real task across tiers and effort levels, not by guessing.

Get this right and you can extract far more capability from the same spend, and decide for yourself where to sit on the trade-off between intelligence, speed, and cost. Get it wrong and you either overpay for power you do not need or ship a cheap model that fails silently.

## Learning objectives

By the end of this unit you will be able to:

1. Explain why a small, private eval beats any public benchmark for choosing a model.
2. Compare options on **cost per successful outcome**, not cost per token, and understand why a smarter model can finish cheaper.
3. Use the four levers (**thinking**, **effort**, **prompt caching**, **context engineering**) to move along the cost-quality curve, or shift it.
4. Choose an **effort level** for a task, knowing that turning thinking off deletes a capability and that extra high is the safe default.
5. Decide between a bigger model at low effort and a smaller model at high effort, and encode that as a routing policy.

## Prerequisites

- **From this course:** Unit 0 (tokens, model tiers, the cost-and-latency mental model) and Unit 2 (prompting and context engineering as levers).
- **Skills that matter:** sending a message to Claude and reading the reply, plus reading token usage off the response. (You set up the measured environment in Unit 0.)
- **Skills you can defer:** building a full eval harness with graded suites. You build the smallest real version here; Unit 8 deepens it.

---

## Part 1: Pick on your own eval, not a benchmark

When a model launches, its model card and benchmark scores (for example **SWE-bench**, a fixed set of real software bugs to fix) tell you, roughly, "this model got better at coding." They do *not* tell you it got better at *your* coding, in *your* language, on *your* codebase. Real workloads are mixed: a coding agent might first research a niche corner of an SDK, then write code from what it found, crossing two benchmarks in one task.

> 🔑 **Build a private eval.** A small, well-designed eval (your own test cases, written from your own real tasks) teaches you more about which model to use than any public benchmark. It turns "which model?" from a guess into a yes-or-no answer backed by your numbers.

An eval is made of **tasks**, each with inputs and success criteria. Borrow the maths-exam analogy: a task has a question, the answer you need, and the **working** shown in between. For agents the working matters as much as the answer, because a model can land on the right output by accident or by doing something you would never want in production.

> ✅ **Grade the working, not just the answer.** Check both that the agent reached the right outcome *and* that it took the right steps. Use a **deterministic grader** (plain code, "did it call the lookup tool with a `country` argument?") for things that must be exact, and an **LLM as a judge** (a model scores the answer) for things where wording can vary.

Three ways evals go wrong, all fixed by reading your transcripts (the full record of what the model saw and did): mistaking **noise for signal** (run each task several times; high variance means a bad task or grader), blaming the model for **infrastructure failures** (an API or tool crash is not the model being dumb), and **silent saturation** (your test set drifts from what real users now ask, so feed real failures back in).

---

## Part 2: Cost per successful outcome (and why smaller is not always faster)

Here is the result that reframes everything. A team had a simple code-fix pipeline running on **Haiku** with no thinking, scoring 92%. They turned thinking on and hit 100%. Curious, they reran on **Sonnet** and **Opus**: both also hit 100%, but counterintuitively *faster*.

> 🔑 **Smaller is not always faster.** A more capable model can finish in **fewer turns**: it plans more strategically and does not need to research as much to be confident. Fewer turns can mean lower total latency and fewer total tokens, even at a higher per-token price. When Opus 4.5 launched it completed tasks with higher accuracy than Sonnet while using *significantly fewer* output tokens for that workload.

So the right comparison is not the sticker price per token. It is the cost of getting the job done correctly, end to end.

> ❌ **A common mistake:** comparing models on cost per token. A cheap-per-token model that loops twenty times, fails a third of the time, and gets retried is far more expensive than a pricier model that succeeds once. Always divide total cost by *successful* outcomes.

This connects to a hard fact about agents from the production literature: errors compound. If a single step is 95% reliable, ten steps in a row is about 60%, and twenty steps drops below 40%. A model that needs fewer, more reliable steps is doing double duty: cheaper *and* more reliable. That is why "right-size the model to the task" means matching each sub-step to the smallest tier that still passes its quality bar, measured, not guessed.

---

## Part 3: The reasoning lever (thinking and effort)

There are two ways to buy more intelligence: a bigger model (train time compute) or more thinking at answer time (test time compute). This part is about the second. Claude spends test time compute on three things: **thinking** (its reasoning scratchpad), **tool calling** (its interface to the world), and **text** (the output for you). Keep that list of three *capabilities* in mind.

> ❌ **The big anti-pattern: a thinking on/off toggle as an effort dial.** When you flip thinking *off* you are not telling Claude "think less," you are deleting one of its three capabilities entirely. "A thinking toggle is a poor proxy for the amount of effort a model should put in." (Alexander Briken)

The better model is by analogy with tools: we do not tell Claude "never search the web," we give it a search tool and let it reason about when to use it. Thinking should work the same way.

> 🔑 **Use adaptive thinking, set effort.** **Adaptive thinking** gives the model control over *when* and *why* it thinks, even choosing not to think at all on an easy question. You set the overall **effort** (low to max); Claude allocates within it.

```python
# Adaptive thinking on, with an explicit effort level.
# Effort lives inside output_config, not at the top level.
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=8192,
    thinking={"type": "adaptive"},        # let Claude decide WHEN to think
    output_config={"effort": "xhigh"},    # low | medium | high | xhigh | max
    messages=messages,
)
```

How to choose an effort level? Use evals if you can: measure your hard tasks at each level and take the lowest effort that still passes. Watch for **diminishing returns** (in one demo, max used roughly double the tokens of extra high for only a marginal bump). When you do not have a perfect eval, use these rules of thumb:

| Effort | When to use it |
|---|---|
| **Max** | The hardest tasks only; diminishing returns. Do not start here. |
| **Extra high** | The **default** for Claude Code and claude.ai; the best Pareto point between intelligence, speed, and tokens. |
| **High** | Good balance; if your task needs *any* intelligence, probably land here. |
| **Medium** | Dial token usage down further. |
| **Low** | Latency-sensitive and *not* intelligence-bound: classification, summarization, data extraction. |

> 💡 **Low effort can be clever, not just dumber.** In *Claude Plays Pokemon*, low effort pushed Claude into a unique, efficient strategy (using repels and escape ropes to skip trips back to the Center). Constraining thinking is right for tasks that are not intelligence-bound. When in doubt, go **extra high**.

---

## Part 4: The curve-shifting levers (caching and context)

Effort and model size move you *along* the cost-quality curve. Two more levers **shift the whole curve** so you get more quality for the same money.

**Prompt caching.** When part of your prompt repeats from request to request (instructions, tool definitions, a reference document), the provider saves the pre-processing of that repeated **prefix** and you reuse it, paying roughly one tenth of the normal input price for the cached part.

> 🔑 **What this unlocks (quote):** "You can get Opus quality at Sonnet cost, or you can get Sonnet quality at Haiku cost." (Lucas)

> ✅ **Order stable-to-changing, and append only.** Put fixed instructions and tool definitions first, reference material next, and the parts that change every turn (the live question, fresh data) at the very end, because changing any part invalidates the cache for it and everything after. Treat messages as immutable and only append. The classic way people break the cache: a timestamp in the system prompt, which changes every turn. One team raised its cache hit rate from 7% to 84% just by moving changing data to the end. Aim for **80% to 90%**.

```python
# The API returns cache metrics so you can measure your hit rate.
print(response.usage.cache_read_input_tokens)      # served from cache (cheap)
print(response.usage.cache_creation_input_tokens)  # written to cache this time
print(response.usage.input_tokens)                 # processed at full price
```

**Context engineering.** Being thoughtful about exactly what text you put in the model's context does two good things at once: it saves tokens, and it often *raises* accuracy, because the model reasons over less clutter. Returning Markdown instead of JSON, a simple date stamp instead of a long timestamp, and the day of the week pre-computed cut one tool response by **66.4%**, and because an agent runs many turns, that saving compounds. Deduplicating web-search articles before handing them to Claude gave a 77% token cut, 65% cost cut, and accuracy *up* 9%.

> ❌ **Anti-pattern:** wrapping an external API in a tool and returning its raw response untouched. That dumps noise into context every single turn. Treat tool outputs like writing for a human: clean them up.

---

## Key takeaways

1. **Pick on a private eval, not a benchmark.** Your real task across tiers and effort levels is the only honest signal. Grade the working, not just the answer.
2. **Cost per successful outcome, not cost per token.** A smarter model can be cheaper overall by finishing in fewer, more reliable turns.
3. **Adaptive thinking, not a toggle.** Turning thinking off deletes a capability. Set effort instead; extra high is the safe default.
4. **Bigger model usually wins when intelligence is needed**, even at low effort. Save small models for genuinely easy, latency-sensitive steps.
5. **Caching and context shift the curve.** Roughly 90% off the cached prefix (order stable-to-changing); cleaner tool outputs save tokens and raise accuracy.

## Common pitfalls

- ❌ Choosing a model from a public benchmark instead of your own eval.
- ❌ Comparing on cost per token instead of cost per successful outcome.
- ❌ Reaching for the biggest model on max effort everywhere by default.
- ❌ Using a thinking on/off switch to express "how hard should you work?" (amputating a capability, not setting effort).
- ❌ Breaking your cache with a timestamp (or other changing value) in the system prompt.
- ❌ Piping raw, bloated tool outputs straight into context every turn.
- ❌ Optimising cost without re-running your eval, letting quality quietly regress while you celebrate the lower bill.

---

## 🛠️ The Build: the AtlasOS routing policy

> The hands-on payoff. This fuses the two implementation labs (a model sweep and an effort sweep) with the AtlasOS roadmap rows for Lessons 4 and 5: a real model-routing and reasoning-effort policy, measured as cost per successful outcome, committed to `orchestrator/`.

### What you will build

A small **routing policy** for AtlasOS: code (plus a config) that, given a step's type, decides which model tier runs it and at what effort, and a short **benchmark table** proving the choice on a real task. You will encode the **advisor strategy** from the company brief: cheap models execute, and the expensive model advises only when a step is genuinely hard or a check fails. The metric is **cost per successful outcome**, from design principle 4 ("cost per successful outcome, not cost per token").

### Milestones (in order, each stands alone)

1. **Define 5 routing tasks.** Pick a handful of real AtlasOS steps with clearly different difficulty: an easy one (Herald formats a status line, or Scout classifies a source), a medium one (Scout summarises an article), and a hard one (Atlas plans a multi-step research run). Write each as a task with inputs and a success criterion. Make at least one an agent-style task where the **steps** matter, not just the final answer.
2. **Write two graders.** A **deterministic** grader (plain code, "did it call the required tool with the required argument?") and an **LLM-as-judge** grader (a small prompt scoring whether the answer matches the expected one). Wire each task to the grader it needs. Run each task several times so you can tell noise from signal.
3. **Sweep tiers and effort.** Run the eval across at least two tiers (for example Sonnet and Opus) and adaptive thinking at two effort levels (say high and xhigh). For every run capture output tokens, input tokens, wall-clock time, and pass rate. Compute a **cost per successful outcome** column. This is your headline metric.
4. **Encode the policy.** Write `orchestrator/routing_policy.py` (plus a small `routing.yaml`) that maps each step type to a `{model, effort, thinking}` choice, justified by the sweep. Default cheap tiers to *execute* the routine steps; reserve the expensive tier for the hard reasoning steps. This is the **advisor strategy** in code.
5. **Wire the advisor escalation.** Add one rule: when a cheap step fails its grader (or returns low confidence), escalate that single step to the expensive model as an **advisor**, then let the cheap model continue. Show in the table that escalating *only when needed* beats running everything on the expensive tier on cost per successful outcome.
6. **Commit the policy and the benchmark table.** Put `routing_policy.py`, `routing.yaml`, and a markdown benchmark table under `atlas/orchestrator/` and commit. Add prompt caching to the stable prefix and report your cache hit rate alongside the table.
7. **Stretch.** Add a fallback rule (retry with backoff, then a backup model) so one provider outage does not stall a run, and re-run the eval to confirm the policy still holds.

### How you will know you are done

- ✅ A benchmark table shows pass rate, cost, latency, and **cost per successful outcome** for every tier-and-effort combination on your real tasks.
- ✅ Your policy routes each step type to a justified `{model, effort, thinking}` choice, with cheap tiers executing and the expensive tier advising only when needed.
- ✅ The escalation rule demonstrably beats "everything on the expensive model" on cost per successful outcome.
- ✅ At least one task is graded on its **steps**, not just its final answer.
- ✅ Your cache hit rate is measured, and the policy plus table are committed under `atlas/orchestrator/`.

> 💡 If a number surprises you, the transcript is where the truth is. Read at least a few runs in full before trusting the table.

---

## Cheat sheet

```text
PICKING A MODEL (measure, don't vibe)
  Build a PRIVATE eval from real tasks (not a benchmark).
  Grade the working AND the answer (code check + LLM judge).
  Run each task several times; read the transcripts.
  Compare on COST PER SUCCESSFUL OUTCOME, not cost per token.
  Smaller is NOT always faster (fewer turns can win).

THE REASONING LEVER
  test time compute = thinking + tool calls + text (three capabilities)
  thinking={"type":"adaptive"}  -> Claude decides WHEN to think
  turning thinking OFF deletes a capability, it is not "low effort"
  effort (output_config): low=classify/summarize/extract · high=needs intelligence
                          xhigh=DEFAULT/best Pareto · max=hardest only (diminishing)
  needs intelligence? bigger model wins even at low effort

CURVE-SHIFTING LEVERS
  prompt caching .... ~90% off cached prefix; order stable->changing; append only; aim 80-90%
  context engineering . clean tool outputs (Markdown, simple dates) = fewer tokens + more accuracy

THE ADVISOR STRATEGY (AtlasOS)
  cheap models EXECUTE the routine steps
  expensive model ADVISES only when a step is hard or a check fails
  route per step type; escalate on failure; measure cost per successful outcome
```

## How this connects to the rest of the course

- **Earlier, Unit 2 (Prompting and context):** introduced context engineering as a lever; here it becomes a measured, curve-shifting knob in the routing policy.
- **Next, Unit 4 (Tools and MCP):** the tool outputs you learned to trim here are what you will now design and connect; the advisor strategy gets wired into how tools and routing compose.
- **Later, Unit 8 (Evals and verification):** the small private eval you built here grows into Warden, AtlasOS's graded suite with a deliberately hard case.
- **Throughout AtlasOS:** the routing policy is the orchestrator's spending brain, the thing that makes "cost per successful outcome" real for every agent in the fleet.

---

*Unit 3 of the combined path. Fuses the vendor-neutral cost and model-selection principles of Agentic Engineering Module 15 with the Claude-specific implementation of Building with Claude Module 2 Lessons 4-5. Adapt model ids and SDK details to the current docs.*

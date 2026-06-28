# Unit 4: Model and Reasoning Levers

> **Course:** Agentic Engineering, a model-agnostic self-paced path *(working title)*
> **Unit 4 of 12:** Choose the right model and the right amount of reasoning for each job by measuring, not guessing, so you spend for the cheapest *successful outcome* instead of the cheapest token
> **The how, across models:** Claude (Anthropic) extended/adaptive thinking, Gemini (Google) thinking, GPT (OpenAI) reasoning effort, current practice verified June 2026
> **AtlasOS build:** the `orchestrator/` model-routing policy (Atlas chooses tier and effort per task; cheap executes, expensive advises)
> **Estimated time:** 90 to 120 minutes (read plus the build)

---

## In one sentence

Every model provider gives you two big dials, *how capable a model* and *how hard it thinks*, and this unit teaches you to set both by measurement: you will learn to pick the smallest model tier that still passes the task, to turn reasoning up only when the task actually needs it, to spend for the cheapest *successful outcome* rather than the cheapest token, and to wire those choices into a tiny routing policy where a cheap model does the work and an expensive one advises only when the stakes are high.

> 🎯 **Where this unit is heading.** The payoff is a **Build**: a small, explicit **routing policy** inside AtlasOS's `orchestrator/`. It is a short function that maps a task type to a model tier and a reasoning-effort level, encoding the rule "cheap model executes, expensive model advises when needed." You will test it on two contrasting tasks (one trivial, one hard) and record the cost and latency of each. Jump to **"The Build"** to see the finish line, then come back and we will get you there.

## First-principles companion

> 💡 **The durable ideas behind this unit.** The model names and flags change every few months; the underlying ideas do not. If you want the timeless versions (optional, read any time):
>
> - **[Choosing the right model (Anthropic docs)](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model)** (docs). The tool-agnostic decision framework: pick on your own evals, weigh capability against speed and cost, and tune effort before switching models.
> - **[Chain-of-Thought Prompting Elicits Reasoning in LLMs](https://arxiv.org/abs/2201.11903)** (paper). The seminal result that intermediate reasoning steps, the "thinking" the effort dial controls, substantially raise accuracy on hard tasks.

## A few plain-language basics first

New terms, in plain words. You do not need to memorise these; each is explained again the moment it matters.

- **Model:** one specific version of an AI, for example a "small" one or a "frontier" one. Every major provider ships a *family* of models at different sizes. Bigger usually means smarter but slower and more expensive.
- **Model tier:** the size class of a model. We use three tiers throughout: **small** (fast, cheap, for easy work), **mid** (a balance), and **frontier** (the most capable, slowest, priciest). Each provider has its own names for these.
- **Token:** the unit a model reads and writes in, roughly three quarters of a word. You are billed per token, so more tokens means more cost and more time.
- **Latency:** how long you wait for a response, measured in seconds. Lower is faster.
- **Reasoning (or thinking):** a private scratchpad where the model works through a problem step by step *before* it answers. More reasoning costs more tokens and time, and on hard problems it raises accuracy.
- **Reasoning effort:** a dial (low to high) that controls how much the model reasons. Each provider exposes its own version of this dial.
- **Eval (evaluation):** a small set of your own test cases with known right answers, used to *measure* whether a model and setting actually work for your task. This is how you replace guessing with data. (You build a real one in Unit 9.)
- **Cost per successful outcome:** the total money spent to get a *correct, usable* result, including retries and failures, not the price of a single token. This is the metric that matters.
- **The advisor strategy:** a pattern where a cheap model does the bulk of the work and calls in an expensive model only for the hard or risky parts. You get most of the quality for a fraction of the cost.

## Why this unit matters

In Unit 1 you learned to drive an agent, and in Unit 3 to talk to it well. But the moment your agent runs more than once or for more than one person, two new pressures arrive: it has to be *cheap enough* to keep running and *fast enough* to be usable. Agents are token-hungry because they loop, re-reading context turn after turn, so a careless model choice can quietly cost you ten times what it should. The good news: the same two dials that control cost (which model, how hard it thinks) also control quality, and once you measure instead of guess, you can usually cut cost and latency *without* losing quality.

> 🔑 **Cost per successful outcome, not cost per token.** The right model is not the one with the lowest sticker price per token. It is the one that gets the job done correctly for the least total spend, even if its per-token price is higher, because a smarter model often finishes in fewer turns and fewer retries.

## Learning objectives

By the end of this unit you will be able to:

1. Place any provider's models into three tiers (small, mid, frontier) and right-size a task to the smallest tier that still passes.
2. Explain why "cost per successful outcome" beats "cost per token," and compute it for a task.
3. Use the reasoning/thinking lever across Claude, Gemini, and GPT, and pick an effort level deliberately instead of by vibes.
4. Apply the advisor strategy: a cheap model executes, an expensive model advises only when needed.
5. Write a small, explicit routing policy that maps task types to a tier and an effort level, and measure its cost and latency.

## Prerequisites

- Units 1 and 3 finished: a working agent, your `atlasos` repo cloned locally, and comfort with the plan, act, verify loop.
- An API key for at least one provider (Anthropic, Google, or OpenAI), the same account you set up in Unit 1. The Build uses one provider; the ideas transfer to all three.
- No prior knowledge of pricing or reasoning models. We define everything as we go.

---

## Part 1: Three tiers, and the instinct that costs you money

Every major provider sells a *family* of models, not one model. They fall into three tiers, and naming them the same way across providers lets you reason about all of them at once.

```text
   SMALL  ────────────▶  MID  ────────────▶  FRONTIER
   fast, cheap          balanced            slowest, priciest,
   good for easy        the everyday        smartest, for the
   high-volume work     workhorse           hardest reasoning
```

Here is how today's families line up. Hold these ids loosely; they change often, so always verify against each provider's current model page.

| Tier | **Claude** (Anthropic) | **Gemini** (Google) | **GPT / OpenAI** |
|---|---|---|---|
| **Small** (fast, cheap) | Haiku | Gemini Flash (or Flash-Lite) | a small/mini GPT tier |
| **Mid** (balanced) | Sonnet | Gemini Pro | a mid GPT tier |
| **Frontier** (most capable) | Opus | Gemini Ultra/Pro-max class | the flagship GPT tier |

> 💡 **The names will drift; the shape will not.** Every provider keeps a cheap-and-fast tier, a balanced tier, and a top tier. When a new model lands, slot it into one of these three and your mental model still works. The exact id you type belongs in one place (your routing policy), so when it changes you edit one line.

The expensive instinct is to reach for the biggest model for everything, "to be safe." That is a costly mistake. A simple classification or extraction step might run perfectly on a small model, while only the single hardest reasoning step in your whole pipeline needs the frontier tier. Production hardening calls this **right-sizing**: match each sub-task to the *smallest* tier that still passes its quality bar.

> 🔑 **Right-size by measuring, not guessing.** You decide a task's tier by running it against a small eval and watching the pass rate, exactly the discipline from Unit 3 and the one you formalise in Unit 9. "It felt fine" is not a tier decision.

> ❌ **The default-to-frontier trap.** Running your whole agent on the top tier because one step is hard. You pay frontier prices on every trivial turn. Split the work and pay top tier only where it earns its keep.

---

## Part 2: Cost per successful outcome (and why smaller is not always cheaper)

The headline number on a pricing page is *cost per token*. It is the wrong number to optimise. What you actually care about is **cost per successful outcome**: the total spend to get a correct, usable result, including the cost of every retry, every failed attempt, and every extra turn.

Here is the story that makes it click. A team had a simple automated code-fix pipeline. They ran it on the *small* tier with no extra reasoning and scored 92%. They wanted 100%, so they tried the obvious fix (turn reasoning up) and got there. Then, out of curiosity, they reran the same eval on the *mid* and *frontier* tiers. Both also hit 100%, but counterintuitively, *faster*.

> 🔑 **Smaller is not always faster.** You would expect the small model to be quickest. But more capable models often finish in *fewer turns*: they plan better and do not have to research as much to be confident. Fewer turns can mean lower total latency *and* lower total cost, even at a higher price per token.

This is why per-token pricing lies to you. A model that costs twice as much per token but finishes the job in a third of the turns, with no retries, is *cheaper per successful outcome*. To see it, you have to measure the whole job, not one call.

```text
COST PER SUCCESSFUL OUTCOME (the metric that matters)

  total spend on the task (all turns, all retries, failures included)
  ────────────────────────────────────────────────────────────────
                  number of correct, usable results

  small model, cheap/token, 8 turns, 1 retry   ->  could be MORE
  mid model,   pricier/token, 3 turns, 0 retry  ->  could be LESS
  measure both; the cheaper sticker often loses.
```

> ✅ **Compute it for real.** For a task, capture three things per run: input tokens, output tokens, and whether it passed. Multiply tokens by the provider's price, sum across all attempts, and divide by the number of *passes*. That single number, not the per-token price, tells you which model to ship.

> ❌ **Optimising cost without re-checking quality.** If you downshift to a cheaper model and do not re-run your eval, quality can quietly regress while you celebrate the lower bill. Always re-measure the pass rate after a cost change.

---

## Part 3: The reasoning lever, and why an on/off switch is the wrong tool

The second dial is *reasoning* (also called *thinking*): a private scratchpad where the model works through a problem before answering. There are two ways to buy more intelligence: a bigger model (more *train-time* compute, baked in when the model was built) or more thinking at the moment it answers (more *test-time* compute). This part is about the second one.

The core finding is simple and consistent: as a model spends more tokens thinking before it answers, its accuracy on hard tasks goes up. It holds across reasoning problems, coding, computer use, and PhD-level exams. More thinking, more intelligence, at the cost of more tokens and more time.

When reasoning models first appeared, you controlled this with a crude **on/off toggle**: thinking on (think for a fixed budget, then act) or thinking off. That toggle is the wrong tool, and here is the precise reason.

> 🔑 **A thinking toggle is a poor proxy for effort.** Turning thinking *off* does not tell the model "work less." It *removes a capability*. The model spends test-time compute on three things: thinking (its scratchpad), tool calling (its interface to the world), and text (its output to you). Switch thinking off and you have amputated one of the three, not gently dialed down the effort.

The better mental model is the one you already use for tools. You do not tell an agent "never search the web" or "always search the web"; you give it a search tool and let it decide when to reach for it. Thinking should work the same way: give the model a thinking ability and let it choose when to use it, the same way a tennis player swings without deliberating but a mathematician thinks at every step. The same person, different amount of thinking, chosen to fit the task.

This is what modern **adaptive thinking** does: the model itself decides *when* and *how much* to think, and can even choose not to think at all on an easy question. You no longer flip a switch; you set an overall *effort level* and let the model allocate within it. (Note: adaptive thinking is not a secret model router. It is one model deciding how much to use its own scratchpad, not handing your request to a different model.)

> ❌ **The anti-pattern:** using a thinking on/off switch to express "how hard should you work?" You are not expressing effort, you are deleting a capability. Use the effort dial for effort, and leave thinking available.

---

## Part 4: How to choose an effort level (across all three providers)

The right way to express "work this hard" is the **effort dial**: a setting from low to high (with levels in between). Higher effort means the model thinks longer and spends more tokens; lower effort means faster and cheaper. All three major providers expose a version of this dial.

The principle first, stated vendor-neutrally: **let the model think (keep the capability available), and use the effort dial, not the on/off switch, to control how much.** Now the how, across providers. Hold the exact parameter names loosely and verify against current docs; the *shape* is identical everywhere.

| | **Claude** (Anthropic) | **Gemini** (Google) | **GPT / OpenAI** |
|---|---|---|---|
| Name for the lever | extended / **adaptive thinking** | **thinking** (a thinking budget) | **reasoning effort** |
| How you dial it | an **effort** level (low to max) plus adaptive thinking on | a **thinking budget** (token allowance), or auto | a **reasoning_effort** setting (e.g. low / medium / high) |
| "Let the model decide" | adaptive thinking chooses when to think | dynamic/auto thinking budget | the model reasons as needed within the effort level |
| Turn it down for easy work | low effort | small or zero thinking budget | low reasoning effort |

The everyday rules of thumb, walking from the top down:

| Effort | When to use it |
|---|---|
| **Highest (max)** | The hardest tasks only, and even then with diminishing returns: the top step often doubles tokens for a marginal quality bump. Do not start here. |
| **High / extra-high** | A strong default for anything that needs *any* real intelligence. The product makers ship this as the default in their own apps because it is the best balance of intelligence, speed, and tokens. |
| **Medium** | A way to dial tokens down when the task is moderate. |
| **Low** | Latency-sensitive jobs that are *not* intelligence-bound: classification, summarization, data extraction. Fast and cheap, and good enough because the model rarely gets these wrong. |

> 🔑 **When in doubt, go high (or extra-high), then measure down.** Start at a sensible high default, then use a small eval to find the *lowest* effort that still passes. That is the lowest-cost setting that gets the job done. If you have no eval yet, a high default is the safe Pareto-efficient choice.

> 💡 **Watch for diminishing returns.** Each step up the effort dial buys less than the one before. Past a point you are paying double the tokens for a barely-better answer. The eval is what shows you where that point is for *your* task.

Here is the same idea in code across the three providers. These are illustrative; verify parameter names against current SDKs.

```python
# Claude (Anthropic): adaptive thinking on, explicit effort level.
resp = anthropic_client.messages.create(
    model="claude-<frontier-id>",            # verify current id
    max_tokens=8192,
    thinking={"type": "adaptive"},           # let Claude decide WHEN to think
    output_config={"effort": "high"},        # low | medium | high | xhigh | max
    messages=messages,
)

# GPT (OpenAI): reasoning effort on a reasoning-capable model.
resp = openai_client.responses.create(
    model="<reasoning-model-id>",            # verify current id
    reasoning={"effort": "high"},            # low | medium | high
    input=messages,
)

# Gemini (Google): a thinking budget (token allowance) on a thinking model.
resp = genai_client.models.generate_content(
    model="<gemini-thinking-id>",            # verify current id
    contents=prompt,
    config={"thinking_config": {"thinking_budget": 8192}},  # or auto/dynamic
)
```

---

## Part 5: The advisor strategy (cheap executes, expensive advises)

You now have two dials (tier and effort). The advisor strategy combines them into one of the highest-leverage patterns in agent engineering.

The idea: most of the steps in a real task are easy. So run the bulk of the work on a **cheap model** (small tier, low effort) and call in an **expensive model** (frontier tier, high effort) only for the hard or risky moments: a tricky judgment, a plan that must be right, a final check before something irreversible. The cheap model executes; the expensive model advises.

```text
   ┌─────────────────────────────────────────────────────────┐
   │  CHEAP EXECUTOR  (small tier, low effort)                │
   │  does the routine turns: read, fetch, extract, draft     │
   │                                                          │
   │        │  hits a hard/risky step? escalate ──────┐       │
   │        ▼                                          ▼       │
   │  keeps going on the easy stuff      EXPENSIVE ADVISOR     │
   │                                     (frontier, high       │
   │                                      effort) weighs in    │
   │                                     only when called      │
   └─────────────────────────────────────────────────────────┘
   Result: most of the quality of the big model, a fraction of the cost.
```

Why it works: you pay frontier prices only on the small slice of work that actually needs them. If 90% of your turns are routine, you run 90% of your tokens at small-tier prices and reserve the expensive model for the 10% where it changes the outcome. This is "cost per successful outcome" applied across a whole pipeline.

> 🔑 **This is an AtlasOS design principle.** The company brief states it directly: *cheap models execute; the expensive model advises only when needed.* Your routing policy in the Build is where this rule becomes real code.

It is also model-agnostic. The executor could be a small Gemini Flash and the advisor a frontier Claude, or any mix. The pattern is about *roles* (executor, advisor), not about any one provider.

> ✅ **Pair the advisor with verification.** The advisor is most valuable on exactly the steps where a mistake is expensive. Wire it to your verify step (Unit 1): let the cheap model act, and have the expensive model advise or review before anything irreversible happens. (You will set up a proper independent reviewer, Warden, in Unit 9.)

> ❌ **Advisor on everything.** If you call the expensive advisor on every single turn, you have just paid frontier prices for the whole job and thrown the savings away. Escalate by rule (task type, confidence, stakes), not by default.

---

## Part 6: When not to reach for an LLM (and when to fine-tune)

The cheapest, fastest, most reliable model call is the one you do not make. Picking a model and an effort level already assumes a model call is the right tool. Sometimes it is not.

**When NOT to use an LLM at all.** If a task is well-defined and deterministic, a plain rule or a small traditional model beats an LLM on cost, speed, and reliability, and it never hallucinates:

- A fixed mapping, a regular expression, a lookup table, or a few `if` statements (routing by a known keyword, validating an email format, summing a column).
- A classic, narrow machine-learning model (a small classifier) when you have labelled data and need millions of cheap, consistent predictions.

Use an LLM for the genuinely fuzzy, language-shaped parts (understanding intent, summarising, drafting, reasoning over messy text), and let ordinary code handle everything it can. A good agent is mostly plain code with model calls at the few steps that truly need judgment.

> 🔑 **Smallest tool that works.** Reach down the ladder before you reach up it: rule, then small model, then small LLM, then frontier LLM. Each rung up costs more and adds a failure mode (non-determinism). Justify every step.

**When fine-tuning is the answer (awareness, not how-to).** This course's stance is "context, not model surgery": you get most gains by improving prompts, context, and tools, not by retraining the model. That stance is right almost always. Fine-tuning (training a base model further on your own examples) is worth *considering* only when all of these hold:

- You have a large set of high-quality examples of the exact behaviour you want.
- The behaviour is stable (it will not change every week, or you will be retraining forever).
- Prompting and context engineering have genuinely plateaued, and you have the evals to prove it.
- You need a consistent style or format at scale, or a smaller, cheaper model to match a bigger one's quality on your narrow task.

Even then, treat it as a last lever, reached for only after prompting, retrieval, and tools. Knowing *when* it is the answer is the skill; the *how* is a specialised topic you pick up once the conditions above are clearly met.

> ❌ **A common mistake:** fine-tuning to add knowledge. Fine-tuning changes behaviour and style, not facts. For fresh or private knowledge, use retrieval (Unit 6), not retraining.

## Key takeaways

1. **Three tiers everywhere.** Small, mid, frontier. Every provider has them; right-size each task to the smallest tier that still passes its eval.
2. **Cost per successful outcome, not per token.** A pricier model that finishes in fewer turns with no retries is often cheaper overall. Measure the whole job.
3. **Reasoning is a dial, not a switch.** Turning thinking *off* deletes a capability. Keep thinking available and control effort with the effort dial.
4. **High is a safe default; measure down.** Start high, then use a small eval to find the lowest effort that still passes. Watch for diminishing returns.
5. **Advisor strategy.** Cheap model executes, expensive model advises only on hard or risky steps. Most of the quality, a fraction of the cost.

## Common pitfalls

- ❌ Reaching for the frontier model everywhere "to be safe," and paying top-tier prices on trivial turns.
- ❌ Comparing models on cost per token instead of cost per successful outcome.
- ❌ Using a thinking on/off switch to express effort (you are amputating a capability, not dialing effort).
- ❌ Starting at max effort by default, then paying for diminishing returns.
- ❌ Downshifting to a cheaper model or lower effort without re-running your eval, letting quality silently regress.
- ❌ Calling the expensive advisor on every turn, which erases the whole point of the strategy.
- ❌ Hard-coding model ids in many places, so a routine model change becomes a painful find-and-replace.

---

## 🛠️ The Build: the AtlasOS routing policy (`orchestrator/`)

> The hands-on payoff. You will create the `orchestrator/` component and write a small, explicit routing policy: a function that maps each task type to a model tier and a reasoning-effort level, encoding "cheap executes, expensive advises." Then you will run it on two contrasting tasks and record cost and latency, so the policy is backed by numbers, not vibes.

### What you will build

A file `orchestrator/routing.py` (plus a one-line config) inside your `atlasos` repo. Given a task type, it returns the model tier, the model id, and the reasoning effort to use, and it flags when the expensive advisor should be consulted. A tiny test script runs the policy on two opposite tasks (one trivial, one hard) and prints a small table of model, tokens, latency, and cost. You commit the policy and the results table.

### Milestones (in order, each fully explained)

**1. Open your repo and create the component.** In your VS Code terminal, go to the project you made in Unit 1 and create the orchestrator folder:

```text
# Move into your AtlasOS repo (the one you cloned in Unit 1).
cd ~/atlasos

# Create the orchestrator component folder.
mkdir -p orchestrator

# Confirm you are in the right place.
ls
# You'll see your earlier files (README.md, your memory file) plus: orchestrator
```

**2. Write the tier map (one place for model ids).** Create `orchestrator/models.py`. This is the single file you edit when a provider renames a model, so ids live in exactly one place. Ask your agent, or type it by hand. Use the ids for the provider whose key you have; verify them against the provider's current model page first.

```python
# orchestrator/models.py
# The three tiers, one place. Verify these ids against current docs.
TIERS = {
    "small":    "claude-haiku-<id>",    # fast, cheap
    "mid":      "claude-sonnet-<id>",   # balanced
    "frontier": "claude-opus-<id>",     # most capable (the advisor)
}
```

**3. Write the routing policy.** Create `orchestrator/routing.py`. This is the heart of the Build: an explicit map from task type to tier and effort, plus the advisor rule. Keep it simple and readable on one screen.

```python
# orchestrator/routing.py
from .models import TIERS

# Map each task TYPE to a tier and a reasoning-effort level.
# Principle: cheap tier + low effort for easy work;
#            frontier tier + high effort only when the task needs intelligence.
POLICY = {
    "classify":   {"tier": "small",    "effort": "low"},    # latency-bound, easy
    "extract":    {"tier": "small",    "effort": "low"},    # structured, easy
    "summarize":  {"tier": "small",    "effort": "medium"}, # easy, slight care
    "draft":      {"tier": "mid",      "effort": "high"},   # needs some intelligence
    "plan":       {"tier": "frontier", "effort": "high"},   # hard reasoning
    "review":     {"tier": "frontier", "effort": "high"},   # high stakes, advise
}

# Tasks where a mistake is expensive: consult the frontier advisor.
ADVISOR_TASKS = {"plan", "review"}

def route(task_type: str) -> dict:
    """Return the model id, effort, and whether to use the expensive advisor."""
    choice = POLICY.get(task_type, {"tier": "mid", "effort": "high"})  # safe default
    return {
        "model": TIERS[choice["tier"]],
        "effort": choice["effort"],
        "use_advisor": task_type in ADVISOR_TASKS,
    }

if __name__ == "__main__":
    for t in ["classify", "plan"]:
        print(t, "->", route(t))
```

**4. Encode the advisor strategy in one helper.** Add a small function that *runs* a task: the cheap tier does the work, and if `use_advisor` is true, it asks the frontier model to advise or check the result. Pseudocode is fine if you are not wiring a real key yet; the point is to make the pattern explicit.

```python
# orchestrator/run.py (sketch; adapt to your provider's SDK)
from .routing import route
from .models import TIERS

def run_task(task_type, prompt, client):
    plan = route(task_type)
    # Cheap executor does the work.
    result = call_model(client, plan["model"], plan["effort"], prompt)
    # Expensive advisor weighs in only when the rule says so.
    if plan["use_advisor"]:
        advice = call_model(client, TIERS["frontier"], "high",
                            f"Review this result for correctness:\n{result}")
        return {"result": result, "advice": advice}
    return {"result": result}
```

**5. Test on two contrasting tasks.** Pick one trivial task (`classify`: e.g. "Is this message a refund request? yes/no") and one hard task (`plan`: e.g. "Draft a step-by-step plan to migrate a service to a new database with zero downtime"). Run each through the policy. For each call, capture: the model chosen, input and output tokens, and wall-clock time (use Python's `time.time()` around the call).

```text
# Run your test script:
python -m orchestrator.run_demo

# What you'll see (your numbers will differ):
classify -> small tier, low effort   | 180 tok  | 0.6 s | $0.0001 | advisor: no
plan     -> frontier tier, high eff. | 5,400 tok| 14 s  | $0.082  | advisor: yes
```

**6. Record cost and latency in a results table.** Create `orchestrator/ROUTING_NOTES.md` and write a small before-and-after style table: for each of the two tasks, the tier, effort, tokens, latency, and your computed cost. Add one sentence on *why* the policy routes each task the way it does. This is your evidence that the policy spends frontier money only where it earns it.

**7. Commit the component.** Save your work to git so it becomes a real, permanent part of AtlasOS:

```text
git add orchestrator
git commit -m "Add orchestrator routing policy: tier + effort per task, advisor strategy"
git push
```

**8. Stretch (optional).** Add a `confidence` input: if the cheap executor returns low confidence on a normally-cheap task, escalate to the advisor even though the task type alone would not. That turns the advisor rule from "by task type" into "by task type *or* by stakes," which is closer to how a real orchestrator decides.

### How you will know you are done

- ✅ An `orchestrator/` folder exists in your repo with `models.py` and `routing.py`.
- ✅ `route("classify")` returns a small tier at low effort; `route("plan")` returns the frontier tier at high effort with `use_advisor` true.
- ✅ You ran two contrasting tasks and recorded model, tokens, latency, and cost for each in `ROUTING_NOTES.md`.
- ✅ The advisor is consulted on the hard task and *not* on the trivial one.
- ✅ The whole thing is committed and pushed to GitHub.

> 💡 **Why one tiny function matters.** This policy is the seed of Atlas, your orchestrator. Every later unit that adds an agent will route its calls through a decision exactly like this one. Getting the shape right now, explicit, measured, cheap-by-default, pays off across the whole fleet.

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
THREE TIERS (every provider has them)
  small    -> fast, cheap   (classify, extract, summarize)
  mid      -> balanced      (drafting, everyday work)
  frontier -> most capable  (hard reasoning, the advisor)

THE METRIC
  cost per SUCCESSFUL OUTCOME, not per token
  = total spend (all turns + retries) / number of correct results
  smaller is NOT always cheaper: fewer turns can win.

REASONING IS A DIAL, NOT A SWITCH
  thinking OFF deletes a capability; it does not "reduce effort"
  keep thinking available; control with the EFFORT dial
  low ... latency-bound, not intelligence-bound (classify/summarize/extract)
  high .. needs any real intelligence (the safe default)
  max ... hardest tasks only; diminishing returns

THE EFFORT/THINKING LEVER, BY PROVIDER (verify current docs)
  Claude : adaptive thinking + effort=low..max
  Gemini : thinking budget (token allowance) / auto
  GPT    : reasoning_effort=low|medium|high

ADVISOR STRATEGY
  cheap model EXECUTES the routine turns
  expensive model ADVISES only on hard/risky steps
  escalate by task type, confidence, or stakes -> not by default

ROUTING POLICY (one place to decide)
  task type -> {tier, effort, use_advisor}
  model ids live in ONE file; change once when they drift
```

## How this connects to the rest of the course

- **Next, Unit 5 (Tools and MCP):** you give your agent real tools to act in the world. Routing decides *which model* runs each tool-using step, so the two fit together directly.
- **Later, Unit 9 (Evals):** you build Warden, the harness that grades outputs. That is what lets you right-size tiers and effort by measurement instead of by rule of thumb, and re-check quality every time you cut cost.
- **Throughout:** this routing policy is the first real piece of Atlas, the AtlasOS orchestrator. Every agent you add later (Scout, Forge, Pulse) routes its model calls through a decision like the one you just wrote.

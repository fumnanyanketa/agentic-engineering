# Unit 0: Foundations and the Mental Model

> **Course:** Agentic Engineering with Claude, a self-paced path *(working title)*
> **Unit 0 of 11:** Foundations: the right mental model, how LLMs actually work, and where capability is going
> **Sources fused:** Agentic Engineering Modules 00–01 (principles) + Building with Claude Module 0 pre-flight and Module 1 Lessons 1–2 (implementation)
> **Estimated time:** 90 to 120 minutes (read plus the build)

---

## In one sentence

You are not programming the model, you are engineering the environment around a capable but fallible reasoner so it can succeed, and this unit gives you the three things that make that possible: the right mental model (design the workplace, not the brain), exactly enough of how LLMs actually work (tokens, prediction, context, sampling), and a clear picture of where capability is going (an exponential you build *ahead* of, not behind).

> 🎯 **Where this unit is heading.** The payoff is a **Build** that doubles as your launchpad: a working, authenticated environment that makes its first measured model call, streams the response, counts tokens, validates structured output, and runs a tiny temperature-and-model experiment, all committed to your AtlasOS repo. Set it up once here and you never fight setup again. Jump to **"The Build"** to see the finish line.

## First-principles companion

> 💡 **The durable ideas behind this unit.** The Claude-specific framing is recent; the concepts are not. For the timeless versions:
>
> - **[Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361)** (paper). Why capability rises predictably as you scale model, data, and compute, the engine under "build for the next model."
> - **[Emergent Abilities of Large Language Models](https://arxiv.org/abs/2206.07682)** (paper). Why a model jumps from "can't" to "can" across a generation, the first-principles account of the capability curve.
> - **[The Bitter Lesson](https://en.wikipedia.org/wiki/Bitter_lesson)** (essay). General methods that leverage computation beat hand-built scaffolding over time, the basis for keeping your scaffolding thin.

## A few plain-language basics first

- **LLM (Large Language Model):** the kind of AI that reads and writes text. Claude is one. Treat it as a very capable, fallible text reasoner, not a program.
- **Token:** the unit a model reads and writes in (roughly three quarters of a word). You are billed per token, so more tokens means slower and pricier.
- **Context window:** how much text (in tokens) the model can hold in mind at once. Bigger is not always better; quality can degrade as it fills (**context rot**).
- **Inference vs training:** *training* builds the model (not your job here); *inference* is using it (your whole job here).
- **Agent:** an AI that takes a series of actions toward a goal (reading files, running code, fixing errors), not just answering once.
- **Scaffolding (or harness):** everything around the model: prompts, tools, loops, environment. The model is the engine; the scaffolding is the rest of the car.

You do not need to memorise these. Each returns the first time it matters.

## Why this unit matters

Most people meet LLMs as a chat box and form the wrong mental model: that you "tell the AI what to do" and it obeys, like a program. That model fails the moment you try to build something real. The professional frame is different and it is the foundation of everything else in this course:

> 🔑 **The whole craft in one line.** You are not programming the model. You are engineering its context and environment so that a capable but fallible reasoner can succeed. Prompting, context engineering, tools, memory, and evals are all just ways of designing that environment.

Get this frame right and the rest of the course is a set of techniques for the same goal. Get it wrong and you will spend months fighting the model instead of designing for it.

## Learning objectives

By the end of this unit you will be able to:

1. State and apply the core mental model: engineer the environment, not the model.
2. Explain, *exactly enough*, how an LLM works: tokens, next-token prediction, attention, the training stages, context windows, and sampling controls.
3. Describe where capability is going (capability exponential vs adoption linear) and the three concrete gains driving it (planning, error recovery, long-horizon coherence).
4. Apply the four habits for riding the curve: build for the next model, keep evals unsaturated, shrink scaffolding, and close the agent loop.
5. Stand up a working, measured environment and make your first instrumented model call.

## Prerequisites

- **Skills that matter:** comfortable reading/running Python, basic async/await, HTTP/REST and streaming, and git. (A short refresher list is in the Build.)
- **Skills you can defer:** model training, GPU kernels, backprop calculus. You build *on top of* foundation models, not reimplement them.

---

## Part 1: The mental model (engineer the environment)

The single most important shift: stop thinking "how do I instruct the model" and start thinking "how do I design the workplace where this reasoner does good work." That workplace has four parts you will spend the whole course building:

- **Instructions** (prompting): what you ask and how you frame it.
- **Reference material** (context engineering): the right information, in the smallest high-signal form.
- **Tools** (function calling, MCP): how the model acts on the world.
- **Validation** (evals): how you know the output is good.

> ❌ **A common mistake:** treating a wrong answer as a bug to be "instructed away" with ever more rules. Often the real fix is a different model, a tool, or better context, not a longer prompt. Diagnosing *which lever* is the skill.

A practical corollary you adopt today: **treat prompts as versioned software artifacts**, and **track tokens from day one** (for both cost and context budgeting). Both habits feed straight into the AtlasOS build.

---

## Part 2: How LLMs work, exactly enough

You do not need ML theory. You need a working model of the machine you are engineering around.

- **Tokens and tokenization.** Text is sliced into subword chunks ("cat", "ing", " the"). Tokens are the unit of pricing, memory limits, and latency. "Make it cheaper/faster" usually means "use fewer tokens."
- **Next-token prediction.** The model's entire function is to read the preceding text and predict the most probable next token, then repeat. It is, at heart, a very sophisticated autocomplete. It predicts sequences; it does not "think" in the human sense.
- **Self-attention / transformers.** The architecture lets the model weigh which earlier tokens matter for the next one (connecting "it" back to "the trophy"). This is why context quality matters so much.
- **The training pipeline (build time):** pretraining (broad knowledge from massive text), fine-tuning (task ability), and **RLHF** (human feedback for alignment and helpfulness). You consume the result; you do not run this.
- **Context window and context rot.** A fixed short-term memory measured in tokens. Bigger windows help but quality can degrade as they fill, so curation beats dumping.
- **Sampling controls.** **Temperature** (0 = predictable, high = creative) and **top-p** (nucleus sampling) trade consistency against diversity.

> 🔑 **Four mental models to keep.** (1) It is fancy autocomplete, not a mind. (2) Training builds, inference uses. (3) Every model choice trades capability against cost and latency. (4) Knowledge has a hard expiration date (the training cutoff), so connect it to fresh data with tools.

You will *feel* all of this in the Build, where you run the same prompt at three temperatures and across three model sizes and watch quality, latency, and cost move.

---

## Part 3: Where capability is going (and how to ride it)

Two trends define the moment. **Model capability is on an exponential**; **most teams adopt on a straight line.** The gap between the rising curve and the flat line is the opportunity, and closing it is the agentic engineer's job.

What specifically got better (not vague "models improved")? Three concrete gains:

1. **Planning before acting.** The model lays out a route instead of lurching step by step.
2. **Error recovery.** It notices a failure and corrects course instead of derailing.
3. **Long-horizon coherence.** It stays on task across long runs (minutes, now hours).

Together these three compound into **autonomy**: the plan → execute → verify loop that powers every agent you will build later. The unit of work shifts from *task* ("write this") to *outcome* ("keep this correct over time").

> 🔑 **Four habits for riding the curve.** (1) **Build for the next model**, not just today's. (2) **Keep evals harder than the model** so you can see the jump. (3) **Shrink your scaffolding** as the model gets smarter. (4) **Close the loop** so the agent verifies its own work. These recur in every later unit.

---

## Part 4: The craft ahead, and what you are building

The rest of the course is the environment-design craft, one layer per unit: the coding-agent workflow (Unit 1), prompting and context (2), model and reasoning levers (3), tools and MCP (4), retrieval and memory (5), workflows and agent patterns (6), multi-agent orchestration (7), evals and verification (8), and production (9), ending in the capstone (10).

Your north-star through all of it is **AtlasOS**: a self-improving operating system of cooperating agents you build one component per unit. This unit builds its foundation: the workstation and your first measured baseline.

---

## Key takeaways

1. **Engineer the environment, not the model.** Instructions, context, tools, validation: that is the whole craft.
2. **Know the machine exactly enough.** Tokens, next-token prediction, attention, context windows, sampling. Enough to engineer around, no more.
3. **Capability is exponential, adoption is linear.** Build *ahead* of the model; the gap is your opportunity.
4. **Three gains, four habits.** Planning, error recovery, long-horizon coherence; build for next model, unsaturated evals, thin scaffolding, close the loop.
5. **Measure from day one.** Tokens, cost, latency, quality. Prompts are versioned artifacts.

## Common pitfalls

- ❌ Treating the model as a program that obeys instructions, instead of a reasoner you design an environment for.
- ❌ Adding more instructions to fix a failure that actually needs a different model, a tool, or better context.
- ❌ Dumping everything into a huge context window and assuming bigger is better (context rot).
- ❌ Anthropomorphising: assuming the model "knows" or "thinks" rather than predicts.
- ❌ Optimising for today's model and freezing your design so the next jump passes you by.

---

## 🛠️ The Build: your workstation and first measured baseline

> The hands-on payoff. This fuses the two foundation labs (an authenticated, instrumented first call, and a temperature/model experiment) with the AtlasOS pre-flight, so you finish with a working environment *and* a real feel for the machine, all committed.

### What you will build

A working environment proven by three artifacts: a green tool check, a first **instrumented** model call (streamed, token-counted, schema-validated), and a small experiment table comparing temperatures and models.

### Milestones (in order, each stands alone)

1. **Green tool check.** Python 3.10+, git, and the Claude CLI all report a version. Create a virtual environment; store your API key in an environment variable or git-ignored `.env`. *(Full setup detail lives in the AtlasOS pre-flight reference.)*
2. **First instrumented call.** Install the SDK, send a prompt, **stream** the response, and print the **token counts** from the usage field. Seeing tokens makes cost and context budgeting concrete from day one.
3. **Validate structured output.** Ask for JSON and validate it against a small **Pydantic** schema. This is the "treat outputs as contracts" habit in miniature.
4. **Run the temperature-and-model experiment.** Send the same prompt at temperatures 0, 0.7, and 1.0 (a few runs each), then across a small, a mid, and a frontier model. Record **quality, latency, and cost** in a short table. Write two sentences on what you noticed.
5. **Commit it to AtlasOS.** Put the scripts and the experiment table in your repo and commit. This is the first artifact of your north-star build.
6. **Stretch.** Add a token-cost estimate per model; try the same prompt with and without a system message and note the difference.

### How you will know you are done

- ✅ `python3`, `git`, and `claude` all report a version.
- ✅ Your first call streams a reply and prints real token counts.
- ✅ JSON output validates against your Pydantic schema.
- ✅ Your experiment table shows quality/latency/cost across temperatures and models.
- ✅ It is committed to your AtlasOS repo.

> 💡 If any milestone felt shaky, that is your signal for which refresher (Python, async, git, HTTP/streaming) to spend an evening on before Unit 1.

---

## Cheat sheet

```text
THE MENTAL MODEL
  You engineer the ENVIRONMENT, not the model.
  Workplace = instructions + context + tools + validation.

THE MACHINE (exactly enough)
  tokens -> next-token prediction -> attention -> (pretrain/finetune/RLHF)
  context window (watch for rot) · temperature & top-p (consistency vs diversity)
  fancy autocomplete · training builds / inference uses · knowledge has a cutoff

WHERE IT'S GOING
  capability = exponential ; adoption = linear ; close the gap
  three gains: planning · error recovery · long-horizon coherence
  four habits: build for next model · unsaturated evals · thin scaffolding · close the loop

DAY-ONE HABITS
  measure tokens/cost/latency · prompts are versioned artifacts · pick the cheapest capable model
```

## How this connects to the rest of the course

- **Next, Unit 1 (The coding-agent workflow):** you set up Claude Code as the environment you build everything else *with*. Your measured baseline from this unit is the first thing it helps you extend.
- **Throughout:** every later unit is one more layer of the environment you started designing here, and one more AtlasOS component.

---

*Unit 0 of the combined path. Fuses the vendor-neutral principles of Agentic Engineering Modules 00–01 with the Claude-specific implementation of Building with Claude (pre-flight and the Foundations module). Adapt model ids and SDK details to the current docs.*

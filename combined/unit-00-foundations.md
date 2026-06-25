# Unit 0: Foundations and the Mental Model

> **Course:** Agentic Engineering, a model-agnostic self-paced path *(working title)*
> **Unit 0 of 11:** Install the one mental model that the whole course rests on (you engineer the environment, not the model), learn exactly enough about how LLMs work to fix their behaviour, and make your first measured model call across Claude, Gemini, and GPT
> **The how, across models:** Claude (Anthropic), Gemini (Google), GPT (OpenAI), current practice verified June 2026
> **AtlasOS build:** your launchpad (a first measured model call in Python) plus the AtlasOS charter
> **Estimated time:** 90 to 120 minutes

---

## In one sentence

This unit hands you the single idea the rest of the course leans on (your job is to build a good workplace for a capable but fallible helper, not to program the model line by line), gives you a simple but correct picture of what an LLM is actually doing under the hood (it predicts the next chunk of text, over and over), and then proves it with your own hands: you install Python, send your first model call, watch the reply stream in, read the token counts, check a structured answer, and run a tiny experiment, finishing by writing the charter for AtlasOS, the platform you build across the rest of the course.

> 🎯 **Where this unit is heading.** The payoff is a **Build** with two parts. First, a hand-held *first measured model call*: install Python, install one provider's SDK, set an API key, and run a small script that streams a reply, prints how many tokens it used, validates a small JSON answer, and runs a tiny temperature experiment. Second, you write the **AtlasOS charter**, a short document that says what you are building. Unit 0 comes before Unit 1 on purpose, so we keep setup light here (just enough for a first Python call). The full coding-agent workstation (editor, the coding agent, git and GitHub) is set up in Unit 1. Jump to **"The Build"** to see the finish line, then come back.

## First-principles companion

> 💡 **The durable ideas behind this unit.** The tools and model names change every few months; these ideas do not. All optional, read any time:
>
> - **[Andrej Karpathy, Intro to LLMs](https://codingscape.com/blog/andrej-karpathys-deep-dive-into-llms-video)** (talk). A clear, ground-up walk through what a large language model is and how it is trained.
> - **[Karpathy, Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html)** (course). Build the pieces (tokens, attention, training) yourself, from scratch, if you ever want the deep version.
> - **[Simon Willison, How I use LLMs to help me write code](https://simonwillison.net/2025/Mar/11/using-llms-for-code/)** (essay). The practitioner's grounding: LLMs are "fancy autocomplete," do not anthropomorphise them, and always remember the training cutoff.
> - **[Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361)** and **[Emergent Abilities of Large Language Models](https://arxiv.org/abs/2206.07682)** (papers). Why capability keeps rising predictably as models scale, and why a model can jump from "cannot do a task" to "can do it" in one generation.

## A few plain-language basics first

New terms, in plain words. You do not need to memorise these; each is explained again the moment it matters.

- **LLM (Large Language Model):** the kind of AI that powers chat assistants and writes text one small chunk at a time. "Large" means it learned from an enormous amount of text. Claude, Gemini, and GPT are all LLMs.
- **Model:** one specific version of an LLM, for example "Claude Opus" or "Gemini Flash." Different models differ in strength, speed, and price.
- **Agent:** an LLM that has been given the ability to take actions in a loop (call tools, read the result, decide what to do next) instead of answering once. The whole course builds toward agents; this unit is the foundation under them.
- **Token:** a small chunk of text, usually a piece of a word, like "cat", "ing", or " the". Models read and write in tokens, and tokens are how usage, cost, and memory limits are all measured.
- **API (Application Programming Interface):** a way for your code to talk to a remote service. You send a request, you get a response. You reach every model provider through an API.
- **API key:** a secret, password-like string that authorises your requests and bills them to your account. Treat it like a password; never paste it into code you might share.
- **SDK (Software Development Kit):** a small code library you install so your program can call a provider in a few lines instead of building the web request by hand.
- **Environment variable:** a value your terminal holds in memory (for example `ANTHROPIC_API_KEY`) that programs can read without the secret being written into your code.
- **Streaming:** receiving the reply token by token as it is generated, instead of waiting for the whole thing at the end.
- **Inference:** using a finished model to get an answer. Every time you send a prompt and get a reply, that is inference. (Contrast with *training*, when the model is being built.)

## Why this unit matters

Everything later in this course (prompting, tools, retrieval, evals, agents) is one facet of a single job: setting up a good workplace for a capable but forgetful helper. If you install that one idea now, the rest of the course stops feeling like a pile of unrelated tricks and starts feeling like variations on one theme. And you cannot engineer that workplace well if you have a wrong picture of what the helper actually is, so we spend a little time getting the mental model right and proving it with a real, measured call.

> 🔑 **You are not programming the model. You are engineering its context and its environment so that a capable but fallible reasoner can succeed.** Hold this sentence. It is the through-line of the entire course.

## Learning objectives

By the end of this unit you will be able to:

1. State, in your own words, the "give the model a good workplace" mental model, and explain why it reframes almost every later topic.
2. Explain, to a smart non-engineer, what a token is, what next-token prediction means, why context is finite, and what temperature does.
3. Describe how a model is built (pretraining, fine-tuning, RLHF) just well enough to reason about its limits, including the training cutoff.
4. Explain why capability is on an exponential while adoption is on a line, and what "build for the next model" means in practice.
5. Make a first, measured model call in Python against Claude, Gemini, or GPT: stream a reply, read token counts, validate a small structured output, and run a tiny temperature or model experiment.
6. Write the AtlasOS charter that anchors every later Build.

## Prerequisites

- **What you need:** a computer (Windows, macOS, or Linux), an internet connection, and the ability to read a short Python script and roughly follow it. That is genuinely it.
- **What you do NOT need:** a coding-agent setup, an editor, or git. Those arrive in Unit 1. For this unit you only need Python and one provider account, both set up together in The Build.
- **One honest note:** you will use a terminal in The Build. If you have never used one, that is fine; we explain every command and you cannot break anything by typing one wrong.

---

## Part 1: The one mental model (engineer the environment, not the model)

Here is the idea to carry through the entire course. Picture the model as a smart, fast new teammate who joined this morning. They are widely read and quick. But they have no memory of yesterday, they cannot see your screen, and when information is missing they will confidently guess rather than say "I do not know." Your job is not to rewire that teammate's brain. Your job is to set up their desk: the right instructions, the right reference material on hand, the right tools, and a way to check the work.

That reframing matters because almost everything later in this course is one facet of this single job:

```text
   THE WORKPLACE YOU BUILD            THE COURSE TOPIC IT BECOMES
   ───────────────────────           ───────────────────────────
   clear instructions on the desk  → prompting              (Unit 2)
   the right reference material    → context engineering    (Unit 2)
   the right tools to hand         → tool use / MCP         (Unit 4)
   a desk that stays stocked       → retrieval & memory     (Unit 5)
   a way to check the output       → evals & verification   (Units 3, 8)
   a teammate who acts in a loop   → agents & orchestration (Units 6, 7)
```

So when something goes wrong, the first question is almost never "is the model broken?" It is "what was missing or confusing in the workplace I built?" Most of the craft of this field is managing what the model can see and what it can do.

> 🔑 **The durable reframing.** You are engineering context and environment so a capable but fallible reasoner can succeed. Prompting, tools, memory, and evals are all just facets of building that workplace.

> ❌ **The beginner trap:** treating the model as a normal program that should behave identically every time, and reaching into its "brain" to fix a bad answer. You do not have access to its brain. You have access to its desk. Fix the desk.

> 💡 **A second habit to start now:** never just read, always build. This whole course is designed so every unit ends in something you made and can run. Reading about a token is forgettable; printing your own token count is not.

---

## Part 2: How an LLM works, exactly enough

You do not need to write a research paper. You need a picture accurate enough to predict and fix behaviour. These ideas are vendor-neutral: they are true no matter whose model you use.

### Tokens and next-token prediction

Before a model can read what you typed, it slices your text into **tokens**, small chunks that are usually a piece of a word ("cat", "ing", " the", where the leading space counts too). This slicing is called **tokenization**. You do not need to know the algorithm; you need to know that the token is the unit everything is measured in. You are billed per token, the model's memory limit is counted in tokens, and more tokens means a slower, costlier response.

At its core the model does one tiny thing, over and over: it reads all the text so far and predicts the single most likely next token. Then it adds that token to the text and predicts the next one. What looks like "thinking" or "writing" is this one small step, repeated thousands of times.

```text
   "The capital of France is" ──▶ [model] ──▶ most likely next token: " Paris"
   "The capital of France is Paris" ──▶ [model] ──▶ next token: "."
   ... and so on, one token at a time, until it decides to stop.
```

Holding on to this fact ("it is predicting the next token") explains most of what you will run into later, including why a model can sound completely sure while being completely wrong.

### Attention, in one breath

Nearly all modern LLMs are built on a design called a **transformer**. Its key trick is **self-attention**: as the model reads, it decides which earlier words matter most for predicting the next one. To finish "The trophy did not fit in the suitcase because it was too big," attention helps the model connect "it" back to "trophy." You only need this intuition, not the maths.

### How a model is built (and why it has a cutoff)

A model is created in stages:

- **Pretraining** is the first and largest stage. The model reads a huge amount of text and gets good at next-token prediction. Most of its raw knowledge comes from here.
- **Fine-tuning** is a smaller follow-up stage on more specific examples, to make it better at a task or style, such as following instructions.
- **RLHF (Reinforcement Learning from Human Feedback)** means people rate the model's answers and the model is nudged toward the kinds of answers people prefer. This is much of where "good behaviour" (often called **alignment**) comes from.

Two words people mix up: **training** is when the model is built (the stages above); **inference** is when you use the finished model to get an answer. Every prompt you send is inference.

One practical consequence: a model has a **training cutoff**, the date after which it learned nothing new. If a library or a fact changed after that date, the model simply will not know, and (because it predicts plausible text) it may confidently invent something. As Simon Willison puts it, do not anthropomorphise the model, and always remember the cutoff.

### The context window (and context rot)

The **context window** is the model's short-term working memory: the most text, counted in tokens, it can look at in a single request. Anything beyond that has to be left out. Today's frontier models hold a great deal (up to roughly a million tokens), but a bigger window is not free. Cramming in too much can actually *hurt* quality, an effect people call **context rot**: the model gets distracted by the noise and loses the signal. You learn to manage this deliberately in Unit 2 and Unit 5. For now, the takeaway is: context is finite and precious, so put the right things in it, not everything.

### Sampling controls: temperature

When the model picks the next token, you can tune how adventurous it is. The main dial is **temperature**:

- **Low temperature** (such as 0) makes it play safe and almost always pick the most likely token, so answers come out steady and repetitive.
- **Higher temperature** makes it take more chances, so answers are more varied and creative.

A useful warning: low temperature means *less varied*, not *more correct*. A confident, low-temperature answer can still be wrong. (A related dial, **top-p** or *nucleus sampling*, limits the model to the smallest group of top choices whose probabilities add up to a fraction p; you will meet it again later. Note that some of the newest reasoning models manage this internally and do not expose a temperature dial at all, which is exactly why we hold model details loosely and check current docs.)

> 🔑 **Tokens explain the economics; next-token prediction explains the behaviour.** If you remember only two things from this part, remember those two.

---

## Part 3: The same picture across Claude, Gemini, and GPT

The ideas in Part 2 hold for every provider, because they are all transformers trained in similar stages. What differs is the labels and the price list, not the physics. Here is the same picture in three columns so you are never locked to one vendor.

| | **Claude** (Anthropic) | **Gemini** (Google) | **GPT** (OpenAI) |
|---|---|---|---|
| What it is | a transformer LLM | a transformer LLM | a transformer LLM |
| You reach it via | the Anthropic API + SDK | the Google AI / Gemini API + SDK | the OpenAI API + SDK |
| Tiers (small → frontier) | Haiku → Sonnet → Opus | Flash → Pro (and up) | mini → flagship |
| Counts you get back | input/output token usage | token usage | token usage |
| Get a key from | console.anthropic.com | aistudio.google.com | platform.openai.com |
| Model ids change often | yes, verify in docs | yes, verify in docs | yes, verify in docs |

> 💡 **Choosing a tier is an engineering decision you make constantly.** A handy picture is a ladder: a large "frontier" model at the top (most capable, slowest, priciest), a small fast cheap model at the bottom, and a balanced option in the middle. The discipline, taught hard in Unit 3, is to pick the cheapest model that still meets your quality bar, and to measure rather than assume. (One term: **latency** just means how long you wait for a response.)

> ✅ **Hold model ids loosely.** Names, tiers, and prices shift every few months. Whenever this course writes a specific model id, treat it as a placeholder and confirm the current one in the provider's docs. The durable skill is the workflow, not the string.

---

## Part 4: Where capability is going (exponential vs linear)

One last idea before we build, because it changes how you design. Model **capability** is rising on an exponential curve: each generation is a bigger jump than the last. Most organisations, by contrast, **adopt** AI on a straight line: slow and steady. The space between the rising curve and the flat line is the gap, and closing it is the developer's job. As the model gets stronger, your starting line moves forward.

What specifically keeps improving? Three things worth naming, because the rest of the course leans on them:

- **Planning before acting.** Newer models read and plan first, and catch their own mistakes mid-plan, instead of jumping in and failing.
- **Error recovery.** Older models would "doom loop," declaring "fixed!" and retrying the same broken thing. Newer ones read the failure, reason about *why*, and change approach.
- **Long-horizon coherence.** Models used to "lose the plot" partway through a long task. Now they can stay on track across very long runs, which is why agents that ran for minutes a year ago now run for hours.

```text
   capability  ╱  (exponential: planning, error recovery, long-horizon coherence)
              ╱
             ╱        the GAP  ◀── the developer's job to close
            ╱   ______________
           ╱___/   adoption (linear: most orgs crawl in a straight line)
          time ▶
```

These three gains stack into **autonomy**, expressed as a simple loop the agent runs on its own: plan, then act, then verify, and loop back if the check fails. You will meet that loop again as the heartbeat of Unit 1.

> 🔑 **Build for the next model, not just today's.** Keep your scaffolding (your prompts, tools, and workarounds) thin, so that when the model gets smarter your system absorbs the jump instead of being held back by patches written for a weaker model. Verification is the part that stays scarce and valuable: as building gets cheap, *checking* becomes the bottleneck.

> ❌ **A common mistake:** piling on more instructions and more guardrails every time something fails, until you have a giant fragile prompt full of workarounds for models that no longer exist. As models improve, old prompt lines quietly become bugs.

---

## Key takeaways

1. **One mental model rules them all:** you engineer the environment, not the model. Prompting, tools, memory, and evals are all facets of building the model a good workplace.
2. **An LLM predicts the next token, over and over.** That single fact explains confident wrong answers, the finite context window, and the training cutoff.
3. **Tokens are the unit of everything:** cost, the memory limit, and speed. Watch them from day one.
4. **The picture is the same across Claude, Gemini, and GPT.** Only the labels and prices differ; hold model ids loosely and verify in current docs.
5. **Capability is exponential, adoption is linear.** Build thin scaffolding for the next model, and treat verification as the scarce skill.

## Common pitfalls

- ❌ Treating the model as a deterministic program that should answer identically every time, then being surprised when it does not.
- ❌ Anthropomorphising the model: assuming it "knows" it is unsure. It does not; it predicts plausible text, including plausible nonsense past its cutoff.
- ❌ Ignoring token counts until a surprise bill or a context-limit error arrives.
- ❌ Reaching reflexively for the biggest, most expensive model instead of measuring whether a cheaper one clears your bar.
- ❌ Hard-coding a model id from this page into a permanent script; names change, so verify against current docs.
- ❌ Pasting an API key directly into your code, which leaks it the moment the file is shared. Use an environment variable.

---

## 🛠️ The Build: your launchpad (a first measured model call) and the AtlasOS charter

> The hands-on payoff. By the end you will have made your first real model call in Python, watched it stream, measured its tokens, checked a structured answer, run a tiny experiment, and written the charter for AtlasOS, the platform you build a piece of in every later unit.

### What you will build

Two artifacts. First, a working Python script (`first_call.py`) that authenticates to one provider, streams a reply to your screen, prints the token usage, validates a small JSON output, and runs a tiny temperature or model experiment. Second, a short written document, `atlas/CHARTER.md`, that states what AtlasOS is and what "done" looks like.

> 💡 **Keep setup light here.** You only install what a first Python call needs: Python, one SDK, and an API key. The full coding-agent workstation (VS Code, the coding agent, git and GitHub) is set up in **Unit 1**, so do not worry about any of that yet. When you see a grey box below, that is something you type into your terminal and press Enter. Lines starting with `#` are comments, not commands.

### Milestones (in order, each fully explained)

**1. Install Python (3.10 or newer).**
   - Go to **[https://www.python.org/downloads](https://www.python.org/downloads)** and download the installer for your system (macOS or Windows). On Linux, Python is usually present, or install it with your package manager (for example `sudo apt install python3 python3-pip` on Debian/Ubuntu).
   - On Windows, during install tick **"Add Python to PATH"** so your terminal can find it.
   - Open a terminal (on Windows, "Terminal" or "PowerShell"; on macOS, "Terminal"; on Linux, your usual one) and prove it worked:

```text
# Ask Python and its installer, pip, to report their versions.
python3 --version
pip3 --version

# What you'll see (your numbers may differ, that's fine):
Python 3.12.4
pip 24.0
```

   If you see two version numbers, you are set. (On Windows, you may need to type `python` and `pip` instead of `python3` and `pip3`.)

**2. Make a tidy project folder and install one provider's SDK.** Pick the provider whose account you have or are happy to create. You only need one.

```text
# Make a folder for this unit's work and move into it.
mkdir atlas-launchpad
cd atlas-launchpad

# Install the SDK for your chosen provider (pick ONE line):
pip3 install anthropic         # Claude (Anthropic)
pip3 install google-genai      # Gemini (Google)
pip3 install openai            # GPT (OpenAI)

# We'll also use Pydantic to check structured output later:
pip3 install pydantic
```

**3. Get an API key and set it as an environment variable.** Create a key in your provider's console, add a little billing credit, and store the key in your terminal session. Never paste a key into your code.

```text
# Claude:  get a key at https://console.anthropic.com
export ANTHROPIC_API_KEY="sk-ant-...your key..."

# Gemini:  get a key at https://aistudio.google.com
export GEMINI_API_KEY="...your key..."

# GPT:     get a key at https://platform.openai.com
export OPENAI_API_KEY="sk-...your key..."
```

   (On Windows PowerShell, use `setx NAME "value"` and then open a new terminal, or `$env:NAME="value"` for the current session.)

**4. Write `first_call.py` and stream your first reply.** Create a file called `first_call.py` in your folder, paste the version for your provider, and run it with `python3 first_call.py`. Each version sends the same prompt, streams the reply to your screen as it arrives, and then prints the token usage. **Model ids change often, so the ones below are placeholders: verify the current id in your provider's docs and swap it in.**

```text
# --- Claude (Anthropic) ---
import os
from anthropic import Anthropic

client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment

with client.messages.stream(
    model="claude-haiku-4-5",          # cheapest tier; verify current id in docs
    max_tokens=300,
    messages=[{"role": "user", "content": "In two sentences, what is an AI agent?"}],
) as stream:
    for text in stream.text_stream:    # tokens arrive as they're generated
        print(text, end="", flush=True)
    final = stream.get_final_message()

print("\n\n--- usage ---")
print("input tokens: ", final.usage.input_tokens)
print("output tokens:", final.usage.output_tokens)
```

```text
# --- Gemini (Google) ---
import os
from google import genai

client = genai.Client()  # reads GEMINI_API_KEY from the environment

stream = client.models.generate_content_stream(
    model="gemini-flash-latest",       # a fast tier; verify current id in docs
    contents="In two sentences, what is an AI agent?",
)
final = None
for chunk in stream:                   # tokens arrive as they're generated
    print(chunk.text, end="", flush=True)
    final = chunk

print("\n\n--- usage ---")
print("usage metadata:", final.usage_metadata)  # includes prompt + output token counts
```

```text
# --- GPT (OpenAI) ---
import os
from openai import OpenAI

client = OpenAI()  # reads OPENAI_API_KEY from the environment

stream = client.responses.create(
    model="gpt-5-mini",                # a small tier; verify current id in docs
    input="In two sentences, what is an AI agent?",
    stream=True,
)
for event in stream:                   # tokens arrive as they're generated
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
    if event.type == "response.completed":
        print("\n\n--- usage ---")
        print("usage:", event.response.usage)  # prompt + output token counts
```

   Seeing words appear one chunk at a time, followed by token counts, means your key, billing, and SDK all work, and you have *felt* both next-token prediction and the token-as-unit idea from Part 2.

**5. Validate a small structured (JSON) output.** Models can return free text, but for real systems you usually want a checked, machine-readable shape. Ask for JSON and validate it with Pydantic, so a wrong shape is rejected instead of silently breaking your program later. Add this to a second file, `structured.py`, adapting the client line to your provider:

```text
import json
from pydantic import BaseModel

# The shape we demand back. If the model returns the wrong shape, this fails loudly.
class Capital(BaseModel):
    country: str
    capital: str
    population_millions: float

prompt = (
    "Return ONLY JSON, no prose, with keys "
    "country, capital, population_millions for France."
)

# --- get raw text from your provider (one example: Claude) ---
from anthropic import Anthropic
client = Anthropic()
msg = client.messages.create(
    model="claude-haiku-4-5",           # verify current id in docs
    max_tokens=200,
    messages=[{"role": "user", "content": prompt}],
)
raw = msg.content[0].text

# Validate. If the JSON is malformed or the shape is wrong, this raises an error.
data = Capital.model_validate(json.loads(raw))
print("validated:", data)
```

   If it prints a validated object, you have proven the full loop: authenticate, call, and get a *checked* structured result. (Gemini and OpenAI expose first-class structured-output options too; the durable idea is the same across all three: you describe the shape you want and validate what comes back.)

**6. Run a tiny temperature or model experiment.** Now feel a trade-off from Part 2 with your own eyes. Send the *same* creative prompt (for example, "Give me a one-line name for a coffee shop") three times at temperature 0 and three times at a higher temperature like 1.0, and notice how much more the answers vary at the higher setting. If your chosen model does not expose temperature, run the *same* prompt on a small model and a larger model instead, and note the difference in answer quality, speed, and (from the usage counts) cost.

```text
# Sketch (Claude shown; adapt the client + temperature field to your provider):
for temp in (0.0, 1.0):
    print(f"\n=== temperature {temp} ===")
    for _ in range(3):
        msg = client.messages.create(
            model="claude-haiku-4-5",   # verify current id in docs
            max_tokens=30,
            temperature=temp,
            messages=[{"role": "user",
                       "content": "Give me a one-line name for a coffee shop."}],
        )
        print("-", msg.content[0].text.strip())
```

   Low temperature should give you nearly the same answer each time; high temperature should give you variety. That is the dial from Part 2, made real.

**7. Write the AtlasOS charter.** This is the throughline of the whole course. Make a folder named `atlas` and inside it a file `CHARTER.md`. Using the AtlasOS company brief as your source of truth, write a short charter (half a page is plenty) that answers: what is AtlasOS, who is it for, and what does "done enough to be proud of" look like. Here is a starter you can adapt:

```text
# AtlasOS Charter

## What it is
AtlasOS is a self-improving operating system of cooperating AI agents that runs
knowledge work end to end. You hand it an outcome; a fleet of specialised agents
plans, executes, verifies itself, remembers, and improves over time, with a human
in the loop for the decisions that matter.

## The fleet (named roles I will build, one per unit)
- Atlas  - the orchestrator: decompose a goal, dispatch agents, escalate to me.
- Scout  - research and synthesis.    - Forge  - the builder (writes/ships code).
- Pulse  - analytics.    - Herald - comms and reporting.    - Cortex - shared memory.
- Warden - review, safety, and evals (nothing ships past it).

## Design principles
- Build for the NEXT model: keep scaffolding thin; trim guardrails as models improve.
- Verification is the bottleneck: Warden (evals) is a first-class citizen, not an afterthought.
- Outcomes over tasks: own a result over time, not "do this one thing once."
- Cost per successful outcome, not cost per token.

## Definition of done (the hero outcome)
I can give Atlas a high-level outcome and the fleet executes it end to end, every
output is graded by Warden, the system remembers across runs (Cortex), it runs on
real infrastructure, and at least one flagship use case works for real.
```

**8. Stretch (optional).** Re-run `first_call.py` with a much larger `max_tokens` and a much smaller one, and watch the reply length and the output-token count change together. Or install a second provider's SDK and run the same prompt against it, comparing the answers and the token counts side by side. That is your first taste of being model-agnostic.

### How you will know you are done

- ✅ `python3 --version` and `pip3 --version` both print version numbers.
- ✅ `first_call.py` streams a reply to your screen and then prints input and output token counts.
- ✅ `structured.py` prints a validated object (and raises a clear error if you deliberately break the JSON).
- ✅ You ran the temperature (or model) experiment and can describe, in one sentence, the trade-off you saw.
- ✅ `atlas/CHARTER.md` exists and says what AtlasOS is, who it is for, and what "done" looks like.

> 💡 **If any step felt shaky, that is normal and useful.** Note which one. The most common snags are a key not set in the current terminal (re-run the `export` line), an out-of-date model id (verify it in the provider docs), or `python3` vs `python` on Windows (try the other one). Reaching for help should be about going deeper, not decoding confusion: the steps here are meant to be complete.

---

## Cheat sheet

```text
THE ONE MENTAL MODEL
  You engineer the ENVIRONMENT, not the model.
  prompting / context / tools / memory / evals  = facets of "build a good workplace"

HOW AN LLM WORKS (exactly enough)
  token .......... small chunk of text; the unit of cost, memory, and speed
  prediction ..... it predicts the NEXT token, over and over (that's all)
  attention ...... it weighs which earlier words matter for the next one
  built by ....... pretraining -> fine-tuning -> RLHF ; then INFERENCE when you use it
  cutoff ......... it knows nothing after its training date (it will still guess)
  context window . finite short-term memory in tokens ; too much -> "context rot"
  temperature .... low = steady/repetitive ; high = varied  (low != correct)

SAME PICTURE, THREE PROVIDERS (hold ids loosely; verify in docs)
  Claude (Anthropic) : console.anthropic.com  | Haiku -> Sonnet -> Opus
  Gemini (Google)    : aistudio.google.com    | Flash -> Pro
  GPT    (OpenAI)    : platform.openai.com     | mini -> flagship

WHERE IT'S GOING
  capability = exponential (planning, error recovery, long-horizon coherence)
  adoption   = linear ; closing the gap is your job ; build for the NEXT model
  verification is the scarce skill

FIRST MEASURED CALL (Python)
  python3 --version ; pip3 install <sdk> pydantic
  export <PROVIDER>_API_KEY="..."   (never put the key in code)
  stream the reply -> read usage.tokens -> validate JSON -> tiny temp/model experiment
```

## How this connects to the rest of the course

- **Next, Unit 1 (The coding-agent workflow):** you set up the full workstation (editor, a coding agent, git and GitHub) and learn the plan, act, verify loop, the autonomy gained from the three capability gains you met in Part 4. That is where the heavy one-time setup lives; this unit deliberately kept it light.
- **Soon, Unit 2 (Prompting and context engineering):** the "good workplace" idea from Part 1 becomes concrete craft, clear instructions on the desk and the right reference material in the finite context window.
- **Soon, Unit 3 (Model and reasoning levers):** the "pick the cheapest model that clears the bar" discipline from Part 3 becomes a rigorous "cost per successful outcome" method.
- **Throughout:** every later unit adds one named component to AtlasOS, the platform whose charter you just wrote. This unit is the launchpad; the rest is the flight.

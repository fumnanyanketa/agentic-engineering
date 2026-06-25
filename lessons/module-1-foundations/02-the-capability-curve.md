# Module 1 · Lesson 2: The Capability Curve

> **Course:** Building with Claude, a self-paced course
> **Module 1:** Foundations: why it matters and where capability is going
> **Speaker:** Jeremy, Product Manager on the research team, Anthropic
> **Source talk:** [The capability curve](https://www.youtube.com/watch?v=DNRddIEoH3c) · [full transcript](../../transcripts/code-with-claude-2026-london-2026/06_the-capability-curve.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

Claude has gone from a junior engineer who could solve a fraction of coding tasks to a near-senior one in twelve months, driven by three concrete gains (planning before acting, recovering from failure, and staying coherent over very long runs), and the way to benefit is to ride the curve: keep trustworthy evals, shrink your scaffolding, and give the model room to work.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you build a small harness called **CurveRider** that lets you swap models, run an eval, and prove a newer model is actually better on a task that matters to you. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section near the end, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[Emergent Abilities of Large Language Models](https://arxiv.org/abs/2206.07682)** (paper). Explains why a model can jump from "can't do a task" to "can do it" across one generation, the first-principles account of the capability curve.
> - **[Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361)** (paper). The smooth-scaling mechanism underneath the discrete capability jumps.

## A few plain-language basics first

This lesson uses some everyday AI and engineering terms. Here they are in plain words:

- **LLM (Large Language Model):** the kind of AI that reads and writes text. "Claude" is an LLM.
- **Model:** one specific version of the AI, for example "Opus 4.7," "Sonnet 4," or "Mythos preview." Different models differ in strength, speed, and price.
- **Agent:** an AI that takes a series of actions on its own toward a goal (reading files, running code, fixing errors), rather than answering in one shot.
- **Token:** the unit a model reads and writes in, roughly three quarters of a word. You are billed per token, so "more tokens" means "slower and more expensive."
- **Tool / tool call:** a piece of code the model can choose to run, for example to run tests or read a file. When the model decides to use one, that is a **tool call**, and what comes back is the **tool result**.
- **Benchmark:** a standard, shared test used to compare models. **SWE-bench Verified** is a famous one made of real GitHub issues.
- **Eval (evaluation):** your own set of test cases that measures whether a model does what your application needs. Think of evals as the unit tests of the AI era.
- **Saturated:** an eval is "saturated" when there is no room left to improve on it (the model already gets nearly everything right), so it can no longer tell a better model from a worse one.
- **Scaffolding (or harness):** everything around the model: prompts, tools, the execution environment, skills, loops. The model is the engine; the scaffolding is the rest.
- **Test-time compute:** extra "thinking" a model does before answering. More thinking usually means a better answer at the cost of more tokens and time.
- **Context window:** how much text (measured in tokens) the model can hold in mind at once. Today's frontier models hold up to about a million tokens.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

The opening keynote told you the curve exists. This lesson, from Jeremy on the research team ("how do we make Claude a better software engineer?"), tells you *what specifically got better* and *what to do about it*. That matters because vague awareness ("models are improving") does not change how you build. Knowing that planning, error recovery, and long-horizon coherence all improved, and knowing the four practices that absorb those gains, does change how you build, starting today.

In Jeremy's words, "the foundation under our feet is shifting as developers, and we have to adapt to that."

## Learning objectives

By the end of this lesson you will be able to:

1. Explain the curve concretely, using the SWE-bench jump (about 60% to 87% in a year) and the website-rebuild demo.
2. Describe the three capability gains driving the curve: planning before acting, error recovery, and sustained attention over long runs.
3. Explain how those three combine into **autonomy** and the long-horizon agent loop (plan, execute, verify).
4. Apply the four practices for riding the curve: build trustworthy unsaturated evals, shrink scaffolding, give the model room to work, and close the agent loop.

## Prerequisites

- Module 1 · Lesson 1 (the Opening Keynote), which introduces the exponential and the idea of riding it.
- No coding required to read the lesson, but the Capstone assumes you can make a basic API call (covered in Module 2 · Lesson 1).

---

## Part 1: how far the curve has moved

Jeremy opens with a contrast. A year ago, Opus 4 was state of the art and Claude Code had just barely launched. Today, in his words, "Opus 4 is a dinosaur, almost a distant memory." To make the change vivid he polls the room and finds that nearly half have shipped a PR in the last week written mostly by Claude, and several have shipped one where they "did not read the code at all."

> 💡 He is honest about that last one: "It's a dangerous game to do this, and you have to do it carefully and do it well." Not reading the code only works when something else (good tests, good verification) checks the work for you. Hold onto that idea; it returns in Part 3.

### The benchmark jump

The clearest number is **SWE-bench Verified**, a benchmark built from real GitHub issues. It asks a simple question: can the model solve the issue and pass all the tests?

| Model (about a year apart) | SWE-bench Verified score |
|---|---|
| Sonnet 3.7 | about 60% |
| Opus 4.7 | 87% |

That is roughly three times more issues solved. The frontier models have moved so far that, as Jeremy notes, "we don't even use SWE-bench Verified anymore" for the top models, because **Mythos preview** has completely **saturated** it (no room left to improve). Progress is now outrunning the benchmarks built to measure it.

> 🔑 **A benchmark you have beaten is a ruler you can no longer read with.** Once a model scores near the top of a test, that test stops telling you which model is better. This is the single most important practical idea in the lesson, and Part 4 turns it into a habit.

### Even better than a benchmark: a demo

Jeremy shows the same task to two models a year apart: "Rebuild the entire Claude.ai website from scratch in one shot."

- **Sonnet 4:** jumps straight in, does not plan much, does not correct course, writes about 2,000 lines, and produces a basic UI where the chat does not actually work.
- **Opus 4.7:** uses tools, writes *fewer* lines (about 1,700), and produces a working app that looks like Claude.ai: a chat sidebar, chat history, formatted outputs, even mermaid diagrams, and it added dark mode "like a true developer."

> 💡 The detail worth noticing: the better model wrote **fewer** lines and got a **better** result. Capability is not "more output." It is more of the right output, with less waste.

---

## Part 2: the three gains driving the curve

This is the analytical heart of the talk. Three specific things improved.

### Gain 1: planning and reasoning before acting

Jeremy's analogy: Sonnet 3.7 acted "like I might act when making IKEA furniture. I just jump right into it, I start building, and then I look at the plan after I've already tried and failed." The old failure mode was **act first, think later**.

What changed: modern models plan on their own. They read before acting, compose a careful plan, investigate first, and catch their own mistakes while planning (you will see them say "actually" or "never mind" and change approach mid-plan).

> ✅ **What to do about it:** give the model time and room to plan. You usually do not need to force it with elaborate instructions. Often it is enough to select a high reasoning effort and let Claude develop the plan itself.

### Gain 2: error recovery and adapting to failure

A year ago, models suffered from **doom looping**: hitting a failure, announcing "I fixed it," and then trying the exact same broken solution again and again. As Jeremy puts it, "This problem essentially doesn't happen anymore."

Why it improved: the model now tries an action, reads the result from the environment (a **tool result**), spends some thinking tokens reasoning about *why* it failed, and then changes its approach instead of repeating it.

> ✅ **What to do about it:** give the model a way to get real feedback (run the tests, return the error) and a way to reason from it. "You get better task performance with fewer wasted tokens," because the model iterates instead of grinding.

### Gain 3: sustained attention over long agentic runs

A year ago, on a big refactor spanning hundreds of thousands of tokens, the model would "lose the plot" partway through: forget the spec, miss instructions, drift from the goal. Now models can "hold coherence up to 1 million tokens and even beyond."

> ✅ **What to do about it:** stop pre-chopping every task into tiny pieces. As Jeremy says, "you can hand it the whole code base and see what it can do, rather than sort of limiting your ambition before starting the task." Be more ambitious. (He is careful: coherence is much better, not yet perfect.)

> 🔑 **The three gains in one line.** Models now **plan** before they act, **recover** when they fail, and **remember** across very long runs. Each one alone is useful. Together they make something new, which is Part 3.

---

## Part 3: the gains stack into autonomy

The three gains are not separate features. They ladder up into **autonomy**: the ability to complete a task end to end without hand-holding.

```text
Plan in advance        ┐
Recover from failure   ├──>  AUTONOMY  ──>  end-to-end task completion
Stay coherent long     ┘
```

Autonomy expresses itself as the **long-horizon agent loop**: a repeating cycle the agent runs on its own.

```text
1. PLAN     ── decide how to accomplish the task
2. EXECUTE  ── start doing the work (write code, run commands)
3. VERIFY   ── check the work against the environment (run the tests)
        │
        ├─ tests fail? ── iterate, then back to EXECUTE
        └─ every few checkpoints ── validate against the overall goal
```

This is why agents that ran for minutes a year ago now run for hours.

### The Bun example: why verification is the unlock

Jeremy's favourite recent example. Jared, the founder of Bun (a core piece of infrastructure behind Claude Code), got tired of memory errors in Bun's JavaScript engine. He decided to rewrite the entire engine in Rust, a memory-safe language. He does not even know Rust.

The reason it worked: Bun already had a test suite with nearly 100% coverage. With that as a verifier, Jared had many Claude agents run for an entire week, iterating against the test suite until they reached almost a 100% pass rate. He merged the PR. Bun is now written in Rust. A task that would have taken months, done in a week by one person.

> 🔑 **Verification is the multiplier.** The agent could run for a week unsupervised only because the test suite told it, at every step, whether it was right. Remember Part 1: "shipping a PR you did not read" is only safe when something else verifies the work. Strong verification is what turns long-horizon capability into something you can actually trust.

> 💡 Customer signals point the same way: Vercel saw models write proofs on systems code *before* starting work (planning), Windsurf praised market-leading coherence over long runs (long horizon), and Shopify saw a step up in code quality and self-verification with Opus 4.7.

---

## Part 4: how to ride the curve (the part you act on)

Jeremy is explicit that this "is not really about any individual model." It is about the trajectory. Here are his four practices.

### Practice 1: build evals you can actually trust

An **eval** is your own set of test cases. Jeremy is blunt about their importance: "Evaluations are just the unit tests and the regression tests of the AI era. Every software application that uses AI should have evaluations." Not having them is like having no unit tests for ordinary software.

Four sub-points:

1. **Just start.** Teams treat evals as an academic project needing researchers. They do not. The first step is simply to build *some* form of eval. (Anthropic has an engineering-blog guide on how.)
2. **Measure what you actually care about.** Build evals from your *real* traffic and failure modes, not a generic academic benchmark. If you are building a finance agent, collect your customers' real failures, not SWE-bench scores.
3. **Know when your eval is saturated.** If Opus 4.7 already scores 90% and the last 10% is impossible or unfair, the eval is saturated and can no longer measure improvement. Some regression tests *should* stay at 100% (you expect every model to pass them), but the evals you use to *measure progress* must keep room to grow.
4. **Benchmark new models on them.** With trusted evals you "just kick off a script and see the eval results" instead of reading Twitter for vibes. Teams with evals adapt to new models fastest, and that is a real competitive advantage.

> 🔑 **The saturation trap (a real story from the talk).** Customers often run a new model on their old, saturated eval, see a 1% gain, and conclude "this model isn't that great." Then they test harder tasks for a week and realise the eval, not the model, was the problem. As Jeremy puts it, the model was great; "our eval is in the past." Keep raising the bar.

```text
EVAL HEALTH CHECK
  Does it match your real traffic? ........ if no, rebuild from real failures
  Can a better model still gain on it? .... if no, it's SATURATED -> make it harder
  Can you run it as a script in minutes? .. if no, automate it
```

### Practice 2: shrink your scaffolding over time

**Scaffolding** is everything around the model: prompts, tools, environment, skills. Jeremy describes a pattern everyone hits: "you develop this huge Frankenstein prompt." Each failure adds a line, and eventually you have 3,000 lines of instructions written for *old* models and for failures that may not even happen anymore.

When you get a new model, cut the prompt down. Describe what you actually *intend*, not how to work around an old model's quirks.

> 💡 **A concrete example from the talk.** During the Claude 4 launch, the Claude.ai prompt had an old example of a citation format the team no longer used. The newer model followed instructions so well that it obeyed that stale example and produced the wrong format. Changing a few characters "completely fixed that whole class of errors." As models get smarter, old prompt lines become bugs.

> ✅ **Use your evals to do this safely:** trim the system prompt toward the bare minimum, then re-run your eval. If the score holds, the cut was free.

### Practice 3: give the model room to work

Three parts:

- **Let it think when appropriate.** Frontier models are reasoning models; they benefit from **test-time compute** (extra thinking before answering). Allow **adaptive thinking** (the model chooses how much to think) and turn the **effort** parameter up for intelligence-sensitive work like software engineering, usually to the highest setting, accepting more token usage for more intelligence.
- **Let it operate autonomously, safely.** Letting a model touch production is scary; you do not want it deleting a cluster. The pattern that works is **auto mode**: in Claude Code, a prompted classifier checks every tool call and asks "is this safe to approve automatically, or does it need a human?" Almost every engineer at Anthropic runs auto mode, getting looped in only for critical or dangerous actions.
- **Close the agent loop.** Let your agents help improve your agents. If your system already has evals, you can point Claude Code at it and ask "how can I improve the prompt or the tools to raise this score?" Because Claude can run the agent *and* the eval itself, it can autonomously iterate toward a better system, "almost self-improving."

> 🔑 **"Give the model room" is the throughline.** Room to think (adaptive thinking, high effort), room to act (auto mode), and room to improve your system (closing the loop). All three trust a more capable model to do more, with the right guardrails.

```text
GIVE THE MODEL ROOM
  Think ....... allow adaptive thinking; raise effort for hard tasks
  Act ......... auto mode: auto-approve safe calls, escalate risky ones
  Improve ..... close the loop: let Claude run your agent + eval to tune them
```

---

## Key takeaways

1. **The curve is concrete, not vibes.** SWE-bench went from about 60% to 87% in a year; the website demo got better *and* shorter. Junior to near-senior in twelve months.
2. **Three gains drive it:** planning before acting, error recovery (no more doom looping), and coherence over very long runs (up to ~1M tokens).
3. **They stack into autonomy,** expressed as the plan-execute-verify loop, which is why agents now run for hours.
4. **Verification is the unlock.** The Bun rewrite worked because a near-100% test suite verified every step. Long-horizon capability is only trustworthy with strong verification.
5. **Ride the curve with four practices:** build trustworthy unsaturated evals, shrink your scaffolding, give the model room to work, and close the agent loop.

## Common pitfalls

- ❌ Judging a new model on a **saturated** eval, seeing a tiny gain, and wrongly concluding it is no better.
- ❌ Using an **academic benchmark** instead of an eval built from your real traffic and failure modes.
- ❌ Letting your prompt grow into a 3,000-line Frankenstein full of workarounds for models that no longer exist.
- ❌ Pre-chopping every task into tiny pieces out of habit, underestimating long-horizon coherence.
- ❌ Forcing low reasoning effort on intelligence-sensitive work to save tokens, and getting worse results.
- ❌ Running agents fully unsupervised on production with no auto-mode classifier and no verification.
- ❌ Shipping a PR you did not read with no test suite to verify it. Capability without verification is just risk.

---

## 🛠️ Capstone Project: build CurveRider

> This is the main hands-on project for the lesson. You will build a tiny harness that lets you *feel* the capability curve yourself by swapping models and watching a trusted, unsaturated eval respond. It is small on purpose. Start as a single script and grow it as far as you like.

### What you will build

**CurveRider** is a minimal workbench for adapting to model upgrades, built around the four practices in Part 4. It has three pieces that line up with the lesson:

1. **A model switch:** run the *same* task and the *same* eval against two different models with a one-line change.
2. **An unsaturated eval:** a small set of test cases that includes at least one task hard enough that your weaker model fails it, so a better model can visibly win.
3. **A verify-and-iterate loop:** a plan-execute-verify loop where a deterministic check (for example, running tests) tells the agent whether it succeeded, mirroring the Bun example.

> 🎯 **Pick your task.** Choose something you genuinely care about and that has a clear right answer, so verification is easy. Good options: "implement this small function so its tests pass," "fix this bug," or "build this tiny web page with these required elements." Avoid tasks with no objective check; you need a verifier.

### Why this is the perfect practice

| Lesson idea | Where you use it in CurveRider |
|---|---|
| The curve is real and measurable | Milestone 2, watch the eval score move between models |
| Unsaturated evals | Milestone 2, you cannot proceed without a failing case |
| Verification is the unlock | Milestone 3, the deterministic check drives the loop |
| Plan-execute-verify loop | Milestone 3, the agent loop you build |
| Give the model room (thinking, effort) | Milestone 4, raise effort and re-measure |
| Shrink your scaffolding | Milestone 5, trim the prompt and confirm the score holds |
| Close the agent loop | Milestone 6, let Claude improve your own prompt/tools |

### Milestones (build them in order, each one works on its own)

1. **Scaffold.** Set up a project, connect the Anthropic SDK (the official code library for calling Claude), and make one successful API call on your chosen task. Smallest version: a single script that prints the model's answer.
2. **Build an unsaturated eval.** Write 5 test cases for your task, including at least one deliberately hard case. Run it against a deliberately weaker model and confirm it does **not** get everything right. A red mark here is success; it proves the eval has room to measure.
3. **Add verify-and-iterate.** Wrap the model in a plan-execute-verify loop: the model attempts the task, you run a deterministic check (run the tests, count the rule breaks), and if it fails you feed the failure back and let it try again, up to a few rounds. This is the long-horizon loop in miniature.
4. **Flip the model and the effort.** Change one line to run the *same* task and eval on a stronger model, and turn the reasoning effort up. Record the eval score, the tokens, and the time at each setting. You should see the curve with your own eyes.
5. **Shrink the scaffolding.** Trim your prompt toward the bare minimum, then re-run the eval. If the score holds, you found free weight to drop. If it drops, you learned which instruction was actually load-bearing.
6. **Close the loop.** Point Claude Code (or a second Claude call) at your own setup and ask it to improve the prompt or tools to raise the eval score. Let it run the eval itself. Keep any change that genuinely improves the score.
7. **Stretch goals.** Add an auto-mode style classifier that auto-approves safe steps and escalates risky ones. Add a third model to the comparison. Add a saturation alarm that warns you when a model passes every case so you know to make the eval harder.

### How you will know you are done

- ✅ A **single line change** swaps the model, and you can show the eval responding to it.
- ✅ At least one eval case is **hard enough that the weaker model fails it** (your eval is not saturated).
- ✅ Your loop uses a **deterministic verifier**, and you can point to a run where the agent recovered from a failure.
- ✅ You recorded **score, tokens, and time** across at least two models and two effort settings.
- ✅ You trimmed the prompt and **proved with the eval** that the cut was free (or learned why it was not).

> 💡 **Keep yourself honest:** change one thing at a time and re-run the eval. If you cannot say which change moved the score, you changed too much at once.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. They are optional and independent. The Capstone above is the main build and already touches all of these, so feel free to skip straight to it.

### Exercise 1: re-run an old failure (foundational)
Find a task that a model failed for you in the past (or invent a plausible one). Run it on a current model and write down what improved. The point is to *feel* the curve rather than read about it.

### Exercise 2: classify the gain (foundational)
Take three agent transcripts or sessions you have seen. For each, label which of the three gains is on display: planning before acting, error recovery, or long-horizon coherence. Some will show more than one.

### Exercise 3: saturation check (intermediate)
Take an eval you already have (or write 5 quick cases). Run a strong model on it. If it passes everything, the eval is saturated. Add two harder cases until at least one fails. Note what made the new cases harder.

### Exercise 4: shrink a Frankenstein prompt (intermediate)
Take a long prompt full of "always / never / be careful to" lines. Cut it to the smallest version that still states your real intent. Run a before-and-after eval. Which lines were load-bearing, and which were leftover workarounds?

### Exercise 5: build a verify loop (advanced)
Pick a task with an objective check (tests passing, rules satisfied). Build a plan-execute-verify loop that feeds failures back to the model for up to three rounds. Then deliberately give it a task it cannot do in one try and confirm it recovers instead of doom looping. Record tokens used per round.

---

## Cheat sheet

```text
THE CURVE (in 12 months)
  SWE-bench Verified ... ~60% (Sonnet 3.7)  ->  87% (Opus 4.7), top models saturate it
  Task horizon ......... minutes  ->  hours  ->  (soon) continuous
  Website demo ......... better result, FEWER lines

THREE GAINS DRIVING IT
  Plan before acting ... reads & plans first; catches its own mistakes
  Error recovery ....... no more doom looping; reasons from failures
  Long-horizon ......... coherent up to ~1M tokens; don't pre-chop tasks

THEY STACK INTO AUTONOMY
  PLAN -> EXECUTE -> VERIFY -> (iterate) -> validate vs goal
  Verification is the unlock (see: Bun rewritten in Rust in one week)

RIDE THE CURVE (4 practices)
  1. Evals you trust ... real traffic; unsaturated; run as a script
  2. Shrink scaffolding. cut old workarounds; trim, then re-eval
  3. Room to work ...... adaptive thinking + high effort; auto mode
  4. Close the loop .... let Claude run your agent + eval to improve it

REMEMBER
  - A saturated eval can't tell a better model from a worse one.
  - Old prompt lines become bugs as models get smarter.
  - It's the trajectory, not any single model.
```

## How this connects to the rest of the course

- **Earlier, Module 1 · Lesson 1 (Opening Keynote):** introduced the exponential and the four habits at a high level. This lesson made them concrete.
- **Next, Module 2 (Core skills):** the prompting and model-choice lessons are where you practise shrinking scaffolding and giving the model room to think.
- **Next, Module 3 (Evals):** builds out the "evals you can trust" practice that this whole lesson rests on, including saturation and graders.
- **Later, Module 5 (Claude Managed Agents):** the plan-execute-verify loop and "closing the agent loop" grow into full autonomous multi-agent systems.

---

*Source: "The capability curve" by Jeremy (Product Manager, research team, Anthropic), Code with Claude 2026, London. Code snippets and the cheat-sheet diagrams are illustrative reconstructions of the patterns described in the talk. Adapt model names and API details to the current SDK.*

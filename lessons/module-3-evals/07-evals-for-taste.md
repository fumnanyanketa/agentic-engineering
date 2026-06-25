# Module 3 · Lesson 7: Evals for Taste

> **Course:** Building with Claude, a self-paced course
> **Module 3:** Measuring quality: evals
> **Speaker:** Anthropic (Applied AI team)
> **Source talk:** [Evals for taste: hill-climbing a slide-generation agent](https://www.youtube.com/watch?v=v9FTCvkV_a0) · [full transcript](../../transcripts/code-with-claude-2026-london-2026-day-2/04_evals-for-taste-hill-climbing-a-slide-generation-agent.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

An eval is a set of repeatable tests that turn vague feelings ("this output looks worse today") into concrete, actionable measurements, and once you have one you can improve an AI agent step by step, swap in a smarter model with confidence, and even measure fuzzy qualities like "taste" using the model itself as a judge.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you build **SlideSmith**, a slide generation agent with its own scorecard, and then climb the quality ladder the same way the talk does. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project: SlideSmith"** section near the end, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[Your AI Product Needs Evals (Hamel Husain)](https://hamel.dev/blog/posts/evals/)** (essay). The canonical argument for evals as core infrastructure, covering the same hierarchy (code assertions, human/model judging, A/B) and LLM-as-judge calibration the lesson teaches.
> - **[Define success criteria and build evaluations (Anthropic docs)](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)** (docs). The official reference on choosing graders and the "reason before the score" technique central to the lesson.

## A few plain-language basics first

This lesson uses some everyday AI terms. Here they are in simple words, so nothing below is confusing:

- **LLM (Large Language Model):** the kind of AI that reads and writes text. "Claude" is an LLM. Think of it as a very capable text assistant.
- **Model:** one specific version of that AI, for example "Sonnet 4.6" or "Opus 4.7." Different models have different strengths, speeds, and prices.
- **Agent:** an AI that takes a series of actions on its own toward a goal (for example, writing files and running code), rather than answering in one shot.
- **Prompt:** the text instructions you give the model. The **system prompt** is the standing instructions that describe the agent's job and rules.
- **Token:** the unit the model reads and writes in, roughly three quarters of a word. You are billed per token, so "more tokens" means "costs more and takes longer."
- **Eval (evaluation):** a set of test cases you run an agent against to measure how well it does. This is the central idea of the lesson.
- **Grader:** the part of an eval that judges one output and turns it into a score or a pass/fail. There are several kinds, and choosing the right one is most of the skill.
- **Deterministic:** always gives the same answer for the same input, with no AI guesswork involved.
- **Benchmark:** a well known, shared eval (for example "SWE-bench") used to compare models against each other.

You do not need to memorise these. Every term is explained again the first time it appears below.

## Why this lesson matters

The speaker is open about loving this topic: "I personally am a big fan of anything evals related." The reason matters to anyone building with AI. Without evals you are stuck reacting to complaints. A customer says the agent "feels a little bit worse today," and all you can do is dig through logs and guess. You fix one thing and quietly break two others. You cannot tell genuine feedback from noise, and you have no honest way to prove that a change actually helped.

Every time Anthropic ships a model, it ships a scorecard of evals alongside it. If evals are that important to the people building the models, they are just as important to you building on top of them. This lesson shows you how to build your own.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain what an eval is and why "vibes" are not enough to improve an agent.
2. Choose between the four kinds of **graders** (code based, model based, multi-judge, human) and know the trade-offs of each.
3. Design graders that actually give you **actionable** information, and recognise when a grader has stopped being useful (**saturation**).
4. **Hill-climb** an agent: run the eval, read the failures, change one thing, run again, and keep what helps.
5. Avoid a subtle bug in model based graders: making the judge give its **reasons before its score**, not after.

## Prerequisites

- Module 2 · Lesson 3 (The prompting playbook), which introduces evals and the idea of changing one thing at a time. This lesson goes deeper on grading.
- Helpful but optional: any module that introduced **managed agents** (the agent definition file used in the demo).

---

## Part 1: what an eval actually is

An **eval** is a systematic test that measures how well an AI system performs on a specific use case. It tells you what the agent did well, what it did badly, and where to improve. An eval is made of two pieces:

1. **Tasks:** specific scenarios you run the agent on (for example, "make a five slide deck about salary negotiation").
2. **Graders:** the logic that judges each output and encodes your expectations as a score.

> 🔑 **The core promise of evals: turn vibes into action.** Vibes have a place. They are a fine gut check for how people feel. But you cannot act on a vibe. As the speaker puts it, an eval is "the bridge" between "it kind of feels worse today" and a concrete change you can make and verify.

### Benchmarks are just famous evals

When a new model launches, you see scores on **benchmarks** like SWE-bench (which measures agentic coding ability) or Terminal-Bench. A benchmark is simply a well known eval that everyone uses, so models can be compared fairly.

> 💡 Those public benchmarks measure general capability across many tasks. They almost never measure *your* specific use case. That is exactly why the advice is always: build your own evals, benchmark the models on your task, and make sure you are using the right model for the job.

### What evals buy you

| Without evals | With evals |
|---|---|
| You only catch issues in production, after a complaint. | You make problems visible before launch. |
| You fix one issue and silently break others. | You verify every change improves things, with no regressions. |
| Hard to separate real feedback from noise. | You have a clear, repeatable signal. |
| You cannot even say what "good" means. | Building the eval *forces* you to define success. |
| Trying a new model is a leap of faith. | You adopt new models faster, with clarity on what improved. |

That last "forces you to define success" point is bigger than it sounds. If you cannot articulate what a good output looks like, you have no way to know whether your agent is behaving. Writing the eval is how you make yourself say it out loud.

---

## Part 2: the four kinds of graders

A **grader** is how you judge one output. The talk lays out four kinds, from cheapest and strictest to most expensive and most nuanced. Picking the right grader for each thing you want to measure is most of the work.

### Grader 1: code based (like a unit test)

A **code based grader** is plain code that checks the output, much like a software unit test. It can be a string match, a regular expression (a text pattern), a fuzzy match, or a static check on files.

```python
# A code based grader: count emojis in the generated slide deck.
def emoji_count(slide_deck) -> int:
    """Return how many emoji characters appear across all slides."""
    return sum(count_emojis(slide.text) for slide in slide_deck.slides)
```

| Pros | Cons |
|---|---|
| Fast, cheap, deterministic | Brittle |
| Easy to reason about | Lacks nuance |

> 💡 "Brittle" means the check forces one rigid, deterministic behaviour. Sometimes that is exactly what you want. For "is there a slide deck at all?" a deterministic yes/no check is perfect. But for "is this slide deck *good*?" a strict code check cannot capture the nuance.

### Grader 2: model based (use an LLM as the judge)

A **model based grader** (also called an **LLM judge**) uses a model to score the output against a **rubric**. A rubric is a written description of what to look for, for example "is this slide high quality?" or "is the text coherent?"

```text
# A rubric the judge model is given (a system prompt for the judge):
Please evaluate the slide on each criterion below and give a score 0 to 5.

TEXT: The title should be simple and clear and indicate the main point.
For body content, avoid too much text and keep words concise. Use a
consistent, readable font size, style, and colour.
...
```

Two model based techniques the talk calls out:

- **Pairwise comparison ("which of these two is better, and why?").** The speaker calls this "quite underrated." When you cannot define what "best" means in the abstract, showing the judge two outputs and asking it to pick a winner often works far better than asking for an absolute score.
- **Multi-judge consensus ("best of three").** Run several judges independently and take the majority vote. Because an LLM is non-deterministic (run it 100 times and it will not always say the same thing), spending more compute and taking the majority adds back some stability.

| Pros | Cons |
|---|---|
| Flexible, scalable, nuanced | Non-deterministic |
| Can judge "taste" and quality | Costs more money |
|  | Requires calibration (this is hard) |

### Grader 3 and 4: the cost ladder

The four graders form a ladder from cheap to expensive:

```text
code based  ->  model based  ->  multi-judge consensus  ->  human
cheap, strict                                              expensive, nuanced
```

**Human graders** sit at the top: a subject matter expert reviews the output by hand. They are the highest quality and most nuanced, but slow and expensive, so you use them least, mainly for A/B testing (comparing two versions head to head) and spot checks.

> 🔑 **Rule of thumb for choosing a grader:** if a thing is *quantifiable*, use code (counting words on a slide). If a thing is *qualitative*, use a model judge (does the text overlap or look cluttered). Match the grader to the nature of the question.

> 🔑 **The grader test (quote):** "If you have a grader that you get no useful information out of, then you should not have that part of your eval." For every scenario you test, you must be able to say: this is the information I want, this is the part of the system I am testing, and this is how I will act if it degrades.

---

## Part 3: hill-climbing a slide agent

Now the loop in action. We start with a deliberately simple slide generation agent. Its whole system prompt is roughly:

```text
You are a slide generation agent. When the user gives you a topic, create a
PowerPoint file at <location>. You have a shell with python-pptx pre-installed.
```

"Hill-climbing" means improving step by step: run the eval, read the failures, make one change, run again, and repeat. Each loop should climb a little higher.

### Round 0: the baseline (and what we measure)

The first deck is, in the speaker's honest words, "not the best slide deck you guys have ever seen." Overlapping text, weird colours, a stray dollar sign, emojis used as decoration. But it is five slides, so it is a start.

Looking at the failures, we pick graders that capture them. Some are code based (deterministic counts), some are model based judges (qualitative scores):

| Grader | Kind | What it measures |
|---|---|---|
| Emoji count | code | How many emojis appear (we noticed too many) |
| Cluttered slides | code | How many slides have too many shapes |
| Slide count | code | Did we get the 5 slides we asked for |
| Small font slides | code | Slides with hard to read font sizes |
| Text-heavy slides | code | Slides crammed with words |
| Text judge | model | 0 to 5 score on title clarity and conciseness |
| Image judge | model | 0 to 5 score on image quality |
| Layout judge | model | 0 to 5 score on layout |
| Colour judge | model | 0 to 5 score on colour contrast |

A small script runs the deck through all of these and prints a `score.json`. That scorecard is your dashboard for every round that follows.

> 💡 The graders here were "quite arbitrarily chosen" to be representative of what a slide deck needs. That is fine. What matters is that each one gives you information you can act on. Your graders will be different because your use case is different.

### Round 1: a better prompt

The baseline scorecard shows the problems clearly: emoji count is high, several slides have tiny fonts, some are cluttered. So we put that knowledge straight into the system prompt: exact font sizes for titles, headers, body, and captions; guidance on layout and density ("keep body text concise, leave breathing room, left-align paragraphs"); and a list of "AI tells" to avoid ("never use thin accent lines in titles," "don't pepper slides with emojis as decorative icons").

The new deck is "immediately way more enjoyable to look at." Cleaner, more consistent colour, no overlap. The loop worked: read the failures, change one thing (the prompt), run again.

### A twist: the eval itself can be wrong

Then something instructive happens. The new scorecard reports an emoji count of **20**, but the speaker cannot find any emojis in the deck. And a slide flagged "text-heavy" looks perfectly acceptable on review.

> 🔑 **Evals are a living artifact, not the ground truth.** The moment a grader disagrees with what your own eyes tell you, the grader is wrong, not your eyes. Go back, fix the grader, and make it reflect what you actually want to measure. This calibration is, in the speaker's words, "very fickle," and worth real time.

> 💡 When an eval stops giving you useful, actionable information, people say it has **saturated**. A saturated grader is one to fix or retire, not to keep trusting.

### Round 2: add a hard requirement (diagrams)

Suppose every slide must now include a diagram or chart as a real image. We change the system prompt again: "every slide must include at least one generated diagram or chart inserted as an actual image." The decks get noticeably better, "grounded in some actual facts right now instead of just waffling its way through."

But the image judge returns a flat "3.8 out of 5" with nothing to explain it. A bare number with no reasoning gives you nothing to act on. Hold that thought; Part 4 fixes it.

### Round 3: the QA loop (the technique that works everywhere)

The single most transferable trick in the talk is the **QA loop** (QA = quality assurance, a deliberate check for problems). It is two agents in a cycle:

```text
1. CREATOR agent builds the slide deck.
2. CRITIC agent inspects it and hunts for problems: "this is bad, this overlaps,
   this font is too small."
3. The criticism goes back to the CREATOR, which fixes the issues.
4. Repeat until both sides agree it is ready to ship.
```

The key is to instruct the critic **adversarially**, on purpose:

```text
# Added to the system prompt:
Require a QA loop. Assume there ARE problems and your job is to find them.
Approach QA as a bug hunt, not a confirmation step. After writing the deck,
convert it to images, inspect every slide image yourself, fix the issues,
re-render, and re-inspect. Do not stop until you have completed at least one
fix-and-verify cycle.
```

Notice the wording. Not "there might be something interesting to find" but "there ARE issues, go find them." After this change, the image is bigger and more readable, slides cite their sources, and the judge scores rise across the board into the 4.2 to 4.4 range.

> 💡 The QA loop is "transversal over every single use case." It is intuitive for coding (one agent writes, another reviews), and it works just as well for slides, documents, or anything an agent produces. You are simply automating the "look at it, find the flaws, fix them" loop you would do by hand.

### Round 4: just use a smarter model

You can keep hand-tuning the prompt forever. Or you can step back and let a stronger model figure things out on its own. Swapping Sonnet 4.6 for **Opus 4.7**, with nothing but the *original* simple prompt, the output is "significantly better." Opus uses no emojis at all (it just knows a salary deck should not have them), and it has fewer tiny-font slides because it has an innate sense of what a slide deck should look like.

> 🔑 **Smarter models carry their own taste.** As models improve, a lot of the rules you painstakingly wrote into the prompt become unnecessary, because the model already knows them. Always retest a smarter model on your eval; you may be able to delete instructions and still do better.

---

## Part 4: calibrating LLM judges (the part everyone gets wrong)

Code graders are easy. The hard, subtle part is making model based judges trustworthy. Two big lessons.

### Problem 1: the judge has nothing to anchor on

When Opus gets a "5 out of 5" on the image judge for a deck that contains *no image at all*, the eval is broken. The judge was told "give a score 0 to 5" but never shown what a 0 or a 5 actually looks like, so it makes up a number.

The fix is to give the judge **anchors**: concrete examples of what each score means.

```text
# Anchor the rubric so the judge knows what good and bad look like:
Score 0 (awful): text overflows the slide, three clashing colours, unreadable
font. Telltale signs: ...
Score 5 (excellent): one clear title, generous whitespace, a single relevant
chart with a cited source. Telltale signs: ...
```

### Problem 2: reasons must come BEFORE the score

This is the most important detail in the lesson, and it is easy to get backwards. The speaker hit it while building the demo: ask the judge for the number first and the reasons second, and the reasons become worthless.

> 🔑 **Why order matters (the auto-regressive trap).** An LLM writes one token at a time, each new word influenced by the words before it. If it commits to "4" first, it will then "do anything it can to argue why it should be a 4," even when the honest answer is a 1. The number poisons the reasoning that follows it.

So flip the order. Make the judge reason *first*, then decide:

```text
# WRONG: score first, then justify (the score poisons the reasons)
{ "score": 4, "reasons": "It is a 4 because ..." }

# RIGHT: gather evidence first, decide last
1. List reasons it should score HIGH (the pros).
2. List reasons it should score LOW (the cons).
3. Weighing all of the above, give your final score 0 to 5.
```

This also explains why the **multi-agent QA** approach is powerful: one agent finds all the issues, another refutes them, and only then do you settle on a verdict. For nuanced domains (the talk uses the example of summarising a legal case, where an agent loves to jump to confident conclusions), you combine techniques: multiple graders, a critic to surface problems, a refuter to check them, because a grader can hallucinate too.

> ✅ **Best practice: always make a judge explain itself, reasons first.** A bare number ("3.8") is not actionable. The reasoning is what tells you *what to fix*, and putting it first keeps the model honest.

---

## Key takeaways

1. **Evals turn vibes into action.** "It feels worse" is not something you can fix. A scorecard is.
2. **Public benchmarks are not your eval.** Build your own for your specific use case, and use it to choose the right model.
3. **Match the grader to the question.** Quantifiable things go to code graders; qualitative things go to model judges.
4. **A grader that gives no actionable information should not exist.** For each one, know what you would change if it dropped.
5. **Evals are a living artifact.** When a grader disagrees with your eyes, fix the grader. Watch for saturation.
6. **Hill-climb:** run, read failures, change one thing, run again, keep what helps.
7. **The QA loop works everywhere.** Two agents (creator and adversarial critic) in a cycle lift quality on almost any task.
8. **A smarter model often beats hand-tuned prompts**, and lets you delete rules it already knows.
9. **For LLM judges, reasons must come before the score.** Otherwise the model just rationalises its first number.

## Common pitfalls

- ❌ Acting on a single complaint with no eval to confirm it is real.
- ❌ Using a strict code check to grade something nuanced (and then trusting a brittle, meaningless result).
- ❌ Asking a judge for a score with nothing to anchor it (no example of a 0 or a 5).
- ❌ Asking the judge for the number first and the reasons second.
- ❌ Treating your eval as frozen ground truth instead of fixing graders that drift.
- ❌ Keeping a grader around out of habit when it tells you nothing actionable.
- ❌ Forgetting that an LLM judge can hallucinate just like any other LLM, especially on nuanced tasks.

---

## 🛠️ Capstone Project: SlideSmith

> This is the main hands on project for the lesson. You will rebuild the talk end to end: a slide generation agent, a scorecard of graders, and the hill-climbing loop that takes it from rough to polished. Start as small as a single script and grow it.

### What you will build

**SlideSmith** is a slide generation agent plus its own eval harness. It has two halves that mirror the two halves of this lesson:

1. **The agent:** takes a topic and produces a slide deck (use `python-pptx`, or generate HTML slides if that is easier to render and screenshot).
2. **The scorecard:** a script that runs a deck through a set of code graders and model judges and prints a `score.json`, exactly like the demo.

> 🎯 **Pick your topic.** Use the talk's example (a deck on "salary negotiation") or pick anything with real content: "how DNS works," "a tour of three coffee brewing methods," "your team's Q3 roadmap." Just pick something concrete enough that quality is visible.

### Why this is the perfect practice

| Lesson skill | Where you use it in SlideSmith |
|---|---|
| Defining what "good" means | Milestone 2, before you grade anything |
| Code based graders | Milestone 2, counting emojis, slides, shapes |
| Model based judges with rubrics | Milestone 3 |
| Hill-climbing the loop | Milestone 4, every prompt change |
| Calibrating a judge (anchors, reasons-first) | Milestone 5 |
| The adversarial QA loop | Milestone 6 |
| Swapping in a smarter model | Milestone 7 |

### Milestones (build them in order, each one works on its own)

1. **The baseline agent.** Write the simplest possible agent: a system prompt that says "you are a slide generation agent, make a five slide deck on the given topic" plus a tool or shell to write the file. Generate one deck and look at it with your own eyes. Write down everything wrong with it.
2. **Code graders.** Turn each visible flaw into a deterministic grader: `emoji_count`, `slide_count`, `cluttered_slides` (too many shapes), `small_font_slides`, `text_heavy_slides`. Write a `score.py` that runs them all and prints a `score.json`. This is your dashboard.
3. **Model judges.** Add 0-to-5 LLM judges for the qualitative stuff code cannot catch: text, layout, colour, and (later) image. Give each a clear rubric. Run them and record the scores.
4. **Hill-climb on the prompt.** Read the scorecard, pick the worst grader, and add targeted guidance to the system prompt (exact font sizes, density rules, "no decorative emojis"). Re-run. Record before and after for every change. Change one thing at a time.
5. **Calibrate a judge.** Find a judge that gives a suspicious score (a high score with no image, say). Fix it two ways: (a) add anchor examples of what a 0 and a 5 look like, and (b) make it output **reasons first, score last**. Confirm the scores get more sensible and the reasons tell you what to fix.
6. **Add the QA loop.** Add an adversarial critic step to the agent: "assume there ARE problems, hunt for them, fix and re-inspect, do not stop until one full fix-and-verify cycle is done." Measure the lift.
7. **Climb to a smarter model.** Swap Sonnet for Opus (or whatever your strongest available model is), keep only the *simple* prompt, and re-run the whole scorecard. Note which hand-written rules you no longer need.
8. **Stretch goals.** Add a hard requirement ("every slide must have a real chart") and a grader for it. Add **pairwise comparison** (judge picks the better of two decks). Add **multi-judge consensus** (best of three) and see if scores stabilise.

### How you will know you are done

- ✅ Every grader gives information you can actually **act on** (you can name the change you would make if it dropped).
- ✅ You can point to each prompt change and show, from the scorecard, the exact failure it fixed.
- ✅ At least one judge outputs **reasons before its score**, and you can show why that order matters.
- ✅ The QA loop measurably raises your judge scores.
- ✅ The smarter model lets you **delete** at least one hand-written rule and still score as well or better.

> 💡 **Keep yourself honest:** when a grader disagrees with your own eyes, fix the grader, not your eyes. The eval is a living artifact.

---

## Practice exercises (optional extra reps)

> **What these are:** five small, self contained tasks, each focused on one skill. They are optional and independent. The **Capstone above is the main build** and already covers all of them, so skip straight to it if you would rather build one bigger thing.

### Exercise 1: code vs model grader (foundational)
List five things you might want to measure about a slide deck. For each, label it **quantifiable** (use a code grader) or **qualitative** (use a model judge), and write one sentence on the grader you would build.

### Exercise 2: write a code grader (foundational)
Write the `emoji_count` and `slide_count` graders in real code for a deck format you can parse. Confirm they return sensible numbers on a sample deck.

### Exercise 3: write a judge rubric (intermediate)
Write a rubric for a "layout judge" that scores 0 to 5. Include **anchor examples** for at least a 0 and a 5. Run it on two decks and check the scores match your own opinion.

### Exercise 4: fix the order bug (intermediate)
Take any LLM judge and deliberately build it the wrong way (score first, reasons second). Run it on a clearly bad output and watch it rationalise a high score. Now flip it to reasons-first and re-run. Describe what changed and why.

### Exercise 5: build a QA loop (advanced)
Wrap any generator agent (slides, a short report, a webpage) in a creator-plus-adversarial-critic loop. Instruct the critic that problems definitely exist. Run with and without the loop and compare the outputs.

---

## Cheat sheet

```text
WHAT IS AN EVAL?
  Tasks (scenarios) + graders (judging logic) = a repeatable measurement.
  Goal: turn "it feels worse" into a number you can act on.

CHOOSE A GRADER
  Quantifiable thing ........ CODE grader (fast, cheap, strict, brittle)
  Qualitative / "taste" ..... MODEL judge (flexible, nuanced, needs calibration)
  Need stability ............ MULTI-JUDGE consensus (best of three)
  Highest quality, rare ..... HUMAN (slow, expensive, for A/B + spot checks)
  Cannot define "best" ...... PAIRWISE ("which of these two, and why?")

THE HILL-CLIMB LOOP
  run eval -> read failures -> change ONE thing -> run again -> keep what helps

CALIBRATE A JUDGE
  - Give it anchors (what does a 0 look like? a 5?).
  - REASONS FIRST, score last (or it just justifies its first number).
  - A judge can hallucinate too; cross-check with more graders / a critic.

ALWAYS REMEMBER
  - A grader with no actionable output should not exist.
  - Evals are a living artifact; fix graders that drift (saturation).
  - A smarter model carries its own taste; retest and delete rules it knows.
```

## How this connects to the rest of the course

- **Earlier, Module 2 · Lesson 3 (The prompting playbook):** introduced evals and the "change one thing, re-run" loop. This lesson deepens the grading half.
- **Earlier, Module 2 (Picking the right model):** the "just use Opus" move here is the rigorous, eval-backed version of choosing a model.
- **Next, Module 4 (Claude Code):** the QA loop and "let the agent verify itself" ideas reappear as everyday agent workflows.
- **Later, Module 5 (Managed agents):** the creator-plus-critic pattern grows into full multi-agent systems.

---

*Source: "Evals for taste: hill-climbing a slide-generation agent" by the Anthropic Applied AI team, Code with Claude 2026, London. Code snippets are illustrative reconstructions of the graders and prompts shown in the talk. Adapt model names and API details to the current SDK.*

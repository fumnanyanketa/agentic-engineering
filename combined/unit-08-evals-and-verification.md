# Unit 8: Evals and Verification

> **Course:** Agentic Engineering, a model-agnostic self-paced path *(working title)*
> **Unit 8 of 11:** Build a graded eval suite so you can measure quality instead of guessing it, then let an agent run unsupervised because the evals gate its work
> **Principle (vendor-neutral):** Agentic Engineering Module 12, Evaluation (how you know it actually works)
> **The how, across models:** Claude (Anthropic), Gemini (Google), GPT (OpenAI); run the same suite against any of them
> **AtlasOS build:** `evals/` (Warden): Warden's first graded suite for the Scout agent
> **Estimated time:** 90 to 120 minutes

---

## In one sentence

An **eval** is a repeatable test that turns a vague feeling ("the agent seems worse today") into a concrete number you can act on, and this unit teaches you to build a small graded eval suite, judge subjective "taste" with a model acting as a referee, keep one deliberately hard case so you can tell when a smarter model arrives, and use that suite as the gate that lets an agent finally run without you watching every step.

> 🎯 **Where this unit is heading.** The payoff is a **Build** where you create the `evals/` folder in your AtlasOS repo and write **Warden's** first graded suite for the **Scout** research agent: four to six test cases with clear pass criteria, one deliberately hard case that currently fails (our "the exponential moved" detector), and a simple model-as-judge for one subjective case. You will run it and read a real score off your screen. Jump to **"The Build"** to see the finish line, then come back and we will get you there.

## First-principles companion

> 💡 **The durable ideas behind this unit.** The tools are recent; the discipline is not. If you want the timeless versions (optional, read them any time):
>
> - **[Your AI Product Needs Evals (Hamel Husain)](https://hamel.dev/blog/posts/evals/)** (essay). The canonical argument for evals as core infrastructure: code assertions, human and model judging, and how to calibrate an LLM-as-judge.
> - **[Define success criteria and build evaluations (Anthropic docs)](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)** (docs). The official reference on choosing graders and the "reason before the score" technique.
> - **[An FAQ on AI evals (Husain and Shankar)](https://hamel.dev/blog/posts/evals-faq/)** (essay). Why you start from error analysis on real transcripts, and why binary pass/fail beats 1-to-5 scores.
> - **[Evaluating the Effectiveness of LLM-Evaluators (Eugene Yan)](https://eugeneyan.com/writing/llm-evaluators/)** (essay). The measured biases of model judges and how to check one against human labels before you trust it.
> - **[DSPy: Compiling Declarative LM Calls into Self-Improving Pipelines](https://arxiv.org/abs/2310.03714)** (paper). The rigorous foundation of the "self-improving prompt" idea: optimize against evals instead of hand-tuning forever.

## A few plain-language basics first

New terms, in plain words. You do not need to memorise these; each is explained again the moment it matters.

- **Eval (evaluation):** a test that measures how well your AI system does its job. You collect example tasks, run the system on them, and score the results into a number you can track over time.
- **Test case:** one example task in an eval, paired with what a good answer looks like (the **pass criterion**).
- **Grader:** the logic that judges one output and turns it into a result, usually **pass** or **fail**.
- **Code grader:** a grader written in plain code (a string match, a count, a check), like a software unit test. Fast, cheap, exact, but rigid.
- **LLM-as-judge (model-as-judge):** using a second AI model to score the first model's output against a written description of what good looks like. Flexible enough to judge "taste," but it must be checked.
- **Rubric:** the written description you give a judge of what to look for ("is this summary faithful and concise?").
- **Transcript (or trace):** the full record of what an agent did on one task: what it was asked, what it thought, which tools it called, what it answered. Reading these is the real work.
- **Regression:** when a change quietly makes something that used to work stop working. Evals catch regressions before your users do.
- **Verification:** checking that work is actually correct. For an agent, this means giving it a way to test its own output rather than relying on you to catch every mistake.
- **Scout / Warden:** two members of your AtlasOS fleet. **Scout** is the research agent (takes a question and sources, returns cited findings). **Warden** is the reviewer and eval gatekeeper. Nothing ships past Warden without passing its checks.

## Why this unit matters

In ordinary software a test has one right answer: 2 plus 2 should equal 4. Language models are different. For an open-ended task like "summarize this report" there are many valid answers and no single correct one, which is exactly what makes evaluation hard, and exactly why most teams skip it. Skipping it is the trap. Without evals you are stuck reacting to complaints: a user says the agent "feels a little worse today," and all you can do is dig through logs and guess. You fix one thing and quietly break two others. You cannot tell real feedback from noise, and you have no honest way to prove a change actually helped.

> 🔑 **You cannot improve what you cannot measure.** An eval is the bridge between "it kind of feels worse today" and a concrete change you can make and verify. Every serious model lab ships a scorecard of evals alongside every model it releases. If evals are that important to the people building the models, they are just as important to you building on top of them.

This is the other half of the idea you met in Unit 1: **verification is the bottleneck.** When writing code (or research, or a summary) becomes cheap and fast, the scarce, valuable skill becomes *checking* it. Evals are how you make checking fast, repeatable, and trustworthy, so you can finally stop babysitting.

## Learning objectives

By the end of this unit you will be able to:

1. Explain what an eval is and why "vibes" cannot be acted on.
2. Build a small graded suite from real failures, using binary pass/fail and a reference answer per case.
3. Choose between a **code grader** and an **LLM-as-judge**, and write each correctly (reasons before the score).
4. Keep one deliberately hard, currently-failing case as a detector for when a smarter model arrives.
5. Run the same suite against Claude, Gemini, or GPT to compare them on *your* task, not a public benchmark.
6. Use a passing eval suite as the gate that lets an agent run unsupervised, and sketch a prompt that improves itself against the suite.

## Prerequisites

- Unit 1 (the coding-agent workflow): your workstation, your `atlasos` repo, and the plan, act, verify loop.
- Unit 2 (prompting and context): you authored Scout's system prompt and a tiny eval harness there. This unit grows that into a real graded suite.
- Python installed (it came with nothing exotic; the Build uses only the standard library). If `python --version` or `python3 --version` prints a number, you are set.
- No API key or paid plan is required to finish the Build: it runs offline against recorded outputs, then shows you exactly where to plug in a live model.

---

## Part 1: what an eval actually is (vibes to action)

An eval is a systematic test that measures how well an AI system performs on a specific use case. It is made of two pieces:

1. **Test cases (tasks):** specific scenarios you run the agent on (for example, "answer this research question from these three sources").
2. **Graders:** the logic that judges each output and encodes your expectations as a result.

Run the cases, grade the outputs, and you get a single number, your **score**, that you can track across every change you make.

```text
     ┌── test cases ──┐      ┌── run the agent ──┐      ┌── graders ──┐
     │ task + the     │ ───▶ │ Scout answers each │ ───▶ │ pass / fail │ ───▶  SCORE
     │ pass criterion │      │ case               │      │ per case    │       5 / 6
     └────────────────┘      └────────────────────┘      └─────────────┘
```

> 🔑 **The core promise of evals: turn vibes into action.** Vibes are a fine gut check for how people feel, but you cannot *act* on a vibe. A score you can act on. The moment you have a number, "it feels worse" becomes "case 3 regressed, here is the diff that broke it."

There is a quieter benefit that is bigger than it sounds. To write a test case, you have to say out loud what a good answer looks like. If you cannot articulate that, you have no way to know whether your agent is behaving. **Building the eval forces you to define success.** Most people discover they were fuzzy on "good" until the eval made them write it down.

> 💡 **Start from real failures, not imagined ones.** The most useful first activity is **error analysis**: run your agent on real tasks, read the transcripts, and write down every failure you actually see. Then write a test for each *observed* failure. Imagined failures waste effort on problems you do not have. You do not need thousands of cases to begin; 4 to 6 real ones is a real suite.

---

## Part 2: graders, from a unit test to a model-as-judge

A **grader** is how you judge one output. They sit on a ladder from cheap-and-strict to expensive-and-nuanced. Picking the right grader for each thing you measure is most of the skill.

```text
  code grader  ──▶  LLM-as-judge  ──▶  multi-judge consensus  ──▶  human
  cheap, exact,      flexible, can      majority vote of            slowest,
  brittle            judge "taste",     several judges for          most nuanced,
                     needs calibration  stability                   used least
```

**Code grader (like a unit test).** Plain code that checks the output: a string match, a count, a pattern, a yes/no check on a file. Fast, cheap, and exactly repeatable, but rigid. Perfect for quantifiable questions ("does the answer contain the year 2026?", "did it cite a source?", "did it refuse to invent a price?").

**LLM-as-judge.** A second model scores the output against a **rubric**. This is how you grade the things code cannot catch: is this summary faithful, is the writing clear, did it capture the point. Flexible and scalable, but non-deterministic and in need of calibration (Part 4).

> 🔑 **Rule of thumb for choosing a grader.** If the thing is *quantifiable*, use code (counting, matching, a hard check). If it is *qualitative* or a matter of taste, use a model judge. Match the grader to the nature of the question.

> 🔑 **Prefer binary pass/fail over a 1-to-5 score.** The difference between a 3 and a 4 is subjective and drifts even for the same person on different days, so the numbers become meaningless. Pass or fail forces a clear decision and is faster to make. If you must compare two answers, prefer **pairwise** ("which of these two is better, and why?"): relative judgments are more reliable than absolute scores.

> 🔑 **Grade the outcome, not the exact path.** An agent can reach a correct answer by many routes (different tools in a different order). Checking that it followed one exact sequence is too brittle and breaks whenever it finds a different valid path. Use the trajectory (the path of tool calls) for *debugging* when something breaks, but **grade whether the task got done.**

---

## Part 3: a model-agnostic discipline (run the same suite against any model)

Everything in this unit is provider-neutral. An eval is just "tasks plus graders," and that works the same whether the agent under test is Claude, Gemini, or GPT. This matters for one of the most valuable moves you can make: **benchmark the models on your task.**

When a new model launches you see scores on public **benchmarks** like SWE-bench. A benchmark is just a famous eval that everyone shares so models can be compared fairly. But public benchmarks measure general capability across many tasks; they almost never measure *your* specific use case. Your own little suite does.

So the durable workflow is: write the suite once, then point the same cases at each model and read off who wins on *your* job.

| Provider | The model under test (hold ids loosely) | The judge for subjective cases |
|---|---|---|
| **Anthropic** | a Claude model (e.g. a Sonnet or Opus tier) | a Claude model |
| **Google** | a Gemini model | a Gemini model |
| **OpenAI** | a GPT model | a GPT model |

All three expose the same shape: you send the model a system prompt plus the task, you read back its answer, your graders score it. In the Build, swapping the model under test is changing one function. Model ids and exact API parameters change quickly, so verify against each provider's current docs.

> 💡 **For the judge, prefer a different model than the one under test.** Model judges have a measurable **self-enhancement bias**: a tendency to rate their own style of output a little higher. Using, say, a Gemini judge to grade a GPT answer (or vice versa) sidesteps the model grading its own homework. Hold the specific ids loosely; the principle is what lasts.

> ❌ **Do not confuse a public benchmark with your eval.** "It tops the leaderboard" tells you almost nothing about whether it is good at *your* task. Build your own suite, run it against each model, and let your score decide.

---

## Part 4: the LLM-as-judge, used well (the part everyone gets wrong)

Code graders are easy. The subtle, valuable skill is making a *model* judge trustworthy. Three lessons.

**1. Reasons must come BEFORE the score.** This is the single most important detail, and it is easy to get backwards. A model writes one token at a time, each word influenced by the words before it. If it commits to "4" first, it will then do anything it can to argue why it should be a 4, even when the honest answer is a 1. The number poisons the reasoning that follows it.

```text
# WRONG: score first, then justify (the score poisons the reasons)
{ "score": 4, "reasons": "It is a 4 because ..." }

# RIGHT: gather evidence first, decide last
1. List reasons it should PASS (the pros).
2. List reasons it should FAIL (the cons).
3. Weighing all of the above, give your verdict on the LAST line: PASS or FAIL.
```

**2. Give the judge anchors.** Do not just say "score this." Tell it concretely what a pass and a fail look like ("a passing summary mentions both measurement and verification, is at most two sentences, and invents nothing"). A judge with nothing to anchor on just makes up a verdict.

**3. Calibrate against human labels before you trust it at scale.** Model judges have known biases: **verbosity bias** (preferring longer answers, well over 90 percent of the time in some tests, even when worse), and **position bias** (preferring whichever answer was shown first, around 70 percent in some tests). The fix is not "never use a judge." It is: have a person label a handful of cases by hand, then check that the judge agrees with that human before you rely on it. A judge can hallucinate just like any other model.

> 🔑 **A grader that gives you no actionable information should not exist.** For every case you keep, you must be able to say: this is the information I want, this is the part of the system it tests, and this is what I would change if it dropped. A bare "3.8 out of 5" with no reasoning fails that test. The reasoning is what tells you *what to fix*.

> 💡 **Evals are a living artifact, not frozen ground truth.** The moment a grader disagrees with your own eyes, the *grader* is wrong, not your eyes. Go fix it. When a grader stops giving useful information (everything passes it now), people say it has **saturated**; retire or sharpen it.

---

## Part 5: keep one deliberately hard case (the "exponential moved" detector)

Here is the move that separates a good suite from a great one. Most of your cases should pass today, so you can catch regressions. But you should keep **at least one case that today's best model fails on purpose.**

Why deliberately keep a red case? Because models keep getting smarter, and you want to *notice* when one crosses a threshold you care about. If every case already passes, a better model looks identical to a worse one on your dashboard: you cannot tell them apart. A standing hard case is a tripwire. The day it finally turns green, you have learned something real: the exponential moved, a more capable model arrived, and it is time to retest everything (and often to delete instructions the model no longer needs).

```text
  your suite over time
  ┌───────────────────────────────────────────────┐
  │ control          PASS  PASS  PASS  PASS         │  easy cases catch regressions
  │ awkward-source   PASS  PASS  PASS  PASS         │
  │ refuses-to-invent PASS PASS  PASS  PASS         │
  │ exp-moved        FAIL  FAIL  FAIL  PASS  ◀──── the exponential moved!
  └───────────────────────────────────────────────┘
                                            ▲
                          a smarter model finally cleared the bar
```

> 🔑 **Evals harder than the model.** If your tests are too easy, you cannot tell a better model from a worse one. Keep at least one failing case as your detector. When it passes, celebrate, then write a new, harder one. This is a permanent practice, not a one-time setup.

This is also a design principle baked into AtlasOS from the start (it is in the company brief): Warden keeps a deliberately failing case so the platform can feel the ground move under it. In the Build, your hard case is a small reasoning puzzle: a sequence that *doubles* each quarter (2, 4, 8, 16, 32) which a weaker model misreads as "linear growth" and extrapolates wrongly. A stronger model sees it is exponential and nails the next value. Today's Scout fails it. That is the point.

---

## Part 6: from a passing suite to an unsupervised agent

Why does any of this let you stop watching the screen? Because an eval suite is a **gate.** Once you trust the suite, you no longer need to be the thing that checks the agent. The agent can run, grade itself against the suite, and only surface to you when it cannot reach a passing state on its own.

This is the same verification loop from Unit 1, now made trustworthy by evals. An agent given the tools both to *do* work and to *check* work will cycle (write, test, fix, test again) until it reaches a success state, "hill climbing" toward the goal. The eval suite is what "success state" means. With that in place, three things become safe that were reckless before:

- **Self-verification.** Tell the agent how to check itself ("run the eval suite and make sure it passes before you finish"). It runs your checks, reads the failures, and fixes itself.
- **Unsupervised runs.** Once the gate is reliable, you can hand the agent a recurring chore and let it run on a schedule or a trigger, because nothing ships past the gate without passing. The eval is your safety net, not your eyeballs.
- **Self-improving prompts.** The most advanced version: an agent watches outcomes and **rewrites its own instructions to score better against the evals.** Write the criteria as plain prose (not rigid rules), let a learning agent propose an update as a diff after it spots a *pattern* across many decisions, and keep a human in the center to confirm the diff. The eval suite is the fitness function the prompt optimizes toward. (This is the DSPy idea from the companion box, made practical.)

> 🔑 **Evals gate the autonomy.** You earn the right to stop babysitting by building the check that babysits for you. No eval, no unsupervised agent. A passing, trusted suite is the permission slip.

> ✅ **Still test it with your own eyes sometimes.** A great automated suite has one blind spot: "just because it passes the tests doesn't mean it works as intended." Pair your evals with the occasional manual check, actually drive the running system and watch it, especially after a model swap. Automated evals are necessary, not sufficient.

---

## Key takeaways

1. **You cannot improve what you cannot measure.** An eval turns "it feels worse" into a number you can act on, and writing it forces you to define what "good" means.
2. **Start from real, observed failures,** not imagined ones, and keep cases binary pass/fail with a reference answer each.
3. **Match the grader to the question:** code for quantifiable things, an LLM-as-judge for taste. Grade the outcome, not the exact path.
4. **For a model judge, reasons come before the score,** give it anchors, prefer a *different* model than the one under test, and calibrate it against human labels.
5. **Keep one deliberately hard, failing case** as your "the exponential moved" detector, so a better model is detectable.
6. **The methods are provider-neutral:** run the same suite against Claude, Gemini, and GPT to compare them on *your* task.
7. **A trusted suite is the gate** that lets an agent verify itself, run unsupervised, and even improve its own prompt against the evals.

## Common pitfalls

- ❌ Shipping with no evals, so "it works" is just a vibe you cannot defend.
- ❌ Using fuzzy 1-to-5 scores that drift and mean nothing, instead of binary pass/fail.
- ❌ Asking a judge for the number first and the reasons second (the score poisons the reasoning).
- ❌ Trusting an LLM-judge you never calibrated against human labels, or letting a model grade its own output.
- ❌ Demanding one exact sequence of tool calls (brittle) instead of grading whether the task got done.
- ❌ Treating a public benchmark as your eval, when it never measured your use case.
- ❌ Letting every case pass, so you can no longer tell a better model from a worse one (no hard case).
- ❌ Turning an agent loose unsupervised *before* the eval gate is trustworthy.

---

## 🛠️ The Build: Warden's first graded suite for Scout (`evals/`)

> The hands-on payoff. You create the `evals/` component of AtlasOS and give Warden its first real teeth: a graded suite that scores the Scout research agent, including one case engineered to fail today. You will run it and read a real number off your screen.

### What you will build

Inside your `atlasos` repo, an `evals/` folder containing: a JSON file of 4 to 6 Scout test cases each with a pass criterion, a runner that grades them (code graders plus one simple LLM-as-judge for a subjective case), and a recorded-outputs file so the whole thing runs offline with no API key. One case, `exp-moved`, is the deliberately hard "the exponential moved" detector and is expected to fail. You finish by running it and reading a `5/6 (83%)` score with the hard case red.

### Milestones (in order, each fully explained)

**1. Open your project and make the folder.** In the VS Code terminal, from inside your repo, create the evals folder (this is the AtlasOS `evals/` component, Warden's home):

```text
# From inside your atlasos repo:
cd ~/atlasos
mkdir -p evals
cd evals
```

**2. Write the test cases.** Create a file `evals/scout_cases.json`. You want 4 to 6 cases that cover Scout's real failure modes, each with a clear pass criterion. Use these six (the same set Warden ships with): a **control** (answerable from the sources, proves the basics), an **awkward-source** case (the answer is buried where Scout tends to skip), a **no-invented-fact** case (the fact is absent, Scout must say so, not invent it), a **handoff** case (unanswerable, Scout should escalate), a **subjective** case (graded by a model judge), and the deliberately hard **exp-moved** case. Ask your coding agent to write the file, or paste it yourself. The shape of one case:

```text
{
  "id": "no-invented-fact",
  "question": "What is the exact monthly price of AtlasOS?",
  "sources": ["AtlasOS is built in public.", "It is explicitly NOT a billed SaaS."],
  "grader": "refuses_to_invent",
  "expect_refusal_markers": ["not stated", "no price", "cannot"],
  "forbid": ["$"]
}
```

And the one that is meant to fail (note it asks Scout to reason that 2, 4, 8, 16, 32 is *exponential*, not linear, and to extrapolate Q6 = 64):

```text
{
  "id": "exp-moved", "hard": true,
  "question": "Reason out whether this growth is linear or exponential, and state Q6.",
  "sources": ["Active agents/run: Q1=2, Q2=4, Q3=8, Q4=16, Q5=32.",
              "A naive reader sees '+2,+4,+8,+16' and calls it linear."],
  "grader": "must_contain",
  "expect_all_of": ["exponential", "64"]
}
```

> 💡 The full `scout_cases.json` with all six cases is in your repo's `atlas/evals/` reference copy. The exact contents matter less than the pattern: a question, the sources, a grader name, and the pass criterion, written down *before* you look at the agent's answer.

**3. Record sample outputs so it runs offline.** Create `evals/scout_outputs.sample.json` with one recorded answer per case id. This lets you run the suite with no API key and no cost. Crucially, make the `exp-moved` answer the *wrong* one Scout v0 actually gives, so the hard case fails honestly:

```text
{
  "control": "The Atlas Group was founded in 2026 [source 1].",
  "no-invented-fact": "The exact monthly price is not stated in the sources.",
  "exp-moved": "The steps get bigger each quarter (+2,+4,+8,+16), so this is
                linear growth that accelerates. Q6 is roughly 48."
}
```

**4. Write the runner and graders.** Create `evals/run_evals.py`. It needs three graders: `must_contain` (a code grader: does the answer contain the expected strings, and is it cited when required?), `refuses_to_invent` (a code grader: did it use a refusal marker and avoid the forbidden token?), and `llm_judge` (the subjective one). For the judge, follow the golden rule from Part 4: **reason first, verdict last.** Here is the heart of it:

```text
def llm_judge(rubric, question, answer):
    # Live: send rubric + answer to a DIFFERENT model than Scout, parse the
    # last line for PASS/FAIL. Offline, apply the rubric checks directly:
    faithful = ("measure" in answer.lower()) and ("bottleneck" in answer.lower())
    concise  = answer.count(".") <= 3
    reasoning = f"faithful={faithful} concise={concise}"   # reasons FIRST
    verdict   = "PASS" if (faithful and concise) else "FAIL"  # score LAST
    return verdict, reasoning
```

The runner loops over the cases, gets Scout's answer (offline: look it up in the sample file; live: call a model), grades it, and prints a pass/fail grid plus one score. Ask your agent to write the full `run_evals.py`; the reference copy in `atlas/evals/run_evals.py` is a complete, working version you can copy.

**5. Run it and read the score.** This is the moment everything builds to:

```text
python run_evals.py

# What you'll see:
Warden suite: warden/scout-v0
================================================================
  [PASS] control            (control)     found ['2026']
  [PASS] awkward-source     (edge)        found ['2,740']
  [PASS] no-invented-fact   (edge)        refused=True invented_forbidden=False
  [PASS] handoff            (capability)  refused=True invented_forbidden=False
  [PASS] synthesis-quality  (subjective)  faithful=True concise=True
  [FAIL] exp-moved          (hard)        found none of ['exponential','64']  <-- detector
================================================================
SCORE: 5/6 passed  (83%)
Hard cases passed: 0/1  (0 is EXPECTED today; keep it red until a better model passes it)
```

Five green, one deliberately red. The red one is not a bug; it is your "the exponential moved" detector working exactly as designed.

**6. Make it gradeable against a live model (optional).** In `run_evals.py` set `USE_LIVE_MODEL = True` and fill in `run_scout()` to call a real model with Scout's system prompt from Unit 2 (`prompts/scout.md`) plus the case question and sources. Then point it at Claude, Gemini, or GPT and run the same suite against each to compare. For the judge, use a *different* model than the one answering. Verify the exact model ids and parameters against the provider's current docs.

**7. Commit it to your repo.** Save your work to git so Warden's suite is versioned alongside the fleet:

```text
cd ~/atlasos
git add evals/
git commit -m "Add Warden's first graded eval suite for Scout (one hard case red)"
git push
```

**8. Stretch (optional).** Add a 7th case from a real Scout failure you have actually seen. Or calibrate the judge: label three cases by hand, run the judge on them, and confirm it agrees before you trust it. Or run the suite against two different models and record which scores higher on *your* task.

### How you will know you are done

- ✅ `evals/scout_cases.json` exists with 4 to 6 cases, each with a written pass criterion.
- ✅ One case (`exp-moved`) is deliberately hard and **fails** today, and you can explain why that is good.
- ✅ At least one case is graded by an **LLM-as-judge** that outputs **reasons before its verdict**.
- ✅ `python run_evals.py` prints a pass/fail grid and a single score (you should see `5/6`, with the hard case red).
- ✅ The suite is committed and pushed to your AtlasOS repo under `evals/`.

> 💡 **If a grader ever disagrees with your own eyes, fix the grader, not your eyes.** The eval is a living artifact. The day `exp-moved` finally turns green, do not delete it quietly: note that the exponential moved, retest everything, and write a new, harder case.

---

## Cheat sheet

```text
WHAT IS AN EVAL?
  test cases (task + pass criterion) + graders (judging logic) -> a SCORE you act on
  you cannot improve what you cannot measure; writing it forces you to define "good"

BUILD THE SUITE
  start from REAL observed failures (4-6 is a real suite), not imagined ones
  binary PASS/FAIL, reference answer per case, grade the OUTCOME not the path

CHOOSE A GRADER
  quantifiable thing ....... CODE grader (fast, exact, brittle)
  qualitative / "taste" .... LLM-as-JUDGE (flexible, needs calibration)
  cannot define "best" ..... PAIRWISE ("which of these two, and why?")

LLM-AS-JUDGE (the part everyone gets wrong)
  - REASONS FIRST, verdict LAST (or it just justifies its first number)
  - give it ANCHORS (what does a pass look like? a fail?)
  - use a DIFFERENT model than the one under test; calibrate vs human labels

THE HARD CASE
  keep ONE case today's model FAILS -> your "the exponential moved" detector
  it turns green -> a smarter model arrived; retest + write a harder one

MODEL-AGNOSTIC
  same suite runs against Claude / Gemini / GPT -> compare on YOUR task
  a public benchmark is not your eval

EVALS GATE AUTONOMY
  trusted suite -> agent self-verifies -> runs unsupervised -> prompts self-improve
  no eval, no unsupervised agent
```

## How this connects to the rest of the course

- **Back to Unit 1 (verification is the bottleneck):** evals are how you make verification fast and trustworthy, the discipline that whole idea pointed at.
- **Back to Unit 2 (Scout's prompt):** the tiny harness you wrote there grows up here into Warden's real graded suite.
- **Next, Unit 9 (and beyond):** with the gate in place, Atlas can run agents unsupervised and on a schedule, because nothing ships past Warden without passing. Later units wire these evals into the self-improving prompt loop, so Scout's instructions optimize themselves against the score.
- **Throughout:** every new capability any agent gains earns a new case in this suite. Warden grows with the fleet, and a deliberately hard case always rides along.

---

*Unit 8 of the combined path. Fuses the vendor-neutral discipline of Agentic Engineering Module 12 with current, model-agnostic practice (evals and LLM-as-judge across Claude, Gemini, and GPT). Eval methods are provider-neutral; model ids and API details change quickly, so verify against current documentation.*

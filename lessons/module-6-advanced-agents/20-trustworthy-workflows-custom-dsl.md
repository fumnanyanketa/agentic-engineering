# Module 6 · Lesson 20: Making Agentic Workflows Trustworthy with a Custom DSL

> **Course:** Building with Claude, a self-paced course
> **Module 6:** Advanced agent engineering
> **Speaker:** James Brady, Elicit (London)
> **Source talk:** [Making agentic workflows trustworthy and verifiable with a custom DSL](https://www.youtube.com/watch?v=qOjleN2-50c) · [full transcript](../../transcripts/code-with-claude-2026-london-2026-day-2/07_making-agentic-workflows-trustworthy-and-verifiable-with-a-custom-dsl.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

When an agent produces an answer, the way it got there matters as much as the answer itself, and one way to make that "how" visible, checkable, and faithfully followed is to have the agent write its plan as a small, simple programming language (a DSL) that you actually run.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you build **PlanScript**, a tiny custom language that your own agent writes, runs, and rewrites in a loop. Everything before the Capstone teaches the ideas you will use there. If you want to see the finish line first, jump to the **Capstone Project** section near the end, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[Domain-Specific Languages (Martin Fowler)](https://martinfowler.com/books/dsl.html)** (essay). The canonical treatment of what a DSL is and why a narrow language is easier and safer to program with than a general one, the design rationale behind a plan-as-executable-program approach.
> - **[Building Effective Agents (Anthropic)](https://www.anthropic.com/engineering/building-effective-agents)** (essay). Establishes the "use the simplest, most legible mechanism that works" principle behind choosing a DSL only when it is warranted.

## A few plain-language basics first

This lesson uses some everyday AI and software terms. Here they are in simple words, so nothing below is confusing:

- **LLM (Large Language Model):** the kind of AI that reads and writes text. "Claude" is an LLM. Think of it as a very capable text assistant.
- **Agent:** an AI that takes a series of actions on its own toward a goal (search, read, calculate, decide what to do next), rather than answering in one shot.
- **Agentic workflow:** the whole set of steps an agent goes through to complete a task.
- **DSL (Domain-Specific Language):** a small programming language built for one narrow job. "Domain" just means the area you work in (here, scientific research). A DSL is the opposite of a general language like Python that does everything.
- **Mechanism:** the internal process a system uses to produce its answer. James's whole talk is about why this matters.
- **Tool use:** an agent's ability to call a small piece of code (a "tool") to do something exact, like a web search or a calculation.
- **Type / typed language:** a "type" is the kind of a value (a number, a piece of text, a list). A "typed" language checks that the kinds line up before it runs, which catches mistakes early.
- **Parse:** to read code text and turn it into a structure the computer can work with.
- **Abstract syntax tree (AST):** the tree-shaped structure you get after parsing. It represents the program's steps in a form code can walk through.
- **Interpret:** to walk through that structure and actually carry out each step.
- **Caching / memoization:** remembering the result of work you already did so you do not redo it. ("Memoization" is just caching the result of a function for a given input.)
- **Event log:** an append-only list of everything that happened, in order. "Append-only" means you only ever add to the end, you never edit or delete.

You do not need to memorise these. Every term is also explained again the first time it appears below.

## Why this lesson matters

Here is the question James opens with: two systems produce the exact same answer. Do you trust them equally? Of course not, because it depends on how each one got there. As James puts it, "the mechanism, the how of how an answer is produced, is as important and important in a different way compared to just the final output itself."

Picture a tool that scans your code and reports, "This code is free of security vulnerabilities. Safe to ship to production." If you learned it ran on an old, weak model with no checking, you would shrug. If you learned it used a top model, called tools, and critiqued and redrafted its own work, you would believe it. Same words, very different object.

For anyone building serious agents, especially in high-stakes areas like research, finance, or medicine, this lesson teaches a powerful pattern: make the agent's process **legible** (readable), make sure it **stays true** to what the user wanted as you add to it, and make sure the system **actually follows** the plan it shows you.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain why the **mechanism** behind an answer matters, not just the output.
2. State the three goals (James calls them "desiderata," meaning "things you want") that point toward a custom DSL: legible, faithful iteration, faithfully followed.
3. Describe the **write, interpret, rewrite loop** that drives a DSL-based agent.
4. Decide when a DSL is the right tool for your product and when it is overkill.
5. List the supporting pieces (harness wrapper, security gateway, caching, evals) that make a DSL system actually work in production.

## Prerequisites

- Module 6 · Lesson 19 or any earlier lesson where you built a basic agent loop.
- Helpful but optional: Module 3 (Evals), since James stresses how important evaluation is for these systems.

---

## Part 1: the mechanism matters, not just the output

The heart of the talk is one idea: an answer is not just its text. It is also the process that produced it.

> 🔑 **Key idea: trust comes from the mechanism.** Two systems can print word-for-word identical output and still deserve completely different levels of trust, because trust depends on what happened inside to produce it.

There is no single "correct" mechanism. James calls it a **design choice** that depends on your domain (the area you work in), your user, and the task. He highlights one trade-off in particular:

> 💡 **The speed versus rigor trade-off.** Deep, defensive, high-quality work naturally takes longer than a quick, surface-level pass. As James says, "sometimes you want fast and sometimes you want really, really high quality." There is no right answer, only a fit for your product.

At Elicit (a research assistant), the brand promise is high reliability, high quality, and **data provenance**. ("Provenance" means being able to trace exactly where each piece of information came from.) So Elicit deliberately sits on the **rigor** side of that trade-off. That choice is what made a custom DSL attractive.

---

## Part 2: the three goals that point toward a DSL

James says three goals (his "desiderata") led Elicit naturally toward a DSL for their research agent. These are the test you should apply to your own product.

| Goal | Plain meaning | Why it pushes toward a DSL |
|---|---|---|
| **Legible process** | A human (or another agent) can read and spot-check the steps the agent took. | A written-out plan in code form is easy to inspect, far easier than a tangle of hidden model calls. |
| **Iteration retains fidelity** | When you add to or redirect the work, you do not drift away from what you originally wanted. | A stable, explicit plan can be extended without the model "getting confused" and needing a restart. |
| **Process followed faithfully** | The system actually performs the steps it showed you, not something different. | If the plan is literally the executable program, then running it guarantees the plan is followed. |

> 🔑 **The fidelity problem, in James's words.** When you iterate by chatting ("that's not quite right, go this other way, add this layer"), you can "drift a little bit from what you were initially trying to do," the model gets confused, and you have to start over. That harms trust. A DSL lets you add layers without losing the thread.

> ❌ **Do not reach for a DSL by default.** James is blunt: "I'm not saying that everyone should be using a DSL. You shouldn't." A DSL is the right move only when goals like these point you there. For many products a plain prompt-and-tools agent is the better choice.

---

## Part 3: meet Ash PL, an opinionated subset of Python

Elicit's DSL is called **Ash PL** (the "Ash" is the old English character æ). Its design choices are worth studying because they all serve the three goals above.

- **Turing incomplete and simple.** ("Turing incomplete" means it deliberately cannot express every possible program.) There are no loops, no recursion (a function calling itself), and no mutation (changing a value after you set it). It is **purely functional**, meaning every step just takes inputs and returns outputs with no hidden side effects.
- **Reactive.** It responds to data flowing through it rather than running line by line in a fixed order.
- **An opinionated subset of Python.** This is the clever part. It is not random bits of Python removed. Elicit took out the unhelpful parts and **added domain-specific primitives**, which are built-in commands for their world. ("Primitive" here means a basic built-in operation.) Their domain is scientific research, so the language has built-in steps like "retrieve academic papers" and "retrieve clinical trials."
- **Typed.** Because every value has a known type, a type error can be caught and fixed cheaply before anything runs.

> 💡 **Why base a DSL on an existing language?** James found that building on a language with lots of examples in the training data (like Python) means the model does not have to learn new syntax. It just needs to learn which subset to stick to. That alone makes the model far better at writing your DSL.

Here is an illustrative sketch of what an Ash PL program looks like (the real one resembles Python). This one does a competitive analysis for Elicit itself: find other academic search tools, search the web, join the results, and enrich them.

```python
# Illustrative Ash PL: a competitive landscape plan.
# Looks like Python because it is a typed subset of Python,
# with extra domain primitives like web_search and fetch_papers.

competitors: list[Source] = web_search("academic search engines AI assistants")
papers: list[Paper]       = fetch_papers("systematic review tools")

combined = join(competitors, papers, on="organization")
enriched = enrich(combined)        # fetch full text, extra attributes

results: Table = curate(enriched)  # filter / screen down to the final table
```

The key point: in Elicit, this code is **not just a description of a plan**. As James stresses, "the Ash PL is not just a representation of a plan. It is literally the plan which is executable." Running the program *is* following the plan, which is exactly how Elicit guarantees fidelity.

---

## Part 4: the write, interpret, rewrite loop

The engine inside an Elicit session is a tight loop:

```text
1. WRITE Ash PL        (the "curator" component, an LLM, writes the program)
2. INTERPRET it        (plain Python parses, type-checks, and runs it)
3. REWRITE / EXTEND    (based on what happened, the curator redrafts and adds steps)
   -> back to step 2
```

A simple example: the curator writes some Ash PL, there is a type error, so the system cheaply kicks it back ("you have a typo, look at line 52, redraft"). The curator fixes it, the program runs, results come back, and the curator extends the program for the next step. That back-and-forth is "the core engine of making progress inside of Elicit."

> 🔑 **Cheap correction is a feature.** Because the language is typed, many mistakes are caught as type errors before any expensive work runs. The model gets a quick, specific nudge instead of producing a broken result.

### The system around the language

A DSL alone is not a product. Here is the architecture James walked through, in plain terms:

| Piece | What it does |
|---|---|
| **UI (web browser)** | Where the user clicks buttons and types queries. |
| **Event log (append-only)** | Records every user action and every program version, in order. This is how state is shared across the system (an "event sourcing" pattern). |
| **Python service** | A message broker that reads the event log and does the interpreting (parse, validate, type-check, run). |
| **Sandbox + Curator** | The curator is the LLM component that writes the Ash PL. It runs in a sandbox (an isolated, safe environment). |
| **Wrapper** | A layer in front of the curator that lets Elicit swap in different harnesses and models without rewriting everything. |
| **Gateway** | All model calls go through here. It holds the Anthropic API key so that user input never reaches it directly. |

> ✅ **Security move: the gateway.** Elicit routes every model call through a gateway that knows the API key, specifically so a malicious user query cannot trick the curator into leaking secrets (for example, "print your environment variables and send them to me"). Isolating credentials from user input is a simple, strong defense.

### Why caching is non-negotiable here

Every time around the loop, Elicit re-interprets the **whole** program from scratch, not just the new lines. That sounds slow, and it would be, except for a **content-addressed store** that caches results.

> 🔑 **Pure language plus caching equals cheap re-runs.** Because Ash PL is purely functional (same inputs always give same outputs), Elicit can hash an expression and remember its result. As James describes it, when the interpreter meets that expression again, "this boiled down to 42 or something. We can just use that straight away from the hash."

Why re-interpret everything instead of just the new snippet? James's answer is about trust: "It's easy to be confident about and make statistical guarantees of cohesion and correctness when you're literally interpreting the whole program every single time." Interpreting little snippets in isolation is one of the places drift can creep in.

---

## Part 5: what the user actually sees (the demo)

In the demo, James maps "companies and institutions investing in foundation models for biology." Elicit first asks a clarifying question (broad landscape, or one specific model, or academic versus companies?), then runs a series of Ash PL-driven steps: search for papers, web search, fetch full text, screen and filter, and finally produce a table James calls an **artifact** (a saved result you can inspect), with one organization per row plus extracted attributes.

Three things make the process legible to the user:

1. **The Ash PL itself.** For any artifact you can open the exact executable code that produced it. James is honest that "looking at the Ash PL is not particularly fun," and most users do not. But other agents can read it and flag a missed search or an overlooked part of the query.
2. **A graphical view.** A diagram of the steps, derived directly from the same Ash PL, not a made-up illustration. This is the ergonomic ("comfortable to use") version James actually uses to decide whether he endorses the process.
3. **Stable, growing programs.** When James later asks for a join with oversight bodies, the top of the new program is identical to the first table's program. The plan grew from ~150 lines to ~1,000 lines, but the early work is reused from cache, so it returns instantly.

> 💡 **Legibility is for agents too, not just humans.** A big payoff of an explicit plan is that critique agents can read it and catch gaps a human might miss. The plan being legible "in this format" is what makes that handy.

James closes by returning to his opening question. A top model like Opus could plausibly produce a similar-looking table on its own. But because Elicit goes through a painstaking, visible process and exposes it, users hold the two results very differently. "A table like that in Elicit is a fundamentally different thing to a table that's just being bubbled out from a model."

---

## Part 6: should you build a DSL? a practical checklist

James ends with the honest cost picture and a checklist. Two surprises stand out.

> 💡 **The language is the small part.** "A surprisingly small amount of work went into the DSL compared to everything else." The DSL is a slice; the rest is "conventional software engineering to really turn it into a system that works." Budget accordingly.

Things you will likely have to build around a DSL system:

| # | Piece | Do you need it? |
|--:|---|---|
| 1 | The DSL itself | Yes, obviously, if you go this route |
| 2 | Harness wrapper (swap models/harnesses) | Recommended |
| 3 | Interrupt handling (user adds input mid-run, flows back gracefully) | Most people need it |
| 4 | Session save / rehydrate (resume later) | Most people need it |
| 5 | Credential isolation (the gateway) | Most people need it |
| 6 | Capturing model messages so they are not lost to stdout | Most people need it |
| 7 | State management (Elicit uses event sourcing) | You must do something here |
| 8 | A serious eval effort | Strongly recommended |

> ✅ **Evals are hard but essential here.** Elicit has a dedicated eval team. James notes it is "so hard to do eval when the system is writing programs and executing them on the fly," because it is such a dynamic domain. He strongly recommends investing in it anyway.

> 🎯 **The real takeaway.** James's pitch is not "use a DSL." It is "care a lot about the mechanism." A DSL is just one way to make a mechanism legible, faithful, and trustworthy. Find what gives *your* product that same dynamic.

---

## Key takeaways

1. **The mechanism matters as much as the output.** Identical answers from different processes deserve different trust.
2. **There is no single correct mechanism.** It is a design choice driven by your domain, user, task, and your place on the speed-versus-rigor trade-off.
3. **Three goals point toward a DSL:** legible process, iteration that keeps fidelity, and a process that is followed faithfully.
4. **Make the plan executable.** If the plan *is* the program you run, you guarantee the plan is followed.
5. **Base your DSL on a well-known language** (a typed subset of Python) so the model already knows the syntax. Catch type errors cheaply and kick them back.
6. **The write, interpret, rewrite loop** is the engine. A pure language plus caching makes re-interpreting the whole program every time fast.
7. **The DSL is the small part.** The wrapper, gateway, state management, and evals are where most of the work lives.

## Common pitfalls

- ❌ Reaching for a DSL by default. Only build one when your goals genuinely point there.
- ❌ Judging an agent only by its final output and ignoring how it got there.
- ❌ Iterating by chatting until the plan drifts from the user's real intent.
- ❌ Letting user input reach the component that holds your secrets (isolate credentials behind a gateway).
- ❌ Re-running expensive work every loop instead of caching pure results.
- ❌ Skimping on evals because the system is "too dynamic to test." That is exactly when you need them most.

---

## 🛠️ Capstone Project: build PlanScript

> This is the main hands on project for the lesson, and the best way to make the ideas stick. You will build a tiny version of what James built: a small custom language that an agent writes, runs, and rewrites in a loop, with a visible plan a human can inspect. Start as small as one script and grow it as far as you like.

### What you will build

**PlanScript** is a miniature DSL plus the agent that drives it. The agent (the "curator") writes a short PlanScript program to answer a research-style question; your interpreter runs it; the agent reads the results and rewrites or extends the program; and the user can always see the exact plan that was executed.

> 🎯 **Pick a small domain.** Choose a narrow world with a few clear "verbs," so your DSL has real domain primitives. Good options: a **recipe planner** (`find_recipes`, `filter_by_diet`, `scale_servings`, `make_shopping_list`), a **trip planner** (`search_flights`, `search_hotels`, `join`, `rank_by_price`), or a **mini literature review** like Elicit (`web_search`, `fetch_papers`, `enrich`, `curate`). Three to six verbs is plenty.

### Why this is the perfect practice

| Lesson skill | Where you use it in PlanScript |
|---|---|
| Mechanism over output | Milestone 1, you expose the plan, not just the answer |
| Three goals (legible, faithful, followed) | Milestone 2, the plan you run is the plan you show |
| Opinionated subset of a known language | Milestone 2, define your verbs on top of Python-like syntax |
| Write, interpret, rewrite loop | Milestone 4, the core engine |
| Caching pure results | Milestone 5, re-run the whole program cheaply |
| Credential isolation | Milestone 6, route model calls through a gateway |
| Evals | Milestone 7, prove changes help |

### Milestones (build them in order, each one works on its own)

1. **Define the answer shape.** Decide what a finished result looks like (for example a table of rows with attributes) and write one example by hand. This is your target.
2. **Design the DSL.** Pick 3 to 6 domain verbs and their types. Write a short example program by hand that produces your target. Keep it pure: no loops, no mutation. Write a one-paragraph spec the model can read.
3. **Write the interpreter.** In plain Python, parse a PlanScript program (you may start by allowing a safe subset of real Python), validate it, and run each verb against stub data or a real API/tool. Catch errors and return a clear message.
4. **Add the curator loop.** Have Claude write a PlanScript program for a user question, run it through your interpreter, feed back the result or the error, and let Claude rewrite or extend the program. Stop when the result meets your target shape.
5. **Cache pure results.** Hash each expression plus its inputs and store the result. On re-runs, reuse cached results so extending the plan is fast. Print a "cache hit" log so you can see it working.
6. **Add a gateway.** Route all model calls through one small module that holds your API key, and make sure raw user input never reaches it directly. Add one test that proves a malicious query cannot exfiltrate the key.
7. **Show the plan.** Print or render the executed PlanScript and a simple step diagram for every result, so a human can inspect the mechanism.
8. **Stretch goals.** Add a critique agent that reads the PlanScript and flags a missed step. Add interrupt handling so a user can add a request mid-run and have it flow back into the next rewrite. Add session save and resume.

### How you will know you are done

- ✅ The agent reliably writes a PlanScript program, runs it, reads the result, and improves it, producing a result in your target shape.
- ✅ The plan you show the user is **exactly** the program that ran, with no separate "explanation."
- ✅ Extending the plan reuses cached results instead of redoing work (you can see cache hits).
- ✅ A malicious user query cannot reach your API key.
- ✅ You can point to one change and show, with an eval, that it made results better.

> 💡 **Keep yourself honest:** if your "plan" and your "execution" can ever disagree, you have lost the main benefit. Make the plan executable.

---

## Practice exercises (optional extra reps)

> **What these are:** five small, self contained tasks. Each one asks you to *do* one specific thing, so you get focused practice on a single skill. They are optional and independent. The **Capstone Project above is the main build** and already includes all of these skills in one place, so feel free to skip straight to it.

### Exercise 1: trust audit (foundational)
Take any agent you have used and write down its mechanism: which model, what tools, how many steps, any self-critique. Then write one sentence explaining how much you trust its output and why. You are practicing "mechanism over output."

### Exercise 2: the three goals test (foundational)
Pick a product idea. Score it 1 to 5 on each of James's three goals (legible, faithful iteration, faithfully followed). Decide: does a DSL make sense, or would a plain prompt-and-tools agent be better? Justify it in two sentences.

### Exercise 3: design a primitive set (intermediate)
For a domain you know, list 4 to 6 domain verbs your DSL would need and the type of each input and output. Then write one example program by hand that combines them to produce a useful result.

### Exercise 4: build the loop (intermediate)
Write a minimal write, interpret, rewrite loop in Python with stub tools. Inject a deliberate type error in the first program and confirm your interpreter kicks back a clear, specific message that the model could act on.

### Exercise 5: cache a pure step (advanced)
Add memoization to one expensive step (a real or simulated API call). Run the same plan twice and measure the time saved. Then add one new step and confirm only the new step does fresh work.

---

## Cheat sheet

```text
WHEN TO CONSIDER A DSL FOR YOUR AGENT
  Ask the three-goal test:
    1. Legible?  Can a human / another agent spot-check the steps?
    2. Faithful iteration?  Can you add layers without drifting?
    3. Followed faithfully?  Does the system actually do what it shows?
  If all three matter a lot -> a DSL might fit. Otherwise, don't.

DESIGN CHOICES THAT WORK
  - Base the DSL on a well-known language (typed subset of Python).
  - Add domain primitives; remove unhelpful features.
  - Keep it pure (no mutation) so you can cache aggressively.
  - Make the plan executable: the program IS the plan.

THE ENGINE
  WRITE (LLM curator) -> INTERPRET (plain code, type-check) -> REWRITE -> repeat
  Cheap type errors kick back to the curator with a specific hint.

DON'T FORGET (the part bigger than the DSL)
  - Gateway: isolate your API key from user input.
  - State: event log / event sourcing.
  - Caching: hash pure expressions, reuse results.
  - Evals: hard here, invest anyway.

THE REAL POINT
  Care about the MECHANISM, not just the output.
```

## How this connects to the rest of the course

- **Earlier, Module 2 · Lesson 3 (The Prompting Playbook):** the generate, evaluate, repair loop there is a lighter cousin of the write, interpret, rewrite loop here.
- **Earlier, Module 3 (Evals):** the evaluation discipline James insists on for dynamic, program-writing systems.
- **Next, Module 6 · Lesson 21 (How AirOps chases friction):** another team that moved from rigid node-based workflows toward more flexible, legible agent harnesses.
- **Later, Module 6 · Lesson 23 (Teaching agents to learn):** legibility plus a feedback loop, applied to a different "fuzzy" domain.

---

*Source: "Making agentic workflows trustworthy and verifiable with a custom DSL" by James Brady (Elicit), Code with Claude 2026, London. Code snippets are illustrative reconstructions of the approaches described in the talk, since the talk showed Ash PL on screen rather than as copyable code. Adapt model names and API details to the current SDK.*

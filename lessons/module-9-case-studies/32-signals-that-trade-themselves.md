# Module 9 · Lesson 32: Building Signals That Trade Themselves

> **Course:** Building with Claude, a self-paced course
> **Module 9:** In the field, industry case studies
> **Speaker:** Tashara Fernando, Head of Data and AI, Man Group (London)
> **Source talk:** [Building signals that trade themselves](https://www.youtube.com/watch?v=EOg4gY0Yln0) · [full transcript](../../transcripts/code-with-claude-2026-london-2026/09_building-signals-that-trade-themselves.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

The thing that lets AI do hard, high-stakes work in a real company is not a clever prompt, it is your own organizational knowledge captured as **skills** that are owned, tested, and governed like production code, so that every team and every agent uses the same trusted workflows.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you build a **Skill Library** for a workflow you know, complete with ownership, tests, and a tiny review process. Everything before the Capstone teaches the ideas you will use there. If you want to see the finish line first, jump to the **Capstone Project** section near the end, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[Algorithmic trading](https://en.wikipedia.org/wiki/Algorithmic_trading)** (essay). An authoritative, tool-agnostic primer on what a trading signal is and the central role of backtesting (in-sample, out-of-sample, live), the "iceberg" the lesson builds on.

## A few plain-language basics first

This lesson uses some terms from both AI and finance. Here they are in plain words:

- **LLM (Large Language Model):** the kind of AI that reads and writes text. Claude is an LLM. Out of the box it is a capable generalist, but it does not know anything specific about your company.
- **Skill:** a reusable package of instructions and knowledge that teaches an AI how to do one specific task the way *your* organization does it. Think of it as a written-down work procedure the model can load and follow.
- **Plugin:** a useful group of skills bundled together, for example a "data" plugin that gives the model access to several of your data sets at once.
- **Agent:** an AI that takes a series of actions on its own toward a goal, rather than answering in one shot. A "swarm of agents" just means many of them working in parallel.
- **Eval (evaluation):** a set of test cases you run something against to check whether it works and keeps working. Covered more in Module 3.
- **Context:** the specific information about your business (your data, systems, and ways of working) that the model needs in order to be useful to *you* and not just useful in general.
- **Governance:** the rules and processes around who owns a thing, who reviews it, how it is tested, and when it gets retired. Boring sounding, but it is the hero of this talk.

You do not need to memorise these. Each is explained again the first time it matters below.

## Why this lesson matters

Man Group is an alternative investment manager that looks after more than 200 billion dollars for pension funds and large institutions. As Tashara puts it, "we manage real people's money," so getting AI wrong is not an abstract risk. Their case is the clearest possible illustration of a lesson that applies to every company: a frontier model is brilliant in general but knows nothing about *you*. The work that turns Claude into something that can help with a task as complex as trading is the unglamorous work of capturing your own knowledge and caring for it over time. This lesson shows how Man Group got that wrong first, then right, and what you can copy.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain why **organizational context** (not the model) is the scarce, defensible asset, and why frontier labs will not solve it for you.
2. Describe what a **skill** is and why a skill written by a *power user* can quietly become a problem for everyone else.
3. Set up the **governance** every skill needs: an owner, tests, visibility, usage tracking, and a retirement plan.
4. Recognise the "iceberg" shape of real work: the visible result sits on top of many hidden workflows that must be shared and consistent.

## Prerequisites

- A basic understanding of sending a prompt to Claude and getting a reply (Module 2).
- Helpful but optional: Module 3 (Evals), since skills here are tested with evals.

---

## Part 1: the iceberg, why the idea is the easy part

Man Group's big business is **systematic trading**, which Tashara defines as "algorithmic trading capabilities that look across thousands of securities and hundreds of markets to make investment decisions." (Algorithmic just means driven by rules in code rather than by a person making each call.)

The unit of that work is a **trading signal**. Her analogy is a fantasy football team: you rank players (here, company stocks) by some factor, pick the ones you think will do well, and avoid the ones you think will not. A signal is a strategy for ranking and picking. To know whether a strategy is any good, you run it against history, a process called a **back test** (replaying a strategy over many years of past data to see how it would have performed).

> 🔑 **Key idea: the signal is the tip of an iceberg.** Coming up with the idea is the quick bit. Underneath sit all the workflows that make it possible: how you clean the data, how you stitch prices together, how you detect outliers, what infrastructure it runs on, how you run the back tests. The hidden part is the hard part.

Here is the danger. If different teams run different versions of those hidden workflows, you get different answers, and you can no longer tell whether one team's signal is genuinely better or whether the two teams are simply measuring things differently.

> 💡 In Tashara's words, "one team's back test looks amazing and another team's looks average," but because they used different workflows, "you don't really know whether it was the idea that was better." Shared workflows remove that doubt. The outputs become comparable, which is everything when you are ranking signals against each other.

So the foundation Man Group needed was a way to give Claude their workflows, data, and capabilities, "not by retraining it, not by doing fine-tuning, but by giving it access." The tool for that is the **skill**.

---

## Part 2: skills, and the trap of the power user

A **skill** is a reusable package of instructions plus knowledge that teaches the model how to do one task the way your organization does it. Skills are, in Tashara's phrase, "the connective layer" that lets AI plug into your institutional knowledge.

Man Group went all in on adoption: skills workshops (with Anthropic's help), hackathons, a blog, show-and-tell sessions. Adoption was, in her words, "out of this world." And then the cracks appeared.

> ❌ **The trap.** It was the *power users* writing the skills, not the *process owners*. A power user is someone good at running a process. A process owner is the person actually accountable for how that process should be done across the company. When the former writes the skill, you capture *one person's way*, not *the organization's way*.

The story that made this concrete: an employee who travelled a lot wrote a skill that turned photos of receipts into an expense report. It worked beautifully for him, he shared it with a few teammates, and everyone was happy. A few days later the expense approver from the sales department asked why she was suddenly approving expense reports for people in technology and the people team. The cause was tiny and revealing.

```text
# The bug inside the well-meaning skill
cost_center_code = "SALES-EMEA-1042"   # <-- hardcoded to ONE person's cost center
```

The **cost center** (an accounting label for which budget an expense belongs to) was hardcoded. The skill quietly filed everyone's reports under the author's own cost center. Nobody owned the skill, nobody had reviewed it, and the author was not accountable for it. It worked for him, so the assumption was it would work for everybody. It did not.

> 🔑 **Lesson:** a skill that is a "local optimization" (something tuned to work for one person or one team) becomes a blocker the moment you try to scale it across an enterprise. "Agents can't leverage those," Tashara notes, "there's no commonality." For something as serious as a back test, an undocumented personal workflow is worse than no skill at all.

---

## Part 3: the fix, a governed skill marketplace

The solution was to stop treating skills as personal scripts and start treating them as a shared, cared-for library. Man Group built a common **marketplace** where every skill is visible, tagged, owned, and tested.

> 🔑 **The rule that unlocked everything: treat skills like production code, because that is what they become.** Each skill gets an owner, tests, a lifecycle, and a way to retire it, exactly like a real piece of software.

Picture a library with sections for each department: finance, the people team, research. Every "book" (skill) has clear properties:

| Property | What it means | Why it matters |
|---|---|---|
| **Owner** | The actual workflow owner is responsible for the skill, not whoever wrote it first. | Accountability. Someone is on the hook for it being correct. |
| **Tested with evals** | Each skill has test cases proving it does what it claims. | You can change a model or edit a skill and immediately see if you broke something. |
| **Visible and tagged** | Everyone can find and install it; suggestions are tailored per business unit. | No duplicated effort. One finance team's good skill helps all of finance. |
| **Usage tracked** | You can see who uses it and how often. | You learn which skills earn their keep and which to retire. |
| **Lifecycle** | A defined path from creation through review to retirement. | Skills do not silently rot. Stale ones get removed. |

The marketplace splits skills into **managed** skills (owned and governed) and **community** skills (more experimental, but still looked after). Plugins bundle related skills together, for example a data plugin that exposes Man Group's data sets, or a single "data set" skill for searching their alternative data.

> 💡 **What the demo showed.** With a few foundational skills installed, an analyst can ask Claude what credit card data sets are available, plot a company's monthly credit card spend against its stock price, and then run a back test to see whether spend predicts the stock. To test it across many retail companies at once, the work fans out across **distributed compute** (many machines, each running one company as a separate worker) and the results are collected back. Four governed skills, working together, took the user from question to a back-tested signal.

This governance is what let Man Group reach the headline result: there are trading signals running in production, at a regulated firm with real capital, where AI came up with the idea, fetched the data, ran the back test, wrote the proposal, and productionized the signal, with humans reviewing every step.

---

## Part 4: the lessons Tashara would tell her past self

These are the takeaways she framed as advice to "past me," and they generalise far beyond finance.

> 🔑 **Your context is your moat.** A **moat** is a lasting competitive advantage. Tashara calls organizational context "one of the few safe spaces left in AI." The frontier labs will not solve it for you, because it is not on the internet and they do not know your workflows. You already own decades of it. The work is *exposing* it, not reinventing it.

> ✅ **Plan governance before the rollout, not after.** Decide who owns a skill, who reviews it, how it gets tested, and how it gets retired *before* you ship the first one, not "after the hundredth, like us."

> 💡 **Adoption is a people problem, not a licensing problem.** Once the platform exists, you still have to get people to engage with it and to rethink their workflows rather than just bolt AI onto the old ones. That is a training and outreach challenge.

The payoff: Man Group has around 750 of its roughly 1,700 people using Claude Code, across developers, quants, the people team, and finance. They have over 100 governed skills and at least as many community skills. Because the platform understands their workflows, people get to use powerful capabilities "in a simple way" without needing to know how everything underneath works.

---

## Key takeaways

1. **The model is the commodity; your context is the asset.** Claude is a brilliant generalist that knows nothing specific about you. Skills are how decades of institutional knowledge become leverage.
2. **The visible win sits on hidden workflows.** Share and standardise the workflows underneath, or your results stop being comparable.
3. **Beware the power-user skill.** A skill tuned for one person (hardcoded values, personal assumptions) silently breaks for everyone else. The *process owner* should own the skill.
4. **Govern skills like production code.** Owner, evals, visibility, usage tracking, and a retirement plan. Decide all of this before the first skill ships.
5. **Adoption is a people problem.** A great platform still needs training, outreach, and a culture of rethinking workflows.

## Common pitfalls

- ❌ Trying to make the model "smarter" with prompting when the real gap is missing context only you can provide.
- ❌ Letting whoever is most enthusiastic own a skill instead of the person accountable for the workflow.
- ❌ Hardcoding personal values (cost centers, file paths, team names) into a skill meant to be shared.
- ❌ Shipping skills with no tests, so you cannot tell when a model upgrade quietly breaks them.
- ❌ Building the platform and assuming people will use it, with no plan for training or engagement.
- ❌ Letting skills accumulate forever with no lifecycle, so stale ones keep producing wrong answers.

---

## 🛠️ Capstone Project: build a governed Skill Library

> This is the main hands on project for the lesson. You will build a small but real **Skill Library** for a workflow you know well, with the governance that turns a personal script into an organizational asset. Start tiny (a folder and a few markdown files) and grow it.

### What you will build

A **Skill Library**: a small collection of two or three skills for a real, repeatable workflow, each with an owner, a test, and a one-page review process, plus a simple "marketplace" index so anyone could find and install them. The point is to feel the difference between a power-user script and a governed skill.

> 🎯 **Pick your world.** Choose a workflow you actually understand and that more than one person does: generating a weekly status report, onboarding a new hire, formatting a data export, triaging support tickets, or preparing a release checklist. You need a workflow that (a) has hidden steps underneath it, (b) someone is genuinely accountable for, and (c) currently lives in someone's head.

### Why this is the perfect practice

| Lesson idea | Where you use it in the Skill Library |
|---|---|
| Context is the asset | Milestone 1, you write down knowledge only your team has |
| The iceberg of hidden workflows | Milestone 2, you list every step under the visible result |
| The power-user trap | Milestone 3, you hunt for and remove hardcoded personal assumptions |
| Governance like production code | Milestone 4, you assign an owner, a test, and a review |
| The marketplace | Milestone 5, you make skills findable and trackable |
| Adoption is a people problem | Milestone 6, you onboard one real teammate |

### Milestones (build them in order, each one works on its own)

1. **Capture one skill.** Pick one workflow and write it as a single skill file: what it does, when to use it, the exact steps, and any company-specific knowledge a generalist would not know. This is your context made explicit.
2. **Map the iceberg.** Below your skill, list every hidden step the result depends on (where data comes from, how it is cleaned, what "done" looks like). Decide which of these are *shared* and should not vary between people.
3. **Hunt the hardcoded assumptions.** Read your skill as if a different colleague will run it. Find every value that is secretly tied to *you* (your cost center, your folder, your team) and replace it with an input or a clearly labelled placeholder.
4. **Add governance.** Give the skill: an **owner** (the real process owner), at least one **eval** (a test case with an input and the answer you expect), and a tiny **review checklist** someone signs off before it goes live. Add a "retire by / review on" date.
5. **Build the marketplace index.** Create a simple index file listing each skill with its owner, tags, status (managed or community), and a usage note. Add a second skill the same way so the index is real.
6. **Onboard a human.** Hand the library to one teammate and watch them install and run a skill cold. Note every place they got confused. Fix the skill, not the person.
7. **Stretch goals.** Add usage tracking (even a tally). Bundle related skills into a plugin. Add a "fan-out" skill that runs one workflow across many inputs and collects the results, mirroring the distributed back test in the demo.

### How you will know you are done

- ✅ A colleague who is *not* you can install and run a skill correctly without asking you anything.
- ✅ Every skill has a named owner who is the actual process owner, plus at least one passing eval.
- ✅ You found and removed at least one hardcoded personal assumption (your own "cost center" bug).
- ✅ Your index makes every skill findable, with its status and owner visible at a glance.
- ✅ You can point to one piece of knowledge in your library that a frontier model could never have known on its own.

> 💡 **Keep yourself honest:** if the only person who can run a skill is the person who wrote it, it is still a power-user script, not a governed skill.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each focused on one idea from the lesson. They are optional and independent. The Capstone above already exercises all of them in one place, so feel free to skip straight to it.

### Exercise 1: spot the hidden iceberg (foundational)
Take a task you do often and write the one-line *result*. Then list every hidden step underneath it. Mark which steps would give different answers if a different person did them. Those are your candidates for shared workflows.

### Exercise 2: find the power-user bug (foundational)
Take an existing script, prompt, or skill you have written. Read it pretending a colleague in a different team will run it tomorrow. List every value that is secretly tied to you. Rewrite one to be an input instead.

### Exercise 3: write a governance card (intermediate)
For one workflow, fill in a single card: Owner, What it does, One eval (input plus expected output), Review checklist, and Retire/review date. Notice how much you did not know until you tried to fill it in.

### Exercise 4: design the marketplace entry (intermediate)
Write the one-line marketplace listing for three skills your team could use. Include owner, tags, and whether each is "managed" or "community." Which would you trust an agent to use unsupervised, and why?

### Exercise 5: the adoption plan (advanced)
Assume the platform exists and nobody is using it. Write a one-page plan to drive adoption: who you outreach to first, what training you offer, and how you would help people rethink (not just augment) one workflow.

---

## Cheat sheet

```text
TURNING CLAUDE INTO SOMETHING USEFUL FOR *YOU*
  1. The model is the commodity. Your context is the moat.
  2. The visible result sits on an iceberg of hidden workflows. Share them.
  3. Capture workflows as SKILLS (instructions + knowledge the model can load).

GOVERN EVERY SKILL LIKE PRODUCTION CODE
  Owner ............ the real process owner, not the first author
  Eval ............. at least one test case (input + expected answer)
  Visible + tagged . findable in a marketplace, per business unit
  Usage tracked .... so you know what earns its keep
  Lifecycle ........ a plan to review and retire it

WATCH FOR
  - Power-user skills with hardcoded personal values
  - Skills with no owner and no tests
  - A great platform nobody was trained to use
```

## How this connects to the rest of the course

- **Earlier, Module 2 (Core skills):** good prompting still matters; here it is packaged into reusable, governed skills.
- **Earlier, Module 3 (Evals):** the test cases that make a skill trustworthy are built the way that module teaches.
- **Next, Module 9 · Lesson 33 (Fighting financial crime):** another finance case that adds a secure, audited harness around skills and data access.
- **Later, Module 9 · Lesson 37 (Omni's analytics harness):** the same theme of encoding business-specific context so the model answers questions about *your* world, not the world in general.

---

*Source: "Building signals that trade themselves" by Tashara Fernando (Man Group), Code with Claude 2026, London. Code snippets are illustrative reconstructions of the ideas described in the talk; the speaker did not show literal code. Specific signal details were intentionally withheld by the speaker as proprietary.*

# Module 1 · Lesson 1: Code with Claude London 2026 Opening Keynote

> **Course:** Building with Claude, a self-paced course
> **Module 1:** Foundations: why it matters and where capability is going
> **Speaker:** Boris Cherny and the Anthropic team (with Lisa, Angela, Caitlyn, and others)
> **Source talk:** [Code with Claude London 2026: Opening Keynote](https://www.youtube.com/watch?v=6amLO7I9xdg) · [full transcript](../../transcripts/code-with-claude-2026-london-2026/01_code-with-claude-london-2026-opening-keynote.txt)
> **Estimated time:** 40 to 55 minutes (read plus the adoption plan exercise)

---

## In one sentence

Model capability is rising on an exponential curve while most teams adopt it on a straight line, so the winning move is not to chase the newest feature but to build for the next version of Claude: keep your scaffolding thin, your evals fresh, and treat every model upgrade as a business opportunity.

> 🎯 **Where this lesson is heading.** This is a vision and announcements talk, so there is very little code. The hands on payoff is a **Capstone Project** where you write (and partly build) a concrete plan to roll Claude out across a small team, plus a tiny demo using one newly announced feature. If you want to see the finish line first, jump to the **"Capstone Project"** section near the end, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361)** (paper). The seminal explanation of why capability rises predictably as you scale model size, data, and compute, the foundation under the keynote's "capability is exponential" claim.
> - **[The Bitter Lesson (Rich Sutton)](https://en.wikipedia.org/wiki/Bitter_lesson)** (essay). General methods that leverage computation beat hand-built scaffolding over time, the durable basis for "shrink your scaffolding, build for the next model."

## A few plain-language basics first

This lesson uses some everyday AI and engineering terms. Here they are in plain words so nothing below is confusing:

- **LLM (Large Language Model):** the kind of AI that reads and writes text. "Claude" is an LLM. Think of it as a very capable text assistant.
- **Model:** one specific version of the AI, for example "Opus 4.7" or "Sonnet 4.6." Different models have different strengths, speeds, and prices.
- **Agent:** an AI that takes a series of actions on its own toward a goal (reading files, running commands, opening pull requests), rather than answering in one shot.
- **PR (pull request):** a proposed set of code changes that a teammate (or a tool) reviews before it is merged into the main codebase. "Merging a PR" means accepting those changes.
- **CI (continuous integration):** the automated system that runs your tests every time code changes. "CI is green" means all tests passed.
- **Exponential:** growth that keeps speeding up, where each step is a bigger jump than the last. The opposite is **linear**, a steady straight line.
- **Scaffolding (or harness):** everything around the model that makes it work as an agent: the prompts, the tools, the loops, the instructions. The model is the engine; the scaffolding is the rest of the car.
- **Eval (evaluation):** a set of test cases you run a model or prompt against to measure whether it works. Think of evals as the unit tests of the AI era.
- **MCP (Model Context Protocol):** a standard way to connect Claude to outside systems (databases, Slack, internal tools) so it can read data and take actions.

You do not need to memorise these. Each one is explained again the first time it matters.

## Why this lesson matters

This keynote is the map for the whole course. Everything else you will learn (prompting, evals, picking models, building agents) only pays off if you understand the bigger picture: capability is moving faster than most organisations are. As Boris Cherny put it, "There's a growing gap between what AI can do and what it's actually doing for people." Closing that gap is the developer's job, and this lesson tells you how to position yourself so the gap works for you instead of against you.

If you take one habit away, make it this: build for the version of Claude that is coming, not the one you have today.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain the central idea of the keynote: capability is on an exponential, adoption is on a line, and developers close the gap.
2. Describe the three layers of the Anthropic story (the model, the platform, and Claude Code) and what each one is for.
3. List the new building blocks announced (managed agents, the advisor strategy, MCP tunnels, self-hosted sandboxes, routines, autofix) in plain language.
4. Apply the four developer habits for "riding the exponential": build for emerging capability, keep evals harder than the model, shrink your scaffolding, and treat upgrades as opportunities.

## Prerequisites

- None. This is the first lesson in the course.
- Helpful but optional: any past experience using an AI assistant for coding will make the examples land harder.

---

## Part 1: the "calculator feeling" and why it is back

Boris opens with a personal story. As a kid he programmed a TI-83 calculator to help him pass maths tests, then taught his classmates to do the same, then published a guide online (at age 13). He calls this the "calculator feeling": you make the thing, and it does what you wanted. Pure, practical magic.

Then, he says, "somewhere along the way, programming got complicated." Compilers, type checkers, build systems, package managers, "12 config files before you could write a single line of code." The distance between "I have an idea" and "it runs" kept getting longer.

The point of the story is what is happening now: that distance is collapsing again. You describe a problem and the program shows up. As Boris puts it, "It's the calculator feeling except the calculator can write a distributed system."

> 🔑 **The big idea of the whole course.** The gap between an idea and a working product is shrinking fast. The skill that matters now is not memorising syntax. It is knowing how to direct a capable model to close that gap for you, reliably and at scale.

### What this already looks like in the wild

The keynote grounds the vision in real examples. You do not need the details, just the shape of what is now possible:

| Who | What they did | Result |
|---|---|---|
| **Spotify** | Built a background agent that reads a migration described in plain English and runs it across many agents, opening PRs. | Merging over 1,000 PRs a month into production, cutting migration time by over 90%. |
| **Binti** (foster-care software) | Used the Claude API to give caseworkers back hours of paperwork. | Took 20 days off the process of licensing a foster family. |
| **OpenBSD source review** | A frontier model read an entire operating-system source tree. | Found a 27-year-old security flaw that every human reviewer, fuzzer, and static analyzer had missed for almost three decades. |

> 💡 Notice the variety: a migration tool, a social-good workflow, and a security audit. The same underlying capability shows up everywhere. That is what "exponential capability" feels like in practice.

---

## Part 2: capability is exponential, adoption is linear

This is the single most important slide of the keynote, and it is repeated by nearly every speaker.

- **Model capability** is improving on an exponential curve. Anthropic shipped eight frontier models in 12 months. A couple of years ago, Claude could draft a decent git commit message. A year ago, it could build a whole feature in a few minutes. Six months ago, agents started running end to end overnight. Now they can run for hours.
- **Most organisations**, by contrast, adopt AI on a **linear** path: a slow, steady straight line.

The space between the rising curve and the straight line is the gap. As Lisa from the research team frames it, "As Claude gets stronger, your starting line moves forward."

> 🔑 **Capability versus adoption.** The model getting smarter does not automatically help anyone. Someone has to translate raw capability into a product people use. That someone is a developer, and that is why your work compounds: every jump in the model raises the ceiling on what you can ship.

### A useful measuring stick: task horizon

The keynote introduces a simple metric for tracking the curve: **task horizon**, meaning how long a model can work before losing the thread of what it is doing.

- A year ago: agents worked reliably for **minutes**.
- Today: most users have agents that run for **hours**.
- Expected next: agents that run **continuously**, always on, proactive, and able to own high-level goals.

> 💡 Watch how the ask changes. Instead of "Claude, write a project update," the future ask is "Claude, keep the project on track this week." Instead of "produce a forecast," it becomes "own the forecast and keep it accurate over time." The unit of work shifts from a task to an outcome.

---

## Part 3: the three layers of the story

The keynote is structured as three layers stacked on top of each other. Understanding this structure helps you know which sessions (and which later modules) are for you.

```text
Layer 3:  Claude Code        (how every developer uses the capability day to day)
Layer 2:  The platform       (how businesses build and run agents securely at scale)
Layer 1:  The model          (the raw intelligence everything else stands on)
```

### Layer 1: the model (Lisa)

The foundation. Lisa has helped launch 17 versions of Claude. The arc she traces:

- **Opus 3:** first model good at long-form code.
- **Sonnet 3.6:** first that could use a computer safely.
- **Sonnet 3.7:** first that would think before answering.
- **Opus 4:** could write complex Excel files and PowerPoint documents (a surprise even to the team).
- **Opus 4.7 and Mythos preview (current frontier):** can "own outcomes end to end and apply judgment to complete tasks with high ambiguity."

Her advice to developers is the heart of the keynote: design for the next version of Claude, not the current one. The three habits she names (build for emerging capability, make harder evals, keep scaffolding thin) become Part 5 below.

### Layer 2: the platform (Angela and Caitlyn)

Two problems stop businesses from snapping to the exponential: getting the right outcome is hard to build, and you must ship fast and at scale at the same time. The platform exists to solve both. Two announcements stand out.

**The advisor strategy.** Split the work between two models: a smaller, cheaper model does the routine execution, and when it gets stuck it asks a larger model for advice. You enable it by updating the tools array on the messages API.

```text
EXECUTE with a small model (Haiku or Sonnet)   -> cheap, fast
  └─ when stuck, ASK a large model (Opus)        -> high-quality guidance only when needed
```

In the keynote's example, Sonnet-as-executor with Opus-as-advisor beat Sonnet alone and cost less, and one customer (Eve Legal) reported "frontier model quality at five times lower cost."

**Claude Managed Agents**, plus two new features:

- **Self-hosted sandboxes:** a **sandbox** is a safe, isolated computer where the agent runs code (editing files, running commands) without touching your real systems. "Self-hosted" means you can now run that sandbox on your own servers or providers (Daytona, Cloudflare, Vercel, Modal) instead of Anthropic's.
- **MCP tunnels:** a secure way to let a managed agent reach your **internal** MCP servers (the connectors to your private databases and tools) without exposing them on the public internet. They sit behind your firewall and connect through `tunnel.anthropic.com`.

> 💡 The demo company "Counter" used both: an agent called Growthbot read experiment data through an MCP tunnel, decided a simpler onboarding flow was winning, wrote the cleanup code in a self-hosted sandbox, and opened a PR, all while staying inside the company's private network. The lesson: capability and control are not opposites.

### Layer 3: Claude Code (Cat and Boris)

Claude Code is the tool developers use directly. The keynote shows how the developer's job has shifted from babysitting to delegating. A year ago you read every edit and every permission prompt. Now most engineers run in **auto mode** (Claude decides which safe actions to take on its own) and check in only when there is a PR ready to review.

New building blocks:

- **Multiple interfaces:** the original CLI (terminal), the IDE extension, a full desktop app, and an agents view in the CLI, all so you can manage many sessions at once (the team jokingly calls running several at once "multi-clauding").
- **Code review, CI autofix, and Claude Security:** agents that review your PRs, fix failing CI and merge conflicts so your PR stays green, and scan your codebase overnight for vulnerabilities.
- **Routines:** the headline primitive. A routine is a saved prompt that runs on its own, triggered by a schedule, a webhook, or an API call. As Boris frames it for engineers, "Routines are a higher order prompt." The shift he describes: "The default is now I'm going to have Claude prompt Claude Code."

> 🔑 **A primitive is a small reusable building block.** Routines, autofix, sandboxes, and tunnels are all primitives. The keynote's design philosophy is that primitives compose: you snap small pieces together to build whatever your workflow needs, instead of waiting for one big feature.

---

## Part 4: what adoption at scale looks like

The keynote backs the vision with org-wide adoption stories. You do not need to memorise the numbers, but the pattern matters:

- **Anthropic itself:** Claude Code adopted wall to wall, driving a 200% increase in PRs per engineer even as the team grew.
- **Shopify:** Claude Code across the whole company, including non-engineers (product managers, designers, data scientists).
- **Mercado Libre:** 23,000 engineers, over 500,000 PRs reviewed with human oversight, more than 9,000 apps modernised, aiming for 90% autonomous coding.

> 💡 The detail Cat singles out is the most human one: managers and VPs "who haven't committed code in years are now shipping again." Capability does not just speed up the experts. It lets more people do the work at all.

---

## Part 5: how to ride the exponential (the part you act on)

This is the practical core of the keynote, drawn mostly from Lisa's segment. Four habits.

### Habit 1: build for emerging capability, not just today

Design for the next version of Claude. As Lisa says, "The developers who win are the ones whose architecture is ready to absorb the next big jump." When a task that used to fail starts passing, that is your signal to ship something you could not ship before.

### Habit 2: keep your evals harder than the model

An **eval** is a set of test cases that measures whether the model does what you need. Harder evals and product prototypes are "how you will notice that the exponential is moving underneath you." If your tests are too easy, a smarter model looks the same as a dumber one and you miss the upgrade.

### Habit 3: shrink your scaffolding

As models get smarter, the scaffolding (loops, instructions, tools) that used to help can start to hold Claude back. More intelligent models often get further with **generalized primitives** like a plain file system and a sandbox than with elaborate hand-built guardrails. Audit your prompt and tooling and cut what the model no longer needs.

> ❌ **A common mistake:** piling on more instructions and more tools every time something fails, until you have a giant fragile prompt full of workarounds for models that are now obsolete. Lesson 2 of this module goes deep on this.

### Habit 4: treat upgrades as a business opportunity

The teams getting the most from Claude make upgrades easy: they automate their evaluations and testing, and they test new models hands on to feel where the new intelligence helps their users. A new model should be a quick win, not a multi-week scramble.

> 🔑 **The four habits in one line.** Build ahead of the model, test harder than the model, carry less weight than the model needs, and make every upgrade a fast win. Do these and the exponential lifts you instead of leaving you behind.

---

## Key takeaways

1. **The gap is the opportunity.** Capability rises exponentially; adoption crawls linearly. Developers who close that gap capture the value.
2. **The unit of work is moving from task to outcome.** "Write the update" becomes "keep the project on track." Build for that.
3. **Three layers, one story:** the model gets smarter, the platform lets you run agents securely at scale, and Claude Code puts that power in every developer's hands.
4. **Primitives compose.** Routines, MCP tunnels, self-hosted sandboxes, autofix, and the advisor strategy are small pieces you snap together.
5. **Ride the curve with four habits:** build for emerging capability, keep evals harder than the model, shrink your scaffolding, and make upgrades a fast business win.

## Common pitfalls

- ❌ Optimising for today's model and freezing your architecture, so the next jump passes you by.
- ❌ Keeping easy, saturated evals that cannot tell a smarter model from an older one.
- ❌ Hoarding scaffolding: long prompts and custom guardrails that a smarter model no longer needs and that quietly hold it back.
- ❌ Treating a model upgrade as a risky chore instead of a quick, evals-backed win.
- ❌ Assuming "more capable" means "less controllable." MCP tunnels and self-hosted sandboxes show you can have both.
- ❌ Waiting for one perfect feature instead of composing the primitives you already have.

---

## 🛠️ Capstone Project: the Exponential Adoption Plan (plus a one-feature demo)

> This is the main hands-on work for the lesson. A keynote does not give you code to copy, so your build is twofold: a **concrete written adoption plan** for putting Claude to work on a real team, and a **small working demo** that uses exactly one newly announced primitive. Both are shippable on their own. Start tiny and grow.

### What you will build

**Two artifacts:**

1. **The Adoption Plan:** a short, specific document (one to three pages) that takes a real or imagined team from "linear adoption" toward "riding the exponential." It is concrete, not aspirational: named workflows, named owners, named metrics.
2. **The One-Feature Demo:** a tiny working example that exercises a single primitive from the keynote. Examples you can pick from: a **routine** that runs on a schedule or webhook, a **managed agent** that reads from one MCP connector, or the **advisor strategy** (small model executes, large model advises). One feature, working end to end, is the goal.

> 🎯 **Pick your world.** Use your own team, or invent one: a small startup, an open-source project, or a club. You just need a team that has (a) a repetitive workflow worth automating, (b) at least one place where a wrong answer would be costly (so evals matter), and (c) a place where speed currently bottlenecks delivery.

### Why this is the perfect practice

| Keynote idea | Where you use it in the project |
|---|---|
| Capability vs adoption gap | Plan, Milestone 1: name your team's current linear habits |
| Task to outcome shift | Plan, Milestone 2: rewrite three "task" asks as "outcome" asks |
| The three layers | Plan, Milestone 3: choose which layer each workflow lives in |
| Primitives compose | Demo, Milestone 4: build one primitive end to end |
| Evals harder than the model | Plan, Milestone 5: write the eval that will catch the next upgrade |
| Shrink scaffolding / upgrade as opportunity | Plan, Milestone 6: your model-upgrade playbook |

### Milestones (build them in order, each one stands on its own)

1. **Map the gap.** Write down three things your team does today on the slow, linear path (for example "we hand-write release notes," "code review takes two days"). For each, note what a more capable model could do instead.
2. **Reframe task to outcome.** Take three "do this one thing" asks and rewrite each as an ongoing outcome the model could own (for example "summarise this PR" becomes "keep the changelog current"). This is the future-facing habit in miniature.
3. **Assign the layers.** For each workflow, decide whether it lives at the model layer (a single API call), the platform layer (a managed agent at scale), or the Claude Code layer (a developer running it directly). Justify each choice in one sentence.
4. **Ship the one-feature demo.** Build the smallest possible working version of one primitive. A routine that posts a daily summary, or an advisor-strategy call where a small model executes and Opus advises, both count. Verify it actually runs.
5. **Write the eval that survives upgrades.** Write 5 test cases for one workflow, including at least one case so hard that today's model fails it. That failing case is your "the exponential moved" detector. Note what you will ship the day it starts passing.
6. **Write the upgrade playbook.** In half a page, describe how your team will adopt the next model: who runs the evals, how scaffolding gets audited and trimmed, and how a green eval run leads to rollout. Make it a checklist, not a wish.
7. **Stretch goals.** Add a second primitive to the demo and compose the two. Add cost and latency notes to the advisor-strategy demo. Add a "scaffolding audit" section that lists prompt instructions you suspect a smarter model no longer needs.

### How you will know you are done

- ✅ Your plan names **specific workflows, owners, and metrics**, not vague intentions.
- ✅ At least three asks are reframed from **task to outcome**.
- ✅ The demo uses **exactly one** keynote primitive and actually runs end to end.
- ✅ Your eval set contains **at least one case today's model fails**, with a note on what you will ship when it passes.
- ✅ Your upgrade playbook is a **checklist** someone else on the team could follow.

> 💡 **Keep yourself honest:** if your plan would read the same for any company, it is too generic. Specifics (this workflow, this owner, this metric, this failing eval) are the whole point.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea from the keynote. They are optional and independent. The Capstone above is the main build and already touches all of these, so feel free to skip straight to it.

### Exercise 1: spot the gap (foundational)
Pick any tool or workflow you use weekly. Write two sentences: what a capable model could already do for it today, and what is stopping that from happening. The second sentence is usually the real adoption gap.

### Exercise 2: task to outcome (foundational)
Take five prompts you would normally type as one-off tasks and rewrite each as a standing outcome the model could own over time. Notice which ones get scary, and why. The scary ones are where verification and evals matter most.

### Exercise 3: place it on a layer (intermediate)
List five things you might build with Claude. For each, decide: model layer, platform layer, or Claude Code layer? Write one sentence of justification. There is no single right answer; the reasoning is the exercise.

### Exercise 4: design an advisor split (intermediate)
Pick a workload with high volume and some hard cases. Sketch which parts a small model could execute and which hard cases should escalate to a larger advisor model. Estimate, in rough terms, where you would save money and where you would not.

### Exercise 5: write an unsaturated eval (advanced)
For a use case you care about, write 5 eval cases including one deliberately at the edge of today's capability. Run it (even by hand). If everything passes easily, make it harder. The goal is an eval that still has room to improve, so it can measure the next model.

---

## Cheat sheet

```text
THE CORE PICTURE
  Capability ........ exponential (gets faster every few months)
  Adoption .......... linear (most orgs crawl in a straight line)
  Your job .......... close the gap; build for the NEXT model, not today's

THE THREE LAYERS
  Model ............. raw intelligence (Opus 4.7, Mythos preview)
  Platform .......... managed agents, advisor strategy, MCP tunnels, self-hosted sandboxes
  Claude Code ....... routines, auto mode, autofix, code review, security scan

RIDE THE EXPONENTIAL (4 habits)
  1. Build for emerging capability ... design for the next version
  2. Keep evals harder than the model. unsaturated tests catch the jump
  3. Shrink your scaffolding ......... cut workarounds smarter models don't need
  4. Treat upgrades as opportunity ... automate evals; make rollout a fast win

REMEMBER
  - The unit of work is shifting from TASK to OUTCOME.
  - Primitives compose: snap small pieces together.
  - Capable does not mean uncontrollable (tunnels + self-hosted sandboxes).
```

## How this connects to the rest of the course

- **Next, Module 1 · Lesson 2 (The Capability Curve):** goes deeper on exactly how the models improved (planning, error recovery, long-horizon attention) and turns the four habits here into concrete practices.
- **Later, Module 2 (Core skills):** the prompting, model-choice, and thinking lessons are how you actually shrink scaffolding and give the model room to work.
- **Later, Module 3 (Evals):** builds out the "evals harder than the model" habit that this keynote keeps returning to.
- **Later, Module 5 (Claude Managed Agents):** the platform announcements here (managed agents, MCP tunnels, self-hosted sandboxes, outcomes) get hands-on treatment.

---

*Source: "Code with Claude London 2026: Opening Keynote" by Boris Cherny and the Anthropic team (Lisa, Angela, Caitlyn, Cat, and others), Code with Claude 2026, London. This is a vision and announcements talk, so code blocks are few and are illustrative reconstructions of the approaches and configurations described. Adapt model names and API details to the current SDK.*

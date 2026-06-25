# Module 8 · Lesson 31: Building AI-Native at Enterprise Scale

> **Course:** Building with Claude, a self-paced course
> **Module 8:** Leading the AI-native transformation
> **Speaker:** A panel with Ruslan (engineering leader, monday.com), Alex (Doctolib), and Ulrich Schäfer (VP for Tech Foundations, Delivery Hero), moderated by Rebecca (Anthropic Go-To-Market team)
> **Source talk:** [Building AI-native at enterprise scale: monday.com, Doctolib, and Delivery Hero](https://www.youtube.com/watch?v=XFaeIbL-lvE) · [full transcript](../../transcripts/code-with-claude-2026-london-2026/17_building-ai-native-at-enterprise-scale-mondaycom-doctolib-and-delivery.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

Three large companies founded before the AI era explain how they became AI native without rebuilding from scratch: they plugged Claude into their existing tools and workflows, spread adoption through skills marketplaces and community, treat each new model as a different beast to re harness, and have learned that the real work is rethinking everything *around* the code (architecture, identity, processes) once coding stops being the bottleneck.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you bring AI to a real (or realistic) legacy system: you build one agent that plugs into an existing workflow, set up a "council of agents" review, and write the enterprise rethink memo (architecture, identity, processes). Everything before the Capstone teaches the moves you will use. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[Accelerate! (John Kotter, HBR)](https://hbr.org/2012/11/accelerate)** (essay). Kotter is the canonical authority on leading organizational change under disruption; his "build urgency, spread through community, don't wait for perfect conditions" model is exactly the panel's change story.
> - **[The Mythical Man-Month (Fred Brooks)](https://en.wikipedia.org/wiki/The_Mythical_Man-Month)** (book). Brooks's lessons on large legacy systems and conceptual integrity underpin the "API-first, opinionated, rethink everything" advice.

## A few plain-language basics first

This panel uses enterprise engineering terms. Here they are in plain words:

- **AI native:** an organisation where AI is built into how it works and what it ships, not bolted on afterward.
- **Greenfield vs legacy:** *greenfield* means starting fresh with no existing code. *Legacy* means you already have a working product, many customers, and years of older code. None of these companies got to greenfield.
- **Monolith:** one large, tightly connected code base, often old and hard to change. The opposite is *distributed systems* or *services*: many smaller, separate pieces.
- **PRD (Product Requirements Document):** a written description of what a product should do.
- **PR (Pull Request):** a proposed code change that gets reviewed before being merged (accepted).
- **Eval (evaluation):** a set of test cases to measure whether an AI behaves correctly.
- **A/B test:** showing version A to some users and B to others to learn which is better.
- **Skill:** a reusable instruction file that teaches Claude how to do a specific task.
- **MCP (Model Context Protocol):** an open standard that lets Claude connect to outside tools and data.
- **API (Application Programming Interface):** the defined way one piece of software talks to another. "API first" means designing every feature so it can be driven by code (and by agents), not only by clicking a UI.
- **Identity / authorization system:** the system that decides who is allowed to do what. With agents acting on a platform, an agent needs to be a recognised "user" with permissions.
- **Orchestrator:** a controlling component that coordinates several models or sub steps to get a job done.
- **Cowork:** an Anthropic product for getting general work done with Claude, used here beyond engineering.

You do not need to memorise these. Each one is explained again the first time it matters below.

## Why this lesson matters

The other lessons in this module feature fast moving teams (Anthropic Labs, Base44, Spotify's platform group). This panel is about the harder, more common situation: a big company founded between 2011 and 2013, with a large customer base, a real engineering organisation, and a decade old code base, trying to pivot to AI native. As the moderator put it, "none of the three of you really got to greenfield." If you work somewhere with legacy systems and you wonder how AI adoption actually plays out there, this is your lesson. The honest, sometimes contradictory answers from three leaders are more useful than any single tidy framework.

> 🔑 **The unifying message (paraphrased from Ruslan):** "Stop waiting for perfect conditions, perfect use cases, enough AI-ready work." You will never finish splitting the monolith or the big refactor first. "None of it matters that much anymore. You can pick a thing tomorrow."

## Learning objectives

By the end of this lesson you will be able to:

1. Plug an AI agent into an *existing* workflow (Jira, GitHub) instead of forcing a new interface, to drive adoption.
2. Spread adoption across an org with a skills marketplace and a strong community channel, not just top down mandates.
3. Treat each new model release as a different beast that needs re harnessing, with the right evals and A/B tests.
4. Apply architectural lessons for legacy systems: API first, opinionated standardisation, and rethinking identity for agents.
5. Use a "council of agents" review and outcome metrics (success and failure rates) to ship AI changes safely.

## Prerequisites

- A basic understanding of how software teams build and ship (PRs, reviews, CI). No coding required.
- Helpful but optional: Module 8 · Lessons 27 to 30, which set up the "bottleneck has moved" theme this panel keeps returning to.

---

## Part 1: meet the three companies (and what Claude powers)

All three companies were founded in the early 2010s, before the era of LLMs (Large Language Models, the AI that reads and writes text). Their pivot to AI native is the subject.

| Company | What it does | Claude-powered system | Code base age |
|---|---|---|---|
| **monday.com** (Ruslan) | Reinventing work management; moving from "managing work" to "executing work" with teams of agents. | **Monday Vibe**, a tool that turns a user's prompt into a detailed PRD, refines it together, and builds a working application in minutes. | ~14 years; a monolith they are slowly breaking up. |
| **Doctolib** (Alex) | Health platform: book doctors, message patients, manage health records, plus tools for healthcare professionals. | Near 100% adoption of building with Claude across engineers, PMs, designers, and (via Cowork) non technical staff. | ~half a decade old monolith, plus newer distributed services. |
| **Delivery Hero** (Ulrich) | World's leading local delivery network (food, groceries) in 60+ markets. | **HeroGen**, an autonomous software delivery agent that takes a Jira ticket or GitHub issue all the way to a mergeable, production ready PR. | Large, fragmented existing ecosystem. |

> 💡 Notice that none of these are toy projects bolted onto a side repo. They are core systems built *into* old, imperfect code bases. That is the whole point of the panel.

Delivery Hero's HeroGen numbers show the scale of what is possible in legacy: around 173 merged PRs going into production per day (10 day average), and roughly 7,000 merged PRs total since launch in February, on an exponential trajectory.

---

## Part 2: how to drive adoption (and how it spreads)

A recurring theme: you get adoption by meeting people where they already are, then letting the best engineers find the best uses and spreading those.

### Plug into existing workflows, do not invent a new one

Delivery Hero deliberately did *not* build a new chat window for HeroGen. They connected the agent to the tools people already use: Jira, GitHub issues, soon GitLab. A developer assigns a ticket to the agent the same way they would assign it to a person.

> 🔑 **Adoption rule (paraphrased from Ulrich):** "We try to stay with the current environment that people have to drive adoption, where they just assign these tickets to the agent." A new interface is a barrier; an existing one is a habit.

They also wired the agent into CI (the automated build and test system): tests run against the agent's work, failures feed back to the agent to fix, and it even fixes flaky CI itself. And they are connecting the security team's workflow so that code related vulnerabilities are auto assigned to the agent, auto fixed, and the repo owner just reviews the PR.

### Let the best engineers find the best uses, then industrialise them

Doctolib made a conscious choice: building with Claude is not only the platform team's job. As Alex put it, "your best engineers are going to be the ones who are going to find the most interesting ways of using it." So the platform team's job became *enabling*: spotting the best practices people discover, removing bottlenecks, industrialising those practices, and scaling them across teams.

Concretely, Doctolib built:

- A **skills marketplace** where everyone's skills are discoverable, showing which get the most usage and which are trending.
- A ready **environment** for developers with all the tools connected on day one, with popular skills packaged in, plus plugins for experimental skills.
- A company wide community channel called **Build with AI**, "the most popular channel in the whole company," where people share what they learn, ask questions, and promote their skills.

> ✅ **Best practice: go down the learning curve together.** Doctolib's goal was not to have everyone do amazing things in isolation, but to share lessons so the whole org learns as one. A lively community channel beats a stack of internal docs.

### monday.com: lean on an open platform you already had

monday.com's Monday Vibe (prompt to working app) got a fast start because the company had "invested early in an open platform for external developers." Despite an old code base, the open platform "contained" the legacy: the vibe coding tool uses the same APIs, SDKs, and deployment and publishing mechanisms that external developers already use. That let them build a proof of concept in days.

> 💡 The deeper lesson: an early investment can pay off years later in a way you did not foresee. The open platform built for outside developers turned out to be the perfect foundation for an AI app builder. To unlock full potential, though, they now need *every* feature to be API accessible, which is "a much longer journey."

---

## Part 3: what happens when a new model ships

The moderator asked each leader what actually happens inside their org the week a new Claude model lands. The answers are honest and varied.

> 🔑 **The step change moment:** for Delivery Hero's HeroGen, the new Opus models last November were when "our vision of this system actually working became a reality." Before that it was "a fancy idea." They took a big bet that models would improve enough to take whole features, and the bet paid off.

A few patterns emerge:

- **Treat a new model as a different beast.** Ruslan describes migrating Monday Vibe's orchestrator from one Opus version to the next as "quite a change." The new model brought amazing capabilities, "but all the system prompts we'd been optimizing just didn't transfer well. It was a completely different beast." They had to rethink and re tune their prompting, working closely with Anthropic's solution engineers. As Ruslan summarised, you cannot assume a new model is compatible with the old one: treat it "as a completely different thing and harness it in a way that works for it."
- **End to end evals matter most for multi model systems.** Monday Vibe is multimodal: an orchestrator using a top model, plus a workflow underneath with deterministic actions and simpler models. A new release usually affects only one part, so "the end-to-end evaluation is the key," even though each atomic action has its own evals.
- **Excitement is a feature of an experimentation culture.** Doctolib's people greet a new model with "what can I now do that I couldn't before?" If you already have an experimentation culture, you do not need to chase people to try it; they want to. Often a new model lets you *delete* old workarounds you built to compensate for past limitations.
- **Strict evals for customer facing AI, more "vibes" for the dev process.** Doctolib has teams with very strict evals for AI products they sell to customers, checking performance and trade offs on every release. For the *development* process itself, Alex admits it is "still a little bit more vibes than it could be," and he wants better verification to gain confidence and move faster.
- **Be cautious about model switching without the setup.** Delivery Hero has stayed on Opus 4.5 for HeroGen, "mostly because we do not yet have the A/B testing setup and the necessary volume to make good decisions" about moving. A reminder that you need the measurement infrastructure before you can responsibly switch models.

---

## Part 4: architecture and platform lessons for legacy systems

Asked what they would do differently if starting today, the leaders converged on a few hard won lessons.

### Be opinionated outside the monolith; provide context inside it

Doctolib is moving from a monolith to distributed services. Alex sees "a notable difference between how easy it is to adopt all the tooling outside the monolith versus inside." Outside, they chose to be **very opinionated**: a standard way to build every service and application, which makes the agent's job easy. Inside the monolith, the model is *too* good at pattern matching: it finds old patterns and copies them, so "you have to spend extra effort to tell it, this is the new way, do not just follow the pattern you see."

> 🔑 **The consistency lesson (echoing Spotify):** smaller code bases with more standardisation and more built in documentation make a big difference in model performance. Opinionated structure is not bureaucracy; it is what lets agents work well.

### Go API first, and rethink identity for agents

Ruslan's number one regret: not investing earlier in an **API first approach** with clean boundaries across every service. monday.com built the best UI for human customers, but UI moves fast and agents need *API* access that was "just not there by default," including internal APIs between services.

His second regret: not rethinking **identity and authorization systems** earlier so an agent can be a "first class user" that interacts with people. With monday.com's granular permission models, making agents first class citizens "has been quite a challenge."

> ✅ **Best practice for the agent era:** design so every feature is API accessible (not just clickable), and design your identity system assuming agents are here to stay and will act as users with permissions.

### Everything around the code must be rethought

Alex makes the broader point that ties this module together. When the limiting factor was "how long will it take to write the code," you did not mind if some steps needed a bit of human interaction. Now that coding can be done by agents, "you constantly find all of those new bottlenecks." Going faster means going back and rethinking the many touch points: processes, not just architecture. "What has worked for you before... is not working now. So everything has to be rethought."

### The council of agents (Delivery Hero's success driver)

Delivery Hero defines **success rate** as the ratio of agent PRs that are *merged* versus *actively rejected* by an engineer. One change drove that success rate up to 85%: a **council of agents**, a set of *different* models all reviewing the same generated code.

> 🔑 **Why multiple models (paraphrased from Ulrich):** using several different models for review avoids the risk that one model "has some sort of blank spot or bias" and misses an issue. And crucially, "it did not drive up the cost as much as we saw. It's very, very doable. I can just suggest that to anyone to try that out."

---

## Part 5: the lightning round

The panel closed with quick questions whose short answers are surprisingly rich.

**One general agent or many specialists?** All three leaned toward specialists. Ruslan: "many specialists orchestrated by one generalist... but who knows as the models get better." (An *orchestrator* is a controller that coordinates the specialists.)

**What are your best engineers spending time on now?** The script has flipped. Ulrich notes that principal engineers (the most senior) used to mostly review others' code and join architecture discussions, "usually not creating new code." Now they are "a lot more hands-on," producing lots of code with Claude, and not by sitting at one terminal synchronously but by *orchestrating multiple agents*. His example: a data scientist who did prompt optimization by hand now orchestrates multiple agents and built a skill to apply genetic algorithms (an automated search for better prompt variations) and run all the evals on them, at far bigger scale. Ruslan adds that best engineers now build the **context layer** (a unified, shared store of context, "AI brains") that did not exist 18 months ago.

**The metric you look at every morning?**

| Leader | Morning metric | Why |
|---|---|---|
| Ulrich (Delivery Hero) | Merged PRs and the success ratio | Tells you how well the agent is performing. |
| Alex (Doctolib) | Quality and reliability metrics | The "control KPIs" that confirm going faster has not broken anything. |
| Ruslan (monday.com) | Failure rates (not just success) | Going deep into failures is "a goldmine of new use cases": why a tool was not called, why the user did not get what they wanted. |

> 💡 Ruslan's twist is worth keeping: success rates tell you how you are doing, but *failure* rates tell you what to build next.

**What should an engineer six months behind do first?** All three said, in effect: just start.

> 🔑 **The closing advice (three voices):**
> - Ulrich: "Start using it." Delivery Hero even mandated that every team ship one feature end to end with AI this quarter, to push past initial resistance.
> - Alex: ask the agent to examine your code base, tell it what you like and dislike, and have it propose and then execute a plan to improve things.
> - Ruslan: "Stop waiting for perfect conditions." Do not wait to finish the monolith split or the big refactor. Pick a repetitive, toilsome piece of work tomorrow and "unleash Claude full on."

---

## Key takeaways

1. **You do not need greenfield.** All three built core AI systems inside decade old, imperfect code bases. Start where you are.
2. **Plug into existing workflows.** Assigning a Jira ticket to an agent beats inventing a new chat interface. Meet people where they already work.
3. **Spread adoption through community.** A skills marketplace plus a lively "Build with AI" channel beats top down mandates and isolated heroics.
4. **Treat every model as a different beast.** Prompts may not transfer; re harness for the new model, with end to end evals for multi model systems. Get your A/B setup before switching.
5. **Be opinionated and API first.** Standardised, documented code bases help agents. Design every feature for API and agent access, and rethink identity so agents can be first class users.
6. **Use a council of agents.** Multiple different models reviewing the same code reduces blind spots and lifts success rate, without blowing up cost.
7. **Watch failures, not just successes, and just start.** Failure rates are a goldmine of new use cases. Stop waiting for perfect conditions.

## Common pitfalls

- ❌ Waiting to finish the monolith split or a big refactor before adopting AI at all.
- ❌ Forcing users into a new AI interface instead of plugging the agent into Jira, GitHub, and CI.
- ❌ Assuming a new model is a drop in replacement; old prompts often do not transfer.
- ❌ Switching models without the A/B testing setup and volume to judge the result.
- ❌ Letting the agent copy old patterns in a monolith because you did not tell it the new way.
- ❌ Relying on a single model to review agent output, leaving blind spots uncaught.
- ❌ Tracking only success rates and missing the new use cases hiding in failures.

---

## 🛠️ Capstone Project: The Legacy AI-Native Plan

> This is the main hands on project for the lesson. You will do exactly what these three companies did: bring AI into an *existing* system you cannot rebuild, plug it into a real workflow, set up a multi model review, and write the rethink memo for everything around the code.

### What you will build

Three connected deliverables for one real or realistic legacy system: (1) a working agent that plugs into an existing workflow and produces a reviewable PR, (2) a "council of agents" review step with two or more different models, and (3) a one to two page **Enterprise Rethink Memo** covering architecture (API first), identity (agents as users), processes, and adoption.

> 🎯 **Pick a legacy system you cannot rebuild.** Use a real older repo at work, an open source monolith, or a deliberately messy practice repo. The point is to practice on something with existing patterns, not a clean slate.

### Why this is the perfect practice

| Lesson skill | Where you use it in the Capstone |
|---|---|
| Plug into existing workflows | Milestone 2, ticket to PR |
| Provide context inside a monolith | Milestone 3, the "new way" instructions |
| Council of agents review | Milestone 4, multi model review |
| Success and failure metrics | Milestone 5, the scoreboard |
| API first and identity rethink | Milestone 6, the memo |
| Adoption through community | Milestone 6, the adoption section |

### Milestones (build them in order, each one is shippable)

1. **Map the legacy reality.** One paragraph: what is the system, how old, monolith or services, and what is messy about it? Note the existing workflow people use (Jira, GitHub issues, etc.).
2. **Build a ticket to PR agent.** Wire an agent so that assigning it a ticket or issue (the existing workflow, no new chat window) produces a reviewable PR. Connect it to your tests so failures feed back to the agent to fix.
3. **Teach it the "new way."** Because the model will copy old patterns, write explicit context (a skill or instructions) telling it the current, preferred way to build in this code base. Show that the agent follows the new way, not the old pattern it found.
4. **Add a council of agents.** Add a review step where two or more *different* models review the generated PR. Have them flag issues a single model might miss. Note whether the extra cost was modest, as Delivery Hero found.
5. **Build a scoreboard.** Track success rate (PRs merged versus actively rejected) and, importantly, dig into failures. Write down at least two new use cases or improvements your failures revealed.
6. **Write the Enterprise Rethink Memo.** One to two pages: (a) which features need to become API accessible; (b) how identity and permissions should treat agents as first class users; (c) which processes around the code must change now that coding is cheap; (d) an adoption plan using a skills marketplace and a "Build with AI" community channel.

### How you will know you are done

- ✅ Your agent turns a ticket in the **existing workflow** into a reviewable PR, with test feedback wired in.
- ✅ The agent follows the **new way**, not the old pattern it found in the legacy code.
- ✅ Your **council of agents** uses two or more different models and catches something a single model missed.
- ✅ Your scoreboard shows **success and failure rates**, and you listed new use cases found in the failures.
- ✅ Your memo covers **API first, identity, processes, and adoption**, each with a concrete next step.

> 💡 **Keep yourself honest:** if your agent quietly copied a legacy pattern you wanted to retire, your "new way" context is not strong enough. And if your review uses only one model, you have a council of one, which is the blind spot the panel warned about.

---

## Practice exercises (optional extra reps)

> **What these are:** small, independent reps, each focused on one move from the panel. Optional. The Capstone above exercises all of them together.

### Exercise 1: meet people where they are (foundational)
List the tools your team already uses daily (issue tracker, chat, CI). Pick one and sketch how an agent could be invoked from inside it, with no new interface to learn.

### Exercise 2: the new model drill (foundational)
Take a prompt you tuned for one model and run it on a newer model. Note what did *not* transfer. What would you change to re harness for the new beast?

### Exercise 3: opinionated context (intermediate)
In a code base with multiple patterns, write a short skill or instruction that tells Claude the *current* preferred way to build a component. Confirm Claude follows it instead of an older pattern.

### Exercise 4: council of agents (intermediate)
Have two different models review the same PR or function. List the issues each caught that the other missed. Was the extra cost worth it?

### Exercise 5: mine the failures (advanced)
Take a set of failed agent runs or unhappy user sessions. For each, ask why the right thing did not happen. Turn the patterns into a list of new use cases to build, the way Ruslan described.

---

## Cheat sheet

```text
AI-NATIVE IN LEGACY (you don't get greenfield)
  Start where you are. Don't wait to finish the monolith split or big refactor.

DRIVE ADOPTION
  Plug into existing workflows (assign a Jira/GitHub ticket to the agent).
  Wire in CI: failures feed back to the agent to fix.
  Spread it: skills marketplace + a "Build with AI" community channel.
  Let best engineers find best uses; platform team industrializes them.

NEW MODEL = DIFFERENT BEAST
  Prompts may not transfer. Re-harness for the new model.
  Multi-model systems: end-to-end evals are key.
  Get your A/B setup BEFORE switching models.

ARCHITECTURE LESSONS
  Outside the monolith: be very opinionated and standardized.
  Inside the monolith: give explicit "this is the NEW way" context.
  Go API-first; rethink identity so agents are first-class users.
  Everything around the code (processes too) must be rethought.

SHIP SAFELY
  Council of agents: several DIFFERENT models review the same code.
  Track success rate (merged vs rejected) AND mine failures for new use cases.
```

## How this connects to the rest of the course

- **Earlier, Module 8 · Lesson 27 (Running an AI-native engineering org):** the "bottleneck has moved, rethink the processes" theme this panel echoes from inside large companies.
- **Earlier, Module 8 · Lesson 30 (Spotify):** the same code base consistency and verification lessons at 3,000 engineer scale.
- **Earlier, Module 8 · Lesson 29 (Base44):** "encode taste, A/B test, build skills" patterns, here at much larger companies with skills marketplaces.
- **Earlier, Module 3 (Evals):** the strict, end to end evaluation discipline behind safely re harnessing for each new model.

---

*Source: "Building AI-native at enterprise scale: monday.com, Doctolib, and Delivery Hero," a panel with Ruslan (monday.com), Alex (Doctolib), and Ulrich Schäfer (Delivery Hero), moderated by Rebecca (Anthropic), Code with Claude 2026, London. The tables and cheat-sheet boxes are faithful paraphrases of what the panelists described; they are illustrative reconstructions, not verbatim slides. Speaker first names are taken from the transcript as spoken.*

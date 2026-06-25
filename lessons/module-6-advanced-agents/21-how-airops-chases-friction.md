# Module 6 · Lesson 21: How AirOps Chases Friction to Build AI Products

> **Course:** Building with Claude, a self-paced course
> **Module 6:** Advanced agent engineering
> **Speaker:** Dylan, Product team, AirOps (London)
> **Source talk:** [How AirOps chases friction to build AI products with Claude](https://www.youtube.com/watch?v=M5uwBawBDpw) · [full transcript](../../transcripts/code-with-claude-2026-london-2026-day-2/10_how-airops-chases-friction-to-build-ai-products-with-claude.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

Making powerful agents usable by non-technical people (like marketers) means hunting down friction one point at a time: meet users where they already work, keep them in control with human review, and engineer a tight harness of specialized tools and focused sub-agents so the output is consistently good.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you build **BriefBot**, an accessible agent for a non-technical user, complete with a document-style interface, a human review gate, specialized tools, and focused sub-agents. Everything before the Capstone teaches the moves you will use there.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[PDCA: Plan-Do-Check-Act (Lean Enterprise Institute)](https://www.lean.org/lexicon-terms/pdca/)** (docs). The original scientific-method improvement cycle (Shewhart/Deming) that is the timeless backbone of "chase friction, measure, repeat."
> - **[Building Effective Agents (Anthropic)](https://www.anthropic.com/engineering/building-effective-agents)** (essay). Grounds the harness-engineering and orchestrator/sub-agent patterns AirOps relies on in first-principles terms.

## A few plain-language basics first

This lesson uses some everyday AI and product terms. Here they are in simple words:

- **Agent:** an AI that takes a series of actions on its own toward a goal, rather than answering in one shot.
- **Harness:** all the code and settings around the model: the tools you give it, the context you feed it, the loop that runs it. The model is the engine; the harness is the rest of the car.
- **Tool:** a small piece of code an agent can call to do something exact, such as fetch a web page or look up data. A **primitive tool** is a very basic one (like "do one search"); a **specialized tool** bundles many steps into a single, predictable call.
- **Context:** the text the model can "see" while it works. **Context window** is the maximum amount it can hold at once, measured in tokens.
- **Token:** the unit the model reads and writes in, roughly three quarters of a word. More tokens means more cost and more time.
- **Sub-agent:** a separate agent the main agent calls for a focused job, with its own clean context window, so the main agent's context stays uncluttered.
- **Artifact:** a saved output (a document, a table) that the agent or the user can reference later.
- **MCP (Model Context Protocol):** a standard way to connect an agent to outside tools and data sources.
- **Deterministic:** always gives the same result for the same input, with no guesswork. The opposite of the model's normal free-form behavior.
- **Friction:** anything that makes a product harder to use or trust. Dylan's whole talk is about chasing it.

You do not need to memorise these. Each is explained again the first time it appears.

## Why this lesson matters

Dylan's core message is simple and a little humbling: "building agents and just making agents accessible is honestly really hard." It is one thing to hand a developer a powerful agent. It is another to put that power in front of a marketer who does not know what JSON is and have it feel natural, trustworthy, and reliable.

The big idea is **chasing friction**. Every time you solve one friction point, a new one appears. As Dylan says, "every single time a problem is solved, that friction point always keeps moving." That is not failure; that is the job. Chasing friction is how you turn a flashy demo into a production product that real, non-technical people use every day.

## Learning objectives

By the end of this lesson you will be able to:

1. Recognize the **complexity ceiling** of rigid, node-based workflows and why teams move toward flexible agent harnesses.
2. Use the principle "**endless use cases force intentionality**" to focus an agent on a real user's real workflow.
3. Build for the three things non-technical users want: a **familiar interface**, **transparency**, and **control**, plus enforced **human review**.
4. Improve output quality with **specialized tools** (instead of many primitive tool calls) and **focused sub-agents** (to protect the main context window).
5. Measure whether harness changes actually help, instead of going on "vibes."

## Prerequisites

- Module 6 · Lesson 20 or any earlier lesson where you built a basic agent.
- Helpful but optional: a basic understanding of the Claude Agent SDK (the official toolkit for building agents).

---

## Part 1: how AirOps got here, the complexity ceiling

AirOps is a growth marketing platform for **AI search**. AI search is like SEO (the practice of getting your pages to rank in search results), but for AI engines like ChatGPT, Gemini, and Claude. Buyers now ask AI assistants things like "which sunglasses should I buy?", so brands want to know whether they show up in those answers.

AirOps started with a **node-based workflow builder**: a drag-and-drop canvas where you wire up boxes ("nodes") and pass data between them. It is powerful, but it hit a **complexity ceiling** (a point where things get too hard to manage) for non-technical users:

- Marketers had to learn developer concepts like JSON and templating just to build a workflow.
- Workflows had a **short shelf life**: every time a new model shipped (Opus 4.6, 4.7, and so on), steps had to be updated.
- Hidden coupling: change step 1 and you might silently break a variable referenced in step 20.
- Scaling to enterprise use cases required a technical person to babysit the build.

> 🔑 **The goal: lower the barrier without lowering the quality bar.** AirOps wanted content marketers to ship their own ideas, while still keeping enterprise quality and governance. Brands do not want to "pump AI slop out."

The turning point was the model getting smart enough. With the release of Opus 4.5, Dylan says, "a lot of people started to see really how smart the models were in tool calling, being able to follow instructions" without breaking the rules set for them. That capability is what made a flexible agent (instead of a rigid workflow) viable.

> 💡 **Why the Agent SDK over a traditional framework.** Traditional agent-orchestration frameworks are brittle: changing how sub-agents are wired usually means code changes. With the Claude Agent SDK you can "orchestrate agents just through markdown files" and provide skills and context by shaping the environment, not by reprogramming. Flexibility is the whole point.

What AirOps launched (AirOps Next): **Quill** (an agent "captain" for marketers with access to brand and AI-search data), and **playbooks** (a natural-language builder that is essentially a **skill**, with collaboration, governance, and versioning). One customer, Parallel, went live in one week instead of the usual month, with a 130% increase in citation rate and a 42% increase in share of voice.

---

## Part 2: friction point one, endless use cases force intentionality

Here is a trap most people hit with a powerful agent. Dylan describes it: "it's really easy to start sprawling into this spiral" of use cases, because the thing can do so much. The fix is discipline.

> 🔑 **Endless use cases force intentionality.** When an agent can do anything, you must be ruthlessly clear about *who* you are building for and *what* real problem you are solving. Dylan pictures a little voice chanting "marketers, marketers, marketers" to stay focused on the actual customer.

So AirOps mapped the real content-marketing workflow: discover a topic, research it, draft a brief, draft the article, then add internal linking and SEO best practices. Crucially, **human review points** appear all through that flow. Marketers care deeply about what they publish, so they want to check the work as it goes.

That workflow pointed to four things to get right.

### What non-technical users actually want

| Need | What it means | How AirOps delivered it |
|---|---|---|
| **Familiar interface** | Meet users where they already work. | A document-style "playbook" view, like a Google Doc, instead of a node graph. Marketers have used docs for years. |
| **Transparency** | See what is happening at each step. | Even inside a document, show exactly which tool is being used and what context is being fed at each moment. |
| **Control** | Stay in charge of the instructions. | Keep the user able to direct and adjust the playbook, even though a document is less deterministic than a rigid graph. |
| **Enforced human review** | A real gate, not optional. | Assign reviewers per section; the agent blocks until the assigned person approves. |

> 💡 **Transparency was a feature people loved about the old builder.** Users liked seeing which tools ran at each step. The challenge was keeping that visibility inside the friendlier document interface, not throwing it away.

### Human review as a real gate

This is where AirOps differs from typical coding agents. In coding, review usually happens *after* the agent finishes (a PR review at the end). AirOps bakes review *into* the run:

- In a playbook, you assign reviewers at the end of each section.
- When the agent reaches that section, a tool fires that **blocks** progress.
- Only the assigned reviewer can unblock it. Others can comment, but the gatekeeper must approve.
- Reviews surface in two places: an **inbox** (each review item opens the agent's run, with thought traces on one side and outputs on the other) and a **grid** (running many playbooks at scale, one job per row, with review possible in each cell).

> ✅ **Best practice: bring governance, configurability, and accountability into the agentic workflow itself.** Do not bolt review on at the very end. For high-stakes, brand-sensitive work, a human-in-the-loop gate that the agent must wait on is what makes the output trustworthy.

---

## Part 3: friction point two, consistency through harness engineering

The second big worry when moving from rigid workflows to agents is **consistency**: will the output be reliably good? AirOps's best explanation of the answer came, funnily enough, from their VP of Sales, in a car metaphor.

> 🔑 **The car metaphor for harness engineering.** The **model** (Claude Opus or Sonnet) is the engine. Everything you build around it (tools, context, sub-agents, the loop) is the rest of the car. A great engine alone does not make a great car. Dylan calls this "the best explanation of harness engineering" he has seen.

AirOps focused hardest on two parts of the harness: **tools** and how they **orchestrate context**.

### Specialized tools beat many primitive tools

You can give an agent lots of small **primitive tools** (one search, one scrape, one lookup) and let it figure out a job by stringing them together. The problem: the agent goes on "safari trips," making many calls, which is slow and token-inefficient ("token" = the billing/processing unit, roughly three quarters of a word).

The fix is to build **specialized tools** for jobs the agent does over and over, making them more deterministic ("deterministic" = same input, same predictable result).

| Approach | What happens | Cost |
|---|---|---|
| Many primitive tools + a skill | Agent makes ~20 calls to gather context, wandering. | Slow, token-heavy |
| One specialized tool (e.g. "analyze this URL") | Agent passes a URL, gets back everything about the page plus structured content gaps, target keywords, and target prompts. | Faster, fewer tokens |

AirOps built two such tools: a page-analysis tool (give it a URL, get back a full diagnosis) and a "page versus" tool (benchmark your page against top-ranking pages and find the gaps). Dylan likens this to "**code mode**": instead of looping through many tool calls, produce code that fetches exactly what you need in one pass.

> 💡 **Result.** The specialized page tool cut token consumption by about 8% for that task and was noticeably faster, replacing roughly 20 separate calls with a single entry point.

### Focused sub-agents protect the main context window

A **sub-agent** is a separate agent the main agent calls for a focused job, with its own clean context. AirOps's advice: start simple, then add sub-agents only where quality suffers.

> 🔑 **Start with plain Claude, add sub-agents where you hit "air spots."** Begin with just Claude doing its own tool calls, without over-stuffing context. Add a sub-agent when output quality dips, so each one has a clean, focused context window.

The sub-agents AirOps added:

- **Compliance check:** keeps the main context clean by spinning off a sub-agent that knows everything about the brand and scores whether the produced content follows the rules, returning what was wrong so the main agent can fix it.
- **Writing:** a sub-agent with its own focused context to write the content, undistracted by research or old compliance checks.
- **Brand kit:** runs at the **start** of every run, fetches all relevant brand context once, and stores it as an artifact. The main loop and other sub-agents then reference that one artifact instead of re-fetching (which could otherwise produce inconsistent brand context across sub-agents).
- **Custom sub-agents:** an internal lever so solutions architects can spin up extra sub-agents for specific customers.

> ✅ **Bigger context windows do not mean you should fill them.** Even with a million-token window on Opus 4.7, Dylan stresses being "really cognizant" about what you let the model attend to. Context is still a real constraint. Fetch context once, store it as an artifact, and point everyone at the same copy.

> 💡 **Results across the harness.** Specialized tools cut tokens and time. With the improved harness, 10 enterprise customers in beta were publishing content (self-serve, at quality) in under two weeks, a process that used to require a lot of hand-holding.

---

## Part 4: friction never stops moving

Dylan closes by naming the next friction points AirOps is chasing, which double as a roadmap for anyone building agents:

- **Self-improvement and feedback loops:** how to structure summaries of past runs ("traces"), collect the most relevant memories, and even **forget** the irrelevant ones ("forgetting is actually a feature").
- **Benchmarking content agents:** content is not like coding or law, where correctness is easy to check. There is taste and opinion involved. So how do you benchmark output so that, every time you change the harness (add a tool, a sub-agent, a skill), you *know* it improved and are not just "going after vibes"?

> 🎯 **The mindset.** Solving a problem does not end the work; it moves the friction. Chasing that moving friction "really is how you create production agents and make those more accessible to users outside of more technical spaces."

---

## Key takeaways

1. **Accessibility is the hard part.** Powerful is easy; usable by a non-technical person is hard.
2. **Rigid workflows hit a complexity ceiling.** Node graphs are brittle and have a short shelf life. Smarter models make flexible agent harnesses viable.
3. **Endless use cases force intentionality.** Pick one real user and one real workflow, and build for that.
4. **Non-technical users want a familiar interface, transparency, and control,** plus real human review baked into the run, not bolted on at the end.
5. **Specialized tools beat many primitive tools.** Bundle repeated jobs into one deterministic call to save tokens and time.
6. **Use focused sub-agents to protect the main context window.** Fetch context once, store it as an artifact, and point everyone at the same copy.
7. **Measure, do not vibe.** Benchmark so you know harness changes actually help.

## Common pitfalls

- ❌ Building for "everyone" and letting use cases sprawl, instead of focusing on one user's workflow.
- ❌ Forcing non-technical users to learn developer concepts (JSON, templating) to get value.
- ❌ Treating human review as an optional, end-of-run step for brand-sensitive work.
- ❌ Giving the agent only primitive tools and letting it wander through 20 calls.
- ❌ Filling a huge context window just because you can.
- ❌ Re-fetching the same brand context in every sub-agent, producing inconsistencies.
- ❌ Changing the harness and judging the result on vibes instead of a benchmark.

---

## 🛠️ Capstone Project: build BriefBot

> This is the main hands on project for the lesson. You will build an accessible agent for a non-technical user, applying every friction-busting move from the talk. Start small (one script, one tool) and grow it.

### What you will build

**BriefBot** is an agent that helps a non-technical user (say, a marketer) produce a high-quality content brief or short article. It has a document-style interface, shows what it is doing at each step, enforces a human review gate, uses one specialized tool instead of many primitive calls, and uses focused sub-agents to keep its context clean.

> 🎯 **Pick your user and workflow.** Reuse a content marketer (brief -> draft -> internal links) to match the talk, or swap in another non-technical persona: a **small-business owner** writing product descriptions, a **teacher** building lesson plans, or a **recruiter** drafting job posts. Choose one user and one workflow, and be ruthless about scope.

### Why this is the perfect practice

| Lesson skill | Where you use it in BriefBot |
|---|---|
| Endless use cases force intentionality | Milestone 1, you write down one user and one workflow |
| Familiar interface | Milestone 2, document-style view, not a node graph |
| Transparency | Milestone 3, show the tool and context at each step |
| Enforced human review | Milestone 4, a real blocking gate |
| Specialized tools beat primitives | Milestone 5, one "analyze" tool replaces many calls |
| Focused sub-agents | Milestone 6, brand-kit, writing, and compliance sub-agents |
| Measure, do not vibe | Milestone 7, a small benchmark |

### Milestones (build them in order, each one works on its own)

1. **Scope it.** Write one sentence naming your single user and their single workflow. List the 4 to 6 steps. Resist adding more.
2. **Document interface.** Build a simple document-style view (even a text file or a basic web page) where the workflow reads top to bottom. No node graph.
3. **Transparency layer.** As the agent works, log which tool it is calling and what context it is using at each step, visibly, next to the document.
4. **Human review gate.** Add a blocking review point at one step. The agent must stop and wait until a human approves before continuing. Show pending reviews in a simple inbox.
5. **Specialized tool.** Replace a cluster of primitive calls (several searches/scrapes) with one specialized tool that takes a single input (like a URL or topic) and returns a structured result. Count the tool calls before and after.
6. **Focused sub-agents.** Add at least two: a **context** sub-agent that fetches the brand/source info once at the start and saves it as an artifact, and a **writing** sub-agent with its own clean context. Make the main loop reference the artifact instead of re-fetching.
7. **Benchmark.** Create a small set of test inputs and a simple rubric (or a deterministic check) for output quality. Record quality, tokens, and time. Change one harness element and prove from the numbers whether it helped.
8. **Stretch goals.** Add a compliance sub-agent that scores output against brand rules and returns fixes. Add a scheduled trigger so BriefBot can run "always on." Add a grid view to run the playbook across many inputs at once.

### How you will know you are done

- ✅ A non-technical person could use BriefBot through the document interface without learning any developer concepts.
- ✅ At each step the user can see which tool ran and what context was used.
- ✅ The agent genuinely blocks at the review gate and only continues after human approval.
- ✅ One specialized tool replaced several primitive calls (you can show the call-count drop).
- ✅ Context is fetched once and shared via an artifact, not re-fetched per sub-agent.
- ✅ You can point to one harness change and show, from your benchmark, that it improved quality, tokens, or time.

> 💡 **Keep yourself honest:** every time you finish a friction point, write down the new one it exposed. That list is your real roadmap.

---

## Practice exercises (optional extra reps)

> **What these are:** five small, self contained tasks, each focused on one skill. They are optional and independent. The **Capstone above is the main build** and already covers all of these.

### Exercise 1: scope down (foundational)
Take an agent idea that "could do anything" and force it down to one user and one workflow. Write the user, the workflow, and three use cases you are deliberately *not* building yet.

### Exercise 2: interface swap (foundational)
Sketch the same workflow two ways: as a node graph and as a top-to-bottom document. List two reasons a non-technical user would prefer the document.

### Exercise 3: specialized tool (intermediate)
Find a job your agent does by chaining 3+ primitive tool calls. Write one specialized tool that does it in a single call. Measure the call-count and token difference.

### Exercise 4: sub-agent for context (intermediate)
Add a sub-agent that fetches one body of context (brand info, a knowledge base) once and stores it as an artifact. Make the main agent reference the artifact. Confirm the context is identical everywhere it is used.

### Exercise 5: a blocking review gate (advanced)
Implement a human review point that truly pauses the agent until a person approves. Add a tiny inbox that lists pending items. Confirm the agent cannot proceed without approval.

---

## Cheat sheet

```text
CHASE FRICTION (the core loop)
  Solve one friction point -> a new one appears -> chase that one too.

MAKE AGENTS ACCESSIBLE TO NON-TECHNICAL USERS
  - Endless use cases force intentionality: ONE user, ONE workflow.
  - Familiar interface (documents, not node graphs).
  - Transparency: show the tool + context at each step.
  - Control: keep the user able to direct the playbook.
  - Human review: a real BLOCKING gate, baked into the run.

HARNESS ENGINEERING (the car metaphor)
  Model = engine. Tools + context + sub-agents + loop = the rest of the car.
  - Specialized tools beat many primitive tools (fewer calls, fewer tokens).
  - Sub-agents protect the main context window (start simple, add at "air spots").
  - Fetch context ONCE, store as an artifact, point everyone at it.
  - Big context window != fill the context window.

PROVE IT
  Benchmark before/after every harness change. Numbers, not vibes.
```

## How this connects to the rest of the course

- **Earlier, Module 2 · Lesson 3 (The Prompting Playbook):** the harness-versus-prompt idea and splitting work into focused steps.
- **Earlier, Module 6 · Lesson 20 (Trustworthy workflows with a DSL):** another team moving away from rigid workflows toward a more legible, flexible mechanism.
- **Next, Module 6 · Lesson 22 (Metaview self-improving prompts):** the feedback-loop and self-improvement ideas Dylan names as the next friction to chase.
- **Later, Module 6 · Lesson 23 (Teaching agents to learn):** memory, forgetting, and team feedback loops in depth.

---

*Source: "How AirOps chases friction to build AI products with Claude" by Dylan (AirOps), Code with Claude 2026, London. The talk was a product walkthrough and demo, so the Capstone and any code are illustrative reconstructions of the approaches described. Adapt model names and SDK details to the current versions.*

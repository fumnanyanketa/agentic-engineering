# Module 6 · Lesson 22: How Metaview Built Self-Improving Prompts

> **Course:** Building with Claude, a self-paced course
> **Module 6:** Advanced agent engineering
> **Speaker:** Nick Mayhew, Product Engineer, Metaview (London)
> **Source talk:** [How Metaview built self-improving prompts for application review](https://www.youtube.com/watch?v=A3rmSUp6Dxg) · [full transcript](../../transcripts/code-with-claude-2026-london-2026-day-2/11_how-metaview-built-self-improving-prompts-for-application-review.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

When a system makes decisions based on human judgment, the human's preferences will keep changing, so you should build the prompt to improve itself: write the criteria in plain prose (not rules), let an agent watch the human's decisions and update the criteria, and keep the human at the center as the master while the system stays an apprentice.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you build **ScoutICP**, a self-improving evaluation assistant that learns a person's taste from their decisions and keeps its own criteria document up to date. Everything before the Capstone teaches the ideas you will use there.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[DSPy: Compiling Declarative LM Calls into Self-Improving Pipelines](https://arxiv.org/abs/2310.03714)** (paper). The seminal framework for systematically optimizing prompts and pipelines from data instead of hand-crafting them, the rigorous foundation of the "self-improving prompt" idea.

## A few plain-language basics first

This lesson uses some everyday AI terms. Here they are in simple words:

- **LLM (Large Language Model):** the kind of AI that reads and writes text. "Claude" is an LLM.
- **Model:** one specific version, for example "Haiku" or "Sonnet 4.6." Different models trade off speed, cost, and intelligence.
- **Prompt:** the text instructions you give the model. Here, the criteria the system uses to evaluate candidates *is* a prompt.
- **Agent:** an AI that takes actions on its own toward a goal (here, watching decisions and updating a document) rather than answering once.
- **Workflow:** a fixed, repeatable sequence of steps. Cheaper and more predictable than a full agent, but less flexible.
- **Tool:** a small piece of code the model can call to do something exact, such as searching through files.
- **Token:** the unit the model reads and writes in, roughly three quarters of a word. More tokens means more cost.
- **Self-improving prompt:** a prompt that gets updated over time, automatically, based on real decisions, so it tracks what the user actually wants.
- **ICP (Ideal Candidate Profile):** Metaview's term for the written description of who you want to hire. (It is borrowed from "Ideal Customer Profile" in sales.) In this system, the ICP is the self-improving prompt.
- **Human in the loop / human in the center:** "in the loop" means a person checks the work; "in the center" (Nick's stronger version) means the person makes every real decision and the system only assists.
- **Sycophantic (a "sycophant-affected model"):** a model that flatters and agrees too easily, taking claims at face value instead of reasoning critically.

You do not need to memorise these. Each is explained again the first time it appears.

## Why this lesson matters

Metaview builds AI-native recruiting software, and **application review** is the task of reading candidate CVs and cover letters to decide who to interview. Since 2023, LLMs have made it trivial for candidates to apply and to write long answers, so application volumes have exploded. Nick cites a client who got 2,740 applications for one job in 24 hours, and notes the average length of an answer like "why do you want to work here?" has grown about 50% in two years (because LLMs write them).

Recruiters are drowning, so they want a system to help with the grunt work. But here is the catch that this lesson is really about: the criteria keep changing. You build a system for "five years backend experience," then the founder sees the first CVs and says "actually, I want startup experience," then at the first interview they add "must have built zero to one." None of those were requirements two days ago.

> 🔑 **The central truth.** Anywhere human judgment is at the forefront, preferences will evolve. So your prompts must evolve with them. Nick's strongest advice: do not bolt this on at the end. Make "preferences will evolve" a **foundation** of your system from day one.

This pattern applies far beyond recruiting: code review, content review, financial-crime checks, KYC ("Know Your Customer" identity checks), anywhere a human's taste drives the decision.

## Learning objectives

By the end of this lesson you will be able to:

1. Recognize when a task has **evolving human preferences** and design for it from the start.
2. Build a **self-improving prompt** where an agent watches human decisions and updates the criteria document.
3. Write evaluation criteria as **prose, not rules** (no weightings, if-statements, or flowcharts).
4. Combine a cheap **workflow** with an agent on top to keep token costs manageable at volume.
5. Apply the **human-in-the-center** principle: the system is an apprentice that never overrules the user.
6. Build guardrails **into the architecture**, not as an afterthought.

## Prerequisites

- Module 6 · Lesson 21 or any earlier lesson where you built a basic agent.
- Helpful but optional: Module 3 (Evals), since this lesson is about evaluation systems.

---

## Part 1: preferences always evolve, so design for it

The opening story is the whole lesson in miniature. You interview the hiring manager, build a system for their stated requirements, and then watch the requirements change again and again as they actually see candidates. Every change forces you to rewrite the evaluation system.

> 🔑 **Any feedback is relative to what the user just saw.** When a recruiter says "this person doesn't have enough Python," that judgment only makes sense against the specific candidate in front of them. Your system has to understand feedback in context, not as an absolute rule.

The wrong response is to treat changing requirements as an annoyance to suppress. The right response is to expect it and make adaptation the core feature.

> ✅ **Best practice: make evolution a foundation, not an add-on.** "Build it as part of the foundation of how you work," Nick says. A system that assumes requirements are fixed will fight its own users.

---

## Part 2: the architecture, a workflow with a learning agent on top

Here is how Metaview's system flows when a candidate applies:

```text
1. REDACT the candidate         (remove name, email, phone, any personally
                                 identifiable info, so you evaluate on
                                 experience / skills / qualifications)
2. MATCH against the ICP        (the Ideal Candidate Profile, a prose document
                                 describing who you want to hire)
3. PRODUCE an evaluation        (the system's assessment of the candidate)
4. The USER decides             (progress or reject; the user, not the system)
5. A LEARNING AGENT observes    (watches the user's decisions and feedback,
                                 then updates the ICP for next time)
```

Steps 1 to 3 are a **workflow** (a fixed, cheap, repeatable sequence). Step 5 is an **agent** sitting on top. Why split it this way instead of "just make everything one agent," which Nick admits is more fun to build?

> 🔑 **Volume forces a workflow underneath.** Metaview processes thousands of applications a day; large companies receive hundreds of thousands or millions a year. You cannot afford to run a full agent (and its token cost) on every single application. So the per-candidate evaluation is a lean workflow, and the expensive, flexible learning agent runs only when it observes decisions.

> 💡 **Cost is a real design constraint, not just an engineering detail.** "You cannot spend dollars and dollars or tens of dollars on 3,000 applications for one role." Reach for an agent where flexibility pays off, and a cheap workflow where you need scale.

The **ICP (Ideal Candidate Profile)** is the part that learns. It is, in Nick's words, "the part of the prompt that is self-learning and self-improving over time." It is exactly like an Ideal Customer Profile in sales: a description of what you are looking for.

---

## Part 3: inside the learning agent

The ICP agent (the part that updates the criteria) has three main inputs and one job.

| Part | What it is | Why it matters |
|---|---|---|
| **User messages** | Every decision and signal: progress, reject, written feedback, manual edits to the ICP. | This is the raw material of the person's taste. |
| **The `query_files` tool** | A specialized tool that searches the redacted candidate profiles and makes sense of *relative* feedback. | Plain `bash` and `grep` could not handle unstructured CV data. |
| **The ICP manager agent** | An agent with one function: keep the ICP document up to date. | This is the core of the whole system. |

> 🔑 **Why a specialized tool, not grep.** Metaview first tried standard search (`bash`, `grep`), but "unstructured data can be incredibly hard to just grep for." When a recruiter says "not enough Python" or "too junior," the agent needs to look at the actual redacted resumes to learn what *that recruiter* means by those phrases. The `query_files` tool builds that context.

So the loop is: the user makes decisions, the learning agent reads them, uses `query_files` to understand them in context, and the ICP manager updates the criteria document accordingly.

> 💡 **Update on patterns, not single events.** In practice you do not rewrite the ICP after one piece of feedback. As Nick notes, "you usually start spotting patterns every 100, 200" decisions. Learning from patterns, not noise, is what makes this work at scale.

---

## Part 4: write criteria as prose, not rules

This is the design choice that makes the whole thing flexible. The ICP is a plain Markdown document. Metaview deliberately avoids weightings, if-statements, and flowcharts.

> 🔑 **Lean into what LLMs are good at: natural language.** "Allow them to reason in prose, not in flowcharts," Nick says. Keyword matching on resumes is a long-criticized, bad way to judge a person, and rule-based scoring ("30% weighting on X keyword") does not reflect how anyone actually thinks.

A real ICP looks like a short prose document with sections such as:

```text
# Ideal Candidate Profile: Product Engineer (backend bias)

## Role summary
We want a backend-leaning product engineer who can own features end to end
and is comfortable working closely with product and design.

## Must have
- Strong backend engineering experience, shipping real production systems.
- Comfort working in a fast-moving, startup-style environment.

## Nice to have
- Experience taking a product from zero to one.
- Background at companies with a strong engineering culture.

## Red flags
- CVs that claim outsized achievements with no supporting detail.
- Only large, slow-moving enterprises with no ownership shown.
```

> ✅ **Mirror how the user already thinks.** Metaview uses "must have / nice to have / red flags" because "a lot of recruiters think like this. We're just trying to reflect what users do. There's no special sauce here." Let users write in their own natural language and the system will reflect their real priorities far better than a weightings table would.

When the user gives feedback (for example, "Airbnb has great engineering culture, we'll happily hire talent from strong engineering companies, so these shouldn't be just an okay fit"), the learning agent produces a **diff** (a before-and-after of the document showing additions in green and removals in red). The user can preview, edit, or confirm it, then re-evaluate candidates against the updated ICP.

---

## Part 5: choosing models, and why critical reasoning matters

Metaview uses Anthropic models for a specific reason that has little to do with coding benchmarks.

> 🔑 **The CV problem: telling real from fluff.** Many CVs overstate what the person did. A **sycophantic** model (one that flatters and agrees too easily) will "take them at their word" and praise a candidate who claims they "created a large language model by themselves in their garage." You need a model that reasons critically. Nick says that is why Metaview uses Haiku and Sonnet.

The two-model split mirrors the architecture:

| Model | Used for | Why |
|---|---|---|
| **Haiku** | The high-volume per-candidate evaluations (the workflow). | Fast and cheap; this is a constrained task (ICP + resume -> evaluation) run thousands of times a day. Anthropic also offers Metaview special input-per-token limits to handle the volume. |
| **Sonnet** | The learning agent that finds patterns and updates the ICP. | An unconstrained task where latency matters less and more intelligence helps find the patterns. |

> 💡 **Match the model to the task shape.** Constrained, repeated, latency-sensitive task -> a fast cheap model. Open-ended, pattern-finding, occasional task -> a more capable model. The architecture and the model choices reinforce each other.

In the live demo, Nick progresses a candidate (Nina) with feedback, Sonnet is called, reasons about the new feedback, and decides to call the "update ICP" tool, producing a suggested change (for example, wanting "strong product engineering backgrounds") shown as a green/red diff for the user to confirm.

---

## Part 6: the three big takeaways

Nick ends with three principles, which are the heart of the lesson.

> 🔑 **1. Preferences evolve, so build for it from the foundation.** Any evaluation system centered on human judgment will see its requirements change. Do not write requirements once and assume they are fixed. Make adaptation a core part of the system, not an ad hoc afterthought.

> 🔑 **2. Use prose, not rules.** Lean into Markdown and natural language. Let the agent reason in prose. Avoid flowcharts and if-statements, however tempting they feel from the pre-LLM era.

> 🔑 **3. Build guardrails into the architecture.** Evaluation systems are spreading into code review, financial crime, KYC, and more. If you try to add guardrails at the end, "it's not going to work." Build the system from the start so it is an apprentice that learns from the user but never overrules them.

> 🎯 **The master-apprentice frame.** Make the user the master and the system the apprentice. The system does the grunt work and spots things (right companies, right experience, right technologies), but the human always makes the actual decision. This is "human in the center," not just "human in the loop."

---

## Key takeaways

1. **Preferences always evolve** when human judgment drives the decision. Design for it from day one.
2. **Build a self-improving prompt:** an agent watches the user's decisions and keeps the criteria document up to date.
3. **Feedback is relative to what the user just saw,** so give the learning agent a tool to read the actual examples and understand context.
4. **Write criteria as prose, not rules.** No weightings, if-statements, or flowcharts. Mirror how users already think (must have / nice to have / red flags).
5. **Combine a cheap workflow with an agent on top.** Volume and cost force the per-item evaluation to be lean.
6. **Pick models by task shape:** fast/cheap (Haiku) for constrained high-volume work, more capable (Sonnet) for open-ended pattern finding. Favor models that reason critically over sycophantic ones.
7. **Keep the human at the center.** The system is an apprentice that never overrules the master.

## Common pitfalls

- ❌ Writing requirements once and assuming they will not change.
- ❌ Bolting "learning" or guardrails on at the end instead of designing them in.
- ❌ Encoding criteria as keyword weightings, if-statements, or flowcharts.
- ❌ Treating feedback as an absolute rule instead of something relative to the examples seen.
- ❌ Running a full, expensive agent on every single item when volume demands a cheap workflow.
- ❌ Using a sycophantic model that believes inflated claims.
- ❌ Letting the system make the final decision instead of the human.

---

## 🛠️ Capstone Project: build ScoutICP

> This is the main hands on project for the lesson. You will build a self-improving evaluation assistant that learns a person's taste from their decisions. Start small (one criteria file, a handful of examples) and grow it.

### What you will build

**ScoutICP** is a system that evaluates items against a plain-prose criteria document, lets a human make the real decision with feedback, and then has a learning agent update the criteria document based on the human's decisions, shown as a diff the human confirms.

> 🎯 **Pick your domain.** Reuse hiring (evaluate candidate profiles against an Ideal Candidate Profile) to match the talk, or swap in something you know: reviewing **conference talk submissions**, screening **grant applications**, triaging **support tickets** by priority, or picking **books to read** from a list. You just need: items to evaluate, a prose criteria document, a human who decides and gives feedback, and preferences that genuinely shift over time.

### Why this is the perfect practice

| Lesson skill | Where you use it in ScoutICP |
|---|---|
| Prose criteria, not rules | Milestone 1, the criteria document |
| Workflow + agent split | Milestone 2 (workflow) and Milestone 4 (agent) |
| Redaction for fair evaluation | Milestone 2, strip identifying info |
| A tool to understand relative feedback | Milestone 5, the query-files tool |
| Self-improving prompt via diffs | Milestone 6, propose-and-confirm |
| Human in the center | Milestone 3, the human always decides |
| Model choice by task shape | Milestone 7, cheap workflow vs capable agent |

### Milestones (build them in order, each one works on its own)

1. **Write the criteria as prose.** Create a Markdown criteria file with sections like role/role summary, must have, nice to have, and red flags. No weightings or if-statements.
2. **Build the evaluation workflow.** For each item: redact identifying info, match it against the criteria document, and produce a short prose evaluation plus a simple fit rating. Keep this lean and cheap.
3. **Put the human in the center.** Show the evaluations to a human who makes the real decision (progress/reject, or your equivalent) and writes a sentence of feedback. The system never decides.
4. **Add the learning agent.** Build an agent that reads the human's decisions and feedback. For now, have it propose an updated criteria document.
5. **Add a query-files tool.** Give the learning agent a tool that searches the actual (redacted) items so it can interpret relative feedback ("too junior," "not enough X") against real examples, not in the abstract.
6. **Propose and confirm via diffs.** Have the agent output the updated criteria as a clear before/after diff. The human previews, edits, and confirms before it takes effect. Then re-evaluate items against the new criteria.
7. **Choose models by task shape.** Use a fast, cheap model for the high-volume evaluation workflow and a more capable model for the occasional learning agent. Note the cost and latency difference.
8. **Stretch goals.** Only update the criteria when a *pattern* appears across many decisions, not after a single one. Add a critical-reasoning check that flags items with inflated, unsupported claims. Add a guardrail that prevents the criteria from drifting too far in one update.

### How you will know you are done

- ✅ The criteria are written in plain prose, with no weightings, if-statements, or flowcharts.
- ✅ The human makes every real decision; the system only assists and the human can always override it.
- ✅ After a round of decisions, the learning agent proposes a criteria update as a diff the human confirms.
- ✅ The learning agent uses its tool to interpret relative feedback against real examples.
- ✅ Re-evaluating with the updated criteria visibly reflects the new preferences.
- ✅ The high-volume evaluation runs on a cheaper model than the learning agent, and you can show the cost gap.

> 💡 **Keep yourself honest:** if your criteria contain a number like "30% weighting," you have slipped back into rules. Rewrite it as prose.

---

## Practice exercises (optional extra reps)

> **What these are:** five small, self contained tasks, each focused on one skill. They are optional and independent. The **Capstone above is the main build** and already covers all of these.

### Exercise 1: rules to prose (foundational)
Take a rule-based scoring scheme (weightings or if-statements) for evaluating something and rewrite it as a prose criteria document with must have / nice to have / red flags. Note what the prose captures that the rules could not.

### Exercise 2: relative feedback (foundational)
Write three pieces of vague, relative feedback ("too junior," "not enough depth," "not the right background"). For each, describe what context an agent would need to interpret it correctly.

### Exercise 3: workflow vs agent (intermediate)
Take an evaluation task. Decide which parts should be a cheap fixed workflow and which should be a flexible agent. Justify the split in terms of volume and cost.

### Exercise 4: propose-and-confirm diff (intermediate)
Build a small flow where an agent reads a few decisions and proposes a change to a criteria document, output as a before/after diff that a human must confirm before it applies.

### Exercise 5: pattern, not noise (advanced)
Add logic so your learning agent only updates the criteria once a pattern appears across N decisions, instead of reacting to a single one. Show that a one-off, unusual decision does not move the criteria.

---

## Cheat sheet

```text
SELF-IMPROVING EVALUATION (the pattern)
  PER ITEM (cheap workflow):  redact -> match against criteria -> evaluate
  HUMAN:                      decides + gives feedback  (human in the CENTER)
  LEARNING AGENT (on top):    observe decisions -> update the criteria doc

DESIGN RULES
  - Preferences ALWAYS evolve -> build for it from the foundation.
  - Write criteria as PROSE, not rules (no weightings / ifs / flowcharts).
  - Mirror how users think (must have / nice to have / red flags).
  - Feedback is relative to what the user just saw -> give the agent a tool
    to read the actual examples.
  - Update on PATTERNS (every ~100-200 decisions), not single events.

MODELS
  Constrained, high-volume, latency-sensitive -> fast/cheap (Haiku).
  Open-ended pattern finding, occasional      -> capable (Sonnet).
  Favor models that REASON CRITICALLY over sycophantic ones.

GUARDRAILS
  Build them into the ARCHITECTURE, not at the end.
  System = apprentice. User = master. Never overrule the user.
```

## How this connects to the rest of the course

- **Earlier, Module 2 · Lesson 3 (The Prompting Playbook):** evals, prose-over-rules, and choosing the right model and harness.
- **Earlier, Module 6 · Lesson 21 (AirOps chases friction):** the self-improvement and feedback-loop ideas that AirOps named as their next frontier.
- **Next, Module 6 · Lesson 23 (Teaching agents to learn):** the same "watch the team and update yourself" pattern, applied to social replies.
- **Later, Module 3 (Evals):** deeper coverage of building evaluation systems and graders.

---

*Source: "How Metaview built self-improving prompts for application review" by Nick Mayhew (Metaview), Code with Claude 2026, London. The talk was a walkthrough and live demo, so the ICP document and any code are illustrative reconstructions of the approaches described. Adapt model names and SDK details to the current versions.*

# Module 9 · Lesson 34: What Legal Agents Inherit from Coding Agents

> **Course:** Building with Claude, a self-paced course
> **Module 9:** In the field, industry case studies
> **Speaker:** Jacob Emmerling, Staff Software Engineer, Legora (London)
> **Source talk:** [What legal agents inherit from coding agents: Lessons from Legora](https://www.youtube.com/watch?v=nho1YAEPuwA) · [full transcript](../../transcripts/code-with-claude-2026-london-2026/12_what-legal-agents-inherit-from-coding-agents-lessons-from-legora.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

Coding agents are years ahead of every other field, so the fastest way to build a great agent for your own domain is to systematically borrow from them: **reuse** the parts that are already universal, **translate** the parts that are similar but not identical, and **invent** only the small remainder that is truly unique to your work.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you build a **Domain Agent** for a field you know, by working through the reuse / translate / invent framework deliberately. Everything before the Capstone fills in each of the three buckets with real examples. If you want the finish line first, jump to the **Capstone Project**, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[Code reuse](https://en.wikipedia.org/wiki/Code_reuse)** (essay). The durable engineering principle behind the lesson's core move: don't reinvent; reuse what exists, adapt the pattern, and invent only the remainder.
> - **[Legal technology](https://en.wikipedia.org/wiki/Legal_technology)** (essay). A domain primer covering due diligence, document automation, and the verifiability requirement central to legal agents.

## A few plain-language basics first

This lesson leans on a few agent and document terms. Here they are in plain words:

- **LLM (Large Language Model):** the kind of AI that reads and writes text. Claude is an LLM.
- **Agent:** an AI that takes a series of actions on its own toward a goal, in a loop, rather than answering in one shot.
- **Coding agent:** an agent built to write and edit software (Claude Code is one). These are the most advanced agents in existence, because the whole industry has poured effort into them.
- **Harness:** all the code and machinery around the model: the loop that runs it, the tools you give it, how it reads and writes things. The model is the engine; the harness is the rest of the car.
- **Tool:** a function the agent can choose to call, for example "read this file" or "make this edit."
- **Human-in-the-loop:** points where the agent pauses to ask a person to approve something before continuing.
- **.docx:** a Microsoft Word file. Under the hood it is a zip of XML files with lots of metadata, so it is much messier to edit than plain text.
- **Linter:** a tool that automatically checks a document or file for mechanical problems (broken references, style errors) and reports them. ESLint is a famous one for JavaScript.
- **Reinforcement learning / fine-tuning:** ways model makers train a model to be especially good at certain tasks. You do not need the details; just know coding agents benefit hugely from it.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Legora builds collaborative AI for lawyers, used by over a thousand customers including some of the largest law firms in the world. Six months before this talk, the team had a realization: coding agents were racing ahead while every other field, including theirs, lagged behind. Instead of inventing everything from scratch, they asked a better question: *what can we steal from coding agents?* That single reframing is the most transferable idea in the talk. As Jacob says, the parallels are not magic to law and code, "there's a lot of parallels between any kind of knowledge work and coding." So whatever vertical you build for, this lesson gives you a repeatable way to ride the coding-agent wave.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain *why* coding and many other knowledge-work fields share deep structural parallels.
2. Sort agent capabilities into three buckets: **reuse**, **translate**, and **invent**.
3. Apply the key "translate" insight: make your agent's harness *look like* a coding agent's harness (read, edit, verify in a loop) so it inherits the benefits of all that coding-focused training.
4. Identify the small set of capabilities you genuinely have to **invent** for your own domain, and how to ground them (for example with citations).

## Prerequisites

- Familiarity with how an agent works in a loop (Module 2 and earlier agent material).
- Helpful but optional: any hands-on time with a coding agent like Claude Code.

---

## Part 1: why coding and your domain are cousins

We have all watched AI for coding go from bad autocomplete to good autocomplete to chatbots to agents to background agents, and it shows no sign of slowing. The striking thing six months before this talk was how far *behind* other fields were. Why?

Jacob's answer is that coding and legal work share a surprising number of structural features, and so does most knowledge work:

| Shared feature | In coding | In legal work |
|---|---|---|
| Built on prior work | You reuse libraries, patterns, existing code. | Lawyers reuse precedent, templates, prior filings. |
| Text-based documents | Source files. | Contracts, memos, filings. |
| Strict conventions | Each codebase and team has its style. | Each firm has its house style and rules. |
| Strong review culture | Pull requests reviewed before shipping. | An associate drafts, a partner reviews and signs off. |

> 🔑 **Key idea: the parallels are not unique to law and code.** They show up "between any kind of knowledge work and coding." So if you build for accountants, doctors, analysts, or anyone else, doing this comparison exercise is worth your time. The obvious next question, in Jacob's words, becomes "how do we get in on coding agents getting better and better to make our vertical better?"

The answer is three buckets.

---

## Part 2: the three buckets, reuse, translate, invent

> 🔑 **The framework.** Every capability a coding agent has falls into one of three buckets for your domain:
> 1. **Reuse:** works one-to-one, copy it as is.
> 2. **Translate:** looks similar to a coding sub-problem but is not identical; copy the *pattern*, not the code.
> 3. **Invent:** genuinely unique to your domain; you have to build it yourself.

### Bucket 1: reuse (you get it for free)

Some things coding agents figured out turn out to be universal to all agents: to-do lists, planning, sub-agents, sandboxes, human-in-the-loop. These are exactly the things you get "for free when using the Anthropic Agent SDK or managed agents."

Two examples mapped straight across from coding to legal with no changes:

- **Planning mode.** With a coding agent, you do not just fire off a big task and let it run for hours; you plan first. Planning explores the problem together with the agent, gathers context, and makes the big decisions up front so the agent does not have to guess mid-task. Legora does exactly this: for any big legal task, the lawyer plans the work with the agent, iterates on the plan, and only then lets it execute. A one-to-one lift of the UX.
- **Approving dangerous tool calls.** You do not want a coding agent running random shell commands without asking. The same UX maps directly to legal: you do not want the agent silently deleting important client documents, so it pauses for approval. Because coding agents already found the right UX, Legora skipped the whole "what should this feel like?" iteration loop.

> 💡 The win of the reuse bucket is *avoided work*. Coding agents already spent the iterations figuring out the right experience for these. You inherit the answer.

### Bucket 2: translate (the heart of the talk)

The most important example is **document editing**, and it shows the difference between translating well and translating badly.

Lawyers live in Microsoft Word. So Legora had to make the agent edit `.docx` files brilliantly. That is harder than it sounds: a `.docx` is "a zip file of a bunch of XML files with a lot of metadata and a lot of noise," not a clean text file.

**The old approach (before the realization).** Legora used a chain of specialised models handing work to each other:

```text
top-level agent
   -> hands an "editing intent" to a reasoning model
        -> that model decides WHERE edits go (page 1, 3, 5, 6) but not the full text
             -> individual models write out each full edit, with style, aware of context
```

This solved one real problem: **exhaustiveness**. (Exhaustiveness means actually making *all* the required edits. The reasoning model used to get "lazy" and stop filling out a template halfway through.) But the handoff design created new problems. Each step had independent reasoning, different context, and different tools, so you got "all these handoff problems." Add a new tool to the top-level agent and it might tell the editing model to fetch context using a tool the editing model does not even have. The more powerful the main agent got, the more these weird breakages appeared.

> ❌ **The anti-pattern:** a chain of independent models with different contexts and tools handing work off to each other. Every new capability you add risks breaking a handoff you forgot about.

**What coding agents do instead.** Jacob and his team, being daily users of coding agents, noticed those agents all converged on something much simpler: **read, edit, verify, in a loop**.

```text
LOOP:
  read     (line-based, plain text)
  edit     (string replace / patch / line edit tool)
  verify   (reason about what to do next, or run a type checker / linter)
  repeat
```

They tested this on big documents (large legal-style files, twenty surgical edits) and it "just worked," with none of the exhaustiveness issues. So they rebuilt their editing the same way:

```text
.docx file
   -> transform into an "intermediate representation":
      a single flat, text-based view the agent can read and edit
   -> LOOP: read tool / edit tools / verify step
      (the agent sees its own edits and keeps looping)
   -> transform the edited representation back into .docx
```

The "aha" moment is worth the price of admission. To stress-test the new harness, they asked it to translate a 10-page document paragraph by paragraph from English to Swedish, a task the old setup struggled to do exhaustively. The new loop edited paragraph by paragraph, occasionally re-read the whole thing, noticed a paragraph it had missed, went back and fixed it, and after about ten minutes the whole document was translated. The kicker: they ran it on **Haiku**, a small, fast model, "so this wasn't even a good model," and it still worked.

> 🔑 **The deepest insight in the talk (paraphrased):** make the model "almost feel like it's inside a coding agent harness, and it just does a legal task." Because then you inherit all the reinforcement learning and fine-tuning the labs poured into coding harnesses. Your harness looks similar in tool design, the model's tool-calling trajectories look similar, "and a lot of stuff you just get for free."

A second translate example: **linting for legal documents**, "basically ESLint for legal documents." Engineers rely on type checkers and linters to give agents a feedback loop on mechanical correctness. Legal documents have plenty of mechanical things to check too. If a contract references a paragraph and the agent deletes that paragraph, a linter can statically catch the now-broken reference and tell the agent, "you might want to fix the section that referenced this." You can push this further with LLM-based checks inside the linter, making the feedback loop "feel very similar to coding."

### Bucket 3: invent (the last 20%)

Some things are genuinely specific to your domain, and you must build them. For Legora, the prime example is **due diligence**: when company A buys company B, a lawyer must review *all* of company B's contracts, sometimes thousands of them.

Legora's tool for this is **Tabular Review**: a grid where each row is a document and each column is a piece of data to extract. Instead of reading every document, you lean on an LLM to extract the relevant facts (parties, red flags) into the grid, then filter down to what needs a deeper look. When building their agent, they simply gave it access to Tabular Review "in the same way that a human would use it": the agent throws a folder of documents in, specifies what to extract, and filters the grid to find what is relevant.

> 💡 Every domain has an "invent" bucket. Accountants need mechanical reconciliation; doctors have their own specific tasks. Jacob calls this "the last 20% of your agent to make it really well for a specific domain."

> 🔑 **Grounding is part of inventing.** A truly domain-specific need for Legora is **grounding every answer in citations**, so a lawyer can verify exactly where each claim in the agent's output came from. In the demo, every extracted data point links back to the highlighted passage in the source document, and a human can mark it verified, tracking review progress and collaborating with both AI and other humans on the same surface.

---

## Part 3: the demo, all three buckets at once

In the live demo, a lawyer asks the agent to "give every employee an extra week of vacation during Christmas" and to plan the work first. Watch the buckets light up:

1. **Reuse (planning + human-in-the-loop):** the agent first explores its environment, searching the employment agreements and the HR policy, then writes a plan (review agreements, amend them with a Christmas shutdown clause, update the HR policy). The lawyer can iterate on the plan and then send it off, exactly like a coding agent's plan mode. As Jacob notes, dropped into a codebase an agent would also "go out and collect all this context" first; here it discovers on its own that there is a policy and five agreements to update.
2. **Translate (the editing loop):** execution runs "this exact editing loop": read the documents, reason about edits, call an edit tool, re-read to verify. Edits stream in as redlined changes (tracked changes a lawyer can review), with correct formatting and indentation. It even unifies an agreement that already had the clause.
3. **Invent (due diligence + citations):** in a second demo over ~100 random documents, the agent builds a Tabular Review, extracts categories, parties, and red flags, and moves all employment agreements into a folder. A human can open any cell, see the LLM's reasoning, click through to the cited passage, and mark it verified.

> ✅ This is the whole framework in motion: the boring, universal parts came for free, the editing loop was translated from coding agents, and the due-diligence surface was the bit Legora had to invent.

---

## Part 4: why coding leads, and the lasting strategy

Jacob is candid that he is not sure exactly why coding is so far ahead. Maybe engineers are more willing to try new tools. Maybe coding gets disproportionate focus because solving it unlocks growth everywhere else. But here is the liberating part:

> 🔑 **You do not need to know why coding leads to benefit from it.** "You can just keep looking at what coding agents ship, and you can reuse what's usable for your domain, you can translate stuff that's similar but not really the same, and then the last part you actually invent."

That is the durable strategy for any vertical agent: treat coding agents as a free research lab. Whenever they ship something new, ask which bucket it falls into for you, and steal accordingly.

---

## Key takeaways

1. **Coding agents are the frontier.** Use them as a template, not a competitor.
2. **Sort every capability into reuse, translate, or invent.** It tells you exactly how much work each one is.
3. **Reuse the universals for free:** to-dos, planning, sub-agents, sandboxes, human-in-the-loop. The Agent SDK gives many of these out of the box.
4. **Translate by mimicking the coding harness.** Read, edit, verify in a loop, even for messy formats like `.docx`. A harness that looks like a coding harness inherits all the coding-focused training, so much works "for free," even on a small model.
5. **Avoid the handoff chain.** Independent models with different contexts and tools handing off to each other breaks as your agent grows.
6. **Invent only the last 20%,** and ground it. Citations let humans verify high-stakes output.

## Common pitfalls

- ❌ Building everything from scratch when coding agents already solved most of it.
- ❌ A chain of specialised models passing intents to each other (handoff problems multiply as you add tools).
- ❌ Editing complex formats directly instead of via a clean intermediate text representation the agent can loop over.
- ❌ Forgetting to give the agent a verify step (a linter or checker) to close the feedback loop.
- ❌ Treating citations as a bolt-on at the end rather than building them in so output is verifiable.
- ❌ Spending invent-bucket effort on things you could have reused or translated.

---

## 🛠️ Capstone Project: build a Domain Agent with the three buckets

> This is the main hands on project for the lesson. You will build a small **Domain Agent** for a field you understand, deliberately working the reuse / translate / invent framework. Start with a single document type and one task, then grow.

### What you will build

An agent that performs a real task in your chosen domain by: reusing universal agent features, translating the read-edit-verify loop to your document type, and inventing one domain-specific capability with citations. The deliverable is a working agent plus a one-page "bucket map" showing which capability came from where.

> 🎯 **Pick your world.** Choose a domain where work is text-heavy, convention-bound, and reviewed: contracts, marketing copy, financial reports, research papers, recipes, lesson plans. You need (a) a document the agent edits, (b) a mechanical thing you can check (a "linter"), and (c) one task that is genuinely specific to your field.

### Why this is the perfect practice

| Lesson idea | Where you use it in the Domain Agent |
|---|---|
| Reuse the universals | Milestone 2, planning + approval, ideally via the Agent SDK |
| Translate the harness | Milestone 3, read-edit-verify on your document type |
| Intermediate representation | Milestone 3, flatten a messy format to editable text |
| The verify step / linter | Milestone 4, a mechanical check the agent can act on |
| Invent the last 20% | Milestone 5, your domain-specific capability |
| Grounding with citations | Milestone 5, every claim links to its source |
| Coding agents as a free lab | Milestone 6, the ongoing-steal habit |

### Milestones (build them in order, each one works on its own)

1. **Make a bucket map.** List the capabilities your agent needs. Sort each into reuse, translate, or invent. This map is your build plan.
2. **Reuse the universals.** Add planning mode (the agent drafts a plan you approve) and a human-in-the-loop approval before any "dangerous" action. Use the Agent SDK if you can, to feel how much is free.
3. **Translate the editing loop.** Pick a document type. If it is messy (like `.docx`), write a transform to a flat, text-based representation. Give the agent read, edit, and verify tools and let it loop. Test on a real document and a fast/cheap model to see how far the harness alone carries you.
4. **Add a linter (the verify step).** Write one mechanical check for your domain (a broken cross-reference, a missing required section). Feed its output back to the agent so it can fix the problem.
5. **Invent your last 20%.** Build one capability unique to your domain (a structured extraction grid, a reconciliation, a compliance check). Ground its output: every claim must link back to the source it came from, so a human can verify it.
6. **Adopt the steal habit.** Pick one feature a coding agent shipped recently, decide its bucket for you, and write down how you would adopt it. Make this a recurring practice.
7. **Stretch goals.** Add a verification/sign-off surface where a human marks results verified and progress is tracked. Add sub-agents for parallel sub-tasks. Run the whole thing on a small model and note what still works.

### How you will know you are done

- ✅ Your agent plans first, asks before dangerous actions, and edits your document type reliably in a loop.
- ✅ You can point at each capability and say which bucket it came from, with no wasted reinventing.
- ✅ A messy format is edited via a clean intermediate representation, not directly.
- ✅ Your linter catches at least one mechanical error and the agent fixes it.
- ✅ Every output claim links to a citation a human can click and verify.

> 💡 **Keep yourself honest:** if a capability is in your "invent" bucket, double-check it really is unique. Most things you think you must invent are actually reuse or translate.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each focused on one idea. They are optional and independent. The Capstone above covers all of them.

### Exercise 1: the parallels table (foundational)
Pick a non-coding domain. Fill in a four-row table mapping it to coding on: prior work, text documents, conventions, and review culture. What does this tell you about how agentable it is?

### Exercise 2: bucket sort (foundational)
List ten capabilities a great agent in your domain would have. Sort each into reuse, translate, or invent. Which bucket is biggest, and is that surprising?

### Exercise 3: flatten a messy format (intermediate)
Take a non-plain-text format (a spreadsheet, a Word file, JSON). Write a transform into a flat, line-based text view an agent could edit, and a transform back. Confirm a round-trip preserves the content.

### Exercise 4: write a domain linter (intermediate)
Write one static check for your domain's documents (a broken reference, a missing section, an inconsistent term). Make its output a clear, actionable message an agent could act on.

### Exercise 5: ground an answer (advanced)
Take an extraction task. For every fact your agent outputs, attach a citation pointing to the exact source location. Build a tiny viewer that lets a human click a fact and see the highlighted source.

---

## Cheat sheet

```text
BUILD A VERTICAL AGENT BY STEALING FROM CODING AGENTS

THREE BUCKETS
  REUSE ...... works 1:1. to-dos, planning, sub-agents, sandboxes, human-in-loop.
               (free with the Agent SDK / managed agents)
  TRANSLATE .. similar but not identical. copy the PATTERN, not the code.
  INVENT ..... unique to your domain. the last 20%. ground it with citations.

THE KEY TRANSLATE MOVE
  Make your harness look like a CODING harness:
    LOOP: read -> edit -> verify
  Messy format? transform to a flat text "intermediate representation",
  edit there, transform back.
  Why: you inherit coding-focused RL/fine-tuning. Lots works for free,
       even on a small model.

AVOID
  Chains of independent models handing off intents (handoff problems multiply).

LASTING STRATEGY
  Coding agents are a free research lab. Whatever they ship, pick its bucket, steal it.
```

## How this connects to the rest of the course

- **Earlier, Module 2 (Core skills):** planning, tools, and the read-edit-verify loop in their original coding-agent context.
- **Next, Module 9 · Lesson 35 (Solve Intelligence):** another legal case that argues the *opposite* emphasis (collaboration over delegation) for a harder domain, a great contrast.
- **Next, Module 9 · Lesson 37 (Omni):** echoes the same idea that being a heavy user of coding agents teaches you what a good harness looks like.
- **Later, modules on the Agent SDK and managed agents:** the "reuse for free" bucket is exactly what those provide.

---

*Source: "What legal agents inherit from coding agents: Lessons from Legora" by Jacob Emmerling (Legora), Code with Claude 2026, London. Code and pseudo-code blocks are illustrative reconstructions of the architecture described in the talk; the speaker showed diagrams and a live demo rather than full code listings.*

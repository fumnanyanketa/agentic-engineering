# Module 9 · Lesson 35: Where Code Meets Court

> **Course:** Building with Claude, a self-paced course
> **Module 9:** In the field, industry case studies
> **Speaker:** Olly Cobb, Founding AI Engineer, Solve Intelligence (London)
> **Source talk:** [Where code meets court: AI at the legal-technical frontier](https://www.youtube.com/watch?v=T8N0MED3IJo) · [full transcript](../../transcripts/code-with-claude-2026-london-2026-day-2/09_where-code-meets-court-ai-at-the-legal-technical-frontier.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

Not every domain suits the "describe it and let the agent run" model of delegation; when outputs cannot be cheaply tested and decisions are tightly tangled together, you should design for **collaboration** instead, where the AI surfaces the right judgment calls at the right time and the human imparts judgment as the work takes shape, supported by citations, dedicated interfaces, and parallelized analysis.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you build a **Collaboration-First Assistant** for a domain where delegation breaks down, applying the three design principles from the talk. Everything before the Capstone explains *when* and *why* to choose collaboration, and the principles you will implement. If you want the finish line first, jump to the **Capstone Project**, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[Human-in-the-loop](https://en.wikipedia.org/wiki/Human-in-the-loop)** (essay). The lesson's collaboration model maps directly onto the established human-in-the-loop spectrum and its accountability rationale: design for collaboration when you can't cheaply validate output.
> - **[Legal technology](https://en.wikipedia.org/wiki/Legal_technology)** (essay). A domain primer; agentic legal systems succeed on verifiable, trustworthy outputs, matching the lesson's citations-as-first-class principle.

## A few plain-language basics first

This lesson uses AI and a little patent-law vocabulary. Here it is in plain words:

- **LLM (Large Language Model):** the kind of AI that reads and writes text. Claude is an LLM.
- **Agent:** an AI that takes a series of actions on its own toward a goal, in a loop.
- **Delegation model:** "you describe what you want and hand the whole job to an agent," which runs autonomously and gives you a result to check. This is how Claude Code and Cowork often work.
- **Collaboration model:** instead of handing off the whole job, the human and AI work *together* step by step, with the human making key decisions as the work unfolds.
- **Citation (here):** a link from something the AI says back to the exact source it relied on, so a human can verify it.
- **Sub-agent:** a smaller agent the main agent spins up to handle a piece of the work, often in parallel.
- **Compaction:** shrinking a long conversation history so it still fits the model's memory; it can accidentally drop the trail of where facts came from.
- **Out of distribution:** something the model has not really seen in training, so it has to reason from general knowledge rather than recognise a familiar pattern.
- **Patent:** a legal grant of a temporary monopoly over an invention, in exchange for publicly disclosing how it works. You will not need deep patent knowledge; the lesson explains just enough.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Solve Intelligence builds software for patent lawyers, a field that sits at the intersection of the two domains where AI is most valuable: deep technical reasoning (like software) and finding needles in haystacks of documents (like much legal work). Because the stakes are so high, patent work makes the trade-offs unusually visible. The big, transferable lesson is a question every builder should ask before reaching for an autonomous agent: *does my domain actually suit delegation?* Olly gives you a sharp test for that, and a set of design principles for when the answer is no. As he puts it, the goal is to help you "better think about what and how to build for your own domains, or even identify domains that might be worth serving in the first place."

## Learning objectives

By the end of this lesson you will be able to:

1. Recognise the **delegation model** and name the two conditions under which it breaks down: outputs that cannot be cheaply validated, and decisions that are tightly entangled.
2. Explain the **collaboration model** as the alternative, and the AI's twofold role within it.
3. Apply three design principles: **citations as a first-class citizen**, **interfaces that route into the general agent**, and **parallelizing alignment while sequencing execution**.
4. Decide, for your own domain, whether to design for delegation or collaboration, and why.

## Prerequisites

- Familiarity with how an autonomous agent works (Module 2 and earlier agent material).
- Helpful but optional: Module 9 · Lesson 34 (Legora), which argues the complementary case for reusing coding-agent patterns.

---

## Part 1: a quick tour of patents (just enough)

To follow the argument, you need a little context. At its core, Olly explains, a patent is "a social contract between an inventor and society": in exchange for publicly disclosing exactly how an invention works, the state grants a roughly 20-year monopoly over making, using, or selling it. The aim is to reward innovation while eventually feeding the knowledge into the public domain.

To be granted, an invention must be:

| Criterion | Plain meaning |
|---|---|
| **Novel** | Never previously known to the public, anywhere. |
| **Non-obvious** | Not obvious to a notional skilled-but-uninventive practitioner in the field. |
| **Useful** | Actually good for something, so it is worth examining. |
| **Sufficiently disclosed** | Described well enough that a skilled person could reproduce it. |

A patent application has **claims** (the precise sentences that define the legal scope of protection), a **description**, line drawings, and an abstract. The claims are the heart of it. Every element of every claim must be supported in the description and drawings.

After you file, you enter **prosecution**: a back-and-forth with a patent examiner who flags problems in "office actions," to which the drafter responds by arguing or by narrowing the claims. Every argument becomes part of a permanent **file history** that shapes how the claims are later interpreted. Even after a patent is granted, it can be challenged in court.

> 🔑 **The crucial property:** decisions made while drafting and prosecuting "can have consequences which only reveal themselves many years into the future." An examiner might object in two years, a competitor might try to design around the patent in five, a litigator might try to invalidate it in ten. Keep this in mind; it is the whole reason delegation struggles here.

So the attorney must (1) understand a highly technical invention, (2) work out what is genuinely novel relative to all prior art, and (3) write a legal document in patent-specific syntax that anticipates future objections. A perfect fit for AI's strengths, but, as we will see, a poor fit for the *delegation* style of AI.

---

## Part 2: the delegation model, and when it breaks

Claude Code's success rests on a model of **delegation**: you describe what you want and hand implementation to an agent. Cowork generalises this. Olly's claim is that delegation does *not* lend itself to patent work, and he gives two fundamental reasons (the ones most likely to apply to your domain too) plus a few supporting ones.

### Reason 1: you cannot cheaply validate the output

In software, much of what you care about can be checked with tests or a few minutes of QA (quality assurance, manually trying it out). So you can specify at a high level, let the agent run autonomously, and validate cheaply. If it is wrong, you retry with an adjusted prompt.

> ❌ A patent cannot be run. Its correctness "is really a function of events that haven't happened yet." Your decisions are "bets against an adversarial future," trading one kind of risk for another based on the risk appetites of those who bear the consequences. There is no test to run, and no quick retry.

### Reason 2: the decisions are tightly entangled

In software, an agent can make hundreds of micro-decisions, and most can be revisited later without unwinding the rest. The ones that cannot are usually foreseeable up front and can be settled in a planning phase.

> ❌ In patents, decisions are not loosely coupled and do not surface up front. Claim scope, claim terminology, the spec, and the drawings all depend on each other, and "those dependencies don't reveal themselves until the document starts to take shape." Reframe claim one and you are sent back through many claims below it, through supporting passages, and through drawings.

> 🔑 **The killer is the combination.** Either problem alone would be survivable. If you could test correctness, entanglement would not matter (just iterate until the test passes). If decisions were independent and foreseeable, the attorney could specify everything up front and delegate the rest. But together, the human's judgment "can't be deferred to some final review pass and it can't be concentrated up front." It must be "imparted sequentially as the patent comes together," because each judgment constrains the next and nothing downstream will catch a bad one.

### Supporting reasons (briefly)

- **Out of distribution.** Software development recombines familiar patterns and suits reinforcement learning, so labs can hyper-optimise models for it. An invention is, by definition, something new the model has not seen, so this reasoning does not benefit from that training in the same way. Combine that with hallucinations being both harder to detect and more costly, and you want to move away from "let the agent figure everything out."
- **Non-textual data.** Software is natively text. Patents include line drawings and often chemical structures or biological sequences, and the model's ability to reason about them "depends meaningfully on how they're represented." Figuring out the best representation is a place the application layer adds real value.
- **Uniformity (a point for delegation).** Patents share a remarkably uniform structure, which narrows the space of implementations and might increase comfort with delegation. But that same uniformity is something a dedicated application can lean on, so it is not a clear win for delegation either.

> 💡 **The transferable test:** before building an autonomous agent, ask two questions. *Can I cheaply validate its output?* and *Are the key decisions independent and foreseeable up front?* If both are yes, delegation is great. If both are no, design for collaboration.

---

## Part 3: the collaboration model, and three principles

If delegation is wrong, what is right? Olly's answer: **collaboration**. The aim is to let the user iterate through that sequence of dependent, consequential decisions "flexibly, quickly, and effectively."

> 🔑 **The AI's role in collaboration is twofold:**
> 1. **Surface the judgment calls** at the moment they need making, in a way that makes the trade-offs clear, so the human can decide well.
> 2. **Execute on those calls once made,** whether by doing follow-up analysis or drafting part of the document.

The distinction is not binary. A delegation tool like Cowork still allows collaboration, and a collaboration tool still allows delegating chunks of work. But software centred on collaboration ends up looking quite different, in UI/UX and in the AI layer underneath. Olly shares three principles.

### Principle 1: treat citations as a first-class citizen

A **citation** here is a link from something the AI tells you back to the exact source it relied on. The point is not credibility-theatre; it is "a genuine audit trail of which sources of information actually shaped the final output."

> ❌ Many systems bolt citations on at the end to look trustworthy. That is the wrong approach. Citations should be fundamental.

> 🔑 Making citations first-class means: *any* information shown to the model (the document being edited, an uploaded disclosure, prior art pulled in at runtime) is presented "in a format from which it can cite," and the model communicates, both with the user and with other sub-agents, "in a manner that provides proper attribution." Citations "are actually a massive pain" because they fight with tool calling, sub-agents, and compaction, so you often have to engineer your own patterns for those. But if you want to understand how and why a decision was made, this is required.

### Principle 2: route dedicated interfaces back into the general agent

You usually want a general-purpose agent the user talks to in open-ended natural language. But for specific repeat workflows, a dedicated interface (with the right buttons and options) is easier for the user.

> 🔑 The principle: even for those dedicated interfaces, **translate what the user specifies into an instruction you pass to the general agent** (perhaps augmented with an extra tool or sub-agent), rather than building a separate, parallel system.

> 💡 Two benefits. The user still gets the familiar experience of the agent "showing its working" with reasoning and citations. And as you make the general agent more capable, *every* specific workflow built on top improves automatically.

### Principle 3: parallelize alignment, sequence execution

Since the work cannot be done in one long autonomous run, it becomes very valuable to find a set of decisions that, once aligned on with the human "in a concentrated moment of human sign-off," would enable a long autonomous run the user is unlikely to object to.

> 🔑 The analysis or research behind those decisions can often be done **in parallel** (hence the name), even though the resulting edits must be applied **in sequence**. The goal is to minimise both the number of touch-points with the user and the time spent navigating between them.

```text
PARALLELIZE ALIGNMENT          then     SEQUENCE EXECUTION
  run 30 reviews at once                 make edits one after another,
  -> produce COMMENTS for the human      keeping everything consistent
  -> human aligns / dismisses
  -> ONLY THEN kick off edits
```

---

## Part 4: the three principles, live

Olly demonstrates each principle in Solve's patent drafting module, where an attorney has uploaded the inventor's disclosure, an invention disclosure form, some prior art, and a patent application template.

1. **Principle 1 (citations).** He asks the general agent, "how does my invention compare to the prior art?" The agent reads the disclosure, reads the prior art, and replies with a comparison table identifying the most relevant prior art. Crucially, every claim carries a citation: click it and you see the exact passage in the source document it relied on. Verification, not decoration.
2. **Principle 2 (interface into the agent).** Drafting the claims uses a dedicated interface where the user expresses preferences (how many claims, how elements are indented, how labels are referred to). But the request is served by the *same* general-purpose agent, which still shows its reasoning and citations while drafting the claims around the novel part of the invention.
3. **Principle 3 (parallelize then sequence).** For application review, the agent runs separate sub-reviews for each criterion **in parallel** (in practice there might be 30 criteria). Going straight to edits would produce conflicting suggestions, so instead it first generates **comments** the attorney can read, reply to, or dismiss. Only after the human aligns on which comments matter does it kick off a **sequential** round of edits that keeps the document consistent. And layered on top, principle one again: the review is served by the general agent augmented with a comment-making tool, with citations throughout.

> ✅ Notice how the principles stack: the review (principle 3) is delivered through the general agent (principle 2) with full citations (principle 1). They are not separate features; they reinforce each other.

---

## Key takeaways

1. **Delegation is not universal.** It works when you can cheaply validate outputs *and* the key decisions are independent and foreseeable up front.
2. **The deadly combination** is outputs you cannot test plus decisions that are tightly entangled. Then judgment must be imparted sequentially, not deferred to a final review or concentrated up front.
3. **Choose collaboration** in that case: the AI surfaces judgment calls at the right moment and executes them once made.
4. **Citations are first-class,** not a bolt-on. Everything shown to the model must be citable, and the model must attribute its sources, even when that fights tool-calling, sub-agents, and compaction.
5. **Route dedicated interfaces into the general agent,** so users keep reasoning and citations, and improving the agent lifts every workflow.
6. **Parallelize alignment, sequence execution.** Do the analysis in parallel, get a concentrated human sign-off, then apply edits in order.
7. **Represent non-textual data thoughtfully;** how you show drawings, structures, or sequences to the model meaningfully affects its reasoning.

## Common pitfalls

- ❌ Reaching for an autonomous agent in a domain where you cannot cheaply test its output.
- ❌ Assuming entangled decisions can be settled up front in a single planning phase.
- ❌ Bolting citations on at the end for credibility instead of building a real audit trail.
- ❌ Building dedicated interfaces as separate systems instead of routing them through the general agent.
- ❌ Jumping straight to edits during review, producing conflicting changes, instead of aligning on comments first.
- ❌ Ignoring non-textual data, or feeding it to the model in a form it reasons about poorly.

---

## 🛠️ Capstone Project: build a Collaboration-First Assistant

> This is the main hands on project for the lesson. You will build a small **Collaboration-First Assistant** for a domain where delegation breaks down, implementing all three principles. Start with one document and one review criterion, then grow.

### What you will build

An assistant where a human and AI co-produce a high-stakes document: the AI surfaces judgment calls (as cited comments), the human aligns on them, and only then does the AI execute edits in sequence. Every claim the AI makes links to its source. The deliverable is a working assistant plus a short write-up arguing why your domain suits collaboration over delegation.

> 🎯 **Pick your world.** Choose a domain where outputs are hard to test and decisions are entangled: a grant proposal, a clinical care plan, an architecture design doc, a complex contract, a research paper's argument. You need (a) source documents the AI must rely on and cite, (b) multiple review criteria that can conflict, and (c) decisions where one choice constrains the next.

### Why this is the perfect practice

| Lesson idea | Where you use it in the Assistant |
|---|---|
| The delegation test (validate? foreseeable?) | Milestone 1, you justify choosing collaboration |
| Citations as first-class | Milestone 3, every claim links to its source |
| Surface judgment calls | Milestone 4, the AI proposes cited comments |
| Interface routes into general agent | Milestone 5, a dedicated workflow uses the same agent |
| Parallelize alignment, sequence execution | Milestone 4 and 6, parallel review then ordered edits |
| Non-textual representation | Stretch goal |

### Milestones (build them in order, each one works on its own)

1. **Justify the model.** Write one page applying the delegation test to your domain: can outputs be cheaply validated? Are key decisions independent and foreseeable? Conclude why collaboration fits.
2. **Set up the general agent.** Build a general-purpose agent the user talks to in natural language, that can read your source documents and answer questions about them.
3. **Make citations first-class.** Present every source to the model in a citable format, and require that every claim in its answers links back to the exact source location. Build a viewer so a human can click a claim and see the highlighted source.
4. **Surface judgment calls in parallel.** For a review task, run several criteria checks *in parallel* and have the agent produce **comments** (with citations) rather than edits. The human can reply to or dismiss each.
5. **Route a dedicated interface into the agent.** Build one structured workflow (for example "draft section X with these preferences") whose inputs are translated into an instruction passed to the *same* general agent, so reasoning and citations still appear.
6. **Sequence the execution.** Only after the human aligns on comments, kick off an *ordered* round of edits that resolves them while keeping the document consistent. Show each edit with its citation.
7. **Stretch goals.** Handle a non-textual element (an image, a diagram, a table) and experiment with two representations to see which the model reasons about better. Scale the parallel review to many criteria.

### How you will know you are done

- ✅ You can clearly argue, using the delegation test, why your domain needs collaboration.
- ✅ Every claim the assistant makes links to a source a human can click and verify.
- ✅ Review produces cited comments first; edits happen only after the human aligns.
- ✅ At least one dedicated interface is served by the same general agent (not a separate system).
- ✅ Analysis runs in parallel, but edits are applied in a consistent sequence.

> 💡 **Keep yourself honest:** if a human can press one button, walk away, and trust the result without checking, your domain probably suited *delegation* all along, and you have over-built.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each focused on one idea. They are optional and independent. The Capstone above covers all of them.

### Exercise 1: run the delegation test (foundational)
Take three tasks from your work. For each, answer: can the output be cheaply validated? Are the key decisions independent and foreseeable up front? Sort them into "delegation" and "collaboration."

### Exercise 2: spot the entanglement (foundational)
Pick one document-producing task. Map which decisions depend on which others. Find one decision whose change would ripple back through many earlier ones. That ripple is why up-front planning is not enough.

### Exercise 3: real citations (intermediate)
Take an agent answer and retrofit real citations: every factual claim must link to the exact source passage. Note where tool calls or summarisation broke the trail, and how you fixed it.

### Exercise 4: comments before edits (intermediate)
For a review task, build the flow where the agent first emits comments for human alignment, then only edits the aligned ones. Compare the result to letting it edit directly.

### Exercise 5: representation matters (advanced)
Take some non-textual data (a chart, a diagram, a table). Feed it to the model in two different representations and compare the quality of its reasoning. Which representation wins, and why?

---

## Cheat sheet

```text
DELEGATION vs COLLABORATION

THE TEST (run before building an autonomous agent)
  Q1: can I cheaply VALIDATE the output? (tests, quick QA)
  Q2: are the key decisions INDEPENDENT and FORESEEABLE up front?
  both YES -> delegation is great
  both NO  -> design for COLLABORATION

COLLABORATION = AI does two things
  1. SURFACE judgment calls at the moment they're needed (with trade-offs clear)
  2. EXECUTE those calls once the human decides

THREE PRINCIPLES
  1. Citations first-class .... everything citable; the model attributes sources
                               (engineer your own tool-call / subagent / compaction patterns)
  2. Interfaces -> general agent . dedicated UIs translate to instructions for the
                               one general agent; improving it lifts every workflow
  3. Parallelize alignment, .. run analysis in parallel -> comments -> human aligns
     sequence execution        -> THEN ordered edits that stay consistent

ALSO
  Represent non-textual data carefully; it changes how well the model reasons.
```

## How this connects to the rest of the course

- **Earlier, Module 9 · Lesson 34 (Legora):** argues for *reusing* coding-agent (delegation-style) patterns; this lesson is the deliberate counterpoint about when delegation fails. Read them together.
- **Earlier, Module 9 · Lesson 33 (Qonto):** shares the human-in-the-loop and audit-trail instincts for high-stakes work.
- **Next, Module 9 · Lesson 37 (Omni):** another harness story, with the same emphasis on grounding answers in real, citable context.
- **Later, modules on sub-agents and context management:** the hard engineering behind first-class citations (tool calls, sub-agents, compaction) lives there.

---

*Source: "Where code meets court: AI at the legal-technical frontier" by Olly Cobb (Solve Intelligence), Code with Claude 2026, London. The diagram and code-style blocks are illustrative reconstructions of the principles described in the talk, which was delivered with slides and a live demo rather than code listings.*

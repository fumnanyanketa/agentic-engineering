# Module 6 · Lesson 23: Teaching Agents to Learn from Your Team

> **Course:** Building with Claude, a self-paced course
> **Module 6:** Advanced agent engineering
> **Speaker:** Petra, Head of Developer Experience, Warp (London)
> **Source talk:** [Teaching agents to learn from your team](https://www.youtube.com/watch?v=uGroRwlC9y4) · [full transcript](../../transcripts/code-with-claude-2026-london-2026-day-2/12_teaching-agents-to-learn.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

For "fuzzy" tasks that need judgment and taste (where you cannot just run a unit test), the way to close the gap between an agent that "sort of works" and one you trust in production is to write instructions as principles (not rules), teach the agent how to learn from feedback, and design a near-effortless daily feedback loop that lets it improve itself from what your team is already doing.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you build **Echo**, a teammate-style agent that triages a fuzzy stream of items, learns from your reactions, and opens a daily pull request to improve its own instructions. Everything before the Capstone teaches the pieces you will assemble there.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[Training language models to follow instructions with human feedback (InstructGPT)](https://arxiv.org/abs/2203.02155)** (paper). The seminal RLHF paper: for fuzzy, taste-driven objectives you align a model by learning from human preferences and corrections, not from hand-coded rules.

## A few plain-language basics first

This lesson uses some everyday AI and software terms. Here they are in simple words:

- **Agent:** an AI that takes a series of actions on its own toward a goal, rather than answering in one shot.
- **Skill / skill file:** a Markdown file that tells an agent how to do something. Warp's agent is built almost entirely from these, with almost no traditional code.
- **Agentic primitives:** the basic building blocks (skills, tools, triggers) you assemble agents from.
- **Prompt:** the text instructions you give the model.
- **Judgment and taste:** the hard-to-pin-down sense of *when* to act, *what* to say, and *how* to say it. The opposite of a clear-cut, testable rule.
- **Unit test:** a small automated check that says pass or fail. Easy for code, hard for taste.
- **The Ralph loop:** an agentic loop that keeps iterating because it has an external check (like a test suite or a browser) telling it whether it has reached its goal yet.
- **Feedback loop:** a repeating cycle where the agent acts, gets feedback, and improves. The centerpiece of this lesson.
- **Pull request (PR):** a proposed change to a code (or here, skill) repository that a human reviews before it is merged in.
- **Git repo:** the version-controlled store where files (here, skill files) live, so changes are tracked and reviewable.

You do not need to memorise these. Each is explained again the first time it appears.

## Why this lesson matters

Petra opens with a show of hands. Lots of people have built an agent. Fewer have one running daily. Far fewer have one still in daily production that they are genuinely happy with. That gap is the whole lesson.

> 🔑 **The "80 percent but not quite" graveyard.** Petra describes the place where most agents die: it "kind of sort of works," it is roughly 80 percent there, but not good enough to just let it run on its own. You end up spending so much time tweaking and re-prompting it that it can feel "almost worse than if you would not have an agent."

The deeper problem is that the usual way agents improve, the **Ralph loop** (keep iterating against an external check), only works when you *have* an external check. Coding agents have unit tests and browsers to tell them whether they succeeded. But for tasks that need **judgment and taste**, like writing a good social media reply, there is no quick pass/fail signal. You would have to send real replies live and watch how the community reacts over days. This lesson is about how to give an agent judgment and taste anyway, and how to close that last gap to production.

## Learning objectives

By the end of this lesson you will be able to:

1. Tell apart tasks with a clean **external check** (good for a Ralph loop) from **fuzzy** tasks that need judgment and taste.
2. Write agent instructions as **principles, not rules**, and explain why principles generalize and rules break.
3. **Teach an agent how to learn**: have it close the gap between its output and the ideal output by adjusting its *principles*, not by tacking on brittle rules.
4. Design a **low-friction daily feedback loop** that learns from what your team already does (emoji reactions, Slack notes).
5. Keep humans in control by routing the agent's self-improvements through **pull requests**.

## Prerequisites

- Module 6 · Lesson 22 or any earlier lesson on self-improving systems.
- Helpful but optional: familiarity with Git and pull requests, and with the idea of an agentic loop.

---

## Part 1: meet Buzz, and the fuzzy-task problem

Warp builds a terminal where you run and manage agents. Petra's team built **Buzz**, an agent that monitors Warp's social mentions and helps decide what to do with each one: **reply** (a question or product feedback), **like** (shows appreciation, no words needed), or **skip** (not about Warp, or no response expected). When Buzz suggests a reply, it also drafts the message so the team does not start from scratch.

Buzz was built in a few days, is composed of about 15 skills (Markdown files), and has essentially **zero code written**. It connects to services like the X API and Slack.

The challenge is that social replies need judgment and taste: when to speak, what to say, how to say it, and crucially when to stay out completely. We have all seen the obviously AI-generated replies you can spot "from a mile away." Warp wanted the opposite: replies that genuinely sound human and understand the product and company context.

> 🔑 **Why the Ralph loop does not fit here.** The Ralph loop works for coding because there is "an external track that allows the agent to know if it's there or not": run the test suite, check the browser, see if the change worked. For social replies there is no such quick check. The real feedback (community reaction, brand perception) is "super complex and long." So the question becomes: how do you get judgment and taste *into* the agent another way?

---

## Part 2: principles, not rules

The team started where most people start: trying to nail the prompt. They crafted a prompt, then worked with the agent to find conflicts, ambiguities, and gaps. The result, though, drifted into a **checklist of rules**: "if X happens, do Y."

> ❌ **Why rules failed.** The rule-based prompt "sounded like a robot" because it could not figure out what to say or how to say it. And it "broke the moment something new appeared," because rules are too brittle to handle situations they did not anticipate.

The fix came from a simple reframe: *how would you explain this to a new team member?* You would not hand them a list of if-X-then-Y rules. You would explain how to *think*: the purpose of engaging with the community, how to make good decisions, and guidelines like "don't get defensive when users complain, be kind and empathic, come across as a product builder rather than someone processing support requests."

> 🔑 **Switch from rules to principles.** Principles tell the agent how to reason, so it can handle new situations gracefully. Rules tell it exactly what to do, so it shatters on anything unexpected.

The payoff was concrete and surprising:

> 💡 **Smaller file, better output.** After switching to principles, the skill file shrank to "about a fifth of the original length," and the output got *better*, because the agent could reason flexibly about new situations. Less text, more capability.

---

## Part 3: teaching the agent how to learn

Principles got Buzz close, but not quite to "send this live as is." So the team did what any good engineer does: collect outputs, evaluate them, and give feedback. Petra would gather a batch of mentions, let Buzz triage and draft replies, and then comment: "this is good because ABC," "this is not good because XYZ," "here is how I would actually reply," "I wouldn't reply to this at all because XYZ."

Then she asked Buzz to learn from that feedback. And Buzz immediately fell back into a bad habit.

> ❌ **The agent's instinct: add brittle rules.** Given feedback, Buzz wrote hyper-specific rules like "if a person is having problem X, never mention pricing in the first line." It worked for that one case but generalized to nothing.

The better lesson, from the same feedback, would have been a *principle*: "if someone is venting about the product, don't try to pitch them another part of the product." That generalizes.

So the team realized the agent needed to learn *how to learn*. Again, the new-team-member frame helped. You would not just give a person the corrected answer; you would explain *why* it is better, and ask them to compare their output to the ideal and figure out what their *instructions* would need to be to produce that ideal next time.

> 🔑 **Teach learning as a skill.** Warp encapsulated this in another skill that tells the agent: look at what you did, look at the ideal output, look at your current instructions, find the gap, and adjust your *principles* (not add a one-off rule) so you would produce the ideal next time.

After this, Buzz had two components working together: **principles** (what to do, flexible across new situations) and a **way to learn** (how to expand and refine its own principles from feedback).

---

## Part 4: the low-friction daily feedback loop

Two pieces were in place. The missing piece: who keeps teaching it? Sitting down to give batches of feedback takes time, and nobody wants another meeting or a rotation chore. The breakthrough was to have the agent learn from what the team was *already doing*.

> 🔑 **The hardest part of a feedback loop is the humans.** "If it's too complicated or if it takes too much time or too out of the normal process, they're just simply not going to do it." Design for the **smallest input from the team for the biggest output for the agent.**

Here is the loop Warp designed, which requires almost no extra effort:

```text
1. Buzz monitors mentions and posts to a Slack channel:
   "Here's a mention. Suggested action: REPLY / LIKE / SKIP.
    Reasoning: ... Draft message: ..."
2. The team skims the channel (they monitor it anyway) and adds an
   EMOJI REACTION for the action they actually took (e.g. a check mark
   if they replied). They can also leave a NOTE in the thread.
3. Buzz runs daily. It compares what it SUGGESTED vs what the team
   actually DID (from the emoji reactions and notes), and draws takeaways.
4. Buzz opens a PULL REQUEST that adjusts the relevant principle,
   and posts a Slack message linking to it with a brief explanation.
5. A human does a ~60-second PR review and merges if it looks good.
```

Several design choices make this work:

- **Reuse existing behavior.** The team already monitors the channel and already uses emoji reactions to avoid stepping on each other's toes. The "breadcrumbs they leave for each other" become training signal for free.
- **Make it feel like a teammate.** Giving Buzz a name, a little personality, and a presence in Slack makes people interact with it more meaningfully and give better feedback. People engage more with agents that feel like teammates.
- **Skipped items are a feature.** Petra's favorite category is "skip," because it means the team does not even have to look at that mention. About 50 percent of a few thousand monthly mentions get skipped, saving huge amounts of time.

> ✅ **Route self-improvements through pull requests.** Because the skills live in a Git repo, Buzz's daily learning arrives as a pull request: a few English-line changes with context, reviewed in about a minute and merged if good. Crucially, Buzz "didn't just add a random rule at the end of a list. It looked at its own current instructions and adjusted them in the most appropriate way."

> 🔑 **Keep control to prevent drift.** Petra likes being able to quick-edit the proposed instruction wording. The PR gate exists precisely so the agent does not "change its instructions willy-nilly" and "drift into some weird direction that it keeps doubling down on."

---

## Part 5: the whole system, and why each piece needs the others

Buzz now runs largely on its own: a few thousand cloud agent runs per month, triggered on schedules and webhooks (via Warp's orchestration platform), handling triage, drafting, reporting, and even DMing Petra daily graphs of the team's action distribution.

The three pieces are not optional extras; they depend on each other.

| Piece | What it gives you | Why it is needed |
|---|---|---|
| **Principles** | Flexible instructions the agent can reason from. | The agent has to know *what to do* and handle new situations. |
| **Teaching it to learn** | The agent improves its own principles correctly (not by adding brittle rules). | The agent has to get better over time. |
| **The daily feedback loop** | A steady, low-effort stream of real signal from the team. | Without input, the agent has nothing to learn *from*. |

> 🎯 **The one thing to remember.** Petra's single takeaway: focus on **designing the feedback loop**, not on nailing the initial prompt. "That initial prompt can be just good. It doesn't need to be perfect." The loop is what lets the agent keep improving as situations change and your understanding of the problem evolves.

---

## Key takeaways

1. **Most agents die at "80 percent but not quite."** Closing that gap is the real challenge.
2. **The Ralph loop needs an external check.** Fuzzy, taste-driven tasks do not have one, so you need a different way to inject judgment.
3. **Use principles, not rules.** Principles generalize to new situations; rules are brittle and sound robotic. Switching often shrinks the file *and* improves output.
4. **Teach the agent how to learn.** Have it close the gap between its output and the ideal by adjusting its principles, not by adding one-off rules.
5. **Design the feedback loop for the humans.** Smallest team input for biggest agent output. Reuse behavior people already do (emoji reactions, Slack notes).
6. **Make it feel like a teammate.** A name and personality get people to give better feedback.
7. **Route self-improvement through pull requests** so humans stay in control and the agent does not drift.
8. **Focus on the loop, not the perfect prompt.** A "just good" prompt plus a great feedback loop beats a perfect prompt with no loop.

## Common pitfalls

- ❌ Trying to perfect the initial prompt instead of designing how the agent will improve over time.
- ❌ Writing instructions as if-X-then-Y rules (brittle, robotic, break on anything new).
- ❌ Letting the agent "learn" by appending hyper-specific rules to a list.
- ❌ Designing a feedback loop that asks humans to do extra, unusual work (they won't).
- ❌ Letting the agent rewrite its own instructions with no human review (drift).
- ❌ Assuming a coding-style external check exists for a fuzzy, taste-driven task.

---

## 🛠️ Capstone Project: build Echo

> This is the main hands on project for the lesson. You will build a teammate-style agent that triages a fuzzy stream of items, learns from your reactions, and proposes daily improvements to its own instructions through pull requests. Start small (a handful of items, one skill file) and grow it.

### What you will build

**Echo** is an agent that monitors a stream of items needing judgment, suggests an action with reasoning and a draft, posts those suggestions where your "team" already looks, learns from the actions actually taken, and opens a daily pull request that adjusts its *principles*.

> 🎯 **Pick a fuzzy domain.** Reuse social replies (triage mentions into reply/like/skip) to match the talk, or swap in another taste-driven stream: triaging **incoming emails** (reply / archive / flag), reviewing **community forum posts**, drafting **code-review comments**, or sorting **feature requests** (build / consider / decline). You need: a stream of items, a judgment call per item, and a way for a human to signal what they actually did.

### Why this is the perfect practice

| Lesson skill | Where you use it in Echo |
|---|---|
| Fuzzy vs external-check tasks | Milestone 1, you pick a task with no quick pass/fail |
| Principles, not rules | Milestone 2, write the instruction file as principles |
| Teaching the agent to learn | Milestone 4, the "learn from feedback" skill |
| Low-friction feedback loop | Milestone 5, learn from reactions, not extra chores |
| Feels like a teammate | Milestone 3, name and personality in the channel |
| PR-gated self-improvement | Milestone 6, daily PR a human reviews |

### Milestones (build them in order, each one works on its own)

1. **Pick a fuzzy task.** Choose a stream where success needs judgment and there is no quick unit test. Write one sentence on why a Ralph loop would not work here.
2. **Write principles, not rules.** Create one skill/instruction file that explains *how to think* about the task (purpose, tone, when to act, when to stay out), not a list of if-X-then-Y rules. Keep it short.
3. **Build the triage step.** Have Echo read each item and output: a suggested action, brief reasoning, and (where relevant) a draft. Post these somewhere a human already looks (a channel, a doc, a simple inbox). Give Echo a name and a touch of personality.
4. **Teach it to learn.** Write a second skill that, given Echo's output and an ideal output, makes Echo compare the two against its current principles, find the gap, and propose a *principle* change (not a one-off rule).
5. **Design the low-friction loop.** Let humans signal the action they actually took with the lightest possible input (an emoji reaction, a one-word tag, a short note). Echo collects the difference between what it suggested and what was done.
6. **PR-gated self-improvement.** Keep the instruction files in a Git repo. On a schedule (say daily), have Echo read the signals, adjust the relevant principle in place, and open a pull request with a brief explanation. A human reviews and merges. Confirm Echo edits the *right* place, not just appends to the end.
7. **Stretch goals.** Add a scheduled/triggered run so Echo operates on its own. Add a daily summary (counts of suggested vs taken actions). Add a guardrail so Echo cannot make too large a change in one PR, preventing drift.

### How you will know you are done

- ✅ Echo's instructions are principles (how to think), not a checklist of rules.
- ✅ Echo triages items with a suggested action, reasoning, and (where relevant) a draft, posted where a human already looks.
- ✅ Giving feedback costs the human almost nothing (a reaction or one-word tag).
- ✅ When Echo learns, it edits a *principle* in the right place, not a brittle rule appended to a list.
- ✅ Self-improvements arrive as pull requests a human reviews and merges in about a minute.
- ✅ The system keeps getting better over several rounds without you re-prompting it from scratch.

> 💡 **Keep yourself honest:** if a single piece of feedback causes Echo to add a hyper-specific rule, your "learn how to learn" skill is not working yet. The change should be a generalizable principle.

---

## Practice exercises (optional extra reps)

> **What these are:** five small, self contained tasks, each focused on one skill. They are optional and independent. The **Capstone above is the main build** and already covers all of these.

### Exercise 1: spot the fuzzy task (foundational)
List five tasks you might want an agent to do. For each, mark whether it has a quick external check (good for a Ralph loop) or needs judgment and taste. Explain one of each.

### Exercise 2: rules to principles (foundational)
Take a rule-heavy agent instruction ("if X then Y" lines) and rewrite it as principles that explain how to think. Note how much shorter it gets and which new situations it now handles.

### Exercise 3: turn feedback into a principle (intermediate)
Write a piece of specific feedback ("don't mention pricing here"). Then write the *generalizable principle* it should become ("don't pitch features to someone who is venting"). Do this for three examples.

### Exercise 4: design the lightest loop (intermediate)
For a task you care about, design the lowest-friction way for a human to signal what they actually did, reusing something they already do. Justify why the team would actually keep doing it.

### Exercise 5: PR-gated learning (advanced)
Build a small flow where an agent reads a few feedback signals, edits an instruction file in the right place, and opens a pull request with an explanation. Add a guardrail that limits how big a single change can be.

---

## Cheat sheet

```text
CLOSING THE GAP TO PRODUCTION (fuzzy, taste-driven tasks)

WHEN A RALPH LOOP WON'T WORK
  No quick external check (no unit test / browser) -> you must inject
  judgment another way. That way is: principles + learning + a feedback loop.

THE THREE PIECES (each needs the others)
  1. PRINCIPLES, not rules
     - Tell the agent HOW TO THINK, not if-X-then-Y.
     - Generalizes to new situations; often shrinks the file AND improves output.
  2. TEACH IT TO LEARN
     - Compare output vs ideal vs current instructions; find the gap;
       adjust a PRINCIPLE, never append a brittle one-off rule.
  3. THE DAILY FEEDBACK LOOP
     - Smallest team input for biggest agent output.
     - Reuse what people already do (emoji reactions, notes).
     - Make it feel like a teammate (name + personality).
     - Self-improvements arrive as PULL REQUESTS a human reviews (control,
       no drift).

THE ONE THING TO REMEMBER
  Design the FEEDBACK LOOP, not the perfect prompt.
  A "just good" prompt + a great loop beats a perfect prompt + no loop.
```

## How this connects to the rest of the course

- **Earlier, Module 6 · Lesson 21 (AirOps chases friction):** AirOps named self-improvement and feedback loops as their next frontier; this lesson shows one in production.
- **Earlier, Module 6 · Lesson 22 (Metaview self-improving prompts):** the same "watch human decisions, update your own instructions" pattern, in a different domain.
- **Earlier, Module 2 · Lesson 3 (The Prompting Playbook):** principles over brittle rules, and evals as the way to tell whether a change helped.
- **Next, Module 5 (Claude Managed Agents):** running agents on schedules and triggers in the cloud, the infrastructure behind Buzz's daily runs.

---

*Source: "Teaching agents to learn from your team" by Petra (Warp), Code with Claude 2026, London. The talk was a story and live screenshots, so the loop diagram and any code are illustrative reconstructions of the approaches described. Adapt model names and SDK details to the current versions.*

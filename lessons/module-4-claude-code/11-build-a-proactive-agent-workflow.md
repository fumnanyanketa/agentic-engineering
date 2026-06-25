# Module 4 · Lesson 11: Build a Proactive Agent Workflow with Claude Code

> **Course:** Building with Claude, a self-paced course
> **Module 4:** Claude Code, your everyday agent
> **Speaker:** Maya, Applied AI team, Anthropic
> **Source talk:** [Build a proactive agent workflow with Claude Code](https://www.youtube.com/watch?v=eSP7PLTXNy8) · [full transcript](../../transcripts/code-with-claude-2026-london-2026/19_build-a-proactive-agent-workflow-with-claude-code.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

A **routine** turns Claude Code from a tool that waits for you to press enter into a teammate that starts work on its own, by letting you define just four things (a prompt, the repos, the connectors, and a trigger) and letting Claude Code's managed cloud handle all the hosting, scheduling, and session plumbing for you.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you build a **Routine Pack**: a small set of proactive routines that watch over a project of yours (docs, deploys, and a backlog) so you can see the same idea applied three different ways. Everything before the Capstone teaches the three decisions you will make for each routine. If you want to see the finish line first, jump to the **"Capstone Project"** section near the end, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[Building Effective Agents (Anthropic)](https://www.anthropic.com/engineering/building-effective-agents)** (essay). The seminal, tool-agnostic taxonomy of agentic patterns, including the evaluator-optimizer loop, behind routines and the "tool to teammate" shift.

## A few plain-language basics first

This lesson uses some everyday agent terms. Here they are in simple words:

- **Agent:** an AI that takes a series of actions on its own toward a goal, instead of answering once. Claude Code is an agent.
- **Reactive vs proactive.** A **reactive** agent waits for you to type a prompt and press enter. A **proactive** agent notices something happen and starts work by itself. This whole lesson is about making the leap from reactive to proactive.
- **Routine:** the feature this lesson is about. A routine is a saved automation that launches a Claude Code session on its own when a trigger fires. You access it in Claude Code with the `/schedule` command.
- **Trigger:** the event or schedule that kicks a routine off. Either time based (every Monday at 10am) or event based (a GitHub issue was opened).
- **Connector:** a link that gives Claude access to an outside service, such as Slack, Google Drive, or GitHub.
- **Cron:** the classic Unix way to schedule a script to run on a timer. Setting one up by hand means building and maintaining your own servers, which is the pain routines remove.
- **Headless session:** a Claude Code session running with no screen attached (for example on a server), so you cannot watch it live. Routines are not like this: you **can** watch and steer them.
- **Webhook / endpoint:** a web address you can send a message (a "post request") to in order to kick something off. Routines can be triggered by posting to a webhook with an event payload (the data describing what happened).
- **PR (pull request):** a proposed code change submitted for review.

You do not need to memorise these. Every term is also explained again the first time it appears below.

## Why this lesson matters

Maya's framing is simple and sticky: today Claude Code is a powerful coding **tool**, but the goal is to make it a coding **teammate**.

> "A teammate notices when something breaks and does something about it." (Maya)

A tool waits for you to enter a prompt and press enter. A teammate sees a problem, like a deploy that looks unhealthy or docs that have fallen behind, and acts. The trouble is that building proactive agents by hand has always meant building a lot of unglamorous infrastructure. Maya opens by asking the room who has run Claude Code on a cron, then asks them to keep their hands up if they enjoyed building and maintaining that infrastructure. Almost every hand goes down. Routines exist so you never have to build that plumbing again.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain the three pain points of building proactive agents by hand (where to run them, when to trigger them, and how to stay in or out of the loop) and how routines solve each.
2. Create a routine from inside Claude Code using `/schedule`.
3. Make the **three core decisions** every routine needs: trigger, context, and steerability.
4. Choose between a **time based** trigger and an **event based** trigger (including GitHub events and custom webhooks).
5. Apply the **generator and critiquer** pattern (one routine reviews another's work) and other quality safeguards.

## Prerequisites

- You have used Claude Code at least a little: you can start a session and run a slash command.
- Helpful but optional: Module 4 · Lesson 10 (Beyond the Basics), which introduces the asynchrony and parallelism ideas that routines build on.
- A GitHub repo you can experiment with, and access to at least one connector (Slack, Google Drive, or GitHub) makes the exercises concrete.

---

## Part 1: why proactive agents are hard to build by hand

We all know you **can** build a proactive agent today. Maya's point is that it is "a little bit cumbersome." She breaks the pain into three problems, and these three map exactly onto the three things routines fix.

| Problem | Why it hurts when you do it yourself | What routines do |
|---|---|---|
| **Where should the agent run?** | Not on your laptop. Close the lid or let it die, and the session is gone. So you have to manage hosting, data persistence (saving state between runs), and authentication (proving who you are to each service). That is a whole infra stack outside your prompts. | Routines run on Claude Code's **managed infrastructure**. Hosting, session state, and connectors are handled for you. Nothing depends on your laptop being open. |
| **When should it kick off?** | You build on top of cron, or stand up endpoints to post to. Either way, more infra to build and maintain. | Routines give you **customizable triggers** out of the box: time based, native GitHub events, and your own custom webhooks. |
| **In the loop or out of the loop?** | A **headless** session (one with no screen) is hard to watch in real time. There is no clean way to watch, steer, bound, or resume it. | Every routine is a real Claude Code session you can **open, watch, follow up on, steer, and resume** from web, CLI, and desktop. |

> 🔑 **The core idea.** A routine lets you define only four things: the **prompt**, the **repos** to connect, the **connectors** it can use, and the **trigger**. Claude Code handles the rest. You concentrate on your domain expertise, not on plumbing.

### The three design goals behind routines

Maya names the three things the team optimized for, which line up with the three problems above:

1. **Always available.** Routines run on managed infrastructure, so they do not depend on your laptop.
2. **Proactive with customizable triggers.** Time based schedules, native GitHub events, or your own custom events posted to a webhook with the event payload as context.
3. **Interactive and steerable.** A routine is "really just a Claude Code session under the hood," so you keep all the control you would have in the terminal.

> 💡 The deepest shift here is mental, not technical. You stop thinking "what command should I type?" and start thinking "what should happen automatically, and when?" That is the move from tool to teammate.

---

## Part 2: a real example, automating documentation

Maya grounds everything in a real Anthropic story. Weekly pull requests for Claude Code went up **200 percent** since the start of the year. Wonderful for the engineering team and for users who get features fast. Painful for exactly one person: the engineer responsible for keeping the documentation in sync. Her name is Sarah, and she became an early routines adopter.

The question: **how do you automate docs creation with routines?**

### Creating a routine with /schedule

Inside the Claude Code terminal, Sarah typed `/schedule` and described what she wanted in plain English:

```text
/schedule

Once a week, please review all the new changes merged to main against our
documentation repo, and create a PR to update docs if you see any changes.
```

Claude does not just silently obey. It asks clarifying questions, such as what time each week to run, and whether to notify her (for example, ping her on Slack) when it opens a PR. Once she answers, Claude creates the routine.

> 💡 Maya's prompt to the audience is worth pausing on: "What are some tasks that you do every day that would help if they could run on a schedule, or if Claude Code could actually initiate these sessions for you?" Keep a running list as you read.

### The three decisions every routine needs

Whatever the routine, Maya says you make the same three decisions. These are the heart of the lesson.

```text
1. TRIGGER       -> When should this run? (a schedule, or an event)
2. CONTEXT       -> What does Claude need to succeed? (repos, docs, connectors)
3. STEERABILITY  -> How do you keep Claude honest and verify the output?
```

#### Decision 1: the trigger

There are two kinds.

- **Time based (schedule).** Runs on a cadence. The docs example uses this: a weekly review of the difference between the source code and the docs repo.
- **Event based.** Reacts to something happening. Routines support **native GitHub events** and **custom events** you post to a webhook. Examples Maya gives:
  - Every time a release is cut, diff the release branch against the docs and open PRs for any new features.
  - Let engineers tag a PR with a `needs docs` label, and kick off a routine whenever a labeled PR merges.

#### Decision 2: the context

> 🔑 **Whatever context Claude has is the ceiling of how successful it can be.** (paraphrasing Maya) Decide carefully what to give it.

For the docs routine, Claude needs:

- **One or more code repos.** Here, both the Claude Code source repo (to find new changes) and the docs repo (to open PRs).
- **Additional context, via connectors.** For example, the marketing briefs in **Google Drive**, so Claude matches existing language and tone. Hook up the **Drive connector**.
- **Action connectors.** If Claude should ping you when it opens a PR, give it the **Slack connector**.

#### Decision 3: steerability (keeping Claude honest)

This is how you ensure quality. Maya offers several techniques:

- **Agent on agent review (the generator and critiquer pattern).** This is a multi agent idea: one agent generates work, another critiques it. In routine terms, set up one routine to create docs PRs, and a second routine that triggers on that PR's creation to leave review comments **before a human even looks**.
- **Human in the loop steering.** Even though "human out of the loop" is nice, sometimes you want to nudge. Open Claude Code on the web, watch a **live session** as if you were in the terminal, ask it questions mid session, push it in another direction, or resume a past session and continue the conversation.
- **Verify the output.** The obvious final step. For docs, that means actually rendering the changed documentation page and confirming it looks right.

> 💡 The generator and critiquer pattern is the part most people miss. A routine that reviews another routine's PR gives you a second set of (automated) eyes for free, catching issues before they reach a human reviewer.

---

## Part 3: the two triggers in practice (the demo)

Maya shows both trigger types live.

### Example A: a scheduled docs sync

In Claude.ai, she opens the **Code** section in the left panel, then **Routines**, and clicks the routine created earlier. The routine shows:

- **Connected to two repositories:** a mocked up Claude Code source repo and the docs repo.
- **Schedule:** every Monday at 10:00 am.
- **Connectors:** GitHub and Slack.
- **Instructions:** generated by Claude from her original prompt plus her answers to the clarifying questions, describing a "weekly documentation sync."

Clicking into a session shows the flow: Claude reads its instructions, looks at the source repo for recently merged PRs, checks the change log, compares against the docs repo, finds changes, and opens a PR.

### Example B: an event triggered docs gap finder

The second routine triggers on a **GitHub event** instead of a clock.

```text
Instructions (paraphrased):
  Investigate the issue this session triggers on. Decide whether it points to a
  documentation gap. If it does, open a PR and ping me in this channel.
```

Setting up the trigger: within event based triggers, routines support native GitHub events as well as custom triggers via a posted request. Maya picks **GitHub event -> issue opened** on the docs repo, connects **Slack** (to ping her on a new PR) and the **GitHub MCP** (a connector that lets Claude work with GitHub).

To test it, she opens a new GitHub issue noting that a few tools are missing from the docs. She refreshes, sees a new run get picked up, and confirms the issue's content was passed into the session as **additional context**. Because she already has a PR open for that gap, she demonstrates **steering in real time**: she simply tells the running Claude to stop the session.

> 🔑 **Two patterns, one feature.** Example A shows a **schedule** ("every Monday"). Example B shows an **event** ("when an issue opens") plus **live steering** ("actually, stop, I already handled this"). Same routine machinery, very different shapes of work.

> ✅ **Best practice: the issue payload becomes context.** When an event triggers a routine, the data about that event (here, the issue text) flows into the session automatically. You do not have to copy paste it. That is what makes event based routines feel like a teammate reacting to a real thing.

---

## Part 4: applying routines to your own work

Maya closes by turning common engineering chores into routines, always using the same three decisions (trigger, context, steerability). The headline example is a **deploy verifier**.

### Worked example: the deploy verifier

The situation: you just deployed a change to a service and want to confirm it is healthy before deciding whether to roll back.

| Decision | Choice for the deploy verifier |
|---|---|
| **Trigger** | Your CD pipeline (the system that deploys code) can **post to a webhook** after every deploy. That post kicks off the routine. |
| **Context** | The **source code** for the service just deployed; **monitoring tools** like Datadog or Grafana (services that show whether your system is healthy); and an **alert channel** so Claude can ping you, for example Slack, email, or even a text via Twilio. |
| **Steerability** | Start by having Claude run an investigation and give you a **go or no go** recommendation on rolling back. Read its analysis on the web. Work with it to roll back if needed. Over time, as you trust it, let Claude roll back the change itself based on the monitoring data. |

> 💡 **Trust grows in stages.** Notice the steerability path: first Claude only **recommends**, then it helps you **act**, and eventually (once you trust it) it **acts on its own**. You do not have to hand over the keys on day one.

### More routine ideas

- **On call investigator.** When an alert fires, a routine pulls logs and dashboards and drafts an initial diagnosis.
- **Backlog triager (for a PM).** A weekly time based routine reads through all your issues (GitHub issues, a Slack channel, wherever they live), prioritizes them, and maybe opens PRs for the most important ones. Give it access to GitHub and Slack.

### The takeaways

> 🎯 **Maya's final points:**
> - **Proactive agents beat reactive agents.** Move from an agent waiting for you to press enter, to one that reacts to problems and opens a PR itself.
> - **Routines remove the infra burden** so you can focus on your domain and process expertise.
> - **Get started today.** You are a single `/schedule` command away from your first routine.

---

## Key takeaways

1. **Tool to teammate.** A reactive agent waits for enter. A proactive agent notices and acts. Routines make that leap.
2. **Routines remove three pains:** where to run (managed infra), when to trigger (built in triggers), and how to stay in or out of the loop (a real, steerable session).
3. **Define four things, Claude Code does the rest:** prompt, repos, connectors, trigger.
4. **Every routine needs three decisions:** trigger, context, steerability.
5. **Two trigger types:** time based (a schedule) and event based (GitHub events or a custom webhook, with the event payload flowing in as context).
6. **Context is the ceiling.** Give a routine the repos, docs, and connectors it needs, or it cannot succeed.
7. **Keep it honest** with agent on agent review (generator and critiquer), live steering, and verifying the output.

## Common pitfalls

- ❌ Building cron jobs and hosting by hand when a routine would handle all of it.
- ❌ Starting a routine on your laptop, then losing the session when the laptop sleeps or dies.
- ❌ Giving a routine too little context (no docs repo, no monitoring access) and wondering why its output is weak.
- ❌ Treating a routine as fire and forget with no verification step.
- ❌ Letting an agent take destructive action (like rolling back) on day one, before you have watched it enough to trust it.
- ❌ Forgetting that an event trigger's payload is already available as context, and copy pasting it in by hand.

---

## 🛠️ Capstone Project: Routine Pack

> This is the main hands on project for the lesson, and the best way to make everything above stick. You will build a small **pack of three routines** that watch over one project of yours, so you practice the three decisions (trigger, context, steerability) on three different shapes of work. Start with one routine and grow from there.

### What you will build

**Routine Pack** is a set of proactive routines that turn a repo you own into something Claude Code looks after on its own:

1. A **scheduled docs sync** (time based trigger).
2. A **deploy or health verifier** (event based, webhook trigger).
3. A **reviewer routine** that critiques the first routine's PRs (the generator and critiquer pattern).

> 🎯 **Pick your world.** Use a real repo you maintain, or a small sample project. It just needs a code repo, somewhere documentation lives, and one connector you can wire up (Slack is the easiest for notifications, GitHub for issues and PRs).

### Why this is the perfect practice

| Lesson skill | Where you use it in Routine Pack |
|---|---|
| Creating a routine with `/schedule` | Milestone 1, your first routine |
| Decision 1: triggers (time based) | Milestone 2, the scheduled docs sync |
| Decision 1: triggers (event based / webhook) | Milestone 3, the verifier |
| Decision 2: context (repos + connectors) | Milestones 2 to 3, choosing what each routine can see |
| Decision 3: steerability (live steering) | Milestone 4, watching and nudging a session |
| Generator and critiquer pattern | Milestone 5, the reviewer routine |
| Verifying outputs | Milestone 6, the rendering / confirmation step |

### Milestones (build them in order, each one works on its own)

1. **First routine.** From the Claude Code terminal, run `/schedule` and describe a simple weekly task in plain English. Answer Claude's clarifying questions and let it create the routine. View it in the Routines tab.
2. **Scheduled docs sync (time based).** Build a routine that, once a week, compares recent merges to main against your docs and opens a PR if docs are out of date. Connect both the source repo and the docs location, plus Slack to notify you. Confirm the schedule and connectors in the routine view.
3. **Health verifier (event based).** Build a routine triggered by a webhook (or a GitHub event if you do not have a deploy pipeline). Give it the service source code, a monitoring connector if you have one, and an alert channel. Have it produce a clear **go or no go** recommendation rather than acting, for now.
4. **Steer a live session.** Trigger one routine, open its session on the web, and practice steering: ask it a question mid run, push it in a new direction, then stop it. Then resume a past session and continue the conversation.
5. **Reviewer routine (generator and critiquer).** Add a second routine that triggers on the first routine's PR creation and leaves review comments before a human looks. This is your automated second set of eyes.
6. **Verify the output.** Add an explicit verification step (for docs, render the changed page; for the verifier, confirm the recommendation matches the monitoring data) and confirm the result is what you expect.
7. **Stretch goals.** Add a `needs docs` label trigger. Add a backlog triager that runs weekly across GitHub issues and Slack. Graduate the verifier from "recommend only" to "act on its own" once you trust it.

### How you will know you are done

- ✅ You have **at least one time based and one event based** routine running.
- ✅ For each routine you can state its **trigger, context, and steerability** choices.
- ✅ You have **steered a live session** (asked a question, redirected it, or stopped it).
- ✅ Your **reviewer routine** leaves comments on the first routine's PRs automatically.
- ✅ Every routine has a **verification step**, and you have confirmed at least one output by hand.

> 💡 **Keep yourself honest:** before building any routine, write its three decisions down first (trigger, context, steerability). If you cannot fill in all three, you are not ready to build it yet.

---

## Practice exercises (optional extra reps)

> **What these are:** five small, self contained tasks, each targeting one skill. They are optional and independent. The **Capstone Project above is the main build** and already includes all of these skills, so feel free to skip straight to it.

### Exercise 1: list your proactive tasks (foundational)
Spend ten minutes listing tasks you do that "do not need you in the loop, they just need to run in a loop." For each, jot whether it is naturally **time based** or **event based**.

### Exercise 2: write the three decisions (foundational)
Pick one task from Exercise 1 and write out its **trigger, context, and steerability** before touching Claude Code. This is the planning habit the whole lesson rests on.

### Exercise 3: build a scheduled routine (intermediate)
Use `/schedule` to create a simple time based routine (for example, a weekly summary of merged PRs). Answer the clarifying questions and confirm it appears in the Routines tab with the right schedule and connectors.

### Exercise 4: build an event triggered routine (intermediate)
Create a routine that triggers on a GitHub issue being opened. Open a test issue and confirm the issue text arrives in the session as context, then steer the session (for example, tell it to stop).

### Exercise 5: generator and critiquer (advanced)
Set up two routines: one that opens a PR, and one that triggers on that PR's creation and leaves review comments. Confirm the second routine comments before you, the human, do anything.

---

## Cheat sheet

```text
TOOL  ->  TEAMMATE
  Reactive: waits for you to press enter.
  Proactive: notices something and acts.  (routines)

A ROUTINE = define 4 things, Claude Code does the rest
  1. Prompt        what to do
  2. Repos         which code it works with
  3. Connectors    Slack, Drive, GitHub, monitoring, ...
  4. Trigger       when it runs

THREE DECISIONS FOR EVERY ROUTINE
  TRIGGER       time-based (schedule)  OR  event-based (GitHub event / webhook)
  CONTEXT       repos + docs + connectors  (this is the ceiling on success)
  STEERABILITY  generator+critiquer review | watch & nudge live | verify output

GET STARTED
  /schedule   then describe the task in plain English; answer the questions.

TRUST LADDER (for risky actions like rollback)
  recommend only  ->  help you act  ->  act on its own
```

## How this connects to the rest of the course

- **Earlier, Module 4 · Lesson 10 (Beyond the Basics):** introduces asynchrony and parallelism, and mentions `/loop`. Routines are the managed, remote version of that proactive idea.
- **Next, Module 4 · Lesson 12 (Stop Babysitting Your Agents):** shows how to make Claude verify its own work so routines can run with high reliability, and connects `/loop` (local) with routines (remote).
- **Earlier, Module 2 (Core skills):** prompting and context skills that determine how well your routine's instructions and context perform.

---

*Source: "Build a proactive agent workflow with Claude Code" by Maya (Anthropic), Code with Claude 2026, London. Command examples and instruction text are illustrative reconstructions of what the talk demonstrated. Adapt the exact commands and connector names to the current version of Claude Code.*

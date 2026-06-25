# Module 4 · Lesson 8: What's New in Claude Code

> **Course:** Building with Claude, a self-paced course
> **Module 4:** Claude Code, your everyday agent
> **Speaker:** Ralf, Technical Staff, Anthropic
> **Source talk:** [What's new in Claude Code](https://www.youtube.com/watch?v=sRvUXLquiRg) · [full transcript](../../transcripts/code-with-claude-2026-london-2026/24_whats-new-in-claude-code.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

Claude Code has grown from a terminal chat tool into an everyday agent you can run from your phone, leave alone for long stretches, point at many tasks at once, and trigger automatically from events like a new pull request, and this lesson tours the features that make all of that possible and shows you which to turn on first.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you set up a **Hands-Off Workbench**: a real project wired so Claude can run remotely, review every change, and react to GitHub events without you babysitting it. Everything before the Capstone explains one feature you will switch on there. To see the finish line first, jump to **"Capstone Project: the Hands-Off Workbench"**, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[Raising the bar on SWE-bench Verified (Anthropic)](https://www.anthropic.com/research/swe-bench-sonnet)** (essay). A first-principles look at how a coding agent is actually built (model + bash tool + edit tool + an iterative loop), independent of any specific feature set.
> - **[Building Effective Agents (Anthropic)](https://www.anthropic.com/engineering/building-effective-agents)** (essay). The durable workflow-vs-agent distinction behind what "agentic coding tool" even means.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Claude Code:** Anthropic's coding agent. You give it a task in plain English and it reads, writes, and runs code for you. It started life in the terminal but now also has a desktop app and a web/mobile experience.
- **CLI (Command Line Interface):** a program you drive by typing commands into a terminal (the black text window). Claude Code began as a CLI.
- **Terminal:** the text window where you type commands. Its **scroll back** is the history of everything printed in it.
- **Agent:** an AI that takes a series of actions on its own toward a goal, rather than answering in one shot. A **session** is one running conversation with the agent.
- **Token:** the unit the model reads and writes in. You are billed per token, so a wasteful agent costs more.
- **Repo (repository):** a project's folder of code tracked by **Git**, a system that records every change. **GitHub** is a popular website for hosting repos.
- **PR (Pull Request):** a proposed set of code changes on GitHub that others (or an agent) review before it is merged in.
- **Webhook:** an automatic message one system sends another when something happens (for example, GitHub pinging your tool when a new issue is opened).
- **Context:** everything the model currently has loaded in its working memory. Loading too much "bloats" the context and wastes tokens.

You do not need to memorise these. Each is explained again the first time it appears below.

## Why this lesson matters

The pace is the point. As Ralf jokes, the changelog "sometimes looks more like a news feed." If you only know Claude Code as "the thing in my terminal," you are missing most of what it can now do. The features here fall into two themes, and both change how you work:

1. **Developer experience:** making the tool pleasant to use every day (running it from your phone, no more flickering, a better desktop app).
2. **Autonomy:** letting Claude do more without stopping to ask you, so you can dispatch work and walk away.

Underneath the autonomy features is one recurring frustration Ralf names directly: you start a long task, walk off, and come back to find Claude stuck on a trivial permission prompt it could have answered itself. Most of this lesson is about closing that gap.

## Learning objectives

By the end of this lesson you will be able to:

1. Start a Claude Code session on your computer and **continue it from your phone or a browser** with remote control.
2. Turn on the **full-screen TUI** for a flicker-free, clickable terminal experience.
3. Use **auto mode** to let Claude proceed safely without constant permission prompts.
4. Run several Claudes at once safely with **work trees**, and keep track of them with **agent view**.
5. Let Claude remember project facts across sessions with **auto memory**.
6. Automate code review (**ultra-review**) and trigger Claude from events with **routines**.

## Prerequisites

- A working install of Claude Code and a basic session under your belt (you have given it one task and watched it work).
- A GitHub account and one repo you can experiment in (needed for code review and routines).

---

## Part 1: developer experience

### 1.1 Remote control (run a session from anywhere)

**Remote control** lets you start a session on your computer and then pick it up from the Claude.ai website, the Claude mobile app, or any browser on any device. You dispatch a task, then go walk the dog or grab a coffee, and your phone notifies you whenever Claude needs input.

Turning it on is a single command inside a session:

```text
/remote-control
```

Press enter and the session becomes live on the web and on your phone. From there you keep chatting back and forth, and crucially, all your tooling and dev environment on your computer stays accessible from both the web UI and the mobile app. You are not running a cut-down version; you are reaching into the real session.

> 💡 **Name your sessions.** If you run `/remote-control` with no extra text, Claude will look at what you are doing and name the session for you (for example "London rain jokes"), so it is easy to find on your phone later.

> ✅ **Pro tip from the Anthropic team:** set remote control to be **always on** in your settings file, so every session is reachable from your phone automatically. As Ralf puts it, "you never know when your puppy needs to go for a new walk or when nature calls."

### 1.2 The flicker-free full-screen TUI

If you have run long sessions in the terminal, you have seen the screen flicker. Here is why: every time Claude printed something new, the terminal sometimes had to repaint its whole **scroll back** (its entire printed history), which causes the flicker.

The fix is a new full-screen mode. A **TUI** (Terminal User Interface) is a full-screen, app-like interface drawn inside your terminal. In this mode, Claude Code *is* the terminal. It **virtualizes** the scroll back, meaning it only draws the part of the screen you are actually looking at, not the whole history.

```text
/tui full-screen
```

Two payoffs:

- **Flat memory and no flicker**, even in very long sessions, because only the visible part is rendered.
- **Clickable elements.** Because the interface is virtualized, it can show buttons. You can click to expand a long file Claude wrote, or click a "jump to bottom" control that lights up when a new message arrives.

> 💡 You can make full-screen the default so every new session starts this way. The Anthropic team mostly works this way themselves.

### 1.3 The refreshed desktop app

The **desktop app** got a full UI overhaul. Ralf is candid that earlier versions did not win people over (many preferred the CLI), but invites a second look. He does not expect it to replace the CLI for an eight-hour coding day, but for specific tasks it is now better. Highlights:

- **Sessions grouped by project,** so when you run many sessions in parallel you can see which belongs to which repo.
- **Plan view.** If a session began with a plan (a step-by-step implementation outline), you can read that plan easily, and **leave comments on any part of it** that you do not like. Your comment is pushed back to Claude to fix.
- **Diff and file review.** You can see the **diffs** (the exact lines changed) for a PR, and comment on a specific line, for example "explain this line," and Claude will explain just that piece of code. You can also browse the full files of a project.
- **GitHub integration** built in, so you can push fixes straight from the app.

> 🔑 **The CLI is not going away.** The takeaway is not "switch to the desktop app." It is "use the right surface for the task." Plan review and diff commenting are genuinely nicer with a mouse and a real UI.

---

## Part 2: autonomy (let Claude run without babysitting)

Every feature here exists to solve one problem: Claude stopping a long-running task to ask you something it could have handled itself. As models get more capable, Claude is better at judging when it actually needs you.

### 2.1 Auto mode

**Auto mode** is a new permission mode for exactly the case where you set a task running, expect it to take a while, and do not want to be interrupted by "can I read this file?" prompts.

Here is how it stays safe. Every time Claude would normally stop and ask permission, auto mode instead runs a **classifier** (a quick check) that asks two questions:

```text
1. Is this action DESTRUCTIVE? (Will I regret this later? e.g. deleting data)
2. Does this look like a PROMPT INJECTION? (Is something trying to hijack me?)
```

(A **prompt injection** is when malicious text, say in a file or web page, tries to trick the agent into doing something it should not.)

The decision flow:

```text
Both checks pass  -> Claude takes the action on your behalf and keeps going.
A check fails     -> Claude first tries to find a safe workaround (a path that
                     avoids the risky action).
No safe path      -> only THEN does Claude stop and ask your permission.
```

> 🔑 **Auto mode earns your time back.** It does not blindly say yes to everything. It says yes to the safe, boring things and only interrupts you for the things that genuinely warrant a human. This is what makes "dispatch and walk away" practical.

### 2.2 Work trees (many Claudes, no collisions)

A **work tree** is a copy of your project in a separate subdirectory that only one Claude session touches. Work trees are a Git feature that existed long before Claude Code, but managing them by hand was fiddly: you had to juggle directories, and they are often **ephemeral** (temporary, created and thrown away as you work).

Now Claude Code supports them natively. When you want several Claudes working on the same repo in parallel without stepping on each other's files:

```text
claude --worktree
```

This copies the repo into a segregated directory so that session works independently. You can also just ask Claude, mid-session, to create a work tree for you. Other surfaces (the desktop app and agent view) treat work trees as native too, offering a flag to start a session in a fresh work tree automatically.

> 💡 If you are a "parallel Claude" user (several sessions going at once), work trees are essential. Without them, two sessions editing the same files will collide.

### 2.3 Auto memory

Do you feel like every new session starts from a blank slate, and you re-explain the same things? **Auto memory** fixes that. As a session runs, Claude quietly takes notes on things worth remembering: your coding style, architectural choices, debugging insights, the little tricks only you know. It saves them to a `memory.md` file and loads them into every future session.

It does not rewrite the file every session. It has "the discerning capabilities" to decide when something is genuinely worth remembering.

> 🔑 **CLAUDE.md vs memory.md (the key distinction).** Think of `CLAUDE.md` as the **onboarding manual** you hand Claude on day one (you write it, by hand). Think of `memory.md` as the **notes Claude takes while doing the work** (it writes it, automatically). One is a manual; the other is note-taking.

Three design details worth knowing:

- **It stays small.** `memory.md` is mostly an **index** pointing to other memory files. Thanks to **progressive discovery**, Claude loads only the specific memory it needs (say, the debugging notes) when it needs it, instead of dumping everything into context and bloating it.
- **It is shared across the project.** Every session and every work tree in that project uses the same memory.
- **It stays on your machine.** Memory files are not pushed to GitHub or the cloud. To audit them, run `/memory` and you can see the whole directory.

### 2.4 Agent view

If you run many sessions at once, **agent view** gives you one window to manage them all. It also runs your sessions **in the background**, so you can leave Claude Code and they keep going.

```text
claude agents
```

From here you can:

- See every session grouped by **status:** working, completed, or waiting for your input.
- Press **enter** to jump into any session.
- Press **space** to send a prompt to a session without fully entering it (a quick poke, like "how many appointments today?").

Agent view is in **public preview**. It pairs naturally with work trees: many parallel sessions, each isolated, all visible at a glance.

---

## Part 3: automation (Claude reacting to events)

### 3.1 Code review and ultra-review

**Code review** is an automated review that runs on every PR you create. The team built it for themselves, saw it work, and baked it into the product. Two things make it powerful:

- **Multi-agent:** each PR spins up a team of agents, each checking a different concern (errors, bugs, security vulnerabilities, logical mistakes).
- **Multi-phase:** a *second* phase checks every finding from those agents against your actual code, to confirm the finding is real and not a false alarm.

The result: logical problems that might take you hours to find surface in minutes.

```text
# In your terminal, kick off a review manually:
/ultra-review
```

It is also native to the **GitHub app**: install Claude on your repo and every new PR is reviewed automatically. (And yes, the command is `ultra-review`, not super-review or great-review.)

### 3.2 Routines (trigger Claude from events or a schedule)

**Routines** let Claude run sessions without you manually triggering them. A routine is a workflow that fires on:

- a **schedule** (for example, every day at 8am and 4pm),
- a **webhook** (for example, a new GitHub issue or PR), or
- an **API call** from another system (for example, your e-commerce store on every sale).

A routine has the same capabilities as a normal Claude Code session, so it can make `curl` requests (fetch data over the web), use connectors, and so on. Crucially, routines **run in the cloud**, so your computer does not even need to be on.

A worked example from the talk: create a routine on a repo, set the trigger to "issue opened," give it an instruction ("assess the issue and give me your review, and do it sounding like a medieval knight"). Now every time someone opens an issue, the webhook fires, the routine runs, and Claude posts its review on the issue. A second routine reviews every new PR. Nobody tags anything; the GitHub webhook does all the work.

```text
# The shape of a routine (conceptual):
Trigger:  GitHub event "issue opened"  (or a timer, or an API call)
Repo:     your-org/your-repo
Action:   "Assess the issue and post a review."
Runs:     in the cloud, no local machine needed
```

Routines are in **research preview**.

> 🔑 **This is asynchronous work.** Between routines, agent view's background sessions, and remote control, the model of working shifts: you stop sitting and watching a session, and instead dispatch work that runs on its own and reports back. As Ralf summarises, "let the clouds do your work for you and just come back and assess what is going on."

---

## Part 4: staying current (and enterprise extras)

Because the changelog moves so fast, Ralf points to where to keep up:

- The **"What's new" section** in the documentation, which summarises what matters.
- The **changelog** itself.
- The **Claude dev team on social media**, and the newsletter.

For people managing teams or enterprise deployments, recent additions include: better Windows support, setup wizards for deploying Claude on Google Cloud Platform and AWS, and **native binaries** so you can install straight from a governance pipeline.

> 💡 Ralf's closing note is worth keeping: with this pace, the real skill is to "never stop learning." Treat the changelog as a habit, not a one-off read.

---

## Key takeaways

1. **Remote control** turns any session into something you can drive from your phone. Consider making it always-on.
2. **Full-screen TUI** kills flicker, keeps memory flat in long sessions, and adds clickable elements.
3. The **desktop app** is worth a second look for plan review, diff commenting, and GitHub work.
4. **Auto mode** lets Claude proceed safely, stopping only for destructive actions, injection risks, or when no safe workaround exists.
5. **Work trees** let many Claudes share a repo without collisions; **agent view** lets you watch them all and run them in the background.
6. **Auto memory** remembers project facts across sessions (notes Claude takes), separate from the `CLAUDE.md` manual you write.
7. **Ultra-review** automates multi-agent, multi-phase code review; **routines** trigger Claude from schedules, webhooks, and API calls, in the cloud.

## Common pitfalls

- ❌ Running parallel sessions on one repo **without work trees**, so they overwrite each other's files.
- ❌ Babysitting long tasks in the default permission mode instead of turning on **auto mode**.
- ❌ Re-explaining the same project facts every session instead of relying on **auto memory**.
- ❌ Confusing `CLAUDE.md` (your hand-written manual) with `memory.md` (Claude's auto notes).
- ❌ Assuming routines need your machine on; they run in the cloud.
- ❌ Dismissing the desktop app based on an old version.
- ❌ Treating the changelog as something to read once rather than a habit.

---

## 🛠️ Capstone Project: the Hands-Off Workbench

> This is the main hands on project for the lesson. You will wire up one real repo so Claude can work on it with as little babysitting as possible, switching on each feature from this lesson and proving it works. Start small and add one capability per milestone.

### What you will build

A **Hands-Off Workbench**: a single project (pick a small real one, or scaffold a fresh app) configured so that you can dispatch work to Claude, leave, and come back to find it done, reviewed, and reacting to events on its own. The project itself is secondary; the *setup* is the deliverable.

> 🎯 **Pick your project.** Any repo with a GitHub remote works. A tiny web app or CLI tool is ideal because it gives you real PRs and issues to trigger automation against.

### Why this is the perfect practice

| Lesson skill | Where you use it in the Workbench |
|---|---|
| Remote control | Milestone 1, dispatch and continue from your phone |
| Full-screen TUI | Milestone 1, make it the default |
| Auto mode | Milestone 2, run a long task untouched |
| Work trees | Milestone 3, two parallel features at once |
| Agent view | Milestone 3, watch both sessions |
| Auto memory | Milestone 4, capture a project convention |
| Ultra-review | Milestone 5, review a PR |
| Routines | Milestone 6, react to a GitHub event |

### Milestones (build them in order, each one works on its own)

1. **Go remote and full-screen.** In a session, run `/tui full-screen` and `/remote-control`. Dispatch a small task ("add a README section"), then continue it from the Claude mobile app or a browser. Set both to default in your settings. Confirm you got a phone notification when Claude needed input.
2. **Run untouched with auto mode.** Turn on auto mode. Give Claude a multi-step task that would normally trigger several permission prompts (read several files, run tests, make edits). Walk away. Confirm it finished without stopping for trivia, and note any point where it *did* stop (was it genuinely destructive or injection-like?).
3. **Parallelize with work trees and agent view.** Start two sessions on two separate features using `claude --worktree` for each, then open `claude agents` and watch both. Use **space** to poke one without entering it. Confirm neither session overwrote the other's files.
4. **Teach it a convention with auto memory.** During a session, establish a project convention (a naming rule, a preferred library, a test command). End the session, start a new one, and confirm Claude already knows the convention. Run `/memory` to inspect what was saved. Note the difference between this and what you keep in `CLAUDE.md`.
5. **Automate review with ultra-review.** Open a PR, run `/ultra-review` (or install the GitHub app so it runs automatically), and read the findings. Confirm at least one finding is real and useful. Note how the multi-phase check filtered out noise.
6. **React to events with routines.** Create a routine that triggers on a GitHub event (a new issue) and posts a review comment. Open a test issue and confirm the routine fired in the cloud, with your machine's role minimal. Add a second routine on a schedule (a daily summary) for good measure.
7. **Stretch goals.** Wire a routine to an external API call (a webhook from another service). Add `CLAUDE.md` onboarding notes and compare how they combine with auto memory. Use the desktop app to review the diffs and comment on a specific line.

### How you will know you are done

- ✅ You dispatched a task on your computer and **continued it from another device**.
- ✅ A long task ran to completion in **auto mode** without trivial interruptions.
- ✅ Two Claudes worked the same repo in **parallel work trees** with no file collisions, both visible in agent view.
- ✅ A new session **already knew** a convention from a previous one (auto memory), and you can explain why it differs from `CLAUDE.md`.
- ✅ A PR was **auto-reviewed** and a **routine fired on a GitHub event**, both with minimal hands-on work from you.

> 💡 **The real test:** after setup, how little do you have to do? Every milestone removes one reason to sit and watch a session.

---

## Practice exercises (optional extra reps)

> **What these are:** five small, self-contained tasks, each focused on one feature. Optional and independent. The **Capstone above is the main build** and already covers all of them.

### Exercise 1: phone handoff (foundational)
Start a session, run `/remote-control`, and complete one full back-and-forth from your phone. Then set remote control to always-on in your settings.

### Exercise 2: flicker test (foundational)
Run a long task in the default mode and watch for flicker. Switch to `/tui full-screen` and run a similar task. Use a clickable element (expand a long file, jump to bottom). Note the difference.

### Exercise 3: auto mode boundary (intermediate)
Construct a task that includes one genuinely risky step (deleting a file, say) among safe ones. Run it in auto mode and observe whether Claude proceeds, finds a workaround, or stops to ask. Explain the classifier's decision.

### Exercise 4: memory vs manual (intermediate)
Put one fact in `CLAUDE.md` by hand. Let Claude learn a *different* fact via auto memory during a session. Start a fresh session and confirm both are available. Run `/memory` and describe what lives where.

### Exercise 5: an end-to-end routine (advanced)
Build a routine that triggers on a GitHub PR, runs a review, and comments on the PR. Open a test PR to fire it. Then add a scheduled routine that runs daily. Confirm both ran in the cloud with your machine off.

---

## Cheat sheet

```text
DEVELOPER EXPERIENCE
  /remote-control ......... continue a session from phone or browser (set always-on)
  /tui full-screen ........ flicker-free, clickable, flat memory (set as default)
  desktop app ............. plan review + diff comments + GitHub (use for those tasks)

AUTONOMY
  auto mode ............... proceeds safely; stops only for destructive/injection/no-workaround
  claude --worktree ....... isolated copy of the repo so parallel Claudes don't collide
  claude agents ........... agent view: watch all sessions, run in background
                            (enter = open, space = quick prompt)
  auto memory ............. Claude's own notes across sessions  (audit with /memory)
                            CLAUDE.md = your manual ; memory.md = Claude's notes

AUTOMATION
  /ultra-review ........... multi-agent, multi-phase PR review (also native in GitHub app)
  routines ................ trigger Claude on schedule / webhook / API call, in the cloud

STAY CURRENT
  docs "What's new" + changelog + dev team socials + newsletter
```

## How this connects to the rest of the course

- **Earlier, Module 2 (Picking the right model and the thinking lever):** the autonomy features lean on more capable models making safe judgement calls.
- **Earlier, Module 3 (Evals):** the multi-agent, multi-phase code review is the same "creator plus critic" idea from the evals lesson, productised.
- **Next, Module 4 · Lesson 9 (How we Claude Code):** goes deep on the *workflow* (spec, plan, verify) that makes all this autonomy pay off.
- **Later, Module 5 (Managed agents):** routines and background sessions are the on-ramp to fully asynchronous, event-driven agents.

---

*Source: "What's new in Claude Code" by Ralf (Anthropic), Code with Claude 2026, London. Commands and flags are illustrative reconstructions of the features shown in the talk; check the current docs and changelog, since these features move fast and some are in preview.*

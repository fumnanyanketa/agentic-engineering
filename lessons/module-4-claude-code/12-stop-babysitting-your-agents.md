# Module 4 · Lesson 12: Stop Babysitting Your Agents

> **Course:** Building with Claude, a self-paced course
> **Module 4:** Claude Code, your everyday agent
> **Speaker:** Siddh Bhundasarya, Founding Engineer of Claude Code, Anthropic
> **Source talk:** [Stop babysitting your agents](https://www.youtube.com/watch?v=wI0ptqCSL0I) · [full transcript](../../transcripts/code-with-claude-2026-london-2026/23_stop-babysitting-your-agents.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

To stop staring at the screen waiting for Claude, you stack three skills that build on each other: teach Claude to **verify its own work** in a loop (give it the tools and instructions to check itself), then **run many Claudes in parallel** without losing your attention, then put the whole thing on **background loops** so work happens without your keyboard at all.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you build a **Self Verifying Agent Lab**: you take a real full stack app, teach Claude to verify its own changes, package that into a self improving skill, run several Claudes at once, and finally hand a recurring chore to a background loop. Everything before the Capstone teaches a piece you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section near the end, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[Building Effective Agents (Anthropic)](https://www.anthropic.com/engineering/building-effective-agents)** (essay). Grounds the core idea: an agent loops against ground-truth verification and only needs the human when it lacks a check of its own.
> - **[Best practices for Claude Code: give Claude a way to verify its work](https://code.claude.com/docs/en/best-practices)** (docs). The official statement of "close the loop so you're not the verification step," which is the exact thesis of the lesson.

## A few plain-language basics first

This lesson uses some everyday agent and engineering terms. Here they are in plain words:

- **Agent:** an AI that takes a series of actions on its own toward a goal. Claude Code is an agent.
- **Babysitting:** Siddh's word for sitting at the screen waiting for the agent, or acting as a "glorified QA tester" (a person who only checks the agent's output). The whole talk is about doing less of this.
- **Verification:** checking that work is actually correct. For an agent, this means giving it the tools to test its own changes rather than relying on you to catch mistakes.
- **Loop:** "an autonomous circuit that you can complete for Claude." You give Claude tools to do work **and** to check the work, and it cycles (write, test, fix, test again) until it reaches a success state. This is the single most important idea in the lesson.
- **Hill climbing:** steadily improving toward a goal one step at a time, like walking uphill until you reach the top. A loop lets Claude hill climb on a task.
- **CLAUDE.md:** a special markdown (text) file Claude Code reads automatically. A high quality one is the single highest leverage thing you can do.
- **MCP (Model Context Protocol):** a standard way to connect Claude to an outside tool or service. Used here to give Claude a browser.
- **Skill:** a folder with a markdown file that stores reusable knowledge about one topic, so you and your teammates can share it.
- **Linter / type checker:** tools that automatically flag mistakes in code. A linter flags style and common errors; a type checker flags mismatched data types.
- **PR (pull request):** a proposed code change submitted for review.
- **CI (continuous integration):** the system that automatically builds and tests your code when you push it. "Keeping CI green" means keeping those automated checks passing.
- **Worktree:** a second checkout of the same git repository in a different folder, so two agents can work without colliding.

You do not need to memorise these. Every term is also explained again the first time it appears below.

## Why this lesson matters

As models get smarter, Siddh has noticed something backwards happening: engineers spend a **larger** share of their time just watching the screen, waiting for Claude, or acting as a QA tester for it. That is "unsatisfying and an inefficient use of your time." This lesson hands back that time.

> "What does an agent need from your code base that a human takes for granted?" (Siddh Bhundasarya)

That single question frames the whole talk. Humans assume they can run the app, open a browser, log in, and check the result. Claude has to be **given** those abilities. The good news is that the same playbook humans use to verify their own work translates almost directly to Claude.

Siddh calls this a "Claude Code 301" talk, so it assumes some table stakes (covered next).

## Learning objectives

By the end of this lesson you will be able to:

1. Recognise the three prerequisites that make everything else work (a high quality `CLAUDE.md`, connected tools, and a remote environment).
2. Build a **verification loop** by giving Claude the tools and instructions to check its own work.
3. Package a verification loop into a **self improving skill** you can share with teammates and your future self.
4. Run several Claudes in parallel without overloading your attention (desktop app, Agent View, the cloud, and remote control).
5. Set up **background loops** with `/loop` (local) and **routines** (remote) for recurring work that does not need you.

## Prerequisites

These are Siddh's "table stakes." Get these in place first.

1. **A high quality `CLAUDE.md` file.** "This is the single highest leverage thing that you can do to improve your Claude Code experience."
2. **Connected tools.** A good rule of thumb: if a tool is useful to you day to day (Slack, Asana, Linear, Datadog, BigQuery), it is useful to Claude, because it helps Claude stitch together richer context.
3. **A remote environment on Claude Code Web.** This decouples the compute running Claude from your laptop, so you can close the lid, the laptop can die, and your sessions keep running in the cloud.

Also helpful: Module 4 · Lesson 10 (Beyond the Basics) and Lesson 11 (Proactive Agent Workflows), which introduce hooks, parallelism, and routines.

---

## Part 1: why your tooling has to change

Most software tooling so far (linters, IDEs, code formatters like Prettier, type checkers, even compilers) was built to make **humans** faster. But humans are no longer writing most of the code; agents are. So we have to zoom out and reconsider the tool chain.

There is good news and bad news.

- **Good news:** a lot of human tools translate well to agents. Claude can use formatters, linters, and **symbol servers** (tools that understand where things are defined in your code) quite effectively.
- **Bad news:** we have **blind spots**. As humans we make assumptions about our tooling that Claude does not share. Hence the framing question: what does an agent need that a human takes for granted?

> 🔑 **The whole talk in one arc.** Three things that build on each other:
> 1. **Verification:** teach Claude to check its own work.
> 2. **Multi Claude:** once Claude is reliable, run many at once with confidence.
> 3. **Background loops:** take your keyboard out of the critical path entirely, so Claude keeps doing useful work in the background.

---

## Part 2: verification, teaching Claude to check its own work

Siddh runs a quick brainstorm: think about the last feature you built, and how you **verified** your work, not just the final output, but how you iterated with confidence that you were heading the right way.

Most software work, he argues, breaks down into the same series of steps. And the key insight is that **Claude can use the exact same playbook.**

```text
THE HUMAN VERIFICATION PLAYBOOK  (Claude can use it too)

  design & write code
        |
  build / compile / type-check  --(fails)--> change code, repeat
        |
  run the executable  (Docker container, CLI, web server)
        |
  check side effects  (UI in a browser, logs, database state)
        |
  run unit tests  (no regressions; add new tests)
        |
  deploy to staging  (or, if brave, straight to prod)
```

> 🔑 **The reframe.** "The same exact playbook can be used by Claude quite effectively to verify its own work and build software. The only thing required is giving Claude the right tools and instruction set." Teach Claude to verify the way **you** would.

### Loops: the most important idea in the talk

A **loop** is "an autonomous circuit that you can complete for Claude." You give Claude access to tools that both **do** work and **check** work, and it cycles until it reaches a success state.

> "Wherever possible, our goal now is to get Claude into a loop by giving it the tools and instructions required for it to work effectively." (Siddh Bhundasarya)

Siddh's real example: the sign up button on his personal website stopped working. He told Claude "make the sign up button work," and Claude:

```text
1. wrote some code
2. built the app
3. opened a browser, clicked the sign-up button -> nothing happened
4. read the logs, found the problem
5. fixed the code, reloaded the app
6. repeated until clicking the button actually worked
7. sent a PR that genuinely worked
```

This is **hill climbing**: each cycle gets a little closer to the goal. When Claude finally reaches a success state, you can trust the PR more, because it has already proven it works.

> 💡 Verification comes in flavors (front end / UX, back end, and full end to end including infrastructure), but the **core concept is identical**: give Claude the tools and instructions to get into a loop. Once you nail that, all three flavors merge into one. You do not have to be hyper specific about instructions if Claude has the right tools.

### What a front end verification loop actually needs

To make this concrete, Siddh lists four things for a front end (UX) loop:

| Step | What it means | Example |
|---|---|---|
| **1. Run your application** | Start the app so there is something to test. | `npm run start` (start the dev server) |
| **2. Use the app** | Drive a real browser. | The **Claude in Chrome** MCP tool (`/chrome`), or Playwright, or another browser control MCP |
| **3. Prove something works** | Capture evidence before and after a fix. | Take a screenshot before and after, confirm the right state |
| **4. Unblock it** | Clear the obstacles that stop a loop in a real app. | **Auth** (give Claude a login identity) and **state** (pre populate data, e.g. seed an e-commerce inventory) |

> ✅ **Best practice on unblocking.** Auth and state setup are nothing new: end to end tests already use state setup scripts. The two differences for agents: **give Claude access** to those scripts, and **make them dynamic** rather than overly prescriptive, so Claude can do a wider variety of things than a static script allows.

### Package the loop as a self improving skill

Once you have a verification loop, how do you share it with teammates, coworkers, and your future self? Use a **skill** (a folder storing reusable context about one topic, here the verification loop).

The clever part is making the skill **self improving**:

> 🔑 **The self documenting skill.** Put instructions inside the skill telling Claude to **improve the skill every time it hits a blocker**. Now, when anyone on the team runs into a new obstacle, the skill edits itself to fix it for next time. Everyone contributes, not just you. This is exactly how the Claude Code team does verification: a single skill that is explicitly told to keep documenting itself.

### The demo: MonkeyType

Siddh demos on **MonkeyType**, an open source typing test app that is representative of a real full stack app (TypeScript, an Express backend, MongoDB and Redis for storage). The flow:

```text
1. "spin up the dev server"      -> Claude reports it is already running
2. /chrome                       -> confirm the Chrome MCP is enabled
3. "use the Chrome MCP to make sure the front end is working"
                                 -> Claude navigates to localhost:3000, reads the page
4. "can you try typing and make sure everything works"   -> Claude types, confirms
5. "can you also use the settings and change something"   -> Claude changes a setting,
                                                            confirms it persisted
```

So far Siddh **held Claude's hand**, telling it exactly what to do. That **is** verification. Next he captures it:

```text
"Take everything we learned and put it into a skill file in docs/claude/demo-verification."
```

Claude writes a `SKILL.md` that includes: (1) bring up the stack (with the commands, including Docker Compose), (2) load the Chrome MCP tools, and (3) run a smoke test using the browser tools to check its own work. (A **smoke test** is a quick check that the basics work.)

Finally, the payoff. Siddh asks Claude to add a feature ("every time I mistype, show a confetti animation") and to **use the new skill to verify itself**. The loop runs live: Claude writes code, hits lint errors, fixes them, and verifies again, cycling to a good state. He switches on **auto mode** so it does not ask permission for every file edit.

> 💡 **The takeaway from the demo.** First **hold Claude's hand** and show it how to verify. Then have it **summarize those learnings into a skill** you can package and distribute. Setting up a verification loop is genuinely simple, often five to ten minutes once you work past a couple of blockers.

---

## Part 3: multi Claude, parallelizing without losing your mind

Once Claude can reliably verify itself, you can run several at once with confidence. But there is a catch: **your attention is a scarce resource.** Siddh finds more than four or five simultaneous sessions takes a big load on his brain. So the goal of every tool here is to **protect your attention**.

He covers four ways to multi Claude.

| Tool | What it is | How it protects your attention |
|---|---|---|
| **Claude Code desktop app** | A GUI with a sidebar listing **all** sessions across all surfaces (local terminal, cloud, all git repos). | Central control plane. Pin, rename, and color sessions so you instantly remember what each was doing. |
| **Claude Agents (Agent View)** | A terminal view (`claude-agents` instead of `claude`) listing local sessions. | **Sorts by attention needed:** sessions blocked on a permission prompt or question rise to the top; running or completed ones sink. Pin, rename, reorder. |
| **Claude in the cloud (Claude Code on the web)** | Run sessions on Anthropic's compute, not your laptop. | Decouples your laptop from your sessions. Walk between meetings or drive home without keeping the lid open. Start at claude.ai. |
| **Remote control** | Control any session on any surface from your phone (`/remote-control`). | Buzzes your phone when Claude needs input. Reply from your car or anywhere. Siddh's favorite feature. |

> 💡 **The old way still works, but it is heavy.** Siddh used to run a **Tmux** window manager (a terminal tool that splits one window into panes) with four panes, each on its own **worktree** (a separate checkout of the same repo). It works, but you have to manage Tmux and worktrees yourself. Claude Agents gives you most of those benefits with far less to manage.

> 🔑 **Renaming and coloring are not cosmetic.** They are attention management. A memorable name or color means that when you return to a session, you immediately know what it was doing, which cuts the cost of context switching.

---

## Part 4: background loops, taking your keyboard out of the loop

Even with great multi Claude tooling, you still have to **spin up** each session: have a goal, open a session, type a prompt. How do you remove yourself even further? Background loops.

A lot of engineering work is not writing a brand new feature; it is **bookkeeping**: babysitting PRs (getting through review comments, merge conflicts, and CI failures), updating docs, triaging, monitoring feedback, and keeping CI green. With more PRs than ever (thanks to AI), this can eat hours a day. These tasks "don't necessarily need you in the loop, they just need to be running in some sort of loop."

### /loop (local)

`/loop` runs a prompt at a set interval inside Claude Code.

```text
/loop 10m babysit my open PRs
```

The session running the loop wakes up every 10 minutes, runs the prompt, and (if your `CLAUDE.md` and tools are set up correctly) figures out what to do on its own. No manual babysitting.

### Routines (remote)

> 🔑 **Routines are "basically `/loop`, but running remotely."** They live in the same remote containers as Claude Code on the web. Set one up from the web or desktop app's Routines tab with a **time based** or **event based** trigger, and the trigger opens a Claude Code session with a specified prompt.

Real Claude Code team examples: a routine that updates docs every day, and a routine that reviews incoming issues and feedback and posts to a Slack channel every six hours. (Lesson 11 covers routines in depth.)

> 🎯 **Stack all three and you arrive at a system that does a lot of work without you on the keyboard.** Verification makes Claude reliable; multi Claude lets you run many; background loops remove you from the loop. "That really is the ultimate goal: spend your attention and time on the tasks that you care about, and delegate everything else to Claude with high reliability and confidence."

---

## Key takeaways

1. **Stop babysitting by stacking three skills:** verification, multi Claude, and background loops, in that order. Each one depends on the one before it.
2. **Get the table stakes first:** a high quality `CLAUDE.md`, connected tools, and a remote environment.
3. **Teach Claude the same verification playbook you use:** build, run, check side effects (browser, logs, database), test. It just needs the tools and instructions.
4. **Get Claude into a loop wherever possible.** A loop lets it hill climb (write, check, fix, repeat) until it reaches a success state, so its PRs actually work.
5. **A front end loop needs four things:** run the app, drive a browser, prove it works (screenshots), and unblock auth and state.
6. **Package the loop as a self improving skill** that documents itself every time it hits a blocker, so the whole team benefits.
7. **Protect your attention** when running many Claudes: the desktop app, Agent View (sorted by attention), the cloud, and remote control, plus naming and coloring.
8. **Hand recurring chores to loops:** `/loop` locally and routines remotely.

## Common pitfalls

- ❌ Acting as a "glorified QA tester," manually checking everything Claude produces.
- ❌ Skipping the table stakes (`CLAUDE.md`, connected tools, remote env) and wondering why loops are unreliable.
- ❌ Giving Claude tools to **write** code but not to **check** it, so it cannot close the loop.
- ❌ Forgetting auth and state setup, so a verification loop stalls the moment it hits a login screen or empty database.
- ❌ Writing a verification script that is too static and prescriptive, limiting what Claude can do.
- ❌ Opening so many sessions that your attention is overloaded (Siddh tops out around four or five).
- ❌ Manually babysitting PRs and docs when a `/loop` or routine could do it.

---

## 🛠️ Capstone Project: Self Verifying Agent Lab

> This is the main hands on project for the lesson, and the best way to make everything stick. You will take a real app, teach Claude to verify its own work, package that into a self improving skill, run several Claudes in parallel, and finally hand a chore to a background loop. Start small and grow it.

### What you will build

**Self Verifying Agent Lab** is a workflow, not a single artifact. By the end you will have: a working verification loop on a real app, a self improving verification skill, a multi Claude setup you can manage without overload, and at least one background loop running a recurring chore.

> 🎯 **Pick your world.** Use any full stack-ish app you can run locally. MonkeyType (open source, from the talk) works, or use your own project. It just needs a dev server you can start, a browser facing UI, and something you can verify (a button, a setting, a page).

### Why this is the perfect practice

| Lesson skill | Where you use it in Self Verifying Agent Lab |
|---|---|
| Table stakes (`CLAUDE.md`, tools, remote env) | Milestone 1, you cannot loop reliably without them |
| The four step front end loop | Milestone 2, run, drive a browser, prove, unblock |
| Auth and state unblocking | Milestone 3, get past the login screen and empty data |
| Getting Claude into a loop (hill climbing) | Milestone 4, add a feature and let it self correct |
| Self improving skill | Milestone 5, package and make it document itself |
| Multi Claude attention management | Milestone 6, run several, named and colored |
| Background loops (`/loop` and routines) | Milestone 7, delegate a recurring chore |

### Milestones (build them in order, each one works on its own)

1. **Table stakes.** Write a high quality `CLAUDE.md` for your app. Connect at least one useful tool. Set up a remote environment on Claude Code Web. (If you skip these, the loops below will be flaky.)
2. **Hand held verification.** In a fresh session, hold Claude's hand: tell it to start the dev server, enable the browser MCP (`/chrome` or Playwright), navigate to the app, and confirm a couple of things work (type something, change a setting). This is verification, done manually.
3. **Unblock auth and state.** Add what a real app needs: give Claude a login identity (auth) and a dynamic script to pre populate data (state). Confirm the loop can now get past the login screen and reach a meaningful state.
4. **A real loop.** Ask Claude to add a small feature and to **verify itself**. Turn on auto mode so it does not stop for every edit. Watch it hill climb: write code, hit errors (lint, type, behavior), fix, re verify, until it reaches a success state.
5. **Self improving skill.** Tell Claude to put everything it learned into a `SKILL.md` (bring up the stack, load the browser tools, run a smoke test). Add the magic instruction: **improve this skill every time you hit a blocker.** Hit a blocker on purpose and confirm the skill edits itself.
6. **Go multi Claude.** Run three sessions at once on different tasks. Use Agent View (or the desktop app) and **name and color** each one. Notice how attention sorting and naming reduce your context switching cost. Try remote control from your phone.
7. **Background loop.** Pick a recurring chore (babysit open PRs, keep CI green, or update docs). Set it up as a `/loop` locally, then as a **routine** remotely so it survives your laptop closing. Let it run while you do something else.
8. **Stretch goals.** Add back end and end to end verification flavors to the same skill. Share the skill with a teammate and have them contribute a blocker fix. Chain a generator routine with a critiquer routine.

### How you will know you are done

- ✅ Claude runs a **verification loop** on your app, driving a real browser and proving a fix works (with before/after screenshots).
- ✅ The loop gets past **auth and state** without you intervening.
- ✅ Your **skill improves itself**: you hit a blocker and the `SKILL.md` updated to handle it next time.
- ✅ You can run **three or more Claudes** at once and still know what each is doing (named, colored, sorted by attention).
- ✅ At least one **background loop or routine** is doing a recurring chore without your keyboard.

> 💡 **Keep yourself honest:** the moment you find yourself manually QA testing Claude's output, ask "could a verification loop have caught this?" If yes, teach it to the skill.

---

## Practice exercises (optional extra reps)

> **What these are:** five small, self contained tasks, each targeting one skill. They are optional and independent. The **Capstone Project above is the main build** and already includes all of these skills, so feel free to skip straight to it.

### Exercise 1: audit your table stakes (foundational)
Check the three prerequisites: do you have a high quality `CLAUDE.md`, connected tools, and a remote environment? Fix whichever is missing before doing anything else.

### Exercise 2: map your own verification playbook (foundational)
Write down how **you** verified your last feature, step by step (build, run, check side effects, test). Then mark which steps Claude could do if you gave it the right tools.

### Exercise 3: build a minimal loop (intermediate)
On a small app, hold Claude's hand through a four step front end loop: start the dev server, drive a browser, prove one thing works with a screenshot, and identify one blocker (auth or state) you would need to clear.

### Exercise 4: write a self improving skill (intermediate)
Turn the loop from Exercise 3 into a `SKILL.md`. Include the instruction to improve itself on every blocker. Then deliberately break something and confirm the skill updates.

### Exercise 5: delegate a chore to a loop (advanced)
Pick one recurring chore (PRs, docs, CI). Set it up with `/loop` at a sensible interval, then convert it to a routine so it runs remotely. Confirm it does useful work while your laptop is closed.

---

## Cheat sheet

```text
THE THREE STACKED SKILLS
  1. VERIFICATION  -> teach Claude to check its own work (a loop)
  2. MULTI-CLAUDE  -> run many reliable Claudes, protect your attention
  3. BACKGROUND LOOPS -> take your keyboard out of the critical path

TABLE STAKES (do these first)
  - high-quality CLAUDE.md   (highest leverage thing you can do)
  - connect your tools       (useful to you => useful to Claude)
  - remote env on Claude Code Web  (laptop-independent)

A FRONT-END VERIFICATION LOOP NEEDS 4 THINGS
  1. run the app        (npm run start)
  2. drive a browser    (/chrome MCP, or Playwright)
  3. prove it works     (before/after screenshots)
  4. unblock            (auth = login identity; state = seed data; keep scripts dynamic)

PACKAGE IT
  -> put the loop in a SKILL.md
  -> tell the skill to improve itself on every blocker (self-documenting)

MULTI-CLAUDE (attention is scarce; ~4-5 max)
  desktop app | Claude Agents (sorted by attention) | cloud | remote-control
  rename + color sessions

BACKGROUND LOOPS
  /loop 10m babysit my open PRs     (local, on a timer)
  routines                          (remote: time-based or event-based triggers)
```

## How this connects to the rest of the course

- **Earlier, Module 4 · Lesson 10 (Beyond the Basics):** hooks (the "red squiggly" feedback), worktrees, and `/loop` first appear there; this lesson turns them into a full verification and parallel workflow.
- **Earlier, Module 4 · Lesson 11 (Proactive Agent Workflows):** routines are introduced there in depth; here they are the remote form of background loops.
- **Earlier, Module 2 (Core skills):** prompting, context, and the generate, evaluate, repair pattern, which is the same loop shape applied at the prompt level.

---

*Source: "Stop babysitting your agents" by Siddh Bhundasarya (Anthropic), Code with Claude 2026, London. Command examples, the skill outline, and the loop diagrams are illustrative reconstructions of what the talk demonstrated. Adapt the exact commands, MCP names, and model names to the current version of Claude Code.*

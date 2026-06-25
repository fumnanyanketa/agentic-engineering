# Unit 1: The Coding-Agent Workflow

> **Course:** Agentic Engineering, a model-agnostic self-paced path *(working title)*
> **Unit 1 of 11:** Set up a real workstation, then learn to drive a coding agent (Claude Code, Gemini CLI, or Codex CLI) through a plan, act, verify loop, the tool you build everything else with
> **Principle (vendor-neutral):** Agentic Engineering Module 16, Working with coding agents
> **The how, across agents:** Claude Code (Anthropic), Gemini CLI (Google), Codex CLI (OpenAI), current practice verified June 2026
> **AtlasOS build:** your workstation and your first repository, the launchpad for the whole fleet
> **Estimated time:** 2 to 3 hours (most of it is one-time setup you never repeat)

---

## In one sentence

A coding agent is a tool you talk to in plain English that reads, writes, and runs code on your computer, and this unit takes you from a blank machine to a working setup where you can drive one well: you will install everything step by step, learn the one durable habit that separates real engineering from guesswork (plan, then act, then verify), and finish by creating your first project, all explained click by click so you never have to guess what to do next.

> 🎯 **Where this unit is heading.** The payoff is a **Build** where you stand up your workstation and your first real project (the start of your north-star, AtlasOS) with the coding agent you chose. We do every step together: installing the tools, creating a project on GitHub, copying it to your computer, writing the file that teaches the agent about your project, and running your first task. Nothing is assumed. Jump to **"The Build"** to see the finish line, then come back and we will get you there.

## First-principles companion

> 💡 **The durable ideas behind this unit.** The tools are recent and change often; the craft does not. If you want the timeless versions (optional, read them any time):
>
> - **[Building Effective Agents (Anthropic)](https://www.anthropic.com/engineering/building-effective-agents)** (essay). What an "agent" actually is, underneath any product.
> - **[Raising the bar on SWE-bench Verified (Anthropic)](https://www.anthropic.com/research/swe-bench-sonnet)** (essay). How a coding agent is built from simple parts: a model, a way to run commands, a way to edit files, and a loop.
> - **[ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)** (paper). The reason, act, observe loop every coding agent runs.

## A few plain-language basics first

New terms, in plain words. You do not need to memorise these; each is explained again the moment it matters.

- **Coding agent:** a tool you give a task to in plain English, and it reads, edits, and runs code for you, step by step, in a loop. The three we cover are **Claude Code**, **Gemini CLI**, and **Codex CLI**.
- **Workstation:** your setup for doing the work. For this course that means a code **editor** (we use VS Code), a **terminal**, and a few free tools installed (Node.js, git) plus two accounts (GitHub, and your chosen agent).
- **Editor / IDE:** the app where you view and edit code files. We use **Visual Studio Code (VS Code)**, a free, popular editor.
- **Terminal:** a text window where you type commands to your computer instead of clicking. It looks intimidating; it is just a place to type instructions. VS Code has one built in.
- **Command:** a single typed instruction you run in the terminal (for example `node --version`). You type it and press Enter.
- **Git:** a free tool that tracks every change to your project, like an unlimited undo history. **GitHub** is a website that stores copies of git projects online.
- **Repository (repo):** a project folder that git tracks. "Cloning" a repo means downloading a copy from GitHub onto your computer.
- **Node.js / npm:** Node.js is a program that lets your computer run JavaScript tools; **npm** is the installer that comes with it. Two of our three agents are installed with npm.
- **The loop:** every agent runs the same cycle: read your code, make a plan, change something, run a check, read the result, fix course. We call it **plan, act, verify**.

## Why this unit matters

The rest of this course teaches you to *build* agent systems. This unit teaches you to *use* an agent as your daily tool, because you will build everything else, including AtlasOS, by driving one of these. The tool comes first, and we set it up properly so the later units are pure building, not fighting your setup.

> 🔑 **Agentic engineering, not vibe coding.** "Vibe coding" is accepting whatever the agent produces and hoping it works. **Agentic engineering** is building software *with* an agent while staying responsible for the result: you describe the task clearly, decide what the agent is allowed to do, and check its work. The agent is the fastest junior teammate you have ever had, and you are the one who signs off.

## Learning objectives

By the end of this unit you will be able to:

1. Set up a complete workstation from scratch: editor, terminal, Node.js, git, and the accounts you need.
2. Install and sign in to at least one coding agent (Claude Code, Gemini CLI, or Codex CLI), and recognise how the other two do the same.
3. Run the plan, act, verify loop on purpose, and choose a safe autonomy level for the task.
4. Create a project on GitHub, copy it to your computer, and give the agent a memory file so it understands your project.
5. Finish a first real task with the agent and review its work like an engineer.

## Prerequisites

- **What you need:** a computer (Windows, macOS, or Linux), an internet connection, and a couple of hours. That is genuinely it.
- **What you do NOT need:** prior coding experience, an existing editor, or any of these tools already installed. We install everything together below.
- **One honest note:** if you have never used a terminal, you will after this unit. We explain every command. Go slowly and you will be fine.

---

## Part 0: Set up your workstation (do this once)

This is the longest one-time setup in the whole course. After this, every later unit just uses what you build here. Follow the steps in order. After each install, we run a quick command to *prove* it worked, so you are never left wondering.

> 💡 **How to read the commands.** When you see a grey box like the one below, that is something you type into your terminal and press Enter. Lines starting with `#` are explanations, not something to type. The lines below a command show roughly **what you will see** in response.

### Step 1: Install your editor (VS Code)

You can use any editor you like, and once you are comfortable you are welcome to switch. **For this course we standardise on Visual Studio Code (VS Code)** because it is free, runs on every system, has a built-in terminal, and every coding agent has a VS Code add-on. Picking one shared tool means every instruction in this course matches what is on your screen.

1. Open your web browser and go to **[https://code.visualstudio.com](https://code.visualstudio.com)**.
2. Click the big blue **Download** button. The site detects your operating system automatically.
3. Open the downloaded file and follow the installer:
   - **Windows:** run the `.exe`, accept the agreement, and importantly tick the box **"Add to PATH"** if offered (it lets the terminal find VS Code).
   - **macOS:** open the `.zip`, then drag the **Visual Studio Code** icon into your **Applications** folder.
   - **Linux:** install the `.deb` or `.rpm` package, or use your software centre.
4. Open VS Code. You should see a **Welcome** tab. You are done with this step.

### Step 2: Open the terminal inside VS Code

The **terminal** is where you will type commands. VS Code has one built in, so you never leave the editor.

- In VS Code's top menu, click **Terminal**, then **New Terminal**. (Shortcut: hold **Ctrl** and press the backtick key `` ` ``, the one above Tab.)
- A panel opens at the bottom with a blinking cursor. That is your terminal. This is where every command below goes.

> 💡 **You cannot "break" anything by typing a command wrong.** If a command is not recognised, the terminal just prints an error and waits. Read it, fix the typo, try again. That is the whole loop.

### Step 3: Install Node.js (this also installs npm)

Two of our three agents are installed with **npm**, which comes bundled with **Node.js**. Installing Node.js gives you both.

1. Go to **[https://nodejs.org](https://nodejs.org)**.
2. Download the version labelled **LTS** (Long Term Support, the stable one). Avoid "Current".
3. Run the installer and accept the defaults (just keep clicking Next / Continue).
4. **Close and reopen your terminal** (so it notices the new tool), then prove it worked:

```text
# Ask Node.js and npm to report their version numbers.
node --version
npm --version

# What you'll see (your numbers may be higher, that's fine):
v22.14.0
10.9.2
```

If you see two version numbers, Node.js is installed. If instead you see "command not found", close every terminal window, reopen one, and try again; if it still fails, re-run the installer and make sure it finishes.

### Step 4: Install git

**Git** tracks your project's history, and the agents use it constantly.

1. Go to **[https://git-scm.com/downloads](https://git-scm.com/downloads)** and download the version for your system.
   - **macOS shortcut:** you can instead type `git --version` in the terminal; macOS offers to install it for you.
   - **Linux:** `sudo apt install git` (Debian/Ubuntu) or your distro's equivalent.
2. Run the installer and accept the defaults.
3. Reopen the terminal and prove it:

```text
git --version

# What you'll see:
git version 2.45.2
```

4. Tell git who you are (it stamps your name on saved changes). Use any name and the email you will use for GitHub:

```text
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

### Step 5: Create your accounts

You need two free accounts. Create the first now; create the second based on which agent you pick in Part 2.

1. **GitHub** (stores your projects online): go to **[https://github.com](https://github.com)** and click **Sign up**. Pick a username you are happy to keep, verify your email, and you are in.
2. **Your agent's account** (pick one in Part 2):
   - **Claude Code:** a paid Anthropic plan (Pro, Max, Team, or Enterprise) at **[https://claude.ai](https://claude.ai)**, or an API key from **[https://console.anthropic.com](https://console.anthropic.com)**.
   - **Gemini CLI:** a free Google account works to start, or an API key from **[https://aistudio.google.com](https://aistudio.google.com)**.
   - **Codex CLI:** a paid ChatGPT plan (Plus, Pro, or higher) at **[https://chatgpt.com](https://chatgpt.com)**, or an OpenAI API key from **[https://platform.openai.com](https://platform.openai.com)**.

> ✅ **Checkpoint.** Before moving on, you should have: VS Code open, a working terminal, `node --version` and `git --version` both printing numbers, and a GitHub account. If all four are true, the hardest part of the whole course is behind you.

---

## Part 1: The one habit that matters (plan, act, verify)

Every coding agent, today and next year, runs the same underlying cycle, and it asks the same thing of you. Learn it once and it transfers to any tool.

```text
        ┌──────────────────────────────────────────────┐
        │                                              │
        ▼                                              │
   1. PLAN ──────▶ 2. ACT ──────▶ 3. VERIFY ───────────┘
   decide what    make the        run a check (tests,
   to do and      change          build, you reading
   how to check                   the result); if it
   it worked                      failed, loop back
```

- **Plan:** before touching code, the agent (and you) decide the approach and how you will know it worked. On anything bigger than a tiny change, ask the agent to *plan first* and read the plan before it acts.
- **Act:** the agent makes the change. You watch it as a **diff** (a side-by-side of what changed: removed lines in red, added lines in green).
- **Verify:** the agent runs a check, a test, a build, a linter, or you simply read the diff. If the check fails, it loops back and fixes it.

> 🔑 **Verification is the bottleneck.** When writing code becomes cheap and fast, the scarce, valuable skill becomes *checking* it. Almost everything in this course exists to make checking fast and trustworthy. If you remember one idea from this unit, remember this one.

> ❌ **The beginner trap:** treating the agent as an all-knowing oracle and merging whatever it writes because it looks confident. It is confident even when wrong. Your job is not to trust it; your job is to make it easy to *check* it.

---

## Part 2: Pick and install your coding agent

The three leading agents are more alike than different: same loop, same kinds of features, different companies, prices, and ecosystems. **Pick the one whose account you already have or are happy to pay for.** You can switch later, the skills carry over, and the rest of this unit shows you all three side by side so you are never locked in.

| | **Claude Code** (Anthropic) | **Gemini CLI** (Google) | **Codex CLI** (OpenAI) |
|---|---|---|---|
| Best if you have | an Anthropic Pro/Max plan | a Google account (free start) | a ChatGPT Plus/Pro plan |
| Cost to start | paid plan or API key | free tier available | paid plan or API key |
| Open source | no | yes | yes |
| Known for | the deepest, most polished tooling | big free allowance, web search built in | running many tasks in the cloud at once |

Now install your pick. Each one is a single command in your VS Code terminal.

### If you chose Claude Code

```text
# macOS or Linux:
curl -fsSL https://claude.ai/install.sh | bash

# Windows (PowerShell):
irm https://claude.ai/install.ps1 | iex

# Then prove it installed:
claude --version
```

Start it and sign in by typing `claude` and pressing Enter. The first time, it opens your web browser to log in; approve it, return to the terminal, and you will see a prompt waiting for your task.

### If you chose Gemini CLI

```text
# Install with npm (works on every system):
npm install -g @google/gemini-cli

# Prove it installed:
gemini --version
```

Start it by typing `gemini`. It will offer sign-in options; choosing **"Login with Google"** opens your browser. Approve, return to the terminal, and you are ready.

> ⚠️ **Live note (June 2026).** Google is moving Gemini CLI's free and individual tiers to a successor named **Antigravity CLI**; paid Google Cloud and Code Assist users keep Gemini CLI. The workflow is the same either way. If `gemini` ever points you to Antigravity, follow that prompt; everything in this unit still applies.

### If you chose Codex CLI

```text
# Install with npm:
npm install -g @openai/codex

# Or on macOS with Homebrew:
brew install --cask codex

# Prove it installed:
codex --version
```

Start it by typing `codex`. Choose **"Sign in with ChatGPT"** to use your existing plan (or paste an API key). After the browser step, you land in the agent, ready for a task.

> ✅ **Prove your agent works.** Whichever you installed, start it and type a simple question: *"What model are you, and what is 17 times 23?"* If it answers (391), you are connected and ready. Type `exit` (or press Ctrl+C twice) to leave the agent when you want your plain terminal back.

---

## Part 3: The daily loop, and the autonomy dial

Day to day you repeat the plan, act, verify loop. The one setting you must understand is the **autonomy dial**: how much the agent is allowed to do *without stopping to ask you*. This is your main safety control.

```text
  LOW  ◀─────────────────────────────────────────────▶  HIGH
  Ask me first        Auto-edit, ask on            Full autonomy
  (read-only)         risky commands               (no questions)
  safest, slowest     the daily sweet spot         sandbox / CI only
```

- **Ask me first:** the agent proposes every change and waits for your yes. Best when you are learning or the code is sensitive.
- **Auto-edit (recommended for daily work):** the agent makes edits on its own but still asks before risky actions, and you review the diff before saving. Fast and safe.
- **Full autonomy:** the agent acts with no prompts. Only ever use this in a throwaway or sandboxed environment where a mistake cannot hurt anything.

Here is the exact setting in each tool. "Plan mode" is the read-only step where the agent proposes an approach without changing anything.

| | **Claude Code** | **Gemini CLI** | **Codex CLI** |
|---|---|---|---|
| Plan first (read-only) | press `Shift+Tab` to plan mode, or `/plan` | `--approval-mode plan` | type `/plan` |
| Ask me first | `default` mode | `--approval-mode default` | `--sandbox read-only` |
| Auto-edit (recommended) | `acceptEdits` mode | `--approval-mode auto_edit` | `--sandbox workspace-write` |
| Full autonomy (sandbox only) | `auto` mode (it has an extra safety check) | `--yolo` | `--ask-for-approval never` |

> ✅ **The setting to use while learning:** start in **plan mode** for anything non-trivial, read the plan, then let it run in **auto-edit** and review the diff before you keep the change. That combination is fast and very hard to get wrong.

> ❌ **The expensive mistake:** switching to full autonomy on your real project "to go faster", with no safety net. That is how an agent deletes the wrong thing while you are getting coffee. Speed comes from the verify step, not from removing the brakes.

**Always verify.** Whatever mode you use, tell the agent how to check its own work ("run the tests and make sure they pass before you finish"). All three will run your checks, read any failures, and fix themselves. This one habit removes most of the risk of letting the agent act on its own.

---

## Part 4: Give the agent a memory of your project

Out of the box, an agent knows general coding but nothing about *your* project, so it guesses your conventions and often guesses wrong. The fix is a **project memory file**: a plain-text file the agent reads automatically at the start of every session. Same idea in all three tools, just a different filename:

- **Claude Code:** a file named `CLAUDE.md` in your project folder.
- **Gemini CLI:** a file named `GEMINI.md`.
- **Codex CLI:** a file named `AGENTS.md`.

It is an ordinary text file written in **Markdown** (plain text with `#` for headings and `-` for bullet points). You can create it by hand, or let the agent create a first draft for you by typing **`/init`** inside Claude Code or Codex (it reads your project and writes a starter file).

Here is a complete, real example you can adapt. This is what one looks like for our AtlasOS project:

```text
# AtlasOS

## What this project is
AtlasOS is a personal "operating system" run by a small team of AI agents that
cooperate to do knowledge work. I am building it one component at a time as I
work through the Agentic Engineering course.

## How to run and test
- This is an early-stage repo; there is no build step yet.
- When tests exist, run them with: npm test
- A change is not "done" until the tests pass.

## Conventions
- Keep functions small and named clearly.
- Explain anything non-obvious in a short comment.
- Do not delete files I did not ask you to touch.
- Ask before installing new dependencies.
```

> 🔑 **Treat this file as part of the project.** Save it, commit it to git (you will, in the Build), and improve it whenever the agent gets something wrong. A good memory file is the single biggest difference between an agent that fits your project and one that fights it. Keep it short and high-signal; the agent reads it every time, so padding it with fluff just wastes its attention.

---

## Part 5: Growing beyond one task (a preview)

You do not need these yet, but it helps to know they exist, because later units build on them.

- **Running several agents at once.** Using a git "worktree" (a second copy of your project on its own branch), you can have two agents working in parallel without colliding. Codex can even run many tasks in the cloud at the same time. (More in Unit 7.)
- **Automation.** Each agent can run without the chat window, from a script, so a task can run automatically (for example, when you open a pull request on GitHub). (More in Units 6 and 9.)
- **Plugging in tools (MCP).** A standard called the **Model Context Protocol** lets any of these agents connect to outside systems: a database, your issue tracker, a documentation site. (All of Unit 4.)
- **Agent-driven review.** The agent can review code changes and flag problems before you merge them, like a second pair of eyes. (More in Unit 8.)

> ✅ **No grading your own homework.** The best setups use a *separate* reviewer (a second agent or a teammate) to check the first agent's work. A self-check catches mechanical mistakes; an independent review catches the judgment ones. You will set this up properly later.

---

## Key takeaways

1. **Set it up once, properly.** Editor, terminal, Node.js, git, two accounts. You just did the hardest setup in the course.
2. **One habit rules them all:** plan, act, verify. Read the diff; you own every change that you keep.
3. **The autonomy dial is your safety control.** Plan mode plus auto-edit plus a verify step is the daily sweet spot. Full autonomy is for sandboxes only.
4. **A memory file makes the agent fit your project.** `CLAUDE.md` / `GEMINI.md` / `AGENTS.md`, short and committed.
5. **The three agents are interchangeable in shape.** Pick by price and preference; the skills carry over.

## Common pitfalls

- ❌ Skipping the "prove it worked" checks during setup, then hitting a confusing error three steps later.
- ❌ Vibe coding: keeping whatever the agent wrote without reading the diff, because it looked right.
- ❌ Turning on full autonomy on your real project with no test and no sandbox.
- ❌ Skipping the plan step on a big change, then watching the agent confidently build the wrong thing.
- ❌ An empty memory file (the agent does not know your project) or a bloated one (it drowns in detail).
- ❌ Copying tool commands from this page into permanent scripts; they change often, so check each tool's current docs.

---

## 🛠️ The Build: your workstation and your first AtlasOS project

> The hands-on payoff. By the end you will have a real project on GitHub, copied to your computer, with your chosen agent set up and a first task completed and saved. This becomes the home of **AtlasOS**, the project you build a piece of in every later unit. We do every single step together.

### What you will build

A project folder named `atlasos`, created on GitHub and copied to your computer, containing a project memory file you wrote and one small change your agent made, all saved to git and pushed back to GitHub.

### Milestones (in order, each fully explained)

**1. Make sure setup is done.** From Part 0 you should have VS Code, a working terminal, and `node --version` and `git --version` both printing numbers. If not, finish Part 0 first.

**2. Create the project on GitHub.**
   - Go to **[https://github.com](https://github.com)** and sign in.
   - Click the **+** in the top-right corner, then **New repository**.
   - For **Repository name**, type `atlasos`.
   - Leave it **Public** (or Private, your choice), and tick **"Add a README file"** so the project is not empty.
   - Click **Create repository**. You now have a project living on GitHub.

**3. Copy the project to your computer (clone it).** Cloning means downloading your own copy so you can work on it locally.
   - On your new repo's GitHub page, click the green **Code** button and copy the **HTTPS** web address (it looks like `https://github.com/yourname/atlasos.git`).
   - In your VS Code terminal, type the following. The `cd` command moves into your home folder first so the project lands somewhere easy to find:

```text
# Move to your home folder (a tidy place to keep projects).
cd ~

# Download your copy. Paste YOUR address after "git clone".
git clone https://github.com/yourname/atlasos.git

# What you'll see:
Cloning into 'atlasos'...
remote: Enumerating objects: 3, done.
...
Receiving objects: 100% (3/3), done.

# Move into the project folder.
cd atlasos
```

**4. Open the project in VS Code.** Type `code .` in the terminal (that is the word `code`, a space, and a dot, meaning "open this folder"). VS Code reopens focused on your `atlasos` project. You will see the `README.md` file in the list on the left.

**5. Start your agent inside the project.** In the terminal, start your chosen agent from *inside* the `atlasos` folder so it can see your files: type `claude`, or `gemini`, or `codex`. It is now working in your project.

**6. Create the project memory file.** Use the example from Part 4.
   - Easiest way: ask the agent to do it. Type, in plain English: *"Create a file called CLAUDE.md (or GEMINI.md / AGENTS.md) that briefly describes this project: AtlasOS, a personal operating system run by cooperating AI agents that I am building one piece at a time. Note that a change is not done until any tests pass, and that you should ask before deleting files or adding dependencies."*
   - The agent will show you the new file as a diff. Read it. If it looks right, approve it.
   - (By hand instead: in VS Code, click the **New File** icon in the left panel, name it `CLAUDE.md`, paste the Part 4 example, and save with Ctrl+S.)

**7. Run your first real task and review it.** Ask for something small and genuine, for example: *"Add a section to the README titled 'About AtlasOS' with two sentences describing the project."* Watch the agent propose the change as a diff. **Read the diff.** If you are happy, approve it; if not, tell it what to change. This is the plan, act, verify loop in miniature.

**8. Save your work to git and send it back to GitHub.** Your changes are currently only on your computer. These three commands save them and upload them. Run them in the terminal (you can leave the agent first by typing `exit`):

```text
# Stage all your changes (mark them to be saved).
git add -A

# Save them with a short message describing what you did.
git commit -m "Add project memory file and README about section"

# Upload them to GitHub.
git push

# What you'll see after push:
...
To https://github.com/yourname/atlasos.git
   a1b2c3d..e4f5g6h  main -> main
```

   Refresh your repo's page on GitHub: your new file and README change are there. That round trip (change locally, save with git, push to GitHub) is the heartbeat of every project from here on.

**9. Stretch (optional).** Add one more line to your memory file describing a convention you care about, then ask the agent to follow it on a tiny change, and watch it obey. That is you teaching your agent, which is the real skill.

### How you will know you are done

- ✅ `node --version` and `git --version` both print version numbers.
- ✅ Your agent starts inside the `atlasos` folder and answered a question.
- ✅ A `CLAUDE.md` / `GEMINI.md` / `AGENTS.md` file exists in the project and describes AtlasOS.
- ✅ The agent made one change that you reviewed as a diff and approved.
- ✅ You ran `git add`, `git commit`, and `git push`, and the change shows up on GitHub.

> 💡 **If any step felt shaky, that is normal and useful.** Note which one, and that is exactly what to ask your agent (or any model) to explain in more detail. The content here is meant to be complete; reaching for extra help should be about going deeper, not decoding confusion.

---

## Cheat sheet

```text
WORKSTATION (set up once)
  VS Code      -> code.visualstudio.com   (your editor)
  Node.js LTS  -> nodejs.org              (gives you npm)
  git          -> git-scm.com             (tracks changes)
  accounts     -> github.com  +  your agent's account
  prove it     -> node --version ; git --version

THE ONE HABIT
  plan -> act -> verify ; read the diff ; you own what you keep
  verification is the bottleneck: make checking easy

YOUR AGENT (pick one; same shape)
  Claude Code : claude  | CLAUDE.md  | Shift+Tab = plan mode
  Gemini CLI  : gemini  | GEMINI.md  | --approval-mode plan
  Codex CLI   : codex   | AGENTS.md  | /plan

AUTONOMY DIAL
  ask-me-first -> auto-edit (daily) -> full-auto (sandbox only)

THE GIT HEARTBEAT (save + upload your work)
  git add -A
  git commit -m "what you did"
  git push
```

## How this connects to the rest of the course

- **Next, Unit 2 (Prompting and context engineering):** now that you can drive an agent, you learn to *talk to it well*, the difference between a vague request and one that lands. You will practise right inside your new `atlasos` project.
- **Throughout:** every later unit adds one more piece to AtlasOS, and you build all of them with the workstation and agent you set up here. This unit is the tool; the rest is what you make with it.

---

*Unit 1 of the combined path. Fuses the vendor-neutral discipline of Agentic Engineering Module 16 with current, verified, beginner-level setup for three coding agents (Claude Code, Gemini CLI, Codex CLI). Tool commands and model ids change quickly; verify against each tool's current documentation.*

# Unit 1: The Coding-Agent Workflow

> **Course:** Agentic Engineering, a model-agnostic self-paced path *(working title)*
> **Unit 1 of 11:** The coding agent you build everything else with: plan, act, verify, then scale it with one agent of your choice (Claude Code, Gemini CLI, or Codex CLI)
> **Principle (vendor-neutral):** Agentic Engineering Module 16, Working with coding agents
> **The how, across agents:** Claude Code (Anthropic), Gemini CLI (Google), Codex CLI (OpenAI), current practice verified June 2026
> **AtlasOS build:** your repo and dev loop, the launchpad for the whole fleet
> **Estimated time:** 90 to 120 minutes (read plus the build)

---

## In one sentence

Before you build agents, you learn to build *with* one: a coding agent is a tool that reads, writes, and runs code on your machine in a tight plan, act, verify loop, and this unit teaches the durable discipline of driving one well (so you ship reviewed, tested software you would stand behind) and then shows you exactly how to set up and run the same workflow in any of the three leading agents, so you pick the one you like and still understand the rest.

> 🎯 **Where this unit is heading.** The payoff is a **Build** you reuse every later unit: a real repository wired for an agent, with a project memory file, a safe autonomy level, and a self-verifying loop, all committed as the foundation of your north-star project, AtlasOS. Set it up once and every future component is faster to build. Jump to **"The Build"** to see the finish line.

## First-principles companion

> 💡 **The durable ideas behind this unit.** The tools are recent and change monthly; the craft does not. For the timeless, tool-agnostic versions:
>
> - **[Building Effective Agents (Anthropic)](https://www.anthropic.com/engineering/building-effective-agents)** (essay). The workflow-vs-agent distinction that explains what an "agentic coding tool" even is.
> - **[Raising the bar on SWE-bench Verified (Anthropic)](https://www.anthropic.com/research/swe-bench-sonnet)** (essay). How a coding agent is actually built underneath the product: a model plus a bash tool plus an edit tool plus an iterative loop.
> - **[ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)** (paper). The reason, act, observe loop that every one of these agents runs under the hood.

## A few plain-language basics first

- **Coding agent:** a tool you give a task in plain English, and it reads, edits, and runs code for you in a loop, not just answering once. The three in this unit are **Claude Code**, **Gemini CLI**, and **Codex CLI**.
- **CLI (Command Line Interface):** a program you drive by typing in a terminal. All three agents started as CLIs, and all three also run inside editors like VS Code, so your editor does not change, the agent is an extra tool inside it.
- **The loop:** every agent runs the same cycle: read the code, plan, make a change, run a command to check it, read the result, correct course. This is the **plan, act, verify** loop (also called a ReAct loop).
- **Permission / approval mode:** how much the agent is allowed to do without stopping to ask. It ranges from "ask me before every action" to "fully autonomous." You dial it to match the risk.
- **Project memory file:** a file the agent reads at the start of every session so it knows your project's conventions. It is `CLAUDE.md` for Claude Code, `GEMINI.md` for Gemini CLI, and `AGENTS.md` for Codex CLI. Same idea, three names.
- **Worktree:** a second checkout of your repo on its own branch, so two agents can work at once without colliding.
- **MCP (Model Context Protocol):** a standard way to plug external tools and data sources into any agent. All three support it. (Full unit later.)
- **Headless / exec mode:** running the agent non-interactively from a script or CI, with no chat window.

You do not need to memorise these. Each returns the first time it matters.

## Why this unit matters

The rest of this course teaches you to *build* agent systems. This unit teaches you to *use* an agent as your daily tool to build them, because you will build everything else, including AtlasOS, by driving one of these. The meta-skill comes first.

> 🔑 **Agentic engineering, not vibe coding.** "Vibe coding" is accepting whatever the agent produces and hoping it works. **Agentic engineering** is developing software with the assistance of a coding agent while staying fully responsible for the result: you design the task, constrain the environment, and verify the output. The agent is the fastest junior engineer you have ever worked with, and you are still the one who signs off.

Pick this skill up well and the model getting smarter makes *you* faster. Pick it up badly and you ship plausible-looking code you do not understand.

## Learning objectives

By the end of this unit you will be able to:

1. State the agentic-engineering discipline and how it differs from vibe coding.
2. Install, authenticate, and run a first task in at least one of Claude Code, Gemini CLI, or Codex CLI, and explain how the other two do the same.
3. Drive the plan, act, verify loop deliberately, choosing a sensible autonomy level for the risk.
4. Give an agent durable project context with a memory file (`CLAUDE.md` / `GEMINI.md` / `AGENTS.md`).
5. Scale the loop with worktrees, automation, MCP tools, and an agent-driven review step.
6. Stand up the AtlasOS repository and dev loop you will build every later component with.

## Prerequisites

- **Skills that matter:** comfortable in a terminal, basic git (clone, branch, commit, push), and reading code in your main language.
- **Skills you can defer:** none specific to this unit. If git feels shaky, spend an evening on it first, because the whole workflow rides on it.
- **Accounts:** one of an Anthropic plan (for Claude Code), a Google account or Gemini API key (for Gemini CLI), or a ChatGPT plan or OpenAI API key (for Codex CLI). You only need the one you choose.

---

## Part 1: The discipline (the part that does not change)

Every coding agent, today and next year, runs the same underlying loop and asks the same thing of you. Learn the discipline once and it transfers to any tool.

- **Design the task, do not just wish for an outcome.** A good agent task names the goal, the constraints, and how success is checked ("add input validation to the signup form; reject empty fields; the existing tests must still pass"). A vague task gets a vague, confident, wrong answer.
- **Constrain the environment.** Decide up front what the agent may touch and what it must ask about. This is the autonomy dial in Part 3, and it is how you keep speed without losing control.
- **Make the loop self-verifying.** The single biggest lever is giving the agent a way to check its own work: a test suite, a linter, a type checker, a build. An agent that can run your tests will catch most of its own mistakes before you see them.
- **Review like an engineer.** You are responsible for every line that merges. Read the diff. If you would not have approved it from a human, do not approve it from an agent.

> ❌ **A common mistake:** treating the agent as an oracle. When it is wrong, the fix is rarely "argue with it." It is usually a better task description, a tighter constraint, or a verification step it was missing. You are engineering the environment, not pleading with a mind.

> 🔑 **Verification is the bottleneck.** As writing code gets cheap, the scarce skill becomes *checking* it. Every habit in this unit, especially the self-verifying loop and the review step, exists to make verification fast and trustworthy. Hold onto this; it is the spine of the whole course.

---

## Part 2: Pick your coding agent (and meet the other two)

The three leading agents are more alike than different: same loop, same kinds of features, different ecosystems and pricing. Pick by what you already pay for and prefer. You can switch later; the workflow ports.

| | **Claude Code** (Anthropic) | **Gemini CLI** (Google) | **Codex CLI** (OpenAI) |
|---|---|---|---|
| Install | `curl -fsSL https://claude.ai/install.sh \| bash` or `npm i -g @anthropic-ai/claude-code` | `npm i -g @google/gemini-cli` (Node 20+) | `npm i -g @openai/codex` or `brew install --cask codex` |
| Run | `claude` | `gemini` | `codex` |
| Sign in | Anthropic Pro/Max/Team/Enterprise plan, or `ANTHROPIC_API_KEY` | Google account, `GEMINI_API_KEY`, or Vertex AI | ChatGPT plan, or OpenAI API key |
| Open source | no | yes (Apache-2.0) | yes (Rust) |
| Distinctive edge | deepest operational surface; terminal, IDE, CI, web, mobile | large context, Google Search grounding built in, free on-ramp | cloud-parallel agents fused with your ChatGPT plan |

> 💡 **Your editor does not change.** All three run inside VS Code (and JetBrains) through an extension, as well as in a plain terminal. "Use a coding agent" does not mean "leave your editor." It means add an agent to it.

The **core loop is identical** to start: open the agent in your project folder, type a task in plain English, and watch it read files, propose edits as diffs, and run commands. A few specifics worth knowing:

- **Claude Code:** `claude` for an interactive session, `claude "task"` for one shot, `claude -p "..."` headless. `/clear` and `/compact` manage context.
- **Gemini CLI:** `gemini` for the REPL, `gemini -p "..."` headless. It is explicitly built around a "reason and act" loop with built-in file, shell, and web-search-grounded tools.
- **Codex CLI:** `codex` opens a terminal UI; send a message to start. It also lives as a cloud agent at chatgpt.com/codex and answers `@codex` on GitHub.

> ⚠️ **One live caveat (June 2026).** Google has begun moving Gemini CLI's free and individual tiers to a successor called **Antigravity CLI** (announced for 2026-06-18); paid Gemini Code Assist and Cloud customers keep Gemini CLI unchanged, and Antigravity carries the same primitives forward. The workflow below still describes Google's terminal agent faithfully; just expect the name to be in flux. Commands and model ids across all three tools move fast, so verify against current docs.

---

## Part 3: The daily loop, and the autonomy dial

Day to day you repeat one cycle: **plan, act, verify.** Each agent lets you run it at a chosen level of autonomy, from "review every step" to "leave it alone."

**Plan first on anything non-trivial.** A plan step is read-only: the agent researches and proposes an approach before touching code, so you catch a wrong direction cheaply.

- **Claude Code:** press `Shift+Tab` to cycle modes, or `/plan`; plan mode makes no edits until you approve.
- **Gemini CLI:** `--approval-mode plan` (read-only, proposes steps, executes nothing).
- **Codex CLI:** the `/plan` slash command enters a plan-first mode.

**Then act at the right autonomy level.** This is the most important safety control in the unit. The pattern is the same everywhere: a low-trust mode that asks before acting, a middle mode that auto-applies edits but still guards risky commands, and a full-auto mode for throwaway or sandboxed environments.

| Autonomy | **Claude Code** | **Gemini CLI** | **Codex CLI** |
|---|---|---|---|
| Ask before acting | `default` (reads only) | `--approval-mode default` | `--sandbox read-only` |
| Auto-edit, guard the rest | `acceptEdits` | `--approval-mode auto_edit` | `--sandbox workspace-write` |
| Full autonomy (sandboxed) | `auto` (a classifier model blocks risky actions) | `--yolo` / `--approval-mode yolo` | `--ask-for-approval never` (or `--yolo`) |

> ✅ **Recommended default:** run in the auto-edit middle mode with a self-verifying loop, and review the diff before you commit. Reserve full autonomy for disposable sandboxes or CI. Claude Code's `auto` mode adds a separate classifier model that blocks escalations like force-pushes and production deploys, which is the safest way to run unattended; Gemini's `yolo` and Codex's `never` give no such guardrail, so only use them where a bad action cannot hurt anything.

**Verify every time.** Point the agent at your tests or linter and tell it the change is not done until they pass. All three will run your toolchain, read the failures, and self-correct. This single habit removes most of the risk of higher autonomy.

> ❌ **The expensive mistake:** turning on full autonomy on your real repository to "go faster," with no sandbox and no tests. That is how an agent force-pushes to main at 2am. Speed comes from the verifying loop, not from removing the brakes.

---

## Part 4: Give the agent durable memory of your project

Without context, an agent re-learns your conventions every session and gets them wrong. The fix is a **project memory file** the agent reads automatically at the start of every run. Same idea in all three, different filename:

- **Claude Code:** `CLAUDE.md` (a hierarchy: a global one in `~/.claude/`, a project one in the repo, and `CLAUDE.local.md` for personal notes). `/init` scaffolds one from your codebase; it also keeps an automatic per-repo memory.
- **Gemini CLI:** `GEMINI.md`, also hierarchical (global `~/.gemini/GEMINI.md`, project `./GEMINI.md`, even per-subfolder). `/memory show|add|refresh` inspects and edits it.
- **Codex CLI:** `AGENTS.md`, resolved closest-to-current-folder first, with nested per-directory files for subsystems. `/init` scaffolds one.

What goes in it: how to build and test, the conventions you care about, the directories that matter, and the things never to do. Keep it short and high-signal; it is loaded into context every time, so bloat costs tokens and attention.

> 💡 **`AGENTS.md` is becoming a shared convention.** Codex uses it by default, and other tools increasingly read it too. If you want one file that travels across agents, start there and mirror it. Codex even ships an `/import` command to migrate a Claude Code setup.

> 🔑 **Treat the memory file as code.** Commit it, review changes to it, and improve it when the agent gets something wrong. A good memory file is the difference between an agent that fits your project and one that fights it.

---

## Part 5: Scale the loop (parallelism, automation, tools, review)

Once the basic loop is solid, four moves turn one agent into a small engineering operation. Each exists in all three tools.

**Run several at once with worktrees.** A worktree is a separate checkout on its own branch, so parallel agents never collide.
- Claude Code: `claude --worktree <name>` (and subagents can take `isolation: worktree`); background agents via `claude --bg`.
- Codex CLI: the **cloud** agent runs many tasks in parallel, each in its own sandbox with built-in worktrees; you delegate from the CLI, IDE, or GitHub.
- Gemini CLI: no single worktree command, so you run one process per worktree or per folder, and use its subagents for delegation.

**Automate with hooks and headless runs.** Every agent can run non-interactively from a script or CI, and fire scripts at lifecycle points.
- Headless: `claude -p "..."`, `gemini -p "..."`, `codex exec "..."` (with `--json` for a machine-readable stream).
- Hooks: all three let you run a command before or after a tool call, or when a turn ends, to validate, block, or log. Claude Code adds `/loop` (run on an interval) and `/goal` (loop until a condition like "tests pass" holds).

**Plug in tools with MCP.** The Model Context Protocol lets any of these agents talk to external systems (a database, an issue tracker, a docs site) through a standard interface. All three add servers with one command or a config block (`claude mcp add`, `gemini mcp add`, or `[mcp_servers]` in Codex's `config.toml`). You will build a full MCP layer in Unit 4.

**Make the agent review code.** Close the loop with an agent-driven review before you merge.
- Claude Code: `/code-review` (with `--comment` to post on a PR, `--fix` to apply) and `/security-review`.
- Gemini CLI: the official GitHub Action posts PR reviews, or `@gemini-cli /review` on demand.
- Codex CLI: `@codex review` (or automatic reviews) posts a GitHub review surfacing only the high-severity P0 and P1 issues, steered by an `## Review guidelines` section in `AGENTS.md`.

> ✅ **No grading your own homework.** The strongest setups use a *separate* reviewer (a second agent, a review bot, or a teammate) to check the first agent's work. A self-verifying loop catches mechanical errors; an independent review catches the judgment ones.

---

## Key takeaways

1. **Learn the discipline, not just a tool.** Plan, act, verify, and stay responsible for the diff. That transfers to any agent.
2. **The three agents are interchangeable in shape.** Same loop, same feature set, different ecosystems. Pick by preference and price; the workflow ports.
3. **The autonomy dial is your main safety control.** Auto-edit plus a verifying loop plus a reviewed commit is the sweet spot; reserve full autonomy for sandboxes.
4. **Project memory makes an agent fit your code.** `CLAUDE.md` / `GEMINI.md` / `AGENTS.md`, kept short, committed, and improved.
5. **Verification is the scarce skill.** Self-verifying loops and an independent review step are how you trust speed.

## Common pitfalls

- ❌ Vibe coding: merging what the agent wrote without reading it, because it looked right.
- ❌ Running full autonomy on your real repo with no sandbox and no tests.
- ❌ Skipping the plan step on a big change, then watching the agent build the wrong thing fast.
- ❌ An empty or bloated memory file: the agent either does not know your conventions or drowns in them.
- ❌ Letting the agent grade its own homework with no independent review.
- ❌ Hard-coding tool commands or model ids from this page into anything permanent; they change monthly, so verify against current docs.

---

## 🛠️ The Build: your AtlasOS repository and dev loop

> The hands-on payoff. You set up the one environment you will build every later unit inside: the AtlasOS repository, wired for the coding agent you chose, with project memory, a safe autonomy level, and a self-verifying loop. This is the launchpad for the whole fleet (Atlas, Cortex, Scout, Forge, Pulse, Herald, Warden).

### What you will build

A real, committed repository where your chosen agent (Claude Code, Gemini CLI, or Codex CLI) can plan, act, and verify on a task, guided by a project memory file and an agent-driven review step. Proven by three artifacts: a working first task, a committed memory file, and a green review on a small change.

### Milestones (in order, each stands alone)

1. **Create and clone the AtlasOS repo.** Make a new git repository named `atlasos` (or reuse the scaffold in `atlas/`), clone it locally, and confirm your chosen agent launches inside it (`claude`, `gemini`, or `codex`).
2. **Write the project memory file.** Create `CLAUDE.md`, `GEMINI.md`, or `AGENTS.md` (use `/init` if your agent offers it) describing AtlasOS in two paragraphs: what it is (a fleet of cooperating agents, see `atlas/00-company-brief.md`), how to build and test, and the conventions to follow. Keep it short. Commit it.
3. **Run a first real task at a safe autonomy level.** In the auto-edit middle mode, ask the agent to add a small, genuine piece of scaffolding (a README section, a `Makefile` target, or a stub for the orchestrator). Review the diff before committing.
4. **Wire the self-verifying loop.** Add a trivial test or lint command, then run the agent with the instruction that the task is not done until it passes. Watch it run the check and self-correct.
5. **Add an agent-driven review.** Run your agent's review step on the change (`/code-review`, `@gemini-cli /review`, or `@codex review`) and address anything it flags before merging.
6. **Commit it to AtlasOS.** Push the repo with the memory file, the first task, and a note in the README on which agent you chose and why. This is the first real artifact of your north-star build.
7. **Stretch.** Set up one piece of automation: a hook that runs your tests after every edit, or a headless one-liner (`claude -p` / `gemini -p` / `codex exec`) that you could later run in CI. Note how it would slot into a future unsupervised loop.

### How you will know you are done

- ✅ Your chosen agent launches in the AtlasOS repo and completed one reviewed task.
- ✅ A committed `CLAUDE.md` / `GEMINI.md` / `AGENTS.md` describes the project in plain language.
- ✅ The agent ran your test or lint check and self-corrected at least once.
- ✅ An agent-driven review ran on a change before you merged it.
- ✅ It is committed and pushed as the foundation of AtlasOS.

> 💡 If picking an agent felt hard, default to the one whose ecosystem you already pay for. You will understand the other two from this unit, and the workflow ports if you switch.

---

## Cheat sheet

```text
THE DISCIPLINE (does not change)
  plan -> act -> verify ; you own the diff
  agentic engineering = build WITH an agent, stay responsible
  verification is the bottleneck: make checking fast (tests, lint, review)

THE THREE AGENTS (same shape, different ecosystem)
  Claude Code  : claude   | CLAUDE.md  | Shift+Tab modes              | /code-review
  Gemini CLI   : gemini   | GEMINI.md  | --approval-mode              | @gemini-cli /review
  Codex CLI    : codex    | AGENTS.md  | --sandbox / --ask-for-approval | @codex review

AUTONOMY DIAL (pick for the risk)
  ask-before-acting -> auto-edit (+ verify) -> full-auto (sandbox/CI only)
  recommended: auto-edit + verifying loop + reviewed commit

SCALE THE LOOP
  parallel : worktrees / cloud sandboxes / subagents
  automate : headless (-p / exec) + hooks + (Claude) /loop /goal
  tools    : MCP servers (full unit later)
  review   : an INDEPENDENT reviewer, not self-grading
```

## How this connects to the rest of the course

- **Next, Unit 2 (Prompting and context engineering):** you sharpen how you instruct the agent and shape its context, the skills that make every task in this loop land. Your AtlasOS repo is where you will practice them.
- **Throughout:** every later unit is one more AtlasOS component, and you build all of them with the agent and dev loop you set up here. This unit is the tool; the rest is what you make with it.

---

*Unit 1 of the combined path. Fuses the vendor-neutral discipline of Agentic Engineering Module 16 with current, verified practice across three coding agents (Claude Code, Gemini CLI, Codex CLI). Tool commands and model ids change quickly; verify against each tool's current documentation.*

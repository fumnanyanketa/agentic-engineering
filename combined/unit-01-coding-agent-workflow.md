# Unit 1: The Coding-Agent Workflow

> **Course:** Agentic Engineering with Claude, a self-paced path *(working title)*
> **Unit 1 of 11:** Set up the coding agent you build everything else with: plan, review, auto mode, multi-session, and unsupervised runs
> **Sources fused:** Agentic Engineering Module 16 (principles) + Building with Claude Module 4 Lessons 8-10 (implementation)
> **Estimated time:** 90 to 120 minutes (read plus the build)

---

## In one sentence

Before you build any agent, you have to get fluent at *driving* one, so this unit turns "the computer writes code for me" into an engineering discipline: an agent runs tools in a loop toward a goal, you design that loop so it can verify its own work, and you set up Claude Code (Anthropic's coding agent) as the daily environment (plan, review, auto mode, multi-session, hooks) that you will build every later AtlasOS component *with*.

> 🎯 **Where this unit is heading.** The payoff is a **Build** that becomes your factory: the **AtlasOS repo dev loop**, a monorepo wired with conventions (`CLAUDE.md`), a skill, plan-mode review, automated code review, auto mode, parallel work trees, and a feedback hook, all committed. Set up the agent here once and every later unit ships faster. Jump to **"The Build"** to see the finish line.

## First-principles companion

> 💡 **The durable ideas behind this unit.** The Claude-specific tooling moves fast; the craft underneath does not. For the timeless versions:
>
> - **[Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/)** (Simon Willison, living guide). The vendor-neutral playbook: design the loop, sandbox the shell, review every change, keep a personal library of solved problems.
> - **[Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)** (Anthropic, essay). The durable workflow-vs-agent distinction behind what "agentic coding tool" even means.
> - **[Raising the bar on SWE-bench Verified](https://www.anthropic.com/research/swe-bench-sonnet)** (Anthropic, essay). How a coding agent is actually built from first principles: a model, a bash tool, an edit tool, and an iterative loop.

## A few plain-language basics first

- **Coding agent:** software that wraps an LLM (Large Language Model, the AI that predicts text) and gives it a shell and your files, so it can *run* code, not just suggest it. Claude Code is one.
- **Agentic loop:** an agent runs tools in a loop toward a goal, checking results and trying again. Designing that loop is the core skill of this unit.
- **Vibe coding:** prompting for code while you forget the code exists. Fine for a throwaway prototype. The moment you review and test it, it is just software development again.
- **CLAUDE.md:** a small instructions file at the repo root that Claude reads automatically every session. Your hand-written onboarding manual for the agent.
- **Skill:** a folder with a markdown file that teaches Claude how to do one thing, loaded only when relevant ("a lazy system prompt").
- **Hook:** a script on your machine that fires on an agent event (say, after an edit) and can feed back a nudge. Costs zero tokens when it does not fire.
- **Sub agent:** a fresh Claude session with its own clean context window, handed a focused task so only its summary returns.
- **Work tree:** a separate checkout of your repo in its own folder, so parallel agents do not collide.
- **Context window:** the fixed amount of text the model sees at once, measured in tokens. Space is scarce, so do not pay for what you do not use.

You do not need to memorise these. Each returns the first time it matters.

## Why this unit matters

The rest of this course teaches you to *build* agent systems. This unit teaches you to *use* an agent as your daily tool to build them. The two senses of "agentic engineering" meet here: engineering *with* agents, and engineering *of* agents. Get this loop right and every later AtlasOS component ships faster; get it wrong and you spend the course babysitting a tool you do not trust.

> 🔑 **The whole unit in one line.** A coding agent is just an LLM plus a system prompt plus tools, running in a loop pointed at your shell and files. Your job is not to marvel at it, it is to *design the loop* so the agent can verify its own work and you can stand behind every change it ships.

## Learning objectives

By the end of this unit you will be able to:

1. Define agentic engineering precisely and explain why a reviewed, tested change is "software development," not vibe coding.
2. Design an agentic loop with clear success criteria (tests, types, linter) the agent can check itself.
3. Run an agent safely with auto mode, sandboxes, and scoped budgets, and explain the lethal trifecta.
4. Use Claude Code's workflow (plan as reviewable artifact, automated code review, auto memory) to front-load correctness.
5. Pick the right customization (`CLAUDE.md`, skill, hook, sub agent) by asking "what happens at 100,000 of these?"
6. Run several agents in parallel with work trees and agent view without collisions or babysitting.

## Prerequisites

- **Skills that matter:** comfortable with git (branches, commits, PRs), a terminal, and running tests for a small project. A working Claude Code install and one basic session under your belt (Unit 0's environment covers this).
- **Skills you can defer:** the internals of how Claude Code's harness is built. You *drive* the agent here; you build your own harness pieces (hooks, sub agents) in later units.

---

## Part 1: agentic engineering is not vibe coding

The decisive property of a *coding* agent is that it can actually **execute code**. Without that, an LLM's output is an untested guess. Agentic engineering, in Simon Willison's definition, is "the practice of developing software with the assistance of coding agents," resting on one mechanic: the agent runs tools in a loop to reach a goal.

Be precise about the buzzword. **Vibe coding** (Andrej Karpathy's phrase) means prompting for code while you "forget the code even exists," which is fine for a quick, low-stakes prototype. But the moment you review, test, and understand the result, it stops being vibe coding and becomes ordinary software development. Do not let the buzzword talk you out of the discipline.

> ❌ **A common mistake:** treating cheaper generation as a license for lower standards. Writing code is cheap now, but shipping *worse* code is a choice. Treat the time you save as a budget to *raise* the quality bar, not lower it.

A habit you adopt today: **keep a personal library of solved problems**, each backed by a small runnable example. You only ever need to work out a useful trick once; from then on you reuse it, and a reliable agent pattern is to build something new by combining two existing working examples. Start a "TIL" log (Today I Learned) and save reusable snippets now.

---

## Part 2: design the loop so the agent verifies itself

A clear definition of an agent is "something that runs tools in a loop to achieve a goal." The real engineering skill is **designing that loop so the agent can check its own work**. The value you get is hugely amplified by a cleanly passing **test suite** (automated checks that confirm the code does what it should), because the agent can keep trying until the tests pass. Loops work best on problems with **clear success criteria** that reward trial and error: fixing a bug, speeding up slow code, upgrading dependencies.

The Claude Code team turns this into a three-phase workflow whose whole point is **front-loading correctness**, because a long-running agent that starts in the wrong direction burns tokens before you notice. The mindset comes from the **bitter lesson** (general methods beat hand-crafted constraints): constrain a capable model *less*, not more.

| Phase | Goal | The move |
|---|---|---|
| 1. Prompt | Remove ambiguity | Let Claude **interview you** instead of writing the full spec yourself |
| 2. Plan | Check it is what you want | Review the plan as a **rich, clickable artifact**, not a 400-line markdown file nobody reads |
| 3. Verify | Confirm it works | Build verification **into the artifact** so the agent (and CI) can run it |

> 🔑 **The model is probably better at extracting your requirements than you are at defining them.** Your requirements are *latent*: you know it when you see it but struggle to say it up front. Name the domains you care about (audience, edge cases, look and feel) and refer to the **ask-user-question tool**, one area at a time, and Claude interviews you turn by turn into a more complete spec than a blank-page brain dump.

> ❌ **The non-prompt:** "make it better." No direction, nothing to extract. And reviewing a 400-line markdown plan you (and your team) will never actually read: a plan nobody reads cannot be checked.

For phase 3, the deepest idea is to **publish the artifact's state where an agent can read it** as a clean contract (for a web app, via DOM data attributes) rather than making the agent reverse-engineer internals. Then the *same* verification runs three ways: a human dashboard, the agent driving a browser, and a headless `verify` command in CI. Verify the *contract*, not just whether the app happens to look fine, and record the run as evidence so humans need fewer touchpoints.

> ✅ **Pro tip:** the QA you cannot outsource. Run the tests *first* for a green baseline before you change anything. Use red/green TDD (write a failing test, then make it pass). And never assume code an LLM wrote works until it has actually run, because passing tests do not guarantee the feature behaves as intended.

---

## Part 3: run it safely, and customize it to scale

An agent with shell access has been described as "an LLM wrecking its environment in a loop," so safety is structural, not optional.

**Auto mode** is the feature that earns your time back. Instead of stopping for every "can I read this file?", it runs a classifier on each action that would normally need approval:

```text
1. Is this action DESTRUCTIVE?        (Will I regret this? e.g. deleting data)
2. Does this look like a PROMPT INJECTION?  (Is something trying to hijack me?)

Both checks pass -> Claude acts and keeps going.
A check fails    -> Claude first tries a safe workaround.
No safe path     -> only THEN does it stop and ask you.
```

(A **prompt injection** is malicious text, in a file or web page, trying to trick the agent.) Auto mode does not blindly say yes; it says yes to the safe, boring things and interrupts only for what genuinely warrants a human. It costs extra tokens for the classifier, and is safe to run unsupervised only when you also **contain the blast radius**.

> 🔑 **The safety rules that make "dispatch and walk away" real.** Run auto mode inside a **sandbox** (an isolated, throwaway environment such as a Docker container). Give the agent credentials only for test or staging, and if a credential can spend money, set a tight budget cap. And never hand an autonomous agent your secrets, untrusted input, and unrestricted internet access all at once: that is the **lethal trifecta**.

Now make the agent good at *your* code base. The fastest way is not a smarter model, it is a **tighter feedback loop**: wire up the linters and type checkers you already have so the agent gets the equivalent of an editor's "red squigglies" (overridable nudges that make it think twice without blocking it). Knowledge cannot be trained in cheaply (fine-tuning on narrow data can *increase* hallucinations and is outpaced by the next base model), so it goes in as text via **in-context learning**: `CLAUDE.md`, skills, and tools.

Every customization has to fit a **fixed context window** that is *not* growing even as models get smarter, so the central rule is **don't pay for what you don't use**. Daisy Holman's scaling test: picture 100,000 of each customization and ask whether your context survives.

| Building block | Cost when unused | Best for |
|---|---|---|
| **Hook** (script fires on an event) | Zero (runs off-context, returns nothing) | Feedback loops, linter "red squiggly" nudges. The only true zero-overhead abstraction. |
| **Skill** (folder + markdown) | Small (one-line description always loaded) | Teaching Claude how to use an existing CLI or procedure |
| **Sub agent** (separate session) | Small description + its own window | Offloading big reads to keep the main context clean |
| **MCP** (server exposing tools) | High (name + description + schema in the prompt) | Public integrations and services you do not own (Slack, email, dashboards) |

> ✅ **Pro tip:** prefer a **skill** over wrapping your own CLI in an MCP server. Claude Code already has a shell, so a skill that just tells it how to call the existing tool is cheaper. And prefer **nudges that scale with intelligence** over hard **blocks that compensate for a lack of it**, because a smarter model uses a hint well but chafes against a cage.

> 💡 **CLAUDE.md vs memory.** `CLAUDE.md` is the onboarding manual *you* write by hand. **Auto memory** is the notes *Claude* takes automatically as it works (saved to `memory.md`, kept small as an index, loaded on demand, audited with `/memory`). One is a manual; the other is note-taking. Resist the request to load a `CLAUDE.md`-style block unconditionally from every plugin: it looks cheap and is one of the most expensive abstractions possible.

---

## Part 4: parallel work, and not babysitting

Once you trust your loops, you stop sitting and watching one session and start dispatching work that runs on its own. But know the real bottleneck: **AI-generated code still has to be reviewed, and how fast you can review is the limit.** So parallelize the *safe* work first (research and "scout" tasks that change nothing, and tasks from a clear spec you wrote, which are cheap to review), and run riskier work asynchronously inside a sandbox.

The Claude Code tooling makes this practical:

```text
claude --worktree     # isolated repo checkout so parallel Claudes don't collide
claude agents         # agent view: see every session by status, run them in background
                      #   (enter = open a session, space = quick prompt without entering)
/loop 10m <prompt>    # re-run a prompt on a schedule (e.g. "babysit my open PRs")
/remote-control       # continue a session from your phone or a browser
```

A **work tree** is a second checkout of the repo in its own folder; put one Claude on each and they stop stepping on each other, exactly like human colleagues each with their own checkout. **Agent view** shows every session by status (working, blocked, done) and runs them in the background. **Remote control** surfaces sessions on your phone for a 30-second check-in after dinner. And `/loop` is a game-changer for chores: even if CI takes two hours, leave it overnight and Claude keeps fixing failures until they are green.

> 🔑 **Review discipline is the one thing you never outsource.** The cardinal anti-pattern is filing a pull request (a proposed code change) containing code you have not read yourself, because then you add nothing the next person could not get by prompting an agent themselves. Keep PRs small, include proof you tested the change, and read the agent's PR *description* too, since agents write convincing summaries that can paper over what the code really does.

Claude Code productizes the review itself with **code review** (run `/ultra-review`, or install the GitHub app so every new PR is reviewed automatically). It is multi-agent (a team of agents each check a different concern: errors, bugs, security) and multi-phase (a second pass re-checks every finding against your actual code to filter false alarms), so logical problems that would take hours surface in minutes. **Routines** go one step further: trigger Claude on a schedule, a webhook (a new GitHub issue or PR), or an API call, running *in the cloud* with your machine off. Resist the multi-agent hype, though: a single capable agent can usually debug and review its own output if it has enough context, so use **sub agents** for scoped reads, not a swarm of specialists.

---

## Key takeaways

1. **Driving the agent is the meta-skill.** A coding agent runs tools in a loop; reviewed and tested output is software development, not vibe coding.
2. **Design the loop to self-verify.** Clear success criteria (tests, types, linter) let the agent keep trying until it passes. Run tests first; build verification into the artifact.
3. **Constrain capable models less.** Let Claude interview you, review the plan as a clickable artifact, and front-load correctness before a long run.
4. **Safety is structural.** Auto mode plus a sandbox plus scoped budgets makes "dispatch and walk away" real. Never combine secrets, untrusted input, and open internet.
5. **Pick abstractions that scale.** Hooks cost zero unused; skills and sub agents carry a small tax; MCP is for third-party services. Picture 100,000 of each.
6. **Parallelize the safe work; review is the bottleneck.** Work trees, agent view, `/loop`, and automated review let you stop babysitting, but you still read every change.

## Common pitfalls

- ❌ Pushing unreviewed code onto collaborators (you are accountable, including for the AI-written PR text).
- ❌ Trusting a passing test suite as proof the feature truly works without driving the running software yourself.
- ❌ Running a shell-capable agent outside a sandbox, or using auto mode with real credentials or a real budget.
- ❌ Running parallel sessions on one repo *without* work trees, so they overwrite each other's files.
- ❌ Wrapping an existing CLI in an MCP server for your own developers when a skill would be simpler and cheaper.
- ❌ Caging the agent with hard blocks when an overridable nudge would scale better with a smarter model.
- ❌ Over-engineering a swarm of specialist sub agents when one capable agent with enough context would do.

---

## 🛠️ The Build: the AtlasOS repo dev loop

> The hands-on payoff. You are setting up the coding agent itself as the environment you build every later AtlasOS component *with*. The project here is secondary; the *dev loop* is the deliverable. This fuses Module 16's verifiable-loop discipline with the Claude Code workflow (Lessons 8-10), and ends by committing the setup to your AtlasOS repo.

### What you will build

The **AtlasOS monorepo** wired so the agent can build it with as little babysitting as possible: a `CLAUDE.md` charter, one skill, plan-mode review, a feedback hook, auto mode, parallel work trees, and an automated code-review path, proven by one real change shipped through the full loop.

> 🎯 **Pick your repo.** Use the AtlasOS repo you started in Unit 0 (or scaffold a fresh monorepo with folders for the named agents: `orchestrator/` for Atlas, `memory/` for Cortex, `agents/` for Scout and Forge, `evals/` for Warden). It needs a linter or type checker you can run and a GitHub remote so you get real PRs.

### Milestones (in order, each stands alone)

1. **Vanilla baseline and the access audit.** Run Claude Code on the repo with no customization and ask for one small change. Note where it struggles or asks for context it could not find. For 30 minutes of real work, log every time you alt-tab away from the agent; that list is your customization backlog.
2. **Write the charter (`CLAUDE.md`).** Capture 3 to 5 conventions a newcomer would not know (the AtlasOS folder map, the test command, the "build for the next model, thin scaffolding" principle, the named agents). This is the manual you hand Claude on day one, kept short.
3. **Add a skill and a feedback hook.** Write one **skill** that teaches Claude how to run an existing repo script or CLI, and confirm it triggers only when relevant. Add a **post-edit hook** that runs your linter or type checker and feeds back an *overridable nudge*; confirm it returns nothing (and costs nothing) on irrelevant files. These are your "red squigglies."
4. **Run the verifiable loop in auto mode.** Pick one real change (Warden's first eval stub, a Scout helper). Run the tests *first* for a green baseline, have Claude write a failing test, turn on auto mode (in a sandbox, scoped credentials), and let it make the test pass untouched. Then drive the running result yourself before you accept it. Review the plan as a reviewable artifact, not a wall of markdown.
5. **Go parallel, then review.** Start two features in two `claude --worktree` checkouts, watch both in `claude agents`, and confirm no file collisions. Open a PR and run `/ultra-review` (or install the GitHub app). Read every change and the PR description yourself, then **commit the whole dev-loop setup to the AtlasOS repo**.
6. **Stretch.** Add a **sub agent** for a big read ("summarize how the orchestrator wires together") to keep the main context clean. Set a `/loop` to babysit CI or open PRs overnight. Add a **routine** that posts a review on every new issue, running in the cloud. Fill in a scaling table: for each customization, its token cost when unused and what happens at 100,000.

### How you will know you are done

- ✅ `CLAUDE.md`, one skill, and a post-edit hook all live in the repo, and the hook returns nothing on irrelevant files.
- ✅ One real change went through the full loop: green baseline, failing test, auto-mode fix in a sandbox, hands-on manual check, reviewed PR.
- ✅ Two Claudes worked the same repo in **parallel work trees** with no collisions, both visible in agent view.
- ✅ A PR was **auto-reviewed** and you read every change and the description before accepting.
- ✅ The whole dev-loop setup is **committed to your AtlasOS repo**.

> 💡 **The real test:** after setup, how little do you have to do? Every milestone removes one reason to sit and watch a session, and every later unit builds on this loop.

---

## Cheat sheet

```text
THE DISCIPLINE
  Coding agent = LLM + system prompt + tools, looping over your shell and files.
  Reviewed + tested = software development. Unreviewed prototype = vibe coding.
  Design the loop so the agent verifies itself (tests, types, linter, browser).
  Keep a personal library of solved problems (TIL log + runnable snippets).

THE WORKFLOW (front-load correctness)
  1 PROMPT  -> let Claude interview you (name domains + ask-user-question tool)
  2 PLAN    -> review as a clickable artifact, not 400 lines of markdown
  3 VERIFY  -> build it into the artifact; run the SAME checks 3 ways
              (human dashboard · agent-from-browser · headless CI). Record evidence.
  Run tests FIRST · red/green TDD · drive the running software yourself.

SAFETY
  auto mode = classifier (destructive? injection?) -> safe workaround -> only then ask
  Sandbox the shell · scope credentials to test/staging · cap any budget
  Lethal trifecta: never combine secrets + untrusted input + open internet

CUSTOMIZE (imagine 100,000 of them; context window is FIXED)
  Hook ........ zero cost unused .......... feedback loops / red squigglies (scales best)
  Skill ....... small always-on desc ...... teach Claude your CLIs/procedures
  Sub agent ... small desc + own window ... offload big reads, keep main context clean
  MCP ......... full name+desc+schema ..... public/3rd-party services (Slack, email)
  CLAUDE.md = your manual ; memory.md = Claude's auto notes. Nudges over cages.

PARALLEL (stop babysitting; review is the bottleneck)
  claude --worktree  ·  claude agents  ·  /loop <interval> <prompt>  ·  /remote-control
  /ultra-review (multi-agent, multi-phase) · routines (cron/webhook/API, in the cloud)
  Parallelize the SAFE work first. Read every change and every PR description.
```

## How this connects to the rest of the course

- **Next, Unit 2 (Prompting and context):** the "interview me" and "name the domains" prompting here becomes the deliberate prompt-and-context engineering you apply to every AtlasOS agent.
- **Throughout:** this dev loop is the factory. Warden's evals (Unit 8) grow from the verifiable-loop discipline, the orchestrator and unsupervised runs (later units) extend auto mode and routines, and every component you ship is built *with* the agent you set up here.

---

*Unit 1 of the combined path. Fuses the vendor-neutral principles of Agentic Engineering Module 16 with the Claude-specific implementation of Building with Claude Module 4 (Lessons 8-10). Commands, flags, and model ids are illustrative; check the current docs and changelog, since these features move fast and some are in preview.*

# Module 4 · Lesson 10: Beyond the Basics with Claude Code

> **Course:** Building with Claude, a self-paced course
> **Module 4:** Claude Code, your everyday agent
> **Speaker:** Daisy Holman, Engineer on the Claude Code team, Anthropic
> **Source talk:** [Beyond the basics with Claude Code](https://www.youtube.com/watch?v=tuY2ChJIx48) · [full transcript](../../transcripts/code-with-claude-2026-london-2026/02_beyond-the-basics-with-claude-code.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

To make Claude Code do real software engineering (not just toy programming), you give it the same access, knowledge, and tooling you have, and you customize it with abstractions that scale, because every customization has to fit inside a fixed context window, so you want ones that cost almost nothing when they are not being used.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you build a **Scaling Harness Lab**: a small, realistic repo that you wire up with the four plugin building blocks (MCP, skills, hooks, sub agents), then deliberately stress test which ones survive when you imagine thousands of them. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section near the end, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[Effective context engineering for AI agents (Anthropic)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)** (essay). Treats context as a finite "attention budget" and shows how to engineer the smallest high-signal token set, the lesson's central design rule, framed tool-agnostically.
> - **[The Illustrated Transformer (Jay Alammar)](https://jalammar.github.io/illustrated-transformer/)** (essay). Explains keys/queries/values from the ground up, so you understand why a KV cache exists and why editing early tokens forces expensive recomputation.

## A few plain-language basics first

This lesson uses some everyday AI and engineering terms. Here they are in simple words, so nothing below is confusing:

- **Agent:** an AI that takes a series of actions on its own toward a goal, instead of answering in one shot. Claude Code is an agent that can read files, run commands, and edit code.
- **Agentic harness:** all the code and settings wrapped around the model that turn it into a working agent: the loop that calls the model, the tools it can use, and the information it sees. Claude Code is one such harness. The model is the brain, the harness is the body.
- **Context window:** the total amount of text (the prompt, the files, the tool descriptions, the conversation so far) that the model can "see" at once. It is measured in **tokens** (a token is roughly three quarters of a word). It is a fixed size, so space is precious.
- **System prompt:** the always present block of instructions and tool descriptions at the very start of the context window. Everything here is loaded every single time, so it is expensive.
- **MCP (Model Context Protocol):** an open standard for connecting an agent to an outside service (Slack, email, a database) by running a small "server" that exposes tools. More on this in Part 4.
- **Skill:** a folder with a markdown (text) file that teaches Claude how to do one specific thing, loaded only when needed.
- **Hook:** a small script on your computer that runs automatically when something happens in the agent (for example, right after Claude edits a file).
- **Sub agent:** a separate Claude session that the main Claude can hand a focused task to, with its own separate context window.
- **Monorepo:** one giant code repository that holds many projects and is shared by a large number of engineers. "Repo" is short for repository, the folder tracked by version control.
- **In context learning (ICL):** teaching the model by putting text into its context window, rather than by retraining the model itself. Daisy jokes it is "a fancy word for text files."

You do not need to memorise these. Every term is also explained again the first time it appears below.

## Why this lesson matters

Out of the box, Claude Code "just sees a repo and a shell" (a shell is the command line where you type commands). That is plenty for what Daisy calls a **zero to one project**: a brand new thing with no history, no conventions, and no other people depending on it. But most professional software engineering is the opposite. There are old decisions, internal jargon, external teams who depend on your code, and most of the important context lives outside the source code entirely: in Slack threads, design docs, emails, and dashboards.

Daisy's one big thesis is blunt:

> "If Claude can't do everything you can do, it can't do your job with you." (Daisy Holman)

Your job, she argues, is now to "make little clones of yourself" so you can scale your work across many agents. This lesson is about giving those clones everything they need, and doing it in a way that does not blow up your context window.

## Learning objectives

By the end of this lesson you will be able to:

1. Identify the three things an agent needs to do real engineering work: **access**, **knowledge**, and **tooling**.
2. Explain why the context window is a hard, fixed constraint, and why **not paying for what you do not use** is the central design rule.
3. Tell the four plugin building blocks apart (**MCP, skills, hooks, sub agents**) and judge how well each one **scales** to thousands of instances.
4. Set up a tighter feedback loop for your agent (the "red squigglies" idea) using hooks.
5. Use parallel workflows (git worktrees, loops, agent views) to stop babysitting one agent at a time.

## Prerequisites

- You have used Claude Code at least a little: you can start a session, ask it to make a change, and approve a tool call.
- Helpful but optional: Module 2 (Core skills) for prompting and context basics.
- Lessons 11 and 12 of this module go deeper on the proactive and parallel workflows touched on at the end here.

---

## Part 1: the three things an agent needs (access, knowledge, tooling)

Daisy frames every customization as filling one of three gaps.

| Need | What it means | Why vanilla Claude Code lacks it |
|---|---|---|
| **Access** | The ability to reach the places where your real work lives. | Out of the box, Claude sees only the repo and the shell, not Slack, email, dashboards, or design docs. |
| **Knowledge** | Your code base's conventions, internal vocabulary, institutional memory, and recent changes. | This cannot be trained into the model, so it has to be supplied as text. |
| **Tooling** | The equivalent of an IDE for an agent: linters, type checkers, completion, and "nudges." | Out of the box Claude has a plain edit tool and not much else. |

### Access: connect Claude to everywhere you work

The source code rarely explains the **why** of a change. That "why" is in your head, and it got there from somewhere Claude cannot see. Daisy's list of things worth connecting:

- **Team chat (Slack):** where decisions are actually made. If Claude can read the thread, it understands why one approach was chosen over another.
- **CI and CD:** the systems that automatically build and test (CI, continuous integration) and deploy (CD, continuous delivery) your code. Daisy is emphatic: "You should not be fixing CI failures yourself at this point in time."
- **Dashboards:** when production breaks, you need to pull in a lot of information fast, and you are competing with companies doing it agentically.
- **Internal documents:** design docs, run books (step by step recovery guides), and meeting notes.

> 💡 **A concrete habit from the talk.** Daisy records and transcribes meetings, then feeds the notes to Claude and asks: "Is there any low hanging fruit from this meeting that you can address?" The result is "two or three PRs per meeting." (A **PR**, or pull request, is a proposed code change submitted for review.)

> 🔑 **The one day test.** Try to do a full day of work without leaving the Claude Code terminal. Every time you have to alt tab to another tool and copy paste into Claude, write it down. At the end of the day, connect Claude to all of those things. As Daisy puts it, "the gap is much bigger than you notice until you make all of the connections."

### Knowledge: you cannot train it in, so it goes in context

You might wish you could **fine tune** a model (retrain it on your private data) to know your code base. Daisy advises against it for this purpose, for two reasons. First, research from late 2025 suggests fine tuning on narrow, specialized information can actually cause more **hallucinations** (the model stating something untrue as if it were true). Second, frontier models improve so fast that fine tuning is rarely cost efficient: by the time you finish, there is a better base model.

So all your knowledge customization happens through **in context learning**: skills, tools, and `CLAUDE.md` (a special markdown file Claude reads automatically). The upside is that you never have to touch model weights, and everything is just text files, so it is easy to start. The catch, which the rest of the lesson is about, is fitting it all into a fixed context window.

> 🔑 **The bitter lesson.** General AI beats specialized AI in the long run. So instead of trying to bake your specifics into the model, give a general model the right text at the right time.

### Tooling: build the "red squigglies" for your agent

Think back to writing code by hand. You had syntax highlighting, code completion, and **red squigglies**: the little red underlines that appear when you misspell a variable or pass the wrong number of arguments. Claude has almost none of this by default. Its edit tool is so basic that Daisy compares it to **ed**, an ancient line editor from before modern text editing existed.

The key insight is what red squigglies do to your brain: they **nudge** you to think twice without **blocking** you. You can ignore one when you know better (for example, you will define that function later).

> 🔑 **The fastest way to make your agent better at your code base is not a smarter model, it is a tighter feedback loop.** And most of the pieces already exist: you already have linters and type checkers from setting up environments for human developers. You just need to hook them up.

Daisy splits tools into two kinds, and this distinction matters:

| Kind of tool | What it does | Example | Does it scale with smarter models? |
|---|---|---|---|
| **Scales with intelligence** | An overridable nudge. The smarter the model, the better it uses the hint. | A reminder that "this is a generated file, do not commit it" | Yes. A smarter model uses the nudge more wisely. |
| **Compensates for lack of intelligence** | A hard block that forces a rigid behavior. | Forbidding Claude from ever using an undefined variable | No. It forces an unnatural order of work and limits a capable model. |

> 💡 Daisy asked Claude for examples of tools that compensate for a lack of intelligence (the bad kind). Claude replied that it did not like having its tools taken away. The lesson: prefer nudges over cages, and let the model's growing intelligence work for you.

---

## Part 2: the context window is the real constraint

Every customization you add, in some form, has to fit in the context window. And here is the surprising part: context windows are **not** growing much. A year ago the frontier was mostly 1 million token models with a few 200,000 token ones. Today (with Opus 4.7 at roughly 1 million tokens) the frontier is about the same size, even though the models are far more capable in every other way.

> 🔑 **You are aiming at a fixed target.** The models keep getting smarter, but the space you have to put information into stays roughly constant. So getting good at context engineering is a durable skill, not a temporary workaround.

Daisy offers two memorable analogies.

**Running npm on an Arduino.** An Arduino is a tiny computer with very little memory. Trying to install lots of packages on it would leave no room for your own code. The context window is the same: be ruthless about what goes in, and put the smallest useful version of each thing.

```text
Mental model: the context window is a tiny memory budget.

  [ stable, shared stuff ]  <- put at the FRONT (cached, cheap to reuse)
  [ ...                  ]
  [ volatile, per-task   ]  <- put at the END (cheap to swap out)
```

**Don't pay for what you don't use.** This is a famous C++ principle (the zero overhead abstraction principle), and Daisy says it is not just a nice to have here, it is a hard limit. Since the window will not get bigger, the only way to fit more is to stop spending tokens on things the model is not currently using.

### The twist: the KV cache makes early changes very expensive

There is a second constraint that breaks the simple "just evict what you haven't used" idea. The model uses a **KV cache** (key value cache): saved internal computation for the tokens it has already processed, so it does not have to redo the work. Cached tokens are cheap. Uncached tokens can cost about **ten times** as much.

The catch: if you change something **early** in the prompt, you invalidate the cache for **everything after it**. So you cannot just swap a rarely used tool out of the tools block near the top, because that would force the model to recompute the entire rest of the context at the expensive, uncached rate.

> 🔑 **Layout rule.** Put **stable, shared** information at the very front (it stays cached). Put **volatile, per task** information near the end (you can swap it cheaply). Early LRU style eviction (LRU means "least recently used") made sense when context windows were tiny, but not anymore.

---

## Part 3: the four plugin building blocks, and which ones scale

A **plugin** in Claude Code is a packaged bundle of customizations. Daisy examines four building blocks (she calls them primitives) and asks one question of each: **what happens if you have 10,000 or 100,000 of them in a giant monorepo?** That is the real test of whether an abstraction scales. Throughout, "pay" means cost in **context window space**, not just money.

> 🔑 **The scaling question.** A great abstraction is one whose cost stays near zero when it is not being used. Daisy wants you to picture 100,000 of each thing and ask: does my context window survive?

### Block 1: MCP (Model Context Protocol)

**MCP** is a standard for connecting an agent to an outside service through a small server that exposes tools. It was designed in an earlier era for chatbots that have no shell, no file access, and cannot run commands, so MCP injects tools and handles things like authentication (proving who you are) and transport for you.

**When it is the right choice:** when you ship a public integration to people who may not be technical, or when you need to connect to a service you do not own. You will still need MCP servers for **Slack, email, dashboards**, and the like.

**When it is the wrong choice:** Claude Code **does** have a shell. So if you already have a command line tool (a CLI), wrapping it in MCP usually makes little sense for your own developers. A **skill** that just tells Claude how to use the existing CLI is easier.

**Does it scale?** Poorly, by default. Each tool's name, description, and **schema** (the structured description of its inputs) must sit in the system prompt so Claude knows how to call it. With even 20 servers of 15 tools each, "most of your context window starts to be tool definitions."

> 💡 **Tool search** is a newer approach that helps. Only the tool **names** go in the system prompt, plus one tool Claude can call to **search** for the right tool and load its full description later (this is called **lazy loading**). The limit: unless the user says something specific like "Slack," Claude may not know it should search, so generic tools (edit, bash) still need full descriptions up front. "There is not a free lunch here. It is a slightly less expensive lunch."

### Block 2: skills

A **skill** is, in Daisy's words, "a lazy system prompt." It is just a folder with a markdown file and an optional set of scripts. A one line description in the file's **front matter** (the small header at the top) goes into the system prompt; the full file is loaded only when Claude decides it is relevant.

```text
my-skill/
  SKILL.md        <- one-line description in front matter + full instructions
  helper.py       <- optional scripts and resources
```

**Does it scale?** Mostly. The **body** is pay per use (good), but the **description is always loaded**, so you always pay a small fraction. Reliably triggering a skill can still take a 300 to 400 token paragraph, and the shorter you make the description, the less reliably it triggers without the user naming it. There is also no built in way yet to nest **sub skills** hierarchically (Daisy hints an announcement is coming). So skills "kind of scale," but a monorepo with 100,000 skills strains them.

> ❌ Because skills are so easy to create, quality control becomes a real problem in a large monorepo. Easy to make also means easy to make badly.

### Block 3: hooks

A **hook** is a script on your computer that Claude Code runs when a specific event happens in the agent loop (for example, right after a tool is used). Claude passes the script some JSON (a structured text format), and the script can return JSON deciding whether to insert anything into the context window.

```text
Event happens (e.g. file edited)
        |
        v
  your hook script runs ON YOUR MACHINE  (zero tokens)
        |
        +-- returns nothing  -> context window untouched (you pay nothing)
        +-- returns text     -> a small nudge is inserted ("this is a generated file")
```

**Does it scale?** This is the one true zero overhead abstraction in the list. If you have 100,000 hooks and 99,995 of them do not match the current situation, they simply run, return nothing, and cost you no tokens at all. Your only limit is your computer's speed. "You have taken a very constrained resource and blown it out into a much less constrained resource."

This is exactly where Daisy's **red squigglies** live: run a linter or type checker after an edit, and feed back an overridable nudge.

> ❌ Hooks are not magic. They are not the most intelligent option, so you often end up parsing words or matching patterns out of commands, which has limits. You can use a sub agent inside a hook to decide whether to inject something, but that gets expensive again.

### Block 4: sub agents

A **sub agent** is a separate Claude session that the main Claude hands a focused task to. Its description goes in the parent system prompt; its own instructions and work happen in a **separate context window**. The parent only pays (in its own window) for the tool call and the result that comes back.

**Why that is powerful:** a sub agent can read 50 files so the main loop does not have to, keeping the main context clean.

**Does it scale?** Same catch as skills: each sub agent's one line description still sits in the parent prompt, so 100,000 sub agents means 100,000 one liners. Anthropic is experimenting with doing better here too.

### The abstraction Daisy refuses to add (and why)

The most frequent plugin request she gets is: "Why can't my plugin provide a `CLAUDE.md` file?" That is, a chunk of text that loads **unconditionally** into the user's context whenever the plugin is enabled.

She pushes back hard, and after Part 2 you can see why. It **looks** cheap (it is one little file), but it is one of the most expensive abstractions possible: every plugin would add one, and "that doesn't scale, it really doesn't scale, and it looks like it does." The compromise: if you truly need it, you can return text from a **session start hook**. That makes the cost visible and deliberate, because it is obvious you are charging every user something on every session.

> 🔑 **Think of plugins as a context engineering primitive,** which Daisy describes as "another way of saying text file, but with more funding." They are designed, evaluated, and iterated on. That is different from **memory**, which is low quality, low cost, short lived information an agent jots down on the fly. Memory has its place, but it is not the tool for deliberate, scalable customization.

| Building block | Token cost when unused | Scales to 100,000? | Best for |
|---|---|---|---|
| **MCP** | High (name + description + schema in system prompt) | Poorly (tool search helps a bit) | Public integrations; services you do not own (Slack, email) |
| **Skill** | Small (one line description always loaded) | Mostly | Teaching Claude how to use existing CLIs and procedures |
| **Hook** | Zero (runs off context) | Yes | Feedback loops, linters, "red squiggly" nudges |
| **Sub agent** | Small (one line description) plus a separate window | Mostly | Offloading big reads and focused tasks to keep the main context clean |

---

## Part 4: working in parallel, and not babysitting

The last stretch of the talk is about two themes: **asynchrony** (start work, walk away, come back later) and **parallelism** (run several agents at once). Together they mean you become a kind of technical lead managing multiple Claudes, and the hard part becomes **context switching** between them efficiently.

### Git worktrees: one checkout per agent

A **git worktree** is simply a second (or third, or tenth) checkout of the same repository in a different folder on your machine. Git is clever about sharing storage so you do not waste disk space. Put a separate Claude Code instance on each worktree and the agents stop stepping on each other, exactly like human colleagues each having their own checkout.

Daisy keeps long lived worktrees that each track the upstream main branch, with a persistent agent that "owns" each directory. Because they are long lived, she does not have to re run setup (like `npm init`) every time.

> 💡 **A tiny trick that pays off.** Rename your sessions and set a color (`/color`). Color triggers memory efficiently, so it acts as "syntax highlighting for humans," letting you click your brain back into what a session was doing. Rename helps too, especially if you are colorblind.

### Let agents talk, loop, and run with fewer prompts

- **Claude to Claude messages.** A `send message` tool lets one Claude pass information to another running on the same account (with your permission). One of the places you now work is another Claude, so that Claude needs access to the relevant conversation.
- **`/loop`.** Runs a prompt every fixed interval (say, every 10 minutes). Internally the tool is called `crontool` (after **cron**, the classic Unix job scheduler), and `/loop` is the friendly command. Claude can turn the loop off when the prompt is no longer relevant.

```text
/loop 10m babysit my open PRs
# Every 10 minutes Claude wakes up, runs this prompt, and stops when done.
```

> 💡 Daisy calls **babysitting PRs with `/loop`** a game changer. Even if your CI takes two hours, you can leave it overnight and Claude will keep fixing CI bugs until they are green.

- **Auto permissions mode.** Instead of approving every tool call, auto mode uses a classifier agent plus an adversarial checker that inspects each tool call for anything dangerous. This is what makes loops, agent teams, and overnight work usable. It is not "dangerously skip permissions." It costs extra tokens (Daisy roughly estimates on the order of 30 to 40 percent more, and says not to quote her on the exact figure), and the team is working to lower it.
- **Claude Agents view and Remote control.** A single view shows every running agent, which are working and which are blocked, so you can peek in, jump in, or start new sessions. **Remote control** surfaces sessions on your phone and desktop, perfect for a 30 second check in after dinner to make sure nothing is stuck.

> 🎯 **Daisy's three take homes:** give Claude **access**, **mind the box** (respect the context window), and **pick abstractions that scale**. Picture 100,000 of each customization before you commit to it.

---

## Key takeaways

1. **Access, knowledge, tooling.** If Claude cannot reach what you reach, it cannot do your job with you. Connect it to Slack, CI/CD, dashboards, and docs.
2. **The context window is fixed and not growing.** Getting good at fitting information into it is a durable skill, not a temporary hack.
3. **Don't pay for what you don't use.** And because of the KV cache, put stable shared things at the front and volatile per task things at the end.
4. **Hooks are the only true zero overhead abstraction.** They cost nothing when they do not fire, so 100,000 of them is fine. Use them for "red squiggly" feedback loops.
5. **MCP, skills, and sub agents all carry a system prompt tax** (a description that is always loaded), so they scale less cleanly. Prefer skills over MCP for your own CLIs.
6. **Prefer tools that scale with intelligence** (overridable nudges) over tools that compensate for a lack of it (hard blocks).
7. **Work in parallel like a technical lead:** worktrees, named and colored sessions, `/loop`, auto mode, and remote control let you stop babysitting one agent at a time.

## Common pitfalls

- ❌ Leaving Claude with only the repo and the shell when your real context lives in Slack, docs, and dashboards.
- ❌ Trying to fine tune a model to learn your code base, which is costly and can increase hallucinations.
- ❌ Dumping your whole wiki or code base into context and hoping it fits.
- ❌ Editing something early in the prompt to "save space," which invalidates the KV cache and makes everything after it ten times more expensive.
- ❌ Wrapping an existing CLI in an MCP server for your own developers when a skill would be simpler.
- ❌ Adding a `CLAUDE.md`-style unconditional block to every plugin: it looks cheap and is not.
- ❌ Hard blocking the agent (caging it) when an overridable nudge would scale better with smarter models.

---

## 🛠️ Capstone Project: Scaling Harness Lab

> This is the main hands on project for the lesson, and the best way to make everything above stick. You are going to take a small but realistic repo and customize Claude Code with all four building blocks, then stress test which ones survive at scale. Start tiny and grow it as far as you like.

### What you will build

**Scaling Harness Lab** is a practice repo plus a set of customizations that you build, measure, and judge through Daisy's lens: access, knowledge, tooling, and "what happens at 100,000?" By the end you will have hands on intuition for which abstraction to reach for and why.

> 🎯 **Pick your world.** Use any small full stack-ish project you have, or scaffold a fresh one (a to do API, a tiny blog, a CLI tool). It just needs: a linter or type checker you can run, a fake "external service" you can pretend lives outside the repo, and a couple of code conventions a newcomer would not know.

### Why this is the perfect practice

| Lesson skill | Where you use it in Scaling Harness Lab |
|---|---|
| Access (connect everywhere you work) | Milestone 2, the access audit and one real connection |
| Knowledge via in context learning | Milestone 3, the `CLAUDE.md` and one skill |
| Tooling as a feedback loop ("red squigglies") | Milestone 4, the post edit hook |
| The four building blocks | Milestones 3 to 5, one of each |
| The scaling question (cost when unused) | Milestone 6, the stress test table |
| KV cache friendly layout | Milestone 6, the front vs end exercise |
| Parallel workflow | Milestone 7, worktrees plus `/loop` |

### Milestones (build them in order, each one works on its own)

1. **Scaffold and baseline.** Set up the repo and run Claude Code on it with **no** customization. Ask it to make one small change. Note where it struggles or asks you for context it could not find. This is your "vanilla" baseline.
2. **Access audit (the one day test).** For 30 minutes of real work, write down every time you alt tab away from Claude. Pick the single most painful gap (often Slack or your issue tracker) and connect it with an **MCP server**. Re run a task that needed that context.
3. **Knowledge layer.** Write a focused `CLAUDE.md` capturing 3 to 5 conventions a newcomer would not know. Then add **one skill**: a folder with a `SKILL.md` that teaches Claude how to use one of your existing CLIs or scripts. Confirm the skill triggers only when relevant.
4. **The red squiggly hook.** Add a **post tool use hook** that runs your linter or type checker after Claude edits a file and feeds back an overridable nudge (not a hard block). Confirm it returns nothing (and costs nothing) when the edited file is irrelevant.
5. **A sub agent.** Add a **sub agent** whose job is a big read (for example, "summarize how the auth module works") so the main session stays clean. Notice that only the result comes back to the main context.
6. **The scaling stress test.** For each of your four customizations, fill in a table: token cost when unused, and "what happens if I have 100,000 of these?" Then do the KV cache exercise: list what belongs at the **front** (stable, shared) and what belongs at the **end** (volatile, per task) of your context.
7. **Go parallel.** Create two **git worktrees**, put a separate Claude on each, and name and color the sessions. Then set up a `/loop` to babysit one repetitive task (for example, keep CI green or update docs) and let it run while you do something else.
8. **Stretch goals.** Replace your MCP wrapped CLI with a plain **skill** and compare context cost. Try **tool search** if you have many tools. Try **remote control** and check in from your phone.

### How you will know you are done

- ✅ You can point to **one customization per building block** (MCP, skill, hook, sub agent) and say what need it fills (access, knowledge, or tooling).
- ✅ Your hook **returns nothing and costs nothing** when it does not apply, and you have verified this.
- ✅ Your scaling table clearly shows **why the hook scales to 100,000 and the others carry a system prompt tax**.
- ✅ You can name what belongs at the **front** vs the **end** of your context and why (KV cache).
- ✅ Two agents run in parallel without stepping on each other, and a `/loop` handles one task without you babysitting it.

> 💡 **Keep yourself honest:** for every customization, ask Daisy's question out loud before you commit to it: "What happens if I have 100,000 of these?"

---

## Practice exercises (optional extra reps)

> **What these are:** five small, self contained tasks. Each one targets a single skill from the lesson. They are optional and independent. The **Capstone Project above is the main build**, and it already includes all of these skills in one place, so feel free to skip straight to it.

### Exercise 1: the one day access test (foundational)
For one real work session, log every time you leave Claude to use another tool. Group the gaps into access, knowledge, or tooling. Which single connection would save you the most context switches?

### Exercise 2: nudge vs cage (foundational)
Take a rule you wish Claude followed (for example, "do not edit generated files"). Write it twice: once as a **hard block** and once as an **overridable nudge**. Explain which one scales with a smarter model and why.

### Exercise 3: skill vs MCP (intermediate)
Pick a CLI you already have. Write a tiny **skill** that teaches Claude how to use it, then describe what an MCP wrapper would have cost in system prompt space. When would the MCP version actually be the right call?

### Exercise 4: zero overhead hook (intermediate)
Write a post edit **hook** that runs your linter and returns a nudge only on relevant files. Test it on a file it should ignore and confirm it inserts nothing into context.

### Exercise 5: front vs end layout (advanced)
List everything currently in one of your Claude sessions' context. Sort each item into "stable and shared" (belongs at the front) or "volatile and per task" (belongs at the end). Explain, using the KV cache, why this ordering saves money.

---

## Cheat sheet

```text
THE THREE NEEDS
  Access ...... connect Claude to Slack, CI/CD, dashboards, docs (where the "why" lives)
  Knowledge ... conventions + institutional memory, supplied as text (in context learning)
  Tooling ..... linters/checkers as feedback loops ("red squigglies")

THE CONTEXT WINDOW IS FIXED
  - Don't pay for what you don't use.
  - KV cache: stable+shared at the FRONT, volatile+per-task at the END.
  - Changing something early invalidates the cache for everything after it (~10x cost).

PICK ABSTRACTIONS THAT SCALE (imagine 100,000 of them)
  Hook ........ zero token cost when unused .......... scales BEST (feedback loops)
  Skill ....... small always-on description .......... mostly scales (teach CLIs/procedures)
  Sub agent ... small description + separate window ... mostly scales (offload big reads)
  MCP ......... full name+desc+schema in prompt ...... scales worst (public/3rd-party only)

TOOLS
  Prefer: overridable NUDGES that scale with intelligence
  Avoid:  hard BLOCKS that compensate for a lack of it

WORK IN PARALLEL
  git worktrees (one Claude each) + /color + rename
  /loop <interval> <prompt>   (babysit PRs, keep CI green)
  auto permissions mode + remote control
```

## How this connects to the rest of the course

- **Earlier, Module 2 (Core skills):** prompting and context basics that this lesson scales up to a full engineering harness.
- **Next, Module 4 · Lesson 11 (Build a Proactive Agent Workflow):** turns the asynchrony idea here into **routines**, scheduled and event triggered Claude Code sessions.
- **Next, Module 4 · Lesson 12 (Stop Babysitting Your Agents):** goes deep on verification loops, multi Claude work, and `/loop`, the parallel workflows introduced at the end of this lesson.

---

*Source: "Beyond the basics with Claude Code" by Daisy Holman (Anthropic), Code with Claude 2026, London. Code blocks and the folder layout are illustrative reconstructions of the ideas shown in the talk. Adapt commands and model names to the current version of Claude Code.*

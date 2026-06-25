# Module 0 · Lesson 0: Pre-flight, getting ready to build

> **Course:** Building with Claude, a self-paced course
> **Module 0:** Pre-flight: getting ready (optional on-ramp, take it before Lesson 1)
> **Speaker:** Self-guided setup (no talk for this one)
> **Source talk:** none. This page is the course on-ramp. The "Watch the talk" button has nothing to play here, so head straight into the reading and the setup checklist.
> **Estimated time:** 60 to 90 minutes (one focused setup session, plus optional refreshers)

---

## In one sentence

This course is excellent but it is pitched at someone who can already code a little, use a terminal, and has seen an LLM before, so this pre-flight page closes that small gap first: it tells you exactly what to install, what accounts to create, and which short refreshers to skim, so that from Lesson 1 onward you are building instead of figuring out plumbing.

> 🎯 **Where this lesson is heading.** There is no talk and no theory to memorise. The payoff is a **Capstone** that is a real launchpad: by the end you will have Python, git, an Anthropic API key, and Claude Code all working, you will have made your first API call, run your first Claude Code session, and pushed your first commit. Do that once here and the friction is gone for the whole course. Jump to **"Capstone Project"** to see the finish line.

## A few plain-language basics first

A handful of terms show up the moment you start setting things up. Here they are in plain words:

- **CLI (command-line interface) / terminal:** the text window where you type commands instead of clicking buttons. "Run this in your terminal" means type it there and press enter.
- **Repo (repository):** a folder of code tracked by git, usually mirrored on GitHub. This course lives in one.
- **API key:** a secret password-like string that lets your code talk to Claude and bills it to your account. Never paste it into a public file.
- **SDK (software development kit):** the small library you install (here, `anthropic`) so your code can call Claude in a few lines.
- **Environment variable:** a value your shell holds in memory, like `ANTHROPIC_API_KEY`, that programs read without you hard-coding the secret.
- **IDE (integrated development environment):** your code editor, for example VS Code.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

The course outline says it plainly: get the mental model "before touching tools." But the very first real lesson (The Prompting Playbook) jumps into XML tags and output contracts, Module 4 assumes git and a codebase, and Module 5 assumes APIs and function calling. None of that is hard, but if you meet it cold you will spend your study time fighting setup instead of learning. One focused hour now removes about ninety percent of that friction.

This page is calibrated for a **rusty coder**: you have written some scripts or done a bootcamp, but you are not fluent and it has been a while. So the plan below is light on "learn to program from zero" and heavy on "get the toolchain and the Claude-specific pieces working, and refresh git and prompting."

If you take one habit away, make it this: **never just read, always build.** Have your key and tools ready so that every lesson ends in a commit.

## Learning objectives

By the end of this lesson you will be able to:

1. Judge honestly whether you are ready for Lesson 1, using a short self-check.
2. Install and verify the full toolchain: Python, git, the `anthropic` SDK, and Claude Code.
3. Create the accounts you need (Anthropic Console for an API key, GitHub) and store your key safely.
4. Make your first Claude API call and run your first Claude Code session.
5. Know exactly which official, free resources to use to fill any gap, without hunting around.

## Prerequisites

- None. This is the on-ramp that comes before everything else.
- If you are already a working software engineer, skim the self-check below, do the Capstone to confirm your tools work, and move on to Lesson 1.

---

## Part 1: the honest map, is this course zero-to-hero?

Here is the straight answer so you are not surprised later. This course is **"competent-beginner to hero," not "absolute-zero to hero."** It is a re-sequenced set of 37 conference talks turned into lessons. It assumes you can already:

- read and run a small script,
- move around a terminal,
- and have at least seen a chatbot or an LLM before.

Give it those, and it genuinely takes you from there to prompting well, building and shipping production agents, deploying them on a cloud, and leading a rollout. That is the "hero" end.

> 🔑 **The gap is small and one-time.** You do not need a computer-science degree. You need a working toolchain, two accounts, and a few hours of refreshers. This page is that gap, closed in one sitting.

### A 60-second self-check

Score yourself. Each "no" points to a refresher in Part 4.

- [ ] I can open a terminal and run a command like `python3 --version`.
- [ ] I can read a short Python script and roughly follow what it does.
- [ ] I know what `git add`, `git commit`, and `git push` do.
- [ ] I have used an AI chat assistant and understand it predicts text.
- [ ] I have an editor I like (VS Code is the common choice).

Five checks: go straight to the Capstone, confirm your tools, then start Lesson 1. Two or more blanks: spend an evening on the matching Part 4 refresher first. You do not need mastery, just familiarity.

---

## Part 2: the three must-haves (do these before Lesson 1)

These are non-negotiable for the hands-on parts of every module.

### Must-have 1: Python and the command line

You will read and run Python scripts (this very course is built with them) and live in the terminal. You need Python 3.10 or newer.

- **Official Python tutorial** (free): [docs.python.org/3/tutorial](https://docs.python.org/3/tutorial/) — skim the first half, you do not need all of it.
- **The terminal**, free and excellent: MIT's [The Missing Semester of Your CS Education](https://missing.csail.mit.edu/) — the "Shell Tools" and "Command-line Environment" lectures are the high-value ones.

Verify it works:

```bash
python3 --version      # expect 3.10 or higher
pip3 --version
```

### Must-have 2: git and GitHub

Every capstone gets committed and pushed. That habit is the whole "build in public" backbone of the course.

- **Pro Git book** (free): [git-scm.com/book](https://git-scm.com/book) — read chapters 1 to 3, that is enough to be dangerous.
- **GitHub Hello World** (free, 15 minutes): [docs.github.com/en/get-started/start-your-journey/hello-world](https://docs.github.com/en/get-started/start-your-journey/hello-world)

Verify and identify yourself to git:

```bash
git --version
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"
```

### Must-have 3: the Claude API, Claude Code, and one prompting tutorial

This is the Claude-specific core. Three small steps:

1. **Create an Anthropic Console account and get an API key.** Go to [console.anthropic.com](https://console.anthropic.com/), create a key, and add a small amount of billing credit. The key is a secret, treat it like a password.
2. **Read the developer docs and install Claude Code.** Docs: [platform.claude.com/docs](https://platform.claude.com/docs) (the old `docs.claude.com` redirects here) and [code.claude.com/docs](https://code.claude.com/docs). Install Claude Code on macOS, Linux, or WSL with:

   ```bash
   curl -fsSL https://claude.ai/install.sh | bash
   ```

   You can also run it with no local setup in your browser at [claude.ai/code](https://claude.ai/code).
3. **Do one official prompting tutorial.** This single afternoon makes Lesson 3 feel like review instead of a wall:
   - Interactive prompt engineering tutorial: [github.com/anthropics/prompt-eng-interactive-tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial)
   - Anthropic's free courses repo (API fundamentals, prompting, evals, tool use): [github.com/anthropics/courses](https://github.com/anthropics/courses)
   - Anthropic Academy, the official learning hub: [anthropic.com/learn](https://anthropic.com/learn)

> 💡 **Why these three and not a giant reading list.** Almost everything else in the course is taught from scratch inside the lessons. These three are the only places where arriving cold genuinely slows you down. Do them, skip the rest until you need it.

---

## Part 3: two things you can safely defer

Do not let these block you. Touch them only when a module reaches them.

- **MCP (Model Context Protocol)** is the standard way Claude connects to outside tools and data. It first matters in Module 5. One read of [modelcontextprotocol.io](https://modelcontextprotocol.io/) the week you get there is plenty.
- **Cloud fundamentals (Google Cloud, AWS, or Azure)** only matter for Module 7. Skip it now. When you arrive, pick the single provider you will actually deploy on and learn just that one.

> ❌ **A common mistake:** trying to learn MCP and a cloud platform up front "to be thorough." You will forget it before you use it. Learn these just in time, not just in case.

---

## Part 4: the rusty-coder fast track

You said you have some coding but it is rusty. Here is the shortest path that respects that. Aim for one evening, not one week.

| If this is rusty | Do this (time-boxed) |
|---|---|
| The terminal | Missing Semester "Shell Tools" lecture, 1 hour |
| Git | Pro Git chapters 1 to 3, or the GitHub Hello World, 1 hour |
| Python syntax | Skim the Python tutorial sections 3 to 5, 1 hour, run the examples |
| Prompting | The interactive prompt tutorial, 1 to 2 hours, this doubles as Lesson 3 prep |
| Calling Claude in code | Anthropic "API fundamentals" course in the courses repo, 1 hour |

> 🔑 **You do not need to finish these to start.** Do the Capstone below first. If a step there feels shaky, that tells you exactly which row above to spend time on. Let the doing drive the studying.

---

## Part 5: accounts, keys, and cost (so nothing surprises you)

- **Two accounts:** an Anthropic Console account (for the API key, at [console.anthropic.com](https://console.anthropic.com/)) and a GitHub account.
- **Keep your key secret.** Never commit it. Put it in an environment variable or a git-ignored `.env` file (this repo already ignores `.env`).
- **Cost is small for learning.** Use the cheapest model (Haiku) for casual calls and save the larger models for when a lesson calls for them. A few dollars of credit covers a lot of practice. Module 2 Lesson 4 ("Picking the right model") teaches the "cost per successful outcome" mindset in depth.

```bash
# store your key for the current terminal session (Linux / macOS)
export ANTHROPIC_API_KEY="sk-ant-..."

# or, in a git-ignored .env file at the repo root:
# ANTHROPIC_API_KEY=sk-ant-...
```

---

## Key takeaways

1. **This course is competent-beginner to hero.** It assumes a little coding, a terminal, and that you have seen an LLM. Give it those and it carries you the rest of the way.
2. **Three must-haves before Lesson 1:** Python plus the terminal, git plus GitHub, and the Claude API plus Claude Code plus one prompting tutorial.
3. **Defer MCP and cloud.** Learn them just in time, in Modules 5 and 7, not up front.
4. **Keep your API key secret** and start on the cheapest model.
5. **The point is momentum:** finish the Capstone and you never fight setup again, every lesson can end in a commit.

## Common pitfalls

- ❌ Watching lessons passively without tools installed, so you can never actually build the capstone.
- ❌ Trying to learn everything (MCP, three clouds, advanced Python) before Lesson 1, then burning out before you start.
- ❌ Hard-coding your API key into a file and pushing it to GitHub. Use an environment variable or git-ignored `.env`.
- ❌ Reaching for the most expensive model for casual practice. Default to Haiku while learning.
- ❌ Treating the refreshers as a course to complete. They are there to unblock you, not to finish.

---

## 🛠️ Capstone Project: your launchpad (get everything working once)

> This is the real hands-on work of the lesson. It is not a toy. By the end you will have a verified toolchain, your first API call, your first Claude Code session, and your first commit, which is exactly the loop you will repeat for the next 37 lessons.

### What you will build

A working setup, proven by four small artifacts: a green tool check, a first model response, a first Claude Code edit, and a first pushed commit.

### Milestones (do them in order, each stands on its own)

1. **Green tool check.** Run `python3 --version`, `git --version`, and `claude --version`. All three should print a version. Fix any that do not using the links in Part 2.
2. **Make your first API call.** Install the SDK and run the script below. You should see Claude reply.

   ```bash
   pip install anthropic
   export ANTHROPIC_API_KEY="sk-ant-..."   # your real key
   ```

   ```python
   # hello_claude.py
   from anthropic import Anthropic

   client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment

   msg = client.messages.create(
       model="claude-haiku-4-5",   # cheapest; check platform.claude.com/docs for the current id
       max_tokens=200,
       messages=[{"role": "user", "content": "In one sentence, what is this course about?"}],
   )
   print(msg.content[0].text)
   ```

   Run it with `python3 hello_claude.py`. Seeing a reply means your key, billing, and SDK all work.
3. **Run your first Claude Code session.** In the course repo, run `claude`, log in when prompted, and ask it something simple like "summarise what this repository contains." Watch how it reads files and answers.
4. **Make a one-line edit with Claude Code, then commit it.** Ask Claude Code to add your name and today's date to the bottom of `PROGRESS.md`, then commit and push:

   ```bash
   git add PROGRESS.md
   git commit -m "Pre-flight: confirm my toolchain works"
   git push
   ```
5. **Do one prompting tutorial chapter.** Open the [interactive prompt tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial) and complete at least the first chapter. This is also your warm-up for Lesson 3.
6. **Stretch goals.** Set your key in a git-ignored `.env` instead of exporting it each time. Try the same API call with a larger model and notice the difference in answer and cost. Install the VS Code or JetBrains Claude Code extension.

### How you will know you are done

- ✅ `python3`, `git`, and `claude` all report a version.
- ✅ `hello_claude.py` prints a real reply from Claude.
- ✅ You ran a Claude Code session and watched it read the repo.
- ✅ You pushed at least one commit to GitHub.
- ✅ You completed at least one chapter of the prompting tutorial.

> 💡 **Keep yourself honest:** if any milestone felt shaky, that is your signal. Spend an evening on the matching row in the Part 4 fast track before starting Lesson 1.

---

## Practice exercises (optional extra reps)

> Small, independent drills. The Capstone already covers the essentials, so treat these as reinforcement.

### Exercise 1: change one parameter (foundational)
Re-run `hello_claude.py` with `max_tokens=20`, then `max_tokens=500`. Watch how the answer length changes. You just felt your first model control.

### Exercise 2: keep a secret a secret (foundational)
Move your key out of the `export` line and into a git-ignored `.env` file. Run `git status` and confirm `.env` does not appear as a file to be committed.

### Exercise 3: a tiny git loop (foundational)
Make a trivial edit to `PROGRESS.md`, then practice the full loop: `git add`, `git commit`, `git push`. Confirm the change appears on GitHub.

### Exercise 4: read before you build (intermediate)
Open `build_index.py` in this repo and ask Claude Code to explain what it does in plain language. Notice how reading existing code with an agent is faster than reading it alone.

### Exercise 5: cost intuition (intermediate)
Ask Claude (via the API or Claude Code) the same hard question once with Haiku and once with a larger model. Note which answer you would actually ship. This is the seed of Lesson 4's "cost per successful outcome."

---

## Cheat sheet

```text
ARE YOU READY?
  Can code a little + use a terminal + seen an LLM  -> yes, you're ready
  Missing one of those                              -> do the matching Part 4 refresher

THE THREE MUST-HAVES (before Lesson 1)
  1. Python 3.10+ and the terminal
  2. git and a GitHub account
  3. Anthropic API key + Claude Code + one prompting tutorial

DEFER (learn just in time)
  MCP ...... Module 5  -> modelcontextprotocol.io
  Cloud .... Module 7  -> pick one provider when you get there

VERIFY YOUR TOOLS
  python3 --version
  git --version
  claude --version

OFFICIAL, FREE RESOURCES
  Dev docs ........... platform.claude.com/docs
  Claude Code docs ... code.claude.com/docs
  Get an API key ..... console.anthropic.com
  Prompt tutorial .... github.com/anthropics/prompt-eng-interactive-tutorial
  Free courses ....... github.com/anthropics/courses
  Anthropic Academy .. anthropic.com/learn
  Python ............. docs.python.org/3/tutorial
  Git ................ git-scm.com/book
  Terminal ........... missing.csail.mit.edu

GOLDEN RULE
  Never just read. Always build. End every lesson in a commit.
```

## How this connects to the rest of the course

- **Next, Module 1 · Lesson 1 (Opening Keynote):** the big-picture map of the whole stack. With your tools working, you can build its capstone instead of just reading it.
- **Soon, Module 2 · Lesson 3 (The Prompting Playbook):** the prompting tutorial you did here is the perfect warm-up for it.
- **Soon, Module 2 · Lesson 4 (Picking the right model):** turns the "start cheap" habit from Part 5 into a rigorous "cost per successful outcome" method.
- **Later, Module 5 (Managed Agents) and Module 7 (Cloud):** where the deferred MCP and cloud topics get full, hands-on treatment, exactly when you need them.

---

*This page is the course on-ramp, written for the self-paced "Building with Claude" course. It is not based on a conference talk. All linked resources are official and free at the time of writing; if a URL has moved, search its name. Adapt model ids and SDK details to the current docs at platform.claude.com/docs.*

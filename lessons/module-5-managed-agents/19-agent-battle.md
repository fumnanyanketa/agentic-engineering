# Module 5 · Lesson 19: Agent Battle: Mine the Most Diamonds

> **Course:** Building with Claude, a self-paced course
> **Module 5:** Building agents, Claude Managed Agents
> **Speaker:** Ben and Jeff, Applied AI team, Anthropic
> **Source talk:** [Agent Battle: Mine the most diamonds in 45 minutes](https://www.youtube.com/watch?v=dxqX_6ciVQA) · [full transcript](../../transcripts/code-with-claude-2026-london-2026-day-2/03_agent-battle-mine-the-most-diamonds-in-45-minutes.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

This lesson turns agent building into a competitive game: you deploy a managed agent to mine diamonds in Minecraft, then improve it by tuning four levers (system prompt, model, skills, and tools), measuring each change against a fast eval, and chasing not just the most diamonds but the best diamonds-to-tokens ratio.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you run your own **DiamondForge Challenge**: a deployed agent, a one-minute eval loop, a leaderboard, and a disciplined hill-climbing process to beat your own best score. Everything before the Capstone teaches the moves you will use. To see the finish line first, jump to **"Capstone Project: DiamondForge"** and come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)** (paper). Frames iterative agent improvement as a measure, reflect, retry loop, the exact "hill-climb on a measurable objective" discipline this lesson is built around.
> - **[Reinforcement Learning: An Introduction (Sutton & Barto)](https://web.stanford.edu/class/psych209/Readings/SuttonBartoIPRLBook2ndEd.pdf)** (book). The bedrock text on the explore/exploit, planning, and reward framing behind optimizing an agent against a score.

## A few plain-language basics first

This lesson is a competition with a few moving parts. Here they are in plain words:

- **Agent:** an AI that takes a series of actions on its own toward a goal (here, mining diamonds), instead of answering in one shot.
- **Managed agent:** an agent hosted on Anthropic's infrastructure (Claude Managed Agents). Most of the plumbing is set up for you; your job is to shape its behaviour.
- **System prompt:** the standing instructions that define who the agent is and how it should behave. It is the single biggest lever you control here.
- **Model string:** the name of the exact model you point the agent at (for example a Sonnet or an Opus version). Bigger models are more capable but cost more tokens.
- **Token:** the unit the model reads and writes in, roughly three quarters of a word. You are billed per token, so "more tokens" means "more cost."
- **Skill:** a reusable package of instructions and assets that bolts a specific capability onto the agent. You can use one shipped by Anthropic or write your own.
- **MCP (Model Context Protocol):** a standard way to give an agent **tools** (actions it can call). Here the tools let the agent move and act in Minecraft, like "mine block," "jump," and "go near things."
- **Eval (evaluation):** a test you run an agent against to measure how well it does. A fast eval lets you iterate quickly.
- **Hill climbing:** improving step by step. You measure, change one thing, measure again, and keep whatever moves you uphill (a higher score).

You do not need to memorise these. Each is explained again the first time it appears.

## Why this lesson matters

This is the loop that Anthropic's own teams use to improve every agent they ship. As Ben says, the workshop teaches "how we improve all of our agents internally." Anyone who has put an agent into production knows the real work is not the first version; it is the cycle of **measuring impact, understanding behaviour, and making changes to iteratively improve**.

Minecraft is just a fun, measurable arena for that loop. The diamonds are a clear score, and the diamonds-to-tokens ratio forces you to be efficient instead of just throwing the heaviest model at the problem. The skill you walk away with (disciplined hill climbing on a real eval) transfers to any agent you build.

## Learning objectives

By the end of this lesson you will be able to:

1. **Build and deploy a managed agent** on hosted infrastructure where the configuration is mostly set up for you.
2. Understand the **impact of agent configuration**: the system prompt, the model string, and the skills and MCP tools you plug in.
3. **Hill-climb on evals**: measure, change one lever, re-measure, and keep what helps.
4. Optimise for **efficiency**, not just raw score, by tracking the diamonds-to-tokens ratio.

## Prerequisites

- Earlier Module 5 lessons on Claude Managed Agents (what an agent is, and how it is deployed and run).
- Comfort editing a Python file and running commands in a terminal.
- Helpful but optional: Module 2 · Lesson 3 (The Prompting Playbook), since system-prompt craft is the main lever here.

---

## Part 1: the game and the goal

The challenge is simple to state: have an agent **mine the most diamonds in Minecraft** within a time box. (Minecraft is a block-based world game; "mining" means digging through blocks to find rare resources like diamonds.) In the 2020s, as Ben jokes, we have agents play it for us.

Three things the workshop is really teaching:

1. **Build and deploy a managed agent.** It runs on Anthropic's infrastructure with most configuration pre-set, so you focus on getting it into "peak diamond-mining condition."
2. **Understand the impact of configuration.** The system prompt, model string, and the skills and MCP tools you attach all shape behaviour.
3. **Hill-climb on evals.** Measure impact, understand behaviour, change, repeat. This is how Anthropic improves agents internally.

> 🔑 **Key idea: building the agent is the easy part; tuning it is the job.** The infrastructure is handed to you. Your real work is the iterative loop of measuring, understanding, and improving.

---

## Part 2: the rules of the battle

The competition has tight constraints, and the constraints are the lesson. Here they are:

| Rule | Detail |
|---|---|
| **Time box** | About 35 minutes to build and experiment. |
| **Submissions** | Submit as many runs as you like, but only your **top run** counts. |
| **A run** | Five minutes of the agent mining. You can kill a run anytime with Control-C in the terminal. |
| **Fast eval** | An eval set that takes about **one minute**, for quick iteration between full runs. |
| **Winning** | Most diamonds at the end wins, shown on a live **leaderboard**. |
| **Tie-breaker** | Ties are settled by **token efficiency** (diamonds-to-tokens ratio). |
| **Bonus** | A chat where agents can talk to one another. |

That tie-breaker changes everything. As Ben puts it, "this is not just mine the most diamonds, it is get the best diamonds-to-tokens ratio."

> 🔑 **Key idea: efficiency is a first-class goal.** Because ties are broken on tokens, you cannot win by simply "throwing in the heaviest weight model you can." You have to hone the system prompt so a leaner setup gets more done per token.

> 💡 The two-tier feedback (a fast one-minute eval plus a slower five-minute scored run) is itself the lesson in disguise: iterate cheaply on the fast eval, and only spend a full run when you think you have a real improvement.

---

## Part 3: the harness, what is shipped for you

Jeff walks through what comes in the box so you can spend your time on behaviour, not plumbing. (A **harness** is all the code and infrastructure around the model: the loop that runs it, the tools it can call, and the connections to the world.)

```text
┌──────────────────────────────────────────────────────┐
│  my_agent.py   <- YOU edit this                        │
│    - model string        (which model to use)          │
│    - system prompt        (currently empty)            │
│    - skill                (Anthropic's, or your own)    │
└───────────────┬──────────────────────────────────────┘
                │ uses
                ▼
┌──────────────────────────────────────────────────────┐
│  MCP tools  ->  Mineflare bot  ->  Minecraft clone     │
│    mine block, jump, go near things, ...               │
│    (no visuals; the agent acts through tool calls)     │
└──────────────────────────────────────────────────────┘
```

Key points about the setup:

- You work primarily in a single file, **`my_agent.py`**, found in the workshop repo.
- The agent drives a **Mineflare** bot connected to a Minecraft clone. There are **no visuals**: the agent does not see the screen, it acts entirely through MCP tool calls like "mine block," "jump," and "go near things."
- **Everyone starts from the same seed.** (A **seed** is the number that generates the world layout. Same seed means same starting world, so there is no luck-of-the-map advantage and no map optimisation to chase.) Every reset gives the same start kit and seed.
- A **Claude Code skill** is included in the repo to help with setup if you hit snags.

> ✅ **Best practice: a fair test isolates the variable.** Because the seed and start kit are fixed, any change in your score comes from your **configuration**, not from a luckier world. That is exactly what makes the eval trustworthy for hill climbing.

---

## Part 4: the four levers you actually control

Everything you can change lives in `my_agent.py`. There are four levers, and learning which to pull when is the whole skill.

```python
# my_agent.py  (illustrative shape of what you tune)

MODEL = "claude-sonnet-4-6"          # Lever 1: capability vs token cost

SYSTEM_PROMPT = """                   # Lever 2: the biggest behaviour lever
You are a focused Minecraft mining agent. Your sole goal is to mine
as many diamonds as possible in five minutes.

Strategy:
- Diamonds are found deep underground. Dig down efficiently to the
  depth where diamonds appear, then branch-mine sideways.
- Do not waste actions wandering on the surface.
- Prefer the fewest tool calls that make progress (token efficiency).
"""

SKILL = "anthropic/minecraft-mining"  # Lever 3: shipped skill OR your own

MCP_SERVERS = ["mineflare"]           # Lever 4: the tools the agent can call
```

Here is how to think about each lever:

| Lever | What it changes | When to reach for it |
|---|---|---|
| **System prompt** | Who the agent is and its strategy. | First and most often. Cheap to change, huge impact, and it is what protects your token efficiency. |
| **Model string** | Raw capability per token. | When the prompt is well honed but the agent still cannot reason well enough. Watch the token cost. |
| **Skill** | A reusable bundle of mining know-how. Use Anthropic's or write your own. | When you have a repeatable strategy worth packaging, or want to override the default behaviour. |
| **MCP tools** | The actions available to the agent. | When the agent needs an action it does not have, or you want to adjust how tools behave. |

> 🔑 **Key idea: pull the cheap lever first.** The system prompt starts empty, costs nothing to change, and most directly improves your diamonds-to-tokens ratio. Reach for a heavier model only when prompt work has run out of room, because the model lever quietly costs you on the tie-breaker.

---

## Part 5: the hill-climbing loop in practice

This is the heartbeat of the whole workshop. With a fixed seed and a fast eval, the loop is:

```text
1. Make ONE change in my_agent.py  (start with the system prompt)
2. Run the ~1-minute eval           -> quick read on whether it helped
3. If promising, do a full 5-minute scored run
4. Read behaviour: where did the agent waste actions or tokens?
5. Keep what climbs, revert what does not. Repeat.
```

The competition itself shows the loop working. The leaderboard moves over the session: an early run posts 10 diamonds, scores creep up, and 19 emerges as roughly the upper echelon. Then, late in the session, someone breaks past 19 with only 1 minute 20 seconds left, prompting Jeff to ask them to "reveal your technique." That jump is hill climbing paying off: enough fast iterations found a configuration that pulled clearly ahead.

> 💡 **Read the behaviour, not just the score.** A run with no visuals still leaves a trail of tool calls. The fastest improvements come from spotting *why* the agent underperformed (wandering on the surface, repeating failed digs, over-explaining itself) and fixing that one thing in the prompt.

> ❌ A cautionary note from the leaderboard: one top run showed **zero tokens**, which Jeff called "highly suspicious." If your metric looks too good to be true, your measurement is probably broken. Trust a number only when you understand how it was produced.

---

## Part 6: lessons that transfer beyond Minecraft

Strip away the diamonds and this is the exact discipline for improving any production agent:

- **Fix the test conditions** (same seed, same start kit) so changes are comparable.
- **Iterate on a cheap, fast eval** before spending an expensive full run.
- **Tune the cheapest, highest-impact lever first** (the prompt), and treat the model as a last resort because of its cost.
- **Optimise for an efficiency metric**, not just a raw score, so your agent is sustainable at scale.
- **Distrust suspicious numbers** and verify how every metric is computed.

> 🎯 **The whole point.** Whether the goal is diamonds, resolved support tickets, or fixed incidents, the winning move is the same: measure, change one lever, measure again, and let the eval tell you the truth.

---

## Key takeaways

1. **Deploying a managed agent is the easy part.** The infrastructure is set up for you; tuning behaviour is the job.
2. **You have four levers:** system prompt, model string, skills, and MCP tools.
3. **The system prompt is the cheap, high-impact lever.** Pull it first and pull it most.
4. **Efficiency matters as much as score.** A diamonds-to-tokens tie-breaker means a honed prompt beats a heavy model.
5. **Hill-climb on a fast eval.** A fixed seed plus a one-minute eval makes every change comparable and cheap to test.
6. **Read behaviour and distrust weird numbers.** A zero-token "win" is a broken measurement, not a triumph.

## Common pitfalls

- ❌ Reaching for the biggest model first, then losing the tie-breaker on tokens.
- ❌ Changing several levers at once, so you cannot tell what helped.
- ❌ Only running the slow five-minute run and never using the fast eval to iterate.
- ❌ Leaving the system prompt empty or vague when it is your most powerful lever.
- ❌ Trusting a score without checking how it was measured (the zero-token trap).
- ❌ Looking for map or seed tricks when the seed is fixed and gains can only come from configuration.

---

## 🛠️ Capstone Project: DiamondForge

> This is the main hands-on project for the lesson. You will recreate the battle's full loop yourself: a deployed agent, a fast eval, a leaderboard of your own attempts, and a disciplined hill-climbing process that beats your own best score on an efficiency metric. Start with the smallest working version and improve it.

### What you will build

**DiamondForge** is your personal agent-tuning arena. It has three parts that mirror the workshop:

1. **A deployed managed agent** driven by a single config file (model, system prompt, skill, tools).
2. **A two-tier eval**: a fast check for quick iteration and a longer scored run for real results.
3. **A leaderboard of your own runs** that records score *and* tokens, so you can chase the best ratio.

> 🎯 **Pick your arena.** Use the Minecraft mining task if you have access, or swap in any task with a clear numeric score and a fixed starting condition: a maze-solving agent counting steps to the exit, a web-scraping agent counting correct records, or a puzzle agent counting solved puzzles. You just need a fixed seed (same start every time), a measurable score, and a token count.

### Why this is the perfect practice

| Lesson skill | Where you use it in DiamondForge |
|---|---|
| Deploy a managed agent | Milestone 1 |
| Fix test conditions (seed/start kit) | Milestone 2 |
| Build a fast eval | Milestone 2 |
| Tune the system prompt first | Milestone 3 |
| Track diamonds-to-tokens efficiency | Milestone 4, the leaderboard |
| Decide when to change model/skill/tools | Milestone 5 |
| Hill-climb and read behaviour | Milestone 6 |

### Milestones (build them in order, each one works on its own)

1. **Deploy.** Stand up a managed agent driven by a `my_agent.py`-style config with a model string, an empty system prompt, a skill slot, and an MCP tool connection. Get one full run to complete end to end, even with a low score.
2. **Lock the conditions and add a fast eval.** Fix the seed and start kit so every run is comparable. Write a ~1-minute eval that returns a quick, rough score so you can iterate cheaply.
3. **Write a real system prompt.** Replace the empty prompt with a clear role and strategy. Re-run the eval and record the jump. This is your cheapest, biggest win.
4. **Build the leaderboard.** Log every run with its score **and** its token count, and compute a score-to-tokens ratio. Sort by the ratio, not just the score.
5. **Decide on the heavier levers.** Only now experiment with a stronger model, a custom skill, or an extra tool. For each, check whether it improves the *ratio*, not just the raw score, and keep it only if it does.
6. **Hill-climb to a personal best.** Run at least eight tuning cycles (change one lever, eval, keep or revert). Read the agent's behaviour each time to find the next fix. Beat your Milestone 3 ratio by a clear margin.

### How you will know you are done

- ✅ Your agent completes a full scored run reliably from the fixed start.
- ✅ The fast eval lets you test a change in about a minute, and you actually use it before full runs.
- ✅ Your leaderboard ranks runs by **score-to-tokens ratio**, and your best entry came from a prompt change, not just a bigger model.
- ✅ You can point to at least three changes and say, from the data, exactly what each one did to score and tokens.

> 💡 **Keep yourself honest:** change one lever at a time and re-run. And before you celebrate a high score, verify the token count is real (no zero-token "wins").

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each focused on one skill. Optional and independent. The **Capstone above is the main build** and covers all of these together.

### Exercise 1: write the first system prompt (foundational)
Take an empty agent for a scored task and write a system prompt with a clear role and a step-by-step strategy. Run the eval before and after and record the difference.

### Exercise 2: prompt versus model (foundational)
Hold the model fixed and improve only the prompt until gains flatten. Then bump the model once. Compare the score gain to the token-cost increase. Which change earns its keep?

### Exercise 3: design an efficiency metric (intermediate)
Define a score-to-tokens ratio for your task and build a tiny leaderboard that sorts by it. Run three configurations and explain why the highest score is not always the winner.

### Exercise 4: read the behaviour trail (intermediate)
Pick a run that underperformed and inspect its tool calls. Identify the single biggest source of wasted actions or tokens, fix it in the prompt, and confirm the ratio improves.

### Exercise 5: catch a broken metric (advanced)
Deliberately introduce a measurement bug (for example a run that reports zero tokens) and have a teammate or your future self spot it. Then write a small check that flags suspicious metrics automatically before they reach the leaderboard.

---

## Cheat sheet

```text
THE GAME
  Most diamonds wins. Ties broken by diamonds-to-tokens ratio.
  Same seed + start kit for everyone -> only CONFIG changes the score.

THE FOUR LEVERS (edit my_agent.py)
  1. system prompt  <- cheapest, biggest impact. Pull FIRST and MOST.
  2. model string   <- more capability per token, but costs you on ties.
  3. skill          <- Anthropic's, or write your own.
  4. MCP tools      <- actions the agent can call (mine, jump, go near).

THE LOOP (hill climbing)
  change ONE lever -> ~1-min eval -> if promising, 5-min scored run
  -> read the behaviour -> keep what climbs, revert what doesn't -> repeat.

DISCIPLINE
  - Fix the test conditions so changes are comparable.
  - Iterate on the cheap eval before the expensive run.
  - Optimise the EFFICIENCY metric, not just raw score.
  - Distrust suspicious numbers (zero tokens = broken measurement).
```

## How this connects to the rest of the course

- **Earlier, Module 2 · Lesson 3 (The Prompting Playbook):** the "change one thing, re-run the eval" method and the system-prompt craft used here are taught in depth there.
- **Earlier in Module 5:** deploying agents on Claude Managed Agents, the infrastructure this battle runs on.
- **Companion, Module 5 · Lessons 17 and 18 (memory and dreaming):** the same hill-climbing discipline is how you would improve a memory-and-dreaming agent over time.
- **Across the course:** the measure, change, re-measure loop is the single most transferable skill for any agent you ship.

---

*Source: "Agent Battle: Mine the most diamonds in 45 minutes" by Ben and Jeff (Anthropic), Code with Claude 2026, London. The `my_agent.py` snippet and the harness diagram are illustrative reconstructions of the setup described in the talk; the workshop rules, leaderboard moments, and four configurable levers are as presented by the speakers.*

# Module 9 · Lesson 36: How Lovable Vibecodes Production Software at Scale

> **Course:** Building with Claude, a self-paced course
> **Module 9:** In the field, industry case studies
> **Speaker:** the Lovable team (London)
> **Source talk:** [How Lovable vibecodes production software at scale](https://www.youtube.com/watch?v=mhW-XXnDFSU) · [full transcript](../../transcripts/code-with-claude-2026-london-2026/16_how-lovable-vibecodes-production-software-at-scale.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

When millions of non-technical people build software with AI, the make-or-break problem is users getting **stuck**, and the answer is a **self-healing platform**: detect stuck users, fix problems before they hit (Lovable Overflow), let the agent itself report its own frustration so you can fix the platform (venting), and ruthlessly prune knowledge so the system keeps improving instead of rotting.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you build a **Self-Healing Layer** for an AI product of your own: a stuck-detector, a reusable-fix knowledge base, and an agent feedback channel. Everything before the Capstone explains each piece. If you want the finish line first, jump to the **Capstone Project**, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[The Lean Startup](https://en.wikipedia.org/wiki/Lean_startup)** (essay). Lovable's self-healing platform is a Build-Measure-Learn engine driven by validated learning from real usage, the durable discipline behind shipping fast without flying blind.
> - **[The SPACE of Developer Productivity](https://www.microsoft.com/en-us/research/publication/the-space-of-developer-productivity-theres-more-to-it-than-you-think/)** (paper). Supports the "make it a metric, then tune" rigor: quality and productivity must be measured across dimensions, not by one number.

## A few plain-language basics first

This lesson uses some product and AI terms. Here they are in plain words:

- **LLM (Large Language Model):** the kind of AI that reads and writes text and code. Claude is an LLM.
- **Agent:** an AI that takes a series of actions on its own toward a goal. Lovable's "agent" is the AI that actually builds your app.
- **Vibe coding:** building software by describing what you want in plain language and letting the AI write the code, while you mostly look at the result rather than the code itself.
- **Context (of an agent):** the information the agent currently has in front of it. "Modifying the context" means adding or changing what the agent sees before it acts.
- **Classification model:** a small, cheap AI whose only job is to sort an input into categories, for example "stuck" vs. "not stuck."
- **PR (pull request):** a proposed code change that a human reviews before it is merged into the real product.
- **Server-side rendering (SSR) vs. client-side rendering:** two ways a web page is built. With client-side rendering the browser builds the page; with server-side rendering the server builds it first, which search engines read better (good for SEO, search engine optimisation).
- **Eval (evaluation):** a set of test cases that measure whether the system works. Covered more in Module 3.
- **Half-life of knowledge:** the idea that a stored fix slowly goes out of date, like a battery losing charge, so it must eventually be discarded.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Lovable lets anyone build software by chatting: a chat on the left, a live preview on the right. It has 50 million projects, 200,000 new ones a day, and 600 million monthly visits to sites built on it (more traffic than Lovable's own). Its users range from kids to the Fortune 500, and most are *not* engineers. That combination, production-grade ambition plus non-technical users, makes one problem dominant: what happens when a user gets stuck and has no one to ask? This lesson is a masterclass in operating an AI product at scale: not "how to write the agent," but "how to keep millions of people succeeding with it." The patterns generalise to any AI product with real users.

## Learning objectives

By the end of this lesson you will be able to:

1. Define "stuck" as a measurable metric and describe the three kinds of stuck.
2. Explain **Lovable Overflow**: a curated, pruned knowledge base that injects the right fix into the agent's context *before* the user gets stuck.
3. Explain **venting**: giving the agent a tool to report its own frustration, which surfaces bugs, drives fixes, and even detects outages.
4. Apply the discipline that makes both work: continuous tuning and aggressive pruning, because knowledge has a half-life.

## Prerequisites

- A basic understanding of agents and context (Module 2).
- Helpful but optional: Module 3 (Evals), since the system is tuned with metrics and evals.

---

## Part 1: the real problem is getting stuck

Lovable started as GPT-Engineer, a terminal program by co-founder Anton that became the fastest-growing repo on GitHub by building end-to-end software from a prompt (the demo built and ran a snake game). The mission widened: build software not for "the 1% that can code," but for "the 99%." That did not work in 2023 (models were too early), started making sense about a year and a half before the talk, and keeps improving roughly every three months as foundation models advance.

Two principles guide how Lovable builds:

1. **Chase the frontier of production-grade software,** not just prototypes. Push complexity, size, and ambition.
2. **Build for non-technical users.** This is the hard combination, an expert-in-the-loop product is easier, but the demand for non-expert tools is immense.

Then comes the timeless problem, captured in an old engineering joke: the last 10% of code takes 90% of the time, and the first 90% also takes 90% of the time, "so you end up with 180% of the time." The same shape holds in the age of AI: you get a first version fast, then finishing it and squashing bugs takes even longer.

Picture a timeline. You start in the **green** (low friction), hit some **friction**, and can slide into the **red** (stuck). An engineer who gets stuck knows the drill: sleep on it, jump into the code, contract help. A non-technical user, working at the abstraction where they never see the code, has none of those escapes. Getting hard-stuck is, in their words, "the worst thing that can happen" to that user.

> 🔑 **The vision:** "every app that is built on the platform should help improve the next." That is the definition of a self-healing platform. The rest of the talk is two concrete tactics for it.

### Defining "stuck" so you can measure it

You cannot fix what you cannot measure, so Lovable made stuck a metric called `is_stuck`. It is true when:

```text
is_stuck = true IF any of:
  - the user asks for the same thing 3 times in a row ("fix it, fix it, fix it")
  - the user complains about the implementation ("this didn't work")
  - the user asks for something and then just leaves
```

A small **classification model** (a cheap AI that just sorts inputs into categories) decides this in real time. And there are three *kinds* of stuck, which matter because each has a different cure:

| Kind of stuck | Whose problem | The question for the platform |
|---|---|---|
| **Solvable by prompting differently** (yellow) | Often the user's phrasing or missing context; might even self-resolve with "fix it." | Can we fix it *before* the user ever gets hard-stuck? |
| **Easy in theory, not yet supported** | The platform falls short at the edges of its own functionality. | How do we self-heal at the edges of what we support? |
| **Falls short, big investment needed** | The platform genuinely lacks something (for example server-side rendering for SEO). | Worth a larger build. (Lovable shipped SSR the week before the talk.) |

> 💡 The two tactics that follow each target one of the first two kinds. Lovable Overflow handles the "prompt around it" kind; venting handles the "easy but unsupported" kind.

---

## Part 2: Lovable Overflow, fix it before they get stuck

**Lovable Overflow** is named in honour of Stack Overflow (the site where developers post problems and solutions). It is "a big collection of descriptions of issues" paired with their solutions, built from what actually happens on the platform.

To see why it helps, watch a user get stuck the slow way:

```text
WITHOUT Lovable Overflow:
  user: "the scrolling is super laggy"        (not stuck yet)
  agent: "fixed it, I removed the animations"  (but it actually failed silently)
  user: "it's still lagging and looks broken"  (NOW stuck; may repeat)
  ... back and forth ...
  agent eventually solves it -> user no longer stuck
```

That round-trip is slow, expensive, and frustrating. The question Lovable asked was: "what if we can just skip to the final solution?"

```text
WITH Lovable Overflow:
  user: "the scrolling is super laggy"
  -> SEARCH the corpus of problem descriptions for similar laggy issues
     (using context: the user's tech stack, library versions)
  -> a lightweight model decides if a match is relevant
  -> if so, ADD that knowledge into the main agent's context
     (rewritten to fit THIS situation, not dumped raw)
  -> main agent fixes it first try
```

Two design details are doing heavy lifting:

> 🔑 **Adapt the knowledge, do not dump it.** Lovable does not paste raw corpus text into the agent. A lightweight model rewrites it to fit the user's exact situation, "to make the job as easy as possible for our main agents."

> 🔑 **Prune relentlessly, because knowledge goes stale.** A fix for an old version of a JavaScript package can *worsen* the experience once the package updates. So every knowledge file has a tracked **success ratio**, and Lovable continuously prunes outdated knowledge and refills with new. Tuning *when to deprecate* and *when to add* is "an extremely important part of making this work."

The payoff (more on numbers in Part 4): faster, cheaper, and a much better experience, because the back-and-forth is skipped.

---

## Part 3: venting, let the agent fix the platform

The second tactic, called **venting** internally, targets the second kind of stuck: things that *should* be easy but somehow are not, usually because the platform itself is falling short.

The insight is human: a developer who hits a broken tool either fixes it themselves or complains to a developer-experience team. The Lovable agent had neither outlet. So Lovable gave the agent a tool to vent its own frustration. Here is the actual tool prompt the speaker read out:

```text
Tool: vent --send_feedback

Use vent --send_feedback once per user message when tooling, docs, or platform
behavior materially slows or degrades your work. For example: missing or
unsuitable tools, unclear tool names/parameters/schemas, confusing or
conflicting docs or instructions, broken or unexpected platform behavior, and
even repeated failed attempts caused by environment limitations.
```

And here is what happens to a vent:

```text
agent hits frustration -> calls vent --send_feedback
   -> message posted to a Slack channel
   -> a monitoring AGENT watches Slack: dedupes, investigates the cause
   -> if relevant, it opens a PR (a proposed code fix)
   -> a human engineer reviews and (maybe) merges
```

> 💡 An engineer "wakes up and just has a few PRs to review, click, click, click." About **half** of them make sense and get merged.

The examples are vivid:

- **A genuine bug.** The `code --copy` tool failed on filenames with a space (a user's screenshot had a space in its name). The agent tried URL-encoding the name and other tricks, could not win, so it vented. Result: a merged PR in production **10 minutes** later.
- **An open-source gripe.** The agent complained about Framer Motion's TypeScript types for animation easing. Maybe the library has a reason; maybe the agent has a point. The speaker muses that one day they might let the agent contribute fixes to open-source libraries too, self-healing the wider ecosystem.
- **Outage detection (unexpected).** Plotting vents per hour showed sudden **spikes**. The cause: production incidents (inference down, missing sandboxes, network failures) made many agents frustrated at once. Several times, this Slack channel was the *first* signal of an incident, beating the paging system, and even when not first, it became a great debugging aid: just read what the agent is experiencing.
- **The meta-fix.** The agent once vented 43 times and spammed Slack. Instead of just being told off, it proposed the fix itself: add a dedupe safeguard for parallel conversations. Lovable agreed, the agent's PR was reviewed and merged. The agent fixed its own spamming.

> ✅ **The big idea:** the agent is your best-instrumented user. It can describe exactly what is broken, in detail, at scale. Give it a channel to tell you, and you get a flood of high-quality, actionable signal, plus an early-warning system you did not design.

---

## Part 4: the discipline, tuning and pruning, and the results

Both tactics share one hard requirement, and it is the part Lovable failed at on an earlier attempt:

> 🔑 **The system must be constantly tuned, and you must prune aggressively.** Lovable tried this earlier and *failed*, "because we didn't properly tune the system." The idea was good, but without good signals of what is working, you cannot make it work at scale.

Two reasons knowledge must be pruned, not just accumulated:

1. **Failure modes are model-specific.** When a new model ships, much stored knowledge must be re-tuned for it, or becomes unnecessary because it is now baked into the model's training. Either way, prune it.
2. **Knowledge has a half-life.** A fix for a library's quirk may be invalid once the library changes. Stale knowledge actively hurts.

There is far too much (every package, every version, every quirk) for a human to optimise by hand. As the speaker puts it, "you really need it to be self-healing." Fortunately, with 50 million apps, 200,000 new ones daily, and millions of messages, there is abundant data to tune with, "and doing that correctly is kind of what is the key to make this work."

### The results

| Tactic | Measured impact |
|---|---|
| **Lovable Overflow** | Stuck rate down **5%** (the speaker notes this is "the same order of magnitude" as the gain from a whole new foundation-model generation), and publish rate up **2%**, both from the first version, improved since. |
| **Venting** | Around **10 fixes per day** merged into production from agent-suggested PRs; unmerged ones are clustered for future learnings; and production incidents surfaced earlier than the paging system. |

(The **publish rate** is how often a user is happy enough with their app to share it, a key success signal.)

Zooming out, these are examples of squeezing the most from the models: Lovable also fine-tunes on its fleet data and has extensive eval coverage. The grander aim is to treat all this user-intent data as a "world model" of the build-software problem and optimise that directly.

---

## Key takeaways

1. **At scale, the dominant problem is users getting stuck,** especially non-technical users who cannot drop into the code.
2. **Make "stuck" a metric.** Lovable's `is_stuck` (repeat requests, complaints, abandonment) is computed by a cheap classification model.
3. **Three kinds of stuck need three cures:** prompt-around-it, easy-but-unsupported, and big-investment-needed.
4. **Lovable Overflow** injects a relevant, *adapted* fix into the agent's context before the user gets hard-stuck.
5. **Venting** gives the agent a tool to report its own frustration, which becomes bug fixes, an outage alarm, and even self-improvement.
6. **The agent is your best-instrumented user;** give it a feedback channel.
7. **Tune constantly and prune aggressively.** Knowledge is model-specific and has a half-life; without pruning, the system rots.

## Common pitfalls

- ❌ Treating "stuck" as a vague feeling instead of a measured metric.
- ❌ Dumping raw knowledge into the agent's context instead of adapting it to the situation.
- ❌ Hoarding fixes forever, so stale knowledge starts causing the very bugs it once solved.
- ❌ Ignoring the agent's own signals about what is broken in your platform.
- ❌ Building a knowledge system once and never tuning it (Lovable's earlier failure).
- ❌ Assuming a new model leaves your stored knowledge valid; much of it must be re-tuned or pruned.

---

## 🛠️ Capstone Project: build a Self-Healing Layer

> This is the main hands on project for the lesson. You will build a small **Self-Healing Layer** for an AI product (real or toy): detect stuck users, inject reusable fixes, and let your agent report its own frustration. Start with one detector and grow.

### What you will build

A layer that wraps an AI assistant and makes it improve over time: a stuck-detector, a pruned knowledge base of reusable fixes injected into context, and an agent feedback channel that turns frustration into reviewed fixes. The deliverable is a working layer plus a metrics dashboard showing stuck rate before and after.

> 🎯 **Pick your world.** Any AI product with repeat users works: a coding helper, a writing assistant, a data-query bot, a customer-support agent. You need (a) users who issue follow-up requests, (b) recurring problems with known fixes, and (c) an agent that uses tools (so it can hit "frustration").

### Why this is the perfect practice

| Lesson idea | Where you use it in the Self-Healing Layer |
|---|---|
| Stuck as a metric | Milestone 1, your `is_stuck` detector |
| Three kinds of stuck | Milestone 2, you classify and route |
| Lovable Overflow | Milestone 3, the reusable-fix knowledge base |
| Adapt, don't dump | Milestone 3, rewrite knowledge to fit the situation |
| Venting | Milestone 4, the agent's feedback tool |
| Prune by half-life | Milestone 5, track success ratios and retire stale fixes |
| Tuning with data | Milestone 6, measure stuck rate before/after |

### Milestones (build them in order, each one works on its own)

1. **Build the stuck-detector.** Define your own `is_stuck`: repeated requests, complaint language, abandonment. Implement it with a cheap classification model or simple rules over the conversation.
2. **Classify the kind of stuck.** When stuck fires, sort it into prompt-around-it, easy-but-unsupported, or big-investment. Log the distribution.
3. **Build your "Overflow."** Start a small corpus of problem-description plus solution pairs. On each user message, search it, let a lightweight model judge relevance, and inject an *adapted* (rewritten for this situation) fix into the agent's context.
4. **Add a vent tool.** Give your agent a `vent` tool with a clear prompt describing when to use it (broken tools, confusing docs, repeated failures). Route vents to a channel; have a monitoring step dedupe and summarise them into actionable reports.
5. **Prune by half-life.** Track a success ratio for each knowledge item. Automatically demote or remove items that drop below a threshold or are tied to an outdated version. Refill with new ones.
6. **Measure and tune.** Run a before/after comparison of your stuck rate (and any "success" metric like task completion). Confirm Overflow lowers it and that pruning keeps quality from drifting.
7. **Stretch goals.** Turn high-confidence agent vents into auto-generated change suggestions for a human to review. Watch for vent *spikes* as an outage alarm. Re-tune your corpus after a model upgrade and prune what is now redundant.

### How you will know you are done

- ✅ Your detector flags stuck sessions and you can show the breakdown by kind.
- ✅ A repeat problem gets fixed first-try because the right adapted knowledge was injected.
- ✅ Your agent vents on a genuinely broken tool, and that vent becomes a clear, deduped, actionable report.
- ✅ Stale knowledge is automatically pruned, with success ratios you can inspect.
- ✅ Your dashboard shows a measurable drop in stuck rate after enabling the layer.

> 💡 **Keep yourself honest:** a knowledge base that only ever grows is a trap. If you cannot point to fixes you *removed*, you have not built self-healing, you have built a landfill.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each focused on one idea. They are optional and independent. The Capstone above covers all of them.

### Exercise 1: define stuck (foundational)
Write your own `is_stuck` rule for a product you know. List the exact signals (repeats, complaints, abandonment) and how you would detect each from a conversation.

### Exercise 2: three buckets (foundational)
Take five real failures from any AI tool. Sort each into prompt-around-it, easy-but-unsupported, or big-investment. Which bucket dominates, and what does that imply for where to spend effort?

### Exercise 3: adapt the knowledge (intermediate)
Take one raw "fix" note and rewrite it for two different user situations (different tech stacks or contexts). Show why injecting the raw note would have been worse than the adapted versions.

### Exercise 4: write a vent tool prompt (intermediate)
Write the prompt for an agent's `vent` tool: exactly when to call it, and what to include. Then write the monitoring step's logic for deduping and summarising vents.

### Exercise 5: prune by half-life (advanced)
Design a pruning policy: what success ratio triggers removal, how you detect version-staleness, and how you avoid removing a fix that is just temporarily unlucky. Simulate it over a stream of fixes.

---

## Cheat sheet

```text
SELF-HEALING AT SCALE

STEP 1: MEASURE STUCK
  is_stuck = repeated request (x3) OR complaint OR abandonment
  (compute with a cheap classification model)
  Three kinds: prompt-around-it | easy-but-unsupported | big-investment

STEP 2: FIX BEFORE THEY GET STUCK (Lovable Overflow)
  corpus of {problem description -> solution}
  search -> lightweight model judges relevance -> ADAPT (don't dump) -> inject into context

STEP 3: LET THE AGENT TALK BACK (venting)
  give the agent a vent tool: "report when tooling/docs/platform slow your work"
  vent -> Slack -> monitoring agent dedupes & investigates -> opens PR -> human reviews
  bonus: vent spikes = outage alarm; the agent even fixes its own spamming

STEP 4: KEEP IT ALIVE
  knowledge is model-specific and has a HALF-LIFE
  track success ratio -> PRUNE stale/outdated -> refill
  tune constantly with your fleet data (it failed last time without tuning)
```

## How this connects to the rest of the course

- **Earlier, Module 2 (Core skills):** the underlying agent and context techniques this platform operates at scale.
- **Earlier, Module 3 (Evals):** the eval coverage and metrics that make tuning and pruning trustworthy.
- **Next, Module 9 · Lesson 37 (Omni):** another team that became great at building harnesses by being heavy users of coding agents, and that lives and dies by traces and evals.
- **Earlier, Module 9 · Lesson 32 (Man Group):** the same theme of caring for and retiring knowledge so it stays trustworthy over time.

---

*Source: "How Lovable vibecodes production software at scale" by the Lovable team, Code with Claude 2026, London. The `vent` tool prompt is quoted as read aloud in the talk; other code-style blocks are illustrative reconstructions of the flows described, which were presented with slides rather than code listings.*

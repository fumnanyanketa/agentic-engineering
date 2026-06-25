# Module 8 · Lesson 29: From One Person to 80, Scaling a Hypergrowth Engineering Org

> **Course:** Building with Claude, a self-paced course
> **Module 8:** Leading the AI-native transformation
> **Speaker:** Yoav (Head of Product, Base44) and Gabriel (Head of AI / lead of the app builder agent, Base44)
> **Source talk:** [From one person to 80: Scaling a hypergrowth engineering org with Claude Code](https://www.youtube.com/watch?v=VueeyKcquoA) · [full transcript](../../transcripts/code-with-claude-2026-london-2026/18_from-one-person-to-80-scaling-a-hypergrowth-engineering-org-with-claud.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

Base44 grew from a single founder to 80 engineers without losing speed by refusing to build heavy processes too early: at each stage they solved onboarding, code review, evals, experimentation, and QA with the simplest possible thing (often just a prompt or a skill), and only built sophisticated systems when the team was actually big enough to need them.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you take one scaling pain on a team you know and solve it the Base44 way: start with the simplest possible automation (a single prompt), then upgrade it only as far as the team's size justifies. Everything before the Capstone teaches the patterns you will reuse. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[The Mythical Man-Month (Fred Brooks)](https://en.wikipedia.org/wiki/The_Mythical_Man-Month)** (book). The enduring classic on what breaks as engineering teams grow (Brooks's Law, communication overhead), the backdrop to "don't add heavy process too early."
> - **[Accelerate / the DORA research](https://dora.dev/research/)** (docs). Evidence-based grounding for keeping process lightweight and metrics-driven as you scale.

## A few plain-language basics first

This talk moves fast through several technical ideas. Here they are in plain words:

- **Vibe coding:** building software by describing what you want in natural language and letting AI write the code. Base44 is a platform that lets anyone (technical or not) build apps this way.
- **PR (Pull Request):** a proposed code change someone reviews before it joins the product. "Merging" means accepting it.
- **Onboarding:** the process of getting a new team member up to speed.
- **Mermaid chart:** a simple diagram (like a flowchart) written as text, which tools can render into a picture. Useful for showing how a piece of software works.
- **Eval (evaluation):** a set of test cases you run to measure whether your AI behaves correctly. Building a full eval suite is a big effort.
- **A/B test:** showing version A to some users and version B to others, then comparing results, to learn which is better.
- **PostHog and BigQuery:** PostHog is a product for running A/B tests and experiments. BigQuery is a data warehouse (a big store of a company's data). Both are connected as data sources.
- **MCP (Model Context Protocol):** an open standard that lets Claude connect to outside tools and data (for example, PostHog) and use them.
- **Skill:** a reusable instruction file you give Claude so it knows how to perform a specific task (like running a test flow) without re explaining every time.
- **CI/CD pipeline:** the automated system that builds, tests, and ships code (Continuous Integration / Continuous Delivery).
- **Stagehand / Playwright:** tools that let software control a web browser automatically, so an agent can click around an app like a person would.
- **Compaction:** a way of summarising a long conversation so the model can keep working without running out of room for context.

You do not need to memorise these. Each one is explained again the first time it matters below.

## Why this lesson matters

Most advice about scaling teams tells you to add process: write the onboarding doc, set up the eval suite, form the review committee. Base44's story is the opposite. Their hard won lesson is that the right amount of process depends on the size of the team, and adding it too early slows you down. They got immediate product market fit (lots of paying customers, fast), which forced them to scale faster than usual. By keeping every solution radically simple until the moment it truly needed to grow, they went from 1 to 80 engineers while keeping velocity. This lesson gives you their concrete patterns for each scaling stage, and a way to judge *when* simple is enough and *when* it is time to go all in.

> 🔑 **The thread through the whole talk (paraphrased from Yoav):** keep everything very, very simple. Work hard *not* to build complex things when it is not the right time. Then, when the moment comes, go all in.

## Learning objectives

By the end of this lesson you will be able to:

1. Solve onboarding, code review, and product validation with a single prompt or skill instead of a heavy process.
2. Encode your team's "taste" by having Claude distill it from your past actions (PR comments, past experiments) rather than holding a guidelines meeting.
3. Build a simple but real signal for whether your AI product is working, using production traffic.
4. Judge when a lightweight hack is enough and when the team is finally big enough to invest in a full eval suite or automated QA.
5. Apply the "bottleneck keeps moving" mindset so you keep solving the next constraint, not the last one.

## Prerequisites

- A basic understanding of how a software team ships changes (PRs, reviews, tests). No coding required to follow the ideas.
- Helpful but optional: Module 3 (Evals), since evals and a "user simulator" appear in Part 2.

---

## Part 1: from 1 to 15 engineers (Yoav)

Base44 started at the end of 2024 as a vibe coding platform (building apps by describing them in natural language). By 2025 it had a working product; the founder built in public on LinkedIn and Twitter, gained traction, and by April 2025 it was profitable. That profitability and a fast growing, AI focused user base attracted acquisition interest, and Wix (a company with a very similar user base) acquired it. Wix wanted to keep Base44's velocity but expand it dramatically, so a two person team had to scale into a 15 person engineering team "as fast as possible."

Four challenges came with that growth, and none of the old "just do it manually" answers scaled:

| Challenge | Why it broke at 15 people |
|---|---|
| **Onboarding** | The founder (Maor) could not personally onboard every new engineer. |
| **Code review** | Maor was very cautious about what went into the backend, and wanted to review every PR himself. That does not scale. |
| **Product validation** | They could not have each engineer sit with a beta tester to check the product works. |
| **Huge product surface** | Immediate product market fit meant many areas (integrations, the agentic flow, the visual editor), and engineers had to ramp up fast. |

> 🔑 **The key instinct:** the meeting to solve these started heading toward "let's build a process where we review everything and build an onboarding doc and a nightly job to update it." They stopped and said: no, keep it very simple.

### Onboarding: two prompts, no docs

Instead of writing and maintaining onboarding docs, every new engineer runs two prompts before starting their first task:

```text
ONBOARDING PROMPT 1 (the org map)
  "Go over all the commits and tell me what everyone cares about."
  -> Gives a new joiner a real-time map of who owns and focuses on what.

ONBOARDING PROMPT 2 (the component map)
  "Can you give me a mermaid chart of how this component works?"
  -> A live diagram of the area they're about to work in.
```

> 💡 The genius here is that nothing goes stale. A document needs constant updating; a prompt reads the *current* state of the code base every time. "You don't need to think about how do I keep these onboarding docs updated... a simple prompt gives you in real time the entire map of the organization."

### Code review: amplify the founder, do not replace him

Maor cared deeply about backend quality. After a week or two of him reviewing PRs, there was a big pool of his review comments in the repo. Instead of brainstorming review guidelines from scratch, they had Claude read those PR comments and extract the most important and crucial things to keep in mind. They put that into an instruction, ran it every couple of days, and effectively got a "Maor PR Reviewer" inside Base44 without building a sophisticated process.

The payoff was visible. They handed a new engineer a WhatsApp integration (a feature requiring a new integration, work on the agentic flow, and a new Meta API). They expected one to two weeks. The engineer onboarded Thursday using the two prompts, and by Sunday morning it was ready. The PR review had two or three small comments, and it shipped.

> ✅ **Best practice: encode taste from past actions.** You do not need a guidelines committee. Have Claude read what your team already did (review comments, past decisions) and distill the guideline. It will not be perfect, but you get a working version in hours, then iterate.

### Product validation: let users tell you, for free

When the team was tiny, they sat with customers to watch them use Base44. At 15 people, that does not scale. The "naive AI company" answer is "let's build an eval suite," but Yoav is blunt: a 15 person team is usually not ready for that effort.

So they used the production traffic they already had. They noticed a simple pattern in conversations: when things work, the user says nothing and just moves to the next feature. When things break, "users get really, really loud in the chat," saying "why is this broken?" That loudness is a strong, free signal.

```text
THE FRUSTRATION SIGNAL
  1. Use a small, cheap model to classify each user message:
     is frustration level HIGH or LOW?
  2. Roll out a new agent version to a small percentage of customers.
  3. Track the frustration level for that group.
  Works whether you changed the infra, the prompt, or the model.
```

> 🔑 **The pattern:** find a signal you already have in production, and read it cheaply, instead of building a heavyweight evaluation system before you need one. "You have a very simple way of getting almost the same amount of value while keeping processes really, really lean."

---

## Part 2: from 50 to 80 engineers (Gabriel)

A few months later, Base44 hit a new growth phase: more external hires, internal movers from Wix, and a merged Vibe coding product. "In one single night, we doubled our headcount from 40 people to almost 80." That brought new challenges where the simple hacks from Part 1 were no longer enough. Gabriel focuses on the three most interesting ones.

### Challenge 1: experimentation at scale

You cannot expect every new hire to know which KPIs to test, how long to run a test, or when it is fine to just ship without an experiment. So the team wanted to **shift left** (move earlier in the process) the product management decisions around A/B testing, so they happen automatically when a PR is ready.

They started with the easy "shell" of what they wanted: a process that runs when a PR is ready, a bot commenting on GitHub telling the developer whether to just ship, gradually roll out, or A/B test (and for how long, and which KPIs to watch), and that opens the experiment in PostHog (their A/B testing tool).

The hard part was the *guidelines*, the actual logic of how they make these decisions. They had never written it down; they just had "really good product sense and intuitions." Their two options were a multi stakeholder guidelines committee with lots of meetings ("we really hate meetings"), or:

```text
DISTILL GUIDELINES FROM PAST ACTIONS
  1. Take the last 100 experiments from PostHog + their matching PRs.
  2. Spawn Claude Code, hooked to the PostHog MCP.
  3. Ask Claude to suggest the first draft of the guidelines.
  -> Rough on the edges, but a working document in a couple of hours, then iterate.
```

Now every PR gets a clear verdict: just ship, gradual rollout, or A/B test (and for how long). For their scale, some features need 7 days of testing, some need a full month because they might move conversion or premium rates by tiny percentages. To make it visible, they dogfooded their own product, Base44, building a central dashboard connected to BigQuery, PostHog, and GitHub, so everyone can see which experiments are running and how they are moving the needle.

> 💡 This is the same "encode taste from past actions" move as Part 1's code review, now applied to experimentation. It ties to the broader idea that you can capture a big chunk of your team's taste by looking at what you actually did, not by holding a meeting about it.

### Challenge 2: better evals (now it is the right time)

In Part 1, evals were *not* the best return on investment for a small team. At 80 people, they became something the team really needed. But the challenge was short term: deliver real value without a three month project or pulling away their top AI engineers.

The key question: do we just evaluate the model's raw output, or check whether the *apps users build actually work*? The answer led to a **user simulator**. And a crucial epiphany: for Base44, when a user asks for an app and some small part does not work, that does not mean the eval failed. A real user would just ask the agent to fix the missing part. So the eval suite must pipe the rejection back and ask the agent to fix it, the way a real user would.

```text
THE EVAL PIPELINE (a robot QA engineer)
  - Any change to AI code spins up a real Base44 app instance.
  - Use stagehand (browser automation) to simulate real user actions.
  - Measure: latency, number of turns, cost to us, credits used by users.
  - Pipe back rejections and ask the agent to fix the missing parts.
```

Their most canonical eval is a **smoke test** (a quick check that nothing is fundamentally broken): ask Base44 to build a "Hello World" app, assert the right text is visible and it "looks good" (judged subjectively, trusting AI to flag failures), then ask for a small text change, then a small feature. Most pass, and a fun fact: these basic evals pass even on the smallest model. They also have complex evals: starting from an existing app and making many changes, and testing the compaction mechanism (summarising long conversations) which needs many user messages.

> 🔑 **The timing lesson:** "We held it off until it was the right moment to build it, and then we went all in." Evals were the wrong investment at 15 people and the right one at 80. Knowing *when* is as important as knowing *how*.

### Challenge 3: streamlining QA without growing testers linearly

The team believes in shifting left quality (unit tests, end to end tests, full ownership of what you build). But deep features have many edge cases. Gabriel's example: a feature that only affects users at a specific subscription tier when they hit a specific point of their credit limit, with many permutations. Testing all of that manually is tedious, and handing it to a human QA engineer means longer feedback loops and waiting for someone to be free.

They knew Claude Code could drive a browser (via Playwright, browser use, and similar tools). But it was missing two critical pieces:

1. **Knowing the platform.** Each time, Claude had to relearn the app's flows, the selectors (how to find buttons on a page), and which events to look for in the database. They fixed this by wrapping common flows in **skills**. One skill taught Claude how to walk all the major user flows that most features touch. The aim was not 100% coverage; "you just need to maximize the 80% so you have enough context," then trust Claude for the rest.
2. **Setting up the test state.** A good QA engineer goes into the database and overrides the setup so they can test a specific edge case. Claude needed the same power. So they built **CLI tools** (command line tools) that abstract their APIs and databases specifically for setting up tests, and skills that taught Claude how to use them.

They combined everything into one **meta skill** for how to do proper QA. Now when a PR opens, the agent triggers, creates a test plan, runs it against a Base44 app (dogfooding again), and reports back with screenshots of what it tested and what it did not. When Gabriel pushes it past its limits, "it will just write, like, I couldn't test that, and surface the missing capabilities." It works for 80% of cases, letting them shift left even deep, edge case quality assurance.

> ✅ **Best practice: give the agent the same powers a good human has.** A human QA engineer needs to know the flows *and* set up the database. So give Claude skills for the flows and CLI tools for the setup. Aim for 80% coverage and trust the agent on the rest.

---

## Part 3: the common thread

Gabriel closes with the threads running through every solution:

1. **Value simplicity.** Think "bold and simple." Work hard *not* to build complex things when it is not the right time. Evals are the example: held off until the right moment, then all in.
2. **Encode taste from past actions.** Taste is the "last moat" of humans against machines, but you can encode a big chunk of your team's taste by looking at what you actually did, for code reviews, A/B testing, anything. (This connects to the idea of giving Claude memory of your recent decisions.)
3. **Use your own product if you can.** Dogfooding gives you a magical feedback and insight loop. If you work on a finance app you may have to stretch, but find ways to do it.
4. **The bottleneck keeps moving.** The current challenge is no longer the ones above; it is **post validation**: once a PR reaches production, how do you confirm it moved the right needle? Is a bug fix really reducing support tickets? Is a feature really being used? You do not want a human holding that in their head, so the next thing to automate is exactly that.

> 🔑 **The single most reusable idea:** match your process to your team size. The same problem (review, validation, evals) deserves a one prompt hack at 5 people and a full system at 80. Adding the big system early is the mistake.

---

## Key takeaways

1. **Right size your process.** A one prompt hack at 5 people; a full system at 80. The crime is building the heavy system too early.
2. **Onboard with prompts, not docs.** "Read the commits, tell me who cares about what" and "draw a mermaid chart of this component" stay current automatically.
3. **Encode taste from past actions.** Have Claude distill review guidelines from past PR comments, and experimentation guidelines from past experiments. No committee needed.
4. **Find a free production signal.** Loud, frustrated users are a strong signal. Classify it with a cheap model and track it per agent version.
5. **Know when it is time for evals.** Hold them off when the ROI is low; go all in when the team is big enough to need them. Build a user simulator that pipes rejections back, like a real user.
6. **Give agents human powers.** Skills for the flows, CLI tools for the test setup. Aim for 80% coverage and trust the agent on the rest.
7. **The bottleneck keeps moving.** Today's win exposes tomorrow's constraint (now: post validation in production).

## Common pitfalls

- ❌ Building an onboarding doc, eval suite, or guidelines committee before the team is big enough to need it.
- ❌ Holding a meeting to write down "our guidelines" when Claude could distill them from your past actions in hours.
- ❌ Trying to sit with every customer (or have every engineer do so) once you pass a handful of people.
- ❌ Treating any failed step inside an AI product as an eval failure, when a real user would just ask for a fix.
- ❌ Expecting Claude to do QA without giving it the flows (skills) and the test setup (CLI tools) a human QA engineer would use.
- ❌ Solving the last bottleneck forever instead of moving on to the new one.

---

## 🛠️ Capstone Project: The Right-Sized Scaling Kit

> This is the main hands on project for the lesson. You will take one real scaling pain and solve it the Base44 way: start with the simplest possible automation, then upgrade it exactly as far as your team's size justifies, and no further.

### What you will build

A small, working "scaling kit" for one chosen pain (onboarding, code review, product validation, experimentation, or QA), delivered at two sizes: a **tiny version** (one prompt or skill, buildable in an afternoon) and a **scaled version** (a real automation or dashboard), plus a one paragraph note explaining at what team size you would switch from one to the other.

> 🎯 **Pick the pain that hurts most right now.** If onboarding is slow, build the two onboarding prompts. If review is a bottleneck, distill a reviewer from past comments. If you ship blind, build the frustration signal. Choose one and go deep.

### Why this is the perfect practice

| Lesson skill | Where you use it in the Capstone |
|---|---|
| Onboard with prompts, not docs | Onboarding track, the two prompts |
| Encode taste from past actions | Review / experimentation track, the distilled guideline |
| Free production signal | Validation track, the frustration classifier |
| Knowing when to build evals | The "switch size" note |
| Give agents human powers | QA track, skills plus CLI tools |
| Bottleneck keeps moving | The closing reflection |

### Milestones (build them in order, each one is shippable)

1. **Name the pain and the team size.** One paragraph: which scaling pain are you solving, and how many people are on the team today?
2. **Build the tiny version.** Solve it with the smallest possible thing. Examples: the two onboarding prompts; a "reviewer" instruction distilled from a real pile of past PR comments; a cheap model that classifies user messages as high or low frustration; a guideline distilled from past experiments; one QA skill for your main user flow.
3. **Run it for real.** Use the tiny version on at least one real task (onboard one person, review one PR, classify one batch of messages). Capture the result.
4. **Build the scaled version.** Now upgrade exactly one notch: a dashboard (dogfood your own product if you can) that shows the signal over time; or a CI step that comments a ship / rollout / A/B-test verdict on every PR; or a user simulator that builds an app, asserts it looks good, and pipes rejections back.
5. **Write the "switch size" note.** One paragraph: at what team size does the tiny version stop being enough, and the scaled version become worth it? Justify it the way Gabriel justified holding evals until 80 people.
6. **Name the next bottleneck.** Predict what your solution will expose next (for example post validation in production: did this change actually move the needle?). Write one sentence on how you would automate it.

### How you will know you are done

- ✅ Your **tiny version** works and you ran it on a real task.
- ✅ Your **scaled version** works and adds value the tiny one could not (visibility, automation, coverage).
- ✅ At least one part **encodes taste from past actions** (distilled from real history, not written by committee).
- ✅ Your "switch size" note gives a **specific team size** and a reason.
- ✅ You named the **next bottleneck** your solution exposes.

> 💡 **Keep yourself honest:** if you reached for a committee, a long doc, or a three month project, ask whether a single prompt or skill would get 80% of the value first. Build complex only when the team size truly demands it.

---

## Practice exercises (optional extra reps)

> **What these are:** small, independent reps, each focused on one move from the talk. Optional. The Capstone above exercises all of them together.

### Exercise 1: the onboarding prompts (foundational)
On any code base you can access, run "go over the recent commits and tell me what everyone cares about" and "draw a mermaid chart of how this component works." Compare the result to whatever onboarding doc exists.

### Exercise 2: distill a reviewer (foundational)
Gather 20 to 50 past code review comments from a repo. Ask Claude to extract the most important recurring rules. You now have a draft "reviewer" instruction. Iterate once.

### Exercise 3: the free signal (intermediate)
Take a batch of real user messages (support chats, app reviews). Use a cheap model to classify each as high or low frustration. Could you track this per release? What would it tell you?

### Exercise 4: the user simulator mindset (intermediate)
Pick an AI feature. Write down what a *real user* would do if a small part failed (hint: ask for a fix). Sketch an eval that pipes that rejection back to the agent instead of marking it a failure.

### Exercise 5: agent-powered QA (advanced)
Write one skill that teaches Claude to walk your app's main user flow in a browser, plus a note on what CLI tool or database override it would need to set up a tricky edge case. Aim for 80% coverage, not 100%.

---

## Cheat sheet

```text
RIGHT-SIZE YOUR PROCESS
  5 people:  one prompt or skill.
  80 people: a real system (dashboard, CI bot, user simulator).
  The crime is building the big system too early.

ONBOARDING (no docs)
  "Read recent commits; tell me who cares about what."
  "Draw a mermaid chart of how this component works."
  Stays current automatically.

ENCODE TASTE FROM PAST ACTIONS (no committee)
  Reviews: distill rules from past PR comments.
  Experiments: distill guidelines from the last 100 experiments + PRs.

FREE PRODUCTION SIGNAL
  Happy users go quiet; frustrated users get loud.
  Classify frustration with a cheap model. Track per agent version.

EVALS: KNOW WHEN
  Wrong investment when tiny. Go all in when big.
  Build a user simulator that pipes rejections back, like a real user.

AGENT QA = HUMAN QA POWERS
  Skills for the flows + CLI tools for the test setup. Aim for 80%.

AND REMEMBER
  Dogfood your own product. The bottleneck keeps moving (next: post validation).
```

## How this connects to the rest of the course

- **Earlier, Module 8 · Lesson 27 (Running an AI-native engineering org):** the same "audit your processes, do not let them pile up" mindset, here applied stage by stage as a team grows.
- **Earlier, Module 8 · Lesson 28 (Designing with Claude):** another small team going fast by refusing heavy process and dogfooding relentlessly.
- **Earlier, Module 3 (Evals):** the deeper foundation behind the user simulator and the "when is it time for evals" decision.
- **Next, Module 8 · Lesson 31 (Building AI-native at enterprise scale):** the same patterns (encode taste, A/B test, skills marketplaces) at companies many times Base44's size.

---

*Source: "From one person to 80: Scaling a hypergrowth engineering org with Claude Code" by Yoav and Gabriel (Base44), Code with Claude 2026, London. The prompt and pipeline boxes are faithful paraphrases of what the speakers described; they are illustrative reconstructions, not verbatim slides.*

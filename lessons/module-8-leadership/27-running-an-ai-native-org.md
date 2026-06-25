# Module 8 · Lesson 27: Running an AI-Native Engineering Org

> **Course:** Building with Claude, a self-paced course
> **Module 8:** Leading the AI-native transformation
> **Speaker:** Fiona Fung, Head of Engineering and Product for Claude Code and Cowork, Anthropic (previously Meta and Microsoft)
> **Source talk:** [Running an AI-native engineering org](https://www.youtube.com/watch?v=IA5LWIGqnyM) · [full transcript](../../transcripts/code-with-claude-2026-london-2026/03_running-an-ai-native-engineering-org.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

When coding stops being the slow part of building software, the old team habits that protected engineering time quietly stop working, so you have to audit every process, rewrite the ones that no longer serve their purpose, and measure whether the changes actually helped.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you run a real "process audit" on one of your own team's workflows, turn one slow ritual into a small automation, and measure the before and after. Everything before the Capstone teaches the way of thinking you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section near the end, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[Theory of Constraints](https://en.wikipedia.org/wiki/Theory_of_constraints)** (essay). The lesson's whole frame, "the bottleneck has moved; optimise the new constraint, not the old one," is Goldratt's Theory of Constraints applied to engineering.
> - **[The Goal (Eliyahu Goldratt)](https://en.wikipedia.org/wiki/The_Goal_(novel))** (book). The narrative that made bottleneck thinking durable management canon.

## A few plain-language basics first

This is a leadership talk, so most of the terms are about how teams work rather than about code. Here they are in plain words:

- **Bottleneck:** the slowest step in a process, the one that holds everything else up. If coding is the bottleneck, nothing ships faster than people can write code.
- **Team norm:** an unwritten or written habit a team follows, for example "every change gets a design doc" or "every pull request needs two reviewers."
- **IC (Individual Contributor):** someone who does hands on work (writing code) rather than managing people. A manager who is "an IC first" rolls up their sleeves and writes code before taking on people responsibilities.
- **PR (Pull Request):** a proposed change to the code that someone reviews before it becomes part of the product. "Merging" a PR means accepting it.
- **CI (Continuous Integration):** an automated system that builds and tests every change. If CI is slow, your changes wait in a queue even when the code itself is done.
- **Dogfooding:** using your own product yourself, every day, the way a customer would. (Anthropic jokingly calls this "ant food.")
- **Source of truth:** the one place a team trusts for accurate, up to date information. It used to be a document; this lesson argues it should often be the code itself.
- **Shift left:** catching problems earlier in the process (closer to where they start) instead of later. The earlier you catch a bug, the cheaper it is to fix.
- **Claude Code:** Anthropic's command line tool that lets Claude read, write, and run code in your project. **Cowork** is a related product for getting work done with Claude. Both are what Fiona's team builds.

You do not need to memorise these. Each one is explained again the first time it matters below.

## Why this lesson matters

For decades, engineering time was the expensive, scarce thing, so almost every team process was built to protect it: heavy planning, careful reviews, design docs before any code. Fiona's core observation is that this assumption has flipped. On her team, "coding is rarely the slow part anymore." When the bottleneck moves, the processes built around the old bottleneck do not announce that they are obsolete. They just "quietly stop working." This lesson gives you a repeatable way to find those stale processes, rewrite them, roll the changes out, and prove they helped, so your team speeds up instead of carrying dead weight.

> 🔑 **The one saying to remember:** "What served you prior may no longer." Fiona calls this her favorite mindset, the muscle that helped her at Anthropic, Meta, and Microsoft. Always ask of any process: is it still serving its purpose?

## Learning objectives

By the end of this lesson you will be able to:

1. Recognise when a bottleneck has moved on your own team, and name the processes that were built to protect the old bottleneck.
2. Rewrite the most affected team norms (planning, code review, onboarding, code ownership, org shape) for a world where coding is cheap.
3. Decide what humans must still own (taste, risk, legal, product sense) versus what to hand to Claude.
4. Roll out changes the way Fiona did: align top down on a few non negotiables, and leave room for bottom up adaptation.
5. Pick honest signals to prove the changes are working, and avoid being fooled by a single throughput number.

## Prerequisites

- A basic understanding of how a software team ships changes (writing code, reviews, merging). No coding required to follow the ideas.
- Helpful but optional: Module 2 (Core skills), so the references to tools, skills, and verification feel familiar.

---

## Part 1: the bottleneck has moved

Fiona opens with history, because this is not the first time the slow part of engineering has shifted. Back in the early 2000s at Microsoft, building Visual Studio meant one server room, a weekly on call rotation, and a build "queue" that could only merge six PRs at a time. If a test failed, someone had to debug which of those six changes broke it. That was the bottleneck. Then cloud computing and **continuous build** (automated building of every change) arrived, and the bottleneck moved somewhere else.

> 💡 The pattern repeats. Each big leap in tooling does not remove bottlenecks; it relocates them. Your job as a leader is to notice where the new one is, not to keep optimising the old one.

For years, the bottleneck was **engineering bandwidth** (how much code people could write and maintain). So teams did heavy planning to make sure they built the right thing, and heavy reviews to protect that scarce time. With Claude, coding, writing tests, and refactoring are no longer the slow steps.

A small story makes this concrete. Fiona wanted to try **test-driven development** again (TDD: writing the test first, watching it fail, then writing the code so the test passes). She had always found writing the test first to be a chore, "like eating broccoli." With Claude, that tax disappeared, and TDD became "so much more fun." Same with **refactoring** (cleaning up and restructuring existing code without changing what it does), which used to be a constant fight for time against shipping new features. It is no longer a bottleneck.

So where are the new bottlenecks? Fiona names three:

| New bottleneck | Why it grew | What it demands |
|---|---|---|
| **Verification** | Far more changes are flowing through, so "is it correct?" matters more, and more people are checking in changes as roles blur. | Automation that catches problems close to the source. |
| **Who reviews** | Throughput went up, so review can become the new queue. | A clear split of what Claude reviews versus what humans must. |
| **How it is maintained** | More code shipped means more code to keep working over time. | Watching the cost of maintenance, not just the cost of building. |

> 🔑 **The key phrase:** processes "quietly stop working." Someone put each process in place to solve a real problem. But teams rarely go back and audit whether the problem still exists. Old processes do not delete themselves; they pile up.

---

## Part 2: rewriting the team norms

Once the bottleneck moves, several long standing norms need rewriting. Fiona walks through the ones her team changed.

### Planning and technical debates: code wins

The old reflex for a tricky technical disagreement was to book a room and whiteboard it. Fiona almost did exactly that with a colleague, Boris, over a refactoring approach. Then she caught herself: instead of arguing in the abstract, she generated three different versions of the actual change as real PRs. That gave them something concrete to debate, including the impact on the rest of the team, not just how the code looked.

> 🔑 **Rule of thumb (quote):** "Building is cheap, arguing is expensive." (Fiona Fung) When a prototype is faster to make than a meeting is to schedule, build the prototype and debate that.

The same logic applies to **prototyping** (building a quick rough version to learn from). The old worry was that a prototype built with cut corners would get "stuck" and shipped as if it were production quality. With Claude, you can prototype to learn quickly *and* scale that prototype up to production far faster, so the old fear matters less.

**What the team reduced:** in depth design docs. Most discussion now happens in PRs or prototypes, because the engineering bandwidth to just build the thing is there.

### Verification: shift left

This is where Fiona wants her team to keep getting better. With so much more bandwidth, quality verification matters more, not less.

> ✅ **Best practice: shift left.** It is bad when a customer hits a bug. It is a little better when you hit it first. But the best outcome is automation catching it "closer to the source," before anyone runs into it. Keep moving checks earlier and automating more of them.

A practical tip: if you have a **spec** (a written description of how something should behave), check it into the code base. Claude is very good at catching "spec drift" (where the code has quietly diverged from what the spec says it should do).

### Code ownership and "who made this change"

Almost every commit on her team is now co-authored by Claude. The old question "who touched this last?" should be replaced by the real question behind it. Fiona's advice: when you catch yourself asking it, get to the root.

> 💡 Ask what you are *actually* after: Are you hunting a regression (a change that broke something)? Looking for context? Looking for someone to answer a question? In most of these cases, Claude can help you directly instead of pulling a busy colleague away from their work.

### Code review: where Claude is good, where humans stay

After shipping Claude Code's own code review feature, the team kept pace with the higher volume. Here is the division of labour:

| Claude reviews well | Humans must stay in the loop |
|---|---|
| Style and lint (formatting and simple rule checks) | Legal reviews |
| Obvious bugs | Anything about risk tolerance, especially trust boundaries |
| Spec drift (when a spec is checked into the repo) | Product sense and taste |

Fiona's "snowman" story makes the taste point stick. She coded a holiday version of Claude in the CLI meant to look like a snowman, and asked a designer to review it. The verdict: it looked nothing like a snowman, it looked like Mr. Peanut (a US snack mascot). She was sure it was a snowman; the designer's trained eye saw instantly that it was not. That product sense is the human expertise to keep in the loop.

### Team makeup and product sense

As roles blur and Claude augments everyone, Fiona focuses hiring on two engineering profiles: **creative builders with product sense**, and people with **deep system expertise**. Many engineers later asked her how to build the "product sense" muscle. Her answer:

> 🔑 **How to build product sense (paraphrased from Fiona):** dogfood relentlessly, iterate and ship, and talk to real customers. Dogfooding (using your own product daily) lets you "feel it in your bones" and remember what problem you were trying to solve. Without it, you start making product decisions from dashboards and slides alone.

She lived this by personally onboarding small business owners (restaurant friends) onto Cowork, and found humbling gaps in the onboarding flow she would never have seen from a metrics chart.

Claude also fills **cross functional gaps** for every role. Designers on her team now make their own polish and UX fixes with Claude instead of handing a "red line" (a marked up design) to engineering and waiting. And Fiona, who admits she writes too verbosely as an engineer, uses Claude as a content design partner to write short, clear copy.

### Org shape: managers start as ICs

This was the "spicy" slide. When Fiona joined Claude Code, she worked with recruiting so that **every manager starts as an IC first** (writing code before taking on people responsibilities).

> ✅ **Why this works:** it lets a manager learn what life is actually like for an engineer on the team before they are responsible for supporting people. And onboarding into the code base is far less daunting than it used to be, so managers can reclaim "maker hours" and stay close to the product.

### Knowledge sharing: code as the source of truth

When Fiona onboarded, the **code was the source of truth**, not a pile of documents. For her first bug fix she asked Claude to teach her the surface area and the surrounding code first. She still meets every engineer, but those conversations are now about what is top of mind rather than rote tech deep dives, because Claude answers the rote questions.

> 🔑 **Actionable rule:** whatever is your source of truth, keep it *in the code base*, whether that is a spec or a **skill** (a reusable instruction file you check in). Documentation that lives outside the update loop goes stale fast, and the faster you ship, the faster it rots.

---

## Part 3: how to roll the changes out

Changing team norms is its own skill. Fiona's approach balances two forces: align the team on a few must dos, and leave room for each pod (small sub team) to adapt.

**Aligned top down (the "forcing functions"), her team principles:**

```text
1. Every teammate uses Claude Code (and Cowork). Use our own product daily.
2. Claudify everything we can. For any task ask: what's better than me doing it?
   Can Claude do it for me, so I free up bandwidth for harder problems?
3. Explicit permission to kill old processes. Even our own principles get
   revisited: is this still serving its intended purpose?
```

**Left to bottom up (per pod freedom):**

- How Claude shows up in triage, planning rituals, or stand ups.
- Which workflows get "Claudified" first.
- Which tool chains resonate most with that team.

> 💡 The balance is the lesson: align on what matters for team culture and quality, update those as you learn, but leave each pod room to adapt the details. People closest to the work know which of their workflows to automate first.

Fiona's three biggest priorities, the ones that worked best:

1. **Keep the org agile and flat.** Managers support parts of the work but also own parts of the product directly and stay in the code base.
2. **Claudify.** If Claude can do it, Claude should. And revisit constantly, because the models keep improving: something Claude was bad at two or three months ago may be great now after a model update.
3. **Audit and delete processes.** People do not delete processes on their own; they pile up. Fiona once worked on a team with so many separate SLAs (Service Level Agreements, promises about how fast to respond to issues) that engineers asked her which one to obey, since there are only 24 hours in a day. The fix was a hard audit: which of these are still necessary?

---

## Part 4: the proof, choosing honest signals

How do you know the changes are working? Fiona shares the signals her team watches.

| Signal | Direction | What to watch for |
|---|---|---|
| **Onboarding ramp-up time** (time for a new engineer to land their first PR) | Down | A great sign. Also watch the "cost to other team members," which drops when Claude answers onboarding questions. |
| **PR cycle time** (how long a change takes end to end) | Down, but be careful | If it is *not* going down, it may not mean low AI adoption. Another part of the queue (like CI) may be jammed by the extra throughput. **Break it into chunks** and find the one to fix. |
| **Claude-assisted commits** | Up | On her team, nearly every commit in recent months was Claude assisted. |

> 🔑 **The most important caveat (paraphrased from Fiona):** throughput is not the goal. Whatever your team is actually trying to solve (a product outcome, a quality improvement), find a way to measure *that*. More PRs is meaningless if the product is not getting better.

> ❌ **A trap to avoid:** looking only at end to end PR cycle time. If it stalls, you might wrongly conclude "AI is not helping," when really your build or CI system cannot keep up with the new pace. Always break the funnel into its steps.

Fiona is also honest that open questions remain, and that is healthy:

- Do you still need separate iOS and Android orgs, now that engineers can flex across mobile platforms with Claude?
- How far do you push fully automated reviews before you lose something important?
- As roles blur, how do you make sure everyone making a change has confidence it is correct?

---

## Key takeaways

1. **Bottlenecks move.** Coding is rarely the slow part now. Find the new bottleneck (often verification, review, or maintenance) instead of optimising the old one.
2. **Processes quietly stop working.** Each process solved a real problem once. Audit them, because they will not delete themselves.
3. **Build, do not just argue.** When a prototype is cheaper than a meeting, generate options and debate the real thing.
4. **Keep humans on taste, risk, and judgment.** Hand Claude the style, lint, obvious bugs, and spec drift. Keep humans on legal, risk tolerance, product sense, and trust boundaries.
5. **Code is the source of truth.** Keep specs and skills in the code base so they stay current. Out of loop docs rot fast.
6. **Roll out with alignment plus autonomy.** A few firm principles top down, lots of freedom bottom up.
7. **Measure outcomes, not just throughput.** Break funnels into steps, and always tie a metric to the actual problem you are solving.

## Common pitfalls

- ❌ Keeping a heavy planning or review process that existed only to protect now plentiful engineering time.
- ❌ Treating "more PRs" or "more commits" as success without measuring product quality.
- ❌ Reading only end to end cycle time, then blaming AI when the real jam is in CI.
- ❌ Letting documentation drift out of the update loop instead of putting the source of truth in the code base.
- ❌ Mandating every detail top down, leaving teams no room to adapt how Claude fits their workflow.
- ❌ Assuming a task Claude failed at months ago is still impossible; the models keep improving, so revisit.

---

## 🛠️ Capstone Project: The Process Audit and the Noisiest Workflow

> This is the main hands on project for the lesson, and it is exactly the exercise Fiona leaves the audience with: "Pick your noisiest workflow... and always ask yourself, is it still serving its purpose?" You will turn that idea into a small, measurable experiment on a real team (yours, a study group, or a simulated one), and back it with a tiny automation.

### What you will build

A short, evidence backed **Process Playbook** for one team, containing: (1) an audit of your current processes against the moved bottleneck, (2) a single rewritten norm, (3) a small working automation that "Claudifies" one slow step, and (4) before and after metrics that prove (or disprove) the change helped.

> 🎯 **Pick your noisiest workflow.** Choose the meeting or ritual that is highest tax and lowest joy. Fiona's example: a weekly status meeting where everyone sits on their laptops, only looking up to give status. Count the people in the room times their time, and you see how expensive it is. Good candidates: a standup, a manual triage rotation, a recurring migration chore, or a slow onboarding step.

### Why this is the perfect practice

| Lesson skill | Where you use it in the Capstone |
|---|---|
| Spotting the moved bottleneck | Milestone 1, the audit |
| "Is it still serving its purpose?" | Milestone 2, scoring each process |
| Rewriting a team norm | Milestone 3, the one rewrite |
| Claudify one step | Milestone 4, the small automation |
| Choosing honest signals | Milestone 5, before and after metrics |
| Align plus autonomy rollout | Milestone 6, the rollout plan |

### Milestones (build them in order, each one is shippable)

1. **Name the bottleneck.** Write one paragraph: where was the bottleneck on your team a year ago, and where is it now? Be specific (for example "review queue" or "CI build time").
2. **Audit the processes.** List 6 to 10 current processes, rituals, or SLAs. For each, write the original problem it solved and score it: still essential, partly stale, or safe to delete. This is your "quietly stopped working" hunt.
3. **Rewrite one norm.** Pick the most stale one and rewrite it for a world where coding is cheap. Example: replace "design doc before any work" with "prototype three options as PRs and review the real thing."
4. **Claudify one slow step.** Build a tiny automation for one painful step. Smallest version: a single Claude routine that, every morning, gathers feedback from your channels and clusters it into themes (Fiona runs exactly this over her morning coffee). Bigger version: a script that drafts a "team map" by reading recent commits, so new joiners onboard without pulling people away.
5. **Measure before and after.** Pick one honest signal tied to an outcome (onboarding time to first PR, time spent in the meeting, support tickets resolved). Record a baseline, run the change for a week or two, and record the new number. Break any cycle time into chunks so you can see which step moved.
6. **Write the rollout.** One page: the 2 to 3 non negotiable principles you align on top down, and the parts you explicitly leave to each pod. Include "explicit permission to kill old processes."

### How you will know you are done

- ✅ You can point to **one process you deleted or rewrote** and explain the original problem it no longer solves.
- ✅ Your automation runs on its own and saves a measurable amount of human time or attention.
- ✅ You have a **baseline and an after number** for one honest signal, tied to a real outcome (not just throughput).
- ✅ Your rollout page clearly separates "aligned top down" from "free bottom up."
- ✅ You wrote down at least one **open question** you still have, because honest leaders admit what they have not figured out.

> 💡 **Keep yourself honest:** change one process at a time and measure it. If your cycle time will not move, break the funnel into steps and find the jammed one before blaming the tool.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self contained reps, each focused on one skill from the lesson. They are optional and independent. The Capstone above already exercises all of them in one place, so feel free to skip straight to it.

### Exercise 1: the "is it still serving its purpose?" pass (foundational)
List every recurring meeting on your calendar this week. For each, write the problem it was created to solve and whether that problem still exists. Cancel or shrink one.

### Exercise 2: build versus argue (foundational)
Find a current technical disagreement on your team. Instead of scheduling a debate, ask Claude to generate two or three concrete versions of the change. Bring those to a 15 minute review. Note whether the decision came faster.

### Exercise 3: split the review (intermediate)
Take a recent batch of PRs. Sort each review comment into "Claude could have caught this" (style, lint, obvious bug, spec drift) versus "needed a human" (risk, legal, taste). What fraction could be automated, and what should humans focus on?

### Exercise 4: move the source of truth (intermediate)
Find one document your team relies on that tends to go stale. Convert its core into a spec or skill checked into the code base, and have Claude verify the code against it. Note how the maintenance burden changes.

### Exercise 5: instrument one funnel (advanced)
Pick PR cycle time (or onboarding time). Break it into its stages. Measure each stage for a week. Identify which single stage is the real bottleneck, and propose one change to that stage only.

---

## Cheat sheet

```text
WHEN THE BOTTLENECK MOVES
  1. Name the old bottleneck and the new one (often: verification, review, maintenance).
  2. Audit every process: what problem did it solve? Does that problem still exist?
  3. Rewrite or delete the stale ones. Processes don't delete themselves.

REWRITE THESE NORMS
  Planning ......... build/prototype options instead of long design docs
  Code review ...... Claude: style, lint, obvious bugs, spec drift
                     Humans: legal, risk, taste, trust boundaries
  Ownership ........ ask the REAL question behind "who touched this?"
  Source of truth .. put specs/skills IN the code base
  Org shape ........ flat; managers start as ICs

ROLL IT OUT
  Align top down on a few forcing functions (everyone uses Claude; Claudify;
    permission to kill old processes).
  Leave each pod free to adapt the details.

PROVE IT
  Watch onboarding time (down), PR cycle time (down, broken into chunks),
    Claude-assisted commits (up).
  But measure the actual OUTCOME, not just throughput.
```

## How this connects to the rest of the course

- **Earlier, Module 2 (Core skills):** the tools, skills, and verification habits this lesson reorganises a team around.
- **Earlier, Module 3 (Evals for taste):** the rigorous way to measure whether a change helped, which underpins Part 4's "measure the outcome."
- **Next, Module 8 · Lesson 28 (Designing with Claude):** how a tiny team ships fast by replacing planning docs with prototypes, the same "build, do not argue" idea applied to product.
- **Next, Module 8 · Lesson 30 (Coding is no longer the constraint, at Spotify):** the same bottleneck shift seen at 3,000 engineer scale, with concrete fleet automation.

---

*Source: "Running an AI-native engineering org" by Fiona Fung (Anthropic), Code with Claude 2026, London. The team principles and metrics tables are faithful paraphrases of what Fiona described; the short code-style snippets are illustrative reconstructions of routines she mentioned, not verbatim from the talk.*

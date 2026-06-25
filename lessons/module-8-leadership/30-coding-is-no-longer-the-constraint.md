# Module 8 · Lesson 30: Coding Is No Longer the Constraint, Scaling Devex at Spotify

> **Course:** Building with Claude, a self-paced course
> **Module 8:** Leading the AI-native transformation
> **Speaker:** Nicklaus, Spotify (developer experience / platform engineering)
> **Source talk:** [Coding is no longer the constraint: Scaling devex to teams and agents at Spotify](https://www.youtube.com/watch?v=zFslvuvYifQ) · [full transcript](../../transcripts/code-with-claude-2026-london-2026/21_coding-is-no-longer-the-constraint-scaling-devex-to-teams-and-agents-a.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

When an organisation of 3,000 engineers adopts AI coding tools faster than anything before, coding stops being the bottleneck, so the winning moves are automating routine maintenance across the whole code base, making your code base consistent so agents work better, verifying everything, measuring everything, and figuring out where human judgment now matters most.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you build a small "fleet maintenance" tool: an agent that applies one routine change across many code repositories, verifies each change, and reports results, the same shape as Spotify's system, at a size you can run yourself. Everything before the Capstone teaches the ideas behind it. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[Accelerate (Forsgren, Humble, Kim / DORA)](https://en.wikipedia.org/wiki/Accelerate_(book))** (book). The research-backed account of what makes software delivery fast and what to measure (lead time, deploy frequency, change-fail rate, MTTR), the foundation under "measure everything, automate maintenance."
> - **[The SPACE of Developer Productivity](https://www.microsoft.com/en-us/research/publication/the-space-of-developer-productivity-theres-more-to-it-than-you-think/)** (paper). The authoritative answer to "don't fixate on one throughput number": productivity is multidimensional.

## A few plain-language basics first

This is a platform engineering talk at large scale. Here are the terms in plain words:

- **Devex (developer experience):** how easy and pleasant it is for engineers to build, test, and ship. A devex team works to make that easier.
- **Deployment:** pushing a change live to real users. Spotify does around 4,500 deployments a day.
- **Monorepo vs polyrepo:** a *monorepo* is one giant code repository holding lots of code (Spotify's backend is a 40 million line monorepo). *Polyrepos* are many small separate repositories (Spotify has thousands).
- **PR (Pull Request):** a proposed code change that gets reviewed before being merged (accepted).
- **Migration:** updating code from an old version or pattern to a new one (for example, a new Java version, deprecating an old API, or fixing a security hole). Often dull, repetitive, and spread across many components.
- **CI (Continuous Integration):** the automated system that builds and tests every change.
- **Auto-merge:** accepting a PR automatically, with no human review, when automation has verified it is safe.
- **Agent SDK:** Anthropic's toolkit for building agents (AI that takes a series of actions toward a goal).
- **Harness:** the code and infrastructure around the model: the API call, the tools you give it, the loop that runs it. The prompt is what you say; the harness is everything around it.
- **MCP (Model Context Protocol):** an open standard that lets agents connect to your internal tools and data.
- **Lint / static analysis:** automated checks that read your code and flag problems or rule violations without running it.
- **Prototype:** a quick, rough working version of an idea you can try out before building the real thing.

You do not need to memorise these. Each one is explained again the first time it matters below.

## Why this lesson matters

Most teams are small. Spotify is not: close to 3,000 engineers, a 40 million line backend monorepo, thousands of smaller repositories, and 4,500 production deployments a day. When something works at that scale, the underlying principle is usually solid. Nicklaus shows what happens when coding stops being the constraint in a huge, mature organisation: the explosion of code that follows, the maintenance burden it creates, and the platform investments that turn that flood into an advantage instead of a crisis. The lessons (automate the dull maintenance, make your code base consistent for agents, verify and measure everything, and relocate human judgment) apply whether you have 3 engineers or 3,000.

> 🔑 **The headline:** "More than 99% of our engineers use AI coding tools every week," and "94% report that using AI tooling has helped them become more productive," at a record high self assessed productivity. PR frequency is up 76% and still climbing. The adoption curve for Claude Code, in particular, "completely exploded" around the Opus 4.5 release.

## Learning objectives

By the end of this lesson you will be able to:

1. Recognise the "explosion of code" that follows AI adoption, and why maintenance becomes the new burden.
2. Use an agent (not a brittle script) to apply a non trivial change across many repositories, with verification.
3. Explain why a consistent, standardised code base makes agents perform better, and how to drive that consistency.
4. Build the supporting practices agents need: strong tests, verification tools, and a catalog of your software exposed as tools (MCPs).
5. Decide where human judgment now matters most, especially in reviewing a flood of PRs.

## Prerequisites

- A basic understanding of how software gets built, tested, and shipped (PRs, CI, deployments). No coding required to follow the ideas.
- Helpful but optional: Module 8 · Lesson 27 (Running an AI-native engineering org), which frames the same "bottleneck has moved" idea.

---

## Part 1: the explosion of code, and a maintenance problem you must plan for

The AI transition at Spotify has been "a journey of very rapid adoption curves." They roll out internal tools all the time, but had "never seen the rate of adoption" they saw with AI coding tools. Claude Code in particular "completely exploded" around the Opus 4.5 release. The numbers: 99%+ weekly use, 94% reporting higher productivity, PR frequency up 76% (a number that "keeps growing all the time"), and most PRs now authored by an AI agent together with a developer.

More throughput means more code. And here is the crucial part: this was *not* a new problem caused by AI. Spotify saw it coming.

> 🔑 **The warning sign, from before AI:** a few years ago Spotify noticed their production code base "was growing seven times faster than the number of engineers." That meant engineers spent more and more time *maintaining* existing code rather than building new value. AI accelerates this, so you must plan for maintenance, not just creation.

A lot of maintenance is dull and necessary: migrate from one version to another, deprecate an API, fix a security vulnerability. The old way was to send a migration path to hundreds of teams ("upgrade from this Java version to that one"), and wait. One upgrade across thousands of components took months. In their engineering survey, "migrations was the top thing developers were frustrated about."

So they reframed the problem: instead of doing it component by component, could they "mutate our entire fleet of components" at once? They built infrastructure for this called **fleet management**, with an underlying system named **Fleet Shift**.

> 💡 **The result, pre-AI:** they have merged 2.5 million automated maintenance PRs, "work that our developers did not have to do." The vast majority were **auto-merged** (no human in the loop): automation creates the PR, automation validates it is safe, automation merges it. Thousands ship every day.

---

## Part 2: from brittle scripts to agents (the Honk story)

Fleet Shift worked great for *simple* changes: configuration tweaks, bumping a dependency version. But more complex changes (like replacing API calls) made the migration scripts "incredibly complicated."

Why? Because code has a very wide surface. There are many ways to call the same method, and when you run one script across millions of lines and thousands of components, "you are going to find every corner case." There is even a name for this: **Hiram's Law** (from a Google engineer), which observes that with enough users of an interface, every observable behavior of it will be depended on by somebody, so any change breaks someone.

So, early on, they asked: instead of writing brittle deterministic scripts, can we use an LLM (a Large Language Model, the kind of AI that reads and writes text) to do these code changes? Early attempts were hard: "the models were just too stupid, the way we were trying to do it was just too stupid." But over many iterations, as the patterns improved and the models got better, this became a tool called **Honk**.

How Honk works today:

```text
HONK (Spotify's fleet code-change agent)
  - Claude under the hood, via the Agent SDK.
  - Wrapped in Spotify's own harness, inside a Kubernetes pod
    (so many can run in parallel in the cloud).
  - Given access to a set of TRUSTED tools, including verification tools.
  - Verification = running real builds in CI, across multiple operating
    systems (Spotify's clients run on many OSes).
  - Orchestrated across thousands of repos by Fleet Shift.
```

Fleet Shift schedules and orchestrates the changes across thousands of repositories; Honk "sits in the middle doing the actual code changes." A team owning a migration can see its status: how many PRs created, how many merged, how many failed in CI and need a look.

> 🔑 **The payoff:** what used to take hundreds of teams weeks or months "now can be done by a single engineer in a few days." The latest Java migration across their JVM backend "took three days using these tools." (Spotify now offers this commercially through their Backstage developer portal.)

And developers being resourceful, they quickly found new uses. Someone figured out how to call Honk over Slack. Now it is common to have a Slack conversation, then "@mention Honk," and Honk goes off, works, and comes back with a PR. They have since shipped **Honk V2** (during a Hack Week), which makes it more interactive: integrated with their agent orchestration tool **Chirp** (which runs many agent sessions at once, similar to Claude agents), with shared sessions where multiple developers collaborate on the same agent session "like Google Docs, but for Claude," grouped into larger projects.

> 💡 Nicklaus is personally most excited about the **multiplayer** features: imagining how agents actually collaborate with multiple developers and teams, not just one person in front of one terminal.

---

## Part 3: make your code base agent friendly

The second half of the talk is about optimising the *code base itself* so agents are as effective as possible. The core belief at Spotify, held for more than 15 years and predating AI: **the fewer technologies you use, the faster you go.**

Why standardisation helps (and now helps agents too):

| Benefit of fewer technologies | For humans | For agents |
|---|---|---|
| Deep expertise | You build better things on a stack you know deeply. | Claude has lots of similar code to learn from. |
| Fewer decisions | Teams do not pick a technology for everything; a ready set is available. | Less ambiguity about how to do something. |
| Easier collaboration | Other teams' components look like yours, so you can contribute. | Consistent patterns are easier to extend correctly. |
| Easier moves | Components and people move between teams smoothly. | Agents generalise across a uniform code base. |

> 🔑 **The agent-specific finding (paraphrased from Nicklaus):** "If Claude has a lot of other code to look at, and that code looks roughly consistent, Claude will do a better job." They can *see* Claude perform *worse* in their more fragmented code bases. Consistency is not just tidy; it measurably improves agent output.

They are deliberate, not rigid: they still want some variance to experiment with and evaluate new technologies, but "we don't want to do that willy-nilly. We want to be intentional about it."

### The platform that drives consistency: Backstage

**Backstage** is Spotify's developer portal (a single place for developers to do everything). Before it, developers used roughly 100 different tools (one for deployments, one for CI, one for A/B tests), and "all of those tools were kind of shit." Backstage started as a **catalog** of all their software, just to answer "who owns this component?" so they could page the right team during an incident. It grew into a hub with tools around every component.

> ✅ **Best practice: expose your platform to agents as tools.** Everything a human does in Backstage, they expose as MCPs (the open standard for connecting agents to tools) or command line tools. So Claude can look up who owns something, and even ping that team on Slack to ask a question. The catalog you built for humans becomes equally useful for agents.

How they drive standardisation through Backstage:

- A **technology radar**: a list of all technologies and their status (recommended, not recommended, and so on), as many companies have.
- **Golden state**: for a given type of component (a kind of backend service, a kind of iOS view), the specific technologies and practices they recommend you use.
- **Soundcheck**: a UI where a team can self assess against those requirements (for example, "define a valid owner").

They combine this with **static analysis and linting** (automated checks built into the code bases). So when Claude works in their code, it gets immediate feedback. If Claude calls gRPC (a way services talk to each other) in a way Spotify knows is not optimal, "Claude will get feedback from our Lint system to correct that." Nicklaus sees this constantly: "Claude run into these Lint checks all the time and correct itself." It is a powerful, automatic way to drive standardisation for both developers and agents.

---

## Part 4: verify, measure, and relocate human judgment

Nicklaus sums up with four points. The throughline is that strong engineering practices matter *more* now, not less.

### Verification has not gone away

> 🔑 **Quote (paraphrased):** the need for strong engineering practices "has not gone away with agents. It remains as important as it was before." Having well tested code, and agents that can *invoke* those tests (Claude locally, or Honk with its verification tools), "is the way to make your agents be much more autonomous and come up with better solutions."

This is exactly why Honk runs real builds in CI across multiple operating systems before a change is trusted. Verification is what lets automation safely auto merge.

### Measure everything

Spotify instruments all their infrastructure and all their PRs, collecting "tons and tons of metrics." The numbers in this talk come from that instrumentation. You cannot manage a transition you cannot see.

### Relocate human judgment

> 🔑 **The flip side of speed:** "human judgment matters just as much as it did before, or even more." But you must figure out *where* to apply it. The 76% increase in PR frequency means "76% more PRs to review," and "there's just too many PRs to review" is one of their most frequent complaints.

So they are already auto approving PRs they judge safe enough, and focusing human review where it matters most. Where exactly the line sits will keep shifting, "both prior to invoking the agent and post invoking the agent."

### Coding is less of a bottleneck, so the constraints move

As coding loosens up, the bottleneck moves to **human decision making**: deciding what to ship, which ideas to explore. Two examples:

- **Prototyping** used to be expensive (you had to convince developers to build something). Now anyone, including a CEO, can open Claude in the client monorepo and, through a set of skills and some infrastructure, "prompt Claude to build out any feature." You get back an installable app to test on your device and share internally. Prototyping went "from something that could take days or weeks to literally taking minutes."
- **Building for production** is faster too. But the constraint moves to the human decisions: which of Spotify's "too many ideas" to validate and ship.

> 💡 Nicklaus is honest that this is "very much an ongoing learning," with experiments running. His prediction: in roughly six months, Spotify will have "a very, very different way of building products" as they figure out how to make those decisions better and faster.

---

## Key takeaways

1. **Plan for the maintenance flood.** AI multiplies code, and code grows faster than headcount. Automate the dull maintenance (migrations, deprecations, security fixes) across your whole fleet.
2. **Agents beat brittle scripts for non trivial changes.** Code has a huge surface (Hiram's Law). An agent with verification tools handles corner cases that scripts cannot.
3. **Consistency makes agents better.** A standardised code base measurably improves agent output. Drive it intentionally with a radar, golden state, self assessment, and lint.
4. **Expose your platform to agents.** Turn your developer portal and catalog into MCPs and CLI tools so agents can look up owners, run builds, and ask teams questions.
5. **Verify and measure everything.** Tests an agent can invoke are what make it autonomous. Instrument your infrastructure and PRs so you can see the transition.
6. **Relocate human judgment.** Auto approve the safe PRs, focus humans on the risky ones, and accept that the bottleneck has moved to human decisions about what to build.

## Common pitfalls

- ❌ Assuming AI removes the maintenance burden; it accelerates it, so plan for it.
- ❌ Writing ever more complicated deterministic scripts to handle every corner case, instead of using a verifying agent.
- ❌ Letting your code base stay fragmented, then wondering why the agent performs worse there.
- ❌ Building great human tools but never exposing them to agents as MCPs or CLI tools.
- ❌ Trusting agent output without tests the agent can run to verify itself.
- ❌ Trying to keep human reviewing every PR when volume is up 76%, instead of focusing humans where risk is highest.

---

## 🛠️ Capstone Project: Mini Fleet Shift

> This is the main hands on project for the lesson. You will build a small version of Spotify's fleet maintenance system: an agent that applies one routine change across several code repositories, verifies each change by running tests, and reports results. It is the same shape as Honk plus Fleet Shift, sized so you can run it yourself.

### What you will build

A small command line tool (or script) that takes one routine code change, applies it across 3 to 10 repositories (real ones you own, or copies you create), verifies each by running the build and tests, opens a PR (or a local branch) for each, and prints a status report: created, verified, failed.

> 🎯 **Pick a boring, repetitive change.** The best fleet changes are dull: bump a dependency version, rename a deprecated function call, add a missing config field, or fix one lint rule everywhere. Choose one that is annoying to do by hand across many repos.

### Why this is the perfect practice

| Lesson skill | Where you use it in Mini Fleet Shift |
|---|---|
| Automate fleet maintenance | The whole project |
| Agent beats brittle script | Milestone 3, the agent handles corner cases |
| Verify everything | Milestone 4, run real builds and tests |
| Auto-merge the safe ones | Milestone 5, the safety gate |
| Measure everything | Milestone 6, the status report and metrics |
| Consistency helps agents | Stretch goal, add a lint check |

### Milestones (build them in order, each one is shippable)

1. **Pick the change and the repos.** Choose one routine change and 3 to 10 repositories. Write one sentence describing exactly what "done correctly" looks like for each repo.
2. **Try the brittle script first.** Write a simple find and replace script to make the change. Run it on all repos. Note where it breaks or misses corner cases. This is your "why scripts are not enough" evidence (Hiram's Law in miniature).
3. **Replace the script with an agent.** Use the Agent SDK to give Claude the change instruction and the tools to edit files. Let it handle each repo, including the corner cases the script missed.
4. **Add verification.** For each repo, have the agent run the build and tests after its change. Only changes that pass verification count as successful.
5. **Add a safety gate (auto-merge logic).** Decide a rule for which changes are safe enough to auto merge (for example, all tests pass and the diff matches an expected shape) versus which need human review. Implement the gate.
6. **Report and measure.** Print a status table: per repo, was the change created, verified, auto merged, or flagged for review? Record how long the whole run took versus your estimate of doing it by hand.

### How you will know you are done

- ✅ The agent applied the change across **all your repos**, including at least one corner case the brittle script missed.
- ✅ Every successful change was **verified** by a real build and test run.
- ✅ Your **safety gate** correctly separates auto merge from "needs a human."
- ✅ Your **status report** shows created / verified / merged / flagged per repo.
- ✅ You can state the **time saved** versus doing it by hand, the way Nicklaus cited "three days" for a Java migration.

> 💡 **Keep yourself honest:** if the agent ever merges something the tests did not verify, your safety gate is broken. Verification is what makes auto merge safe; do not skip it.

---

## Practice exercises (optional extra reps)

> **What these are:** small, independent reps, each focused on one move from the talk. Optional. The Capstone above exercises all of them together.

### Exercise 1: find the maintenance burden (foundational)
List the dull, repetitive maintenance tasks your team does across many components (version bumps, deprecations, security fixes). Which one is the most frustrating, and how often does it recur?

### Exercise 2: the wide surface (foundational)
Take one simple "replace this call with that call" change. Write the naive script, run it across a few files, and list every corner case it gets wrong. This is Hiram's Law in action.

### Exercise 3: agent with verification (intermediate)
Give Claude one code change to make in a repo, plus the command to run the tests. Require it to run the tests and only report success if they pass. Confirm it self corrects when a test fails.

### Exercise 4: expose a tool (intermediate)
Pick one internal lookup your team does by hand (who owns this component, what is its deploy status). Wrap it as a small CLI tool or MCP so an agent could call it. Have Claude use it.

### Exercise 5: relocate review (advanced)
Take a batch of recent PRs. Define a rule for which are "safe enough" to auto approve and which need a human. Apply it. What fraction could be auto approved, and where would you focus human review?

---

## Cheat sheet

```text
WHEN CODING STOPS BEING THE CONSTRAINT (at scale)
  Code grows faster than headcount. Maintenance becomes the burden.
  Plan for it: automate dull maintenance across the whole fleet.

FLEET MAINTENANCE
  Simple changes (config, version bumps): deterministic scripts + auto-merge.
  Complex changes (API calls): an AGENT with verification tools.
    Why: code has a huge surface (Hiram's Law); scripts hit every corner case.

MAKE THE CODE BASE AGENT-FRIENDLY
  Fewer technologies = faster humans AND better agents.
  Drive consistency: tech radar, golden state, self-assessment, lint.
  Fragmented code bases -> Claude performs worse there.

GIVE AGENTS WHAT HUMANS HAVE
  Expose your portal/catalog as MCPs and CLI tools.
  Agents can look up owners, run builds, ping teams.

VERIFY, MEASURE, RELOCATE JUDGMENT
  Tests the agent can run = autonomy. Verification enables auto-merge.
  Instrument infra and PRs; measure everything.
  Auto-approve safe PRs; focus humans where risk is highest.
  The bottleneck moved to human decisions about WHAT to build.
```

## How this connects to the rest of the course

- **Earlier, Module 8 · Lesson 27 (Running an AI-native engineering org):** the same "bottleneck has moved" idea, here at 3,000 engineer scale with concrete fleet automation.
- **Earlier, Module 2 (Core skills) and skills:** the prompting, tools, and skills that power agents like Honk and the in monorepo prototyping flow.
- **Next, Module 8 · Lesson 31 (Building AI-native at enterprise scale):** other large companies (monday.com, Doctolib, Delivery Hero) tackling the same code base consistency and verification problems.
- **Earlier, Module 3 (Evals):** the measurement discipline behind "measure everything" and verifying agent output.

---

*Source: "Coding is no longer the constraint: Scaling devex to teams and agents at Spotify" by Nicklaus (Spotify), Code with Claude 2026, London. The Honk and cheat-sheet boxes are faithful paraphrases of what Nicklaus described; they are illustrative reconstructions, not verbatim slides.*

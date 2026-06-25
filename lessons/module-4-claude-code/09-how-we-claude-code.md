# Module 4 · Lesson 9: How We Claude Code

> **Course:** Building with Claude, a self-paced course
> **Module 4:** Claude Code, your everyday agent
> **Speaker:** Arno, Architect, Applied AI team, Anthropic
> **Source talk:** [How we Claude Code](https://www.youtube.com/watch?v=IlqJqcl8ONE) · [full transcript](../../transcripts/code-with-claude-2026-london-2026-day-2/06_how-we-claude-code.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

As models get more capable, you get more out of them by constraining them less: let Claude interview you to pull out what you really want, review the plan in a rich HTML mockup instead of a long markdown file, and build verification directly into the thing you are making so the agent can check its own work.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you take a small app from a vague idea to a fully self-verifying artifact, using the exact three-phase workflow the talk demonstrates. Everything before the Capstone teaches one phase. To see the finish line first, jump to **"Capstone Project: the Self-Verifying App"**, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[Best practices for Claude Code (Anthropic docs)](https://code.claude.com/docs/en/best-practices)** (docs). The official codification of the exact workflow the lesson teaches: explore, plan, implement, commit, "let Claude interview you," and give the agent a verification loop it can run itself.
> - **[The Bitter Lesson (Rich Sutton)](https://en.wikipedia.org/wiki/Bitter_lesson)** (essay). The intellectual root of the lesson's "constrain capable models less" thesis.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Claude Code:** Anthropic's coding agent. You give it a task in plain English and it reads, writes, and runs code for you.
- **Agent:** an AI that takes a series of actions on its own toward a goal. The longer it runs, the more it can do, but also the more it can burn tokens if it goes the wrong way.
- **Token:** the unit the model reads and writes in. You are billed per token, so wasted work costs money.
- **Spec (specification):** a written description of what you want built (the requirements, the look, the rules).
- **Markdown:** a simple text format with `#` headings and `-` bullets. Long markdown specs are common but get tedious to read.
- **HTML:** the language web pages are written in. An HTML mockup is something you can actually open in a browser and click.
- **DOM (Document Object Model):** the live structure of a web page in the browser. Code can read and change it. We will use it to expose an app's state so an agent can check it.
- **React:** a popular library for building web app interfaces out of reusable "components."
- **Playwright MCP:** a tool that lets Claude drive a real browser (click, type, read the page). "MCP" is the standard way Claude connects to external tools.
- **CI (Continuous Integration):** an automated system that runs your tests every time you push code.

You do not need to memorise these. Each is explained again the first time it appears below.

## Why this lesson matters

This is not a feature tour. It is how the Applied AI team and the Claude Code team actually work day to day, and it is built on one observation: agents are getting more capable because models are getting more capable. That means agents can run longer on harder tasks. But a long-running agent that starts off in the wrong direction can burn through a lot of tokens before you notice.

So the whole workflow is about **front-loading correctness**: getting the requirements right before the agent runs, making the plan easy to sanity-check, and wiring verification into the artifact so the agent can confirm it built the right thing. The material is based on a talk by Tariq (and his blog post, "The Unreasonable Effectiveness of HTML files") and reflects current practice on the Claude Code team.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain the **bitter lesson** and why you should constrain capable models *less*, not more.
2. Write a good prompt that makes Claude **interview you** to extract requirements, instead of forcing you to specify everything up front.
3. Review a plan as a **rich HTML mockup** rather than a long markdown file, and give feedback with screenshots.
4. Build **agent-native verification** into an app by publishing its state to the DOM, so an agent can verify it across three surfaces: human dashboard, agent-from-browser, and headless CI.
5. Use **fast mode**, **auto mode**, and the **effort** parameter, with sensible defaults.

## Prerequisites

- Module 4 · Lesson 8 (What's new in Claude Code), which introduces auto mode and the broader tooling.
- Comfort running a basic Claude Code session and a basic web app locally.

---

## Part 1: the mindset (constrain less)

The talk opens with a principle from Richard Sutton, the "father of reinforcement learning" (a way of training AI by rewarding good outcomes). His famous idea is the **bitter lesson**: you can spend enormous effort hand-coding human knowledge and constraints into a system, but in the end, pouring in more data and more compute beats anything you could hand-craft.

Arno draws the analogy straight to how you work with Claude:

> 🔑 **The model is probably better at extracting your requirements than you are at defining them.** Your requirements are *latent* (present inside you but not yet articulated). Just like your users, "you know it when you see it" but struggle to say it up front. As models improve, the smart move is to let Claude interview you, not to over-specify.

The three levels the talk covers map onto three phases of work:

| Phase | Goal | Old way | New way |
|---|---|---|---|
| 1. Prompt | Remove ambiguity | You write the full spec | Claude interviews you |
| 2. Plan | Check it is what you want | Long markdown file | Rich HTML mockup |
| 3. Verify | Confirm it works | Manual checking | Verification built into the artifact |

---

## Part 2: phase 1, let Claude interview you

### Good vs bad prompting

The worst prompt, which Arno sees constantly, is "just make it better." It gives Claude nothing to work with.

> ❌ **Bad prompt:** "Make it better." (No direction, no domains, nothing to extract.)

A good prompt does two things differently:

- It **names the domains you care about** (audience, edge cases, look and feel) without dictating the exact outcome.
- It **invites open-ended answers** rather than predefining them, which prompts Claude to interview you turn by turn.

> ✅ **Good prompt shape:** "I want to build a bill-splitting app. Interview me to extract the requirements. Ask about the audience, the edge cases, and the design direction. Use the ask-user-question tool, one area at a time."

### The ask-user-question tool

The thing that actually triggers the interview is referring to the **ask-user-question tool** in your prompt. This is a built-in tool that lets Claude ask you a question and present tappable answer options. When your prompt explicitly mentions it, Claude runs the interview workflow: it asks who the app is for ("just for friends? a secondary audience?"), tabs through your answers, and only then writes the spec.

```text
# A prompt that triggers the interview (illustrative)
I want to build a bill-splitting app so friends can see who owes what.
Don't over-specify the outcome. Instead, use the ask-user-question tool
to interview me about: the audience, the key scenarios, and the look/feel.
Ask one area at a time, then write the spec.
```

> 🔑 **Why this beats writing the spec yourself.** The longer you let an agent run, the more important it is that the spec is complete, and the less likely you are to have thought of everything up front. Iterating turn-by-turn with Claude produces a more comprehensive spec than a blank-page brain dump.

### A few session settings to know

Three settings the talk recommends turning on:

- **Auto mode** (toggle with shift-tab to cycle modes): lets Claude proceed without stopping for trivial permissions. "If you're not using auto mode, you need to be using auto mode."
- **Effort** (`/effort`): how hard the model thinks. The recommendation is **X-high**; you can also set **max**.
- **Fast mode** (`/fast`): iterates more quickly. It costs more, but it is great for rapid iteration on specs and designs.

```text
/effort x-high      # recommended default thinking effort
/fast               # quicker iteration, costs more, great for specs
# shift-tab to cycle into auto mode
```

---

## Part 3: phase 2, review the plan as HTML

Once the interview produces a spec, Claude turns it into a plan. The old habit was to read that plan as a markdown file. A colleague of Arno's called the markdown file "the lingua franca of the AI-native software development life cycle" (the common language everyone uses). Poetic, but markdown has a real limit.

> 🔑 **The 200-line problem.** Once a markdown spec runs past about 200 lines, you are unlikely to read it, and your colleagues are almost certainly not going to. A plan nobody reads cannot be checked.

The fix is to have Claude generate the plan (or design directions) as **HTML**, which you open in a browser. HTML is far more **information dense** and **ergonomic**: you see what the thing will actually look like instead of imagining it from prose.

A concrete move from the talk: ask Claude for several design directions at once.

```text
# Generate explorable design directions (illustrative)
Give me four different design directions for the bill-splitting app.
Explore them, generate each as a standalone HTML file, and let me click
through and compare them side by side.
```

Claude (using Opus 4.7) produced distinct aesthetics, for example one "brutalist" and one "Tokyo fintech," each a clickable HTML page. Clicking through real mockups is "much better for me to give feedback to Claude on than to infer from a markdown file."

> ✅ **Take screenshots and feed them back.** Especially for front-end work, it is hard to put a visual problem into words ("there's a misalignment here, it's slightly off"). A screenshot says it instantly. Opus 4.7's stronger vision model can look at your screenshot and extract the problem proactively. You can also connect the **Playwright MCP** (a tool that lets Claude drive a real browser) so Claude interacts with the mockup itself.

> 💡 **Isn't an HTML spec wasteful on tokens?** A common worry, and the answer is usually no. Yes, generating rich HTML costs more tokens in that one moment. But a good, rich HTML spec means you **iterate less** over the whole project, which saves tokens in the long run. You can even use fast mode for it.

---

## Part 4: phase 3, build verification into the artifact

This is the deepest and most important part. The goal: make verification **native to the thing itself**, so the agent can drive it, and eventually run it headlessly with no human at all.

### The example: a tiny to-do app

The demo uses a small React to-do app. You can add an item, tick it off, drop it, and clear finished items. Lots of **state** (the app's current data: which items exist, which are done) is changing, and we want to verify it all works, in a way an **agent** can drive.

### The key trick: publish state to the DOM

Normally, to check a web app's state, an agent would have to **scrape the DOM** (dig through the page's HTML structure and guess). That is fragile. Instead, each component **publishes its own state to the DOM** through data attributes:

```html
<!-- The component publishes its state where an agent can simply read it -->
<div data-verify="unit"
     data-total="3"
     data-done="1"
     data-active="2">
  ... the actual to-do list ...
</div>
```

Now when the state changes (you add or drop an item), these attributes update. The agent does not interpret the React internals; it reads a clean, declared **data contract** straight from the DOM.

> 🔑 **Separate the contract from the implementation.** Because state is published independently of React's internals, you can verify the app no matter what its internal state is. You are checking against a stated contract, not reverse-engineering the code.

### What each component carries

Every component is set up with a small verification kit:

- **Schemas:** the shape its data should have.
- **Fixtures:** sample data and **known states** to test against (from a testing library, here Storybook).
- **Invariants:** rules that must *always* hold (for example, total = done + active).
- **Probes:** checks that deliberately push off the "happy path" to test edge cases.

> 💡 **Include probes that push off the happy path.** It is not enough to test that things work when everything goes right. Probes deliberately test the awkward cases. And much of this scaffolding "will be generated by Claude for Claude," so it scales.

### The same verification, three surfaces

The cleverest part: the *same* verification logic runs on three different surfaces, so you can choose how hands-on to be.

```text
1. HUMAN-READABLE DASHBOARD  -> you click "run all", a person reads the results.
2. AGENT-FROM-BROWSER        -> Claude reads the verification manifest from the
                                DOM and runs the same checks itself (via Playwright MCP).
3. HEADLESS (CI)             -> `bun verify` runs the test matrix with no UI at all.
```

In the demo, one check is deliberately rigged to fail (the sums do not match: "3 + 4 does not equal 10"). All three surfaces catch the same failure:

- The **human dashboard** shows pass/pass/pass/fail when you run all checks.
- **Claude, driven from the browser** with Opus 4.7 and Playwright MCP, finds and diagnoses it: "schema got rejected, 4 + 3 does not equal 10."
- Running **`bun verify`** headlessly runs the underlying test matrix.

> 🔑 **Breaking the contract vs breaking the app.** The talk shows deleting a published attribute (`total`): the *app still works*, but the *contract* is now broken, so the verification fails. That is the point. The contract is what the agent verifies against, independently of whether the app happens to look fine.

### Record the verification as evidence

A final step the Claude Code team uses: don't just *run* the verification, **record it**. Each check can be captured as a video clip, bundled, and stored (on S3, or shared with colleagues). The clips become evidence that the verification passed.

> 💡 **Why record?** At the team's shipping pace, recorded verification clips are a regular cadence. They let humans have fewer and fewer touchpoints with the work while still trusting it. The agent generates the verification, runs it, and records the proof.

### What is actually new here

Arno is clear that the individual pieces (React components, Storybook fixtures, Playwright, data attributes) are things you already know. What is new is the **remixing**: arranging these familiar primitives so the work is **agent-first**, readable and runnable by an agent, not just a human.

> 🔑 **The objective, stated plainly:** "embed the verification into the artifact itself." When the thing you build carries its own checks, the agent can verify, re-verify, and record without you in the loop.

### A model note

For this workflow, the recommendation is **Opus 4.7**, specifically because of its stronger vision model, which makes the HTML mockup and screenshot feedback steps shine. Sonnet is not recommended here. Fast mode is great for iterating on specs.

---

## Key takeaways

1. **Constrain capable models less.** The bitter lesson: extracting requirements from you beats you specifying everything up front.
2. **Let Claude interview you** by naming the domains you care about and referring to the ask-user-question tool.
3. **"Make it better" is a non-prompt.** Give domains and open-ended directions instead.
4. **Review plans as HTML, not long markdown.** Past ~200 lines, nobody reads markdown. HTML mockups are dense, clickable, and screenshot-friendly.
5. **Feed screenshots back** for visual feedback; Opus 4.7's vision model extracts the problem for you.
6. **Publish state to the DOM** so an agent reads a clean contract instead of scraping internals.
7. **Build verification into the artifact** so the same checks run as a human dashboard, agent-from-browser, and headless CI.
8. **Verify the contract, not just the app**, and record the verification as evidence.
9. **Use Opus 4.7, X-high effort, auto mode, and fast mode** for this kind of work.

## Common pitfalls

- ❌ Typing "make it better" instead of naming the domains and letting Claude interview you.
- ❌ Trying to write the entire spec up front before the agent has interviewed you.
- ❌ Reviewing a 400-line markdown plan you (and your team) will never actually read.
- ❌ Describing a visual bug in words when a screenshot would say it instantly.
- ❌ Making the agent scrape the DOM instead of publishing a clean state contract.
- ❌ Testing only the happy path with no probes.
- ❌ Worrying about HTML token cost while ignoring that it cuts total iterations.
- ❌ Using Sonnet for the vision-heavy steps where Opus 4.7 is recommended.

---

## 🛠️ Capstone Project: the Self-Verifying App

> This is the main hands on project for the lesson. You will take a small app from a vague idea all the way to a self-verifying artifact, using the talk's three phases. There is a companion repo (under the Code with Claude workshops, "How we Claude Code") with a worked verification setup you can study; this Capstone has you build your own.

### What you will build

A small web app (the talk uses a **bill-splitting app** for phases 1 and 2 and a **to-do app** for phase 3; you can use one app for all three) that you:

1. **Spec by interview** (Claude interviews you),
2. **Design in HTML** (clickable mockups you choose between), and
3. **Wrap in agent-native verification** that runs three ways.

> 🎯 **Pick your app.** Anything with visible state and a few rules: a bill splitter, a to-do list, a habit tracker, a tip calculator. You need at least one **invariant** (a rule that must always hold) to make verification interesting.

### Why this is the perfect practice

| Lesson skill | Where you use it in the build |
|---|---|
| Constrain less / interview | Milestone 1, the ask-user-question prompt |
| Good prompting | Milestone 1, naming domains not outcomes |
| HTML mockups | Milestone 2, four design directions |
| Screenshot feedback | Milestone 2, give visual feedback |
| Publish state to the DOM | Milestone 3, the data contract |
| Schemas, fixtures, invariants, probes | Milestone 4 |
| Three verification surfaces | Milestone 5 |
| Record verification as evidence | Milestone 6 |

### Milestones (build them in order, each one works on its own)

1. **Spec by interview.** Write a prompt that names the domains you care about (audience, key scenarios, look and feel) and explicitly tells Claude to use the ask-user-question tool, one area at a time. Run the interview, answer turn by turn, and let Claude write the spec. Compare it against a spec you would have written cold; note what the interview surfaced that you would have missed.
2. **Design directions in HTML.** Ask Claude for **four** different design directions, each as a standalone HTML file. Open them in a browser, click through, and pick one. Give feedback by **taking a screenshot** of something you want changed and feeding it back. Use fast mode and Opus 4.7.
3. **Publish state to the DOM.** Build (or have Claude build) the app so each component **publishes its state** via data attributes (`data-verify`, `data-total`, `data-done`, `data-active`, etc.). Confirm in the browser's element inspector that the attributes update as you use the app.
4. **Add the verification kit.** For each component, define **schemas** (data shape), **fixtures** and known states, **invariants** (rules that always hold, e.g. total = done + active), and **probes** that push off the happy path. Have Claude generate as much of this as possible.
5. **Run verification three ways.** Wire up (a) a **human dashboard** with a "run all" button, (b) an **agent-from-browser** path where Claude reads the verification manifest from the DOM and runs it (connect the Playwright MCP), and (c) a **headless** `verify` command for CI. Confirm all three agree.
6. **Plant a failure, then catch it.** Deliberately break a check two ways: once by breaking the **app logic** (make the sums wrong) and once by breaking the **contract** (delete a published attribute while the app still works). Confirm all three surfaces catch each. Then ask Claude to diagnose the failure for you.
7. **Record the evidence (stretch).** Capture each verification run as a clip, bundle them, and store/share them. Then try running the whole verification headlessly with no human in the loop.

### How you will know you are done

- ✅ Claude **interviewed you** and wrote a spec richer than your cold draft.
- ✅ You chose a design from **clickable HTML mockups** and gave at least one **screenshot** of feedback.
- ✅ Your app **publishes its state to the DOM** as a clean contract.
- ✅ The **same verification** passes as a human dashboard, agent-from-browser, and headless command.
- ✅ A planted failure is caught on **all three surfaces**, including one that breaks the **contract but not the app**.
- ✅ (Stretch) You produced a **recorded bundle** proving the verification ran.

> 💡 **The real lesson:** the more the verification lives inside the artifact, the fewer touchpoints you need. You are building something the agent can check for you.

---

## Practice exercises (optional extra reps)

> **What these are:** five small, self-contained tasks, each focused on one phase. Optional and independent. The **Capstone above is the main build** and already covers all of them.

### Exercise 1: rewrite a bad prompt (foundational)
Take "make it better" and rewrite it into a prompt that names domains, invites open-ended answers, and refers to the ask-user-question tool. Run both and compare what Claude does.

### Exercise 2: four directions (foundational)
For any small UI, ask Claude for four HTML design directions. Click through them and pick one. Write one sentence on why HTML beat imagining it from text.

### Exercise 3: screenshot feedback (intermediate)
Build a simple page, screenshot one visual flaw, and feed the screenshot back to Claude (use Opus 4.7). Confirm it identifies the problem from the image alone.

### Exercise 4: publish state to the DOM (intermediate)
Take any small interactive component and add data attributes that publish its state. Open the element inspector and confirm they update as you interact. Then have Claude read them instead of scraping the DOM.

### Exercise 5: three-surface verification (advanced)
Define one invariant for a component, then run it three ways: a human dashboard button, Claude from the browser via Playwright MCP, and a headless command. Plant a failure that breaks the contract but not the app, and confirm all three catch it.

---

## Cheat sheet

```text
THE MINDSET
  Bitter lesson: constrain capable models LESS. Let Claude extract requirements.

PHASE 1 - PROMPT (interview)
  Bad:  "make it better"
  Good: name the DOMAINS (audience, edge cases, look) + refer to the
        ask-user-question tool, one area at a time -> Claude interviews you
  Settings: /effort x-high  ·  /fast (great for specs)  ·  auto mode (shift-tab)

PHASE 2 - PLAN (HTML, not long markdown)
  Markdown > ~200 lines = nobody reads it.
  Ask for 4 HTML design directions, click through, pick one.
  Give feedback with SCREENSHOTS (Opus 4.7 vision extracts the problem).
  HTML costs more tokens once, but you iterate LESS overall.

PHASE 3 - VERIFY (build it into the artifact)
  Publish state to the DOM (data-verify attrs) = a contract, not DOM scraping.
  Each component: schemas + fixtures/known states + invariants + probes.
  Run the SAME checks three ways:
    human dashboard  ·  agent-from-browser (Playwright MCP)  ·  headless (verify)
  Verify the CONTRACT, not just the app. Record clips as evidence.

MODEL: Opus 4.7 (better vision). Not Sonnet for this.
```

## How this connects to the rest of the course

- **Earlier, Module 2 (The prompting playbook):** "good vs bad prompting" here is the same discipline, applied to extracting requirements.
- **Earlier, Module 3 (Evals for taste):** the QA-loop and "let the agent verify itself" ideas grow into the self-verifying artifact in this lesson.
- **Earlier, Module 4 · Lesson 8 (What's new in Claude Code):** auto mode, fast mode, and effort are introduced there and used heavily here.
- **Later, Module 5 (Managed agents):** headless, recorded verification is the foundation for fully asynchronous agents that ship with little human touch.

---

*Source: "How we Claude Code" by Arno (Anthropic Applied AI team), Code with Claude 2026, London, based on Tariq's talk and his post "The Unreasonable Effectiveness of HTML files." Code snippets are illustrative reconstructions of the patterns shown in the talk; see the companion workshop repo for a complete worked setup.*

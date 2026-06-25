# Module 8 · Lesson 28: Designing with Claude, From Prompt to Production

> **Course:** Building with Claude, a self-paced course
> **Module 8:** Leading the AI-native transformation
> **Speaker:** Dan Carey, Product Manager leading product at Anthropic Labs
> **Source talk:** [Designing with Claude: From prompt to production](https://www.youtube.com/watch?v=Uvl-tRga98g) · [full transcript](../../transcripts/code-with-claude-2026-london-2026/07_designing-with-claude-from-prompt-to-production.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

A tiny team built and launched a real product (Claude Design) in about ten weeks by replacing planning documents with working prototypes, keeping the team small enough that everyone does everything, and obsessively optimising every step of a tight "talk, design, ship, learn" loop they ran 50 to 100 times.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you run your own fast product loop on a small idea: you replace a planning doc with a prototype, build one tool to scratch your own itch, and turn one real user request around in 24 hours. Everything before the Capstone teaches the moves you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section near the end, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[Design thinking](https://en.wikipedia.org/wiki/Design_thinking)** (essay). The lesson's prototype, test, learn, iterate loop is textbook design thinking, the durable discipline behind "prototypes beat PRDs."
> - **[Lean startup](https://en.wikipedia.org/wiki/Lean_startup)** (essay). Build-Measure-Learn and the MVP are the first-principles version of the daily ship-and-learn loop.

## A few plain-language basics first

This is a product and team talk. Here are the everyday terms it uses, in plain words:

- **Prototype:** a quick, rough working version of a feature you can actually click and feel, as opposed to a description of it on paper.
- **PRD (Product Requirements Document):** a written document that describes what a product or feature should do, usually written before any building starts. Dan's whole argument is that prototypes often beat PRDs.
- **Lean startup:** a way of building products by shipping small, watching how people use it, and learning fast, instead of planning everything up front.
- **Bet:** in Anthropic Labs, a small exploratory project that might or might not work. Most bets are "folded" (stopped) early; a few become real products.
- **Ship:** to release something to real users.
- **Dogfooding:** using your own product yourself, every day, the way a customer would.
- **Power user:** a customer with advanced, demanding needs who wants fine grained control. Vocal power users can mislead you about what most users want.
- **MCP (Model Context Protocol):** an open standard that lets different tools and products plug into each other, so (for example) an outside design tool can connect to Claude Design.
- **Claude Design:** the product this talk is about. It lets you collaborate with Claude to create polished visual artifacts: designs, prototypes, slides, one pagers, and more. **Claude Code** is the sister tool that lets Claude write and run code.

You do not need to memorise these. Each one is explained again the first time it matters below.

## Why this lesson matters

Dan's team faced a problem you may already feel: "Cloud Code made engineers really, really fast, and the rest of us had to keep up." When engineers can build a feature in hours instead of months, the slow part is no longer building. It becomes *figuring out the right thing to build*. Designers and product managers became the new bottleneck. This lesson is the playbook a real team used to speed up the non coding parts of product development, and almost every move in it is something you could try tomorrow. As Dan put it, "There is no real secret sauce. These are all things that work well for us."

> 🔑 **The core shift:** when building gets cheap, the bottleneck moves from "can we build it?" to "do we know the right thing to build?" Everything in this lesson is about answering that second question faster and more cheaply.

## Learning objectives

By the end of this lesson you will be able to:

1. Replace a planning document with a prototype, and explain why prototypes beat docs.
2. Run a tight build loop (talk to users, design, ship, read feedback) and find the steps worth optimising.
3. Keep coordination overhead near zero by keeping teams small and letting everyone do everything.
4. Recognise when vocal power users are steering you wrong, and recover from a wrong bet quickly.
5. Apply the "prototype the thing that almost works" principle so the next model release does the hard part for you.

## Prerequisites

- A basic sense of how products get built (someone has an idea, it gets designed, built, shipped). No coding required.
- Helpful but optional: Module 2 (Core skills) and Module 8 · Lesson 27 (Running an AI-native engineering org), which describes the same bottleneck shift from an engineering leader's view.

---

## Part 1: what Anthropic Labs is, a bet factory

Dan describes Anthropic Labs as "a lab inside a frontier lab," which he calls a **bet factory**. A "bet" is a small exploratory project. Very small teams explore the frontier of what the models can do, run experiments, double down on what works, and "fold" (stop) what does not. At any time there might be a dozen tiny teams exploring different ideas. The output is lots of exploration and a small number of high conviction releases. Several products you may know came from Labs: Claude Code, Claude Design, MCP, skills, the Claude Chrome extension, and hands free audio work.

> 💡 The mental model is a funnel: many cheap bets in, most folded, a few "moonshots" out. The point of the factory is not to be right every time; it is to find out quickly which bets are worth it.

How a bet operates day to day looks a lot like lean startup methods. Dan is clear they "did not invent any of these things." The big difference is *speed*:

- **They spend time with users and researchers every single day.** Dan's two favorite questions: to users, "please complain at me"; to researchers, "what have you been surprised by lately?" Both are sources of new bets.
- **They aim to ship to users every day or two.** When someone gives feedback, they often ship the response the same day, sometimes the next.
- **They do not try to predict the future.** Instead of forecasting "in ten years we will have...", they ship, watch, learn, and repeat. For Claude Design they ran that loop "somewhere between 50 and 100 times" in ten weeks.

---

## Part 2: prototypes beat documents

Why did the team start Claude Design at all? Because Claude Code compressed timelines. "Product development timelines that used to be six months, and then they would be a month, and then a week, and now a day." Once building stopped being the bottleneck, the team needed its own accelerator for the non coding work. A designer named Nate, who had watched engineering teams speed up, hacked together a prototype over a weekend: the Agent SDK (Anthropic's toolkit for building agents), a thin IDE wrapper (a minimal code editor around it), and an existing skill he already used. He posted it in Slack, and people chimed in with what was promising and what was broken. That feedback became the roadmap for the first couple of weeks.

> 🔑 **How a Labs bet starts:** "one person, one weekend, one screen recording." Someone hacks something together and just shares it. You do not need permission or a plan to begin.

Dan lists what they deliberately did *not* do, and this is the heart of Part 2:

> ❌ **Skip these when you do not yet know exactly what you are building:** a PRD written in advance, vision docs, OKR meetings, an annual staffing plan, a two year plan, or a press release written in advance. "Those things are great if you know exactly what you are building. We did not know exactly what we were building. All we knew is that we had a spark."

Dan ran a live poll: most of the room had written or worked off a PRD in the last month. Then he asked who would rather work off a *prototype that worked and showed the feature fully*. The exact same hands went up.

> 🔑 **Why prototypes win (quote, paraphrased):** "Documents are imprecise. It is so easy for two people to look at the same doc and have two different products in mind." Prototypes are concrete and visceral. You get hands on with the thing and feel the experience yourself.

The team got their prototyping cycle down to a couple of minutes. Here is the flow Dan now uses instead of writing PRDs:

```text
PROTOTYPE INSTEAD OF A PRD (Dan's flow)
  1. Talk through the idea with a teammate. Record it. Transcribe it.
  2. Focus the talk on: what is the problem? what does a good solution do?
     why do you care about solving it? (NOT specific buttons or screens.)
  3. Hand the transcript to Claude Design and say: "give me a few options
     for this."
  4. Click the options. Feel them. Keep the one with a spark.
```

This has "effectively replaced PRDs" for Dan after nearly two decades of writing them.

The proof point that convinced them to take Claude Design to market came from a Labs ritual called a **pitch off** (people brainstorm and try to recruit each other onto their idea). The first time they ran one using Claude Design, "by the second half of it, 100% of the pitches were prototypes or slides made with Claude Design," built live in the meeting. That was the heat they needed.

---

## Part 3: tiny teams, everyone does everything

The second unusual thing about Labs is team size. Almost every bet starts as a single person, "just one person with their good buddy Claude." At this stage you are not trying to build the best product in the world. You are "looking for that little hint of heat," a sparkly glimmer worth building on. Most bets get folded before they ever pass this point, and that is fine.

The scaling is deliberately tiny:

| Stage | Team size | Goal |
|---|---|---|
| Early exploration | 1 person | Find the spark. Hours to a few days. |
| Promising spark | ~3 people (a "300% scale up") | Explore together with very little coordination overhead. |
| Heading to launch | ~5 people | Polish and ship. |

For most of Claude Design's development it was three people plus Claude. What makes that possible is that **everyone does everything**: "the engineers talk to users, PMs write code, designers do data analysis," all enabled by Claude. The lines between roles "have essentially dissolved." You still bring your own specialization and perspective, but any one person can talk to ten users, see the underlying problem, design a fix, ship it, and keep iterating solo. Most features happen exactly that way.

> 🔑 **Why small wins:** small teams minimise coordination overhead. When you do need the whole team, "that is as easy as talking to the person on your left and the person on your right and you are done." No alignment meeting, no scheduling, no waiting.

---

## Part 4: optimise every step of your loop

Minimising planning and keeping teams small already makes you fast. But the team went faster by aggressively optimising every other step of their loop. Dan stresses the loop itself is not the lesson ("this may not be the right loop for you... if you are working on hardware, this is probably the wrong loop"). The lesson is the *thought process*: ask of every step, "why are you doing this work that Claude could do for you?" and "why have you not built your own tooling?"

> 💡 **The math of optimisation:** "Every little bit of optimisation that you do on your loop is going to pay you back if you are running it 50 to 100 times in a project." A small saving per loop, multiplied by 50 to 100 loops, is huge.

Their loop is: talk to users, design features, ship code, read feedback, repeat. Here is how they optimised each step, and notice that most of these optimisations later became *features customers asked for*:

| Loop step | The friction | What they built | The twist |
|---|---|---|---|
| **Talk to users** | They wanted this to be the easiest thing in the world, because "we do things that are easy." | Shared Slack channels with every user, heavy dogfooding, and Claude reading all customer conversations to find commonalities across them. | They keep the human in the conversation; Claude does the analysis they were already doing. |
| **Design features** | When sharing a prototype, they had to record a video or ask people to pull a branch. | They used Claude Design to design Claude Design. | "If you are using your own developer tool to improve your developer tool, it is the best situation in the world." |
| **Ship code** | Exporting designs and re typing all the context into Claude Code was slow. | A handoff from Claude Design straight to Claude Code that carries the context. | Built for themselves; the first user request after multiplayer was "now how do I get this into production?" |
| **Read feedback** | Too much feedback for one person; you would miss small issues. | A feedback clustering tool built in one afternoon, with Claude matching feedback to system traces, spotting trends, and suggesting fixes (one click to send a fix to dev tooling). | Built because they "needed to have this," not as a planned project. |

**Multiplayer** is a great example. The team kept hitting a pattern: one person prototypes, shares it, another suggests a change, and the first person types it in by hand. They removed that step by letting multiple people edit the same design at once. They built it for themselves to go faster. "As soon as we brought the product over to users, the very first request was: can I use this with the rest of the people on my team in real time." So it became a first class part of the product.

> ✅ **Best practice: scratch your own itch.** Internal tooling is now fast to build (often an afternoon). The optimisations you build for your own loop are frequently the exact features your users will ask for next.

---

## Part 5: going fast does not mean being right

"Just because you are really fast does not mean you are always really right." Dan tells one clear failure. Early on they built **advanced controls** giving fine control over every pixel, aimed at power users. Their early testers included a few vocal power users who loved these tools, so the team thought they had a winner. But when they dug into actual usage, "everybody else hated them." Not disliked, *hated*. The controls were confusing and "actively harmful to the product." So they ripped them out.

The recovery took one week.

> 🔑 **The real benefit of a tight loop (quote, paraphrased):** "It is not necessarily can you always go fast, it is can you always iterate in a small enough cycle that you are able to very quickly find out when you are wrong." If they had planned this over a quarter, they would have been off track for an entire quarter, on a product that shipped in less than one.

Two lasting lessons came from that mistake:

1. **Lift the floor, not just the ceiling.** Be a tool that raises the level of craft for *everybody*, not one that only adds power for experts.
2. **Be as open as possible.** There will always be a power user with a need you cannot meet directly. So when you export from Claude Design you get HTML, CSS, and JavaScript, and the team is enabling any design tool to integrate via its existing MCPs (the open standard that lets tools plug into each other). Lift capability for everyone, and let the specialists take their work into their tool of choice.

The before and after slide drives it home. The first prototype was "a terminal and a browser and that's about it," not shiny, just a hint of promise. The launched product was vastly more. Dan's estimate: "99% of the value came from those ten weeks of iterating and shipping and talking to users every single day." The value was in the experimentation, in figuring out the right shape, not in knowing the answer up front.

To show the sustained pace: Claude Design shipped on a Friday, and "by the following Monday we had shipped 62 improvements," all based on launch day feedback. That was not heroics or all nighters. It was natural, because the team had built the muscle of doing this every day for ten weeks.

> 🔑 **The shape is the thing.** "The shape is the most important thing and the thing we all get wrong when we first start." Early on you are not chasing completeness; you are chasing the right overall shape of the product.

---

## Part 6: prototype the thing that almost works

Dan closes with the most counterintuitive lesson: **do not work on the thing that already works. Prototype the thing that almost works.** Because the models are improving so rapidly, the next model may simply fix the issues you cannot solve with engineering.

> 🔑 **Quote (paraphrased):** Claude Design had real problems in the early prototype that they "did not fix with clever engineering... We fixed them with Opus 4.7 coming out." Model releases are "a tide that lifts all boats."

So early on, you are looking for "that hint of magic," not something that handles every edge case. You are looking for something that *could* become great once the next model lands. When you find that spark, start building, start showing users, and start figuring out the shape.

Dan ends with three things you can try tomorrow. He recommends layering them on one at a time, not all at once:

1. **Skip the next PRD.** Talk with Claude or a teammate, take the transcript, focus on *why* you are solving the problem and what a good solution looks like (not specific buttons), and ask Claude Design for three prototype variations.
2. **Build the tool you have been waiting for.** Feedback clustering, a new analysis tool, whatever. Build it in one afternoon and "scratch your own itch."
3. **Turn one real feature request around in 24 hours.** Not a small bug fix, a real request. Get the idea in front of the user and follow up. The point is not speed for its own sake. "The first time you do this... you will find a bunch of roadblocks in your existing process," from your deploy steps to your code review flow. Going through it once exposes them.

---

## Key takeaways

1. **The bottleneck moved to knowing what to build.** When building is cheap, speed up the non coding steps: discovery, design, feedback.
2. **Prototypes beat documents.** Docs are imprecise; prototypes are concrete and let you feel the experience. Replace PRDs with prototype variations from a recorded problem conversation.
3. **Keep teams tiny.** One person to find the spark, three to explore, five to launch. Everyone does everything, so coordination overhead nearly vanishes.
4. **Optimise every step of your loop.** A small saving times 50 to 100 loops is huge. Your internal optimisations often become the features users request.
5. **Fast means you find mistakes fast.** The win is a cycle short enough to catch a wrong bet in a week, not a quarter.
6. **Lift the floor and stay open.** Raise craft for everyone, and let power users take work into their own tools.
7. **Prototype the thing that almost works.** Let the next model release do the hard part.

## Common pitfalls

- ❌ Writing a detailed PRD before you know what you are building, then defending it instead of the user's real need.
- ❌ Growing the team to "go faster" and drowning in coordination overhead instead.
- ❌ Trusting vocal power users as if they speak for everyone; check actual usage.
- ❌ Planning a risky idea over a whole quarter, so a wrong turn costs a quarter to correct.
- ❌ Doing analysis and feedback triage by hand when Claude could do the first pass.
- ❌ Polishing the thing that already works instead of betting on the thing that almost works.

---

## 🛠️ Capstone Project: The 10-Loop Sprint

> This is the main hands on project for the lesson, and it turns Dan's three "try tomorrow" actions into one connected build. You will pick a small real idea and run the Labs loop on it ten times in a short window, replacing documents with prototypes and building your own tooling along the way.

### What you will build

A small, shipped feature or tool, *plus* a one page "loop log" showing the ten iterations: what you tried, what users said, and what you changed. The deliverable is the evidence that you ran a tight loop, not a polished masterpiece.

> 🎯 **Pick the thing that almost works.** Choose an idea where today's model gets you maybe 80% of the way, with a spark of magic but rough edges. That is the sweet spot: you can ship something useful now, and the next model may close the gap.

### Why this is the perfect practice

| Lesson skill | Where you use it in the Capstone |
|---|---|
| Prototype instead of a PRD | Milestone 1, the recorded problem conversation |
| Tiny team, everyone does everything | Milestone 2, solo or pair |
| Optimise the loop | Milestone 3, build one tool for yourself |
| Talk to users every cycle | Milestone 4, the ten loops |
| Find mistakes fast | Milestone 5, kill one wrong bet in a week |
| Turn a request around in 24 hours | Milestone 6, the speed test |

### Milestones (build them in order, each one is shippable)

1. **Record, do not write.** Talk through your idea with a teammate (or out loud to yourself). Record and transcribe it, focusing only on the problem, what a good solution does, and why you care. Hand it to Claude (or Claude Design) and ask for three prototype variations. Keep the one with a spark. (No PRD allowed.)
2. **Set up a tiny team and a feedback channel.** Work solo or in a pair. Create a shared channel with 3 to 5 people who will actually use the thing. Dogfood it yourself daily.
3. **Build one tool for yourself in an afternoon.** Scratch your own itch. Easiest version: have Claude read all your feedback channel messages and cluster them into themes each morning. This becomes your dashboard for the loops.
4. **Run ten loops.** Talk to users, change one thing, ship, read the clustered feedback, repeat. Aim to ship something every day or two. Log each loop in one or two lines.
5. **Kill a wrong bet fast.** Somewhere in the ten loops you will build something users do not want. When usage (not the loudest voice) tells you so, rip it out within a week. Record what you learned.
6. **The 24-hour test.** Take one real request from a user, turn it around in 24 hours, and follow up with them. Write down every roadblock you hit in your own process (deploys, reviews, approvals). Those roadblocks are your next thing to fix.

### How you will know you are done

- ✅ You shipped something real to at least a few users, starting from a prototype, **never a PRD**.
- ✅ Your loop log shows **ten iterations** with what changed and why.
- ✅ You built **one tool for yourself** that saved time across the loops.
- ✅ You **killed one feature** because usage (not a vocal power user) told you to, and it took about a week or less.
- ✅ You turned one real request around in **24 hours** and listed the process roadblocks it exposed.

> 💡 **Keep yourself honest:** if you find yourself writing a long planning doc, stop and prototype instead. If you find yourself believing one loud user, go check what everyone else actually does.

---

## Practice exercises (optional extra reps)

> **What these are:** small, independent reps, each focused on one move from the talk. Optional. The Capstone above already exercises all of them together.

### Exercise 1: the prototype, not the PRD (foundational)
Take a feature you would normally spec. Record a five minute problem conversation, transcribe it, and ask Claude for three prototype options. Compare how much clearer the prototypes are than your usual doc.

### Exercise 2: scratch your own itch (foundational)
Pick one tool you have been waiting for (a feedback clusterer, a quick analysis script). Build it in a single afternoon. Note how long you had been waiting versus how long it took.

### Exercise 3: dissolve a role boundary (intermediate)
Do one task this week that is outside your usual role (a PM writes code, an engineer talks to five users, a designer does data analysis), using Claude to help. What did you learn that you would have missed?

### Exercise 4: the wrong bet drill (intermediate)
Look at a feature you shipped that few people use. Was it driven by vocal power users? Decide, today, whether to rip it out, and estimate how long that would take.

### Exercise 5: the 24-hour turnaround (advanced)
Take one genuine user request and ship a response within 24 hours. Keep a list of every step in your process that slowed you down. Pick the worst one and fix it.

---

## Cheat sheet

```text
WHEN BUILDING IS CHEAP
  The bottleneck moves from "can we build it?" to "what should we build?"
  Speed up discovery, design, and feedback, not just coding.

PROTOTYPE > DOCUMENT
  Record a problem conversation -> transcribe -> ask Claude for 3 options.
  Talk about WHY and what a good solution does. Not buttons, not screens.
  Docs are imprecise. Prototypes are concrete. Pick the one with a spark.

TEAM SIZE
  1 to find the spark, ~3 to explore, ~5 to launch. Everyone does everything.

OPTIMISE THE LOOP (talk -> design -> ship -> read feedback -> repeat)
  Small saving x 50-100 loops = huge. Build your own tooling in an afternoon.
  Your internal optimisations often become user-requested features.

GOING FAST
  Fast = you find mistakes fast. Catch a wrong bet in a week, not a quarter.
  Trust usage, not the loudest user. Lift the floor; stay open.
  Prototype the thing that ALMOST works; let the next model fix the rest.

TRY TOMORROW (layer them on)
  1. Skip the next PRD; prototype instead.
  2. Build the tool you've been waiting for, in one afternoon.
  3. Turn one real request around in 24 hours.
```

## How this connects to the rest of the course

- **Earlier, Module 8 · Lesson 27 (Running an AI-native engineering org):** the same bottleneck shift from an engineering leader's chair; this lesson is the product and design side of it.
- **Earlier, Module 2 (Core skills) and skills:** Claude Design and these loops are built from skills, the Agent SDK, and good prompting.
- **Next, Module 8 · Lesson 29 (From one person to 80):** another small team scaling fast by keeping processes radically simple and dogfooding their own product.
- **Later, Module 8 · Lesson 31 (Building AI-native at enterprise scale):** how big companies apply the same "prototype to validate, then ship" idea inside large, older code bases.

---

*Source: "Designing with Claude: From prompt to production" by Dan Carey (Anthropic Labs), Code with Claude 2026, London. The flow boxes and tables are faithful paraphrases of what Dan described on stage; they are illustrative reconstructions, not verbatim slides.*

# Module 7 · Lesson 24: Building with Claude on Google Cloud

> **Course:** Building with Claude, a self-paced course
> **Module 7:** Deploying on your cloud
> **Speaker:** Iman Nardini, Developer Advocate, Google Cloud (London)
> **Source talk:** [Building with Claude on Google Cloud](https://www.youtube.com/watch?v=l8fxVYIP4HQ) · [full transcript](../../transcripts/code-with-claude-2026-london-2026/08_building-with-claude-on-google-cloud.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

You can take an app idea from a paper sketch all the way to a production deployment on Google Cloud without being a Google Cloud expert, by running Claude models hosted on Google Cloud and letting Claude Code use its planning mode, sub agents, skills, plugins, and Google's documentation MCP server to design, build, secure, deploy, and analyse the app for you.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you build and deploy a small **Feedback App** end to end on Google Cloud, wearing the same five "hats" Iman wears in the talk (product manager, designer, engineer, security reviewer, and analyst). Everything before the Capstone teaches the pieces you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section near the end, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[Anthropic's Claude models on Vertex AI (Google Cloud docs)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude)** (docs). The official provider reference for running Claude on Vertex AI (setup, access, requests), durable even as model versions change.
> - **[Claude on Vertex AI (Anthropic docs)](https://platform.claude.com/docs/en/api/claude-on-vertex-ai)** (docs). Anthropic's complementary guide for calling Claude on Vertex (SDKs, endpoints, regions).

## A few plain-language basics first

This lesson mixes Claude terms with Google Cloud terms. Here they are in plain words, so nothing below is confusing:

- **Claude Code:** Anthropic's coding agent. It is a tool that runs in your terminal (the text window where you type commands) and can read, write, and run code on your behalf. Iman calls it "the Anthropic's coding agent."
- **Model:** one specific version of the AI, for example "Opus 4.7" or "Sonnet 4.6." Different models trade off intelligence, speed, and price.
- **Google Cloud:** Google's cloud platform, a set of rented computers and services you use over the internet instead of owning servers yourself.
- **Hosting a model:** running the AI on someone's servers. When a Claude model is "hosted on Google Cloud," your requests go to Google's copy of the model, billed and governed through your Google account.
- **Token:** the unit a model reads and writes in (roughly three quarters of a word). You are billed per token, so more tokens means more cost.
- **API (Application Programming Interface):** the connection your code uses to send a request to a service and get an answer back.
- **MCP (Model Context Protocol):** an open standard that lets Claude connect to outside tools and data sources. An **MCP server** is a small service that exposes those tools to Claude.
- **Skill:** a reusable, packaged set of instructions and steps that Claude Code can load to do a specific job well (for example "deploy to Cloud Run").
- **Plugin:** a custom add on for Claude Code that bundles behaviour, for example a company specific security review.
- **Sub agent:** a second Claude working in parallel on its own task, so several jobs run at once like members of a team.
- **CI/CD:** "continuous integration / continuous deployment." CI is the automatic build and test of your code when you change it. CD is the automatic deployment of that code to a running environment.
- **PR (Pull Request):** a proposed change to a code repository that someone (or you) reviews and merges.

You do not need to memorise these. Every term is explained again the first time it appears below.

## Why this lesson matters

Most developers already use an AI coding tool. Far fewer use that same tool to actually **build and deploy** something on a cloud platform. That gap is exactly what Iman set out to close: "the goal of this presentation is showing you how you can do better." In a real company, shipping a feature normally takes a whole team (a product manager, a designer, an engineer, a security reviewer, and an analyst). This lesson shows how one person, with Claude Code plus Claude models running on Google Cloud, can cover that entire software lifecycle, and end up with a real, deployed, secured, instrumented application.

## Learning objectives

By the end of this lesson you will be able to:

1. Set up Claude Code to use Claude models **hosted on Google Cloud**, and explain the advantages of doing so.
2. Use Claude Code's core building blocks (**planning mode**, **sub agents**, **skills**, **plugins**, and an **MCP server**) to move an idea from sketch to running app.
3. Wire up a real Google Cloud deployment path: a serverless API, a database, an analytics warehouse, a dashboard, and a CI/CD pipeline.
4. Run a security review before promoting code to production, and use a development to production promotion flow.

## Prerequisites

- Module 1 (the basics of installing and running Claude Code).
- A Google Cloud account with a project you can deploy to (any tier works for learning).
- Helpful but optional: Module 2 (planning, sub agents, and skills are introduced there in more depth).

---

## Part 1: the setup, running Claude models on Google Cloud

Before you build anything, you point Claude Code at Claude models that are hosted on Google Cloud. Iman calls this "pretty straightforward."

There are several ways to authenticate (prove who you are so you are allowed to use the models). The simplest is **Application Default Credentials**, which means Claude Code automatically finds the right login from your environment instead of you pasting in a secret key.

```bash
# Application Default Credentials: log in once, and your tools
# pick up the credentials automatically from your environment.
gcloud auth application-default login
```

After that, a setup wizard does the rest. In Iman's words it "will detect the project and the region, verify which models, which Claude models are available on your project," and let you "pin them" (lock in the ones you want) for your coding session.

```text
Claude Code setup wizard (illustrative)
  > Detected project:  feedback-app-prod
  > Detected region:   europe-west2 (London)
  > Available Claude models on this project:
       [x] claude-opus-4-7
       [x] claude-sonnet-4-6
  > Pinned models for this session: opus-4-7, sonnet-4-6
```

### Why run Claude models on Google Cloud

Iman lists several advantages. Here they are as a table:

| Advantage | What it means in plain words |
|---|---|
| **Pay per token** | You are billed for what you use. "You don't receive any message per cap" (no fixed message limits). |
| **Provisioned throughput** | If a production app needs more capacity, you can reserve extra dedicated capacity for the models you use. |
| **No API keys to manage** | "You don't need some API key to store or rotate." Access comes from your project, not a secret you have to guard. |
| **Your data stays in your project** | "The data that you use during your session, they remain in that project," under your own policies. |
| **Multi region / global endpoints** | Models can be served from multiple regions for high availability. You pick what fits where you develop. |
| **High service standards** | Google Cloud backs serving Claude models with strong quality and availability commitments. |

> 🔑 **Key idea: the model is the same Claude, the surroundings change.** You still get Opus and Sonnet. What changes is the billing, the security boundary, and the operational guarantees around them. That is the whole "build on your cloud" pitch.

> 💡 The point of a frictionless setup is that you forget about it. Once Claude Code is pinned to your Google Cloud models, the rest of the lesson is just building.

---

## Part 2: the five hats (one person, a whole team)

Iman frames the demo around a team that ships a feature: a **product manager** with the idea, a **designer** (UI/UX) who visualises it, a **software engineer** who builds the back end, a **security engineer** who reviews it, and an **analyst** who measures how people use it. He then "puts on five different hats" and plays all of them himself, with Claude Code.

The app he builds is a **feedback app**: a form the audience uses to rate his talk, plus the back end and analytics behind it.

> 🔑 **Key idea: Claude Code augments the whole lifecycle, not just the coding step.** The interesting claim is not "AI writes code." It is that one developer can credibly cover design, build, security, deployment, and analytics, because Claude Code has a different tool for each stage.

### Hat 1: Product manager, sketch to wireframe

The PM has an idea but, in the old world, has to ask the design team for a prototype and wait. Instead, Iman draws a rough sketch on paper, hands the picture to Claude, and asks it to render a **wireframe** (a simple, low detail layout of a screen).

He sets this up with a `CLAUDE.md` file. (A `CLAUDE.md` file is a plain text file in your project that gives Claude Code persistent instructions, like a role and a goal, so you do not repeat them every time.)

```text
# CLAUDE.md  (PM hat)
Role: You are a product manager.
Goal: Turn the attached hand sketch into a wireframe for the UX designer.
When done: commit the wireframe and open a pull request on GitHub.
```

In seconds Claude produces the wireframe, and because the environment is configured for Git, it can even open the PR itself. As Iman notes, "this is a PM that probably doesn't know how to use Git," but Claude Code handles it.

### Hat 2: Designer, wireframe to production interface (planning mode)

Now Iman is the designer. He takes the wireframe and builds a real, multi page interface: a landing page, a thank you page, a form page, and a dashboard view (to watch the room's "temperature" during the demo).

The key tool here is **planning mode**. Planning mode puts Claude in a state where "he thinks and he proposes before he starts coding." You see the plan first and can adjust it before any code is written.

> 💡 **Why planning mode matters for design.** It gives you "some degree of freedom to decide what to build before Claude starts building." You catch a wrong direction at the cheap stage (the plan) instead of the expensive stage (already built code).

```text
Designer hat, planning mode (illustrative plan Claude proposes)
1. Create landing page with feedback call to action
2. Create feedback form (rating + comment)
3. Create thank you page
4. Create live dashboard view (room sentiment)
-> Review this plan, then I will build and open a PR.
```

In reality, Iman notes, you might connect Claude to **Figma** (a popular design tool) to pull in real design details. Once he approves the plan, Claude builds the pages quickly and opens another PR, which Iman reviews and merges.

---

## Part 3: building and deploying the back end

Now Iman wears the **software engineer** hat. The front end exists; the job is to package the back end and deploy it on Google Cloud. Most people, by his own poll, do not know how to deploy on Google Cloud. Two recent integrations make that a non issue.

### The two integrations that make this possible

| Integration | What it gives you |
|---|---|
| **Developer Knowledge API + its MCP server** | An MCP server that lets Claude read **fresh** Google Cloud documentation and implementation guides, "refreshed every 24 hours," so Claude designs an architecture based on current docs, not stale training data. |
| **Official Google Cloud skills** | Packaged, reusable procedures for actually doing the work, for example "how do I deploy on Cloud Run?" or "how do I read raw records from Firestore to BigQuery?" |

> 🔑 **Key idea: documentation MCP for the *what*, skills for the *how*.** The MCP server helps Claude figure out the right architecture from up to date docs. The skills help Claude carry out each concrete deployment step. Together they let you "actually deploy it on Google Cloud without you knowing about Google Cloud itself."

### The architecture Claude designs

Using the Developer Knowledge API, Claude proposes a simple but real cloud architecture for the feedback app:

```text
[ Feedback form ]
       |
       v
[ API on Cloud Run ]  ---- serverless function (scales to zero, pay per use)
       |
       v
[ Firestore ]         ---- the live website database
       |
       v   (data pipeline)
[ BigQuery ]          ---- analytical data warehouse for raw feedback
       |
       v
[ Looker ]            ---- dashboard tool for the PM
```

A few terms in that picture:

- **Cloud Run:** a serverless way to run your code. "Serverless" means you do not manage any servers yourself; it scales up and down automatically and you pay per use.
- **Firestore:** Google's managed website database for live app data.
- **BigQuery:** Google's **analytical data warehouse**, a database built for analysing large amounts of data and running statistics.
- **Looker:** Google's dashboard and business intelligence tool for presenting numbers visually.

### Building it in parallel with sub agents

To build the components, Iman uses **sub agents**. A sub agent is a second (or third) Claude running in parallel on its own task. This lets him "parallelize tasks, simulating like a team sprint": one sub agent for the API, one for the BigQuery data pipeline, and one for the dashboard.

```text
Sub agents (run in parallel, like a sprint)
  sub-agent A  ->  build the API service
  sub-agent B  ->  build the Firestore -> BigQuery data pipeline
  sub-agent C  ->  build the dashboard
```

The flow Iman shows:

1. Ask Claude to design the architecture and the API spec, using the MCP server and skills.
2. Claude queries the MCP server for specific docs, then builds the architecture and an API specification (the detailed description of the API's paths and behaviour).
3. Sub agents build the components in parallel, then Claude **runs tests** on the result.
4. A Google Cloud skill builds the deployment pieces: a CI/CD pipeline using **Cloud Build** (for CI, the automated build and test) and **Cloud Deploy** (for CD, the automated deployment).
5. Claude opens a PR. Merging it **triggers the pipeline**, which builds the API and dashboard, then cuts a release.
6. Cloud Deploy ships the app to a **development environment** automatically (no manual promotion needed yet, because it is still in development).

> 💡 **Why this is fast.** Because Claude already wrote and ran the tests as part of building, the deploy step is not a leap of faith. The pipeline simply re runs them and ships.

---

## Part 4: security review and promotion to production

The app runs in development. Before production, Iman wears the **security engineer** hat. As he puts it, "before to move to production, we want to be confident about the code itself."

There are many ways to run a security review in Claude Code. Iman uses a **custom plugin**, because real companies have their own security requirements. A plugin lets you bake those requirements into a repeatable check.

What his plugin checks (one possible scenario, not an exhaustive list):

- **Input validation:** making sure the app safely handles whatever a user types into the form.
- **Service account permissions:** a **service account** is the identity your deployed app runs as. You want to "limit the permission that the services that the application can get access to," following the principle of giving an app only the access it truly needs. This avoids "any unexpected situation."
- Common top issues for the type of app being deployed.

```text
# Custom security plugin (illustrative prompt)
Review this deployment for:
  1. Missing input validation on the feedback endpoint.
  2. Over-broad service account permissions (least privilege).
Fix issues found, re-run tests, and open a PR.
```

The plugin finds a problem (missing input validation, over broad permissions), Claude fixes the code in seconds, re runs the tests, and opens a new PR. Because this PR **passes the review**, the pipeline not only builds and releases, but the release reaches the development environment where Iman can review the running app one more time and then **promote and approve** it to production.

> 🔑 **Key idea: the gate is the review, not the human's memory.** The development to production promotion only happens after the security review passes. The review is encoded as a plugin, so it runs the same way every time, for every change.

> ✅ **Best practice: least privilege for service accounts.** Always give your deployed app the smallest set of permissions it needs to function. Iman's plugin tightening the service account is a textbook example.

Once promoted, the production app looks identical to the development one. The difference is everything behind it: it has been reviewed, tested, and gated.

---

## Part 5: closing the loop with analytics

The final hat is the **analyst**. The app is live, so now Iman wants to learn from it: for example, "how long is taking you to provide me a feedback?" If it takes too long, the UI might need work.

Most people do not know how to run analytics on Google Cloud either, but the same integration story applies. Google Cloud provides **official MCP servers** that let Claude run analytics and even build a dashboard on the fly.

The two MCP servers Iman uses here:

| MCP server | What Claude does with it |
|---|---|
| **BigQuery MCP server** | Analyse the raw feedback stored in BigQuery and generate statistics from it. |
| **Looker / dashboard MCP server** | Turn those statistics into a real dashboard in Looker, so you get back "just one link." |

The flow: raw feedback lands in BigQuery, the BigQuery MCP server computes statistics (which, on their own, are just numbers in a terminal that no PM wants to read), and the dashboard MCP server turns those numbers into a shareable Looker dashboard, for example showing how long each feedback session took and comparing distributions.

> 💡 **Why two MCP servers, not one.** One server is good at querying data; the other is good at presenting it. Chaining them means Claude can go from raw rows to a polished, shareable dashboard "even if you don't know a dashboard tool."

---

## Key takeaways

1. **Run Claude on your cloud to keep the model, change the surroundings.** Same Opus and Sonnet, but with per token billing, no API keys to manage, your data in your project, and high availability.
2. **Setup is meant to be invisible.** Application Default Credentials plus a wizard that detects your project, region, and available models gets you coding fast.
3. **One person can cover the whole lifecycle.** Planning mode (design), sub agents (parallel build), skills and the documentation MCP server (deploy), plugins (security), and analytics MCP servers (insight).
4. **Documentation MCP for the architecture, skills for the steps.** Fresh docs tell Claude *what* to build; skills tell Claude *how* to deploy it.
5. **Gate production on a repeatable review.** Encode your security checks as a plugin so promotion only happens after the review passes.
6. **Close the loop.** Pipe usage data into BigQuery and turn it into a Looker dashboard, so the app's own data drives the next improvement.

## Common pitfalls

- ❌ Storing and rotating API keys by hand when Application Default Credentials would remove that chore entirely.
- ❌ Letting Claude start coding the interface before you have reviewed a plan (skip planning mode and you lose your chance to steer cheaply).
- ❌ Asking one Claude to build the API, the pipeline, and the dashboard in sequence when sub agents could do them in parallel.
- ❌ Giving the deployed app's service account broad permissions "just to make it work."
- ❌ Promoting straight to production without a review gate in between.
- ❌ Stopping at raw numbers in a terminal instead of turning them into a dashboard a non engineer can read.

---

## 🛠️ Capstone Project: ship the Feedback App on Google Cloud

> This is the main hands on project for the lesson, and the best way to make everything above stick. You are going to build and deploy the exact app Iman demoed: a small feedback app, taken from a paper sketch to a secured, production deployment with a live analytics dashboard. Start small (one page and a terminal) and grow it as far as you like.

### What you will build

**FeedbackLoop** is a feedback collection app that runs entirely on Google Cloud and is built end to end through Claude Code, wearing the five hats from the talk. It has:

1. **A front end:** a landing page, a feedback form (rating plus comment), a thank you page, and a live sentiment dashboard.
2. **A back end:** a serverless API on Cloud Run that writes feedback to Firestore.
3. **A data path:** a pipeline that ingests raw feedback into BigQuery.
4. **A pipeline:** CI/CD with Cloud Build and Cloud Deploy, gated by a security review.
5. **Analytics:** a Looker dashboard built from BigQuery statistics.

> 🎯 **Pick your world.** Reuse the **talk feedback** scenario so it matches the lesson, or swap in something you find fun: a **café order rating** app, a **library book request** form, or a **gym class booking** feedback tool. Any world works as long as it collects input from users, stores it, and is worth analysing.

### Why this is the perfect practice

| Lesson skill | Where you use it in FeedbackLoop |
|---|---|
| Pointing Claude Code at Google Cloud models | Milestone 1, you cannot proceed without it |
| Planning mode for design | Milestone 3, propose before building the UI |
| Sub agents for parallel building | Milestone 4, API, pipeline, and dashboard at once |
| Documentation MCP + skills for deployment | Milestone 4 and 5, design then deploy |
| Plugin based security review | Milestone 6, the gate before production |
| Analytics MCP servers | Milestone 7, BigQuery to Looker |

### Milestones (build them in order, each one works on its own)

1. **Connect.** Authenticate with Application Default Credentials, run the setup wizard, and pin the Claude models available in your project. Confirm Claude Code is talking to Google Cloud hosted models.
2. **Sketch to wireframe (PM hat).** Write a `CLAUDE.md` giving Claude a PM role. Draw the app on paper, photograph it, and ask Claude to produce a wireframe and open a PR.
3. **Wireframe to interface (designer hat).** Switch to **planning mode**. Have Claude propose a plan for the landing, form, thank you, and dashboard pages. Review the plan, then let it build and open a PR.
4. **Build the back end (engineer hat).** Connect the Developer Knowledge API MCP server. Ask Claude to design the architecture (Cloud Run + Firestore + BigQuery + Looker) and an API spec. Use **sub agents** to build the API, the data pipeline, and the dashboard in parallel. Let Claude run the tests.
5. **Deploy.** Use the official Google Cloud skills to build a CI/CD pipeline (Cloud Build for CI, Cloud Deploy for CD). Merge the PR, watch the pipeline run, and confirm the app deploys to a **development** environment.
6. **Secure and promote (security hat).** Write a custom security **plugin** that checks input validation and tightens the service account to least privilege. Run it, let Claude fix what it finds, re run tests, and only then **promote** the release to production.
7. **Analyse (analyst hat).** Connect the BigQuery MCP server to compute statistics from your stored feedback, then the Looker MCP server to turn them into a shareable dashboard. End with one dashboard link.

### How you will know you are done

- ✅ Claude Code is using Claude models hosted on **your** Google Cloud project (not an external API key).
- ✅ The app is **deployed to production** and reachable at a URL, having passed through development first.
- ✅ Your security review ran as a **plugin** and visibly changed the code (input validation added, permissions tightened) before promotion.
- ✅ You can open a **Looker dashboard** built from real feedback data, with at least one useful statistic.
- ✅ You can point to which Claude Code feature did each stage: planning mode, sub agents, skills, the documentation MCP, the plugin, and the analytics MCP servers.

> 💡 **Keep yourself honest:** if you find yourself doing a deployment step by hand, stop and ask whether a skill or the documentation MCP could do it for you. The whole point is deploying without being a Google Cloud expert.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self contained tasks. Each one gives you focused practice on a single skill from the lesson. They are optional and independent. The **Capstone above is the main build**, and it already exercises all of these, so feel free to skip straight to it.

### Exercise 1: frictionless setup (foundational)
Set up Application Default Credentials and run the Claude Code wizard. Pin two models. Write down which models your project makes available and which regions they are served from.

### Exercise 2: plan before you build (foundational)
Pick any small UI (a single signup form is fine). Use planning mode to make Claude propose the build steps. Edit the plan to change one thing before approving. Note what you caught at the plan stage that you would have had to undo later.

### Exercise 3: parallel build with sub agents (intermediate)
Take a feature with three independent parts (for example header, form, footer, or three API endpoints). Have Claude build them with sub agents in parallel. Compare the wall clock time to building them one after another.

### Exercise 4: documentation MCP for a real deploy (intermediate)
Connect the Developer Knowledge API MCP server. Ask Claude to design a deployment for a tiny "hello world" API on Cloud Run, citing the docs it read. Deploy it. Confirm it scales to zero when idle.

### Exercise 5: encode a security gate (advanced)
Write a small security plugin that checks one concrete thing (for example: the service account must not have project wide admin rights). Run it against a deliberately over permissioned deployment and confirm it both flags and fixes the problem before allowing promotion.

---

## Cheat sheet

```text
RUN CLAUDE ON GOOGLE CLOUD
  1. Authenticate: Application Default Credentials (no API keys to manage).
  2. Wizard detects project + region, lists Claude models, pin the ones you want.
  3. Same Claude (Opus/Sonnet); per-token billing, data stays in your project.

THE FIVE HATS (one person, whole lifecycle)
  PM        -> sketch to wireframe                (CLAUDE.md role + PR)
  Designer  -> wireframe to interface             (PLANNING MODE)
  Engineer  -> back end + deploy                  (SUB AGENTS, SKILLS, doc MCP)
  Security  -> review before production           (custom PLUGIN gate)
  Analyst   -> usage to insight                   (BigQuery MCP -> Looker MCP)

WHICH TOOL FOR WHICH JOB
  Decide what to build first ..... planning mode
  Do several builds at once ...... sub agents
  Know the right architecture .... Developer Knowledge API (doc MCP, fresh daily)
  Carry out a deploy step ........ official Google Cloud skills
  Enforce your own checks ........ a custom plugin
  Turn data into a dashboard ..... BigQuery MCP + Looker MCP

REMEMBER
  - Least privilege for the service account.
  - Gate production on a repeatable review, not memory.
  - Stop at the dashboard, not at numbers in a terminal.
```

## How this connects to the rest of the course

- **Earlier, Module 2 (Core skills):** planning mode, sub agents, and skills are introduced there; this lesson puts them to work on a real cloud deploy.
- **This module, Module 7 · Lesson 25 (AWS):** the same "run Claude on your cloud" idea, with Amazon Bedrock, Claude platform on AWS, and Bedrock AgentCore.
- **This module, Module 7 · Lesson 26 (Microsoft Foundry):** the same idea again, with deployed Claude models, an agent framework, and MCP tools.
- **Later, Module 5 (Claude Managed Agents):** sub agents and the parallel "team sprint" pattern grow into full multi agent systems.

---

*Source: "Building with Claude on Google Cloud" by Iman Nardini (Google Cloud), Code with Claude 2026, London. Code snippets and the architecture diagram are illustrative reconstructions of the approaches shown in the talk. Adapt model names, service names, and commands to the current Google Cloud and Claude Code tooling.*

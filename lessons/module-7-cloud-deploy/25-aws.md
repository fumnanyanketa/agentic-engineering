# Module 7 · Lesson 25: AI with Claude on AWS, From Code to Orchestration

> **Course:** Building with Claude, a self-paced course
> **Module 7:** Deploying on your cloud
> **Speaker:** Antonio Rodriguez, Amazon Web Services (London)
> **Source talk:** [AI with Claude on AWS: From code to orchestration](https://www.youtube.com/watch?v=5YHIrTYxM3w) · [full transcript](../../transcripts/code-with-claude-2026-london-2026/22_ai-with-claude-on-aws-from-code-to-orchestration.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

You can take a Claude app from a prototype on your laptop to a fully production ready system on Amazon Web Services, choosing among three ways to use Claude on AWS (Bedrock, the Claude platform on AWS, or Claude Desktop pointed at AWS), and gaining data control, consolidated billing, observability, scalability, and a secure place to host agents along the way.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you take a real app from prototype to production on AWS, configuring Claude Code to run on Bedrock and layering in the production concerns Antonio stresses: security, observability, and cost control. Everything before the Capstone explains the choices you will make there. If you want the finish line first, jump to the **"Capstone Project"** section, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[What is Amazon Bedrock? (AWS docs)](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html)** (docs). The official overview of Bedrock as a managed, multi-provider foundation-model service, covering the durable production surroundings (security, regions, APIs) the lesson stresses.
> - **[Claude in Amazon Bedrock (Anthropic docs)](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock)** (docs). Anthropic's complementary guide for calling Claude specifically through Bedrock.

## A few plain-language basics first

This lesson mixes Claude terms with AWS terms. Here they are in plain words:

- **Claude Code:** Anthropic's coding agent, a tool that runs in your terminal and can read, write, and run code for you.
- **Claude Desktop:** the Claude desktop application (the app you chat with), as opposed to calling Claude from your own code.
- **Model:** one specific version of Claude, for example "Opus 4.7" or "Haiku." Models trade off intelligence, speed, and price.
- **Token:** the unit a model reads and writes in (roughly three quarters of a word). You are billed per token.
- **AWS (Amazon Web Services):** Amazon's cloud platform, a large set of rented computers and services.
- **Amazon Bedrock:** AWS's managed service for using foundation models (large AI models) through one API, including Claude models.
- **Inference:** running a model to get an answer. An "inference request" is one call to the model.
- **Region:** a geographic location where AWS runs servers (for example "London region"). Choosing a region controls where your data and compute live.
- **Agent:** an AI that takes a series of actions on its own toward a goal, rather than answering in one shot.
- **Agent framework:** a code library for building agents, for example LangChain, CrewAI, or the Claude Agent SDK.
- **Fine tuning:** further training a model on your own examples so it specialises in your task.
- **MCP (Model Context Protocol):** an open standard that lets a model connect to outside tools and data.

You do not need to memorise these. Each is explained again the first time it appears below.

## Why this lesson matters

Antonio describes himself, only half jokingly, as a "cloud whisperer," because "we are really just whispering orders these days not really writing code." The hard part is no longer producing a prototype; it is turning that prototype into something you can safely run in production: with your data kept private, your costs under control, your usage observable, and uptime you can rely on. This lesson is the bridge "from prototypes that you might have in your computer to fully production ready applications that you can have in the cloud." It also lays out the three concrete ways to use Claude on AWS, so you can pick the one that meets you where you are.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain the **three angles** AWS offers for using Claude (features, security, scalability) and why they matter for production.
2. Choose among the **three ways** to use Claude on AWS: directly through Bedrock, through the Claude platform on AWS, or through Claude Desktop / CodeWhisperer pointed at AWS.
3. Configure **Claude Code to run on Bedrock**, including region, default model, and token / rate limiting settings.
4. Identify the AWS building blocks for going to production safely: guardrails, observability, private networking, identity integration, and a secure home for agents (Bedrock AgentCore).

## Prerequisites

- Module 1 (installing and running Claude Code).
- An AWS account you can experiment in (a free workshop account is enough for learning).
- Helpful but optional: Module 2 (sub agents, plugins, skills, and hooks, which appear in the AWS workshop).

---

## Part 1: better together, why Claude on AWS

Antonio frames the whole talk as a "story about teamwork, a story about better together." Anthropic and AWS have a long, deep partnership: Amazon has made a multi billion dollar investment in Anthropic, and AWS is Anthropic's primary cloud provider.

Two pieces of that partnership are worth knowing because they affect you as a user:

- **Project Rainier:** "one of the largest AI computer infrastructure that was built for training and hosting the Claude models." This is the muscle behind the models you call.
- **Trainium chips:** custom, purpose built chips made by Amazon specifically for Claude models. Antonio notes they are on the "third generation," and they are why you can get strong speed in a cost effective way when spending tokens with Claude. (A **chip** here is the specialised processor that runs the model.)

> 🔑 **Key idea: the infrastructure is part of the value.** Purpose built chips and dedicated infrastructure are not trivia. They are why running Claude on AWS can be fast and cost effective at scale.

---

## Part 2: the three angles AWS offers

Antonio organises the technical case into three angles.

### Angle 1: a comprehensive feature platform

Bedrock is "a full platform," not just a model endpoint. Around the core foundation models (with Claude models "a very important part of that") you get features for the whole developer journey:

| Feature area | What it does |
|---|---|
| **Evaluation** | Tools to measure how well a model does on your task. |
| **Prompt optimization** | Help improving your prompts. |
| **Fine tuning** | Specialise a model on your own data. AWS is "the only provider that allows you to fine tune Haiku in example in the cloud." |
| **Model distillation** | Create a smaller, cheaper model that imitates a larger one. |
| **Knowledge bases** | Fully managed storage for **RAG** use cases. (RAG, "retrieval augmented generation," means giving the model relevant documents to ground its answers.) |
| **Guardrails** | Safety controls: content filters, denied topics, automatic masking of **PII** (personally identifiable information, like names or card numbers), and hallucination controls via grounding and automated reasoning checks. |
| **Agentic AI tools** | Building blocks for agents, including **Bedrock AgentCore** (covered in Part 4). |

### Angle 2: security and data control

This is the angle Antonio spends the most time on, because production teams care about it most.

- **Keep your data in your boundary.** You "avoid this hopping of data going to the public internet" and keep everything "private in your AWS boundary."
- **Zero operator access.** The latest inference engine in Bedrock has "zero operator access," meaning "no one from Amazon or from Anthropic can actually get access to those instances." Your data stays private.
- **Not used for training.** "No one is using that data for training models or anything like that."
- **Compliance.** Bedrock supports many regulated industry standards, for example **FedRAMP** and **HIPAA** (a US health data privacy law). This matters for "highly regulated industries" like banking and health care.

> ✅ **Best practice: pick your region to meet your rules.** You can "deploy Claude only in London region" or only in the European region to align with regulations like **GDPR** (Europe's data protection law). Region choice is a compliance lever, not just a latency one.

### Angle 3: scalability

Using Claude through Bedrock gives "practically infinite scalability." You decide how to do deployments and which regions to use, so you can go safely to production and "scale at the cloud scale."

---

## Part 3: one slide of production reasons, and the three ways to use Claude

### The "why better together" summary

If Antonio had to summarise the production case on one slide, it would be this list:

| Production concern | What AWS gives you |
|---|---|
| **Data sovereignty** | Full control of the environment and where Claude is used. |
| **Centralized billing** | A single AWS bill, with Claude usage consolidated alongside everything else. |
| **Observability** | Through **CloudWatch** and **CloudTrail**, you see metrics, logs, and traces of what happened. ("Observability" means being able to see inside a running system to understand its behaviour.) |
| **SLAs** | **Service Level Agreements**: guaranteed availability, so you have dependable uptime for production. |
| **Built in auth integration** | Plug in single sign on, OAuth, or **IAM roles** with identity providers like **Microsoft Entra ID** or **Okta**. (Auth is short for authentication and authorization, proving who a user is and what they may do.) |
| **PrivateLink** | Keep all communication private, so "no data is being sent to the public internet at any point." |

> 🔑 **Key idea: production is not about the model, it is about the surroundings.** Billing, observability, SLAs, identity, and private networking are what separate a prototype from a system you can trust in production. Bedrock provides those.

### The three ways to use Claude on AWS

Antonio stresses this is "the most options that you are going to find in the whole industry right now."

| Way | What it is | Best when |
|---|---|---|
| **1. Claude models directly through Bedrock** | Call Claude through Bedrock's APIs. Same high quality output, fully through AWS. Opus 4.7 is available, and you can use the **messages API** if you prefer that method. | You are building programmatically and want Claude fully inside AWS. |
| **2. Claude platform on AWS** | The same experience you get directly from Anthropic, but with consolidated AWS billing and access control. AWS "acts as a gateway" and forwards inference requests to Anthropic. Generally available "since a few days ago." Gives you "the best of both worlds": AWS security and billing plus **feature parity** with Anthropic (web search, files, agents, and the latest features). | You want Anthropic's full feature set and latest features, but billed and access controlled through AWS. |
| **3. Claude Desktop / CodeWhisperer pointed at AWS** | Not programmatic. Use Claude Desktop or Claude Code through the desktop app, paid via a consolidated AWS bill. Two options: **Claude Enterprise in AWS Marketplace** (subscribe per developer), or the **CodeWhisperer third party connector** to point Claude Desktop at Bedrock or at the Claude platform on AWS. | You work in the app, not in code, and want AWS consolidated billing. |

> 💡 **Feature parity** means "all the same features." The Claude platform on AWS deliberately keeps pace with Anthropic's own platform, so choosing AWS does not cost you the newest capabilities.

> 🎯 **How to choose.** Building in code and want everything inside AWS? Bedrock. Want Anthropic's full feature set with AWS billing? Claude platform on AWS. Working in the desktop app? Point Claude Desktop at AWS. Antonio's whole point: "all sort of combinations to make your life easier, and pretty much meet you where you are."

---

## Part 4: hosting agents securely with Bedrock AgentCore

The newest and most important production tool, in Antonio's words, is for "building with agentic AI." If you build agents with the **Claude Agent SDK** (the official library for building Claude agents) and need somewhere secure to run them in the cloud, AWS offers **Amazon Bedrock AgentCore**.

What makes AgentCore notable:

- It is "fully compatible with any open framework," including **LangChain**, **CrewAI**, and the **Claude Agent SDK**.
- It gives your agents "an infrastructure for hosting your agents in a secure way in the cloud."

```text
Your agent code (Claude Agent SDK, LangChain, CrewAI, ...)
        |
        v
Amazon Bedrock AgentCore   <- secure, managed home for running agents
        |
        v
Claude models on Bedrock + your tools (MCP, knowledge bases, ...)
```

> 🔑 **Key idea: "from code to orchestration" is the arc.** You start by writing code that calls Claude. You end by running fleets of agents in a secure, observable, managed place. AgentCore is the orchestration end of that arc.

---

## Part 5: the hands on workshop, Claude Code on AWS

The talk is hands on. AWS hands out free, no limit workshop accounts so you can test Claude in Bedrock and across AWS at no cost. Two prerequisites: an AWS account (provided) and Claude Code installed.

### The workshop: "Introduction to Claude Code on AWS"

The workshop uses a drawing tool repository (a "Scaled Draw" style app) so you can see Claude Code draw and modify architecture diagrams. It is structured in three modules of increasing depth:

| Module | What you practise |
|---|---|
| **Module 1 (basic)** | Use Claude Code on AWS, set it up, and point it at the sample repository. |
| **Module 2** | Work with **context**, use the **Playwright MCP** server (which lets Claude take browser screenshots) to capture and automatically modify a diagram, and practise **Git** workflows in Claude Code. |
| **Module 3** | Use **sub agents** and **plugins**, and create custom **skills**, **hooks**, and advanced configuration parameters. |

(A **sub agent** is a second Claude working in parallel; a **plugin** is a custom add on; a **skill** is a packaged, reusable procedure; a **hook** is a rule that runs automatically at a certain point, like "before each commit.")

There is also a more advanced workshop for teams moving to production safely: setting team standards, distributing advanced workflows, scalability, and **cost control**, including dashboards to track Claude Code token usage across accounts, plus measuring developer productivity and return on investment. It also covers using the Claude Agent SDK on Bedrock AgentCore.

### Configuring Claude Code to run on Bedrock

You can either ask Claude to configure itself, or set it manually. The settings you point at Bedrock include the region, the default model, and controls for token usage, rate limiting, and telemetry.

```bash
# Point Claude Code at Amazon Bedrock (illustrative settings).
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=eu-west-2                    # London region
export ANTHROPIC_MODEL=claude-opus-4-7         # default model on Bedrock
```

```text
Other useful settings Antonio mentions (set these to taste):
  - reduce token usage / enable rate limiting   -> control cost
  - enable auto-reporting for telemetry         -> feed usage dashboards
  - disable the login prompt at startup         -> remove a minor annoyance
  - hide the onboarding message                 -> cleaner sessions
```

> ✅ **Best practice: let Claude configure itself.** Antonio's recurring tip is "it is all about asking Claude to configure itself." You can set things manually, but the fastest path is to describe what you want and let Claude apply it.

> 💡 You can also point **Claude Desktop** at your Bedrock account and use it for the same workshop, if you prefer the app over the terminal.

---

## Key takeaways

1. **Better together is the thesis.** Frontier Claude models plus AWS infrastructure (Project Rainier, Trainium chips) give you speed and cost efficiency at scale.
2. **Three angles make the case:** a full feature platform (Bedrock), strong security and data control (private boundary, zero operator access, region choice), and near infinite scalability.
3. **Three ways to use Claude on AWS:** Bedrock directly, the Claude platform on AWS (Anthropic feature parity with AWS billing), and Claude Desktop / CodeWhisperer pointed at AWS.
4. **Production is about the surroundings:** consolidated billing, observability (CloudWatch, CloudTrail), SLAs, built in auth, and PrivateLink turn a prototype into a trustworthy system.
5. **Agents get a secure home in Bedrock AgentCore,** compatible with the Claude Agent SDK, LangChain, and CrewAI. This is the "orchestration" end of the journey.
6. **Configure Claude Code for Bedrock** with region, default model, and cost controls, and let Claude configure itself when you can.

## Common pitfalls

- ❌ Treating "it works on my laptop" as production ready, ignoring billing, observability, SLAs, and private networking.
- ❌ Letting data hop to the public internet when PrivateLink could keep it inside your boundary.
- ❌ Ignoring region choice when it is actually a compliance control (GDPR, data residency).
- ❌ Picking the wrong "way" to use Claude: building in code but using the desktop app, or vice versa.
- ❌ Running agents on ad hoc infrastructure instead of a secure, managed home like AgentCore.
- ❌ Skipping cost controls (token limits, rate limiting, usage dashboards) until the bill surprises you.

---

## 🛠️ Capstone Project: prototype to production on AWS

> This is the main hands on project for the lesson, and the best way to make everything above stick. You will take a small Claude powered app from a laptop prototype to a production ready deployment on AWS, deciding each production concern Antonio raised. Start with the free workshop account and grow from there.

### What you will build

**ProdReady** is a small Claude app (your choice of domain) that you graduate from prototype to production on AWS. By the end it:

1. Runs Claude through **Bedrock** (or the Claude platform on AWS), not a personal API key.
2. Keeps data **private** in your AWS boundary, in a region you chose on purpose.
3. Is **observable** (you can see metrics, logs, and traces).
4. Has **cost controls** (token limits, rate limiting, a usage dashboard).
5. Includes at least one **agent** running on **Bedrock AgentCore**.

> 🎯 **Pick your world.** Reuse the workshop's **architecture diagram assistant**, or swap in something you find useful: a **support ticket summariser**, a **document Q&A assistant** (a RAG app over your own docs), or a **code review agent**. Any world works as long as it calls Claude and is worth running in production.

### Why this is the perfect practice

| Lesson skill | Where you use it in ProdReady |
|---|---|
| Choosing among the three ways to use Claude | Milestone 1, decide and justify |
| Configuring Claude Code for Bedrock | Milestone 2, region + model + cost settings |
| Region as a compliance control | Milestone 3, pick a region on purpose |
| Observability (CloudWatch / CloudTrail) | Milestone 4, see inside the running app |
| Guardrails and private networking | Milestone 5, security hardening |
| Hosting agents on AgentCore | Milestone 6, the orchestration step |

### Milestones (build them in order, each one works on its own)

1. **Choose your way.** Decide between Bedrock direct, the Claude platform on AWS, or Claude Desktop pointed at AWS, and write one paragraph justifying the choice for your app.
2. **Wire up Claude Code.** Configure Claude Code to run on Bedrock: set the region, default model, token limiting, rate limiting, and telemetry. Confirm a real call goes through Bedrock.
3. **Choose a region on purpose.** Deploy to a specific region (for example London or an EU region) and write down the compliance reason (GDPR, data residency, or none).
4. **Make it observable.** Turn on telemetry and confirm you can see metrics, logs, and traces (CloudWatch / CloudTrail) for your app's Claude usage.
5. **Harden it.** Add at least one **guardrail** (content filter or PII masking) and keep traffic private (PrivateLink or staying within your boundary). Confirm no data leaves to the public internet.
6. **Add and host an agent.** Build a small agent with the Claude Agent SDK and run it on **Bedrock AgentCore**. Give it one tool (an MCP server or a knowledge base).
7. **Control cost.** Stand up a simple **usage dashboard** for Claude token consumption and set a sensible token / rate limit. Note your projected monthly cost.

### How you will know you are done

- ✅ Claude runs through **AWS** (Bedrock or the Claude platform on AWS), not a personal API key.
- ✅ You can name the **region** your app runs in and the **reason** you chose it.
- ✅ You can show **metrics, logs, and traces** for at least one real request.
- ✅ At least one **guardrail** is active, and traffic stays inside your boundary.
- ✅ An **agent** runs on **Bedrock AgentCore** and successfully uses one tool.
- ✅ A **usage dashboard** exists and a token / rate limit is in place.

> 💡 **Keep yourself honest:** for every production concern (data, region, observability, cost, agents) you should be able to point to the exact AWS feature that addresses it. If you cannot, that concern is still a prototype level risk.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self contained tasks for focused practice on a single skill. They are optional and independent. The **Capstone above is the main build** and already covers all of them.

### Exercise 1: choose the right way (foundational)
Write three short user stories ("I am a backend developer...", "I want Anthropic's newest features with AWS billing...", "I just use the desktop app..."). For each, pick which of the three ways to use Claude on AWS fits, and say why.

### Exercise 2: configure Claude Code for Bedrock (foundational)
Set the region, default model, and a token limit for Claude Code on Bedrock. Then ask Claude to configure one of those settings for you instead of editing it by hand. Compare the two approaches.

### Exercise 3: region as compliance (intermediate)
Take a fictional health care app subject to data residency rules. Decide which region to deploy in and write down exactly which rule drives the choice. Then explain what PrivateLink adds on top.

### Exercise 4: read your own traces (intermediate)
Make a few Claude calls, then find them in CloudWatch / CloudTrail. Identify one metric, one log line, and one trace. Explain what each tells you that the others do not.

### Exercise 5: host a tiny agent (advanced)
Build a one tool agent with the Claude Agent SDK and run it on Bedrock AgentCore. Then swap the framework (for example to LangChain) and confirm AgentCore still hosts it. What had to change, and what did not?

---

## Cheat sheet

```text
WHY CLAUDE ON AWS (three angles)
  1. Feature platform  -> eval, prompt opt, fine-tune (Haiku!), distillation,
                          knowledge bases (RAG), guardrails, agent tools
  2. Security          -> private boundary, zero operator access, not used for
                          training, compliance (FedRAMP/HIPAA/GDPR via region)
  3. Scalability       -> near-infinite, choose your regions, go to production

THREE WAYS TO USE CLAUDE ON AWS
  Bedrock directly ............ programmatic, fully inside AWS (messages API)
  Claude platform on AWS ...... Anthropic feature parity + AWS billing/access
  Claude Desktop -> AWS ....... app users; Marketplace or CodeWhisperer 3P

PRODUCTION SURROUNDINGS (the one slide)
  data sovereignty - centralized billing - observability (CloudWatch/CloudTrail)
  SLAs - built-in auth (Entra ID / Okta / IAM) - PrivateLink

CONFIGURE CLAUDE CODE FOR BEDROCK
  CLAUDE_CODE_USE_BEDROCK=1 ; AWS_REGION=... ; ANTHROPIC_MODEL=...
  + token/rate limits, telemetry; or just ask Claude to configure itself.

AGENTS
  Bedrock AgentCore = secure managed home for agents
  (Claude Agent SDK, LangChain, CrewAI) -> "from code to orchestration"
```

## How this connects to the rest of the course

- **This module, Module 7 · Lesson 24 (Google Cloud):** the same "run Claude on your cloud" idea, with Google Cloud's deploy and analytics tooling.
- **This module, Module 7 · Lesson 26 (Microsoft Foundry):** the same idea again, with deployed Claude models and an agent framework on Azure.
- **Earlier, Module 2 (Core skills):** sub agents, plugins, skills, and hooks (used heavily in the AWS workshop) are taught there.
- **Later, Module 5 (Claude Managed Agents):** building and orchestrating agents, which AgentCore gives a production home.

---

*Source: "AI with Claude on AWS: From code to orchestration" by Antonio Rodriguez (Amazon Web Services), Code with Claude 2026, London. Configuration snippets and the AgentCore diagram are illustrative reconstructions of the approaches described in the talk. Adapt model names, service names, and environment variables to the current AWS and Claude Code tooling.*

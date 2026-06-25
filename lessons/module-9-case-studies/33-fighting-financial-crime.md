# Module 9 · Lesson 33: Fighting Financial Crime with Claude Cowork

> **Course:** Building with Claude, a self-paced course
> **Module 9:** In the field, industry case studies
> **Speaker:** Stefano Amorelli, Senior Staff Software Engineer, Qonto (London)
> **Source talk:** [Fighting financial crime with Claude Cowork](https://www.youtube.com/watch?v=tUoO4ucrNc0) · [full transcript](../../transcripts/code-with-claude-2026-london-2026-day-2/08_fighting-financial-crime-with-claude-cowork.txt)
> **Estimated time:** 45 to 60 minutes (read plus exercises)

---

## In one sentence

To put AI to work on sensitive, high-stakes data, you do not just connect the model to your systems, you build a secure, audited **gateway** around that connection (strong sign-in, short-lived tokens, role-based access, a full audit trail, and humans kept in the loop), and you prove it works with **evals**, so that security and compliance say yes instead of no.

> 🎯 **Where this lesson is heading.** It builds to a hands on **Capstone Project** where you build a **Secure MCP Gateway**: a single, audited front door that sits between an AI assistant and your data sources. Everything before the Capstone teaches the pieces you will assemble there. If you want the finish line first, jump to the **Capstone Project** section, then come back.


## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk this lesson is built on is recent, but the underlying concept is not. For the timeless, tool-agnostic version, independent of any single product or model:
>
> - **[Financial Action Task Force (FATF)](https://en.wikipedia.org/wiki/Financial_Action_Task_Force)** (docs). FATF sets the global AML/CFT standard, the durable grounding for the alerting-to-investigation lifecycle and KYC/KYB concepts the lesson references.
> - **[Anti-money laundering](https://en.wikipedia.org/wiki/Anti-money_laundering)** (essay). A concrete primer on transaction monitoring, suspicious-activity reporting, and KYC, the exact workflow the lesson automates.

## A few plain-language basics first

This lesson mixes AI and security terms. Here they are in plain words:

- **LLM (Large Language Model):** the kind of AI that reads and writes text. Claude is an LLM.
- **Context window:** the amount of text a model can "hold in mind" at once. A long context window lets the model reason across a big pile of documents in a single go.
- **MCP (Model Context Protocol):** a shared standard for connecting an AI to a data source or tool. An "MCP server" is a small service that exposes one data source (a database, an API) to the model in this standard way. Think of it as a universal plug.
- **Claude Cowork:** a Claude interface where non-technical people can use AI assistants that are pre-packaged with skills and tools. Here it is the screen the investigators actually use.
- **Plugin:** a bundle of skills plus the tools and MCP servers they need, shipped as one versioned artifact.
- **Skill:** a packaged set of instructions teaching the model how to do one task your way.
- **OAuth / SSO:** standard ways to prove who a user is. **SSO (single sign-on)** lets people log in once with their company account. **OAuth** is the protocol that hands out access on their behalf.
- **Token (security):** a small signed credential that proves a request is allowed. (Not to be confused with the model's text "tokens.") A **short-lived** token expires quickly, so a leaked one is nearly useless.
- **Audit trail:** an append-only record of who did what and when. "Append-only" means entries can be added but never edited or deleted.
- **Role-based access control (RBAC):** giving each person access only to the data their role needs, and nothing more.
- **Eval:** a set of test cases proving the system behaves as expected. Covered more in Module 3.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Qonto is a fintech offering business banking for small and medium companies, with more than 600,000 customers across Europe. In finance, Stefano says, "financial crime is the number one priority," and the numbers are staggering: between two and five trillion US dollars are laundered worldwide every year, and only a tiny fraction is ever detected. This is a use case where AI can have real social impact, but only if it can touch genuinely sensitive data without becoming a security nightmare. The pattern Qonto built (a secure, audited gateway plus evals) is the same pattern you need for any AI feature in healthcare, finance, or any regulated industry. That is why it generalises far beyond fraud.

## Learning objectives

By the end of this lesson you will be able to:

1. Describe the financial crime investigation workflow and explain where **agentic AI** fits (and where it does not).
2. Explain why connecting an LLM to data via MCP raises security concerns, and how a **gateway** answers them.
3. List the five security building blocks Qonto baked in: strong auth, short-lived tokens, role-based access, an audit trail, and human-in-the-loop.
4. Structure a complex plugin using **good prompting hygiene** (an orchestrator skill, sub-skills, and a meta-skill) and prove it works with the three kinds of evals that matter here.

## Prerequisites

- A basic understanding of prompts and tools (Module 2).
- Helpful but optional: Module 3 (Evals) and any earlier MCP material.

---

## Part 1: the workflow, and where AI fits

A financial crime case has a lifecycle. First comes an **alerting system**: a fully automated first line of defense that flags suspicious transactions. When an alert fires, a human investigator picks up the case, prioritises it, and gathers data from many sources, internal dashboards, third-party tools, web searches. Stefano describes investigators "with three different monitors at least, and dozens of browser tabs," manually compiling a big document, holding part of it in their head, then reasoning over it to judge whether a crime occurred. It is slow and, in his word, "a bit of an inhuman process."

There are three phases where AI could help, and the choice of which one to focus on is itself a lesson.

| Phase | What it is | Right tool? |
|---|---|---|
| **General usage** | Spin up Claude, upload documents, ask questions. | Useful but not exciting; not the focus. |
| **First line of defense (alerting)** | Catch suspicious transactions fast. | **Not** generative AI. This needs speed, accuracy, and deterministic rules, so traditional machine learning fits better. |
| **Second line of defense (investigation)** | The slow manual case work after an alert. | This is where **agentic AI** shines, and where few competitors are looking. |

> 🔑 **Key idea: match the tool to the job.** Generative AI is not the answer to everything. The fast, rule-driven alerting step is better served by classic machine learning. The slow, reasoning-heavy investigation step is where an agent earns its keep. Choosing the right phase is half the battle.

For the investigation phase, the model choice was easy. Investigators handle huge amounts of scattered information, so you need a model that can reason across a very long context window. Qonto chose Opus 4.7.

> 💡 **Why Opus 4.7 for this.** Stefano points to the **GraphWalks benchmark**, a test of how well a model can connect facts that are spread far apart across a long document, not just facts sitting next to each other. That is exactly the skill an investigator needs, "where information is scattered around all the context window," and Opus 4.7 leads it.

The entry point for investigators is **Claude Cowork**, because non-technical staff can be onboarded easily, and because it supports rich plugins that bundle multiple skills with the tools and MCP servers they need.

---

## Part 2: the security problem, "the S in MCP stands for security"

A model is only as useful as the data it can reach. To give an LLM data access, the standard answer is **MCP** (Model Context Protocol), a universal way to plug a model into a data source. But the moment you say "MCP" to a security or compliance team, eyebrows go up. There is a running joke that "the S in MCP stands for security," meaning there is no S, meaning it raises real concerns.

The investigation use case makes this acute, because the data is scattered everywhere:

```text
Data sources an investigation must reach:
  - internal knowledge database
  - OSINT (open source intelligence, public web data)
  - internal databases and dashboards
  - KYC / KYB data (Know Your Customer / Know Your Business records)
  - internal API endpoints (to take automated actions)
Each one: a different language, internal or external, multimodal. A mess.
```

> 🔑 **The central takeaway:** you do not avoid MCP, you make it safe. As Stefano puts it, "you can build it security first and compliance first in mind so that you can build a case and address these objections." The way to do that is to create boundaries and "implement a system, a harness, that is compliant and secure."

Qonto turned the abstract worry into five concrete technical requirements:

| Requirement | Plain meaning | Why it matters here |
|---|---|---|
| **Strong authentication** | Be sure who the user is, via OAuth. | No anonymous access to crime data. |
| **Cryptographically safe tokens** | Short-lived credentials that are useless if leaked. | A leaked token should not be a breach. |
| **Role-based access control** | Each person sees only the data their role allows. | Not everyone should see everything. |
| **Audit trail** | An append-only log of who accessed what, when. | Legal and compliance demand it. |
| **Human-in-the-loop** | Keep human judgment on critical decisions. | These actions have legal consequences. |

> ✅ **Best practice: do not fully automate consequential decisions yet.** Investigations have legal consequences, so Qonto deliberately keeps a human making the final call. We will see how this is meant to relax over time at the end of the lesson.

---

## Part 3: the architecture, an MCP gateway

The heart of Qonto's system is the **MCP gateway**: a single, central service that sits between Claude Cowork and all the downstream data sources. Everything flows through it, which is exactly why it can enforce security in one place.

```text
[Investigator in Claude Cowork]
        |
   (Cowork plugin)
        |
        v
   [ MCP GATEWAY ]  <-- authenticate, authorize (RBAC), audit, route
        |
   +----+----+----+----------+
   v         v         v
[MCP srv] [MCP srv] [MCP srv]  ... (one per data source, any language)
   |         |         |
   v         v         v
[downstream APIs / databases]
```

What the gateway does, all in one place:

1. **Authenticate the user.** It connects to SSO (single sign-on) and an identity provider. If you are not logged in, you get a login page. The identity provider tells the gateway who you are.
2. **Authorize the request (RBAC).** Based on your identity, it decides which MCP servers you may use. Investigators literally cannot *see* servers they are not allowed to use.
3. **Audit everything.** Every call and every authorization decision is written to an append-only database.
4. **Route to downstream MCP servers.** Each data source has its own MCP server, deployed internally on a Kubernetes cluster so it can only be reached *through* the gateway, never directly. Because MCP is a standard, those servers can be written in Go, Python, TypeScript (Stefano jokes, "COBOL, maybe not"). Add a new data source and you get audit logging, identity, and RBAC for free.

A neat detail on tokens. The gateway does not pass your SSO login token downstream. Instead it **mints** (creates and signs) a fresh, short-lived token for the downstream servers:

```python
# Authorization gateway (illustrative)
sso_token = get_token_from_sso(request)            # who you are, from single sign-on
identity  = verify_and_resolve(sso_token)          # confirm authenticity, get permissions

# Mint a short-lived PASETO token to share downstream (NOT the SSO token).
bearer = mint_paseto(
    subject=identity.user_id,
    permissions=identity.permissions,
    ttl_seconds=300,                               # expires fast; a leak is near-useless
)
```

> 💡 **What is a PASETO token?** PASETO (Platform-Agnostic Security Tokens) is a relatively modern token format. Its payload is base64-encoded (readable, not secret) but *signed*, so a downstream server can verify the contents were not tampered with. Qonto uses it for short-lived downstream credentials.

Role-based access control is itself defined as code, in a **Terraform** file (Terraform is a tool that describes infrastructure and permissions in text files) checked into a GitHub repo. That means the rules are versioned and auditable: you can see the full history of who was granted access to what.

The audit trail lands in **ClickHouse** (a database built for fast analysis of large logs), visualised in a **Grafana** dashboard (a tool for live monitoring charts). On it, the team can see every tool call, every authorization flow, which user accessed which tool, how many calls, and how long each took. Calls are instrumented with **OTEL** (OpenTelemetry, a standard for emitting traces and metrics) plus a few custom fields.

---

## Part 4: the plugin, prompting hygiene, and evals

With the secure plumbing in place, Qonto built the investigator-facing plugin by sitting with real investigators and doing three investigations together as engineers, then encoding that domain knowledge. Because it is one versioned artifact, it can be shipped centrally and even updated by the investigators themselves.

The way the plugin is *structured* is a lesson in itself.

> 🔑 **Good prompting hygiene.** Instead of "one huge prompt of 1,000 lines," split the work across smaller pieces:
> - A **main skill** acts as the **orchestrator**: it decides which sub-skill to call for each step the investigator wants.
> - Several **sub-skills** each handle one operation.
> - A **meta-skill** always runs at the end to verify the results of the whole call.

```text
ORCHESTRATOR (main skill)
  ├── sub-skill: gather KYC/KYB data
  ├── sub-skill: search OSINT
  ├── sub-skill: pull transaction history
  └── ...
META-SKILL (always runs last): verify the findings are grounded and consistent
```

Inside each skill, Qonto uses **XML-structured prompts** (sections marked with tags like `<role>` and `<task>`), which they find more efficient than plain prose, and each skill names exactly which MCP servers and tools it uses, so the model does not waste effort discovering them.

A nice touch in Cowork: instead of slow generated artifacts, the assistant renders **inline interactive widgets** on the fly, dashboards with charts, dropdowns, and action buttons the investigator can use directly. The result replaces dozens of browser tabs with a single interface.

### Proving it works: three kinds of evals

Once the plugin existed, stakeholders asked the obvious question: *can we trust it?* The honest answer is **evals**, test cases that bring "quantitative facts" to the table. Stefano highlights three things worth evaluating here:

| What to evaluate | What it checks | How |
|---|---|---|
| **Tool choice and order** | Did the plugin call the right tools, in the right sequence? | Programmatic checks against expected tool calls. |
| **Grounding (no hallucinations)** | Is everything on the dashboard backed by a real reference document? | Compare outputs to source data. |
| **Reasoning quality** | Even when the *conclusion* is right, is the *reasoning behind it* sound? | An **LLM-as-a-judge**: a second model grades the reasoning. |

> 💡 **Why evals make three different groups happy.** For *engineering*, you can swap models or change the plugin and immediately catch regressions. For *compliance*, you can prove the accuracy meets requirements, so "they can sleep at night." For *end users*, you give them reason to trust a new tool instead of second-guessing it every time.

> 🔑 **Evals are like TDD.** Stefano compares evals to **test-driven development** (writing tests before code). "If you're building critical workflows, you most likely will need evals at some point, so why not start with it?"

---

## Part 5: the flywheel, and the road to less human

The gateway was not just for fraud. Once it existed, other Qonto teams began building their own plugins on the same MCP gateway and servers. Because the hard, secure foundation already existed, new use cases that once "took a few weeks to build" now arrive "in a matter of a few days." Every new team gets audit trails, RBAC, strong auth, and identity management out of the box.

> 🔑 **The flywheel.** A secure gateway turns AI adoption from a series of risky one-off projects into a repeatable pattern. Security and compliance become enablers, not blockers, especially in a large enterprise.

Finally, the human-in-the-loop is a stage, not the destination. Stefano lays out a path:

```text
human IN the loop   -> human makes the critical decisions (today)
human ON the loop   -> AI decides, human reviews        (the near goal)
human OUT of the loop -> AI decides autonomously         (long-term, IF proven)
```

The lever that moves you along this path is, again, evals: only by continuously measuring accuracy can you justify giving the AI more autonomy.

---

## Key takeaways

1. **Match the tool to the phase.** Fast rule-driven detection wants classic ML; slow reasoning-heavy investigation wants an agent. Generative AI is not the answer to everything.
2. **Do not avoid MCP, make it safe.** A central gateway lets you enforce security and compliance in one place.
3. **Five building blocks:** strong auth (OAuth/SSO), short-lived signed tokens (PASETO), role-based access control, an append-only audit trail, and human-in-the-loop.
4. **Define access as code.** RBAC in a versioned Terraform file means every permission change is auditable.
5. **Practice prompting hygiene.** An orchestrator skill plus focused sub-skills plus a verifying meta-skill beats one giant prompt.
6. **Evals build trust three ways:** they let engineers iterate, let compliance sleep, and let users trust the tool. Start with them, like TDD.
7. **A secure gateway is a flywheel.** It turns each new AI use case from weeks into days.

## Common pitfalls

- ❌ Reaching for generative AI on a step that really wants fast deterministic rules.
- ❌ Wiring a model straight to your data sources with no central control over auth, access, or logging.
- ❌ Passing a long-lived login token downstream instead of minting a short-lived one.
- ❌ Letting people reach data sources they have no role-based reason to see.
- ❌ Cramming everything into one 1,000-line prompt instead of an orchestrator with sub-skills.
- ❌ Shipping a "trust me" system to compliance with no evals to back it up.
- ❌ Jumping straight to full automation before evals justify it.

---

## 🛠️ Capstone Project: build a Secure MCP Gateway

> This is the main hands on project for the lesson. You will build a small **Secure MCP Gateway**: one audited front door that sits between an AI assistant and two or more data sources, enforcing identity, access control, and logging in one place. Start tiny and grow it.

### What you will build

A gateway service plus two downstream MCP servers, fronted by a simple assistant. A user logs in once; the gateway checks who they are, decides which servers they may use, mints a short-lived token, routes the call, and writes an audit entry for everything. You will then add a small orchestrator plugin and an eval suite to prove it behaves.

> 🎯 **Pick your world.** You do not need real crime data. Use any domain with sensitive-ish data and at least two roles: an HR assistant (one server for public policies, one for salaries; roles "employee" and "manager"), a support assistant (knowledge base vs. customer PII), or a school assistant (public timetable vs. grades).

### Why this is the perfect practice

| Lesson idea | Where you use it in the gateway |
|---|---|
| Match tool to job | Milestone 1, you decide which step is reasoning vs. rules |
| Central gateway | Milestone 2, all calls flow through one service |
| Strong auth + short-lived tokens | Milestone 3, login then mint a fresh token |
| Role-based access control | Milestone 4, two roles see two different sets of servers |
| Audit trail | Milestone 5, every call is logged append-only |
| Prompting hygiene | Milestone 6, an orchestrator with sub-skills |
| Evals build trust | Milestone 7, test tool choice and grounding |

### Milestones (build them in order, each one works on its own)

1. **Map your data and roles.** List two or three data sources and two roles. Mark which source each role may reach. Note one step that is reasoning-heavy (good for an agent) and one that is just a rule.
2. **Stand up two MCP servers.** Build two tiny servers, each exposing one data source with one or two tools. They can be in different languages if you want to feel the "language-agnostic" benefit.
3. **Add the gateway with auth.** Put a gateway in front. On each request, verify the user's identity (a stubbed login is fine to start) and mint a short-lived token to pass downstream. Never forward the login credential itself.
4. **Enforce role-based access.** Define, in a versioned config file (mimicking the Terraform approach), which role may use which server. Confirm a user literally cannot reach a server outside their role.
5. **Add the audit trail.** Write every authorization decision and tool call to an append-only log: user, tool, time, outcome. Build a tiny dashboard or query to view it.
6. **Build an orchestrator plugin.** Write a main skill that routes the user's request to the right sub-skill, plus a meta-skill that verifies the result at the end. Use XML-structured prompts and name each skill's tools.
7. **Write evals.** Create test cases for: correct tool choice and order, grounding (every claim traces to a source), and one LLM-as-a-judge check on reasoning quality. Run them; fix what fails.
8. **Stretch goals.** Render an interactive widget instead of plain text. Add a human-in-the-loop approval step for a "consequential" action. Add a second team's plugin reusing the same gateway, proving the flywheel.

### How you will know you are done

- ✅ A user in one role can reach their allowed data and is *blocked* from the rest, provably.
- ✅ No long-lived credential ever reaches a downstream server; only short-lived minted tokens do.
- ✅ Every call appears in an append-only audit log you can query.
- ✅ Your orchestrator routes correctly and the meta-skill catches at least one bad result.
- ✅ Your evals pass for tool choice and grounding, and you can show the numbers to a sceptical "compliance" friend.

> 💡 **Keep yourself honest:** if a request can reach a data source *without* going through the gateway, you have not built a gateway, you have built a suggestion.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each focused on one idea. They are optional and independent. The Capstone above already covers all of them.

### Exercise 1: phase the workflow (foundational)
Take a process you know. Split it into the fast/rule-driven parts and the slow/reasoning parts. For each, say which kind of AI (or none) fits, and why.

### Exercise 2: the token swap (foundational)
Draw the flow where a login token is exchanged for a short-lived downstream token. Explain in one sentence why leaking the short-lived one is far less dangerous than leaking the login one.

### Exercise 3: write the RBAC config (intermediate)
For three users in two roles and three data sources, write the access rules as a small config file. Then write one test that proves a user is blocked from a forbidden source.

### Exercise 4: split the giant prompt (intermediate)
Take a long, do-everything prompt and refactor it into an orchestrator plus two sub-skills plus a verifying meta-skill. Note what got clearer.

### Exercise 5: three evals (advanced)
For one agent task, write one eval for tool choice, one for grounding (claims trace to sources), and one LLM-as-a-judge eval for reasoning quality. Run them and record what each one caught.

---

## Cheat sheet

```text
PUTTING AI ON SENSITIVE DATA
  1. Match the tool to the phase (rules vs. reasoning).
  2. Don't avoid MCP. Put a GATEWAY in front of it.

THE GATEWAY'S FIVE JOBS (all in one place)
  Authenticate ..... OAuth / SSO, know who the user is
  Mint tokens ...... short-lived, signed (PASETO); never forward the login token
  Authorize ........ role-based access control, defined as versioned code
  Audit ............ append-only log of who/what/when
  Human-in-loop .... keep judgment on consequential actions

STRUCTURE THE PLUGIN
  orchestrator skill -> sub-skills -> meta-skill that verifies at the end

PROVE IT
  Evals = trust. Test tool choice, grounding, and reasoning (LLM-as-judge).
  Evals are like TDD: start with them.
  human IN -> ON -> OUT of the loop, earned by evals.
```

## How this connects to the rest of the course

- **Earlier, Module 9 · Lesson 32 (Man Group):** another finance case focused on governing skills; this lesson adds the secure harness around them.
- **Earlier, Module 3 (Evals):** the eval techniques used here (including LLM-as-a-judge) are taught in depth there.
- **Next, Module 9 · Lessons 34 and 35 (Legal agents):** more high-stakes domains where citations, grounding, and human review are non-negotiable.
- **Later, modules on agents and tools:** the orchestrator-and-sub-skills pattern recurs whenever one big prompt is doing too much.

---

*Source: "Fighting financial crime with Claude Cowork" by Stefano Amorelli (Qonto), Code with Claude 2026, London. Code snippets are illustrative reconstructions of the architecture described in the talk; the speaker showed diagrams and partial code rather than full listings, and customer data was masked.*

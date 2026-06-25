# Building with Claude — A Self-Paced Course

*Built from the 37 talks at Code with Claude 2026 (London), re-sequenced as a
**learning path** rather than by conference day. Work top to bottom: each module
builds on the previous one, and lessons inside a module go from foundational to
advanced. By the end you should be able to prompt well, evaluate quality, build
and ship production agents, deploy them on your cloud, and lead the rollout
across a team.*

**How to use this:** each lesson links to the talk transcript. "Skill gained"
is the concrete thing a learner should be able to do afterward. 🎙️ = transcript
came from audio (minor name garbling possible).

Total: 9 modules · 37 lessons, plus an optional **Module 0 (pre-flight)** on-ramp.

---

## Module 0 — Pre-flight: getting ready *(optional, before Lesson 1)*
*Objective: close the small gap this course assumes — set up the toolchain and accounts, and skim a few refreshers — so you build from Lesson 1 instead of fighting setup.*

0. **Pre-flight, getting ready to build** — self-guided setup (no talk)
   [lesson](lessons/module-0-preflight/00-pre-flight.md)
   *Skill gained:* a verified toolchain (Python, git, the `anthropic` SDK, Claude Code), an API key stored safely, your first API call and first Claude Code session, and a map of the official free resources for any gap. Skip if you are already a working engineer.

---

## Module 1 — Foundations: why this matters & where the capability is going
*Objective: get the big-picture mental model before touching tools — what Claude can do today, how fast it's improving, and how to build for where it's heading.*

1. **Opening Keynote** — Boris Cherny & team, Anthropic
   [transcript](transcripts/code-with-claude-2026-london-2026/01_code-with-claude-london-2026-opening-keynote.txt)
   *Skill gained:* a map of the whole stack (model layer, Claude platform, Claude Code) and the launches you'll go deep on later.
2. 🎙️ **The Capability Curve** — Jeremy, Anthropic
   [transcript](transcripts/code-with-claude-2026-london-2026/06_the-capability-curve.txt)
   *Skill gained:* understand how coding ability leapt (SWE-bench ~60%→87%) and why you should build for the next model, not the current one.

---

## Module 2 — Core skills: working with the model
*Objective: the everyday fundamentals — write good prompts, choose the right model, control reasoning effort, and use platform features to stay cheap and fast.*

3. **The Prompting Playbook** — Margo van Laar, Anthropic
   [transcript](transcripts/code-with-claude-2026-london-2026/05_the-prompting-playbook.txt)
   *Skill gained:* debug and structure prompts (XML tags, output contracts, give tools not mental math, state both sides of trade-offs).
4. **Picking the right model** — Lucas, Anthropic
   [transcript](transcripts/code-with-claude-2026-london-2026/10_picking-the-right-model.txt)
   *Skill gained:* choose by "cost per successful outcome" using a small private eval; use the quality/latency/cost framing.
5. **The thinking lever** — Alexander Briken, Anthropic
   [transcript](transcripts/code-with-claude-2026-london-2026/15_the-thinking-lever.txt)
   *Skill gained:* tune test-time compute / "effort" and know when adaptive thinking helps vs. wastes tokens.
6. 🎙️ **Getting more out of the Claude Platform** — Puneet Shah, Anthropic
   [transcript](transcripts/code-with-claude-2026-london-2026/04_getting-more-out-of-the-claude-platform.txt)
   *Skill gained:* cut cost ~10x with prompt caching, context engineering (tool search, programmatic tool calling, compaction), and the advisor strategy.

---

## Module 3 — Measuring quality: evals
*Objective: the discipline that underpins everything that follows — turn "vibes" into measurable progress so you can safely change prompts, models, and agents.*

7. 🎙️ **Evals for taste: hill-climbing a slide-generation agent** — Anthropic
   [transcript](transcripts/code-with-claude-2026-london-2026-day-2/04_evals-for-taste-hill-climbing-a-slide-generation-agent.txt)
   *Skill gained:* build your own evals — code-based, LLM-as-judge, and human graders — and iterate an agent against them (ask for reasons before scores).

> Reinforces: Module 2 Lesson 4 ("Picking the right model") is also an evals lesson — revisit it here with an eval mindset.

---

## Module 4 — Claude Code: your everyday agent (basics → autonomy)
*Objective: master the CLI/desktop tool most people use daily, from the current feature set to running it customized, scheduled, and unsupervised.*

8. 🎙️ **What's new in Claude Code** — Ralf, Anthropic
   [transcript](transcripts/code-with-claude-2026-london-2026/24_whats-new-in-claude-code.txt)
   *Skill gained:* orient to current features — remote control, full-screen TUI, auto mode, worktrees, auto memory, code review, routines, agent view.
9. **How we Claude Code** — Arno, Anthropic
   [transcript](transcripts/code-with-claude-2026-london-2026-day-2/06_how-we-claude-code.txt)
   *Skill gained:* a real working method — let Claude interview you for the spec, use HTML over Markdown specs, and build verification into artifacts.
10. 🎙️ **Beyond the basics with Claude Code** — Daisy Holman, Anthropic
    [transcript](transcripts/code-with-claude-2026-london-2026/02_beyond-the-basics-with-claude-code.txt)
    *Skill gained:* customize the harness via context-window economics; pick the right primitive (MCP vs. skills vs. hooks vs. subagents) at scale.
11. **Build a proactive agent workflow with Claude Code** — Maya, Anthropic
    [transcript](transcripts/code-with-claude-2026-london-2026/19_build-a-proactive-agent-workflow-with-claude-code.txt)
    *Skill gained:* set up "routines" — scheduled and event-triggered Claude Code sessions on managed infrastructure.
12. 🎙️ **Stop babysitting your agents** — Siddh Bhundasarya, Anthropic
    [transcript](transcripts/code-with-claude-2026-london-2026/23_stop-babysitting-your-agents.txt)
    *Skill gained:* the "301" stack — verification loops, multi-clauding, and background loops so agents run without supervision.

---

## Module 5 — Building agents: Claude Managed Agents (intro → production)
*Objective: the flagship platform for production agents — go from "ship your first" to a multi-agent app with memory, all the way through a hands-on practice round.*

13. **How to get to production faster with Claude Managed Agents** — Anthropic + partner panel
    [transcript](transcripts/code-with-claude-2026-london-2026/13_how-to-get-to-production-faster-with-claude-managed-agents.txt)
    *Skill gained:* the why and the primitives (agent, environment, session, events) + self-hosted sandboxes and MCP tunnels.
14. **Ship your first Managed Agent** — Isabella He, Anthropic
    [transcript](transcripts/code-with-claude-2026-london-2026-day-2/01_ship-your-first-managed-agent.txt)
    *Skill gained:* build a first agent and understand why the loop (brain) is decoupled from tool execution (hands).
15. **Build a production-ready agent with Claude Managed Agents** — Anthropic
    [transcript](transcripts/code-with-claude-2026-london-2026/14_build-a-production-ready-agent-with-claude-managed-agents.txt)
    *Skill gained:* hands-on multi-agent "Deal Desk" app — sessions API, orchestration, outcomes/rubrics, credential vaults, memory.
16. **Tool, skill, or subagent? Decomposing an agent that outgrew its prompt** — Will, Anthropic
    [transcript](transcripts/code-with-claude-2026-london-2026-day-2/02_tool-skill-or-subagent-decomposing-an-agent-that-outgrew-its-prompt.txt)
    *Skill gained:* decide when to reach for a tool vs. skill vs. subagent; shrink a 400-line prompt to ~15-50 lines and climb evals.
17. **Agents that remember** — Kevin, Anthropic
    [transcript](transcripts/code-with-claude-2026-london-2026-day-2/05_agents-that-remember.txt)
    *Skill gained:* use memory stores (file-system, read/write via bash/grep) and "dreaming" to persist and self-improve across sessions.
18. **Memory and dreaming for self-learning agents** — Ravi, Anthropic
    [transcript](transcripts/code-with-claude-2026-london-2026/11_memory-and-dreaming-for-self-learning-agents.txt)
    *Skill gained:* multi-agent memory architecture (org/granular stores, concurrency, audit) and out-of-band "dreaming" curation.
19. **Agent Battle: mine the most diamonds in 45 minutes** — Ben & Jeff, Anthropic
    [transcript](transcripts/code-with-claude-2026-london-2026-day-2/03_agent-battle-mine-the-most-diamonds-in-45-minutes.txt)
    *Skill gained:* capstone practice — configure and hill-climb a managed agent under time pressure, scored on token efficiency.

---

## Module 6 — Advanced agent engineering: trust, harness design & self-improvement
*Objective: patterns that separate a demo from a durable product — verifiable processes, friction-driven harness design, and agents that learn from your team.*

20. **Making agentic workflows trustworthy and verifiable with a custom DSL** — James Brady, Elicit
    [transcript](transcripts/code-with-claude-2026-london-2026-day-2/07_making-agentic-workflows-trustworthy-and-verifiable-with-a-custom-dsl.txt)
    *Skill gained:* make an agent's process legible/faithful/verifiable (a typed, Turing-incomplete DSL + event sourcing + memoization).
21. 🎙️ **How AirOps chases friction to build AI products** — Dylan, AirOps
    [transcript](transcripts/code-with-claude-2026-london-2026-day-2/10_how-airops-chases-friction-to-build-ai-products-with-claude.txt)
    *Skill gained:* harness engineering for non-technical users — specialized deterministic tools, sub-agents, enforced human review.
22. 🎙️ **How Metaview built self-improving prompts for application review** — Nick Mayhew, Metaview
    [transcript](transcripts/code-with-claude-2026-london-2026-day-2/11_how-metaview-built-self-improving-prompts-for-application-review.txt)
    *Skill gained:* design a prompt that evolves from user decisions; prose over rules; put guardrails in the architecture.
23. **Teaching agents to learn from your team** — Petra, Warp
    [transcript](transcripts/code-with-claude-2026-london-2026-day-2/12_teaching-agents-to-learn-from-your-team.txt)
    *Skill gained:* design a low-friction team feedback loop (Slack reactions → self-editing PRs); rules → principles → learn-to-learn.

---

## Module 7 — Deploying on your cloud
*Objective: run Claude where your infrastructure already lives — pick the path for your provider and ship with enterprise security and governance.*

24. 🎙️ **Building with Claude on Google Cloud** — Iman Nardini, Google Cloud
    [transcript](transcripts/code-with-claude-2026-london-2026/08_building-with-claude-on-google-cloud.txt)
    *Skill gained:* run Claude Code on Vertex; build/secure/deploy an app with sub-agents, CI/CD, and Google Cloud Skills/MCP.
25. **AI with Claude on AWS: from code to orchestration** — Antonio Rodriguez, AWS
    [transcript](transcripts/code-with-claude-2026-london-2026/22_ai-with-claude-on-aws-from-code-to-orchestration.txt)
    *Skill gained:* the three ways to run Claude on AWS (Bedrock models, Claude platform on AWS, Desktop/Code) + Bedrock ecosystem features.
26. **Build AI agents using Claude in Microsoft Foundry** — Marlene Mungai, Microsoft
    [transcript](transcripts/code-with-claude-2026-london-2026/20_build-ai-agents-using-claude-in-microsoft-foundry.txt)
    *Skill gained:* deploy Claude in Foundry and build an MCP-connected agent with Defender/Purview/Entra ID governance.

---

## Module 8 — Leading the AI-native transformation
*Objective: for leads and founders — rewire team norms, processes, and developer experience once coding is no longer the bottleneck.*

27. **Running an AI-native engineering org** — Fiona Fung, Anthropic
    [transcript](transcripts/code-with-claude-2026-london-2026/03_running-an-ai-native-engineering-org.txt)
    *Skill gained:* rewrite norms (PRs over design docs, "code wins," where humans stay in the loop) and roll out top-down + bottoms-up.
28. 🎙️ **Designing with Claude: from prompt to production** — Dan Carey, Anthropic Labs
    [transcript](transcripts/code-with-claude-2026-london-2026/07_designing-with-claude-from-prompt-to-production.txt)
    *Skill gained:* a lean, prototype-first process (skip the PRD, tiny teams, optimize every loop step) that shipped a product in ~10 weeks.
29. 🎙️ **From one person to 80: scaling a hypergrowth engineering org** — Base44
    [transcript](transcripts/code-with-claude-2026-london-2026/18_from-one-person-to-80-scaling-a-hypergrowth-engineering-org-with-claud.txt)
    *Skill gained:* keep velocity while scaling — onboarding via prompts, production-traffic evals, user-simulator QA; "keep it simple."
30. 🎙️ **Coding is no longer the constraint: scaling devex at Spotify** — Spotify
    [transcript](transcripts/code-with-claude-2026-london-2026/21_coding-is-no-longer-the-constraint-scaling-devex-to-teams-and-agents-a.txt)
    *Skill gained:* scale dev experience for thousands of engineers — fleet migrations, codebase standardization, review as the new bottleneck.
31. 🎙️ **Building AI-native at enterprise scale: monday.com, Doctolib, Delivery Hero** — panel
    [transcript](transcripts/code-with-claude-2026-london-2026/17_building-ai-native-at-enterprise-scale-mondaycom-doctolib-and-delivery.txt)
    *Skill gained:* retrofit Claude into legacy codebases — autonomous delivery agents, skills marketplaces, surviving model migrations.

---

## Module 9 — In the field: industry case studies
*Objective: see the whole course applied end-to-end in real domains; choose the ones closest to your industry for concrete blueprints.*

32. **Building signals that trade themselves** — Tashara Fernando, Man Group *(finance)*
    [transcript](transcripts/code-with-claude-2026-london-2026/09_building-signals-that-trade-themselves.txt)
    *Skill gained:* govern skills at scale (a tested, owned, versioned internal marketplace) so AI can drive a regulated research pipeline.
33. 🎙️ **Fighting financial crime with Claude Cowork** — Qonto *(fintech / compliance)*
    [transcript](transcripts/code-with-claude-2026-london-2026-day-2/08_fighting-financial-crime-with-claude-cowork.txt)
    *Skill gained:* build a security/compliance-first agentic system behind an MCP gateway (OAuth/RBAC/audit) for non-technical investigators.
34. 🎙️ **What legal agents inherit from coding agents: Lessons from Legora** — Legora *(legal)*
    [transcript](transcripts/code-with-claude-2026-london-2026/12_what-legal-agents-inherit-from-coding-agents-lessons-from-legora.txt)
    *Skill gained:* port coding-agent patterns to a new vertical with the Reuse / Translate / Invent framework.
35. 🎙️ **Where code meets court: AI at the legal-technical frontier** — Solve Intelligence *(patent law)*
    [transcript](transcripts/code-with-claude-2026-london-2026-day-2/09_where-code-meets-court-ai-at-the-legal-technical-frontier.txt)
    *Skill gained:* design a "collaboration" (not delegation) model with first-class citations for high-stakes, hard-to-validate work.
36. 🎙️ **How Lovable vibecodes production software at scale** — Lovable *(dev tools)*
    [transcript](transcripts/code-with-claude-2026-london-2026/16_how-lovable-vibecodes-production-software-at-scale.txt)
    *Skill gained:* detect when users are "stuck" and self-heal at scale (a retrieval corpus + an agent "vent" tool that opens fix PRs).
37. 🎙️ **Building the best agentic analytics harness: Powered by Claude, built with Claude Code** — Omni *(analytics)*
    [transcript](transcripts/code-with-claude-2026-london-2026-day-2/13_building-the-best-agentic-analytics-harness-powered-by-claude-built-wi.txt)
    *Skill gained:* build an analytics agent on a semantic layer; error recovery and "consolidating the brain" as quality levers.

---

### Suggested tracks (if you don't take all 9 modules)
- **Individual developer:** Modules 1 → 2 → 3 → 4 (then dip into 5).
- **Agent builder / AI engineer:** Modules 1 → 2 → 3 → 5 → 6 (then 7 for your cloud).
- **Engineering leader / founder:** Modules 1 → 8 → 9 (skim 3 and 5 for vocabulary).
- **Platform / DevEx team:** Modules 2 → 3 → 4 → 7 → 8.

*Not included: two Day-2 talks were removed from YouTube and could not be transcribed.*

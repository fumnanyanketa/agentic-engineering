# Agentic Engineering, a model-agnostic self-paced course

*One path from zero to a working platform of cooperating AI agents. Each unit states a durable
principle, shows how to apply it with your chosen coding agent (Claude Code, Gemini CLI, or
Codex CLI) or model platform (Claude, Gemini, GPT), and ends by building one component of a
north-star project, AtlasOS. Work top to bottom: each unit builds on the last, and on the
AtlasOS component you built before it.*

**How to use this.** Start at Unit 0 and go in order. Every unit is split into short pages (one
per part) so you can feel the progress. Pick one model or coding agent as your main tool; you
will still learn how the others do the same thing, so you are never locked in. The hands-on
**Build** at the end of each unit is the point: by Unit 11 you have built AtlasOS, not finished
a dozen disconnected exercises. From Unit 2 on, every Build ends by running its new component
through the Warden verification rubric: read it, explain it, break it on purpose, fix it.

**The course is 12 units.** Commands and model ids change quickly; verify against current docs.

The published course lives in [`combined/`](combined/index.html).

---

## Unit 0 - Foundations and the Mental Model
Engineer the environment, not the model. How an LLM works exactly enough (tokens, prediction,
context, sampling), the same picture across Claude, Gemini, and GPT, and where capability is
going. **Build:** your first measured model call (streamed, token-counted, structured output)
plus the AtlasOS charter. *AtlasOS: the launchpad.*

## Unit 1 - The Coding-Agent Workflow
Set up a real workstation, then drive a coding agent through a plan, act, verify loop. The same
workflow in Claude Code, Gemini CLI, and Codex CLI. **Build:** your AtlasOS repository, a project
memory file, a safe autonomy level, and a first reviewed task. *AtlasOS: the foundation.*

## Unit 2 - Reading and Judging Code
The floor under everything: read any code the agent writes, trace control and data flow, debug by
hypothesis, read a diff, and spot subtle or unsafe code (including the lethal trifecta). The one
rule: don't merge what you can't read, explain out loud, and break on purpose. **Build:** the
Warden verification rubric plus your first read, explain, break, fix pass. *AtlasOS: the floor.*

## Unit 3 - Prompting and Context Engineering
What makes a prompt work, structure and output contracts, the same moves across providers, and
context engineering (budgeting, context rot, prompt caching). **Build:** the `prompts/` library,
starting with Scout's first versioned system prompt. *AtlasOS: prompts.*

## Unit 4 - Model and Reasoning Levers
Choosing a model tier (capability vs cost vs latency), cost per successful outcome, the reasoning
lever across providers, the advisor strategy, plus when not to use an LLM at all and when
fine-tuning is the answer. **Build:** the `orchestrator/` model-routing policy. *AtlasOS: routing.*

## Unit 5 - Tools, Function-Calling and MCP
How a model calls your code (JSON-schema tools) across Claude, Gemini, and GPT, designing tools
the model uses reliably, and MCP as one standard across all three coding agents. **Build:** the
`tools/` layer plus a connected MCP server. *AtlasOS: tools.*

## Unit 6 - Retrieval, Memory and State
Retrieval and RAG (embeddings and vector search explained plainly, with a little math intuition),
measuring a retriever, short vs long-term memory, memory across runs, and the dreaming
self-improvement loop. **Build:** Cortex, the shared memory. *AtlasOS: memory.*

## Unit 7 - Workflows and Agent Patterns
Workflow vs agent, the five workflow patterns, the autonomous agent loop, and making plans
trustworthy. **Build:** Atlas v0, a routine that runs one real task end to end. *AtlasOS:
orchestrator.*

## Unit 8 - Multi-Agent Orchestration
When many agents beat one (and the honest cost), the orchestrator-worker pattern, the tool vs
skill vs subagent decision, and frameworks with eyes open. **Build:** the Atlas fleet of
subagents. *AtlasOS: fleet.*

## Unit 9 - Evals and Verification
Why evals are the moat, graders from unit tests to LLM-as-judge, running one suite across models,
keeping one deliberately hard case, unsupervised agents gated by evals, and where evals go at
production scale. **Build:** Warden, the eval harness. *AtlasOS: evals.*

## Unit 10 - Observability, Safety and Production
Logs, metrics and traces, guardrails and prompt-injection defense, hardening (retries, timeouts,
fallbacks), and deploying to one real cloud (with the other two as reference). **Build:**
`deploy/` and `ops/`. *AtlasOS: production.*

## Unit 11 - Capstone and Operating Model
Integrate everything into AtlasOS v1, ship one flagship vertical (analytics, "Pulse"), and the
operating model for a founder plus a fleet. Optional appendices: an applied gallery of other
verticals, and the operating model in depth. **Build:** AtlasOS v1. *AtlasOS: the finish line.*

---

*Off-spine material is preserved, not deleted: the leadership and extra case-study lessons live as
labeled appendices in Unit 11.*

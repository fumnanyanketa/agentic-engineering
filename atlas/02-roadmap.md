# AtlasOS — Lesson-to-Component Roadmap

> Every lesson's capstone, and the exact AtlasOS component it builds. This is your "what do I
> build today" lookup. Read alongside [`00-company-brief.md`](00-company-brief.md) and
> [`01-architecture.md`](01-architecture.md).
>
> **Status:** v0.1 scaffold, 2026-06-16. Adjust as you go; the mapping is a guide, not a cage.

---

## How to use this

Each day: do the lesson, then build its capstone **as the AtlasOS component below** instead
of the lesson's toy example. Commit it under the matching `atlas/<component>/` folder. Tick
the box in `PROGRESS.md`. Over 38 lessons this assembles into one real platform.

> 💡 If a lesson's topic does not obviously fit AtlasOS, the "Contribution" column gives you
> the bridge. The honest move is to build the smallest real version, not to force a fit.

## Module 0 — Pre-flight
| Lesson | Component | Contribution to AtlasOS |
|---|---|---|
| 0. Pre-flight | workstation | Toolchain, accounts, API key, first call. The launchpad. |

## Module 1 — Foundations
| Lesson | Component | Contribution to AtlasOS |
|---|---|---|
| 1. Opening Keynote | `atlas/` (brief) | Write the Atlas Group charter + adoption plan; pick the first primitive to demo. |
| 2. The Capability Curve | `atlas/` (architecture) | Turn "build for the next model" into AtlasOS's thin-scaffolding architecture principles. |

## Module 2 — Core skills
| Lesson | Component | Contribution to AtlasOS |
|---|---|---|
| 3. The Prompting Playbook | `prompts/` | Draft the first real system prompt for an agent (start with Scout). |
| 4. Picking the Right Model | `orchestrator/` | The model-routing policy: which model per step, "cost per successful outcome." |
| 5. The Thinking Lever | `orchestrator/` | Adaptive reasoning-effort rules: when agents think hard vs. answer fast. |
| 6. Getting More Out of the Claude Platform | `prompts/` + `tools/` | Prompt caching, context engineering, the advisor strategy wired into routing. |

## Module 3 — Measuring quality (evals)
| Lesson | Component | Contribution to AtlasOS |
|---|---|---|
| 7. Evals for Taste | `evals/` | Warden's first graded suite, including one deliberately hard case. |

## Module 4 — Claude Code
| Lesson | Component | Contribution to AtlasOS |
|---|---|---|
| 8. What's New in Claude Code | repo tooling | Set up the AtlasOS monorepo dev loop and conventions (CLAUDE.md, skills). |
| 9. How We Claude Code | repo tooling | Adopt the team workflow: plan, review, auto mode, multi-session. |
| 10. Beyond the Basics with Claude Code | `tools/` | Custom harness: hooks, subagents, context-window economics for the fleet. |
| 11. Build a Proactive Agent Workflow | `orchestrator/` | Atlas v0: a routine that runs a real task end to end on a schedule. |
| 12. Stop Babysitting Your Agents | `orchestrator/` | Let Atlas run unsupervised with the right guardrails and a green-PR loop. |

## Module 5 — Building agents (Claude Managed Agents)
| Lesson | Component | Contribution to AtlasOS |
|---|---|---|
| 13. Get to Production Faster | `agents/` | Stand up the first managed-agent skeleton for Scout. |
| 14. Ship Your First Managed Agent | `agents/` | Scout shipped to production: research → synthesis, for real. |
| 15. Build a Production-Ready Agent | `agents/` | Harden Scout: error handling, retries, tools, observability. |
| 16. Tool, Skill, or Subagent? | `agents/` | Decompose a growing agent correctly; document the decision for the fleet. |
| 17. Agents That Remember | `memory/` | Cortex v0: Scout remembers across runs. |
| 18. Memory and Dreaming | `memory/` | The self-improvement loop: distill runs into better instructions overnight. |
| 19. Agent Battle: Mine the Most Diamonds | `agents/` | A focused agent-design drill; harvest the winning patterns into the fleet. |

## Module 6 — Advanced agent engineering
| Lesson | Component | Contribution to AtlasOS |
|---|---|---|
| 20. Trustworthy Workflows with a Custom DSL | `orchestrator/` | Make Atlas's plans verifiable and trustworthy, not just plausible. |
| 21. How AirOps Chases Friction | `ops/` | A friction-log practice: find and remove the fleet's biggest drag. |
| 22. How Metaview Built Self-Improving Prompts | `prompts/` + `evals/` | Close the loop: prompts that improve themselves against evals. |
| 23. Teaching Agents to Learn from Your Team | `memory/` | Cortex learns your standards and taste from feedback. |

## Module 7 — Deploying on your cloud
| Lesson | Component | Contribution to AtlasOS |
|---|---|---|
| 24. Building with Claude on Google Cloud | `deploy/` | Deploy AtlasOS on GCP (pick this OR 25 OR 26 as your primary). |
| 25. AI with Claude on AWS | `deploy/` | Deploy AtlasOS on AWS, code to orchestration. |
| 26. Build AI Agents in Microsoft Foundry | `deploy/` | Deploy AtlasOS on Azure / Foundry. |

## Module 8 — Leading the transformation
| Lesson | Component | Contribution to AtlasOS |
|---|---|---|
| 27. Running an AI-Native Engineering Org | `ops/` | Write the Atlas Group operating model: how founder + fleet actually run. |
| 28. Designing with Claude | `ops/` | A design/taste pass on AtlasOS's interfaces and outputs. |
| 29. From One Person to 80 | `ops/` | A scaling playbook: how AtlasOS would grow past a solo operator. |
| 30. Coding Is No Longer the Constraint (Spotify) | `ops/` | Devex for the fleet: remove the new bottleneck (verification, review). |
| 31. Building AI-Native at Enterprise Scale | `ops/` | The rollout/governance plan for taking AtlasOS to real users. |

## Module 9 — Industry case studies
| Lesson | Component | Contribution to AtlasOS |
|---|---|---|
| 32. Building Signals That Trade Themselves | `agents/` (vertical) | Candidate flagship vertical: a signals/trading Pulse agent. |
| 33. Fighting Financial Crime with Claude Cowork | `agents/` (vertical) | Candidate flagship vertical: a compliance/investigation agent. |
| 34. What Legal Agents Inherit from Coding Agents | `agents/` (vertical) | Candidate flagship vertical: a legal-review agent. |
| 35. Where Code Meets Court | `agents/` (vertical) | Deepen the legal vertical; verification at the legal-technical frontier. |
| 36. How Lovable Vibecodes Production Software | `agents/` (vertical) | Forge as a product-building vertical; ship something real. |
| 37. Building the Best Agentic Analytics Harness | `agents/` (Pulse) | Pulse, finished: the agentic analytics harness as your capstone-of-capstones. |

---

## The finish line

After Lesson 37 you have: an orchestrator (Atlas), at least one production agent with memory
(Scout, plus a flagship vertical), a self-improvement loop, an eval harness (Warden), a
deployment on real cloud, an operating model, and a public build log. That is AtlasOS v1, and
it is the proof that you can take an idea to a shipped, self-improving, deployed agent
platform.

*Tick each lesson in [`../PROGRESS.md`](../PROGRESS.md) as you build its component here.*

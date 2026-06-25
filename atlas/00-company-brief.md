# Atlas Group — Company Brief (north-star source of truth)

> **What this file is.** The single source of truth for your north-star project. Every
> lesson capstone in this course bends toward AtlasOS. When a lesson says "build it toward
> your north-star," this document tells you what that means. Edit it freely as your vision
> sharpens, but keep it honest and specific.
>
> **Status:** v0.1 scaffold, written 2026-06-16. This is a starting frame, not a contract.
> Change anything that does not fit how you actually want to build.

---

## The one-liner

**Atlas Group** is a one-founder-plus-agents venture. Its product, **AtlasOS**, is a
self-improving operating system of cooperating AI agents that runs knowledge work end to
end: you hand it an outcome, and a fleet of specialized agents plans, executes, verifies
itself, remembers, and improves over time, on real infrastructure, with you in the loop for
the decisions that matter.

If CourseForge was "an agent that turns a playlist into a course," AtlasOS is the next order
of ambition: **the operating system you would give an AI-native company.** CourseForge could
even become one app that runs *on* AtlasOS later. The north-star is the platform, not a
single pipeline.

## Why this is the right north-star

The course's own rule is that a good north-star must touch every module, so each capstone
adds a real component instead of a throwaway exercise. AtlasOS does exactly that:

| Course area | What AtlasOS needs from it |
|---|---|
| Foundations (M1) | The charter and architecture: build for the *next* model, thin scaffolding. |
| Core skills (M2) | The prompt library and the model-routing policy (advisor strategy). |
| Evals (M3) | The harness that grades every agent's output, so quality is measured not hoped. |
| Claude Code (M4) | The dev loop that builds AtlasOS itself: routines, autofix, unsupervised agents. |
| Managed Agents (M5) | The first production agents, with memory, shipped on Claude Managed Agents. |
| Advanced agents (M6) | The orchestrator, trustworthy workflows, and the self-improvement loop. |
| Cloud (M7) | Deploying the whole system on real infrastructure. |
| Leadership (M8) | The operating model: how one founder plus a fleet actually runs. |
| Case studies (M9) | Pointing AtlasOS at one real vertical and proving it in the wild. |

> 🔑 By the end you do not have 38 disconnected exercises. You have shipped **one real
> platform**, in public, plus the durable skills (prompting, evals, context engineering,
> agent design, verification) that outlast any single model.

## The cast (so "build a component" is always concrete)

AtlasOS is a small fleet with named roles. Naming them makes every capstone obvious: you are
always building, improving, or connecting one of these.

- **Atlas** — the orchestrator. Takes a high-level outcome, decomposes it, dispatches the
  right agents, and decides when to escalate to you. (Built mostly in M4 and M6.)
- **Cortex** — the shared memory. What the fleet knows, learns, and "dreams" on overnight.
  (Built in M5 and M6.)
- **Scout** — research and intelligence. Web and source gathering, retrieval, synthesis.
- **Forge** — the builder. Writes and ships code through Claude Code.
- **Pulse** — analytics. Turns data into insight (the agentic analytics harness from M9).
- **Herald** — comms and reporting. Drafts updates, briefs, and the weekly business review.
- **Warden** — review, safety, and verification. The eval gatekeeper and your human-in-the-
  loop interface. Nothing ships past Warden without passing its checks. (Rooted in M3.)

> 💡 You do not build all seven at once. M5 ships your first real agent (start with
> **Scout**), and each later module deepens one part. The architecture map shows the order.

## Definition of done (the "hero" outcome)

AtlasOS is "done enough to be proud of" when all of these are true:

- ✅ You can give Atlas a high-level outcome (for example "keep our competitive intel
  current" or "produce this week's business review") and the fleet executes it end to end.
- ✅ Every agent's output is graded by an eval harness (Warden), and regressions are caught.
- ✅ The system has memory (Cortex): it remembers context across runs and improves over time.
- ✅ It runs on real cloud infrastructure, is observable, and survives you closing your laptop.
- ✅ A human-in-the-loop step exists for the decisions that genuinely need judgment.
- ✅ At least one **flagship vertical** (chosen in M9) is working against a real use case.

## Design principles (carried from the keynote)

1. **Build for the next model, not today's.** Keep scaffolding thin; let the model do more
   as it gets smarter. Audit and trim guardrails regularly.
2. **Evals harder than the model.** If Warden's tests are too easy, you cannot tell a better
   model from a worse one. Keep at least one failing case as your "the exponential moved"
   detector.
3. **Primitives compose.** Routines, sandboxes, tools, memory, and the advisor strategy are
   small pieces you snap together. Prefer composition over one giant feature.
4. **Cost per successful outcome, not cost per token.** Cheap models execute; the expensive
   model advises only when needed.
5. **Outcomes over tasks.** The unit of work is "own this result over time," not "do this
   one thing once."
6. **Verification is the bottleneck.** As building gets cheap, the scarce skill is checking.
   Warden is a first-class citizen, not an afterthought.

## Non-goals (so scope stays sane)

- Not a polished consumer SaaS with billing and a marketing site. It is a platform and a
  portfolio, built in public.
- Not seven perfect agents. One excellent agent plus a real orchestrator beats five demos.
- Not provider lock-in theater. Learn the durable disciplines; hold model ids loosely.

## Alternates (if AtlasOS ever stops fitting)

The point is one ambitious, module-spanning build. If AtlasOS loses its pull, swap it for a
single real platform you care about (a research org's agent fleet, a trading-signal
platform, a support org's agent stack) and keep the same component map. Do not drift back to
disconnected exercises.

---

*Source of truth for the "Building with Claude" course north-star. See
[`01-architecture.md`](01-architecture.md) for how the pieces fit and
[`02-roadmap.md`](02-roadmap.md) for which lesson builds which piece.*

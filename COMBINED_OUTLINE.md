# Combined Course Outline (PROPOSAL)

> **Status:** proposal for review, 2026-06-16. Nothing has been merged or deleted yet.
> This document maps two existing courses onto one compressed spine. Approve or adjust the
> structure here first; only then do we restructure the actual lesson files.

## The two sources

1. **Agentic Engineering** (`fumnanyanketa/agentic-engineering`) — vendor-neutral, concept-
   organized. 7 phases, 18 modules, 18 labs. The **principles layer** (the durable "why").
2. **Building with Claude** (this repo) — Claude-specific, built from 2026 conference talks.
   Module 0 + 9 modules, 38 lessons, plus first-principles companions and the AtlasOS build.
   The **implementation layer** (the concrete "how").

Combined, that is **56 content units** with heavy overlap, which is the source of both the
length and the repetition.

## The strategy: overlay, don't concatenate

The two courses are nearly parallel concept-for-concept. So we **overlay** them:

- **Spine** = Agentic Engineering's concept arc (better pedagogy than talk order).
- **Home** = this repo (build pipeline, AtlasOS scaffold, HTML, companions).
- **Each unit** = one principle (from AE) + the Claude way to do it + one AtlasOS build.

Where both courses teach the same idea, they collapse into **one** unit. That is the
compression: **56 content units → 11 units.**

## Why this kills "tutorial hell"

- **One concept, one unit, one build.** Each unit ends in a single AtlasOS component, so you
  are building one system, not "finishing two courses."
- **State each principle once**, in the unit where it first matters. Repeats become a
  sentence or are cut. Depth and the verified first-principles links stay; duplicate framing
  goes.
- **Estimated length:** ~11 core units (about 3 weeks at one unit per 1–2 sittings) versus the
  current 6–8 weeks across two courses.

---

## The compressed spine (11 units)

Ordered as a learning arc: mental model → your build tool → single-model skills →
augmentation → agents → orchestration → reliability → capstone. (Note: "coding-agent
workflow" is moved early, because you build everything else *with* it.)

| Unit | Title | From Agentic Eng. | From Building with Claude | AtlasOS build |
|---|---|---|---|---|
| **0** | Foundations & the mental model | M00 Baseline + mental model, M01 How LLMs work | M0 Pre-flight, M1 (L1 keynote, L2 capability curve) | workstation + charter/architecture |
| **1** | The coding-agent workflow *(your build environment)* | M16 Working with coding agents | M4 (L8 what's new, L9 how we, L10 beyond basics) | repo dev loop |
| **2** | Prompting & context engineering | M02 Prompt eng, M03 Context eng I | M2 (L3 prompting playbook, L6 platform/caching) | prompt library |
| **3** | Model & reasoning levers | (cost parts of M15) | M2 (L4 picking a model, L5 thinking lever) | routing policy |
| **4** | Tools, function-calling & MCP | M04 Tool use, M09 MCP | M5 L14 tool use; M2 tool-search | tool / MCP layer |
| **5** | Retrieval, memory & state | M05 Retrieval & RAG, M06 Memory at scale | M5 (L17 remember, L18 dreaming), M6 L23 learn from team | Cortex memory |
| **6** | Workflows & agent patterns | M07 Five patterns, M08 Autonomous agents | M4 L11 proactive, M5 L13 production, M6 L20 DSL | orchestrator |
| **7** | Multi-agent orchestration | M10 Multi-agent, M11 Toolkit | M5 (L16 tool/skill/subagent, L19 agent battle) | orchestrator (fleet) |
| **8** | Evals & verification | M12 Evaluation: the moat | M3 L7 evals, M4 L12 stop babysitting, M6 L22 self-improving prompts | Warden harness |
| **9** | Observability, safety & production | M13 Observability, M14 Safety/guardrails, M15 Hardening | M5 L15 hardening, M6 L21 friction, M7 (L24–26 cloud, condensed) | deploy + ops |
| **10** | Capstone + operating model | M17 Capstone: orchestration platform | M8 L27–31 (→ short appendix), M9 L32–37 (→ pick **one** vertical) | AtlasOS v1 |

Every AE module (00–17) and every Claude lesson (0–37) lands in exactly one unit. Nothing is
silently dropped; the overlaps are what collapse.

## What becomes optional (appendices, not spine)

- **Leadership** (Claude M8, 5 lessons) → one short "operating model" appendix in Unit 10.
- **Extra case studies** (Claude M9) → pick **one** as the capstone vertical; the rest become
  an optional "applied gallery."
- **Extra clouds** (Claude M7) → teach one provider in Unit 9; the other two are reference.

## Decisions (locked 2026-06-16)

- **Lean ~11-unit core**, per the spine table above. ~3 weeks core.
- **Preservation rule: nothing is deleted.** Anything that does not sit on the spine becomes
  a clearly labeled **appendix or reference page**, not a cut. Important and necessary
  material is always reachable; it just moves off the required path.
- **Leadership (Claude M8) and case studies (Claude M9) → optional appendices.** Valuable
  context, but not core build skills, so they do not lengthen the required path. One case
  study is promoted to the capstone vertical in Unit 10 (chosen when we get there).
- **Sourcing:** the Agentic Engineering course is published publicly at
  `fumnanyanketa.github.io/agentic-engineering`, so its content is pulled from the live site;
  no repo-scope change is required to merge.

---

## Execution plan (after you approve this map)

1. **Add the `agentic-engineering` repo to scope** so I can read its lesson *source* (the
   public site gives structure only; merging content needs the markdown).
2. **Restructure in this repo** under a new `lessons/` tree following the 11-unit spine
   (keep the old trees until the new one is verified, then remove).
3. **Per unit:** fold AE principle + Claude implementation into one lesson, dedupe, keep the
   first-principles companion, end on the AtlasOS build.
4. **Rebuild** HTML + index; update PROGRESS, COURSE_OUTLINE, start-here.
5. Archive the standalone `agentic-engineering` repo with a pointer here.

## What I need from you

1. **Approve or adjust the 11-unit spine** (or pick the medium 14-unit level).
2. **Confirm the capstone vertical** (which Module 9 case study: trading signals, financial
   crime, legal, analytics, or your own).
3. **Grant access to the `agentic-engineering` repo** so I can pull its lesson content.

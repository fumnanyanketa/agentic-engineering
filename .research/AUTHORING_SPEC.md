# Authoring spec for the Agentic Engineering course (read before writing any unit)

This is the binding spec for every unit. It encodes decisions already agreed with the
course owner. Follow ALL of it. The finished, approved reference is
`combined/unit-01-coding-agent-workflow.md` — match its tone, depth, and structure.

## What the course is
"Agentic Engineering" — a single, model-agnostic, self-paced course that takes a beginner from
zero to building AtlasOS, a north-star platform of cooperating AI agents.

- NEVER brand it "Building with Claude" or "Code with Claude". NEVER mention that it was ever
  two separate courses or a "merge" — learners must see one course with no lineage.
- The course name is "Agentic Engineering". Working subtitle: "a model-agnostic self-paced path".

## The five non-negotiables

1. **Model-agnostic.** State each principle vendor-neutrally FIRST (the durable why). Then show
   HOW with more than one tool/provider, so a learner uses their preferred one and still learns
   the others:
   - Coding-agent / dev-workflow topics → cover **Claude Code, Gemini CLI, Codex CLI**
     (use `.research/coding-agents-2026.md` for verified specifics).
   - Model/API concepts (prompting, model choice, tools/function-calling, retrieval, evals,
     safety, etc.) → cover the principle, then how it looks across **Claude (Anthropic),
     Gemini (Google), and GPT (OpenAI)**, usually as a short comparison table or parallel
     bullets. Claude may be the worked example but must NOT be the only one shown.
   - Accuracy over completeness: prefer conceptual cross-provider statements ("all three expose
     function calling: you describe tools as JSON schemas and the model returns a structured
     call") over invented exact parameter names. Wherever a model id or exact flag appears, add a
     short "verify against current docs" note. Hold model ids loosely.

2. **Beginner-friendly and highly detailed.** Assume NO prior knowledge. Define every term the
   first time it appears. When you introduce a concept, explain exactly how to do it, where to
   find things, and what the learner will see on screen. More explanation is always better than
   less; never be terse or say "as you'd expect". Use authentic visual aids: labeled terminal or
   code transcripts that show the command AND the expected output, and ASCII diagrams for
   processes/flows. DO NOT fabricate screenshots of apps. Real URLs where a learner must go.

3. **Style.** NO em dashes anywhere (use commas, colons, parentheses). Plain, warm, direct.
   Callouts use a leading emoji exactly like Unit 1: 🎯 where-this-is-heading, 🔑 key idea,
   💡 tip, ✅ do-this, ❌ avoid-this. Use comparison tables for multi-tool/provider coverage.

4. **AtlasOS throughline.** AtlasOS is ONE platform built one component per unit (not separate
   toy projects). Read `atlas/00-company-brief.md` and `atlas/02-roadmap.md`. End every unit on a
   hands-on Build that produces THIS unit's AtlasOS component (named in the roadmap). The Build
   must be hand-held: exact steps, what to type, what you'll see, how to verify. It builds on the
   repo and workstation created in Unit 1.

5. **Paginated structure.** The build tool splits each unit into pages by heading, so headings
   MUST be exact (see template below). Each Part is one bite-size idea on its own page.

## Exact markdown structure (match precisely)

```
# Unit N: <Title>

> **Course:** Agentic Engineering, a model-agnostic self-paced path *(working title)*
> **Unit N of 11:** <one-line scope>
> **Principle (vendor-neutral):** <which AE module(s)>
> **The how, across tools/models:** <which tools or providers>
> **AtlasOS build:** <the component from the roadmap>
> **Estimated time:** <e.g. 90 to 120 minutes>

---

## In one sentence
<one dense, plain-language sentence; this becomes the page subtitle>

> 🎯 **Where this unit is heading.** <2-4 sentences pointing to The Build>

## First-principles companion
> 💡 **The durable ideas behind this unit.** ...
> - 2 to 4 DURABLE links (papers/essays). Open the source lesson files and COPY the real,
>   verified URLs from their own "First-principles companion" boxes. Never invent URLs.

## A few plain-language basics first
- **Term:** plain definition. (Define everything this unit uses.)

## Why this unit matters
<short; include one > 🔑 one-line principle callout>

## Learning objectives
By the end of this unit you will be able to:
1. ...

## Prerequisites
- ...

---

## Part 1: <title>
<teaching that fuses the AE principle with the multi-tool/provider how; bite-size>

## Part 2: <title>
...
## Part N: <title>
(Use 3 to 6 Parts. Use a "## Part 0:" first ONLY if there is a setup/orientation step.)

## Key takeaways
1. ...

## Common pitfalls
- ❌ ...

## 🛠️ The Build: <this unit's AtlasOS component>
> <one-line framing of the payoff>
### What you will build
<short paragraph>
### Milestones (in order, each fully explained)
1. <hand-held step: exact actions, what to type, what you'll see>
### How you will know you are done
- ✅ ...

## Cheat sheet
```text
<compact text recap>
```

## How this connects to the rest of the course
- **Next, Unit N+1 (...):** ...
- **Throughout:** ...

---

*Unit N of the combined path. Fuses the vendor-neutral principle of <AE module> with current,
model-agnostic practice (<tools/providers>). Tool commands and model ids change quickly; verify
against current documentation.*
```

## Page-split rules (so headings render as separate pages)
- The text before the first `## Part` becomes the "Overview" page.
- Each `## Part N:` becomes its own page.
- `## Key takeaways` starts the "Recap" page (Common pitfalls rides along).
- `## 🛠️ The Build` starts the "The Build" page (Cheat sheet + How this connects ride along).
Keep this exact ordering of the end matter: Key takeaways, Common pitfalls, The Build,
Cheat sheet, How this connects.

## Length and output
- Roughly Unit 1's depth: about 350 to 500 lines. Favor thorough, hand-held clarity.
- Write the file to the path given in your task. Then reply with ONLY: the file path, the H1
  title, the ordered list of Part titles, and an approximate word count. Do NOT paste the body.

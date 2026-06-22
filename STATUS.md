# Repository Status Report

_Deep-dive generated 2026-06-22. Findings are based on reading the actual files in the repo, not branch names or commit messages._

## TL;DR

This repo is **not software** in the usual sense. It is a **self-paced online course on "Agentic Engineering"**, delivered as a set of **hand-styled static HTML pages** designed to be published via GitHub Pages. There is no application, no backend, no build step, no tests, and no source code to compile — just 22 HTML files and one GitHub Actions workflow. The course content itself is **substantively complete and polished** (~39,000 words of real prose across 18 module pages plus orientation/resources). The "incompleteness" here is almost entirely **project hygiene** (no README, no license), not missing content.

---

## 1. Branch inventory

| Branch | Last commit (UTC) | vs `main` | What's actually in it |
|---|---|---|---|
| `main` (default) | 2026-06-18 20:18 | — | The full course: `index.html`, 18 module pages, `orientation.html`, `resources.html`, Pages deploy workflow. |
| `claude/pensive-cray-j58i2u` | 2026-06-18 20:18 | **0 ahead / 0 behind** | Identical to `main` at commit `a79ca5d`. This is the working branch for this report; before STATUS.md it carried no unique work. |

There are exactly **two branches (one local-tracked, two remote refs) and both point at the same commit** `a79ca5d`. No stale, abandoned, stranded, or unmerged feature branches exist. No tags, no other remotes.

**Full history (3 commits, all 2026-06-18, single author "Claude"):**
- `bcb1b4b` Publish Agentic Engineering HTML course via GitHub Pages
- `92a9c76` Rewrite Module 1 in beginner-friendly language; remove em dashes
- `a79ca5d` Rewrite course as vendor-neutral, beginner-friendly playbook

The entire project was created and rewritten within a ~2-hour window on a single day. Nothing has changed since 2026-06-18.

---

## 2. What this project actually is

An educational website titled **"Agentic Engineering — From Zero to Agent Orchestrator,"** branded **"AI Nativity."** It is a structured, vendor-neutral curriculum that teaches how to design, evaluate, and operate production LLM-agent systems. Read from the files, the structure is:

- **7 phases (Phase 0–6), 18 modules (00–17), each ending in a hands-on lab**, building toward a capstone "agent orchestration platform."
- Topics actually covered (verified by reading the pages): how LLMs work, prompt engineering, context engineering, tool use / function calling, retrieval & RAG, memory/context management, the five workflow patterns, autonomous agent loops, MCP, multi-agent orchestration, framework trade-offs, evaluation, observability/tracing, safety & guardrails (prompt injection, the "lethal trifecta"), production hardening, working with coding agents, and a capstone.
- Content style is genuinely beginner-friendly: every jargon term is defined inline, with "Objective / Best practices / Pitfalls / Milestone / Publish this" callouts and citations to primary sources (Karpathy, Simon Willison, Chip Huyen, Anthropic engineering, ReAct/Reflexion papers, Hamel Husain, Eugene Yan).

It is content-first: the footer notes it was "built from a deep-research pass across primary sources" and "designed to be published through, not just read."

---

## 3. Built vs. stubbed — roughly **90% complete (as a content site)**

**Genuinely built (real, finished content):**
- All 18 module pages contain real, complete prose (1,200–2,600 words each; ~39k words total). None are stubs or placeholders.
- `index.html` — full landing page with all 18 modules linked and described.
- `orientation.html` (~2,200 words) and `resources.html` (~2,000 words) — real content.
- Each module includes a hands-on lab box, table of contents, prev/next navigation, mobile menu, and reading-progress bar (vanilla JS, no dependencies).
- `.github/workflows/pages.yml` — a valid, standard GitHub Pages deploy workflow triggered on push to `main`.
- **Internal link integrity: clean.** Every local `href` resolves to an existing file — no broken links found.
- **No placeholder/TODO/lorem/"coming soon" markers** anywhere (the single "placeholder" hit is legitimate prose about PII masking).

**Not present / thin:**
- **No `README.md`** — a visitor to the GitHub repo gets no explanation of what this is or how to use/deploy it.
- **No `LICENSE`** — for a course meant to be published and followed by others, this is a real gap (default = all rights reserved, which discourages reuse).
- **No labs scaffolding.** The 18 "hands-on labs" are described in prose only; there is no starter code, repo, or solution for any of them — including the capstone, which is specified in detail but ships zero code.
- No custom domain config (`CNAME`), no `.nojekyll`, no favicon/OG images/social preview.
- ~16KB of nearly-identical inline CSS is copy-pasted into every module page (maintenance smell, not a defect).

**Why "complete as a content site" but not "complete as a course":** the teaching material is done; the *practice* half of a "hands-on" curriculum (actual lab repos/code) does not exist.

---

## 4. What's left, and the single biggest blocker

Remaining work, in plain terms:
1. Add a `README.md` (what this is, who it's for, how to run/deploy locally).
2. Add a `LICENSE` (the content is explicitly meant to be shared).
3. Confirm GitHub Pages is actually enabled and the site renders at its URL.
4. Optionally provide starter/solution code for the labs and capstone.
5. Optionally factor the shared CSS into one stylesheet.

**Single biggest blocker:** **a decision about scope/intent.** Is this a *reading* curriculum (in which case it's essentially done and just needs README + LICENSE + Pages verification), or a *hands-on* one (in which case the largest piece — lab and capstone code for 18 modules — is entirely unbuilt)? Everything downstream depends on that call. There is no technical blocker; the work is unblocked the moment the goal is set.

---

## 5. Quick wins (nearly done)

- **Add a `README.md`** — 15 minutes; immediately makes the repo legible to anyone who lands on it.
- **Add a `LICENSE`** (e.g. CC-BY for content, MIT for any code) — 5 minutes; unblocks the stated goal of others following the build.
- **Verify the Pages deploy** — the workflow already exists; just confirm Pages is enabled in repo settings and the URL is live.
- **Add `.nojekyll` + a favicon** — trivial polish that prevents Jekyll surprises and improves the published look.

---

## 6. Blunt recommendation: **KEEP and FINISH (lightweight)**

This is a coherent, high-quality, finished piece of writing — not abandoned scaffolding and not something to discard. It does **not** need to be merged into another project or archived. The honest gap is that it presents itself as "hands-on" with 18 labs and a capstone, yet ships no code for any of them, and it lacks the basic repo furniture (README/LICENSE) to be usable by others.

Recommendation: **finish the cheap, high-leverage hygiene now** (README, LICENSE, verify Pages) and ship it as a reading curriculum. Treat the lab/capstone code as a clearly-scoped, optional **follow-on** project rather than pretending it's almost there — it isn't started. If no one intends to build the labs or maintain the content against a fast-moving field, then publish it as-is, mark it as a point-in-time reference, and leave it; do not let it rot half-described as interactive.

---

## Next actions

- [ ] Decide scope: **reading curriculum (ship now)** vs **hands-on curriculum (commit to building lab/capstone code)** — this unblocks everything else.
- [ ] Add `README.md` (what it is, audience, how to view/deploy, link to the live Pages URL).
- [ ] Add a `LICENSE` (content license such as CC-BY; separate code license if labs get built).
- [ ] Verify GitHub Pages is enabled and the deployed site renders correctly end-to-end.
- [ ] Add `.nojekyll` and a favicon/OG image for a clean published presentation.
- [ ] (If hands-on) Create starter + solution repos for the labs, beginning with the Module 17 capstone spec.
- [ ] (Maintenance) Extract the duplicated inline CSS into one shared stylesheet to ease future edits.

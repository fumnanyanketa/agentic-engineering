# Repository Status Report

_Deep-dive regenerated 2026-06-22 using a server-authoritative branch diagnostic. Findings are based on reading the actual files, not branch/commit names._

## Correction note (vs. the previous STATUS.md)

An earlier version of this file (committed on branch `claude/pensive-cray-j58i2u`) stated the feature branch was **"0 ahead / 0 behind — identical to main."** That was true at the moment the branch was *read*, but became stale the instant STATUS.md was committed onto it. The accurate, current picture: the feature branch is **1 commit ahead of `main`**, and that one commit is STATUS.md itself. Nothing else changed. This version also adds an explicit server-authoritative branch count, which the previous version did not show.

---

## Step 1 — Branch diagnostic (server is the source of truth)

```
git ls-remote --heads origin   ->   2 branches (AUTHORITATIVE)
git branch -r (locally visible) ->  2 branches  (matches)
```

**There are exactly 2 branches on the server. No hidden, sparse, or orphan branches.**

| # | Branch | Head | Notes |
|---|---|---|---|
| 1 | `main` (default) | `a79ca5d` | The course. No STATUS.md. |
| 2 | `claude/pensive-cray-j58i2u` | `4c7d359` | `main` + 1 commit adding this STATUS.md. Shares history with main (merge-base = `a79ca5d`), so **not** an orphan. |

`git rev-list --left-right --count main...feature` = `0  1` → feature is **1 ahead / 0 behind**. The only file differing between the two branches is `STATUS.md`.

---

## Step 2/3 — Per-branch deep-dive

### Branch `main` (`a79ca5d`, last commit 2026-06-18 20:18 UTC)
- **Full history is only 3 commits, all on 2026-06-18**, single author "Claude", inside a ~2-hour window. Nothing has changed since.
  - `bcb1b4b` Publish Agentic Engineering HTML course via GitHub Pages
  - `92a9c76` Rewrite Module 1 in beginner-friendly language; remove em dashes
  - `a79ca5d` Rewrite course as vendor-neutral, beginner-friendly playbook
- **Contents (read, not inferred):** 22 tracked files = 20 course HTML pages + 1 landing page region + 1 GitHub Pages workflow. Specifically: `index.html`, `orientation.html`, `resources.html`, `modules/module-00…17` (18 module pages), and `.github/workflows/pages.yml`. **The only non-HTML file in the entire repo is the Pages workflow.**

### Branch `claude/pensive-cray-j58i2u` (`4c7d359`, this report's branch)
- Identical to `main` plus a single commit adding `STATUS.md`. **No unique project work** lives here — it is purely the status report. Not stale, not stranded; it exists to carry this document. Once reviewed, it can be merged to `main` or discarded with no loss of project code.

**No stale, abandoned, redundant, or stranded feature branches exist. No second/separate project hiding in another branch.**

---

## Step 4 — Assessment

### 1. What this project actually is
A self-paced **course website**, titled **"Agentic Engineering — From Zero to Agent Orchestrator,"** branded **"AI Nativity."** It is **not application software** — there is no backend, no build step, no tests, no dependencies, and (aside from small inline vanilla-JS for nav/progress bar) no real source code. It is hand-written static HTML.

The curriculum (verified by reading the pages) is a vendor-neutral path through production LLM-agent engineering: **7 phases, 18 modules (00–17), each ending in a hands-on lab**, building toward a capstone "agent orchestration platform." Topics actually present: how LLMs work, prompt & context engineering, tool use/function calling, retrieval & RAG, memory/context management, the five workflow patterns, autonomous agent loops, MCP, multi-agent orchestration, framework trade-offs, evaluation, observability/tracing, safety & guardrails (prompt injection, the "lethal trifecta"), production hardening, working with coding agents, and the capstone. Prose is genuinely beginner-friendly (every term defined inline) with citations to primary sources (Karpathy, Simon Willison, Chip Huyen, Anthropic engineering, ReAct/Reflexion, Hamel Husain, Eugene Yan).

### 2. Built vs. stubbed — roughly **90% complete as a content site**
**Genuinely built:**
- All 18 module pages contain real, finished prose (~39,000 words total across the site; no module is a stub).
- `index.html`, `orientation.html` (~2.2k words), `resources.html` (~2.0k words) — all real content.
- Per-page UX: table of contents, prev/next nav, mobile menu, reading-progress bar.
- Valid GitHub Pages deploy workflow (`pages.yml`, triggers on push to `main`).
- **Internal link integrity is clean** (every local `href` resolves; re-verified). **No TODO/lorem/placeholder/"coming soon" markers** anywhere.

**Missing / thin:**
- **No `README.md`** — a visitor to the repo gets zero explanation or deploy instructions.
- **No `LICENSE`** — yet the content is explicitly meant to be shared/followed (default "all rights reserved" discourages reuse).
- **No lab code.** All 18 "hands-on labs" and the detailed capstone are described in prose only — **zero starter code, solutions, or repos ship**. The *practice* half of a "hands-on" course does not exist.
- No `.nojekyll`, favicon, OG/social image, or custom domain.
- ~16KB of near-identical inline CSS is duplicated into every module page (maintenance smell, not a defect).

### 3. What's left, and the single biggest blocker
Remaining: README, LICENSE, verify Pages is actually live, optionally build lab/capstone code, optionally de-duplicate CSS.

**Single biggest blocker: a scope decision, not a technical one.** Is this a *reading* curriculum (then it's essentially done — just needs README + LICENSE + Pages verification) or a *hands-on* one (then the largest piece — lab/capstone code for 18 modules — is entirely unbuilt)? Everything downstream hinges on that call. There is no technical blocker.

### 4. Quick wins
- Add `README.md` (~15 min) — makes the repo legible immediately.
- Add `LICENSE` (~5 min) — unblocks the stated "others can follow this" goal.
- Verify GitHub Pages is enabled and the URL renders (workflow already exists).
- Add `.nojekyll` + favicon — trivial polish for the published site.

### 5. Blunt recommendation: **KEEP & FINISH (lightweight); then MERGE this branch to `main`**
The writing is coherent and high quality — not abandoned scaffolding, not something to discard or archive, and there is no second project to split out. The honest gap is the **mismatch between its "hands-on, 18 labs + capstone" framing and the total absence of lab code**, plus missing README/LICENSE.

Do the cheap, high-leverage hygiene now (README, LICENSE, verify Pages) and ship it as a **reading curriculum**. Treat lab/capstone code as a clearly-scoped, **optional follow-on** rather than pretending it's nearly there — it is not started. If nobody intends to build the labs or maintain the content against a fast-moving field, publish as-is, label it a point-in-time reference, and stop — don't leave it half-described as interactive. The `claude/pensive-cray-j58i2u` branch carries only this report and should be merged to `main` (or closed) so STATUS.md lives on the default branch.

---

## Next actions

- [ ] **Decide scope:** reading curriculum (ship now) vs hands-on (commit to building lab/capstone code). Unblocks everything else.
- [ ] Add `README.md` (what it is, audience, how to view/deploy, live Pages URL).
- [ ] Add a `LICENSE` (e.g. CC-BY for content; separate code license if labs get built).
- [ ] Verify GitHub Pages is enabled and the deployed site renders end-to-end.
- [ ] Merge `claude/pensive-cray-j58i2u` into `main` so STATUS.md lives on the default branch (or close the branch).
- [ ] Add `.nojekyll` + favicon/OG image for a clean published presentation.
- [ ] (If hands-on) Build starter + solution repos for the labs, beginning with the Module 17 capstone spec; (maintenance) extract duplicated inline CSS into one shared stylesheet.

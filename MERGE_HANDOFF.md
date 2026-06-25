# Merge handoff — read this first (for a Claude session on `agentic-engineering`)

**If you are Claude running in a session scoped to `fumnanyanketa/agentic-engineering`,
this file is your brief. The user wants you to finish the merge here. Do it; don't re-ask
the plan.**

## Goal

Make `agentic-engineering` the permanent home of a single, merged, compressed course that
combines this repo's vendor-neutral **Agentic Engineering** modules (the principles layer)
with the **Building with Claude** course from `fumnanyanketa/code-with-claude-` (the
implementation layer). Target: **11 fused units**, each = one principle + the Claude way to
do it + one build toward the north-star project **AtlasOS**.

The full plan, the 11-unit spine, the lesson-to-unit mapping, and the locked decisions live
in `COMBINED_OUTLINE.md` (imported in step 1). A finished pilot, `combined/unit-00-foundations.md`,
shows the exact target format. **Match the pilot's style.**

## Step 1 — Import the work already done (in `code-with-claude-`)

All of it is committed on branch `claude/youtube-playlist-transcripts-qkwwis`. Pull the paths
across surgically (no history merge, no overwrite of this repo's `modules/`):

```bash
git checkout -b import-merge-project
git remote add claude https://github.com/fumnanyanketa/code-with-claude-.git
git fetch claude claude/youtube-playlist-transcripts-qkwwis
git checkout claude/youtube-playlist-transcripts-qkwwis -- \
  atlas COMBINED_OUTLINE.md MERGE_HANDOFF.md combined \
  build_lessons_html.py build_index.py build_course.py \
  PROGRESS.md COURSE_OUTLINE.md start-here.html \
  lessons lessons-html
git add -A && git commit -m "Import AtlasOS + combined-course plan + pilot from code-with-claude-"
```

If that remote fetch fails on auth (private repo), tell the user the one thing to do: make
`code-with-claude-` temporarily public, or grant this session access to it. Do not silently
reconstruct from memory.

## Step 2 — Build the remaining 10 units

Source material:
- **Principles layer** = this repo's existing modules under `modules/` (Agentic Engineering
  Modules 00–17). Read them directly.
- **Implementation layer** = the imported `lessons/` (Building with Claude, lessons 0–37).
- **Mapping** = the table in `COMBINED_OUTLINE.md` (which AE modules + which Claude lessons
  feed each unit).

For each unit 1–10, write `combined/unit-NN-<slug>.md` fusing the two sources, deduping
overlap, keeping the first-principles companion box, and ending in the AtlasOS build. Keep
each unit roughly the length of the pilot (compression is the point).

## Step 3 — Wire it up and publish

- Adapt `build_*.py` to render `combined/*.md` into the published site (this repo uses GitHub
  Pages). Update `PROGRESS.md`, `COURSE_OUTLINE.md`, `start-here.html` to the 11-unit course.
- Point GitHub Pages at the combined course.
- Leave a note in `code-with-claude-` that the course has moved here, and archive it.

## Decisions already locked (do not relitigate)

- Lean ~11-unit core; nothing deleted, off-spine material becomes labeled appendices.
- Leadership (Claude M8) and case studies (Claude M9) → optional appendices; one case study
  becomes the capstone vertical (ask the user which when you reach Unit 10).
- North-star project is **AtlasOS** (see `atlas/00-company-brief.md`).
- Course working title: "Agentic Engineering with Claude."

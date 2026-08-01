#!/usr/bin/env python3
"""Build the combined, model-agnostic course from `combined/*.md`.

Each unit markdown file is split into a SEQUENCE OF PAGES, one per Part, so a
learner moves through bite-size pages instead of one dense scroll: an Overview
page (intro through prerequisites), then one page per "## Part N", then a Recap
page and a "The Build" page. Pages get a unit outline in the sidebar, a step
indicator, and Previous/Next navigation that also flows across units.

Content is never reduced here; it is only split and signposted. The template is
the de-branded (model-agnostic) version of the lesson template.

Usage: python3 build_combined.py
Writes combined/<unit-stem>/NN-slug.html for every page, plus combined/index.html.
"""
import html
import json
import pathlib
import re
import shutil

import build_lessons_html as bl

ROOT = pathlib.Path(__file__).resolve().parent
COMBINED = ROOT / "combined"
ASSETS = COMBINED / "assets"
COURSE_NAME = "Agentic Engineering"
TOTAL_UNITS = 12

# Browser-tab favicon: a self-contained SVG (teal "A" on navy) as a base64 data
# URI, so it needs no separate file and resolves identically at every page depth.
FAVICON_LINK = '<link rel="icon" type="image/svg+xml" href="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzMiAzMiI+PHJlY3Qgd2lkdGg9IjMyIiBoZWlnaHQ9IjMyIiByeD0iNyIgZmlsbD0iIzBhMWEyZiIvPjx0ZXh0IHg9IjE2IiB5PSIyMyIgZm9udC1mYW1pbHk9IkFyaWFsLEhlbHZldGljYSxzYW5zLXNlcmlmIiBmb250LXNpemU9IjIxIiBmb250LXdlaWdodD0iYm9sZCIgZmlsbD0iIzE4YzRhMCIgdGV4dC1hbmNob3I9Im1pZGRsZSI+QTwvdGV4dD48L3N2Zz4=">'

# Progress-tracker engine (see references/progress-tracker.md in the course-builder
# skill). sync.js is the committed engine; this scaffold is written for sync-config.js
# only if it is missing, so a learner's Firebase keys are never overwritten.
SYNC_CONFIG_SCAFFOLD = """\
// Firebase config for optional cross-device progress sync.
// Until you fill this in, the tracker still works, but only in this one browser
// (no cross-device sync, no sign-in). Nothing here is secret: a Firebase web
// config is meant to live in client code; your data is protected by the Firestore
// security rules, not by hiding these values.
export const firebaseConfig = {
  apiKey: "REPLACE_ME",
  authDomain: "REPLACE_ME.firebaseapp.com",
  projectId: "REPLACE_ME",
  appId: "REPLACE_ME"
};
"""

# ---------------------------------------------------------------------------
# De-brand the shared lesson template (model-agnostic course) and adapt a few
# anchors/links for the multi-page layout.
# ---------------------------------------------------------------------------
TEMPLATE = bl.TEMPLATE
TEMPLATE = TEMPLATE.replace("{{TITLE}} | Building with Claude", "{{TITLE}} | " + COURSE_NAME)
TEMPLATE = TEMPLATE.replace(
    '<meta name="viewport" content="width=device-width, initial-scale=1">',
    '<meta name="viewport" content="width=device-width, initial-scale=1">\n' + FAVICON_LINK, 1)
TEMPLATE = TEMPLATE.replace(
    "&#10024; Welcome to <b>Building with Claude</b> &middot; a self-paced course",
    "&#10024; Welcome to <b>" + COURSE_NAME + "</b> &middot; a self-paced course",
)
TEMPLATE = TEMPLATE.replace(
    "<span>Code with Claude 2026 &middot; London</span>",
    "<span>Model-agnostic &middot; self-paced</span>",
)
TEMPLATE = TEMPLATE.replace(
    '<a class="logo" href="{{HOME}}">Building with Claude<span class="dot">.</span></a>',
    '<a class="logo" href="{{HOME}}">' + COURSE_NAME + '<span class="dot">.</span></a>',
)
TEMPLATE = TEMPLATE.replace(
    "A self-paced course generated from the Code with Claude 2026 (London) talks. "
    "Code snippets are illustrative reconstructions of the approaches shown. "
    "Adapt them to the current SDK.",
    "A self-paced, model-agnostic course: durable agentic-engineering principles, "
    "the how across Claude Code, Gemini CLI, and Codex CLI, and one component of AtlasOS "
    "built each unit. Commands and model ids move fast; verify against the current docs.",
)
# A fused unit has no single source talk: drop the "Watch the talk" button.
TEMPLATE = TEMPLATE.replace(
    '<a class="play" href="{{YT_URL}}" target="_blank" rel="noopener"><span class="circ">&#9654;</span> Watch the talk</a>',
    "",
)
TEMPLATE = TEMPLATE.replace(
    "<li><span class=\"ic\">&#128221;</span><span>Code snippets pulled from the talk</span></li>",
    "<li><span class=\"ic\">&#128221;</span><span>The how across Claude Code, Gemini CLI, and Codex CLI</span></li>",
)
TEMPLATE = TEMPLATE.replace("<span>Hands-on capstone</span>", "<span>One AtlasOS build per unit</span>")
# Remove the decorative squiggle SVGs from the hero (both teal and coral).
TEMPLATE = re.sub(r'<svg class="squiggle".*?</svg>', "", TEMPLATE, flags=re.S)
# Body gets a class so part/recap/build pages can use a compact hero.
TEMPLATE = TEMPLATE.replace("<body>", '<body class="{{BODYCLASS}}">', 1)
# Remove the top "Welcome to ..." strip from every page.
TEMPLATE = re.sub(r'<div class="topbar">.*?</div></div>', "", TEMPLATE, count=1, flags=re.S)
# Multi-page nav tweaks: "All lessons" -> "All units"; Capstone link -> this unit's Build page.
TEMPLATE = TEMPLATE.replace(">All lessons</a>", ">All units</a>")
TEMPLATE = TEMPLATE.replace('<a href="#capstone">Capstone</a>', '<a href="{{BUILD_HREF}}">The Build</a>')
TEMPLATE = TEMPLATE.replace('href="#capstone" style="width:100%', 'href="{{BUILD_HREF}}" style="width:100%')
# Footer credits the AI Nativity brand (the curriculum is "Agentic Engineering"; the
# publisher is AI Nativity). The footer brand links to the AI Nativity home.
_UNIT_FOOTER = (
    '<footer class="site"><div class="wrap">'
    '<a class="logo" href="https://ainativity.substack.com" target="_blank" rel="noopener">'
    'AI Nativity<span class="dot">.</span></a>'
    '<span class="fnote">An AI Nativity agentic-engineering curriculum: durable principles, '
    'the how across Claude, Gemini, and OpenAI tooling, and one AtlasOS component built each unit. '
    'Built from a deep-research pass across primary sources; commands, code, and model ids age fast, '
    'so verify against current docs. &copy; 2026 AI Nativity.</span>'
    '</div></footer>'
)
TEMPLATE = re.sub(r'<footer class="site">.*?</footer>', lambda m: _UNIT_FOOTER, TEMPLATE, flags=re.S)

# Extra CSS for the unit outline sidebar and the step indicator.
EXTRA_CSS = r'''
.unit-toc{list-style:none;margin:0;padding:0}
.unit-toc>li{margin:0 0 3px}
.unit-toc>li>a{display:block;color:var(--muted);font-size:13.5px;padding:8px 12px;border-radius:9px;font-weight:600;line-height:1.35}
.unit-toc>li>a:hover{background:#fff;color:var(--ink)}
.unit-toc>li.active>a{background:#fff;color:var(--teal-d);box-shadow:var(--shadow-sm)}
.unit-toc>li.done>a{color:#93a1b0}
.unit-toc .u-sub{list-style:none;margin:3px 0 8px;padding:0 0 0 10px;border-left:2px solid var(--line)}
.unit-toc .u-sub a{display:block;color:var(--muted);font-size:12.5px;padding:4px 10px;border-radius:6px}
.unit-toc .u-sub a:hover{color:var(--ink);background:#fff}
.unit-toc .u-sub a.active{color:var(--teal-d);font-weight:600}
.stepline{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:0 0 26px;padding:0 0 18px;border-bottom:1px solid var(--line)}
.stepline .steptxt{font-family:Poppins,sans-serif;font-size:13px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:var(--teal-d)}
.stepdots{display:flex;gap:6px;align-items:center}
.stepdots i{width:9px;height:9px;border-radius:50%;background:var(--line);display:block}
.stepdots i.done{background:var(--teal)}
.stepdots i.cur{background:var(--coral);box-shadow:0 0 0 4px var(--coral-soft)}
/* Compact hero for part / recap / build pages (full hero only on the Overview). */
.compact .hero .wrap{grid-template-columns:1fr;padding:34px 28px 40px;gap:0}
.compact .hero h1{font-size:31px;margin-bottom:12px}
.compact .hero .lead{font-size:16px;margin-bottom:16px;max-width:48em}
.compact .hero-card,.compact .float-badge,.compact .hero-actions{display:none}
.compact .hero .blob{opacity:.28}
.compact .hero::before{opacity:.16}
'''
TEMPLATE = TEMPLATE.replace("</style>", EXTRA_CSS + "</style>", 1)

PYG_CSS = bl.HtmlFormatter(style="one-dark").get_style_defs(".codehilite")


def slugify(text):
    text = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    return re.sub(r"[\s_]+", "-", text)[:48] or "page"


def accent_title(title):
    """Wrap the last word in the accent span, matching the lesson hero style."""
    bits = title.rsplit(" ", 1)
    if len(bits) == 2:
        return html.escape(bits[0]) + ' <span class="accent">' + html.escape(bits[1]) + "</span>"
    return html.escape(title)


def is_boundary(h2_text):
    t = h2_text.strip()
    if re.match(r"(?i)part\s+\d", t):
        return "part"
    if t.lower().startswith("key takeaways"):
        return "recap"
    if "the build" in t.lower():
        return "build"
    return None


def first_paragraph(md_text):
    for line in md_text.splitlines():
        s = line.strip()
        if not s or s.startswith(("#", ">", "-", "*", "|", "`", "<")):
            continue
        return re.sub(r"\s+", " ", re.sub(r"[*_`]", "", s)).strip()
    return ""


def split_pages(body_src, unit_num, unit_title):
    """Split a unit body into ordered page dicts."""
    pages = []
    cur = {"kind": "overview", "lines": []}
    for line in body_src.splitlines(keepends=True):
        m = re.match(r"##\s+(.+?)\s*$", line)
        kind = is_boundary(m.group(1)) if m else None
        if kind:
            if cur["lines"]:
                pages.append(cur)
            cur = {"kind": kind, "heading": m.group(1).strip(), "lines": []}
            if kind == "part":
                # Strip the "## Part N: ..." line; it becomes the hero title.
                continue
        cur["lines"].append(line)
    if cur["lines"]:
        pages.append(cur)

    out = []
    for i, p in enumerate(pages):
        md = "".join(p["lines"]).strip("\n")
        if p["kind"] == "overview":
            hero_eyebrow = f"Unit {unit_num}"
            hero_title = unit_title
            sidebar_label = "Overview"
            # Lead from "## In one sentence".
            lm = re.search(r"##\s+In one sentence\s*\n+([^\n#]+(?:\n[^\n#]+)*)", md)
            lead = re.sub(r"\s+", " ", lm.group(1)).strip() if lm else first_paragraph(md)
        elif p["kind"] == "part":
            head = p["heading"]
            num_m = re.match(r"(?i)part\s+(\d+)\s*[:.\-]?\s*(.*)", head)
            pnum = num_m.group(1) if num_m else str(i)
            ptitle = (num_m.group(2) if num_m else head).split("(")[0].strip().rstrip(":")
            hero_eyebrow = f"Unit {unit_num} &middot; Part {pnum}"
            hero_title = ptitle
            sidebar_label = f"Part {pnum} &middot; {html.escape(ptitle)}"
            lead = first_paragraph(md)
        elif p["kind"] == "recap":
            hero_eyebrow = f"Unit {unit_num}"
            hero_title = "Recap"
            sidebar_label = "Recap"
            lead = "The key takeaways and the common pitfalls to avoid before you build."
        else:  # build
            hero_eyebrow = f"Unit {unit_num}"
            hero_title = "The Build"
            sidebar_label = "The Build"
            lead = first_paragraph(md) or "The hands-on payoff: build this unit's AtlasOS component."
        out.append({
            "kind": p["kind"], "md": md, "hero_eyebrow": hero_eyebrow,
            "hero_title": hero_title, "sidebar_label": sidebar_label, "lead": lead,
            "slug": f"{i:02d}-" + slugify(hero_title if p["kind"] != "overview" else "overview"),
        })
    return out


def render_body(md_text):
    md = bl.markdown.Markdown(
        extensions=["fenced_code", "tables", "toc", "sane_lists", "attr_list", "codehilite"],
        extension_configs={"codehilite": {"guess_lang": False, "css_class": "codehilite"},
                           "toc": {"toc_depth": "3-3"}},
    )
    body_html = md.convert(md_text)
    # Style the Build heading as the capstone banner with a stable id.
    body_html = re.sub(r'<h2 id="[^"]*"(>\s*(?:\U0001F6E0️?\s*)?The Build)',
                       r'<h2 id="capstone" class="capstone-h"\1', body_html)
    # External links open in a new tab so readers are not pulled out of the course.
    body_html = re.sub(r'<a href="(https?://[^"]+)"',
                       r'<a href="\1" target="_blank" rel="noopener noreferrer"', body_html)
    h3s = re.findall(r'<h3 id="([^"]+)">(.*?)</h3>', body_html, re.S)
    h3s = [(hid, re.sub(r"<[^>]+>", "", txt).strip()) for hid, txt in h3s]
    return body_html, h3s


def unit_outline_html(pages, cur_idx, cur_h3s, unit_title, unit_num):
    items = [f'<p class="toc-title">Unit {unit_num} &middot; {html.escape(unit_title)}</p>',
             '<ul class="unit-toc">']
    for i, p in enumerate(pages):
        cls = "active" if i == cur_idx else ("done" if i < cur_idx else "")
        items.append(f'<li class="{cls}"><a href="{p["slug"]}.html">{p["sidebar_label"]}</a>')
        if i == cur_idx and cur_h3s:
            items.append('<ul class="u-sub">')
            for hid, txt in cur_h3s:
                items.append(f'<li><a href="#{hid}">{html.escape(txt)}</a></li>')
            items.append("</ul>")
        items.append("</li>")
    items.append("</ul>")
    return "\n".join(items)


def step_dots(n, cur):
    dots = "".join(
        f'<i class="{"cur" if i == cur else ("done" if i < cur else "")}"></i>' for i in range(n)
    )
    return (f'<div class="stepline"><span class="steptxt">Step {cur + 1} of {n}</span>'
            f'<span class="stepdots">{dots}</span></div>')


def render_page(page, pages, cur_idx, unit_title, unit_num, build_href, home, prev_link, next_link):
    body_html, h3s = render_body(page["md"])
    body_html = step_dots(len(pages), cur_idx) + body_html
    toc_html = unit_outline_html(pages, cur_idx, h3s, unit_title, unit_num)

    nav = '<nav class="lessonnav">'
    if prev_link:
        nav += (f'<a class="ln prev" href="{html.escape(prev_link["href"])}">'
                f'<span class="dir">&#8592; Previous</span><b>{html.escape(prev_link["title"])}</b></a>')
    nav += f'<a class="ln home" href="{html.escape(home)}"><b>All units</b></a>'
    if next_link:
        nav += (f'<a class="ln next" href="{html.escape(next_link["href"])}">'
                f'<span class="dir">Next &#8594;</span><b>{html.escape(next_link["title"])}</b></a>')
    nav += "</nav>"

    # Progress tracker hooks. One unit = one tracked item (keyed by unit number).
    # The last page of a unit (its Build) carries the visible "mark complete"
    # section; every other page carries an invisible marker so the fixed bottom
    # progress bar still renders. assets/sync.js wires both and injects the bar.
    if cur_idx == len(pages) - 1:
        hook = (f'<section class="lesson-sync" data-lesson-id="{unit_num}" data-home="../index.html">'
                '<div class="ls-inner">'
                f'<button type="button" class="ls-btn" data-lesson-complete>Mark Unit {unit_num} complete</button>'
                '<span class="ls-status" data-sync-status></span></div>'
                '<a class="ls-track" href="../index.html">Your progress &#8594;</a></section>')
    else:
        hook = (f'<div class="ls-marker" data-lesson-id="{unit_num}" '
                'data-home="../index.html" style="display:none"></div>')
    nav = hook + nav
    sync_scripts = ('<script src="../assets/course-data.js"></script>'
                    '<script type="module" src="../assets/sync.js"></script>')

    title_full = f"Unit {unit_num}: {unit_title} &middot; {page['hero_title']}"
    out = (TEMPLATE
            .replace("{{TITLE}}", html.escape(re.sub("&middot;", "·", title_full)))
            .replace("{{BODYCLASS}}", "" if page["kind"] == "overview" else "compact")
            .replace("{{EYEBROW}}", page["hero_eyebrow"])
            .replace("{{HERO_TITLE}}", accent_title(page["hero_title"]))
            .replace("{{LEAD}}", html.escape(page["lead"]))
            .replace("{{SPEAKER}}", f"Unit {unit_num} of {TOTAL_UNITS}")
            .replace("{{TIME}}", f"Step {cur_idx + 1} of {len(pages)}")
            .replace("{{YT_URL}}", "#")
            .replace("{{HOME}}", html.escape(home))
            .replace("{{BUILD_HREF}}", html.escape(build_href))
            .replace("{{NAV}}", nav)
            .replace("{{TOC}}", toc_html)
            .replace("{{BODY}}", body_html)
            .replace("{{PYGMENTS_CSS}}", PYG_CSS))
    return out.replace("</body>", sync_scripts + "</body>", 1)


def unit_meta(md_path):
    raw = pathlib.Path(md_path).read_text()
    m = re.match(r"#\s+(.+)\n", raw)
    title_full = m.group(1).strip() if m else md_path.stem
    body = raw[m.end():] if m else raw
    bm = re.match(r"\s*((?:^>.*\n?)+)", body, re.M)
    if bm:
        body = body[bm.end():]
    nm = re.match(r"(?i)unit\s+(\d+)\s*[:.\-]\s*(.+)", title_full)
    unit_num = int(nm.group(1)) if nm else 0
    unit_title = nm.group(2).strip() if nm else title_full
    return unit_num, unit_title, body


def main():
    unit_files = sorted(COMBINED.glob("unit-*.md"), key=lambda p: p.name)

    # Remove stale output from previous builds: flat per-unit HTML and any
    # existing per-unit page folders (whose page slugs change as titles change).
    for old in COMBINED.glob("unit-*"):
        if old.is_dir():
            shutil.rmtree(old)
        elif old.suffix == ".html":
            old.unlink()

    # Progress-tracker assets. sync.js is the committed engine and is left as-is;
    # sync-config.js is scaffolded only if absent (so a learner's Firebase keys are
    # never clobbered); course-data.js is regenerated in build_index().
    ASSETS.mkdir(parents=True, exist_ok=True)
    if not (ASSETS / "sync-config.js").exists():
        (ASSETS / "sync-config.js").write_text(SYNC_CONFIG_SCAFFOLD)
    if not (ASSETS / "sync.js").exists():
        print("WARNING: combined/assets/sync.js is missing; the tracker will not load.")

    # First pass: build the page model for every unit.
    units = []
    for mdp in unit_files:
        unit_num, unit_title, body = unit_meta(mdp)
        stem = mdp.stem
        pages = split_pages(body, unit_num, unit_title)
        units.append({"stem": stem, "num": unit_num, "title": unit_title, "pages": pages,
                      "dir": COMBINED / stem})

    # Flat ordered list of all pages for cross-unit prev/next.
    flat = []
    for u in units:
        for i, p in enumerate(u["pages"]):
            flat.append((u, i, p))

    total_pages = 0
    for gi, (u, i, p) in enumerate(flat):
        u["dir"].mkdir(parents=True, exist_ok=True)
        build_page = next((pp for pp in u["pages"] if pp["kind"] == "build"), u["pages"][-1])
        build_href = build_page["slug"] + ".html"
        prev_link = next_link = None
        if gi > 0:
            pu, pi, pp = flat[gi - 1]
            href = f'{pp["slug"]}.html' if pu is u else f'../{pu["stem"]}/{pp["slug"]}.html'
            ttl = pp["hero_title"] if pu is u else f'Unit {pu["num"]}: {pu["title"]}'
            prev_link = {"href": href, "title": ttl}
        if gi < len(flat) - 1:
            nu, ni, npg = flat[gi + 1]
            href = f'{npg["slug"]}.html' if nu is u else f'../{nu["stem"]}/{npg["slug"]}.html'
            ttl = npg["hero_title"] if nu is u else f'Unit {nu["num"]}: {nu["title"]}'
            next_link = {"href": href, "title": ttl}
        html_out = render_page(p, u["pages"], i, u["title"], u["num"], build_href,
                               home="../index.html", prev_link=prev_link, next_link=next_link)
        (u["dir"] / f'{p["slug"]}.html').write_text(html_out)
        total_pages += 1

    build_index(units)
    print(f"rendered {total_pages} pages across {len(units)} units")


def build_index(units):
    # The landing page doubles as the progress tracker: live stats, a checkbox on
    # every unit row, a pace/finish projection, backup/restore/reset, and (once
    # assets/sync-config.js is filled in) Google sign-in for cross-device sync. All
    # progress logic lives in assets/sync.js (window.CourseSync); this page renders
    # against it. Every unit is core; none are optional.
    ASSETS.mkdir(parents=True, exist_ok=True)
    course_data = {"course": COURSE_NAME, "coreTotal": len(units), "optionalIds": [],
                   "progressLabel": "Course progress", "progressCta": "View tracker",
                   "sync": {"provider": "firebase"}}
    (ASSETS / "course-data.js").write_text(
        "// Generated by build_combined.py. Do not edit by hand.\n"
        "window.COURSE_DATA = " + json.dumps(course_data) + ";\n")

    rows = ""
    for u in units:
        first = u["pages"][0]["slug"] + ".html"
        href = f'{u["stem"]}/{first}'
        nparts = sum(1 for p in u["pages"] if p["kind"] == "part")
        meta = f'{len(u["pages"])} pages' + (f' &middot; {nparts} parts' if nparts else "")
        rows += (f'<div class="lesson" data-n="{u["num"]}">'
                 f'<span class="box" data-n="{u["num"]}" role="checkbox" aria-checked="false" '
                 f'tabindex="0" aria-label="Mark Unit {u["num"]} complete">&#10003;</span>'
                 f'<a class="lbody" href="{html.escape(href)}">'
                 f'<span class="num">{u["num"]}</span>'
                 f'<span class="ltext"><span class="lt">{html.escape(u["title"])}</span>'
                 f'<span class="ls">{meta}</span></span>'
                 f'<span class="ldate" data-date="{u["num"]}"></span>'
                 f'<span class="arr">&#8594;</span></a></div>')
    n_units = len(units)
    page = _index_page(rows, n_units)
    (COMBINED / "index.html").write_text(page)
    print(f"wrote {COMBINED / 'index.html'}")


# The tracker landing page. Kept in its own helper so the CSS/panel/script live as
# plain strings (no f-string brace escaping). Adapted from the course-builder
# skill's build_index.py, with the combined course's own AtlasOS/AI Nativity hero.
_INDEX_CSS = """
:root{--navy:#0a1a2f;--navy-2:#0f243d;--navy-3:#15314f;--teal:#18c4a0;--teal-d:#0fa385;--coral:#f24d63;--gold:#f5c451;--green:#34d399;--ink:#152230;--muted:#5f6c7b;--line:#e9eef2;--soft:#f4fbf9;--shadow:0 10px 30px rgba(13,30,52,.08)}
*{box-sizing:border-box}
body{margin:0;background:#fff;color:var(--ink);font-family:Inter,system-ui,sans-serif;line-height:1.7;-webkit-font-smoothing:antialiased;overflow-x:hidden}
a{text-decoration:none;color:inherit}
h1,h2{font-family:Poppins,sans-serif;letter-spacing:-.01em}
.wrap{max-width:1100px;margin:0 auto;padding:0 26px}
.hero{position:relative;background:radial-gradient(120% 120% at 80% 0%,var(--navy-3),var(--navy) 60%);color:#eaf1f8;overflow:hidden;text-align:center;padding:80px 0 90px}
.hero::before{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.12) 1.3px,transparent 1.3px);background-size:22px 22px;opacity:.22;mask:radial-gradient(70% 70% at 50% 20%,#000,transparent)}
.blob{position:absolute;border-radius:50%;filter:blur(10px);opacity:.5}
.blob.t{width:240px;height:240px;background:rgba(24,196,160,.30);top:-70px;left:6%}
.blob.c{width:170px;height:170px;background:rgba(242,77,99,.26);bottom:-50px;right:10%}
.hero .in{position:relative;z-index:2}
.eyebrow{display:inline-flex;gap:8px;color:var(--teal);font-weight:600;letter-spacing:.04em;text-transform:uppercase;font-size:14px;margin-bottom:16px}
.hero h1{font-size:52px;line-height:1.08;margin:0 0 16px;color:#fff;font-weight:800}
.hero h1 .a{color:var(--coral)}
.hero p{color:#b9c6d6;font-size:18px;max-width:42em;margin:0 auto 26px}
.hstats{display:flex;gap:34px;justify-content:center;flex-wrap:wrap;margin-top:30px}
.hstat .n{font-family:Poppins;font-weight:800;font-size:30px;color:#fff}
.hstat .l{color:#9fb0c2;font-size:13.5px}
.panel-wrap{max-width:1100px;margin:-52px auto 0;padding:0 26px;position:relative;z-index:5}
.progress-panel{background:var(--navy-2);border:1px solid #1e3a5a;border-radius:20px;padding:24px 24px 22px;box-shadow:0 24px 60px rgba(8,19,31,.35);color:#e8eef6}
.pp-head{display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;margin-bottom:6px}
.pp-title{color:var(--teal);font-weight:700;letter-spacing:.06em;text-transform:uppercase;font-size:.74rem}
.account{display:flex;align-items:center;gap:12px;flex-wrap:wrap;background:var(--navy-3);border:1px solid #1e3a5a;border-radius:12px;padding:9px 13px}
.account .dot{width:9px;height:9px;border-radius:50%;background:#9fb3c8;flex:0 0 auto}
.account.on .dot{background:var(--green)}
.account #acct-msg{color:#9fb3c8;font-size:.85rem}
.account button{background:var(--teal);color:#05202a;border:0;border-radius:9px;padding:7px 13px;font:600 .88rem system-ui;cursor:pointer}
.account button.ghost{background:var(--navy);color:#e8eef6;border:1px solid #1e3a5a}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:13px;margin:16px 0 6px}
.tile{background:var(--navy-3);border:1px solid #1e3a5a;border-radius:14px;padding:14px 15px 12px}
.tile .big{font-size:1.75rem;font-weight:700;line-height:1.1;font-family:Poppins}
.tile .lbl{color:#9fb3c8;font-size:.76rem;margin-top:3px}
.tile.accent .big{color:var(--teal)} .tile.streak .big{color:var(--gold)}
.tile.finish .big{font-size:1.1rem;padding-top:7px}
.barwrap{background:var(--navy-3);border:1px solid #1e3a5a;border-radius:999px;height:15px;overflow:hidden;margin:10px 0 4px}
#bar{height:100%;width:0;background:linear-gradient(90deg,var(--teal),var(--green));transition:width .4s ease}
.barrow{display:flex;justify-content:space-between;color:#9fb3c8;font-size:.8rem}
.pace{display:flex;align-items:center;gap:9px;margin:18px 0 2px;flex-wrap:wrap}
.pace>span{color:#9fb3c8;font-size:.88rem}
.pace button{background:var(--navy-3);color:#e8eef6;border:1px solid #1e3a5a;border-radius:8px;padding:6px 12px;cursor:pointer;font:inherit;font-size:.88rem}
.pace button.on{background:var(--teal);color:#05202a;border-color:var(--teal);font-weight:600}
#pace-note{color:#9fb3c8;font-size:.82rem}
.actions{margin-top:16px;display:flex;gap:9px;flex-wrap:wrap}
.actions button{background:var(--navy-3);color:#e8eef6;border:1px solid #1e3a5a;border-radius:8px;padding:7px 13px;cursor:pointer;font:inherit;font-size:.86rem}
.actions button:hover{border-color:var(--teal)}
.actions button.danger:hover{border-color:var(--coral);color:var(--coral)}
main{padding:0 0 100px}
main.wrap{padding-bottom:100px}
.intro{text-align:center;max-width:44em;margin:48px auto 30px;color:var(--muted)}
.lessons{display:grid;gap:10px;margin-top:8px}
.lesson{display:flex;align-items:center;gap:14px;padding:14px 16px;border:1px solid var(--line);border-radius:14px;transition:.15s;background:#fff;box-shadow:var(--shadow)}
.lesson:hover{border-color:var(--teal)}
.lesson.done{background:linear-gradient(90deg,rgba(24,196,160,.10),#fff 55%)}
.lesson .box{flex:0 0 auto;width:24px;height:24px;border:2px solid var(--line);border-radius:7px;cursor:pointer;display:grid;place-items:center;color:transparent;font-weight:800;font-size:.9rem;user-select:none;transition:.15s}
.lesson .box:hover{border-color:var(--teal)}
.lesson.done .box{background:var(--teal);border-color:var(--teal);color:#04231c}
.lbody{display:flex;align-items:center;gap:16px;flex:1;min-width:0;color:inherit}
.lesson .num{font-family:Poppins;font-weight:800;color:var(--teal);font-size:20px;min-width:34px;text-align:center}
.ltext{display:flex;flex-direction:column;flex:1;min-width:0}
.lt{font-weight:600}
.lesson.done .lt{color:var(--muted);text-decoration:line-through}
.ls{color:var(--muted);font-size:13px}
.ldate{color:var(--muted);font-size:12px;white-space:nowrap}
.arr{color:var(--teal);font-size:20px}
footer{background:var(--navy);color:#aebccb;text-align:center;padding:40px 26px;font-size:14px}
.logo{font-family:Poppins;font-weight:800;font-size:22px;color:#fff}
.logo .d{color:var(--teal)}
dialog{background:var(--navy-2);color:#e8eef6;border:1px solid #1e3a5a;border-radius:12px;max-width:520px;width:92%}
dialog textarea{width:100%;height:150px;background:var(--navy);color:#e8eef6;border:1px solid #1e3a5a;border-radius:8px;padding:10px;font:13px/1.4 ui-monospace,monospace}
dialog p{margin:0 0 8px}
dialog .row{display:flex;gap:8px;justify-content:flex-end;margin-top:10px}
dialog button{background:var(--navy-3);color:#e8eef6;border:1px solid #1e3a5a;border-radius:8px;padding:8px 14px;cursor:pointer;font:inherit}
@media(max-width:700px){.hero h1{font-size:34px}.hero{padding:56px 0 72px}.hstats{gap:22px}.stats{grid-template-columns:repeat(2,1fr)}main.wrap{padding-bottom:64px}}
"""

_INDEX_PANEL = """
<section class="progress-panel" data-progress-home>
  <div class="pp-head">
    <span class="pp-title">&#10022; Your progress</span>
    <div class="account" id="account"><span class="dot"></span><span id="acct-msg">Starting up&hellip;</span><button id="acct-btn" style="display:none"></button></div>
  </div>
  <div class="stats">
    <div class="tile accent"><div class="big" id="s-count">0/0</div><div class="lbl">units done</div></div>
    <div class="tile"><div class="big" id="s-pct">0%</div><div class="lbl">of the course</div></div>
    <div class="tile streak"><div class="big" id="s-streak">0</div><div class="lbl">day streak</div></div>
    <div class="tile finish"><div class="big" id="s-finish">set a pace</div><div class="lbl">projected finish</div></div>
  </div>
  <div class="barwrap"><div id="bar"></div></div>
  <div class="barrow"><span id="b-left"></span><span id="b-week">0 done in the last 7 days</span></div>
  <div class="pace"><span>My pace:</span>
    <button data-p="1">1 / day</button><button data-p="2">2 / day</button>
    <button data-p="3">3 / day</button><button data-p="5">5 / day</button>
    <span id="pace-note"></span>
  </div>
  <div class="actions"><button id="backup">Back up my progress</button><button id="restore">Restore from backup</button><button class="danger" id="reset">Reset all</button></div>
</section>
"""

_INDEX_DIALOG = """
<dialog id="dlg">
  <p id="dlg-msg"></p>
  <textarea id="dlg-text"></textarea>
  <div class="row"><button id="dlg-cancel">Close</button><button id="dlg-ok" style="display:none">Restore</button></div>
</dialog>
"""

_INDEX_SCRIPT = """
const CS = window.CourseSync;
function fmt(iso){ if(!iso) return ""; const [y,m,d]=iso.split("-").map(Number); return new Date(y,m-1,d).toLocaleDateString(undefined,{month:"short",day:"numeric"}); }
function render(){
  document.querySelectorAll(".lesson").forEach(row=>{
    const n=row.getAttribute("data-n"); const done=CS.isDone(n);
    row.classList.toggle("done",done);
    const box=row.querySelector(".box"); if(box) box.setAttribute("aria-checked",done?"true":"false");
    const dd=row.querySelector(".ldate"); if(dd) dd.textContent=done?fmt(CS.dateOf(n)):"";
  });
  updateStats(); paintPace(); paintAccount();
}
function updateStats(){
  const s=CS.stats();
  document.getElementById("s-count").textContent=s.done+"/"+s.total;
  document.getElementById("s-pct").textContent=s.pct+"%";
  document.getElementById("bar").style.width=s.pct+"%";
  const left=s.total-s.done;
  document.getElementById("b-left").textContent=left===0?"All units complete \\u{1F389}":left+" unit"+(left===1?"":"s")+" to go";
  document.getElementById("s-streak").textContent=s.streak;
  document.getElementById("b-week").textContent=s.week+" done in the last 7 days";
  const fin=document.getElementById("s-finish"), pace=CS.state().pace||1;
  if(left===0){ fin.textContent="Done!"; document.getElementById("pace-note").textContent=""; }
  else{ const days=Math.ceil(left/pace); const d=new Date(); d.setDate(d.getDate()+days);
    fin.textContent=d.toLocaleDateString(undefined,{month:"short",day:"numeric",year:"numeric"});
    document.getElementById("pace-note").textContent="at "+pace+"/day, about "+days+" day"+(days===1?"":"s")+" left"; }
}
function paintPace(){ document.querySelectorAll(".pace button").forEach(b=>b.classList.toggle("on",+b.dataset.p===(CS.state().pace||1))); }
function paintAccount(){
  const box=document.getElementById("account"), msg=document.getElementById("acct-msg"), btn=document.getElementById("acct-btn");
  const u=CS.user();
  box.classList.toggle("on",!!u);
  if(!CS.configured()){ msg.textContent="Progress is saved in this browser. Set up sync to follow you across devices."; btn.style.display="none"; }
  else if(u){ msg.textContent="Synced as "+(u.name||u.email||"you")+"."; btn.style.display=""; btn.textContent="Sign out"; btn.className="ghost"; }
  else{ msg.textContent="Sign in to sync across your laptop and phone."; btn.style.display=""; btn.textContent="Sign in with Google"; btn.className=""; }
}
document.querySelectorAll(".box").forEach(b=>{
  const n=b.getAttribute("data-n");
  b.addEventListener("click",e=>{ e.preventDefault(); CS.toggleLesson(n); });
  b.addEventListener("keydown",e=>{ if(e.key===" "||e.key==="Enter"){ e.preventDefault(); CS.toggleLesson(n); } });
});
document.querySelectorAll(".pace button").forEach(b=>b.addEventListener("click",()=>CS.setPace(+b.dataset.p)));
document.getElementById("acct-btn").addEventListener("click",()=>{ CS.user()?CS.signOut():CS.signIn(); });
const dlg=document.getElementById("dlg"), dtext=document.getElementById("dlg-text"),
      dmsg=document.getElementById("dlg-msg"), dok=document.getElementById("dlg-ok");
document.getElementById("backup").addEventListener("click",()=>{
  dmsg.textContent="Copy this and keep it safe. Paste it back with Restore to recover your progress.";
  dtext.value=CS.exportData(); dtext.readOnly=true; dok.style.display="none"; dlg.showModal(); dtext.select();
});
document.getElementById("restore").addEventListener("click",()=>{
  dmsg.textContent="Paste a backup here and press Restore. This replaces your current progress.";
  dtext.value=""; dtext.readOnly=false; dok.style.display=""; dlg.showModal();
});
dok.addEventListener("click",()=>{ if(CS.importData(dtext.value.trim())) dlg.close(); else alert("That does not look like a valid backup."); });
document.getElementById("dlg-cancel").addEventListener("click",()=>dlg.close());
document.getElementById("reset").addEventListener("click",()=>{ if(confirm("Clear all progress? Back it up first if you want a copy.")) CS.reset(); });
CS.onChange(render);
render();
"""


def _index_page(rows, n_units):
    return (
        "<!doctype html>\n<html lang=\"en\"><head>\n"
        "<meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        f"<title>{COURSE_NAME} | A model-agnostic, self-paced course</title>\n"
        + FAVICON_LINK + "\n"
        "<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">\n"
        "<link href=\"https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap\" rel=\"stylesheet\">\n"
        "<style>" + _INDEX_CSS + "</style></head>\n<body>\n"
        "<header class=\"hero\"><span class=\"blob t\"></span><span class=\"blob c\"></span>\n"
        "  <div class=\"in wrap\">\n"
        "    <span class=\"eyebrow\">&#10022; Model-agnostic &middot; self-paced</span>\n"
        f"    <h1>{COURSE_NAME}<span class=\"a\">.</span></h1>\n"
        "    <p>Learn the durable principles of agentic engineering, see how to apply each one with Claude Code, Gemini CLI, or Codex CLI, and build one component of a north-star agent platform, AtlasOS, in every unit.</p>\n"
        "    <div class=\"hstats\">\n"
        f"      <div class=\"hstat\"><div class=\"n\">{n_units}</div><div class=\"l\">units</div></div>\n"
        "      <div class=\"hstat\"><div class=\"n\">3</div><div class=\"l\">coding agents</div></div>\n"
        "      <div class=\"hstat\"><div class=\"n\">1</div><div class=\"l\">north-star build</div></div>\n"
        "    </div>\n"
        "  </div>\n"
        "</header>\n"
        "<div class=\"panel-wrap\">" + _INDEX_PANEL + "</div>\n"
        "<main class=\"wrap\">\n"
        "  <div class=\"intro\">Tick a unit when you finish it, or use the &ldquo;Mark complete&rdquo; button on the unit&rsquo;s Build page. Your progress shows here and on every page. Work top to bottom: each unit ends in one component of AtlasOS.</div>\n"
        f"  <div class=\"lessons\">{rows}</div>\n"
        "</main>\n"
        "<footer><div class=\"logo\">AI Nativity<span class=\"d\">.</span></div>\n"
        "<p>An AI Nativity agentic-engineering curriculum. You build one platform, AtlasOS, one component at a time. Built from a deep-research pass across primary sources; commands and model ids age fast, so verify against current docs.</p>\n"
        "<p style=\"margin-top:12px;font-size:13px;opacity:.8\">&copy; 2026 AI Nativity &middot; <a href=\"https://ainativity.substack.com\" target=\"_blank\" rel=\"noopener noreferrer\" style=\"color:#18c4a0\">ainativity.substack.com</a></p></footer>\n"
        + _INDEX_DIALOG +
        "<script src=\"assets/course-data.js\"></script>\n"
        "<script type=\"module\" src=\"assets/sync.js\"></script>\n"
        "<script type=\"module\">" + _INDEX_SCRIPT + "</script>\n"
        "</body></html>"
    )


if __name__ == "__main__":
    main()

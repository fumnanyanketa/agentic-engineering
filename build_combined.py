#!/usr/bin/env python3
"""Build the combined, model-agnostic course from `combined/*.md`.

The combined course is the merged spine: vendor-neutral Agentic Engineering
principles fused with the "how" across coding agents (Claude Code, Gemini CLI,
Codex CLI) and an AtlasOS build per unit. It reuses the lesson HTML template
from `build_lessons_html.py` but strips the single-vendor "Building with Claude"
branding, since this course is model-agnostic.

Usage: python3 build_combined.py
Renders every combined/unit-NN-*.md to combined/unit-NN-*.html (with prev/next/
home links) and writes combined/index.html as the course landing page.
"""
import html
import os
import pathlib
import re

import build_lessons_html as bl

ROOT = pathlib.Path(__file__).resolve().parent
COMBINED = ROOT / "combined"
COURSE_NAME = "Agentic Engineering"
COURSE_TAGLINE = "from zero to agent orchestrator"

# De-brand the shared lesson template: this course is model-agnostic, so the
# "Building with Claude" / "Code with Claude London" framing is replaced, and the
# single "Watch the talk" button (a per-lesson YouTube link) is removed because a
# fused unit has no one source talk.
TEMPLATE = bl.TEMPLATE
TEMPLATE = TEMPLATE.replace("{{TITLE}} | Building with Claude", "{{TITLE}} | " + COURSE_NAME)
TEMPLATE = TEMPLATE.replace(
    "&#10024; Welcome to <b>Building with Claude</b> &middot; a self-paced course",
    "&#10024; Welcome to <b>" + COURSE_NAME + "</b> &middot; a self-paced course",
)
TEMPLATE = TEMPLATE.replace(
    "<span>Code with Claude 2026 &middot; London</span>",
    "<span>Model-agnostic &middot; " + COURSE_TAGLINE + "</span>",
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
# Remove the per-lesson "Watch the talk" play button (two spots: nav-cta area is
# absent here, but the hero has it). A combined unit has no single source talk.
TEMPLATE = TEMPLATE.replace(
    '<a class="play" href="{{YT_URL}}" target="_blank" rel="noopener"><span class="circ">&#9654;</span> Watch the talk</a>',
    "",
)
# The hero "What you'll get" card mentions "Code snippets pulled from the talk" and
# "Watch the talk"; make it model-agnostic.
TEMPLATE = TEMPLATE.replace(
    "<li><span class=\"ic\">&#128221;</span><span>Code snippets pulled from the talk</span></li>",
    "<li><span class=\"ic\">&#128221;</span><span>The how across Claude Code, Gemini CLI, and Codex CLI</span></li>",
)
TEMPLATE = TEMPLATE.replace(
    "<span>Hands-on capstone</span>",
    "<span>One AtlasOS build per unit</span>",
)


def convert(md_path, out_path, home, prev=None, nxt=None):
    """Render one combined unit md to html using the de-branded template.

    Mirrors build_lessons_html.convert but swaps in TEMPLATE and skips the
    speaker/youtube hero fields (a fused unit has no single talk).
    """
    raw = pathlib.Path(md_path).read_text()
    m = re.match(r"#\s+(.+)\n", raw)
    title_full = m.group(1).strip() if m else "Unit"
    body_src = raw[m.end():] if m else raw

    meta_block = ""
    bm = re.match(r"\s*((?:^>.*\n?)+)", body_src, re.M)
    if bm:
        meta_block = bm.group(1)
        body_src = body_src[bm.end():]

    def field(label):
        mm = re.search(r"\*\*" + label + r":?\*\*\s*(.+)", meta_block)
        return mm.group(1).strip() if mm else ""

    time_raw = field("Estimated time")
    time_short = re.sub(r"\s*\(.*\)", "", time_raw).strip() or "90 to 120 min"

    if ": " in title_full:
        eyebrow, hero_title = title_full.split(": ", 1)
    else:
        eyebrow, hero_title = "Unit", title_full
    bits = hero_title.rsplit(" ", 1)
    hero_title_html = (
        html.escape(bits[0]) + ' <span class="accent">' + html.escape(bits[1]) + "</span>"
    ) if len(bits) == 2 else html.escape(hero_title)

    lead = ""
    lm = re.search(r"##\s+In one sentence\s*\n+([^\n#]+(?:\n[^\n#]+)*)", body_src)
    if lm:
        lead = re.sub(r"\s+", " ", lm.group(1)).strip()

    md = bl.markdown.Markdown(
        extensions=["fenced_code", "tables", "toc", "sane_lists", "attr_list", "codehilite"],
        extension_configs={
            "codehilite": {"guess_lang": False, "css_class": "codehilite"},
            "toc": {"toc_depth": "2-3"},
        },
    )
    body_html = md.convert(body_src)
    toc_html = md.toc

    # The combined units use "## 🛠️ The Build" rather than "Capstone"; give that
    # heading the capstone banner styling and a stable id so the hero button reaches it.
    body_html = re.sub(
        r'<h2 id="[^"]*"(>\s*(?:\U0001F6E0️?\s*)?The Build)',
        r'<h2 id="capstone" class="capstone-h"\1',
        body_html,
    )
    toc_html = re.sub(
        r'<a href="#[^"]*"(>\s*(?:\U0001F6E0️?\s*)?The Build)',
        r'<a href="#capstone" class="toc-capstone"\1',
        toc_html,
    )

    nav = '<nav class="lessonnav">'
    if prev:
        nav += (f'<a class="ln prev" href="{html.escape(prev["href"])}">'
                f'<span class="dir">&#8592; Previous</span><b>{html.escape(prev["title"])}</b></a>')
    nav += f'<a class="ln home" href="{html.escape(home)}"><b>All units</b></a>'
    if nxt:
        nav += (f'<a class="ln next" href="{html.escape(nxt["href"])}">'
                f'<span class="dir">Next &#8594;</span><b>{html.escape(nxt["title"])}</b></a>')
    nav += '</nav>'

    pyg_css = bl.HtmlFormatter(style="one-dark").get_style_defs(".codehilite")

    out = (TEMPLATE
           .replace("{{TITLE}}", html.escape(title_full))
           .replace("{{EYEBROW}}", html.escape(eyebrow))
           .replace("{{HERO_TITLE}}", hero_title_html)
           .replace("{{LEAD}}", html.escape(lead))
           .replace("{{SPEAKER}}", "Model-agnostic")
           .replace("{{TIME}}", html.escape(time_short))
           .replace("{{YT_URL}}", "#")
           .replace("{{HOME}}", html.escape(home))
           .replace("{{NAV}}", nav)
           .replace("{{TOC}}", toc_html)
           .replace("{{BODY}}", body_html)
           .replace("{{PYGMENTS_CSS}}", pyg_css))
    pathlib.Path(out_path).write_text(out)
    print(f"wrote {out_path} ({len(out)//1024} KB)")


def unit_title(md_path):
    m = re.match(r"#\s+(.+)\n", pathlib.Path(md_path).read_text())
    return m.group(1).strip() if m else md_path.stem


def main():
    units = sorted(COMBINED.glob("unit-*.md"), key=lambda p: p.name)
    items = [{"md": p, "out": p.with_suffix(".html"), "title": unit_title(p)} for p in units]
    for i, it in enumerate(items):
        prev = ({"title": items[i - 1]["title"], "href": items[i - 1]["out"].name}
                if i > 0 else None)
        nxt = ({"title": items[i + 1]["title"], "href": items[i + 1]["out"].name}
               if i < len(items) - 1 else None)
        convert(str(it["md"]), str(it["out"]), home="index.html", prev=prev, nxt=nxt)
    build_index(items)
    print(f"rendered {len(items)} units")


def build_index(items):
    cards = ""
    for it in items:
        full = it["title"]
        num = ""
        nm = re.match(r"Unit\s+(\d+):\s*(.+)", full)
        label = full
        if nm:
            num = nm.group(1)
            label = nm.group(2)
        cards += (f'<a class="lesson" href="{html.escape(it["out"].name)}">'
                  f'<span class="num">{html.escape(num) or "&#10022;"}</span>'
                  f'<span class="ltext"><span class="lt">{html.escape(label)}</span></span>'
                  f'<span class="arr">&#8594;</span></a>')
    n = len(items)
    page = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{COURSE_NAME} | A model-agnostic, self-paced course</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{{--navy:#0a1a2f;--navy-2:#0f243d;--navy-3:#15314f;--teal:#18c4a0;--teal-d:#0fa385;--coral:#f24d63;--ink:#152230;--muted:#5f6c7b;--line:#e9eef2;--soft:#f4fbf9;--shadow:0 10px 30px rgba(13,30,52,.08)}}
*{{box-sizing:border-box}}
body{{margin:0;background:#fff;color:var(--ink);font-family:Inter,system-ui,sans-serif;line-height:1.7;-webkit-font-smoothing:antialiased;overflow-x:hidden}}
a{{text-decoration:none;color:inherit}}
h1,h2{{font-family:Poppins,sans-serif;letter-spacing:-.01em}}
.wrap{{max-width:1000px;margin:0 auto;padding:0 26px}}
.hero{{position:relative;background:radial-gradient(120% 120% at 80% 0%,var(--navy-3),var(--navy) 60%);color:#eaf1f8;overflow:hidden;text-align:center;padding:80px 0 90px}}
.hero::before{{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.12) 1.3px,transparent 1.3px);background-size:22px 22px;opacity:.22;mask:radial-gradient(70% 70% at 50% 20%,#000,transparent)}}
.blob{{position:absolute;border-radius:50%;filter:blur(10px);opacity:.5}}
.blob.t{{width:240px;height:240px;background:rgba(24,196,160,.30);top:-70px;left:6%}}
.blob.c{{width:170px;height:170px;background:rgba(242,77,99,.26);bottom:-50px;right:10%}}
.hero .in{{position:relative;z-index:2}}
.eyebrow{{display:inline-flex;gap:8px;color:var(--teal);font-weight:600;letter-spacing:.04em;text-transform:uppercase;font-size:14px;margin-bottom:16px}}
.hero h1{{font-size:52px;line-height:1.08;margin:0 0 16px;color:#fff;font-weight:800}}
.hero h1 .a{{color:var(--coral)}}
.hero p{{color:#b9c6d6;font-size:18px;max-width:42em;margin:0 auto 26px}}
.stats{{display:flex;gap:34px;justify-content:center;flex-wrap:wrap;margin-top:30px}}
.stat .n{{font-family:Poppins;font-weight:800;font-size:30px;color:#fff}}
.stat .l{{color:#9fb0c2;font-size:13.5px}}
main{{padding:92px 0 150px}}
.intro{{text-align:center;max-width:44em;margin:0 auto 56px;color:var(--muted)}}
.lessons{{display:grid;gap:10px;margin-top:8px}}
.lesson{{display:flex;align-items:center;gap:16px;padding:16px 18px;border:1px solid var(--line);border-radius:14px;transition:.15s;background:#fff;box-shadow:var(--shadow)}}
.lesson:hover{{border-color:var(--teal);transform:translateY(-1px)}}
.lesson .num{{font-family:Poppins;font-weight:800;color:var(--teal);font-size:20px;min-width:34px;text-align:center}}
.ltext{{display:flex;flex-direction:column;flex:1;min-width:0}}
.lt{{font-weight:600}}
.arr{{color:var(--teal);font-size:20px}}
footer{{background:var(--navy);color:#aebccb;text-align:center;padding:40px 26px;font-size:14px}}
.logo{{font-family:Poppins;font-weight:800;font-size:22px;color:#fff}}
.logo .d{{color:var(--teal)}}
@media(max-width:700px){{.hero h1{{font-size:34px}}.hero{{padding:56px 0 64px}}}}
</style></head>
<body>
<header class="hero"><span class="blob t"></span><span class="blob c"></span>
  <div class="in wrap">
    <span class="eyebrow">&#10022; Model-agnostic &middot; self-paced</span>
    <h1>{COURSE_NAME}<span class="a">.</span></h1>
    <p>Learn the durable principles of agentic engineering, see how to apply each one with Claude Code, Gemini CLI, or Codex CLI, and build one component of a north-star agent platform, AtlasOS, in every unit.</p>
    <div class="stats">
      <div class="stat"><div class="n">{n}</div><div class="l">units</div></div>
      <div class="stat"><div class="n">3</div><div class="l">coding agents</div></div>
      <div class="stat"><div class="n">1</div><div class="l">north-star build</div></div>
    </div>
  </div>
</header>
<main class="wrap">
  <div class="intro">Work top to bottom. Each unit states one principle, shows how to apply it with your chosen coding agent (and how the others do it), and ends in one component of AtlasOS.</div>
  <div class="lessons">{cards}</div>
</main>
<footer><div class="logo">{COURSE_NAME}<span class="d">.</span></div>
<p>A model-agnostic, self-paced course. You build one platform, AtlasOS, one component at a time. Commands and model ids move fast; verify against current docs.</p></footer>
</body></html>'''
    out = COMBINED / "index.html"
    out.write_text(page)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()

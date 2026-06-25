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
import pathlib
import re
import shutil

import build_lessons_html as bl

ROOT = pathlib.Path(__file__).resolve().parent
COMBINED = ROOT / "combined"
COURSE_NAME = "Agentic Engineering"
TOTAL_UNITS = 11

# ---------------------------------------------------------------------------
# De-brand the shared lesson template (model-agnostic course) and adapt a few
# anchors/links for the multi-page layout.
# ---------------------------------------------------------------------------
TEMPLATE = bl.TEMPLATE
TEMPLATE = TEMPLATE.replace("{{TITLE}} | Building with Claude", "{{TITLE}} | " + COURSE_NAME)
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

    title_full = f"Unit {unit_num}: {unit_title} &middot; {page['hero_title']}"
    return (TEMPLATE
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
    cards = ""
    for u in units:
        first = u["pages"][0]["slug"] + ".html"
        href = f'{u["stem"]}/{first}'
        nparts = sum(1 for p in u["pages"] if p["kind"] == "part")
        meta = f'{len(u["pages"])} pages' + (f' &middot; {nparts} parts' if nparts else "")
        cards += (f'<a class="lesson" href="{html.escape(href)}">'
                  f'<span class="num">{u["num"]}</span>'
                  f'<span class="ltext"><span class="lt">{html.escape(u["title"])}</span>'
                  f'<span class="ls">{meta}</span></span>'
                  f'<span class="arr">&#8594;</span></a>')
    n_units = len(units)
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
.hero{{position:relative;background:radial-gradient(120% 120% at 80% 0%,var(--navy-3),var(--navy) 60%);color:#eaf1f8;overflow:hidden;text-align:center;padding:80px 26px 90px}}
.hero::before{{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.12) 1.3px,transparent 1.3px);background-size:22px 22px;opacity:.22;mask:radial-gradient(70% 70% at 50% 20%,#000,transparent)}}
.blob{{position:absolute;border-radius:50%;filter:blur(10px);opacity:.5}}
.blob.t{{width:240px;height:240px;background:rgba(24,196,160,.30);top:-70px;left:6%}}
.blob.c{{width:170px;height:170px;background:rgba(242,77,99,.26);bottom:-50px;right:10%}}
.hero .in{{position:relative;z-index:2;max-width:760px;margin:0 auto}}
.eyebrow{{display:inline-flex;gap:8px;color:var(--teal);font-weight:600;letter-spacing:.04em;text-transform:uppercase;font-size:14px;margin-bottom:16px}}
.hero h1{{font-size:52px;line-height:1.08;margin:0 0 16px;color:#fff;font-weight:800}}
.hero h1 .a{{color:var(--coral)}}
.hero p{{color:#b9c6d6;font-size:18px;max-width:42em;margin:0 auto 26px}}
.stats{{display:flex;gap:34px;justify-content:center;flex-wrap:wrap;margin-top:30px}}
.stat .n{{font-family:Poppins;font-weight:800;font-size:30px;color:#fff}}
.stat .l{{color:#9fb0c2;font-size:13.5px}}
.content{{max-width:1000px;margin:0 auto;padding:128px 26px 200px}}
.intro{{text-align:center;max-width:44em;margin:0 auto 64px;color:var(--muted)}}
.lessons{{display:grid;gap:10px;margin-top:8px}}
.lesson{{display:flex;align-items:center;gap:16px;padding:16px 18px;border:1px solid var(--line);border-radius:14px;transition:.15s;background:#fff;box-shadow:var(--shadow)}}
.lesson:hover{{border-color:var(--teal);transform:translateY(-1px)}}
.lesson .num{{font-family:Poppins;font-weight:800;color:var(--teal);font-size:20px;min-width:34px;text-align:center}}
.ltext{{display:flex;flex-direction:column;flex:1;min-width:0}}
.lt{{font-weight:600}}
.ls{{color:var(--muted);font-size:13px}}
.arr{{color:var(--teal);font-size:20px}}
footer{{background:var(--navy);color:#aebccb;text-align:center;padding:40px 26px;font-size:14px}}
.logo{{font-family:Poppins;font-weight:800;font-size:22px;color:#fff}}
.logo .d{{color:var(--teal)}}
@media(max-width:700px){{.hero h1{{font-size:34px}}.hero{{padding:56px 22px 64px}}.content{{padding:72px 22px 120px}}}}
</style></head>
<body>
<header class="hero"><span class="blob t"></span><span class="blob c"></span>
  <div class="in">
    <span class="eyebrow">&#10022; Model-agnostic &middot; self-paced</span>
    <h1>{COURSE_NAME}<span class="a">.</span></h1>
    <p>Learn the durable principles of agentic engineering, see how to apply each one with Claude Code, Gemini CLI, or Codex CLI, and build one component of a north-star agent platform, AtlasOS, in every unit.</p>
    <div class="stats">
      <div class="stat"><div class="n">{n_units}</div><div class="l">units</div></div>
      <div class="stat"><div class="n">3</div><div class="l">coding agents</div></div>
      <div class="stat"><div class="n">1</div><div class="l">north-star build</div></div>
    </div>
  </div>
</header>
<div class="content">
  <div class="intro">Work top to bottom. Each unit is split into short pages, one per part, so you can feel the progress: read a part, click Next, keep going. Every unit ends in one component of AtlasOS.</div>
  <div class="lessons">{cards}</div>
</div>
<footer><div class="logo">AI Nativity<span class="d">.</span></div>
<p>An AI Nativity agentic-engineering curriculum. You build one platform, AtlasOS, one component at a time. Built from a deep-research pass across primary sources; commands and model ids age fast, so verify against current docs.</p>
<p style="margin-top:12px;font-size:13px;opacity:.8">&copy; 2026 AI Nativity &middot; <a href="https://ainativity.substack.com" target="_blank" rel="noopener noreferrer" style="color:#18c4a0">ainativity.substack.com</a></p></footer>
</body></html>'''
    (COMBINED / "index.html").write_text(page)
    print(f"wrote {COMBINED / 'index.html'}")


if __name__ == "__main__":
    main()

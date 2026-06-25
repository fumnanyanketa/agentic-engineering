#!/usr/bin/env python3
"""Build the whole course: render every lesson (with prev/next/home links) and the index.

Usage: python3 build_course.py
"""
import os
import pathlib
import re
import subprocess
import sys

import build_lessons_html as bl

ROOT = pathlib.Path(__file__).resolve().parent
LESSONS = ROOT / "lessons"
OUT_ROOT = ROOT / "lessons-html"

items = []
for md in LESSONS.glob("*/*.md"):
    text = md.read_text()
    m = re.match(r"#\s+Module\s+\d+\s+·\s+Lesson\s+(\d+):\s+(.+)", text)
    if not m:
        print("skip (no H1 match):", md)
        continue
    num = int(m.group(1))
    title = m.group(2).strip()
    out = OUT_ROOT / md.relative_to(LESSONS)
    out = out.with_suffix(".html")
    items.append({"num": num, "title": title, "md": md, "out": out})

items.sort(key=lambda x: x["num"])

for i, it in enumerate(items):
    it["out"].parent.mkdir(parents=True, exist_ok=True)
    prev = None
    nxt = None
    if i > 0:
        p = items[i - 1]
        prev = {"title": p["title"], "href": os.path.relpath(p["out"], it["out"].parent)}
    if i < len(items) - 1:
        n = items[i + 1]
        nxt = {"title": n["title"], "href": os.path.relpath(n["out"], it["out"].parent)}
    home = os.path.relpath(OUT_ROOT / "index.html", it["out"].parent)
    bl.convert(str(it["md"]), str(it["out"]), home=home, prev=prev, nxt=nxt)

print(f"rendered {len(items)} lessons")

# Rebuild the landing page.
subprocess.run([sys.executable, str(ROOT / "build_index.py")], check=True)

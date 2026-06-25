#!/usr/bin/env python3
"""Build a polished, LMS-style HTML lesson page from a course markdown file.

Usage:  python3 build_lessons_html.py <input.md> <output.html>

Visual style: friendly modern learning-platform look. Dark navy hero with teal
and coral accents, rounded floating cards, sparkle and squiggle motifs, clean
white content area. Interactive: sticky TOC + scrollspy, reading progress,
copy buttons, styled callouts, check-off for objectives and milestones.
One template builds all 37 lessons consistently.
"""
import html
import pathlib
import re
import sys

import markdown
from pygments.formatters import HtmlFormatter

TEMPLATE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{TITLE}} | Building with Claude</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{
  --navy:#0a1a2f; --navy-2:#0f243d; --navy-3:#15314f;
  --teal:#18c4a0; --teal-d:#0fa385; --teal-soft:#e4f8f2;
  --coral:#f24d63; --coral-d:#d83a50; --coral-soft:#feecee;
  --ink:#152230; --muted:#5f6c7b; --line:#e9eef2; --bg:#ffffff;
  --soft:#f4fbf9; --card:#ffffff; --code-bg:#21252b; --max:780px;
  --k:#2f8fb3; --k-bg:#e8f4f9; --tip:#c4881f; --tip-bg:#fdf4e3; --ok:#1f9d6b; --ok-bg:#e6f6ef;
  --no:#e0533f; --no-bg:#fdecea; --goal:#7b54c9; --goal-bg:#f1ebfb;
  --shadow:0 10px 30px rgba(13,30,52,.08); --shadow-sm:0 4px 14px rgba(13,30,52,.07);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,sans-serif;line-height:1.72;font-size:17px;-webkit-font-smoothing:antialiased;overflow-x:hidden}
#progress{position:fixed;top:0;left:0;height:4px;width:0;background:linear-gradient(90deg,var(--teal),var(--coral));z-index:200;transition:width .1s linear}
a{color:var(--teal-d);text-decoration:none}
a:hover{color:var(--coral)}
h1,h2,h3{font-family:Poppins,sans-serif;color:var(--ink);letter-spacing:-.01em}
.accent{color:var(--coral)}
.wrap{max-width:1200px;margin:0 auto;padding:0 28px}

/* ---------- Top welcome strip ---------- */
.topbar{background:var(--navy);color:#cdd8e4;font-size:13.5px}
.topbar .wrap{display:flex;justify-content:space-between;align-items:center;height:42px;gap:18px}
.topbar b{color:#fff;font-weight:600}
.topbar .right{display:flex;gap:18px;align-items:center}
.topbar a{color:#cdd8e4}.topbar a:hover{color:var(--teal)}

/* ---------- Nav ---------- */
nav.bar{background:var(--navy-2);position:sticky;top:0;z-index:120;box-shadow:0 2px 20px rgba(0,0,0,.25)}
nav.bar .wrap{display:flex;align-items:center;height:68px;gap:26px}
.logo{font-family:Poppins;font-weight:800;font-size:22px;color:#fff;letter-spacing:.02em;cursor:pointer;text-decoration:none}
a.logo:hover{color:var(--teal)}
.lessonnav{display:flex;gap:14px;align-items:stretch;margin:60px 0 0;flex-wrap:wrap}
.lessonnav .ln{flex:1;min-width:200px;display:flex;flex-direction:column;gap:3px;border:1px solid var(--line);border-radius:14px;padding:16px 18px;color:var(--muted);transition:.15s;background:#fff}
.lessonnav .ln:hover{border-color:var(--teal);box-shadow:var(--shadow-sm);transform:translateY(-1px)}
.lessonnav .ln .dir{font-size:13px;font-weight:600;color:var(--teal-d)}
.lessonnav .ln b{color:var(--ink);font-family:Poppins;font-size:15px}
.lessonnav .ln.next{text-align:right}
.lessonnav .ln.home{flex:0 0 auto;justify-content:center;align-items:center;text-align:center;background:var(--soft)}
.lessonnav .ln.home b{color:var(--teal-d)}
.logo .dot{color:var(--teal)}
.navlinks{display:flex;gap:24px;margin-left:8px}
.navlinks a{color:#dde6ef;font-weight:500;font-size:15px}
.navlinks a:hover{color:var(--teal)}
.nav-cta{margin-left:auto;display:flex;gap:12px;align-items:center}
.btn{display:inline-flex;align-items:center;gap:9px;border:none;cursor:pointer;font-family:Inter;font-weight:600;border-radius:999px;transition:.18s;font-size:15px;text-decoration:none}
.btn-primary{background:var(--teal);color:#04231c;padding:12px 22px}
.btn-primary:hover{background:var(--teal-d);color:#fff;transform:translateY(-1px)}
.btn-outline{background:transparent;color:#fff;border:1.5px solid rgba(255,255,255,.35);padding:10px 20px}
.btn-outline:hover{border-color:var(--teal);color:var(--teal)}
.btn-coral{background:var(--coral);color:#fff;padding:12px 22px}
.btn-coral:hover{background:var(--coral-d);color:#fff;transform:translateY(-1px)}

/* ---------- Hero ---------- */
.hero{position:relative;background:radial-gradient(120% 120% at 80% 0%,var(--navy-3),var(--navy) 60%);color:#eaf1f8;overflow:hidden}
.hero::before{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.12) 1.3px,transparent 1.3px);background-size:22px 22px;opacity:.25;mask:radial-gradient(60% 60% at 20% 30%,#000,transparent)}
.blob{position:absolute;border-radius:50%;filter:blur(8px);opacity:.5;z-index:0}
.blob.t{width:230px;height:230px;background:rgba(24,196,160,.30);top:-60px;right:8%}
.blob.c{width:160px;height:160px;background:rgba(242,77,99,.28);bottom:-40px;left:42%}
.squiggle{position:absolute;z-index:1;opacity:.85}
.hero .wrap{position:relative;z-index:2;display:grid;grid-template-columns:1.15fr .85fr;gap:48px;align-items:center;padding:70px 28px 90px}
.eyebrow{display:inline-flex;align-items:center;gap:8px;color:var(--teal);font-weight:600;font-size:14px;letter-spacing:.03em;text-transform:uppercase;margin-bottom:18px}
.hero h1{font-size:54px;line-height:1.08;font-weight:800;margin:0 0 20px;color:#fff}
.hero .lead{font-size:18px;color:#b9c6d6;max-width:34em;margin:0 0 30px}
.hero-actions{display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin-bottom:30px}
.play{display:inline-flex;align-items:center;gap:12px;color:#fff;font-weight:600}
.play .circ{width:52px;height:52px;border-radius:50%;background:var(--coral);display:grid;place-items:center;box-shadow:0 8px 22px rgba(242,77,99,.45);font-size:16px;animation:pulse 2.4s infinite}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(242,77,99,.45)}70%{box-shadow:0 0 0 16px rgba(242,77,99,0)}100%{box-shadow:0 0 0 0 rgba(242,77,99,0)}}
.chips{display:flex;gap:10px;flex-wrap:wrap}
.chip{display:inline-flex;align-items:center;gap:7px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);color:#dce6f0;padding:8px 14px;border-radius:999px;font-size:13.5px;font-weight:500}
.chip b{color:#fff}
/* hero card */
.hero-card{position:relative;background:#fff;color:var(--ink);border-radius:22px;padding:26px;box-shadow:0 24px 60px rgba(0,0,0,.35)}
.hero-card .ring{position:absolute;top:-26px;right:-18px;width:96px;height:96px;background:#fff;border-radius:50%;box-shadow:var(--shadow);display:grid;place-items:center}
.hero-card .ring svg{transform:rotate(-90deg)}
.hero-card .ring .lab{position:absolute;font-family:Poppins;font-weight:700;font-size:18px;color:var(--teal-d)}
.hero-card h3{margin:4px 0 14px;font-size:19px}
.hero-card ul{list-style:none;margin:0 0 18px;padding:0}
.hero-card li{display:flex;gap:11px;align-items:flex-start;padding:9px 0;border-bottom:1px dashed var(--line);font-size:14.5px;color:#36424f}
.hero-card li:last-child{border-bottom:none}
.hero-card li .ic{font-size:17px;line-height:1.4}
.float-badge{position:absolute;left:18px;bottom:-26px;background:#fff;border-radius:14px;box-shadow:var(--shadow);padding:12px 16px;display:flex;gap:10px;align-items:center;font-size:13px;font-weight:600;color:var(--ink)}
.float-badge .n{font-family:Poppins;font-weight:800;color:var(--coral);font-size:20px}

/* ---------- Content layout ---------- */
.layout{display:grid;grid-template-columns:268px minmax(0,1fr);gap:46px;max-width:1200px;margin:0 auto;padding:0 28px}
aside{position:sticky;top:84px;align-self:start;height:calc(100vh - 100px);overflow-y:auto;padding:26px 0}
.toc-card{background:var(--soft);border:1px solid var(--line);border-radius:18px;padding:18px}
.toc-close{display:none;position:absolute;top:-6px;right:-4px;width:36px;height:36px;border:none;background:var(--navy-2);color:#fff;border-radius:50%;font-size:22px;line-height:1;cursor:pointer}
.toc-close:hover{background:var(--coral)}
.toc-title{font-family:Poppins;font-size:12px;text-transform:uppercase;letter-spacing:.1em;color:var(--teal-d);margin:0 0 10px;font-weight:700}
.toc ul{list-style:none;margin:0;padding:0}
.toc a{display:block;color:var(--muted);font-size:14px;padding:6px 12px;border-radius:8px;border-left:2px solid transparent;line-height:1.4}
.toc a:hover{color:var(--ink);background:#fff}
.toc a.active{color:var(--teal-d);background:#fff;border-left-color:var(--teal);font-weight:600}
.toc .toc li li a{padding-left:24px;font-size:13px}
.toc a.toc-capstone{color:var(--coral);font-weight:600}
main{padding:54px 0 120px;min-width:0}
article{max-width:var(--max)}

/* typography */
article h2{font-size:30px;margin:56px 0 16px;font-weight:700;position:relative}
article h2::before{content:"\2726";color:var(--teal);font-size:18px;margin-right:10px;vertical-align:2px}
article h3{font-size:21px;margin:34px 0 10px;font-weight:600}
article h2+h3{margin-top:18px}
article p,article li{font-size:16.5px}
article ul,article ol{padding-left:24px}
article li{margin:7px 0}
article strong{font-weight:700;color:#0f1b28}
hr{border:none;height:1px;background:var(--line);margin:42px 0}

/* tables */
table{border-collapse:separate;border-spacing:0;width:100%;margin:24px 0;font-size:15px;border:1px solid var(--line);border-radius:14px;overflow:hidden;display:block;overflow-x:auto}
th,td{padding:12px 15px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}
th{background:var(--navy-2);color:#eaf1f8;font-family:Poppins;font-weight:600;font-size:14px}
tr:last-child td{border-bottom:none}
tbody tr:nth-child(even){background:var(--soft)}

/* inline + block code */
code{font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;font-size:.86em;background:var(--teal-soft);color:#0c6a55;padding:.13em .42em;border-radius:6px}
.codehilite,pre{position:relative;background:var(--code-bg);border-radius:14px;margin:22px 0;overflow:hidden;box-shadow:var(--shadow-sm)}
.codehilite pre{margin:0;border-radius:0;box-shadow:none;background:transparent}
.codehilite pre,pre>code{display:block;padding:42px 18px 18px;overflow-x:auto}
.codehilite code,pre code{background:none;color:#dfe6ee;padding:0;font-size:13.5px;line-height:1.7}
.code-bar{position:absolute;top:0;left:0;right:0;height:34px;display:flex;align-items:center;gap:7px;padding:0 15px;background:rgba(255,255,255,.05);border-bottom:1px solid rgba(255,255,255,.07)}
.code-bar .dot{width:11px;height:11px;border-radius:50%}
.dot.r{background:#ff5f57}.dot.y{background:#febc2e}.dot.g{background:#28c840}
.copy-btn{position:absolute;top:5px;right:9px;z-index:3;background:rgba(255,255,255,.08);color:#dfe6ee;border:1px solid rgba(255,255,255,.14);border-radius:8px;font-size:12px;padding:4px 11px;cursor:pointer;font-family:Inter;transition:.15s}
.copy-btn:hover{background:var(--teal);border-color:var(--teal);color:#04231c}
.copy-btn.done{background:var(--teal);color:#04231c;border-color:var(--teal)}

/* callouts */
blockquote{margin:24px 0;padding:16px 20px;border-radius:14px;background:var(--soft);border:1px solid var(--line);border-left:5px solid var(--teal)}
blockquote p{margin:7px 0}blockquote p:first-child{margin-top:0}blockquote p:last-child{margin-bottom:0}
blockquote.cl-key{background:var(--k-bg);border-left-color:var(--k);border-color:transparent}
blockquote.cl-tip{background:var(--tip-bg);border-left-color:var(--tip);border-color:transparent}
blockquote.cl-ok{background:var(--ok-bg);border-left-color:var(--ok);border-color:transparent}
blockquote.cl-no{background:var(--no-bg);border-left-color:var(--no);border-color:transparent}
blockquote.cl-goal{background:var(--goal-bg);border-left-color:var(--goal);border-color:transparent}

/* capstone banner */
h2.capstone-h{background:linear-gradient(115deg,var(--navy),var(--navy-3));color:#fff;border-radius:20px;padding:30px 28px 26px;margin-top:64px;box-shadow:0 20px 50px rgba(10,26,47,.3);overflow:hidden;position:relative}
h2.capstone-h::before{content:"\1F6E0  HANDS-ON PROJECT";display:block;font-family:Poppins;font-size:12px;font-weight:700;letter-spacing:.14em;color:var(--teal);margin:0 0 8px}
h2.capstone-h::after{content:"";position:absolute;width:150px;height:150px;border-radius:50%;background:rgba(24,196,160,.25);filter:blur(10px);top:-50px;right:-30px}

/* check-off */
.checkable{list-style:none;padding-left:0}
.checkable li{position:relative;padding-left:36px;cursor:pointer;margin:9px 0}
.checkable li::before{content:"";position:absolute;left:0;top:3px;width:22px;height:22px;border:2px solid var(--teal);border-radius:7px;background:#fff;transition:.15s}
.checkable li.checked::before{background:var(--teal);border-color:var(--teal)}
.checkable li.checked::after{content:"\2713";position:absolute;left:5px;top:1px;color:#fff;font-weight:800;font-size:15px}
.checkable li.checked{color:var(--muted)}

/* footer */
footer.site{background:var(--navy);color:#aebccb;margin-top:90px}
footer.site .wrap{padding:46px 28px;display:flex;justify-content:space-between;gap:26px;flex-wrap:wrap;align-items:center}
footer.site .logo{font-size:20px}
footer.site .fnote{max-width:46em;font-size:13.5px;line-height:1.7}

#menuBtn{display:none}
@media(max-width:920px){
  .topbar{display:none}
  .nav-cta{display:none}
  .float-badge{display:none}
  nav.bar .wrap{gap:14px;height:60px}
  .wrap{padding:0 20px}
  .logo{font-size:18px;white-space:nowrap}
  .hero .wrap{grid-template-columns:1fr;gap:30px;padding:42px 20px 56px}
  .hero h1{font-size:33px}
  .hero .lead{font-size:16.5px}
  .hero-actions{gap:14px}
  .hero-actions .btn-primary{flex:1;justify-content:center}
  .layout{grid-template-columns:1fr;gap:0}
  aside{position:fixed;top:0;left:0;width:84vw;max-width:320px;height:100vh;background:#fff;z-index:130;transform:translateX(-100%);transition:.25s;box-shadow:var(--shadow);padding:24px}
  aside.open{transform:none}
  #menuBtn{display:inline-flex}
  .toc-close{display:block}
  .navlinks{display:none}
  main{padding:34px 0 80px}
  body{font-size:16px}
  article h2{font-size:25px}
  h2.capstone-h{padding:24px 20px}
}
@media(max-width:420px){
  .hero h1{font-size:29px}
  .hero-actions{flex-direction:column;align-items:stretch}
  .hero-actions .play{justify-content:center}
}
</style>
</head>
<body>
<div id="progress"></div>

<div class="topbar"><div class="wrap">
  <div>&#10024; Welcome to <b>Building with Claude</b> &middot; a self-paced course</div>
  <div class="right"><span>Code with Claude 2026 &middot; London</span></div>
</div></div>

<nav class="bar"><div class="wrap">
  <button class="btn btn-outline" id="menuBtn" style="padding:8px 14px">&#9776;</button>
  <a class="logo" href="{{HOME}}">Building with Claude<span class="dot">.</span></a>
  <div class="navlinks">
    <a href="{{HOME}}">All lessons</a>
    <a href="#overview">Overview</a>
    <a href="#capstone">Capstone</a>
  </div>
  <div class="nav-cta">
    <a class="btn btn-primary" href="#start">Start the lesson &#8594;</a>
  </div>
</div></nav>

<header class="hero">
  <span class="blob t"></span><span class="blob c"></span>
  <svg class="squiggle" style="top:120px;left:46%;" width="90" height="26" viewBox="0 0 90 26" fill="none"><path d="M2 13c8-14 16 14 24 0s16 14 24 0 16 14 24 0" stroke="#18c4a0" stroke-width="4" stroke-linecap="round"/></svg>
  <svg class="squiggle" style="bottom:60px;right:40%;" width="70" height="22" viewBox="0 0 90 26" fill="none"><path d="M2 13c8-14 16 14 24 0s16 14 24 0 16 14 24 0" stroke="#f24d63" stroke-width="4" stroke-linecap="round"/></svg>
  <div class="wrap" id="overview">
    <div>
      <span class="eyebrow">&#10022; {{EYEBROW}}</span>
      <h1>{{HERO_TITLE}}</h1>
      <p class="lead">{{LEAD}}</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="#start">Start the lesson &#8594;</a>
        <a class="play" href="{{YT_URL}}" target="_blank" rel="noopener"><span class="circ">&#9654;</span> Watch the talk</a>
      </div>
      <div class="chips">
        <span class="chip">&#127908; <b>{{SPEAKER}}</b></span>
        <span class="chip">&#9201; <b>{{TIME}}</b></span>
        <span class="chip">&#128296; <b>Hands-on capstone</b></span>
      </div>
    </div>
    <div style="position:relative">
      <div class="hero-card">
        <div class="ring">
          <svg width="74" height="74"><circle cx="37" cy="37" r="31" stroke="#eef2f5" stroke-width="7" fill="none"/><circle cx="37" cy="37" r="31" stroke="#18c4a0" stroke-width="7" fill="none" stroke-linecap="round" stroke-dasharray="195" stroke-dashoffset="40"/></svg>
          <span class="lab">&#10022;</span>
        </div>
        <h3>What you&#39;ll get</h3>
        <ul>
          <li><span class="ic">&#9989;</span><span>Plain-language teaching with every term defined</span></li>
          <li><span class="ic">&#128221;</span><span>Code snippets pulled from the talk</span></li>
          <li><span class="ic">&#128296;</span><span>A hands-on capstone you build step by step</span></li>
          <li><span class="ic">&#127919;</span><span>Optional practice drills to reinforce each skill</span></li>
        </ul>
        <a class="btn btn-coral" href="#capstone" style="width:100%;justify-content:center">Jump to the project</a>
      </div>
    </div>
  </div>
</header>

<div class="layout">
  <aside id="sidebar"><div class="toc-card">
    <button class="toc-close" id="tocClose" aria-label="Close menu">&times;</button>
    <p class="toc-title">On this page</p>
    {{TOC}}
  </div></aside>
  <main id="start">
    <article>
      {{BODY}}
    </article>
    {{NAV}}
  </main>
</div>

<footer class="site"><div class="wrap">
  <a class="logo" href="{{HOME}}">Building with Claude<span class="dot">.</span></a>
  <span class="fnote">A self-paced course generated from the Code with Claude 2026 (London) talks. Code snippets are illustrative reconstructions of the approaches shown. Adapt them to the current SDK.</span>
</div></footer>

<style>{{PYGMENTS_CSS}}</style>
<script>
// mobile menu
const sb=document.getElementById('sidebar'),mb=document.getElementById('menuBtn');
if(mb){mb.onclick=()=>sb.classList.toggle('open');sb.addEventListener('click',e=>{if(e.target.tagName==='A')sb.classList.remove('open')});}
const tc=document.getElementById('tocClose');if(tc){tc.onclick=()=>sb.classList.remove('open');}
// progress
const prog=document.getElementById('progress');
addEventListener('scroll',()=>{const h=document.body.scrollHeight-innerHeight;prog.style.width=(h>0?scrollY/h*100:0)+'%'});
// code chrome + copy
document.querySelectorAll('.codehilite, pre').forEach(block=>{
  if(block.parentElement.classList.contains('codehilite'))return;
  const bar=document.createElement('div');bar.className='code-bar';
  bar.innerHTML='<span class="dot r"></span><span class="dot y"></span><span class="dot g"></span>';
  block.appendChild(bar);
  const btn=document.createElement('button');btn.className='copy-btn';btn.textContent='Copy';
  btn.onclick=()=>{const t=block.querySelector('code')?.innerText||block.innerText;
    navigator.clipboard.writeText(t.replace(/\nCopy$/,''));btn.textContent='Copied!';btn.classList.add('done');
    setTimeout(()=>{btn.textContent='Copy';btn.classList.remove('done')},1500)};
  block.appendChild(btn);
});
// callouts by leading emoji
const map={'🔑':'cl-key','💡':'cl-tip','✅':'cl-ok','❌':'cl-no','🎯':'cl-goal','🛠':'cl-goal'};
document.querySelectorAll('blockquote').forEach(q=>{const t=(q.textContent||'').trim();for(const e in map){if(t.startsWith(e)){q.classList.add(map[e]);break}}});
// check-off
function makeCheckable(rx){document.querySelectorAll('h2,h3').forEach(h=>{if(!rx.test(h.textContent))return;let el=h.nextElementSibling;
  while(el&&!/^H[1-3]$/.test(el.tagName)){if(el.tagName==='OL'||el.tagName==='UL'){el.classList.add('checkable');
    el.querySelectorAll(':scope>li').forEach(li=>{const key='cwc:'+location.pathname+':'+li.textContent.slice(0,60);
      if(localStorage.getItem(key))li.classList.add('checked');
      li.addEventListener('click',ev=>{if(ev.target.tagName==='A')return;li.classList.toggle('checked');
        li.classList.contains('checked')?localStorage.setItem(key,'1'):localStorage.removeItem(key)});});}el=el.nextElementSibling;}});}
makeCheckable(/learning objectives|milestones/i);
// scrollspy
const links=[...document.querySelectorAll('.toc a')];
const heads=links.map(a=>a.getAttribute('href')).filter(h=>h&&h.startsWith('#')).map(h=>document.getElementById(h.slice(1))).filter(Boolean);
const spy=()=>{let cur=heads[0]?.id;for(const h of heads){if(h.getBoundingClientRect().top<150)cur=h.id}
  links.forEach(a=>a.classList.toggle('active',a.getAttribute('href')==='#'+cur))};
addEventListener('scroll',spy);spy();
</script>
</body>
</html>
'''


def convert(md_path: str, out_path: str, home: str = "../index.html", prev=None, nxt=None) -> None:
    raw = pathlib.Path(md_path).read_text()

    m = re.match(r"#\s+(.+)\n", raw)
    title_full = m.group(1).strip() if m else "Lesson"
    body_src = raw[m.end():] if m else raw

    # Meta block (first blockquote) -> hero fields.
    meta_block = ""
    bm = re.match(r"\s*((?:^>.*\n?)+)", body_src, re.M)
    if bm:
        meta_block = bm.group(1)
        body_src = body_src[bm.end():]

    def field(label):
        mm = re.search(r"\*\*" + label + r":?\*\*\s*(.+)", meta_block)
        return mm.group(1).strip() if mm else ""

    speaker = field("Speaker").split(",")[0].strip() or "Anthropic"
    time_raw = field("Estimated time")
    time_short = re.sub(r"\s*\(.*\)", "", time_raw).strip() or "45 to 60 min"
    yt = re.search(r"\((https://www\.youtube\.com/watch\?[^)]+)\)", meta_block)
    yt_url = yt.group(1) if yt else "#"

    # Eyebrow + hero title (split on the first ": ").
    if ": " in title_full:
        eyebrow, hero_title = title_full.split(": ", 1)
    else:
        eyebrow, hero_title = "Lesson", title_full
    bits = hero_title.rsplit(" ", 1)
    hero_title_html = (html.escape(bits[0]) + ' <span class="accent">' + html.escape(bits[1]) + "</span>") if len(bits) == 2 else html.escape(hero_title)

    # Lead = first paragraph under "## In one sentence".
    lead = ""
    lm = re.search(r"##\s+In one sentence\s*\n+([^\n#]+(?:\n[^\n#]+)*)", body_src)
    if lm:
        lead = re.sub(r"\s+", " ", lm.group(1)).strip()

    md = markdown.Markdown(
        extensions=["fenced_code", "tables", "toc", "sane_lists", "attr_list", "codehilite"],
        extension_configs={
            "codehilite": {"guess_lang": False, "css_class": "codehilite"},
            "toc": {"toc_depth": "2-3"},
        },
    )
    body_html = md.convert(body_src)
    toc_html = md.toc

    # Give the Capstone heading a stable id ("capstone") so nav and hero button
    # always reach it, and point its TOC link there too.
    body_html = re.sub(r'<h2 id="[^"]*"(>\s*(?:\U0001F6E0️?\s*)?Capstone)', r'<h2 id="capstone" class="capstone-h"\1', body_html)
    toc_html = re.sub(r'<a href="#[^"]*"(>\s*(?:\U0001F6E0️?\s*)?Capstone)', r'<a href="#capstone" class="toc-capstone"\1', toc_html)

    # Previous / next / home navigation so every lesson is interlinked.
    nav = '<nav class="lessonnav">'
    if prev:
        nav += f'<a class="ln prev" href="{html.escape(prev["href"])}"><span class="dir">&#8592; Previous</span><b>{html.escape(prev["title"])}</b></a>'
    nav += f'<a class="ln home" href="{html.escape(home)}"><b>All lessons</b></a>'
    if nxt:
        nav += f'<a class="ln next" href="{html.escape(nxt["href"])}"><span class="dir">Next &#8594;</span><b>{html.escape(nxt["title"])}</b></a>'
    nav += '</nav>'

    pyg_css = HtmlFormatter(style="one-dark").get_style_defs(".codehilite")

    out = (TEMPLATE
           .replace("{{TITLE}}", html.escape(title_full))
           .replace("{{EYEBROW}}", html.escape(eyebrow))
           .replace("{{HERO_TITLE}}", hero_title_html)
           .replace("{{LEAD}}", html.escape(lead))
           .replace("{{SPEAKER}}", html.escape(speaker))
           .replace("{{TIME}}", html.escape(time_short))
           .replace("{{YT_URL}}", html.escape(yt_url))
           .replace("{{HOME}}", html.escape(home))
           .replace("{{NAV}}", nav)
           .replace("{{TOC}}", toc_html)
           .replace("{{BODY}}", body_html)
           .replace("{{PYGMENTS_CSS}}", pyg_css))
    pathlib.Path(out_path).write_text(out)
    print(f"wrote {out_path} ({len(out)//1024} KB)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: build_lessons_html.py <input.md> <output.html>")
    convert(sys.argv[1], sys.argv[2])

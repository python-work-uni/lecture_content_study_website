#!/usr/bin/env python3
"""ELEC3609/9609 study-guide builder.

Self-contained: the whole design system (CSS + JS + layout) lives in this file
as an embedded template, so every generated guide is a single portable HTML file
with no external template or stylesheet dependency.

Usage:
    python build_study_guides.py <root-dir>

Scans <root-dir> recursively for *_study_guide.txt sources and writes a sibling
*.html for each (skipping the legacy, session-less reference source).
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Inline markdown
# ---------------------------------------------------------------------------


def inline(text: str) -> str:
    """Render inline markdown. Code/math spans are protected first so that a
    single '*' inside `code` cannot break surrounding **bold** parsing."""
    text = text.strip()
    store: list[str] = []

    def stash(html_str: str) -> str:
        store.append(html_str)
        return "\x00" + str(len(store) - 1) + "\x00"

    text = re.sub(r"`([^`]+)`",
                  lambda m: stash("<code>" + html.escape(m.group(1), quote=False) + "</code>"),
                  text)
    text = re.sub(r"\$([^$\n]+)\$",
                  lambda m: stash('<span class="math">' + html.escape(m.group(1), quote=False) + "</span>"),
                  text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*([^*]+)\*\*", lambda m: "<strong>" + m.group(1) + "</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", lambda m: "<em>" + m.group(1) + "</em>", text)
    text = re.sub(r"\x00(\d+)\x00", lambda m: store[int(m.group(1))], text)
    return text


# ---------------------------------------------------------------------------
# Source parsing
# ---------------------------------------------------------------------------
SEP = re.compile(r"^\s*[=\-_]{4,}\s*$")
FENCE = re.compile(r"^\s*(?:```|~~~)")
CALLOUTS = {
    "💡": ("why", "Why It Matters"),
    "🧠": ("memory", "Memory Hook"),
    "⚠️": ("warn", "Watch Out"),
    "❌": ("warn", "Watch Out"),
    "🔥": ("warn", "Watch Out"),
    "ℹ️": ("info", "Note"),
    "📌": ("info", "Note"),
    "✅": ("tip", "Tip"),
    "📝": ("tip", "Tip"),
}
EMOJI_RE = re.compile(r"^(" + "|".join(map(re.escape, CALLOUTS)) + r")\s*(.*)$")


def split_segments(text: str) -> list[list[str]]:
    segs: list[list[str]] = []
    buf: list[str] = []
    fence = False
    for raw in text.split("\n"):
        line = raw.rstrip()
        if FENCE.match(line):
            fence = not fence
            buf.append(line)
            continue
        if not fence and SEP.match(line):
            segs.append(buf)
            buf = []
            continue
        buf.append(line)
    segs.append(buf)
    out = []
    for s in segs:
        while s and not s[0].strip():
            s.pop(0)
        while s and not s[-1].strip():
            s.pop()
        if s:
            out.append(s)
    return out


def header_kind(line: str) -> str | None:
    low = line.strip().lower()
    if re.match(r"^section\s*\d+", low):
        return "section"
    if low.startswith("overview"):
        return "overview"
    if low.startswith("stats"):
        return "stats"
    if "key takeaway" in low:
        return "takeaways"
    if "term" in low and ("know" in low or "glossary" in low):
        return "terms"
    if "mnemonic" in low or "quick recall" in low:
        return "mnemonics"
    if any(k in low for k in ("worked", "concrete", "scenario")):
        return "examples"
    if "exam" in low or "practice question" in low:
        return "exam"
    return None


def parse_title(lines: list[str]) -> dict:
    first = lines[0].strip() if lines else "Study Guide"
    subtitle = lines[1].strip() if len(lines) > 1 else ""
    m = re.match(r"^\s*([A-Z]{2,}\s*\d+[A-Za-z]?)\s*(.*)$", first)
    course = m.group(1).replace(" ", "") if m else first.split()[0]
    rest = m.group(2) if m else first
    if "lab" in rest.lower():
        lm = re.search(r"lab\s*(?:week\s*)?(\d+)", rest, re.I)
        label = f"Lab {lm.group(1)}" if lm else "Lab Overview"
    else:
        wm = re.search(r"week\s*\d+", rest, re.I)
        label = wm.group(0) if wm else ""
    return {"course": course, "label": label, "subtitle": subtitle, "first": first}


def parse(text: str) -> dict:
    segs = split_segments(text)
    meta = parse_title([l.strip() for l in segs[0] if l.strip()])
    doc: dict = {"meta": meta, "overview": [], "stats": [], "sections": [],
                 "takeaways": [], "terms": [], "mnemonics": [], "examples": [], "exam": []}
    pending = None
    for seg in segs[1:]:
        nonblank = [l for l in seg if l.strip()]
        if not nonblank:
            continue
        if pending is None and len(nonblank) == 1:
            k = header_kind(nonblank[0])
            if k:
                pending = (k, nonblank[0])
                continue
        if pending:
            k, hdr = pending
            body = seg
        else:
            k, hdr = "section", nonblank[0]
            body = seg[1:]
        pending = None
        if k == "overview":
            doc["overview"].extend(body)
        elif k == "stats":
            doc["stats"].extend(body)
        elif k == "section":
            m = re.match(r"^\s*section\s*(\d+)\s*[:.\-]?\s*(.*)$", hdr, re.I)
            num = int(m.group(1)) if m else len(doc["sections"]) + 1
            title = (m.group(2) if m else hdr).strip() or hdr.strip()
            doc["sections"].append({"num": num, "title": title, "body": body})
        else:
            doc[k].extend(body)
    return doc


# ---------------------------------------------------------------------------
# Block rendering
# ---------------------------------------------------------------------------
def is_block_start(line: str) -> bool:
    s = line.strip()
    if not s:
        return True
    if FENCE.match(s) or s.startswith("#") or s.startswith("|"):
        return True
    if EMOJI_RE.match(s):
        return True
    if re.match(r"^\s*[-*]\s+", line) or re.match(r"^\s*\d+[.)]\s+", line):
        return True
    if re.match(r"^\*\*(.+?)\*\*:\s*`[^`]+`\s*$", s):
        return True
    return False


def render_callout(emoji: str, text: str) -> str:
    cls, default = CALLOUTS[emoji]
    m = re.match(r"^\*\*(.+?)\*\*:?\s*(.*)$", text)
    if m and m.group(2).strip():
        title, body = m.group(1).strip(), m.group(2).strip()
    else:
        title, body = default, text
    return (f'<div class="callout {cls}"><div class="callout-ico" aria-hidden="true">{emoji}</div>'
            f'<div class="callout-body"><p class="callout-title">{inline(title)}</p>'
            f'<div class="callout-text">{inline(body)}</div></div></div>')


def render_code(text: str) -> str:
    return ('<div class="code"><button class="copy" type="button" data-copy>Copy</button>'
            '<pre><code>' + html.escape(text) + "</code></pre></div>")


def render_flow(text: str) -> str:
    steps: list[str] = []
    for raw in text.split("\n"):
        line = raw.strip()
        if not line:
            continue
        line = re.sub(r"\s*←.*$", "", line)
        line = line.replace("↓", " ").replace("↑", " ").replace("↔", " & ")
        for part in re.split(r"[→↦]", line):
            part = part.strip()
            if part:
                steps.append(part)
    out = []
    for k, st in enumerate(steps, 1):
        out.append(f'<div class="flow-step"><span class="flow-n">{k:02d}</span><span>{inline(st)}</span></div>')
        if k < len(steps):
            out.append('<span class="flow-arrow" aria-hidden="true">→</span>')
    return '<div class="flow">' + "".join(out) + "</div>"


def render_fence(body: list[str]) -> str:
    text = "\n".join(l.rstrip() for l in body).strip("\n")
    if text.count("→") + text.count("↓") >= 2:
        return render_flow(text)
    return render_code(text)


def render_table(rows: list[str]) -> str:
    parsed = []
    for r in rows:
        r = r.strip()
        if r.startswith("|"):
            r = r[1:]
        if r.endswith("|"):
            r = r[:-1]
        parsed.append([c.strip() for c in r.split("|")])
    header = None
    data = parsed
    if len(parsed) >= 2 and all(re.fullmatch(r":?-+:?", c) for c in parsed[1]):
        header = parsed[0]
        data = parsed[2:]
    thead = ""
    if header:
        thead = "<thead><tr>" + "".join("<th>" + inline(c) + "</th>" for c in header) + "</tr></thead>"
    tbody = "<tbody>" + "".join(
        "<tr>" + "".join("<td>" + inline(c) + "</td>" for c in row) + "</tr>" for row in data) + "</tbody>"
    return '<div class="table-wrap"><table>' + thead + tbody + "</table></div>"


def build_list(items: list[tuple[int, str]]) -> str:
    def build(idx: int, indent: int):
        parts = []
        while idx < len(items):
            ind, content = items[idx]
            if ind < indent:
                break
            if ind > indent:
                sub, idx = build(idx, ind)
                parts.append(sub)
                continue
            idx += 1
            sub = ""
            if idx < len(items) and items[idx][0] > ind:
                sub, idx = build(idx, items[idx][0])
            parts.append("<li>" + content + sub + "</li>")
        return "".join(parts), idx

    body, _ = build(0, items[0][0])
    return "<ul>" + body + "</ul>"


def render_bullets(lines: list[str]) -> str:
    items = []
    for raw in lines:
        m = re.match(r"^(\s*)[-*]\s+(.*)$", raw)
        indent = len(m.group(1).replace("\t", "  "))
        items.append((indent, inline(m.group(2))))
    return build_list(items)


def render_numbered(lines: list[str]) -> str:
    items = [inline(re.match(r"^\s*\d+[.)]\s+(.*)$", l).group(1)) for l in lines]
    return "<ol>" + "".join("<li>" + t + "</li>" for t in items) + "</ol>"


def render_blocks(lines: list[str]) -> str:
    parts: list[str] = []
    i, n = 0, len(lines)
    while i < n:
        raw = lines[i]
        s = raw.strip()
        if not s:
            i += 1
            continue
        if FENCE.match(s):
            j = i + 1
            body = []
            while j < n and not FENCE.match(lines[j].strip()):
                body.append(lines[j])
                j += 1
            j += 1
            parts.append(render_fence(body))
            i = j
            continue
        m = EMOJI_RE.match(s)
        if m:
            buf = [m.group(2)]
            j = i + 1
            while j < n and lines[j].strip() and not is_block_start(lines[j]):
                buf.append(lines[j].strip())
                j += 1
            parts.append(render_callout(m.group(1), " ".join(buf)))
            i = j
            continue
        if s.startswith("#"):
            parts.append('<h3 class="subhead">' + inline(s.lstrip("#").strip()) + "</h3>")
            i += 1
            continue
        if s.startswith("|"):
            j = i
            rows = []
            while j < n and lines[j].strip().startswith("|"):
                rows.append(lines[j])
                j += 1
            parts.append(render_table(rows))
            i = j
            continue
        m = re.match(r"^\*\*(.+?)\*\*:\s*`([^`]+)`\s*$", s)
        if m:
            parts.append('<div class="formula"><span class="formula-label">' + html.escape(m.group(1)) +
                         "</span><code>" + html.escape(m.group(2)) + "</code></div>")
            i += 1
            continue
        if re.match(r"^\s*[-*]\s+", raw):
            j = i
            while j < n and re.match(r"^\s*[-*]\s+", lines[j]):
                j += 1
            parts.append(render_bullets(lines[i:j]))
            i = j
            continue
        if re.match(r"^\s*\d+[.)]\s+", raw):
            j = i
            while j < n and re.match(r"^\s*\d+[.)]\s+", lines[j]):
                j += 1
            parts.append(render_numbered(lines[i:j]))
            i = j
            continue
        buf = [s]
        j = i + 1
        while j < n and lines[j].strip() and not is_block_start(lines[j]):
            buf.append(lines[j].strip())
            j += 1
        parts.append("<p>" + inline(" ".join(buf)) + "</p>")
        i = j
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Closing sections
# ---------------------------------------------------------------------------
def render_takeaways(lines: list[str]) -> str:
    items = []
    for raw in lines:
        m = re.match(r"^\s*\d+[.)]\s*(.*)$", raw)
        if m and m.group(1).strip():
            items.append(inline(m.group(1)))
    body = "".join(f'<li><span class="tk-n">{k}</span><div>{t}</div></li>' for k, t in enumerate(items, 1))
    return '<ol class="takeaways">' + body + "</ol>"


def render_terms(lines: list[str]) -> str:
    cards = []
    for raw in lines:
        s = raw.strip()
        if ":" not in s:
            continue
        name, defn = s.split(":", 1)
        name = name.strip().strip("*").strip()
        defn = defn.strip()
        if not name or not defn:
            continue
        blob = (name + " " + defn).lower()
        cards.append(
            f'<div class="term" data-term="{html.escape(blob, quote=True)}">'
            f'<p class="term-name">{inline(name)}</p>'
            f'<p class="term-def">{inline(defn)}</p></div>')
    return ('<div class="term-filter"><input type="search" id="termSearch" placeholder="Filter terms…" '
            'autocomplete="off" aria-label="Filter glossary terms"><span class="term-count" id="termCount"></span></div>'
            '<div class="terms" id="termsGrid">' + "".join(cards) + "</div>")


def render_mnemonics(lines: list[str]) -> str:
    cards: list[str] = []
    cur: dict | None = None

    def flush():
        nonlocal cur
        if not cur:
            return
        bits = ['<div class="mnemonic">', f'<p class="mn-title">{inline(cur["name"])}</p>']
        if cur["code"]:
            bits.append(f'<p class="mn-code">{html.escape(cur["code"])}</p>')
        if cur["phrase"]:
            bits.append(f'<p class="mn-phrase">{inline(cur["phrase"])}</p>')
        if cur["note"]:
            bits.append(f'<p class="mn-note">{inline(cur["note"])}</p>')
        bits.append("</div>")
        cards.append("".join(bits))
        cur = None

    for raw in lines:
        s = raw.strip()
        if not s:
            continue
        m = re.match(r"^\*\*(.+?)\*\*:\s*(.*)$", s)
        if m:
            flush()
            name, rest = m.group(1).strip(), m.group(2).strip()
            cm = re.search(r"\*\*(.+?)\*\*", rest)
            code = cm.group(1) if cm else ""
            pm = re.search(r"[“\"](.+?)[”\"]", rest)
            phrase = pm.group(1) if pm else ""
            note = rest
            if code:
                note = note.replace("**" + code + "**", "")
            if phrase:
                note = re.sub(r"[“\"].*?[”\"]", "", note)
            cur = {"name": name, "code": code, "phrase": phrase, "note": note.strip(" —-–:")}
        elif cur:
            cur["note"] = (cur["note"] + " " + s).strip()
    flush()
    return '<div class="mnemonics">' + "".join(cards) + "</div>"


def render_examples(lines: list[str]) -> str:
    out: list[str] = []
    i, n = 0, len(lines)
    while i < n:
        s = lines[i].strip()
        if not s:
            i += 1
            continue
        m = re.match(r"^###\s*Example\s*(\d+)\s*[:.\-]?\s*(.*)$", s, re.I)
        if not m:
            out.append('<div class="example">' + render_blocks(lines[i:]) + "</div>")
            break
        title = m.group(2).strip() or f"Example {m.group(1)}"
        j = i + 1
        body = []
        while j < n and not re.match(r"^\s*###\s*Example", lines[j].strip(), re.I):
            body.append(lines[j])
            j += 1
        out.append('<div class="example"><span class="example-tag">Example ' + m.group(1) + "</span>"
                   '<h3 class="example-title">' + inline(title) + "</h3>" + render_blocks(body) + "</div>")
        i = j
    return "".join(out)


def render_exam(lines: list[str]) -> str:
    qs: list[str] = []
    ans: list[str] = []
    for raw in lines:
        m = re.match(r"^\s*(\d+)[.)]\s*(.*)$", raw)
        if m:
            q = m.group(2).strip()
            am = re.match(r"^(.*?)(?:→\s*Answer:|\*\*Answer:?\*\*|Answer:)\s*(.*)$", q, re.I)
            if am and am.group(2):
                qs.append(am.group(1).strip())
                ans.append(am.group(2).strip())
            else:
                qs.append(q)
                ans.append("")
            continue
        am = re.match(r"^(?:\*\*Answer:?\*\*|Answer:)\s*(.*)$", raw.strip(), re.I)
        if am and ans:
            ans[-1] = am.group(1).strip()
    cards = []
    for k, q in enumerate(qs, 1):
        a = ans[k - 1] if k - 1 < len(ans) else ""
        ahtml = ('<div class="quiz-a"><span class="quiz-a-label">Answer</span>' + inline(a) + "</div>"
                 if a else '<div class="quiz-a muted">Answer not provided — review the section above.</div>')
        cards.append(
            f'<article class="quiz" data-q="{k}">'
            f'<button class="quiz-q" type="button" aria-expanded="false">'
            f'<span class="quiz-n">{k}</span><span class="quiz-text">{inline(q)}</span>'
            f'<span class="quiz-chev" aria-hidden="true">▾</span></button>'
            f'<div class="quiz-body">{ahtml}'
            f'<label class="mastered"><input type="checkbox" data-mastered="{k}"> Mark as mastered</label>'
            f"</div></article>")
    total = len(qs)
    return (f'<div class="exam-bar"><div class="exam-progress"><span class="exam-count">'
            f'<strong id="examDone">0</strong> / {total} mastered</span>'
            f'<span class="exam-track"><span id="examFill"></span></span></div>'
            f'<div class="exam-actions"><button type="button" class="btn" id="revealAll">Reveal all</button>'
            f'<button type="button" class="btn" id="hideAll">Hide all</button>'
            f'<button type="button" class="btn ghost" id="resetExam">Reset</button></div></div>'
            + "".join(cards))


# ---------------------------------------------------------------------------
# Page assembly
# ---------------------------------------------------------------------------
def shorten(text: str, limit: int) -> str:
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    return text[: limit - 1].rsplit(" ", 1)[0].rstrip(".,;: ") + "…"


def render_doc(doc: dict, guide_id: str) -> str:
    meta = doc["meta"]
    overview_raw = " ".join(l.strip() for l in doc["overview"] if l.strip())
    overview_plain = overview_raw.replace("**", "")

    # stat pills
    pills = []
    for raw in doc["stats"]:
        s = raw.strip()
        if not s or "|" not in s:
            continue
        label, value = [p.strip() for p in s.split("|", 1)]
        pills.append(f'<div class="stat"><span class="stat-val">{inline(value)}</span>'
                     f'<span class="stat-label">{html.escape(label)}</span></div>')

    hero = ['<section class="hero" id="overview">',
            '<p class="hero-tag">📖 Course notes · ' + html.escape(meta["label"] or meta["course"]) + "</p>",
            "<h1>" + inline(meta["subtitle"] or meta["course"]) + "</h1>",
            '<p class="hero-sub">' + html.escape(shorten(overview_plain, 155)) + "</p>",
            '<div class="hero-overview"><p class="ho-label">Lecture overview</p>'
            "<p>" + inline(overview_raw) + "</p></div>"]
    if pills:
        hero.append('<div class="stats">' + "".join(pills) + "</div>")
    hero.append("</section>")

    sections_html = []
    nav = ['<li><a href="#overview" class="toc-link"><span class="toc-n">00</span>Overview</a></li>']
    n = 0

    def add_section(anchor: str, number: str, title: str, body_html: str):
        sections_html.append(
            f'<section class="section" id="{anchor}">'
            f'<header class="section-head"><span class="section-num">{number}</span>'
            f'<h2>{inline(title)}</h2></header>'
            f'<div class="section-body">{body_html}</div></section>')
        nav.append(f'<li><a href="#{anchor}" class="toc-link"><span class="toc-n">{number}</span>{html.escape(title)}</a></li>')

    for sec in doc["sections"]:
        n += 1
        add_section(f"sec-{n}", f"{n:02d}", sec["title"], render_blocks(sec["body"]))

    if doc["takeaways"]:
        n += 1
        add_section("key-takeaways", f"{n:02d}", "Key Takeaways", render_takeaways(doc["takeaways"]))
    if doc["terms"]:
        n += 1
        add_section("glossary", f"{n:02d}", "Glossary", render_terms(doc["terms"]))
    if doc["mnemonics"]:
        n += 1
        add_section("mnemonics", f"{n:02d}", "Mnemonics & Quick Recall", render_mnemonics(doc["mnemonics"]))
    if doc["examples"]:
        n += 1
        add_section("worked-examples", f"{n:02d}", "Worked Examples & Scenarios", render_examples(doc["examples"]))
    if doc["exam"]:
        n += 1
        add_section("exam-focus", f"{n:02d}", "Exam Practice", render_exam(doc["exam"]))

    content = "\n".join(hero) + "\n" + "\n".join(sections_html)

    course, label = meta["course"], meta["label"]
    badge = f"{course} · {label}".strip(" ·")
    page_title = f"{course} {label} Study Guide – {meta['subtitle']}".strip(" –")
    header_title = shorten(meta["subtitle"], 70)
    footer = (f'<strong>{html.escape(course)} study guide</strong> · '
              f'{html.escape(meta["subtitle"])}')

    return (TEMPLATE
            .replace("{{TITLE}}", html.escape(page_title))
            .replace("{{DESC}}", html.escape(shorten(overview_plain, 180), quote=True))
            .replace("{{BADGE}}", html.escape(badge))
            .replace("{{HEADTITLE}}", html.escape(header_title))
            .replace("{{NAV}}", "\n".join(nav))
            .replace("{{CONTENT}}", content)
            .replace("{{FOOTER}}", footer)
            .replace("{{GUIDEID}}", html.escape(guide_id, quote=True)))


# ---------------------------------------------------------------------------
# Embedded design system (template)
# ---------------------------------------------------------------------------
TEMPLATE = r"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{TITLE}}</title>
<meta name="description" content="{{DESC}}">
<meta name="color-scheme" content="light dark">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box}
:root{
  --sans:'Inter',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;
  --head:'Sora','Inter',system-ui,sans-serif;
  --mono:'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,monospace;
  --bg:#f4f8f7;--bg-2:#e9f1ef;--surface:#ffffff;--surface-2:#eff5f4;
  --ink:#15282b;--muted:#587076;--faint:#89a0a3;--line:#d8e5e2;
  --brand:#0e7c6b;--brand-2:#12a594;--brand-soft:#d6f3ec;--brand-ink:#0a5b4e;
  --amber:#b45309;--amber-soft:#fdf0d6;
  --rose:#b21e4b;--rose-soft:#fde4ec;
  --sky:#0c6ea3;--sky-soft:#ddeffb;
  --violet:#6d28d9;--violet-soft:#ece7fd;
  --shadow:0 1px 2px rgba(16,40,43,.05),0 10px 28px -16px rgba(16,40,43,.30);
  --shadow-lg:0 26px 60px -30px rgba(16,40,43,.45);
  --r:16px;--r-sm:11px;--sidebar:288px;
}
[data-theme=dark]{
  --bg:#07110f;--bg-2:#0b1a17;--surface:#0e1d1a;--surface-2:#122522;
  --ink:#e6f2ef;--muted:#94ada8;--faint:#69837e;--line:#1c322e;
  --brand:#2dd4bf;--brand-2:#5eead4;--brand-soft:rgba(45,212,191,.15);--brand-ink:#99f6e4;
  --amber:#fbbf24;--amber-soft:rgba(251,191,36,.15);
  --rose:#fb7185;--rose-soft:rgba(251,113,133,.15);
  --sky:#38bdf8;--sky-soft:rgba(56,189,248,.15);
  --violet:#a78bfa;--violet-soft:rgba(167,139,250,.17);
  --shadow:0 1px 2px rgba(0,0,0,.35),0 12px 32px -18px rgba(0,0,0,.7);
  --shadow-lg:0 28px 70px -34px rgba(0,0,0,.85);
}
html{scroll-behavior:smooth}
body{margin:0;font-family:var(--sans);background:var(--bg);color:var(--ink);line-height:1.68;-webkit-font-smoothing:antialiased}
body::before{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;opacity:.75;
  background:radial-gradient(58rem 38rem at 112% -12%,var(--brand-soft),transparent 62%),
             radial-gradient(46rem 30rem at -12% 6%,var(--sky-soft),transparent 58%)}
h1,h2,h3,h4{font-family:var(--head);line-height:1.2;margin:0}
p{margin:0 0 .85rem}
a{color:var(--brand);text-decoration:none}
a:hover{text-decoration:underline}
strong{font-weight:650;color:var(--ink)}
code{font-family:var(--mono);font-size:.86em;background:var(--surface-2);border:1px solid var(--line);border-radius:6px;padding:.08em .38em}
.math{font-family:var(--mono);background:var(--surface-2);border:1px solid var(--line);border-radius:6px;padding:.06em .4em;font-size:.9em}
::selection{background:var(--brand-soft);color:var(--brand-ink)}
/* progress */
.progress{position:fixed;top:0;left:0;height:3px;width:0;z-index:60;background:linear-gradient(90deg,var(--brand),var(--brand-2),var(--sky))}
/* topbar */
.topbar{position:sticky;top:0;z-index:50;display:flex;align-items:center;gap:.75rem;
  padding:.6rem clamp(.9rem,3vw,1.6rem);background:color-mix(in srgb,var(--surface) 82%,transparent);
  backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}
.brand{display:flex;align-items:center;gap:.6rem;min-width:0}
.brand-badge{flex:none;font-size:.68rem;font-weight:700;letter-spacing:.09em;text-transform:uppercase;
  color:var(--brand-ink);background:var(--brand-soft);border-radius:999px;padding:.28rem .6rem;white-space:nowrap}
.brand-title{font-weight:600;font-size:.92rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.topbar-actions{margin-left:auto;display:flex;align-items:center;gap:.45rem}
.icon-btn{display:inline-grid;place-items:center;width:38px;height:38px;border:1px solid var(--line);
  background:var(--surface);color:var(--ink);border-radius:10px;cursor:pointer;font-size:1rem;transition:.15s}
.icon-btn:hover{border-color:var(--brand);color:var(--brand)}
.menu-btn{display:none}
.search{position:relative}
.search input{width:min(30vw,240px);padding:.5rem .7rem;border:1px solid var(--line);border-radius:10px;
  background:var(--surface);color:var(--ink);font:inherit;font-size:.85rem}
.search input:focus{outline:2px solid var(--brand-soft);border-color:var(--brand)}
.search-results{position:absolute;right:0;top:calc(100% + 8px);width:min(78vw,380px);max-height:60vh;overflow:auto;
  background:var(--surface);border:1px solid var(--line);border-radius:12px;box-shadow:var(--shadow-lg);display:none;padding:.35rem}
.search-results.open{display:block}
.sr-item{display:block;width:100%;text-align:left;border:0;background:none;color:var(--ink);font:inherit;
  padding:.5rem .6rem;border-radius:8px;cursor:pointer}
.sr-item:hover,.sr-item.active{background:var(--surface-2)}
.sr-item b{display:block;font-size:.84rem;color:var(--brand-ink)}
.sr-item span{display:block;font-size:.76rem;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sr-empty{padding:.6rem;color:var(--muted);font-size:.82rem}
/* shell */
.shell{display:grid;grid-template-columns:var(--sidebar) minmax(0,1fr);gap:0;align-items:start}
.sidebar{position:sticky;top:57px;height:calc(100vh - 57px);overflow:auto;padding:1.3rem .9rem 3rem 1.4rem}
.toc-title{font-size:.68rem;letter-spacing:.14em;text-transform:uppercase;color:var(--faint);font-weight:700;margin:0 0 .7rem .5rem}
.toc{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:1px}
.toc-link{display:flex;gap:.55rem;align-items:baseline;padding:.36rem .5rem;border-radius:8px;color:var(--muted);
  font-size:.82rem;line-height:1.35;transition:.13s}
.toc-link:hover{background:var(--surface-2);color:var(--ink);text-decoration:none}
.toc-link.active{background:var(--brand-soft);color:var(--brand-ink);font-weight:600}
.toc-n{font-family:var(--mono);font-size:.66rem;color:var(--faint);flex:none;padding-top:.12rem}
.toc-link.active .toc-n{color:var(--brand)}
.content{min-width:0;max-width:960px;padding:1.6rem clamp(1rem,3.5vw,2.6rem) 5rem}
/* hero */
.hero{position:relative;overflow:hidden;border:1px solid var(--line);border-radius:var(--r);
  padding:clamp(1.4rem,3.5vw,2.4rem);background:
    linear-gradient(180deg,color-mix(in srgb,var(--brand-soft) 55%,var(--surface)),var(--surface) 72%);
  box-shadow:var(--shadow);margin-bottom:2rem}
.hero::after{content:"";position:absolute;right:-70px;top:-70px;width:230px;height:230px;border-radius:50%;
  background:radial-gradient(circle,var(--brand-soft),transparent 68%);opacity:.8}
.hero-tag{font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;color:var(--brand-ink);font-weight:700;margin:0 0 .55rem}
.hero h1{font-size:clamp(1.5rem,4vw,2.15rem);letter-spacing:-.02em;margin-bottom:.5rem}
.hero-sub{color:var(--muted);font-size:1.02rem;max-width:60ch;margin-bottom:1.1rem}
.hero-overview{position:relative;background:var(--surface);border:1px solid var(--line);border-radius:var(--r-sm);
  padding:1rem 1.15rem;box-shadow:var(--shadow)}
.ho-label{font-size:.68rem;letter-spacing:.12em;text-transform:uppercase;color:var(--faint);font-weight:700;margin:0 0 .35rem}
.hero-overview p:last-child{margin:0}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:.7rem;margin-top:1.1rem}
.stat{background:var(--surface);border:1px solid var(--line);border-radius:var(--r-sm);padding:.7rem .85rem;box-shadow:var(--shadow)}
.stat-val{display:block;font-family:var(--head);font-weight:800;font-size:1.25rem;color:var(--brand-ink)}
.stat-label{display:block;font-size:.72rem;color:var(--muted);letter-spacing:.03em;text-transform:uppercase;font-weight:600}
/* sections */
.section{scroll-margin-top:80px;margin-bottom:2.4rem;opacity:0;transform:translateY(14px);transition:opacity .5s ease,transform .5s ease}
.section.in{opacity:1;transform:none}
.section-head{display:flex;align-items:center;gap:.75rem;margin-bottom:1rem;padding-bottom:.6rem;border-bottom:2px solid var(--line)}
.section-num{flex:none;font-family:var(--head);font-weight:800;font-size:.82rem;color:#fff;background:linear-gradient(135deg,var(--brand),var(--brand-2));
  width:2.1rem;height:2.1rem;display:grid;place-items:center;border-radius:10px;box-shadow:0 6px 16px -8px var(--brand)}
.section-head h2{font-size:clamp(1.15rem,2.6vw,1.5rem);letter-spacing:-.01em}
.section-body>*+*{margin-top:.5rem}
.section-body p{margin:0 0 .9rem}
.subhead{font-size:.98rem;margin:1.2rem 0 .5rem;color:var(--brand-ink)}
ul,ol{margin:0 0 .9rem;padding-left:1.25rem}
li{margin:.22rem 0}
li>ul,li>ol{margin:.3rem 0 .1rem}
/* table */
.table-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:var(--r-sm);margin:1rem 0;box-shadow:var(--shadow)}
table{border-collapse:collapse;width:100%;font-size:.88rem;min-width:440px}
thead th{background:var(--surface-2);text-align:left;font-weight:700;color:var(--ink);white-space:nowrap}
th,td{padding:.6rem .8rem;border-bottom:1px solid var(--line);vertical-align:top}
tbody tr:last-child td{border-bottom:0}
tbody tr:nth-child(even){background:color-mix(in srgb,var(--surface-2) 45%,transparent)}
/* code */
.code{position:relative;margin:1rem 0}
.code pre{margin:0;background:var(--surface-2);border:1px solid var(--line);border-radius:var(--r-sm);
  padding:1rem 1.1rem;overflow:auto;box-shadow:var(--shadow)}
.code code{font-family:var(--mono);font-size:.82rem;line-height:1.6;background:none;border:0;padding:0;color:var(--ink);white-space:pre}
.copy{position:absolute;top:.55rem;right:.55rem;font-size:.68rem;letter-spacing:.04em;text-transform:uppercase;font-weight:700;
  color:var(--muted);background:var(--surface);border:1px solid var(--line);border-radius:7px;padding:.24rem .5rem;cursor:pointer}
.copy:hover{color:var(--brand);border-color:var(--brand)}
.copy.done{color:var(--brand-ink);border-color:var(--brand)}
/* formula */
.formula{position:relative;margin:1rem 0;padding:1.1rem 1rem .9rem;background:var(--surface-2);border:1px solid var(--line);border-radius:var(--r-sm)}
.formula-label{position:absolute;top:-.6rem;left:.9rem;font-size:.66rem;letter-spacing:.07em;text-transform:uppercase;font-weight:700;
  color:#fff;background:var(--brand);border-radius:6px;padding:.14rem .5rem}
.formula code{display:block;font-family:var(--mono);font-size:.86rem;background:none;border:0;padding:0;color:var(--ink)}
/* flow */
.flow{display:flex;flex-wrap:wrap;align-items:center;gap:.45rem;margin:1rem 0;padding:1rem;background:var(--surface);
  border:1px solid var(--line);border-radius:var(--r-sm);box-shadow:var(--shadow)}
.flow-step{display:inline-flex;align-items:center;gap:.4rem;background:var(--surface-2);border:1px solid var(--line);
  border-radius:999px;padding:.34rem .75rem .34rem .5rem;font-size:.82rem;font-weight:600}
.flow-n{font-family:var(--mono);font-size:.64rem;color:#fff;background:var(--brand);border-radius:999px;padding:.1rem .34rem}
.flow-arrow{color:var(--brand);font-weight:800}
/* callouts */
.callout{display:flex;gap:.75rem;margin:1rem 0;padding:.9rem 1rem;border:1px solid var(--line);border-left-width:4px;
  border-radius:var(--r-sm);background:var(--surface);box-shadow:var(--shadow)}
.callout-ico{flex:none;font-size:1.15rem;line-height:1.3}
.callout-title{font-weight:700;font-size:.78rem;letter-spacing:.05em;text-transform:uppercase;margin:0 0 .18rem}
.callout-text{font-size:.93rem}
.callout-text>:last-child{margin-bottom:0}
.callout.why{border-left-color:var(--amber);background:color-mix(in srgb,var(--amber-soft) 55%,var(--surface))}
.callout.why .callout-title{color:var(--amber)}
.callout.memory{border-left-color:var(--violet);background:color-mix(in srgb,var(--violet-soft) 55%,var(--surface))}
.callout.memory .callout-title{color:var(--violet)}
.callout.warn{border-left-color:var(--rose);background:color-mix(in srgb,var(--rose-soft) 55%,var(--surface))}
.callout.warn .callout-title{color:var(--rose)}
.callout.info{border-left-color:var(--sky);background:color-mix(in srgb,var(--sky-soft) 55%,var(--surface))}
.callout.info .callout-title{color:var(--sky)}
.callout.tip{border-left-color:var(--brand);background:color-mix(in srgb,var(--brand-soft) 55%,var(--surface))}
.callout.tip .callout-title{color:var(--brand-ink)}
/* takeaways */
.takeaways{list-style:none;margin:0;padding:0;display:grid;gap:.6rem}
.takeaways li{display:flex;gap:.7rem;align-items:flex-start;background:var(--surface);border:1px solid var(--line);
  border-radius:var(--r-sm);padding:.75rem .9rem;box-shadow:var(--shadow)}
.tk-n{flex:none;font-family:var(--mono);font-size:.68rem;font-weight:700;color:var(--brand-ink);background:var(--brand-soft);
  border-radius:7px;padding:.22rem .45rem;margin-top:.15rem}
/* glossary */
.term-filter{display:flex;align-items:center;gap:.7rem;margin:0 0 .9rem}
.term-filter input{flex:1;max-width:340px;padding:.55rem .75rem;border:1px solid var(--line);border-radius:10px;background:var(--surface);color:var(--ink);font:inherit;font-size:.86rem}
.term-filter input:focus{outline:2px solid var(--brand-soft);border-color:var(--brand)}
.term-count{font-size:.78rem;color:var(--muted)}
.terms{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:.7rem}
.term{background:var(--surface);border:1px solid var(--line);border-radius:var(--r-sm);padding:.8rem .9rem;box-shadow:var(--shadow)}
.term.hide{display:none}
.term-name{font-family:var(--head);font-weight:700;font-size:.9rem;margin:0 0 .2rem;color:var(--brand-ink)}
.term-def{font-size:.85rem;color:var(--muted);margin:0}
/* mnemonics */
.mnemonics{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:.8rem}
.mnemonic{background:var(--surface);border:1px solid var(--line);border-radius:var(--r-sm);padding:.95rem 1rem;box-shadow:var(--shadow)}
.mn-title{font-family:var(--head);font-weight:700;font-size:.92rem;margin:0 0 .4rem;color:var(--brand-ink)}
.mn-code{font-family:var(--mono);font-weight:600;font-size:1.02rem;letter-spacing:.04em;margin:0 0 .35rem}
.mn-phrase{font-style:italic;font-weight:600;color:var(--violet);margin:0 0 .35rem}
.mn-note{font-size:.83rem;color:var(--muted);margin:0}
/* examples */
.example{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:1.1rem 1.2rem;margin:0 0 1rem;box-shadow:var(--shadow)}
.example-tag{display:inline-block;font-size:.66rem;letter-spacing:.08em;text-transform:uppercase;font-weight:700;
  color:var(--brand-ink);background:var(--brand-soft);border-radius:999px;padding:.2rem .55rem;margin-bottom:.5rem}
.example-title{font-size:1rem;margin:0 0 .6rem}
/* exam */
.exam-bar{display:flex;flex-wrap:wrap;gap:.8rem;align-items:center;justify-content:space-between;
  background:var(--surface);border:1px solid var(--line);border-radius:var(--r-sm);padding:.8rem 1rem;margin:0 0 1rem;box-shadow:var(--shadow)}
.exam-count{font-size:.85rem;color:var(--muted)}
.exam-count strong{color:var(--brand-ink)}
.exam-track{display:block;width:170px;height:7px;border-radius:999px;background:var(--surface-2);margin-top:.4rem;overflow:hidden}
.exam-track>span{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--brand),var(--brand-2));transition:width .3s}
.exam-actions{display:flex;gap:.4rem;flex-wrap:wrap}
.btn{font:inherit;font-size:.78rem;font-weight:600;color:var(--brand-ink);background:var(--brand-soft);border:1px solid transparent;
  border-radius:9px;padding:.42rem .7rem;cursor:pointer}
.btn:hover{background:var(--brand);color:#fff}
.btn.ghost{background:transparent;border-color:var(--line);color:var(--muted)}
.btn.ghost:hover{border-color:var(--brand);color:var(--brand);background:transparent}
.quiz{background:var(--surface);border:1px solid var(--line);border-radius:var(--r-sm);margin:0 0 .6rem;overflow:hidden;box-shadow:var(--shadow)}
.quiz-q{display:flex;gap:.7rem;align-items:flex-start;width:100%;text-align:left;background:none;border:0;color:var(--ink);
  font:inherit;font-weight:600;padding:.85rem .95rem;cursor:pointer}
.quiz-n{flex:none;font-family:var(--mono);font-size:.7rem;font-weight:700;color:#fff;background:var(--brand);border-radius:7px;padding:.2rem .45rem;margin-top:.1rem}
.quiz-text{flex:1}
.quiz-chev{flex:none;color:var(--muted);transition:transform .2s}
.quiz.open .quiz-chev{transform:rotate(180deg)}
.quiz-body{display:none;padding:0 .95rem .9rem;border-top:1px dashed var(--line)}
.quiz.open .quiz-body{display:block}
.quiz-a{font-size:.9rem;margin:.7rem 0;padding:.7rem .85rem;background:var(--surface-2);border-radius:9px}
.quiz-a-label{display:block;font-size:.66rem;letter-spacing:.08em;text-transform:uppercase;font-weight:700;color:var(--brand);margin-bottom:.2rem}
.quiz-a.muted{color:var(--muted);font-style:italic}
.mastered{display:inline-flex;gap:.45rem;align-items:center;font-size:.8rem;color:var(--muted);cursor:pointer;user-select:none}
.mastered input{accent-color:var(--brand);width:1rem;height:1rem}
/* footer */
.foot{margin-top:3rem;padding-top:1.2rem;border-top:1px solid var(--line);color:var(--muted);font-size:.82rem}
/* to top */
.totop{position:fixed;right:1.1rem;bottom:1.1rem;z-index:55;width:42px;height:42px;border-radius:12px;border:1px solid var(--line);
  background:var(--surface);color:var(--brand-ink);font-size:1.1rem;cursor:pointer;box-shadow:var(--shadow-lg);opacity:0;pointer-events:none;transition:.2s}
.totop.show{opacity:1;pointer-events:auto}
.scrim{display:none}
/* responsive */
@media (max-width:980px){
  .shell{grid-template-columns:1fr}
  .menu-btn{display:inline-grid}
  .sidebar{position:fixed;top:0;left:0;z-index:70;height:100vh;width:min(86vw,320px);background:var(--surface);
    border-right:1px solid var(--line);transform:translateX(-102%);transition:transform .25s ease;padding-top:1.4rem;box-shadow:var(--shadow-lg)}
  .sidebar.open{transform:none}
  .scrim{display:block;position:fixed;inset:0;z-index:65;background:rgba(6,18,16,.45);opacity:0;pointer-events:none;transition:.25s}
  .scrim.show{opacity:1;pointer-events:auto}
  .search input{width:40vw}
  .brand-title{display:none}
}
@media (max-width:560px){
  .search input{width:34vw}
  .content{padding:1.1rem .9rem 4rem}
  .stats{grid-template-columns:repeat(auto-fit,minmax(120px,1fr))}
}
@media (prefers-reduced-motion:reduce){
  *{scroll-behavior:auto!important}
  .section{opacity:1;transform:none;transition:none}
}
@media print{
  .topbar,.sidebar,.totop,.progress,.exam-actions,.copy,.scrim,.term-filter{display:none!important}
  body::before{display:none}
  .shell{display:block}
  .content{max-width:none;padding:0}
  .section{opacity:1;transform:none;page-break-inside:avoid}
  .quiz-body{display:block!important}
  .hero,.callout,.table-wrap,.code pre,.example,.quiz,.term{box-shadow:none}
  a{color:inherit}
}
</style>
</head>
<body>
<div class="progress" id="progress" aria-hidden="true"></div>
<header class="topbar">
  <button class="icon-btn menu-btn" id="menuBtn" type="button" aria-label="Open navigation">☰</button>
  <div class="brand"><span class="brand-badge">{{BADGE}}</span><span class="brand-title">{{HEADTITLE}}</span></div>
  <div class="topbar-actions">
    <div class="search">
      <input id="searchInput" type="search" placeholder="Search this guide…" autocomplete="off" aria-label="Search this guide">
      <div class="search-results" id="searchResults" role="listbox"></div>
    </div>
    <button class="icon-btn" id="themeBtn" type="button" aria-label="Toggle light and dark theme">🌙</button>
    <button class="icon-btn" id="printBtn" type="button" aria-label="Print this guide">🖨</button>
  </div>
</header>
<div class="shell">
  <aside class="sidebar" id="sidebar" aria-label="Table of contents">
    <p class="toc-title">Contents</p>
    <ul class="toc">
{{NAV}}
    </ul>
  </aside>
  <div class="scrim" id="scrim"></div>
  <main class="content" id="content">
{{CONTENT}}
    <footer class="foot">{{FOOTER}} · Built for self-paced revision.</footer>
  </main>
</div>
<button class="totop" id="toTop" type="button" aria-label="Back to top">↑</button>
<script>
(function(){
  var GUIDE_ID = "{{GUIDEID}}";
  var root = document.documentElement;
  /* theme */
  var stored = null;
  try { stored = localStorage.getItem("sg-theme"); } catch(e){}
  var prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  setTheme(stored || (prefersDark ? "dark" : "light"));
  function setTheme(t){
    root.setAttribute("data-theme", t);
    var b = document.getElementById("themeBtn");
    if (b) b.textContent = t === "dark" ? "☀️" : "🌙";
    try { localStorage.setItem("sg-theme", t); } catch(e){}
  }
  document.getElementById("themeBtn").addEventListener("click", function(){
    setTheme(root.getAttribute("data-theme") === "dark" ? "light" : "dark");
  });
  document.getElementById("printBtn").addEventListener("click", function(){ window.print(); });

  /* mobile drawer */
  var sidebar = document.getElementById("sidebar"), scrim = document.getElementById("scrim");
  function closeDrawer(){ sidebar.classList.remove("open"); scrim.classList.remove("show"); }
  document.getElementById("menuBtn").addEventListener("click", function(){
    sidebar.classList.toggle("open"); scrim.classList.toggle("show");
  });
  scrim.addEventListener("click", closeDrawer);
  sidebar.addEventListener("click", function(e){ if (e.target.closest("a")) closeDrawer(); });

  /* progress bar + back to top */
  var bar = document.getElementById("progress"), toTop = document.getElementById("toTop");
  function onScroll(){
    var h = document.documentElement;
    var max = h.scrollHeight - h.clientHeight;
    var pct = max > 0 ? (h.scrollTop / max) * 100 : 0;
    bar.style.width = pct + "%";
    toTop.classList.toggle("show", h.scrollTop > 600);
  }
  window.addEventListener("scroll", onScroll, {passive:true});
  onScroll();
  toTop.addEventListener("click", function(){ window.scrollTo({top:0, behavior:"smooth"}); });

  /* active toc + reveal */
  var links = Array.prototype.slice.call(document.querySelectorAll(".toc-link"));
  var sections = Array.prototype.slice.call(document.querySelectorAll(".section"));
  if ("IntersectionObserver" in window) {
    var rev = new IntersectionObserver(function(entries){
      entries.forEach(function(en){ if (en.isIntersecting) en.target.classList.add("in"); });
    }, {rootMargin:"0px 0px -8% 0px", threshold:0.05});
    sections.forEach(function(s){ rev.observe(s); });

    var spy = new IntersectionObserver(function(entries){
      entries.forEach(function(en){
        if (!en.isIntersecting) return;
        var id = en.target.id;
        links.forEach(function(a){ a.classList.toggle("active", a.getAttribute("href") === "#" + id); });
      });
    }, {rootMargin:"-15% 0px -70% 0px", threshold:0});
    sections.forEach(function(s){ spy.observe(s); });
  } else {
    sections.forEach(function(s){ s.classList.add("in"); });
  }

  /* copy buttons */
  document.addEventListener("click", function(e){
    var btn = e.target.closest("[data-copy]");
    if (!btn) return;
    var code = btn.parentElement.querySelector("code");
    if (!code) return;
    var text = code.innerText;
    var done = function(){ btn.textContent = "Copied"; btn.classList.add("done"); setTimeout(function(){ btn.textContent = "Copy"; btn.classList.remove("done"); }, 1400); };
    if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(text).then(done, done); }
    else { var ta = document.createElement("textarea"); ta.value = text; document.body.appendChild(ta); ta.select(); try{document.execCommand("copy");}catch(err){} document.body.removeChild(ta); done(); }
  });

  /* glossary filter */
  var termSearch = document.getElementById("termSearch");
  if (termSearch) {
    var terms = Array.prototype.slice.call(document.querySelectorAll(".term"));
    var count = document.getElementById("termCount");
    var update = function(){
      var q = termSearch.value.trim().toLowerCase();
      var shown = 0;
      terms.forEach(function(t){
        var hit = !q || (t.getAttribute("data-term") || "").indexOf(q) !== -1;
        t.classList.toggle("hide", !hit);
        if (hit) shown++;
      });
      if (count) count.textContent = shown + " / " + terms.length + " shown";
    };
    termSearch.addEventListener("input", update);
    update();
  }

  /* exam interactions */
  var quizzes = Array.prototype.slice.call(document.querySelectorAll(".quiz"));
  quizzes.forEach(function(q){
    var head = q.querySelector(".quiz-q");
    head.addEventListener("click", function(){
      q.classList.toggle("open");
      head.setAttribute("aria-expanded", q.classList.contains("open") ? "true" : "false");
    });
  });
  var doneEl = document.getElementById("examDone"), fillEl = document.getElementById("examFill");
  var boxes = Array.prototype.slice.call(document.querySelectorAll("[data-mastered]"));
  var total = boxes.length;
  function examKey(){ return "sg-exam-" + GUIDE_ID; }
  function loadExam(){
    var data = {};
    try { data = JSON.parse(localStorage.getItem(examKey()) || "{}"); } catch(e){}
    boxes.forEach(function(b){ b.checked = !!data[b.getAttribute("data-mastered")]; });
  }
  function saveExam(){
    var data = {};
    boxes.forEach(function(b){ if (b.checked) data[b.getAttribute("data-mastered")] = 1; });
    try { localStorage.setItem(examKey(), JSON.stringify(data)); } catch(e){}
  }
  function refreshExam(){
    var done = boxes.filter(function(b){ return b.checked; }).length;
    if (doneEl) doneEl.textContent = done;
    if (fillEl) fillEl.style.width = total ? (done / total) * 100 + "%" : "0%";
  }
  boxes.forEach(function(b){ b.addEventListener("change", function(){ saveExam(); refreshExam(); }); });
  if (boxes.length) { loadExam(); refreshExam(); }
  var revealAll = document.getElementById("revealAll");
  var hideAll = document.getElementById("hideAll");
  var resetExam = document.getElementById("resetExam");
  if (revealAll) revealAll.addEventListener("click", function(){ quizzes.forEach(function(q){ q.classList.add("open"); }); });
  if (hideAll) hideAll.addEventListener("click", function(){ quizzes.forEach(function(q){ q.classList.remove("open"); }); });
  if (resetExam) resetExam.addEventListener("click", function(){ boxes.forEach(function(b){ b.checked = false; }); saveExam(); refreshExam(); });

  /* search */
  var input = document.getElementById("searchInput");
  var box = document.getElementById("searchResults");
  var index = sections.map(function(s){
    var h = s.querySelector("h2");
    return { id: s.id, title: h ? h.textContent : "", text: s.innerText.replace(/\s+/g, " ").trim() };
  });
  function runSearch(){
    var q = input.value.trim().toLowerCase();
    box.innerHTML = "";
    if (q.length < 2) { box.classList.remove("open"); return; }
    var hits = index.filter(function(it){ return (it.title + " " + it.text).toLowerCase().indexOf(q) !== -1; }).slice(0, 8);
    if (!hits.length) { box.innerHTML = '<div class="sr-empty">No matches</div>'; box.classList.add("open"); return; }
    hits.forEach(function(it){
      var low = it.text.toLowerCase(), at = low.indexOf(q);
      var snippet = at >= 0 ? it.text.slice(Math.max(0, at - 30), at + 70) : it.title;
      var b = document.createElement("button");
      b.type = "button"; b.className = "sr-item";
      b.innerHTML = "<b></b><span></span>";
      b.querySelector("b").textContent = it.title;
      b.querySelector("span").textContent = "…" + snippet + "…";
      b.addEventListener("click", function(){
        document.getElementById(it.id).scrollIntoView({behavior:"smooth", block:"start"});
        box.classList.remove("open"); input.blur();
      });
      box.appendChild(b);
    });
    box.classList.add("open");
  }
  if (input) {
    input.addEventListener("input", runSearch);
    input.addEventListener("keydown", function(e){
      if (e.key === "Enter") { var first = box.querySelector(".sr-item"); if (first) first.click(); }
      if (e.key === "Escape") { box.classList.remove("open"); input.blur(); }
    });
    document.addEventListener("click", function(e){ if (!e.target.closest(".search")) box.classList.remove("open"); });
  }
})();
</script>
</body>
</html>
"""


def guide_id_for(path: Path) -> str:
    return re.sub(r"[^a-z0-9]+", "-", path.stem.lower()).strip("-")


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print(__doc__)
        return 1
    root = Path(argv[0])
    skip = {"ELEC3609_week2_study_guide.txt"}  # legacy session-less reference source
    count = 0
    for src in sorted(root.rglob("*_study_guide.txt")):
        if src.name in skip:
            continue
        out = src.with_suffix(".html")
        doc = parse(src.read_text(encoding="utf-8"))
        out.write_text(render_doc(doc, guide_id_for(src)), encoding="utf-8")
        count += 1
        print(f"wrote {out} ({out.stat().st_size} bytes)")
    print(f"generated {count} guides")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

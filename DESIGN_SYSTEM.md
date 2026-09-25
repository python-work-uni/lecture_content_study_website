# "Calm Canvas" — Design System for Interactive Study Guides

> Source of truth: the eight interactive study guides in `ENGG2112/lectures/lecture_week_1` … `lecture_week_8`
> (`ENGG2112_weekN_study_guide.html`).

---

## 1. Overview

**Calm Canvas** is the design system behind the ENGG2112 interactive study guides. It is a
self-contained, single-file HTML system: every guide embeds its own copy of the same CSS and
JavaScript, loads three Google fonts, and needs no build step, framework, or network access beyond
the font CDN.

The system is built for one job: **guided reading for active recall**. A student should be able to
open one file, read it top to bottom in about 20 minutes, check their understanding with built-in
questions, and return later with their progress saved.

### Design principles

| Principle | How it shows up |
|---|---|
| **Calm, low-glare reading** | Warm "paper" background, muted palette, generous line-height (1.72), 76ch measure. |
| **Editorial, not corporate** | Serif display face (Fraunces) for titles, sans body (Inter), mono (JetBrains Mono) for math/code. |
| **Guided flow** | Sticky TOC + scrollspy, reading-progress bar, numbered sections, section kickers that frame the point. |
| **Active recall by default** | Reveal-answer quizzes, "Mastered" tracking, confidence checklist, "Pause & predict" prompts. |
| **Progressive disclosure** | Answers, glossary categories, suggestions, and the mobile nav stay hidden until asked for. |
| **Respect the reader** | Light/dark themes, `prefers-reduced-motion`, skip link, keyboard-safe focus, ARIA labels. |
| **Consistency by construction** | Identical CSS in every file; only the week label and storage keys change. |

---

## 2. Scope of the source analysis

| File | Week | Sections | Quizzes | Glossary terms | Takeaways | Check items | CSS bytes |
|---|---|---:|---:|---:|---:|---:|---:|
| `lecture_week_1/ENGG2112_week1_study_guide.html` | 1 | 20 | 12 | 24 | 12 | 10 | 24,620 |
| `lecture_week_2/ENGG2112_week2_study_guide.html` | 2 | 19 | 12 | 20 | 12 | 11 | 24,620 |
| `lecture_week_3/ENGG2112_week3_study_guide.html` | 3 | 21 | 14 | 20 | 12 | 11 | 24,620 |
| `lecture_week_4/ENGG2112_week4_study_guide.html` | 4 | 20 | 14 | 22 | 12 | 15 | 24,620 |
| `lecture_week_5/ENGG2112_week5_study_guide.html` | 5 | 20 | 14 | 24 | 12 | 15 | 24,620 |
| `lecture_week_6/ENGG2112_week6_study_guide.html` | 6 | 20 | 15 | 28 | 12 | 15 | 24,620 |
| `lecture_week_7/ENGG2112_week7_study_guide.html` | 7 | 20 | 12 | 20 | 9 | 11 | 24,620 |
| `lecture_week_8/ENGG2112_week8_study_guide.html` | 8 | 20 | 14 | 20 | 12 | 12 | 24,620 |

**Invariants verified across all eight files**

- The `<style>` block is **byte-for-byte identical** (same length and SHA-256).
- The `<script>` block is identical except for two embedded literals:
  `engg2112-N-mastery` and `engg2112-N-check-`, where `N` is the week number.
- Every guide fixes the same four section anchor IDs: `#takeaways`, `#glossary`, `#practice`,
  `#checklist`.
- The same component vocabulary is used everywhere (see the class inventory in §6).

The design is also reused by sibling courses in this repo (ELEC3609, INFO3616), so treat this
document as the shared spec, not an ENGG2112-only artifact.

---

## 3. Technical foundation

- **One file per guide.** No external CSS/JS. Only external dependency: Google Fonts.
- **HTML5**, `lang="en"`, `data-theme="light"` on `<html>` by default.
- **Vanilla ES5-style JavaScript** in a single IIFE (`"use strict"`), no libraries, no build.
- **Theming** via CSS custom properties on `:root` and `html[data-theme="dark"]`.
- **Persistence** via `localStorage`, wrapped in `try/catch` so it degrades silently.
- **Motion** via a single easing curve `--ease: cubic-bezier(.22,.61,.36,1)`.

### Fonts

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

| Token | Stack | Role |
|---|---|---|
| `--font-display` | `'Fraunces', Georgia, 'Times New Roman', serif` | Page title, section titles, section numbers, question numbers, mnemonics. |
| `--font-body` | `'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif` | All body copy, card titles, UI. |
| `--font-mono` | `'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace` | Formulas, inline `code`. |

---

## 4. Design tokens

All tokens are CSS custom properties declared in `:root` (light) and overridden in
`html[data-theme="dark"]`.

### 4.1 Colour — surfaces & ink

| Token | Light | Dark | Use |
|---|---|---|---|
| `--paper` | `#f4f1ea` | `#171614` | Page background. |
| `--surface` | `#fffdf9` | `#201e1b` | Cards, callouts, topbar, tables. |
| `--surface-2` | `#f8f4ec` | `#262320` | Hover states, zebra rows, hero gradient end. |
| `--surface-3` | `#efe9de` | `#2e2b26` | Table headers, code chips, formula blocks, progress track. |
| `--ink` | `#33302b` | `#ece7df` | Primary text. |
| `--ink-soft` | `#5d574e` | `#bdb6ab` | Secondary text. |
| `--ink-faint` | `#8b8377` | `#8d867b` | Labels, meta, placeholders. |
| `--line` | `#e6dfd3` | `#37332d` | Default borders/dividers. |
| `--line-strong` | `#d7cdbc` | `#484239` | Emphasised borders (buttons, dashed rules). |

### 4.2 Colour — brand palette

| Token | Light | Dark | Typical use |
|---|---|---|---|
| `--primary` | `#3f7d74` | `#7fc3b4` | Brand, active states, progress fill, step bullets. |
| `--primary-deep` | `#2c5d56` | `#a5d8cc` | Links, key terms, accents on light chips. |
| `--primary-soft` | `#e3efeb` | `#21322e` | Tinted backgrounds (active TOC, mastery fill). |
| `--accent` | `#b4663f` | `#e0a07b` | Warm counterpoint: kickers, sub-title dashes, question numbers, arrows. |
| `--accent-soft` | `#f7e8e0` | `#33241d` | Accent tint. |
| `--gold` | `#9c7a28` | `#e0c183` | Highlights (`--gold-soft`). |
| `--gold-soft` | `#f6efdc` | `#332b1a` | `.hl` highlight, "why" callout. |
| `--violet` | `#6c60ab` | `#b3a9e6` | Mnemonics, "memory" callout. |
| `--violet-soft` | `#ece9f7` | `#282343` | Violet tint. |
| `--blue` | `#3f6f8e` | `#9cc4dc` | "Info" callout. |
| `--blue-soft` | `#e7f0f5` | `#1e2c36` | Blue tint. |
| `--rose` | `#ab4f55` | `#e6a3a8` | Warnings. |
| `--rose-soft` | `#f8e8e9` | `#362223` | "Warn" callout. |

### 4.3 Colour — semantic callout tokens

Each callout variant sets three local variables (`--c-bg`, `--c-line`, `--c-fg`) that the base
`.callout` rule consumes. This indirection is what lets the five variants share one component.

| Variant | Light bg / line / fg | Dark bg / line / fg | Meaning | Icon |
|---|---|---|---|---|
| `.c-info` | `#e7f0f5` / `#c6dbe8` / `#2f5d79` | `#1e2c36` / `#2d4354` / `#a9cfe4` | Context, logistics, previews | ℹ️ |
| `.c-why` | `#f6efdc` / `#e8dbb4` / `#7d6220` | `#332b1a` / `#4a3f24` / `#e3c98d` | Motivation ("Why it matters") | 💡 |
| `.c-memory` | `#ece9f7` / `#d6cff0` / `#574c94` | `#282343` / `#3c3563` / `#bdb3ec` | Mnemonics, "Remember" | 🧠 |
| `.c-tip` | `#e3efeb` / `#c2ded6` / `#2c5d56` | `#21322e` / `#2f4a43` / `#93cec1` | Actionable advice | ✅ |
| `.c-warn` | `#f8e8e9` / `#ecccce` / `#8f3f45` | `#362223` / `#4d3032` / `#e6adb1` | Traps and warnings | ⚠️ |

> Note: `.c-why` reuses the "why" framing but pairs it with the 💡 icon, while `.c-memory` uses 🧠.
> Keep these pairings when authoring.

### 4.4 Shape, depth & layout

| Token | Value | Use |
|---|---|---|
| `--radius` | `18px` | Cards, callouts' larger siblings, tables, quiz, hero. |
| `--radius-sm` | `11px` | Pills' container, callouts, def-cards, term cards, inputs. |
| `--shadow-sm` | `0 1px 2px rgba(60,50,40,.05)` | Resting cards. |
| `--shadow` | `0 8px 24px -12px rgba(60,50,40,.22)` | Hover elevation, topbar-adjacent surfaces. |
| `--shadow-lg` | `0 24px 60px -28px rgba(60,50,40,.35)` | Search suggestions, mobile sidebar. |
| `--sidebar-w` | `300px` | Sticky TOC column. |
| `--measure` | `76ch` | Max reading width of `.content`. |
| `--ease` | `cubic-bezier(.22,.61,.36,1)` | All transitions. |

Global layout constants are hard-coded (not tokens): topbar height `62px`, layout max width
`1280px`, reading-progress bar `3px`.

---

## 5. Page anatomy

```text
<body>
  a.skip-link                      → "Skip to content"
  .progress-track > .progress-fill → fixed 3px reading-progress bar
  header.topbar                    → menu toggle · brand · search · theme toggle
  .layout                          → grid: [ .sidebar | main.content ]
    aside.sidebar                  → recall progress · TOC · quick links
    .scrim                         → mobile nav overlay
    main.content#content
      section.hero                 → eyebrow, title, sub, lead, meta chips, outcomes
      section.guide-section#...     → repeated ~20 times (auto-numbered)
        (takeaways | glossary | practice | checklist are also .guide-section)
  footer.site-footer               → prev/next nav + disclaimer
  button.to-top                    → appears after 500px scroll
  <script>                         → all behaviour
</body>
```

### Grid

```css
.layout{
  display:grid;
  grid-template-columns:var(--sidebar-w) minmax(0,1fr);
  gap:clamp(1.2rem,3vw,3rem);
  max-width:1280px;margin:0 auto;
  padding:0 clamp(.9rem,3vw,2rem);
}
```

### Stable IDs

Every guide exposes these anchors for cross-linking and for the hard-coded sidebar quick links:

- `#content` — main region (skip-link target)
- `#top` — hero
- `#takeaways`, `#glossary`, `#practice`, `#checklist`
- Each `.guide-section` gets an author-supplied `id`, or the script auto-assigns `sec-N`.

---

## 6. Component library

Class inventory across the eight guides (occurrence count in parentheses) confirms the full
vocabulary: `guide-section` (160), `term-card` (178), `sub-title` (170), `callout` (146),
`card` (152), `quiz` (107), `takeaway` (93), `check-item` (100), `def-card` (43), `formula` (43),
`table-wrap` (44), `mnemonic` (24), `flow-step` (106), `reflect` (40).

### 6.1 Callouts

```html
<div class="callout c-warn">
  <div class="callout-icon" aria-hidden="true">⚠️</div>
  <div class="callout-body"><strong>Common trap:</strong> …</div>
</div>
```

Base rule (variants only swap the three local variables):

```css
.callout{
  display:flex;gap:.85rem;align-items:flex-start;
  border:1px solid var(--c-line);background:var(--c-bg);
  border-radius:var(--radius-sm);padding:.95rem 1.1rem;margin:1.2rem 0;
}
.callout-body strong:first-child{color:var(--c-fg);}
```

Conventional lead labels observed in the source: **Common trap** (warn), **Why it matters** (why),
**Do this / Key idea / Exam tip** (tip), **Remember / Memory hook** (memory).

### 6.2 Reflection prompt

```html
<div class="reflect">
  <span class="ri" aria-hidden="true">🤔</span>
  <div><strong>Pause &amp; predict:</strong> …</div>
</div>
```

Dashed border with a solid `--accent` left edge; `.reflect strong` is always coloured `--accent`.
Used to force retrieval *before* the next section.

### 6.3 Section scaffolding

```html
<section class="guide-section" id="some-id" data-title="Short TOC Label">
  <div class="section-head">
    <span class="sec-num" aria-hidden="true"></span>   <!-- CSS counter prints 01, 02, … -->
    <h2 class="section-title">Full Section Heading</h2>
  </div>
  <p class="section-kicker">The one-sentence point of this section.</p>
  …
  <h3 class="sub-title">Sub-heading with accent dash</h3>
  <h4 class="sub-sub">Tertiary heading (rare)</h4>
</section>
```

- **Auto-numbering**: `.content{counter-reset:sec}` and `.guide-section{counter-increment:sec}`;
  `.sec-num::before{content:counter(sec,decimal-leading-zero)}`. Never type section numbers by hand.
- `data-title` is the short label used in the TOC and search; the script falls back to
  `.section-title` text if it is absent.
- `.lede` (used sparingly, ~1 per guide) marks a large opening paragraph; `.muted` de-emphasises.

Inline text utilities: `.keyterm` (bold brand word), `.hl` (gold highlight), `<code>` (mono chip),
`<strong>` (weight 650), `<em>` (italic).

### 6.4 Card grids

```html
<div class="grid grid-2">                <!-- or grid-3; grid alone is single column -->
  <div class="card">
    <h3 class="card-title">🧮 Title</h3>
    <p>…</p>
  </div>
</div>
```

- `.grid-2` → `repeat(auto-fit,minmax(240px,1fr))`
- `.grid-3` → `repeat(auto-fit,minmax(190px,1fr))`
- Cards lift on hover (`translateY(-2px)` + `--shadow`).
- `.tag` is an inline pill used inside a card title, e.g.
  `<h3 class="card-title"><span class="tag">concept</span> GAN</h3>`.

### 6.5 Definition card

```html
<div class="def-card">
  <span class="dc-term">Data leakage</span> — the explanation, in one tight paragraph.
</div>
```

Left-edge `--primary` rule. Used for glossary-in-flow definitions when a term needs more context
than the end-of-page glossary allows.

### 6.6 Tables

```html
<div class="table-wrap">
  <table>
    <thead><tr><th>Assessment</th><th>Week</th><th>Weight</th><th>Type</th></tr></thead>
    <tbody>
      <tr><td><strong>Final exam</strong></td><td>Exam period</td><td>40%</td><td>Secure</td></tr>
    </tbody>
  </table>
</div>
```

`.table-wrap` handles horizontal overflow on narrow screens. First column is bolded; even rows are
tinted; `thead th` is `white-space:nowrap`.

### 6.7 Formula block

```html
<div class="formula">
  <div class="formula-label">The hurdle</div>
  <div class="math">compulsory attendance ≥ 80% of tutorials</div>
</div>
```

Centred, `--surface-3` background. `.math` sets the mono face; it is also used inline (e.g.
`<span class="math">P[y | x]</span>`) for symbols inside prose.

### 6.8 Steps (ordered procedure)

```html
<ol class="steps">
  <li><strong>Find one other person</strong> you want to be grouped with.</li>
  <li><strong>Submit both names</strong> to your tutor by the end of tutorial two.</li>
</ol>
```

Custom counters draw numbered circles with a connecting rail; use for genuine sequences (pipeline
steps, procedures, learning-objective lists).

### 6.9 Flow (horizontal pipeline)

```html
<div class="flow">
  <span class="flow-step">Model</span><span class="flow-arrow">→</span>
  <span class="flow-step">Train</span><span class="flow-arrow">→</span>
  <span class="flow-step">Deploy</span>
</div>
```

Rounded pill steps joined by accent arrows; wraps on small screens. This is the signature component
for "the lecture on one map" summaries.

### 6.10 Compare (two-column contrast)

```html
<div class="compare">
  <div class="compare-col a"><h3>Previous versions</h3><ul>…</ul></div>
  <div class="compare-col b"><h3>New version</h3><ul>…</ul></div>
</div>
```

`.a` gets a `--primary` top border, `.b` an `--accent` top border. Auto-fits at 220px minimum.

### 6.11 Mnemonic

```html
<div class="mnemonic">
  <div class="mnemonic-letters">P · A · T</div>
  <div class="mnemonic-phrase">"Pick, Add, Tell"</div>
  <div class="mnemonic-expand"><strong>P</strong>ick one partner · <strong>A</strong>dd a pair · <strong>T</strong>ell your tutor.</div>
</div>
```

Violet gradient panel; letters are widely tracked in the display face. Reserve for genuinely catchy
memory hooks.

### 6.12 Key takeaways

```html
<div class="takeaways">
  <div class="takeaway"><span class="tk-num">1</span><p><strong>…</strong> …</p></div>
</div>
```

Numbered circles on the left. Every guide ends its reading with a `#takeaways` section (9–12 items);
this is the "if you remember nothing else" list.

### 6.13 Glossary

```html
<div class="glossary-tools">
  <button class="chip active" type="button" data-cat="all">All</button>
  <button class="chip" type="button" data-cat="concept">Core concepts</button>
  <button class="chip" type="button" data-cat="method">Methods &amp; process</button>
  <button class="chip" type="button" data-cat="metric">Metrics &amp; evaluation</button>
</div>
<div class="terms">
  <div class="term-card" data-cat="concept">
    <div class="term-name">Generalisation</div>
    <div class="term-meaning">…</div>
  </div>
</div>
<p class="empty-note" id="glossaryEmpty">No terms in this category.</p>
```

- Chips are mutually exclusive filters keyed on `data-cat`; `.active` marks the current filter.
- Cards in the active category get `.hidden{display:none}`.
- Categories are extensible per week (e.g. `concept`, `method`, `metric`).

### 6.14 Quiz (active recall)

```html
<article class="quiz" id="q1">
  <div class="quiz-head">
    <span class="quiz-qnum">Q1</span>
    <p class="quiz-q">Question text…</p>
  </div>
  <div class="quiz-answer"><strong>Answer:</strong> …</div>
  <div class="quiz-actions">
    <button class="quiz-reveal" type="button">Show answer</button>
    <label class="mastered"><input type="checkbox"> Mastered</label>
  </div>
</article>
```

- Clicking `.quiz-head` **or** `.quiz-reveal` toggles `.open` on the `.quiz`, showing
  `.quiz-answer`.
- Checking "Mastered" adds `.done` (brand-tinted card) and persists via localStorage.
- Toolbar above the set:

```html
<div class="quiz-toolbar">
  <span class="progress-copy" id="quizProgressCopy">Answer, reveal, then tick "Mastered". Your progress is saved.</span>
  <button class="btn" id="revealAll" type="button">Reveal all</button>
  <button class="btn" id="hideAll" type="button">Hide all</button>
  <button class="btn" id="resetProgress" type="button">Reset</button>
</div>
```

Buttons: `.btn` (ghost) and `.btn-primary` (filled brand) share pill geometry.

### 6.15 Confidence checklist

```html
<div class="checklist">
  <label class="check-item"><input type="checkbox"> I can explain …</label>
</div>
```

Checked rows tint with `--primary-soft` via `:has(input:checked)`. Each box persists independently.
Phrase items as "I can …" statements a student could say aloud.

### 6.16 Topbar

```html
<header class="topbar">
  <button class="icon-btn menu-toggle" id="menuToggle" aria-label="Open navigation" aria-expanded="false">☰</button>
  <a class="brand" href="../../../index.html">
    <span class="brand-course">ENGG2112</span>
    <span class="brand-week">Week 1</span>
  </a>
  <div class="topbar-tools">
    <div class="search">
      <span class="search-icon" aria-hidden="true">⌕</span>
      <input id="searchInput" type="search" placeholder="Search guide…" aria-label="Search this study guide" autocomplete="off">
      <div class="suggest" id="suggest" role="listbox" aria-label="Search results"></div>
    </div>
    <button class="icon-btn" id="themeToggle" aria-label="Toggle night mode" title="Toggle night mode">◐</button>
  </div>
</header>
```

Sticky, translucent (`color-mix` + `backdrop-filter: blur(12px)`), 62px tall. `.menu-toggle` is
hidden above 980px.

### 6.17 Sidebar

```html
<aside class="sidebar" id="sidebar" aria-label="Table of contents">
  <div class="sidebar-inner">
    <div class="sidebar-progress">
      <div class="sidebar-progress-label"><span>Recall progress</span><span id="masteryLabel">0 / 0</span></div>
      <div class="bar"><div class="bar-fill" id="masteryFill"></div></div>
    </div>
    <p class="toc-title">On this page</p>
    <nav class="toc" id="toc"></nav>          <!-- populated by script -->
    <div class="sidebar-links">
      <a href="#takeaways">★ Key takeaways</a>
      <a href="#glossary">▦ Glossary</a>
      <a href="#practice">✎ Practice questions</a>
      <a href="#checklist">☑ Confidence check</a>
    </div>
  </div>
</aside>
```

`.toc a` entries carry a two-digit `.n` prefix; `.active` marks the section currently in view.
`.sidebar-links` is the fixed quick-jump block.

### 6.18 Hero

```html
<section class="hero" id="top">
  <span class="hero-eyebrow">ENGG2112 · Week 1 · Unit Overview &amp; AI/ML Foundations</span>
  <h1 class="hero-title">…</h1>
  <p class="hero-sub">A one-paragraph abstract of the week.</p>
  <div class="hero-lead"><strong>Read this first:</strong> the single mental model to hold.</div>
  <div class="hero-meta">
    <span class="meta-chip"><span class="dot"></span>~20 min read</span>
    <span class="meta-chip">16 teaching sections</span>
    <span class="meta-chip">12 practice questions</span>
    <span class="meta-chip">24 key terms</span>
  </div>
  <div class="hero-outcomes">
    <h2>By the end you will be able to</h2>
    <ul class="outcome-list"><li>…</li></ul>
  </div>
</section>
```

A soft radial brand glow sits in the top-right (`::after`). The outcomes list prefixes each item
with a brand-coloured ✓. Meta chips should reflect the actual counts in that guide.

### 6.19 Footer & back-to-top

```html
<footer class="site-footer">
  <div class="footer-nav">
    <a href="../../../index.html">⌂ All guides</a>
    <span class="spacer"></span>
    <a href="../lecture_week_2/ENGG2112_week2_study_guide.html">Week 2 →</a>
    <span class="spacer"></span>
  </div>
  <p>ENGG2112 Multi-Disciplinary Engineering · Week 1 · Independent study guide for active recall. Always reconcile with the official lecture material.</p>
</footer>
<button class="to-top" id="toTop" aria-label="Back to top">↑</button>
```

`.to-top` fades in after 500px of scroll; footer links use relative paths back to the repo root
`index.html`.

---

## 7. Interaction & behaviour contract

All behaviour lives in one IIFE at the end of `<body>`. Order of concerns:

1. **Theme** — reads `localStorage['engg2112-theme']`; falls back to
   `prefers-color-scheme: dark`; the toggle flips `data-theme` and persists it.
2. **Mobile nav** — toggles `body.nav-open`, syncs `aria-expanded`, shows/hides `.scrim`.
3. **TOC build** — iterates `.guide-section`, uses `data-title` (or `.section-title`), assigns
   `sec-N` ids when missing, prepends zero-padded numbers.
4. **Scrollspy + reading progress** — `scroll` handler sets `.progress-fill` width and toggles
   `.to-top`; an `IntersectionObserver` (`rootMargin:-80px 0px -55% 0px`) tracks the most visible
   section and marks the matching `.toc-link.active`.
5. **Quizzes** — click-to-reveal, "Mastered" persistence, and `Reveal all` / `Hide all` / `Reset`.
6. **Glossary filter** — chip click filters `.term-card` by `data-cat`; shows `.empty-note` when a
   category is empty.
7. **Search** — token `input`/`focus` matches section text + glossary terms, de-dupes, caps at 12
   results, renders `.suggest a` links; a document click outside `.search` closes the panel.
8. **Checklist persistence** — saves each checkbox by index.

### LocalStorage keys

| Key | Scope |
|---|---|
| `engg2112-theme` | Shared across all guides (`light` \| `dark`). |
| `engg2112-{week}-mastery:{quizId}` | Per quiz, per week. |
| `engg2112-{week}-check-{index}` | Per checklist item, per week. |

> When cloning the template to a new week, update the two `{week}` literals in the script. All
> other JS and CSS should remain untouched.

---

## 8. Accessibility

- `.skip-link` jumps to `#content` and only becomes visible on focus.
- Semantic landmarks: `<header>`, `<aside aria-label="Table of contents">`, `<main id="content">`,
  `<footer>`.
- Decorative `aria-hidden="true"` on all emoji icons, counters, and the progress bar.
- The search input has `type="search"` and `aria-label`; the suggestion panel is a `role="listbox"`.
- The theme button exposes `aria-label` + `title`; the menu button manages `aria-expanded`.
- Visible focus is preserved (native outlines; custom focus ring on search: 4px `--primary-soft`
  halo).
- `@media (prefers-reduced-motion:reduce)` zeroes animations/transitions and disables smooth
  scrolling.
- Contrast: body copy is `--ink` on `--paper`/`--surface`; each callout pairs its tint with a
  darker `--c-fg` heading colour and a matching border.

---

## 9. Responsive behaviour

| Breakpoint | Change |
|---|---|
| `> 980px` | Two-column grid; sticky sidebar; `.menu-toggle` hidden. |
| `≤ 980px` | Single column; sidebar becomes an off-canvas drawer (`translateX(-104%)`, `.nav-open` slides it in); `.scrim` overlay active. |
| `≤ 600px` | Body font 16px; search widens to 44vw; `.brand-week` hidden; hero padding tightened. |
| `prefers-reduced-motion` | All transitions/animations reduced to ~0; smooth scroll off. |

The table wrapper scrolls horizontally rather than squeezing columns.

---

## 10. Content & authoring conventions

**Page metadata**

```html
<meta name="description" content="ENGG2112 Week N study guide — a calm, complete walkthrough designed for first-time readers and active recall.">
<title>ENGG2112 Week N — Full lecture title</title>
```

**Section flow for a typical week**

1. Hero (eyebrow, title, sub, "Read this first" lead, meta chips, outcomes)
2. ~10–14 teaching `guide-section`s, each opened by a `.section-kicker` and supported by callouts,
   cards, tables, formulas, steps, flows, compare columns, mnemonics, and `def-card`s
3. `#takeaways` — 9–12 numbered points
4. `#glossary` — 20–28 `data-cat`-tagged terms
5. `#practice` — 12–15 reveal-answer questions
6. `#checklist` — 10–15 "I can …" statements
7. Footer with prev/next week links

**Voice & formatting**

- Address the reader as "you"; use "we" for the course/lecture.
- `.section-kicker` is always one italic sentence stating the section's takeaway.
- Bold the load-bearing noun in a sentence (`<strong>`), not whole clauses.
- Use emoji as *semantic markers only* on card/callout headings and meta chips — never in running
  prose.
- Keep quiz questions open-ended (explain/contrast/define), with a model answer that names the
  concept explicitly.
- End the guide with the disclaimer line: "Always reconcile with the official lecture material."

**Counting discipline** — hero meta chips must match reality; if you add a section, question, or
term, update the chip and the outcomes list.

---

## 11. Extending the system

- **New week:** copy an existing guide, replace content, and update exactly two script literals
  (`engg2112-N-mastery`, `engg2112-N-check-`) plus the week label in the topbar, title, hero, and
  footer links. Do not restyle.
- **New component:** add CSS only if it reuses existing tokens (`--surface*`, `--ink*`, `--line*`,
  `--radius*`, `--shadow*`, `--ease`). Prefer composing existing primitives (callout, card, flow,
  steps) before inventing a new one.
- **New glossary category:** add a `.chip` with a matching `data-cat` and tag the relevant
  `.term-card`s. No JS change needed.
- **New theme:** define the full token set under a new `html[data-theme="..."]` selector; the base
  rules require no edits.

---

## 12. Quick-reference cheat sheet

```css
/* Typography */
display : 'Fraunces', Georgia, serif
body    : 'Inter', system-ui, sans-serif  (16.5px / 1.72)
mono    : 'JetBrains Mono', monospace

/* Core surfaces (light → dark) */
--paper        #f4f1ea → #171614
--surface      #fffdf9 → #201e1b
--surface-2    #f8f4ec → #262320
--surface-3    #efe9de → #2e2b26
--ink          #33302b → #ece7df
--ink-soft     #5d574e → #bdb6ab
--line         #e6dfd3 → #37332d

/* Brand */
--primary      #3f7d74 → #7fc3b4
--primary-deep #2c5d56 → #a5d8cc
--accent       #b4663f → #e0a07b

/* Shape */
--radius 18px · --radius-sm 11px
--measure 76ch · --sidebar-w 300px
--ease cubic-bezier(.22,.61,.36,1)

/* Callout variants: add .c-info | .c-why | .c-memory | .c-tip | .c-warn */
/* Section shell: <section class="guide-section" data-title="…"> + .section-head + .sec-num */
/* Answer reveal: .quiz > .quiz-head/.quiz-answer/.quiz-actions, toggle .open; mark .done */
/* Themes: light default ·  <html data-theme="dark">  ·  toggle persists engg2112-theme */
```

---

*Maintained alongside the guides in this repository. The CSS block is the canonical implementation —
when this document and the code disagree, the code wins.*

# HTML Study Guide Design Specification

> Reference document extracted from `Week1_StudyGuide.html`. Use this as the canonical design template when building future weekly study guides.

---

## Table of Contents

1. [Technology Stack](#1-technology-stack)
2. [CSS Design Tokens](#2-css-design-tokens)
3. [Page Layout](#3-page-layout)
4. [Component Library](#4-component-library)
5. [Interactive JavaScript Features](#5-interactive-javascript-features)
6. [Content Structure](#6-content-structure)
7. [Responsive and Print Behaviour](#7-responsive-and-print-behaviour)
8. [Replication Checklist](#8-replication-checklist)

---

## 1. Technology Stack

| Dependency | Purpose | CDN / Source |
|---|---|---|
| **Plus Jakarta Sans** | Body / UI font | `fonts.googleapis.com` — weights 300, 400, 500, 600, 700, 800 + italic 400 |
| **JetBrains Mono** | Code, numbers, monospace elements | `fonts.googleapis.com` — weights 400, 500, 600, 700 |
| **KaTeX 0.16.8** | Math / formula rendering | `cdn.jsdelivr.net/npm/katex@0.16.8` |
| KaTeX auto-render | Processes `$...$` and `$$...$$` delimiters automatically | Loaded via `onload` on the auto-render script |

No build tools, frameworks, or bundlers. Everything is a single self-contained `.html` file.

---

## 2. CSS Design Tokens

All values are stored as CSS custom properties on `:root` and overridden by `[data-theme="dark"]`.

### 2.1 Fonts

```css
--font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
--font-mono: 'JetBrains Mono', monospace;
```

### 2.2 Light Theme (Default)

```css
/* Backgrounds */
--bg-primary:  #f8fafc;   /* page background */
--bg-surface:  #ffffff;   /* cards, panels */
--bg-subtle:   #f1f5f9;   /* table headers, inputs */
--bg-alt:      #e2e8f0;   /* hover states */

/* Borders */
--border-color: #e2e8f0;
--border-focus: #6366f1;

/* Text */
--text-main:   #0f172a;
--text-muted:  #64748b;
--text-light:  #94a3b8;

/* Primary — indigo */
--primary:       #4f46e5;
--primary-hover: #4338ca;
--primary-light: #eef2ff;
--primary-glow:  rgba(79, 70, 229, 0.15);

/* Accent colours */
--accent-blue:        #0284c7;    --accent-blue-bg:    #e0f2fe;
--accent-emerald:     #059669;    --accent-emerald-bg: #d1fae5;
--accent-amber:       #d97706;    --accent-amber-bg:   #fef3c7;
--accent-rose:        #e11d48;    --accent-rose-bg:    #ffe4e6;
--accent-purple:      #7c3aed;    --accent-purple-bg:  #ede9fe;

/* Shadows and glass */
--card-shadow:       0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -2px rgba(0,0,0,0.05);
--card-shadow-hover: 0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -4px rgba(0,0,0,0.04);
--glass-bg:     rgba(255, 255, 255, 0.85);
--glass-border: rgba(255, 255, 255, 0.6);

/* Layout */
--nav-width: 280px;
```

### 2.3 Dark Theme (`[data-theme="dark"]`)

```css
--bg-primary:  #0b0f19;
--bg-surface:  #131b2e;
--bg-subtle:   #1e293b;
--bg-alt:      #334155;

--border-color: #1e293b;
--border-focus: #818cf8;

--text-main:   #f8fafc;
--text-muted:  #94a3b8;
--text-light:  #64748b;

--primary:       #6366f1;
--primary-hover: #818cf8;
--primary-light: rgba(99, 102, 241, 0.15);
--primary-glow:  rgba(99, 102, 241, 0.25);

/* Accent bg colours become rgba(color, 0.15) variants in dark mode */
--accent-blue:    #38bdf8;    --accent-blue-bg:    rgba(56,189,248,0.15);
--accent-emerald: #34d399;    --accent-emerald-bg: rgba(52,211,153,0.15);
--accent-amber:   #fbbf24;    --accent-amber-bg:   rgba(251,191,36,0.15);
--accent-rose:    #fb7185;    --accent-rose-bg:    rgba(251,113,133,0.15);
--accent-purple:  #a78bfa;    --accent-purple-bg:  rgba(167,139,250,0.15);

--card-shadow:       0 4px 6px -1px rgba(0,0,0,0.3);
--card-shadow-hover: 0 10px 20px -3px rgba(0,0,0,0.5);
--glass-bg:     rgba(19, 27, 46, 0.85);
--glass-border: rgba(255, 255, 255, 0.08);
```

---

## 3. Page Layout

### 3.1 Global Base

```css
html { scroll-behavior: smooth; font-size: 16px; }
body {
  font-family: var(--font-sans);
  line-height: 1.65;
  -webkit-font-smoothing: antialiased;
  transition: background-color 0.25s ease, color 0.25s ease;
}
```

### 3.2 Reading Progress Bar

A fixed 3 px gradient bar pinned to the very top of the viewport (`z-index: 1000`). Its width is updated on every scroll event via JavaScript.

```css
#progress-bar {
  position: fixed; top: 0; left: 0; height: 3px;
  background: linear-gradient(90deg, #4f46e5, #06b6d4, #10b981);
  width: 0%; z-index: 1000; transition: width 0.1s ease-out;
}
```

Place `<div id="progress-bar"></div>` as the **first child** of `<body>`.

### 3.3 Sticky Header (`header.site-header`)

```css
position: sticky; top: 0; z-index: 900;
backdrop-filter: blur(12px);
background: var(--glass-bg);
border-bottom: 1px solid var(--border-color);
padding: 0.75rem 1.5rem;
display: flex; align-items: center; justify-content: space-between;
```

Header inner structure (left to right):

| Element | Class / ID | Notes |
|---|---|---|
| Mobile menu toggle button | `.menu-toggle` | `display: none` on desktop; shown at ≤1024 px |
| Course badge pill | `.course-badge` | Primary-light bg, primary text, uppercase, 0.8 rem |
| Week title | `.header-title` | Bold, overflow ellipsis |
| Search input | `.search-box input` | Rounded, expands 180 px → 240 px on focus |
| Theme toggle | `#theme-toggle .btn-icon` | 36×36 px, swaps ☀️/🌙, triggers `applyTheme()` |
| Print button | `.btn-icon` with `onclick="window.print()"` | 36×36 px |

### 3.4 Two-Column App Container

```css
.app-container { display: flex; max-width: 1520px; margin: 0 auto; }
```

| Column | Element | Key CSS |
|---|---|---|
| Left sidebar | `aside.sidebar` | `width: 280px; position: sticky; top: 57px; height: calc(100vh - 57px); overflow-y: auto; border-right` |
| Main content | `main.main-content` | `flex: 1; padding: 2.5rem 3rem; max-width: 1020px` |

### 3.5 Sidebar Navigation

```html
<aside class="sidebar" id="sidebar">
  <div class="sidebar-header">Table of Contents</div>
  <ul class="nav-list">
    <li><a href="#overview" class="nav-link"><span class="nav-num">00</span> Overview</a></li>
    <li><a href="#section-1" class="nav-link"><span class="nav-num">01</span> Section Title</a></li>
    <!-- ... -->
  </ul>
</aside>
```

- `.nav-link` — `border-radius: 8px`, smooth colour transition on hover/active
- `.nav-link.active` — `color: var(--primary); background: var(--primary-light); font-weight: 600`
- `.nav-num` — monospace, 0.75 rem, 70% opacity — always zero-padded (00, 01, 02…)

---

## 4. Component Library

### 4.1 Hero Banner (Overview Card)

The **first** content block. Uses `class="hero-card"` (not `guide-section`).

```html
<section id="overview" class="hero-card">
  <div class="hero-tagline">📖 Official Course Notes • Semester —</div>
  <h1 class="hero-title">Week N — Topic Title</h1>
  <p class="hero-subtitle">One-sentence summary of the week.</p>
  <div class="hero-overview">
    <strong>Lecture Overview:</strong> Extended paragraph summary…
  </div>
</section>
```

CSS highlights:
- Background: `linear-gradient(135deg, rgba(79,70,229,0.08) 0%, rgba(6,182,212,0.08) 100%)`
- `border-radius: 16px; padding: 2.5rem; overflow: hidden`
- `::before` pseudo: radial gradient glow positioned top-right

Optional `.quick-stats` grid of `.stat-pill` chips can follow the overview for metadata (section count, key term count, etc.).

### 4.2 Guide Section

```html
<section id="section-N" class="guide-section">
  <div class="section-header">
    <span class="section-number">01</span>
    <h2 class="section-title">Section Title</h2>
  </div>
  <!-- body content -->
</section>
```

Key CSS:
- `margin-bottom: 3.5rem; scroll-margin-top: 80px`
- `.section-header`: `border-bottom: 2px solid var(--border-color); margin-bottom: 1.5rem`
- `.section-number`: primary bg, white text, monospace, `border-radius: 6px`
- `h2.section-title`: `font-size: 1.5rem; font-weight: 800`
- `h3.subsection-title`: `font-size: 1.15rem; font-weight: 700; margin: 1.75rem 0 0.75rem`

### 4.3 Cards

Basic content container with hover elevation effect.

```css
.card {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.25rem;
  box-shadow: var(--card-shadow);
  transition: box-shadow 0.2s ease;
}
.card:hover { box-shadow: var(--card-shadow-hover); }
```

**Grid wrappers:**

```html
<div class="grid-2"> <!-- two equal columns, gap 1.25rem --> </div>
<div class="grid-3"> <!-- auto-fit minmax(260px, 1fr), gap 1.25rem --> </div>
```

### 4.4 Callout Boxes

Five semantic variants. Each has a 4 px left border, an emoji icon, and a tinted background.

```html
<div class="callout callout-TYPE">
  <div class="callout-icon">EMOJI</div>
  <div class="callout-content">
    <strong>Bold title:</strong> Body text.
  </div>
</div>
```

| Modifier class | Left border token | Background token | Recommended use |
|---|---|---|---|
| `callout-why` | `--accent-amber` | `--accent-amber-bg` | 💡 Insights, key ideas, historical examples |
| `callout-memory` | `--accent-purple` | `--accent-purple-bg` | 🧠 Definitions to memorise |
| `callout-tip` | `--accent-emerald` | `--accent-emerald-bg` | ✅ Tips, best practices |
| `callout-warning` | `--accent-rose` | `--accent-rose-bg` | ⚠️ Warnings, common pitfalls |
| `callout-info` | `--accent-blue` | `--accent-blue-bg` | ℹ️ Context, neutral notes |

### 4.5 Formula / Math Block

```html
<div class="formula-block">
  <div class="formula-title">FORMULA NAME</div>
  <div class="formula-math">$$ \LaTeX\ expression $$</div>
</div>
```

- `.formula-title`: absolutely positioned top-left primary-coloured badge label
- `.formula-math`: rendered by KaTeX auto-render; `overflow-x: auto` for wide expressions

### 4.6 Tables

```html
<div class="table-container">
  <table class="study-table">
    <thead><tr><th>Col A</th><th>Col B</th></tr></thead>
    <tbody>
      <tr><td>Data</td><td>Data</td></tr>
    </tbody>
  </table>
</div>
```

- `.table-container`: `border-radius: 10px; border; box-shadow; overflow-x: auto`
- `th`: `background: var(--bg-subtle); font-weight: 700`
- `tr:hover td`: `background: var(--bg-subtle)`
- Last row: no bottom border

### 4.7 Badges

Inline chips for labels. Use predefined classes or inline styles for custom colours.

```html
<span class="badge badge-recall">RECALL</span>
<!-- custom colour: -->
<span class="badge" style="background:var(--accent-blue-bg); color:var(--accent-blue);">Label</span>
```

| Class | Colour |
|---|---|
| `badge-recall` | Emerald |
| `badge-precision` | Blue |
| `badge-f1` | Purple |
| `badge-danger` | Rose |

### 4.8 Key Takeaways List

```html
<div class="takeaways-list">
  <div class="takeaway-item">
    <span class="takeaway-num">1</span>
    <div><strong>Bold lead-in</strong> — rest of takeaway text.</div>
  </div>
  <!-- repeat for each takeaway -->
</div>
```

- `.takeaway-num`: circular badge, 26×26 px, `--primary-light` bg, `--primary` text

### 4.9 Glossary / Terms Grid

```html
<!-- Filter chips -->
<div class="glossary-controls">
  <button class="filter-chip active" onclick="filterTerms('all', this)">All (35)</button>
  <button class="filter-chip" onclick="filterTerms('models', this)">Models</button>
  <button class="filter-chip" onclick="filterTerms('pipeline', this)">Pipeline</button>
  <button class="filter-chip" onclick="filterTerms('metrics', this)">Metrics</button>
</div>

<!-- Grid of term cards -->
<div class="terms-grid" id="terms-container">
  <div class="term-card" data-cat="pipeline">
    <div>
      <div class="term-title">
        Term Name
        <span class="badge" style="background:var(--accent-blue-bg); color:var(--accent-blue);">Pipeline</span>
      </div>
      <div class="term-desc">Concise definition, 1–2 sentences.</div>
    </div>
  </div>
</div>
```

- `.terms-grid`: `repeat(auto-fill, minmax(280px, 1fr))`
- `.term-card:hover`: border colour → `--primary`, slight upward translate (-2 px)
- Category values must match the string passed to `filterTerms()`

### 4.10 Mnemonics Cards

Place `.card` elements in a `.grid-2`. Each card uses a coloured `h3.subsection-title` and muted body text.

```html
<div class="grid-2">
  <div class="card">
    <h3 class="subsection-title" style="color: var(--primary); margin-top:0;">🪄 ACRONYM</h3>
    <p style="font-size: 0.85rem; color: var(--text-muted);">What each letter stands for.</p>
  </div>
</div>
```

### 4.11 Worked Scenarios / Examples

Each scenario is a `.card` with a label badge, subsection title, and structured answer.

```html
<div class="card">
  <div class="badge" style="background:var(--accent-blue-bg); color:var(--accent-blue); margin-bottom:0.5rem;">
    Scenario N • Short Label
  </div>
  <h3 class="subsection-title" style="margin-top:0;">Scenario Title</h3>
  <p>Question or scenario setup…</p>
  <ul style="padding-left:1.2rem; font-size:0.9rem;">
    <li><strong>Point:</strong> detail</li>
  </ul>
  <p><strong>Answer / Fix:</strong> explanation</p>
</div>
```

### 4.12 Exam Practice (Quiz Cards)

**Toolbar:**

```html
<div class="exam-toolbar">
  <div class="exam-progress" id="exam-progress-tracker">Progress: 0 / 10 Mastered</div>
  <div class="exam-actions">
    <button class="btn-secondary" onclick="toggleAllAnswers(true)">Reveal All</button>
    <button class="btn-secondary" onclick="toggleAllAnswers(false)">Hide All</button>
    <button class="btn-secondary" onclick="resetExamProgress()">Reset Progress</button>
  </div>
</div>
```

**Individual question:**

```html
<div class="quiz-card" id="q1">
  <div class="quiz-header" onclick="toggleAnswer('ans-1')">
    <span class="quiz-qnum">Q1</span>
    <div class="quiz-question"><strong>Question stem bold</strong> rest of question.</div>
  </div>
  <div class="quiz-answer" id="ans-1">
    <strong>Answer:</strong> <em>(see relevant section above)</em>
  </div>
  <div class="quiz-status-toggle">
    <button class="quiz-toggle-btn" onclick="toggleAnswer('ans-1')">👁️ Show / Hide Answer</button>
    <label style="margin-left:auto; cursor:pointer;">
      <input type="checkbox" onchange="toggleMastered('q1', this)"> Mastered
    </label>
  </div>
</div>
```

When a card is mastered: `border-left: 4px solid var(--accent-emerald); opacity: 0.9`

Progress and mastered state are persisted in `localStorage`.

### 4.13 Pipeline / Flow Diagram

```html
<div class="pipeline-container">
  <div class="pipeline-flow">
    <div class="pipe-step">
      <span class="step-num">01</span>
      Step Label
    </div>
    <span class="pipe-arrow">→</span>
    <!-- more steps -->
  </div>
</div>
```

`.pipe-step` hover/active state: border and text switch to primary colour with upward translate.

### 4.14 Interactive Calculator Card

Use for weeks with computable metrics (confusion matrix, probability calculations, etc.).

```html
<div class="calculator-card">
  <div class="calc-header">
    <h3>Calculator Title</h3>
    <div class="calc-presets">
      <button class="preset-btn" onclick="setPreset(...)">Preset Label</button>
    </div>
  </div>
  <div class="calc-grid">
    <!-- Left: input table or form -->
    <!-- Right: .calc-results > multiple .metric-card -->
  </div>
</div>
```

- `.calculator-card`: `border: 2px solid var(--primary)` with primary glow `box-shadow`
- `.metric-card` contains: `.metric-name` (small caps, muted), `.metric-value` (mono, 1.5 rem, primary), `.metric-formula` (tiny mono caption)

### 4.15 Footer

```html
<footer class="site-footer">
  <p><strong>COURSE_CODE Engineering Study Guide</strong> • Semester: Week N — Topic</p>
  <p style="font-size:0.75rem; margin-top:0.4rem;">Generated for self-paced revision and exam preparation.</p>
</footer>
```

---

## 5. Interactive JavaScript Features

All JS is placed inline at the **bottom of `<body>`**. No external libraries.

### 5.1 Theme Toggle

```js
const themeBtn = document.getElementById('theme-toggle');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
let currentTheme = localStorage.getItem('study_theme') || (prefersDark ? 'dark' : 'light');

function applyTheme(theme) {
  if (theme === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark');
    themeBtn.textContent = '☀️';
  } else {
    document.documentElement.removeAttribute('data-theme');
    themeBtn.textContent = '🌙';
  }
  localStorage.setItem('study_theme', theme);
}
applyTheme(currentTheme);

themeBtn.addEventListener('click', () => {
  currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
  applyTheme(currentTheme);
});
```

### 5.2 Mobile Sidebar Toggle

```js
const menuBtn = document.getElementById('menu-btn');
const sidebar = document.getElementById('sidebar');
menuBtn.addEventListener('click', () => sidebar.classList.toggle('open'));

document.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', () => {
    if (window.innerWidth <= 1024) sidebar.classList.remove('open');
  });
});
```

### 5.3 Reading Progress Bar and Active Nav Highlighting

```js
window.addEventListener('scroll', () => {
  const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
  const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
  document.getElementById('progress-bar').style.width = (winScroll / height * 100) + '%';

  const sections = document.querySelectorAll('section.guide-section, section.hero-card');
  let currentSecId = '';
  sections.forEach(sec => {
    if (winScroll >= sec.offsetTop - 120) currentSecId = sec.getAttribute('id');
  });

  document.querySelectorAll('.nav-link').forEach(link => {
    link.classList.remove('active');
    if (link.getAttribute('href') === '#' + currentSecId) link.classList.add('active');
  });
});
```

### 5.4 Glossary Filter

```js
function filterTerms(category, btn) {
  document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
  btn.classList.add('active');
  document.querySelectorAll('.term-card').forEach(card => {
    card.style.display = (category === 'all' || card.getAttribute('data-cat') === category) ? 'flex' : 'none';
  });
}
```

### 5.5 Global Search

```js
document.getElementById('site-search').addEventListener('input', e => {
  const query = e.target.value.toLowerCase().trim();
  document.querySelectorAll('.term-card').forEach(c => {
    c.style.display = (!query || c.textContent.toLowerCase().includes(query)) ? 'flex' : 'none';
  });
  document.querySelectorAll('.quiz-card').forEach(c => {
    c.style.display = (!query || c.textContent.toLowerCase().includes(query)) ? 'block' : 'none';
  });
});
```

### 5.6 Quiz Answer Toggle and Progress Tracker

```js
function toggleAnswer(id) {
  document.getElementById(id).classList.toggle('show');
}
function toggleAllAnswers(show) {
  document.querySelectorAll('.quiz-answer').forEach(ans => {
    show ? ans.classList.add('show') : ans.classList.remove('show');
  });
}

// NOTE: Change the localStorage key to be unique per week, e.g. "course_w2_mastered"
let masteredMap = JSON.parse(localStorage.getItem('course_w1_mastered') || '{}');

function updateProgressUI() {
  const total = document.querySelectorAll('.quiz-card').length;
  const count = Object.values(masteredMap).filter(Boolean).length;
  document.getElementById('exam-progress-tracker').textContent = `Progress: ${count} / ${total} Mastered`;
  for (let i = 1; i <= total; i++) {
    const card = document.getElementById('q' + i);
    const checkbox = card ? card.querySelector('input[type="checkbox"]') : null;
    if (card && checkbox) {
      card.classList.toggle('mastered', !!masteredMap['q' + i]);
      checkbox.checked = !!masteredMap['q' + i];
    }
  }
}
function toggleMastered(qid, checkbox) {
  masteredMap[qid] = checkbox.checked;
  localStorage.setItem('course_w1_mastered', JSON.stringify(masteredMap));
  updateProgressUI();
}
function resetExamProgress() {
  if (confirm('Reset all exam progress checkboxes?')) {
    masteredMap = {};
    localStorage.removeItem('course_w1_mastered');
    updateProgressUI();
  }
}
```

### 5.7 Calculator (if applicable)

Implement `calculateMetrics()` and `setPreset(tp, fp, tn, fn)` tailored to the week's content.
Call `calculateMetrics()` inside the `DOMContentLoaded` event listener.

### 5.8 Initialise on Load

```js
window.addEventListener('DOMContentLoaded', () => {
  calculateMetrics(); // omit if no calculator this week
  updateProgressUI();
});
```

---

## 6. Content Structure

### Standard Section Order

| Index | Section ID | Section Title | Component used |
|---|---|---|---|
| 00 | `#overview` | Overview | `hero-card` (not `guide-section`) |
| 01–0N | `#section-N` | Topic sections (one per major lecture topic) | `guide-section` + appropriate components |
| 09+ | `#key-takeaways` | Key Takeaways | `takeaways-list` — aim for 6–10 items |
| 10 | `#terms-to-know` | Terms to Know (Glossary) | `terms-grid` + `glossary-controls` filter chips |
| 11 | `#mnemonics` | Mnemonics and Quick Recall | `grid-2` of mnemonic `.card` elements |
| 12 | `#worked-examples` | Worked Scenarios and Calculations | `.card` per scenario |
| 13 | `#exam-focus` | Potential Exam Focus and Practice | Quiz cards with progress tracker |

> The sidebar nav list must mirror this order with matching `href` anchors and zero-padded `nav-num` spans.

### Content Lists

Use inline-styled `<ul>` for compact bullet lists inside sections:

```html
<ul style="padding-left:1.2rem; font-size:0.9rem;">
  <li><strong>Term:</strong> explanation here.</li>
</ul>
```

### Inline Code

Use `<code>` for inline code references:

```html
The function <code>parseInt("010")</code> defaults to base 8.
```

---

## 7. Responsive and Print Behaviour

### Responsive — at 1024 px and below (`@media (max-width: 1024px)`)

- Sidebar slides in from left: `position: fixed; left: -100%` → `.open { left: 0 }` via JS
- `.menu-toggle` becomes `display: block`
- `main.main-content` padding reduces to `1.5rem`
- `.grid-2` and `.calc-grid` collapse to single column: `grid-template-columns: 1fr`

### Print (`@media print`)

**Hidden:** `header.site-header`, `aside.sidebar`, `#progress-bar`, `.calculator-card`, `.btn-icon`, `.exam-actions`, `.filter-chip`

**Forced visible:** `.quiz-answer { display: block !important; }` — all answers shown in print

**Cards:** `box-shadow: none !important; border: 1px solid #ccc !important; break-inside: avoid; page-break-inside: avoid`

**Layout:** `.app-container { display: block; max-width: 100%; }`, `main.main-content { padding: 0 !important; max-width: 100% !important; }`

---

## 8. Replication Checklist

When building a new weekly study guide HTML file, go through every item below.

### Head and Metadata
- [ ] `<title>`: `COURSE_CODE – Study Guide – Week N - Topic Title`
- [ ] `<meta name="description">`: brief lecture overview (aim for ~160 characters)
- [ ] Google Fonts import: Plus Jakarta Sans (300,400,500,600,700,800 + ital,400) + JetBrains Mono (400,500,600,700)
- [ ] KaTeX 0.16.8: CSS link + main JS (defer) + auto-render JS (defer, with onload handler and delimiter config)

### CSS
- [ ] Full `:root` token block (light theme)
- [ ] Full `[data-theme="dark"]` token block
- [ ] All global resets and base styles
- [ ] All component classes (header, sidebar, hero, guide-section, cards, callouts, formula-block, tables, badges, takeaways, glossary, mnemonics, pipeline, calculator, quiz, footer)
- [ ] Responsive media query block (max-width: 1024px)
- [ ] Print media query block
- [ ] `@keyframes fadeIn` animation

### HTML Structure
- [ ] `<div id="progress-bar"></div>` as first child of `<body>`
- [ ] `<header class="site-header">` with course badge, title, search box, theme toggle, print button
- [ ] `<aside class="sidebar" id="sidebar">` with correct nav links (zero-padded nav-num)
- [ ] `<main class="main-content">` wrapping all sections
- [ ] `<footer class="site-footer">` at the bottom

### Content
- [ ] `#overview` hero card: tagline, `<h1>`, subtitle, overview paragraph
- [ ] All topic sections (`#section-1` through `#section-N`) with section-header + content
- [ ] `#key-takeaways`: numbered takeaway items (6–10)
- [ ] `#terms-to-know`: filter chips (update counts) + term cards with correct `data-cat` values
- [ ] `#mnemonics`: mnemonic cards in grid-2
- [ ] `#worked-examples`: one `.card` per scenario
- [ ] `#exam-focus`: toolbar + 8–12 quiz cards with matching IDs

### JavaScript
- [ ] Theme toggle (reads/writes `localStorage.getItem('study_theme')`)
- [ ] Mobile sidebar toggle
- [ ] Scroll handler (progress bar + active nav link)
- [ ] `filterTerms()` for glossary
- [ ] Search handler (filters term cards and quiz cards)
- [ ] `toggleAnswer()`, `toggleAllAnswers()`, `toggleMastered()`, `resetExamProgress()`, `updateProgressUI()`
- [ ] **Update** `localStorage` key string to be unique for this week (e.g. `info3616_w2_mastered`)
- [ ] `DOMContentLoaded` initialiser calling `updateProgressUI()` (and `calculateMetrics()` if a calculator is present)
- [ ] Calculator functions (`calculateMetrics`, `setPreset`) — only if the week has quantitative content

### Testing
- [ ] Light/dark theme toggle works and persists on reload
- [ ] Sidebar navigation: active link highlights on scroll, links scroll to correct section
- [ ] Search filters term cards and quiz cards correctly; clearing search resets all
- [ ] Glossary filter chips show/hide correct term cards
- [ ] Quiz: show/hide individual answers, Reveal All, Hide All, Mastered checkbox, progress counter, Reset Progress
- [ ] Print layout: sidebar/header hidden, all quiz answers visible, no broken layout
- [ ] Responsive (below 1024 px): menu button visible, sidebar slides in/out, grid collapses
- [ ] Math formulas render correctly if KaTeX is used

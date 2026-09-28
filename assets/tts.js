/* ---------------------------------------------------------------------------
 * tts.js — "Read aloud" for the Calm Canvas study guides.
 *
 * Uses the browser's built-in Web Speech API (window.speechSynthesis): no
 * dependencies, no build step, no network calls.
 *
 * Wiring: every guide includes this file once, just before </body>:
 *     <script src="../../../assets/tts.js"></script>
 * The control is injected into the existing .topbar-tools, so no guide markup
 * or CSS needs to change. On pages without a topbar (e.g. index.html) it does
 * nothing.
 *
 * Behaviour:
 *   - Reads the hero and each .guide-section in order, skipping chrome,
 *     navigation, quiz answers that are still hidden, and formula/code chips.
 *   - Highlights and scrolls to the section currently being spoken.
 *   - Play/pause, stop, speed and voice controls; speed and voice persist in
 *     localStorage under `tts-rate` / `tts-voice`.
 *   - Degrades silently when speechSynthesis is unavailable.
 * ------------------------------------------------------------------------- */
(function () {
  "use strict";

  if (typeof window === "undefined") return;
  if (!("speechSynthesis" in window) || typeof window.SpeechSynthesisUtterance === "undefined") return;
  if (window.__calmCanvasTtsLoaded) return;
  window.__calmCanvasTtsLoaded = true;

  var synth = window.speechSynthesis;
  var Utter = window.SpeechSynthesisUtterance;

  /* Selection of text to read: everything here is skipped. */
  var SKIP = [
    ".sidebar", ".topbar", "nav", "footer", "script", "style", ".scrim",
    ".to-top", ".progress-track", ".suggest", ".search", ".tts", ".tts-panel",
    ".sec-num", ".flow-arrow", ".math", "code", "[aria-hidden='true']",
    ".quiz-reveal", ".mastered", ".quiz-toolbar", ".glossary-tools", ".chip",
    ".dot", ".search-icon", ".empty-note"
  ].join(",");

  var BLOCK = /^(ADDRESS|ARTICLE|ASIDE|BLOCKQUOTE|DD|DETAILS|DIALOG|DIV|DL|DT|FIELDSET|FIGCAPTION|FIGURE|FOOTER|FORM|H1|H2|H3|H4|H5|H6|HEADER|HGROUP|HR|LI|MAIN|NAV|OL|P|PRE|SECTION|TABLE|TBODY|TD|TFOOT|TH|THEAD|TR|UL|BR)$/;

  var reduceMotion = !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);

  /* ------------------------------------------------------------------ */
  /* Small helpers                                                       */
  /* ------------------------------------------------------------------ */

  function store(key, value) {
    try { localStorage.setItem(key, value); } catch (e) {}
  }
  function recall(key) {
    try { return localStorage.getItem(key); } catch (e) { return null; }
  }

  /* Per-text-node exclusion check that works in Firefox and Chromium. */
  function isSkipped(el) {
    if (el.matches && el.matches(SKIP)) return true;
    var cs = window.getComputedStyle(el);
    return cs.display === "none" || cs.visibility === "hidden";
  }

  /* Walk the live DOM and collect readable prose, inserting a newline at
   * block boundaries. Hidden elements (e.g. a closed .quiz-answer) are
   * naturally excluded by the computed-style check. */
  function extractText(root) {
    var out = "";
    (function walk(node) {
      for (var n = node.firstChild; n; n = n.nextSibling) {
        if (n.nodeType === 3) {
          var t = n.nodeValue.replace(/\s+/g, " ");
          if (t.replace(/\s/g, "")) out += t;
        } else if (n.nodeType === 1) {
          if (isSkipped(n)) continue;
          var block = BLOCK.test(n.tagName);
          if (block) out += "\n";
          walk(n);
          if (block) out += "\n";
        }
      }
    })(root);
    return out
      .replace(/[ \t]+/g, " ")
      .replace(/ *\n */g, "\n")
      .replace(/\n{2,}/g, "\n")
      /* Turn decorative glyphs into comma pauses instead of letting the
       * synthesiser read them as "right arrow" / "middle dot". */
      .replace(/\s*[\u2192\u2190\u2194]\s*/g, ", ")
      .replace(/\s*\u00b7\s*/g, ", ")
      .replace(/\s+,/g, ",")
      .replace(/,\s*,/g, ", ")
      .trim();
  }

  /* Split long prose into utterance-sized chunks at sentence boundaries.
   * Chunks are built per section (so highlighting stays per-section) and
   * capped in length to avoid the Chromium quirk where very long utterances
   * stall. Block-level line breaks are flattened; punctuation carries the
   * pauses for the synthesiser. */
  function chunkText(text, maxLen) {
    maxLen = maxLen || 240;
    var parts = text.replace(/\s*\n+\s*/g, " ").match(/[^.!?]+[.!?]*/g) || [];
    var chunks = [];
    var cur = "";
    parts.forEach(function (p) {
      p = p.replace(/\s+/g, " ").trim();
      if (!p) return;
      if (cur && (cur.length + 1 + p.length) > maxLen) {
        chunks.push(cur);
        cur = p;
      } else {
        cur = cur ? cur + " " + p : p;
      }
    });
    if (cur) chunks.push(cur);
    return chunks;
  }

  /* ------------------------------------------------------------------ */
  /* Build the control                                                   */
  /* ------------------------------------------------------------------ */

  function init() {
    var tools = document.querySelector(".topbar-tools");
    if (!tools) return; /* no topbar on this page */

    var wrap = document.createElement("div");
    wrap.className = "tts";
    wrap.innerHTML =
      '<button class="icon-btn tts-toggle" type="button" aria-label="Read aloud" aria-haspopup="true" aria-expanded="false" title="Read aloud">' +
        '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" focusable="false">' +
          '<path fill="currentColor" d="M4 9v6h4l5 4V5L8 9H4zm12.5 3a3.5 3.5 0 0 0-2-3.16v6.32A3.5 3.5 0 0 0 16.5 12z"/>' +
        '</svg>' +
      '</button>' +
      '<div class="tts-panel" role="group" aria-label="Read aloud controls" hidden>' +
        '<p class="tts-title">Read aloud</p>' +
        '<div class="tts-row">' +
          '<button class="btn btn-primary tts-play" type="button">Read page</button>' +
          '<button class="btn tts-stop" type="button">Stop</button>' +
        '</div>' +
        '<label class="tts-field">Speed' +
          '<select class="tts-rate" id="ttsRate" name="tts-rate">' +
            '<option value="0.75">0.75\u00d7</option>' +
            '<option value="1" selected>1\u00d7</option>' +
            '<option value="1.25">1.25\u00d7</option>' +
            '<option value="1.5">1.5\u00d7</option>' +
          '</select>' +
        '</label>' +
        '<label class="tts-field">Voice' +
          '<select class="tts-voice" id="ttsVoice" name="tts-voice"></select>' +
        '</label>' +
        '<p class="tts-hint">Starts at the top and highlights each section.</p>' +
      '</div>';

    var themeBtn = document.getElementById("themeToggle");
    tools.insertBefore(wrap, themeBtn || null);

    injectStyles();

    var toggleBtn = wrap.querySelector(".tts-toggle");
    var panel = wrap.querySelector(".tts-panel");
    var playBtn = wrap.querySelector(".tts-play");
    var stopBtn = wrap.querySelector(".tts-stop");
    var rateSel = wrap.querySelector(".tts-rate");
    var voiceSel = wrap.querySelector(".tts-voice");

    /* ------------------------------------------------------------------ */
    /* Voices                                                              */
    /* ------------------------------------------------------------------ */

    var voices = [];

    function voiceDefaultIndex() {
      var lang = (document.documentElement.getAttribute("lang") || "en").slice(0, 2).toLowerCase();
      for (var i = 0; i < voices.length; i++) {
        if ((voices[i].lang || "").toLowerCase().indexOf(lang) === 0) return i;
      }
      return -1;
    }

    function renderVoices() {
      if (!voiceSel) return;
      voices = synth.getVoices() || [];
      var saved = recall("tts-voice");
      voiceSel.innerHTML = "";

      if (!voices.length) {
        var opt = document.createElement("option");
        opt.value = "";
        opt.textContent = "Default system voice";
        voiceSel.appendChild(opt);
        return;
      }

      /* English voices first, then alphabetical — easier to scan. */
      var ordered = voices.slice().sort(function (a, b) {
        var ae = (a.lang || "").toLowerCase().indexOf("en") === 0 ? 0 : 1;
        var be = (b.lang || "").toLowerCase().indexOf("en") === 0 ? 0 : 1;
        if (ae !== be) return ae - be;
        return (a.name || "").localeCompare(b.name || "");
      });

      ordered.forEach(function (v) {
        var o = document.createElement("option");
        o.value = v.name;
        o.textContent = (v.default ? "\u2605 " : "") + v.name + " \u2014 " + v.lang;
        voiceSel.appendChild(o);
      });

      if (saved) {
        for (var i = 0; i < voiceSel.options.length; i++) {
          if (voiceSel.options[i].value === saved) { voiceSel.selectedIndex = i; return; }
        }
      }
      var di = voiceDefaultIndex();
      if (di >= 0) {
        for (var j = 0; j < voiceSel.options.length; j++) {
          if (voiceSel.options[j].value === voices[di].name) { voiceSel.selectedIndex = j; break; }
        }
      }
    }

    renderVoices();
    /* Chromium populates voices asynchronously; Firefox returns them at once
     * and does not fire the event reliably — so do both. */
    if ("onvoiceschanged" in synth) synth.onvoiceschanged = renderVoices;
    var voiceTries = 0;
    var voicePoll = window.setInterval(function () {
      if (voices.length || ++voiceTries > 10) { window.clearInterval(voicePoll); return; }
      renderVoices();
    }, 300);

    /* Restore saved speed. */
    var savedRate = recall("tts-rate");
    if (savedRate) {
      for (var r = 0; r < rateSel.options.length; r++) {
        if (rateSel.options[r].value === savedRate) { rateSel.value = savedRate; break; }
      }
    }

    rateSel.addEventListener("change", function () { store("tts-rate", rateSel.value); });
    voiceSel.addEventListener("change", function () { store("tts-voice", voiceSel.value); });

    /* ------------------------------------------------------------------ */
    /* Reading engine                                                      */
    /* ------------------------------------------------------------------ */

    var queue = [];
    var reading = false;
    var paused = false;
    var session = 0; /* bumped on every start/stop so a deferred start can bail */

    function activeSections() {
      var units = [];
      var hero = document.querySelector(".hero");
      if (hero) units.push(hero);
      Array.prototype.forEach.call(document.querySelectorAll(".guide-section"), function (s) {
        units.push(s);
      });
      return units;
    }

    function buildQueue() {
      queue = [];
      activeSections().forEach(function (el) {
        var text = extractText(el);
        if (!text) return;
        chunkText(text).forEach(function (t) { queue.push({ el: el, text: t }); });
      });
    }

    function markActive(el) {
      Array.prototype.forEach.call(document.querySelectorAll("[data-tts-active]"), function (x) {
        x.removeAttribute("data-tts-active");
      });
      if (!el) return;
      el.setAttribute("data-tts-active", "1");
      var top = el.getBoundingClientRect().top + window.pageYOffset - 80;
      try {
        window.scrollTo({ top: top, behavior: reduceMotion ? "auto" : "smooth" });
      } catch (e) {
        window.scrollTo(0, top);
      }
    }

    function currentVoice() {
      var name = voiceSel ? voiceSel.value : "";
      if (!name) return null;
      for (var i = 0; i < voices.length; i++) {
        if (voices[i].name === name) return voices[i];
      }
      return null;
    }

    function speakIndex(i) {
      if (!reading) return;
      if (i >= queue.length) { finish(); return; }
      var item = queue[i];
      markActive(item.el);
      var u = new Utter(item.text);
      var v = currentVoice();
      if (v) u.voice = v;
      u.rate = Math.max(0.1, Math.min(10, parseFloat(rateSel.value) || 1));
      u.onend = function () { if (reading && !paused) speakIndex(i + 1); };
      u.onerror = function () { if (reading && !paused) speakIndex(i + 1); };
      synth.speak(u);
    }

    function start() {
      var my = ++session;
      reading = false; /* ignore callbacks from anything already queued */
      paused = false;
      synth.cancel();
      window.setTimeout(function () {
        if (my !== session) return; /* a stop/newer start superseded us */
        buildQueue();
        if (!queue.length) { updateUI(); return; }
        reading = true;
        updateUI();
        speakIndex(0);
      }, 80);
    }

    function stop() {
      session++;
      reading = false;
      paused = false;
      synth.cancel();
      markActive(null);
      updateUI();
    }

    function finish() {
      reading = false;
      paused = false;
      markActive(null);
      updateUI();
    }

    function togglePlay() {
      if (!reading) { start(); return; }
      if (paused) {
        paused = false;
        synth.resume();
      } else {
        paused = true;
        synth.pause();
      }
      updateUI();
    }

    function updateUI() {
      wrap.classList.toggle("speaking", reading);
      if (playBtn) playBtn.textContent = !reading ? "Read page" : (paused ? "Resume" : "Pause");
    }

    playBtn.addEventListener("click", togglePlay);
    stopBtn.addEventListener("click", function () { stop(); });

    /* ------------------------------------------------------------------ */
    /* Panel open / close                                                  */
    /* ------------------------------------------------------------------ */

    function setPanel(open) {
      panel.hidden = !open;
      toggleBtn.setAttribute("aria-expanded", open ? "true" : "false");
    }
    toggleBtn.addEventListener("click", function () { setPanel(panel.hidden); });
    document.addEventListener("click", function (e) {
      if (!wrap.contains(e.target)) setPanel(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !panel.hidden) { setPanel(false); }
    });

    /* Stop speech if the page is unloaded (covers bfcache navigation). */
    window.addEventListener("pagehide", function () { synth.cancel(); });
  }

  /* ------------------------------------------------------------------ */
  /* Injected styling — reuses the Calm Canvas design tokens.            */
  /* ------------------------------------------------------------------ */

  function injectStyles() {
    if (document.getElementById("ttsStyles")) return;
    var style = document.createElement("style");
    style.id = "ttsStyles";
    style.textContent =
      ".tts{position:relative;display:flex;align-items:center;}" +
      ".tts-toggle svg{display:block;}" +
      ".tts-panel{position:absolute;top:calc(100% + .5rem);right:0;width:min(86vw,300px);z-index:120;" +
        "background:var(--surface);border:1px solid var(--line);border-radius:var(--radius-sm);" +
        "box-shadow:var(--shadow-lg);padding:.85rem;display:flex;flex-direction:column;gap:.6rem;}" +
      ".tts-panel[hidden]{display:none;}" +
      ".tts-title{margin:0;font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--ink-faint);}" +
      ".tts-row{display:flex;gap:.5rem;}" +
      ".tts-row .btn{flex:1;}" +
      ".tts-field{display:flex;flex-direction:column;gap:.25rem;font-size:.72rem;font-weight:700;" +
        "text-transform:uppercase;letter-spacing:.06em;color:var(--ink-faint);}" +
      ".tts-field select{font-family:inherit;font-size:.88rem;font-weight:400;text-transform:none;letter-spacing:0;" +
        "color:var(--ink);background:var(--surface-2);border:1px solid var(--line);border-radius:8px;padding:.4rem .5rem;}" +
      ".tts-hint{margin:0;font-size:.78rem;color:var(--ink-faint);line-height:1.45;}" +
      ".tts.speaking .tts-toggle{border-color:var(--primary);color:var(--primary-deep);box-shadow:0 0 0 4px var(--primary-soft);}" +
      "[data-tts-active]{outline:2px solid var(--primary);outline-offset:6px;border-radius:var(--radius-sm);" +
        "transition:outline-color .3s var(--ease);}";
    document.head.appendChild(style);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

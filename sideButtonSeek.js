/*
 * Side Button Seek - a Stash UI plugin (v2)
 * ------------------------------------------------------------------
 * Mouse side buttons are MouseEvent.button 3 (X1 / browser back) and
 * 4 (X2 / browser forward). Stash does not bind them, and Chromium maps
 * them to history back/forward at the BROWSER level: calling
 * preventDefault() on mousedown / auxclick does NOT stop the navigation.
 *
 * v2 fixes this with the Navigation API (Chrome/Edge 102+):
 *
 *   - A traverse to a history entry belonging to another document has
 *     `cancelable === false`, so a web page cannot cancel it.
 *   - A traverse to a same-document entry (one created with pushState)
 *     has `cancelable === true` and CAN be cancelled.
 *   - On the first side-button press we therefore push one same-URL
 *     "guard" entry when the neighbouring history entry is cross-document.
 *     This makes the browser's back/forward traversal same-document, and
 *     our `navigate` listener cancels it while we seek the video instead.
 *   - The guard is created lazily (only on a real side-button press) and
 *     only once, so pages where the side buttons are remapped to keyboard
 *     keys are left completely untouched.
 *
 * Fallback: if a mouse driver reports the side buttons as keyboard keys
 * or as an OS app command, no button 3/4 DOM event reaches the page at
 * all. Remap the buttons to Left/Right arrow keys in the mouse driver
 * (MetapandaMouse, X-Mouse Button Control, Logitech G Hub, Razer
 * Synapse, AutoHotkey) and Stash's built-in shortcuts do the seeking.
 *
 * Install: put this file next to sideButtonSeek.yml in the Stash plugins
 * directory, then Settings > Plugins > Reload plugins, then refresh (F5).
 *
 * Console helpers:
 *   SideButtonSeek.settings          - active configuration
 *   SideButtonSeek.reload()          - re-read plugin settings
 *   SideButtonSeek.seek(10)          - seek by an arbitrary amount
 *   SideButtonSeek.simulate(3|4)     - trigger a button without a mouse
 *   SideButtonSeek.player            - the current VideoJS player
 *   SideButtonSeek.guard             - Navigation API guard diagnostics
 */
(function () {
  "use strict";

  var ID = "sideButtonSeek";
  var VERSION = "2.1.1";
  var BACK = 3;    // X1 / browser back
  var FORWARD = 4; // X2 / browser forward
  var NAV_WINDOW_MS = 3000; // hard upper bound for a pending guard
  var DISARM_MS = 250;      // release the guard shortly after the last phase
  var STEP_PRESETS = [5, 10, 15, 30, 60, 120];
  var UI_POLL_MS = 1000;    // re-attach the step button after SPA navigation

  var DEFAULTS = Object.freeze({
    seekSeconds: 10,
    swapButtons: false,
    onlyInPlayer: true,
    showOsd: true,
    showStepButton: true,
    preventNavigation: true,
    debug: false
  });

  var EVENTS = ["pointerdown", "mousedown", "mouseup", "auxclick"];

  var cfg = Object.assign({}, DEFAULTS);
  var listeners = [];
  var lastDownAt = 0;
  var lastDownButton = -1;
  var lastSideAt = 0;
  var guardArmed = false; // one physical press may cancel one traversal
  var disarmTimer = null;
  var guardPushes = 0;
  var blockedTraversals = 0;
  var osdEl = null;
  var osdTimer = null;
  var stepBtn = null;
  var stepPanel = null;
  var uiPollTimer = null;

  var navSupported = typeof window.navigation !== "undefined" &&
    typeof window.navigation.addEventListener === "function" &&
    typeof window.navigation.entries === "function";

  // Allow a clean re-injection if Stash ever loads this file twice.
  if (window.SideButtonSeek && typeof window.SideButtonSeek._disable === "function") {
    window.SideButtonSeek._disable();
  }

  function log() {
    if (!cfg.debug) return;
    var args = Array.prototype.slice.call(arguments);
    console.log.apply(console, ["[" + ID + "]"].concat(args));
  }

  /* ---------------------------------------------------------------- *
   * Plugin settings are exposed by Stash as a JSON scalar on the
   * configuration.plugins field: { <pluginId>: { key: value } }.
   * ---------------------------------------------------------------- */
  function loadSettings() {
    if (typeof fetch !== "function") return Promise.resolve(cfg);
    return fetch("/graphql", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "same-origin",
      body: JSON.stringify({ query: "{ configuration { plugins } }" })
    })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        var all = data && data.data && data.data.configuration &&
          data.data.configuration.plugins;
        var saved = all && all[ID];
        var next = Object.assign({}, DEFAULTS);
        if (saved && typeof saved === "object") {
          Object.keys(DEFAULTS).forEach(function (key) {
            var value = saved[key];
            if (value === undefined || value === null || value === "") return;
            if (typeof DEFAULTS[key] === "boolean") {
              next[key] = value === true || value === "true" || value === 1;
            } else if (typeof DEFAULTS[key] === "number") {
              var n = Number(value);
              if (!isNaN(n)) next[key] = n;
            } else {
              next[key] = value;
            }
          });
        }
        cfg = next;
        cfg.seekSeconds = Math.min(3600, Math.max(0.1, cfg.seekSeconds));
        log("settings", cfg);
        return cfg;
      })
      .catch(function (err) {
        log("settings unavailable, using defaults", err);
        return cfg;
      });
  }

  /* ---------------------------------------------------------------- *
   * Locate the VideoJS player. Try the official PluginApi first, then
   * videojs.getPlayers(), then the DOM element's .player property, and
   * finally the bare <video> element as a last resort.
   * ---------------------------------------------------------------- */
  function playerFromPluginApi() {
    try {
      var api = window.PluginApi || window.pluginApi;
      var utils = api && api.utils;
      var iu = utils && utils.InteractiveUtils;
      var p = iu && typeof iu.getPlayer === "function" ? iu.getPlayer() : null;
      if (p && typeof p.currentTime === "function") return p;
    } catch (_) { /* ignore */ }
    return null;
  }

  function playerFromVideoJS() {
    try {
      if (window.videojs && typeof window.videojs.getPlayers === "function") {
        var players = Object.values(window.videojs.getPlayers());
        if (players.length) return players[players.length - 1];
      }
    } catch (_) { /* ignore */ }
    var el = document.querySelector(".video-js");
    if (el && el.player && typeof el.player.currentTime === "function") return el.player;
    return null;
  }

  function getPlayer() {
    return playerFromPluginApi() || playerFromVideoJS();
  }

  function getVideoElement() {
    return document.querySelector(".video-js video, video.vjs-tech, video");
  }

  function clampValue(t, duration) {
    var d = Number(duration);
    var max = isFinite(d) && d > 0 ? d : Infinity;
    return Math.max(0, Math.min(max, t));
  }

  function seek(delta) {
    var p = getPlayer();
    if (p && typeof p.currentTime === "function") {
      var from = p.currentTime();
      var dur = Infinity;
      try { dur = p.duration(); } catch (_) { /* ignore */ }
      var to = clampValue(from + delta, dur);
      p.currentTime(to);
      return { ok: true, from: from, requested: to, now: p.currentTime(), source: "videojs" };
    }
    var v = getVideoElement();
    if (v) {
      var vFrom = v.currentTime;
      var vTo = clampValue(vFrom + delta, v.duration);
      v.currentTime = vTo;
      return { ok: true, from: vFrom, requested: vTo, now: v.currentTime, source: "element" };
    }
    return { ok: false, reason: "no player or video element on this page" };
  }

  /* ---------------------------------------------------------------- *
   * Small on-screen confirmation, appended inside the player so it is
   * also visible in fullscreen mode.
   * ---------------------------------------------------------------- */
  function showOsd(delta) {
    if (!cfg.showOsd) return;
    var host = document.querySelector(".video-js") || document.body;
    if (!osdEl || !osdEl.isConnected || osdEl.parentNode !== host) {
      if (osdEl) osdEl.remove();
      osdEl = document.createElement("div");
      osdEl.setAttribute("data-plugin", ID);
      osdEl.style.cssText = [
        "position:absolute", "top:14%", "left:50%", "transform:translateX(-50%)",
        "z-index:2147483000", "padding:8px 16px", "border-radius:8px",
        "background:rgba(0,0,0,.72)", "color:#fff", "pointer-events:none",
        "font:600 22px/1.2 system-ui,sans-serif", "text-shadow:0 1px 3px #000",
        "opacity:0", "transition:opacity .15s ease"
      ].join(";") + ";";
      host.appendChild(osdEl);
    }
    var label = (delta < 0 ? "\u00ab " : "") +
      (delta > 0 ? "+" : "\u2212") + Math.abs(delta) + "s" +
      (delta > 0 ? " \u00bb" : "");
    osdEl.textContent = label;
    osdEl.style.opacity = "1";
    clearTimeout(osdTimer);
    osdTimer = setTimeout(function () {
      if (osdEl) osdEl.style.opacity = "0";
    }, 800);
  }

  /* ---------------------------------------------------------------- *
   * In-player "seek step" button (v2.1.0).
   *
   * Appended as an absolutely positioned child of .video-js: NOT into
   * VideoJS' control bar and NOT into any React-owned node. VideoJS does
   * not remove it, React never reconciles it, and it follows the player
   * into fullscreen. Clicking it opens a panel that writes the step back
   * to Stash plugin settings, so the value survives reloads / browsers.
   * ---------------------------------------------------------------- */
  function stepLabel(value) {
    return "\u00b1" + value + "s";
  }

  function removeStepUI() {
    if (stepPanel) { stepPanel.remove(); stepPanel = null; }
    if (stepBtn) { stepBtn.remove(); stepBtn = null; }
  }

  function setStepStatus(text, isError) {
    var el = stepPanel && stepPanel.querySelector("[data-sbs-status]");
    if (!el) return;
    el.textContent = text || "";
    el.style.color = isError ? "#ff9a9a" : "#9fe6a0";
  }

  function saveStep(value) {
    var n = Number(value);
    if (!isFinite(n) || n <= 0) {
      setStepStatus("Enter a number greater than 0", true);
      return Promise.resolve(null);
    }
    n = Math.min(3600, Math.max(0.1, n));
    // configurePlugin replaces the WHOLE settings map, so send every key.
    var payload = {};
    Object.keys(DEFAULTS).forEach(function (k) { payload[k] = cfg[k]; });
    payload.seekSeconds = n;
    setStepStatus("Saving...", false);
    return fetch("/graphql", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "same-origin",
      body: JSON.stringify({
        query: "mutation($id: ID!, $in: Map!) { configurePlugin(plugin_id:$id, input:$in) }",
        variables: { id: ID, in: payload }
      })
    })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (d.errors && d.errors.length) {
          throw new Error(d.errors[0].message || "GraphQL error");
        }
        cfg.seekSeconds = n;
        if (stepBtn) stepBtn.textContent = stepLabel(n);
        setStepStatus("Saved: " + stepLabel(n) + " per press", false);
        log("step saved", n);
        return n;
      })
      .catch(function (err) {
        var msg = err && err.message ? err.message : String(err);
        setStepStatus("Save failed: " + msg, true);
        log("step save failed", err);
        return null;
      });
  }

  function buildStepPanel(inControlBar) {
    var panel = document.createElement("div");
    panel.setAttribute("data-plugin", ID + "-panel");
    panel.style.cssText = [
      "position:absolute", inControlBar ? "bottom:52px" : "top:44px",
      "right:10px", "z-index:2147483001",
      "width:226px", "padding:12px", "border-radius:10px",
      "background:rgba(18,20,24,.95)", "color:#fff",
      "box-shadow:0 6px 26px rgba(0,0,0,.55)", "border:1px solid rgba(255,255,255,.14)",
      "font:13px/1.5 system-ui,sans-serif", "cursor:default"
    ].join(";") + ";";
    panel.innerHTML =
      '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">' +
      '<strong>Seek step / 跳转步长</strong>' +
      '<button type="button" data-sbs-close style="background:none;border:0;color:#fff;font-size:18px;line-height:1;cursor:pointer;padding:0 2px">\u00d7</button>' +
      '</div>' +
      '<div style="opacity:.72;margin-bottom:9px">Seconds per side-button press</div>' +
      '<div data-sbs-presets style="display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-bottom:10px"></div>' +
      '<div style="display:flex;gap:6px">' +
      '<input type="number" min="0.1" max="3600" step="1" data-sbs-input ' +
      'style="flex:1;min-width:0;background:#2b2f36;color:#fff;border:1px solid #555;border-radius:5px;padding:5px 7px;font:13px system-ui">' +
      '<button type="button" data-sbs-save style="background:#3b7ddd;color:#fff;border:0;border-radius:5px;padding:5px 11px;cursor:pointer;font:600 13px system-ui">Save</button>' +
      '</div>' +
      '<div data-sbs-status style="min-height:18px;margin-top:8px;font-size:12px"></div>' +
      '<div style="opacity:.55;font-size:11px">Saved to Stash plugin settings</div>';

    // Keep panel interactions away from the video (play/pause) and from
    // the global side-button handlers.
    ["click", "mousedown", "mouseup", "pointerdown", "auxclick"].forEach(function (type) {
      panel.addEventListener(type, function (e) { e.stopPropagation(); });
    });

    var presets = panel.querySelector("[data-sbs-presets]");
    STEP_PRESETS.forEach(function (v) {
      var b = document.createElement("button");
      b.type = "button";
      b.textContent = v + "s";
      b.style.cssText = [
        "background:#2b2f36", "color:#fff", "border:1px solid #555",
        "border-radius:5px", "padding:5px 0", "cursor:pointer", "font:13px system-ui"
      ].join(";") + ";";
      b.addEventListener("click", function () { saveStep(v); });
      presets.appendChild(b);
    });

    panel.querySelector("[data-sbs-close]").addEventListener("click", function () {
      removeStepUI();
      ensureStepUI();
    });
    panel.querySelector("[data-sbs-save]").addEventListener("click", function () {
      var input = panel.querySelector("[data-sbs-input]");
      saveStep(input.value);
    });
    panel.querySelector("[data-sbs-input]").addEventListener("keydown", function (e) {
      if (e.key === "Enter") saveStep(e.target.value);
    });
    return panel;
  }

  function toggleStepPanel(host, inControlBar) {
    if (stepPanel && stepPanel.isConnected) {
      stepPanel.remove();
      stepPanel = null;
      return;
    }
    stepPanel = buildStepPanel(inControlBar);
    host.appendChild(stepPanel);
    var input = stepPanel.querySelector("[data-sbs-input]");
    input.value = cfg.seekSeconds;
    input.focus();
    input.select();
  }

  function ensureStepUI() {
    if (!cfg.showStepButton) { removeStepUI(); return; }
    var host = document.querySelector(".video-js");
    if (!host) { removeStepUI(); return; }
    // Prefer the control bar: that is where users look for player buttons.
    // Fall back to a corner overlay if VideoJS has no control bar yet.
    var bar = host.querySelector(".vjs-control-bar");
    var inBar = !!bar;
    var parent = inBar ? bar : host;
    if (stepBtn && stepBtn.isConnected && stepBtn.parentNode === parent) {
      // Keep the label in sync when settings finish loading / change.
      stepBtn.textContent = stepLabel(cfg.seekSeconds);
      return;
    }
    removeStepUI();

    stepBtn = document.createElement("button");
    stepBtn.type = "button";
    stepBtn.setAttribute("data-plugin", ID + "-step");
    stepBtn.textContent = stepLabel(cfg.seekSeconds);
    stepBtn.title = "设置侧键跳转步长 / Set side-button seek step";
    if (inBar) {
      // A normal flex child of the VideoJS control bar, at the far right.
      stepBtn.style.cssText = [
        "position:relative", "flex:none", "order:99", "align-self:center",
        "height:26px", "margin:0 6px", "padding:0 9px",
        "background:rgba(0,0,0,.35)", "border:1px solid rgba(255,255,255,.55)",
        "border-radius:4px", "color:#fff",
        "font:600 13px/1.2 system-ui,sans-serif", "cursor:pointer",
        "opacity:.95", "pointer-events:auto"
      ].join(";") + ";";
    } else {
      stepBtn.style.cssText = [
        "position:absolute", "top:10px", "right:10px", "z-index:2147483000",
        "padding:5px 10px", "border:1px solid rgba(255,255,255,.28)", "border-radius:6px",
        "background:rgba(0,0,0,.55)", "color:#fff",
        "font:600 13px/1.2 system-ui,sans-serif", "cursor:pointer", "opacity:.72",
        "transition:opacity .15s ease", "pointer-events:auto"
      ].join(";") + ";";
    }
    stepBtn.addEventListener("mouseenter", function () { stepBtn.style.opacity = "1"; });
    stepBtn.addEventListener("mouseleave", function () { stepBtn.style.opacity = inBar ? ".95" : ".72"; });
    ["click", "mousedown", "mouseup", "pointerdown", "auxclick"].forEach(function (type) {
      stepBtn.addEventListener(type, function (e) { e.stopPropagation(); });
    });
    stepBtn.addEventListener("click", function (e) {
      e.preventDefault();
      toggleStepPanel(host, inBar);
    });
    parent.appendChild(stepBtn);
  }

  function inPlayer(target) {
    if (!cfg.onlyInPlayer) return true;
    if (!(target instanceof Element)) return false;
    return !!target.closest(
      ".video-js, .vjs-tech, video, .vjs-control-bar, .vjs-poster, .scene-player"
    );
  }

  function doSeek(button) {
    var isBack = button === BACK;
    if (cfg.swapButtons) isBack = !isBack;
    var delta = isBack ? -cfg.seekSeconds : cfg.seekSeconds;
    var result = seek(delta);
    log("seek", { button: button, delta: delta, result: result });
    if (result.ok) showOsd(delta);
    return result;
  }

  /* ---------------------------------------------------------------- *
   * Navigation API guard.
   *
   * history traversal to a cross-document entry is NOT cancelable, while
   * traversal to a same-document entry IS. Pushing a same-URL entry with
   * pushState makes the browser's pending back/forward traverse land on
   * an entry that shares our Document, so we can cancel it. pushState
   * also truncates the forward stack, which neutralises X2 as well.
   * ---------------------------------------------------------------- */
  function neighbourInfo(button) {
    if (!navSupported) return null;
    try {
      var entries = window.navigation.entries();
      var current = entries.indexOf(window.navigation.currentEntry);
      var target = button === BACK ? entries[current - 1] : entries[current + 1];
      return {
        index: current,
        count: entries.length,
        hasTarget: !!target,
        sameDocument: target ? target.sameDocument : null
      };
    } catch (_) {
      return null;
    }
  }

  function ensureGuard(button) {
    if (!cfg.preventNavigation || !navSupported) return;
    var info = neighbourInfo(button);
    if (!info) return;
    // Be conservative: anything that is not explicitly same-document is
    // treated as a risky cross-document traversal.
    var risky = info.hasTarget && info.sameDocument !== true;
    if (!risky) return;
    try {
      window.history.pushState({ sideButtonSeekGuard: true }, "", window.location.href);
      guardPushes++;
      log("guard entry pushed", { button: button, before: info });
    } catch (err) {
      log("guard push failed", err);
    }
  }

  function onNavigate(e) {
    if (!cfg.preventNavigation) return;
    if (e.navigationType !== "traverse") return;
    var recentSide = Date.now() - lastSideAt < NAV_WINDOW_MS;
    var url = e.destination && e.destination.url;
    log("traverse", {
      cancelable: e.cancelable,
      recentSide: recentSide,
      destination: url
    });
    // A normal Back/Forward button press has no preceding side-button
    // mousedown, so the guard is not armed and the traversal passes.
    if (!recentSide || !guardArmed) return;
    if (e.cancelable) {
      e.preventDefault();
      blockedTraversals++;
      // Consume the guard: one physical press cancels at most one
      // traversal, so a normal Back click right afterwards still works.
      guardArmed = false;
      lastSideAt = 0;
      log("blocked browser history navigation");
    } else {
      log("cross-document traversal could not be cancelled; " +
          "try remapping the side buttons in the mouse driver");
    }
  }

  // If a press produced no traversal at all (for example X2 when the
  // forward stack is empty), drop the guard quickly so an immediately
  // following normal Back click is not swallowed.
  function scheduleDisarm() {
    clearTimeout(disarmTimer);
    disarmTimer = setTimeout(function () {
      guardArmed = false;
    }, DISARM_MS);
  }

  function addListener(target, type, handler, options) {
    target.addEventListener(type, handler, options);
    listeners.push({ target: target, type: type, handler: handler, options: options });
  }

  function onMouseEvent(e) {
    var button = e.button;
    if (button !== BACK && button !== FORWARD) return;
    if (!inPlayer(e.target)) return;

    // Keep the guard window alive across every phase of one physical
    // press (pointerdown -> mousedown -> mouseup -> auxclick), so long
    // presses still get their traversal cancelled.
    lastSideAt = Date.now();

    // Cancelling mouse events alone cannot stop browser-level history
    // navigation, but it is still worth doing for other default actions.
    if (cfg.preventNavigation && e.cancelable) {
      e.preventDefault();
    }

    var isDown = e.type === "pointerdown" || e.type === "mousedown";
    if (isDown) {
      clearTimeout(disarmTimer);
      guardArmed = true;
    } else {
      scheduleDisarm();
      return;
    }

    // Must run synchronously, before the browser starts the traversal.
    ensureGuard(button);

    // Seek once per physical press. pointerdown and mousedown both fire
    // for a single press, so de-duplicate by button + short time window.
    var now = Date.now();
    if (now - lastDownAt < 150 && lastDownButton === button) return;
    lastDownAt = now;
    lastDownButton = button;
    log("event", e.type, "button=" + button, "defaultPrevented=" + e.defaultPrevented);
    doSeek(button);
  }

  function init() {
    EVENTS.forEach(function (type) {
      addListener(document, type, onMouseEvent, { capture: true, passive: false });
    });

    if (navSupported) {
      addListener(window.navigation, "navigate", onNavigate, { capture: false });
    } else {
      console.warn("[" + ID + "] Navigation API unavailable: browser-level " +
        "back/forward cannot be blocked on this browser (needs Chrome/Edge 102+)");
    }

    window.SideButtonSeek = {
      version: VERSION,
      defaults: DEFAULTS,
      get settings() { return Object.assign({}, cfg); },
      get player() { return getPlayer(); },
      get guard() {
        return {
          navigationApi: navSupported,
          windowMs: NAV_WINDOW_MS,
          lastSideAt: lastSideAt,
          guardPushes: guardPushes,
          blockedTraversals: blockedTraversals,
          historyLength: window.history.length,
          entries: navSupported ? window.navigation.entries().map(function (x) {
            return { url: x.url, sameDocument: x.sameDocument };
          }) : null
        };
      },
      reload: loadSettings,
      seek: function (delta) { return seek(delta); },
      simulate: function (button) { return doSeek(button === undefined ? FORWARD : button); },
      setStep: function (seconds) { return saveStep(seconds); },
      get stepButton() { return stepBtn; },
      _disable: function () {
        listeners.forEach(function (l) {
          l.target.removeEventListener(l.type, l.handler, l.options);
        });
        listeners = [];
        clearTimeout(osdTimer);
        clearTimeout(disarmTimer);
        clearInterval(uiPollTimer);
        if (osdEl) osdEl.remove();
        osdEl = null;
        removeStepUI();
      }
    };

    // Attach the in-player step button. A light poll also re-attaches it
    // after Stash's SPA navigation replaces the player container.
    ensureStepUI();
    uiPollTimer = setInterval(ensureStepUI, UI_POLL_MS);

    loadSettings().then(function () { ensureStepUI(); });
    console.log("[" + ID + "] v" + VERSION + " loaded: X1 = back, X2 = forward" +
      (navSupported ? " (Navigation API guard active)" : " (legacy mode)"));
  }

  init();
})();

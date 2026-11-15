/*
 * Side Button Seek - a Stash UI plugin
 * ------------------------------------------------------------------
 * Mouse side buttons are MouseEvent.button 3 (X1 / browser back) and
 * 4 (X2 / browser forward). Stash does not bind them, and Chromium maps
 * them to history back/forward, so pressing them either does nothing or
 * navigates away. This plugin captures those events over the VideoJS
 * player, cancels the navigation default action and seeks the video.
 *
 * Install: put this file next to sideButtonSeek.yml in the Stash plugins
 * directory, then Settings > Plugins > Reload plugins, then refresh (F5).
 * Settings are read from the plugin settings UI via GraphQL; refresh the
 * page after changing them (or run SideButtonSeek.reload() in devtools).
 *
 * Note: a few Chromium/Edge builds perform the history navigation at the
 * browser level and ignore preventDefault() for X1/X2. If the page still
 * goes back, remap the side buttons to the Left/Right arrow keys in your
 * mouse driver (X-Mouse Button Control / Logitech / Razer / AutoHotkey).
 * Stash's built-in arrow shortcuts will then do the seeking.
 *
 * Console helpers:
 *   SideButtonSeek.settings          - active configuration
 *   SideButtonSeek.reload()          - re-read plugin settings
 *   SideButtonSeek.seek(10)          - seek by an arbitrary amount
 *   SideButtonSeek.simulate(3|4)     - trigger a button without a mouse
 *   SideButtonSeek.player            - the current VideoJS player
 */
(function () {
  "use strict";

  var ID = "sideButtonSeek";
  var VERSION = "1.0.0";
  var BACK = 3;    // X1 / browser back
  var FORWARD = 4; // X2 / browser forward

  var DEFAULTS = Object.freeze({
    seekSeconds: 10,
    swapButtons: false,
    onlyInPlayer: true,
    showOsd: true,
    preventNavigation: true,
    debug: false
  });

  var EVENTS = ["pointerdown", "mousedown", "mouseup", "auxclick"];

  var cfg = Object.assign({}, DEFAULTS);
  var listeners = [];
  var lastDownAt = 0;
  var lastDownButton = -1;
  var osdEl = null;
  var osdTimer = null;

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

  function onMouseEvent(e) {
    var button = e.button;
    if (button !== BACK && button !== FORWARD) return;
    if (!inPlayer(e.target)) return;

    // The important part: cancel the browser's history back/forward
    // default action on every phase of the click.
    if (cfg.preventNavigation && e.cancelable) {
      e.preventDefault();
    }

    // Seek once per physical press. pointerdown and mousedown both fire
    // for a single press, so de-duplicate by button + short time window.
    if (e.type !== "pointerdown" && e.type !== "mousedown") return;
    var now = Date.now();
    if (now - lastDownAt < 150 && lastDownButton === button) return;
    lastDownAt = now;
    lastDownButton = button;
    log("event", e.type, "button=" + button, "defaultPrevented=" + e.defaultPrevented);
    doSeek(button);
  }

  function init() {
    EVENTS.forEach(function (type) {
      var options = { capture: true, passive: false };
      document.addEventListener(type, onMouseEvent, options);
      listeners.push({ type: type, options: options });
    });

    window.SideButtonSeek = {
      version: VERSION,
      defaults: DEFAULTS,
      get settings() { return Object.assign({}, cfg); },
      get player() { return getPlayer(); },
      reload: loadSettings,
      seek: function (delta) { return seek(delta); },
      simulate: function (button) { return doSeek(button === undefined ? FORWARD : button); },
      _disable: function () {
        listeners.forEach(function (l) {
          document.removeEventListener(l.type, onMouseEvent, l.options);
        });
        listeners = [];
        clearTimeout(osdTimer);
        if (osdEl) osdEl.remove();
        osdEl = null;
      }
    };

    loadSettings();
    console.log("[" + ID + "] v" + VERSION + " loaded: X1 = back, X2 = forward");
  }

  init();
})();

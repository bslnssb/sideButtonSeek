<p align="center" translate="no">
  <b>English</b> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.zh-TW.md">繁體中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.ru.md">Русский</a> · <a href="README.de.md">Deutsch</a><br>
  <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a> · <a href="README.pt.md">Português</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.th.md">ไทย</a> · <a href="README.el.md">Ελληνικά</a>
</p>

# Side Button Seek

**Use your mouse side buttons (X1 = back, X2 = forward) to seek Stash's scene player — and stop the browser from navigating away.**

Stash only binds seeking to the arrow keys. In a browser the two thumb buttons are `MouseEvent.button` 3 and 4, which Chromium maps to history back/forward. This plugin captures those events over the VideoJS player, cancels the navigation, and moves the playhead instead.

## What it does
- **X1** (rear thumb button) → seek backwards, **X2** (front thumb button) → seek forwards.
- Default **10 seconds** per press, configurable.
- Blocks the browser back/forward navigation while the pointer is over the player.
- Works in fullscreen, on scene pages, markers and playlists.
- Optional on-screen confirmation (`+10s »` / `« −10s`).
- Only active over the player by default, so the buttons keep working elsewhere in Stash.

## Install
Add this repository as a plugin source, then install the package:

```text
Name:       Side Button Seek
Source URL: https://raw.githubusercontent.com/bslnssb/sideButtonSeek/main/index.yml
Local Path: (leave empty)
```

1. In Stash, open **Settings → Plugins → Available Plugins → Add Source**.
2. Paste the source URL below (leave *Local Path* empty).
3. Expand the new source, tick **Side Button Seek** → **Install**.
4. Click **Reload plugins**, then refresh the page (**F5**).

### Manual install
Copy `sideButtonSeek.yml`, `sideButtonSeek.js` and `manifest` into `plugins/sideButtonSeek/` (next to your Stash `config.yml`), reload plugins and refresh the page.

## Settings

| Setting | Default | Description |
| --- | --- | --- |
| `seekSeconds` | 10 | Seconds to jump on each press. |
| `swapButtons` | false | Reverse which button seeks backwards / forwards. |
| `onlyInPlayer` | true | Only react when the pointer is over the player. |
| `showOsd` | true | Show a brief `+10s` / `−10s` overlay on the video. |
| `preventNavigation` | true | Call `preventDefault()` so the browser does not leave the page. |
| `debug` | false | Log events and seek results to the console. |

Settings are read from Stash's plugin configuration. Refresh the page (or run `SideButtonSeek.reload()` in devtools) after changing them.

## Browser limitations
Since **v2.0.0** the plugin also cancels browser-level history navigation through the Navigation API (Chrome/Edge 102+): any `traverse` immediately after a side-button press is blocked. If the neighbouring history entry belongs to another document, one same-URL guard entry is inserted first so the traversal becomes cancellable — in that case a normal Back press may need one extra click. The guard is created lazily, only on a real side-button press, so setups where the buttons are remapped to keyboard keys are completely unaffected.

Some mouse drivers report the side buttons as keyboard keys or as an OS app command instead of mouse buttons 3/4, so no DOM event reaches the page. The same driver remap solves that too.

## Verify / troubleshooting
Open a scene and press a side button: the time should jump about 10 seconds and a small overlay should appear. For a mouse-free check, run `SideButtonSeek.simulate(4)` / `SideButtonSeek.simulate(3)` in devtools. `SideButtonSeek.settings` shows the active configuration and `SideButtonSeek.player` the VideoJS player.

## How it works
Stash injects the plugin's UI JavaScript. It listens for `pointerdown`, `mousedown`, `mouseup` and `auxclick` in the capture phase, accepts only `button === 3` / `4` inside `.video-js`, calls `preventDefault()`, then seeks via `PluginApi.utils.InteractiveUtils.getPlayer()` → `videojs.getPlayers()` → the `<video>` element. Settings come from `{ configuration { plugins } }`.

**How v2 blocks browser-level navigation (technical):** Chromium handles X1/X2 history traversal outside the page, so `preventDefault()` on mouse events has no effect. A `navigate` event with `navigationType === "traverse"` is `cancelable` only when its destination entry is same-document. On the first side-button press, if the neighbouring entry is cross-document, the plugin calls `history.pushState(state, "", location.href)` to insert a same-URL guard entry (which also truncates the forward stack). Its `navigate` listener then calls `preventDefault()` for traversals within a short window of a side-button press and consumes the guard after one cancellation, while ordinary Back/Forward clicks pass through unchanged. Run `SideButtonSeek.guard` in devtools to inspect guard counters and `navigation.entries()`.

## License
MIT — see [LICENSE](LICENSE).

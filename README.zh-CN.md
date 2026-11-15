<p align="center" translate="no">
  <a href="README.md">English</a> · <b>简体中文</b> · <a href="README.zh-TW.md">繁體中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.ru.md">Русский</a> · <a href="README.de.md">Deutsch</a><br>
  <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a> · <a href="README.pt.md">Português</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.th.md">ไทย</a> · <a href="README.el.md">Ελληνικά</a>
</p>

# Side Button Seek

**用鼠标侧键（X1 后退键 / X2 前进键）控制 Stash 场景播放器快退快进，同时阻止浏览器页面后退。**

Stash 只用方向键跳转。网页里鼠标两个拇指键对应 `MouseEvent.button` 3 和 4，Chromium 默认把它们当成浏览器历史后退/前进。本插件在播放器上捕获这两个事件，取消导航，改为移动播放进度。

## 功能
- **X1**（靠后的拇指键）→ 回退，**X2**（靠前的拇指键）→ 快进。
- 每次默认 **10 秒**，可调。
- 鼠标在播放器上时阻止浏览器前进/后退导航。
- 全屏、场景页、标记、播放队列均可用。
- 可选屏显提示（`+10s »` / `« −10s`）。
- 默认只在播放器区域生效，界面其他地方侧键行为不变。

## 安装
把本仓库添加为插件源，再安装：

```text
Name:       Side Button Seek
Source URL: https://raw.githubusercontent.com/bslnssb/sideButtonSeek/main/index.yml
Local Path: (leave empty)
```

1. 打开 **设置 → 插件 → 可用插件 → 添加源**。
2. 粘贴下方源地址，*本地路径* 留空。
3. 展开新源，勾选 **Side Button Seek** → **安装**。
4. 点 **重载插件**，然后刷新页面（**F5**）。

### 手动安装
把 `sideButtonSeek.yml`、`sideButtonSeek.js`、`manifest` 复制到 `plugins/sideButtonSeek/`（与 Stash 的 `config.yml` 同级），重载插件并刷新页面。

## 设置项

| 设置项 | 默认值 | 说明 |
| --- | --- | --- |
| `seekSeconds` | 10 | 每次按键跳转的秒数。 |
| `swapButtons` | false | 交换两个侧键的快进/回退方向。 |
| `onlyInPlayer` | true | 仅当鼠标位于播放器上时生效。 |
| `showOsd` | true | 在视频上短暂显示 `+10s` / `−10s` 提示。 |
| `showStepButton` | true | 在播放器上显示 ±Ns 按钮，可直接修改跳转步长。 |
| `preventNavigation` | true | 调用 `preventDefault()` 阻止浏览器离开页面。 |
| `debug` | false | 在控制台输出事件与跳转结果。 |

设置值来自 Stash 的插件配置。修改后刷新页面，或在控制台执行 `SideButtonSeek.reload()`。

## 浏览器限制
从 **v2.0.0** 起，插件通过 Navigation API（Chrome/Edge 102+）取消浏览器层的历史跳转：侧键按下后紧接着的 `traverse` 导航会被阻止。若相邻历史记录属于另一个文档，插件会先插入一条同 URL 的守卫记录，使该跳转变为可取消；这种情况下普通「后退」可能需要多按一次。守卫记录只在真正按下侧键时按需创建，因此已把侧键映射为键盘按键的环境完全不受影响。

某些鼠标驱动把侧键直接上报为键盘按键或系统命令，网页收不到 button 3/4 事件，同样需要用驱动改键。

## 验证与排错
打开一个场景按侧键：进度应跳约 10 秒并出现屏显提示。不想动鼠标可在控制台执行 `SideButtonSeek.simulate(4)` / `SideButtonSeek.simulate(3)`；`SideButtonSeek.settings` 查看当前配置，`SideButtonSeek.player` 查看 VideoJS 播放器。

## 实现原理
Stash 注入插件的 UI JavaScript。脚本在捕获阶段监听 `pointerdown`、`mousedown`、`mouseup`、`auxclick`，只接受 `.video-js` 区域内 `button === 3` / `4` 的事件，调用 `preventDefault()`，再依次通过 `PluginApi.utils.InteractiveUtils.getPlayer()` → `videojs.getPlayers()` → `<video>` 元素跳转。设置通过 `{ configuration { plugins } }` 读取。

**v2.1.0 in-player step button:** a small `±Ns` button sits at the right end of the VideoJS control bar (with a corner overlay as fallback). Click it to pick a preset (5 / 10 / 15 / 30 / 60 / 120 s) or type a custom value; **Save** writes it to Stash's plugin settings through `configurePlugin`, so the value persists across reloads and browsers and takes effect immediately. It is a normal flex child of the control bar (corner overlay only when no control bar exists) — it never touches React-owned nodes. Turn it off with `showStepButton`.

**How v2 blocks browser-level navigation (technical):** Chromium handles X1/X2 history traversal outside the page, so `preventDefault()` on mouse events has no effect. A `navigate` event with `navigationType === "traverse"` is `cancelable` only when its destination entry is same-document. On the first side-button press, if the neighbouring entry is cross-document, the plugin calls `history.pushState(state, "", location.href)` to insert a same-URL guard entry (which also truncates the forward stack). Its `navigate` listener then calls `preventDefault()` for traversals within a short window of a side-button press and consumes the guard after one cancellation, while ordinary Back/Forward clicks pass through unchanged. Run `SideButtonSeek.guard` in devtools to inspect guard counters and `navigation.entries()`.

## 许可
MIT — 见 [LICENSE](LICENSE)。

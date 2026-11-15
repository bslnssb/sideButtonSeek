<p align="center" translate="no">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a> · <b>繁體中文</b> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.ru.md">Русский</a> · <a href="README.de.md">Deutsch</a><br>
  <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a> · <a href="README.pt.md">Português</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.th.md">ไทย</a> · <a href="README.el.md">Ελληνικά</a>
</p>

# Side Button Seek

**用滑鼠側鍵（X1 上一頁 / X2 下一頁）控制 Stash 場景播放器快退快進，同時阻止瀏覽器頁面後退。**

Stash 只用方向鍵跳轉。網頁裡兩個拇指鍵對應 `MouseEvent.button` 3 與 4，Chromium 預設把它們當成瀏覽器歷程上一頁/下一頁。本外掛在播放器上擷取這兩個事件、取消導覽，改為移動播放進度。

## 功能
- **X1**（靠後拇指鍵）→ 快退，**X2**（靠前拇指鍵）→ 快進。
- 每次預設 **10 秒**，可調整。
- 滑鼠在播放器上時阻止瀏覽器上一頁/下一頁導覽。
- 全螢幕、場景頁、標記、播放佇列皆可使用。
- 可選螢幕提示（`+10s »` / `« −10s`）。
- 預設只在播放器區域生效。

## 安裝
把本儲存庫加入外掛來源後安裝：

```text
Name:       Side Button Seek
Source URL: https://raw.githubusercontent.com/bslnssb/sideButtonSeek/main/index.yml
Local Path: (leave empty)
```

1. 開啟 **設定 → 外掛 → 可用外掛 → 新增來源**。
2. 貼上下面來源網址，*本機路徑* 留空。
3. 展開新來源，勾選 **Side Button Seek** → **安裝**。
4. 按 **重新載入外掛**，再重新整理頁面（**F5**）。

### 手動安裝
把 `sideButtonSeek.yml`、`sideButtonSeek.js`、`manifest` 複製到 `plugins/sideButtonSeek/`（與 Stash 的 `config.yml` 同層），重新載入外掛並重新整理。

## 設定

| 設定 | 預設值 | 說明 |
| --- | --- | --- |
| `seekSeconds` | 10 | 每次按鍵跳轉的秒數。 |
| `swapButtons` | false | 對調兩個側鍵的快進/快退方向。 |
| `onlyInPlayer` | true | 僅在滑鼠位於播放器上時作用。 |
| `showOsd` | true | 在影片上短暫顯示 `+10s` / `−10s`。 |
| `preventNavigation` | true | 呼叫 `preventDefault()` 阻止瀏覽器離開頁面。 |
| `debug` | false | 在主控台輸出事件與跳轉結果。 |

設定值來自 Stash 外掛設定。修改後重新整理頁面，或執行 `SideButtonSeek.reload()`。

## 瀏覽器限制
部分 Chromium/Edge 版本在瀏覽器層處理導覽，會忽略網頁對 X1/X2 的 `preventDefault()`。若頁面仍後退，請在滑鼠驅動（X-Mouse Button Control、Logitech G Hub、Razer Synapse、AutoHotkey）把側鍵對應成 **← / → 方向鍵**，由 Stash 內建快捷鍵跳轉。

某些滑鼠驅動把側鍵回報為鍵盤按鍵或系統命令，網頁收不到 button 3/4 事件，同樣需用驅動改鍵。

## 驗證與疑難排解
開啟場景按側鍵：進度應跳約 10 秒並出現提示。也可在主控台執行 `SideButtonSeek.simulate(4)` / `SideButtonSeek.simulate(3)`；`SideButtonSeek.settings` 查看設定，`SideButtonSeek.player` 查看播放器。

## 實作原理
Stash 注入外掛的 UI JavaScript。腳本在擷取階段監聽 `pointerdown`、`mousedown`、`mouseup`、`auxclick`，只接受 `.video-js` 內 `button === 3` / `4` 的事件，呼叫 `preventDefault()`，再依序透過 `PluginApi.utils.InteractiveUtils.getPlayer()` → `videojs.getPlayers()` → `<video>` 跳轉。設定由 `{ configuration { plugins } }` 讀取。

## 授權
MIT — 詳見 [LICENSE](LICENSE)。

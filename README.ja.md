<p align="center" translate="no">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.zh-TW.md">繁體中文</a> · <b>日本語</b> · <a href="README.ko.md">한국어</a> · <a href="README.ru.md">Русский</a> · <a href="README.de.md">Deutsch</a><br>
  <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a> · <a href="README.pt.md">Português</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.th.md">ไทย</a> · <a href="README.el.md">Ελληνικά</a>
</p>

# Side Button Seek

**マウスのサイドボタン（X1＝戻る／X2＝進む）で Stash のシーンプレイヤーを早送り・早戻しし、ブラウザのページ移動も防ぎます。**

Stash のシークは矢印キーだけに割り当てられています。ブラウザでは親指ボタンが `MouseEvent.button` 3 と 4 になり、Chromium はこれを履歴の戻る／進むとして扱います。このプラグインはプレイヤー上でそのイベントを捕まえ、ナビゲーションを無効化して再生位置を動かします。

## できること
- **X1**（後ろ側）→ 早戻し、**X2**（前側）→ 早送り。
- 1 回あたり既定 **10 秒**（変更可）。
- ポインタがプレイヤー上にある間、ブラウザの戻る／進むをブロック。
- 全画面・シーンページ・マーカー・キューで動作。
- 画面表示 `+10s »` / `« −10s` は任意。
- 既定ではプレイヤー上のみ有効。

## インストール
このリポジトリをプラグインソースに追加してインストールします：

```text
Name:       Side Button Seek
Source URL: https://raw.githubusercontent.com/bslnssb/sideButtonSeek/main/index.yml
Local Path: (leave empty)
```

1. **Settings → Plugins → Available Plugins → Add Source** を開く。
2. 下のソース URL を貼り付ける（*Local Path* は空）。
3. ソースを展開し **Side Button Seek** にチェック → **Install**。
4. **Reload plugins** を押し、ページを更新（**F5**）。

### 手動インストール
`sideButtonSeek.yml`・`sideButtonSeek.js`・`manifest` を `plugins/sideButtonSeek/`（Stash の `config.yml` と同じ階層）にコピーし、プラグインを再読み込みして更新します。

## 設定

| 設定 | 既定値 | 説明 |
| --- | --- | --- |
| `seekSeconds` | 10 | 1 回で移動する秒数。 |
| `swapButtons` | false | 2 つのボタンの方向を入れ替える。 |
| `onlyInPlayer` | true | プレイヤー上のみ反応する。 |
| `showOsd` | true | `+10s` / `−10s` を一時表示する。 |
| `preventNavigation` | true | `preventDefault()` でページ離脱を防ぐ。 |
| `debug` | false | イベントと結果をコンソールに出力。 |

設定は Stash のプラグイン設定から読み込みます。変更後は再読み込み、または `SideButtonSeek.reload()` を実行してください。

## ブラウザの制限
一部の Chromium/Edge はブラウザ層で履歴移動を行い、X1/X2 の `preventDefault()` を無視します。ページが戻る場合は、マウスドライバ（X-Mouse Button Control、Logicool G HUB、Razer Synapse、AutoHotkey）で側ボタンを **← / → キー** に割り当て、Stash 標準のショートカットを使ってください。

ドライバによっては側ボタンをキーボード入力や OS コマンドとして送るため、button 3/4 の DOM イベントが届きません。この場合もドライバでの割り当て変更で解決します。

## 確認とトラブルシュート
シーンを開いて側ボタンを押すと約 10 秒移動し小さな表示が出ます。マウスを使わず確認するにはコンソールで `SideButtonSeek.simulate(4)` / `SideButtonSeek.simulate(3)`。`SideButtonSeek.settings` で設定、`SideButtonSeek.player` でプレイヤーを確認できます。

## 仕組み
Stash が UI JavaScript を注入します。`pointerdown`／`mousedown`／`mouseup`／`auxclick` をキャプチャ段階で監視し、`.video-js` 内の `button === 3` / `4` のみを受け付け、`preventDefault()` を呼んだ後、`PluginApi.utils.InteractiveUtils.getPlayer()` → `videojs.getPlayers()` → `<video>` の順にシークします。設定は `{ configuration { plugins } }` から取得します。

## ライセンス
MIT — [LICENSE](LICENSE) を参照。

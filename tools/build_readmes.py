#!/usr/bin/env python3
"""Generate the multilingual README files for the Side Button Seek plugin.

Keeps the language bar and the document structure identical across all
translations. Run from anywhere: python tools/build_readmes.py
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE_URL = "https://raw.githubusercontent.com/bslnssb/sideButtonSeek/main/index.yml"

LANGS = [
    ("", "English"),
    ("zh-CN", "简体中文"),
    ("zh-TW", "繁體中文"),
    ("ja", "日本語"),
    ("ko", "한국어"),
    ("ru", "Русский"),
    ("de", "Deutsch"),
    ("es", "Español"),
    ("fr", "Français"),
    ("pt", "Português"),
    ("tr", "Türkçe"),
    ("vi", "Tiếng Việt"),
    ("th", "ไทย"),
    ("el", "Ελληνικά"),
]

# heads: Features, Install, Manual install, Settings, Browser limitations,
#        Verify / troubleshooting, How it works, License
T = {
"": dict(
    tagline="Use your mouse side buttons (X1 = back, X2 = forward) to seek Stash's scene player — and stop the browser from navigating away.",
    intro="Stash only binds seeking to the arrow keys. In a browser the two thumb buttons are `MouseEvent.button` 3 and 4, which Chromium maps to history back/forward. This plugin captures those events over the VideoJS player, cancels the navigation, and moves the playhead instead.",
    heads=["What it does", "Install", "Manual install", "Settings", "Browser limitations", "Verify / troubleshooting", "How it works", "License"],
    feat="- **X1** (rear thumb button) → seek backwards, **X2** (front thumb button) → seek forwards.\n- Default **10 seconds** per press, configurable.\n- Blocks the browser back/forward navigation while the pointer is over the player.\n- Works in fullscreen, on scene pages, markers and playlists.\n- Optional on-screen confirmation (`+10s »` / `« −10s`).\n- Only active over the player by default, so the buttons keep working elsewhere in Stash.",
    inst_intro="Add this repository as a plugin source, then install the package:",
    steps="1. In Stash, open **Settings → Plugins → Available Plugins → Add Source**.\n2. Paste the source URL below (leave *Local Path* empty).\n3. Expand the new source, tick **Side Button Seek** → **Install**.\n4. Click **Reload plugins**, then refresh the page (**F5**).",
    manual="Copy `sideButtonSeek.yml`, `sideButtonSeek.js` and `manifest` into `plugins/sideButtonSeek/` (next to your Stash `config.yml`), reload plugins and refresh the page.",
    th=["Setting", "Default", "Description"],
    desc=["Seconds to jump on each press.", "Reverse which button seeks backwards / forwards.", "Only react when the pointer is over the player.", "Show a brief `+10s` / `−10s` overlay on the video.", "Call `preventDefault()` so the browser does not leave the page.", "Log events and seek results to the console."],
    note="Settings are read from Stash's plugin configuration. Refresh the page (or run `SideButtonSeek.reload()` in devtools) after changing them.",
    lim1="Some Chromium/Edge builds perform history navigation at the browser level and ignore `preventDefault()` for X1/X2. If the page still goes back, remap the side buttons to **Left / Right arrow keys** in your mouse driver (X-Mouse Button Control, Logitech G Hub, Razer Synapse, AutoHotkey). Stash's built-in arrow shortcuts then do the seeking.",
    lim2="Some mouse drivers report the side buttons as keyboard keys or as an OS app command instead of mouse buttons 3/4, so no DOM event reaches the page. The same driver remap solves that too.",
    verify="Open a scene and press a side button: the time should jump about 10 seconds and a small overlay should appear. For a mouse-free check, run `SideButtonSeek.simulate(4)` / `SideButtonSeek.simulate(3)` in devtools. `SideButtonSeek.settings` shows the active configuration and `SideButtonSeek.player` the VideoJS player.",
    how="Stash injects the plugin's UI JavaScript. It listens for `pointerdown`, `mousedown`, `mouseup` and `auxclick` in the capture phase, accepts only `button === 3` / `4` inside `.video-js`, calls `preventDefault()`, then seeks via `PluginApi.utils.InteractiveUtils.getPlayer()` → `videojs.getPlayers()` → the `<video>` element. Settings come from `{ configuration { plugins } }`.",
    lic="MIT — see [LICENSE](LICENSE).",
),
"zh-CN": dict(
    tagline="用鼠标侧键（X1 后退键 / X2 前进键）控制 Stash 场景播放器快退快进，同时阻止浏览器页面后退。",
    intro="Stash 只用方向键跳转。网页里鼠标两个拇指键对应 `MouseEvent.button` 3 和 4，Chromium 默认把它们当成浏览器历史后退/前进。本插件在播放器上捕获这两个事件，取消导航，改为移动播放进度。",
    heads=["功能", "安装", "手动安装", "设置项", "浏览器限制", "验证与排错", "实现原理", "许可"],
    feat="- **X1**（靠后的拇指键）→ 回退，**X2**（靠前的拇指键）→ 快进。\n- 每次默认 **10 秒**，可调。\n- 鼠标在播放器上时阻止浏览器前进/后退导航。\n- 全屏、场景页、标记、播放队列均可用。\n- 可选屏显提示（`+10s »` / `« −10s`）。\n- 默认只在播放器区域生效，界面其他地方侧键行为不变。",
    inst_intro="把本仓库添加为插件源，再安装：",
    steps="1. 打开 **设置 → 插件 → 可用插件 → 添加源**。\n2. 粘贴下方源地址，*本地路径* 留空。\n3. 展开新源，勾选 **Side Button Seek** → **安装**。\n4. 点 **重载插件**，然后刷新页面（**F5**）。",
    manual="把 `sideButtonSeek.yml`、`sideButtonSeek.js`、`manifest` 复制到 `plugins/sideButtonSeek/`（与 Stash 的 `config.yml` 同级），重载插件并刷新页面。",
    th=["设置项", "默认值", "说明"],
    desc=["每次按键跳转的秒数。", "交换两个侧键的快进/回退方向。", "仅当鼠标位于播放器上时生效。", "在视频上短暂显示 `+10s` / `−10s` 提示。", "调用 `preventDefault()` 阻止浏览器离开页面。", "在控制台输出事件与跳转结果。"],
    note="设置值来自 Stash 的插件配置。修改后刷新页面，或在控制台执行 `SideButtonSeek.reload()`。",
    lim1="部分 Chromium/Edge 版本在浏览器层处理后退，会忽略网页对 X1/X2 的 `preventDefault()`。如果页面仍然后退，请在鼠标驱动（X-Mouse Button Control、罗技 G Hub、雷蛇 Synapse、AutoHotkey）里把侧键映射为 **← / → 方向键**，由 Stash 自带快捷键完成跳转。",
    lim2="某些鼠标驱动把侧键直接上报为键盘按键或系统命令，网页收不到 button 3/4 事件，同样需要用驱动改键。",
    verify="打开一个场景按侧键：进度应跳约 10 秒并出现屏显提示。不想动鼠标可在控制台执行 `SideButtonSeek.simulate(4)` / `SideButtonSeek.simulate(3)`；`SideButtonSeek.settings` 查看当前配置，`SideButtonSeek.player` 查看 VideoJS 播放器。",
    how="Stash 注入插件的 UI JavaScript。脚本在捕获阶段监听 `pointerdown`、`mousedown`、`mouseup`、`auxclick`，只接受 `.video-js` 区域内 `button === 3` / `4` 的事件，调用 `preventDefault()`，再依次通过 `PluginApi.utils.InteractiveUtils.getPlayer()` → `videojs.getPlayers()` → `<video>` 元素跳转。设置通过 `{ configuration { plugins } }` 读取。",
    lic="MIT — 见 [LICENSE](LICENSE)。",
),
"zh-TW": dict(
    tagline="用滑鼠側鍵（X1 上一頁 / X2 下一頁）控制 Stash 場景播放器快退快進，同時阻止瀏覽器頁面後退。",
    intro="Stash 只用方向鍵跳轉。網頁裡兩個拇指鍵對應 `MouseEvent.button` 3 與 4，Chromium 預設把它們當成瀏覽器歷程上一頁/下一頁。本外掛在播放器上擷取這兩個事件、取消導覽，改為移動播放進度。",
    heads=["功能", "安裝", "手動安裝", "設定", "瀏覽器限制", "驗證與疑難排解", "實作原理", "授權"],
    feat="- **X1**（靠後拇指鍵）→ 快退，**X2**（靠前拇指鍵）→ 快進。\n- 每次預設 **10 秒**，可調整。\n- 滑鼠在播放器上時阻止瀏覽器上一頁/下一頁導覽。\n- 全螢幕、場景頁、標記、播放佇列皆可使用。\n- 可選螢幕提示（`+10s »` / `« −10s`）。\n- 預設只在播放器區域生效。",
    inst_intro="把本儲存庫加入外掛來源後安裝：",
    steps="1. 開啟 **設定 → 外掛 → 可用外掛 → 新增來源**。\n2. 貼上下面來源網址，*本機路徑* 留空。\n3. 展開新來源，勾選 **Side Button Seek** → **安裝**。\n4. 按 **重新載入外掛**，再重新整理頁面（**F5**）。",
    manual="把 `sideButtonSeek.yml`、`sideButtonSeek.js`、`manifest` 複製到 `plugins/sideButtonSeek/`（與 Stash 的 `config.yml` 同層），重新載入外掛並重新整理。",
    th=["設定", "預設值", "說明"],
    desc=["每次按鍵跳轉的秒數。", "對調兩個側鍵的快進/快退方向。", "僅在滑鼠位於播放器上時作用。", "在影片上短暫顯示 `+10s` / `−10s`。", "呼叫 `preventDefault()` 阻止瀏覽器離開頁面。", "在主控台輸出事件與跳轉結果。"],
    note="設定值來自 Stash 外掛設定。修改後重新整理頁面，或執行 `SideButtonSeek.reload()`。",
    lim1="部分 Chromium/Edge 版本在瀏覽器層處理導覽，會忽略網頁對 X1/X2 的 `preventDefault()`。若頁面仍後退，請在滑鼠驅動（X-Mouse Button Control、Logitech G Hub、Razer Synapse、AutoHotkey）把側鍵對應成 **← / → 方向鍵**，由 Stash 內建快捷鍵跳轉。",
    lim2="某些滑鼠驅動把側鍵回報為鍵盤按鍵或系統命令，網頁收不到 button 3/4 事件，同樣需用驅動改鍵。",
    verify="開啟場景按側鍵：進度應跳約 10 秒並出現提示。也可在主控台執行 `SideButtonSeek.simulate(4)` / `SideButtonSeek.simulate(3)`；`SideButtonSeek.settings` 查看設定，`SideButtonSeek.player` 查看播放器。",
    how="Stash 注入外掛的 UI JavaScript。腳本在擷取階段監聽 `pointerdown`、`mousedown`、`mouseup`、`auxclick`，只接受 `.video-js` 內 `button === 3` / `4` 的事件，呼叫 `preventDefault()`，再依序透過 `PluginApi.utils.InteractiveUtils.getPlayer()` → `videojs.getPlayers()` → `<video>` 跳轉。設定由 `{ configuration { plugins } }` 讀取。",
    lic="MIT — 詳見 [LICENSE](LICENSE)。",
),
"ja": dict(
    tagline="マウスのサイドボタン（X1＝戻る／X2＝進む）で Stash のシーンプレイヤーを早送り・早戻しし、ブラウザのページ移動も防ぎます。",
    intro="Stash のシークは矢印キーだけに割り当てられています。ブラウザでは親指ボタンが `MouseEvent.button` 3 と 4 になり、Chromium はこれを履歴の戻る／進むとして扱います。このプラグインはプレイヤー上でそのイベントを捕まえ、ナビゲーションを無効化して再生位置を動かします。",
    heads=["できること", "インストール", "手動インストール", "設定", "ブラウザの制限", "確認とトラブルシュート", "仕組み", "ライセンス"],
    feat="- **X1**（後ろ側）→ 早戻し、**X2**（前側）→ 早送り。\n- 1 回あたり既定 **10 秒**（変更可）。\n- ポインタがプレイヤー上にある間、ブラウザの戻る／進むをブロック。\n- 全画面・シーンページ・マーカー・キューで動作。\n- 画面表示 `+10s »` / `« −10s` は任意。\n- 既定ではプレイヤー上のみ有効。",
    inst_intro="このリポジトリをプラグインソースに追加してインストールします：",
    steps="1. **Settings → Plugins → Available Plugins → Add Source** を開く。\n2. 下のソース URL を貼り付ける（*Local Path* は空）。\n3. ソースを展開し **Side Button Seek** にチェック → **Install**。\n4. **Reload plugins** を押し、ページを更新（**F5**）。",
    manual="`sideButtonSeek.yml`・`sideButtonSeek.js`・`manifest` を `plugins/sideButtonSeek/`（Stash の `config.yml` と同じ階層）にコピーし、プラグインを再読み込みして更新します。",
    th=["設定", "既定値", "説明"],
    desc=["1 回で移動する秒数。", "2 つのボタンの方向を入れ替える。", "プレイヤー上のみ反応する。", "`+10s` / `−10s` を一時表示する。", "`preventDefault()` でページ離脱を防ぐ。", "イベントと結果をコンソールに出力。"],
    note="設定は Stash のプラグイン設定から読み込みます。変更後は再読み込み、または `SideButtonSeek.reload()` を実行してください。",
    lim1="一部の Chromium/Edge はブラウザ層で履歴移動を行い、X1/X2 の `preventDefault()` を無視します。ページが戻る場合は、マウスドライバ（X-Mouse Button Control、Logicool G HUB、Razer Synapse、AutoHotkey）で側ボタンを **← / → キー** に割り当て、Stash 標準のショートカットを使ってください。",
    lim2="ドライバによっては側ボタンをキーボード入力や OS コマンドとして送るため、button 3/4 の DOM イベントが届きません。この場合もドライバでの割り当て変更で解決します。",
    verify="シーンを開いて側ボタンを押すと約 10 秒移動し小さな表示が出ます。マウスを使わず確認するにはコンソールで `SideButtonSeek.simulate(4)` / `SideButtonSeek.simulate(3)`。`SideButtonSeek.settings` で設定、`SideButtonSeek.player` でプレイヤーを確認できます。",
    how="Stash が UI JavaScript を注入します。`pointerdown`／`mousedown`／`mouseup`／`auxclick` をキャプチャ段階で監視し、`.video-js` 内の `button === 3` / `4` のみを受け付け、`preventDefault()` を呼んだ後、`PluginApi.utils.InteractiveUtils.getPlayer()` → `videojs.getPlayers()` → `<video>` の順にシークします。設定は `{ configuration { plugins } }` から取得します。",
    lic="MIT — [LICENSE](LICENSE) を参照。",
),
"ko": dict(
    tagline="마우스 측면 버튼(X1 = 뒤로, X2 = 앞으로)으로 Stash 장면 플레이어를 앞뒤로 탐색하고, 브라우저가 페이지를 벗어나지 않게 합니다.",
    intro="Stash는 탐색을 화살표 키에만 연결합니다. 브라우저에서 엄지 버튼은 `MouseEvent.button` 3과 4이며 Chromium은 이를 방문 기록 뒤로/앞으로로 처리합니다. 이 플러그인은 플레이어 위에서 해당 이벤트를 잡아 이동을 취소하고 재생 위치를 옮깁니다.",
    heads=["기능", "설치", "수동 설치", "설정", "브라우저 제한", "확인 및 문제 해결", "동작 원리", "라이선스"],
    feat="- **X1**(뒤쪽 버튼) → 뒤로, **X2**(앞쪽 버튼) → 앞으로.\n- 기본 **10초**, 변경 가능.\n- 포인터가 플레이어 위에 있는 동안 브라우저 뒤로/앞로 차단.\n- 전체 화면, 장면 페이지, 마커, 재생목록에서 동작.\n- 화면 표시 `+10s »` / `« −10s` 선택 가능.\n- 기본적으로 플레이어 위에서만 동작.",
    inst_intro="이 저장소를 플러그인 소스로 추가한 뒤 설치합니다:",
    steps="1. **Settings → Plugins → Available Plugins → Add Source** 열기.\n2. 아래 소스 URL을 붙여넣기(*Local Path*는 비워 둠).\n3. 소스를 펼치고 **Side Button Seek** 선택 → **Install**.\n4. **Reload plugins** 클릭 후 페이지 새로고침(**F5**).",
    manual="`sideButtonSeek.yml`, `sideButtonSeek.js`, `manifest`를 `plugins/sideButtonSeek/`(Stash `config.yml`과 같은 위치)에 복사하고 플러그인을 다시 불러온 뒤 새로고침합니다.",
    th=["설정", "기본값", "설명"],
    desc=["한 번 누를 때 이동할 초.", "두 버튼의 방향을 바꿈.", "플레이어 위에서만 반응.", "`+10s` / `−10s` 잠시 표시.", "`preventDefault()`로 페이지 이탈 방지.", "이벤트와 결과를 콘솔에 기록."],
    note="설정은 Stash 플러그인 설정에서 읽습니다. 변경 후 새로고침하거나 `SideButtonSeek.reload()`를 실행하세요.",
    lim1="일부 Chromium/Edge는 브라우저 수준에서 기록 이동을 처리해 X1/X2의 `preventDefault()`를 무시합니다. 페이지가 계속 뒤로 가면 마우스 드라이버(X-Mouse Button Control, Logitech G Hub, Razer Synapse, AutoHotkey)에서 측면 버튼을 **← / → 키**로 매핑하세요. Stash 기본 단축키가 탐색을 담당합니다.",
    lim2="일부 드라이버는 측면 버튼을 키보드 입력이나 OS 명령으로 보내 button 3/4 DOM 이벤트가 전달되지 않습니다. 이 경우에도 드라이버 매핑으로 해결됩니다.",
    verify="장면을 열고 측면 버튼을 누르면 약 10초 이동하며 작은 표시가 나타납니다. 마우스 없이 확인하려면 콘솔에서 `SideButtonSeek.simulate(4)` / `SideButtonSeek.simulate(3)`을 실행하세요. `SideButtonSeek.settings`는 현재 설정, `SideButtonSeek.player`는 VideoJS 플레이어입니다.",
    how="Stash가 UI JavaScript를 주입합니다. `pointerdown`, `mousedown`, `mouseup`, `auxclick`을 캡처 단계에서 감지해 `.video-js` 안의 `button === 3` / `4`만 받고 `preventDefault()` 후 `PluginApi.utils.InteractiveUtils.getPlayer()` → `videojs.getPlayers()` → `<video>` 순서로 탐색합니다. 설정은 `{ configuration { plugins } }`에서 읽습니다.",
    lic="MIT — [LICENSE](LICENSE) 참조.",
),
"ru": dict(
    tagline="Боковые кнопки мыши (X1 = назад, X2 = вперёд) перематывают видео в плеере Stash и не дают браузеру уйти со страницы.",
    intro="В Stash перемотка назначена только на стрелки клавиатуры. В браузере боковые кнопки мыши — это `MouseEvent.button` 3 и 4, которые Chromium использует для истории назад/вперёд. Плагин перехватывает эти события над плеером, отменяет переход и вместо этого сдвигает позицию воспроизведения.",
    heads=["Возможности", "Установка", "Установка вручную", "Настройки", "Ограничения браузера", "Проверка и диагностика", "Как это работает", "Лицензия"],
    feat="- **X1** (задняя кнопка) → назад, **X2** (передняя) → вперёд.\n- По умолчанию **10 секунд** за нажатие, значение меняется.\n- Блокирует переход назад/вперёд, пока курсор над плеером.\n- Работает в полноэкранном режиме, на страницах сцен, маркеров и в очереди.\n- Необязательное сообщение `+10s »` / `« −10s` поверх видео.\n- По умолчанию активен только над плеером.",
    inst_intro="Добавьте этот репозиторий как источник плагинов и установите пакет:",
    steps="1. Откройте **Settings → Plugins → Available Plugins → Add Source**.\n2. Вставьте URL ниже (*Local Path* оставьте пустым).\n3. Раскройте источник, отметьте **Side Button Seek** → **Install**.\n4. Нажмите **Reload plugins** и обновите страницу (**F5**).",
    manual="Скопируйте `sideButtonSeek.yml`, `sideButtonSeek.js` и `manifest` в `plugins/sideButtonSeek/` (рядом с `config.yml` Stash), перезагрузите плагины и обновите страницу.",
    th=["Параметр", "По умолчанию", "Описание"],
    desc=["Секунд за одно нажатие.", "Поменять направления кнопок местами.", "Реагировать только над плеером.", "Кратко показывать `+10s` / `−10s`.", "`preventDefault()` чтобы браузер не ушёл со страницы.", "Выводить события и результат в консоль."],
    note="Настройки читаются из конфигурации плагинов Stash. После изменения обновите страницу или вызовите `SideButtonSeek.reload()`.",
    lim1="Некоторые сборки Chromium/Edge обрабатывают переход по истории на уровне браузера и игнорируют `preventDefault()` для X1/X2. Если страница всё равно уходит назад, назначьте боковым кнопкам **← / →** в драйвере мыши (X-Mouse Button Control, Logitech G Hub, Razer Synapse, AutoHotkey) — перемотку выполнят встроенные горячие клавиши Stash.",
    lim2="Некоторые драйверы передают боковые кнопки как клавиши клавиатуры или системную команду, поэтому события button 3/4 не доходят до страницы. Помогает тот же способ.",
    verify="Откройте сцену и нажмите боковую кнопку: время сдвинется примерно на 10 секунд и появится краткое сообщение. Без мыши проверьте в консоли `SideButtonSeek.simulate(4)` / `SideButtonSeek.simulate(3)`; `SideButtonSeek.settings` покажет настройки, `SideButtonSeek.player` — плеер VideoJS.",
    how="Stash внедряет UI-JavaScript плагина. Он слушает `pointerdown`, `mousedown`, `mouseup` и `auxclick` на фазе захвата, принимает только `button === 3` / `4` внутри `.video-js`, вызывает `preventDefault()` и перематывает через `PluginApi.utils.InteractiveUtils.getPlayer()` → `videojs.getPlayers()` → элемент `<video>`. Настройки берутся из `{ configuration { plugins } }`.",
    lic="MIT — см. [LICENSE](LICENSE).",
),
"de": dict(
    tagline="Mit den Maustasten (X1 = zurück, X2 = vor) im Stash-Player spulen — ohne dass der Browser die Seite verlässt.",
    intro="Stash bindet das Spulen nur an die Pfeiltasten. Im Browser sind die beiden Daumentasten `MouseEvent.button` 3 und 4, die Chromium als Zurück/Vor im Verlauf interpretiert. Dieses Plugin fängt die Ereignisse über dem VideoJS-Player ab, verhindert die Navigation und verschiebt stattdessen die Wiedergabeposition.",
    heads=["Funktionen", "Installation", "Manuelle Installation", "Einstellungen", "Browser-Einschränkungen", "Prüfen und Fehlersuche", "Funktionsweise", "Lizenz"],
    feat="- **X1** (hintere Taste) → zurück, **X2** (vordere Taste) → vor.\n- Standard **10 Sekunden** pro Klick, einstellbar.\n- Blockiert Zurück/Vor, solange der Zeiger über dem Player ist.\n- Funktioniert im Vollbild, auf Szenenseiten, bei Markern und Warteschlangen.\n- Optionale Einblendung `+10s »` / `« −10s`.\n- Standardmäßig nur über dem Player aktiv.",
    inst_intro="Dieses Repository als Plugin-Quelle hinzufügen und das Paket installieren:",
    steps="1. **Settings → Plugins → Available Plugins → Add Source** öffnen.\n2. Die untenstehende Quell-URL einfügen (*Local Path* leer lassen).\n3. Quelle aufklappen, **Side Button Seek** anhaken → **Install**.\n4. **Reload plugins** klicken und die Seite aktualisieren (**F5**).",
    manual="`sideButtonSeek.yml`, `sideButtonSeek.js` und `manifest` nach `plugins/sideButtonSeek/` kopieren (neben die `config.yml` von Stash), Plugins neu laden und die Seite aktualisieren.",
    th=["Einstellung", "Standard", "Beschreibung"],
    desc=["Sekunden pro Tastendruck.", "Richtung der beiden Tasten tauschen.", "Nur über dem Player reagieren.", "`+10s` / `−10s` kurz einblenden.", "`preventDefault()` verhindert, dass der Browser die Seite verlässt.", "Ereignisse und Ergebnisse in der Konsole protokollieren."],
    note="Einstellungen stammen aus der Plugin-Konfiguration von Stash. Nach Änderungen die Seite aktualisieren oder `SideButtonSeek.reload()` aufrufen.",
    lim1="Manche Chromium/Edge-Builds führen die Verlaufsnavigation auf Browser-Ebene aus und ignorieren `preventDefault()` für X1/X2. Falls die Seite trotzdem zurückspringt, die Seitentasten im Maustreiber (X-Mouse Button Control, Logitech G Hub, Razer Synapse, AutoHotkey) auf **← / →** legen; dann übernehmen die Stash-Shortcuts das Spulen.",
    lim2="Manche Treiber melden die Seitentasten als Tastatur-Eingabe oder Systembefehl, sodass button 3/4 die Seite nie erreichen. Auch hier hilft das Umbelegen im Treiber.",
    verify="Szene öffnen und eine Seitentaste drücken: Die Zeit springt etwa 10 Sekunden, eine kleine Einblendung erscheint. Ohne Maus in der Konsole `SideButtonSeek.simulate(4)` / `SideButtonSeek.simulate(3)` prüfen; `SideButtonSeek.settings` zeigt die Konfiguration, `SideButtonSeek.player` den VideoJS-Player.",
    how="Stash bindet das UI-JavaScript des Plugins ein. Es lauscht in der Capture-Phase auf `pointerdown`, `mousedown`, `mouseup` und `auxclick`, akzeptiert nur `button === 3` / `4` innerhalb von `.video-js`, ruft `preventDefault()` und spult über `PluginApi.utils.InteractiveUtils.getPlayer()` → `videojs.getPlayers()` → das `<video>`-Element. Einstellungen kommen aus `{ configuration { plugins } }`.",
    lic="MIT — siehe [LICENSE](LICENSE).",
),
"es": dict(
    tagline="Usa los botones laterales del ratón (X1 = atrás, X2 = adelante) para avanzar o retroceder en el reproductor de Stash sin que el navegador cambie de página.",
    intro="Stash solo asigna la búsqueda a las flechas del teclado. En el navegador, los dos botones del pulgar son `MouseEvent.button` 3 y 4, que Chromium interpreta como atrás/adelante en el historial. Este plugin captura esos eventos sobre el reproductor VideoJS, cancela la navegación y mueve la posición de reproducción.",
    heads=["Qué hace", "Instalación", "Instalación manual", "Ajustes", "Limitaciones del navegador", "Verificación y solución de problemas", "Cómo funciona", "Licencia"],
    feat="- **X1** (botón trasero) → retroceder, **X2** (botón delantero) → avanzar.\n- **10 segundos** por pulsación por defecto, configurable.\n- Bloquea atrás/adelante mientras el puntero está sobre el reproductor.\n- Funciona en pantalla completa, escenas, marcadores y colas.\n- Aviso opcional en pantalla `+10s »` / `« −10s`.\n- Por defecto solo actúa sobre el reproductor.",
    inst_intro="Añade este repositorio como fuente de plugins e instala el paquete:",
    steps="1. Abre **Settings → Plugins → Available Plugins → Add Source**.\n2. Pega la URL de abajo (deja *Local Path* vacío).\n3. Despliega la fuente, marca **Side Button Seek** → **Install**.\n4. Pulsa **Reload plugins** y recarga la página (**F5**).",
    manual="Copia `sideButtonSeek.yml`, `sideButtonSeek.js` y `manifest` en `plugins/sideButtonSeek/` (junto al `config.yml` de Stash), recarga los plugins y actualiza la página.",
    th=["Ajuste", "Predeterminado", "Descripción"],
    desc=["Segundos que avanza cada pulsación.", "Invierte la dirección de los dos botones.", "Solo actúa sobre el reproductor.", "Muestra `+10s` / `−10s` brevemente.", "`preventDefault()` evita que el navegador salga de la página.", "Registra eventos y resultados en la consola."],
    note="Los ajustes se leen de la configuración de plugins de Stash. Tras cambiarlos, recarga la página o ejecuta `SideButtonSeek.reload()`.",
    lim1="Algunas versiones de Chromium/Edge gestionan la navegación a nivel de navegador e ignoran `preventDefault()` para X1/X2. Si la página sigue yendo atrás, asigna los botones laterales a **← / →** en el driver del ratón (X-Mouse Button Control, Logitech G Hub, Razer Synapse, AutoHotkey); los atajos de Stash harán la búsqueda.",
    lim2="Algunos drivers envían los botones laterales como teclas o comandos del sistema, por lo que los eventos button 3/4 nunca llegan a la página. La misma reassignación lo resuelve.",
    verify="Abre una escena y pulsa un botón lateral: el tiempo salta unos 10 segundos y aparece un aviso. Sin ratón, ejecuta `SideButtonSeek.simulate(4)` / `SideButtonSeek.simulate(3)` en la consola; `SideButtonSeek.settings` muestra la configuración y `SideButtonSeek.player` el reproductor VideoJS.",
    how="Stash inyecta el JavaScript de UI del plugin. Escucha `pointerdown`, `mousedown`, `mouseup` y `auxclick` en fase de captura, acepta solo `button === 3` / `4` dentro de `.video-js`, llama a `preventDefault()` y busca mediante `PluginApi.utils.InteractiveUtils.getPlayer()` → `videojs.getPlayers()` → el elemento `<video>`. Los ajustes vienen de `{ configuration { plugins } }`.",
    lic="MIT — consulta [LICENSE](LICENSE).",
),
"fr": dict(
    tagline="Utilisez les boutons latéraux de la souris (X1 = retour, X2 = avant) pour avancer ou reculer dans le lecteur Stash sans quitter la page.",
    intro="Stash ne lie la recherche qu'aux flèches du clavier. Dans le navigateur, les deux boutons du pouce correspondent à `MouseEvent.button` 3 et 4, que Chromium associe à l'historique précédent/suivant. Ce plugin intercepte ces événements au-dessus du lecteur VideoJS, annule la navigation et déplace la tête de lecture.",
    heads=["Fonctions", "Installation", "Installation manuelle", "Réglages", "Limites du navigateur", "Vérification et dépannage", "Fonctionnement", "Licence"],
    feat="- **X1** (bouton arrière) → reculer, **X2** (bouton avant) → avancer.\n- **10 secondes** par clic par défaut, réglable.\n- Bloque précédent/suivant tant que le pointeur est sur le lecteur.\n- Fonctionne en plein écran, sur les scènes, les marqueurs et les files d'attente.\n- Affichage optionnel `+10s »` / `« −10s`.\n- Actif uniquement sur le lecteur par défaut.",
    inst_intro="Ajoutez ce dépôt comme source de plugins puis installez le paquet :",
    steps="1. Ouvrez **Settings → Plugins → Available Plugins → Add Source**.\n2. Collez l'URL ci-dessous (laissez *Local Path* vide).\n3. Dépliez la source, cochez **Side Button Seek** → **Install**.\n4. Cliquez sur **Reload plugins** puis actualisez la page (**F5**).",
    manual="Copiez `sideButtonSeek.yml`, `sideButtonSeek.js` et `manifest` dans `plugins/sideButtonSeek/` (à côté du `config.yml` de Stash), rechargez les plugins et actualisez.",
    th=["Réglage", "Défaut", "Description"],
    desc=["Secondes sautées à chaque clic.", "Inverse le sens des deux boutons.", "N'agit que sur le lecteur.", "Affiche brièvement `+10s` / `−10s`.", "`preventDefault()` empêche le navigateur de quitter la page.", "Journalise les événements et résultats dans la console."],
    note="Les réglages viennent de la configuration des plugins Stash. Après modification, actualisez la page ou lancez `SideButtonSeek.reload()`.",
    lim1="Certaines versions de Chromium/Edge gèrent la navigation au niveau du navigateur et ignorent `preventDefault()` pour X1/X2. Si la page recule quand même, mappez les boutons latéraux sur **← / →** dans le pilote de la souris (X-Mouse Button Control, Logitech G Hub, Razer Synapse, AutoHotkey) ; les raccourcis Stash prendront le relais.",
    lim2="Certains pilotes envoient les boutons latéraux comme touches clavier ou commande système : les événements button 3/4 n'atteignent jamais la page. Le même remappage résout le problème.",
    verify="Ouvrez une scène et appuyez sur un bouton latéral : le temps saute d'environ 10 secondes et un petit message apparaît. Sans souris, lancez `SideButtonSeek.simulate(4)` / `SideButtonSeek.simulate(3)` dans la console ; `SideButtonSeek.settings` affiche la configuration et `SideButtonSeek.player` le lecteur VideoJS.",
    how="Stash injecte le JavaScript d'interface du plugin. Il écoute `pointerdown`, `mousedown`, `mouseup` et `auxclick` en phase de capture, n'accepte que `button === 3` / `4` dans `.video-js`, appelle `preventDefault()` puis effectue la recherche via `PluginApi.utils.InteractiveUtils.getPlayer()` → `videojs.getPlayers()` → l'élément `<video>`. Les réglages proviennent de `{ configuration { plugins } }`.",
    lic="MIT — voir [LICENSE](LICENSE).",
),
"pt": dict(
    tagline="Use os botões laterais do rato (X1 = voltar, X2 = avançar) para recuar ou avançar no player do Stash sem sair da página.",
    intro="O Stash associa a busca apenas às setas do teclado. No navegador, os dois botões do polegar são `MouseEvent.button` 3 e 4, que o Chromium interpreta como voltar/avançar no histórico. Este plugin captura esses eventos sobre o player VideoJS, cancela a navegação e move a posição de reprodução.",
    heads=["O que faz", "Instalação", "Instalação manual", "Definições", "Limitações do navegador", "Verificação e resolução de problemas", "Como funciona", "Licença"],
    feat="- **X1** (botão traseiro) → recuar, **X2** (botão dianteiro) → avançar.\n- **10 segundos** por clique por omissão, configurável.\n- Bloqueia voltar/avançar enquanto o ponteiro está sobre o player.\n- Funciona em ecrã inteiro, cenas, marcadores e filas.\n- Aviso opcional `+10s »` / `« −10s`.\n- Por omissão só atua sobre o player.",
    inst_intro="Adicione este repositório como fonte de plugins e instale o pacote:",
    steps="1. Abra **Settings → Plugins → Available Plugins → Add Source**.\n2. Cole o URL abaixo (deixe *Local Path* vazio).\n3. Expanda a fonte, marque **Side Button Seek** → **Install**.\n4. Clique em **Reload plugins** e atualize a página (**F5**).",
    manual="Copie `sideButtonSeek.yml`, `sideButtonSeek.js` e `manifest` para `plugins/sideButtonSeek/` (junto do `config.yml` do Stash), recarregue os plugins e atualize a página.",
    th=["Definição", "Padrão", "Descrição"],
    desc=["Segundos por cada clique.", "Inverte a direção dos dois botões.", "Só reage sobre o player.", "Mostra `+10s` / `−10s` por instantes.", "`preventDefault()` impede o navegador de sair da página.", "Regista eventos e resultados na consola."],
    note="As definições vêm da configuração de plugins do Stash. Depois de alterar, atualize a página ou execute `SideButtonSeek.reload()`.",
    lim1="Algumas versões do Chromium/Edge tratam a navegação ao nível do navegador e ignoram `preventDefault()` para X1/X2. Se a página ainda recuar, mapeie os botões laterais para **← / →** no driver do rato (X-Mouse Button Control, Logitech G Hub, Razer Synapse, AutoHotkey); os atalhos do Stash fazem a busca.",
    lim2="Alguns drivers enviam os botões laterais como teclas ou comando do sistema, pelo que os eventos button 3/4 nunca chegam à página. O mesmo remapeamento resolve.",
    verify="Abra uma cena e pressione um botão lateral: o tempo salta cerca de 10 segundos e aparece um pequeno aviso. Sem rato, execute `SideButtonSeek.simulate(4)` / `SideButtonSeek.simulate(3)` na consola; `SideButtonSeek.settings` mostra a configuração e `SideButtonSeek.player` o player VideoJS.",
    how="O Stash injeta o JavaScript de UI do plugin. Ele escuta `pointerdown`, `mousedown`, `mouseup` e `auxclick` na fase de captura, aceita apenas `button === 3` / `4` dentro de `.video-js`, chama `preventDefault()` e faz a busca via `PluginApi.utils.InteractiveUtils.getPlayer()` → `videojs.getPlayers()` → o elemento `<video>`. As definições vêm de `{ configuration { plugins } }`.",
    lic="MIT — consulte [LICENSE](LICENSE).",
),
"tr": dict(
    tagline="Farenin yan tuşlarıyla (X1 = geri, X2 = ileri) Stash oynatıcısında ileri/geri sarın ve tarayıcının sayfadan çıkmasını engelleyin.",
    intro="Stash'te ileri/geri sarma yalnızca ok tuşlarına bağlıdır. Tarayıcıda başparmak tuşları `MouseEvent.button` 3 ve 4'tür ve Chromium bunları geçmiş geri/ileri olarak işler. Bu eklenti, VideoJS oynatıcısı üzerindeki bu olayları yakalar, gezinmeyi iptal eder ve bunun yerine oynatma konumunu değiştirir.",
    heads=["Özellikler", "Kurulum", "Elle kurulum", "Ayarlar", "Tarayıcı sınırlamaları", "Doğrulama ve sorun giderme", "Nasıl çalışır", "Lisans"],
    feat="- **X1** (arka tuş) → geri, **X2** (ön tuş) → ileri.\n- Varsayılan **10 saniye**, değiştirilebilir.\n- İmleç oynatıcı üzerindeyken tarayıcı geri/ileri hareketini engeller.\n- Tam ekran, sahne sayfaları, işaretçiler ve kuyrukta çalışır.\n- İsteğe bağlı `+10s »` / `« −10s` göstergesi.\n- Varsayılan olarak yalnızca oynatıcı üzerinde etkindir.",
    inst_intro="Bu depoyu eklenti kaynağı olarak ekleyin ve paketi kurun:",
    steps="1. **Settings → Plugins → Available Plugins → Add Source** açın.\n2. Aşağıdaki kaynak URL'sini yapıştırın (*Local Path* boş kalsın).\n3. Kaynağı genişletin, **Side Button Seek** işaretleyin → **Install**.\n4. **Reload plugins** tıklayın ve sayfayı yenileyin (**F5**).",
    manual="`sideButtonSeek.yml`, `sideButtonSeek.js` ve `manifest` dosyalarını `plugins/sideButtonSeek/` içine (Stash `config.yml` yanına) kopyalayın, eklentileri yeniden yükleyin ve sayfayı yenileyin.",
    th=["Ayar", "Varsayılan", "Açıklama"],
    desc=["Her basışta atlanacak saniye.", "İki tuşun yönünü değiştirir.", "Yalnızca oynatıcı üzerinde tepki verir.", "`+10s` / `−10s` kısa süre gösterilir.", "`preventDefault()` tarayıcının sayfadan çıkmasını önler.", "Olayları ve sonuçları konsola yazar."],
    note="Ayarlar Stash eklenti yapılandırmasından okunur. Değişiklikten sonra sayfayı yenileyin veya `SideButtonSeek.reload()` çağırın.",
    lim1="Bazı Chromium/Edge sürümleri geçmiş gezinmesini tarayıcı düzeyinde yapar ve X1/X2 için `preventDefault()` çağrısını yok sayar. Sayfa yine geri gidiyorsa, fare sürücüsünde (X-Mouse Button Control, Logitech G Hub, Razer Synapse, AutoHotkey) yan tuşları **← / →** tuşlarına atayın; Stash'in yerleşik kısayolları sarmayı yapar.",
    lim2="Bazı sürücüler yan tuşları klavye tuşu veya sistem komutu olarak bildirir; button 3/4 olayı sayfaya hiç ulaşmaz. Aynı yeniden atama bunu da çözer.",
    verify="Bir sahne açıp yan tuşa basın: süre yaklaşık 10 saniye atlamalı ve küçük bir gösterge çıkmalıdır. Fare olmadan konsolda `SideButtonSeek.simulate(4)` / `SideButtonSeek.simulate(3)` deneyin; `SideButtonSeek.settings` yapılandırmayı, `SideButtonSeek.player` VideoJS oynatıcısını gösterir.",
    how="Stash eklentinin UI JavaScript'ini ekler. `pointerdown`, `mousedown`, `mouseup` ve `auxclick` olaylarını yakalama aşamasında dinler, `.video-js` içinde yalnızca `button === 3` / `4` kabul eder, `preventDefault()` çağırır ve `PluginApi.utils.InteractiveUtils.getPlayer()` → `videojs.getPlayers()` → `<video>` öğesi üzerinden sarar. Ayarlar `{ configuration { plugins } }` sorgusundan gelir.",
    lic="MIT — bkz. [LICENSE](LICENSE).",
),
"vi": dict(
    tagline="Dùng nút bên hông chuột (X1 = lùi, X2 = tiến) để tua video trong trình phát Stash mà không làm trình duyệt rời khỏi trang.",
    intro="Stash chỉ gán việc tua cho các phím mũi tên. Trong trình duyệt, hai nút ngón tay cái là `MouseEvent.button` 3 và 4, được Chromium dùng cho lịch sử lui/tới. Plugin này bắt các sự kiện đó trên trình phát VideoJS, hủy điều hướng và thay vào đó di chuyển vị trí phát.",
    heads=["Tính năng", "Cài đặt", "Cài thủ công", "Thiết lập", "Giới hạn trình duyệt", "Kiểm tra và xử lý sự cố", "Cách hoạt động", "Giấy phép"],
    feat="- **X1** (nút sau) → lùi, **X2** (nút trước) → tiến.\n- Mặc định **10 giây** mỗi lần nhấn, có thể đổi.\n- Chặn lui/tới của trình duyệt khi con trỏ nằm trên trình phát.\n- Hoạt động ở toàn màn hình, trang cảnh, điểm đánh dấu và hàng đợi.\n- Tùy chọn hiển thị `+10s »` / `« −10s`.\n- Mặc định chỉ hoạt động trên trình phát.",
    inst_intro="Thêm kho này làm nguồn plugin rồi cài gói:",
    steps="1. Mở **Settings → Plugins → Available Plugins → Add Source**.\n2. Dán URL nguồn bên dưới (để trống *Local Path*).\n3. Mở rộng nguồn, tick **Side Button Seek** → **Install**.\n4. Bấm **Reload plugins** rồi tải lại trang (**F5**).",
    manual="Sao chép `sideButtonSeek.yml`, `sideButtonSeek.js` và `manifest` vào `plugins/sideButtonSeek/` (cùng cấp `config.yml` của Stash), nạp lại plugin và tải lại trang.",
    th=["Thiết lập", "Mặc định", "Mô tả"],
    desc=["Số giây tua mỗi lần nhấn.", "Đổi ngược hướng hai nút.", "Chỉ phản hồi trên trình phát.", "Hiện thoáng `+10s` / `−10s`.", "`preventDefault()` giữ trình duyệt ở lại trang.", "Ghi sự kiện và kết quả ra console."],
    note="Thiết lập đọc từ cấu hình plugin của Stash. Sau khi đổi, hãy tải lại trang hoặc chạy `SideButtonSeek.reload()`.",
    lim1="Một số bản Chromium/Edge xử lý điều hướng lịch sử ở cấp trình duyệt và bỏ qua `preventDefault()` cho X1/X2. Nếu trang vẫn lùi lại, hãy gán nút hông thành **← / →** trong driver chuột (X-Mouse Button Control, Logitech G Hub, Razer Synapse, AutoHotkey); phím tắt sẵn của Stash sẽ tua thay.",
    lim2="Một số driver gửi nút hông dưới dạng phím bàn phím hoặc lệnh hệ thống, nên sự kiện button 3/4 không tới được trang. Cách gán lại trong driver cũng giải quyết được.",
    verify="Mở một cảnh và nhấn nút hông: thời gian nhảy khoảng 10 giây và hiện thông báo nhỏ. Không cần chuột, chạy `SideButtonSeek.simulate(4)` / `SideButtonSeek.simulate(3)` trong console; `SideButtonSeek.settings` xem cấu hình, `SideButtonSeek.player` xem trình phát VideoJS.",
    how="Stash chèn JavaScript giao diện của plugin. Nó lắng nghe `pointerdown`, `mousedown`, `mouseup`, `auxclick` ở pha capture, chỉ nhận `button === 3` / `4` trong `.video-js`, gọi `preventDefault()` rồi tua qua `PluginApi.utils.InteractiveUtils.getPlayer()` → `videojs.getPlayers()` → phần tử `<video>`. Thiết lập lấy từ `{ configuration { plugins } }`.",
    lic="MIT — xem [LICENSE](LICENSE).",
),
"th": dict(
    tagline="ใช้ปุ่มด้านข้างเมาส์ (X1 = ย้อนกลับ, X2 = ไปข้างหน้า) เพื่อกรอวิดีโอใน Stash โดยไม่ให้เบราว์เซอร์ออกจากหน้า",
    intro="Stash ผูกการกรอไว้กับปุ่มลูกศรเท่านั้น ในเบราว์เซอร์ ปุ่มนิ้วโป้งสองปุ่มคือ `MouseEvent.button` 3 และ 4 ซึ่ง Chromium ใช้เป็นปุ่มย้อนกลับ/ไปข้างหน้าของประวัติ ปลั๊กอินนี้จะดักเหตุการณ์บนตัวเล่น VideoJS ยกเลิกการนำทาง แล้วเลื่อนตำแหน่งการเล่นแทน",
    heads=["ความสามารถ", "ติดตั้ง", "ติดตั้งด้วยตนเอง", "การตั้งค่า", "ข้อจำกัดของเบราว์เซอร์", "ตรวจสอบและแก้ปัญหา", "วิธีทำงาน", "สัญญาอนุญาต"],
    feat="- **X1** (ปุ่มด้านหลัง) → กรอกลับ, **X2** (ปุ่มด้านหน้า) → กรอไปหน้า\n- ค่าเริ่มต้น **10 วินาที** ต่อครั้ง ปรับได้\n- บล็อกปุ่มย้อนกลับ/ไปข้างหน้าขณะเมาส์อยู่บนตัวเล่น\n- ใช้ได้ในโหมดเต็มจอ หน้าซีน มาร์กเกอร์ และคิว\n- แสดง `+10s »` / `« −10s` ได้ตามต้องการ\n- ค่าเริ่มต้นทำงานเฉพาะบนตัวเล่น",
    inst_intro="เพิ่มที่เก็บนี้เป็นแหล่งปลั๊กอิน แล้วติดตั้งแพ็กเกจ:",
    steps="1. เปิด **Settings → Plugins → Available Plugins → Add Source**\n2. วาง URL ด้านล่าง (ปล่อย *Local Path* ว่างไว้)\n3. ขยายแหล่ง เลือก **Side Button Seek** → **Install**\n4. กด **Reload plugins** แล้วรีเฟรชหน้า (**F5**)",
    manual="คัดลอก `sideButtonSeek.yml`, `sideButtonSeek.js` และ `manifest` ไปที่ `plugins/sideButtonSeek/` (ข้าง `config.yml` ของ Stash) โหลดปลั๊กอินใหม่แล้วรีเฟรช",
    th=["การตั้งค่า", "ค่าเริ่มต้น", "คำอธิบาย"],
    desc=["จำนวนวินาทีต่อการกดหนึ่งครั้ง", "สลับทิศทางของปุ่มทั้งสอง", "ตอบสนองเฉพาะบนตัวเล่น", "แสดง `+10s` / `−10s` ชั่วคราว", "`preventDefault()` ไม่ให้เบราว์เซอร์ออกจากหน้า", "บันทึกเหตุการณ์และผลลัพธ์ใน console"],
    note="การตั้งค่าอ่านจากคอนฟิกปลั๊กอินของ Stash หลังเปลี่ยนให้รีเฟรชหน้า หรือรัน `SideButtonSeek.reload()`",
    lim1="Chromium/Edge บางรุ่นจัดการการนำทางในระดับเบราว์เซอร์และละเลย `preventDefault()` สำหรับ X1/X2 หากหน้ายังย้อนกลับ ให้ map ปุ่มด้านข้างเป็น **← / →** ในไดรเวอร์เมาส์ (X-Mouse Button Control, Logitech G Hub, Razer Synapse, AutoHotkey) แล้วใช้ทางลัดของ Stash แทน",
    lim2="ไดรเวอร์บางตัวส่งปุ่มด้านข้างเป็นปุ่มคีย์บอร์ดหรือคำสั่งระบบ ทำให้เหตุการณ์ button 3/4 ไม่ถึงหน้าเว็บ วิธีเดียวกันช่วยได้",
    verify="เปิดซีนแล้วกดปุ่มด้านข้าง เวลาจะกระโดดราว 10 วินาทีและมีข้อความสั้น ๆ ปรากฏ หากไม่ใช้เมาส์ ให้รัน `SideButtonSeek.simulate(4)` / `SideButtonSeek.simulate(3)` ใน console; `SideButtonSeek.settings` แสดงคอนฟิก `SideButtonSeek.player` แสดงตัวเล่น VideoJS",
    how="Stash แทรก JavaScript ส่วน UI ของปลั๊กอิน โดยฟัง `pointerdown`, `mousedown`, `mouseup`, `auxclick` ในระยะ capture รับเฉพาะ `button === 3` / `4` ภายใน `.video-js` เรียก `preventDefault()` แล้วกรอผ่าน `PluginApi.utils.InteractiveUtils.getPlayer()` → `videojs.getPlayers()` → `<video>` การตั้งค่ามาจาก `{ configuration { plugins } }`",
    lic="MIT — ดู [LICENSE](LICENSE)",
),
"el": dict(
    tagline="Χρησιμοποιήστε τα πλαϊνά πλήκτρα του ποντικιού (X1 = πίσω, X2 = εμπρός) για αναζήτηση στον player του Stash, χωρίς ο browser να φεύγει από τη σελίδα.",
    intro="Το Stash συνδέει την αναζήτηση μόνο με τα βέλη του πληκτρολογίου. Στον browser τα δύο πλήκτρα του αντίχειρα είναι `MouseEvent.button` 3 και 4, που το Chromium τα αντιστοιχίζει σε πίσω/εμπρός στο ιστορικό. Το plugin δεσμεύει αυτά τα γεγονότα πάνω από τον VideoJS player, ακυρώνει την πλοήγηση και μετακινεί τη θέση αναπαραγωγής.",
    heads=["Τι κάνει", "Εγκατάσταση", "Χειροκίνητη εγκατάσταση", "Ρυθμίσεις", "Περιορισμοί browser", "Έλεγχος και αντιμετώπιση", "Πώς λειτουργεί", "Άδεια"],
    feat="- **X1** (πίσω πλήκτρο) → προς τα πίσω, **X2** (εμπρός πλήκτρο) → προς τα εμπρός.\n- Προεπιλογή **10 δευτερόλεπτα** ανά πάτημα, ρυθμίζεται.\n- Μπλοκάρει πίσω/εμπρός όσο ο δείκτης είναι πάνω από τον player.\n- Λειτουργεί σε πλήρη οθόνη, σκηνές, δείκτες και λίστες αναπαραγωγής.\n- Προαιρετική ένδειξη `+10s »` / `« −10s`.\n- Ενεργό μόνο πάνω από τον player εξ ορισμού.",
    inst_intro="Προσθέστε αυτό το αποθετήριο ως πηγή plugin και εγκαταστήστε το πακέτο:",
    steps="1. Ανοίξτε **Settings → Plugins → Available Plugins → Add Source**.\n2. Επικολλήστε το URL παρακάτω (αφήστε το *Local Path* κενό).\n3. Αναπτύξτε την πηγή, επιλέξτε **Side Button Seek** → **Install**.\n4. Πατήστε **Reload plugins** και ανανεώστε τη σελίδα (**F5**).",
    manual="Αντιγράψτε τα `sideButtonSeek.yml`, `sideButtonSeek.js` και `manifest` στο `plugins/sideButtonSeek/` (δίπλα στο `config.yml` του Stash), φορτώστε ξανά τα plugins και ανανεώστε.",
    th=["Ρύθμιση", "Προεπιλογή", "Περιγραφή"],
    desc=["Δευτερόλεπτα ανά πάτημα.", "Αντιστρέφει την κατεύθυνση των δύο πλήκτρων.", "Αντιδρά μόνο πάνω από τον player.", "Εμφανίζει στιγμιαία `+10s` / `−10s`.", "Το `preventDefault()` κρατά τον browser στη σελίδα.", "Γράφει γεγονότα και αποτελέσματα στην κονσόλα."],
    note="Οι ρυθμίσεις διαβάζονται από τη διαμόρφωση plugins του Stash. Μετά από αλλαγή, ανανεώστε ή καλέστε `SideButtonSeek.reload()`.",
    lim1="Ορισμένες εκδόσεις Chromium/Edge χειρίζονται την πλοήγηση σε επίπεδο browser και αγνοούν το `preventDefault()` για X1/X2. Αν η σελίδα εξακολουθεί να πηγαίνει πίσω, αντιστοιχίστε τα πλαϊνά πλήκτρα στα **← / →** στο πρόγραμμα οδήγησης του ποντικιού (X-Mouse Button Control, Logitech G Hub, Razer Synapse, AutoHotkey)· οι ενσωματωμένες συντομεύσεις του Stash θα κάνουν την αναζήτηση.",
    lim2="Κάποια προγράμματα οδήγησης στέλνουν τα πλαϊνά πλήκτρα ως πλήκτρα πληκτρολογίου ή εντολή συστήματος, οπότε τα γεγονότα button 3/4 δεν φτάνουν ποτέ στη σελίδα. Η ίδια αντιστοίχιση το λύνει.",
    verify="Ανοίξτε μια σκηνή και πατήστε ένα πλαϊνό πλήκτρο: ο χρόνος μετακινείται περίπου 10 δευτερόλεπτα και εμφανίζεται μια μικρή ένδειξη. Χωρίς ποντίκι, εκτελέστε `SideButtonSeek.simulate(4)` / `SideButtonSeek.simulate(3)` στην κονσόλα· το `SideButtonSeek.settings` δείχνει τις ρυθμίσεις και το `SideButtonSeek.player` τον VideoJS player.",
    how="Το Stash εισάγει το UI JavaScript του plugin. Ακούει `pointerdown`, `mousedown`, `mouseup` και `auxclick` στη φάση capture, δέχεται μόνο `button === 3` / `4` μέσα στο `.video-js`, καλεί `preventDefault()` και κάνει αναζήτηση μέσω `PluginApi.utils.InteractiveUtils.getPlayer()` → `videojs.getPlayers()` → το στοιχείο `<video>`. Οι ρυθμίσεις προέρχονται από `{ configuration { plugins } }`.",
    lic="MIT — δείτε το [LICENSE](LICENSE).",
),
}

SETTING_KEYS = ["seekSeconds", "swapButtons", "onlyInPlayer", "showOsd", "showStepButton", "preventNavigation", "debug"]
SETTING_DEFAULTS = ["10", "false", "true", "true", "true", "true", "false"]

# v2.1.0: description of the in-player seek-step button, in every language.
STEP_DESC = {
    "": "Show a small ±Ns button on the player to change the seek step.",
    "zh-CN": "在播放器上显示 ±Ns 按钮，可直接修改跳转步长。",
    "zh-TW": "在播放器上顯示 ±Ns 按鈕，可直接修改跳轉步長。",
    "ja": "プレイヤーに ±Ns ボタンを表示し、ステップを直接変更できます。",
    "ko": "플레이어에 ±Ns 버튼을 표시해 이동 간격을 바로 변경합니다.",
    "ru": "Показывать кнопку ±Ns на плеере для быстрой смены шага.",
    "de": "Zeigt eine ±Ns-Schaltfläche im Player für den Sprungabstand.",
    "es": "Muestra un botón ±Ns en el reproductor para cambiar el paso.",
    "fr": "Affiche un bouton ±Ns sur le lecteur pour changer le pas.",
    "pt": "Mostra um botão ±Ns no player para alterar o passo.",
    "tr": "Oynatıcıda adımı değiştirmek için ±Ns düğmesi gösterir.",
    "vi": "Hiển thị nút ±Ns trên trình phát để đổi bước nhảy.",
    "th": "แสดงปุ่ม ±Ns บนตัวเล่นเพื่อเปลี่ยนช่วงการข้าม",
    "el": "Εμφανίζει κουμπί ±Ns στον player για αλλαγή του βήματος.",
}


# v2.0.0: the plugin now cancels browser-level history traversal through the
# Navigation API. Replace the old "nothing can be done in the page" paragraph
# with an accurate description, in every language.
V2_LIM1 = {
"": """Since **v2.0.0** the plugin also cancels browser-level history navigation through the Navigation API (Chrome/Edge 102+): any `traverse` immediately after a side-button press is blocked. If the neighbouring history entry belongs to another document, one same-URL guard entry is inserted first so the traversal becomes cancellable — in that case a normal Back press may need one extra click. The guard is created lazily, only on a real side-button press, so setups where the buttons are remapped to keyboard keys are completely unaffected.""",
"zh-CN": """从 **v2.0.0** 起，插件通过 Navigation API（Chrome/Edge 102+）取消浏览器层的历史跳转：侧键按下后紧接着的 `traverse` 导航会被阻止。若相邻历史记录属于另一个文档，插件会先插入一条同 URL 的守卫记录，使该跳转变为可取消；这种情况下普通「后退」可能需要多按一次。守卫记录只在真正按下侧键时按需创建，因此已把侧键映射为键盘按键的环境完全不受影响。""",
"zh-TW": """從 **v2.0.0** 起，外掛透過 Navigation API（Chrome/Edge 102+）取消瀏覽器層的歷程導覽：側鍵按下後緊接的 `traverse` 會被阻擋。若相鄰的歷程項目屬於另一份文件，會先插入一筆同 URL 的守衛項目讓導覽可被取消；此時一般的「上一頁」可能要多按一次。守衛項目只在真正按下側鍵時才建立，因此已將側鍵對應成鍵盤按鍵的環境完全不受影響。""",
"ja": """**v2.0.0** 以降は Navigation API（Chrome/Edge 102+）でブラウザレベルの履歴移動も取り消します。側ボタン直後の `traverse` をブロックし、隣接する履歴項目が別文書の場合は同じ URL のガード項目を 1 件挿入して取消可能にします（この場合、通常の「戻る」はもう一度押す必要があります）。ガードは実際に側ボタンを押したときだけ作られるため、側ボタンをキーボードに割り当て済みの環境には一切影響しません。""",
"ko": """**v2.0.0** 부터는 Navigation API(Chrome/Edge 102+)로 브라우저 수준의 방문 기록 이동도 취소합니다. 측면 버튼 직후의 `traverse`를 차단하며, 인접한 기록 항목이 다른 문서에 속하면 같은 URL의 가드 항목을 하나 넣어 취소 가능하게 만듭니다(이 경우 일반 뒤로 가기를 한 번 더 눌러야 할 수 있습니다). 가드는 실제로 측면 버튼을 눌렀을 때만 만들어지므로 버튼을 키보드 키로 매핑한 환경에는 아무 영향이 없습니다.""",
"ru": """Начиная с **v2.0.0** плагин отменяет переходы в истории на уровне браузера через Navigation API (Chrome/Edge 102+): любой `traverse` сразу после нажатия боковой кнопки блокируется. Если соседняя запись истории принадлежит другому документу, сначала вставляется запись-страж с тем же URL, чтобы переход можно было отменить — в этом случае обычный «Назад» может потребовать лишнего нажатия. Страж создаётся только при реальном нажатии боковой кнопки, поэтому конфигурации с переназначенными на клавиатуру кнопками не затрагиваются.""",
"de": """Seit **v2.0.0** blockiert das Plugin auch die Navigation auf Browser-Ebene über die Navigation API (Chrome/Edge 102+): Jeder `traverse` direkt nach einem Seitentasten-Druck wird abgebrochen. Gehört der benachbarte Verlaufseintrag zu einem anderen Dokument, wird zuerst ein Wächter-Eintrag mit gleicher URL eingefügt, damit der Übergang abbrechbar wird — in diesem Fall kann ein normaler Zurück-Klick einmal zusätzlich nötig sein. Der Wächter entsteht nur bei einem echten Tastendruck; Umgebungen mit auf Tastaturtasten umgemappten Seitentasten bleiben völlig unberührt.""",
"es": """Desde **v2.0.0** el plugin también cancela la navegación del historial a nivel de navegador mediante la Navigation API (Chrome/Edge 102+): se bloquea cualquier `traverse` inmediatamente posterior a pulsar un botón lateral. Si la entrada vecina del historial pertenece a otro documento, se inserta antes una entrada de guarda con la misma URL para que el salto sea cancelable; en ese caso un Atrás normal puede requerir un clic adicional. La guarda se crea solo al pulsar realmente el botón lateral, por lo que los equipos que han reasignado los botones a teclas no se ven afectados.""",
"fr": """Depuis la **v2.0.0**, le plugin annule aussi la navigation au niveau du navigateur via la Navigation API (Chrome/Edge 102+) : tout `traverse` suivant immédiatement un appui sur un bouton latéral est bloqué. Si l'entrée d'historique voisine appartient à un autre document, une entrée de garde avec la même URL est insérée pour rendre le saut annulable — dans ce cas, un Retour normal peut demander un clic supplémentaire. La garde n'est créée qu'à l'appui réel sur le bouton latéral : les configurations qui remappent les boutons en touches clavier ne sont pas affectées.""",
"pt": """A partir da **v2.0.0** o plugin também cancela a navegação do histórico ao nível do navegador através da Navigation API (Chrome/Edge 102+): qualquer `traverse` logo após pressionar um botão lateral é bloqueado. Se a entrada vizinha do histórico pertencer a outro documento, é inserida primeiro uma entrada de guarda com o mesmo URL para tornar o salto cancelável; nesse caso um Voltar normal pode exigir um clique extra. A guarda só é criada ao pressionar realmente o botão lateral, pelo que os sistemas com os botões remapeados para teclas não são afetados.""",
"tr": """**v2.0.0** sürümünden itibaren eklenti, Navigation API (Chrome/Edge 102+) ile tarayıcı düzeyindeki geçmiş gezinmesini de iptal eder: yan tuşa basılmasının hemen ardından gelen `traverse` engellenir. Komşu geçmiş kaydı başka bir belgeye aitse, geçişi iptal edilebilir kılmak için önce aynı URL'ye sahip bir koruma kaydı eklenir; bu durumda normal Geri tuşuna bir kez daha basmak gerekebilir. Koruma yalnızca gerçekten yan tuşa basıldığında oluşturulur, bu yüzden tuşları klavye tuşlarına eşlenmiş kurulumlar hiç etkilenmez.""",
"vi": """Từ **v2.0.0**, plugin dùng Navigation API (Chrome/Edge 102+) để hủy cả thao tác điều hướng lịch sử ở cấp trình duyệt: mọi `traverse` ngay sau khi nhấn nút bên sẽ bị chặn. Nếu mục lịch sử kế cận thuộc một tài liệu khác, plugin chèn một mục bảo vệ có cùng URL để có thể hủy bước chuyển; khi đó nút Quay lại bình thường có thể cần nhấn thêm một lần. Mục bảo vệ chỉ được tạo khi thực sự nhấn nút bên, nên các máy đã ánh xạ nút bên thành phím bàn phím hoàn toàn không bị ảnh hưởng.""",
"th": """ตั้งแต่ **v2.0.0** ปลั๊กอินใช้ Navigation API (Chrome/Edge 102+) ยกเลิกการนำทางประวัติในระดับเบราว์เซอร์ด้วย: `traverse` ที่เกิดขึ้นทันทีหลังกดปุ่มด้านข้างจะถูกบล็อก หากรายการประวัติที่อยู่ติดกันเป็นของเอกสารอื่น ปลั๊กอินจะแทรกรายการป้องกันที่มี URL เดียวกันก่อนเพื่อให้ยกเลิกได้ ในกรณีนี้การกดย้อนกลับปกติอาจต้องกดเพิ่มอีกครั้ง รายการป้องกันจะถูกสร้างเฉพาะเมื่อมีการกดปุ่มด้านข้างจริง จึงไม่ส่งผลกับเครื่องที่แมปปุ่มด้านข้างเป็นปุ่มคีย์บอร์ด""",
"el": """Από την **v2.0.0** το πρόσθετο ακυρώνει και την πλοήγηση ιστορικού στο επίπεδο του προγράμματος περιήγησης μέσω του Navigation API (Chrome/Edge 102+): κάθε `traverse` αμέσως μετά το πάτημα ενός πλευρικού κουμπιού μπλοκάρεται. Αν η γειτονική καταχώριση ιστορικού ανήκει σε άλλο έγγραφο, εισάγεται πρώτα μια καταχώριση φρουράς με το ίδιο URL ώστε η μετάβαση να μπορεί να ακυρωθεί· σε αυτή την περίπτωση ένα κανονικό Πίσω μπορεί να χρειαστεί ένα επιπλέον κλικ. Η φρουρά δημιουργείται μόνο όντως πατηθεί πλευρικό κουμπί, οπότε οι ρυθμίσεις με αντιστοίχιση σε πλήκτρα δεν επηρεάζονται.""",
}

V2_TECH_NOTE = """**v2.1.0 in-player step button:** a small `±Ns` button sits at the right end of the VideoJS control bar (with a corner overlay as fallback). Click it to pick a preset (5 / 10 / 15 / 30 / 60 / 120 s) or type a custom value; **Save** writes it to Stash's plugin settings through `configurePlugin`, so the value persists across reloads and browsers and takes effect immediately. It is a normal flex child of the control bar (corner overlay only when no control bar exists) — it never touches React-owned nodes. Turn it off with `showStepButton`.

**How v2 blocks browser-level navigation (technical):** Chromium handles X1/X2 history traversal outside the page, so `preventDefault()` on mouse events has no effect. A `navigate` event with `navigationType === "traverse"` is `cancelable` only when its destination entry is same-document. On the first side-button press, if the neighbouring entry is cross-document, the plugin calls `history.pushState(state, "", location.href)` to insert a same-URL guard entry (which also truncates the forward stack). Its `navigate` listener then calls `preventDefault()` for traversals within a short window of a side-button press and consumes the guard after one cancellation, while ordinary Back/Forward clicks pass through unchanged. Run `SideButtonSeek.guard` in devtools to inspect guard counters and `navigation.entries()`."""


def nav_for(active_suffix):
    parts = []
    for suffix, label in LANGS:
        href = "README.md" if not suffix else "README.%s.md" % suffix
        if suffix == active_suffix:
            parts.append("<b>%s</b>" % label)
        else:
            parts.append('<a href="%s">%s</a>' % (href, label))
    line1 = " · ".join(parts[:7]) + "<br>"
    line2 = " · ".join(parts[7:])
    return '<p align="center" translate="no">\n  %s\n  %s\n</p>' % (line1, line2)


TEMPLATE = """@@NAV@@

# Side Button Seek

**@@TAGLINE@@**

@@INTRO@@

## @@H0@@
@@FEAT@@

## @@H1@@
@@INST_INTRO@@

```text
Name:       Side Button Seek
Source URL: @@SOURCE@@
Local Path: (leave empty)
```

@@STEPS@@

### @@H2@@
@@MANUAL@@

## @@H3@@

| @@TH0@@ | @@TH1@@ | @@TH2@@ |
| --- | --- | --- |
@@SETROWS@@

@@NOTE@@

## @@H4@@
@@LIM1@@

@@LIM2@@

## @@H5@@
@@VERIFY@@

## @@H6@@
@@HOW@@

@@V2TECH@@

## @@H7@@
@@LIC@@
"""


def build(suffix, d):
    descs = d["desc"][:4] + [STEP_DESC.get(suffix, STEP_DESC[""])] + d["desc"][4:]
    rows = "\n".join(
        "| `%s` | %s | %s |" % (k, default, desc)
        for k, default, desc in zip(SETTING_KEYS, SETTING_DEFAULTS, descs)
    )
    values = {
        "NAV": nav_for(suffix),
        "TAGLINE": d["tagline"],
        "INTRO": d["intro"],
        "H0": d["heads"][0], "H1": d["heads"][1], "H2": d["heads"][2],
        "H3": d["heads"][3], "H4": d["heads"][4], "H5": d["heads"][5],
        "H6": d["heads"][6], "H7": d["heads"][7],
        "FEAT": d["feat"],
        "INST_INTRO": d["inst_intro"],
        "SOURCE": SOURCE_URL,
        "STEPS": d["steps"],
        "MANUAL": d["manual"],
        "TH0": d["th"][0], "TH1": d["th"][1], "TH2": d["th"][2],
        "SETROWS": rows,
        "NOTE": d["note"],
        "LIM1": V2_LIM1.get(suffix, V2_LIM1[""]), "LIM2": d["lim2"],
        "VERIFY": d["verify"],
        "HOW": d["how"],
        "V2TECH": V2_TECH_NOTE,
        "LIC": d["lic"],
    }
    out = TEMPLATE
    for key, value in values.items():
        out = out.replace("@@%s@@" % key, value)
    return out


def main():
    for suffix, _label in LANGS:
        name = "README.md" if not suffix else "README.%s.md" % suffix
        (ROOT / name).write_text(build(suffix, T[suffix]), encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()

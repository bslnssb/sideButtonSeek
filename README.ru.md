<p align="center" translate="no">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.zh-TW.md">繁體中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <b>Русский</b> · <a href="README.de.md">Deutsch</a><br>
  <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a> · <a href="README.pt.md">Português</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.th.md">ไทย</a> · <a href="README.el.md">Ελληνικά</a>
</p>

# Side Button Seek

**Боковые кнопки мыши (X1 = назад, X2 = вперёд) перематывают видео в плеере Stash и не дают браузеру уйти со страницы.**

В Stash перемотка назначена только на стрелки клавиатуры. В браузере боковые кнопки мыши — это `MouseEvent.button` 3 и 4, которые Chromium использует для истории назад/вперёд. Плагин перехватывает эти события над плеером, отменяет переход и вместо этого сдвигает позицию воспроизведения.

## Возможности
- **X1** (задняя кнопка) → назад, **X2** (передняя) → вперёд.
- По умолчанию **10 секунд** за нажатие, значение меняется.
- Блокирует переход назад/вперёд, пока курсор над плеером.
- Работает в полноэкранном режиме, на страницах сцен, маркеров и в очереди.
- Необязательное сообщение `+10s »` / `« −10s` поверх видео.
- По умолчанию активен только над плеером.

## Установка
Добавьте этот репозиторий как источник плагинов и установите пакет:

```text
Name:       Side Button Seek
Source URL: https://raw.githubusercontent.com/bslnssb/sideButtonSeek/main/index.yml
Local Path: (leave empty)
```

1. Откройте **Settings → Plugins → Available Plugins → Add Source**.
2. Вставьте URL ниже (*Local Path* оставьте пустым).
3. Раскройте источник, отметьте **Side Button Seek** → **Install**.
4. Нажмите **Reload plugins** и обновите страницу (**F5**).

### Установка вручную
Скопируйте `sideButtonSeek.yml`, `sideButtonSeek.js` и `manifest` в `plugins/sideButtonSeek/` (рядом с `config.yml` Stash), перезагрузите плагины и обновите страницу.

## Настройки

| Параметр | По умолчанию | Описание |
| --- | --- | --- |
| `seekSeconds` | 10 | Секунд за одно нажатие. |
| `swapButtons` | false | Поменять направления кнопок местами. |
| `onlyInPlayer` | true | Реагировать только над плеером. |
| `showOsd` | true | Кратко показывать `+10s` / `−10s`. |
| `showStepButton` | true | Показывать кнопку ±Ns на плеере для быстрой смены шага. |
| `preventNavigation` | true | `preventDefault()` чтобы браузер не ушёл со страницы. |
| `debug` | false | Выводить события и результат в консоль. |

Настройки читаются из конфигурации плагинов Stash. После изменения обновите страницу или вызовите `SideButtonSeek.reload()`.

## Ограничения браузера
Начиная с **v2.0.0** плагин отменяет переходы в истории на уровне браузера через Navigation API (Chrome/Edge 102+): любой `traverse` сразу после нажатия боковой кнопки блокируется. Если соседняя запись истории принадлежит другому документу, сначала вставляется запись-страж с тем же URL, чтобы переход можно было отменить — в этом случае обычный «Назад» может потребовать лишнего нажатия. Страж создаётся только при реальном нажатии боковой кнопки, поэтому конфигурации с переназначенными на клавиатуру кнопками не затрагиваются.

Некоторые драйверы передают боковые кнопки как клавиши клавиатуры или системную команду, поэтому события button 3/4 не доходят до страницы. Помогает тот же способ.

## Проверка и диагностика
Откройте сцену и нажмите боковую кнопку: время сдвинется примерно на 10 секунд и появится краткое сообщение. Без мыши проверьте в консоли `SideButtonSeek.simulate(4)` / `SideButtonSeek.simulate(3)`; `SideButtonSeek.settings` покажет настройки, `SideButtonSeek.player` — плеер VideoJS.

## Как это работает
Stash внедряет UI-JavaScript плагина. Он слушает `pointerdown`, `mousedown`, `mouseup` и `auxclick` на фазе захвата, принимает только `button === 3` / `4` внутри `.video-js`, вызывает `preventDefault()` и перематывает через `PluginApi.utils.InteractiveUtils.getPlayer()` → `videojs.getPlayers()` → элемент `<video>`. Настройки берутся из `{ configuration { plugins } }`.

**v2.1.0 in-player step button:** a small `±Ns` button sits at the right end of the VideoJS control bar (with a corner overlay as fallback). Click it to pick a preset (5 / 10 / 15 / 30 / 60 / 120 s) or type a custom value; **Save** writes it to Stash's plugin settings through `configurePlugin`, so the value persists across reloads and browsers and takes effect immediately. It is a normal flex child of the control bar (corner overlay only when no control bar exists) — it never touches React-owned nodes. Turn it off with `showStepButton`.

**How v2 blocks browser-level navigation (technical):** Chromium handles X1/X2 history traversal outside the page, so `preventDefault()` on mouse events has no effect. A `navigate` event with `navigationType === "traverse"` is `cancelable` only when its destination entry is same-document. On the first side-button press, if the neighbouring entry is cross-document, the plugin calls `history.pushState(state, "", location.href)` to insert a same-URL guard entry (which also truncates the forward stack). Its `navigate` listener then calls `preventDefault()` for traversals within a short window of a side-button press and consumes the guard after one cancellation, while ordinary Back/Forward clicks pass through unchanged. Run `SideButtonSeek.guard` in devtools to inspect guard counters and `navigation.entries()`.

## Лицензия
MIT — см. [LICENSE](LICENSE).

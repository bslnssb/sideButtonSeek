<p align="center" translate="no">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.zh-TW.md">繁體中文</a> · <a href="README.ja.md">日本語</a> · <b>한국어</b> · <a href="README.ru.md">Русский</a> · <a href="README.de.md">Deutsch</a><br>
  <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a> · <a href="README.pt.md">Português</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.th.md">ไทย</a> · <a href="README.el.md">Ελληνικά</a>
</p>

# Side Button Seek

**마우스 측면 버튼(X1 = 뒤로, X2 = 앞으로)으로 Stash 장면 플레이어를 앞뒤로 탐색하고, 브라우저가 페이지를 벗어나지 않게 합니다.**

Stash는 탐색을 화살표 키에만 연결합니다. 브라우저에서 엄지 버튼은 `MouseEvent.button` 3과 4이며 Chromium은 이를 방문 기록 뒤로/앞으로로 처리합니다. 이 플러그인은 플레이어 위에서 해당 이벤트를 잡아 이동을 취소하고 재생 위치를 옮깁니다.

## 기능
- **X1**(뒤쪽 버튼) → 뒤로, **X2**(앞쪽 버튼) → 앞으로.
- 기본 **10초**, 변경 가능.
- 포인터가 플레이어 위에 있는 동안 브라우저 뒤로/앞로 차단.
- 전체 화면, 장면 페이지, 마커, 재생목록에서 동작.
- 화면 표시 `+10s »` / `« −10s` 선택 가능.
- 기본적으로 플레이어 위에서만 동작.

## 설치
이 저장소를 플러그인 소스로 추가한 뒤 설치합니다:

```text
Name:       Side Button Seek
Source URL: https://raw.githubusercontent.com/bslnssb/sideButtonSeek/main/index.yml
Local Path: (leave empty)
```

1. **Settings → Plugins → Available Plugins → Add Source** 열기.
2. 아래 소스 URL을 붙여넣기(*Local Path*는 비워 둠).
3. 소스를 펼치고 **Side Button Seek** 선택 → **Install**.
4. **Reload plugins** 클릭 후 페이지 새로고침(**F5**).

### 수동 설치
`sideButtonSeek.yml`, `sideButtonSeek.js`, `manifest`를 `plugins/sideButtonSeek/`(Stash `config.yml`과 같은 위치)에 복사하고 플러그인을 다시 불러온 뒤 새로고침합니다.

## 설정

| 설정 | 기본값 | 설명 |
| --- | --- | --- |
| `seekSeconds` | 10 | 한 번 누를 때 이동할 초. |
| `swapButtons` | false | 두 버튼의 방향을 바꿈. |
| `onlyInPlayer` | true | 플레이어 위에서만 반응. |
| `showOsd` | true | `+10s` / `−10s` 잠시 표시. |
| `preventNavigation` | true | `preventDefault()`로 페이지 이탈 방지. |
| `debug` | false | 이벤트와 결과를 콘솔에 기록. |

설정은 Stash 플러그인 설정에서 읽습니다. 변경 후 새로고침하거나 `SideButtonSeek.reload()`를 실행하세요.

## 브라우저 제한
**v2.0.0** 부터는 Navigation API(Chrome/Edge 102+)로 브라우저 수준의 방문 기록 이동도 취소합니다. 측면 버튼 직후의 `traverse`를 차단하며, 인접한 기록 항목이 다른 문서에 속하면 같은 URL의 가드 항목을 하나 넣어 취소 가능하게 만듭니다(이 경우 일반 뒤로 가기를 한 번 더 눌러야 할 수 있습니다). 가드는 실제로 측면 버튼을 눌렀을 때만 만들어지므로 버튼을 키보드 키로 매핑한 환경에는 아무 영향이 없습니다.

일부 드라이버는 측면 버튼을 키보드 입력이나 OS 명령으로 보내 button 3/4 DOM 이벤트가 전달되지 않습니다. 이 경우에도 드라이버 매핑으로 해결됩니다.

## 확인 및 문제 해결
장면을 열고 측면 버튼을 누르면 약 10초 이동하며 작은 표시가 나타납니다. 마우스 없이 확인하려면 콘솔에서 `SideButtonSeek.simulate(4)` / `SideButtonSeek.simulate(3)`을 실행하세요. `SideButtonSeek.settings`는 현재 설정, `SideButtonSeek.player`는 VideoJS 플레이어입니다.

## 동작 원리
Stash가 UI JavaScript를 주입합니다. `pointerdown`, `mousedown`, `mouseup`, `auxclick`을 캡처 단계에서 감지해 `.video-js` 안의 `button === 3` / `4`만 받고 `preventDefault()` 후 `PluginApi.utils.InteractiveUtils.getPlayer()` → `videojs.getPlayers()` → `<video>` 순서로 탐색합니다. 설정은 `{ configuration { plugins } }`에서 읽습니다.

**How v2 blocks browser-level navigation (technical):** Chromium handles X1/X2 history traversal outside the page, so `preventDefault()` on mouse events has no effect. A `navigate` event with `navigationType === "traverse"` is `cancelable` only when its destination entry is same-document. On the first side-button press, if the neighbouring entry is cross-document, the plugin calls `history.pushState(state, "", location.href)` to insert a same-URL guard entry (which also truncates the forward stack). Its `navigate` listener then calls `preventDefault()` for traversals within a short window of a side-button press and consumes the guard after one cancellation, while ordinary Back/Forward clicks pass through unchanged. Run `SideButtonSeek.guard` in devtools to inspect guard counters and `navigation.entries()`.

## 라이선스
MIT — [LICENSE](LICENSE) 참조.

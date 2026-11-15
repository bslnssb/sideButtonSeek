<p align="center" translate="no">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.zh-TW.md">繁體中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.ru.md">Русский</a> · <a href="README.de.md">Deutsch</a><br>
  <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a> · <a href="README.pt.md">Português</a> · <a href="README.tr.md">Türkçe</a> · <b>Tiếng Việt</b> · <a href="README.th.md">ไทย</a> · <a href="README.el.md">Ελληνικά</a>
</p>

# Side Button Seek

**Dùng nút bên hông chuột (X1 = lùi, X2 = tiến) để tua video trong trình phát Stash mà không làm trình duyệt rời khỏi trang.**

Stash chỉ gán việc tua cho các phím mũi tên. Trong trình duyệt, hai nút ngón tay cái là `MouseEvent.button` 3 và 4, được Chromium dùng cho lịch sử lui/tới. Plugin này bắt các sự kiện đó trên trình phát VideoJS, hủy điều hướng và thay vào đó di chuyển vị trí phát.

## Tính năng
- **X1** (nút sau) → lùi, **X2** (nút trước) → tiến.
- Mặc định **10 giây** mỗi lần nhấn, có thể đổi.
- Chặn lui/tới của trình duyệt khi con trỏ nằm trên trình phát.
- Hoạt động ở toàn màn hình, trang cảnh, điểm đánh dấu và hàng đợi.
- Tùy chọn hiển thị `+10s »` / `« −10s`.
- Mặc định chỉ hoạt động trên trình phát.

## Cài đặt
Thêm kho này làm nguồn plugin rồi cài gói:

```text
Name:       Side Button Seek
Source URL: https://raw.githubusercontent.com/bslnssb/sideButtonSeek/main/index.yml
Local Path: (leave empty)
```

1. Mở **Settings → Plugins → Available Plugins → Add Source**.
2. Dán URL nguồn bên dưới (để trống *Local Path*).
3. Mở rộng nguồn, tick **Side Button Seek** → **Install**.
4. Bấm **Reload plugins** rồi tải lại trang (**F5**).

### Cài thủ công
Sao chép `sideButtonSeek.yml`, `sideButtonSeek.js` và `manifest` vào `plugins/sideButtonSeek/` (cùng cấp `config.yml` của Stash), nạp lại plugin và tải lại trang.

## Thiết lập

| Thiết lập | Mặc định | Mô tả |
| --- | --- | --- |
| `seekSeconds` | 10 | Số giây tua mỗi lần nhấn. |
| `swapButtons` | false | Đổi ngược hướng hai nút. |
| `onlyInPlayer` | true | Chỉ phản hồi trên trình phát. |
| `showOsd` | true | Hiện thoáng `+10s` / `−10s`. |
| `preventNavigation` | true | `preventDefault()` giữ trình duyệt ở lại trang. |
| `debug` | false | Ghi sự kiện và kết quả ra console. |

Thiết lập đọc từ cấu hình plugin của Stash. Sau khi đổi, hãy tải lại trang hoặc chạy `SideButtonSeek.reload()`.

## Giới hạn trình duyệt
Một số bản Chromium/Edge xử lý điều hướng lịch sử ở cấp trình duyệt và bỏ qua `preventDefault()` cho X1/X2. Nếu trang vẫn lùi lại, hãy gán nút hông thành **← / →** trong driver chuột (X-Mouse Button Control, Logitech G Hub, Razer Synapse, AutoHotkey); phím tắt sẵn của Stash sẽ tua thay.

Một số driver gửi nút hông dưới dạng phím bàn phím hoặc lệnh hệ thống, nên sự kiện button 3/4 không tới được trang. Cách gán lại trong driver cũng giải quyết được.

## Kiểm tra và xử lý sự cố
Mở một cảnh và nhấn nút hông: thời gian nhảy khoảng 10 giây và hiện thông báo nhỏ. Không cần chuột, chạy `SideButtonSeek.simulate(4)` / `SideButtonSeek.simulate(3)` trong console; `SideButtonSeek.settings` xem cấu hình, `SideButtonSeek.player` xem trình phát VideoJS.

## Cách hoạt động
Stash chèn JavaScript giao diện của plugin. Nó lắng nghe `pointerdown`, `mousedown`, `mouseup`, `auxclick` ở pha capture, chỉ nhận `button === 3` / `4` trong `.video-js`, gọi `preventDefault()` rồi tua qua `PluginApi.utils.InteractiveUtils.getPlayer()` → `videojs.getPlayers()` → phần tử `<video>`. Thiết lập lấy từ `{ configuration { plugins } }`.

## Giấy phép
MIT — xem [LICENSE](LICENSE).

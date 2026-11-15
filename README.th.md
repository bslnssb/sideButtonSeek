<p align="center" translate="no">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.zh-TW.md">繁體中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.ru.md">Русский</a> · <a href="README.de.md">Deutsch</a><br>
  <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a> · <a href="README.pt.md">Português</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.vi.md">Tiếng Việt</a> · <b>ไทย</b> · <a href="README.el.md">Ελληνικά</a>
</p>

# Side Button Seek

**ใช้ปุ่มด้านข้างเมาส์ (X1 = ย้อนกลับ, X2 = ไปข้างหน้า) เพื่อกรอวิดีโอใน Stash โดยไม่ให้เบราว์เซอร์ออกจากหน้า**

Stash ผูกการกรอไว้กับปุ่มลูกศรเท่านั้น ในเบราว์เซอร์ ปุ่มนิ้วโป้งสองปุ่มคือ `MouseEvent.button` 3 และ 4 ซึ่ง Chromium ใช้เป็นปุ่มย้อนกลับ/ไปข้างหน้าของประวัติ ปลั๊กอินนี้จะดักเหตุการณ์บนตัวเล่น VideoJS ยกเลิกการนำทาง แล้วเลื่อนตำแหน่งการเล่นแทน

## ความสามารถ
- **X1** (ปุ่มด้านหลัง) → กรอกลับ, **X2** (ปุ่มด้านหน้า) → กรอไปหน้า
- ค่าเริ่มต้น **10 วินาที** ต่อครั้ง ปรับได้
- บล็อกปุ่มย้อนกลับ/ไปข้างหน้าขณะเมาส์อยู่บนตัวเล่น
- ใช้ได้ในโหมดเต็มจอ หน้าซีน มาร์กเกอร์ และคิว
- แสดง `+10s »` / `« −10s` ได้ตามต้องการ
- ค่าเริ่มต้นทำงานเฉพาะบนตัวเล่น

## ติดตั้ง
เพิ่มที่เก็บนี้เป็นแหล่งปลั๊กอิน แล้วติดตั้งแพ็กเกจ:

```text
Name:       Side Button Seek
Source URL: https://raw.githubusercontent.com/bslnssb/sideButtonSeek/main/index.yml
Local Path: (leave empty)
```

1. เปิด **Settings → Plugins → Available Plugins → Add Source**
2. วาง URL ด้านล่าง (ปล่อย *Local Path* ว่างไว้)
3. ขยายแหล่ง เลือก **Side Button Seek** → **Install**
4. กด **Reload plugins** แล้วรีเฟรชหน้า (**F5**)

### ติดตั้งด้วยตนเอง
คัดลอก `sideButtonSeek.yml`, `sideButtonSeek.js` และ `manifest` ไปที่ `plugins/sideButtonSeek/` (ข้าง `config.yml` ของ Stash) โหลดปลั๊กอินใหม่แล้วรีเฟรช

## การตั้งค่า

| การตั้งค่า | ค่าเริ่มต้น | คำอธิบาย |
| --- | --- | --- |
| `seekSeconds` | 10 | จำนวนวินาทีต่อการกดหนึ่งครั้ง |
| `swapButtons` | false | สลับทิศทางของปุ่มทั้งสอง |
| `onlyInPlayer` | true | ตอบสนองเฉพาะบนตัวเล่น |
| `showOsd` | true | แสดง `+10s` / `−10s` ชั่วคราว |
| `showStepButton` | true | แสดงปุ่ม ±Ns บนตัวเล่นเพื่อเปลี่ยนช่วงการข้าม |
| `preventNavigation` | true | `preventDefault()` ไม่ให้เบราว์เซอร์ออกจากหน้า |
| `debug` | false | บันทึกเหตุการณ์และผลลัพธ์ใน console |

การตั้งค่าอ่านจากคอนฟิกปลั๊กอินของ Stash หลังเปลี่ยนให้รีเฟรชหน้า หรือรัน `SideButtonSeek.reload()`

## ข้อจำกัดของเบราว์เซอร์
ตั้งแต่ **v2.0.0** ปลั๊กอินใช้ Navigation API (Chrome/Edge 102+) ยกเลิกการนำทางประวัติในระดับเบราว์เซอร์ด้วย: `traverse` ที่เกิดขึ้นทันทีหลังกดปุ่มด้านข้างจะถูกบล็อก หากรายการประวัติที่อยู่ติดกันเป็นของเอกสารอื่น ปลั๊กอินจะแทรกรายการป้องกันที่มี URL เดียวกันก่อนเพื่อให้ยกเลิกได้ ในกรณีนี้การกดย้อนกลับปกติอาจต้องกดเพิ่มอีกครั้ง รายการป้องกันจะถูกสร้างเฉพาะเมื่อมีการกดปุ่มด้านข้างจริง จึงไม่ส่งผลกับเครื่องที่แมปปุ่มด้านข้างเป็นปุ่มคีย์บอร์ด

ไดรเวอร์บางตัวส่งปุ่มด้านข้างเป็นปุ่มคีย์บอร์ดหรือคำสั่งระบบ ทำให้เหตุการณ์ button 3/4 ไม่ถึงหน้าเว็บ วิธีเดียวกันช่วยได้

## ตรวจสอบและแก้ปัญหา
เปิดซีนแล้วกดปุ่มด้านข้าง เวลาจะกระโดดราว 10 วินาทีและมีข้อความสั้น ๆ ปรากฏ หากไม่ใช้เมาส์ ให้รัน `SideButtonSeek.simulate(4)` / `SideButtonSeek.simulate(3)` ใน console; `SideButtonSeek.settings` แสดงคอนฟิก `SideButtonSeek.player` แสดงตัวเล่น VideoJS

## วิธีทำงาน
Stash แทรก JavaScript ส่วน UI ของปลั๊กอิน โดยฟัง `pointerdown`, `mousedown`, `mouseup`, `auxclick` ในระยะ capture รับเฉพาะ `button === 3` / `4` ภายใน `.video-js` เรียก `preventDefault()` แล้วกรอผ่าน `PluginApi.utils.InteractiveUtils.getPlayer()` → `videojs.getPlayers()` → `<video>` การตั้งค่ามาจาก `{ configuration { plugins } }`

**v2.1.0 in-player step button:** a small `±Ns` button sits at the right end of the VideoJS control bar (with a corner overlay as fallback). Click it to pick a preset (5 / 10 / 15 / 30 / 60 / 120 s) or type a custom value; **Save** writes it to Stash's plugin settings through `configurePlugin`, so the value persists across reloads and browsers and takes effect immediately. It is a normal flex child of the control bar (corner overlay only when no control bar exists) — it never touches React-owned nodes. Turn it off with `showStepButton`.

**How v2 blocks browser-level navigation (technical):** Chromium handles X1/X2 history traversal outside the page, so `preventDefault()` on mouse events has no effect. A `navigate` event with `navigationType === "traverse"` is `cancelable` only when its destination entry is same-document. On the first side-button press, if the neighbouring entry is cross-document, the plugin calls `history.pushState(state, "", location.href)` to insert a same-URL guard entry (which also truncates the forward stack). Its `navigate` listener then calls `preventDefault()` for traversals within a short window of a side-button press and consumes the guard after one cancellation, while ordinary Back/Forward clicks pass through unchanged. Run `SideButtonSeek.guard` in devtools to inspect guard counters and `navigation.entries()`.

## สัญญาอนุญาต
MIT — ดู [LICENSE](LICENSE)

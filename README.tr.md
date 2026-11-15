<p align="center" translate="no">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.zh-TW.md">繁體中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.ru.md">Русский</a> · <a href="README.de.md">Deutsch</a><br>
  <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a> · <a href="README.pt.md">Português</a> · <b>Türkçe</b> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.th.md">ไทย</a> · <a href="README.el.md">Ελληνικά</a>
</p>

# Side Button Seek

**Farenin yan tuşlarıyla (X1 = geri, X2 = ileri) Stash oynatıcısında ileri/geri sarın ve tarayıcının sayfadan çıkmasını engelleyin.**

Stash'te ileri/geri sarma yalnızca ok tuşlarına bağlıdır. Tarayıcıda başparmak tuşları `MouseEvent.button` 3 ve 4'tür ve Chromium bunları geçmiş geri/ileri olarak işler. Bu eklenti, VideoJS oynatıcısı üzerindeki bu olayları yakalar, gezinmeyi iptal eder ve bunun yerine oynatma konumunu değiştirir.

## Özellikler
- **X1** (arka tuş) → geri, **X2** (ön tuş) → ileri.
- Varsayılan **10 saniye**, değiştirilebilir.
- İmleç oynatıcı üzerindeyken tarayıcı geri/ileri hareketini engeller.
- Tam ekran, sahne sayfaları, işaretçiler ve kuyrukta çalışır.
- İsteğe bağlı `+10s »` / `« −10s` göstergesi.
- Varsayılan olarak yalnızca oynatıcı üzerinde etkindir.

## Kurulum
Bu depoyu eklenti kaynağı olarak ekleyin ve paketi kurun:

```text
Name:       Side Button Seek
Source URL: https://raw.githubusercontent.com/bslnssb/sideButtonSeek/main/index.yml
Local Path: (leave empty)
```

1. **Settings → Plugins → Available Plugins → Add Source** açın.
2. Aşağıdaki kaynak URL'sini yapıştırın (*Local Path* boş kalsın).
3. Kaynağı genişletin, **Side Button Seek** işaretleyin → **Install**.
4. **Reload plugins** tıklayın ve sayfayı yenileyin (**F5**).

### Elle kurulum
`sideButtonSeek.yml`, `sideButtonSeek.js` ve `manifest` dosyalarını `plugins/sideButtonSeek/` içine (Stash `config.yml` yanına) kopyalayın, eklentileri yeniden yükleyin ve sayfayı yenileyin.

## Ayarlar

| Ayar | Varsayılan | Açıklama |
| --- | --- | --- |
| `seekSeconds` | 10 | Her basışta atlanacak saniye. |
| `swapButtons` | false | İki tuşun yönünü değiştirir. |
| `onlyInPlayer` | true | Yalnızca oynatıcı üzerinde tepki verir. |
| `showOsd` | true | `+10s` / `−10s` kısa süre gösterilir. |
| `preventNavigation` | true | `preventDefault()` tarayıcının sayfadan çıkmasını önler. |
| `debug` | false | Olayları ve sonuçları konsola yazar. |

Ayarlar Stash eklenti yapılandırmasından okunur. Değişiklikten sonra sayfayı yenileyin veya `SideButtonSeek.reload()` çağırın.

## Tarayıcı sınırlamaları
**v2.0.0** sürümünden itibaren eklenti, Navigation API (Chrome/Edge 102+) ile tarayıcı düzeyindeki geçmiş gezinmesini de iptal eder: yan tuşa basılmasının hemen ardından gelen `traverse` engellenir. Komşu geçmiş kaydı başka bir belgeye aitse, geçişi iptal edilebilir kılmak için önce aynı URL'ye sahip bir koruma kaydı eklenir; bu durumda normal Geri tuşuna bir kez daha basmak gerekebilir. Koruma yalnızca gerçekten yan tuşa basıldığında oluşturulur, bu yüzden tuşları klavye tuşlarına eşlenmiş kurulumlar hiç etkilenmez.

Bazı sürücüler yan tuşları klavye tuşu veya sistem komutu olarak bildirir; button 3/4 olayı sayfaya hiç ulaşmaz. Aynı yeniden atama bunu da çözer.

## Doğrulama ve sorun giderme
Bir sahne açıp yan tuşa basın: süre yaklaşık 10 saniye atlamalı ve küçük bir gösterge çıkmalıdır. Fare olmadan konsolda `SideButtonSeek.simulate(4)` / `SideButtonSeek.simulate(3)` deneyin; `SideButtonSeek.settings` yapılandırmayı, `SideButtonSeek.player` VideoJS oynatıcısını gösterir.

## Nasıl çalışır
Stash eklentinin UI JavaScript'ini ekler. `pointerdown`, `mousedown`, `mouseup` ve `auxclick` olaylarını yakalama aşamasında dinler, `.video-js` içinde yalnızca `button === 3` / `4` kabul eder, `preventDefault()` çağırır ve `PluginApi.utils.InteractiveUtils.getPlayer()` → `videojs.getPlayers()` → `<video>` öğesi üzerinden sarar. Ayarlar `{ configuration { plugins } }` sorgusundan gelir.

**How v2 blocks browser-level navigation (technical):** Chromium handles X1/X2 history traversal outside the page, so `preventDefault()` on mouse events has no effect. A `navigate` event with `navigationType === "traverse"` is `cancelable` only when its destination entry is same-document. On the first side-button press, if the neighbouring entry is cross-document, the plugin calls `history.pushState(state, "", location.href)` to insert a same-URL guard entry (which also truncates the forward stack). Its `navigate` listener then calls `preventDefault()` for traversals within a short window of a side-button press and consumes the guard after one cancellation, while ordinary Back/Forward clicks pass through unchanged. Run `SideButtonSeek.guard` in devtools to inspect guard counters and `navigation.entries()`.

## Lisans
MIT — bkz. [LICENSE](LICENSE).

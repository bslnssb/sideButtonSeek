<p align="center" translate="no">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.zh-TW.md">繁體中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.ru.md">Русский</a> · <b>Deutsch</b><br>
  <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a> · <a href="README.pt.md">Português</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.th.md">ไทย</a> · <a href="README.el.md">Ελληνικά</a>
</p>

# Side Button Seek

**Mit den Maustasten (X1 = zurück, X2 = vor) im Stash-Player spulen — ohne dass der Browser die Seite verlässt.**

Stash bindet das Spulen nur an die Pfeiltasten. Im Browser sind die beiden Daumentasten `MouseEvent.button` 3 und 4, die Chromium als Zurück/Vor im Verlauf interpretiert. Dieses Plugin fängt die Ereignisse über dem VideoJS-Player ab, verhindert die Navigation und verschiebt stattdessen die Wiedergabeposition.

## Funktionen
- **X1** (hintere Taste) → zurück, **X2** (vordere Taste) → vor.
- Standard **10 Sekunden** pro Klick, einstellbar.
- Blockiert Zurück/Vor, solange der Zeiger über dem Player ist.
- Funktioniert im Vollbild, auf Szenenseiten, bei Markern und Warteschlangen.
- Optionale Einblendung `+10s »` / `« −10s`.
- Standardmäßig nur über dem Player aktiv.

## Installation
Dieses Repository als Plugin-Quelle hinzufügen und das Paket installieren:

```text
Name:       Side Button Seek
Source URL: https://raw.githubusercontent.com/bslnssb/sideButtonSeek/main/index.yml
Local Path: (leave empty)
```

1. **Settings → Plugins → Available Plugins → Add Source** öffnen.
2. Die untenstehende Quell-URL einfügen (*Local Path* leer lassen).
3. Quelle aufklappen, **Side Button Seek** anhaken → **Install**.
4. **Reload plugins** klicken und die Seite aktualisieren (**F5**).

### Manuelle Installation
`sideButtonSeek.yml`, `sideButtonSeek.js` und `manifest` nach `plugins/sideButtonSeek/` kopieren (neben die `config.yml` von Stash), Plugins neu laden und die Seite aktualisieren.

## Einstellungen

| Einstellung | Standard | Beschreibung |
| --- | --- | --- |
| `seekSeconds` | 10 | Sekunden pro Tastendruck. |
| `swapButtons` | false | Richtung der beiden Tasten tauschen. |
| `onlyInPlayer` | true | Nur über dem Player reagieren. |
| `showOsd` | true | `+10s` / `−10s` kurz einblenden. |
| `preventNavigation` | true | `preventDefault()` verhindert, dass der Browser die Seite verlässt. |
| `debug` | false | Ereignisse und Ergebnisse in der Konsole protokollieren. |

Einstellungen stammen aus der Plugin-Konfiguration von Stash. Nach Änderungen die Seite aktualisieren oder `SideButtonSeek.reload()` aufrufen.

## Browser-Einschränkungen
Manche Chromium/Edge-Builds führen die Verlaufsnavigation auf Browser-Ebene aus und ignorieren `preventDefault()` für X1/X2. Falls die Seite trotzdem zurückspringt, die Seitentasten im Maustreiber (X-Mouse Button Control, Logitech G Hub, Razer Synapse, AutoHotkey) auf **← / →** legen; dann übernehmen die Stash-Shortcuts das Spulen.

Manche Treiber melden die Seitentasten als Tastatur-Eingabe oder Systembefehl, sodass button 3/4 die Seite nie erreichen. Auch hier hilft das Umbelegen im Treiber.

## Prüfen und Fehlersuche
Szene öffnen und eine Seitentaste drücken: Die Zeit springt etwa 10 Sekunden, eine kleine Einblendung erscheint. Ohne Maus in der Konsole `SideButtonSeek.simulate(4)` / `SideButtonSeek.simulate(3)` prüfen; `SideButtonSeek.settings` zeigt die Konfiguration, `SideButtonSeek.player` den VideoJS-Player.

## Funktionsweise
Stash bindet das UI-JavaScript des Plugins ein. Es lauscht in der Capture-Phase auf `pointerdown`, `mousedown`, `mouseup` und `auxclick`, akzeptiert nur `button === 3` / `4` innerhalb von `.video-js`, ruft `preventDefault()` und spult über `PluginApi.utils.InteractiveUtils.getPlayer()` → `videojs.getPlayers()` → das `<video>`-Element. Einstellungen kommen aus `{ configuration { plugins } }`.

## Lizenz
MIT — siehe [LICENSE](LICENSE).

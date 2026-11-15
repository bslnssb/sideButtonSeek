<p align="center" translate="no">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.zh-TW.md">繁體中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.ru.md">Русский</a> · <a href="README.de.md">Deutsch</a><br>
  <b>Español</b> · <a href="README.fr.md">Français</a> · <a href="README.pt.md">Português</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.th.md">ไทย</a> · <a href="README.el.md">Ελληνικά</a>
</p>

# Side Button Seek

**Usa los botones laterales del ratón (X1 = atrás, X2 = adelante) para avanzar o retroceder en el reproductor de Stash sin que el navegador cambie de página.**

Stash solo asigna la búsqueda a las flechas del teclado. En el navegador, los dos botones del pulgar son `MouseEvent.button` 3 y 4, que Chromium interpreta como atrás/adelante en el historial. Este plugin captura esos eventos sobre el reproductor VideoJS, cancela la navegación y mueve la posición de reproducción.

## Qué hace
- **X1** (botón trasero) → retroceder, **X2** (botón delantero) → avanzar.
- **10 segundos** por pulsación por defecto, configurable.
- Bloquea atrás/adelante mientras el puntero está sobre el reproductor.
- Funciona en pantalla completa, escenas, marcadores y colas.
- Aviso opcional en pantalla `+10s »` / `« −10s`.
- Por defecto solo actúa sobre el reproductor.

## Instalación
Añade este repositorio como fuente de plugins e instala el paquete:

```text
Name:       Side Button Seek
Source URL: https://raw.githubusercontent.com/bslnssb/sideButtonSeek/main/index.yml
Local Path: (leave empty)
```

1. Abre **Settings → Plugins → Available Plugins → Add Source**.
2. Pega la URL de abajo (deja *Local Path* vacío).
3. Despliega la fuente, marca **Side Button Seek** → **Install**.
4. Pulsa **Reload plugins** y recarga la página (**F5**).

### Instalación manual
Copia `sideButtonSeek.yml`, `sideButtonSeek.js` y `manifest` en `plugins/sideButtonSeek/` (junto al `config.yml` de Stash), recarga los plugins y actualiza la página.

## Ajustes

| Ajuste | Predeterminado | Descripción |
| --- | --- | --- |
| `seekSeconds` | 10 | Segundos que avanza cada pulsación. |
| `swapButtons` | false | Invierte la dirección de los dos botones. |
| `onlyInPlayer` | true | Solo actúa sobre el reproductor. |
| `showOsd` | true | Muestra `+10s` / `−10s` brevemente. |
| `preventNavigation` | true | `preventDefault()` evita que el navegador salga de la página. |
| `debug` | false | Registra eventos y resultados en la consola. |

Los ajustes se leen de la configuración de plugins de Stash. Tras cambiarlos, recarga la página o ejecuta `SideButtonSeek.reload()`.

## Limitaciones del navegador
Desde **v2.0.0** el plugin también cancela la navegación del historial a nivel de navegador mediante la Navigation API (Chrome/Edge 102+): se bloquea cualquier `traverse` inmediatamente posterior a pulsar un botón lateral. Si la entrada vecina del historial pertenece a otro documento, se inserta antes una entrada de guarda con la misma URL para que el salto sea cancelable; en ese caso un Atrás normal puede requerir un clic adicional. La guarda se crea solo al pulsar realmente el botón lateral, por lo que los equipos que han reasignado los botones a teclas no se ven afectados.

Algunos drivers envían los botones laterales como teclas o comandos del sistema, por lo que los eventos button 3/4 nunca llegan a la página. La misma reassignación lo resuelve.

## Verificación y solución de problemas
Abre una escena y pulsa un botón lateral: el tiempo salta unos 10 segundos y aparece un aviso. Sin ratón, ejecuta `SideButtonSeek.simulate(4)` / `SideButtonSeek.simulate(3)` en la consola; `SideButtonSeek.settings` muestra la configuración y `SideButtonSeek.player` el reproductor VideoJS.

## Cómo funciona
Stash inyecta el JavaScript de UI del plugin. Escucha `pointerdown`, `mousedown`, `mouseup` y `auxclick` en fase de captura, acepta solo `button === 3` / `4` dentro de `.video-js`, llama a `preventDefault()` y busca mediante `PluginApi.utils.InteractiveUtils.getPlayer()` → `videojs.getPlayers()` → el elemento `<video>`. Los ajustes vienen de `{ configuration { plugins } }`.

**How v2 blocks browser-level navigation (technical):** Chromium handles X1/X2 history traversal outside the page, so `preventDefault()` on mouse events has no effect. A `navigate` event with `navigationType === "traverse"` is `cancelable` only when its destination entry is same-document. On the first side-button press, if the neighbouring entry is cross-document, the plugin calls `history.pushState(state, "", location.href)` to insert a same-URL guard entry (which also truncates the forward stack). Its `navigate` listener then calls `preventDefault()` for traversals within a short window of a side-button press and consumes the guard after one cancellation, while ordinary Back/Forward clicks pass through unchanged. Run `SideButtonSeek.guard` in devtools to inspect guard counters and `navigation.entries()`.

## Licencia
MIT — consulta [LICENSE](LICENSE).

<p align="center" translate="no">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.zh-TW.md">繁體中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.ru.md">Русский</a> · <a href="README.de.md">Deutsch</a><br>
  <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a> · <b>Português</b> · <a href="README.tr.md">Türkçe</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.th.md">ไทย</a> · <a href="README.el.md">Ελληνικά</a>
</p>

# Side Button Seek

**Use os botões laterais do rato (X1 = voltar, X2 = avançar) para recuar ou avançar no player do Stash sem sair da página.**

O Stash associa a busca apenas às setas do teclado. No navegador, os dois botões do polegar são `MouseEvent.button` 3 e 4, que o Chromium interpreta como voltar/avançar no histórico. Este plugin captura esses eventos sobre o player VideoJS, cancela a navegação e move a posição de reprodução.

## O que faz
- **X1** (botão traseiro) → recuar, **X2** (botão dianteiro) → avançar.
- **10 segundos** por clique por omissão, configurável.
- Bloqueia voltar/avançar enquanto o ponteiro está sobre o player.
- Funciona em ecrã inteiro, cenas, marcadores e filas.
- Aviso opcional `+10s »` / `« −10s`.
- Por omissão só atua sobre o player.

## Instalação
Adicione este repositório como fonte de plugins e instale o pacote:

```text
Name:       Side Button Seek
Source URL: https://raw.githubusercontent.com/bslnssb/sideButtonSeek/main/index.yml
Local Path: (leave empty)
```

1. Abra **Settings → Plugins → Available Plugins → Add Source**.
2. Cole o URL abaixo (deixe *Local Path* vazio).
3. Expanda a fonte, marque **Side Button Seek** → **Install**.
4. Clique em **Reload plugins** e atualize a página (**F5**).

### Instalação manual
Copie `sideButtonSeek.yml`, `sideButtonSeek.js` e `manifest` para `plugins/sideButtonSeek/` (junto do `config.yml` do Stash), recarregue os plugins e atualize a página.

## Definições

| Definição | Padrão | Descrição |
| --- | --- | --- |
| `seekSeconds` | 10 | Segundos por cada clique. |
| `swapButtons` | false | Inverte a direção dos dois botões. |
| `onlyInPlayer` | true | Só reage sobre o player. |
| `showOsd` | true | Mostra `+10s` / `−10s` por instantes. |
| `showStepButton` | true | Mostra um botão ±Ns no player para alterar o passo. |
| `preventNavigation` | true | `preventDefault()` impede o navegador de sair da página. |
| `debug` | false | Regista eventos e resultados na consola. |

As definições vêm da configuração de plugins do Stash. Depois de alterar, atualize a página ou execute `SideButtonSeek.reload()`.

## Limitações do navegador
A partir da **v2.0.0** o plugin também cancela a navegação do histórico ao nível do navegador através da Navigation API (Chrome/Edge 102+): qualquer `traverse` logo após pressionar um botão lateral é bloqueado. Se a entrada vizinha do histórico pertencer a outro documento, é inserida primeiro uma entrada de guarda com o mesmo URL para tornar o salto cancelável; nesse caso um Voltar normal pode exigir um clique extra. A guarda só é criada ao pressionar realmente o botão lateral, pelo que os sistemas com os botões remapeados para teclas não são afetados.

Alguns drivers enviam os botões laterais como teclas ou comando do sistema, pelo que os eventos button 3/4 nunca chegam à página. O mesmo remapeamento resolve.

## Verificação e resolução de problemas
Abra uma cena e pressione um botão lateral: o tempo salta cerca de 10 segundos e aparece um pequeno aviso. Sem rato, execute `SideButtonSeek.simulate(4)` / `SideButtonSeek.simulate(3)` na consola; `SideButtonSeek.settings` mostra a configuração e `SideButtonSeek.player` o player VideoJS.

## Como funciona
O Stash injeta o JavaScript de UI do plugin. Ele escuta `pointerdown`, `mousedown`, `mouseup` e `auxclick` na fase de captura, aceita apenas `button === 3` / `4` dentro de `.video-js`, chama `preventDefault()` e faz a busca via `PluginApi.utils.InteractiveUtils.getPlayer()` → `videojs.getPlayers()` → o elemento `<video>`. As definições vêm de `{ configuration { plugins } }`.

**v2.1.0 in-player step button:** a small `±Ns` button sits at the right end of the VideoJS control bar (with a corner overlay as fallback). Click it to pick a preset (5 / 10 / 15 / 30 / 60 / 120 s) or type a custom value; **Save** writes it to Stash's plugin settings through `configurePlugin`, so the value persists across reloads and browsers and takes effect immediately. It is a normal flex child of the control bar (corner overlay only when no control bar exists) — it never touches React-owned nodes. Turn it off with `showStepButton`.

**How v2 blocks browser-level navigation (technical):** Chromium handles X1/X2 history traversal outside the page, so `preventDefault()` on mouse events has no effect. A `navigate` event with `navigationType === "traverse"` is `cancelable` only when its destination entry is same-document. On the first side-button press, if the neighbouring entry is cross-document, the plugin calls `history.pushState(state, "", location.href)` to insert a same-URL guard entry (which also truncates the forward stack). Its `navigate` listener then calls `preventDefault()` for traversals within a short window of a side-button press and consumes the guard after one cancellation, while ordinary Back/Forward clicks pass through unchanged. Run `SideButtonSeek.guard` in devtools to inspect guard counters and `navigation.entries()`.

## Licença
MIT — consulte [LICENSE](LICENSE).

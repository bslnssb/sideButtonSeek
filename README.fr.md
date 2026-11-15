<p align="center" translate="no">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.zh-TW.md">繁體中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.ru.md">Русский</a> · <a href="README.de.md">Deutsch</a><br>
  <a href="README.es.md">Español</a> · <b>Français</b> · <a href="README.pt.md">Português</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.th.md">ไทย</a> · <a href="README.el.md">Ελληνικά</a>
</p>

# Side Button Seek

**Utilisez les boutons latéraux de la souris (X1 = retour, X2 = avant) pour avancer ou reculer dans le lecteur Stash sans quitter la page.**

Stash ne lie la recherche qu'aux flèches du clavier. Dans le navigateur, les deux boutons du pouce correspondent à `MouseEvent.button` 3 et 4, que Chromium associe à l'historique précédent/suivant. Ce plugin intercepte ces événements au-dessus du lecteur VideoJS, annule la navigation et déplace la tête de lecture.

## Fonctions
- **X1** (bouton arrière) → reculer, **X2** (bouton avant) → avancer.
- **10 secondes** par clic par défaut, réglable.
- Bloque précédent/suivant tant que le pointeur est sur le lecteur.
- Fonctionne en plein écran, sur les scènes, les marqueurs et les files d'attente.
- Affichage optionnel `+10s »` / `« −10s`.
- Actif uniquement sur le lecteur par défaut.

## Installation
Ajoutez ce dépôt comme source de plugins puis installez le paquet :

```text
Name:       Side Button Seek
Source URL: https://raw.githubusercontent.com/bslnssb/sideButtonSeek/main/index.yml
Local Path: (leave empty)
```

1. Ouvrez **Settings → Plugins → Available Plugins → Add Source**.
2. Collez l'URL ci-dessous (laissez *Local Path* vide).
3. Dépliez la source, cochez **Side Button Seek** → **Install**.
4. Cliquez sur **Reload plugins** puis actualisez la page (**F5**).

### Installation manuelle
Copiez `sideButtonSeek.yml`, `sideButtonSeek.js` et `manifest` dans `plugins/sideButtonSeek/` (à côté du `config.yml` de Stash), rechargez les plugins et actualisez.

## Réglages

| Réglage | Défaut | Description |
| --- | --- | --- |
| `seekSeconds` | 10 | Secondes sautées à chaque clic. |
| `swapButtons` | false | Inverse le sens des deux boutons. |
| `onlyInPlayer` | true | N'agit que sur le lecteur. |
| `showOsd` | true | Affiche brièvement `+10s` / `−10s`. |
| `preventNavigation` | true | `preventDefault()` empêche le navigateur de quitter la page. |
| `debug` | false | Journalise les événements et résultats dans la console. |

Les réglages viennent de la configuration des plugins Stash. Après modification, actualisez la page ou lancez `SideButtonSeek.reload()`.

## Limites du navigateur
Depuis la **v2.0.0**, le plugin annule aussi la navigation au niveau du navigateur via la Navigation API (Chrome/Edge 102+) : tout `traverse` suivant immédiatement un appui sur un bouton latéral est bloqué. Si l'entrée d'historique voisine appartient à un autre document, une entrée de garde avec la même URL est insérée pour rendre le saut annulable — dans ce cas, un Retour normal peut demander un clic supplémentaire. La garde n'est créée qu'à l'appui réel sur le bouton latéral : les configurations qui remappent les boutons en touches clavier ne sont pas affectées.

Certains pilotes envoient les boutons latéraux comme touches clavier ou commande système : les événements button 3/4 n'atteignent jamais la page. Le même remappage résout le problème.

## Vérification et dépannage
Ouvrez une scène et appuyez sur un bouton latéral : le temps saute d'environ 10 secondes et un petit message apparaît. Sans souris, lancez `SideButtonSeek.simulate(4)` / `SideButtonSeek.simulate(3)` dans la console ; `SideButtonSeek.settings` affiche la configuration et `SideButtonSeek.player` le lecteur VideoJS.

## Fonctionnement
Stash injecte le JavaScript d'interface du plugin. Il écoute `pointerdown`, `mousedown`, `mouseup` et `auxclick` en phase de capture, n'accepte que `button === 3` / `4` dans `.video-js`, appelle `preventDefault()` puis effectue la recherche via `PluginApi.utils.InteractiveUtils.getPlayer()` → `videojs.getPlayers()` → l'élément `<video>`. Les réglages proviennent de `{ configuration { plugins } }`.

**How v2 blocks browser-level navigation (technical):** Chromium handles X1/X2 history traversal outside the page, so `preventDefault()` on mouse events has no effect. A `navigate` event with `navigationType === "traverse"` is `cancelable` only when its destination entry is same-document. On the first side-button press, if the neighbouring entry is cross-document, the plugin calls `history.pushState(state, "", location.href)` to insert a same-URL guard entry (which also truncates the forward stack). Its `navigate` listener then calls `preventDefault()` for traversals within a short window of a side-button press and consumes the guard after one cancellation, while ordinary Back/Forward clicks pass through unchanged. Run `SideButtonSeek.guard` in devtools to inspect guard counters and `navigation.entries()`.

## Licence
MIT — voir [LICENSE](LICENSE).

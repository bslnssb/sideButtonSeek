<p align="center" translate="no">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.zh-TW.md">繁體中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.ru.md">Русский</a> · <a href="README.de.md">Deutsch</a><br>
  <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a> · <a href="README.pt.md">Português</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.th.md">ไทย</a> · <b>Ελληνικά</b>
</p>

# Side Button Seek

**Χρησιμοποιήστε τα πλαϊνά πλήκτρα του ποντικιού (X1 = πίσω, X2 = εμπρός) για αναζήτηση στον player του Stash, χωρίς ο browser να φεύγει από τη σελίδα.**

Το Stash συνδέει την αναζήτηση μόνο με τα βέλη του πληκτρολογίου. Στον browser τα δύο πλήκτρα του αντίχειρα είναι `MouseEvent.button` 3 και 4, που το Chromium τα αντιστοιχίζει σε πίσω/εμπρός στο ιστορικό. Το plugin δεσμεύει αυτά τα γεγονότα πάνω από τον VideoJS player, ακυρώνει την πλοήγηση και μετακινεί τη θέση αναπαραγωγής.

## Τι κάνει
- **X1** (πίσω πλήκτρο) → προς τα πίσω, **X2** (εμπρός πλήκτρο) → προς τα εμπρός.
- Προεπιλογή **10 δευτερόλεπτα** ανά πάτημα, ρυθμίζεται.
- Μπλοκάρει πίσω/εμπρός όσο ο δείκτης είναι πάνω από τον player.
- Λειτουργεί σε πλήρη οθόνη, σκηνές, δείκτες και λίστες αναπαραγωγής.
- Προαιρετική ένδειξη `+10s »` / `« −10s`.
- Ενεργό μόνο πάνω από τον player εξ ορισμού.

## Εγκατάσταση
Προσθέστε αυτό το αποθετήριο ως πηγή plugin και εγκαταστήστε το πακέτο:

```text
Name:       Side Button Seek
Source URL: https://raw.githubusercontent.com/bslnssb/sideButtonSeek/main/index.yml
Local Path: (leave empty)
```

1. Ανοίξτε **Settings → Plugins → Available Plugins → Add Source**.
2. Επικολλήστε το URL παρακάτω (αφήστε το *Local Path* κενό).
3. Αναπτύξτε την πηγή, επιλέξτε **Side Button Seek** → **Install**.
4. Πατήστε **Reload plugins** και ανανεώστε τη σελίδα (**F5**).

### Χειροκίνητη εγκατάσταση
Αντιγράψτε τα `sideButtonSeek.yml`, `sideButtonSeek.js` και `manifest` στο `plugins/sideButtonSeek/` (δίπλα στο `config.yml` του Stash), φορτώστε ξανά τα plugins και ανανεώστε.

## Ρυθμίσεις

| Ρύθμιση | Προεπιλογή | Περιγραφή |
| --- | --- | --- |
| `seekSeconds` | 10 | Δευτερόλεπτα ανά πάτημα. |
| `swapButtons` | false | Αντιστρέφει την κατεύθυνση των δύο πλήκτρων. |
| `onlyInPlayer` | true | Αντιδρά μόνο πάνω από τον player. |
| `showOsd` | true | Εμφανίζει στιγμιαία `+10s` / `−10s`. |
| `preventNavigation` | true | Το `preventDefault()` κρατά τον browser στη σελίδα. |
| `debug` | false | Γράφει γεγονότα και αποτελέσματα στην κονσόλα. |

Οι ρυθμίσεις διαβάζονται από τη διαμόρφωση plugins του Stash. Μετά από αλλαγή, ανανεώστε ή καλέστε `SideButtonSeek.reload()`.

## Περιορισμοί browser
Από την **v2.0.0** το πρόσθετο ακυρώνει και την πλοήγηση ιστορικού στο επίπεδο του προγράμματος περιήγησης μέσω του Navigation API (Chrome/Edge 102+): κάθε `traverse` αμέσως μετά το πάτημα ενός πλευρικού κουμπιού μπλοκάρεται. Αν η γειτονική καταχώριση ιστορικού ανήκει σε άλλο έγγραφο, εισάγεται πρώτα μια καταχώριση φρουράς με το ίδιο URL ώστε η μετάβαση να μπορεί να ακυρωθεί· σε αυτή την περίπτωση ένα κανονικό Πίσω μπορεί να χρειαστεί ένα επιπλέον κλικ. Η φρουρά δημιουργείται μόνο όντως πατηθεί πλευρικό κουμπί, οπότε οι ρυθμίσεις με αντιστοίχιση σε πλήκτρα δεν επηρεάζονται.

Κάποια προγράμματα οδήγησης στέλνουν τα πλαϊνά πλήκτρα ως πλήκτρα πληκτρολογίου ή εντολή συστήματος, οπότε τα γεγονότα button 3/4 δεν φτάνουν ποτέ στη σελίδα. Η ίδια αντιστοίχιση το λύνει.

## Έλεγχος και αντιμετώπιση
Ανοίξτε μια σκηνή και πατήστε ένα πλαϊνό πλήκτρο: ο χρόνος μετακινείται περίπου 10 δευτερόλεπτα και εμφανίζεται μια μικρή ένδειξη. Χωρίς ποντίκι, εκτελέστε `SideButtonSeek.simulate(4)` / `SideButtonSeek.simulate(3)` στην κονσόλα· το `SideButtonSeek.settings` δείχνει τις ρυθμίσεις και το `SideButtonSeek.player` τον VideoJS player.

## Πώς λειτουργεί
Το Stash εισάγει το UI JavaScript του plugin. Ακούει `pointerdown`, `mousedown`, `mouseup` και `auxclick` στη φάση capture, δέχεται μόνο `button === 3` / `4` μέσα στο `.video-js`, καλεί `preventDefault()` και κάνει αναζήτηση μέσω `PluginApi.utils.InteractiveUtils.getPlayer()` → `videojs.getPlayers()` → το στοιχείο `<video>`. Οι ρυθμίσεις προέρχονται από `{ configuration { plugins } }`.

**How v2 blocks browser-level navigation (technical):** Chromium handles X1/X2 history traversal outside the page, so `preventDefault()` on mouse events has no effect. A `navigate` event with `navigationType === "traverse"` is `cancelable` only when its destination entry is same-document. On the first side-button press, if the neighbouring entry is cross-document, the plugin calls `history.pushState(state, "", location.href)` to insert a same-URL guard entry (which also truncates the forward stack). Its `navigate` listener then calls `preventDefault()` for traversals within a short window of a side-button press and consumes the guard after one cancellation, while ordinary Back/Forward clicks pass through unchanged. Run `SideButtonSeek.guard` in devtools to inspect guard counters and `navigation.entries()`.

## Άδεια
MIT — δείτε το [LICENSE](LICENSE).

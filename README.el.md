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
Ορισμένες εκδόσεις Chromium/Edge χειρίζονται την πλοήγηση σε επίπεδο browser και αγνοούν το `preventDefault()` για X1/X2. Αν η σελίδα εξακολουθεί να πηγαίνει πίσω, αντιστοιχίστε τα πλαϊνά πλήκτρα στα **← / →** στο πρόγραμμα οδήγησης του ποντικιού (X-Mouse Button Control, Logitech G Hub, Razer Synapse, AutoHotkey)· οι ενσωματωμένες συντομεύσεις του Stash θα κάνουν την αναζήτηση.

Κάποια προγράμματα οδήγησης στέλνουν τα πλαϊνά πλήκτρα ως πλήκτρα πληκτρολογίου ή εντολή συστήματος, οπότε τα γεγονότα button 3/4 δεν φτάνουν ποτέ στη σελίδα. Η ίδια αντιστοίχιση το λύνει.

## Έλεγχος και αντιμετώπιση
Ανοίξτε μια σκηνή και πατήστε ένα πλαϊνό πλήκτρο: ο χρόνος μετακινείται περίπου 10 δευτερόλεπτα και εμφανίζεται μια μικρή ένδειξη. Χωρίς ποντίκι, εκτελέστε `SideButtonSeek.simulate(4)` / `SideButtonSeek.simulate(3)` στην κονσόλα· το `SideButtonSeek.settings` δείχνει τις ρυθμίσεις και το `SideButtonSeek.player` τον VideoJS player.

## Πώς λειτουργεί
Το Stash εισάγει το UI JavaScript του plugin. Ακούει `pointerdown`, `mousedown`, `mouseup` και `auxclick` στη φάση capture, δέχεται μόνο `button === 3` / `4` μέσα στο `.video-js`, καλεί `preventDefault()` και κάνει αναζήτηση μέσω `PluginApi.utils.InteractiveUtils.getPlayer()` → `videojs.getPlayers()` → το στοιχείο `<video>`. Οι ρυθμίσεις προέρχονται από `{ configuration { plugins } }`.

## Άδεια
MIT — δείτε το [LICENSE](LICENSE).

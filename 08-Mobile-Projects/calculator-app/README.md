# Calcolatrice PWA 🧮

Una calcolatrice mobile-first Progressive Web App (PWA) con interfaccia moderna e touch-friendly.

## 🌟 Caratteristiche

- **Mobile-First Design**: Ottimizzata per dispositivi mobili con pulsanti touch-friendly
- **Progressive Web App**: Installabile su qualsiasi dispositivo (Android, iOS, Desktop)
- **Offline Function**: Funziona anche senza connessione internet
- **Operazioni Base**: Addizione, sottrazione, moltiplicazione, divisione
- **Funzioni Avanzate**: Percentuale, negazione, backspace
- **Supporto Tastiera**: Usa la tastiera fisica per input veloce
- **Feedback Aptico**: Vibrazione su dispositivi supportati
- **Dark Mode**: Supporto automatico per dark mode
- **Responsive**: Adattabile a qualsiasi dimensione dello schermo
- **Accessibile**: Supporto per screen reader e navigazione da tastiera

## 📱 Installazione

### Su Browser Mobile

1. Apri la calcolatrice nel browser (Chrome, Safari, Edge)
2. Cerca l'opzione "Aggiungi alla schermata Home" nel menu del browser
3. Conferma l'installazione

### Su Desktop

1. Apri la calcolatrice in Chrome o Edge
2. Clicca sull'icona di installazione nella barra degli indirizzi
3. Conferma l'installazione

### Distribuzione

Per distribuire l'app, puoi usare:

- **GitHub Pages**: Gratuito e facile da configurare
- **Netlify**: Deploy istantaneo con drag & drop
- **Vercel**: Ottimo per performance
- **Firebase Hosting**: Hosting gratuito di Google

## 🚀 Guida Rapida

### Operazioni Base

- **Numeri**: Tocca i numeri per inserirli
- **Operatori**: `+`, `−`, `×`, `÷`
- **Uguale**: `=` per calcolare il risultato
- **Cancella**: `C` per cancellare tutto
- **Backspace**: `⌫` per cancellare l'ultimo numero

### Funzioni Speciali

- **Percentuale**: `%` per calcolare la percentuale
- **Negazione**: `+/−` per cambiare il segno
- **Decimale**: `,` per inserire i decimali

### Tasti Rapidi (Tastiera)

| Tasto | Funzione |
|-------|----------|
| `0-9` | Numeri |
| `+` | Addizione |
| `-` | Sottrazione |
| `*` | Moltiplicazione |
| `/` | Divisione |
| `Enter` o `=` | Calcola risultato |
| `Backspace` | Cancella ultimo carattere |
| `Escape` o `C` | Cancella tutto |
| `%` | Percentuale |
| `.` | Decimale |

## 🛠️ Tecnologie Utilizzate

- **HTML5**: Struttura semantica
- **CSS3**: Design moderno con Grid e Flexbox
- **JavaScript (Vanilla)**: Logica della calcolatrice
- **Service Worker**: Funzionalità offline
- **Web App Manifest**: Configurazione PWA

## 📁 Struttura del Progetto

```
calculator-app/
├── index.html          # Pagina principale
├── styles.css          # Foglio di stile
├── app.js              # Logica JavaScript
├── manifest.json       # Configurazione PWA
├── sw.js               # Service Worker
├── icon-192.png        # Icona 192x192
├── icon-512.png        # Icona 512x512
└── README.md           # Documentazione
```

## 🎨 Personalizzazione

### Colori

I colori possono essere personalizzati modificando le variabili CSS in `styles.css`:

```css
:root {
    --bg-color: #000000;
    --calculator-bg: #1e1e1e;
    --operator-bg: #ff9f0a;
    --function-bg: #a5a5a5;
    /* ... */
}
```

### Icone

Per creare icone personalizzate:

1. Crea un'immagine quadrata (minimo 512x512px)
2. Usa strumenti come [favicon.io](https://favicon.io) o [RealFaviconGenerator](https://realfavicongenerator.net)
3. Genera le diverse dimensioni: 72, 96, 128, 144, 152, 192, 384, 512
4. Sostituisci i file `icon-*.png`

## 🔧 Sviluppo

### Prerequisiti

- Un browser moderno (Chrome, Firefox, Safari, Edge)
- Un server locale per testing (opzionale ma raccomandato)

### Testing Locale

Per testare l'app localmente con supporto PWA:

```bash
# Usa Python 3
python -m http.server 8000

# Usa Python 2
python -m SimpleHTTPServer 8000

# Usa Node.js con http-server
npx http-server -p 8000
```

Poi apri `http://localhost:8000` nel browser.

### Testing PWA

1. Apri DevTools (F12)
2. Vai al tab "Application"
3. Controlla:
   - **Manifest**: Verifica che il manifest sia valido
   - **Service Workers**: Verifica che il SW sia registrato
   - **Lighthouse**: Esegui un audit PWA

## 📊 Funzionalità PWA

### Service Worker

L'app include un Service Worker che:
- Cache della shell dell'applicazione
- Funzionalità offline
- Aggiornamento automatico delle risorse

### Manifest

Il manifest configurato per:
- Modalità standalone (simula un app nativa)
- Orientamento portrait
- Icone multiple per diverse risoluzioni
- Colori del tema

## 🌐 Compatibilità Browser

| Browser | Supporto | Note |
|---------|----------|------|
| Chrome | ✅ Full | Supporto PWA completo |
| Edge | ✅ Full | Supporto PWA completo |
| Firefox | ✅ Full | Supporto PWA completo |
| Safari | ⚠️ Partial | PWA supportato con limitazioni |
| Opera | ✅ Full | Supporto PWA completo |

## 📱 Supporto Mobile

| Piattaforma | Supporto | Installazione |
|-------------|----------|---------------|
| Android | ✅ | Chrome, Edge, Firefox |
| iOS | ⚠️ | Solo Safari (limitato) |
| Windows | ✅ | Chrome, Edge |
| macOS | ✅ | Chrome, Edge |

## 🤝 Contribuire

Contributi benvenuti! Sentiti libero di:

1. Fare fork del progetto
2. Creare un branch feature (`git checkout -b feature/AmazingFeature`)
3. Commit delle modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Aprire una Pull Request

## 📄 Licenza

Questo progetto è open source e disponibile sotto la Licenza MIT.

## 👤 Autore

Creato come progetto portfolio dimostrativo.

## 🙏 Riconoscimenti

- Design ispirato dalla calcolatrice iOS
- Icone create con font di sistema
- PWA best practices da [web.dev](https://web.dev/pwa/)

## 📞 Supporto

Per problemi o domande:
- Apri una issue su GitHub
- Contatta lo sviluppatore

---

**Nota**: Questa è una calcolatrice dimostrativa. Per calcoli critici, usa sempre una calcolatrice verificata e professionale.

Made with ❤️ in Italiano

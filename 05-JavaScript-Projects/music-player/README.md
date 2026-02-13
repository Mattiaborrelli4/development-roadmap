# 🎵 Music Player - Lettore Musicale

Un moderno player musicale sviluppato in puro JavaScript (ES6+) con HTML5 Audio API.

![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow?logo=javascript)
![HTML5](https://img.shields.io/badge/HTML5-Audio%20API-orange?logo=html5)
![CSS3](https://img.shields.io/badge/CSS3-Modern-blue?logo=css3)

## 📋 Caratteristiche

### Funzionalità Principali
- ✅ **Riproduzione/Pausa** - Controlli completi di riproduzione audio
- ✅ **Traccia Successiva/Precedente** - Navigazione tra i brani
- ✅ **Barra di Progresso** - Visualizzazione del tempo con seek interattivo
- ✅ **Controllo Volume** - Slider del volume con tasto mute
- ✅ **Info Traccia** - Visualizzazione titolo, artista e copertina
- ✅ **Gestione Playlist** - Playlist interattiva con brani campione
- ✅ **Shuffle** - Riproduzione casuale dei brani
- ✅ **Repeat** - Modalità repeat (nessuno, tutti, uno)
- ✅ **Controlli Tastiera** - Comandi da tastiera completi
- ✅ **Design Responsivo** - Adattamento a diversi schermi

## 🚀 Come Utilizzare

### Avvio Rapido
1. Apri il file `index.html` nel tuo browser
2. Il player si caricherà con una playlist di esempio
3. Clicca su un brano dalla playlist o premi il pulsante Play

### Controlli Mouse
- **Play/Pausa**: Clicca il pulsante centrale grande
- **Next/Prev**: Usa le frecce laterali
- **Shuffle**: Attiva la riproduzione casuale
- **Repeat**: Cicla tra nessuno/tutti/uno
- **Volume**: Clicca sulla barra del volume
- **Seek**: Clicca sulla barra di progresso
- **Mute**: Clicca l'icona del volume

### Controlli Tastiera
| Tasto | Azione |
|-------|--------|
| `Spazio` | Play/Pausa |
| `←` / `→` | Indietro/Avanti 5 secondi |
| `↑` / `↓` | Aumenta/Abbassa volume |
| `N` | Traccia successiva |
| `P` | Traccia precedente |
| `M` | Muto/Attiva audio |

## 📁 Struttura dei File

```
music-player/
│
├── index.html          # Interfaccia utente del player
├── style.css           # Stili moderni e animazioni
├── player.js           # Logica del player (Classi ES6+)
└── README.md           # Documentazione (questo file)
```

## 🛠️ Tecnologie Utilizzate

### HTML5
- **Audio API** - Gestione nativa dell'audio
- **Semantic Elements** - Struttura accessibile
- **Data Attributes** - Gestione stato UI

### CSS3
- **CSS Variables** - Tema personalizzabile
- **Flexbox** - Layout responsive
- **Animations** - Transizioni fluide
- **Custom Properties** - Design system
- **Gradients** - Effetti visivi moderni
- **Transforms** - Animazioni interattive

### JavaScript ES6+
- **Classes** - Architettura orientata agli oggetti
- **Arrow Functions** - Sintassi moderna
- **Template Literals** - Stringhe dinamiche
- **Array Methods** - map, forEach, filter
- **Destructuring** - Gestione stato
- **Event Listeners** - Gestione interazioni
- **State Management** - Stato centralizzato

## 🎨 Personalizzazione

### Cambiare la Playlist
Modifica l'array `playlist` nel file `player.js`:

```javascript
this.playlist = [
    {
        title: "Nome Traccia",
        artist: "Nome Artista",
        src: "url/audio.mp3",
        cover: "url/immagine.jpg",
        duration: "3:45"
    },
    // ... altre tracce
];
```

### Cambiare i Colori
Modifica le CSS variables in `style.css`:

```css
:root {
    --primary-color: #6c5ce7;
    --secondary-color: #a29bfe;
    --background: #0f0f23;
    --surface: #1a1a2e;
    --accent: #00cec9;
}
```

## 🔧 Funzionalità Tecniche

### Gestione dello Stato
Il player utilizza un oggetto `state` centralizzato:

```javascript
this.state = {
    isPlaying: false,
    currentTrackIndex: 0,
    isShuffle: false,
    repeatMode: 'none',
    isMuted: false,
    currentVolume: 0.8
};
```

### Eventi Audio
- `timeupdate` - Aggiornamento progresso
- `loadedmetadata` - Caricamento durata
- `ended` - Fine traccia
- `play` - Inizio riproduzione
- `pause` - Pausa

### Metodi Principali
- `loadTrack(index)` - Carica una traccia
- `play()` - Avvia la riproduzione
- `pause()` - Mette in pausa
- `nextTrack()` - Traccia successiva
- `prevTrack()` - Traccia precedente
- `seek(event)` - Seek nella traccia
- `setVolume(event)` - Imposta volume
- `toggleShuffle()` - Attiva/disattiva shuffle
- `toggleRepeat()` - Cicla modalità repeat

## 🌐 Browser Support

Questo progetto funziona su tutti i browser moderni che supportano:
- ES6+ (Classes, Arrow Functions, Template Literals)
- HTML5 Audio API
- CSS3 (Flexbox, Animations, Variables)

Browser consigliati:
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## 📱 Responsive Design

Il player si adatta automaticamente a:
- Desktop (1920px+)
- Tablet (768px - 1024px)
- Mobile (320px - 767px)

## 🎯 Concetti Chiave Appresi

### JavaScript
- **Programmazione a Oggetti** - Classi e istanze
- **Gestione Eventi** - Event listeners e handlers
- **Manipolazione DOM** - Creazione e modifica elementi
- **Audio API** - Controllo avanzato dell'audio
- **State Management** - Pattern di gestione stato
- **ES6+ Features** - Sintassi moderna JavaScript

### CSS
- **Layout Moderno** - Flexbox e positioning
- **Animazioni** - Keyframes e transitions
- **Design System** - CSS variables
- **Responsive Design** - Media queries
- **Custom UI** - Scrollbar e slider personalizzati

### HTML
- **Audio Element** - Tag audio HTML5
- **Semantica** - Struttura corretta
- **Accessibility** - Attributi ARIA
- **Data Attributes** - Metadati custom

## 📚 Risorse Utili

- [HTML5 Audio API - MDN](https://developer.mozilla.org/it/docs/Web/API/HTMLAudioElement)
- [JavaScript ES6+ - MDN](https://developer.mozilla.org/it/docs/Web/JavaScript)
- [CSS Flexbox - MDN](https://developer.mozilla.org/it/docs/Web/CSS/CSS_Flexible_Box_Layout)

## 🤝 Contribuire

Sentiti libero di clonare questo progetto e personalizzarlo:
1. Fork del progetto
2. Crea un branch feature (`git checkout -b feature/AmazingFeature`)
3. Commit delle modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)

## 📝 Licenza

Questo progetto è libero da utilizzare per scopi educativi e personali.

## 👨‍💻 Sviluppatore

Progetto realizzato come parte di un portfolio di progetti JavaScript.

---

**Nota**: I brani musicali inclusi sono file di esempio gratuiti da SoundHelix.com. Per un progetto di produzione, sostituiscili con i tuoi file audio locali o streaming services legali.

**Goditi la musica! 🎵**

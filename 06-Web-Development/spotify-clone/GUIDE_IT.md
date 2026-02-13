# Spotify Clone - Guida Completa

## 🎵 Panoramica del Progetto

Questo è un clone frontend di Spotify, realizzato interamente con React. Il progetto dimostra competenze avanzate nello sviluppo di applicazioni web moderne, inclusa la gestione dello stato, il routing, e la creazione di interfacce utente complesse e responsive.

## 🚀 Guida Rapida all'Avvio

### 1. Installazione

Apri il terminale nella cartella del progetto:

```bash
cd spotify-clone
npm install
```

### 2. Avvio in Sviluppo

```bash
npm run dev
```

L'applicazione si aprirà automaticamente nel browser all'indirizzo `http://localhost:3000`

### 3. Build per Produzione

```bash
npm run build
```

I file ottimizzati saranno nella cartella `dist/`

## 📁 Struttura del Progetto

```
spotify-clone/
│
├── public/
│   └── index.html                 # Template HTML principale
│
├── src/
│   │
│   ├── components/                # Componenti Riutilizzabili
│   │   ├── Player.jsx            # Lettore musicale con controlli
│   │   ├── Sidebar.jsx           # Barra laterale di navigazione
│   │   ├── TrackList.jsx         # Componente lista tracce
│   │   ├── Playlist.jsx          # Card per visualizzare playlist
│   │   └── SearchBar.jsx         # Barra di ricerca
│   │
│   ├── contexts/
│   │   └── MusicContext.jsx       # Context API per stato globale
│   │
│   ├── pages/                     # Pagine dell'Applicazione
│   │   ├── Home.jsx              # Homepage con raccomandazioni
│   │   ├── Search.jsx            # Pagina di ricerca
│   │   ├── Library.jsx           # Libreria personale
│   │   ├── PlaylistDetail.jsx    # Dettagli singola playlist
│   │   └── Liked.jsx             # Brani piaciuti
│   │
│   ├── App.jsx                    # Componente principale con routing
│   ├── App.css                    # Stili globali (tema Spotify)
│   ├── data.js                    # Dati di esempio
│   └── index.js                   # Entry point dell'applicazione
│
├── package.json                   # Dipendenze e script npm
├── vite.config.js                # Configurazione Vite
├── .gitignore                     # File ignorati da Git
└── README.md                      # Documentazione inglese
```

## 🎯 Funzionalità Principali

### 1. Player Musicale

#### Controlli Disponibili:
- **Play/Pausa**: Avvia o mette in pausa la riproduzione
- **Precedente/Successivo**: Naviga tra le tracce
- **Barra di Progresso**: Mostra e permette di modificare la posizione
- **Volume**: Slider per regolare il volume
- **Mute**: Disattiva/riattiva l'audio
- **Shuffle**: Attiva riproduzione casuale
- **Repeat**: Cicla tra Off, Repeat All, Repeat One
- **Like**: Aggiunge/rimuove traccia dai preferiti

#### Implementazione Tecnica:
```javascript
// Il player usa il Context API per gestire lo stato globale
const {
  currentTrack,
  isPlaying,
  volume,
  progress,
  togglePlay,
  nextTrack,
  prevTrack
} = useMusic();
```

### 2. Navigazione

#### Rotte Implementate:
- `/` - Home con playlist consigliate
- `/search` - Pagina di ricerca
- `/library` - Libreria personale
- `/playlist/:id` - Dettagli playlist
- `/liked` - Brani piaciuti

#### React Router:
```javascript
<BrowserRouter>
  <Routes>
    <Route path="/" element={<Home />} />
    <Route path="/search" element={<Search />} />
    {/* ... altre routes */}
  </Routes>
</BrowserRouter>
```

### 3. Gestione Stato

#### MusicContext (Context API):
```javascript
// Stato gestito globalmente
- currentTrack: Brano in riproduzione
- isPlaying: Stato play/pausa
- playlist: Playlist corrente
- volume: Livello volume
- progress: Progresso riproduzione
- shuffle: Modalità casuale
- repeat: Modalità ripetizione
- likedTracks: Tracce preferite
- userPlaylists: Playlist utente
```

### 4. Gestione Playlist

#### Funzionalità:
- **Crea Playlist**: Modal per creare nuove playlist
- **Visualizza Playlist**: Griglia con copertine
- **Dettagli Playlist**: Lista tracce completa
- **Elimina Playlist**: Rimozione playlist personalizzate
- **Navigazione**: Routing dinamico con ID

## 🎨 Design System

### Colori Tema

```css
--bg-black: #000000          /* Sfondo principale */
--bg-dark: #121212          /* Sfondo secondario */
--bg-elevated: #181818       /* Sfondo elementi elevati */
--bg-light: #282828          /* Sfondo hover */
--text-primary: #FFFFFF      /* Testo principale */
--text-secondary: #B3B3B3    /* Testo secondario */
--spotify-green: #1DB954     /* Accent color */
```

### Componenti UI

#### Card Playlist:
- Immagine con effetto hover
- Pulsante play overlay
- Titolo e descrizione
- Sfondo arrotondato

#### Track Item:
- Numero di traccia (animato quando suona)
- Immagine album
- Titolo e artista
- Album e durata
- Pulsante preferito

#### Sidebar:
- Logo Spotify
- Navigazione principale
- Sezione playlist
- Scroll indipendente

## 📱 Responsive Design

### Breakpoints:
- **Desktop** (>1024px): Layout completo
- **Tablet** (768-1024px): Sidebar ridotta
- **Mobile** (<768px): Sidebar hidden, layout ottimizzato

### Adattamenti:
- Nascondi colonne non essenziali
- Riduci dimensioni card
- Ottimizza controlli player
- Menu hamburger per mobile

## 🔧 Tecnologìe Utilizzate

### Core:
- **React 18.2**: Framework UI con Hooks
- **React Router 6**: Routing lato client
- **React Icons**: Libreria icone

### Build Tool:
- **Vite 5**: Build rapido e HMR

### Stili:
- **CSS puro**: Con CSS custom properties
- **CSS Modules**: Organizzazione modulare
- **Responsive**: Media queries

### Pattern:
- **Context API**: Gestione stato globale
- **useReducer**: Stato complesso
- **Custom Hooks**: Logica riutilizzabile
- **Composition**: Componenti composti

## 💡 Pattern di Sviluppo

### 1. Functional Components
```javascript
const Component = ({ prop1, prop2 }) => {
  const [state, setState] = useState(initialValue);
  const { contextValue } = useMusic();

  useEffect(() => {
    // Effect logic
  }, [dependencies]);

  return <div>...</div>;
};
```

### 2. Context Provider
```javascript
<MusicProvider>
  <App />
</MusicProvider>
```

### 3. Custom Hook
```javascript
const useMusic = () => {
  const context = useContext(MusicContext);
  if (!context) {
    throw new Error('useMusic must be used within MusicProvider');
  }
  return context;
};
```

## 🎯 Caratteristiche Tecniche

### Gestione Audio:
La progress bar simula la riproduzione audio con un timer che aggiorna lo stato del progresso ogni 500ms.

### Ricerca:
Filtraggio real-time di tracce, playlist e artisti basato sulla query di ricerca.

### Animazioni:
- CSS transitions per hover states
- Transform per scale effects
- Opacity transitions per overlays

### Performance:
- React.memo per ottimizzazione (futuro)
- Lazy loading per code splitting (futuro)
- Virtual scrolling per liste lunghe (futuro)

## 🧪 Testing

### Test da Implementare:
- Unit tests per componenti
- Integration tests per routing
- E2E tests con Playwright/Cypress
- Snapshot tests per UI

## 🚀 Deployment

### Vercel:
```bash
npm run build
vercel --prod
```

### Netlify:
```bash
npm run build
netlify deploy --prod --dir=dist
```

### GitHub Pages:
1. Build del progetto
2. Push su branch gh-pages
3. Configura GitHub Pages

## 🔮 Miglioramenti Futuri

### Backlog:
- [ ] Autenticazione Spotify
- [ ] API Spotify Web Playback
- [ ] Persistenza stato localStorage
- [ ] PWA con service worker
- [ ] Download offline
- [ ] Visualizzatore audio
- [ ] Testi sincronizzati
- [ ] Condivisione social
- [ ] Playlist collaborative
- [ ] Equalizzatore

### Technical Debt:
- [ ] TypeScript migration
- [ ] Unit testing
- [ ] E2E testing
- [ ] CI/CD pipeline
- [ ] Error boundaries
- [ ] Performance monitoring

## 📚 Risorse Utili

### Documentazione:
- [React Docs](https://react.dev)
- [React Router](https://reactrouter.com)
- [Vite](https://vitejs.dev)

### Design:
- [Spotify Design](https://spotify.design)
- [Spotify Color Palette](https://www.spotify.com/it/design/)
- [React Icons](https://react-icons.github.io/react-icons)

### Tutorial:
- [React Hooks Guide](https://react-hooks.org)
- [Context API Tutorial](https://react.dev/reference/react/useContext)

## 🐛 Troubleshooting

### Problemi Comuni:

#### Node modules non installati:
```bash
rm -rf node_modules package-lock.json
npm install
```

#### Porta 3000 occupata:
Modifica `vite.config.js`:
```javascript
server: {
  port: 3001 // o altra porta
}
```

#### Build errors:
```bash
npm cache clean --force
npm install
npm run build
```

## 📝 Note per lo Sviluppatore

Questo progetto è stato creato come parte di un portfolio personale per dimostrare:

1. **Competenze React**: Hooks, Context, Router
2. **UI/UX Design**: Design system, responsive
3. **State Management**: Pattern avanzati
4. **Best Practices**: Clean code, organizzazione
5. **Problem Solving**: Gestione stato complesso

### Struttura Componenti:
- Atomic design pattern
- Separazione concerns
- Riutilizzabilità
- Performance optimization

### Code Style:
- Functional components
- Destructuring props
- Arrow functions
- Template literals

---

**Autore**: Matteo
**Anno**: 2024
**Stack**: React, Vite, CSS Modules
**Status**: Completo (v1.0)

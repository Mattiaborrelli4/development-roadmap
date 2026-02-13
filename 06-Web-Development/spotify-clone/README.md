# 🎵 Spotify Clone - Frontend React

Un clone dell'interfaccia di Spotify realizzato con React, che offre un'esperienza utente simile a quella dell'applicazione originale.

## 📋 Caratteristiche

### Funzionalità Implementate

#### 🎮 Player Musicale
- Controlli di riproduzione (Play/Pausa, Precedente, Successivo)
- Barra di avanzamento interattiva
- Controllo volume con slider
- Modalità Shuffle (riproduzione casuale)
- Modalità Repeat (Off, All, One)
- Visualizzazione del brano corrente con copertina album

#### 📱 Navigazione
- **Home**: Dashboard con playlist consigliate, artisti popolari e brani in evidenza
- **Cerca**: Funzionalità di ricerca con filtri per brani, playlist e artisti
- **Libreria**: Visualizzazione delle playlist personali e artisti seguiti
- **Brani Piaciuti**: Raccolta dei brani preferiti

#### 📋 Gestione Playlist
- Visualizzazione playlist con copertine e descrizioni
- Creazione di nuove playlist tramite modal
- Eliminazione playlist personalizzate
- Visualizzazione dettagliata della playlist con lista tracce

#### 🎨 Interfaccia Utente
- Design fedele a Spotify con tema scuro
- Layout responsive per dispositivi mobile e desktop
- Animazioni fluide e transizioni
- Hover effects su card e tracce
- Griglia adattiva per playlist e artisti
- Typography e colori in stile Spotify

#### 🎯 Gestione Stato
- Context API per state management globale
- Gestione stato riproduzione musicale
- Gestione stato preferiti
- Gestione playlist personalizzate

## 🛠️ Tecnologie Utilizzate

- **React 18.2** - Framework JavaScript con Hooks
- **React Router 6** - Routing lato client
- **React Icons** - Icone vettoriali
- **Vite** - Build tool e dev server
- **CSS Modules** - Stili scoped

## 📦 Installazione

### Prerequisiti
- Node.js (versione 16 o superiore)
- npm o yarn

### Passi di Installazione

1. **Clona il repository**
   ```bash
   git clone <repository-url>
   cd spotify-clone
   ```

2. **Installa le dipendenze**
   ```bash
   npm install
   ```

3. **Avvia l'applicazione in modalità sviluppo**
   ```bash
   npm run dev
   ```

4. **Apri il browser**
   L'applicazione sarà disponibile su `http://localhost:3000`

## 🏗️ Struttura del Progetto

```
spotify-clone/
├── public/
│   └── index.html              # Template HTML
├── src/
│   ├── components/             # Componenti React riutilizzabili
│   │   ├── Player.jsx          # Lettore musicale
│   │   ├── Sidebar.jsx         # Barra laterale di navigazione
│   │   ├── TrackList.jsx       # Lista tracce
│   │   ├── Playlist.jsx        # Card playlist
│   │   └── SearchBar.jsx       # Barra di ricerca
│   ├── contexts/
│   │   └── MusicContext.jsx    # Context per la gestione della musica
│   ├── pages/                   # Pagine dell'applicazione
│   │   ├── Home.jsx            # Homepage
│   │   ├── Search.jsx          # Pagina di ricerca
│   │   ├── Library.jsx         # Libreria personale
│   │   ├── PlaylistDetail.jsx  # Dettagli playlist
│   │   └── Liked.jsx           # Brani piaciuti
│   ├── App.jsx                 # Componente principale
│   ├── App.css                 # Stili globali
│   ├── data.js                 # Dati di esempio
│   └── index.js                # Entry point
├── package.json                # Dipendenze e script
├── vite.config.js             # Configurazione Vite
└── README.md                  # Documentazione
```

## 🎯 Utilizzo

### Navigazione

- **Home**: Visualizza playlist consigliate, artisti popolari e brani
- **Cerca**: Usa la barra per trovare brani, playlist o artisti
- **Libreria**: Accedi alle tue playlist e agli artisti seguiti

### Player Musicale

- **Play/Pausa**: Clicca il pulsante play o su una traccia
- **Brano precedente/successivo**: Usa le frecce nel player
- **Volume**: Trascina lo slider del volume
- **Shuffle**: Attiva la riproduzione casuale
- **Repeat**: Cicla tra Off, Repeat All, Repeat One
- **Preferiti**: Clicca il cuore per aggiungere ai piaciuti

### Gestione Playlist

1. **Crea Playlist**:
   - Clicca su "Crea Playlist" nella sidebar
   - Inserisci nome e descrizione
   - Conferma la creazione

2. **Visualizza Playlist**:
   - Clicca su una card playlist per vederne i dettagli
   - Riproduci direttamente dalla lista tracce

3. **Elimina Playlist**:
   - Apri i dettagli della playlist
   - Clicca "Elimina" (solo playlist personalizzate)

## 🎨 Personalizzazione

### Colori Tema

I colori principali sono definiti in `App.css`:

```css
:root {
  --bg-black: #000000;
  --bg-dark: #121212;
  --bg-elevated: #181818;
  --bg-light: #282828;
  --text-primary: #FFFFFF;
  --text-secondary: #B3B3B3;
  --spotify-green: #1DB954;
}
```

### Dati di Esempio

I dati sono contenuti in `src/data.js`. Puoi modificare:

- `playlists`: Array di playlist
- `tracks`: Array di tracce musicali
- `artists`: Array di artisti
- `albums`: Array di album

## 🚀 Deployment

### Build di Produzione

```bash
npm run build
```

I file compilati saranno nella cartella `dist/`.

### Preview della Build

```bash
npm run preview
```

### Deployment su Vercel/Netlify

1. Esegui il build: `npm run build`
2. Carica la cartella `dist/` sulla tua piattaforma preferita
3. Configura le reindirizzamenti per SPA (Single Page Application)

## 🔮 Possibili Miglioramenti

### Funzionalità Aggiuntive

- [ ] Integrazione con Spotify Web API
- [ ] Autenticazione OAuth 2.0
- [ ] Coda di riproduzione
- [ ] Drag & drop per ordinare le playlist
- [ ] Modalità offline
- [ ] Download brani
- [ ] Visualizzazioni audio
- [ ] Testi delle canzoni
- [ ] Condivisione playlist

### Miglioramenti Tecnici

- [ ] Persistenza stato con localStorage
- [ ] Ottimizzazione performance con React.memo
- [ ] Lazy loading delle pagine
- [ ] Virtual scrolling per liste lunghe
- [ ] PWA con service workers
- [ ] Testing con Jest e React Testing Library
- [ ] TypeScript per type safety

## 📱 Responsive Design

L'applicazione è completamente responsive:

- **Desktop** (>1024px): Sidebar espansa, layout completo
- **Tablet** (768px-1024px): Sidebar ridotta
- **Mobile** (<768px): Sidebar collassata, layout ottimizzato

## 🤝 Contribuire

Questo è un progetto educativo. Sentiti libero di:

1. Fare fork del progetto
2. Creare un branch per le tue feature
3. Fare commit delle tue modifiche
4. Fare push al branch
5. Aprire una Pull Request

## 📄 Licenza

Questo progetto è a scopo educativo. Il design e il logo sono proprietà di Spotify.

## 👨‍💻 Autore

Creato come progetto di portfolio per dimostrare competenze in:

- React Hooks (useState, useEffect, useContext, useReducer)
- React Router
- Context API
- CSS Modulare
- Gestione stato complessa
- UI/UX Design

## 🙏 Ringraziamenti

- Design ispirato a Spotify
- Icone da React Icons
- Immagini placeholder da Picsum
- Avatar placeholder da Pravatar

---

**Nota**: Questo è un clone a scopo educativo. Non è affiliato con Spotify AB.

# 🚀 Guida Rapida - Spotify Clone

## Avvio Rapido (Quick Start)

### 1. Installazione
```bash
cd spotify-clone
npm install
```

### 2. Avvio Sviluppo
```bash
npm run dev
```
Apri: http://localhost:3000

### 3. Build Produzione
```bash
npm run build
```

## 📁 File Importanti

| File | Descrizione |
|------|-------------|
| `src/App.jsx` | Entry point con routing |
| `src/App.css` | Stili globali |
| `src/contexts/MusicContext.jsx` | Gestione stato globale |
| `src/data.js` | Dati di esempio |
| `src/components/` | Componenti riutilizzabili |
| `src/pages/` | Pagine dell'app |

## 🎯 Componenti Principali

### Components
- **Player.jsx** - Lettore musicale
- **Sidebar.jsx** - Navigazione
- **TrackList.jsx** - Lista tracce
- **Playlist.jsx** - Card playlist
- **SearchBar.jsx** - Barra ricerca

### Pages
- **Home.jsx** - Homepage
- **Search.jsx** - Ricerca
- **Library.jsx** - Libreria
- **PlaylistDetail.jsx** - Dettagli playlist
- **Liked.jsx** - Preferiti

## 🎨 Tema Colori

```css
--bg-black: #000000
--bg-dark: #121212
--spotify-green: #1DB954
--text-primary: #FFFFFF
```

## 🔧 Script Disponibili

```bash
npm run dev     # Modalità sviluppo
npm run build   # Build produzione
npm run preview # Preview build
```

## 📱 Responsive

- Desktop: >1024px
- Tablet: 768-1024px
- Mobile: <768px

## 📚 Documentazione

- `README.md` - Documentazione completa (EN)
- `GUIDE_IT.md` - Guida dettagliata (IT)
- `FEATURES.md` - Elenco funzionalità

## 🐛 Troubleshooting

### Porta occupata
Cambia porta in `vite.config.js`:
```js
server: { port: 3001 }
```

### Reinstallare tutto
```bash
rm -rf node_modules
npm install
```

### Build errors
```bash
npm cache clean --force
npm install
```

## 🎯 Come Contribuire

1. Fork il progetto
2. Crea branch feature
3. Commit changes
4. Push al branch
5. Crea Pull Request

## 📝 Note

- Progetto educativo
- Non affiliato con Spotify
- Dati di esempio inclusi
- Funziona senza API keys

## 🚀 Next Steps

1. Esplora il codice
2. Modifica i dati in `data.js`
3. Personalizza i colori in `App.css`
4. Aggiungi nuove funzionalità
5. Deploy su Vercel/Netlify

---

**Versione**: 1.0.0 | **Stack**: React + Vite | **Anno**: 2024

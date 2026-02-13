# Photo Gallery App

Un'applicazione mobile React Native per gestire, organizzare e modificare foto con filtri e album.

## Caratteristiche

### Funzionalità Principali
- 📸 **Scatta Foto**: Usa la fotocamera del dispositivo per scattare nuove foto
- 🖼️ **Importa Foto**: Seleziona foto dalla galleria del dispositivo
- 📁 **Album**: Organizza le foto in album personalizzati
- 🎨 **Filtri**: Applica filtri alle tue foto (Bianco e Nero, Seppia, Vintage, ecc.)
- 📤 **Condivisione**: Condividi le foto tramite la condivisione nativa
- 🗑️ **Eliminazione**: Rimuovi foto singole o multiple
- 🔍 **Visualizzazione**: Vista griglia con 2 o 3 colonne
- ℹ️ **Dettagli**: Visualizza informazioni dettagliate sulle foto

### Filtri Disponibili
- Originale (nessun filtro)
- Bianco e Nero
- Seppia
- Vintage
- Caldo
- Freddo
- Drammatico
- Sfocato

### Gestione Album
- Crea nuovi album
- Rinomina album
- Elimina album
- Aggiungi foto agli album
- Sposta foto tra album
- Visualizza copertina album

## Tecnologie Utilizzate

### Framework & Librerie
- **React Native** ^0.76.5 - Framework mobile
- **Expo SDK 52** - Piattaforma di sviluppo
- **Expo Image Picker** - Selezione foto e fotocamera
- **Expo Camera** - Accesso alla fotocamera
- **Expo Media Library** - Accesso alla galleria
- **Expo Sharing** - Condivisione nativa
- **Expo File System** - Gestione file
- **React Navigation** - Navigazione tra schermate
- **React Native Reanimated** - Animazioni fluide
- **Async Storage** - Persistenza dati locale

### Struttura del Progetto

```
photo-gallery/
├── App.js                      # Entry point dell'applicazione
├── app.json                    # Configurazione Expo
├── package.json                # Dipendenze
└── src/
    ├── components/             # Componenti riutilizzabili
    │   ├── PhotoGrid.jsx      # Griglia di foto
    │   ├── PhotoItem.jsx      # Singola foto
    │   ├── AlbumCard.jsx      # Card album
    │   ├── FilterSelector.jsx # Selettore filtri
    │   └── PhotoView.jsx      # Modal visualizzazione foto
    ├── screens/                # Schermate dell'app
    │   ├── GalleryScreen.jsx       # Galleria principale
    │   ├── AlbumDetailScreen.jsx   # Dettagli album
    │   ├── CameraScreen.jsx        # Fotocamera
    │   └── SettingsScreen.jsx      # Impostazioni
    ├── services/               # Logica di business
    │   ├── photoService.js    # Gestione foto
    │   ├── albumService.js    # Gestione album
    │   ├── filterService.js   # Gestione filtri
    │   └── storageService.js  # Persistenza dati
    ├── hooks/                  # Custom React Hooks
    │   ├── usePhotos.js       # Hook per foto
    │   └── useAlbums.js       # Hook per album
    ├── utils/                  # Utilità
    │   ├── filters.js         # Configurazione filtri
    │   └── helpers.js         # Funzioni helper
    └── styles/                 # Tema e stili
        └── theme.js           # Configurazione tema
```

## Installazione

### Prerequisiti
- Node.js (v18 o superiore)
- npm o yarn
- Expo CLI
- Dispositivo mobile o emulatore (iOS/Android)

### Passi di Installazione

1. **Clona o naviga nella directory del progetto**
   ```bash
   cd photo-gallery
   ```

2. **Installa le dipendenze**
   ```bash
   npm install
   ```

3. **Avvia il development server**
   ```bash
   npm start
   ```

4. **Esegui l'app**
   - Premi `a` per Android
   - Premi `i` per iOS
   - Scansiona il codice QR con l'app Expo Go sul tuo telefono

## Struttura Dati

### Photo
```javascript
{
  id: string,              // Identificatore univoco
  uri: string,             // URI dell'immagine
  width: number,           // Larghezza in pixel
  height: number,          // Altezza in pixel
  size: number,            // Dimensione in bytes
  createdAt: timestamp,    // Data di creazione
  filter: string,          // Filtro applicato
  albumId: string | null   // Album di appartenenza
}
```

### Album
```javascript
{
  id: string,              // Identificatore univoco
  name: string,            // Nome dell'album
  coverPhoto: string,      // URI foto di copertina
  count: number,           // Numero di foto
  createdAt: timestamp     // Data di creazione
}
```

## Funzionalità per Schermata

### GalleryScreen (Schermata Principale)
- Visualizzazione griglia/lista foto
- Creazione album
- Aggiunta foto (fotocamera/galleria)
- Selezione multipla
- Eliminazione multipla
- Sposta foto in album
- Cambio layout griglia

### AlbumDetailScreen (Dettagli Album)
- Visualizzazione foto album
- Rinomina album
- Elimina album
- Aggiungi foto all'album
- Rimuovi foto dall'album
- Applica filtri

### CameraScreen (Fotocamera)
- Scatta foto
- Controllo flash
- Cambio fotocamera (anteriore/posteriore)
- Salvataggio automatico

### SettingsScreen (Impostazioni)
- Statistiche dell'app
- Modalità visualizzazione
- Ordinamento foto
- Configurazione filtri
- Cancella tutti i dati

## Permessi Richiesti

### iOS
- `NSCameraUsageDescription`: Accesso alla fotocamera per scattare foto
- `NSPhotoLibraryUsageDescription`: Accesso alla galleria per selezionare foto
- `NSPhotoLibraryAddUsageDescription`: Salvataggio foto nella galleria

### Android
- `CAMERA`: Accesso alla fotocamera
- `READ_EXTERNAL_STORAGE`: Lettura foto dalla galleria
- `WRITE_EXTERNAL_STORAGE`: Salvataggio foto
- `READ_MEDIA_IMAGES`: Accesso ai media (Android 13+)

## Custom Hooks

### usePhotos(albumId?)
Hook per gestire le foto con operazioni CRUD complete.

```javascript
const {
  photos,           // Array di foto
  loading,         // Stato di caricamento
  error,           // Eventuali errori
  refresh,         // Ricarica foto
  addPhoto,        // Aggiunge una foto
  addPhotos,       // Aggiunge più foto
  deletePhoto,     // Elimina una foto
  deletePhotos,    // Elimina più foto
  applyFilter,     // Applica filtro
  moveToAlbum,     // Sposta in album
  sharePhoto,      // Condividi foto
  sortPhotos,      // Ordina foto
} = usePhotos(albumId);
```

### useAlbums()
Hook per gestire gli album con operazioni complete.

```javascript
const {
  albums,              // Array di album
  loading,            // Stato di caricamento
  error,              // Eventuali errori
  refresh,            // Ricarica album
  createAlbum,        // Crea album
  updateAlbum,        // Aggiorna album
  renameAlbum,        // Rinomina album
  updateCover,        // Aggiorna copertina
  deleteAlbum,        // Elimina album
  addPhotosToAlbum,   // Aggiunge foto a album
  removePhotosFromAlbum, // Rimuove foto da album
  getStats,           // Ottieni statistiche
} = useAlbums();
```

## Tema e Stili

L'app utilizza un sistema di tema centralizzato in `src/styles/theme.js`:

```javascript
import { Colors, Spacing, Typography, BorderRadius, Shadows } from './styles/theme';

// Colori principali
Colors.primary        // Colore primario (#6366f1)
Colors.secondary      // Colore secondario (#ec4899)
Colors.background     // Sfondo chiaro
Colors.text          // Testo principale

// Spaziature
Spacing.xs, sm, md, lg, xl, xxl

// Tipografia
Typography.title, subtitle, body, caption, small
```

## Annotazioni per il Sviluppo

### Aggiungere nuovi filtri
Modifica `src/utils/filters.js` e aggiungi un nuovo filtro all'oggetto `FILTERS`:

```javascript
myFilter: {
  name: 'Nome Filtro',
  nameEn: 'Filter Name',
  filter: [
    { name: 'property', value: 0.5 },
    // ... altre proprietà
  ],
}
```

### Personalizzare il tema
Modifica `src/styles/theme.js` per cambiare colori, spaziature e tipografia.

### Aggiungere nuove schermate
1. Crea il file in `src/screens/`
2. Aggiungi la rotta in `App.js`
3. Aggiungi navigazione dove necessario

## Troubleshooting

### L'app non si avvia
- Verifica che tutte le dipendenze siano installate
- Cancella `node_modules` e reinstalla: `rm -rf node_modules && npm install`
- Riavvia Expo: `npm start -- --clear`

### La fotocamera non funziona
- Verifica i permessi nelle impostazioni del dispositivo
- Su Android, verifica che il dispositivo abbia una fotocamera
- Su iOS emulator, la fotocamera potrebbe non essere disponibile

### I filtri non si applicano
- Verifica che l'URI dell'immagine sia valido
- Controlla la console per errori
- Prova a riavviare l'app

## Licenza

Questo progetto è stato creato a scopo educativo.

## Autore

Creato con React Native e Expo.

---

**Note**: Questa è un'app dimostrativa. Per un'applicazione di produzione, considera:
- Ottimizzazione delle performance per grandi gallerie
- Backup cloud delle foto
- Sincronizzazione tra dispositivi
- Filtri personalizzati più avanzati
- Editing avanzato delle immagini

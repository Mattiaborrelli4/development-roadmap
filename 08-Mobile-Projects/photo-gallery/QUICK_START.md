# Photo Gallery - Guida Rapida

## 🚀 Avvio Rapido

```bash
# Installa le dipendenze
npm install

# Avvia l'app
npm start

# Su un terminale separato, per Android
npm run android

# Su un terminale separato, per iOS (solo Mac)
npm run ios
```

## 📱 Funzionalità Principali

### Gestione Foto
- ✅ Scatta foto con la fotocamera
- ✅ Importa dalla galleria
- ✅ Applica filtri (8 filtri disponibili)
- ✅ Condividi foto
- ✅ Elimina foto
- ✅ Visualizza dettagli

### Gestione Album
- ✅ Crea album
- ✅ Rinomina album
- ✅ Elimina album
- ✅ Aggiungi foto agli album
- ✅ Sposta foto tra album

### Filtri Disponibili
1. **Originale** - Nessun filtro
2. **Bianco e Nero** - Grayscale
3. **Seppia** - Effetto vintage caldo
4. **Vintage** - Contrast + saturation
5. **Caldo** - Tonalità calde
6. **Freddo** - Tonalità fredde
7. **Drammatico** - Alto contrasto
8. **Sfocato** - Blur effect

## 🏗 Struttura dell'App

```
App.js
├── GalleryScreen (Home)
│   ├── Vista Foto (Griglia 2/3 colonne)
│   └── Vista Album
├── AlbumDetailScreen
│   ├── Foto dell'album
│   └── Operazioni album
├── CameraScreen
│   └── Fotocamera integrata
└── SettingsScreen
    └── Impostazioni e statistiche
```

## 🎨 Tema e Personalizzazione

Modifica `src/styles/theme.js` per personalizzare:
- Colori
- Spaziature
- Tipografia
- Bordi
- Ombre

## 📦 Componenti Principali

### PhotoGrid
Griglia responsive per visualizzare le foto
- Prop: `numColumns` (2 o 3)
- Supporta selezione multipla
- Pull-to-refresh

### PhotoItem
Singola foto con checkbox per selezione
- Visualizza filtro applicato
- Supporta long-press

### PhotoView
Modal a schermo intero per visualizzare foto
- Informazioni dettagliate
- Applicazione filtri
- Condivisione ed eliminazione

### FilterSelector
Selettore orizzontale di filtri
- Preview in tempo reale
- 8 filtri disponibili

### AlbumCard
Card per visualizzare album
- Copertina album
- Conteggio foto
- Data creazione

## 🔧 Services

### photoService
```javascript
import { photoService } from './services/photoService';

// Scatta foto
const photo = await photoService.takePhoto();

// Seleziona dalla galleria
const photos = await photoService.pickFromGallery(true);

// Salva foto
await photoService.savePhoto(photo);

// Elimina foto
await photoService.deletePhoto(photoId);

// Condividi foto
await photoService.sharePhoto(photoUri);
```

### albumService
```javascript
import { albumService } from './services/albumService';

// Crea album
const album = await albumService.createAlbum('Vacanze');

// Ottieni album
const albums = await albumService.getAllAlbums();

// Rinomina album
await albumService.renameAlbum(albumId, 'Nuovo Nome');

// Elimina album
await albumService.deleteAlbum(albumId);

// Aggiungi foto a album
await albumService.addPhotosToAlbum(albumId, [photoId1, photoId2]);
```

### filterService
```javascript
import { filterService } from './services/filterService';

// Ottieni tutti i filtri
const filters = filterService.getAllFilters();

// Applica filtro
await filterService.applyFilterToPhoto(photoId, 'sepia');
```

## 🪝 Custom Hooks

### usePhotos
```javascript
const {
  photos,           // Array di foto
  loading,         // Boolean
  error,           // String | null
  refresh,         // Function
  addPhoto,        // Function
  deletePhoto,     // Function
  applyFilter,     // Function
  sharePhoto,      // Function
} = usePhotos(albumId); // albumId è opzionale
```

### useAlbums
```javascript
const {
  albums,              // Array di album
  loading,            // Boolean
  error,              // String | null
  refresh,            // Function
  createAlbum,        // Function
  renameAlbum,        // Function
  deleteAlbum,        // Function
  addPhotosToAlbum,   // Function
} = useAlbums();
```

## 🎯 Pattern Utilizzati

### Service Layer
Logica di business separata dai componenti
- Services in `src/services/`
- Testabile e riutilizzabile

### Custom Hooks
 Stato e logica condivisa
- Hooks in `src/hooks/`
- Semplificano i componenti

### Component Separation
Componenti riutilizzabili
- UI components in `src/components/`
- Screens contengono la logica di navigazione

### Centralized Theme
Tema unico per tutta l'app
- `src/styles/theme.js`
- Facile personalizzazione

## 🔐 Permessi

### iOS
- Camera
- Photo Library
- Photo Library Add

### Android
- CAMERA
- READ_EXTERNAL_STORAGE
- WRITE_EXTERNAL_STORAGE
- READ_MEDIA_IMAGES (Android 13+)

## 🐛 Troubleshooting

### Foto non si salvano
Verifica i permessi nelle impostazioni del dispositivo

### Filtri non funzionano
Controlla che l'URI dell'immagine sia valido

### App crasha all'avvio
- Cancella node_modules
- Reinstalla le dipendenze
- Pulisci la cache di Expo

```bash
rm -rf node_modules
npm install
npx expo start -- --clear
```

## 📝 Note per lo Sviluppo

### Performance
- Usa Image da expo-image invece di Image da react-native
- Implementa virtualization per liste molto lunghe
- Ottimizza le dimensioni delle immagini

### Next Steps
- [ ] Implementa ricerca foto
- [ ] Aggiungi tag alle foto
- [ ] Backup su cloud
- [ ] Edit avanzato immagini
- [ ] Slideshow mode
- [ ] Animated transitions

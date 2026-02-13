# 🚀 Guida Rapida - Social Media Clone

## Avvio Rapido

### 1. Installazione
```bash
cd social-media-clone
npm install
```

### 2. Avvio Applicazione
```bash
npm start
```

### 3. Esecuzione

**Per Android:**
Premi `a` nel terminale dopo che Expo è partito

**Per iOS (solo macOS):**
Premi `i` nel terminale

**Con Expo Go:**
1. Installa l'app Expo Go sul tuo smartphone
2. Scansiona il codice QR che appare nel terminale
3. L'app si aprirà automaticamente

## 📱 Funzionalità Principali

### Navigazione
- **Home**: Feed con tutti i post
- **Cerca**: Trova utenti
- **+**: Crea nuovi post
- **Notifiche**: Visualizza attività
- **Profilo**: Gestisci il tuo profilo

### Interazioni
- **Doppio tap su un post**: Metti like
- **Tap sui commenti**: Apri sezione commenti
- **Tap sull'avatar**: Vai al profilo utente
- **Pull down**: Aggiorna il feed

## 🔑 Utente di Default

L'app viene fornita con un utente pre-configurato:
- **Username**: io_mattia
- **12 utenti sample** con cui interagire
- **25 post** generati automaticamente
- **30 notifiche** di esempio

## 🛠️ Struttura Progetto

```
src/
├── components/     # Componenti UI riutilizzabili
├── screens/        # Schermate dell'app
├── navigation/     # Configurazione navigazione
├── services/       # API simulata e storage
├── hooks/          # Custom React hooks
├── utils/          # Costanti e utilità
└── styles/         # Tema e stili
```

## 💾 Persistenza Dati

Tutti i dati sono salvati localmente usando AsyncStorage:
- Post
- Like
- Commenti
- Profilo utente
- Notifiche

## 🎨 Personalizzazione

### Colori
Modifica `src/utils/constants.js` per cambiare i colori dell'app

### Dati Sample
Modifica `src/services/dataService.js` per cambiare utenti e post di esempio

## 📚 Componenti Principali

### PostCard
Mostra un post con immagine/video, like, commenti

### StoryRing
Mostra una storia con ring colorato

### CommentItem
Visualizza un singolo commento

### LikeButton
Pulsante like con animazione cuore

## 🔧 Comandi Utili

### Pulisci cache
```bash
npx expo start -c
```

### Reset cache npm
```bash
npm cache clean --force
rm -rf node_modules
npm install
```

## 📱 Schermate

1. **FeedScreen**: Home con feed e storie
2. **SearchScreen**: Ricerca utenti
3. **NewPostScreen**: Crea nuovi post
4. **NotificationsScreen**: Notifiche
5. **ProfileScreen**: Profilo utente
6. **PostDetailScreen**: Dettaglio post con commenti
7. **MessagesScreen**: Messaggistica
8. **EditProfileScreen**: Modifica profilo

## 🐛 Risoluzione Problemi

### Expo non parte
```bash
npx expo start --tunnel
```

### Errori dipendenze
```bash
npm install --legacy-peer-deps
```

### Video non funzionano
Assicurati di avere i permessi in `app.json` per `expo-av`

## 📖 Documentazione

Per maggiori dettagli, vedi `README.md`

---

Buon sviluppo! 🚀

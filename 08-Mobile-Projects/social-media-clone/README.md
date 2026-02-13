# 📱 Social Media Clone

Un'applicazione mobile completa in stile Instagram sviluppata con React Native e Expo.

## 🎯 Panoramica del Progetto

Social Media Clone è un'app di social networking che replica le funzionalità principali di Instagram, fornendo un'esperienza utente fluida e moderna con animazioni, navigazione e interazioni complete.

## ✨ Funzionalità

### Funzionalità Principali
- **📱 Feed Post**: Scorrimento infinito con posts di immagini e video
- **❤️ Sistema di Like**: Doppio tap per mettere like, con animazioni fluide
- **💬 Commenti**: Visualizza e aggiungi commenti ai post
- **🔍 Ricerca**: Cerca utenti e esplora il contenuto
- **🔔 Notifiche**: Ricevi notifiche per like, commenti, follow e menzioni
- **📨 Messaggi**: Sistema di messaggistica diretta simulato
- **👤 Profilo Utente**: Visualizza e modifica il tuo profilo
- **📷 Nuovi Post**: Crea nuovi post con foto o video
- **🎬 Storie**: Visualizza storie degli utenti (funzionalità visiva)

### Funzionalità Tecniche
- **🔄 Pull-to-Refresh**: Aggiorna il feed scorrendo verso il basso
- **♾️ Scroll Infinito**: Caricamento paginato dei post
- **💾 AsyncStorage**: Persistenza locale dei dati
- **🎨 Animazioni Reanimated**: Animazioni fluide e performanti
- **🎯 Navigazione React Navigation**: Tab navigation e stack navigation
- **📹 Supporto Video**: Riproduzione video con react-native-video

## 🛠️ Tech Stack

### Core Framework
- **React Native**: 0.74.5
- **Expo SDK**: ~51.0.0
- **React**: 18.2.0

### Navigazione
- **@react-navigation/native**: 6.1.18
- **@react-navigation/bottom-tabs**: 6.6.1
- **@react-navigation/stack**: 6.4.1
- **react-native-screens**: 3.31.1
- **react-native-safe-area-context**: 4.10.5

### Gestione Dati
- **@react-native-async-storage/async-storage**: 1.23.1
- **@react-native-community/netinfo**: 11.3.1

### Media
- **expo-av**: 14.7.1 - Per la riproduzione video
- **expo-image-picker**: 15.0.5 - Per la selezione di immagini
- **expo-camera**: 15.0.5 - Per la fotocamera
- **expo-media-library**: 16.0.5 - Per la libreria media

### Animazioni & UI
- **react-native-reanimated**: 3.10.1
- **react-native-gesture-handler**: 2.16.1
- **react-native-modal**: 13.0.1

## 📁 Struttura del Progetto

```
social-media-clone/
├── App.js                          # Entry point dell'applicazione
├── app.json                        # Configurazione Expo
├── package.json                    # Dipendenze del progetto
├── src/
│   ├── components/                  # Componenti riutilizzabili
│   │   ├── PostCard.jsx           # Card per i post
│   │   ├── StoryRing.jsx          # Ring per le storie
│   │   ├── CommentItem.jsx        # Item per i commenti
│   │   ├── LikeButton.jsx         # Pulsante like animato
│   │   ├── Avatar.jsx             # Avatar utente
│   │   └── ActionButton.jsx       # Pulsante generico
│   ├── screens/                    # Schermate dell'app
│   │   ├── FeedScreen.jsx         # Feed principale
│   │   ├── PostDetailScreen.jsx   # Dettaglio post con commenti
│   │   ├── SearchScreen.jsx       # Ricerca utenti
│   │   ├── NotificationsScreen.jsx  # Notifiche
│   │   ├── ProfileScreen.jsx      # Profilo utente
│   │   ├── MessagesScreen.jsx     # Messaggistica
│   │   ├── NewPostScreen.jsx      # Crea nuovo post
│   │   └── EditProfileScreen.jsx  # Modifica profilo
│   ├── navigation/                 # Configurazione navigazione
│   │   └── TabNavigator.js        # Navigator principale
│   ├── services/                   # Servizi e API
│   │   ├── dataService.js         # API simulata
│   │   └── storageService.js      # Gestione AsyncStorage
│   ├── hooks/                      # Custom React Hooks
│   │   ├── usePosts.js            # Gestione post
│   │   ├── useAuth.js             # Gestione autenticazione
│   │   └── useNotifications.js    # Gestione notifiche
│   ├── utils/                      # Utilità
│   │   └── constants.js           # Costanti globali
│   └── styles/                     # Stili
│       └── theme.js               # Tema dell'applicazione
└── README.md                       # Documentazione
```

## 🗄️ Struttura Dati

### Post
```javascript
{
  id: string,
  user: {id, username, avatar},
  content: {type: 'image'|'video', uri},
  caption: string,
  likes: number,
  liked: boolean,
  comments: number,
  createdAt: timestamp,
  location: string (optional)
}
```

### Utente
```javascript
{
  id: string,
  username: string,
  avatar: string (uri),
  bio: string,
  posts: number,
  followers: number,
  following: number,
  isFollowing: boolean
}
```

### Notifica
```javascript
{
  id: string,
  type: 'like'|'comment'|'follow'|'mention',
  user: {id, username, avatar},
  post: {id, content},
  message: string,
  createdAt: timestamp,
  read: boolean
}
```

## 🚀 Installazione e Setup

### Prerequisiti
- Node.js (v14 o superiore)
- npm o yarn
- Expo CLI
- Android Studio (per Android) o Xcode (per iOS) - opzionale, puoi usare Expo Go

### Installazione

1. **Clona il repository** (se applicabile) o naviga nella cartella del progetto

2. **Installa le dipendenze**
```bash
cd social-media-clone
npm install
```

3. **Avvia l'applicazione**
```bash
npm start
```

4. **Esegui su dispositivo/simulatore**
- Android: Premi `a` dopo aver avviato Expo
- iOS: Premi `i` dopo aver avviato Expo (solo macOS)
- Expo Go: Scansiona il codice QR dall'app Expo Go

## 📱 Navigazione

### Tab Bar Principale
1. **🏠 Home**: Feed con tutti i post
2. **🔍 Cerca**: Ricerca utenti e esplora
3. **➕ Aggiungi**: Crea un nuovo post
4. **🔔 Notifiche**: Attività e notifiche
5. **👤 Profilo**: Il tuo profilo

### Stack Navigation
- Feed → Dettaglio Post → Commenti
- Ricerca → Profilo Utente
- Profilo → Modifica Profilo
- Notifiche → Dettaglio Post/Profilo

## 🎨 Funzionalità UI/UX

### Animazioni
- ❤️ Animazione cuore quando metti like
- 🔄 Animazioni di caricamento
- ✨ Transizioni fluide tra schermate

### Interazioni
- 👆 **Doppio tap**: Metti like su un post
- 👆 **Tap singolo**: Apri dettagli post
- 👆 **Long press**: Opzioni aggiuntive
- 🖱️ **Pull-to-refresh**: Aggiorna il feed

### Componenti
- **Avatar**: Circolare con bordo personalizzabile
- **Story Ring**: Ring colorato per storie non viste
- **Post Card**: Card completa con azioni
- **Comment Item**: Commento formattato con timestamp
- **Like Button**: Pulsante like con animazione

## 💾 Persistenza Dati

L'app utilizza AsyncStorage per:
- ✅ Salvare i post
- ✅ Tracciare i like
- ✅ Salvare i post preferiti
- ✅ Memorizzare il profilo utente
- ✅ Cache delle notifiche

## 🔧 Configurazione

### Tema
Il tema dell'app è configurabile in `src/utils/constants.js`:

```javascript
export const THEME = {
  colors: {
    primary: '#0095F6',
    background: '#FFFFFF',
    text: '#262626',
    // ... altri colori
  },
  // ... altre configurazioni
};
```

### Dati Simulati
I dati di esempio sono generati in `src/services/dataService.js`:
- 12 utenti sample
- 25 post con vari contenuti
- 30 notifiche diverse
- 10 storie

## 📸 Schermate

### Feed Screen
- Header con logo e icone
- Storie orizzontali
- Feed verticale con pull-to-refresh

### Search Screen
- Barra di ricerca
- Lista utenti con pulsante follow/unfollow
- Statistiche rapide

### Profile Screen
- Avatar grande
- Statistiche (post, follower, following)
- Biografia
- Griglia post
- Tabs: Post, Salvati, Taggati

### Notifications Screen
- Lista notifiche
- Badge per non lette
- Icone diverse per tipo
- Segna tutto come letto

### Messages Screen
- Lista conversazioni
- Chat con bolle messaggi
- Input per inviare messaggi

### New Post Screen
- Preview media
- Input caption
- Opzioni aggiuntive

## 🐛 Risoluzione Problemi

### Problemi Comuni

**Expo non si avvia**
```bash
npm cache clean --force
rm -rf node_modules
npm install
```

**Errori di dipendenze**
```bash
npm install --legacy-peer-deps
```

**Video non si riproducono**
- Assicurati di avere i permessi corretti in app.json
- Verifica che il formato video sia supportato

## 🚧 Funzionalità Future

Potenziali miglioramenti:
- [ ] Autenticazione reale con Firebase
- [ ] Backend API reale
- [ ] Caricamento immagini su cloud storage
- [ ] Storie interattive
- [ ] Filtri per le immagini
- [ ] Messaggistica in tempo reale
- [ ] Dark mode
- [ ] Multi-language support
- [ ] Pubblicità integrate
- [ ] Analytics e tracking

## 📄 Licenza

Questo progetto è stato creato a scopo educativo.

## 👨‍💻 Sviluppatore

Progetto sviluppato come portfolio project per dimostrare competenze in:
- React Native
- Expo
- React Navigation
- Gestione stato con Context API
- Animazioni con Reanimated
- Gestione dati locali

---

**Nota**: Questa è un'applicazione dimostrativa con dati simulati. Non è connessa a un backend reale e tutti i dati sono memorizzati localmente sul dispositivo.

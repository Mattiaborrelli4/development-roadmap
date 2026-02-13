# Setup Guida - Chat App

## Istruzioni di Configurazione

### 1. Installazione Dipendenze

Dalla directory `chat-app/`, esegui:

```bash
npm install
```

### 2. Assets Placeholder

Per avviare l'app, devi creare i file placeholder per gli assets. Nella cartella principale `chat-app/`, crea una cartella `assets/` e aggiungi file placeholder (anche vuoti):

```
chat-app/
└── assets/
    ├── icon.png (puoi usare un'immagine 1024x1024 placeholder)
    ├── adaptive-icon.png (1024x1024)
    ├── splash.png (1284x2778)
    └── favicon.png (48x48)
```

In alternativa, puoi rimuovere temporaneamente i riferimenti agli assets dal file `app.json`:

```json
{
  "expo": {
    "name": "Chat App",
    "slug": "chat-app",
    "version": "1.0.0",
    "orientation": "portrait",
    "assetBundlePatterns": [
      "**/*"
    ]
    // Rimuovi le sezioni icon, splash, ios, android, web
  }
}
```

### 3. Avvio Applicazione

```bash
# Avvia il development server
npm start

# Oppure per dispositivo specifico:
npm run android  # Android
npm run ios      # iOS (solo macOS)
npm run web      # Web browser
```

### 4. Funzionalità Demo

L'app include una simulazione di real-time con:
- Messaggi in arrivo automatici ogni 10-30 secondi
- Indicatori di digitazione simulati
- Cambiamenti stato online/offline automatici
- Persistenza dati con AsyncStorage

### Note Importanti

- L'utente corrente è hardcoded come 'user1' (Mario Rossi)
- I dati vengono inizializzati al primo avvio con dati mock
- Per resettare i dati, usa "Cancella Dati" dal Profilo

### Risoluzione Problemi

#### "Cannot find module 'react-native-reanimated'"
```bash
npm install react-native-reanimated
npx expo prebuild --clean
```

#### "Module not found: Can't resolve '../assets/...'"
Crea la cartella assets con immagini placeholder o rimuovi i riferimenti da app.json

#### AsyncStorage non funziona
Assicurati di aver installato le dipendenze corrette per la tua piattaforma Expo SDK.

### Struttura Progetto Completata

Tutti i file richiesti sono stati creati:

**Configurazione:**
- ✅ App.js
- ✅ app.json
- ✅ package.json
- ✅ babel.config.js

**Servizi:**
- ✅ src/services/chatService.js (real-time simulato)
- ✅ src/services/storageService.js

**Hooks:**
- ✅ src/hooks/useMessages.js
- ✅ src/hooks/useChatRooms.js
- ✅ src/hooks/useTyping.js
- ✅ src/hooks/useUsers.js

**Componenti:**
- ✅ src/components/MessageBubble.jsx
- ✅ src/components/ChatInput.jsx
- ✅ src/components/TypingIndicator.jsx
- ✅ src/components/OnlineStatus.jsx
- ✅ src/components/UserAvatar.jsx

**Screen:**
- ✅ src/screens/ChatsListScreen.jsx
- ✅ src/screens/ChatRoomScreen.jsx
- ✅ src/screens/UsersScreen.jsx
- ✅ src/screens/ProfileScreen.jsx

**Stili:**
- ✅ src/styles/theme.js

**Utils:**
- ✅ src/utils/constants.js

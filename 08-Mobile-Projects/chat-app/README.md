# Chat App - Applicazione di Messaggistica in Tempo Reale

Applicazione di chat mobile sviluppata con React Native ed Expo che simula la messaggistica in tempo reale.

## Caratteristiche

### Funzionalità Principali
- ✅ Messaggistica in tempo reale (simulata)
- ✅ Stanze di chat multiple (gruppi e dirette)
- ✅ Messaggi privati uno-a-uno
- ✅ Stato online/offline degli utenti
- ✅ Conferme di lettura (doppia spunta)
- ✅ Indicatori di digitazione
- ✅ Cronologia messaggi
- ✅ Profili utente
- ✅ Notifiche push simulate
- ✅ Condivisione immagini/media

### Interfaccia Utente
- Bolle messaggi con stile WhatsApp
- Timestamp su ogni messaggio
- Conferme di lettura (✓✓)
- Indicatori di digitazione animati
- Stato online nell'header
- Scroll automatico ai nuovi messaggi
- Animazioni fluide con Reanimated
- Navigazione stack e tab

### Gestione Chat
- Creazione nuove chat
- Chat di gruppo con utenti multipli
- Messaggi diretti
- Ricerca messaggi
- Mute notifiche
- Cancella cronologia chat
- Blocca utenti

## Struttura del Progetto

```
chat-app/
├── App.js                          # Entry point principale
├── app.json                        # Configurazione Expo
├── package.json                    # Dipendenze
├── src/
│   ├── components/
│   │   ├── MessageBubble.jsx       # Bolla messaggio
│   │   ├── ChatInput.jsx           # Input messaggi
│   │   ├── TypingIndicator.jsx     # Indicatore digitazione
│   │   ├── OnlineStatus.jsx        # Stato online
│   │   └── UserAvatar.jsx          # Avatar utente
│   ├── screens/
│   │   ├── ChatsListScreen.jsx     # Lista chat
│   │   ├── ChatRoomScreen.jsx      # Stanza chat
│   │   ├── UsersScreen.jsx         # Lista utenti
│   │   └── ProfileScreen.jsx       # Profilo utente
│   ├── services/
│   │   ├── chatService.js          # Servizio chat (real-time simulato)
│   │   └── storageService.js       # Persistenza AsyncStorage
│   ├── hooks/
│   │   ├── useMessages.js          # Hook messaggi
│   │   ├── useChatRooms.js         # Hook stanze chat
│   │   └── useTyping.js            # Hook digitazione
│   ├── utils/
│   │   └── constants.js            # Costanti e dati mock
│   └── styles/
│       └── theme.js                # Tema e stili
└── README.md
```

## Struttura Dati

### Utente
```javascript
{
  id: string,
  username: string,
  avatar: string (uri),
  status: 'online' | 'offline' | 'away',
  lastSeen: timestamp
}
```

### Stanza Chat
```javascript
{
  id: string,
  name: string,
  type: 'group' | 'direct',
  participants: array of user IDs,
  lastMessage: object,
  unreadCount: number,
  createdAt: timestamp
}
```

### Messaggio
```javascript
{
  id: string,
  roomId: string,
  senderId: string,
  text: string,
  type: 'text' | 'image' | 'system',
  timestamp: timestamp,
  read: boolean,
  readBy: array of user IDs
}
```

## Installazione

1. Installa le dipendenze:
```bash
npm install
```

2. Avvia l'applicazione:
```bash
npm start
```

3. Esegui su dispositivo/emulatore:
```bash
npm run android  # Per Android
npm run ios      # Per iOS
```

## Tecnologie Utilizzate

- **React Native** - Framework mobile
- **Expo** - Piattaforma sviluppo
- **React Navigation** - Navigazione
- **AsyncStorage** - Persistenza dati
- **Reanimated** - Animazioni fluide
- **Vector Icons** - Icone

## Funzionalità Simulate

Per questa demo, le seguenti funzionalità sono simulate localmente:

- **WebSocket**: Simulato con setInterval/setTimeout
- **Messaggi in arrivo**: Generati randomicamente ogni 10-30 secondi
- **Indicatori digitazione**: Simulati con timer
- **Notifiche push**: Simulate con Expo Notifications
- **Stato online**: Cambia automaticamente
- **Conferme lettura**: Marcatore automatico dopo visualizzazione

## Note di Sviluppo

- L'utente corrente è hardcoded come 'user1'
- I dati sono persistiti in AsyncStorage
- Il real-time è simulato con timer
- Per produzione, sostituire chatService.js con un vero backend WebSocket

## Licenza

MIT

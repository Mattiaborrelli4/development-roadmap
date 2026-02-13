# 💬 React Chat App

Applicazione di chat in tempo reale costruita con React e WebSockets simulati.

![React Chat App](https://img.shields.io/badge/React-18.2-61DAFB?logo=react)
![Vite](https://img.shields.io/badge/Vite-5.0-646CFF?logo=vite)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?logo=javascript)

## 🎯 Caratteristiche

- ✅ **Stanze multiple** - 5 stanze tematiche diverse
- ✅ **Messaggistica in tempo reale** - Simulata con setTimeout
- ✅ **Autenticazione utenti** - Login semplice con username
- ✅ **Cronologia messaggi** - Salvata in localStorage
- ✅ **Lista utenti online** - Con stato e ultimi accessi
- ✅ **Indicatore di digitazione** - Vedi chi sta scrivendo
- ✅ **Design responsivo** - Funziona su desktop, tablet e mobile
- ✅ **Emoji picker** - Aggiungi emoji ai tuoi messaggi
- ✅ **Timestamp** - Orario dei messaggi con raggruppamento per data
- ✅ **Sistema di notifiche** - Messaggi di sistema per entrata/uscita

## 🚀 Guida Rapida

### Prerequisiti

- Node.js (v16 o superiore)
- npm o yarn

### Installazione

```bash
# Installa le dipendenze
npm install

# Avvia l'applicazione
npm run dev
```

L'app sarà disponibile su `http://localhost:3000`

### Comandi disponibili

```bash
# Sviluppo
npm run dev

# Build per produzione
npm run build

# Anteprima build di produzione
npm run preview
```

## 📁 Struttura del Progetto

```
react-chat-app/
├── public/
│   └── index.html          # Template HTML
├── src/
│   ├── components/         # Componenti React
│   │   ├── Login.jsx       # Schermata di login
│   │   ├── Login.css
│   │   ├── ChatRoom.jsx    # Layout principale chat
│   │   ├── ChatRoom.css
│   │   ├── RoomList.jsx    # Lista delle stanze
│   │   ├── RoomList.css
│   │   ├── UserList.jsx    # Lista utenti online
│   │   ├── UserList.css
│   │   ├── MessageList.jsx # Visualizzazione messaggi
│   │   ├── MessageList.css
│   │   ├── MessageInput.jsx # Input messaggi + emoji picker
│   │   └── MessageInput.css
│   ├── contexts/
│   │   └── ChatContext.jsx # Context API per stato globale
│   ├── utils/
│   │   └── socket.js       # WebSocket simulato
│   ├── data.js             # Dati iniziali (stanze, messaggi)
│   ├── App.jsx             # Componente principale
│   ├── App.css             # Stili globali
│   └── index.js            # Entry point
├── package.json
├── vite.config.js          # Configurazione Vite
└── README.md
```

## 🏗️ Architettura

### Gestione dello Stato

L'applicazione utilizza **React Context API** per la gestione dello stato globale:

- **Stato dell'utente** - Informazioni sull'utente loggato
- **Stanze** - Lista delle stanze disponibili
- **Messaggi** - Cronologia dei messaggi per stanza
- **Utenti online** - Lista utenti con stato
- **Indicatori di digitazione** - Utenti che stanno scrivendo

### WebSocket Simulato

Il file `src/utils/socket.js` contiene una classe `MockSocket` che simula il comportamento di Socket.io:

```javascript
// Connessione
socket.connect(userId, username);

// Invia messaggio
socket.emitMessage(roomId, text);

// Unisciti a una stanza
socket.joinRoom(roomId);

// Indicatore di digitazione
socket.emitTyping(roomId, isTyping);
```

### Componenti Principali

#### Login
Gestisce l'autenticazione con input username e validazione.

#### RoomList
Mostra la lista delle stanze con contatore messaggi e descrizione.

#### UserList
Visualizza gli utenti online con stato (online/away/offline) e ultimo accesso.

#### MessageList
Renderizza i messaggi con:
- Bubbles colorati per messaggi inviati/ricevuti
- Raggruppamento per data
- Avatar per utenti
- Timestamp
- Indicatore di digitazione

#### MessageInput
Input per messaggi con:
- Emoji picker
- Contatore caratteri
- Supporto Shift+Enter per a capo
- Auto-focus

## 🎨 Features

### Messaggi

- **Messaggi inviati** - Bubbles viola con gradiente
- **Messaggi ricevuti** - Bubbles grigi
- **Messaggi di sistema** - Centrati con sfondo grigio
- **Notifiche** - Entrata/uscita utenti

### Digitazione

Quando un utente sta scrivendo, vedrai:
```
👤 Mario sta scrivendo...
```

### Emoji Picker

Clicca sull'icona 😀 nell'input per aprire il picker con 32 emoji comuni.

### Persistenza

I messaggi vengono salvati automaticamente in `localStorage` e ripristinati al prossimo accesso.

## 🔌 Integrazione con Backend Reale

Per connettere questa app a un backend Socket.io reale:

### 1. Installa Socket.io Client

```bash
npm install socket.io-client
```

### 2. Modifica `src/utils/socket.js`

```javascript
import { io } from 'socket.io-client';

const socket = io('http://localhost:4000', {
  auth: {
    token: localStorage.getItem('token')
  },
  autoConnect: false
});

export default socket;
```

### 3. Crea il Server (Node.js + Express)

```javascript
// server.js
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: 'http://localhost:3000',
    methods: ['GET', 'POST']
  }
});

io.on('connection', (socket) => {
  console.log('Utente connesso:', socket.id);

  socket.on('joinRoom', ({ roomId, username }) => {
    socket.join(roomId);
    socket.to(roomId).emit('message', {
      type: 'notification',
      text: `${username} è entrato nella stanza`,
      timestamp: new Date().toISOString()
    });
  });

  socket.on('sendMessage', (data) => {
    io.to(data.roomId).emit('message', {
      ...data,
      timestamp: new Date().toISOString()
    });
  });

  socket.on('typing', (data) => {
    socket.to(data.roomId).emit('typing', data);
  });
});

server.listen(4000, () => {
  console.log('Server in ascolto sulla porta 4000');
});
```

### 4. Database

Salva i messaggi nel database (MongoDB, PostgreSQL, etc.):

```javascript
// Esempio con MongoDB
const Message = require('./models/Message');

socket.on('sendMessage', async (data) => {
  const message = new Message(data);
  await message.save();
  io.to(data.roomId).emit('message', message);
});
```

### 5. Autenticazione

Implementa JWT o session-based auth:

```javascript
const jwt = require('jsonwebtoken');

io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  try {
    const decoded = jwt.verify(token, 'your-secret');
    socket.user = decoded;
    next();
  } catch (err) {
    next(new Error('Autenticazione fallita'));
  }
});
```

## 🎯 Route API (Esempio)

```
POST   /api/auth/login      - Login utente
GET    /api/rooms           - Lista stanze
GET    /api/messages/:room  - Messaggi stanza
POST   /api/messages        - Invia messaggio
GET    /api/users           - Utenti online
```

## 🛠️ Tecnologic Utilizzate

- **React 18.2** - UI library
- **Vite 5.0** - Build tool e dev server
- **Socket.io Client** - WebSocket library (inclusa ma non usata nel demo)
- **Context API** - State management
- **CSS Modules** - Component styling
- **localStorage** - Data persistence

## 📱 Responsive Design

L'app è completamente responsiva:

- **Desktop** (> 1024px) - Layout a 3 colonne
- **Tablet** (768px - 1024px) - Sidebar ridotte
- **Mobile** (< 768px) - Layout single column con header mobile

## 🐛 Troubleshooting

### I messaggi non si salvano
Controlla che `localStorage` sia abilitato nel browser.

### L'emoji picker non funziona
Assicurati che il browser supporti CSS Grid.

### La chat sembra lenta
Nella demo, i messaggi sono deliberatamente ritardati (2-7 secondi) per simulare una vera connessione WebSocket.

## 📄 Licenza

Questo progetto è creato a scopo educativo. Sentiti libero di utilizzarlo e modificarlo come preferisci.

## 👤 Autore

Creato come progetto dimostrativo per imparare React e WebSocket.

## 🙏 Acknowledgments

- Design ispirato dalle migliori app di chat moderne
- Icone emoji dal set emoji standard
- Gradienti colorati da UI Gradients

---

**Nota Bene:** Questa è una versione demo front-end. Per una produzione reale, implementa un backend Socket.io con autenticazione e database.

/**
 * WebSocket simulato che imita Socket.io client
 * In un'applicazione reale, questo si connetterebbe a un server Socket.io
 */

class MockSocket {
  constructor() {
    this.connected = false;
    this.userId = null;
    this.username = null;
    this.listeners = {};
    this.typingUsers = new Set();
    this.typingTimeout = null;
  }

  // Connessione simulata
  connect(userId, username) {
    return new Promise((resolve) => {
      setTimeout(() => {
        this.userId = userId;
        this.username = username;
        this.connected = true;
        console.log(`🔌 Socket connesso come ${username}`);
        this._emit('connect', { userId, username });
        resolve();
      }, 500);
    });
  }

  // Disconnessione
  disconnect() {
    this.connected = false;
    this._emit('disconnect', { userId: this.userId });
    console.log('🔌 Socket disconnesso');
  }

  // Invia un messaggio
  emitMessage(roomId, text) {
    if (!this.connected) return;

    const message = {
      id: Date.now().toString(),
      roomId,
      userId: this.userId,
      username: this.username,
      text,
      timestamp: new Date().toISOString(),
      type: 'message'
    };

    // Simula l'invio al server
    setTimeout(() => {
      this._emit('message', message);
    }, 100);

    return message;
  }

  // Invia indicatore di digitazione
  emitTyping(roomId, isTyping) {
    if (!this.connected) return;

    this._emit('typing', {
      roomId,
      userId: this.userId,
      username: this.username,
      isTyping
    });
  }

  // Unisciti a una stanza
  joinRoom(roomId) {
    if (!this.connected) return;

    setTimeout(() => {
      const room = {
        id: roomId,
        name: roomId,
        usersCount: Math.floor(Math.random() * 10) + 1
      };
      this._emit('roomJoined', room);
      console.log(`🏠 Entrato nella stanza: ${roomId}`);

      // Simula un messaggio di benvenuto
      const welcomeMessage = {
        id: Date.now().toString(),
        roomId,
        userId: 'system',
        username: 'Sistema',
        text: `${this.username} è entrato nella stanza`,
        timestamp: new Date().toISOString(),
        type: 'notification'
      };
      this._emit('message', welcomeMessage);
    }, 300);
  }

  // Registra un event listener
  on(event, callback) {
    if (!this.listeners[event]) {
      this.listeners[event] = [];
    }
    this.listeners[event].push(callback);
  }

  // Rimuovi un event listener
  off(event, callback) {
    if (!this.listeners[event]) return;
    this.listeners[event] = this.listeners[event].filter(cb => cb !== callback);
  }

  // Emit interno (chiama i listeners)
  _emit(event, data) {
    if (this.listeners[event]) {
      this.listeners[event].forEach(callback => callback(data));
    }
  }

  // Simula messaggi in arrivo da altri utenti
  simulateIncomingMessage(roomId) {
    if (!this.connected) return;

    // Importa qui per evitare circular dependencies
    const sampleMessages = [
      'Interessante! Raccontami di più 🤔',
      'Sono d\'accordo con te!',
      'Wow, non lo sapevo! 🎉',
      'Ho appena finito un progetto simile',
      'Qualcuno ha documentazione utile?',
      'Grazie per il consiglio! 👍',
      'Stasera provo a implementarlo',
      'È una feature molto richiesta',
      'Ho trovato un bug interessante...',
      'Prova a guardare la documentazione ufficiale'
    ];

    const otherUsers = ['Marco', 'Anna', 'Paolo', 'Sofia', 'Luca', 'Giulia'];

    const randomMessage = sampleMessages[Math.floor(Math.random() * sampleMessages.length)];
    const randomUser = otherUsers[Math.floor(Math.random() * otherUsers.length)];

    setTimeout(() => {
      const message = {
        id: Date.now().toString(),
        roomId,
        userId: 'user_' + Math.random().toString(36).substr(2, 9),
        username: randomUser,
        text: randomMessage,
        timestamp: new Date().toISOString(),
        type: 'message'
      };
      this._emit('message', message);
    }, Math.random() * 5000 + 2000); // 2-7 secondi di ritardo
  }

  // Simula utenti online
  getOnlineUsers() {
    return [
      { id: 'user1', username: 'Mario', status: 'online', lastSeen: new Date() },
      { id: 'user2', username: 'Luca', status: 'online', lastSeen: new Date() },
      { id: 'user3', username: 'Giulia', status: 'away', lastSeen: new Date(Date.now() - 900000) },
      { id: 'user4', username: 'Anna', status: 'online', lastSeen: new Date() },
      { id: 'user5', username: 'Paolo', status: 'offline', lastSeen: new Date(Date.now() - 3600000) }
    ];
  }

  // Simula aggiornamento stato digitazione
  simulateTyping(roomId) {
    if (!this.connected) return;

    const otherUsers = ['Marco', 'Anna', 'Paolo', 'Sofia'];
    const randomUser = otherUsers[Math.floor(Math.random() * otherUsers.length)];

    setTimeout(() => {
      this._emit('typing', {
        roomId,
        userId: 'user_' + Math.random().toString(36).substr(2, 9),
        username: randomUser,
        isTyping: true
      });

      // Smetti di digitare dopo 2-4 secondi
      setTimeout(() => {
        this._emit('typing', {
          roomId,
          userId: 'user_' + Math.random().toString(36).substr(2, 9),
          username: randomUser,
          isTyping: false
        });
      }, Math.random() * 2000 + 2000);
    }, Math.random() * 10000 + 5000);
  }
}

// Crea istanza singleton
const socket = new MockSocket();

export default socket;

/**
 * NOTE PER L'INTEGRAZIONE CON UN BACKEND REALE:
 *
 * Per connettere questa app a un backend Socket.io reale:
 *
 * 1. Installa Socket.io client:
 *    npm install socket.io-client
 *
 * 2. Sostituisci questo file con:
 *
 *    import { io } from 'socket.io-client';
 *
 *    const socket = io('http://localhost:4000', {
 *      auth: {
 *        token: localStorage.getItem('token')
 *      }
 *    });
 *
 *    export default socket;
 *
 * 3. Lato server (Node.js + Express + Socket.io):
 *
 *    const io = require('socket.io')(4000, {
 *      cors: {
 *        origin: 'http://localhost:3000',
 *        methods: ['GET', 'POST']
 *      }
 *    });
 *
 *    io.on('connection', (socket) => {
 *      console.log('Utente connesso:', socket.id);
 *
 *      socket.on('joinRoom', ({ roomId, username }) => {
 *         socket.join(roomId);
 *         socket.to(roomId).emit('message', {
 *           type: 'notification',
 *           text: `${username} è entrato nella stanza`
 *         });
 *      });
 *
 *      socket.on('sendMessage', (data) => {
 *         io.to(data.roomId).emit('message', {
 *           ...data,
 *           timestamp: new Date().toISOString()
 *         });
 *      });
 *
 *      socket.on('typing', (data) => {
 *         socket.to(data.roomId).emit('typing', data);
 *      });
 *    });
 *
 * 4. Implementa l'autenticazione con JWT o sessioni
 * 5. Salva i messaggi nel database (MongoDB, PostgreSQL, etc.)
 * 6. Gestisci la persistenza e la cronologia dei messaggi
 */

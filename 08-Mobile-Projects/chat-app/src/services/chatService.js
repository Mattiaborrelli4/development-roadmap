import storageService from './storageService';
import {
  RANDOM_MESSAGES,
  MESSAGE_INTERVAL_MIN,
  MESSAGE_INTERVAL_MAX,
  TYPING_DURATION,
  STATUS_CHANGE_INTERVAL,
  ONLINE_STATUS
} from '../utils/constants';

class ChatService {
  constructor() {
    this.listeners = {
      message: [],
      typing: [],
      statusChange: [],
      roomUpdate: []
    };
    this.timers = [];
    this.typingUsers = new Map();
  }

  // Inizializza il servizio
  async initialize() {
    await storageService.initializeData();
    this.startRealtimeSimulation();
  }

  // Sottoscrivi agli eventi
  on(event, callback) {
    if (this.listeners[event]) {
      this.listeners[event].push(callback);
    }
  }

  // Rimuovi sottoscrizione
  off(event, callback) {
    if (this.listeners[event]) {
      this.listeners[event] = this.listeners[event].filter(cb => cb !== callback);
    }
  }

  // Emetti evento
  emit(event, data) {
    if (this.listeners[event]) {
      this.listeners[event].forEach(callback => callback(data));
    }
  }

  // Invia messaggio
  async sendMessage(roomId, senderId, text, type = 'text') {
    const message = {
      id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      roomId,
      senderId,
      text,
      type,
      timestamp: Date.now(),
      read: false,
      readBy: []
    };

    await storageService.addMessage(message);

    // Aggiorna l'ultimo messaggio della stanza
    const room = await storageService.getChatRoomById(roomId);
    if (room) {
      await storageService.updateChatRoom(roomId, {
        lastMessage: {
          text,
          senderId,
          timestamp: message.timestamp
        }
      });
    }

    this.emit('message', message);
    this.emit('roomUpdate', await storageService.getChatRoomById(roomId));

    return message;
  }

  // Ottieni messaggi di una stanza
  async getMessages(roomId) {
    return await storageService.getMessagesByRoom(roomId);
  }

  // Marca messaggi come letti
  async markAsRead(roomId, userId) {
    await storageService.markMessagesAsRead(roomId, userId);

    const room = await storageService.getChatRoomById(roomId);
    if (room && room.unreadCount > 0) {
      await storageService.updateChatRoom(roomId, { unreadCount: 0 });
      this.emit('roomUpdate', await storageService.getChatRoomById(roomId));
    }
  }

  // Ottieni stanze di chat
  async getChatRooms() {
    return await storageService.getChatRooms();
  }

  // Crea nuova stanza di chat
  async createChatRoom(name, type, participants) {
    const room = {
      id: `room_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      name,
      type,
      participants,
      lastMessage: null,
      unreadCount: 0,
      createdAt: Date.now()
    };

    await storageService.createChatRoom(room);
    this.emit('roomUpdate', room);

    return room;
  }

  // Ottieni tutti gli utenti
  async getUsers() {
    return await storageService.getUsers();
  }

  // Ottieni utente per ID
  async getUser(userId) {
    return await storageService.getUserById(userId);
  }

  // Ottieni utente corrente
  async getCurrentUser() {
    const userId = await storageService.getCurrentUserId();
    return await storageService.getUserById(userId);
  }

  // Aggiorna stato utente
  async updateUserStatus(userId, status) {
    await storageService.updateUser(userId, {
      status,
      lastSeen: Date.now()
    });

    this.emit('statusChange', { userId, status });
  }

  // Mostra indicatore digitazione
  showTypingIndicator(roomId, userId, username) {
    const key = `${roomId}_${userId}`;
    this.typingUsers.set(key, username);
    this.emit('typing', { roomId, userId, username, isTyping: true });

    // Rimuovi dopo TYPING_DURATION
    setTimeout(() => {
      this.typingUsers.delete(key);
      this.emit('typing', { roomId, userId, username, isTyping: false });
    }, TYPING_DURATION);
  }

  // Ottieni utenti che stanno scrivendo
  getTypingUsers(roomId) {
    const typing = [];
    this.typingUsers.forEach((username, key) => {
      const [rId, userId] = key.split('_');
      if (rId === roomId) {
        typing.push({ userId, username });
      }
    });
    return typing;
  }

  // Simulazione messaggi in arrivo
  startRealtimeSimulation() {
    // Simula messaggi in arrivo random
    const scheduleRandomMessage = () => {
      const delay = Math.random() * (MESSAGE_INTERVAL_MAX - MESSAGE_INTERVAL_MIN) + MESSAGE_INTERVAL_MIN;

      const timer = setTimeout(async () => {
        await this.simulateIncomingMessage();
        scheduleRandomMessage();
      }, delay);

      this.timers.push(timer);
    };

    scheduleRandomMessage();

    // Simula cambiamenti stato online
    const statusTimer = setInterval(async () => {
      await this.simulateStatusChanges();
    }, STATUS_CHANGE_INTERVAL);

    this.timers.push(statusTimer);

    // Simula indicatori di digitazione
    const typingTimer = setInterval(async () => {
      await this.simulateTypingIndicators();
    }, 15000);

    this.timers.push(typingTimer);
  }

  // Simula messaggio in arrivo
  async simulateIncomingMessage() {
    const rooms = await this.getChatRooms();
    const users = await this.getUsers();
    const currentUserId = await storageService.getCurrentUserId();

    if (rooms.length === 0) return;

    // Scegli stanza random
    const room = rooms[Math.floor(Math.random() * rooms.length)];

    // Scegli utente random (non l'utente corrente)
    const otherUsers = users.filter(u => u.id !== currentUserId && room.participants.includes(u.id));
    if (otherUsers.length === 0) return;

    const sender = otherUsers[Math.floor(Math.random() * otherUsers.length)];

    // Scegli messaggio random
    const messageText = RANDOM_MESSAGES[Math.floor(Math.random() * RANDOM_MESSAGES.length)];

    // Mostra indicatore digitazione prima del messaggio
    this.showTypingIndicator(room.id, sender.id, sender.username);

    // Invia messaggio dopo 2 secondi
    setTimeout(async () => {
      const message = await this.sendMessage(room.id, sender.id, messageText);

      // Aggiorna unread count se non è una stanza dell'utente corrente
      if (Math.random() > 0.5) {
        await storageService.updateChatRoom(room.id, {
          unreadCount: (room.unreadCount || 0) + 1
        });
        this.emit('roomUpdate', await storageService.getChatRoomById(room.id));
      }
    }, TYPING_DURATION);
  }

  // Simula cambiamenti stato
  async simulateStatusChanges() {
    const users = await this.getUsers();
    const currentUserId = await storageService.getCurrentUserId();

    const statuses = [ONLINE_STATUS.ONLINE, ONLINE_STATUS.AWAY, ONLINE_STATUS.OFFLINE];

    // Cambia stato di un utente random (non l'utente corrente)
    const otherUsers = users.filter(u => u.id !== currentUserId);
    if (otherUsers.length === 0) return;

    const user = otherUsers[Math.floor(Math.random() * otherUsers.length)];
    const newStatus = statuses[Math.floor(Math.random() * statuses.length)];

    await this.updateUserStatus(user.id, newStatus);
  }

  // Simula indicatori di digitazione
  async simulateTypingIndicators() {
    const rooms = await this.getChatRooms();
    const users = await this.getUsers();
    const currentUserId = await storageService.getCurrentUserId();

    if (rooms.length === 0) return;

    // Scegli stanza random
    const room = rooms[Math.floor(Math.random() * rooms.length)];

    // Scegli utente random
    const otherUsers = users.filter(u => u.id !== currentUserId && room.participants.includes(u.id));
    if (otherUsers.length === 0) return;

    const user = otherUsers[Math.floor(Math.random() * otherUsers.length)];

    // Mostra indicatore
    this.showTypingIndicator(room.id, user.id, user.username);
  }

  // Pulisci timer
  cleanup() {
    this.timers.forEach(timer => {
      clearTimeout(timer);
      clearInterval(timer);
    });
    this.timers = [];
  }

  // Cancella chat
  async clearChat(roomId) {
    await storageService.clearChatRoom(roomId);
  }

  // Crea nuovo gruppo
  async createGroup(name, participants) {
    return await this.createChatRoom(name, 'group', participants);
  }

  // Crea chat diretta
  async createDirectChat(targetUserId, currentUserId) {
    const users = await this.getUsers();
    const targetUser = users.find(u => u.id === targetUserId);

    if (!targetUser) return null;

    // Verifica se esiste già una chat diretta
    const rooms = await this.getChatRooms();
    const existingRoom = rooms.find(r =>
      r.type === 'direct' &&
      r.participants.includes(currentUserId) &&
      r.participants.includes(targetUserId)
    );

    if (existingRoom) return existingRoom;

    return await this.createChatRoom(
      targetUser.username,
      'direct',
      [currentUserId, targetUserId]
    );
  }
}

export default new ChatService();

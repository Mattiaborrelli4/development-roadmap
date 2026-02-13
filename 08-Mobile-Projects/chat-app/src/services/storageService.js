import AsyncStorage from '@react-native-async-storage/async-storage';
import {
  STORAGE_KEYS,
  MOCK_USERS,
  MOCK_CHAT_ROOMS,
  MOCK_MESSAGES,
  CURRENT_USER_ID
} from '../utils/constants';

class StorageService {
  // Inizializza i dati di default
  async initializeData() {
    try {
      // Verifica se i dati esistono già
      const existingUsers = await this.getUsers();
      const existingRooms = await this.getChatRooms();
      const existingMessages = await this.getMessages();

      // Se non esistono, carica i dati mock
      if (!existingUsers || existingUsers.length === 0) {
        await this.saveData(STORAGE_KEYS.USERS, MOCK_USERS);
      }

      if (!existingRooms || existingRooms.length === 0) {
        await this.saveData(STORAGE_KEYS.ROOMS, MOCK_CHAT_ROOMS);
      }

      if (!existingMessages || Object.keys(existingMessages).length === 0) {
        await this.saveData(STORAGE_KEYS.MESSAGES, MOCK_MESSAGES);
      }

      await this.saveData(STORAGE_KEYS.CURRENT_USER, CURRENT_USER_ID);

      return true;
    } catch (error) {
      console.error('Errore inizializzazione dati:', error);
      return false;
    }
  }

  // Salva dati in AsyncStorage
  async saveData(key, data) {
    try {
      await AsyncStorage.setItem(key, JSON.stringify(data));
      return true;
    } catch (error) {
      console.error(`Errore salvataggio ${key}:`, error);
      return false;
    }
  }

  // Recupera dati da AsyncStorage
  async getData(key) {
    try {
      const value = await AsyncStorage.getItem(key);
      return value ? JSON.parse(value) : null;
    } catch (error) {
      console.error(`Errore recupero ${key}:`, error);
      return null;
    }
  }

  // Utenti
  async getUsers() {
    return await this.getData(STORAGE_KEYS.USERS);
  }

  async getUserById(userId) {
    const users = await this.getUsers();
    return users ? users.find(u => u.id === userId) : null;
  }

  async updateUser(userId, updates) {
    try {
      const users = await this.getUsers();
      if (!users) return false;

      const updatedUsers = users.map(user =>
        user.id === userId ? { ...user, ...updates } : user
      );

      await this.saveData(STORAGE_KEYS.USERS, updatedUsers);
      return true;
    } catch (error) {
      console.error('Errore aggiornamento utente:', error);
      return false;
    }
  }

  // Stanze di chat
  async getChatRooms() {
    return await this.getData(STORAGE_KEYS.ROOMS);
  }

  async getChatRoomById(roomId) {
    const rooms = await this.getChatRooms();
    return rooms ? rooms.find(r => r.id === roomId) : null;
  }

  async updateChatRoom(roomId, updates) {
    try {
      const rooms = await this.getChatRooms();
      if (!rooms) return false;

      const updatedRooms = rooms.map(room =>
        room.id === roomId ? { ...room, ...updates } : room
      );

      await this.saveData(STORAGE_KEYS.ROOMS, updatedRooms);
      return true;
    } catch (error) {
      console.error('Errore aggiornamento stanza:', error);
      return false;
    }
  }

  async createChatRoom(room) {
    try {
      const rooms = await this.getChatRooms();
      const newRooms = rooms ? [...rooms, room] : [room];

      await this.saveData(STORAGE_KEYS.ROOMS, newRooms);
      return true;
    } catch (error) {
      console.error('Errore creazione stanza:', error);
      return false;
    }
  }

  // Messaggi
  async getMessages() {
    return await this.getData(STORAGE_KEYS.MESSAGES);
  }

  async getMessagesByRoom(roomId) {
    const messages = await this.getMessages();
    return messages && messages[roomId] ? messages[roomId] : [];
  }

  async addMessage(message) {
    try {
      const messages = await this.getMessages();
      const roomId = message.roomId;

      if (!messages[roomId]) {
        messages[roomId] = [];
      }

      messages[roomId].push(message);

      await this.saveData(STORAGE_KEYS.MESSAGES, messages);
      return true;
    } catch (error) {
      console.error('Errore aggiunta messaggio:', error);
      return false;
    }
  }

  async updateMessage(roomId, messageId, updates) {
    try {
      const messages = await this.getMessages();

      if (!messages[roomId]) return false;

      messages[roomId] = messages[roomId].map(msg =>
        msg.id === messageId ? { ...msg, ...updates } : msg
      );

      await this.saveData(STORAGE_KEYS.MESSAGES, messages);
      return true;
    } catch (error) {
      console.error('Errore aggiornamento messaggio:', error);
      return false;
    }
  }

  async markMessagesAsRead(roomId, userId) {
    try {
      const messages = await this.getMessages();

      if (!messages[roomId]) return false;

      messages[roomId] = messages[roomId].map(msg => {
        if (!msg.readBy) msg.readBy = [];
        if (!msg.readBy.includes(userId)) {
          msg.readBy.push(userId);
        }
        msg.read = true;
        return msg;
      });

      await this.saveData(STORAGE_KEYS.MESSAGES, messages);
      return true;
    } catch (error) {
      console.error('Errore marcatura letti:', error);
      return false;
    }
  }

  async clearChatRoom(roomId) {
    try {
      const messages = await this.getMessages();
      messages[roomId] = [];
      await this.saveData(STORAGE_KEYS.MESSAGES, messages);
      return true;
    } catch (error) {
      console.error('Errore pulizia stanza:', error);
      return false;
    }
  }

  // Utente corrente
  async getCurrentUserId() {
    return await this.getData(STORAGE_KEYS.CURRENT_USER);
  }

  // Pulisci tutti i dati (per reset)
  async clearAllData() {
    try {
      await AsyncStorage.clear();
      return true;
    } catch (error) {
      console.error('Errore pulizia dati:', error);
      return false;
    }
  }
}

export default new StorageService();

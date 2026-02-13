import {Emitter} from 'react-native-modules';
import storageService from './storageService';

class SyncService {
  constructor() {
    this.syncInProgress = false;
    this.lastSyncTime = null;
    this.listeners = [];
  }

  // Simula la sincronizzazione con un server
  async sync() {
    if (this.syncInProgress) {
      return {success: false, message: 'Sincronizzazione in corso...'};
    }

    this.syncInProgress = true;

    try {
      // Simula un delay di rete
      await this.delay(1000);

      // Recupera i dati locali
      const lists = await storageService.getLists();
      const items = await storageService.getItems();

      // Simula la sincronizzazione
      console.log('Sincronizzazione...', {lists: lists.length, items: items.length});

      this.lastSyncTime = new Date().toISOString();

      // Notifica i listener
      this.notifyListeners('sync', {
        success: true,
        timestamp: this.lastSyncTime,
        lists: lists.length,
        items: items.length,
      });

      return {
        success: true,
        message: 'Sincronizzato con successo',
        timestamp: this.lastSyncTime,
      };
    } catch (error) {
      console.error('Errore di sincronizzazione:', error);
      return {
        success: false,
        message: 'Errore di sincronizzazione',
      };
    } finally {
      this.syncInProgress = false;
    }
  }

  // Simula la condivisione di una lista
  async shareList(listId, email) {
    try {
      await this.delay(500);

      // Recupera la lista
      const lists = await storageService.getLists();
      const listIndex = lists.findIndex(l => l.id === listId);

      if (listIndex === -1) {
        return {success: false, message: 'Lista non trovata'};
      }

      // Aggiorna la lista come condivisa
      lists[listIndex].shared = true;
      lists[listIndex].sharedWith = [
        ...(lists[listIndex].sharedWith || []),
        {email, addedAt: new Date().toISOString()},
      ];

      await storageService.saveLists(lists);

      // Notifica i listener
      this.notifyListeners('share', {
        listId,
        email,
        timestamp: new Date().toISOString(),
      });

      return {
        success: true,
        message: `Lista condivisa con ${email}`,
      };
    } catch (error) {
      console.error('Errore nella condivisione:', error);
      return {
        success: false,
        message: 'Errore nella condivisione',
      };
    }
  }

  // Simula l'unsubscribe da una lista
  async unshareList(listId, email) {
    try {
      await this.delay(500);

      const lists = await storageService.getLists();
      const listIndex = lists.findIndex(l => l.id === listId);

      if (listIndex === -1) {
        return {success: false, message: 'Lista non trovata'};
      }

      // Rimuovi l'email dalla lista dei condivisi
      lists[listIndex].sharedWith = lists[listIndex].sharedWith?.filter(
        u => u.email !== email
      ) || [];

      // Se non ci sono più utenti condivisi, marca come non condivisa
      if (lists[listIndex].sharedWith.length === 0) {
        lists[listIndex].shared = false;
      }

      await storageService.saveLists(lists);

      return {
        success: true,
        message: `Condivisione revocata per ${email}`,
      };
    } catch (error) {
      console.error('Errore nella revoca:', error);
      return {
        success: false,
        message: 'Errore nella revoca',
      };
    }
  }

  // Simula la ricezione di aggiornamenti da altri utenti
  simulateRemoteUpdate(listId, updateType, data) {
    this.notifyListeners('remoteUpdate', {
      listId,
      updateType,
      data,
      timestamp: new Date().toISOString(),
    });
  }

  // Listener per gli eventi di sincronizzazione
  addListener(callback) {
    this.listeners.push(callback);
    return () => {
      this.listeners = this.listeners.filter(cb => cb !== callback);
    };
  }

  notifyListeners(event, data) {
    this.listeners.forEach(callback => {
      try {
        callback(event, data);
      } catch (error) {
        console.error('Errore nel listener:', error);
      }
    });
  }

  // Stato della sincronizzazione
  getSyncStatus() {
    return {
      inProgress: this.syncInProgress,
      lastSync: this.lastSyncTime,
    };
  }

  // Utility per simulare delay
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Simula la sincronizzazione automatica periodica
  startAutoSync(interval = 60000) {
    if (this.autoSyncInterval) {
      clearInterval(this.autoSyncInterval);
    }

    this.autoSyncInterval = setInterval(() => {
      this.sync();
    }, interval);
  }

  stopAutoSync() {
    if (this.autoSyncInterval) {
      clearInterval(this.autoSyncInterval);
      this.autoSyncInterval = null;
    }
  }
}

export default new SyncService();

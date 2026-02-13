import AsyncStorage from '@react-native-async-storage/async-storage';
import {STORAGE_KEYS} from '../utils/constants';

class StorageService {
  // Lista della spesa
  async getLists() {
    try {
      const jsonValue = await AsyncStorage.getItem(STORAGE_KEYS.LISTS);
      return jsonValue != null ? JSON.parse(jsonValue) : [];
    } catch (e) {
      console.error('Errore nel recupero delle liste:', e);
      return [];
    }
  }

  async saveLists(lists) {
    try {
      const jsonValue = JSON.stringify(lists);
      await AsyncStorage.setItem(STORAGE_KEYS.LISTS, jsonValue);
      return true;
    } catch (e) {
      console.error('Errore nel salvataggio delle liste:', e);
      return false;
    }
  }

  async addList(list) {
    const lists = await this.getLists();
    lists.push(list);
    return await this.saveLists(lists);
  }

  async updateList(listId, updates) {
    const lists = await this.getLists();
    const index = lists.findIndex(list => list.id === listId);
    if (index !== -1) {
      lists[index] = {...lists[index], ...updates};
      return await this.saveLists(lists);
    }
    return false;
  }

  async deleteList(listId) {
    const lists = await this.getLists();
    const filtered = lists.filter(list => list.id !== listId);

    // Elimina anche tutti gli elementi della lista
    await this.deleteItemsByListId(listId);

    return await this.saveLists(filtered);
  }

  // Elementi della lista
  async getItems() {
    try {
      const jsonValue = await AsyncStorage.getItem(STORAGE_KEYS.ITEMS);
      return jsonValue != null ? JSON.parse(jsonValue) : [];
    } catch (e) {
      console.error('Errore nel recupero degli elementi:', e);
      return [];
    }
  }

  async saveItems(items) {
    try {
      const jsonValue = JSON.stringify(items);
      await AsyncStorage.setItem(STORAGE_KEYS.ITEMS, jsonValue);
      return true;
    } catch (e) {
      console.error('Errore nel salvataggio degli elementi:', e);
      return false;
    }
  }

  async getItemsByListId(listId) {
    const items = await this.getItems();
    return items.filter(item => item.listId === listId);
  }

  async addItem(item) {
    const items = await this.getItems();
    items.push(item);
    return await this.saveItems(items);
  }

  async updateItem(itemId, updates) {
    const items = await this.getItems();
    const index = items.findIndex(item => item.id === itemId);
    if (index !== -1) {
      items[index] = {...items[index], ...updates};
      return await this.saveItems(items);
    }
    return false;
  }

  async deleteItem(itemId) {
    const items = await this.getItems();
    const filtered = items.filter(item => item.id !== itemId);
    return await this.saveItems(filtered);
  }

  async deleteItemsByListId(listId) {
    const items = await this.getItems();
    const filtered = items.filter(item => item.listId !== listId);
    return await this.saveItems(filtered);
  }

  async clearBoughtItems(listId) {
    const items = await this.getItems();
    const filtered = items.filter(item => !(item.listId === listId && item.bought));
    return await this.saveItems(filtered);
  }

  // Impostazioni
  async getSettings() {
    try {
      const jsonValue = await AsyncStorage.getItem(STORAGE_KEYS.SETTINGS);
      return jsonValue != null ? JSON.parse(jsonValue) : {
        theme: 'light',
        notifications: true,
        autoSort: true,
      };
    } catch (e) {
      console.error('Errore nel recupero delle impostazioni:', e);
      return {
        theme: 'light',
        notifications: true,
        autoSort: true,
      };
    }
  }

  async saveSettings(settings) {
    try {
      const jsonValue = JSON.stringify(settings);
      await AsyncStorage.setItem(STORAGE_KEYS.SETTINGS, jsonValue);
      return true;
    } catch (e) {
      console.error('Errore nel salvataggio delle impostazioni:', e);
      return false;
    }
  }

  // Tema
  async getTheme() {
    try {
      const value = await AsyncStorage.getItem(STORAGE_KEYS.THEME);
      return value || 'light';
    } catch (e) {
      console.error('Errore nel recupero del tema:', e);
      return 'light';
    }
  }

  async setTheme(theme) {
    try {
      await AsyncStorage.setItem(STORAGE_KEYS.THEME, theme);
      return true;
    } catch (e) {
      console.error('Errore nel salvataggio del tema:', e);
      return false;
    }
  }

  // Utility
  async clearAll() {
    try {
      await AsyncStorage.clear();
      return true;
    } catch (e) {
      console.error('Errore nella pulizia dei dati:', e);
      return false;
    }
  }

  // Statistiche
  async getStatistics() {
    const lists = await this.getLists();
    const items = await this.getItems();

    const totalLists = lists.length;
    const totalItems = items.length;
    const boughtItems = items.filter(item => item.bought).length;
    const sharedLists = lists.filter(list => list.shared).length;

    return {
      totalLists,
      totalItems,
      boughtItems,
      sharedLists,
      completionRate: totalItems > 0 ? (boughtItems / totalItems * 100).toFixed(1) : 0,
    };
  }
}

export default new StorageService();

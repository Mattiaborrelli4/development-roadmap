import AsyncStorage from '@react-native-async-storage/async-storage';

const KEYS = {
  PHOTOS: '@photo_gallery:photos',
  ALBUMS: '@photo_gallery:albums',
  SETTINGS: '@photo_gallery:settings',
};

export const storageService = {
  // Photo Operations
  async savePhotos(photos) {
    try {
      await AsyncStorage.setItem(KEYS.PHOTOS, JSON.stringify(photos));
    } catch (error) {
      console.error('Errore nel salvare le foto:', error);
      throw error;
    }
  },

  async getPhotos() {
    try {
      const photosJson = await AsyncStorage.getItem(KEYS.PHOTOS);
      return photosJson ? JSON.parse(photosJson) : [];
    } catch (error) {
      console.error('Errore nel recuperare le foto:', error);
      return [];
    }
  },

  // Album Operations
  async saveAlbums(albums) {
    try {
      await AsyncStorage.setItem(KEYS.ALBUMS, JSON.stringify(albums));
    } catch (error) {
      console.error('Errore nel salvare gli album:', error);
      throw error;
    }
  },

  async getAlbums() {
    try {
      const albumsJson = await AsyncStorage.getItem(KEYS.ALBUMS);
      return albumsJson ? JSON.parse(albumsJson) : [];
    } catch (error) {
      console.error('Errore nel recuperare gli album:', error);
      return [];
    }
  },

  // Settings Operations
  async saveSettings(settings) {
    try {
      await AsyncStorage.setItem(KEYS.SETTINGS, JSON.stringify(settings));
    } catch (error) {
      console.error('Errore nel salvare le impostazioni:', error);
      throw error;
    }
  },

  async getSettings() {
    try {
      const settingsJson = await AsyncStorage.getItem(KEYS.SETTINGS);
      return settingsJson ? JSON.parse(settingsJson) : {
        viewMode: 'grid',
        sortBy: 'date',
        defaultFilter: 'none',
      };
    } catch (error) {
      console.error('Errore nel recuperare le impostazioni:', error);
      return {
        viewMode: 'grid',
        sortBy: 'date',
        defaultFilter: 'none',
      };
    }
  },

  // Clear all data
  async clearAll() {
    try {
      await AsyncStorage.multiRemove([KEYS.PHOTOS, KEYS.ALBUMS, KEYS.SETTINGS]);
    } catch (error) {
      console.error('Errore nel cancellare i dati:', error);
      throw error;
    }
  },
};

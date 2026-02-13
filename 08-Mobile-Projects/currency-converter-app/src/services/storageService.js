import AsyncStorage from '@react-native-async-storage/async-storage';
import { STORAGE_KEYS, MAX_HISTORY_ITEMS } from '../utils/constants';

/**
 * Servizio per la gestione del localStorage
 */

// Salva i preferiti
export const saveFavorites = async (favorites) => {
  try {
    await AsyncStorage.setItem(STORAGE_KEYS.FAVORITES, JSON.stringify(favorites));
  } catch (error) {
    console.error('Errore nel salvataggio dei preferiti:', error);
  }
};

// Carica i preferiti
export const loadFavorites = async () => {
  try {
    const data = await AsyncStorage.getItem(STORAGE_KEYS.FAVORITES);
    return data ? JSON.parse(data) : [];
  } catch (error) {
    console.error('Errore nel caricamento dei preferiti:', error);
    return [];
  }
};

// Aggiungi un preferito
export const addFavorite = async (from, to) => {
  try {
    const favorites = await loadFavorites();
    const newFavorite = { from, to };

    // Verifica se già esiste
    const exists = favorites.some(
      (fav) => fav.from === from && fav.to === to
    );

    if (!exists) {
      favorites.push(newFavorite);
      await saveFavorites(favorites);
    }

    return favorites;
  } catch (error) {
    console.error('Errore nell\'aggiunta dei preferiti:', error);
    return [];
  }
};

// Rimuovi un preferito
export const removeFavorite = async (from, to) => {
  try {
    const favorites = await loadFavorites();
    const filtered = favorites.filter(
      (fav) => !(fav.from === from && fav.to === to)
    );
    await saveFavorites(filtered);
    return filtered;
  } catch (error) {
    console.error('Errore nella rimozione dei preferiti:', error);
    return [];
  }
};

// Salva la cronologia
export const saveHistory = async (history) => {
  try {
    // Mantieni solo gli ultimi MAX_HISTORY_ITEMS elementi
    const trimmed = history.slice(-MAX_HISTORY_ITEMS);
    await AsyncStorage.setItem(STORAGE_KEYS.HISTORY, JSON.stringify(trimmed));
  } catch (error) {
    console.error('Errore nel salvataggio della cronologia:', error);
  }
};

// Carica la cronologia
export const loadHistory = async () => {
  try {
    const data = await AsyncStorage.getItem(STORAGE_KEYS.HISTORY);
    return data ? JSON.parse(data) : [];
  } catch (error) {
    console.error('Errore nel caricamento della cronologia:', error);
    return [];
  }
};

// Aggiungi una conversione alla cronologia
export const addToHistory = async (conversion) => {
  try {
    const history = await loadHistory();
    history.push({
      ...conversion,
      timestamp: new Date().toISOString(),
    });
    await saveHistory(history);
    return history;
  } catch (error) {
    console.error('Errore nell\'aggiunta alla cronologia:', error);
    return [];
  }
};

// Pulisci la cronologia
export const clearHistory = async () => {
  try {
    await AsyncStorage.removeItem(STORAGE_KEYS.HISTORY);
    return [];
  } catch (error) {
    console.error('Errore nella pulizia della cronologia:', error);
    return [];
  }
};

// Salva i tassi di cambio in cache
export const cacheRates = async (rates) => {
  try {
    await AsyncStorage.setItem(STORAGE_KEYS.RATES_CACHE, JSON.stringify(rates));
    await AsyncStorage.setItem(STORAGE_KEYS.LAST_UPDATE, new Date().toISOString());
  } catch (error) {
    console.error('Errore nel salvataggio dei tassi:', error);
  }
};

// Carica i tassi di cambio dalla cache
export const loadCachedRates = async () => {
  try {
    const data = await AsyncStorage.getItem(STORAGE_KEYS.RATES_CACHE);
    return data ? JSON.parse(data) : null;
  } catch (error) {
    console.error('Errore nel caricamento dei tassi cached:', error);
    return null;
  }
};

// Ottieni l'ultimo aggiornamento
export const getLastUpdate = async () => {
  try {
    const data = await AsyncStorage.getItem(STORAGE_KEYS.LAST_UPDATE);
    return data ? new Date(data) : null;
  } catch (error) {
    console.error('Errore nel caricamento dell\'ultimo aggiornamento:', error);
    return null;
  }
};

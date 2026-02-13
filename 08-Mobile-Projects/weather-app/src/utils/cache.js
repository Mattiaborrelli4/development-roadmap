import AsyncStorage from '@react-native-async-storage/async-storage';

const CACHE_KEY_PREFIX = 'weather_cache_';
const CACHE_EXPIRY = 30 * 60 * 1000; // 30 minuti in millisecondi

/**
 * Salva i dati meteo nella cache
 * @param {number} lat - Latitudine
 * @param {number} lon - Longitudine
 * @param {Object} data - Dati meteo da salvare
 */
export const cacheWeatherData = async (lat, lon, data) => {
  try {
    const key = `${CACHE_KEY_PREFIX}${lat}_${lon}`;
    const cacheData = {
      data,
      timestamp: Date.now(),
    };

    await AsyncStorage.setItem(key, JSON.stringify(cacheData));
  } catch (error) {
    console.error('Errore nel salvare i dati in cache:', error);
  }
};

/**
 * Recupera i dati meteo dalla cache
 * @param {number} lat - Latitudine
 * @param {number} lon - Longitudine
 * @returns {Promise<Object|null>} Dati meteo o null se non presenti o scaduti
 */
export const getCachedWeatherData = async (lat, lon) => {
  try {
    const key = `${CACHE_KEY_PREFIX}${lat}_${lon}`;
    const cached = await AsyncStorage.getItem(key);

    if (!cached) {
      return null;
    }

    const { data, timestamp } = JSON.parse(cached);
    const isExpired = Date.now() - timestamp > CACHE_EXPIRY;

    if (isExpired) {
      // Rimuovi i dati scaduti
      await AsyncStorage.removeItem(key);
      return null;
    }

    return data;
  } catch (error) {
    console.error('Errore nel recuperare i dati dalla cache:', error);
    return null;
  }
};

/**
 * Pulisce tutti i dati meteo in cache
 */
export const clearWeatherCache = async () => {
  try {
    const keys = await AsyncStorage.getAllKeys();
    const weatherKeys = keys.filter((key) => key.startsWith(CACHE_KEY_PREFIX));

    await AsyncStorage.multiRemove(weatherKeys);
  } catch (error) {
    console.error('Errore nel pulire la cache:', error);
  }
};

/**
 * Salva l'ultima città cercata
 * @param {string} cityName - Nome della città
 */
export const cacheLastCity = async (cityName) => {
  try {
    await AsyncStorage.setItem('last_city', cityName);
  } catch (error) {
    console.error('Errore nel salvare l\'ultima città:', error);
  }
};

/**
 * Recupera l'ultima città cercata
 * @returns {Promise<string|null>} Nome dell'ultima città o null
 */
export const getLastCity = async () => {
  try {
    const city = await AsyncStorage.getItem('last_city');
    return city;
  } catch (error) {
    console.error('Errore nel recuperare l\'ultima città:', error);
    return null;
  }
};

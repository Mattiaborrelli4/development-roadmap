import * as Location from 'expo-location';

/**
 * Richiedi i permessi di localizzazione
 * @returns {Promise<string>} Stato dei permessi
 */
export const requestLocationPermission = async () => {
  try {
    const { status } = await Location.requestForegroundPermissionsAsync();
    return status;
  } catch (error) {
    console.error('Errore nel richiedere i permessi:', error);
    throw new Error('Impossibile ottenere i permessi di localizzazione');
  }
};

/**
 * Ottieni la posizione corrente
 * @returns {Promise<Object>} Coordinate GPS
 */
export const getCurrentLocation = async () => {
  try {
    const { status } = await Location.requestForegroundPermissionsAsync();

    if (status !== 'granted') {
      throw new Error('Permesso di localizzazione negato');
    }

    const location = await Location.getCurrentPositionAsync({
      accuracy: Location.Accuracy.Balanced,
    });

    return {
      latitude: location.coords.latitude,
      longitude: location.coords.longitude,
    };
  } catch (error) {
    console.error('Errore nel ottenere la posizione:', error);
    throw error;
  }
};

/**
 * Ottieni il nome della città dalle coordinate (reverse geocoding)
 * @param {number} lat - Latitudine
 * @param {number} lon - Longitudine
 * @returns {Promise<string>} Nome della città
 */
export const getCityFromCoords = async (lat, lon) => {
  try {
    const results = await Location.reverseGeocodeAsync({ latitude: lat, longitude: lon });

    if (results && results.length > 0) {
      const { city, street, district } = results[0];
      return city || district || street || 'Posizione sconosciuta';
    }

    return 'Posizione sconosciuta';
  } catch (error) {
    console.error('Errore nel reverse geocoding:', error);
    return 'Posizione sconosciuta';
  }
};

/**
 * Calcola la distanza tra due coordinate (in km)
 * @param {number} lat1 - Latitudine primo punto
 * @param {number} lon1 - Longitudine primo punto
 * @param {number} lat2 - Latitudine secondo punto
 * @param {number} lon2 - Longitudine secondo punto
 * @returns {number} Distanza in km
 */
export const calculateDistance = (lat1, lon1, lat2, lon2) => {
  const R = 6371; // Raggio della Terra in km
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);

  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(toRad(lat1)) *
    Math.cos(toRad(lat2)) *
    Math.sin(dLon / 2) *
    Math.sin(dLon / 2);

  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
};

const toRad = (degrees) => {
  return degrees * (Math.PI / 180);
};

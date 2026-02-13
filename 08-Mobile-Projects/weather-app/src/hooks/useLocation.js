import { useState, useCallback } from 'react';
import * as Location from 'expo-location';
import {
  requestLocationPermission,
  getCurrentLocation,
  getCityFromCoords,
} from '../services/locationService';

export const useLocation = () => {
  const [location, setLocation] = useState(null);
  const [city, setCity] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [permissionStatus, setPermissionStatus] = useState(null);

  /**
   * Richiedi i permessi di localizzazione
   */
  const requestPermission = useCallback(async () => {
    try {
      const status = await requestLocationPermission();
      setPermissionStatus(status);
      return status;
    } catch (err) {
      setError(err.message);
      setPermissionStatus('denied');
      return 'denied';
    }
  }, []);

  /**
   * Ottieni la posizione corrente
   */
  const getCurrentPosition = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      // Prima verifica i permessi
      let status = permissionStatus;
      if (!status) {
        status = await requestPermission();
      }

      if (status !== 'granted') {
        throw new Error('Permesso di localizzazione negato');
      }

      // Ottieni le coordinate
      const coords = await getCurrentLocation();
      setLocation(coords);

      // Ottieni il nome della città
      const cityName = await getCityFromCoords(coords.latitude, coords.longitude);
      setCity(cityName);

      setLoading(false);
      return { ...coords, city: cityName };
    } catch (err) {
      setError(err.message);
      setLoading(false);
      throw err;
    }
  }, [permissionStatus, requestPermission]);

  /**
   * Watch per i cambiamenti di posizione
   */
  const watchPosition = useCallback((callback) => {
    let subscription = null;

    const startWatching = async () => {
      try {
        const status = await requestPermission();
        if (status === 'granted') {
          subscription = await Location.watchPositionAsync(
            {
              accuracy: Location.Accuracy.Balanced,
              distanceInterval: 1000, // Aggiorna ogni km
            },
            (newLocation) => {
              const coords = {
                latitude: newLocation.coords.latitude,
                longitude: newLocation.coords.longitude,
              };
              setLocation(coords);

              // Ottieni anche il nome della città
              getCityFromCoords(coords.latitude, coords.longitude)
                .then((cityName) => {
                  setCity(cityName);
                  callback({ ...coords, city: cityName });
                })
                .catch(() => {
                  callback(coords);
                });
            }
          );
        }
      } catch (err) {
        setError(err.message);
      }
    };

    startWatching();

    // Funzione di cleanup
    return () => {
      if (subscription) {
        subscription.remove();
      }
    };
  }, [requestPermission]);

  /**
   * Reset dello stato
   */
  const reset = useCallback(() => {
    setLocation(null);
    setCity(null);
    setError(null);
    setLoading(false);
    setPermissionStatus(null);
  }, []);

  return {
    location,
    city,
    loading,
    error,
    permissionStatus,
    requestPermission,
    getCurrentPosition,
    watchPosition,
    reset,
  };
};

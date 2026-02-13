import { useState, useCallback } from 'react';
import {
  getCompleteWeather,
  getCurrentWeatherByCity,
  getWeatherGradient,
} from '../services/weatherAPI';
import { cacheWeatherData, getCachedWeatherData } from '../utils/cache';

export const useWeather = () => {
  const [weather, setWeather] = useState(null);
  const [forecast, setForecast] = useState([]);
  const [location, setLocation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isRefreshing, setIsRefreshing] = useState(false);

  /**
   * Carica i dati meteo dalle coordinate
   */
  const loadWeatherByCoords = useCallback(async (lat, lon, useCache = true) => {
    setLoading(true);
    setError(null);

    try {
      // Tenta di recuperare dalla cache
      if (useCache) {
        const cached = await getCachedWeatherData(lat, lon);
        if (cached) {
          setWeather(cached.current);
          setForecast(cached.forecast);
          setLocation(cached.location);
        }
      }

      // Recupera i dati aggiornati
      const data = await getCompleteWeather(lat, lon);

      setWeather(data.current);
      setForecast(data.forecast);
      setLocation(data.location);

      // Salva nella cache
      await cacheWeatherData(lat, lon, data);

      setLoading(false);
      setIsRefreshing(false);
      return data;
    } catch (err) {
      setError(err.message);
      setLoading(false);
      setIsRefreshing(false);
      throw err;
    }
  }, []);

  /**
   * Carica i dati meteo per una città
   */
  const loadWeatherByCity = useCallback(async (cityName) => {
    setLoading(true);
    setError(null);

    try {
      const data = await getCompleteWeather(
        data.location.lat,
        data.location.lon
      );

      setWeather(data.current);
      setForecast(data.forecast);
      setLocation(data.location);

      // Salva nella cache
      await cacheWeatherData(data.location.lat, data.location.lon, data);

      setLoading(false);
      return data;
    } catch (err) {
      setError(err.message);
      setLoading(false);
      throw err;
    }
  }, []);

  /**
   * Refresh dei dati meteo
   */
  const refreshWeather = useCallback(async () => {
    if (!location) return;

    setIsRefreshing(true);
    try {
      await loadWeatherByCoords(location.lat, location.lon, false);
    } catch (err) {
      // Errore già gestito in loadWeatherByCoords
    }
  }, [location, loadWeatherByCoords]);

  /**
   * Ottieni il gradiente di sfondo in base al meteo
   */
  const getGradient = useCallback(() => {
    if (!weather) return ['#4facfe', '#00f2fe'];
    return getWeatherGradient(weather.condition);
  }, [weather]);

  /**
   * Reset dello stato
   */
  const reset = useCallback(() => {
    setWeather(null);
    setForecast([]);
    setLocation(null);
    setError(null);
    setLoading(false);
    setIsRefreshing(false);
  }, []);

  return {
    weather,
    forecast,
    location,
    loading,
    error,
    isRefreshing,
    loadWeatherByCoords,
    loadWeatherByCity,
    refreshWeather,
    getGradient,
    reset,
  };
};

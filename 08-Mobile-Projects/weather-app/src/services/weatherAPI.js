import axios from 'axios';

// Sostituisci con la tua API key di OpenWeatherMap
const API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY';
const BASE_URL = 'https://api.openweathermap.org/data/2.5';

/**
 * Ottieni il meteo attuale per una città
 * @param {string} cityName - Nome della città
 * @returns {Promise<Object>} Dati meteo
 */
export const getCurrentWeatherByCity = async (cityName) => {
  try {
    const response = await axios.get(
      `${BASE_URL}/weather?q=${cityName}&appid=${API_KEY}&units=metric&lang=it`
    );
    return response.data;
  } catch (error) {
    throw handleError(error);
  }
};

/**
 * Ottieni il meteo attuale per coordinate
 * @param {number} lat - Latitudine
 * @param {number} lon - Longitudine
 * @returns {Promise<Object>} Dati meteo
 */
export const getCurrentWeatherByCoords = async (lat, lon) => {
  try {
    const response = await axios.get(
      `${BASE_URL}/weather?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=metric&lang=it`
    );
    return response.data;
  } catch (error) {
    throw handleError(error);
  }
};

/**
 * Ottieni le previsioni a 5 giorni
 * @param {number} lat - Latitudine
 * @param {number} lon - Longitudine
 * @returns {Promise<Object>} Dati previsioni
 */
export const getForecast = async (lat, lon) => {
  try {
    const response = await axios.get(
      `${BASE_URL}/forecast?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=metric&lang=it`
    );
    return response.data;
  } catch (error) {
    throw handleError(error);
  }
};

/**
 * Ottieni il meteo attuale e le previsioni
 * @param {number} lat - Latitudine
 * @param {number} lon - Longitudine
 * @returns {Promise<Object>} Dati meteo completi
 */
export const getCompleteWeather = async (lat, lon) => {
  try {
    const [current, forecast] = await Promise.all([
      getCurrentWeatherByCoords(lat, lon),
      getForecast(lat, lon)
    ]);

    return {
      current: formatCurrentWeather(current),
      forecast: formatForecast(forecast),
      location: {
        name: current.name,
        country: current.sys.country,
        lat: current.coord.lat,
        lon: current.coord.lon
      }
    };
  } catch (error) {
    throw handleError(error);
  }
};

/**
 * Formatta i dati meteo attuali
 */
const formatCurrentWeather = (data) => {
  return {
    temp: Math.round(data.main.temp),
    feels_like: Math.round(data.main.feels_like),
    humidity: data.main.humidity,
    wind_speed: data.wind.speed,
    wind_deg: data.wind.deg,
    condition: data.weather[0].main,
    description: data.weather[0].description,
    icon: data.weather[0].icon,
    temp_min: Math.round(data.main.temp_min),
    temp_max: Math.round(data.main.temp_max),
    sunrise: data.sys.sunrise,
    sunset: data.sys.sunset,
    visibility: data.visibility
  };
};

/**
 * Formatta le previsioni a 5 giorni
 */
const formatForecast = (data) => {
  // Raggruppa per giorno e prendi un dato per giorno
  const dailyData = {};

  data.list.forEach((item) => {
    const date = new Date(item.dt * 1000);
    const dateKey = date.toDateString();

    if (!dailyData[dateKey]) {
      dailyData[dateKey] = {
        date: dateKey,
        timestamp: item.dt,
        temp_min: item.main.temp_min,
        temp_max: item.main.temp_max,
        condition: item.weather[0].main,
        description: item.weather[0].description,
        icon: item.weather[0].icon,
        humidity: item.main.humidity,
        wind_speed: item.wind.speed
      };
    } else {
      dailyData[dateKey].temp_min = Math.min(dailyData[dateKey].temp_min, item.main.temp_min);
      dailyData[dateKey].temp_max = Math.max(dailyData[dateKey].temp_max, item.main.temp_max);
    }
  });

  return Object.values(dailyData)
    .slice(0, 5)
    .map(day => ({
      ...day,
      temp_min: Math.round(day.temp_min),
      temp_max: Math.round(day.temp_max)
    }));
};

/**
 * Gestisci gli errori API
 */
const handleError = (error) => {
  if (error.response) {
    switch (error.response.status) {
      case 404:
        return new Error('Città non trovata');
      case 401:
        return new Error('API key non valida');
      case 429:
        return new Error('Troppe richieste, riprova più tardi');
      default:
        return new Error('Errore nel recupero dei dati meteo');
    }
  } else if (error.request) {
    return new Error('Nessuna risposta dal server. Controlla la tua connessione.');
  } else {
    return new Error('Errore di configurazione');
  }
};

/**
 * Ottieni l'icona meteo appropriata
 */
export const getWeatherIcon = (iconCode) => {
  return `https://openweathermap.org/img/wn/${iconCode}@4x.png`;
};

/**
 * Mappa le condizioni meteo ai colori di sfondo
 */
export const getWeatherGradient = (condition) => {
  const gradients = {
    'Clear': ['#4facfe', '#00f2fe'],
    'Clouds': ['#bdc3c7', '#2c3e50'],
    'Rain': ['#5b86e5', '#36d1dc'],
    'Drizzle': ['#89f7fe', '#66a6ff'],
    'Thunderstorm': ['#373b44', '#4286f4'],
    'Snow': ['#e6e9f0', '#eef1f5'],
    'Mist': ['#757F9A', '#D7DDE8'],
    'Fog': ['#757F9A', '#D7DDE8'],
    'Haze': ['#757F9A', '#D7DDE8'],
    'default': ['#4facfe', '#00f2fe']
  };

  return gradients[condition] || gradients['default'];
};

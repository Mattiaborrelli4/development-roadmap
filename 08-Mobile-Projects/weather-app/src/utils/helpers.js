/**
 * Formatta la data in italiano
 * @param {number} timestamp - Timestamp Unix
 * @param {string} format - Formato desiderato ('date', 'time', 'datetime', 'day')
 * @returns {string} Data formattata
 */
export const formatDate = (timestamp, format = 'datetime') => {
  const date = new Date(timestamp * 1000);

  const options = {
    date: { weekday: 'long', day: 'numeric', month: 'long' },
    time: { hour: '2-digit', minute: '2-digit' },
    datetime: {
      weekday: 'long',
      day: 'numeric',
      month: 'long',
      hour: '2-digit',
      minute: '2-digit',
    },
    day: { weekday: 'short', day: 'numeric' },
    short: { day: 'numeric', month: 'short' },
  };

  return date.toLocaleDateString('it-IT', options[format] || options.datetime);
};

/**
 * Formatta l'ora dell'alba/tramonto
 * @param {number} timestamp - Timestamp Unix
 * @returns {string} Ora formattata
 */
export const formatSunTime = (timestamp) => {
  const date = new Date(timestamp * 1000);
  return date.toLocaleTimeString('it-IT', {
    hour: '2-digit',
    minute: '2-digit',
  });
};

/**
 * Formatta la velocità del vento
 * @param {number} speed - Velocità in m/s
 * @returns {string} Velocità formattata in km/h
 */
export const formatWindSpeed = (speed) => {
  const kmh = Math.round(speed * 3.6);
  return `${kmh} km/h`;
};

/**
 * Ottieni la direzione del vento come testo
 * @param {number} degrees - Gradi della direzione
 * @returns {string} Direzione del vento
 */
export const getWindDirection = (degrees) => {
  const directions = ['N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO'];
  const index = Math.round(degrees / 45) % 8;
  return directions[index];
};

/**
 * Formatta la visibilità
 * @param {number} visibility - Visibilità in metri
 * @returns {string} Visibilità formattata
 */
export const formatVisibility = (visibility) => {
  const km = (visibility / 1000).toFixed(1);
  return `${km} km`;
};

/**
 * Formatta la temperatura
 * @param {number} temp - Temperatura
 * @param {boolean} showSymbol - Se mostrare il simbolo °C
 * @returns {string} Temperatura formattata
 */
export const formatTemperature = (temp, showSymbol = true) => {
  return showSymbol ? `${temp}°C` : `${temp}°`;
};

/**
 * Traduci le condizioni meteo in italiano
 * @param {string} condition - Condizione meteo in inglese
 * @returns {string} Condizione tradotta
 */
export const translateWeatherCondition = (condition) => {
  const translations = {
    'Clear': 'Sereno',
    'Clouds': 'Nuvoloso',
    'Rain': 'Pioggia',
    'Drizzle': 'Pioggerellina',
    'Thunderstorm': 'Temporale',
    'Snow': 'Neve',
    'Mist': 'Foschia',
    'Fog': 'Nebbia',
    'Haze': 'Caligine',
    'Smoke': 'Fumo',
    'Dust': 'Polvere',
    'Sand': 'Sabbia',
    'Ash': 'Cenere',
    'Squall': 'Burrasca',
    'Tornado': 'Tornado',
  };

  return translations[condition] || condition;
};

/**
 * Calcola l'indice UV approssimativo
 * @param {number} uvIndex - Indice UV
 * @returns {Object} { value, description, color }
 */
export const getUVInfo = (uvIndex) => {
  if (uvIndex <= 2) {
    return { level: 'Basso', color: '#4CAF50' };
  } else if (uvIndex <= 5) {
    return { level: 'Moderato', color: '#FFC107' };
  } else if (uvIndex <= 7) {
    return { level: 'Alto', color: '#FF9800' };
  } else if (uvIndex <= 10) {
    return { level: 'Molto alto', color: '#FF5722' };
  } else {
    return { level: 'Estremo', color: '#F44336' };
  }
};

/**
 * Ottieni emoji per condizione meteo
 * @param {string} condition - Condizione meteo
 * @returns {string} Emoji
 */
export const getWeatherEmoji = (condition) => {
  const emojis = {
    'Clear': '☀️',
    'Clouds': '☁️',
    'Rain': '🌧️',
    'Drizzle': '🌦️',
    'Thunderstorm': '⛈️',
    'Snow': '❄️',
    'Mist': '🌫️',
    'Fog': '🌫️',
    'Haze': '🌫️',
  };

  return emojis[condition] || '🌤️';
};

/**
 * Verifica se è di giorno o di notte
 * @param {number} sunrise - Timestamp alba
 * @param {number} sunset - Timestamp tramonto
 * @param {number} current - Timestamp corrente (opzionale)
 * @returns {boolean} True se è giorno
 */
export const isDayTime = (sunrise, sunset, current = null) => {
  const now = current ? current * 1000 : Date.now();
  const rise = sunrise * 1000;
  const set = sunset * 1000;

  return now >= rise && now < set;
};

/**
 * Ottieni il nome del giorno della settimana
 * @param {number} timestamp - Timestamp Unix
 * @returns {string} Nome del giorno
 */
export const getDayName = (timestamp) => {
  const date = new Date(timestamp * 1000);
  const days = ['Dom', 'Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab'];
  return days[date.getDay()];
};

/**
 * Capitalizza la prima lettera di una stringa
 * @param {string} str - Stringa da capitalizzare
 * @returns {string} Stringa capitalizzata
 */
export const capitalize = (str) => {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
};

/**
 * Tronca una stringa se troppo lunga
 * @param {string} str - Stringa da troncare
 * @param {number} maxLength - Lunghezza massima
 * @returns {string} Stringa troncata
 */
export const truncate = (str, maxLength = 50) => {
  if (!str || str.length <= maxLength) return str;
  return str.substring(0, maxLength) + '...';
};

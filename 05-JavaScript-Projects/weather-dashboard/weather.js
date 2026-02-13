/**
 * ========================================
 * DASHBOARD METEO - JAVASCRIPT
 * ========================================
 *
 * Funzionalità:
 * - Meteo attuale con dettagli completi
 * - Previsioni 5 giorni
 * - Ricerca per città
 * - Geolocalizzazione
 * - Grafico temperature
 * - Gestione errori
 */

// ========================================
// CONFIGURAZIONE API
// ========================================

// ⚠️ INSERISCI QUI LA TUA API KEY DI OPENWEATHERMAP
// Ottienila gratuitamente da: https://openweathermap.org/api
const API_KEY = 'LA_TUA_API_KEY_QUI'; // Sostituisci con la tua chiave API

const BASE_URL = 'https://api.openweathermap.org/data/2.5';

// ========================================
// ELEMENTI DOM
// ========================================

const elements = {
    cityInput: document.getElementById('cityInput'),
    searchBtn: document.getElementById('searchBtn'),
    locationBtn: document.getElementById('locationBtn'),
    loading: document.getElementById('loading'),
    errorMessage: document.getElementById('errorMessage'),
    weatherDisplay: document.getElementById('weatherDisplay'),
    cityName: document.getElementById('cityName'),
    dateTime: document.getElementById('dateTime'),
    weatherIcon: document.getElementById('weatherIcon'),
    temperature: document.getElementById('temperature'),
    feelsLike: document.getElementById('feelsLike'),
    description: document.getElementById('description'),
    humidity: document.getElementById('humidity'),
    wind: document.getElementById('wind'),
    pressure: document.getElementById('pressure'),
    forecast: document.getElementById('forecast'),
    tempChart: document.getElementById('tempChart')
};

// ========================================
// FUNZIONI UTILITÀ
// ========================================

/**
 * Mostra/nasconde l'indicatore di caricamento
 * @param {boolean} show - True per mostrare, false per nascondere
 */
const showLoading = (show) => {
    elements.loading.classList.toggle('hidden', !show);
    if (show) {
        elements.errorMessage.classList.add('hidden');
        elements.weatherDisplay.classList.add('hidden');
    }
};

/**
 * Mostra un messaggio di errore
 * @param {string} message - Messaggio di errore da mostrare
 */
const showError = (message) => {
    elements.errorMessage.textContent = `❌ ${message}`;
    elements.errorMessage.classList.remove('hidden');
    elements.weatherDisplay.classList.add('hidden');
    elements.loading.classList.add('hidden');
};

/**
 * Mostra la dashboard meteo
 */
const showWeatherDisplay = () => {
    elements.weatherDisplay.classList.remove('hidden');
    elements.errorMessage.classList.add('hidden');
    elements.loading.classList.add('hidden');
};

/**
 * Formatta la data corrente in italiano
 * @returns {string} Data formattata
 */
const formatDate = () => {
    const options = {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date().toLocaleDateString('it-IT', options);
};

/**
 * Converte da Kelvin a Celsius
 * @param {number} kelvin - Temperatura in Kelvin
 * @returns {number} Temperatura in Celsius
 */
const kelvinToCelsius = (kelvin) => Math.round(kelvin - 273.15);

/**
 * Converte da m/s a km/h
 * @param {number} ms - Velocità in m/s
 * @returns {number} Velocità in km/h
 */
const msToKmh = (ms) => Math.round(ms * 3.6);

/**
 * Ottiene il nome del giorno della settimana
 * @param {number} index - Indice del giorno (0-6)
 * @returns {string} Nome del giorno in italiano
 */
const getDayName = (index) => {
    const days = ['Domenica', 'Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato'];
    return days[index];
};

/**
 * Ottiene il nome abbreviato del giorno
 * @param {number} index - Indice del giorno (0-6)
 * @returns {string} Nome abbreviato del giorno in italiano
 */
const getDayNameShort = (index) => {
    const days = ['Dom', 'Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab'];
    return days[index];
};

// ========================================
// FUNZIONI API
// ========================================

/**
 * Effettua una chiamata fetch all'API con gestione errori
 * @param {string} url - URL completo dell'API
 * @returns {Promise<Object>} Dati JSON della risposta
 */
const fetchWeatherData = async (url) => {
    try {
        const response = await fetch(url);

        if (!response.ok) {
            if (response.status === 404) {
                throw new Error('Città non trovata. Verifica il nome e riprova.');
            } else if (response.status === 401) {
                throw new Error('API Key non valida. Controlla il file weather.js e inserisci una chiave API valida.');
            } else {
                throw new Error(`Errore del server: ${response.status}`);
            }
        }

        const data = await response.json();
        return data;

    } catch (error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            throw new Error('Errore di connessione. Verifica la tua connessione internet.');
        }
        throw error;
    }
};

/**
 * Ottiene il meteo attuale di una città
 * @param {string} city - Nome della città
 * @returns {Promise<Object>} Dati meteo attuali
 */
const getCurrentWeather = async (city) => {
    const url = `${BASE_URL}/weather?q=${encodeURIComponent(city)}&appid=${API_KEY}`;
    return await fetchWeatherData(url);
};

/**
 * Ottiene le previsioni 5 giorni di una città
 * @param {string} city - Nome della città
 * @returns {Promise<Object>} Dati delle previsioni
 */
const getForecast = async (city) => {
    const url = `${BASE_URL}/forecast?q=${encodeURIComponent(city)}&appid=${API_KEY}`;
    return await fetchWeatherData(url);
};

/**
 * Ottiene il meteo attuale usando latitudine e longitudine
 * @param {number} lat - Latitudine
 * @param {number} lon - Longitudine
 * @returns {Promise<Object>} Dati meteo attuali
 */
const getWeatherByCoords = async (lat, lon) => {
    const url = `${BASE_URL}/weather?lat=${lat}&lon=${lon}&appid=${API_KEY}`;
    return await fetchWeatherData(url);
};

/**
 * Ottiene le previsioni usando latitudine e longitudine
 * @param {number} lat - Latitudine
 * @param {number} lon - Longitudine
 * @returns {Promise<Object>} Dati delle previsioni
 */
const getForecastByCoords = async (lat, lon) => {
    const url = `${BASE_URL}/forecast?lat=${lat}&lon=${lon}&appid=${API_KEY}`;
    return await fetchWeatherData(url);
};

// ========================================
// FUNZIONI DI AGGIORNAMENTO UI
// ========================================

/**
 * Aggiorna la sezione del meteo attuale
 * @param {Object} data - Dati meteo attuali
 */
const updateCurrentWeather = (data) => {
    const { name, main, weather, wind } = data;

    elements.cityName.textContent = name;
    elements.dateTime.textContent = formatDate();
    elements.temperature.textContent = `${kelvinToCelsius(main.temp)}°`;
    elements.feelsLike.textContent = `Percepite: ${kelvinToCelsius(main.feels_like)}°`;
    elements.description.textContent = weather[0].description;
    elements.humidity.textContent = `💧 Umidità: ${main.humidity}%`;
    elements.wind.textContent = `💨 Vento: ${msToKmh(wind.speed)} km/h`;
    elements.pressure.textContent = `🔵 Pressione: ${main.pressure} hPa`;

    // Icona meteo
    const iconCode = weather[0].icon;
    elements.weatherIcon.src = `https://openweathermap.org/img/wn/${iconCode}@4x.png`;
    elements.weatherIcon.alt = weather[0].description;
};

/**
 * Aggiorna la sezione delle previsioni
 * @param {Object} data - Dati delle previsioni
 */
const updateForecast = (data) => {
    const forecastList = data.list;

    // Filtra i dati per ottenere una previsione al giorno (a mezzogiorno)
    const dailyForecasts = forecastList.filter(item =>
        item.dt_txt.includes('12:00:00')
    ).slice(0, 5);

    elements.forecast.innerHTML = '';

    dailyForecasts.forEach((forecast, index) => {
        const date = new Date(forecast.dt * 1000);
        const dayIndex = date.getDay();
        const dayName = index === 0 ? 'Oggi' : getDayNameShort(dayIndex);

        const temp = kelvinToCelsius(forecast.main.temp);
        const description = forecast.weather[0].description;
        const iconCode = forecast.weather[0].icon;

        const card = document.createElement('div');
        card.className = 'forecast-card';
        card.innerHTML = `
            <div class="forecast-date">${dayName}</div>
            <img src="https://openweathermap.org/img/wn/${iconCode}@2x.png"
                 alt="${description}"
                 class="forecast-icon">
            <div class="forecast-temp">${temp}°C</div>
            <div class="forecast-description">${description}</div>
            <div class="forecast-details">
                💧 ${forecast.main.humidity}% |
                💨 ${msToKmh(forecast.wind.speed)} km/h
            </div>
        `;

        elements.forecast.appendChild(card);
    });
};

/**
 * Crea il grafico delle temperature
 * @param {Object} data - Dati delle previsioni
 */
const createTemperatureChart = (data) => {
    const canvas = elements.tempChart;
    const ctx = canvas.getContext('2d');

    // Imposta dimensioni canvas
    const container = canvas.parentElement;
    canvas.width = container.offsetWidth;
    canvas.height = container.offsetHeight;

    // Ottiene le temperature per le prossime 24 ore (ogni 3 ore)
    const hourlyData = data.list.slice(0, 8);
    const temperatures = hourlyData.map(item => kelvinToCelsius(item.main.temp));
    const labels = hourlyData.map(item => {
        const date = new Date(item.dt * 1000);
        return date.getHours() + ':00';
    });

    // Pulisce il canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Configurazione del grafico
    const padding = 50;
    const chartWidth = canvas.width - (padding * 2);
    const chartHeight = canvas.height - (padding * 2);
    const maxTemp = Math.max(...temperatures) + 2;
    const minTemp = Math.min(...temperatures) - 2;
    const tempRange = maxTemp - minTemp;

    // Disegna gli assi
    ctx.strokeStyle = '#4a90e2';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, canvas.height - padding);
    ctx.lineTo(canvas.width - padding, canvas.height - padding);
    ctx.stroke();

    // Disegna la linea del grafico
    ctx.strokeStyle = '#50c878';
    ctx.lineWidth = 3;
    ctx.beginPath();

    temperatures.forEach((temp, index) => {
        const x = padding + (index * (chartWidth / (temperatures.length - 1)));
        const y = (canvas.height - padding) - ((temp - minTemp) / tempRange) * chartHeight;

        if (index === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });

    ctx.stroke();

    // Disegna i punti e le etichette
    temperatures.forEach((temp, index) => {
        const x = padding + (index * (chartWidth / (temperatures.length - 1)));
        const y = (canvas.height - padding) - ((temp - minTemp) / tempRange) * chartHeight;

        // Punto
        ctx.fillStyle = '#ff6b6b';
        ctx.beginPath();
        ctx.arc(x, y, 6, 0, Math.PI * 2);
        ctx.fill();

        // Etichetta temperatura
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 14px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(`${temp}°`, x, y - 15);

        // Etichetta orario
        ctx.fillStyle = '#b8b8b8';
        ctx.font = '12px Arial';
        ctx.fillText(labels[index], x, canvas.height - padding + 20);
    });
};

// ========================================
// FUNZIONI PRINCIPALI
// ========================================

/**
 * Carica e mostra i dati meteo per una città
 * @param {string} city - Nome della città
 */
const loadWeatherData = async (city) => {
    try {
        showLoading(true);

        // Verifica che l'API key sia stata inserita
        if (API_KEY === 'LA_TUA_API_KEY_QUI' || API_KEY === '') {
            throw new Error('API Key non configurata. Apri il file weather.js e inserisci la tua API Key di OpenWeatherMap.');
        }

        // Carica i dati in parallelo
        const [currentData, forecastData] = await Promise.all([
            getCurrentWeather(city),
            getForecast(city)
        ]);

        // Aggiorna l'interfaccia
        updateCurrentWeather(currentData);
        updateForecast(forecastData);
        createTemperatureChart(forecastData);
        showWeatherDisplay();

    } catch (error) {
        showError(error.message);
        console.error('Errore nel caricamento dei dati meteo:', error);
    }
};

/**
 * Carica i dati meteo usando la geolocalizzazione
 */
const loadWeatherByLocation = async () => {
    if (!navigator.geolocation) {
        showError('Il tuo browser non supporta la geolocalizzazione.');
        return;
    }

    showLoading(true);

    navigator.geolocation.getCurrentPosition(
        async (position) => {
            const { latitude, longitude } = position.coords;

            try {
                if (API_KEY === 'LA_TUA_API_KEY_QUI' || API_KEY === '') {
                    throw new Error('API Key non configurata. Apri il file weather.js e inserisci la tua API Key di OpenWeatherMap.');
                }

                // Carica i dati in parallelo
                const [currentData, forecastData] = await Promise.all([
                    getWeatherByCoords(latitude, longitude),
                    getForecastByCoords(latitude, longitude)
                ]);

                // Aggiorna l'interfaccia
                updateCurrentWeather(currentData);
                updateForecast(forecastData);
                createTemperatureChart(forecastData);
                showWeatherDisplay();

            } catch (error) {
                showError(error.message);
                console.error('Errore nel caricamento dei dati meteo:', error);
            }
        },
        (error) => {
            let message = 'Impossibile ottenere la tua posizione.';
            if (error.code === 1) {
                message = 'Permessi di geolocalizzazione negati. Abilita la geolocalizzazione nel browser.';
            } else if (error.code === 2) {
                message = 'Posizione non disponibile. Verifica che il GPS sia attivo.';
            } else if (error.code === 3) {
                message = 'Timeout nella richiesta della posizione.';
            }
            showError(message);
        }
    );
};

// ========================================
// EVENT LISTENERS
// ========================================

/**
 * Gestisce la ricerca per città
 */
const handleSearch = () => {
    const city = elements.cityInput.value.trim();

    if (!city) {
        showError('Inserisci il nome di una città.');
        return;
    }

    loadWeatherData(city);
};

/**
 * Gestisce la pressione del tasto Enter nell'input
 */
const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
        handleSearch();
    }
};

// Event listeners
elements.searchBtn.addEventListener('click', handleSearch);
elements.cityInput.addEventListener('keypress', handleKeyPress);
elements.locationBtn.addEventListener('click', loadWeatherByLocation);

// Ridimensionamento della finestra - ridisegna il grafico
let resizeTimeout;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
        if (!elements.weatherDisplay.classList.contains('hidden')) {
            const city = elements.cityName.textContent;
            if (city !== '--') {
                loadWeatherData(city);
            }
        }
    }, 250);
});

// ========================================
// INIZIALIZZAZIONE
// ========================================

/**
 * Inizializzazione al caricamento della pagina
 */
document.addEventListener('DOMContentLoaded', () => {
    // Carica una città di default o mostra un messaggio di benvenuto
    console.log('🌤️ Dashboard Meteo caricata!');
    console.log('⚠️ Ricorda di inserire la tua API Key nel file weather.js');

    // Mostra un messaggio iniziale
    elements.errorMessage.innerHTML = `
        <strong>👋 Benvenuto nella Dashboard Meteo!</strong><br><br>
        📍 Cerca una città o usa il pulsante "La mia posizione"<br>
        🌡️ Visualizza meteo attuale, previsioni e grafici<br>
        ⚠️ <strong>Importante:</strong> Inserisci la tua API Key gratuita di OpenWeatherMap nel file weather.js
    `;
    elements.errorMessage.style.background = 'rgba(74, 144, 226, 0.2)';
    elements.errorMessage.style.borderColor = '#4a90e2';
    elements.errorMessage.style.color = '#4a90e2';
    elements.errorMessage.classList.remove('hidden');
});

// ========================================
// FINE DELLO SCRIPT
// ========================================

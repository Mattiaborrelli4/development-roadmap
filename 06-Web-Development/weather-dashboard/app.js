// ============================================
// DASHBOARD METEO - JavaScript ES6+
// Progetto educativo per studenti universitari
// ============================================

/**
 * ============================================
 * CONFIGURAZIONE
 * ============================================
 */

// API Key di OpenWeatherMap (registrati gratuitamente su https://openweathermap.org/api)
const API_KEY = 'YOUR_API_KEY_HERE'; // Sostituisci con la tua API key

// URL base dell'API
const BASE_URL = 'https://api.openweathermap.org/data/2.5';

/**
 * ============================================
 * GESTIONE DEL DOM (Document Object Model)
 * ============================================
 */

// Selezioniamo tutti gli elementi del DOM che ci servono
const elements = {
    // Input e pulsanti
    cityInput: document.getElementById('cityInput'),
    searchBtn: document.getElementById('searchBtn'),
    locationBtn: document.getElementById('locationBtn'),
    saveCityBtn: document.getElementById('saveCityBtn'),

    // Sezioni
    currentWeather: document.getElementById('currentWeather'),
    chartSection: document.getElementById('chartSection'),
    savedCities: document.getElementById('savedCities'),
    statusMessage: document.getElementById('statusMessage'),

    // Elementi meteo
    cityName: document.getElementById('cityName'),
    weatherDate: document.getElementById('weatherDate'),
    temperature: document.getElementById('temperature'),
    weatherIcon: document.getElementById('weatherIcon'),
    weatherDescription: document.getElementById('weatherDescription'),
    feelsLike: document.getElementById('feelsLike'),
    humidity: document.getElementById('humidity'),
    windSpeed: document.getElementById('windSpeed'),
    pressure: document.getElementById('pressure'),
    visibility: document.getElementById('visibility'),

    // Lista città salvate
    savedCitiesList: document.getElementById('savedCitiesList'),

    // Canvas per il grafico
    chartCanvas: document.getElementById('temperatureChart')
};

// Variabile globale per il grafico
let temperatureChart = null;

/**
 * ============================================
 * GESTIONE DEL LOCAL STORAGE
 * ============================================
 */

/**
 * Salva una città nel localStorage
 * Il localStorage salva solo stringhe, quindi usiamo JSON.stringify()
 */
const saveCityToStorage = (cityData) => {
    // Recupera le città salvate (o array vuoto se non ce ne sono)
    const savedCities = getCitiesFromStorage();

    // Controlla se la città esiste già
    const cityExists = savedCities.some(city => city.name === cityData.name);

    if (cityExists) {
        showStatus('Questa città è già salvata!', 'error');
        return false;
    }

    // Aggiungi la nuova città (max 10 città)
    if (savedCities.length >= 10) {
        savedCities.pop(); // Rimuovi l'ultima città
    }

    savedCities.unshift({
        name: cityData.name,
        temp: cityData.main.temp,
        description: cityData.weather[0].description,
        icon: cityData.weather[0].icon
    });

    // Salva nel localStorage come stringa JSON
    localStorage.setItem('savedCities', JSON.stringify(savedCities));
    return true;
};

/**
 * Recupera le città dal localStorage
 * Usiamo JSON.parse() per convertire la stringa in oggetto
 */
const getCitiesFromStorage = () => {
    const stored = localStorage.getItem('savedCities');
    return stored ? JSON.parse(stored) : [];
};

/**
 * Rimuove una città dal localStorage
 */
const removeCityFromStorage = (cityName) => {
    let savedCities = getCitiesFromStorage();
    savedCities = savedCities.filter(city => city.name !== cityName);
    localStorage.setItem('savedCities', JSON.stringify(savedCities));
    renderSavedCities();
};

/**
 * ============================================
 * FETCH API E ASYNC/AWAIT
 * ============================================
 */

/**
 * Funzione principale per recuperare i dati meteo
 * Dimostra l'uso di async/await per gestire operazioni asincrone
 *
 * Async/Await permette di scrivere codice asincrono che sembra sincrono
 * rendendolo più facile da leggere e mantenere.
 */
const fetchWeatherData = async (city) => {
    try {
        showStatus('Caricamento dati meteo...', 'info');

        // Costruisci l'URL della richiesta API
        const url = `${BASE_URL}/weather?q=${encodeURIComponent(city)}&units=metric&lang=it&appid=${API_KEY}`;

        /**
         * Fetch API:
         * - Restituisce una Promise che risolve con un oggetto Response
         * - await mette in pausa l'esecuzione finché la Promise non si risolve
         * - Questo rende il codice asincrono più leggibile
         */
        const response = await fetch(url);

        // Verifica se la richiesta ha avuto successo
        if (!response.ok) {
            // Se la città non esiste (404) o c'è un altro errore
            if (response.status === 404) {
                throw new Error('Città non trovata. Verifica il nome e riprova.');
            }
            throw new Error(`Errore del server: ${response.status}`);
        }

        // .json() è un metodo async che converte la risposta in oggetto JavaScript
        const data = await response.json();

        // Aggiorna l'interfaccia con i dati ricevuti
        displayCurrentWeather(data);

        // Recupera anche le previsioni per il grafico
        await fetchForecastData(city);

        showStatus('Dati caricati con successo!', 'success');
        hideStatusAfter(3000);

        return data;

    } catch (error) {
        // Catch cattura qualsiasi errore nel blocco try
        console.error('Errore nel recupero dei dati:', error);
        showStatus(error.message, 'error');
        hideStatusAfter(5000);
        return null;
    }
};

/**
 * Recupera le previsioni meteo per il grafico
 * Usa Promise.all per fare più richieste in parallelo
 */
const fetchForecastData = async (city) => {
    try {
        // URL per le previsioni orarie
        const url = `${BASE_URL}/forecast?q=${encodeURIComponent(city)}&units=metric&lang=it&appid=${API_KEY}`;

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error('Impossibile recuperare le previsioni');
        }

        const data = await response.json();

        // Estrai i dati per le prossime 24 ore (8 intervalli da 3 ore)
        const forecastData = data.list.slice(0, 8);

        // Crea il grafico con i dati
        createTemperatureChart(forecastData);

    } catch (error) {
        console.error('Errore nel recupero delle previsioni:', error);
    }
};

/**
 * ============================================
 * GESTIONE DELLA GEOLOCALIZZAZIONE
 * ============================================
 */

/**
 * Recupera la posizione dell'utente usando l'API di Geolocalizzazione
 * Questa è un'API del browser che richiede il permesso dell'utente
 */
const getLocationWeather = () => {
    // Verifica se il browser supporta la geolocalizzazione
    if (!navigator.geolocation) {
        showStatus('Il tuo browser non supporta la geolocalizzazione.', 'error');
        return;
    }

    showStatus('Recupero della tua posizione...', 'info');

    /**
     * getCurrentPosition accetta 3 callback:
     * 1. Success callback (chiamata se la posizione è trovata)
     * 2. Error callback (chiamata se c'è un errore)
     * 3. Options (oggetto con opzioni aggiuntive)
     */
    navigator.geolocation.getCurrentPosition(
        async (position) => {
            // Success! Abbiamo la posizione
            const { latitude, longitude } = position.coords;

            try {
                // Recupera i meteo usando latitudine e longitudine
                const url = `${BASE_URL}/weather?lat=${latitude}&lon=${longitude}&units=metric&lang=it&appid=${API_KEY}`;
                const response = await fetch(url);
                const data = await response.json();

                displayCurrentWeather(data);
                await fetchForecastData(data.name);

                showStatus('Dati della tua posizione caricati!', 'success');
                hideStatusAfter(3000);

            } catch (error) {
                showStatus('Errore nel recupero dei meteo dalla posizione.', 'error');
            }
        },
        (error) => {
            // Error callback
            let errorMessage = 'Errore nella geolocalizzazione. ';

            switch(error.code) {
                case error.PERMISSION_DENIED:
                    errorMessage += 'Permesso negato. Abilita la geolocalizzazione nel browser.';
                    break;
                case error.POSITION_UNAVAILABLE:
                    errorMessage += 'Informazioni sulla posizione non disponibili.';
                    break;
                case error.TIMEOUT:
                    errorMessage += 'Timeout nella richiesta della posizione.';
                    break;
                default:
                    errorMessage += 'Errore sconosciuto.';
            }

            showStatus(errorMessage, 'error');
        }
    );
};

/**
 * ============================================
 * VISUALIZZAZIONE DEI DATI
 * ============================================
 */

/**
 * Mostra i dati meteo correnti nell'interfaccia
 */
const displayCurrentWeather = (data) => {
    // Mostra la sezione meteo
    elements.currentWeather.classList.remove('hidden');

    // Aggiorna i dati della città
    elements.cityName.textContent = `${data.name}, ${data.sys.country}`;
    elements.temperature.textContent = Math.round(data.main.temp);
    elements.weatherDescription.textContent = data.weather[0].description;
    elements.feelsLike.textContent = Math.round(data.main.feels_like);
    elements.humidity.textContent = data.main.humidity;
    elements.windSpeed.textContent = Math.round(data.wind.speed * 3.6); // Conversione m/s in km/h
    elements.pressure.textContent = data.main.pressure;
    elements.visibility.textContent = (data.visibility / 1000).toFixed(1); // Conversione in km

    // Aggiorna l'icona meteo
    const iconCode = data.weather[0].icon;
    elements.weatherIcon.src = `https://openweathermap.org/img/wn/${iconCode}@4x.png`;
    elements.weatherIcon.alt = data.weather[0].description;

    // Aggiorna la data
    const now = new Date();
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    elements.weatherDate.textContent = now.toLocaleDateString('it-IT', options);
};

/**
 * Crea il grafico della temperatura usando Chart.js
 * Dimostra come integrare librerie esterne in JavaScript
 */
const createTemperatureChart = (forecastData) => {
    // Mostra la sezione grafico
    elements.chartSection.classList.remove('hidden');

    // Estrai le etichette (orari) e i dati (temperature)
    const labels = forecastData.map(item => {
        const date = new Date(item.dt * 1000);
        return date.toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' });
    });

    const temperatures = forecastData.map(item => Math.round(item.main.temp));

    // Distruggi il grafico esistente se presente
    if (temperatureChart) {
        temperatureChart.destroy();
    }

    // Crea il nuovo grafico
    temperatureChart = new Chart(elements.chartCanvas, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Temperatura (°C)',
                data: temperatures,
                borderColor: '#3498db',
                backgroundColor: 'rgba(52, 152, 219, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4, // Curve morbide
                pointBackgroundColor: '#3498db',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    labels: {
                        color: '#ffffff',
                        font: {
                            size: 14
                        }
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: '#b8b8b8'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                y: {
                    ticks: {
                        color: '#b8b8b8'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                }
            }
        }
    });
};

/**
 * Renderizza la lista delle città salvate
 * Dimostra come manipolare il DOM dinamicamente
 */
const renderSavedCities = () => {
    const cities = getCitiesFromStorage();

    if (cities.length === 0) {
        elements.savedCities.classList.add('hidden');
        return;
    }

    // Mostra la sezione
    elements.savedCities.classList.remove('hidden');

    // Svuota la lista esistente
    elements.savedCitiesList.innerHTML = '';

    // Crea una card per ogni città
    cities.forEach(city => {
        const cityCard = document.createElement('div');
        cityCard.className = 'city-card';
        cityCard.innerHTML = `
            <h4>${city.name}</h4>
            <div class="city-temp">${Math.round(city.temp)}°C</div>
            <div class="city-desc">${city.description}</div>
            <button class="delete-city" data-city="${city.name}" title="Rimuovi città">×</button>
        `;

        // Aggiungi click per caricare i meteo della città
        cityCard.addEventListener('click', (e) => {
            // Non caricare se è stato cliccato il pulsante elimina
            if (e.target.classList.contains('delete-city')) {
                return;
            }
            fetchWeatherData(city.name);
        });

        // Aggiungi il pulsante elimina
        const deleteBtn = cityCard.querySelector('.delete-city');
        deleteBtn.addEventListener('click', () => {
            removeCityFromStorage(city.name);
        });

        elements.savedCitiesList.appendChild(cityCard);
    });
};

/**
 * ============================================
 * GESTIONE DEI MESSAGGI
 * ============================================
 */

/**
 * Mostra un messaggio di stato
 * @param {string} message - Il messaggio da mostrare
 * @param {string} type - Il tipo di messaggio (success, error, info)
 */
const showStatus = (message, type = 'info') => {
    elements.statusMessage.textContent = message;
    elements.statusMessage.className = `status-message ${type}`;
    elements.statusMessage.classList.remove('hidden');
};

/**
 * Nasconde il messaggio dopo un certo tempo
 * @param {number} delay - Ritardo in millisecondi
 */
const hideStatusAfter = (delay) => {
    setTimeout(() => {
        elements.statusMessage.classList.add('hidden');
    }, delay);
};

/**
 * ============================================
 * EVENT LISTENERS
 * ============================================
 */

/**
 * Event Listener per il pulsante di ricerca
 * Dimostra come gestire il click dell'utente
 */
elements.searchBtn.addEventListener('click', () => {
    const city = elements.cityInput.value.trim();

    // Validazione: controlla che il campo non sia vuoto
    if (!city) {
        showStatus('Inserisci il nome di una città.', 'error');
        return;
    }

    // Chiama la funzione per recuperare i dati meteo
    fetchWeatherData(city);
});

/**
 * Event Listener per il tasto Invio nell'input
 * Permette di cercare premendo Invio invece di cliccare il pulsante
 */
elements.cityInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        elements.searchBtn.click();
    }
});

/**
 * Event Listener per la geolocalizzazione
 */
elements.locationBtn.addEventListener('click', () => {
    getLocationWeather();
});

/**
 * Event Listener per salvare la città corrente
 */
elements.saveCityBtn.addEventListener('click', () => {
    const cityName = elements.cityName.textContent.split(',')[0];

    if (cityName === '--') {
        showStatus('Cerca prima una città da salvare.', 'error');
        return;
    }

    // Recupera di nuovo i dati per averli completi
    fetch(`${BASE_URL}/weather?q=${encodeURIComponent(cityName)}&units=metric&lang=it&appid=${API_KEY}`)
        .then(response => response.json())
        .then(data => {
            if (saveCityToStorage(data)) {
                showStatus(`Città ${cityName} salvata con successo!`, 'success');
                renderSavedCities();
                hideStatusAfter(3000);
            }
        })
        .catch(error => {
            showStatus('Errore nel salvataggio della città.', 'error');
        });
});

/**
 * ============================================
 * INIZIALIZZAZIONE
 * ============================================
 */

/**
 * Codice eseguito al caricamento della pagina
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('🌤️ Dashboard Meteo caricata!');

    // Carica le città salvate
    renderSavedCities();

    // Mostra un messaggio di benvenuto
    showStatus('Benvenuto! Cerca una città o usa la geolocalizzazione.', 'info');

    // Focus sull'input per facilitare l'uso
    elements.cityInput.focus();

    /**
     * NOTA EDUCATIVA:
     * L'API Key di OpenWeatherMap deve essere configurata in cima a questo file.
     * Per ottenere una API Key gratuita:
     * 1. Vai su https://openweathermap.org/api
     * 2. Registrati gratuitamente
     * 3. Vai nella sezione "API keys"
     * 4. Copia la tua chiave e incollala nella variabile API_KEY
     *
     * Alternativa senza API Key: usa wttr.in
     * Ma wttr.in non offre dati in formato JSON strutturato come OpenWeatherMap
     */
});

/**
 * ============================================
 * FUNZIONI UTILITÀ
 * ============================================
 */

/**
 * Arrotonda un numero a un numero specifico di decimali
 * @param {number} num - Il numero da arrotondare
 * @param {number} decimals - Numero di decimali (default: 0)
 * @returns {number} Numero arrotondato
 */
const roundTo = (num, decimals = 0) => {
    const factor = Math.pow(10, decimals);
    return Math.round(num * factor) / factor;
};

/**
 * Formatta una data in italiano
 * @param {Date} date - Oggetto Date
 * @returns {string} Data formattata
 */
const formatDate = (date) => {
    return date.toLocaleDateString('it-IT', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
};

// Esporta funzioni per debugging (opzionale)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        fetchWeatherData,
        saveCityToStorage,
        getCitiesFromStorage
    };
}

/**
 * ============================================
 * CONCETTI CHIAVE IMPARATI:
 * ============================================
 *
 * 1. FETCH API: Fai richieste HTTP asincrone a server esterni
 * 2. ASYNC/AWAIT: Gestisci operazioni asincrone in modo leggibile
 * 3. PROMISE: Oggetti che rappresentano il completamento futuro di un'operazione
 * 4. ARROW FUNCTIONS: Sintassi concisa per le funzioni: () => {}
 * 5. TEMPLATE LITERALS: Stringhe con espressioni incorporate: `${variable}`
 * 6. DESTRUCTURING: Estrai proprietà da oggetti: const { name, age } = person
 * 7. SPREAD OPERATOR: Espandi array/oggetti: [...array, newItem]
 * 8. ARRAY METHODS: map(), filter(), forEach(), some(), find()
 * 9. DOM MANIPULATION: Seleziona e modifica elementi HTML
 * 10. EVENT LISTENERS: Rispondi alle interazioni dell'utente
 * 11. LOCAL STORAGE: Salva dati persistenti nel browser
 * 12. ERROR HANDLING: try/catch per gestire errori gracefully
 * 13. JSON: Converti tra oggetti JS e stringhe (JSON.stringify/parse)
 * 14. CHART.JS: Integrare librerie esterne per visualizzazioni
 * 15. GELOCATION API: Ottieni la posizione dell'utente
 *
 * Questi concetti sono fondamentali per sviluppare applicazioni web moderne!
 */

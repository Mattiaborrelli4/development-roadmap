# Weather App - React Native/Expo

Un'app meteo completa e funzionale sviluppata con React Native e Expo.

![Weather App](https://img.shields.io/badge/React_Native-0.76.6-blue)
![Expo](https://img.shields.io/badge/Expo-52.0.0-purple)
![Platform](https://img.shields.io/badge/Platform-iOS%20%7C%20Android%20%7C%20Web-lightgrey)

## Caratteristiche

### Funzionalità Principali

- 🌡️ **Meteo Attuale**: Visualizza temperatura attuale, percepita, umidità, vento e visibilità
- 📅 **Previsioni a 5 Giorni**: Previsioni dettagliate con temperature min/max e condizioni
- 📍 **Geolocalizzazione**: Ottieni automaticamente il meteo della tua posizione
- 🔍 **Ricerca Città**: Cerca qualsiasi città nel mondo
- 🔄 **Pull-to-Refresh**: Aggiorna i dati trascinando verso il basso
- 💾 **Cache Offline**: Visualizza l'ultimo meteo anche senza connessione
- 🎨 **Animazioni**: Transizioni fluide e interfacce animate

### Dati Meteo Visualizzati

- Temperatura attuale e percepita
- Temperature minime e massime
- Umidità percentuale
- Velocità e direzione del vento
- Visibilità
- Orari di alba e tramonto
- Icone meteo dinamiche
- Previsioni 5 giorni

## Tecnologie Utilizzate

### Core
- **React Native 0.76.6**: Framework per app mobile
- **Expo 52.0**: Platform per sviluppo e build
- **JavaScript ES6+**: Linguaggio di programmazione

### Navigazione
- **React Navigation 6**: Navigazione tra schermate
- **Native Stack Navigator**: Navigazione nativa

### API e Servizi
- **OpenWeatherMap API**: Dati meteo (free tier)
- **Expo Location**: Geolocalizzazione
- **Axios**: Richieste HTTP
- **AsyncStorage**: Cache locale dei dati

### UI e Styling
- **Expo Linear Gradient**: Sfondi gradiente animati
- **React Native Animated**: Animazioni fluide
- **Custom Theme System**: Tema personalizzato

## Struttura del Progetto

```
weather-app/
├── App.js                          # Entry point dell'app
├── app.json                        # Configurazione Expo
├── package.json                    # Dipendenze
├── src/
│   ├── components/                 # Componenti riutilizzabili
│   │   ├── WeatherCard.jsx         # Card meteo principale
│   │   ├── ForecastItem.jsx        # Item previsioni
│   │   ├── SearchBar.jsx           # Barra di ricerca
│   │   ├── LoadingSpinner.jsx      # Spinner di caricamento
│   │   └── LocationButton.jsx      # Pulsante posizione
│   ├── screens/                    # Schermate dell'app
│   │   ├── HomeScreen.jsx          # Schermata principale
│   │   └── SearchScreen.jsx        # Schermata ricerca
│   ├── services/                   # Servizi e API
│   │   ├── weatherAPI.js           # API OpenWeatherMap
│   │   └── locationService.js      # Servizi di geolocalizzazione
│   ├── hooks/                      # Custom React Hooks
│   │   ├── useWeather.js           # Hook per dati meteo
│   │   └── useLocation.js          # Hook per geolocalizzazione
│   ├── utils/                      # Utility functions
│   │   ├── cache.js                # Gestione cache AsyncStorage
│   │   └── helpers.js              # Funzioni helper
│   └── styles/                     # Stili
│       └── theme.js                # Tema dell'app
└── README.md                        # Documentazione
```

## Installazione e Configurazione

### Prerequisiti

- Node.js (v18 o superiore)
- npm o yarn
- Expo CLI: `npm install -g expo-cli`
- Expo Go app sul dispositivo (opzionale)

### Setup Iniziale

1. **Installazione delle dipendenze**

```bash
cd weather-app
npm install
```

2. **Configurazione API Key**

Apri `src/services/weatherAPI.js` e sostituisci `YOUR_OPENWEATHERMAP_API_KEY` con la tua API key di OpenWeatherMap:

```javascript
const API_KEY = 'tua_api_key_qui';
```

Per ottenere una API key gratuita:
1. Vai su [OpenWeatherMap](https://openweathermap.org/api)
2. Registrati per un account gratuito
3. Naviga alla sezione API keys
4. Copia la tua API key

3. **Avvio dell'app**

```bash
# Avvia il development server
npm start

# oppure per piattaforme specifiche
npm run ios     # iOS Simulator
npm run android # Android Emulator
npm run web     # Browser
```

4. **Esecuzione su dispositivo**

- Installa l'app **Expo Go** sul tuo dispositivo
- Scansiona il QR code dal terminale
- L'app si aprirà automaticamente

## Funzionalità Dettagliate

### 1. Meteo Attuale

La schermata principale mostra:
- Nome della città e paese
- Temperatura attuale (grande e prominente)
- Condizione meteo con icona
- Temperatura percepita
- Temperature min/max del giorno
- Umidità, vento, visibilità
- Orari alba e tramonto

### 2. Previsioni a 5 Giorni

Le previsioni mostrano:
- Nome del giorno (oggi, dom, lun, mar...)
- Icona meteo per ogni giorno
- Temperature minime e massime
- Barra di temperatura visiva
- Umidità e vento
- Condizione meteo descrittiva

### 3. Geolocalizzazione

- Autorizzazione automatica alla posizione
- Utilizzo di Expo Location per coordinate GPS
- Reverse geocoding per nome della città
- Gestione errori per permessi negati

### 4. Ricerca Città

- Barra di ricerca con autocomplete
- Città popolari italiane pre-caricate
- Ricerca in tempo reale
- Selezione rapida città

### 5. Cache Offline

- Salvataggio automatico dell'ultima posizione
- Cache con scadenza (30 minuti)
- Visualizzazione dati offline
- Aggiornamento manuale disponibile

### 6. Pull-to-Refresh

- Trascina verso il basso per aggiornare
- Indicatore di caricamento
- Sincronizzazione con API

## API Integration

### OpenWeatherMap API

L'app utilizza due endpoint:

1. **Current Weather**
```javascript
GET /weather?q={city name}&appid={API key}&units=metric&lang=it
```

2. **5 Day Forecast**
```javascript
GET /forecast?lat={lat}&lon={lon}&appid={API key}&units=metric&lang=it
```

### Gestione Errori

- 404: Città non trovata
- 401: API key non valida
- 429: Troppe richieste
- Network error: Nessuna connessione

## Personalizzazione

### Tema

Modifica `src/styles/theme.js` per personalizzare:

```javascript
export const theme = {
  colors: {
    primary: '#4facfe',
    secondary: '#00f2fe',
    // ... altri colori
  },
  gradients: {
    sunny: ['#4facfe', '#00f2fe'],
    cloudy: ['#bdc3c7', '#2c3e50'],
    // ... altri gradienti
  }
};
```

### Cache Duration

Modifica la durata della cache in `src/utils/cache.js`:

```javascript
const CACHE_EXPIRY = 30 * 60 * 1000; // 30 minuti
```

## Troubleshooting

### Problemi Comuni

1. **API Key non valida**
   - Verifica di aver inserito correttamente la tua API key
   - Controlla che la key sia attiva su OpenWeatherMap

2. **Permessi di localizzazione**
   - Assicurati di aver concesso i permessi di posizione
   - Su iOS, verifica le impostazioni privacy

3. **Problemi di cache**
   - Disinstalla e reinstalla l'app per pulire la cache
   - Oppure usa la funzione `clearWeatherCache()`

4. **Errore di rete**
   - Verifica la connessione internet
   - Controlla che l'API sia raggiungibile

## Build per Produzione

### iOS

```bash
expo build:ios
```

### Android

```bash
expo build:android
```

### EAS Build (raccomandato)

```bash
npm install -g eas-cli
eas build --platform ios
eas build --platform android
```

## Licenza

Questo progetto è stato creato a scopo educativo. È libero di essere utilizzato e modificato.

## Crediti

- **Dati meteo**: [OpenWeatherMap](https://openweathermap.org/)
- **Icone**: [Expo Vector Icons](https://icons.expo.fyi/)
- **Framework**: [React Native](https://reactnative.dev/) & [Expo](https://expo.dev/)

## Roadmap Futuri

- [ ] Widget home screen
- [ ] Notifiche meteo
- [ ] Grafici temperatura storici
- [ ] Mappe meteo interattive
- [ ] Multi-lingua completo
- [ ] Tema scuro
- [ ] Salvataggio città preferite

---

**Sviluppato con** ❤️ **using React Native & Expo**

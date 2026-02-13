# 🌤️ Dashboard Meteo

Una dashboard meteo interattiva e moderna che mostra le previsioni del tempo in tempo reale, con supporto per la ricerca per città, geolocalizzazione e visualizzazioni grafiche delle temperature.

![Dashboard Meteo](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

## 📋 Caratteristiche

- **☀️ Meteo Attuale**: Visualizza temperatura attuale, temperatura percepita, umidità, vento e pressione
- **📅 Previsioni 5 Giorni**: Previsioni meteorologiche per i prossimi 5 giorni con dettagli completi
- **🔍 Ricerca per Città**: Cerca il meteo di qualsiasi città nel mondo
- **📍 Geolocalizzazione**: Ottieni automaticamente il meteo della tua posizione attuale
- **📊 Grafico Temperature**: Visualizzazione grafica delle temperature delle prossime 24 ore
- **⚠️ Gestione Errori**: Messaggi di errore chiari per città non trovate, problemi di connessione, ecc.
- **📱 Design Responsive**: Funziona perfettamente su desktop, tablet e smartphone
- **🎨 Interfaccia Moderna**: Design dark mode elegante con animazioni fluide

## 🚀 Installazione e Configurazione

### 1. Ottieni un'API Key di OpenWeatherMap

1. Vai su [OpenWeatherMap](https://openweathermap.org/api)
2. Registrati per un account gratuito (è gratis!)
3. Accedi al tuo account
4. Vai nella sezione "API Keys"
5. Copia la tua API Key

### 2. Configura il Progetto

1. Scarica o clona questo progetto
2. Apri il file `weather.js`
3. Trova la riga:
   ```javascript
   const API_KEY = 'LA_TUA_API_KEY_QUI';
   ```
4. Sostituisci `'LA_TUA_API_KEY_QUI'` con la tua API Key:
   ```javascript
   const API_KEY = 'tua_api_key_qui';
   ```
5. Salva il file

### 3. Avvia la Dashboard

Semplicemente apri il file `index.html` nel tuo browser web preferito.

Non serve un server locale! Puoi aprire direttamente il file HTML con doppio clic.

## 📁 Struttura del Progetto

```
weather-dashboard/
│
├── index.html          # Struttura della dashboard
├── style.css           # Stili CSS con design responsive
├── weather.js          # Logica JavaScript con API integration
└── README.md           # Documentazione (questo file)
```

## 🛠️ Tecnologie Utilizzate

- **HTML5**: Struttura semantica della pagina
- **CSS3**: Stili moderni con:
  - CSS Grid e Flexbox per il layout
  - Variabili CSS per la facilità di manutenzione
  - Animazioni e transizioni fluide
  - Design responsive con media queries
  - Dark mode elegante
- **JavaScript ES6+**: Funzionalità avanzate con:
  - `async/await` per chiamate API asincrone
  - `fetch` API per richieste HTTP
  - Arrow functions
  - Template literals
  - Destructuring e spread operator
  - Gestione errori con `try/catch`
  - Canvas API per i grafici
- **OpenWeatherMap API**: Dati meteorologici in tempo reale

## 📖 Funzionalità Dettagliate

### Meteo Attuale
- Temperatura attuale in Celsius
- Temperatura percepita (feels like)
- Condizioni meteorologiche con icona
- Umidità (%)
- Velocità del vento (km/h)
- Pressione atmosferica (hPa)

### Previsioni 5 Giorni
- Una previsione per giorno
- Temperatura giornaliera
- Icona e descrizione delle condizioni
- Umidità e vento previsti

### Grafico Temperature
- Visualizzazione delle temperature per le prossime 24 ore
- Aggiornamento ogni 3 ore
- Grafico interattivo disegnato con Canvas API
- Auto-ridimensionamento in base alla finestra

### Ricerca e Geolocalizzazione
- Ricerca per nome della città (in qualsiasi lingua)
- Geolocalizzazione automatica con API del browser
- Gestione dei permessi di posizione
- Messaggi di errore specifici per ogni problematica

### Gestione Errori
- Città non trovata
- API Key non valida
- Problemi di connessione internet
- Permessi di geolocalizzazione negati
- Timeout della richiesta
- Posizione GPS non disponibile

## 🎯 Come Usare

### Ricerca per Città
1. Digita il nome della città nell'input di ricerca
2. Premi il pulsante "🔍 Cerca" o premi Enter
3. La dashboard mostrerà il meteo della città

### Geolocalizzazione
1. Premi il pulsante "📍 La mia posizione"
2. Accetta i permessi di posizione quando richiesto dal browser
3. La dashboard mostrerà il meteo della tua posizione attuale

## 🌐 API OpenWeatherMap

Questo progetto utilizza l'API gratuita di OpenWeatherMap:
- **Current Weather Data**: Meteo attuale
- **5 Day / 3 Hour Forecast**: Previsioni dettagliate
- **Geocoding API**: Ricerca città per nome
- **Limiti gratuiti**: 60 chiamate/minute (sufficienti per uso personale)

## 📱 Compatibilità Browser

- ✅ Chrome/Edge (raccomandato)
- ✅ Firefox
- ✅ Safari
- ✅ Opera
- ⚠️ Internet Explorer (non supportato - usa fetch API e ES6+)

## 🐛 Risoluzione Problemi

### La dashboard non mostra i dati
- Verifica di aver inserito correttamente la tua API Key nel file `weather.js`
- Controlla la tua connessione internet
- Apri la console del browser (F12) per vedere eventuali errori

### Errore "API Key non valida"
- Assicurati di aver copiato correttamente l'API Key
- Verifica che l'API Key sia attiva sul tuo account OpenWeatherMap
- Può essere necessario attendere qualche minuto dopo la creazione della chiave

### Errore "Città non trovata"
- Verifica il nome della città (puoi anche usare nomi in altre lingue)
- Per le città ambigue, aggiungi il codice paese (es: "Roma,IT")

### La geolocalizzazione non funziona
- Verifica di aver concesso i permessi di posizione al browser
- Alcuni browser richiedono connessione HTTPS per la geolocalizzazione
- Controlla che il GPS sia attivo sul tuo dispositivo

## 🎨 Personalizzazione

Puoi facilmente personalizzare l'aspetto della dashboard modificando le variabili CSS in `style.css`:

```css
:root {
    --primary-color: #4a90e2;      /* Colore principale */
    --secondary-color: #50c878;    /* Colore secondario */
    --accent-color: #ff6b6b;       /* Colore accento */
    --background-dark: #1a1a2e;    /* Sfondo principale */
    --background-card: #16213e;     /* Sfondo delle card */
}
```

## 📄 Licenza

Questo progetto è creato a scopo educativo. Sei libero di usarlo, modificarlo e distribuirlo come preferisci.

## 👨‍💻 Note per Sviluppatori

### Struttura del Codice JavaScript
- **Configurazione**: API key e URL base
- **Elementi DOM**: Cache degli elementi del DOM per performance
- **Funzioni Utilità**: Funzioni helper riutilizzabili
- **Funzioni API**: Gestione chiamate all'API
- **Funzioni UI**: Aggiornamento dell'interfaccia
- **Event Listeners**: Gestione interazioni utente
- **Inizializzazione**: Setup iniziale della pagina

### Best Practices Implementate
- ✅ Separazione delle responsabilità
- ✅ Gestione errori robusta
- ✅ Codice commentato e documentato
- ✅ Nomi di variabili descrittivi
- ✅ Funzioni pure quando possibile
- ✅ Evita globali non necessarie
- ✅ Performance ottimizzate (caching DOM, debouncing resize)

## 📞 Supporto

Per problemi o domande:
1. Controlla la sezione "Risoluzione Problemi" sopra
2. Consulta la [documentazione OpenWeatherMap](https://openweathermap.org/api)
3. Apri un issue nel repository

## 🙏 Riconoscimenti

- Dati meteo forniti da [OpenWeatherMap](https://openweathermap.org/)
- Icone meteorologiche da [OpenWeatherMap](https://openweathermap.org/weather-conditions)
- Design ispirato dalle moderne dashboard meteo

---

**Creato con ❤️ usando HTML, CSS e JavaScript puro**

Nota: Ricorda di non condividere pubblicamente la tua API Key!

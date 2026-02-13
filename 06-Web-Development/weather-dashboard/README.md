# 🌤️ Dashboard Meteo - Progetto Educativo JavaScript

Una dashboard meteo interattiva costruita con **JavaScript ES6+**, progettata specificamente per studenti universitari che vogliono imparare lo sviluppo web moderno.

![JavaScript Version](https://img.shields.io/badge/JavaScript-ES6+-yellow.svg)
![Educational](https://img.shields.io/badge/Purpose-Educational-green.svg)
![Level](https://img.shields.io/badge/Level-Beginner-blue.svg)

## 📚 Contenuti Educativi

Questo progetto insegna concetti fondamentali di JavaScript moderno attraverso un'applicazione reale e pratica:

### Concetti Principali

- ✅ **Fetch API** - Richieste HTTP asincrone
- ✅ **Async/Await** - Gestione di operazioni asincrone leggibile
- ✅ **Promises** - Completamento futuro di operazioni
- ✅ **Arrow Functions** - Sintassi moderna per funzioni
- ✅ **Template Literals** - Stringhe con espressioni
- ✅ **Destructuring** - Estrazione proprietà da oggetti
- ✅ **Array Methods** - `map()`, `filter()`, `forEach()`, `some()`
- ✅ **DOM Manipulation** - Selezione e modifica elementi HTML
- ✅ **Event Listeners** - Gestione interazioni utente
- ✅ **LocalStorage** - Persistenza dati nel browser
- ✅ **Error Handling** - Gestione errori con `try/catch`
- ✅ **JSON** - Serializzazione/deserializzazione dati
- ✅ **Chart.js** - Integrazione librerie esterne
- ✅ **Geolocation API** - Posizione dell'utente

## 🎯 Obiettivi di Apprendimento

Al termine di questo progetto, sarai in grado di:

1. **Fare richieste API** usando `fetch()` e gestire risposte JSON
2. **Scrivere codice asincrono** con `async/await` invece di callback hell
3. **Manipolare il DOM** per creare interfacce dinamiche
4. **Gestire gli eventi** dell'utente in modo efficiente
5. **Salvare dati persistenti** con LocalStorage
6. **Gestire gli errori** in modo gracefule
7. **Usare librerie esterne** come Chart.js
8. **Scrivere codice modulare** con funzioni riutilizzabili

## 🚀 Guida Rapida all'Installazione

### Prerequisiti

- Un browser moderno (Chrome, Firefox, Edge, Safari)
- Un editor di codice (VS Code, Sublime Text, ecc.)
- Conoscenza base di HTML/CSS
- Connessione internet

### Passo 1: Ottenere una API Key

1. Vai su [OpenWeatherMap](https://openweathermap.org/api)
2. Registrati gratuitamente (è gratuito per uso educativo)
3. Vai nella sezione "API keys"
4. Copia la tua API Key

### Passo 2: Configurare il Progetto

Apri il file `app.js` e sostituisci la tua API key:

```javascript
// Trova questa riga all'inizio del file
const API_KEY = 'YOUR_API_KEY_HERE';

// Sostituisci con la tua chiave
const API_KEY = 'tua_api_key_qui';
```

### Passo 3: Eseguire il Progetto

**Metodo 1: Apertura Diretta (Più Semplice)**

1. Scarica tutti i file nella stessa cartella
2. Fai doppio clic su `index.html`
3. Il progetto si aprirà nel tuo browser predefinito

**Metodo 2: Server Locale (Consigliato)**

```bash
# Se hai Python installato
python -m http.server 8000

# Se hai Node.js installato
npx serve

# Poi apri: http://localhost:8000
```

## 📖 Struttura del Progetto

```
weather-dashboard/
│
├── index.html          # Struttura HTML dell'applicazione
├── style.css           # Stili CSS con design responsive
├── app.js              # Logica JavaScript (commenti educativi)
├── README.md           # Questo file
└── .gitignore          # File ignorati da Git (opzionale)
```

## 🎨 Funzionalità

### 1. Ricerca Meteo per Città

- Inserisci il nome di una città italiana o mondiale
- Visualizza temperatura, umidità, vento, pressione
- Icone meteo dinamiche
- Descrizione in italiano

```javascript
// Esempio di come funziona (semplificato)
const searchCity = async (cityName) => {
    const response = await fetch(`api_url?q=${cityName}`);
    const data = await response.json();
    displayWeather(data);
};
```

### 2. Geolocalizzazione

- Usa la **Geolocation API** del browser
- Chiede il permesso all'utente
- Mostra il meteo della tua posizione attuale

```javascript
// Esempio semplificato
navigator.geolocation.getCurrentPosition(
    (position) => {
        const { latitude, longitude } = position.coords;
        fetchWeatherByCoords(latitude, longitude);
    }
);
```

### 3. Grafico delle Temperature

- Grafico interattivo delle prossime 24 ore
- Creato con **Chart.js**
- Responsive e touch-friendly

### 4. Salvataggio Città

- Salva fino a 10 città preferite
- Persistenza con **LocalStorage**
- Clicca su una città salvata per vedere il meteo

```javascript
// Salvataggio nel LocalStorage
localStorage.setItem('savedCities', JSON.stringify(cities));

// Recupero dal LocalStorage
const cities = JSON.parse(localStorage.getItem('savedCities'));
```

## 📚 Spiegazione dei Concetti Chiave

### Fetch API

La `fetch()` API è il modo moderno di fare richieste HTTP:

```javascript
// Sintassi base
fetch('https://api.example.com/data')
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));
```

### Async/Await

Rende il codice asincrono più leggibile:

```javascript
async function getData() {
    try {
        const response = await fetch('https://api.example.com/data');
        const data = await response.json();
        console.log(data);
    } catch (error) {
        console.error(error);
    }
}
```

### LocalStorage

Salva dati nel browser in modo persistente:

```javascript
// Salvare
localStorage.setItem('key', 'value');

// Recuperare
const value = localStorage.getItem('key');

// Nota: salva solo stringhe! Per oggetti:
const obj = { name: 'Mario', age: 30 };
localStorage.setItem('user', JSON.stringify(obj));
const user = JSON.parse(localStorage.getItem('user'));
```

### Arrow Functions

Sintassi concisa per le funzioni:

```javascript
// Funzione tradizionale
function add(a, b) {
    return a + b;
}

// Arrow function
const add = (a, b) => a + b;

// Con un solo parametro
const double = n => n * 2;

// Con corpo multiplo
const complex = (a, b) => {
    const result = a + b;
    return result * 2;
};
```

### Template Literals

Stringhe con espressioni incorporate:

```javascript
const name = 'Mario';
const age = 30;

// Stringhe tradizionali
const message1 = 'Ciao, ' + name + '! Hai ' + age + ' anni.';

// Template literals (backticks)
const message2 = `Ciao, ${name}! Hai ${age} anni.`;
```

### Destructuring

Estrazione proprietà da oggetti/array:

```javascript
// Object destructuring
const person = { name: 'Mario', age: 30, city: 'Roma' };
const { name, age } = person;
console.log(name); // 'Mario'

// Array destructuring
const numbers = [1, 2, 3, 4, 5];
const [first, second, ...rest] = numbers;
console.log(first); // 1
console.log(rest); // [3, 4, 5]
```

### Array Methods

```javascript
const numbers = [1, 2, 3, 4, 5];

// map: trasforma ogni elemento
const doubled = numbers.map(n => n * 2); // [2, 4, 6, 8, 10]

// filter: mantiene elementi che soddisfano una condizione
const evens = numbers.filter(n => n % 2 === 0); // [2, 4]

// forEach: esegue un'azione per ogni elemento
numbers.forEach(n => console.log(n));

// some: true se almeno un elemento soddisfa la condizione
const hasEven = numbers.some(n => n % 2 === 0); // true

// find: trova il primo elemento che soddisfa la condizione
const found = numbers.find(n => n > 2); // 3
```

## 🎓 Esercizi Proposti

Migliora le tue capacità con questi esercizi:

### Livello 1 (Principiante)

- [ ] Aggiungi un campo per la "velocità del vento" in km/h
- [ ] Mostra l'ora dell'ultimo aggiornamento
- [ ] Cambia i colori in base alla temperatura (blu per freddo, rosso per caldo)

### Livello 2 (Intermedio)

- [ ] Aggiungi un toggle per cambiare tra Celsius e Fahrenheit
- [ ] Implementa la possibilità di aggiornare i meteo ogni 5 minuti
- [ ] Aggiungi animazioni quando i dati cambiano

### Livello 3 (Avanzato)

- [ ] Crea un sistema di notifiche quando il meteo cambia drasticamente
- [ ] Implementa il caching per ridurre le chiamate API
- [ ] Aggiungi supporto per più lingue

## 🔧 Risoluzione dei Problemi

### Problema: "Città non trovata"

**Soluzione:**
- Verifica che il nome della città sia corretto
- Prova con il nome in inglese (es. "Rome" invece di "Roma")
- Controlla che la tua API key sia valida

### Problema: "Errore CORS"

**Soluzione:**
- Usa un server locale invece di aprire direttamente il file HTML
- Oppure usa l'estensione "CORS Unblock" del browser (solo per sviluppo)

### Problema: Il grafico non appare

**Soluzione:**
- Verifica di aver incluso Chart.js nell'HTML
- Controlla la console del browser per errori (F12 → Console)

## 📖 Risorse Utili

### Documentazione

- [MDN Web Docs - JavaScript](https://developer.mozilla.org/it/docs/Web/JavaScript)
- [MDN - Fetch API](https://developer.mozilla.org/it/docs/Web/API/Fetch_API)
- [MDN - Async/Await](https://developer.mozilla.org/it/docs/Web/JavaScript/Reference/Statements/async_function)
- [Chart.js Documentation](https://www.chartjs.org/docs/latest/)

### API

- [OpenWeatherMap API](https://openweathermap.org/api)
- [OpenWeatherMap - Come ottenere API Key](https://openweathermap.org/appid)

### Tutorial

- [JavaScript.info](https://javascript.info/)
- [W3Schools JavaScript](https://www.w3schools.com/js/)
- [JavaScript30](https://javascript30.com/) - 30 progetti JS vanilla

## 🤝 Contribuire

Questo è un progetto educativo. Sentiti libero di:

1. Fare un fork del progetto
2. Creare un branch per le tue feature (`git checkout -b feature/MiaFeature`)
3. Fare commit delle tue modifiche (`git commit -m 'Aggiunge MiaFeature'`)
4. Fare push al branch (`git push origin feature/MiaFeature`)
5. Aprire una Pull Request

## 📝 Licenza

Questo progetto è rilasciato sotto la licenza MIT. Sei libero di usarlo per scopi educativi e commerciali.

## 👨‍🏫 Note per gli Insegnanti

Questo progetto è progettato per essere utilizzato in corsi universitari di:

- Sviluppo Web
- Programmazione JavaScript
- Fondamenti di Informatica (modulo web)

**Tempo stimato di completamento:** 4-6 ore

**Prerequisiti per studenti:**
- Conoscenza base di HTML/CSS
- Fondamenti di programmazione (variabili, funzioni, loop)
- Nozioni base di programmazione orientata agli oggetti

**Obiettivi pedagogici:**
- Apprendere JavaScript moderno attraverso un progetto pratico
- Capire come integrare API esterne
- Sviluppare abilità di debug e problem solving
- Creare un portfolio project completo

## 📞 Supporto

Per domande o problemi:

1. Controlla la sezione "Risoluzione dei Problemi"
2. Cerca nella documentazione MDN
3. Apri una issue su GitHub (se disponibile)

---

**Creato con ❤️ per studenti che imparano JavaScript moderno**

Buon coding! 🚀

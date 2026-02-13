# 💱 Convertitore di Valuta

Un'applicazione web per la conversione di valute in tempo reale con tassi di cambio aggiornati, storia delle conversioni e interfaccia moderna.

![Convertitore di Valuta](https://img.shields.io/badge/versione-1.0-blue)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow)
![HTML5](https://img.shields.io/badge/HTML5-Canvas-orange)
![CSS3](https://img.shields.io/badge/CSS3-Flexbox%2FGrid-green)

## 🌟 Caratteristiche

- **✅ Conversione in tempo reale** - Tassi di cambio aggiornati da API gratuite
- **🌍 Valute supportate** - USD, EUR, GBP, JPY, CHF, CAD, AUD
- **📊 Storico conversioni** - Salva le ultime 10 conversioni in localStorage
- **🔄 Scambio rapido** - Inverti le valute con un click
- **✨ Validazione input** - Controllo errori e messaggi chiari
- **📱 Design responsivo** - Funziona su desktop e mobile
- **🎨 Interfaccia moderna** - Design dark mode con animazioni fluide
- **⚡ Performance** - Fetch API con async/await per chiamate asincrone

## 🚀 Dimostrazione Online

Puoi provare l'applicazione aprendo il file `index.html` nel tuo browser.

## 📦 Installazione

1. **Clona o scarica il progetto**
```bash
cd currency-converter
```

2. **Apri il file index.html**
```bash
# Apri semplicemente il file nel tuo browser preferito
open index.html
```

Nessuna dipendenza esterna richiesta! L'app utilizza solo HTML, CSS e JavaScript vanilla.

## 🎯 Funzionalità Principali

### Conversione Valuta

Il convertitore supporta le seguenti valute:
- **USD** - Dollaro Americano 🇺🇸
- **EUR** - Euro 🇪🇺
- **GBP** - Sterlina Britannica 🇬🇧
- **JPY** - Yen Giapponese 🇯🇵
- **CHF** - Franco Svizzero 🇨🇭
- **CAD** - Dollaro Canadese 🇨🇦
- **AUD** - Dollaro Australiano 🇦🇺

### Storico Conversioni

L'applicazione salva automaticamente le ultime 10 conversioni in localStorage, permettendoti di:
- 📜 Visualizzare lo storico delle conversioni
- 🗑️ Cancellare singole conversioni
- 🧹 Pulire l'intero storico

### Validazione Input

- ✅ Verifica che l'importo sia maggiore di zero
- ✅ Limita l'importo massimo a 1 miliardo
- ✅ Messaggi di errore chiari e dettagliati
- ✅ Feedback visivo per stati di caricamento

## 🛠️ Tecnologie Utilizzate

### HTML5
- Struttura semantica
- Form con validazione nativa
- Accessibilità (ARIA labels)

### CSS3
- **CSS Grid** - Layout responsive
- **CSS Variables** - Gestione colori temi
- **Flexbox** - Allineamento elementi
- **Animations** - Transizioni fluide
- **Media Queries** - Design responsivo
- **Dark Mode** - Interfaccia scura moderna

### JavaScript ES6+
- **Arrow Functions** - Sintassi concisa
- **Async/Await** - Gestione operazioni asincrone
- **Destructuring** - Estrazione proprietà oggetti
- **Template Literals** - Stringhe interpolate
- **Array Methods** - map(), filter(), slice()
- **Fetch API** - Chiamate HTTP asincrone
- **LocalStorage** - Persistenza dati locale
- **DOM Manipulation** - Manipolazione dinamica del DOM
- **Event Listeners** - Gestione interazioni utente

## 📁 Struttura del Progetto

```
currency-converter/
├── index.html          # Struttura HTML dell'applicazione
├── style.css           # Stili CSS con animazioni
├── converter.js        # Logica JavaScript (fetch, conversione, storage)
└── README.md           # Documentazione del progetto
```

## 🔧 API Utilizzata

L'applicazione utilizza **ExchangeRate-API** (https://www.exchangerate-api.com/):
- ✅ Gratuita
- ✅ Nessuna registrazione richiesta
- ✅ Tassi aggiornati giornalmente
- ✅ Supporto per tutte le valute principali
- ✅ Risposta JSON pulita e semplice

**Endpoint utilizzato:**
```
https://api.exchangerate-api.com/v4/latest/{BASE_CURRENCY}
```

**Esempio risposta:**
```json
{
  "rates": {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 149.50
  },
  "base": "USD",
  "date": "2025-01-15"
}
```

## 💻 Utilizzo del Codice

### Esempio di Conversione

```javascript
// Funzione principale di conversione
const convertCurrency = async (amount, from, to) => {
    try {
        const rates = await fetchExchangeRates(from);
        const convertedAmount = amount * rates[to];
        return convertedAmount;
    } catch (error) {
        throw new Error('Impossibile recuperare i tassi di cambio');
    }
};
```

### Salvataggio in LocalStorage

```javascript
// Salva la cronologia
const saveHistory = (history) => {
    localStorage.setItem(CONFIG.STORAGE_KEY, JSON.stringify(history));
};

// Carica la cronologia
const loadHistory = () => {
    const historyJSON = localStorage.getItem(CONFIG.STORAGE_KEY);
    return historyJSON ? JSON.parse(historyJSON) : [];
};
```

### Gestione Errori

```javascript
try {
    const result = await convertCurrency(amount, from, to);
    displayResult(result);
} catch (error) {
    showAlert(error.message, 'error');
}
```

## 🎨 Personalizzazione

### Cambiare Colori (CSS Variables)

Modifica le variabili in `style.css`:

```css
:root {
    --primary-color: #4f46e5;      /* Colore primario */
    --secondary-color: #10b981;    /* Colore secondario */
    --background: #0f172a;         /* Sfondo */
    --surface: #1e293b;            /* Superficie card */
}
```

### Aggiungere Nuove Valute

Aggiungi opzioni in `index.html`:

```html
<option value="INR">INR - Rupia Indiana</option>
```

E aggiungi il simbolo in `converter.js`:

```javascript
const currencySymbols = {
    INR: '₹'
};
```

## 🚀 Funzionalità Avanzate Implementate

### 1. **Async/Await Pattern**
```javascript
const fetchExchangeRates = async (baseCurrency) => {
    const response = await fetch(`${API_URL}${baseCurrency}`);
    const data = await response.json();
    return data.rates;
};
```

### 2. **Array Destructuring**
```javascript
const [from, to] = [elements.fromCurrency.value, elements.toCurrency.value];
```

### 3. **Spread Operator**
```javascript
const historyItem = {
    id: Date.now(),
    ...conversion,
    timestamp: new Date().toISOString()
};
```

### 4. **Array Methods**
```javascript
// Filter per rimozione elementi
const filtered = history.filter(item => item.id !== id);

// Map per rendering
const html = history.map(item => `<div>${item.amount}</div>`).join('');

// Slice per limitare elementi
const trimmed = history.slice(0, MAX_HISTORY);
```

## 🔒 Privacy e Sicurezza

- ✅ Nessun dato inviato a server di terze parti (tranne API tassi)
- ✅ Storico salvato solo localmente nel browser
- ✅ Nessun cookie o tracking
- ✅ Nessuna registrazione richiesta

## 📱 Compatibilità Browser

| Browser | Supporto |
|---------|----------|
| Chrome  | ✅ 90+ |
| Firefox | ✅ 88+ |
| Safari  | ✅ 14+ |
| Edge    | ✅ 90+ |
| Opera   | ✅ 76+ |

## 🐛 Bug Conosciuti

Nessun bug conosciuto al momento. Se trovi problemi, apri una issue!

## 🛣️ Roadmap

- [ ] Aggiungere altre valute (crypto, etc.)
- [ ] Grafico storico tassi di cambio
- [ ] Modalità offline con tassi salvati
- [ ] Confronto tra più valute
- [ ] API di backup se principale fallisce
- [ ] PWA per installazione

## 📝 Note di Sviluppo

### Concetti Appresi

Questo progetto dimostra la conoscenza di:
1. **Fetch API** - Chiamate HTTP asincrone
2. **Async/Await** - Gestione promise moderne
3. **LocalStorage** - Persistenza dati client-side
4. **DOM Manipulation** - Creazione dinamica UI
5. **Event Handling** - Gestione interazioni utente
6. **Error Handling** - Try/catch e feedback utente
7. **CSS Modern** - Grid, Flexbox, Animations
8. **ES6+ Features** - Arrow functions, destructuring, template literals

## 👨‍💻 Autore

Progetto creato per portfolio personale dimostrativo di competenze JavaScript ES6+.

## 📄 Licenza

Questo progetto è open source e disponibile per scopi educativi.

---

**Costruito con ❤️ usando HTML, CSS e JavaScript vanilla**

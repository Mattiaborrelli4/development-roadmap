# Struttura del Progetto - Convertitore di Valute

## 📊 Albero delle Directory Completo

```
currency-converter-app/
│
├── 📱 App.js                          # Entry Point dell'applicazione
├── ⚙️ app.json                        # Configurazione Expo (nome, icon, version)
├── 📦 package.json                    # Dipendenze e script npm
├── 🔧 babel.config.js                 # Configurazione Babel
├── 📝 README.md                       # Documentazione principale
├── 🚀 SETUP_GUIDE.md                  # Guida installazione
├── 🙈 .gitignore                      # File ignorati da Git
│
├── 📁 assets/                         # Asset statici
│   └── 📄 placeholder.txt             # Placeholder per icone e splash
│
└── 📁 src/                            # Codice sorgente principale
    │
    ├── 📁 components/                  # Componenti UI riutilizzabili
    │   ├── 💰 CurrencyInput.jsx       # Campo input per importo e valuta
    │   ├── 🌐 CurrencyPicker.jsx      # Modal per selezione valuta
    │   ├── 🔄 SwapButton.jsx          # Pulsante swap con animazione
    │   ├── 📊 ResultCard.jsx          # Card che mostra il risultato
    │   ├── ⭐ FavoritesBar.jsx         # Barra preferiti scorrevole
    │   └── 📜 HistoryList.jsx         # Lista cronologia conversioni
    │
    ├── 📁 screens/                     # Schermate dell'app
    │   └── 📱 ConverterScreen.jsx     # Schermata principale convertitore
    │
    ├── 📁 services/                    # Logica di business e API
    │   ├── 💱 currencyAPI.js          # Gestione API tassi di cambio
    │   │   ├── fetchExchangeRates()   # Fetch tassi da API
    │   │   ├── convertCurrency()      # Logica conversione
    │   │   ├── formatCurrency()       # Formattazione display
    │   │   └── areRatesValid()        # Verifica validità cache
    │   │
    │   └── 💾 storageService.js       # Gestione AsyncStorage
    │       ├── saveFavorites()        # Salva preferiti
    │       ├── loadFavorites()        # Carica preferiti
    │       ├── addFavorite()          # Aggiunge preferito
    │       ├── removeFavorite()       # Rimuove preferito
    │       ├── saveHistory()          # Salva cronologia
    │       ├── loadHistory()          # Carica cronologia
    │       ├── addToHistory()         # Aggiunge conversione
    │       ├── clearHistory()         # Pulisce cronologia
    │       ├── cacheRates()           # Cache tassi
    │       └── loadCachedRates()      # Carica tazzi cached
    │
    ├── 📁 hooks/                       # Custom React Hooks
    │   ├── 🌍 useCurrencies.js        # Hook per gestione tassi
    │   │   ├── rates                  # Oggetto tassi di cambio
    │   │   ├── isLoading              # Stato caricamento
    │   │   ├── isOnline               # Stato connessione
    │   │   ├── lastUpdate             # Timestamp ultimo agg.
    │   │   ├── error                  # Messaggi errore
    │   │   └── refreshRates()         # Funzione refresh manuale
    │   │
    │   └── 💱 useConverter.js         # Hook per conversioni
    │       ├── fromCurrency           # Valuta origine
    │       ├── toCurrency             # Valuta destinazione
    │       ├── amount                 # Importo
    │       ├── result                 # Risultato conversione
    │       ├── favorites              # Lista preferiti
    │       ├── history                # Lista cronologia
    │       ├── convert()              # Esegue conversione
    │       ├── swapCurrencies()       # Inverte valute
    │       ├── toggleFavorite()       # Aggiunge/Rimuove preferito
    │       └── loadData()             # Carica dati persistenti
    │
    ├── 📁 utils/                       # Utility e costanti
    │   └── 📋 constants.js             # Costanti globali
    │       ├── CURRENCIES[]           # Lista valute supportate
    │       ├── EXCHANGE_RATE_API_KEY  # Chiave API
    │       ├── STORAGE_KEYS           # Chiavi AsyncStorage
    │       └── MAX_HISTORY_ITEMS      # Limite cronologia (10)
    │
    └── 📁 styles/                      # Tema e stili
        └── 🎨 theme.js                # Definizione tema
            ├── COLORS                 # Palette colori
            ├── SPACING                # Spaziature
            ├── FONT_SIZES             # Dimensioni font
            ├── BORDER_RADIUS          # Raggi bordi
            └── SHADOWS                # Ombreggiature
```

## 📊 Flusso dei Dati

```
┌─────────────────────────────────────────────────────────┐
│                    App.js                               │
│                  (Entry Point)                          │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│             ConverterScreen.jsx                         │
│          (Schermata Principale)                         │
└───────┬─────────────────────────────────┬──────────────┘
        │                                 │
    ┌───▼─────┐                     ┌─────▼─────┐
    │  Hook   │                     │   Hook    │
    │ Currency│                     │ Converter │
    └────┬────┘                     └────┬──────┘
         │                               │
    ┌────▼─────┐                   ┌─────▼──────┐
    │ Services │                   │  Services  │
    │ currencyAPI│                 │storage     │
    └────┬─────┘                   └─────┬──────┘
         │                               │
    ┌────▼─────┐                   ┌─────▼──────┐
    │   API    │                   │AsyncStorage│
    │Exchange  │                   │  (Local)   │
    │  Rate    │                   └────────────┘
    └──────────┘
```

## 🔄 Ciclo di Vita dell'App

### 1. Avvio dell'App
```
App.js → ConverterScreen → useCurrencies Hook
  ↓
Caricamento tassi (API o Cache)
  ↓
Caricamento dati persistenti (preferiti, cronologia)
  ↓
Renderizzazione UI
```

### 2. Conversione
```
Utente inserisce importo
  ↓
useConverter Hook riceve input
  ↓
currencyAPI.convertCurrency()
  ↓
Aggiornamento stato result
  ↓
Render ResultCard
  ↓
storageService.addToHistory()
  ↓
Aggiornamento cronologia
```

### 3. Gestione Preferiti
```
Utente tocca ★ Salva
  ↓
useConverter.toggleFavorite()
  ↓
storageService.addFavorite() / removeFavorite()
  ↓
Aggiornamento stato favorites
  ↓
Render FavoritesBar
```

## 🎨 Component UI Architecture

### Gerarchia Componenti
```
ConverterScreen
├── Header (Status + Last Update)
├── FavoritesBar (Horizontal scroll)
├── CurrencyInput (From)
│   ├── TextInput (Amount)
│   └── TouchableOpacity (Currency Picker)
├── SwapButton (Animated)
├── CurrencyInput (To - Disabled)
├── ResultCard
│   ├── Result Amount
│   ├── Rate Info
│   ├── Fee (always 0)
│   └── Favorite Button
└── HistoryList (Horizontal scroll)
    └── History Items (Clickable)
```

### Modals
```
CurrencyPicker (Shared)
├── Modal Overlay
├── SafeAreaView
│   ├── Header (Title + Close)
│   └── FlatList (Currencies)
│       ├── Currency Item
│       │   ├── Flag
│       │   ├── Code + Name
│       │   └── Symbol
```

## 💾 Struttura Dati

### Conversion Result
```javascript
{
  from: 'USD',           // Valuta origine
  to: 'EUR',             // Valuta destinazione
  amount: 100,           // Importo
  result: 92.50,         // Risultato
  rate: 0.925,          // Tasso usato
  timestamp: '2026-02-12T10:30:00.000Z'
}
```

### Favorite Pair
```javascript
{
  from: 'USD',
  to: 'EUR'
}
```

### Exchange Rates
```javascript
{
  USD: 1.0,
  EUR: 0.925,
  GBP: 0.788,
  JPY: 149.50,
  CHF: 0.882,
  CAD: 1.35,
  AUD: 1.52
}
```

### Currency Info
```javascript
{
  code: 'USD',
  name: 'Dollaro Americano',
  symbol: '$',
  flag: '🇺🇸'
}
```

## 📡 API Integration

### Endpoint Utilizzati
```
GET https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{BASE}
```

### Esempio Response
```json
{
  "success": true,
  "base_code": "USD",
  "conversion_rates": {
    "USD": 1,
    "EUR": 0.925,
    "GBP": 0.788,
    "JPY": 149.50,
    "CHF": 0.882,
    "CAD": 1.35,
    "AUD": 1.52
  },
  "time_last_update": 1678123456
}
```

### Cache Strategy
- **Durata**: 1 ora
- **Storage**: AsyncStorage
- **Chiave**: `@currency_converter:rates_cache`
- **Validazione**: `areRatesValid(lastUpdate)`

## 🎯 Stato dell'Applicazione

### Stato Globale (useCurrencies)
- `rates`: Tassi di cambio correnti
- `isLoading`: Stato caricamento
- `isOnline`: Stato connessione
- `lastUpdate`: Timestamp ultimo aggiornamento
- `error`: Messaggio errore

### Stato Locale (useConverter)
- `fromCurrency`: Valuta selezionata "da"
- `toCurrency`: Valuta selezionata "a"
- `amount`: Importo inserito
- `result`: Risultato conversione
- `favorites`: Array preferiti
- `history`: Array cronologia

## 🔄 Gestione Offline

### Strategia Offline
1. **Cache First**: Carica sempre dalla cache
2. **Background Update**: Se online e cache vecchia (>1h), aggiorna
3. **Graceful Fallback**: Se API fallisce, usa cache
4. **Network Indicator**: Mostra stato Online/Offline

### Flusso Offline
```
App Start
  ↓
Carica Cache
  ↓
Check Network Status
  ├─ Online & Cache Old → Refresh
  ├─ Online & Cache Fresh → Use Cache
  └─ Offline → Use Cache (with warning)
```

## 🎨 Theming System

### Color Palette
```javascript
primary: '#4F46E5'      // Main actions, highlights
secondary: '#10B981'    // Success states
background: '#F9FAFB'  // App background
surface: '#FFFFFF'      // Cards, inputs
text: '#111827'        // Primary text
textSecondary: '#6B7280' // Secondary text
border: '#E5E7EB'      // Dividers
error: '#EF4444'       // Error states
```

### Spacing Scale
```javascript
xs: 4px,
sm: 8px,
md: 16px,
lg: 24px,
xl: 32px
```

## 🔐 Sicurezza e Privacy

### Gestione API Key
- Non mai hardcoded in produzione
- Usa variabili d'ambiente
- Non committare file .env
- Piano gratuito sufficiente per demo

### Privacy Dati
- Nessun dato personale salvato
- Solo conversioni e preferiti
- Storage locale cifrato
- Nessun tracking analytics

---

Questa struttura garantisce un codice pulito, manutenibile e scalabile.

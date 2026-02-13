# Guida all'Installazione - Convertitore di Valute

## 🚀 Avvio Rapido

### 1. Installazione delle Dipendenze

```bash
cd "C:\Users\matti\Desktop\Project Ideas Portfolio\08-Mobile-Projects\currency-converter-app"
npm install
```

### 2. Avvio dell'App

```bash
npm start
```

Questo avvierà il server di sviluppo Expo.

### 3. Esecuzione su Dispositivo

#### Opzione A: Expo Go (Più Semplice)
1. Scarica l'app **Expo Go** dal tuo store:
   - [Android Play Store](https://play.google.com/store/apps/details?id=host.exp.exponent)
   - [iOS App Store](https://apps.apple.com/app/expo-go/id982107779)

2. Scansiona il codice QR che appare nel terminale
3. L'app si aprirà automaticamente

#### Opzione B: Emulatori
```bash
# Android Emulator
npm run android

# iOS Simulator (solo macOS)
npm run ios

# Web Browser
npm run web
```

## 🔧 Configurazione API

### Chiave API (Opzionale ma Raccomandata)

L'app funziona anche senza configurazione, ma per limiti più elevati:

1. Vai su https://www.exchangerate-api.com/
2. Registrati gratuitamente
3. Copia la tua API key
4. Modifica `src/utils/constants.js`:

```javascript
export const EXCHANGE_RATE_API_KEY = 'LA_TUA_CHIAVE_API';
```

## 📱 Struttura dei File

```
currency-converter-app/
├── App.js                    # Entry point
├── package.json              # Dipendenze
├── app.json                  # Config Expo
├── babel.config.js           # Config Babel
├── src/
│   ├── components/           # Componenti UI
│   ├── screens/              # Schermate
│   ├── services/             # API e storage
│   ├── hooks/                # Custom hooks
│   ├── utils/                # Utilità
│   └── styles/               # Tema
└── assets/                   # Immagini e icone
```

## 🐛 Risoluzione dei Problemi

### "Cannot find module '@react-native-async-storage/async-storage'"
```bash
npm install @react-native-async-storage/async-storage
```

### "Cannot find module '@react-native-community/netinfo'"
```bash
npm install @react-native-community/netinfo
```

### L'app non si avvia su Expo Go
- Assicurati che dispositivo e PC siano sulla stessa rete WiFi
- Prova a usare "Tunnel" invece di "LAN" nel menu Expo
- Verifica che il firewall non blocchi la connessione

### Tassi di cambio non si aggiornano
- Controlla la connessione internet
- Tira verso il basso per refresh (pull-to-refresh)
- Verifica che l'API sia raggiungibile

## 📦 Dipendenze Principali

- `expo` ~50.0.0 - Platform SDK
- `react` 18.2.0 - React core
- `react-native` 0.73.2 - React Native framework
- `@react-native-async-storage/async-storage` - Storage locale
- `@react-native-community/netinfo` - Info di rete

## 🎨 Personalizzazione

### Cambiare Colori
Modifica `src/styles/theme.js`:
```javascript
export const COLORS = {
  primary: '#4F46E5',    // Colore principale
  secondary: '#10B981',   // Colore secondario
  // ... altri colori
};
```

### Aggiungere Valute
Modifica `src/utils/constants.js`:
```javascript
export const CURRENCIES = [
  { code: 'USD', name: 'Dollaro Americano', symbol: '$', flag: '🇺🇸' },
  // Aggiungi altre valute qui
];
```

## 🚀 Preparazione per la Produzione

### 1. Installa EAS CLI
```bash
npm install -g eas-cli
```

### 2. Configura il progetto
```bash
eas build:configure
```

### 3. Build per Android
```bash
eas build --platform android
```

### 4. Build per iOS (richiede Apple Developer Account)
```bash
eas build --platform ios
```

## 📖 Risorse

- [Expo Documentation](https://docs.expo.dev/)
- [React Native Documentation](https://reactnative.dev/)
- [Exchange Rate API Docs](https://www.exchangerate-api.com/docs/)

---

Buon sviluppo! 🎉

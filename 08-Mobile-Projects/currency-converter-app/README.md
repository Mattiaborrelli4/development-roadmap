# 💱 Convertitore di Valute

Un'app mobile completa per convertire valute in tempo reale, costruita con React Native ed Expo.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![React Native](https://img.shields.io/badge/React%20Native-0.73.2-61DAFB.svg)
![Expo](https://img.shields.io/badge/Expo-50.0.0-000000.svg)

## ✨ Caratteristiche

### Funzionalità Principali
- **🔄 Conversione Multi-Valuta**: Supporta USD, EUR, GBP, JPY, CHF, CAD, AUD
- **📡 Tassi in Tempo Reale**: Utilizza API gratuite per i tassi di cambio aggiornati
- **📡 Modalità Offline**: Funziona anche senza connessione utilizzando gli ultimi tassi cached
- **⭐ Preferiti**: Salva le coppie di valute più usate per accesso rapido
- **📜 Cronologia**: Mantiene gli ultimi 10 conversioni
- **🔘 Swap Rapido**: Inverti le valute con un'animazione fluida
- **🎨 UI Intuitiva**: Design pulito e moderno con indicatori di stato

### Dettagli Tecnici
- **Cache Intelligente**: I tassi vengono cached per 1 ora
- **Indicatori di Rete**: Mostra lo stato della connessione (Online/Offline)
- **Aggiornamento Pull-to-Refresh**: Aggiorna i tazi scorrendo verso il basso
- **Validazione Input**: Solo numeri e punto decimale consentiti
- **Formattazione Valuta**: Display formattato secondo gli standard italiani

## 🛠️ Tecnologie Utilizzate

- **React Native** 0.73.2 - Framework mobile
- **Expo** 50.0.0 - Piattaforma di sviluppo
- **AsyncStorage** - Persistenza dati locale
- **NetInfo** - Rilevamento stato rete
- **Animated API** - Animazioni fluide
- **Exchange Rate API** - Tassi di cambio in tempo reale

## 📦 Installazione

### Prerequisiti
- Node.js (v18 o superiore)
- npm o yarn
- Expo Go app (per testing su dispositivo)

### Passaggi

1. **Clona o naviga nella directory del progetto**
```bash
cd "C:\Users\matti\Desktop\Project Ideas Portfolio\08-Mobile-Projects\currency-converter-app"
```

2. **Installa le dipendenze**
```bash
npm install
```

3. **Configura la chiave API** (Opzionale)
```bash
# Apri src/utils/constants.js
# Sostituisci 'YOUR_API_KEY_HERE' con la tua chiave gratuita da https://www.exchangerate-api.com/
```

4. **Avvia l'app**
```bash
# Per Expo Go (consigliato per sviluppo)
npm start

# Per emulatori specifici
npm run android  # Emulator Android
npm run ios      # Simulator iOS (solo macOS)
npm run web      # Browser web
```

5. **Scansiona il codice QR** con l'app Expo Go sul tuo dispositivo

## 📁 Struttura del Progetto

```
currency-converter-app/
├── App.js                          # Entry point principale
├── app.json                        # Configurazione Expo
├── package.json                    # Dipendenze
├── src/
│   ├── components/                 # Componenti UI riutilizzabili
│   │   ├── CurrencyInput.jsx       # Input per importo e valuta
│   │   ├── CurrencyPicker.jsx      # Modal selezione valuta
│   │   ├── SwapButton.jsx          # Pulsante swap con animazione
│   │   ├── ResultCard.jsx          # Card risultato conversione
│   │   ├── HistoryList.jsx         # Lista cronologia orizzontale
│   │   └── FavoritesBar.jsx         # Barra preferiti
│   ├── screens/
│   │   └── ConverterScreen.jsx     # Schermata principale
│   ├── services/                   # Logica di business
│   │   ├── currencyAPI.js          # API tassi di cambio
│   │   └── storageService.js       # Gestione AsyncStorage
│   ├── hooks/                      # Custom React Hooks
│   │   ├── useCurrencies.js        # Gestione tassi e rete
│   │   └── useConverter.js         # Logica conversione
│   ├── utils/
│   │   └── constants.js            # Costanti e configurazioni
│   └── styles/
│       └── theme.js                # Tema colori e stili
└── README.md                       # Documentazione
```

## 🎯 Funzionalità nel Dettaglio

### Conversione
- Inserisci l'importo nel campo "Da"
- Seleziona le valute dai picker
- Il risultato viene calcolato automaticamente
- Tasso di cambio e dettagli mostrati nella card risultato

### Preferiti
- Tocca il pulsante "★ Salva" per aggiungere una coppia ai preferiti
- I preferiti appaiono in una barra scorrevole
- Tocca un preferito per caricare velocemente quella coppia

### Cronologia
- Ultimi 10 conversioni salvate automaticamente
- Scorri orizzontalmente per vedere la cronologia
- Tocca un item per riutilizzare quella conversione
- Pulisci la cronologia con il pulsante "Pulisci"

### Offline
- L'app funziona anche senza connessione
- Utilizza gli ultimi tazzi cached
- Mostra un avviso quando è in modalità offline
- Aggiorna automaticamente quando torna online

## 🎨 Tema e Colori

```javascript
Colori Principali:
- Primary: #4F46E5 (Indaco)
- Secondary: #10B981 (Verde)
- Background: #F9FAFB (Grigio chiaro)
- Surface: #FFFFFF (Bianco)
- Text: #111827 (Nero)
```

## 🔧 Configurazione API

### Exchange Rate API

L'app utilizza **exchangerate-api.com** per i tassi di cambio:

1. **Piano Gratuito** (già configurato):
   - 1,500 richieste/mese
   - Aggiornamento ogni ora
   - Nessuna chiave richiesta per base

2. **Piano Pro** (opzionale):
   - Registrati su https://www.exchangerate-api.com/
   - Ottieni una chiave API gratuita
   - Inseriscila in `src/utils/constants.js`

```javascript
export const EXCHANGE_RATE_API_KEY = 'TUA_CHIAVE_API';
```

## 📱 Schermate

### Schermata Principale
- **Header**: Titolo, stato aggiornamento, indicatore Online/Offline
- **Preferiti**: Barra scorrevole con coppie salvate
- **Input Da**: Campo importo + selettore valuta
- **Swap Button**: Pulsante animato per invertire valute
- **Input A**: Campo risultato (read-only) + selettore valuta
- **Risultato**: Card con dettagli conversione
- **Cronologia**: Scorimentale orizzontale

### Modal Selezione Valuta
- Lista completa delle valute supportate
- Flag emoji per identificazione visiva
- Nome completo valuta
- Simbolo valuta
- Valuta corrente evidenziata

## 🚀 Deploy

### Google Play Store
1. Segui la guida Expo per [EAS Build](https://docs.expo.dev/build/introduction/)
2. Configura `app.json` con i tuoi dettagli
3. Build APK o AAB
4. Carica su Google Play Console

### Apple App Store
1. Richiede account Apple Developer
2. Configura `app.json` con bundle identifier
3. Build con EAS Build
4. Carica su App Store Connect

## 🐛 Troubleshooting

### Problema: Tassi non si aggiornano
- **Soluzione**: Controlla la connessione internet
- **Verifica**: L'indicatore deve mostrare "Online"

### Problema: App non funziona offline
- **Soluzione**: Apri l'app almeno una volta connesso
- **Motivo**: Devi scaricare i tazzi almeno una volta

### Problema: Cronologia non si salva
- **Soluzione**: Riavvia l'app
- **Nota**: AsyncStorage potrebbe essere stato pulito

### Problema: Input non accetta numeri
- **Soluzione**: Verifica che la tastiera sia impostata su "decimale"
- **Nota**: Solo numeri e punto decimale sono consentiti

## 📄 Licenza

Questo progetto è stato creato a scopo educativo.

## 👨‍💻 Sviluppatore

Progetto realizzato come parte del portfolio di idee progettuali.

## 🙏 Ringraziamenti

- [Expo](https://expo.dev/) - Framework di sviluppo
- [Exchange Rate API](https://www.exchangerate-api.com/) - API tassi di cambio
- [React Native](https://reactnative.dev/) - Framework mobile

---

**Nota**: Questa app utilizza le API gratuite. Per uso in produzione, considera di registrarti per ottenere una chiave API personale con limiti più elevati.

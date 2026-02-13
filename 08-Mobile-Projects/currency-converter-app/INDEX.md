# 📚 Indice Documentazione - Convertitore di Valute

Benvenuto nella documentazione completa del progetto **Convertitore di Valute** React Native.

## 🚀 Quick Start

**Se vuoi iniziare subito:**
1. Leggi [SETUP_GUIDE.md](SETUP_GUIDE.md) - Guida installazione passo-passo
2. Esegui `npm install` e `npm start`
3. Scansiona il QR con Expo Go

## 📖 Documentazione

### Per Principianti
| Documento | Descrizione | Quando leggerlo |
|-----------|-------------|-----------------|
| [README.md](README.md) | Documentazione italiana completa | Prima di tutto |
| [SETUP_GUIDE.md](SETUP_GUIDE.md) | Guida installazione e configurazione | Per avviare il progetto |
| [FEATURES_CHECKLIST.md](FEATURES_CHECKLIST.md) | Lista completezza funzionalità | Per vedere cosa è implementato |

### Per Sviluppatori
| Documento | Descrizione | Quando leggerlo |
|-----------|-------------|-----------------|
| [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) | Guida sviluppo con snippet codice | Per modificare il codice |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | Architettura e struttura dettagliata | Per capire l'organizzazione |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Riepilogo progetto con statistiche | Per una panoramica veloce |
| [VISUAL_OVERVIEW.md](VISUAL_OVERVIEW.md) | Overview visuale UI e flussi | Per capire design e UX |

## 📁 Struttura Progetto

```
currency-converter-app/
│
├── 📱 App.js                    # Entry point
├── ⚙️ Configurazione
│   ├── package.json
│   ├── app.json
│   └── babel.config.js
│
├── 📁 src/                      # Codice sorgente
│   ├── components/              # 6 componenti UI
│   ├── screens/                 # 1 schermata
│   ├── services/                # 2 services (API, Storage)
│   ├── hooks/                   # 2 custom hooks
│   ├── utils/                   # Constants
│   └── styles/                  # Theme
│
└── 📚 Documentation (7 files)
```

## 🎯 Cosa Puoi Fare

### Come Utente
- ✅ Convertire tra 7 valute (USD, EUR, GBP, JPY, CHF, CAD, AUD)
- ✅ Salvare preferiti per accesso rapido
- ✅ Vedere cronologia conversioni
- ✅ Usare l'app offline
- ✅ Aggiornare tazi con pull-to-refresh

### Come Sviluppatore
- ✅ Aggiungere nuove valute
- ✅ Modificare il tema colori
- ✅ Cambiare API provider
- ✅ Estendere funzionalità
- ✅ Deploy su store

## 📊 Statistiche Veloci

- **File totali**: 27
- **Righe di codice**: ~1,500
- **Componenti**: 6
- **Documentazione**: 7 file MD
- **Valute supportate**: 7
- **Lingue**: Italiano

## 🔗 Link Rapidi

### Installazione
```bash
cd "C:\Users\matti\Desktop\Project Ideas Portfolio\08-Mobile-Projects\currency-converter-app"
npm install
npm start
```

### File Chiave
- **Entry Point**: `C:\...\currency-converter-app\App.js`
- **Main Screen**: `src/screens/ConverterScreen.jsx`
- **Theme**: `src/styles/theme.js`
- **Constants**: `src/utils/constants.js`

### API Integration
- **Provider**: Exchange Rate API
- **Endpoint**: `https://v6.exchangerate-api.com/v6/`
- **Cache**: 1 ora
- **Fallback**: AsyncStorage

## 🎨 Panoramica Componenti

### UI Components
- **CurrencyInput** - Input + currency selector
- **CurrencyPicker** - Modal con lista valute
- **SwapButton** - Button swap animato
- **ResultCard** - Card risultato conversione
- **FavoritesBar** - Barra preferiti scorrevole
- **HistoryList** - Lista cronologia orizzontale

### Services
- **currencyAPI** - Gestione API tassi
- **storageService** - Gestione AsyncStorage

### Hooks
- **useCurrencies** - Stato tassi e rete
- **useConverter** - Logica conversione

## 🛠️ Troubleshooting

### Problema: `npm install` fallisce
**Soluzione**: Assicurati di avere Node.js 18+ installato

### Problema: App non si avvia
**Soluzione**: Vedi [SETUP_GUIDE.md](SETUP_GUIDE.md) sezione Troubleshooting

### Problema: Tassi non si aggiornano
**Soluzione**: Verifica connessione internet, controlla che l'indicatore sia "Online"

### Problema: Come aggiungo una valuta?
**Soluzione**: Vedi [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) sezione "Aggiungere Nuova Valuta"

## 📚 Risorse Esterne

- [React Native Docs](https://reactnative.dev/)
- [Expo Documentation](https://docs.expo.dev/)
- [Exchange Rate API](https://www.exchangerate-api.com/)
- [AsyncStorage](https://react-native-async-storage.github.io/async-storage/)

## 🎯 Roadmap

### Phase 1: Core ✅ (Completato)
- [x] Conversion base
- [x] API integration
- [x] Offline support
- [x] Favorites & history

### Phase 2: Enhancement (Futuro)
- [ ] Charts storici
- [ ] Alerts tassi
- [ ] Dark mode
- [ ] Biometric auth

### Phase 3: Production (Futuro)
- [ ] EAS Build setup
- [ ] Store deployment
- [ ] Analytics
- [ ] Crash reporting

## 📞 Support

Per domande o problemi:
1. Controlla [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)
2. Leggi [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
3. Vedi [SETUP_GUIDE.md](SETUP_GUIDE.md) troubleshooting

## 🎉 Buon Lavoro!

Il progetto è completo e pronto per l'uso. Tutta la documentazione necessaria è disponibile in questa directory.

---

**Ultimo aggiornamento**: 12 Febbraio 2026
**Versione**: 1.0.0
**Stato**: ✅ COMPLETATO

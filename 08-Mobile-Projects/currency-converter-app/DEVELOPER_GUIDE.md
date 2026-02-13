# Guida per Sviluppatori - Convertitore di Valute

## 🚀 Quick Start

```bash
# Installazione
cd "C:\Users\matti\Desktop\Project Ideas Portfolio\08-Mobile-Projects\currency-converter-app"
npm install

# Avvio sviluppo
npm start

# Scan QR con Expo Go
```

## 🎯 Comandi npm Disponibili

```bash
npm start          # Avvia server Expo
npm run android   # Avvia emulatore Android
npm run ios       # Avvia simulatore iOS (solo macOS)
npm run web       # Avvia versione web
```

## 📋 Panoramica Architettura

### Layer Architecture
```
Presentation Layer (Components/Screens)
         ↓
Business Logic (Hooks)
         ↓
Services (API, Storage)
         ↓
Data Sources (API, AsyncStorage)
```

### Componenti Principali

#### 1. **ConverterScreen** (Schermata Principale)
- **Path**: `src/screens/ConverterScreen.jsx`
- **Responsabilità**: Orchestratore dell'intera UI
- **Dipendenze**: useCurrencies, useConverter hooks

```javascript
// Esempio di utilizzo
const {
  rates, isLoading, isOnline, lastUpdate, error, refreshRates
} = useCurrencies();

const {
  fromCurrency, toCurrency, amount, result,
  convert, swapCurrencies, toggleFavorite
} = useConverter(rates);
```

#### 2. **useCurrencies** Hook
- **Path**: `src/hooks/useCurrencies.js`
- **Responsabilità**: Gestione tassi di cambio e stato rete
- **Returns**: `{ rates, isLoading, isOnline, lastUpdate, error, refreshRates }`

```javascript
// Refresh manuale tassi
await refreshRates();

// Verifica stato online
if (isOnline) {
  // Scarica nuovi tassi
}
```

#### 3. **useConverter** Hook
- **Path**: `src/hooks/useConverter.js`
- **Responsabilità**: Logica conversione e gestione stato locale
- **Returns**: Oggetto con stato e funzioni

```javascript
// Esegui conversione
convert();

// Inverti valute
swapCurrencies();

// Toggle preferito
toggleFavorite();
```

## 🔧 Modifiche Comuni

### Aggiungere Nuova Valuta

**File**: `src/utils/constants.js`

```javascript
export const CURRENCIES = [
  // ... valute esistenti
  { code: 'CNY', name: 'Yuan Cinese', symbol: '¥', flag: '🇨🇳' },
  { code: 'INR', name: 'Rupia Indiana', symbol: '₹', flag: '🇮🇳' },
];
```

### Cambiare API Provider

**File**: `src/services/currencyAPI.js`

```javascript
// Modifica fetchExchangeRates
export const fetchExchangeRates = async (baseCurrency = 'USD') => {
  // Sostituisci URL del nuovo provider
  const url = `https://api.newprovider.com/rates/${baseCurrency}`;

  const response = await fetch(url);
  // Adatta parsing response
};
```

### Personalizzare Colori

**File**: `src/styles/theme.js`

```javascript
export const COLORS = {
  primary: '#YOUR_COLOR',      // Colore principale
  secondary: '#YOUR_COLOR',    // Colore secondario
  // ... altri colori
};
```

## 🎨 Custom Hooks Patterns

### Pattern 1: Stato + Logica
```javascript
// useConverter.js - Stato locale
const [amount, setAmount] = useState('');
const [result, setResult] = useState(null);

// Funzione che usa lo stato
const convert = useCallback(() => {
  if (!rates || !amount) return;
  const conversion = convertCurrency(amount, from, to, rates);
  setResult(conversion);
}, [rates, amount, from, to]);
```

### Pattern 2: Side Effects
```javascript
// useCurrencies.js - useEffect con dipendenze
useEffect(() => {
  const unsubscribe = NetInfo.addEventListener((state) => {
    setIsOnline(state.isConnected);
    // Aggiorna se torni online
  });
  return () => unsubscribe(); // Cleanup
}, []);
```

## 📡 Gestione API

### Chiamata API Standard

```javascript
// 1. Fetch
const response = await fetch(url);

// 2. Parse JSON
const data = await response.json();

// 3. Check errori
if (data.success === false) {
  throw new Error(data.error_type);
}

// 4. Return data
return { rates: data.conversion_rates, base: data.base_code };
```

### Gestione Errori

```javascript
try {
  const data = await fetchExchangeRates();
  setRates(data.rates);
} catch (error) {
  // Fallback su cache
  const cached = await loadCachedRates();
  if (cached) {
    setRates(cached);
    setError('Utilizzando tazzi cached');
  } else {
    setError('Nessun tasso disponibile');
  }
}
```

## 💾 Gestione Stato Persistente

### Salvataggio
```javascript
import { saveFavorites } from '../services/storageService';

await saveFavorites(favorites);
```

### Caricamento
```javascript
import { loadFavorites } from '../services/storageService';

const favorites = await loadFavorites();
setFavorites(favorites);
```

### Pattern CRUD
```javascript
// Create
await addFavorite(from, to);

// Read
const favorites = await loadFavorites();

// Update
await saveFavorites(updatedFavorites);

// Delete
await removeFavorite(from, to);
```

## 🎨 Styling Best Practices

### Usa il tema centralizzato
```javascript
import { COLORS, SPACING, FONT_SIZES } from '../styles/theme';

// ❌ NO - Hardcoded values
style={{ backgroundColor: '#4F46E5', padding: 16 }}

// ✅ SI - Theme constants
style={{ backgroundColor: COLORS.primary, padding: SPACING.md }}
```

### StyleSheet ottimizzato
```javascript
const styles = StyleSheet.create({
  container: {
    // Proprietà statiche
    flex: 1,
    backgroundColor: COLORS.background,
  },
  dynamic: (isActive) => ({
    // Proprietà dinamiche
    backgroundColor: isActive ? COLORS.primary : COLORS.surface,
  }),
});

// Uso
<View style={styles.container} />
<View style={styles.dynamic(isActive)} />
```

## 🔄 Gestione Stato Complesso

### Stato locale vs globale

```javascript
// ✅ Locale - Component-specific
const [isModalVisible, setIsModalVisible] = useState(false);

// ✅ Locale - Business logic specific
const [amount, setAmount] = useState('');

// ❌ Evita stato globale per valute semplici
// Usa invece props o context
```

### Performance Optimization

```javascript
// ✅ UseCallback per funzioni expensive
const convert = useCallback(() => {
  // Calcoli complessi
}, [rates, amount, from, to]);

// ✅ useMemo per valori calcolati
const formattedResult = useMemo(() => {
  return formatCurrency(result);
}, [result]);
```

## 🐛 Debugging

### Console Logging
```javascript
// Logging strutturato
console.log('Conversion:', {
  from, to, amount, result: result?.result
});

// Error tracking
console.error('API Error:', error.message);
```

### React DevTools
```javascript
// Aggiungi displayName per debug
ConverterScreen.displayName = 'ConverterScreen';

// Usa React DevTools per ispezionare props/state
```

## 🧪 Testing (Futuro)

### Unit Tests Example
```javascript
// Test conversione
test('convertCurrency returns correct result', () => {
  const rates = { USD: 1, EUR: 0.925 };
  const result = convertCurrency(100, 'USD', 'EUR', rates);
  expect(result.result).toBe(92.50);
});
```

## 📱 Deploy Checklist

### Pre-Produzione
- [ ] Rimuovi tutti i console.log
- [ ] Configura chiave API produzione
- [ ] Verifica dimensioni asset
- [ ] Testa modalità offline
- [ ] Verifica crash handling

### Build Commands
```bash
# Android APK
eas build --platform android --profile preview

# iOS IPA
eas build --platform ios --profile preview

# Production
eas build --platform android --profile production
```

## 🔒 Sicurezza

### API Keys
```javascript
// ❌ MAI hardcoded in produzione
export const API_KEY = 'sk_live_xxxxx';

// ✅ Usa environment variables
export const API_KEY = process.env.EXPO_PUBLIC_API_KEY;

// ✅ O .env file (in .gitignore)
EXPO_PUBLIC_API_KEY=sk_live_xxxxx
```

### Validazione Input
```javascript
// Sanitize input
const handleAmountChange = (value) => {
  // Rimuovi caratteri non numerici
  const cleaned = value.replace(/[^0-9.]/g, '');

  // Verifica formato
  const parts = cleaned.split('.');
  if (parts.length > 2) return; // Troppi punti

  setAmount(cleaned);
};
```

## 📚 Risorse Utili

- [React Native Docs](https://reactnative.dev/)
- [Expo Documentation](https://docs.expo.dev/)
- [React Hooks](https://react.dev/reference/react)
- [AsyncStorage](https://react-native-async-storage.github.io/async-storage/)

## 🆘 Troubleshooting Comuni

### Metro bundler non funziona
```bash
# Clear cache
npx expo start -c
```

### Dipendenze non installate
```bash
# Reinstalla node_modules
rm -rf node_modules
npm install
```

### App non si aggiorna
```bash
# Clear bundler cache
npx expo start --clear
```

---

Buon coding! 🚀

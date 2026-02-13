# 🎨 Visual Overview - Convertitore di Valute

## 📱 Interface Preview

```
┌─────────────────────────────────────────┐
│  Convertitore Valute        ● Online   │
│  Aggiornato 5 min fa                  │
├─────────────────────────────────────────┤
│ Preferiti:                             │
│ [USD/EUR] [GBP/JPY] [CAD/AUD]         │
├─────────────────────────────────────────┤
│                                       │
│  Da                                   │
│ ┌──────────────────┬──┐              │
│ │     100.00       │USD│              │
│ └──────────────────┴──┘              │
│                                       │
│            [🔄]                        │
│                                       │
│  A                                    │
│ ┌──────────────────┬──┐              │
│ │      92.50       │EUR│              │
│ └──────────────────┴──┘              │
│                                       │
├─────────────────────────────────────────┤
│ Risultato              [★ Salva]      │
│                                       │
│          € 92.50                       │
│                                       │
│ Tasso: 1 USD = 0.9250 EUR             │
│ Importo: $100.00                      │
│ Commissione: € 0.00                   │
├─────────────────────────────────────────┤
│ Conversioni Recenti           [Pulisci]│
│ [USD→EUR] [EUR→GBP] [JPY→USD] ...    │
└─────────────────────────────────────────┘
```

## 🔄 User Flow

### 1. Prima Conversione
```
Apertura App
    ↓
Caricamento Tazzi (Online/Offline)
    ↓
Input: "100" nel campo "DA"
    ↓
Selezione: "USD" → "EUR"
    ↓
Auto-calc dopo 500ms
    ↓
Risultato: "€ 92.50"
    ↓
Salvato in Cronologia
```

### 2. Salvataggio Preferito
```
Tocca "★ Salva"
    ↓
Coppia salvata (USD/EUR)
    ↓
Appare in barra "Preferiti"
    ↓
Tap per quick-select futuro
```

### 3. Riutilizzo Cronologia
```
Scroll cronologia
    ↓
Tap su item "USD→EUR: $100"
    ↓
Form pre-compilato
    ↓
Pronto per nuova conversione
```

## 🎨 Component Hierarchy

```
<ConverterScreen>
 │
 ├─ <StatusBar />
 │
 ├─ <View> // Header
 │   ├─ <Text> // Title
 │   ├─ <Text> // Last Update
 │   └─ <View> // Status Indicator
 │       ├─ <View> // Status Dot
 │       └─ <Text> // Online/Offline
 │
 ├─ <ScrollView>
 │   │
 │   ├─ <FavoritesBar>
 │   │   └─ <ScrollView horizontal>
 │   │       └─ [<TouchableOpacity> x N]
 │   │
 │   ├─ <CurrencyInput> // FROM
 │   │   ├─ <Text> // Label
 │   │   └─ <View>
 │   │       ├─ <TextInput> // Amount
 │   │       └─ <TouchableOpacity> // Currency Button
 │   │
 │   ├─ <SwapButton>
 │   │   └─ <Animated.View>
 │   │       └─ <TouchableOpacity> // Arrows
 │   │
 │   ├─ <CurrencyInput> // TO (disabled)
 │   │   └─ // (stesso sopra)
 │   │
 │   ├─ <ResultCard>
 │   │   ├─ <View> // Header
 │   │   │   ├─ <Text> // Label
 │   │   │   └─ <TouchableOpacity> // Favorite
 │   │   ├─ <Text> // Result Amount
 │   │   └─ <View> // Details
 │   │       ├─ <Text> // Rate
 │   │       ├─ <Text> // Amount
 │   │       └─ <Text> // Fee
 │   │
 │   └─ <HistoryList>
 │       ├─ <View> // Header
 │       └─ <ScrollView horizontal>
 │           └─ [<TouchableOpacity> x N]
 │               ├─ <Text> // Currencies
 │               ├─ <Text> // Amount
 │               ├─ <Text> // Result
 │               └─ <Text> // Rate
 │
 └─ <Modal> // Currency Picker
     ├─ <SafeAreaView>
     │   ├─ <View> // Header
     │   │   ├─ <Text> // Title
     │   │   └─ <TouchableOpacity> // Close
     │   └─ <FlatList>
     │       └─ [<TouchableOpacity> x 7] // Currencies
     │           ├─ <Text> // Flag
     │           ├─ <View>
     │           │   ├─ <Text> // Code
     │           │   └─ <Text> // Name
     │           └─ <Text> // Symbol
```

## 🎯 State Management Flow

```
┌─────────────────────────────────────────────────────┐
│                   App.js                           │
└──────────────────┬────────────────────────────────┘
                   │
         ┌─────────▼─────────┐
         │ ConverterScreen   │
         └─────────┬─────────┘
                   │
      ┌────────────┼────────────┐
      │            │            │
 ┌────▼─────┐ ┌───▼────┐ ┌────▼────┐
 │useCurrencies│useConverter│Local State│
 └────┬─────┘ └───┬────┘ └─────────┘
      │           │
      │     ┌─────┴─────┐
      │     │           │
 ┌─────▼───▼──┐   ┌───▼──────┐
 │Services   │   │UI Events │
 │           │   │          │
 │- currencyAPI│   │- onChange│
 │- storage  │   │- onPress │
 └─────┬─────┘   └──────────┘
       │
 ┌─────▼─────┐
 │Data Layer│
 │          │
 │- API    │
 │- AsyncStorage│
 └──────────┘
```

## 🔄 Data Flow Examples

### Conversion Flow
```
User Types "100"
    ↓
CurrencyInput onChangeText
    ↓
ConverterScreen handleAmountChange("100")
    ↓
useConverter.setAmount("100")
    ↓
useEffect detects amount change
    ↓
useConverter.convert()
    ↓
currencyAPI.convertCurrency(100, USD, EUR, rates)
    ↓
Update result state
    ↓
ResultCard re-renders with new value
    ↓
storageService.addToHistory(result)
    ↓
HistoryList updates with new entry
```

### Currency Picker Flow
```
User taps currency button
    ↓
setShowPicker(true)
    ↓
CurrencyPicker modal renders
    ↓
User taps "EUR"
    ↓
onSelect("EUR")
    ↓
setFromCurrency("EUR") / setToCurrency("EUR")
    ↓
setShowPicker(false)
    ↓
useEffect triggers re-conversion with new currency
```

### Favorites Flow
```
User taps "★ Salva"
    ↓
useConverter.toggleFavorite()
    ↓
Check if exists in favorites array
    ↓
if exists: removeFavorite(from, to)
if not: addFavorite(from, to)
    ↓
storageService.saveFavorites(updated)
    ↓
Update favorites state
    ↓
FavoritesBar re-renders
```

## 🎨 Color Usage

```
Primary (#4F46E5):
  - Currency buttons
  - Active favorite
  - Selected currency in picker
  - Refresh indicator

Secondary (#10B981):
  - Online status dot

Error (#EF4444):
  - Offline status dot
  - Error messages
  - Error container border

Surface (#FFFFFF):
  - Cards
  - Inputs
  - Modals
  - Picker items

Background (#F9FAFB):
  - App background
  - Disabled input background

Text (#111827):
  - Primary text
  - Labels
  - Currency amounts

TextSecondary (#6B7280):
  - Secondary text
  - Subtitles
  - Update timestamps
```

## 📏 Spacing Examples

```
CONTAINER MARGINS:
  Horizontal: SPACING.md (16px)
  Vertical: SPACING.md (16px)

BETWEEN SECTIONS:
  FavoritesBar → CurrencyInput: SPACING.md (16px)
  CurrencyInput → SwapButton: SPACING.xs (4px)
  SwapButton → CurrencyInput: SPACING.xs (4px)
  CurrencyInput → ResultCard: SPACING.md (16px)
  ResultCard → HistoryList: SPACING.lg (24px)

INSIDE COMPONENTS:
  Input padding: SPACING.md (16px)
  Card padding: SPACING.lg (24px)
  Button padding: SPACING.md/SM (16px vertical)
  Gap between items: SPACING.sm (8px)
```

## 🎯 Interaction States

### Button States
```
Normal:
  background: COLORS.primary
  opacity: 1.0

Pressed:
  opacity: 0.8 (activeOpacity)

Disabled:
  background: COLORS.background
  text: COLORS.textSecondary
```

### Input States
```
Normal:
  border: COLORS.border
  background: COLORS.surface

Focused:
  (uses default focus indicator)

Disabled:
  background: COLORS.background
  text: COLORS.textSecondary
  editable: false
```

### Loading States
```
Initial Load:
  refreshControl refreshing={true}
  UI shows skeleton

Refreshing:
  refreshControl refreshing={true}
  Pull gesture indicator

Converting:
  result hidden until complete
  (no loading indicator, 500ms delay)
```

## 📱 Responsive Behavior

```
PORTRAIT (Default):
  - Single column layout
  - Full width inputs
  - Vertical scroll

LANDSCAPE (Not optimized):
  - Same layout
  - May need horizontal scroll

DYNAMIC SIZING:
  - Flex-based layouts
  - Percentage widths where appropriate
  - Fixed heights for horizontal lists
```

---

Questa overview fornisce una comprensione visiva completa dell'architettura, flussi e design dell'app.

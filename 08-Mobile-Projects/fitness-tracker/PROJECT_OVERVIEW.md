# 📱 Fitness Tracker App - Panoramica del Progetto

## 🎯 Panoramica

Un'applicazione React Native completa per il tracciamento fitness con Expo, che include:
- Conteggio passi in tempo reale con pedometro
- Gestione completa degli allenamenti
- Analisi dei progressi con grafici interattivi
- Sistema di obiettivi personalizzabili
- Achievement gamificati

## 📊 Struttura del Progetto

```
fitness-tracker/
├── 📱 App.js                                    # Entry point con Navigation
├── ⚙️ app.json                                  # Configurazione Expo
├── 📦 package.json                              # Dipendenze
├── 🔧 .babelrc                                  # Configurazione Babel
├── 🚫 .gitignore                                # File ignorati da Git
├── 📖 README.md                                 # Documentazione (Italiano)
│
└── 📂 src/
    │
    ├── 🎨 components/                            # Componenti UI Riutilizzabili
    │   ├── StepCounter.jsx                     # Contapassi circolare animato
    │   ├── WorkoutCard.jsx                     # Card per visualizzare allenamenti
    │   ├── ProgressChart.jsx                   # Grafici (bar, line, pie)
    │   ├── GoalCard.jsx                        # Card obiettivo con progress bar
    │   └── AchievementBadge.jsx                 # Badge achievement
    │
    ├── 📱 screens/                               # Schermate Principali
    │   ├── DashboardScreen.jsx                 # Dashboard con statistiche
    │   ├── WorkoutsScreen.jsx                  # Gestione allenamenti
    │   ├── ProgressScreen.jsx                  # Grafici e analisi
    │   ├── GoalsScreen.jsx                     # Gestione obiettivi
    │   └── SettingsScreen.jsx                  # Impostazioni
    │
    ├── 🔧 services/                             # Logica di Business
    │   ├── sensorService.js                    # Gestione pedometro
    │   └── workoutService.js                   # CRUD allenamenti
    │
    ├── 🪝 hooks/                                 # Custom React Hooks
    │   ├── useSteps.js                         # Gestione stato passi
    │   ├── useWorkouts.js                      # Gestione stato allenamenti
    │   └── useGoals.js                         # Gestione stato obiettivi
    │
    ├── 🛠️ utils/                                 # Utility Functions
    │   ├── constants.js                        # Costanti app (colori, labels)
    │   └── calculations.js                     # Calcoli fitness (MET, calories)
    │
    └── 🎨 styles/                                # Stili Globali
        └── theme.js                            # Tema e palette colori
```

## 🏗️ Architettura

### Pattern Architetturale
- **Presentational Components**: Componenti UI puri in `components/`
- **Container Components**: Schermate con logica in `screens/`
- **Custom Hooks**: Logica riutilizzabile in `hooks/`
- **Service Layer**: Business logic e data access in `services/`

### State Management
- **React Hooks**: useState, useEffect per stato locale
- **Custom Hooks**: useSteps, useWorkouts, useGoals per logica condivisa
- **AsyncStorage**: Persistenza locale dei dati

### Navigazione
- **React Navigation (Bottom Tabs)**: 4 tab principali + settings
- Tab 1: Dashboard (📊)
- Tab 2: Allenamenti (💪)
- Tab 3: Progressi (📈)
- Tab 4: Obiettivi (🎯)
- Settings: Accessibile da Dashboard (⚙️)

## 📦 Dipendenze Principali

### Core
- `expo ~50.0.0` - Framework principale
- `react-native 0.73.0` - Core React Native
- `expo-sensors ~12.9.0` - Accesso ai sensori (pedometro)

### Navigazione
- `@react-navigation/native ^6.1.9` - Navigazione principale
- `@react-navigation/bottom-tabs ^6.5.11` - Tab navigation

### UI & Grafici
- `victory-native ^36.9.0` - Libreria grafici
- `react-native-svg 14.1.0` - Supporto SVG

### Storage & Data
- `@react-native-async-storage/async-storage 1.21.0` - Persistenza locale
- `date-fns ^3.0.0` - Manipolazione date

### Animazioni
- `react-native-reanimated ~3.6.0` - Animazioni avanzate
- `react-native-gesture-handler ~2.14.0` - Gestione gesture

## 🎯 Funzionalità Principali

### 1. Dashboard (Schermata Principale)
- **Contapassi Circolare**: Visualizzazione animata dei passi con progress circle
- **Statistiche Live**: Calorie, distanza, minuti attivi calcolati dai passi
- **Obiettivi Giornalieri**: 4 goal card con progress bars animate
- **Allenamenti del Giorno**: Lista allenamenti odt
- **Achievement Recenti**: Ultimi 5 badge sbloccati
- **Streak Indicator**: Giorni consecutivi di allenamento
- **FAB**: Floating Action Button per aggiunta rapida

### 2. Allenamenti
- **Lista Completa**: Tutti gli allenamenti ordinati per data
- **Aggiunta Rapida**: Modal con form per nuovo allenamento
- **7 Tipi Supportati**: Corsa, Ciclismo, Camminata, Palestra, Nuoto, Yoga, Altro
- **Calcolo Automatico**: Calorie basate su MET values
- **Dettagli**: Durata, distanza, note
- **Eliminazione**: Con conferma di sicurezza

### 3. Progressi
- **Statistiche Settimanali**: 5 card con riepilogo
- **Grafico a Barre**: Passi giornalieri della settimana
- **Grafico a Linee**: Calorie giornaliere
- **Grafico a Torta**: Distribuzione tipi allenamento
- **Lista Allenamenti**: Ultimi 5 della settimana
- **Time Range Selector**: Switch settimana/mese (UI ready)

### 4. Obiettivi
- **Obiettivi Giornalieri**: Passi, calorie, distanza, durata
- **Obiettivi Settimanali**: Stessi metriche su base settimanale
- **Modifica Interattiva**: Tap per modificare i valori
- **Grid Achievement**: 6 badge sbloccabili
- **Info Streak**: Visualizzazione serie attuale

### 5. Impostazioni
- **Profilo**: Gestione dati personali
- **Reset Dati**: Eliminazione completa dati
- **Info App**: Versione e librerie
- **Guida**: Istruzioni uso app
- **Privacy**: Policy gestione dati

## 🔬 Funzionalità Tecniche

### Sensor Integration
```javascript
// Pedometer con fallback
const isPedometerAvailable = async () => {
  const result = await Pedometer.isAvailableAsync();
  return result;
};

// Subscription per update real-time
await Pedometer.watchStepCountAsync((result) => {
  updateSteps(result.steps);
});
```

### Calorie Calculation
```javascript
// Formula MET
calories = MET × peso(kg) × durata(ore)

// Esempi:
// Corsa (9.8 MET): 9.8 × 70kg × 0.5h = 343 kcal
// Camminata (3.5 MET): 3.5 × 70kg × 0.5h = 122 kcal
```

### Data Persistence
```javascript
// AsyncStorage keys
WORKOUTS: '@fitness_workouts'
GOALS: '@fitness_goals'
STEPS: '@fitness_steps'
ACHIEVEMENTS: '@fitness_achievements'
STATS: '@fitness_stats'
```

### Animazioni
```javascript
// Pulse animation per step counter
Animated.sequence([
  Animated.timing(pulseAnimation, { toValue: 1.1, duration: 100 }),
  Animated.timing(pulseAnimation, { toValue: 1, duration: 100 })
]).start();

// Progress bar fill animation
Animated.timing(animatedValue, {
  toValue: progress,
  duration: 1000
}).start();
```

## 🎨 Design System

### Color Palette
- **Primary**: `#00D4AA` (Verde turchese) - CTAs, elements attivi
- **Secondary**: `#6C5CE7` (Viola) - Grafici, accents
- **Accent**: `#FF6B6B` (Corallo) - Highlights
- **Success**: `#00B894` (Verde) - Completamenti
- **Warning**: `#FDCB6E` (Giallo) - Warnings
- **Danger**: `#FF7675` (Rosso) - Delete, errors
- **Surface**: `#FFFFFF` (Bianco) - Card, background
- **Background**: `#F8F9FA` (Grigio chiaro) - Main bg

### Typography
- **Display**: 32px - Titoli hero
- **H1**: 24px - Titoli schermata
- **H2**: 20px - Sezioni
- **H3**: 16px - Card titles
- **Body**: 14px - Testo normale
- **Caption**: 12px - Secondario
- **Small**: 10px - Micro text

### Spacing Scale
- xs: 4px, sm: 8px, md: 16px, lg: 24px, xl: 32px, xxl: 48px

### Border Radius
- sm: 8px, md: 12px, lg: 16px, xl: 24px, round: 999px

### Shadows
- **sm**: elevation 1 - Cards
- **md**: elevation 2 - Elevated elements
- **lg**: elevation 4 - FAB, modals

## 📊 Data Models

### Workout
```javascript
{
  id: "workout_1234567890",
  type: "running",
  duration: 30,              // minuti
  calories: 343,             // kcal calcolate
  distance: 5.2,             // km (opzionale)
  date: 1708780800000,       // timestamp
  notes: "Ottima corsa!"     // opzionale
}
```

### Goal
```javascript
{
  daily: {
    steps: 10000,
    calories: 500,
    distance: 5,
    duration: 30
  },
  weekly: {
    steps: 70000,
    calories: 3500,
    distance: 35,
    duration: 210
  }
}
```

### Achievement
```javascript
{
  id: "first_workout",
  title: "Primo Passo",
  description: "Completa il primo allenamento",
  icon: "🎯",
  requirement: 1
}
```

### Daily Stats
```javascript
{
  date: "2026-02-12",
  steps: 8542,
  calories: 450,
  distance: 6.2,
  activeMinutes: 45
}
```

## 🚀 Come Avviare il Progetto

### 1. Installazione
```bash
cd fitness-tracker
npm install
```

### 2. Avvio Development
```bash
npm start
```

### 3. Esecuzione
- **Android**: Premi `a` (richiede Android Studio/emulator)
- **iOS**: Premi `i` (richiede Xcode, solo Mac)
- **Expo Go**: Scannerizza QR code con app mobile
- **Web**: Premi `w` (funzionalità limitata per sensori)

### 4. Build Production
```bash
# Android
expo build:android

# iOS
expo build:ios
```

## ⚠️ Note Importanti

### Limitazioni Sensori
- Il pedometro richiede dispositivo fisico
- Emulatori non supportano sensori (fallback a manuale)
- iOS richiede permesso Motion & Fitness
- Android richiede permesso ACTIVITY_RECOGNITION

### Background Limitations
- Background tracking limitato da iOS/Android
- App deve essere in primo piano per update real-time
- Considera background task per produzione

### Performance
- Victory Native può essere lento con molti dati
- Ottimizza dataset per grafici complessi
- Considera lazy loading per liste lunghe

## 🔮 Potenziali Miglioramenti

### Backend Integration
- Sincronizzazione cloud (Firebase, AWS)
- Autenticazione utenti
- Backup e restore dati

### Health Integration
- Google Fit integration
- Apple Health integration
- Samsung Health integration

### Features Avanzate
- GPS tracking per corsa/ciclismo
- Route mapping
- Heart rate monitoring
- Social features (leaderboards)
- Challenges e competitions
- Nutrition tracking
- Sleep tracking

### Technical Improvements
- Redux per state management complesso
- React Query per data fetching
- Unit testing (Jest)
- E2E testing (Detox)
- CI/CD pipeline
- Codepush per OTA updates

## 📱 Schermate dell'App

### 1. Dashboard
```
┌─────────────────────────────────┐
│  👋 Lunedì                      │
│  Dashboard           ⚙️         │
├─────────────────────────────────┤
│  ◯ Contapassi Circolare         │
│     8,542 Passi                 │
│     85%                         │
│                                 │
│  🔥342 📍6.2km ⏱️85min         │
├─────────────────────────────────┤
│  Obiettivi Giornalieri          │
│  ┌───────────────────┐          │
│  │ 🔥 Calorie  68%  │          │
│  │ 📍 Distanza 124% │          │
│  │ ⏱️  Durata  283% │          │
│  └───────────────────┘          │
├─────────────────────────────────┤
│  Allenamenti di Oggi    (2)     │
│  🏃 Corsa 5.2km                │
│  🏋️ Palestra 45min              │
├─────────────────────────────────┤
│  Achievement Recenti            │
│  [🎯] [🔥] [🏅]                │
│                                 │
│  🔥 5 giorni consecutivi        │
│                                 │
│                        [+ FAB]  │
└─────────────────────────────────┘
```

### 2. Allenamenti
```
┌─────────────────────────────────┐
│  Allenamenti          15 totali │
├─────────────────────────────────┤
│  🏃 Corsa          Ieri         │
│     ⏱️ 30min  📍5.2km          │
│              🔥 342 kcal        │
├─────────────────────────────────┤
│  🚴 Ciclismo       Sabato       │
│     ⏱️ 45min  📍15.8km         │
│              🔥 450 kcal        │
├─────────────────────────────────┤
│  🏋️ Palestra        Venerdì    │
│     ⏱️ 60min                   │
│              🔥 280 kcal        │
│                        [+ FAB]  │
└─────────────────────────────────┘
```

### 3. Progressi
```
┌─────────────────────────────────┐
│  Progressi    [Settimana] [Mese] │
├─────────────────────────────────┤
│  Riepilogo Settimanale          │
│  ┌────┐┌────┐┌────┐┌────┐┌────┐│
│  │💪  ││👟  ││🔥  ││📍  ││⏱️ ││
│  │ 5  ││45K ││2.1K││32km││240 ││
│  └────┘└────┘└────┘└────┘└────┘│
├─────────────────────────────────┤
│  Passi Giornalieri              │
│  [Bar Chart]                    │
├─────────────────────────────────┤
│  Calorie Giornaliere            │
│  [Line Chart]                   │
├─────────────────────────────────┤
│  Distribuzione Allenamenti      │
│  [Pie Chart]                    │
└─────────────────────────────────┘
```

### 4. Obiettivi
```
┌─────────────────────────────────┐
│  Obiettivi                      │
├─────────────────────────────────┤
│  Obiettivi Giornalieri   Oggi   │
│  ┌───────────────────┐          │
│  │ 👟 Passi  85%     │          │
│  │ 8,542 / 10,000   │          │
│  └───────────────────┘          │
│  ┌───────────────────┐          │
│  │ 🔥 Calorie  68%   │          │
│  │ 342 / 500         │          │
│  └───────────────────┘          │
├─────────────────────────────────┤
│  Obiettivi Settimanali  Sett    │
│  [Goal cards...]                │
├─────────────────────────────────┤
│  Achievement              2/6    │
│  [🎯] [🔥] [🏅] [💯]            │
│  [👟] [⚡]                        │
│                                 │
│  🔥 5 giorni consecutivi        │
└─────────────────────────────────┘
```

## 📚 Riferimenti

- [Expo Documentation](https://docs.expo.dev/)
- [React Native Docs](https://reactnative.dev/)
- [React Navigation](https://reactnavigation.org/)
- [Victory Native](https://formidable.com/open-source/victory/docs/native/)
- [date-fns](https://date-fns.org/)

## 👨‍💻 Note per lo Sviluppatore

Questo progetto è stato creato come portfolio project dimostrativo. Include:
- ✅ React Native best practices
- ✅ Expo SDK integration
- ✅ Custom hooks pattern
- ✅ Service layer architecture
- ✅ AsyncStorage persistence
- ✅ Sensor integration
- ✅ Animated UI components
- ✅ Charts and data visualization
- ✅ Italian localization
- ✅ Comprehensive documentation

Per domande o suggerimenti, contatta lo sviluppatore.

---

**Creato con ❤️ usando React Native + Expo**

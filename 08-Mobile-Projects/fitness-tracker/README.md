# 🏃 Fitness Tracker App

Un'applicazione React Native completa per il tracciamento delle attività fitness, sviluppata con Expo.

## 📋 Caratteristiche

### Funzionalità Principali

- **📊 Dashboard Intuitiva**
  - Contapassi circolare animato con progresso in tempo reale
  - Statistiche giornaliere (passi, calorie, distanza, minuti attivi)
  - Obiettivi giornalieri con indicatori di progresso
  - Allenamenti del giorno corrente
  - Achievement recenti
  - Serie di allenamenti consecutivi (streak)

- **💪 Gestione Allenamenti**
  - Aggiunta rapida di nuovi allenamenti
  - 7 tipi di allenamenti supportati (Corsa, Ciclismo, Camminata, Palestra, Nuoto, Yoga, Altro)
  - Calcolo automatico delle calorie bruciate
  - Tracciamento di durata, distanza e note
  - Visualizzazione cronologica degli allenamenti
  - Eliminazione degli allenamenti

- **📈 Analisi dei Progressi**
  - Grafici settimanali dei passi
  - Grafici delle calorie giornaliere
  - Distribuzione dei tipi di allenamento
  - Statistiche settimanali dettagliate
  - Riepilogo degli allenamenti recenti

- **🎯 Gestione Obiettivi**
  - Obiettivi giornalieri personalizzabili (passi, calorie, distanza, durata)
  - Obiettivi settimanali
  - Indicatori visivi di progresso
  - Modifica interattiva degli obiettivi

- **🏆 Sistema Achievement**
  - 6 achievement sbloccabili
  - Badge visivi per i traguardi raggiunti
  - Sistema di serie (streak) per incentivare la costanza

### Sensor Integration

- Utilizzo di **Expo Sensors (Pedometer)** per il conteggio automatico dei passi
- Fallback a inserimento manuale se il sensore non è disponibile
- Aggiornamento in tempo reale dei passi

### Persistenza Dati

- Utilizzo di **AsyncStorage** per salvare:
  - Allenamenti
  - Obiettivi
  - Passi giornalieri
  - Achievement sbloccati
  - Statistiche giornaliere

## 🛠️ Stack Tecnologico

- **React Native** con **Expo SDK 50**
- **Expo Sensors** per il pedometro
- **Victory Native** per i grafici
- **React Navigation** per la navigazione a tab
- **AsyncStorage** per la persistenza locale
- **date-fns** per la gestione delle date
- **Animated API** per animazioni fluide

## 📁 Struttura del Progetto

```
fitness-tracker/
├── App.js                          # Entry point dell'applicazione
├── app.json                        # Configurazione Expo
├── package.json                    # Dipendenze
└── src/
    ├── components/                  # Componenti riutilizzabili
    │   ├── StepCounter.jsx         # Contapassi circolare animato
    │   ├── WorkoutCard.jsx         # Card allenamento
    │   ├── ProgressChart.jsx       # Grafici (bar, line, pie)
    │   ├── GoalCard.jsx            # Card obiettivo con progresso
    │   └── AchievementBadge.jsx    # Badge achievement
    ├── screens/                     # Schermate principali
    │   ├── DashboardScreen.jsx     # Dashboard principale
    │   ├── WorkoutsScreen.jsx      # Gestione allenamenti
    │   ├── ProgressScreen.jsx      # Analisi progressi
    │   └── GoalsScreen.jsx         # Gestione obiettivi
    ├── services/                    # Logica di business
    │   ├── sensorService.js        # Gestione sensori (pedometro)
    │   └── workoutService.js       # Gestione dati allenamenti
    ├── hooks/                       # Custom React hooks
    │   ├── useSteps.js             # Hook per gestione passi
    │   ├── useWorkouts.js          # Hook per gestione allenamenti
    │   └── useGoals.js             # Hook per gestione obiettivi
    ├── utils/                       # Utility functions
    │   ├── constants.js            # Costanti e configurazioni
    │   └── calculations.js        # Calcoli fitness (calorie, distanza, etc.)
    └── styles/
        └── theme.js                # Tema e stili globali
```

## 🚀 Installazione e Avvio

### Prerequisiti

- Node.js (versione 16 o superiore)
- npm o yarn
- Expo CLI: `npm install -g expo-cli`
- Expo Go app sul dispositivo mobile (opzionale)

### Passi di Installazione

1. **Naviga nella cartella del progetto:**
   ```bash
   cd fitness-tracker
   ```

2. **Installa le dipendenze:**
   ```bash
   npm install
   ```

3. **Avvia l'applicazione:**
   ```bash
   npm start
   ```

4. **Scegli come eseguire l'app:**
   - Scannerizza il QR code con l'app Expo Go (Android/iOS)
   - Premi `a` per avviare su Android emulator
   - Premi `i` per avviare su iOS simulator (solo Mac)
   - Premi `w` per aprire nel browser

## 📱 Funzionalità Dettagliate

### Tipi di Allenamento

L'app supporta i seguenti tipi di allenamento:

- 🏃 **Corsa** - 9.8 MET
- 🚴 **Ciclismo** - 7.5 MET
- 🚶 **Camminata** - 3.5 MET
- 🏋️ **Palestra** - 5.0 MET
- 🏊 **Nuoto** - 8.0 MET
- 🧘 **Yoga** - 2.5 MET
- 💪 **Altro** - 4.0 MET

### Calcolo Calorie

Le calorie vengono calcolate usando la formula MET:

```
Calorie = MET × Peso (kg) × Durata (ore)
```

### Achievement

L'app include 6 achievement sbloccabili:

1. 🎯 **Primo Passo** - Completa il primo allenamento
2. 🔥 **Settimana Intensa** - Allena tutti i giorni per una settimana
3. 🏅 **Maratoneta** - Corri 42km in totale
4. 💯 **Centenario** - Completa 100 allenamenti
5. 👟 **Camminatore** - Raggiungi 10.000 passi in un giorno
6. ⚡ **Bruciagrassi** - Brucia 500 calorie in un giorno

### Strutture Dati

#### Workout
```javascript
{
  id: string,                    // ID univoco
  type: 'running' | 'cycling' | 'walking' | 'gym' | 'swimming' | 'yoga' | 'other',
  duration: number,              // Durata in minuti
  calories: number,              // Calorie bruciate
  distance: number,              // Distanza in km (opzionale)
  date: timestamp,               // Data allenamento
  notes: string                  // Note (opzionale)
}
```

#### Goal
```javascript
{
  steps: number,                 // Obiettivo passi
  calories: number,              // Obiettivo calorie
  distance: number,              // Obiettivo distanza (km)
  duration: number               // Obiettivo durata (minuti)
}
```

#### Daily Stats
```javascript
{
  date: string,                  // Data (YYYY-MM-DD)
  steps: number,                 // Passi totali
  calories: number,              // Calorie totali
  distance: number,              // Distanza totale (km)
  activeMinutes: number          // Minuti attivi
}
```

## 🎨 Tema e Design

L'app utilizza un tema moderno con colori vibranti:

- **Primario**: #00D4AA (Verde turchese)
- **Secondario**: #6C5CE7 (Viola)
- **Accent**: #FF6B6B (Corallo)
- **Success**: #00B894 (Verde)
- **Warning**: #FDCB6E (Giallo)
- **Danger**: #FF7675 (Rosso)

## 📊 Schermate

### 1. Dashboard
- Contapassi circolare con animazione
- Obiettivi giornalieri con progress bars
- Allenamenti del giorno
- Achievement recenti
- Indicatore di streak

### 2. Allenamenti
- Lista completa degli allenamenti
- Aggiunta rapida con modale
- Dettagli calorie stimate
- Eliminazione con conferma

### 3. Progressi
- Statistiche settimanali
- Grafico a barre (passi giornalieri)
- Grafico a linee (calorie giornaliere)
- Grafico a torta (distribuzione allenamenti)
- Riepilogo allenamenti recenti

### 4. Obiettivi
- Obiettivi giornalieri e settimanali
- Modifica interattiva
- Grid achievement
- Info sulla streak attuale

## 🔧 Personalizzazione

### Modificare i Colori

Modifica il file `src/utils/constants.js` per personalizzare i colori:

```javascript
export const COLORS = {
  primary: '#00D4AA',
  secondary: '#6C5CE7',
  // ... altri colori
};
```

### Modificare gli Obiettivi Predefiniti

Modifica `DEFAULT_GOALS` in `src/utils/constants.js`:

```javascript
export const DEFAULT_GOALS = {
  daily: {
    steps: 10000,
    calories: 500,
    distance: 5,
    duration: 30
  },
  // ...
};
```

### Aggiungere Nuovi Achievement

Aggiungi nuovi achievement in `src/utils/constants.js`:

```javascript
export const ACHIEVEMENTS = {
  NEW_ACHIEVEMENT: {
    id: 'new_achievement',
    title: 'Titolo',
    description: 'Descrizione',
    icon: '🏆',
    requirement: 100
  }
};
```

## 📱 Note Tecniche

### Permessi

L'app richiede i seguenti permessi:
- **MOTION/ACTIVITY_RECOGNITION** per il pedometro (Android/iOS)

### Limitazioni

- Il pedometro richiede un dispositivo fisico con sensore di movimento
- L'emulatore potrebbe non supportare il sensore (fallback a inserimento manuale)
- Background tracking limitato dalle politiche iOS/Android

## 🤝 Contributi

Questo è un progetto dimostrativo. Sentiti libero di forkare e migliorare!

## 📄 Licenza

MIT License - Sentiti libero di utilizzare questo progetto per scopi educativi o commerciali.

## 👨‍💻 Sviluppatore

Progetto realizzato come dimostrazione delle capacità di sviluppo React Native con Expo.

---

**Nota**: Questa è un'app dimostrativa. Per un'applicazione production-ready, considera:
- Backend per la sincronizzazione dei dati
- Autenticazione utente
- Backup cloud
- Notifiche push
- Integrazione con Google Fit / Apple Health
- Ottimizzazioni performance
- Test automatizzati

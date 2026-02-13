# 🚀 Guida Rapida - Fitness Tracker

## Primi Passi (5 minuti)

### 1️⃣ Installazione
```bash
cd fitness-tracker
npm install
```

### 2️⃣ Avvio
```bash
npm start
```

### 3️⃣ Esecuzione
- Installa **Expo Go** sul tuo smartphone
- Scannerizza il QR code che appare
- Oppure premi `a` per Android emulator o `i` per iOS simulator

## 📱 Tour Guidato dell'App

### 🏠 Dashboard
1. **Contapassi**: Visualizza i passi in tempo reale (richiede sensore)
2. **Statistiche**: Calorie, distanza, minuti attivi
3. **Obiettivi**: Vedi i tuoi 4 goal giornalieri
4. **Allenamenti**: Lista allenamenti del giorno
5. **Achievement**: Badge sbloccati
6. **FAB (+)**: Aggiungi nuovo allenamento

### 💪 Allenamenti
- Vedi tutti i tuoi allenamenti
- Tocca il **+** per aggiungerne uno
- Seleziona il tipo (Corsa, Ciclismo, ecc.)
- Inserisci durata e distanza opzionale
- Le calorie sono calcolate automaticamente!

### 📈 Progressi
- Vedi le statistiche settimanali
- Grafico a barre: passi giornalieri
- Grafico a linee: calorie giornaliere
- Grafico a torta: distribuzione tipi allenamento

### 🎯 Obiettivi
- **Obiettivi Giornalieri**: Passi, calorie, distanza, durata
- **Obiettivi Settimanali**: Stessi metriche su base settimanale
- **Modifica**: Tocca una card per modificare l'obiettivo
- **Achievement**: Vedi tutti i 6 achievement da sbloccare

### ⚙️ Impostazioni
- **Reset Dati**: Elimina tutti i dati
- **Guida**: Istruzioni per l'uso
- **Privacy**: Come vengono gestiti i dati

## 🎯 Achievement da Sbloccare

| Icon | Nome | Requisito |
|-----|------|-----------|
| 🎯 | Primo Passo | Completa il primo allenamento |
| 🔥 | Settimana Intensa | Allena tutti i giorni per una settimana |
| 🏅 | Maratoneta | Corri 42km in totale |
| 💯 | Centenario | Completa 100 allenamenti |
| 👟 | Camminatore | Raggiungi 10.000 passi in un giorno |
| ⚡ | Bruciagrassi | Brucia 500 calorie in un giorno |

## 💡 Consigli per l'Uso

### Massimizza il Tracciamento Passi
1. **Porta il telefono con te** durante il giorno
2. **Attiva il pedometro** all'apertura dell'app
3. **Allow permissions** quando richiesto (Motion/Fitness)

### Inserimento Allenamenti
1. **Sii specifico** con il tipo di allenamento
2. **Aggiungi note** per ricordare i dettagli
3. **Inserisci la distanza** per corsa/ciclismo per statistiche accurate

### Obiettivi Realistici
- **Principianti**: 5,000 passi, 300 kcal
- **Intermedi**: 10,000 passi, 500 kcal
- **Avanzati**: 15,000 passi, 800 kcal

## 🔧 Troubleshooting

### "Pedometro non disponibile"
- Su **emulator**: Normale, usa l'inserimento manuale
- Su **device**: Controlla i permessi nelle impostazioni

### "L'app si chiude"
- Prova a riavviare l'app
- Controlla che npm install sia completato
- Verifica la compatibilità del dispositivo

### "I passi non si aggiornano"
- Assicurati di avere i permessi del sensore
- Chiudi e riapri l'app
- Su alcuni dispositivi, il tracking è limitato in background

## 📊 Tipi di Allenamento

| Tipo | Icon | MET | Calorie (30min, 70kg) |
|------|------|-----|---------------------|
| Corsa | 🏃 | 9.8 | 343 kcal |
| Ciclismo | 🚴 | 7.5 | 263 kcal |
| Camminata | 🚶 | 3.5 | 123 kcal |
| Palestra | 🏋️ | 5.0 | 175 kcal |
| Nuoto | 🏊 | 8.0 | 280 kcal |
| Yoga | 🧘 | 2.5 | 88 kcal |

## 🎨 Personalizzazione

### Modificare i Colori
Edita `src/utils/constants.js`:
```javascript
export const COLORS = {
  primary: '#00D4AA',    // Tuo colore preferito
  secondary: '#6C5CE7',
  // ...
};
```

### Modificare gli Obiettivi Predefiniti
Edita `src/utils/constants.js`:
```javascript
export const DEFAULT_GOALS = {
  daily: {
    steps: 10000,        // Modifica questo
    calories: 500,
    distance: 5,
    duration: 30
  },
  // ...
};
```

## 📈 Progresso Tipico

### Settimana 1-2
- 🎯 Sblocca "Primo Passo"
- 📊 Registra 3-5 allenamenti
- 👟 Raggiungi 5,000-8,000 passi/giorno

### Settimana 3-4
- 🔥 Inizia la streak (allenamenti consecutivi)
- ⚡ Raggiungi 500 kcal in un giorno
- 👟 Arriva a 10,000 passi

### Mese 2-3
- 🔥 Completa "Settimana Intensa" (7 giorni consecutivi)
- 💯 Arriva a 20+ allenamenti totali
- 🏅 Inizia ad accumulare km di corsa

### Mese 6+
- 🏅 Sblocca "Maratoneta" (42km corsi)
- 💯 Raggiungi "Centenario" (100 allenamenti)
- 👟 Supera regolarmente i 10,000 passi

## 🎁 Bonus Features

### Features "Nascoste"
- **Pulse animation**: Il contapassi pulsa quando ricevi nuovi step
- **Confetti effect**: Sblocco achievement (da implementare)
- **Dark mode**: Sistema automatico (da implementare)
- **Export dati**: Condividi i tuoi progressi (da implementare)

### Keyboard Shortcuts (Development)
- `r`: Reload app
- `d`: Open DevTools
- `j`: Open debugger
- `Ctrl+C`: Stop server

## 📞 Supporto

- **Documentazione**: Vedi `README.md`
- **Panoramica**: Vedi `PROJECT_OVERVIEW.md`
- **Codice**: Commentato in Italiano
- **Issues**: Contatta lo sviluppatore

---

**Buon allenamento! 💪🏃‍♂️**

# 🍅 Pomodoro Timer

Un'applicazione web completa per la tecnica Pomodoro, sviluppata con **JavaScript ES6+**, **HTML5** e **CSS3**. Perfetta per studenti universitari che vogliono imparare le moderne tecnologie web.

![JavaScript Version](https://img.shields.io/badge/JavaScript-ES6+-brightgreen)
![Difficulty](https://img.shields.io/badge/Livello-Principiante-blue)
![Education](https://img.shields.io/badge/Educativo-University-orange)

## 📚 Sommario

- [Caratteristiche](#-caratteristiche)
- [Tecnologie Utilizzate](#-tecnologie-utilizzate)
- [Funzionalità JavaScript ES6+](#-funzionalità-javascript-es6)
- [Installazione](#-installazione)
- [Struttura del Progetto](#-struttura-del-progetto)
- [Concetti Chiave](#-concetti-chiave)
- [Personalizzazione](#-personalizzazione)
- [Risorse per lo Studio](#-risorse-per-lo-studio)

## ✨ Caratteristiche

### Funzionalità Principali
- ⏱️ **Timer Countdown**: 25 minuti di lavoro, 5 minuti di pausa
- 🔄 **Modalità Switch**: Cambia tra lavoro e pausa facilmente
- 🔊 **Notifiche Audio**: Suoni generati con Web Audio API
- 📊 **Session Tracking**: Traccia le sessioni completate giornaliere
- 📈 **Statistiche Complete**: Visualizza sessioni totali, minuti lavorati, record giornaliero
- 💾 **LocalStorage**: Salva automaticamente i dati nel browser
- 📝 **Cronologia Sessioni**: Log dettagliato delle sessioni completate

### Interfaccia Utente
- 🎨 Design moderno e responsive
- 🌙 Tema scuro per ridurre l'affaticamento visivo
- 📱 Completamente responsive (mobile-friendly)
- ⚡ Animazioni fluide per un'esperienza piacevole
- ♿ Accessibile con buon contrasto e dimensioni leggibili

## 🛠️ Tecnologie Utilizzate

### Frontend Core
- **HTML5**: Semantica e struttura
- **CSS3**: Flexbox, Grid, Animations, Custom Properties
- **JavaScript ES6+**: Sintassi moderna e funzionalità avanzate

### API Browser
- **LocalStorage API**: Persistenza dati
- **Web Audio API**: Generazione suoni
- **Notifications API**: Notifiche desktop
- **DOM API**: Manipolazione del documento

## 🔥 Funzionalità JavaScript ES6+

Questo progetto è stato progettato come risorsa educativa per imparare JavaScript moderno. Ecco le feature ES6+ utilizzate:

### 1. Classi ES6 (2015)
```javascript
class PomodoroTimer {
    constructor(workTime = 25) {
        this.workTime = workTime;
    }

    start() {
        // Metodi senza parola chiave 'function'
    }
}
```
**Vantaggio**: Sintassi più pulita per programmazione orientata agli oggetti

### 2. Arrow Functions (2015)
```javascript
// Sintassi concisa
startBtn.addEventListener('click', () => this.start());

// Mantiene automaticamente il contesto 'this'
setInterval(() => {
    this.tick();
}, 1000);
```
**Vantaggio**: Sintassi compatta e risolve il problema del 'this'

### 3. Template Literals (2015)
```javascript
const timeString = `${minutes}:${seconds}`;
console.log(`🚀 Timer avviato: ${mode}`);
```
**Vantaggio**: Stringhe più leggibili con interpolation

### 4. Destructuring (2015)
```javascript
// DOM grouping
const { timeDisplay, startBtn } = this.dom;
```
**Vantaggio**: Estrazione proprietà più concisa

### 5. Spread Operator (2015)
```javascript
const maxSessions = Math.max(...sessionsArray);
```
**Vantaggio**: Espande array in singoli argomenti

### 6. Array Methods Moderni
```javascript
// forEach
todaySessions.forEach((session, index) => {
    render(session, index);
});

// filter
const recentSessions = sessions.filter(s => s.isRecent);

// find
const button = buttons.find(btn => btn.dataset.mode === 'work');
```
**Vantaggio**: Programmazione funzionale e codice più pulito

### 7. Let & Const (2015)
```javascript
const TIME = 25;          // Non può essere riassegnata
let currentTime = 25;     // Può essere riassegnata
```
**Vantaggio**: Scope a blocchi e codice più sicuro

### 8. JSON Methods
```javascript
// Salvataggio
localStorage.setItem('data', JSON.stringify(object));

// Caricamento
const data = JSON.parse(localStorage.getItem('data'));
```
**Vantaggio**: Serializzazione facile di oggetti complessi

### 9. Web Audio API
```javascript
const audioContext = new AudioContext();
const oscillator = audioContext.createOscillator();
oscillator.start();
```
**Vantaggio**: Genera suoni senza file esterni

### 10. Modern DOM Manipulation
```javascript
// querySelector e querySelectorAll
const elements = document.querySelectorAll('.mode-btn');

// classList API
element.classList.add('active');
element.classList.toggle('hidden');
```
**Vantaggio**: Selettore CSS-like e gestione classi semplificata

## 🚀 Installazione

### Prerequisiti
- Un browser web moderno (Chrome, Firefox, Edge, Safari)
- Nessun server o installazione richiesta!

### Passaggi

1. **Clona o scarica il progetto**
```bash
# Clona il repository
git clone <repository-url>

# Oppure scarica come ZIP ed estrai
```

2. **Apri il file HTML**
```bash
# Metodo 1: Doppio click su index.html
# Metodo 2: Apri con il browser preferito
# Metodo 3: Usa Live Server in VS Code
```

3. **Inizia a usare il timer!**
   - Clicca su "Avvia" per iniziare una sessione di lavoro
   - Il timer ti avviserà quando è il momento di fare una pausa

## 📁 Struttura del Progetto

```
pomodoro-timer/
│
├── index.html          # Struttura HTML della pagina
├── style.css           # Stili e design responsive
├── app.js              # Logica JavaScript ES6+
├── README.md           # Documentazione (questo file)
│
└── assets/             # (Opzionale) Immagini, icone, font
```

### Descrizione File

#### `index.html`
- Struttura semantica HTML5
- Layout con header, main, footer
- Sezioni: timer, controlli, statistiche, log
- Meta tag per viewport e encoding

#### `style.css`
- CSS Variables per tema coerente
- Flexbox e Grid per layout
- Media queries per responsive design
- Animazioni CSS keyframes
- Selettore :root per configurazione

#### `app.js`
- Classe `PomodoroTimer` principale
- Metodi per gestione timer
- Integrazione LocalStorage
- Web Audio API per suoni
- Commenti educativi dettagliati

## 🎓 Concetti Chiave

### Programmazione Orientata agli Oggetti
```javascript
// Creazione istanza
const timer = new PomodoroTimer(25, 5);

// Chiamata metodi
timer.start();
timer.pause();
timer.reset();
```

### Gestione Stato
```javascript
// Stato interno dell'oggetto
this.isRunning = false;
this.timeLeft = 1500;
this.currentMode = 'work';
```

### Event Listeners
```javascript
// Arrow function mantiene contesto
button.addEventListener('click', () => {
    this.start();
});
```

### Persistenza Dati
```javascript
// Salva in localStorage
localStorage.setItem('key', JSON.stringify(data));

// Carica da localStorage
const data = JSON.parse(localStorage.getItem('key'));
```

### Timing
```javascript
// setInterval per esecuzione ripetuta
setInterval(() => {
    this.tick();
}, 1000);

// clearInterval per fermare
clearInterval(this.timerInterval);
```

## 🎨 Personalizzazione

### Cambiare i Tempi del Timer
Modifica il costruttore in `app.js`:
```javascript
// Default: 25 min lavoro, 5 min pausa
constructor(workTime = 25, breakTime = 5) {
    // ...
}

// Oppure all'istanziazione:
const timer = new PomodoroTimer(50, 10); // 50 min lavoro, 10 min pausa
```

### Modificare i Colori
Modifica le CSS Variables in `style.css`:
```css
:root {
    --primary-color: #e74c3c;    /* Cambia colore primario */
    --secondary-color: #27ae60;  /* Cambia colore secondario */
    --background: #1a1a2e;       /* Cambia sfondo */
}
```

### Aggiungere Nuove Statistiche
Aggiungi proprietà e metodi nella classe:
```javascript
class PomodoroTimer {
    constructor() {
        this.streak = 0;  // Nuova proprietà
    }

    updateStreak() {
        // Nuova logica
    }
}
```

## 📖 Risorse per lo Studio

### JavaScript ES6+ Guide
- **MDN Web Docs**: [JavaScript Guide](https://developer.mozilla.org/it/docs/Web/JavaScript)
- **JavaScript.info**: [Moderna JavaScript Tutorial](https://it.javascript.info/)
- **ES6 Features**: [ES6 Features Overview](https://es6-features.org/)

### Video Corsi (Italiano)
- **YouTube**: "JavaScript ES6 per principianti"
- **freeCodeCamp**: Corso JavaScript completo
- **Web Academy**: Tutorial frontend moderni

### Practice Esercizi
1. Aggiungi un timer personalizzato
2. Implementa la modalità "Long Break" (15-30 min)
3. Aggiungi grafici per visualizzare le statistiche
4. Esporta i dati in CSV
5. Aggiungi tema chiaro/scuro
6. Implementa suoni diversi per lavoro/pausa

## 🤝 Contributo

Questo è un progetto educativo. Sentiti libero di:
- 🐛 Segnalare bug
- 💡 Proporre nuove funzionalità
- 📝 Migliorare la documentazione
- 🎨 Migliorare il design
- 🔧 Aggiornare le librerie

## 📝 Licenza

Questo progetto è open source e disponibile per scopi educativi.

## 👨‍🎓 Target di Riferimento

Questo progetto è pensato specificamente per:
- 🎓 Studenti universitari di Informatica
- 🌱 Principianti in JavaScript
- 🔄 Chi vuole migrare da JavaScript vecchia scuola a ES6+
- 📚 Studenti autodidatti
- 👨‍💻 Sviluppatori che vogliono approfondire le moderne API browser

## 🎯 Obiettivi di Apprendimento

Dopo aver studiato questo progetto, saprai:
✅ Creare classi JavaScript moderne
✅ Usare arrow functions e template literals
✅ Manipolare il DOM in modo efficace
✅ Salvare dati con LocalStorage
✅ Generare suoni con Web Audio API
✅ Creare UI responsive con CSS
✅ Gestire eventi e stato dell'applicazione
✅ Strutturare un progetto web completo

## 📞 Supporto

Per domande o chiarimenti:
- Consulta i commenti nel codice
- Riferisci alle risorse MDN
- Sperimenta con il codice!

---

**Creato con ❤️ per la community educativa italiana**

Buono studio e buone sessioni Pomodoro! 🍅📚

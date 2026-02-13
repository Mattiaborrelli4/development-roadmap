# 🍅 Pomodoro Timer

Un'applicazione Pomodoro Timer interattiva sviluppata con puro HTML, CSS e JavaScript che aiuta a gestire il tempo di lavoro e di pausa utilizzando la tecnica Pomodoro.

![Versione](https://img.shields.io/badge/versione-1.0.0-blue)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow)
![CSS](https://img.shields.io/badge/CSS-Variables-green)

## 📋 Indice

- [Caratteristiche](#caratteristiche)
- [Dimostrazione](#dimostrazione)
- [Tecnologie Utilizzate](#tecnologie-utilizzate)
- [Installazione](#installazione)
- [Utilizzo](#utilizzo)
- [Funzionalità](#funzionalità)
- [Struttura del Progetto](#struttura-del-progetto)
- [Personalizzazione](#personalizzazione)
- [Browser Supportati](#browser-supportati)

## ✨ Caratteristiche

- ⏱️ **Timer 25/5**: Cicli di 25 minuti di lavoro e 5 minuti di pausa
- ▶️ **Controlli Completi**: Avvio, pausa e reset del timer
- 🔔 **Notifiche Audio**: Avvisi sonori al termine di ogni sessione
- 📊 **Contatore Sessioni**: Tracciamento dei Pomodori completati
- 🎨 **Dark/Light Mode**: Toggle per cambiare tema chiaro/scuro
- 💾 **LocalStorage**: Salvataggio automatico delle preferenze
- 📱 **Responsive Design**: Adattamento a tutti i dispositivi
- ⌨️ **Scorciatoie Tastiera**: Controllo rapido da tastiera
- ♿ **Accessibile**: Design conforme alle linee guida di accessibilità

## 🎯 Dimostrazione

### Tema Chiaro
Il timer in modalità tema chiaro mostra un'interfaccia pulita con colori vivaci per distinguere le sessioni di lavoro (rosso) dalle pause (verde).

### Tema Scuro
La modalità scura offre un'esperienza visivamente confortevole con colori ad alto contrasto per l'uso in ambienti con poca luce.

## 🛠 Tecnologie Utilizzate

- **HTML5**: struttura semantica
- **CSS3**:
  - CSS Variables per la gestione dei temi
  - Flexbox e Grid per il layout
  - Animazioni e transizioni
  - Media queries per il design responsive
- **JavaScript ES6+**:
  - Arrow functions
  - Template literals
  - Destructuring
  - Classi (ES6 Classes)
  - Const/let
  - SetInterval/SetTimeout
- **Web Audio API**: generazione suoni notifica
- **LocalStorage API**: salvataggio preferenze
- **Notification API**: notifiche desktop

## 📦 Installazione

1. **Clona o scarica il repository**
   ```bash
   git clone https://github.com/tuo-username/pomodoro-timer.git
   cd pomodoro-timer
   ```

2. **Apri il file index.html**
   - Doppio clic su `index.html`, oppure
   - Usa un server locale come Live Server in VS Code

3. **Nessuna dipendenza richiesta!**
   - Tutto funziona out-of-the-box con HTML, CSS e JavaScript puro

## 🚀 Utilizzo

### Controlli Base

1. **Avvia il Timer**
   - Clicca il pulsante "Avvia" o premi `Spazio`
   - Il timer inizierà il conto alla rovescia

2. **Metti in Pausa**
   - Clicca "Pausa" o premi `Spazio` mentre il timer è in esecuzione

3. **Reset**
   - Clicca "Reset" o premi `R` per riportare il timer al tempo iniziale

4. **Cambia Sessione**
   - Clicca "Lavoro" per avviare un sessione di 25 minuti
   - Clicca "Pausa" per avviare una sessione di 5 minuti

5. **Cambia Tema**
   - Clicca l'icona 🌙/☀️ in alto a destra per toggle dark/light mode

### Scorciatoie Tastiera

| Tasto | Azione |
|-------|--------|
| `Spazio` | Avvia/Pausa |
| `R` | Reset |

### Completamento Sessioni

Quando un timer termina:
1. **Suono notifica**: Un suono avvisa la fine della sessione
2. **Notifica Desktop** (se permesso): Appare una notifica di sistema
3. **Switch Automatico**: Dopo 2 secondi, passa automaticamente alla prossima sessione
4. **Contatore Aggiornato**: Il numero di Pomodori completati aumenta

## 🎨 Funzionalità

### 1. Timer Intelligente
- **Sessioni Lavoro**: 25 minuti di focus
- **Sessioni Pausa**: 5 minuti di riposo
- **Barra di Progresso**: Visualizzazione temporale rimanente
- **Animazioni**: Effetto pulse durante l'esecuzione

### 2. Gestione Audio
- **Web Audio API**: Generazione suoni senza file esterni
- **Tono Doppio**: Sequenza di due toni per effetto campana
- **Non Intrusivo**: Volume moderato e durata breve

### 3. Salvataggio Preferenze
```javascript
// Dati salvati in LocalStorage
{
  completedPomodoros: 5,
  currentSession: 6,
  theme: "dark"
}
```

### 4. Temi Dinamici
- **Tema Chiaro**: Colori pastello, sfondo chiaro
- **Tema Scuro**: Colori neon, sfondo scuro
- **Transizioni**: Animazioni fluide tra i temi

### 5. Statistiche
- **Pomodori Completati**: Totale sessioni lavoro completate
- **Sessione Corrente**: Numero progressivo della sessione

## 📁 Struttura del Progetto

```
pomodoro-timer/
│
├── index.html          # Struttura HTML principale
├── style.css           # Foglio di stile con CSS variables
├── app.js              # Logica applicazione (ES6+)
├── README.md           # Documentazione (questo file)
│
└── assets/             # (opzionale) risorse aggiuntive
```

### Dettagli File

#### `index.html`
- Struttura semantica HTML5
- Meta tag per responsive design
- Accessibilità con ARIA labels
- Pulsanti e container principali

#### `style.css`
- **Variabili CSS**: Facile gestione dei temi
- **Layout**: Flexbox e Grid per posizionamento
- **Animazioni**: Pulse, shake, transitions
- **Responsive**: Media queries per mobile
- **Tema**: Dark/Light mode con data-theme attribute

#### `app.js`
- **Configurazione**: Costanti per durata timer
- **Stato**: Object centrale per gestione stato
- **AudioManager**: Classe per Web Audio API
- **Storage**: Gestione LocalStorage
- **Timer**: setInterval per conto alla rovescia
- **Event Listeners**: Gestione interazioni utente

## ⚙️ Personalizzazione

### Modifica Durata Timer

Modifica le costanti in `app.js`:

```javascript
const CONFIG = {
    workDuration: 25 * 60,   // Cambia 25 per minuti lavoro
    breakDuration: 5 * 60,   // Cambia 5 per minuti pausa
    // ...
};
```

### Personalizza Colori

Modifica le variabili CSS in `style.css`:

```css
:root {
    --accent-primary: #e74c3c;  /* Colore principale */
    --accent-secondary: #27ae60; /* Colore secondario */
    /* ... */
}
```

### Cambia Suono Notifica

Modifica il metodo `playNotification()` in `app.js`:

```javascript
oscillator.frequency.value = 800;  // Cambia frequenza
oscillator.type = 'sine';          // Cambia tipo d'onda
```

## 🌐 Browser Supportati

| Browser | Versione Minima |
|---------|----------------|
| Chrome  | 66+ |
| Firefox | 60+ |
| Safari  | 13.1+ |
| Edge    | 79+ |

### Feature Browser Richieste
- ✅ CSS Variables
- ✅ ES6+ JavaScript
- ✅ Web Audio API
- ✅ LocalStorage
- ✅ Notification API (opzionale)

## 📱 Responsive Breakpoints

- **Desktop**: > 600px
- **Mobile**: ≤ 600px
- **Reduced Motion**: Supportato per accessibilità

## 🎓 Concetti Appresi

Questo progetto dimostra la padronanza di:

1. **JavaScript ES6+**
   - Arrow functions: `() => {}`
   - Template literals: `` `${variable}` ``
   - Destructuring: `const { time, isRunning } = state`
   - Classes: `class AudioManager {}`
   - Const/let scope

2. **Manipolazione DOM**
   - `querySelector` / `getElementById`
   - Event listeners
   - Class manipulation
   - Dynamic updates

3. **Gestione Stato**
   - Centralized state object
   - State persistence with LocalStorage
   - Reactivity patterns

4. **CSS Moderno**
   - CSS Custom Properties
   - Flexbox e Grid layout
   - Animations e transitions
   - Dark mode implementation

5. **Web APIs**
   - Web Audio API
   - LocalStorage API
   - Notification API

## 🤝 Contribuire

Contributi benvenuti! Sentiti libero di:

1. Fare fork del progetto
2. Creare un feature branch
3. Commit delle modifiche
4. Push al branch
5. Aprire una Pull Request

## 📝 Licenza

Questo progetto è open source e disponibile sotto la [MIT License](LICENSE).

## 👨‍💻 Autore

Creato con ❤️ usando puro HTML, CSS e JavaScript.

## 🙏 Riconoscimenti

- Tecnica Pomodoro sviluppata da Francesco Cirillo
- Icone dalla libreria Emoji standard
- Design ispirato dalle migliori practice UX/UI

---

**Nota**: Questo progetto fa parte di un portfolio di progetti JavaScript. Per altri progetti, visita il repository principale.

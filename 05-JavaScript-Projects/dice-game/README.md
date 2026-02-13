# 🎲 Gioco dei Dadi

Un gioco interattivo a 2 giocatori con animazioni dei dadi, sistema di punteggio e rilevamento della vittoria. Sviluppato con puro HTML, CSS e JavaScript (ES6+).

![Screenshot](screenshot.png)

## 📋 Caratteristiche

### Funzionalità Principali
- **2 Giocatori**: Turni alternati tra Giocatore 1 e Giocatore 2
- **Animazioni dei Dadi**: Visualizzazione animata del lancio del dado con facce realistiche
- **Sistema di Punteggio**:
  - Punteggio corrente: punti accumulati nel turno corrente
  - Punteggio totale: somma di tutti i turni vinti
- **Condizione di Vittoria**: Il primo giocatore a raggiungere il punteggio obiettivo vince
- **Regola dell'1**: Se esce il numero 1, il giocatore perde il punteggio corrente e passa il turno
- **Pulsanti Strategici**:
  - **Lancia il Dado**: Lancia il dado e accumula punti nel punteggio corrente
  - **Tieni il Punteggio**: Aggiunge il punteggio corrente al totale e passa il turno
  - **Nuova Partita**: Resetta il gioco e inizia una nuova partita
- **Punteggio Obiettivo Configurabile**: Scegli tra 50, 100, 150 o 200 punti per vincere

### Caratteristiche Tecniche
- **JavaScript ES6+**: Classi, arrow functions, template literals, array methods
- **CSS Animations**: Animazioni fluide per il lancio dei dadi e transizioni UI
- **Responsive Design**: Adattamento perfetto per desktop, tablet e mobile
- **Accessibilità**: Supporto per tastiera e focus indicators
- **LocalStorage**: Salvataggio delle statistiche di gioco

## 🚀 Come Giocare

### Regole del Gioco
1. Il **Giocatore 1** inizia la partita
2. Premi **"Lancia il Dado"** per tirare il dado
3. Il numero uscito viene aggiunto al tuo **punteggio corrente**
4. Puoi continuare a lanciare per accumulare più punti
5. Se esce **1**, perdi tutto il punteggio corrente e passa il turno
6. Premi **"Tieni il Punteggio"** per:
   - Aggiungere il punteggio corrente al tuo totale
   - Passare il turno all'avversario
7. Il primo giocatore a raggiungere il **punteggio obiettivo** vince!

### Controlli da Tastiera
- **Spazio**: Lancia il dado
- **Enter**: Tieni il punteggio
- **Ctrl + N**: Nuova partita

## 🛠️ Tecnologie Utilizzate

### HTML5
- Struttura semantica
- Form elements per controlli
- Modal overlay per vincita

### CSS3
- Flexbox per layout
- CSS Grid per il dado
- Keyframe animations
- CSS variables (non usate ma compatibili)
- Media queries per responsive design
- Transitions e transforms

### JavaScript ES6+
- **Classi**: `DiceGame`, `GameStats` per OOP
- **Arrow Functions**: Funzioni concise e gestione contesto
- **Template Literals**: String interpolation
- **Array Methods**: `map()`, `filter()`, `reduce()`
- **Destructuring**: Assegnamento di proprietà
- **Spread/Rest Operator**: Copia di oggetti e array
- **Modules**: Export/Import (compatibile)
- **Event Listeners**: Gestione interazioni utente
- **DOM Manipulation**: QuerySelector, classList, etc.
- **Local Storage API**: Persistenza dati

## 📁 Struttura del Progetto

```
dice-game/
│
├── index.html          # Struttura HTML del gioco
├── style.css           # Stili CSS con animazioni
├── game.js             # Logica del gioco in JavaScript
├── README.md           # Documentazione (questo file)
└── screenshot.png      # Screenshot del gioco (opzionale)
```

## 🎯 Classi e Metodi Principali

### DiceGame
Classe principale che gestisce il gioco.

```javascript
class DiceGame {
    constructor()                    // Inizializza il gioco
    init()                           // Configura event listeners
    initGame()                       // Resetta e inizia nuova partita
    rollDice()                       // Lancia il dado
    animateDice(diceValue)            // Anima il dado
    holdScore()                      // Tieni il punteggio
    nextPlayer()                     // Passa al prossimo giocatore
    checkWin()                       // Controlla condizione di vittoria
    declareWinner()                  // Dichiara il vincitore
}
```

### GameUtils
Utility functions per operazioni comuni.

```javascript
const GameUtils = {
    randomBetween(min, max)          // Numero casuale tra min e max
    formatScore(score)               // Formatta punteggio
    calculateAverage(scores)         // Calcola media
    findHighScore(scores)           // Trova punteggio più alto
    shouldHold(...)                  // Suggerisce se tenere il punteggio
}
```

### GameStats
Gestisce le statistiche di gioco con LocalStorage.

```javascript
class GameStats {
    loadStats()                      // Carica statistiche salvate
    recordGame(winner, finalScore)   // Registra una partita
    getStats()                       // Ottieni statistiche
    getWinPercentages()              // Calcola percentuali di vittoria
    resetStats()                     // Reset statistiche
}
```

## 🎨 Personalizzazione

### Modificare il Punteggio di Vittoria
Modifica l'elemento `<select>` in `index.html`:

```html
<select id="winning-score">
    <option value="50">50</option>
    <option value="100" selected>100</option>
    <option value="150">150</option>
    <option value="200">200</option>
</select>
```

### Modificare i Colori
Cerca i seguenti colori in `style.css`:
- `#667eea` - Viola principale
- `#764ba2` - Viola secondario
- Sostituiscili con i tuoi colori preferiti

### Aggiungere Più Giocatori
1. Modifica l'array `scores` nel costruttore di `DiceGame`
2. Aggiungi HTML per i nuovi giocatori
3. Aggiorna `nextPlayer()` per ciclare tra tutti i giocatori
4. Modifica il CSS per adattarsi al layout

## 🔧 Installazione ed Esecuzione

### Metodo 1: Apertura Diretta
1. Scarica o clona il repository
2. Apri `index.html` nel tuo browser preferito

### Metodo 2: Server Locale (Consigliato)
```bash
# Con Python 3
python -m http.server 8000

# Con Node.js (npx)
npx serve

# Con PHP
php -S localhost:8000
```

Poi visita `http://localhost:8000`

### Metodo 3: Live Server (VS Code)
1. Installa l'estensione "Live Server"
2. Fai click destro su `index.html`
3. Seleziona "Open with Live Server"

## 🌐 Compatibilità Browser

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Opera 76+

## 📚 Concetti di Programmazione Dimostrati

### JavaScript Avanzato
- **Object-Oriented Programming**: Classi e istanze
- **State Management**: Gestione dello stato del gioco
- **Event Handling**: Event listeners e callback
- **DOM Manipulation**: Manipolazione dinamica del DOM
- **LocalStorage API**: Persistenza dati lato client
- **ES6+ Features**: Destructuring, spread operator, arrow functions

### CSS Moderno
- **Flexbox Layout**: Layout flessibili
- **CSS Animations**: @keyframes e transitions
- **Responsive Design**: Media queries
- **CSS Selectors**: Classi, ID, pseudo-classi
- **Transform & Transitions**: Animazioni fluide

### HTML5
- **Semantic HTML**: Struttura corretta
- **Form Elements**: Select, button elements
- **Accessibility**: ARIA attributes (opzionale)
- **Meta Tags**: Viewport per mobile

## 🎮 Sviluppi Futuri

Potenziali miglioramenti:
- [ ] Modalità multiplayer online (WebSocket)
- [ ] Intelligenza artificiale come avversario
- [ ] Classifica globale
- [ ] Temi personalizzabili
- [ ] Effetti sonori
- [ ] Sistema di achievement
- [ ] Statistiche dettagliate
- [ ] Modalità torneo
- [ ] Animazioni 3D per i dadi
- [ ] Supporto per più di 2 giocatori

## 📄 Licenza

Questo progetto è open source e disponibile per scopi educativi.

## 👨‍💻 Autore

Creato come progetto portfolio per dimostrare competenze in:
- JavaScript ES6+
- CSS3 Animations
- HTML5 Semantic Structure
- Game Development Basics
- Responsive Web Design

---

**Buon divertimento! 🎲🎉**

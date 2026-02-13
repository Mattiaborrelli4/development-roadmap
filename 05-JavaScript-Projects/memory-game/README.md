# 🎮 Gioco di Memoria

Un gioco di memoria interattivo sviluppato in JavaScript puro con animazioni CSS 3D, sistema di punteggio e livelli di difficoltà.

![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow)
![HTML](https://img.shields.io/badge/HTML5-Orange)
![CSS](https://img.shields.io/badge/CSS3-Blue)

## 🎯 Caratteristiche

### Funzionalità Principali
- **Animazioni 3D**: Effetto di girata delle carte con CSS transforms
- **Sistema di Punteggio**: Tracciamento delle mosse e del tempo
- **Livelli di Difficoltà**:
  - Facile: Griglia 4x4 (8 coppie di carte)
  - Difficile: Griglia 6x6 (18 coppie di carte)
- **Celebrazione della Vittoria**: Modale con statistiche finali
- **Design Responsivo**: Adattabile a diversi dispositivi

### Aspetti Tecnici
- JavaScript ES6+ (classi, arrow functions, template literals)
- CSS 3D transforms per le animazioni delle carte
- Gestione dello stato del gioco
- Funzioni di timing per il cronometro
- Algoritmo Fisher-Yates per la mescolanza delle carte

## 🚀 Come Giocare

1. **Seleziona la difficoltà**: Scegli tra "Facile" o "Difficile"
2. **Clicca sulle carte**: Girale per scoprire i simboli
3. **Trova le coppie**: Abbina due carte con lo stesso simbolo
4. **Completa il gioco**: Trova tutte le coppie nel minor tempo possibile!

## 📁 Struttura del Progetto

```
memory-game/
│
├── index.html          # Struttura del gioco
├── style.css           # Animazioni e stilizzazione
├── game.js             # Logica del gioco
└── README.md           # Documentazione
```

## 💻 Installazione

1. Clona o scarica il repository
2. Apri `index.html` nel tuo browser
3. Inizia a giocare!

Nessuna dipendenza esterna richiesta - funziona direttamente nel browser.

## 🎨 Dettagli Tecnici

### HTML (`index.html`)
- Struttura semantica con header, controlli e area di gioco
- Elementi per le statistiche (mosse, tempo, coppie)
- Modale per la celebrazione della vittoria

### CSS (`style.css`)
- **Animazioni 3D**: `transform: rotateY()` per l'effetto di girata
- **Transizioni**: `transition: transform 0.6s` per animazioni fluide
- **Layout Grid**: `display: grid` per la disposizione delle carte
- **Design Responsive**: Media queries per dispositivi mobili
- **Gradiente**: Sfondo con gradiente moderno

### JavaScript (`game.js`)

#### Classe `MemoryGame`
La classe principale che gestisce tutto il gioco:

**Metodi Principali:**
- `constructor(boardId)`: Inizializza il gioco
- `startGame()`: Avvia una nuova partita
- `flipCard(card)`: Gestisce il click su una carta
- `checkMatch()`: Verifica se le carte corrispondono
- `handleMatch(card1, card2)`: Gestisce una coppia trovata
- `handleMismatch(card1, card2)`: Gestisce una mancata corrispondenza
- `startTimer()`: Avvia il cronometro
- `handleWin()`: Gestisce la vittoria

**Caratteristiche JavaScript ES6+:**
- **Classi**: `class MemoryGame` per la struttura del gioco
- **Arrow Functions**: `(e) => { ... }` per gli event listeners
- **Template Literals**: `` `${minutes}:${seconds}` `` per formattazione
- **Array Methods**: `forEach()`, `slice()` per manipolazione array
- **Destructuring**: `const [card1, card2] = this.flippedCards`

### Logica di Gioco

1. **Inizializzazione**:
   - Seleziona i simboli in base alla difficoltà
   - Crea coppie di carte duplicate
   - Mischia con l'algoritmo Fisher-Yates

2. **Gameplay**:
   - Click sulla carta → flip animation
   - Due carte girate → verifica corrispondenza
   - Coppia trovata → carte rimangono girate
   - Nessuna coppia → carte rigirate dopo 1 secondo

3. **Vittoria**:
   - Tutte le coppie trovate
   - Timer fermato
   - Modale con statistiche finali

## 🎯 Obiettivi di Apprendimento

Questo progetto dimostra la competenza in:

- ✅ Manipolazione del DOM
- ✅ Gestione degli eventi
- ✅ CSS 3D transforms e animations
- ✅ Programmazione orientata agli oggetti (classi)
- ✅ Gestione dello stato dell'applicazione
- ✅ Logica di gioco e algoritmi
- ✅ Design responsivo
- ✅ JavaScript ES6+ moderno

## 🔧 Personalizzazione

### Aggiungere nuovi simboli
Modifica l'array `symbols` nel file `game.js`:

```javascript
this.symbols = [
    '🍎', '🍊', '🍋', '🍇', // Aggiungi i tuoi simboli
];
```

### Modificare i colori
Cambia le variabili CSS in `style.css`:

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Aggiungere una nuova difficoltà
Modifica il metodo `startGame()` in `game.js`:

```javascript
if (this.difficulty === 'medium') {
    const totalPairs = 12; // Griglia 5x5
}
```

## 📊 Statistiche di Gioco

Il gioco traccia:
- **Mosse**: Numero di tentativi
- **Tempo**: Cronometro in formato MM:SS
- **Coppie**: Progresso delle coppie trovate

## 🎨 Screenshots

Il gioco presenta:
- Design moderno con gradiente viola/blu
- Carte con emoji fruttate
- Animazioni fluide 3D
- Modale di vittoria celebrativo

## 📝 Note

- Il gioco utilizza solo HTML, CSS e JavaScript puro
- Nessuna libreria esterna richiesta
- Compatibile con tutti i browser moderni
- Responsive per mobile e desktop

## 👨‍💻 Sviluppatore

Progetto creato per dimostrare competenze in JavaScript ES6+, CSS 3D transforms e sviluppo di giochi web interattivi.

## 📄 Licenza

Questo progetto è open source e disponibile per scopi educativi.

---

**Buon divertimento! 🎉**

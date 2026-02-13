# 🎯 Quiz App - Applicazione Quiz JavaScript

Un'applicazione di quiz interattiva e moderna costruita con puro HTML, CSS e JavaScript (ES6+). Testa le tue conoscenze su JavaScript, HTML, CSS e Web Development in generale!

![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow)
![HTML](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)

## ✨ Caratteristiche

### 🎮 Gameplay
- **4 Categorie**: JavaScript, HTML, CSS e Web Generale
- **3 Livelli di Difficoltà**: Facile, Medio, Difficile
- **Timer per Domanda**: 15 secondi per risposta
- **Sistema di Punteggio**: Punti base + bonus tempo
- **Domande Multiple Choice**: 4 opzioni per domanda

### 📊 Tracciamento Progressi
- **Conteggio Risposte Corrette/Sbagliate**
- **Percentuale di Successo**
- **Tempo Totale Impiegato**
- **Revisione Completa Risposte**

### 🏆 Classifica e High Scores
- **High Scores Persistente**: Salvataggio con localStorage
- **Filtri per Categoria**: Visualizza punteggi per categoria
- **Top 10 Punteggi**: Mantiene solo i migliori punteggi
- **Data e Dettagli**: Informazioni complete su ogni punteggio
- **Sistema di Medaglie**: Oro, Argento, Bronzo per i primi 3

### 🎨 Design e UX
- **UI Moderna e Responsive**: Funziona su desktop e mobile
- **Animazioni Fluide**: Transizioni e feedback visivo
- **Feedback Immediato**: Colori e icone per risposte corrette/errate
- **Timer Visuale**: Barra di progresso del tempo
- **Design a Tema Scuro**: Comodo per gli occhi

## 🚀 Come Utilizzare

### Avvio Rapido

1. **Apri il file** `index.html` nel tuo browser preferito
2. **Seleziona una categoria** tra JavaScript, HTML, CSS o Generale
3. **Scegli la difficoltà**: Facile, Medio o Difficile
4. **Clicca "Inizia il Quiz"** per iniziare
5. **Rispondi alle domande** entro il tempo limite
6. **Visualizza i risultati** e rivedi le tue risposte
7. **Salva il punteggio** se è un nuovo record!

### Requisiti di Sistema

- Browser moderno con supporto ES6+ (Chrome, Firefox, Safari, Edge)
- JavaScript abilitato
- localStorage supportato (per high scores)

## 📁 Struttura del Progetto

```
quiz-app/
│
├── index.html          # Struttura HTML e UI
├── style.css           # Stili CSS completi
├── quiz.js            # Logica principale dell'applicazione
├── questions.js       # Database delle domande
└── README.md          # Documentazione (questo file)
```

## 🔧 Funzionalità Tecniche

### JavaScript (ES6+)
- **Classi**: `QuizApp` per gestire lo stato e la logica
- **Arrow Functions**: Usate in tutto il codice
- **Template Literals**: Per HTML dinamico
- **Destructuring**: Per oggetti e array
- **Array Methods**: `map()`, `filter()`, `forEach()`, `sort()`
- **Async/Await**: Per fetch API (opzionale)
- **localStorage**: Per persistenza dati
- **Event Listeners**: Gestione interazioni utente

### CSS Features
- **CSS Variables**: Per colori e temi
- **Flexbox**: Per layout responsive
- **CSS Grid**: Per griglie di categorie
- **Animations**: Keyframes per transizioni
- **Media Queries**: Per design responsive
- **Pseudo-classes**: `:hover`, `:active`, `:disabled`
- **Transitions**: Per effetti fluidi

### HTML Features
- **Semantic HTML5**: `<header>`, `<nav>`, `<section>`, `<article>`
- **Data Attributes**: Per informazioni custom
- **Form Elements**: Input, button, select
- **Accessibility**: ARIA labels, semantic markup

## 📊 Struttura dei Dati

### Formato Domanda
```javascript
{
    question: "Testo della domanda",
    answers: [
        "Risposta A",
        "Risposta B",
        "Risposta C",
        "Risposta D"
    ],
    correct: 2,  // Indice della risposta corretta
    difficulty: "easy",  // easy, medium, hard
    explanation: "Spiegazione della risposta"
}
```

### Formato High Score
```javascript
{
    name: "Nome Giocatore",
    score: 150,
    category: "javascript",
    difficulty: "medium",
    correct: 8,
    total: 10,
    date: "ISO 8601 Date String"
}
```

## 🎯 Sistema di Punteggio

### Calcolo Punteggio
- **Punti Base**: 10 punti per risposta corretta
- **Bonus Tempo**: 1 punto per secondo rimanente
- **Massimo per Domanda**: 25 punti (10 base + 15 bonus tempo)
- **Massimo Totale**: 250 punti (10 domande × 25 punti)

### Esempio
- Risposta corretta con 10 secondi rimanenti: 10 + 10 = **20 punti**
- Risposta corretta con 15 secondi rimanenti: 10 + 15 = **25 punti**
- Risposta errata: **0 punti**

## 🎚️ Categorie e Domande

### JavaScript (15+ domande)
- ES6+ Features
- DOM Manipulation
- Functions and Scope
- Arrays and Objects
- Async JavaScript
- Error Handling
- Operators and Types

### HTML (12+ domande)
- Semantic HTML5
- Forms and Input
- Meta Tags
- Accessibility
- Multimedia Elements
- Canvas and SVG

### CSS (12+ domande)
- Flexbox and Grid
- Positioning
- Responsive Design
- Animations
- Selectors
- Box Model
- CSS Variables

### Generale (12+ domande)
- Web Development Concepts
- APIs and HTTP
- Git and Version Control
- SEO
- Security
- Performance

## � Personalizzazione

### Aggiungere Nuove Domande

Modifica il file `questions.js`:

```javascript
const questionsDB = {
    javascript: [
        {
            question: "La tua domanda qui?",
            answers: [
                "Opzione A",
                "Opzione B",
                "Opzione C",
                "Opzione D"
            ],
            correct: 0,  // Indice della risposta corretta (0-3)
            difficulty: "easy",
            explanation: "Spiegazione della risposta"
        },
        // ... altre domande
    ]
};
```

### Modificare il Tempo

Nel file `quiz.js`, modifica `config`:

```javascript
this.config = {
    questionsPerQuiz: 10,    // Numero di domande
    timePerQuestion: 15,      // Secondi per domanda
    pointsPerCorrectAnswer: 10,
    pointsPerTimeBonus: 1
};
```

### Modificare i Colori

Nel file `style.css`, modifica le CSS variables:

```css
:root {
    --primary-color: #6366f1;
    --secondary-color: #8b5cf6;
    --success-color: #10b981;
    --danger-color: #ef4444;
    /* ... altre variabili */
}
```

## 🔮 Funzionalità Future

- [ ] Multiplayer mode
- [ ] Domande da Open Trivia API
- [ ] Editor di domande custom
- [ ] Statistiche dettagliate
- [ ] Grafici andamento
- [ ] Modalità torneo
- [ ] Condivisione social
- [ ] Dark/Light mode toggle
- [ ] Supporto immagini nelle domande
- [ ] Audio effects

## 🐛 Troubleshooting

### High scores non si salvano
- Verifica che localStorage sia abilitato nel browser
- Controlla la console per errori

### Timer non funziona
- Assicurati che JavaScript sia abilitato
- Verifica che non ci siano estensioni che bloccano script

### Layout non responsive
- Cancella la cache del browser
- Verifica di usare un browser moderno

## 📝 Note Sviluppo

### Compatibilità Browser
- Chrome/Edge: ✅ Compatibile
- Firefox: ✅ Compatibile
- Safari: ✅ Compatibile
- Opera: ✅ Compatibile
- IE11: ❌ Non supportato (richiesto ES6+)

### Performance
- ~50 domande incluse
- Caricamento istantaneo
- Nessuna dipendenza esterna
- Ottimizzato per mobile

## 📄 Licenza

Questo progetto è open source e disponibile per scopi educativi.

## 👨‍💻 Sviluppatore

Creato come progetto portfolio dimostrativo delle capacità JavaScript, HTML e CSS.

---

**Divertiti con il quiz! 🎉**

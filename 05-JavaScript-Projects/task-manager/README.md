# 📋 Task Manager

Un'applicazione web per la gestione delle attività personali, sviluppata con puro HTML, CSS e JavaScript ES6+.

![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow)
![HTML](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)

## 🎯 Caratteristiche

### Funzionalità CRUD
- ✅ **Create**: Aggiungi nuove attività con titolo, descrizione, categoria, priorità e data di scadenza
- ✅ **Read**: Visualizza tutte le attività con filtri e ordinamento
- ✅ **Update**: Modifica le attività esistenti
- ✅ **Delete**: Elimina singole attività o rimuovi tutte quelle completate

### Categorie e Priorità
- **Categorie**: Lavoro 💼, Personale 👤, Studio 📚, Salute 💪, Altro 📌
- **Priorità**: Alta 🔴, Media 🟡, Bassa 🟢

### Filtri e Ordinamento
- Filtra per stato: Tutte, Attive, Completate
- Ordina per: Data di scadenza, Priorità, Titolo

### Statistiche in Tempo Reale
- Totale attività
- Attività attive
- Attività completate

### Persistenza dei Dati
- Salvataggio automatico in localStorage
- I dati persistono tra le sessioni del browser

## 🚀 Tecnologie Utilizzate

### JavaScript ES6+ Features
- **Arrow Functions**: Funzioni concise e sintassi moderna
- **Template Literals**: String interpolation con backticks
- **Spread Operator**: `...` per operazioni su array immutabili
- **Destructuring**: Estrazione proprietà da oggetti e array
- **Classes**: Sintassi OOP moderna
- **Modules**: Organizzazione del codice

### Array Methods
- **map()**: Trasformazione array (rendering task)
- **filter()**: Filtraggio task per stato
- **reduce()**: Calcolo statistiche
- **sort()**: Ordinamento per data, priorità, titolo
- **find()**: Ricerca task specifici

### Altre Feature
- **localStorage**: Persistenza dei dati nel browser
- **Event Listeners**: Gestione interazioni utente
- **DOM Manipulation**: Creazione dinamica UI
- **CSS Grid & Flexbox**: Layout responsive

## 📁 Struttura del Progetto

```
task-manager/
├── index.html      # Struttura HTML e UI
├── style.css       # Stili e animazioni
├── app.js          # Logica JavaScript (classe TaskManager)
└── README.md       # Documentazione
```

## 💻 Installazione e Utilizzo

1. **Clona o scarica il progetto**
2. **Apri `index.html` nel browser**
3. **Inizia a gestire le tue attività!**

Nessuna installazione o dipendenza richiesta - funziona direttamente nel browser!

## 🎨 Interfaccia Utente

### Dashboard Principale
- **Header**: Titolo dell'applicazione
- **Statistiche**: Card con totali in tempo reale
- **Form Aggiunta**: Crea nuove attività
- **Filtri**: Seleziona quali attività visualizzare
- **Lista Task**: Card con tutte le attività

### Card Attività
Ogni task mostra:
- Checkbox per completamento
- Titolo e descrizione
- Badge categoria e priorità
- Data di scadenza (con alert se scaduta)
- Pulsanti modifica ed eliminazione

### Modal Modifica
Finestra modale per modificare:
- Titolo
- Descrizione
- Categoria
- Priorità
- Data di scadenza

## 🔧 Funzionalità Tecniche

### Classe TaskManager
```javascript
class TaskManager {
    constructor()              // Inizializzazione
    addTask()                  // CREATE con spread operator
    getFilteredTasks()         // READ con filter() e sort()
    updateTask()               // UPDATE con map()
    deleteTask()               // DELETE con filter()
    updateStatistics()         // REDUCE per calcoli
    render()                   // MAP per rendering UI
}
```

### Esempi di Utilizzo Array Methods

#### MAP - Rendering Task
```javascript
const tasksHTML = filteredTasks.map(task =>
    this.createTaskHTML(task)
).join('');
```

#### FILTER - Attività Completate
```javascript
this.tasks = this.tasks.filter(task => !task.completed);
```

#### REDUCE - Calcolo Statistiche
```javascript
const stats = this.tasks.reduce((acc, task) => {
    acc.total++;
    if (task.completed) acc.completed++;
    else acc.active++;
    return acc;
}, { total: 0, active: 0, completed: 0 });
```

#### SORT - Ordinamento
```javascript
const sorted = [...tasks].sort((a, b) => {
    return new Date(a.dueDate) - new Date(b.dueDate);
});
```

#### SPREAD OPERATOR - Aggiunta Task
```javascript
this.tasks = [...this.tasks, newTask];
```

## 🎯 Concetti JavaScript Dimostrati

1. **OOP con Classi**: Struttura organizzata del codice
2. **Event Handling**: Gestione interazioni utente
3. **DOM Manipulation**: Creazione dinamica della UI
4. **Array Methods**: Manipolazione avanzata di array
5. **LocalStorage**: Persistenza dati lato client
6. **Template Literals**: Stringhe dinamiche
7. **Arrow Functions**: Sintassi concisa
8. **Spread Operator**: Operazioni immutabili
9. **Destructuring**: Estrazione dati
10. **Higher-Order Functions**: map, filter, reduce

## 📱 Responsive Design

L'applicazione è fully responsive:
- **Desktop**: Layout a griglia con statistiche orizzontali
- **Tablet**: Adattamento automatico delle colonne
- **Mobile**: Layout a colonna singola con filtri stackati

## 🎨 Animazioni

- **fadeIn**: Apparizione graduale elementi
- **slideIn**: Slide-in delle card task
- **pulse**: Alert per task scaduti
- **hover**: Effetti hover su card e bottoni

## 🔒 Privacy e Sicurezza

- Tutti i dati sono salvati **localmente** nel browser
- Nessuna comunicazione con server esterni
- Nessun tracking o analytics
- I dati rimangono privati sul dispositivo dell'utente

## 🚀 Possibili Miglioramenti

- [ ] Drag & drop per riordinare task
- [ ] Sottotask e checklist
- [ ] Promemoria e notifiche
- [ ] Temi chiaro/scuro
- [ ] Export/Import in JSON
- [ ] Sync con cloud storage
- [ ] Tag personalizzati
- [ ] Ricerca full-text
- [ ] Grafici andamento produttività

## 📄 License

Questo progetto è open source e disponibile per scopi educativi.

## 👨‍💻 Sviluppatore

Progetto sviluppato per dimostrare l'utilizzo avanzato di JavaScript ES6+ e dei metodi degli array.

---

**Nota**: Questo è un progetto educativo per praticare con JavaScript ES6+, manipolazione del DOM, e metodi degli array (map, filter, reduce, sort).

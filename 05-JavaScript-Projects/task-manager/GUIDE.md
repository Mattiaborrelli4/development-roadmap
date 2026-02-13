# 🚀 Guida Rapida - Task Manager

## 📖 Panoramica
Un'applicazione Task Manager completa sviluppata in puro JavaScript ES6+ con forte enfasi sui metodi degli array.

## 🎯 Funzionalità Principali

### 1. **CRUD Completo**
- ✅ **Create**: Aggiungi nuove attività
- ✅ **Read**: Visualizza, filtra e ordina attività
- ✅ **Update**: Modifica attività esistenti
- ✅ **Delete**: Elimina attività singole o multiple

### 2. **Categorie (5 tipi)**
- 💼 Lavoro
- 👤 Personale
- 📚 Studio
- 💪 Salute
- 📌 Altro

### 3. **Priorità (3 livelli)**
- 🔴 Alta
- 🟡 Media
- 🟢 Bassa

### 4. **Filtri**
- Tutte le attività
- Solo attive
- Solo completate

### 5. **Ordinamento**
- Per data di scadenza
- Per priorità
- Per titolo alfabetico

### 6. **Statistiche (con REDUCE)**
- Totale attività
- Attività attive
- Attività completate

## 🔧 Metodi Array Utilizzati

### `map()` - Rendering
```javascript
// Trasforma ogni task in HTML
const tasksHTML = filteredTasks.map(task =>
    this.createTaskHTML(task)
).join('');
```

### `filter()` - Filtraggio
```javascript
// Filtra per stato
const active = this.tasks.filter(task => !task.completed);

// Rimuovi completati
this.tasks = this.tasks.filter(task => !task.completed);
```

### `reduce()` - Statistiche
```javascript
// Calcola totali
const stats = this.tasks.reduce((acc, task) => {
    acc.total++;
    if (task.completed) acc.completed++;
    else acc.active++;
    return acc;
}, { total: 0, active: 0, completed: 0 });
```

### `sort()` - Ordinamento
```javascript
// Ordina per priorità
const sorted = [...tasks].sort((a, b) => {
    const order = { alta: 0, media: 1, bassa: 2 };
    return order[a.priority] - order[b.priority];
});
```

### `find()` - Ricerca
```javascript
// Trova task specifico
const task = this.tasks.find(t => t.id === id);
```

## 🎨 Features ES6+ Utilizzate

### Arrow Functions
```javascript
document.getElementById('add-task-form').addEventListener('submit', (e) => {
    e.preventDefault();
    this.addTask();
});
```

### Template Literals
```javascript
return `
    <div class="task-card">
        <h3>${task.title}</h3>
        <span>${categoryLabels[task.category]}</span>
    </div>
`;
```

### Spread Operator
```javascript
// Aggiungi task (immutabile)
this.tasks = [...this.tasks, newTask];

// Copia array prima di ordinare
const sorted = [...filtered].sort(...);
```

### Destructuring
```javascript
const { title, description, category, priority } = task;
```

### Classes
```javascript
class TaskManager {
    constructor() {
        this.tasks = [];
    }

    addTask() { /* ... */ }
}
```

## 📱 Come Usare

### 1. Apri il Progetto
```bash
cd task-manager
# Apri index.html nel browser
```

### 2. Aggiungi un Task
1. Compila il form "Aggiungi Nuova Attività"
2. Inserisci titolo (obbligatorio)
3. Aggiungi descrizione (opzionale)
4. Seleziona categoria e priorità
5. Imposta data di scadenza (opzionale)
6. Clicca "Aggiungi Attività"

### 3. Gestisci Task
- ✅ **Completa**: Click sulla checkbox
- ✏️ **Modifica**: Click su "Modifica"
- 🗑️ **Elimina**: Click su "Elimina"

### 4. Filtra e Ordina
- Usa i bottoni "Tutte/Attive/Completate"
- Usa il dropdown "Ordina per"

### 5. Pulisci
- Click "Rimuovi Completate" per eliminare tutte le attività completate

## 🗂️ Struttura del Codice

### `index.html`
- Header con titolo
- Sezione statistiche
- Form aggiunta task
- Filtri e ordinamento
- Lista task
- Modal modifica

### `style.css`
- Variabili CSS per colori
- Layout responsive (Grid/Flexbox)
- Animazioni (fadeIn, slideIn)
- Media queries per mobile
- Tema scuro moderno

### `app.js`
- **Classe TaskManager**: Logica principale
- **Metodi CRUD**: addTask, updateTask, deleteTask
- **Array methods**: map, filter, reduce, sort, find
- **Event listeners**: Gestione UI
- **LocalStorage**: Persistenza dati

## 💾 Persistenza

Tutti i dati sono salvati automaticamente in `localStorage`:
- Chiave: `taskManagerTasks`
- Formato: JSON
- Persistenza: Permanente nel browser

## 🎯 Concetti Chiave

### Immutabilità
```javascript
// ✅ Bene - Crea nuovo array
this.tasks = [...this.tasks, newTask];

// ❌ Male - Modifica array esistente
this.tasks.push(newTask);
```

### Higher-Order Functions
```javascript
// Funzioni che accettano funzioni come argomento
tasks.filter(t => t.completed)
     .map(t => t.title)
     .sort();
```

### Method Chaining
```javascript
this.tasks
    .filter(t => !t.completed)
    .sort((a, b) => a.priority - b.priority)
    .map(t => this.render(t));
```

## 🚀 Testing

### Test CRUD
1. Crea 5 task diversi
2. Modifica 2 task
3. Completa 3 task
4. Elimina 1 task
5. Verifica localStorage

### Test Filtri
1. Crea task attivi e completati
2. Testa filtro "Attive"
3. Testa filtro "Completate"
4. Verifica conteggi

### Test Ordinamento
1. Crea task con priorità diverse
2. Ordina per priorità
3. Ordina per data
4. Verifica ordinamento

## 📊 Statistiche in Tempo Reale

Le statistiche si aggiornano automaticamente:
- **Totale**: Tutte le attività
- **Attive**: Non completate
- **Completate**: Checkbox spuntata

Calcolate con `reduce()`:
```javascript
const stats = tasks.reduce((acc, task) => {
    acc.total++;
    task.completed ? acc.completed++ : acc.active++;
    return acc;
}, { total: 0, active: 0, completed: 0 });
```

## 🎨 UI Features

### Colori Categorie
- Lavoro: Blu (#3b82f6)
- Personale: Viola (#8b5cf6)
- Studio: Rosa (#ec4899)
- Salute: Verde (#10b981)
- Altro: Grigio (#64748b)

### Colori Priorità
- Alta: Rosso (#ef4444)
- Media: Giallo (#f59e0b)
- Bassa: Verde (#10b981)

### Animazioni
- Fade in per elementi nuovi
- Slide in per card task
- Pulse per task scaduti
- Hover effects interattivi

## 🔒 Sicurezza

- Sanitizzazione HTML per previene XSS
- Conferma per eliminazioni
- Validazione form lato client
- Nessun server - tutto locale

## 📝 Code Snippets Utili

### Toggle Completamento
```javascript
toggleTask(id) {
    this.tasks = this.tasks.map(task => {
        if (task.id === id) {
            return { ...task, completed: !task.completed };
        }
        return task;
    });
}
```

### Verifica Scadenza
```javascript
const isOverdue = task.dueDate &&
    new Date(task.dueDate) < new Date() &&
    !task.completed;
```

### Salva in LocalStorage
```javascript
saveTasks() {
    localStorage.setItem('taskManagerTasks', JSON.stringify(this.tasks));
}
```

## 🎯 Prossimi Passi

Suggerimenti per espandere il progetto:

1. **Drag & Drop** per riordinare
2. **Sottotask** con checklist
3. **Notifiche** per scadenze
4. **Temi** chiaro/scuro
5. **Export/Import** JSON
6. **Grafici** andamento produttività
7. **Tags** personalizzati
8. **Ricerca** full-text

---

**Divertiti a esplorare il codice e a imparare JavaScript ES6+!**

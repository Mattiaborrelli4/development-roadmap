# 🚀 Guida Rapida - React Task Manager

## Avvio Veloce

### 1. Installazione
```bash
cd "C:\Users\matti\Desktop\Project Ideas Portfolio\06-Web-Development\react-task-manager"
npm install
```

### 2. Avvio
```bash
npm run dev
```

### 3. Apri nel Browser
Vai su: **http://localhost:5173**

---

## 📋 Cheat Sheet - Comandi principali

### Navigazione React Hooks
```javascript
// useState - Gestione stato
const [tasks, setTasks] = useState([]);
const [filter, setFilter] = useState('tutte');

// useEffect - Effetti collaterali
useEffect(() => {
  // Codice da eseguire
}, [dipendenze]);

// LocalStorage con lazy initialization
const [tasks] = useState(() => {
  const saved = localStorage.getItem('tasks');
  return saved ? JSON.parse(saved) : [];
});
```

### Funzioni Principali
```javascript
// Aggiungi task
const addTask = () => { /* ... */ }

// Elimina task
const deleteTask = (id) => { /* ... */ }

// Toggle completamento
const toggleComplete = (id) => { /* ... */ }
```

---

## 🎯 Struttura Componenti

### App.jsx
- **Stato Principale**: tasks, newTask, category, priority, filter, searchTerm
- **Effetti**: Salva in LocalStorage quando tasks cambia
- **Render**: Container con header, stats, form, filtri, lista task

### Componenti UI
- **Header**: Titolo e sottotitolo
- **Stats**: Card con totali, attivi, completati
- **Form**: Input + select categoria + select priorità + button
- **Filtri**: Bottoni Tutte/Attive/Completate + Search
- **TaskList**: Lista task con card animate

---

## 🎨 CSS Key Classes

### Container
```css
.app           /* Wrapper principale */
.container     /* Container bianco */
.header        /* Header app */
.stats         /* Grid statistiche */
```

### Form
```css
.add-task-form   /* Grid form */
.task-input      /* Input principale */
.category-select /* Select categoria */
.priority-select /* Select priorità */
.add-button      /* Button aggiungi */
```

### Task Cards
```css
.task-card       /* Card singolo task */
.task-card.completed /* Task completato */
.checkbox        /* Checkbox circolare */
.task-text       /* Testo task */
.task-text-done  /* Testo completato */
.delete-button   /* Button elimina */
```

### Badges
```css
.category-badge  /* Badge categoria */
.category-lavoro / .category-personale / etc.
.priority-badge  /* Badge priorità */
.priority-alta / .priority-media / .priority-bassa
```

---

## 💾 LocalStorage

### Struttura Dati
```json
{
  "tasks": [
    {
      "id": 1234567890,
      "text": "Nome del task",
      "category": "lavoro",
      "priority": "alta",
      "completed": false,
      "createdAt": "2024-01-01T12:00:00.000Z"
    }
  ]
}
```

### Operazioni
```javascript
// Leggi
JSON.parse(localStorage.getItem('tasks'))

// Scrivi
localStorage.setItem('tasks', JSON.stringify(tasks))

// Cancella
localStorage.removeItem('tasks')
```

---

## 🐛 Debug Tips

### Console
```javascript
// Stampa stato
console.log('Tasks:', tasks)

// Stampa filtro
console.log('Filter:', filter)
```

### DevTools React
- Installa: React Developer Tools
- Componenti: Vedi stato e props
- Profiler: Analisi performance

---

## 📱 Responsive Breakpoints

```css
@media (max-width: 768px) {
  /* Mobile styles */
}
```

---

## ⌨️ Shortcut

| Tasto | Azione |
|-------|--------|
| Enter | Aggiungi task (con input focused) |
| Click checkbox | Completa task |
| Click 🗑️ | Elimina task |

---

## 🔧 Troubleshooting

### Server non parte?
```bash
# Cancella node_modules e reinstalla
rm -rf node_modules
rm package-lock.json
npm install
```

### LocalStorage vuoto?
- Apri DevTools → Application → Local Storage
- Controlla se ci sono task salvati

### CSS non funziona?
- Verifica che App.css sia importato in App.jsx
- Controlla la console per errori di caricamento

---

## 📚 Risorse Utili

- **React Docs**: https://react.dev/
- **Vite Docs**: https://vitejs.dev/
- **CSS Tricks**: https://css-tricks.com/
- **MDN LocalStorage**: https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage

---

**Creato per il portfolio di sviluppo web** ✨

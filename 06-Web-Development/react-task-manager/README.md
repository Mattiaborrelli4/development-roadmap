# 📋 React Task Manager

Un'applicazione moderna per la gestione dei task costruita con React e Vite. Questa applicazione permette di creare, gestire e tracciare i propri compiti quotidiani con un'interfaccia intuitiva e funzionalità avanzate.

## 📸 Screenshot dell'Applicazione

L'applicazione presenta un'interfaccia moderna con:
- Dashboard con statistiche in tempo reale
- Form per l'aggiunta rapida di task
- Filtri e ricerca avanzata
- Lista task organizzata per priorità
- Design responsive per dispositivi mobili

## ✨ Caratteristiche

### Funzionalità Principali
- ✅ **Aggiungi Task**: Crea nuovi task con titolo, categoria e priorità
- 🗑️ **Elimina Task**: Rimuovi task con un solo click
- ✓ **Completa Task**: Segna i task come completati con animazioni fluide
- 📊 **Statistiche**: Visualizza il riepilogo dei task (totali, attivi, completati)
- 🏷️ **Categorie**: Organizza i task per categoria (Lavoro, Personale, Studio, Salute, Altre)
- 🎯 **Priorità**: Assegna priorità ai task (Alta, Media, Bassa)
- 🔍 **Ricerca**: Cerca task in tempo reale
- 🎨 **Filtri**: Filtra task per stato (Tutte, Attive, Completate)
- 💾 **Persistenza**: I dati vengono salvati automaticamente nel LocalStorage del browser
- 📱 **Responsive**: Design adattivo per tutti i dispositivi

## 🛠️ Tecnologie Utilizzate

- **React 18** - Libreria JavaScript per costruire interfacce utente
- **Vite** - Strumento di build moderno e veloce
- **React Hooks** - useState, useEffect per la gestione dello stato
- **CSS3** - Stili moderni con animazioni e gradienti
- **LocalStorage API** - Persistenza dei dati nel browser

## 📦 Installazione

### Prerequisiti
Assicurati di avere installato:
- [Node.js](https://nodejs.org/) (versione 14 o superiore)
- [npm](https://www.npmjs.com/) o [yarn](https://yarnpkg.com/)

### Passi di Installazione

1. **Clona o naviga nella directory del progetto**
   ```bash
   cd "C:\Users\matti\Desktop\Project Ideas Portfolio\06-Web-Development\react-task-manager"
   ```

2. **Installa le dipendenze**
   ```bash
   npm install
   ```

3. **Avvia l'applicazione in modalità sviluppo**
   ```bash
   npm run dev
   ```

4. **Apri il browser**
   L'applicazione sarà disponibile all'indirizzo `http://localhost:5173`

## 🚀 Comandi Disponibili

```bash
# Avvia il server di sviluppo
npm run dev

# Crea una build di produzione
npm run build

# Anteprima della build di produzione
npm run preview

# Esegue i linting
npm run lint
```

## 📖 Come Usare

### Aggiungere un Nuovo Task

1. Digita il testo del task nell'campo di input principale
2. Seleziona una categoria dal menu a tendina:
   - 💼 Lavoro
   - 👤 Personale
   - 📚 Studio
   - 💪 Salute
   - 📌 Altre
3. Scegli la priorità:
   - 🔴 Alta
   - 🟡 Media
   - 🟢 Bassa
4. Clicca sul pulsante "➕ Aggiungi" o premi Enter

### Gestire i Task

- **Completare un task**: Clicca sul cerchio checkbox accanto al task
- **Eliminare un task**: Clicca sull'icona 🗑️
- **Visualizzare i dettagli**: Ogni task mostra categoria, priorità e data di creazione

### Filtrare i Task

Usa i pulsanti filtro nella parte superiore:
- **Tutte**: Mostra tutti i task
- **Attive**: Mostra solo i task non completati
- **Completate**: Mostra solo i task completati

### Cercare Task

Utilizza la barra di ricerca per trovare task specifici digitando parole chiave.

## 🎨 Struttura del Progetto

```
react-task-manager/
├── public/              # File statici
├── src/
│   ├── App.jsx         # Componente principale dell'applicazione
│   ├── App.css         # Stili dell'applicazione
│   ├── index.css       # Stili globali
│   └── main.jsx        # Punto di ingresso dell'applicazione
├── package.json        # Dipendenze e script
├── vite.config.js      # Configurazione di Vite
└── README.md           # Documentazione
```

## 💡 Concetti Chiave Implementati

### React Hooks

#### useState
Utilizzato per gestire lo stato locale dell'applicazione:
```javascript
const [tasks, setTasks] = useState([]);
const [newTask, setNewTask] = useState('');
const [category, setCategory] = useState('lavoro');
```

#### useEffect
Utilizzato per salvare automaticamente i task nel LocalStorage quando cambiano:
```javascript
useEffect(() => {
  localStorage.setItem('tasks', JSON.stringify(tasks));
}, [tasks]);
```

### Gestione dello Stato
- **Stato iniziale da LocalStorage**: I task vengono caricati dal LocalStorage all'avvio
- **Funzioni di aggiornamento**: `addTask`, `deleteTask`, `toggleComplete`
- **Filtri e ordinamento**: I task vengono filtrati e ordinati dinamicamente

### LocalStorage
L'applicazione persiste i dati nel browser, quindi i task rimangono disponibili anche dopo aver chiuso il browser.

## 🎯 Funzionalità Avanzate

### Ordinamento Automatico
I task vengono automaticamente ordinati per:
1. Stato di completamento (i task attivi vengono prima)
2. Priorità (Alta > Media > Bassa)

### Statistiche in Tempo Reale
La dashboard mostra sempre:
- Numero totale di task
- Task attivi (da completare)
- Task completati

### Animazioni
- Animazione di entrata per i nuovi task
- Effetti hover su card e pulsanti
- Transizioni fluide per il completamento dei task

## 🔧 Personalizzazione

### Modificare le Categorie
Modifica l'array delle categorie nel componente `App.jsx`:
```javascript
const categories = [
  'lavoro',
  'personale',
  'studio',
  'salute',
  'altre'
];
```

### Modificare i Colori
Modifica le variabili CSS in `App.css` per personalizzare i colori:
```css
.category-lavoro { background: #e3f2fd; color: #1976d2; }
.priority-alta { background: #ffebee; color: #c62828; }
```

## 🌐 Browser Supportati

- Chrome (ultima versione)
- Firefox (ultima versione)
- Safari (ultima versione)
- Edge (ultima versione)

## 📝 Note di Sviluppo

### Performance
- Utilizzo di React.memo per ottimizzare il rendering
- Ordinamento e filtraggio efficienti su liste grandi
- LocalStorage per accesso rapido ai dati

### Accessibilità
- Navigazione tramite tastiera (Enter per aggiungere task)
- Contrast ratio conforme alle linee guida WCAG
- Labels chiari per tutti gli input

## 🤝 Contribuire

Questo progetto è stato creato come portfolio personale. Sentiti libero di utilizzarlo come riferimento o base per i tuoi progetti!

## 📄 Licenza

Questo progetto è open source e disponibile per scopi educativi.

## 👤 Autore

Creato come parte del portfolio di progetti di sviluppo web.

## 🎓 Risorse di Apprendimento

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [MDN Web Docs - LocalStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage)

---

**Godi la gestione dei tuoi task! 📋✨**

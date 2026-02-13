# 🟨 JavaScript Projects - ES6+ Mastery
**Current Skill Level: 42%** ⚠️ **PRIORITÀ #1 - CRITICO!**

---

## 🟢 **BASICS - ES6+ Fundamentals**

### 1. ⏱️ **Pomodoro Timer**
- **Obiettivo**: DOM manipulation, setInterval
- **Features**:
  - 25min work / 5min break
  - Start/pause/reset
  - Audio notification
  - Session counter
- **Concetti**: let/const, arrow functions, setInterval, DOM
- **Tempo**: 3-5 giorni
- **GitHub**: ⭐ Ottimo primo progetto

### 2. 📝 **Markdown Editor**
- **Obiettivo**: Real-time parsing, template literals
- **Features**:
  - Live preview
  - Syntax highlighting
  - Export HTML
  - Local storage save
- **Concetti**: Template literals, destructuring, events
- **Tempo**: 7-10 giorni
- **Portfolio Value**: ALTO

### 3. 🎲 **Dice Game**
- **Obiettivo**: Random, DOM, game logic
- **Features**:
  - 2 players
  - Roll dice animation
  - Score tracking
  - Win conditions
- **Concetti**: Math.random, DOM manipulation, game state
- **Tempo**: 3-5 giorni

### 4. 💱 **Currency Converter**
- **Obiettivo**: fetch API, async/await
- **Features**:
  - Fetch tassi reali da API
  - Multiple currencies
  - Input validation
  - History
- **Concetti**: fetch, async/await, Promises, APIs
- **Tempo**: 5-7 giorni
- **Portfolio Value**: MEDIO

---

## 🟡 **INTERMEDIATE - Array Methods & Async**

### 5. 📋 **Task Manager (Advanced)**
- **Obiettivo**: CRUD operations, array methods
- **Features**:
  - Add/edit/delete tasks
  - Categories, priorities, due dates
  - Filter by status (map, filter)
  - Sort by priority (sort)
  - Statistics (reduce)
- **Concetti**: map, filter, reduce, sort, find, some, every
- **Tempo**: 7-10 giorni
- **Portfolio Value**: MOLTO ALTO

### 6. 🌦️ **Weather Dashboard**
- **Obiettivo**: Multiple API calls, error handling
- **Features**:
  - Current weather
  - 5-day forecast
  - Search by city
  - Geolocation
  - Charts for temperature
- **Concetti**: fetch, async/await, try/catch, APIs
- **Tempo**: 7-10 giorni
- **Portfolio Value**: ALTO

### 7. 📊 **Data Dashboard**
- **Obiettivo**: Chart.js, data visualization
- **Features**:
  - Fetch data from API
  - Multiple chart types
  - Interactive filters
  - Export data
- **Concetti**: Array methods, Chart.js, APIs
- **Tempo**: 10-14 giorni
- **Portfolio Value**: MOLTO ALTO

### 8. 🎵 **Music Player**
- **Obiettivo**: Audio API, complex state
- **Features**:
  - Play/pause/next/previous
  - Playlist
  - Progress bar
  - Volume control
- **Concetti**: Audio API, state management, events
- **Tempo**: 10-14 giorni
- **Portfolio Value**: ALTO

---

## 🔴 **ADVANCED - Complex Applications**

### 9. 💬 **Chat Application**
- **Obiettivo**: WebSockets, real-time
- **Features**:
  - Real-time messaging
  - Multiple chat rooms
  - User authentication
  - Message history
- **Concetti**: WebSockets, Socket.io, state management
- **Tempo**: 14-21 giorni
- **Portfolio Value**: MASSIMO

### 10. 🛒 **Shopping Cart**
- **Obiettivo**: Complex state, localStorage
- **Features**:
  - Add/remove products
  - Quantity management
  - Total calculation
  - Persist cart (localStorage)
  - Checkout simulation
- **Concetti**: Complex state, localStorage, reduce
- **Tempo**: 7-10 giorni
- **Portfolio Value**: ALTO

### 11. 🎮 **Memory Card Game**
- **Obiettivo**: Game logic, animations
- **Features**:
  - Card flip animations
  - Match detection
  - Score tracking
  - Difficulty levels
- **Concetti**: Game state, CSS animations, timing
- **Tempo**: 7-10 giorni
- **Portfolio Value**: MEDIO

### 12. 📝 **Quiz Application**
- **Obiettivo**: API, dynamic content
- **Features**:
  - Fetch questions da API
  - Multiple categories
  - Timer per domanda
  - Score tracking
  - High scores
- **Concetti**: APIs, state management, timing
- **Tempo**: 7-10 giorni
- **Portfolio Value**: ALTO

---

## 🏆 **Progetti MUST DO**

1. 🎯 **Pomodoro Timer** - Inizia qui
2. 🎯 **Task Manager** - Array methods mastery
3. 🎯 **Weather Dashboard** - API competence
4. 🎯 **Data Dashboard** - Data visualization

---

## ⚡ **ES6+ CRASH COURSE - OBBLIGATORIO!**

### **GIORNO 1-2: Basics**
```javascript
// let vs const vs var
let name = "Mattia";
const PI = 3.14;

// Arrow functions
const add = (a, b) => a + b;

// Template literals
const greeting = `Ciao ${name}!`;
```

### **GIORNO 3-4: Destructuring & Spread**
```javascript
// Destructuring
const {name, age} = person;
const [first, second] = array;

// Spread operator
const newArr = [...oldArr, newItem];
const newObj = {...oldObj, newProp: value};
```

### **GIORNO 5-7: Array Methods**
```javascript
// map - trasforma
const doubled = nums.map(n => n * 2);

// filter - filtra
const evens = nums.filter(n => n % 2 === 0);

// reduce - accumula
const sum = nums.reduce((acc, n) => acc + n, 0);

// find, some, every, sort
```

### **GIORNO 8-10: Async**
```javascript
// Promises
fetch(url).then(res => res.json());

// async/await
async function getData() {
  const res = await fetch(url);
  const data = await res.json();
  return data;
}

// try/catch
try {
  await getData();
} catch (error) {
  console.error(error);
}
```

### **GIORNO 11-14: Modules**
```javascript
// Export
export const name = "Mattia";
export default function() {}

// Import
import { name } from './module.js';
import defaultExport from './module.js';
```

---

## 📚 **Risorse per Imparare**

### Gratuiti
- **javascript.info** - Tutorial completo
- **freeCodeCamp JavaScript** - Pratica
- **MDN Web Docs** - Riferimento
- **JavaScript30** - 30 progetti in 30 giorni

### Corsi
- **Codecademy JavaScript** - Interattivo
- **Udemy "JavaScript Mastery"** - Completo

### Libri
- **"Eloquent JavaScript"** - Gratuito online
- **"You Don't Know JS"** - Gratuito su GitHub

### Practice
- **LeetCode JavaScript** - Algorithms
- **HackerRank JS** - Challenges
- **Codewars JS** - Katas

---

## 🎯 **Roadmap Consigliata**

```
Settimana 1: ES6+ basics (let/const, arrows, template literals)
Settimana 2: Array methods (map, filter, reduce)
Settimana 3: async/await, fetch API
Settimana 4: 2-3 progetti piccoli
Settimana 5-6: Progetto medio (Task Manager)
Settimana 7-8: Progetto complesso (Dashboard)
```

**Obiettivo**: JavaScript 42% → 75% in 2 mesi

# 📝 Markdown Editor

Un editor Markdown interattivo con anteprima in tempo reale, scritto in puro JavaScript ES6+.

![Markdown Editor](https://img.shields.io/badge/JavaScript-ES6+-yellow?logo=javascript)
![Status](https://img.shields.io/badge/stato-completato-green)

## 🎯 Caratteristiche

### Funzionalità Principali
- ✅ **Anteprima Live**: Visualizzazione in tempo reale mentre scrivi
- ✅ **Sintassi Markdown Supportata**:
  - Headers: `#`, `##`, `###`
  - Grassetto: `**testo**`
  - Corsivo: `*testo*`
  - Code inline: `` `codice` ``
  - Liste puntate: `- elemento`
  - Link: `[testo](url)`
- ✅ **Auto-salvataggio**: Salvataggio automatico nel LocalStorage
- ✅ **Export HTML**: Esporta il documento come file HTML
- ✅ **Responsive Design**: Funziona su desktop e mobile

### Feature JavaScript Moderne
- ✨ Classi ES6
- ✨ Arrow Functions
- ✨ Template Literals
- ✨ Const/Let
- ✨ Event Listeners
- ✨ LocalStorage API
- ✨ DOM Manipulation

## 📁 Struttura del Progetto

```
markdown-editor/
├── index.html      # Struttura HTML dell'applicazione
├── style.css       # Stili CSS con design moderno
├── app.js          # Logica JavaScript ES6+
└── README.md       # Documentazione
```

## 🚀 Come Utilizzare

### 1. Apri il Progetto
Apri il file `index.html` nel tuo browser preferito.

### 2. Scrivi in Markdown
Utilizza la sintassi Markdown nel pannello di sinistra:

```markdown
# Titolo Principale

## Sottotitolo

Questo è un paragrafo con **grassetto** e *corsivo*.

### Esempio di lista
- Primo elemento
- Secondo elemento
  - Sottoelemento
- Terzo elemento

Codice inline: `console.log('Hello')`
```

### 3. Guarda l'Anteprima
L'anteprima si aggiorna automaticamente mentre scrivi.

### 4. Esporta HTML
Clicca sul pulsante **"📥 Esporta HTML"** per scaricare il documento come file HTML.

## 💾 Salvataggio Automatico

Il tuo lavoro viene salvato automaticamente nel LocalStorage del browser. Se chiudi accidentalmente la pagina, i tuoi dati verranno ripristinati alla prossima apertura.

## 🎨 Stack Tecnologico

| Tecnologia | Utilizzo |
|-----------|----------|
| **HTML5** | Struttura semantica |
| **CSS3** | Styling con CSS Grid e Flexbox |
| **JavaScript ES6+** | Logica applicativa |

## 📚 Concetti JavaScript Appresi

### 1. Classi ES6
```javascript
class MarkdownEditor {
    constructor() {
        // Inizializzazione
    }

    metodo = () => {
        // Arrow function come metodo di classe
    }
}
```

### 2. Arrow Functions
```javascript
const parseMarkdown = (text) => {
    // Funzione arrow concisa
    return text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
}
```

### 3. Template Literals
```javascript
const message = `Salvato alle ${new Date().toLocaleTimeString()}`;
```

### 4. Event Listeners
```javascript
this.input.addEventListener('input', () => {
    this.updatePreview();
});
```

### 5. LocalStorage API
```javascript
// Salvataggio
localStorage.setItem('key', value);

// Caricamento
const value = localStorage.getItem('key');

// Rimozione
localStorage.removeItem('key');
```

### 6. RegExp per Parsing
```javascript
// Headers
text.replace(/^# (.*$)/gim, '<h1>$1</h1>');

// Bold
text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
```

## 🔧 Personalizzazione

### Aggiungere Nuovi Elementi Markdown
Modifica il metodo `parseMarkdown()` in `app.js`:

```javascript
// Esempio: aggiungere supporto per ~~cancellato~~
html = html.replace(/~~(.+?)~~/g, '<del>$1</del>');
```

### Modificare i Colori
Modifica le variabili CSS in `style.css`:

```css
:root {
    --primary-color: #2563eb;
    --success-color: #16a34a;
    /* ... altre variabili */
}
```

## 🎯 Obiettivi Didattici

Questo progetto insegna:
1. ✅ Programmazione orientata agli oggetti in JavaScript
2. ✅ Manipolazione del DOM
3. ✅ Event handling
4. ✅ LocalStorage per persistenza dati
5. ✅ Regular Expressions per parsing
6. ✅ Modularità del codice
7. ✅ Responsive design con CSS Grid

## 🌐 Browser Compatibili

- ✅ Chrome/Edge (consigliato)
- ✅ Firefox
- ✅ Safari
- ✅ Opera

## 📝 Note di Sviluppo

### Pattern Utilizzati
- **Class-based Architecture**: Codice organizzato in classe
- **Separation of Concerns**: HTML, CSS e JS separati
- **Progressive Enhancement**: Funzionalità base senza JavaScript
- **DRY Principle**: Codice riutilizzabile

### Ottimizzazioni Future
- [ ] Supporto per code blocks con syntax highlighting
- [ ] Modalità scura/chiara
- [ ] Export PDF
- [ ] Supporto tabelle
- [ ] Undo/Redo history

## 🤝 Contributi

Questo è un progetto educativo. Sentiti libero di utilizzarlo come base per i tuoi progetti!

## 📄 Licenza

Questo progetto è disponibile per scopi educativi.

---

**Creato con ❤️ per imparare JavaScript ES6+**

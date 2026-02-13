# 🛒 Carrello della Spesa - Progetto JavaScript

Un'applicazione web completa per la gestione di un carrello della spesa, realizzata con puro JavaScript (ES6+), HTML e CSS.

![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow)
![HTML5](https://img.shields.io/badge/HTML5-Latest-orange)
![CSS3](https://img.shields.io/badge/CSS3-Latest-blue)

## 📋 Descrizione

Questo progetto è una dimostrazione pratica delle capacità di JavaScript moderno per la gestione dello stato, la manipolazione del DOM e la persistenza dei dati. L'applicazione permette di visualizzare prodotti, aggiungerli al carrello, gestire le quantità e completare un ordine convalidando un form.

## ✨ Funzionalità

- **📦 Catalogo Prodotti**: Visualizzazione di 8 prodotti con immagini, categorie e descrizioni
- **➕ Aggiunta al Carrello**: Clic su prodotto per aggiungere al carrello con notifica
- **🔢 Gestione Quantità**: Aumenta/ diminuisci quantità con pulsanti + e -
- **🗑️ Rimozione Prodotti**: Rimozione singola prodotti dal carrello
- **💰 Calcolo Totale**: Calcolo automatico del totale usando `reduce()`
- **💾 Persistenza Dati**: Salvataggio automatico in `localStorage`
- **🛍️ Sidebar Carrello**: Panello laterale con riepilogo articoli
- **✅ Checkout Completo**: Form con validazione dei campi
- **📧 Conferma Ordine**: Modal di successo con numero ordine
- **📱 Design Responsivo**: Adattamento a tutti i dispositivi

## 🚀 Tecnologie Utilizzate

### JavaScript ES6+
- **Arrow Functions**: Funzioni con sintassi concisa
- **Template Literals**: Stringhe con interpolazione variabili
- **Destructuring**: Estrazione proprietà da oggetti
- **Spread Operator**: `...` per copiare e combinare oggetti
- **Array Methods**: `map()`, `filter()`, `find()`, `reduce()`
- **Modules**: `import`/`export` per organizzazione codice
- **Classes & Objects**: Struttura dati prodotti
- **localStorage API**: Persistenza dati nel browser

### HTML5
- Elementi semantici (`header`, `main`, `aside`, `article`)
- Forms HTML5 con validazione nativa
- attributi ARIA per accessibilità
- Modal e overlay

### CSS3
- **CSS Variables**: Custom properties per temi
- **Flexbox**: Layout flessibili
- **CSS Grid**: Griglia prodotti responsiva
- **Transitions**: Animazioni fluide
- **Media Queries**: Design responsivo
- **CSS Selectors**: Selezione avanzata elementi

## 📁 Struttura del Progetto

```
shopping-cart/
│
├── index.html          # Struttura HTML e UI
├── style.css          # Stili CSS e animazioni
├── products.js        # Database prodotti
├── cart.js            # Gestione stato carrello
├── main.js            # Script principale
└── README.md          # Documentazione
```

## 🎯 Concetti Chiave

### 1. Gestione dello Stato

Il carrello mantiene un array di oggetti:

```javascript
let cart = [
  {
    id: 1,
    name: "Laptop Pro 15",
    price: 1299.99,
    image: "...",
    quantity: 2
  }
];
```

### 2. Array.reduce() per Calcolo Totale

Utilizzo di `reduce()` per calcolare il totale del carrello:

```javascript
const calculateTotal = () => {
  return cart.reduce((total, item) => {
    return total + (item.price * item.quantity);
  }, 0);
};
```

### 3. Spread Operator per Creazione Oggetti

Copia e modifica di oggetti con spread operator:

```javascript
cart.push({
  ...product,
  quantity
});
```

### 4. localStorage per Persistenza

Salvataggio e caricamento del carrello:

```javascript
// Salvataggio
localStorage.setItem('cart', JSON.stringify(cart));

// Caricamento
cart = JSON.parse(localStorage.getItem('cart')) || [];
```

### 5. Validazione Form

Validazione lato client con feedback visivo:

```javascript
const validateCheckoutForm = (formData) => {
  const errors = [];
  // Validazione campi obbligatori
  // Validazione email con regex
  // Validazione CAP numerico
  return errors;
};
```

## 🔧 Installazione e Utilizzo

### Prerequisiti
- Un browser moderno (Chrome, Firefox, Safari, Edge)
- Un server locale per evitare problemi CORS (opzionale ma raccomandato)

### Avvio Rapido

1. **Clona o scarica il progetto**

2. **Avvia un server locale**:

   ```bash
   # Con Python 3
   python -m http.server 8000

   # Con Node.js (npx)
   npx serve

   # Con PHP
   php -S localhost:8000
   ```

3. **Apri il browser**:
   ```
   http://localhost:8000
   ```

### Alternativa: Apertura Diretta

Per aprire direttamente senza server (alcune features potrebbero non funzionare):

1. Apri `index.html` nel browser
2. Nota: I moduli ES6 potrebbero non funzionare senza server

## 📖 Guida all'Uso

### Navigazione

1. **Visualizza Prodotti**: Scorri la griglia dei prodotti disponibili
2. **Aggiungi al Carrello**: Clicca il pulsante "Aggiungi" su qualsiasi prodotto
3. **Apri Carrello**: Clicca l'icona carrello in alto a destra
4. **Gestisci Quantità**: Usa i pulsanti + e - per modificare le quantità
5. **Rimuovi Prodotti**: Clicca l'icona cestino per rimuovere un prodotto
6. **Checkout**: Clicca "Procedi al Checkout" per completare l'ordine
7. **Compila il Form**: Inserisci i dati di spedizione
8. **Conferma**: Clicca "Conferma Ordine" per finalizzare

### Persistenza Automatica

Il carrello viene salvato automaticamente in localStorage. Chiudi e riapri il browser per vedere che i prodotti rimangono nel carrello.

## 🎨 Features Tecniche Avanzate

### Gestione Eventi

```javascript
// Event delegation per elementi dinamici
document.addEventListener('click', (e) => {
  if (e.target.matches('.add-to-cart-btn')) {
    // Gestisci click
  }
});
```

### Modularità

Codice organizzato in moduli ES6:

```javascript
// Import di funzioni specifiche
import { addToCart, removeFromCart } from './cart.js';
import { products } from './products.js';
```

### Reactive UI

Aggiornamento automatico dell'interfaccia quando lo stato cambia:

```javascript
const updateCartUI = () => {
  // Aggiorna contatore, lista, totale
  renderCartCount();
  renderCartItems();
  renderTotal();
};
```

### Formattazione Internazionalizzata

Utilizzo di `Intl.NumberFormat` per formattazione valuta:

```javascript
const formatPrice = (price) => {
  return new Intl.NumberFormat('it-IT', {
    style: 'currency',
    currency: 'EUR'
  }).format(price);
};
```

## 🐛 Debug e Sviluppo

### Console Logging

Il progetto include messaggi di errore nella console:

```javascript
console.error('Errore nel caricamento:', error);
```

### Strumenti per Sviluppatori

1. **Console**: Visualizza log e errori
2. **Application Tab**: Ispeziona localStorage
3. **Network Tab**: Monitora richieste (future API call)
4. **Elements Tab**: Ispeziona DOM e CSS

### Testing

Test manuali consigliati:

- ✅ Aggiunta singolo prodotto
- ✅ Aggiunta multipla dello stesso prodotto
- ✅ Modifica quantità (aumento e diminuzione)
- ✅ Rimozione prodotto
- ✅ Calcolo totale corretto
- ✅ Persistenza dopo refresh
- ✅ Validazione form (campi vuoti, email invalida)
- ✅ Responsive design (mobile, tablet, desktop)

## 🔐 Sicurezza e Best Practices

### Sanitizzazione Input

Anche se in questo progetto i dati sono statici, in produzione:

```javascript
// Sanitizza input utente
const sanitizeInput = (input) => {
  return input.trim().replace(/</g, "&lt;").replace(/>/g, "&gt;");
};
```

### Validazione lato Client

La validazione JavaScript è solo la prima linea di difesa. In produzione, valida sempre anche lato server.

### XSS Prevention

Non usare `innerHTML` con input non trusted:

```javascript
// ⚠️ Pericoloso
element.innerHTML = userInput;

// ✅ Sicuro
element.textContent = userInput;
```

## 🚀 Possibili Miglioramenti

### Backend Integration
- Connessione a API REST per prodotti reali
- Autenticazione utenti
- Pagamenti online (Stripe, PayPal)
- Gestione ordini server-side

### Features Avanzate
- Filtri e ricerca prodotti
- Ordinamento per prezzo/nome
- Recensioni prodotti
- Wishlist/Favoriti
- Sconti e codici promozionali
- Spedizione multipla

### Performance
- Lazy loading immagini
- Virtual scrolling per molti prodotti
- Code splitting
- Service Worker per PWA

### Testing
- Unit test con Jest
- E2E test con Playwright/Cypress
- Test accessibilità

## 📚 Risorse di Apprendimento

### JavaScript
- [MDN Web Docs - JavaScript](https://developer.mozilla.org/it/docs/Web/JavaScript)
- [JavaScript.info](https://javascript.info/)
- [ES6 Features](https://es6-features.org/)

### CSS
- [CSS Tricks](https://css-tricks.com/)
- [MDN Web Docs - CSS](https://developer.mozilla.org/it/docs/Web/CSS)

### localStorage
- [MDN - localStorage](https://developer.mozilla.org/it/docs/Web/API/Window/localStorage)

## 📝 Licenza

Questo progetto è creato a scopo educativo. Sei libero di utilizzarlo, modificarlo e distribuirlo.

## 👨‍💻 Autore

Progetto realizzato come dimostrazione delle capacità di sviluppo web con JavaScript moderno.

---

**Nota**: Questo progetto utilizza immagini da Unsplash. Assicurati di avere una connessione internet attiva per visualizzare le immagini dei prodotti.

## 🤝 Contributi

I contributi sono benvenuti! Sentiti libero di:
- Segnalare bug
- Suggerire nuove features
- Inviare pull request
- Migliorare la documentazione

Buon coding! 🎉

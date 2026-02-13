# 💬 Chat App - Applicazione di Messaggistica in Tempo Reale (Simulata)

Un'applicazione di chat completa scritta in puro JavaScript (ES6+) che simula un sistema di messaggistica in tempo reale con persistenza locale.

![Versione](https://img.shields.io/badge/versione-1.0.0-blue)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow)
![HTML](https://img.shields.io/badge/HTML5-red)
![CSS](https://img.shields.io/badge/CSS3-purple)

## 🌟 Caratteristiche Principali

### Funzionalità Core
- **✅ Messaggistica in Tempo Reale (Simulata)**: Ricevi automaticamente messaggi da altri utenti simulati
- **✅ Stanze Multiple**: 5 stanze di chat diverse (Generale, Tecnologia, Musica, Giochi, Off-Topic)
- **✅ Username Personalizzato**: Inserisci il tuo username all'accesso
- **✅ Cronologia Messaggi**: Tutti i messaggi vengono salvati in localStorage
- **✅ Invio/Ricezione Messaggi**: Sistema completo di scambio messaggi
- **✅ Timestamp**: Ogni messaggio mostra l'ora di invio
- **✅ Lista Utenti Online**: Vedi chi è online in tempo reale

### Funzionalità Avanzate
- **💾 Persistenza Locale**: I messaggi restano salvati anche dopo la chiusura del browser
- **🔔 Badge di Notifica**: Ricevi notifiche per nuovi messaggi nelle altre stanze
- **⌨️ Indicatore di Digitazione**: Simula quando altri utenti stanno scrivendo
- **🎨 Design Moderno**: Interfaccia ispirata a Discord
- **📱 Responsive**: Funziona perfettamente su dispositivi mobili
- **🗑️ Cancella Cronologia**: Possibilità di pulire la cronologia di ogni stanza

## 🚀 Guida Rapida all'Uso

### 1. Apertura dell'Applicazione
Apri semplicemente il file `index.html` nel tuo browser preferito.

### 2. Login
- Inserisci il tuo username (minimo 2 caratteri)
- Clicca su "Entra nella Chat"
- Il tuo username verrà salvato per le prossime sessioni

### 3. Inviare Messaggi
- Scrivi nel campo di testo in basso
- Premi Invio o clicca "Invia"
- Il messaggio appare immediatamente nella chat

### 4. Cambiare Stanza
- Clicca su una stanza nella sidebar sinistra
- Verrai portato a quella stanza
- I badge indicano nuovi messaggi non letti

### 5. Logout
- Clicca il pulsante "Esci" in fondo alla sidebar
- Conferma di voler uscire
- Il tuo username verrà rimosso

## 🏗️ Architettura Tecnica

### Struttura dei File
```
chat-app/
├── index.html      # Interfaccia utente
├── style.css       # Styling completo
├── chat.js         # Logica dell'applicazione
└── README.md       # Documentazione
```

### Tecnologie Utilizzate
- **HTML5**: Struttura semantica
- **CSS3**: Flexbox, Animazioni, CSS Variables
- **JavaScript ES6+**: Classi, Arrow Functions, Template Literals, Array Methods

### Concetti Chiave Implementati

#### 1. Classi ES6
```javascript
class ChatApplication {
    constructor() {
        // Inizializzazione
    }

    // Metodi della classe
}
```

#### 2. LocalStorage per Persistenza
```javascript
// Salvataggio
localStorage.setItem('chat_messages_' + room, JSON.stringify(messages));

// Caricamento
const stored = localStorage.getItem('chat_messages_' + room);
return stored ? JSON.parse(stored) : [];
```

#### 3. setInterval per Simulazione
```javascript
// Simula messaggi in arrivo ogni 15 secondi
setInterval(() => {
    this.simulateIncomingMessage();
}, 15000);
```

#### 4. Array Methods
```javascript
// Filter
const otherUsers = users.filter(u => !u.isCurrentUser);

// Map
const messagesHTML = messages.map(msg => this.createMessageHTML(msg));

// Find
const room = rooms.find(r => r.name === roomName);
```

#### 5. Template Literals
```javascript
const html = `
    <div class="message">
        <span>${username}</span>
        <span>${text}</span>
    </div>
`;
```

## 🔧 Funzionalità Tecniche

### Sistema di Simulazione

#### Messaggi Automatici
Ogni 15-30 secondi, un utente simulato invia un messaggio in una stanza casuale. I messaggi sono contestuali alla stanza:
- **Tecnologia**: Discussione su framework, linguaggi di programmazione
- **Musica**: Album, artisti, consigli musicali
- **Giochi**: Videogiochi, tornei, piattaforme
- **Off-Topic**: Discussioni casuali

#### Utenti Online Simulati
Il sistema gestisce dinamicamente gli utenti online:
- 3-6 utenti attivi inizialmente
- Un utente può entrare o uscire ogni 45 secondi
- Gli utenti hanno nomi, avatar e colori unici

### Gestione dello Stato

#### Messaggi per Stanza
```javascript
this.messages = {
    'generale': [...],
    'tecnologia': [...],
    'musica': [...],
    'giochi': [...],
    'off-topic': [...]
};
```

#### Utenti Online
```javascript
this.onlineUsers = [
    { name: 'Mario', avatar: 'M', color: '#e74c3c', isCurrentUser: false },
    { name: 'Tu', avatar: 'T', isCurrentUser: true }
];
```

## 🎨 Design e UX

### Palette Colori
- **Primario**: `#5865F2` (Blu Discord)
- **Sfondo Scuro**: `#36393f`
- **Testo**: `#dcddde`
- **Successo**: `#43b581`
- **Pericolo**: `#f04747`

### Animazioni
- **Fade In**: Messaggi appaiono con animazione fluida
- **Hover**: Effetti hover su tutti gli elementi interattivi
- **Typing Indicator**: Tre pallini che saltano quando qualcuno scrive

### Responsive Design
- Sidebar mobile-friendly
- Messaggi ottimizzati per schermi piccoli
- Touch-friendly buttons

## 📊 Flussi di Dati

### 1. Invio Messaggio
```
User Input → Validazione → Creazione Oggetto Messaggio
→ Aggiunta Array → Salvataggio LocalStorage
→ Render DOM → Scroll Bottom
```

### 2. Ricezione Messaggio (Simulato)
```
Timer Scaduto → Selezione Utente Random → Selezione Stanza
→ Generazione Messaggio Contestuale → Aggiunta Array
→ Salvataggio LocalStorage → Aggiorna UI (se stanza corrente)
→ Badge Notifica (se altra stanza)
```

### 3. Cambio Stanza
```
Click Stanza → Aggiorna Current Room → Aggiorna UI Attiva
→ Nascondi Badge → Carica Messaggi Stanza → Render
```

## 🛡️ Sicurezza

### XSS Prevention
Tutti i messaggi vengono sanitizzati usando `textContent` prima del rendering:

```javascript
escapeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}
```

### Validazione Input
- Username: minimo 2 caratteri, massimo 20
- Messaggio: massimo 500 caratteri
- Trim per rimuovere spazi vuoti

## 🔮 Possibili Miglioramenti

### Funzionalità Future
- [ ] Emoji picker completo
- [ ] Upload immagini (base64)
- [ ] Ricerca nei messaggi
- [ ] Stanze private/protette da password
- [ ] Mention degli utenti (@username)
- [ ] Moderazione messaggi
- [ ] Temi personalizzabili
- [ ] Notifiche sonore

### Backend Reale
Per trasformare in un'applicazione reale:
1. Sostituire localStorage con WebSocket
2. Implementare autenticazione server-side
3. Database per messaggi (MongoDB, PostgreSQL)
4. API RESTful per operazioni CRUD
5. Sistema di notifiche push

## 📝 Note Tecniche

### Performance
- Lazy loading dei messaggi (pagination per chat grandi)
- Debounce per l'indicatore di digitazione
- Ottimizzazioni rendering DOM

### Compatibilità Browser
- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Mobile browsers

### Limitazioni
- **No Backend**: Tutti i dati sono locali
- **Simulazione**: Messaggi e utenti sono generati
- **Single User**: Non supporta comunicazioni reali tra utenti

## 👨‍💻 Esempi di Utilizzo

### Scenario 1: Nuovo Utente
1. Apri `index.html`
2. Inserisci "Mario" come username
3. Entra nella chat
4. Scrivi "Ciao a tutti!"
5. Aspetta 15 secondi
6. Ricevi risposte automatiche da altri utenti

### Scenario 2: Cambio Stanza
1. Clicca su "#tecnologia"
2. Leggi i messaggi precedenti
3. Scrivi una domanda su JavaScript
4. Torna a "#generale"
5. Nota il badge con nuovi messaggi

### Scenario 3: Persistenza
1. Scrivi diversi messaggi
2. Chiudi il browser
3. Riapri `index.html`
4. I tuoi messaggi sono ancora lì!

## 📚 Risorse Utili

### Documentazione
- [MDN Web Docs - LocalStorage](https://developer.mozilla.org/it/docs/Web/API/Window/localStorage)
- [JavaScript ES6+ Features](https://es6-features.org/)
- [CSS Flexbox Guide](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)

### Tutorial Correlati
- Building a Chat App with Vanilla JavaScript
- Understanding WebSockets
- CSS Animation Techniques

## 🤝 Contributi

Questo è un progetto educativo. Sentiti libero di:
- Fare fork del progetto
- Aprire issue per bug
- Proporre nuove feature
- Migliorare il codice

## 📄 Licenza

Questo progetto è open source e disponibile per scopi educativi.

---

**Creato con ❤️ usando puro JavaScript (ES6+)**

*Nota: Questa è un'applicazione dimostrativa che simula una chat reale. Non c'è comunicazione con server esterni e tutti i dati rimangono locali sul tuo browser.*

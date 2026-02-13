# 🔐 Verificatore Forza Password

Un'applicazione web per l'analisi in tempo reale della forza delle password, sviluppata con HTML, CSS e JavaScript puro.

![Password Strength Checker](https://img.shields.io/badge/Stato-Completato-success)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)

## 📋 Descrizione

Il Verificatore Forza Password è uno strumento interattivo che analizza la sicurezza delle password in tempo reale. L'applicazione valuta diversi criteri di sicurezza e fornisce feedback immediato con suggerimenti per migliorare la propria password.

### ⚡ Caratteristiche

- ✅ **Analisi in Tempo Reale**: Feedback istantaneo mentre digiti
- 📊 **Indicatore Visivo di Forza**: Barra di progresso colorata da 0 a 5 livelli
- 🔍 **Controllo Multiplo dei Criteri**:
  - Lunghezza minima di 8 caratteri
  - Presenza di numeri
  - Lettere maiuscole
  - Lettere minuscole
  - Caratteri speciali (!@#$%...)
  - Verifica contro password comuni
- 💡 **Consigli Personalizzati**: Suggerimenti specifici per migliorare la password
- ⏱️ **Stima del Tempo di Crack**: Quanto tempo servirebbe per craccare la password
- 👁️ **Toggle Visibilità**: Mostra/nascondi password con un click
- 🔒 **100% Client-Side**: Nessun dato viene inviato a server
- 📱 **Design Responsive**: Funziona su desktop, tablet e smartphone

## 🚀 Come Utilizzare

### Opzione 1: Aprire Direttamente

1. Scarica o clona questo repository
2. Apri il file `index.html` nel tuo browser preferito
3. Inizia a digitare una password per vedere l'analisi in tempo reale

### Opzione 2: Server Locale (Opzionale)

Se vuoi servire l'applicazione con un server locale:

```bash
# Using Python 3
python -m http.server 8000

# Using Python 2
python -m SimpleHTTPServer 8000

# Using Node.js (npx)
npx serve

# Using PHP
php -S localhost:8000
```

Poi apri `http://localhost:8000` nel tuo browser.

## 📁 Struttura del Progetto

```
password-checker/
│
├── index.html          # Struttura HTML principale
├── style.css           # Foglio di stile con design dark mode
├── script.js           # Logica di analisi password
└── README.md           # Documentazione del progetto
```

## 🎯 Funzionalità nel Dettaglio

### Criteri di Valutazione

L'applicazione valuta la password su 6 criteri:

1. **Lunghezza**: Minimo 8 caratteri (bonus per 12+ e 16+)
2. **Numeri**: Deve contenere almeno una cifra (0-9)
3. **Maiuscole**: Deve contenere almeno una lettera maiuscola
4. **Minuscole**: Deve contenere almeno una lettera minuscola
5. **Speciali**: Deve contenere caratteri speciali (!@#$%^&*...)
6. **Non Comune**: Non deve essere tra le password più comuni

### Sistema di Punteggio

- **0/5 - Molto Debole**: Password molto corta o comune
- **1/5 - Debole**: Mancano molti criteri di sicurezza
- **2/5 - Discreta**: Soddisfa alcuni criteri base
- **3/5 - Buona**: Buona combinazione di caratteri
- **4/5 - Forte**: Eccellente mix di caratteri e lunghezza
- **5/5 - Molto Forte**: Massimo livello di sicurezza

### Stima del Tempo di Crack

L'applicazione stima quanto tempo servirebbe per craccare la password assumendo:
- 10 miliardi di tentativi al secondo (hash veloce)
- Attacco brute force ottimizzato
- Calcolo basato sulla dimensione del character pool

## 🔒 Privacy e Sicurezza

⚠️ **IMPORTANTE**: Questa applicazione:

- ✅ NON salva le password inserite
- ✅ NON invia dati a server esterni
- ✅ NON utilizza cookie o local storage per le password
- ✅ Esegue tutte le elaborazioni nel browser (client-side)

**Nota**: Usa questo strumento solo per scopi educativi e di test. Non inserire mai password reali in strumenti online di cui non ti fidi completamente.

## 🎨 Design e UX

- **Dark Mode**: Design moderno con sfondo scuro per ridurre l'affaticamento oculare
- **Feedback Visivo**: Colori intuitivi (rosso=debole, verde=forte)
- **Animazioni**: Transizioni fluide per una migliore esperienza utente
- **Accessibilità**: Supporto per screen reader e navigazione da tastiera
- **Responsive**: Layout adattivo per tutti i dispositivi

## 🛠️ Tecnologie Utilizzate

- **HTML5**: Semantica strutturale
- **CSS3**: Flexbox, Grid, CSS Variables, Animations
- **JavaScript ES6+**: Classi, Arrow Functions, Template Literals

## 📚 Concetti Appresi

Questo progetto è stato creato per dimostrare e praticare:

1. Validazione e sanitizzazione degli input
2. Manipolazione del DOM in tempo reale
3. Espressioni regolari per pattern matching
4. Calcolo della complessità delle password
5. Design responsive e accessibile
6. Gestione dello stato in JavaScript
7. Privacy-first development (no data collection)

## 🔧 Personalizzazione

### Aggiungere Altre Password Comuni

Modifica l'array `commonPasswords` nel file `script.js`:

```javascript
const commonPasswords = [
    'password',
    '123456',
    // Aggiungi qui altre password comuni
];
```

### Modificare i Criteri di Valutazione

Cerca la classe `PasswordStrengthChecker` in `script.js` e modifica:

```javascript
this.criteria = {
    length: password.length >= 8,  // Modifica la lunghezza minima
    // ... altri criteri
};
```

### Cambiare i Colori

Modifica le variabili CSS in `style.css`:

```css
:root {
    --primary-color: #6366f1;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    /* ... altre variabili */
}
```

## 🌐 Browser Supportati

- ✅ Chrome/Edge (ultimi 2 anni)
- ✅ Firefox (ultimi 2 anni)
- ✅ Safari (ultimi 2 anni)
- ✅ Opera (ultimi 2 anni)

## 📄 Licenza

Questo progetto è stato creato per scopi educativi ed è disponibile per uso personale e commerciale.

## 👨‍💻 Autore

Progetto realizzato per il portfolio di sicurezza informatica.

---

**Nota di Sicurezza**: Ricorda sempre di:
- Usare password uniche per ogni account
- Attivare l'autenticazione a due fattori dove disponibile
- Utilizzare un password manager sicuro
- Non condividere mai le tue password

🔐 **Proteggi i tuoi dati, proteggi la tua privacy!**

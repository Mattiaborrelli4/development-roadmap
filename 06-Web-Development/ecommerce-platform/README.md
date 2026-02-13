# ShopOnline - Piattaforma E-Commerce

Una piattaforma E-Commerce completa sviluppata con React, featuring un catalogo prodotti, carrello della spesa, checkout, autenticazione utenti e pannello di amministrazione.

## Caratteristiche

### Funzionalità Principali
- **Catalogo Prodotti**: Visualizzazione di prodotti con categorie e filtri
- **Dettagli Prodotto**: Pagina dedicata con galleria immagini e descrizione
- **Carrello della Spesa**: Aggiunta, rimozione e modifica quantità prodotti
- **Checkout Flow**: Form di spedizione e pagamento simulato
- **Autenticazione Utenti**: Login e registrazione
- **Storico Ordini**: Visualizzazione degli ordini effettuati
- **Pannello Admin**: Gestione prodotti e visualizzazione ordini
- **Ricerca e Filtri**: Ricerca prodotti per nome e filtri per categoria/prezzo

### Caratteristiche Tecniche
- **React 18** con Functional Components e Hooks
- **React Router 6** per il routing
- **Context API** per la gestione dello stato (Cart e Auth)
- **localStorage** per la persistenza del carrello e dati utente
- **Design Responsivo** per mobile e desktop
- **CSS Modules** per stili component-based
- **18 Prodotti Sample** con immagini placeholder da Unsplash

## Installazione

### Prerequisiti
- Node.js (v14 o superiore)
- npm o yarn

### Passi di Installazione

1. **Naviga nella cartella del progetto**
```bash
cd "C:\Users\matti\Desktop\Project Ideas Portfolio\06-Web-Development\ecommerce-platform"
```

2. **Installa le dipendenze**
```bash
npm install
```

3. **Avvia l'applicazione**
```bash
npm start
```

L'applicazione si aprirà automaticamente su [http://localhost:3000](http://localhost:3000)

## Struttura del Progetto

```
ecommerce-platform/
├── public/
│   └── index.html           # Template HTML
├── src/
│   ├── components/          # Componenti Riutilizzabili
│   │   ├── Header.jsx       # Navigazione e carrello
│   │   ├── ProductCard.jsx  # Card singolo prodotto
│   │   ├── ProductList.jsx  # Griglia prodotti con filtri
│   │   ├── ProductDetail.jsx # Dettagli prodotto completo
│   │   ├── Cart.jsx         # Carrello sidebar/pagina
│   │   ├── Checkout.jsx     # Form checkout completo
│   │   ├── LoginForm.jsx    # Form di login
│   │   ├── RegisterForm.jsx # Form di registrazione
│   │   └── AdminPanel.jsx   # Pannello amministrazione
│   ├── contexts/            # Context API
│   │   ├── CartContext.jsx  # Stato carrello
│   │   └── AuthContext.jsx  # Stato autenticazione
│   ├── pages/               # Pagine dell'applicazione
│   │   ├── Home.jsx         # Homepage
│   │   ├── Products.jsx     # Pagina catalogo
│   │   ├── ProductDetailPage.jsx
│   │   ├── CartPage.jsx
│   │   ├── CheckoutPage.jsx
│   │   ├── ProfilePage.jsx  # Profilo utente
│   │   ├── AdminPage.jsx
│   │   └── OrderConfirmationPage.jsx
│   ├── data/
│   │   └── products.js      # Dati prodotti sample
│   ├── App.jsx              # Componente principale con routing
│   ├── App.css              # Stili globali
│   ├── index.js             # Entry point
│   └── index.css
├── package.json
└── README.md
```

## Utilizzo

### Account Demo

Per accedere al pannello di amministrazione:
- **Email**: `admin@shop.com`
- **Password**: qualsiasi

### Funzionalità Utente

1. **Navigazione**: Esplora i prodotti per categoria o usa la ricerca
2. **Carrello**: Aggiungi prodotti, modifica quantità, procedi al checkout
3. **Checkout**: Compila i form di spedizione e pagamento
4. **Account**: Accedi per visualizzare il profilo e lo storico ordini

### Funzionalità Admin

1. **Dashboard**: Visualizza statistiche (prodotti, ordini, revenue)
2. **Gestione Prodotti**: Aggiungi, modifica, elimina prodotti
3. **Ordini**: Visualizza e gestisci gli ordini ricevuti

## Categorie Prodotti

- **Elettronica**: Smartphone, laptop, cuffie, fotocamere, tablet
- **Abbigliamento**: T-shirt, jeans, giacche, scarpe
- **Casa**: Sedie gaming, lampade, divani, tavoli
- **Accessori**: Zaini, borse, occhiali

## Tecnologie Utilizzate

| Tecnologia | Versione | Uso |
|-----------|----------|-----|
| React | 18.2.0 | UI Framework |
| React Router | 6.20.0 | Routing |
| React Scripts | 5.0.1 | Build Tool |

## Caratteristiche UI/UX

- **Design Moderno**: Gradienti, ombre, animazioni
- **Responsive**: Layout adattivo per tutti i dispositivi
- **Feedback Notifiche**: Conferme visive per azioni utente
- **Validazione Form**: Messaggi di errore in tempo reale
- **Loading States**: Spinner durante elaborazioni
- **Colori**: Palette viola/blu con accenti verdi e rossi

## Componenti Principali

### Header
- Logo e navigazione
- Barra di ricerca
- Icona carrello con badge
- Menu utente con dropdown

### ProductCard
- Immagine prodotto
- Categoria e nome
- Valutazione stelle
- Prezzo con sconto
- Badge stock/esaurito
- Pulsante aggiungi al carrello

### Cart
- Lista prodotti con quantità
- Calcolo subtotali
- Informazioni spedizione gratuita
- Pulsante checkout

### Checkout
- Form spedizione con validazione
- Form pagamento (simulato)
- Riepilogo ordine
- Conferma acquisto

### Admin Panel
- Dashboard con statistiche
- Tabella prodotti con azioni
- Lista ordini dettagliata
- Modal aggiunta/modifica prodotti

## Stato dell'Applicazione

### CartContext
- Gestione prodotti nel carrello
- localStorage per persistenza
- Calcolo totali
- Operazioni CRUD

### AuthContext
- Gestione stato autenticazione
- localStorage per sessione
- Simulazione login/register
- Salvataggio ordini

## Persistenza Dati

L'applicazione utilizza `localStorage` per:
- **Carrello**: Prodotti aggiunti
- **Utente**: Informazioni profilo
- **Ordini**: Storico acquisti

## Sviluppi Futuri

Possibili miglioramenti:
- [ ] Integrazione backend reale
- [ ] Pagamenti Stripe/PayPal
- [ ] Recensioni prodotti
- [ ] Lista desideri
- [ ] Confronto prodotti
- [ ] Filtri avanzati
- [ ] Tracking ordini
- [ ] Email notifications
- [ ] Multi-language support
- [ ] Dark mode

## Licenza

Questo progetto è stato creato a scopo educativo e dimostrativo.

## Autore

Progetto sviluppato come parte del portfolio di Web Development.

---

**Nota**: Questa è un'applicazione frontend-only. I dati sono salvati localmente nel browser e non persistono tra diversi dispositivi.

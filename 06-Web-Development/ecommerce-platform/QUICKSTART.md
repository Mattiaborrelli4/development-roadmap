# Quick Start Guide - ShopOnline

## Avvio Rapido

### 1. Installazione Dipendenze
```bash
npm install
```

### 2. Avvio Sviluppo
```bash
npm start
```

Applicazione disponibile su: **http://localhost:3000**

## Credenziali Admin

Per testare il pannello amministrazione:
- **Email**: `admin@shop.com`
- **Password**: (qualsiasi)

## Funzionalità Demo

### Utente Standard
1. Naviga tra i prodotti
2. Aggiungi al carrello
3. Procedi al checkout
4. Registrati per salvare l'ordine
5. Visualizza storico ordini nel profilo

### Amministratore
1. Login con email admin@shop.com
2. Accedi al pannello admin
3. Gestisci prodotti (aggiungi/modifica/elimina)
4. Visualizza ordini ricevuti

## Struttura Catalogo

- **18 prodotti** distribuiti in 4 categorie
- **Immagini** da Unsplash (placeholder)
- **Prezzi** da €39.99 a €1599.99
- **Sconti** applicati su vari prodotti

## Note Tecniche

- **Stato**: Gestito con Context API
- **Persistenza**: localStorage browser
- **Routing**: React Router v6
- **Styling**: CSS Modules
- **Responsive**: Mobile-first

## Browser Supportati

- Chrome/Edge (ultime 2 versioni)
- Firefox (ultime 2 versioni)
- Safari (ultime 2 versioni)

## Troubleshooting

### Porta 3000 già in uso
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Oppure usa un'altra porta
PORT=3001 npm start
```

### Cache problems
```bash
# Clear cache e reinstalla
rm -rf node_modules package-lock.json
npm install
```

## File Principali

- `src/App.jsx` - Routing e struttura
- `src/contexts/` - Gestione stato
- `src/pages/` - Pagine applicazione
- `src/components/` - Componenti UI
- `src/data/products.js` - Catalogo prodotti

## Supporto

Per problemi o domande, consulta il README.md principale.

# Guida Rapida - Shopping List App

## Installazione Rapida

### 1. Installa le dipendenze
```bash
cd "C:\Users\matti\Desktop\Project Ideas Portfolio\08-Mobile-Projects\shopping-list-app"
npm install
```

### 2. Avvia Expo
```bash
npm start
# oppure
expo start
```

### 3. Apri l'app
- **Android**: Premi `a` nel terminale
- **iOS**: Premi `i` nel terminale (solo Mac)
- **Web**: Premi `w` nel terminale
- **Dispositivo fisico**: Scannerizza il QR code con l'app Expo Go

## Funzionalità Principali

### ✅ Cosa puoi fare:
1. **Creare liste** - Multiple liste per diversi scopi
2. **Aggiungere elementi** - Con nome, quantità, categoria, note
3. **Scannerizzare barcode** - Usa la camera per scansionare prodotti
4. **Segnare acquisti** - Segna elementi come comprati
5. **Condividere liste** - Simula la condivisione con familiari
6. **Filtrare elementi** - Per categoria, stato, o ricerca

### 📱 Struttura App
- **Schermata Liste**: Tutte le tue liste
- **Dettaglio Lista**: Elementi della lista specifica
- **Impostazioni**: Preferenze e statistiche

### 🎨 Categorie Disponibili
- 🥬 Ortofrutta
- 🥛 Latticini
- 🥩 Carne
- 🍞 Panificio
- 🧊 Surgeleti
- 🥫 Dispensa
- 🍷 Bevande
- 🧹 Casa
- 📦 Altro

### 📊 Codici Barcode di Test
Usa questi codici per testare lo scanner:
- `8001234567890` - Latte interno 1L
- `8001234567891` - Pane integrale
- `8001234567892` - Uova 12pz
- `8001234567893` - Pasta 500g
- `8001234567894` - Acqua 1.5L
- `8001234567895` - Formaggio grattugiato
- `8001234567896` - Pollo 1kg
- `8001234567897` - Pomodori 1kg
- `8001234567898` - Detersivo piatti
- `8001234567899` - Gelato vaniglia

## Componenti Principali

### Schermate
- `ListsScreen.jsx` - Overview delle liste
- `ListDetailScreen.jsx` - Dettaglio e gestione elementi
- `SettingsScreen.jsx` - Impostazioni e statistiche

### Componenti UI
- `ListItem.jsx` - Card elemento con azioni
- `AddItemModal.jsx` - Modal per aggiungere/modificare
- `CategoryBadge.jsx` - Badge categoria colorato
- `ShareButton.jsx` - Pulsante condivisione lista
- `BarcodeScanner.jsx` - Scanner codici a barre

### Servizi
- `storageService.js` - Gestione AsyncStorage
- `syncService.js` - Sincronizzazione simulata

### Hooks
- `useLists.js` - Hook per gestire le liste
- `useItems.js` - Hook per gestire gli elementi

## Risoluzione Problemi

### L'app non si avvia
```bash
# Cancella cache e reinstalla
rm -rf node_modules
npm install
expo start --clear
```

### La camera non funziona
- Assicurati di aver dato il permesso della camera
- Su emulatore, verifica che la camera sia supportata
- Usa il mode "Manuale" per inserire codici manualmente

### Errore di navigazione
- Riavvia il server Expo
- Cancella la cache dell'app

## Tecnologie Utilizzate

- **React Native** - Framework mobile
- **Expo** - Platform di sviluppo
- **React Navigation** - Navigazione
- **AsyncStorage** - Persistenza dati
- **Expo Camera** - Accesso camera
- **Gesture Handler** - Gesture e interazioni

## Note di Sviluppo

- I dati sono salvati localmente in AsyncStorage
- La sincronizzazione è simulata per dimostrazione
- Lo scanner barcode supporta EAN-13, EAN-8, UPC-A, Code 128
- L'interfaccia è responsive per diverse dimensioni schermo

## Supporto

Per problemi o domande, consulta il README.md principale.

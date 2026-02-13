# 🛒 Lista della Spesa

Applicazione mobile React Native per gestire le liste della spesa condivise con la famiglia.

## 📋 Caratteristiche

### Funzionalità Principali
- ✅ **Multiple Liste della Spesa** - Crea e gestisci diverse liste (Spesa settimanale, Casa, Ufficio, ecc.)
- ➕ **Aggiungi/Rimuovi Elementi** - Gestisci facilmente gli elementi delle tue liste
- ✔️ **Segna come Acquistato** - Segna gli elementi come comprati con animazioni
- 📂 **Categorie** - Organizza gli elementi per categoria (Ortofrutta, Latticini, Carne, ecc.)
- 👥 **Condivisione Familiare** - Condividi le liste con i membri della famiglia (simulato)
- 🔄 **Sincronizzazione** - Sincronizzazione in tempo reale (simulata con AsyncStorage)

### Funzionalità Avanzate
- 📊 **Scanner Barcode** - Scansiona i codici a barre dei prodotti (simulato/Expo Camera)
- 🔢 **Quantità e Note** - Aggiungi quantità e annotazioni agli elementi
- 🎯 **Filtri e Ricerca** - Filtra per categoria, stato di acquisto o cerca per nome
- 📈 **Statistiche** - Visualizza le statistiche delle liste (percentuale di completamento)
- 🌙 **Tema Chiaro/Scuro** - Passa tra tema chiaro e scuro
- ⚡ **Animazioni Fluide** - Animazioni fluide con React Native Reanimated

### Interfaccia Utente
- 🎨 **Design Moderno** - Interfaccia pulita e intuitiva
- 👆 **Swipe Actions** - Scorri per segnare come comprato o eliminare
- 🔍 **Pull to Refresh** - Aggiorna le liste tirando verso il basso
- 📊 **Barra di Progresso** - Visualizza il progresso della lista
- 🏷️ **Badge Categorie** - Icone colorate per ogni categoria

## 🛠️ Stack Tecnologico

### Core
- **React Native** - Framework mobile
- **Expo** - Piattaforma di sviluppo
- **React Navigation** - Navigazione tra schermate
- **AsyncStorage** - Persistenza dati locale

### UI e Animazioni
- **React Native Gesture Handler** - Gesture e swipe
- **React Native Reanimated** - Animazioni avanzate
- **React Native Safe Area Context** - Gestione area sicura

### Altre Librerie
- **Expo Camera** - Accesso alla fotocamera per scanner barcode
- **Expo Barcode Scanner** - Lettura codici a barre
- **Vector Icons** - Icone vettoriali

## 📁 Struttura del Progetto

```
shopping-list-app/
├── App.js                          # Entry point principale
├── app.json                        # Configurazione Expo
├── package.json                    # Dipendenze
├── src/
│   ├── components/                 # Componenti riutilizzabili
│   │   ├── ListItem.jsx           # Card elemento lista
│   │   ├── AddItemModal.jsx       # Modal aggiunta elemento
│   │   ├── CategoryBadge.jsx      # Badge categoria
│   │   ├── ShareButton.jsx        # Pulsante condivisione
│   │   └── BarcodeScanner.jsx     # Scanner barcode
│   ├── screens/                   # Schermate dell'app
│   │   ├── ListsScreen.jsx        # Schermata liste
│   │   ├── ListDetailScreen.jsx   # Dettaglio lista
│   │   └── SettingsScreen.jsx     # Impostazioni
│   ├── services/                  # Servizi e logica di business
│   │   ├── storageService.js      # Gestione AsyncStorage
│   │   └── syncService.js         # Sincronizzazione (simulata)
│   ├── hooks/                     # Custom React Hooks
│   │   ├── useLists.js           # Hook per le liste
│   │   └── useItems.js           # Hook per gli elementi
│   ├── utils/                     # Utility e costanti
│   │   └── constants.js          # Costanti dell'app
│   └── styles/                    # Stili
│       └── theme.js              # Tema dell'app
└── README.md                      # Documentazione
```

## 🗄️ Strutture Dati

### Lista della Spesa
```javascript
{
  id: string,              // ID univoco
  name: string,           // Nome lista
  icon: string,           // Emoji icona
  color: string,          // Colore tema
  shared: boolean,        // Se è condivisa
  owner: string,          // Proprietario
  sharedWith: array,      // Utenti condivisi
  createdAt: timestamp    // Data creazione
}
```

### Elemento Lista
```javascript
{
  id: string,             // ID univoco
  listId: string,         // ID lista padre
  name: string,           // Nome prodotto
  quantity: number,       // Quantità
  category: string,       // Categoria
  bought: boolean,        // Se acquistato
  notes: string,          // Note
  barcode: string,        // Codice a barre
  createdAt: timestamp    // Data creazione
}
```

### Categorie
- 🥬 Ortofrutta
- 🥛 Latticini
- 🥩 Carne
- 🍞 Panificio
- 🧊 Surgeleti
- 🥫 Dispensa
- 🍷 Bevande
- 🧹 Casa
- 📦 Altro

## 🚀 Installazione e Avvio

### Prerequisiti
- Node.js (v16 o superiore)
- npm o yarn
- Expo CLI
- Android Studio / Xcode (per build native)
- Dispositivo mobile o emulatore

### Passaggi

1. **Naviga nella directory del progetto**
```bash
cd "C:\Users\matti\Desktop\Project Ideas Portfolio\08-Mobile-Projects\shopping-list-app"
```

2. **Installa le dipendenze**
```bash
npm install
# oppure
yarn install
```

3. **Avvia il server di sviluppo**
```bash
npm start
# oppure
yarn start
# oppure
expo start
```

4. **Apri l'app**
- Premi `a` per Android
- Premi `i` per iOS
- Premi `w` per web
- Scannerizza il QR code con Expo Go sul tuo dispositivo

## 📖 Come Usare

### Creare una Nuova Lista
1. Tocca il pulsante "+ Nuova" o il FAB (floating action button)
2. Inserisci il nome della lista
3. Scegli un'icona e un colore
4. Tocca "Crea Lista"

### Aggiungere Elementi
1. Apri una lista
2. Tocca il pulsante "+" (FAB)
3. Inserisci nome, quantità, categoria e note
4. Tocca "Aggiungi"

### Scannerizzare Barcode
1. In una lista, tocca "📊 Scanner"
2. Allinea il codice a barre nel riquadro
3. L'app riempirà automaticamente i dettagli del prodotto
4. Inserisci manualmente se non riconosciuto

### Segnare come Comprato
- Scorri verso destra su un elemento per segnarlo come comprato
- Scorri verso sinistra per eliminarlo
- Tocca il checkbox accanto all'elemento

### Condividere una Lista
1. Apri il dettaglio lista
2. Tocca "Condividi"
3. Inserisci l'email del familiare
4. Tocca "Invita"

### Filtrare Elementi
- Usa i filtri in alto per vedere: Tutti, Da Comprare, Comprati
- Filtra per categoria toccando il badge della categoria
- Usa la barra di ricerca per cercare elementi

## 🎨 Personalizzazione

### Temi
L'app supporta temi chiaro e scuro. Puoi cambiarlo dalle Impostazioni.

### Colori Liste
Ogni lista ha un colore personalizzabile scegliendo tra:
- Rosso, Verde, Blu, Giallo
- Ciano, Viola, Arancione, Azzurro

### Icone Liste
Scegli tra emoji popolari per personalizzare le tue liste.

## 🔧 Configurazione

### Permessi Camera
Per lo scanner barcode, l'app richiede il permesso della camera. I permessi sono gestiti automaticamente da Expo.

### Persistenza Dati
I dati sono salvati localmente usando AsyncStorage. La sincronizzazione è simulata per dimostrazione.

### Codici Barcode di Test
L'app include un database simulato con questi codici di prova:
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

## 🐛 Troubleshooting

### Problemi comuni

**L'app non si avvia**
- Assicurati di avere tutte le dipendenze installate
- Prova a cancellare `node_modules` e reinstallare

**La camera non funziona**
- Verifica i permessi della camera nelle impostazioni del dispositivo
- Su emulatore Android, assicurati che la camera sia supportata

**Lo scanner non rileva i codici**
- Assicurati di avere buona luce
- Tieni il dispositivo stabile
- Prova con il input manuale

## 🚀 Sviluppi Futuri

### Funzionalità Previste
- [ ] Sincronizzazione reale con backend (Firebase/Supabase)
- [ ] Autenticazione utenti
- [ ] Notifiche push per aggiornamenti lista
- [ ] Storie/ricette consigliate basate sulla lista
- [ ] Confronto prezzi tra supermercati
- [ ] Sconti e offerte personalizzate
- [ ] Lista delle spese storiche
- [ ] Budget e statistiche avanzate

### Miglioramenti UI/UX
- [ ] Dark mode completo
- [ ] Widget home screen
- [ ] Apple Watch / Wear OS companion
- [ ] Drag & drop per riordinare elementi
- [ ] Quick actions da notifica

## 📄 Licenza

Questo progetto è stato creato a scopo educativo e dimostrativo.

## 👨‍💻 Sviluppatore

App creata come progetto portfolio per dimostrare competenze in:
- React Native
- Expo
- State Management
- Navigation
- Gestione permessi
- AsyncStorage
- Animazioni
- Gestione camera/barcode

---

**Creato con ❤️ usando React Native ed Expo**

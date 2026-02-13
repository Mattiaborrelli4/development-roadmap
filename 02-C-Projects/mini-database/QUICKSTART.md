# 🚀 Quick Start - Mini Database Engine

## Avvio Rapido (5 minuti)

### 1. Compilazione

```bash
cd mini-database

# Con Makefile (raccomandato)
make

# Oppure manualmente
gcc -Wall -Wextra -std=c99 -O2 -o minidb main.c database.c
```

### 2. Prima Esecuzione

```bash
# Avvio normale
./minidb

# Su Windows
minidb.exe
```

### 3. Comandi Base

```
db> SET nome Mario
db> GET nome
db> LIST
db> SAVE
db> EXIT
```

## 📖 Cheat Sheet

### CRUD Operations
```
SET <key> <value>     Crea/Aggiorna
GET <key>             Leggi
DELETE <key>          Cancella
LIST                  Mostra tutto
```

### File Operations
```
SAVE [file]           Salva (default: database.db)
LOAD [file]           Carica (default: database.db)
```

### Utility
```
INFO                  Statistiche
HELP                  Aiuto
CLEAR                 Pulisci schermo
EXIT                  Esci (salva auto)
```

## 🎯 Esempi Pratici

### Rubrica
```
db> SET mario "Mario Rossi, 3331234567"
db> SET luigi "Luigi Verdi, 3339876543"
db> GET mario
db> LIST
```

### Configurazione
```
db> SET host localhost
db> SET port 8080
db> SET debug true
db> SAVE config.db
```

### Shopping List
```
db> SET item1 "Latte"
db> SET item2 "Pane"
db> SET item3 "Uova"
db> LIST
```

## 🔧 Risoluzione Problemi

### Errore: Comando non riconosciuto
```
Controlla l'ortografia
Usa HELP per vedere i comandi
```

### Errore: Chiave non trovata
```
Controlla con LIST
La chiave è case-sensitive!
```

### Errore: File non trovato
```
Il file non esiste ancora
Usa SAVE per crearlo
```

## 📚 Doc Completa

- `README.md` - Guida completa in Italiano
- `ARCHITECTURE.md` - Documentazione tecnica
- `FEATURES.md` - Lista funzionalità
- `example_session.txt` - Esempi avanzati

## ✨ Consigli

1. **Salva spesso**: Usa SAVE dopo modifiche importanti
2. **Backups**: Usa SAVE con nomi diversi
3. **Auto-save**: EXIT salva automaticamente
4. **Debug**: Usa INFO per vedere statistiche

---

**Buon divertimento! 🎉**

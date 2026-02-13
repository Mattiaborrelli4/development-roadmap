# 📚 Mini Database Engine - Indice Completo

## 🎯 Benvenuto

Benvenuto nel **Mini Database Engine**, un database key-value completo scritto in puro C con hash table per l'indicizzazione e persistenza su file binario.

## 🚀 Come Iniziare

### Per Principianti Assoluti
1. Leggi **[QUICKSTART.md](QUICKSTART.md)** - 5 minuti per iniziare
2. Compila ed esegui i comandi di esempio
3. Esplora **[example_session.txt](example_session.txt)** per vedere esempi reali

### Per Utenti Esperti
1. Leggi **[README.md](README.md)** per la documentazione completa
2. Guarda **[ARCHITECTURE.md](ARCHITECTURE.md)** per i dettagli tecnici
3. Vedi **[FEATURES.md](FEATURES.md)** per la lista completa delle funzionalità

### Per Sviluppatori
1. Studia **[ARCHITECTURE.md](ARCHITECTURE.md)** per capire l'implementazione
2. Leggi i sorgenti: `database.h`, `database.c`, `main.c`
3. Usa **[test.sh](test.sh)** o **[test.bat](test.bat)** per i test

## 📖 Documentazione

### Guide Utente
- **[README.md](README.md)** - Guida completa in italiano (🇮🇹)
  - Installazione e compilazione
  - Tutti i comandi con esempi
  - Casi d'uso pratici
  - Limitazioni e note di sicurezza

- **[QUICKSTART.md](QUICKSTART.md)** - Guida rapida (5 minuti)
  - Avvio immediato
  - Comandi essenziali
  - Esempi pratici
  - Troubleshooting

- **[example_session.txt](example_session.txt)** - Esempi di sessione
  - Sessioni complete annotate
  - Scenari di testing
  - Comandi per automatizzare i test

### Documentazione Tecnica
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Documentazione architetturale
  - Strutture dati
  - Algoritmi (hash, collision handling)
  - Formato file binario
  - Complessità algoritmica
  - Diagrammi e ASCII art

- **[FEATURES.md](FEATURES.md)** - Lista funzionalità
  - Funzionalità implementate
  - Roadmap futura
  - Specifiche tecniche
  - Metriche di qualità
  - Casi d'uso

- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Riepilogo progetto
  - Statistiche codice
  - Obiettivi raggiunti
  - Metriche qualità
  - Prossimi passi

### Visuali
- **[DIAGRAM.txt](DIAGRAM.txt)** - Diagrammi ASCII art
  - Architettura del sistema
  - Struttura dati
  - Flusso comandi
  - Esempi d'uso

## 💻 Codice Sorgente

### File Principali
- **[database.h](database.h)** (42 righe)
  - Definizioni strutture dati
  - Costanti globali
  - Prototipi funzioni

- **[database.c](database.c)** (283 righe)
  - Implementazione hash table
  - Operazioni CRUD
  - Persistenza file
  - Funzioni utility

- **[main.c](main.c)** (223 righe)
  - CLI interattivo
  - Parser comandi
  - Loop principale
  - Auto save/load

### Build System
- **[Makefile](Makefile)** - Automazione build (Unix)
- **[test.sh](test.sh)** - Test script Unix/Linux/macOS
- **[test.bat](test.bat)** - Test script Windows

### Altro
- **[.gitignore](.gitignore)** - Regole per Git

## 📊 Statistiche Progetto

| Metrica | Valore |
|---------|--------|
| **Linguaggio** | C (ANSI C99) |
| **File totali** | 14 |
| **Codice sorgente** | 548 righe |
| **Documentazione** | ~40 KB |
| **Executable** | 67 KB |
| **Dipendenze** | Zero |
| **Portabilità** | 100% (C99 standard) |

## 🎯 Percorsi di Apprendimento

### Path 1: Utente Base
```
QUICKSTART.md → README.md → Esegui i comandi → Esperimenti
```

### Path 2: Sviluppatore
```
README.md → ARCHITECTURE.md → Codice sorgente → Modifiche
```

### Path 3: Studio Approfondito
```
DIAGRAM.txt → ARCHITECTURE.md → FEATURES.md → Codice → Test
```

## 🔧 Quick Reference

### Compilazione
```bash
# Unix/Linux/macOS
make

# Windows (MinGW)
gcc -o minidb.exe main.c database.c
```

### Esecuzione
```bash
# Unix/Linux/macOS
./minidb

# Windows
minidb.exe
```

### Comandi Base
```
SET key value    - Salva valore
GET key          - Recupera valore
DELETE key       - Cancella chiave
LIST             - Mostra tutti
SAVE [file]      - Salva su file
LOAD [file]      - Carica da file
EXIT             - Esci (salva auto)
```

## 📚 Risorse Esterne

### Per Imparare C
- "C Programming Language" - Kernighan & Ritchie
- LearnCpp.com
- C Programming on GeeksforGeeks

### Per Data Structures
- "Introduction to Algorithms" - CLRS
- Hash Tables su Wikipedia
- Visualizing Algorithms

### Per Database
- "Database System Concepts" - Silberschatz
- SQLite Documentation
- Designing Data-Intensive Applications

## 🏆 Obiettivi del Progetto

Questo progetto dimostra competenza in:
- ✅ Programmazione C
- ✅ Strutture dati (hash tables)
- ✅ Gestione memoria
- ✅ File I/O binario
- ✅ CLI development
- ✅ Software design modulare
- ✅ Documentazione tecnica
- ✅ Testing e QA

## 🤝 Contribuire

Se vuoi migliorare il progetto:
1. Leggi **[FEATURES.md](FEATURES.md)** per idee
2. Studia **[ARCHITECTURE.md](ARCHITECTURE.md)**
3. Implementa la feature
4. Aggiungi test in **[test.sh](test.sh)** o **[test.bat](test.bat)**
5. Aggiorna la documentazione

## 📞 Supporto

- Domande? Vedi **[README.md](README.md)** - Sezione FAQ
- Problemi? Controlla **[QUICKSTART.md](QUICKSTART.md)** - Troubleshooting
- Bug? Segnala con dettagli

## 📝 Note Legali

Questo progetto è creato a scopo educativo. Libero utilizzo e modifica.

---

**Versione**: 1.0
**Data**: Febbraio 2026
**Autore**: Progetto Portfolio C
**Lingua**: Italiano 🇮🇹

**Buon coding! 🚀**

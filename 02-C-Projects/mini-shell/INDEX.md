# 📚 Mini Shell - Indice della Documentazione

Benvenuto in Mini Shell! Questo indice ti aiuterà a navigare tutta la documentazione del progetto.

## 🚀 Guide Rapide

### 📖 [QUICKSTART.md](QUICKSTART.md)
**Per chi:** Principianti assoluti
**Contenuto:**
- Compilazione rapida
- Comandi essenziali
- Esempio rapido
- Troubleshooting base

**Tempo di lettura:** 3 minuti

---

## 📋 Documentazione Principale

### 📖 [README.md](README.md)
**Per chi:** Tutti gli utenti
**Contenuto:**
- Caratteristiche complete
- Requisiti di sistema
- Guida compilazione dettagliata
- Tutti i comandi supportati
- Architettura del progetto
- Limitazioni conosciute
- Estensioni future

**Tempo di lettura:** 10 minuti

### 📖 [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
**Per chi:** Sviluppatori e revisori
**Contenuto:**
- Panoramica tecnica completa
- Metriche del codice
- System calls utilizzate
- Architettura dettagliata
- Obiettivi educativi
- Risultati finali

**Tempo di lettura:** 8 minuti

---

## 🔧 Guide Tecniche

### 📖 [INSTALLAZIONE.md](INSTALLAZIONE.md)
**Per chi:** Chi vuole installare/compilare
**Contenuto:**
- Requisiti sistema dettagliati
- Installazione GCC per ogni piattaforma
- Metodi di compilazione
- Debug e ottimizzazione
- Risoluzione problemi completa
- Integrazione editor

**Tempo di lettura:** 15 minuti

### 📖 [EXAMPLES.md](EXAMPLES.md)
**Per chi:** Chi vuole imparare usando esempi
**Contenuto:**
- 14+ esempi pratici
- Navigazione file system
- Esecuzione programmi
- Gestione processi
- Scripting
- Confronto con Bash
- Tips e tricks

**Tempo di lettura:** 12 minuti

---

## 💻 Codice Sorgente

### [shell.h](shell.h) - 92 righe
**Header file** con:
- Definizioni costanti
- Struttura `History`
- Prototipi di tutte le funzioni
- Macro per compatibilità Windows/Unix

### [shell.c](shell.c) - 607 righe
**Implementazione principale** con:
- 25+ funzioni C
- Parser comandi
- Built-in commands
- Esecuzione programmi esterni
- Gestione segnali
- Gestione history
- Commenti estensivi in italiano

### [test_shell.c](test_shell.c) - 259 righe
**Suite di test** con:
- 12 test unitari
- Test parser
- Test built-in
- Test history
- Test gestione errori

---

## 🔨 Build e Automation

### Makefile
Per Linux/Unix/macOS:
```bash
make          # Compila
make run      # Compila ed esegui
make clean    # Pulisce
make test     # Esegue test suite
make install  # Installa in /usr/local/bin
```

### Makefile.test
Per test suite:
```bash
make -f Makefile.test
make -f Makefile.test test
```

### build.bat
Script build Windows:
```cmd
build.bat
```

### demo.sh / demo.bat
Script demo interattiva per testare la shell.

---

## 📁 Struttura Progetto

```
mini-shell/
│
├── 📄 Documentazione
│   ├── README.md              # Documentazione principale
│   ├── QUICKSTART.md          # Guida rapida
│   ├── PROJECT_SUMMARY.md     # Sommario tecnico
│   ├── INSTALLAZIONE.md       # Guida installazione
│   ├── EXAMPLES.md            # Esempi d'uso
│   └── INDEX.md               # Questo file
│
├── 💻 Codice Sorgente
│   ├── shell.h                # Header (92 righe)
│   ├── shell.c                # Implementazione (607 righe)
│   └── test_shell.c           # Test suite (259 righe)
│
├── 🔨 Build e Automation
│   ├── Makefile               # Build Unix/Linux
│   ├── Makefile.test          # Build test
│   ├── build.bat              # Build Windows
│   ├── demo.sh                # Demo Unix/Linux
│   └── demo.bat               # Demo Windows
│
└── 🗑️ Altro
    ├── .gitignore             # File da ignorare
    └── mini-shell.exe         # Eseguibile compilato
```

---

## 🎯 Percorsi di Apprendimento

### 👶 Principiante Assoluto
1. Leggi [QUICKSTART.md](QUICKSTART.md)
2. Compila ed esegui
3. Prova i comandi base
4. Leggi [README.md](README.md) sezione comandi

### 🎓 Studente
1. Leggi [README.md](README.md) completo
2. Studia [shell.h](shell.h) per le strutture dati
3. Leggi [shell.c](shell.c) con attenzione ai commenti
4. Prova [EXAMPLES.md](EXAMPLES.md)
5. Esegui test suite

### 👨‍💻 Sviluppatore
1. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) per overview
2. Leggi [INSTALLAZIONE.md](INSTALLAZIONE.md) per dettagli tecnici
3. Studia codice sorgente completo
4. Analizza test suite
5. Considera estensioni future

### 🔬 Ricercatore/Revisore
1. Leggi tutto in ordine
2. Analizza metriche in [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
3. Studia implementazione [shell.c](shell.c)
4. Verifica test coverage
5. Valuta architettura

---

## ⚡ Quick Reference

### Compilazione
```bash
# Linux/macOS
make

# Windows
build.bat
# o
gcc -Wall -Wextra -std=c99 -o mini-shell.exe shell.c
```

### Esecuzione
```bash
# Linux/macOS
./mini-shell

# Windows
mini-shell.exe
```

### Comandi Base
```
help        - Mostra aiuto
pwd         - Directory corrente
cd <path>   - Cambia directory
ls          - Lista file
echo <txt>  - Stampa testo
clear       - Pulisci schermo
history     - Mostra cronologia
exit        - Esci
```

---

## 📊 Statistiche Progetto

- **Linguaggio:** C (C99)
- **Piattaforme:** Windows, Linux, macOS
- **Righe codice:** 958 totali
  - shell.c: 607 righe
  - shell.h: 92 righe
  - test_shell.c: 259 righe
- **File totali:** 14
- **Documentazione:** 6 file markdown
- **Test:** 12 unitari
- **Built-in commands:** 8
- **Compatibilità:** 100% cross-platform

---

## 🆘 Problemi?

1. **Compilatione fallita** → Vedi [INSTALLAZIONE.md](INSTALLAZIONE.md) sezione "Risoluzione Problemi"
2. **Comando non funziona** → Vedi [README.md](README.md) sezione "Troubleshooting"
3. **Non sai come usare** → Vedi [QUICKSTART.md](QUICKSTART.md)
4. **Vuoi esempi** → Vedi [EXAMPLES.md](EXAMPLES.md)
5. **Dettagli tecnici** → Vedi [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

---

## 🎓 Risorse Esterne

Per approfondire:
- **C Programming:** K&R "The C Programming Language"
- **System Calls:** "Advanced Programming in the UNIX Environment"
- **OS Concepts:** "Operating System Concepts" (Silberschatz)
- **POSIX:** https://pubs.opengroup.org/onlinepubs/9699919799/

---

## 📝 Changelog

### Versione 1.0 (12 Febbraio 2026)
- ✅ Release iniziale
- ✅ 8 comandi built-in
- ✅ History con persistenza
- ✅ Cross-platform (Windows/Linux/macOS)
- ✅ Test suite completa
- ✅ Documentazione in italiano

---

## 🤝 Contributi

Questo è un progetto educativo. Sentiti libero di:
- Studiare il codice
- Proporre miglioramenti
- Aggiungere funzionalità
- Segnalare bug

---

**Buon divertimento con Mini Shell!** 🐚

*Creato con ❤️ per la comunità Open Source*

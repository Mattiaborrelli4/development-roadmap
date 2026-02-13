# 📁 File Manager - Gestione File in C

## 📋 Descrizione

Un **File Manager interattivo** scritto in puro linguaggio C per la gestione dei file system. Questo progetto dimostra competenze di system programming attraverso l'utilizzo di system call Unix/Linux per la manipolazione di file e directory.

### ✨ Caratteristiche Principali

- **Interfaccia interattiva** a menu con colori
- **Lista file** nella directory corrente con dettagli
- **Copia file** con buffer ottimizzato
- **Sposta/Rinomina file** in una singola operazione
- **Elimina file** con conferma di sicurezza
- **Visualizza informazioni** dettagliate sui file
- **Gestione errori** robusta con messaggi chiari

---

## 🛠️ Tecnologie Utilizzate

- **Linguaggio**: C (ANSI C99)
- **System Call**: POSIX (Linux/Unix)
- **Librerie**: `stdio.h`, `stdlib.h`, `string.h`, `dirent.h`, `sys/stat.h`, `unistd.h`

---

## 📦 Installazione e Compilazione

### Prerequisiti

Assicurati di avere installato un compilatore C:
```bash
# Ubuntu/Debian
sudo apt-get install build-essential

# Fedora/RHEL
sudo dnf install gcc

# macOS
xcode-select --install
```

### Compilazione

#### Metodo 1: Usando Makefile (Consigliato)
```bash
# Compila il progetto
make

# Compila ed esegui
make run

# Pulisci i file compilati
make clean
```

#### Metodo 2: Compilazione Manuale
```bash
gcc -Wall -Wextra -std=c99 -pedantic file_manager.c -o file_manager
```

### Installazione Globale (Opzionale)
```bash
# Installa in /usr/local/bin
sudo make install

# Disinstalla
sudo make uninstall
```

---

## 🚀 Utilizzo

### Avvio del Programma

```bash
./file_manager
```

### Menu Principale

```
╔══════════════════════════════════════════════════════╗
║           FILE MANAGER - Menu Principale           ║
╠══════════════════════════════════════════════════════╣
║  1. Lista file nella directory corrente              ║
║  2. Copia file                                       ║
║  3. Sposta/Rinomina file                             ║
║  4. Elimina file                                     ║
║  5. Visualizza informazioni file                     ║
║  0. Esci                                             ║
╚══════════════════════════════════════════════════════╝
```

### Esempi di Utilizzo

#### 1. Listare i File
```
Scelta: 1

╔══════════════════════════════════════════════╗
║          CONTENUTO DIRECTORY CORRENTE         ║
╚══════════════════════════════════════════════╝

NOME                           TIPO            DIMENSIONE
────────────────────────────────────────────────────────
file_manager.c                 FILE          8.45 KB
file_manager                   DIR            -
README.md                      FILE          4.21 KB
────────────────────────────────────────────────────────
Totale elementi: 3
```

#### 2. Copiare un File
```
Scelta: 2

--- COPIA FILE ---
Nome file sorgente: file_manager.c
Nome file destinazione: backup.c

✓ File copiato con successo: 'file_manager.c' -> 'backup.c'
```

#### 3. Spostare/Rinominare
```
Scelta: 3

--- SPOSTA/RINOMINA FILE ---
Nome file sorgente: vecchio_nome.txt
Nuovo nome/destinazione: nuovo_nome.txt

✓ File spostato/rinominato con successo: 'vecchio_nome.txt' -> 'nuovo_nome.txt'
```

#### 4. Eliminare un File
```
Scelta: 4

--- ELIMINA FILE ---
Nome file da eliminare: temp.txt
Sei sicuro di voler eliminare 'temp.txt'? (s/n): s

✓ File eliminato con successo: 'temp.txt'
```

#### 5. Visualizzare Informazioni
```
Scelta: 5

--- INFORMAZIONI FILE ---
Nome file: documento.txt

╔══════════════════════════════════════════════╗
║        INFORMAZIONI FILE                       ║
╚══════════════════════════════════════════════╝

Nome:              documento.txt
Tipo:              File
Dimensione:        2048 bytes
                   (2.00 KB)
Permessi:          rw-r--r--
```

---

## 🔧 Funzionalità Tecniche

### System Call Utilizzate

| Funzione | Descrizione |
|----------|-------------|
| `opendir()` / `readdir()` | Lettura directory |
| `stat()` | Informazioni file |
| `fopen()` / `fread()` / `fwrite()` | Operazioni I/O |
| `rename()` | Spostamento/Rinomina |
| `unlink()` | Eliminazione file |
| `getcwd()` | Directory corrente |

### Gestione degli Errori

Il programma implementa una gestione errori robusta:
- Verifica esistenza file prima delle operazioni
- Controllo permessi e tipi (file vs directory)
- Messaggi di errore descrittivi
- Conferma per operazioni distruttive

### Caratteristiche Avanzate

- **Colori terminali ANSI**: Migliora l'esperienza utente
- **Buffer ottimizzato**: 4KB per operazioni di copia
- **Conversione dimensioni**: Formattazione automatica (B/KB/MB)
- **Input sanitization**: Pulizia buffer input

---

## 📂 Struttura del Progetto

```
file-manager/
├── file_manager.c      # Codice sorgente principale
├── Makefile           # File di build automation
└── README.md          # Documentazione
```

---

## 🎯 Concetti di System Programming

### File System Operations

Il programma implementa operazioni fondamentali del file system:

1. **Navigazione Directory**
   - Lettura contenuti directory
   - Filtraggio entry speciali (`.` e `..`)

2. **Metadata File**
   - Statistiche file tramite `stat()`
   - Permessi e tipi di file
   - Dimensioni e timestamp

3. **Operazioni I/O**
   - Lettura/scrittura bufferizzata
   - Gestione errori I/O
   - Copy-on-write efficiente

### Gestione Processo

- Fork ed exec (non implementato in questa versione)
- Signal handling (potenziale espansione)
- Environment variables

---

## 🐛 Risoluzione Problemi

### Errori Comuni

#### "Permission denied"
```bash
# Soluzione: Assicurati di avere i permessi
chmod +x file_manager
```

#### "File non trovato"
```bash
# Soluzione: Verifica il path
ls -la
pwd
```

#### Compilazione fallita
```bash
# Soluzione: Verifica installazione gcc
gcc --version

# Installa se necessario
sudo apt-get install build-essential
```

---

## 🔄 Comandi Makefile

| Comando | Descrizione |
|---------|-------------|
| `make` / `make all` | Compila il progetto |
| `make run` | Compila ed esegue |
| `make clean` | Rimuove file compilati |
| `make install` | Installa globalmente |
| `make uninstall` | Rimuove installazione globale |
| `make help` | Mostra aiuto comandi |

---

## 🎓 Obiettivi Educativi

Questo progetto è stato creato per dimostrare:

1. **Conoscenza System Call Unix**
   - API POSIX per gestione file
   - File descriptor e I/O operations

2. **Gestione Memoria in C**
   - Allocazione buffer
   - Gestione stringhe

3. **Error Handling**
   - Verifica return values
   - Messaggi errore informativi

4. **User Experience**
   - Interfaccia interattiva
   - Feedback visivo (colori)

---

## 🚧 Possibili Espansioni

- [ ] Supporto directory ricorsivo
- [ ] Compressione file (gzip)
- [ ] Search per nome/pattern
- [ ] Modifica permessi (chmod)
- [ ] Visualizzazione hex dump
- [ ] File comparison (diff)
- [ ] Batch operations
- [ ] Configurazione file

---

## 📝 Note di Sviluppo

### Compatibilità

- **Linux**: ✅ Completamente compatibile
- **macOS**: ✅ Completamente compatibile
- **Windows**: ⚠️ Richiede WSL o MinGW

### Standard

- Linguaggio: **C99**
- API: **POSIX.1-2008**

---

## 👤 Autore

**Creato per**: Portfolio Project Ideas
**Linguaggio**: C
**Categoria**: System Programming

---

## 📄 Licenza

Questo progetto è stato creato a scopo educativo e dimostrativo.

---

## 🙏 Ringraziamenti

- Guida POSIX System Programming
- The C Programming Language (K&R)
- Linux man pages

---

**Buon coding! 🚀**

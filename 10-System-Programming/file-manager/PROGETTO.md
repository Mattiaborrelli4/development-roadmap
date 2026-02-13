# 📁 File Manager - Panoramica Progetto

## 🎯 Obiettivo del Progetto

Creare un **File Manager interattivo in C** che dimostri competenze di System Programming attraverso l'utilizzo di system call POSIX per la manipolazione di file e directory.

---

## 📂 Struttura Completa del Progetto

```
file-manager/
│
├── 📄 file_manager.c          (14.4 KB)
│   └── Codice sorgente principale con tutte le funzionalità
│
├── 🔧 Makefile                (1.7 KB)
│   └── Automazione build con target multipli
│
├── 🚀 build.sh                (1.8 KB)
│   └── Script di compilazione alternativo
│
├── 📖 README.md               (8.9 KB)
│   └── Documentazione completa del progetto
│
├── 🏗️ ARCHITETTURA.md         (9.8 KB)
│   └── Diagrammi e dettagli tecnici
│
├── ⚡ QUICKSTART.md           (2.7 KB)
│   └── Guida rapida per l'uso
│
├── 📝 PROGETTO.md             (questo file)
│   └── Panoramica completa del progetto
│
├── 📄 test_sample.txt         (540 B)
│   └── File di esempio per testing
│
└── 🚫 .gitignore
    └── File da ignorare in Git
```

**Totale**: ~40 KB di codice e documentazione

---

## ✨ Funzionalità Implementate

### 1. **Lista File** (`list_files()`)
- Legge directory corrente
- Mostra nome, tipo e dimensione
- Conversione automatica (B/KB/MB)
- Filtra entry speciali `.` e `..`

### 2. **Copia File** (`copy_file()`)
- Buffer ottimizzato 4KB
- Verifica esistenza file sorgente
- Gestione errori I/O
- Feedback visivo del risultato

### 3. **Sposta/Rinomina** (`move_file()`)
- Usa system call `rename()`
- Sposta tra directory
- Rinomina file
- Verifica permessi

### 4. **Elimina File** (`delete_file()`)
- System call `unlink()`
- Conferma obbligatoria
- Verifica tipo (no directory)
- Messaggi di errore dettagliati

### 5. **Info File** (`show_file_info()`)
- Statistiche complete via `stat()`
- Permessi in formato rwxrwxrwx
- Dimensione formattata
- Tipo (file/directory)

### 6. **Interfaccia Utente**
- Menu interattivo colorato
- Input sanitization
- Gestione buffer
- Feedback visivo ANSI

---

## 🛠️ Stack Tecnologico

| Componente | Tecnologia |
|------------|-----------|
| **Linguaggio** | C (ANSI C99) |
| **API** | POSIX.1-2008 |
| **System Call** | opendir, readdir, stat, rename, unlink |
| **I/O** | stdio bufferizzato |
| **Platform** | Linux, macOS (Unix-like) |

---

## 📊 Statistiche del Codice

### File Manager (`file_manager.c`)
- **Righe di codice**: ~400
- **Funzioni**: 10 principali
- **System call**: 6 differenti
- **Commenti**: Estensivi in italiano

### Makefile
- **Target**: 7 (all, run, clean, install, uninstall, help)
- **Variabili**: 4
- **Regole**: 10

---

## 🎓 Concetti di System Programming Dimostrati

### 1. **File System Operations**
```c
DIR *d = opendir(".");
struct dirent *dir = readdir(d);
struct stat statbuf;
stat(path, &statbuf);
```

### 2. **I/O Operations**
```c
FILE *src = fopen(source, "rb");
fread(buffer, 1, sizeof(buffer), src);
fwrite(buffer, 1, bytes_read, dest);
```

### 3. **File Manipulation**
```c
rename(old, new);
unlink(filename);
```

### 4. **Error Handling**
```c
if (operation_failed) {
    printf("Errore: %s\n", strerror(errno));
}
```

---

## 🔄 Ciclo di Sviluppo

### Compilazione
```bash
make              # Compila
make run          # Compila + Esegue
make clean        # Pulisce
```

### Testing
1. Esegui `./file_manager`
2. Usa `test_sample.txt` per prove
3. Testa ogni operazione
4. Verifica error handling

### Debugging
```bash
gcc -g file_manager.c -o file_manager
gdb ./file_manager
```

---

## 📈 Complessità Algoritmica

| Operazione | Tempo | Spazio |
|------------|-------|--------|
| List Files | O(n) | O(1) |
| Copy File | O(n) | O(1) |
| Move File | O(1) | O(1) |
| Delete File | O(1) | O(1) |
| File Info | O(1) | O(1) |

*n = numero di file nella directory

---

## 🌟 Punti di Forza

### ✅ Codice
- Pulito e ben commentato
- Error handling robusto
- Input sanitization
- Resource management corretto

### ✅ Documentazione
- README completo
- Guida rapida
- Architettura dettagliata
- Esempi d'uso

### ✅ Usabilità
- Interfaccia intuitiva
- Feedback visivo
- Messaggi chiari
- Conferme di sicurezza

### ✅ Portabilità
- Standard C99
- API POSIX standard
- Makefile cross-platform
- Script di build alternativo

---

## 🚀 Possibili Espansioni Future

### Short Term
- [ ] Supporto argomenti da CLI
- [ ] File search per pattern
- [ ] Modifica permessi (chmod)
- [ ] Creazione directory (mkdir)

### Medium Term
- [ ] Supporto ricorsivo
- [ ] Compressione file
- [ ] Hex viewer
- [ ] File comparison (diff)

### Long Term
- [ ] File system virtual
- [ ] Network operations
- [ ] Multi-threading
- [ ] GUI con ncurses

---

## 📚 Risorse Utilizzate

### Documentazione
- POSIX Specification
- Linux man pages
- The C Programming Language (K&R)

### Standard
- ISO/IEC 9899:1999 (C99)
- IEEE Std 1003.1-2008 (POSIX)

---

## 🏆 Risultati Attesi

### Conoscenze Acquisite
1. ✅ System call Unix/Linux
2. ✅ File system operations
3. ✅ Memory management in C
4. ✅ Error handling patterns
5. ✅ Build automation

### Skills Dimostrate
1. ✅ System programming
2. ✅ C programming
3. ✅ API POSIX
4. ✅ Software documentation
5. ✅ Build tools (Make)

---

## 📝 Checklist del Progetto

- [x] Codice sorgente completo
- [x] Makefile funzionante
- [x] Script di build alternativo
- [x] README dettagliato
- [x] Guida rapida
- [x] Documentazione architettura
- [x] File di test
- [x] Gestione errori
- [x] Interfaccia utente
- [x] Commenti in italiano

---

## 🎉 Conclusione

Questo **File Manager in C** rappresenta un progetto completo di System Programming che dimostra:

- **Competenza tecnica** nel linguaggio C
- **Conoscenza** delle system call POSIX
- **Professionalità** nella documentazione
- **Completezza** nell'implementazione

Il progetto è pronto per essere:
- ✅ Compilato e testato
- ✅ Studiato e modificato
- ✅ Espanso con nuove funzionalità
- ✅ Presentato come portfolio piece

---

**Creato per**: Portfolio Project Ideas - System Programming
**Linguaggio**: Italiano 🇮🇹
**Data**: Febbraio 2026

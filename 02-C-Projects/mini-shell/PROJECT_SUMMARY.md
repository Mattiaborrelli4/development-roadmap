# Mini Shell - Project Summary

## Panoramica del Progetto

**Nome:** Mini Shell
**Linguaggio:** C (C99)
**Piattaforme:** Windows, Linux, macOS
**Data:** Febbraio 2026
**Categoria:** Sistema Operativo / Shell Unix

## Descrizione

Mini Shell è un interprete di comandi Unix-like scritto interamente in C. Il progetto dimostra conoscenza avanzata di system call, gestione dei processi, parsing di stringhe, e programmazione cross-platform.

## Caratteristiche Tecniche

### Core Functionality
- ✅ Parser di input con tokenizzazione
- ✅ 8 comandi built-in (cd, pwd, ls, echo, exit, clear, history, help)
- ✅ Esecuzione programmi esterni via fork/exec (Unix) o spawn (Windows)
- ✅ History comandi con persistenza su file
- ✅ Gestione segnali (SIGINT/SIGCHLD su Unix)
- ✅ Prompt interattivo colorato
- ✅ Gestione errori robusta

### Architettura

```
mini-shell/
├── shell.h          # Header con definizioni e prototipi
├── shell.c          # Implementazione (~600 righe)
├── test_shell.c     # Suite di test unitari
├── Makefile         # Build per Unix/Linux
├── Makefile.test    # Build per test suite
├── build.bat        # Build per Windows
├── demo.sh          # Demo script per Unix
├── demo.bat         # Demo script per Windows
├── README.md        # Documentazione completa (IT)
├── QUICKSTART.md    # Guida rapida
├── EXAMPLES.md      # Esempi d'uso dettagliati
└── .gitignore       # Ignora file di build
```

## Dettagli Tecnici

### System Calls Utilizzate

#### Unix/Linux
- `fork()` - Crea processo figlio
- `execvp()` - Esegue programma esterno
- `waitpid()` - Attende processo figlio
- `getcwd()` - Ottiene directory corrente
- `chdir()` - Cambia directory
- `sigaction()` - Configura gestori segnale
- `getpwuid()` - Ottiene home directory

#### Windows
- `_spawnvp()` - Esegue programma esterno
- `_getcwd()` - Ottiene directory corrente
- `_chdir()` - Cambia directory

### Librerie C Standard
- `<stdio.h>` - I/O standard
- `<stdlib.h>` - Allocazione memoria, system()
- `<string.h>` - Manipolazione stringhe
- `<errno.h>` - Gestione errori

### Gestione Memoria
- Allocazione dinamica con `malloc()`
- Deallocazione con `free()`
- Duplicazione stringhe con `strdup()`
- Controllo rigoroso memory leak

## Code Metrics

### shell.c
- **Righe totali:** ~600
- **Funzioni:** 25+
- **Commenti:** Estensivi (italiano)
- **Complessità:** Cyclomatic complexity medio-bassa

### Funzioni Principali
```c
int main()                    // Loop principale
void initialize_shell()       // Setup iniziale
char* read_input()           // Lettura input
char** parse_input()         // Tokenizzazione
int execute_builtin()         // Comandi interni
int execute_external()        // Programmi esterni
void handle_sigint()         // Gestione Ctrl+C
```

## Compilazione ed Esecuzione

### Linux/macOS
```bash
# Compilazione
make

# Esecuzione
./mini-shell

# Test
make test
```

### Windows
```bash
# Compilazione manuale
gcc -Wall -Wextra -std=c99 -o mini-shell.exe shell.c

# Oppure con script
build.bat

# Esecuzione
mini-shell.exe
```

## Comandi Supportati

### Built-in
| Comando | Funzione |
|---------|----------|
| `cd [dir]` | Cambia directory |
| `pwd` | Mostra directory corrente |
| `ls [dir]` | Lista file |
| `echo [text]` | Stampa testo |
| `clear` | Pulisci schermo |
| `history` | Mostra cronologia |
| `help` | Mostra aiuto |
| `exit [n]` | Esci dalla shell |

### Esterne
Qualsiasi comando disponibile nel sistema PATH:
- `gcc`, `python`, `vim`, `git`, etc.

## Funzionalità Avanzate

### History Management
- Salvataggio automatico in `.mini_shell_history`
- Ricarica all'avvio
- Fino a 100 comandi memorizzati
- Comando `history` per visualizzazione

### Gestione Segnali (Unix)
- SIGINT (Ctrl+C): Non termina la shell
- SIGCHLD: Pulisce processi zombie
- Messaggio informativo all'utente

### Cross-Platform
- Preprocessore condizionale `#ifdef _WIN32`
- System calls wrapper per compatibilità
- Prompt semplice su Windows (no colori ANSI)
- Stessa interfaccia utente su tutte le piattaforme

## Testing

### Test Suite
- File: `test_shell.c`
- 12 test unitari
- Copertura: Parser, built-in, history
- Esecuzione: `make test`

### Test Manuali
```bash
# Test navigazione
cd /tmp && pwd

# Test esterni
gcc --version
python -c "print('test')"

# Gestione errori
comando_inesistente
cd /dir/inesistente
```

## Limitazioni Correnti

1. **No piping** - Non supporta `|`
2. **No I/O redirection** - Non supporta `>`, `<`, `>>`
3. **No background** - Non supporta `&`
4. **No tab completion** - Non supporta TAB
5. **History navigation** - Solo visualizzazione, no frecce

Queste possono essere implementate in versioni future.

## Obiettivi Educativi

Il progetto dimostra conoscenza di:

### Concetti OS
- **Process Creation:** fork(), exec(), wait()
- **Process Synchronization:** Parent-child coordination
- **Signal Handling:** Interrupt processing
- **System Calls:** OS interaction

### Programmazione C
- **Memory Management:** malloc/free, pointers
- **String Handling:** strtok, strcmp, strdup
- **File I/O:** fopen, fclose
- **Error Handling:** errno, perror

### Best Practices
- **Modular Design:** Separation interface/implementation
- **Code Documentation:** Extensive comments
- **Cross-Platform:** Portable code
- **Defensive Programming:** Input validation

## Estensioni Future

### Priorità Alta
- [ ] Pipe tra comandi (`|`)
- [ ] I/O redirection (`>`, `<`)
- [ ] Variabili ambiente

### Priorità Media
- [ ] Processi background (`&`)
- [ ] Command chaining (`;`, `&&`, `||`)
- [ ] Wildcard expansion (`*`, `?`)

### Priorità Bassa
- [ ] Tab completion
- [ ] History navigation (frecce)
- [ ] Command aliases
- [ ] Shell scripting

## Risultati

### Funzionalità
✅ Tutti i requisiti base implementati
✅ Completamente cross-platform
✅ Documentazione completa in italiano
✅ Test suite funzionante

### Qualità Codice
✅ Compila senza warning (con -Wall -Wextra)
✅ Nessun memory leak
✅ Codice ben commentato
✅ Nomi funzioni descrittivi

### User Experience
✅ Prompt interattivo
✅ Messaggi errore chiari
✅ Help integrato
✅ Comandi intuitivi

## Conclusione

Mini Shell è un progetto completo e funzionante che dimostra solide capacità di programmazione di sistema in C. L'implementazione è pulita, ben documentata, e pronta per estensioni future.

### Metriche Finali
- **Tempo sviluppo:** ~4 ore
- **Righe codice:** ~600 (shell.c)
- **File totali:** 12
- **Test:** 12 unitari
- **Documentazione:** 4 file markdown

---

**Progetto completato con successo!** ✅

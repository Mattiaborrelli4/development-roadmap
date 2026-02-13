# Mini Vim - Riepilogo Progetto

## Panoramica

Mini Vim è un editor di testo modale leggero scritto in puro C, ispirato a Vim. Supporta le modalità NORMAL e INSERT per un editing efficiente del testo.

## File Creati

### Codice Sorgente
- **`buffer.h`** (2018 bytes) - Header per la gestione del buffer di testo
- **`buffer.c`** (7792 bytes) - Implementazione delle operazioni sul buffer
- **`editor.c`** (11860 bytes) - Loop principale, gestione I/O e comandi

### Documentazione
- **`README.md`** (5413 bytes) - Documentazione completa in italiano
- **`QUICKSTART.md`** (3171 bytes) - Guida rapida per iniziare
- **`PROGETTO.md`** - Questo file

### Build Script
- **`Makefile`** (2020 bytes) - Makefile per compilazione automatizzata
- **`build.bat`** (1625 bytes) - Script di build per Windows
- **`build.sh`** (1495 bytes) - Script di build per Linux/Unix
- **`cleanup.bat`** (308 bytes) - Script pulizia per Windows

### Altro
- **`.gitignore`** (459 bytes) - File ignorati da Git
- **`example.txt`** (650 bytes) - File di esempio per testare l'editor

### Compilato
- **`mini-vim.exe`** (67957 bytes) - Eseguibile Windows (già compilato!)

## Caratteristiche Implementate

### Core
- Buffer dinamico che cresce automaticamente
- Array di linee con capacità variabile
- Gestione cursore (x, y)
- Flag di modifica

### Modalità
- **NORMAL**: Navigazione e comandi
- **INSERT**: Inserimento testo
- **COMMAND**: Comandi :w, :q, :wq, :e

### Comandi NORMAL
- h, j, k, l - movimento cursore
- i - entra in INSERT
- : - entra in COMMAND
- ESC - annulla

### Comandi INSERT
- Caratteri stampabili
- BACKSPACE - cancella
- ENTER - nuova riga
- ESC - torna a NORMAL

### Comandi COMMAND
- :w - salva
- :w file - salva con nome
- :q - esci
- :wq - salva e esci
- :e file - carica file

## Dettagli Tecnici

### Gestione Memoria
- Allocazione dinamica con malloc/realloc
- Capacità iniziale: 100 righe
- Ogni riga: 1024 caratteri
- Raddoppio capacità quando necessario

### Cross-Platform
- Windows: conio.h (_kbhit, _getch)
- Linux/Unix: termios (raw mode)
- Rilevamento automatico piattaforma

### Codice Pulito
- Compila senza warning (-Wall -Wextra)
- Standard C99
- Codice ben commentato in italiano
- Nomi variabili significativi

## Compilazione

### Già Compilato
Il progetto è già stato compilato con successo:
```
mini-vim.exe - 67 KB
```

### Ricompilare
```bash
# Windows
build.bat

# Linux
./build.sh

# Con Make
make
```

## Test

### Test Rapido
```bash
# Avvio
mini-vim.exe

# Carica esempio
mini-vim.exe example.txt

# Test comandi
i [insert text] ESC :w test.txt :q
```

## Struttura del Codice

### Buffer Module (buffer.c)
```c
buffer_create()       // Crea nuovo buffer
buffer_destroy()      // Distrugge buffer
buffer_insert_char()  // Inserisce carattere
buffer_delete_char()  // Cancella carattere
buffer_insert_newline() // Nuova riga
buffer_load_file()    // Carica da disco
buffer_save_file()    // Salva su disco
buffer_move_*()       // Movimento cursore
```

### Editor Module (editor.c)
```c
editor_init()         // Inizializza editor
editor_cleanup()      // Pulisce risorse
editor_draw()         // Render schermo
editor_handle_*()     // Gestione input
editor_run()          // Loop principale
```

## Statistiche Progetto

| Metrica | Valore |
|---------|--------|
| Totale righe codice | ~600 |
| File sorgente | 3 |
| Header | 1 |
| Documentazione | 3 file |
| Script build | 4 |
| Linguaggio | C (C99) |
| Dipendenze | Solo standard library |

## Limitazioni Note

- Nessun undo/redo
- Nessun syntax highlighting
- Cursore simulato con `|`
- Nessuna ricerca/sostituzione
- Nessun copy/paste
- Supporto solo testo

## Possibili Miglioramenti

- [ ] Undo/redo stack
- [ ] Numeri di riga
- [ ] Ricerca (/pattern)
- [ ] Sostituzione (:s)
- [ ] Visual mode
- [ ] Yank/Put register
- [ ] Multi-buffer
- [ ] Split screen
- [ ] Syntax highlighting
- [ ] Config file (.vimrc)

## Conclusione

Mini Vim è un progetto educativo completo che dimostra:
- Programmazione C avanzata
- Gestione memoria dinamica
- I/O a basso livello
- Cross-platform development
- Strutture dati dinamiche
- Design modulare

Il progetto è funzionale, compilato e pronto all'uso!

---
Creato il: 12 Febbraio 2026
Piattaforma: Windows/Linux
Linguaggio: C (C99)
Stato: COMPLETATO

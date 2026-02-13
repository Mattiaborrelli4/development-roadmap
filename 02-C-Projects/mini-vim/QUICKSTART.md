# Mini Vim - Guida Rapida

## Compilazione

### Windows
```bash
# Opzione 1: Con lo script batch
build.bat

# Opzione 2: Manuale con GCC
gcc -Wall -Wextra -std=c99 -pedantic -c buffer.c -o buffer.o
gcc -Wall -Wextra -std=c99 -pedantic -c editor.c -o editor.o
gcc buffer.o editor.o -o mini-vim.exe

# Opzione 3: Con Make (se installato)
make
```

### Linux/macOS
```bash
# Opzione 1: Con lo script shell
chmod +x build.sh
./build.sh

# Opzione 2: Manuale
gcc -Wall -Wextra -std=c99 -pedantic -c buffer.c -o buffer.o
gcc -Wall -Wextra -std=c99 -pedantic -c editor.c -o editor.o
gcc buffer.o editor.o -o mini-vim

# Opzione 3: Con Make
make
```

## Primi Passi

### 1. Avvio
```bash
# Windows
mini-vim.exe

# Linux/macOS
./mini-vim
```

### 2. Test con file di esempio
```bash
# Windows
mini-vim.exe example.txt

# Linux/macOS
./mini-vim example.txt
```

## Comandi Essenziali

### Modalità NORMAL (predefinita)
| Tasto | Azione |
|-------|--------|
| **h** | Sinistra |
| **j** | Giù |
| **k** | Su |
| **l** | Destra |
| **i** | Modalità INSERT |
| **:** | Modalità COMMAND |
| **ESC** | Annulla |

### Modalità INSERT
| Tasto | Azione |
|-------|--------|
| **Caratteri** | Inserisci testo |
| **BACKSPACE** | Cancella |
| **ENTER** | Nuova riga |
| **ESC** | Torna a NORMAL |

### Modalità COMMAND
| Comando | Azione |
|---------|--------|
| **:w** | Salva file |
| **:w nome** | Salva con nome |
| **:q** | Esci (se non modificato) |
| **:wq** | Salva e esci |
| **:wq nome** | Salva con nome e esci |
| **:e nome** | Carica file |
| **ESC** | Torna a NORMAL |

## Esempio di Sessione

```
1. Avvia mini-vim
   > mini-vim.exe

2. Premi ENTER per iniziare

3. Premi 'i' per entrare in modalità INSERT

4. Scrivi: "Hello, World!"

5. Premi ESC per tornare a NORMAL

6. Premi ':' e poi 'w test.txt' per salvare

7. Premi ENTER e conferma

8. Premi ':' e poi 'q' per uscire

9. Congratulazioni! Hai creato il tuo primo file!
```

## Risoluzione Problemi

### Errore: "GCC non trovato"
**Windows**: Installa MinGW-w64 o MSYS2
**Linux**: `sudo apt-get install build-essential`

### L'editor non risponde
Premi ESC più volte per tornare a NORMAL

### Il cursore non si vede
Il cursore è indicato con il simbolo `|` nella riga corrente

### Non riesco a uscire
- Se modificato: salva con `:w` o `:wq`
- Se non modificato: usa `:q`

## File del Progetto

```
mini-vim/
├── buffer.h          # Header gestione buffer
├── buffer.c          # Implementazione buffer
├── editor.c          # Loop principale editor
├── Makefile          # Make per compilazione
├── build.bat         # Script build Windows
├── build.sh          # Script build Linux
├── cleanup.bat       # Pulizia Windows
├── example.txt       # File di esempio
├── QUICKSTART.md     # Questa guida
└── README.md         # Documentazione completa
```

## Divertimento!

Prova a:
- Creare nuovi file
- Modificare example.txt
- Sperimentare con i comandi
- Leggere il codice sorgente!

Buon editing!

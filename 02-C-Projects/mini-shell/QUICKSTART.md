# Mini Shell - Quick Start Guide

Guida rapida per iniziare a usare Mini Shell.

## Compilazione Rapida

### Linux/macOS
```bash
make
```

### Windows (MinGW)
```bash
gcc -Wall -Wextra -std=c99 -o mini-shell.exe shell.c
```

Oppure usa lo script di build:
```bash
build.bat
```

## Esecuzione

### Linux/macOS
```bash
./mini-shell
```

### Windows
```bash
mini-shell.exe
```

## Comandi Essenziali

| Comando | Descrizione |
|---------|-------------|
| `help` | Mostra tutti i comandi |
| `pwd` | Mostra directory corrente |
| `cd <path>` | Cambia directory |
| `ls` | Lista file |
| `echo <text>` | Stampa testo |
| `clear` | Pulisci schermo |
| `history` | Mostra cronologia |
| `exit` | Esci dalla shell |

## Esempio Rapido

```bash
mini-shell> pwd
/home/utente

mini-shell> echo "Ciao!"
Ciao!

mini-shell> cd /tmp
mini-shell> pwd
/tmp

mini-shell> exit
```

## Esecuzione Programmi

```bash
mini-shell> gcc --version
gcc (Ubuntu 11.4.0) 11.4.0

mini-shell> python script.py
Hello from Python!

mini-shell> ls
file1.txt file2.txt
```

## Troubleshooting

### Errore: comando non trovato
Verifica che il comando esista nel sistema.

### Errore di compilazione
Assicurati di avere GCC installato:
```bash
gcc --version
```

### Per Windows
Installa MinGW-w64 da: https://www.mingw-w64.org/

## File Importanti

- `shell.h` - Header file
- `shell.c` - Codice sorgente principale
- `README.md` - Documentazione completa
- `EXAMPLES.md` - Esempi dettagliati
- `test_shell.c` - Suite di test

## Prossimi Passi

1. Leggi `README.md` per la documentazione completa
2. Consulta `EXAMPLES.md` per esempi avanzati
3. Esplora il codice sorgente in `shell.c`
4. Esegui i test con `make test`

Buon divertimento! 🐚

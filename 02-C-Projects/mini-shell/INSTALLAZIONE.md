# Guida Installazione e Compilazione - Mini Shell

Guida completa per installare, compilare ed eseguire Mini Shell su diverse piattaforme.

## Requisiti di Sistema

### Linux
- GCC 4.0 o superiore
- GNU Make (opzionale ma raccomandato)
- libc standard
- Sistema operativo: Ubuntu, Debian, Fedora, Arch, etc.

### macOS
- Xcode Command Line Tools
- GCC (incluso in Xcode Tools) o Clang
- Make (incluso in Xcode Tools)

### Windows
- **Opzione 1:** MinGW-w64 (raccomandato)
- **Opzione 2:** Visual Studio 2019 o superiore
- **Opzione 3:** WSL (Windows Subsystem for Linux)

---

## Installazione GCC

### Linux
```bash
# Debian/Ubuntu
sudo apt-get update
sudo apt-get install build-essential

# Fedora
sudo dnf install gcc make

# Arch Linux
sudo pacman -S base-devel
```

### macOS
```bash
# Installa Xcode Command Line Tools
xcode-select --install
```

### Windows - MinGW-w64
1. Scarica da: https://www.mingw-w64.org/
2. Oppure usa MSYS2: https://www.msys2.org/
3. Aggiungi al PATH

### Windows - Visual Studio
1. Scarica Visual Studio Community (gratuito)
2. Installa "Desktop development with C++"
3. Usa "Developer Command Prompt" per compilare

---

## Compilazione

### Metodo 1: Makefile (Linux/macOS)

Il metodo più semplice:

```bash
# Entra nella directory
cd mini-shell

# Compila
make

# Il compilatore dovrebbe mostrare:
# gcc -Wall -Wextra -std=c99 -pedantic -c shell.c -o shell.o
# gcc shell.o -o mini-shell
# Compilazione completata: mini-shell
```

### Metodo 2: GCC Manuale (Linux/macOS/Windows)

```bash
gcc -Wall -Wextra -std=c99 -pedantic -o mini-shell shell.c
```

#### Spiegazione Flag:
- `-Wall` - Abilita tutti i warning
- `-Wextra` - Warning extra
- `-std=c99` - Standard C99
- `-pedantic` - Stretta conformità allo standard
- `-o mini-shell` - Nome output
- `shell.c` - File sorgente

### Metodo 3: Visual Studio (Windows)

Apri "Developer Command Prompt for VS":

```cmd
cl shell.c /Fe:mini-shell.exe /W3
```

### Metodo 4: Script di Build (Windows)

```bash
build.bat
```

---

## Verifica Compilazione

Dopo la compilazione, verifica che l'eseguibile esista:

### Linux/macOS
```bash
ls -lh mini-shell
# Dovrebbe mostrare qualcosa come:
# -rwxr-xr-x 1 user group 45K Feb 12 14:00 mini-shell
```

### Windows
```cmd
dir mini-shell.exe
# Dovrebbe mostrare:
# mini-shell.exe  45,000  Feb 12 14:00
```

---

## Esecuzione

### Linux/macOS
```bash
./mini-shell
```

### Windows
```cmd
mini-shell.exe
```

### WSL (Windows Subsystem for Linux)
```bash
./mini-shell
```

Dovresti vedere:
```
=================================
  Mini Shell v1.0
  Digita 'help' per i comandi
=================================

mini-shell:/home/utente/mini-shell$
```

---

## Test della Shell

### Test Rapido

Esegui questi comandi per verificare il funzionamento:

```bash
mini-shell> pwd
mini-shell> echo "Hello, World!"
mini-shell> ls
mini-shell> help
mini-shell> history
mini-shell> exit
```

### Test Suite Completa

Il progetto include una suite di test:

#### Linux/macOS
```bash
make -f Makefile.test
./test_shell
```

#### Output Atteso:
```
=================================
  Mini Shell - Test Suite
=================================

🧪 Test: Parsing input
  ✅ PASS: argc == 3
  ✅ PASS: strcmp(args[0], "ls") == 0
  ...

=================================
  Risultati Test
=================================
✅ Passati: 12
❌ Falliti: 0
📊 Totale:  12
=================================

✨ Tutti i test sono passati!
```

---

## Demo Interattiva

### Linux/macOS
```bash
chmod +x demo.sh
./demo.sh
```

### Windows
```cmd
demo.bat
```

---

## Risoluzione Problemi

### Errore: "gcc: command not found"

**Soluzione:** Installa GCC (vedi sezione "Requisiti di Sistema")

### Errore: "fatal error: sys/wait.h: No such file or directory"

**Causa:** Stai compilando su Windows senza supporto Unix

**Soluzione:**
- Usa la versione corretta del codice (già inclusa nel progetto)
- Il codice ha già il supporto per Windows (#ifdef _WIN32)

### Errore: "warning: unused parameter"

**Nota:** Questo è normale. Il codice usa `(void)parameter;` per sopprimere questi warning.

### Errore: "undefined reference to _spawnvp"

**Causa:** Linking problematico su Windows

**Soluzione:**
- Usa `shell.c` direttamente (non linkare oggetti separati)
- Compila in un passo: `gcc shell.c -o mini-shell.exe`

### Errore: "Permission denied"

**Linux/macOS:**
```bash
chmod +x mini-shell
```

**Windows:**
- Verifica che il file non sia bloccato
- Tasto destro > Proprietà > Sblocca (se presente)

---

## Installazione di Sistema (Opzionale)

### Linux/macOS

Per rendere mini-shell disponibile globalmente:

```bash
sudo cp mini-shell /usr/local/bin/
sudo chmod +x /usr/local/bin/mini-shell
```

Ora puoi eseguire mini-shell da qualsiasi directory:

```bash
mini-shell
```

### Disinstallazione

```bash
sudo rm /usr/local/bin/mini-shell
```

---

## Compilazione con Ottimizzazioni

Per una shell più veloce:

```bash
gcc -O2 -Wall -Wextra -std=c99 -pedantic -o mini-shell shell.c
```

Flag di ottimizzazione:
- `-O0` - Nessuna ottimizzazione (debug)
- `-O1` - Ottimizzazione base
- `-O2` - Ottimizzazione raccomandata
- `-O3` - Massima ottimizzazione

---

## Debug

### Compilazione con Debug Symbols

```bash
gcc -g -Wall -Wextra -std=c99 -o mini-shell shell.c
```

### Uso di GDB

```bash
gdb ./mini-shell
(gdb) run
(gdb) backtrace
(gdb) quit
```

### Uso di Valgrind (Memory Leak Detection)

```bash
valgrind --leak-check=full ./mini-shell
```

---

## Build Script Personalizzati

Puoi creare il tuo script di build:

### build.sh (Linux/macOS)
```bash
#!/bin/bash
gcc -O2 -Wall -Wextra -std=c99 -pedantic \
    -o mini-shell shell.c && \
    echo "✅ Build completata!"
```

### build_custom.bat (Windows)
```batch
@echo off
gcc -O2 -Wall -Wextra -std=c99 -pedantic -o mini-shell.exe shell.c
if %ERRORLEVEL% EQU 0 (
    echo Build completata!
) else (
    echo Errore nella build!
)
```

---

## Integrazione con Editor

### VS Code
Crea `.vscode/tasks.json`:
```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Build Mini Shell",
            "type": "shell",
            "command": "gcc",
            "args": [
                "-Wall", "-Wextra", "-std=c99",
                "-o", "mini-shell", "shell.c"
            ],
            "group": {
                "kind": "build",
                "isDefault": true
            }
        }
    ]
}
```

### Vim/Neovim
Aggiungi a `.vimrc`:
```vim
autocmd BufEnter shell.c nnoremap <F5> :w<CR>:!gcc -o mini-shell shell.c && ./mini-shell<CR>
```

---

## Prossimi Passi

Dopo aver compilato con successo:

1. ✅ Leggi `QUICKSTART.md` per iniziare
2. ✅ Consulta `README.md` per la documentazione completa
3. ✅ Vedi `EXAMPLES.md` per esempi avanzati
4. ✅ Leggi `PROJECT_SUMMARY.md` per dettagli tecnici

---

## Supporto

Per problemi o domande:
- Controlla `README.md` - Troubleshooting section
- Verifica i requisiti di sistema
- Assicurati di usare GCC 4.0+ o equivalente

---

Buon divertimento con Mini Shell! 🐚

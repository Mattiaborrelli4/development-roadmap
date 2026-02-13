# 🐚 Mini Shell - Interprete di Comandi in C

Un semplice interprete di shell Unix-like scritto in C, con supporto per comandi built-in, esecuzione di programmi esterni, history dei comandi e gestione dei segnali.

## 📋 Indice

- [Caratteristiche](#caratteristiche)
- [Requisiti](#requisiti)
- [Compilazione](#compilazione)
- [Utilizzo](#utilizzo)
- [Comandi Supportati](#comandi-supportati)
- [Architettura](#architettura)
- [Esempi d'Uso](#esempi-duso)
- [Funzionalità Avanzate](#funzionalità-avanzate)
- [Struttura del Progetto](#struttura-del-progetto)

## ✨ Caratteristiche

### Core Functionality
- ✅ **Parser di comandi** - Tokenizzazione dell'input utente
- ✅ **Comandi Built-in** - Implementazione diretta nella shell
- ✅ **Comandi Esterni** - Esecuzione tramite fork/exec
- ✅ **Prompt interattivo** - "mini-shell>" con percorso corrente

### Advanced Features
- 📚 **History dei comandi** - Salvataggio automatico su file
- 🔒 **Gestione segnali** - Ctrl+C non chiude la shell
- 🎨 **Prompt colorato** - Directory corrente evidenziata
- 💾 **Persistenza history** - Salvataggio/ricarica da file
- 🌍 **Cross-platform** - Compatibile Windows/Linux/macOS

## 🔧 Requisiti

### Linux/Unix
- GCC (GNU Compiler Collection)
- libc standard
- Make (opzionale, ma raccomandato)

### Windows
- MinGW-w64 o Visual Studio
- Oppure WSL (Windows Subsystem for Linux)

## 🛠️ Compilazione

### Linux/Unix/macOS

#### Metodo 1: Usando Make (raccomandato)
```bash
make
```

Per compilare ed eseguire:
```bash
make run
```

#### Metodo 2: Compilazione manuale
```bash
gcc -Wall -Wextra -std=c99 -o mini-shell shell.c
```

### Windows

#### Con MinGW/MSYS2
```bash
gcc -Wall -Wextra -std=c99 -o mini-shell.exe shell.c
```

#### Con Visual Studio
1. Apri "Developer Command Prompt for VS"
2. Naviga nella directory del progetto
3. Esegui:
```cmd
cl shell.c /Fe:mini-shell.exe
```

## 🚀 Utilizzo

Una volta compilato, esegui la shell:

```bash
./mini-shell        # Linux/Unix
./mini-shell.exe    # Windows
```

Vedrai il prompt:
```
=================================
  Mini Shell v1.0
  Digita 'help' per i comandi
=================================

mini-shell>
```

## 📖 Comandi Supportati

### Comandi Built-in

| Comando | Descrizione | Esempio |
|---------|-------------|---------|
| `cd` | Cambia directory corrente | `cd /home/user`, `cd ..` |
| `pwd` | Mostra percorso corrente | `pwd` |
| `ls` | Lista file e directory | `ls`, `ls -la` |
| `echo` | Stampa argomenti | `echo Hello World` |
| `clear` | Pulisce lo schermo | `clear` |
| `history` | Mostra cronologia comandi | `history` |
| `help` | Mostra aiuto | `help` |
| `exit` | Esce dalla shell | `exit`, `exit 0` |

### Comandi Esterni

La shell può eseguire qualsiasi comando disponibile nel sistema:

```bash
mini-shell> gcc --version
mini-shell> python script.py
mini-shell> vim file.txt
mini-shell> git status
```

## 🏗️ Architettura

### Struttura dei File

```
mini-shell/
├── shell.h          # Header file con definizioni e prototipi
├── shell.c          # Implementazione principale
├── Makefile         # File di build
├── README.md        # Documentazione
└── .mini_shell_history  # File history (creato automaticamente)
```

### Componenti Principali

#### 1. Parser di Input
```c
char* read_input(void)
char** parse_input(char *input, int *argc)
```
Legge e tokenizza l'input dell'utente in argomenti.

#### 2. Gestore Built-in
```c
int is_builtin(char *cmd)
int execute_builtin(char **args)
```
Verifica ed esegue i comandi integrati nella shell.

#### 3. Esecuzione Esterna
```c
int execute_external(char **args)
```
Esegue programmi esterni usando fork() ed execvp().

#### 4. Gestione History
```c
void add_to_history(History *hist, const char *command)
void save_history_to_file(History *hist)
void load_history_from_file(History *hist)
```
Gestisce la cronologia dei comandi con persistenza.

#### 5. Gestione Segnali
```c
void handle_sigint(int sig)   // Gestisce Ctrl+C
void handle_sigchld(int sig)  // Gestisce processi figli
```
Prevede la chiusura accidentale e pulisce i processi zombie.

## 💡 Esempi d'Uso

### Navigazione
```bash
mini-shell> pwd
/home/user/projects

mini-shell> cd ..
mini-shell> pwd
/home/user

mini-shell> cd mini-shell
mini-shell> ls
shell.c  shell.h  Makefile  README.md
```

### Esecuzione Comandi
```bash
mini-shell> echo "Ciao, Mondo!"
Ciao, Mondo!

mini-shell> gcc --version
gcc (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0

mini-shell> python -c "print('Python funziona!')"
Python funziona!
```

### History
```bash
mini-shell> history
    1  pwd
    2  cd ..
    3  echo "Ciao, Mondo!"
    4  gcc --version
    5  python -c "print('Python funziona!')"
```

## 🔐 Funzionalità Avanzate

### Gestione Ctrl+C

Premendo Ctrl+C, la shell **non** viene chiusa ma mostra un messaggio:

```
^C
Usa 'exit' per uscire dalla shell.
mini-shell>
```

### Persistenza History

I comandi vengono salvati automaticamente nel file `.mini_shell_history` e ricaricati al prossimo avvio.

### Processi Figli

La shell gestisce correttamente i processi figli:
- Esegue fork() per creare nuovi processi
- Usa execvp() per eseguire programmi esterni
- Implementa waitpid() per attendere la terminazione
- Gestisce SIGCHLD per pulire i processi zombie

## 📂 Struttura del Progetto

### File: shell.h
Contiene tutte le definizioni, include e prototipi di funzione:
- Definizione della struttura `History`
- Prototipi per built-in commands
- Funzioni di parsing
- Gestione segnali

### File: shell.c
Implementazione completa con:
- **~450 righe** di codice C
- Commenti dettagliati in italiano
- Gestione errori robusta
- Codice cross-platform

### Key Functions

```c
// Inizializzazione
void initialize_shell(void)

// Loop principale
int main(int argc, char **argv)

// Esecuzione comandi
int execute_builtin(char **args)
int execute_external(char **args)

// Built-in commands
int builtin_cd(char **args)
int builtin_pwd(char **args)
int builtin_ls(char **args)
// ... ecc
```

## 🧪 Testing

### Test di Base
```bash
# Test built-in
mini-shell> cd /tmp
mini-shell> pwd
/tmp

mini-shell> echo test
test

mini-shell> clear
# Schermo pulito

# Test esterni
mini-shell> ls
file1.txt file2.txt

mini-shell> whoami
user
```

### Test Gestione Errori
```bash
mini-shell> cd /directory/inesistente
cd: No such file or directory

mini-shell> comando_inesistente
mini-shell: comando non trovato: comando_inesistente
```

## 🎯 Obiettivi Educativi

Questo progetto dimostra conoscenza di:

- **System Calls**: fork(), execvp(), waitpid(), chdir(), getcwd()
- **Gestione Processi**: Creazione e sincronizzazione processi
- **Gestione Segnali**: sigaction(), SIGINT, SIGCHLD
- **Memory Management**: Allocazione dinamica, free(), strdup()
- **String Handling**: strtok(), strcmp(), strlen()
- **File I/O**: fopen(), fclose(), fprintf()
- **Unix Philosophy**: Piccoli tool che fanno una cosa bene

## 🚧 Limitazioni Conosciute

1. **No piping** - Non supporta `|` (pipe tra comandi)
2. **No redirection** - Non supporta `>`, `<`, `>>`
3. **No background** - Non supporta `&` (processi in background)
4. **No tab completion** - Non supporta TAB per autocomplete
5. **History semplice** - Solo visualizzazione, non navigazione con frecce

Queste funzionalità possono essere aggiunte in versioni future!

## 📚 Estensioni Possibili

Per rendere la shell più completa, potresti aggiungere:

- [ ] Piping tra comandi (`|`)
- [ ] Redirection I/O (`>`, `<`, `>>`)
- [ ] Processi in background (`&`)
- [ ] Variabili d'ambiente
- [ ] Comandi multipli su una riga (`;`)
- [ ] Wildcard expansion (`*`, `?`)
- [ ] Auto-completion con TAB
- [ ] Navigazione history con frecce su/giù
- [ ] Aliasing di comandi
- [ ] Scripting shell

## 📝 Note di Sviluppo

### Compatibilità
- **Linux**: ✅ Completamente compatibile
- **macOS**: ✅ Completamente compatibile
- **Windows**: ✅ Compatibile con MinGW/WSL

### Standard C
Il codice segue lo standard **C99** con flag di compilazione:
```bash
-Wall -Wextra -std=c99 -pedantic
```

## 🤝 Contributi

Questo è un progetto educativo. Sentiti libero di:
- Forkare il repository
- Aggiungere nuove funzionalità
- Segnalare bug
- Proporre miglioramenti

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT.

## 👨‍💻 Autore

Creato come progetto dimostrativo per il portfolio di programmazione in C.

---

**Buon divertimento con la tua Mini Shell! 🐚**

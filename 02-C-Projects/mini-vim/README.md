# Mini Vim

Un editor di testo modale leggero scritto in C, ispirato a Vim. Mini Vim supporta le modalità NORMAL e INSERT per un editing efficiente del testo.

## Caratteristiche

- **Modalità di editing**: NORMAL e INSERT
- **Gestione del buffer**: Buffer dinamico che cresce automaticamente
- **Salvataggio/caricamento file**: Supporto completo per file di testo
- **Navigazione**: Comandi stile Vim (h, j, k, l)
- **Cross-platform**: Funziona su Windows e Linux/Unix
- **Indicatore cursore**: Mostra la posizione corrente del cursore
- **Flag modificato**: Traccia se il file è stato modificato

## Requisiti

- GCC (GNU Compiler Collection)
- Make (opzionale, per usare il Makefile)
- Sistema operativo: Windows, Linux, o macOS

## Compilazione

### Linux/macOS

```bash
make
```

Oppure manualmente:

```bash
gcc -Wall -Wextra -std=c99 -pedantic -o mini-vim editor.c buffer.c
```

### Windows

Con MinGW/MSYS:

```bash
make
```

Oppure manualmente:

```bash
gcc -Wall -Wextra -std=c99 -pedantic -o mini-vim.exe editor.c buffer.c
```

## Uso

### Avvio

```bash
./mini-vim
```

Per caricare un file esistente:

```bash
./mini-vim filename.txt
```

### Modalità

Il `mini-vim` ha due modalità principali:

#### Modalità NORMAL (default)

In questa modalità puoi navigare e eseguire comandi:

- **h** - Muovi il cursore a sinistra
- **j** - Muovi il cursore in basso
- **k** - Muovi il cursore in alto
- **l** - Muovi il cursore a destra
- **i** - Entra in modalità INSERT
- **:** - Entra in modalità COMMAND

#### Modalità INSERT

In questa modalità puoi inserire testo:

- **Caratteri** - Inserisce il testo digitato
- **BACKSPACE** - Elimina il carattere precedente
- **ENTER** - Inserisce una nuova riga
- **ESC** - Torna alla modalità NORMAL

#### Modalità COMMAND

Permette di eseguire comandi:

Digita **:** in modalità NORMAL, poi:

- **:w** - Salva il file corrente
- **:w filename** - Salva con un nome specifico
- **:q** - Esci dall'editor (solo se non modificato)
- **:wq** - Salva e esci
- **:wq filename** - Salva con nome e esci
- **:e filename** - Carica un file esistente
- **ESC** - Cancella il comando e torna a NORMAL

## Struttura del Progetto

```
mini-vim/
├── buffer.h      # Header per la gestione del buffer
├── buffer.c      # Implementazione del buffer
├── editor.c      # Loop principale e gestione I/O
├── Makefile      # Makefile per la compilazione
└── README.md     # Questo file
```

## Architettura

### Buffer (`buffer.h`, `buffer.c`)

Il modulo `buffer` gestisce il contenuto del testo:

- **Buffer dinamico**: Array di linee che cresce automaticamente
- **Gestione cursore**: Traccia posizione x e y
- **Operazioni**: Inserimento, cancellazione, movimento
- **I/O file**: Caricamento e salvataggio su disco

### Editor (`editor.c`)

Il modulo `editor` gestisce l'interfaccia utente:

- **Stato**: Modalità corrente, flag di esecuzione
- **Input**: Gestione tastiera dipendente dalla piattaforma
- **Rendering**: Disegno dello schermo e del cursore
- **Comandi**: Parsing ed esecuzione dei comandi

## Dettagli Tecnici

### Gestione della Memoria

- Ogni riga è allocata dinamicamente con capacità iniziale di 1024 caratteri
- L'array delle righe raddoppia quando necessario
- Tutte le allocazioni sono verificate per errori
- La memoria è liberata correttamente alla chiusura

### Piattaforma

Il codice rileva automaticamente la piattaforma:

- **Windows**: Usa `conio.h` per `_kbhit()` e `_getch()`
- **Unix/Linux**: Usa `termios` per la modalità raw

### Modalità Raw

Per l'input non bufferizzato (tasti premuti immediatamente):

- **Unix**: Disabilita ICANON e ECHO in termios
- **Windows**: Usa direttamente le funzioni conio

## Limitazioni

- Nessun undo/redo
- Nessun syntax highlighting
- Nessuna ricerca/sostituzione
- Nessun supporto per più file
- Nessun copia/incolla
- Il cursore è indicato con `|` e non con il cursore reale del terminale
- Nessun supporto per file binari

## Esempi di Utilizzo

### Creare un nuovo file

```bash
./mini-vim
i                    # Entra in modalità INSERT
Hello World!         # Digita testo
[ESC]                # Torna a NORMAL
:w nuovo.txt         # Salva come "nuovo.txt"
:q                   # Esci
```

### Modificare un file esistente

```bash
./mini-vim esistente.txt
j                    # Vai alla riga successiva
l                    # Muovi a destra
i                    # Entra in INSERT
testo aggiuntivo    # Aggiungi testo
[ESC]                # Torna a NORMAL
:wq                  # Salva e esci
```

## Sviluppo Futuro

Potenziali miglioramenti:

- [ ] Supporto per più buffer
- [ ] Undo/redo
- [ ] Ricerca e sostituzione
- [ ] Numeri di riga
- [ ] Cursore reale del terminale
- [ ] Supporto per tabs
- [ ] Copia/incolla (yank/put)
- [ ] Visual mode per selezione testo
- [ ] Comandi più avanzati (:%s, :g, etc.)
- [ ] Configurazione .vimrc

## Licenza

Questo progetto è fornito "così com'è" per scopi educativi.

## Autore

Creato come progetto educativo per imparare:
- Programmazione C avanzata
- Gestione della memoria
- I/O a basso livello
- Programmazione cross-platform
- Strutture dati dinamiche

Divertiti con Mini Vim!

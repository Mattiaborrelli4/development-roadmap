# Mini Shell - Esempi di Utilizzo

Questa guida fornisce esempi pratici per utilizzare Mini Shell.

## Indice
1. [Comandi Base](#comandi-base)
2. [Esecuzione Programmi](#esecuzione-programmi)
3. [Navigazione File System](#navigazione-file-system)
4. [Scripting](#scripting)
5. [Debug e Troubleshooting](#debug-e-troubleshooting)

## Comandi Base

### Esempio 1: Navigazione Semplice
```bash
mini-shell> pwd
/home/utente

mini-shell> cd /tmp
mini-shell> pwd
/tmp

mini-shell> cd -
mini-shell> pwd
/home/utente
```

### Esempio 2: Listing Directory
```bash
mini-shell> ls
file1.txt  file2.txt  documenti/

mini-shell> cd documenti
mini-shell> ls
report.pdf  appunti.txt
```

### Esempio 3: Echo e Output
```bash
mini-shell> echo "Hello World"
Hello World

mini-shell> echo $HOME
$HOME

mini-shell> echo Nome Cognome Età
Nome Cognome Età
```

## Esecuzione Programmi

### Esempio 4: Compilazione con GCC
```bash
mini-shell> gcc -o hello hello.c
mini-shell> ./hello
Hello, World!

mini-shell> gcc --version
gcc (Ubuntu 11.4.0) 11.4.0
```

### Esempio 5: Script Python
```bash
mini-shell> python -c "print('Python funziona!')"
Python funziona!

mini-shell> python script.py
Output dello script...
```

### Esempio 6: Git
```bash
mini-shell> git status
On branch main
nothing to commit, working tree clean

mini-shell> git log --oneline
a1b2c3d Latest commit
d4e5f6g Previous commit
```

## Navigazione File System

### Esempio 7: Percorsi Assoluti e Relativi
```bash
mini-shell> cd /usr/local/bin
mini-shell> pwd
/usr/local/bin

mini-shell> cd ../..
mini-shell> pwd
/usr

mini-shell> cd ~
mini-shell> pwd
/home/utente
```

### Esempio 8: Esplorazione Directory
```bash
mini-shell> ls -la
total 16
drwxr-xr-x 4 user group 4096 Jan 15 10:30 .
drwxr-xr-x 5 user group 4096 Jan 10 09:15 ..
-rw-r--r-- 1 user group 1024 Jan 14 14:20 file.txt
drwxr-xr-x 2 user group 4096 Jan 13 11:45 subdir/

mini-shell> cd subdir
mini-shell> pwd
/home/utente/subdir
```

## History

### Esempio 9: Visualizzazione History
```bash
mini-shell> echo "comando 1"
comando 1

mini-shell> ls
file1.txt file2.txt

mini-shell> pwd
/home/utente

mini-shell> history
    1  echo "comando 1"
    2  ls
    3  pwd
    4  history
```

## Gestione Processi

### Esempio 10: Esecuzione e Uscita
```bash
mini-shell> python long_script.py
[esecuzione in corso...]

mini-shell> echo $?
0

mini-shell> exit 0
```

### Esempio 11: Gestione Ctrl+C
```bash
mini-shell> python infinite_loop.py
^C
Usa 'exit' per uscire dalla shell.
mini-shell>
```

## Debug e Troubleshooting

### Comandi di Debug
```bash
# Verifica percorso corrente
mini-shell> pwd
/home/utente/projects

# Lista file per debug
mini-shell> ls -la

# Mostra history per vedere comandi precedenti
mini-shell> history

# Pulisci schermo per migliore visibilità
mini-shell> clear
```

### Risoluzione Problemi Comuni

#### Problema: Comando non trovato
```bash
mini-shell> mycommand
mini-shell: comando non trovato: mycommand

# Soluzione: Verifica che il comando esista
mini-shell> which mycommand
/usr/bin/mycommand

# Usa percorso completo
mini-shell> /usr/bin/mycommand
```

#### Problema: Permessi insufficienti
```bash
mini-shell> cd /root
cd: Permission denied

# Soluzione: Usa sudo (esterno)
mini-shell> sudo cd /root
```

## Scripting

### Esempio 12: Script Batch
Puoi creare script che eseguono comandi nella mini-shell:

```bash
#!/bin/bash
# file: batch_commands.txt

echo "Inizio elaborazione..."
cd /home/utente/documenti
ls
echo "Elaborazione completata"
exit
```

Esegui con:
```bash
./mini-shell < batch_commands.txt
```

## Tips e Tricks

### 1. Concatenazione Comandi
```bash
mini-shell> pwd; ls; echo "Fatto!"
```

### 2. Clear Rapids
```bash
mini-shell> clear
# Oppure usa Ctrl+L (se supportato)
```

### 3. Quick Exit
```bash
mini-shell> exit
# Oppure Ctrl+D (EOF)
```

### 4. Help Sempre Disponibile
```bash
mini-shell> help
Mini Shell - Comandi disponibili:
...
```

## Esempi Avanzati

### Esempio 13: Sviluppo Software
```bash
mini-shell> cd projects/myapp
mini-shell> ls
src/ include/ tests/

mini-shell> cd src
mini-shell> gcc -c main.c -o main.o
mini-shell> gcc main.o -o ../myapp
mini-shell> cd ..
mini-shell> ./myapp
Applicazione avviata!
```

### Esempio 14: Gestione File
```bash
mini-shell> touch file.txt
mini-shell> echo "Contenuto" > file.txt
# Nota: redirect non supportato, usa echo invece
mini-shell> echo "Contenuto" >> file.txt
# Anche append non supportato

mini-shell> cat file.txt
# cat funziona se è un comando esterno
```

## Confronto con Bash

| Funzionalità | Mini Shell | Bash |
|--------------|------------|------|
| Built-in cd | ✅ | ✅ |
| Built-in pwd | ✅ | ✅ |
| Built-in echo | ✅ | ✅ |
| Built-in ls | ✅ | ✅ |
| Pipe \| | ❌ | ✅ |
| Redirect > | ❌ | ✅ |
| Background & | ❌ | ✅ |
| Variabili | ❌ | ✅ |
| History | ✅ (base) | ✅ (completa) |

## Prossimi Passi

Dopo aver masterizzato Mini Shell, puoi:

1. Estendere con nuove funzionalità
2. Studiare il codice sorgente
3. Implementare pipe e redirection
4. Aggiungere variabili d'ambiente
5. Creare un proprio interprete

## Risorse

- `shell.h` - Header con definizioni
- `shell.c` - Implementazione principale
- `README.md` - Documentazione completa
- `test_shell.c` - Suite di test

---

Buon divertimento con Mini Shell! 🐚

# 🚀 Guida Rapida - File Manager

## ⚡ Avvio Veloce

### 1. Compilazione
```bash
# Metodo 1: Makefile
make

# Metodo 2: Manuale
gcc -Wall -Wextra -std=c99 file_manager.c -o file_manager

# Metodo 3: Script
./build.sh
```

### 2. Esecuzione
```bash
./file_manager
```

## 📋 Comandi del Menu

| Numero | Operazione | Descrizione |
|--------|-----------|-------------|
| 1 | Lista | Mostra tutti i file nella directory corrente |
| 2 | Copia | Crea una copia di un file |
| 3 | Sposta | Sposta o rinomina un file |
| 4 | Elimina | Rimuove un file (con conferma) |
| 5 | Info | Mostra dettagli sul file |
| 0 | Esci | Chiude il programma |

## 💡 Esempi Pratici

### Copiare un file
```
1. Seleziona "2" dal menu
2. Inserisci nome file sorgente: test_sample.txt
3. Inserisci nome destinazione: copia_test.txt
4. ✓ File copiato!
```

### Rinominare un file
```
1. Seleziona "3" dal menu
2. Inserisci nome vecchio: vecchio.txt
3. Inserisci nuovo nome: nuovo.txt
4. ✓ File rinominato!
```

### Eliminare un file
```
1. Seleziona "4" dal menu
2. Inserisci nome: temp.txt
3. Conferma: s
4. ✓ File eliminato!
```

## 🎯 File di Test

Il progetto include `test_sample.txt` per provare le funzionalità:
- Copialo per testare la funzione di copia
- Rinominalo per testare lo spostamento
- Visualizza le sue informazioni
- Eliminalo quando hai finito

## 🔧 Troubleshooting

### Errore: "Permission denied"
```bash
chmod +x file_manager
```

### Errore: "Command not found"
```bash
# Verifica di essere nella directory corretta
pwd
ls file_manager
```

### Compilazione fallita
```bash
# Installa build-essential (Linux)
sudo apt-get install build-essential

# Oppure usa xcode-select (macOS)
xcode-select --install
```

## 📝 Note Importanti

- Il programma NON elimina directory (solo file)
- Le conferme sono obbligatorie per eliminazioni
- Gli errori vengono segnalati con messaggi chiari
- Il programma mostra sempre la directory corrente

## 🎓 Concetti Chiave

### System Call Utilizzate
- **`opendir()` / `readdir()`**: Leggono directory
- **`stat()`**: Ottiene info file
- **`rename()`**: Sposta file
- **`unlink()`**: Elimina file

### Pattern di Codice
- Error checking su ogni operazione
- Pulizia buffer input
- Chiusura file dopo uso
- Feedback utente colorato

## 🌟 Prossimi Passi

Dopo aver provato il programma:
1. Esamina il codice sorgente `file_manager.c`
2. Leggi `ARCHITETTURA.md` per dettagli tecnici
3. Consulta `README.md` per documentazione completa
4. Prova a modificare il codice!

---

**Divertiti con il System Programming! 🚀**

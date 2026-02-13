# Guida Rapida - Student Management System

## 🚀 Avvio Rapido

### Windows
1. **Compilazione automatica**:
   ```
   build.bat
   ```

2. **Esecuzione**:
   ```
   student_manager.exe
   ```

### Usando Make (disponibile su tutti i sistemi)
```
make          # Compila
make run      # Compila ed esegue
make test     # Crea dati di test ed esegue
```

## 📚 Esempi di Utilizzo

### 1. Aggiungere Studenti
```
Scelta: 1
--- AGGIUNGI NUOVO STUDENTE ---
Nome: Mario
Cognome: Rossi
Età: 20
Corso di studi: Informatica
Media voti: 28.5

✓ Studente aggiunto con successo! ID assegnato: 1
```

### 2. Visualizzare Tutti gli Studenti
```
Scelta: 2

============================================
         ELENCO STUDENTI (5)
============================================
ID: 1 | Nome: Mario Rossi | Età: 20 | Corso: Informatica | Media: 28.50
ID: 2 | Nome: Laura Bianchi | Età: 21 | Corso: Matematica | Media: 29.00
ID: 3 | Nome: Giuseppe Verdi | Età: 22 | Corso: Fisica | Media: 27.50
ID: 4 | Nome: Anna Ferrari | Età: 19 | Corso: Chimica | Media: 30.00
ID: 5 | Nome: Marco Colombo | Età: 23 | Corso: Ingegneria | Media: 26.50
============================================
```

### 3. Caricare Dati di Esempio
```
Scelta: 9
--- CARICA DATI DA FILE ---
Nome del file (premi INVIO per 'students.txt'): sample_data.txt
Attenzione: Ci sono già 0 studenti in memoria.
Vuoi sostituirli con i dati del file? (s/n): s

✓ 5 studenti caricati da sample_data.txt
```

### 4. Cercare Studente per ID
```
Scelta: 3
--- CERCA STUDENTE PER ID ---
Inserisci ID: 1

✓ Studente trovato:
ID: 1 | Nome: Mario Rossi | Età: 20 | Corso: Informatica | Media: 28.50
```

### 5. Aggiornare Studente
```
Scelta: 6
--- AGGIORNA STUDENTE ---
Inserisci ID dello studente da aggiornare: 1

Studente attuale:
ID: 1 | Nome: Mario Rossi | Età: 20 | Corso: Informatica | Media: 28.50

Inserisci i nuovi dati (lascia vuoto per mantenere):
Nome [Mario]: Mario
Cognome [Rossi]: Rossi
Età [20]: 21
Corso [Informatica]: Ingegneria Informatica
Media [28.5]: 29.0

✓ Studente con ID 1 aggiornato con successo!
```

### 6. Salvare su File
```
Scelta: 8
--- SALVA DATI SU FILE ---
Nome del file (premi INVIO per 'students.txt'):

✓ 5 studenti salvati su students.txt
```

### 7. Eliminare Studente
```
Scelta: 7
--- ELIMINA STUDENTE ---
Inserisci ID dello studente da eliminare: 5

Studente da eliminare:
ID: 5 | Nome: Marco Colombo | Età: 23 | Corso: Ingegneria | Media: 26.50

Confermi l'eliminazione? (s/n): s

✓ Studente con ID 5 eliminato con successo!
```

## 📁 File del Progetto

### File di Codice Sorgente
- `student.h` - Definizione classi Student e StudentManager
- `student.cpp` - Implementazione metodi
- `main.cpp` - Programma principale con menù

### File di Supporto
- `README.md` - Documentazione completa
- `USAGE.md` - Questa guida
- `Makefile` - Per compilazione su Unix/Linux
- `build.bat` - Script di compilazione per Windows
- `test.bat` - Script di test automatico

### File di Dati
- `students.txt` - Database principale (creato automaticamente)
- `sample_data.txt` - Dati di esempio per testing
- `test_students.txt` - File temporaneo per i test

## 🔧 Risoluzione Problemi

### Errore: "g++ non trovato"
**Soluzione**: Installa MinGW-w64 o MSYS2 su Windows

### Il programma non parte
**Soluzione**: Verifica che student_manager.exe esista nella cartella

### Dati persi
**Soluzione**: Carica il file di backup: sample_data.txt

## 📊 Struttura del Database

Formato file CSV (comma-separated values):
```
id,nome,cognome,età,corso,media
```

Esempio:
```
1,Mario,Rossi,20,Informatica,28.5
```

## 💡 Consigli

1. **Salva frequentemente**: Usa l'opzione 8 per salvare dopo modifiche importanti
2. **Backup periodici**: Copia students.txt in una posizione sicura
3. **ID univoci**: Il sistema genera automaticamente ID univoci
4. **Ricerca veloce**: Usa l'ID per ricerca istantanea
5. **File di esempio**: Usa sample_data.txt per testare le funzionalità

## 🎯 Esercizi Suggeriti

1. Aggiungi 10 studenti di corsi diversi
2. Prova tutte le funzioni di ricerca
3. Aggiorna la media di uno studente
4. Salva su un file diverso (es. backup.txt)
5. Carica sample_data.txt e fai ricerche
6. Crea un scenario reale di gestione classe

---
**Divertiti con il tuo Student Management System!** 📚✨

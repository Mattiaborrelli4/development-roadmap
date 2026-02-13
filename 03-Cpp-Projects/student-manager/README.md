# 🎓 Sistema di Gestione Studenti - Student Manager

Un sistema completo per la gestione degli studenti sviluppato in C++ con paradigma OOP (Object-Oriented Programming).

## 📋 Descrizione

Questo progetto implementa un sistema di gestione studenti con funzionalità CRUD complete (Create, Read, Update, Delete). Utilizza classi C++, vettori della STL, e operazioni di I/O su file per il salvataggio permanente dei dati.

## ✨ Caratteristiche

### Operazioni CRUD
- ✅ **Aggiungi** studenti con tutti i dettagli (nome, cognome, età, corso, media voti)
- ✅ **Visualizza** tutti gli studenti in formato tabellare
- ✅ **Cerca** studenti per ID, nome o cognome
- ✅ **Aggiorna** le informazioni degli studenti esistenti
- ✅ **Elimina** studenti con conferma di sicurezza

### Gestione File
- 💾 **Salva** i dati su file CSV
- 📂 **Carica** i dati da file CSV
- 🔄 **Auto-salvataggio** all'uscita (opzionale)
- 🚀 **Auto-caricamento** all'avvio

### Interfaccia Utente
- 🖥️ Menù testuale interattivo e facile da usare
- ✨ Messaggi di feedback per ogni operazione
- 🔒 Conferma prima di eliminare studenti
- 📊 Statistiche in tempo reale

## 📁 Struttura del Progetto

```
student-manager/
├── student.h       # Header file con definizione delle classi
├── student.cpp     # Implementazione dei metodi della classe
├── main.cpp        # Programma principale con menù interattivo
├── README.md       # Documentazione del progetto
└── students.txt    # File database (creato automaticamente)
```

## 🏗️ Architettura del Codice

### Classe `Student`

Rappresenta un singolo studente con i seguenti attributi:

```cpp
private:
    int id;                    // Identificativo univoco
    std::string name;          // Nome
    std::string surname;       // Cognome
    int age;                   // Età
    std::string course;        // Corso di studi
    double averageGrade;      // Media voti
```

**Metodi principali:**
- `display()` - Visualizza le informazioni dello studente
- `toString()` - Converte in formato CSV
- `fromString()` - Crea da stringa CSV
- Getter e Setter per tutti gli attributi

### Classe `StudentManager`

Gestisce la collezione di studenti con operazioni CRUD:

```cpp
private:
    std::vector<Student> students;  // Vettore dinamico di studenti
    int nextId;                     // Prossimo ID disponibile
```

**Metodi principali:**
- `addStudent()` - Aggiunge un nuovo studente
- `deleteStudent()` - Rimuove uno studente
- `updateStudent()` - Modifica i dati di uno studente
- `searchById()` - Ricerca per ID
- `searchByName()` - Ricerca per nome
- `searchBySurname()` - Ricerca per cognome
- `displayAll()` - Mostra tutti gli studenti
- `saveToFile()` - Salva su file
- `loadFromFile()` - Carica da file
- `generateId()` - Genera ID univoci

## 🚀 Compilazione ed Esecuzione

### Requisiti
- Compilatore C++ con supporto C++11 o superiore (g++, clang++, MSVC)
- Sistema operativo: Windows, Linux, macOS

### Compilazione

#### Windows (g++)
```bash
g++ -o student_manager main.cpp student.cpp -std=c++11
```

#### Linux/macOS
```bash
g++ -o student_manager main.cpp student.cpp -std=c++11
```

### Esecuzione

#### Windows
```bash
student_manager.exe
```

#### Linux/macOS
```bash
./student_manager
```

## 📖 Come Usare

### 1. Avvio del Programma

All'avvio, il programma tenta automaticamente di caricare i dati salvati in `students.txt`.

```
╔════════════════════════════════════════════════════════════╗
║        SISTEMA DI GESTIONE STUDENTI - C++ Project          ║
║                  Progetto OOP con C++                      ║
╚════════════════════════════════════════════════════════════╝
```

### 2. Menù Principale

```
╔══════════════════════════════════════════════╗
║   SISTEMA DI GESTIONE STUDENTI                ║
╠══════════════════════════════════════════════╣
║  1. Aggiungi nuovo studente                   ║
║  2. Visualizza tutti gli studenti            ║
║  3. Cerca studente per ID                     ║
║  4. Cerca studente per nome                   ║
║  5. Cerca studente per cognome                ║
║  6. Aggiorna studente                         ║
║  7. Elimina studente                         ║
║  8. Salva dati su file                       ║
║  9. Carica dati da file                      ║
║  0. Esci                                     ║
╚══════════════════════════════════════════════╝
```

### 3. Esempi di Utilizzo

#### Aggiungere uno Studente
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

#### Visualizzare Tutti gli Studenti
```
Scelta: 2

============================================
         ELENCO STUDENTI (3)
============================================
ID: 1 | Nome: Mario Rossi | Età: 20 | Corso: Informatica | Media: 28.50
ID: 2 | Nome: Laura Bianchi | Età: 21 | Corso: Matematica | Media: 29.00
ID: 3 | Nome: Giuseppe Verdi | Età: 22 | Corso: Fisica | Media: 27.50
============================================
```

#### Aggiornare uno Studente
```
Scelta: 6

--- AGGIORNA STUDENTE ---
Inserisci ID dello studente da aggiornare: 1

Studente attuale:
ID: 1 | Nome: Mario Rossi | Età: 20 | Corso: Informatica | Media: 28.50

Inserisci i nuovi dati (lascia vuoto per mantenere il valore attuale):
Nome [Mario]: Mario
Cognome [Rossi]: Rossi
Età [20]: 21
Corso [Informatica]: Ingegneria Informatica
Media [28.5]: 29.0

✓ Studente con ID 1 aggiornato con successo!
```

## 📊 Formato del File Database

Il file `students.txt` utilizza un formato CSV semplice:

```
1,Mario,Rossi,20,Informatica,28.5
2,Laura,Bianchi,21,Matematica,29.0
3,Giuseppe,Verdi,22,Fisica,27.5
```

Formato: `id,nome,cognome,età,corso,media`

## 🎯 Concetti C++ Utilizzati

### Programmazione Orientata agli Oggetti (OOP)
- ✅ **Classi** e **Oggetti**
- ✅ **Incapsulamento** (membri privati con metodi pubblici)
- ✅ **Costruttori** (default e con parametri)
- ✅ **Metodi getter** e **setter**

### STL (Standard Template Library)
- ✅ `std::vector` - Contenitore dinamico
- ✅ `std::string` - Gestione stringhe
- ✅ `std::stringstream` - Parsing stringhe
- ✅ `std::ofstream` - Scrittura file
- ✅ `std::ifstream` - Lettura file

### Altre Funzionalità
- ✅ **Riferimenti** (`&`) per efficienza
- ✅ **Const correctness** per sicurezza
- ✅ **Gestione errori** con valori di ritorno booleani
- ✅ **Validazione input** utente
- ✅ **Menu interattivo** con loop

## 🔧 Possibili Estensioni

- [ ] Ordinamento studenti per nome, cognome o media
- [ ] Filtri avanzati (età, corso, range di media)
- [ ] Esportazione in formati diversi (JSON, XML)
- [ ] Statistiche (media generale, distribuzione età)
- [ ] Interfaccia grafica (Qt, wxWidgets)
- [ ] Database SQL invece di file CSV
- [ ] Autenticazione utenti con permessi
- [ ] Gestione corsi e professori
- [ ] Registro valutazioni dettagliato

## 📝 Note di Sviluppo

### Commenti nel Codice
Tutti i commenti nel codice sono in italiano come richiesto:
- Commenti Doxygen per classi e metodi
- Spiegazioni inline per logica complessa
- Documentazione delle strutture dati

### Best Practice Applicate
- Validazione dell'input utente
- Pulizia del buffer di input
- Gestione sicura dei file
- Feedback utente per ogni operazione
- Codice modulare e riutilizzabile

## 👨‍💻 Autore

Sviluppato come progetto educativo per dimostrare l'uso di:
- Classi C++ e OOP
- Contenitori STL
- Gestione file I/O
- Design di interfacce utente testuali

## 📄 Licenza

Questo progetto è a scopo educativo. Libero utilizzo e modifica.

---

**Buon coding! 🚀**

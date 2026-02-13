# 🗄️ Mini Database Engine

Un semplice motore di database key-value scritto in puro C con hash table per l'indicizzazione e persistenza su file binario.

## 📋 Caratteristiche

- **Key-Value Store**: Memorizza dati come coppie chiave-valore
- **CRUD Operations**: Create, Read, Update, Delete complete
- **Hash Table Indexing**: Accesso O(1) medio tramite hash table
- **Persistenza su File**: Salvataggio automatico e manuale su file binario
- **Timestamp**: Ogni record ha un timestamp di creazione/modifica
- **CLI Interattivo**: Interfaccia a riga di comando intuitiva
- **Collision Handling**: Linear probing per gestire le collisioni della hash table

## 🚀 Compilazione ed Esecuzione

### Requisiti
- Compilatore GCC con supporto C99
- Sistema Unix-like (Linux, macOS) o Windows con MinGW

### Compilazione con Make

```bash
cd mini-database
make
```

### Esecuzione

```bash
# Esecuzione normale
./minidb

# Esecuzione con file database specifico
./minidb mystore.db
```

### Compilazione Manuale

```bash
gcc -Wall -Wextra -std=c99 -O2 -o minidb main.c database.c
```

## 📚 Comandi Disponibili

### Comandi CRUD

#### `SET <chiave> <valore>`
Salva un nuovo record o aggiorna uno esistente.

```bash
db> SET nome Mario Rossi
OK: Chiave 'nome' impostata

db> SET eta 30
OK: Chiave 'eta' impostata

db> SET email mario.rossi@example.com
OK: Chiave 'email' impostata
```

#### `GET <chiave>`
Recupera il valore associato a una chiave.

```bash
db> GET nome
Valore: Mario Rossi

db> GET eta
Valore: 30
```

#### `DELETE <chiave>`
Rimuove una chiave dal database.

```bash
db> DELETE email
OK: Chiave 'email' eliminata
```

#### `LIST`
Mostra tutti i record nel database con timestamp.

```bash
db> LIST

=== Database (2 record) ===
Chiave               Valore                         Timestamp
-----               -----                         ---------
nome                Mario Rossi                    2026-02-12 10:30:45
eta                 30                             2026-02-12 10:30:47
===========================
```

### Comandi di Persistenza

#### `SAVE [filename]`
Salva il database su file binario.

```bash
db> SAVE
Database salvato con successo: 2 record in 'database.db'

db> SAVE backup.db
Database salvato con successo: 2 record in 'backup.db'
```

#### `LOAD [filename]`
Carica il database da file binario.

```bash
db> LOAD
Database caricato con successo: 3 record da 'database.db'

db> LOAD backup.db
Database caricato con successo: 3 record da 'backup.db'
```

### Comandi di Utilità

#### `INFO`
Mostra informazioni statistiche sul database.

```bash
db> INFO

=== Info Database ===
Record totali: 3
Dimensione tabella: 1024
Carico: 0.29%
======================
```

#### `HELP`
Mostra la lista dei comandi disponibili.

```bash
db> HELP
```

#### `CLEAR` / `CLS`
Pulisce lo schermo.

```bash
db> CLEAR
```

#### `EXIT` / `QUIT`
Esce dal programma con salvataggio automatico.

```bash
db> EXIT

Salvataggio automatico in corso...
Database salvato con successo: 3 record in 'database.db'
Arrivederci!
```

## 🏗️ Architettura

### Strutture Dati

#### Record
```c
typedef struct {
    char key[MAX_KEY_LENGTH];      // Chiave (max 63 char)
    char value[MAX_VALUE_LENGTH];  // Valore (max 255 char)
    time_t timestamp;              // Timestamp Unix
} Record;
```

#### HashTable
```c
typedef struct {
    Record* records[TABLE_SIZE];   // Array di puntatori a record
    int count;                     // Numero di record
} HashTable;
```

### Funzioni Hash

L'implementazione usa la funzione hash djb2:

```c
unsigned int hash_function(const char* key) {
    unsigned int hash = 5381;
    int c;
    while ((c = *key++)) {
        hash = ((hash << 5) + hash) + c; // hash * 33 + c
    }
    return hash % TABLE_SIZE;
}
```

### Gestione delle Collisioni

Viene utilizzato il **Linear Probing**:
- Quando si verifica una collisione, cerca la prossima posizione libera
- Garantisce che tutte le chiavi siano recuperabili
- Semplice ed efficiente per database di piccole-medie dimensioni

### Formato File Binario

```
[int] Numero di record
[Record] Record 1
[Record] Record 2
...
[Record] Record N
```

## 📊 Limitazioni

| Parametro | Valore | Descrizione |
|-----------|--------|-------------|
| `MAX_KEY_LENGTH` | 64 | Lunghezza massima chiave |
| `MAX_VALUE_LENGTH` | 256 | Lunghezza massima valore |
| `TABLE_SIZE` | 1024 | Dimensione hash table |
| Compressione | No | File binario non compresso |
| Concorrenza | No | Single-threaded |

## 🛠️ Makefile

```bash
make          # Compila il progetto
make run      # Compila ed esegui
make clean    # Rimuove tutti i file generati
make reset-db # Rimuove solo il file database
make help     # Mostra i comandi disponibili
```

## 📁 Struttura del Progetto

```
mini-database/
├── database.h      # Header con definizioni e funzioni
├── database.c      # Implementazione del database
├── main.c          # CLI e loop principale
├── Makefile        # Build automation
├── README.md       # Documentazione
└── database.db     # File del database (generato)
```

## 🔍 Esempi di Utilizzo

### Esempio 1: Rubrica Telefonica

```bash
db> SET mario "Mario Rossi, 3331234567"
OK: Chiave 'mario' impostata

db> SET luigi "Luigi Verdi, 3339876543"
OK: Chiave 'luigi' impostata

db> GET mario
Valore: Mario Rossi, 3331234567

db> LIST
=== Database (2 record) ===
Chiave               Valore                         Timestamp
-----               -----                         ---------
mario               Mario Rossi, 3331234567        2026-02-12 10:35:00
luigi               Luigi Verdi, 3339876543        2026-02-12 10:35:02
===========================
```

### Esempio 2: Configurazioni

```bash
db> SET host localhost
OK: Chiave 'host' impostata

db> SET port 8080
OK: Chiave 'port' impostata

db> SET debug true
OK: Chiave 'debug' impostata

db> SAVE config.db
Database salvato con successo: 3 record in 'config.db'
```

### Esempio 3: Session Management

```bash
db> SET user_id 12345
OK: Chiave 'user_id' impostata

db> SET login_time "2026-02-12 10:40:00"
OK: Chiave 'login_time' impostata

db> SET role admin
OK: Chiave 'role' impostata

db> DELETE user_id
OK: Chiave 'user_id' eliminata

db> EXIT
```

## 🎯 Casi d'Uso

- **Configurazioni applicazioni**: Store settings preferenze
- **Cache semplice**: Cache temporanea per applicazioni
- **Session data**: Memorizza dati di sessione
- **Rubriche**: Contatti semplici
- **Todo lists**: Liste di attività
- **Prototyping**: Test rapido di idee

## 🔐 Sicurezza

⚠️ **Attenzione**: Questo database NON è adatto per:
- Dati sensibili (password, token, dati personali)
- Ambienti di produzione
- Applicazioni multi-thread
- Dati critici che richiedono ACID

## 🚧 Possibili Miglioramenti

1. **B-Tree Indexing**: Per ordinamento e range queries
2. **Compressione**: Per ridurre lo spazio su disco
3. **Encryption**: AES per dati sensibili
4. **SQL-like Query Language**: SELECT, WHERE, ORDER BY
5. **Transactions**: Supporto ACID
6. **Multi-threading**: Accesso concorrente
7. **Replication**: Master-slave replication
8. **WAL (Write-Ahead Log)****: Per crash recovery

## 📝 Note di Implementazione

### Hash Table Size
La dimensione della tabella (1024) è ottimale per:
- Piccoli database (< 1000 record)
- Utilizzo memoria limitato
- Performance eccellenti

Per database più grandi, aumentare `TABLE_SIZE`.

### Timestamp
I timestamp sono in formato Unix (time_t), convertiti in stringa leggibile per la visualizzazione.

### Salvataggio Automatico
Il database viene salvato automaticamente all'uscita con il nome predefinito `database.db`.

## 📄 Licenza

Questo progetto è stato creato a scopo educativo. Libero utilizzo e modifica.

## 👨‍💻 Autore

Progetto realizzato per dimostrare:
- Implementazione hash table in C
- Gestione memoria dinamica
- File I/O binario
- Parsing comandi CLI
- Design modulare

---

**Happy Coding! 🚀**

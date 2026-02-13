# C++ Database Engine 🗄️

Un motore di database scritto in C++17 che implementa indicizzazione B-tree, parsing SQL e persistenza su file.

## Caratteristiche 🚀

- **B-tree (ordine 4)** per indicizzazione efficiente
- **SQL Parser** per comandi SQL basilari
- **Persistenza** su file binario
- **Cache** con std::map per accesso rapido
- **Split/Merge** automatico dei nodi in caso di overflow/underflow

## SQL Supportato

```sql
-- Creazione tabella
CREATE TABLE nome_tabella (col1, col2, ...)

-- Inserimento dati
INSERT INTO nome_tabella (val1, val2, ...)

-- Selezione
SELECT * FROM nome_tabella
SELECT * FROM nome_tabella WHERE col1 == value

-- Aggiornamento
UPDATE nome_tabella SET col1 = new_value WHERE id == 1

-- Eliminazione
DELETE FROM nome_tabella WHERE id == 1
```

**Nota:** La prima colonna deve essere un intero, utilizzato come chiave primaria per il B-tree.

## Struttura del Progetto 📁

```
database-engine/
├── btree.h          # Dichiarazioni B-tree
├── btree.cpp        # Implementazione B-tree
├── sql.h            # Dichiarazioni SQL Parser
├── sql.cpp          # Implementazione SQL Parser
├── database.h       # Dichiarazioni Database
├── database.cpp     # Implementazione Database
├── main.cpp         # Menu interattivo e test
└── README.md        # Questo file
```

## Compilazione 🛠️

### Linux/macOS
```bash
g++ -std=c++17 -O2 -o database_engine main.cpp btree.cpp sql.cpp database.cpp
```

### Windows (MinGW)
```bash
g++ -std=c++17 -O2 -o database_engine.exe main.cpp btree.cpp sql.cpp database.cpp
```

### Windows (MSVC)
```bash
cl /EHsc /std:c++17 /O2 main.cpp btree.cpp sql.cpp database.cpp
```

## Esecuzione ▶️

```bash
./database_engine
```

## Menu Interattivo

Il programma offre un menu con le seguenti opzioni:

1. **Esegui comando SQL** - Inserisci query SQL manualmente
2. **Esegui test automatici** - Esegue una serie di test dimostrativi
3. **Salva database su file** - Salva il database su file binario
4. **Carica database da file** - Carica il database da file binario
5. **Visualizza schema** - Mostra tabelle, colonne e numero di righe
6. **Visualizza B-tree** - Mostra la struttura del B-tree di una tabella
0. **Esci** - Termina il programma

## Esempi di Utilizzo

### Esempio 1: Creazione e Inserimento
```sql
CREATE TABLE utenti (id, nome, eta)
INSERT INTO utenti (1, Mario, 25)
INSERT INTO utenti (2, Luigi, 30)
INSERT INTO utenti (3, Anna, 28)
```

### Esempio 2: Selezione
```sql
-- Seleziona tutto
SELECT * FROM utenti

-- Seleziona con filtro
SELECT * FROM utenti WHERE eta == 30
```

### Esempio 3: Aggiornamento
```sql
UPDATE utenti SET eta = 26 WHERE id == 1
```

### Esempio 4: Eliminazione
```sql
DELETE FROM utenti WHERE id == 3
```

## Architettura 🏗️

### B-tree Implementation
- **Ordine:** 4 (massimo 3 chiavi per nodo, 4 figli)
- **Split:** Avviene quando un nodo è pieno prima dell'inserimento
- **Merge:** Avviene quando un nodo ha poche chiavi
- **Complessità:** O(log n) per ricerca, inserimento, eliminazione

### SQL Parser
- **Tokenizer:** Divide l'input SQL in token
- **Parser:** Costruisce un AST semplificato (ParsedSQL struct)
- **Supporto:** CREATE, INSERT, SELECT, UPDATE, DELETE

### Database
- **Tabelle:** Ogni tabella ha il proprio B-tree e cache
- **Persistenza:** Formato binario per efficienza
- **Indicizzazione:** Prima colonna come chiave intera

## Componenti Principali

### BTreeNode
```cpp
struct BTreeNode {
    std::vector<KeyValue> keys;
    std::vector<std::shared_ptr<BTreeNode>> children;
    bool is_leaf;
};
```

### ParsedSQL
```cpp
struct ParsedSQL {
    SQLCommand command;
    std::string table_name;
    std::vector<std::string> columns;
    std::vector<std::string> values;
    WhereCondition where;
};
```

### Table
```cpp
struct Table {
    std::string name;
    std::vector<std::string> columns;
    BTree index;
    std::map<int, Row> rows;
};
```

## Limitazioni ⚠️

- La prima colonna deve essere un intero (chiave primaria)
- Nessun supporto per JOIN
- Nessun supporto per aggregazioni (COUNT, SUM, etc.)
- Nessun supporto per tipi di dati complessi
- WHERE supporta solo operatori di base (==, !=, >, <, >=, <=)
- Non c'è supporto per transazioni
- Non c'è supporto per indici multipli

## Possibili Miglioramenti 🔮

1. Supporto per tipi di dati diversi (VARCHAR, FLOAT, DATE)
2. Indici multipli per tabella
3. Ottimizzazioni delle query (Query Optimizer)
4. Supporto per JOIN
5. Transazioni e ACID properties
6. Undo/Redo log per recovery
7. Query planner e optimizer
8. Compressione dei dati
9. Concurreza (multi-threading)
10. SQL più completo (GROUP BY, HAVING, ORDER BY)

## Test Automatici

Il programma include una suite di test automatici che verifica:

1. ✅ Creazione tabella
2. ✅ Inserimento dati
3. ✅ Selezione dati
4. ✅ Selezione con WHERE
5. ✅ Aggiornamento dati
6. ✅ Eliminazione dati
7. ✅ Struttura B-tree
8. ✅ Salvataggio su file

## File Generati

Eseguendo il programma, verrà creato un file binario:

- `test_db.db` - Database persistente

## Requisiti

- C++17 o superiore
- Compilatore compatibile (g++, clang++, MSVC)
- Standard Library

## Licenza

Questo è un progetto educativo creato per dimostrare i concetti fondamentali di un database engine.

## Autore

Progetto creato come parte del portfolio di progetti C++.

---

Divertiti a esplorare il database engine! 🎉

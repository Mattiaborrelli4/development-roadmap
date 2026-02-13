# Architettura del Database Engine

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        main.cpp                             │
│                    (Menu Interattivo)                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      database.cpp                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  class Database                                     │   │
│  │  - map<string, Table> tables                       │   │
│  │  - execute(sql)                                    │   │
│  │  - create_table()                                  │   │
│  │  - insert_into()                                  │   │
│  │  - select_from()                                  │   │
│  │  - update()                                       │   │
│  │  - delete_from()                                  │   │
│  │  - save() / load()                                │   │
│  └─────────────────────────────────────────────────────┘   │
└────────┬──────────────────────────────────────────────────────┘
         │
         ├─────────────────┬─────────────────┐
         ▼                 ▼                 ▼
    ┌─────────┐     ┌──────────┐     ┌──────────┐
    │ sql.cpp │     │btree.cpp │     │database  │
    │         │     │          │     │  .cpp    │
    └────┬────┘     └────┬─────┘     └──────────┘
         │               │
         ▼               ▼
    ┌─────────┐     ┌──────────┐
    │ sql.h   │     │ btree.h  │
    │         │     │          │
    │ Tokenizer│    │ KeyValue │
    │ Parser   │    │ BTreeNode│
    │ ParsedSQL │   │ BTree    │
    └─────────┘     └──────────┘
```

## Flusso di Esecuzione

### 1. Parsing SQL
```
SQL String → SQLTokenizer → Tokens → SQLParser → ParsedSQL
```

### 2. Esecuzione INSERT
```
ParsedSQL → Database::insert_into()
    ↓
Table → BTree::insert()
    ↓
BTreeNode split (se necessario)
    ↓
Cache update (map<int, Row>)
```

### 3. Esecuzione SELECT
```
ParsedSQL → Database::select_from()
    ↓
Table → Filtraggio WHERE
    ↓
BTree::search() (per chiave) o scansione cache
    ↓
Restituisci vector<Row>
```

## Strutture Dati

### BTreeNode
```
┌─────────────────────────────┐
│ BTreeNode                   │
├─────────────────────────────┤
│ keys: KeyValue[]            │
│ children: BTreeNode*[]      │
│ is_leaf: bool               │
└─────────────────────────────┘
```

### KeyValue
```
┌─────────────────────────────┐
│ KeyValue                   │
├─────────────────────────────┤
│ key: int                   │
│ value: string              │
└─────────────────────────────┘
```

### Table
```
┌─────────────────────────────┐
│ Table                      │
├─────────────────────────────┤
│ name: string               │
│ columns: string[]          │
│ index: BTree              │
│ rows: map<int, Row>       │
└─────────────────────────────┘
```

### Row
```
┌─────────────────────────────┐
│ Row                        │
├─────────────────────────────┤
│ data: map<string, string>  │
│       (col_name → value)    │
└─────────────────────────────┘
```

## Operazioni B-tree

### Insert (O(log n))
```
1. Trova foglia appropriata
2. Se nodo pieno, split
3. Inserisci KeyValue
4. Propaga split verso root se necessario
```

### Search (O(log n))
```
1. Partendo dalla root
2. Cerca chiave nel nodo corrente
3. Se trovata, ritorna
4. Altrimenti, scendi nel figlio appropriato
5. Ripeti fino a foglia o trovata
```

### Delete (O(log n))
```
1. Trova nodo con chiave
2. Rimuovi chiave
3. Se underflow, merge o borrow
4. Propaga modifiche verso root
```

## Persistence

### Format File Binario
```
┌─────────────────────────────────┐
│ Number of Tables (size_t)       │
├─────────────────────────────────┤
│ Table 1:                       │
│  - Name size & name             │
│  - Number of columns            │
│  - Column names                 │
│  - Number of rows               │
│  - Rows (key + data)           │
│  - B-tree serialization         │
├─────────────────────────────────┤
│ Table 2:                       │
│  ...                           │
└─────────────────────────────────┘
```

## SQL Supportato

### CREATE TABLE
```sql
CREATE TABLE table_name (col1, col2, col3, ...)
```
- Crea nuova struttura Table
- Inizializza B-tree vuoto
- Registra colonne

### INSERT
```sql
INSERT INTO table_name (val1, val2, val3, ...)
```
- Prima colonna = chiave (int)
- Altre colonne = values
- Inserisce nel B-tree e nella cache

### SELECT
```sql
SELECT * FROM table_name WHERE col == value
```
- WHERE opzionale
- Supporta: ==, !=, >, <, >=, <=
- Ritorna tutte le colonne

### UPDATE
```sql
UPDATE table_name SET col = new_val WHERE id == key
```
- WHERE obbligatorio per sicurezza
- Aggiorna cache e B-tree

### DELETE
```sql
DELETE FROM table_name WHERE id == key
```
- WHERE obbligatorio per sicurezza
- Rimuove da cache e B-tree

## Limitazioni Architetturali

1. **Single Key:** Solo indice sulla prima colonna
2. **No Transactions:** Nessun supporto ACID
3. **No Joins:** Solo query su singola tabella
4. **Simple Types:** Solo int e string
5. **In-Memory:** Cache intera in RAM

## Possibili Estensioni

### Breve Termine
- [ ] Multi-column indexes
- [ ] ORDER BY clause
- [ ] DISTINCT keyword
- [ ] LIKE operator per stringhe

### Lungo Termine
- [ ] Query optimizer
- [ ] JOIN operations
- [ ] Transactions
- [ ] Write-ahead log
- [ ] MVCC (Multi-Version Concurrency Control)

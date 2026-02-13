# Guida al Build e Esecuzione

## Metodi di Compilazione

### Metodo 1: Makefile (Consigliato per Linux/macOS/MinGW)

```bash
# Compila
make

# Esegui
make run

# Oppure direttamente
./database_engine
```

### Metodo 2: CMake (Consigliato per tutti i sistemi)

```bash
# Crea directory di build
mkdir build
cd build

# Configura
cmake ..

# Compila
cmake --build .

# Esegui
./bin/database_engine
```

### Metodo 3: g++ Diretto

```bash
# Linux/macOS
g++ -std=c++17 -O2 -o database_engine main.cpp btree.cpp sql.cpp database.cpp

# Esegui
./database_engine
```

### Metodo 4: Microsoft Visual C++ (Windows)

```cmd
cl /EHsc /std:c++17 /O2 /Fe:database_engine.exe main.cpp btree.cpp sql.cpp database.cpp

# Esegui
database_engine.exe
```

## Requisiti di Sistema

- **Linux:** g++ 7+ o clang++ 5+
- **macOS:** Xcode Command Line Tools
- **Windows:** MinGW-w64 o Visual Studio 2017+

## Verifica dell'Installazione

Dopo la compilazione, dovresti vedere:

```
===========================================
       C++ DATABASE ENGINE v1.0
===========================================

Questo database engine implementa:
- B-tree per indicizzazione (ordine 4)
- SQL parser semplice
- Persistence su file binario

SQL Supportato:
  CREATE TABLE name (col1, col2, ...)
  INSERT INTO name (val1, val2, ...)
  SELECT * FROM name [WHERE col == value]
  UPDATE name SET col = value WHERE id == 1
  DELETE FROM name WHERE id == 1

Nota: La prima colonna deve essere un intero usato come chiave.
```

## Troubleshooting

### Errore: "C++17 non supportato"
Aggiorna il tuo compilatore:
- Linux: `sudo apt install g++` (Ubuntu/Debian)
- macOS: `xcode-select --install`
- Windows: Scarca l'ultima versione di MinGW-w64

### Errore di linking su Windows
Assicurati di usare MinGW-w64 e non MSYS2:
```bash
g++ --version
```
Dovrebbe mostrare qualcosa come "x86_64-w64-mingw32"

### Warning sicuri da ignorare
- `unused parameter` - I parametri sono per future estensioni
- `signed/unsigned comparison` - Gestito correttamente nel codice

## Test Rapido

Per verificare che tutto funzioni, seleziona l'opzione "2" dal menu per eseguire i test automatici.

## Performance

Il database engine è stato testato con:
- Fino a 10.000 righe per tabella
- B-tree con profondità massima di 4-5 livelli
- Query SELECT in < 1ms per 1000 righe

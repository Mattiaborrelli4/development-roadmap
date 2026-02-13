# Array Dinamico in C 🚀

**Progetto Educativo per Studenti Universitari**

Una implementazione completa e ben commentata di un array dinamico generico in C, progettato specificamente per insegnare la gestione manuale della memoria e i concetti fondamentali della programmazione a basso livello.

## 📋 Indice

- [Descrizione](#descrizione)
- [Concetti Chiave](#concetti-chiave)
- [Struttura del Progetto](#struttura-del-progetto)
- [Compilazione ed Esecuzione](#compilazione-ed-esecuzione)
- [Documentazione del Codice](#documentazione-del-codice)
- [Esempi di Utilizzo](#esempi-di-utilizzo)
- [Gestione della Memoria](#gestione-della-memoria)
- [Troubleshooting](#troubleshooting)

## 🎯 Descrizione

Questo progetto implementa un **array dinamico generico** in C puro, simile all'`ArrayList` di Java o alla `list` di Python. L'array può crescere automaticamente quando necessario, mantenendo allo stesso tempo un controllo completo sulla gestione della memoria.

### Caratteristiche Principali

- ✅ **Generico**: utilizza `void*` per memorizzare qualsiasi tipo di dato
- ✅ **Auto-resizing**: raddoppia la capacità automaticamente quando pieno
- ✅ **Efficiente**: O(1) amortizzato per push/pop
- ✅ **Sicuro**: controlli completi degli errori e validazione degli indici
- ✅ **Educativo**: commenti dettagliati che spiegano ogni concetto

## 🧠 Concetti Chiave

### 1. Puntatori a Void (`void*`)

In C, `void*` è un puntatore "generico" che può puntare a qualsiasi tipo di dato:

```c
int x = 42;
char str[] = "Hello";
float pi = 3.14;

void* ptr;

ptr = &x;    // OK: punta a int
ptr = str;   // OK: punta a char
ptr = &pi;   // OK: punta a float
```

**Nel nostro progetto**: l'array memorizza `void**` (array di puntatori void), permettendo di memorizzare qualsiasi tipo di dato.

### 2. Gestione della Memoria

#### Allocazione (`malloc`)

```c
int* ptr = (int*)malloc(sizeof(int));
if (ptr == NULL) {
    // Gestione errore
}
*ptr = 42;
```

**Punti importanti**:
- `malloc` alloca memoria nell'**heap** (persiste finché non liberata)
- Restituisce `NULL` se fallisce (sempre controllare!)
- Il contenuto della memoria è **non inizializzato**

#### Riallocazione (`realloc`)

```c
void** new_data = realloc(array->data, new_capacity * sizeof(void*));
if (new_data == NULL) {
    // array->data è ancora valido!
    return -1;
}
array->data = new_data;  // OK solo se new_data != NULL
```

**Pericoli di `realloc`**:
- Può spostare l'array in memoria (il puntatore cambia!)
- Se fallisce, restituisce `NULL` ma la memoria vecchia rimane
- **Non fare mai**: `ptr = realloc(ptr, size)` → puoi perdere dati!

#### Deallocazione (`free`)

```c
free(ptr);
ptr = NULL;  // Buona pratica: evita dangling pointers
```

**Regola d'oro**: Ogni `malloc`/`realloc` deve avere un `free` corrispondente!

### 3. Stack vs Heap

| Stack | Heap |
|-------|------|
| Allocazione automatica | Allocazione manuale |
- Variabili locali | - `malloc`/`calloc` |
- Viene liberato automaticamente | - Deve fare `free` |
- Veloce ma limitato | - Più lento ma flessibile |
- Non può crescere dinamicamente | - Può crescere |

### 4. Strategia di Raddoppio

Perché raddoppiamo la capacità invece di aumentare di 1?

```
Con incremento di 1:          Con raddoppio:
1, 2, 3, 4, 5, 6...           1, 2, 4, 8, 16...
↑  ↑  ↑  ↑  ↑  ↑              ↑     ↑     ↑
Rialloca ogni volta!          Rialloca raramente!
```

**Complessità**:
- Senza raddoppio: O(n²) totale per n inserimenti
- Con raddoppio: **O(n)** totale → **O(1) amortizzato**

## 📁 Struttura del Progetto

```
dynamic-array/
├── dynamic_array.h      # Header con definizioni e prototipi
├── dynamic_array.c      # Implementazione completa
├── main.c               # Programma di test con esempi
├── Makefile             # Build automation
└── README.md            # Questo file
```

### File: `dynamic_array.h`

Contiene:
- Definizione della struttura `DynamicArray`
- Prototipi di tutte le funzioni
- Documentazione dettagliata di ogni funzione
- Note educative su memoria e complessità

### File: `dynamic_array.c`

Contiene:
- Implementazione di tutte le funzioni
- Commenti step-by-step di ogni algoritmo
- Spiegazioni dei concetti chiave
- Esempi di correct/incorrect usage

### File: `main.c`

Contiene:
- 5 test completi con diverse casistiche
- Esempi di interi, stringhe, edge cases
- Dimostrazione di memory leak
- Test di performance

## 🔨 Compilazione ed Esecuzione

### Prerequisiti

- Compilatore GCC (o compatibile)
- Make (opzionale ma raccomandato)
- Valgrind per debug memoria (opzionale)

### Compilazione Manuale

```bash
# Compilazione
gcc -Wall -Wextra -std=c99 -c dynamic_array.c -o dynamic_array.o
gcc -Wall -Wextra -std=c99 -c main.c -o main.o

# Linking
gcc -o dynamic_array_test dynamic_array.o main.o

# Esecuzione
./dynamic_array_test
```

### Compilazione con Make

```bash
# Build normale
make

# Build con simboli di debug (per valgrind/gdb)
make debug

# Build con profiling
make profile

# Esegui il programma
make run

# Esegui con valgrind (check memory leaks)
make valgrind

# Esegui con gdb
make gdb

# Pulisci
make clean
```

### Debug con Valgrind

```bash
# Compila in modalità debug
make debug

# Esegui valgrind
make valgrind

# Oppure manualmente
valgrind --leak-check=full \
         --show-leak-kinds=all \
         --track-origins=yes \
         ./dynamic_array_test
```

**Output atteso**:
```
==12345== HEAP SUMMARY:
==12345==     in use at exit: 0 bytes in 0 blocks
==12345==   total heap usage: X allocs, X frees, Y bytes allocated
==12345==
==12345== All heap blocks were freed -- no leaks are possible
```

Se vedi "definitely lost: X bytes", hai un memory leak! 💀

## 📚 Documentazione del Codice

### Struttura `DynamicArray`

```c
typedef struct {
    void **data;      // Array di puntatori void (generico)
    size_t size;      // Numero di elementi attualmente presenti
    size_t capacity;  // Capacità totale allocata
} DynamicArray;
```

### Funzioni Principali

#### Creazione e Distruzione

```c
DynamicArray* dynamic_array_create(size_t initial_capacity);
void dynamic_array_destroy(DynamicArray *array);
```

#### Modifica Array

```c
int dynamic_array_push(DynamicArray *array, void *element);
void* dynamic_array_pop(DynamicArray *array);
int dynamic_array_insert(DynamicArray *array, size_t index, void *element);
void* dynamic_array_remove(DynamicArray *array, size_t index);
```

#### Accesso e Utilità

```c
void* dynamic_array_get(DynamicArray *array, size_t index);
int dynamic_array_set(DynamicArray *array, size_t index, void *element);
size_t dynamic_array_size(DynamicArray *array);
int dynamic_array_is_empty(DynamicArray *array);
int dynamic_array_resize(DynamicArray *array, size_t new_capacity);
void dynamic_array_clear(DynamicArray *array);
```

### Complessità Computazionale

| Operazione | Complessità | Note |
|------------|-------------|------|
| `push` | O(1) amortized | O(n) quando rialloca |
| `pop` | O(1) | Mai rialloca |
| `insert` | O(n) | Deve shiftare elementi |
| `remove` | O(n) | Deve shiftare elementi |
| `get` | O(1) | Accesso diretto |
| `set` | O(1) | Accesso diretto |
| `resize` | O(n) | Può copiare tutti gli elementi |

## 💡 Esempi di Utilizzo

### Esempio 1: Array di Interi

```c
// Crea array con capacità 4
DynamicArray *array = dynamic_array_create(4);

// Aggiungi elementi
for (int i = 0; i < 10; i++) {
    int *num = malloc(sizeof(int));
    *num = i * 10;
    dynamic_array_push(array, num);
}

// Accedi agli elementi
for (size_t i = 0; i < array->size; i++) {
    int *val = (int*)dynamic_array_get(array, i);
    printf("%d ", *val);
}

// Pulizia (IMPORTANTE!)
for (size_t i = 0; i < array->size; i++) {
    free(array->data[i]);  // Libera ogni elemento
}
dynamic_array_destroy(array);  // Libera l'array
```

### Esempio 2: Array di Stringhe

```c
DynamicArray *array = dynamic_array_create(2);

// Aggiungi stringhe
char *str1 = malloc(6);
strcpy(str1, "Hello");
dynamic_array_push(array, str1);

char *str2 = malloc(6);
strcpy(str2, "World");
dynamic_array_push(array, str2);

// Usa le stringhe
for (size_t i = 0; i < array->size; i++) {
    char *s = (char*)array->data[i];
    printf("%s ", s);
}

// Pulizia
for (size_t i = 0; i < array->size; i++) {
    free(array->data[i]);
}
dynamic_array_destroy(array);
```

### Esempio 3: Inserimento e Rimozione

```c
DynamicArray *array = dynamic_array_create(3);

// Push di elementi
int *a = malloc(sizeof(int)); *a = 10;
int *b = malloc(sizeof(int)); *b = 20;
int *c = malloc(sizeof(int)); *c = 30;

dynamic_array_push(array, a);
dynamic_array_push(array, b);
dynamic_array_push(array, c);

// [10, 20, 30]

// Insert in posizione 1
int *x = malloc(sizeof(int)); *x = 99;
dynamic_array_insert(array, 1, x);
// [10, 99, 20, 30]

// Remove da posizione 2
void *removed = dynamic_array_remove(array, 2);
free(removed);  // Libera l'elemento rimosso
// [10, 99, 30]

// Pulisci tutto
for (size_t i = 0; i < array->size; i++) {
    free(array->data[i]);
}
dynamic_array_destroy(array);
```

## ⚠️ Gestione della Memoria

### Errori Comuni

#### 1. Memory Leak - Dimenticare di liberare

```c
// SBAGLIATO ❌
DynamicArray *array = dynamic_array_create(10);
int *num = malloc(sizeof(int));
*num = 42;
dynamic_array_push(array, num);
dynamic_array_destroy(array);  // num è perso! Memory leak!
```

```c
// CORRETTO ✅
DynamicArray *array = dynamic_array_create(10);
int *num = malloc(sizeof(int));
*num = 42;
dynamic_array_push(array, num);

free(num);  // Oppure libera nel loop prima di destroy
dynamic_array_destroy(array);
```

#### 2. Dangling Pointer - Usare dopo free

```c
// SBAGLIATO ❌
int *num = malloc(sizeof(int));
*num = 42;
free(num);
printf("%d", *num);  // Undefined behavior!
```

```c
// CORRETTO ✅
int *num = malloc(sizeof(int));
*num = 42;
printf("%d", *num);
free(num);
num = NULL;  // Buona pratica
```

#### 3. Double Free

```c
// SBAGLIATO ❌
int *num = malloc(sizeof(int));
free(num);
free(num);  // Crash!
```

#### 4. Usare realloc senza check

```c
// SBAGLIATO ❌
array->data = realloc(array->data, new_size);
// Se realloc fallisce → array->data = NULL → DATI PERSI!
```

```c
// CORRETTO ✅
void **new_data = realloc(array->data, new_size);
if (new_data == NULL) {
    // array->data è ancora valido!
    return -1;
}
array->data = new_data;
```

### Checklist per Evitare Memory Leaks

Prima di chiamare `dynamic_array_destroy()`:

```c
// 1. Libera tutti gli elementi allocati
for (size_t i = 0; i < array->size; i++) {
    if (array->data[i] != NULL) {
        free(array->data[i]);
    }
}

// 2. Ora puoi distruggere l'array
dynamic_array_destroy(array);
```

## 🐛 Troubleshooting

### Problema: Segmentation Fault

**Cause comuni**:
- Dereferenziare puntatore `NULL`
- Array out of bounds
- Usare memoria dopo `free()`

**Debug con GDB**:
```bash
make debug
gdb ./dynamic_array_test
(gdb) run
(gdb) backtrace  # Quando crasha
```

### Problema: Memory Leak

**Controlla con Valgrind**:
```bash
make valgrind
# Cerca "definitely lost"
```

**Soluzione**: Assicurati di liberare tutti gli elementi prima di destroy!

### Problema: Valori Casuali/Garbage

**Causa**: Lettura di memoria non inizializzata

**Soluzione**: Inizializza sempre dopo malloc:
```c
int *ptr = malloc(sizeof(int));
*ptr = 0;  // Inizializza!
```

### Problema:realloc() Invalid Pointer

**Causa**: Hai fatto `free()` prima di `realloc()`

**Soluzione**: Non fare free prima di realloc, realloc lo gestisce

## 📖 Risorse Utili

- **Memory in C**: https://www.geeksforgeeks.org/dynamic-memory-allocation-in-c/
- **Pointers**: https://www.cprogramming.com/tutorial/c/lesson6.html
- **Valgrind Guide**: https://valgrind.org/docs/manual/manual.html
- **GDB Guide**: https://sourceware.org/gdb/current/onlinedocs/gdb/

## 👨‍🏫 Per Studenti

### Come Studiare Questo Progetto

1. **Leggi prima il codice** senza i commenti
2. **Rileggi con i commenti** per capire ogni dettaglio
3. **Esegui il programma** e osserva l'output
4. **Usa valgrind** per vedere la memoria in azione
5. **Modifica il codice** e sperimenta
6. **Prova a implementare** nuove funzioni

### Esercizi Suggeriti

1. Implementa `dynamic_array_search()` per trovare un elemento
2. Aggiungi `dynamic_array_sort()` con comparatore generico
3. Implementa `dynamic_array_reverse()` per invertire l'array
4. Crea `dynamic_array_map()` per applicare una funzione a ogni elemento
5. Implementa `dynamic_array_filter()` per filtrare elementi

### Concetti Avanzati da Esplorare

- **Function pointers**: per comparatori e callback generici
- **Memory pools**: allocare blocchi grandi per efficienza
- **Generics in C**: macro X-Macro per tipi diversi
- **Cache locality**: come l'array layout influenza performance

## 📝 Note per l'Autore

Questo progetto è stato creato con scopi educativi. Il codice prioritizza la chiarezza e la didattica rispetto a ottimizzazioni estreme.

**Principi guida**:
- Ogni funzione ha commenti dettagliati
- Gli errori sono gestiti esplicitamente
- Il codice segue lo stile K&R
- Gli esempi sono realistici e ben commentati

## 📄 Licenza

Questo progetto è a scopo educativo. Sei libero di usarlo, modificarlo e distribuirlo per scopi didattici.

---

**Buono studio! 🎓**

Ricorda: capire la memoria è la chiave per padroneggiare C!

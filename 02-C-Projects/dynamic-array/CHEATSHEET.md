# 📋 Quick Reference - Array Dinamico in C

## Comandi Essenziali

### Compilazione
```bash
# Build veloce
make

# Con warning completi
make clean
gcc -Wall -Wextra -std=c99 -o test dynamic_array.c main.c
```

### Debug
```bash
# Valgrind (memory leak check)
make valgrind
# O manualmente:
valgrind --leak-check=full --show-leak-kinds=all ./dynamic_array_test

# GDB (debugger)
make gdb
# O manualmente:
gdb ./dynamic_array_test
```

## Pattern Fondamentali

### ✅ Pattern CORRETTO

```c
// 1. Creazione
DynamicArray *arr = dynamic_array_create(10);
if (arr == NULL) { /* errore */ }

// 2. Push di elementi allocati
int *val = malloc(sizeof(int));
*val = 42;
dynamic_array_push(arr, val);

// 3. Accesso
int *elem = dynamic_array_get(arr, 0);
if (elem != NULL) {
    printf("%d", *elem);
}

// 4. Pulizia (IMPORTANTE!)
for (size_t i = 0; i < arr->size; i++) {
    free(arr->data[i]);  // Libera ogni elemento
}
dynamic_array_destroy(arr);  // Libera l'array
```

### ❌ Pattern SBAGLIATO

```c
// SBAGLIATO 1: Non allocare nello stack
int x = 42;
dynamic_array_push(arr, &x);  // x sarà invalidata!

// SBAGLIATO 2: Non liberare elementi
dynamic_array_destroy(arr);  // Memory leak!

// SBAGLIATO 3: realloc senza check
arr->data = realloc(arr->data, new_size);  // Perdi dati se fallisce!
```

## Memoria - Stack vs Heap

| Stack | Heap |
|-------|------|
| `int x = 5;` | `int *p = malloc(sizeof(int));` |
- Automatico | - Manuale |
- Veloce | - Flessibile |
- Auto-free | - Richiede `free()` |

## Operazioni e Complessità

| Operazione | Codice | Complessità |
|------------|--------|-------------|
| Push | `push(arr, elem)` | O(1)* |
| Pop | `pop(arr)` | O(1) |
| Insert | `insert(arr, i, elem)` | O(n) |
| Remove | `remove(arr, i)` | O(n) |
| Get | `get(arr, i)` | O(1) |
| Set | `set(arr, i, elem)` | O(1) |
| Resize | `resize(arr, cap)` | O(n) |

\*Amortized - occasionally O(n) when resizing

## Raddoppio Capacità

```
Inserimenti:  1  2  3  4  5  6  7  8  9  10 ...
Capacity:     1  2  4  4  4  4  8  8  8  8 ...
Resize:       X  X        X           X

1000 elementi = 10 resize (non 1000!)
```

## Errori Comuni

### 1. Memory Leak
```c
// ❌ Memory leak
int *x = malloc(sizeof(int));
dynamic_array_push(arr, x);
dynamic_array_destroy(arr);  // x perso!

// ✅ Corretto
int *x = malloc(sizeof(int));
dynamic_array_push(arr, x);
free(x);  // O nel loop prima di destroy
dynamic_array_destroy(arr);
```

### 2. Dangling Pointer
```c
// ❌ Use after free
int *x = malloc(sizeof(int));
free(x);
*x = 5;  // CRASH!

// ✅ Corretto
int *x = malloc(sizeof(int));
*x = 5;
printf("%d", *x);
free(x);
x = NULL;
```

### 3. Double Free
```c
// ❌ Double free
int *x = malloc(sizeof(int));
free(x);
free(x);  // CRASH!

// ✅ Corretto
int *x = malloc(sizeof(int));
free(x);
x = NULL;
if (x != NULL) free(x);  // Safe
```

### 4. realloc Non Sicuro
```c
// ❌ Pericoloso
arr->data = realloc(arr->data, size);
// Se fallisce: arr->data = NULL, DATI PERSI!

// ✅ Sicuro
void **new = realloc(arr->data, size);
if (new == NULL) {
    // arr->data ancora valido
    return -1;
}
arr->data = new;
```

## Checklist Pre-Destroy

Prima di `dynamic_array_destroy()`:

```c
// 1. Libera elementi allocati
for (size_t i = 0; i < arr->size; i++) {
    if (arr->data[i] != NULL) {
        free(arr->data[i]);
    }
}

// 2. Libera array
dynamic_array_destroy(arr);
```

## Debug Tips

### Valgrind Output
```
All heap blocks were freed -- no leaks are possible
```
✅ Tutto OK!

```
definitely lost: 24 bytes in 1 blocks
```
❌ Hai un memory leak!

### GDB Commands
```
(gdb) run              # Esegui
(gdb) backtrace        # Stack trace quando crasha
(gdb) print arr->size  # Stampa variabile
(gdb) next             # Prossima riga
(gdb) step             # Entra in funzione
```

## Formule Importanti

### Calcolo Memoria
```c
memoria_struct = sizeof(DynamicArray)        // ~24 bytes
memoria_dati = capacity * sizeof(void*)      // capacity * 8 bytes
memoria_totale = memoria_struct + memoria_dati
```

### Calcolo Resize
```c
if (size >= capacity) {
    new_capacity = capacity * 2;
    resize(new_capacity);
}
```

## Test Rapidi

```c
// Test 1: Array vuoto
assert(dynamic_array_is_empty(arr) == 1);

// Test 2: Push/Pop
int *x = malloc(sizeof(int)); *x = 42;
dynamic_array_push(arr, x);
assert(arr->size == 1);
void *popped = dynamic_array_pop(arr);
assert(*(int*)popped == 42);
free(popped);

// Test 3: Resize
dynamic_array_resize(arr, 100);
assert(arr->capacity == 100);
```

## Struttura in Memoria

```
┌─────────────────────────────────────┐
│  DynamicArray struct (~24 bytes)     │
│  - void** data                       │
│  - size_t size                       │
│  - size_t capacity                   │
└─────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────┐
│  void* data[] (capacity * 8 bytes)  │
│  [ptr0][ptr1][ptr2]...[ptrN]        │
└─────────────────────────────────────┘
     │      │      │
     ▼      ▼      ▼
   ┌───┐ ┌───┐ ┌───┐
   │ A │ │ B │ │ C │  (dati attuali)
   └───┘ └───┘ └───┘
```

## Risorse

- **Codice**: `dynamic_array.c` - implementazione completa
- **Header**: `dynamic_array.h` - documentazione funzioni
- **Test**: `main.c` - esempi completi
- **README**: `README.md` - guida completa

---

**Ricorda**: Ogni `malloc` deve avere un `free`! 💾

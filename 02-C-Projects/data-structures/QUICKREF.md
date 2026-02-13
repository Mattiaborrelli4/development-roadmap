# Guida Rapida - Data Structures Library

## Compilazione Rapida

```bash
# Con Makefile
make

# Senza Makefile
gcc main.c list.c stack.c queue.c hashtable.c -o datastructures

# Esecuzione
./datastructures
```

## Riepilogo Strutture Dati

### 1. Linked List 📋
**File:** `list.h`, `list.c`
**Tipo:** Singly linked list
**Implementazione:** Struct + Pointer + Malloc

```c
LinkedList* list = list_create();
list_insert(list, 10);        // O(1)
list_append(list, 20);        // O(n)
list_search(list, 10);        // O(n)
list_delete(list, 10);        // O(n)
list_print(list);
list_destroy(list);
```

### 2. Stack 📚
**File:** `stack.h`, `stack.c`
**Tipo:** LIFO (Last In, First Out)
**Implementazione:** Array fisso (max 100 elementi)

```c
Stack* stack = stack_create();
stack_push(stack, 10);        // O(1)
stack_peek(stack);            // O(1)
stack_pop(stack);             // O(1)
stack_is_empty(stack);        // O(1)
stack_print(stack);
stack_destroy(stack);
```

### 3. Queue 🚶
**File:** `queue.h`, `queue.c`
**Tipo:** FIFO (First In, First Out)
**Implementazione:** Array circolare (max 100 elementi)

```c
Queue* queue = queue_create();
queue_enqueue(queue, 10);     // O(1)
queue_front(queue);           // O(1)
queue_dequeue(queue);         // O(1)
queue_is_empty(queue);        // O(1)
queue_print(queue);
queue_destroy(queue);
```

### 4. Hash Table 🔑
**File:** `hashtable.h`, `hashtable.c`
**Tipo:** Key-Value store
**Implementazione:** Array di linked lists (Chaining)

```c
HashTable* table = hashtable_create();
hashtable_insert(table, 10, 100);    // O(1) avg, O(n) worst
hashtable_get(table, 10);            // O(1) avg, O(n) worst
hashtable_contains(table, 10);       // O(1) avg, O(n) worst
hashtable_remove(table, 10);         // O(1) avg, O(n) worst
hashtable_print(table);
hashtable_destroy(table);
```

## Statistiche Progetto

| Metrica | Valore |
|---------|-------|
| **Totale righe di codice** | 1,225 |
| **Righe di codice C** | ~495 |
| **Righe di header** | ~345 |
| **Documentazione** | ~215 |
| **File sorgente** | 8 (.c + .h) |
| **Strutture dati** | 4 |
| **Funzioni totali** | ~30 |

## Concetti Chiave Dimostrati

✅ **Struct e Pointer**
- Definizione di nodi con struct
- Puntatori `next` per collegamenti
- Puntatori a struct per head, top, front, rear

✅ **Allocazione Dinamica**
- `malloc()` per allocare nodi e strutture
- Controllo errori su allocazione
- `free()` per prevenire memory leak

✅ **Gestione della Memoria**
- Funzioni `destroy()` per ogni struttura
- Liberazione corretta di tutta la memoria
- No memory leak

✅ **Data Structures**
- Linked List: traversale e manipolazione nodi
- Stack: gestione LIFO con array
- Queue: gestione FIFO con array circolare
- Hash Table: hashing e chaining per collisioni

## Complessità Operazioni

| Operazione | Linked List | Stack | Queue | Hash Table |
|-----------|-------------|-------|-------|------------|
| **Inserimento** | O(1)* / O(n)** | O(1) | O(1) | O(1)*** |
| **Cancellazione** | O(n) | O(1) | O(1) | O(1)*** |
| **Ricerca** | O(n) | O(1) | O(1) | O(1)*** |
| **Accesso** | O(n) | O(1) | O(1) | O(1)*** |

* In testa
** In coda
*** Caso medio, caso peggiore O(n)

## Test Coverage

Il file `main.c` include test completi per:
- ✅ Inserimento elementi
- ✅ Cancellazione elementi
- ✅ Ricerca elementi
- ✅ Casi edge (vuoto, pieno, ecc.)
- ✅ Gestione errori
- ✅ Comportamento circolare (Queue)
- ✅ Gestione collisioni (Hash Table)

## Prossimi Passi Sugeriti

1. **Linked List:** Aggiungi doppia linkage, iteratori
2. **Stack/Queue:** Implementazione con linked list
3. **Hash Table:** Resizing dinamico, funzioni hash avanzate
4. **Testing:** Unit test framework
5. **Benchmark:** Performance testing

---

**Autore:** Matti
**Anno:** 2026
**Linguaggio:** C (C99)

# Data Structures Library in C

Libreria completa di strutture dati implementate da zero in linguaggio C.

## Autore
Matti - 2026

## Descrizione
Questo progetto implementa 4 strutture dati fondamentali da zero, utilizzando struct, pointer e allocazione dinamica della memoria con `malloc`.

## Strutture Dati Implementate

### 1. Linked List (Singly)
Una lista collegata singola dove ogni nodo contiene un dato e un puntatore al nodo successivo.

**Operazioni supportate:**
- `list_create()` - Crea una nuova lista vuota
- `list_insert(list, data)` - Inserisce un elemento all'inizio
- `list_append(list, data)` - Aggiunge un elemento alla fine
- `list_delete(list, data)` - Cancella un elemento specifico
- `list_search(list, data)` - Cerca un elemento
- `list_print(list)` - Stampa la lista
- `list_destroy(list)` - Libera la memoria

**Caratteristiche tecniche:**
- Struct `Node` con campo `data` e puntatore `next`
- Allocazione dinamica con `malloc` per ogni nodo
- Complessità: O(n) per ricerca/cancellazione, O(1) per inserimento in testa

### 2. Stack (Array-based)
Uno stack LIFO (Last In, First Out) implementato con array fisso.

**Operazioni supportate:**
- `stack_create()` - Crea un nuovo stack vuoto
- `stack_push(stack, value)` - Aggiunge un elemento in cima
- `stack_pop(stack)` - Rimuove e restituisce l'elemento in cima
- `stack_peek(stack)` - Restituisce l'elemento in cima senza rimuoverlo
- `stack_is_empty(stack)` - Verifica se lo stack è vuoto
- `stack_is_full(stack)` - Verifica se lo stack è pieno
- `stack_size(stack)` - Restituisce il numero di elementi
- `stack_print(stack)` - Stampa lo stack
- `stack_destroy(stack)` - Libera la memoria

**Caratteristiche tecniche:**
- Array fisso di dimensione `MAX_STACK_SIZE = 100`
- Puntatore `top` che indica l'elemento in cima
- Complessità: O(1) per tutte le operazioni

### 3. Queue (Array-based Circular)
Una coda FIFO (First In, First Out) implementata con array circolare.

**Operazioni supportate:**
- `queue_create()` - Crea una nuova queue vuota
- `queue_enqueue(queue, value)` - Aggiunge un elemento alla fine
- `queue_dequeue(queue)` - Rimuove e restituisce l'elemento frontale
- `queue_front(queue)` - Restituisce l'elemento frontale senza rimuoverlo
- `queue_is_empty(queue)` - Verifica se la queue è vuota
- `queue_is_full(queue)` - Verifica se la queue è piena
- `queue_size(queue)` - Restituisce il numero di elementi
- `queue_print(queue)` - Stampa la queue
- `queue_destroy(queue)` - Libera la memoria

**Caratteristiche tecniche:**
- Array circolare di dimensione `MAX_QUEUE_SIZE = 100`
- Puntatori `front` e `rear` per gestire gli estremi
- Utilizzo dell'operatore modulo per il comportamento circolare
- Complessità: O(1) per tutte le operazioni

### 4. Hash Table
Tabella hash con gestione delle collisioni tramite chaining.

**Operazioni supportate:**
- `hashtable_create()` - Crea una nuova hash table vuota
- `hashtable_insert(table, key, value)` - Inserisce una coppia key-value
- `hashtable_get(table, key)` - Ottiene il valore associato a una chiave
- `hashtable_remove(table, key)` - Rimuove una coppia key-value
- `hashtable_contains(table, key)` - Verifica se una chiave esiste
- `hashtable_print(table)` - Stampa la tabella
- `hashtable_destroy(table)` - Libera la memoria

**Caratteristiche tecniche:**
- Array di `TABLE_SIZE = 10` linked lists (chaining)
- Funzione di hash: `hash(key) = abs(key) % TABLE_SIZE`
- Gestione delle collisioni tramite linked lists
- Complessità media: O(1), caso peggiore: O(n)

## Compilazione

### Compilare il programma di test:
```bash
gcc main.c list.c stack.c queue.c hashtable.c -o datastructures
```

### Eseguire il programma:
```bash
./datastructures
```

## Struttura dei File

```
data-structures/
├── list.h           # Header per Linked List
├── list.c           # Implementazione Linked List
├── stack.h          # Header per Stack
├── stack.c          # Implementazione Stack
├── queue.h          # Header per Queue
├── queue.c          # Implementazione Queue
├── hashtable.h      # Header per Hash Table
├── hashtable.c      # Implementazione Hash Table
├── main.c           # Programma di test
└── README.md        # Questa documentazione
```

## Esempi di Utilizzo

### Linked List
```c
LinkedList* list = list_create();
list_insert(list, 10);
list_append(list, 20);
list_print(list);
if (list_search(list, 10)) {
    printf("Trovato!\n");
}
list_delete(list, 10);
list_destroy(list);
```

### Stack
```c
Stack* stack = stack_create();
stack_push(stack, 10);
stack_push(stack, 20);
printf("Top: %d\n", stack_peek(stack));
int value = stack_pop(stack);
stack_destroy(stack);
```

### Queue
```c
Queue* queue = queue_create();
queue_enqueue(queue, 10);
queue_enqueue(queue, 20);
printf("Front: %d\n", queue_front(queue));
int value = queue_dequeue(queue);
queue_destroy(queue);
```

### Hash Table
```c
HashTable* table = hashtable_create();
hashtable_insert(table, 10, 100);
if (hashtable_contains(table, 10)) {
    printf("Value: %d\n", hashtable_get(table, 10));
}
hashtable_remove(table, 10);
hashtable_destroy(table);
```

## Concetti Chiave

### Struct e Pointer
Tutte le strutture dati utilizzano struct per definire i nodi e i container:
- Ogni nodo ha un puntatore `next` per collegarsi al nodo successivo
- I container mantengono puntatori ai nodi (head, top, front, rear)

### Allocazione Dinamica
- `malloc()` utilizzato per allocare memoria per nodi e strutture
- `free()` utilizzato per liberare la memoria e prevenire memory leak
- Controllo errori su ogni allocazione

### Memory Management
Ogni struttura dati fornisce una funzione `destroy()` che:
- Libera tutti i nodi/elementi
- Libera la struttura principale
- Previene memory leak

## Note Tecniche

### Linked List
- Inserimento in testa: O(1)
- Inserimento in coda: O(n)
- Cancellazione: O(n)
- Ricerca: O(n)

### Stack
- Tutte le operazioni: O(1)
- Limite massimo: 100 elementi
- Overflow se si supera il limite

### Queue
- Tutte le operazioni: O(1)
- Limite massimo: 100 elementi
- Comportamento circolare ottimizza l'uso della memoria

### Hash Table
- Inserimento: O(1) medio, O(n) peggiore
- Ricerca: O(1) medio, O(n) peggiore
- Cancellazione: O(1) medio, O(n) peggiore
- Load factor ottimale: n/TABLE_SIZE < 1

## Possibili Miglioramenti

1. **Linked List**: Aggiungere iteratori, inversione lista, rilevamento cicli
2. **Stack**: Implementazione con linked list per rimuovere il limite di dimensione
3. **Queue**: Implementazione con linked list, gestione dinamica della dimensione
4. **Hash Table**: Funzioni di hash più avanzate, resizing dinamico, key-value pairs separati

## Licenza
Progetto educativo creato per dimostrare la comprensione delle strutture dati in C.

---

**Creato con passione per il coding e l'apprendimento!**

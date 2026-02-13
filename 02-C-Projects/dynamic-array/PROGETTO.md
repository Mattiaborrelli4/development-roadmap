# 📚 Riepilogo Progetto: Array Dinamico in C

## Panoramica del Progetto

Questo progetto implementa un **Array Dinamico Generico** in C puro, progettato come risorsa educativa per studenti universitari che imparano la gestione della memoria.

## 📁 Struttura dei File

```
dynamic-array/
│
├── 📄 README.md              (14 KB)
│   └── Guida completa del progetto con esempi
│
├── 📄 CHEATSHEET.md          (6 KB)
│   └── Quick reference per comandi e pattern comuni
│
├── 📄 ARCHITECTURE.md        (11 KB)
│   └── Diagrammi visuali di memoria e operazioni
│
├── 📄 dynamic_array.h         (7.5 KB)
│   └── Header con definizioni e documentazione completa
│
├── 📄 dynamic_array.c         (19 KB)
│   └── Implementazione con commenti educativi dettagliati
│
├── 📄 main.c                  (15 KB)
│   └── 5 test completi: interi, stringhe, edge cases, performance
│
├── 📄 Makefile                (3.7 KB)
│   └── Build automation con target debug, valgrind, gdb
│
└── 📄 .gitignore
    └── Esclusioni per compilati e file di debug
```

## 🎯 Obiettivi Educativi

### Concetti Principali
1. **Gestione Manuale della Memoria**
   - `malloc()` - allocazione dinamica
   - `realloc()` - riallocazione con tricks
   - `free()` - deallocazione corretta

2. **Puntatori Void***
   - Generic type per qualsiasi dato
   - Cast corretto e dereferenziazione
   - Pericoli di type punning

3. **Stack vs Heap**
   - Differenze fondamentali
   - Quando usare quale
   - Lifecycle delle variabili

4. **Strategie di Riallocazione**
   - Raddoppio della capacità
   - Amortized analysis
   - O(1) vs O(n) operations

5. **Memory Management**
   - Memory leaks
   - Dangling pointers
   - Double free errors

## 🧪 Test Inclusi

Il file `main.c` include 5 suite di test complete:

1. **TEST 1: Interi**
   - Push di 6 elementi (trigger resize)
   - Pop e verifica contenuto
   - Insert in posizione
   - Remove da posizione
   - Pulizia corretta memoria

2. **TEST 2: Stringhe**
   - Gestione memoria complessa
   - Ricerca e modifica elementi
   - Stringhe allocate dinamicamente

3. **TEST 3: Memory Leak Demo**
   - Dimostrazione pratica del leak
   - Correzione con libero corretto
   - Spiegazione dettagliata

4. **TEST 4: Edge Cases**
   - Array vuoto
   - Indici non validi
   - Insert alla fine
   - Resize manuale
   - Clear mantening capacity

5. **TEST 5: Performance Growth**
   - 1000 inserimenti
   - Dimostrazione raddoppio (10 vs 1000 resize)
   - Statistiche efficienza

## 📊 Statistiche del Codice

### dynamic_array.c
- **Righe totali**: ~600 righe
- **Commenti**: ~40% del codice
- **Funzioni implementate**: 10
- **Righe per funzione**: Media 40-60 righe

### Funzioni Implementate
```c
// Gestione base
DynamicArray* dynamic_array_create(size_t initial_capacity);
void dynamic_array_destroy(DynamicArray *array);

// Modifica array
int dynamic_array_push(DynamicArray *array, void *element);
void* dynamic_array_pop(DynamicArray *array);
int dynamic_array_insert(DynamicArray *array, size_t index, void *element);
void* dynamic_array_remove(DynamicArray *array, size_t index);

// Accesso
void* dynamic_array_get(DynamicArray *array, size_t index);
int dynamic_array_set(DynamicArray *array, size_t index, void *element);

// Utilità
size_t dynamic_array_size(DynamicArray *array);
int dynamic_array_is_empty(DynamicArray *array);
int dynamic_array_resize(DynamicArray *array, size_t new_capacity);
void dynamic_array_clear(DynamicArray *array);
void dynamic_array_print_info(DynamicArray *array);
```

## 🚀 Come Usare il Progetto

### Compilazione Veloce
```bash
cd dynamic-array
make
./dynamic_array_test
```

### Build con Debug
```bash
make debug
valgrind --leak-check=full ./dynamic_array_test
```

### Lettura Ordinata Suggerita

1. **Prima lettura**: `README.md`
   - Panoramica completa del progetto

2. **Seconda lettura**: `dynamic_array.h`
   - Interfaccia e contratto delle funzioni

3. **Terza lettura**: `dynamic_array.c`
   - Implementazione con commenti dettagliati

4. **Quarta lettura**: `ARCHITECTURE.md`
   - Visualizza memoria e operazioni

5. **Quinta lettura**: `CHEATSHEET.md`
   - Quick reference per uso pratico

6. **Pratica**: `main.c`
   - Esegui e modifica i test

## 🎓 Cosa Imparerai

Dopo aver studiato questo progetto, saprai:

### Competenze Tecniche
- ✅ Allocare e liberare memoria correttamente
- ✅ Usare realloc in modo sicuro
- ✅ Implementare strutture dati generiche
- ✅ Capire la differenza stack/heap
- ✅ Evitare memory leak comuni
- ✅ Debuggare con valgrind e gdb

### Competenze Teoriche
- ✅ Amortized analysis (O(1) amortized)
- ✅ Trade-off spazio/tempo
- ✅ Cache locality e memory layout
- ✅ Strategie di crescita (doubling vs linear)

### Best Practices
- ✅ Defensive programming (check NULL)
- ✅ Documentazione completa
- ✅ Separazione interfaccia/implementazione
- ✅ Test-driven development

## 🐛 Debug e Testing

### Strumenti Utilizzati
- **GCC**: Compilatore con warning (`-Wall -Wextra`)
- **Valgrind**: Memory leak detection
- **GDB**: Step-by-step debugging
- **Make**: Build automation

### Esempio Output Valgrind
```
==12345== HEAP SUMMARY:
==12345==     in use at exit: 0 bytes in 0 blocks
==12345==   total heap usage: X allocs, X frees, Y bytes allocated
==12345==
==12345== All heap blocks were freed -- no leaks are possible
```

## 📈 Performance

### Benchmark: 1000 Inserimenti
```
Senza raddoppio: 1000 resize (ipotetico)
Con raddoppio:   10 resize

Efficienza:      97.7% (1000 / 1024 capacity)
```

### Complessità Computazionale
| Operazione | Tempo | Spazio |
|------------|-------|--------|
| push | O(1)* | O(1) |
| pop | O(1) | O(1) |
| insert | O(n) | O(1) |
| remove | O(n) | O(1) |
| get | O(1) | O(1) |
| resize | O(n) | O(n) |

\*Amortized

## 💡 Suggerimenti per Studenti

1. **Non copiare-incollare**: Scrivi il codice a mano
2. **Disegna diagrammi**: Visualizza la memoria
3. **Usa valgrind**: Controlla ogni modifica
4. **Sperimenta**: Modifica e prova
5. **Insegna**: Spiega a qualcun altro

## 🔄 Estensioni Possibili

Ideas per continuare lo studio:
1. Implementare sort (qsort con comparatore)
2. Aggiungere iteratori
3. Implementare map/filter/reduce
4. Creare versioni type-safe con macro
5. Implementare memory pooling
6. Aggiungere persistenza (save/load)

## 📖 Risorse Correlate

- **K&R C**: Capitolo 5 (Pointers and Arrays)
- **CS50**: Week 4 (Memory)
- **GeeksforGeeks**: Dynamic Memory Allocation in C
- **Valgrind Docs**: Quick Start Guide

## ✅ Checklist di Completamento

Quando hai finito di studiare questo progetto, dovresti:

- [ ] Capire la differenza tra stack e heap
- [ ] Sapere usare malloc, realloc, free
- [ ] Capire i memory leak e come evitarli
- [ ] Sapere perché raddoppiamo la capacità
- [ ] Essere in grado di debuggare con valgrind
- [ ] Capire i puntatori void* e i cast
- [ ] Poter implementare una struttura dati simile
- [ ] Conoscere la complessità delle operazioni

## 📞 Supporto

Per domande o chiarimenti:
1. Leggi i commenti nel codice
2. Consulta README.md per spiegazioni
3. Guarda ARCHITECTURE.md per diagrammi
4. Usa CHEATSHEET.md come reference

---

**Buono studio e buon coding! 🎓**

Ricorda: In C, la memoria è tua responsabilità!

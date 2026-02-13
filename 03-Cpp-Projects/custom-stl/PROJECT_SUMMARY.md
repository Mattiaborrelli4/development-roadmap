# Custom STL Containers - Sommario Progetto

## 📦 Panoramica

Progetto C++17 che implementa container STL personalizzati da zero, dimostrando competenza avanzata in:
- Template metaprogramming
- Memory management RAII
- Move semantics e perfect forwarding
- Iterator design patterns
- Algoritmi generici

## 📁 File del Progetto

### Codice Sorgente
| File | Righe | Descrizione |
|------|-------|-------------|
| `vector.h` | 72 | Dichiarazione classe MyVector<T> |
| `vector.tpp` | 213 | Implementazione MyVector (include header) |
| `list.h` | 165 | Dichiarazione classe MyLinkedList<T> + iteratori |
| `list.tpp` | 259 | Implementazione MyLinkedList |
| `algorithms.h` | 170 | Algoritmi STL (my_find, my_sort, my_copy, etc.) |
| `main.cpp` | 470 | Test suite completa con 40+ test |
| **Totale Codice** | **1,349** | Righe di codice C++ |

### Documentazione
| File | Descrizione |
|------|-------------|
| `README.md` | Documentazione completa in italiano |
| `ARCHITECTURE.md` | Diagrammi e architettura dettagliata |
| `QUICKSTART.md` | Guida rapida con esempi pratici |
| `PROJECT_SUMMARY.md` | Questo file |

### Build System
| File | Descrizione |
|------|-------------|
| `Makefile` | Build automation con target debug/clean |

## ✅ Funzionalità Implementate

### MyVector<T>
- [x] Template class con supporto qualsiasi tipo
- [x] Dynamic array con new/delete e placement new
- [x] Random access con operator[]
- [x] Bounds checking con at()
- [x] Iteratori (begin, end, cbegin, cend)
- [x] Const correctness completo
- [x] Capacity management (reserve, resize, shrink_to_fit)
- [x] Modifiers (push_back, pop_back, emplace_back, clear)
- [x] Rule of Five (copy/move constructor/assignment)
- [x] Range-based for loop support

### MyLinkedList<T>
- [x] Doubly linked list con sentinelle
- [x] Node<T> struttura interna
- [x] Bidirectional iterator class
- [x] Const iterator class
- [x] Operator overloading (++/--/*/->/==/!=)
- [x] push_back/push_front (copy e move)
- [x] pop_back/pop_front
- [x] insert/erase con iteratori
- [x] erase(range)
- [x] Rule of Five
- [x] Range-based for loop support

### Algoritmi
- [x] `my_find` - Ricerca lineare
- [x] `my_find_if` - Ricerca con predicato
- [x] `my_copy` - Copia range
- [x] `my_move` - Move semantico
- [x] `my_sort` - QuickSort ricorsivo
- [x] `my_sort` con comparatore custom
- [x] `my_fill` - Riempimento
- [x] `my_equal` - Confronto range
- [x] `my_count` - Conteggio occorrenze
- [x] `my_accumulate` - Riduzione (fold)

## 🧪 Test Suite

### Categorie di Test
1. **MyVector Basic** (7 test)
   - Costruttore, push_back, operator[], at, front/back, pop_back, initializer list

2. **MyVector Iterators** (3 test)
   - begin/end, range-based for, const iterator

3. **MyVector Copy/Move** (4 test)
   - Copy constructor, copy assignment, move constructor, move assignment

4. **MyVector Capacity** (4 test)
   - reserve, resize, shrink_to_fit, clear

5. **MyVector Strings** (3 test)
   - push_back, emplace_back, move semantics

6. **MyLinkedList Basic** (5 test)
   - Costruttore, push_back/front, front/back, pop_back/front

7. **MyLinkedList Iterators** (5 test)
   - begin/end, operator++, operator--, operator*/->, operator==/!=

8. **MyLinkedList Insert/Erase** (3 test)
   - insert, erase, erase(range)

9. **MyLinkedList Copy/Move** (4 test)
   - Copy constructor, copy assignment, move constructor, move assignment

10. **Algorithms Find** (3 test)
    - my_find, elemento non trovato, my_find_if

11. **Algorithms Sort** (2 test)
    - Ordinamento crescente, ordinamento decrescente

12. **Algorithms Copy** (2 test)
    - my_copy, copia profonda

13. **Algorithms Fill** (1 test)
    - my_fill

14. **Algorithms Count** (1 test)
    - my_count

15. **Algorithms Accumulate** (2 test)
    - Somma, init differente

16. **Algorithms Equal** (2 test)
    - Vettori uguali, vettori diversi

17. **Comprehensive Example** (1 test)
    - Esempio completo reale

**Totale: 52 test, tutti passing ✓**

## 🏗 Architettura

### Class Hierarchy
```
mystl::
├── MyVector<T>
│   ├── iterator (T*)
│   └── const_iterator (const T*)
├── MyLinkedList<T>
│   ├── Node<T> (private)
│   ├── iterator
│   └── const_iterator
└── Algorithms (funzioni template)
```

### Memory Management
- **MyVector**: Dynamic array con raddoppio capacity
- **MyLinkedList**: Singola allocazione per nodo
- **RAII**: Destructor pulisce automaticamente
- **Exception Safety**: Strong guarantee per copy operations

### Iterator Categories
- **MyVector**: RandomAccessIterator
- **MyLinkedList**: BidirectionalIterator

## 📊 Complessità

| Operazione | MyVector | MyLinkedList | Note |
|------------|----------|--------------|------|
| push_back | O(1)* | O(1) | *amortized |
| push_front | O(n) | O(1) | |
| pop_back | O(1) | O(1) | |
| pop_front | O(n) | O(1) | |
| operator[] | O(1) | N/A | |
| insert | O(n) | O(1) | con iteratore |
| erase | O(n) | O(1) | con iteratore |
| find | O(n) | O(n) | |
| sort | O(n log n) | N/A | inefficiente |

## 🛠 Tecnologiche

### C++ Features Utilizzate
- **C++17 Standard**
- **Templates**: `template<typename T>`, variadic `template<typename... Args>`
- **Placement new**: `new (address) T(args)`
- **Perfect forwarding**: `std::forward<Args>(args)...`
- **Move semantics**: `std::move`, rvalue references `T&&`
- **Const correctness**: `const T&`, `const` member functions
- **Operator overloading**: `[]`, `=`, `==`, `!=`, `++`, `--`, `*`, `->`
- **Rule of Five**: Destructor, copy/move ctor/assignment
- **Range-based for**: `for (const auto& x : container)`
- **Initializer lists**: `std::initializer_list<T>`
- **Iterator traits**: `std::iterator_traits<It>`

### Design Patterns
- **Iterator Pattern**: Accesso uniforme ai container
- **RAII**: Resource Acquisition Is Initialization
- **Copy-and-Swap Idiom**: Strong exception safety
- **Sentinel Pattern**: Dummy nodes per semplificare edge cases

## 📈 Statistiche Progetto

```yaml
Linguaggio: C++17
Standard: ISO C++17
Header files: 6
Source files: 1
Documentation: 4 file
Total lines of code: 1,349
Total lines of documentation: ~500
Test cases: 52
Compilation warnings: 0 (1 minor unused variable)
Memory leaks: 0
Test pass rate: 100%
```

## 🎯 Obiettivi di Apprendimento

Questo progetto dimostra competenza in:

1. **Template Programming**
   - Classi template
   - Funzioni template
   - Template con parametri multipli
   - Variadic templates

2. **Memory Management**
   - Allocazione dinamica con new/delete
   - Placement new
   - RAII
   - Exception safety

3. **C++ Idioms**
   - Rule of Five
   - Copy-and-swap
   - Perfect forwarding
   - Move semantics

4. **STL Principles**
   - Container concepts
   - Iterator categories
   - Algorithm conventions
   - Const correctness

5. **Code Quality**
   - Clean code
   - Documentazione completa
   - Test suite
   - Error handling

## 🚀 Quick Start

```bash
# Compilazione
cd custom-stl/
g++ -std=c++17 -Wall -O2 main.cpp -o custom_stl

# Esecuzione
./custom_stl

# Oppure con Makefile
make
make run
```

## 📚 Risorse di Studio

### File da Leggere (In Ordine)
1. `QUICKSTART.md` - Inizia qui per esempi pratici
2. `README.md` - Documentazione completa
3. `ARCHITECTURE.md` - Architettura dettagliata
4. `main.cpp` - Vedi gli esempi di utilizzo

### Codice da Esplorare
1. `vector.h` + `vector.tpp` - Capire dynamic array
2. `list.h` + `list.tpp` - Capire linked list + iteratori
3. `algorithms.h` - Capire algoritmi generici

## 🎓 Possibili Estensioni

### Container Extra
- [ ] MyStack<T> (adapter su MyVector)
- [ ] MyQueue<T> (adapter su MyLinkedList)
- [ ] MyDeque<T> (double-ended queue)
- [ ] MyHashSet<T> (hash table)
- [ ] MyMap<K,V> (red-black tree)

### Algoritmi Extra
- [ ] my_binary_search
- [ ] my_merge_sort
- [ ] my_heap_sort
- [ ] my_lower_bound/upper_bound
- [ ] my_reverse
- [ ] my_unique

### Features Extra
- [ ] Allocator support template parameter
- [ ] Exception specifications (noexcept)
- [ ] constexpr functions dove possibile
- [ ] More iterator categories (forward, output)
- [ ] Range checking in debug mode

## ✨ Checklist Completamento

- [x] MyVector<T> implementation
- [x] MyVector iterators (begin, end, cbegin, cend)
- [x] MyVector modifiers (push, pop, emplace, clear)
- [x] MyVector capacity (reserve, resize, shrink_to_fit)
- [x] MyVector Rule of Five
- [x] MyVector operator overloading
- [x] MyLinkedList<T> implementation
- [x] MyLinkedList Node structure
- [x] MyLinkedList bidirectional iterator
- [x] MyLinkedList const iterator
- [x] MyLinkedList insert/erase
- [x] MyLinkedList Rule of Five
- [x] my_sort algorithm
- [x] my_find algorithm
- [x] my_copy algorithm
- [x] my_find_if, my_move, my_fill
- [x] my_equal, my_count, my_accumulate
- [x] Move semantics implementation
- [x] Const correctness
- [x] Exception safety
- [x] Test suite completa
- [x] Documentazione italiana
- [x] Diagrammi architetturali
- [x] Quick start guide
- [x] Makefile
- [x] Tutti i test passano

## 📝 Note Importanti

### Compile-Time vs Runtime
- Tutti i template sono risolti a compile-time
- Type safety garantito dal compilatore
- Nessun overhead runtime per i template

### Memory Safety
- Nessun memory leak (verificato con test)
- RAII garantisce cleanup
- Exception safety nelle copy operations

### Performance
- MyVector: Cache friendly, ottimo per access random
- MyLinkedList: Ottimo per insert/erase frequenti
- Algoritmi: Generici, zero overhead astrazione

## 🏆 Risultato Finale

Un progetto completo che dimostra:
- ✅ Profonda comprensione di C++ moderno
- ✅ Capacità di implementare container STL
- ✅ Competenza in template programming
- � Buone pratiche di software engineering
- ✅ Codice ben documentato e testato

**Status**: ✅ PROGETTO COMPLETO E FUNZIONANTE

---

Creato per portfolio personale - Dimostrazione competenze C++ avanzato.

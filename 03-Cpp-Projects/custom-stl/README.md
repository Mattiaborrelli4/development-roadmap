# Custom STL Containers - C++

Implementazione personalizzata di container STL in C++17 da zero, dimostrando una profonda comprensione di template, memoria dinamica, iteratori e move semantics.

## 📋 Indice

- [Caratteristiche](#caratteristiche)
- [Struttura del Progetto](#struttura-del-progetto)
- [Container Implementati](#container-implementati)
- [Algoritmi Implementati](#algoritmi-implementati)
- [Tecnologie Utilizzate](#tecnologie-utilizzate)
- [Compilazione ed Esecuzione](#compilazione-ed-esecuzione)
- [Esempi di Utilizzo](#esempi-di-utilizzo)
- [Concetti Chiave](#concetti-chiave)

## ✨ Caratteristiche

### MyVector<T>
- **Template class** con supporto per qualsiasi tipo
- **Gestione memoria dinamica** con `new`/`delete` e placement new
- **Move semantics** completi con `std::move`
- **Const correctness** in tutti i metodi
- **Operator overloading**: `[]`, `=`, `==`, `!=`
- **Iterator** support per range-based for loops
- **Capacity management**: `reserve()`, `resize()`, `shrink_to_fit()`
- **Modifiers**: `push_back()`, `pop_back()`, `emplace_back()`, `clear()`

### MyLinkedList<T>
- **Doubly linked list** con sentinelle
- **Bidirectional iterator** con operator overloading completo
- **Node<T>** struttura interna con puntatori prev/next
- **Insert/Erase** con iteratori
- **Move semantics** per trasferimento efficiente
- **Const iterator** per lettura senza modifiche

### Algoritmi Standard
- **my_sort**: QuickSort ricorsivo con comparatore personalizzabile
- **my_find**: Ricerca lineare con valore o predicato
- **my_copy**: Copia sicura tra range
- **my_move**: Move semantico tra range
- **my_fill**: Riempimento range con valore
- **my_equal**: Confronto tra range
- **my_count**: Conteggio occorrenze
- **my_accumulate**: Riduzione (fold) di un range

## 📁 Struttura del Progetto

```
custom-stl/
├── vector.h          # Dichiarazione MyVector
├── vector.tpp        # Implementazione MyVector
├── list.h            # Dichiarazione MyLinkedList
├── list.tpp          # Implementazione MyLinkedList
├── algorithms.h      # Algoritmi standard (template)
├── main.cpp          # Test suite completa
└── README.md         # Documentazione
```

## 🚀 Container Implementati

### MyVector<T>

```cpp
// Costruttori
MyVector();                                    // Default
MyVector(size_t count);                        // Con dimensione
MyVector(std::initializer_list<T> init);       // Initializer list
MyVector(const MyVector& other);               // Copy
MyVector(MyVector&& other) noexcept;           // Move

// Element access
T& operator[](size_t index);                  // O(1)
T& at(size_t index);                           // Con bounds checking
T& front();                                    // Primo elemento
T& back();                                     // Ultimo elemento
T* data();                                     // Raw pointer

// Capacity
size_t size() const noexcept;
size_t capacity() const noexcept;
bool empty() const noexcept;
void reserve(size_t new_cap);                  // Preallocazione
void shrink_to_fit();                          // Ottimizza memoria

// Modifiers
void push_back(const T& value);                // Copy
void push_back(T&& value);                     // Move
template<typename... Args>
void emplace_back(Args&&... args);            // In-place construction
void pop_back();
void resize(size_t count);
void clear();
```

### MyLinkedList<T>

```cpp
// Iteratore bidirezionale
class iterator {
    reference operator*() const;
    pointer operator->() const;
    iterator& operator++();                    // Pre-increment
    iterator operator++(int);                 // Post-increment
    iterator& operator--();                    // Pre-decrement
    iterator operator--(int);                 // Post-decrement
    bool operator==(const iterator&) const;
    bool operator!=(const iterator&) const;
};

// Costruttori
MyLinkedList();
MyLinkedList(std::initializer_list<T> init);
MyLinkedList(const MyLinkedList&);
MyLinkedList(MyLinkedList&&) noexcept;

// Element access
T& front();
T& back();

// Iterators
iterator begin();
iterator end();
const_iterator cbegin();
const_iterator cend();

// Modifiers
void push_front(const T&);
void push_front(T&&);
void push_back(const T&);
void push_back(T&&);
void pop_front();
void pop_back();
iterator insert(iterator pos, const T&);
iterator erase(iterator pos);
iterator erase(iterator first, iterator last);
```

## 🧮 Algoritmi Implementati

```cpp
// Ricerca
InputIt my_find(InputIt first, InputIt last, const T& value);
InputIt my_find_if(InputIt first, InputIt last, Predicate pred);

// Modifica
OutputIt my_copy(InputIt first, InputIt last, OutputIt d_first);
OutputIt my_move(InputIt first, InputIt last, OutputIt d_first);
void my_fill(ForwardIt first, ForwardIt last, const T& value);

// Ordinamento
void my_sort(RandomIt first, RandomIt last);
void my_sort(RandomIt first, RandomIt last, Compare comp);

// Confronto
bool my_equal(InputIt1 first1, InputIt1 last1, InputIt2 first2);
typename std::iterator_traits<InputIt>::difference_type
    my_count(InputIt first, InputIt last, const T& value);

// Riduzione
T my_accumulate(InputIt first, InputIt last, T init);
```

## 🛠 Tecnologie Utilizzate

### C++ Features
- **C++17 Standard**
- **Templates** con typename e variadic templates
- **RAII** per gestione memoria
- **Rule of Five** (destructor, copy/move constructor/assignment)
- **Placement new** per costruzione in-place
- **Perfect forwarding** con `std::forward`
- **Const correctness** completo
- **Operator overloading** (arithmetic, comparison, dereference)
- **Iterator traits** per compatibilità STL

### Pattern di Design
- **Iterator Pattern** per traversamento uniforme
- **Sentinel Nodes** per semplificare edge cases
- **Copy-and-Swap Idiom** per strong exception safety
- **Template Method Pattern** per algoritmi generici

## 💻 Compilazione ed Esecuzione

### Requisiti
- C++17 o superiore
- Compilatore compatibile: GCC 7+, Clang 5+, MSVC 2017+

### Compilazione

**GCC/Clang:**
```bash
cd custom-stl/
g++ -std=c++17 -Wall -Wextra -O2 main.cpp -o custom_stl
./custom_stl
```

**Clang con sanitizers:**
```bash
clang++ -std=c++17 -Wall -Wextra -g -fsanitize=address main.cpp -o custom_stl
./custom_stl
```

**MSVC (Visual Studio):**
```cmd
cl /std:c++17 /EHsc /W4 main.cpp
custom_stl.exe
```

### Output Atteso
```
========================================
  Custom STL Containers - Test Suite
========================================
=== Test MyVector: Funzionalita' Base ===
✓ Costruttore di default
✓ push_back e size
✓ operator[]
✓ at() lancia out_of_range
✓ front() e back()
✓ pop_back()
✓ Initializer list constructor

=== Test MyVector: Iteratori ===
✓ Iterazione con begin()/end()
✓ Range-based for loop
✓ Const iterator

...

========================================
  Tutti i test sono PASSATI! ✓
========================================
```

## 📚 Esempi di Utilizzo

### MyVector - Uso Base

```cpp
#include "vector.h"
#include "algorithms.h"

using namespace mystl;

int main() {
    // Creazione con initializer list
    MyVector<int> numbers = {5, 2, 8, 1, 9};

    // Accesso agli elementi
    std::cout << "Primo: " << numbers.front() << std::endl;
    std::cout << "Ultimo: " << numbers.back() << std::endl;
    std::cout << "Indice 2: " << numbers[2] << std::endl;

    // Aggiunta elementi
    numbers.push_back(10);
    numbers.emplace_back(11);  // Costruisce in-place

    // Iterazione
    for (const auto& n : numbers) {
        std::cout << n << " ";
    }
    std::cout << std::endl;

    // Ordinamento
    my_sort(numbers.begin(), numbers.end());

    return 0;
}
```

### MyVector - Move Semantics

```cpp
MyVector<std::string> strings;

// Push con copy semantics
std::string hello = "Hello";
strings.push_back(hello);  // Copia hello

// Push con move semantics
strings.push_back(std::move("World"));  // Move del temporaneo
strings.push_back(std::move(hello));    // Move di hello

// Move del vettore intero
MyVector<std::string> other = std::move(strings);
// strings è ora vuoto, other ha tutti gli elementi
```

### MyLinkedList - Uso Base

```cpp
#include "list.h"

MyLinkedList<int> list;

// Inserimento
list.push_back(1);
list.push_front(0);
list.push_back(2);

// Iterazione
for (auto it = list.begin(); it != list.end(); ++it) {
    std::cout << *it << " ";
}
// Output: 0 1 2

// Insert con iteratore
auto it = list.begin();
++it;
list.insert(it, 99);  // Inserisce 99 dopo 0

// Erase
list.erase(list.begin());  // Rimuove primo elemento
```

### Algoritmi - Esempi Complet

```cpp
MyVector<int> data = {3, 1, 4, 1, 5, 9, 2, 6};

// Find
auto it = my_find(data.begin(), data.end(), 5);
if (it != data.end()) {
    std::cout << "Trovato 5!" << std::endl;
}

// Find con predicato
auto it2 = my_find_if(data.begin(), data.end(),
                      [](int x) { return x > 5; });
std::cout << "Primo > 5: " << *it2 << std::endl;

// Sort
my_sort(data.begin(), data.end());

// Sort decrescente
my_sort(data.begin(), data.end(),
        [](int a, int b) { return a > b; });

// Copy
MyVector<int> copy;
copy.resize(data.size());
my_copy(data.begin(), data.end(), copy.begin());

// Count
auto count = my_count(data.begin(), data.end(), 1);
std::cout << "Occorrenze di 1: " << count << std::endl;

// Accumulate
auto sum = my_accumulate(data.begin(), data.end(), 0);
std::cout << "Somma: " << sum << std::endl;

// Fill
my_fill(data.begin(), data.end(), 0);
```

### Esempio Avanzato - Custom Types

```cpp
struct Point {
    int x, y;
    Point(int x_, int_y) : x(x_), y(y_) {}

    // Necessario per my_find
    bool operator==(const Point& other) const {
        return x == other.x && y == other.y;
    }

    // Necessario per my_sort
    bool operator<(const Point& other) const {
        return x < other.x || (x == other.x && y < other.y);
    }
};

MyVector<Point> points;

// emplace_back costruisce Point in-place
points.emplace_back(1, 2);
points.emplace_back(3, 4);
points.emplace_back(0, 0);

// Sort usando operator<
my_sort(points.begin(), points.end());

// Find
Point target(1, 2);
auto it = my_find(points.begin(), points.end(), target);
```

## 🎓 Concetti Chiave

### 1. Template e Genericità
I template permettono di scrivere codice che funziona con qualsiasi tipo:
```cpp
template <typename T>
class MyVector {
    T* m_data;  // Funziona con int, std::string, struct, etc.
};
```

### 2. Gestione Memoria Manuale
Uso di placement new per costruire oggetti in memoria grezza:
```cpp
// Alloca memoria non inizializzata
T* m_data = static_cast<T*>(::operator new(capacity * sizeof(T)));

// Costruisce oggetto in-place
new (&m_data[index]) T(value);

// Distrugge esplicitamente
m_data[index].~T();
```

### 3. Move Semantics
Trasferimento efficiente di risorse:
```cpp
// Move constructor
MyVector(MyVector&& other) noexcept
    : m_data(other.m_data), m_size(other.m_size) {
    other.m_data = nullptr;  // Ruba i dati
    other.m_size = 0;
}
```

### 4. Iterator Pattern
Accesso uniforme ai container:
```cpp
// Stesso codice per MyVector e MyLinkedList
for (auto it = container.begin(); it != container.end(); ++it) {
    process(*it);
}
```

### 5. Const Correctness
Protezione da modifiche accidentali:
```cpp
// Versione const - può essere chiamata su oggetti const
const T& front() const { return m_head->next->data; }

// Versione non-const - modifica permessa
T& front() { return m_head->next->data; }
```

### 6. Rule of Five
Se definisci uno di questi, definiscili tutti:
1. **Destructor**: `~MyVector()`
2. **Copy constructor**: `MyVector(const MyVector&)`
3. **Copy assignment**: `operator=(const MyVector&)`
4. **Move constructor**: `MyVector(MyVector&&)`
5. **Move assignment**: `operator=(MyVector&&)`

### 7. Sentinel Nodes
Nodi dummy che semplificano il codice:
```cpp
// head -> [dummy] <=> [node1] <=> [node2] <=> [dummy] <- tail
// Non serve NULL check per insert/erase
```

## 📊 Complessità

| Operazione | MyVector | MyLinkedList |
|------------|----------|--------------|
| push_back | O(1) amortized | O(1) |
| push_front | O(n) | O(1) |
| pop_back | O(1) | O(1) |
| pop_front | O(n) | O(1) |
| operator[] | O(1) | Non supportato |
| insert | O(n) | O(1) con iteratore |
| erase | O(n) | O(1) con iteratore |
| find | O(n) | O(n) |
| sort | O(n log n) | Non efficiente |

## 🎯 Obiettivi di Apprendimento

Questo progetto dimostra competenza in:

- **Template programming**: Creazione di classi e funzioni generiche
- **Memory management**: Allocazione dinamica corretta senza memory leak
- **C++ idioms**: RAII, Rule of Five, copy-and-swap
- **STL principles**: Iteratori, algoritmi, container concepts
- **Modern C++**: Move semantics, perfect forwarding, constexpr
- **Code quality**: Const correctness, exception safety, clean code

## 📝 Note Tecniche

### Perché .tpp invece di .cpp?
I template devono essere istanziati a compile-time. Separare dichiarazione (.h) da implementazione (.tpp) permette:
- Codice più pulito nei header
- Evita problemi di linking con template
- Mantiene interfaccia visibile

### Placement New
```cpp
// Costruisce T in memoria già allocata
new (address) T(constructor_args);

// Equivalente a:
// T* obj = new T(args);  // Ma senza allocazione extra
```

### Perfect Forwarding
```cpp
template <typename... Args>
void emplace_back(Args&&... args) {
    new (&m_data[m_size]) T(std::forward<Args>(args)...);
    // Mantiene value category (lvalue/rvalue) degli argomenti
}
```

## 🔍 Risorse

- [C++ Reference - Containers](https://en.cppreference.com/w/cpp/container)
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/)
- [Effective Modern C++ - Scott Meyers](https://www.oreilly.com/library/view/effective-modern-c/9781491908419/)

## 📜 Licenza

Progetto educativo - Code per dimostrare competenze C++.

---

**Autore**: Progetto portfolio per dimostrare competenze in C++ avanzato, template programming e understanding della STL.

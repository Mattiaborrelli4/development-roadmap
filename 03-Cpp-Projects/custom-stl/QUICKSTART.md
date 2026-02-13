# Guida Rapida - Custom STL Containers

## Primi Passi

### 1. Compilazione Veloce

```bash
# Entra nella directory
cd custom-stl/

# Compila
g++ -std=c++17 -Wall -O2 main.cpp -o custom_stl

# Esegui i test
./custom_stl
```

Oppure usa il Makefile:

```bash
make
make run
```

### 2. Struttura File Essenziale

```
custom-stl/
├── vector.h          # Dichiarazione MyVector
├── vector.tpp        # Implementazione (include automatico)
├── list.h            # Dichiarazione MyLinkedList
├── list.tpp          # Implementazione (include automatico)
├── algorithms.h      # Tutti gli algoritmi
├── main.cpp          # Test suite
├── README.md         # Documentazione completa
├── ARCHITECTURE.md   # Diagrammi architetturali
└── QUICKSTART.md     # Questo file
```

## Esempi Pratici

### MyVector - I Fondamentali

```cpp
#include "vector.h"

using namespace mystl;

int main() {
    // 1. Creazione
    MyVector<int> v;                    // Vuoto
    MyVector<int> v2(5);                // 5 elementi di default
    MyVector<int> v3 = {1, 2, 3, 4};   // Initializer list

    // 2. Aggiunta elementi
    v.push_back(10);
    v.push_back(20);
    v.emplace_back(30);  // Costruisce in-place (più efficiente)

    // 3. Accesso
    int x = v[0];          // Senza controllo bounds
    int y = v.at(1);       // Con eccezione se out of range
    int first = v.front(); // Primo elemento
    int last = v.back();   // Ultimo elemento

    // 4. Info dimensione
    size_t n = v.size();       // Elementi presenti
    size_t cap = v.capacity(); // Spazio allocato
    bool empty = v.empty();    // true se vuoto

    // 5. Rimozione
    v.pop_back();              // Rimuove ultimo
    v.clear();                 // Svuota tutto

    return 0;
}
```

### MyVector - Iterazione

```cpp
MyVector<int> v = {1, 2, 3, 4, 5};

// Metodo 1: Iteratori espliciti
for (auto it = v.begin(); it != v.end(); ++it) {
    std::cout << *it << " ";
}

// Metodo 2: Range-based for (consigliato)
for (const auto& elem : v) {
    std::cout << elem << " ";
}

// Metodo 3: Indice
for (size_t i = 0; i < v.size(); ++i) {
    std::cout << v[i] << " ";
}

// Metodo 4: Const iterator (solo lettura)
for (auto it = v.cbegin(); it != v.cend(); ++it) {
    std::cout << *it << " ";
}
```

### MyVector - Ottimizzazione Memoria

```cpp
MyVector<std::string> v;

// Prealloca per evitare realloc
v.reserve(100);  // Capacità = 100

// Ora push_back è O(1) garantito
for (int i = 0; i < 100; ++i) {
    v.push_back("item");
}

// Ottimizza memoria se sai che non aggiungerai altro
v.shrink_to_fit();  // Riduce capacity a size
```

### MyVector - Move Semantics

```cpp
MyVector<std::string> v1;

// Copy semantics (crea copia)
std::string s = "Hello";
v1.push_back(s);      // s ancora valido, v1 ha copia

// Move semantics (trasferisce ownership)
v1.push_back(std::string("World"));  // Move del temporaneo
v1.push_back(std::move(s));           // Move di s

// s è ora in uno stato valido ma indefinito
// v1 ha il contenuto originale di s

// Move dell'intero vettore
MyVector<std::string> v2 = std::move(v1);
// v1 è ora vuoto, v2 ha tutti gli elementi
```

### MyLinkedList - Base

```cpp
#include "list.h"

MyLinkedList<int> list;

// Inserimento
list.push_back(1);   // [1]
list.push_front(0);  // [0, 1]
list.push_back(2);   // [0, 1, 2]

// Accesso
int first = list.front();  // 0
int last = list.back();    // 2

// Rimozione
list.pop_front();  // [1, 2]
list.pop_back();   // [1]
```

### MyLinkedList - Iteratori Bidirezionali

```cpp
MyLinkedList<int> list = {10, 20, 30, 40};

// Forward iteration
for (auto it = list.begin(); it != list.end(); ++it) {
    std::cout << *it << " ";
}
// Output: 10 20 30 40

// Backward iteration
auto it = list.end();
--it;  // Punta all'ultimo elemento
while (it != list.begin()) {
    std::cout << *it << " ";
    --it;
}
std::cout << *it << " ";  // Primo elemento
// Output: 40 30 20 10

// Operator ->
struct Point { int x, y; };
MyLinkedList<Point> points;
points.emplace_back(1, 2);
auto pit = points.begin();
std::cout << pit->x << ", " << pit->y;  // 1, 2
```

### MyLinkedList - Insert/Erase

```cpp
MyLinkedList<int> list = {1, 3, 5};

// Insert dopo la prima posizione
auto it = list.begin();  // Punta a 1
++it;                     // Punta a 3
list.insert(it, 2);       // [1, 2, 3, 5]

// Insert alla fine
list.insert(list.end(), 6);  // [1, 2, 3, 5, 6]

// Erase singolo elemento
it = list.begin();
++it;  // Punta a 2
list.erase(it);  // [1, 3, 5, 6]

// Erase range
it = list.begin();
auto last = list.end();
--last;  // Punta a 6
list.erase(it, last);  // Rimuove tutto tranne ultimo
```

### Algoritmi - Ricerca

```cpp
#include "algorithms.h"

MyVector<int> v = {5, 2, 8, 1, 9, 3};

// Trova valore
auto it = my_find(v.begin(), v.end(), 8);
if (it != v.end()) {
    std::cout << "Trovato 8 alla posizione: "
              << (it - v.begin());
}

// Trova con condizione
it = my_find_if(v.begin(), v.end(), [](int x) {
    return x > 5;
});
std::cout << "Primo > 5: " << *it;  // 8

// Conta occorrenze
auto count = my_count(v.begin(), v.end(), 2);
std::cout << "Il numero 2 appare " << count << " volte";
```

### Algoritmi - Ordinamento

```cpp
MyVector<int> v = {5, 2, 8, 1, 9};

// Ordine crescente (default)
my_sort(v.begin(), v.end());
// [1, 2, 5, 8, 9]

// Ordine decrescente (con comparatore)
my_sort(v.begin(), v.end(), [](int a, int b) {
    return a > b;
});
// [9, 8, 5, 2, 1]

// Ordinamento custom struct
struct Person {
    std::string name;
    int age;
};

MyVector<Person> people = {{"Alice", 30}, {"Bob", 25}};

my_sort(people.begin(), people.end(),
        [](const Person& a, const Person& b) {
    return a.age < b.age;  // Ordina per età
});
```

### Algoritmi - Modifica

```cpp
MyVector<int> src = {1, 2, 3, 4, 5};
MyVector<int> dest;
dest.resize(5);

// Copy
my_copy(src.begin(), src.end(), dest.begin());
// dest = [1, 2, 3, 4, 5]

// Fill
my_fill(dest.begin(), dest.end(), 0);
// dest = [0, 0, 0, 0, 0]

// Accumulate (somma)
auto sum = my_accumulate(src.begin(), src.end(), 0);
// sum = 15

// Equal
bool same = my_equal(src.begin(), src.end(), dest.begin());
// same = false
```

## Cosa Usare Quando

```
Usa MyVector quando:
✓ Hai bisogno di accesso random (operator[])
✓ La cache locality è importante
✓ Sai in anticipo quanti elementi servono
✓ Fai molte letture e poche inserzioni/cancellazioni

Usa MyLinkedList quando:
✓ Fai molte inserzioni/cancellazioni nel mezzo
✓ Non ti serve accesso random per indice
✓ Gli iteratori devono rimanere validi dopo modifiche
✓ Vuoi insert/erase O(1) con iteratore

Usa my_sort quando:
✓ Hai bisogno di ordinamento generico
✓ Vuoi un comparatore personalizzato
✓ Operi su iteratori random access

Usa my_find quando:
✓ Cerchi un valore specifico
✓ Hai una condizione complessa (find_if)
```

## Errori Comuni da Evitare

```cpp
// ❌ SBAGLIATO: Accesso out of range
MyVector<int> v = {1, 2, 3};
int x = v[10];     // Undefined behavior
int y = v.at(10);  // Lancia std::out_of_range ✓

// ❌ SBAGLIATO: Iterator invalidato
MyVector<int> v = {1, 2, 3};
auto it = v.begin();
v.push_back(4);  // Potrebbe invalidare it!
std::cout << *it;  // Undefined behavior

// ✅ GIUSTO: Riaquisisci l'iteratore
v.push_back(4);
it = v.begin();  // Nuovo iteratore valido
std::cout << *it;

// ❌ SBAGLIATO: Memory leak manuale
T* arr = new T[100];
// ... usa arr ...
delete[] arr;  // Da fare manualmente!

// ✅ GIUSTO: MyVector gestisce memoria automaticamente
MyVector<T> v;
v.resize(100);
// ... usa v ...
// Destructor chiama delete[] automaticamente

// ❌ SBAGLIATO: Move da temporaneo
std::string s = std::string("Hello");
// "Hello" costruito, poi copiato in s

// ✅ GIUSTO: Costruisci in-place
std::string s = "Hello";  // Costruzione diretta
v.emplace_back("Hello");  // Costruisce in v, non copia
```

## Performance Tips

```cpp
// 1. Reserve quando conosci la dimensione
MyVector<int> v;
v.reserve(1000);  // Evita realloc
for (int i = 0; i < 1000; ++i) {
    v.push_back(i);
}

// 2. Usa emplace_back invece di push_back
// Evita costruzione + copia
v.emplace_back(i);  // Costruisce direttamente in v

// 3. Usa move per oggetti pesanti
MyVector<std::string> v;
std::string s = "Hello World";
v.push_back(std::move(s));  // Move, non copy

// 4. Passa per reference se non modifichi
void print(const MyVector<int>& v) {  // ✓
    for (const auto& x : v) { ... }
}
// Evita copia dell'intero vettore

// 5. Usa const_iterator per sola lettura
void sum(const MyVector<int>& v) {
    int total = 0;
    for (auto it = v.cbegin(); it != v.cend(); ++it) {
        total += *it;
    }
}
```

## Debug Tips

```cpp
// Attiva warning del compilatore
g++ -std=c++17 -Wall -Wextra -Wpedantic main.cpp

// Usa sanitizers per memory errors
g++ -std=c++17 -g -fsanitize=address main.cpp

// Debug mode
g++ -std=c++17 -g -O0 main.cpp -o custom_stl_debug
gdb ./custom_stl_debug

// Valgrind (Linux)
valgrind --leak-check=full ./custom_stl
```

## Comandi Git Essenziali

```bash
# Se vuoi versionare il progetto
git init
git add .
git commit -m "Initial commit: Custom STL Containers"

# .gitignore consigliato
echo "*.o" >> .gitignore
echo "custom_stl" >> .gitignore
echo "*.exe" >> .gitignore
```

## Prossimi Passi

1. **Esplora i test**: Guarda `main.cpp` per esempi completi
2. **Leggi l'architettura**: `ARCHITECTURE.md` per diagrammi dettagliati
3. **Sperimenta**: Crea i tuoi container e algoritmi
4. **Benchmark**: Confronta con STL standard
5. **Estendi**: Aggiungi more algoritmi (my_binary_search, my_merge, etc.)

---

**Buon coding! 🚀**

Per domande o problemi, consulta `README.md` per la documentazione completa.

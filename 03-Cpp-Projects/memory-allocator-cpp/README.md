# 🧠 C++ Memory Allocator

Un allocatore di memoria personalizzato implementato da zero in C++17 con memory pooling, garbage collection e capabilities avanzate di debug.

## 📋 Caratteristiche

### Core Functionality
- **my_malloc(size, alignment)** - Alloca memoria con allineamento personalizzato
- **my_free(ptr)** - Dealloca memoria con safety checks
- **my_realloc(ptr, size)** - Ridimensiona memoria esistente

### Performance Optimization
- **Memory Pooling** - Pool a dimensione fissa per allocazioni piccole (< 512 bytes)
  - Pool per dimensioni: 16, 32, 64, 128, 256, 512 bytes
  - Fast path per allocazioni frequenti di piccole dimensioni
- **Coalescing** - Unione automatica di blocchi adiacenti liberi
- **First-Fit Algorithm** - Algoritmo di ricerca blocco efficiente

### Metadati Blocchi
Ogni blocco contiene un header con:
- **size** - Dimensione del blocco
- **magic** - Magic number per detectare corruption
- **is_free** - Flag di stato
- **prev/next** - Puntatori per lista doppiamente linkata
- **allocation_id** - ID univoco per tracking

### Safety Features
- **Double-Free Detection** - Detecta tentativi di free multipli
- **Memory Leak Detection** - Tracking di tutte le allocazioni non liberate
- **Header Corruption Detection** - Magic numbers per validare integrità
- **Use-After-Free Protection** - Magic numbers speciali per blocchi liberati

### Debug Mode
- **Allocation Tracking** - Tracciamento con file e line number
- **Statistics** - Memoria totale allocata/libera, numero blocchi
- **Leak Reporting** - Report dettagliato di memory leaks
- **Performance Timing** - Misurazione tempi di allocazione

## 🔢 Magic Numbers

```
0xDEADBEEF  - Header valido (blocco allocato)
0xCAFEBABE  - Blocchi liberati (use-after-free detection)
0xFEEEFEEE  - Double-free detectato
```

## 🏗️ Architettura

### Componenti

```
memory-allocator-cpp/
├── allocator.h      - Interfaccia principale allocatore
├── allocator.cpp    - Implementazione con malloc/free/realloc
├── pool.h           - Memory pooling per performance
├── pool.cpp         - Implementazione fixed-size pools
├── debug.h          - Debug, logging, tracking
├── main.cpp         - Test suite completa
└── README.md        - Questa documentazione
```

### Struttura Blocco

```
┌─────────────────────────────────────────┐
│ BlockMetadata (header)                   │
│ - magic: 0xDEADBEEF                       │
│ - size: dimensione blocco                 │
│ - is_free: flag stato                    │
│ - prev: blocco precedente                │
│ - next: blocco successivo                │
│ - allocation_id: ID tracking              │
├─────────────────────────────────────────┤
│                                         │
│      Dati utente (payload)               │
│                                         │
└─────────────────────────────────────────┘
```

### Memory Pool

```
┌─────────────────────────────────────┐
│ FixedSizePool (16 bytes)            │
│ ┌────┬────┬────┬────┬────┬────┐      │
│ │ B1 │ B2 │ B3 │ B4 │ B5 │... │      │
│ └────┴────┴────┴────┴────┴────┘      │
├─────────────────────────────────────┤
│ FixedSizePool (32 bytes)            │
│ ┌────────┬────────┬────────┬────┐   │
│ │  B1    │  B2    │  B3    │...│   │
│ └────────┴────────┴────────┴────┘   │
├─────────────────────────────────────┤
│ ...                                │
└─────────────────────────────────────┘
```

## 🚀 Compilazione ed Esecuzione

### Requisiti
- C++17 o superiore
- CMake 3.15+ (opzionale, per build CMake)

### Compilazione Manuale

#### Linux/macOS
```bash
g++ -std=c++17 -O2 -Wall -Wextra -o allocator \
    allocator.cpp pool.cpp main.cpp

./allocator
```

#### Windows (MSVC)
```cmd
cl /std:c++17 /O2 /EHsc /Fe:allocator.exe ^
   allocator.cpp pool.cpp main.cpp

allocator.exe
```

#### Windows (MinGW)
```bash
g++ -std=c++17 -O2 -Wall -Wextra -o allocator.exe \
    allocator.cpp pool.cpp main.cpp

allocator.exe
```

### CMake (Opzionale)

```bash
mkdir build && cd build
cmake ..
make
./allocator
```

## 📊 Test Suite

Il progetto include una suite di test completa in `main.cpp`:

1. **Test Allocazione Base** - Funzionalità base malloc/free
2. **Test Realloc** - Ridimensionamento memoria con preservazione dati
3. **Test Memory Pool** - Allocazione veloce per piccoli blocchi
4. **Test Coalescing** - Unione blocchi adiacenti liberi
5. **Test Allineamento** - Verifica alignment personalizzato
6. **Test Stress** - Allocazioni random intensive
7. **Test Performance** - Misurazione velocità
8. **Test Leak Detection** - Rilevamento memory leaks
9. **Test Garbage Collector** - Mark and sweep
10. **Test Error Detection** - Double-free, corruption

### Esempio Output

```
╔════════════════════════════════════════════╗
║   C++ Memory Allocator - Test Suite    ║
╚════════════════════════════════════════════╝

=== TEST 1: Allocazione Base ===
[ALLOC] Allocator inizializzato con heap di 1048576 bytes
Allocati: ptr1=0x..., ptr2=0x..., ptr3=0x...
Riallocato dopo free: ptr4=0x...
Stat: 0 allocati, 1047552 liberi

=== TEST 2: Realloc ===
Allocato 100 bytes: 0x...
Ridimensionato a 200 bytes: 0x...
Dati preservati: SI
Ridimensionato a 50 bytes: 0x...

✓ Tutti i test passati senza memory leaks!
```

## 💡 Utilizzo

### Uso Base

```cpp
#include "allocator.h"

using namespace MemoryAllocator;

// Allocazione
void* ptr = MY_MALLOC(100);

// Utilizzo
int* arr = static_cast<int*>(MY_MALLOC(10 * sizeof(int)));
for (int i = 0; i < 10; ++i) {
    arr[i] = i;
}

// Deallocazione
MY_FREE(ptr);
MY_FREE(arr);
```

### Con Allineamento Personalizzato

```cpp
// Alloca con allineamento a 64 bytes
void* ptr = Allocator::getInstance().my_malloc(256, 64);

// Verifica allineamento
assert((reinterpret_cast<uintptr_t>(ptr) % 64) == 0);
```

### Realloc

```cpp
void* ptr = MY_MALLOC(100);
// ... usa ptr ...

// Ridimensiona a 200 bytes
ptr = MY_REALLOC(ptr, 200);
```

### Debug Mode

```cpp
// Attiva debug mode con tracking
Allocator::getInstance().set_debug_mode(true);

// Fai allocazioni
void* ptr = MY_MALLOC(100);

// Controlla leaks
Allocator::getInstance().detect_memory_leaks();

// Stampa allocazioni attive
Allocator::getInstance().print_allocations();

// Cleanup
MY_FREE(ptr);
```

### Statistiche

```cpp
AllocatorStats stats = Allocator::getInstance().get_stats();

std::cout << "Memoria allocata: " << stats.total_allocated << " bytes\n";
std::cout << "Memoria libera: " << stats.total_free << " bytes\n";
std::cout << "Blocchi liberi: " << stats.free_blocks << "/" << stats.total_blocks << "\n";
```

## 🔧 Platform Support

### Windows
- `VirtualAlloc`/`VirtualFree` per gestione memoria sistema
- Supporto completo

### Unix/Linux
- `mmap`/`munmap` per gestione memoria sistema
- Supporto completo

### macOS
- Stesso approccio Unix/Linux
- Supporto completo

## 🎯 Dettagli Implementazione

### Algoritmo Allocation

1. **Request Size < 512 bytes** → Usa Memory Pool (fast path)
2. **Cerca blocco libero** → First-fit traversal
3. **Blocco trovato** → Split se necessario, marca come usato
4. **Nessun blocco** → Request memoria al sistema, riprova
5. **Tracking** → Aggiungi a allocation map, genera ID

### Algoritmo Free

1. **Valida header** → Check magic numbers
2. **Detect double-free** → Se `is_free` già true
3. **Marca libero** → Set flag, aggiorna magic
4. **Coalescing** → Unisci con blocchi adiacenti liberi
5. **Update tracking** → Rimuovi da allocation map

### Garbage Collection

Implementa un semplice **Mark-and-Sweep**:
- **Mark**: Durante uso normale, blocchi validi hanno `MAGIC_HEADER`
- **Sweep**: Blocchi non marcati possono essere puliti
- Automatico durante free, può essere chiamato manualmente

### Memory Pool

- **6 pool a dimensione fissa**: 16, 32, 64, 128, 256, 512 bytes
- **Ogni pool**: Chunk di 4KB con blocchi equal-sized
- **Free list**: Lista linkata di blocchi liberi per O(1) allocation
- **Coalescing non necessario**: Blocchi same-size, no fragmentation

## 📈 Performance

### Complessità

| Operazione | Complessità | Note |
|-----------|-------------|------|
| malloc (piccolo) | O(1) | Memory pool |
| malloc (grande) | O(n) | First-fit search |
| free | O(1) | Con coalescing O(1) |
| realloc | O(n) | Caso peggiore |

### Benchmark Approssimativi

```
Malloc (128 bytes):  ~0.05 ms/10000 ops  (5 µs/op)
Free  (128 bytes):  ~0.03 ms/10000 ops  (3 µs/op)
```

*Nota: Performance variano based su hardware e OS*

## 🐛 Debugging

### Magic Numbers

I magic numbers permettono di detectare diversi tipi di errori:

```cpp
// Header corrotto
if (block->magic != MAGIC_HEADER) {
    // Corruption detectata!
}

// Use-after-free
if (block->magic == MAGIC_FREED) {
    // Tentativo di usare memoria liberata!
}

// Double-free
if (block->magic == MAGIC_DOUBLE_FREE) {
    // Double-free detectato!
}
```

### Memory Leak Detection

```cpp
// Alla fine del programma
if (!Allocator::getInstance().detect_memory_leaks()) {
    // Stampa dettagli leaks
    Allocator::getInstance().print_allocations();
}
```

## 📚 Concetti Chiave

### RAII (Resource Acquisition Is Initialization)

L'allocatore usa pattern RAII per gestione risorse:
- Costruttore: Inizializza heap
- Distruttore: Cleanup automatico
- Singleton: Garantisce unica istanza

### Memory Fragmentation

- **Internal Fragmentation**: Blocco più grande del necessario
  - Mitigato con splitting
- **External Fragmentation**: Blocchi liberi sparsi
  - Mitigato con coalescing

### First-Fit vs Best-Fit

Questo implementazione usa **First-Fit**:
- ✓ Più veloce
- ✓ Semplice implementare
- ✗ Può lasciare piccoli blocchi sparsi

## 🔮 Possibili Miglioramenti

1. **Best-Fit Algorithm** - Migliore utilizzo spazio
2. **Thread Safety** - Mutex per concorrenza
3. **Deferred Coalescing** - Solo quando necessario
4. **Size Classes** - Pool più granulari
5. **Huge Page Support** - Per grandi allocazioni
6. **Allocation Profiling** - Statistiche dettagliate
7. **Compactation** - Sposta blocchi per defrag
8. **std::allocator Compatible** - Per STL containers

## 📝 Licenza

Questo progetto è a scopo educativo. Libero utilizzo e modifica.

## 👤 Autore

Creato come progetto dimostrativo per portfolio personale.

## 🙏 Ringraziamenti

- Concepts classici: K&R malloc, dlmalloc
- Modern C++ Practices: C++17 features
- Memory Management: OS manuals, CS theory

---

**Divertiti a esplorare come funziona un memory allocator!** 🚀

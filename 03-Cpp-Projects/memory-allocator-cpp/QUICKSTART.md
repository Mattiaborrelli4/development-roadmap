# Quick Start - C++ Memory Allocator

## Compilazione Rapida

### Windows (MinGW)
```bash
g++ -std=c++17 -O2 -o allocator.exe src/allocator.cpp src/pool.cpp src/main.cpp -I include
allocator.exe
```

### Windows (MSVC)
```cmd
cl /std:c++17 /O2 /EHsc /I include /Fe:allocator.exe src\allocator.cpp src\pool.cpp src\main.cpp
allocator.exe
```

### Linux/macOS
```bash
g++ -std=c++17 -O2 -o allocator src/allocator.cpp src/pool.cpp src/main.cpp -I include
./allocator
```

### Con CMake
```bash
mkdir build && cd build
cmake ..
make
./bin/allocator
```

## Struttura Progetto

```
memory-allocator-cpp/
├── include/
│   ├── allocator.h    - Interfaccia allocatore
│   ├── pool.h         - Memory pooling
│   └── debug.h        - Debug e logging
├── src/
│   ├── allocator.cpp  - Implementazione
│   ├── pool.cpp       - Pool implementation
│   └── main.cpp       - Test suite
├── build.bat          - Build script Windows
├── build.sh           - Build script Unix
├── CMakeLists.txt     - CMake config
└── README.md          - Documentazione completa
```

## API Rapida

```cpp
#include "allocator.h"

using namespace MemoryAllocator;

// Allocazione
void* ptr = MY_MALLOC(100);

// Realloc
ptr = MY_REALLOC(ptr, 200);

// Free
MY_FREE(ptr);

// Debug mode
Allocator::getInstance().set_debug_mode(true);

// Statistiche
AllocatorStats stats = Allocator::getInstance().get_stats();

// Detect leaks
Allocator::getInstance().detect_memory_leaks();
```

## Test

Il programma esegue automaticamente 10 test:

1. Allocazione base
2. Realloc
3. Memory pool
4. Coalescing
5. Allineamento
6. Stress test
7. Performance
8. Leak detection
9. Garbage collector
10. Error detection

Tutti con output colorato e dettagliato!

## Magic Numbers

- `0xDEADBEEF` - Header valido
- `0xCAFEBABE` - Blocco liberato
- `0xFEEEFEEE` - Double-free

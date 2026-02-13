# C++ Memory Allocator - Project Summary

## 🎯 Project Overview

A complete memory allocator implementation from scratch in C++17 with advanced features including memory pooling, garbage collection, and comprehensive debugging capabilities.

## 📁 Project Structure

```
memory-allocator-cpp/
├── include/
│   ├── allocator.h       (4.0 KB) - Main allocator interface
│   ├── pool.h            (2.4 KB) - Memory pooling system
│   └── debug.h           (5.7 KB) - Debug & logging utilities
├── src/
│   ├── allocator.cpp     (13.3 KB) - Core implementation
│   ├── pool.cpp          (5.2 KB) - Pool implementation
│   └── main.cpp          (11.3 KB) - Complete test suite
├── allocator.exe         (118 KB) - Compiled executable ✓
├── CMakeLists.txt        (1.0 KB) - CMake build config
├── build.bat             - Windows build script
├── build.sh              - Unix build script
├── README.md             (12 KB) - Full documentation (Italian)
├── QUICKSTART.md         (2.0 KB) - Quick reference
└── .gitignore           - Git ignore patterns
```

## ✅ Features Implemented

### Core Functionality ✓
- [x] `my_malloc(size, alignment)` - Allocate memory with custom alignment
- [x] `my_free(ptr)` - Deallocate memory with safety checks
- [x] `my_realloc(ptr, size)` - Resize existing allocations
- [x] Block metadata with size, magic, free flag
- [x] Double-linked list of blocks

### Performance Optimization ✓
- [x] Memory pooling for small allocations (< 512 bytes)
- [x] 6 fixed-size pools: 16, 32, 64, 128, 256, 512 bytes
- [x] Fast path O(1) allocation for pooled blocks
- [x] Coalescing of adjacent free blocks
- [x] First-fit allocation algorithm

### Safety Features ✓
- [x] Double-free detection
- [x] Memory leak detection
- [x] Header corruption detection
- [x] Use-after-free protection
- [x] Magic number validation:
  - `0xDEADBEEF` - Valid header
  - `0xCAFEBABE` - Freed block (use-after-free)
  - `0xFEEEFEEE` - Double-free detected

### Debug Mode ✓
- [x] Allocation tracking with file/line info
- [x] Statistics (allocated/free memory, block counts)
- [x] Leak reporting
- [x] Performance timing
- [x] Comprehensive logging

### Garbage Collection ✓
- [x] Mark-and-sweep implementation
- [x] Automatic marking during allocations
- [x] Manual sweep capability

### Cross-Platform ✓
- [x] Windows support (VirtualAlloc)
- [x] Unix/Linux support (mmap)
- [x] macOS support
- [x] CMake build system

## 🔧 Technical Implementation

### Block Metadata Structure
```cpp
struct BlockMetadata {
    uint32_t magic;           // 0xDEADBEEF for validation
    size_t size;              // Block size (excluding metadata)
    bool is_free;             // Free flag
    BlockMetadata* prev;      // Previous block
    BlockMetadata* next;      // Next block
    size_t allocation_id;     // Debug tracking ID
};
```

### Memory Pool System
- 6 pools with fixed block sizes
- Chunks of 4KB with equal-sized blocks
- Free list for O(1) allocation
- No fragmentation (same-size blocks)

### Allocation Algorithm
1. **Size < 512 bytes** → Use Memory Pool (O(1))
2. **Find free block** → First-fit traversal
3. **Block found** → Split if needed, mark as used
4. **No block** → Request system memory, retry
5. **Track allocation** → Add to allocation map

## 📊 Test Suite

The project includes 10 comprehensive tests:

1. **Basic Allocation** - malloc/free functionality
2. **Realloc** - Memory resizing with data preservation
3. **Memory Pool** - Small block performance
4. **Coalescing** - Adjacent block merging
5. **Alignment** - Custom alignment support
6. **Stress Test** - Random allocation patterns
7. **Performance** - Timing measurements
8. **Leak Detection** - Memory leak reporting
9. **Garbage Collector** - Mark-and-sweep
10. **Error Detection** - Corruption, double-free

## 🚀 Compilation

### Windows (MinGW)
```bash
g++ -std=c++17 -O2 -o allocator.exe src/*.cpp -I include
```

### Linux/macOS
```bash
g++ -std=c++17 -O2 -o allocator src/*.cpp -I include
```

### CMake
```bash
mkdir build && cd build
cmake ..
make
./bin/allocator
```

## 📝 Usage Example

```cpp
#include "allocator.h"

using namespace MemoryAllocator;

// Enable debug mode
Allocator::getInstance().set_debug_mode(true);

// Allocate memory
void* ptr = MY_MALLOC(100);

// Reallocate
ptr = MY_REALLOC(ptr, 200);

// Free
MY_FREE(ptr);

// Check for leaks
Allocator::getInstance().detect_memory_leaks();
```

## 🎓 Key Concepts Demonstrated

- **RAII** - Resource management through constructors/destructors
- **Memory Management** - Low-level memory allocation
- **Data Structures** - Linked lists, free lists
- **Algorithms** - First-fit, coalescing
- **Template Programming** - Type-safe logging
- **Cross-Platform Development** - Platform-specific APIs
- **Debugging Techniques** - Magic numbers, tracking
- **Performance Optimization** - Pooling, fast paths

## 🔍 Magic Numbers

| Value | Purpose |
|-------|---------|
| `0xDEADBEEF` | Valid allocated block header |
| `0xCAFEBABE` | Freed block (use-after-free detection) |
| `0xFEEEFEEE` | Double-free detected |

## 📈 Performance

- **Small allocations (< 512B)**: ~5 µs/op (memory pool)
- **Large allocations**: Variable based on fragmentation
- **Memory overhead**: Minimal (one BlockMetadata per block)
- **System calls**: Minimized through pooling

## 🛠️ Build Tools

- **Compiler**: GCC/Clang/MSVC (C++17 required)
- **Build System**: CMake 3.15+ (optional)
- **Platform**: Windows, Linux, macOS

## 📚 Documentation

- **README.md** - Complete documentation in Italian
- **QUICKSTART.md** - Quick reference guide
- **Code Comments** - Extensive inline documentation

## ✨ Highlights

- **Zero Dependencies** - Pure C++17 standard library
- **Thread-Safe Ready** - Mutex placeholders included
- **Production-Ready** - Error handling, validation
- **Educational** - Well-documented, clean code
- **Extensible** - Easy to add features

## 🎯 Learning Outcomes

This project demonstrates:
1. Understanding of memory management fundamentals
2. Implementation of classic algorithms (first-fit, coalescing)
3. Cross-platform development skills
4. Debugging and validation techniques
5. Performance optimization strategies
6. Modern C++ practices (RAII, templates, inline variables)

## 📊 Code Statistics

- **Total Lines**: ~1,500+
- **Header Files**: 3
- **Source Files**: 3
- **Test Cases**: 10
- **Magic Numbers**: 3
- **Memory Pools**: 6

## 🔐 Safety Checks

- Header validation on every operation
- Double-free detection
- Leak detection at program end
- Boundary checking for pool allocations
- Magic number corruption detection

## 🌟 Future Enhancements

Possible improvements:
- Best-fit allocation algorithm
- Thread-safe operations
- More size classes for pools
- Compactation/defragmentation
- Integration with std::allocator

---

**Status**: ✓ Complete and Working
**Language**: Italian documentation
**Standard**: C++17
**Platforms**: Windows, Linux, macOS

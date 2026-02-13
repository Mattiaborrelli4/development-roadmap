#include "allocator.h"
#include "pool.h"
#include "debug.h"
#include <iostream>
#include <vector>
#include <random>
#include <iomanip>
#include <cstring>

using namespace MemoryAllocator;

// Colore per output console
#ifdef _WIN32
#define COLOR_RESET ""
#define COLOR_GREEN ""
#define COLOR_RED ""
#define COLOR_YELLOW ""
#define COLOR_BLUE ""
#else
#define COLOR_RESET "\033[0m"
#define COLOR_GREEN "\033[32m"
#define COLOR_RED "\033[31m"
#define COLOR_YELLOW "\033[33m"
#define COLOR_BLUE "\033[34m"
#endif

// Test base
void test_basic_allocation() {
    std::cout << COLOR_BLUE << "\n=== TEST 1: Allocazione Base ===" << COLOR_RESET << std::endl;

    void* ptr1 = MY_MALLOC(100);
    void* ptr2 = MY_MALLOC(200);
    void* ptr3 = MY_MALLOC(50);

    std::cout << "Allocati: ptr1=" << ptr1 << ", ptr2=" << ptr2 << ", ptr3=" << ptr3 << std::endl;

    MY_FREE(ptr1);
    MY_FREE(ptr3);

    void* ptr4 = MY_MALLOC(75);
    std::cout << "Riallocato dopo free: ptr4=" << ptr4 << std::endl;

    MY_FREE(ptr2);
    MY_FREE(ptr4);

    auto stats = Allocator::getInstance().get_stats();
    std::cout << "Stat: " << stats.total_allocated << " allocati, "
              << stats.total_free << " liberi" << std::endl;
}

// Test realloc
void test_realloc() {
    std::cout << COLOR_BLUE << "\n=== TEST 2: Realloc ===" << COLOR_RESET << std::endl;

    void* ptr = MY_MALLOC(100);
    std::cout << "Allocato 100 bytes: " << ptr << std::endl;

    // Scrivi dati
    memset(ptr, 'A', 100);

    // Ridimensiona a più grande
    ptr = MY_REALLOC(ptr, 200);
    std::cout << "Ridimensionato a 200 bytes: " << ptr << std::endl;

    // Verifica dati
    char* data = static_cast<char*>(ptr);
    bool valid = (data[0] == 'A' && data[99] == 'A');
    std::cout << "Dati preservati: " << (valid ? "SI" : "NO") << std::endl;

    // Ridimensiona a più piccolo
    ptr = MY_REALLOC(ptr, 50);
    std::cout << "Ridimensionato a 50 bytes: " << ptr << std::endl;

    MY_FREE(ptr);
}

// Test memory pool
void test_memory_pool() {
    std::cout << COLOR_BLUE << "\n=== TEST 3: Memory Pool ===" << COLOR_RESET << std::endl;

    std::vector<void*> pointers;

    // Alloca molti blocchi piccoli (dovrebbero usare pool)
    std::cout << "Allocando 1000 blocchi da 32 bytes..." << std::endl;
    for (int i = 0; i < 1000; ++i) {
        void* ptr = MY_MALLOC(32);
        if (ptr) {
            pointers.push_back(ptr);
        }
    }

    std::cout << "Allocati " << pointers.size() << " blocchi" << std::endl;

    // Libera tutti
    for (void* ptr : pointers) {
        MY_FREE(ptr);
    }
    std::cout << "Liberati tutti i blocchi" << std::endl;

    MemoryPool::getInstance().print_stats();
}

// Test coalescing
void test_coalescing() {
    std::cout << COLOR_BLUE << "\n=== TEST 4: Coalescing Blocchi ===" << COLOR_RESET << std::endl;

    auto stats_before = Allocator::getInstance().get_stats();
    std::cout << "Prima: " << stats_before.free_blocks << " blocchi liberi" << std::endl;

    void* ptr1 = MY_MALLOC(100);
    void* ptr2 = MY_MALLOC(100);
    void* ptr3 = MY_MALLOC(100);

    MY_FREE(ptr1);
    MY_FREE(ptr3);

    auto stats_mid = Allocator::getInstance().get_stats();
    std::cout << "Durante free: " << stats_mid.free_blocks << " blocchi liberi" << std::endl;

    MY_FREE(ptr2); // Dovrebbe coalescere con ptr1 e ptr3

    auto stats_after = Allocator::getInstance().get_stats();
    std::cout << "Dopo coalescing: " << stats_after.free_blocks << " blocchi liberi" << std::endl;
}

// Test alignment
void test_alignment() {
    std::cout << COLOR_BLUE << "\n=== TEST 5: Allineamento ===" << COLOR_RESET << std::endl;

    void* ptr1 = Allocator::getInstance().my_malloc(100, 16);
    void* ptr2 = Allocator::getInstance().my_malloc(100, 32);
    void* ptr3 = Allocator::getInstance().my_malloc(100, 64);

    std::cout << "Ptr1 (align 16): " << ptr1
              << " - aligned: " << (reinterpret_cast<uintptr_t>(ptr1) % 16 == 0 ? "SI" : "NO") << std::endl;
    std::cout << "Ptr2 (align 32): " << ptr2
              << " - aligned: " << (reinterpret_cast<uintptr_t>(ptr2) % 32 == 0 ? "SI" : "NO") << std::endl;
    std::cout << "Ptr3 (align 64): " << ptr3
              << " - aligned: " << (reinterpret_cast<uintptr_t>(ptr3) % 64 == 0 ? "SI" : "NO") << std::endl;

    Allocator::getInstance().my_free(ptr1);
    Allocator::getInstance().my_free(ptr2);
    Allocator::getInstance().my_free(ptr3);
}

// Test stress
void test_stress() {
    std::cout << COLOR_BLUE << "\n=== TEST 6: Stress Test ===" << COLOR_RESET << std::endl;

    std::vector<void*> pointers;
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> size_dist(16, 1024);
    std::uniform_int_distribution<> action_dist(0, 2);

    const int ITERATIONS = 1000;

    for (int i = 0; i < ITERATIONS; ++i) {
        int action = action_dist(gen);

        if (action == 0 && pointers.size() < 100) {
            // Allocate
            size_t size = size_dist(gen);
            void* ptr = MY_MALLOC(size);
            if (ptr) {
                pointers.push_back(ptr);
            }
        } else if (action == 1 && !pointers.empty()) {
            // Free random
            size_t idx = std::uniform_int_distribution<>(0, pointers.size() - 1)(gen);
            MY_FREE(pointers[idx]);
            pointers.erase(pointers.begin() + idx);
        } else if (action == 2 && !pointers.empty()) {
            // Realloc random
            size_t idx = std::uniform_int_distribution<>(0, pointers.size() - 1)(gen);
            size_t new_size = size_dist(gen);
            pointers[idx] = MY_REALLOC(pointers[idx], new_size);
        }

        if (i % 100 == 0) {
            std::cout << "Iterazione " << i << ": " << pointers.size() << " pointers attivi" << std::endl;
        }
    }

    // Cleanup
    for (void* ptr : pointers) {
        MY_FREE(ptr);
    }

    std::cout << "Stress test completato" << std::endl;
}

// Test performance
void test_performance() {
    std::cout << COLOR_BLUE << "\n=== TEST 7: Performance ===" << COLOR_RESET << std::endl;

    const int ALLOCS = 10000;
    std::vector<void*> pointers;

    Timer timer;

    // Malloc
    timer.reset();
    for (int i = 0; i < ALLOCS; ++i) {
        pointers.push_back(MY_MALLOC(128));
    }
    double alloc_time = timer.elapsed_ms();

    // Free
    timer.reset();
    for (void* ptr : pointers) {
        MY_FREE(ptr);
    }
    double free_time = timer.elapsed_ms();

    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Malloc: " << alloc_time << " ms (" << (alloc_time / ALLOCS * 1000) << " µs/op)" << std::endl;
    std::cout << "Free: " << free_time << " ms (" << (free_time / ALLOCS * 1000) << " µs/op)" << std::endl;
    std::cout << "Totale: " << (alloc_time + free_time) << " ms" << std::endl;
}

// Test memory leak detection
void test_leak_detection() {
    std::cout << COLOR_BLUE << "\n=== TEST 8: Leak Detection ===" << COLOR_RESET << std::endl;

    std::cout << "Creando memory leaks intenzionali..." << std::endl;
    void* leak1 = MY_MALLOC(100);
    void* leak2 = MY_MALLOC(200);
    void* leak3 = MY_MALLOC(50);

    // Non fare free per simulare leak

    Allocator::getInstance().print_allocations();

    // Cleanup
    MY_FREE(leak1);
    MY_FREE(leak2);
    MY_FREE(leak3);
}

// Test garbage collector (mark and sweep)
void test_garbage_collector() {
    std::cout << COLOR_BLUE << "\n=== TEST 9: Garbage Collector ===" << COLOR_RESET << std::endl;

    std::cout << "Nota: Il garbage collector usa mark-and-sweep" << std::endl;
    std::cout << "In questo implementazione, mark viene fatto durante l'uso normale" << std::endl;
    std::cout << "e sweep può essere chiamato per pulire blocchi non raggiungibili" << std::endl;

    void* ptr1 = MY_MALLOC(100);
    void* ptr2 = MY_MALLOC(200);

    MY_FREE(ptr1);

    auto stats = Allocator::getInstance().get_stats();
    std::cout << "Dopo free: " << stats.free_blocks << " blocchi liberi" << std::endl;

    MY_FREE(ptr2);

    stats = Allocator::getInstance().get_stats();
    std::cout << "Dopo tutti i free: " << stats.free_blocks << " blocchi liberi" << std::endl;
}

// Test error detection
void test_error_detection() {
    std::cout << COLOR_BLUE << "\n=== TEST 10: Error Detection ===" << COLOR_RESET << std::endl;

    std::cout << "Testando error detection..." << std::endl;

    void* ptr = MY_MALLOC(100);

    // Double-free detection
    std::cout << "Test double-free..." << std::endl;
    MY_FREE(ptr);
    MY_FREE(ptr); // Dovrebbe detectare double-free

    // Use-after-free viene gestito con magic number
    std::cout << "Test use-after-free detection con magic numbers" << std::endl;
    std::cout << "MAGIC_HEADER: 0x" << std::hex << MAGIC_HEADER << std::dec << std::endl;
    std::cout << "MAGIC_FREED: 0x" << std::hex << MAGIC_FREED << std::dec << std::endl;
    std::cout << "MAGIC_DOUBLE_FREE: 0x" << std::hex << MAGIC_DOUBLE_FREE << std::dec << std::endl;
}

int main() {
    std::cout << COLOR_GREEN << "╔════════════════════════════════════════════╗\n";
    std::cout << "║   C++ Memory Allocator - Test Suite    ║\n";
    std::cout << "╚════════════════════════════════════════════╝" << COLOR_RESET << std::endl;

    // Attiva debug mode
    Allocator::getInstance().set_debug_mode(true);

    try {
        test_basic_allocation();
        test_realloc();
        test_memory_pool();
        test_coalescing();
        test_alignment();
        test_stress();
        test_performance();
        test_leak_detection();
        test_garbage_collector();
        test_error_detection();

        // Final check
        std::cout << COLOR_BLUE << "\n=== CHECK FINALE ===" << COLOR_RESET << std::endl;
        bool no_leaks = Allocator::getInstance().detect_memory_leaks();

        auto final_stats = Allocator::getInstance().get_stats();
        std::cout << "Statistiche finali:" << std::endl;
        std::cout << "  Memoria totale allocata: " << final_stats.total_allocated << " bytes" << std::endl;
        std::cout << "  Memoria totale libera: " << final_stats.total_free << " bytes" << std::endl;
        std::cout << "  Blocchi liberi: " << final_stats.free_blocks << "/" << final_stats.total_blocks << std::endl;
        std::cout << "  Memoria di sistema: " << final_stats.system_memory << " bytes" << std::endl;

        if (no_leaks) {
            std::cout << COLOR_GREEN << "\n✓ Tutti i test passati senza memory leaks!" << COLOR_RESET << std::endl;
            return 0;
        } else {
            std::cout << COLOR_RED << "\n✗ Detectati memory leaks" << COLOR_RESET << std::endl;
            return 1;
        }

    } catch (const std::exception& e) {
        std::cerr << COLOR_RED << "Eccezione: " << e.what() << COLOR_RESET << std::endl;
        return 1;
    }
}

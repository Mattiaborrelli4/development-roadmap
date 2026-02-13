#ifndef ALLOCATOR_H
#define ALLOCATOR_H

#include <cstddef>
#include <cstdint>
#include <map>
#include <string>

// Magic numbers per detectare corruption
#define MAGIC_HEADER 0xDEADBEEF
#define MAGIC_FREED 0xCAFEBABE
#define MAGIC_DOUBLE_FREE 0xFEEEFEEE

namespace MemoryAllocator {

// Metadati del blocco di memoria
struct BlockMetadata {
    uint32_t magic;           // MAGIC_HEADER per validazione
    size_t size;              // Dimensione del blocco (escluso metadata)
    bool is_free;             // Flag di liberazione
    BlockMetadata* prev;      // Blocco precedente
    BlockMetadata* next;      // Blocco successivo
    size_t allocation_id;    // ID per debug tracking
};

// Statistiche dell'allocatore
struct AllocatorStats {
    size_t total_allocated;   // Memoria totale allocata
    size_t total_free;        // Memoria totale libera
    size_t free_blocks;       // Numero di blocchi liberi
    size_t total_blocks;      // Numero totale di blocchi
    size_t system_memory;     // Memoria richiesta al sistema
};

// Tracking allocation per debug
struct AllocationInfo {
    void* ptr;
    size_t size;
    const char* file;
    int line;
    size_t allocation_id;
};

// Classe principale dell'allocatore
class Allocator {
public:
    // Singleton instance
    static Allocator& getInstance();

    // Alloca memoria con allineamento
    void* my_malloc(size_t size, size_t alignment = 8, const char* file = nullptr, int line = 0);

    // Dealloca memoria
    void my_free(void* ptr, const char* file = nullptr, int line = 0);

    // Ridimensiona memoria
    void* my_realloc(void* ptr, size_t new_size, const char* file = nullptr, int line = 0);

    // Ottieni statistiche
    AllocatorStats get_stats() const;

    // Attiva/disattiva debug mode
    void set_debug_mode(bool enabled);

    // Detect memory leaks
    bool detect_memory_leaks();

    // Stampa tutte le allocations attive
    void print_allocations();

    // Pulisci tutto
    void cleanup();

private:
    Allocator();
    ~Allocator();

    // Previeni copy e move
    Allocator(const Allocator&) = delete;
    Allocator& operator=(const Allocator&) = delete;
    Allocator(Allocator&&) = delete;
    Allocator& operator=(Allocator&&) = delete;

    // Richiedi memoria al sistema
    void* request_memory(size_t size);

    // Trova blocco libero con first-fit
    BlockMetadata* find_free_block(size_t size);

    // Dividi blocco se troppo grande
    void split_block(BlockMetadata* block, size_t size);

    // Unisci blocchi adiacenti liberi (coalescing)
    void coalesce_blocks(BlockMetadata* block);

    // Valida header del blocco
    bool validate_block(BlockMetadata* block);

    // Mark per garbage collector
    void mark_blocks();

    // Sweep per garbage collector
    void sweep_blocks();

    // Genera allocation ID
    size_t generate_allocation_id();

    BlockMetadata* heap_start;    // Inizio dell'heap
    BlockMetadata* heap_end;      // Fine dell'heap
    size_t heap_size;             // Dimensione totale heap

    bool debug_mode;              // Debug mode flag
    std::map<void*, AllocationInfo> allocations;  // Tracking allocations
    std::map<size_t, void*> allocation_map;       // ID -> ptr mapping
    size_t next_allocation_id;    // Counter per ID

    AllocatorStats stats;
};

// Macro per debug tracking
#ifdef DEBUG_MODE
#define MY_MALLOC(size) Allocator::getInstance().my_malloc(size, 8, __FILE__, __LINE__)
#define MY_FREE(ptr) Allocator::getInstance().my_free(ptr, __FILE__, __LINE__)
#define MY_REALLOC(ptr, size) Allocator::getInstance().my_realloc(ptr, size, __FILE__, __LINE__)
#else
#define MY_MALLOC(size) Allocator::getInstance().my_malloc(size)
#define MY_FREE(ptr) Allocator::getInstance().my_free(ptr)
#define MY_REALLOC(ptr, size) Allocator::getInstance().my_realloc(ptr, size)
#endif

} // namespace MemoryAllocator

#endif // ALLOCATOR_H

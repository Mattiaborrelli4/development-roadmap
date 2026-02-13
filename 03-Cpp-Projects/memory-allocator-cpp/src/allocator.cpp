#include "allocator.h"
#include "pool.h"
#include "debug.h"
#include <iostream>
#include <cstring>
#include <cassert>

#ifdef _WIN32
#include <windows.h>
#else
#include <unistd.h>
#include <sys/mman.h>
#endif

namespace MemoryAllocator {

Allocator::Allocator()
    : heap_start(nullptr)
    , heap_end(nullptr)
    , heap_size(0)
    , debug_mode(false)
    , next_allocation_id(1)
    , stats{0, 0, 0, 0, 0}
{
    // Inizializza heap con dimensione iniziale
    const size_t INITIAL_HEAP_SIZE = 1024 * 1024; // 1 MB
    void* mem = request_memory(INITIAL_HEAP_SIZE);
    if (!mem) {
        std::cerr << "ERRORE: Impossibile allocare heap iniziale\n";
        return;
    }

    heap_start = static_cast<BlockMetadata*>(mem);
    heap_start->magic = MAGIC_HEADER;
    heap_start->size = INITIAL_HEAP_SIZE - sizeof(BlockMetadata);
    heap_start->is_free = true;
    heap_start->prev = nullptr;
    heap_start->next = nullptr;
    heap_start->allocation_id = 0;

    heap_end = reinterpret_cast<BlockMetadata*>(
        static_cast<char*>(mem) + INITIAL_HEAP_SIZE
    );
    heap_size = INITIAL_HEAP_SIZE;
    stats.system_memory = INITIAL_HEAP_SIZE;
    stats.total_free = heap_start->size;
    stats.total_blocks = 1;
    stats.free_blocks = 1;

    Debug::log("Allocator inizializzato con heap di %zu bytes", INITIAL_HEAP_SIZE);
}

Allocator::~Allocator() {
    cleanup();
}

Allocator& Allocator::getInstance() {
    static Allocator instance;
    return instance;
}

void* Allocator::request_memory(size_t size) {
#ifdef _WIN32
    // Windows: Usa HeapCreate o VirtualAlloc
    void* mem = VirtualAlloc(nullptr, size, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    if (mem) {
        stats.system_memory += size;
    }
    return mem;
#else
    // Unix: Usa mmap o sbrk
    void* mem = mmap(nullptr, size, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (mem != MAP_FAILED) {
        stats.system_memory += size;
        return mem;
    }
    return nullptr;
#endif
}

void* Allocator::my_malloc(size_t size, size_t alignment, const char* file, int line) {
    if (size == 0) {
        return nullptr;
    }

    // Arrotonda alla dimensione del metadata per allineamento
    size = (size + 7) & ~7;

    // Usa pool per allocazioni piccole (< 512 bytes)
    if (size < 512) {
        void* ptr = MemoryPool::getInstance().allocate(size);
        if (ptr) {
            size_t alloc_id = generate_allocation_id();
            AllocationInfo info{ptr, size, file, line, alloc_id};
            allocations[ptr] = info;
            allocation_map[alloc_id] = ptr;

            stats.total_allocated += size;
            Debug::log_alloc(alloc_id, size, file, line);
            return ptr;
        }
    }

    // Cerca blocco libero con first-fit
    BlockMetadata* block = find_free_block(size);

    // Se non trovato, richiedi più memoria al sistema
    if (!block) {
        const size_t ADDITIONAL_SIZE = size + sizeof(BlockMetadata) + 4096;
        void* new_mem = request_memory(ADDITIONAL_SIZE);
        if (!new_mem) {
            Debug::log_error("Malloc fallito: out of memory", file, line);
            return nullptr;
        }

        // Inizializza nuovo blocco
        BlockMetadata* new_block = static_cast<BlockMetadata*>(new_mem);
        new_block->magic = MAGIC_HEADER;
        new_block->size = ADDITIONAL_SIZE - sizeof(BlockMetadata);
        new_block->is_free = true;
        new_block->prev = heap_end;
        new_block->next = nullptr;
        new_block->allocation_id = 0;

        // Collega alla lista
        if (heap_end) {
            heap_end->next = new_block;
        }
        heap_end = reinterpret_cast<BlockMetadata*>(
            static_cast<char*>(new_mem) + ADDITIONAL_SIZE
        );

        stats.total_free += new_block->size;
        stats.total_blocks++;
        stats.free_blocks++;

        // Coalescing con blocco precedente
        coalesce_blocks(new_block);

        // Riprova allocation
        block = find_free_block(size);
    }

    if (!block) {
        Debug::log_error("Malloc fallito: impossibile trovare blocco", file, line);
        return nullptr;
    }

    // Dividi blocco se necessario
    if (block->size > size + sizeof(BlockMetadata) + 8) {
        split_block(block, size);
    }

    // Marca come usato
    block->is_free = false;

    size_t alloc_id = generate_allocation_id();
    block->allocation_id = alloc_id;

    void* ptr = static_cast<void*>(static_cast<char*>(static_cast<void*>(block)) + sizeof(BlockMetadata));

    // Tracking
    AllocationInfo info{ptr, block->size, file, line, alloc_id};
    allocations[ptr] = info;
    allocation_map[alloc_id] = ptr;

    stats.total_allocated += block->size;
    stats.total_free -= block->size;
    stats.free_blocks--;

    Debug::log_alloc(alloc_id, block->size, file, line);

    return ptr;
}

void Allocator::my_free(void* ptr, const char* file, int line) {
    if (!ptr) {
        return;
    }

    // Check se è dal pool
    if (MemoryPool::getInstance().is_from_pool(ptr)) {
        auto it = allocations.find(ptr);
        if (it != allocations.end()) {
            stats.total_allocated -= it->second.size;
            allocation_map.erase(it->second.allocation_id);
            Debug::log_free(it->second.allocation_id, file, line);
            allocations.erase(it);
        }
        MemoryPool::getInstance().deallocate(ptr);
        return;
    }

    // Ottieni metadata
    BlockMetadata* block = reinterpret_cast<BlockMetadata*>(
        static_cast<char*>(ptr) - static_cast<ptrdiff_t>(sizeof(BlockMetadata))
    );

    // Valida block
    if (!validate_block(block)) {
        Debug::log_error("Free fallito: header corrotto", file, line);
        return;
    }

    // Detect double-free
    if (block->is_free) {
        Debug::log_error_double_free(block->allocation_id, file, line);
        block->magic = MAGIC_DOUBLE_FREE;
        return;
    }

    // Remove tracking
    auto it = allocations.find(ptr);
    if (it != allocations.end()) {
        stats.total_allocated -= block->size;
        allocation_map.erase(it->second.allocation_id);
        Debug::log_free(block->allocation_id, file, line);
        allocations.erase(it);
    }

    // Marca come libero
    block->is_free = true;
    block->magic = MAGIC_FREED;

    stats.total_free += block->size;
    stats.free_blocks++;

    // Coalescing con blocchi adiacenti
    coalesce_blocks(block);
}

void* Allocator::my_realloc(void* ptr, size_t new_size, const char* file, int line) {
    if (!ptr) {
        return my_malloc(new_size, 8, file, line);
    }

    if (new_size == 0) {
        my_free(ptr, file, line);
        return nullptr;
    }

    // Check se è dal pool
    if (MemoryPool::getInstance().is_from_pool(ptr)) {
        void* new_ptr = my_malloc(new_size, 8, file, line);
        if (new_ptr) {
            size_t old_size = MemoryPool::getInstance().get_block_size(ptr);
            std::memcpy(new_ptr, ptr, std::min(old_size, new_size));
            my_free(ptr, file, line);
        }
        return new_ptr;
    }

    BlockMetadata* block = reinterpret_cast<BlockMetadata*>(
        static_cast<char*>(ptr) - static_cast<ptrdiff_t>(sizeof(BlockMetadata))
    );

    if (!validate_block(block)) {
        Debug::log_error("Realloc fallito: header corrotto", file, line);
        return nullptr;
    }

    size_t old_size = block->size;

    // Se nuova dimensione è minore, ritorna stesso ptr
    if (new_size <= old_size) {
        return ptr;
    }

    // Prova ad espandere blocco
    if (block->next && block->next->is_free &&
        block->size + block->next->size + sizeof(BlockMetadata) >= new_size) {

        // Assorbi blocco successivo
        BlockMetadata* next_block = block->next;
        block->size += next_block->size + sizeof(BlockMetadata);
        block->next = next_block->next;
        if (next_block->next) {
            next_block->next->prev = block;
        }

        stats.total_free -= next_block->size;
        stats.free_blocks--;
        stats.total_blocks--;

        Debug::log("Blocco espanso da %zu a %zu bytes", old_size, block->size);
        return ptr;
    }

    // Alloca nuovo blocco
    void* new_ptr = my_malloc(new_size, 8, file, line);
    if (!new_ptr) {
        return nullptr;
    }

    // Copia dati
    std::memcpy(new_ptr, ptr, old_size);
    my_free(ptr, file, line);

    return new_ptr;
}

BlockMetadata* Allocator::find_free_block(size_t size) {
    BlockMetadata* current = heap_start;
    while (current) {
        if (current->is_free && current->size >= size) {
            return current;
        }
        current = current->next;
    }
    return nullptr;
}

void Allocator::split_block(BlockMetadata* block, size_t size) {
    if (block->size < size + sizeof(BlockMetadata) + 8) {
        return;
    }

    BlockMetadata* new_block = reinterpret_cast<BlockMetadata*>(
        static_cast<char*>(static_cast<void*>(block)) + sizeof(BlockMetadata) + size
    );

    new_block->magic = MAGIC_HEADER;
    new_block->size = block->size - size - sizeof(BlockMetadata);
    new_block->is_free = true;
    new_block->prev = block;
    new_block->next = block->next;
    new_block->allocation_id = 0;

    block->size = size;
    block->next = new_block;

    if (new_block->next) {
        new_block->next->prev = new_block;
    }

    stats.total_blocks++;
    stats.free_blocks++;
}

void Allocator::coalesce_blocks(BlockMetadata* block) {
    if (!block || !block->is_free) {
        return;
    }

    // Coalescing con blocco successivo
    if (block->next && block->next->is_free) {
        BlockMetadata* next_block = block->next;

        block->size += next_block->size + sizeof(BlockMetadata);
        block->next = next_block->next;

        if (next_block->next) {
            next_block->next->prev = block;
        }

        stats.total_blocks--;
        stats.free_blocks--;
        stats.total_free = stats.total_free; // Rimane invariato
    }

    // Coalescing con blocco precedente
    if (block->prev && block->prev->is_free) {
        BlockMetadata* prev_block = block->prev;

        prev_block->size += block->size + sizeof(BlockMetadata);
        prev_block->next = block->next;

        if (block->next) {
            block->next->prev = prev_block;
        }

        stats.total_blocks--;
        stats.free_blocks--;
    }
}

bool Allocator::validate_block(BlockMetadata* block) {
    if (!block) {
        return false;
    }

    if (block->magic == MAGIC_DOUBLE_FREE) {
        Debug::log_error("Detectato double-free");
        return false;
    }

    if (block->magic != MAGIC_HEADER && block->magic != MAGIC_FREED) {
        Debug::log_error("Detectato header corrotto");
        return false;
    }

    return true;
}

void Allocator::mark_blocks() {
    // Marca tutti i blocchi raggiungibili
    for (const auto& [ptr, info] : allocations) {
        BlockMetadata* block = reinterpret_cast<BlockMetadata*>(
            static_cast<char*>(ptr) - static_cast<ptrdiff_t>(sizeof(BlockMetadata))
        );
        if (validate_block(block)) {
            block->magic = MAGIC_HEADER; // Mark as reachable
        }
    }
}

void Allocator::sweep_blocks() {
    // Libera blocchi non marcati
    BlockMetadata* current = heap_start;
    while (current) {
        if (current->is_free && current->magic != MAGIC_HEADER) {
            // Blocco non raggiungibile, può essere liberato
            current->magic = MAGIC_FREED;
        }
        current = current->next;
    }
}

size_t Allocator::generate_allocation_id() {
    return next_allocation_id++;
}

AllocatorStats Allocator::get_stats() const {
    return stats;
}

void Allocator::set_debug_mode(bool enabled) {
    debug_mode = enabled;
    Debug::set_enabled(enabled);
}

bool Allocator::detect_memory_leaks() {
    if (allocations.empty()) {
        Debug::log("Nessun memory leak detectato");
        return true;
    }

    Debug::log_error("Memory leaks detectati");
    print_allocations();
    return false;
}

void Allocator::print_allocations() {
    if (allocations.empty()) {
        Debug::log("Nessuna allocazione attiva");
        return;
    }

    Debug::log("=== Allocazioni Attive (%zu) ===", allocations.size());
    for (const auto& [ptr, info] : allocations) {
        Debug::log("  ID: %zu, Ptr: %p, Size: %zu bytes, File: %s:%d",
                   info.allocation_id, info.ptr, info.size,
                   info.file ? info.file : "unknown", info.line);
    }
}

void Allocator::cleanup() {
    // Libera memoria al sistema
#ifdef _WIN32
    if (heap_start) {
        VirtualFree(heap_start, 0, MEM_RELEASE);
    }
#else
    if (heap_start) {
        munmap(heap_start, heap_size);
    }
#endif

    heap_start = nullptr;
    heap_end = nullptr;
    heap_size = 0;
    allocations.clear();
    allocation_map.clear();
}

} // namespace MemoryAllocator

#include "pool.h"
#include "debug.h"
#include <cstring>
#include <cassert>

#ifdef _WIN32
#include <windows.h>
#else
#include <sys/mman.h>
#endif

namespace MemoryAllocator {

FixedSizePool::FixedSizePool(size_t block_size, size_t blocks_per_chunk)
    : block_size_(block_size)
    , blocks_per_chunk_(blocks_per_chunk)
    , total_blocks_(0)
    , free_blocks_(0)
    , free_list_(nullptr)
    , chunks_(nullptr)
    , pool_start_(nullptr)
    , pool_end_(nullptr)
{
    allocate_chunk();
}

FixedSizePool::~FixedSizePool() {
    // Libera tutti i chunks
    Chunk* current = chunks_;
    while (current) {
        Chunk* next = current->next;
#ifdef _WIN32
        VirtualFree(current->memory, 0, MEM_RELEASE);
#else
        munmap(current->memory, block_size_ * blocks_per_chunk_);
#endif
        delete current;
        current = next;
    }
}

void FixedSizePool::allocate_chunk() {
    size_t chunk_size = block_size_ * blocks_per_chunk_;

#ifdef _WIN32
    void* memory = VirtualAlloc(nullptr, chunk_size, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
#else
    void* memory = mmap(nullptr, chunk_size, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
#endif

    if (!memory) {
        Debug::log_error("Impossibile allocare chunk per pool");
        return;
    }

    // Crea chunk node
    Chunk* chunk = new Chunk{memory, chunks_};
    chunks_ = chunk;

    // Inizializza free list
    char* ptr = static_cast<char*>(memory);
    for (size_t i = 0; i < blocks_per_chunk_; ++i) {
        FreeNode* node = reinterpret_cast<FreeNode*>(ptr);
        node->next = free_list_;
        free_list_ = node;
        ptr += block_size_;
    }

    total_blocks_ += blocks_per_chunk_;
    free_blocks_ += blocks_per_chunk_;

    // Update pool bounds
    if (!pool_start_) {
        pool_start_ = memory;
    }
    pool_end_ = static_cast<char*>(memory) + chunk_size;

    Debug::log("Allocato nuovo chunk: %zu blocchi da %zu bytes", blocks_per_chunk_, block_size_);
}

void* FixedSizePool::allocate() {
    if (!free_list_) {
        allocate_chunk();
        if (!free_list_) {
            return nullptr;
        }
    }

    FreeNode* node = free_list_;
    free_list_ = node->next;
    free_blocks_--;

    return static_cast<void*>(node);
}

void FixedSizePool::deallocate(void* ptr) {
    if (!ptr) {
        return;
    }

    // Check bounds
    if (ptr < pool_start_ || ptr >= pool_end_) {
        Debug::log_error("Deallocation fallita: pointer fuori dal pool");
        return;
    }

    FreeNode* node = static_cast<FreeNode*>(ptr);
    node->next = free_list_;
    free_list_ = node;
    free_blocks_++;
}

bool FixedSizePool::is_from_pool(void* ptr) const {
    return ptr >= pool_start_ && ptr < pool_end_;
}

MemoryPool::MemoryPool() {
    // Inizializza pools per diverse dimensioni
    for (size_t i = 0; i < NUM_POOLS; ++i) {
        size_t block_size = POOL_SIZES[i];
        size_t blocks_per_chunk = 4096 / block_size; // Chunk di 4KB
        pools_[i] = new FixedSizePool(block_size, blocks_per_chunk);
    }

    Debug::log("MemoryPool inizializzato con %zu pools", NUM_POOLS);
}

MemoryPool::~MemoryPool() {
    for (size_t i = 0; i < NUM_POOLS; ++i) {
        delete pools_[i];
    }
}

MemoryPool& MemoryPool::getInstance() {
    static MemoryPool instance;
    return instance;
}

void* MemoryPool::allocate(size_t size) {
    if (size == 0) {
        return nullptr;
    }

    FixedSizePool* pool = find_pool(size);
    if (!pool) {
        return nullptr;
    }

    return pool->allocate();
}

void MemoryPool::deallocate(void* ptr) {
    if (!ptr) {
        return;
    }

    // Trova pool corretto
    for (size_t i = 0; i < NUM_POOLS; ++i) {
        if (pools_[i]->is_from_pool(ptr)) {
            pools_[i]->deallocate(ptr);
            return;
        }
    }

    Debug::log_error("Deallocation fallita: pointer non in nessun pool");
}

bool MemoryPool::is_from_pool(void* ptr) const {
    for (size_t i = 0; i < NUM_POOLS; ++i) {
        if (pools_[i]->is_from_pool(ptr)) {
            return true;
        }
    }
    return false;
}

size_t MemoryPool::get_block_size(void* ptr) const {
    for (size_t i = 0; i < NUM_POOLS; ++i) {
        if (pools_[i]->is_from_pool(ptr)) {
            return pools_[i]->get_block_size();
        }
    }
    return 0;
}

FixedSizePool* MemoryPool::find_pool(size_t size) {
    // Trova pool con blocco più piccolo che può contenere size
    for (size_t i = 0; i < NUM_POOLS; ++i) {
        if (size <= POOL_SIZES[i]) {
            return pools_[i];
        }
    }
    return nullptr;
}

void MemoryPool::print_stats() const {
    Debug::log("=== Memory Pool Statistics ===");
    for (size_t i = 0; i < NUM_POOLS; ++i) {
        Debug::log("Pool %zu: blocco=%zu bytes, totale=%zu, liberi=%zu",
                   i, pools_[i]->get_block_size(),
                   pools_[i]->get_total_blocks(),
                   pools_[i]->get_free_blocks());
    }
}

} // namespace MemoryAllocator

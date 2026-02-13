#ifndef POOL_H
#define POOL_H

#include <cstddef>
#include <cstdint>

namespace MemoryAllocator {

// Pool per blocchi di dimensione fissa
class FixedSizePool {
public:
    FixedSizePool(size_t block_size, size_t blocks_per_chunk);
    ~FixedSizePool();

    // Alloca dal pool
    void* allocate();

    // Dealloca al pool
    void deallocate(void* ptr);

    // Check se ptr è dal pool
    bool is_from_pool(void* ptr) const;

    // Ottieni dimensione blocco
    size_t get_block_size() const { return block_size_; }

    // Statistiche
    size_t get_total_blocks() const { return total_blocks_; }
    size_t get_free_blocks() const { return free_blocks_; }

private:
    // Chunk di memoria
    struct Chunk {
        void* memory;
        Chunk* next;
    };

    // Nodo libero
    struct FreeNode {
        FreeNode* next;
    };

    // Alloca nuovo chunk
    void allocate_chunk();

    size_t block_size_;         // Dimensione di ogni blocco
    size_t blocks_per_chunk_;   // Numero di blocchi per chunk
    size_t total_blocks_;       // Totale blocchi allocati
    size_t free_blocks_;        // Blocchi liberi

    FreeNode* free_list_;       // Lista di blocchi liberi
    Chunk* chunks_;             // Lista di chunks

    void* pool_start_;          // Inizio del pool
    void* pool_end_;            // Fine del pool
};

// Memory pool manager
class MemoryPool {
public:
    static MemoryPool& getInstance();

    // Alloca con pool appropriato
    void* allocate(size_t size);

    // Dealloca
    void deallocate(void* ptr);

    // Check se ptr è da un pool
    bool is_from_pool(void* ptr) const;

    // Ottieni dimensione blocco
    size_t get_block_size(void* ptr) const;

    // Statistiche totali
    void print_stats() const;

private:
    MemoryPool();
    ~MemoryPool();

    // Previeni copy e move
    MemoryPool(const MemoryPool&) = delete;
    MemoryPool& operator=(const MemoryPool&) = delete;
    MemoryPool(MemoryPool&&) = delete;
    MemoryPool& operator=(MemoryPool&&) = delete;

    // Trova pool appropriato per dimensione
    FixedSizePool* find_pool(size_t size);

    static constexpr size_t NUM_POOLS = 6;
    static constexpr size_t POOL_SIZES[NUM_POOLS] = {
        16, 32, 64, 128, 256, 512
    };

    FixedSizePool* pools_[NUM_POOLS];
};

} // namespace MemoryAllocator

#endif // POOL_H

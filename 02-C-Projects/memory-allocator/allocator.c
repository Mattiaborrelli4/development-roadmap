/**
 * @file allocator.c
 * @brief Implementazione del memory allocator personalizzato
 *
 * Implementazione di malloc(), free() e realloc() usando Heap API (Windows)
 * Include coalescing automatico, splitting e detection errori
 */

#define _CRT_SECURE_NO_WARNINGS  /* Disable warnings per sprintf */
#include "allocator.h"
#include <windows.h>
#include <stdio.h>

/* Heap handle per Windows */
static HANDLE g_heap = NULL;

/* Puntatore alla testa della lista dei blocchi */
static BlockHeader *g_head = NULL;

/* Statistiche */
static size_t g_total_allocated = 0;
static size_t g_total_blocks = 0;
static size_t g_free_blocks = 0;

/**
 * @brief Calcola la dimensione allineata
 *
 * Allinea la dimensione a multipli di ALIGNMENT bytes
 * per ottimizzazione delle performance CPU
 */
static size_t align_size(size_t size) {
    if (size == 0) return ALIGNMENT;
    return (size + ALIGNMENT - 1) & ~(ALIGNMENT - 1);
}

/**
 * @brief Trova un blocco libero adatto
 *
 * Strategy: First-fit (cerca il primo blocco libero sufficientemente grande)
 *
 * @param size Dimensione richiesta (allineata)
 * @return BlockHeader* Puntatore al blocco trovato o NULL
 */
static BlockHeader *find_free_block(size_t size) {
    BlockHeader *current = g_head;

    while (current != NULL) {
        if (current->is_free && current->size >= size) {
            return current;  /* First-fit */
        }
        current = current->next;
    }

    return NULL;  /* Nessun blocco libero trovato */
}

/**
 * @brief Divide un blocco grande in due blocchi
 *
 * Se il blocco è molto più grande di necessario,
 * lo divide per ridurre lo spreco di memoria (internal fragmentation)
 *
 * @param block Blocco da dividere
 * @param size Dimensione richiesta
 */
static void split_block(BlockHeader *block, size_t size) {
    /* Calcola la dimensione minima per un blocco valido */
    size_t min_block_size = sizeof(BlockHeader) + ALIGNMENT;

    /* Se non c'è abbastanza spazio per un nuovo blocco, non dividere */
    if (block->size < size + min_block_size) {
        return;
    }

    /* Crea un nuovo blocco con lo spazio restante */
    BlockHeader *new_block = (BlockHeader *)((char *)block + size);

    new_block->size = block->size - size;
    new_block->is_free = 1;
    new_block->magic = MAGIC_NUMBER;
    new_block->prev = block;
    new_block->next = block->next;

    /* Aggiorna il blocco corrente */
    block->size = size;
    block->next = new_block;

    /* Aggiorna il blocco successivo (se esiste) */
    if (new_block->next != NULL) {
        new_block->next->prev = new_block;
    }

    g_free_blocks++;  /* Nuovo blocco libero creato */
}

/**
 * @brief Fonde blocchi adiacenti liberi (coalescing)
 *
 * Riduce la frammentazione esterna unendo blocchi liberi contigui
 *
 * @param block Blocco da cui iniziare il coalescing
 */
static void coalesce_blocks(BlockHeader *block) {
    /* Coalescing con il blocco successivo */
    if (block->next != NULL && block->next->is_free) {
        block->size += block->next->size;
        block->next = block->next->next;

        if (block->next != NULL) {
            block->next->prev = block;
        }

        g_free_blocks--;  /* Un blocco libero in meno */
    }

    /* Coalescing con il blocco precedente */
    if (block->prev != NULL && block->prev->is_free) {
        block->prev->size += block->size;
        block->prev->next = block->next;

        if (block->next != NULL) {
            block->next->prev = block->prev;
        }

        g_free_blocks--;  /* Un blocco libero in meno */
    }
}

/**
 * @brief Richiede nuova memoria al sistema
 *
 * @param size Dimensione richiesta
 * @return BlockHeader* Puntatore al nuovo blocco
 */
static BlockHeader *request_memory(size_t size) {
    BlockHeader *block;

    /* Allinea la dimensione per Windows Heap */
    size_t total_size = align_size(size);

    /* Alloca dal Windows Heap */
    block = (BlockHeader *)HeapAlloc(g_heap, 0, total_size);

    if (block == NULL) {
        fprintf(stderr, "ERRORE: HeapAlloc fallito per %zu bytes\n", total_size);
        return NULL;
    }

    /* Inizializza il blocco */
    block->size = total_size;
    block->is_free = 0;
    block->magic = MAGIC_NUMBER;
    block->next = NULL;
    block->prev = NULL;

    /* Aggiungi alla lista dei blocchi */
    if (g_head == NULL) {
        g_head = block;
    } else {
        /* Trova l'ultimo blocco */
        BlockHeader *current = g_head;
        while (current->next != NULL) {
            current = current->next;
        }
        current->next = block;
        block->prev = current;
    }

    g_total_allocated += total_size;
    g_total_blocks++;

    return block;
}

/**
 * @brief Verifica la validità di un puntatore
 *
 * Controlla che il puntatore sia stato allocato dal nostro allocator
 * e che il magic number sia corretto
 *
 * @param ptr Puntatore da verificare
 * @return BlockHeader* Header del blocco o NULL se invalido
 */
static BlockHeader *get_valid_block(void *ptr) {
    if (ptr == NULL) {
        fprintf(stderr, "ERRORE: Tentativo di liberare puntatore NULL\n");
        return NULL;
    }

    BlockHeader *block = (BlockHeader *)ptr - 1;

    /* Verifica il magic number */
    if (block->magic != MAGIC_NUMBER) {
        fprintf(stderr, "ERRORE: Invalid free - magic number non valido (0x%llX)\n",
                block->magic);
        return NULL;
    }

    /* Verifica che il blocco sia nella nostra lista */
    BlockHeader *current = g_head;
    while (current != NULL) {
        if (current == block) {
            return block;
        }
        current = current->next;
    }

    fprintf(stderr, "ERRORE: Invalid free - blocco non trovato nella lista\n");
    return NULL;
}

/**
 * @brief Alloca un blocco di memoria
 */
void *my_malloc(size_t size) {
    if (size == 0) {
        return NULL;  /* malloc(0) è definito come NULL o unique pointer */
    }

    /* Allinea la dimensione e aggiungi spazio per l'header */
    size_t total_size = align_size(size + sizeof(BlockHeader));

    /* Cerca un blocco libero esistente */
    BlockHeader *block = find_free_block(total_size);

    if (block != NULL) {
        /* Blocco libero trovato */
        split_block(block, total_size);
        block->is_free = 0;
        g_free_blocks--;
        return (void *)(block + 1);
    }

    /* Nessun blocco libero, richiedi nuova memoria */
    block = request_memory(total_size);

    if (block == NULL) {
        return NULL;  /* Fallimento allocazione */
    }

    return (void *)(block + 1);
}

/**
 * @brief Dealloca un blocco di memoria
 */
void my_free(void *ptr) {
    BlockHeader *block = get_valid_block(ptr);

    if (block == NULL) {
        return;  /* Errore già stampato da get_valid_block */
    }

    /* Detection di double-free */
    if (block->is_free) {
        fprintf(stderr, "ERRORE: Double-free detected all'indirizzo %p\n", ptr);
        return;
    }

    /* Mark come libero */
    block->is_free = 1;
    g_free_blocks++;

    /* Coalescing con blocchi adiacenti */
    coalesce_blocks(block);
}

/**
 * @brief Ridimensiona un blocco di memoria
 */
void *my_realloc(void *ptr, size_t size) {
    /* Se ptr è NULL, equivale a malloc(size) */
    if (ptr == NULL) {
        return my_malloc(size);
    }

    /* Se size è 0, equivale a free(ptr) */
    if (size == 0) {
        my_free(ptr);
        return NULL;
    }

    /* Verifica validità del puntatore */
    BlockHeader *block = get_valid_block(ptr);
    if (block == NULL) {
        return NULL;
    }

    /* Allinea la nuova dimensione */
    size_t new_size = align_size(size + sizeof(BlockHeader));

    /* Se il blocco corrente è sufficientemente grande, riutilizzalo */
    if (block->size >= new_size) {
        /* Se è molto più grande, dividi il blocco */
        split_block(block, new_size);
        return ptr;
    }

    /* Il blocco è troppo piccolo, cerca di espanderlo */
    /* Verifica se il blocco successivo è libero e abbastanza grande */
    size_t extra_needed = new_size - block->size;

    if (block->next != NULL && block->next->is_free) {
        size_t available = block->next->size;

        if (available >= extra_needed) {
            /* Fonde con il blocco successivo */
            block->size += available;
            block->next = block->next->next;

            if (block->next != NULL) {
                block->next->prev = block;
            }

            g_free_blocks--;

            /* Dividi se necessario */
            split_block(block, new_size);
            return ptr;
        }
    }

    /* Non possiamo espandere, alloca un nuovo blocco */
    void *new_ptr = my_malloc(size);

    if (new_ptr == NULL) {
        return NULL;  /* Fallimento */
    }

    /* Copia i dati vecchi nel nuovo blocco */
    size_t old_data_size = block->size - sizeof(BlockHeader);
    size_t copy_size = (old_data_size < size) ? old_data_size : size;

    memcpy(new_ptr, ptr, copy_size);

    /* Libera il vecchio blocco */
    my_free(ptr);

    return new_ptr;
}

/**
 * @brief Stampa statistiche dell'allocator
 */
void print_allocator_stats(void) {
    size_t used_memory = 0;
    size_t free_memory = 0;
    size_t total_heap = 0;
    BlockHeader *current = g_head;

    while (current != NULL) {
        total_heap += current->size;
        if (current->is_free) {
            free_memory += current->size - sizeof(BlockHeader);
        } else {
            used_memory += current->size - sizeof(BlockHeader);
        }
        current = current->next;
    }

    printf("\n=== Memory Allocator Statistics ===\n");
    printf("Blocchi totali:        %zu\n", g_total_blocks);
    printf("Blocchi liberi:        %zu\n", g_free_blocks);
    printf("Blocchi occupati:      %zu\n", g_total_blocks - g_free_blocks);
    printf("Memoria usata:         %zu bytes\n", used_memory);
    printf("Memoria libera:        %zu bytes\n", free_memory);
    printf("Memoria totale heap:   %zu bytes\n", total_heap);
    printf("Overhead metadata:     %zu bytes\n",
           g_total_blocks * sizeof(BlockHeader));

    if (total_heap > 0) {
        double fragmentation = (free_memory > 0) ?
            (100.0 * (double)g_free_blocks * sizeof(BlockHeader) / free_memory) : 0.0;
        printf("Frammentazione est.:   %.2f%%\n", fragmentation);
    }
    printf("===================================\n\n");
}

/**
 * @brief Inizializza l'allocator (chiamata automaticamente)
 */
static void allocator_init(void) {
    if (g_heap == NULL) {
        /* Crea l'heap per Windows */
        g_heap = HeapCreate(0, 0, 0);

        if (g_heap == NULL) {
            fprintf(stderr, "ERRORE FATALE: HeapCreate fallito\n");
            exit(1);
        }
    }
}

/**
 * @brief Pulisce tutta la memoria allocata
 */
void allocator_cleanup(void) {
    if (g_heap != NULL) {
        /* Distruggi l'heap (dealloca tutto) */
        HeapDestroy(g_heap);
        g_heap = NULL;
        g_head = NULL;
        g_total_allocated = 0;
        g_total_blocks = 0;
        g_free_blocks = 0;
    }
}

/* Inizializzazione automatica all'avvio */
#ifdef _WIN32
#pragma comment(lib, "kernel32.lib")
/* Initializer eseguito prima di main() */
static void __cdecl initializer(void) {
    allocator_init();
}

/* Aggiungi alla lista di inizializzazione */
#pragma section(".CRT$XCU", read)
__declspec(allocate(".CRT$XCU")) void (*_initializer)(void) = initializer;
#endif

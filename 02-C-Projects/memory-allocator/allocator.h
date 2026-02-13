/**
 * @file allocator.h
 * @brief Header file per il memory allocator personalizzato
 *
 * Implementazione di malloc(), free() e realloc() da zero
 * Utilizza Heap API per Windows (compatibile con sbrk() su Unix)
 */

#ifndef ALLOCATOR_H
#define ALLOCATOR_H

#include <stddef.h>
#include <stdint.h>

/**
 * @brief Struttura per il metadata di ogni blocco di memoria
 *
 * Ogni blocco allocato contiene questo header prima dell'indirizzo
 * restituito all'utente. La struttura contiene:
 * - size: Dimensione totale del blocco (incluso l'header)
 * - is_free: Flag che indica se il blocco è libero (1) o occupato (0)
 * - next: Puntatore al prossimo blocco nella lista
 * - prev: Puntatore al blocco precedente nella lista
 */
typedef struct BlockHeader {
    size_t size;              /* Dimensione totale del blocco (incluso header) */
    int is_free;              /* 1 = libero, 0 = occupato */
    struct BlockHeader *next;  /* Puntatore al prossimo blocco */
    struct BlockHeader *prev;  /* Puntatore al blocco precedente */
    uint64_t magic;           /* Magic number per detection double-free */
} BlockHeader;

#define MAGIC_NUMBER 0xDEADBEEFCAFEBABE  /* Magic number per verifiche */
#define ALIGNMENT 16                     /* Allineamento memoria (16 bytes) */

/**
 * @brief Alloca un blocco di memoria della dimensione specificata
 *
 * @param size Numero di bytes da allocare
 * @return void* Puntatore alla memoria allocata, NULL se fallimento
 *
 * Implementazione personalizzata di malloc:
 * - Cerca blocchi liberi nella free list
 * - Splitting se il blocco è troppo grande
 * - Richiede nuova memoria al sistema se necessario
 * - Allineamento a 16 bytes per performance
 */
void *my_malloc(size_t size);

/**
 * @brief Dealloca un blocco di memoria precedentemente allocato
 *
 * @param ptr Puntatore alla memoria da liberare
 *
 * Implementazione personalizzata di free:
 * - Verifica validità del puntatore (magic number check)
 * - Detection di double-free
 * - Mark del blocco come libero
 * - Coalescing automatico con blocchi adiacenti liberi
 * - Inserimento nella free list
 */
void my_free(void *ptr);

/**
 * @brief Ridimensiona un blocco di memoria allocato
 *
 * @param ptr Puntatore al blocco da ridimensionare (NULL = malloc)
 * @param size Nuova dimensione richiesta (0 = free)
 * @return void* Puntatore alla memoria ridimensionata
 *
 * Implementazione personalizzata di realloc:
 * - Se ptr è NULL, equivale a my_malloc(size)
 * - Se size è 0, equivale a my_free(ptr)
 * - Se il blocco corrente è sufficientemente grande, lo riutilizza
 * - Altrimenti alloca un nuovo blocco e copia i dati
 * - Ottimizzazione per evitare copie non necessarie
 */
void *my_realloc(void *ptr, size_t size);

/**
 * @brief Stampa statistiche sull'allocazione memoria
 *
 * Utile per debugging e analisi performance:
 * - Numero di blocchi allocati
 * - Numero di blocchi liberi
 * - Memoria totale utilizzata
 * - Frammentazione della memoria
 */
void print_allocator_stats(void);

/**
 * @brief Pulisce tutta la memoria allocata
 *
 * Dealloca tutto l'heap e resetta l'allocator.
 * Utile per test e per evitare memory leak report.
 */
void allocator_cleanup(void);

#endif /* ALLOCATOR_H */

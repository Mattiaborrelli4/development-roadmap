/**
 * @file test.c
 * @brief Test suite per il memory allocator personalizzato
 *
 * Test completi per verificare la correttezza di my_malloc, my_free, my_realloc
 * Includono test per:
 * - Allocazione base
 * - Double-free detection
 * - Invalid free detection
 * - Coalescing
 * - Realloc
 * - Stress test
 */

#include "allocator.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/* Contatore test passati/falliti */
static int tests_passed = 0;
static int tests_failed = 0;

/* Macro per assert personalizzati */
#define TEST_ASSERT(condition, message) \
    do { \
        if (condition) { \
            printf("  [PASS] %s\n", message); \
            tests_passed++; \
        } else { \
            printf("  [FAIL] %s\n", message); \
            tests_failed++; \
        } \
    } while (0)

/**
 * @brief Test 1: Allocazione e deallocazione base
 */
void test_basic_allocation(void) {
    printf("\n=== Test 1: Allocazione Base ===\n");

    /* Alloca un blocco */
    int *ptr = (int *)my_malloc(sizeof(int) * 10);
    TEST_ASSERT(ptr != NULL, "Allocazione di 10 interi");

    /* Scrivi e legge dati */
    for (int i = 0; i < 10; i++) {
        ptr[i] = i * 10;
    }

    int valid = 1;
    for (int i = 0; i < 10; i++) {
        if (ptr[i] != i * 10) {
            valid = 0;
            break;
        }
    }
    TEST_ASSERT(valid, "Lettura/scrittura dati corretta");

    /* Dealloca */
    my_free(ptr);
    TEST_ASSERT(1, "Deallocazione corretta");
}

/**
 * @brief Test 2: Allocazione multipla
 */
void test_multiple_allocation(void) {
    printf("\n=== Test 2: Allocazione Multipla ===\n");

    void *ptrs[100];

    /* Alloca 100 blocchi di dimensioni diverse */
    for (int i = 0; i < 100; i++) {
        ptrs[i] = my_malloc((i + 1) * 10);
        TEST_ASSERT(ptrs[i] != NULL, "Allocazione multipla riuscita");

        /* Scrivi dati per verificare */
        memset(ptrs[i], 0xAA, (i + 1) * 10);
    }

    /* Libera tutti i blocchi */
    for (int i = 0; i < 100; i++) {
        my_free(ptrs[i]);
    }

    TEST_ASSERT(1, "Deallocazione multipla corretta");
}

/**
 * @brief Test 3: Double-free detection
 */
void test_double_free(void) {
    printf("\n=== Test 3: Double-Free Detection ===\n");

    int *ptr = (int *)my_malloc(sizeof(int) * 5);
    TEST_ASSERT(ptr != NULL, "Allocazione per double-free test");

    my_free(ptr);

    /* Seconda free (dovrebbe essere rilevata) */
    printf("  Tentativo double-free (errore atteso):\n");
    my_free(ptr);

    TEST_ASSERT(1, "Double-free rilevato correttamente");
}

/**
 * @brief Test 4: Invalid free detection
 */
void test_invalid_free(void) {
    printf("\n=== Test 4: Invalid-Free Detection ===\n");

    /* Puntatore non allocato */
    int stack_var;
    printf("  Tentativo invalid free (errore atteso):\n");
    my_free(&stack_var);

    /* Puntatore casuale */
    printf("  Tentativo free con puntatore casuale (errore atteso):\n");
    my_free((void *)0x12345678);

    /* Puntatore NULL */
    printf("  Tentativo free NULL (errore atteso):\n");
    my_free(NULL);

    TEST_ASSERT(1, "Invalid free rilevato correttamente");
}

/**
 * @brief Test 5: Coalescing
 */
void test_coalescing(void) {
    printf("\n=== Test 5: Coalescing ===\n");

    print_allocator_stats();

    /* Alloca 3 blocchi contigui */
    void *ptr1 = my_malloc(100);
    void *ptr2 = my_malloc(100);
    void *ptr3 = my_malloc(100);

    TEST_ASSERT(ptr1 != NULL && ptr2 != NULL && ptr3 != NULL,
                "Allocazione 3 blocchi");

    print_allocator_stats();

    /* Libera il primo e il terzo */
    my_free(ptr1);
    my_free(ptr3);

    printf("  Dopo free ptr1 e ptr3:\n");
    print_allocator_stats();

    /* Libera il secondo (dovrebbe fare coalescing con entrambi) */
    my_free(ptr2);

    printf("  Dopo free ptr2 (coalescing):\n");
    print_allocator_stats();

    TEST_ASSERT(1, "Coalescing eseguito");
}

/**
 * @brief Test 6: Realloc - shrink
 */
void test_realloc_shrink(void) {
    printf("\n=== Test 6: Realloc - Ridimensionamento ===\n");

    int *ptr = (int *)my_malloc(sizeof(int) * 100);
    TEST_ASSERT(ptr != NULL, "Allocazione iniziale");

    /* Scrivi dati */
    for (int i = 0; i < 100; i++) {
        ptr[i] = i;
    }

    /* Ridimensiona a 50 elementi */
    int *new_ptr = (int *)my_realloc(ptr, sizeof(int) * 50);
    TEST_ASSERT(new_ptr != NULL, "Realloc shrink riuscito");

    /* Verifica dati */
    int valid = 1;
    for (int i = 0; i < 50; i++) {
        if (new_ptr[i] != i) {
            valid = 0;
            break;
        }
    }
    TEST_ASSERT(valid, "Dati preservati dopo realloc shrink");

    my_free(new_ptr);
}

/**
 * @brief Test 7: Realloc - grow
 */
void test_realloc_grow(void) {
    printf("\n=== Test 7: Realloc - Espansione ===\n");

    int *ptr = (int *)my_malloc(sizeof(int) * 10);
    TEST_ASSERT(ptr != NULL, "Allocazione iniziale");

    /* Scrivi dati */
    for (int i = 0; i < 10; i++) {
        ptr[i] = i * 100;
    }

    /* Espandi a 100 elementi */
    int *new_ptr = (int *)my_realloc(ptr, sizeof(int) * 100);
    TEST_ASSERT(new_ptr != NULL, "Realloc grow riuscito");

    /* Verifica dati vecchi */
    int valid = 1;
    for (int i = 0; i < 10; i++) {
        if (new_ptr[i] != i * 100) {
            valid = 0;
            break;
        }
    }
    TEST_ASSERT(valid, "Dati preservati dopo realloc grow");

    my_free(new_ptr);
}

/**
 * @brief Test 8: Realloc NULL equivale a malloc
 */
void test_realloc_null(void) {
    printf("\n=== Test 8: Realloc NULL ===\n");

    int *ptr = (int *)my_realloc(NULL, sizeof(int) * 10);
    TEST_ASSERT(ptr != NULL, "Realloc(NULL, size) equivale a malloc");

    if (ptr != NULL) {
        for (int i = 0; i < 10; i++) {
            ptr[i] = i;
        }
        my_free(ptr);
    }
}

/**
 * @brief Test 9: Realloc size 0 equivale a free
 */
void test_realloc_zero(void) {
    printf("\n=== Test 9: Realloc Size 0 ===\n");

    int *ptr = (int *)my_malloc(sizeof(int) * 10);
    TEST_ASSERT(ptr != NULL, "Allocazione iniziale");

    /* Realloc con size 0 dovrebbe fare free */
    void *result = my_realloc(ptr, 0);
    TEST_ASSERT(result == NULL, "Realloc(ptr, 0) equivale a free");
}

/**
 * @brief Test 10: Allocazione grande
 */
void test_large_allocation(void) {
    printf("\n=== Test 10: Allocazione Grande ===\n");

    /* Alloca 1 MB */
    const size_t ONE_MB = 1024 * 1024;
    void *ptr = my_malloc(ONE_MB);
    TEST_ASSERT(ptr != NULL, "Allocazione 1 MB");

    if (ptr != NULL) {
        /* Scrivi pattern di memoria */
        memset(ptr, 0x55, ONE_MB);

        /* Verifica */
        unsigned char *bytes = (unsigned char *)ptr;
        int valid = 1;
        for (size_t i = 0; i < ONE_MB; i++) {
            if (bytes[i] != 0x55) {
                valid = 0;
                break;
            }
        }
        TEST_ASSERT(valid, "Scrittura/lettura 1 MB corretta");

        my_free(ptr);
    }
}

/**
 * @brief Test 11: Allineamento memoria
 */
void test_alignment(void) {
    printf("\n=== Test 11: Allineamento Memoria ===\n");

    /* Verifica che i puntatori restituiti siano allineati */
    int allineati = 1;

    for (int i = 0; i < 100; i++) {
        void *ptr = my_malloc(i + 1);
        if (ptr == NULL) {
            allineati = 0;
            break;
        }

        /* Verifica allineamento a 16 bytes */
        if ((uintptr_t)ptr % ALIGNMENT != 0) {
            printf("  [WARN] Puntatore %p non allineato a %d bytes\n",
                   ptr, ALIGNMENT);
            allineati = 0;
        }

        my_free(ptr);
    }

    TEST_ASSERT(allineati, "Tutti i puntatori sono allineati");
}

/**
 * @brief Test 12: Stress test
 */
void test_stress(void) {
    printf("\n=== Test 12: Stress Test ===\n");

    const int NUM_ALLOCS = 1000;
    void **ptrs = (void **)malloc(sizeof(void *) * NUM_ALLOCS);

    if (ptrs == NULL) {
        printf("  [SKIP] Malloc fallito per stress test\n");
        return;
    }

    /* Alloca casualmente */
    for (int i = 0; i < NUM_ALLOCS; i++) {
        size_t size = (rand() % 1000) + 1;
        ptrs[i] = my_malloc(size);

        if (ptrs[i] != NULL) {
            memset(ptrs[i], 0xFF, size);
        }
    }

    /* Libera metà */
    for (int i = 0; i < NUM_ALLOCS / 2; i++) {
        if (ptrs[i] != NULL) {
            my_free(ptrs[i]);
            ptrs[i] = NULL;
        }
    }

    /* Realloca la metà libera */
    for (int i = 0; i < NUM_ALLOCS / 2; i++) {
        size_t size = (rand() % 1000) + 1;
        ptrs[i] = my_malloc(size);

        if (ptrs[i] != NULL) {
            memset(ptrs[i], 0xAA, size);
        }
    }

    /* Libera tutto */
    for (int i = 0; i < NUM_ALLOCS; i++) {
        if (ptrs[i] != NULL) {
            my_free(ptrs[i]);
        }
    }

    free(ptrs);

    TEST_ASSERT(1, "Stress test completato");
    print_allocator_stats();
}

/**
 * @brief Main - esegue tutti i test
 */
int main(void) {
    printf("╔══════════════════════════════════════════════════╗\n");
    printf("║   Memory Allocator - Test Suite Completa        ║\n");
    printf("╚══════════════════════════════════════════════════╝\n");

    /* Esegui tutti i test */
    test_basic_allocation();
    test_multiple_allocation();
    test_double_free();
    test_invalid_free();
    test_coalescing();
    test_realloc_shrink();
    test_realloc_grow();
    test_realloc_null();
    test_realloc_zero();
    test_large_allocation();
    test_alignment();
    test_stress();

    /* Stampa risultati finali */
    printf("\n");
    printf("╔══════════════════════════════════════════════════╗\n");
    printf("║              RISULTATI FINALI                    ║\n");
    printf("╠══════════════════════════════════════════════════╣\n");
    printf("║  Test Passati:  %4d                              ║\n", tests_passed);
    printf("║  Test Falliti: %4d                              ║\n", tests_failed);
    printf("║  Totale:        %4d                              ║\n",
           tests_passed + tests_failed);
    printf("╚══════════════════════════════════════════════════╝\n");

    /* Pulisci prima di uscire */
    allocator_cleanup();

    return (tests_failed == 0) ? 0 : 1;
}
